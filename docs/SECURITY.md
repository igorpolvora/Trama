# Segurança e privacidade do Trama

## Modelo de ameaças

Os riscos principais previstos para o MVP são:
- acesso indevido a conteúdo privado;
- IDOR por troca de identificadores;
- vazamento de dados por feeds, perfis ou rankings;
- reputação e fraude em competições;
- ataques de brute force e abuso de autenticação;
- uso indevido de links e conteúdo malicioso;
- falta de auditoria em ações sensíveis.

## Requisitos de segurança previstos

| Requisito | Descrição | Status |
| --- | --- | --- |
| RNF-01 | Hash de senhas | proposto |
| RNF-02 | Sessões e recuperação seguras | proposto |
| RNF-03 | Rate limiting | proposto |
| RNF-04 | Autenticação reforçada para admin | proposto |
| RNF-05 | Permissão no servidor | proposto |
| RNF-06 | Impedir IDOR | proposto |
| RNF-07 | Preferir componentes consolidados | proposto |
| RNF-08 | Evitar contas múltiplas para fraudar competição | pendente |
| RNF-09 | Minimizar coleta de dados | proposto |
| RNF-10 | Princípio do menor privilégio | proposto |
| RNF-11 | Validação de entradas e saídas | proposto |
| RNF-12 | Manter segredos fora do código | proposto |
| RNF-13 | Telemetria sem conteúdo privado | proposto |
| RNF-16 | Links com http/https e sem prévias automáticas | proposto |
| RNF-17 | Proteção contra SSRF | pendente |
| RNF-18 | Medição sem ler conteúdo privado | proposto |
| RNF-19 | Configuração por ambiente | proposto |
| RNF-20 | Dados fictícios em desenvolvimento/testes | proposto |
| RNF-23 | Backups e recuperação | pendente |
| RNF-25 | Não compartilhar dados reais com IA sem autorização | proposto |
| RNF-26 | Acessibilidade | proposto |

## Controles recomendados

Desafios: participar e concluir exigem POST, com tokens nos formulários e verificação do middleware CSRF. As regressões com CSRF habilitado cobrem GET 405 sem mutação, POST sem token/inválido 403 e POST autorizado. Permissões e dez pontos existentes foram preservados. Teste de concorrência PostgreSQL pela rota verifica exclusão mútua sobre a participação e crédito único (CA-15).

Controle aplicado no módulo de amizades: solicitar e responder (aceitar/recusar) exigem POST e passam pelo middleware CSRF existente. Os formulários de resposta incluem token; login obrigatório e filtro pelo destinatário foram preservados. Sete regressões de rotas usam `Client(enforce_csrf_checks=True)` para método, token e titularidade (RNF-11, CA-27). O controle é restrito a essas ações; outras mutações por GET apontadas na auditoria continuam fora deste incremento.

CA-07 no detalhe da comunidade: busca por ID executada diretamente no queryset filtrado por visibilidade; conteúdo inacessível e inexistente usam o mesmo caminho 404. Regressões HTTP conferem ausência de redirecionamento, título/texto/comentários/autor reservados e igualdade do corpo 404 com DEBUG desligado. Autor, amigo autorizado e leitor de conteúdo público continuam com acesso. POST inacessível não cria comentário. Não houve mudança na política de audiência ou bloqueio.

- Centralizar visibilidade em uma função única.
- Aplicar filtros no queryset e no serviço.
- Não expor conteúdo privado em listas públicas.
- Rejeitar links invalidos e URLs não permitidas.
- Registrar ações administrativas e ações de pontuação em metadados.
- Garantir idempotência de recompensas e eventos.
- Separar ambientes e armazenar segredos em variáveis de ambiente.

## Tratamento de dados

- O projeto deve minimizar a coleta de dados pessoais.
- O conteúdo privado deve ser tratado como dado sensível.
- O registro de auditoria deve manter metadados, não o texto do conteúdo.
- Exportação e exclusão de conta precisam estar documentadas antes do uso real.

## Decisões pendentes

- D01: idade mínima e proteção de menores
- D10: fraude, contas múltiplas e moderação excepcional
- D12: retenção e exclusão
- D15: avaliação jurídica
- D20: nível de acessibilidade

## Status geral

A segurança foi tratada como requisito central desde o desenho do produto. Ainda assim, a política concreta de moderação, retenção e ranking competitivo continua sujeita a aprovação humana antes da implementação funcional.
