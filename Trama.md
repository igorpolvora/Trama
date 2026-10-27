# Trama — Documento do MVP

Versão: 0.2 — 26/10/2026  
Status: definição de produto em refinamento; não é uma especificação pronta para lançamento.

## 0. Como ler esta versão

Marcações usadas ao longo do documento:

- **[C]** decisão confirmada pelo responsável do projeto (seção 3).
- **[P]** proposta de escopo ou requisito, sujeita a aprovação.
- **[?]** decisão pendente. A IA implementadora não deve inventar a resposta (seção 14).
- **[R]** acréscimo ou ajuste desta revisão (v0.2). É proposta editorial, também sujeita a aprovação. Nada marcado [R] é decisão confirmada.

Principais mudanças em relação à v0.1:

1. Glossário (seção 6.1) e dois conflitos de definição sinalizados: diário × conteúdo e "ranking global".
2. Requisitos de segurança numerados (RNF-xx), para permitir rastreio entre requisito e teste.
3. Novas regras de privacidade: comentários, acesso de moderação a conteúdo denunciado, links e prévias, e pontos que revelam atividade privada.
4. Critérios de aceitação ampliados, no formato Dado/Quando/Então, cobrindo todos os requisitos funcionais.
5. Decisões pendentes numeradas (D01 a D20), cada uma com o incremento que ela bloqueia.
6. Incrementos com pontos de validação por hipótese, critérios de entrada para um piloto fechado e proposta de piloto com público adulto.
7. Menores de idade e legislação aplicável tratados como bloqueio do primeiro incremento.
8. Recomendação de stack (Django + PostgreSQL + HTMX) e estrutura inicial do projeto na seção 15.1.

## 1. Visão do produto

Trama é uma rede social para estudantes de diversas áreas registrarem sua aprendizagem, compartilharem conhecimentos e projetos e construírem sua trajetória acadêmica e profissional. A experiência reúne diário de estudos, comunidade e desafios com gamificação inspirada em mecanismos de constância e competição de produtos como Duolingo e Strava.

O desenvolvimento será realizado com apoio de IA. Requisitos, critérios de aceitação e revisão humana devem orientar a implementação.

Frase de marca proposta, ainda não aprovada: "Conecte ideias. Construa sua trajetória."

## 2. Objetivo do MVP

Validar se estudantes encontram valor em acompanhar sua evolução e aprender em comunidade, com controle sobre a exposição de seus conteúdos e competição opcional.

Hipóteses a validar e o ponto do desenvolvimento em que cada uma passa a ser testável **[R]**:

| Hipótese | Testável a partir de |
| --- | --- |
| H1. Registrar atividades ajuda o estudante a perceber sua evolução. | Fim do incremento 2 |
| H2. Compartilhar conhecimentos, dúvidas e projetos gera trocas úteis. | Fim do incremento 3 |
| H3. Metas, desafios e ligas incentivam o retorno à plataforma. | Fim do incremento 5 (metas, já no incremento 2) |
| H4. Controles de visibilidade permitem atender tanto ao uso pessoal quanto ao social. | Fim do incremento 3 |

Consequência: H1 e parte de H4 podem ser avaliadas sem desafios nem rankings. Isso permite decidir com evidência se vale continuar para os incrementos 4 e 5.

## 3. Decisões confirmadas [C]

- Nome do projeto: Trama.
- Público pretendido: estudantes em geral, de diversas áreas.
- A experiência deve contemplar registro de estudos, consumo e compartilhamento de conteúdo e desafios de aprendizagem.
- Haverá gamificação com ligas, ranking global e ranking entre amigos. *(Nota [R]: o significado exato de "ranking global" está em aberto; ver D08.)*
- Cada conteúdo poderá ser privado, público ou visível apenas para amigos, conforme escolha do usuário.
- Compartilhar com outras pessoas não será obrigatório para utilizar a plataforma.
- Segurança de dados pessoais, do sistema e das interações deve fazer parte do projeto desde o início.

As demais escolhas deste documento são propostas de escopo ou requisitos recomendados, sujeitos a refinamento. Idade mínima e participação de menores ainda não foram definidas.

## 4. Público e papéis

### Estudante

Pode cadastrar uma conta, organizar estudos, criar conteúdos, escolher sua visibilidade, estabelecer amizades e participar da gamificação.

### Moderador

Pode analisar denúncias e aplicar medidas previstas nas regras da comunidade. Não recebe acesso irrestrito aos diários privados; qualquer acesso excepcional deve ter finalidade, autorização e auditoria definidas.

### Administrador

Pode administrar configurações, desafios e regras operacionais. Suas permissões devem ser limitadas por função, com ações relevantes registradas.

### Visitante sem conta **[?]**

Se existirá e o que poderá ver depende de D05.

### Quadro de permissões **[R]**

