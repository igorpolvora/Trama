# Trama

Status do projeto: em desenho inicial do MVP, conforme a base documental em [Trama.md](./Trama.md) e os critérios operacionais em [AGENTS.MD](./AGENTS.MD).

## Visão geral

Trama é uma rede social educacional para estudantes registrar estudos, acompanhar progresso, compartilhar conhecimento e participar de desafios, com controle claro de visibilidade e foco em privacidade.

## Objetivo do primeiro ciclo

Definir a base técnica e o desenho de produto para o Incremento 0/1, com foco em:
- contas e autenticação;
- visibilidade privada/amigos/público;
- estrutura de módulos e dados;
- regras de segurança e auditoria;
- documentação de progresso e rastreabilidade.

## Base de decisão

A visão de produto foi tomada como referência a partir de [Trama.md](./Trama.md), com as regras operacionais em [AGENTS.MD](./AGENTS.MD). As decisões pendentes que bloqueiam implementação específica foram registradas no documento do MVP e não foram presumidas neste projeto.

## Escopo inicial recomendado

- Conta e perfil
- Diário de estudos
- Metas pessoais
- Visibilidade por audiência
- Feed simples e filtro por interesse
- Amizades e bloqueios
- Comentários com permissão
- Moderação básica
- Desafios e pontuação, quando aprovados
- Rankings somente após decisões D08/D09/D10

## Estrutura do repositório

```text
Trama/
├── AGENTS.MD
├── Trama.md
├── README.md
├── CHANGELOG.md
├── .env.example
├── Trama_Incremento_0.md
├── scripts/
│   └── verificar
├── docs/
│   ├── PROGRESS.md
│   ├── ROADMAP.md
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── DECISIONS/
│       ├── ADR-0001-exemplo.md
│       └── PROD-D01-exemplo.md
└── src/                 # a ser criado no incremento 0
```

## Stack recomendada

Conforme a recomendação de desenho do MVP e a direção atual do projeto:
- Python
- Django
- PostgreSQL
- HTMX
- django-allauth e controles de autenticação/segurança
- CI com testes automatizados
- ambientes de teste e produção distintos

Observação: a decisão de stack foi tratada como recomendação e não como adoção final sem revisão humana e definição de custos/responsáveis.

## Estado atual do repositório

- Repositório Git inicializado localmente.
- Nenhum commit de código ainda foi realizado.
- A documentação técnica e de produto está sendo estruturada a partir dos documentos de produto e operacional.
- Foi criado um esqueleto técnico inicial em Django para refletir a arquitetura sugerida no MVP, incluindo apps de contas, diário, acessos, comunidade, moderação, desafios e pontuação.

## Próximo passo

Implementar o Incremento 0: fundação técnica, estrutura de diretórios, ambiente, regras de segurança, modelo de visibilidade e documentação mínima de integração.

## Limitações conhecidas

- O projeto ainda depende de decisões humanas pendentes sobre menor de idade, cadastro, visibilidade padrão, ranking global, regras de pontuação e retenção de dados.
- Qualquer entrega funcional deve respeitar os bloqueios documentados em [Trama.md](./Trama.md).
