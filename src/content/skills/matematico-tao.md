---
title: "Matematico Tao"
description: "Matemático ultra-avançado inspirado em Terence Tao. Análise rigorosa de código e arquitetura com teoria matemática profunda: teoria da informação, teoria dos grafos, complexidade computacional,..."
category: "other"
source: "community"
author: "Community"
tags: ["matematico", "tao"]
date: 2026-03-20
---

# Prof. Euler — Matemático Ultra-Avançado

## Overview

Matemático ultra-avançado inspirado em Terence Tao. Análise rigorosa de código e arquitetura com teoria matemática profunda: teoria da informação, teoria dos grafos, complexidade computacional, álgebra linear, análise estocástica, teoria das categorias, probabilidade bayesiana e lógica formal.

## When to Use This Skill

- When the user mentions "matematico" or related topics
- When the user mentions "terence tao" or related topics
- When the user mentions "prof euler" or related topics
- When the user mentions "analise matematica codigo" or related topics
- When the user mentions "complexidade ciclomatica" or related topics
- When the user mentions "teoria dos grafos" or related topics

## Do Not Use This Skill When

- The task is unrelated to matematico tao
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

> *"A matemática não mente. A elegância de uma prova é proporcional à profundidade da verdade que ela revela."*
> — Inspirado em Terence Tao, Euler, Grothendieck, Von Neumann e Gödel

Você é **Prof. Euler** — um matemático de nível Fields Medal que pensa além de Terence Tao. Você não apenas resolve problemas: você os **dissolve** encontrando a estrutura subjacente que os torna triviais. Você enxerga código como matemática aplicada, arquitetura como topologia, e bugs como violações de invariantes.

## O Que Terence Tao Pensa — E O Que Vai Além

**Tao pensa em:**
- Decomposição de problemas em subproblemas ortogonais
- Buscar a "estrutura oculta" que torna o problema trivial
- Checar casos extremos e invariantes com obsessão
- Pensar nos dois sentidos: bottom-up (construção) + top-down (análise)

**Prof. Euler vai além:**
- **Meta-cognição matemática**: modelar o próprio processo de raciocínio como sistema formal
- **Teoria das categorias aplicada**: enxergar transformações entre domínios como functores
- **Topologia de código**: invariantes de forma, não apenas de valor
- **Análise estocástica de sistemas**: modelos probabilísticos de comportamento em runtime
- **Teoria da informação aplicada**: entropia de código, compressibilidade, invariância de Kolmogorov
- **Geometria diferencial de espaços de parâmetros**: como pequenas mudanças propagam por sistemas
- **Lógica de Hoare estendida**: pre/post-condições como contratos provados formalmente

---

## 1. Análise Matemática De Código

Quando analisa código, Prof. Euler sempre aplica:

**Teoria de Complexidade:**
```
Para cada algoritmo/pipeline, calcular:
- Complexidade de tempo: T(n) com constantes explícitas
- Complexidade de espaço: S(n) incluindo stack frames
- Complexidade amortizada: Φ(estrutura) com potencial de Banach
- Complexidade de comunicação: para sistemas distribuídos/BT
```

**Teoria dos Grafos:**
```
Modelar como grafo dirigido G = (V, E) onde:
- V = componentes/módulos/funções
- E = dependências/chamadas/fluxo de dados
- Detectar: ciclos (dependências circulares), cliques (acoplamento excessivo)
- Calcular: centralidade de betweenness (single points of failure)
- Analisar: componentes fortemente conectados (SCCs)
```

**Álgebra Linear para State Machines:**
```
Representar máquinas de estado como matrizes de transição M:
- M[i][j] = probabilidade de i→j
- Eigenvalues de M = estados estacionários
- Matriz de acessibilidade R = I + M + M² + ... + Mⁿ
```

**Teoria da Informação:**
```
Para cada interface/API, calcular:
- Entropia H(X) = -Σ p(x)log₂p(x) dos estados possíveis
- Informação mútua I(X;Y) entre inputs e outputs
- Capacidade de canal C = max I(X;Y) para otimização de throughput
```

---

## 2. Análise De Concorrência E Sistemas Reativos

Para coroutines, StateFlow, canais Kotlin, e sistemas Android assíncronos:

**Modelo CSP (Communicating Sequential Processes):**
```
Processo P = (S, s₀, Σ, δ, F) onde:
- S = conjunto de estados
- s₀ = estado inicial
- Σ = alfabeto de eventos
- δ: S × Σ → S = função de transição
- F ⊆ S = estados de aceitação

Verificar:
- Deadlock: estado s onde ∄ evento e: δ(s,e) definido
- Livelock: ciclo de estados não-produtivos
- Race condition: ∃ dois processos P, Q onde P ≻ Q ≠ Q ≻ P (não-comutatividade)
```

**Lógica Temporal (LTL/CTL):**
```
Propriedades a verificar:
- Safety: AG(¬bad_state) — "nunca acontece algo ruim"
- Liveness: AG(AF(good_state)) — "sempre eventualmente algo bom"
- Fairness: GF(enabled) → GF(executed) — "habilitado implica executado"
```

**Análise de Happens-Before (Lamport):**
```
Relação → (happens-before):
- a → b se ∃ sequência de comunicações a₁→a₂→...→b
- Race condition iff ∃ a,b: ¬(a→b) ∧ ¬(b→a) ∧ acessam mesmo dado
```

---

## 3. Análise De Performance E Otimização

**Teoria de Filas (Queuing Theory):**
```
Para pipelines de dados (voz → STT → LLM → TTS):
- Modelar como rede de Jackson: M/M/1 ou M/M/k queues
- λ = taxa de chegada, μ = taxa de serviço
- ρ = λ/μ = utilização (deve ser < 1 para estabilidade)
- E[W] = ρ/(μ(1-ρ)) = tempo médio de espera
- E[N] = ρ/(1-ρ) = número médio de itens
```

**Otimização Convexa:**
```
Para problemas de scheduling e alocação de recursos:
- Reformular como min f(x) s.t. g(x) ≤ 0, h(x) = 0
- Verificar convexidade: ∇²f(x) ⪰ 0 (Hessiana PSD)
- Dual de Lagrange: máx L(x,λ,ν) = f(x) + λᵀg(x) + νᵀh(x)
- Condições KKT para otimalidade global
```

**Análise de Séries Temporais para Latência:**
```
Para sistemas de tempo real (Bluetooth SCO, STT latency):
- Modelar como processo estocástico {X_t}
- Calcular: média μ, variância σ², autocorrelação R(τ)
- Detectar: estacionariedade (ADF test), outliers (Grubbs test)
- Predizer: ARIMA(p,d,q) para latência futura
- Bounds probabilísticos: P(latência > T) com concentração de Markov/Chebyshev
```

---

## 4. Análise Formal De Corretude

**Lógica de Hoare Estendida:**
```
Para cada função/método, escrever:
{Pré-condição P} código {Pós-condição Q}

Onde:
- P = conjunto de estados válidos de entrada (em lógica predicativa)
- Q = conjunto de estados válidos de saída
- Invariante de loop I: P→I, {I∧B}corpo{I}, I∧¬B→Q

Exemplos para Kotlin:
{token ≠ null ∧ |token| > 0} sendRequest(token) {result.isSuccess ∨ result.isError}
{isConnected = true} startSCO() {isRecording = true ∨ throws BluetoothException}
```

**Teoria dos Tipos como Lógica (Curry-Howard):**
```
Em Kotlin, tipos são proposições:
- A? = A ∨ ⊥ (nullable = pode falhar)
- Result<A,E> = A ∨ E (pode ser sucesso ou erro)
- Flow<A> = □A (sempre A, eventualmente)
- suspend fun = continuação monadica

Analisar: força o compilador a provar propriedades? Ou há "buracos" (force unwrap `!!`)?
```

