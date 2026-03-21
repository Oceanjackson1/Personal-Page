---
title: "Whatsapp Cloud API"
description: "Integracao com WhatsApp Business Cloud API (Meta). Mensagens, templates, webhooks HMAC-SHA256, automacao de atendimento. Boilerplates Node.js e Python."
category: "devops"
source: "community"
author: "Community"
tags: ["whatsapp", "cloud", "api"]
date: 2026-03-20
---

# WhatsApp Cloud API - Integracao Profissional

## Overview

Integracao com WhatsApp Business Cloud API (Meta). Mensagens, templates, webhooks HMAC-SHA256, automacao de atendimento. Boilerplates Node.js e Python.

## When to Use This Skill

- When the user mentions "whatsapp" or related topics
- When the user mentions "whatsapp business" or related topics
- When the user mentions "api whatsapp" or related topics
- When the user mentions "chatbot whatsapp" or related topics
- When the user mentions "mensagem whatsapp" or related topics
- When the user mentions "template whatsapp" or related topics

## Do Not Use This Skill When

- The task is unrelated to whatsapp cloud api
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Skill para implementar integracoes profissionais com WhatsApp Business usando a Cloud API oficial da Meta. Suporta Node.js/TypeScript e Python.

## Overview

A WhatsApp Cloud API e a API oficial da Meta para envio e recebimento de mensagens via WhatsApp Business. Desde outubro 2025, e a unica opcao suportada (a API On-Premises foi descontinuada).

**Versao da API:** Graph API v21.0 (2026)
**Base URL:** `https://graph.facebook.com/v21.0/{phone-number-id}/messages`
**Autenticacao:** Bearer Token (System User Token para producao)

**Pricing 2026 (por mensagem):**

| Categoria      | Custo             | Quando cobrado                          |
|----------------|-------------------|-----------------------------------------|
| Marketing      | $0.025-$0.1365    | Campanhas, promocoes                    |
| Utility        | $0.004-$0.0456    | Confirmacoes de pedido, atualizacoes    |
| Authentication | $0.004-$0.0456    | OTP, reset de senha                     |
| Service        | GRATIS            | Resposta dentro da janela de 24h        |

**Pre-requisitos:**
- Conta Meta Business Suite (gratuita)
- App no Meta for Developers com produto WhatsApp
- Numero de telefone verificado
- System User Token (permanente)

Se o usuario nao tem conta Meta Business, leia `references/setup-guide.md` para o guia completo de setup do zero.

---

## Decision Tree

Use esta arvore para determinar o proximo passo:

```
O usuario precisa de setup inicial?
├── SIM → Leia references/setup-guide.md
└── NAO → Qual linguagem?
    ├── Node.js/TypeScript
    └── Python
    → O que quer fazer?
       ├── Enviar mensagens → Secao "Tipos de Mensagem" abaixo
       ├── Receber mensagens → Secao "Webhooks" abaixo
       ├── Automatizar atendimento → Secao "Automacao" abaixo
       ├── WhatsApp Flows / Commerce → Secao "Features Avancados" abaixo
       ├── Gerenciar templates → references/template-management.md
       └── Compliance / limites → Secao "Compliance & Quality" abaixo
```

Para iniciar um projeto do zero com boilerplate pronto, use o script:
```bash
python scripts/setup_project.py --language nodejs --path ./meu-projeto

## Ou

python scripts/setup_project.py --language python --path ./meu-projeto
```

---

## 1. Configurar Variaveis De Ambiente

```env
WHATSAPP_TOKEN=seu_access_token_aqui
PHONE_NUMBER_ID=seu_phone_number_id
WABA_ID=seu_whatsapp_business_account_id
APP_SECRET=seu_app_secret
VERIFY_TOKEN=token_customizado_para_webhook
```

## 2. Enviar Mensagem De Texto Simples

**Node.js/TypeScript:**
```typescript
import axios from 'axios';

const GRAPH_API = 'https://graph.facebook.com/v21.0';

async function sendText(to: string, message: string) {
  const response = await axios.post(
    `${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`,
    {
      messaging_product: 'whatsapp',
      to,
      type: 'text',
      text: { body: message }
    },
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );
  return response.data; // { messaging_product, contacts, messages: [{ id }] }
}
```

**Python:**
```python
import httpx
import os

GRAPH_API = "https://graph.facebook.com/v21.0"

async def send_text(to: str, message: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_API}/{os.environ['PHONE_NUMBER_ID']}/messages",
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            },
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()  # {"messaging_product", "contacts", "messages": [{"id"}]}
```

## 3. Enviar Template Message (Fora Da Janela De 24H)

Templates sao a unica forma de iniciar conversa com um cliente. Devem ser aprovados pela WhatsApp antes do uso.

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "João" }
        ]
      }
    ]
  }
}
```

## 4. Verificar Entrega

Use o script de teste para validar:
```bash
python scripts/send_test_message.py --to 5511999999999 --message "Teste de integracao"
```

---

## Tipos De Mensagem

| Tipo               | Uso                                   | Limite           |
|--------------------|---------------------------------------|------------------|
| Text               | Mensagens simples de texto            | 4096 chars       |
| Template           | Iniciar conversa / fora da janela 24h | 1600 chars body  |
| Image              | Fotos e imagens                       | 5MB              |
| Document           | PDFs, planilhas, docs                 | 100MB            |
| Video              | Videos                                | 16MB             |
| Audio              | Mensagens de voz                      | 16MB             |
| Interactive Button | Botoes de resposta rapida             | Max 3 botoes     |
| Interactive List   | Menu com opcoes em secoes             | Max 10 opcoes    |
| Location           | Compartilhar localizacao              | lat/long         |
| Contact            | Compartilhar contato                  | vCard format     |
| Reaction           | Reagir com emoji a mensagem           | 1 emoji          |

**Exemplo - Botoes interativos (Node.js):**
```typescript
async function sendButtons(to: string, body: string, buttons: Array<{id: string, title: string}>) {
  return axios.post(`${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`, {
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      body: { text: body },
      action: {
        buttons: buttons.map(b => ({
          type: 'reply',
          reply: { id: b.id, title: b.title }
        }))
      }
    }
  }, { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } });
}

// Uso:
await sendButtons('5511999999999', 'Como posso ajudar?', [
  { id: 'suporte', title: 'Suporte' },
  { id: 'vendas', title: 'Vendas' },
  { id: 'info', title: 'Informacoes' }
]);
```

**Para exemplos completos de todos os tipos em Node.js e Python**, leia `references/message-types.md`.

---

## Webhooks

Webhooks permitem receber mensagens e atualizacoes de status em tempo real.

## Verificacao (Get) - Obrigatorio

Quando voce configura o webhook no Meta Developers, a Meta envia um GET para verificar:

```typescript
// Node.js (Express)
app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === process.env.VERIFY_TOKEN) {
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
});
```

## Recebimento (Post) - Com Seguranca Hmac-Sha256

Toda notificacao de webhook vem assinada no header `X-Hub-Signature-256`. Valide SEMPRE antes de processar:

```typescript
import crypto from 'crypto';

function validateSignature(rawBody: Buffer, signature: string): boolean {
  const expectedSig = crypto
    .createHmac('sha256', process.env.APP_SECRET!)
    .update(rawBody)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(`sha256=${expectedSig}`),
    Buffer.from(signature)
  );
}
```

**Importante:** Usar `crypto.timingSafeEqual` (Node.js) ou `hmac.compare_digest` (Python) para prevenir timing attacks. Nunca use comparacao simples de strings.

## Eventos Recebidos

- **messages** - Mensagem do cliente (texto, midia, botao, localizacao)
- **statuses** - Atualizado de status (sent → delivered → read)
- **errors** - Erros de entrega

**Requisitos:**
- Endpoint HTTPS com certificado SSL valido
- Responder com HTTP 200 em ate 5 segundos
- Dev: use ngrok para teste local

**Para setup completo com exemplos Node.js e Python**, leia `references/webhook-setup.md`.

---

## Menu Principal Interativo

Use botoes ou listas para criar um menu de opcoes na primeira interacao:

```python

## Python - Menu Com Lista Interativa

async def send_main_menu(to: str):
    await send_interactive_list(
        to=to,
        header="Bem-vindo!",
        body="Selecione o que precisa:",
        button_text="Ver opcoes",
        sections=[{
            "title": "Atendimento",
            "rows": [
                {"id": "suporte", "title": "Suporte Tecnico", "description": "Ajuda com problemas"},
                {"id": "vendas", "title": "Vendas", "description": "Conhecer nossos produtos"},
                {"id": "financeiro", "title": "Financeiro", "description": "Boletos e pagamentos"},
            ]
        }]
    )
```

## State Machine Para Fluxos

Gerencie conversas com uma maquina de estados. Cada cliente tem um estado atual que determina como a proxima mensagem sera processada:

```
INICIO → MENU_PRINCIPAL → SUPORTE → AGUARDANDO_DETALHES → ESCALACAO_HUMANO
                        → VENDAS → CATALOGO → CHECKOUT
                        → FINANCEIRO → SEGUNDA_VIA_BOLETO