| Ação | Estudante | Moderador | Administrador |
| --- | --- | --- | --- |
| Ler o próprio diário privado | Sim | Não | Não |
| Ler conteúdo denunciado que não seja público | Não (salvo audiência) | Somente o denunciado, com registro | [?] D10 |
| Aplicar medida a conteúdo ou conta | Não | Sim, conforme regras | [?] D11 |
| Ajustar pontuação | Não | [?] D10 | [?] D10 |
| Criar e editar desafios | Não | Não | Sim |
| Alterar configurações e regras | Não | Não | Sim, com autenticação reforçada |

## 5. Jornada principal

1. Criar uma conta e escolher áreas de interesse.
2. Definir um objetivo ou meta de estudo.
3. Estudar e registrar uma atividade.
4. Escolher se o registro será privado, para amigos ou público.
5. Explorar conteúdos acessíveis e trocar comentários.
6. Participar de desafios e, se desejar, dos rankings.
7. Consultar histórico e progresso pessoal.

Exemplo: uma pessoa estuda HTML, registra uma reflexão, adiciona o link de uma página criada e escolhe compartilhar com amigos. Esse projeto pode ser associado a um desafio, caso cumpra seus critérios. O mesmo fluxo deve comportar outras áreas de conhecimento.

## 6. Escopo funcional proposto [P]

| ID | Módulo | Funcionalidades do MVP |
| --- | --- | --- |
| RF01 | Conta | Cadastro, verificação do contato de acesso, login, saída e recuperação de conta. O tipo de contato (e-mail, telefone) é D02. |
| RF02 | Perfil | Apelido, apresentação opcional, interesses e projetos compartilhados. Nome completo, instituição, empresa e localização não são obrigatórios. |
| RF03 | Diário | Criar, consultar, editar e excluir registros de estudo com título, assunto, data e reflexão. Tempo estudado pode ser opcional. |
| RF04 | Objetivos | Criar metas pessoais e acompanhar seu progresso. |
| RF05 | Conteúdo | Criar conhecimentos, dúvidas e projetos usando texto e links. |
| RF06 | Visibilidade | Escolher e alterar a audiência de cada conteúdo ou registro: privado, amigos ou público. |
| RF07 | Comunidade | Visualizar um feed simples e filtrar conteúdos acessíveis por interesse. Ordem do feed proposta [R]: cronológica reversa, sem recomendação algorítmica. |
| RF08 | Amizades | Enviar, aceitar, recusar e desfazer solicitações de amizade. |
| RF09 | Interações | Comentar conteúdos quando houver permissão de acesso; editar ou excluir os próprios comentários. |
| RF10 | Desafios | Consultar desafios criados pela plataforma, participar e registrar conclusão conforme critérios definidos. |
| RF11 | Progresso | Consultar histórico pessoal e conquistas separadamente dos pontos competitivos. |
| RF12 | Competição | Optar por participar de ligas e visualizar ranking global (ver D08) e ranking entre amigos. |
| RF13 | Proteção | Bloquear usuários e denunciar conteúdos ou contas. |
| RF14 | Moderação | Receber denúncias, registrar análise, aplicar medidas e permitir contestação. |
| RF15 | Dados da conta | Solicitar exportação dos próprios dados e exclusão da conta, com regras claras de processamento. |
| RF16 **[R]** | Constância e lembretes | **[?] D13.** Sequência de dias de estudo e lembretes opcionais. A visão do produto cita "mecanismos de constância" e H3 depende de retorno à plataforma, mas a v0.1 não tinha requisito para isso. Só entra no escopo se aprovado. |

Proposta para reduzir complexidade: começar com texto e links; uploads de arquivos dependem de definição dos formatos, limites, armazenamento e inspeção de segurança.

### 6.1 Glossário **[R]**

| Termo | Definição usada neste documento |
| --- | --- |
| Registro de estudo | Entrada do diário (RF03), com título, assunto, data e reflexão. |
| Conteúdo | Publicação do tipo conhecimento, dúvida ou projeto (RF05). |
| Audiência | Quem pode acessar um registro ou conteúdo: privado, amigos ou público. |
| Desafio | Atividade proposta pela plataforma com critérios de conclusão (RF10). |
| Liga | **[?]** Agrupamento de competição. A definição está em D08. |
| Temporada | Período semanal de competição, ao fim do qual a pontuação competitiva reinicia. |
| Conquista | **[?]** Marco de progresso pessoal (RF11). O que conta como conquista está em D09. |

**Conflito a resolver (D03):** o passo 4 da jornada aplica visibilidade a um "registro", enquanto o RF06 a um "conteúdo". Não está definido se Registro de estudo e Conteúdo são a mesma entidade (com tipos) ou duas entidades. Enquanto D03 estiver aberto, implementar apenas o diário (RF03) com visibilidade.

## 7. Privacidade e visibilidade

| Opção | Audiência |
| --- | --- |
| Privado | Apenas o autor na experiência comum do produto. Não deve aparecer em feeds, buscas ou perfis de terceiros. |
| Amigos | Autor e usuários com amizade aceita, respeitando bloqueios e demais restrições. |
| Público | Comunidade da plataforma. Acesso por visitantes sem conta e indexação em buscadores estão pendentes (D05). |

