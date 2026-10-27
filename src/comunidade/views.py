from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from acesso.visibility import visiveis_para
from amizades.models import Amizade
from .forms import ComentarioForm, ConteudoForm
from .models import Comentario, Conteudo


@login_required
def feed(request):
    conteudos = visiveis_para(Conteudo.objects.select_related("autor"), request.user)
    return render(request, "comunidade/feed.html", {"conteudos": conteudos})


@login_required
def conteudo_novo(request):
    form = ConteudoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        conteudo = form.save(commit=False)
        conteudo.autor = request.user
        conteudo.save()
        messages.success(request, "Conteúdo publicado.")
        return redirect("comunidade:feed")
    return render(request, "comunidade/formulario.html", {"form": form, "titulo": "Novo conteúdo"})


@login_required
def conteudo_detalhe(request, pk):
    conteudo = get_object_or_404(Conteudo.objects.select_related("autor"), pk=pk)
    if not visiveis_para(Conteudo.objects.filter(pk=conteudo.pk), request.user).exists():
        return redirect("comunidade:feed")

    comentarios = conteudo.comentarios.select_related("autor").all()
    form = ComentarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comentario = form.save(commit=False)
        comentario.autor = request.user
        comentario.conteudo = conteudo
        comentario.save()
        messages.success(request, "Comentário adicionado.")
        return redirect("comunidade:detalhe", pk=conteudo.pk)

    return render(
        request,
        "comunidade/detalhe.html",
        {"conteudo": conteudo, "comentarios": comentarios, "form": form},
    )


@login_required
def comentario_excluir(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk, autor=request.user)
    conteudo_pk = comentario.conteudo.pk
    if request.method == "POST":
        comentario.delete()
        messages.success(request, "Comentário removido.")
        return redirect("comunidade:detalhe", pk=conteudo_pk)
    return render(request, "comunidade/confirmar_exclusao.html", {"comentario": comentario})
