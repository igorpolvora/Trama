from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from acesso.visibility import visiveis_para
from amizades.models import Amizade
from comunidade.models import Comentario, Conteudo

Usuario = get_user_model()


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
class DetalheConteudoRotaTests(TestCase):
    """CA-07/08/27: inexistente e inacessível sem revelar dados pela rota."""

    def setUp(self):
        self.autor = Usuario.objects.create_user(username="autor_detalhe")
        self.leitor = Usuario.objects.create_user(username="leitor_detalhe")
        self.conteudo = Conteudo.objects.create(
            autor=self.autor, titulo="Titulo reservado", texto="Texto reservado",
            visibilidade="privado",
        )
        Comentario.objects.create(
            autor=self.autor, conteudo=self.conteudo, texto="Comentario reservado"
        )
        self.url = reverse("comunidade:detalhe", args=[self.conteudo.pk])
        self.inexistente = reverse("comunidade:detalhe", args=[self.conteudo.pk + 1000])
        self.client.force_login(self.leitor)

    def assert_oculto(self, response):
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("Location", response.headers)
        for texto in ("Titulo reservado", "Texto reservado", "Comentario reservado", self.autor.username):
            self.assertNotContains(response, texto, status_code=404)

    def test_ca07_privado_existente_retorna_404_sem_conteudo(self):
        self.assert_oculto(self.client.get(self.url))

    def test_ca07_inexistente_retorna_404_sem_redirecionar(self):
        self.assert_oculto(self.client.get(self.inexistente))

    def test_ca07_respostas_indistinguiveis(self):
        existente = self.client.get(self.url)
        ausente = self.client.get(self.inexistente)
        self.assert_oculto(existente)
        self.assert_oculto(ausente)
        self.assertEqual(existente.content, ausente.content)

    def test_ca08_autor_abre_publicacao_privada(self):
        self.client.force_login(self.autor)
        response = self.client.get(self.url)
        self.assertContains(response, self.conteudo.texto)
        self.assertContains(response, "Comentario reservado")

    def test_ca08_amigo_abre_publicacao_para_amigos(self):
        self.conteudo.visibilidade = "amigos"
        self.conteudo.save()
        Amizade.objects.create(de=self.autor, para=self.leitor, status="aceita")
        self.assertContains(self.client.get(self.url), self.conteudo.texto)

    def test_ca08_leitor_abre_publicacao_publica(self):
        self.conteudo.visibilidade = "publico"
        self.conteudo.save()
        self.assertContains(self.client.get(self.url), self.conteudo.texto)

    def test_ca27_post_inacessivel_nao_cria_comentario(self):
        antes = Comentario.objects.count()
        for url in (self.url, self.inexistente):
            with self.subTest(url=url):
                self.assert_oculto(self.client.post(url, {"texto": "Tentativa indevida"}))
        self.assertEqual(Comentario.objects.count(), antes)


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
