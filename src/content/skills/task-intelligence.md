---
title: "Task Intelligence"
description: "Protocolo de Inteligência Pré-Tarefa — ativa TODOS os agentes relevantes do ecossistema ANTES de executar qualquer tarefa solicitada pelo usuário. Enriquece o contexto com análise paralela..."
category: "development"
source: "community"
author: "Community"
tags: ["task", "intelligence"]
date: 2026-03-20
---

# Task Intelligence — Protocolo de Amplificação Pré-Tarefa

## Overview

Protocolo de Inteligência Pré-Tarefa — ativa TODOS os agentes relevantes do ecossistema ANTES de executar qualquer tarefa solicitada pelo usuário. Enriquece o contexto com análise paralela multi-agente, produz estimativa real de tempo (início→fim), mapeia problemas prováveis e improvável, e formula um plano de execução antecipado com estratégias de contingência.

## When to Use This Skill

- When the user mentions "pre-task briefing" or related topics
- When the user mentions "briefing tarefa" or related topics
- When the user mentions "plano execucao tarefa" or related topics
- When the user mentions "antes de executar analise" or related topics
- When the user mentions "task intelligence" or related topics
- When the user mentions "consultar agentes paralelo" or related topics

## Do Not Use This Skill When

- The task is unrelated to task intelligence
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Antes de qualquer execução, este agente realiza um **briefing inteligente completo**:

1. **Ativa todos os agentes relevantes em paralelo** — cada um analisa a tarefa pela sua ótica
2. **Sintetiza o conhecimento coletivo** em um plano unificado
3. **Estima tempo real** do início ao fim (com breakdown por etapa)
4. **Mapeia problemas prováveis** e os resolve antecipadamente
5. **Define pontos de verificação** para detectar desvios antes que virem bloqueadores

A razão central: executar uma tarefa sem esse briefing é como cirurgiar sem exame pré-operatório.
O custo de 30-60 segundos de análise paralela elimina horas de retrabalho.

---

## Fase 1 — Classificação Da Tarefa (5-10 Segundos)

Antes de qualquer coisa, classifique a tarefa em uma das categorias:

| Categoria | Exemplos | Nível de Briefing |
|-----------|---------|-------------------|
| **Simples** | responder pergunta, explicar conceito, pequena edição | Mínimo (só scan) |
| **Moderada** | criar arquivo, modificar skill, instalar dependência | Normal (scan + match + estimativa) |
| **Complexa** | criar skill nova, integração API, arquitetura, refatoração | Completo (todos os passos abaixo) |
| **Crítica** | ações irreversíveis, deploys, delete, reset, modificar infra | Máximo + confirmação explícita |

Para tarefas **Simples**, execute normalmente sem briefing completo.
Para **Moderada**, **Complexa** e **Crítica**, execute o protocolo completo abaixo.

---

## Fase 2 — Scan E Match Paralelo

Execute simultaneamente:

```bash

## Terminal 1 — Atualizar Registry

python agent-orchestrator/scripts/scan_registry.py

## Terminal 2 — Identificar Agentes Relevantes

python agent-orchestrator/scripts/match_skills.py "<tarefa do usuário>"
```

Se `matched >= 2`, execute orquestração:
```bash
python agent-orchestrator/scripts/orchestrate.py --skills <skill1,skill2,...> --query "<tarefa>"
```

---

## Fase 3 — Briefing Dos Agentes Especializados

Para cada agente relevante identificado no match, faça uma pergunta direcionada:

**Padrão de consulta por tipo de agente:**

- **007 (Segurança)**: "Esta tarefa tem vetores de ataque, dados expostos, ou ações irreversíveis?"
- **skill-sentinel (Qualidade)**: "Existe skill redundante? A skill que será criada/modificada segue os padrões?"
- **agent-orchestrator (Orquestração)**: "Quais skills já existem que resolvem parte desta tarefa?"
- **matematico-tao (Complexidade)**: "Qual a complexidade computacional? Há otimizações não-óbvias?"
- **context-guardian (Continuidade)**: "Existe contexto de sessões anteriores relevante para esta tarefa?"
- **advogado-especialista/criminal (Legal)**: "Há implicações legais, LGPD, ou riscos regulatórios?"
- **leiloeiro-ia (Leilões)**: "Esta tarefa envolve dados ou lógica do domínio de leilões?"

Não consulte todos os agentes cegamente — escolha os **3-5 mais relevantes** para a tarefa.

---

## Fase 4 — Estimativa De Tempo Real

