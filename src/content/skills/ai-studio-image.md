---
title: "AI Studio Image"
description: "Geracao de imagens humanizadas via Google AI Studio (Gemini). Fotos realistas estilo influencer ou educacional com iluminacao natural e imperfeicoes sutis."
category: "other"
source: "community"
author: "Community"
tags: ["ai", "studio", "image"]
date: 2026-03-20
---

# AI Studio Image — Especialista em Imagens Humanizadas

## Overview

Geracao de imagens humanizadas via Google AI Studio (Gemini). Fotos realistas estilo influencer ou educacional com iluminacao natural e imperfeicoes sutis.

## When to Use This Skill

- When the user mentions "gera imagem" or related topics
- When the user mentions "gerar foto" or related topics
- When the user mentions "criar imagem" or related topics
- When the user mentions "foto realista" or related topics
- When the user mentions "imagem humanizada" or related topics
- When the user mentions "foto influencer" or related topics

## Do Not Use This Skill When

- The task is unrelated to ai studio image
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

A diferenca entre uma imagem de IA e uma foto real esta nos detalhes imperceptiveis:
a leve granulacao de um sensor de celular, a iluminacao que nao e perfeita, o enquadramento
ligeiramente descentralizado, a profundidade de campo caracteristica de uma lente pequena.
Esta skill injeta sistematicamente essas qualidades em cada geracao.

## Ai Studio Image — Especialista Em Imagens Humanizadas

Skill de geracao de imagens via Google AI Studio que transforma qualquer prompt em fotos
com aparencia genuinamente humana. Cada imagem gerada parece ter sido tirada por uma
pessoa real com seu celular — nao por uma IA.

## 1. Configurar Api Key

O usuario precisa de uma API key do Google AI Studio:
- Acesse https://aistudio.google.com/apikey
- Crie ou copie sua API key
- Configure como variavel de ambiente:

```bash

## Windows

set GEMINI_API_KEY=sua-api-key-aqui

## Linux/Mac

export GEMINI_API_KEY=sua-api-key-aqui
```

Ou crie um arquivo `.env` em `C:\Users\renat\skills\ai-studio-image\`:
```
GEMINI_API_KEY=sua-api-key-aqui
```

## 2. Instalar Dependencias

```bash
pip install -r C:\Users\renat\skills\ai-studio-image\scripts\requirements.txt
```

## 3. Gerar Sua Primeira Imagem

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py --prompt "mulher jovem tomando cafe em cafeteria" --mode influencer --format square
```

## Workflow Principal

Quando o usuario pedir para gerar uma imagem, siga este fluxo:

## Passo 1: Identificar O Modo

Pergunte ou deduza pelo contexto:

| Modo | Quando Usar | Caracteristicas |
|------|-------------|-----------------|
| **influencer** | Posts de redes sociais, lifestyle, branding pessoal | Estetica atraente mas natural, cores vibrantes sem saturacao excessiva, composicao que prende atencao |
| **educacional** | Material de curso, tutorial, apresentacao, infografico | Visual limpo, profissional, foco no conteudo, elementos claros e legiveis |

Se o usuario nao especificar, use **influencer** como padrao para conteudo de redes sociais
e **educacional** para qualquer coisa relacionada a ensino/apresentacao.

## Passo 2: Identificar O Formato

| Formato | Aspect Ratio | Uso Ideal |
|---------|-------------|-----------|
| `square` | 1:1 | Feed Instagram, Facebook, perfis |
| `portrait` | 3:4 | Instagram portrait, Pinterest |
| `landscape` | 16:9 | YouTube thumbnails, banners, desktop |
| `stories` | 9:16 | Instagram/Facebook Stories, TikTok, Reels |

Se nao especificado, deduza pelo contexto (stories → 9:16, feed → 1:1, etc).

## Passo 3: Transformar O Prompt

