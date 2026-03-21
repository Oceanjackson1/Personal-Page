---
title: "Instagram"
description: "Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator."
category: "workflow"
source: "community"
author: "Community"
tags: ["instagram"]
date: 2026-03-20
---

# Skill: Instagram Integration

## Overview

Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator.

## When to Use This Skill

- When the user mentions "instagram" or related topics
- When the user mentions "ig" or related topics
- When the user mentions "post instagram" or related topics
- When the user mentions "publicar instagram" or related topics
- When the user mentions "reels instagram" or related topics
- When the user mentions "stories instagram" or related topics

## Do Not Use This Skill When

- The task is unrelated to instagram
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Controle completo da conta Instagram via Graph API. Publicação, comunidade, analytics,
DMs, hashtags, templates e dashboard — tudo gerido com governança (rate limits, audit log,
confirmações antes de ações públicas).

## Resumo Rápido

| Área | Scripts | O que faz |
|------|---------|-----------|
| **Setup** | `account_setup.py`, `auth.py` | Configurar conta, OAuth, token |
| **Publicação** | `publish.py`, `schedule.py` | Publicar foto/vídeo/reel/story/carrossel, agendar |
| **Comunidade** | `comments.py`, `messages.py` | Comentários, DMs, menções |
| **Analytics** | `insights.py`, `analyze.py` | Métricas, melhores horários, top posts |
| **Hashtags** | `hashtags.py` | Pesquisa e tracking |
| **Inteligência** | `templates.py`, `analyze.py` | Templates de conteúdo, tendências |
| **Infra** | `export.py`, `serve_api.py`, `run_all.py` | Exportar, dashboard, sync |
| **Leitura** | `profile.py`, `media.py` | Perfil, listar mídia |

## Localização

```
C:\Users\renat\skills\instagram\
├── SKILL.md
├── scripts/
│   ├── requirements.txt
│   │  # ── CORE ──
│   ├── config.py                     # Paths, constantes, specs de mídia
│   ├── db.py                         # SQLite: accounts, posts, comments, insights
│   ├── auth.py                       # OAuth 2.0, token storage/refresh
│   ├── api_client.py                 # Instagram Graph API wrapper + retry
│   ├── governance.py                 # Rate limits, audit log, confirmações
│   │  # ── FEATURES ──
│   ├── account_setup.py              # Detecção conta, migração, verificação
│   ├── publish.py                    # Publicar + upload local via Imgur
│   ├── schedule.py                   # Orquestrador: approved → published
│   ├── comments.py                   # Ler/responder/deletar comentários
│   ├── messages.py                   # DMs (enviar/receber/listar)
│   ├── insights.py                   # Fetch + store métricas
│   ├── hashtags.py                   # Pesquisa + tracking
│   ├── profile.py                    # Ver/atualizar perfil
│   ├── media.py                      # Listar mídia, detalhes
│   │  # ── INTELIGÊNCIA ──
│   ├── templates.py                  # Templates de caption/hashtags
│   ├── analyze.py                    # Melhores horários, top posts
│   │  # ── INFRA ──
│   ├── export.py                     # Exportar JSON/CSV/JSONL
│   ├── serve_api.py                  # FastAPI + dashboard
│   └── run_all.py                    # Sync completo
├── references/
│   ├── graph_api.md                  # Endpoints e parâmetros
│   ├── permissions.md                # Scopes OAuth por feature
│   ├── rate_limits.md                # Limites 2025
│   ├── account_types.md              # Business vs Creator
│   ├── publishing_guide.md           # Specs de mídia
│   ├── setup_walkthrough.md          # Guia Meta App
│   └── schema.md                     # ER diagram
├── static/
│   └── dashboard.html                # Dashboard Chart.js
└── data/
    

## Instalação (Uma Vez)

```bash
pip install -r C:\Users\renat\skills\instagram\scripts\requirements.txt
```

## Configuração Inicial

```bash

## 1. Verificar Tipo De Conta Instagram

python C:\Users\renat\skills\instagram\scripts\account_setup.py --check

## 2. Configurar Oauth (Abre Browser Para Autorização)

python C:\Users\renat\skills\instagram\scripts\auth.py --setup

## 3. Verificar Se Está Tudo Funcionando

python C:\Users\renat\skills\instagram\scripts\profile.py --view
```

Se a conta for pessoal, o script `account_setup.py --guide` dá instruções de migração
para Business ou Creator.

## Foto (Aceita Arquivo Local — Faz Upload Automático Via Imgur)

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image caminho/foto.jpg --caption "Texto do post"

## Vídeo

python C:\Users\renat\skills\instagram\scripts\publish.py --type video --video caminho/video.mp4 --caption "Meu vídeo"

## Reel

python C:\Users\renat\skills\instagram\scripts\publish.py --type reel --video caminho/reel.mp4 --caption "Novo reel!"

## Story

python C:\Users\renat\skills\instagram\scripts\publish.py --type story --image caminho/story.jpg

## Carrossel (2-10 Imagens)

python C:\Users\renat\skills\instagram\scripts\publish.py --type carousel --images img1.jpg img2.jpg img3.jpg --caption "Carrossel"

## Criar Como Rascunho (Não Publica Imediatamente)

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto" --draft

## Aprovar Rascunho Para Publicação

python C:\Users\renat\skills\instagram\scripts\publish.py --approve --id 5
```

## Agendar Publicação Futura

python C:\Users\renat\skills\instagram\scripts\schedule.py --type photo --image foto.jpg --caption "Post agendado" --at "2026-03-01T10:00"

## Listar Posts Agendados

python C:\Users\renat\skills\instagram\scripts\schedule.py --list

## Processar Posts Prontos Para Publicar

python C:\Users\renat\skills\instagram\scripts\schedule.py --process

## Cancelar Agendamento

python C:\Users\renat\skills\instagram\scripts\schedule.py --cancel --id 5
```

## Listar Comentários De Um Post

python C:\Users\renat\skills\instagram\scripts\comments.py --list --media-id 12345

## Responder A Um Comentário

python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id 67890 --text "Obrigado!"

## Deletar Comentário

python C:\Users\renat\skills\instagram\scripts\comments.py --delete --comment-id 67890

## Ver Menções

python C:\Users\renat\skills\instagram\scripts\comments.py --mentions

## Comentários Não Respondidos

python C:\Users\renat\skills\instagram\scripts\comments.py --unreplied
```

