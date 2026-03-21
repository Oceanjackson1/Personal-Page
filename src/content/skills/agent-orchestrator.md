---
title: "Agent Orchestrator"
description: "Meta-skill que orquestra todos os agentes do ecossistema. Scan automatico de skills, match por capacidades, coordenacao de workflows multi-skill e registry management."
category: "workflow"
source: "community"
author: "Community"
tags: ["agent", "orchestrator"]
date: 2026-03-20
---

# Agent Orchestrator

## Overview

Meta-skill que orquestra todos os agentes do ecossistema. Scan automatico de skills, match por capacidades, coordenacao de workflows multi-skill e registry management.

## When to Use This Skill

- When you need specialized assistance with this domain

## Do Not Use This Skill When

- The task is unrelated to agent orchestrator
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Meta-skill que funciona como camada central de decisao e coordenacao para todo
o ecossistema de skills. Faz varredura automatica, identifica agentes relevantes
e orquestra multiplos skills para tarefas complexas.

## Principio: Zero Intervencao Manual

- **SEMPRE faz varredura** antes de processar qualquer solicitacao
- Novas skills sao **auto-detectadas e incluidas** ao criar SKILL.md em qualquer subpasta
- Skills removidas sao **auto-excluidas** do registry
- Nenhum comando manual e necessario para registrar novas skills

---

## Workflow Obrigatorio (Toda Solicitacao)

Execute estes passos ANTES de processar qualquer request do usuario.
Os scripts usam paths relativos automaticamente - funciona de qualquer diretorio.

## Passo 1: Auto-Discovery (Varredura)

```bash
python agent-orchestrator/scripts/scan_registry.py
```

Ultra-rapido (<100ms) via cache de hashes MD5. So re-processa arquivos alterados.
Retorna JSON com resumo de todos os skills encontrados.

## Passo 2: Match De Skills

```bash
python agent-orchestrator/scripts/match_skills.py "<solicitacao do usuario>"
```

Retorna JSON com skills ranqueadas por relevancia. Interpretar o resultado:

| Resultado              | Acao                                                    |
|:-----------------------|:--------------------------------------------------------|
| `matched: 0`          | Nenhum skill relevante. Operar normalmente sem skills.  |
| `matched: 1`          | Um skill relevante. Carregar seu SKILL.md e seguir.     |
| `matched: 2+`         | Multiplos skills. Executar Passo 3 (orquestracao).      |

## Passo 3: Orquestracao (Se Matched >= 2)

```bash
python agent-orchestrator/scripts/orchestrate.py --skills skill1,skill2 --query "<solicitacao>"
```

Retorna plano de execucao com padrao, ordem dos steps e data flow entre skills.

## Passo Rapido (Atalho)

Para queries simples, os passos 1+2 podem ser combinados em sequencia:
```bash
python agent-orchestrator/scripts/scan_registry.py && python agent-orchestrator/scripts/match_skills.py "<solicitacao>"
```

---

## Skill Registry

O registry vive em:
```
agent-orchestrator/data/registry.json
```

## Locais De Busca

O scanner procura SKILL.md em:
1. `.claude/skills/*/` (skills registradas no Claude Code)
2. `*/` (skills standalone no top-level)
3. `*/*\` (skills em subpastas, ate profundidade 3)

## Metadata Por Skill

Cada entrada no registry contem:

| Campo          | Descricao                                          |
|:---------------|:---------------------------------------------------|
| name           | Nome da skill (do frontmatter YAML)                |
| description    | Descricao completa (triggers inclusos)             |
| location       | Caminho absoluto do diretorio                      |
| skill_md       | Caminho absoluto do SKILL.md                       |
| registered     | Se esta em .claude/skills/ (true/false)            |
| capabilities   | Tags de capacidade (auto-extraidas + explicitas)   |
| triggers       | Keywords de ativacao extraidas da description      |
| language       | Linguagem principal (python/nodejs/bash/none)      |
| status         | active / incomplete / missing                      |

## Comandos Do Registry

```bash

## Scan Rapido (Usa Cache De Hashes)

python agent-orchestrator/scripts/scan_registry.py

## Tabela De Status Detalhada

python agent-orchestrator/scripts/scan_registry.py --status

