# Progresso do projeto

## Estado atual

- Status: em projeto / desenho inicial com base técnica esboçada
- Requisitos vinculados: RF01, RF02, RF03, RF06, RNF-01 a RNF-08, RNF-12, RNF-13, RNF-19, RNF-20
- Objetivo: preparar a base técnica e de documentação para o Incremento 0 e a implementação segura do Incremento 1.
- Arquivos afetados: [README.md](../README.md), [Trama.md](../Trama.md), [AGENTS.MD](../AGENTS.MD), [manage.py](../manage.py), [src/trama/settings.py](../src/trama/settings.py), [src/acesso/visibility.py](../src/acesso/visibility.py), [docs/ROADMAP.md](./ROADMAP.md), [docs/ARCHITECTURE.md](./ARCHITECTURE.md), [docs/SECURITY.md](./SECURITY.md)
- Testes executados: verificação de sintaxe dos módulos Python com `python -m compileall .`.
- Testes pendentes: infraestrutura real, autenticação, visibilidade, IDOR, regras de acessos e auditoria.
- Problemas encontrados e soluções adotadas: decisões de produto pendentes foram mantidas como bloqueios explícitos e não como premissas; a base técnica foi organizada em módulos sugeridos no MVP.
- Decisões tomadas: manter o desenho MVP alinhado ao documento [Trama.md](../Trama.md), priorizar privacidade e visibilidade centralizada, não inventar itens pendentes.
- Riscos e pendências: decisões D01, D02, D08, D09, D10, D12, D14, D15 e D20 ainda exigem aprovação humana.
- Git: branch `main`; sem commits ainda registrados.
- Próxima ação sugerida: validar a estrutura Django inicial, depois avançar para as migrações e autenticação do Incremento 1.

## Diário de evolução

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
