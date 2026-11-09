# Progresso do projeto

## Estado atual

- Etapa: 6/6 — Participação única e consolidação de duplicatas.
- Implementação: UniqueConstraint(usuario, desafio), migração de duplicatas e testes históricos/concorrentes de inscrição. Manter concluída de menor ID se houver; senão pendente de menor ID. Eventos de pontos intactos, sem créditos retroativos. Reverter remove unicidade, mas não recupera IDs eliminados: recuperação exige backup. Regra de consolidação aprovada explicitamente pelo responsável em 2026-11-09 nesta sessão.
- Verificação deste estado intermediário: SQLite: 40 descobertos, 38 aprovados, 2 ignorados, 106.560 s, saída 0; PostgreSQL: 40 descobertos, 40 aprovados, 0 ignorados, 106.190 s, saída 0
- Git: histórico local organizado em commits na branch main; nenhum push autorizado.
- Bancos: somente descartáveis; banco pessoal não utilizado.
- Decisões D06/D09/D10 e demais condições de piloto não foram encerradas.
- Como verificar: `python scripts/verificar`; PostgreSQL exige servidor descartável, banco vazio explícito e variáveis POSTGRES_HOST/PORT/USER/PASSWORD conforme README.

## Diário de evolução

### 2026-11-09 — Lote local 1: Diagnóstico e auditoria históricos
- Escopo: Registrar diagnóstico e auditoria como retratos históricos anteriores aos commits de correção; sem mudança funcional.
- Verificação do estado intermediário: Verificador Bash legado: documentação aprovada (saída 0). Não executa suíte nem utiliza bancos; verificação completa disponível a partir do commit de instalação.
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — AUDIT-01: duas auditorias independentes
- Status: auditoria concluída; validação funcional parcial por bloqueio de preparação dos testes PostgreSQL.
- Requisitos vinculados: RNF-05/06/11, CA-07/08/14/27, instalação e rastreabilidade.
- Objetivo e implementação: dois subagentes em paralelo, após correção de desafios; somente leitura do repositório e probes em ambientes/bancos descartáveis. Achados no [relatório](./AUDITORIA-2026-11-09.md).
- Arquivos afetados: relatório e progresso consolidados pelo agente principal; subagentes não editaram arquivos versionados.
- Testes executados e resultado: instalação nova e pip check OK; SQLite 20/20; descoberta padrão zero; migrate 22 em SQLite/PostgreSQL, mas sete tabelas ausentes; probes HTTP de visibilidade e IDOR executados.
- Testes não executados e motivo: suíte PostgreSQL detecta 20 mas falha preparando FK de usuário; contorno diagnóstico dos oito testes também falhou preparando FK auth_group. Concorrência não exercitada.
- Problemas encontrados e soluções adotadas: apenas registrados; sem correções durante auditoria. PostgreSQL temporário encerrado, banco local não utilizado.
- Decisões tomadas / ADRs: nenhuma; efeitos de comentários após bloqueio/perda de acesso continuam D06.
- Riscos, limitações e pendências: migrações, GET com efeitos e distinção 302/404 prioritários; detalhes e limites no relatório.
- Git: branch `main`, base `5bbd7b2`, não commitado.
- Próxima ação sugerida: completar migrações e validar suíte PostgreSQL antes de ampliar funções.

