# Arquitetura do Trama

## Visão geral

A arquitetura proposta para o MVP do Trama segue a recomendação do documento de produto e do manual operacional: Django + PostgreSQL + HTMX, com foco em segurança, visibilidade por servidor e regras de autorização explícitas.

## Princípios de desenho

1. Usuário próprio como base desde o início.
2. Centralização da regra de visibilidade em um único ponto de consulta.
3. Acesso negado deve retornar resposta indistinguível de recurso inexistente.
4. Pontuação tratada como evento auditável, sem armazenamento de conteúdo sensível.
5. Auditoria com metadados e sem texto de registros privados.
6. Regras de negócio e autorização no servidor.

## Estrutura arquitetural sugerida

| App | Responsabilidade |
| --- | --- |
| `contas` | usuário, perfil e interesses |
| `acesso` | visibilidade centralizada |
| `diario` | registros e metas pessoais |
| `amizades` | solicitações, amizades e bloqueios |
| `comunidade` | conteúdos e comentários |
| `moderacao` | denúncias e decisões |
| `desafios` | desafios e concluições |
| `pontuacao` | eventos, temporada, ranking e adesão opcional |

## Regras de visibilidade

O detalhe da comunidade consulta `visiveis_para` antes da busca por ID com `get_object_or_404`. Conteúdo inexistente e conteúdo fora da audiência seguem o mesmo caminho 404, antes de consultar comentários ou processar formulário; o filtro central e suas regras não foram alterados. Sete regressões HTTP cobrem negação sem redirecionamento/exposição e acessos autorizados (CA-07/08/27).

A regra central deve operar como filtro de consulta e de listagem:
- autor sempre consegue ver seu próprio conteúdo;
- conteúdo público é acessível para todos os usuários autenticados ou visitantes, quando aprovado;
- conteúdo para amigos é acessível somente para usuários com amizade aceita;
- conteúdo privado não é exibido em feeds, perfis de terceiros, buscas ou rankings;
- bloqueios e remoção de amizade refletem imediatamente no acesso futuro.

## Fluxo de dados principal

1. Usuário autentica e solicita acesso a recurso.
2. A view ou serviço chama a função de visibilidade.
3. O queryset é filtrado antes da resposta ser montada.
4. A view retorna 404 em caso de ausência de permissão.
5. Auditoria e eventos registrados com metadados.

## Segurança

- Senhas protegidas por hash.
- Sessões e recuperação com expiração e revogação.
- Limitação de tentativas em login e ações sensíveis.
- Autenticação reforçada para administradores.
- Validação de entrada e rejeição de links inválidos.
- Regras de acesso e IDOR testadas no nível de qualquer tipo de recurso.

## Limitações conhecidas

- Instalação vazia validada em SQLite e PostgreSQL 18 em 2026-11-09: 26 migrações aplicadas e 26 tabelas de modelos presentes. Diário, amizades e moderação têm migrações iniciais dependentes do usuário configurado. `scripts/verificar` descobre a suíte em `src`; resultados de cada etapa no progresso; não exige sincronização manual dos modelos.

- Banco existente criado por sincronização manual não foi atualizado. Adoção das novas migrações nesse caso exige avaliação do esquema e backup; reversão das migrações iniciais remove tabelas/dados. Nenhum banco local foi utilizado nas verificações.

- Participação e conclusão de desafios exigem POST/CSRF. A conclusão usa transação conjunta com os pontos e `select_for_update`. Rollback, repetição e autorização foram preservados nos testes HTTP. Concorrência validada em PostgreSQL 18: dois clientes com CSRF válido em conexões distintas aguardaram a mesma linha; ambas as respostas foram 302, com conclusão e um único evento de dez pontos. O teste usa `TransactionTestCase` e é ignorado explicitamente no SQLite, sem suporte equivalente a esse lock.

- Participação em desafio tem unicidade `(usuario, desafio)` no banco. O `get_or_create` existente usa essa restrição para resolver a corrida entre inscrições; não há concessão de pontos na inscrição. Migração 0002 conserva uma linha concluída se existente (senão uma pendente), sem modificar eventos de pontos, que não referenciam IDs de participação. Reversão não restaura IDs redundantes removidos; usar backup para recuperação. Divergências antigas de conclusão/pontos não são recalculadas.

- Ainda há decisões pendentes para cadastro, privacidade padrão, ranking global e retenção de dados.
- A feature de ranking competitivo não deve ser implementada como premissa antes de D08 e D09.
- A moderação de conteúdo privado continua dependente de D10.
- O nível de acessibilidade e a revisão jurídica ainda precisam ser explicitados.

## Próximo desenho implementável

O próximo passo é criar a base do Incremento 0: modelagem mínima do usuário, estrutura de apps, controle de acessos e documentação de proteção de dados.
