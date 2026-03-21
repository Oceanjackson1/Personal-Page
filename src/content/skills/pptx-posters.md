---
title: "Pptx Posters"
description: "Create research posters using HTML/CSS that can be exported to PDF or PPTX. Use this skill ONLY when the user explicitly requests PowerPoint/PPTX poster format. For standard research posters, use latex-posters instead. This skill provides modern w..."
category: "research"
source: "community"
author: "Community"
tags: ["pptx", "posters"]
date: 2026-03-20
---

# PPTX Research Posters (HTML-Based)

## Overview

**⚠️ USE THIS SKILL ONLY WHEN USER EXPLICITLY REQUESTS PPTX/POWERPOINT POSTER FORMAT.**

For standard research posters, use the **latex-posters** skill instead, which provides better typographic control and is the default for academic conferences.

This skill creates research posters using HTML/CSS, which can then be exported to PDF or converted to PowerPoint format. The web-based approach offers:
- Modern, responsive layouts
- Easy integration of AI-generated visuals
- Quick iteration and preview in browser
- Export to PDF via browser print function
- Conversion to PPTX if specifically needed

## When to Use This Skill

**ONLY use this skill when:**
- User explicitly requests "PPTX poster", "PowerPoint poster", or "PPT poster"
- User specifically asks for HTML-based poster
- User needs to edit poster in PowerPoint after creation
- LaTeX is not available or user requests non-LaTeX solution

**DO NOT use this skill when:**
- User asks for a "poster" without specifying format → Use latex-posters
- User asks for "research poster" or "conference poster" → Use latex-posters
- User mentions LaTeX, tikzposter, beamerposter, or baposter → Use latex-posters

## AI-Powered Visual Element Generation

**STANDARD WORKFLOW: Generate ALL major visual elements using AI before creating the HTML poster.**

This is the recommended approach for creating visually compelling posters:
1. Plan all visual elements needed (hero image, intro, methods, results, conclusions)
2. Generate each element using scientific-schematics or Nano Banana Pro
3. Assemble generated images in the HTML template
4. Add text content around the visuals

**Target: 60-70% of poster area should be AI-generated visuals, 30-40% text.**

---

### CRITICAL: Poster-Size Font Requirements

**⚠️ ALL text within AI-generated visualizations MUST be poster-readable.**

When generating graphics for posters, you MUST include font size specifications in EVERY prompt. Poster graphics are viewed from 4-6 feet away, so text must be LARGE.

**MANDATORY prompt requirements for EVERY poster graphic:**

```
POSTER FORMAT REQUIREMENTS (STRICTLY ENFORCE):
- ABSOLUTE MAXIMUM 3-4 elements per graphic (3 is ideal)
- ABSOLUTE MAXIMUM 10 words total in the entire graphic
- NO complex workflows with 5+ steps (split into 2-3 simple graphics instead)
- NO multi-level nested diagrams (flatten to single level)
- NO case studies with multiple sub-sections (one key point per case)
- ALL text GIANT BOLD (80pt+ for labels, 120pt+ for key numbers)
- High contrast ONLY (dark on white OR white on dark, NO gradients with text)
- MANDATORY 50% white space minimum (half the graphic should be empty)
- Thick lines only (5px+ minimum), large icons (200px+ minimum)
- ONE SINGLE MESSAGE per graphic (not 3 related messages)
```

**⚠️ BEFORE GENERATING: Review your prompt and count elements**
- If your description has 5+ items → STOP. Split into multiple graphics
- If your workflow has 5+ stages → STOP. Show only 3-4 high-level steps
- If your comparison has 4+ methods → STOP. Show only top 3 or Our vs Best Baseline

**Example - WRONG (7-stage workflow):**
```bash
# ❌ Creates tiny unreadable text
python scripts/generate_schematic.py "Drug discovery workflow: Stage 1 Target ID, Stage 2 Synthesis, Stage 3 Screening, Stage 4 Lead Opt, Stage 5 Validation, Stage 6 Clinical Trial, Stage 7 FDA Approval with metrics." -o figures/workflow.png
```

**Example - CORRECT (3 mega-stages):**
```bash
# ✅ Same content, simplified to readable poster format
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word in GIANT bold (120pt+). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_simple.png
```

---

### CRITICAL: Preventing Content Overflow

**⚠️ POSTERS MUST NOT HAVE TEXT OR CONTENT CUT OFF AT EDGES.**

**Prevention Rules:**

**1. Limit Content Sections (MAXIMUM 5-6 sections):**
```
✅ GOOD - 5 sections with room to breathe:
   - Title/Header
   - Introduction/Problem
   - Methods
   - Results (1-2 key findings)
   - Conclusions

❌ BAD - 8+ sections crammed together
```

**2. Word Count Limits:**
- **Per section**: 50-100 words maximum
- **Total poster**: 300-800 words MAXIMUM
- **If you have more content**: Cut it or make a handout

---

## Core Capabilities

### 1. HTML/CSS Poster Design

The HTML template (`assets/poster_html_template.html`) provides:
- Fixed poster dimensions (36×48 inches = 2592×3456 pt)
- Professional header with gradient styling
- Three-column content layout
- Block-based sections with modern styling
- Footer with references and contact info

### 2. Poster Structure

**Standard Layout:**
```
┌─────────────────────────────────────────┐
│  HEADER: Title, Authors, Hero Image     │
├─────────────┬─────────────┬─────────────┤
│ Introduction│   Results   │  Discussion │
│             │             │             │
│   Methods   │   (charts)  │ Conclusions │
│             │             │             │
│  (diagram)  │   (data)    │   (summary) │
├─────────────┴─────────────┴─────────────┤
│  FOOTER: References & Contact Info      │
└─────────────────────────────────────────┘
```

### 3. Visual Integration

Each section should prominently feature AI-generated visuals:

**Hero Image (Header):**
```html
<img src="figures/hero.png" class="hero-image">
```

**Section Graphics:**
```html
<div class="block">
  <h2 class="block-title">Methods</h2>
  <div class="block-content">
    <img src="figures/workflow.png" class="block-image">
    <ul>
      <li>Brief methodology point</li>
    </ul>
  </div>
</div>
```

### 4. Generating Visual Elements

**Before creating the HTML, generate all visual elements:**

```bash
# Create figures directory
mkdir -p figures

# Hero image - SIMPLE, impactful
python scripts/generate_schematic.py "POSTER FORMAT for A0. Hero banner: '[TOPIC]' in HUGE text (120pt+). Dark blue gradient background. ONE iconic visual. Minimal text. Readable from 15 feet." -o figures/hero.png

# Introduction visual - ONLY 3 elements
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 icons: [icon1] → [icon2] → [icon3]. ONE word labels (80pt+). 50% white space. Readable from 8 feet." -o figures/intro.png

# Methods flowchart - ONLY 4 steps
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: STEP1 → STEP2 → STEP3 → STEP4. GIANT labels (100pt+). Thick arrows. 50% white space. NO sub-steps." -o figures/workflow.png

# Results visualization - ONLY 3 bars
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: BASELINE (70%), EXISTING (85%), OURS (95%). GIANT percentages ON bars (120pt+). NO axis, NO legend. 50% white space." -o figures/results.png

# Conclusions - EXACTLY 3 key findings
python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 cards: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'READY' (60pt). 50% white space. NO other text." -o figures/conclusions.png
```

---

## Workflow for PPTX Poster Creation

### Stage 1: Planning

1. **Confirm PPTX is explicitly requested**
2. **Determine poster requirements:**
   - Size: 36×48 inches (most common) or A0
   - Orientation: Portrait (most common)
3. **Develop content outline:**
   - Identify 1-3 core messages
   - Plan 3-5 visual elements
   - Draft minimal text (300-800 words total)

### Stage 2: Generate Visual Elements (AI-Powered)

**CRITICAL: Generate SIMPLE figures with MINIMAL content.**

```bash
mkdir -p figures

# Generate each element with POSTER FORMAT specifications
# (See examples in Section 4 above)
```

### Stage 3: Create HTML Poster

1. **Copy the template:**
   ```bash
   cp skills/pptx-posters/assets/poster_html_template.html poster.html
   ```

2. **Update content:**
   - Replace placeholder title and authors
   - Insert AI-generated images
   - Add minimal supporting text
   - Update references and contact info

3. **Preview in browser:**
   ```bash
   open poster.html  # macOS
   # or
   xdg-open poster.html  # Linux
   ```

### Stage 4: Export to PDF

**Browser Print Method:**
1. Open poster.html in Chrome or Firefox
2. Print (Cmd/Ctrl + P)
3. Select "Save as PDF"
4. Set paper size to match poster dimensions
5. Remove margins
6. Enable "Background graphics"

**Command Line (if Chrome available):**
```bash
# Chrome headless PDF export
google-chrome --headless --print-to-pdf=poster.pdf \
  --print-to-pdf-no-header \
  --no-margins \
  poster.html
```

### Stage 5: Convert to PPTX (If Required)

**Option 1: PDF to PPTX conversion**
```bash
# Using LibreOffice
libreoffice --headless --convert-to pptx poster.pdf

# Or use online converters for simple cases
```

**Option 2: Direct PPTX creation with python-pptx**
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(48)
prs.slide_height = Inches(36)

slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

# Add images from figures/
slide.shapes.add_picture("figures/hero.png", Inches(0), Inches(0), width=Inches(48))
# ... add other elements

prs.save("poster.pptx")
```

---

## HTML Template Structure

The provided template (`assets/poster_html_template.html`) includes:

### CSS Variables for Customization

```css
/* Poster dimensions */
body {
  width: 2592pt;   /* 36 inches */
  height: 3456pt;  /* 48 inches */
}

/* Color scheme - customize these */
.header {
  background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
}

