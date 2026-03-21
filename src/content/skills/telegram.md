---
title: "Telegram"
description: "Integracao completa com Telegram Bot API. Setup com BotFather, mensagens, webhooks, inline keyboards, grupos, canais. Boilerplates Node.js e Python."
category: "workflow"
source: "community"
author: "Community"
tags: ["telegram"]
date: 2026-03-20
---

# Telegram Bot API - Integracao Profissional

## Overview

Integracao completa com Telegram Bot API. Setup com BotFather, mensagens, webhooks, inline keyboards, grupos, canais. Boilerplates Node.js e Python.

## When to Use This Skill

- When the user mentions "telegram" or related topics
- When the user mentions "bot telegram" or related topics
- When the user mentions "telegram bot" or related topics
- When the user mentions "api telegram" or related topics
- When the user mentions "chatbot telegram" or related topics
- When the user mentions "mensagem telegram" or related topics

## Do Not Use This Skill When

- The task is unrelated to telegram
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Skill para implementar bots profissionais no Telegram usando a Bot API oficial. Suporta Node.js/TypeScript e Python.

## Overview

A Telegram Bot API permite criar bots que interagem com usuarios via mensagens, comandos, inline keyboards, pagamentos e muito mais. Bots sao criados pelo @BotFather e autenticados via token unico.

**Base URL:** `https://api.telegram.org/bot<TOKEN>/METHOD_NAME`
**Metodos HTTP:** GET e POST
**Formatos de parametros:** query string, application/x-www-form-urlencoded, application/json, multipart/form-data (uploads)
**Limite de arquivos:** 50MB download, 20MB upload (via multipart), 50MB via URL

**Portas suportadas para webhooks:** 443, 80, 88, 8443

**Pre-requisitos:**
- Conta no Telegram
- Bot criado via @BotFather (fornece o token)
- Token no formato: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

Se o usuario nao tem um bot criado, oriente a conversar com @BotFather no Telegram e enviar `/newbot`.

---

## Decision Tree

```
O usuario precisa criar um bot?
├── SIM → Secao "Setup com BotFather" abaixo
└── NAO → Qual linguagem?
    ├── Node.js/TypeScript
    └── Python
    → O que quer fazer?
       ├── Enviar mensagens → Secao "Tipos de Mensagem"
       ├── Receber mensagens → Secao "Receber Updates"
       ├── Teclados interativos → Secao "Keyboards"
       ├── Gerenciar grupos/canais → references/chat-management.md
       ├── Webhook setup → references/webhook-setup.md
       ├── Inline mode → references/advanced-features.md
       ├── Pagamentos → references/advanced-features.md
       ├── Bot de atendimento com IA → Secao "Automacao com IA"
       └── Referencia completa da API → references/api-reference.md
```

Para iniciar um projeto do zero com boilerplate pronto:
```bash
python scripts/setup_project.py --language nodejs --path ./meu-bot-telegram

## Ou

python scripts/setup_project.py --language python --path ./meu-bot-telegram
```

Para testar se o token do bot funciona:
```bash
python scripts/test_bot.py --token "SEU_TOKEN"
```

Para enviar uma mensagem de teste:
```bash
python scripts/send_message.py --token "SEU_TOKEN" --chat-id "CHAT_ID" --text "Hello!"
```

---

## Setup Com Botfather

1. Abra o Telegram e busque @BotFather
2. Envie `/newbot`
3. Escolha nome de exibicao (ex: "Meu Bot Incrivel")
4. Escolha username (deve terminar com "bot", ex: `meu_incrivel_bot`)
5. BotFather retorna o token - guarde com seguranca
6. Comandos uteis do BotFather:
   - `/setdescription` - descricao do bot
   - `/setabouttext` - texto "sobre" do bot
   - `/setuserpic` - foto de perfil
   - `/setcommands` - lista de comandos
   - `/mybots` - gerenciar bots existentes
   - `/setinline` - habilitar inline mode
   - `/setprivacy` - modo privacidade em grupos

---

## Variaveis De Ambiente

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## Node.Js/Typescript

```typescript
// Instalar: npm install node-telegram-bot-api dotenv
// Para TypeScript: npm install -D @types/node-telegram-bot-api typescript
import TelegramBot from 'node-telegram-bot-api';
import dotenv from 'dotenv';
dotenv.config();

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, 'Ola! Eu sou seu bot. Como posso ajudar?');
});

bot.on('message', (msg) => {
  if (msg.text && !msg.text.startsWith('/')) {
    bot.sendMessage(msg.chat.id, `Voce disse: ${msg.text}`);
  }
});
```

## Python

```python

## Instalar: Pip Install Python-Telegram-Bot Python-Dotenv

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ola! Eu sou seu bot. Como posso ajudar?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Voce disse: {update.message.text}')

app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()
```

## Sem Biblioteca (Http Puro)

```python
import requests

TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

## Verificar Bot

r = requests.get(f"{BASE}/getMe")
print(r.json())

## Enviar Mensagem

r = requests.post(f"{BASE}/sendMessage", json={
    "chat_id": "CHAT_ID",
    "text": "Hello from pure HTTP!",
    "parse_mode": "HTML"
})
print(r.json())
```

---

## Tipos De Mensagem

O Telegram suporta diversos tipos de conteudo. Todos os metodos aceitam `chat_id`, `reply_parameters` (para responder), `reply_markup` (para keyboards), `disable_notification` e `protect_content`.

## Html (Recomendado)

await bot.send_message(
    chat_id=chat_id,
    text="<b>Negrito</b>, <i>italico</i>, <code>codigo</code>, <a href='https://example.com'>link</a>",
    parse_mode="HTML"
)

## Markdownv2 (Escapar Caracteres Especiais: _ * [ ] ( ) ~ ` > # + - = | { } . !)