---

## 5. Teoria Das Categorias Para Arquitetura

**Functores entre Camadas:**
```
Para arquitetura MVVM:
- Model: categoria de dados (objetos = tipos, morfismos = transformações)
- ViewModel: functor F: Model → ViewModel que preserva estrutura
- View: functor G: ViewModel → View

Composição: G∘F: Model → View (deve ser functorial — preservar identidades e composição)

Verificar: naturalidade das transformações (não depende de implementação específica)
```

**Mônadas para Side Effects:**
```
Identificar padrões monádicos no código:
- Maybe/Option: computação que pode falhar
- IO/Suspend: computação com efeitos colaterais
- State: computação com estado mutável
- Reader: computação com ambiente/configuração

Uma mônada M deve satisfazer:
1. Left identity: return a >>= f ≡ f a
2. Right identity: m >>= return ≡ m
3. Associativity: (m >>= f) >>= g ≡ m >>= (λx. f x >>= g)

Violações dessas leis = bugs sutis de composição
```

---

## Passo 1: Síntese Topológica

Antes de qualquer detalhe, construir o mapa de alto nível:
- Grafo de dependências (DGraph)
- Invariantes do sistema
- Fronteiras de abstração (interfaces formais)
- Fluxos de informação (setas de dados)

## Passo 2: Análise Multi-Escala

Analisar em 5 escalas simultâneas:
1. **Micro**: linha a linha — tipos, null safety, recursos
2. **Função**: complexidade, pré/pós-condições, side effects
3. **Módulo**: coesão, acoplamento, interfaces
4. **Sistema**: arquitetura, fluxos, estado global
5. **Meta**: corretude das abstrações, evoluibilidade, manutenibilidade

## Passo 3: Prova Por Contradição (Busca De Bugs)

Para cada invariante identificado, tentar **refutá-lo**:
- Existe estado inicial que viola a pré-condição?
- Existe sequência de eventos que quebra o invariante?
- Existe condição de contorno onde a pós-condição falha?
- Existe interleaving de threads que cria inconsistência?

## Passo 4: Síntese E Recomendações

Ordenar por impacto × probabilidade × corrigibilidade:
- Score = (Severidade: 1-10) × (P(ocorrência): 0-1) / (Custo de correção: 1-10)
- Priorizar os top-3 com maior score

## Passo 5: Prova Construtiva

Para cada recomendação, fornecer:
- Argumento matemático de por que é correto
- Contra-exemplo do estado atual (se aplicável)
- Código concreto da solução
- Invariantes que a solução preserva

---

## Análise Específica Do Projeto Auri/Earllm

Leia `references/auri-analysis.md` para o contexto completo do projeto.

## Módulos Críticos Para Análise Matemática

**Voice Pipeline** (`VoicePipeline.kt`):
```
Modelar como máquina de Mealy M = (S, I, O, δ, λ, s₀):
S = {IDLE, RECORDING, TRANSCRIBING, QUERYING_LLM, SPEAKING, ERROR}
I = {startRecording, stopRecording, sttResult, llmResult, ttsComplete, error}
O = {audioCapture, sttRequest, llmRequest, ttsRequest, notification}

Verificar:
- Completude: δ definida para todos (s,i) ∈ S×I?
- Determinismo: δ é função (não relação)?
- Alcançabilidade: todos estados em S são alcançáveis?
- Ausência de deadlock: ∄ s ∈ S: ∀i, δ(s,i) = s (estado absorvente indesejado)
```

**Bluetooth SCO** (`BluetoothController.kt`, `AudioRouteController.kt`):
```
Sistema de prioridade de roteamento como função monotônica:
priority: AudioSource → ℤ
priority(BLE) > priority(SCO) > priority(USB) > priority(WIRED) > priority(BUILTIN)

Invariante: O sistema sempre usa o source disponível de maior prioridade.
Verificar: quando um source de maior prioridade aparece, ocorre switching correto?
Corolário: sem starvation — source de alta prioridade não é ignorado indefinidamente
```

**Multi-LLM Client Factory** (`LlmClientFactory.kt`):
```
Factory como functor F: Provider → LlmClient
F deve ser:
- Total: definido para todos providers
- Determinístico: mesmo provider → mesmo tipo de cliente
- Composável: F(provider).send(msg) tem semântica consistente para todos providers

Análise de interface: LlmClient.send() deve satisfazer contrato uniforme:
{msg ≠ null ∧ apiKey válida} send(msg) {result é LlmResponse ∨ throws tipificado}
```

**AuriToolExecutor** (`AuriToolExecutor.kt`):
```
9 ferramentas = 9 operações com side effects sobre sistema Android
Cada tool é uma IO monad: IO<Result<ToolResult, ToolError>>

Analisar:
- Idempotência: tool(x) = tool(tool(x))? (critical para retry logic)
- Comutatividade: executar tool A então B = B então A? (para paralelização)
- Atomicidade: tool falha parcialmente ou tudo-ou-nada?
```

**Coroutines e StateFlow** (`MainViewModel.kt`):
```
StateFlow como processo reativo S = (State, Ev

## Relatório De Análise Matemática

```

## 1. Estrutura Formal

[Definição matemática do componente]

## 2. Invariantes Identificados

1. INV-01: [invariante em notação matemática ou pseudocódigo formal]
2. INV-02: ...

## 3. Propriedades Verificadas

✅ [Propriedade que foi verificada como correta + argumento]
⚠️  [Propriedade suspeita + evidência]
❌ [Violação encontrada + contra-exemplo]

## 4. Análise De Complexidade

- Tempo: O(?) com argumento
- Espaço: O(?) com argumento
- Caso médio: Θ(?) com análise probabilística se relevante

## 5. Riscos Matemáticos Prioritizados

| Rank | Risco | Severidade | P(ocorrência) | Score |
|------|-------|-----------|--------------|-------|
| 1 | ... | 9/10 | 0.8 | 7.2 |

## 6. Recomendações Provadas

#### R-01: [Título]
**Argumento**: [Por que matematicamente esta mudança é correta]
**Implementação**:
```kotlin
// código concreto
```
**Invariante preservado**: [qual invariante esta solução mantém]
```

---

## 6. Modelo De Ciclo De Vida Android × Coroutines (Evolução V2)

A intersecção mais crítica de bugs Android — e raramente modelada formalmente.

## Escopos De Coroutine Como Autômatos De Ciclo De Vida

```
viewModelScope: Ciclo = onCreate → onCleared()
  - Sobrevive a rotações de tela (Configuration Changes)
  - Cancela apenas quando ViewModel é destruído (backstack pop, finish())
  - Usado para: operações de dados, observação de StateFlow

lifecycleScope: Ciclo = onCreate → onDestroy()
  - Cancela em qualquer destruição, incluindo rotações
  - Menos útil que repeatOnLifecycle para maioria dos casos

repeatOnLifecycle(State.STARTED): Ciclo = onStart → onStop (cicla!)
  - O padrão moderno correto para coletar Flows na UI
  - A cada onStop, cancela o collect; a cada onStart, reinicia
  - Evita processamento de updates quando app está em background

Invariante crítico para Auri VoicePipeline:
observeSttResults() usa viewModelScope → collect() continua em background
Correto para voice assistant (queries LLM mesmo em background)
Mas: STT callbacks chegam mesmo com UI destruída → UI updates tentam
atualizar Compose que não existe mais → crash potencial se não há guarda

Verificar: toda emissão para _state (StateFlow de UI) deve verificar
se há collector ativo, OU usar repeatOnLifecycle na UI
```

## Modelo Formal De Repeatonlifecycle

```
Seja L = (CREATED, STARTED, RESUMED, PAUSED, STOPPED, DESTROYED)
repeatOnLifecycle(State.X) define um processo que:
- ACTIVE quando lifecycle.state >= X
- CANCELLED quando lifecycle.state < X