## Re-Scan Completo (Ignora Cache)

python agent-orchestrator/scripts/scan_registry.py --force
```

---

## Algoritmo De Matching

Para cada solicitacao, o matcher pontua skills usando:

| Criterio                     | Pontos | Exemplo                               |
|:-----------------------------|:-------|:--------------------------------------|
| Nome do skill na query       | +15    | "use web-scraper" -> web-scraper      |
| Keyword trigger exata        | +10    | "scrape" -> web-scraper               |
| Categoria de capacidade      | +5     | data-extraction -> web-scraper        |
| Sobreposicao de palavras     | +1     | Palavras da query na description      |
| Boost de projeto             | +20    | Skill atribuida ao projeto ativo      |

Threshold minimo: 5 pontos. Skills abaixo disso sao ignoradas.

## Match Com Projeto

```bash
python agent-orchestrator/scripts/match_skills.py --project meu-projeto "query aqui"
```

Skills atribuidas ao projeto recebem +20 de boost automatico.

---

## Padroes De Orquestracao

Quando multiplos skills sao relevantes, o orchestrator classifica o padrao:

## 1. Pipeline Sequencial

Skills formam uma cadeia onde o output de uma alimenta a proxima.

**Quando:** Mix de skills "produtoras" (data-extraction, government-data) e "consumidoras" (messaging, social-media).

**Exemplo:** web-scraper coleta precos -> whatsapp-cloud-api envia alerta

```
user_query -> web-scraper -> whatsapp-cloud-api -> result
```

## 2. Execucao Paralela

Skills trabalham independentemente em aspectos diferentes da solicitacao.

**Quando:** Todas as skills tem o mesmo papel (todas produtoras ou todas consumidoras).

**Exemplo:** instagram publica post + whatsapp envia notificacao (ambos recebem o mesmo conteudo)

```
user_query -> [instagram, whatsapp-cloud-api] -> aggregated_result
```

## 3. Primario + Suporte

Uma skill principal lidera; outras fornecem dados de apoio.

**Quando:** Uma skill tem score muito superior as demais (>= 2x).

**Exemplo:** whatsapp-cloud-api envia mensagem (primario) + web-scraper fornece dados (suporte)

```
user_query -> whatsapp-cloud-api (primary) + web-scraper (support) -> result
```

## Detalhes Em `References/Orchestration-Patterns.Md`

---

## Gerenciamento De Projetos

Atribuir skills a projetos permite boost de relevancia e contexto persistente.

## Arquivo De Projetos

```
agent-orchestrator/data/projects.json
```

## Operacoes

**Criar projeto:**
Adicionar entrada ao projects.json:
```json
{
  "name": "nome-do-projeto",
  "created_at": "2026-02-25T12:00:00",
  "skills": ["web-scraper", "whatsapp-cloud-api"],
  "description": "Descricao do projeto"
}
```

**Adicionar skill a projeto:** Atualizar o array `skills` do projeto.

**Remover skill de projeto:** Remover do array `skills`.

**Consultar skills do projeto:** Ler o projects.json e listar skills atribuidas.

---

## Adicionando Novas Skills

Para adicionar uma nova skill ao ecossistema:

1. Criar uma pasta em qualquer lugar sob `skills root:`
2. Criar um `SKILL.md` com frontmatter YAML:
```yaml
---
name: minha-nova-skill
description: "Descricao com keywords de ativacao..."
---

## Documentacao Da Skill