await bot.send_message(
    chat_id=chat_id,
    text="*Negrito*, _italico_, `codigo`, [link](https://example\\.com)",
    parse_mode="MarkdownV2"
)
```

## Foto (Por Url, File_Id Ou Upload)

await bot.send_photo(chat_id, photo="https://example.com/img.jpg", caption="Legenda aqui")

## Documento

await bot.send_document(chat_id, document=open("relatorio.pdf", "rb"), caption="Relatorio mensal")

## Video

await bot.send_video(chat_id, video="https://example.com/video.mp4", caption="Assista!")

## Audio

await bot.send_audio(chat_id, audio=open("musica.mp3", "rb"), title="Minha Musica")

## Voz (Ogg Com Opus)

await bot.send_voice(chat_id, voice=open("audio.ogg", "rb"))

## Localizacao

await bot.send_location(chat_id, latitude=-23.5505, longitude=-46.6333)

## Contato

await bot.send_contact(chat_id, phone_number="+5511999999999", first_name="Joao")

## Enquete

await bot.send_poll(
    chat_id, question="Qual sua cor favorita?",
    options=["Azul", "Verde", "Vermelho"],
    is_anonymous=False
)

## Grupo De Midias

await bot.send_media_group(chat_id, media=[
    InputMediaPhoto("url1", caption="Foto 1"),
    InputMediaPhoto("url2"),
    InputMediaVideo("url3")
])

## Acao De Chat (Typing, Upload_Photo, Etc.)

await bot.send_chat_action(chat_id, action="typing")
```

## Node.Js Equivalente

```typescript
// Foto
bot.sendPhoto(chatId, 'https://example.com/img.jpg', { caption: 'Legenda' });

// Documento
bot.sendDocument(chatId, fs.createReadStream('relatorio.pdf'), { caption: 'Relatorio' });

// Localizacao
bot.sendLocation(chatId, -23.5505, -46.6333);

// Enquete
bot.sendPoll(chatId, 'Qual sua cor favorita?', ['Azul', 'Verde', 'Vermelho']);
```

---

## Inline Keyboard (Botoes Dentro Da Mensagem)

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Opcao A", callback_data="opt_a"),
     InlineKeyboardButton("Opcao B", callback_data="opt_b")],
    [InlineKeyboardButton("Abrir Site", url="https://example.com")],
    [InlineKeyboardButton("Compartilhar", switch_inline_query="texto")]
])

await bot.send_message(chat_id, "Escolha uma opcao:", reply_markup=keyboard)

## Handler De Callback

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Importante: sempre responder o callback
    await query.edit_message_text(f"Voce escolheu: {query.data}")

app.add_handler(CallbackQueryHandler(button_callback))
```

## Reply Keyboard (Teclado Customizado)

```python
from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("Enviar Localizacao", request_location=True)],
     [KeyboardButton("Enviar Contato", request_contact=True)],
     ["Opcao 1", "Opcao 2"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

await bot.send_message(chat_id, "Escolha:", reply_markup=keyboard)
```

## Remover Teclado

```python
from telegram import ReplyKeyboardRemove
await bot.send_message(chat_id, "Teclado removido", reply_markup=ReplyKeyboardRemove())
```

---

## Receber Updates

Existem duas formas de receber updates: **Long Polling** e **Webhooks**.

## Long Polling (Desenvolvimento)

Mais simples, ideal para desenvolvimento. O bot faz requisicoes periodicas ao servidor do Telegram.

```python

## Python-Telegram-Bot Ja Faz Isso Automaticamente

app.run_polling(allowed_updates=Update.ALL_TYPES)
```

```typescript
// node-telegram-bot-api com polling
const bot = new TelegramBot(token, { polling: true });
```

## Webhooks (Producao)

Para producao, webhooks sao mais eficientes. O Telegram envia updates via POST para sua URL HTTPS.

Leia `references/webhook-setup.md` para configuracao completa com Express, Flask, ngrok e deploy.

Setup rapido:

```python

## Flask Webhook

from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        requests.post(f"{BASE}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"Recebi: {text}"
        })
    return "OK", 200

## Registrar Webhook

requests.post(f"{BASE}/setWebhook", json={
    "url": "https://seu-dominio.com/webhook/" + TOKEN,
    "allowed_updates": ["message", "callback_query"],
    "secret_token": "seu_secret_seguro_aqui"
})
```

---

## Comandos Do Bot

Registre comandos para aparecerem no menu do Telegram:

```python
from telegram import BotCommand

await bot.set_my_commands([
    BotCommand("start", "Iniciar o bot"),
    BotCommand("help", "Ver comandos disponiveis"),
    BotCommand("settings", "Configuracoes"),
    BotCommand("status", "Ver status do servico"),
])
```

Via HTTP:
```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{"commands":[{"command":"start","description":"Iniciar o bot"},{"command":"help","description":"Ajuda"}]}'
```

---

## Automacao Com Ia

Padrao para bot de atendimento com IA (Claude, GPT, etc.):

```python
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import anthropic  # ou openai

client = anthropic.Anthropic()
user_conversations = {}  # chat_id -> messages history

async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_text = update.message.text

    # Indicar que esta digitando
    await context.bot.send_chat_action(chat_id, "typing")

    # Manter historico
    if chat_id not in user_conversations:
        user_conversations[chat_id] = []

    user_conversations[chat_id].append({"role": "user", "content": user_text})

    # Chamar IA
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="Voce e um assistente prestativo. Responda em portugues.",
        messages=user_conversations[chat_id]
    )

    reply = response.content[0].text
    user_conversations[chat_id].append({"role": "assistant", "content": reply})

    # Limitar historico (ultimas 20 mensagens)
    if len(user_conversations[chat_id]) > 20:
        user_conversations[chat_id] = user_conversations[chat_id][-20:]

    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