**Esta e a etapa mais importante.** Nunca envie o prompt do usuario diretamente para a API.
Sempre passe pelo motor de humanizacao:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\prompt_engine.py --prompt "prompt do usuario" --mode influencer
```

O motor de humanizacao adiciona camadas de realismo:

**Camada 1 — Dispositivo e Tecnica:**
- Fotografado com smartphone (iPhone/Samsung Galaxy)
- Lente de celular com profundidade de campo natural
- Sem flash — apenas luz ambiente
- Leve ruido de sensor (ISO elevado em baixa luz)

**Camada 2 — Iluminacao Natural:**
- Luz do sol indireta / golden hour / luz de janela
- Sombras suaves e organicas
- Sem iluminacao de estudio
- Reflexos naturais em superficies

**Camada 3 — Imperfeicoes Humanas:**
- Enquadramento ligeiramente imperfeito (nao centralizado matematicamente)
- Foco seletivo natural (algo levemente fora de foco no background)
- Micro-tremor de maos (nitidez nao e absoluta)
- Elementos aleatorios do ambiente real

**Camada 4 — Autenticidade:**
- Expressoes faciais genuinas (nao poses de estudio)
- Roupas e cenarios do dia-a-dia
- Textura de pele real (poros, marcas sutis — sem pele de porcelana)
- Proporcoes corporais realistas

**Camada 5 — Contexto Ambiental:**
- Cenarios reais (nao fundos genericos de stock)
- Objetos do cotidiano no ambiente
- Iluminacao consistente com o cenario
- Hora do dia coerente com a atividade

## Passo 4: Gerar A Imagem

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "prompt humanizado gerado no passo anterior" \
  --mode influencer \
  --format square \
  --model gemini-2-flash-exp \
  --output C:\Users\renat\skills\ai-studio-image\data\outputs\
```

**Modelos disponiveis (em ordem de recomendacao):**

| Modelo | Velocidade | Qualidade | Custo | Uso Ideal |
|--------|-----------|-----------|-------|-----------|
| `gemini-2-flash-exp` | Rapido | Alta | **GRATIS** | **Padrao — usar sempre** |
| `imagen-4` | Medio | Alta | $0.03/img | Alta qualidade (requer --force-paid) |
| `imagen-4-ultra` | Lento | Maxima | $0.06/img | Impressao, 2K (requer --force-paid) |
| `imagen-4-fast` | Rapido | Boa | $0.02/img | Volume alto (requer --force-paid) |
| `gemini-flash-image` | Rapido | Alta | $0.039/img | Edicao de imagem (requer --force-paid) |
| `gemini-pro-image` | Medio | Maxima+4K | $0.134/img | Referencia, 4K (requer --force-paid) |

## Passo 5: Apresentar E Iterar

Mostre o resultado ao usuario. Se precisar ajustar:
- Reluz: Ajustar iluminacao
- Reenquadrar: Mudar composicao
- Mais/menos natural: Ajustar nivel de imperfeicoes
- Mudar cenario: Alterar ambiente

## Templates Pre-Configurados

Para cenarios comuns, use templates prontos. Execute:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\templates.py --list
```

Templates disponiveis:

## Modo Influencer

| Template | Descricao |
|----------|-----------|
| `cafe-lifestyle` | Pessoa em cafeteria/restaurante com bebida/comida |
| `outdoor-adventure` | Atividade ao ar livre, natureza, viagem |
| `workspace-minimal` | Mesa de trabalho elegante, home office |
| `fitness-natural` | Exercicio/wellness com visual natural |
| `food-flat-lay` | Comida vista de cima, flat lay casual |
| `urban-street` | Cenario urbano, street style |
| `golden-hour-portrait` | Retrato com luz dourada do por-do-sol |
| `mirror-selfie` | Selfie no espelho, casual e espontaneo |
| `product-in-use` | Produto sendo usado naturalmente por pessoa |
| `behind-scenes` | Bastidores, making of, dia-a-dia real |

## Modo Educacional

| Template | Descricao |
|----------|-----------|
| `tutorial-step` | Pessoa demonstrando passo de tutorial |
| `whiteboard-explain` | Pessoa explicando em quadro/lousa |
| `hands-on-demo` | Maos fazendo demonstracao pratica |
| `before-after` | Comparacao antes/depois |
| `tool-showcase` | Ferramenta/software sendo utilizado |
| `classroom-natural` | Ambiente de aula/workshop |
| `infographic-human` | Pessoa apontando para dados/graficos |
| `interview-setup` | Setup de entrevista/podcast natural |
| `screen-recording-human` | Pessoa com notebook mostrando tela |
| `team-collaboration` | Equipe trabalhando junta naturalmente |

Usar template:
```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --template cafe-lifestyle \
  --custom "mulher ruiva, 30 anos, lendo livro" \
  --format square
