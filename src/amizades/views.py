from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Amizade


@login_required
def lista_amigos(request):
    amizades = Amizade.objects.filter(
        Q(de=request.user, status="aceita") | Q(para=request.user, status="aceita")
    ).select_related("de", "para")
    solicitacoes = Amizade.objects.filter(para=request.user, status="pendente").select_related("de")

    return render(
        request,
        "amizades/lista.html",
        {"amizades": amizades, "solicitacoes": solicitacoes},
    )


@login_required
def solicitar_amizade(request, usuario_id):
    if usuario_id == request.user.pk:
        messages.info(request, "Você não pode enviar solicitação para si mesmo.")
        return redirect("amizades:lista")

    destino = get_object_or_404(request.user.__class__, pk=usuario_id)
    amizade, criada = Amizade.objects.get_or_create(
        de=request.user,
        para=destino,
        defaults={"status": "pendente"},
    )

    if criada:
        messages.success(request, "Solicitação de amizade enviada.")
    elif amizade.status == "aceita":
        messages.info(request, "Vocês já são amigos.")
    else:
        messages.info(request, "Você já enviou uma solicitação para este usuário.")

    return redirect("amizades:lista")


@login_required
def responder_solicitacao(request, pk, acao):
    amizade = get_object_or_404(Amizade, pk=pk, para=request.user)

    if acao == "aceitar":
        amizade.status = "aceita"
        amizade.save(update_fields=["status"])
        messages.success(request, "Solicitação aceita.")
    elif acao == "recusar":
        amizade.delete()
        messages.info(request, "Solicitação recusada.")
    else:
        messages.error(request, "Ação inválida.")
        return redirect("amizades:lista")

    return redirect("amizades:lista")
