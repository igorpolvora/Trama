from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

Usuario = get_user_model()


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class AutenticacaoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(username="aluno", password="senha123")

    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")

    def test_login_with_valid_credentials_redirects_to_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": "aluno", "password": "senha123"},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_authenticated_user_is_redirected_from_login_page(self):
        self.client.force_login(self.usuario)
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_login_with_invalid_credentials_shows_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": "aluno", "password": "senha-errada"},
            follow=True,
        )

        self.assertContains(response, "Credenciais inv?lidas.")
