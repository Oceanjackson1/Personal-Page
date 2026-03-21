---
title: "Perplexity Search"
description: "Perform AI-powered web searches with real-time information using Perplexity models via LiteLLM and OpenRouter. This skill should be used when conducting web searches for current information, finding recent scientific literature, getting grounded a..."
category: "research"
source: "community"
author: "Community"
tags: ["perplexity", "search"]
date: 2026-03-20
---

# Perplexity Search

## Overview

Perform AI-powered web searches using Perplexity models through LiteLLM and OpenRouter. Perplexity provides real-time, web-grounded answers with source citations, making it ideal for finding current information, recent scientific literature, and facts beyond the model's training data cutoff.

This skill provides access to all Perplexity models through OpenRouter, requiring only a single API key (no separate Perplexity account needed).

## When to Use This Skill

Use this skill when:
- Searching for current information or recent developments (2024 and beyond)
- Finding latest scientific publications and research
- Getting real-time answers grounded in web sources
- Verifying facts with source citations
- Conducting literature searches across multiple domains
- Accessing information beyond the model's knowledge cutoff
- Performing domain-specific research (biomedical, technical, clinical)
- Comparing current approaches or technologies

**Do not use** for:
- Simple calculations or logic problems (use directly)
- Tasks requiring code execution (use standard tools)
- Questions well within the model's training data (unless verification needed)

## Quick Start

### Setup (One-time)

1. **Get OpenRouter API key**:
   - Visit https://openrouter.ai/keys
   - Create account and generate API key
   - Add credits to account (minimum $5 recommended)

2. **Configure environment**:
   ```bash
   # Set API key
   export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

   # Or use setup script
   python scripts/setup_env.py --api-key sk-or-v1-your-key-here
   ```

3. **Install dependencies**:
   ```bash
   uv pip install litellm
   ```

4. **Verify setup**:
   ```bash
   python scripts/perplexity_search.py --check-setup
   ```

See `references/openrouter_setup.md` for detailed setup instructions, troubleshooting, and security best practices.

### Basic Usage

**Simple search:**
```bash
python scripts/perplexity_search.py "What are the latest developments in CRISPR gene editing?"
```

**Save results:**
```bash
python scripts/perplexity_search.py "Recent CAR-T therapy clinical trials" --output results.json
```

**Use specific model:**
```bash
python scripts/perplexity_search.py "Compare mRNA and viral vector vaccines" --model sonar-pro-search
```

**Verbose output:**
```bash
python scripts/perplexity_search.py "Quantum computing for drug discovery" --verbose
```

## Available Models

Access models via `--model` parameter:

- **sonar-pro** (default): General-purpose search, best balance of cost and quality
- **sonar-pro-search**: Most advanced agentic search with multi-step reasoning
- **sonar**: Basic model, most cost-effective for simple queries
- **sonar-reasoning-pro**: Advanced reasoning with step-by-step analysis
- **sonar-reasoning**: Basic reasoning capabilities

**Model selection guide:**
- Default queries → `sonar-pro`
- Complex multi-step analysis → `sonar-pro-search`
- Explicit reasoning needed → `sonar-reasoning-pro`
- Simple fact lookups → `sonar`
- Cost-sensitive bulk queries → `sonar`

See `references/model_comparison.md` for detailed comparison, use cases, pricing, and performance characteristics.

## Crafting Effective Queries

### Be Specific and Detailed

**Good examples:**
- "What are the latest clinical trial results for CAR-T cell therapy in treating B-cell lymphoma published in 2024?"
- "Compare the efficacy and safety profiles of mRNA vaccines versus viral vector vaccines for COVID-19"
- "Explain AlphaFold3 improvements over AlphaFold2 with specific accuracy metrics from 2023-2024 research"

**Bad examples:**
- "Tell me about cancer treatment" (too broad)
- "CRISPR" (too vague)
- "vaccines" (lacks specificity)

### Include Time Constraints

Perplexity searches real-time web data:
- "What papers were published in Nature Medicine in 2024 about long COVID?"
- "What are the latest developments (past 6 months) in large language model efficiency?"
- "What was announced at NeurIPS 2023 regarding AI safety?"

### Specify Domain and Sources

For high-quality results, mention source preferences:
- "According to peer-reviewed publications in high-impact journals..."
- "Based on FDA-approved treatments..."
- "From clinical trial registries like clinicaltrials.gov..."

### Structure Complex Queries

Break complex questions into clear components:
1. **Topic**: Main subject
2. **Scope**: Specific aspect of interest
3. **Context**: Time frame, domain, constraints
4. **Output**: Desired format or type of answer

**Example:**
"What improvements does AlphaFold3 offer over AlphaFold2 for protein structure prediction, according to research published between 2023 and 2024? Include specific accuracy metrics and benchmarks."

See `references/search_strategies.md` for comprehensive guidance on query design, domain-specific patterns, and advanced techniques.

## Common Use Cases

### Scientific Literature Search

```bash
python scripts/perplexity_search.py \
  "What does recent research (2023-2024) say about the role of gut microbiome in Parkinson's disease? Focus on peer-reviewed studies and include specific bacterial species identified." \
  --model sonar-pro
```

### Technical Documentation

```bash
python scripts/perplexity_search.py \
  "How to implement real-time data streaming from Kafka to PostgreSQL using Python? Include considerations for handling backpressure and ensuring exactly-once semantics." \
  --model sonar-reasoning-pro
```

### Comparative Analysis