app.run_polling()
```

---

## Editar Texto

await bot.edit_message_text(
    chat_id=chat_id,
    message_id=msg.message_id,
    text="Texto atualizado!",
    parse_mode="HTML"
)

## Editar Markup (Botoes)

await bot.edit_message_reply_markup(
    chat_id=chat_id,
    message_id=msg.message_id,
    reply_markup=new_keyboard
)

## Deletar Mensagem

await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

## Encaminhar Mensagem

await bot.forward_message(
    chat_id=dest_chat_id,
    from_chat_id=source_chat_id,
    message_id=msg.message_id
)
```

---

## Tratamento De Erros

```python
from telegram.error import TelegramError, BadRequest, TimedOut, NetworkError

async def safe_send(bot, chat_id, text, **kwargs):
    """Envio com retry e tratamento de erros."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await bot.send_message(chat_id, text, **kwargs)
        except TimedOut:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
        except BadRequest as e:
            if "chat not found" in str(e).lower():
                print(f"Chat {chat_id} nao encontrado")
                return None
            raise
        except NetworkError:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise
```

---

## Rate Limits

- **Mensagens em chat privado:** ~30 msg/segundo
- **Mensagens em grupo:** ~20 msg/minuto por grupo
- **Broadcast geral:** ~30 msg/segundo no total
- **Bulk notifications:** use `asyncio.sleep(0.05)` entre envios para evitar flood

Se receber erro 429 (Too Many Requests), respeite o `retry_after` retornado.

---

## Referencia De Arquivos

| Topico | Arquivo |
|--------|---------|
| Setup de webhooks | `references/webhook-setup.md` |
| Gerenciamento de chats | `references/chat-management.md` |
| Recursos avancados | `references/advanced-features.md` |
| Referencia completa da API | `references/api-reference.md` |
| Boilerplate Node.js | `assets/boilerplate/nodejs/` |
| Boilerplate Python | `assets/boilerplate/python/` |
| Exemplos de payloads | `assets/examples/` |

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
- `whatsapp-cloud-api` - Complementary skill for enhanced analysis

---

## Reference: Advanced Features

# Recursos Avancados - Telegram Bot