Regras propostas [P]:

- Privado será o padrão inicial, ainda sujeito à aprovação (D04).
- O usuário deve visualizar a audiência antes de salvar ou compartilhar.
- A alteração de audiência deve valer para acessos futuros ao conteúdo e aos seus recursos associados.
- Comentários, anexos futuros e prévias não podem ampliar a audiência do conteúdo original.
- Desfazer amizade deve remover o acesso concedido exclusivamente por essa amizade.
- Restrições devem ser aplicadas no servidor, inclusive no acesso por link direto.
- Tornar um conteúdo privado não recolhe cópias que outras pessoas já tenham feito. A interface deve comunicar esse limite ao ampliar a audiência.
- Dados de autenticação e recuperação de conta nunca serão exibidos no perfil ou ranking.

Regras adicionadas nesta revisão [R], todas sujeitas a aprovação:

- **Acesso negado sem revelar existência.** Ao tentar abrir um conteúdo ao qual não tem acesso, o usuário recebe a mesma resposta que receberia para um conteúdo inexistente.
- **Comentários e perda de acesso.** Quem perde acesso a um conteúdo (visibilidade reduzida, amizade desfeita ou bloqueio) deixa de ver o conteúdo e a conversa em torno dele. O destino dos comentários que essa pessoa já deixou é D06.
- **Moderação de conteúdo restrito.** Um moderador só abre conteúdo não público quando houver denúncia sobre ele, e apenas o conteúdo denunciado, com finalidade e momento registrados. Diários privados não são alcançáveis por denúncia de terceiros. Casos excepcionais seguem D10.
- **Pontos e atividade privada.** Registros privados podem gerar pontos sem expor conteúdo, mas a pontuação em si revela volume e frequência de atividade. Isso deve ser uma escolha consciente e comunicada ao usuário que optar por competir.
- **Links.** Ver RNF-16 e RNF-17.

## 8. Gamificação e rankings

### Estrutura proposta [P]

- Áreas de interesse organizam conteúdos; ligas organizam a competição. Uma pessoa pode ter vários interesses.
- Temporadas semanais, com pontuação competitiva reiniciada ao final de cada temporada.
- Histórico de estudos, projetos e conquistas permanece disponível após o encerramento da temporada.
- Grupos limitados dentro de cada liga organizam disputas locais.
- Ranking global da liga reúne todos os participantes daquela liga. **[R]** A decisão confirmada diz apenas "ranking global"; se ele é um só para toda a plataforma ou um por liga é D08.
- Ranking entre amigos compara participantes elegíveis pela mesma pontuação semanal, mesmo em ligas diferentes. **[R]** Proposta: só aparecem no ranking de amigos pessoas que optaram por competir. Quem não optou não tem pontuação exibida a amigos.
- Promoção, permanência e rebaixamento seguem regras visíveis antes de cada temporada.
- Participação nos rankings é opcional.

### Pontuação

Pontos representam participação segundo as regras da plataforma; não certificam domínio, qualidade acadêmica ou competência profissional.

- Registros privados podem contribuir sem revelar conteúdo, desde que cumpram as regras da atividade.
- Publicar não deve ser condição para todo tipo de progresso.
- Registrar horas, publicar ou comentar não deve gerar pontos ilimitados.
- Curtidas ou popularidade não devem determinar diretamente a classificação.
- Critérios de desafios devem ser claros e possíveis de aplicar a diferentes áreas.
- Pontos devem ser calculados no servidor e associados a eventos auditáveis.
- Repetir uma solicitação não pode conceder a mesma recompensa novamente.
- Edição, exclusão, desclassificação e fraude precisam de regras explícitas de ajuste da pontuação.
- Correções administrativas devem registrar motivo e permitir contestação.
- **[R]** Os eventos auditáveis de pontos não devem guardar o conteúdo do registro, apenas o necessário para auditar (tipo de evento, data, regra aplicada).

**Tensão a resolver (D10) [R]:** a moderação não acessa diários privados, mas a pontuação exige regras contra fraude e desclassificação. É preciso definir como detectar abuso em registros privados sem lê-los (por exemplo, regras baseadas em metadados e limites, ou evidência apresentada voluntariamente pelo usuário). Também é preciso definir como mitigar contas múltiplas usadas para inflar a competição (RNF-08).

Pendências (D08 e D09): nomes e quantidade de ligas, fórmula de pontos, limites, desempate, critérios de conclusão, tamanho dos grupos, promoção/rebaixamento, entrada no meio da temporada, fuso horário de encerramento e o que conta como conquista.

## 9. Segurança e desenvolvimento com IA

Os itens abaixo são requisitos de engenharia propostos [P], não uma declaração de conformidade legal. Foram numerados nesta versão [R] para que cada requisito possa ser ligado a um teste.

### Conta e autorização

