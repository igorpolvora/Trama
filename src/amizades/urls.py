from django.urls import path

from .views import lista_amigos, responder_solicitacao, solicitar_amizade

app_name = "amizades"

urlpatterns = [
    path("", lista_amigos, name="lista"),
    path("solicitar/<int:usuario_id>/", solicitar_amizade, name="solicitar"),
    path("responder/<int:pk>/<str:acao>/", responder_solicitacao, name="responder"),
]