### 2026-11-09 — Lote local 2: Instalação por migrações e verificação isolada
- Escopo: Migrações iniciais de diário, amizades e moderação; verificador Python com checks, migrações normais, tabelas e descoberta em src; bancos descartáveis separados.
- Verificação do estado intermediário: SQLite: 16 descobertos, 16 aprovados, 0 ignorados, 80.638 s, saída 0; PostgreSQL: 16 descobertos, 16 aprovados, 0 ignorados, 78.390 s, saída 0
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — FIX-INSTALL-01: migrações completas e suíte nos dois bancos
- Status: concluída.
- Requisitos vinculados: fundação técnica, RF03/RF08/RF14 (persistência dos modelos existentes), CA-15/CA-27 (regressões), RNF-05/06 (testes existentes).
- Objetivo e implementação: instalação normal em banco vazio; três migrações iniciais com dependência do usuário e verificador Python que confere documentos, checks, migrações, tabelas e suíte descoberta em src.
- Arquivos afetados: migrações e inicializadores de diário/amizades/moderação; scripts/verificar; README, changelog, arquitetura, roadmap e progresso.
- Testes executados e resultado: 20 encontrados e 20 aprovados por banco (SQLite 78,878 s; PostgreSQL 18 76,132 s). Quatro testes da rota de conclusão aprovados nos dois. Instalação com 25 migrações e 26 tabelas de modelos; recusa de banco preenchido confirmada.
- Testes não executados e motivo: migração de banco preexistente fora do escopo; concorrência real e demais fluxos sem novos testes neste incremento.
- Problemas encontrados e soluções adotadas: ausência de migrações resolvida sem sincronização manual; descoberta zero corrigida no comando de verificação com diretório explícito e falha em suíte vazia.
- Decisões tomadas / ADRs: nenhuma decisão de produto ou stack alterada; modelos existentes preservados.
- Riscos, limitações e pendências: reverter migrações iniciais apaga tabelas; não aplicar em banco preexistente sem conferir esquema/backup. Demais achados da auditoria continuam abertos.
- Git: branch main, base 5bbd7b2, não commitado.
- Próxima ação sugerida: proteção POST/CSRF e CA-07 em incremento separado.

### 2026-11-09 — Lote local 3: Conclusão atômica, POST/CSRF e concorrência de desafios
- Escopo: Identificador do usuário corrigido, transação conjunta de conclusão/pontos e select_for_update; participar/concluir exigem POST/CSRF com formulários. Testes de primeira conclusão, repetição, rollback, autorização e concorrência PostgreSQL.
- Verificação do estado intermediário: SQLite: 24 descobertos, 23 aprovados, 1 ignorados, 102.341 s, saída 0; PostgreSQL: 24 descobertos, 24 aprovados, 0 ignorados, 99.776 s, saída 0
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — FIX-CSRF-DESAFIOS: POST e conclusão concorrente
- Status: concluída.
- Requisitos vinculados: RF10, RNF-11, CA-15, CA-27.
- Objetivo e implementação: require_POST nas rotas de participação/conclusão; links convertidos em formulários CSRF; regras existentes preservadas.
- Arquivos afetados: src/desafios/views.py, src/desafios/tests.py, templates/desafios/lista.html e documentos de changelog, arquitetura, segurança, roadmap e progresso.
- Testes executados e resultado: scripts/verificar SQLite 31 descobertos, 30 aprovados + 1 skip PostgreSQL (114,812 s); PostgreSQL 31 aprovados (101,127 s); concorrência isolada 1 aprovado (2,025 s). Checks, migrações e tabelas passaram.
- Testes não executados e motivo: concorrência ignorada no SQLite por não oferecer os locks PostgreSQL necessários; inscrição simultânea e navegador fora do escopo.
- Problemas encontrados e soluções adotadas: sem duplicação/erro na conclusão simultânea; preservado select_for_update dentro da transação existente. Instrumentação do teste observa conexões dentro das requisições e espera de ambas pela mesma linha.
- Decisões tomadas / ADRs: nenhuma; pontuação e regras atuais preservadas.
- Riscos, limitações e pendências: outras ações e decisões de produto não alteradas; banco local preservado.
- Git: main, base 5bbd7b2, não commitado.
- Próxima ação sugerida: CA-07 da comunidade em incremento separado.

