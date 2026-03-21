---
title: "Parallel Web"
description: "Search the web, extract URL content, and run deep research using the Parallel Chat API and Extract API. Use for ALL web searches, research queries, and general information gathering. Provides synthesized summaries with citations."
category: "research"
source: "community"
author: "Community"
tags: ["parallel", "web"]
date: 2026-03-20
---

# Parallel Web Systems API

## Overview

This skill provides access to **Parallel Web Systems** APIs for web search, deep research, and content extraction. It is the **primary tool for all web-related operations** in the scientific writer workflow.

**Primary interface:** Parallel Chat API (OpenAI-compatible) for search and research.
**Secondary interface:** Extract API for URL verification and special cases only.

**API Documentation:** https://docs.parallel.ai
**API Key:** https://platform.parallel.ai
**Environment Variable:** `PARALLEL_API_KEY`

## When to Use This Skill

Use this skill for **ALL** of the following:

- **Web Search**: Any query that requires searching the internet for information
- **Deep Research**: Comprehensive research reports on any topic
- **Market Research**: Industry analysis, competitive intelligence, market data
- **Current Events**: News, recent developments, announcements
- **Technical Information**: Documentation, specifications, product details
- **Statistical Data**: Market sizes, growth rates, industry figures
- **General Information**: Company profiles, facts, comparisons

