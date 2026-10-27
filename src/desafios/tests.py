from django.contrib.auth import get_user_model
from django.test import TestCase

from pontuacao.models import EventoPontos
from .models import Desafio, ParticipacaoDesafio

Usuario = get_user_model()


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