/* Typography */
.poster-title { font-size: 108pt; }
.authors { font-size: 48pt; }
.block-title { font-size: 52pt; }
.block-content { font-size: 34pt; }
```

### Key Classes

| Class | Purpose | Font Size |
|-------|---------|-----------|
| `.poster-title` | Main title | 108pt |
| `.authors` | Author names | 48pt |
| `.affiliations` | Institutions | 38pt |
| `.block-title` | Section headers | 52pt |
| `.block-content` | Body text | 34pt |
| `.key-finding` | Highlight box | 36pt |

---

## Quality Checklist

### Step 0: Pre-Generation Review (MANDATORY)

**For EACH planned graphic, verify:**
- [ ] Can describe in 3-4 items or less? (NOT 5+)
- [ ] Is it a simple workflow (3-4 steps, NOT 7+)?
- [ ] Can describe all text in 10 words or less?
- [ ] Does it convey ONE message (not multiple)?

**Reject these patterns:**
- ❌ "7-stage workflow" → Simplify to "3 mega-stages"
- ❌ "Multiple case studies" → One case per graphic
- ❌ "Timeline 2015-2024 annual" → "ONLY 3 key years"
- ❌ "Compare 6 methods" → "ONLY 2: ours vs best"

### Step 2b: Post-Generation Review (MANDATORY)

**For EACH generated figure at 25% zoom:**

**✅ PASS criteria (ALL must be true):**
- [ ] Can read ALL text clearly
- [ ] Count: 3-4 elements or fewer
- [ ] White space: 50%+ empty
- [ ] Understand in 2 seconds
- [ ] NOT a complex 5+ stage workflow
- [ ] NOT multiple nested sections

**❌ FAIL criteria (regenerate if ANY true):**
- [ ] Text small/hard to read → Regenerate with "150pt+"
- [ ] More than 4 elements → Regenerate "ONLY 3 elements"
- [ ] Less than 50% white space → Regenerate "60% white space"
- [ ] Complex multi-stage → SPLIT into 2-3 graphics
- [ ] Multiple cases cramped → SPLIT into separate graphics

### After Export

- [ ] NO content cut off at ANY of the 4 edges (check carefully)
- [ ] All images display correctly
- [ ] Colors render as expected
- [ ] Text readable at 25% scale
- [ ] Graphics look SIMPLE (not like complex 7-stage workflows)

---

## Common Pitfalls to Avoid

**AI-Generated Graphics Mistakes:**
- ❌ Too many elements (10+ items) → Keep to 3-5 max
- ❌ Text too small → Specify "GIANT (100pt+)" in prompts
- ❌ No white space → Add "50% white space" to every prompt
- ❌ Complex flowcharts (8+ steps) → Limit to 4-5 steps

**HTML/Export Mistakes:**
- ❌ Content exceeding poster dimensions → Check overflow in browser
- ❌ Missing background graphics in PDF → Enable in print settings
- ❌ Wrong paper size in PDF → Match poster dimensions exactly
- ❌ Low-resolution images → Use 300 DPI minimum

**Content Mistakes:**
- ❌ Too much text (over 1000 words) → Cut to 300-800 words
- ❌ Too many sections (7+) → Consolidate to 5-6
- ❌ No clear visual hierarchy → Make key findings prominent

---

## Integration with Other Skills

This skill works with:
- **Scientific Schematics**: Generate all poster diagrams and flowcharts
- **Generate Image / Nano Banana Pro**: Create stylized graphics and hero images
- **LaTeX Posters**: DEFAULT skill for poster creation (use this instead unless PPTX explicitly requested)

---

## Template Assets

Available in `assets/` directory:

- `poster_html_template.html`: Main HTML poster template (36×48 inches)
- `poster_quality_checklist.md`: Pre-submission validation checklist

## References

Available in `references/` directory:

- `poster_content_guide.md`: Content organization and writing guidelines
- `poster_design_principles.md`: Typography, color theory, and visual hierarchy
- `poster_layout_design.md`: Layout principles and grid systems

---

## Reference: Poster_Content_Guide

# Research Poster Content Guide

## Overview

Content is king in research posters. This guide covers writing strategies, section-specific guidance, visual-text balance, and best practices for communicating research effectively in poster format.

## Core Content Principles

### 1. The 3-5 Minute Rule

**Reality**: Most viewers spend 3-5 minutes at your poster
- **1 minute**: Scanning from distance (title, figures)
- **2-4 minutes**: Reading key points up close
- **5+ minutes**: Engaged conversation (if interested)

**Design Implication**: Poster must work at three levels:
1. **Distance view** (6-10 feet): Title and main figure visible
2. **Browse view** (3-6 feet): Section headers and key results readable
3. **Detail view** (1-3 feet): Full content accessible

### 2. Tell a Story, Not a Paper

**Poster ≠ Condensed Paper**

**Paper approach** (❌):
- Comprehensive literature review
- Detailed methodology
- All results presented
- Lengthy discussion
- 50+ references

**Poster approach** (✅):
- One sentence background
- Visual methods diagram
- 3-5 key results
- 3-4 bullet point conclusions
- 5-10 key references

**Story Arc for Posters**:
```
Hook (Problem) → Approach → Discovery → Impact
```

**Example**:
- **Hook**: "Antibiotic resistance threatens millions of lives annually"
- **Approach**: "We developed an AI system to predict resistance patterns"
- **Discovery**: "Our model achieves 87% accuracy, 20% better than existing methods"
- **Impact**: "Could reduce treatment failures by identifying resistance earlier"

### 3. The 800-Word Maximum

**Word Count Guidelines**:
- **Ideal**: 300-500 words
- **Maximum**: 800 words
- **Hard limit**: 1000 words (beyond this, poster is unreadable)

**Word Budget by Section**:
| Section | Word Count | % of Total |
|---------|-----------|------------|
| Introduction/Background | 50-100 | 15% |
| Methods | 100-150 | 25% |
| Results (text) | 100-200 | 25% |
| Discussion/Conclusions | 100-150 | 25% |
| References/Acknowledgments | 50-100 | 10% |

**Counting Tool**:
```latex
% Add word count to poster (remove for final)
\usepackage{texcount}
% Compile with: texcount -inc poster.tex
```

### 4. Visual-to-Text Ratio

**Optimal Balance**: 40-50% visual content, 50-60% text+white space

**Visual Content Includes**:
- Figures and graphs
- Photos and images
- Diagrams and flowcharts
- Icons and symbols
- Color blocks and design elements

**Too Text-Heavy** (❌):
- Wall of text
- Small figures
- Intimidating to viewers
- Low engagement

**Well-Balanced** (✅):
- Clear figures dominate
- Text supports visuals
- Easy to scan
- Inviting appearance

## Section-Specific Content Guidance

### Title

**Purpose**: Capture attention, convey topic, establish credibility

**Characteristics of Effective Titles**:
- **Concise**: 10-15 words maximum
- **Descriptive**: Clearly states research topic
- **Active**: Uses strong verbs when possible
- **Specific**: Avoids vague terms
- **Jargon-aware**: Balances field-specific terms with accessibility

**Title Formulas**:

**1. Descriptive**:
```
[Method/Approach] for [Problem/Application]

Example: "Deep Learning for Early Detection of Alzheimer's Disease"
```

**2. Question**:
```
[Research Question]?

Example: "Can Microbiome Diversity Predict Treatment Response?"
```

**3. Assertion**:
```
[Finding] in [Context]

Example: "Novel Mechanism Identified in Drug Resistance Pathways"
```

**4. Colon Format**:
```
[Topic]: [Specific Approach/Finding]