```bash
python scripts/perplexity_search.py \
  "Compare PyTorch versus TensorFlow for implementing transformer models in terms of ease of use, performance, and ecosystem support. Include benchmarks from recent studies." \
  --model sonar-pro-search
```

### Clinical Research

```bash
python scripts/perplexity_search.py \
  "What is the evidence for intermittent fasting in managing type 2 diabetes in adults? Focus on randomized controlled trials and report HbA1c changes and weight loss outcomes." \
  --model sonar-pro
```

### Trend Analysis

```bash
python scripts/perplexity_search.py \
  "What are the key trends in single-cell RNA sequencing technology over the past 5 years? Highlight improvements in throughput, cost, and resolution, with specific examples." \
  --model sonar-pro
```

## Working with Results

### Programmatic Access

Use `perplexity_search.py` as a module:

```python
from scripts.perplexity_search import search_with_perplexity

result = search_with_perplexity(
    query="What are the latest CRISPR developments?",
    model="openrouter/perplexity/sonar-pro",
    max_tokens=4000,
    temperature=0.2,
    verbose=False
)

if result["success"]:
    print(result["answer"])
    print(f"Tokens used: {result['usage']['total_tokens']}")
else:
    print(f"Error: {result['error']}")
```

### Save and Process Results

```bash
# Save to JSON
python scripts/perplexity_search.py "query" --output results.json

# Process with jq
cat results.json | jq '.answer'
cat results.json | jq '.usage'
```

### Batch Processing

Create a script for multiple queries:

```bash
#!/bin/bash
queries=(
  "CRISPR developments 2024"
  "mRNA vaccine technology advances"
  "AlphaFold3 accuracy improvements"
)

for query in "${queries[@]}"; do
  echo "Searching: $query"
  python scripts/perplexity_search.py "$query" --output "results_$(echo $query | tr ' ' '_').json"
  sleep 2  # Rate limiting
done
```

## Cost Management

Perplexity models have different pricing tiers:

**Approximate costs per query:**
- Sonar: $0.001-0.002 (most cost-effective)
- Sonar Pro: $0.002-0.005 (recommended default)
- Sonar Reasoning Pro: $0.005-0.010
- Sonar Pro Search: $0.020-0.050+ (most comprehensive)

**Cost optimization strategies:**
1. Use `sonar` for simple fact lookups
2. Default to `sonar-pro` for most queries
3. Reserve `sonar-pro-search` for complex analysis
4. Set `--max-tokens` to limit response length
5. Monitor usage at https://openrouter.ai/activity
6. Set spending limits in OpenRouter dashboard

## Troubleshooting

### API Key Not Set

**Error**: "OpenRouter API key not configured"

**Solution**:
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
# Or run setup script
python scripts/setup_env.py --api-key sk-or-v1-your-key-here
```

### LiteLLM Not Installed

**Error**: "LiteLLM not installed"

**Solution**:
```bash
uv pip install litellm
```

### Rate Limiting

**Error**: "Rate limit exceeded"

**Solutions**:
- Wait a few seconds before retrying
- Increase rate limit at https://openrouter.ai/keys
- Add delays between requests in batch processing

### Insufficient Credits

**Error**: "Insufficient credits"

**Solution**:
- Add credits at https://openrouter.ai/account
- Enable auto-recharge to prevent interruptions

See `references/openrouter_setup.md` for comprehensive troubleshooting guide.

## Integration with Other Skills

This skill complements other scientific skills:

### Literature Review

Use with `literature-review` skill:
1. Use Perplexity to find recent papers and preprints
2. Supplement PubMed searches with real-time web results
3. Verify citations and find related work
4. Discover latest developments post-database indexing

### Scientific Writing

Use with `scientific-writing` skill:
1. Find recent references for introduction/discussion
2. Verify current state of the art
3. Check latest terminology and conventions
4. Identify recent competing approaches

### Hypothesis Generation

Use with `hypothesis-generation` skill:
1. Search for latest research findings
2. Identify current gaps in knowledge
3. Find recent methodological advances
4. Discover emerging research directions

### Critical Thinking

Use with `scientific-critical-thinking` skill:
1. Find evidence for and against hypotheses
2. Locate methodological critiques
3. Identify controversies in the field
4. Verify claims with current evidence

## Best Practices

### Query Design

1. **Be specific**: Include domain, time frame, and constraints
2. **Use terminology**: Domain-appropriate keywords and phrases
3. **Specify sources**: Mention preferred publication types or journals
4. **Structure questions**: Clear components with explicit context
5. **Iterate**: Refine based on initial results

### Model Selection

1. **Start with sonar-pro**: Good default for most queries
2. **Upgrade for complexity**: Use sonar-pro-search for multi-step analysis
3. **Downgrade for simplicity**: Use sonar for basic facts
4. **Use reasoning models**: When step-by-step analysis needed

### Cost Optimization

1. **Choose appropriate models**: Match model to query complexity
2. **Set token limits**: Use `--max-tokens` to control costs
3. **Monitor usage**: Check OpenRouter dashboard regularly
4. **Batch efficiently**: Combine related simple queries when possible
5. **Cache results**: Save and reuse results for repeated queries

### Security

1. **Protect API keys**: Never commit to version control
2. **Use environment variables**: Keep keys separate from code
3. **Set spending limits**: Configure in OpenRouter dashboard
4. **Monitor usage**: Watch for unexpected activity
5. **Rotate keys**: Change keys periodically

## Resources

### Bundled Resources

**Scripts:**
- `scripts/perplexity_search.py`: Main search script with CLI interface
- `scripts/setup_env.py`: Environment setup and validation helper

**References:**
- `references/search_strategies.md`: Comprehensive query design guide
- `references/model_comparison.md`: Detailed model comparison and selection guide
- `references/openrouter_setup.md`: Complete setup, troubleshooting, and security guide

**Assets:**
- `assets/.env.example`: Example environment file template

### External Resources

**OpenRouter:**
- Dashboard: https://openrouter.ai/account
- API Keys: https://openrouter.ai/keys
- Perplexity Models: https://openrouter.ai/perplexity
- Usage Monitoring: https://openrouter.ai/activity
- Documentation: https://openrouter.ai/docs

**LiteLLM:**
- Documentation: https://docs.litellm.ai/
- OpenRouter Provider: https://docs.litellm.ai/docs/providers/openrouter
- GitHub: https://github.com/BerriAI/litellm

**Perplexity:**
- Official Docs: https://docs.perplexity.ai/

## Dependencies

### Required

```bash
# LiteLLM for API access
uv pip install litellm
```

### Optional

```bash
# For .env file support
uv pip install python-dotenv

