from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from .models import AdesaoCompeticao, EventoPontos, Temporada


@login_required
def ranking(request):
    temporada_ativa = Temporada.objects.order_by("-fim").first()
    adesoes = AdesaoCompeticao.objects.filter(opt_in=True)

    if temporada_ativa:
        adesoes = adesoes.filter(temporada=temporada_ativa)

    dados = []
    for adesao in adesoes.select_related("usuario", "temporada"):
        total = (
            EventoPontos.objects.filter(usuario=adesao.usuario)
            .aggregate(total=Sum("quantidade"))["total"]
            or 0
        )
        dados.append({
            "usuario": adesao.usuario,
            "total": total,
            "temporada": adesao.temporada,
        })

    dados.sort(key=lambda item: item["total"], reverse=True)
    return render(request, "pontuacao/ranking.html", {
        "temporada": temporada_ativa,
        "dados": dados,
    })