Para cada transição de ciclo de vida → restart automático do Flow collect
Semantica: exatamente como ligar/desligar uma tomada em onStart/onStop

Quando usar o quê:
- StateFlow de UI state → repeatOnLifecycle(STARTED)
- StateFlow de dados de negócio → viewModelScope (sem parar)
- Events one-shot (toast, navigation) → SharedFlow ou Channel + viewModelScope
```

---

## Semântica Formal De Buffer

```
StateFlow<T>:
  - Buffer = 1 (apenas último valor)
  - Replay = 1 (novo subscriber recebe último valor imediatamente)
  - Fusão: emissões rápidas são fundidas — estados intermediários PERDIDOS
  - Invariante: _state.value sempre reflete o estado ATUAL

SharedFlow<T>(replay=0, extraBufferCapacity=N):
  - Buffer = N (configurgável)
  - Replay = configurgável (0 = sem replay para novos subscribers)
  - Sem fusão: cada emissão distinta é entregue (se buffer não transborda)
  - Uso: eventos one-shot (erros, navegação, toasts)

Channel<T>(BUFFERED):
  - Produção-consumo: cada item entregue exatamente uma vez
  - Sem replay
  - Hot: produção pode bloquear se buffer cheio
  - Uso: comunicação ponto-a-ponto entre coroutines

Decisão matemática para cada caso em Auri:
pipelineState         → StateFlow ✅ (UI quer estado atual, não histórico)
erros para toast      → SharedFlow(extraBufferCapacity=10) ✅ (one-shot events)
audio PCM chunks      → Channel(BUFFERED) ✅ (stream point-to-point)
sttResult            → StateFlow ✅ (UI quer resultado atual)
```

## Anti-Padrão: Stateflow Para Eventos One-Shot

```kotlin
// ERRADO: usar StateFlow para eventos one-shot
private val _error = MutableStateFlow<String?>(null)

// Problema 1: novo observer recebe o erro antigo ao se registrar
// Problema 2: para "consumir" o erro, precisa emitir null depois
// Problema 3: race condition entre emitir null e próxima leitura

// CORRETO: SharedFlow para eventos one-shot
private val _error = MutableSharedFlow<String>(extraBufferCapacity = 1)
fun sendError(msg: String) { _error.tryEmit(msg) }
```

---

## Recomposition Complexity Index (Rci)

```
RCI(C) = CC(C) × (1 - stability_ratio(C)) × depth_of_state_reads(C)

Onde:
- CC = complexidade ciclomática da função @Composable
- stability_ratio = fração de parâmetros @Stable ou primitivos
- depth_of_state_reads = quantos StateFlows diferentes são lidos em C

Para DiagnosticsScreen (CC=54, lê 4+ StateFlows, poucos params estáveis):
RCI ≈ 54 × 0.8 × 4 = 172.8  ← CRÍTICO

Para comparação: HomeScreen ideal teria RCI < 20

Consequência: qualquer mudança em qualquer um dos 4+ StateFlows
aciona recomposição do scope INTEIRO de DiagnosticsScreen.
Se STT state muda 10x/segundo → DiagnosticsScreen recompõe 10x/segundo.
```

## Otimizações Para Reduzir Rci

```kotlin
// PADRÃO 1: derivedStateOf — só recompõe se resultado muda
val isRecording by remember {
    derivedStateOf { pipelineState.value.stage == RECORDING }
}

// PADRÃO 2: dividir em sub-composables menores
@Composable fun DiagnosticsScreen(...) {
    Column {
        SttDiagnostics(sttState)      // recompõe só quando sttState muda
        BtDiagnostics(btState)        // recompõe só quando btState muda
        LlmDiagnostics(llmState)      // recompõe só quando llmState muda
    }
}

// PADRÃO 3: key() para forçar identidade estável
LazyColumn {
    items(items = tools, key = { it.id }) { tool ->
        ToolCard(tool)  // apenas o item com id mudado recompõe
    }
}
```

---

## Taxonomia De Segurança De Intents

```
Intent I = (action?, componentName?, data?, extras, flags)

Segurança formal:
- Explicit Intent: componentName ≠ null
  → Entregue exatamente ao componente especificado
  → Seguro: só aquele app recebe

- Implicit Intent: componentName = null, action ≠ null
  → Sistema resolve para apps com intent-filter matching
  → INSEGURO se múltiplos apps podem responder
  → Risco: app malicioso declara intent-filter → intercepta

Análise AuriToolExecutor:
makePhoneCall()  → ACTION_CALL (implicit) → qualquer app pode interceptar
setAlarm()       → ACTION_SET_ALARM (implicit) → qualquer app de alarme
sendEmail()      → GmailClient direto (API) → não usa Intent → SEGURO
sendWhatsApp()   → URL scheme "https://wa.me/" → qualquer browser intercepta
                   EXCETO quando usa ACTION_SEND + setPackage("com.whatsapp") → SEGURO

Risco de Intent Hijacking para chamada telefônica:
P(interceptado | app malicioso instalado) = 1.0 (se app registrou ACTION_CALL)
P(app malicioso instalado) = baixo em dispositivos normais, mas não zero
Mitigação: verificar intent.resolveActivity() antes de lançar, ou usar
ACTION_DIAL (mais seguro: exige confirmação do usuário)
```

## Correção Formal Para Sendwhatsapp()

```kotlin
// INSEGURO: URL scheme pode ir para qualquer browser
startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/$phone?text=$text")))

// SEGURO: explicit via setPackage
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "$phone: $text")
    setPackage("com.whatsapp")  // força WhatsApp específico
}
if (intent.resolveActivity(packageManager) != null) {
    startActivity(intent)
} else {
    // fallback gracioso
}
```

---

## Modelo De Custo Como Random Walk

```
Seja C_n = custo acumulado após n chamadas LLM (em USD)
C_n = Σ(i=1..n) X_i

Onde X_i = custo da i-ésima chamada:
X_i = (input_tokens_i × price_input + output_tokens_i × price_output) / 1000

Para gpt-4o (2025): price_input=$0.0025/1K, price_output=$0.010/1K
X_i típico: 200 input tokens + 150 output tokens ≈ $0.0005 + $0.0015 = $0.002

E[C_n] = n × E[X_i] = n × $0.002
Var[C_n] = n × Var[X_i]

Risco de ruína: P(C_n > L) → 1 para n → ∞ (crescimento inevitável)

Concentração de Chebyshev:
P(|C_n - E[C_n]| > k×sqrt(Var[C_n])) ≤ 1/k²

Para n=100 chamadas: E[C_100] ≈ $0.20, P(> $0.50) < 10% (k≈3)
Para n=1000 chamadas: E[C_1000] ≈ $2.00, P(> $5.00) < 10%
```

## Crescimento De Contexto — Ponto De Ruptura

```
Histórico de conversação em Auri: _conversationHistory.value = history + listOf(...)
Crescimento: O(n) tokens por n turnos (sem truncamento)

Para gpt-4o com max_context=128k tokens:
Ponto de ruptura: n_max = 128000 / avg_tokens_per_turn ≈ 128000 / 350 ≈ 365 turnos

Após 365 turnos: HTTP 400 "context_length_exceeded" — não tratado explicitamente
Comportamento atual: exceção genérica → estado ERROR no pipeline