## Enviar Dm

python C:\Users\renat\skills\instagram\scripts\messages.py --send --user-id 12345 --text "Olá!"

## Listar Conversas

python C:\Users\renat\skills\instagram\scripts\messages.py --conversations

## Ver Mensagens De Uma Conversa

python C:\Users\renat\skills\instagram\scripts\messages.py --thread --conversation-id 12345
```

## Métricas De Um Post Específico

python C:\Users\renat\skills\instagram\scripts\insights.py --media --media-id 12345

## Métricas Da Conta (Últimos 7 Dias)

python C:\Users\renat\skills\instagram\scripts\insights.py --user --period day --since 7

## Buscar E Salvar Insights De Todos Os Posts Recentes

python C:\Users\renat\skills\instagram\scripts\insights.py --fetch-all --limit 20
```

## Melhores Horários Para Postar (Baseado Nos Seus Dados)

python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times

## Top Posts Por Engajamento

python C:\Users\renat\skills\instagram\scripts\analyze.py --top-posts --limit 10

## Tendências De Crescimento

python C:\Users\renat\skills\instagram\scripts\analyze.py --growth --period 30
```

## Buscar Posts Recentes Com Uma Hashtag

python C:\Users\renat\skills\instagram\scripts\hashtags.py --search "artificialintelligence" --limit 25

## Top Posts De Uma Hashtag

python C:\Users\renat\skills\instagram\scripts\hashtags.py --top "tecnologia"

## Info Da Hashtag (Contagem De Posts)

python C:\Users\renat\skills\instagram\scripts\hashtags.py --info "marketing"
```

## Criar Template

python C:\Users\renat\skills\instagram\scripts\templates.py --create --name "promo" --caption "Nova promoção: {produto}! {desconto}% OFF" --hashtags "#oferta,#desconto,#promoção"

## Listar Templates

python C:\Users\renat\skills\instagram\scripts\templates.py --list

## Usar Template Em Um Post

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --template promo --vars produto="Tênis" desconto=30
```

## Ver Perfil

python C:\Users\renat\skills\instagram\scripts\profile.py --view

## Listar Posts Recentes

python C:\Users\renat\skills\instagram\scripts\media.py --list --limit 10

## Detalhes De Um Post

python C:\Users\renat\skills\instagram\scripts\media.py --details --media-id 12345
```

## Exportar Analytics Para Csv

python C:\Users\renat\skills\instagram\scripts\export.py --type insights --format csv

## Exportar Comentários

python C:\Users\renat\skills\instagram\scripts\export.py --type comments --format json

## Exportar Tudo

python C:\Users\renat\skills\instagram\scripts\export.py --type all --format csv

## Iniciar Dashboard Web

python C:\Users\renat\skills\instagram\scripts\serve_api.py

## Acesse: Http://Localhost:8000/Dashboard

```

## Status Da Autenticação

python C:\Users\renat\skills\instagram\scripts\auth.py --status

## Sync Completo (Busca Perfil + Mídia + Insights + Comentários)

python C:\Users\renat\skills\instagram\scripts\run_all.py

## Sync Parcial

python C:\Users\renat\skills\instagram\scripts\run_all.py --only media insights
```

## Rate Limits

A skill rastreia automaticamente os rate limits da API:
- **200 requests/hora** por conta
- **25 publicações/dia** por conta
- **30 hashtags únicas/semana** por conta
- **200 DMs/hora** por conta

Quando em 90% do limite, a skill emite warnings. Se exceder, bloqueia a ação e informa
quanto tempo esperar.

## Confirmações

Ações que afetam conteúdo público requerem confirmação:
- **PUBLISH**: Publicar foto/vídeo/reel/story/carrossel
- **DELETE**: Deletar comentário
- **MESSAGE**: Enviar DM
- **ENGAGE**: Responder comentário, ocultar comentário

O script retorna os detalhes da ação e pede confirmação antes de executar.

## Audit Log

Todas as ações que modificam dados são logadas no banco SQLite (`action_log` table):
- Timestamp, ação, parâmetros, resultado, status de confirmação
- Consultar via: `python C:\Users\renat\skills\instagram\scripts\db.py`

## Token Auto-Refresh

O token OAuth (60 dias) é renovado automaticamente quando está a 7 dias de expirar.
Sem intervenção manual necessária.

## Limitações Da Api

Coisas que a Instagram Graph API **não permite**:
- Deletar posts já publicados
- Editar captions após publicar
- Aplicar filtros via API
- Postar de contas pessoais (só Business/Creator)
- DMs fora da janela de 24hrs (usuário precisa ter interagido primeiro)
- Fotos em formato diferente de JPEG (auto-conversão feita pelos scripts)

## "Quero Publicar Uma Foto"

```bash
python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto"
```

## "Me Mostra Meus Analytics"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py --only insights
python C:\Users\renat\skills\instagram\scripts\analyze.py --summary
```

## "Qual O Melhor Horário Para Postar?"

```bash
python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times
```

## "Responde Esse Comentário"

```bash
python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id ID --text "Resposta"
```

## "Sincroniza Tudo"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py
```

## "Abre O Dashboard"

```bash
python C:\Users\renat\skills\instagram\scripts\serve_api.py
```

## Referências

Consultar quando precisar de detalhes:
- `references/graph_api.md` — Endpoints, parâmetros e responses da API
- `references/publishing_guide.md` — Specs de mídia (dimensões, formatos, tamanhos)
- `references/rate_limits.md` — Rate limits detalhados e estratégias
- `references/account_types.md` — Diferenças Business vs Creator, migração
- `references/permissions.md` — Scopes OAuth necessários por feature
- `references/setup_walkthrough.md` — Guia passo-a-passo de setup do Meta App
- `references/schema.md` — Schema do banco SQLite (ER diagram, campos, índices, queries)

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `social-orchestrator` - Complementary skill for enhanced analysis
- `telegram` - Complementary skill for enhanced analysis
- `whatsapp-cloud-api` - Complementary skill for enhanced analysis

---

## Reference: Account_Types

# Tipos de Conta Instagram — Business vs Creator

## Comparação

