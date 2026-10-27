from django.urls import path

from .views import comentario_excluir, conteudo_detalhe, conteudo_novo, feed

app_name = "comunidade"

urlpatterns = [
    path("feed/", feed, name="feed"),
    path("novo/", conteudo_novo, name="novo"),
    path("<int:pk>/", conteudo_detalhe, name="detalhe"),
    path("comentario/<int:pk>/excluir/", comentario_excluir, name="comentario-excluir"),
]