```
3. **Pronto!** O auto-discovery detecta automaticamente na proxima solicitacao.

Opcionalmente, para discovery nativo do Claude Code:
4. Copiar o SKILL.md para `.claude/skills/<nome>/SKILL.md`

## Tags De Capacidade Explicitas (Opcional)

Adicionar ao frontmatter para matching mais preciso:
```yaml
capabilities: [data-extraction, web-automation]
```

---

## Ver Status De Todos Os Skills

```bash
python agent-orchestrator/scripts/scan_registry.py --status
```

## Interpretar Status

| Status     | Significado                                        |
|:-----------|:---------------------------------------------------|
| active     | SKILL.md com name + description presentes          |
| incomplete | SKILL.md existe mas falta name ou description      |
| missing    | Diretorio existe mas sem SKILL.md                  |

---

## Skills Atuais Do Ecossistema

| Skill              | Capacidades                           | Status  |
|:-------------------|:--------------------------------------|:--------|
| web-scraper        | data-extraction, web-automation       | active  |
| junta-leiloeiros   | government-data, data-extraction      | active  |
| whatsapp-cloud-api | messaging, api-integration            | active  |
| instagram          | social-media, api-integration         | partial |

*Esta tabela e atualizada automaticamente via `scan_registry.py --status`.*

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `multi-advisor` - Complementary skill for enhanced analysis
- `task-intelligence` - Complementary skill for enhanced analysis

---

## Reference: Capability Taxonomy

# Taxonomia de Capacidades (Capability Tags)

Categorias padrao para classificar skills no ecossistema.
Cada skill pode ter multiplas categorias.

---

## Categorias

### data-extraction
**Descricao:** Coleta e extracao de dados de fontes web ou APIs.
**Keywords PT:** raspar, extrair, coletar, dados, tabela
**Keywords EN:** scrape, extract, crawl, parse, harvest, collect, data, table, csv
**Skills atuais:** web-scraper, junta-leiloeiros

### messaging
**Descricao:** Envio e recebimento de mensagens via plataformas de comunicacao.
**Keywords PT:** mensagem, enviar, notificacao, atendimento, comunicar, avisar
**Keywords EN:** whatsapp, message, send, chat, notify, notification, sms
**Skills atuais:** whatsapp-cloud-api

### social-media
**Descricao:** Interacao com plataformas de redes sociais (posts, stories, analytics).
**Keywords PT:** publicar, rede social, engajamento, post, stories
**Keywords EN:** instagram, facebook, twitter, post, stories, reels, social, feed, follower
**Skills atuais:** instagram

### government-data
**Descricao:** Coleta de dados governamentais, registros publicos, orgaos oficiais.
**Keywords PT:** junta, leiloeiro, cadastro, governo, comercial, tribunal, certidao, registro
**Keywords EN:** government, registry, official, court, public records
**Skills atuais:** junta-leiloeiros

### web-automation
**Descricao:** Automacao de navegador, preenchimento de formularios, interacao com paginas.
**Keywords PT:** navegador, automatizar, automacao, preencher
**Keywords EN:** browser, selenium, playwright, automate, click, fill form
**Skills atuais:** web-scraper

### api-integration
**Descricao:** Integracao com APIs externas, webhooks, autenticacao OAuth.
**Keywords PT:** integracao, integrar, conectar, api, webhook
**Keywords EN:** api, endpoint, webhook, rest, graph, oauth, token
**Skills atuais:** whatsapp-cloud-api, instagram

### analytics
**Descricao:** Analise de dados, metricas, dashboards, relatorios.
**Keywords PT:** relatorio, metricas, analise, estatistica
**Keywords EN:** insight, analytics, metrics, dashboard, report, stats
**Skills atuais:** (nenhuma dedicada ainda)

### content-management
**Descricao:** Publicacao, agendamento e gestao de conteudo em plataformas.
**Keywords PT:** publicar, agendar, conteudo, midia, template
**Keywords EN:** publish, schedule, template, content, media, upload
**Skills atuais:** instagram

---

## Roles (Papeis)

As categorias se agrupam em papeis para orquestracao:

| Papel      | Categorias                                      | Descricao                        |
|:-----------|:------------------------------------------------|:---------------------------------|
| Producer   | data-extraction, government-data, analytics     | Gera/coleta dados                |
| Consumer   | messaging, social-media, content-management     | Atua sobre dados (envia, publica)|
| Hybrid     | api-integration, web-automation                 | Pode produzir e consumir dados   |

---

## Como Declarar no SKILL.md

Adicionar campo `capabilities` ao frontmatter YAML:

```yaml
---
name: minha-skill
description: "..."
capabilities: [data-extraction, web-automation]
---
```

Se omitido, o scanner extrai automaticamente da `description` via keywords.
Tags explicitas tem prioridade e nao sao duplicadas com as auto-extraidas.

---

## Reference: Orchestration Patterns

# Padroes de Orquestracao Multi-Skill

Guia detalhado para coordenar multiplos skills em workflows complexos.

---

## 1. Pipeline Sequencial

Output de um skill alimenta o input do proximo.

### Quando Usar
- Mix de skills "produtoras" (data-extraction, government-data, analytics) e "consumidoras" (messaging, social-media, content-management)
- A tarefa tem etapas distintas: coletar -> processar -> entregar

### Fluxo
```
user_query -> Skill A (produtora) -> dados -> Skill B (consumidora) -> resultado
```

### Exemplo Concreto
**Solicitacao:** "Coletar precos de leiloeiros de SP e enviar por WhatsApp"
```
1. junta-leiloeiros: Executar scraper para SP, exportar dados
2. whatsapp-cloud-api: Formatar dados como mensagem e enviar
```

### Regras de Contexto
- O output de cada step deve ser passado como contexto para o proximo
- Formatos comuns de passagem: JSON, tabela Markdown, texto resumido
- Se um step falhar, interromper o pipeline e reportar ao usuario

---

## 2. Execucao Paralela

Skills trabalham independentemente em aspectos diferentes.

### Quando Usar
- Todas as skills tem o mesmo papel (todas produtoras OU todas consumidoras)
- Os aspectos da tarefa sao independentes entre si
- Nao ha dependencia de dados entre skills

### Fluxo
```
              ┌─> Skill A ─> output A ─┐
