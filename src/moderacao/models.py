from django.db import models


class Denuncia(models.Model):
    autor = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="denuncias")
    alvo = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="denunciado_por")
    motivo = models.CharField(max_length=200)
    resolvida = models.BooleanField(default=False)

    class Meta:
        app_label = "moderacao"


class DecisaoModeracao(models.Model):
    denuncia = models.OneToOneField("moderacao.Denuncia", on_delete=models.CASCADE, related_name="decisao")
    responsavel = models.ForeignKey("contas.Usuario", on_delete=models.DO_NOTHING, related_name="decisoes")
    observacao = models.TextField(blank=True)

    class Meta:
        app_label = "moderacao"


class RegistroAuditoria(models.Model):
    ator = models.ForeignKey("contas.Usuario", on_delete=models.DO_NOTHING, related_name="auditorias")
    acao = models.CharField(max_length=120)
    alvo = models.CharField(max_length=200)
    momento = models.DateTimeField(auto_now_add=True)
    finalidade = models.TextField(blank=True)

    class Meta:
        app_label = "moderacao"
