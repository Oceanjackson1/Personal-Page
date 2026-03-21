---
title: "Skill Sentinel"
description: "Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude."
category: "development"
source: "community"
author: "Community"
tags: ["skill", "sentinel"]
date: 2026-03-20
---

# Skill Sentinel

## Overview

Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude.

## When to Use This Skill

- When the user mentions "auditar skills" or related topics
- When the user mentions "qualidade skills" or related topics
- When the user mentions "verificar skills ecossistema" or related topics
- When the user mentions "saude ecossistema skills" or related topics
- When the user mentions "skills duplicadas" or related topics
- When the user mentions "otimizar skills" or related topics

## Do Not Use This Skill When

- The task is unrelated to skill sentinel
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Meta-agente que monitora, audita e evolui o ecossistema de skills. Analisa
todas as skills em 7 dimensoes, identifica problemas, sugere melhorias
e recomenda novas skills especialistas.

## Resumo Rapido

| Area | Script | O que faz |
|------|--------|-----------|
| **Discovery** | `scanner.py` | Descobre todas as skills automaticamente |
| **Qualidade** | `analyzers/code_quality.py` | Complexidade, docstrings, error handling |
| **Seguranca** | `analyzers/security.py` | Secrets, SQL injection, HTTPS |
| **Performance** | `analyzers/performance.py` | API calls, caching, retry |
| **Governanca** | `analyzers/governance_audit.py` | Rate limits, audit log, confirmacoes |
| **Documentacao** | `analyzers/documentation.py` | SKILL.md, triggers, references |
| **Dependencias** | `analyzers/dependencies.py` | requirements.txt, versoes |
| **Cross-Skill** | `analyzers/cross_skill.py` | Duplicacao, padroes compartilhados |
| **Custos** | `cost_optimizer.py` | Tokens, verbosidade, output |
| **Recomendacoes** | `recommender.py` | Gap analysis, novas skills |
| **Relatorio** | `report_generator.py` | Markdown estruturado |
| **Orquestracao** | `run_audit.py` | CLI principal |

## Localizacao

```
C:\Users\renat\skills\skill-sentinel\
├── SKILL.md
├── scripts/
│   ├── requirements.txt
│   ├── config.py
│   ├── db.py
│   ├── governance.py
│   ├── scanner.py
│   ├── analyzers/
│   │   ├── code_quality.py
│   │   ├── security.py
│   │   ├── performance.py
│   │   ├── governance_audit.py
│   │   ├── documentation.py
│   │   ├── dependencies.py
│   │   └── cross_skill.py
│   ├── recommender.py
│   ├── cost_optimizer.py
│   ├── report_generator.py
│   └── run_audit.py
├── references/
│   ├── analysis_criteria.md
│   ├── security_patterns.md
│   ├── skill_template.md
│   └── schema.md
└── data/
    ├── sentinel.db
    └── reports/
```

## Instalacao

```bash
pip install -r C:\Users\renat\skills\skill-sentinel\scripts\requirements.txt
```

## Comandos Principais

```bash

## Auditoria Completa De Todas As Skills

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py

## Auditar Apenas Uma Skill

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --skill instagram

## Apenas Recomendacoes De Novas Skills

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --recommend

## Comparar Com Auditoria Anterior (Tendencias)

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --compare

## Output Em Json (Para Processamento)

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --format json

## Ver Historico De Auditorias

python C:\Users\renat\skills\skill-sentinel\scripts\run_audit.py --history

## Descobrir Skills Disponiveis

python C:\Users\renat\skills\skill-sentinel\scripts\scanner.py

## Ver Audit Log Do Sentinel

python C:\Users\renat\skills\skill-sentinel\scripts\governance.py

## Verificar Banco De Dados

python C:\Users\renat\skills\skill-sentinel\scripts\db.py
```

## 1. Qualidade De Codigo (Peso: 20%)

- Complexidade ciclomatica por funcao (limiar: 10)
- Tamanho de funcoes (limiar: 50 linhas)
- Tamanho de arquivos (limiar: 500 linhas)
- Cobertura de docstrings
- Padroes de error handling (bare except, broad except)

## 2. Seguranca (Peso: 20%)

- Secrets hardcoded (tokens, passwords, API keys)
- SQL injection (f-strings em queries)
- URLs HTTP inseguras
- Tokens em logs
- Validacao de input

## 3. Performance (Peso: 15%)

- Retry com backoff para APIs
- Timeouts configurados
- Reuso de conexoes HTTP
- N+1 queries
- Async/concorrencia

## 4. Governanca (Peso: 15%)