# For JSON processing (usually pre-installed)
uv pip install jq
```

### Environment Variables

Required:
- `OPENROUTER_API_KEY`: Your OpenRouter API key

Optional:
- `DEFAULT_MODEL`: Default model to use (default: sonar-pro)
- `DEFAULT_MAX_TOKENS`: Default max tokens (default: 4000)
- `DEFAULT_TEMPERATURE`: Default temperature (default: 0.2)

## Summary

This skill provides:

1. **Real-time web search**: Access current information beyond training data cutoff
2. **Multiple models**: From cost-effective Sonar to advanced Sonar Pro Search
3. **Simple setup**: Single OpenRouter API key, no separate Perplexity account
4. **Comprehensive guidance**: Detailed references for query design and model selection
5. **Cost-effective**: Pay-as-you-go pricing with usage monitoring
6. **Scientific focus**: Optimized for research, literature search, and technical queries
7. **Easy integration**: Works seamlessly with other scientific skills

Conduct AI-powered web searches to find current information, recent research, and grounded answers with source citations.

---

## Reference: Model_Comparison

# Perplexity Model Comparison

Guide to different Perplexity models available through OpenRouter and when to use each.

## Available Models

All Perplexity models are accessed through OpenRouter using the format:
`openrouter/perplexity/[model-name]`

### Sonar Pro Search

**Model ID**: `openrouter/perplexity/sonar-pro-search`

**Best for:**
- Complex multi-step research questions
- Queries requiring deep analysis and synthesis
- Situations needing comprehensive source exploration
- Comparative analyses across multiple domains
- Research requiring agentic reasoning workflow

**Characteristics:**
- Most advanced agentic search system
- Executes multi-step reasoning workflows
- Uses tools and intermediate queries
- Provides most comprehensive answers
- Higher cost due to extensive processing

**Use cases:**
- "Conduct a comprehensive analysis of competing CAR-T cell therapy approaches, including mechanism differences, clinical outcomes, and cost-effectiveness"
- "Compare quantum computing approaches for drug discovery with traditional computational methods across multiple metrics"
- Research questions requiring synthesis from many sources

**Pricing** (approximate):
- Input: $3/million tokens
- Output: $15/million tokens
- Request fee: $18 per 1000 requests

**Context window**: 200K tokens

### Sonar Pro

**Model ID**: `openrouter/perplexity/sonar-pro`

**Best for:**
- General-purpose research and search
- Balanced performance and cost
- Standard scientific queries
- Quick information gathering
- Most use cases

**Characteristics:**
- Enhanced capabilities over base Sonar
- Good balance of quality and cost
- Reliable for most queries
- Faster than Pro Search
- Recommended default choice

**Use cases:**
- "What are the latest developments in CRISPR base editing?"
- "Summarize recent clinical trials for Alzheimer's treatment"
- "Explain how transformer architectures work in modern LLMs"
- Standard literature searches
- Technical documentation queries

**Pricing** (approximate):
- Lower cost than Pro Search
- Good cost-performance ratio

**Context window**: 200K tokens

### Sonar

**Model ID**: `openrouter/perplexity/sonar`

**Best for:**
- Basic searches and queries
- Cost-sensitive applications
- Simple fact-finding
- High-volume queries
- Quick lookups

**Characteristics:**
- Base model with solid performance
- Most cost-effective option
- Faster response times
- Good for straightforward queries
- Lower accuracy than Pro variants

**Use cases:**
- "What is the molecular weight of aspirin?"
- "When was CRISPR-Cas9 first used in humans?"
- "List the main symptoms of diabetes"
- Simple fact verification
- Basic information retrieval

**Pricing** (approximate):
- Lowest cost option
- Best for high-volume simple queries

**Context window**: 200K tokens

### Sonar Reasoning Pro

**Model ID**: `openrouter/perplexity/sonar-reasoning-pro`

**Best for:**
- Complex logical reasoning tasks
- Multi-step problem solving
- Technical analysis requiring step-by-step thinking
- Mathematical or computational problems
- Queries needing explicit reasoning chains

**Characteristics:**
- Advanced reasoning capabilities
- Shows step-by-step thinking
- Better for analytical tasks
- Excels at technical problem-solving
- More structured outputs

**Use cases:**
- "Walk through the steps to design a clinical trial for testing a novel cancer therapy"
- "Analyze the computational complexity of different protein folding algorithms"
- "Reason through the molecular mechanisms linking multiple genes to a disease phenotype"
- Technical troubleshooting with multiple steps
- Logical analysis of complex systems

**Pricing** (approximate):
- Higher cost due to reasoning capabilities
- Worth it for complex analytical tasks

**Context window**: 200K tokens

### Sonar Reasoning

**Model ID**: `openrouter/perplexity/sonar-reasoning`

**Best for:**
- Basic reasoning tasks
- Cost-effective analytical queries
- Simpler logical problems
- Step-by-step explanations

**Characteristics:**
- Basic reasoning capabilities
- More affordable than Reasoning Pro
- Good for moderate complexity tasks
- Shows logical thinking process

**Use cases:**
- "Explain the logic behind vaccine efficacy calculations"
- "Walk through basic statistical analysis steps"
- Simple analytical questions
- Educational explanations

**Pricing** (approximate):
- Lower cost than Reasoning Pro
- Good balance for basic reasoning

**Context window**: 200K tokens

## Model Selection Guide

### Decision Tree

```
Is your query complex and requiring deep multi-step analysis?
├─ YES → Use Sonar Pro Search
└─ NO → Continue