- **RNF-01** Proteger senhas com algoritmo apropriado de hash; nunca armazená-las em texto puro.
- **RNF-02** Proteger sessões e recuperação de conta, com expiração e revogação de credenciais quando necessário.
- **RNF-03** Limitar tentativas abusivas (*rate limiting*, isto é, limitar quantas tentativas são aceitas por período) em login, recuperação, publicações e interações.
- **RNF-04** Exigir autenticação reforçada para contas administrativas.
- **RNF-05** Verificar no servidor a permissão para cada leitura e alteração de recurso.
- **RNF-06** Impedir que um usuário consulte ou altere dados de outro apenas trocando um identificador (falha conhecida como IDOR, *Insecure Direct Object Reference*). **[R]** Cada tipo de recurso deve ter teste automatizado em que o usuário A tenta acessar um recurso do usuário B.
- **RNF-07 [R]** Preferir componentes consolidados e mantidos para autenticação, sessões e controle de acesso, em vez de implementações próprias. A escolha da stack é D14.
- **RNF-08 [R]** Mitigar a criação de contas múltiplas para fraudar a competição. O nível de rigor depende de D10.

### Dados e aplicação

- **RNF-09** Coletar apenas dados necessários às funcionalidades definidas.
- **RNF-10** Usar transporte criptografado e proteção adequada para dados armazenados e backups.
- **RNF-11** Validar entradas e tratar conteúdo exibido para evitar execução de código e injeções.
- **RNF-12** Manter credenciais e segredos fora do código e dos registros de execução.
- **RNF-13** Evitar dados pessoais desnecessários em logs e ferramentas de monitoramento.
- **RNF-14** Definir retenção, exclusão, exportação e tratamento de cópias de segurança (D12).
- **RNF-15** Caso uploads sejam habilitados, aplicar limites, validação de arquivos e autorização também no download.
- **RNF-16 [R]** Links: aceitar somente `http` e `https`; rejeitar esquemas como `javascript:`; exibir o domínio ao usuário; abrir com `rel="noopener noreferrer nofollow ugc"`, de modo que o site de destino não ganhe controle sobre a página da Trama.
- **RNF-17 [R] [P]** Não gerar prévias de link no MVP. Se forem aprovadas, o servidor que busca a página externa fica sujeito a SSRF (*Server-Side Request Forgery*, quando o servidor é induzido a acessar endereços internos). Nesse caso: bloquear destinos internos, limitar redirecionamentos, tamanho e tempo, e a prévia herdar a visibilidade do conteúdo.
- **RNF-18 [R]** Medição de uso (analytics) sem coletar conteúdo privado e com base de consentimento definida (D19).

### Operação e revisão

- **RNF-19** Separar desenvolvimento, testes e produção.
- **RNF-20** Usar dados fictícios no desenvolvimento e nos testes com IA.
- **RNF-21** Revisar código gerado, dependências e configurações antes de disponibilizar alterações.
- **RNF-22** Testar acesso indevido, visibilidade, recuperação de conta e manipulação de pontos.
- **RNF-23** Manter backups e comprovar a possibilidade de restauração.
- **RNF-24** Monitorar falhas e estabelecer procedimento para incidentes e reversão de versões.
- **RNF-25** Não disponibilizar credenciais ou bases reais à IA sem uma avaliação específica de necessidade e proteção.
- **RNF-26 [R] [P]** Acessibilidade: usar WCAG 2.2 nível AA como referência nos fluxos principais.

## 10. Segurança da comunidade e menores

- Definir regras contra assédio, golpes, exposição de terceiros, plágio e manipulação da competição.
- Disponibilizar bloqueio e denúncia em pontos acessíveis da interface.
- Definir responsáveis, prioridades e procedimentos para análise de denúncias.
- Não apresentar pontuação como certificação ou garantia de credibilidade do conteúdo.
- Definir idade mínima e eventual participação de menores antes de implementar cadastro e regras de interação.
- Caso menores participem, projetar proteção específica de exposição, descoberta de perfis, contato e tratamento de dados, com avaliação jurídica aplicável antes do lançamento.

**[R] Bloqueio do incremento 1.** "Estudantes em geral" provavelmente inclui menores de 18 anos, e a Trama é uma rede social com perfis, comentários e competição. No Brasil, o Estatuto Digital da Criança e do Adolescente (Lei 15.211/2025, "ECA Digital") está em vigor desde 17/03/2026 e, segundo a imprensa e a literatura jurídica consultada, alcança serviços digitais com "acesso provável" por menores, não apenas os voltados a eles. Esta referência é um ponto de partida, não um parecer: o enquadramento da Trama deve ser avaliado por profissional jurídico (D15). Sem D01 (idade mínima e regras para menores) definida, o incremento 1 não deve começar.

**[R] [P] Alternativa para reduzir o risco no início:** piloto fechado com público adulto verificável (por exemplo, uma turma de curso superior), sem prejuízo da decisão final sobre D01.

## 11. Critérios de aceitação

Formato: Dado / Quando / Então. Critérios novos ou ampliados nesta versão estão marcados **[R]**. Critérios que dependem de decisão pendente indicam qual.

