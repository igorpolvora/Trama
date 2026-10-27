from django.contrib.auth import get_user_model
from django.test import TestCase

from acesso.visibility import visiveis_para
from amizades.models import Amizade
from comunidade.models import Comentario, Conteudo

Usuario = get_user_model()


class CommunityAccessTests(TestCase):
    def setUp(self):
        self.usuario_a = Usuario.objects.create_user(username="a", password="senha123")
        self.usuario_b = Usuario.objects.create_user(username="b", password="senha123")
        self.usuario_c = Usuario.objects.create_user(username="c", password="senha123")

    def test_conteudo_privado_nao_aparece_para_terceiro(self):
        Conteudo.objects.create(
            autor=self.usuario_a,
            titulo="Privado",
            texto="Conteúdo privado",
            visibilidade="privado",
        )

        qs = visiveis_para(Conteudo.objects.all(), self.usuario_b)
        self.assertEqual(qs.count(), 0)

    def test_conteudo_para_amigos_aparece_para_amigo_aceito(self):
        Conteudo.objects.create(
            autor=self.usuario_a,
            titulo="Amigos",
            texto="Só para amigos",
            visibilidade="amigos",
        )
        Amizade.objects.create(de=self.usuario_a, para=self.usuario_b, status="aceita")

        qs = visiveis_para(Conteudo.objects.all(), self.usuario_b)
        self.assertEqual(qs.count(), 1)

    def test_comentario_aceita_conteudo_publico(self):
        conteudo = Conteudo.objects.create(
            autor=self.usuario_a,
            titulo="Publico",
            texto="Conteúdo público",
            visibilidade="publico",
        )
        comentario = Comentario.objects.create(autor=self.usuario_b, conteudo=conteudo, texto="Bom texto")

        qs = visiveis_para(Conteudo.objects.filter(pk=conteudo.pk), self.usuario_c)
        self.assertTrue(qs.exists())
        self.assertEqual(conteudo.comentarios.count(), 1)
        self.assertEqual(comentario.texto, "Bom texto")
