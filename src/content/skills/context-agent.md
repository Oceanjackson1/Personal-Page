---
title: "Context Agent"
description: "Agente de contexto para continuidade entre sessoes. Salva resumos, decisoes, tarefas pendentes e carrega briefing automatico na sessao seguinte."
category: "development"
source: "community"
author: "Community"
tags: ["context", "agent"]
date: 2026-03-20
---

# Context Agent

## Overview

Agente de contexto para continuidade entre sessoes. Salva resumos, decisoes, tarefas pendentes e carrega briefing automatico na sessao seguinte.

## When to Use This Skill

- When the user mentions "salvar contexto" or related topics
- When the user mentions "salva o contexto" or related topics
- When the user mentions "proxima sessao" or related topics
- When the user mentions "briefing sessao" or related topics
- When the user mentions "resumo sessao" or related topics
- When the user mentions "continuidade sessao" or related topics

## Do Not Use This Skill When

- The task is unrelated to context agent
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Continuidade perfeita entre sessões do Claude Code. Captura, comprime e
restaura contexto automaticamente — tópicos, decisões, tarefas, erros,
arquivos modificados e descobertas técnicas.

## Localização

```
C:\Users\renat\skills\context-agent\
├── SKILL.md
├── scripts/
│   ├── config.py               # Paths e constantes
│   ├── models.py               # Dataclasses
│   ├── session_parser.py       # Parser JSONL do Claude Code
│   ├── session_summary.py      # Gerador de resumos
│   ├── active_context.py       # Gerencia ACTIVE_CONTEXT.md
│   ├── project_registry.py     # Registro de projetos
│   ├── compressor.py           # Compressão e arquivamento
│   ├── search.py               # Busca FTS5
│   ├── context_loader.py       # Carrega contexto
│   └── context_manager.py      # CLI entry point
├── references/
│   ├── context-format.md       # Especificação de formatos
│   └── compression-rules.md    # Regras de compressão
└── data/
    ├── sessions/               # session-001.md, session-002.md, ...
    ├── archive/                # Sessões arquivadas
    ├── ACTIVE_CONTEXT.md       # Contexto consolidado (max 150 linhas)
    ├── PROJECT_REGISTRY.md     # Status de todos os projetos
    └── context.db              # SQLite FTS5 para busca
```

## Inicialização (Primeira Vez)

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py init
```

## Salvar Contexto Da Sessão Atual

Quando a sessão está terminando ou antes de uma tarefa longa, salvar o contexto:

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py save
```

O que faz:
1. Encontra o arquivo JSONL mais recente da sessão
2. Analisa todas as mensagens, tool calls e resultados
3. Gera resumo estruturado (session-NNN.md)
4. Atualiza ACTIVE_CONTEXT.md com novas informações
5. Sincroniza com MEMORY.md (carregado no system prompt)
6. Indexa para busca full-text

## Carregar Contexto (Briefing)

No início de uma nova sessão, carregar o contexto:

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py load
```

Gera briefing com: projetos ativos, tarefas pendentes (por prioridade),
bloqueadores, decisões recentes, convenções e resumo das últimas sessões.

## Status Rápido

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py status
```

Resumo em poucas linhas: projetos, pendências críticas, bloqueadores.

## Buscar No Histórico

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py search "rate limit"
```

Busca full-text (SQLite FTS5) em todas as sessões — tópicos, decisões,
erros, arquivos, etc.

## Manutenção

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py maintain
```

Arquiva sessões antigas, comprime arquivo, ressincroniza MEMORY.md,
reconstrói índice de busca.

## Fluxo De Trabalho

```
[Sessão termina]
  → save → session-NNN.md + ACTIVE_CONTEXT.md + MEMORY.md

[Nova sessão começa]
  → MEMORY.md já está no system prompt (automático)
  → load → briefing detalhado com tudo que precisa saber

[Contexto cresce demais]
  → maintain → arquiva sessões antigas, comprime, otimiza
```

## O Que É Capturado Em Cada Sessão

- **Tópicos**: assuntos discutidos
- **Decisões**: escolhas técnicas e de arquitetura
- **Tarefas concluídas**: o que foi feito
- **Tarefas pendentes**: o que falta (com prioridade)
- **Arquivos modificados**: quais arquivos foram editados/criados
- **Descobertas**: insights técnicos importantes
- **Erros resolvidos**: problemas e suas soluções
- **Questões em aberto**: perguntas sem resposta
- **Métricas**: tokens consumidos, mensagens, tool calls

## Integração Com Memory.Md

O ACTIVE_CONTEXT.md é automaticamente copiado para:
`C:\Users\renat\.claude\projects\C--Users-renat-skills\memory\MEMORY.md`

Como o MEMORY.md é incluído no system prompt de toda sessão, o Claude
sempre começa sabendo o estado atual dos projetos, tarefas pendentes
e decisões tomadas — sem precisar de nenhuma ação manual.

## Referências

- Para formato detalhado dos arquivos: `references/context-format.md`
- Para regras de compressão e arquivamento: `references/compression-rules.md`

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `context-guardian` - Complementary skill for enhanced analysis

---

## Reference: Compression Rules

# Regras de Compressão e Arquivamento

## Quando Arquivar

