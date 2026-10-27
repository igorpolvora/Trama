from django.db import models


class Conteudo(models.Model):
    autor = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="conteudos")
    tipo = models.CharField(max_length=32, default="texto")
    titulo = models.CharField(max_length=200, blank=True)
    texto = models.TextField(blank=True)
    visibilidade = models.CharField(max_length=16, default="privado")

    class Meta:
        app_label = "comunidade"


class Comentario(models.Model):
    autor = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="comentarios")
    conteudo = models.ForeignKey("comunidade.Conteudo", on_delete=models.CASCADE, related_name="comentarios")
    texto = models.TextField()

    class Meta:
        app_label = "comunidade"