Example: "Urban Heat Islands: A Machine Learning Framework for Mitigation"
```

**Avoid**:
- ❌ Generic titles: "A Study of X"
- ❌ Overly cute or clever wordplay (confuses message)
- ❌ Excessive jargon: "Utilization of CRISPR-Cas9..."
- ❌ Unnecessarily long: "Investigation of the potential role of..."

**LaTeX Title Formatting**:
```latex
% Emphasize key words with bold
\title{Deep Learning for \textbf{Early Detection} of Alzheimer's Disease}

% Two-line titles for long names
\title{Machine Learning Framework for\\Urban Heat Island Mitigation}

% Avoid ALL CAPS (harder to read)
```

### Authors and Affiliations

**Best Practices**:
- **Presenting author**: Bold, underline, or asterisk
- **Corresponding author**: Include email
- **Affiliations**: Superscript numbers or symbols
- **Institutional logos**: 2-4 maximum

**Format Examples**:
```latex
% Simple format
\author{\textbf{Jane Smith}\textsuperscript{1}, John Doe\textsuperscript{2}}
\institute{
  \textsuperscript{1}University of Example, 
  \textsuperscript{2}Research Institute
}

% With contact
\author{Jane Smith\textsuperscript{1,*}}
\institute{
  \textsuperscript{1}Department, University\\
  \textsuperscript{*}jane.smith@university.edu
}
```

### Introduction/Background

**Purpose**: Establish context, motivate research, state objective

**Structure** (50-100 words):
1. **Problem statement** (1-2 sentences): What's the issue?
2. **Knowledge gap** (1-2 sentences): What's unknown/unsolved?
3. **Research objective** (1 sentence): What did you do?

**Example** (95 words):
```
Antibiotic resistance causes 700,000 deaths annually, projected to reach 
10 million by 2050. Current diagnostic methods require 48-72 hours, 
delaying appropriate treatment. Machine learning offers potential for 
rapid resistance prediction, but existing models lack generalizability 
across bacterial species. 

We developed a transformer-based deep learning model to predict antibiotic 
resistance from genomic sequences across multiple pathogen species. Our 
approach integrates evolutionary information and protein structure to 
improve cross-species accuracy.
```

**Visual Support**:
- Conceptual diagram showing problem
- Infographic with statistics
- Image of application context

**Common Mistakes**:
- ❌ Extensive literature review
- ❌ Too much background detail
- ❌ Undefined acronyms at first use
- ❌ Missing clear objective statement

### Methods

**Purpose**: Describe approach sufficiently for understanding (not replication)

**Key Question**: "How did you do it?" not "How could someone else replicate it?"

**Content Strategy**:
- **Prioritize**: Visual methods diagram > text description
- **Include**: Study design, key procedures, analysis approach
- **Omit**: Detailed protocols, routine procedures, specific reagent details

**Visual Methods (Highly Recommended)**:
```latex
% Flowchart of study design
\begin{tikzpicture}[node distance=2cm]
  \node (start) [box] {Data Collection\\n=1,000 samples};
  \node (process) [box, below of=start] {Preprocessing\\Quality Control};
  \node (analysis) [box, below of=process] {Statistical Analysis\\Mixed Models};
  \node (end) [box, below of=analysis] {Validation\\Independent Cohort};
  
  \draw [arrow] (start) -- (process);
  \draw [arrow] (process) -- (analysis);
  \draw [arrow] (analysis) -- (end);
\end{tikzpicture}
```

**Text Methods** (50-150 words):

**For Experimental Studies**:
```
Methods
• Study design: Randomized controlled trial (n=200)
• Participants: Adults aged 18-65 with Type 2 diabetes
• Intervention: 12-week exercise program vs. standard care
• Outcomes: HbA1c (primary), insulin sensitivity (secondary)
• Analysis: Linear mixed models, intention-to-treat
```

**For Computational Studies**:
```
Methods
• Dataset: 10,000 labeled images from ImageNet
• Architecture: ResNet-50 with custom attention mechanism
• Training: 100 epochs, Adam optimizer, learning rate 0.001
• Validation: 5-fold cross-validation
• Comparison: Baseline CNN, VGG-16, Inception-v3
```

**Format Options**:
- **Bullet points**: Quick scanning (recommended)
- **Numbered list**: Sequential procedures
- **Diagram + brief text**: Ideal combination
- **Table**: Multiple conditions or parameters

### Results

**Purpose**: Present key findings visually and clearly

**Golden Rule**: Show, don't tell

**Content Allocation**:
- **Figures**: 70-80% of Results section
- **Text**: 20-30% (brief descriptions, statistics)

**How Many Results**:
- **Ideal**: 3-5 main findings
- **Maximum**: 6-7 distinct results
- **Focus**: Primary outcomes, most impactful findings

**Figure Selection Criteria**:
1. Does it support the main message?
2. Is it self-explanatory with caption?
3. Can it be understood in 10 seconds?
4. Does it add information beyond text?

**Figure Captions**:
- **Descriptive**: Explain what is shown
- **Standalone**: Understandable without reading full poster
- **Statistical**: Include significance indicators, sample sizes
- **Concise**: 1-3 sentences

**Example Caption**:
```latex
\caption{Treatment significantly improved outcomes. 
Mean±SD shown for control (blue, n=45) and treatment (orange, n=47) groups. 
**p<0.01, ***p<0.001 (two-tailed t-test).}
```

**Text Support for Results** (100-200 words):
- State main finding per figure
- Include key statistics
- Note trends or patterns
- Avoid detailed interpretation (save for Discussion)

**Example Results Text**:
```
Key Findings
• Model achieved 87% accuracy on test set (vs. 73% baseline)
• Performance consistent across 5 bacterial species (p<0.001)
• Prediction speed: <30 seconds per isolate
• Feature importance: protein structure (42%), sequence (35%), 
  evolutionary conservation (23%)
```

**Data Presentation Formats**:

**1. Bar Charts**: Comparing categories
```latex
\begin{tikzpicture}
  \begin{axis}[
    ybar,
    ylabel=Accuracy (\%),
    symbolic x coords={Baseline, Model A, Our Method},
    xtick=data,
    nodes near coords
  ]
  \addplot coordinates {(Baseline,73) (Model A,81) (Our Method,87)};
  \end{axis}
\end{tikzpicture}
```

**2. Line Graphs**: Trends over time
**3. Scatter Plots**: Correlations
**4. Heatmaps**: Matrix data, clustering
**5. Box Plots**: Distributions, comparisons
**6. ROC Curves**: Classification performance

### Discussion/Conclusions

**Purpose**: Interpret findings, state implications, acknowledge limitations

**Structure** (100-150 words):

**1. Main Conclusions** (50-75 words):
- 3-5 bullet points
- Clear, specific takeaways
- Linked to research objectives

**Example**:
```
Conclusions
• First cross-species model for antibiotic resistance prediction 
  achieving >85% accuracy
• Protein structure integration critical for generalizability 
  (improved accuracy by 14%)
• Prediction speed enables clinical decision support within 
  consultation timeframe
• Potential to reduce inappropriate antibiotic use by 20-30%
```

**2. Limitations** (25-50 words, optional but recommended):
- Acknowledge key constraints
- Brief, honest
- Shows scientific rigor

**Example**:
```
Limitations
• Training data limited to 5 bacterial species
• Requires genomic sequencing (not widely available)
• Validation needed in prospective clinical trials
```

**3. Future Directions** (25-50 words, optional):
- Next steps
- Broader implications
- Call to action

**Example**:
```
Next Steps
• Expand to 20+ additional species
• Develop point-of-care sequencing integration
• Launch multi-center clinical validation study (2025)
```

**Avoid**:
- ❌ Overstating findings: "This revolutionary breakthrough..."
- ❌ Extensive comparison to other work
- ❌ New results in Discussion
- ❌ Vague conclusions: "Further research is needed"

### References

**How Many**: 5-10 key citations

**Selection Criteria**:
- Include seminal work in the field
- Recent relevant studies (last 5 years)
- Methods cited in your poster
- Controversial claims that need support

**Format**: Abbreviated, consistent style

**Examples**:

**Numbered (Vancouver)**:
```
References
1. Smith et al. (2023). Nature. 615:234-240.
2. Jones & Lee (2024). Science. 383:112-118.
3. Chen et al. (2022). Cell. 185:456-470.
```

**Author-Year (APA)**:
```
References
Smith, J. et al. (2023). Title. Nature, 615, 234-240.
Jones, A., & Lee, B. (2024). Title. Science, 383, 112-118.
```

**Minimal (For Space Constraints)**:
```
Key References: Smith (Nature 2023), Jones (Science 2024), 
Chen (Cell 2022). Full bibliography: [QR Code]
```

**Alternative**: QR code linking to full reference list

### Acknowledgments

**Include**:
- Funding sources (with grant numbers)
- Major collaborators
- Core facilities used
- Dataset sources

**Format** (25-50 words):
```
Acknowledgments
Funded by NIH Grant R01-123456 and NSF Award 7890123. 
We thank Dr. X for data access, the Y Core Facility for 
sequencing, and Z for helpful discussions.
```

### Contact Information

**Essential Elements**:
- Name of presenting/corresponding author
- Email address
- Optional: Lab website, Twitter/X, LinkedIn, ORCID

**Format**:
```
Contact: Jane Smith, jane.smith@university.edu
Lab: smithlab.university.edu | Twitter: @smithlab
```

**QR Code Alternative**:
- Link to personal/lab website
- Link to paper preprint/publication
- Link to code repository (GitHub)
- Link to supplementary materials

## Writing Style for Posters

### Active vs. Passive Voice

**Prefer Active Voice** (more engaging, clearer):
- ✅ "We developed a model..."
- ✅ "The treatment reduced symptoms..."

**Passive Voice** (when appropriate):
- ✅ "Samples were collected from..."
- ✅ "Data were analyzed using..."

### Sentence Length

**Keep Sentences Short**:
- **Ideal**: 10-15 words per sentence
- **Maximum**: 20-25 words
- **Avoid**: >30 words (hard to follow)

**Example Revision**:
- ❌ Long: "We performed a comprehensive analysis of gene expression data from 500 patients with colorectal cancer using RNA sequencing and identified 47 differentially expressed genes associated with treatment response." (31 words)
- ✅ Short: "We analyzed RNA sequencing data from 500 colorectal cancer patients. We identified 47 genes associated with treatment response." (19 words total, two sentences)

### Bullet Points vs. Paragraphs

**Use Bullet Points For**:
- ✅ Lists of items or findings
- ✅ Key conclusions
- ✅ Methods steps
- ✅ Study characteristics

**Use Short Paragraphs For**:
- ✅ Narrative flow (Introduction)
- ✅ Complex explanations
- ✅ Connected ideas

**Bullet Point Best Practices**:
- Start with action verbs or nouns
- Parallel structure throughout list
- 3-7 bullets per list (not too many)
- Brief (1-2 lines each)

**Example**:
```
Methods
• Participants: 200 adults (18-65 years)
• Design: Double-blind RCT (12 weeks)
• Intervention: Daily 30-min exercise
• Control: Standard care
• Analysis: Mixed models (SPSS v.28)
```

### Acronyms and Jargon

**First Use Rule**: Define at first appearance
```
We used machine learning (ML) to analyze... Later, ML predicted...
```

**Common Acronyms**: May not need definition if universal to field
- DNA, RNA, MRI, CT, PCR (in biomedical context)
- AI, ML, CNN (in computer science context)

**Avoid Excessive Jargon**:
- ❌ "Utilized" → ✅ "Used"
- ❌ "Implement utilization of" → ✅ "Use"
- ❌ "A majority of" → ✅ "Most"

### Numbers and Statistics

**Present Statistics Clearly**:
- Always include measure of variability (SD, SE, CI)
- Report sample sizes: n=50
- Indicate significance: p<0.05, p<0.01, p<0.001
- Use symbols consistently: * for p<0.05, ** for p<0.01

**Format Numbers**:
- Round appropriately (avoid false precision)
- Use consistent decimal places
- Include units: 25 mg/dL, 37°C
- Large numbers: 1,000 or 1000 (be consistent)

**Example**:
```
Treatment increased response by 23.5% (95% CI: 18.2-28.8%, p<0.001, n=150)
```

## Visual-Text Integration

### Figure-Text Relationship

**Figure First, Text Second**:
1. Design poster around key figures
2. Add text to support and explain visuals
3. Ensure figures can stand alone

**Text Placement Relative to Figures**:
- **Above**: Context, "What you're about to see"
- **Below**: Explanation, statistics, caption
- **Beside**: Comparison, interpretation

### Callouts and Annotations

**On-Figure Annotations**:
```latex
\begin{tikzpicture}
  \node[inner sep=0] (img) {\includegraphics[width=10cm]{figure.pdf}};
  \draw[->, thick, red] (8,5) -- (6,3) node[left] {Key region};
  \draw[red, thick] (3,2) circle (1cm) node[above=1.2cm] {Anomaly};
\end{tikzpicture}
```

**Callout Boxes**:
```latex
\begin{tcolorbox}[colback=yellow!10, colframe=orange!80, 
                  title=Key Finding]
Our method reduces errors by 34\% compared to state-of-the-art.
\end{tcolorbox}
```

### Icons for Section Headers

**Visual Section Markers**:
```latex
\usepackage{fontawesome5}

\block{\faFlask~Introduction}{...}
\block{\faCog~Methods}{...}
\block{\faChartBar~Results}{...}
\block{\faLightbulb~Conclusions}{...}
```

## Content Adaptation Strategies

### From Paper to Poster

**Condensation Process**:

**1. Identify Core Message** (The Elevator Pitch):
- What's the one thing you want people to remember?
- If you had 30 seconds, what would you say?

**2. Select Key Results**:
- Choose 3-5 most impactful findings
- Omit supporting/secondary results
- Focus on figures with strong visual impact

**3. Simplify Methods**:
- Visual flowchart > text description
- Omit routine procedures
- Include only essential parameters

**4. Trim Literature Review**:
- One sentence background
- One sentence gap/motivation
- One sentence your contribution

**5. Condense Discussion**:
- Main conclusions only
- Brief limitations
- One sentence future direction

### For Different Audiences

**Specialist Audience** (Same Field):
- Can use field-specific jargon
- Less background needed
- Focus on novel methodology
- Emphasize nuanced findings

**General Scientific Audience**:
- Define key terms
- More context/background
- Broader implications
- Visual metaphors helpful

**Public/Lay Audience**:
- Minimal jargon, all defined
- Extensive context
- Real-world applications
- Analogies and simple language

**Example Adaptation**:

**Specialist**: "CRISPR-Cas9 knockout of BRCA1 induced synthetic lethality with PARP inhibitors"

**General**: "We used gene editing to make cancer cells vulnerable to existing drugs"

**Public**: "We found a way to make cancer treatments work better by targeting specific genetic weaknesses"

## Quality Control Checklist

### Content Review

**Clarity**:
- [ ] Main message immediately clear
- [ ] All acronyms defined
- [ ] Sentences short and direct
- [ ] No unnecessary jargon

**Completeness**:
- [ ] Research question/objective stated
- [ ] Methods sufficiently described
- [ ] Key results presented
- [ ] Conclusions drawn
- [ ] Limitations acknowledged

**Accuracy**:
- [ ] All statistics correct
- [ ] Figure captions accurate
- [ ] References properly cited
- [ ] No overstated claims

**Engagement**:
- [ ] Compelling title
- [ ] Visual interest
- [ ] Clear take-home message
- [ ] Conversation starters

### Readability Testing

**Distance Test**:
- Print at 25% scale
- View from 2-3 feet (simulates 8-12 feet for full poster)
- Can you read: Title? Section headers? Body text?

**Scan Test**:
- Give poster to colleague for 30 seconds
- Ask: "What is this poster about?"
- They should identify: Topic, approach, main finding

**Detail Test**:
- Ask colleague to read poster thoroughly (5 min)
- Ask: "What are the key conclusions?"
- Verify understanding matches your intent

## Common Content Mistakes

**1. Too Much Text**
- ❌ >1000 words
- ❌ Long paragraphs
- ❌ Full paper condensed
- ✅ 300-800 words, bullet points, key findings only

**2. Unclear Message**
- ❌ Multiple unrelated findings
- ❌ No clear conclusion
- ❌ Vague implications
- ✅ 1-3 main points, explicit conclusions

**3. Methods Overkill**
- ❌ Detailed protocols
- ❌ All parameters listed
- ❌ Routine procedures described
- ✅ Visual flowchart, key details only

**4. Poor Figure Integration**
- ❌ Figures without context
- ❌ Unclear captions
- ❌ Text doesn't reference figures
- ✅ Figures central, well-captioned, text integrated

**5. Missing Context**
- ❌ No background
- ❌ Undefined acronyms
- ❌ Assumes expert knowledge
- ✅ Brief context, definitions, accessible to broader audience

## Conclusion

Effective poster content:
- **Concise**: 300-800 words maximum
- **Visual**: 40-50% figures and graphics
- **Clear**: One main message, 3-5 key findings
- **Engaging**: Compelling story, not just facts
- **Accessible**: Appropriate for target audience
- **Actionable**: Clear implications and next steps

Remember: Your poster is a conversation starter, not a comprehensive treatise. Design content to intrigue, engage, and invite discussion.

---

## Reference: Poster_Design_Principles

# Research Poster Design Principles

## Overview

Effective poster design balances visual appeal, readability, and scientific content. This guide covers typography, color theory, visual hierarchy, accessibility, and evidence-based design principles for research posters.

## Core Design Principles

### 1. Visual Hierarchy

Guide viewers through content in logical order using size, color, position, and contrast.

**Hierarchy Levels**:

1. **Primary (Title)**: Largest, most prominent
   - Size: 72-120pt
   - Position: Top center or top spanning
   - Weight: Bold
   - Purpose: Capture attention from 20+ feet

2. **Secondary (Section Headers)**: Organize content
   - Size: 48-72pt
   - Weight: Bold or semi-bold
   - Purpose: Section navigation, readable from 10 feet

3. **Tertiary (Body Text)**: Main content
   - Size: 24-36pt minimum
   - Weight: Regular
   - Purpose: Detailed information, readable from 4-6 feet

4. **Quaternary (Captions, References)**: Supporting info
   - Size: 18-24pt
   - Weight: Regular or light
   - Purpose: Context and attribution

**Implementation**:
```latex
% Define hierarchy in LaTeX
\setbeamerfont{title}{size=\VeryHuge,series=\bfseries}        % 90pt+
\setbeamerfont{block title}{size=\Huge,series=\bfseries}      % 60pt
\setbeamerfont{block body}{size=\LARGE}                        % 30pt
\setbeamerfont{caption}{size=\large}                           % 24pt
```

### 2. White Space (Negative Space)

Empty space is not wasted space—it enhances readability and guides attention.

**White Space Functions**:
- **Breathing room**: Prevents overwhelming viewers
- **Grouping**: Shows which elements belong together
- **Focus**: Draws attention to important elements
- **Flow**: Creates visual pathways through content

**Guidelines**:
- Minimum 5-10% margins on all sides
- Consistent spacing between blocks (1-2cm)
- Space around figures equal to or greater than border width
- Group related items closely, separate unrelated items
- Don't fill every inch—aim for 40-60% text coverage

**LaTeX Implementation**:
```latex
% beamerposter spacing
\setbeamertemplate{block begin}{
  \vskip2ex  % Space before block
  ...
}

% tikzposter spacing
\documentclass[..., blockverticalspace=15mm, colspace=15mm]{tikzposter}

% Manual spacing
\vspace{2cm}  % Vertical space
\hspace{1cm}  % Horizontal space
```

### 3. Alignment and Grid Systems

Proper alignment creates professional, organized appearance.

**Alignment Types**:
- **Left-aligned text**: Most readable for body text (Western audiences)
- **Center-aligned**: Headers, titles, symmetric layouts
- **Right-aligned**: Rarely used, special cases only
- **Justified**: Avoid (creates uneven spacing)

**Grid Systems**:
- **2-column**: Simple, traditional, good for narrative flow
- **3-column**: Most common, balanced, versatile
- **4-column**: Complex, information-dense, requires careful design
- **Asymmetric**: Creative, modern, requires expertise

**Best Practices**:
- Align block edges to invisible grid lines
- Keep consistent column widths (unless intentionally asymmetric)
- Align similar elements (all figures, all text blocks)
- Use consistent margins throughout

### 4. Visual Flow and Reading Patterns

Design for natural eye movement and logical content progression.

**Common Reading Patterns**:

**Z-Pattern (Landscape posters)**:
```
Start → → → Top Right
  ↓
Middle Left → → Middle
  ↓
Bottom Left → → → End
```

**F-Pattern (Portrait posters)**:
```
Title → → → →
↓
Section 1 → →
↓
Section 2 → →
↓
Section 3 → →
↓
Conclusion → →
```

**Gutenberg Diagram**:
```
Primary Area     Strong Fallow
(top-left)       (top-right)
        ↓              ↓
Weak Fallow      Terminal Area
(bottom-left)    (bottom-right)
```

**Implementation Strategy**:
1. Place most important content in "hot zones" (top-left, center)
2. Create visual paths with arrows, lines, or color
3. Use numbering for sequential information (Methods steps)
4. Design left-to-right, top-to-bottom flow (Western audiences)
5. Position conclusions prominently (bottom-right is natural endpoint)

## Typography

### Font Selection

**Recommended Fonts**:

**Sans-Serif (Recommended for posters)**:
- **Helvetica**: Clean, professional, widely available
- **Arial**: Similar to Helvetica, universal compatibility
- **Calibri**: Modern, friendly, good readability
- **Open Sans**: Contemporary, excellent web and print
- **Roboto**: Modern, Google design, highly readable
- **Lato**: Warm, professional, works at all sizes

**Serif (Use sparingly)**:
- **Times New Roman**: Traditional, formal
- **Garamond**: Elegant, good for humanities
- **Georgia**: Designed for screens, readable

**Avoid**:
- ❌ Comic Sans (unprofessional)
- ❌ Decorative or script fonts (illegible from distance)
- ❌ Mixing more than 2-3 font families

**LaTeX Implementation**:
```latex
% Helvetica (sans-serif)
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

% Arial-like
\usepackage{avant}
\renewcommand{\familydefault}{\sfdefault}

% Modern fonts with fontspec (requires LuaLaTeX/XeLaTeX)
\usepackage{fontspec}
\setmainfont{Helvetica Neue}
\setsansfont{Open Sans}
```

### Font Sizing

**Absolute Minimum Sizes** (readable from 4-6 feet):
- Title: 72pt+ (85-120pt recommended)
- Section headers: 48-72pt
- Body text: 24-36pt (30pt+ recommended)
- Captions/small text: 18-24pt
- References: 16-20pt minimum

**Testing Readability**:
- Print at 25% scale
- Read from 2-3 feet distance
- If legible, full-scale poster will be readable from 8-12 feet

**Size Conversion**:
| LaTeX Command | Approximate Size | Use Case |
|---------------|------------------|----------|
| `\tiny` | 10pt | Avoid on posters |
| `\small` | 16pt | Minimal use only |
| `\normalsize` | 20pt | References (scaled up) |
| `\large` | 24pt | Captions, small text |
| `\Large` | 28pt | Body text (minimum) |
| `\LARGE` | 32pt | Body text (recommended) |
| `\huge` | 36pt | Subheadings |
| `\Huge` | 48pt | Section headers |
| `\VeryHuge` | 72pt+ | Title |

### Text Formatting Best Practices

**Use**:
- ✅ **Bold** for emphasis and headers
- ✅ Short paragraphs (3-5 lines maximum)
- ✅ Bullet points for lists
- ✅ Adequate line spacing (1.2-1.5)
- ✅ High contrast (dark text on light background)

**Avoid**:
- ❌ Italics from distance (hard to read)
- ❌ ALL CAPS FOR LONG TEXT (SLOW TO READ)
- ❌ Underlines (old-fashioned, interferes with descenders)
- ❌ Long paragraphs (> 6 lines)
- ❌ Light text on light backgrounds

**Line Spacing**:
```latex
% Increase line spacing for readability
\usepackage{setspace}
\setstretch{1.3}  % 1.3x normal spacing

% Or in specific blocks
\begin{spacing}{1.5}
  Your text here with extra spacing
\end{spacing}
```

## Color Theory for Posters

### Color Psychology and Meaning

Colors convey meaning and affect viewer perception:

| Color | Associations | Use Cases |
|-------|--------------|-----------|
| **Blue** | Trust, professionalism, science | Academic, medical, technology |
| **Green** | Nature, health, growth | Environmental, biology, health |
| **Red** | Energy, urgency, passion | Attention, warnings, bold statements |
| **Orange** | Creativity, enthusiasm | Innovative research, friendly approach |
| **Purple** | Wisdom, creativity, luxury | Humanities, arts, premium research |
| **Gray** | Neutral, professional, modern | Technology, minimal designs |
| **Yellow** | Optimism, attention, caution | Highlights, energy, caution areas |

### Color Scheme Types

**1. Monochromatic**: Variations of single hue
- **Pros**: Harmonious, professional, easy to execute
- **Cons**: Can be boring, less visual interest
- **Use**: Conservative conferences, institutional branding

```latex
% Monochromatic blue scheme
\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{medblue}{RGB}{51,102,153}
\definecolor{lightblue}{RGB}{204,229,255}
```

**2. Analogous**: Adjacent colors on color wheel
- **Pros**: Harmonious, visually comfortable
- **Cons**: Low contrast, may lack excitement
- **Use**: Nature/biology topics, smooth gradients

```latex
% Analogous blue-green scheme
\definecolor{blue}{RGB}{0,102,204}
\definecolor{teal}{RGB}{0,153,153}
\definecolor{green}{RGB}{51,153,102}
```

**3. Complementary**: Opposite colors on wheel
- **Pros**: High contrast, vibrant, energetic
- **Cons**: Can be overwhelming if intense
- **Use**: Drawing attention, modern designs

```latex
% Complementary blue-orange scheme
\definecolor{primary}{RGB}{0,71,171}     % Blue
\definecolor{accent}{RGB}{255,127,0}     % Orange
```

**4. Triadic**: Three evenly spaced colors
- **Pros**: Balanced, vibrant, visually rich
- **Cons**: Can appear busy if not balanced
- **Use**: Multi-topic posters, creative fields

```latex
% Triadic scheme
\definecolor{blue}{RGB}{0,102,204}
\definecolor{red}{RGB}{204,0,51}
\definecolor{yellow}{RGB}{255,204,0}
```

**5. Split-Complementary**: Base + two adjacent to complement
- **Pros**: High contrast but less tense than complementary
- **Cons**: Complex to balance
- **Use**: Sophisticated designs, experienced designers

### High-Contrast Combinations

Ensure readability with sufficient contrast:

**Excellent Contrast (Use these)**:
- Dark blue on white
- Black on white
- White on dark blue/green/purple
- Dark gray on light yellow
- Black on light cyan

**Poor Contrast (Avoid)**:
- ❌ Red on green (color-blind issue)
- ❌ Yellow on white
- ❌ Light gray on white
- ❌ Blue on black (hard to read)
- ❌ Any pure colors on each other

**Contrast Ratio Standards**:
- Minimum: 4.5:1 (WCAG AA)
- Recommended: 7:1 (WCAG AAA)
- Test at: https://webaim.org/resources/contrastchecker/

**LaTeX Color Contrast**:
```latex
% High contrast header
\setbeamercolor{block title}{bg=black, fg=white}

% Medium contrast body
\setbeamercolor{block body}{bg=gray!10, fg=black}

% Check contrast manually or use online tools
```

### Color-Blind Friendly Palettes

~8% of males and ~0.5% of females have color vision deficiency.

**Safe Color Combinations**:
- Blue + Orange (most universally distinguishable)
- Blue + Yellow
- Blue + Red
- Purple + Green (use with caution)

**Avoid**:
- ❌ Red + Green (indistinguishable to most common color blindness)
- ❌ Green + Brown
- ❌ Blue + Purple (can be problematic)
- ❌ Light green + Yellow

**Recommended Palettes**:

**IBM Color Blind Safe** (excellent accessibility):
```latex
\definecolor{ibmblue}{RGB}{100,143,255}
\definecolor{ibmmagenta}{RGB}{254,97,0}
\definecolor{ibmpurple}{RGB}{220,38,127}
\definecolor{ibmcyan}{RGB}{33,191,115}
```

**Okabe-Ito Palette** (scientifically tested):
```latex
\definecolor{okorange}{RGB}{230,159,0}
\definecolor{okskyblue}{RGB}{86,180,233}
\definecolor{okgreen}{RGB}{0,158,115}
\definecolor{okyellow}{RGB}{240,228,66}
\definecolor{okblue}{RGB}{0,114,178}
\definecolor{okvermillion}{RGB}{213,94,0}
\definecolor{okpurple}{RGB}{204,121,167}
```

**Paul Tol's Bright Palette**:
```latex
\definecolor{tolblue}{RGB}{68,119,170}
\definecolor{tolred}{RGB}{204,102,119}
\definecolor{tolgreen}{RGB}{34,136,51}
\definecolor{tolyellow}{RGB}{238,221,136}
\definecolor{tolcyan}{RGB}{102,204,238}
```

### Institutional Branding

Match university or department colors:

```latex
% Example: Stanford colors
\definecolor{stanford-red}{RGB}{140,21,21}
\definecolor{stanford-gray}{RGB}{83,86,90}

% Example: MIT colors
\definecolor{mit-red}{RGB}{163,31,52}
\definecolor{mit-gray}{RGB}{138,139,140}

% Example: Cambridge colors
\definecolor{cambridge-blue}{RGB}{163,193,173}
\definecolor{cambridge-lblue}{RGB}{212,239,223}
```

## Accessibility Considerations

### Universal Design Principles

Design posters usable by the widest range of people:

**1. Visual Accessibility**:
- High contrast text (minimum 4.5:1 ratio)
- Large font sizes (24pt+ body text)
- Color-blind safe palettes
- Clear visual hierarchy
- Avoid relying solely on color to convey information

**2. Cognitive Accessibility**:
- Clear, simple language
- Logical organization
- Consistent layout
- Visual cues for navigation (arrows, numbers)
- Avoid clutter and information overload

**3. Physical Accessibility**:
- Position critical content at wheelchair-accessible height (3-5 feet)
- Include QR codes to digital versions
- Provide printed handouts for detail viewing
- Consider lighting and reflection in poster material choice

### Alternative Text and Descriptions

Make posters accessible to screen readers (for digital versions):

```latex
% Add alt text to figures
\includegraphics[width=\linewidth]{figure.pdf}
% Alternative: Include detailed caption
\caption{Bar graph showing mean±SD of treatment outcomes. 
Control group (blue): 45±5\%; Treatment group (orange): 78±6\%. 
Asterisks indicate significance: *p<0.05, **p<0.01.}
```

### Multi-Modal Information

Don't rely on single sensory channel:

**Use Redundant Encoding**:
- Color + Shape (not just color for categories)
- Color + Pattern (hatching, stippling)
- Color + Label (text labels on graph elements)
- Text + Icons (visual + verbal)

**Example**:
```latex
% Good: Color + shape + label
\begin{tikzpicture}
  \draw[fill=blue, circle] (0,0) circle (0.3) node[right] {Male: 45\%};
  \draw[fill=red, rectangle] (0,-1) rectangle (0.6,-0.4) node[right] {Female: 55\%};
\end{tikzpicture}
```

## Layout Composition

### Rule of Thirds

Divide poster into 3×3 grid; place key elements at intersections:

```
+-----+-----+-----+
|  ×  |     |  ×  |  ← Top third (title, logos)
+-----+-----+-----+
|     |  ×  |     |  ← Middle third (main content)
+-----+-----+-----+
|  ×  |     |  ×  |  ← Bottom third (conclusions)
+-----+-----+-----+
  ↑           ↑
Left        Right
```

**Power Points** (intersections):
- Top-left: Primary section start
- Top-right: Logos, QR codes
- Center: Key figure or main result
- Bottom-right: Conclusions, contact

### Balance and Symmetry

**Symmetric Layouts**:
- Formal, traditional, stable
- Easy to design
- Can appear static or boring
- Good for conservative audiences

**Asymmetric Layouts**:
- Dynamic, modern, interesting
- Harder to execute well
- More visually engaging
- Good for creative fields

**Visual Weight Balance**:
- Large elements = heavy weight
- Dark colors = heavy weight
- Dense text = heavy weight
- Distribute weight evenly across poster

### Proximity and Grouping

**Gestalt Principles**:

**Proximity**: Items close together are perceived as related
```
[Introduction]  [Methods]

[Results]       [Discussion]
```

**Similarity**: Similar items are perceived as grouped
- Use consistent colors for related sections
- Same border styles for similar content types

**Continuity**: Eyes follow lines and paths
- Use arrows to guide through methods
- Align elements to create invisible lines

**Closure**: Mind completes incomplete shapes
- Use partial borders to group without boxing in

## Visual Elements

### Icons and Graphics

Strategic use of icons enhances comprehension:

**Benefits**:
- Universal language (crosses linguistic barriers)
- Faster processing than text
- Adds visual interest
- Clarifies concepts

**Best Practices**:
- Use consistent style (all line, all filled, all flat)
- Appropriate size (1-3cm typical)
- Label ambiguous icons
- Source: Font Awesome, Noun Project, academic icon sets

**LaTeX Implementation**:
```latex
% Font Awesome icons
\usepackage{fontawesome5}
\faFlask{} Methods \quad \faChartBar{} Results

% Custom icons with TikZ
\begin{tikzpicture}
  \node[circle, draw, thick, minimum size=1cm] {\Huge \faAtom};
\end{tikzpicture}
```

### Borders and Dividers

**Use Borders To**:
- Define sections
- Group related content
- Add visual interest
- Match institutional branding

**Border Styles**:
- Solid lines: Traditional, formal
- Dashed lines: Informal, secondary info
- Rounded corners: Friendly, modern
- Drop shadows: Depth, modern (use sparingly)

**Guidelines**:
- Keep consistent width (2-5pt typical)
- Use sparingly (not every element needs a border)
- Match border color to content or theme
- Ensure sufficient padding inside borders

```latex
% tikzposter borders
\usecolorstyle{Denmark}
\tikzposterlatexaffectionproofoff  % Remove bottom-right logo

% Custom border style
\defineblockstyle{CustomBlock}{
  titlewidthscale=1, bodywidthscale=1, titleleft,
  titleoffsetx=0pt, titleoffsety=0pt, bodyoffsetx=0pt, bodyoffsety=0pt,
  bodyverticalshift=0pt, roundedcorners=10, linewidth=2pt,
  titleinnersep=8mm, bodyinnersep=8mm
}{
  \draw[draw=blocktitlebgcolor, fill=blockbodybgcolor, 
        rounded corners=\blockroundedcorners, line width=\blocklinewidth]
       (blockbody.south west) rectangle (blocktitle.north east);
}
```

### Background and Texture

**Background Options**:

**Plain (Recommended)**:
- White or very light color
- Maximum readability
- Professional
- Print-friendly

**Gradient**:
- Subtle gradients acceptable
- Top-to-bottom or radial
- Avoid strong contrasts that interfere with text

**Textured**:
- Very subtle textures only
- Watermarks of logos/molecules (5-10% opacity)
- Avoid patterns that create visual noise

**Avoid**:
- ❌ Busy backgrounds
- ❌ Images behind text
- ❌ High contrast backgrounds
- ❌ Repeating patterns that cause visual artifacts

```latex
% Gradient background in tikzposter
\documentclass{tikzposter}
\definecolorstyle{GradientStyle}{
  % ...color definitions...
}{
  \colorlet{backgroundcolor}{white!90!blue}
  \colorlet{framecolor}{white!70!blue}
}

% Watermark
\usepackage{tikz}
\AddToShipoutPictureBG{
  \AtPageCenter{
    \includegraphics[width=0.5\paperwidth,opacity=0.05]{university-seal.pdf}
  }
}
```

## Common Design Mistakes

### Critical Errors

**1. Too Much Text** (Most common mistake)
- ❌ More than 1000 words
- ❌ Long paragraphs (>5 lines)
- ❌ Small font sizes to fit more content
- ✅ Solution: Cut ruthlessly, use bullet points, focus on key messages

**2. Poor Contrast**
- ❌ Light text on light background
- ❌ Colored text on colored background
- ✅ Solution: Dark on light or light on dark, test contrast ratio

**3. Font Size Too Small**
- ❌ Body text under 24pt
- ❌ Trying to fit full paper content
- ✅ Solution: 30pt+ body text, prioritize key findings

**4. Cluttered Layout**
- ❌ No white space
- ❌ Elements touching edges
- ❌ Random placement
- ✅ Solution: Generous margins, grid alignment, intentional white space

**5. Inconsistent Styling**
- ❌ Multiple font families
- ❌ Varying header styles
- ❌ Misaligned elements
- ✅ Solution: Define style guide, use templates, align to grid

### Moderate Issues

**6. Poor Figure Quality**
- ❌ Pixelated images (<300 DPI)
- ❌ Tiny axis labels
- ❌ Unreadable legends
- ✅ Solution: Vector graphics (PDF/SVG), large labels, clear legends

**7. Color Overload**
- ❌ Too many colors (>5 distinct hues)
- ❌ Neon or overly saturated colors
- ✅ Solution: Limit to 2-3 main colors, use tints/shades for variation

**8. Ignoring Visual Hierarchy**
- ❌ All text same size
- ❌ No clear entry point
- ✅ Solution: Vary sizes significantly, clear title, visual flow

**9. Information Overload**
- ❌ Trying to show everything
- ❌ Too many figures
- ✅ Solution: Show 3-5 key results, link to full paper via QR code

**10. Poor Typography**
- ❌ Justified text (uneven spacing)
- ❌ All caps body text
- ❌ Mixing serif and sans-serif randomly
- ✅ Solution: Left-align body, sentence case, consistent fonts

## Design Checklist

### Before Printing

- [ ] Title visible and readable from 20+ feet
- [ ] Body text minimum 24pt, ideally 30pt+
- [ ] High contrast (4.5:1 minimum) throughout
- [ ] Color-blind friendly palette
- [ ] Less than 800 words total
- [ ] White space around all elements
- [ ] Consistent alignment and spacing
- [ ] All figures high resolution (300+ DPI)
- [ ] Figure labels readable (18pt+ minimum)
- [ ] No orphaned text or awkward breaks
- [ ] Contact information included
- [ ] QR codes tested and functional
- [ ] Consistent font usage (2-3 families max)
- [ ] All acronyms defined
- [ ] Proper institutional branding/logos
- [ ] Print test at 25% scale for readability check

### Content Review

- [ ] Clear narrative arc (problem → approach → findings → impact)
- [ ] 1-3 main messages clearly communicated
- [ ] Methods concise but reproducible
- [ ] Results visually presented (not just text)
- [ ] Conclusions actionable and clear
- [ ] References cited appropriately
- [ ] No typos or grammatical errors
- [ ] Figures have descriptive captions
- [ ] Data visualizations are clear and honest
- [ ] Statistical significance properly indicated

## Evidence-Based Design Recommendations

Research on poster effectiveness shows:

**Findings from Studies**:
1. **Viewers spend 3-5 minutes average** on posters
   - Design for scanning, not deep reading
   - Most important info must be visible immediately

2. **Visual content processed 60,000× faster** than text
   - Use figures, not paragraphs, to convey key findings
   - Images attract attention first

3. **High contrast improves recall** by 40%
   - Dark on light > light on dark for comprehension
   - Color contrast aids memory retention

4. **White space increases comprehension** by 20%
   - Don't fear empty space
   - Margins and padding are essential

5. **Three-column layouts most effective** for portrait posters
   - Balanced visual weight
   - Natural reading flow

6. **QR codes increase engagement** by 30%
   - Provide digital access to full paper
   - Link to videos, code repositories, data

## Resources and Tools

### Color Tools
- **Coolors.co**: Generate color palettes
- **Adobe Color**: Color wheel and accessibility checker
- **ColorBrewer**: Scientific visualization palettes
- **WebAIM Contrast Checker**: Test contrast ratios

### Design Resources
- **Canva**: Poster mockups and inspiration
- **Figma**: Design prototypes before LaTeX
- **Noun Project**: Icons and graphics
- **Font Awesome**: Icon fonts for LaTeX

### Testing Tools
- **Coblis**: Color blindness simulator
- **Vischeck**: Another color blindness checker
- **Accessibility Checker**: WCAG compliance

### LaTeX Packages
- `xcolor`: Extended color support
- `tcolorbox`: Colored boxes and frames
- `fontawesome5`: Icon fonts
- `qrcode`: QR code generation
- `tikz`: Custom graphics

## Conclusion

Effective poster design requires balancing aesthetics, readability, and scientific content. Follow these core principles:

1. **Less is more**: Prioritize key messages over comprehensive detail
2. **Size matters**: Make text large enough to read from distance
3. **Contrast is critical**: Ensure all text is highly readable
4. **Accessibility first**: Design for diverse audiences
5. **Visual hierarchy**: Guide viewers through content logically
6. **Test early**: Print at reduced scale and gather feedback

Remember: A poster is an advertisement for your research and a conversation starter—not a substitute for reading the full paper.

---

## Reference: Poster_Layout_Design

# Poster Layout and Design Guide

## Overview

Effective poster layout organizes content for maximum impact and comprehension. This guide covers grid systems, spatial organization, visual flow, and layout patterns for research posters.

## Grid Systems and Column Layouts

### Common Grid Patterns

#### 1. Two-Column Layout

**Characteristics**:
- Simple, traditional structure
- Easy to design and execute
- Clear narrative flow
- Good for text-heavy content
- Best for A1 size or smaller

**Content Organization**:
```
+-------------------------+
|       Title/Header      |
+-------------------------+
| Column 1  | Column 2    |
|           |             |
| Intro     | Results     |
|           |             |
| Methods   | Discussion  |
|           |             |
|           | Conclusions |
+-------------------------+
|    References/Contact   |
+-------------------------+
```

**LaTeX Implementation (beamerposter)**:
```latex
\begin{columns}[t]
  \begin{column}{.48\linewidth}
    \begin{block}{Introduction}
      % Content
    \end{block}
    \begin{block}{Methods}
      % Content
    \end{block}
  \end{column}
  
  \begin{column}{.48\linewidth}
    \begin{block}{Results}
      % Content
    \end{block}
    \begin{block}{Conclusions}
      % Content
    \end{block}
  \end{column}
\end{columns}
```

**Best For**:
- Small posters (A1, A2)
- Narrative-heavy content
- Simple comparisons (before/after, control/treatment)
- Linear storytelling

**Limitations**:
- Limited space for multiple results
- Can appear basic or dated
- Less visual variety

#### 2. Three-Column Layout (Most Popular)

**Characteristics**:
- Balanced, professional appearance
- Optimal for A0 posters
- Versatile content distribution
- Natural visual rhythm
- Industry standard

**Content Organization**:
```
+--------------------------------+
|          Title/Header          |
+--------------------------------+
| Column 1  | Column 2 | Column 3|
|           |          |         |
| Intro     | Results  | Results |
|           | (Fig 1)  | (Fig 2) |
| Methods   |          |         |
|           | Results  | Discuss |
| Methods   | (Fig 3)  |         |
| (cont.)   |          | Concl.  |
+--------------------------------+
|     Acknowledgments/Refs       |
+--------------------------------+
```

**LaTeX Implementation (tikzposter)**:
```latex
\begin{columns}
  \column{0.33}
  \block{Introduction}{...}
  \block{Methods}{...}
  
  \column{0.33}
  \block{Results Part 1}{...}
  \block{Results Part 2}{...}
  
  \column{0.33}
  \block{Results Part 3}{...}
  \block{Discussion}{...}
  \block{Conclusions}{...}
\end{columns}
```

**Best For**:
- Standard A0 conference posters
- Multiple results/figures (4-6)
- Balanced content distribution
- Professional academic presentations

**Strengths**:
- Visual balance and symmetry
- Adequate space for text and figures
- Clear section delineation
- Easy to scan left-to-right

#### 3. Four-Column Layout

**Characteristics**:
- Information-dense
- Modern, structured appearance
- Best for large posters (>A0)
- Requires careful design
- More complex to balance

**Content Organization**:
```
+----------------------------------------+
|             Title/Header               |
+----------------------------------------+
| Col 1  | Col 2  | Col 3    | Col 4    |
|        |        |          |          |
| Intro  | Method | Results  | Results  |
|        | (Flow) | (Fig 1)  | (Fig 3)  |
| Motiv. |        |          |          |
|        | Method | Results  | Discuss. |
| Hypoth.| (Stats)| (Fig 2)  |          |
|        |        |          | Concl.   |
+----------------------------------------+
|          References/Contact            |
+----------------------------------------+
```

**LaTeX Implementation (baposter)**:
```latex
\begin{poster}{columns=4, colspacing=1em, ...}
  
  \headerbox{Intro}{name=intro, column=0, row=0}{...}
  \headerbox{Methods}{name=methods, column=1, row=0}{...}
  \headerbox{Results 1}{name=res1, column=2, row=0}{...}
  \headerbox{Results 2}{name=res2, column=3, row=0}{...}
  
  % Continue with below=... for stacking
  
\end{poster}
```

**Best For**:
- Large format posters (48×72")
- Data-heavy presentations
- Comparison studies (multiple conditions)
- Engineering/technical posters

**Challenges**:
- Can appear crowded
- Requires more white space management
- Harder to achieve visual balance
- Risk of overwhelming viewers

#### 4. Asymmetric Layouts

**Characteristics**:
- Dynamic, modern appearance
- Flexible content arrangement
- Emphasizes hierarchy
- Requires design expertise
- Best for creative fields

**Example Pattern**:
```
+--------------------------------+
|          Title/Header          |
+--------------------------------+
| Wide Column  | Narrow Column   |
| (66%)        | (33%)           |
|              |                 |
| Intro +      | Key             |
| Methods      | Figure          |
| (narrative)  | (emphasized)    |
|              |                 |
+--------------------------------+
| Results (spanning full width)  |
+--------------------------------+
| Discussion   | Conclusions     |
| (50%)        | (50%)           |
+--------------------------------+
```

**LaTeX Implementation (tikzposter)**:
```latex
\begin{columns}
  \column{0.65}
  \block{Introduction and Methods}{
    % Combined narrative section
  }
  
  \column{0.35}
  \block{}{
    % Key figure with minimal text
    \includegraphics[width=\linewidth]{key-figure.pdf}
  }
\end{columns}

\block[width=1.0\linewidth]{Results}{
  % Full-width results section
}
```

**Best For**:
- Design-oriented conferences
- Single key finding with supporting content
- Modern, non-traditional fields
- Experienced poster designers

### Grid Alignment Principles

**Baseline Grid**:
- Establish invisible horizontal lines
- Align all text blocks to grid
- Typical spacing: 5mm or 10mm increments
- Creates visual rhythm and professionalism

**Column Grid**:
- Divide width into equal units (12, 16, or 24 units common)
- Elements span multiple units
- Allows flexible but structured layouts

**Example 12-Column Grid**:
```
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |
|-------|-------|-------|-------|-------|-------|
| Block spanning 6 units| Block spanning 6 units|
|               Block spanning 12 units          |
| 4 units  | 8 units (emphasized)               |
```

**LaTeX Grid Helper**:
```latex
% Debug grid overlay (remove for final version)
\usepackage{tikz}
\AddToShipoutPictureBG{
  \begin{tikzpicture}[remember picture, overlay]
    \draw[help lines, step=5cm, very thin, gray!30] 
      (current page.south west) grid (current page.north east);
  \end{tikzpicture}
}
```

## Visual Flow and Reading Patterns

### Z-Pattern (Landscape Posters)

Viewers' eyes naturally follow a Z-shape on landscape layouts:

```
START → → → → → → → → → → → → → → TOP RIGHT
  ↓                                    ↓
  ↓                                    ↓
MIDDLE LEFT → → → → → → → → → MIDDLE RIGHT
  ↓                                    ↓
  ↓                                    ↓
BOTTOM LEFT → → → → → → → → → → → → END
```

**Design Strategy**:
1. **Top-left**: Title and introduction (entry point)
2. **Top-right**: Institution logo, QR code
3. **Center**: Key result or main figure
4. **Bottom-right**: Conclusions and contact (exit point)

**Content Placement**:
- Critical information at corners and center
- Support information along diagonal paths
- Use arrows or visual cues to reinforce flow

### F-Pattern (Portrait Posters)

Portrait posters follow F-shaped eye movement:

```
TITLE → → → → → → → → → → → →
  ↓
INTRO → → → →
  ↓
METHODS
  ↓
RESULTS → → →
  ↓
RESULTS (cont.)
  ↓
DISCUSSION
  ↓
CONCLUSIONS → → → → → → → → →
```

**Design Strategy**:
1. Place engaging content at top-left
2. Use section headers to create horizontal scan points
3. Most important figures in upper-middle area
4. Conclusions visible without scrolling (if digital) or from distance

### Gutenberg Diagram

Classic newspaper layout principle:

```
+------------------+------------------+
| PRIMARY AREA     | STRONG FALLOW    |
| (most attention) | (moderate attn)  |
|   ↓              |        ↓         |
+------------------+------------------+
| WEAK FALLOW      | TERMINAL AREA    |
| (least attention)| (final resting)  |
|                  |        ↑         |
+------------------+------------------+
```

**Optimization**:
- **Primary Area** (top-left): Introduction, problem statement
- **Strong Fallow** (top-right): Supporting figure, logo
- **Weak Fallow** (bottom-left): Methods details, references
- **Terminal Area** (bottom-right): Conclusions, take-home message

### Directional Cues

Guide viewers explicitly through content:

**Numerical Ordering**:
```latex
\block{❶ Introduction}{...}
\block{❷ Methods}{...}
\block{❸ Results}{...}
\block{❹ Conclusions}{...}
```

**Arrows and Lines**:
```latex
\begin{tikzpicture}
  \node[block] (intro) {Introduction};
  \node[block, right=of intro] (methods) {Methods};
  \node[block, right=of methods] (results) {Results};
  \draw[->, thick, blue] (intro) -- (methods);
  \draw[->, thick, blue] (methods) -- (results);
\end{tikzpicture}
```

**Color Progression**:
- Light to dark shades indicating progression
- Cool to warm colors showing importance increase
- Consistent color for related sections

## Spatial Organization Strategies

### Header/Title Area

**Typical Size**: 10-15% of total poster height

**Essential Elements**:
- **Title**: Concise, descriptive (10-15 words max)
- **Authors**: Full names, presenting author emphasized
- **Affiliations**: Institutions, departments
- **Logos**: University, funding agencies (2-4 max)
- **Conference info** (optional): Name, date, location

**Layout Options**:

**Centered**:
```
+----------------------------------------+
|  [Logo]    POSTER TITLE HERE    [Logo]|
|         Authors and Affiliations       |
|           email@university.edu         |
+----------------------------------------+
```

**Left-aligned**:
```
+----------------------------------------+
| POSTER TITLE HERE            [Logo]   |
| Authors and Affiliations     [Logo]   |
+----------------------------------------+
```

**Split**:
```
+----------------------------------------+
| [Logo]           | Authors & Affil.    |
| POSTER TITLE     | email@edu          |
|                  | [QR Code]          |
+----------------------------------------+
```

**LaTeX Header (beamerposter)**:
```latex
\begin{columns}[T]
  \begin{column}{.15\linewidth}
    \includegraphics[width=\linewidth]{logo1.pdf}
  \end{column}
  
  \begin{column}{.7\linewidth}
    \centering
    {\VeryHuge\textbf{Your Research Title Here}}\\[0.5cm]
    {\Large Author One\textsuperscript{1}, Author Two\textsuperscript{2}}\\[0.3cm]
    {\normalsize \textsuperscript{1}University A, \textsuperscript{2}University B}
  \end{column}
  
  \begin{column}{.15\linewidth}
    \includegraphics[width=\linewidth]{logo2.pdf}
  \end{column}
\end{columns}
```

### Main Content Area

**Typical Size**: 70-80% of total poster

**Organization Principles**:

**1. Top-to-Bottom Flow**:
```
Introduction/Background
        ↓
Methods/Approach
        ↓
Results (Multiple panels)
        ↓
Discussion/Conclusions
```

**2. Left-to-Right, Top-to-Bottom**:
```
[Intro] [Results 1] [Results 3]
[Methods] [Results 2] [Discussion]
```

**3. Centralized Main Figure**:
```
[Intro]  [Main Figure]  [Discussion]
[Methods]   (center)    [Conclusions]
```

**Section Sizing**:
- Introduction: 10-15% of content area
- Methods: 15-20%
- Results: 40-50% (largest section)
- Discussion/Conclusions: 15-20%

### Footer Area

**Typical Size**: 5-10% of total poster height

**Common Elements**:
- References (abbreviated, 5-10 key citations)
- Acknowledgments (funding, collaborators)
- Contact information
- QR codes (paper, code, data)
- Social media handles (optional)
- Conference hashtags

**Layout**:
```
+----------------------------------------+
| References: 1. Author (2023) ... |  📱  |
| Acknowledgments: Funded by ...   | QR   |
| Contact: name@email.edu          | Code |
+----------------------------------------+
```

**LaTeX Footer**:
```latex
\begin{block}{}
  \footnotesize
  \begin{columns}[T]
    \begin{column}{0.7\linewidth}
      \textbf{References}
      \begin{enumerate}
        \item Author A et al. (2023). Journal. doi:...
        \item Author B et al. (2024). Conference.
      \end{enumerate}
      
      \textbf{Acknowledgments}
      This work was supported by Grant XYZ.
      
      \textbf{Contact}: firstname.lastname@university.edu
    \end{column}
    
    \begin{column}{0.25\linewidth}
      \centering
      \qrcode[height=3cm]{https://doi.org/10.1234/paper}\\
      \tiny Scan for full paper
    \end{column}
  \end{columns}
\end{block}
```

## White Space Management

### Margins and Padding

**Outer Margins**:
- Minimum: 2-3cm (0.75-1 inch)
- Recommended: 3-5cm (1-2 inches)
- Prevents edge trimming issues in printing
- Provides visual breathing room

**Inner Spacing**:
- Between columns: 1-2cm
- Between blocks: 1-2cm
- Inside blocks (padding): 0.5-1.5cm
- Around figures: 0.5-1cm

**LaTeX Margin Control**:
```latex
% beamerposter
\usepackage[size=a0, scale=1.4]{beamerposter}
\setbeamersize{text margin left=3cm, text margin right=3cm}

% tikzposter
\documentclass[..., margin=30mm, innermargin=15mm]{tikzposter}

% baposter
\begin{poster}{
  colspacing=1.5em,  % Horizontal spacing
  ...
}
```

### Active White Space vs. Passive White Space

**Active White Space**: Intentionally placed for specific purpose
- Around key figures (draws attention)
- Between major sections (creates clear separation)
- Above/below titles (emphasizes hierarchy)

**Passive White Space**: Natural result of layout
- Margins and borders
- Line spacing
- Gaps between elements

**Balance**: Aim for 30-40% white space overall

### Visual Breathing Room

**Avoid**:
- ❌ Elements touching edges
- ❌ Text blocks directly adjacent
- ❌ Figures without surrounding space
- ❌ Cramped, claustrophobic feel

**Implement**:
- ✅ Clear separation between sections
- ✅ Space around focal points
- ✅ Generous padding inside boxes
- ✅ Balanced distribution of content

## Block and Box Design

### Block Types and Functions

**Title Block**: Poster header
- Full width, top position
- High visual weight
- Contains identifying information

**Content Blocks**: Main sections
- Column-based or free-floating
- Hierarchical sizing (larger = more important)
- Clear headers and structure

**Callout Blocks**: Emphasized information
- Key findings or quotes
- Different color or style
- Visually distinct

**Reference Blocks**: Supporting info
- Footer position
- Smaller, less prominent
- Informational, not critical

### Block Styling Options

**Border Styles**:
```latex
% Rounded corners (friendly, modern)
\begin{block}{Title}
  % beamerposter with rounded
  \setbeamertemplate{block begin}[rounded]
  
% Sharp corners (formal, traditional)
  \setbeamertemplate{block begin}[default]

% No border (minimal, clean)
  \setbeamercolor{block title}{bg=white, fg=black}
  \setbeamercolor{block body}{bg=white, fg=black}
```

**Shadow and Depth**:
```latex
% tikzposter shadow
\tikzset{
  block/.append style={
    drop shadow={shadow xshift=2mm, shadow yshift=-2mm}
  }
}

% tcolorbox drop shadow
\usepackage{tcolorbox}
\begin{tcolorbox}[enhanced, drop shadow]
  Content with shadow
\end{tcolorbox}
```

**Background Shading**:
- **Solid**: Clean, professional
- **Gradient**: Modern, dynamic
- **Transparent**: Layered, sophisticated

### Relationship and Grouping

**Visual Grouping Techniques**:

**1. Proximity**: Place related items close
```
[Intro Text]
[Related Figure]
    ↓ grouped
[Methods Text]
[Methods Diagram]
```

**2. Color Coding**: Use color to show relationships
- All "Methods" blocks in blue
- All "Results" blocks in green
- Conclusions in orange

**3. Borders**: Enclose related elements
```latex
\begin{tcolorbox}[title=Experimental Pipeline]
  \begin{enumerate}
    \item Sample preparation
    \item Data collection
    \item Analysis
  \end{enumerate}
\end{tcolorbox}
```

**4. Alignment**: Aligned elements appear related
```
[Block A Left-aligned]
[Block B Left-aligned]
    vs.
[Block C Centered]
```

## Responsive and Adaptive Layouts

### Designing for Different Poster Sizes

**Scaling Strategy**:
- Design for target size (e.g., A0)
- Test at other common sizes (A1, 36×48")
- Use relative sizing (percentages, not absolute)

**Font Scaling**:
```latex
% Scale fonts proportionally
\usepackage[size=a0, scale=1.4]{beamerposter}  % A0 at 140%
\usepackage[size=a1, scale=1.0]{beamerposter}  % A1 at 100%

% Or define sizes relatively
\newcommand{\titlesize}{\fontsize{96}{110}\selectfont}
\newcommand{\headersize}{\fontsize{60}{72}\selectfont}
```

**Content Adaptation**:
- **A0 (full)**: All content, 5-6 figures
- **A1 (reduced)**: Condense to 3-4 main figures
- **A2 (compact)**: Key finding only, 1-2 figures

### Portrait vs. Landscape Orientation

**Portrait (Vertical)**:
- **Pros**: Traditional, more common stands, natural reading flow
- **Cons**: Less width for figures, can feel cramped
- **Best for**: Text-heavy posters, multi-section flow, conferences

**Landscape (Horizontal)**:
- **Pros**: Wide figures, natural for timelines, modern feel
- **Cons**: Harder to read from distance, less common
- **Best for**: Timelines, wide data visualizations, non-traditional venues

**LaTeX Orientation**:
```latex
% Portrait
\usepackage[size=a0, orientation=portrait]{beamerposter}
\documentclass[..., portrait]{tikzposter}

% Landscape
\usepackage[size=a0, orientation=landscape]{beamerposter}
\documentclass[..., landscape]{tikzposter}
```

## Layout Patterns by Research Type

### Experimental Research

**Typical Flow**:
```
[Title and Authors]
+---------------------------+
| Background | Methods      |
| Problem    | (Diagram)    |
+---------------------------+
| Results (Figure 1)        |
| Results (Figure 2)        |
+---------------------------+
| Discussion | Conclusions  |
| Limitations| Future Work  |
+---------------------------+
[References and Contact]
```

**Emphasis**: Visual results, clear methodology

### Computational/Modeling

**Typical Flow**:
```
[Title and Authors]
+---------------------------+
| Motivation | Algorithm    |
|            | (Flowchart)  |
+---------------------------+
| Implementation Details    |
+---------------------------+
| Results    | Results      |
| (Benchmark)| (Comparison) |
+---------------------------+
| Conclusions| Code QR      |
+---------------------------+
[GitHub, Docker, Documentation]
```

**Emphasis**: Algorithm clarity, reproducibility

### Clinical/Medical

**Typical Flow**:
```
[Title and Authors]
+---------------------------+
| Background | Methods      |
| Clinical   | - Design     |
| Need       | - Population |
|            | - Outcomes   |
+---------------------------+
| Results               |    |
| (Primary Outcome)     | Key|
|                       | Fig|
+---------------------------+
| Discussion | Clinical     |
|            | Implications |
+---------------------------+
[Trial Registration, Ethics, Funding]
```

**Emphasis**: Patient outcomes, clinical relevance

### Review/Meta-Analysis

**Typical Flow**:
```
[Title and Authors]
+---------------------------+
| Research  | Search        |
| Question  | Strategy      |
|           | (PRISMA Flow) |
+---------------------------+
| Included Studies Overview |
+---------------------------+
| Findings  | Findings      |
| (Theme 1) | (Theme 2)     |
+---------------------------+
| Synthesis | Gaps &        |
|           | Future Needs  |
+---------------------------+
[Systematic Review Registration]
```

**Emphasis**: Comprehensive coverage, synthesis

## Layout Testing and Iteration

### Design Iteration Process

**1. Sketch Phase**:
- Hand-draw rough layout
- Experiment with different arrangements
- Mark primary, secondary, tertiary content

**2. Digital Mockup**:
- Create low-fidelity version in LaTeX
- Use placeholder text/figures
- Test different grid systems

**3. Content Integration**:
- Replace placeholders with actual content
- Adjust spacing and sizing
- Refine visual hierarchy

**4. Refinement**:
- Fine-tune alignment
- Balance visual weight
- Optimize white space

**5. Testing**:
- Print at reduced scale (25%)
- View from distance
- Get colleague feedback

### Feedback Checklist

**Visual Balance**:
- [ ] No single area feels too heavy or too light
- [ ] Color distributed evenly across poster
- [ ] Text and figures balanced
- [ ] White space well-distributed

**Hierarchy and Flow**:
- [ ] Clear entry point (title visible)
- [ ] Logical reading path
- [ ] Section relationships clear
- [ ] Conclusions easy to find

**Technical Execution**:
- [ ] Consistent alignment
- [ ] Uniform spacing
- [ ] Professional appearance
- [ ] No awkward breaks or orphans

## Common Layout Mistakes

**1. Unbalanced Visual Weight**
- ❌ All content on left, empty right side
- ❌ Large figure dominating, tiny text elsewhere
- ✅ Distribute content evenly across poster

**2. Inconsistent Spacing**
- ❌ Random gaps between blocks
- ❌ Elements touching in some places, spaced in others
- ✅ Use consistent spacing values throughout

**3. Poor Column Width**
- ❌ Extremely narrow columns (hard to read)
- ❌ Very wide columns (eye tracking difficult)
- ✅ Optimal: 40-80 characters per line

**4. Ignoring Grid**
- ❌ Random placement of elements
- ❌ Misaligned blocks
- ✅ Align to invisible grid, consistent positioning

**5. Overcrowding**
- ❌ No white space, cramped feel
- ❌ Trying to fit too much content
- ✅ Generous margins, clear separation

## Conclusion

Effective layout design:
- Uses appropriate grid systems (2, 3, or 4 columns)
- Follows natural eye movement patterns
- Maintains visual balance and hierarchy
- Provides adequate white space
- Groups related content clearly
- Adapts to different poster sizes and orientations

Remember: Layout should support content, not compete with it. When viewers focus on your research rather than your design, you've succeeded.
