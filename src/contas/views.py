from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CadastroForm
from .models import Perfil


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        Perfil.objects.create(usuario=usuario, apelido=usuario.username)
        login(request, usuario)
        messages.success(request, "Cadastro conclu?do.")
        return redirect("home")
    return render(request, "contas/cadastro.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("home")
        messages.error(request, "Credenciais inv?lidas.")
    return render(request, "contas/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    return render(request, "contas/home.html", {"usuario": request.user})
