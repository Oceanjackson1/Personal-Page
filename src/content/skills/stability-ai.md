---
title: "Stability AI"
description: "Geracao de imagens via Stability AI (SD3.5, Ultra, Core). Text-to-image, img2img, inpainting, upscale, remove-bg, search-replace. 15 estilos artisticos."
category: "other"
source: "community"
author: "Community"
tags: ["stability", "ai"]
date: 2026-03-20
---

# Stability AI — Gerador de Imagens Profissional

## Overview

Geracao de imagens via Stability AI (SD3.5, Ultra, Core). Text-to-image, img2img, inpainting, upscale, remove-bg, search-replace. 15 estilos artisticos.

## When to Use This Skill

- When the user mentions "stability ai" or related topics
- When the user mentions "stable diffusion" or related topics
- When the user mentions "sd3.5" or related topics
- When the user mentions "gerar arte" or related topics
- When the user mentions "gerar ilustracao" or related topics
- When the user mentions "image to image" or related topics

## Do Not Use This Skill When

- The task is unrelated to stability ai
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

Skill para gerar imagens artisticas e fotorrealistas usando a Stability AI API.
**Gratuito** com Community License (sem limite para uso pessoal/pequenas empresas).

## Quando Usar Esta Skill Vs Ai-Studio-Image

| Cenario | Skill recomendada |
|---------|-------------------|
| Foto humanizada para Instagram/redes sociais | ai-studio-image |
| Arte digital, ilustracao, concept art | **stability-ai** |
| Foto com camera de celular (realismo casual) | ai-studio-image |
| Fotorrealismo cinematografico (8K, detalhado) | **stability-ai** |
| Material educacional com visual profissional | ai-studio-image |
| Poster, wallpaper, book cover, game asset | **stability-ai** |
| Inpainting (editar parte de uma imagem) | **stability-ai** |
| Upscale (aumentar resolucao) | **stability-ai** |
| Remover fundo de imagem | **stability-ai** |
| Search & Replace (trocar objeto em imagem) | **stability-ai** |
| Apagar elemento de uma imagem | **stability-ai** |

## Setup Rapido

1. Criar conta em **platform.stability.ai** (gratuito)
2. Copiar API Key do dashboard
3. Colar no `.env`: `STABILITY_API_KEY=sk-sua-chave-aqui`
4. `pip install -r scripts/requirements.txt`

Detalhes completos em `references/setup-guide.md`.

## 1. Modos De Operacao

| Comando | O que faz | Endpoint |
|---------|-----------|----------|
| `--mode generate` | Texto para imagem (SD3.5) | `/generate/sd3` |
| `--mode ultra` | Texto para imagem premium | `/generate/ultra` |
| `--mode core` | Texto para imagem rapido | `/generate/core` |
| `--mode img2img` | Imagem + texto para nova imagem | `/generate/sd3` |
| `--mode upscale` | Aumentar resolucao (conservativo) | `/upscale/conservative` |
| `--mode upscale-creative` | Aumentar resolucao com detalhes | `/upscale/creative` |
| `--mode remove-bg` | Remover fundo (PNG transparente) | `/edit/remove-background` |
| `--mode inpaint` | Editar parte da imagem (mascara) | `/edit/inpaint` |
| `--mode search-replace` | Trocar objeto por descricao | `/edit/search-and-replace` |
| `--mode erase` | Apagar parte da imagem | `/edit/erase` |

## 2. Exemplos De Uso

```bash

## Geracao Basica (Sd 3.5 Large)

python scripts/generate.py --prompt "a serene mountain landscape at sunset" --mode generate

## Qualidade Maxima (Ultra)

python scripts/generate.py --prompt "cinematic portrait, dramatic lighting" --mode ultra --aspect-ratio 16:9

## Rapido Para Iteracao (Core)

python scripts/generate.py --prompt "cute cat ninja" --mode core --style anime

## Image-To-Image

python scripts/generate.py --prompt "watercolor style" --mode img2img --image foto.jpg --strength 0.7

## Upscale Conservativo

python scripts/generate.py --prompt "landscape photo" --mode upscale --image foto_pequena.jpg

## Remover Fundo

python scripts/generate.py --mode remove-bg --image produto.jpg

## Inpainting Com Mascara

python scripts/generate.py --prompt "red roses" --mode inpaint --image jardim.jpg --mask mascara.png

## Search & Replace

python scripts/generate.py --prompt "a golden retriever" --mode search-replace --image parque.jpg --search "the cat"

## Apagar Objeto

python scripts/generate.py --mode erase --image foto.jpg --mask area.png

## Listar Modelos

python scripts/generate.py --list-models

## Listar Estilos

python scripts/generate.py --list-styles

## Analisar Prompt (Sugestoes Automaticas)

python scripts/generate.py --prompt "anime warrior girl, widescreen" --analyze --json
```

