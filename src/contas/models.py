from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Modelo de usuário da plataforma.

    O projeto mantém a decisão de cadastro e perfil como pendente (D02), então este modelo
    permanece intencionalmente mínimo e extensível.
    """

    class Meta:
        app_label = "contas"


class Perfil(models.Model):
    usuario = models.OneToOneField("contas.Usuario", on_delete=models.CASCADE, related_name="perfil")
    apelido = models.CharField(max_length=80, blank=True)
    apresentacao = models.TextField(blank=True)

    class Meta:
        app_label = "contas"


class Interesse(models.Model):
    nome = models.CharField(max_length=80)
    usuario = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="interesses")

    class Meta:
        app_label = "contas"


class TokenRecuperacao(models.Model):
    """Token de recuperação de conta para fluxo inicial de autenticação."""

    usuario = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="tokens_recuperacao")
    token = models.CharField(max_length=255, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    class Meta:
        app_label = "contas"