### 2026-11-09 — FIX-CA15: conclusão atômica de desafios
- Status: correção validada em SQLite; validação PostgreSQL pendente.
- Requisitos vinculados: RF10, CA-15, CA-27, RNF-05.
- Objetivo e implementação: corrigir falha na rota de conclusão e garantir que participação e pontos persistam juntos; idempotência mantida no serviço existente.
- Arquivos afetados: views e testes de desafios, changelog, arquitetura, roadmap e progresso.
- Testes executados e resultado: reprodução HTTP antes da correção (3 erros/4 testes); depois, oito testes de desafios/pontuação aprovados e dependências consistentes (`pip check`).
- Testes não executados e motivo: PostgreSQL e concorrência real ainda sem ambiente de teste verificado.
- Problemas encontrados e soluções adotadas: atributo inexistente corrigido; gravações reunidas em transação; teste injeta exceção depois de inserir evento e confirma reversão de evento e participação.
- Decisões tomadas / ADRs: nenhuma decisão de produto alterada; regra e método HTTP existentes preservados.
- Riscos, limitações e pendências: mutação por GET continua pendente; regras finais D09/D10 e validação PostgreSQL abertas.
- Git: branch `main`, base `5bbd7b2`, não commitado.
- Próxima ação sugerida: priorizar auditorias e proteção contra mutação por GET.

### 2026-11-09 — Lote local 4: POST/CSRF nas ações de amizade
- Escopo: Solicitar/aceitar/recusar amizade exigem POST/CSRF, com formulários de resposta e filtros de titularidade preservados. Sete regressões com CSRF habilitado.
- Verificação do estado intermediário: SQLite: 31 descobertos, 30 aprovados, 1 ignorados, 108.341 s, saída 0; PostgreSQL: 31 descobertos, 31 aprovados, 0 ignorados, 106.571 s, saída 0
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — FIX-CSRF-AMIZADES: ações de amizade por POST
- Status: concluída.
- Requisitos vinculados: RF08, RNF-11, CA-27.
- Objetivo e implementação: eliminar mutações por GET em solicitar/responder amizade, com formulários POST/CSRF para aceitar/recusar e permissões existentes preservadas.
- Arquivos afetados: src/amizades/views.py, src/amizades/tests.py, templates/amizades/lista.html, CHANGELOG.md, docs/ROADMAP.md, docs/SECURITY.md e este progresso.
- Testes executados e resultado: sete regressões HTTP de método/token/autorização e suíte completa; 27 encontrados e aprovados em cada banco (SQLite 109,786 s, PostgreSQL 18 99,340 s). Instalação e checks incluídos no comando verificar, sem falhas.
- Testes não executados e motivo: navegador e acessibilidade manual fora do escopo; regressões validam HTML dos formulários e requisições reais pelo cliente Django.
- Problemas encontrados e soluções adotadas: links de resposta substituídos por formulários; views exigem POST sem mudar filtros de titularidade. Rota solicitar não tinha botão existente a atualizar.
- Decisões tomadas / ADRs: nenhuma; sem alterar política de bloqueio, amizade ou decisões de produto.
- Riscos, limitações e pendências: outras mutações por GET e distinção 302/404 da comunidade continuam fora deste incremento.
- Git: branch main, base 5bbd7b2, não commitado.
- Próxima ação sugerida: corrigir CA-07 em incremento separado.

