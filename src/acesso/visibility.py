from django.db.models import Q

PRIVADO = "privado"
AMIGOS = "amigos"
PUBLICO = "publico"


def visiveis_para(queryset, usuario):
    """Centraliza a regra de visibilidade do Trama.

    O autor sempre vê seus próprios registros. Usuários com amizade aceita podem ver itens
    para amigos. Conteúdo público é visível para quem estiver autenticado e não estiver
    bloqueado. Qualquer registro ou conteúdo que o usuário não tenha permissão é filtrado.
    """
    if not getattr(usuario, "is_authenticated", False):
        return queryset.none()

    amigos_ids = list(
        usuario.amizades_recebidas.filter(status="aceita").values_list("de_id", flat=True)
    ) + list(
        usuario.amizades_enviadas.filter(status="aceita").values_list("para_id", flat=True)
    )

    bloqueados = set(
        usuario.bloqueios_feitos.values_list("bloqueado_id", flat=True)
    ) | set(usuario.bloqueios_recebidos.values_list("quem_bloqueou_id", flat=True))

    return (
        queryset.exclude(autor_id__in=bloqueados)
        .filter(
            Q(autor=usuario)
            | Q(visibilidade=PUBLICO)
            | Q(visibilidade=AMIGOS, autor_id__in=amigos_ids)
        )
    )