Does your query require explicit step-by-step reasoning?
├─ YES → Use Sonar Reasoning Pro (complex) or Sonar Reasoning (simple)
└─ NO → Continue

Is this a standard research or information query?
├─ YES → Use Sonar Pro (recommended default)
└─ NO → Continue

Is this a simple fact-finding or basic lookup?
├─ YES → Use Sonar (cost-effective)
└─ NO → Use Sonar Pro (safe default)
```

### By Use Case

| Use Case | Recommended Model | Alternative |
|----------|------------------|-------------|
| Literature review | Sonar Pro | Sonar Pro Search |
| Quick fact check | Sonar | Sonar Pro |
| Complex analysis | Sonar Pro Search | Sonar Reasoning Pro |
| Step-by-step tutorial | Sonar Reasoning Pro | Sonar Pro |
| Cost-sensitive bulk queries | Sonar | Sonar Pro |
| General research | Sonar Pro | Sonar |
| Technical debugging | Sonar Reasoning Pro | Sonar Pro |
| Comparative analysis | Sonar Pro Search | Sonar Pro |

### By Domain

**Biomedical Research:**
- Default: Sonar Pro
- Complex mechanisms: Sonar Reasoning Pro
- Literature synthesis: Sonar Pro Search
- Quick lookups: Sonar

**Computational Science:**
- Default: Sonar Pro
- Algorithm analysis: Sonar Reasoning Pro
- Technical docs: Sonar Pro
- Basic syntax: Sonar

**Drug Discovery:**
- Default: Sonar Pro
- Multi-target analysis: Sonar Pro Search
- Mechanism reasoning: Sonar Reasoning Pro
- Compound properties: Sonar

**Clinical Research:**
- Default: Sonar Pro
- Trial design: Sonar Reasoning Pro
- Evidence synthesis: Sonar Pro Search
- Basic guidelines: Sonar

## Performance Characteristics

### Response Time

**Fastest to Slowest:**
1. Sonar (fastest)
2. Sonar Pro
3. Sonar Reasoning
4. Sonar Reasoning Pro
5. Sonar Pro Search (slowest, due to multi-step processing)

**Considerations:**
- For time-sensitive queries, use Sonar or Sonar Pro
- For comprehensive analysis, accept the slower Sonar Pro Search
- Reasoning models are slower due to explicit thinking steps

### Quality vs Cost Trade-offs

**Quality Hierarchy** (highest to lowest):
1. Sonar Pro Search
2. Sonar Reasoning Pro
3. Sonar Pro
4. Sonar Reasoning
5. Sonar

**Cost Hierarchy** (most to least expensive):
1. Sonar Pro Search
2. Sonar Reasoning Pro
3. Sonar Pro
4. Sonar Reasoning
5. Sonar

**Recommendation**: Start with Sonar Pro as the default. Upgrade to Pro Search for complex queries, downgrade to Sonar for simple lookups.

### Accuracy and Comprehensiveness

**Most Comprehensive:**
- Sonar Pro Search: Explores multiple sources, synthesizes deeply
- Sonar Reasoning Pro: Thorough step-by-step analysis

**Most Accurate:**
- Sonar Pro Search: Best source verification and cross-checking
- Sonar Pro: Reliable for most queries

**Good Enough:**
- Sonar: Adequate for simple facts and basic queries

## Special Considerations

### Context Window

All models support 200K token context windows:
- Sufficient for most queries
- Can handle long documents or multiple sources
- Consider chunking very large analyses

### Temperature Settings

Different models benefit from different temperature settings:

**Sonar Pro Search:**
- Default: 0.2 (more focused, analytical)
- Use lower (0.0-0.1) for factual queries
- Use higher (0.3-0.5) for creative synthesis

**Sonar Reasoning Pro:**
- Default: 0.2
- Keep low (0.0-0.2) for logical consistency
- Reasoning quality degrades at high temperatures

**Sonar Pro / Sonar:**
- Default: 0.2
- Adjust based on query type (factual vs exploratory)

### Rate Limits and Quotas

OpenRouter enforces rate limits:
- Check your OpenRouter dashboard for current limits
- Consider request batching for high-volume use
- Monitor costs with OpenRouter's tracking tools

### API Key Security

**Best practices:**
- Never commit API keys to version control
- Use environment variables or .env files
- Rotate keys periodically
- Monitor usage for unexpected activity
- Use separate keys for different projects

## Example Comparisons

### Query: "Explain CRISPR-Cas9 gene editing"

**Sonar:**
- Quick overview
- Basic mechanism explanation
- ~200-300 tokens
- 1-2 sources cited
- Cost: $0.001

**Sonar Pro:**
- Detailed explanation
- Multiple mechanisms covered
- ~500-800 tokens
- 3-5 sources cited
- Cost: $0.003

**Sonar Reasoning Pro:**
- Step-by-step mechanism breakdown
- Logical flow of editing process
- ~800-1200 tokens
- Shows reasoning steps
- Cost: $0.005

**Sonar Pro Search:**
- Comprehensive analysis
- Multiple sources synthesized
- Historical context included
- Recent developments covered
- ~1500-2000 tokens
- 10+ sources explored
- Cost: $0.020+

### Query: "What is 2+2?"

All models return accurate answer. Use Sonar for simple queries to minimize cost.

### Query: "Design a clinical trial for novel immunotherapy"

**Sonar:**
- Basic template provided
- May miss important details
- Cost-effective but incomplete

**Sonar Pro:**
- Solid trial design framework
- Covers main components
- Good starting point

**Sonar Reasoning Pro:**
- Detailed step-by-step design
- Considers multiple factors
- Shows reasoning for each choice
- **Recommended for this query type**

**Sonar Pro Search:**
- Most comprehensive design
- Incorporates best practices from multiple sources
- Compares different approaches
- May be overkill for initial design

## Summary

**Default recommendation**: Start with **Sonar Pro** for most scientific queries.

**When to upgrade:**
- Complex multi-step analysis → Sonar Pro Search
- Explicit reasoning needed → Sonar Reasoning Pro

**When to downgrade:**
- Simple facts or lookups → Sonar
- Cost-sensitive bulk queries → Sonar

**Remember**: The best model depends on your specific use case, budget, and quality requirements. Monitor your usage and adjust model selection based on results.

---

## Reference: Openrouter_Setup

# OpenRouter Setup Guide

Complete guide to setting up and using OpenRouter for Perplexity model access.

## What is OpenRouter?

OpenRouter is a unified API gateway that provides access to 100+ AI models from various providers through a single API interface. It offers:

- **Single API key**: Access multiple models with one key
- **Unified format**: OpenAI-compatible API format
- **Cost tracking**: Built-in usage monitoring and billing
- **Model routing**: Intelligent fallback and load balancing
- **Pay-as-you-go**: No subscriptions, pay only for what you use

For Perplexity models specifically, OpenRouter provides exclusive access to certain models like Sonar Pro Search.

## Getting Started

### Step 1: Create OpenRouter Account

1. Visit https://openrouter.ai/
2. Click "Sign Up" in the top right
3. Sign up with Google, GitHub, or email
4. Verify your email if using email signup

### Step 2: Add Payment Method

OpenRouter uses pay-as-you-go billing:

1. Navigate to https://openrouter.ai/account
2. Click "Credits" tab
3. Add a payment method (credit card)
4. Add initial credits (minimum $5 recommended)
5. Optionally set up auto-recharge

**Pricing notes:**
- Models have different per-token costs
- See https://openrouter.ai/perplexity for Perplexity pricing
- Monitor usage at https://openrouter.ai/activity

### Step 3: Generate API Key

1. Go to https://openrouter.ai/keys
2. Click "Create Key"
3. Give your key a descriptive name (e.g., "perplexity-search-skill")
4. Optionally set usage limits for safety
5. Copy the key (starts with `sk-or-v1-...`)
6. **Important**: Save this key securely - you can't view it again!

**Security tips:**
- Never share your API key publicly
- Don't commit keys to version control
- Use separate keys for different projects
- Set usage limits to prevent unexpected charges
- Rotate keys periodically

### Step 4: Configure Environment

You have two options for setting up your API key:

#### Option A: Environment Variable (Recommended)

**Linux/macOS:**
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
```

