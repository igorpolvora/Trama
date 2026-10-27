from django.urls import path

from .views import desafio_concluir, desafio_criar, desafio_participar, desafios_lista

app_name = "desafios"

urlpatterns = [
    path("", desafios_lista, name="lista"),
    path("novo/", desafio_criar, name="criar"),
    path("<int:pk>/participar/", desafio_participar, name="participar"),
    path("<int:pk>/concluir/", desafio_concluir, name="concluir"),
]
