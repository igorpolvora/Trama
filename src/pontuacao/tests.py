from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from .models import AdesaoCompeticao, EventoPontos, Temporada
from .services import registrar_evento_pontos
from .views import ranking

Usuario = get_user_model()


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class PontuacaoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="pontos", password="senha123")
        self.outro_usuario = Usuario.objects.create_user(username="rival", password="senha123")
        self.temporada = Temporada.objects.create(
            nome="Temporada 1",
            inicio=timezone.now() - timedelta(days=7),
            fim=timezone.now() + timedelta(days=7),
        )
        AdesaoCompeticao.objects.create(usuario=self.usuario, temporada=self.temporada, opt_in=True)
        AdesaoCompeticao.objects.create(usuario=self.outro_usuario, temporada=self.temporada, opt_in=True)

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

    def test_ranking_exibe_usuarios_ordenados_por_pontos(self):
        request = RequestFactory().get("/pontuacao/ranking/")
        request.user = self.usuario
        EventoPontos.objects.create(
            usuario=self.usuario,
            tipo="desafio",
            regra="desafios:estudo",
            quantidade=25,
            idempotencia="desafio-usuario-25",
        )
        EventoPontos.objects.create(
            usuario=self.outro_usuario,
            tipo="desafio",
            regra="desafios:estudo",
            quantidade=40,
            idempotencia="desafio-rival-40",
        )

        response = ranking(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ranking da temporada", response.content)
        self.assertIn(b"rival", response.content)
        self.assertIn(b"pontos", response.content)