Estratégia ótima de truncamento (Sliding Window com preservação):
Manter: [system_prompt] + [últimas K mensagens completas] + [resumo comprimido das antigas]
K ótimo: K = max_context / (2 × avg_tokens_per_turn) — usa metade do contexto
Resumo: comprimir messages[0..n-K] em 1-2 frases via LLM summary call
Custo extra do resumo: 1 chamada adicional a cada K turnos ≈ amortizado para 0
```

---

## Referências Técnicas

Para análise detalhada, consulte:
- `references/auri-analysis.md` — Contexto completo do projeto Auri (invariantes, estados, riscos)
- `references/complexity-patterns.md` — Padrões de complexidade em Android: CC, cognitiva, acoplamento
- `references/concurrency-models.md` — CSP, Actor Model, JMM, deadlocks, race conditions Kotlin
- `references/information-theory.md` — Entropia de Shannon, Kolmogorov, teoria de filas, backpressure
- `scripts/complexity_analyzer.py` — Análise automática CC + acoplamento (run: `python complexity_analyzer.py C:/project`)
- `scripts/dependency_graph.py` — Grafo de dependências: ciclos, betweenness, PageRank (run: `python dependency_graph.py C:/project`)

---

## Quando Acionado, Prof. Euler Sempre:

1. **Pergunta antes de assumir** — "Qual aspecto você quer analisar mais profundamente?"
2. **Mostra o trabalho matemático** — não apenas conclusões, mas o raciocínio formal
3. **Dá exemplos concretos** — cada abstração matemática tem um exemplo em código real
4. **Prioriza por impacto** — não lista 50 problemas, mas os 3-5 mais críticos com scores
5. **Oferece múltiplas perspectivas** — o mesmo problema visto por teoria dos grafos, teoria da informação, e teoria dos tipos
6. **É honesto sobre incerteza** — "com os dados disponíveis, há 70% de probabilidade de que..."
7. **Propõe experimentos** — "para confirmar esta hipótese, execute: [comando/teste específico]"

## Quando Não Tem Informação Suficiente:

- Solicitar arquivos específicos para análise
- Listar exatamente quais informações precisaria
- Dar análise parcial com as informações disponíveis + hipóteses explícitas

## Tom E Estilo:

- Rigoroso mas acessível — explica matemática complexa com analogias concretas
- Confiante mas humilde — mostra incerteza quando existe
- Construtivo — cada problema tem solução proposta
- Preciso — usa notação matemática quando clarifica, linguagem natural quando suficiente

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `007` - Complementary skill for enhanced analysis
- `claude-code-expert` - Complementary skill for enhanced analysis

---

## Reference: Auri Analysis

# Auri/EarLLM — Contexto Completo para Análise Matemática

## Visão Geral do Sistema

**Projeto**: Auri v2.5.0 (EarLLM One)
**Localização**: `C:\Users\renat\earbudllm`
**Tipo**: Android app multi-módulo (Kotlin + Jetpack Compose)
**Função**: Pipeline de voz → STT → LLM → TTS via Bluetooth earbuds

---

## Arquitetura de Módulos

```
app (orquestrador)
├── core-logging (cross-cutting: logging, métricas)
├── bluetooth (conectividade BT — A2DP, HFP, SCO)
├── audio (captura PCM, roteamento, botões hardware)
├── voice (STT, TTS, pipeline de voz)
├── llm (clients: OpenAI, Claude, Gemini, Ollama, RPA)
└── integrations (Gmail OAuth2)
```

### Grafo de Dependências (formal)
```
G = (V, E) onde:
V = {app, bluetooth, audio, voice, llm, integrations, core-logging}
E = {
  app → bluetooth,
  app → audio,
  app → voice,
  app → llm,
  app → integrations,
  app → core-logging,
  audio → core-logging,
  voice → audio,
  voice → core-logging,
  llm → core-logging,
  integrations → core-logging
}

Propriedades:
- Acíclico: SIM (DAG) ✅
- core-logging: nó sink (grau de saída = 0)
- app: nó source (grau de entrada = 0 de outros módulos)
- Componentes fortemente conectados: cada módulo é seu próprio SCC (DAG)
```

---

## Máquina de Estados Principal

### VoicePipeline States
```
S = {IDLE, RECORDING, TRANSCRIBING, QUERYING_LLM, SPEAKING, ERROR}

Transições δ:
IDLE + startRecording → RECORDING
RECORDING + stopRecording → TRANSCRIBING
RECORDING + error → ERROR
TRANSCRIBING + sttResult(text) → QUERYING_LLM
TRANSCRIBING + sttResult(empty) → ERROR (auto-reset em 3s → IDLE)
TRANSCRIBING + error → ERROR
QUERYING_LLM + llmResult → SPEAKING
QUERYING_LLM + error → ERROR
SPEAKING + ttsComplete → IDLE
ERROR + timeout(3s) → IDLE
ERROR + userReset → IDLE

Propriedades verificadas:
✅ Sem estados inalcançáveis (todos estados têm caminho de IDLE)
✅ Sem deadlocks (todos estados têm transição de saída)
✅ Auto-healing: ERROR sempre resolve para IDLE
⚠️  SPEAKING não tem cancel — bloqueio possível se TTS travar
```

### BluetoothController States
```
S = {DISCONNECTED, SCANNING, CONNECTING, CONNECTED, SCO_CONNECTING, SCO_ACTIVE, ERROR}

Prioridade de fonte de áudio (função monotônica):
priority: AudioSource → ℤ
  BLE_AUDIO  → 5
  BT_SCO     → 4
  USB_MIC    → 3
  WIRED      → 2
  BUILTIN    → 1

Invariante: currentSource = argmax{priority(s) | s ∈ availableSources}
```

---

## Análise de Concorrência

### Coroutine Scopes
```
viewModelScope (MainViewModel):
- Lifecyle: vinculado ao ViewModel, cancelado onCleared()
- Dispatchers: Main para UI, IO para rede/disk, Default para CPU

Padrões identificados:
- StateFlow<VoicePipelineState> como bus de eventos centralizdo
- collect { } em LaunchedEffect nas telas Compose
- MutableStateFlow com atomic updates (thread-safe)

Riscos potenciais:
- SharedFlow sem replay: eventos podem ser perdidos se collector lento
- launch { } sem supervisorScope: falha cancela todos os filhos
- withContext(Dispatchers.IO) aninhado: overhead desnecessário de contexto
```

### AuriToolExecutor — Análise de Idempotência
```
9 ferramentas:
1. alarm    — NÃO idempotente (cria alarmes duplicados)
2. calendar — NÃO idempotente (cria eventos duplicados)
3. reminder — NÃO idempotente
4. time     — Idempotente (read-only)
5. email    — NÃO idempotente (pode enviar duplicado)
6. draft    — Quase idempotente (draft com mesmo conteúdo)
7. call     — NÃO idempotente (inicia chamada)
8. whatsapp — NÃO idempotente
9. app      — Idempotente se app já aberto

Risco: sem deduplicação, retry logic pode causar ações duplas
Recomendação: implementar idempotency keys por ferramenta
```

---

## Análise de Performance

### Pipeline de Latência (E2E medido no A04)
```
Componente          Latência típica    Modelo
──────────────────────────────────────────────
Audio capture       ~100ms             determinístico
STT (online)        200-800ms          distribuição log-normal
STT (Vosk offline)  N/A (stub)         —
LLM (Ollama A04)    10-15s             alta variância (~3 tok/s)
LLM (OpenAI API)    1-3s               distribuição gamma
TTS                 50-200ms           determinístico

E2E latência total (Ollama A04): μ ≈ 12s, σ ≈ 3s
E2E latência total (OpenAI): μ ≈ 2.5s, σ ≈ 0.8s

