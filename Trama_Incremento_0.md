# Trama — Incremento 0

## Objetivo

Estabelecer a fundação técnica, de documentação e requisitos mínimos para o desenvolvimento seguro do MVP do Trama, sem implementar funcionalidades de usuário que dependam de decisões pendentes do produto.

## Requisitos vinculados

- RF01 (Conta) – base técnica para cadastro e autenticação
- RF02 (Perfil) – base de usuário e interesses
- RNF-01 a RNF-08
- RNF-12, RNF-13, RNF-19, RNF-20
- CA-25, CA-26, CA-27, CA-28

## Escopo

- Definir estrutura do repositório e convenções básicas.
- Registrar documentação mínima de produto, progresso e arquitetura.
- Preparar ambiente de desenvolvimento com Django + PostgreSQL + HTMX como direção recomendada.
- Definir modelo de usuário próprio e regras básicas de segurança.
- Implementar ponto de entrada para visibilidade centralizada.
- Prever migrações e auditoria sem conteúdo sensível.
- Criar documentação de decisões pendentes e de riscos.

## Critérios de aceite do incremento

1. O repositório contém base documental necessária para continuar o desenvolvimento com rastreabilidade.
2. Existe uma visão clara da arquitetura do MVP e dos limites do Incremento 0.
3. O projeto identifica decisões pendentes que bloqueiam entregas futuras.
4. O desenho do modelo de visibilidade e do usuário próprio está explicitado antes da implementação funcional.
5. O ambiente e a configuração de segurança básica estão documentados.

## Bloqueios conhecidos

- D01: idade mínima e menores
- D02: campos de cadastro e contato de acesso
- D12: retenção e exclusão
- D14: stack, custos e responsável da revisão técnica
- D15: avaliação jurídica

## Saída esperada

- Estrutura inicial do projeto organizada.
- Documentação de progresso e roadmap atualizada.
- Arquitetura de módulos pronta para gerar a base de implementação do Incremento 1.
- Scripts e ambiente iniciais documentados.

## Validação recomendada

- Verificar que todos os documentos mínimos existem.
- Confirmar que o desenho de visibilidade foi centralizado em um único ponto.
- Revisar o checklist de segurança mínimo antes de implementar autenticação real.
- Validar que decisões pendentes não foram tratadas como aprovadas.