## 3. Aspect Ratios

| Nome | Ratio | Aliases | Uso tipico |
|------|-------|---------|-----------|
| square | 1:1 | ig, instagram, quadrado | Feed Instagram |
| portrait | 2:3 | retrato, pinterest | Retrato, poster |
| landscape | 3:2 | paisagem, horizontal | Paisagem, banner |
| photo | 4:5 | ig-feed | Instagram feed otimizado |
| wide | 16:9 | widescreen, youtube, cinema, wallpaper | Cinema, YT |
| ultrawide | 21:9 | — | Monitor ultrawide |
| stories | 9:16 | vertical, tiktok, ig-stories | Stories, Reels |
| phone | 9:21 | — | Wallpaper celular |

## 4. Estilos (15 Presets)

Cada estilo adiciona qualificadores automaticamente ao prompt:

| Estilo | Descricao | Ideal para |
|--------|-----------|-----------|
| photorealistic | Fotorrealismo cinematografico | Retratos, cenas |
| anime | Anime/Manga japones | Personagens, cenas |
| digital-art | Arte digital detalhada | Ilustracoes gerais |
| oil-painting | Pintura a oleo classica | Arte classica |
| watercolor | Aquarela fluida | Arte delicada |
| pixel-art | Pixel art retro 8/16-bit | Games retro |
| 3d-render | Render 3D fotorrealista | Produtos, cenas 3D |
| concept-art | Concept art profissional | Games, filmes |
| comic | Comics/HQ estilizado | Quadrinhos |
| minimalist | Minimalista limpo | Design, logos |
| fantasy | Fantasy art epico | RPG, medieval |
| sci-fi | Sci-fi futurista | Cyberpunk, espaco |
| sketch | Desenho a lapis/carvao | Estudos, rascunhos |
| pop-art | Pop art vibrante | Arte moderna |
| noir | Film noir dramatico | Atmosfera sombria |

## 5. Output

Imagens salvas em `data/outputs/` com naming: `{mode}_{style}_{timestamp}_{index}.png`

Metadados salvos em `.meta.json` com: prompt original, prompt final, modelo, aspect ratio, seed, tempo, tamanho.

## Integracao Com Outras Skills

- **ai-studio-image**: Complementar — Stability AI para arte, Gemini para fotos humanizadas
- **instagram**: Gerar arte → publicar no Instagram
- **telegram**: Gerar imagem → enviar via bot

## Rate Limits & Seguranca

- **Community License**: 150 requests/10 segundos
- **Limite diario**: 100 imagens/dia (configuravel via `SAFETY_MAX_IMAGES_PER_DAY`)
- **Retry automatico** com backoff exponencial em caso de 429
- **Fallback de API keys** (primaria + backups)

## Referencia De Arquivos

| Arquivo | Quando consultar |
|---------|-----------------|
| `references/setup-guide.md` | Setup inicial, API key, troubleshooting |
| `references/prompt-engineering.md` | Tecnicas avancadas de prompt |
| `references/api-reference.md` | Endpoints, parametros, respostas, erros |

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `ai-studio-image` - Complementary skill for enhanced analysis
- `comfyui-gateway` - Complementary skill for enhanced analysis
- `image-studio` - Complementary skill for enhanced analysis

---

## Reference: Api Reference

# API Reference — Stability AI v2beta

## Indice