### 2026-11-09 — Lote local 5: CA-07 no detalhe da comunidade
- Escopo: Detalhe busca por ID no queryset de visibilidade; inexistente/inacessível retornam 404 sem redirecionar, conteúdo ou comentários. Sete regressões HTTP e acessos autorizados preservados.
- Verificação do estado intermediário: SQLite: 38 descobertos, 37 aprovados, 1 ignorados, 109.326 s, saída 0; PostgreSQL: 38 descobertos, 38 aprovados, 0 ignorados, 107.077 s, saída 0
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — FIX-CA07: detalhe sem revelar existência
- Status: concluída.
- Requisitos vinculados: RF06, CA-07/08/27, RNF-05/06.
- Objetivo e implementação: usar o queryset de visibilidade diretamente na busca de detalhe, retornando 404 tanto para inexistente como inacessível, sem redirecionar nem processar comentários.
- Arquivos afetados: views e testes da comunidade, changelog, arquitetura, segurança, roadmap e progresso.
- Testes executados e resultado: reprodução inicial 7 testes/3 falhas por 302; após correção, sete regressões aprovadas nos dois bancos. Suíte completa: SQLite 38 descobertos, 37 aprovados + 1 skip (108,264 s); PostgreSQL 38 aprovados (98,996 s). Migrações/checks/tabelas e diff sem erros.
- Testes não executados e motivo: navegador e análise temporal de respostas fora do escopo; teste de concorrência PostgreSQL ignorado no SQLite, como previsto.
- Problemas encontrados e soluções adotadas: consulta original distinguia existência antes de verificar audiência; consulta filtrada unifica o caminho 404. Autor, amigo autorizado e leitor de público continuam com 200.
- Decisões tomadas / ADRs: nenhuma; política de visibilidade preservada.
- Riscos, limitações e pendências: outros achados e D06 continuam abertos; nenhum banco existente migrado.
- Git: main, base 5bbd7b2, não commitado.
- Próxima ação sugerida: selecionar próxima pendência da auditoria em incremento separado.

### 2026-11-09 — Lote local 6: Participação única e consolidação de duplicatas
- Escopo: UniqueConstraint(usuario, desafio), migração de duplicatas e testes históricos/concorrentes de inscrição. Manter concluída de menor ID se houver; senão pendente de menor ID. Eventos de pontos intactos, sem créditos retroativos. Reverter remove unicidade, mas não recupera IDs eliminados: recuperação exige backup. Regra de consolidação aprovada explicitamente pelo responsável em 2026-11-09 nesta sessão.
- Verificação do estado intermediário: SQLite: 40 descobertos, 38 aprovados, 2 ignorados, 106.560 s, saída 0; PostgreSQL: 40 descobertos, 40 aprovados, 0 ignorados, 106.190 s, saída 0
- Git: commit local deste incremento; consultar histórico.

Registros de execução anteriores ao fracionamento (referem-se ao working tree histórico, não ao checkout intermediário):

### 2026-11-09 — FIX-PARTICIPACAO-UNICA
- Status: concluída.
- Requisitos vinculados: RF10, CA-15, RNF-11 (regressões HTTP).
- Objetivo e implementação: garantir unicidade no banco e consolidar duplicatas preservando conclusão e pontos existentes; fluxo inscrição usa get_or_create sem mudança de regra.
- Arquivos afetados: src/desafios/models.py, migrations/0002_participacao_unica.py, test_migrations.py, tests.py; README e documentação de entrega.
- Testes executados e resultado: erro com duplicatas reproduzido em SQLite; corrida de inscrição reproduzida no PostgreSQL antes da restrição. Após correção, migração e inscrição concorrente aprovadas isoladamente (2 testes/4,641 s). Suíte completa SQLite 40 descobertos/38 aprovados/2 skips (164,547 s); PostgreSQL 40 aprovados (163,691 s).
- Testes não executados e motivo: bancos pessoais/produção fora do escopo; concorrência PostgreSQL ignorada no SQLite.
- Problemas encontrados e soluções adotadas: banco permitia dupla inscrição e conclusão retornava MultipleObjectsReturned; restrição única permite ao get_or_create recuperar a participação concorrente. Migração preserva uma conclusão existente e deixa eventos intactos.
- Decisões tomadas / ADRs: preservação autorizada aplicada sem recalcular pontuação; nenhuma regra de produto nova. Divergência histórica sem evento permanece sem concessão retroativa.
- Riscos, limitações e pendências: reversão não recupera IDs removidos; backup exigido para recuperação. Apenas bancos descartáveis usados; nenhum banco real corrigido.
- Git: main, base 5bbd7b2, não commitado.
- Próxima ação sugerida: revisar migração e separar commits.

