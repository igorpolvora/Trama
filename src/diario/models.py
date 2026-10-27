from django.db import models


class RegistroEstudo(models.Model):
    autor = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="registros")
    titulo = models.CharField(max_length=200)
    assunto = models.CharField(max_length=120)
    data = models.DateField()
    reflexao = models.TextField()
    tempo_estudado = models.DurationField(null=True, blank=True)
    visibilidade = models.CharField(max_length=16, default="privado")

    class Meta:
        app_label = "diario"


class MetaEstudo(models.Model):
    dono = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="metas")
    descricao = models.CharField(max_length=200)
    progresso = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "diario"
