from django.contrib.auth import get_user_model
from django.test import TestCase

from acesso.visibility import visiveis_para
from amizades.models import Amizade
from diario.models import RegistroEstudo

Usuario = get_user_model()


class VisibilityDiaryTests(TestCase):
    def setUp(self):
        self.usuario_a = Usuario.objects.create_user(username="a", password="senha123")
        self.usuario_b = Usuario.objects.create_user(username="b", password="senha123")
        self.usuario_c = Usuario.objects.create_user(username="c", password="senha123")

    def test_registro_privado_nao_aparece_para_outro_usuario(self):
        RegistroEstudo.objects.create(
            autor=self.usuario_a,
            titulo="Privado",
            assunto="Matemática",
            data="2026-10-26",
            reflexao="Nada para ver",
            visibilidade="privado",
        )

        qs = visiveis_para(RegistroEstudo.objects.all(), self.usuario_b)
        self.assertEqual(qs.count(), 0)

    def test_registro_para_amigos_aparece_para_amigo_aceito(self):
        RegistroEstudo.objects.create(
            autor=self.usuario_a,
            titulo="Amigos",
            assunto="História",
            data="2026-10-26",
            reflexao="Somente amigos",
            visibilidade="amigos",
        )
        Amizade.objects.create(de=self.usuario_a, para=self.usuario_b, status="aceita")

        qs = visiveis_para(RegistroEstudo.objects.all(), self.usuario_b)
        self.assertEqual(qs.count(), 1)

    def test_registro_publico_aparece_para_qualquer_usuario(self):
        RegistroEstudo.objects.create(
            autor=self.usuario_a,
            titulo="Público",
            assunto="Física",
            data="2026-10-26",
            reflexao="Todos podem ver",
            visibilidade="publico",
        )

        qs = visiveis_para(RegistroEstudo.objects.all(), self.usuario_c)
        self.assertEqual(qs.count(), 1)
