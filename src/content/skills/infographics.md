---
title: "Infographics"
description: "Create professional infographics using Nano Banana Pro AI with smart iterative refinement. Uses Gemini 3 Pro for quality review. Integrates research-lookup and web search for accurate data. Supports 10 infographic types, 8 industry styles, and col..."
category: "research"
source: "community"
author: "Community"
tags: ["infographics"]
date: 2026-03-20
---

# Infographics

## Overview

Infographics are visual representations of information, data, or knowledge designed to present complex content quickly and clearly. **This skill uses Nano Banana Pro AI for infographic generation with Gemini 3 Pro quality review and Perplexity Sonar for research.**

**How it works:**
- (Optional) **Research phase**: Gather accurate facts and statistics using Perplexity Sonar
- Describe your infographic in natural language
- Nano Banana Pro generates publication-quality infographics automatically
- **Gemini 3 Pro reviews quality** against document-type thresholds
- **Smart iteration**: Only regenerates if quality is below threshold
- Professional-ready output in minutes
- No design skills required

**Quality Thresholds by Document Type:**
| Document Type | Threshold | Description |
|---------------|-----------|-------------|
| marketing | 8.5/10 | Marketing materials - must be compelling |
| report | 8.0/10 | Business reports - professional quality |
| presentation | 7.5/10 | Slides, talks - clear and engaging |
| social | 7.0/10 | Social media content |
| internal | 7.0/10 | Internal use |
| draft | 6.5/10 | Working drafts |
| default | 7.5/10 | General purpose |

**Simply describe what you want, and Nano Banana Pro creates it.**

## Quick Start

Generate any infographic by simply describing it:

```bash
# Generate a list infographic (default threshold 7.5/10)
python skills/infographics/scripts/generate_infographic.py \
  "5 benefits of regular exercise" \
  -o figures/exercise_benefits.png --type list

# Generate for marketing (highest threshold: 8.5/10)
python skills/infographics/scripts/generate_infographic.py \
  "Product features comparison" \
  -o figures/product_comparison.png --type comparison --doc-type marketing

# Generate with corporate style
python skills/infographics/scripts/generate_infographic.py \
  "Company milestones 2010-2025" \
  -o figures/timeline.png --type timeline --style corporate

# Generate with colorblind-safe palette
python skills/infographics/scripts/generate_infographic.py \
  "Heart disease statistics worldwide" \
  -o figures/health_stats.png --type statistical --palette wong

# Generate WITH RESEARCH for accurate, up-to-date data
python skills/infographics/scripts/generate_infographic.py \
  "Global AI market size and growth projections" \
  -o figures/ai_market.png --type statistical --research
```

**What happens behind the scenes:**
1. **(Optional) Research**: Perplexity Sonar gathers accurate facts, statistics, and data
2. **Generation 1**: Nano Banana Pro creates initial infographic following design best practices
3. **Review 1**: **Gemini 3 Pro** evaluates quality against document-type threshold
4. **Decision**: If quality >= threshold → **DONE** (no more iterations needed!)
5. **If below threshold**: Improved prompt based on critique, regenerate
6. **Repeat**: Until quality meets threshold OR max iterations reached

**Smart Iteration Benefits:**
- ✅ Saves API calls if first generation is good enough
- ✅ Higher quality standards for marketing materials
- ✅ Faster turnaround for drafts/internal use
- ✅ Appropriate quality for each use case

**Output**: Versioned images plus a detailed review log with quality scores, critiques, and early-stop information.

## When to Use This Skill

Use the **infographics** skill when:
- Presenting data or statistics in a visual format
- Creating timeline visualizations for project milestones or history
- Explaining processes, workflows, or step-by-step guides
- Comparing options, products, or concepts side-by-side
- Summarizing key points in an engaging visual format
- Creating geographic or map-based data visualizations
- Building hierarchical or organizational charts
- Designing social media content or marketing materials

**Use scientific-schematics instead for:**
- Technical flowcharts and circuit diagrams
- Biological pathways and molecular diagrams
- Neural network architecture diagrams
- CONSORT/PRISMA methodology diagrams

---

## Research Integration

### Automatic Data Gathering (`--research`)

When creating infographics that require accurate, up-to-date data, use the `--research` flag to automatically gather facts and statistics using **Perplexity Sonar Pro**.

```bash
# Research and generate statistical infographic
python skills/infographics/scripts/generate_infographic.py \
  "Global renewable energy adoption rates by country" \
  -o figures/renewable_energy.png --type statistical --research

# Research for timeline infographic
python skills/infographics/scripts/generate_infographic.py \
  "History of artificial intelligence breakthroughs" \
  -o figures/ai_history.png --type timeline --research

# Research for comparison infographic
python skills/infographics/scripts/generate_infographic.py \
  "Electric vehicles vs hydrogen vehicles comparison" \
  -o figures/ev_hydrogen.png --type comparison --research
```

### What Research Provides

The research phase automatically:

1. **Gathers Key Facts**: 5-8 relevant facts and statistics about the topic
2. **Provides Context**: Background information for accurate representation
3. **Finds Data Points**: Specific numbers, percentages, and dates
4. **Cites Sources**: Mentions major studies or sources
5. **Prioritizes Recency**: Focuses on 2023-2026 information

### When to Use Research

**Enable research (`--research`) for:**
- Statistical infographics requiring accurate numbers
- Market data, industry statistics, or trends
- Scientific or medical information
- Current events or recent developments
- Any topic where accuracy is critical

**Skip research for:**
- Simple conceptual infographics
- Internal process documentation
- Topics where you provide all the data in the prompt
- Speed-critical generation

### Research Output

When research is enabled, additional files are created:
- `{name}_research.json` - Raw research data and sources
- Research content is automatically incorporated into the infographic prompt

---

## Infographic Types

### 1. Statistical/Data-Driven (`--type statistical`)

Best for: Presenting numbers, percentages, survey results, and quantitative data.

**Key Elements:** Charts (bar, pie, line, donut), large numerical callouts, data comparisons, trend indicators.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Global internet usage 2025: 5.5 billion users (68% of population), \
   Asia Pacific 53%, Europe 15%, Americas 20%, Africa 12%" \
  -o figures/internet_stats.png --type statistical --style technology
```

---

### 2. Timeline (`--type timeline`)

Best for: Historical events, project milestones, company history, evolution of concepts.

**Key Elements:** Chronological flow, date markers, event nodes, connecting lines.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "History of AI: 1950 Turing Test, 1956 Dartmouth Conference, \
   1997 Deep Blue, 2016 AlphaGo, 2022 ChatGPT" \
  -o figures/ai_history.png --type timeline --style technology
```

---

### 3. Process/How-To (`--type process`)

Best for: Step-by-step instructions, workflows, procedures, tutorials.

**Key Elements:** Numbered steps, directional arrows, action icons, clear flow.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "How to start a podcast: 1. Choose your niche, 2. Plan content, \
   3. Set up equipment, 4. Record episodes, 5. Publish and promote" \
  -o figures/podcast_process.png --type process --style marketing
```

---

### 4. Comparison (`--type comparison`)

Best for: Product comparisons, pros/cons, before/after, option evaluation.

**Key Elements:** Side-by-side layout, matching categories, check/cross indicators.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Electric vs Gas Cars: Fuel cost (lower vs higher), \
   Maintenance (less vs more), Range (improving vs established)" \
  -o figures/ev_comparison.png --type comparison --style nature
```

---

### 5. List/Informational (`--type list`)

Best for: Tips, facts, key points, summaries, quick reference guides.

**Key Elements:** Numbered or bulleted points, icons, clear hierarchy.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "7 Habits of Highly Effective People: Be Proactive, \
   Begin with End in Mind, Put First Things First, Think Win-Win, \
   Seek First to Understand, Synergize, Sharpen the Saw" \
  -o figures/habits.png --type list --style corporate
```

---

### 6. Geographic (`--type geographic`)

Best for: Regional data, demographics, location-based statistics, global trends.

**Key Elements:** Map visualization, color coding, data overlays, legend.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Renewable energy adoption by region: Iceland 100%, Norway 98%, \
   Germany 50%, USA 22%, India 20%" \
  -o figures/renewable_map.png --type geographic --style nature
```

---

### 7. Hierarchical/Pyramid (`--type hierarchical`)

Best for: Organizational structures, priority levels, importance ranking.

**Key Elements:** Pyramid or tree structure, distinct levels, size progression.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Maslow's Hierarchy: Physiological, Safety, Love/Belonging, \
   Esteem, Self-Actualization" \
  -o figures/maslow.png --type hierarchical --style education
```

---

### 8. Anatomical/Visual Metaphor (`--type anatomical`)

Best for: Explaining complex systems using familiar visual metaphors.

**Key Elements:** Central metaphor image, labeled parts, connection lines.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Business as a human body: Brain=Leadership, Heart=Culture, \
   Arms=Sales, Legs=Operations, Skeleton=Systems" \
  -o figures/business_body.png --type anatomical --style corporate
```

---

### 9. Resume/Professional (`--type resume`)

Best for: Personal branding, CVs, portfolio highlights, professional achievements.

**Key Elements:** Photo area, skills visualization, timeline, contact info.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "UX Designer resume: Skills - User Research 95%, Wireframing 90%, \
   Prototyping 85%. Experience - 2020-2022 Junior, 2022-2025 Senior" \
  -o figures/resume.png --type resume --style technology
```

---

### 10. Social Media (`--type social`)

Best for: Instagram, LinkedIn, Twitter/X posts, shareable graphics.

**Key Elements:** Bold headline, minimal text, maximum impact, vibrant colors.

```bash
python skills/infographics/scripts/generate_infographic.py \
  "Save Water, Save Life: 2.2 billion people lack safe drinking water. \
   Tips: shorter showers, fix leaks, full loads only" \
  -o figures/water_social.png --type social --style marketing