| ID | Requisito | Critério |
| --- | --- | --- |
| CA-01 | RF01, RF03 | **Dado** que não tenho conta, **quando** me cadastro, verifico o contato e registro um estudo, **então** consigo sair, entrar de novo e consultar o registro. |
| CA-02 **[R]** | RF01 | **Dado** uma conta existente, **quando** solicito recuperação, **então** é exigida prova de posse do contato, o token expira e só vale uma vez, e a resposta não revela se a conta existe. |
| CA-03 **[R]** | RF02 | **Dado** que não informo nome completo, instituição, empresa nem localização, **quando** concluo o cadastro e edito meu perfil, **então** o fluxo funciona (campos obrigatórios conforme D02). |
| CA-04 **[R]** | RF03 | **Dado** um registro meu, **quando** o edito ou excluo, **então** a alteração aparece no histórico e o excluído some de histórico, feed e buscas. O efeito nos pontos segue D09. |
| CA-05 **[R]** | RF04 | **Dado** uma meta pessoal, **quando** registro uma atividade vinculada, **então** o progresso da meta é atualizado. |
| CA-06 **[R]** | RF05 | **Dado** que crio conhecimento, dúvida ou projeto com texto e links, **quando** salvo, **então** o conteúdo é criado; um link com esquema inválido (por exemplo `javascript:`) é rejeitado (RNF-16). Depende de D03. |
| CA-07 | RF06 | **Dado** um registro privado, **quando** outro usuário tenta abri-lo por tela, endereço direto ou chamada à API, **então** o acesso é negado sem revelar que ele existe. |
| CA-08 | RF06, RF08 | **Dado** um conteúdo para amigos, **quando** alguém sem amizade aceita tenta acessar, **então** é negado; **quando** a amizade é desfeita, **então** o acesso é removido. |
| CA-09 | RF06 | **Dado** que altero a visibilidade, **quando** outro usuário acessa depois, **então** o novo acesso vale imediatamente, sem deixar prévias, cache, resultados de busca ou recursos associados expostos. Ao ampliar a audiência, a interface avisa que cópias já feitas não são recolhidas. |
| CA-10 **[R]** | RF06 | **Dado** que vou salvar ou compartilhar, **quando** escolho a audiência, **então** vejo a audiência atual antes de confirmar. |
| CA-11 **[R]** | RF07 | **Dado** o feed, **quando** o abro e filtro por interesse, **então** só vejo conteúdos aos quais tenho acesso, na ordem definida (proposta: cronológica reversa). |
| CA-12 **[R]** | RF08 | **Dado** outro usuário, **quando** envio, aceito, recuso ou desfaço uma solicitação, **então** o estado da amizade muda conforme a ação; um usuário bloqueado não consegue enviar solicitação. |
| CA-13 **[R]** | RF09 | **Dado** um conteúdo ao qual tenho acesso, **quando** comento, **então** o comentário aparece, posso editá-lo ou excluí-lo, e ele não amplia a audiência do conteúdo. |
| CA-14 **[R]** | RF09, RF08, RF13 | **Dado** que perdi acesso a um conteúdo (visibilidade reduzida, amizade desfeita ou bloqueio), **quando** tento abri-lo, **então** não vejo conteúdo nem comentários. O tratamento dos comentários que já deixei depende de D06. |
| CA-15 | RF10 | **Dado** uma atividade elegível, **quando** ela é concluída, **então** a recompensa prevista é concedida uma única vez; repetir a solicitação não a duplica e o cliente não define a quantidade de pontos. Depende de D09. |
| CA-16 | RF11 | **Dado** meu histórico e minhas conquistas, **quando** os consulto, **então** aparecem separados da pontuação competitiva e continuam disponíveis após o fim da temporada. |
| CA-17 | RF12 | **Dado** que não optei por competir, **quando** o ranking é calculado, **então** não apareço em nenhum ranking; **quando** opto, **então** apareço com meu apelido. No ranking entre amigos só aparecem pessoas que optaram. |
| CA-18 | RF12 | **Dado** um ranking, **quando** qualquer usuário o consulta, **então** não aparecem títulos, textos ou evidências de registros privados. |
| CA-19 | RF12 | **Dado** o encerramento de temporada, **quando** ele ocorre, **então** a pontuação competitiva é reiniciada, o histórico pessoal é preservado e as regras de promoção, permanência e rebaixamento são aplicadas. Depende de D08 e D09. |
| CA-20 | RF03, RF04 | **Dado** que não publico nada nem participo de rankings, **quando** uso diário e metas, **então** todas as funções de registro e progresso funcionam. |
| CA-21 | RF13 | **Dado** que bloqueei um usuário, **quando** ele tenta as interações previstas (amizade, comentário), **então** são impedidas. O efeito sobre perfis, conteúdos públicos e rankings depende de D06. |
| CA-22 | RF13, RF14 | **Dado** uma denúncia, **quando** ela é enviada, **então** é recebida, analisada e encerrada com registro da decisão e do responsável, e o denunciado pode contestar. |
| CA-23 **[R]** | RF14 | **Dado** um moderador, **quando** ele analisa uma denúncia, **então** acessa somente o conteúdo denunciado, com finalidade e momento registrados, e não consegue abrir diários privados. Acesso excepcional depende de D10. |
| CA-24 | RF15 | **Dado** uma solicitação de exportação ou exclusão, **quando** ela é feita, **então** exige reautenticação e, no caso da exportação, contém apenas dados do próprio usuário. Regras de exclusão seguem D12. |
| CA-25 **[R]** | RF01, RF15 | **Dado** uma ação sensível (recuperação, exportação, exclusão, troca de contato), **quando** é solicitada, **então** passa por verificação de autorização. |
| CA-26 **[R]** | Papéis | **Dado** uma conta de administrador, **quando** ela entra ou executa ação relevante, **então** usa autenticação reforçada e a ação fica registrada em auditoria. |
| CA-27 **[R]** | RNF-06 | **Dado** cada tipo de recurso, **quando** o usuário A usa o identificador de um recurso do usuário B, **então** o acesso é negado (teste automatizado). |
| CA-28 **[R]** | RNF-03 | **Dado** tentativas repetidas de login ou recuperação, **quando** o limite é excedido, **então** novas tentativas são bloqueadas temporariamente. |
| CA-29 | RNF-26 | **Dado** os fluxos principais (cadastro, registrar estudo, escolher visibilidade, consultar histórico, comentar, denunciar), **quando** usados em celular e computador, só com teclado e com leitor de tela, **então** podem ser concluídos e os controles são identificáveis. |
| CA-30 **[R]** | RNF-18 | **Dado** a medição de uso, **quando** os indicadores são calculados, **então** não dependem de ler o conteúdo de registros privados. |