### 2026-10-26 — ID da tarefa: desenho inicial do MVP
- Status: concluída
- Requisitos vinculados: RF01, RF02, RF03, RF06, RNF-01 a RNF-08, RNF-12, RNF-13, RNF-19, RNF-20
- Objetivo e implementação: leitura dos documentos centrais e início do desenho do produto e da arquitetura. Foram criados os arquivos base de documentação e a estrutura do repositório.
- Arquivos afetados: [README.md](../README.md), [CHANGELOG.md](../CHANGELOG.md), [Trama_Incremento_0.md](../Trama_Incremento_0.md), [docs/PROGRESS.md](./PROGRESS.md), [docs/ROADMAP.md](./ROADMAP.md), [docs/ARCHITECTURE.md](./ARCHITECTURE.md), [docs/SECURITY.md](./SECURITY.md), [docs/DECISIONS/ADR-0001-exemplo.md](./DECISIONS/ADR-0001-exemplo.md), [docs/DECISIONS/PROD-D01-exemplo.md](./DECISIONS/PROD-D01-exemplo.md), [.env.example](../.env.example), [scripts/verificar](../scripts/verificar)
- Testes executados e resultado: estrutura e documentos criados; verificação mínima por listagem do diretório e existência dos arquivos.
- Testes não executados e motivo: não há código funcional ainda nem stack configurada.
- Problemas encontrados e soluções adotadas: muitas decisões do produto ainda estão pendentes e foram explicitadas como bloqueios; não foram convertidas em premissas.
- Decisões tomadas / ADRs: arquitetura recomendada registrada como proposta e não como decisão final; foco em visibilidade centralizada e segurança.
- Riscos, limitações e pendências: ausência de decisão de menor, de cadastro, de retenção e de ranking global; ainda não há infraestrutura ou app Django implementados.
- Git: branch `main`; sem commit, apenas arquivos novos no working tree.
- Próxima ação sugerida: começar o Incremento 0 de infraestrutura e requisitos mínimos de conta e visibilidade.

### 2026-10-26 — ID da tarefa: incremento 2 base do diário
- Status: concluída
- Requisitos vinculados: RF03, RF04, RF06, CA-07, CA-08, CA-09, CA-10, CA-20
- Objetivo e implementação: criar o fluxo mínimo de diário com registros, metas e visibilidade centralizada por audiência. Foram adicionados formulário, listagem, criação, edição e exclusão de registros.
- Arquivos afetados: [src/acesso/visibility.py](../src/acesso/visibility.py), [src/diario/forms.py](../src/diario/forms.py), [src/diario/views.py](../src/diario/views.py), [src/diario/urls.py](../src/diario/urls.py), [src/diario/tests.py](../src/diario/tests.py), [templates/diario/lista.html](../templates/diario/lista.html), [templates/diario/formulario.html](../templates/diario/formulario.html), [templates/diario/meta_formulario.html](../templates/diario/meta_formulario.html), [templates/diario/confirmar_exclusao.html](../templates/diario/confirmar_exclusao.html)
- Testes executados e resultado: `python manage.py test diario` — OK, 3 testes executados com sucesso.
- Testes não executados e motivo: não foi implementado ainda o fluxo de amizades por interface, nem rankings / desafios.
- Problemas encontrados e soluções adotadas: a visibilidade foi centralizada em função única e os acessos foram testados por audiência; não foi assumida regra de ranking nem publicação pública sem decisão.
- Decisões tomadas / ADRs: nenhum item de produto pendente foi tratado como aprovado; o comportamento respeita a política de acesso privado/amigos/público definida no MVP.
- Riscos, limitações e pendências: visibilidade privada, bloqueio e amizade continuam dependentes de evoluções de interface e casos de acesso por link direto e moderação.
- Git: branch `main`; sem commit, apenas arquivos novos no working tree.
- Próxima ação sugerida: avançar para o fluxo de comunidade (conteúdo, feed e comentários) com foco em permissão, denúncia e moderação básica.

