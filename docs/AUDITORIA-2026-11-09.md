# Correção e auditoria — 2026-11-09

> Documento histórico: registra o working tree da investigação inicial anterior ao fracionamento em commits. Achados e limitações podem ter sido resolvidos pelos commits seguintes; consultar PROGRESS.md e histórico para o estado atual.

## Correção de conclusão de desafios

Base `main`, commit `5bbd7b2`; alterações não commitadas. Ambiente isolado `.venv`, Python 3.14, dependências de `requirements.txt`, Django 5.2.19. Configuração temporária importando settings do projeto e sobrescrevendo banco para SQLite `:memory:` e hosts de teste. Banco local não utilizado.

- Reprodução: quatro regressões HTTP executadas antes da correção; três erros com `AttributeError: 'WSGIRequest' object has no attribute 'user_id'`; autorização por titular passou.
- Correção em [views](../src/desafios/views.py): `request.user.pk`, `transaction.atomic`, consulta da participação com `select_for_update`, atualização limitada a `concluido`.
- [Testes](../src/desafios/tests.py): primeiro GET conclui e registra dez pontos; repetição registra apenas um evento; erro simulado depois da inserção dos pontos reverte evento e conclusão; usuário alheio recebe 404.
- Verificação após correção: `manage.py test desafios pontuacao --settings=trama_test_settings --noinput`: oito testes aprovados, 18,162 s. `pip check`: sem dependências quebradas. `git diff --check`: sem erros.
- Configuração de teste temporária: `from trama.settings import *`; `DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:', 'TEST': {'NAME': ':memory:'}}}`; `ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']`. Adicionar o diretório do módulo ao `PYTHONPATH` e executar o comando com o Python da venv.
- Limites: método GET e quantidade existente preservados; erro inesperado ainda propaga resposta de erro, com rollback. Sem validação de concorrência PostgreSQL nem novas decisões D09/D10.
- Documentos atualizados: changelog, arquitetura, rastreabilidade no roadmap e progresso.

## Auditoria independente de permissões e privacidade

Subagente executado em paralelo com auditor de instalação, após correção. Entrega somente de achados; nenhum arquivo rastreado editado pelo auditor. Probes HTTP temporários em SQLite em memória, com sincronização explícita dos apps sem migrações para permitir os testes de acesso. Isso não comprova instalação normal.

| Prioridade | Achado | Evidência |
| --- | --- | --- |
| Alta | Solicitar/aceitar amizade altera dados por GET, inclusive com bloqueio existente | Confirmado por HTTP com `Client(enforce_csrf_checks=True)`: 302 e estado alterado. [views](../src/amizades/views.py). Falta POST/CSRF; efeitos definitivos de bloqueio dependem D06. |
| Alta | Conteúdo privado existente responde 302, inexistente 404 | Confirmado por HTTP; permite distinguir existência, em desacordo com CA-07. [detalhe](../src/comunidade/views.py). Texto privado não retornado e comentário não criado. |
| Média, decisão D06 | Comentários de pessoa bloqueada permanecem em publicação de terceiro | Nome/texto visíveis em probe HTTP. [consulta](../src/comunidade/views.py) usa todos os comentários. Comportamento confirmado; adequação depende da política pendente. |
| Baixa, decisão D06 | Autor pode excluir comentário próprio depois de perder acesso à publicação | GET 200 e POST exclui; link Cancelar contém ID da publicação, sem texto da publicação/comentário. [view](../src/comunidade/views.py), [template](../templates/comunidade/confirmar_exclusao.html). Não houve acesso demonstrado ao texto privado. |

Resultados positivos confirmados por HTTP: edição/exclusão de diário alheio, edição de meta alheia e exclusão de comentário alheio retornaram 404; amizade aceita liberou leitura; desfazer amizade, bloquear autor/leitor e reduzir audiência revogaram acesso ao conteúdo. Permanece a ressalva do 302 no detalhe. POST em conteúdo privado inacessível não criou comentário.

Limites: probes temporários, sem novos testes persistentes; concorrência e cache externo não exercitados.

## Auditoria de instalação

Ambiente virtual novo em diretório temporário: instalação de todas as dependências declaradas concluída; `pip check` sem conflitos. SQLite vazio separado do banco local.

| Prioridade | Achado | Evidência |
| --- | --- | --- |
| Alta | Instalação com migrações normais fica sem tabelas essenciais | `migrate --noinput` aplicou 22 migrações, mas consulta a `RegistroEstudo` falhou com `no such table`. Diário, amizades e moderação não possuem migrações. Confirmado em SQLite descartável; [modelos diário](../src/diario/models.py), [amizades](../src/amizades/models.py), [moderação](../src/moderacao/models.py). |
| Média | Comando padrão de testes pode dar verde sem testar nada | `manage.py test --noinput` descobriu zero testes; nomes explícitos dos seis módulos descobriram e aprovaram 20 testes em 91,179 s. Confirmado na prática. Código está em `src/`, fora da descoberta padrão a partir da raiz. |
| Média | Runner de testes mascara falta de migrações | Com módulos explícitos, runner sincronizou automaticamente sete tabelas sem migrações, ausentes no banco criado por `migrate` normal. Confirmado na prática; testes verdes não provam instalação completa. |
| Média | Verificação não cobre instalação/testes e README não ensina execução completa | Identificado por leitura de [scripts/verificar](../scripts/verificar) e [README](../README.md); script só confere documentos. |
| Média | Dependências sem resolução travada | Identificado por leitura de [requirements](../requirements.txt), com intervalos e sem lockfile; instalação nova funcionou, mas resolução futura pode variar. |

**Alta — suíte PostgreSQL não consegue preparar o banco de testes. Confirmado na prática:** cluster PostgreSQL 18 temporário, porta própria, banco vazio. `migrate` aplicou as mesmas 22 migrações; consulta ao diário falhou com `relation diario_registroestudo does not exist`. A suíte encontrou 20 testes, mas falhou antes de executá-los: `ProgrammingError: relation contas_usuario does not exist`, na sincronização dos apps sem migrações, cujas FKs dependem do usuário ainda não migrado. Nenhum teste dessa tentativa deve ser contabilizado como executado/aprovado.

Verificação adicional da correção: configuração temporária desativou migrações dos sete apps do projeto para tentar executar os oito testes de desafios/pontuação por sincronização. Também falhou antes dos testes: FK do usuário referenciou `auth_group` ainda inexistente. Não é validação do caminho original nem dos testes no PostgreSQL. Não se ampliou o contorno; a próxima ação é completar as migrações versionadas e repetir a suíte. Cluster temporário encerrado ao final.

## Encerramento

As duas auditorias foram executadas em paralelo, após a correção, sem edições no repositório pelos subagentes. O autor principal consolidou este relatório e atualizou a documentação. Instalação das dependências e `pip check` passaram em venv novo. Não houve bloqueio de infraestrutura remanescente: PostgreSQL 18 descartável foi iniciado; o bloqueio de preparação da suíte decorre do projeto. Não foram testados concorrência real, navegador, cache externo ou acessibilidade. Nenhuma decisão de produto foi aprovada e nenhum commit/deploy foi realizado.