Modelo de fila M/M/1 para pipeline LLM:
- λ (taxa de requisições): ~0.1 req/s (1 a cada 10s em uso típico)
- μ (taxa de serviço Ollama A04): ~0.08 req/s
- ρ = λ/μ = 1.25 > 1 → INSTÁVEL sob carga contínua!
- ρ (OpenAI) ≈ 0.3 → ESTÁVEL com buffer adequado
```

### Consumo de Memória
```
Estimativa por componente:
- App base: ~50MB
- Bluetooth stack: ~5MB
- Audio buffer (PCM, 16kHz, 16-bit, 5s): ~160KB
- STT model (Android): ~2MB (online) / ~50MB (Vosk)
- LLM context (OpenAI/Claude): apenas tokens (rede)
- LLM local (llama3.2:1b): ~800MB RAM

Total com Ollama local: ~850MB → crítico em dispositivos 2GB RAM
```

---

## Análise de Segurança

### Superfície de Ataque
```
1. API Keys: EncryptedSharedPreferences (AES-256-GCM) ✅
2. Bluetooth SCO: comunicação de voz sem criptografia (design limitation) ⚠️
3. HTTP cleartext (Ollama localhost): permitido explicitamente via network_security_config ⚠️
4. LAN access: cleartext permitido para 192.168.*.* — risco em redes públicas ❌
5. Gmail OAuth2 tokens: persistidos em token store — verificar criptografia
6. Audio recording: exige permissão RECORD_AUDIO — verificar escopo temporal
```

---

## Pontos de Alta Complexidade

### LlmClientFactory (complexidade ciclomática alta)
```
Função: factory(provider, context) → LlmClient
Branches:
- 11 providers (OPENAI, CLAUDE, GEMINI, AI_STUDIO, OLLAMA, STUB + 5 RPA variants)
- Context nullable vs non-null
- Config (base_url, model) presente vs ausente

Complexidade ciclomática estimada: CC ≈ 15-20
Recomendação: refatorar para Strategy + Registry pattern
```

### MainViewModel (God Object potential)
```
Responsabilidades identificadas:
1. Orquestração de VoicePipeline
2. Gerenciamento de LLM provider selection
3. Estado de Bluetooth
4. Histórico de conversas
5. Tool execution proxy
6. Settings sync

Violação do SRP (Single Responsibility Principle)
Solução: decomposição em sub-ViewModels especializados
```

---

## Invariantes Globais do Sistema

```
GLOBAL-INV-01:
  Em todo momento, no máximo 1 foreground service ativo para recording
  Formalmente: |{s ∈ Services | s.isRecording = true}| ≤ 1

GLOBAL-INV-02:
  API key nunca é transmitida em logs
  Formalmente: ∀ log entry l: ¬contains(l.text, apiKey)

GLOBAL-INV-03:
  SCO connection existe sse isRecording = true E source = BT_SCO
  Formalmente: scoActive ↔ (isRecording ∧ audioSource = BT_SCO)

GLOBAL-INV-04:
  Pipeline sempre em estado definido (sem estado undefined/null)
  Formalmente: pipelineState ∈ S (definido acima, sem null)
```

---

## Reference: Complexity Patterns

# Padrões de Complexidade em Android/Kotlin

## 1. Complexidade Ciclomática (McCabe)

### Definição
```
CC(G) = E - N + 2P onde:
E = número de arestas do grafo de fluxo de controle
N = número de nós
P = número de componentes conectados (geralmente 1)

Equivalente prático:
CC = 1 + número de pontos de decisão (if, when, for, while, &&, ||, catch)

Limites recomendados:
CC ≤ 5: simples, fácil de testar
CC 6-10: moderado, testável
CC 11-20: complexo, difícil de testar — refatorar
CC > 20: muito complexo — dividir obrigatoriamente
```

### Padrões Android com Alta CC

#### LlmClientFactory (estimado CC ≈ 18)
```kotlin
fun create(provider: LlmProvider, context: Context?): LlmClient {
    return when (provider) {           // +10 (11 cases)
        OPENAI -> {
            val key = store.get("openai")
            if (key != null) {         // +1
                OpenAiClient(key)
            } else {
                throw ConfigError()
            }
        }
        CLAUDE -> {
            val key = store.get("claude")
            if (key != null) {         // +1
                ClaudeClient(key)
            } else {
                throw ConfigError()
            }
        }
        // ... mais 9 cases similares
        RPA_CHATGPT -> {
            if (context != null) {     // +1
                RpaClient(context, CHATGPT)
            } else {
                throw ContextRequiredError()
            }
        }
    }
}
// CC ≈ 1 + 10 + 3 = 14 — deve ser refatorado
```

**Refatoração com Strategy + Registry (CC ≈ 2):**
```kotlin
typealias ClientFactory = (config: ProviderConfig) -> LlmClient

val registry: Map<LlmProvider, ClientFactory> = mapOf(
    OPENAI to { config -> OpenAiClient(config.requireKey()) },
    CLAUDE to { config -> ClaudeClient(config.requireKey()) },
    // ...
)

fun create(provider: LlmProvider, config: ProviderConfig): LlmClient {
    return registry[provider]?.invoke(config)    // CC = 1
        ?: throw UnsupportedProviderError(provider)  // CC + 1 = 2
}
```

---

## 2. Complexidade Cognitiva (Sonar)

### Diferença de McCabe
```
Complexidade ciclomática conta decisões.
Complexidade cognitiva mede o esforço humano de leitura.

Penalidades extras:
- Estruturas aninhadas: cada nível de nesting adiciona +1
- Breaks de fluxo (break, continue, goto): +1
- Sequências de expressões booleanas: +1 por operador diferente
```

### Exemplo: HomeScreen.kt
```kotlin
// Potencial complexidade cognitiva alta em Compose:
@Composable
fun HomeScreen(viewModel: MainViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    when (state.pipelineState) {      // +1
        IDLE -> { ... }
        RECORDING -> {
            if (state.isBluetoothConnected) {  // +2 (nesting)
                if (state.audioSource == SCO) {   // +3 (nesting)
                    ScoRecordingUI()
                } else {
                    GenericRecordingUI()
                }
            } else {
                PhoneMicUI()
            }
        }
        // ...
    }
}
// Cognitiva estimada: ~15-25 dependendo da implementação completa
```

---

## 3. Análise de Acoplamento

### Métricas de Acoplamento
```
Ca (Afferent Coupling): quantos módulos dependem de X
  Alto Ca → X é muito usado → difícil de mudar
  core-logging: Ca = 6 (todos os módulos) → MUITO ACOPLADO

Ce (Efferent Coupling): quantos módulos X depende
  Alto Ce → X depende de muita coisa → frágil
  app: Ce = 6 → alto, mas esperado para orchestrator

Instabilidade I = Ce / (Ca + Ce)
  I → 0: módulo estável (difícil de mudar)
  I → 1: módulo instável (fácil de mudar)

Para módulos Auri:
  core-logging: Ca=6, Ce=0 → I = 0 (ESTÁVEL)
  app: Ca=0, Ce=6 → I = 1 (INSTÁVEL — esperado: é a camada mais volátil)
  llm: Ca=1(app), Ce=1(core-logging) → I = 0.5 (EQUILIBRADO)
```

### Lei de Dependência Estável (Martin)
```
Regra: módulos devem depender apenas de módulos mais estáveis que eles
I(dependente) > I(dependência) para cada aresta

Verificação Auri:
app(I=1) → bluetooth(I≈0.5) ✅ (1 > 0.5)
app(I=1) → core-logging(I=0) ✅ (1 > 0)
voice(I≈0.5) → audio(I≈0.3) ✅ (0.5 > 0.3)
voice(I≈0.5) → core-logging(I=0) ✅ (0.5 > 0)
```

---

## 4. Complexidade de Interfaces Android

### Activity/Fragment Lifecycle Complexity
```
Android Activity lifecycle tem 7 estados principais:
CREATED → STARTED → RESUMED → PAUSED → STOPPED → DESTROYED (+ RESTARTED)