user_query ──>├─> Skill B ─> output B ─├──> resultado agregado
              └─> Skill C ─> output C ─┘
```

### Exemplo Concreto
**Solicitacao:** "Publicar a promocao no Instagram e enviar por WhatsApp"
```
1. (paralelo) instagram: Criar e publicar post da promocao
1. (paralelo) whatsapp-cloud-api: Enviar mensagem da promocao
-> Agregar: reportar status de ambas as publicacoes
```

### Regras de Contexto
- Cada skill recebe a query original completa
- Os outputs sao agregados em uma resposta unificada
- Se um skill falhar, os outros continuam normalmente
- Reportar sucesso/falha de cada skill individualmente

---

## 3. Primario + Suporte

Uma skill principal lidera; outras fornecem dados de apoio.

### Quando Usar
- Uma skill tem score de relevancia muito superior (>= 2x a proxima)
- A tarefa principal e clara, mas pode se beneficiar de dados adicionais
- Skills de suporte sao opcionais / "nice to have"

### Fluxo
```
user_query -> Skill A (primaria) ──────────────> resultado
                  ↑
              Skill B (suporte) ─> dados extras
```

### Exemplo Concreto
**Solicitacao:** "Configurar chatbot WhatsApp para responder com dados de leiloeiros"
```
1. (primaria) whatsapp-cloud-api: Configurar webhook e logica do chatbot
2. (suporte) junta-leiloeiros: Fornecer endpoint/dados para o chatbot consultar
```

### Regras de Contexto
- A skill primaria conduz o workflow
- Skills de suporte sao consultadas sob demanda
- Se skill de suporte falhar, a primaria deve continuar (graceful degradation)

---

## Tratamento de Erros

### Regras Gerais
1. **Falha em skill individual**: Reportar ao usuario qual skill falhou e por que
2. **Falha em pipeline**: Interromper e mostrar ate onde chegou
3. **Falha parcial em paralelo**: Continuar com as demais, reportar falha(s)
4. **Skill incomplete**: Avisar que a skill esta com status incompleto antes de tentar usa-la

### Fallback
- Se uma skill falha, verificar se outra skill tem capacidade similar
- Se nao houver alternativa, operar sem a skill e informar o usuario

---

## Serializacao de Contexto

Formato padrao para passar dados entre skills:

```json
{
  "source_skill": "web-scraper",
  "target_skill": "whatsapp-cloud-api",
  "data_type": "table",
  "data": [
    {"nome": "Joao Silva", "uf": "SP", "registro": "12345"},
    {"nome": "Maria Santos", "uf": "RJ", "registro": "67890"}
  ],
  "metadata": {
    "total_items": 2,
    "collected_at": "2026-02-25T12:00:00",
    "query": "leiloeiros de SP e RJ"
  }
}
```
