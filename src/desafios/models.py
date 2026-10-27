from django.db import models


class Desafio(models.Model):
    nome = models.CharField(max_length=160)
    descricao = models.TextField(blank=True)
    regras = models.TextField(blank=True)

    class Meta:
        app_label = "desafios"


class ParticipacaoDesafio(models.Model):
    desafio = models.ForeignKey("desafios.Desafio", on_delete=models.CASCADE, related_name="participacoes")
    usuario = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="desafios_participados")
    concluido = models.BooleanField(default=False)

    class Meta:
        app_label = "desafios"