### 2026-10-26 — ID da tarefa: incremento 3 base da comunidade
- Status: concluída
- Requisitos vinculados: RF05, RF07, RF08, RF09, RF13, RF14, CA-11, CA-13, CA-14
- Objetivo e implementação: criar o feed de conteúdos, a publicação de textos por audiência, comentários e controle de acesso por visibilidade e amizade. Também foram criadas rotas e testes de feed e comentários.
- Arquivos afetados: [src/comunidade/forms.py](../src/comunidade/forms.py), [src/comunidade/views.py](../src/comunidade/views.py), [src/comunidade/urls.py](../src/comunidade/urls.py), [src/comunidade/tests.py](../src/comunidade/tests.py), [templates/comunidade/feed.html](../templates/comunidade/feed.html), [templates/comunidade/formulario.html](../templates/comunidade/formulario.html), [templates/comunidade/detalhe.html](../templates/comunidade/detalhe.html), [templates/comunidade/confirmar_exclusao.html](../templates/comunidade/confirmar_exclusao.html)
- Testes executados e resultado: `python manage.py test comunidade diario` — OK, 6 testes executados com sucesso.
- Testes não executados e motivo: ainda não há moderação funcional e bloqueio por interface; a lógica de denúncia e resposta está em desenho, não em regra final.
- Problemas encontrados e soluções adotadas: o feed usa a mesma visão de acesso do diário e a regra de visibilidade foi reaproveitada; comentários só são permitidos quando o conteúdo é acessível.
- Decisões tomadas / ADRs: a comunidade respeita a mesma política de privacidade e audiência; qualquer decisão futura sobre denúncia e conteúdo restrito continua pendente.
- Riscos, limitações e pendências: moderação, bloqueio e denúncia requerem regras de produto específicas antes do uso em ambiente real; a base serve ao MVP inicial, mas não substitui revisão de segurança.
- Git: branch `main`; sem commit, apenas arquivos novos no working tree.
- Próxima ação sugerida: avançar para desafios, pontuação e rankings, mantendo os limites de D08, D09 e D10.

### 2026-10-26 — ID da tarefa: incremento 4 base de desafios e pontuação
- Status: concluída
- Requisitos vinculados: RF10, RF11, RF12, CA-15, CA-16, CA-17, CA-18, CA-19, RNF-08
- Objetivo e implementação: criar a base de desafios com inscrição, conclusão e atribuição de pontos por evento idempotente. Também foi adicionado o serviço de registro de pontos, mantendo a regra de que o cliente não define a quantidade de pontos.
- Arquivos afetados: [src/desafios/forms.py](../src/desafios/forms.py), [src/desafios/views.py](../src/desafios/views.py), [src/desafios/urls.py](../src/desafios/urls.py), [src/desafios/tests.py](../src/desafios/tests.py), [src/pontuacao/services.py](../src/pontuacao/services.py), [src/pontuacao/tests.py](../src/pontuacao/tests.py), [templates/desafios/lista.html](../templates/desafios/lista.html), [templates/desafios/formulario.html](../templates/desafios/formulario.html)
- Testes executados e resultado: `python manage.py test comunidade diario desafios pontuacao` — OK, 9 testes executados com sucesso.
- Testes não executados e motivo: rankings globais e temporada de competição continuam pendentes porque D08 e D09 ainda não foram aprovados.
- Problemas encontrados e soluções adotadas: o registro de evento de pontuação foi centralizado em um serviço único com chave de idempotência; isso evita duplicação por requisições repetidas.
- Decisões tomadas / ADRs: a pontuação foi tratada como evento auditável, sem guardar conteúdo do registro, e a competição ficou como base de integração sem estabelecer a regra final de rankings globais.
- Riscos, limitações e pendências: D08 (ranking global), D09 (temporadas e conquistas) e D10 (fraude e moderação) ainda exigem aprovação antes de exportar esse comportamento para a experiência real.
- Git: branch `main`; sem commit, apenas arquivos alterados no working tree.
- Próxima ação sugerida: formalizar a primeira versão de rankings e temporadas, mantendo a competição opcional e os critérios de visibilidade intactos.