Construa um breakdown de tempo honesto com base na complexidade real:

```
ESTIMATIVA DE TEMPO — [Nome da Tarefa]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Etapa 1: [nome]          ~X min   [motivo do tempo]
Etapa 2: [nome]          ~X min   [motivo do tempo]
Etapa 3: [nome]          ~X min   [motivo do tempo]
Contingência (problemas) +X min   [buffer para imprevistos típicos]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL ESTIMADO:          ~X min
Confiança: Alta/Média/Baixa — [justificativa]
```

**Regras de estimativa honesta:**
- Nunca subestime para agradar — o usuário precisa saber o tempo real
- Adicione sempre 20-30% de buffer para problemas típicos
- Se a confiança for Baixa, explique por quê e o que aumentaria ela
- Diferencie "tempo de execução do agente" vs "tempo de espera do usuário"

---

## Fase 5 — Mapa De Problemas (Antecipação Proativa)

Pense em TRÊS camadas de problemas:

#### Problemas Prováveis (80%+ de chance de acontecer)
São os problemas que SEMPRE acontecem. Resolva-os ANTES de começar.

Exemplos por categoria:
- **Skills novas**: YAML inválido → valide com `python -c "import yaml; yaml.safe_load(open('SKILL.md').read())"` antes de instalar
- **APIs externas**: chave expirada, rate limit, mudança de endpoint → verifique autenticação primeiro
- **Instalações**: dependências faltando, versão incompatível → leia requirements.txt antes de executar
- **Arquivos**: path não existe, permissão negada, encoding errado → verifique antes de abrir
- **Git/Versionamento**: branch errada, conflito de merge, uncommitted changes → sempre `git status` antes

#### Problemas Possíveis (30-70% de chance)
Problemas que podem acontecer dependendo do estado atual.

Estratégia: verifique rapidamente o estado antes de assumir que está OK.

#### Problemas Improváveis mas Críticos (< 10% mas alto impacto)
Ações irreversíveis, perda de dados, exposição de credenciais.

Estratégia: backup preventivo, confirmação explícita, rollback plan.

**Template de mapa de problemas:**

```
MAPA DE PROBLEMAS — [Nome da Tarefa]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROVÁVEIS (resolver antes de começar):
  ⚠ [problema] → [solução preventiva aplicada agora]
  ⚠ [problema] → [solução preventiva aplicada agora]

POSSÍVEIS (monitorar durante execução):
  ~ [problema] → [sinal de alerta] → [ação se ocorrer]

CRÍTICOS (baixa prob, alto impacto):
  🔴 [risco] → [backup/rollback plan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Fase 6 — Plano De Execução Enriquecido

Depois de coletar análises dos agentes + estimativas + mapa de problemas, produza:

```
BRIEFING PRÉ-EXECUÇÃO — [Nome da Tarefa]
════════════════════════════════════════════
CONTEXTO COLETADO:
  • [insight do agente 1]
  • [insight do agente 2]
  • [insight do agente 3]

PLANO DE EXECUÇÃO:
  1. [etapa] (~Xmin) — [por quê esta ordem]
  2. [etapa] (~Xmin) — [dependência da anterior]
  3. [etapa] (~Xmin) — [verificação de qualidade]

TEMPO TOTAL: ~Xmin | CONFIANÇA: Alta/Média/Baixa

PROBLEMAS PRÉ-RESOLVIDOS:
  ✅ [problema] → [solução aplicada]
  ✅ [problema] → [solução aplicada]

PONTOS DE VERIFICAÇÃO:
  [ ] Após etapa 1: verificar [critério de sucesso]
  [ ] Após etapa 2: verificar [critério de sucesso]
  [ ] Final: validar resultado completo

ROLLBACK PLAN (se algo der errado):
  → [como desfazer cada etapa crítica]