```

---

## Style Presets

### Industry Styles (`--style`)

| Style | Colors | Best For |
|-------|--------|----------|
| `corporate` | Navy, steel blue, gold | Business reports, finance |
| `healthcare` | Medical blue, cyan, light cyan | Medical, wellness |
| `technology` | Tech blue, slate, violet | Software, data, AI |
| `nature` | Forest green, mint, earth brown | Environmental, organic |
| `education` | Academic blue, light blue, coral | Learning, academic |
| `marketing` | Coral, teal, yellow | Social media, campaigns |
| `finance` | Navy, gold, green/red | Investment, banking |
| `nonprofit` | Warm orange, sage, sand | Social causes, charities |

```bash
# Corporate style
python skills/infographics/scripts/generate_infographic.py \
  "Q4 Results" -o q4.png --type statistical --style corporate

# Healthcare style
python skills/infographics/scripts/generate_infographic.py \
  "Patient Journey" -o journey.png --type process --style healthcare
```

---

## Colorblind-Safe Palettes

### Available Palettes (`--palette`)

| Palette | Colors | Description |
|---------|--------|-------------|
| `wong` | Orange, sky blue, green, blue, vermillion | Most widely recommended |
| `ibm` | Ultramarine, indigo, magenta, orange, gold | IBM's accessible palette |
| `tol` | 12-color extended palette | For many categories |

```bash
# Wong's colorblind-safe palette
python skills/infographics/scripts/generate_infographic.py \
  "Survey results by category" -o survey.png --type statistical --palette wong
```

---

## Smart Iterative Refinement

### How It Works

```
┌─────────────────────────────────────────────────────┐
│  1. Generate infographic with Nano Banana Pro       │
│                    ↓                                │
│  2. Review quality with Gemini 3 Pro                │
│                    ↓                                │
│  3. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 1            │
│                    ↓                                │
│  4. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### Quality Review Criteria

Gemini 3 Pro evaluates each infographic on:

1. **Visual Hierarchy & Layout** (0-2 points)
   - Clear visual hierarchy
   - Logical reading flow
   - Balanced composition

2. **Typography & Readability** (0-2 points)
   - Readable text
   - Bold headlines
   - No overlapping

3. **Data Visualization** (0-2 points)
   - Prominent numbers
   - Clear charts/icons
   - Proper labels

4. **Color & Accessibility** (0-2 points)
   - Professional colors
   - Sufficient contrast
   - Colorblind-friendly

5. **Overall Impact** (0-2 points)
   - Professional appearance
   - Free of visual bugs
   - Achieves communication goal

### Review Log

Each generation produces a JSON review log:
```json
{
  "user_prompt": "5 benefits of exercise...",
  "infographic_type": "list",
  "style": "healthcare",
  "doc_type": "marketing",
  "quality_threshold": 8.5,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/exercise_v1.png",
      "score": 8.7,
      "needs_improvement": false,
      "critique": "SCORE: 8.7\nSTRENGTHS:..."
    }
  ],
  "final_score": 8.7,
  "early_stop": true,
  "early_stop_reason": "Quality score 8.7 meets threshold 8.5"
}
```

---

## Command-Line Reference

```bash
python skills/infographics/scripts/generate_infographic.py [OPTIONS] PROMPT

Arguments:
  PROMPT                    Description of the infographic content

Options:
  -o, --output PATH         Output file path (required)
  -t, --type TYPE           Infographic type preset
  -s, --style STYLE         Industry style preset
  -p, --palette PALETTE     Colorblind-safe palette
  -b, --background COLOR    Background color (default: white)
  --doc-type TYPE           Document type for quality threshold
  --iterations N            Maximum refinement iterations (default: 3)
  --api-key KEY             OpenRouter API key
  -v, --verbose             Verbose output
  --list-options            List all available options
```

### List All Options

```bash
python skills/infographics/scripts/generate_infographic.py --list-options
```

---

## Configuration

### API Key Setup

Set your OpenRouter API key:
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

Get an API key at: https://openrouter.ai/keys

---

## Prompt Engineering Tips

### Be Specific About Content

✓ **Good prompts** (specific, detailed):
```
"5 benefits of meditation: reduces stress, improves focus, 
better sleep, lower blood pressure, emotional balance"
```

✗ **Avoid vague prompts**:
```
"meditation infographic"
```

### Include Data Points

✓ **Good**:
```
"Market growth from $10B (2020) to $45B (2025), CAGR 35%"
```

✗ **Vague**:
```
"market is growing"
```

### Specify Visual Elements

✓ **Good**:
```
"Timeline showing 5 milestones with icons for each event"
```

---

## Reference Files

For detailed guidance, load these reference files:

- **`references/infographic_types.md`**: Extended templates for all 10+ types
- **`references/design_principles.md`**: Visual hierarchy, layout, typography
- **`references/color_palettes.md`**: Full palette specifications

---

## Troubleshooting

### Common Issues

**Problem**: Text in infographic is unreadable
- **Solution**: Reduce text content; use --type to specify layout type

**Problem**: Colors clash or are inaccessible
- **Solution**: Use `--palette wong` for colorblind-safe colors

**Problem**: Quality score too low
- **Solution**: Increase iterations with `--iterations 3`; use more specific prompt

**Problem**: Wrong infographic type generated
- **Solution**: Always specify `--type` flag for consistent results

---

## Integration with Other Skills

This skill works synergistically with:

- **scientific-schematics**: For technical diagrams and flowcharts
- **market-research-reports**: Infographics for business reports
- **scientific-slides**: Infographic elements for presentations
- **generate-image**: For non-infographic visual content

---

## Quick Reference Checklist

Before generating:
- [ ] Clear, specific content description
- [ ] Infographic type selected (`--type`)
- [ ] Style appropriate for audience (`--style`)
- [ ] Output path specified (`-o`)
- [ ] API key configured

After generating:
- [ ] Review the generated image
- [ ] Check the review log for scores
- [ ] Regenerate with more specific prompt if needed

---

Use this skill to create professional, accessible, and visually compelling infographics using the power of Nano Banana Pro AI with intelligent quality review.

---

## Reference: Color_Palettes

# Infographic Color Palettes Reference

This reference provides comprehensive color palette options for creating accessible, professional infographics.

---

## Colorblind-Safe Palettes

These palettes are designed to be distinguishable by people with various forms of color vision deficiency.

### Wong's Palette (7 Colors)

The most widely recommended colorblind-safe palette, developed by Bang Wong for scientific visualization.

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Black | `#000000` | 0, 0, 0 | Text, outlines |
| Orange | `#E69F00` | 230, 159, 0 | Primary accent |
| Sky Blue | `#56B4E9` | 86, 180, 233 | Primary data |
| Bluish Green | `#009E73` | 0, 158, 115 | Secondary data |
| Yellow | `#F0E442` | 240, 228, 66 | Highlight |
| Blue | `#0072B2` | 0, 114, 178 | Primary category |
| Vermillion | `#D55E00` | 213, 94, 0 | Alert, emphasis |
| Reddish Purple | `#CC79A7` | 204, 121, 167 | Tertiary data |

**Prompt usage:**
```
"Use Wong's colorblind-safe palette: orange (#E69F00), sky blue (#56B4E9), 
bluish green (#009E73), and blue (#0072B2) for data categories"
```

---

### IBM Colorblind-Safe Palette (8 Colors)

IBM's accessible color palette designed for data visualization.

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Ultramarine | `#648FFF` | 100, 143, 255 | Primary blue |
| Indigo | `#785EF0` | 120, 94, 240 | Secondary |
| Magenta | `#DC267F` | 220, 38, 127 | Accent/Alert |
| Orange | `#FE6100` | 254, 97, 0 | Warning/Highlight |
| Gold | `#FFB000` | 255, 176, 0 | Positive/Success |
| Black | `#000000` | 0, 0, 0 | Text |
| White | `#FFFFFF` | 255, 255, 255 | Background |
| Gray | `#808080` | 128, 128, 128 | Neutral |

**Prompt usage:**
```
"Use IBM colorblind-safe colors: ultramarine (#648FFF), indigo (#785EF0),
magenta (#DC267F), and gold (#FFB000) for visual elements"
```

---

### Okabe-Ito Palette (8 Colors)

Developed by Masataka Okabe and Kei Ito, widely used in scientific publications.

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Black | `#000000` | 0, 0, 0 | Text, primary |
| Orange | `#E69F00` | 230, 159, 0 | Category 1 |
| Sky Blue | `#56B4E9` | 86, 180, 233 | Category 2 |
| Bluish Green | `#009E73` | 0, 158, 115 | Category 3 |
| Yellow | `#F0E442` | 240, 228, 66 | Category 4 |
| Blue | `#0072B2` | 0, 114, 178 | Category 5 |
| Vermillion | `#D55E00` | 213, 94, 0 | Category 6 |
| Reddish Purple | `#CC79A7` | 204, 121, 167 | Category 7 |

**Note:** Identical to Wong's palette - both are industry standards.

---

### Tol's Qualitative Palette (12 Colors)

Paul Tol's extended colorblind-safe palette for more categories.

| Name | Hex | RGB |
|------|-----|-----|
| Indigo | `#332288` | 51, 34, 136 |
| Cyan | `#88CCEE` | 136, 204, 238 |
| Teal | `#44AA99` | 68, 170, 153 |
| Green | `#117733` | 17, 119, 51 |
| Olive | `#999933` | 153, 153, 51 |
| Sand | `#DDCC77` | 221, 204, 119 |
| Rose | `#CC6677` | 204, 102, 119 |
| Wine | `#882255` | 136, 34, 85 |
| Purple | `#AA4499` | 170, 68, 153 |
| Light Gray | `#DDDDDD` | 221, 221, 221 |
| Gray | `#888888` | 136, 136, 136 |
| Black | `#000000` | 0, 0, 0 |

