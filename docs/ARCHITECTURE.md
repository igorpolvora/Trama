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

- Ainda há decisões pendentes para cadastro, privacidade padrão, ranking global e retenção de dados.
- A feature de ranking competitivo não deve ser implementada como premissa antes de D08 e D09.
- A moderação de conteúdo privado continua dependente de D10.
- O nível de acessibilidade e a revisão jurídica ainda precisam ser explicitados.

## Próximo desenho implementável

O próximo passo é criar a base do Incremento 0: modelagem mínima do usuário, estrutura de apps, controle de acessos e documentação de proteção de dados.
