from django.urls import path

from .views import (
    diario_criar,
    diario_editar,
    diario_excluir,
    diario_list,
    meta_criar,
    meta_editar,
)

app_name = "diario"

urlpatterns = [
    path("", diario_list, name="listar"),
    path("novo/", diario_criar, name="criar"),
    path("<int:pk>/editar/", diario_editar, name="editar"),
    path("<int:pk>/excluir/", diario_excluir, name="excluir"),
    path("meta/nova/", meta_criar, name="meta-criar"),
    path("meta/<int:pk>/editar/", meta_editar, name="meta-editar"),
]
