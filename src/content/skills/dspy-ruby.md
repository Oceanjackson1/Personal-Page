---
title: "Dspy Ruby"
description: "Build type-safe LLM applications with DSPy.rb — Ruby's programmatic prompt framework with signatures, modules, agents, and optimization. Use when implementing predictable AI features, creating LLM signatures and modules, configuring language model..."
category: "research"
source: "community"
author: "Community"
tags: ["dspy", "ruby"]
date: 2026-03-20
---

# DSPy.rb

> Build LLM apps like you build software. Type-safe, modular, testable.

DSPy.rb brings software engineering best practices to LLM development. Instead of tweaking prompts, define what you want with Ruby types and let DSPy handle the rest.

## Overview

DSPy.rb is a Ruby framework for building language model applications with programmatic prompts. It provides:

- **Type-safe signatures** — Define inputs/outputs with Sorbet types
- **Modular components** — Compose and reuse LLM logic
- **Automatic optimization** — Use data to improve prompts, not guesswork
- **Production-ready** — Built-in observability, testing, and error handling

## Core Concepts

### 1. Signatures

Define interfaces between your app and LLMs using Ruby types:

```ruby
class EmailClassifier < DSPy::Signature
  description "Classify customer support emails by category and priority"

  class Priority < T::Enum
    enums do
      Low = new('low')
      Medium = new('medium')
      High = new('high')
      Urgent = new('urgent')
    end
  end

  input do
    const :email_content, String
    const :sender, String
  end

  output do
    const :category, String
    const :priority, Priority  # Type-safe enum with defined values
    const :confidence, Float
  end
end
```

### 2. Modules

Build complex workflows from simple building blocks:

- **Predict** — Basic LLM calls with signatures
- **ChainOfThought** — Step-by-step reasoning
- **ReAct** — Tool-using agents
- **CodeAct** — Dynamic code generation agents (install the `dspy-code_act` gem)

### 3. Tools & Toolsets

Create type-safe tools for agents with comprehensive Sorbet support:

```ruby
# Enum-based tool with automatic type conversion
class CalculatorTool < DSPy::Tools::Base
  tool_name 'calculator'
  tool_description 'Performs arithmetic operations with type-safe enum inputs'

  class Operation < T::Enum
    enums do
      Add = new('add')
      Subtract = new('subtract')
      Multiply = new('multiply')
      Divide = new('divide')
    end
  end

  sig { params(operation: Operation, num1: Float, num2: Float).returns(T.any(Float, String)) }
  def call(operation:, num1:, num2:)
    case operation
    when Operation::Add then num1 + num2
    when Operation::Subtract then num1 - num2
    when Operation::Multiply then num1 * num2
    when Operation::Divide
      return "Error: Division by zero" if num2 == 0
      num1 / num2
    end
  end
end

# Multi-tool toolset with rich types
class DataToolset < DSPy::Tools::Toolset
  toolset_name "data_processing"

  class Format < T::Enum
    enums do
      JSON = new('json')
      CSV = new('csv')
      XML = new('xml')
    end
  end

  tool :convert, description: "Convert data between formats"
  tool :validate, description: "Validate data structure"

  sig { params(data: String, from: Format, to: Format).returns(String) }
  def convert(data:, from:, to:)
    "Converted from #{from.serialize} to #{to.serialize}"
  end

  sig { params(data: String, format: Format).returns(T::Hash[String, T.any(String, Integer, T::Boolean)]) }
  def validate(data:, format:)
    { valid: true, format: format.serialize, row_count: 42, message: "Data validation passed" }
  end
end
```

### 4. Type System & Discriminators

DSPy.rb uses sophisticated type discrimination for complex data structures:

- **Automatic `_type` field injection** — DSPy adds discriminator fields to structs for type safety
- **Union type support** — `T.any()` types automatically disambiguated by `_type`
- **Reserved field name** — Avoid defining your own `_type` fields in structs
- **Recursive filtering** — `_type` fields filtered during deserialization at all nesting levels

### 5. Optimization

Improve accuracy with real data:

- **MIPROv2** — Advanced multi-prompt optimization with bootstrap sampling and Bayesian optimization
- **GEPA** — Genetic-Pareto Reflective Prompt Evolution with feedback maps, experiment tracking, and telemetry
- **Evaluation** — Comprehensive framework with built-in and custom metrics, error handling, and batch processing

## Quick Start

```ruby
# Install
gem 'dspy'

# Configure
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])
end

# Define a task
class SentimentAnalysis < DSPy::Signature
  description "Analyze sentiment of text"

  input do
    const :text, String
  end

  output do
    const :sentiment, String  # positive, negative, neutral
    const :score, Float       # 0.0 to 1.0
  end
end

# Use it
analyzer = DSPy::Predict.new(SentimentAnalysis)
result = analyzer.call(text: "This product is amazing!")
puts result.sentiment  # => "positive"
puts result.score      # => 0.92
```

## Provider Adapter Gems

Two strategies for connecting to LLM providers:

### Per-provider adapters (direct SDK access)

```ruby
# Gemfile
gem 'dspy'
gem 'dspy-openai'    # OpenAI, OpenRouter, Ollama
gem 'dspy-anthropic' # Claude
gem 'dspy-gemini'    # Gemini
```

Each adapter gem pulls in the official SDK (`openai`, `anthropic`, `gemini-ai`).

### Unified adapter via RubyLLM (recommended for multi-provider)

```ruby
# Gemfile
gem 'dspy'
gem 'dspy-ruby_llm'  # Routes to any provider via ruby_llm
gem 'ruby_llm'
```

RubyLLM handles provider routing based on the model name. Use the `ruby_llm/` prefix:

```ruby
DSPy.configure do |c|
  c.lm = DSPy::LM.new('ruby_llm/gemini-2.5-flash', structured_outputs: true)
  # c.lm = DSPy::LM.new('ruby_llm/claude-sonnet-4-20250514', structured_outputs: true)
  # c.lm = DSPy::LM.new('ruby_llm/gpt-4o-mini', structured_outputs: true)
end
```

## Events System

DSPy.rb ships with a structured event bus for observing runtime behavior.

### Module-Scoped Subscriptions (preferred for agents)

```ruby
class MyAgent < DSPy::Module
  subscribe 'lm.tokens', :track_tokens, scope: :descendants

  def track_tokens(_event, attrs)
    @total_tokens += attrs.fetch(:total_tokens, 0)
  end
end
```

### Global Subscriptions (for observability/integrations)

```ruby
subscription_id = DSPy.events.subscribe('score.create') do |event, attrs|
  Langfuse.export_score(attrs)
end

# Wildcards supported
DSPy.events.subscribe('llm.*') { |name, attrs| puts "[#{name}] tokens=#{attrs[:total_tokens]}" }
```

Event names use dot-separated namespaces (`llm.generate`, `react.iteration_complete`). Every event includes module metadata (`module_path`, `module_leaf`, `module_scope.ancestry_token`) for filtering.

## Lifecycle Callbacks

Rails-style lifecycle hooks ship with every `DSPy::Module`:

- **`before`** — Runs ahead of `forward` for setup (metrics, context loading)
- **`around`** — Wraps `forward`, calls `yield`, and lets you pair setup/teardown logic
- **`after`** — Fires after `forward` returns for cleanup or persistence

```ruby
class InstrumentedModule < DSPy::Module
  before :setup_metrics
  around :manage_context
  after :log_metrics

  def forward(question:)
    @predictor.call(question: question)
  end

  private

  def setup_metrics
    @start_time = Time.now
  end

  def manage_context
    load_context
    result = yield
    save_context
    result
  end

  def log_metrics
    duration = Time.now - @start_time
    Rails.logger.info "Prediction completed in #{duration}s"
  end
end
```

Execution order: before → around (before yield) → forward → around (after yield) → after. Callbacks are inherited from parent classes and execute in registration order.

## Fiber-Local LM Context

Override the language model temporarily using fiber-local storage:

```ruby
fast_model = DSPy::LM.new("openai/gpt-4o-mini", api_key: ENV['OPENAI_API_KEY'])

DSPy.with_lm(fast_model) do
  result = classifier.call(text: "test")  # Uses fast_model inside this block
end
# Back to global LM outside the block
```

**LM resolution hierarchy**: Instance-level LM → Fiber-local LM (`DSPy.with_lm`) → Global LM (`DSPy.configure`).

Use `configure_predictor` for fine-grained control over agent internals:

```ruby
agent = DSPy::ReAct.new(MySignature, tools: tools)
agent.configure { |c| c.lm = default_model }
agent.configure_predictor('thought_generator') { |c| c.lm = powerful_model }
```

## Evaluation Framework

Systematically test LLM application performance with `DSPy::Evals`:

```ruby
metric = DSPy::Metrics.exact_match(field: :answer, case_sensitive: false)
evaluator = DSPy::Evals.new(predictor, metric: metric)
result = evaluator.evaluate(test_examples, display_table: true)
puts "Pass Rate: #{(result.pass_rate * 100).round(1)}%"
```

Built-in metrics: `exact_match`, `contains`, `numeric_difference`, `composite_and`. Custom metrics return `true`/`false` or a `DSPy::Prediction` with `score:` and `feedback:` fields.

Use `DSPy::Example` for typed test data and `export_scores: true` to push results to Langfuse.

## GEPA Optimization

GEPA (Genetic-Pareto Reflective Prompt Evolution) uses reflection-driven instruction rewrites:

```ruby
gem 'dspy-gepa'

teleprompter = DSPy::Teleprompt::GEPA.new(
  metric: metric,
  reflection_lm: DSPy::ReflectionLM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY']),
  feedback_map: feedback_map,
  config: { max_metric_calls: 600, minibatch_size: 6 }
)

result = teleprompter.compile(program, trainset: train, valset: val)
optimized_program = result.optimized_program
```

The metric must return `DSPy::Prediction.new(score:, feedback:)` so the reflection model can reason about failures. Use `feedback_map` to target individual predictors in composite modules.

## Typed Context Pattern

Replace opaque string context blobs with `T::Struct` inputs. Each field gets its own `description:` annotation in the JSON schema the LLM sees:

```ruby
class NavigationContext < T::Struct
  const :workflow_hint, T.nilable(String),
        description: "Current workflow phase guidance for the agent"
  const :action_log, T::Array[String], default: [],
        description: "Compact one-line-per-action history of research steps taken"
  const :iterations_remaining, Integer,
        description: "Budget remaining. Each tool call costs 1 iteration."
end

class ToolSelectionSignature < DSPy::Signature
  input do
    const :query, String
    const :context, NavigationContext  # Structured, not an opaque string
  end

  output do
    const :tool_name, String
    const :tool_args, String, description: "JSON-encoded arguments"
  end
end
```

Benefits: type safety at compile time, per-field descriptions in the LLM schema, easy to test as value objects, extensible by adding `const` declarations.

## Schema Formats (BAML / TOON)

Control how DSPy describes signature structure to the LLM:

- **JSON Schema** (default) — Standard format, works with `structured_outputs: true`
- **BAML** (`schema_format: :baml`) — 84% token reduction for Enhanced Prompting mode. Requires `sorbet-baml` gem.
- **TOON** (`schema_format: :toon, data_format: :toon`) — Table-oriented format for both schemas and data. Enhanced Prompting mode only.

BAML and TOON apply only when `structured_outputs: false`. With `structured_outputs: true`, the provider receives JSON Schema directly.

## Storage System

Persist and reload optimized programs with `DSPy::Storage::ProgramStorage`:

```ruby
storage = DSPy::Storage::ProgramStorage.new(storage_path: "./dspy_storage")
storage.save_program(result.optimized_program, result, metadata: { optimizer: 'MIPROv2' })
```

Supports checkpoint management, optimization history tracking, and import/export between environments.

## Rails Integration

### Directory Structure

Organize DSPy components using Rails conventions:

```
app/
  entities/          # T::Struct types shared across signatures
  signatures/        # DSPy::Signature definitions
  tools/             # DSPy::Tools::Base implementations
    concerns/        # Shared tool behaviors (error handling, etc.)
  modules/           # DSPy::Module orchestrators
  services/          # Plain Ruby services that compose DSPy modules
config/
  initializers/
    dspy.rb          # DSPy + provider configuration
    feature_flags.rb # Model selection per role
spec/
  signatures/        # Schema validation tests
  tools/             # Tool unit tests
  modules/           # Integration tests with VCR
  vcr_cassettes/     # Recorded HTTP interactions
```

### Initializer

```ruby
# config/initializers/dspy.rb
Rails.application.config.after_initialize do
  next if Rails.env.test? && ENV["DSPY_ENABLE_IN_TEST"].blank?

  RubyLLM.configure do |config|
    config.gemini_api_key = ENV["GEMINI_API_KEY"] if ENV["GEMINI_API_KEY"].present?
    config.anthropic_api_key = ENV["ANTHROPIC_API_KEY"] if ENV["ANTHROPIC_API_KEY"].present?
    config.openai_api_key = ENV["OPENAI_API_KEY"] if ENV["OPENAI_API_KEY"].present?
  end

  model = ENV.fetch("DSPY_MODEL", "ruby_llm/gemini-2.5-flash")
  DSPy.configure do |config|
    config.lm = DSPy::LM.new(model, structured_outputs: true)
    config.logger = Rails.logger
  end

  # Langfuse observability (optional)
  if ENV["LANGFUSE_PUBLIC_KEY"].present? && ENV["LANGFUSE_SECRET_KEY"].present?
    DSPy::Observability.configure!
  end
end
```