## 12. Fora do MVP proposto [P]

- Chat privado e chamadas de áudio ou vídeo.
- Recrutamento, vagas e seleção de candidatos.
- Certificação de conhecimento ou validação oficial de diplomas.
- Cursos completos e aulas ao vivo.
- Pagamentos, assinaturas e marketplace.
- Recomendações complexas baseadas em IA.
- Criação livre de desafios por qualquer usuário.
- Aplicativos nativos separados para Android e iOS.
- **[R]** Prévias automáticas de link (RNF-17).

Essas exclusões são propostas para limitar a primeira entrega e podem ser revisadas pelo responsável pelo projeto.

## 13. Indicadores para validar o MVP

- Quantos novos usuários realizam o primeiro registro de estudo.
- Quantos retornam em semanas seguintes.
- Frequência de registros e de conclusão de metas e desafios.
- Proporção de uso privado, entre amigos e público, medida sem analisar conteúdo privado desnecessariamente.
- Participação e permanência voluntária na competição.
- Percepção de utilidade, pressão competitiva e qualidade das interações.
- Volume de denúncias, tempo de tratamento e incidência de fraude.

Metas numéricas e período de avaliação ainda serão definidos (D18). Quantidade de publicações, isoladamente, não comprova aprendizagem.

**[R] Instrumentação.** Para medir esses indicadores é preciso decidir antes quais eventos serão registrados, por quanto tempo e com qual base de consentimento (D19), respeitando RNF-13 e RNF-18. **[R] Cold start** (massa crítica): feed vazio, grupos pequenos e poucos amigos prejudicam H2 e H3. O piloto deve ter público suficiente para formar grupos, o que reforça a ideia de começar por um grupo existente, como uma turma (D17).

## 14. Decisões pendentes antes da implementação

A coluna "Bloqueia" indica o primeiro incremento que não deve começar sem a decisão. "Recomendação" é a sugestão da revisão **[R]**; não é decisão.