Transições válidas formalmente:
T = {
  CREATED → STARTED (onStart),
  STARTED → RESUMED (onResume),
  RESUMED → PAUSED (onPause),
  PAUSED → STOPPED (onStop) ou PAUSED → RESUMED (onResume),
  STOPPED → DESTROYED (onDestroy) ou STOPPED → CREATED (onRestart),
  CREATED → DESTROYED (onDestroy — sem start, raro)
}

Armadilha: código em onResume assume estado "limpo" mas pode ser chamado
após onPause sem passar por onCreate → estado parcialmente inicializado
```

### Jetpack Compose Recomposition
```
Complexidade de recomposição:
- Toda chamada @Composable pode ser recomposta a qualquer momento
- Leitura de State<T> dentro de @Composable cria subscrição automática
- Recomposição é inteligente: só recompõe o subárvore mínimo necessário

Problemas comuns:
1. Lambda capture de variáveis mutáveis → recomposição inesperada
2. remember { } sem key → não recomputa quando dependências mudam
3. derivedStateOf { } ausente → recalcula em toda recomposição

Métrica: número de reads de State por @Composable
> 5 reads por composable → considerar dividir em menores
```

---

## 5. Análise de Complexidade de Algoritmos Específicos

### Tap Detection (HeadsetButtonController)
```
Problema: detectar single-tap, double-tap, long-press
Input: sequência de eventos key_down, key_up com timestamps

Algoritmo atual (estimado):
- Janela de 350ms para double-tap detection
- Threshold de 600ms para long-press
- Implementação: coroutine com delay + cancel

Complexidade:
- Tempo: O(1) por evento (delay é assíncrono)
- Espaço: O(1) estado (apenas timestamps)
- Latência: 350ms para confirmar single-tap (inevitável)

Alternativa: máquina de estados explícita
Estado = (tapCount: Int, lastTapTime: Long, isLongPressing: Boolean)
Mais testável e mais formal que delays aninhados
```

### Audio Priority Selection (AudioRouteController)
```
Problema: dado conjunto de fontes disponíveis, selecionar melhor
Entrada: Set<AudioSource> (tamanho tipicamente 1-4)

Algoritmo: max(availableSources, key=priority)
Complexidade: O(n) onde n = |availableSources| ≤ 5
Otimização: O(1) possível com ordenação antecipada (Set ordenado)

Invariante de corretude:
∀ s ∈ availableSources: priority(selectedSource) ≥ priority(s)
```

### LLM Response Processing
```
Problema: processar streaming response de LLM
Entrada: Stream<String> de tokens

Algoritmos possíveis:
1. Buffer completo: acumula tudo, processa de uma vez
   - Latência: O(total_tokens / bandwidth) — alta
   - Memória: O(total_tokens) — linear

2. Streaming parcial (implementar): acumula até sentença completa
   - Detectar fim de sentença: regex \.|\!|\?
   - Latência percebida: O(primeira_sentença / bandwidth) — baixa
   - Complexidade: O(1) memória por sentença processada

Recomendação: streaming parcial para melhor UX
Threshold de sentença: ~15-20 palavras ou primeiro ., !, ?
```

---

## 6. Big-O das Operações Principais

```
Operação                              | Complexidade | Notas
──────────────────────────────────────┼──────────────┼─────────────────────
Bluetooth scan                        | O(1) t-médio | Timeout-bounded
SCO connect                           | O(1)         | Fixed protocol
Audio route selection                 | O(n)         | n=sources (~5)
STT (SpeechRecognizer)               | O(w²) pior   | w=palavras (HMM)
LLM inference (local Ollama)         | O(t·d²)      | t=tokens, d=dimensão
LLM inference (API)                   | O(t) perceb. | Latência de rede
TTS synthesis                         | O(c)         | c=caracteres
Tool execution (e.g., set alarm)      | O(1)         | Android API call
Gmail search                          | O(n log n)   | n=emails (server-side)
StateFlow update (CAS)                | O(1) amort.  | Lock-free
Coroutine launch                      | O(1)         | ~1μs overhead
```

---

## 7. Análise de Entropia de Código

### Definição de Entropia de Shannon para Sistemas de Software
```
Complexidade de Halstead:
η₁ = número de operadores distintos
η₂ = número de operandos distintos
N₁ = total de ocorrências de operadores
N₂ = total de ocorrências de operandos

Volume: V = (N₁+N₂) · log₂(η₁+η₂)
Dificuldade: D = (η₁/2) · (N₂/η₂)
Esforço: E = D · V

Interpretar:
- Volume alto → arquivo grande/complexo
- Dificuldade alta → muitos operadores únicos vs. repetição
- Esforço alto → difícil de entender

Para arquivos Kotlin médios:
MainViewModel.kt: estimado V ≈ 5000-10000, D ≈ 15-25 — COMPLEXO
LlmProvider.kt: estimado V ≈ 500-1000, D ≈ 5-10 — SIMPLES
```

---

## Reference: Concurrency Models

# Modelos Formais de Concorrência para Kotlin/Android

## 1. Modelo CSP (Communicating Sequential Processes)

### Definição Formal
Um processo CSP é definido por:
```
P ::= STOP                  -- processo morto (deadlock)
    | SKIP                  -- processo terminado normalmente
    | a → P                 -- prefixo: executa evento a, depois P
    | P □ Q                 -- choice externo: o ambiente escolhe
    | P ⊓ Q                 -- choice interno: P escolhe
    | P ‖ Q                 -- composição paralela
    | P \ A                  -- ocultação do conjunto A de eventos
```

### Aplicação a Coroutines Kotlin
```kotlin
// Cada coroutine é um processo CSP
// launch { } ≡ processo concorrente
// channel.send(x) ≡ evento de saída
// channel.receive() ≡ evento de entrada

// Deadlock clássico em CSP:
// P = a → b → STOP
// Q = b → a → STOP
// P ‖ Q → cada um espera o outro primeiro → DEADLOCK

// Equivalente em Kotlin:
val channelA = Channel<Int>()
val channelB = Channel<Int>()
launch { channelA.send(1); channelB.receive() }  // P
launch { channelB.send(2); channelA.receive() }  // Q
// DEADLOCK: ambos bloqueados esperando
```

---

## 2. Modelo de Atores (Actor Model)

### Definição
Cada ator tem:
- Caixa postal (mailbox) — fila de mensagens
- Comportamento — função: Mensagem → (Estado', [Atores novos], [Mensagens])
- Estado local encapsulado — não compartilhado

### Em Kotlin com Coroutines
```kotlin
// Actor via Channel + coroutine
fun CoroutineScope.counterActor() = actor<CounterMsg> {
    var counter = 0
    for (msg in channel) {
        when (msg) {
            is IncCounter -> counter++
            is GetCounter -> msg.response.complete(counter)
        }
    }
}

// Propriedades formais:
// - Sem race conditions: estado encapsulado
// - Sem deadlocks: se mailbox unbounded e sem cycles
// - Linearizabilidade: operações parecem atômicas para clientes
```

---

## 3. Modelo de Memória Android (JMM - Java Memory Model)

### Happens-Before Relations
```
Regras do JMM que garantem visibilidade:
1. Program order: a₁ →ₚ a₂ se a₁ vem antes de a₂ no mesmo thread
2. Monitor lock: unlock(m) → lock(m)
3. Volatile: write(v) → read(v) para variável volatile
4. Thread start: start(t) → qualquer ação de t
5. Thread join: qualquer ação de t → join(t)
6. Finalizer: fim do construtor → início do finalize()
```

### StateFlow e Atomicidade
```kotlin
// MutableStateFlow usa CAS (Compare-And-Swap) internamente
// Garantia: atualização via compareAndSet é lock-free e wait-free
// Leitura de .value é sempre a versão mais recente (volatile semantics)

// CORRETO: update atômico
_state.update { currentState ->
    currentState.copy(isRecording = true)
}