### Feature-Flagged Model Selection

Use different models for different roles (fast/cheap for classification, powerful for synthesis):

```ruby
# config/initializers/feature_flags.rb
module FeatureFlags
  SELECTOR_MODEL = ENV.fetch("DSPY_SELECTOR_MODEL", "ruby_llm/gemini-2.5-flash-lite")
  SYNTHESIZER_MODEL = ENV.fetch("DSPY_SYNTHESIZER_MODEL", "ruby_llm/gemini-2.5-flash")
end
```

Then override per-tool or per-predictor:

```ruby
class ClassifyTool < DSPy::Tools::Base
  def call(query:)
    predictor = DSPy::Predict.new(ClassifyQuery)
    predictor.configure { |c| c.lm = DSPy::LM.new(FeatureFlags::SELECTOR_MODEL, structured_outputs: true) }
    predictor.call(query: query)
  end
end
```

## Schema-Driven Signatures

**Prefer typed schemas over string descriptions.** Let the type system communicate structure to the LLM rather than prose in the signature description.

### Entities as Shared Types

Define reusable `T::Struct` and `T::Enum` types in `app/entities/` and reference them across signatures:

```ruby
# app/entities/search_strategy.rb
class SearchStrategy < T::Enum
  enums do
    SingleSearch = new("single_search")
    DateDecomposition = new("date_decomposition")
  end
end

# app/entities/scored_item.rb
class ScoredItem < T::Struct
  const :id, String
  const :score, Float, description: "Relevance score 0.0-1.0"
  const :verdict, String, description: "relevant, maybe, or irrelevant"
  const :reason, String, default: ""
end
```

### Schema vs Description: When to Use Each

**Use schemas (T::Struct/T::Enum)** for:
- Multi-field outputs with specific types
- Enums with defined values the LLM must pick from
- Nested structures, arrays of typed objects
- Outputs consumed by code (not displayed to users)

**Use string descriptions** for:
- Simple single-field outputs where the type is `String`
- Natural language generation (summaries, answers)
- Fields where constraint guidance helps (e.g., `description: "YYYY-MM-DD format"`)

**Rule of thumb**: If you'd write a `case` statement on the output, it should be a `T::Enum`. If you'd call `.each` on it, it should be `T::Array[SomeStruct]`.

## Tool Patterns

### Tools That Wrap Predictions

A common pattern: tools encapsulate a DSPy prediction, adding error handling, model selection, and serialization:

```ruby
class RerankTool < DSPy::Tools::Base
  tool_name "rerank"
  tool_description "Score and rank search results by relevance"

  MAX_ITEMS = 200
  MIN_ITEMS_FOR_LLM = 5

  sig { params(query: String, items: T::Array[T::Hash[Symbol, T.untyped]]).returns(T::Hash[Symbol, T.untyped]) }
  def call(query:, items: [])
    return { scored_items: items, reranked: false } if items.size < MIN_ITEMS_FOR_LLM

    capped_items = items.first(MAX_ITEMS)
    predictor = DSPy::Predict.new(RerankSignature)
    predictor.configure { |c| c.lm = DSPy::LM.new(FeatureFlags::SYNTHESIZER_MODEL, structured_outputs: true) }

    result = predictor.call(query: query, items: capped_items)
    { scored_items: result.scored_items, reranked: true }
  rescue => e
    Rails.logger.warn "[RerankTool] LLM rerank failed: #{e.message}"
    { error: "Rerank failed: #{e.message}", scored_items: items, reranked: false }
  end
end
```

**Key patterns:**
- Short-circuit LLM calls when unnecessary (small data, trivial cases)
- Cap input size to prevent token overflow
- Per-tool model selection via `configure`
- Graceful error handling with fallback data

### Error Handling Concern

```ruby
module ErrorHandling
  extend ActiveSupport::Concern

  private

  def safe_predict(signature_class, **inputs)
    predictor = DSPy::Predict.new(signature_class)
    yield predictor if block_given?
    predictor.call(**inputs)
  rescue Faraday::Error, Net::HTTPError => e
    Rails.logger.error "[#{self.class.name}] API error: #{e.message}"
    nil
  rescue JSON::ParserError => e
    Rails.logger.error "[#{self.class.name}] Invalid LLM output: #{e.message}"
    nil
  end
end
```

## Observability

### Tracing with DSPy::Context

Wrap operations in spans for Langfuse/OpenTelemetry visibility:

```ruby
result = DSPy::Context.with_span(
  operation: "tool_selector.select",
  "dspy.module" => "ToolSelector",
  "tool_selector.tools" => tool_names.join(",")
) do
  @predictor.call(query: query, context: context, available_tools: schemas)
end
```

### Setup for Langfuse

```ruby
# Gemfile
gem 'dspy-o11y'
gem 'dspy-o11y-langfuse'

# .env
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
DSPY_TELEMETRY_BATCH_SIZE=5
```

Every `DSPy::Predict`, `DSPy::ReAct`, and tool call is automatically traced when observability is configured.

### Score Reporting

Report evaluation scores to Langfuse:

```ruby
DSPy.score(name: "relevance", value: 0.85, trace_id: current_trace_id)
```

## Testing

### VCR Setup for Rails

```ruby
VCR.configure do |config|
  config.cassette_library_dir = "spec/vcr_cassettes"
  config.hook_into :webmock
  config.configure_rspec_metadata!
  config.filter_sensitive_data('<GEMINI_API_KEY>') { ENV['GEMINI_API_KEY'] }
  config.filter_sensitive_data('<OPENAI_API_KEY>') { ENV['OPENAI_API_KEY'] }
end
```

### Signature Schema Tests

Test that signatures produce valid schemas without calling any LLM:

```ruby
RSpec.describe ClassifyResearchQuery do
  it "has required input fields" do
    schema = described_class.input_json_schema
    expect(schema[:required]).to include("query")
  end

  it "has typed output fields" do
    schema = described_class.output_json_schema
    expect(schema[:properties]).to have_key(:search_strategy)
  end
end
```

### Tool Tests with Mocked Predictions

```ruby
RSpec.describe RerankTool do
  let(:tool) { described_class.new }

  it "skips LLM for small result sets" do
    expect(DSPy::Predict).not_to receive(:new)
    result = tool.call(query: "test", items: [{ id: "1" }])
    expect(result[:reranked]).to be false
  end

  it "calls LLM for large result sets", :vcr do
    items = 10.times.map { |i| { id: i.to_s, title: "Item #{i}" } }
    result = tool.call(query: "relevant items", items: items)
    expect(result[:reranked]).to be true
  end
end
```

## Resources

- [core-concepts.md](./references/core-concepts.md) — Signatures, modules, predictors, type system deep-dive
- [toolsets.md](./references/toolsets.md) — Tools::Base, Tools::Toolset DSL, type safety, testing
- [providers.md](./references/providers.md) — Provider adapters, RubyLLM, fiber-local LM context, compatibility matrix
- [optimization.md](./references/optimization.md) — MIPROv2, GEPA, evaluation framework, storage system
- [observability.md](./references/observability.md) — Event system, dspy-o11y gems, Langfuse, score reporting
- [signature-template.rb](./assets/signature-template.rb) — Signature scaffold with T::Enum, Date/Time, defaults, union types
- [module-template.rb](./assets/module-template.rb) — Module scaffold with .call(), lifecycle callbacks, fiber-local LM
- [config-template.rb](./assets/config-template.rb) — Rails initializer with RubyLLM, observability, feature flags

## Key URLs

- Homepage: https://oss.vicente.services/dspy.rb/
- GitHub: https://github.com/vicentereig/dspy.rb
- Documentation: https://oss.vicente.services/dspy.rb/getting-started/

## Guidelines for Claude

When helping users with DSPy.rb:

1. **Schema over prose** — Define output structure with `T::Struct` and `T::Enum` types, not string descriptions
2. **Entities in `app/entities/`** — Extract shared types so signatures stay thin
3. **Per-tool model selection** — Use `predictor.configure { |c| c.lm = ... }` to pick the right model per task
4. **Short-circuit LLM calls** — Skip the LLM for trivial cases (small data, cached results)
5. **Cap input sizes** — Prevent token overflow by limiting array sizes before sending to LLM
6. **Test schemas without LLM** — Validate `input_json_schema` and `output_json_schema` in unit tests
7. **VCR for integration tests** — Record real HTTP interactions, never mock LLM responses by hand
8. **Trace with spans** — Wrap tool calls in `DSPy::Context.with_span` for observability
9. **Graceful degradation** — Always rescue LLM errors and return fallback data

### Signature Best Practices

**Keep description concise** — The signature `description` should state the goal, not the field details:

```ruby
# Good — concise goal
class ParseOutline < DSPy::Signature
  description 'Extract block-level structure from HTML as a flat list of skeleton sections.'

  input do
    const :html, String, description: 'Raw HTML to parse'
  end

  output do
    const :sections, T::Array[Section], description: 'Block elements: headings, paragraphs, code blocks, lists'
  end
end
```

**Use defaults over nilable arrays** — For OpenAI structured outputs compatibility:

```ruby
# Good — works with OpenAI structured outputs
class ASTNode < T::Struct
  const :children, T::Array[ASTNode], default: []
end
```

### Recursive Types with `$defs`

DSPy.rb supports recursive types in structured outputs using JSON Schema `$defs`:

```ruby
class TreeNode < T::Struct
  const :value, String
  const :children, T::Array[TreeNode], default: []  # Self-reference
end
```

The schema generator automatically creates `#/$defs/TreeNode` references for recursive types, compatible with OpenAI and Gemini structured outputs.

### Field Descriptions for T::Struct

DSPy.rb extends T::Struct to support field-level `description:` kwargs that flow to JSON Schema:

```ruby
class ASTNode < T::Struct
  const :node_type, NodeType, description: 'The type of node (heading, paragraph, etc.)'
  const :text, String, default: "", description: 'Text content of the node'
  const :level, Integer, default: 0  # No description — field is self-explanatory
  const :children, T::Array[ASTNode], default: []
end
```

**When to use field descriptions**: complex field semantics, enum-like strings, constrained values, nested structs with ambiguous names. **When to skip**: self-explanatory fields like `name`, `id`, `url`, or boolean flags.

## Version

Current: 0.34.3

---

## Reference: Core Concepts

# DSPy.rb Core Concepts

## Signatures

Signatures define the interface between application code and language models. They specify inputs, outputs, and a task description using Sorbet types for compile-time and runtime type safety.

### Structure

```ruby
class ClassifyEmail < DSPy::Signature
  description "Classify customer support emails by urgency and category"

  input do
    const :subject, String
    const :body, String
  end

  output do
    const :category, String
    const :urgency, String
  end
end
```

### Supported Types

| Type | JSON Schema | Notes |
|------|-------------|-------|
| `String` | `string` | Required string |
| `Integer` | `integer` | Whole numbers |
| `Float` | `number` | Decimal numbers |
| `T::Boolean` | `boolean` | true/false |
| `T::Array[X]` | `array` | Typed arrays |
| `T::Hash[K, V]` | `object` | Typed key-value maps |
| `T.nilable(X)` | nullable | Optional fields |
| `Date` | `string` (ISO 8601) | Auto-converted |
| `DateTime` | `string` (ISO 8601) | Preserves timezone |
| `Time` | `string` (ISO 8601) | Converted to UTC |

### Date and Time Types

Date, DateTime, and Time fields serialize to ISO 8601 strings and auto-convert back to Ruby objects on output.

```ruby
class EventScheduler < DSPy::Signature
  description "Schedule events based on requirements"

  input do
    const :start_date, Date                  # ISO 8601: YYYY-MM-DD
    const :preferred_time, DateTime          # ISO 8601 with timezone
    const :deadline, Time                    # Converted to UTC
    const :end_date, T.nilable(Date)         # Optional date
  end

  output do
    const :scheduled_date, Date              # String from LLM, auto-converted to Date
    const :event_datetime, DateTime          # Preserves timezone info
    const :created_at, Time                  # Converted to UTC
  end
end

predictor = DSPy::Predict.new(EventScheduler)
result = predictor.call(
  start_date: "2024-01-15",
  preferred_time: "2024-01-15T10:30:45Z",
  deadline: Time.now,
  end_date: nil
)

result.scheduled_date.class  # => Date
result.event_datetime.class  # => DateTime
```

Timezone conventions follow ActiveRecord: Time objects convert to UTC, DateTime objects preserve timezone, Date objects are timezone-agnostic.

### Enums with T::Enum