| ID | Decisão | Bloqueia | Recomendação da revisão |
| --- | --- | --- | --- |
| D01 | Idade mínima e regras para menores | Inc. 1 | Decidir antes de qualquer cadastro; considerar piloto só com adultos. |
| D02 | Campos obrigatórios de cadastro e perfil; tipo de contato de acesso (e-mail ou telefone) | Inc. 1 | Mínimo possível (RNF-09). |
| D03 | Registro de estudo e Conteúdo: mesma entidade ou duas | Inc. 2 | Decidir antes de modelar dados. |
| D04 | Aprovação da visibilidade privada como padrão | Inc. 2 | Manter privado como padrão. |
| D05 | Acesso público sem conta e indexação em buscadores | Inc. 3 | Começar sem acesso de visitantes e sem indexação. |
| D06 | Política de bloqueio e audiência de perfis, lista de amigos e rankings; efeito de perda de acesso e bloqueio sobre comentários já feitos | Inc. 3 | Definir junto com D05. |
| D07 | Tipos de anexos, se houver | Fora do MVP | Manter texto e links. |
| D08 | O que é uma liga; "ranking global" é único ou por liga | Inc. 5 | Definir antes de modelar pontuação. |
| D09 | Regras de pontuação, desafios, conquistas e temporadas (fórmula, limites, desempate, grupos, promoção, entrada no meio da temporada, fuso horário) | Inc. 4 | Começar com poucos desafios e regras simples. |
| D10 | Detecção de fraude e contas múltiplas em registros privados; acesso excepcional de moderação; quem ajusta pontos | Inc. 4 | Priorizar métodos que não leem conteúdo privado. |
| D11 | Processo de moderação e recursos administrativos; quem revisa contestações | Inc. 3 | Revisor diferente de quem aplicou a medida, sempre que possível. |
| D12 | Prazos de retenção, exportação e exclusão (inclui comentários, histórico de pontos, registros de moderação e backups) | Inc. 1 | Definir junto com D15. |
| D13 | Incluir sequência de estudo e lembretes (RF16)? Canal de lembrete | Inc. 4 | Decidir antes de apostar em H3. |
| D14 | Stack, infraestrutura, custos e responsável pela revisão técnica | Inc. 0 | Direção aceita: Django + PostgreSQL + HTMX (seção 15.1). Falta fechar custos e o responsável pela revisão experiente de autenticação, autorização e privacidade. |
| D15 | Avaliação jurídica das obrigações aplicáveis e documentação de privacidade (inclui menores) | Inc. 1 | Antes de abrir para usuários reais. |
| D16 | Disponibilidade do nome Trama como marca (INPI), domínio e identificadores sociais | Marca | Pesquisar antes de investir em identidade. |
| D17 | Piloto fechado: público, tamanho e duração | Piloto | Grupo existente, com massa crítica. |
| D18 | Metas numéricas e período de avaliação dos indicadores | Piloto | Definir antes de abrir o piloto. |
| D19 | Instrumentação e base de consentimento para medição de uso | Piloto | Eventos de metadados, sem conteúdo privado. |
| D20 | Nível de acessibilidade de referência | Inc. 2 | WCAG 2.2 AA (RNF-26). |

## 15. Orientação para a IA implementadora

Este documento orienta o refinamento e não autoriza inventar respostas para decisões pendentes. Antes de implementar um fluxo dependente dessas decisões, registrar a dúvida e obter sua definição. Itens marcados [R] e [P] não são decisões confirmadas.

Implementar em incrementos revisáveis. Segurança deve acompanhar cada incremento. **[R]** Ordem e pontos de validação propostos:

| Incremento | Conteúdo | Observações |
| --- | --- | --- |
| 0 | Decisões D01, D02, D12, D14, D15 e fundação técnica (ambientes, revisão, dados fictícios) | Sem funcionalidades para usuários. |
| 1 | Contas e autorização (RF01, RF02) | RNF-01 a RNF-08. |
| 2 | Diário, metas e visibilidade (RF03, RF04, RF06) | **Validação A:** H1 e parte de H4. |
| 3 | Comunidade e proteção (RF05, RF07, RF08, RF09, RF13, RF14 básico) | **Validação B:** H2 e H4. Bloqueio, denúncia e moderação básica entram junto com a comunidade, não depois. |
| 4 | Desafios e pontuação (RF10, RF11 e, se aprovado, RF16) | Depende de D09, D10 e D13. |
| 5 | Rankings e temporadas (RF12) | **Validação C:** H3. Depende de D08. |
| 6 | Operação e validação de lançamento | Backups restauráveis, monitoramento, incidentes, reversão. |

**[R] Critérios de entrada para qualquer usuário real, mesmo em piloto:** D01 e D15 resolvidas; RF13, RF14 básico e RF15 (exportação e exclusão) funcionando; backups com restauração comprovada; testes de CA-07, CA-08, CA-27 e CA-28 aprovados; D18 e D19 definidas.

Cada entrega deve informar requisitos atendidos, testes realizados, limitações conhecidas e instruções de execução. Nenhuma declaração de "seguro" ou "conforme à legislação" deve substituir evidências de revisão e validação.

### 15.1 Stack recomendada e estrutura inicial **[R] [P]**

Direção aceita para a D14. A D14 só é encerrada quando houver estimativa de custos e um responsável pela revisão técnica (autenticação, autorização e privacidade). Nada abaixo autoriza decidir D03, D08 ou D09.

**Stack:**

- Python com Django, PostgreSQL, páginas geradas no servidor e HTMX para interações parciais.
- `django-allauth` (cadastro, verificação de contato e recuperação) e `django-axes` ou equivalente (limite de tentativas), conforme RNF-03 e RNF-07.
- Hospedagem gerenciada com PostgreSQL gerenciado e backups automáticos; restauração testada (RNF-23).
- E-mail transacional de provedor externo; monitoramento de erros sem dados pessoais (RNF-13).
- Fechamento de temporada por comando agendado do Django. Sem Celery nem Redis no MVP.
- CI (testes automáticos a cada alteração) com testes de visibilidade e IDOR e verificação de dependências.
- Dois ambientes (teste e produção), com dados fictícios (RNF-19, RNF-20).

**Estrutura de apps** (cada app é um módulo do Django; os campos listados são o mínimo e podem mudar):

