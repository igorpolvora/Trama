from django.db import transaction

from .models import EventoPontos


@transaction.atomic
def registrar_evento_pontos(usuario, tipo, regra, quantidade, idempotencia):
    """Registra um evento de pontos uma única vez para uma chave de idempotência."""
    evento, criado = EventoPontos.objects.get_or_create(
        usuario=usuario,
        idempotencia=idempotencia,
        defaults={
            "tipo": tipo,
            "regra": regra,
            "quantidade": quantidade,
        },
    )
    return evento, criado