To make it permanent, add to your shell profile:
```bash
# For bash: Add to ~/.bashrc or ~/.bash_profile
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# For zsh: Add to ~/.zshrc
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

To make it permanent:
```powershell
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-your-key-here', 'User')
```

#### Option B: .env File

Create a `.env` file in your project directory:

```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=sk-or-v1-your-key-here
EOF
```

Or use the setup script:
```bash
python scripts/setup_env.py --api-key sk-or-v1-your-key-here
```

Then load it before running scripts:
```bash
# Load environment variables from .env
source .env

# Or use python-dotenv
pip install python-dotenv
```

**Using python-dotenv in scripts:**
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file automatically

import os
api_key = os.environ.get("OPENROUTER_API_KEY")
```

### Step 5: Install Dependencies

Install LiteLLM using uv:

```bash
uv pip install litellm
```

Or with regular pip:
```bash
pip install litellm
```

**Optional dependencies:**
```bash
# For .env file support
uv pip install python-dotenv

# For additional features
uv pip install litellm[proxy]  # If using LiteLLM proxy server
```

### Step 6: Verify Setup

Test your configuration:

```bash
# Using the setup script
python scripts/setup_env.py --validate

# Or using the search script
python scripts/perplexity_search.py --check-setup
```

You should see:
```
✓ OPENROUTER_API_KEY is set (sk-or-v1-...xxxx)
✓ LiteLLM is installed (version X.X.X)
✓ Setup is complete! You're ready to use Perplexity Search.
```

### Step 7: Test Your First Search

Run a simple test query:

```bash
python scripts/perplexity_search.py "What is CRISPR gene editing?"
```

