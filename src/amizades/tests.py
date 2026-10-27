from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
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

        response = self.client.get(reverse("amizades:solicitar", args=[self.usuario_b.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Amizade.objects.filter(de=self.usuario_a, para=self.usuario_b, status="pendente").exists()
        )

    def test_aceitar_solicitacao_altera_status(self):
        amizade = Amizade.objects.create(de=self.usuario_b, para=self.usuario_a, status="pendente")
        self.client.force_login(self.usuario_a)

        response = self.client.get(reverse("amizades:responder", args=[amizade.pk, "aceitar"]))

        self.assertEqual(response.status_code, 302)
        amizade.refresh_from_db()
        self.assertEqual(amizade.status, "aceita")