1. [Autenticacao](#autenticacao)
2. [Endpoints de Geracao](#endpoints-de-geracao)
3. [Endpoints de Edicao](#endpoints-de-edicao)
4. [Endpoints de Upscale](#endpoints-de-upscale)
5. [Parametros Comuns](#parametros-comuns)
6. [Respostas](#respostas)
7. [Erros](#erros)

---

## Autenticacao

Todas as requests usam header `Authorization`:

```
Authorization: Bearer sk-sua-chave-aqui
```

Base URL: `https://api.stability.ai/v2beta`

Formato: Todas as requests usam `multipart/form-data` (nao JSON).

## Endpoints de Geracao

### POST /stable-image/generate/sd3

Gera imagens com Stable Diffusion 3.5.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `prompt` | string | Sim | Prompt de texto (max 10000 chars) |
| `model` | string | Nao | `sd3.5-large` (default), `sd3.5-large-turbo`, `sd3.5-medium` |
| `aspect_ratio` | string | Nao | Ratio como `1:1`, `16:9`, etc. Default: `1:1` |
| `negative_prompt` | string | Nao | O que evitar na geracao |
| `seed` | int | Nao | Seed para reproducibilidade (0 a 4294967294) |
| `output_format` | string | Nao | `png` (default), `jpeg`, `webp` |
| `image` | file | Nao | Imagem base para img2img |
| `strength` | float | Nao | Forca da transformacao img2img (0.0-1.0, default 0.7) |
| `mode` | string | Nao | `text-to-image` (default) ou `image-to-image` |

**Modelos disponiveis:**
- `sd3.5-large` — Melhor qualidade geral (recomendado)
- `sd3.5-large-turbo` — Rapido, menos passos
- `sd3.5-medium` — Balanco velocidade/qualidade

### POST /stable-image/generate/ultra

Geracao premium com maxima qualidade.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `prompt` | string | Sim | Prompt de texto |
| `aspect_ratio` | string | Nao | Default: `1:1` |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed para reproducibilidade |
| `output_format` | string | Nao | `png`, `jpeg`, `webp` |

Nao aceita `model` (modelo fixo Ultra).

### POST /stable-image/generate/core

Geracao rapida e eficiente.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `prompt` | string | Sim | Prompt de texto |
| `aspect_ratio` | string | Nao | Default: `1:1` |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed para reproducibilidade |
| `output_format` | string | Nao | `png`, `jpeg`, `webp` |
| `style_preset` | string | Nao | Preset de estilo (ex: `cinematic`) |

## Endpoints de Edicao

### POST /stable-image/edit/inpaint

Edita parte de uma imagem usando mascara.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem original |
| `prompt` | string | Sim | O que gerar na area mascarada |
| `mask` | file | Nao | Mascara (branco = area a editar) |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |

Se `mask` nao for enviada, o modelo tenta inferir automaticamente.

### POST /stable-image/edit/search-and-replace

Encontra e substitui objetos na imagem.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem original |
| `prompt` | string | Sim | O que colocar no lugar |
| `search_prompt` | string | Sim | O que procurar/substituir |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |

### POST /stable-image/edit/erase

Apaga parte de uma imagem (preenche com contexto).

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem original |
| `mask` | file | Nao | Mascara da area a apagar |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |

### POST /stable-image/edit/outpaint

Expande a imagem alem das bordas originais.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem original |
| `prompt` | string | Nao | Descricao do conteudo a gerar |
| `left` | int | Nao | Pixels a expandir para esquerda (0-2000) |
| `right` | int | Nao | Pixels a expandir para direita (0-2000) |
| `up` | int | Nao | Pixels a expandir para cima (0-2000) |
| `down` | int | Nao | Pixels a expandir para baixo (0-2000) |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |

Pelo menos uma direcao deve ser > 0.

### POST /stable-image/edit/remove-background

Remove o fundo da imagem.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem para remover fundo |
| `output_format` | string | Nao | `png` (com transparencia) |

Retorna imagem com fundo transparente (PNG).

## Endpoints de Upscale

### POST /stable-image/upscale/conservative

Aumenta resolucao mantendo fidelidade maxima ao original.

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem para upscale |
| `prompt` | string | Sim | Descricao da imagem |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |
| `creativity` | float | Nao | Nivel de liberdade criativa (0.2-0.5) |

### POST /stable-image/upscale/creative

Aumenta resolucao adicionando detalhes criativamente.

Fluxo em 2 etapas:
1. POST para iniciar — retorna `generation_id`
2. GET para buscar resultado (pode demorar)

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `image` | file | Sim | Imagem para upscale |
| `prompt` | string | Sim | Descricao da imagem |
| `negative_prompt` | string | Nao | O que evitar |
| `seed` | int | Nao | Seed |
| `output_format` | string | Nao | Formato de saida |
| `creativity` | float | Nao | Nivel de liberdade criativa (0.2-0.5) |

## Parametros Comuns

### aspect_ratio
Ratios suportados: `1:1`, `2:3`, `3:2`, `4:5`, `5:4`, `9:16`, `16:9`, `9:21`, `21:9`

### output_format
- `png` — Sem perda, maior arquivo
- `jpeg` — Comprimido, menor arquivo
- `webp` — Moderno, bom balanco

### seed
- Range: 0 a 4294967294
- Mesma seed + mesmo prompt = mesma imagem (reproducibilidade)
- 0 ou omitido = aleatorio

## Respostas

### Sucesso (200)
- Header `Content-Type: image/png` (ou jpeg/webp)
- Body: bytes da imagem
- Header `seed`: seed usada na geracao
- Header `finish-reason`: `SUCCESS` ou `CONTENT_FILTERED`

### Sucesso com JSON
Se `Accept: application/json`:
```json
{
  "image": "base64_encoded_image_data",
  "seed": 12345,
  "finish_reason": "SUCCESS"
}
```

## Erros

| Codigo | Significado | Acao |
|--------|-------------|------|
| 400 | Bad Request | Verificar parametros |
| 401 | Unauthorized | Verificar API key |
| 402 | Payment Required | Verificar creditos/plano |
| 403 | Forbidden | Conteudo bloqueado por moderacao |
| 404 | Not Found | Endpoint incorreto |
| 429 | Rate Limited | Aguardar e retentar (retry automatico) |
| 500 | Internal Error | Retentar apos alguns segundos |

### Formato de Erro
```json
{
  "id": "error-id",
  "name": "bad_request",
  "errors": ["prompt must not be empty"]
}
```

## Headers Importantes

### Request
```
Authorization: Bearer sk-...
Content-Type: multipart/form-data
Accept: image/* (ou application/json)
```

### Response
```
Content-Type: image/png
seed: 12345
finish-reason: SUCCESS
```

---

## Reference: Prompt Engineering

# Prompt Engineering para Stable Diffusion

## Indice

1. [Estrutura do Prompt](#estrutura-do-prompt)
2. [Qualificadores de Qualidade](#qualificadores-de-qualidade)
3. [Iluminacao](#iluminacao)
4. [Composicao](#composicao)
5. [Estilos Artisticos](#estilos-artisticos)
6. [Negative Prompts](#negative-prompts)
7. [Tecnicas Avancadas](#tecnicas-avancadas)
8. [Exemplos por Categoria](#exemplos-por-categoria)

---

## Estrutura do Prompt

Stable Diffusion responde melhor a prompts estruturados em camadas:

```
[assunto principal], [detalhes visuais], [estilo], [iluminacao], [qualidade], [camera/tecnica]
```

Cada camada adiciona especificidade. Comece pelo assunto e va adicionando detalhes.

**Bom:**
```
a warrior princess in golden armor, intricate filigree details,
fantasy art style, dramatic rim lighting, 8k uhd, highly detailed
```

**Ruim:**
```
princess
```

## Qualificadores de Qualidade

Adicione ao final do prompt para melhorar a qualidade geral:

### Alta Qualidade
- `masterpiece, best quality`
- `highly detailed, ultra detailed`
- `8k uhd, high resolution`
- `sharp focus, crisp details`
- `professional, award-winning`

### Renderizacao
- `ray tracing, global illumination`
- `physically based rendering`
- `subsurface scattering`
- `volumetric lighting`

### Fotografia
- `shot on Canon EOS R5`
- `85mm f/1.4 lens`
- `DSLR quality`
- `film grain, Kodak Portra 400`

## Iluminacao

A iluminacao define o humor da imagem:

| Tipo | Efeito | Uso |
|------|--------|-----|
| `natural lighting` | Suave, realista | Cenas externas |
| `golden hour` | Quente, dourado | Retratos, paisagens |
| `dramatic lighting` | Alto contraste | Acao, drama |
| `rim lighting` | Contorno brilhante | Retratos artisticos |
| `studio lighting` | Uniforme, profissional | Produtos, retratos |
| `neon lighting` | Colorido, urbano | Cyberpunk, noturno |
| `candlelight` | Quente, intimo | Cenas intimistas |
| `moonlight` | Frio, misterioso | Noturno, fantasy |
| `chiaroscuro` | Extremo claro/escuro | Classico, dramatico |
| `backlit` | Silhueta, halo | Artistico |
| `volumetric fog` | Atmosferico | Fantasy, horror |

## Composicao

Controle o enquadramento e perspectiva:

| Termo | Efeito |
|-------|--------|
| `close-up portrait` | Rosto em destaque |
| `full body shot` | Corpo inteiro |
| `wide angle` | Panoramico, expansivo |
| `bird's eye view` | Vista aerea |
| `low angle` | De baixo para cima (poder) |
| `dutch angle` | Inclinado (tensao) |
| `symmetrical` | Simetria central |
| `rule of thirds` | Composicao classica |
| `depth of field` | Fundo desfocado |
| `macro` | Extremo close-up |

## Estilos Artisticos

### Por Movimento
- `art nouveau` — Curvas organicas, decorativo
- `art deco` — Geometrico, luxuoso
- `impressionism` — Pinceladas visiveis
- `surrealism` — Surrealista, onírico
- `baroque` — Dramatico, ornamentado
- `romanticism` — Emocional, natureza

### Por Midia
- `oil painting` — Classico, textural
- `watercolor` — Suave, fluido
- `pencil sketch` — Monocromatico, linhas
- `digital painting` — Limpo, detalhado
- `vector art` — Formas limpas, flat
- `pixel art` — Retro, blocky
- `3d render` — Volumetrico, realista

### Por Referencia
- `trending on artstation` — Alta qualidade digital
- `unreal engine 5` — Fotorrealista 3D
- `octane render` — Render premium
- `studio ghibli` — Anime japones classico

## Negative Prompts

Negative prompts removem elementos indesejados. A skill aplica automaticamente
por estilo, mas voce pode adicionar com `--negative-prompt`.

### Universais (bons para quase tudo)
```
low quality, blurry, distorted, deformed, ugly,
bad anatomy, bad proportions, extra limbs,
watermark, text, signature, logo
```

### Para Fotorrealismo
```
cartoon, anime, painting, illustration,
drawing, cgi, render, sketch, comic
```

### Para Arte
```
photo, photograph, realistic, 3d render,
low quality, amateur
```

### Para Rostos
```
deformed face, ugly face, bad eyes,
cross-eyed, asymmetric face, extra fingers
```

## Tecnicas Avancadas

### Peso de Palavras
Alguns modelos suportam peso entre parenteses:
```
(masterpiece:1.4), (beautiful:1.2), landscape
```
Maior peso = mais enfase nesse elemento.

### Prompt Mixing
Combine estilos para resultados unicos:
```
cyberpunk city, art nouveau architecture, neon lights,
watercolor style with digital art details
```

### Descricao Progressiva
Comece amplo, va afunilando:
```
epic landscape, mountain range at sunset,
snow-capped peaks reflecting golden light,
a lone traveler on a winding path below,
fantasy art, dramatic clouds, volumetric lighting
```

### Mood Words
Palavras que definem o tom emocional:
- `serene, peaceful, calm` — Tranquilo
- `epic, grand, majestic` — Epico
- `dark, moody, ominous` — Sombrio
- `whimsical, playful, fun` — Divertido
- `ethereal, dreamy, mystical` — Onirico
- `gritty, raw, intense` — Intenso

## Exemplos por Categoria

### Retrato Artistico
```
a young woman with flowing red hair, wind-blown,
freckles, green eyes, wearing a flower crown,
oil painting style, warm golden hour lighting,
masterpiece, highly detailed, soft focus background
```

### Paisagem Fantasy
```
floating islands above clouds, waterfalls cascading into void,
ancient temple ruins with glowing runes, bioluminescent plants,
epic fantasy landscape, dramatic sunset, volumetric god rays,
concept art, matte painting, 8k uhd
```

### Sci-Fi Ambiente
```
neon-lit cyberpunk alley in rain, holographic advertisements,
steam rising from grates, lone figure with umbrella,
blade runner aesthetic, moody atmosphere, reflections on wet ground,
cinematic composition, anamorphic lens flare
```

### Produto/Objeto
```
luxury wristwatch on marble surface,
crystal clear details, metal and glass textures,
professional product photography, studio lighting,
shallow depth of field, 4k, commercial quality
```

### Game Asset
```
crystal sword with ice enchantment,
glowing blue runes along the blade, ornate silver handle,
game item concept art, clean background,
multiple angle views, pixel-perfect details
```

### Poster/Cover
```
epic dragon perched on mountain peak, wings spread wide,
medieval castle in valley below, army approaching,
cinematic movie poster composition, dramatic sky,
bold contrast, fantasy art, highly detailed illustration
```

---

## Reference: Setup Guide

# Setup Guide — Stable Diffusion Skill

## 1. Criar Conta na Stability AI

1. Acesse **https://platform.stability.ai**
2. Clique em **Sign Up** (ou Login se ja tem conta)
3. Pode usar Google, GitHub ou email/senha
4. A **Community License** e gratuita e automatica para uso pessoal ou empresas com faturamento < $1M/ano

## 2. Obter API Key

1. Apos login, va para **Account** > **API Keys** (ou acesse direto: https://platform.stability.ai/account/keys)
2. Clique em **Create API Key**
3. De um nome (ex: "claude-skills")
4. Copie a key gerada (comeca com `sk-`)

## 3. Configurar a Key

Edite o arquivo `.env` na raiz da skill (`stable-diffusion/.env`):

```
STABILITY_API_KEY=sk-sua-chave-aqui
```

Alternativa: exportar como variavel de ambiente:

```bash
export STABILITY_API_KEY="sk-sua-chave-aqui"
```

## 4. Instalar Dependencias

```bash
cd stable-diffusion
pip install -r scripts/requirements.txt
```

Unica dependencia externa: **Pillow** (manipulacao de imagens).
As chamadas HTTP usam `urllib` (stdlib do Python).

## 5. Testar Conexao

```bash
python scripts/generate.py --list-models
```

Se a key estiver correta, voce vera a lista de modelos disponiveis.

## 6. Primeira Geracao

```bash
python scripts/generate.py --prompt "a beautiful sunset over mountains" --mode generate
```

A imagem sera salva em `data/outputs/`.

## Troubleshooting

### Erro 401 (Unauthorized)
- Verifique se a key esta correta no `.env`
- Verifique se nao ha espacos extras na key
- Gere uma nova key no dashboard

### Erro 402 (Payment Required)
- Sua conta pode ter excedido limites de credito
- Community License tem uso generoso mas pode ter restricoes em pico
- Verifique o dashboard para status

### Erro 429 (Rate Limited)
- Limite: 150 requests a cada 10 segundos
- O script ja faz retry automatico com backoff
- Se persistir, aguarde alguns minutos

### Erro 400 (Bad Request)
- Verifique se o prompt nao esta vazio
- Verifique se o aspect ratio e valido (use `--list-models` para ver opcoes)
- Para img2img/inpaint, verifique se o arquivo de imagem existe

### Imagem nao salva
- Verifique permissoes de escrita em `data/outputs/`
- O diretorio e criado automaticamente, mas pode falhar em ambientes restritos

## Rate Limits Detalhados

| Plano | Requests/10s | Modelos |
|-------|-------------|---------|
| Community | 150 | Todos SD3.5, Ultra, Core |

## Seguranca

- A key nunca e logada ou exibida em outputs
- O `.env` esta no `.gitignore` (nao committar!)
- Limite diario configuravel: `SAFETY_MAX_IMAGES_PER_DAY=100` (env var)
- Contador diario em `data/daily_counter.json`