```

## Nivel De Humanizacao

Controle quanto "imperfeicao" injetar:

| Nivel | Efeito |
|-------|--------|
| `ultra` | Maximo realismo — parece 100% foto de celular |
| `natural` (padrao) | Equilibrio perfeito entre qualidade e realismo |
| `polished` | Mais limpo, ainda natural mas com mais cuidado estetico |
| `editorial` | Estilo revista, natural mas com producao |

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --humanization natural
```

## Hora Do Dia

A iluminacao muda drasticamente:

| Opcao | Descricao |
|-------|-----------|
| `morning` | Luz matinal suave, tons frios-quentes |
| `golden-hour` | Por-do-sol/nascer, tons dourados |
| `midday` | Luz dura do meio-dia, sombras marcadas |
| `overcast` | Dia nublado, luz difusa uniforme |
| `night` | Iluminacao artificial, tons quentes |
| `indoor` | Luz de interiores, mista |

## Geracao Em Lote

Para gerar multiplas variacoes:

```bash
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "..." --variations 4 --format square
```

## Instagram Skill

Gere imagens e publique diretamente:
1. Use `ai-studio-image` para gerar a foto
2. Use `instagram` skill para publicar com caption otimizada

## Canva Integration

As imagens geradas podem ser enviadas para o Canva para adicao de texto/branding.

## Troubleshooting

| Problema | Solucao |
|----------|---------|
| `GEMINI_API_KEY not found` | Configure a variavel de ambiente ou crie `.env` |
| `quota exceeded` | Aguarde reset do rate limit ou upgrade do plano |
| `image blocked` | Ajuste o prompt — pode conter conteudo restrito |
| `low quality output` | Aumente humanization para `ultra`, tente outro modelo |

## Referencias

Para guias detalhados, consulte:
- `references/setup-guide.md` — Instalacao e configuracao completa
- `references/prompt-engineering.md` — Tecnicas avancadas de prompt para imagens humanizadas
- `references/api-reference.md` — Documentacao da API do Google AI Studio

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `comfyui-gateway` - Complementary skill for enhanced analysis
- `image-studio` - Complementary skill for enhanced analysis
- `stability-ai` - Complementary skill for enhanced analysis

---

## Reference: Prompt Engineering

# AI Studio Image — Guia Avancado de Prompt Engineering

## Principio Fundamental (da Google)

> "Describe the scene, don't just list keywords."

Paragrafos narrativos e descritivos sempre superam listas de palavras-chave
porque aproveitam a compreensao profunda de linguagem do modelo.

## Templates Oficiais

### 1. Cenas Fotorrealistas

```
A photorealistic [tipo de enquadramento] of [sujeito], [acao/expressao],
set in [ambiente]. Illuminated by [iluminacao], creating [humor/atmosfera].
Captured with [camera/lente], emphasizing [texturas/detalhes].
```

### 2. Mockups de Produto

```
High-resolution product photograph of [produto] on [superficie].
Lighting: [setup] to [proposito]. Camera angle: [angulo] showcasing [feature].
Ultra-realistic, sharp focus on [detalhe].
```

### 3. Material Educacional

```
Create a [tipo visual] explaining [conceito] styled as [referencia].
Show [elementos-chave] and [resultado]. Design resembles [exemplo],
suitable for [audiencia-alvo].
```

### 4. Texto em Imagens

```
Create a [tipo] for [marca] with text "[texto exato]" in [estilo fonte].
Design should be [estilo], with [esquema de cores].
```

**Limite para Imagen: 25 caracteres, ate 3 frases distintas.**
**Para texto complexo: use gemini-pro-image.**