Define constrained output values using `T::Enum` classes. Do not use inline `T.enum([...])` syntax.

```ruby
class SentimentAnalysis < DSPy::Signature
  description "Analyze sentiment of text"

  class Sentiment < T::Enum
    enums do
      Positive = new('positive')
      Negative = new('negative')
      Neutral = new('neutral')
    end
  end

  input do
    const :text, String
  end

  output do
    const :sentiment, Sentiment
    const :confidence, Float
  end
end

predictor = DSPy::Predict.new(SentimentAnalysis)
result = predictor.call(text: "This product is amazing!")

result.sentiment              # => #<Sentiment::Positive>
result.sentiment.serialize    # => "positive"
result.confidence             # => 0.92
```

Enum matching is case-insensitive. The LLM returning `"POSITIVE"` matches `new('positive')`.

### Default Values

Default values work on both inputs and outputs. Input defaults reduce caller boilerplate. Output defaults provide fallbacks when the LLM omits optional fields.

```ruby
class SmartSearch < DSPy::Signature
  description "Search with intelligent defaults"

  input do
    const :query, String
    const :max_results, Integer, default: 10
    const :language, String, default: "English"
  end

  output do
    const :results, T::Array[String]
    const :total_found, Integer
    const :cached, T::Boolean, default: false
  end
end

search = DSPy::Predict.new(SmartSearch)
result = search.call(query: "Ruby programming")
# max_results defaults to 10, language defaults to "English"
# If LLM omits `cached`, it defaults to false
```

### Field Descriptions

Add `description:` to any field to guide the LLM on expected content. These descriptions appear in the generated JSON schema sent to the model.

```ruby
class ASTNode < T::Struct
  const :node_type, String, description: "The type of AST node (heading, paragraph, code_block)"
  const :text, String, default: "", description: "Text content of the node"
  const :level, Integer, default: 0, description: "Heading level 1-6, only for heading nodes"
  const :children, T::Array[ASTNode], default: []
end

ASTNode.field_descriptions[:node_type]  # => "The type of AST node ..."
ASTNode.field_descriptions[:children]   # => nil (no description set)
```

Field descriptions also work inside signature `input` and `output` blocks:

```ruby
class ExtractEntities < DSPy::Signature
  description "Extract named entities from text"

  input do
    const :text, String, description: "Raw text to analyze"
    const :language, String, default: "en", description: "ISO 639-1 language code"
  end

  output do
    const :entities, T::Array[String], description: "List of extracted entity names"
    const :count, Integer, description: "Total number of unique entities found"
  end
end
```

### Schema Formats

DSPy.rb supports three schema formats for communicating type structure to LLMs.

#### JSON Schema (default)

Verbose but universally supported. Access via `YourSignature.output_json_schema`.

#### BAML Schema

Compact format that reduces schema tokens by 80-85%. Requires the `sorbet-baml` gem.

```ruby
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'],
    schema_format: :baml
  )
end
```

BAML applies only in Enhanced Prompting mode (`structured_outputs: false`). When `structured_outputs: true`, the provider receives JSON Schema directly.

#### TOON Schema + Data Format

Table-oriented text format that shrinks both schema definitions and prompt values.

```ruby
DSPy.configure do |c|
  c.lm = DSPy::LM.new('openai/gpt-4o-mini',
    api_key: ENV['OPENAI_API_KEY'],
    schema_format: :toon,
    data_format:   :toon
  )
end
```

`schema_format: :toon` replaces the schema block in the system prompt. `data_format: :toon` renders input values and output templates inside `toon` fences. Only works with Enhanced Prompting mode. The `sorbet-toon` gem is included automatically as a dependency.

### Recursive Types

Structs that reference themselves produce `$defs` entries in the generated JSON schema, using `$ref` pointers to avoid infinite recursion.

```ruby
class ASTNode < T::Struct
  const :node_type, String
  const :text, String, default: ""
  const :children, T::Array[ASTNode], default: []
end
```

The schema generator detects the self-reference in `T::Array[ASTNode]` and emits:

```json
{
  "$defs": {
    "ASTNode": { "type": "object", "properties": { ... } }
  },
  "properties": {
    "children": {
      "type": "array",
      "items": { "$ref": "#/$defs/ASTNode" }
    }
  }
}
```

Access the schema with accumulated definitions via `YourSignature.output_json_schema_with_defs`.

### Union Types with T.any()

Specify fields that accept multiple types:

```ruby
output do
  const :result, T.any(Float, String)
end
```

For struct unions, DSPy.rb automatically adds a `_type` discriminator field to each struct's JSON schema. The LLM returns `_type` in its response, and DSPy converts the hash to the correct struct instance.

```ruby
class CreateTask < T::Struct
  const :title, String
  const :priority, String
end

class DeleteTask < T::Struct
  const :task_id, String
  const :reason, T.nilable(String)
end

class TaskRouter < DSPy::Signature
  description "Route user request to the appropriate task action"

  input do
    const :request, String
  end

  output do
    const :action, T.any(CreateTask, DeleteTask)
  end
end

result = DSPy::Predict.new(TaskRouter).call(request: "Create a task for Q4 review")
result.action.class  # => CreateTask
result.action.title  # => "Q4 Review"
```

Pattern matching works on the result:

```ruby
case result.action
when CreateTask then puts "Creating: #{result.action.title}"
when DeleteTask then puts "Deleting: #{result.action.task_id}"
end
```

Union types also work inside arrays for heterogeneous collections:

```ruby
output do
  const :events, T::Array[T.any(LoginEvent, PurchaseEvent)]
end
```

Limit unions to 2-4 types for reliable LLM comprehension. Use clear struct names since they become the `_type` discriminator values.

---

## Modules

Modules are composable building blocks that wrap predictors. Define a `forward` method; invoke the module with `.call()`.

### Basic Structure

```ruby
class SentimentAnalyzer < DSPy::Module
  def initialize
    super
    @predictor = DSPy::Predict.new(SentimentSignature)
  end

  def forward(text:)
    @predictor.call(text: text)
  end
end

analyzer = SentimentAnalyzer.new
result = analyzer.call(text: "I love this product!")

result.sentiment    # => "positive"
result.confidence   # => 0.9
```

**API rules:**
- Invoke modules and predictors with `.call()`, not `.forward()`.
- Access result fields with `result.field`, not `result[:field]`.

### Module Composition

Combine multiple modules through explicit method calls in `forward`:

```ruby
class DocumentProcessor < DSPy::Module
  def initialize
    super
    @classifier = DocumentClassifier.new
    @summarizer = DocumentSummarizer.new
  end

  def forward(document:)
    classification = @classifier.call(content: document)
    summary = @summarizer.call(content: document)

    {
      document_type: classification.document_type,
      summary: summary.summary
    }
  end
end
```

### Lifecycle Callbacks

Modules support `before`, `after`, and `around` callbacks on `forward`. Declare them as class-level macros referencing private methods.

#### Execution order

1. `before` callbacks (in registration order)
2. `around` callbacks (before `yield`)
3. `forward` method
4. `around` callbacks (after `yield`)
5. `after` callbacks (in registration order)

```ruby
class InstrumentedModule < DSPy::Module
  before :setup_metrics
  after :log_metrics
  around :manage_context

  def initialize
    super
    @predictor = DSPy::Predict.new(MySignature)
    @metrics = {}
  end

  def forward(question:)
    @predictor.call(question: question)
  end

  private

  def setup_metrics
    @metrics[:start_time] = Time.now
  end

  def manage_context
    load_context
    result = yield
    save_context
    result
  end

  def log_metrics
    @metrics[:duration] = Time.now - @metrics[:start_time]
  end
end
```

Multiple callbacks of the same type execute in registration order. Callbacks inherit from parent classes; parent callbacks run first.

#### Around callbacks

Around callbacks must call `yield` to execute the wrapped method and return the result:

```ruby
def with_retry
  retries = 0
  begin
    yield
  rescue StandardError => e
    retries += 1
    retry if retries < 3
    raise e
  end
end
```

### Instruction Update Contract

Teleprompters (GEPA, MIPROv2) require modules to expose immutable update hooks. Include `DSPy::Mixins::InstructionUpdatable` and implement `with_instruction` and `with_examples`, each returning a new instance:

```ruby
class SentimentPredictor < DSPy::Module
  include DSPy::Mixins::InstructionUpdatable

  def initialize
    super
    @predictor = DSPy::Predict.new(SentimentSignature)
  end

  def with_instruction(instruction)
    clone = self.class.new
    clone.instance_variable_set(:@predictor, @predictor.with_instruction(instruction))
    clone
  end

  def with_examples(examples)
    clone = self.class.new
    clone.instance_variable_set(:@predictor, @predictor.with_examples(examples))
    clone
  end
end
```

If a module omits these hooks, teleprompters raise `DSPy::InstructionUpdateError` instead of silently mutating state.

---

## Predictors

Predictors are execution engines that take a signature and produce structured results from a language model. DSPy.rb provides four predictor types.

### Predict

Direct LLM call with typed input/output. Fastest option, lowest token usage.

```ruby
classifier = DSPy::Predict.new(ClassifyText)
result = classifier.call(text: "Technical document about APIs")

result.sentiment    # => #<Sentiment::Positive>
result.topics       # => ["APIs", "technical"]
result.confidence   # => 0.92
```

### ChainOfThought

Adds a `reasoning` field to the output automatically. The model generates step-by-step reasoning before the final answer. Do not define a `:reasoning` field in the signature output when using ChainOfThought.

```ruby
class SolveMathProblem < DSPy::Signature
  description "Solve mathematical word problems step by step"

  input do
    const :problem, String
  end

  output do
    const :answer, String
    # :reasoning is added automatically by ChainOfThought
  end
end

solver = DSPy::ChainOfThought.new(SolveMathProblem)
result = solver.call(problem: "Sarah has 15 apples. She gives 7 away and buys 12 more.")

result.reasoning  # => "Step by step: 15 - 7 = 8, then 8 + 12 = 20"
result.answer     # => "20 apples"
```

Use ChainOfThought for complex analysis, multi-step reasoning, or when explainability matters.

### ReAct

Reasoning + Action agent that uses tools in an iterative loop. Define tools by subclassing `DSPy::Tools::Base`. Group related tools with `DSPy::Tools::Toolset`.

```ruby
class WeatherTool < DSPy::Tools::Base
  extend T::Sig

  tool_name "weather"
  tool_description "Get weather information for a location"

  sig { params(location: String).returns(String) }
  def call(location:)
    { location: location, temperature: 72, condition: "sunny" }.to_json
  end
end

class TravelSignature < DSPy::Signature
  description "Help users plan travel"

  input do
    const :destination, String
  end

  output do
    const :recommendations, String
  end
end

agent = DSPy::ReAct.new(
  TravelSignature,
  tools: [WeatherTool.new],
  max_iterations: 5
)

result = agent.call(destination: "Tokyo, Japan")
result.recommendations  # => "Visit Senso-ji Temple early morning..."
result.history          # => Array of reasoning steps, actions, observations
result.iterations       # => 3
result.tools_used       # => ["weather"]
```

Use toolsets to expose multiple tool methods from a single class:

```ruby
text_tools = DSPy::Tools::TextProcessingToolset.to_tools
agent = DSPy::ReAct.new(MySignature, tools: text_tools)
```

### CodeAct

Think-Code-Observe agent that synthesizes and executes Ruby code. Ships as a separate gem.

```ruby
# Gemfile
gem 'dspy-code_act', '~> 0.29'
```

```ruby
programmer = DSPy::CodeAct.new(ProgrammingSignature, max_iterations: 10)
result = programmer.call(task: "Calculate the factorial of 20")
```

### Predictor Comparison

| Predictor | Speed | Token Usage | Best For |
|-----------|-------|-------------|----------|
| Predict | Fastest | Low | Classification, extraction |
| ChainOfThought | Moderate | Medium-High | Complex reasoning, analysis |
| ReAct | Slower | High | Multi-step tasks with tools |
| CodeAct | Slowest | Very High | Dynamic programming, calculations |

### Concurrent Predictions

Process multiple independent predictions simultaneously using `Async::Barrier`:

```ruby
require 'async'
require 'async/barrier'

analyzer = DSPy::Predict.new(ContentAnalyzer)
documents = ["Text one", "Text two", "Text three"]

Async do
  barrier = Async::Barrier.new

  tasks = documents.map do |doc|
    barrier.async { analyzer.call(content: doc) }
  end

  barrier.wait
  predictions = tasks.map(&:wait)

  predictions.each { |p| puts p.sentiment }
end
```

Add `gem 'async', '~> 2.29'` to the Gemfile. Handle errors within each `barrier.async` block to prevent one failure from cancelling others:

```ruby
barrier.async do
  begin
    analyzer.call(content: doc)
  rescue StandardError => e
    nil
  end
end
```

### Few-Shot Examples and Instruction Tuning