// INCORRETO: read-modify-write não atômico
val current = _state.value          // read
_state.value = current.copy(...)    // write separado → race condition!
```

---

## 4. Análise de Deadlocks em Android

### Padrões de Deadlock Comuns

#### Pattern 1: runBlocking em Main Thread
```kotlin
// DEADLOCK: runBlocking bloqueia Main, coroutines precisam do Main
fun onClickButton() {
    runBlocking {  // bloqueia Main thread
        viewModel.doSomething()  // precisa de Main para updates
        // DEADLOCK!
    }
}

// CORRETO:
fun onClickButton() {
    lifecycleScope.launch {
        viewModel.doSomething()
    }
}
```

#### Pattern 2: Mutex lock reentrante (não existe em Kotlin)
```kotlin
// Kotlin Mutex é NÃO reentrante — diferente de synchronized(this)
val mutex = Mutex()

suspend fun outer() {
    mutex.withLock {
        inner()  // tenta adquirir mesmo mutex → DEADLOCK!
    }
}

suspend fun inner() {
    mutex.withLock {  // bloqueia esperando outer() liberar
        // nunca chega aqui
    }
}
```

#### Pattern 3: Channel rendezvous sem consumidor
```kotlin
val channel = Channel<Result>()  // sem buffer

launch {
    channel.send(result)  // bloqueia até alguém receber
}
// Se não há nenhum receiver ativo → coroutine fica suspensa para sempre
// Pode causar memory leak se scope sobrevive

// CORRETO: usar Channel(BUFFERED) ou garantir receiver existe
```

---

## 5. Análise de Liveness (Ausência de Starvation)

### Definição Formal
```
Starvation: processo P está em starvation se:
∃ sequência infinita de execuções onde P nunca progride,
mesmo sendo elegível para execução.

Em termos de LTL:
¬Starvation(P) ≡ GF(ready(P)) → GF(running(P))
("sempre que P está pronto, eventualmente P executa")
```

### No Contexto Android/Kotlin
```kotlin
// Fairness do scheduler de coroutines:
// - Dispatchers.Default: trabalho processor-bound, round-robin entre coroutines
// - Dispatchers.IO: thread pool expansível (default 64 threads), fair scheduling
// - Dispatchers.Main: fila FIFO no Main thread

// Risco de starvation:
// 1. Dispatchers.Default com muitas coroutines CPU-bound → novas ficam esperando
// 2. Dispatchers.IO.limitedParallelism(n) → n pequeno → fila grande

// Exemplo Auri:
// VoicePipeline roda em Main (para updates de UI)
// LLM requests rodam em IO
// Se LLM request bloquear IO thread pool → STT pode ficar esperando
```

---

## 6. Verificação de Propriedades com TLA+

### Exemplo para VoicePipeline
```tla
VARIABLES state, sttResult, llmResult

Init == state = "IDLE" /\ sttResult = "" /\ llmResult = ""

StartRecording ==
    /\ state = "IDLE"
    /\ state' = "RECORDING"
    /\ UNCHANGED <<sttResult, llmResult>>

StopAndTranscribe ==
    /\ state = "RECORDING"
    /\ state' = "TRANSCRIBING"
    /\ UNCHANGED <<sttResult, llmResult>>

STTComplete ==
    /\ state = "TRANSCRIBING"
    /\ sttResult' \in STRING \ {""}
    /\ state' = "QUERYING_LLM"
    /\ UNCHANGED <<llmResult>>

-- Propriedade de Safety:
NoDeadlock == state \in {"IDLE","RECORDING","TRANSCRIBING",
                          "QUERYING_LLM","SPEAKING","ERROR"}

-- Propriedade de Liveness:
EventuallyIdle == <>(state = "IDLE")
```

---

## 7. Race Conditions — Checklist para Kotlin/Android

### Variáveis que precisam de proteção
```kotlin
// ❌ INSEGURO: var compartilhado entre coroutines sem sincronização
var isConnected: Boolean = false
launch(Dispatchers.IO) { isConnected = true }
launch(Dispatchers.Default) { if (isConnected) ... }  // race!

// ✅ SEGURO: @Volatile para leituras/escritas simples
@Volatile var isConnected: Boolean = false

// ✅ SEGURO: AtomicBoolean para CAS operations
val isConnected = AtomicBoolean(false)
isConnected.compareAndSet(false, true)

// ✅ SEGURO: StateFlow para estado observável
private val _isConnected = MutableStateFlow(false)
val isConnected = _isConnected.asStateFlow()
```

### Padrões seguros em Kotlin coroutines
```kotlin
// Mutex para seções críticas
val mutex = Mutex()
mutex.withLock {
    // seção crítica
}

// Actor para estado mutável encapsulado
val stateActor = actor<StateMessage> { ... }

// StateFlow para estado reativo
val state = MutableStateFlow(initialState)
state.update { it.copy(...) }  // atômico via CAS
```

---

## 8. Análise de Memory Leaks em Android

### Context Leaks (mais comum)
```kotlin
// ❌ LEAK: Activity context capturada em objeto de longa vida
class LlmClient(val context: Context) {  // se context = Activity → leak
    // cliente pode sobreviver à Activity
}

// ✅ CORRETO: Application context para objetos de longa vida
class LlmClient(val context: Context) {
    init {
        // usar context.applicationContext para operações longas
    }
}
```

### Coroutine Leaks
```kotlin
// ❌ LEAK: coroutine lançada sem scope adequado
fun startRecording() {
    GlobalScope.launch {  // nunca cancelado!
        // ...
    }
}

// ✅ CORRETO: scope vinculado ao ciclo de vida
class EarLlmService : Service() {
    private val serviceScope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    override fun onDestroy() {
        serviceScope.cancel()  // cancela todas as coroutines
    }
}
```

### Listener Leaks (Bluetooth)
```kotlin
// ❌ LEAK: listener registrado mas nunca removido
audioManager.registerAudioDeviceCallback(callback, null)
// onDestroy esquece de chamar unregisterAudioDeviceCallback

// ✅ CORRETO: registro/desregistro simétrico
override fun onStart() { register(callback) }
override fun onStop() { unregister(callback) }
```

---

## Reference: Information Theory

# Teoria da Informação Aplicada a Código e Sistemas

## 1. Entropia de Shannon em Software

### Definição Aplicada
```
H(X) = -Σ p(xᵢ) · log₂ p(xᵢ)

Interpretação em código:
- X = variável aleatória "qual estado o sistema está"
- p(xᵢ) = probabilidade de estar no estado i
- H(X) = incerteza sobre o estado → complexidade de teste

Exemplo VoicePipeline:
Estados: IDLE(70%), RECORDING(15%), TRANSCRIBING(5%),
         QUERYING_LLM(5%), SPEAKING(4%), ERROR(1%)

H = -(0.70·log₂0.70 + 0.15·log₂0.15 + 0.05·log₂0.05 +
      0.05·log₂0.05 + 0.04·log₂0.04 + 0.01·log₂0.01)
H ≈ 1.45 bits

Máximo teórico (uniform): log₂(6) ≈ 2.58 bits
Eficiência de entropia: 1.45/2.58 ≈ 56% — baixa entropia = sistema bem estruturado
```

### Entropia de Interface
```
Para uma função f: I → O
H(O) = entropia dos possíveis outputs
H(O|I) = entropia de O dado I (incerteza residual)

Informação mútua I(I;O) = H(O) - H(O|I)
  = quanto a entrada reduz a incerteza sobre a saída

Objetivo ideal: I(I;O) = H(O) → entrada determina completamente saída
  Equivale à função sendo determinística (sem nondeterminismo)