## Tecnicas de Humanizacao

### A Camera de Celular

O segredo para imagens humanizadas esta na simulacao da camera de celular:

- **Profundidade de campo rasa**: Lentes pequenas criam bokeh natural
- **Ruido de sensor**: Especialmente em ambientes com pouca luz
- **Distorcao de lente**: Bordas levemente distorcidas em lente wide
- **Auto-exposicao imperfeita**: Areas levemente sobre/sub-expostas
- **Granulacao**: Textura organica que adiciona vida a imagem

### Expressoes Genuinas

Evite poses de estudio. Descreva momentos reais:

- "caught mid-laugh while talking to a friend"
- "looking down at phone with slight smile"
- "concentrating on work, didn't notice camera"
- "turning to look at something off-camera"

### Ambientes Reais

Descreva cenarios com vida:

- "coffee shop with other customers blurred in background"
- "kitchen with used cutting board and half-chopped vegetables"
- "desk with coffee stain ring, scattered pens, and post-its"
- "park bench with leaves on ground, pigeons nearby"

## Terminologia Fotografica para Prompts

### Iluminacao
- Golden hour, blue hour, overcast diffused
- Window light, mixed indoor lighting
- Backlit with lens flare
- Open shade, dappled forest light

### Lentes e Camera
- 85mm portrait lens, 35mm wide angle
- f/1.8 shallow depth of field
- Smartphone camera, iPhone quality
- Natural bokeh, creamy background

### Composicao
- Rule of thirds, off-center subject
- Leading lines, natural framing
- Negative space, breathing room
- Layered depth: foreground/midground/background

### Textura e Detalhe
- Visible skin pores and natural blemishes
- Fabric texture, material quality
- Environmental texture: wood grain, concrete, brick
- Water droplets, steam, atmospheric particles

## Niveis de Complexidade

### Prompt Simples (Bom)
```
Mulher jovem tomando cafe em cafeteria, luz natural da janela
```

### Prompt Intermediario (Melhor)
```
Young woman sitting by a large window in a cozy coffee shop, holding a
warm latte, morning sunlight creating soft shadows, genuine relaxed smile,
wearing a casual sweater, taken with smartphone
```

### Prompt Avancado (Excelente)
```
A medium close-up photograph of a young woman in her late 20s sitting at
a wooden table next to a large cafe window. She is holding a ceramic latte
cup with both hands, steam visible, looking slightly to the side with a
genuine warm smile. Soft morning sunlight streams through the window creating
natural shadows across the table. She wears a casual cream knit sweater with
slightly pushed-up sleeves. Her hair is naturally styled, not perfect.
Background shows blurred cafe interior with other customers. Taken with a
smartphone camera, natural depth of field, no professional lighting or flash.
Real skin texture visible, subtle freckles. The image feels warm, authentic,
and completely unposed — like a friend snapped this photo across the table.
```

## Erros Comuns a Evitar

1. **Prompt muito curto** → Resultado generico
2. **Lista de keywords** → Menos natural que narrativa
3. **Pedir "perfeicao"** → AI gera algo que parece artificial
4. **Esquecer o contexto** → Fundo generico/vazio
5. **Nao especificar camera** → Modelo assume DSLR profissional
6. **Pele "perfeita"** → Uncanny valley, parece falso
7. **Iluminacao de estudio** → Mata a naturalidade
8. **Poses de modelo** → Stock photo vibe

## Features Avancadas

### Multi-Turn (Gemini)
Use chat para iterar:
1. Gere a imagem base
2. "Move the coffee cup to the left"
3. "Make the lighting warmer"
4. "Add a small plant in the background"

### Reference Images (Gemini Pro)
Envie ate 14 imagens de referencia:
- 6 para objetos (alta fidelidade)
- 5 para pessoas (consistencia de personagem)

### Thinking Mode (Gemini Pro)
O modelo "pensa" antes de gerar — cria composicoes intermediarias
para refinar o resultado final. Ideal para cenas complexas.