```ruby
classifier = DSPy::Predict.new(SentimentAnalysis)

examples = [
  DSPy::FewShotExample.new(
    input: { text: "Love it!" },
    output: { sentiment: "positive", confidence: 0.95 }
  )
]

optimized = classifier.with_examples(examples)
tuned = classifier.with_instruction("Be precise and confident.")
```

---

## Type System

### Automatic Type Conversion

DSPy.rb v0.9.0+ automatically converts LLM JSON responses to typed Ruby objects:

- **Enums**: String values become `T::Enum` instances (case-insensitive)
- **Structs**: Nested hashes become `T::Struct` objects
- **Arrays**: Elements convert recursively
- **Defaults**: Missing fields use declared defaults

### Discriminators for Union Types

When a field uses `T.any()` with struct types, DSPy adds a `_type` field to each struct's schema. On deserialization, `_type` selects the correct struct class:

```json
{
  "action": {
    "_type": "CreateTask",
    "title": "Review Q4 Report"
  }
}
```

DSPy matches `"CreateTask"` against the union members and instantiates the correct struct. No manual discriminator field is needed.

### Recursive Types

Structs referencing themselves are supported. The schema generator tracks visited types and produces `$ref` pointers under `$defs`:

```ruby
class TreeNode < T::Struct
  const :label, String
  const :children, T::Array[TreeNode], default: []
end
```

The generated schema uses `"$ref": "#/$defs/TreeNode"` for the children array items, preventing infinite schema expansion.

### Nesting Depth

- 1-2 levels: reliable across all providers.
- 3-4 levels: works but increases schema complexity.
- 5+ levels: may trigger OpenAI depth validation warnings and reduce LLM accuracy. Flatten deeply nested structures or split into multiple signatures.

### Tips

- Prefer `T::Array[X], default: []` over `T.nilable(T::Array[X])` -- the nilable form causes schema issues with OpenAI structured outputs.
- Use clear struct names for union types since they become `_type` discriminator values.
- Limit union types to 2-4 members for reliable model comprehension.
- Check schema compatibility with `DSPy::OpenAI::LM::SchemaConverter.validate_compatibility(schema)`.

---

## Reference: Observability

# DSPy.rb Observability

DSPy.rb provides an event-driven observability system built on OpenTelemetry. The system replaces monkey-patching with structured event emission, pluggable listeners, automatic span creation, and non-blocking Langfuse export.

## Event System

### Emitting Events

Emit structured events with `DSPy.event`:

```ruby
DSPy.event('lm.tokens', {
  'gen_ai.system' => 'openai',
  'gen_ai.request.model' => 'gpt-4',
  input_tokens: 150,
  output_tokens: 50,
  total_tokens: 200
})
```

Event names are **strings** with dot-separated namespaces (e.g., `'llm.generate'`, `'react.iteration_complete'`, `'chain_of_thought.reasoning_complete'`). Do not use symbols for event names.

Attributes must be JSON-serializable. DSPy automatically merges context (trace ID, module stack) and creates OpenTelemetry spans.

### Global Subscriptions

Subscribe to events across the entire application with `DSPy.events.subscribe`:

```ruby
# Exact event name
subscription_id = DSPy.events.subscribe('lm.tokens') do |event_name, attrs|
  puts "Tokens used: #{attrs[:total_tokens]}"
end

# Wildcard pattern -- matches llm.generate, llm.stream, etc.
DSPy.events.subscribe('llm.*') do |event_name, attrs|
  track_llm_usage(attrs)
end

# Catch-all wildcard
DSPy.events.subscribe('*') do |event_name, attrs|
  log_everything(event_name, attrs)
end
```

Use global subscriptions for cross-cutting concerns: observability exporters (Langfuse, Datadog), centralized logging, metrics collection.

### Module-Scoped Subscriptions

Declare listeners inside a `DSPy::Module` subclass. Subscriptions automatically scope to the module instance and its descendants:

```ruby
class ResearchReport < DSPy::Module
  subscribe 'lm.tokens', :track_tokens, scope: :descendants

  def initialize
    super
    @outliner = DSPy::Predict.new(OutlineSignature)
    @writer   = DSPy::Predict.new(SectionWriterSignature)
    @token_count = 0
  end

  def forward(question:)
    outline = @outliner.call(question: question)
    outline.sections.map do |title|
      draft = @writer.call(question: question, section_title: title)
      { title: title, body: draft.paragraph }
    end
  end

  def track_tokens(_event, attrs)
    @token_count += attrs.fetch(:total_tokens, 0)
  end
end
```

The `scope:` parameter accepts:
- `:descendants` (default) -- receives events from the module **and** every nested module invoked inside it.
- `DSPy::Module::SubcriptionScope::SelfOnly` -- restricts delivery to events emitted by the module instance itself; ignores descendants.

Inspect active subscriptions with `registered_module_subscriptions`. Tear down with `unsubscribe_module_events`.

### Unsubscribe and Cleanup

Remove a global listener by subscription ID:

```ruby
id = DSPy.events.subscribe('llm.*') { |name, attrs| }
DSPy.events.unsubscribe(id)
```

Build tracker classes that manage their own subscription lifecycle:

```ruby
class TokenBudgetTracker
  def initialize(budget:)
    @budget = budget
    @usage  = 0
    @subscriptions = []
    @subscriptions << DSPy.events.subscribe('lm.tokens') do |_event, attrs|
      @usage += attrs.fetch(:total_tokens, 0)
      warn("Budget hit") if @usage >= @budget
    end
  end

  def unsubscribe
    @subscriptions.each { |id| DSPy.events.unsubscribe(id) }
    @subscriptions.clear
  end
end
```

### Clearing Listeners in Tests

Call `DSPy.events.clear_listeners` in `before`/`after` blocks to prevent cross-contamination between test cases:

```ruby
RSpec.configure do |config|
  config.after(:each) { DSPy.events.clear_listeners }
end
```

## dspy-o11y Gems

Three gems compose the observability stack:

| Gem | Purpose |
|---|---|
| `dspy` | Core event bus (`DSPy.event`, `DSPy.events`) -- always available |
| `dspy-o11y` | OpenTelemetry spans, `AsyncSpanProcessor`, `DSPy::Context.with_span` helpers |
| `dspy-o11y-langfuse` | Langfuse adapter -- configures OTLP exporter targeting Langfuse endpoints |

### Installation

```ruby
# Gemfile
gem 'dspy'
gem 'dspy-o11y'           # core spans + helpers
gem 'dspy-o11y-langfuse'  # Langfuse/OpenTelemetry adapter (optional)
```

If the optional gems are absent, DSPy falls back to logging-only mode with no errors.

## Langfuse Integration

### Environment Variables

```bash
# Required
export LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
export LANGFUSE_SECRET_KEY=sk-lf-your-secret-key

# Optional (defaults to https://cloud.langfuse.com)
export LANGFUSE_HOST=https://us.cloud.langfuse.com

# Tuning (optional)
export DSPY_TELEMETRY_BATCH_SIZE=100        # spans per export batch (default 100)
export DSPY_TELEMETRY_QUEUE_SIZE=1000       # max queued spans (default 1000)
export DSPY_TELEMETRY_EXPORT_INTERVAL=60    # seconds between timed exports (default 60)
export DSPY_TELEMETRY_SHUTDOWN_TIMEOUT=10   # seconds to drain on shutdown (default 10)
```

### Automatic Configuration

Call `DSPy::Observability.configure!` once at boot (it is already called automatically when `require 'dspy'` runs and Langfuse env vars are present):

```ruby
require 'dspy'
# If LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are set,
# DSPy::Observability.configure! runs automatically and:
#   1. Configures the OpenTelemetry SDK with an OTLP exporter
#   2. Creates dual output: structured logs AND OpenTelemetry spans
#   3. Exports spans to Langfuse using proper authentication
#   4. Falls back gracefully if gems are missing
```

Verify status with `DSPy::Observability.enabled?`.

### Automatic Tracing

With observability enabled, every `DSPy::Module#forward` call, LM request, and tool invocation creates properly nested spans. Langfuse receives hierarchical traces:

```
Trace: abc-123-def
+-- ChainOfThought.forward [2000ms]  (observation type: chain)
    +-- llm.generate [1000ms]        (observation type: generation)
        Model: gpt-4-0613
        Tokens: 100 in / 50 out / 150 total
```

DSPy maps module classes to Langfuse observation types automatically via `DSPy::ObservationType.for_module_class`:

| Module | Observation Type |
|---|---|
| `DSPy::LM` (raw chat) | `generation` |
| `DSPy::ChainOfThought` | `chain` |
| `DSPy::ReAct` | `agent` |
| Tool invocations | `tool` |
| Memory/retrieval | `retriever` |
| Embedding engines | `embedding` |
| Evaluation modules | `evaluator` |
| Generic operations | `span` |

## Score Reporting

### DSPy.score API

Report evaluation scores with `DSPy.score`:

```ruby
# Numeric (default)
DSPy.score('accuracy', 0.95)

# With comment
DSPy.score('relevance', 0.87, comment: 'High semantic similarity')

# Boolean
DSPy.score('is_valid', 1, data_type: DSPy::Scores::DataType::Boolean)

# Categorical
DSPy.score('sentiment', 'positive', data_type: DSPy::Scores::DataType::Categorical)

# Explicit trace binding
DSPy.score('accuracy', 0.95, trace_id: 'custom-trace-id')
```

Available data types: `DSPy::Scores::DataType::Numeric`, `::Boolean`, `::Categorical`.

### score.create Events

Every `DSPy.score` call emits a `'score.create'` event. Subscribe to react:

```ruby
DSPy.events.subscribe('score.create') do |event_name, attrs|
  puts "#{attrs[:score_name]} = #{attrs[:score_value]}"
  # Also available: attrs[:score_id], attrs[:score_data_type],
  # attrs[:score_comment], attrs[:trace_id], attrs[:observation_id],
  # attrs[:timestamp]
end
```

### Async Langfuse Export with DSPy::Scores::Exporter

Configure the exporter to send scores to Langfuse in the background:

```ruby
exporter = DSPy::Scores::Exporter.configure(
  public_key: ENV['LANGFUSE_PUBLIC_KEY'],
  secret_key: ENV['LANGFUSE_SECRET_KEY'],
  host: 'https://cloud.langfuse.com'
)

# Scores are now exported automatically via a background Thread::Queue
DSPy.score('accuracy', 0.95)

# Shut down gracefully (waits up to 5 seconds by default)
exporter.shutdown
```

The exporter subscribes to `'score.create'` events internally, queues them for async processing, and retries with exponential backoff on failure.

### Automatic Export with DSPy::Evals

Pass `export_scores: true` to `DSPy::Evals` to export per-example scores and an aggregate batch score automatically:

```ruby
evaluator = DSPy::Evals.new(
  program,
  metric: my_metric,
  export_scores: true,
  score_name: 'qa_accuracy'
)

result = evaluator.evaluate(test_examples)
```

## DSPy::Context.with_span

Create manual spans for custom operations. Requires `dspy-o11y`.

```ruby
DSPy::Context.with_span(operation: 'custom.retrieval', 'retrieval.source' => 'pinecone') do |span|
  results = pinecone_client.query(embedding)
  span&.set_attribute('retrieval.count', results.size) if span
  results
end
```

Pass semantic attributes as keyword arguments alongside `operation:`. The block receives an OpenTelemetry span object (or `nil` when observability is disabled). The span automatically nests under the current parent span and records `duration.ms`, `langfuse.observation.startTime`, and `langfuse.observation.endTime`.

Assign a Langfuse observation type to custom spans:

```ruby
DSPy::Context.with_span(
  operation: 'evaluate.batch',
  **DSPy::ObservationType::Evaluator.langfuse_attributes,
  'batch.size' => examples.length
) do |span|
  run_evaluation(examples)
end
```

Scores reported inside a `with_span` block automatically inherit the current trace context.

## Module Stack Metadata

When `DSPy::Module#forward` runs, the context layer maintains a module stack. Every event includes:

```ruby
{
  module_path: [
    { id: "root_uuid",    class: "DeepSearch",    label: nil },
    { id: "planner_uuid", class: "DSPy::Predict", label: "planner" }
  ],
  module_root: { id: "root_uuid", class: "DeepSearch", label: nil },
  module_leaf: { id: "planner_uuid", class: "DSPy::Predict", label: "planner" },
  module_scope: {
    ancestry_token: "root_uuid>planner_uuid",
    depth: 2
  }
}
```

| Key | Meaning |
|---|---|
| `module_path` | Ordered array of `{id, class, label}` entries from root to leaf |
| `module_root` | The outermost module in the current call chain |
| `module_leaf` | The innermost (currently executing) module |
| `module_scope.ancestry_token` | Stable string of joined UUIDs representing the nesting path |
| `module_scope.depth` | Integer depth of the current module in the stack |

Labels are set via `module_scope_label=` on a module instance or derived automatically from named predictors. Use this metadata to power Langfuse filters, scoped metrics, or custom event routing.

## Dedicated Export Worker

The `DSPy::Observability::AsyncSpanProcessor` (from `dspy-o11y`) keeps telemetry export off the hot path:

- Runs on a `Concurrent::SingleThreadExecutor` -- LLM workflows never compete with OTLP networking.
- Buffers finished spans in a `Thread::Queue` (max size configurable via `DSPY_TELEMETRY_QUEUE_SIZE`).
- Drains spans in batches of `DSPY_TELEMETRY_BATCH_SIZE` (default 100). When the queue reaches batch size, an immediate async export fires.
- A background timer thread triggers periodic export every `DSPY_TELEMETRY_EXPORT_INTERVAL` seconds (default 60).
- Applies exponential backoff (`0.1 * 2^attempt` seconds) on export failures, up to `DEFAULT_MAX_RETRIES` (3).
- On shutdown, flushes all remaining spans within `DSPY_TELEMETRY_SHUTDOWN_TIMEOUT` seconds, then terminates the executor.
- Drops the oldest span when the queue is full, logging `'observability.span_dropped'`.

No application code interacts with the processor directly. Configure it entirely through environment variables.

## Built-in Events Reference

| Event Name | Emitted By | Key Attributes |
|---|---|---|
| `lm.tokens` | `DSPy::LM` | `gen_ai.system`, `gen_ai.request.model`, `input_tokens`, `output_tokens`, `total_tokens` |
| `chain_of_thought.reasoning_complete` | `DSPy::ChainOfThought` | `dspy.signature`, `cot.reasoning_steps`, `cot.reasoning_length`, `cot.has_reasoning` |
| `react.iteration_complete` | `DSPy::ReAct` | `iteration`, `thought`, `action`, `observation` |
| `codeact.iteration_complete` | `dspy-code_act` gem | `iteration`, `code_executed`, `execution_result` |
| `optimization.trial_complete` | Teleprompters (MIPROv2) | `trial_number`, `score` |
| `score.create` | `DSPy.score` | `score_name`, `score_value`, `score_data_type`, `trace_id` |
| `span.start` | `DSPy::Context.with_span` | `trace_id`, `span_id`, `parent_span_id`, `operation` |

## Best Practices

- Use dot-separated string names for events. Follow OpenTelemetry `gen_ai.*` conventions for LLM attributes.
- Always call `unsubscribe` (or `unsubscribe_module_events` for scoped subscriptions) when a tracker is no longer needed to prevent memory leaks.
- Call `DSPy.events.clear_listeners` in test teardown to avoid cross-contamination.
- Wrap risky listener logic in a rescue block. The event system isolates listener failures, but explicit rescue prevents silent swallowing of domain errors.
- Prefer module-scoped `subscribe` for agent internals. Reserve global `DSPy.events.subscribe` for infrastructure-level concerns.

---

## Reference: Optimization

# DSPy.rb Optimization

## MIPROv2

MIPROv2 (Multi-prompt Instruction Proposal with Retrieval Optimization) is the primary instruction tuner in DSPy.rb. It proposes new instructions and few-shot demonstrations per predictor, evaluates them on mini-batches, and retains candidates that improve the metric. It ships as a separate gem to keep the Gaussian Process dependency tree out of apps that do not need it.

### Installation

```ruby
# Gemfile
gem "dspy"
gem "dspy-miprov2"
```

Bundler auto-requires `dspy/miprov2`. No additional `require` statement is needed.

### AutoMode presets

Use `DSPy::Teleprompt::MIPROv2::AutoMode` for preconfigured optimizers:

```ruby
light  = DSPy::Teleprompt::MIPROv2::AutoMode.light(metric: metric)   # 6 trials, greedy
medium = DSPy::Teleprompt::MIPROv2::AutoMode.medium(metric: metric)  # 12 trials, adaptive
heavy  = DSPy::Teleprompt::MIPROv2::AutoMode.heavy(metric: metric)   # 18 trials, Bayesian
```

| Preset   | Trials | Strategy   | Use case                                            |
|----------|--------|------------|-----------------------------------------------------|
| `light`  | 6      | `:greedy`  | Quick wins on small datasets or during prototyping. |
| `medium` | 12     | `:adaptive`| Balanced exploration vs. runtime for most pilots.   |
| `heavy`  | 18     | `:bayesian`| Highest accuracy targets or multi-stage programs.   |

### Manual configuration with dry-configurable

`DSPy::Teleprompt::MIPROv2` includes `Dry::Configurable`. Configure at the class level (defaults for all instances) or instance level (overrides class defaults).

**Class-level defaults:**

```ruby
DSPy::Teleprompt::MIPROv2.configure do |config|
  config.optimization_strategy = :bayesian
  config.num_trials = 30
  config.bootstrap_sets = 10
end
```

**Instance-level overrides:**

```ruby
optimizer = DSPy::Teleprompt::MIPROv2.new(metric: metric)
optimizer.configure do |config|
  config.num_trials = 15
  config.num_instruction_candidates = 6
  config.bootstrap_sets = 5
  config.max_bootstrapped_examples = 4
  config.max_labeled_examples = 16
  config.optimization_strategy = :adaptive       # :greedy, :adaptive, :bayesian
  config.early_stopping_patience = 3
  config.init_temperature = 1.0
  config.final_temperature = 0.1
  config.minibatch_size = nil                     # nil = auto
  config.auto_seed = 42
end
```

The `optimization_strategy` setting accepts symbols (`:greedy`, `:adaptive`, `:bayesian`) and coerces them internally to `DSPy::Teleprompt::OptimizationStrategy` T::Enum values.

The old `config:` constructor parameter is removed. Passing `config:` raises `ArgumentError`.

### Auto presets via configure

Instead of `AutoMode`, set the preset through the configure block:

```ruby
optimizer = DSPy::Teleprompt::MIPROv2.new(metric: metric)
optimizer.configure do |config|
  config.auto_preset = DSPy::Teleprompt::AutoPreset.deserialize("medium")
end
```

### Compile and inspect

```ruby
program = DSPy::Predict.new(MySignature)

result = optimizer.compile(
  program,
  trainset: train_examples,
  valset: val_examples
)

optimized_program = result.optimized_program
puts "Best score: #{result.best_score_value}"
```

The `result` object exposes:
- `optimized_program` -- ready-to-use predictor with updated instruction and demos.
- `optimization_trace[:trial_logs]` -- per-trial record of instructions, demos, and scores.
- `metadata[:optimizer]` -- `"MIPROv2"`, useful when persisting experiments from multiple optimizers.

### Multi-stage programs

MIPROv2 generates dataset summaries for each predictor and proposes per-stage instructions. For a ReAct agent with `thought_generator` and `observation_processor` predictors, the optimizer handles credit assignment internally. The metric only needs to evaluate the final output.

### Bootstrap sampling

During the bootstrap phase MIPROv2:
1. Generates dataset summaries from the training set.
2. Bootstraps few-shot demonstrations by running the baseline program.
3. Proposes candidate instructions grounded in the summaries and bootstrapped examples.
4. Evaluates each candidate on mini-batches drawn from the validation set.

Control the bootstrap phase with `bootstrap_sets`, `max_bootstrapped_examples`, and `max_labeled_examples`.

### Bayesian optimization

When `optimization_strategy` is `:bayesian` (or when using the `heavy` preset), MIPROv2 fits a Gaussian Process surrogate over past trial scores to select the next candidate. This replaces random search with informed exploration, reducing the number of trials needed to find high-scoring instructions.

---

## GEPA

GEPA (Genetic-Pareto Reflective Prompt Evolution) is a feedback-driven optimizer. It runs the program on a small batch, collects scores and textual feedback, and asks a reflection LM to rewrite the instruction. Improved candidates are retained on a Pareto frontier.

### Installation

```ruby
# Gemfile
gem "dspy"
gem "dspy-gepa"
```

The `dspy-gepa` gem depends on the `gepa` core optimizer gem automatically.

### Metric contract

GEPA metrics return `DSPy::Prediction` with both a numeric score and a feedback string. Do not return a plain boolean.

```ruby
metric = lambda do |example, prediction|
  expected  = example.expected_values[:label]
  predicted = prediction.label

  score = predicted == expected ? 1.0 : 0.0
  feedback = if score == 1.0
    "Correct (#{expected}) for: \"#{example.input_values[:text][0..60]}\""
  else
    "Misclassified (expected #{expected}, got #{predicted}) for: \"#{example.input_values[:text][0..60]}\""
  end

  DSPy::Prediction.new(score: score, feedback: feedback)
end
```

Keep the score in `[0, 1]`. Always include a short feedback message explaining what happened -- GEPA hands this text to the reflection model so it can reason about failures.

### Feedback maps

`feedback_map` targets individual predictors inside a composite module. Each entry receives keyword arguments and returns a `DSPy::Prediction`:

```ruby
feedback_map = {
  'self' => lambda do |predictor_output:, predictor_inputs:, module_inputs:, module_outputs:, captured_trace:|
    expected  = module_inputs.expected_values[:label]
    predicted = predictor_output.label

    DSPy::Prediction.new(
      score: predicted == expected ? 1.0 : 0.0,
      feedback: "Classifier saw \"#{predictor_inputs[:text][0..80]}\" -> #{predicted} (expected #{expected})"
    )
  end
}
```

For single-predictor programs, key the map with `'self'`. For multi-predictor chains, add entries per component so the reflection LM sees localized context at each step. Omit `feedback_map` entirely if the top-level metric already covers the basics.

### Configuring the teleprompter

```ruby
teleprompter = DSPy::Teleprompt::GEPA.new(
  metric: metric,
  reflection_lm: DSPy::ReflectionLM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY']),
  feedback_map: feedback_map,
  config: {
    max_metric_calls: 600,
    minibatch_size: 6,
    skip_perfect_score: false
  }
)
```

Key configuration knobs:

| Knob                 | Purpose                                                                                   |
|----------------------|-------------------------------------------------------------------------------------------|
| `max_metric_calls`   | Hard budget on evaluation calls. Set to at least the validation set size plus a few minibatches. |
| `minibatch_size`     | Examples per reflective replay batch. Smaller = cheaper iterations, noisier scores.       |
| `skip_perfect_score` | Set `true` to stop early when a candidate reaches score `1.0`.                            |

### Minibatch sizing

| Goal                                            | Suggested size | Rationale                                                  |
|-------------------------------------------------|----------------|------------------------------------------------------------|
| Explore many candidates within a tight budget   | 3--6           | Cheap iterations, more prompt variants, noisier metrics.   |
| Stable metrics when each rollout is costly      | 8--12          | Smoother scores, fewer candidates unless budget is raised. |
| Investigate specific failure modes              | 3--4 then 8+   | Start with breadth, increase once patterns emerge.         |

### Compile and evaluate

```ruby
program = DSPy::Predict.new(MySignature)

result = teleprompter.compile(program, trainset: train, valset: val)
optimized_program = result.optimized_program

test_metrics = evaluate(optimized_program, test)
```

The `result` object exposes:
- `optimized_program` -- predictor with updated instruction and few-shot examples.
- `best_score_value` -- validation score for the best candidate.
- `metadata` -- candidate counts, trace hashes, and telemetry IDs.

### Reflection LM

Swap `DSPy::ReflectionLM` for any callable object that accepts the reflection prompt hash and returns a string. The default reflection signature extracts the new instruction from triple backticks in the response.

### Experiment tracking

Plug `GEPA::Logging::ExperimentTracker` into a persistence layer:

```ruby
tracker = GEPA::Logging::ExperimentTracker.new
tracker.with_subscriber { |event| MyModel.create!(payload: event) }

teleprompter = DSPy::Teleprompt::GEPA.new(
  metric: metric,
  reflection_lm: reflection_lm,
  experiment_tracker: tracker,
  config: { max_metric_calls: 900 }
)
```

The tracker emits Pareto update events, merge decisions, and candidate evolution records as JSONL.

### Pareto frontier

GEPA maintains a diverse candidate pool and samples from the Pareto frontier instead of mutating only the top-scoring program. This balances exploration and prevents the search from collapsing onto a single lineage.

Enable the merge proposer after multiple strong lineages emerge:

```ruby
config: {
  max_metric_calls: 900,
  enable_merge_proposer: true
}
```

Premature merges eat budget without meaningful gains. Gate merge on having several validated candidates first.

### Advanced options

- `acceptance_strategy:` -- plug in bespoke Pareto filters or early-stop heuristics.
- Telemetry spans emit via `GEPA::Telemetry`. Enable global observability with `DSPy.configure { |c| c.observability = true }` to stream spans to an OpenTelemetry exporter.

---

## Evaluation Framework

`DSPy::Evals` provides batch evaluation of predictors against test datasets with built-in and custom metrics.

### Basic usage

```ruby
metric = proc do |example, prediction|
  prediction.answer == example.expected_values[:answer]
end

evaluator = DSPy::Evals.new(predictor, metric: metric)

result = evaluator.evaluate(
  test_examples,
  display_table: true,
  display_progress: true
)

puts "Pass rate: #{(result.pass_rate * 100).round(1)}%"
puts "Passed: #{result.passed_examples}/#{result.total_examples}"
```

### DSPy::Example

