# Progresso do projeto

## Estado atual

- Etapa: 1/6 — Diagnóstico e auditoria históricos.
- Implementação: Registrar diagnóstico e auditoria como retratos históricos anteriores aos commits de correção; sem mudança funcional.
- Verificação deste estado intermediário: Verificador Bash legado: documentação aprovada (saída 0). Não executa suíte nem utiliza bancos; verificação completa disponível a partir do commit de instalação.
- Git: histórico local organizado em commits na branch main; nenhum push autorizado.
- Bancos: somente descartáveis; banco pessoal não utilizado.
- Decisões D06/D09/D10 e demais condições de piloto não foram encerradas.
- Como verificar: verificador Bash legado; testes completos ainda indisponíveis nesta etapa.

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