- Nivel 0: Nenhuma
- Nivel 1: Action logging
- Nivel 2: Logging + rate limiting
- Nivel 3: Completa (+ confirmacoes 2-step)
- Nivel 4: Avancada (+ alertas e trends)

## 5. Documentacao (Peso: 15%)

- SKILL.md com frontmatter (name, description, version)
- Trigger keywords (PT-BR e EN)
- Secoes obrigatorias e recomendadas
- Reference files

## 6. Dependencias (Peso: 15%)

- requirements.txt presente
- Versoes pinadas
- Deps importadas vs listadas
- Deps listadas vs importadas

## 7. Cross-Skill (Analise Global)

- Modulos duplicados entre skills
- Padroes de Database compartilhados
- Governanca inconsistente
- Oportunidades de extracao

## Otimizacao De Custos

Alem das 7 dimensoes, o sentinel analisa impacto de custo:
- Tamanho do SKILL.md (tokens consumidos por ativacao)
- References grandes sem indice
- Output verboso dos scripts
- Ausencia de output JSON estruturado

## Gap Analysis E Recomendacoes

O recommender identifica capacidades ausentes no ecossistema comparando
com uma taxonomia de 20 categorias e gera templates de SKILL.md prontos
para novas skills sugeridas.

## Governanca Do Sentinel

O proprio sentinel pratica o que prega:
- Todas as auditorias sao registradas em action_log
- Historico de scores em score_history para tendencias
- Relatorios salvos em data/reports/

## Workflows Comuns

**1. Primeira auditoria do ecossistema:**
```
python run_audit.py
```
Gera relatorio completo com scores, findings e recomendacoes.

**2. Monitorar evolucao ao longo do tempo:**
```
python run_audit.py --compare
```
Mostra delta de scores entre auditorias.

**3. Validar uma skill antes de deploy:**
```
python run_audit.py --skill nome-da-skill
```
Auditoria focada com findings especificos.

**4. Identificar proxima skill a criar:**
```
python run_audit.py --recommend
```
Gap analysis com templates prontos.

## Formato Do Relatorio

O relatorio gerado em `data/reports/` contem:
1. Resumo executivo (tabela de scores)
2. Tendencias (se houver auditoria anterior)
3. Findings por severidade (critico/alto/medio/baixo/info)
4. Analise por skill (detalhada)
5. Recomendacoes de novas skills
6. Plano de acao priorizado

## Referencias

Para detalhes tecnicos, consultar:
- `references/analysis_criteria.md` - Rubricas de scoring
- `references/security_patterns.md` - Padroes de seguranca
- `references/skill_template.md` - Template para novas skills
- `references/schema.md` - Schema do banco de dados

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `skill-installer` - Complementary skill for enhanced analysis

---

## Reference: Analysis_Criteria

# Criterios de Analise - Skill Sentinel

## Scoring por Dimensao

Cada dimensao inicia com score 100 e sofre deducoes por violacoes encontradas.
Score final: max(0, min(100, score)).

### Qualidade de Codigo

| Criterio | Penalidade | Limiar |
|----------|-----------|---------|
| Complexidade ciclomatica > 10 | -5 por funcao | CC > 10 |
| Funcao > 50 linhas | -3 por funcao | > 50 linhas |
| Arquivo > 500 linhas | -5 por arquivo | > 500 linhas |
| Funcao publica sem docstring | -1 por funcao | Publicas (sem _) |
| Bare except | -8 por ocorrencia | `except:` |
| except Exception sem log | -3 por ocorrencia | Sem logging |
| Erro de sintaxe | -15 por arquivo | SyntaxError |

### Seguranca

| Criterio | Penalidade |
|----------|-----------|
| Secret hardcoded (critical) | -20 |
| SQL injection (high) | -15 |
| Token em log (high) | -10 |
| URL HTTP insegura (medium) | -5 |
| Input validation fraca (low) | -2 |
| Bonus: modulo auth | +5 |
| Bonus: usa env vars | +5 |

### Performance

| Criterio | Penalidade |
|----------|-----------|
| Sem retry/backoff | -10 |
| Sem timeout | -5 |
| Sem connection reuse | -3 |
| N+1 query | -8 |
| Conexao em loop | -5 |
| Bonus: retry | +5 |
| Bonus: async/concurrency | +5 |
| Bonus: caching | +3 |

### Governanca

Score direto baseado no nivel de maturidade:
- Nivel 0 (nenhuma): 0 pts
- Nivel 1 (action log): 25 pts
- Nivel 2 (+ rate limit): 50 pts
- Nivel 3 (+ confirmacoes): 75 pts
- Nivel 4 (+ alertas): 100 pts