Convert raw data into `DSPy::Example` instances before passing to optimizers or evaluators. Each example carries `input_values` and `expected_values`:

```ruby
examples = rows.map do |row|
  DSPy::Example.new(
    input_values: { text: row[:text] },
    expected_values: { label: row[:label] }
  )
end

train, val, test = split_examples(examples, train_ratio: 0.6, val_ratio: 0.2, seed: 42)
```

Hold back a test set from the optimization loop. Optimizers work on train/val; only the test set proves generalization.

### Built-in metrics

```ruby
# Exact match -- prediction must exactly equal expected value
metric = DSPy::Metrics.exact_match(field: :answer, case_sensitive: true)

# Contains -- prediction must contain expected substring
metric = DSPy::Metrics.contains(field: :answer, case_sensitive: false)

# Numeric difference -- numeric output within tolerance
metric = DSPy::Metrics.numeric_difference(field: :answer, tolerance: 0.01)

# Composite AND -- all sub-metrics must pass
metric = DSPy::Metrics.composite_and(
  DSPy::Metrics.exact_match(field: :answer),
  DSPy::Metrics.contains(field: :reasoning)
)
```

### Custom metrics

```ruby
quality_metric = lambda do |example, prediction|
  return false unless prediction

  score = 0.0
  score += 0.5 if prediction.answer == example.expected_values[:answer]
  score += 0.3 if prediction.explanation && prediction.explanation.length > 50
  score += 0.2 if prediction.confidence && prediction.confidence > 0.8
  score >= 0.7
end

evaluator = DSPy::Evals.new(predictor, metric: quality_metric)
```

Access prediction fields with dot notation (`prediction.answer`), not hash notation.

### Observability hooks

Register callbacks without editing the evaluator:

```ruby
DSPy::Evals.before_example do |payload|
  example = payload[:example]
  DSPy.logger.info("Evaluating example #{example.id}") if example.respond_to?(:id)
end

DSPy::Evals.after_batch do |payload|
  result = payload[:result]
  Langfuse.event(
    name: 'eval.batch',
    metadata: {
      total: result.total_examples,
      passed: result.passed_examples,
      score: result.score
    }
  )
end
```

Available hooks: `before_example`, `after_example`, `before_batch`, `after_batch`.

### Langfuse score export

Enable `export_scores: true` to emit `score.create` events for each evaluated example and a batch score at the end:

```ruby
evaluator = DSPy::Evals.new(
  predictor,
  metric: metric,
  export_scores: true,
  score_name: 'qa_accuracy'   # default: 'evaluation'
)

result = evaluator.evaluate(test_examples)
# Emits per-example scores + overall batch score via DSPy::Scores::Exporter
```

Scores attach to the current trace context automatically and flow to Langfuse asynchronously.

### Evaluation results

```ruby
result = evaluator.evaluate(test_examples)

result.score            # Overall score (0.0 to 1.0)
result.passed_count     # Examples that passed
result.failed_count     # Examples that failed
result.error_count      # Examples that errored

result.results.each do |r|
  r.passed              # Boolean
  r.score               # Numeric score
  r.error               # Error message if the example errored
end
```

### Integration with optimizers

```ruby
metric = proc do |example, prediction|
  expected  = example.expected_values[:answer].to_s.strip.downcase
  predicted = prediction.answer.to_s.strip.downcase
  !expected.empty? && predicted.include?(expected)
end

optimizer = DSPy::Teleprompt::MIPROv2::AutoMode.medium(metric: metric)

result = optimizer.compile(
  DSPy::Predict.new(QASignature),
  trainset: train_examples,
  valset: val_examples
)

evaluator = DSPy::Evals.new(result.optimized_program, metric: metric)
test_result = evaluator.evaluate(test_examples, display_table: true)
puts "Test accuracy: #{(test_result.pass_rate * 100).round(2)}%"
```

---

## Storage System

`DSPy::Storage` persists optimization results, tracks history, and manages multiple versions of optimized programs.

### ProgramStorage (low-level)

```ruby
storage = DSPy::Storage::ProgramStorage.new(storage_path: "./dspy_storage")

# Save
saved = storage.save_program(
  result.optimized_program,
  result,
  metadata: {
    signature_class: 'ClassifyText',
    optimizer: 'MIPROv2',
    examples_count: examples.size
  }
)
puts "Stored with ID: #{saved.program_id}"

# Load
saved = storage.load_program(program_id)
predictor = saved.program
score = saved.optimization_result[:best_score_value]

# List
storage.list_programs.each do |p|
  puts "#{p[:program_id]} -- score: #{p[:best_score]} -- saved: #{p[:saved_at]}"
end
```

### StorageManager (recommended)

```ruby
manager = DSPy::Storage::StorageManager.new

# Save with tags
saved = manager.save_optimization_result(
  result,
  tags: ['production', 'sentiment-analysis'],
  description: 'Optimized sentiment classifier v2'
)

# Find programs
programs = manager.find_programs(
  optimizer: 'MIPROv2',
  min_score: 0.85,
  tags: ['production']
)

recent = manager.find_programs(
  max_age_days: 7,
  signature_class: 'ClassifyText'
)

# Get best program for a signature
best = manager.get_best_program('ClassifyText')
predictor = best.program
```

Global shorthand:

```ruby
DSPy::Storage::StorageManager.save(result, metadata: { version: '2.0' })
DSPy::Storage::StorageManager.load(program_id)
DSPy::Storage::StorageManager.best('ClassifyText')
```

### Checkpoints

Create and restore checkpoints during long-running optimizations:

```ruby
# Save a checkpoint
manager.create_checkpoint(
  current_result,
  'iteration_50',
  metadata: { iteration: 50, current_score: 0.87 }
)

# Restore
restored = manager.restore_checkpoint('iteration_50')
program = restored.program

# Auto-checkpoint every N iterations
if iteration % 10 == 0
  manager.create_checkpoint(current_result, "auto_checkpoint_#{iteration}")
end
```

### Import and export

Share programs between environments:

```ruby
storage = DSPy::Storage::ProgramStorage.new

# Export
storage.export_programs(['abc123', 'def456'], './export_backup.json')

# Import
imported = storage.import_programs('./export_backup.json')
puts "Imported #{imported.size} programs"
```

### Optimization history

```ruby
history = manager.get_optimization_history

history[:summary][:total_programs]
history[:summary][:avg_score]

history[:optimizer_stats].each do |optimizer, stats|
  puts "#{optimizer}: #{stats[:count]} programs, best: #{stats[:best_score]}"
end

history[:trends][:improvement_percentage]
```

### Program comparison

```ruby
comparison = manager.compare_programs(id_a, id_b)
comparison[:comparison][:score_difference]
comparison[:comparison][:better_program]
comparison[:comparison][:age_difference_hours]
```

### Storage configuration

```ruby
config = DSPy::Storage::StorageManager::StorageConfig.new
config.storage_path = Rails.root.join('dspy_storage')
config.auto_save = true
config.save_intermediate_results = false
config.max_stored_programs = 100

manager = DSPy::Storage::StorageManager.new(config: config)
```

### Cleanup

Remove old programs. Cleanup retains the best performing and most recent programs using a weighted score (70% performance, 30% recency):

```ruby
deleted_count = manager.cleanup_old_programs
```

### Storage events

The storage system emits structured log events for monitoring:
- `dspy.storage.save_start`, `dspy.storage.save_complete`, `dspy.storage.save_error`
- `dspy.storage.load_start`, `dspy.storage.load_complete`, `dspy.storage.load_error`
- `dspy.storage.delete`, `dspy.storage.export`, `dspy.storage.import`, `dspy.storage.cleanup`

### File layout

```
dspy_storage/
  programs/
    abc123def456.json
    789xyz012345.json
  history.json
```

---

## API rules

- Call predictors with `.call()`, not `.forward()`.
- Access prediction fields with dot notation (`result.answer`), not hash notation (`result[:answer]`).
- GEPA metrics return `DSPy::Prediction.new(score:, feedback:)`, not a boolean.
- MIPROv2 metrics may return `true`/`false`, a numeric score, or `DSPy::Prediction`.

---

## Reference: Providers

# DSPy.rb LLM Providers

## Adapter Architecture

DSPy.rb ships provider SDKs as separate adapter gems. Install only the adapters the project needs. Each adapter gem depends on the official SDK for its provider and auto-loads when present -- no explicit `require` necessary.

```ruby
# Gemfile
gem 'dspy'              # core framework (no provider SDKs)
gem 'dspy-openai'       # OpenAI, OpenRouter, Ollama
gem 'dspy-anthropic'    # Claude
gem 'dspy-gemini'       # Gemini
gem 'dspy-ruby_llm'     # RubyLLM unified adapter (12+ providers)
```

---

## Per-Provider Adapters

### dspy-openai

Covers any endpoint that speaks the OpenAI chat-completions protocol: OpenAI itself, OpenRouter, and Ollama.

**SDK dependency:** `openai ~> 0.17`

```ruby
# OpenAI
lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])

# OpenRouter -- access 200+ models behind a single key
lm = DSPy::LM.new('openrouter/x-ai/grok-4-fast:free',
  api_key: ENV['OPENROUTER_API_KEY']
)

# Ollama -- local models, no API key required
lm = DSPy::LM.new('ollama/llama3.2')

# Remote Ollama instance
lm = DSPy::LM.new('ollama/llama3.2',
  base_url: 'https://my-ollama.example.com/v1',
  api_key: 'optional-auth-token'
)
```

All three sub-adapters share the same request handling, structured-output support, and error reporting. Swap providers without changing higher-level DSPy code.

For OpenRouter models that lack native structured-output support, disable it explicitly:

```ruby
lm = DSPy::LM.new('openrouter/deepseek/deepseek-chat-v3.1:free',
  api_key: ENV['OPENROUTER_API_KEY'],
  structured_outputs: false
)
```

### dspy-anthropic

Provides the Claude adapter. Install it for any `anthropic/*` model id.

**SDK dependency:** `anthropic ~> 1.12`

```ruby
lm = DSPy::LM.new('anthropic/claude-sonnet-4-20250514',
  api_key: ENV['ANTHROPIC_API_KEY']
)
```

Structured outputs default to tool-based JSON extraction (`structured_outputs: true`). Set `structured_outputs: false` to use enhanced-prompting extraction instead.

```ruby
# Tool-based extraction (default, most reliable)
lm = DSPy::LM.new('anthropic/claude-sonnet-4-20250514',
  api_key: ENV['ANTHROPIC_API_KEY'],
  structured_outputs: true
)

# Enhanced prompting extraction
lm = DSPy::LM.new('anthropic/claude-sonnet-4-20250514',
  api_key: ENV['ANTHROPIC_API_KEY'],
  structured_outputs: false
)
```

### dspy-gemini

Provides the Gemini adapter. Install it for any `gemini/*` model id.

**SDK dependency:** `gemini-ai ~> 4.3`

```ruby
lm = DSPy::LM.new('gemini/gemini-2.5-flash',
  api_key: ENV['GEMINI_API_KEY']
)
```

**Environment variable:** `GEMINI_API_KEY` (also accepts `GOOGLE_API_KEY`).

---

## RubyLLM Unified Adapter