**Use Extract API only for:**
- Citation verification (confirming a specific URL's content)
- Special cases where you need raw content from a known URL

**Do NOT use this skill for:**
- Academic-specific paper searches (use `research-lookup` which routes to Perplexity for purely academic queries)
- Google Scholar / PubMed database searches (use `citation-management` skill)

---

## Two Capabilities

### 1. Web Search (`search` command)

Search the web via the Parallel Chat API (`base` model) and get a **synthesized summary** with cited sources.

**Best for:** General web searches, current events, fact-finding, technical lookups, news, market data.

```bash
# Basic search
python scripts/parallel_web.py search "latest advances in quantum computing 2025"

# Use core model for more complex queries
python scripts/parallel_web.py search "compare EV battery chemistries NMC vs LFP" --model core

# Save results to file
python scripts/parallel_web.py search "renewable energy policy updates" -o results.txt

# JSON output for programmatic use
python scripts/parallel_web.py search "AI regulation landscape" --json -o results.json
```

**Key Parameters:**
- `objective`: Natural language description of what you want to find
- `--model`: Chat model to use (`base` default, or `core` for deeper research)
- `-o`: Output file path
- `--json`: Output as JSON

**Response includes:** Synthesized summary organized by themes, with inline citations and a sources list.

### 2. Deep Research (`research` command)

Run comprehensive multi-source research via the Parallel Chat API (`core` model) that produces detailed intelligence reports with citations.

**Best for:** Market research, comprehensive analysis, competitive intelligence, technology surveys, industry reports, any research question requiring synthesis of multiple sources.

```bash
# Default deep research (core model)
python scripts/parallel_web.py research "comprehensive analysis of the global EV battery market"

# Save research report to file
python scripts/parallel_web.py research "AI adoption in healthcare 2025" -o report.md

# Use base model for faster, lighter research
python scripts/parallel_web.py research "latest funding rounds in AI startups" --model base

# JSON output
python scripts/parallel_web.py research "renewable energy storage market in Europe" --json -o data.json
```

**Key Parameters:**
- `query`: Research question or topic
- `--model`: Chat model to use (`core` default for deep research, or `base` for faster results)
- `-o`: Output file path
- `--json`: Output as JSON

### 3. URL Extraction (`extract` command) — Verification Only

Extract content from specific URLs. **Use only for citation verification and special cases.**

For general research, use `search` or `research` instead.

```bash
# Verify a citation's content
python scripts/parallel_web.py extract "https://example.com/article" --objective "key findings"

# Get full page content for verification
python scripts/parallel_web.py extract "https://docs.example.com/api" --full-content

# Save extraction to file
python scripts/parallel_web.py extract "https://paper-url.com" --objective "methodology" -o extracted.md
```

---

## Model Selection Guide

The Chat API supports two research models. Use `base` for most searches and `core` for deep research.

| Model  | Latency    | Strengths                        | Use When                    |
|--------|------------|----------------------------------|-----------------------------|
| `base` | 15s-100s   | Standard research, factual queries | Web searches, quick lookups |
| `core` | 60s-5min   | Complex research, multi-source synthesis | Deep research, comprehensive reports |

**Recommendations:**
- `search` command defaults to `base` — fast, good for most queries
- `research` command defaults to `core` — thorough, good for comprehensive reports
- Override with `--model` when you need different depth/speed tradeoffs

---

## Python API Usage

### Search

```python
from parallel_web import ParallelSearch

searcher = ParallelSearch()
result = searcher.search(
    objective="Find latest information about transformer architectures in NLP",
    model="base",
)

if result["success"]:
    print(result["response"])  # Synthesized summary
    for src in result["sources"]:
        print(f"  {src['title']}: {src['url']}")
```

### Deep Research

```python
from parallel_web import ParallelDeepResearch

researcher = ParallelDeepResearch()
result = researcher.research(
    query="Comprehensive analysis of AI regulation in the EU and US",
    model="core",
)

if result["success"]:
    print(result["response"])  # Full research report
    print(f"Citations: {result['citation_count']}")
```

### Extract (Verification Only)

```python
from parallel_web import ParallelExtract

extractor = ParallelExtract()
result = extractor.extract(
    urls=["https://docs.example.com/api-reference"],
    objective="API authentication methods and rate limits",
)

if result["success"]:
    for r in result["results"]:
        print(r["excerpts"])
```

---

## MANDATORY: Save All Results to Sources Folder

**Every web search and deep research result MUST be saved to the project's `sources/` folder.**

This ensures all research is preserved for reproducibility, auditability, and context window recovery.

### Saving Rules

| Operation | `-o` Flag Target | Filename Pattern |
|-----------|-----------------|------------------|
| Web Search | `sources/search_<topic>.md` | `search_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| Deep Research | `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
| URL Extract | `sources/extract_<source>.md` | `extract_YYYYMMDD_HHMMSS_<brief_source>.md` |

### How to Save (Always Use `-o` Flag)

**CRITICAL: Every call to `parallel_web.py` MUST include the `-o` flag pointing to the `sources/` folder.**

```bash
# Web search — ALWAYS save to sources/
python scripts/parallel_web.py search "latest advances in quantum computing 2025" \
  -o sources/search_20250217_143000_quantum_computing.md

# Deep research — ALWAYS save to sources/
python scripts/parallel_web.py research "comprehensive analysis of the global EV battery market" \
  -o sources/research_20250217_144000_ev_battery_market.md

# URL extraction (verification only) — save to sources/
python scripts/parallel_web.py extract "https://example.com/article" --objective "key findings" \
  -o sources/extract_20250217_143500_example_article.md
```

### Why Save Everything

1. **Reproducibility**: Every claim in the final document can be traced back to its raw source material
2. **Context Window Recovery**: If context is compacted mid-task, saved results can be re-read from `sources/`
3. **Audit Trail**: The `sources/` folder provides complete transparency into how information was gathered
4. **Reuse Across Sections**: Saved research can be referenced by multiple sections without duplicate API calls
5. **Cost Efficiency**: Avoid redundant API calls by checking `sources/` for existing results
6. **Peer Review Support**: Reviewers can verify the research backing every claim

### Logging

When saving research results, always log:

```
[HH:MM:SS] SAVED: Search results to sources/search_20250217_143000_quantum_computing.md
[HH:MM:SS] SAVED: Deep research report to sources/research_20250217_144000_ev_battery_market.md
```

### Before Making a New Query, Check Sources First

Before calling `parallel_web.py`, check if a relevant result already exists in `sources/`:

```bash
ls sources/  # Check existing saved results
```

---

## Integration with Scientific Writer

### Routing Table

| Task | Tool | Command |
|------|------|---------|
| Web search (any) | `parallel_web.py search` | `python scripts/parallel_web.py search "query" -o sources/search_<topic>.md` |
| Deep research | `parallel_web.py research` | `python scripts/parallel_web.py research "query" -o sources/research_<topic>.md` |
| Citation verification | `parallel_web.py extract` | `python scripts/parallel_web.py extract "url" -o sources/extract_<source>.md` |
| Academic paper search | `research_lookup.py` | Routes to Perplexity sonar-pro-search |
| DOI/metadata lookup | `parallel_web.py extract` | Extract from DOI URLs (verification) |

### When Writing Scientific Documents

1. **Before writing any section**, use `search` or `research` to gather background information — **save results to `sources/`**
2. **For academic citations**, use `research-lookup` (which routes academic queries to Perplexity) — **save results to `sources/`**
3. **For citation verification** (confirming a specific URL), use `parallel_web.py extract` — **save results to `sources/`**
4. **For current market/industry data**, use `parallel_web.py research --model core` — **save results to `sources/`**
5. **Before any new query**, check `sources/` for existing results to avoid duplicate API calls

---

## Environment Setup

```bash
# Required: Set your Parallel API key
export PARALLEL_API_KEY="your_api_key_here"

# Required Python packages
pip install openai        # For Chat API (search/research)
pip install parallel-web  # For Extract API (verification only)
```

Get your API key at https://platform.parallel.ai

---

## Error Handling

The script handles errors gracefully and returns structured error responses:

```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2025-02-14 12:00:00"
}
```

**Common issues:**
- `PARALLEL_API_KEY not set`: Set the environment variable
- `openai not installed`: Run `pip install openai`
- `parallel-web not installed`: Run `pip install parallel-web` (only needed for extract)
- `Rate limit exceeded`: Wait and retry (default: 300 req/min for Chat API)

---

## Complementary Skills

| Skill | Use For |
|-------|---------|
| `research-lookup` | Academic paper searches (routes to Perplexity for scholarly queries) |
| `citation-management` | Google Scholar, PubMed, CrossRef database searches |
| `literature-review` | Systematic literature reviews across academic databases |
| `scientific-schematics` | Generate diagrams from research findings |

---

## Reference: Api_Reference

# Parallel Web Systems API Quick Reference

**Full Documentation:** https://docs.parallel.ai
**API Key:** https://platform.parallel.ai
**Python SDK:** `pip install parallel-web`
**Environment Variable:** `PARALLEL_API_KEY`

---

## Search API (Beta)

**Endpoint:** `POST https://api.parallel.ai/v1beta/search`
**Header:** `parallel-beta: search-extract-2025-10-10`

### Request

```json
{
  "objective": "Natural language search goal (max 5000 chars)",
  "search_queries": ["keyword query 1", "keyword query 2"],
  "max_results": 10,
  "excerpts": {
    "max_chars_per_result": 10000,
    "max_chars_total": 50000
  },
  "source_policy": {
    "allow_domains": ["example.com"],
    "deny_domains": ["spam.com"],
    "after_date": "2024-01-01"
  }
}
```

### Response

```json
{
  "search_id": "search_...",
  "results": [
    {
      "url": "https://...",
      "title": "Page Title",
      "publish_date": "2025-01-15",
      "excerpts": ["Relevant content..."]
    }
  ]
}
```

### Python SDK

```python
from parallel import Parallel
client = Parallel(api_key="...")
result = client.beta.search(
    objective="...",
    search_queries=["..."],
    max_results=10,
    excerpts={"max_chars_per_result": 10000},
)
```

**Cost:** $5 per 1,000 requests (default 10 results each)
**Rate Limit:** 600 requests/minute

---

## Extract API (Beta)

**Endpoint:** `POST https://api.parallel.ai/v1beta/extract`
**Header:** `parallel-beta: search-extract-2025-10-10`

### Request

```json
{
  "urls": ["https://example.com/page"],
  "objective": "What to focus on",
  "excerpts": true,
  "full_content": false
}
```

### Response

```json
{
  "extract_id": "extract_...",
  "results": [
    {
      "url": "https://...",
      "title": "Page Title",
      "excerpts": ["Focused content..."],
      "full_content": null
    }
  ],
  "errors": []
}
```

### Python SDK

```python
result = client.beta.extract(
    urls=["https://..."],
    objective="...",
    excerpts=True,
    full_content=False,
)
```

**Cost:** $1 per 1,000 URLs
**Rate Limit:** 600 requests/minute

---

## Task API (Deep Research)

**Endpoint:** `POST https://api.parallel.ai/v1/tasks/runs`

### Create Task Run

```json
{
  "input": "Research question (max 15,000 chars)",
  "processor": "pro-fast",
  "task_spec": {
    "output_schema": {
      "type": "text"
    }
  }
}
```

### Response (immediate)

```json
{
  "run_id": "trun_...",
  "status": "queued"
}
```

### Get Result (blocking)

**Endpoint:** `GET https://api.parallel.ai/v1/tasks/runs/{run_id}/result`

### Python SDK

```python
# Text output (markdown report with citations)
from parallel.types import TaskSpecParam
task_run = client.task_run.create(
    input="Research question",
    processor="pro-fast",
    task_spec=TaskSpecParam(output_schema={"type": "text"}),
)
result = client.task_run.result(task_run.run_id, api_timeout=3600)
print(result.output.content)

# Auto-schema output (structured JSON)
task_run = client.task_run.create(
    input="Research question",
    processor="pro-fast",
)
result = client.task_run.result(task_run.run_id, api_timeout=3600)
print(result.output.content)  # structured dict
print(result.output.basis)    # citations per field
```

### Processors

| Processor | Latency | Cost/1000 | Best For |
|-----------|---------|-----------|----------|
| `lite-fast` | 10-20s | $5 | Basic metadata |
| `base-fast` | 15-50s | $10 | Standard enrichments |
| `core-fast` | 15s-100s | $25 | Cross-referenced |
| `core2x-fast` | 15s-3min | $50 | High complexity |
| **`pro-fast`** | **30s-5min** | **$100** | **Default: exploratory research** |
| `ultra-fast` | 1-10min | $300 | Deep multi-source |
| `ultra2x-fast` | 1-20min | $600 | Difficult research |
| `ultra4x-fast` | 1-40min | $1200 | Very difficult |
| `ultra8x-fast` | 1hr | $2400 | Most difficult |

Standard (non-fast) processors have the same cost but higher latency and freshest data.

---

## Chat API (Beta)

**Endpoint:** `POST https://api.parallel.ai/chat/completions`
**Compatible with OpenAI SDK.**

### Models

| Model | Latency (TTFT) | Cost/1000 | Use Case |
|-------|----------------|-----------|----------|
| `speed` | ~3s | $5 | Low-latency chat |
| `lite` | 10-60s | $5 | Simple lookups with basis |
| `base` | 15-100s | $10 | Standard research with basis |
| `core` | 1-5min | $25 | Complex research with basis |

### Python SDK (OpenAI-compatible)

```python
from openai import OpenAI
client = OpenAI(
    api_key="PARALLEL_API_KEY",
    base_url="https://api.parallel.ai",
)
response = client.chat.completions.create(
    model="speed",
    messages=[{"role": "user", "content": "What is Parallel Web Systems?"}],
)
```

---

## Rate Limits

| API | Default Limit |
|-----|---------------|
| Search | 600 req/min |
| Extract | 600 req/min |
| Chat | 300 req/min |
| Task | Varies by processor |

---

## Source Policy

Control which sources are used in searches:

```json
{
  "source_policy": {
    "allow_domains": ["nature.com", "science.org"],
    "deny_domains": ["unreliable-source.com"],
    "after_date": "2024-01-01"
  }
}
```

Works with Search API and can be used to focus results on specific authoritative domains.

---

## Reference: Deep_Research_Guide

# Deep Research Guide

Comprehensive guide to using Parallel's Task API for deep research, including processor selection, output formats, structured schemas, and advanced patterns.

---

## Overview

Deep Research transforms natural language research queries into comprehensive intelligence reports. Unlike simple search, it performs multi-step web exploration across authoritative sources and synthesizes findings with inline citations and confidence levels.

**Key characteristics:**
- Multi-step, multi-source research
- Automatic citation and source attribution
- Structured or text output formats
- Asynchronous processing (30 seconds to 25+ minutes)
- Research basis with confidence levels per finding

---

## Processor Selection

Choosing the right processor is the most important decision. It determines research depth, speed, and cost.

### Decision Matrix

| Scenario | Recommended Processor | Why |
|----------|----------------------|-----|
| Quick background for a paper section | `pro-fast` | Fast, good depth, low cost |
| Comprehensive market research report | `ultra-fast` | Deep multi-source synthesis |
| Simple fact lookup or metadata | `base-fast` | Fast, low cost |
| Competitive landscape analysis | `pro-fast` | Good balance of depth and speed |
| Background for grant proposal | `pro-fast` | Thorough but timely |
| State-of-the-art review for a topic | `ultra-fast` | Maximum source coverage |
| Quick question during writing | `core-fast` | Sub-2-minute response |
| Breaking news or very recent events | `pro` (standard) | Freshest data prioritized |
| Large-scale data enrichment | `base-fast` | Cost-effective at scale |

### Processor Tiers Explained

**`pro-fast`** (default, recommended for most tasks):
- Latency: 30 seconds to 5 minutes
- Depth: Explores 10-20+ web sources
- Best for: Section-level research, background gathering, comparative analysis
- Cost: $0.10 per query

**`ultra-fast`** (for comprehensive research):
- Latency: 1 to 10 minutes
- Depth: Explores 20-50+ web sources, multiple reasoning steps
- Best for: Full reports, market analysis, complex multi-faceted questions
- Cost: $0.30 per query

**`core-fast`** (quick cross-referenced answers):
- Latency: 15 seconds to 100 seconds
- Depth: Cross-references 5-10 sources
- Best for: Moderate complexity questions, verification tasks
- Cost: $0.025 per query

**`base-fast`** (simple enrichment):
- Latency: 15 to 50 seconds
- Depth: Standard web lookup, 3-5 sources
- Best for: Simple factual queries, metadata enrichment
- Cost: $0.01 per query

### Standard vs Fast

- **Fast processors** (`-fast`): 2-5x faster, very fresh data, ideal for interactive use
- **Standard processors** (no suffix): Highest data freshness, better for background jobs

**Rule of thumb:** Always use `-fast` variants unless you specifically need the freshest possible data (breaking news, live financial data, real-time events).

---

## Output Formats

### Text Mode (Markdown Reports)

Returns a comprehensive markdown report with inline citations. Best for human consumption and document integration.

```python
researcher = ParallelDeepResearch()

result = researcher.research(
    query="Comprehensive analysis of mRNA vaccine technology platforms and their applications beyond COVID-19",
    processor="pro-fast",
    description="Focus on clinical trials, approved applications, pipeline developments, and key companies. Include market size data."
)

# result["output"] contains a full markdown report
# result["citations"] contains source URLs with excerpts
```

**When to use text mode:**
- Writing scientific documents (papers, reviews, reports)
- Background research for a topic
- Creating summaries for human readers
- When you need flowing prose, not structured data

**Guiding text output with `description`:**

The `description` parameter steers the report content:

```python
# Focus on specific aspects
result = researcher.research(
    query="Electric vehicle battery technology landscape",
    description="Focus on: (1) solid-state battery progress, (2) charging speed improvements, (3) cost per kWh trends, (4) key patents and IP. Format as a structured report with clear sections."
)

# Control length and depth
result = researcher.research(
    query="AI in drug discovery",
    description="Provide a concise 500-word executive summary covering key applications, notable successes, leading companies, and market projections."
)
```

### Auto-Schema Mode (Structured JSON)

Lets the processor determine the best output structure automatically. Returns structured JSON with per-field citations.

```python
result = researcher.research_structured(
    query="Top 5 cloud computing companies: revenue, market share, key products, and recent developments",
    processor="pro-fast",
)

# result["content"] contains structured data (dict)
# result["basis"] contains per-field citations with confidence
```

**When to use auto-schema:**
- Data extraction and enrichment
- Comparative analysis with specific fields
- When you need programmatic access to individual data points
- Integration with databases or spreadsheets

### Custom JSON Schema

Define exactly what fields you want returned:

```python
schema = {
    "type": "object",
    "properties": {
        "market_size_2024": {
            "type": "string",
            "description": "Global market size in USD billions for 2024. Include source."
        },
        "growth_rate": {
            "type": "string",
            "description": "CAGR percentage for 2024-2030 forecast period."
        },
        "top_companies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Company name"},
                    "market_share": {"type": "string", "description": "Approximate market share percentage"},
                    "revenue": {"type": "string", "description": "Most recent annual revenue"}
                },
                "required": ["name", "market_share", "revenue"]
            },
            "description": "Top 5 companies by market share"
        },
        "key_trends": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Top 3-5 industry trends driving growth"
        }
    },
    "required": ["market_size_2024", "growth_rate", "top_companies", "key_trends"],
    "additionalProperties": False
}

result = researcher.research_structured(
    query="Global cybersecurity market analysis",
    output_schema=schema,
)
```

---

## Writing Effective Research Queries

### Query Construction Framework

Structure your query as: **[Topic] + [Specific Aspect] + [Scope/Time] + [Output Expectations]**

**Good queries:**
```
"Comprehensive analysis of the global lithium-ion battery recycling market,
including market size, key players, regulatory drivers, and technology
approaches. Focus on 2023-2025 developments."

"Compare the efficacy, safety profiles, and cost-effectiveness of GLP-1
receptor agonists (semaglutide, tirzepatide, liraglutide) for type 2
diabetes management based on recent clinical trial data."

"Survey of federated learning approaches for healthcare AI, covering
privacy-preserving techniques, real-world deployments, regulatory
compliance, and performance benchmarks from 2023-2025 publications."
```

**Poor queries:**
```
"Tell me about batteries"          # Too vague
"AI"                                # No specific aspect
"What's new?"                       # No topic at all
"Everything about quantum computing from all time"  # Too broad
```

### Tips for Better Results

1. **Be specific about what you need**: "market size" vs "tell me about the market"
2. **Include time bounds**: "2024-2025" narrows to relevant data
3. **Name entities**: "semaglutide vs tirzepatide" vs "diabetes drugs"
4. **Specify output expectations**: "Include statistics, key players, and growth projections"
5. **Keep under 15,000 characters**: Concise queries work better than massive prompts

---

## Working with Research Basis

Every deep research result includes a **basis** -- citations, reasoning, and confidence levels for each finding.

### Text Mode Basis

```python
result = researcher.research(query="...", processor="pro-fast")

# Citations are deduplicated and include URLs + excerpts
for citation in result["citations"]:
    print(f"Source: {citation['title']}")
    print(f"URL: {citation['url']}")
    if citation.get("excerpts"):
        print(f"Excerpt: {citation['excerpts'][0][:200]}")
```

### Structured Mode Basis

```python
result = researcher.research_structured(query="...", processor="pro-fast")

for basis_entry in result["basis"]:
    print(f"Field: {basis_entry['field']}")
    print(f"Confidence: {basis_entry['confidence']}")
    print(f"Reasoning: {basis_entry['reasoning']}")
    for cit in basis_entry["citations"]:
        print(f"  Source: {cit['url']}")
```

### Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| `high` | Multiple authoritative sources agree | Use directly |
| `medium` | Some supporting evidence, minor uncertainty | Use with caveat |
| `low` | Limited evidence, significant uncertainty | Verify independently |

---

## Advanced Patterns

### Multi-Stage Research

Use different processors in sequence for progressively deeper research:

```python
# Stage 1: Quick overview with base-fast
overview = researcher.research(
    query="What are the main approaches to quantum error correction?",
    processor="base-fast",
)

# Stage 2: Deep dive on the most promising approach
deep_dive = researcher.research(
    query=f"Detailed analysis of surface code quantum error correction: "
          f"recent breakthroughs, implementation challenges, and leading research groups. "
          f"Context: {overview['output'][:500]}",
    processor="pro-fast",
)
```

### Comparative Research

```python
result = researcher.research(
    query="Compare and contrast three leading large language model architectures: "
          "GPT-4, Claude, and Gemini. Cover architecture differences, benchmark performance, "
          "pricing, context window, and unique capabilities. Include specific benchmark scores.",
    processor="pro-fast",
    description="Create a structured comparison with a summary table. Include specific numbers and benchmarks."
)
```

### Research with Follow-Up Extraction

```python
# Step 1: Research to find relevant sources
research_result = researcher.research(
    query="Most influential papers on attention mechanisms in 2024",
    processor="pro-fast",
)

# Step 2: Extract full content from the most relevant sources
from parallel_web import ParallelExtract
extractor = ParallelExtract()

key_urls = [c["url"] for c in research_result["citations"][:5]]
for url in key_urls:
    extracted = extractor.extract(
        urls=[url],
        objective="Key methodology, results, and conclusions",
    )
```

---

## Performance Optimization

### Reducing Latency

1. **Use `-fast` processors**: 2-5x faster than standard
2. **Use `core-fast` for moderate queries**: Sub-2-minute for most questions
3. **Be specific in queries**: Vague queries require more exploration
4. **Set appropriate timeouts**: Don't over-wait

### Reducing Cost

1. **Start with `base-fast`**: Upgrade only if depth is insufficient
2. **Use `core-fast` for moderate complexity**: $0.025 vs $0.10 for pro
3. **Batch related queries**: One well-crafted query > multiple simple ones
4. **Cache results**: Store research output for reuse across sections

### Maximizing Quality

1. **Use `pro-fast` or `ultra-fast`**: More sources = better synthesis
2. **Provide context**: "I'm writing a paper for Nature Medicine about..."
3. **Use `description` parameter**: Guide the output structure and focus
4. **Verify critical findings**: Cross-check with Search API or Extract

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Query too vague | Scattered, unfocused results | Add specific aspects and time bounds |
| Query too long (>15K chars) | API rejection or degraded results | Summarize context, focus on key question |
| Wrong processor | Too slow or too shallow | Use decision matrix above |
| Not using `description` | Report structure not aligned with needs | Add description to guide output |
| Ignoring confidence levels | Using low-confidence data as fact | Check basis confidence before citing |
| Not verifying citations | Risk of outdated or misattributed data | Cross-check key citations with Extract |

---

## See Also

- [API Reference](api_reference.md) - Complete API parameter reference
- [Search Best Practices](search_best_practices.md) - For quick web searches
- [Extraction Patterns](extraction_patterns.md) - For reading specific URLs
- [Workflow Recipes](workflow_recipes.md) - Common multi-step patterns

---

## Reference: Extraction_Patterns

# Extraction Patterns

Guide to using Parallel's Extract API for converting web pages into clean, LLM-optimized content.

---

## Overview

The Extract API converts any public URL into clean markdown. It handles JavaScript-heavy pages, PDFs, and complex layouts that simple HTTP fetching cannot parse. Results are optimized for LLM consumption.

**Key capabilities:**
- JavaScript rendering (SPAs, dynamic content)
- PDF extraction to clean text
- Focused excerpts aligned to your objective
- Full page content extraction
- Multiple URL batch processing

---

## When to Use Extract vs Search

| Scenario | Use Extract | Use Search |
|----------|-------------|------------|
| You have a specific URL | Yes | No |
| You need content from a known page | Yes | No |
| You want to find pages about a topic | No | Yes |
| You need to read a research paper URL | Yes | No |
| You need to verify information on a specific site | Yes | No |
| You're looking for information broadly | No | Yes |
| You found URLs from a search and want full content | Yes | No |

**Rule of thumb:** If you have a URL, use Extract. If you need to find URLs, use Search.

---

## Excerpt Mode vs Full Content Mode

### Excerpt Mode (Default)

Returns focused content aligned to your objective. Smaller token footprint, higher relevance.

```python
extractor = ParallelExtract()

result = extractor.extract(
    urls=["https://arxiv.org/abs/2301.12345"],
    objective="Key methodology and experimental results",
    excerpts=True,     # Default
    full_content=False  # Default
)
```

**Best for:**
- Extracting specific information from long pages
- Token-efficient processing
- When you know what you're looking for
- Reading papers for specific claims or data points

### Full Content Mode

Returns the complete page content as clean markdown.

```python
result = extractor.extract(
    urls=["https://docs.example.com/api-reference"],
    objective="Complete API documentation",
    excerpts=False,
    full_content=True,
)
```

**Best for:**
- Complete documentation pages
- Full article text needed for analysis
- When you need every detail, not just excerpts
- Archiving or converting web content

### Both Modes

You can request both excerpts and full content:

```python
result = extractor.extract(
    urls=["https://example.com/report"],
    objective="Executive summary and key recommendations",
    excerpts=True,
    full_content=True,
)

# Use excerpts for focused analysis
# Use full_content for complete reference
```

---

## Objective Writing for Extraction

The `objective` parameter focuses extraction on relevant content. It dramatically improves excerpt quality.

### Good Objectives

```python
# Specific and actionable
objective="Extract the methodology section, including sample size, statistical methods, and primary endpoints"

# Clear about what you need
objective="Find the pricing information, feature comparison table, and enterprise plan details"

# Targeted for your task
objective="Key findings, effect sizes, confidence intervals, and author conclusions from this clinical trial"
```

### Poor Objectives

```python
# Too vague
objective="Tell me about this page"

# No objective at all (still works but excerpts are less focused)
extractor.extract(urls=["https://..."])
```

### Objective Templates by Use Case

**Academic Paper:**
```python
objective="Abstract, key findings, methodology (sample size, design, statistical tests), results with effect sizes and p-values, and main conclusions"
```

**Product/Company Page:**
```python
objective="Company overview, key products/services, pricing, founding date, leadership team, and recent announcements"
```

**Technical Documentation:**
```python
objective="API endpoints, authentication methods, request/response formats, rate limits, and code examples"
```

**News Article:**
```python
objective="Main story, key quotes, data points, timeline of events, and named sources"
```

**Government/Policy Document:**
```python
objective="Key policy provisions, effective dates, affected parties, compliance requirements, and penalties"
```

---

## Batch Extraction

Extract from multiple URLs in a single call:

```python
result = extractor.extract(
    urls=[
        "https://nature.com/articles/s12345",
        "https://science.org/doi/full/10.1234/science.xyz",
        "https://thelancet.com/journals/lancet/article/PIIS0140-6736(24)12345/fulltext"
    ],
    objective="Key findings, sample sizes, and statistical results from each study",
)

# Results are returned in the same order as input URLs
for r in result["results"]:
    print(f"=== {r['title']} ===")
    print(f"URL: {r['url']}")
    for excerpt in r["excerpts"]:
        print(excerpt[:500])
```

**Batch limits:**
- No hard limit on number of URLs per request
- Each URL counts as one extraction unit for billing
- Large batches may take longer to process
- Failed URLs are reported in the `errors` field without blocking successful ones

---

## Handling Different Content Types

### Web Pages (HTML)

Standard extraction. JavaScript is rendered, so SPAs and dynamic content work.

```python
# Standard web page
result = extractor.extract(
    urls=["https://example.com/article"],
    objective="Main article content",
)
```

### PDFs

PDFs are automatically detected and converted to text.

```python
# PDF extraction
result = extractor.extract(
    urls=["https://example.com/whitepaper.pdf"],
    objective="Executive summary and key recommendations",
)
```

### Documentation Sites

Single-page apps and documentation frameworks (Docusaurus, GitBook, ReadTheDocs) are fully rendered.

```python
result = extractor.extract(
    urls=["https://docs.example.com/getting-started"],
    objective="Installation instructions and quickstart guide",
    full_content=True,
)
```

---

## Common Extraction Patterns

### Pattern 1: Search Then Extract

Find relevant pages with Search, then extract full content from the best results.

```python
from parallel_web import ParallelSearch, ParallelExtract

searcher = ParallelSearch()
extractor = ParallelExtract()

# Step 1: Find relevant pages
search_result = searcher.search(
    objective="Find the original transformer paper and its key follow-up papers",
    search_queries=["attention is all you need paper", "transformer architecture paper"],
)

# Step 2: Extract detailed content from top results
top_urls = [r["url"] for r in search_result["results"][:3]]
extract_result = extractor.extract(
    urls=top_urls,
    objective="Abstract, architecture description, key results, and ablation studies",
)
```

### Pattern 2: DOI Resolution and Paper Reading

```python
# Extract content from a DOI URL
result = extractor.extract(
    urls=["https://doi.org/10.1038/s41586-024-07487-w"],
    objective="Study design, patient population, primary endpoints, efficacy results, and safety data",
)
```

### Pattern 3: Competitive Intelligence from Company Pages

```python
companies = [
    "https://openai.com/about",
    "https://anthropic.com/company",
    "https://deepmind.google/about/",
]

result = extractor.extract(
    urls=companies,
    objective="Company mission, team size, key products, recent announcements, and funding information",
)
```

### Pattern 4: Documentation Extraction for Reference

```python
result = extractor.extract(
    urls=["https://docs.parallel.ai/search/search-quickstart"],
    objective="Complete API usage guide including request format, response format, and code examples",
    full_content=True,
)
```

### Pattern 5: Metadata Verification

```python
# Verify citation metadata for a specific paper
result = extractor.extract(
    urls=["https://doi.org/10.1234/example-doi"],
    objective="Complete citation metadata: authors, title, journal, volume, pages, year, DOI",
)
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| URL not accessible | Page requires authentication, is behind paywall, or is down | Try a different URL or use Search instead |
| Timeout | Page takes too long to render | Retry or use a simpler URL |
| Empty content | Page is dynamically loaded in a way that can't be rendered | Try full_content mode or use Search |
| Rate limited | Too many requests | Wait and retry, or reduce batch size |

### Checking for Errors

```python
result = extractor.extract(urls=["https://example.com/page"])

if not result["success"]:
    print(f"Extraction failed: {result['error']}")
elif result.get("errors"):
    print(f"Some URLs failed: {result['errors']}")
else:
    print(f"Successfully extracted {len(result['results'])} pages")
```

---

## Tips and Best Practices

1. **Always provide an objective**: Even a general one improves excerpt quality significantly
2. **Use excerpts by default**: Full content is only needed when you truly need everything
3. **Batch related URLs**: One call with 5 URLs is better than 5 separate calls
4. **Check for errors**: Not all URLs are extractable (paywalls, auth, etc.)
5. **Combine with Search**: Search finds URLs, Extract reads them in detail
6. **Use for DOI resolution**: Extract handles DOI redirects automatically
7. **Prefer Extract over manual fetching**: Handles JavaScript, PDFs, and complex layouts

---

## See Also

- [API Reference](api_reference.md) - Complete API parameter reference
- [Search Best Practices](search_best_practices.md) - For finding URLs to extract
- [Deep Research Guide](deep_research_guide.md) - For comprehensive research tasks
- [Workflow Recipes](workflow_recipes.md) - Common multi-step patterns

---

## Reference: Search_Best_Practices

# Search API Best Practices

Comprehensive guide to getting the best results from Parallel's Search API.

---

## Core Concepts

The Search API returns ranked, LLM-optimized excerpts from web sources based on natural language objectives. Results are designed to serve directly as model input, enabling faster reasoning and higher-quality completions.

### Key Advantages Over Traditional Search

- **Context engineering for token efficiency**: Results are ranked by reasoning utility, not engagement
- **Single-hop resolution**: Complex multi-topic queries resolved in one request
- **Multi-hop efficiency**: Deep research workflows complete in fewer tool calls

---

## Crafting Effective Search Queries

### Provide Both `objective` AND `search_queries`

The `objective` describes your broader goal; `search_queries` ensures specific keywords are prioritized. Using both together gives significantly better results.

**Good:**
```python
searcher.search(
    objective="I'm writing a literature review on Alzheimer's treatments. Find peer-reviewed research papers and clinical trial results from the past 2 years on amyloid-beta targeted therapies.",
    search_queries=[
        "amyloid beta clinical trials 2024-2025",
        "Alzheimer's monoclonal antibody treatment results",
        "lecanemab donanemab trial outcomes"
    ],
)
```

**Poor:**
```python
# Too vague - no context about intent
searcher.search(objective="Alzheimer's treatment")

# Missing objective - no context for ranking
searcher.search(search_queries=["Alzheimer's drugs"])
```

### Objective Writing Tips

1. **State your broader task**: "I'm writing a research paper on...", "I'm analyzing the market for...", "I'm preparing a presentation about..."
2. **Be specific about source preferences**: "Prefer official government websites", "Focus on peer-reviewed journals", "From major news outlets"
3. **Include freshness requirements**: "From the past 6 months", "Published in 2024-2025", "Most recent data available"
4. **Specify content type**: "Technical documentation", "Clinical trial results", "Market analysis reports", "Product announcements"

### Example Objectives by Use Case

**Academic Research:**
```
"I'm writing a literature review on CRISPR gene editing applications in cancer therapy.
Find peer-reviewed papers from Nature, Science, Cell, and other high-impact journals
published in 2023-2025. Prefer clinical trial results and systematic reviews."
```

**Market Intelligence:**
```
"I'm preparing Q1 2025 investor materials for a fintech startup.
Find recent announcements from the Federal Reserve and SEC about digital asset
regulations and banking partnerships with crypto firms. Past 3 months only."
```

**Technical Documentation:**
```
"I'm designing a machine learning course. Find technical documentation and API guides
that explain how transformer attention mechanisms work, preferably from official
framework documentation like PyTorch or Hugging Face."
```

**Current Events:**
```
"I'm tracking AI regulation developments. Find official policy announcements,
legislative actions, and regulatory guidance from the EU, US, and UK governments
from the past month."
```

---

## Search Modes

Use the `mode` parameter to optimize for your workflow:

| Mode | Best For | Excerpt Style | Latency |
|------|----------|---------------|---------|
| `one-shot` (default) | Direct queries, single-request workflows | Comprehensive, longer | Lower |
| `agentic` | Multi-step reasoning loops, agent workflows | Concise, token-efficient | Slightly higher |
| `fast` | Real-time applications, UI auto-complete | Minimal, speed-optimized | ~1 second |

### When to Use Each Mode

**`one-shot`** (default):
- Single research question that needs comprehensive answer
- Writing a section of a paper and need full context
- Background research before starting a document
- Any case where you'll make only one search call

**`agentic`**:
- Multi-step research workflows (search → analyze → search again)
- Agent loops where token efficiency matters
- Iterative refinement of research queries
- When integrating with other tools (search → extract → synthesize)

**`fast`**:
- Live autocomplete or suggestion systems
- Quick fact-checking during writing
- Real-time metadata lookups
- Any latency-sensitive application

---

## Source Policy

Control which domains are included or excluded from results:

```python
searcher.search(
    objective="Find clinical trial results for new cancer immunotherapy drugs",
    search_queries=["checkpoint inhibitor clinical trials 2025"],
    source_policy={
        "allow_domains": ["clinicaltrials.gov", "nejm.org", "thelancet.com", "nature.com"],
        "deny_domains": ["reddit.com", "quora.com"],
        "after_date": "2024-01-01"
    },
)
```

### Source Policy Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `allow_domains` | list[str] | Only include results from these domains |
| `deny_domains` | list[str] | Exclude results from these domains |
| `after_date` | str (YYYY-MM-DD) | Only include content published after this date |

### Domain Lists by Use Case

**Academic Research:**
```python
allow_domains = [
    "nature.com", "science.org", "cell.com", "thelancet.com",
    "nejm.org", "bmj.com", "pnas.org", "arxiv.org",
    "pubmed.ncbi.nlm.nih.gov", "scholar.google.com"
]
```

**Technology/AI:**
```python
allow_domains = [
    "arxiv.org", "openai.com", "anthropic.com", "deepmind.google",
    "huggingface.co", "pytorch.org", "tensorflow.org",
    "proceedings.neurips.cc", "proceedings.mlr.press"
]
```

**Market Intelligence:**
```python
deny_domains = [
    "reddit.com", "quora.com", "medium.com",
    "wikipedia.org"  # Good for facts, not for market data
]
```

**Government/Policy:**
```python
allow_domains = [
    "gov", "europa.eu", "who.int", "worldbank.org",
    "imf.org", "oecd.org", "un.org"
]
```

---

## Controlling Result Volume

### `max_results` Parameter

- Range: 1-20 (default: 10)
- More results = broader coverage but more tokens to process
- Fewer results = more focused but may miss relevant sources

**Recommendations:**
- Quick fact check: `max_results=3`
- Standard research: `max_results=10` (default)
- Comprehensive survey: `max_results=20`

### Excerpt Length Control

```python
searcher.search(
    objective="...",
    max_chars_per_result=10000,  # Default: 10000
)
```

- **Short excerpts (1000-3000)**: Quick summaries, metadata extraction
- **Medium excerpts (5000-10000)**: Standard research, balanced depth
- **Long excerpts (10000-50000)**: Full article content, deep analysis

---

## Common Patterns

### Pattern 1: Research Before Writing

```python
# Before writing each section, search for relevant information
result = searcher.search(
    objective="Find recent advances in transformer attention mechanisms for a NeurIPS paper introduction",
    search_queries=["attention mechanism innovations 2024", "efficient transformers"],
    max_results=10,
)

# Extract key findings for the section
for r in result["results"]:
    print(f"Source: {r['title']} ({r['url']})")
    # Use excerpts to inform writing
```

### Pattern 2: Fact Verification

```python
# Quick verification of a specific claim
result = searcher.search(
    objective="Verify: Did GPT-4 achieve 86.4% on MMLU benchmark?",
    search_queries=["GPT-4 MMLU benchmark score"],
    max_results=5,
)
```

### Pattern 3: Competitive Intelligence

```python
result = searcher.search(
    objective="Find recent product launches and funding announcements for AI coding assistants in 2025",
    search_queries=[
        "AI coding assistant funding 2025",
        "code generation tool launch",
        "AI developer tools new product"
    ],
    source_policy={"after_date": "2025-01-01"},
    max_results=15,
)
```

### Pattern 4: Multi-Language Research

```python
# Search includes multilingual results automatically
result = searcher.search(
    objective="Find global perspectives on AI regulation, including EU, China, and US approaches",
    search_queries=[
        "EU AI Act implementation 2025",
        "China AI regulation policy",
        "US AI executive order updates"
    ],
)
```

---

## Troubleshooting

### Few or No Results

- **Broaden your objective**: Remove overly specific constraints
- **Add more search queries**: Different phrasings of the same concept
- **Remove source policy**: Domain restrictions may be too narrow
- **Check date filters**: `after_date` may be too recent

### Irrelevant Results

- **Make objective more specific**: Add context about your task
- **Use source policy**: Allow only authoritative domains
- **Add negative context**: "Not about [unrelated topic]"
- **Refine search queries**: Use more precise keywords

### Too Many Tokens in Results

- **Reduce `max_results`**: From 10 to 5 or 3
- **Reduce excerpt length**: Lower `max_chars_per_result`
- **Use `agentic` mode**: More concise excerpts
- **Use `fast` mode**: Minimal excerpts

---

## See Also

- [API Reference](api_reference.md) - Complete API parameter reference
- [Deep Research Guide](deep_research_guide.md) - For comprehensive research tasks
- [Extraction Patterns](extraction_patterns.md) - For reading specific URLs
- [Workflow Recipes](workflow_recipes.md) - Common multi-step patterns

---

## Reference: Workflow_Recipes

# Workflow Recipes

Common multi-step patterns combining Parallel's Search, Extract, and Deep Research APIs for scientific writing tasks.

---

## Recipe Index

| Recipe | APIs Used | Time | Use Case |
|--------|-----------|------|----------|
| [Section Research Pipeline](#recipe-1-section-research-pipeline) | Research + Search | 2-5 min | Writing a paper section |
| [Citation Verification](#recipe-2-citation-verification) | Search + Extract | 1-2 min | Verifying paper metadata |
| [Literature Survey](#recipe-3-literature-survey) | Research + Search + Extract | 5-15 min | Comprehensive lit review |
| [Market Intelligence Report](#recipe-4-market-intelligence-report) | Research (multi-stage) | 10-30 min | Market/industry analysis |
| [Competitive Analysis](#recipe-5-competitive-analysis) | Search + Extract + Research | 5-10 min | Comparing companies/products |
| [Fact-Check Pipeline](#recipe-6-fact-check-pipeline) | Search + Extract | 1-3 min | Verifying claims |
| [Current Events Briefing](#recipe-7-current-events-briefing) | Search + Research | 3-5 min | News synthesis |
| [Technical Documentation Gathering](#recipe-8-technical-documentation-gathering) | Search + Extract | 2-5 min | API/framework docs |
| [Grant Background Research](#recipe-9-grant-background-research) | Research + Search | 5-10 min | Grant proposal background |

---

## Recipe 1: Section Research Pipeline

**Goal:** Gather research and citations for writing a single section of a scientific paper.

**APIs:** Deep Research (pro-fast) + Search

```bash
# Step 1: Deep research for comprehensive background
python scripts/parallel_web.py research \
  "Recent advances in federated learning for healthcare AI, focusing on privacy-preserving training methods, real-world deployments, and regulatory considerations (2023-2025)" \
  --processor pro-fast -o sources/section_background.md

# Step 2: Targeted search for specific citations
python scripts/parallel_web.py search \
  "Find peer-reviewed papers on federated learning in hospitals" \
  --queries "federated learning clinical deployment" "privacy preserving ML healthcare" \
  --max-results 10 -o sources/section_citations.txt
```

**Python version:**
```python
from parallel_web import ParallelDeepResearch, ParallelSearch

researcher = ParallelDeepResearch()
searcher = ParallelSearch()

# Step 1: Deep background research
background = researcher.research(
    query="Recent advances in federated learning for healthcare AI (2023-2025): "
          "privacy-preserving methods, real-world deployments, regulatory landscape",
    processor="pro-fast",
    description="Structure as: (1) Key approaches, (2) Clinical deployments, "
                "(3) Regulatory considerations, (4) Open challenges. Include statistics."
)

# Step 2: Find specific papers to cite
papers = searcher.search(
    objective="Find recent peer-reviewed papers on federated learning deployed in hospital settings",
    search_queries=[
        "federated learning hospital clinical study 2024",
        "privacy preserving machine learning healthcare deployment"
    ],
    source_policy={"allow_domains": ["nature.com", "thelancet.com", "arxiv.org", "pubmed.ncbi.nlm.nih.gov"]},
)

# Combine: use background for writing, papers for citations
```

**When to use:** Before writing each major section of a research paper, literature review, or grant proposal.

---

## Recipe 2: Citation Verification

**Goal:** Verify that a citation is real and get complete metadata (DOI, volume, pages, year).

**APIs:** Search + Extract

```bash
# Option A: Search for the paper
python scripts/parallel_web.py search \
  "Vaswani et al 2017 Attention is All You Need paper NeurIPS" \
  --queries "Attention is All You Need DOI" --max-results 5

# Option B: Extract metadata from a DOI
python scripts/parallel_web.py extract \
  "https://doi.org/10.48550/arXiv.1706.03762" \
  --objective "Complete citation: authors, title, venue, year, pages, DOI"
```

**Python version:**
```python
from parallel_web import ParallelSearch, ParallelExtract

searcher = ParallelSearch()
extractor = ParallelExtract()

# Step 1: Find the paper
result = searcher.search(
    objective="Find the exact citation details for the Attention Is All You Need paper by Vaswani et al.",
    search_queries=["Attention is All You Need Vaswani 2017 NeurIPS DOI"],
    max_results=5,
)

# Step 2: Extract full metadata from the paper's page
paper_url = result["results"][0]["url"]
metadata = extractor.extract(
    urls=[paper_url],
    objective="Complete BibTeX citation: all authors, title, conference/journal, year, pages, DOI, volume",
)
```

**When to use:** After writing a section, verify every citation in references.bib has correct and complete metadata.

---

## Recipe 3: Literature Survey

**Goal:** Comprehensive survey of a research field, identifying key papers, themes, and gaps.

**APIs:** Deep Research + Search + Extract

```python
from parallel_web import ParallelDeepResearch, ParallelSearch, ParallelExtract

researcher = ParallelDeepResearch()
searcher = ParallelSearch()
extractor = ParallelExtract()

topic = "CRISPR-based diagnostics for infectious diseases"

# Stage 1: Broad research overview
overview = researcher.research(
    query=f"Comprehensive review of {topic}: key developments, clinical applications, "
          f"regulatory status, commercial products, and future directions (2020-2025)",
    processor="ultra-fast",
    description="Structure as a literature review: (1) Historical development, "
                "(2) Current technologies, (3) Clinical applications, "
                "(4) Regulatory landscape, (5) Commercial products, "
                "(6) Limitations and future directions. Include key statistics and milestones."
)

# Stage 2: Find specific landmark papers
key_papers = searcher.search(
    objective=f"Find the most cited and influential papers on {topic} from Nature, Science, Cell, NEJM",
    search_queries=[
        "CRISPR diagnostics SHERLOCK DETECTR Nature",
        "CRISPR point-of-care testing clinical study",
        "nucleic acid detection CRISPR review"
    ],
    source_policy={
        "allow_domains": ["nature.com", "science.org", "cell.com", "nejm.org", "thelancet.com"],
    },
    max_results=15,
)

# Stage 3: Extract detailed content from top 5 papers
top_urls = [r["url"] for r in key_papers["results"][:5]]
detailed = extractor.extract(
    urls=top_urls,
    objective="Study design, key results, sensitivity/specificity data, and clinical implications",
)
```

**When to use:** Starting a literature review, systematic review, or comprehensive background section.

---

## Recipe 4: Market Intelligence Report

**Goal:** Generate a comprehensive market research report on an industry or product category.

**APIs:** Deep Research (multi-stage)

```python
researcher = ParallelDeepResearch()

industry = "AI-powered drug discovery"

# Stage 1: Market overview (ultra-fast for maximum depth)
market_overview = researcher.research(
    query=f"Comprehensive market analysis of {industry}: market size, growth rate, "
          f"key segments, geographic distribution, and forecast through 2030",
    processor="ultra-fast",
    description="Include specific dollar figures, CAGR percentages, and data sources. "
                "Break down by segment and geography."
)

# Stage 2: Competitive landscape
competitors = researcher.research_structured(
    query=f"Top 10 companies in {industry}: revenue, funding, key products, partnerships, and market position",
    processor="pro-fast",
)

# Stage 3: Technology and innovation trends
tech_trends = researcher.research(
    query=f"Technology trends and innovation landscape in {industry}: "
          f"emerging approaches, breakthrough technologies, patent landscape, and R&D investment",
    processor="pro-fast",
    description="Focus on specific technologies, quantify R&D spending, and identify emerging leaders."
)

# Stage 4: Regulatory and risk analysis
regulatory = researcher.research(
    query=f"Regulatory landscape and risk factors for {industry}: "
          f"FDA guidance, EMA requirements, compliance challenges, and market risks",
    processor="pro-fast",
)
```

**When to use:** Creating market research reports, investor presentations, or strategic analysis documents.

---

## Recipe 5: Competitive Analysis

**Goal:** Compare multiple companies, products, or technologies side-by-side.

**APIs:** Search + Extract + Research

```python
searcher = ParallelSearch()
extractor = ParallelExtract()
researcher = ParallelDeepResearch()

companies = ["OpenAI", "Anthropic", "Google DeepMind"]

# Step 1: Search for recent data on each company
for company in companies:
    result = searcher.search(
        objective=f"Latest product launches, funding, team size, and strategy for {company} in 2025",
        search_queries=[f"{company} product launch 2025", f"{company} funding valuation"],
        source_policy={"after_date": "2024-06-01"},
    )

# Step 2: Extract from company pages
company_pages = [
    "https://openai.com/about",
    "https://anthropic.com/company",
    "https://deepmind.google/about/",
]
company_data = extractor.extract(
    urls=company_pages,
    objective="Mission, key products, team size, founding date, and recent milestones",
)

# Step 3: Deep research for synthesis
comparison = researcher.research(
    query=f"Detailed comparison of {', '.join(companies)}: "
          f"products, pricing, technology approach, market position, strengths, weaknesses",
    processor="pro-fast",
    description="Create a structured comparison covering: "
                "(1) Product portfolio, (2) Technology approach, (3) Pricing, "
                "(4) Market position, (5) Strengths/weaknesses, (6) Future outlook. "
                "Include a summary comparison table."
)
```

---

## Recipe 6: Fact-Check Pipeline

**Goal:** Verify specific claims or statistics before including in a document.

**APIs:** Search + Extract

```python
searcher = ParallelSearch()
extractor = ParallelExtract()

claim = "The global AI market is expected to reach $1.8 trillion by 2030"

# Step 1: Search for corroborating sources
result = searcher.search(
    objective=f"Verify this claim: '{claim}'. Find authoritative sources that confirm or contradict this figure.",
    search_queries=["global AI market size 2030 forecast", "artificial intelligence market projection trillion"],
    max_results=8,
)

# Step 2: Extract specific figures from top sources
source_urls = [r["url"] for r in result["results"][:3]]
details = extractor.extract(
    urls=source_urls,
    objective="Specific market size figures, forecast years, CAGR, and methodology of the projection",
)

# Analyze: Do multiple authoritative sources agree?
```

**When to use:** Before including any specific statistic, market figure, or factual claim in a paper or report.

---

## Recipe 7: Current Events Briefing

**Goal:** Get up-to-date synthesis of recent developments on a topic.

**APIs:** Search + Research

```python
searcher = ParallelSearch()
researcher = ParallelDeepResearch()

topic = "EU AI Act implementation"

# Step 1: Find the latest news
latest = searcher.search(
    objective=f"Latest news and developments on {topic} from the past month",
    search_queries=[f"{topic} 2025", f"{topic} latest updates"],
    source_policy={"after_date": "2025-01-15"},
    max_results=15,
)

# Step 2: Synthesize into a briefing
briefing = researcher.research(
    query=f"Summarize the latest developments in {topic} as of February 2025: "
          f"key milestones, compliance deadlines, industry reactions, and implications",
    processor="pro-fast",
    description="Write a concise 500-word executive briefing with timeline of key events."
)
```

---

## Recipe 8: Technical Documentation Gathering

**Goal:** Collect and synthesize technical documentation for a framework or API.

**APIs:** Search + Extract

```python
searcher = ParallelSearch()
extractor = ParallelExtract()

# Step 1: Find documentation pages
docs = searcher.search(
    objective="Find official PyTorch documentation for implementing custom attention mechanisms",
    search_queries=["PyTorch attention mechanism tutorial", "PyTorch MultiheadAttention documentation"],
    source_policy={"allow_domains": ["pytorch.org", "github.com/pytorch"]},
)

# Step 2: Extract full content from documentation pages
doc_urls = [r["url"] for r in docs["results"][:3]]
full_docs = extractor.extract(
    urls=doc_urls,
    objective="Complete API reference, parameters, usage examples, and code snippets",
    full_content=True,
)
```

---

## Recipe 9: Grant Background Research

**Goal:** Build a comprehensive background section for a grant proposal with verified statistics.

**APIs:** Deep Research + Search

```python
researcher = ParallelDeepResearch()
searcher = ParallelSearch()

research_area = "AI-guided antibiotic discovery to combat antimicrobial resistance"

# Step 1: Significance and burden of disease
significance = researcher.research(
    query=f"Burden of antimicrobial resistance: mortality statistics, economic impact, "
          f"WHO priority pathogens, and projections. Include specific numbers.",
    processor="pro-fast",
    description="Focus on statistics suitable for NIH Significance section: "
                "deaths per year, economic cost, resistance trends, and urgency."
)

# Step 2: Innovation landscape
innovation = researcher.research(
    query=f"Current approaches to {research_area}: successes (halicin, etc.), "
          f"limitations of current methods, and what makes our approach novel",
    processor="pro-fast",
    description="Focus on Innovation section: what has been tried, what gaps remain, "
                "and what new approaches are emerging."
)

# Step 3: Find specific papers for preliminary data context
papers = searcher.search(
    objective="Find landmark papers on AI-discovered antibiotics and ML approaches to drug discovery",
    search_queries=[
        "halicin AI antibiotic discovery Nature",
        "machine learning antibiotic resistance prediction",
        "deep learning drug discovery antibiotics"
    ],
    source_policy={"allow_domains": ["nature.com", "science.org", "cell.com", "pnas.org"]},
)
```

**When to use:** Writing Significance, Innovation, or Background sections for NIH, NSF, or other grant proposals.

---

## Combining with Other Skills

### With `research-lookup` (Academic Papers)

```python
# Use parallel-web for general research
researcher.research("Current state of quantum computing applications")

# Use research-lookup for academic paper search (auto-routes to Perplexity)
# python research_lookup.py "find papers on quantum error correction in Nature and Science"
```

### With `citation-management` (BibTeX)

```python
# Step 1: Find paper with parallel search
result = searcher.search(objective="Vaswani et al Attention Is All You Need paper")

# Step 2: Get DOI from results
doi = "10.48550/arXiv.1706.03762"

# Step 3: Convert to BibTeX with citation-management skill
# python scripts/doi_to_bibtex.py 10.48550/arXiv.1706.03762
```

### With `scientific-schematics` (Diagrams)

```python
# Step 1: Research a process
result = researcher.research("How does the CRISPR-Cas9 gene editing mechanism work step by step")

# Step 2: Use the research to inform a schematic
# python scripts/generate_schematic.py "CRISPR-Cas9 gene editing workflow: guide RNA design -> Cas9 binding -> DNA cleavage -> repair pathway" -o figures/crispr_mechanism.png
```

---

## Performance Cheat Sheet

| Task | Processor | Expected Time | Approximate Cost |
|------|-----------|---------------|------------------|
| Quick fact lookup | `base-fast` | 15-50s | $0.01 |
| Section background | `pro-fast` | 30s-5min | $0.10 |
| Comprehensive report | `ultra-fast` | 1-10min | $0.30 |
| Web search (10 results) | Search API | 1-3s | $0.005 |
| URL extraction (1 URL) | Extract API | 1-20s | $0.001 |
| URL extraction (5 URLs) | Extract API | 5-30s | $0.005 |

---

## See Also

- [API Reference](api_reference.md) - Complete API parameter reference
- [Search Best Practices](search_best_practices.md) - Effective search queries
- [Deep Research Guide](deep_research_guide.md) - Processor selection and output formats
- [Extraction Patterns](extraction_patterns.md) - URL content extraction
