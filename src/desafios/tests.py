from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time
from unittest import skipUnless
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import close_old_connections, connection, connections, transaction
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from pontuacao.models import EventoPontos
from .models import Desafio, ParticipacaoDesafio

Usuario = get_user_model()


class DesafiosCsrfTests(TestCase):
    """RNF-11: POST/CSRF nas rotas de participação e conclusão."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="csrf")
        self.desafio = Desafio.objects.create(nome="Desafio CSRF")
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.usuario)
        self.participar = reverse("desafios:participar", args=[self.desafio.pk])
        self.concluir = reverse("desafios:concluir", args=[self.desafio.pk])

    def token(self, url):
        response = self.client.get(reverse("desafios:lista"))
        self.assertContains(response, f'<form method="post" action="{url}">')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertNotContains(response, f'href="{url}"')
        return self.client.cookies["csrftoken"].value

    def estado(self):
        return (list(ParticipacaoDesafio.objects.values_list("pk", "concluido")),
                list(EventoPontos.objects.values_list("pk", "quantidade")))

    def test_rnf11_get_405_sem_alterar_dados(self):
        antes = self.estado()
        self.assertEqual(self.client.get(self.participar).status_code, 405)
        self.assertEqual(self.estado(), antes)
        ParticipacaoDesafio.objects.create(usuario=self.usuario, desafio=self.desafio)
        antes = self.estado()
        self.assertEqual(self.client.get(self.concluir).status_code, 405)
        self.assertEqual(self.estado(), antes)

    def test_rnf11_post_sem_token_ou_invalido_403(self):
        for url in (self.participar, self.concluir):
            if url == self.concluir:
                ParticipacaoDesafio.objects.create(usuario=self.usuario, desafio=self.desafio)
            self.token(url)
            antes = self.estado()
            for data in ({}, {"csrfmiddlewaretoken": "invalido"}):
                with self.subTest(url=url, data=data):
                    self.assertEqual(self.client.post(url, data).status_code, 403)
                    self.assertEqual(self.estado(), antes)

    def test_rnf11_post_valido_participa_e_conclui(self):
        response = self.client.post(self.participar, {"csrfmiddlewaretoken": self.token(self.participar)})
        self.assertRedirects(response, reverse("desafios:lista"))
        participacao = ParticipacaoDesafio.objects.get(usuario=self.usuario, desafio=self.desafio)
        self.assertFalse(participacao.concluido)
        response = self.client.post(self.concluir, {"csrfmiddlewaretoken": self.token(self.concluir)})
        self.assertRedirects(response, reverse("desafios:lista"))
        participacao.refresh_from_db()
        self.assertTrue(participacao.concluido)
        self.assertEqual(EventoPontos.objects.get(usuario=self.usuario).quantidade, 10)


@skipUnless(connection.vendor == "postgresql", "Concorrência exige locks PostgreSQL")
class ConclusaoConcorrenteTests(TransactionTestCase):
    """CA-15: duas requisições HTTP em conexões PostgreSQL distintas."""

    def test_ca15_duas_conclusoes_simultaneas_creditam_uma_vez(self):
        usuario = Usuario.objects.create_user(username="concorrente")
        desafio = Desafio.objects.create(nome="Concorrência")
        participacao = ParticipacaoDesafio.objects.create(usuario=usuario, desafio=desafio)
        url = reverse("desafios:concluir", args=[desafio.pk])
        clientes = []
        for _ in range(2):
            client = Client(enforce_csrf_checks=True)
            client.force_login(usuario)
            client.get(reverse("desafios:lista"))
            clientes.append((client, client.cookies["csrftoken"].value))
        pids = Queue()

        def buscar_participacao(*args, **kwargs):
            # Medir a conexão dentro da requisição, após os sinais do Django.
            with connection.cursor() as cursor:
                cursor.execute("SET lock_timeout = '15s'")
                cursor.execute("SELECT pg_backend_pid()")
                pids.put(cursor.fetchone()[0])
            return get_object_or_404(*args, **kwargs)

        def concluir(client, token):
            close_old_connections()
            try:
                return client.post(url, {"csrfmiddlewaretoken": token}).status_code
            finally:
                connections.close_all()

        # Segurar a linha até as DUAS requisições aguardarem o lock prova sobreposição.
        with patch("desafios.views.get_object_or_404", side_effect=buscar_participacao), \
                ThreadPoolExecutor(max_workers=2) as executor:
            with transaction.atomic():
                ParticipacaoDesafio.objects.select_for_update().get(pk=participacao.pk)
                futures = [executor.submit(concluir, client, token) for client, token in clientes]
                workers = [pids.get(timeout=10), pids.get(timeout=10)]
                self.assertNotEqual(*workers)
                limite = time.monotonic() + 10
                aguardando = 0
                while time.monotonic() < limite:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT pg_stat_clear_snapshot()")
                        cursor.execute(
                            "SELECT count(*) FROM pg_stat_activity "
                            "WHERE pid IN (%s, %s) AND wait_event_type = 'Lock'",
                            workers,
                        )
                        aguardando = cursor.fetchone()[0]
                    if aguardando == 2:
                        break
                    time.sleep(0.02)
                self.assertEqual(aguardando, 2, "As duas requisições devem disputar a linha")
            self.assertEqual([future.result(timeout=20) for future in futures], [302, 302])
        participacao.refresh_from_db()
        self.assertTrue(participacao.concluido)
        eventos = EventoPontos.objects.filter(usuario=usuario)
        self.assertEqual(eventos.count(), 1)
        self.assertEqual(eventos.get().quantidade, 10)


class ConclusaoDesafioRotaTests(TestCase):
    """CA-15: conclusão, repetição e falha pela rota usada na interface."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="conclusao", password="senha123")
        self.desafio = Desafio.objects.create(nome="Desafio de teste")
        self.participacao = ParticipacaoDesafio.objects.create(
            usuario=self.usuario, desafio=self.desafio
        )
        self.client.force_login(self.usuario)
        self.url = reverse("desafios:concluir", args=[self.desafio.pk])

    def test_ca15_primeira_conclusao_registra_pontos(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("desafios:lista"))
        self.participacao.refresh_from_db()
        self.assertTrue(self.participacao.concluido)
        evento = EventoPontos.objects.get(usuario=self.usuario)
        self.assertEqual(evento.quantidade, 10)
        self.assertEqual(
            evento.idempotencia,
            f"desafio:{self.desafio.pk}:{self.usuario.pk}:conclusao",
        )

    def test_ca15_repetir_conclusao_nao_duplica_pontos(self):
        self.client.post(self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("desafios:lista"))
        self.assertEqual(EventoPontos.objects.filter(usuario=self.usuario).count(), 1)
        self.participacao.refresh_from_db()
        self.assertTrue(self.participacao.concluido)

    def test_ca15_falha_nos_pontos_mantem_participacao_pendente(self):
        from pontuacao.services import registrar_evento_pontos

        def registrar_e_falhar(**kwargs):
            registrar_evento_pontos(**kwargs)
            raise RuntimeError("Falha simulada depois de inserir pontos")

        with patch("desafios.views.registrar_evento_pontos", side_effect=registrar_e_falhar):
            with self.assertRaisesMessage(RuntimeError, "Falha simulada"):
                self.client.post(self.url)
        self.participacao.refresh_from_db()
        self.assertFalse(self.participacao.concluido)
        self.assertFalse(EventoPontos.objects.filter(usuario=self.usuario).exists())

    def test_ca27_nao_conclui_participacao_de_outro_usuario(self):
        outro = Usuario.objects.create_user(username="outro", password="senha123")
        self.client.force_login(outro)
        self.assertEqual(self.client.post(self.url).status_code, 404)
        self.participacao.refresh_from_db()
        self.assertFalse(self.participacao.concluido)
        self.assertFalse(EventoPontos.objects.exists())


class DesafioTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="usuario", password="senha123")
        self.desafio = Desafio.objects.create(
            nome="Estudar 30 minutos",
            descricao="Estudar por 30 minutos hoje",
            regras="Qualquer assunto vale.",
        )

    def test_usuario_pode_participar_do_desafio(self):
        participacao, created = ParticipacaoDesafio.objects.get_or_create(
            desafio=self.desafio,
            usuario=self.usuario,
        )
        self.assertTrue(created)
        self.assertEqual(participacao.desafio, self.desafio)

    def test_conclusao_do_desafio_gera_evento_publico(self):
        participacao = ParticipacaoDesafio.objects.create(desafio=self.desafio, usuario=self.usuario)
        participacao.concluido = True
        participacao.save()

        evento = EventoPontos.objects.create(
            usuario=self.usuario,
            tipo="desafio",
            regra=f"conclusao:{self.desafio.pk}",
            quantidade=10,
            idempotencia=f"desafio:{self.desafio.pk}:{self.usuario.pk}:conclusao",
        )

        self.assertEqual(evento.quantidade, 10)
        self.assertEqual(EventoPontos.objects.filter(usuario=self.usuario).count(), 1)