The `dspy-ruby_llm` gem provides a single adapter that routes to 12+ providers through [RubyLLM](https://rubyllm.com). Use it when a project talks to multiple providers or needs access to Bedrock, VertexAI, DeepSeek, or Mistral without dedicated adapter gems.

**SDK dependency:** `ruby_llm ~> 1.3`

### Model ID Format

Prefix every model id with `ruby_llm/`:

```ruby
lm = DSPy::LM.new('ruby_llm/gpt-4o-mini')
lm = DSPy::LM.new('ruby_llm/claude-sonnet-4-20250514')
lm = DSPy::LM.new('ruby_llm/gemini-2.5-flash')
```

The adapter detects the provider from RubyLLM's model registry automatically. For models not in the registry, pass `provider:` explicitly:

```ruby
lm = DSPy::LM.new('ruby_llm/llama3.2', provider: 'ollama')
lm = DSPy::LM.new('ruby_llm/anthropic/claude-3-opus',
  api_key: ENV['OPENROUTER_API_KEY'],
  provider: 'openrouter'
)
```

### Using Existing RubyLLM Configuration

When RubyLLM is already configured globally, omit the `api_key:` argument. DSPy reuses the global config automatically:

```ruby
RubyLLM.configure do |config|
  config.openai_api_key = ENV['OPENAI_API_KEY']
  config.anthropic_api_key = ENV['ANTHROPIC_API_KEY']
end

# No api_key needed -- picks up the global config
DSPy.configure do |c|
  c.lm = DSPy::LM.new('ruby_llm/gpt-4o-mini')
end
```

When an `api_key:` (or any of `base_url:`, `timeout:`, `max_retries:`) is passed, DSPy creates a **scoped context** instead of reusing the global config.

### Cloud-Hosted Providers (Bedrock, VertexAI)

Configure RubyLLM globally first, then reference the model:

```ruby
# AWS Bedrock
RubyLLM.configure do |c|
  c.bedrock_api_key = ENV['AWS_ACCESS_KEY_ID']
  c.bedrock_secret_key = ENV['AWS_SECRET_ACCESS_KEY']
  c.bedrock_region = 'us-east-1'
end
lm = DSPy::LM.new('ruby_llm/anthropic.claude-3-5-sonnet', provider: 'bedrock')

# Google VertexAI
RubyLLM.configure do |c|
  c.vertexai_project_id = 'your-project-id'
  c.vertexai_location = 'us-central1'
end
lm = DSPy::LM.new('ruby_llm/gemini-pro', provider: 'vertexai')
```

### Supported Providers Table

| Provider    | Example Model ID                           | Notes                           |
|-------------|--------------------------------------------|---------------------------------|
| OpenAI      | `ruby_llm/gpt-4o-mini`                    | Auto-detected from registry     |
| Anthropic   | `ruby_llm/claude-sonnet-4-20250514`       | Auto-detected from registry     |
| Gemini      | `ruby_llm/gemini-2.5-flash`               | Auto-detected from registry     |
| DeepSeek    | `ruby_llm/deepseek-chat`                  | Auto-detected from registry     |
| Mistral     | `ruby_llm/mistral-large`                  | Auto-detected from registry     |
| Ollama      | `ruby_llm/llama3.2`                       | Use `provider: 'ollama'`        |
| AWS Bedrock | `ruby_llm/anthropic.claude-3-5-sonnet`    | Configure RubyLLM globally      |
| VertexAI    | `ruby_llm/gemini-pro`                     | Configure RubyLLM globally      |
| OpenRouter  | `ruby_llm/anthropic/claude-3-opus`        | Use `provider: 'openrouter'`    |
| Perplexity  | `ruby_llm/llama-3.1-sonar-large`          | Use `provider: 'perplexity'`    |
| GPUStack    | `ruby_llm/model-name`                     | Use `provider: 'gpustack'`      |

---

## Rails Initializer Pattern

Configure DSPy inside an `after_initialize` block so Rails credentials and environment are fully loaded:

```ruby
# config/initializers/dspy.rb
Rails.application.config.after_initialize do
  return if Rails.env.test? # skip in test -- use VCR cassettes instead

  DSPy.configure do |config|
    config.lm = DSPy::LM.new(
      'openai/gpt-4o-mini',
      api_key: Rails.application.credentials.openai_api_key,
      structured_outputs: true
    )

    config.logger = if Rails.env.production?
      Dry.Logger(:dspy, formatter: :json) do |logger|
        logger.add_backend(stream: Rails.root.join("log/dspy.log"))
      end
    else
      Dry.Logger(:dspy) do |logger|
        logger.add_backend(level: :debug, stream: $stdout)
      end
    end
  end
end
```

Key points:

- Wrap in `after_initialize` so `Rails.application.credentials` is available.
- Return early in the test environment. Rely on VCR cassettes for deterministic LLM responses.
- Set `structured_outputs: true` (the default) for provider-native JSON extraction.
- Use `Dry.Logger` with `:json` formatter in production for structured log parsing.

---

## Fiber-Local LM Context

`DSPy.with_lm` sets a temporary language-model override scoped to the current Fiber. Every predictor call inside the block uses the override; outside the block the previous LM takes effect again.

```ruby
fast = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])
powerful = DSPy::LM.new('anthropic/claude-sonnet-4-20250514', api_key: ENV['ANTHROPIC_API_KEY'])

classifier = Classifier.new

# Uses the global LM
result = classifier.call(text: "Hello")

# Temporarily switch to the fast model
DSPy.with_lm(fast) do
  result = classifier.call(text: "Hello")   # uses gpt-4o-mini
end

# Temporarily switch to the powerful model
DSPy.with_lm(powerful) do
  result = classifier.call(text: "Hello")   # uses claude-sonnet-4
end
```

### LM Resolution Hierarchy

DSPy resolves the active language model in this order:

1. **Instance-level LM** -- set directly on a module instance via `configure`
2. **Fiber-local LM** -- set via `DSPy.with_lm`
3. **Global LM** -- set via `DSPy.configure`

Instance-level configuration always wins, even inside a `DSPy.with_lm` block:

```ruby
classifier = Classifier.new
classifier.configure { |c| c.lm = DSPy::LM.new('anthropic/claude-sonnet-4-20250514', api_key: ENV['ANTHROPIC_API_KEY']) }

fast = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY'])

DSPy.with_lm(fast) do
  classifier.call(text: "Test")  # still uses claude-sonnet-4 (instance-level wins)
end
```

### configure_predictor for Fine-Grained Agent Control

Complex agents (`ReAct`, `CodeAct`, `DeepResearch`, `DeepSearch`) contain internal predictors. Use `configure` for a blanket override and `configure_predictor` to target a specific sub-predictor:

```ruby
agent = DSPy::ReAct.new(MySignature, tools: tools)

# Set a default LM for the agent and all its children
agent.configure { |c| c.lm = DSPy::LM.new('openai/gpt-4o-mini', api_key: ENV['OPENAI_API_KEY']) }

# Override just the reasoning predictor with a more capable model
agent.configure_predictor('thought_generator') do |c|
  c.lm = DSPy::LM.new('anthropic/claude-sonnet-4-20250514', api_key: ENV['ANTHROPIC_API_KEY'])
end

result = agent.call(question: "Summarize the report")
```

Both methods support chaining:

```ruby
agent
  .configure { |c| c.lm = cheap_model }
  .configure_predictor('thought_generator') { |c| c.lm = expensive_model }
```

#### Available Predictors by Agent Type

| Agent                | Internal Predictors                                              |
|----------------------|------------------------------------------------------------------|
| `DSPy::ReAct`        | `thought_generator`, `observation_processor`                    |
| `DSPy::CodeAct`      | `code_generator`, `observation_processor`                       |
| `DSPy::DeepResearch`  | `planner`, `synthesizer`, `qa_reviewer`, `reporter`            |
| `DSPy::DeepSearch`    | `seed_predictor`, `search_predictor`, `reader_predictor`, `reason_predictor` |

#### Propagation Rules

- Configuration propagates recursively to children and grandchildren.
- Children with an already-configured LM are **not** overwritten by a later parent `configure` call.
- Configure the parent first, then override specific children.

---

## Feature-Flagged Model Selection

Use a `FeatureFlags` module backed by ENV vars to centralize model selection. Each tool or agent reads its model from the flags, falling back to a global default.

```ruby
module FeatureFlags
  module_function

  def default_model
    ENV.fetch('DSPY_DEFAULT_MODEL', 'openai/gpt-4o-mini')
  end

  def default_api_key
    ENV.fetch('DSPY_DEFAULT_API_KEY') { ENV.fetch('OPENAI_API_KEY', nil) }
  end

  def model_for(tool_name)
    env_key = "DSPY_MODEL_#{tool_name.upcase}"
    ENV.fetch(env_key, default_model)
  end

  def api_key_for(tool_name)
    env_key = "DSPY_API_KEY_#{tool_name.upcase}"
    ENV.fetch(env_key, default_api_key)
  end
end
```

### Per-Tool Model Override

Override an individual tool's model without touching application code:

```bash
# .env
DSPY_DEFAULT_MODEL=openai/gpt-4o-mini
DSPY_DEFAULT_API_KEY=sk-...

# Override the classifier to use Claude
DSPY_MODEL_CLASSIFIER=anthropic/claude-sonnet-4-20250514
DSPY_API_KEY_CLASSIFIER=sk-ant-...

# Override the summarizer to use Gemini
DSPY_MODEL_SUMMARIZER=gemini/gemini-2.5-flash
DSPY_API_KEY_SUMMARIZER=...
```

Wire each agent to its flag at initialization:

```ruby
class ClassifierAgent < DSPy::Module
  def initialize
    super
    model = FeatureFlags.model_for('classifier')
    api_key = FeatureFlags.api_key_for('classifier')

    @predictor = DSPy::Predict.new(ClassifySignature)
    configure { |c| c.lm = DSPy::LM.new(model, api_key: api_key) }
  end

  def forward(text:)
    @predictor.call(text: text)
  end
end
```

This pattern keeps model routing declarative and avoids scattering `DSPy::LM.new` calls across the codebase.

---

## Compatibility Matrix

Feature support across direct adapter gems. All features listed assume `structured_outputs: true` (the default).

| Feature              | OpenAI | Anthropic | Gemini | Ollama   | OpenRouter | RubyLLM     |
|----------------------|--------|-----------|--------|----------|------------|-------------|
| Structured Output    | Native JSON mode | Tool-based extraction | Native JSON schema | OpenAI-compatible JSON | Varies by model | Via `with_schema` |
| Vision (Images)      | File + URL | File + Base64 | File + Base64 | Limited  | Varies     | Delegates to underlying provider |
| Image URLs           | Yes    | No        | No     | No       | Varies     | Depends on provider |
| Tool Calling         | Yes    | Yes       | Yes    | Varies   | Varies     | Yes         |
| Streaming            | Yes    | Yes       | Yes    | Yes      | Yes        | Yes         |

**Notes:**

- **Structured Output** is enabled by default on every adapter. Set `structured_outputs: false` to fall back to enhanced-prompting extraction.
- **Vision / Image URLs:** Only OpenAI supports passing a URL directly. For Anthropic and Gemini, load images from file or Base64:
  ```ruby
  DSPy::Image.from_url("https://example.com/img.jpg")    # OpenAI only
  DSPy::Image.from_file("path/to/image.jpg")             # all providers
  DSPy::Image.from_base64(data, mime_type: "image/jpeg")  # all providers
  ```
- **RubyLLM** delegates to the underlying provider, so feature support matches the provider column in the table.

### Choosing an Adapter Strategy

| Scenario                                  | Recommended Adapter            |
|-------------------------------------------|--------------------------------|
| Single provider (OpenAI, Claude, or Gemini) | Dedicated gem (`dspy-openai`, `dspy-anthropic`, `dspy-gemini`) |
| Multi-provider with per-agent model routing | `dspy-ruby_llm`               |
| AWS Bedrock or Google VertexAI             | `dspy-ruby_llm`               |
| Local development with Ollama              | `dspy-openai` (Ollama sub-adapter) or `dspy-ruby_llm` |
| OpenRouter for cost optimization           | `dspy-openai` (OpenRouter sub-adapter) |

### Current Recommended Models

| Provider  | Model ID                              | Use Case              |
|-----------|---------------------------------------|-----------------------|
| OpenAI    | `openai/gpt-4o-mini`                 | Fast, cost-effective  |
| Anthropic | `anthropic/claude-sonnet-4-20250514` | Balanced reasoning    |
| Gemini    | `gemini/gemini-2.5-flash`            | Fast, cost-effective  |
| Ollama    | `ollama/llama3.2`                    | Local, zero API cost  |

---

## Reference: Toolsets

# DSPy.rb Toolsets

## Tools::Base

`DSPy::Tools::Base` is the base class for single-purpose tools. Each subclass exposes one operation to an LLM agent through a `call` method.

### Defining a Tool

Set the tool's identity with the `tool_name` and `tool_description` class-level DSL methods. Define the `call` instance method with a Sorbet `sig` declaration so DSPy.rb can generate the JSON schema the LLM uses to invoke the tool.

```ruby
class WeatherLookup < DSPy::Tools::Base
  extend T::Sig

  tool_name "weather_lookup"
  tool_description "Look up current weather for a given city"

  sig { params(city: String, units: T.nilable(String)).returns(String) }
  def call(city:, units: nil)
    # Fetch weather data and return a string summary
    "72F and sunny in #{city}"
  end
end
```

Key points:

- Inherit from `DSPy::Tools::Base`, not `DSPy::Tool`.
- Use `tool_name` (class method) to set the name the LLM sees. Without it, the class name is lowercased as a fallback.
- Use `tool_description` (class method) to set the human-readable description surfaced in the tool schema.
- The `call` method must use **keyword arguments**. Positional arguments are supported but keyword arguments produce better schemas.
- Always attach a Sorbet `sig` to `call`. Without a signature, the generated schema has empty properties and the LLM cannot determine parameter types.

### Schema Generation

`call_schema_object` introspects the Sorbet signature on `call` and returns a hash representing the JSON Schema `parameters` object:

```ruby
WeatherLookup.call_schema_object
# => {
#   type: "object",
#   properties: {
#     city:  { type: "string", description: "Parameter city" },
#     units: { type: "string", description: "Parameter units (optional)" }
#   },
#   required: ["city"]
# }
```

`call_schema` wraps this in the full LLM tool-calling format:

```ruby
WeatherLookup.call_schema
# => {
#   type: "function",
#   function: {
#     name: "call",
#     description: "Call the WeatherLookup tool",
#     parameters: { ... }
#   }
# }
```

### Using Tools with ReAct

Pass tool instances in an array to `DSPy::ReAct`:

```ruby
agent = DSPy::ReAct.new(
  MySignature,
  tools: [WeatherLookup.new, AnotherTool.new]
)

result = agent.call(question: "What is the weather in Berlin?")
puts result.answer
```

Access output fields with dot notation (`result.answer`), not hash access (`result[:answer]`).

---

## Tools::Toolset

`DSPy::Tools::Toolset` groups multiple related methods into a single class. Each exposed method becomes an independent tool from the LLM's perspective.

### Defining a Toolset

```ruby
class DatabaseToolset < DSPy::Tools::Toolset
  extend T::Sig

  toolset_name "db"

  tool :query,  description: "Run a read-only SQL query"
  tool :insert, description: "Insert a record into a table"
  tool :delete, description: "Delete a record by ID"

  sig { params(sql: String).returns(String) }
  def query(sql:)
    # Execute read query
  end

  sig { params(table: String, data: T::Hash[String, String]).returns(String) }
  def insert(table:, data:)
    # Insert record
  end

  sig { params(table: String, id: Integer).returns(String) }
  def delete(table:, id:)
    # Delete record
  end
end
```

### DSL Methods

**`toolset_name(name)`** -- Set the prefix for all generated tool names. If omitted, the class name minus `Toolset` suffix is lowercased (e.g., `DatabaseToolset` becomes `database`).

```ruby
toolset_name "db"
# tool :query produces a tool named "db_query"
```

**`tool(method_name, tool_name:, description:)`** -- Expose a method as a tool.

- `method_name` (Symbol, required) -- the instance method to expose.
- `tool_name:` (String, optional) -- override the default `<toolset_name>_<method_name>` naming.
- `description:` (String, optional) -- description shown to the LLM. Defaults to a humanized version of the method name.

```ruby
tool :word_count, tool_name: "text_wc", description: "Count lines, words, and characters"
# Produces a tool named "text_wc" instead of "text_word_count"
```

### Converting to a Tool Array

Call `to_tools` on the class (not an instance) to get an array of `ToolProxy` objects compatible with `DSPy::Tools::Base`:

```ruby
agent = DSPy::ReAct.new(
  AnalyzeText,
  tools: DatabaseToolset.to_tools
)
```

Each `ToolProxy` wraps one method, delegates `call` to the underlying toolset instance, and generates its own JSON schema from the method's Sorbet signature.

### Shared State

All tool proxies from a single `to_tools` call share one toolset instance. Store shared state (connections, caches, configuration) in the toolset's `initialize`:

```ruby
class ApiToolset < DSPy::Tools::Toolset
  extend T::Sig

  toolset_name "api"

  tool :get,  description: "Make a GET request"
  tool :post, description: "Make a POST request"

  sig { params(base_url: String).void }
  def initialize(base_url:)
    @base_url = base_url
    @client = HTTP.persistent(base_url)
  end

  sig { params(path: String).returns(String) }
  def get(path:)
    @client.get("#{@base_url}#{path}").body.to_s
  end

  sig { params(path: String, body: String).returns(String) }
  def post(path:, body:)
    @client.post("#{@base_url}#{path}", body: body).body.to_s
  end
end
```

---

## Type Safety

Sorbet signatures on tool methods drive both JSON schema generation and automatic type coercion of LLM responses.

### Basic Types

```ruby
sig { params(
  text: String,
  count: Integer,
  score: Float,
  enabled: T::Boolean,
  threshold: Numeric
).returns(String) }
def analyze(text:, count:, score:, enabled:, threshold:)
  # ...
end
```

| Sorbet Type      | JSON Schema                                        |
|------------------|----------------------------------------------------|
| `String`         | `{"type": "string"}`                               |
| `Integer`        | `{"type": "integer"}`                              |
| `Float`          | `{"type": "number"}`                               |
| `Numeric`        | `{"type": "number"}`                               |
| `T::Boolean`     | `{"type": "boolean"}`                              |
| `T::Enum`        | `{"type": "string", "enum": [...]}`                |
| `T::Struct`      | `{"type": "object", "properties": {...}}`          |
| `T::Array[Type]` | `{"type": "array", "items": {...}}`                |
| `T::Hash[K, V]`  | `{"type": "object", "additionalProperties": {...}}`|
| `T.nilable(Type)`| `{"type": [original, "null"]}`                     |
| `T.any(T1, T2)`  | `{"oneOf": [{...}, {...}]}`                        |
| `T.class_of(X)`  | `{"type": "string"}`                               |

### T::Enum Parameters

Define a `T::Enum` and reference it in a tool signature. DSPy.rb generates a JSON Schema `enum` constraint and automatically deserializes the LLM's string response into the correct enum instance.

```ruby
class Priority < T::Enum
  enums do
    Low = new('low')
    Medium = new('medium')
    High = new('high')
    Critical = new('critical')
  end
end

class Status < T::Enum
  enums do
    Pending = new('pending')
    InProgress = new('in-progress')
    Completed = new('completed')
  end
end

sig { params(priority: Priority, status: Status).returns(String) }
def update_task(priority:, status:)
  "Updated to #{priority.serialize} / #{status.serialize}"
end
```

The generated schema constrains the parameter to valid values:

```json
{
  "priority": {
    "type": "string",
    "enum": ["low", "medium", "high", "critical"]
  }
}
```

**Case-insensitive matching**: When the LLM returns `"HIGH"` or `"High"` instead of `"high"`, DSPy.rb first tries an exact `try_deserialize`, then falls back to a case-insensitive lookup. This prevents failures caused by LLM casing variations.

### T::Struct Parameters

Use `T::Struct` for complex nested objects. DSPy.rb generates nested JSON Schema properties and recursively coerces the LLM's hash response into struct instances.

```ruby
class TaskMetadata < T::Struct
  prop :id, String
  prop :priority, Priority
  prop :tags, T::Array[String]
  prop :estimated_hours, T.nilable(Float), default: nil
end

class TaskRequest < T::Struct
  prop :title, String
  prop :description, String
  prop :status, Status
  prop :metadata, TaskMetadata
  prop :assignees, T::Array[String]
end

sig { params(task: TaskRequest).returns(String) }
def create_task(task:)
  "Created: #{task.title} (#{task.status.serialize})"
end
```

The LLM sees the full nested object schema and DSPy.rb reconstructs the struct tree from the JSON response, including enum fields inside nested structs.

### Nilable Parameters

Mark optional parameters with `T.nilable(...)` and provide a default value of `nil` in the method signature. These parameters are excluded from the JSON Schema `required` array.

```ruby
sig { params(
  query: String,
  max_results: T.nilable(Integer),
  filter: T.nilable(String)
).returns(String) }
def search(query:, max_results: nil, filter: nil)
  # query is required; max_results and filter are optional
end
```

### Collections

Typed arrays and hashes generate precise item/value schemas:

```ruby
sig { params(
  tags: T::Array[String],
  priorities: T::Array[Priority],
  config: T::Hash[String, T.any(String, Integer, Float)]
).returns(String) }
def configure(tags:, priorities:, config:)
  # Array elements and hash values are validated and coerced
end
```

### Union Types

`T.any(...)` generates a `oneOf` JSON Schema. When one of the union members is a `T::Struct`, DSPy.rb uses the `_type` discriminator field to select the correct struct class during coercion.

```ruby
sig { params(value: T.any(String, Integer, Float)).returns(String) }
def handle_flexible(value:)
  # Accepts multiple types
end
```

---

## Built-in Toolsets

### TextProcessingToolset

`DSPy::Tools::TextProcessingToolset` provides Unix-style text analysis and manipulation operations. Toolset name prefix: `text`.

| Tool Name                         | Method            | Description                                |
|-----------------------------------|-------------------|--------------------------------------------|
| `text_grep`                       | `grep`            | Search for patterns with optional case-insensitive and count-only modes |
| `text_wc`                         | `word_count`      | Count lines, words, and characters         |
| `text_rg`                         | `ripgrep`         | Fast pattern search with context lines     |
| `text_extract_lines`              | `extract_lines`   | Extract a range of lines by number         |
| `text_filter_lines`               | `filter_lines`    | Keep or reject lines matching a regex      |
| `text_unique_lines`               | `unique_lines`    | Deduplicate lines, optionally preserving order |
| `text_sort_lines`                 | `sort_lines`      | Sort lines alphabetically or numerically   |
| `text_summarize_text`             | `summarize_text`  | Produce a statistical summary (counts, averages, frequent words) |

Usage:

```ruby
agent = DSPy::ReAct.new(
  AnalyzeText,
  tools: DSPy::Tools::TextProcessingToolset.to_tools
)

result = agent.call(text: log_contents, question: "How many error lines are there?")
puts result.answer
```

### GitHubCLIToolset

`DSPy::Tools::GitHubCLIToolset` wraps the `gh` CLI for read-oriented GitHub operations. Toolset name prefix: `github`.

| Tool Name              | Method            | Description                                       |
|------------------------|-------------------|---------------------------------------------------|
| `github_list_issues`   | `list_issues`     | List issues filtered by state, labels, assignee   |
| `github_list_prs`      | `list_prs`        | List pull requests filtered by state, author, base|
| `github_get_issue`     | `get_issue`       | Retrieve details of a single issue                |
| `github_get_pr`        | `get_pr`          | Retrieve details of a single pull request         |
| `github_api_request`   | `api_request`     | Make an arbitrary GET request to the GitHub API    |
| `github_traffic_views` | `traffic_views`   | Fetch repository traffic view counts              |
| `github_traffic_clones`| `traffic_clones`  | Fetch repository traffic clone counts             |

This toolset uses `T::Enum` parameters (`IssueState`, `PRState`, `ReviewState`) for state filters, demonstrating enum-based tool signatures in practice.

```ruby
agent = DSPy::ReAct.new(
  RepoAnalysis,
  tools: DSPy::Tools::GitHubCLIToolset.to_tools
)
```

---

## Testing

### Unit Testing Individual Tools

Test `DSPy::Tools::Base` subclasses by instantiating and calling `call` directly:

```ruby
RSpec.describe WeatherLookup do
  subject(:tool) { described_class.new }

  it "returns weather for a city" do
    result = tool.call(city: "Berlin")
    expect(result).to include("Berlin")
  end

  it "exposes the correct tool name" do
    expect(tool.name).to eq("weather_lookup")
  end

  it "generates a valid schema" do
    schema = described_class.call_schema_object
    expect(schema[:required]).to include("city")
    expect(schema[:properties]).to have_key(:city)
  end
end
```

### Unit Testing Toolsets

Test toolset methods directly on an instance. Verify tool generation with `to_tools`:

```ruby
RSpec.describe DatabaseToolset do
  subject(:toolset) { described_class.new }

  it "executes a query" do
    result = toolset.query(sql: "SELECT 1")
    expect(result).to be_a(String)
  end

  it "generates tools with correct names" do
    tools = described_class.to_tools
    names = tools.map(&:name)
    expect(names).to contain_exactly("db_query", "db_insert", "db_delete")
  end

  it "generates tool descriptions" do
    tools = described_class.to_tools
    query_tool = tools.find { |t| t.name == "db_query" }
    expect(query_tool.description).to eq("Run a read-only SQL query")
  end
end
```

### Mocking Predictions Inside Tools

When a tool calls a DSPy predictor internally, stub the predictor to isolate tool logic from LLM calls:

```ruby
class SmartSearchTool < DSPy::Tools::Base
  extend T::Sig

  tool_name "smart_search"
  tool_description "Search with query expansion"

  sig { void }
  def initialize
    @expander = DSPy::Predict.new(QueryExpansionSignature)
  end

  sig { params(query: String).returns(String) }
  def call(query:)
    expanded = @expander.call(query: query)
    perform_search(expanded.expanded_query)
  end

  private

  def perform_search(query)
    # actual search logic
  end
end

RSpec.describe SmartSearchTool do
  subject(:tool) { described_class.new }

  before do
    expansion_result = double("result", expanded_query: "expanded test query")
    allow_any_instance_of(DSPy::Predict).to receive(:call).and_return(expansion_result)
  end

  it "expands the query before searching" do
    allow(tool).to receive(:perform_search).with("expanded test query").and_return("found 3 results")
    result = tool.call(query: "test")
    expect(result).to eq("found 3 results")
  end
end
```

### Testing Enum Coercion

Verify that string values from LLM responses deserialize into the correct enum instances:

```ruby
RSpec.describe "enum coercion" do
  it "handles case-insensitive enum values" do
    toolset = GitHubCLIToolset.new
    # The LLM may return "OPEN" instead of "open"
    result = toolset.list_issues(state: IssueState::Open)
    expect(result).to be_a(String)
  end
end
```

---

## Constraints

- All exposed tool methods must use **keyword arguments**. Positional-only parameters generate schemas but keyword arguments produce more reliable LLM interactions.
- Each exposed method becomes a **separate, independent tool**. Method chaining or multi-step sequences within a single tool call are not supported.
- Shared state across tool proxies is scoped to a single `to_tools` call. Separate `to_tools` invocations create separate toolset instances.
- Methods without a Sorbet `sig` produce an empty parameter schema. The LLM will not know what arguments to pass.
