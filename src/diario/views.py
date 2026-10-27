from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from acesso.visibility import visiveis_para
from .forms import MetaEstudoForm, RegistroEstudoForm
from .models import MetaEstudo, RegistroEstudo


@login_required
def diario_list(request):
    registros = visiveis_para(RegistroEstudo.objects.select_related("autor"), request.user)
    metas = MetaEstudo.objects.filter(dono=request.user)
    return render(request, "diario/lista.html", {"registros": registros, "metas": metas})


@login_required
def diario_criar(request):
    form = RegistroEstudoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        registro = form.save(commit=False)
        registro.autor = request.user
        registro.save()
        messages.success(request, "Registro salvo com sucesso.")
        return redirect("diario:listar")
    return render(request, "diario/formulario.html", {"form": form, "titulo": "Novo registro"})


@login_required
def diario_editar(request, pk):
    registro = get_object_or_404(RegistroEstudo, pk=pk, autor=request.user)
    form = RegistroEstudoForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registro atualizado.")
        return redirect("diario:listar")
    return render(request, "diario/formulario.html", {"form": form, "titulo": "Editar registro"})


@login_required
def diario_excluir(request, pk):
    registro = get_object_or_404(RegistroEstudo, pk=pk, autor=request.user)
    if request.method == "POST":
        registro.delete()
        messages.success(request, "Registro removido.")
        return redirect("diario:listar")
    return render(request, "diario/confirmar_exclusao.html", {"registro": registro})


@login_required
def meta_criar(request):
    form = MetaEstudoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        meta = form.save(commit=False)
        meta.dono = request.user
        meta.save()
        messages.success(request, "Meta salva.")
        return redirect("diario:listar")
    return render(request, "diario/meta_formulario.html", {"form": form, "titulo": "Nova meta"})


@login_required
def meta_editar(request, pk):
    meta = get_object_or_404(MetaEstudo, pk=pk, dono=request.user)
    form = MetaEstudoForm(request.POST or None, instance=meta)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Meta atualizada.")
        return redirect("diario:listar")
    return render(request, "diario/meta_formulario.html", {"form": form, "titulo": "Editar meta"})