### Documentacao

| Criterio | Penalidade |
|----------|-----------|
| Sem campo name no frontmatter | -20 |
| Sem campo description | -20 |
| Sem campo version | -3 |
| Triggers fracas (< 10 palavras) | -10 |
| Secao recomendada faltando | -3 cada |
| References vazio | -5 |
| SKILL.md < 20 linhas | -10 |

### Dependencias

| Criterio | Penalidade |
|----------|-----------|
| Sem requirements.txt | -15 |
| Versao nao pinada | -2 por dep |
| Dep importada nao listada | -2 por dep |

## Score Composto

```
overall = sum(score_dimensao * peso_dimensao) / sum(pesos)
```

Pesos padrao:
- code_quality: 0.20
- security: 0.20
- performance: 0.15
- governance: 0.15
- documentation: 0.15
- dependencies: 0.15

## Labels

| Range | Label |
|-------|-------|
| 90-100 | Excelente |
| 75-89 | Bom |
| 50-74 | Adequado |
| 25-49 | Precisa melhorar |
| 0-24 | Critico |

---

## Reference: Schema

# Schema do Banco de Dados - Sentinel

Banco: `data/sentinel.db` (SQLite, WAL mode)

## Tabelas

### audit_runs
Cada execucao de auditoria.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| started_at | TEXT | Timestamp ISO 8601 |
| completed_at | TEXT | Timestamp conclusao |
| skills_scanned | INTEGER | Quantidade de skills |
| total_findings | INTEGER | Total de findings |
| overall_score | REAL | Score medio do ecossistema |
| report_path | TEXT | Path do relatorio .md |
| status | TEXT | running / completed / failed |

### skill_snapshots
Estado de cada skill em cada auditoria.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| audit_run_id | INTEGER FK | Ref audit_runs |
| skill_name | TEXT | Nome da skill |
| skill_path | TEXT | Path no filesystem |
| version | TEXT | Versao do SKILL.md |
| file_count | INTEGER | Arquivos Python |
| line_count | INTEGER | Total de linhas |
| overall_score | REAL | Score composto |
| code_quality | REAL | Score qualidade |
| security | REAL | Score seguranca |
| performance | REAL | Score performance |
| governance | REAL | Score governanca |
| documentation | REAL | Score documentacao |
| dependencies | REAL | Score dependencias |
| raw_metrics | TEXT | JSON com metricas detalhadas |

### findings
Problemas e recomendacoes individuais.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| audit_run_id | INTEGER FK | Ref audit_runs |
| skill_name | TEXT | Skill afetada |
| dimension | TEXT | code_quality/security/etc |
| severity | TEXT | critical/high/medium/low/info |
| category | TEXT | Categoria especifica |
| title | TEXT | Titulo curto |
| description | TEXT | Descricao detalhada |
| file_path | TEXT | Arquivo afetado |
| line_number | INTEGER | Linha afetada |
| recommendation | TEXT | Sugestao de correcao |
| effort | TEXT | low/medium/high |
| impact | TEXT | low/medium/high |

### skill_recommendations
Sugestoes de novas skills.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| audit_run_id | INTEGER FK | Ref audit_runs |
| suggested_name | TEXT | Nome sugerido |
| rationale | TEXT | Justificativa |
| capabilities | TEXT | JSON array de capacidades |
| priority | TEXT | critical/high/medium/low |
| skill_md_draft | TEXT | Rascunho de SKILL.md |

### score_history
Historico de scores para analise de tendencias.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| audit_run_id | INTEGER FK | Ref audit_runs |
| skill_name | TEXT | Nome da skill |
| dimension | TEXT | Dimensao |
| score | REAL | Score registrado |
| recorded_at | TEXT | Timestamp |

### action_log
Auto-governanca do sentinel.

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| id | INTEGER PK | Auto-increment |
| action | TEXT | Tipo de acao |
| params | TEXT | JSON com parametros |
| result | TEXT | JSON com resultado |
| created_at | TEXT | Timestamp |

## Indices

- `idx_snapshots_run` - skill_snapshots(audit_run_id)
- `idx_snapshots_skill` - skill_snapshots(skill_name)
- `idx_findings_run` - findings(audit_run_id)
- `idx_findings_skill` - findings(skill_name)
- `idx_findings_severity` - findings(severity)
- `idx_findings_dim` - findings(dimension)
- `idx_history_skill` - score_history(skill_name)
- `idx_history_time` - score_history(recorded_at)
- `idx_action_log_time` - action_log(created_at)

