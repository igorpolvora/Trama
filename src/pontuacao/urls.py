from django.urls import path

from .views import ranking

app_name = "pontuacao"

urlpatterns = [
    path("ranking/", ranking, name="ranking"),
]
