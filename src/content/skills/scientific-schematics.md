---
title: "Scientific Schematics"
description: "Create publication-quality scientific diagrams using Nano Banana 2 AI with smart iterative refinement. Uses Gemini 3.1 Pro Preview for quality review. Only regenerates if quality is below threshold for your document type. Specialized in neural net..."
category: "research"
source: "community"
author: "Community"
tags: ["scientific", "schematics"]
date: 2026-03-20
---

# Scientific Schematics and Diagrams

## Overview

Scientific schematics and diagrams transform complex concepts into clear visual representations for publication. **This skill uses Nano Banana 2 AI for diagram generation with Gemini 3.1 Pro Preview quality review.**

**How it works:**
- Describe your diagram in natural language
- Nano Banana 2 generates publication-quality images automatically
- **Gemini 3.1 Pro Preview reviews quality** against document-type thresholds
- **Smart iteration**: Only regenerates if quality is below threshold
- Publication-ready output in minutes
- No coding, templates, or manual drawing required

**Quality Thresholds by Document Type:**
| Document Type | Threshold | Description |
|---------------|-----------|-------------|
| journal | 8.5/10 | Nature, Science, peer-reviewed journals |
| conference | 8.0/10 | Conference papers |
| thesis | 8.0/10 | Dissertations, theses |
| grant | 8.0/10 | Grant proposals |
| preprint | 7.5/10 | arXiv, bioRxiv, etc. |
| report | 7.5/10 | Technical reports |
| poster | 7.0/10 | Academic posters |
| presentation | 6.5/10 | Slides, talks |
| default | 7.5/10 | General purpose |

**Simply describe what you want, and Nano Banana 2 creates it.** All diagrams are stored in the figures/ subfolder and referenced in papers/posters.

## Quick Start: Generate Any Diagram

Create any scientific diagram by simply describing it. Nano Banana 2 handles everything automatically with **smart iteration**:

```bash
# Generate for journal paper (highest quality threshold: 8.5/10)
python scripts/generate_schematic.py "CONSORT participant flow diagram with 500 screened, 150 excluded, 350 randomized" -o figures/consort.png --doc-type journal

# Generate for presentation (lower threshold: 6.5/10 - faster)
python scripts/generate_schematic.py "Transformer encoder-decoder architecture showing multi-head attention" -o figures/transformer.png --doc-type presentation

# Generate for poster (moderate threshold: 7.0/10)
python scripts/generate_schematic.py "MAPK signaling pathway from EGFR to gene transcription" -o figures/mapk_pathway.png --doc-type poster

# Custom max iterations (max 2)
python scripts/generate_schematic.py "Complex circuit diagram with op-amp, resistors, and capacitors" -o figures/circuit.png --iterations 2 --doc-type journal
```

**What happens behind the scenes:**
1. **Generation 1**: Nano Banana 2 creates initial image following scientific diagram best practices
2. **Review 1**: **Gemini 3.1 Pro Preview** evaluates quality against document-type threshold
3. **Decision**: If quality >= threshold → **DONE** (no more iterations needed!)
4. **If below threshold**: Improved prompt based on critique, regenerate
5. **Repeat**: Until quality meets threshold OR max iterations reached

**Smart Iteration Benefits:**
- ✅ Saves API calls if first generation is good enough
- ✅ Higher quality standards for journal papers
- ✅ Faster turnaround for presentations/posters
- ✅ Appropriate quality for each use case

**Output**: Versioned images plus a detailed review log with quality scores, critiques, and early-stop information.

### Configuration

Set your OpenRouter API key:
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

Get an API key at: https://openrouter.ai/keys

### AI Generation Best Practices

**Effective Prompts for Scientific Diagrams:**

✓ **Good prompts** (specific, detailed):
- "CONSORT flowchart showing participant flow from screening (n=500) through randomization to final analysis"
- "Transformer neural network architecture with encoder stack on left, decoder stack on right, showing multi-head attention and cross-attention connections"
- "Biological signaling cascade: EGFR receptor → RAS → RAF → MEK → ERK → nucleus, with phosphorylation steps labeled"
- "Block diagram of IoT system: sensors → microcontroller → WiFi module → cloud server → mobile app"

✗ **Avoid vague prompts**:
- "Make a flowchart" (too generic)
- "Neural network" (which type? what components?)
- "Pathway diagram" (which pathway? what molecules?)

**Key elements to include:**
- **Type**: Flowchart, architecture diagram, pathway, circuit, etc.
- **Components**: Specific elements to include
- **Flow/Direction**: How elements connect (left-to-right, top-to-bottom)
- **Labels**: Key annotations or text to include
- **Style**: Any specific visual requirements

**Scientific Quality Guidelines** (automatically applied):
- Clean white/light background
- High contrast for readability
- Clear, readable labels (minimum 10pt)
- Professional typography (sans-serif fonts)
- Colorblind-friendly colors (Okabe-Ito palette)
- Proper spacing to prevent crowding
- Scale bars, legends, axes where appropriate

## When to Use This Skill

This skill should be used when:
- Creating neural network architecture diagrams (Transformers, CNNs, RNNs, etc.)
- Illustrating system architectures and data flow diagrams
- Drawing methodology flowcharts for study design (CONSORT, PRISMA)
- Visualizing algorithm workflows and processing pipelines
- Creating circuit diagrams and electrical schematics
- Depicting biological pathways and molecular interactions
- Generating network topologies and hierarchical structures
- Illustrating conceptual frameworks and theoretical models
- Designing block diagrams for technical papers

## How to Use This Skill

**Simply describe your diagram in natural language.** Nano Banana 2 generates it automatically:

```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

**That's it!** The AI handles:
- ✓ Layout and composition
- ✓ Labels and annotations
- ✓ Colors and styling
- ✓ Quality review and refinement
- ✓ Publication-ready output

**Works for all diagram types:**
- Flowcharts (CONSORT, PRISMA, etc.)
- Neural network architectures
- Biological pathways
- Circuit diagrams
- System architectures
- Block diagrams
- Any scientific visualization

**No coding, no templates, no manual drawing required.**

---

# AI Generation Mode (Nano Banana 2 + Gemini 3.1 Pro Preview Review)

## Smart Iterative Refinement Workflow

The AI generation system uses **smart iteration** - it only regenerates if quality is below the threshold for your document type:

### How Smart Iteration Works

```
┌─────────────────────────────────────────────────────┐
│  1. Generate image with Nano Banana 2             │
│                    ↓                                │
│  2. Review quality with Gemini 3.1 Pro Preview                │
│                    ↓                                │
│  3. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 1            │
│                    ↓                                │
│  4. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### Iteration 1: Initial Generation
**Prompt Construction:**
```
Scientific diagram guidelines + User request
```