---

## Reference: Security_Patterns

# Padroes de Seguranca

## Padroes Bons (Referencia)

### Queries parametrizadas (como instagram/scripts/db.py)
```python
# BOM: usar ? como placeholder
conn.execute("SELECT * FROM posts WHERE id = ?", [post_id])
conn.execute(
    "INSERT INTO accounts (ig_user_id, username) VALUES (?, ?)",
    [ig_user_id, username]
)
```

### Variaveis de ambiente para secrets
```python
# BOM: secrets em env vars
import os
API_KEY = os.environ.get("API_KEY")
APP_SECRET = os.getenv("APP_SECRET")
```

### Token refresh com validacao
```python
# BOM: verificar expiracao antes de usar
if token_expires_at and datetime.now() >= token_expires_at:
    token = refresh_token(refresh_token_value)
```

### Rate limiting com threshold
```python
# BOM: padrão GovernanceManager
if requests_used >= LIMIT * 0.9:
    warnings.append("Proximo do limite")
if requests_used >= LIMIT:
    raise RateLimitExceeded(...)
```

## Padroes Ruins (Detectados pelo Sentinel)

### Secrets hardcoded
```python
# RUIM: secret direto no codigo
API_KEY = "sk-abc123def456"
PASSWORD = "minha_senha_123"
```

### SQL injection via f-string
```python
# RUIM: interpolacao em SQL
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
cursor.execute("SELECT * FROM users WHERE name = '%s'" % name)
```

### URL HTTP insegura
```python
# RUIM: HTTP sem TLS
API_URL = "http://api.external.com/data"
```

### Token em log
```python
# RUIM: logando credencial
print(f"Token: {access_token}")
logging.info(f"Usando key: {api_key}")
```

### Bare except
```python
# RUIM: engolindo todos os erros
try:
    do_something()
except:
    pass
```

## Excecoes Conhecidas

Alguns valores parecem secrets mas sao publicos:
- `546c25a59c58ad7` - Imgur anonymous upload client ID (publico)
- Chaves de teste/exemplo em documentacao

---

## Reference: Skill_Template

# Template para Novas Skills

Use este template ao criar skills recomendadas pelo Sentinel.

## Estrutura de Diretorio

```
nome-da-skill/
├── SKILL.md                    # Metadata + documentacao
├── scripts/
│   ├── requirements.txt        # Dependencias Python
│   ├── config.py               # Paths, constantes, thresholds
│   ├── db.py                   # SQLite persistence (WAL mode)
│   ├── governance.py           # Rate limits, audit log, confirmacoes
│   └── [feature_modules].py    # Modulos de funcionalidade
├── references/
│   ├── api-reference.md        # Documentacao de APIs
│   ├── schema.md               # Schema do banco de dados
│   └── [domain].md             # Docs especificos do dominio
└── data/
    ├── nome-da-skill.db        # SQLite (WAL mode)
    └── exports/                # Arquivos exportados
```

## Template SKILL.md

```yaml
---
name: nome-da-skill
description: >-
  Descricao completa com trigger keywords em PT-BR e EN.
  Use quando o usuario mencionar: keyword1, keyword2, keyword3.
  Triggers: trigger1, trigger2, trigger3.
version: 1.0.0
---

# Skill: Nome da Skill

Descricao breve do que a skill faz.

## Resumo Rapido

| Area | Script | O que faz |
|------|--------|-----------|
| Core | config.py | Configuracao central |
| Core | db.py | Persistencia SQLite |
| Core | governance.py | Governanca |
| Feature | feature.py | Funcionalidade principal |

## Localizacao

[arvore de diretorios]

## Instalacao

[comando pip install]

## Comandos Principais

[exemplos de uso CLI]

## Governanca

[descricao de rate limits, audit log, confirmacoes]

## Referencias

[links para docs em references/]
```

## Template config.py

```python
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "nome-da-skill.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
```

## Template db.py

```python
import sqlite3
from config import DB_PATH

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init(self):
        with self._connect() as conn:
            conn.executescript(DDL)
```

## Checklist de Qualidade

- [ ] SKILL.md com frontmatter (name, description, version)
- [ ] Description com triggers bilingues (PT-BR + EN)
- [ ] requirements.txt com versoes pinadas
- [ ] config.py com paths padrao
- [ ] db.py com WAL mode e row_factory
- [ ] governance.py com action log
- [ ] Pelo menos 1 reference doc
- [ ] Sem secrets hardcoded
- [ ] Queries SQL parametrizadas
- [ ] Error handling especifico (sem bare except)