════════════════════════════════════════════
```

---

## Integração Com O Ecossistema

Este agente **complementa** o agent-orchestrator — não substitui:

- **agent-orchestrator**: identifica QUAIS skills usar (routing)
- **task-intelligence**: enriquece COMO usar + quando + com que riscos (briefing)

Ambos devem ser ativados juntos. O CLAUDE.md já exige o orchestrator — este agente adiciona a camada de inteligência sobre ele.

---

## Quando Não Usar O Briefing Completo

- Perguntas rápidas de 1 linha (responder diretamente é mais eficiente)
- Tarefas de leitura pura (read, grep, glob sem efeitos colaterais)
- Iterações simples dentro de uma tarefa já planejada
- Quando o usuário pede "só responde rápido" / "vibe comigo"

O objetivo não é burocracia — é inteligência a serviço da velocidade real.

---

## Referências

- `references/problem-catalog.md` — Catálogo de problemas típicos por domínio
- `references/time-patterns.md` — Padrões históricos de tempo por tipo de tarefa
- `scripts/pre_task_check.py` — Script de verificação automatizada pré-tarefa

---

## Exemplo De Briefing Completo

**Tarefa do usuário:** "Crie uma skill para integração com Stripe"

```
BRIEFING PRÉ-EXECUÇÃO — Skill: stripe-integration
════════════════════════════════════════════════════

CONTEXTO COLETADO (3 agentes consultados):
  • 007: CRÍTICO — API keys do Stripe NÃO devem ir para SKILL.md ou git.
    Usar variáveis de ambiente (.env). Webhooks precisam validação HMAC-SHA256.
  • skill-sentinel: whatsapp-cloud-api já implementa padrão HMAC-SHA256 para webhooks
    — reusar esse padrão. Skill deve seguir estrutura: config.py + client.py + SKILL.md.
  • agent-orchestrator: 3 skills similares (whatsapp, telegram, instagram) como referência
    de arquitetura. Nenhuma conflita com Stripe.

PLANO DE EXECUÇÃO:
  1. Criar estrutura de diretórios (~2min) — base para os demais arquivos
  2. Escrever SKILL.md com workflow (~5min) — define comportamento do agente
  3. Criar config.py com variáveis de ambiente (~3min) — sem hardcode de keys
  4. Criar stripe_client.py com autenticação (~10min) — métodos principais
  5. Criar webhook_handler.py com HMAC-SHA256 (~5min) — reusar padrão whatsapp
  6. Instalar via skill-installer (~2min) — validação + registro
  7. Gerar ZIP (~1min) — para backup/upload manual

TEMPO TOTAL: ~28min | CONFIANÇA: Alta
(estrutura clara, dependências conhecidas, sem APIs externas incertas)

PROBLEMAS PRÉ-RESOLVIDOS:
  ✅ API key exposta → .env obrigatório, .gitignore configurado
  ✅ YAML inválido → validar antes de instalar
  ✅ Webhook sem autenticação → HMAC-SHA256 incluído no plano

PONTOS DE VERIFICAÇÃO:
  [ ] Após SKILL.md: yaml.safe_load não levanta exceção
  [ ] Após config.py: sem strings hardcoded de credenciais
  [ ] Final: skill-installer valida os 10 checks

ROLLBACK PLAN:
  → Se skill-installer falhar: pasta em /tmp/stripe-skill-backup/
  → Se ZIP corrompido: reconstruir com build_ecosystem.py