### Search Grounding (Gemini Pro)
Gera imagens baseadas em informacoes em tempo real da web.

---

## Reference: Setup Guide

# AI Studio Image — Guia de Setup Completo

## 1. Obter API Key

1. Acesse https://aistudio.google.com/apikey
2. Clique em "Create API Key"
3. Selecione ou crie um projeto Google Cloud
4. Copie a key gerada

## 2. Configurar API Key

### Opcao A: Arquivo .env (recomendado)

Crie/edite `C:\Users\renat\skills\ai-studio-image\.env`:

```
GEMINI_API_KEY=sua-api-key-principal
GEMINI_API_KEY_BACKUP_1=key-backup-1
GEMINI_API_KEY_BACKUP_2=key-backup-2
```

### Opcao B: Variavel de ambiente

```bash
# Windows CMD
set GEMINI_API_KEY=sua-api-key

# Windows PowerShell
$env:GEMINI_API_KEY="sua-api-key"

# Linux/Mac
export GEMINI_API_KEY=sua-api-key
```

## 3. Instalar Dependencias

```bash
pip install -r C:\Users\renat\skills\ai-studio-image\scripts\requirements.txt
```

Ou manualmente:
```bash
pip install google-genai Pillow python-dotenv
```

## 4. Teste Rapido

```bash
# Testar se tudo funciona
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py --list-models

# Gerar primeira imagem
python C:\Users\renat\skills\ai-studio-image\scripts\generate.py \
  --prompt "pessoa jovem sorrindo em cafeteria" \
  --mode influencer \
  --format square
```

## 5. Modelos Disponiveis

| Modelo | ID | Velocidade | Qualidade | Custo | Melhor Para |
|--------|-----|-----------|-----------|-------|-------------|
| imagen-4 | imagen-4.0-generate-001 | Medio | Alta | $0.03 | **Uso geral (recomendado)** |
| imagen-4-ultra | imagen-4.0-ultra-generate-001 | Lento | Maxima | $0.06 | Alta qualidade, impressao |
| imagen-4-fast | imagen-4.0-fast-generate-001 | Rapido | Boa | $0.02 | Volume alto, iteracao rapida |
| gemini-flash-image | gemini-2.5-flash-preview-image-generation | Rapido | Alta | Var. | Edicao, multi-turn |
| gemini-pro-image | gemini-3-pro-image-preview | Medio | Maxima+4K | Var. | Texto, referencia, 4K |

## 6. Formatos (Aspect Ratios)

| Nome | Ratio | Uso |
|------|-------|-----|
| square | 1:1 | Feed Instagram/Facebook |
| portrait-45 | 4:5 | Instagram portrait (melhor!) |
| portrait-34 | 3:4 | Pinterest, cards |
| portrait-23 | 2:3 | Posters, prints |
| widescreen | 16:9 | YouTube, banners |
| ultrawide | 21:9 | Cinematico |
| stories | 9:16 | Stories, Reels, TikTok |
| landscape-43 | 4:3 | Apresentacoes |
| landscape-32 | 3:2 | Fotografia 35mm |
| landscape-54 | 5:4 | Quase-quadrado |

## 7. Niveis de Humanizacao

| Nivel | Descricao | Quando Usar |
|-------|-----------|-------------|
| ultra | Parece celular amador | Conteudo muito casual, BTS |
| natural | Celular moderno, equilibrado | **Padrao — maioria dos casos** |
| polished | Natural mas caprichado | Conteudo profissional |
| editorial | Estilo revista | Branding, editorial |

## 8. Troubleshooting

| Erro | Causa | Solucao |
|------|-------|---------|
| API key not found | Sem key configurada | Crie .env ou set variavel |
| 403 Forbidden | Key sem permissao | Verifique permissoes no Google Cloud |
| 429 Rate Limited | Muitas requisicoes | Aguarde ou use key backup |
| Image blocked | Conteudo restrito | Ajuste prompt, evite conteudo sensivel |
| Model not found | Modelo indisponivel | Tente outro modelo: imagen-4 |
| Empty response | Prompt muito generico | Adicione mais detalhes ao prompt |
