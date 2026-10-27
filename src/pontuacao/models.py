from django.db import models


class EventoPontos(models.Model):
    usuario = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="eventos_pontos")
    tipo = models.CharField(max_length=80)
    regra = models.CharField(max_length=120)
    quantidade = models.IntegerField(default=0)
    momento = models.DateTimeField(auto_now_add=True)
    idempotencia = models.CharField(max_length=128, unique=True)

    class Meta:
        app_label = "pontuacao"


class Temporada(models.Model):
    nome = models.CharField(max_length=120)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    class Meta:
        app_label = "pontuacao"


class AdesaoCompeticao(models.Model):
    usuario = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="adesoes_competicao")
    temporada = models.ForeignKey("pontuacao.Temporada", on_delete=models.CASCADE, related_name="adesoes")
    opt_in = models.BooleanField(default=True)

    class Meta:
        app_label = "pontuacao"
