---
title: "Junta Leiloeiros"
description: "Coleta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON."
category: "development"
source: "community"
author: "Community"
tags: ["junta", "leiloeiros"]
date: 2026-03-20
---

# Skill: Leiloeiros das Juntas Comerciais do Brasil

## Overview

Coleta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON.

## When to Use This Skill

- When the user mentions "leiloeiro junta" or related topics
- When the user mentions "junta comercial leiloeiro" or related topics
- When the user mentions "scraper junta" or related topics
- When the user mentions "jucesp leiloeiro" or related topics
- When the user mentions "jucerja" or related topics
- When the user mentions "jucemg leiloeiro" or related topics

## Do Not Use This Skill When

- The task is unrelated to junta leiloeiros
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Coleta dados públicos de leiloeiros oficiais de todas as 27 Juntas Comerciais estaduais,
persiste em banco SQLite local e oferece API REST e exportação em múltiplos formatos.

## Localização

```
C:\Users\renat\skills\junta-leiloeiros\
├── scripts/
│   ├── scraper/
│   │   ├── base_scraper.py      ← classe abstrata
│   │   ├── states.py            ← registro dos 27 scrapers
│   │   ├── jucesp.py / jucerja.py / jucemg.py / jucec.py / jucis_df.py
│   │   └── generic_scraper.py   ← usado pelos 22 estados restantes
│   ├── db.py                    ← banco SQLite
│   ├── run_all.py               ← orquestrador de scraping
│   ├── serve_api.py             ← API FastAPI
│   ├── export.py                ← exportação
│   └── requirements.txt
├── references/
│   ├── juntas_urls.md           ← URLs e status de todas as 27 juntas
│   ├── schema.md                ← schema do banco
│   └── legal.md                 ← base legal
└── data/
    ├── leiloeiros.db            ← banco SQLite (criado no primeiro run)
    ├── scraping_log.json        ← log de cada coleta
    └── exports/                 ← arquivos exportados
```

## Instalação (Uma Vez)

```bash
pip install -r C:\Users\renat\skills\junta-leiloeiros\scripts\requirements.txt

## Para Sites Com Javascript:

playwright install chromium
```

## Coletar Dados

```bash

## Todos Os 27 Estados

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py

## Estados Específicos

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --estado SP RJ MG

## Ver O Que Seria Coletado Sem Executar

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --dry-run

## Controlar Paralelismo (Default: 5)

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --concurrency 3
```

## Estatísticas Por Estado

python C:\Users\renat\skills\junta-leiloeiros\scripts\db.py

## Sql Direto

sqlite3 C:\Users\renat\skills\junta-leiloeiros\data\leiloeiros.db \
  "SELECT estado, COUNT(*) FROM leiloeiros GROUP BY estado"
```

## Servir Api Rest

```bash
python C:\Users\renat\skills\junta-leiloeiros\scripts\serve_api.py

## Docs Interativos: Http://Localhost:8000/Docs

```

**Endpoints:**
- `GET /leiloeiros?estado=SP&situacao=ATIVO&nome=silva&limit=100`
- `GET /leiloeiros/{estado}` — ex: `/leiloeiros/SP`
- `GET /busca?q=texto`
- `GET /stats`
- `GET /export/json`
- `GET /export/csv`

## Exportar Dados

```bash
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format csv
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format json
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format all
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format csv --estado SP
```

## Usar Em Código Python

```python
import sys
sys.path.insert(0, r"C:\Users\renat\skills\junta-leiloeiros\scripts")
from db import Database

db = Database()
db.init()

## Todos Os Leiloeiros Ativos De Sp

leiloeiros = db.get_all(estado="SP", situacao="ATIVO")

## Busca Por Nome

resultados = db.search("silva")

## Estatísticas

stats = db.get_stats()
```

## Adicionar Scraper Customizado

Se um estado precisar de lógica específica (ex: site usa JavaScript):

```python

## Scripts/Scraper/Meu_Estado.Py

from .base_scraper import AbstractJuntaScraper, Leiloeiro
from typing import List