| Feature | Personal | Creator | Business |
|---------|----------|---------|----------|
| Graph API | Sem acesso | Acesso completo | Acesso completo |
| Publicar via API | Proibido | Sim | Sim |
| Insights de mídia | Proibido | Sim | Sim |
| Insights de conta | Proibido | Sim | Sim |
| DMs via API | Proibido | Sim | Sim |
| Comentários via API | Proibido | Sim | Sim |
| Agendamento nativo API | Proibido | Limitado | Sim |
| Hashtag search | Proibido | Sim | Sim |
| Shopping/Catalog | Proibido | Proibido | Sim |
| Facebook Page link | Não necessário | Opcional | Obrigatório |

## Quando Usar Cada Tipo

### Business
Recomendado para:
- Empresas, lojas, marcas
- Precisa de agendamento nativo via API
- Quer usar Shopping/Catalog
- Já tem Facebook Page da empresa

### Creator
Recomendado para:
- Influenciadores, artistas, criadores de conteúdo
- Indivíduos que querem analytics
- Não quer vincular a uma Facebook Page obrigatoriamente

### Personal
**Não suportada pela Graph API.** Migração necessária.

## Migração: Personal → Business/Creator

### Pré-requisitos
1. Conta Instagram ativa
2. Para Business: Facebook Page vinculada (pode criar uma nova)
3. Para Creator: não precisa de Page (opcional)

### Passo a Passo (no app Instagram)

#### Para Business:
1. Abrir Instagram → Configurações
2. Conta → Mudar tipo de conta profissional
3. Escolher "Empresa"
4. Selecionar categoria do negócio
5. Vincular a uma Facebook Page (ou criar nova)
6. Confirmar

#### Para Creator:
1. Abrir Instagram → Configurações
2. Conta → Mudar tipo de conta profissional
3. Escolher "Criador de conteúdo"
4. Selecionar categoria
5. Confirmar

### O que acontece na migração
- **Preservado:** Posts, followers, following, DMs, bio
- **Adicionado:** Insights, botões de contato, categoria
- **Mudança:** Perfil público (se era privado, será convertido)

### Reversão
É possível voltar para Personal, mas:
- Perde acesso à API imediatamente
- Perde histórico de insights
- Posts e followers permanecem

## Migração: Business ↔ Creator

Também é possível alternar entre Business e Creator:
1. Configurações → Conta → Mudar tipo de conta
2. Escolher o outro tipo profissional
3. Histórico de insights pode ser reiniciado

## Detecção Automática (account_setup.py)

O script `account_setup.py --check` detecta o tipo via:
```
GET /me?fields=account_type
```

Possíveis valores: `BUSINESS`, `MEDIA_CREATOR`, `PERSONAL`

Se `PERSONAL`, guia o usuário pela migração com `--guide`.

## Vinculação com Facebook Page

### Por que é necessária (Business)
- A Graph API acessa o Instagram via Facebook Pages API
- O token OAuth autoriza a Page, que dá acesso à conta IG vinculada
- Sem Page vinculada → sem acesso API

### Fluxo de descoberta (auth.py)
```
1. GET /me/accounts → lista Facebook Pages do usuário
2. Para cada Page: GET /{page-id}?fields=instagram_business_account
3. Retorna o IG user ID vinculado
```

### Conta Creator sem Page
Contas Creator podem funcionar sem Page, mas o fluxo de autenticação
ainda precisa de pelo menos uma Page para o OAuth funcionar. Recomendação:
criar uma Page básica (não precisa de conteúdo) apenas para a vinculação.

---

## Reference: Graph_Api

# Instagram Graph API — Referência de Endpoints

Base URL: `https://graph.instagram.com/v21.0`

## Índice