**Output:** `diagram_v1.png`

### Quality Review by Gemini 3.1 Pro Preview

Gemini 3.1 Pro Preview evaluates the diagram on:
1. **Scientific Accuracy** (0-2 points) - Correct concepts, notation, relationships
2. **Clarity and Readability** (0-2 points) - Easy to understand, clear hierarchy
3. **Label Quality** (0-2 points) - Complete, readable, consistent labels
4. **Layout and Composition** (0-2 points) - Logical flow, balanced, no overlaps
5. **Professional Appearance** (0-2 points) - Publication-ready quality

**Example Review Output:**
```
SCORE: 8.0

STRENGTHS:
- Clear flow from top to bottom
- All phases properly labeled
- Professional typography

ISSUES:
- Participant counts slightly small
- Minor overlap on exclusion box

VERDICT: ACCEPTABLE (for poster, threshold 7.0)
```

### Decision Point: Continue or Stop?

| If Score... | Action |
|-------------|--------|
| >= threshold | **STOP** - Quality is good enough for this document type |
| < threshold | Continue to next iteration with improved prompt |

**Example:**
- For a **poster** (threshold 7.0): Score of 7.5 → **DONE after 1 iteration!**
- For a **journal** (threshold 8.5): Score of 7.5 → Continue improving

### Subsequent Iterations (Only If Needed)

If quality is below threshold, the system:
1. Extracts specific issues from Gemini 3.1 Pro Preview's review
2. Enhances the prompt with improvement instructions
3. Regenerates with Nano Banana 2
4. Reviews again with Gemini 3.1 Pro Preview
5. Repeats until threshold met or max iterations reached

### Review Log
All iterations are saved with a JSON review log that includes early-stop information:
```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "doc_type": "poster",
  "quality_threshold": 7.0,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.5,
      "needs_improvement": false,
      "critique": "SCORE: 7.5\nSTRENGTHS:..."
    }
  ],
  "final_score": 7.5,
  "early_stop": true,
  "early_stop_reason": "Quality score 7.5 meets threshold 7.0 for poster"
}
```

**Note:** With smart iteration, you may see only 1 iteration instead of the full 2 if quality is achieved early!

## Advanced AI Generation Usage

### Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize generator
generator = ScientificSchematicGenerator(
    api_key="your_openrouter_key",
    verbose=True
)

# Generate with iterative refinement (max 2 iterations)
results = generator.generate_iterative(
    user_prompt="Transformer architecture diagram",
    output_path="figures/transformer.png",
    iterations=2
)

