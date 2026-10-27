from django.db import models


class Amizade(models.Model):
    de = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="amizades_enviadas")
    para = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="amizades_recebidas")
    status = models.CharField(max_length=16, default="pendente")

    class Meta:
        app_label = "amizades"


class Bloqueio(models.Model):
    quem_bloqueou = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="bloqueios_feitos")
    bloqueado = models.ForeignKey("contas.Usuario", on_delete=models.CASCADE, related_name="bloqueios_recebidos")

    class Meta:
        app_label = "amizades"
