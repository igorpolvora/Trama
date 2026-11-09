# Changelog

Todos as mudanças relevantes do projeto serão registradas aqui.

## Unreleased

- Registrados diagnóstico e auditoria como documentos históricos da revisão inicial.

- Participação e conclusão de desafios exigem POST/CSRF, com formulários e testes de rota; teste PostgreSQL de duas conclusões simultâneas confirma crédito único.

- Solicitar, aceitar e recusar amizade agora exigem POST com CSRF; aceitar/recusar usam formulários, com regressões HTTP de método, token e titularidade.

- Adicionadas migrações iniciais de diário, amizades e moderação, validadas em instalações vazias SQLite e PostgreSQL 18.
- Comando `python scripts/verificar` agora valida instalação por migrações, tabelas e descobre a suíte em `src`, com bancos descartáveis separados para instalação e testes.

- Corrigida a conclusão de desafios pela rota: identificador do usuário válido e transação conjunta para participação e pontos, com regressões de repetição, rollback e autorização.

- Estrutura inicial do repositório criada.
- Documentação base do projeto iniciada a partir dos arquivos de produto e operacional.
- Definição inicial de arquitetura do MVP e do Incremento 0.
- Registros de risco e pendências documentados para tomada de decisão humana.
- Esqueleto técnico inicial do Django criado para os módulos de contas, diário, visibilidade, comunidade, moderação, desafios e pontuação.
- Incremento 2 em base funcional: diário com criação, edição, exclusão, metas e visibilidade centralizada por audiência e amizade.
- Incremento 3 em base funcional: feed de comunidade, criação de conteúdo, comentários e testes de visibilidade por audiência.
- Incremento 4 em base funcional: desafios com participação e conclusão, além de eventos de pontuação idempotentes por regra.
- Integração inicial do ranking da temporada à navegação principal e roteamento do módulo de pontuação, com teste de ordenação por pontos.
- Ajuste de compatibilidade do Django para versões suportadas no Python 3.14, resolvendo a falha de renderização no template de login.
- Base inicial do módulo de amizades com solicitações, aceite e listagem, além de proteção para login já autenticado e testes de regressão.

## 0.1.0

- Não publicado ainda.