# Access results
print(f"Final score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review individual iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"Critique: {iteration['critique']}")
```

### Command-Line Options

```bash
# Basic usage (default threshold 7.5/10)
python scripts/generate_schematic.py "diagram description" -o output.png

# Specify document type for appropriate quality threshold
python scripts/generate_schematic.py "diagram" -o out.png --doc-type journal      # 8.5/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type conference   # 8.0/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type poster       # 7.0/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type presentation # 6.5/10

# Custom max iterations (1-2)
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 2

# Verbose output (see all API calls and reviews)
python scripts/generate_schematic.py "flowchart" -o flow.png -v

# Provide API key via flag
python scripts/generate_schematic.py "diagram" -o out.png --api-key "sk-or-v1-..."

# Combine options
python scripts/generate_schematic.py "neural network" -o nn.png --doc-type journal --iterations 2 -v
```

### Prompt Engineering Tips

**1. Be Specific About Layout:**
```
✓ "Flowchart with vertical flow, top to bottom"
✓ "Architecture diagram with encoder on left, decoder on right"
✓ "Circular pathway diagram with clockwise flow"
```

**2. Include Quantitative Details:**
```
✓ "Neural network with input layer (784 nodes), hidden layer (128 nodes), output (10 nodes)"
✓ "Flowchart showing n=500 screened, n=150 excluded, n=350 randomized"
✓ "Circuit with 1kΩ resistor, 10µF capacitor, 5V source"
```

**3. Specify Visual Style:**
```
✓ "Minimalist block diagram with clean lines"
✓ "Detailed biological pathway with protein structures"
✓ "Technical schematic with engineering notation"
```

**4. Request Specific Labels:**
```
✓ "Label all arrows with activation/inhibition"
✓ "Include layer dimensions in each box"
✓ "Show time progression with timestamps"
```

**5. Mention Color Requirements:**
```
✓ "Use colorblind-friendly colors"
✓ "Grayscale-compatible design"
✓ "Color-code by function: blue for input, green for processing, red for output"
```

## AI Generation Examples

### Example 1: CONSORT Flowchart
```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for randomized controlled trial. \
   Start with 'Assessed for eligibility (n=500)' at top. \
   Show 'Excluded (n=150)' with reasons: age<18 (n=80), declined (n=50), other (n=20). \
   Then 'Randomized (n=350)' splits into two arms: \
   'Treatment group (n=175)' and 'Control group (n=175)'. \
   Each arm shows 'Lost to follow-up' (n=15 and n=10). \
   End with 'Analyzed' (n=160 and n=165). \
   Use blue boxes for process steps, orange for exclusion, green for final analysis." \
  -o figures/consort.png
```

### Example 2: Neural Network Architecture
```bash
python scripts/generate_schematic.py \
  "Transformer encoder-decoder architecture diagram. \
   Left side: Encoder stack with input embedding, positional encoding, \
   multi-head self-attention, add & norm, feed-forward, add & norm. \
   Right side: Decoder stack with output embedding, positional encoding, \
   masked self-attention, add & norm, cross-attention (receiving from encoder), \
   add & norm, feed-forward, add & norm, linear & softmax. \
   Show cross-attention connection from encoder to decoder with dashed line. \
   Use light blue for encoder, light red for decoder. \
   Label all components clearly." \
  -o figures/transformer.png --iterations 2
```

### Example 3: Biological Pathway
```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway diagram. \
   Start with EGFR receptor at cell membrane (top). \
   Arrow down to RAS (with GTP label). \
   Arrow to RAF kinase. \
   Arrow to MEK kinase. \
   Arrow to ERK kinase. \
   Final arrow to nucleus showing gene transcription. \
   Label each arrow with 'phosphorylation' or 'activation'. \
   Use rounded rectangles for proteins, different colors for each. \
   Include membrane boundary line at top." \
  -o figures/mapk_pathway.png
```

### Example 4: System Architecture
```bash
python scripts/generate_schematic.py \
  "IoT system architecture block diagram. \
   Bottom layer: Sensors (temperature, humidity, motion) in green boxes. \
   Middle layer: Microcontroller (ESP32) in blue box. \
   Connections to WiFi module (orange box) and Display (purple box). \
   Top layer: Cloud server (gray box) connected to mobile app (light blue box). \
   Show data flow arrows between all components. \
   Label connections with protocols: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_architecture.png
```

---

## Command-Line Usage

The main entry point for generating scientific schematics:

```bash
# Basic usage
python scripts/generate_schematic.py "diagram description" -o output.png

# Custom iterations (max 2)
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 2

# Verbose mode
python scripts/generate_schematic.py "diagram" -o out.png -v
```

**Note:** The Nano Banana 2 AI generation system includes automatic quality review in its iterative refinement process. Each iteration is evaluated for scientific accuracy, clarity, and accessibility.

## Best Practices Summary

### Design Principles

1. **Clarity over complexity** - Simplify, remove unnecessary elements
2. **Consistent styling** - Use templates and style files
3. **Colorblind accessibility** - Use Okabe-Ito palette, redundant encoding
4. **Appropriate typography** - Sans-serif fonts, minimum 7-8 pt
5. **Vector format** - Always use PDF/SVG for publication

### Technical Requirements

1. **Resolution** - Vector preferred, or 300+ DPI for raster
2. **File format** - PDF for LaTeX, SVG for web, PNG as fallback
3. **Color space** - RGB for digital, CMYK for print (convert if needed)
4. **Line weights** - Minimum 0.5 pt, typical 1-2 pt
5. **Text size** - 7-8 pt minimum at final size

### Integration Guidelines

1. **Include in LaTeX** - Use `\includegraphics{}` for generated images
2. **Caption thoroughly** - Describe all elements and abbreviations
3. **Reference in text** - Explain diagram in narrative flow
4. **Maintain consistency** - Same style across all figures in paper
5. **Version control** - Keep prompts and generated images in repository

## Troubleshooting Common Issues

### AI Generation Issues

**Problem**: Overlapping text or elements
- **Solution**: AI generation automatically handles spacing
- **Solution**: Increase iterations: `--iterations 2` for better refinement

**Problem**: Elements not connecting properly
- **Solution**: Make your prompt more specific about connections and layout
- **Solution**: Increase iterations for better refinement

### Image Quality Issues

**Problem**: Export quality poor
- **Solution**: AI generation produces high-quality images automatically
- **Solution**: Increase iterations for better results: `--iterations 2`

**Problem**: Elements overlap after generation
- **Solution**: AI generation automatically handles spacing
- **Solution**: Increase iterations: `--iterations 2` for better refinement
- **Solution**: Make your prompt more specific about layout and spacing requirements

### Quality Check Issues

**Problem**: False positive overlap detection
- **Solution**: Adjust threshold: `detect_overlaps(image_path, threshold=0.98)`
- **Solution**: Manually review flagged regions in visual report

**Problem**: Generated image quality is low
- **Solution**: AI generation produces high-quality images by default
- **Solution**: Increase iterations for better results: `--iterations 2`

**Problem**: Colorblind simulation shows poor contrast
- **Solution**: Switch to Okabe-Ito palette explicitly in code
- **Solution**: Add redundant encoding (shapes, patterns, line styles)
- **Solution**: Increase color saturation and lightness differences

**Problem**: High-severity overlaps detected
- **Solution**: Review overlap_report.json for exact positions
- **Solution**: Increase spacing in those specific regions
- **Solution**: Re-run with adjusted parameters and verify again

**Problem**: Visual report generation fails
- **Solution**: Check Pillow and matplotlib installations
- **Solution**: Ensure image file is readable: `Image.open(path).verify()`
- **Solution**: Check sufficient disk space for report generation

### Accessibility Problems

**Problem**: Colors indistinguishable in grayscale
- **Solution**: Run accessibility checker: `verify_accessibility(image_path)`
- **Solution**: Add patterns, shapes, or line styles for redundancy
- **Solution**: Increase contrast between adjacent elements

**Problem**: Text too small when printed
- **Solution**: Run resolution validator: `validate_resolution(image_path)`
- **Solution**: Design at final size, use minimum 7-8 pt fonts
- **Solution**: Check physical dimensions in resolution report

**Problem**: Accessibility checks consistently fail
- **Solution**: Review accessibility_report.json for specific failures
- **Solution**: Increase color contrast by at least 20%
- **Solution**: Test with actual grayscale conversion before finalizing

## Resources and References

### Detailed References

Load these files for comprehensive information on specific topics:

- **`references/diagram_types.md`** - Catalog of scientific diagram types with examples
- **`references/best_practices.md`** - Publication standards and accessibility guidelines

### External Resources

**Python Libraries**
- Schemdraw Documentation: https://schemdraw.readthedocs.io/
- NetworkX Documentation: https://networkx.org/documentation/
- Matplotlib Documentation: https://matplotlib.org/

**Publication Standards**
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- CONSORT Diagram: http://www.consort-statement.org/consort-statement/flow-diagram

## Integration with Other Skills

This skill works synergistically with:

- **Scientific Writing** - Diagrams follow figure best practices
- **Scientific Visualization** - Shares color palettes and styling
- **LaTeX Posters** - Generate diagrams for poster presentations
- **Research Grants** - Methodology diagrams for proposals
- **Peer Review** - Evaluate diagram clarity and accessibility

## Quick Reference Checklist

Before submitting diagrams, verify:

### Visual Quality
- [ ] High-quality image format (PNG from AI generation)
- [ ] No overlapping elements (AI handles automatically)
- [ ] Adequate spacing between all components (AI optimizes)
- [ ] Clean, professional alignment
- [ ] All arrows connect properly to intended targets

### Accessibility
- [ ] Colorblind-safe palette (Okabe-Ito) used
- [ ] Works in grayscale (tested with accessibility checker)
- [ ] Sufficient contrast between elements (verified)
- [ ] Redundant encoding where appropriate (shapes + colors)
- [ ] Colorblind simulation passes all checks

### Typography and Readability
- [ ] Text minimum 7-8 pt at final size
- [ ] All elements labeled clearly and completely
- [ ] Consistent font family and sizing
- [ ] No text overlaps or cutoffs
- [ ] Units included where applicable

### Publication Standards
- [ ] Consistent styling with other figures in manuscript
- [ ] Comprehensive caption written with all abbreviations defined
- [ ] Referenced appropriately in manuscript text
- [ ] Meets journal-specific dimension requirements
- [ ] Exported in required format for journal (PDF/EPS/TIFF)

### Quality Verification (Required)
- [ ] Ran `run_quality_checks()` and achieved PASS status
- [ ] Reviewed overlap detection report (zero high-severity overlaps)
- [ ] Passed accessibility verification (grayscale and colorblind)
- [ ] Resolution validated at target DPI (300+ for print)
- [ ] Visual quality report generated and reviewed
- [ ] All quality reports saved with figure files

### Documentation and Version Control
- [ ] Source files (.tex, .py) saved for future revision
- [ ] Quality reports archived in `quality_reports/` directory
- [ ] Configuration parameters documented (colors, spacing, sizes)
- [ ] Git commit includes source, output, and quality reports
- [ ] README or comments explain how to regenerate figure

### Final Integration Check
- [ ] Figure displays correctly in compiled manuscript
- [ ] Cross-references work (`\ref{}` points to correct figure)
- [ ] Figure number matches text citations
- [ ] Caption appears on correct page relative to figure
- [ ] No compilation warnings or errors related to figure

## Environment Setup

```bash
# Required
export OPENROUTER_API_KEY='your_api_key_here'

# Get key at: https://openrouter.ai/keys
```

## Getting Started

**Simplest possible usage:**
```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

---

Use this skill to create clear, accessible, publication-quality diagrams that effectively communicate complex scientific concepts. The AI-powered workflow with iterative refinement ensures diagrams meet professional standards.

---

## Reference: Quick_Reference

# Scientific Schematics - Quick Reference

**How it works:** Describe your diagram → Nano Banana 2 generates it automatically

## Setup (One-Time)

```bash
# Get API key from https://openrouter.ai/keys
export OPENROUTER_API_KEY='sk-or-v1-your_key_here'

# Add to shell profile for persistence
echo 'export OPENROUTER_API_KEY="sk-or-v1-your_key"' >> ~/.bashrc  # or ~/.zshrc
```

## Basic Usage

```bash
# Describe your diagram, Nano Banana 2 creates it
python scripts/generate_schematic.py "your diagram description" -o output.png

# That's it! Automatic:
# - Iterative refinement (3 rounds)
# - Quality review and improvement
# - Publication-ready output
```

## Common Examples

### CONSORT Flowchart
```bash
python scripts/generate_schematic.py \
  "CONSORT flow: screened n=500, excluded n=150, randomized n=350" \
  -o consort.png
```

### Neural Network
```bash
python scripts/generate_schematic.py \
  "Transformer architecture with encoder and decoder stacks" \
  -o transformer.png
```

### Biological Pathway
```bash
python scripts/generate_schematic.py \
  "MAPK pathway: EGFR → RAS → RAF → MEK → ERK" \
  -o mapk.png
```

### Circuit Diagram
```bash
python scripts/generate_schematic.py \
  "Op-amp circuit with 1kΩ resistor and 10µF capacitor" \
  -o circuit.png
```

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o, --output` | Output file path | `-o figures/diagram.png` |
| `--iterations N` | Number of refinements (1-2) | `--iterations 2` |
| `-v, --verbose` | Show detailed output | `-v` |
| `--api-key KEY` | Provide API key | `--api-key sk-or-v1-...` |

## Prompt Tips

### ✓ Good Prompts (Specific)
- "CONSORT flowchart with screening (n=500), exclusion (n=150), randomization (n=350)"
- "Transformer architecture: encoder on left with 6 layers, decoder on right, cross-attention connections"
- "MAPK signaling: receptor → RAS → RAF → MEK → ERK → nucleus, label each phosphorylation"

### ✗ Avoid (Too Vague)
- "Make a flowchart"
- "Neural network"
- "Pathway diagram"

## Output Files

For input `diagram.png`, you get:
- `diagram_v1.png` - First iteration
- `diagram_v2.png` - Second iteration  
- `diagram_v3.png` - Final iteration
- `diagram.png` - Copy of final
- `diagram_review_log.json` - Quality scores and critiques

## Review Log

```json
{
  "iterations": [
    {
      "iteration": 1,
      "score": 7.0,
      "critique": "Good start. Font too small..."
    },
    {
      "iteration": 2,
      "score": 8.5,
      "critique": "Much improved. Minor spacing issues..."
    },
    {
      "iteration": 3,
      "score": 9.5,
      "critique": "Excellent. Publication ready."
    }
  ],
  "final_score": 9.5
}
```

## Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize
gen = ScientificSchematicGenerator(api_key="your_key")

# Generate
results = gen.generate_iterative(
    user_prompt="diagram description",
    output_path="output.png",
    iterations=2
)

# Check quality
print(f"Score: {results['final_score']}/10")
```

## Troubleshooting

### API Key Not Found
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY='your_key'
```

### Import Error
```bash
# Install requests
pip install requests
```

### Low Quality Score
- Make prompt more specific
- Include layout details (left-to-right, top-to-bottom)
- Specify label requirements
- Increase iterations: `--iterations 2`

## Testing

```bash
# Verify installation
python test_ai_generation.py

# Should show: "6/6 tests passed"
```

## Cost

Typical cost per diagram (max 2 iterations):
- Simple (1 iteration): $0.05-0.15
- Complex (2 iterations): $0.10-0.30

## How Nano Banana 2 Works

**Simply describe your diagram in natural language:**
- ✓ No coding required
- ✓ No templates needed
- ✓ No manual drawing
- ✓ Automatic quality review
- ✓ Publication-ready output
- ✓ Works for any diagram type

**Just describe what you want, and it's generated automatically.**

## Getting Help

```bash
# Show help
python scripts/generate_schematic.py --help

# Verbose mode for debugging
python scripts/generate_schematic.py "diagram" -o out.png -v
```

## Quick Start Checklist

- [ ] Set `OPENROUTER_API_KEY` environment variable
- [ ] Run `python test_ai_generation.py` (should pass 6/6)
- [ ] Try: `python scripts/generate_schematic.py "test diagram" -o test.png`
- [ ] Review output files (test_v1.png, v2, v3, review_log.json)
- [ ] Read SKILL.md for detailed documentation
- [ ] Check README.md for examples

## Resources

- Full documentation: `SKILL.md`
- Detailed guide: `README.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Example script: `example_usage.sh`
- Get API key: https://openrouter.ai/keys

---

## Reference: Readme

# Scientific Schematics - Nano Banana 2

**Generate any scientific diagram by describing it in natural language.**

Nano Banana 2 creates publication-quality diagrams automatically - no coding, no templates, no manual drawing required.

## Quick Start

### Generate Any Diagram

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY='your_api_key_here'

# Generate any scientific diagram
python scripts/generate_schematic.py "CONSORT participant flow diagram" -o figures/consort.png

# Neural network architecture
python scripts/generate_schematic.py "Transformer encoder-decoder architecture" -o figures/transformer.png

# Biological pathway
python scripts/generate_schematic.py "MAPK signaling pathway" -o figures/pathway.png
```

### What You Get

- **Up to two iterations** (v1, v2) with progressive refinement
- **Automatic quality review** after each iteration
- **Detailed review log** with scores and critiques (JSON format)
- **Publication-ready images** following scientific standards

## Features

### Iterative Refinement Process

1. **Generation 1**: Create initial diagram from your description
2. **Review 1**: AI evaluates clarity, labels, accuracy, accessibility
3. **Generation 2**: Improve based on critique
4. **Review 2**: Second evaluation with specific feedback
5. **Generation 3**: Final polished version

### Automatic Quality Standards

All diagrams automatically follow:
- Clean white/light background
- High contrast for readability
- Clear labels (minimum 10pt font)
- Professional typography
- Colorblind-friendly colors
- Proper spacing between elements
- Scale bars, legends, axes where appropriate

## Installation

### For AI Generation

```bash
# Get OpenRouter API key
# Visit: https://openrouter.ai/keys

# Set environment variable
export OPENROUTER_API_KEY='sk-or-v1-...'

# Or add to .env file
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> .env

# Install Python dependencies (if not already installed)
pip install requests
```

## Usage Examples

### Example 1: CONSORT Flowchart

```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for RCT. \
   Assessed for eligibility (n=500). \
   Excluded (n=150): age<18 (n=80), declined (n=50), other (n=20). \
   Randomized (n=350) into Treatment (n=175) and Control (n=175). \
   Lost to follow-up: 15 and 10 respectively. \
   Final analysis: 160 and 165." \
  -o figures/consort.png
```

**Output:**
- `figures/consort_v1.png` - Initial generation
- `figures/consort_v2.png` - After first review
- `figures/consort_v3.png` - Final version
- `figures/consort.png` - Copy of final version
- `figures/consort_review_log.json` - Detailed review log

### Example 2: Neural Network Architecture

```bash
python scripts/generate_schematic.py \
  "Transformer architecture with encoder on left (input embedding, \
   positional encoding, multi-head attention, feed-forward) and \
   decoder on right (masked attention, cross-attention, feed-forward). \
   Show cross-attention connection from encoder to decoder." \
  -o figures/transformer.png \
  --iterations 2
```

### Example 3: Biological Pathway

```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway: EGFR receptor → RAS → RAF → MEK → ERK → nucleus. \
   Label each step with phosphorylation. Use different colors for each kinase." \
  -o figures/mapk.png
```

### Example 4: System Architecture

```bash
python scripts/generate_schematic.py \
  "IoT system block diagram: sensors (bottom) → microcontroller → \
   WiFi module and display (middle) → cloud server → mobile app (top). \
   Label all connections with protocols." \
  -o figures/iot_system.png
```

## Command-Line Options

```bash
python scripts/generate_schematic.py [OPTIONS] "description" -o output.png

Options:
  --iterations N          Number of AI refinement iterations (default: 2, max: 2)
  --api-key KEY          OpenRouter API key (or use env var)
  -v, --verbose          Verbose output
  -h, --help             Show help message
```

## Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize
generator = ScientificSchematicGenerator(
    api_key="your_key",
    verbose=True
)

# Generate with iterative refinement
results = generator.generate_iterative(
    user_prompt="CONSORT flowchart",
    output_path="figures/consort.png",
    iterations=2
)

# Access results
print(f"Final score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"Critique: {iteration['critique']}")
```

## Prompt Engineering Tips

### Be Specific About Layout
✓ "Flowchart with vertical flow, top to bottom"  
✓ "Architecture diagram with encoder on left, decoder on right"  
✗ "Make a diagram" (too vague)

### Include Quantitative Details
✓ "Neural network: input (784), hidden (128), output (10)"  
✓ "Flowchart: n=500 screened, n=150 excluded, n=350 randomized"  
✗ "Some numbers" (not specific)

### Specify Visual Style
✓ "Minimalist block diagram with clean lines"  
✓ "Detailed biological pathway with protein structures"  
✓ "Technical schematic with engineering notation"

### Request Specific Labels
✓ "Label all arrows with activation/inhibition"  
✓ "Include layer dimensions in each box"  
✓ "Show time progression with timestamps"

### Mention Color Requirements
✓ "Use colorblind-friendly colors"  
✓ "Grayscale-compatible design"  
✓ "Color-code by function: blue=input, green=processing, red=output"

## Review Log Format

Each generation produces a JSON review log:

```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "prompt": "Full generation prompt...",
      "critique": "Score: 7/10. Issues: font too small...",
      "score": 7.0,
      "success": true
    },
    {
      "iteration": 2,
      "image_path": "figures/consort_v2.png",
      "score": 8.5,
      "critique": "Much improved. Remaining issues..."
    },
    {
      "iteration": 3,
      "image_path": "figures/consort_v3.png",
      "score": 9.5,
      "critique": "Excellent. Publication ready."
    }
  ],
  "final_image": "figures/consort_v3.png",
  "final_score": 9.5,
  "success": true
}
```

## Why Use Nano Banana 2

**Simply describe what you want - Nano Banana 2 creates it:**

- ✓ **Fast**: Results in minutes
- ✓ **Easy**: Natural language descriptions (no coding)
- ✓ **Quality**: Automatic review and refinement
- ✓ **Universal**: Works for all diagram types
- ✓ **Publication-ready**: High-quality output immediately

**Just describe your diagram, and it's generated automatically.**

## Troubleshooting

### API Key Issues

```bash
# Check if key is set
echo $OPENROUTER_API_KEY

# Set temporarily
export OPENROUTER_API_KEY='your_key'

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENROUTER_API_KEY="your_key"' >> ~/.bashrc
```

### Import Errors

```bash
# Install requests library
pip install requests

# Or use the package manager
pip install -r requirements.txt
```

### Generation Fails

```bash
# Use verbose mode to see detailed errors
python scripts/generate_schematic.py "diagram" -o out.png -v

# Check API status
curl https://openrouter.ai/api/v1/models
```

### Low Quality Scores

If iterations consistently score below 7/10:
1. Make your prompt more specific
2. Include more details about layout and labels
3. Specify visual requirements explicitly
4. Increase iterations: `--iterations 2`

## Testing

Run verification tests:

```bash
python test_ai_generation.py
```

This tests:
- File structure
- Module imports
- Class initialization
- Error handling
- Prompt engineering
- Wrapper script

## Cost Considerations

OpenRouter pricing for models used:
- **Nano Banana 2**: ~$2/M input tokens, ~$12/M output tokens

Typical costs per diagram:
- Simple diagram (1 iteration): ~$0.05-0.15
- Complex diagram (2 iterations): ~$0.10-0.30

## Examples Gallery

See the full SKILL.md for extensive examples including:
- CONSORT flowcharts
- Neural network architectures (Transformers, CNNs, RNNs)
- Biological pathways
- Circuit diagrams
- System architectures
- Block diagrams

## Support

For issues or questions:
1. Check SKILL.md for detailed documentation
2. Run test_ai_generation.py to verify setup
3. Use verbose mode (-v) to see detailed errors
4. Review the review_log.json for quality feedback

## License

Part of the scientific-writer package. See main repository for license information.

---

## Reference: Best_Practices

# Best Practices for Scientific Diagrams

## Overview

This guide provides publication standards, accessibility guidelines, and best practices for creating high-quality scientific diagrams that meet journal requirements and communicate effectively to all readers.

## Publication Standards

### 1. File Format Requirements

**Vector Formats (Preferred)**
- **PDF**: Universal acceptance, preserves quality, works with LaTeX
  - Use for: Line drawings, flowcharts, block diagrams, circuit diagrams
  - Advantages: Scalable, small file size, embeds fonts
  - Standard for LaTeX workflows

- **EPS (Encapsulated PostScript)**: Legacy format, still accepted
  - Use for: Older publishing systems
  - Compatible with most journals
  - Can be converted from PDF

- **SVG (Scalable Vector Graphics)**: Web-friendly, increasingly accepted
  - Use for: Online publications, interactive figures
  - Can be edited in vector graphics software
  - Not all journals accept SVG

**Raster Formats (When Necessary)**
- **TIFF**: Professional standard for raster graphics
  - Use for: Microscopy images, photographs combined with diagrams
  - Minimum 300 DPI at final print size
  - Lossless compression (LZW)

- **PNG**: Web-friendly, lossless compression
  - Use for: Online supplementary materials, presentations
  - Minimum 300 DPI for print
  - Supports transparency

**Never Use**
- **JPEG**: Lossy compression creates artifacts in diagrams
- **GIF**: Limited colors, inappropriate for scientific figures
- **BMP**: Uncompressed, unnecessarily large files

### 2. Resolution Requirements

**Vector Graphics**
- Infinite resolution (scalable)
- **Recommended**: Always use vector when possible

**Raster Graphics (when vector not possible)**
- **Publication quality**: 300-600 DPI
- **Line art**: 600-1200 DPI
- **Web/screen**: 150 DPI acceptable
- **Never**: Below 300 DPI for print

**Calculating DPI**
```
DPI = pixels / (inches at final size)

Example:
Image size: 2400 × 1800 pixels
Final print size: 8 × 6 inches
DPI = 2400 / 8 = 300 ✓ (acceptable)
```

### 3. Size and Dimensions

**Journal-Specific Column Widths**
- **Nature**: Single column 89 mm (3.5 in), Double 183 mm (7.2 in)
- **Science**: Single column 55 mm (2.17 in), Double 120 mm (4.72 in)
- **Cell**: Single column 85 mm (3.35 in), Double 178 mm (7 in)
- **PLOS**: Single column 83 mm (3.27 in), Double 173 mm (6.83 in)
- **IEEE**: Single column 3.5 in, Double 7.16 in

**Best Practices**
- Design at final print size (avoid scaling)
- Use journal templates when available
- Allow margins for cropping
- Test appearance at final size before submission

### 4. Typography Standards

**Font Selection**
- **Recommended**: Arial, Helvetica, Calibri (sans-serif)
- **Acceptable**: Times New Roman (serif) for mathematics-heavy
- **Avoid**: Decorative fonts, script fonts, system fonts that may not embed

**Font Sizes (at final print size)**
- **Minimum**: 6-7 pt (journal dependent)
- **Axis labels**: 8-9 pt
- **Figure labels**: 10-12 pt
- **Panel labels (A, B, C)**: 10-14 pt, bold
- **Main text**: Should match manuscript body text

**Text Clarity**
- Use sentence case: "Time (seconds)" not "TIME (SECONDS)"
- Include units in parentheses: "Temperature (°C)"
- Spell out abbreviations in figure caption
- Avoid rotated text when possible (exception: y-axis labels)
- **No figure numbers in diagram** - do not include "Figure 1:", "Fig. 1", etc. (these are added by LaTeX/document)

### 5. Line Weights and Strokes

**Recommended Line Widths**
- **Diagram outlines**: 0.5-1.0 pt
- **Connection lines/arrows**: 1.0-2.0 pt
- **Emphasis elements**: 2.0-3.0 pt
- **Minimum visible**: 0.25 pt at final size

**Consistency**
- Use same line weight for similar elements
- Vary line weight to show hierarchy
- Avoid hairline rules (too thin to print reliably)

## Accessibility and Colorblindness

### 1. Colorblind-Safe Palettes

**Okabe-Ito Palette (Recommended)**
Most distinguishable by all types of colorblindness:

```latex
% RGB values
Orange:     #E69F00 (230, 159,   0)
Sky Blue:   #56B4E9 ( 86, 180, 233)
Green:      #009E73 (  0, 158, 115)
Yellow:     #F0E442 (240, 228,  66)
Blue:       #0072B2 (  0, 114, 178)
Vermillion: #D55E00 (213,  94,   0)
Purple:     #CC79A7 (204, 121, 167)
Black:      #000000 (  0,   0,   0)
```

**Alternative: ColorBrewer Palettes**
- **Qualitative**: Set2, Paired, Dark2
- **Sequential**: Blues, Greens, Oranges (avoid Reds/Greens together)
- **Diverging**: RdBu (Red-Blue), PuOr (Purple-Orange)

**Colors to Avoid Together**
- Red-Green combinations (8% of males cannot distinguish)
- Blue-Purple combinations
- Yellow-Light green combinations

### 2. Redundant Encoding

Don't rely on color alone. Use multiple visual channels:

**Shape + Color**
```
Circle + Blue   = Condition A
Square + Orange = Condition B
Triangle + Green = Condition C
```

**Line Style + Color**
```
Solid + Blue = Treatment 1
Dashed + Orange = Treatment 2
Dotted + Green = Control
```

**Pattern Fill + Color**
```
Solid fill + Blue = Group A
Diagonal stripes + Orange = Group B
Cross-hatch + Green = Group C
```

### 3. Grayscale Compatibility

**Test Requirement**: All diagrams must be interpretable in grayscale

**Strategies**
- Use different shades (light, medium, dark)
- Add patterns or textures to filled areas
- Vary line styles (solid, dashed, dotted)
- Use labels directly on elements
- Include text annotations

**Grayscale Test**
```bash
# Convert to grayscale to test
convert diagram.pdf -colorspace gray diagram_gray.pdf
```

### 4. Contrast Requirements

**Minimum Contrast Ratios (WCAG Guidelines)**
- **Normal text**: 4.5:1
- **Large text** (≥18pt): 3:1
- **Graphical elements**: 3:1

**High Contrast Practices**
- Dark text on light background (or vice versa)
- Avoid low-contrast color pairs (yellow on white, light gray on white)
- Use black or dark gray for critical text
- White text on dark backgrounds needs larger font size

### 5. Alternative Text and Descriptions

**Figure Captions Must Include**
- Description of diagram type
- All abbreviations spelled out
- Explanation of symbols and colors
- Sample sizes (n) where relevant
- Statistical annotations explained
- Reference to detailed methods if applicable

**Example Caption**
"Participant flow diagram following CONSORT guidelines. Rectangles represent study stages, with participant numbers (n) shown. Exclusion criteria are listed beside each screening stage. Final analysis included n=350 participants across two groups."

## Design Principles

### 1. Simplicity and Clarity

**Occam's Razor for Diagrams**
- Remove every element that doesn't add information
- Simplify complex relationships
- Break complex diagrams into multiple panels
- Use consistent layouts across related figures

**Visual Hierarchy**
- Most important elements: Largest, darkest, central
- Supporting elements: Smaller, lighter, peripheral
- Annotations: Minimal, clear labels only

### 2. Consistency

**Within a Figure**
- Same shape/color represents same concept
- Consistent arrow styles for same relationships
- Uniform spacing and alignment
- Matching font sizes for similar elements

**Across Figures in a Paper**
- Reuse color schemes
- Maintain consistent node styles
- Use same notation system
- Apply same layout principles

### 3. Professional Appearance

**Alignment**
- Use grids for node placement
- Align nodes horizontally or vertically
- Evenly space elements
- Center labels within shapes

**White Space**
- Don't overcrowd diagrams
- Leave breathing room around elements
- Use white space to group related items
- Margins around entire diagram

**Polish**
- No jagged lines or misaligned elements
- Smooth curves and precise angles
- Clean connection points
- No overlapping text

## Common Pitfalls and Solutions

### Pitfall 1: Overcomplicated Diagrams

**Problem**: Too much information in one diagram
**Solution**: 
- Split into multiple panels (A, B, C)
- Create overview + detailed diagrams
- Move details to supplementary figures
- Use hierarchical presentation

### Pitfall 2: Inconsistent Styling

**Problem**: Different styles for same elements across figures
**Solution**:
- Create and use style templates
- Use the same color palette throughout
- Document your style choices

### Pitfall 3: Poor Label Placement

**Problem**: Labels overlap elements or are hard to read
**Solution**:
- Place labels outside shapes when possible
- Use leader lines for distant labels
- Rotate text only when necessary
- Ensure adequate contrast with background

### Pitfall 4: Tiny Text

**Problem**: Text too small to read at final print size
**Solution**:
- Design at final size from the start
- Test print at final size
- Minimum 7-8 pt font
- Simplify labels if space is limited

### Pitfall 5: Ambiguous Arrows

**Problem**: Unclear what arrows represent or where they point
**Solution**:
- Use different arrow styles for different meanings
- Add labels to arrows
- Include legend for arrow types
- Use anchor points for precise connections

### Pitfall 6: Color Overuse

**Problem**: Too many colors, confusing or inaccessible
**Solution**:
- Limit to 3-5 colors maximum
- Use color purposefully (categories, emphasis)
- Stick to colorblind-safe palette
- Provide redundant encoding

## Quality Control Checklist

### Before Submission

**Technical Requirements**
- [ ] Correct file format (PDF/EPS preferred for diagrams)
- [ ] Sufficient resolution (vector or 300+ DPI)
- [ ] Appropriate size (matches journal column width)
- [ ] Fonts embedded in PDF
- [ ] No compression artifacts

**Accessibility**
- [ ] Colorblind-safe palette used
- [ ] Works in grayscale (tested)
- [ ] Text minimum 7-8 pt at final size
- [ ] High contrast between elements
- [ ] Redundant encoding (not color alone)

**Design Quality**
- [ ] Elements aligned properly
- [ ] Consistent spacing and layout
- [ ] No overlapping text or elements
- [ ] Clear visual hierarchy
- [ ] Professional appearance

**Content**
- [ ] All elements labeled
- [ ] Abbreviations defined
- [ ] Units included where relevant
- [ ] Legend provided if needed
- [ ] Caption comprehensive

**Consistency**
- [ ] Matches other figures in style
- [ ] Same notation as text
- [ ] Consistent with journal guidelines
- [ ] Cross-references work

## Journal-Specific Guidelines

### Nature

**Figure Requirements**
- **Size**: 89 mm (single) or 183 mm (double column)
- **Format**: PDF, EPS, or high-res TIFF
- **Fonts**: Sans-serif preferred
- **File size**: <10 MB per file
- **Resolution**: 300 DPI minimum for raster

**Style Notes**
- Panel labels: lowercase bold (a, b, c)
- Simple, clean design
- Minimal colors
- Clear captions

### Science

**Figure Requirements**
- **Size**: 55 mm (single) or 120 mm (double column)
- **Format**: PDF, EPS, TIFF, or JPEG (high quality)
- **Resolution**: 300 DPI for photos, 600 DPI for line art
- **File size**: <10 MB
- **Fonts**: 6-7 pt minimum

**Style Notes**
- Panel labels: capital bold (A, B, C)
- High contrast
- Readable at small size

### Cell

**Figure Requirements**
- **Size**: 85 mm (single) or 178 mm (double column)
- **Format**: PDF preferred, TIFF, EPS acceptable
- **Resolution**: 300 DPI minimum
- **Fonts**: 8-10 pt for labels
- **Line weight**: 0.5 pt minimum

**Style Notes**
- Clean, professional
- Color or grayscale
- Panel labels capital (A, B, C)

### IEEE

**Figure Requirements**
- **Size**: 3.5 in (single) or 7.16 in (double column)
- **Format**: PDF, EPS (vector preferred)
- **Resolution**: 600 DPI for line art, 300 DPI for halftone
- **Fonts**: 8-10 pt minimum
- **Color**: Grayscale in print, color in digital

**Style Notes**
- Follow IEEE Graphics Manual
- Standard symbols for circuits
- Technical precision
- Clear axis labels

## Software-Specific Export Settings

### AI-Generated Images

AI-generated diagrams are exported as PNG images and can be included in LaTeX documents using:

```latex
\includegraphics[width=\textwidth]{diagram.png}
```

### Python (Matplotlib) Export

```python
import matplotlib.pyplot as plt

# Set publication quality
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 8
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts in PDF

# Save with proper DPI and cropping
fig.savefig('diagram.pdf', dpi=300, bbox_inches='tight', 
            pad_inches=0.1, transparent=False)
fig.savefig('diagram.png', dpi=300, bbox_inches='tight')
```

### Schemdraw Export

```python
import schemdraw

d = schemdraw.Drawing()
# ... build circuit ...

# Export
d.save('circuit.svg')  # Vector
d.save('circuit.pdf')  # Vector
d.save('circuit.png', dpi=300)  # Raster
```

### Inkscape Command Line

```bash
# PDF to high-res PNG
inkscape diagram.pdf --export-png=diagram.png --export-dpi=300

# SVG to PDF
inkscape diagram.svg --export-pdf=diagram.pdf
```

## Version Control Best Practices

**Keep Source Files**
- Save original .tex, .py, or .svg files
- Use descriptive filenames with versions
- Document color palette and style choices
- Include README with regeneration instructions

**Directory Structure**
```
figures/
├── source/          # Editable source files
│   ├── diagram1.tex
│   ├── circuit.py
│   └── pathway.svg
├── generated/       # Auto-generated outputs
│   ├── diagram1.pdf
│   ├── circuit.pdf
│   └── pathway.pdf
└── final/          # Final submission versions
    ├── figure1.pdf
    └── figure2.pdf
```

**Git Tracking**
- Track source files (.tex, .py)
- Consider .gitignore for generated PDFs (large files)
- Use releases/tags for submission versions
- Document generation process in README

## Testing and Validation

### Pre-Submission Tests

**Visual Tests**
1. **Print test**: Print at final size, check readability
2. **Grayscale test**: Convert to grayscale, verify interpretability
3. **Zoom test**: View at 400% and 25% to check scalability
4. **Screen test**: View on different devices (phone, tablet, desktop)

**Technical Tests**
1. **Font embedding**: Check PDF properties
2. **Resolution check**: Verify DPI meets requirements
3. **File size**: Ensure under journal limits
4. **Format compliance**: Verify accepted format

**Accessibility Tests**
1. **Colorblind simulation**: Use tools like Color Oracle
2. **Contrast checker**: WCAG contrast ratio tools
3. **Screen reader**: Test alt text (for web figures)

### Tools for Testing

**Colorblind Simulation**
- Color Oracle (free, cross-platform)
- Coblis (Color Blindness Simulator)
- Photoshop/GIMP colorblind preview modes

**PDF Inspection**
```bash
# Check PDF properties
pdfinfo diagram.pdf

# Check fonts
pdffonts diagram.pdf

# Check image resolution
identify -verbose diagram.pdf
```

**Contrast Checking**
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Colorable: https://colorable.jxnblk.com/

## Summary: Golden Rules

1. **Vector first**: Always use vector formats when possible
2. **Design at final size**: Avoid scaling after creation
3. **Colorblind-safe palette**: Use Okabe-Ito or similar
4. **Test in grayscale**: Diagrams must work without color
5. **Minimum 7-8 pt text**: At final print size
6. **Consistent styling**: Across all figures in paper
7. **Keep it simple**: Remove unnecessary elements
8. **High contrast**: Ensure readability
9. **Align elements**: Professional appearance matters
10. **Comprehensive caption**: Explain everything

## Further Resources

- **Nature Figure Preparation**: https://www.nature.com/nature/for-authors/final-submission
- **Science Figure Guidelines**: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- **WCAG Accessibility Standards**: https://www.w3.org/WAI/WCAG21/quickref/
- **Color Universal Design (CUD)**: https://jfly.uni-koeln.de/color/
- **ColorBrewer**: https://colorbrewer2.org/

Following these best practices ensures your diagrams meet publication standards and effectively communicate to all readers, regardless of colorblindness or viewing conditions.
