from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import EventoPontos
from .services import registrar_evento_pontos

Usuario = get_user_model()


class PontuacaoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="pontos", password="senha123")

    def test_evento_de_pontos_e_idempotente(self):
        evento1, criado1 = registrar_evento_pontos(
            self.usuario,
            "desafio",
            "desafios:estudo",
            10,
            "desafio-1",
        )
        evento2, criado2 = registrar_evento_pontos(
            self.usuario,
            "desafio",
            "desafios:estudo",
            10,
            "desafio-1",
        )

        self.assertTrue(criado1)
        self.assertFalse(criado2)
        self.assertEqual(evento1.pk, evento2.pk)
        self.assertEqual(EventoPontos.objects.filter(usuario=self.usuario).count(), 1)