Expected output:
```
================================================================================
ANSWER
================================================================================
CRISPR (Clustered Regularly Interspaced Short Palindromic Repeats) is a
revolutionary gene editing technology that allows precise modifications to DNA...
[detailed answer continues]
================================================================================
```

## Usage Monitoring

### Check Your Usage

Monitor your OpenRouter usage and costs:

1. Visit https://openrouter.ai/activity
2. View requests, tokens, and costs
3. Filter by date range, model, or key
4. Export usage data for analysis

### Set Usage Limits

Protect against unexpected charges:

1. Go to https://openrouter.ai/keys
2. Click on your key
3. Set "Rate limit" (requests per minute)
4. Set "Spending limit" (maximum total spend)
5. Enable "Auto-recharge" with limit if desired

**Recommended limits for development:**
- Rate limit: 10-20 requests per minute
- Spending limit: $10-50 depending on usage

### Cost Optimization

Tips for reducing costs:

1. **Choose appropriate models**: Use Sonar for simple queries, not Sonar Pro Search
2. **Set max_tokens**: Limit response length with `--max-tokens` parameter
3. **Batch queries**: Combine multiple simple questions when possible
4. **Monitor usage**: Check costs daily during heavy development
5. **Use caching**: Store results for repeated queries

## Troubleshooting

### Error: "OpenRouter API key not configured"

**Cause**: Environment variable not set

**Solution**:
```bash
# Check if variable is set
echo $OPENROUTER_API_KEY

# If empty, set it
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# Or use setup script
python scripts/setup_env.py --api-key sk-or-v1-your-key-here
```

### Error: "Invalid API key"

**Causes**:
- Key was deleted or revoked
- Key has expired
- Typo in the key
- Wrong key format

**Solutions**:
1. Verify key at https://openrouter.ai/keys
2. Check for extra spaces or quotes
3. Generate a new key if needed
4. Ensure key starts with `sk-or-v1-`

### Error: "Insufficient credits"

**Cause**: OpenRouter account has run out of credits

**Solution**:
1. Go to https://openrouter.ai/account
2. Click "Credits" tab
3. Add more credits
4. Consider enabling auto-recharge

### Error: "Rate limit exceeded"

**Cause**: Too many requests in a short time

**Solutions**:
1. Wait a few seconds before retrying
2. Increase rate limit at https://openrouter.ai/keys
3. Implement exponential backoff in code
4. Batch requests or reduce frequency

### Error: "Model not found"

**Cause**: Incorrect model name or model no longer available

**Solution**:
1. Check available models at https://openrouter.ai/models
2. Use correct format: `openrouter/perplexity/sonar-pro`
3. Verify model is still supported

### Error: "LiteLLM not installed"

**Cause**: LiteLLM package is not installed

**Solution**:
```bash
uv pip install litellm
```

### Import Error with LiteLLM

**Cause**: Python path issues or version conflicts

**Solutions**:
1. Verify installation: `pip list | grep litellm`
2. Reinstall: `uv pip install --force-reinstall litellm`
3. Check Python version: `python --version` (requires 3.8+)
4. Use virtual environment to avoid conflicts

## Advanced Configuration

### Using Multiple Keys

For different projects or team members:

```bash
# Project 1
export OPENROUTER_API_KEY='sk-or-v1-project1-key'

# Project 2
export OPENROUTER_API_KEY='sk-or-v1-project2-key'
```

Or use .env files in different directories.

### Custom Base URL

If using OpenRouter proxy or custom endpoint:

```python
from litellm import completion

response = completion(
    model="openrouter/perplexity/sonar-pro",
    messages=[{"role": "user", "content": "query"}],
    api_base="https://custom-endpoint.com/v1"  # Custom URL
)
```

### Request Headers

Add custom headers for tracking:

```python
from litellm import completion

response = completion(
    model="openrouter/perplexity/sonar-pro",
    messages=[{"role": "user", "content": "query"}],
    extra_headers={
        "HTTP-Referer": "https://your-app.com",
        "X-Title": "Your App Name"
    }
)
```

### Timeout Configuration

Set custom timeouts for long-running queries:

```python
from litellm import completion

response = completion(
    model="openrouter/perplexity/sonar-pro-search",
    messages=[{"role": "user", "content": "complex query"}],
    timeout=120  # 120 seconds timeout
)
```

## Security Best Practices

### API Key Management

1. **Never commit keys**: Add `.env` to `.gitignore`
2. **Use key rotation**: Rotate keys every 3-6 months
3. **Separate keys**: Different keys for dev/staging/production
4. **Monitor usage**: Check for unauthorized access
5. **Set limits**: Configure spending and rate limits

### .gitignore Template

Add to your `.gitignore`:
```
# Environment variables
.env
.env.local
.env.*.local

# API keys
*api_key*
*apikey*
*.key

# Sensitive configs
config/secrets.yaml
```

### Key Revocation

If a key is compromised:

1. Go to https://openrouter.ai/keys immediately
2. Click "Delete" on the compromised key
3. Generate a new key
4. Update all applications using the old key
5. Review usage logs for unauthorized access
6. Contact OpenRouter support if needed

## FAQs

**Q: How much does it cost to use Perplexity via OpenRouter?**

A: Pricing varies by model. Sonar is cheapest (~$0.001-0.002 per query), Sonar Pro is moderate (~$0.002-0.005), and Sonar Pro Search is most expensive (~$0.02-0.05+ per query). See https://openrouter.ai/perplexity for exact pricing.