### 2026-10-26 — ID da tarefa: integração do ranking e versionamento inicial
- Status: concluída
- Requisitos vinculados: RF10, RF11, RF12, CA-15, CA-16, CA-17, CA-18, CA-19, RNF-08
- Objetivo e implementação: concluir a integração do módulo de pontuação com os fluxos principais, permitindo acesso ao ranking da temporada pela navegação autenticada e validando a ordenação dos usuários por pontos.
- Arquivos afetados: [src/trama/urls.py](../src/trama/urls.py), [templates/contas/home.html](../templates/contas/home.html), [src/pontuacao/tests.py](../src/pontuacao/tests.py), [templates/pontuacao/ranking.html](../templates/pontuacao/ranking.html)
- Testes executados e resultado: `python manage.py test desafios pontuacao` — OK, 4 testes executados com sucesso.
- Testes não executados e motivo: a regra final de ligas, temporadas e ranking global continua pendente de aprovação do produto (D08, D09).
- Problemas encontrados e soluções adotadas: a rota do ranking estava ausente e a página de entrada não expunha a navegação; ambos foram conectados ao fluxo principal sem assumir regras de competição ainda não aprovadas.
- Decisões tomadas / ADRs: o ranking foi tratado como visão mínima da temporada ativa, com opt-in voluntário e ordenação por somatória de eventos de pontuação.
- Riscos, limitações e pendências: sem decisão final de produto, a base de competição continua intencionalmente limitada e não substitui regras de liga, ranking global e moderação.
- Git: branch `main`; commit `598f0ab` registrado com a mensagem `feat(mvp): add challenge and scoring foundation`.
- Próxima ação sugerida: validar a integração completa da competição com a experiência ao incluir o ranking na navegação de autenticação e manter as regras pendentes explícitas.

### 2026-10-26 — ID da tarefa: amizades e reforço do login
- Status: concluída
- Requisitos vinculados: RF02, RF03, RF06, RF07, CA-07, CA-11, CA-12, RNF-05
- Objetivo e implementação: iniciar o módulo de amizades com solicitações, aceite e listagem, e reforçar o fluxo de login para redirecionar usuários autenticados de volta à home.
- Arquivos afetados: [src/contas/views.py](../src/contas/views.py), [src/contas/tests.py](../src/contas/tests.py), [src/amizades/views.py](../src/amizades/views.py), [src/amizades/urls.py](../src/amizades/urls.py), [src/amizades/tests.py](../src/amizades/tests.py), [src/trama/urls.py](../src/trama/urls.py), [templates/contas/home.html](../templates/contas/home.html), [templates/amizades/lista.html](../templates/amizades/lista.html)
- Testes executados e resultado: `python manage.py test contas amizades desafios pontuacao` — OK, 10 testes executados com sucesso.
- Testes não executados e motivo: ainda não há interface completa de busca de usuários nem bloqueio de conta, itens que continuam pendentes de decisão de produto/UX.
- Problemas encontrados e soluções adotadas: o login agora evita o retorno à página de entrada para usuários já autenticados; o módulo de amizades usa o modelo existente e mantém a regra de status pendente/aceita sem criar suposições sobre regras de bloqueio final.
- Decisões tomadas / ADRs: amizade foi tratada como fluxo mínimo de solicitação com aprovação por parte do destinatário, respeitando o modelo do produto sem definir regras de ranking ou moderação.
- Riscos, limitações e pendências: o módulo ainda não cobre busca por usuários, notificações e bloqueio, e a experiência de relacionamento social continua sendo uma base inicial do MVP.
- Git: branch `main`; commit `a90fdf2` registrado com a mensagem `fix(auth): stabilize login tests on Django 5.2`.
- Próxima ação sugerida: avançar para a próxima extensão de rede social, como busca de usuários ou bloqueio, mantendo a visibilidade e a privacidade centralizadas no servidor.
