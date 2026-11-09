from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pontuacao.services import registrar_evento_pontos

from .forms import DesafioForm, ParticipacaoDesafioForm
from .models import Desafio, ParticipacaoDesafio


@login_required
def desafios_lista(request):
    desafios = Desafio.objects.all()
    participacoes = ParticipacaoDesafio.objects.filter(usuario=request.user)
    return render(
        request,
        "desafios/lista.html",
        {"desafios": desafios, "participacoes": participacoes},
    )


@login_required
def desafio_criar(request):
    form = DesafioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        desafio = form.save()
        messages.success(request, "Desafio criado.")
        return redirect("desafios:lista")
    return render(request, "desafios/formulario.html", {"form": form, "titulo": "Novo desafio"})


@login_required
@require_POST
def desafio_participar(request, pk):
    desafio = get_object_or_404(Desafio, pk=pk)
    participacao, created = ParticipacaoDesafio.objects.get_or_create(
        desafio=desafio,
        usuario=request.user,
    )
    if created:
        messages.success(request, "Você entrou no desafio.")
    else:
        messages.info(request, "Você já está participando deste desafio.")
    return redirect("desafios:lista")


@login_required
@require_POST
@transaction.atomic
def desafio_concluir(request, pk):
    participacao = get_object_or_404(
        ParticipacaoDesafio.objects.select_for_update(),
        desafio_id=pk,
        usuario=request.user,
    )
    if not participacao.concluido:
        participacao.concluido = True
        participacao.save(update_fields=["concluido"])
        registrar_evento_pontos(
            usuario=request.user,
            tipo="desafio",
            regra=f"conclusao:{participacao.desafio_id}",
            quantidade=10,
            idempotencia=f"desafio:{participacao.desafio_id}:{request.user.pk}:conclusao",
        )
        messages.success(request, "Desafio concluído e pontos atribuídos.")
    else:
        messages.info(request, "Este desafio já foi concluído.")
    return redirect("desafios:lista")
