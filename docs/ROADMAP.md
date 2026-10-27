# Roadmap do Trama

## Visão geral

Este roadmap organiza o primeiro ciclo de desenvolvimento em incrementos verificáveis, obedecendo ao documento de produto [Trama.md](../Trama.md) e ao manual operacional em [AGENTS.MD](../AGENTS.MD).

## Incrementos propostos

| Incremento | Conteúdo | Status | Observações |
| --- | --- | --- | --- |
| 0 | Fundação técnica e documentação | em desenho | Sem funcionalidades de usuário |
| 1 | Contas e autorização | pendente | Depende de D01, D02 e revisão de autenticação |
| 2 | Diário, metas e visibilidade | pendente | Validação inicial de H1 e parte de H4 |
| 3 | Comunidade e proteção | pendente | Inclui amizades, comentários, bloqueio e moderação básica |
| 4 | Desafios e pontuação | pendente | Depende de D09, D10 e D13 |
| 5 | Rankings e temporadas | pendente | Depende de D08 |
| 6 | Operação e validação de lançamento | pendente | Backups, incidentes, revisão final |

## Matriz de rastreabilidade

| Requisito | Critério de aceitação principal | Teste sugerido | Status |
| --- | --- | --- | --- |
| RF01 | Cadastro e autenticação com regras de segurança | Teste de cadastro e login bem-sucedido | pendente |
| RF02 | Perfil e interesses | Criação e edição de perfil | pendente |
| RF03 | Registro de estudo | Criação, edição e exclusão do diário | pendente |
| RF04 | Metas pessoais | Progresso de meta via registro | pendente |
| RF05 | Conteúdo de comunidade | Criação de texto/link com visibilidade aplicada | pendente |
| RF06 | Visibilidade privado/amigos/público | Matrix de acesso por audiência | pendente |
| RF07 | Feed simples | Feed filtrando itens acessíveis | pendente |
| RF08 | Amizades e bloqueios | Solicitação, aceite e exclusão | pendente |
| RF09 | Comentários | Comentário visível para quem tem acesso | pendente |
| RF10 | Desafios | Participação e conclusão validada | pendente |
| RF11 | Progresso pessoal | Histórico separado de rankings | pendente |
| RF12 | Competição | Ranking opcional e sem conteúdo privado | pendente |
| RF13 | Proteção e bloqueio | Requisição bloqueada e notificação | pendente |
| RF14 | Moderação | Denúncia, análise e decisão | pendente |
| RF15 | Dados da conta | Exportação e exclusão válidas | pendente |
| RNF-01 | Hash de senha | Teste de persistência sem texto puro | pendente |
| RNF-02 | Sessões e recuperação | Sessão expira/revoga corretamente | pendente |
| RNF-03 | Rate limit | Bloqueio por múltiplas tentativas | pendente |
| RNF-05 | Permissão no servidor | Teste de autorização por recurso | pendente |
| RNF-06 | IDOR | Acesso não autorizado por identificador | pendente |
| RNF-11 | Validação e proteção | Rejeição de entrada maliciosa | pendente |
| RNF-16 | Links seguros | URL inválida rejeitada | pendente |
| RNF-26 | Acessibilidade | Fluxos com teclado e leitor de tela | pendente |

## Decisões pendentes e bloqueios relevantes

- D01: idade mínima e proteção de menores
- D02: campos de cadastro e tipo de acesso
- D03: diário e conteúdo são a mesma entidade ou duas entidades
- D04: visibilidade privada como padrão
- D05: visitante sem conta e indexação
- D08: escopo do ranking global
- D09: pontuação, conquistas e temporadas
- D10: fraude, contas múltiplas e moderação excepcional
- D11: moderação e recursos administrativos
- D12: retenção, exportação e exclusão
- D13: sequência de estudo e lembretes
- D14: stack e revisão técnica
- D15: avaliação jurídica
- D20: nível de acessibilidade de referência

## Critérios de entrada para piloto real

Antes do piloto, a revisão recomenda que as seguintes condições estejam ativas:
- D01 e D15 resolvidas;
- RF13, RF14 básico e RF15 funcionando;
- backups com restauração comprovada;
- testes de CA-07, CA-08, CA-27 e CA-28 aprovados;
- D18 e D19 definidos.

## Status geral

A fase atual é de desenho e preparação. A implementação funcional deve começar somente após a base técnica e os bloqueios de produto estarem explicitados e revisados.