| App | Incremento | Modelos principais | Observações |
| --- | --- | --- | --- |
| `contas` | 1 | `Usuario` (modelo de usuário próprio), `Perfil` (apelido, apresentação), `Interesse` | Campos obrigatórios dependem de D02. |
| `acesso` | 2 | Sem modelos próprios. Contém a função central de visibilidade (abaixo). | Único lugar com a regra privado/amigos/público. |
| `diario` | 2 | `RegistroEstudo` (autor, título, assunto, data, reflexão, tempo opcional, visibilidade), `Meta` (dono, descrição, progresso) | Visibilidade padrão `privado` (D04). Se D03 unir diário e conteúdo, `Conteudo` passa a ser um tipo de registro. |
| `amizades` | 2 (modelos) e 3 (telas) | `Amizade` (de, para, status), `Bloqueio` (quem bloqueou, bloqueado) | Os modelos entram no incremento 2, sem telas, para a função de visibilidade e a matriz de testes ficarem completas; solicitações e bloqueio na interface (RF08, RF13) ficam no incremento 3. Restrição de unicidade por par de usuários. Efeito do bloqueio: D06. |
| `comunidade` | 3 | `Conteudo` (se D03 mantiver entidade separada), `Comentario` | Feed e filtro por interesse. Sem prévias de link (RNF-17). |
| `moderacao` | 3 | `Denuncia`, `DecisaoModeracao`, `RegistroAuditoria` (ator, ação, alvo, momento, finalidade; sem conteúdo) | Acesso a conteúdo restrito só por denúncia (CA-23). |
| `desafios` | 4 | `Desafio`, `ParticipacaoDesafio` | Critérios de conclusão: D09. |
| `pontuacao` | 4 e 5 | `EventoPontos`, `Temporada`, `AdesaoCompeticao` (opt-in); `Liga` e `GrupoLiga` só após D08 | Ver regra de pontos como eventos. |

**Regras de arquitetura (propostas):**

1. **Modelo de usuário próprio desde o primeiro dia** (`AUTH_USER_MODEL`). Trocar depois, com dados em produção, é trabalhoso.
2. **Visibilidade em um só lugar.** Nenhuma tela, API ou tarefa consulta `RegistroEstudo` ou `Conteudo` diretamente; sempre passam por `acesso.visiveis_para(...)`.
3. **Acesso negado devolve 404, não 403.** Assim, um conteúdo sem permissão é indistinguível de um inexistente (CA-07).
4. **Pontos como eventos.** `EventoPontos` é só de inserção, com restrição de unicidade em (usuário, chave de idempotência), o que garante "uma única vez" mesmo com solicitação repetida (CA-15). Ajustes são novos eventos com motivo e responsável, nunca edição do evento original. O cliente nunca envia a quantidade de pontos.
5. **Auditoria sem conteúdo.** Eventos de pontos e registros de auditoria guardam metadados, não o texto dos registros.
6. **Configuração e segredos por variáveis de ambiente**, com configurações separadas por ambiente (RNF-12, RNF-19).

**Esboço ilustrativo da função central** (a ser implementado, testado e revisado; não é código pronto):

```python
# acesso/visibilidade.py
from django.db.models import Q

PRIVADO, AMIGOS, PUBLICO = "privado", "amigos", "publico"

def visiveis_para(queryset, usuario):
    """Devolve apenas os itens que `usuario` pode ver."""
    if not usuario.is_authenticated:
        return queryset.none()          # visitantes: depende de D05

    amigos = ids_de_amigos_aceitos(usuario)       # amizade com status "aceita"
    bloqueados = ids_com_bloqueio_entre(usuario)  # qualquer direção

    return (
        queryset
        .exclude(autor_id__in=bloqueados)
        .filter(
            Q(autor=usuario)                                # o autor vê tudo seu
            | Q(visibilidade=PUBLICO)
            | Q(visibilidade=AMIGOS, autor_id__in=amigos)   # privado fica só com o autor
        )
    )

# Uso em uma tela (404 se não puder ver ou não existir):
# registro = get_object_or_404(visiveis_para(RegistroEstudo.objects.all(), request.user), pk=pk)
```

**Primeiros testes a escrever (antes das telas):** uma matriz que combina quem acessa (autor, amigo aceito, amizade desfeita, não amigo, bloqueado, anônimo) com cada audiência (privado, amigos, público) e confere o resultado esperado. Ela cobre CA-07, CA-08, CA-14 e CA-27 para cada novo tipo de recurso.

| Quem acessa | Privado | Amigos | Público |
| --- | --- | --- | --- |
| Autor | Vê | Vê | Vê |
| Amigo aceito | Não vê | Vê | Vê |
| Amizade desfeita | Não vê | Não vê | Vê |
| Não amigo | Não vê | Não vê | Vê |
| Bloqueado (em qualquer direção) | Não vê | Não vê | Não vê |
| Anônimo | Não vê | Não vê | Depende de D05 |

*O efeito do bloqueio sobre conteúdo público é uma escolha desta proposta; a política definitiva é D06.*