1. [Perfil do Usuário](#perfil-do-usuário)
2. [Mídia](#mídia)
3. [Publicação (2-Step)](#publicação)
4. [Comentários](#comentários)
5. [Insights de Mídia](#insights-de-mídia)
6. [Insights do Usuário](#insights-do-usuário)
7. [Hashtags](#hashtags)
8. [Mensagens (DMs)](#mensagens)
9. [Menções](#menções)
10. [Erros Comuns](#erros-comuns)

---

## Perfil do Usuário

### GET /{user-id}

Retorna informações do perfil.

**Campos disponíveis:**
- `id`, `username`, `name`, `account_type`
- `biography`, `followers_count`, `follows_count`, `media_count`
- `profile_picture_url`, `website`

**Exemplo:**
```
GET /me?fields=id,username,name,account_type,biography,followers_count,follows_count,media_count&access_token=TOKEN
```

**Resposta:**
```json
{
  "id": "17841400000000",
  "username": "minha_conta",
  "name": "Meu Nome",
  "account_type": "BUSINESS",
  "biography": "Bio aqui",
  "followers_count": 1500,
  "follows_count": 200,
  "media_count": 45
}
```

---

## Mídia

### GET /{user-id}/media

Lista mídia publicada pelo usuário.

**Parâmetros:**
- `fields`: id, caption, media_type, media_url, permalink, timestamp, thumbnail_url
- `limit`: 1-100 (default 25)
- `after`/`before`: cursor de paginação

**Media types:** IMAGE, VIDEO, CAROUSEL_ALBUM

### GET /{media-id}

Detalhes de uma mídia específica.

**Campos adicionais:** `like_count`, `comments_count`, `is_shared_to_feed`

### GET /{media-id}/children

Para CAROUSEL_ALBUM — retorna itens do carrossel.

---

## Publicação

### Processo de 2 Etapas

**Etapa 1 — Criar Container:**

```
POST /{user-id}/media
```

| Tipo | Parâmetros obrigatórios |
|------|------------------------|
| Foto | `image_url`, `caption` (opcional) |
| Vídeo | `video_url`, `caption`, `media_type=VIDEO` |
| Reel | `video_url`, `caption`, `media_type=REELS` |
| Story (foto) | `image_url`, `media_type=STORIES` |
| Story (vídeo) | `video_url`, `media_type=STORIES` |
| Carousel item | `image_url` ou `video_url`, `is_carousel_item=true` |
| Carousel container | `media_type=CAROUSEL`, `children=[id1,id2,...]`, `caption` |

**Resposta:** `{"id": "container_id"}`

**Etapa 1.5 — Verificar Status (vídeos):**

```
GET /{container-id}?fields=status_code
```

Status: `IN_PROGRESS`, `FINISHED`, `ERROR`

Aguardar até `FINISHED` antes de publicar. Poll a cada 5-10s.

**Etapa 2 — Publicar:**

```
POST /{user-id}/media_publish
  creation_id={container_id}
```

**Resposta:** `{"id": "ig_media_id"}`

### Agendamento via API

```
POST /{user-id}/media
  image_url=URL
  caption=texto
  published=false
  scheduled_publish_time=UNIX_TIMESTAMP
```

- Timestamp deve ser entre 10 min e 75 dias no futuro
- Apenas contas Business (Creator não suporta scheduling nativo)

---

## Comentários

### GET /{media-id}/comments

Lista comentários de uma mídia.

**Campos:** `id`, `text`, `username`, `timestamp`, `like_count`
**Parâmetros:** `limit` (max 50), paginação com cursors

### POST /{media-id}/comments

Responder no post (novo comentário de primeiro nível).

**Body:** `message=texto`

### POST /{comment-id}/replies

Responder a um comentário específico.

**Body:** `message=texto`

### DELETE /{comment-id}

Deleta um comentário (apenas comentários na sua mídia ou seus próprios).

### POST /{comment-id}

Ocultar/mostrar comentário.

**Body:** `hide=true` ou `hide=false`

---

## Insights de Mídia

### GET /{media-id}/insights

**Métricas para IMAGE/CAROUSEL:**
- `impressions` — Vezes que a mídia foi exibida
- `reach` — Contas únicas que viram
- `engagement` — Likes + comments + saves
- `saved` — Vezes que foi salva

**Métricas adicionais para VIDEO/REELS:**
- `video_views` — Visualizações do vídeo
- `plays` — Vezes que o reel foi reproduzido

**Parâmetros:**
```
metric=impressions,reach,engagement,saved
```

**Resposta:**
```json
{
  "data": [
    {
      "name": "impressions",
      "period": "lifetime",
      "values": [{"value": 250}],
      "title": "Impressions"
    }
  ]
}
```

---

## Insights do Usuário

### GET /{user-id}/insights

Métricas agregadas da conta.

**Métricas por período `day`:**
- `impressions` — Total de impressões
- `reach` — Contas únicas alcançadas
- `follower_count` — Total de seguidores (só `day`)
- `profile_views` — Visualizações do perfil

**Métricas por período `week` / `days_28`:**
- `impressions`, `reach`

**Parâmetros:**
```
metric=impressions,reach,follower_count,profile_views
period=day
since=UNIX_TIMESTAMP
until=UNIX_TIMESTAMP
```

**Limite:** máximo 30 dias por request. `since` e `until` devem ser alinhados ao fuso.

---

## Hashtags

### GET /ig_hashtag_search

Busca o ID de uma hashtag.

**Parâmetros:**
- `user_id`: ID da conta
- `q`: nome da hashtag (sem #)

**Resposta:** `{"data": [{"id": "17843853986012965"}]}`

**Limite:** 30 hashtags únicas por conta por semana (janela de 7 dias rolling).

### GET /{hashtag-id}/recent_media

Posts recentes com a hashtag.

**Campos:** `id`, `caption`, `media_type`, `media_url`, `permalink`, `timestamp`
**Parâmetros:** `user_id` (obrigatório), `fields`, `limit`

### GET /{hashtag-id}/top_media

Top posts (ordenados por popularidade).

Mesmos campos e parâmetros que `recent_media`.

---

## Mensagens

### GET /{user-id}/conversations

Lista conversas do Instagram Messaging.

**Campos:** `id`, `participants`, `updated_time`
**Requer:** scope `instagram_manage_messages`

### GET /{conversation-id}/messages

Mensagens de uma conversa.

**Campos:** `id`, `message`, `from`, `created_time`

### POST /me/messages

Enviar mensagem.

**Body:**
```json
{
  "recipient": {"id": "user_ig_scoped_id"},
  "message": {"text": "Olá!"}
}
```

**Restrições:**
- Apenas responder a conversas existentes (dentro de janela de 24hrs)
- Ou usar Message Templates aprovados (requer aprovação Meta)

---

## Menções

### GET /{user-id}/tags

Mídias em que o usuário foi mencionado/tagueado.

**Campos:** `id`, `caption`, `media_type`, `media_url`, `permalink`, `timestamp`, `username`

---

## Erros Comuns

| Código | Subcódigo | Significado | Ação |
|--------|-----------|-------------|------|
| 4 | - | Rate limit atingido | Backoff 1 hora |
| 10 | - | Permissão negada | Verificar scopes |
| 17 | - | Rate limit da conta | Esperar período indicado |
| 24 | - | Webhook inválido | Verificar URL/certificado |
| 100 | - | Parâmetro inválido | Verificar request |
| 190 | - | Token expirado/inválido | Refresh token |
| 200 | - | Permissão insuficiente | Verificar app review |
| 368 | - | Conteúdo bloqueado | Política de conteúdo |

**Formato de erro padrão:**
```json
{
  "error": {
    "message": "Descrição do erro",
    "type": "OAuthException",
    "code": 190,
    "fbtrace_id": "AbCdEfG"
  }
}
```

---

## Reference: Permissions

# Permissões OAuth — Scopes por Feature

## Scopes Necessários

| Scope | Descrição | Features |
|-------|-----------|----------|
| `instagram_basic` | Ler perfil e mídia | Perfil, listar posts, mídia |
| `instagram_content_publish` | Publicar conteúdo | Publicar fotos, vídeos, reels, stories, carrossel |
| `instagram_manage_comments` | Gerenciar comentários | Ler, responder, deletar, ocultar comentários |
| `instagram_manage_insights` | Ler insights | Insights de mídia e conta |
| `instagram_manage_messages` | Gerenciar DMs | Enviar, receber, listar mensagens |
| `pages_show_list` | Listar Facebook Pages | Necessário para descobrir a conta IG vinculada |
| `pages_read_engagement` | Ler engajamento da Page | Necessário para algumas métricas |

## Mapeamento Feature → Scopes

### Leitura (Básico)
```
Ver perfil            → instagram_basic, pages_show_list
Listar mídia          → instagram_basic
Ver comentários       → instagram_basic
```

### Publicação
```
Publicar foto/vídeo   → instagram_content_publish, instagram_basic
Publicar reel         → instagram_content_publish, instagram_basic
Publicar story        → instagram_content_publish, instagram_basic
Publicar carrossel    → instagram_content_publish, instagram_basic
Agendar post          → instagram_content_publish, instagram_basic
```

### Comunidade
```
Responder comentário  → instagram_manage_comments
Deletar comentário    → instagram_manage_comments
Ocultar comentário    → instagram_manage_comments
Ver menções           → instagram_basic
```

### Mensagens
```
Listar conversas      → instagram_manage_messages
Ler mensagens         → instagram_manage_messages
Enviar mensagem       → instagram_manage_messages
```

### Analytics
```
Insights de mídia     → instagram_manage_insights
Insights da conta     → instagram_manage_insights
Pesquisa de hashtag   → instagram_basic
```

## Processo de Aprovação

### Desenvolvimento (Modo de Teste)
- Até 5 testers configurados no Meta App
- Todos os scopes funcionam sem aprovação
- Token de teste funciona normalmente

### Produção (App Review)
Para uso além dos testers, cada scope precisa de aprovação:

1. **instagram_basic** — Aprovação simples (uso básico)
2. **instagram_content_publish** — Requer justificativa de uso
3. **instagram_manage_comments** — Requer justificativa
4. **instagram_manage_insights** — Requer justificativa
5. **instagram_manage_messages** — Aprovação mais rigorosa (privacidade)

### Dicas para App Review
- Gravar screencast mostrando o uso
- Explicar claramente por que cada permissão é necessária
- Demonstrar que os dados são usados de forma responsável
- Para uso pessoal (1 conta), modo de teste é suficiente

## Checklist de Scopes para auth.py

O arquivo `config.py` define os scopes padrão:
```python
OAUTH_SCOPES = [
    "instagram_basic",
    "instagram_content_publish",
    "instagram_manage_comments",
    "instagram_manage_insights",
    "instagram_manage_messages",
    "pages_show_list",
    "pages_read_engagement",
]
```

Se não precisar de todas as features, pode reduzir os scopes durante o setup.

---

## Reference: Publishing_Guide

# Guia de Publicação — Specs de Mídia e Fluxos

## Specs de Mídia

### Foto (IMAGE)
| Propriedade | Requisito |
|-------------|-----------|
| Formato | JPEG (obrigatório — PNG/WebP são convertidos automaticamente pelo publish.py via Pillow) |
| Resolução mínima | 320 x 320 px |
| Resolução máxima | 1080 x 1350 px (recomendado) |
| Aspect ratio | 4:5 (portrait) a 1.91:1 (landscape) |
| Tamanho máximo | 8 MB |
| Color space | sRGB |

### Vídeo (VIDEO)
| Propriedade | Requisito |
|-------------|-----------|
| Formato | MP4 (H.264 codec) |
| Resolução mínima | 640 x 640 px |
| Resolução máxima | 1920 x 1080 px |
| Duração | 3 segundos a 60 minutos |
| Tamanho máximo | 250 MB (recomendado < 100 MB) |
| Frame rate | 23-60 fps |
| Audio | AAC, 48kHz sample rate |

### Reel (REELS)
| Propriedade | Requisito |
|-------------|-----------|
| Formato | MP4 (H.264 codec) |
| Aspect ratio | 9:16 (vertical, obrigatório) |
| Resolução recomendada | 1080 x 1920 px |
| Duração | 3 segundos a 15 minutos |
| Tamanho máximo | 250 MB |
| Audio | Obrigatório (pode ser mudo, mas track precisa existir) |

### Story (STORIES)
| Propriedade | Requisito |
|-------------|-----------|
| Formato foto | JPEG |
| Formato vídeo | MP4 |
| Aspect ratio | 9:16 (1080 x 1920 px recomendado) |
| Duração vídeo | Até 60 segundos |
| Desaparece | Após 24 horas |

### Carrossel (CAROUSEL_ALBUM)
| Propriedade | Requisito |
|-------------|-----------|
| Itens | 2 a 10 imagens/vídeos |
| Tipos permitidos | Mix de fotos e vídeos |
| Cada item segue specs | De IMAGE ou VIDEO acima |
| Aspect ratio | Todos os itens devem ter o mesmo aspect ratio |

## Fluxo de Publicação (2-Step)

### Fluxo Completo para Foto

```
1. Upload local → Imgur (se path local)
   POST https://api.imgur.com/3/image
   → Retorna URL pública

2. Criar Container
   POST /{user-id}/media
     image_url=<URL_publica>
     caption=<texto>
   → Retorna container_id

3. Publicar Container
   POST /{user-id}/media_publish
     creation_id=<container_id>
   → Retorna ig_media_id + permalink
```

### Fluxo Completo para Vídeo/Reel

```
1. Upload local → Imgur (se path local)

2. Criar Container
   POST /{user-id}/media
     video_url=<URL_publica>
     caption=<texto>
     media_type=VIDEO (ou REELS)
   → Retorna container_id

3. Aguardar Processamento (POLL)
   GET /{container_id}?fields=status_code
   Repetir a cada 10s até status = FINISHED
   (Timeout: 5 minutos)

4. Publicar Container
   POST /{user-id}/media_publish
     creation_id=<container_id>
   → Retorna ig_media_id
```

### Fluxo Completo para Carrossel

```
1. Para cada item (2-10):
   POST /{user-id}/media
     image_url=<URL> (ou video_url)
     is_carousel_item=true
   → Retorna item_container_id

2. Criar Container do Carrossel
   POST /{user-id}/media
     media_type=CAROUSEL
     children=[item1_id, item2_id, ...]
     caption=<texto>
   → Retorna carousel_container_id

3. Publicar
   POST /{user-id}/media_publish
     creation_id=<carousel_container_id>
   → Retorna ig_media_id
```

## Pipeline de Status (publish.py)

```
draft → approved → scheduled → container_created → published
                                      ↓
                                    failed
```

| Status | Significado | Próxima ação |
|--------|-------------|--------------|
| `draft` | Rascunho, não será publicado automaticamente | `--approve --id X` |
| `approved` | Aprovado para publicação | `schedule.py --process` |
| `scheduled` | Agendado para data futura | Aguardar horário |
| `container_created` | Container criado na API, aguardando publish | Recovery automático |
| `published` | Publicado com sucesso | Concluído |
| `failed` | Erro na publicação | Verificar error_msg, retry possível |

## Recovery de Crash

Se o processo crashar entre `container_created` e `published`:
1. O `schedule.py --process` detecta posts com status `container_created`
2. Verifica se o container ainda é válido via API
3. Se válido → publica
4. Se inválido → recria container e republica

## Upload Local via Imgur

O `publish.py` detecta se o caminho é local (não começa com http):

1. Lê o arquivo local
2. Converte para JPEG se necessário (via Pillow)
3. Faz upload anônimo para Imgur (POST https://api.imgur.com/3/image)
4. Usa a URL retornada como `image_url` na Graph API

**Configuração:** `IMGUR_CLIENT_ID` em config.py ou variável de ambiente.

## Captions e Hashtags

### Limites
- Caption: máximo 2.200 caracteres
- Hashtags: máximo 30 por post
- Menções (@): sem limite oficial

### Templates (via templates.py)
```python
caption_template = "Nova promoção: {produto}! {desconto}% OFF"
# Com variáveis: produto="Tênis", desconto=30
# Resultado: "Nova promoção: Tênis! 30% OFF"
```

### Hashtags em Templates
Hashtags são armazenadas como JSON array e adicionadas ao final da caption:
```
Caption renderizada + "\n\n" + " ".join(hashtags)
```

---

## Reference: Rate_Limits

# Rate Limits — Instagram Graph API

## Limites Principais

| Recurso | Limite | Janela | Notas |
|---------|--------|--------|-------|
| API calls gerais | 200 requests | 1 hora | Por usuário/token |
| Publicação de conteúdo | 25 posts | 24 horas | Por conta IG |
| Pesquisa de hashtags | 30 hashtags únicas | 7 dias (rolling) | Por conta IG |
| DMs (envio) | 200 mensagens | 1 hora | Human Agent messaging |
| Stories | Sem limite oficial | — | Mas recomenda-se < 25/dia |

## Como a Skill Rastreia

### Sliding Window (SQLite)
O `governance.py` usa a tabela `action_log` para contar ações dentro da janela:

```sql
-- Requests na última hora
SELECT COUNT(*) FROM action_log
WHERE account_id = ? AND created_at >= datetime('now', '-1 hour')

-- Publicações nas últimas 24h
SELECT COUNT(*) FROM action_log
WHERE account_id = ? AND action IN ('publish_photo','publish_video',...)
AND created_at >= datetime('now', '-24 hours')

-- Hashtags únicas na última semana
SELECT COUNT(DISTINCT hashtag) FROM hashtag_searches
WHERE account_id = ? AND searched_at >= datetime('now', '-7 days')
```

### Thresholds de Warning
- **80%**: Info log — "Approaching rate limit"
- **90%**: Warning — "Near rate limit, consider slowing down"
- **100%**: Block — Retorna erro com tempo de espera estimado

## Respostas de Rate Limit da API

### Erro code 4 (Application-level)
```json
{
  "error": {
    "message": "Application request limit reached",
    "type": "OAuthException",
    "code": 4
  }
}
```
**Ação:** Backoff de 1 hora. O `api_client.py` detecta e faz retry automático.

### Erro code 17 (User-level)
```json
{
  "error": {
    "message": "(#17) User request limit reached",
    "type": "OAuthException",
    "code": 17
  }
}
```
**Ação:** Backoff de 1 hora por conta.

### HTTP 429 (Too Many Requests)
Alguns endpoints retornam HTTP 429 em vez de erro JSON.
**Ação:** Respeitar header `Retry-After` se presente, senão backoff padrão.

## Estratégias de Backoff

### api_client.py — Exponential Backoff
```
Tentativa 1: espera 2s
Tentativa 2: espera 4s
Tentativa 3: espera 8s
Após 3 falhas: desiste e reporta
```

### Rate limit específico
```
Code 4/17: espera 3600s (1 hora)
Code 190 (token): fail imediato (refresh necessário)
Code 10/200 (permission): fail imediato
```

## Otimizações

### Batch Requests
Para reduzir contagem de requests, usar fields parameter para buscar múltiplos campos em uma chamada:
```
GET /me?fields=id,username,followers_count,media{id,caption,media_type,permalink}
```

### Caching Local
O `db.py` persiste dados em SQLite — evita refazer chamadas para dados recentes.

### Sync Inteligente
O `run_all.py` processa em ordem de prioridade:
1. Profile (1 request)
2. Media (1 request, batch)
3. Insights (N requests, 1 por post)
4. Comments (N requests, 1 por post)

Use `--limit` para controlar quantos posts processar por sync.

## Monitoramento

```bash
# Ver rate limit restante (estimativa baseada em logs)
python scripts/auth.py --status

# Ver ações recentes no audit log
python scripts/export.py --type actions --format json
```

---

## Reference: Schema

# Schema do Banco SQLite — instagram.db

Localização: `C:\Users\renat\skills\instagram\data\instagram.db`
Modo: WAL (Write-Ahead Logging) com foreign keys habilitadas.

## Diagrama ER

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   accounts   │       │    posts     │       │  templates   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │──┐    │ id (PK)      │    ┌──│ id (PK)      │
│ ig_user_id   │  │    │ account_id(FK)│◄───┤  │ name (UNIQUE)│
│ username     │  │    │ media_type   │    │  │ caption_tpl  │
│ account_type │  │    │ media_url    │    │  │ hashtag_set  │
│ access_token │  │    │ local_path   │    │  │ default_time │
│ token_exp    │  │    │ caption      │    │  │ created_at   │
│ fb_page_id   │  │    │ hashtags     │    │  └──────────────┘
│ app_id       │  │    │ template_id(FK)│◄──┘
│ app_secret   │  │    │ status       │
│ is_active    │  │    │ scheduled_at │
│ created_at   │  │    │ published_at │
└──────────────┘  │    │ ig_media_id  │
                  │    │ ig_container │
                  │    │ permalink    │
                  │    │ error_msg    │
                  │    │ created_at   │
                  │    └──────────────┘
                  │
                  │    ┌──────────────┐
                  ├───►│  comments    │
                  │    ├──────────────┤
                  │    │ id (PK)      │
                  │    │ account_id(FK)│
                  │    │ ig_comment_id│
                  │    │ ig_media_id  │
                  │    │ username     │
                  │    │ text         │
                  │    │ timestamp    │
                  │    │ replied      │
                  │    │ reply_text   │
                  │    │ hidden       │
                  │    └──────────────┘
                  │
                  │    ┌──────────────┐
                  ├───►│  insights    │
                  │    ├──────────────┤
                  │    │ id (PK)      │
                  │    │ account_id(FK)│
                  │    │ ig_media_id  │
                  │    │ metric_name  │
                  │    │ metric_value │
                  │    │ period       │
                  │    │ fetched_at   │
                  │    │ raw_json     │
                  │    └──────────────┘
                  │
                  │    ┌──────────────────┐
                  ├───►│  user_insights   │
                  │    ├──────────────────┤
                  │    │ id (PK)          │
                  │    │ account_id (FK)  │
                  │    │ metric_name      │
                  │    │ metric_value     │
                  │    │ period           │
                  │    │ end_time         │
                  │    │ fetched_at       │
                  │    └──────────────────┘
                  │
                  │    ┌──────────────────┐
                  ├───►│ hashtag_searches │
                  │    ├──────────────────┤
                  │    │ id (PK)          │
                  │    │ account_id (FK)  │
                  │    │ hashtag          │
                  │    │ ig_hashtag_id    │
                  │    │ searched_at      │
                  │    └──────────────────┘
                  │
                  │    ┌──────────────┐
                  └───►│ action_log   │
                       ├──────────────┤
                       │ id (PK)      │
                       │ account_id   │
                       │ action       │
                       │ params (JSON)│
                       │ result (JSON)│
                       │ confirmed    │
                       │ rate_remain  │
                       │ created_at   │
                       └──────────────┘
```

## Tabelas Detalhadas

### accounts
Armazena contas Instagram configuradas. Multi-conta pronta desde o dia 1.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| ig_user_id | TEXT | UNIQUE NOT NULL | ID do usuário IG na Graph API |
| username | TEXT | | @username |
| account_type | TEXT | | BUSINESS, MEDIA_CREATOR |
| access_token | TEXT | NOT NULL | Token longo (60 dias) |
| token_expires_at | TEXT | | ISO 8601 datetime |
| facebook_page_id | TEXT | | ID da Facebook Page vinculada |
| app_id | TEXT | | Meta App ID |
| app_secret | TEXT | | Meta App Secret |
| is_active | INTEGER | DEFAULT 1 | Conta ativa (1) ou desativada (0) |
| created_at | TEXT | DEFAULT now | Timestamp de criação |

### posts
Pipeline de conteúdo com status machine.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | FK → accounts | Conta associada |
| media_type | TEXT | | PHOTO, VIDEO, CAROUSEL, REEL, STORY |
| media_url | TEXT | | URL pública (após upload Imgur) |
| local_path | TEXT | | Caminho local original |
| caption | TEXT | | Texto do post |
| hashtags | TEXT | | JSON array de hashtags |
| template_id | INTEGER | FK → templates | Template usado (opcional) |
| status | TEXT | DEFAULT 'draft' | draft, approved, scheduled, container_created, published, failed |
| scheduled_at | TEXT | | Datetime agendado (ISO 8601) |
| published_at | TEXT | | Datetime efetivo de publicação |
| ig_media_id | TEXT | | ID retornado pela API após publicar |
| ig_container_id | TEXT | | Container ID para recovery do 2-step |
| permalink | TEXT | | URL do post no Instagram |
| error_msg | TEXT | | Mensagem de erro se failed |
| created_at | TEXT | DEFAULT now | Timestamp de criação |

**Índices:** `idx_posts_status`, `idx_posts_account`, `idx_posts_ig_media`

### comments
Comentários dos posts, com tracking de respostas.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | FK → accounts | Conta associada |
| ig_comment_id | TEXT | UNIQUE | ID do comentário na Graph API |
| ig_media_id | TEXT | | ID da mídia relacionada |
| username | TEXT | | @username do autor |
| text | TEXT | | Conteúdo do comentário |
| timestamp | TEXT | | Datetime ISO 8601 |
| replied | INTEGER | DEFAULT 0 | Se já foi respondido (0/1) |
| reply_text | TEXT | | Texto da resposta dada |
| hidden | INTEGER | DEFAULT 0 | Se está oculto (0/1) |

### insights
Métricas individuais de cada mídia.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | FK → accounts | Conta associada |
| ig_media_id | TEXT | | ID da mídia |
| metric_name | TEXT | | impressions, reach, engagement, saved, video_views |
| metric_value | REAL | | Valor numérico da métrica |
| period | TEXT | | lifetime, day, week, days_28 |
| fetched_at | TEXT | DEFAULT now | Quando foi buscado |
| raw_json | TEXT | | Resposta completa da API (preservada) |

**Índice:** `idx_insights_media`

### user_insights
Métricas agregadas da conta (não por mídia).

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | FK → accounts | Conta associada |
| metric_name | TEXT | | follower_count, reach, impressions, profile_views |
| metric_value | REAL | | Valor numérico |
| period | TEXT | | day, week, days_28 |
| end_time | TEXT | | Fim do período ISO 8601 |
| fetched_at | TEXT | DEFAULT now | Quando foi buscado |

### templates
Templates reutilizáveis para captions e hashtags.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| name | TEXT | UNIQUE NOT NULL | Nome do template (ex: "promo") |
| caption_template | TEXT | | Template com {variáveis} |
| hashtag_set | TEXT | | JSON array de hashtags |
| default_schedule_time | TEXT | | Horário padrão (HH:MM) |
| created_at | TEXT | DEFAULT now | Timestamp de criação |

### hashtag_searches
Tracking de buscas de hashtag (para respeitar limite de 30/semana).

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | FK → accounts | Conta associada |
| hashtag | TEXT | | Hashtag pesquisada |
| ig_hashtag_id | TEXT | | ID retornado pela API |
| searched_at | TEXT | DEFAULT now | Timestamp da pesquisa |

### action_log
Audit log de todas as ações que modificam dados.

| Campo | Tipo | Constraint | Descrição |
|-------|------|------------|-----------|
| id | INTEGER | PK | Auto-increment |
| account_id | INTEGER | | Conta associada (pode ser NULL) |
| action | TEXT | NOT NULL | Nome da ação (publish_photo, delete_comment, etc.) |
| params | TEXT | | JSON com parâmetros da ação |
| result | TEXT | | JSON com resultado |
| confirmed | INTEGER | | Se foi confirmado pelo usuário (0/1/NULL) |
| rate_remaining | TEXT | | JSON com rate limits restantes |
| created_at | TEXT | DEFAULT now | Timestamp da ação |

**Índice:** `idx_action_log_created`

## Queries Comuns

### Contar publicações hoje
```sql
SELECT COUNT(*) FROM action_log
WHERE action LIKE 'publish_%' AND created_at >= date('now')
```

### Posts não publicados prontos para processar
```sql
SELECT * FROM posts
WHERE status IN ('approved', 'scheduled', 'container_created')
AND (scheduled_at IS NULL OR scheduled_at <= datetime('now'))
ORDER BY created_at
```

### Engajamento médio por tipo de mídia
```sql
SELECT p.media_type,
       AVG(i.metric_value) as avg_engagement
FROM posts p
JOIN insights i ON i.ig_media_id = p.ig_media_id
WHERE i.metric_name = 'engagement'
GROUP BY p.media_type
```

### Comentários não respondidos
```sql
SELECT c.*, p.permalink
FROM comments c
JOIN posts p ON p.ig_media_id = c.ig_media_id
WHERE c.replied = 0
ORDER BY c.timestamp DESC
```

### Hashtags usadas esta semana
```sql
SELECT DISTINCT hashtag, COUNT(*) as searches
FROM hashtag_searches
WHERE searched_at >= datetime('now', '-7 days')
GROUP BY hashtag
ORDER BY searches DESC
```

---

## Reference: Setup_Walkthrough

# Setup Walkthrough — Meta App e OAuth

## Pré-requisitos

1. Conta Instagram Business ou Creator
2. Facebook Page vinculada à conta IG (obrigatório para Business, recomendado para Creator)
3. Conta de desenvolvedor Meta (developers.facebook.com)

## Passo 1: Criar Meta App

1. Acesse [Meta for Developers](https://developers.facebook.com/apps/)
2. Clique "Create App"
3. Escolha "Business" como tipo
4. Preencha:
   - **App name**: Nome do seu app (ex: "Meu Instagram Manager")
   - **Contact email**: Seu email
   - **Business account**: Selecione ou crie
5. Clique "Create App"

## Passo 2: Adicionar Instagram API

1. No dashboard do app, vá em "Add Products"
2. Encontre "Instagram" e clique "Set Up"
3. Em "Instagram Graph API", clique "Configure"

## Passo 3: Configurar OAuth

### Redirect URI
1. Vá em Settings → Basic
2. Em "Valid OAuth Redirect URIs", adicione:
   ```
   http://localhost:8765/callback
   ```
   (Esta é a porta padrão do auth.py)

### Obter Credenciais
1. Anote o **App ID** (visível no topo do dashboard)
2. Vá em Settings → Basic → **App Secret** (clique "Show")
3. Guarde ambos — serão usados no setup

## Passo 4: Adicionar Testers (Modo de Desenvolvimento)

Em modo de desenvolvimento, apenas testers podem usar o app:

1. App Dashboard → Roles → Roles
2. Clique "Add Testers"
3. Adicione a conta Instagram que será gerenciada
4. O tester precisa aceitar o convite via Settings → Apps and Websites no Instagram

## Passo 5: Configurar Permissões

1. App Dashboard → App Review → Permissions and Features
2. Request as seguintes permissões:
   - `instagram_basic`
   - `instagram_content_publish`
   - `instagram_manage_comments`
   - `instagram_manage_insights`
   - `instagram_manage_messages`
   - `pages_show_list`
   - `pages_read_engagement`

**Nota:** Em modo de desenvolvimento, permissões funcionam para testers sem aprovação formal.

## Passo 6: Executar auth.py

Com App ID e App Secret em mãos:

```bash
python C:\Users\renat\skills\instagram\scripts\auth.py --setup
```

O script vai:
1. Pedir App ID e App Secret
2. Abrir o navegador na página de autorização do Facebook
3. Você autoriza o app e as permissões
4. O navegador redireciona para `localhost:8765/callback`
5. O script captura o código, troca por token curto, depois longo
6. Descobre a conta IG vinculada via Facebook Pages API
7. Salva tudo no banco SQLite

### Resultado esperado:
```json
{
  "status": "success",
  "account": {
    "ig_user_id": "17841400000000",
    "username": "sua_conta",
    "account_type": "BUSINESS",
    "token_expires_at": "2026-04-26T..."
  }
}
```

## Passo 7: Verificar

```bash
# Verificar token e conta
python C:\Users\renat\skills\instagram\scripts\auth.py --status

# Testar leitura de perfil
python C:\Users\renat\skills\instagram\scripts\profile.py --view

# Testar listagem de mídia
python C:\Users\renat\skills\instagram\scripts\media.py --list --limit 3
```

## Troubleshooting

### "No Instagram Business Account found"
- Verifique se a conta IG é Business ou Creator (não Personal)
- Verifique se a Facebook Page está vinculada à conta IG
- Execute: `python scripts/account_setup.py --check`

### "Invalid OAuth redirect_uri"
- Confirme que `http://localhost:8765/callback` está nas Redirect URIs do app
- Verifique se não há espaço extra na URL

### "App not approved"
- Em modo de desenvolvimento, adicione seu perfil como Tester
- Para produção, submeta para App Review

### Token expirado
```bash
python C:\Users\renat\skills\instagram\scripts\auth.py --refresh
```
O token longo dura 60 dias e é renovado automaticamente quando faltam 7 dias.

### "Permission denied" (code 10/200)
- Verifique se o scope necessário foi autorizado
- Consulte `references/permissions.md` para o scope correto
- Pode ser necessário re-autorizar: `python scripts/auth.py --setup`

## Variáveis de Ambiente (Opcional)

Em vez de digitar no setup, pode usar env vars:
```bash
export INSTAGRAM_APP_ID="seu_app_id"
export INSTAGRAM_APP_SECRET="seu_app_secret"
export IMGUR_CLIENT_ID="seu_imgur_client_id"
```

O `config.py` checa env vars antes de pedir input.
