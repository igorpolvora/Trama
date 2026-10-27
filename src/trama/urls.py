from django.contrib import admin
from django.urls import include, path

from contas.views import cadastro, home, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
    path("diario/", include(("diario.urls", "diario"), namespace="diario")),
    path("comunidade/", include(("comunidade.urls", "comunidade"), namespace="comunidade")),
    path("desafios/", include(("desafios.urls", "desafios"), namespace="desafios")),
]