Uma sessão é candidata a arquivamento quando:
- Está há mais de 20 sessões no passado
- Configurable via `ARCHIVE_AFTER_SESSIONS` em `config.py`

## O que Manter no Arquivo

Seções preservadas (informação durável):
- **Tópicos**: sempre mantidos
- **Decisões**: sempre mantidas (formam base de conhecimento)
- **Tarefas pendentes**: mantidas se ainda não completadas
- **Descobertas**: sempre mantidas
- **Erros resolvidos**: sempre mantidos (evita re-trabalho)

Seções removidas (informação efêmera):
- **Métricas**: tokens, contadores (dados transitórios)
- **Arquivos modificados**: detalhes granulares desnecessários a longo prazo
- **Dívida técnica**: frequentemente já resolvida

## Consolidação de Arquivo

Quando `archive/` acumula 5+ sessões individuais, elas são consolidadas
em um único `ARCHIVE_YYYY.md` com formato ultra-compacto:

```markdown
# Arquivo Consolidado — 2026

### Sessão 001 — 2026-01-15
  - Decisão sobre arquitetura
  - Decisão sobre banco de dados

### Sessão 002 — 2026-01-20
  - Decisão sobre API
```

Apenas cabeçalhos e decisões são mantidos na consolidação.

## Manutenção do ACTIVE_CONTEXT.md

Para manter o limite de 150 linhas:

1. **Tarefas completadas**: removidas automaticamente ao salvar nova sessão
2. **Decisões antigas**: podadas após 30 dias (configurable)
3. **Sessões recentes**: mantidas apenas as últimas 5
4. **Bloqueadores resolvidos**: removidos quando não mais mencionados
5. **Convenções**: mantidas permanentemente (raramente mudam)

## Detecção de Drift

O sistema verifica se `ACTIVE_CONTEXT.md` e `MEMORY.md` estão sincronizados.
Se divergirem (edição manual, corrupção), `maintain` corrige automaticamente.

## Fluxo de Auto-Manutenção

```
maintain
  ├── Verificar sessões antigas → arquivar
  ├── Consolidar arquivo se necessário
  ├── Verificar drift ACTIVE_CONTEXT ↔ MEMORY.md → sincronizar
  └── Reindexar busca FTS5
```

---

## Reference: Context Format

# Especificação de Formatos — Context Agent

## session-NNN.md

Cada arquivo de sessão segue este formato:

```markdown
# Sessão NNN — YYYY-MM-DD
**Slug:** session-slug | **Duração:** ~Xmin | **Modelo:** claude-opus-4-6

## Tópicos
- Assunto principal discutido
- Outro assunto

## Decisões
- Decisão tomada e por quê

## Tarefas Concluídas
- [x] Tarefa que foi completada

## Tarefas Pendentes
- [ ] Tarefa que ficou pendente (prioridade: alta|média|baixa)

## Arquivos Modificados
- `path/to/file.py` — edit|write

## Descobertas
- Insight técnico importante

## Erros Resolvidos
- Descrição do erro encontrado

## Questões em Aberto
- Pergunta que ficou sem resposta

## Dívida Técnica
- Item de dívida técnica identificado

## Métricas
- Input tokens: N
- Output tokens: N
- Cache tokens: N
- Mensagens: N
- Tool calls: N

---
*Sessão anterior: [session-NNN-1](session-NNN-1.md)*
```

## ACTIVE_CONTEXT.md

Máximo de 150 linhas. Formato:

```markdown
# Contexto Ativo — Atualizado em YYYY-MM-DD HH:MM

## Projetos Ativos
| Projeto | Status | Última Sessão | Próxima Ação |
|---------|--------|---------------|--------------|
| Nome    | ativo  | session-NNN   | Ação         |

## Tarefas Pendentes
### Alta Prioridade
- [ ] Tarefa (desde session-NNN)
### Média Prioridade
- [ ] Tarefa
### Baixa Prioridade
- [ ] Tarefa

## Decisões Recentes
- [session-NNN] Decisão tomada

## Bloqueadores Ativos
- Bloqueador ou "Nenhum"

## Convenções Estabelecidas
- Padrão adotado

## Últimas Sessões
- session-NNN: Tópico 1, Tópico 2
```

## PROJECT_REGISTRY.md

```markdown
# Registro de Projetos — Atualizado em YYYY-MM-DD HH:MM

| Projeto | Status | Última Interação | Próximas Ações |
|---------|--------|------------------|----------------|
| Nome    | ativo  | YYYY-MM-DD (session-NNN) | Ação1; Ação2 |
```

## MEMORY.md

Cópia do ACTIVE_CONTEXT.md com cabeçalho adicional:

```markdown
<!-- Auto-generated by context-agent. Para detalhes:
python C:\Users\renat\skills\context-agent\scripts\context_manager.py load -->

[Conteúdo idêntico ao ACTIVE_CONTEXT.md]
```

## context.db (SQLite FTS5)

Tabela virtual para busca full-text:

```sql
CREATE VIRTUAL TABLE session_search USING fts5(
    session_number,    -- "001", "002", etc.
    date,              -- "2026-02-25"
    section,           -- "topics", "decisions", etc.
    content,           -- Texto completo da seção
    tokenize='unicode61'
);
```
