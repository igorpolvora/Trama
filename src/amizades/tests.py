from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Amizade

Usuario = get_user_model()


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class AmizadesTests(TestCase):
    def setUp(self):
        self.usuario_a = Usuario.objects.create_user(username="aluno_a", password="senha123")
        self.usuario_b = Usuario.objects.create_user(username="aluno_b", password="senha123")

    def test_solicitacao_de_amizade_cria_pedido_pendente(self):
        self.client.force_login(self.usuario_a)

        response = self.client.post(reverse("amizades:solicitar", args=[self.usuario_b.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Amizade.objects.filter(de=self.usuario_a, para=self.usuario_b, status="pendente").exists()
        )

    def test_aceitar_solicitacao_altera_status(self):
        amizade = Amizade.objects.create(de=self.usuario_b, para=self.usuario_a, status="pendente")
        self.client.force_login(self.usuario_a)

        response = self.client.post(reverse("amizades:responder", args=[amizade.pk, "aceitar"]))

        self.assertEqual(response.status_code, 302)
        amizade.refresh_from_db()
        self.assertEqual(amizade.status, "aceita")


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class AmizadesCsrfTests(TestCase):
    """RNF-11 / CA-27: método, CSRF e titularidade pelas rotas reais."""

    def setUp(self):
        self.autor = Usuario.objects.create_user(username="autor")
        self.destinatario = Usuario.objects.create_user(username="destinatario")
        self.terceiro = Usuario.objects.create_user(username="terceiro")
        self.amizade = Amizade.objects.create(de=self.autor, para=self.destinatario)
        self.client = Client(enforce_csrf_checks=True)
        self.client.force_login(self.destinatario)
        self.urls = [
            reverse("amizades:solicitar", args=[self.terceiro.pk]),
            reverse("amizades:responder", args=[self.amizade.pk, "aceitar"]),
            reverse("amizades:responder", args=[self.amizade.pk, "recusar"]),
        ]

    def estado(self):
        return list(Amizade.objects.order_by("pk").values_list("pk", "de_id", "para_id", "status"))

    def token(self):
        response = self.client.get(reverse("amizades:lista"))
        self.assertContains(response, 'name="csrfmiddlewaretoken"', count=2)
        for acao in ("aceitar", "recusar"):
            url = reverse("amizades:responder", args=[self.amizade.pk, acao])
            self.assertContains(response, f'<form method="post" action="{url}">')
            self.assertNotContains(response, f'href="{url}"')
        return self.client.cookies["csrftoken"].value

    def test_rnf11_get_retorna_405_sem_alterar_dados(self):
        antes = self.estado()
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 405)
                self.assertEqual(response.headers["Allow"], "POST")
                self.assertEqual(self.estado(), antes)

    def test_rnf11_post_sem_token_retorna_403_sem_alterar_dados(self):
        antes = self.estado()
        for url in self.urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.post(url).status_code, 403)
                self.assertEqual(self.estado(), antes)

    def test_rnf11_post_token_invalido_retorna_403(self):
        self.token()
        antes = self.estado()
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.post(url, {"csrfmiddlewaretoken": "invalido"})
                self.assertEqual(response.status_code, 403)
                self.assertEqual(self.estado(), antes)

    def test_rnf11_solicitar_com_token_valido(self):
        response = self.client.post(self.urls[0], {"csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, reverse("amizades:lista"))
        self.assertTrue(Amizade.objects.filter(
            de=self.destinatario, para=self.terceiro, status="pendente"
        ).exists())

    def test_rnf11_aceitar_com_token_valido(self):
        response = self.client.post(self.urls[1], {"csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, reverse("amizades:lista"))
        self.amizade.refresh_from_db()
        self.assertEqual(self.amizade.status, "aceita")

    def test_rnf11_recusar_com_token_valido(self):
        response = self.client.post(self.urls[2], {"csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, reverse("amizades:lista"))
        self.assertFalse(Amizade.objects.filter(pk=self.amizade.pk).exists())

    def test_ca27_terceiro_com_token_valido_nao_responde_pedido_alheio(self):
        # Obter token real antes de trocar usuário: o login rotaciona o segredo.
        for usuario in (self.terceiro, self.autor):
            self.client.force_login(usuario)
            # Exibir formulários de outro pedido próprio apenas para obter CSRF.
            pedido = Amizade.objects.create(de=self.destinatario, para=usuario)
            self.client.get(reverse("amizades:lista"))
            token = self.client.cookies["csrftoken"].value
            antes = self.estado()
            for url in self.urls[1:]:
                with self.subTest(usuario=usuario.username, url=url):
                    response = self.client.post(url, {"csrfmiddlewaretoken": token})
                    self.assertEqual(response.status_code, 404)
                    self.assertEqual(self.estado(), antes)
            pedido.delete()