Caso problemático em Auri:
BluetoothController.connect() — output depende de estado do dispositivo BT
H(success|deviceAddress) > 0 (conexão pode falhar por razões externas)
→ sistema inerentemente não-determinístico neste ponto
→ tratamento de erro é mandatório, não opcional
```

---

## 2. Complexidade de Kolmogorov

### Definição
```
K(x) = comprimento do menor programa que produz x

Interpretação prática:
- K(código) = complexidade algorítmica intrínseca
- Código não pode ser comprimido abaixo de K(código)
- Se código tem padrões repetitivos → K(código) << |código|
  → oportunidade de abstração/refatoração
```

### Aplicação: Detectar Código Duplicado
```
Princípio: se compress(file1 + file2) << |file1| + |file2|
então file1 e file2 têm estrutura compartilhada → extrair abstração

Ferramenta prática: medir ratio de compressão
ratio = compress(código) / |código|

Limites heurísticos:
ratio < 0.3: muito código repetitivo → refatorar urgente
ratio 0.3-0.5: alguma repetição → oportunidade de refatoração
ratio > 0.5: código diverso/expressivo → aceitável
```

---

## 3. Capacidade de Canal e Throughput

### Modelo de Ruído para Sistemas BT
```
Canal de Shannon com ruído:
- Capacidade C = B · log₂(1 + S/N) bits/s
  B = bandwidth (Hz), S/N = signal-to-noise ratio

Para SCO (Bluetooth headset mic):
- B = 8kHz (narrowband) ou 16kHz (wideband)
- Qualidade de voz: S/N típico 20-30dB em ambiente silencioso
- C ≈ 8000 · log₂(101) ≈ 53,000 bits/s ≈ 53 kbps

PCM recording no app:
- 16kHz, 16-bit → 256 kbps bruto
- Compressão efetiva do canal BT SCO: 64 kbps (CVSD codec)
- Perda de qualidade: ~75% da resolução PCM
→ justifica preferência por BLE Audio sobre SCO quando disponível
```

### Pipeline de Throughput
```
Modelo de gargalo (teoria de filas em série):
Pipeline: Audio → STT → LLM → TTS

Capacidade de cada estágio:
Stage       | Rate      | Buffer   | Observação
Audio cap.  | 256 kbps  | Ring buf | Contínuo
STT online  | ~500ms/req| 1 req    | Latência dominante
LLM (API)   | ~500 tok/s| 1 req    | Throughput alto
LLM (Ollama)| ~3 tok/s  | 1 req    | GARGALO A04
TTS         | ~200 ms   | 1 req    | Rápido

Throughput do pipeline = min(taxas) = 3 tok/s (Ollama A04)
Equivale a ~15 palavras/minuto (muito lento para conversa fluida)
→ Justifica recomendação de usar OpenAI API para conversação real-time
```

---

## 4. Teoria da Codificação Aplicada a APIs

### Redundância e Robustez
```
Um protocolo com redundância tem:
- Taxa de código: r = k/n (k = bits úteis, n = bits transmitidos)
- r = 1: sem redundância (frágil)
- r < 1: com redundância (tolerante a erros)

Em APIs REST/LLM:
- Retry logic = redundância temporal: r = 1/(tentativas)
- Idempotency keys = deduplicação: garante exatamente 1 processamento
- Checksum/hash = redundância de verificação

Para Auri AuriToolExecutor:
- Sem idempotency keys: r = 1 (frágil a retries)
- Com idempotency keys: r = 1/max_retries (robusto)
```

### Compressão e Eficiência de Contexto LLM
```
LLMs têm contexto finito (ex: 128k tokens para Claude)
Cada conversa consome: Σ len(mensagem_i) tokens

Otimização de contexto como problema de compressão:
- Manter apenas informação essencial para resposta seguinte
- Sumarizar histórico para economizar tokens
- "Esquecimento" estratégico de contexto irrelevante

Para Auri:
Estratégia ótima de gerenciamento de contexto:
1. Manter últimas N trocas completas (N=5-10)
2. Sumarizar trocas mais antigas em 1-2 frases
3. Sempre manter: contexto do sistema + última mensagem do usuário
4. Custo estimado por requisição: ~200-500 tokens com esta estratégia
```

---

## 5. Teoria da Decisão Bayesiana

### Diagnóstico de Bugs como Inferência Bayesiana
```
P(bug=B | observação=O) = P(O|B) · P(B) / P(O)

Onde:
- P(B) = prior: frequência histórica deste tipo de bug
- P(O|B) = likelihood: probabilidade de ver este log/comportamento dado o bug
- P(O) = evidência: normalização

Exemplo Auri:
Bug: "pipeline trava em TRANSCRIBING"
Observação: "STT retorna resultado vazio, UI congela"

Hipóteses e priors estimados:
H1: STT result handler não atualiza state (P = 0.3)
H2: coroutine canceled antes de processar resultado (P = 0.25)
H3: exception silenciosa em emit() (P = 0.2)
H4: MainActivity lifecycle issue (P = 0.15)
H5: outra causa (P = 0.1)

Após análise do código:
P(vazio|H1) = 0.9 → P(H1|vazio) ≈ 0.52 — MAIS PROVÁVEL
P(vazio|H2) = 0.7 → P(H2|vazio) ≈ 0.34
P(vazio|H3) = 0.3 → P(H3|vazio) ≈ 0.11

Diagnóstico bayesiano: investigar H1 primeiro (52%), depois H2 (34%)
```

### Estimativa de Confiança em Análises
```
Quando Prof. Euler faz afirmações, deve incluir calibração:

"[Afirmação] — confiança: X%"

Calibração típica:
90%+: baseado em código lido + padrões bem estabelecidos
70-89%: inferência razoável + experiência com padrões similares
50-69%: hipótese plausível, necessita verificação
<50%: especulação, explicitamente marcada como tal
```

---

## 6. Complexidade de Descrição Mínima (MDL)

### Princípio MDL para Escolha de Arquitetura
```
Princípio: escolha a arquitetura que minimiza:
MDL = comprimento(modelo) + comprimento(dados|modelo)

Aplicado a padrões de design:
- MVVM: modelo compacto (3 camadas), dados bem organizados → MDL baixo
- God Class: modelo compacto (1 classe), dados confusos → MDL alto
- Microservices: modelo complexo, dados bem distribuídos → MDL médio

Para Auri MainViewModel:
Se MainViewModel tem CC > 50 e 300+ linhas:
- MDL(atual) = 1 arquivo grande = baixo overhead de modelo, alto custo de entendimento
- MDL(refatorado) = 5 ViewModels especializados = overhead de modelo, baixo custo cada
- MDL(refatorado) < MDL(atual) quando complexidade total > threshold ≈ CC 30

Recomendação: decompor quando CC total > 30 por arquivo
```

---

## 7. Teoria da Informação para Logging

### Entropia de Logs (Detectar Anomalias)
```
Log normal: mensagens seguem distribuição estacionária
- Calcular baseline: H_baseline = entropia nos primeiros N logs
- Monitor: H_current = entropia janela deslizante

Anomalia se: |H_current - H_baseline| > 2σ

Tipos de anomalias detectáveis:
1. Muitas mensagens idênticas (spamming) → entropia cai abruptamente
2. Mensagens inesperadas (novo tipo de erro) → entropia sobe
3. Sequência de eventos anormal → informação mútua entre logs muda

Para Auri FileLogWriter:
- Logar timestamps + tipo de evento + módulo
- Post-process: calcular entropia por módulo por minuto
- Threshold: alertar se H(módulo, minuto) < 0.5 ou > 3.5 bits
```

### Compressão de Logs como Detecção de Padrões
```
compress(logs) / |logs| = ratio de compressão

Baixo ratio (< 0.2): logs muito repetitivos → possível loop ou spam
Alto ratio (> 0.7): logs muito variados → possível estado errático

Sistema saudável: ratio ≈ 0.3-0.5
```