**Q: Do I need a separate Perplexity API key?**

A: No! OpenRouter provides access to Perplexity models using only your OpenRouter key.

**Q: Can I use OpenRouter for other models besides Perplexity?**

A: Yes! OpenRouter provides access to 100+ models from OpenAI, Anthropic, Google, Meta, and more through the same API key.

**Q: Is there a free tier?**

A: OpenRouter requires payment, but offers very competitive pricing. Initial $5 credit should last for extensive testing.

**Q: How do I cancel my OpenRouter account?**

A: Contact OpenRouter support. Note that unused credits may not be refundable.

**Q: Can I use OpenRouter in production applications?**

A: Yes, OpenRouter is designed for production use with robust infrastructure, SLAs, and enterprise support available.

## Resources

**Official Documentation:**
- OpenRouter: https://openrouter.ai/docs
- Perplexity Models: https://openrouter.ai/perplexity
- LiteLLM: https://docs.litellm.ai/

**Account Management:**
- Dashboard: https://openrouter.ai/account
- API Keys: https://openrouter.ai/keys
- Usage: https://openrouter.ai/activity
- Billing: https://openrouter.ai/credits

**Community:**
- OpenRouter Discord: https://discord.gg/openrouter
- GitHub Issues: https://github.com/OpenRouter
- LiteLLM GitHub: https://github.com/BerriAI/litellm

## Summary

Setting up OpenRouter for Perplexity access involves:

1. Create account at https://openrouter.ai
2. Add payment method and credits
3. Generate API key at https://openrouter.ai/keys
4. Set `OPENROUTER_API_KEY` environment variable
5. Install LiteLLM: `uv pip install litellm`
6. Verify setup: `python scripts/setup_env.py --validate`
7. Start searching: `python scripts/perplexity_search.py "your query"`

Monitor usage and costs regularly to optimize your spending and ensure security.

---

## Reference: Search_Strategies

# Search Strategies for Perplexity

Best practices and strategies for crafting effective search queries with Perplexity models.

## Query Design Principles

### Be Specific and Detailed

Better results come from specific, well-structured queries rather than broad questions.

**Good examples:**
- "What are the latest clinical trial results for CAR-T cell therapy in treating B-cell lymphoma published in 2024?"
- "Compare the efficacy and safety profiles of mRNA vaccines versus viral vector vaccines for COVID-19"
- "Explain the mechanism of CRISPR-Cas9 off-target effects and current mitigation strategies"

**Bad examples:**
- "Tell me about cancer treatment" (too broad)
- "CRISPR" (too vague)
- "vaccines" (lacks specificity)

### Structure Complex Queries

Break complex questions into clear components:

1. **Topic**: What is the main subject?
2. **Scope**: What specific aspect are you interested in?
3. **Context**: What time frame, domain, or constraints apply?
4. **Output**: What format or type of answer do you need?

**Example:**
```
Topic: Protein folding prediction
Scope: AlphaFold3 improvements over AlphaFold2
Context: Published research from 2023-2024
Output: Technical comparison with specific accuracy metrics
```

**Query:**
"What improvements does AlphaFold3 offer over AlphaFold2 for protein structure prediction, according to research published between 2023 and 2024? Include specific accuracy metrics and benchmarks."

## Domain-Specific Search Patterns

### Scientific Literature Search

For scientific queries, include:
- Specific terminology and concepts
- Time constraints (recent publications)
- Methodology or study types of interest
- Journal quality or domain constraints

**Template:**
"What does recent research (2023-2024) say about [specific scientific concept] in [domain]? Focus on [peer-reviewed/preprint] studies and include [specific metrics/findings]."

**Example:**
"What does recent research (2023-2024) say about the role of gut microbiome in Parkinson's disease? Focus on peer-reviewed studies and include specific bacterial species identified."

### Technical/Engineering Search

For technical queries, specify:
- Technology stack or framework
- Use case or application context
- Version requirements
- Performance or implementation constraints

**Template:**
"How to [specific technical task] using [technology/framework] for [use case]? Include [implementation details/performance considerations]."

**Example:**
"How to implement real-time data streaming from Kafka to PostgreSQL using Python? Include considerations for handling backpressure and ensuring exactly-once semantics."

### Medical/Clinical Search

For medical queries, include:
- Specific conditions, treatments, or interventions
- Patient population or demographics
- Outcomes of interest
- Evidence level (RCTs, meta-analyses, etc.)

**Template:**
"What is the evidence for [intervention] in treating [condition] in [population]? Focus on [study types] and report [specific outcomes]."

**Example:**
"What is the evidence for intermittent fasting in managing type 2 diabetes in adults? Focus on randomized controlled trials and report HbA1c changes and weight loss outcomes."

## Advanced Query Techniques

### Comparative Analysis

For comparing multiple options:

**Template:**
"Compare [option A] versus [option B] for [use case] in terms of [criteria 1], [criteria 2], and [criteria 3]. Include [specific evidence or metrics]."

**Example:**
"Compare PyTorch versus TensorFlow for implementing transformer models in terms of ease of use, performance, and ecosystem support. Include benchmarks from recent studies."

### Trend Analysis

For understanding trends over time:

**Template:**
"What are the key trends in [domain/topic] over the past [time period]? Highlight [specific aspects] and include [data or examples]."

**Example:**
"What are the key trends in single-cell RNA sequencing technology over the past 5 years? Highlight improvements in throughput, cost, and resolution, with specific examples."

### Gap Identification

For finding research or knowledge gaps:

