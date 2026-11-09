from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class ParticipacaoUnicaMigracaoTests(TransactionTestCase):
    """CA-15: consolidar duplicatas sem apagar conclusões nem alterar pontos."""

    def test_migracao_preserva_conclusoes_e_eventos(self):
        anterior = [("desafios", "0001_initial"), ("pontuacao", "0001_initial")]
        atual = [("desafios", "0002_participacao_unica")]
        executor = MigrationExecutor(connection)
        executor.migrate(anterior)
        try:
            apps = executor.loader.project_state(anterior).apps
            Usuario = apps.get_model("contas", "Usuario")
            Desafio = apps.get_model("desafios", "Desafio")
            Participacao = apps.get_model("desafios", "ParticipacaoDesafio")
            Evento = apps.get_model("pontuacao", "EventoPontos")
            usuario = Usuario.objects.create(username="migracao")
            esperados = []
            for indice, estados in enumerate(((False, False), (True, True), (False, True), (True,))):
                desafio = Desafio.objects.create(nome=f"Grupo {indice}")
                linhas = [Participacao.objects.create(
                    usuario_id=usuario.pk, desafio_id=desafio.pk, concluido=estado
                ) for estado in estados]
                manter = next((linha for linha in linhas if linha.concluido), linhas[0])
                esperados.append((manter.pk, usuario.pk, desafio.pk, any(estados)))
                if any(estados):
                    Evento.objects.create(
                        usuario_id=usuario.pk, tipo="desafio", regra=f"conclusao:{desafio.pk}",
                        quantidade=10, idempotencia=f"desafio:{desafio.pk}:{usuario.pk}:conclusao",
                    )
            # Conclusão sem evento: não inferir recompensa nem criar pontos retroativos.
            desafio_sem_pontos = Desafio.objects.create(nome="Sem evento")
            manter = Participacao.objects.create(usuario_id=usuario.pk, desafio_id=desafio_sem_pontos.pk, concluido=True)
            Participacao.objects.create(usuario_id=usuario.pk, desafio_id=desafio_sem_pontos.pk, concluido=False)
            esperados.append((manter.pk, usuario.pk, desafio_sem_pontos.pk, True))
            eventos_antes = list(Evento.objects.order_by("pk").values())

            executor = MigrationExecutor(connection)
            executor.migrate(atual)
            apps = executor.loader.project_state().apps
            Participacao = apps.get_model("desafios", "ParticipacaoDesafio")
            Evento = apps.get_model("pontuacao", "EventoPontos")
            self.assertEqual(
                set(Participacao.objects.values_list("pk", "usuario_id", "desafio_id", "concluido")),
                set(esperados),
            )
            self.assertEqual(list(Evento.objects.order_by("pk").values()), eventos_antes)
            with self.assertRaises(IntegrityError), transaction.atomic():
                Participacao.objects.create(usuario_id=usuario.pk, desafio_id=desafio_sem_pontos.pk)
        finally:
            MigrationExecutor(connection).migrate(atual)