class MeuEstadoScraper(AbstractJuntaScraper):
    estado = "XX"
    junta = "JUCEX"
    url = "https://www.jucex.xx.gov.br/leiloeiros"

    async def parse_leiloeiros(self) -> List[Leiloeiro]:
        soup = await self.fetch_page()
        if not soup:
            return []
        # lógica específica aqui
        return [self.make_leiloeiro(nome="...", matricula="...")]
```

Registrar em `scripts/scraper/states.py`:
```python
from .meu_estado import MeuEstadoScraper
SCRAPERS["XX"] = MeuEstadoScraper
```

## Referências

- URLs de todas as juntas: `references/juntas_urls.md`
- Schema do banco: `references/schema.md`
- Base legal da coleta: `references/legal.md`
- Log de coleta: `data/scraping_log.json`

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `leiloeiro-avaliacao` - Complementary skill for enhanced analysis
- `leiloeiro-edital` - Complementary skill for enhanced analysis
- `leiloeiro-ia` - Complementary skill for enhanced analysis
- `leiloeiro-juridico` - Complementary skill for enhanced analysis
- `leiloeiro-mercado` - Complementary skill for enhanced analysis

---

## Reference: Juntas_Urls

# Juntas Comerciais do Brasil — URLs e Status de Scraping

Tabela de referência atualizada com todas as 27 Juntas Comerciais e seus sites de leiloeiros.
**Última verificação:** 2026-02-25

| UF | Junta | URL Leiloeiros | Método | Status |
|----|-------|---------------|--------|--------|
| SP | JUCESP | https://www.institucional.jucesp.sp.gov.br/tradutores-leiloeiros.html | httpx+BS4 | CUSTOMIZADO |
| RJ | JUCERJA | https://www.jucerja.rj.gov.br/AuxiliaresComercio/Leiloeiros | PLAYWRIGHT | CUSTOMIZADO |
| MG | JUCEMG | https://jucemg.mg.gov.br/pagina/139/leiloeiros-oficiais | httpx+BS4 | CUSTOMIZADO |
| ES | JUCEES | https://jucees.es.gov.br/leiloeiros | httpx+BS4 | GENÉRICO |
| RS | JUCISRS | https://sistemas.jucisrs.rs.gov.br/leiloeiros/ | PLAYWRIGHT | CUSTOMIZADO (domínio antigo: jucers.rs.gov.br APOSENTADO) |
| PR | JUCEPAR | https://www.juntacomercial.pr.gov.br/Pagina/LEILOEIROS-OFICIAIS | httpx+BS4 | CUSTOMIZADO (migrou de jucepar.pr.gov.br) |
| SC | JUCESC | https://leiloeiros.jucesc.sc.gov.br/site/ | httpx+BS4 | CUSTOMIZADO (subdomínio dedicado) |
| BA | JUCEB | https://www.ba.gov.br/juceb/home/matriculas-e-carteira-profissional/leiloeiros | httpx+BS4 | CUSTOMIZADO (migrou de juceb.ba.gov.br) |
| PE | JUCEPE | https://portal.jucepe.pe.gov.br/leiloeiros | PLAYWRIGHT | CUSTOMIZADO (SPA - migrou de jucepe.pe.gov.br) |
| CE | JUCEC | https://www.jucec.ce.gov.br/leiloeiros/ | httpx+BS4 | CUSTOMIZADO |
| MA | JUCEMA | http://www.jucema.ma.gov.br/leiloeiros | httpx+multi-URL | CUSTOMIZADO (múltiplas URLs tentadas) |
| PI | JUCEPI | https://portal.pi.gov.br/jucepi/leiloeiro-oficial/ | httpx+BS4 | CUSTOMIZADO (migrou para portal estadual) |
| RN | JUCERN | http://www.jucern.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=8695&ACT=&PAGE=0&PARM=&LBL=Leiloeiros | httpx+BS4 | CUSTOMIZADO (HTTP, query string) |
| PB | JUCEP | https://jucep.pb.gov.br/contatos/leiloeiros | httpx+BS4 | CUSTOMIZADO (domínio migrou para jucep.pb.gov.br) |
| AL | JUCEAL | http://www.juceal.al.gov.br/servicos/leiloeiros | httpx+BS4 | CUSTOMIZADO (URL: /servicos/leiloeiros) |
| SE | JUCESE | https://jucese.se.gov.br/leiloeiros/ | httpx+BS4 | GENÉRICO |
| DF | JUCIS-DF | https://jucis.df.gov.br/leiloeiros/ | httpx+BS4 | CUSTOMIZADO |
| GO | JUCEG | https://goias.gov.br/juceg/ | httpx+BS4 | GENÉRICO |
| MT | JUCEMAT | https://www.jucemat.mt.gov.br/leiloeiros | httpx+BS4 | GENÉRICO |
| MS | JUCEMS | https://www.jucems.ms.gov.br/empresas/controles-especiais/agentes-auxiliares/leiloeiros/ | httpx+BS4 | GENÉRICO (URL com path completo) |
| PA | JUCEPA | https://www.jucepa.pa.gov.br/node/171 | httpx+BS4 | CUSTOMIZADO (Drupal node ID) |
| AM | JUCEA | https://www.jucea.am.gov.br/leiloeiros/ | httpx+BS4 | GENÉRICO |
| RO | JUCER | https://rondonia.ro.gov.br/jucer/lista-de-leiloeiros-oficiais/ | httpx+BS4 | CUSTOMIZADO (migrou para portal estadual) |
| RR | JUCERR | https://jucerr.rr.gov.br/leiloeiros/ | httpx+BS4 | GENÉRICO |
| AP | JUCAP | http://www.jucap.ap.gov.br/leiloeiros | httpx (verify=False) | CUSTOMIZADO (cert TLS inválido) |
| AC | JUCEAC | https://juceac.ac.gov.br/leiloeiro/ | httpx+BS4 | CUSTOMIZADO (URL: /leiloeiro/ singular) |
| TO | JUCETINS | https://www.to.gov.br/jucetins/leiloeiros/152aezl6blm0 | httpx+BS4 | CUSTOMIZADO (domínio antigo: juceto.to.gov.br APOSENTADO) |

## Legenda de Status

- **CUSTOMIZADO**: Scraper dedicado com lógica específica para o formato da página
- **GENÉRICO**: Usa `GenericJuntaScraper` com detecção automática de tabela/lista
- **PLAYWRIGHT**: Requer renderização JS (browser headless)
- **INDISPONÍVEL**: Site fora do ar ou sem página de leiloeiros (registrado no log)

## Migrações Confirmadas (2025-2026)

| Antigo | Novo | Junta |
|--------|------|-------|
| jucers.rs.gov.br | jucisrs.rs.gov.br + sistemas.jucisrs.rs.gov.br | JUCISRS (renomeada) |
| jucepar.pr.gov.br | juntacomercial.pr.gov.br | JUCEPAR |
| jucesc.sc.gov.br/index.php | leiloeiros.jucesc.sc.gov.br/site/ | JUCESC |
| juceb.ba.gov.br | ba.gov.br/juceb | JUCEB |
| jucepe.pe.gov.br | portal.jucepe.pe.gov.br | JUCEPE |
| jucepa.pa.gov.br/index.php | jucepa.pa.gov.br/node/171 | JUCEPA |
| jucepi.pi.gov.br | portal.pi.gov.br/jucepi | JUCEPI |
| jucepb.pb.gov.br | jucep.pb.gov.br | JUCEP (renomeada) |
| juceal.al.gov.br/leiloeiros | juceal.al.gov.br/servicos/leiloeiros | JUCEAL |
| jucer.ro.gov.br | rondonia.ro.gov.br/jucer | JUCER |
| juceac.ac.gov.br/leiloeiros | juceac.ac.gov.br/leiloeiro/ | JUCEAC |
| juceto.to.gov.br | to.gov.br/jucetins | JUCETINS (renomeada) |
| jucers.ms.gov.br/leiloeiros | jucems.ms.gov.br/empresas/controles-especiais/agentes-auxiliares/leiloeiros/ | JUCEMS |

## Fontes Alternativas (fallback)

Caso um site esteja indisponível, verificar:
- **DREI**: https://www.gov.br/empresas-e-negocios/pt-br/drei/tradutores-e-leiloeiros
- **BomValor**: https://osleiloeiros.bomvalor.com.br/
- **InnLei**: https://innlei.org.br/juntas-comerciais
- **FENAJU**: https://www.fenaju.org.br/federados

## Integração com Web-Scraper (skill)

Para estados com baixa coleta ou sites problemáticos, o `web_scraper_fallback.py` aciona
automaticamente a skill web-scraper para extração inteligente adicional.

Execute: `python scripts/web_scraper_fallback.py --estado MA RN AP`

## Como Atualizar Este Arquivo

Após cada scraping, verificar no `data/scraping_log.json`:
- Estados com `status: VAZIO` → investigar se URL mudou
- Estados com `status: ERRO` → possível necessidade de Playwright
- Atualizar colunas `Método` e `URL` se necessário

---

## Reference: Legal

# Base Legal para Coleta de Dados de Leiloeiros

## Fundamento Legal

### Decreto nº 21.981/1932
Regulamento dos Leiloeiros Oficiais do Brasil. Estabelece que leiloeiros devem ser
matriculados nas Juntas Comerciais dos estados e que seus dados de registro são
**públicos por natureza**, sendo necessários para que o público possa verificar
a legitimidade do profissional antes de participar de um leilão.

### IN DREI nº 72/2019
Instrução Normativa do Departamento de Registro Empresarial e Integração.
Rege os procedimentos de registro de tradutores públicos e leiloeiros.
Confirma que matrícula, nome e situação cadastral são dados de acesso público.

### Lei Geral de Proteção de Dados (LGPD) — Lei nº 13.709/2018
**Art. 7º, II**: O tratamento de dados pessoais é permitido para o cumprimento
de obrigação legal ou regulatória pelo controlador.

**Art. 7º, III**: Permitido pelo poder público para execução de políticas públicas.

**Art. 13**: Dados anonimizados e dados públicos têm tratamento diferenciado.

Os dados coletados (nome, matrícula, situação, contato profissional) são
**dados públicos de registro profissional**, divulgados pelas próprias
juntas comerciais no cumprimento de obrigação legal.

### Lei de Acesso à Informação (LAI) — Lei nº 12.527/2011
Garante o direito de acesso a informações públicas. Os registros de leiloeiros
mantidos pelas juntas comerciais (órgãos públicos estaduais) são informações
de interesse público e devem ser disponibilizados.

## Responsabilidades na Coleta

### O que esta skill faz
- Acessa páginas **públicas** das juntas comerciais
- Coleta apenas informações **já disponíveis publicamente** nos sites oficiais
- Não acessa sistemas internos, áreas restritas ou APIs privadas
- Não realiza engenharia reversa de sistemas

### Boas Práticas Adotadas
1. **Rate limiting**: 2 segundos entre requests por domínio
2. **User-Agent identificável**: Header padrão de browser
3. **Retry limitado**: Máximo 3 tentativas com backoff exponencial
4. **Sem sobrecarga**: Máximo 5 scrapers simultâneos
5. **Dados sem deleção**: Histórico preservado

### Limitações
- Dados de **contato pessoal** (CPF, email, telefone residencial) tratados com
  cuidado — usados apenas para fins profissionais de identificação
- Não publicar nem transmitir dados a terceiros sem consentimento adicional
- Para uso comercial em larga escala, considerar contato formal com as juntas

## Referências

- [DREI — Tradutores e Leiloeiros](https://www.gov.br/empresas-e-negocios/pt-br/drei/tradutores-e-leiloeiros)
- [Decreto 21.981/1932](https://www.planalto.gov.br/ccivil_03/decreto/antigos/d21981.htm)
- [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [LAI](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm)

---

## Reference: Schema

# Schema de Dados — Leiloeiros das Juntas Comerciais

## Tabela `leiloeiros` (SQLite)

```sql
CREATE TABLE leiloeiros (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    estado           TEXT    NOT NULL,     -- UF: SP, RJ, MG, ...
    junta            TEXT    NOT NULL,     -- nome da junta: JUCESP, JUCERJA, ...
    matricula        TEXT,                 -- número de matrícula (pode ser NULL se não publicado)
    nome             TEXT    NOT NULL,     -- nome completo do leiloeiro
    cpf_cnpj         TEXT,                 -- CPF ou CNPJ (quando disponível)
    situacao         TEXT,                 -- ATIVO | CANCELADO | SUSPENSO | IRREGULAR
    endereco         TEXT,                 -- endereço completo
    municipio        TEXT,                 -- cidade
    telefone         TEXT,                 -- telefone de contato
    email            TEXT,                 -- e-mail
    data_registro    TEXT,                 -- data de registro na junta (ISO 8601 ou texto)
    data_atualizacao TEXT,                 -- última atualização cadastral
    url_fonte        TEXT,                 -- URL de onde o dado foi coletado
    scraped_at       TEXT    NOT NULL,     -- timestamp da coleta (ISO 8601 UTC)
    UNIQUE (estado, matricula) ON CONFLICT REPLACE
);
```

## Campos

| Campo | Tipo | Obrigatório | Valores |
|-------|------|-------------|---------|
| `id` | int | auto | PK auto-incremento |
| `estado` | text | sim | UF 2 letras maiúsculas |
| `junta` | text | sim | Nome da junta ex: JUCESP |
| `matricula` | text | não | Número de matrícula na junta |
| `nome` | text | sim | Nome completo |
| `cpf_cnpj` | text | não | Documento sem formatação preferencial |
| `situacao` | text | não | ATIVO, CANCELADO, SUSPENSO, IRREGULAR |
| `endereco` | text | não | Logradouro completo |
| `municipio` | text | não | Cidade |
| `telefone` | text | não | Formato livre |
| `email` | text | não | E-mail de contato |
| `data_registro` | text | não | Data ISO ou texto da junta |
| `data_atualizacao` | text | não | Data ISO ou texto da junta |
| `url_fonte` | text | não | URL da página coletada |
| `scraped_at` | text | sim | ISO 8601 UTC ex: 2024-03-15T10:30:00+00:00 |

## Normalização de `situacao`

Os textos das juntas são normalizados para valores padrão:

| Texto Original (exemplos) | Valor Normalizado |
|--------------------------|-------------------|
| Ativo, Regular, Habilitado, Regularizado | `ATIVO` |
| Cancelado, Baixado, Extinto | `CANCELADO` |
| Suspenso | `SUSPENSO` |
| Irregular | `IRREGULAR` |
| Qualquer outro | mantido como recebido |

## Formato de Exportação (JSON)

```json
{
  "exported_at": "2024-03-15T10:30:00+00:00",
  "total": 1234,
  "data": [
    {
      "id": 1,
      "estado": "SP",
      "junta": "JUCESP",
      "matricula": "001234",
      "nome": "João da Silva Leiloeiro",
      "cpf_cnpj": null,
      "situacao": "ATIVO",
      "endereco": "Rua das Flores, 100",
      "municipio": "São Paulo",
      "telefone": "(11) 3456-7890",
      "email": "joao@leiloes.com.br",
      "data_registro": "2010-05-20",
      "data_atualizacao": null,
      "url_fonte": "https://www.institucional.jucesp.sp.gov.br/tradutores-leiloeiros.html",
      "scraped_at": "2024-03-15T10:30:00+00:00"
    }
  ]
}
```

## Índices

```sql
CREATE INDEX idx_estado   ON leiloeiros (estado);
CREATE INDEX idx_nome     ON leiloeiros (nome);
CREATE INDEX idx_situacao ON leiloeiros (situacao);
CREATE INDEX idx_scraped  ON leiloeiros (scraped_at);
```
