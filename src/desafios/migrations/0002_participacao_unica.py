from django.db import migrations, models
from django.db.models import Count


def consolidar_participacoes(apps, schema_editor):
    Participacao = apps.get_model("desafios", "ParticipacaoDesafio")
    registros = Participacao.objects.using(schema_editor.connection.alias)
    duplicados = list(
        registros.values("usuario_id", "desafio_id")
        .annotate(total=Count("pk")).filter(total__gt=1)
    )
    for grupo in duplicados:
        participantes = registros.filter(
            usuario_id=grupo["usuario_id"], desafio_id=grupo["desafio_id"]
        )
        # Preservar uma conclusão existente, sem gerar conclusão ou pontos novos.
        manter = participantes.order_by("-concluido", "pk").first()
        participantes.exclude(pk=manter.pk).delete()


class Migration(migrations.Migration):
    dependencies = [("desafios", "0001_initial")]

    operations = [
        migrations.RunPython(consolidar_participacoes, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="participacaodesafio",
            constraint=models.UniqueConstraint(
                fields=("usuario", "desafio"),
                name="participacao_usuario_desafio_unica",
            ),
        ),
    ]