---

## Industry-Specific Palettes

### Corporate/Business

Classic, professional appearance suitable for business reports and presentations.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Navy | `#1E3A5F` | 30, 58, 95 |
| Secondary | Steel Blue | `#4A90A4` | 74, 144, 164 |
| Tertiary | Light Blue | `#A8D5E2` | 168, 213, 226 |
| Accent | Gold | `#F5A623` | 245, 166, 35 |
| Background | Light Gray | `#F5F5F5` | 245, 245, 245 |
| Text | Charcoal | `#333333` | 51, 51, 51 |

**Prompt usage:**
```
"Corporate business color scheme: navy blue (#1E3A5F) primary, 
steel blue (#4A90A4) secondary, gold (#F5A623) accent, 
light gray background, professional clean design"
```

---

### Healthcare/Medical

Trust-inducing, clinical colors appropriate for health-related content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Medical Blue | `#0077B6` | 0, 119, 182 |
| Secondary | Cyan | `#00B4D8` | 0, 180, 216 |
| Tertiary | Light Cyan | `#90E0EF` | 144, 224, 239 |
| Accent | Coral | `#FF6B6B` | 255, 107, 107 |
| Background | White | `#FFFFFF` | 255, 255, 255 |
| Text | Dark Blue | `#023E8A` | 2, 62, 138 |

**Prompt usage:**
```
"Healthcare medical color scheme: medical blue (#0077B6), 
cyan (#00B4D8) accents, coral (#FF6B6B) for emphasis, 
clean clinical white background, professional medical design"
```

---

### Technology/Data

Modern, tech-forward appearance, works well with dark mode.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary Dark | Deep Navy | `#1A1A2E` | 26, 26, 46 |
| Secondary | Navy | `#16213E` | 22, 33, 62 |
| Tertiary | Blue | `#0F3460` | 15, 52, 96 |
| Accent | Electric Blue | `#00D9FF` | 0, 217, 255 |
| Accent 2 | Neon Purple | `#7B2CBF` | 123, 44, 191 |
| Text | White | `#FFFFFF` | 255, 255, 255 |

**Light Mode Alternative:**

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Tech Blue | `#2563EB` | 37, 99, 235 |
| Secondary | Slate | `#475569` | 71, 85, 105 |
| Accent | Violet | `#7C3AED` | 124, 58, 237 |
| Background | Light Gray | `#F8FAFC` | 248, 250, 252 |

**Prompt usage:**
```
"Technology data visualization colors: deep navy (#1A1A2E) background,
electric blue (#00D9FF) and neon purple (#7B2CBF) accents,
modern tech aesthetic, futuristic design"
```

---

### Nature/Environmental

Earth tones and greens for sustainability and environmental topics.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Forest | `#2D6A4F` | 45, 106, 79 |
| Secondary | Green | `#40916C` | 64, 145, 108 |
| Tertiary | Mint | `#95D5B2` | 149, 213, 178 |
| Accent | Earth Brown | `#8B4513` | 139, 69, 19 |
| Background | Cream | `#FAF3E0` | 250, 243, 224 |
| Text | Dark Green | `#1B4332` | 27, 67, 50 |

**Prompt usage:**
```
"Environmental nature color scheme: forest green (#2D6A4F),
mint (#95D5B2), earth brown (#8B4513) accents,
cream background, organic natural design feel"
```

---

### Education/Academic

Friendly yet professional colors for learning content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Academic Blue | `#3D5A80` | 61, 90, 128 |
| Secondary | Light Blue | `#98C1D9` | 152, 193, 217 |
| Tertiary | Cream | `#E0FBFC` | 224, 251, 252 |
| Accent | Coral | `#EE6C4D` | 238, 108, 77 |
| Background | Warm White | `#FEFEFE` | 254, 254, 254 |
| Text | Dark Gray | `#293241` | 41, 50, 65 |

**Prompt usage:**
```
"Education academic color scheme: academic blue (#3D5A80),
light blue (#98C1D9), coral (#EE6C4D) highlights,
warm white background, friendly educational design"
```

---

### Marketing/Creative

Bold, vibrant colors for attention-grabbing content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Coral | `#FF6B6B` | 255, 107, 107 |
| Secondary | Teal | `#4ECDC4` | 78, 205, 196 |
| Tertiary | Yellow | `#FFE66D` | 255, 230, 109 |
| Accent | Purple | `#9B59B6` | 155, 89, 182 |
| Background | White | `#FFFFFF` | 255, 255, 255 |
| Text | Charcoal | `#2C3E50` | 44, 62, 80 |

**Prompt usage:**
```
"Marketing creative colors: vibrant coral (#FF6B6B), teal (#4ECDC4),
yellow (#FFE66D) accents, bold eye-catching design,
modern and energetic feel"
```

---

### Finance/Investment

Conservative, trustworthy appearance for financial content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Navy | `#14213D` | 20, 33, 61 |
| Secondary | Gold | `#FCA311` | 252, 163, 17 |
| Tertiary | Light Gray | `#E5E5E5` | 229, 229, 229 |
| Accent | Green | `#2ECC71` | 46, 204, 113 |
| Accent Negative | Red | `#E74C3C` | 231, 76, 60 |
| Background | White | `#FFFFFF` | 255, 255, 255 |
| Text | Black | `#000000` | 0, 0, 0 |

**Prompt usage:**
```
"Finance investment color scheme: navy (#14213D), gold (#FCA311),
green (#2ECC71) for positive, red (#E74C3C) for negative,
conservative professional design, trustworthy appearance"
```

---

### Creative/Design

Artistic, gradient-friendly palette for creative content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Purple | `#7400B8` | 116, 0, 184 |
| Secondary | Indigo | `#5E60CE` | 94, 96, 206 |
| Tertiary | Blue | `#4EA8DE` | 78, 168, 222 |
| Accent | Cyan | `#48BFE3` | 72, 191, 227 |
| Accent 2 | Pink | `#F72585` | 247, 37, 133 |
| Background | Dark | `#1A1A2E` | 26, 26, 46 |

**Prompt usage:**
```
"Creative design colors: purple (#7400B8) to cyan (#48BFE3) gradient,
pink (#F72585) accents, artistic modern style,
dark background, bold creative aesthetic"
```

---

### Government/Policy

Formal, accessible colors for public sector content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Navy | `#003366` | 0, 51, 102 |
| Secondary | Red | `#CC0000` | 204, 0, 0 |
| Tertiary | Light Blue | `#6699CC` | 102, 153, 204 |
| Neutral | Gray | `#666666` | 102, 102, 102 |
| Background | White | `#FFFFFF` | 255, 255, 255 |
| Text | Black | `#000000` | 0, 0, 0 |

**Prompt usage:**
```
"Government policy colors: navy blue (#003366), red (#CC0000) accents,
light blue (#6699CC) secondary, formal accessible design,
high contrast for readability"
```

---

### Nonprofit/Cause

Warm, human-centered colors for social impact content.

| Role | Name | Hex | RGB |
|------|------|-----|-----|
| Primary | Warm Orange | `#E07A5F` | 224, 122, 95 |
| Secondary | Sage | `#81B29A` | 129, 178, 154 |
| Tertiary | Sand | `#F2CC8F` | 242, 204, 143 |
| Accent | Deep Blue | `#3D405B` | 61, 64, 91 |
| Background | Cream | `#F4F1DE` | 244, 241, 222 |
| Text | Dark | `#333333` | 51, 51, 51 |

**Prompt usage:**
```
"Nonprofit cause colors: warm orange (#E07A5F), sage green (#81B29A),
sand (#F2CC8F), human-centered warm design,
cream background, impactful and welcoming"
```

---

## Gradient Combinations

Pre-defined gradient combinations for modern infographics.

### Sunset Gradient
```
Start: #FF6B6B (Coral)
Middle: #FFA07A (Light Salmon)
End: #FFD93D (Yellow)
Direction: Top to bottom or left to right
```

### Ocean Gradient
```
Start: #0077B6 (Blue)
Middle: #00B4D8 (Cyan)
End: #90E0EF (Light Cyan)
Direction: Top to bottom
```

### Forest Gradient
```
Start: #1B4332 (Dark Green)
Middle: #40916C (Green)
End: #95D5B2 (Mint)
Direction: Bottom to top
```

### Purple Dream Gradient
```
Start: #7400B8 (Purple)
Middle: #5E60CE (Indigo)
End: #48BFE3 (Cyan)
Direction: Left to right
```

### Warm Gold Gradient
```
Start: #F5A623 (Gold)
Middle: #FFC857 (Light Gold)
End: #FFE8A8 (Pale Yellow)
Direction: Top to bottom
```

### Cool Steel Gradient
```
Start: #1E3A5F (Navy)
Middle: #4A90A4 (Steel Blue)
End: #A8D5E2 (Light Blue)
Direction: Left to right
```

**Prompt usage for gradients:**
```
"Use ocean gradient background from blue (#0077B6) to light cyan (#90E0EF),
flowing top to bottom, modern clean design"
```

---

## Contrast Checking

### WCAG 2.1 Requirements

| Contrast Ratio | Requirement |
|----------------|-------------|
| 4.5:1 | Normal text (under 18pt) |
| 3:1 | Large text (18pt+ or 14pt bold) |
| 3:1 | Graphics and UI components |

### Common Safe Combinations