**Template:**
"What are the current limitations and open questions in [field/topic]? Focus on [specific aspects] and identify areas needing further research."

**Example:**
"What are the current limitations and open questions in quantum error correction? Focus on practical implementations and identify scalability challenges."

### Mechanism Explanation

For understanding how things work:

**Template:**
"Explain the mechanism by which [process/phenomenon] occurs in [context]. Include [level of detail] and discuss [specific aspects]."

**Example:**
"Explain the mechanism by which mRNA vaccines induce immune responses. Include molecular details of translation, antigen presentation, and memory cell formation."

## Query Refinement Strategies

### Start Broad, Then Narrow

1. **Initial query**: "Recent developments in cancer immunotherapy"
2. **Refined query**: "Recent developments in checkpoint inhibitor combination therapies for melanoma"
3. **Specific query**: "What are the clinical trial results for combining anti-PD-1 and anti-CTLA-4 checkpoint inhibitors in metastatic melanoma patients, published 2023-2024?"

### Add Constraints Iteratively

Start with core query, then add constraints:

1. **Base**: "Machine learning for drug discovery"
2. **Add domain**: "Machine learning for small molecule drug discovery"
3. **Add method**: "Deep learning approaches for small molecule property prediction"
4. **Add context**: "Recent deep learning approaches (2023-2024) for predicting ADMET properties of small molecules, including accuracy benchmarks"

### Specify Desired Output Format

Improve answers by specifying the output format:

- "Provide a step-by-step explanation..."
- "Summarize in bullet points..."
- "Create a comparison table of..."
- "List the top 5 approaches with pros and cons..."
- "Include specific numerical benchmarks and metrics..."

## Common Pitfalls to Avoid

### Too Vague

**Problem**: "Tell me about AI"
**Solution**: "What are the current state-of-the-art approaches for few-shot learning in computer vision as of 2024?"

### Loaded Questions

**Problem**: "Why is drug X better than drug Y?"
**Solution**: "Compare the efficacy and safety profiles of drug X versus drug Y based on clinical trial evidence."

### Multiple Unrelated Questions

**Problem**: "What is CRISPR and how do vaccines work and what causes cancer?"
**Solution**: Ask separate queries for each topic.

### Assumed Knowledge Without Context

**Problem**: "What are the latest results?" (Latest results for what?)
**Solution**: "What are the latest clinical trial results for CAR-T cell therapy in treating acute lymphoblastic leukemia?"

## Domain-Specific Keywords

### Biomedical Research

Use precise terminology:
- "randomized controlled trial" instead of "study"
- "meta-analysis" instead of "review"
- "in vitro" vs "in vivo" vs "clinical"
- "peer-reviewed" for quality filter
- Specific gene/protein names (e.g., "BRCA1" not "breast cancer gene")

### Computational/AI Research

Use technical terms:
- "transformer architecture" not "AI model"
- "few-shot learning" not "learning from limited data"
- "zero-shot" vs "few-shot" vs "fine-tuning"
- Specific model names (e.g., "GPT-4" not "language model")

### Chemistry/Drug Discovery

Use IUPAC names and specific terms:
- "small molecule" vs "biologic"
- "pharmacokinetics" (ADME) vs "pharmacodynamics"
- Specific assay types (e.g., "IC50", "EC50")
- Drug names (generic vs brand)

## Time-Constrained Searches

Perplexity searches real-time web data, making time constraints valuable:

**Templates:**
- "What papers were published in [journal] in [month/year] about [topic]?"
- "What are the latest developments (past 6 months) in [field]?"
- "What was announced at [conference] [year] regarding [topic]?"
- "What are the most recent clinical trial results (2024) for [treatment]?"

**Examples:**
- "What papers were published in Nature Medicine in January 2024 about long COVID?"
- "What are the latest developments (past 6 months) in large language model training efficiency?"
- "What was announced at NeurIPS 2023 regarding AI safety and alignment?"

## Source Quality Considerations

For high-quality results, mention source preferences:

- "According to peer-reviewed publications..."
- "Based on clinical trial registries like clinicaltrials.gov..."
- "From authoritative sources such as Nature, Science, Cell..."
- "According to FDA/EMA approvals..."
- "Based on systematic reviews or meta-analyses..."

**Example:**
"What is the current understanding of microplastics' impact on human health according to peer-reviewed research published in high-impact journals since 2022?"

## Iterative Search Workflow

For comprehensive research:

1. **Broad overview**: Get general understanding
2. **Specific deep-dives**: Focus on particular aspects
3. **Comparative analysis**: Compare approaches/methods
4. **Latest updates**: Find most recent developments
5. **Critical evaluation**: Identify limitations and gaps

**Example workflow for "CAR-T cell therapy":**

1. "What is CAR-T cell therapy and how does it work?"
2. "What are the specific molecular mechanisms by which CAR-T cells recognize and kill cancer cells?"
3. "Compare first-generation, second-generation, and third-generation CAR-T cell designs"
4. "What are the latest clinical trial results for CAR-T therapy in treating solid tumors (2024)?"
5. "What are the current limitations and challenges in CAR-T cell therapy, and what approaches are being investigated to address them?"

## Summary

Effective Perplexity searches require:
1. **Specificity**: Clear, detailed queries
2. **Structure**: Well-organized questions with context
3. **Terminology**: Domain-appropriate keywords
4. **Constraints**: Time frames, sources, output formats
5. **Iteration**: Refine based on initial results

The more specific and structured your query, the better and more relevant your results will be.