════════════════════════════════════════════════════
```

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `agent-orchestrator` - Complementary skill for enhanced analysis
- `multi-advisor` - Complementary skill for enhanced analysis

---

## Reference: Problem Catalog

# Catálogo de Problemas por Domínio

## Skills e Orchestrator

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| YAML inválido no SKILL.md | Alta | `python -c "import yaml; yaml.safe_load(open('SKILL.md').read())"` |
| `name` ou `description` duplicados no YAML | Média | Grep por `^name:` no arquivo — deve ter 1 ocorrência |
| skill-installer falha silenciosamente | Média | Usar `--force` e ler output completo |
| scan_registry.py bug com sets/dicts | Baixa | Atualizar registry manualmente via JSON |
| Skill no .claude mas não em skills/ | Média | Sempre instalar via skill-installer, não copiar manual |

## APIs e Integrações

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| Token/API key expirado | Alta | Verificar validade antes de executar |
| Rate limit atingido | Média | Implementar retry com backoff exponencial |
| Endpoint mudou (breaking change) | Baixa | Fixar versão da API, checar changelog antes |
| HMAC-SHA256 inválido em webhooks | Média | Testar com payload de exemplo antes de ir live |
| Credencial hardcoded commitada | Baixa mas crítica | `.env` obrigatório + `.gitignore` configurado |

## Arquivos e Paths

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| Path não existe | Alta | `os.path.exists()` antes de qualquer operação |
| Permissão negada | Média | Verificar com `os.access(path, os.W_OK)` |
| Encoding errado (pt-BR com acentos) | Alta | `open(f, encoding='utf-8')` explícito sempre |
| ZIP corrompido | Baixa | Verificar com `zipfile.is_zipfile()` após geração |
| Arquivo aberto por outro processo | Baixa | Fechar handles explicitamente com `with` |

## ZIPs e Builds do Ecossistema

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| ecosystem-completo.zip desatualizado | Alta | Executar build_ecosystem.py após cada nova skill |
| Skill numerada fora de ordem | Média | Verificar contagem total antes de atribuir número |
| ZIP muito grande (>50MB) | Baixa | Excluir __pycache__, .pyc, node_modules |

## Git

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| Commit na branch errada | Alta | `git branch --show-current` antes de commits |
| Uncommitted changes perdidos | Média | `git status` antes de operações destrutivas |
| Merge conflict | Média | `git pull --rebase` antes de push |
| Push de secrets | Baixa mas crítica | `git diff --staged` antes de commit |

## Python / Scripts

| Problema | Frequência | Solução Preventiva |
|----------|-----------|-------------------|
| ModuleNotFoundError | Alta | `pip install -r requirements.txt` primeiro |
| Python 2 vs 3 | Baixa | Usar `python3` explicitamente |
| Subprocess sem timeout | Média | Sempre `subprocess.run(..., timeout=30)` |
| JSON decode error | Média | Tratar `json.JSONDecodeError` explicitamente |
| UnicodeDecodeError | Alta | `encoding='utf-8', errors='replace'` em files |

---

## Reference: Time Patterns

# Padrões Históricos de Tempo por Tipo de Tarefa

Baseado em execuções reais do ecossistema.

## Criação de Skills

| Tarefa | Tempo Real | Observações |
|--------|-----------|-------------|
| Skill simples (só SKILL.md, sem scripts) | 5-10 min | ~200-400 linhas |
| Skill moderada (SKILL.md + 1-2 scripts) | 15-25 min | Ex: telegram, whatsapp |
| Skill complexa (múltiplos scripts + refs) | 30-60 min | Ex: instagram (29 arquivos) |
| Evolução de skill (v1→v2) | 20-40 min | Reescrever seções inteiras |
| Ecossistema de skills relacionadas (5-6) | 2-4h | Ex: leiloeiro-ia + 5 módulos |

## Instalação e Infraestrutura

| Tarefa | Tempo Real | Observações |
|--------|-----------|-------------|
| skill-installer (1 skill) | 1-3 min | Inclui 10 validações |
| Gerar ZIP de 1 skill | 30s | Sem compressão máxima |
| Gerar ecosystem-completo.zip (31 skills) | 1-2 min | 342 arquivos, ~1 MB |
| Auditoria do ecossistema completo | 10-20 min | scan + validate + fix |
| Atualizar registry manualmente | 2-5 min | Quando scan_registry tem bugs |

## APIs e Integrações

| Tarefa | Tempo Real | Observações |
|--------|-----------|-------------|
| Setup inicial de API (auth + teste) | 10-20 min | Com API key válida |
| Implementar webhook com HMAC | 15-25 min | Incluindo testes |
| OAuth flow completo | 30-60 min | Depende da plataforma |
| Debug de API (token expirado, 403) | 5-30 min | Alta variância |

## Agentes de IA (Personas)

| Tarefa | Tempo Real | Observações |
|--------|-----------|-------------|
| Criar persona v1 (500-700 linhas) | 15-25 min | Com subagente |
| Evoluir persona para v2 (1200+ linhas) | 20-35 min | Expansão de 80-180% |
| Criar 6 personas em paralelo (v1) | 25-45 min total | Subagentes paralelos |
| Evoluir 5 personas em paralelo (v2) | 30-60 min total | Alta qualidade |

## Análise e Pesquisa

| Tarefa | Tempo Real | Observações |
|--------|-----------|-------------|
| Análise de código (1 arquivo) | 2-5 min | |
| Auditoria de segurança completa | 15-30 min | Com 007 |
| Pesquisa web (5-10 fontes) | 5-10 min | Com subagente Explore |
| Debug de bug complexo | 15-45 min | Alta variância |

## Multiplicadores de Tempo

| Fator | Multiplicador |
|-------|--------------|
| API de terceiro instável | ×1.5 a ×2.0 |
| Dependências não documentadas | ×1.3 a ×1.8 |
| Ambiente Windows vs Linux path issues | ×1.2 |
| Subagentes em paralelo (4+) | ÷2 a ÷3 |
| Primeira vez no domínio | ×1.5 a ×2.5 |
| Task já feita antes (memória ativa) | ×0.5 a ×0.7 |