**On White Background (#FFFFFF):**
| Text Color | Hex | Contrast Ratio |
|------------|-----|----------------|
| Black | `#000000` | 21:1 ✓ |
| Dark Gray | `#333333` | 12.6:1 ✓ |
| Navy | `#1E3A5F` | 11.2:1 ✓ |
| Dark Green | `#1B4332` | 10.9:1 ✓ |
| Dark Blue | `#0072B2` | 5.7:1 ✓ |
| Medium Gray | `#666666` | 5.7:1 ✓ |
| Red | `#CC0000` | 5.5:1 ✓ |

**On Dark Background (#1A1A2E):**
| Text Color | Hex | Contrast Ratio |
|------------|-----|----------------|
| White | `#FFFFFF` | 17.1:1 ✓ |
| Light Gray | `#E5E5E5` | 13.8:1 ✓ |
| Light Cyan | `#90E0EF` | 10.2:1 ✓ |
| Yellow | `#F0E442` | 12.5:1 ✓ |
| Light Blue | `#56B4E9` | 7.8:1 ✓ |

### Colors to Avoid Together

These combinations have poor contrast or are problematic for colorblind users:

- Red and Green (most common colorblindness)
- Blue and Purple (hard to distinguish)
- Light green and Yellow (low contrast)
- Red and Orange (similar hues)
- Blue and Gray (can be confused)
- Pink and Gray (similar values)

---

## Quick Reference: Color Prompt Phrases

Copy-paste these phrases into your prompts:

### By Mood

```
"Warm and inviting color palette with oranges, yellows, and cream"
"Cool professional color palette with blues, grays, and navy"
"Bold and energetic colors with bright accents on white background"
"Soft and calming pastel color scheme"
"High contrast black and white with single accent color"
"Earth tones with greens, browns, and natural colors"
```

### By Industry

```
"Corporate business colors: navy, gray, gold accents"
"Healthcare professional colors: blue, teal, white, clean clinical feel"
"Technology modern colors: dark background with neon blue accents"
"Environmental green color scheme with natural earth tones"
"Educational friendly colors: blue, coral, cream, approachable design"
"Financial conservative colors: navy, gold, high trust appearance"
```

### By Accessibility

```
"Colorblind-safe palette using Wong's recommended colors"
"High contrast color scheme meeting WCAG accessibility standards"
"Distinct colors that work in grayscale"
"IBM colorblind-safe palette for data visualization"
"Colors with patterns and labels for accessibility"
```

---

## Testing Your Colors

### Online Tools

1. **Contrast Checkers:**
   - WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
   - Coolors Contrast Checker: https://coolors.co/contrast-checker

2. **Colorblind Simulators:**
   - Coblis: https://www.color-blindness.com/coblis-color-blindness-simulator/
   - Sim Daltonism (Mac app)
   - Color Oracle (Desktop app)

3. **Palette Generators:**
   - Coolors: https://coolors.co/
   - Adobe Color: https://color.adobe.com/
   - Paletton: https://paletton.com/

### Quick Grayscale Test

Convert your infographic to grayscale. If all elements are still distinguishable, your color choices are accessible.

---

Use these palettes as starting points, adjusting as needed for your specific content and brand requirements. Always test for accessibility before finalizing.

---

## Reference: Design_Principles

# Infographic Design Principles

This reference covers the fundamental design principles for creating effective, professional infographics.

---

## Visual Hierarchy

Visual hierarchy guides the viewer's eye through your infographic in a deliberate order, ensuring key information is seen first.

### The Hierarchy Pyramid

1. **Primary Elements** (Seen First)
   - Headlines and titles
   - Large numbers or key statistics
   - Hero images or main illustrations
   - Call-to-action elements

2. **Secondary Elements** (Seen Second)
   - Subheadings and section titles
   - Charts and graphs
   - Icons and visual markers
   - Key supporting text

3. **Tertiary Elements** (Seen Last)
   - Body text and descriptions
   - Legends and labels
   - Source citations
   - Fine print and footnotes

### Creating Hierarchy

**Size**: Larger elements attract attention first
- Headlines: 200-300% larger than body text
- Key stats: Make numbers 2-4x larger than labels
- Important icons: 1.5-2x larger than supporting icons

**Color**: Bright and contrasting colors draw the eye
- Use accent colors sparingly for emphasis
- Reserve the brightest color for the most important element
- Use muted colors for supporting information

**Position**: Top-left and center are seen first
- Place most important content at top or center
- Supporting details toward bottom or edges
- Reading flow: top-to-bottom, left-to-right (in Western cultures)

**Contrast**: High contrast elements stand out
- Dark on light or light on dark for key text
- Colored elements against neutral backgrounds
- Borders and shadows to lift key elements

**White Space**: Isolation draws attention
- Surround important elements with space
- Don't crowd key information
- Use spacing to group related items

---

## Layout Patterns

### F-Pattern Layout

Best for: Text-heavy infographics, lists, articles

```
┌─────────────────────────────────────┐
│ ████████████████████████████████████│  ← Top horizontal scan
├─────────────────────────────────────┤
│ █████████████████                   │  ← Second horizontal scan
├─────────────────────────────────────┤
│ █████                               │
│ █████                               │  ← Vertical scan down left
│ █████                               │
│ █████                               │
└─────────────────────────────────────┘
```

**Application:**
- Place headline across full width at top
- Important subhead on second line
- Key content aligned to left
- Less critical content on right

### Z-Pattern Layout

Best for: Minimal content, landing pages, single-message infographics

```
┌─────────────────────────────────────┐
│ ●────────────────────────────────→ ●│  ← Start top-left, scan right
├─────────────────────────────────────┤
│      ╲                              │
│        ╲                            │  ← Diagonal scan
│          ╲                          │
├─────────────────────────────────────┤
│ ●────────────────────────────────→ ●│  ← Bottom left to right
└─────────────────────────────────────┘
```

**Application:**
- Logo/headline top-left
- Key visual top-right
- Diagonal eye movement through center
- Call-to-action bottom-right

### Single Column Layout

Best for: Mobile-friendly, scrolling content, process infographics

```
┌───────────────┐
│    HEADER     │
├───────────────┤
│   Section 1   │
├───────────────┤
│   Section 2   │
├───────────────┤
│   Section 3   │
├───────────────┤
│   Section 4   │
├───────────────┤
│    FOOTER     │
└───────────────┘
```

**Application:**
- Vertical scrolling content
- Step-by-step processes
- Timeline infographics
- Mobile-first design

### Multi-Column Layout

Best for: Comparisons, feature lists, complex data

```
┌─────────────────────────────────────┐
│           HEADER/TITLE              │
├──────────────┬──────────────────────┤
│   Column 1   │      Column 2        │
│   --------   │      --------        │
│   Content    │      Content         │
│   Content    │      Content         │
│   Content    │      Content         │
├──────────────┴──────────────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

**Application:**
- Side-by-side comparisons
- Pros and cons lists
- Feature matrices
- Two categories of information

### Grid Layout

Best for: Multiple equal-weight items, statistics, icon grids

```
┌─────────────────────────────────────┐
│           HEADER/TITLE              │
├───────────┬───────────┬─────────────┤
│   Item 1  │   Item 2  │   Item 3    │
├───────────┼───────────┼─────────────┤
│   Item 4  │   Item 5  │   Item 6    │
├───────────┼───────────┼─────────────┤
│   Item 7  │   Item 8  │   Item 9    │
├───────────┴───────────┴─────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

**Application:**
- Multiple statistics (2x2, 3x3, 2x3 grids)
- Icon collections
- Feature highlights
- Team member displays

### Modular/Card Layout

Best for: Varied content types, flexible information, modern designs

```
┌─────────────────────────────────────┐
│           HEADER/TITLE              │
├───────────────────┬─────────────────┤
│                   │      Card 2     │
│     Card 1        ├─────────────────┤
│     (large)       │      Card 3     │
├───────────────────┼─────────────────┤
│      Card 4       │      Card 5     │
└───────────────────┴─────────────────┘
```

**Application:**
- Mixed content types
- Varied importance levels
- Modern dashboard style
- Magazine-style layouts

---

## The 60-40 Rule

The optimal infographic balances visual and text content:

- **60% Visual Elements**: Icons, charts, illustrations, images, shapes
- **40% Text Content**: Headlines, labels, descriptions, data

### Why This Matters

- Too much text: Feels like a document, not an infographic
- Too many visuals: Lacks substance and clarity
- Right balance: Engaging AND informative

### Applying the Rule

**Visual Elements (60%)**
- Charts and graphs
- Icons and symbols
- Illustrations
- Photos
- Decorative shapes
- Color blocks
- Lines and connectors

**Text Elements (40%)**
- Headlines and titles
- Subheadings
- Data labels
- Brief descriptions
- Source citations
- Calls to action

---

## White Space (Negative Space)

White space is the empty area between and around elements. It's not wasted space—it's a design tool.

### Functions of White Space

1. **Improves Readability**: Gives eyes rest between content
2. **Creates Focus**: Isolated elements attract attention
3. **Groups Content**: Related items appear connected
4. **Adds Elegance**: Premium feel to design
5. **Reduces Clutter**: Prevents overwhelming viewers

### White Space Guidelines

**Margins**: Space around the entire infographic
- Minimum 5-10% of width/height
- More margin = more premium feel
- Consistent on all sides

**Padding**: Space inside elements (boxes, cards)
- Minimum equal to text line height
- More padding for important elements
- Consistent within similar elements

**Gaps**: Space between elements
- Related items: Small gaps (8-16px)
- Unrelated items: Large gaps (24-48px)
- Sections: Largest gaps (48-72px)

**Line Spacing**: Space between lines of text
- Body text: 1.4-1.6x font size
- Headlines: 1.1-1.3x font size
- Lists: 1.5-2x font size

---

## Typography

### Font Selection

**Sans-Serif Fonts** (Recommended for Infographics)
- Clean, modern appearance
- Better screen readability
- Professional feel
- Examples: Arial, Helvetica, Open Sans, Roboto, Montserrat

**Serif Fonts** (Use Sparingly)
- Traditional, authoritative feel
- Good for headlines in formal contexts
- Examples: Georgia, Times New Roman, Playfair Display

**Display Fonts** (Headlines Only)
- High impact for titles
- NOT for body text
- Examples: Impact, Bebas Neue, Oswald

### Font Pairing Rules

1. **Maximum 2-3 fonts** per infographic
2. **Contrast is key**: Pair different styles (serif + sans-serif)
3. **Establish roles**: One for headlines, one for body, one for accents
4. **Maintain consistency**: Same font for same purpose throughout

**Safe Pairings:**
- Montserrat (headlines) + Open Sans (body)
- Playfair Display (headlines) + Roboto (body)
- Bebas Neue (headlines) + Lato (body)
- Oswald (headlines) + Source Sans Pro (body)

### Font Sizes

| Element | Size Range | Weight |
|---------|------------|--------|
| Main Title | 36-72pt | Bold |
| Section Headers | 24-36pt | Bold/Semi-bold |
| Subheadings | 18-24pt | Semi-bold |
| Body Text | 12-16pt | Regular |
| Captions/Labels | 10-14pt | Regular/Light |
| Fine Print | 8-10pt | Light |

### Typography Best Practices

1. **Left-align body text** (easier to read than centered)
2. **Center-align headlines** (for impact)
3. **Limit line length** to 45-75 characters
4. **Use bold sparingly** for emphasis
5. **Avoid all caps** for body text (hard to read)
6. **ALL CAPS acceptable** for short headlines/labels
7. **Maintain contrast** between text and background (4.5:1 minimum)

---

## Story Structure

Every effective infographic tells a story with three parts:

### 1. Introduction (Hook)

**Purpose**: Grab attention, establish topic

**Elements:**
- Compelling headline
- Eye-catching hero visual
- Key statistic or question
- Topic introduction

**Best Practices:**
- Make it impossible to ignore
- Promise value ("Learn how to...")
- Create curiosity
- 10-15% of total space

### 2. Body (Content)

**Purpose**: Deliver the main information

**Elements:**
- Data and statistics
- Step-by-step content
- Comparisons and analysis
- Supporting visuals

**Best Practices:**
- Logical flow (chronological, importance, or categorical)
- Clear section breaks
- Balance visuals and text
- 70-80% of total space

### 3. Conclusion (Takeaway)

**Purpose**: Summarize, call to action

**Elements:**
- Key takeaway or summary
- Call to action
- Source citations
- Branding/attribution

**Best Practices:**
- Reinforce main message
- Clear next step for viewer
- Don't introduce new information
- 10-15% of total space

---

## Alignment and Grids

### Grid Systems

Use invisible grids to align elements consistently:

**Column Grid** (Most Common)
- 2, 3, 4, or 6 columns
- Elements span one or more columns
- Gutters (gaps) between columns
- Creates orderly, professional look

**Modular Grid**
- Columns + rows = modules
- More flexibility for varied content
- Good for complex layouts
- Dashboard-style designs

### Alignment Types

**Left Alignment**
- Most common for text
- Creates strong left edge
- Easy to scan
- Professional appearance

**Center Alignment**
- Good for headlines
- Creates symmetry
- Use sparingly for text
- Works for single elements

**Right Alignment**
- Rarely used for primary content
- Good for numbers in tables
- Can feel unusual in Western design
- Use intentionally

### Alignment Best Practices

1. **Pick one primary alignment** and stick to it
2. **Align related elements** to the same edge or center
3. **Use invisible grid lines** for consistency
4. **Avoid random placement**—everything should align to something
5. **Create visual connections** through alignment

---

## Color Usage

### Color Functions in Infographics

1. **Establish hierarchy**: Bright colors for important items
2. **Group related items**: Same color = same category
3. **Create contrast**: Distinguish between elements
4. **Evoke emotions**: Colors carry psychological meaning
5. **Reinforce brand**: Consistent with brand identity

### Color Distribution

**60-30-10 Rule:**
- **60%** Dominant color (background, large areas)
- **30%** Secondary color (supporting elements)
- **10%** Accent color (highlights, CTAs)

### Color Psychology

| Color | Association | Best For |
|-------|-------------|----------|
| Blue | Trust, professionalism, calm | Corporate, tech, healthcare |
| Green | Growth, nature, money | Environmental, finance, health |
| Red | Urgency, energy, passion | Alerts, sales, food |
| Orange | Friendly, confident, creative | CTAs, youth brands |
| Yellow | Optimism, caution, attention | Highlights, warnings |
| Purple | Luxury, creativity, wisdom | Premium brands, education |
| Black | Sophistication, power, elegance | Luxury, formal |
| White | Clean, simple, space | Backgrounds, breathing room |

### Contrast Requirements

For accessibility (WCAG 2.1 AA):
- **Normal text**: 4.5:1 contrast ratio minimum
- **Large text** (18pt+): 3:1 contrast ratio minimum
- **Graphics and UI**: 3:1 contrast ratio minimum

Tools to check contrast:
- WebAIM Contrast Checker
- Coolors Contrast Checker
- Adobe Color Accessibility Tools

---

## Icon Usage

### Icon Styles

**Line Icons** (Outline)
- Clean, modern look
- Work well at small sizes
- Best for minimal designs
- Consistent line weight important

**Filled Icons** (Solid)
- Bolder visual impact
- Good for quick recognition
- Work well as focal points
- More accessible at small sizes

**Illustrated Icons**
- More personality and uniqueness
- Higher visual weight
- Best for playful designs
- May not scale well

### Icon Best Practices

1. **Use one style consistently** throughout the infographic
2. **Ensure recognizability**—icons should be immediately understood
3. **Maintain consistent size** for icons at the same hierarchy level
4. **Add labels** when icon meaning isn't 100% clear
5. **Match visual weight** of icons to surrounding elements
6. **Consider color** carefully—single color often cleaner
7. **Avoid icon overload**—not everything needs an icon

### Icon Size Guidelines

| Context | Recommended Size |
|---------|------------------|
| Hero/Feature icon | 64-128px |
| Section icon | 32-48px |
| List item icon | 24-32px |
| Inline icon | 16-24px |

---

## Data Visualization Best Practices

### Choosing Chart Types

| Data Type | Best Chart |
|-----------|------------|
| Comparison (few items) | Bar chart |
| Comparison (many items) | Horizontal bar |
| Parts of a whole | Pie/donut chart |
| Trend over time | Line chart |
| Distribution | Histogram |
| Relationship | Scatter plot |
| Geographic | Map/choropleth |
| Hierarchy | Treemap |
| Flow/process | Sankey diagram |

### Chart Best Practices

1. **Label everything**: Axes, data points, legends
2. **Start Y-axis at zero** for bar charts (avoid misleading)
3. **Limit pie slices** to 5-7 maximum
4. **Use consistent colors** for same categories across charts
5. **Remove chart junk**: No 3D effects, minimal gridlines
6. **Highlight key data**: Use color to emphasize important points

### Number Presentation

- **Large numbers**: Use abbreviations (1.2M, not 1,200,000)
- **Percentages**: Include % symbol, one decimal max
- **Comparisons**: Use consistent units and precision
- **Context**: Always provide reference points ("2x industry average")

---

## Accessibility Considerations

### Visual Accessibility

1. **Color alone shouldn't convey meaning**
   - Add patterns, labels, or shapes
   - Works for colorblind users

2. **Sufficient contrast**
   - 4.5:1 for normal text
   - 3:1 for large text and graphics

3. **Text size**
   - Minimum 10pt for print
   - Minimum 12px for digital

4. **Don't rely on color legends**
   - Label data directly when possible

### Colorblind-Safe Design

- Use colorblind-safe palettes (see color_palettes.md)
- Test with colorblindness simulators
- Add patterns or textures for differentiation
- Use labels and direct annotation

### Reading Accessibility

- Clear hierarchy and flow
- Concise text
- Simple language
- Adequate spacing
- Logical reading order

---

## Quality Checklist

Before finalizing your infographic, verify:

### Layout
- [ ] Clear visual hierarchy
- [ ] Consistent alignment (grid-based)
- [ ] Adequate white space
- [ ] Logical reading flow
- [ ] Balanced composition

### Typography
- [ ] Maximum 2-3 fonts used
- [ ] Readable font sizes
- [ ] Sufficient text contrast
- [ ] Consistent styling for same elements
- [ ] Left-aligned body text

### Color
- [ ] 60-30-10 distribution
- [ ] Colorblind-safe palette
- [ ] Sufficient contrast (4.5:1 text)
- [ ] Consistent color meanings
- [ ] Not overwhelming

### Content
- [ ] Clear story structure (intro, body, conclusion)
- [ ] 60% visuals, 40% text (approximately)
- [ ] Key message is prominent
- [ ] Data is accurate and sourced
- [ ] Call to action included

### Icons and Graphics
- [ ] Consistent icon style
- [ ] Appropriate sizes
- [ ] Recognizable meanings
- [ ] Not overused

### Accessibility
- [ ] Works in grayscale
- [ ] Patterns/labels supplement color
- [ ] Readable at intended size
- [ ] Logical flow without visual cues

---

Use these principles as a foundation, adapting as needed for your specific content and audience.

---

## Reference: Infographic_Types

# Infographic Types Reference Guide

This reference provides extended templates, examples, and prompt patterns for each infographic type.

---

## 1. Statistical/Data-Driven Infographics

### Purpose
Present quantitative data, statistics, survey results, and numerical comparisons in an engaging visual format.

### Visual Elements
- **Bar charts**: Horizontal or vertical for comparisons
- **Pie/donut charts**: For proportions and percentages
- **Line charts**: For trends over time
- **Large number callouts**: Highlight key statistics
- **Icons**: Represent categories visually
- **Progress bars**: Show percentages or completion

### Layout Patterns
- **Single-stat hero**: One large number with supporting context
- **Multi-stat grid**: 3-6 statistics in a grid layout
- **Chart-centric**: Large visualization with supporting text
- **Comparison bars**: Side-by-side bar comparisons

### Prompt Templates

**Single Statistic Hero:**
```
Statistical infographic featuring one key statistic about [TOPIC]:
Main stat: [LARGE NUMBER] [UNIT/CONTEXT]
Supporting context: [2-3 sentences explaining the significance]
Large bold number in center, supporting text below,
relevant icon or illustration, [COLOR] accent color,
clean minimal design, white background.
```

**Multi-Statistic Grid:**
```
Statistical infographic presenting [TOPIC] data:
Stat 1: [NUMBER] [LABEL] (icon: [ICON])
Stat 2: [NUMBER] [LABEL] (icon: [ICON])
Stat 3: [NUMBER] [LABEL] (icon: [ICON])
Stat 4: [NUMBER] [LABEL] (icon: [ICON])
2x2 grid layout, large bold numbers, small icons above each,
[COLOR SCHEME], modern clean typography, white background.
```

**Chart-Focused:**
```
Statistical infographic with [CHART TYPE] showing [TOPIC]:
Data points: [VALUE 1], [VALUE 2], [VALUE 3], [VALUE 4]
Labels: [LABEL 1], [LABEL 2], [LABEL 3], [LABEL 4]
Large [bar/pie/donut] chart as main element,
title at top, legend below chart, [COLOR SCHEME],
data labels on chart, clean professional design.
```

### Example Prompts

**Healthcare Statistics:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Statistical infographic about heart disease: \
   Main stat: 17.9 million deaths per year globally. \
   Supporting stats in grid: 1 in 4 deaths caused by heart disease, \
   80% of heart disease is preventable, \
   150 minutes of exercise weekly reduces risk by 30%. \
   Heart icon, red and pink color scheme with gray accents, \
   large bold numbers, clean medical professional design, white background" \
  --output figures/heart_disease_stats.png
```

**Business Metrics:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Statistical infographic for Q4 business results: \
   Revenue: $2.4M (+15% YoY), Customers: 12,500 (+22%), \
   NPS Score: 78 (+8 points), Retention: 94%. \
   4-stat grid with upward arrow indicators for growth, \
   bar chart showing quarterly trend, \
   navy blue and gold corporate color scheme, \
   professional business design, white background" \
  --output figures/q4_metrics.png
```

---

## 2. Timeline Infographics

### Purpose
Display events, milestones, or developments in chronological order.

### Visual Elements
- **Timeline axis**: Horizontal or vertical line
- **Date markers**: Years, months, or specific dates
- **Event nodes**: Circles, icons, or images at each point
- **Description boxes**: Brief text for each event
- **Connecting elements**: Lines, arrows, or paths

### Layout Patterns
- **Horizontal timeline**: Left-to-right progression
- **Vertical timeline**: Top-to-bottom progression
- **Winding/snake timeline**: S-curve for many events
- **Circular timeline**: For cyclical or repeating events

### Prompt Templates

**Horizontal Timeline:**
```
Horizontal timeline infographic showing [TOPIC] from [START YEAR] to [END YEAR]:
[YEAR 1]: [EVENT 1] - [brief description]
[YEAR 2]: [EVENT 2] - [brief description]
[YEAR 3]: [EVENT 3] - [brief description]
[YEAR 4]: [EVENT 4] - [brief description]
Left-to-right timeline with circular nodes for each event,
connecting line between nodes, icons above each node,
[COLOR] gradient from past to present, date labels below,
clean modern design, white background.
```

**Vertical Timeline:**
```
Vertical timeline infographic showing [TOPIC]:
Top (earliest): [YEAR] - [EVENT]
Middle events: [YEAR] - [EVENT], [YEAR] - [EVENT]
Bottom (latest): [YEAR] - [EVENT]
Top-to-bottom flow, alternating left-right event boxes,
central vertical line connecting all events,
circular nodes with dates, [COLOR SCHEME],
professional clean design, white background.
```

**Project Milestone Timeline:**
```
Project timeline infographic for [PROJECT NAME]:
Phase 1: [DATES] - [MILESTONE] (status: complete)
Phase 2: [DATES] - [MILESTONE] (status: in progress)
Phase 3: [DATES] - [MILESTONE] (status: upcoming)
Phase 4: [DATES] - [MILESTONE] (status: planned)
Gantt-style horizontal bars, color-coded by status,
green for complete, yellow for in progress, gray for upcoming,
project name header, clean professional design.
```

### Example Prompts

**Technology Evolution:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Horizontal timeline infographic: Evolution of Mobile Phones \
   1983: First mobile phone (Motorola DynaTAC), \
   1992: First smartphone (IBM Simon), \
   2007: iPhone launches touchscreen era, \
   2010: First 4G networks, \
   2019: First 5G phones, \
   2023: Foldable phones mainstream. \
   Phone icons evolving at each node, gradient from gray (old) to blue (new), \
   connecting timeline arrow, year labels, clean tech design" \
  --output figures/mobile_evolution.png
```

**Company History:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Vertical timeline infographic: Our Company Journey \
   2010: Founded in garage with 2 employees, \
   2012: First major client signed, \
   2015: Reached 100 employees, \
   2018: IPO on NASDAQ, \
   2022: Expanded to 30 countries, \
   2025: 10,000 employees worldwide. \
   Milestone icons for each event, alternating left-right layout, \
   blue and gold corporate colors, growth trajectory feel, \
   professional business design" \
  --output figures/company_history.png
```

---

## 3. Process/How-To Infographics

### Purpose
Explain step-by-step procedures, workflows, instructions, or methodologies.

### Visual Elements
- **Numbered steps**: Clear sequence indicators
- **Arrows/connectors**: Show flow and direction
- **Action icons**: Illustrate each step
- **Brief descriptions**: Concise action text
- **Start/end indicators**: Clear beginning and conclusion

### Layout Patterns
- **Vertical cascade**: Steps flow top-to-bottom
- **Horizontal flow**: Left-to-right progression
- **Circular process**: Steps form a cycle
- **Branching flow**: Decision points with alternatives

### Prompt Templates

**Linear Process:**
```
Process infographic: How to [ACCOMPLISH GOAL]
Step 1: [ACTION] - [brief explanation] (icon: [ICON])
Step 2: [ACTION] - [brief explanation] (icon: [ICON])
Step 3: [ACTION] - [brief explanation] (icon: [ICON])
Step 4: [ACTION] - [brief explanation] (icon: [ICON])
Step 5: [ACTION] - [brief explanation] (icon: [ICON])
Numbered circles connected by arrows, icons for each step,
[VERTICAL/HORIZONTAL] flow, [COLOR SCHEME],
clear step labels, clean instructional design, white background.
```

**Circular Process:**
```
Circular process infographic showing [CYCLE NAME]:
Step 1: [ACTION] leads to
Step 2: [ACTION] leads to
Step 3: [ACTION] leads to
Step 4: [ACTION] returns to Step 1
Circular arrangement with arrows forming a cycle,
icons at each point, step numbers, [COLOR SCHEME],
continuous flow design, white background.
```

**Decision Flowchart:**
```
Decision flowchart infographic for [SCENARIO]:
Start: [INITIAL QUESTION]
If Yes: [PATH A] → [OUTCOME A]
If No: [PATH B] → [OUTCOME B]
Diamond shapes for decisions, rectangles for actions,
arrows connecting all elements, [COLOR SCHEME],
clear yes/no labels, flowchart style, white background.
```

### Example Prompts

**Recipe Process:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Process infographic: How to Make Perfect Coffee \
   Step 1: Grind fresh beans (coffee grinder icon), \
   Step 2: Heat water to 200°F (thermometer icon), \
   Step 3: Add 2 tablespoons per 6 oz water (measuring spoon icon), \
   Step 4: Brew for 4 minutes (timer icon), \
   Step 5: Serve and enjoy (coffee cup icon). \
   Vertical flow with large numbered circles, \
   brown and cream coffee color scheme, \
   arrows between steps, cozy design feel" \
  --output figures/coffee_process.png
```

**Onboarding Workflow:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Process infographic: New Employee Onboarding \
   Day 1: Welcome orientation and paperwork (clipboard icon), \
   Week 1: Meet your team and set up workspace (people icon), \
   Week 2: Training and system access (laptop icon), \
   Week 3: Shadow senior colleagues (handshake icon), \
   Week 4: First independent project (checkmark icon). \
   Horizontal timeline flow with milestones, \
   teal and coral corporate colors, \
   professional HR design style" \
  --output figures/onboarding_process.png
```

---

## 4. Comparison Infographics

### Purpose
Compare two or more options, products, concepts, or choices side by side.

### Visual Elements
- **Split layout**: Clear division between options
- **Matching rows**: Same categories for fair comparison
- **Check/cross marks**: Quick visual indicators
- **Rating systems**: Stars, bars, or numbers
- **Headers**: Clear identification of each option

### Layout Patterns
- **Two-column split**: Left vs Right
- **Table format**: Rows and columns
- **Venn diagram**: Overlapping comparisons
- **Feature matrix**: Multi-option comparison grid

### Prompt Templates

**Two-Option Comparison:**
```
Comparison infographic: [OPTION A] vs [OPTION B]
Header: [OPTION A] on left | [OPTION B] on right
Row 1 - [CATEGORY 1]: [A VALUE] | [B VALUE]
Row 2 - [CATEGORY 2]: [A VALUE] | [B VALUE]
Row 3 - [CATEGORY 3]: [A VALUE] | [B VALUE]
Row 4 - [CATEGORY 4]: [A VALUE] | [B VALUE]
Row 5 - [CATEGORY 5]: [A VALUE] | [B VALUE]
Split layout with [COLOR A] for left, [COLOR B] for right,
icons for each option header, checkmarks for advantages,
clean symmetrical design, white background.
```

**Multi-Option Matrix:**
```
Comparison matrix infographic: [TOPIC]
Options: [OPTION 1], [OPTION 2], [OPTION 3]
Feature 1: [✓/✗ for each]
Feature 2: [✓/✗ for each]
Feature 3: [✓/✗ for each]
Feature 4: [✓/✗ for each]
Table layout with colored headers for each option,
checkmarks and X marks in cells, [COLOR SCHEME],
clean grid design, white background.
```

**Pros and Cons:**
```
Pros and Cons infographic for [TOPIC]:
Pros (left side, green):
- [PRO 1]
- [PRO 2]
- [PRO 3]
Cons (right side, red):
- [CON 1]
- [CON 2]
- [CON 3]
Split layout with green left side, red right side,
thumbs up icon for pros, thumbs down for cons,
balanced visual weight, white background.
```

### Example Prompts

**Software Comparison:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Comparison infographic: Slack vs Microsoft Teams \
   Pricing: Both offer free tiers with paid upgrades, \
   Integration: Slack 2000+ apps, Teams Microsoft ecosystem, \
   Video calls: Teams native, Slack via Huddles, \
   File storage: Teams 1TB, Slack 5GB free, \
   Best for: Slack small teams, Teams enterprise. \
   Purple left side (Slack), blue right side (Teams), \
   logos at top, feature comparison rows, \
   checkmarks for strengths, modern tech design" \
  --output figures/slack_vs_teams.png
```

**Diet Comparison:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Comparison infographic: Keto Diet vs Mediterranean Diet \
   Weight loss: Both effective, Keto faster initial, \
   Heart health: Mediterranean better long-term, \
   Sustainability: Mediterranean easier to maintain, \
   Foods allowed: Keto high fat low carb, Med balanced, \
   Research support: Mediterranean more studied. \
   Green left (Keto), blue right (Mediterranean), \
   food icons for each, health/heart icons, \
   clean wellness design style" \
  --output figures/diet_comparison.png
```

---

## 5. List/Informational Infographics

### Purpose
Present tips, facts, key points, or information in an organized, scannable format.

### Visual Elements
- **Numbers or bullets**: Clear list indicators
- **Icons**: Visual representation of each point
- **Brief text**: Concise descriptions
- **Header**: Topic introduction
- **Consistent styling**: Uniform treatment of all items

### Layout Patterns
- **Vertical list**: Standard top-to-bottom
- **Two-column list**: For longer lists
- **Icon grid**: Icons with labels below
- **Cards**: Each point in a card/box

### Prompt Templates

**Numbered List:**
```
List infographic: [NUMBER] [TOPIC]
1. [POINT 1] - [brief explanation] (icon: [ICON])
2. [POINT 2] - [brief explanation] (icon: [ICON])
3. [POINT 3] - [brief explanation] (icon: [ICON])
4. [POINT 4] - [brief explanation] (icon: [ICON])
5. [POINT 5] - [brief explanation] (icon: [ICON])
Large numbers in circles, icons next to each point,
brief text descriptions, [COLOR SCHEME],
vertical layout with spacing, white background.
```

**Tips Format:**
```
Tips infographic: [NUMBER] Tips for [TOPIC]
Tip 1: [TIP] (lightbulb icon)
Tip 2: [TIP] (star icon)
Tip 3: [TIP] (checkmark icon)
Tip 4: [TIP] (target icon)
Tip 5: [TIP] (rocket icon)
Colorful tip boxes or cards, icons for each tip,
[COLOR SCHEME], engaging friendly design,
header at top, white background.
```

**Facts Format:**
```
Facts infographic: [NUMBER] Facts About [TOPIC]
Fact 1: [INTERESTING FACT]
Fact 2: [INTERESTING FACT]
Fact 3: [INTERESTING FACT]
Fact 4: [INTERESTING FACT]
Fact 5: [INTERESTING FACT]
Speech bubble or card style for each fact,
relevant icons, [COLOR SCHEME],
educational engaging design, white background.
```

### Example Prompts

**Productivity Tips:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "List infographic: 7 Productivity Tips for Remote Workers \
   1. Create a dedicated workspace (desk icon), \
   2. Set regular working hours (clock icon), \
   3. Take scheduled breaks (coffee icon), \
   4. Use noise-canceling headphones (headphones icon), \
   5. Batch similar tasks together (stack icon), \
   6. Limit social media during work (phone icon), \
   7. End each day with tomorrow's plan (checklist icon). \
   Large colorful numbers, icons beside each tip, \
   teal and orange color scheme, friendly modern design" \
  --output figures/remote_work_tips.png
```

**Fun Facts:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Facts infographic: 5 Amazing Facts About Honey \
   Fact 1: Honey never spoils - 3000 year old honey is still edible, \
   Fact 2: Bees visit 2 million flowers to make 1 lb of honey, \
   Fact 3: Honey can be used to treat wounds and burns, \
   Fact 4: A bee produces only 1/12 teaspoon in its lifetime, \
   Fact 5: Honey contains natural antibiotics. \
   Hexagon honeycomb shapes for each fact, \
   golden yellow and black color scheme, bee illustrations, \
   fun educational design" \
  --output figures/honey_facts.png
```

---

## 6. Geographic/Map-Based Infographics

### Purpose
Display location-based data, regional statistics, or geographic trends.

### Visual Elements
- **Map visualization**: World, country, or region
- **Color coding**: Data intensity by region
- **Data callouts**: Key statistics for regions
- **Legend**: Color scale explanation
- **Labels**: Region or country names

### Layout Patterns
- **Full map**: Map as primary element
- **Map with sidebar**: Data summary alongside
- **Regional focus**: Zoomed map section
- **Multi-map**: Several maps showing different data

### Prompt Templates

**World Map Data:**
```
Geographic infographic showing [TOPIC] globally:
Highest: [REGION/COUNTRY] - [VALUE]
Medium: [REGIONS] - [VALUE RANGE]
Lowest: [REGION/COUNTRY] - [VALUE]
World map with color-coded countries,
[DARK COLOR] for highest values, [LIGHT COLOR] for lowest,
legend showing color scale, key statistics callout,
clean cartographic design, light gray background.
```

**Country/Region Focus:**
```
Geographic infographic showing [TOPIC] in [COUNTRY/REGION]:
Region 1: [VALUE]
Region 2: [VALUE]
Region 3: [VALUE]
Map of [COUNTRY/REGION] with color-coded areas,
data labels for key regions, [COLOR] gradient,
legend with value scale, clean map design.
```

### Example Prompts

**Global Data:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Geographic infographic: Global Renewable Energy Adoption 2025 \
   Leaders: Iceland 100%, Norway 98%, Costa Rica 95%, \
   Growing: Germany 50%, UK 45%, China 30%, \
   Emerging: USA 22%, India 20%, Brazil 18%. \
   World map with green gradient coloring, \
   darker green for higher adoption, \
   legend showing percentage scale, \
   key country callouts with percentages, \
   clean modern cartographic style" \
  --output figures/renewable_map.png
```

**US Regional:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Geographic infographic: Tech Jobs by US Region 2025 \
   West Coast: 35% of tech jobs (California, Washington), \
   Northeast: 25% (New York, Massachusetts), \
   South: 22% (Texas, Florida, Georgia), \
   Midwest: 18% (Illinois, Colorado, Michigan). \
   US map with color-coded regions, \
   percentage labels on each region, \
   blue and purple tech color scheme, \
   legend showing job concentration, \
   professional business design" \
  --output figures/tech_jobs_map.png
```

---

## 7. Hierarchical/Pyramid Infographics

### Purpose
Show levels of importance, organizational structures, or ranked information.

### Visual Elements
- **Pyramid shape**: Triangle with levels
- **Level labels**: Clear tier identification
- **Size progression**: Larger at base, smaller at top
- **Color progression**: Gradient or distinct colors per level
- **Icons**: Optional for each level

### Layout Patterns
- **Traditional pyramid**: Wide base, narrow top
- **Inverted pyramid**: Narrow base, wide top
- **Org chart**: Tree structure
- **Stacked blocks**: Square levels

### Prompt Templates

**Classic Pyramid:**
```
Hierarchical pyramid infographic: [TOPIC]
Top (Level 1 - most important/rare): [ITEM]
Level 2: [ITEM]
Level 3: [ITEM]
Level 4: [ITEM]
Base (Level 5 - foundation/most common): [ITEM]
Triangle pyramid with 5 horizontal sections,
[COLOR] gradient from [TOP COLOR] to [BASE COLOR],
labels on each tier, icons optional,
clean geometric design, white background.
```

**Organizational Hierarchy:**
```
Organizational chart infographic for [ORGANIZATION]:
Top: [CEO/LEADER]
Level 2: [VPs/DIRECTORS] (3-4 boxes)
Level 3: [MANAGERS] (6-8 boxes)
Level 4: [TEAM LEADS] (multiple boxes)
Tree structure flowing down, connecting lines between levels,
[COLOR SCHEME], professional corporate design,
role titles in boxes, white background.
```

### Example Prompts

**Learning Pyramid:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Hierarchical pyramid infographic: Learning Retention Rates \
   Top: Teaching others - 90% retention, \
   Level 2: Practice by doing - 75% retention, \
   Level 3: Discussion groups - 50% retention, \
   Level 4: Demonstration - 30% retention, \
   Level 5: Audio/Visual - 20% retention, \
   Base: Lecture/Reading - 5-10% retention. \
   Colorful pyramid with 6 levels, \
   gradient from green (top) to red (base), \
   percentage labels, educational design" \
  --output figures/learning_pyramid.png
```

**Energy Pyramid:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Hierarchical pyramid infographic: Ecological Energy Pyramid \
   Top: Apex predators (eagles, wolves) - smallest, \
   Level 2: Secondary consumers (snakes, foxes), \
   Level 3: Primary consumers (rabbits, deer), \
   Base: Producers (plants, algae) - largest. \
   Triangle pyramid with animal silhouettes, \
   green gradient from base to top, \
   energy flow arrows on side, \
   scientific educational design" \
  --output figures/energy_pyramid.png
```

---

## 8. Anatomical/Visual Metaphor Infographics

### Purpose
Explain complex systems using familiar visual metaphors (bodies, machines, trees, etc.).

### Visual Elements
- **Central metaphor image**: The main visual (body, tree, machine)
- **Labeled parts**: Components identified
- **Callout lines**: Connecting labels to parts
- **Descriptions**: Explanations for each part
- **Color coding**: Different parts in different colors

### Layout Patterns
- **Central image with callouts**: Labels pointing to parts
- **Exploded view**: Parts separated but arranged
- **Cross-section**: Inside view of metaphor
- **Before/after**: Metaphor in different states

### Prompt Templates

**Body Metaphor:**
```
Anatomical infographic using human body to explain [TOPIC]:
Brain represents [CONCEPT] - [explanation]
Heart represents [CONCEPT] - [explanation]
Hands represent [CONCEPT] - [explanation]
Feet represent [CONCEPT] - [explanation]
Human body silhouette with labeled callouts,
[COLOR SCHEME], clean medical illustration style,
connecting lines to descriptions, white background.
```

**Machine Metaphor:**
```
Anatomical infographic using machine/engine to explain [TOPIC]:
Fuel tank represents [CONCEPT]
Engine represents [CONCEPT]
Wheels represent [CONCEPT]
Steering represents [CONCEPT]
Machine illustration with labeled components,
callout lines and descriptions, [COLOR SCHEME],
technical illustration style, white background.
```

### Example Prompts

**Business as Body:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Anatomical infographic: A Business is Like a Human Body \
   Brain = Leadership and strategy (makes decisions), \
   Heart = Company culture (pumps energy), \
   Arms = Sales and marketing (reaches out), \
   Legs = Operations (keeps moving forward), \
   Skeleton = Systems and processes (provides structure). \
   Human body silhouette in blue, \
   labeled callout boxes for each part, \
   professional corporate design, white background" \
  --output figures/business_body.png
```

**Computer as House:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Anatomical infographic: Computer as a House \
   CPU = The brain/office (processes information), \
   RAM = The desk (temporary workspace), \
   Hard Drive = The filing cabinet (long-term storage), \
   GPU = The entertainment room (handles visuals), \
   Motherboard = The foundation (connects everything). \
   House illustration with cutaway view, \
   labeled rooms matching computer parts, \
   blue and gray tech colors, educational style" \
  --output figures/computer_house.png
```

---

## 9. Resume/Professional Infographics

### Purpose
Present professional information, skills, experience, and achievements visually.

### Visual Elements
- **Photo/avatar section**: Personal branding
- **Skills visualization**: Bars, charts, ratings
- **Timeline**: Career progression
- **Contact icons**: Email, phone, social
- **Achievement badges**: Certifications, awards

### Layout Patterns
- **Single column**: Vertical flow
- **Two column**: Info left, skills right
- **Header focus**: Large header with photo
- **Modular**: Distinct sections/cards

### Prompt Templates

**Professional Resume:**
```
Resume infographic for [NAME], [PROFESSION]:
Photo area: Circular avatar placeholder
Skills: [SKILL 1] 90%, [SKILL 2] 85%, [SKILL 3] 75%
Experience: [YEAR-YEAR] [ROLE] at [COMPANY], [YEAR-YEAR] [ROLE] at [COMPANY]
Education: [DEGREE] from [INSTITUTION]
Contact: Email, LinkedIn, Portfolio icons
Professional photo area at top, horizontal skill bars,
timeline for experience, [COLOR SCHEME],
modern professional design, white background.
```

### Example Prompts

**Designer Resume:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Resume infographic for a Graphic Designer: \
   Circular avatar placeholder at top, \
   Skills with colored bars: Adobe Suite 95%, UI/UX 90%, Branding 85%, Motion 75%. \
   Experience timeline: 2018-2020 Junior Designer at Agency X, \
   2020-2023 Senior Designer at Studio Y, 2023-Present Creative Director at Company Z. \
   Education: BFA Graphic Design. \
   Contact icons row at bottom. \
   Coral and teal color scheme, creative modern design" \
  --output figures/designer_resume.png
```

---

## 10. Social Media/Interactive Infographics

### Purpose
Create shareable, engaging content optimized for social media platforms.

### Visual Elements
- **Bold headlines**: Attention-grabbing text
- **Minimal text**: Quick to read
- **Vibrant colors**: Stand out in feeds
- **Central visual**: Eye-catching image or icon
- **Call to action**: Engagement prompt

### Layout Patterns
- **Square format**: Instagram, Facebook
- **Vertical format**: Pinterest, Stories
- **Carousel**: Multi-slide series
- **Quote card**: Impactful statement focus

### Platform Dimensions
- **Instagram Square**: 1080x1080px
- **Instagram Portrait**: 1080x1350px
- **Twitter/X**: 1200x675px
- **LinkedIn**: 1200x627px
- **Pinterest**: 1000x1500px

### Prompt Templates

**Social Quote Card:**
```
Social media infographic: Inspirational quote
Quote: "[QUOTE TEXT]"
Attribution: - [AUTHOR]
Large quotation marks, centered quote text,
author name below, [COLOR SCHEME],
Instagram square format, bold typography,
solid gradient background.
```

**Quick Stats Social:**
```
Social media infographic: [TOPIC] in Numbers
Headline: [ATTENTION-GRABBING HEADLINE]
Stat 1: [BIG NUMBER] [CONTEXT]
Stat 2: [BIG NUMBER] [CONTEXT]
Call to action: [CTA]
Bold numbers, minimal text, [COLOR SCHEME],
vibrant engaging design, social media optimized,
Instagram square format.
```

### Example Prompts

**Inspirational Quote:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Social media infographic quote card: \
   Quote: 'The best time to plant a tree was 20 years ago. \
   The second best time is now.' \
   Attribution: Chinese Proverb. \
   Large decorative quotation marks, centered text, \
   gradient background from deep green to teal, \
   tree silhouette illustration, Instagram square format, \
   modern inspirational design" \
  --output figures/tree_quote.png
```

**Engagement Stats:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Social media infographic: Email Marketing Stats \
   Headline: Is Your Email Strategy Working? \
   Stat 1: 4400% ROI on email marketing, \
   Stat 2: 59% of consumers say email influences purchases, \
   Call to action: Double tap if you're an email marketer! \
   Bold colorful numbers, envelope icons, \
   purple and yellow vibrant colors, \
   Instagram square format, engaging design" \
  --output figures/email_stats_social.png
```

---

## Style Variations by Industry

### Corporate/Business Style
- Colors: Navy, gray, gold accents
- Typography: Clean sans-serif (Arial, Helvetica)
- Design: Minimal, professional, structured
- Elements: Charts, icons, clean lines

### Healthcare/Medical Style
- Colors: Blue, teal, green, white
- Typography: Clear, readable
- Design: Trust-inducing, clean, clinical
- Elements: Medical icons, anatomy, research imagery

### Technology/Data Style
- Colors: Dark backgrounds, neon accents, blue/purple
- Typography: Modern sans-serif, monospace for data
- Design: Futuristic, clean, dark mode friendly
- Elements: Circuit patterns, data visualizations, glows

### Education/Academic Style
- Colors: Neutral tones, soft blues, warm accents
- Typography: Readable, slightly traditional
- Design: Organized, clear hierarchy, accessible
- Elements: Books, lightbulbs, graduation icons

### Marketing/Creative Style
- Colors: Bold, vibrant, trendy combinations
- Typography: Mix of display and body fonts
- Design: Eye-catching, dynamic, playful
- Elements: Abstract shapes, gradients, illustrations

---

## Prompt Modifiers Reference

Add these modifiers to any prompt to adjust style:

### Design Style
- "clean minimal design"
- "modern professional design"
- "flat design with bold colors"
- "hand-drawn illustration style"
- "3D isometric style"
- "vintage retro style"
- "corporate business style"
- "playful friendly design"

### Color Instructions
- "[color] and [color] color scheme"
- "monochromatic [color] palette"
- "colorblind-safe palette"
- "warm/cool color tones"
- "high contrast design"
- "muted pastel colors"
- "bold vibrant colors"

### Layout Instructions
- "vertical layout"
- "horizontal layout"
- "centered composition"
- "asymmetrical balance"
- "grid-based layout"
- "flowing organic layout"

### Background Options
- "white background"
- "light gray background"
- "dark background"
- "gradient background from [color] to [color]"
- "subtle pattern background"
- "solid [color] background"

---

Use these templates and examples as starting points, then customize for your specific needs.