## Table of Contents
1. [Inline Mode](#inline-mode)
2. [Pagamentos (Telegram Stars)](#pagamentos)
3. [Mini Apps (WebApps)](#mini-apps)
4. [Conversation Handlers (FSM)](#conversation-handlers)
5. [Stickers](#stickers)
6. [Games](#games)
7. [Passport](#passport)
8. [Business Bots](#business-bots)
9. [Message Drafts (Streaming)](#streaming)

---

## Inline Mode

Permite que usuarios usem o bot em qualquer chat digitando `@seubot consulta`.

**Habilitar:** Fale com @BotFather e envie `/setinline`.

```python
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

async def inline_query(update: Update, context):
    query = update.inline_query.query
    if not query:
        return

    results = [
        InlineQueryResultArticle(
            id="1",
            title=f"Resultado para: {query}",
            input_message_content=InputTextMessageContent(
                message_text=f"Voce buscou: {query}"
            ),
            description="Clique para enviar"
        ),
        InlineQueryResultArticle(
            id="2",
            title="Busca em maiusculas",
            input_message_content=InputTextMessageContent(
                message_text=query.upper()
            )
        )
    ]

    await update.inline_query.answer(results, cache_time=10)

app.add_handler(InlineQueryHandler(inline_query))
```

### Tipos de resultado inline

- `InlineQueryResultArticle` - texto generico
- `InlineQueryResultPhoto` - foto com preview
- `InlineQueryResultGif` - GIF
- `InlineQueryResultVideo` - video
- `InlineQueryResultAudio` - audio
- `InlineQueryResultDocument` - documento
- `InlineQueryResultLocation` - localizacao
- `InlineQueryResultVenue` - local/estabelecimento
- `InlineQueryResultContact` - contato
- `InlineQueryResultCachedPhoto` - foto ja no servidor Telegram

---

## Pagamentos (Telegram Stars)

Telegram permite pagamentos via Stars (moeda interna) para bens digitais.

```python
from telegram import LabeledPrice

# Enviar invoice
await bot.send_invoice(
    chat_id=chat_id,
    title="Assinatura Premium",
    description="Acesso premium por 30 dias",
    payload="premium_30days",
    currency="XTR",  # XTR = Telegram Stars
    prices=[LabeledPrice("Assinatura Premium", 100)],  # 100 Stars
)

# Handler de pre-checkout
async def precheckout(update: Update, context):
    query = update.pre_checkout_query
    if query.invoice_payload == "premium_30days":
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Payload invalido")

# Handler de pagamento concluido
async def successful_payment(update: Update, context):
    payment = update.message.successful_payment
    await update.message.reply_text(
        f"Pagamento recebido! {payment.total_amount} Stars. "
        f"Seu acesso premium foi ativado."
    )

app.add_handler(PreCheckoutQueryHandler(precheckout))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
```

### Provedores de pagamento externos

Para bens fisicos, use provedores como Stripe, YooMoney, etc:

```python
await bot.send_invoice(
    chat_id=chat_id,
    title="Camiseta Bot Telegram",
    description="Camiseta tamanho M, algodao",
    payload="tshirt_m",
    provider_token="SEU_PROVIDER_TOKEN",  # do BotFather
    currency="BRL",
    prices=[
        LabeledPrice("Camiseta", 5990),  # R$ 59.90 (em centavos)
        LabeledPrice("Frete", 1500)       # R$ 15.00
    ],
    need_shipping_address=True,
    need_name=True,
    need_phone_number=True
)
```

---

## Mini Apps (WebApps)

Mini Apps sao aplicacoes web que rodam dentro do Telegram.

```python
from telegram import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

# Botao que abre Mini App
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        "Abrir App",
        web_app=WebAppInfo(url="https://seu-app.com")
    )]
])
await bot.send_message(chat_id, "Clique para abrir:", reply_markup=keyboard)

# Via Reply Keyboard
from telegram import ReplyKeyboardMarkup, KeyboardButton
keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("Abrir App", web_app=WebAppInfo(url="https://seu-app.com"))]
])
```

### Receber dados do Mini App

```python
async def web_app_data(update: Update, context):
    data = update.effective_message.web_app_data.data
    # data e uma string JSON enviada pelo Mini App
    import json
    parsed = json.loads(data)
    await update.message.reply_text(f"Recebi do app: {parsed}")

app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
```

---

## Conversation Handlers (FSM)

Para dialogos multi-passo (formularios, wizards):

```python
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

# Estados
NAME, AGE, CONFIRM = range(3)

async def start_form(update: Update, context):
    await update.message.reply_text("Qual seu nome?")
    return NAME

async def get_name(update: Update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Qual sua idade?")
    return AGE

async def get_age(update: Update, context):
    context.user_data['age'] = update.message.text
    name = context.user_data['name']
    age = context.user_data['age']
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Confirmar", callback_data="confirm"),
         InlineKeyboardButton("Cancelar", callback_data="cancel")]
    ])
    await update.message.reply_text(
        f"Nome: {name}\nIdade: {age}\n\nConfirma?",
        reply_markup=keyboard
    )
    return CONFIRM

async def confirm(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm":
        await query.edit_message_text("Cadastro realizado com sucesso!")
    else:
        await query.edit_message_text("Cadastro cancelado.")
    return ConversationHandler.END

async def cancel(update: Update, context):
    await update.message.reply_text("Operacao cancelada.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('cadastro', start_form)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        CONFIRM: [CallbackQueryHandler(confirm)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300  # 5 minutos timeout
)
app.add_handler(conv_handler)
```

---

## Stickers

```python
# Enviar sticker por file_id
await bot.send_sticker(chat_id, sticker="CAACAgIAAxkBAAI...")

# Obter sticker set
sticker_set = await bot.get_sticker_set("set_name")
for sticker in sticker_set.stickers:
    print(f"Emoji: {sticker.emoji}, ID: {sticker.file_id}")

# Criar sticker set (requer imagem 512x512 PNG/WEBP)
await bot.create_new_sticker_set(
    user_id=user_id,
    name="meupack_by_meubot",
    title="Meu Sticker Pack",
    stickers=[InputSticker(
        sticker=open("sticker.webp", "rb"),
        emoji_list=["😀"],
        format="static"
    )]
)

# Adicionar sticker ao set
await bot.add_sticker_to_set(
    user_id=user_id,
    name="meupack_by_meubot",
    sticker=InputSticker(
        sticker=open("sticker2.webp", "rb"),
        emoji_list=["😎"],
        format="static"
    )
)
```

---

## Games

```python
# Enviar jogo (precisa registrar no BotFather com /newgame)
await bot.send_game(chat_id, game_short_name="meu_jogo")

# Handler de callback para jogo
async def game_callback(update: Update, context):
    query = update.callback_query
    await query.answer(url="https://seu-jogo.com/?user_id=" + str(query.from_user.id))

# Salvar score
await bot.set_game_score(
    user_id=user_id,
    score=150,
    chat_id=chat_id,
    message_id=game_message_id
)

# Obter high scores
scores = await bot.get_game_high_scores(
    user_id=user_id,
    chat_id=chat_id,
    message_id=game_message_id
)
```

---

## Business Bots

Bots para contas Business do Telegram:

```python
# Receber conexao business
async def business_connection(update: Update, context):
    conn = update.business_connection
    if conn.is_enabled:
        print(f"Bot conectado ao business de {conn.user.first_name}")
    else:
        print(f"Bot desconectado do business de {conn.user.first_name}")

# Receber mensagens business
async def business_message(update: Update, context):
    msg = update.business_message
    # Responder em nome do business
    await context.bot.send_message(
        chat_id=msg.chat.id,
        text="Obrigado pela mensagem! Responderemos em breve.",
        business_connection_id=msg.business_connection_id
    )

app.add_handler(BusinessConnectionHandler(business_connection))
app.add_handler(BusinessMessagesHandler(business_message))
```

---

## Message Drafts (Streaming)

Para respostas longas (como de IA), use drafts para dar feedback em tempo real:

```python
import requests

TOKEN = "SEU_TOKEN"
BASE = f"https://api.telegram.org/bot{TOKEN}"

def stream_response(chat_id, full_text):
    """Simula streaming enviando drafts parciais."""
    words = full_text.split()
    partial = ""

    # Enviar draft inicial
    for i, word in enumerate(words):
        partial += word + " "
        if i % 5 == 0:  # Atualizar a cada 5 palavras
            requests.post(f"{BASE}/sendMessageDraft", json={
                "chat_id": chat_id,
                "text": partial.strip() + "..."
            })

    # Enviar mensagem final
    requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": full_text
    })
```

**Nota:** `sendMessageDraft` e um metodo recente. Verifique disponibilidade na versao da API que esta usando.

---

## Reference: Api Reference

# Telegram Bot API - Referencia Completa

## Table of Contents
1. [Autenticacao](#autenticacao)
2. [Metodos de Envio](#envio)
3. [Metodos de Edicao](#edicao)
4. [Metodos de Chat](#chat)
5. [Metodos de Membro](#membros)
6. [Updates e Webhooks](#updates)
7. [Bot Config](#config)
8. [Tipos Principais](#tipos)
9. [Parse Modes](#parse-modes)
10. [Codigos de Erro](#erros)

---

## Autenticacao

**Base URL:** `https://api.telegram.org/bot<TOKEN>/<METHOD>`
**File URL:** `https://api.telegram.org/file/bot<TOKEN>/<file_path>`
**Metodos:** GET e POST

Formas de enviar parametros:
- Query string: `?chat_id=123&text=hello`
- JSON body: `Content-Type: application/json`
- Form data: `Content-Type: application/x-www-form-urlencoded`
- Multipart: `Content-Type: multipart/form-data` (obrigatorio para upload de arquivos)

---

## Metodos de Envio

| Metodo | Descricao | Parametros obrigatorios |
|--------|-----------|------------------------|
| `sendMessage` | Texto | `chat_id`, `text` |
| `sendPhoto` | Foto | `chat_id`, `photo` |
| `sendVideo` | Video | `chat_id`, `video` |
| `sendAnimation` | GIF | `chat_id`, `animation` |
| `sendAudio` | Audio/musica | `chat_id`, `audio` |
| `sendDocument` | Documento | `chat_id`, `document` |
| `sendVoice` | Mensagem de voz | `chat_id`, `voice` |
| `sendVideoNote` | Video circular | `chat_id`, `video_note` |
| `sendSticker` | Sticker | `chat_id`, `sticker` |
| `sendLocation` | Localizacao | `chat_id`, `latitude`, `longitude` |
| `sendVenue` | Local | `chat_id`, `latitude`, `longitude`, `title`, `address` |
| `sendContact` | Contato | `chat_id`, `phone_number`, `first_name` |
| `sendPoll` | Enquete | `chat_id`, `question`, `options` |
| `sendDice` | Dado animado | `chat_id` |
| `sendMediaGroup` | Grupo de midias | `chat_id`, `media` |
| `sendChatAction` | Acao de digitacao | `chat_id`, `action` |
| `sendInvoice` | Fatura/pagamento | `chat_id`, `title`, `description`, `payload`, `currency`, `prices` |

### Parametros comuns a todos os metodos de envio

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `chat_id` | Integer/String | ID do chat ou @username |
| `message_thread_id` | Integer | ID do topic (em forums) |
| `parse_mode` | String | `HTML`, `MarkdownV2`, `Markdown` |
| `reply_parameters` | Object | Para responder a uma mensagem |
| `reply_markup` | Object | InlineKeyboard ou ReplyKeyboard |
| `disable_notification` | Boolean | Enviar sem notificacao |
| `protect_content` | Boolean | Impedir encaminhamento |
| `effect_id` | String | Efeito visual na mensagem |

### sendChatAction - Acoes disponiveis

`typing`, `upload_photo`, `record_video`, `upload_video`, `record_voice`, `upload_voice`, `upload_document`, `find_location`, `record_video_note`, `upload_video_note`, `choose_sticker`

---

## Metodos de Edicao

| Metodo | Descricao |
|--------|-----------|
| `editMessageText` | Editar texto |
| `editMessageCaption` | Editar legenda |
| `editMessageMedia` | Editar midia |
| `editMessageReplyMarkup` | Editar botoes |
| `deleteMessage` | Deletar mensagem |
| `deleteMessages` | Deletar varias |
| `forwardMessage` | Encaminhar |
| `forwardMessages` | Encaminhar varias |
| `copyMessage` | Copiar (sem "encaminhado de") |
| `copyMessages` | Copiar varias |

---

## Metodos de Chat

| Metodo | Descricao |
|--------|-----------|
| `getChat` | Info completa do chat |
| `getChatMemberCount` | Qtd de membros |
| `getChatAdministrators` | Lista admins |
| `setChatTitle` | Alterar titulo |
| `setChatDescription` | Alterar descricao |
| `setChatPhoto` | Alterar foto |
| `deleteChatPhoto` | Remover foto |
| `setChatPermissions` | Permissoes padrao |
| `setChatStickerSet` | Set de stickers |
| `pinChatMessage` | Fixar mensagem |
| `unpinChatMessage` | Desfixar mensagem |
| `unpinAllChatMessages` | Desfixar todas |
| `leaveChat` | Sair do chat |
| `exportChatInviteLink` | Gerar link |
| `createChatInviteLink` | Criar link customizado |
| `editChatInviteLink` | Editar link |
| `revokeChatInviteLink` | Revogar link |

---

## Metodos de Membro

| Metodo | Descricao |
|--------|-----------|
| `getChatMember` | Info de membro |
| `banChatMember` | Banir |
| `unbanChatMember` | Desbanir |
| `restrictChatMember` | Restringir |
| `promoteChatMember` | Promover a admin |
| `setChatAdministratorCustomTitle` | Titulo custom |
| `approveChatJoinRequest` | Aprovar entrada |
| `declineChatJoinRequest` | Recusar entrada |

---

## Updates e Webhooks

| Metodo | Descricao |
|--------|-----------|
| `getUpdates` | Long polling |
| `setWebhook` | Registrar webhook |
| `deleteWebhook` | Remover webhook |
| `getWebhookInfo` | Status do webhook |

### Tipos de update

`message`, `edited_message`, `channel_post`, `edited_channel_post`, `inline_query`, `chosen_inline_result`, `callback_query`, `shipping_query`, `pre_checkout_query`, `poll`, `poll_answer`, `my_chat_member`, `chat_member`, `chat_join_request`, `message_reaction`, `message_reaction_count`

---

## Bot Config

| Metodo | Descricao |
|--------|-----------|
| `getMe` | Info do bot |
| `setMyCommands` | Definir comandos |
| `getMyCommands` | Listar comandos |
| `deleteMyCommands` | Remover comandos |
| `setMyName` | Alterar nome |
| `setMyDescription` | Alterar descricao |
| `setMyShortDescription` | Descricao curta |
| `setMyDefaultAdministratorRights` | Direitos padrao |
| `setChatMenuButton` | Botao do menu |
| `setMyProfilePhoto` | Foto de perfil |

---

## Tipos Principais

### Update
```json
{
  "update_id": 123,
  "message": { ... },
  "callback_query": { ... },
  "inline_query": { ... }
}
```

### Message
```json
{
  "message_id": 1,
  "from": { "id": 123, "first_name": "User" },
  "chat": { "id": 123, "type": "private" },
  "date": 1709000000,
  "text": "Hello",
  "entities": [{ "type": "bot_command", "offset": 0, "length": 6 }]
}
```

### CallbackQuery
```json
{
  "id": "query123",
  "from": { "id": 123 },
  "message": { ... },
  "data": "callback_data_string"
}
```

### InlineKeyboardMarkup
```json
{
  "inline_keyboard": [
    [{ "text": "Button", "callback_data": "data" }],
    [{ "text": "URL", "url": "https://example.com" }]
  ]
}
```

### ReplyKeyboardMarkup
```json
{
  "keyboard": [
    [{ "text": "Option 1" }, { "text": "Option 2" }],
    [{ "text": "Send Location", "request_location": true }]
  ],
  "resize_keyboard": true,
  "one_time_keyboard": true
}
```

---

## Parse Modes

### HTML
```html
<b>bold</b>
<i>italic</i>
<u>underline</u>
<s>strikethrough</s>
<tg-spoiler>spoiler</tg-spoiler>
<code>inline code</code>
<pre>preformatted</pre>
<pre><code class="language-python">python code</code></pre>
<a href="https://example.com">link</a>
<a href="tg://user?id=123">user mention</a>
<blockquote>quote</blockquote>
```

### MarkdownV2
```
*bold*
_italic_
__underline__
~strikethrough~
||spoiler||
`inline code`
```pre block```
```python
python code
```
[link](https://example\.com)
[user](tg://user?id=123)
>blockquote
```

**Caracteres a escapar no MarkdownV2:** `_ * [ ] ( ) ~ ` > # + - = | { } . !`

---

## Codigos de Erro

| Codigo | Descricao | Acao |
|--------|-----------|------|
| 400 | Bad Request - parametros invalidos | Verificar parametros |
| 401 | Unauthorized - token invalido | Verificar token |
| 403 | Forbidden - bot bloqueado | Usuario bloqueou o bot |
| 404 | Not Found - metodo invalido | Verificar nome do metodo |
| 409 | Conflict - webhook e polling | Usar apenas um metodo |
| 429 | Too Many Requests - rate limit | Esperar `retry_after` segundos |

### Mensagens de erro comuns

- `"chat not found"` - Chat ID invalido ou bot nao foi iniciado
- `"bot was blocked by the user"` - Usuario bloqueou o bot
- `"message to edit not found"` - Mensagem ja deletada
- `"query is too old"` - Callback query expirou (responder em ate 10s)
- `"message is not modified"` - Texto igual ao anterior
- `"BUTTON_DATA_INVALID"` - callback_data > 64 bytes
- `"have no rights to send a message"` - Bot sem permissao no grupo

---

## Reference: Chat Management

# Gerenciamento de Chats - Telegram Bot

## Table of Contents
1. [Tipos de Chat](#tipos-de-chat)
2. [Informacoes do Chat](#informacoes)
3. [Gerenciamento de Membros](#membros)
4. [Moderacao](#moderacao)
5. [Configuracoes do Chat](#configuracoes)
6. [Convites](#convites)
7. [Canais](#canais)
8. [Forum Topics](#forum)

---

## Tipos de Chat

| Tipo | `chat.type` | Caracteristicas |
|------|-------------|-----------------|
| Privado | `private` | 1:1 com usuario |
| Grupo | `group` | Ate 200 membros, basico |
| Supergrupo | `supergroup` | Ate 200k membros, historico persistente |
| Canal | `channel` | Broadcast, membros ilimitados |

---

## Informacoes do Chat

```python
# Obter informacoes completas
chat = await bot.get_chat(chat_id)
print(f"Titulo: {chat.title}")
print(f"Tipo: {chat.type}")
print(f"Membros: {await bot.get_chat_member_count(chat_id)}")
print(f"Descricao: {chat.description}")

# Obter membro especifico
member = await bot.get_chat_member(chat_id, user_id)
print(f"Status: {member.status}")  # creator, administrator, member, restricted, left, kicked

# Listar administradores
admins = await bot.get_chat_administrators(chat_id)
for admin in admins:
    print(f"{admin.user.first_name}: {admin.status}")
```

---

## Gerenciamento de Membros

```python
# Banir membro (remove do grupo)
await bot.ban_chat_member(chat_id, user_id)

# Banir temporario (volta apos until_date)
from datetime import datetime, timedelta
until = datetime.now() + timedelta(hours=24)
await bot.ban_chat_member(chat_id, user_id, until_date=until)

# Desbanir
await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)

# Restringir permissoes
from telegram import ChatPermissions
await bot.restrict_chat_member(
    chat_id, user_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_photos=False,
        can_send_videos=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_invite_users=False
    ),
    until_date=until  # opcional: restricao temporaria
)

# Promover a administrador
await bot.promote_chat_member(
    chat_id, user_id,
    can_manage_chat=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_invite_users=True,
    can_pin_messages=True,
    can_manage_video_chats=True
)

# Titulo customizado para admin
await bot.set_chat_administrator_custom_title(chat_id, user_id, "Moderador")
```

---

## Moderacao

### Bot de moderacao automatica

```python
from telegram import Update, ChatPermissions
from telegram.ext import MessageHandler, filters, ContextTypes

# Lista de palavras proibidas
BANNED_WORDS = ["spam", "proibido", "blocked"]

async def moderate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text_lower = msg.text.lower()

    # Verificar palavras proibidas
    for word in BANNED_WORDS:
        if word in text_lower:
            await msg.delete()
            await context.bot.restrict_chat_member(
                msg.chat.id, msg.from_user.id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=datetime.now() + timedelta(minutes=5)
            )
            await context.bot.send_message(
                msg.chat.id,
                f"Mensagem de {msg.from_user.first_name} removida por conteudo proibido. "
                f"Silenciado por 5 minutos."
            )
            return

    # Anti-flood: max 5 msgs em 10 segundos
    user_key = f"flood_{msg.from_user.id}"
    msgs = context.bot_data.get(user_key, [])
    now = datetime.now().timestamp()
    msgs = [t for t in msgs if now - t < 10]  # ultimos 10 segundos
    msgs.append(now)
    context.bot_data[user_key] = msgs

    if len(msgs) > 5:
        await msg.delete()
        await context.bot.send_message(
            msg.chat.id,
            f"{msg.from_user.first_name}, por favor nao envie tantas mensagens seguidas."
        )

app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, moderate))
```

### Boas-vindas automaticas

```python
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        await update.message.reply_text(
            f"Bem-vindo(a), {member.first_name}! "
            f"Leia as regras com /regras antes de participar."
        )

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
```

---

## Configuracoes do Chat

```python
# Alterar titulo
await bot.set_chat_title(chat_id, "Novo Titulo do Grupo")

# Alterar descricao
await bot.set_chat_description(chat_id, "Descricao atualizada do grupo")

# Alterar foto
with open("grupo_foto.jpg", "rb") as photo:
    await bot.set_chat_photo(chat_id, photo)

# Fixar mensagem
await bot.pin_chat_message(chat_id, message_id, disable_notification=True)

# Desfixar
await bot.unpin_chat_message(chat_id, message_id)

# Desfixar todas
await bot.unpin_all_chat_messages(chat_id)

# Definir permissoes padrao
await bot.set_chat_permissions(chat_id, ChatPermissions(
    can_send_messages=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True
))
```

---

## Convites

```python
# Gerar link de convite padrao
link = await bot.export_chat_invite_link(chat_id)

# Criar link customizado
invite = await bot.create_chat_invite_link(
    chat_id,
    name="Link da Campanha Janeiro",
    expire_date=datetime(2026, 2, 28),
    member_limit=100,
    creates_join_request=False  # True = requer aprovacao
)
print(f"Link: {invite.invite_link}")

# Editar link
await bot.edit_chat_invite_link(
    chat_id,
    invite.invite_link,
    name="Link Atualizado",
    member_limit=200
)

# Revogar link
await bot.revoke_chat_invite_link(chat_id, invite.invite_link)

# Aprovar pedido de entrada
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    # Auto-aprovar (ou implementar logica customizada)
    await request.approve()
    await context.bot.send_message(
        request.from_user.id,
        f"Bem-vindo ao grupo {request.chat.title}!"
    )

app.add_handler(ChatJoinRequestHandler(handle_join_request))
```

---

## Canais

Bots em canais podem postar, editar e deletar mensagens:

```python
# Postar em canal (use o @username ou chat_id)
await bot.send_message("@meu_canal", "Post no canal!")

# Postar com botoes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Leia mais", url="https://example.com")]
])
await bot.send_message("@meu_canal", "Novo artigo!", reply_markup=keyboard)

# Editar post do canal
await bot.edit_message_text(
    "Texto atualizado",
    chat_id="@meu_canal",
    message_id=123
)

# Encaminhar do canal para grupo
await bot.forward_message(
    chat_id=group_id,
    from_chat_id="@meu_canal",
    message_id=123
)
```

---

## Forum Topics

Supergrupos com topics habilitados (tipo forum):

```python
# Criar topic
topic = await bot.create_forum_topic(
    chat_id, name="Duvidas Gerais",
    icon_color=0x6FB9F0  # Azul
)

# Enviar mensagem em topic especifico
await bot.send_message(
    chat_id, "Mensagem no topic",
    message_thread_id=topic.message_thread_id
)

# Fechar topic
await bot.close_forum_topic(chat_id, topic.message_thread_id)

# Reabrir topic
await bot.reopen_forum_topic(chat_id, topic.message_thread_id)

# Editar topic
await bot.edit_forum_topic(
    chat_id, topic.message_thread_id,
    name="Duvidas Tecnicas"
)

# Deletar topic
await bot.delete_forum_topic(chat_id, topic.message_thread_id)
```

---

## Reference: Webhook Setup

# Webhook Setup - Telegram Bot

## Table of Contents
1. [Conceitos](#conceitos)
2. [Express.js (Node.js)](#expressjs)
3. [Flask (Python)](#flask)
4. [FastAPI (Python)](#fastapi)
5. [ngrok (desenvolvimento)](#ngrok)
6. [Deploy em producao](#deploy)
7. [Seguranca](#seguranca)
8. [Troubleshooting](#troubleshooting)

---

## Conceitos

Webhooks sao a forma recomendada para producao. O Telegram envia updates via HTTP POST para sua URL HTTPS.

**Requisitos:**
- URL HTTPS valida (certificado SSL)
- Portas suportadas: 443, 80, 88, 8443
- Responder com HTTP 200 em ate 60 segundos
- Se nao responder, Telegram retenta com backoff exponencial

**Registrar webhook:**
```
POST https://api.telegram.org/bot<TOKEN>/setWebhook
{
  "url": "https://seu-dominio.com/webhook/<TOKEN>",
  "allowed_updates": ["message", "callback_query", "inline_query"],
  "max_connections": 40,
  "secret_token": "seu_token_secreto_256chars_max"
}
```

**Verificar webhook:**
```
GET https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

**Remover webhook:**
```
POST https://api.telegram.org/bot<TOKEN>/deleteWebhook
{"drop_pending_updates": true}
```

---

## Express.js

```typescript
import express from 'express';
import TelegramBot from 'node-telegram-bot-api';

const app = express();
const TOKEN = process.env.TELEGRAM_BOT_TOKEN!;
const WEBHOOK_URL = process.env.WEBHOOK_URL!; // https://seu-dominio.com
const SECRET_TOKEN = process.env.WEBHOOK_SECRET || 'meu-secret-seguro';

// Bot sem polling (webhook mode)
const bot = new TelegramBot(TOKEN);

app.use(express.json());

// Validar secret token
app.post(`/webhook/${TOKEN}`, (req, res) => {
  const secretHeader = req.headers['x-telegram-bot-api-secret-token'];
  if (secretHeader !== SECRET_TOKEN) {
    return res.sendStatus(403);
  }

  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok' }));

// Registrar webhook na inicializacao
async function start() {
  await bot.setWebHook(`${WEBHOOK_URL}/webhook/${TOKEN}`, {
    max_connections: 40,
    allowed_updates: ['message', 'callback_query'],
    secret_token: SECRET_TOKEN,
  });

  const info = await bot.getWebHookInfo();
  console.log('Webhook info:', info);

  app.listen(3000, () => console.log('Server rodando na porta 3000'));
}

// Handlers
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, 'Bot ativo via webhook!');
});

start();
```

---

## Flask

```python
import os
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SECRET_TOKEN = os.getenv('WEBHOOK_SECRET', 'meu-secret-seguro')

flask_app = Flask(__name__)

# Criar application do telegram
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text('Bot ativo via webhook!')

application.add_handler(CommandHandler('start', start))

@flask_app.route(f'/webhook/{TOKEN}', methods=['POST'])
async def webhook():
    # Validar secret token
    secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    if secret != SECRET_TOKEN:
        return 'Forbidden', 403

    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return 'OK', 200

@flask_app.route('/health')
def health():
    return jsonify(status='ok')

# Registrar webhook
import requests
requests.post(
    f'https://api.telegram.org/bot{TOKEN}/setWebhook',
    json={
        'url': f'{WEBHOOK_URL}/webhook/{TOKEN}',
        'allowed_updates': ['message', 'callback_query'],
        'secret_token': SECRET_TOKEN,
        'max_connections': 40
    }
)
```

---

## FastAPI

```python
import os
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SECRET_TOKEN = os.getenv('WEBHOOK_SECRET', 'meu-secret-seguro')

app = FastAPI()
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text('Bot ativo via FastAPI webhook!')

application.add_handler(CommandHandler('start', start))

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(
        url=f'{WEBHOOK_URL}/webhook/{TOKEN}',
        allowed_updates=['message', 'callback_query'],
        secret_token=SECRET_TOKEN
    )

@app.on_event("shutdown")
async def on_shutdown():
    await application.shutdown()

@app.post(f'/webhook/{TOKEN}')
async def webhook(request: Request):
    secret = request.headers.get('x-telegram-bot-api-secret-token')
    if secret != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail='Forbidden')

    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {'status': 'ok'}

@app.get('/health')
def health():
    return {'status': 'ok'}
```

---

## ngrok (desenvolvimento)

Para desenvolvimento local, use ngrok para expor sua porta local via HTTPS:

```bash
# Instalar ngrok: https://ngrok.com/download
ngrok http 3000
```

ngrok fornece URL tipo `https://abc123.ngrok-free.app`. Use essa URL para registrar o webhook.

```bash
curl -X POST "https://api.telegram.org/bot$TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://abc123.ngrok-free.app/webhook/$TOKEN\"}"
```

**Alternativa gratuita:** localtunnel
```bash
npx localtunnel --port 3000
```

---

## Deploy em Producao

### Railway
```bash
# railway.json
{
  "build": { "builder": "nixpacks" },
  "deploy": { "startCommand": "npm start" }
}
```

### Render
```yaml
# render.yaml
services:
  - type: web
    name: telegram-bot
    env: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

### Vercel (Serverless)
```typescript
// api/webhook.ts
import { VercelRequest, VercelResponse } from '@vercel/node';
import TelegramBot from 'node-telegram-bot-api';

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!);

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method === 'POST') {
    bot.processUpdate(req.body);
    res.status(200).send('OK');
  } else {
    res.status(200).json({ status: 'ok' });
  }
}
```

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## Seguranca

1. **Secret Token:** Sempre use `secret_token` ao registrar webhook e valide o header `X-Telegram-Bot-Api-Secret-Token`
2. **URL com token:** Inclua o token na URL do webhook para uma camada extra de seguranca
3. **IP whitelist:** Telegram envia webhooks dos IPs:
   - `149.154.160.0/20`
   - `91.108.4.0/22`
4. **HTTPS obrigatorio:** Nunca use HTTP em producao
5. **Nao exponha o token:** Use variaveis de ambiente, nunca hardcode

---

## Troubleshooting

| Problema | Causa | Solucao |
|----------|-------|---------|
| Webhook nao recebe updates | URL incorreta ou SSL invalido | Verifique com `getWebhookInfo` |
| Erro 409 Conflict | Polling e webhook ativos | Delete webhook ou pare polling |
| Erro 401 Unauthorized | Token invalido | Verifique token com `/getMe` |
| Updates duplicados | Nao retorna 200 | Garanta HTTP 200 no handler |
| `last_error_message` | Diversas | Verifique o campo em `getWebhookInfo` |
| Timeout | Handler demora >60s | Processe async, responda 200 rapido |