```

## Janela De 24 Horas

- **Dentro da janela (24h apos ultima mensagem do cliente):** Pode enviar qualquer tipo de mensagem gratuitamente
- **Fora da janela:** Apenas template messages (cobradas por categoria)

## Integracao Com Ia (Claude Api)

Combine WhatsApp com Claude para respostas inteligentes:
1. Receba mensagem via webhook
2. Envie para Claude API com contexto da conversa
3. Retorne resposta via WhatsApp
4. Mantenha escalacao para humano disponivel

**Para padroes completos de automacao**, leia `references/automation-patterns.md`.

---

## Whatsapp Flows

Formularios interativos multi-tela dentro do WhatsApp. O cliente preenche campos sem sair do app. Definidos em JSON com screens, components e actions.

Use cases: cadastros, agendamentos, pesquisas NPS, selecao de produtos.

## Commerce & Catalogo

Ate 500 produtos no catalogo WhatsApp. Envie mensagens de produto individual ou multi-produto com checkout in-app.

## Template Management Api

Crie, liste e delete templates programaticamente. Ate 6000 traducoes por conta. Aprovacao em minutos.

## Whatsapp Channels

Broadcasting unidirecional para subscribers ilimitados. Localizado na aba "Atualizacoes" do WhatsApp.

## Click-To-Whatsapp Ads

Anuncios no Facebook/Instagram com botao que abre conversa no WhatsApp. 99% de taxa de abertura.

## Status Tracking

Rastreie entrega: pending → server → device → read. Receba via webhook de status updates.

**Para detalhes completos de features avancados**, leia `references/advanced-features.md`.
**Para gerenciamento de templates via API**, leia `references/template-management.md`.

---

## Checklist Essencial

- [ ] Opt-in explicito obtido antes de enviar mensagens
- [ ] Mecanismo de opt-out implementado (keyword "SAIR" ou "STOP")
- [ ] Registro de consentimento com timestamp, metodo e proposito
- [ ] Conteudo dentro das politicas do WhatsApp (sem spam, sem conteudo proibido)
- [ ] LGPD/GDPR compliance (base legal definida, direitos do titular)
- [ ] Frequencia de mensagens adequada (nao excessiva)
- [ ] Templates aprovados antes do uso
- [ ] Verificacao de negocio completa (para limites maiores)

## Quality Rating

O WhatsApp monitora a qualidade das suas mensagens e atribui um rating:

| Rating    | Significado                        | Acao                              |
|-----------|------------------------------------|-----------------------------------|
| Verde     | Boa qualidade, poucos bloqueios    | Manter — elegivel para upgrade    |
| Amarelo   | Qualidade media, atencao necessaria| Revisar conteudo e frequencia     |
| Vermelho  | Qualidade baixa, risco de suspensao| Acao imediata: reduzir volume     |

**Sinais positivos:** Alta taxa de resposta, engajamento, poucos bloqueios
**Sinais negativos:** Bloqueios, reports de spam, baixo engajamento

## Tier System (Limites De Mensagem)

Desde outubro 2025, limites sao por **Business Portfolio** (nao por numero):

| Tier         | Conversas/24h | Como alcancar                           |
|--------------|---------------|------------------------------------------|
| Inicial      | 250           | Conta nova / nao verificada              |
| Tier 1       | 1,000         | Auto-upgrade: 50%+ do limite por 7 dias  |
| Tier 2       | 10,000        | Auto-upgrade: 50%+ do limite por 7 dias  |
| Tier 3       | 100,000       | Auto-upgrade: 50%+ do limite por 7 dias  |
| Unlimited    | Ilimitado     | Auto-upgrade: 50%+ do limite por 7 dias  |

**Mudancas 2026:** Tiers 2K e 10K serao removidos. Apos verificacao de negocio, limite imediato de 100K.

**Para guia completo de compliance**, leia `references/compliance.md`.

---

## Troubleshooting

| Problema                       | Causa Provavel                     | Solucao                                    |
|--------------------------------|------------------------------------|--------------------------------------------|
| 401 Unauthorized               | Token expirado ou invalido         | Gerar novo System User Token               |
| 400 Bad Request                | Payload malformado                 | Verificar JSON contra exemplos             |
| Template rejeitado             | Conteudo viola politicas           | Revisar e resubmeter com alteracoes        |
| Webhook nao recebe             | URL invalida ou sem HTTPS          | Usar ngrok (dev) ou certificado SSL (prod) |
| Rate limit exceeded            | Ultrapassou 80 msg/s              | Implementar queue com retry                |
| Quality rating baixo           | Muitos bloqueios/reports           | Reduzir volume, melhorar conteudo          |
| Mensagem nao entregue          | Numero invalido ou nao no WhatsApp | Validar numero antes de enviar             |
| Numero nao verificado          | OTP nao completado                 | Repetir verificacao via SMS ou ligacao      |

Para validar sua configuracao:
```bash
python scripts/validate_config.py
```

---

## Referencias (Leia Conforme Necessidade)

| Arquivo                        | Quando ler                                        |
|--------------------------------|---------------------------------------------------|
| `references/setup-guide.md`    | Setup inicial — criar conta Meta, configurar API  |
| `references/message-types.md`  | Exemplos completos de todos os tipos de mensagem   |
| `references/webhook-setup.md`  | Configurar webhooks com seguranca HMAC             |
| `references/automation-patterns.md` | Chatbot, filas, state machine, integracao IA  |
| `references/compliance.md`     | LGPD/GDPR, opt-in, quality rating, tier system    |
| `references/api-reference.md`  | Endpoints, erros, rate limits, pricing 2026        |
| `references/advanced-features.md` | Flows, Commerce, Channels, Ads, Status Tracking|
| `references/template-management.md` | CRUD de templates via API                     |

## Scripts

| Script                         | O que faz                                         |
|--------------------------------|---------------------------------------------------|
| `scripts/setup_project.py`     | Cria projeto com boilerplate (Node.js ou Python)   |
| `scripts/validate_config.py`   | Valida credenciais e conexao com a API             |
| `scripts/send_test_message.py` | Envia mensagem teste para validar setup            |

## Boilerplate

| Diretorio                      | Conteudo                                          |
|--------------------------------|---------------------------------------------------|
| `assets/boilerplate/nodejs/`   | Projeto TypeScript/Express completo                |
| `assets/boilerplate/python/`   | Projeto Python/Flask completo                      |
| `assets/examples/`             | Exemplos de payloads JSON (templates, webhooks, flows) |

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `instagram` - Complementary skill for enhanced analysis
- `social-orchestrator` - Complementary skill for enhanced analysis
- `telegram` - Complementary skill for enhanced analysis

---

## Reference: Advanced Features

# Features Avancados - WhatsApp Cloud API

Guia dos recursos avancados da WhatsApp Business Platform: Flows, Commerce, Channels, Click-to-WhatsApp Ads e Status Tracking.

---

## Indice

1. [WhatsApp Flows](#whatsapp-flows)
2. [Commerce e Catalogo](#commerce-e-catalogo)
3. [WhatsApp Channels](#whatsapp-channels)
4. [Click-to-WhatsApp Ads](#click-to-whatsapp-ads)
5. [Status Tracking](#status-tracking)
6. [Analytics e Reporting](#analytics-e-reporting)

---

## WhatsApp Flows

WhatsApp Flows permite criar formularios interativos multi-tela dentro do WhatsApp. O cliente preenche campos, seleciona opcoes e envia dados sem sair do app.

### Quando Usar

- Cadastros e registros
- Agendamentos e reservas
- Pesquisas NPS e feedback
- Selecao de produtos com opcoes
- Formularios de suporte com campos estruturados
- Questionarios de qualificacao de leads

### Estrutura JSON de um Flow

Um Flow e composto por **screens** (telas) com **components** (campos):

```json
{
  "version": "3.0",
  "screens": [
    {
      "id": "SCREEN_1",
      "title": "Agendamento",
      "data": {},
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Agende sua consulta"
          },
          {
            "type": "TextInput",
            "name": "customer_name",
            "label": "Seu nome completo",
            "required": true,
            "input-type": "text"
          },
          {
            "type": "DatePicker",
            "name": "appointment_date",
            "label": "Data desejada",
            "required": true,
            "min-date": "1709251200000",
            "max-date": "1711929600000"
          },
          {
            "type": "Dropdown",
            "name": "service_type",
            "label": "Tipo de servico",
            "required": true,
            "data-source": [
              { "id": "consulta", "title": "Consulta" },
              { "id": "retorno", "title": "Retorno" },
              { "id": "exame", "title": "Exame" }
            ]
          },
          {
            "type": "Footer",
            "label": "Confirmar",
            "on-click-action": {
              "name": "navigate",
              "next": { "type": "screen", "name": "SCREEN_2" },
              "payload": {
                "customer_name": "${form.customer_name}",
                "appointment_date": "${form.appointment_date}",
                "service_type": "${form.service_type}"
              }
            }
          }
        ]
      }
    },
    {
      "id": "SCREEN_2",
      "title": "Confirmacao",
      "terminal": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Confirme seus dados"
          },
          {
            "type": "TextBody",
            "text": "Nome: ${data.customer_name}\nData: ${data.appointment_date}\nServico: ${data.service_type}"
          },
          {
            "type": "Footer",
            "label": "Confirmar Agendamento",
            "on-click-action": {
              "name": "complete",
              "payload": {
                "customer_name": "${data.customer_name}",
                "appointment_date": "${data.appointment_date}",
                "service_type": "${data.service_type}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

### Componentes Disponiveis

| Componente       | Descricao                          | Campos principais              |
|------------------|------------------------------------|--------------------------------|
| TextHeading      | Titulo de secao                    | text                           |
| TextBody         | Texto descritivo                   | text                           |
| TextInput        | Campo de texto                     | name, label, input-type        |
| TextArea         | Area de texto multi-linha          | name, label                    |
| DatePicker       | Seletor de data                    | name, label, min-date, max-date|
| Dropdown         | Lista suspensa                     | name, label, data-source       |
| RadioButtonsGroup| Botoes de opcao                    | name, label, data-source       |
| CheckboxGroup    | Caixas de selecao                  | name, label, data-source       |
| OptIn            | Checkbox de aceite                 | name, label                    |
| Footer           | Botao de acao/navegacao            | label, on-click-action         |

### Enviar Flow via API

```typescript
async function sendFlow(to: string, flowId: string, screenId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'flow',
      header: { type: 'text', text: 'Agendar Consulta' },
      body: { text: 'Preencha o formulário abaixo para agendar.' },
      footer: { text: 'Seus dados são protegidos' },
      action: {
        name: 'flow',
        parameters: {
          flow_message_version: '3',
          flow_id: flowId,
          flow_cta: 'Agendar',
          flow_action: 'navigate',
          flow_action_payload: {
            screen: screenId,
            data: {}
          }
        }
      }
    }
  });
}
```

### Receber Resposta do Flow

```typescript
function handleFlowResponse(message: IncomingMessage): Record<string, any> | null {
  if (message.interactive?.type === 'nfm_reply') {
    return JSON.parse(message.interactive.nfm_reply.response_json);
    // Ex: { customer_name: "João", appointment_date: "2026-03-01", service_type: "consulta" }
  }
  return null;
}
```

### Criar Flows

Flows podem ser criados de duas formas:
1. **Visual Builder** - No WhatsApp Manager, arrastar e soltar componentes
2. **JSON Editor** - Editar diretamente o JSON para controle total

---

## Commerce e Catalogo

### Configurar Catalogo

O catalogo WhatsApp suporta ate **500 produtos** vinculados ao seu perfil de negocio.

**Configuracao:**
1. Abra o WhatsApp Manager
2. Va para Account Tools → Catalog
3. Adicione produtos com: nome, descricao, preco, imagem, URL

### Enviar Mensagem de Produto Unico

```typescript
async function sendSingleProduct(to: string, catalogId: string, productId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'product',
      body: { text: 'Confira este produto!' },
      footer: { text: 'Responda para comprar' },
      action: {
        catalog_id: catalogId,
        product_retailer_id: productId
      }
    }
  });
}
```

### Enviar Mensagem Multi-Produto

```typescript
async function sendMultiProduct(
  to: string,
  catalogId: string,
  sections: Array<{ title: string; product_items: Array<{ product_retailer_id: string }> }>
): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'product_list',
      header: { type: 'text', text: 'Nossos Produtos' },
      body: { text: 'Selecione os produtos que deseja:' },
      footer: { text: 'Adicione ao carrinho' },
      action: {
        catalog_id: catalogId,
        sections
      }
    }
  });
}

// Uso:
await sendMultiProduct('5511999999999', 'CATALOG_ID', [
  {
    title: 'Eletronicos',
    product_items: [
      { product_retailer_id: 'SKU_001' },
      { product_retailer_id: 'SKU_002' }
    ]
  },
  {
    title: 'Acessorios',
    product_items: [
      { product_retailer_id: 'SKU_003' },
      { product_retailer_id: 'SKU_004' }
    ]
  }
]);
```

### Checkout In-App

Quando o cliente seleciona produtos e faz checkout, voce recebe via webhook:

```json
{
  "type": "order",
  "order": {
    "catalog_id": "CATALOG_ID",
    "product_items": [
      {
        "product_retailer_id": "SKU_001",
        "quantity": 2,
        "item_price": 99.90,
        "currency": "BRL"
      }
    ],
    "text": "Quero esses produtos"
  }
}
```

### Sync com Inventario

Para manter o catalogo atualizado:

```python
async def sync_inventory(catalog_id: str, products: list[dict]) -> None:
    """Sincroniza inventario com o catalogo WhatsApp via Commerce Manager API."""
    for product in products:
        await update_product(
            catalog_id=catalog_id,
            product_id=product["sku"],
            data={
                "availability": "in stock" if product["stock"] > 0 else "out of stock",
                "price": product["price"] * 100,  # Em centavos
                "currency": "BRL"
            }
        )
```

---

## WhatsApp Channels

WhatsApp Channels e um recurso de broadcasting unidirecional. Voce envia atualizacoes para subscribers ilimitados na aba "Atualizacoes" do WhatsApp.

### Caracteristicas

- **Unidirecional:** Apenas o admin envia, subscribers recebem
- **Privacidade do admin:** Followers nao veem seu numero pessoal
- **Privacidade do subscriber:** Admin nao ve numeros dos followers (a menos que salvos como contatos)
- **Conteudo:** Texto, imagens, videos, stickers, polls

### Analytics Disponiveis (30 dias)

| Metrica           | Descricao                              |
|-------------------|----------------------------------------|
| Crescimento       | Novos followers vs unfollows           |
| Alcance           | Quantos viram suas mensagens           |
| Engajamento       | Reacoes com emoji                      |
| Resultados de polls| Votos em enquetes                     |

### Melhores Praticas

- Publique conteudo relevante e nao promocional em excesso
- Use polls para engajamento
- Frequencia ideal: 2-5 postagens por semana
- Conteudo exclusivo incentiva follows

---

## Click-to-WhatsApp Ads

Anuncios no Facebook e Instagram com botao que abre conversa no WhatsApp.

### Setup no Meta Ads Manager

1. Criar campanha com objetivo "Messaging", "Leads" ou "Sales"
2. Selecionar "Click to WhatsApp" como destino
3. Vincular conta WhatsApp Business
4. Configurar mensagem pre-preenchida (greeting + pre-filled message)

### Pre-filled Messages

Configure a mensagem que o cliente ve quando abre o chat:

```
Greeting: "Olá! Obrigado por clicar no nosso anúncio."
Pre-filled: "Oi, vi o anúncio sobre [produto] e gostaria de saber mais!"
```

### Integracao no Webhook

Quando um cliente vem de um anuncio, o webhook inclui dados de referral:

```json
{
  "messages": [{
    "from": "5511999999999",
    "type": "text",
    "text": { "body": "Oi, vi o anúncio..." },
    "referral": {
      "source_url": "https://fb.me/...",
      "source_type": "ad",
      "source_id": "AD_ID",
      "headline": "Titulo do Anuncio",
      "body": "Texto do anuncio",
      "ctwa_clid": "click_id_para_tracking"
    }
  }]
}
```

### Tracking de Conversao

```typescript
function handleAdReferral(message: IncomingMessage): void {
  if (message.referral) {
    const adData = {
      adId: message.referral.source_id,
      clickId: message.referral.ctwa_clid,
      headline: message.referral.headline,
      customerPhone: message.from,
      timestamp: new Date()
    };

    // Registrar lead vindo do anuncio
    trackConversion(adData);

    // Personalizar atendimento com contexto do anuncio
    customizeGreeting(message.from, adData.headline);
  }
}
```

### Metricas

- **Taxa de abertura:** ~99% (mensagens WhatsApp)
- **Reducao de custo:** Ate 32% menor custo por lead vs formularios
- **Aumento:** Ate 46% mais mensagens de clientes

---

## Status Tracking

### Ciclo de Vida da Mensagem

```
Enviada (sent) → Entregue ao servidor (delivered) → Entregue ao dispositivo (delivered) → Lida (read)
```

### Status via Webhook

```json
{
  "statuses": [
    {
      "id": "wamid.HBgNNTUxMTk5...",
      "status": "delivered",
      "timestamp": "1709251200",
      "recipient_id": "5511999999999",
      "conversation": {
        "id": "CONVERSATION_ID",
        "origin": { "type": "business_initiated" },
        "expiration_timestamp": "1709337600"
      },
      "pricing": {
        "billable": true,
        "pricing_model": "CBP",
        "category": "utility"
      }
    }
  ]
}
```

### Status Possiveis

| Status      | Descricao                              | Confiabilidade      |
|-------------|----------------------------------------|---------------------|
| `sent`      | Mensagem enviada para servidores Meta  | Alta                |
| `delivered` | Entregue ao dispositivo do cliente     | Alta                |
| `read`      | Cliente leu a mensagem (blue check)    | Media (pode ser off)|
| `failed`    | Falha na entrega                       | Alta                |

### Limitacao Importante

O status `read` depende de o usuario ter **read receipts ativados** nas configuracoes do WhatsApp. Muitos usuarios desativam. Use `delivered` como confirmacao confiavel de entrega.

### Implementacao de Tracking

```typescript
interface MessageStatus {
  messageId: string;
  to: string;
  sentAt: Date;
  deliveredAt?: Date;
  readAt?: Date;
  failedAt?: Date;
  failureReason?: string;
}

async function processStatusUpdate(status: WebhookStatus): Promise<void> {
  const update: Partial<MessageStatus> = {};

  switch (status.status) {
    case 'sent':
      update.sentAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'delivered':
      update.deliveredAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'read':
      update.readAt = new Date(parseInt(status.timestamp) * 1000);
      break;
    case 'failed':
      update.failedAt = new Date(parseInt(status.timestamp) * 1000);
      update.failureReason = status.errors?.[0]?.message;
      break;
  }

  await db.messageStatuses.updateOne(
    { messageId: status.id },
    { $set: update }
  );
}
```

---

## Analytics e Reporting

### Metricas Essenciais para Atendimento

| Metrica                        | Como Calcular                          | Meta Ideal          |
|-------------------------------|----------------------------------------|---------------------|
| Tempo Primeira Resposta (FRT) | Timestamp resposta - timestamp mensagem| < 5 minutos         |
| Tempo Medio de Resolucao      | Timestamp fechamento - timestamp inicio| < 30 minutos        |
| Taxa de Resolucao no Bot      | Resolvidos pelo bot / total            | > 60%               |
| Taxa de Escalacao              | Escalados para humano / total          | < 40%               |
| CSAT (Satisfacao)              | Pesquisa NPS pos-atendimento           | > 4.0 / 5.0         |
| Taxa de Entrega                | Delivered / sent                       | > 95%               |
| Taxa de Leitura                | Read / delivered                       | > 70%               |
| Taxa de Opt-out               | Optouts / total da base                | < 2% por campanha   |

### Pesquisa NPS via WhatsApp

```typescript
async function sendNPSSurvey(to: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      body: {
        text: 'De 1 a 5, como voce avalia nosso atendimento?\n\n' +
              '1 = Muito ruim\n5 = Excelente'
      },
      action: {
        buttons: [
          { type: 'reply', reply: { id: 'nps_1_2', title: '1-2 Ruim' } },
          { type: 'reply', reply: { id: 'nps_3', title: '3 Regular' } },
          { type: 'reply', reply: { id: 'nps_4_5', title: '4-5 Bom' } }
        ]
      }
    }
  });
}
```

### Dashboard de Analytics

Para analytics avancados, considere integrar com:
- **Infobip** - Dashboard completo com APIs de reporting
- **Trengo** - CSAT tracking, response times, trending topics
- **Wassenger** - Comparacao de agentes, exportacao CSV/JSON/PDF
- **Solucao propria** - MongoDB/PostgreSQL + Grafana/Metabase

---

## Reference: Api Reference

# API Reference - WhatsApp Cloud API

Referencia tecnica completa dos endpoints, autenticacao, codigos de erro, rate limits e pricing da WhatsApp Cloud API (Graph API v21.0).

---

## Indice

1. [Autenticacao](#autenticacao)
2. [Base URL e Headers](#base-url-e-headers)
3. [Endpoints - Mensagens](#endpoints---mensagens)
4. [Endpoints - Midia](#endpoints---midia)
5. [Endpoints - Templates](#endpoints---templates)
6. [Endpoints - Phone Numbers](#endpoints---phone-numbers)
7. [Endpoints - Business Profile](#endpoints---business-profile)
8. [Webhook Events](#webhook-events)
9. [Codigos de Erro](#codigos-de-erro)
10. [Rate Limits](#rate-limits)
11. [Pricing 2026](#pricing-2026)
12. [Versionamento](#versionamento)

---

## Autenticacao

### Token Temporario (Desenvolvimento)

Obtido no Meta Developers Dashboard. Expira em 24 horas.

### System User Token (Producao)

Token permanente criado via Business Settings:
1. Business Settings → System Users → Add
2. Atribuir role "Admin" ao app
3. Gerar token com permissoes:
   - `whatsapp_business_messaging` (enviar/receber mensagens)
   - `whatsapp_business_management` (gerenciar templates, perfil)

### Header de Autenticacao

```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

---

## Base URL e Headers

```
Base URL: https://graph.facebook.com/v21.0
```

Headers obrigatorios em todas as requests:
```http
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

### IDs Necessarios

| ID                  | Onde encontrar                           | Formato          |
|---------------------|------------------------------------------|------------------|
| Phone Number ID     | WhatsApp > API Setup no dashboard        | Numerico         |
| WABA ID             | WhatsApp > API Setup no dashboard        | Numerico         |
| App Secret          | App Settings > Basic                      | String hex       |
| Business ID         | Business Settings > Business Info         | Numerico         |

---

## Endpoints - Mensagens

### Enviar Mensagem

```
POST /{phone-number-id}/messages
```

**Request Body (texto):**
```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "preview_url": false,
    "body": "Olá! Como posso ajudar?"
  }
}
```

**Response (sucesso):**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    { "input": "5511999999999", "wa_id": "5511999999999" }
  ],
  "messages": [
    { "id": "wamid.HBgNNTUxMTk5..." }
  ]
}
```

**Tipos suportados no campo `type`:**
- `text` - Mensagem de texto
- `template` - Template message
- `image` - Imagem
- `document` - Documento
- `video` - Video
- `audio` - Audio
- `sticker` - Sticker
- `location` - Localizacao
- `contacts` - Contatos
- `interactive` - Botoes, listas, flows
- `reaction` - Reacao com emoji

### Marcar como Lida

```
POST /{phone-number-id}/messages
```

```json
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgNNTUxMTk5..."
}
```

---

## Endpoints - Midia

### Upload de Midia

```
POST /{phone-number-id}/media
Content-Type: multipart/form-data
```

**Form fields:**
- `messaging_product`: "whatsapp"
- `file`: arquivo binario
- `type`: MIME type (ex: "image/jpeg")

**Response:**
```json
{
  "id": "media_id_aqui"
}
```

### Download de Midia

```
GET /{media-id}
```

**Response:**
```json
{
  "url": "https://lookaside.fbsbx.com/...",
  "mime_type": "image/jpeg",
  "sha256": "hash_aqui",
  "file_size": 12345,
  "id": "media_id"
}
```

Depois, faca GET na `url` retornada com o mesmo Authorization header para baixar o arquivo.

### Deletar Midia

```
DELETE /{media-id}
```

### Limites de Midia

| Tipo      | Formatos Aceitos                    | Tamanho Max |
|-----------|-------------------------------------|-------------|
| Image     | JPEG, PNG                           | 5 MB        |
| Document  | PDF, DOC, DOCX, XLS, XLSX, PPT, TXT| 100 MB      |
| Video     | MP4, 3GP                            | 16 MB       |
| Audio     | AAC, AMR, MP3, MP4, OGG             | 16 MB       |
| Sticker   | WEBP                                | 500 KB      |

---

## Endpoints - Templates

### Listar Templates

```
GET /{waba-id}/message_templates
```

**Query parameters:**
- `limit` - Numero de resultados (default: 25)
- `status` - Filtrar por status: APPROVED, PENDING, REJECTED

**Response:**
```json
{
  "data": [
    {
      "name": "hello_world",
      "status": "APPROVED",
      "category": "UTILITY",
      "language": "pt_BR",
      "components": [
        {
          "type": "BODY",
          "text": "Olá {{1}}, seu pedido {{2}} foi confirmado!"
        }
      ],
      "id": "template_id"
    }
  ],
  "paging": { "cursors": { "before": "...", "after": "..." } }
}
```

### Criar Template

```
POST /{waba-id}/message_templates
```

```json
{
  "name": "order_confirmation",
  "category": "UTILITY",
  "language": "pt_BR",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Confirmação de Pedido"
    },
    {
      "type": "BODY",
      "text": "Olá {{1}}, seu pedido #{{2}} foi confirmado! Valor: R$ {{3}}",
      "example": {
        "body_text": [["João", "12345", "99,90"]]
      }
    },
    {
      "type": "FOOTER",
      "text": "Obrigado por comprar conosco!"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "Rastrear Pedido",
          "url": "https://example.com/track/{{1}}",
          "example": ["12345"]
        }
      ]
    }
  ]
}
```

### Deletar Template

```
DELETE /{waba-id}/message_templates
```

```json
{
  "name": "template_name_to_delete"
}
```

**Nota:** Nao e possivel editar um template apos submissao. Para alterar, delete e crie um novo.

**Limite:** Ate 6,000 traducoes de templates por conta.

Para guia completo de gerenciamento de templates, leia `references/template-management.md`.

---

## Endpoints - Phone Numbers

### Listar Numeros

```
GET /{waba-id}/phone_numbers
```

**Response:**
```json
{
  "data": [
    {
      "verified_name": "Minha Empresa",
      "code_verification_status": "VERIFIED",
      "display_phone_number": "+55 11 99999-9999",
      "quality_rating": "GREEN",
      "id": "phone_number_id"
    }
  ]
}
```

### Obter Info do Numero

```
GET /{phone-number-id}?fields=verified_name,code_verification_status,display_phone_number,quality_rating,messaging_limit_tier
```

---

## Endpoints - Business Profile

### Obter Perfil

```
GET /{phone-number-id}/whatsapp_business_profile?fields=about,address,description,email,websites,profile_picture_url
```

### Atualizar Perfil

```
POST /{phone-number-id}/whatsapp_business_profile
```

```json
{
  "messaging_product": "whatsapp",
  "about": "Atendimento de Seg a Sex, 8h-18h",
  "address": "Rua Example, 123 - São Paulo, SP",
  "description": "Empresa líder em soluções digitais",
  "email": "contato@empresa.com",
  "websites": ["https://www.empresa.com"]
}
```

---

## Webhook Events

### Estrutura do Payload

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WABA_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "5511999999999",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              { "profile": { "name": "João" }, "wa_id": "5511888888888" }
            ],
            "messages": [...],
            "statuses": [...]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

### Tipos de Mensagem Recebida

| Campo `type`     | Conteudo                    | Campos relevantes               |
|------------------|-----------------------------|----------------------------------|
| `text`           | Mensagem de texto           | `text.body`                      |
| `image`          | Imagem                      | `image.id`, `image.mime_type`    |
| `document`       | Documento                   | `document.id`, `document.filename`|
| `video`          | Video                       | `video.id`, `video.mime_type`    |
| `audio`          | Audio/voz                   | `audio.id`, `audio.mime_type`    |
| `location`       | Localizacao                 | `location.latitude`, `.longitude`|
| `contacts`       | Contato compartilhado       | `contacts[].name`, `.phones`     |
| `interactive`    | Resposta de botao/lista     | `interactive.button_reply.id` ou `interactive.list_reply.id` |
| `reaction`       | Reacao com emoji            | `reaction.emoji`, `.message_id`  |
| `sticker`        | Sticker                     | `sticker.id`, `sticker.mime_type`|

### Status Updates

```json
{
  "statuses": [
    {
      "id": "wamid.HBgNNTUxMTk5...",
      "status": "delivered",
      "timestamp": "1234567890",
      "recipient_id": "5511999999999"
    }
  ]
}
```

Valores de `status`: `sent` → `delivered` → `read` → `failed`

---

## Codigos de Erro

### Erros Comuns

| Codigo | Mensagem                          | Causa                            | Solucao                              |
|--------|-----------------------------------|----------------------------------|--------------------------------------|
| 0      | AuthException                     | Token invalido ou expirado        | Gerar novo token                     |
| 3      | API Method                        | Metodo HTTP incorreto             | Verificar POST vs GET                |
| 4      | Too many calls                    | Rate limit excedido               | Implementar retry com backoff        |
| 10     | Permission denied                 | Token sem permissao necessaria    | Adicionar permissao ao System User   |
| 100    | Invalid parameter                 | Payload malformado                | Verificar JSON contra documentacao   |
| 131026 | Message undeliverable             | Numero nao esta no WhatsApp       | Validar numero antes de enviar       |
| 131047 | Re-engagement message             | Fora da janela de 24h sem template| Usar template message                |
| 131051 | Unsupported message type          | Tipo de mensagem nao suportado    | Verificar campo `type`               |
| 131053 | Media upload error                | Arquivo invalido ou muito grande  | Verificar formato e tamanho          |
| 132000 | Template param count mismatch     | Numero errado de parametros       | Conferir template e parametros       |
| 132001 | Template does not exist           | Template nao encontrado           | Verificar nome e idioma do template  |
| 132005 | Template hydration failed         | Erro ao preencher variaveis       | Verificar formato dos parametros     |
| 133010 | Phone number not registered       | Numero nao verificado             | Completar verificacao OTP            |
| 135000 | Generic error                     | Erro interno do WhatsApp          | Retry apos alguns segundos           |

### Tratamento de Erros

```typescript
async function sendWithRetry(payload: any, maxRetries = 3): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await axios.post(
        `${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`,
        payload,
        { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
      );
      return response.data;
    } catch (error: any) {
      const errorCode = error.response?.data?.error?.code;
      const errorMessage = error.response?.data?.error?.message;

      // Erros que nao devem ser retentados
      if ([100, 131026, 131051, 132000, 132001].includes(errorCode)) {
        throw new Error(`WhatsApp API Error ${errorCode}: ${errorMessage}`);
      }

      // Rate limit ou erro temporario - retry com backoff
      if (attempt < maxRetries && [4, 135000].includes(errorCode)) {
        const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      throw error;
    }
  }
}
```

---

## Rate Limits

### Throughput (Mensagens por Segundo)

| Tier              | Limite          |
|-------------------|-----------------|
| Standard          | 80 msg/s        |
| Unlimited tier    | 1,000 msg/s     |

### Conversas por 24 Horas

| Tier         | Limite/24h | Como alcancar                         |
|--------------|-----------|----------------------------------------|
| Inicial      | 250       | Conta nova ou nao verificada           |
| Tier 1       | 1,000     | 50%+ do limite por 7 dias + quality ok |
| Tier 2       | 10,000    | 50%+ do limite por 7 dias + quality ok |
| Tier 3       | 100,000   | 50%+ do limite por 7 dias + quality ok |
| Unlimited    | Ilimitado | 50%+ do limite por 7 dias + quality ok |

**Importante:** Limites sao por Business Portfolio (desde outubro 2025), nao por numero.

### Outros Limites

- Templates: 6,000 traducoes por conta
- Botoes interativos: max 3 por mensagem
- Lista interativa: max 10 opcoes, max 3 secoes
- Texto: max 4,096 caracteres
- Template body: max 1,600 caracteres
- Webhooks: responder 200 em ate 5 segundos

---

## Pricing 2026

Desde julho 2025, o modelo e **por mensagem** (nao mais por conversa).

### Custos por Categoria

| Categoria      | Faixa de Preco      | Desconto Volume | Janela 24h    |
|----------------|---------------------|-----------------|---------------|
| Marketing      | $0.025 - $0.1365    | Nao             | Cobrado       |
| Utility        | $0.004 - $0.0456    | Sim             | GRATIS        |
| Authentication | $0.004 - $0.0456    | Sim             | Cobrado       |
| Service        | GRATIS              | N/A             | GRATIS        |

### Exemplos por Regiao (Marketing)

| Regiao          | Custo/msg |
|-----------------|-----------|
| Brasil          | ~$0.05    |
| India           | ~$0.01    |
| EUA/Canada      | ~$0.025   |
| Europa Ocidental| ~$0.10+   |

### Janela de 24 Horas

- Abre quando o cliente envia uma mensagem
- Durante a janela: templates de **utility** sao GRATIS
- Service messages (respostas) sao SEMPRE gratis
- Marketing e authentication sao cobrados mesmo na janela

### Mudancas Janeiro 2026

- Franca e Egito: reducao nos custos de marketing
- India: aumento nos custos de marketing
- America do Norte: reducao em utility e authentication

---

## Versionamento

### Versao Atual

**Graph API v21.0** (lancada janeiro 2026)

### Compatibilidade

- Meta mantem backward compatibility por pelo menos 12 meses
- Versoes antigas recebem aviso de deprecacao antes da remocao
- Sempre especifique a versao na URL: `https://graph.facebook.com/v21.0/`

### Mudancas Planejadas 2026

| Feature                   | Timeline | Descricao                                      |
|---------------------------|----------|-------------------------------------------------|
| BSUID                     | 2026     | Business-Scoped User ID substitui phone numbers |
| Usernames                 | 2026     | WhatsApp introduz usernames para privacidade     |
| Tier removal (2K/10K)     | Q2 2026  | Limite imediato de 100K apos verificacao         |
| Business Portfolio Pacing | Q1 2026  | Pausa automatica de campanhas baseada em feedback|

### Boas Praticas de Versionamento

- Monitore o blog de desenvolvedores da Meta para mudancas
- Teste em sandbox antes de atualizar versao em producao
- Use variaveis de ambiente para a versao da API (facil rollback)
- Mantenha logs de chamadas para debug de compatibilidade

---

## Reference: Automation Patterns

# Padroes de Automacao de Atendimento - WhatsApp Cloud API

Guia completo para implementar automacao de atendimento profissional via WhatsApp, incluindo chatbots, filas de atendimento, state machines e integracao com IA.

---

## Indice

1. [Arquitetura de Automacao](#arquitetura-de-automacao)
2. [Menu Principal Interativo](#menu-principal-interativo)
3. [State Machine para Fluxos](#state-machine-para-fluxos)
4. [Gerenciamento de Sessao](#gerenciamento-de-sessao)
5. [Fila de Atendimento](#fila-de-atendimento)
6. [Escalacao para Humano](#escalacao-para-humano)
7. [Respostas Fora do Horario](#respostas-fora-do-horario)
8. [Integracao com IA (Claude API)](#integracao-com-ia-claude-api)
9. [WhatsApp Flows para Formularios](#whatsapp-flows-para-formularios)
10. [Fluxo End-to-End Completo](#fluxo-end-to-end-completo)

---

## Arquitetura de Automacao

```
Cliente WhatsApp
       │
       ▼
   Webhook POST
       │
       ▼
  HMAC Validation
       │
       ▼
  Session Manager ──► Busca/cria sessao do cliente
       │
       ▼
  State Router ──► Determina handler baseado no estado atual
       │
       ├── INICIO → Menu Principal
       ├── MENU → Router de opcoes
       ├── SUPORTE → Fluxo de suporte
       ├── VENDAS → Catalogo/checkout
       ├── HUMANO → Fila de atendimento
       └── IA → Claude API handler
```

---

## Menu Principal Interativo

### Com Botoes (ate 3 opcoes)

**Node.js:**
```typescript
async function sendMainMenuButtons(to: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      header: { type: 'text', text: 'Bem-vindo!' },
      body: { text: 'Olá! Como posso ajudar você hoje?' },
      footer: { text: 'Selecione uma opção abaixo' },
      action: {
        buttons: [
          { type: 'reply', reply: { id: 'btn_suporte', title: 'Suporte' } },
          { type: 'reply', reply: { id: 'btn_vendas', title: 'Vendas' } },
          { type: 'reply', reply: { id: 'btn_info', title: 'Informações' } }
        ]
      }
    }
  });
}
```

### Com Lista (ate 10 opcoes em secoes)

**Python:**
```python
async def send_main_menu_list(to: str) -> None:
    await send_message({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "Menu Principal"},
            "body": {"text": "Selecione o departamento:"},
            "footer": {"text": "Horário: Seg-Sex 8h-18h"},
            "action": {
                "button": "Ver opções",
                "sections": [
                    {
                        "title": "Atendimento",
                        "rows": [
                            {"id": "suporte_tecnico", "title": "Suporte Técnico", "description": "Problemas com produto ou serviço"},
                            {"id": "suporte_financeiro", "title": "Financeiro", "description": "Boletos, pagamentos, reembolsos"},
                            {"id": "suporte_comercial", "title": "Comercial", "description": "Novos pedidos e orçamentos"}
                        ]
                    },
                    {
                        "title": "Informações",
                        "rows": [
                            {"id": "info_horario", "title": "Horário de Funcionamento"},
                            {"id": "info_endereco", "title": "Endereço e Contato"},
                            {"id": "info_faq", "title": "Perguntas Frequentes"}
                        ]
                    }
                ]
            }
        }
    })
```

---

## State Machine para Fluxos

### Modelo de Estados

```typescript
enum ConversationState {
  INICIO = 'INICIO',
  MENU_PRINCIPAL = 'MENU_PRINCIPAL',
  SUPORTE_TECNICO = 'SUPORTE_TECNICO',
  SUPORTE_AGUARDANDO_DETALHES = 'SUPORTE_AGUARDANDO_DETALHES',
  SUPORTE_AGUARDANDO_ANEXO = 'SUPORTE_AGUARDANDO_ANEXO',
  VENDAS_CATALOGO = 'VENDAS_CATALOGO',
  VENDAS_CHECKOUT = 'VENDAS_CHECKOUT',
  FINANCEIRO = 'FINANCEIRO',
  FINANCEIRO_SEGUNDA_VIA = 'FINANCEIRO_SEGUNDA_VIA',
  ATENDIMENTO_HUMANO = 'ATENDIMENTO_HUMANO',
  ATENDIMENTO_IA = 'ATENDIMENTO_IA',
  PESQUISA_NPS = 'PESQUISA_NPS',
  FINALIZADO = 'FINALIZADO'
}
```

### Router de Estados

```typescript
interface Session {
  phone: string;
  state: ConversationState;
  data: Record<string, any>;
  lastActivity: Date;
  agentId?: string;
}

async function routeMessage(session: Session, message: IncomingMessage): Promise<void> {
  const handlers: Record<ConversationState, MessageHandler> = {
    [ConversationState.INICIO]: handleInicio,
    [ConversationState.MENU_PRINCIPAL]: handleMenuPrincipal,
    [ConversationState.SUPORTE_TECNICO]: handleSuporteTecnico,
    [ConversationState.SUPORTE_AGUARDANDO_DETALHES]: handleAguardandoDetalhes,
    [ConversationState.VENDAS_CATALOGO]: handleVendasCatalogo,
    [ConversationState.FINANCEIRO]: handleFinanceiro,
    [ConversationState.ATENDIMENTO_HUMANO]: handleAtendimentoHumano,
    [ConversationState.ATENDIMENTO_IA]: handleAtendimentoIA,
    [ConversationState.PESQUISA_NPS]: handlePesquisaNPS,
    // ... demais estados
  };

  const handler = handlers[session.state] || handleInicio;
  await handler(session, message);
}
```

### Exemplo de Handler

```typescript
async function handleMenuPrincipal(session: Session, message: IncomingMessage): Promise<void> {
  const selectedId = message.interactive?.button_reply?.id
    || message.interactive?.list_reply?.id
    || message.text?.body?.toLowerCase();

  switch (selectedId) {
    case 'btn_suporte':
    case 'suporte_tecnico':
      session.state = ConversationState.SUPORTE_TECNICO;
      await sendText(session.phone, 'Entendido! Descreva seu problema e nossa equipe vai ajudar.');
      session.state = ConversationState.SUPORTE_AGUARDANDO_DETALHES;
      break;

    case 'btn_vendas':
    case 'suporte_comercial':
      session.state = ConversationState.VENDAS_CATALOGO;
      await sendProductCatalog(session.phone);
      break;

    case 'btn_info':
    case 'info_faq':
      await sendFAQ(session.phone);
      // Mantem no menu apos FAQ
      break;

    default:
      await sendText(session.phone, 'Desculpe, não entendi. Vou mostrar o menu novamente.');
      await sendMainMenuButtons(session.phone);
      break;
  }

  session.lastActivity = new Date();
  await saveSession(session);
}
```

---

## Gerenciamento de Sessao

### Com Redis (Producao)

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);
const SESSION_TTL = 86400; // 24 horas (janela do WhatsApp)

async function getSession(phone: string): Promise<Session> {
  const data = await redis.get(`wa_session:${phone}`);
  if (data) {
    return JSON.parse(data);
  }
  return createNewSession(phone);
}

async function saveSession(session: Session): Promise<void> {
  session.lastActivity = new Date();
  await redis.set(
    `wa_session:${session.phone}`,
    JSON.stringify(session),
    'EX',
    SESSION_TTL
  );
}

function createNewSession(phone: string): Session {
  return {
    phone,
    state: ConversationState.INICIO,
    data: {},
    lastActivity: new Date()
  };
}
```

### Com In-Memory (Desenvolvimento)

```python
from datetime import datetime, timedelta
from typing import Dict, Optional

sessions: Dict[str, dict] = {}
SESSION_TTL = timedelta(hours=24)

def get_session(phone: str) -> dict:
    session = sessions.get(phone)
    if session and datetime.now() - session["last_activity"] < SESSION_TTL:
        return session
    return create_new_session(phone)

def save_session(session: dict) -> None:
    session["last_activity"] = datetime.now()
    sessions[session["phone"]] = session

def create_new_session(phone: str) -> dict:
    session = {
        "phone": phone,
        "state": "INICIO",
        "data": {},
        "last_activity": datetime.now()
    }
    sessions[phone] = session
    return session
```

**Importante:** A janela de 24h do WhatsApp permite respostas gratuitas por 24h apos a ultima mensagem do cliente. Use o TTL da sessao alinhado com esta janela.

---

## Fila de Atendimento

### Modelo de Fila com Prioridade

```typescript
interface QueueItem {
  phone: string;
  department: string;
  priority: 'alta' | 'media' | 'baixa';
  enteredAt: Date;
  estimatedWait: number; // minutos
}

class AttendanceQueue {
  private queues: Map<string, QueueItem[]> = new Map();

  async addToQueue(item: QueueItem): Promise<number> {
    const dept = item.department;
    if (!this.queues.has(dept)) this.queues.set(dept, []);

    const queue = this.queues.get(dept)!;
    queue.push(item);

    // Ordenar por prioridade e depois por tempo de entrada
    queue.sort((a, b) => {
      const priorityOrder = { alta: 0, media: 1, baixa: 2 };
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      }
      return a.enteredAt.getTime() - b.enteredAt.getTime();
    });

    const position = queue.indexOf(item) + 1;

    // Notificar cliente da posicao
    await sendText(item.phone,
      `Você está na posição ${position} da fila do setor ${dept}. ` +
      `Tempo estimado: ~${position * 5} minutos. Aguarde!`
    );

    return position;
  }

  async getNext(department: string): Promise<QueueItem | undefined> {
    const queue = this.queues.get(department);
    return queue?.shift();
  }
}
```

### SLA e Monitoramento

```typescript
const SLA_CONFIG = {
  suporte: { maxWaitMinutes: 15, alertAfterMinutes: 10 },
  vendas: { maxWaitMinutes: 5, alertAfterMinutes: 3 },
  financeiro: { maxWaitMinutes: 20, alertAfterMinutes: 15 }
};

async function checkSLABreaches(): Promise<void> {
  for (const [dept, config] of Object.entries(SLA_CONFIG)) {
    const queue = attendanceQueue.getQueue(dept);
    for (const item of queue) {
      const waitMinutes = (Date.now() - item.enteredAt.getTime()) / 60000;
      if (waitMinutes > config.maxWaitMinutes) {
        await alertSupervisor(dept, item, waitMinutes);
      }
    }
  }
}
```

---

## Escalacao para Humano

### Detectar Necessidade de Escalacao

```typescript
const ESCALATION_TRIGGERS = [
  'falar com humano', 'falar com atendente', 'atendente',
  'pessoa real', 'humano', 'reclamacao', 'reclamar',
  'cancelar', 'cancelamento', 'insatisfeito', 'gerente'
];

function shouldEscalate(message: string): boolean {
  const lower = message.toLowerCase();
  return ESCALATION_TRIGGERS.some(trigger => lower.includes(trigger));
}

async function escalateToHuman(session: Session): Promise<void> {
  session.state = ConversationState.ATENDIMENTO_HUMANO;

  // Notificar cliente
  await sendText(session.phone,
    'Entendi! Vou transferir você para um de nossos atendentes. ' +
    'Por favor, aguarde um momento.'
  );

  // Adicionar a fila
  await attendanceQueue.addToQueue({
    phone: session.phone,
    department: session.data.department || 'geral',
    priority: session.data.isVIP ? 'alta' : 'media',
    enteredAt: new Date(),
    estimatedWait: 5
  });

  // Notificar painel de atendentes
  await notifyAgentPanel({
    type: 'new_customer',
    phone: session.phone,
    context: session.data,
    conversationHistory: session.data.history || []
  });

  await saveSession(session);
}
```

### Transferencia de Contexto

Quando um humano assume, ele deve ver o historico da conversa automatizada:

```typescript
async function buildHandoffContext(session: Session): string {
  return `
📋 Contexto da conversa:
- Cliente: ${session.phone}
- Departamento: ${session.data.department}
- Estado anterior: ${session.state}
- Problema relatado: ${session.data.problemDescription || 'Não especificado'}
- Tentativas do bot: ${session.data.botAttempts || 0}
- Tempo na conversa: ${getElapsedTime(session.data.startedAt)}

📝 Histórico resumido:
${session.data.history?.map(h => `[${h.from}] ${h.text}`).join('\n') || 'Sem histórico'}
  `.trim();
}
```

---

## Respostas Fora do Horario

```typescript
interface BusinessHours {
  timezone: string;
  schedule: Record<string, { open: string; close: string } | null>;
}

const BUSINESS_HOURS: BusinessHours = {
  timezone: 'America/Sao_Paulo',
  schedule: {
    monday: { open: '08:00', close: '18:00' },
    tuesday: { open: '08:00', close: '18:00' },
    wednesday: { open: '08:00', close: '18:00' },
    thursday: { open: '08:00', close: '18:00' },
    friday: { open: '08:00', close: '17:00' },
    saturday: { open: '09:00', close: '13:00' },
    sunday: null // fechado
  }
};

function isWithinBusinessHours(): boolean {
  const now = new Date().toLocaleString('en-US', { timeZone: BUSINESS_HOURS.timezone });
  const date = new Date(now);
  const day = date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
  const hours = BUSINESS_HOURS.schedule[day];

  if (!hours) return false;

  const currentTime = date.toTimeString().slice(0, 5);
  return currentTime >= hours.open && currentTime <= hours.close;
}

async function handleOffHours(phone: string): Promise<void> {
  // Enviar template (fora da janela de 24h pode nao ter sessao ativa)
  await sendText(phone,
    '⏰ Nosso horário de atendimento é:\n' +
    'Seg-Qui: 8h às 18h\n' +
    'Sex: 8h às 17h\n' +
    'Sáb: 9h às 13h\n\n' +
    'Deixe sua mensagem que retornaremos assim que possível!'
  );
}
```

---

## Integracao com IA (Claude API)

### Chatbot Inteligente com Claude

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

const SYSTEM_PROMPT = `Você é um assistente virtual da empresa [NOME]. Sua função é:
- Responder dúvidas sobre produtos e serviços
- Ajudar com problemas técnicos simples
- Encaminhar para atendente humano quando necessário
- Ser cordial, profissional e objetivo
- Responder em português brasileiro

Regras:
- Máximo 300 caracteres por resposta (limite do WhatsApp para boa leitura)
- Se não souber a resposta, diga que vai transferir para um especialista
- Nunca invente informações sobre preços ou disponibilidade
- Use emojis com moderação`;

async function getAIResponse(
  session: Session,
  userMessage: string
): Promise<{ text: string; shouldEscalate: boolean }> {
  const messages = (session.data.aiHistory || []).concat([
    { role: 'user', content: userMessage }
  ]);

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 300,
    system: SYSTEM_PROMPT,
    messages
  });

  const aiText = response.content[0].type === 'text'
    ? response.content[0].text
    : '';

  // Detectar se a IA sugere escalacao
  const shouldEscalate = aiText.toLowerCase().includes('transferir')
    || aiText.toLowerCase().includes('especialista')
    || aiText.toLowerCase().includes('atendente');

  // Salvar historico
  session.data.aiHistory = messages.concat([
    { role: 'assistant', content: aiText }
  ]);

  return { text: aiText, shouldEscalate };
}

async function handleAtendimentoIA(session: Session, message: IncomingMessage): Promise<void> {
  const userText = message.text?.body || '[mídia recebida]';
  const { text, shouldEscalate } = await getAIResponse(session, userText);

  await sendText(session.phone, text);

  if (shouldEscalate) {
    await escalateToHuman(session);
  }
}
```

### Limite de Tentativas do Bot

```typescript
const MAX_BOT_ATTEMPTS = 3;

async function handleWithFallback(session: Session, message: IncomingMessage): Promise<void> {
  session.data.botAttempts = (session.data.botAttempts || 0) + 1;

  if (session.data.botAttempts >= MAX_BOT_ATTEMPTS) {
    await sendText(session.phone,
      'Parece que não estou conseguindo ajudar. Vou transferir para um atendente.'
    );
    await escalateToHuman(session);
    return;
  }

  await handleAtendimentoIA(session, message);
}
```

---

## WhatsApp Flows para Formularios

WhatsApp Flows permite criar formularios interativos multi-tela. Exemplo de Flow de agendamento:

### Enviar Flow

```typescript
async function sendAppointmentFlow(to: string, flowId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'flow',
      header: { type: 'text', text: 'Agendar Consulta' },
      body: { text: 'Preencha o formulário para agendar sua consulta.' },
      footer: { text: 'Seus dados estão protegidos' },
      action: {
        name: 'flow',
        parameters: {
          flow_message_version: '3',
          flow_id: flowId,
          flow_cta: 'Agendar agora',
          flow_action: 'navigate',
          flow_action_payload: {
            screen: 'APPOINTMENT_SCREEN',
            data: {
              available_dates: ['2026-03-01', '2026-03-02', '2026-03-03']
            }
          }
        }
      }
    }
  });
}
```

### Receber Resposta do Flow

As respostas do Flow chegam via webhook como mensagem interativa:

```typescript
function handleFlowResponse(message: IncomingMessage): void {
  if (message.type === 'interactive' && message.interactive?.type === 'nfm_reply') {
    const flowResponse = JSON.parse(message.interactive.nfm_reply.response_json);
    // flowResponse contem os dados preenchidos pelo usuario
    console.log('Dados do flow:', flowResponse);
    // Ex: { date: '2026-03-01', time: '14:00', name: 'João Silva' }
  }
}
```

Para mais detalhes sobre WhatsApp Flows, leia `references/advanced-features.md`.

---

## Fluxo End-to-End Completo

### Webhook Handler Principal

```typescript
app.post('/webhook', validateHMAC, async (req, res) => {
  // Responder 200 imediatamente (requisito: < 5 segundos)
  res.sendStatus(200);

  try {
    const entry = req.body.entry?.[0];
    const changes = entry?.changes?.[0];
    const value = changes?.value;

    // Processar mensagens
    if (value?.messages) {
      for (const message of value.messages) {
        await processIncomingMessage(message);
      }
    }

    // Processar status updates
    if (value?.statuses) {
      for (const status of value.statuses) {
        await processStatusUpdate(status);
      }
    }
  } catch (error) {
    console.error('Erro ao processar webhook:', error);
    // Nao retornar erro - ja respondeu 200
  }
});

async function processIncomingMessage(message: IncomingMessage): Promise<void> {
  const phone = message.from;
  const session = await getSession(phone);

  // Marcar como lida
  await markAsRead(message.id);

  // Verificar horario de funcionamento
  if (!isWithinBusinessHours() && session.state === ConversationState.INICIO) {
    await handleOffHours(phone);
    return;
  }

  // Verificar triggers de escalacao
  if (message.text?.body && shouldEscalate(message.text.body)) {
    await escalateToHuman(session);
    await saveSession(session);
    return;
  }

  // Se e uma nova conversa, enviar menu
  if (session.state === ConversationState.INICIO) {
    session.state = ConversationState.MENU_PRINCIPAL;
    await sendMainMenuButtons(phone);
    await saveSession(session);
    return;
  }

  // Rotear para o handler correto
  await routeMessage(session, message);
}
```

Este fluxo garante:
1. Resposta HTTP 200 imediata (requisito WhatsApp)
2. Validacao HMAC de seguranca
3. Gerenciamento de sessao com estado
4. Verificacao de horario de funcionamento
5. Deteccao de escalacao
6. Roteamento por estado da conversa
7. Marcacao automatica como lida

---

## Reference: Compliance

# Compliance e Boas Praticas - WhatsApp Cloud API

Guia completo de compliance para integracoes WhatsApp Business, cobrindo LGPD, GDPR, politicas do WhatsApp, opt-in/opt-out, quality rating e tier system.

---

## Indice

1. [LGPD - Brasil](#lgpd---brasil)
2. [GDPR - Uniao Europeia](#gdpr---uniao-europeia)
3. [Politicas do WhatsApp](#politicas-do-whatsapp)
4. [Opt-in e Opt-out](#opt-in-e-opt-out)
5. [Quality Rating Dashboard](#quality-rating-dashboard)
6. [Tier System - Limites de Mensagem](#tier-system---limites-de-mensagem)
7. [Retencao e Exclusao de Dados](#retencao-e-exclusao-de-dados)
8. [Checklist de Compliance Pre-Lancamento](#checklist-de-compliance-pre-lancamento)

---

## LGPD - Brasil

A Lei Geral de Protecao de Dados (Lei 13.709/2018) se aplica a qualquer tratamento de dados pessoais realizado no Brasil.

### Base Legal para Mensagens WhatsApp

| Base Legal           | Quando Usar                                    | Exemplo                          |
|----------------------|------------------------------------------------|----------------------------------|
| Consentimento        | Marketing, promocoes, newsletters               | Campanha de Black Friday         |
| Execucao de contrato | Notificacoes de pedido, entrega, pagamento       | Confirmacao de compra            |
| Interesse legitimo   | Atendimento ao cliente, suporte                  | Resposta a duvida do cliente     |
| Obrigacao legal      | Notificacoes regulatorias                        | Aviso de recall de produto       |

### Direitos do Titular (LGPD Art. 18)

Sua integracao deve suportar:

1. **Confirmacao de tratamento** - Informar quais dados sao processados
2. **Acesso aos dados** - Fornecer copia dos dados armazenados
3. **Correcao** - Permitir atualizacao de dados incorretos
4. **Anonimizacao/exclusao** - Apagar dados quando solicitado
5. **Portabilidade** - Exportar dados em formato legivel
6. **Revogacao do consentimento** - Opt-out a qualquer momento

### Implementacao Tecnica

```typescript
// Registrar consentimento com detalhes completos
interface ConsentRecord {
  phone: string;
  consentType: 'marketing' | 'transactional' | 'support';
  method: 'whatsapp_optin' | 'website_form' | 'sms' | 'verbal';
  timestamp: Date;
  ipAddress?: string;
  message?: string; // texto exato do consentimento
  legalBasis: 'consent' | 'contract' | 'legitimate_interest';
}

async function recordConsent(record: ConsentRecord): Promise<void> {
  await db.consents.create({
    ...record,
    timestamp: new Date(),
    active: true
  });
}

// Revogar consentimento
async function revokeConsent(phone: string, type: string): Promise<void> {
  await db.consents.update(
    { phone, consentType: type },
    { active: false, revokedAt: new Date() }
  );
}
```

---

## GDPR - Uniao Europeia

Se voce atende clientes na UE, o GDPR (Regulamento 2016/679) se aplica.

### Requisitos Especificos

1. **Opt-in Duplo (Double Opt-in)**
   - Primeiro opt-in: cliente fornece numero (site, formulario, QR code)
   - Segundo opt-in: enviar mensagem de confirmacao via WhatsApp
   - Cliente responde com keyword (ex: "SIM") para confirmar

2. **BSP Certificado EU**
   - Use apenas Business Solution Providers com servidores na EU
   - A WhatsApp Cloud API da Meta e hospedada nos EUA — verifique se ha adequacao para seu caso

3. **DPA (Data Processing Agreement)**
   - Contrato formal com a Meta sobre processamento de dados
   - Disponivel em Meta Business Settings

4. **Informacao Clara ao Usuario**
   - Antes do opt-in, informar: quais dados, para que finalidade, por quanto tempo
   - Link para politica de privacidade

### Implementacao de Double Opt-in

```python
async def handle_optin_flow(phone: str, stage: str) -> None:
    if stage == "initial":
        # Primeiro contato - enviar template de confirmacao
        await send_template(
            to=phone,
            template_name="optin_confirmation",
            language="pt_BR",
            components=[{
                "type": "body",
                "parameters": [{"type": "text", "text": "mensagens promocionais"}]
            }]
        )
        await save_optin_stage(phone, "awaiting_confirmation")

    elif stage == "awaiting_confirmation":
        # Cliente respondeu - verificar keyword
        # (chamado pelo webhook handler)
        pass

async def process_optin_response(phone: str, message: str) -> None:
    keyword = message.strip().upper()
    if keyword in ["SIM", "YES", "ACEITO", "CONFIRMO"]:
        await record_consent(ConsentRecord(
            phone=phone,
            consent_type="marketing",
            method="whatsapp_double_optin",
            timestamp=datetime.now(),
            message=f"Usuario respondeu: {message}"
        ))
        await send_text(phone, "Obrigado! Voce foi inscrito com sucesso. Envie SAIR a qualquer momento para cancelar.")
    else:
        await send_text(phone, "Opt-in nao confirmado. Voce nao recebera mensagens promocionais.")
```

---

## Politicas do WhatsApp

### Conteudo Proibido

O WhatsApp proibe mensagens contendo:
- Produtos ilegais (drogas, armas, documentos falsos)
- Conteudo adulto explicito
- Jogos de azar nao regulamentados
- Esquemas de piramide ou fraude
- Conteudo que incite violencia ou odio
- Venda de dados pessoais
- Medicamentos controlados sem prescricao

### Regras de Frequencia

- Nao envie mais de 1 mensagem de marketing por semana para o mesmo usuario
- Respeite preferencias de frequencia do usuario
- Mensagens transacionais podem ser mais frequentes (conforme necessidade)
- Nunca envie mensagens em massa sem segmentacao

### Spam Signals

O WhatsApp monitora estes sinais para detectar spam:
- Taxa alta de bloqueios por usuarios
- Envio em massa para numeros que nunca interagiram
- Mensagens identicas para muitos destinatarios
- Baixa taxa de resposta/engajamento
- Reports de spam por usuarios

---

## Opt-in e Opt-out

### Metodos Validos de Opt-in

1. **Website/Landing Page** - Formulario com checkbox explicito
2. **QR Code** - Link wa.me que inicia conversa
3. **SMS** - Enviar keyword para numero curto
4. **Presencial** - Consentimento verbal registrado
5. **WhatsApp** - Double opt-in via mensagem

### Implementacao de Opt-out

```typescript
const OPTOUT_KEYWORDS = ['sair', 'stop', 'cancelar', 'parar', 'descadastrar', 'unsubscribe'];

function isOptOutRequest(message: string): boolean {
  return OPTOUT_KEYWORDS.includes(message.trim().toLowerCase());
}

async function handleOptOut(phone: string): Promise<void> {
  // 1. Revogar consentimento
  await revokeConsent(phone, 'marketing');

  // 2. Confirmar ao usuario
  await sendText(phone,
    'Voce foi descadastrado com sucesso e nao recebera mais mensagens promocionais. ' +
    'Mensagens transacionais (pedidos, entregas) continuarao sendo enviadas conforme necessario. ' +
    'Para se inscrever novamente, envie ATIVAR.'
  );

  // 3. Registrar evento
  await logEvent('optout', { phone, timestamp: new Date() });
}
```

### Registro de Comprovacao

Para cada opt-in, registre:
- **Telefone** do usuario
- **Timestamp** exato (com timezone)
- **Metodo** usado (website, QR, SMS, WhatsApp)
- **Texto exato** do consentimento apresentado
- **IP** (se via web)
- **Finalidade** especifica (marketing, transacional, suporte)

---

## Quality Rating Dashboard

### Como Acessar

WhatsApp Manager → Overview → Insights tab

### Sistema de Cores

| Cor       | Significado                          | Impacto                                  |
|-----------|--------------------------------------|------------------------------------------|
| Verde     | Alta qualidade                       | Elegivel para upgrade de tier             |
| Amarelo   | Qualidade media, atencao necessaria  | Nao perde tier, mas nao avanca            |
| Vermelho  | Qualidade baixa                      | Risco de restricao, nao avanca de tier    |

### Sinais Monitorados (ultimos 7 dias)

**Positivos:**
- Alta taxa de resposta dos clientes
- Engajamento com botoes/listas
- Conversas longas (multiplas mensagens)
- Baixa taxa de bloqueio

**Negativos:**
- Bloqueios frequentes
- Reports de spam
- Baixo engajamento
- Mensagens nao lidas

### Acoes por Rating

**Verde:** Continue como esta. Foque em manter a qualidade.

**Amarelo:**
- Revise o conteudo das mensagens de marketing
- Reduza a frequencia de envio
- Melhore a segmentacao (envie apenas para quem tem interesse)
- Verifique se o opt-out esta funcionando

**Vermelho:**
- Pare imediatamente de enviar marketing
- Revise toda a base de contatos (remova inativos)
- Verifique se ha problemas tecnicos (mensagens duplicadas)
- Foque apenas em mensagens transacionais ate recuperar

---

## Tier System - Limites de Mensagem

### Estrutura de Tiers (Atualizado Outubro 2025)

Desde outubro 2025, os limites sao por **Business Portfolio**, nao por numero individual.

| Tier         | Conversas/24h | Throughput      |
|--------------|---------------|-----------------|
| Inicial      | 250           | 80 msg/s        |
| Tier 1       | 1,000         | 80 msg/s        |
| Tier 2       | 10,000        | 80 msg/s        |
| Tier 3       | 100,000       | 80 msg/s        |
| Unlimited    | Ilimitado     | 1,000 msg/s     |

### Auto-Upgrade

O WhatsApp faz upgrade automatico quando:
1. Quality rating e verde ou amarelo
2. Voce envia para 50%+ do limite atual por 7 dias consecutivos
3. Tempo de upgrade: 6 horas (antes era 24h)

**Exemplo:** Se seu limite e 1,000, envie para 500+ clientes unicos por 7 dias para subir para 10,000.

### Mudancas 2026

- **Q1 2026:** Tiers 2K e 10K serao removidos para parceiros selecionados
- **Q2 2026:** Remocao completa — apos verificacao de negocio, limite imediato de 100K
- **Business Portfolio Pacing:** Novo recurso para campanhas em massa com pausa automatica baseada em feedback

### Regra Importante

Uma vez que voce alcanca um tier, **nao perde** mesmo se a qualidade cair. O rating afeta apenas a capacidade de subir para tiers maiores.

Se um numero no Business Portfolio ja esta em Unlimited, **todos** os novos numeros adicionados iniciam em Unlimited.

---

## Retencao e Exclusao de Dados

### Politica Recomendada

| Tipo de Dado           | Retencao Recomendada | Justificativa                    |
|------------------------|----------------------|----------------------------------|
| Mensagens de conversa  | 90 dias              | Suporte e auditoria              |
| Dados de consentimento | Enquanto ativo + 5 anos | Comprovacao legal             |
| Dados de opt-out       | 5 anos               | Evitar reenvio + comprovacao     |
| Logs de webhook        | 30 dias              | Debug e monitoramento            |
| Metricas agregadas     | 2 anos               | Analytics e melhoria             |

### Exclusao Automatica

```typescript
// Cron job diario para limpar dados antigos
async function cleanupOldData(): Promise<void> {
  const now = new Date();

  // Mensagens > 90 dias
  await db.messages.deleteMany({
    createdAt: { $lt: new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000) }
  });

  // Logs > 30 dias
  await db.webhookLogs.deleteMany({
    createdAt: { $lt: new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000) }
  });

  // Sessoes expiradas
  await db.sessions.deleteMany({
    lastActivity: { $lt: new Date(now.getTime() - 24 * 60 * 60 * 1000) }
  });
}
```

### Atender Pedido de Exclusao (LGPD/GDPR)

```typescript
async function handleDataDeletionRequest(phone: string): Promise<void> {
  // 1. Anonimizar mensagens (manter para analytics, sem PII)
  await db.messages.updateMany(
    { phone },
    { $set: { phone: 'ANONIMIZADO', content: '[REMOVIDO]' } }
  );

  // 2. Deletar dados pessoais
  await db.customers.deleteOne({ phone });
  await db.sessions.deleteOne({ phone });

  // 3. Manter registro de opt-out (para nao enviar novamente)
  await db.optouts.create({ phone, deletedAt: new Date() });

  // 4. Confirmar ao usuario
  await sendText(phone,
    'Seus dados pessoais foram removidos conforme solicitado. ' +
    'Seu número será mantido apenas em nossa lista de exclusão para garantir que não enviaremos mais mensagens.'
  );

  // 5. Log de auditoria
  await logEvent('data_deletion', { phone, timestamp: new Date() });
}
```

---

## Checklist de Compliance Pre-Lancamento

Use esta checklist antes de colocar sua integracao em producao:

### Consentimento
- [ ] Mecanismo de opt-in implementado e testado
- [ ] Double opt-in para EU/GDPR (se aplicavel)
- [ ] Registro de consentimento com timestamp, metodo e finalidade
- [ ] Consentimento especifico para cada tipo (marketing, transacional)

### Opt-out
- [ ] Keywords de opt-out reconhecidas (SAIR, STOP, CANCELAR, etc.)
- [ ] Confirmacao enviada apos opt-out
- [ ] Opt-out processado em tempo real (nao no dia seguinte)
- [ ] Base atualizada imediatamente apos opt-out

### Dados
- [ ] Politica de retencao definida e implementada
- [ ] Rotina de exclusao automatica funcionando
- [ ] Processo para atender pedidos de exclusao (LGPD Art. 18)
- [ ] Dados armazenados com seguranca (encriptacao em repouso)

### WhatsApp
- [ ] Templates aprovados antes do primeiro envio
- [ ] Verificacao de negocio completa (para limites maiores)
- [ ] Quality rating monitorado semanalmente
- [ ] Conteudo dentro das politicas do WhatsApp
- [ ] Frequencia de marketing adequada (max 1x/semana)

### Seguranca
- [ ] HMAC-SHA256 validation no webhook (OBRIGATORIO)
- [ ] Tokens armazenados em variaveis de ambiente (nunca no codigo)
- [ ] HTTPS com certificado SSL valido
- [ ] Access control: apenas pessoal autorizado acessa dados

### Documentacao
- [ ] Politica de privacidade atualizada mencionando WhatsApp
- [ ] Termos de uso incluem uso do canal WhatsApp
- [ ] DPA assinado com a Meta (para GDPR)

---

## Reference: Message Types

# WhatsApp Cloud API - Tipos de Mensagem (Referencia Completa)

> Referencia completa de todos os tipos de mensagem suportados pela WhatsApp Cloud API v21.0.
> Exemplos em Node.js/TypeScript (axios) e Python (httpx async).

**Base URL:** `https://graph.facebook.com/v21.0`

**Variaveis de ambiente necessarias:**

```env
WHATSAPP_TOKEN=seu_token_aqui
PHONE_NUMBER_ID=seu_phone_number_id
```

---

## 1. Mensagem de Texto (Text Message)

Mensagem de texto simples. Suporta ate 4096 caracteres. A opcao `preview_url` gera uma
pre-visualizacao automatica quando a mensagem contem um link.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Confira nosso site: https://exemplo.com.br"
  }
}
```

### Node.js / TypeScript

```typescript
import axios from "axios";

interface TextMessage {
  messaging_product: "whatsapp";
  recipient_type: "individual";
  to: string;
  type: "text";
  text: {
    preview_url?: boolean;
    body: string;
  };
}

async function sendTextMessage(to: string, body: string, previewUrl = false): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: TextMessage = {
    messaging_product: "whatsapp",
    recipient_type: "individual",
    to,
    type: "text",
    text: { preview_url: previewUrl, body },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
import os
import httpx

async def send_text_message(to: str, body: str, preview_url: bool = False) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": preview_url, "body": body},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["messages"][0]["id"]
```

### Resposta esperada

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{ "input": "5511999999999", "wa_id": "5511999999999" }],
  "messages": [{ "id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..." }]
}
```

### Notas

- Limite de 4096 caracteres no campo `body`.
- `preview_url: true` exige que o corpo contenha uma URL valida para gerar a pre-visualizacao.
- Formatacao suportada: `*negrito*`, `_italico_`, `~tachado~`, `` `monoespaco` ``.

---

## 2. Mensagem de Template (Template Message)

Templates sao mensagens pre-aprovadas pela Meta. Obrigatorias para iniciar conversas (fora da
janela de 24h). Suportam variaveis, cabecalhos com midia e botoes.

### 2a. Template com variaveis

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "pedido_confirmado",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "Renato" },
          { "type": "text", "text": "#12345" }
        ]
      }
    ]
  }
}
```

### 2b. Template com cabecalho de imagem

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "promo_imagem",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image",
            "image": { "link": "https://exemplo.com/banner.jpg" }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [{ "type": "text", "text": "20%" }]
      }
    ]
  }
}
```

### 2c. Template com botoes (Quick Reply + CTA)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "acompanhar_pedido",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [{ "type": "text", "text": "#12345" }]
      },
      {
        "type": "button",
        "sub_type": "quick_reply",
        "index": "0",
        "parameters": [{ "type": "payload", "payload": "SIM_CONFIRMAR" }]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": "1",
        "parameters": [{ "type": "text", "text": "12345" }]
      }
    ]
  }
}
```

### Node.js / TypeScript

```typescript
interface TemplateParameter {
  type: "text" | "image" | "document" | "video" | "payload";
  text?: string;
  payload?: string;
  image?: { link: string };
}

interface TemplateComponent {
  type: "header" | "body" | "button";
  sub_type?: "quick_reply" | "url";
  index?: string;
  parameters: TemplateParameter[];
}

interface TemplateMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "template";
  template: {
    name: string;
    language: { code: string };
    components: TemplateComponent[];
  };
}

async function sendTemplateMessage(
  to: string,
  templateName: string,
  languageCode: string,
  components: TemplateComponent[]
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: TemplateMessage = {
    messaging_product: "whatsapp",
    to,
    type: "template",
    template: {
      name: templateName,
      language: { code: languageCode },
      components,
    },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_template_message(
    to: str,
    template_name: str,
    language_code: str,
    components: list[dict],
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
            "components": components,
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Templates precisam ser aprovados no Meta Business Manager antes do uso.
- O campo `language.code` deve corresponder exatamente ao idioma aprovado (ex: `pt_BR`).
- Botoes do tipo `url` usam sufixos dinamicos: o parametro e concatenado ao final da URL base definida no template.
- Botoes do tipo `quick_reply` retornam o `payload` configurado no webhook quando clicados.
- Limite de 3 botoes quick_reply ou 2 botoes CTA por template.

---

## 3. Mensagem de Imagem (Image Message)

Envia uma imagem para o destinatario. Pode ser por URL publica ou por media ID
(apos upload previo para a API de midia).

### 3a. Via URL

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "link": "https://exemplo.com/foto.jpg",
    "caption": "Foto do produto"
  }
}
```

### 3b. Via Media ID

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "image",
  "image": {
    "id": "1234567890",
    "caption": "Foto do produto"
  }
}
```

### Node.js / TypeScript

```typescript
interface ImageMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "image";
  image: {
    link?: string;
    id?: string;
    caption?: string;
  };
}

async function sendImageMessage(
  to: string,
  source: { link: string } | { id: string },
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ImageMessage = {
    messaging_product: "whatsapp",
    to,
    type: "image",
    image: { ...source, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_image_message(
    to: str,
    source: dict,  # {"link": "..."} ou {"id": "..."}
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    image_payload = {**source}
    if caption:
        image_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": image_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Formatos suportados: JPEG, PNG.
- Tamanho maximo: 5 MB.
- A URL precisa ser publica e acessivel (sem autenticacao).
- `caption` e opcional, ate 1024 caracteres.

---

## 4. Mensagem de Documento (Document Message)

Envia documentos como PDFs, planilhas, etc. O campo `filename` define o nome exibido
para download no dispositivo do destinatario.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "document",
  "document": {
    "link": "https://exemplo.com/relatorio.pdf",
    "caption": "Relatorio mensal - Janeiro 2026",
    "filename": "relatorio-janeiro-2026.pdf"
  }
}
```

### Node.js / TypeScript

```typescript
interface DocumentMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "document";
  document: {
    link?: string;
    id?: string;
    caption?: string;
    filename?: string;
  };
}

async function sendDocumentMessage(
  to: string,
  source: { link: string } | { id: string },
  filename: string,
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: DocumentMessage = {
    messaging_product: "whatsapp",
    to,
    type: "document",
    document: { ...source, filename, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_document_message(
    to: str,
    source: dict,
    filename: str,
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    doc_payload = {**source, "filename": filename}
    if caption:
        doc_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": doc_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Formatos suportados: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT e outros.
- Tamanho maximo: 100 MB.
- `filename` e exibido no dispositivo do destinatario como nome do arquivo para download.
- `caption` e opcional, ate 1024 caracteres.

---

## 5. Mensagem de Video (Video Message)

Envia um video com legenda opcional. Util para tutoriais, demonstracoes de produto, etc.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "video",
  "video": {
    "link": "https://exemplo.com/demo.mp4",
    "caption": "Demonstracao do produto"
  }
}
```

### Node.js / TypeScript

```typescript
interface VideoMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "video";
  video: {
    link?: string;
    id?: string;
    caption?: string;
  };
}

async function sendVideoMessage(
  to: string,
  source: { link: string } | { id: string },
  caption?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: VideoMessage = {
    messaging_product: "whatsapp",
    to,
    type: "video",
    video: { ...source, caption },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_video_message(
    to: str,
    source: dict,
    caption: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    video_payload = {**source}
    if caption:
        video_payload["caption"] = caption

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "video",
        "video": video_payload,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Formatos suportados: MP4, 3GPP (somente codecs H.264 e AAC).
- Tamanho maximo: 16 MB.
- `caption` e opcional, ate 1024 caracteres.

---

## 6. Mensagem de Audio (Audio Message)

Envia uma mensagem de voz ou arquivo de audio. Reproduzido diretamente no chat como
mensagem de voz.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "audio",
  "audio": {
    "link": "https://exemplo.com/audio.ogg"
  }
}
```

### Node.js / TypeScript

```typescript
interface AudioMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "audio";
  audio: {
    link?: string;
    id?: string;
  };
}

async function sendAudioMessage(
  to: string,
  source: { link: string } | { id: string }
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: AudioMessage = {
    messaging_product: "whatsapp",
    to,
    type: "audio",
    audio: source,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_audio_message(
    to: str,
    source: dict,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": source,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Formatos suportados: OGG (com codec OPUS), MP3, AMR, AAC, M4A.
- Tamanho maximo: 16 MB.
- Audio NAO suporta `caption`.
- Arquivos `.ogg` com codec OPUS sao reproduzidos como mensagem de voz (com icone de microfone).

---

## 7. Botoes Interativos - Quick Reply (Interactive Buttons)

Exibe ate 3 botoes de resposta rapida. Quando o usuario toca em um botao, a resposta
e enviada automaticamente como mensagem de texto e o `id` do botao e retornado no webhook.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
      "type": "text",
      "text": "Confirmacao de Pedido"
    },
    "body": {
      "text": "Seu pedido #12345 esta pronto. Deseja confirmar a entrega?"
    },
    "footer": {
      "text": "Responda em ate 24h"
    },
    "action": {
      "buttons": [
        { "type": "reply", "reply": { "id": "btn_confirmar", "title": "Confirmar" } },
        { "type": "reply", "reply": { "id": "btn_reagendar", "title": "Reagendar" } },
        { "type": "reply", "reply": { "id": "btn_cancelar", "title": "Cancelar" } }
      ]
    }
  }
}
```

### Node.js / TypeScript

```typescript
interface ReplyButton {
  type: "reply";
  reply: { id: string; title: string };
}

interface InteractiveButtonMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "interactive";
  interactive: {
    type: "button";
    header?: { type: "text"; text: string };
    body: { text: string };
    footer?: { text: string };
    action: { buttons: ReplyButton[] };
  };
}

async function sendButtonMessage(
  to: string,
  body: string,
  buttons: Array<{ id: string; title: string }>,
  header?: string,
  footer?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const interactive: InteractiveButtonMessage["interactive"] = {
    type: "button",
    body: { text: body },
    action: {
      buttons: buttons.map((b) => ({
        type: "reply" as const,
        reply: { id: b.id, title: b.title },
      })),
    },
  };

  if (header) interactive.header = { type: "text", text: header };
  if (footer) interactive.footer = { text: footer };

  const payload: InteractiveButtonMessage = {
    messaging_product: "whatsapp",
    to,
    type: "interactive",
    interactive,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_button_message(
    to: str,
    body: str,
    buttons: list[dict],  # [{"id": "btn_1", "title": "Opcao 1"}, ...]
    header: str | None = None,
    footer: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    interactive: dict = {
        "type": "button",
        "body": {"text": body},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                for b in buttons
            ]
        },
    }

    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"text": footer}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": interactive,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Maximo de 3 botoes por mensagem.
- Titulo do botao: ate 20 caracteres.
- ID do botao: ate 256 caracteres.
- `body` e obrigatorio; `header` e `footer` sao opcionais.
- O `header` tambem pode ser do tipo `image`, `video` ou `document`.

---

## 8. Lista Interativa (Interactive List)

Exibe um menu com secoes e opcoes selecionaveis. Ideal para catalogos, menus de atendimento,
selecao de horarios, etc.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {
      "type": "text",
      "text": "Cardapio do Dia"
    },
    "body": {
      "text": "Escolha uma opcao do nosso cardapio:"
    },
    "footer": {
      "text": "Entrega em ate 40min"
    },
    "action": {
      "button": "Ver opcoes",
      "sections": [
        {
          "title": "Pratos Principais",
          "rows": [
            { "id": "prato_1", "title": "Frango Grelhado", "description": "Com arroz e salada - R$32" },
            { "id": "prato_2", "title": "Peixe Assado", "description": "Com pure e legumes - R$38" }
          ]
        },
        {
          "title": "Bebidas",
          "rows": [
            { "id": "bebida_1", "title": "Suco Natural", "description": "Laranja, limao ou maracuja - R$8" },
            { "id": "bebida_2", "title": "Agua Mineral", "description": "Com ou sem gas - R$5" }
          ]
        }
      ]
    }
  }
}
```

### Node.js / TypeScript

```typescript
interface ListRow {
  id: string;
  title: string;
  description?: string;
}

interface ListSection {
  title: string;
  rows: ListRow[];
}

interface InteractiveListMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "interactive";
  interactive: {
    type: "list";
    header?: { type: "text"; text: string };
    body: { text: string };
    footer?: { text: string };
    action: {
      button: string;
      sections: ListSection[];
    };
  };
}

async function sendListMessage(
  to: string,
  body: string,
  buttonText: string,
  sections: ListSection[],
  header?: string,
  footer?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const interactive: InteractiveListMessage["interactive"] = {
    type: "list",
    body: { text: body },
    action: { button: buttonText, sections },
  };

  if (header) interactive.header = { type: "text", text: header };
  if (footer) interactive.footer = { text: footer };

  const payload: InteractiveListMessage = {
    messaging_product: "whatsapp",
    to,
    type: "interactive",
    interactive,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_list_message(
    to: str,
    body: str,
    button_text: str,
    sections: list[dict],
    header: str | None = None,
    footer: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    interactive: dict = {
        "type": "list",
        "body": {"text": body},
        "action": {"button": button_text, "sections": sections},
    }

    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"text": footer}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": interactive,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- Maximo de 10 secoes.
- Maximo de 10 opcoes (rows) no total entre todas as secoes.
- Titulo da row: ate 24 caracteres.
- Descricao da row: ate 72 caracteres (opcional).
- Texto do botao (`action.button`): ate 20 caracteres.
- `header` so suporta tipo `text` em listas (sem midia).

---

## 9. Mensagem de Localizacao (Location Message)

Compartilha uma localizacao geografica com coordenadas, nome e endereco.
Util para enviar endereco de lojas, pontos de encontro, etc.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "location",
  "location": {
    "latitude": -23.5505,
    "longitude": -46.6333,
    "name": "Loja Centro SP",
    "address": "Av. Paulista, 1000 - Bela Vista, Sao Paulo - SP"
  }
}
```

### Node.js / TypeScript

```typescript
interface LocationMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "location";
  location: {
    latitude: number;
    longitude: number;
    name?: string;
    address?: string;
  };
}

async function sendLocationMessage(
  to: string,
  latitude: number,
  longitude: number,
  name?: string,
  address?: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: LocationMessage = {
    messaging_product: "whatsapp",
    to,
    type: "location",
    location: { latitude, longitude, name, address },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_location_message(
    to: str,
    latitude: float,
    longitude: float,
    name: str | None = None,
    address: str | None = None,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    location_data: dict = {"latitude": latitude, "longitude": longitude}
    if name:
        location_data["name"] = name
    if address:
        location_data["address"] = address

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "location",
        "location": location_data,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- `latitude` e `longitude` sao obrigatorios.
- `name` e `address` sao opcionais mas recomendados para melhor experiencia do usuario.
- A localizacao e exibida com um mapa integrado no WhatsApp.

---

## 10. Mensagem de Contato (Contact Message)

Compartilha um cartao de contato (vCard) com informacoes como nome, telefone, email, etc.
O destinatario pode salvar o contato diretamente na agenda.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "Suporte TechCo",
        "first_name": "Suporte",
        "last_name": "TechCo"
      },
      "phones": [
        { "phone": "+5511988887777", "type": "WORK", "wa_id": "5511988887777" }
      ],
      "emails": [
        { "email": "suporte@techco.com.br", "type": "WORK" }
      ],
      "org": {
        "company": "TechCo Solucoes"
      },
      "urls": [
        { "url": "https://techco.com.br", "type": "WORK" }
      ]
    }
  ]
}
```

### Node.js / TypeScript

```typescript
interface ContactName {
  formatted_name: string;
  first_name?: string;
  last_name?: string;
}

interface ContactPhone {
  phone: string;
  type?: "CELL" | "MAIN" | "IPHONE" | "HOME" | "WORK";
  wa_id?: string;
}

interface ContactInfo {
  name: ContactName;
  phones?: ContactPhone[];
  emails?: Array<{ email: string; type?: string }>;
  org?: { company: string };
  urls?: Array<{ url: string; type?: string }>;
}

interface ContactMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "contacts";
  contacts: ContactInfo[];
}

async function sendContactMessage(
  to: string,
  contacts: ContactInfo[]
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ContactMessage = {
    messaging_product: "whatsapp",
    to,
    type: "contacts",
    contacts,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_contact_message(
    to: str,
    contacts: list[dict],
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "contacts",
        "contacts": contacts,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- O campo `name.formatted_name` e obrigatorio.
- Pode enviar multiplos contatos em uma unica mensagem (array `contacts`).
- `wa_id` permite que o destinatario inicie conversa direto com o contato no WhatsApp.
- Campos suportados: `addresses`, `birthday`, `emails`, `name`, `org`, `phones`, `urls`.

---

## 11. Mensagem de Reacao (Reaction Message)

Reage a uma mensagem existente com um emoji. Para remover a reacao, envie com `emoji` vazio.

### Payload JSON (adicionar reacao)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "reaction",
  "reaction": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ...",
    "emoji": "\ud83d\udc4d"
  }
}
```

### Payload JSON (remover reacao)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "reaction",
  "reaction": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ...",
    "emoji": ""
  }
}
```

### Node.js / TypeScript

```typescript
interface ReactionMessage {
  messaging_product: "whatsapp";
  to: string;
  type: "reaction";
  reaction: {
    message_id: string;
    emoji: string;
  };
}

async function sendReaction(
  to: string,
  messageId: string,
  emoji: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: ReactionMessage = {
    messaging_product: "whatsapp",
    to,
    type: "reaction",
    reaction: { message_id: messageId, emoji },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}

async function removeReaction(to: string, messageId: string): Promise<string> {
  return sendReaction(to, messageId, "");
}
```

### Python

```python
async def send_reaction(to: str, message_id: str, emoji: str) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "reaction",
        "reaction": {"message_id": message_id, "emoji": emoji},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]


async def remove_reaction(to: str, message_id: str) -> str:
    return await send_reaction(to, message_id, "")
```

### Notas

- `message_id` deve ser o ID da mensagem original a qual se deseja reagir.
- Para remover uma reacao, envie `emoji` como string vazia `""`.
- Apenas um emoji por reacao por remetente por mensagem.
- Qualquer emoji Unicode e suportado.

---

## 12. Mensagem com Contexto / Resposta (Reply / Context Message)

Responde a uma mensagem especifica usando o `message_id` como contexto. A mensagem
aparece no chat do destinatario com a citacao visual da mensagem original.

Funciona com qualquer tipo de mensagem (texto, imagem, botoes, etc.) adicionando o campo `context`.

### Payload JSON (resposta de texto)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "context": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
  },
  "type": "text",
  "text": {
    "body": "Obrigado pela sua mensagem! Vamos verificar e retornar em breve."
  }
}
```

### Payload JSON (resposta com imagem)

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "context": {
    "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
  },
  "type": "image",
  "image": {
    "link": "https://exemplo.com/resposta.jpg",
    "caption": "Aqui esta a imagem solicitada"
  }
}
```

### Node.js / TypeScript

```typescript
interface ContextPayload {
  message_id: string;
}

async function sendReplyMessage(
  to: string,
  replyToMessageId: string,
  body: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload = {
    messaging_product: "whatsapp",
    to,
    context: { message_id: replyToMessageId } as ContextPayload,
    type: "text",
    text: { body },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}

// Funcao generica que adiciona contexto a qualquer payload de mensagem
async function sendWithContext<T extends Record<string, unknown>>(
  basePayload: T,
  replyToMessageId: string
): Promise<string> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload = {
    ...basePayload,
    context: { message_id: replyToMessageId },
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.messages[0].id;
}
```

### Python

```python
async def send_reply_message(
    to: str,
    reply_to_message_id: str,
    body: str,
) -> str:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "context": {"message_id": reply_to_message_id},
        "type": "text",
        "text": {"body": body},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]


async def send_with_context(
    base_payload: dict,
    reply_to_message_id: str,
) -> str:
    """Adiciona contexto de resposta a qualquer payload de mensagem."""
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {**base_payload, "context": {"message_id": reply_to_message_id}}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["messages"][0]["id"]
```

### Notas

- O campo `context.message_id` deve conter o ID da mensagem original.
- Funciona com todos os tipos de mensagem: texto, imagem, video, documento, interativos, etc.
- A mensagem original e exibida como citacao visual no chat.
- O `message_id` e obtido atraves do webhook ao receber mensagens.

---

## 13. Marcar como Lido (Mark as Read)

Marca uma mensagem recebida como lida, exibindo as marcas azuis (blue checkmarks)
no dispositivo do remetente. Tambem aciona o evento de "digitando" brevemente.

**Nota:** Este endpoint usa uma acao diferente (`"read"`) e NAO e um tipo de mensagem.

### Payload JSON

```json
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgLNTUxMTk5OTk5OTk5FQ..."
}
```

### Node.js / TypeScript

```typescript
interface MarkAsReadPayload {
  messaging_product: "whatsapp";
  status: "read";
  message_id: string;
}

async function markAsRead(messageId: string): Promise<boolean> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  const payload: MarkAsReadPayload = {
    messaging_product: "whatsapp",
    status: "read",
    message_id: messageId,
  };

  const { data } = await axios.post(url, payload, {
    headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` },
  });

  return data.success === true;
}
```

### Python

```python
async def mark_as_read(message_id: str) -> bool:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("success", False)
```

### Resposta esperada

```json
{
  "success": true
}
```

### Notas

- O `message_id` deve ser de uma mensagem RECEBIDA (nao enviada).
- Marcar como lido e idempotente: chamar mais de uma vez nao causa erro.
- Tambem dispara um breve indicador de "digitando" no chat do remetente.
- Recomenda-se marcar mensagens como lidas ao processa-las no webhook para boa experiencia do usuario.

---

## Referencia Rapida - Limites e Formatos

| Tipo          | Tamanho Max | Formatos                          | Caption |
|---------------|-------------|-----------------------------------|---------|
| Texto         | 4096 chars  | -                                 | -       |
| Imagem        | 5 MB        | JPEG, PNG                         | 1024 ch |
| Documento     | 100 MB      | PDF, DOC, XLS, PPT, TXT, etc.    | 1024 ch |
| Video         | 16 MB       | MP4, 3GPP (H.264 + AAC)          | 1024 ch |
| Audio         | 16 MB       | OGG/OPUS, MP3, AMR, AAC, M4A     | N/A     |
| Sticker       | 100 KB (s) / 500 KB (a) | WEBP                 | N/A     |

| Interativo    | Limite                                              |
|---------------|-----------------------------------------------------|
| Botoes        | 3 botoes, titulo ate 20 chars                       |
| Lista         | 10 secoes, 10 rows total, titulo ate 24 chars       |
| Reacao        | 1 emoji por remetente por mensagem                  |

---

## Tratamento de Erros Comum

Todas as funcoes acima podem lancar erros da API. Estrutura padrao de erro:

```json
{
  "error": {
    "message": "(#131030) Recipient phone number not in allowed list",
    "type": "OAuthException",
    "code": 131030,
    "error_subcode": 2655007,
    "fbtrace_id": "AbCdEfGhIjKlMnOp"
  }
}
```

### Codigos de erro frequentes

| Codigo  | Significado                                          |
|---------|------------------------------------------------------|
| 131030  | Numero do destinatario nao esta na lista permitida   |
| 131031  | Conta do remetente bloqueada                         |
| 131047  | Re-engagement message (mais de 24h sem janela)       |
| 131051  | Tipo de mensagem nao suportado                       |
| 131053  | Upload de midia falhou                               |
| 130429  | Limite de taxa (rate limit) excedido                 |
| 132000  | Quantidade de parametros do template nao confere     |
| 132015  | Template pausado/desativado                          |

### Wrapper com tratamento de erro (Node.js)

```typescript
import axios, { AxiosError } from "axios";

interface WhatsAppError {
  error: {
    message: string;
    type: string;
    code: number;
    error_subcode?: number;
    fbtrace_id: string;
  };
}

async function sendWhatsAppRequest<T>(payload: T): Promise<Record<string, unknown>> {
  const url = `https://graph.facebook.com/v21.0/${process.env.PHONE_NUMBER_ID}/messages`;

  try {
    const { data } = await axios.post(url, payload, {
      headers: {
        Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`,
        "Content-Type": "application/json",
      },
    });
    return data;
  } catch (err) {
    if (err instanceof AxiosError && err.response) {
      const waError = err.response.data as WhatsAppError;
      throw new Error(
        `WhatsApp API Error [${waError.error.code}]: ${waError.error.message}`
      );
    }
    throw err;
  }
}
```

### Wrapper com tratamento de erro (Python)

```python
import httpx


class WhatsAppAPIError(Exception):
    def __init__(self, code: int, message: str, fbtrace_id: str):
        self.code = code
        self.fbtrace_id = fbtrace_id
        super().__init__(f"WhatsApp API Error [{code}]: {message}")


async def send_whatsapp_request(payload: dict) -> dict:
    url = f"https://graph.facebook.com/v21.0/{os.environ['PHONE_NUMBER_ID']}/messages"
    headers = {
        "Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            error_data = response.json().get("error", {})
            raise WhatsAppAPIError(
                code=error_data.get("code", response.status_code),
                message=error_data.get("message", "Unknown error"),
                fbtrace_id=error_data.get("fbtrace_id", ""),
            )

        return response.json()
```

---

## Reference: Setup Guide

# Guia Completo de Setup - WhatsApp Business Cloud API

> Do zero absoluto ate o envio da primeira mensagem em producao.
> Tempo estimado: 1-2 horas (sem verificacao de negocio) | 3-7 dias (com verificacao)

---

## Pre-requisitos

- Email valido (preferencialmente corporativo)
- Documento de identidade pessoal
- Numero de telefone que **NAO esteja registrado** no WhatsApp pessoal
- CNPJ ou documento da empresa (para verificacao de negocio)
- Navegador atualizado (Chrome recomendado)

---

## Passo 1 - Criar Conta no Meta Business Suite

### URL
```
https://business.facebook.com/overview
```

### Procedimento

1. Acesse `https://business.facebook.com/overview`
2. Clique em **"Criar conta"**
3. Se voce ja tem Facebook pessoal, faca login primeiro. Caso contrario, sera pedido para criar um
4. Preencha os campos:
   - **Nome da empresa**: Use o nome oficial/fantasia do seu negocio
   - **Seu nome**: Nome do administrador da conta
   - **Email comercial**: Preferencialmente email corporativo (ex: `contato@suaempresa.com.br`)
5. Clique em **"Enviar"**
6. Acesse seu email e clique no link de confirmacao enviado pela Meta
7. Apos confirmar, voce sera redirecionado ao painel do Meta Business Suite

### Erros Comuns

| Erro | Solucao |
|------|---------|
| "Este email ja esta associado a outra conta" | Use outro email ou recupere o acesso da conta existente em `business.facebook.com/settings` |
| "Nao foi possivel criar a conta" | Desative extensoes de bloqueio de anuncios (uBlock, AdBlock) e tente novamente |
| Nao recebeu email de confirmacao | Verifique pasta de spam. Tente reenviar apos 5 minutos. Se persistir, use outro email |
| Conta bloqueada imediatamente apos criacao | Conta nova em perfil Facebook recente pode ser flagrada. Aguarde 24h e tente novamente |

### Pronto

Voce deve ter:
- Acesso ao painel em `business.facebook.com`
- Um **Business ID** visivel em `Business Settings > Business Info` (numero tipo `123456789012345`)
- Email confirmado

---

## Passo 2 - Criar App no Meta for Developers

### URL
```
https://developers.facebook.com/apps
```

### Procedimento

1. Acesse `https://developers.facebook.com/apps`
2. Se for sua primeira vez, clique em **"Comecar"** e aceite os termos de desenvolvedor
3. Clique no botao **"Criar aplicativo"**
4. Selecione o tipo de app: **"Empresa"** (Business)
   - NAO selecione "Nenhum", "Consumidor" ou "Jogos"
5. Preencha:
   - **Nome do aplicativo**: Ex: `MeuApp WhatsApp API`
   - **Email de contato**: Seu email corporativo
   - **Conta empresarial**: Selecione a conta criada no Passo 1
6. Clique em **"Criar aplicativo"**
7. Pode ser solicitado que voce digite sua senha do Facebook novamente

### Erros Comuns

| Erro | Solucao |
|------|---------|
| "Voce atingiu o limite de aplicativos" | Contas novas tem limite. Delete apps de teste antigos em `developers.facebook.com/apps` |
| Tipo "Empresa" nao aparece | Certifique-se de que sua conta Business foi criada corretamente no Passo 1 |
| "Conta empresarial nao encontrada" | Volte ao Passo 1 e verifique se a conta Business esta ativa. Tente vincular manualmente em Business Settings > Accounts > Apps |
| Erro de permissao ao criar | Verifique se voce e administrador da conta Business |

### Pronto

Voce deve ter:
- App criado e visivel em `developers.facebook.com/apps`
- Um **App ID** (numero tipo `1234567890123456`)
- Status do app como **"Em desenvolvimento"**

---

## Passo 3 - Adicionar Produto WhatsApp

### URL
```
https://developers.facebook.com/apps/{SEU_APP_ID}/dashboard/
```

### Procedimento

1. No painel do seu app, role a pagina ate a secao **"Adicionar produtos ao seu aplicativo"**
2. Localize o card **"WhatsApp"** e clique em **"Configurar"**
3. Aceite os **Termos de Servico do WhatsApp Business**
4. Selecione a **Conta empresarial** vinculada (a mesma do Passo 1)
5. Clique em **"Continuar"**
6. Voce sera redirecionado para o painel do WhatsApp dentro do seu app

### Erros Comuns

| Erro | Solucao |
|------|---------|
| Card do WhatsApp nao aparece | Verifique se o tipo do app e "Empresa". Se nao for, crie um novo app com o tipo correto |
| "Voce nao tem permissao" | Confirme que voce e admin da conta Business vinculada |
| Termos de servico nao carregam | Limpe o cache do navegador ou tente em aba anonima |
| "WhatsApp Business Account could not be created" | Sua conta Business pode ter restricoes. Verifique notificacoes em `business.facebook.com` |

### Pronto

Voce deve ter:
- Menu lateral com opcao **"WhatsApp > Configuracao"** (ou "Getting Started")
- Uma **WhatsApp Business Account (WABA)** criada automaticamente
- Acesso a pagina de Getting Started do WhatsApp

---

## Passo 4 - Obter Phone Number ID e WABA ID

### URL
```
https://developers.facebook.com/apps/{SEU_APP_ID}/whatsapp-business/wa-dev-console/
```

### Procedimento

1. No menu lateral do seu app, clique em **"WhatsApp" > "Configuracao da API"** (ou "API Setup")
2. Na secao **"Informacoes do numero de telefone"**, voce encontrara:
   - **Phone Number ID**: Identificador unico do numero (ex: `109876543210987`)
   - **WhatsApp Business Account ID (WABA ID)**: Identificador da conta Business do WhatsApp (ex: `102345678901234`)
3. Anote ambos os valores. Voce vai precisar deles para todas as chamadas de API

### Onde encontrar cada ID

```
App Dashboard
  └── WhatsApp
       └── Configuracao da API (API Setup)
            ├── Phone Number ID .... campo "Phone number ID" ou "ID do numero"
            └── WABA ID ........... campo "WhatsApp Business Account ID"
```

Alternativa para o WABA ID:
```
https://business.facebook.com/settings/whatsapp-business-accounts/
```
O ID aparece na URL ao clicar na conta ou na coluna de detalhes.

### Erros Comuns

| Erro | Solucao |
|------|---------|
| Phone Number ID nao aparece | Certifique-se de que completou o Passo 3. Tente recarregar a pagina |
| WABA ID nao visivel | Acesse via Business Settings > Accounts > WhatsApp Business Accounts |
| Valores diferentes em paginas diferentes | Use sempre os IDs que aparecem na pagina de API Setup do seu app |
| "No phone numbers" | O numero de teste ainda nao foi provisionado. Aguarde alguns minutos e recarregue |

### Pronto

Voce deve ter anotado:
- **Phone Number ID**: `___________________________`
- **WABA ID**: `___________________________`
- **App ID**: `___________________________` (do Passo 2)

---

## Passo 5 - Gerar Token Temporario de Teste

### URL
```
https://developers.facebook.com/apps/{SEU_APP_ID}/whatsapp-business/wa-dev-console/
```

### Procedimento

1. Na pagina **"Configuracao da API"** (API Setup), localize a secao **"Token de acesso temporario"**
2. Clique em **"Gerar token de acesso"** (ou o botao ao lado do campo de token)
3. Pode ser solicitado login adicional ou confirmacao
4. O token sera exibido - **copie imediatamente**

### Sobre o Token Temporario

```
IMPORTANTE:
- Expira em 24 horas (algumas vezes em 1 hora)
- Serve APENAS para testes iniciais
- NAO use em producao
- Para token permanente, veja o Passo 9
```

### Testando o token via cURL

```bash
curl -X GET \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}" \
  -H "Authorization: Bearer {SEU_TOKEN_TEMPORARIO}"
```

Resposta esperada (resumida):
```json
{
  "id": "109876543210987",
  "display_phone_number": "+1 555-XXX-XXXX",
  "verified_name": "Seu Nome de Teste"
}
```

### Erros Comuns

| Erro | Solucao |
|------|---------|
| Token nao aparece apos clicar | Desative pop-up blockers. Tente em outro navegador |
| "Error validating access token" | Token expirou. Gere um novo |
| "Invalid OAuth access token" | Copie o token novamente, sem espacos extras no inicio/fim |
| Botao de gerar desabilitado | Verifique se o produto WhatsApp foi adicionado corretamente (Passo 3) |

### Pronto

Voce deve ter:
- Um **access token temporario** copiado e salvo em local seguro
- Confirmacao via cURL de que o token funciona

---

## Passo 6 - Testar com Numero de Teste (Sandbox)

### URL
```
https://developers.facebook.com/apps/{SEU_APP_ID}/whatsapp-business/wa-dev-console/
```

### Procedimento

A Meta fornece um **numero de teste** para que voce envie mensagens sem precisar de um numero real.

1. Na pagina de API Setup, localize a secao **"Enviar e receber mensagens"**
2. O campo **"De"** ja deve mostrar o numero de teste da Meta
3. Na secao **"Para"**, clique em **"Gerenciar lista de numeros de telefone"** (ou "Manage phone number list")
4. Clique em **"Adicionar numero de telefone"**
5. Digite o numero do destinatario com codigo do pais (ex: `+5511999998888`)
6. Voce recebera um **codigo de verificacao via WhatsApp** nesse numero
7. Insira o codigo para confirmar
8. Agora envie a mensagem de teste clicando em **"Enviar mensagem"**

### Enviando via cURL

```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer {SEU_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5511999998888",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      }
    }
  }'
```

Resposta esperada:
```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "5511999998888",
      "wa_id": "5511999998888"
    }
  ],
  "messages": [
    {
      "id": "wamid.XXXXXXXXXXXXXXXX"
    }
  ]
}
```

### Limitacoes do Sandbox

- Maximo de **5 numeros de destinatario** cadastrados
- Apenas templates pre-aprovados (como `hello_world`)
- Numero remetente e o numero de teste da Meta (nao personalizavel)
- Mensagens podem demorar ate 1 minuto para chegar

### Erros Comuns

| Erro | Solucao |
|------|---------|
| `131030` - "User's phone number is part of an experiment" | Numero do destinatario pode ter restricao. Tente outro numero |
| `131026` - "Message failed to send" | Verifique se o numero do destinatario tem WhatsApp ativo |
| `100` - "Invalid parameter" | Confira o formato do numero: apenas digitos, com codigo do pais, sem `+` no JSON |
| `130429` - "Rate limit hit" | Aguarde 1 minuto e tente novamente. Sandbox tem limites rigorosos |
| Codigo de verificacao nao chega | O numero destino deve ter WhatsApp instalado e ativo |
| Template `hello_world` nao encontrado | Verifique se o idioma esta como `en_US`. Esse template vem pre-instalado |

### Pronto

Voce deve ter:
- Recebido a mensagem de teste no WhatsApp do destinatario
- Um `message_id` (wamid) retornado pela API
- Confianca de que a API esta funcionando corretamente

---

## Passo 7 - Adicionar Numero de Telefone Real

### URL
```
https://business.facebook.com/settings/whatsapp-business-accounts/{WABA_ID}/phone-numbers
```

Ou via App Dashboard:
```
https://developers.facebook.com/apps/{SEU_APP_ID}/whatsapp-business/wa-dev-console/
```

### Pre-requisito Critico

```
O numero de telefone que voce vai adicionar:
  - NAO pode estar registrado no WhatsApp pessoal
  - NAO pode estar registrado no WhatsApp Business App
  - DEVE ser capaz de receber SMS ou chamada de voz
  - PODE ser fixo (verificacao por chamada) ou movel (SMS ou chamada)

Se o numero esta no WhatsApp pessoal:
  1. Abra o WhatsApp no celular
  2. Va em Configuracoes > Conta > Excluir conta
  3. Confirme a exclusao
  4. Aguarde 5 minutos antes de prosseguir
```

### Procedimento

1. Na pagina de API Setup, clique em **"Adicionar numero de telefone"** (ou va pela URL do Business Settings)
2. Preencha as informacoes do perfil comercial:
   - **Nome de exibicao**: Nome que aparecera no WhatsApp (ex: `Minha Empresa`)
   - **Categoria**: Selecione a categoria do seu negocio
   - **Descricao** (opcional): Breve descricao da empresa
3. Clique em **"Proximo"**
4. Digite o numero com codigo do pais: `+55 11 99999-8888`
5. Selecione o metodo de verificacao (Passo 8)

### Regras do Nome de Exibicao

- Deve representar sua empresa de forma clara
- Nao pode conter apenas caracteres genericos ("Teste", "Admin")
- Nao pode violar marcas registradas
- Deve ter entre 3 e 512 caracteres
- A Meta pode rejeitar e pedir alteracao

### Erros Comuns

| Erro | Solucao |
|------|---------|
| "Este numero ja esta registrado" | O numero ainda esta no WhatsApp pessoal. Exclua a conta conforme descrito acima e aguarde |
| "Numero invalido" | Use formato internacional completo com codigo do pais |
| "Nome de exibicao rejeitado" | Use o nome oficial da empresa. Evite abreviacoes excessivas |
| "Limite de numeros atingido" | Contas nao verificadas podem ter apenas 2 numeros. Complete o Passo 10 |
| Numero fixo nao aceito | Numeros fixos sao aceitos. Selecione "Chamada de voz" como metodo de verificacao |

### Pronto

Voce deve ter:
- Numero adicionado na lista de telefones da WABA
- Proximo passo: verificacao via OTP (Passo 8)

---

## Passo 8 - Verificar Numero via OTP

### Procedimento

Continuando diretamente do Passo 7:

1. Selecione o metodo de verificacao:
   - **Mensagem de texto (SMS)**: Recomendado para numeros moveis
   - **Chamada de voz**: Necessario para numeros fixos
2. Clique em **"Enviar codigo"**
3. Aguarde receber o codigo de 6 digitos
4. Digite o codigo no campo de verificacao
5. Clique em **"Verificar"**

### Verificacao via API (alternativa)

Solicitar codigo:
```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/request_code" \
  -H "Authorization: Bearer {SEU_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "code_method": "SMS",
    "language": "pt_BR"
  }'
```

Confirmar codigo:
```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/verify_code" \
  -H "Authorization: Bearer {SEU_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "123456"
  }'
```

### Erros Comuns

| Erro | Solucao |
|------|---------|
| Codigo nao chega por SMS | Tente "Chamada de voz". Verifique se o numero nao bloqueia mensagens de servicos |
| "Codigo invalido" | Verifique se digitou corretamente. Codigos expiram em 10 minutos |
| "Muitas tentativas" | Aguarde 1 hora antes de tentar novamente. Limite de tentativas por periodo |
| Chamada de voz nao chega | Verifique se o numero aceita chamadas de numeros internacionais |
| "Phone number verification failed" | Certifique-se de que o numero nao esta em outro WhatsApp Business Account |

### Pronto

Voce deve ter:
- Numero com status **"Verificado"** (ou "Connected") no painel
- Novo **Phone Number ID** para o numero real (diferente do numero de teste)
- Capacidade de enviar mensagens usando seu proprio numero

---

## Passo 9 - Criar System User e Token Permanente

### URL
```
https://business.facebook.com/settings/system-users
```

### Por que System User?

O token temporario do Passo 5 expira rapidamente. Para producao, voce precisa de um **token permanente** vinculado a um **System User** (usuario de sistema), que nao depende de um login pessoal.

### Procedimento

#### 9.1 - Criar System User

1. Acesse `https://business.facebook.com/settings`
2. No menu lateral, clique em **"Usuarios" > "Usuarios do sistema"** (System Users)
3. Clique em **"Adicionar"**
4. Preencha:
   - **Nome**: Ex: `whatsapp-api-bot`
   - **Funcao**: Selecione **"Admin"** (necessario para permissoes completas)
5. Clique em **"Criar usuario do sistema"**

#### 9.2 - Atribuir Ativos ao System User

1. Clique no System User criado
2. Clique em **"Atribuir ativos"** (Assign Assets)
3. Selecione **"Apps"** no menu lateral
4. Encontre seu app (criado no Passo 2) e selecione-o
5. Ative **"Controle total"** (Full Control)
6. Clique em **"Salvar alteracoes"**
7. Repita para **"Contas do WhatsApp"**:
   - Selecione sua WABA
   - Ative **"Controle total"**
   - Salve

#### 9.3 - Gerar Token Permanente

1. Na pagina do System User, clique em **"Gerar novo token"**
2. Selecione o **App** (criado no Passo 2)
3. Em **"Permissoes disponíveis"**, marque:
   - `whatsapp_business_messaging` - Para enviar e receber mensagens
   - `whatsapp_business_management` - Para gerenciar conta, templates e configuracoes
4. Clique em **"Gerar token"**
5. **COPIE O TOKEN IMEDIATAMENTE** - Ele so sera exibido uma vez
6. Armazene em local seguro (gerenciador de senhas, variavel de ambiente, vault)

### Seguranca do Token

```
ATENCAO:
- O token NUNCA deve ser commitado em repositorios Git
- Use variaveis de ambiente (.env) ou servicos de secrets
- Rotacione o token periodicamente
- Se o token for comprometido, revogue imediatamente em Business Settings
```

### Testando o Token Permanente

```bash
curl -X GET \
  "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}" \
  -H "Authorization: Bearer {TOKEN_PERMANENTE}"
```

### Erros Comuns

| Erro | Solucao |
|------|---------|
| "Usuarios do sistema" nao aparece no menu | Voce precisa ser Admin da conta Business. Verifique suas permissoes |
| Permissoes `whatsapp_*` nao aparecem na lista | O produto WhatsApp nao foi adicionado ao app (volte ao Passo 3) |
| "Insufficient permissions" ao usar o token | Verifique se os ativos (App + WABA) foram atribuidos corretamente ao System User |
| Token nao funciona apos gerar | Aguarde 1-2 minutos para propagacao. Tente novamente |
| "User does not have permission" | Confira se o System User tem funcao "Admin" e controle total nos ativos |

### Pronto

Voce deve ter:
- System User criado com nome descritivo
- Ativos (App + WABA) atribuidos com controle total
- **Token permanente** copiado e armazenado com seguranca
- Token validado via chamada de API

---

## Passo 10 - Verificacao de Negocio

### URL
```
https://business.facebook.com/settings/security
```

### Por que Verificar?

Sem verificacao de negocio:
- Limite de **250 conversas iniciadas por empresa** em periodo de 24h
- Nao pode solicitar aumento de limites
- Algumas funcionalidades ficam restritas

Com verificacao:
- Limites podem ser aumentados ate **ilimitado** (progressivamente)
- Acesso a funcionalidades avancadas
- Maior confiabilidade perante a Meta

### Procedimento

1. Acesse `https://business.facebook.com/settings`
2. No menu lateral, clique em **"Central de seguranca"** (Security Center)
3. Localize a secao **"Verificacao de negocio"** e clique em **"Comecar verificacao"**
4. Preencha os dados da empresa:
   - **Nome legal da empresa**: Conforme consta no CNPJ
   - **Endereco**: Endereco oficial da empresa
   - **Telefone da empresa**: Numero comercial
   - **Site**: URL do site da empresa
   - **CNPJ**: Numero do cadastro nacional
5. Faca upload dos **documentos comprobatorios** (pelo menos um):
   - Cartao CNPJ
   - Conta de utilidade (luz, agua) no nome da empresa
   - Extrato bancario com nome e endereco da empresa
   - Alvara de funcionamento
   - Contrato social
6. Selecione o **metodo de verificacao de contato**:
   - Email do dominio da empresa (mais rapido)
   - Telefone da empresa
   - Documento adicional
7. Clique em **"Enviar"**

### Dicas para Aprovacao Rapida

- Use email com dominio da empresa (ex: `admin@suaempresa.com.br`) em vez de Gmail/Hotmail
- Certifique-se de que o nome da empresa no cadastro Meta corresponde EXATAMENTE ao nome nos documentos
- O site da empresa deve estar ativo e acessivel
- Documentos devem ser legíveis e em formato PDF ou imagem
- Documentos devem ter menos de 90 dias de emissao (para contas e extratos)

### Prazos

| Cenario | Prazo Estimado |
|---------|---------------|
| Documentacao correta + email corporativo | 1-3 dias uteis |
| Documentacao correta + verificacao por telefone | 3-5 dias uteis |
| Documentacao incompleta / rejeicao + reenvio | 5-14 dias uteis |

### Erros Comuns

| Erro | Solucao |
|------|---------|
| "Documentos rejeitados" | Verifique se o nome no documento corresponde ao nome cadastrado. Envie documentos mais recentes |
| "Nao foi possivel verificar" | Tente outro tipo de documento. Adicione mais de um documento |
| Verificacao travada ha mais de 7 dias | Abra um ticket de suporte em `business.facebook.com/help` |
| "Dominio nao verificado" | Adicione o registro TXT de verificacao no DNS do seu dominio |
| Email de verificacao nao chega | Verifique spam. Tente o metodo por telefone |

### Pronto

Voce deve ter:
- Status de verificacao como **"Verificado"** (badge verde) no Security Center
- Acesso a limites de mensagens progressivos
- Possibilidade de escalar para 1K, 10K, 100K e ilimitado

---

## Niveis de Limite de Mensagens (Pos-Verificacao)

| Nivel | Conversas Iniciadas (24h) | Como Alcancar |
|-------|---------------------------|---------------|
| Nao verificado | 250 | Padrao inicial |
| Nivel 1 | 1.000 | Verificacao de negocio completa |
| Nivel 2 | 10.000 | Enviar 2x o limite atual em 7 dias com qualidade boa |
| Nivel 3 | 100.000 | Manter qualidade e volume |
| Nivel 4 | Ilimitado | Manter qualidade consistente |

---

## Checklist Pos-Setup

Apos completar todos os 10 passos, voce deve ter os seguintes valores. Preencha e armazene em um arquivo `.env`:

```bash
# ===================================
# WhatsApp Cloud API - Variaveis de Ambiente
# ===================================

# Passo 1 - Meta Business Suite
META_BUSINESS_ID=          # ID da conta Business (15 digitos)

# Passo 2 - App no Meta for Developers
META_APP_ID=               # ID do aplicativo
META_APP_SECRET=           # Segredo do app (em App Settings > Basic)

# Passo 4 - IDs do WhatsApp
WHATSAPP_PHONE_NUMBER_ID=  # Phone Number ID (do numero real, nao do teste)
WHATSAPP_WABA_ID=          # WhatsApp Business Account ID

# Passo 9 - Token Permanente
WHATSAPP_API_TOKEN=        # Token do System User (permanente)

# Configuracoes da API
WHATSAPP_API_VERSION=v21.0
WHATSAPP_API_URL=https://graph.facebook.com

# Webhook (configurar separadamente)
WEBHOOK_VERIFY_TOKEN=      # Token que VOCE define para validar o webhook
WEBHOOK_URL=               # URL publica do seu servidor (HTTPS obrigatorio)
```

### Validacao Final

Execute este comando para validar que tudo esta funcionando:

```bash
# Substitua as variaveis pelos seus valores reais
curl -X POST \
  "https://graph.facebook.com/v21.0/${WHATSAPP_PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${WHATSAPP_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "NUMERO_DESTINATARIO",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      }
    }
  }'
```

Se voce receber um JSON com `"messages": [{"id": "wamid.XXXX"}]`, seu setup esta completo.

---

## Links Uteis

| Recurso | URL |
|---------|-----|
| Documentacao oficial | `https://developers.facebook.com/docs/whatsapp/cloud-api` |
| Referencia da API | `https://developers.facebook.com/docs/whatsapp/cloud-api/reference` |
| Status da plataforma | `https://metastatus.com` |
| Suporte Business | `https://business.facebook.com/help` |
| Comunidade de desenvolvedores | `https://developers.facebook.com/community` |
| Changelog da API | `https://developers.facebook.com/docs/whatsapp/cloud-api/changelog` |
| Guia de templates | `https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates` |
| Guia de webhooks | `https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks` |

---

> **Proximo passo**: Configure os webhooks para receber mensagens. Consulte o guia de webhooks na documentacao do projeto.

---

## Reference: Template Management

# Gerenciamento de Templates via API - WhatsApp Cloud API

Guia completo para criar, listar, deletar e gerenciar templates de mensagem programaticamente via WhatsApp Business Management API.

---

## Indice

1. [Visao Geral](#visao-geral)
2. [Categorias de Templates](#categorias-de-templates)
3. [Criar Template](#criar-template)
4. [Listar Templates](#listar-templates)
5. [Deletar Template](#deletar-template)
6. [Templates com Variaveis](#templates-com-variaveis)
7. [Templates com Midia](#templates-com-midia)
8. [Templates com Botoes](#templates-com-botoes)
9. [Enviar Template Message](#enviar-template-message)
10. [Boas Praticas](#boas-praticas)

---

## Visao Geral

Templates sao mensagens pre-aprovadas pela WhatsApp. Sao a **unica forma** de iniciar conversa com um cliente (fora da janela de 24h).

**Limites:**
- Ate 6,000 traducoes de templates por conta WABA
- Aprovacao leva de minutos a poucas horas
- Templates **nao podem ser editados** apos submissao (delete e crie novo)
- Template body: max 1,600 caracteres

**Endpoint base:** `https://graph.facebook.com/v21.0/{waba-id}/message_templates`

---

## Categorias de Templates

| Categoria      | Uso                                          | Custo              |
|----------------|----------------------------------------------|---------------------|
| MARKETING      | Promocoes, campanhas, lancamentos             | $0.025-$0.1365/msg  |
| UTILITY        | Confirmacoes de pedido, atualizacoes, tracking| $0.004-$0.0456/msg  |
| AUTHENTICATION | OTP, reset de senha, verificacao em 2 etapas  | $0.004-$0.0456/msg  |

A categoria afeta o custo e as regras de aprovacao. Templates de marketing tem regras mais rigorosas.

---

## Criar Template

### Node.js

```typescript
interface TemplateComponent {
  type: 'HEADER' | 'BODY' | 'FOOTER' | 'BUTTONS';
  format?: 'TEXT' | 'IMAGE' | 'VIDEO' | 'DOCUMENT';
  text?: string;
  example?: { header_handle?: string[]; body_text?: string[][] };
  buttons?: Array<{
    type: 'QUICK_REPLY' | 'URL' | 'PHONE_NUMBER';
    text: string;
    url?: string;
    phone_number?: string;
    example?: string[];
  }>;
}

async function createTemplate(
  name: string,
  category: 'MARKETING' | 'UTILITY' | 'AUTHENTICATION',
  language: string,
  components: TemplateComponent[]
): Promise<any> {
  const response = await axios.post(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates`,
    { name, category, language, components },
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );
  return response.data;
  // { id: "template_id", status: "PENDING", category: "UTILITY" }
}

// Exemplo: Criar template de confirmacao de pedido
await createTemplate(
  'order_confirmation_v1',
  'UTILITY',
  'pt_BR',
  [
    {
      type: 'HEADER',
      format: 'TEXT',
      text: 'Pedido Confirmado!'
    },
    {
      type: 'BODY',
      text: 'Ola {{1}}, seu pedido #{{2}} foi confirmado!\n\nValor: R$ {{3}}\nPrevisao de entrega: {{4}}',
      example: {
        body_text: [['Joao', '12345', '99,90', '3 dias uteis']]
      }
    },
    {
      type: 'FOOTER',
      text: 'Obrigado por comprar conosco!'
    }
  ]
);
```

### Python

```python
async def create_template(
    name: str,
    category: str,
    language: str,
    components: list[dict]
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            json={
                "name": name,
                "category": category,
                "language": language,
                "components": components
            },
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()

# Exemplo: Criar template de boas-vindas
await create_template(
    name="welcome_v1",
    category="MARKETING",
    language="pt_BR",
    components=[
        {
            "type": "BODY",
            "text": "Ola {{1}}, bem-vindo a nossa loja! 🎉\n\nConfira nossas ofertas exclusivas.",
            "example": {"body_text": [["Maria"]]}
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {
                    "type": "URL",
                    "text": "Ver Ofertas",
                    "url": "https://example.com/ofertas"
                },
                {
                    "type": "QUICK_REPLY",
                    "text": "Falar com Vendedor"
                }
            ]
        }
    ]
)
```

---

## Listar Templates

### Node.js

```typescript
async function listTemplates(status?: string): Promise<any[]> {
  const params = new URLSearchParams({ limit: '100' });
  if (status) params.append('status', status);

  const response = await axios.get(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates?${params}`,
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );

  return response.data.data;
}

// Listar apenas templates aprovados
const approved = await listTemplates('APPROVED');

// Listar todos
const all = await listTemplates();
```

### Python

```python
async def list_templates(status: str | None = None) -> list[dict]:
    params = {"limit": 100}
    if status:
        params["status"] = status

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            params=params,
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()["data"]
```

### Status de Template

| Status     | Significado                          |
|------------|--------------------------------------|
| APPROVED   | Aprovado e pronto para uso           |
| PENDING    | Em revisao pela WhatsApp             |
| REJECTED   | Rejeitado (ver motivo na response)   |
| PAUSED     | Pausado por baixa qualidade          |
| DISABLED   | Desabilitado                         |

---

## Deletar Template

### Node.js

```typescript
async function deleteTemplate(templateName: string): Promise<void> {
  await axios.delete(
    `${GRAPH_API}/${process.env.WABA_ID}/message_templates`,
    {
      data: { name: templateName },
      headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` }
    }
  );
}

await deleteTemplate('old_template_v1');
```

### Python

```python
async def delete_template(template_name: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.request(
            "DELETE",
            f"{GRAPH_API}/{os.environ['WABA_ID']}/message_templates",
            json={"name": template_name},
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
```

**Nota:** Deletar um template remove TODAS as traducoes associadas.

---

## Templates com Variaveis

Variaveis sao representadas por `{{N}}` (1-indexed) no texto do template.

### Regras

- Variaveis devem ser sequenciais: `{{1}}`, `{{2}}`, `{{3}}`
- Ao criar, fornecer `example` com valores de exemplo
- Ao enviar, fornecer `parameters` com valores reais
- Nao pule numeros: `{{1}}`, `{{3}}` sem `{{2}}` e invalido

### Exemplo Completo

**Criar:**
```json
{
  "type": "BODY",
  "text": "Ola {{1}}, seu pedido #{{2}} sera entregue em {{3}}.",
  "example": { "body_text": [["Joao", "12345", "2 dias"]] }
}
```

**Enviar:**
```json
{
  "type": "body",
  "parameters": [
    { "type": "text", "text": "Maria" },
    { "type": "text", "text": "67890" },
    { "type": "text", "text": "3 dias uteis" }
  ]
}
```

---

## Templates com Midia

### Header com Imagem

**Criar:**
```json
{
  "type": "HEADER",
  "format": "IMAGE",
  "example": {
    "header_handle": ["4::aW1hZ2UvanBlZw==:ARb..."]
  }
}
```

Para obter o `header_handle`, faca upload da imagem de exemplo primeiro:
```
POST /{app-id}/uploads?file_type=image/jpeg&file_length=12345
```

**Enviar:**
```json
{
  "type": "header",
  "parameters": [
    {
      "type": "image",
      "image": { "link": "https://example.com/image.jpg" }
    }
  ]
}
```

### Header com Documento

**Criar:**
```json
{
  "type": "HEADER",
  "format": "DOCUMENT",
  "example": {
    "header_handle": ["4::YXBwbGljYXRpb24vcGRm:ARb..."]
  }
}
```

**Enviar:**
```json
{
  "type": "header",
  "parameters": [
    {
      "type": "document",
      "document": {
        "link": "https://example.com/invoice.pdf",
        "filename": "Nota_Fiscal_12345.pdf"
      }
    }
  ]
}
```

---

## Templates com Botoes

### Quick Reply (ate 3 botoes)

```json
{
  "type": "BUTTONS",
  "buttons": [
    { "type": "QUICK_REPLY", "text": "Sim, confirmo" },
    { "type": "QUICK_REPLY", "text": "Nao, cancelar" },
    { "type": "QUICK_REPLY", "text": "Falar com atendente" }
  ]
}
```

### URL Button

```json
{
  "type": "BUTTONS",
  "buttons": [
    {
      "type": "URL",
      "text": "Rastrear Pedido",
      "url": "https://example.com/tracking/{{1}}",
      "example": ["12345"]
    }
  ]
}
```

### Phone Number Button

```json
{
  "type": "BUTTONS",
  "buttons": [
    {
      "type": "PHONE_NUMBER",
      "text": "Ligar para Suporte",
      "phone_number": "+5511999999999"
    }
  ]
}
```

### Enviar Template com Botao URL Dinamico

```typescript
await sendMessage({
  messaging_product: 'whatsapp',
  to: '5511999999999',
  type: 'template',
  template: {
    name: 'order_tracking_v1',
    language: { code: 'pt_BR' },
    components: [
      {
        type: 'body',
        parameters: [
          { type: 'text', text: 'Maria' },
          { type: 'text', text: '67890' }
        ]
      },
      {
        type: 'button',
        sub_type: 'url',
        index: 0,
        parameters: [
          { type: 'text', text: '67890' } // substitui {{1}} na URL
        ]
      }
    ]
  }
});
```

---

## Enviar Template Message

### Exemplo Completo - Node.js

```typescript
async function sendTemplate(
  to: string,
  templateName: string,
  language: string,
  components?: Array<{
    type: string;
    parameters?: Array<{ type: string; text?: string; image?: any; document?: any }>;
    sub_type?: string;
    index?: number;
  }>
): Promise<any> {
  const payload: any = {
    messaging_product: 'whatsapp',
    to,
    type: 'template',
    template: {
      name: templateName,
      language: { code: language }
    }
  };

  if (components) {
    payload.template.components = components;
  }

  return sendWithRetry(payload);
}

// Uso simples (sem variaveis)
await sendTemplate('5511999999999', 'hello_world', 'pt_BR');

// Com variaveis no body
await sendTemplate('5511999999999', 'order_confirmation_v1', 'pt_BR', [
  {
    type: 'body',
    parameters: [
      { type: 'text', text: 'Joao' },
      { type: 'text', text: '12345' },
      { type: 'text', text: '99,90' },
      { type: 'text', text: '3 dias uteis' }
    ]
  }
]);
```

### Exemplo Completo - Python

```python
async def send_template(
    to: str,
    template_name: str,
    language: str,
    components: list[dict] | None = None
) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language}
        }
    }

    if components:
        payload["template"]["components"] = components

    return await send_with_retry(payload)

# Uso simples
await send_template("5511999999999", "hello_world", "pt_BR")

# Com variaveis
await send_template("5511999999999", "order_confirmation_v1", "pt_BR", [
    {
        "type": "body",
        "parameters": [
            {"type": "text", "text": "Maria"},
            {"type": "text", "text": "67890"},
            {"type": "text", "text": "149,90"},
            {"type": "text", "text": "5 dias uteis"}
        ]
    }
])
```

---

## Boas Praticas

### Nomenclatura

Use um padrao consistente para nomes de templates:
```
{finalidade}_{descricao}_v{versao}
```

Exemplos:
- `order_confirmation_v1`
- `welcome_new_customer_v2`
- `payment_reminder_v1`
- `nps_survey_v3`

### Versionamento

Como templates nao podem ser editados:
1. Crie nova versao: `template_name_v2`
2. Teste a nova versao
3. Quando aprovada, migre o codigo para usar a v2
4. Delete a v1 quando nao mais necessaria

### Dicas de Aprovacao

- Evite linguagem excessivamente promocional no corpo
- Inclua exemplos claros e reais no `example`
- Nao use URLs encurtadas (bit.ly, etc.)
- Nao inclua conteudo que possa ser interpretado como spam
- Utility templates tem aprovacao mais rapida que marketing
- Use variaveis para personalizar (nome do cliente, numero do pedido)

### Monitoramento

```typescript
// Verificar status de templates periodicamente
async function monitorTemplates(): Promise<void> {
  const templates = await listTemplates();

  for (const template of templates) {
    if (template.status === 'REJECTED') {
      console.warn(`Template rejeitado: ${template.name}`);
      console.warn(`Motivo: ${template.rejected_reason}`);
    }
    if (template.status === 'PAUSED') {
      console.warn(`Template pausado por qualidade: ${template.name}`);
    }
  }
}
```

---

## Reference: Webhook Setup

# Configuracao de Webhooks - WhatsApp Cloud API

> Guia completo para configurar, validar e proteger webhooks da WhatsApp Cloud API.

---

## 1. Visao Geral

Webhooks sao callbacks HTTP que a Meta envia para o seu servidor sempre que um evento
ocorre na sua conta do WhatsApp Business. Sem webhooks, voce nao recebe mensagens,
confirmacoes de entrega nem atualizacoes de status em tempo real.

**Requisitos obrigatorios:**

| Requisito | Detalhe |
|-----------|---------|
| Protocolo | HTTPS com certificado SSL valido (nao aceita auto-assinado) |
| Resposta | HTTP 200 OK em ate **5 segundos** |
| Disponibilidade | Endpoint deve estar acessivel publicamente na internet |
| Idempotencia | A Meta pode reenviar o mesmo evento; trate duplicatas |

Se o seu servidor nao responder 200 dentro de 5 segundos, a Meta reenvia o evento
com backoff exponencial por ate 7 dias. Apos esse periodo, o webhook e desativado
automaticamente.

---

## 2. Configuracao no Meta Developers

### Passo a passo

1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Selecione seu App
3. No menu lateral: **WhatsApp > Configuration**
4. Na secao **Webhook**, clique em **Edit**

### Campos obrigatorios

| Campo | Descricao |
|-------|-----------|
| **Callback URL** | URL HTTPS do seu servidor (ex: `https://api.seudominio.com/webhook`) |
| **Verify Token** | String secreta que voce define (ex: `meu_token_secreto_2024`) |

### Campos para inscrever (Webhook Fields)

Marque pelo menos:

- **messages** - Mensagens recebidas, status de entrega, leitura

Campos opcionais uteis:

- **message_template_status_update** - Aprovacao/rejeicao de templates
- **account_update** - Alteracoes na conta Business

> **IMPORTANTE:** O Verify Token NAO e o mesmo que o Access Token da API.
> Escolha um valor forte e unico, e armazene-o como variavel de ambiente.

---

## 3. Verificacao de Webhook (GET)

Quando voce salva a configuracao no painel da Meta, ela envia um GET request para
validar que o endpoint pertence a voce. Esse fluxo e chamado de **challenge-response**.

### Fluxo de verificacao

```
Meta                            Seu Servidor
  |                                  |
  |  GET /webhook?                   |
  |    hub.mode=subscribe            |
  |    hub.verify_token=SEU_TOKEN    |
  |    hub.challenge=RANDOM_STRING   |
  |  ---------------------------->>  |
  |                                  |  1. Verifica hub.verify_token
  |                                  |  2. Se valido, retorna hub.challenge
  |  <<----------------------------  |
  |  HTTP 200 + challenge como body  |
```

### Node.js / Express

```javascript
// GET /webhook - Verification endpoint
app.get('/webhook', (req, res) => {
  const VERIFY_TOKEN = process.env.WEBHOOK_VERIFY_TOKEN;

  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === VERIFY_TOKEN) {
    console.log('Webhook verified successfully');
    return res.status(200).send(challenge);
  }

  console.error('Webhook verification failed: invalid token');
  return res.sendStatus(403);
});
```

### Python / Flask

```python
# GET /webhook - Verification endpoint
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    verify_token = os.environ.get('WEBHOOK_VERIFY_TOKEN')

    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == verify_token:
        print('Webhook verified successfully')
        return challenge, 200

    print('Webhook verification failed: invalid token')
    return 'Forbidden', 403
```

### Erros comuns na verificacao

| Erro | Causa | Solucao |
|------|-------|---------|
| 403 Forbidden | Verify token nao confere | Verifique a variavel de ambiente |
| Webhook nao valida | Challenge retornado como JSON | Retorne como **plain text**, nao JSON |
| Timeout | Servidor demorou mais de 5s | Verifique latencia e middleware |
| SSL Error | Certificado invalido ou expirado | Use Let's Encrypt ou certificado valido |

> **Erro classico:** Retornar `res.json({ challenge })` em vez de `res.send(challenge)`.
> A Meta espera o challenge como texto puro no body da resposta.

---

## 4. Recebimento de Mensagens (POST)

Apos a verificacao, a Meta envia eventos via POST. Cada payload segue a mesma
estrutura base, mas o conteudo varia conforme o tipo de evento.

### Node.js / Express - Handler completo

```javascript
// POST /webhook - Receive events
app.post('/webhook', (req, res) => {
  // SEMPRE responda 200 imediatamente
  res.sendStatus(200);

  const body = req.body;

  if (!body.object || !body.entry) return;

  for (const entry of body.entry) {
    for (const change of entry.changes) {
      if (change.field !== 'messages') continue;

      const value = change.value;
      const metadata = value.metadata;
      const phoneNumberId = metadata.phone_number_id;

      // Status updates (sent, delivered, read, failed)
      if (value.statuses) {
        for (const status of value.statuses) {
          handleStatusUpdate(status);
        }
      }

      // Incoming messages
      if (value.messages) {
        for (const message of value.messages) {
          const from = message.from;
          const timestamp = message.timestamp;

          switch (message.type) {
            case 'text':
              handleTextMessage(from, message.text.body, phoneNumberId);
              break;
            case 'image':
            case 'video':
            case 'audio':
            case 'document':
              handleMediaMessage(from, message.type, message[message.type]);
              break;
            case 'interactive':
              handleInteractiveResponse(from, message.interactive);
              break;
            case 'button':
              handleButtonResponse(from, message.button);
              break;
            case 'location':
              handleLocationMessage(from, message.location);
              break;
            default:
              console.log(`Unhandled message type: ${message.type}`);
          }
        }
      }
    }
  }
});
```

### Python / Flask - Handler completo

```python
# POST /webhook - Receive events
@app.route('/webhook', methods=['POST'])
def receive_webhook():
    body = request.get_json()

    if not body or 'entry' not in body:
        return 'OK', 200

    for entry in body.get('entry', []):
        for change in entry.get('changes', []):
            if change.get('field') != 'messages':
                continue

            value = change.get('value', {})
            metadata = value.get('metadata', {})
            phone_number_id = metadata.get('phone_number_id')

            # Status updates
            for status in value.get('statuses', []):
                handle_status_update(status)

            # Incoming messages
            for message in value.get('messages', []):
                sender = message['from']
                msg_type = message['type']

                if msg_type == 'text':
                    handle_text_message(sender, message['text']['body'], phone_number_id)
                elif msg_type in ('image', 'video', 'audio', 'document'):
                    handle_media_message(sender, msg_type, message[msg_type])
                elif msg_type == 'interactive':
                    handle_interactive_response(sender, message['interactive'])
                elif msg_type == 'button':
                    handle_button_response(sender, message['button'])
                elif msg_type == 'location':
                    handle_location_message(sender, message['location'])

    return 'OK', 200
```

### Exemplos de payload por tipo de evento

**Mensagem de texto recebida:**
```json
{
  "messages": [{
    "from": "5511999887766",
    "id": "wamid.HBgNNTUxMTk5OTg...",
    "timestamp": "1677000000",
    "type": "text",
    "text": { "body": "Ola, preciso de ajuda" }
  }]
}
```

**Resposta de botao interativo (list/button reply):**
```json
{
  "messages": [{
    "from": "5511999887766",
    "type": "interactive",
    "interactive": {
      "type": "button_reply",
      "button_reply": {
        "id": "btn_confirm",
        "title": "Confirmar pedido"
      }
    }
  }]
}
```

**Atualizacao de status (entrega):**
```json
{
  "statuses": [{
    "id": "wamid.HBgNNTUxMTk5OTg...",
    "status": "delivered",
    "timestamp": "1677000030",
    "recipient_id": "5511999887766"
  }]
}
```

---

## 5. Seguranca HMAC-SHA256 (CRITICO)

### Por que e essencial

Sem validacao de assinatura, qualquer pessoa que descubra a URL do seu webhook pode
enviar payloads falsos. Isso permite:

- **Spoofing de mensagens** - Simular que um cliente enviou algo que nunca enviou
- **Execucao de comandos** - Se o webhook dispara acoes (pagamentos, envios), atacantes controlam
- **Exfiltracao de dados** - Payloads maliciosos podem explorar falhas de parsing

> **Incidente real documentado:** Uma empresa de e-commerce sofreu prejuizo de US$ 847 mil
> apos atacantes enviarem payloads falsos de "confirmacao de pagamento" para o webhook
> que nao validava assinatura, disparando envios de mercadoria sem pagamento real.

### Como funciona

A cada request POST, a Meta inclui o header `X-Hub-Signature-256` contendo:

```
sha256=<hmac-sha256-hex-digest>
```

O HMAC e calculado usando o **App Secret** como chave e o **raw body** como mensagem.

### Passo a passo da validacao

```
1. Capture o raw body ANTES do JSON parsing
2. Extraia o header X-Hub-Signature-256
3. Compute HMAC-SHA256(app_secret, raw_body)
4. Compare usando funcao constant-time (previne timing attack)
5. Se nao bater, rejeite com 401
```

### Node.js / Express - Middleware de validacao

```javascript
const crypto = require('crypto');

function validateWebhookSignature(req, res, next) {
  const APP_SECRET = process.env.META_APP_SECRET;

  // CRITICO: raw body deve ser capturado ANTES do json parser
  // Configure o Express assim:
  // app.use(express.json({
  //   verify: (req, _res, buf) => { req.rawBody = buf; }
  // }));

  const signature = req.headers['x-hub-signature-256'];

  if (!signature) {
    console.error('Missing X-Hub-Signature-256 header');
    return res.sendStatus(401);
  }

  const expectedSignature = 'sha256=' + crypto
    .createHmac('sha256', APP_SECRET)
    .update(req.rawBody)
    .digest('hex');

  const signatureBuffer = Buffer.from(signature);
  const expectedBuffer = Buffer.from(expectedSignature);

  if (signatureBuffer.length !== expectedBuffer.length ||
      !crypto.timingSafeEqual(signatureBuffer, expectedBuffer)) {
    console.error('Invalid webhook signature');
    return res.sendStatus(401);
  }

  next();
}

// Uso:
// app.post('/webhook', validateWebhookSignature, webhookHandler);
```

### Python / Flask - Decorator de validacao

```python
import hmac
import hashlib
from functools import wraps

def validate_webhook_signature(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app_secret = os.environ.get('META_APP_SECRET')

        # CRITICO: raw body ANTES do JSON parsing
        raw_body = request.get_data()

        signature = request.headers.get('X-Hub-Signature-256', '')

        if not signature:
            print('Missing X-Hub-Signature-256 header')
            return 'Unauthorized', 401

        expected = 'sha256=' + hmac.new(
            app_secret.encode('utf-8'),
            raw_body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            print('Invalid webhook signature')
            return 'Unauthorized', 401

        return f(*args, **kwargs)
    return decorated

# Uso:
# @app.route('/webhook', methods=['POST'])
# @validate_webhook_signature
# def receive_webhook():
#     ...
```

### Erro classico: usar body parseado

```javascript
// ERRADO - body ja foi parseado para JSON, altera o conteudo
const hmac = crypto.createHmac('sha256', secret)
  .update(JSON.stringify(req.body))  // NAO FACA ISSO
  .digest('hex');

// CORRETO - usar o raw body original
const hmac = crypto.createHmac('sha256', secret)
  .update(req.rawBody)  // Buffer original do request
  .digest('hex');
```

> **Por que falha:** `JSON.stringify(JSON.parse(raw))` pode produzir output diferente
> do raw original (espacamento, ordem de chaves, encoding de caracteres Unicode).
> A assinatura da Meta foi calculada sobre o raw body exato.

---

## 6. Desenvolvimento Local

Para testar webhooks localmente, voce precisa expor seu servidor local para a internet.
A ferramenta mais usada para isso e o **ngrok**.

### Instalacao e uso do ngrok

```bash
# Instalar (macOS)
brew install ngrok

# Instalar (Windows via Chocolatey)
choco install ngrok

# Instalar (Linux)
snap install ngrok

# Autenticar (necessario uma vez)
ngrok config add-authtoken SEU_AUTH_TOKEN

# Expor porta local 3000
ngrok http 3000
```

### Saida do ngrok

```
Session Status   online
Forwarding       https://a1b2c3d4.ngrok-free.app -> http://localhost:3000
```

### Configurar no Meta Developers

1. Copie a URL HTTPS do ngrok (ex: `https://a1b2c3d4.ngrok-free.app`)
2. No painel da Meta, atualize o Callback URL para: `https://a1b2c3d4.ngrok-free.app/webhook`
3. Salve e valide

> **ATENCAO:** A URL do ngrok muda a cada reinicio (no plano gratuito).
> Voce precisara atualizar no painel da Meta toda vez que reiniciar o ngrok.

### Debugging de payloads

```bash
# O painel web do ngrok mostra todos os requests
# Acesse: http://127.0.0.1:4040

# Alternativa: log detalhado no servidor
app.post('/webhook', (req, res) => {
  console.log('Headers:', JSON.stringify(req.headers, null, 2));
  console.log('Body:', JSON.stringify(req.body, null, 2));
  res.sendStatus(200);
});
```

### Dicas para desenvolvimento local

- Use `ngrok http 3000 --log=stdout` para ver logs no terminal
- O Inspector web (`http://127.0.0.1:4040`) permite **replay** de requests
- Adicione um endpoint `/health` para verificar rapidamente se o servidor esta no ar
- Considere usar **localtunnel** como alternativa gratuita ao ngrok

---

## 7. Deploy em Producao

### Requisitos de certificado HTTPS

- Certificado SSL valido emitido por CA reconhecida
- **Let's Encrypt** e aceito e gratuito
- Certificados auto-assinados **NAO** sao aceitos
- Certifique-se de que a cadeia completa (chain) esta configurada
- Configure renovacao automatica (certbot renew via cron)

### Retry logic e idempotencia

A Meta reenvia eventos com backoff exponencial quando nao recebe HTTP 200:

| Tentativa | Intervalo aproximado |
|-----------|---------------------|
| 1a | Imediato |
| 2a | ~1 minuto |
| 3a | ~5 minutos |
| 4a | ~30 minutos |
| Seguintes | Backoff crescente ate 7 dias |

**Implemente idempotencia:**

```javascript
const processedMessages = new Set(); // Em producao, use Redis

function isNewMessage(messageId) {
  if (processedMessages.has(messageId)) {
    return false;
  }
  processedMessages.add(messageId);

  // Limpar mensagens antigas apos 24h (em producao, use TTL do Redis)
  setTimeout(() => processedMessages.delete(messageId), 86400000);
  return true;
}

// No handler:
if (!isNewMessage(message.id)) {
  console.log(`Duplicate message ${message.id}, skipping`);
  return;
}
```

### Scaling e capacidade

A Meta recomenda que o seu servidor suporte:

| Metrica | Recomendacao |
|---------|-------------|
| Capacidade de entrada | **3x** o volume de mensagens enviadas + **1x** mensagens recebidas |
| Tempo de resposta | < 5 segundos (idealmente < 1 segundo) |
| Disponibilidade | 99.9% uptime minimo |

**Arquitetura recomendada para alto volume:**

```
[Meta Webhook] --> [Load Balancer]
                        |
                   [Web Server]  --> Responde 200 imediatamente
                        |
                   [Message Queue] (Redis/SQS/RabbitMQ)
                        |
                   [Workers]  --> Processamento assincrono
```

### Monitoramento de saude do webhook

```javascript
// Endpoint de health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Metricas essenciais para monitorar:
// - Taxa de erros 4xx/5xx no endpoint /webhook
// - Latencia media de resposta (deve ser < 1s)
// - Numero de mensagens duplicadas recebidas
// - Fila de processamento (tamanho e tempo medio)
// - Falhas de validacao HMAC (possivel ataque)
```

**Alertas recomendados:**

| Alerta | Threshold | Acao |
|--------|-----------|------|
| Latencia alta | > 3 segundos | Investigar gargalos, escalar workers |
| Taxa de erro | > 1% | Verificar logs, possivel bug no handler |
| Falha HMAC | > 0 por hora | Possivel ataque; verificar APP_SECRET |
| Fila crescendo | > 1000 mensagens | Escalar workers de processamento |
| Webhook desativado | Alerta da Meta | Verificar SSL e disponibilidade |

---

## Checklist Final

- [ ] Endpoint acessivel via HTTPS com certificado valido
- [ ] Verificacao GET retorna challenge como plain text
- [ ] Handler POST responde 200 em menos de 5 segundos
- [ ] Validacao HMAC-SHA256 implementada com raw body
- [ ] Comparacao constant-time (timingSafeEqual / compare_digest)
- [ ] Idempotencia para mensagens duplicadas
- [ ] Processamento assincrono para operacoes demoradas
- [ ] Monitoramento e alertas configurados
- [ ] APP_SECRET e VERIFY_TOKEN em variaveis de ambiente (nunca no codigo)
- [ ] Logs estruturados para debugging em producao
