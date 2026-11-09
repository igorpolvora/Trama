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

## Verificação da instalação e dos testes

Com Python 3.14 e as dependências declaradas, no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/verificar
```

O comando é Python (substitui o antigo script Bash), funciona a partir de qualquer diretório e usa SQLite temporário para instalar por migrações normais. Confere documentos, checks do Django, ausência de migrações pendentes de geração e todas as tabelas dos modelos; depois descobre a suíte em `src/`, falhando se nenhum teste for encontrado. O banco local não é utilizado. O comando direto `manage.py test` sem indicar o diretório continua fora deste fluxo; para execução avulsa, use `manage.py test src` com configuração de banco isolada.

Para PostgreSQL, prepare um servidor descartável e crie um banco vazio exclusivo para a verificação. Configure `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER` e `POSTGRES_PASSWORD` no ambiente e execute:

```powershell
.\.venv\Scripts\python.exe scripts/verificar --database postgresql --postgres-db trama_verificacao
```

O usuário PostgreSQL precisa criar o banco de testes. O comando recusa banco de instalação com tabelas; aplica migrações apenas no banco explicitamente indicado e usa outro banco com nome aleatório para os testes. O Django remove o banco de testes ao terminar; o banco de instalação PostgreSQL permanece no servidor descartável, sob responsabilidade de quem o criou. Não use o banco pessoal como destino.

As migrações iniciais adicionadas para diário, amizades e moderação são destinadas à instalação normal em banco vazio. Bancos antigos criados por sincronização manual precisam de avaliação do esquema e backup antes de adotar essas migrações; este incremento não migrou bancos existentes. Reverter essas migrações remove suas tabelas e dados; recuperação de dados exige backup.

A migração `desafios/0002_participacao_unica` consolida participações repetidas por usuário/desafio antes de criar a restrição única. Mantém uma linha já concluída quando existe (menor ID dentre as concluídas); se todas estão pendentes, mantém a de menor ID. Eventos de pontos não são alterados, removidos nem gerados. Não repara divergências anteriores entre conclusão e pontuação. Reverter remove a restrição, mas não recria as linhas redundantes: recuperação desses IDs exige backup. Aplicar em banco existente exige backup e janela sem inscrições/conclusões; neste trabalho só foram utilizados bancos descartáveis.

## Próximo passo

Implementar o Incremento 0: fundação técnica, estrutura de diretórios, ambiente, regras de segurança, modelo de visibilidade e documentação mínima de integração.

## Limitações conhecidas

- O projeto ainda depende de decisões humanas pendentes sobre menor de idade, cadastro, visibilidade padrão, ranking global, regras de pontuação e retenção de dados.
- Qualquer entrega funcional deve respeitar os bloqueios documentados em [Trama.md](./Trama.md).
