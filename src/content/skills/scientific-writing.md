---
title: "Scientific Writing"
description: "Core skill for the deep research and writing tool. Write scientific manuscripts in full paragraphs (never bullet points). Use two-stage process with (1) section outlines with key points using research-lookup then (2) convert to flowing prose. IMRA..."
category: "research"
source: "community"
author: "Community"
tags: ["scientific", "writing"]
date: 2026-03-20
---

# Scientific Writing

## Overview

**This is the core skill for the deep research and writing tool**—combining AI-driven deep research with well-formatted written outputs. Every document produced is backed by comprehensive literature search and verified citations through the research-lookup skill.

Scientific writing is a process for communicating research with precision and clarity. Write manuscripts using IMRAD structure, citations (APA/AMA/Vancouver), figures/tables, and reporting guidelines (CONSORT/STROBE/PRISMA). Apply this skill for research papers and journal submissions.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in the final manuscript.** Use a two-stage process: first create section outlines with key points using research-lookup, then convert those outlines into complete paragraphs.

## When to Use This Skill

This skill should be used when:
- Writing or revising any section of a scientific manuscript (abstract, introduction, methods, results, discussion)
- Structuring a research paper using IMRAD or other standard formats
- Formatting citations and references in specific styles (APA, AMA, Vancouver, Chicago, IEEE)
- Creating, formatting, or improving figures, tables, and data visualizations
- Applying study-specific reporting guidelines (CONSORT for trials, STROBE for observational studies, PRISMA for reviews)
- Drafting abstracts that meet journal requirements (structured or unstructured)
- Preparing manuscripts for submission to specific journals
- Improving writing clarity, conciseness, and precision
- Ensuring proper use of field-specific terminology and nomenclature
- Addressing reviewer comments and revising manuscripts

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every scientific paper MUST include a graphical abstract plus 1-2 additional AI-generated figures using the scientific-schematics skill.**

This is not optional. Scientific papers without visual elements are incomplete. Before finalizing any document:
1. **ALWAYS generate a graphical abstract** as the first visual element
2. Generate at minimum ONE additional schematic or diagram using scientific-schematics
3. Prefer 3-4 total figures for comprehensive papers (graphical abstract + methods flowchart + results visualization + conceptual diagram)

### Graphical Abstract (REQUIRED)

**Every scientific writeup MUST include a graphical abstract.** This is a visual summary of your paper that:
- Appears before or immediately after the text abstract
- Captures the entire paper's key message in one image
- Is suitable for journal table of contents display
- Uses landscape orientation (typically 1200x600px)

**Generate the graphical abstract FIRST:**
```bash
python scripts/generate_schematic.py "Graphical abstract for [paper title]: [brief description showing workflow from input → methods → key findings → conclusions]" -o figures/graphical_abstract.png
```

**Graphical Abstract Requirements:**
- **Content**: Visual summary showing workflow, key methods, main findings, and conclusions
- **Style**: Clean, professional, suitable for journal TOC
- **Elements**: Include 3-5 key steps/concepts with connecting arrows or flow
- **Text**: Minimal labels, large readable fonts
- Log: `[HH:MM:SS] GENERATED: Graphical abstract for paper summary`

### Additional Figures (GENERATE EXTENSIVELY)

**⚠️ CRITICAL: Use BOTH scientific-schematics AND generate-image EXTENSIVELY throughout all documents.**

Every document should be richly illustrated. Generate figures liberally - when in doubt, add a visual.

**MINIMUM Figure Requirements:**

| Document Type | Minimum | Recommended |
|--------------|---------|-------------|
| Research Papers | 5 | 6-8 |
| Literature Reviews | 4 | 5-7 |
| Market Research | 20 | 25-30 |
| Presentations | 1/slide | 1-2/slide |
| Posters | 6 | 8-10 |
| Grants | 4 | 5-7 |
| Clinical Reports | 3 | 4-6 |

**Use scientific-schematics EXTENSIVELY for technical diagrams:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

- Study design and methodology flowcharts (CONSORT, PRISMA, STROBE)
- Conceptual framework diagrams
- Experimental workflow illustrations
- Data analysis pipeline diagrams
- Biological pathway or mechanism diagrams
- System architecture visualizations
- Neural network architectures
- Decision trees, algorithm flowcharts
- Comparison matrices, timeline diagrams
- Any technical concept that benefits from schematic visualization

**Use generate-image EXTENSIVELY for visual content:**
```bash
python scripts/generate_image.py "your image description" -o figures/output.png
```

- Photorealistic illustrations of concepts
- Medical/anatomical illustrations
- Environmental/ecological scenes
- Equipment and lab setup visualizations
- Artistic visualizations, infographics
- Cover images, header graphics
- Product mockups, prototype visualizations
- Any visual that enhances understanding or engagement

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When in Doubt, Generate a Figure:**
- Complex concept → generate a schematic
- Data discussion → generate a visualization
- Process description → generate a flowchart
- Comparison → generate a comparison diagram
- Reader benefit → generate a visual

For detailed guidance, refer to the scientific-schematics and generate-image skill documentation.

---

## Core Capabilities

### 1. Manuscript Structure and Organization

**IMRAD Format**: Guide papers through the standard Introduction, Methods, Results, And Discussion structure used across most scientific disciplines. This includes:
- **Introduction**: Establish research context, identify gaps, state objectives
- **Methods**: Detail study design, populations, procedures, and analysis approaches
- **Results**: Present findings objectively without interpretation
- **Discussion**: Interpret results, acknowledge limitations, propose future directions

For detailed guidance on IMRAD structure, refer to `references/imrad_structure.md`.

**Alternative Structures**: Support discipline-specific formats including:
- Review articles (narrative, systematic, scoping)
- Case reports and case series
- Meta-analyses and pooled analyses
- Theoretical/modeling papers
- Methods papers and protocols

### 2. Section-Specific Writing Guidance

**Abstract Composition**: Craft concise, standalone summaries (100-250 words) that capture the paper's purpose, methods, results, and conclusions. Support both structured abstracts (with labeled sections) and unstructured single-paragraph formats.

**Introduction Development**: Build compelling introductions that:
- Establish the research problem's importance
- Review relevant literature systematically
- Identify knowledge gaps or controversies
- State clear research questions or hypotheses
- Explain the study's novelty and significance

**Methods Documentation**: Ensure reproducibility through:
- Detailed participant/sample descriptions
- Clear procedural documentation
- Statistical methods with justification
- Equipment and materials specifications
- Ethical approval and consent statements

**Results Presentation**: Present findings with:
- Logical flow from primary to secondary outcomes
- Integration with figures and tables
- Statistical significance with effect sizes
- Objective reporting without interpretation

**Discussion Construction**: Synthesize findings by:
- Relating results to research questions
- Comparing with existing literature
- Acknowledging limitations honestly
- Proposing mechanistic explanations
- Suggesting practical implications and future research

### 3. Citation and Reference Management

Apply citation styles correctly across disciplines. For comprehensive style guides, refer to `references/citation_styles.md`.

**Major Citation Styles:**
- **AMA (American Medical Association)**: Numbered superscript citations, common in medicine
- **Vancouver**: Numbered citations in square brackets, biomedical standard
- **APA (American Psychological Association)**: Author-date in-text citations, common in social sciences
- **Chicago**: Notes-bibliography or author-date, humanities and sciences
- **IEEE**: Numbered square brackets, engineering and computer science

**Best Practices:**
- Cite primary sources when possible
- Include recent literature (last 5-10 years for active fields)
- Balance citation distribution across introduction and discussion
- Verify all citations against original sources
- Use reference management software (Zotero, Mendeley, EndNote)

### 4. Figures and Tables

Create effective data visualizations that enhance comprehension. For detailed best practices, refer to `references/figures_tables.md`.

**When to Use Tables vs. Figures:**
- **Tables**: Precise numerical data, complex datasets, multiple variables requiring exact values
- **Figures**: Trends, patterns, relationships, comparisons best understood visually

**Design Principles:**
- Make each table/figure self-explanatory with complete captions
- Use consistent formatting and terminology across all display items
- Label all axes, columns, and rows with units
- Include sample sizes (n) and statistical annotations
- Follow the "one table/figure per 1000 words" guideline
- Avoid duplicating information between text, tables, and figures

**Common Figure Types:**
- Bar graphs: Comparing discrete categories
- Line graphs: Showing trends over time
- Scatterplots: Displaying correlations
- Box plots: Showing distributions and outliers
- Heatmaps: Visualizing matrices and patterns

### 5. Reporting Guidelines by Study Type

Ensure completeness and transparency by following established reporting standards. For comprehensive guideline details, refer to `references/reporting_guidelines.md`.

**Key Guidelines:**
- **CONSORT**: Randomized controlled trials
- **STROBE**: Observational studies (cohort, case-control, cross-sectional)
- **PRISMA**: Systematic reviews and meta-analyses
- **STARD**: Diagnostic accuracy studies
- **TRIPOD**: Prediction model studies
- **ARRIVE**: Animal research
- **CARE**: Case reports
- **SQUIRE**: Quality improvement studies
- **SPIRIT**: Study protocols for clinical trials
- **CHEERS**: Economic evaluations

Each guideline provides checklists ensuring all critical methodological elements are reported.

### 6. Writing Principles and Style

Apply fundamental scientific writing principles. For detailed guidance, refer to `references/writing_principles.md`.

**Clarity**:
- Use precise, unambiguous language
- Define technical terms and abbreviations at first use
- Maintain logical flow within and between paragraphs
- Use active voice when appropriate for clarity

**Conciseness**:
- Eliminate redundant words and phrases
- Favor shorter sentences (15-20 words average)
- Remove unnecessary qualifiers
- Respect word limits strictly

**Accuracy**:
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish between observations and interpretations
- Acknowledge uncertainty appropriately

**Objectivity**:
- Present results without bias
- Avoid overstating findings or implications
- Acknowledge conflicting evidence
- Maintain professional, neutral tone

### 7. Writing Process: From Outline to Full Paragraphs

**CRITICAL: Always write in full paragraphs, never submit bullet points in scientific papers.**

Scientific papers must be written in complete, flowing prose. Use this two-stage approach for effective writing:

**Stage 1: Create Section Outlines with Key Points**

When starting a new section:
1. Use the research-lookup skill to gather relevant literature and data
2. Create a structured outline with bullet points marking:
   - Main arguments or findings to present
   - Key studies to cite
   - Data points and statistics to include
   - Logical flow and organization
3. These bullet points serve as scaffolding—they are NOT the final manuscript

**Example outline (Introduction section):**
```
- Background: AI in drug discovery gaining traction
  * Cite recent reviews (Smith 2023, Jones 2024)
  * Traditional methods are slow and expensive
- Gap: Limited application to rare diseases
  * Only 2 prior studies (Lee 2022, Chen 2023)
  * Small datasets remain a challenge
- Our approach: Transfer learning from common diseases
  * Novel architecture combining X and Y
- Study objectives: Validate on 3 rare disease datasets
```

**Stage 2: Convert Key Points to Full Paragraphs**

Once the outline is complete, expand each bullet point into proper prose:

1. **Transform bullet points into complete sentences** with subjects, verbs, and objects
2. **Add transitions** between sentences and ideas (however, moreover, in contrast, subsequently)
3. **Integrate citations naturally** within sentences, not as lists
4. **Expand with context and explanation** that bullet points omit
5. **Ensure logical flow** from one sentence to the next within each paragraph
6. **Vary sentence structure** to maintain reader engagement

**Example conversion to prose:**

```
Artificial intelligence approaches have gained significant traction in drug discovery 
pipelines over the past decade (Smith, 2023; Jones, 2024). While these computational 
methods show promise for accelerating the identification of therapeutic candidates, 
traditional experimental approaches remain slow and resource-intensive, often requiring 
years of laboratory work and substantial financial investment. However, the application 
of AI to rare diseases has been limited, with only two prior studies demonstrating 
proof-of-concept results (Lee, 2022; Chen, 2023). The primary obstacle has been the 
scarcity of training data for conditions affecting small patient populations. 

To address this challenge, we developed a transfer learning approach that leverages 
knowledge from well-characterized common diseases to predict therapeutic targets for 
rare conditions. Our novel neural architecture combines convolutional layers for 
molecular feature extraction with attention mechanisms for protein-ligand interaction 
modeling. The objective of this study was to validate our approach across three 
independent rare disease datasets, assessing both predictive accuracy and biological 
interpretability of the results.
```

**Key Differences Between Outlines and Final Text:**

| Outline (Planning Stage) | Final Manuscript |
|--------------------------|------------------|
| Bullet points and fragments | Complete sentences and paragraphs |
| Telegraphic notes | Full explanations with context |
| List of citations | Citations integrated into prose |
| Abbreviated ideas | Developed arguments with transitions |
| For your eyes only | For publication and peer review |

**Common Mistakes to Avoid:**

- ❌ **Never** leave bullet points in the final manuscript
- ❌ **Never** submit lists where paragraphs should be
- ❌ **Don't** use numbered or bulleted lists in Results or Discussion sections (except for specific cases like study hypotheses or inclusion criteria)
- ❌ **Don't** write sentence fragments or incomplete thoughts
- ✅ **Do** use occasional lists only in Methods (e.g., inclusion/exclusion criteria, materials lists)
- ✅ **Do** ensure every section flows as connected prose
- ✅ **Do** read paragraphs aloud to check for natural flow

**When Lists ARE Acceptable (Limited Cases):**

Lists may appear in scientific papers only in specific contexts:
- **Methods**: Inclusion/exclusion criteria, materials and reagents, participant characteristics
- **Supplementary Materials**: Extended protocols, equipment lists, detailed parameters
- **Never in**: Abstract, Introduction, Results, Discussion, Conclusions

**Abstract Format Rule:**
- ❌ **NEVER** use labeled sections (Background:, Methods:, Results:, Conclusions:)
- ✅ **ALWAYS** write as flowing paragraph(s) with natural transitions
- Exception: Only use structured format if journal explicitly requires it in author guidelines

**Integration with Research Lookup:**

The research-lookup skill is essential for Stage 1 (creating outlines):
1. Search for relevant papers using research-lookup
2. Extract key findings, methods, and data
3. Organize findings as bullet points in your outline
4. Then convert the outline to full paragraphs in Stage 2

This two-stage process ensures you:
- Gather and organize information systematically
- Create logical structure before writing
- Produce polished, publication-ready prose
- Maintain focus on the narrative flow

### 8. Professional Report Formatting (Non-Journal Documents)

For research reports, technical reports, white papers, and other professional documents that are NOT journal manuscripts, use the `scientific_report.sty` LaTeX style package for a polished, professional appearance.

**When to Use Professional Report Formatting:**
- Research reports and technical reports
- White papers and policy briefs
- Grant reports and progress reports
- Industry reports and technical documentation
- Internal research summaries
- Feasibility studies and project deliverables

**When NOT to Use (Use Venue-Specific Formatting Instead):**
- Journal manuscripts → Use `venue-templates` skill
- Conference papers → Use `venue-templates` skill
- Academic theses → Use institutional templates

**The `scientific_report.sty` Style Package Provides:**

| Feature | Description |
|---------|-------------|
| Typography | Helvetica font family for modern, professional appearance |
| Color Scheme | Professional blues, greens, and accent colors |
| Box Environments | Colored boxes for key findings, methods, recommendations, limitations |
| Tables | Alternating row colors, professional headers |
| Figures | Consistent caption formatting |
| Scientific Commands | Shortcuts for p-values, effect sizes, confidence intervals |

**Box Environments for Content Organization:**

```latex
% Key findings (blue) - for major discoveries
\begin{keyfindings}[Title]
Content with key findings and statistics.
\end{keyfindings}

% Methodology (green) - for methods highlights
\begin{methodology}[Study Design]
Description of methods and procedures.
\end{methodology}

% Recommendations (purple) - for action items
\begin{recommendations}[Clinical Implications]
\begin{enumerate}
    \item Specific recommendation 1
    \item Specific recommendation 2
\end{enumerate}
\end{recommendations}

% Limitations (orange) - for caveats and cautions
\begin{limitations}[Study Limitations]
Description of limitations and their implications.
\end{limitations}
```

**Professional Table Formatting:**

```latex
\begin{table}[htbp]
\centering
\caption{Results Summary}
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Variable} & \textbf{Treatment} & \textbf{Control} & \textbf{p} \\
\midrule
Outcome 1 & \meansd{42.5}{8.3} & \meansd{35.2}{7.9} & <.001\sigthree \\
\rowcolor{tablealt} Outcome 2 & \meansd{3.8}{1.2} & \meansd{3.1}{1.1} & .012\sigone \\
Outcome 3 & \meansd{18.2}{4.5} & \meansd{17.8}{4.2} & .58\signs \\
\bottomrule
\end{tabular}

{\small \siglegend}
\end{table}
```

**Scientific Notation Commands:**

| Command | Output | Purpose |
|---------|--------|---------|
| `\pvalue{0.023}` | *p* = 0.023 | P-values |
| `\psig{< 0.001}` | ***p* = < 0.001** | Significant p-values (bold) |
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] | Confidence intervals |
| `\effectsize{d}{0.75}` | d = 0.75 | Effect sizes |
| `\samplesize{250}` | *n* = 250 | Sample sizes |
| `\meansd{42.5}{8.3}` | 42.5 ± 8.3 | Mean with SD |
| `\sigone`, `\sigtwo`, `\sigthree` | *, **, *** | Significance stars |

**Getting Started:**

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{scientific_report}

\begin{document}
\makereporttitle
    {Report Title}
    {Subtitle}
    {Author Name}
    {Institution}
    {Date}

% Your content with professional formatting
\end{document}
```

**Compilation**: Use XeLaTeX or LuaLaTeX for proper Helvetica font rendering:
```bash
xelatex report.tex
```

For complete documentation, refer to:
- `assets/scientific_report.sty`: The style package
- `assets/scientific_report_template.tex`: Complete template example
- `assets/REPORT_FORMATTING_GUIDE.md`: Quick reference guide
- `references/professional_report_formatting.md`: Comprehensive formatting guide

### 9. Journal-Specific Formatting

Adapt manuscripts to journal requirements:
- Follow author guidelines for structure, length, and format
- Apply journal-specific citation styles
- Meet figure/table specifications (resolution, file formats, dimensions)
- Include required statements (funding, conflicts of interest, data availability, ethical approval)
- Adhere to word limits for each section
- Format according to template requirements when provided

### 10. Field-Specific Language and Terminology

Adapt language, terminology, and conventions to match the specific scientific discipline. Each field has established vocabulary, preferred phrasings, and domain-specific conventions that signal expertise and ensure clarity for the target audience.

**Identify Field-Specific Linguistic Conventions:**
- Review terminology used in recent high-impact papers in the target journal
- Note field-specific abbreviations, units, and notation systems
- Identify preferred terms (e.g., "participants" vs. "subjects," "compound" vs. "drug," "specimens" vs. "samples")
- Observe how methods, organisms, or techniques are typically described

**Biomedical and Clinical Sciences:**
- Use precise anatomical and clinical terminology (e.g., "myocardial infarction" not "heart attack" in formal writing)
- Follow standardized disease nomenclature (ICD, DSM, SNOMED-CT)
- Specify drug names using generic names first, brand names in parentheses if needed
- Use "patients" for clinical studies, "participants" for community-based research
- Follow Human Genome Variation Society (HGVS) nomenclature for genetic variants
- Report lab values with standard units (SI units in most international journals)

**Molecular Biology and Genetics:**
- Use italics for gene symbols (e.g., *TP53*), regular font for proteins (e.g., p53)
- Follow species-specific gene nomenclature (uppercase for human: *BRCA1*; sentence case for mouse: *Brca1*)
- Specify organism names in full at first mention, then use accepted abbreviations (e.g., *Escherichia coli*, then *E. coli*)
- Use standard genetic notation (e.g., +/+, +/-, -/- for genotypes)
- Employ established terminology for molecular techniques (e.g., "quantitative PCR" or "qPCR," not "real-time PCR")

**Chemistry and Pharmaceutical Sciences:**
- Follow IUPAC nomenclature for chemical compounds
- Use systematic names for novel compounds, common names for well-known substances
- Specify chemical structures using standard notation (e.g., SMILES, InChI for databases)
- Report concentrations with appropriate units (mM, μM, nM, or % w/v, v/v)
- Describe synthesis routes using accepted reaction nomenclature
- Use terms like "bioavailability," "pharmacokinetics," "IC50" consistently with field definitions

**Ecology and Environmental Sciences:**
- Use binomial nomenclature for species (italicized: *Homo sapiens*)
- Specify taxonomic authorities at first species mention when relevant
- Employ standardized habitat and ecosystem classifications
- Use consistent terminology for ecological metrics (e.g., "species richness," "Shannon diversity index")
- Describe sampling methods with field-standard terms (e.g., "transect," "quadrat," "mark-recapture")

**Physics and Engineering:**
- Follow SI units consistently unless field conventions dictate otherwise
- Use standard notation for physical quantities (scalars vs. vectors, tensors)
- Employ established terminology for phenomena (e.g., "quantum entanglement," "laminar flow")
- Specify equipment with model numbers and manufacturers when relevant
- Use mathematical notation consistent with field standards (e.g., ℏ for reduced Planck constant)

**Neuroscience:**
- Use standardized brain region nomenclature (e.g., refer to atlases like Allen Brain Atlas)
- Specify coordinates for brain regions using established stereotaxic systems
- Follow conventions for neural terminology (e.g., "action potential" not "spike" in formal writing)
- Use "neural activity," "neuronal firing," "brain activation" appropriately based on measurement method
- Describe recording techniques with proper specificity (e.g., "whole-cell patch clamp," "extracellular recording")

**Social and Behavioral Sciences:**
- Use person-first language when appropriate (e.g., "people with schizophrenia" not "schizophrenics")
- Employ standardized psychological constructs and validated assessment names
- Follow APA guidelines for reducing bias in language
- Specify theoretical frameworks using established terminology
- Use "participants" rather than "subjects" for human research

**General Principles:**

**Match Audience Expertise:**
- For specialized journals: Use field-specific terminology freely, define only highly specialized or novel terms
- For broad-impact journals (e.g., *Nature*, *Science*): Define more technical terms, provide context for specialized concepts
- For interdisciplinary audiences: Balance precision with accessibility, define terms at first use

**Define Technical Terms Strategically:**
- Define abbreviations at first use: "messenger RNA (mRNA)"
- Provide brief explanations for specialized techniques when writing for broader audiences
- Avoid over-defining terms well-known to the target audience (signals unfamiliarity with field)
- Create a glossary if numerous specialized terms are unavoidable

**Maintain Consistency:**
- Use the same term for the same concept throughout (don't alternate between "medication," "drug," and "pharmaceutical")
- Follow a consistent system for abbreviations (decide on "PCR" or "polymerase chain reaction" after first definition)
- Apply the same nomenclature system throughout (especially for genes, species, chemicals)

**Avoid Field Mixing Errors:**
- Don't use clinical terminology for basic science (e.g., don't call mice "patients")
- Avoid colloquialisms or overly general terms in place of precise field terminology
- Don't import terminology from adjacent fields without ensuring proper usage

**Verify Terminology Usage:**
- Consult field-specific style guides and nomenclature resources
- Check how terms are used in recent papers from the target journal
- Use domain-specific databases and ontologies (e.g., Gene Ontology, MeSH terms)
- When uncertain, cite a key reference that establishes terminology

### 11. Common Pitfalls to Avoid

**Top Rejection Reasons:**
1. Inappropriate, incomplete, or insufficiently described statistics
2. Over-interpretation of results or unsupported conclusions
3. Poorly described methods affecting reproducibility
4. Small, biased, or inappropriate samples
5. Poor writing quality or difficult-to-follow text
6. Inadequate literature review or context
7. Figures and tables that are unclear or poorly designed
8. Failure to follow reporting guidelines

**Writing Quality Issues:**
- Mixing tenses inappropriately (use past tense for methods/results, present for established facts)
- Excessive jargon or undefined acronyms
- Paragraph breaks that disrupt logical flow
- Missing transitions between sections
- Inconsistent notation or terminology

## Workflow for Manuscript Development

**Stage 1: Planning**
1. Identify target journal and review author guidelines
2. Determine applicable reporting guideline (CONSORT, STROBE, etc.)
3. Outline manuscript structure (usually IMRAD)
4. Plan figures and tables as the backbone of the paper

**Stage 2: Drafting** (Use two-stage writing process for each section)
1. Start with figures and tables (the core data story)
2. For each section below, follow the two-stage process:
   - **First**: Create outline with bullet points using research-lookup
   - **Second**: Convert bullet points to full paragraphs with flowing prose
3. Write Methods (often easiest to draft first)
4. Draft Results (describing figures/tables objectively)
5. Compose Discussion (interpreting findings)
6. Write Introduction (setting up the research question)
7. Craft Abstract (synthesizing the complete story)
8. Create Title (concise and descriptive)

**Remember**: Bullet points are for planning only—the final manuscript must be in complete paragraphs.

**Stage 3: Revision**
1. Check logical flow and "red thread" throughout
2. Verify consistency in terminology and notation
3. Ensure figures/tables are self-explanatory
4. Confirm adherence to reporting guidelines
5. Verify all citations are accurate and properly formatted
6. Check word counts for each section
7. Proofread for grammar, spelling, and clarity

**Stage 4: Final Preparation**
1. Format according to journal requirements
2. Prepare supplementary materials
3. Write cover letter highlighting significance
4. Complete submission checklists
5. Gather all required statements and forms

## Integration with Other Scientific Skills

This skill works effectively with:
- **Data analysis skills**: For generating results to report
- **Statistical analysis**: For determining appropriate statistical presentations
- **Literature review skills**: For contextualizing research
- **Figure creation tools**: For developing publication-quality visualizations
- **Venue-templates skill**: For venue-specific writing styles and formatting (journal manuscripts)
- **scientific_report.sty**: For professional reports, white papers, and technical documents

### Professional Reports vs. Journal Manuscripts

**Choose the right formatting approach:**

| Document Type | Formatting Approach |
|---------------|---------------------|
| Journal manuscripts | Use `venue-templates` skill |
| Conference papers | Use `venue-templates` skill |
| Research reports | Use `scientific_report.sty` (this skill) |
| White papers | Use `scientific_report.sty` (this skill) |
| Technical reports | Use `scientific_report.sty` (this skill) |
| Grant reports | Use `scientific_report.sty` (this skill) |

### Venue-Specific Writing Styles

**Before writing for a specific venue, consult the venue-templates skill for writing style guides:**

Different venues have dramatically different writing expectations:
- **Nature/Science**: Accessible, story-driven, broad significance
- **Cell Press**: Mechanistic depth, graphical abstracts, Highlights
- **Medical journals (NEJM, Lancet)**: Structured abstracts, evidence language
- **ML conferences (NeurIPS, ICML)**: Contribution bullets, ablation studies
- **CS conferences (CHI, ACL)**: Field-specific conventions

The venue-templates skill provides:
- `venue_writing_styles.md`: Master style comparison
- Venue-specific guides: `nature_science_style.md`, `cell_press_style.md`, `medical_journal_styles.md`, `ml_conference_style.md`, `cs_conference_style.md`
- `reviewer_expectations.md`: What reviewers look for at each venue
- Writing examples in `assets/examples/`

**Workflow**: First use this skill for general scientific writing principles (IMRAD, clarity, citations), then consult venue-templates for venue-specific style adaptation.

## References

This skill includes comprehensive reference files covering specific aspects of scientific writing:

- `references/imrad_structure.md`: Detailed guide to IMRAD format and section-specific content
- `references/citation_styles.md`: Complete citation style guides (APA, AMA, Vancouver, Chicago, IEEE)
- `references/figures_tables.md`: Best practices for creating effective data visualizations
- `references/reporting_guidelines.md`: Study-specific reporting standards and checklists
- `references/writing_principles.md`: Core principles of effective scientific communication
- `references/professional_report_formatting.md`: Guide to professional report styling with `scientific_report.sty`

## Assets

This skill includes LaTeX style packages and templates for professional report formatting:

- `assets/scientific_report.sty`: Professional LaTeX style package with Helvetica fonts, colored boxes, and attractive tables
- `assets/scientific_report_template.tex`: Complete report template demonstrating all style features
- `assets/REPORT_FORMATTING_GUIDE.md`: Quick reference guide for the style package

**Key Features of `scientific_report.sty`:**
- Helvetica font family for modern, professional appearance
- Professional color scheme (blues, greens, oranges, purples)
- Box environments: `keyfindings`, `methodology`, `resultsbox`, `recommendations`, `limitations`, `criticalnotice`, `definition`, `executivesummary`, `hypothesis`
- Tables with alternating row colors and professional headers
- Scientific notation commands for p-values, effect sizes, confidence intervals
- Professional headers and footers

**For venue-specific writing styles** (tone, voice, abstract format, reviewer expectations), see the **venue-templates** skill which provides comprehensive style guides for Nature/Science, Cell Press, medical journals, ML conferences, and CS conferences.

Load these references as needed when working on specific aspects of scientific writing.

---

## Reference: Citation_Styles

# Citation Styles Guide

## Overview

Citation styles provide standardized formats for acknowledging sources in scientific writing. Different disciplines prefer different styles, and journals typically specify which style to use. The five most common citation styles in science are AMA, Vancouver, APA, Chicago, and IEEE.

## Choosing the Right Style

| Style | Primary Disciplines | In-Text Format |
|-------|-------------------|----------------|
| AMA | Medicine, health sciences | Superscript numbers¹ |
| Vancouver | Biomedical sciences | Numbers in brackets [1] |
| APA | Psychology, social sciences, education | Author-date (Smith, 2023) |
| Chicago | Humanities, history, some sciences | Notes-bibliography or author-date |
| IEEE | Engineering, computer science | Numbers in brackets [1] |
| ACS | Chemistry | Superscript numbers¹ or (1) |
| NLM | Life sciences, PubMed | Numbers in brackets [1] |

**Default recommendation**: When in doubt, check the journal's author guidelines. Most biomedical journals use Vancouver or AMA style.

## AMA Style (American Medical Association)

### Overview
- Used primarily in medical research
- Based on the *AMA Manual of Style* (11th edition, 2020)
- Numbered citations appearing as superscripts
- References listed numerically in order of appearance

### In-Text Citations

**Basic format**: Superscript numerals outside periods and commas, inside semicolons and colons.

**Examples:**
```
Several studies have demonstrated this effect.¹

The results were inconclusive,² although Smith et al³ reported otherwise.

These findings³⁻⁵ suggest a correlation.

One meta-analysis⁶ found significant heterogeneity; however, the pooled effect was significant.⁷
```

**Multiple citations**: Use commas or hyphens for ranges
```
Multiple studies¹,³,⁵⁻⁷ have confirmed this.
```

**Same source cited multiple times**: Use the same number throughout

### Reference List Format

**Journal Articles:**
```
1. Author AA, Author BB, Author CC. Title of article. Journal Name. Year;Volume(Issue):Page range. doi:xx.xxxx
```

**Example:**
```
1. Smith JD, Johnson AB, Williams CD. Effectiveness of cognitive behavioral therapy for anxiety disorders. JAMA Psychiatry. 2023;80(5):456-464. doi:10.1001/jamapsychiatry.2023.0123
```

**Books:**
```
2. Author AA. Book Title. Edition. Publisher; Year.
```

**Book Chapters:**
```
3. Chapter Author AA. Chapter title. In: Editor AA, Editor BB, eds. Book Title. Edition. Publisher; Year:Page range.
```

**Online Resources:**
```
4. Organization Name. Page title. Website name. Published date. Updated date. Accessed date. URL
```

### Special Cases

**More than 6 authors**: List first 3, then "et al"
```
Smith JD, Jones AB, Williams CD, et al.
```

**No author**: Begin with title

**Advance online publication**:
```
Published online Month Day, Year. doi:xx.xxxx
```

## Vancouver Style

### Overview
- Developed by the International Committee of Medical Journal Editors (ICMJE)
- Described in *Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals*
- Also called "author-number style"
- Numbered citations in square brackets
- References listed numerically

### In-Text Citations

**Basic format**: Numbers in square brackets after the relevant text, before periods and commas.

**Examples:**
```
Several studies have shown this effect [1].

The results were inconclusive [2], although Smith et al [3] reported otherwise.

These findings [3-5] suggest a correlation.

Multiple studies [1,3,5-7] have confirmed this.
```

### Reference List Format

**Journal Articles:**
```
1. Author AA, Author BB, Author CC. Title of article. Journal Name. Year;Volume(Issue):Page range.
```

**Example:**
```
1. Smith JD, Johnson AB, Williams CD. Effectiveness of cognitive behavioral therapy for anxiety disorders. JAMA Psychiatry. 2023;80(5):456-464.
```

**Books:**
```
2. Author AA, Author BB. Book title. Edition. Place of publication: Publisher; Year.
```

**Book Chapters:**
```
3. Chapter Author AA, Chapter Author BB. Chapter title. In: Editor AA, Editor BB, editors. Book title. Edition. Place: Publisher; Year. p. Page range.
```

**Electronic Sources:**
```
4. Author AA. Title of page [Internet]. Place: Publisher; Date of publication [cited Date of citation]. Available from: URL
```

### Special Cases

**More than 6 authors**: List first 6, then "et al."

**Journal title abbreviations**: Use PubMed/Index Medicus abbreviations
- *The Journal of the American Medical Association* → *JAMA*
- *Nature Medicine* → *Nat Med*

**No volume or issue**: Use year and page numbers only

**Article in press**: Use "[Epub ahead of print]" notation

## APA Style (American Psychological Association)

### Overview
- Widely used in psychology, education, and social sciences
- Based on the *Publication Manual of the APA* (7th edition, 2020)
- Author-date format for in-text citations
- References listed alphabetically by author surname

### In-Text Citations

**Basic format**: (Author, Year)

**Examples:**
```
One study found significant effects (Smith, 2023).

Smith (2023) found significant effects.

Multiple studies (Jones, 2020; Smith, 2023; Williams, 2024) support this conclusion.
```

**Two authors**: Use "&" in parentheses, "and" in narrative
```
(Smith & Jones, 2023)
Smith and Jones (2023) demonstrated...
```

**Three or more authors**: Use "et al." after first author
```
(Smith et al., 2023)
Smith et al. (2023) reported...
```

**Multiple works by same author(s) in same year**: Add letters
```
(Smith, 2023a, 2023b)
```

**Direct quotations**: Include page numbers
```
(Smith, 2023, p. 45)
"Quote text" (Smith, 2023, p. 45).
Smith (2023) stated, "Quote text" (p. 45).
```

### Reference List Format

**Journal Articles:**
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Journal Name, Volume(Issue), page range. https://doi.org/xx.xxxx
```

**Example:**
```
Smith, J. D., Johnson, A. B., & Williams, C. D. (2023). Effectiveness of cognitive behavioral therapy for anxiety disorders. JAMA Psychiatry, 80(5), 456-464. https://doi.org/10.1001/jamapsychiatry.2023.0123
```

**Books:**
```
Author, A. A. (Year). Book title: Subtitle (Edition). Publisher. https://doi.org/xx.xxxx
```

**Book Chapters:**
```
Chapter Author, A. A., & Chapter Author, B. B. (Year). Chapter title. In E. E. Editor & F. F. Editor (Eds.), Book title (pp. page range). Publisher.
```

**Websites:**
```
Author, A. A. (Year, Month Day). Page title. Website Name. URL
```

### Capitalization Rules
- Sentence case for article and book titles (capitalize only first word and proper nouns)
- Title case for journal names (capitalize all major words)

**Example:**
```
Smith, J. D. (2023). Effects of stress on cognitive performance: A meta-analysis. Journal of Experimental Psychology: General, 152(3), 456-478.
```

### Special Cases

**No author**: Move title to author position
```
Title of work. (Year). Journal Name...
```

**No date**: Use (n.d.)
```
Smith, J. D. (n.d.). Title...
```

**Up to 20 authors**: List all authors with "&" before last
**21 or more authors**: List first 19, then "...", then final author

## Chicago Style

### Overview
- Based on *The Chicago Manual of Style* (17th edition, 2017)
- Two systems: Notes-Bibliography and Author-Date
- Notes-Bibliography common in humanities
- Author-Date common in sciences

### Notes-Bibliography System

**In-Text**: Superscript numbers for footnotes or endnotes
```
One study demonstrated this effect.¹
```

**Note format:**
```
1. John D. Smith, Alice B. Johnson, and Carol D. Williams, "Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders," JAMA Psychiatry 80, no. 5 (2023): 456-64.
```

**Bibliography format:**
```
Smith, John D., Alice B. Johnson, and Carol D. Williams. "Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders." JAMA Psychiatry 80, no. 5 (2023): 456-64.
```

### Author-Date System

**In-Text**: Similar to APA
```
(Smith, Johnson, and Williams 2023)
Smith, Johnson, and Williams (2023) found...
```

**Reference list**: Similar to APA but with different punctuation
```
Smith, John D., Alice B. Johnson, and Carol D. Williams. 2023. "Effectiveness of Cognitive Behavioral Therapy for Anxiety Disorders." JAMA Psychiatry 80 (5): 456-64.
```

### Special Features
- Full names in bibliography (not just initials)
- Uses "and" not "&"
- Different punctuation from APA

## IEEE Style

### Overview
- Used in engineering, computer science, and technology
- Published by the Institute of Electrical and Electronics Engineers
- Numbered citations in square brackets
- References listed numerically

### In-Text Citations

**Format**: Numbers in square brackets

**Examples:**
```
Several studies have demonstrated this effect [1].

The algorithm was described by Smith [2] and later improved [3], [4].

Multiple implementations [1]-[4] have been proposed.
```

### Reference List Format

**Journal Articles:**
```
[1] A. A. Author, B. B. Author, and C. C. Author, "Title of article," Journal Name, vol. X, no. X, pp. XX-XX, Month Year.
```

**Example:**
```
[1] J. D. Smith, A. B. Johnson, and C. D. Williams, "Effectiveness of cognitive behavioral therapy for anxiety disorders," JAMA Psychiatry, vol. 80, no. 5, pp. 456-464, May 2023.
```

**Books:**
```
[2] A. A. Author, Book Title, Edition. City, State: Publisher, Year.
```

**Conference Papers:**
```
[3] A. A. Author, "Paper title," in Proc. Conference Name, City, State, Year, pp. XX-XX.
```

**Online Sources:**
```
[4] A. A. Author. "Title." Website. URL (accessed Mon. Day, Year).
```

### Special Features
- Abbreviated first and middle names
- Uses "and" before last author (not comma)
- Month abbreviations (Jan., Feb., etc.)
- "vol." and "no." before volume and issue
- "pp." before page range

## Additional Styles

### ACS Style (American Chemical Society)

**In-Text**: Superscript numbers or numbers in parentheses
```
This reaction has been well studied.¹
This reaction has been well studied (1).
```

**Reference format:**
```
(1) Smith, J. D.; Johnson, A. B.; Williams, C. D. Title of Article. J. Am. Chem. Soc. 2023, 145, 1234-1245.
```

**Features:**
- Semicolons between authors
- Abbreviated journal names
- Year in bold
- No issue numbers

### NLM Style (National Library of Medicine)

**Very similar to Vancouver**, used by PubMed/MEDLINE

**Key differences:**
- Uses PubMed journal abbreviations
- Specific format for electronic publications
- PMID or PMCID can be included

**Example:**
```
Smith JD, Johnson AB, Williams CD. Effectiveness of cognitive behavioral therapy for anxiety disorders. JAMA Psychiatry. 2023 May;80(5):456-64. doi: 10.1001/jamapsychiatry.2023.0123. PMID: 12345678.
```

## General Citation Best Practices

### Across All Styles

**When to cite:**
- Direct quotations
- Paraphrased ideas from others
- Statistics, data, or figures from other sources
- Theories, models, or frameworks developed by others
- Information that is not common knowledge

**Citation density:**
- Introduction: Cite liberally to establish context
- Methods: Cite when referencing established protocols or instruments
- Results: Rarely cite (focus on your own findings)
- Discussion: Cite frequently when comparing to prior work

**Source quality:**
- Prefer peer-reviewed journal articles
- Cite original sources when possible (not secondary citations)
- Use recent sources (within 5-10 years for active fields)
- Ensure sources are reputable and relevant

**Common mistakes to avoid:**
- Inconsistent formatting
- Missing required elements (DOI, page numbers, etc.)
- Citing sources not actually read (citation chaining)
- Over-reliance on review articles instead of primary sources
- Including uncited references or missing cited references
- Incorrect author names or initials
- Wrong year of publication
- Truncated titles

### Managing Citations

**Reference Management Software:**
- **Zotero**: Free, open-source, browser integration
- **Mendeley**: Free, PDF annotation, social features
- **EndNote**: Commercial, powerful, institutional support
- **RefWorks**: Web-based, institutional subscriptions

**Software benefits:**
- Automatic formatting in multiple styles
- In-text citation insertion
- Reference list generation
- PDF organization
- Sharing capabilities

### Verifying Citations

**Before submission, check:**
1. Every in-text citation has a corresponding reference
2. Every reference is cited in text
3. Formatting is consistent throughout
4. Author names and initials are correct
5. Titles are accurate
6. Journal names match required abbreviations
7. Volume, issue, and page numbers are correct
8. DOIs are included (when required)
9. URLs are functional (for web sources)
10. Citations appear in correct order (numerical styles)

## DOI (Digital Object Identifier)

### What is a DOI?
A unique alphanumeric string identifying digital content permanently.

**Format:**
```
doi:10.1001/jamapsychiatry.2023.0123
or
https://doi.org/10.1001/jamapsychiatry.2023.0123
```

### When to include:
- Required by most journals for recent publications
- Preferred over URLs because DOIs don't change
- Look up DOIs at https://www.crossref.org/ if not provided

### Style-specific formatting:
- **AMA**: `doi:10.xxxx/xxxxx`
- **APA**: `https://doi.org/10.xxxx/xxxxx`
- **Vancouver**: Often omitted or added at journal's discretion
- **Chicago**: `https://doi.org/10.xxxx/xxxxx`

## Quick Reference: Journal Article Format

| Style | Format |
|-------|--------|
| **AMA** | Author AA, Author BB. Title of article. *Journal*. Year;Vol(Iss):pp. doi:xx |
| **Vancouver** | Author AA, Author BB. Title of article. Journal. Year;Vol(Iss):pp. |
| **APA** | Author, A. A., & Author, B. B. (Year). Title of article. *Journal*, Vol(Iss), pp. https://doi.org/xx |
| **Chicago A-D** | Author, A. A., and B. B. Author. Year. "Title." *Journal* Vol (Iss): pp. |
| **IEEE** | A. A. Author and B. B. Author, "Title," *Journal*, vol. X, no. X, pp. XX-XX, Mon. Year. |

## Common Abbreviations

### Journal Abbreviations
Follow the journal's specified system (usually Index Medicus or ISO):
- *The Journal of Biological Chemistry* → *J Biol Chem*
- *Proceedings of the National Academy of Sciences* → *Proc Natl Acad Sci USA*
- *Nature Medicine* → *Nat Med*

### Month Abbreviations
- Jan., Feb., Mar., Apr., May, June, July, Aug., Sept., Oct., Nov., Dec.
- Some styles use three-letter abbreviations without periods

### Edition Abbreviations
- 1st ed., 2nd ed., 3rd ed., etc.
- Or: 1st edition, 2nd edition

## Special Publication Types

### Preprints
```
APA: Author, A. A. (Year). Title [Preprint]. Repository Name. https://doi.org/xx.xxxx
```

### Theses and Dissertations
```
APA: Author, A. A. (Year). Title [Doctoral dissertation, University Name]. Repository Name. URL
```

### Conference Proceedings
```
IEEE: A. A. Author, "Title," in Proc. Conf. Name, City, Year, pp. XX-XX.
```

### Software/Code
```
APA: Author, A. A. (Year). Title (Version X.X) [Computer software]. Publisher. URL
```

### Datasets
```
APA: Author, A. A. (Year). Title of dataset (Version X) [Data set]. Repository. https://doi.org/xx.xxxx
```

## Transitioning Between Styles

When converting between citation styles:

1. **Use reference management software** for automatic conversion
2. **Check these elements** that vary by style:
   - In-text citation format (numbered vs. author-date)
   - Author name format (initials vs. full names)
   - Title capitalization (sentence case vs. title case)
   - Journal name formatting (abbreviated vs. full)
   - Punctuation (periods, commas, semicolons)
   - Use of italics and bold
   - Order of elements
3. **Manually verify** after automatic conversion
4. **Check journal guidelines** for specific requirements

## Journal-Specific Citation Styles and Requirements

### How to Identify a Journal's Citation Style

**Step 1: Check Author Guidelines**
- Every journal provides author instructions (usually "Instructions for Authors" or "Author Guidelines")
- Citation style is typically specified in "References" or "Citations" section
- Look for example references formatted in the journal's style

**Step 2: Review Recent Publications**
- Examine 3-5 recent articles from your target journal
- Note the in-text citation format (numbered vs. author-date)
- Compare reference list formatting
- Check for journal-specific variations

**Step 3: Verify Journal-Specific Variations**
Some journals use modified versions of standard styles:
- Abbreviated vs. full journal names
- DOI inclusion requirements
- Article titles in title case vs. sentence case
- Maximum number of authors before "et al."

### Common Journals and Their Citation Styles

| Journal | Citation Style | Key Features |
|---------|---------------|--------------|
| **JAMA, JAMA Network journals** | AMA | Superscript numbers, abbreviated journal names, no issue numbers |
| **New England Journal of Medicine** | Modified Vancouver | Numbered brackets, abbreviated journals, limited authors (3 then et al) |
| **The Lancet** | Vancouver | Numbered brackets, PubMed abbreviations |
| **BMJ** | Vancouver | Numbered in-text, DOIs required when available |
| **Nature, Nature journals** | Nature style (numbered) | Numbered superscripts, abbreviated journals, no article titles in some journals |
| **Science** | Science style (numbered) | Numbered in-text, abbreviated format |
| **Cell, Cell Press journals** | Cell style (author-year) | Author-date, specific formatting for multiple citations |
| **PLOS journals** | Vancouver | Numbered brackets, full journal names in some PLOS journals |
| **Journal of Biological Chemistry** | JBC style (numbered) | Numbered in-text, specific abbreviation rules |
| **Psychological journals** | APA | Author-date, DOIs required |
| **IEEE journals** | IEEE | Numbered brackets, specific format for conference papers |
| **ACS journals** | ACS | Superscript or numbered, semicolons between authors |

### Journal Family Consistency

**Journals from the same publisher often share citation styles:**

**Elsevier journals:**
- Vary widely; check specific journal
- Many use numbered Vancouver-style
- Some allow author-date

**Springer Nature journals:**
- Nature journals: Nature style (numbered, abbreviated)
- Springer journals: Often numbered or author-date depending on field
- BMC journals: Vancouver with full journal names

**Wiley journals:**
- Varies by field
- Many biomedical journals use Vancouver
- Psychology/social science journals often use APA

**American Chemical Society (ACS):**
- All ACS journals use ACS style
- Consistent across Journal of American Chemical Society, Analytical Chemistry, etc.

### High-Impact Journal and Conference Preferences

| Venue | Field | Citation Preference | Key Features |
|-------|-------|-------------------|--------------|
| **Nature/Science** | Multidisciplinary | Numbered, abbreviated | Space-saving, broad readability |
| **Cell family** | Life sciences | Author-date or numbered | Attribution visibility |
| **NEJM/Lancet/JAMA** | Medicine | Vancouver/AMA numbered | Medical standard |
| **NeurIPS/ICML/ICLR** | Machine Learning | Numbered [1] or (Author, Year) | Varies by conference, check template |
| **CVPR/ICCV/ECCV** | Computer Vision | Numbered [1], IEEE-like | Compact format |
| **ACL/EMNLP** | NLP | Author-year (ACL style) | Attribution-focused |

### Adapting Citations for Different Target Journals

**When switching journals after desk rejection or withdrawal:**

**Use reference management software:**
1. Import references into Zotero, Mendeley, or EndNote
2. Select target journal's citation style from software library
3. Regenerate citations and reference list automatically
4. Manually verify formatting matches journal examples

**Key elements to check when converting:**
- In-text format (switch numbered ↔ author-date)
- Journal name abbreviation style
- Article title capitalization
- Author name format (initials vs. full names)
- DOI format and inclusion
- Issue number inclusion/exclusion
- Page number format

**Manual verification essential for:**
- Preprints and non-standard sources
- Software/datasets citations
- Conference proceedings
- Dissertations and theses

### Venue-Specific Evaluation Criteria

**Content expectations:**
- **High-impact journals**: >50% citations from last 5 years; primary sources preferred
- **Medical journals**: Recent clinical evidence; systematic reviews valued
- **ML conferences**: Recent papers (last 2-3 years); preprints (arXiv) acceptable
- **Self-citation**: Keep <20% across all venues

**Format compliance (often automated):**
- Match venue citation style exactly
- All in-text citations have corresponding references
- Include DOIs when required (journals) or arXiv IDs (ML conferences)
- Use correct abbreviations (PubMed for medical, standard for ML)

**ML conference specifics:**
- **NeurIPS/ICML/ICLR**: ArXiv preprints widely cited; recent work heavily valued
- **Page limits strict**: Citation formatting affects space
- **Supplementary material**: Can include extended bibliography
- **Double-blind review**: Avoid obvious self-citation patterns during review

### Citation Density by Venue Type

| Venue Type | Expected Citations | Key Notes |
|-----------|-------------------|-----------|
| **Nature/Science research** | 30-50 | Selective, high-impact citations |
| **Medical journals (RCT)** | 25-40 | Recent clinical evidence |
| **Field-specific journals** | 30-60 | Comprehensive field coverage |
| **ML conferences (8-page)** | 20-40 | Space-limited, recent work |
| **Review articles** | 100-300+ | Comprehensive coverage |

**ML conference citation practices:**
- **NeurIPS/ICML**: 25-40 references typical for 8-page papers
- **Workshop papers**: 15-25 references
- **ArXiv preprints**: Widely accepted and cited
- **Related work**: Concise but comprehensive; often moved to appendix
- **Recency critical**: Cite work from last 1-2 years when relevant

### Pre-Submission Citation Checklist

**Content:**
- [ ] ≥50% citations from last 5-10 years (or 2-3 years for ML conferences)
- [ ] <20% self-citations; balanced perspectives
- [ ] Primary sources cited (not citation chains)
- [ ] All claims supported by appropriate citations

**Format:**
- [ ] Style matches venue exactly (check template)
- [ ] All in-text citations in reference list and vice versa
- [ ] DOIs/arXiv IDs included as required
- [ ] Abbreviations match venue style

**ML conferences additional:**
- [ ] ArXiv preprints properly formatted
- [ ] Self-citations anonymized if double-blind review
- [ ] References fit within page limits

## Resources for Citation Styles

### Official Manuals
- AMA: https://www.amamanualofstyle.com/
- Vancouver/ICMJE: http://www.icmje.org/
- APA: https://apastyle.apa.org/
- Chicago: https://www.chicagomanualofstyle.org/
- IEEE: https://ieeeauthorcenter.ieee.org/

### Journal-Specific Style Guides
- Nature: https://www.nature.com/nature/for-authors/formatting-guide
- Science: https://www.science.org/content/page/instructions-authors
- Cell: https://www.cell.com/cell/authors
- JAMA: https://jamanetwork.com/journals/jama/pages/instructions-for-authors

### Quick Reference Guides
- Purdue OWL: https://owl.purdue.edu/
- Citation Machine: https://www.citationmachine.net/
- EasyBib: https://www.easybib.com/

### Reference Management
- Zotero: https://www.zotero.org/
- Mendeley: https://www.mendeley.com/
- EndNote: https://endnote.com/

### Journal Citation Style Databases
- Journal Citation Reports (Clarivate): Lists journal citation styles
- EndNote style repository: >7000 journal-specific styles
- Zotero Style Repository: https://www.zotero.org/styles

---

## Reference: Figures_Tables

# Figures and Tables Best Practices

## Overview

Figures and tables are essential components of scientific papers, serving to display data patterns, summarize results, and provide evidence for conclusions. Effective visual displays enhance comprehension and can sustain reader interest while illustrating trends, patterns, and relationships not easily conveyed through text alone.

A recent Nature Cell Biology checklist (2025) emphasizes that creating clear and engaging scientific figures is crucial for communicating complex data with clarity, accessibility, and design excellence.

## When to Use Tables vs. Figures

### Use Tables When:
- Presenting precise numerical values that readers need to reference
- Comparing exact measurements across multiple variables
- Showing detailed statistical outputs
- Data cannot be adequately summarized in 1-2 sentences
- Readers need access to specific data points
- Displaying demographic or baseline characteristics
- Presenting multiple related statistical tests

**Example use cases:**
- Baseline participant characteristics (age, sex, diagnosis, etc.)
- Detailed statistical model outputs (coefficients, p-values, confidence intervals)
- Dose-response data with exact values
- Gene expression levels for specific genes
- Chemical compositions or concentrations

### Use Figures When:
- Showing trends over time
- Displaying relationships or correlations
- Comparing groups visually
- Illustrating distributions
- Demonstrating patterns not easily seen in numbers
- Showing images (microscopy, radiography, etc.)
- Displaying workflows, diagrams, or schematics

**Example use cases:**
- Growth curves or time series
- Dose-response curves
- Scatter plots showing correlations
- Bar graphs comparing treatment groups
- Histograms showing distributions
- Heatmaps displaying patterns across conditions
- Microscopy images or Western blots

### General Decision Rule

**Can the information be conveyed in 1-2 sentences of text?**
- Yes → Use text only
- No, and precise values are needed → Use a table
- No, and patterns/trends are most important → Use a figure

## Core Design Principles

### 1. Self-Explanatory Display Items

**Each figure or table must stand alone without requiring the main text.**

**Essential elements:**
- Complete, descriptive caption
- All abbreviations defined (in caption or footnote)
- Units of measurement clearly indicated
- Sample sizes (n) reported
- Statistical significance annotations explained
- Legend included (for figures with multiple data series)

**Example of self-explanatory caption:**
```
Figure 1. Mean systolic blood pressure (SBP) over 12 weeks in intervention and control groups.
Error bars represent standard error of the mean (SEM). Asterisks indicate significant
differences between groups at each time point (*p < 0.05, **p < 0.01, ***p < 0.001,
two-tailed t-tests). n = 48 per group. BP = blood pressure; SEM = standard error of mean.
```

### 2. Avoid Redundancy

**Do not duplicate information between text, tables, and figures.**

**Bad practice:**
```
"Mean age was 45.2 years in Group A and 47.8 years in Group B. Mean BMI was 26.3 in
Group A and 28.1 in Group B. Mean systolic blood pressure was 132 mmHg in Group A..."
[Also shown in Table 1]
```

**Good practice:**
```
"Baseline characteristics were similar between groups (Table 1), with no significant
differences in age, BMI, or blood pressure (all p > 0.15)."
[Details in Table 1]
```

**Key principle:** Text should highlight key findings from tables/figures, not repeat all data.

### 3. Consistency

**Maintain uniform formatting across all display items:**
- Font types and sizes
- Color schemes
- Terminology and abbreviations
- Axis labels and units
- Statistical annotation methods
- Figure styles (all line graphs should look similar)

**Example of inconsistency to avoid:**
- Figure 1 uses "standard error" while Figure 2 uses "SE"
- Figure 1 has blue/red color scheme while Figure 2 uses green/yellow
- Table 1 reports p-values as "p = 0.023" while Table 2 uses "p-value = .023"

### 4. Optimal Quantity

**Follow the "one display item per 1000 words" guideline.**

**Typical manuscript:**
- 3000-4000 words → 3-4 tables/figures total
- 5000-6000 words → 5-6 tables/figures total

**Quality over quantity:** A few well-designed, information-rich displays are better than many redundant or poorly designed ones.

### 5. Clarity and Simplicity

**Avoid cluttered or overly complex displays:**
- Don't include too many variables in one figure
- Use clear, readable fonts (minimum 8-10 pt in final size)
- Provide adequate spacing between elements
- Use high contrast (especially for color-blind accessibility)
- Remove unnecessary grid lines, borders, or decoration
- Maximize data-ink ratio (Tufte principle: minimize non-data ink)

## Figure Types and When to Use Them

### Bar Graphs

**Best for:**
- Comparing discrete categories or groups
- Showing counts or frequencies
- Displaying mean values with error bars

**Design guidelines:**
- Start y-axis at zero (unless showing small differences in large values)
- Order bars logically (by size, alphabetically, or temporally)
- Use error bars (SD, SEM, or CI) consistently
- Include sample sizes
- Avoid 3D effects (they distort perception)

**Common mistakes:**
- Not starting at zero (can exaggerate differences)
- Too many categories (consider table instead)
- Missing error bars

**Example applications:**
- Mean gene expression across tissue types
- Treatment group comparisons
- Frequency of adverse events

### Line Graphs

**Best for:**
- Showing trends over continuous variables (usually time)
- Displaying multiple groups on same axes
- Illustrating dose-response relationships

**Design guidelines:**
- Use different line styles or colors for groups
- Include data point markers for sparse data
- Show error bars or shaded confidence intervals
- Label axes clearly with units
- Use consistent intervals on x-axis

**Common mistakes:**
- Connecting discrete data points that shouldn't be connected
- Too many lines making graph unreadable
- Inconsistent time intervals without indication

**Example applications:**
- Growth curves
- Time course experiments
- Survival curves (Kaplan-Meier plots)
- Pharmacokinetic profiles

### Scatter Plots

**Best for:**
- Showing relationships between two continuous variables
- Displaying correlations
- Identifying outliers

**Design guidelines:**
- Include trend line or regression line with equation and R²
- Report correlation coefficient and p-value
- Use semi-transparent points if data overlap
- Consider logarithmic scales for wide ranges
- Mark outliers if relevant

**Common mistakes:**
- Not showing individual data points
- Using scatter plots for categorical data
- Missing correlation statistics

**Example applications:**
- Correlation between biomarkers
- Relationship between dose and response
- Method comparison (Bland-Altman plots)

### Box Plots (Box-and-Whisker Plots)

**Best for:**
- Showing distributions and spread
- Comparing distributions across groups
- Identifying outliers

**Design guidelines:**
- Clearly define box elements (median, quartiles, whiskers)
- Show or note outliers explicitly
- Consider violin plots for small sample sizes
- Overlay individual data points when n < 20

**Common mistakes:**
- Not defining what whiskers represent
- Using for very small samples without showing raw data
- Not marking outliers

**Example applications:**
- Comparing distributions across treatment groups
- Showing variability in measurements
- Quality control data

### Heatmaps

**Best for:**
- Displaying matrices of data
- Showing patterns across many conditions
- Representing clustering or grouping

**Design guidelines:**
- Use color scales that are perceptually uniform
- Include color scale bar with units
- Consider hierarchical clustering for rows/columns
- Use appropriate color scheme (diverging vs. sequential)
- Make axes labels readable

**Common mistakes:**
- Poor color choice (rainbow scales are often misleading)
- Too many rows/columns making labels unreadable
- No color scale bar

**Example applications:**
- Gene expression across samples
- Correlation matrices
- Time-series data across multiple variables

### Images (Microscopy, Gels, Blots)

**Best for:**
- Showing representative examples
- Demonstrating morphology or localization
- Presenting gel electrophoresis or Western blots

**Design guidelines:**
- Include scale bars (not magnification in caption)
- Show representative images with quantification in separate panel
- Label important features with arrows or labels
- Ensure adequate resolution (usually 300+ dpi)
- Show full, unmanipulated images with cropping noted
- Include all relevant controls

**Common mistakes:**
- No scale bar
- Over-processed or manipulated images
- Cherry-picking best images without quantification
- Insufficient resolution

**Example applications:**
- Histological sections
- Immunofluorescence
- Western blots
- Gel electrophoresis

### Forest Plots

**Best for:**
- Displaying meta-analysis results
- Showing effect sizes with confidence intervals
- Comparing multiple studies or subgroups

**Design guidelines:**
- Include point estimates and CI for each study
- Show overall pooled estimate clearly
- Include line of no effect (typically at 1.0 or 0)
- List study details or weights

**Example applications:**
- Meta-analyses
- Systematic reviews
- Subgroup analyses

### Flow Diagrams

**Best for:**
- Study participant flow (CONSORT diagrams)
- Systematic review search process (PRISMA diagrams)
- Experimental workflows

**Design guidelines:**
- Follow reporting guideline templates (CONSORT, PRISMA)
- Use consistent shapes and connectors
- Include numbers at each stage
- Clearly show inclusions and exclusions

## Table Design Guidelines

### Structure

**Basic anatomy:**
1. **Table number and title** (above table)
2. **Column headers** (with units)
3. **Row labels**
4. **Data cells** (with appropriate precision)
5. **Footnotes** (below table for abbreviations, statistics, notes)

### Formatting Best Practices

**Column headers:**
- Use clear, concise labels
- Include units in parentheses
- Use abbreviations sparingly (define in footnote)

**Data presentation:**
- Align decimal points in columns
- Use consistent decimal places (usually 1-2 for means)
- Report same precision across rows/columns
- Use en-dash (–) for "not applicable"
- Use appropriate precision (don't over-report)

**Statistical annotations:**
- Use superscript letters (ᵃ, ᵇ, ᶜ) or symbols (*, †, ‡) for footnotes
- Define p-value thresholds clearly
- Report exact p-values when possible (p = 0.032, not p < 0.05)

**Footnotes:**
- Define all abbreviations
- Explain statistical tests used
- Note any missing data
- Indicate data source if not original

### Example Table Format

```
Table 1. Baseline Characteristics of Study Participants

Characteristic          Intervention (n=50)   Control (n=48)    p-value
─────────────────────────────────────────────────────────────────────────
Age, years               45.3 ± 8.2           47.1 ± 9.1        0.28
Male sex, n (%)          28 (56)              25 (52)           0.71
BMI, kg/m²               26.3 ± 3.8           27.1 ± 4.2        0.32
Current smoker, n (%)    12 (24)              15 (31)           0.42
Systolic BP, mmHg        132 ± 15             134 ± 18          0.54
─────────────────────────────────────────────────────────────────────────

Data presented as mean ± SD or n (%). p-values from independent t-tests for
continuous variables and χ² tests for categorical variables. BMI = body mass
index; BP = blood pressure; SD = standard deviation.
```

### Common Table Mistakes

1. **Excessive complexity** (too many rows/columns)
2. **Insufficient context** (missing units, unclear abbreviations)
3. **Over-precision** (reporting 5 decimal places for p-values)
4. **Missing sample sizes**
5. **No statistical comparisons when appropriate**
6. **Inconsistent formatting** across multiple tables
7. **Duplicate information** with figures or text

## Statistical Presentation in Figures and Tables

### Reporting Requirements

**For each comparison, report:**
1. **Point estimate** (mean, median, proportion)
2. **Measure of variability** (SD, SEM, CI)
3. **Sample size** (n)
4. **Test statistic** (t, F, χ², etc.)
5. **p-value** (exact when p > 0.001)
6. **Effect size** (when appropriate)

### Error Bars

**Choose the appropriate measure:**

| Measure | Meaning | When to Use |
|---------|---------|-------------|
| **SD (Standard Deviation)** | Variability in the data | Showing data spread |
| **SEM (Standard Error of Mean)** | Precision of mean estimate | Showing measurement precision |
| **95% CI (Confidence Interval)** | Range likely to contain true mean | Showing statistical significance |

**Key rule:** Always state which measure is shown.

**Example caption:**
```
"Error bars represent 95% confidence intervals."
NOT: "Error bars represent standard error."
```

**Recommendation:** 95% CI preferred because non-overlapping CIs indicate significant differences.

### Significance Indicators

**Common notation:**
```
* p < 0.05
** p < 0.01
*** p < 0.001
n.s. or NS = not significant
```

**Alternative:** Show exact p-values in table or caption

**Best practice:** Define significance indicators in every figure caption or table footnote.

## Accessibility Considerations

### Color-Blind Friendly Design

**Recommendations:**
- Use color palettes designed for color-blind accessibility
- Don't rely on color alone (add patterns, shapes, or labels)
- Test figures in grayscale
- Avoid red-green combinations

**Color-blind safe palettes:**
- Blue-Orange
- Purple-Yellow
- Colorbrewer2.org palettes
- Viridis, Plasma, Inferno (for heatmaps)

### High Contrast

**Ensure readability:**
- Dark text on light background (or vice versa)
- Avoid low-contrast color combinations (gray on gray)
- Use thick enough lines (minimum 0.5-1 pt)
- Large enough text (minimum 8-10 pt after scaling)

### Screen and Print Compatibility

**Design for both media:**
- Use vector formats when possible (PDF, EPS, SVG)
- Minimum 300 dpi for raster images (TIFF, PNG)
- Test appearance at final print size
- Ensure color figures work in grayscale if printed

## Technical Requirements

### File Formats

**Vector formats** (preferred for graphs and diagrams):
- **PDF**: Universal, preserves quality
- **EPS**: Encapsulated PostScript, publishing standard
- **SVG**: Scalable vector graphics, web-friendly

**Raster formats** (for photos and images):
- **TIFF**: Uncompressed, high quality, large files
- **PNG**: Lossless compression, good for screen
- **JPEG**: Lossy compression, avoid for data figures

**Avoid:**
- Low-resolution screenshots
- Figures copied from presentations (usually too low resolution)
- Heavily compressed JPEGs (artifacts)

### Resolution Requirements

**Minimum standards:**
- **Line art** (graphs, diagrams): 300-600 dpi
- **Halftones** (photos, grayscale): 300 dpi
- **Combination** (images with labels): 300-600 dpi

**Best practice:** Create figures at final size and resolution.

### Dimensions

**Check journal requirements:**
- **Single column**: typically 8-9 cm (3-3.5 inches) wide
- **Double column**: typically 17-18 cm (6.5-7 inches) wide
- **Full page**: varies by journal

**Recommendation:** Design figures to fit single column when possible.

### Image Manipulation

**Allowed:**
- Brightness/contrast adjustment applied to entire image
- Color balance adjustment
- Cropping (with notation)
- Rotation

**NOT allowed:**
- Selective editing (e.g., enhancing bands in gels)
- Removing background artifacts
- Splicing images without clear indication
- Any manipulation that obscures, eliminates, or misrepresents data

**Ethical requirement:** Report all image adjustments in Methods section.

## Figure and Table Numbering

### Numbering System

**Figures:**
- Number consecutively in order of first mention in text
- Use Arabic numerals: Figure 1, Figure 2, Figure 3...
- Supplementary figures: Figure S1, Figure S2...

**Tables:**
- Number separately from figures
- Use Arabic numerals: Table 1, Table 2, Table 3...
- Supplementary tables: Table S1, Table S2...

### In-Text References

**Format:**
```
"Results are shown in Figure 1."
"Participant characteristics are presented in Table 2."
"Multiple analyses confirmed this finding (Figures 3-5)."
```

**NOT:**
```
"Figure 1 below shows..." (avoid "above" or "below" - pagination may change)
"The figure shows..." (always use specific number)
```

## Captions

### Caption Structure

**For figures:**
```
Figure 1. [One-sentence title]. [Additional description sentences providing context,
defining abbreviations, explaining panels, describing statistical tests, and noting
sample sizes].
```

**For tables:**
```
Table 1. [Descriptive Title]
[Table contents]
[Footnotes defining abbreviations, statistical methods, and providing additional context]
```

### Caption Content

**Essential information:**
1. What is being shown (brief title)
2. Detailed description of content
3. Definition of all abbreviations and symbols
4. Sample sizes
5. Statistical tests used
6. Meaning of error bars or annotations
7. Panel labels explained (if multiple panels)

**Example comprehensive caption:**
```
Figure 3. Cognitive performance improves with treatment over 12 weeks. (A) Mean Mini-Mental
State Examination (MMSE) scores at baseline, 6 weeks, and 12 weeks for treatment (blue) and
placebo (gray) groups. (B) Individual participant trajectories for treatment group. Error bars
represent 95% confidence intervals. Asterisks indicate significant between-group differences
(*p < 0.05, **p < 0.01, ***p < 0.001; repeated measures ANOVA with Bonferroni correction).
n = 42 treatment, n = 40 placebo. MMSE scores range from 0-30, with higher scores indicating
better cognitive function.
```

## Journal-Specific Requirements

### Before Creating Figures/Tables

**Check journal guidelines for:**
- Preferred file formats
- Resolution requirements
- Color specifications (RGB vs. CMYK)
- Maximum number of display items
- Dimension requirements
- Font restrictions
- Whether to embed figures in manuscript or submit separately

### During Submission

**Prepare checklist:**
- [ ] All figures/tables numbered correctly
- [ ] All cited in text in order
- [ ] Captions complete and self-explanatory
- [ ] Abbreviations defined
- [ ] Correct file format and resolution
- [ ] Appropriate size/dimensions
- [ ] High enough quality for print
- [ ] Color-blind friendly (if using color)
- [ ] Permissions obtained (if adapting from others' work)

## Common Pitfalls to Avoid

### Content Issues
1. **Duplication** between text, tables, and figures
2. **Insufficient context** (unclear what is shown)
3. **Too much information** in one display
4. **Missing key information** (sample sizes, units, statistics)
5. **Cherry-picking** data without showing full picture

### Design Issues
6. **Poor color choices** (not color-blind friendly)
7. **Inconsistent formatting** across displays
8. **Cluttered or busy designs**
9. **Too small text** at final size
10. **Misleading visualizations** (truncated axes, 3D distortions)

### Technical Issues
11. **Insufficient resolution** (pixelated when printed)
12. **Wrong file format** (lossy compression, non-vector graphs)
13. **Improper image manipulation** (undeclared editing)
14. **Missing scale bars** on images
15. **Figures that don't work in grayscale** (if journal prints in B&W)

## Tools for Creating Figures

### Graphing Software
- **R (ggplot2)**: Highly customizable, publication-quality, reproducible
- **Python (matplotlib, seaborn)**: Flexible, programmable, widely used
- **GraphPad Prism**: User-friendly, statistics integrated, common in life sciences
- **Origin**: Advanced graphing, popular in physics/engineering
- **Excel**: Basic graphs, widely available, limited customization
- **MATLAB**: Technical computing, good for complex visualizations

### Image Processing
- **ImageJ/Fiji**: Free, powerful, widely used in microscopy
- **Adobe Photoshop**: Professional standard, extensive tools
- **GIMP**: Free alternative to Photoshop
- **Adobe Illustrator**: Vector graphics, figure assembly
- **Inkscape**: Free vector graphics editor

### Best Practices for Software Choice
- Use tools that produce vector output for graphs
- Learn one tool well rather than many superficially
- Script your figure generation for reproducibility
- Save original data files separately from figure files

## Journal-Specific Figure and Table Requirements

### Understanding Journal Expectations

**Different journals have vastly different requirements for figures and tables.** Before creating display items, always consult your target journal's author guidelines for specific requirements.

### Common Journal-Specific Variations

| Aspect | Variation by Journal | Example Journals |
|--------|---------------------|------------------|
| **Number allowed** | 4-10 display items for research articles | Nature (4-6), PLOS ONE (unlimited), Science (4-5) |
| **File format** | TIFF, EPS, PDF, AI, or specific formats | Nature (EPS/PDF for line art), Cell (TIFF preferred) |
| **Resolution** | 300-1000 dpi depending on type | JAMA (300-600 dpi), Nature (300+ dpi) |
| **Color** | RGB vs. CMYK | Print journals: CMYK; Online: RGB |
| **Dimensions** | Single vs. double column widths | Nature (89mm or 183mm), Science (specific templates) |
| **Figure legends** | Length limits, specific format | Some journals: 150 word max per legend |
| **Table format** | Editable vs. image | Most prefer editable tables, not images |

### Venue-Specific Requirements Summary

| Venue Type | Display Limit | Format | Resolution | Key Features |
|-----------|--------------|--------|------------|--------------|
| **Nature/Science** | 4-6 main | EPS/PDF/TIFF | 300+ dpi | Extended data allowed; multi-panel figures |
| **Medical journals** | 3-5 | TIFF/EPS | 300-600 dpi | CONSORT diagrams; conservative design |
| **PLOS ONE** | Unlimited | TIFF/EPS/PDF | 300+ dpi | Must work in grayscale |
| **ML conferences** | 4-6 in 8-page limit | PDF (vector preferred) | Print quality | Compact design; info-dense figures |

**ML Conference Figure Requirements:**

**NeurIPS/ICML/ICLR:**
- Figures count toward page limit (typically 8 pages including references)
- Vector graphics (PDF) preferred for plots
- High information density expected
- Supplementary material for additional figures
- LaTeX template provided (use neurips_2024.sty or equivalent)
- Figures must be legible when printed in grayscale

**Computer Vision (CVPR/ICCV/ECCV):**
- Qualitative results figures critical
- Side-by-side comparisons standard
- Must show failure cases
- Supplementary material for videos/additional examples
- Often 6-8 main figures in 8-page papers

**Key ML conference figure practices:**
- **Ablation studies**: Compact tables/plots showing component contributions
- **Architecture diagrams**: Clear, professional block diagrams
- **Performance plots**: Include error bars/confidence intervals
- **Qualitative examples**: Show diverse, representative samples
- **Comparison tables**: Concise, bold best results

### Evaluation Criteria Across Venues

**What reviewers check:**
- **Necessity**: Each figure/table supports conclusions
- **Quality**: Professional appearance, sufficient resolution
- **Clarity**: Self-explanatory with captions; proper labeling
- **Statistics**: Error bars, sample sizes, significance indicators
- **Consistency**: Formatting uniform across display items

**Common rejection reasons:**
- Poor resolution or image quality
- Missing error bars or sample sizes
- Unclear or missing labels
- Too many figures (exceeds venue limits)
- Figures duplicate text information

**ML conference specific evaluation:**
- **Ablation studies**: Must demonstrate component contributions
- **Baselines**: Comparison with relevant prior work required
- **Error bars**: Confidence intervals/std dev expected
- **Architecture diagrams**: Must be clear and informative
- **Space efficiency**: Information density valued (page limits strict)

### Caption/Legend Styles by Venue

| Venue Type | Style | Example Features |
|-----------|-------|------------------|
| **Nature/Science** | Concise | Brief; *P<0.05; minimal methods |
| **Medical** | Formal | Title case; 95% CIs; statistical tests spelled out |
| **PLOS/BMC** | Detailed | Complete sentences; all abbreviations defined |
| **ML conferences** | Technical | Architecture details; hyperparameters; dataset info |

**ML conference caption example:**
```
Figure 1. Architecture of proposed model. (a) Encoder with 12 transformer layers.
(b) Attention visualization. (c) Performance vs. baseline on ImageNet (error bars:
95% CI over 3 runs).
```
- Technical precision
- Hyperparameters when relevant
- Dataset/experimental setup details
- Compact to save space

### Quick Adaptation Guide

**When changing venues:**
- **Journal → ML conference**: Compress figures; increase information density; add hyperparameters to captions
- **ML conference → journal**: Expand captions; separate dense figures; add more methodological detail
- **Specialist → broad journal**: Simplify; add explanatory panels; define terms in captions
- **Broad → specialist journal**: Add technical detail; use field-standard plot types

### Pre-Submission Figure/Table Checklist

**Technical (all venues):**
- [ ] Meets format requirements (PDF/EPS/TIFF)
- [ ] Sufficient resolution (300+ dpi) 
- [ ] Fits venue dimensions/page limits
- [ ] Self-explanatory captions
- [ ] All symbols/abbreviations defined
- [ ] Error bars defined; sample sizes noted

**ML conferences additional:**
- [ ] Figures fit in page limit (8-9 pages typical)
- [ ] Comparison with baselines shown
- [ ] Ablation studies included
- [ ] Architecture diagram clear
- [ ] Legible in grayscale

## Checklist for Final Review

### Before Submission

**For every figure:**
- [ ] High enough resolution (300+ dpi)?
- [ ] Correct file format per journal requirements?
- [ ] Correct dimensions for journal (single/double column)?
- [ ] Meets journal's RGB/CMYK requirements?
- [ ] Self-explanatory caption with all abbreviations defined?
- [ ] Caption length within journal limits?
- [ ] All symbols/colors explained in caption or legend?
- [ ] Error bars included and defined?
- [ ] Sample sizes noted?
- [ ] Statistical tests described?
- [ ] Axes labeled with units?
- [ ] Readable text at final print size?
- [ ] Works in grayscale or color-blind friendly?
- [ ] Referenced in text in correct order?
- [ ] Style matches target journal's published figures?

**For every table:**
- [ ] Clear, descriptive title?
- [ ] Title capitalization matches journal style?
- [ ] Column headers include units?
- [ ] Appropriate numerical precision?
- [ ] Abbreviations defined in footnotes?
- [ ] Statistical methods explained?
- [ ] Sample sizes included?
- [ ] Consistent formatting with other tables?
- [ ] Editable format (not image)?
- [ ] Referenced in text in correct order?
- [ ] Formatting matches target journal's tables?

**Overall:**
- [ ] Number of display items within journal limits?
- [ ] Appropriate number of display items (~1 per 1000 words)?
- [ ] No duplication between text, figures, and tables?
- [ ] Consistent formatting across all display items?
- [ ] All display items necessary (each tells important part of story)?
- [ ] Visual style matches target journal?
- [ ] Quality comparable to published examples in journal?

---

## Reference: Imrad_Structure

# IMRAD Structure Guide

## Overview

IMRAD (Introduction, Methods, Results, And Discussion) is the predominant organizational structure for scientific journal articles of original research. Adopted as the majority format since the 1970s, it is now the standard in medical, health, biological, chemical, engineering, and computer sciences.

## Why IMRAD?

The IMRAD structure mirrors the scientific method:
- **Introduction**: What question did you ask?
- **Methods**: How did you study it?
- **Results**: What did you find?
- **Discussion**: What does it mean?

This logical flow makes scientific papers easier to write, read, and evaluate.

## Complete Manuscript Components

A full scientific manuscript typically includes these sections in order:

1. **Title**
2. **Abstract**
3. **Introduction**
4. **Methods** (also called Materials and Methods, Methodology)
5. **Results**
6. **Discussion** (sometimes combined with Results)
7. **Conclusion** (sometimes part of Discussion)
8. **Acknowledgments**
9. **References**
10. **Supplementary Materials** (if applicable)

## Title

### Purpose
Attract readers and accurately represent the paper's content.

### Guidelines
- Be concise yet descriptive (typically 10-15 words)
- Include key variables and the relationship studied
- Avoid abbreviations, jargon, and question formats (unless the journal allows)
- Make it specific enough to distinguish from other studies
- Include key search terms for discoverability

### Examples
- Good: "Effects of High-Intensity Interval Training on Cardiovascular Function in Older Adults"
- Too vague: "Exercise and Health"
- Too detailed: "A Randomized Controlled Trial Examining the Effects of High-Intensity Interval Training Compared to Moderate Continuous Training on Cardiovascular Function Measured by VO2 Max in Adults Aged 60-75 Years"

## Abstract

### Purpose
Provide a complete, standalone summary enabling readers to decide if the full paper is relevant to them.

### Format: Flowing Paragraphs (Default)

**⚠️ CRITICAL: Write abstracts as flowing paragraphs, NOT with labeled sections.**

Most scientific papers use **unstructured abstracts** written as one or two cohesive paragraphs. This is the standard format for the majority of journals including Nature, Science, Cell, PNAS, and most field-specific journals.

❌ **WRONG - Structured abstract with labels:**
```
Background: Hospital-acquired infections remain a major cause of morbidity.
Methods: We conducted a 12-month before-after study...
Results: Post-intervention, surface contamination decreased by 47%...
Conclusions: UV-C disinfection significantly reduced infection rates.
```

✅ **CORRECT - Flowing paragraph style:**
```
Hospital-acquired infections remain a major cause of morbidity, yet optimal 
disinfection strategies remain unclear. We conducted a 12-month before-after 
study in a 500-bed teaching hospital to evaluate UV-C disinfection added to 
standard cleaning protocols. Environmental surfaces were cultured monthly and 
infection rates tracked via surveillance data. Post-intervention, surface 
contamination decreased by 47% (95% CI: 38-56%, p<0.001), and catheter-associated 
urinary tract infections declined from 3.2 to 1.8 per 1000 catheter-days (RR=0.56, 
95% CI: 0.38-0.83, p=0.004). No adverse effects were observed. These findings 
demonstrate that UV-C disinfection significantly reduces environmental contamination 
and infection rates, suggesting it may be a valuable addition to hospital infection 
control programs.
```

### Abstract Structure (as unified paragraph)

While written as flowing prose, the abstract should cover these elements in order:

1. **Context and problem** (1-2 sentences): Why the research matters, what gap exists
2. **Study description** (1-2 sentences): What was done and how (study design, methods)
3. **Key findings** (2-4 sentences): Main results with specific quantitative data
4. **Significance** (1-2 sentences): Interpretation, implications, and conclusions

### Length
- Typically 150-300 words (check journal requirements)
- Some journals allow up to 350 words

### Key Rules
- Write the abstract **last** (after completing all other sections)
- **Write as flowing paragraph(s)** - no labeled sections
- Make it fully understandable without reading the paper
- Do not cite references in the abstract
- Avoid abbreviations or define them at first use
- Use past tense for methods and results, present tense for conclusions
- Include key quantitative results with statistical measures
- Use transitions to connect sentences naturally

### When to Use Structured Abstracts (Exception)

Only use labeled sections (Background/Objective, Methods, Results, Conclusions) when:
- The journal **explicitly requires** structured abstracts in their author guidelines
- Common in some medical journals (JAMA, BMJ, Annals of Internal Medicine)
- Always check journal requirements before formatting

Even for structured abstracts, write each section as complete sentences, not fragments.

### Example: Flowing Paragraph Abstract

```
Transcriptomic aging clocks offer unique advantages for assessing biological age by 
capturing dynamic cellular states and acute responses to perturbations. Using the 
ARCHS4 database containing uniformly processed RNA-seq data from over 1.2 million 
human samples, we developed deep neural network models to predict chronological age 
from gene expression profiles. Our best-performing model achieved a mean absolute 
error of 4.2 years (R² = 0.89) on held-out test data, substantially outperforming 
traditional machine learning approaches including elastic net regression (MAE = 6.8 
years) and random forests (MAE = 5.9 years). Feature importance analysis identified 
genes enriched in senescence, inflammation, and mitochondrial function pathways as 
the strongest predictors. Cross-tissue validation revealed that lung and blood 
samples yielded the most accurate predictions, while liver showed the highest 
variance. These findings establish deep learning as a powerful approach for 
transcriptomic age prediction and identify candidate biomarkers for biological 
aging assessment.
```

## Introduction

### Purpose
Convince readers that the research addresses an important question using an appropriate approach.

### Structure and Content

**Paragraph 1: The Big Picture**
- Establish the broad research area
- Explain why this topic matters
- Use present tense for established facts
- Keep it accessible to non-specialists

**Paragraphs 2-3: Narrowing Down**
- Review relevant prior research
- Show what is already known
- Identify controversies or limitations in existing work
- Create a logical progression toward the gap

**Paragraph 4: The Gap**
- Explicitly identify what remains unknown
- Explain why this knowledge gap is problematic
- Connect the gap to the big picture importance

**Final Paragraph: This Study**
- State the specific research question or hypothesis
- Describe the overall approach briefly
- Explain how this study addresses the gap
- Optional: Preview key findings (some journals discourage this)

### Length
- Typically 1.5-2 pages (depending on journal)
- Usually 4-5 paragraphs
- Shorter for letters/brief communications

### Verb Tense
- **Present tense**: Established facts ("Exercise improves cardiovascular health")
- **Past tense**: Previous studies and their findings ("Smith et al. found that...")
- **Present/past tense**: Your study aims ("This study investigates..." or "This study investigated...")

### Common Mistakes to Avoid
- Starting too broad (e.g., "Since the beginning of time...")
- Exhaustive literature review (save for review articles)
- Citing irrelevant or outdated references
- Failing to identify a clear gap
- Weak justification for the study
- Not stating a clear research question or hypothesis
- Including methods or results (these belong in later sections)

### Key Questions to Answer
1. What do we know about this topic?
2. What don't we know? (the gap)
3. Why does this gap matter?
4. What did this study aim to find out?

## Methods

### Purpose
Provide sufficient detail for others to replicate the study and evaluate its validity.

### Key Principle
Another expert in the field should be able to repeat your experiment exactly as you performed it.

### Standard Subsections

#### Study Design
- State the overall design (e.g., randomized controlled trial, cohort study, cross-sectional survey)
- Justify the design choice if not obvious
- Mention blinding, randomization, or controls if applicable

#### Participants/Subjects/Sample
- Define the population of interest
- Describe inclusion and exclusion criteria precisely
- Report sample size and how it was determined (power analysis)
- Explain recruitment methods and setting
- For animals: specify species, strain, age, sex, housing conditions

#### Materials and Equipment
- List all materials, reagents, and equipment used
- Include manufacturer names and locations (in parentheses)
- Specify catalog numbers for specialized items
- Report software names and versions

#### Procedures
- Describe what was done in chronological order
- Include sufficient detail for replication
- Use subheadings to organize complex procedures
- Specify timing (e.g., "incubated for 2 hours at 37°C")
- For surveys/interviews: describe instruments, validation, administration

#### Measurements and Outcomes
- Define all variables measured
- Specify primary and secondary outcomes
- Describe measurement instruments and their validity
- Include units of measurement

#### Statistical Analysis
- Name all statistical tests used
- Justify test selection
- State significance level (typically α = 0.05)
- Report power analysis for sample size
- Name statistical software with version
- Describe handling of missing data
- Mention adjustments for multiple comparisons if applicable

#### Ethical Considerations
- State IRB/ethics committee approval (with approval number)
- Mention informed consent procedures
- For human studies: state adherence to Helsinki Declaration
- For animal studies: state adherence to relevant guidelines (e.g., ARRIVE)

### Length
- Typically 2-4 pages
- Proportional to study complexity

### Verb Tense
- **Past tense** for actions you performed ("We measured...", "Participants completed...")
- **Present tense** for established procedures ("PCR amplifies...", "The questionnaire contains...")

### Common Mistakes
- Insufficient detail for replication
- Methods appearing for the first time in Results
- Including results or discussion
- Missing statistical tests
- Undefined abbreviations
- Lack of ethical approval statement

## Results

### Purpose
Present the findings objectively without interpretation.

### Key Principle
Show, don't interpret. Save interpretation for the Discussion.

### Structure and Content

**Opening Paragraph**
- Describe the participants/sample characteristics
- Report recruitment flow (e.g., screened, enrolled, completed)
- Consider including a CONSORT-style flow diagram

**Subsequent Paragraphs**
- Present results in logical order (usually primary outcome first)
- Follow the order of objectives stated in Introduction
- Organize by theme or by chronology, depending on what's clearest
- Reference figures and tables by number

**Each Finding Should Include:**
- The observed result
- The direction of the effect
- The magnitude of the effect
- The statistical significance
- The confidence interval

**Example**: "Mean systolic blood pressure decreased by 12 mmHg in the intervention group compared to 3 mmHg in controls (difference: 9 mmHg, 95% CI: 4-14 mmHg, p=0.002)."

### Integration with Figures and Tables

**When to Use:**
- **Figures**: Trends, patterns, distributions, comparisons, relationships
- **Tables**: Precise values, demographic data, multiple variables

**How to Reference:**
- "Figure 1 shows the distribution of..." (not "Figure 1 below")
- "Table 2 presents baseline characteristics..."
- Don't repeat all table data in text; highlight key findings
- Each figure/table should be referenced in text

### Figures and Tables Guidelines
- Number consecutively in order of mention
- Include complete, standalone captions
- Define all abbreviations in caption or footnote
- Report sample sizes (n)
- Indicate statistical significance (*, p-values)
- Use consistent formatting

### Statistical Reporting

**Required Elements:**
- Test statistic (t, F, χ², etc.)
- Degrees of freedom
- p-value (exact if p > 0.001, otherwise report as "p < 0.001")
- Effect size and confidence interval
- Sample sizes

**Example**: "Groups differed significantly on test performance (t(48) = 3.21, p = 0.002, Cohen's d = 0.87, 95% CI: 0.34-1.40)."

### Length
- Typically 2-4 pages
- Roughly equivalent to Methods length

### Verb Tense
- **Past tense** for your findings ("The mean was...", "Participants showed...")

### Common Mistakes
- Interpreting results (save for Discussion)
- Repeating all table/figure data in text
- Presenting new methods
- Insufficient statistical detail
- Inconsistent units or notation
- Not addressing negative or unexpected findings
- Selective reporting (all tested hypotheses should be reported)

### Organization Strategies

**By Objective:**
```
Effect of intervention on primary outcome
Effect of intervention on secondary outcome A
Effect of intervention on secondary outcome B
```

**By Analysis Type:**
```
Descriptive statistics
Univariate analyses
Multivariate analyses
```

**Chronological:**
```
Baseline characteristics
Short-term outcomes (1 month)
Long-term outcomes (6 months)
```

## Discussion

### Purpose
Interpret findings, relate them to existing knowledge, acknowledge limitations, and propose future directions.

### Structure and Content

**Paragraph 1: Summary of Main Findings**
- Restate the primary objective or hypothesis
- Summarize the principal findings in 2-4 sentences
- Avoid repeating details from Results
- State clearly whether the hypothesis was supported

**Paragraphs 2-4: Interpretation in Context**
- Compare your findings with previous research
- Explain agreements and disagreements with prior work
- Propose mechanisms or explanations for findings
- Discuss unexpected results
- Consider alternative explanations
- Address whether findings support or refute existing theories

**Paragraph 5: Strengths and Limitations**
- Acknowledge study limitations honestly
- Explain how limitations might affect interpretation
- Mention study strengths (design, sample, methods)
- Avoid generic limitations ("larger sample needed")—be specific

**Paragraph 6: Implications**
- Clinical implications (for medical research)
- Practical applications
- Policy implications
- Theoretical contributions

**Final Paragraph: Conclusions and Future Directions**
- Summarize the take-home message
- Suggest specific future research to address gaps or limitations
- End with a strong concluding statement

### Length
- Typically 3-5 pages
- Usually the longest section

### Verb Tense
- **Past tense**: Your study findings ("We found that...", "The results showed...")
- **Present tense**: Established facts and your interpretations ("This suggests that...", "These findings indicate...")
- **Future tense**: Implications and future research ("Future studies should investigate...")

### Discussion Strategies

**Comparing to Prior Work:**
```
"Our finding of a 30% reduction in symptoms aligns with Smith et al. (2023), who
reported a 28% reduction using a similar intervention. However, Jones et al. (2022)
found no significant effect, possibly due to their use of a less intensive protocol."
```

**Proposing Mechanisms:**
```
"The observed improvement in cognitive function may result from increased cerebral
blood flow, as evidenced by the concurrent increase in functional MRI signals in the
prefrontal cortex. This interpretation is consistent with the vascular hypothesis of
cognitive enhancement."
```

**Acknowledging Limitations:**
```
"The cross-sectional design prevents causal inference. Additionally, the convenience
sample from a single academic medical center may limit generalizability to community
settings. Self-reported measures may introduce recall bias, though we attempted to
minimize this through structured interviews."
```

### Common Mistakes
- Simply repeating results without interpretation
- Over-interpreting findings or claiming causation without warrant
- Ignoring inconsistent or negative findings
- Failing to compare with existing literature
- Introducing new data or methods
- Generic or superficial discussion of limitations
- Overgeneralization beyond the study population
- Missing the "so what?"—failing to explain significance

### Key Questions to Answer
1. What do these findings mean?
2. How do they compare to prior research?
3. Why might differences exist?
4. What are alternative explanations?
5. What are the limitations?
6. What are the practical implications?
7. What should future research investigate?

## Conclusion

### Purpose
Provide a concise summary of key findings and their significance.

### Placement
- May be a separate section or the final paragraph of Discussion (check journal requirements)

### Content
- 1-2 paragraphs maximum
- Restate the main finding(s)
- Emphasize the significance or implications
- End with a strong, memorable statement
- Do NOT introduce new information

### Example
```
This randomized trial demonstrates that a 12-week mindfulness intervention significantly
reduces anxiety symptoms in college students, with effects persisting at 6-month follow-up.
These findings support the integration of mindfulness-based programs into university mental
health services. Given the scalability and cost-effectiveness of group-based mindfulness
training, this approach offers a promising strategy to address the growing mental health
crisis in higher education.
```

## Additional Sections

### Acknowledgments
- Thank funding sources (with grant numbers)
- Acknowledge substantial contributions not qualifying for authorship
- Thank those who provided materials, equipment, or assistance
- Declare any conflicts of interest

### References
- Format according to journal style (see `citation_styles.md`)
- Verify all citations are accurate
- Ensure all citations appear in text and vice versa
- Typical range: 20-50 references for original research

### Supplementary Materials
- Additional figures, tables, or data sets
- Detailed protocols or questionnaires
- Video or audio files
- Large datasets or code repositories

## Tense Usage Summary

| Section | Verb Tense |
|---------|-----------|
| Abstract - Background | Present (established facts) or past (prior studies) |
| Abstract - Methods | Past |
| Abstract - Results | Past |
| Abstract - Conclusions | Present |
| Introduction - General background | Present |
| Introduction - Prior studies | Past |
| Introduction - Your objectives | Present or past |
| Methods | Past (your actions), present (general procedures) |
| Results | Past |
| Discussion - Your findings | Past |
| Discussion - Interpretations | Present |
| Discussion - Prior work | Present or past |
| Conclusion | Present |

## IMRAD Variations

### Combined Results and Discussion
- Some journals allow or require this format
- Interweaves presentation and interpretation
- Each result is presented then immediately discussed
- Useful for complex studies with multiple experiments

### IMRaD without separate Conclusion
- Conclusion integrated into final Discussion paragraph
- Common in many journals

### Extended IMRAD (ILMRaD)
- Adds "Literature Review" as separate section
- More common in theses and dissertations

## Adapting IMRAD to Different Study Types

### Clinical Trials
- Add CONSORT flow diagram in Results
- Include trial registration number in Methods
- Report adverse events in Results

### Systematic Reviews/Meta-Analyses
- Methods describes search strategy and inclusion criteria
- Results includes PRISMA flow diagram and synthesis
- May have additional sections (risk of bias assessment)

### Case Reports
- Introduction: background on the condition
- Case Presentation: replaces Methods and Results
- Discussion: relates case to literature

### Observational Studies
- Follow STROBE guidelines
- Careful attention to potential confounders in Methods
- Discussion addresses causality limitations

## Venue-Specific Structure Expectations

### Journal vs. Conference Formats

| Venue Type | Length | Structure | Methods Placement | Key Focus |
|-----------|--------|-----------|-------------------|-----------|
| **Nature/Science** | 2,000-4,500 words | Modified IMRAD | Supplement | Broad significance |
| **Medical** | 2,700-3,500 words | Strict IMRAD | Main text | Clinical outcomes |
| **Field journals** | 3,000-6,000 words | Standard IMRAD | Main text | Technical depth |
| **ML conferences** | 8-9 pages (~6,000 words) | Intro-Method-Experiments-Conclusion | Main text (concise) | Novel contribution |

### ML Conference Structure (NeurIPS/ICML/ICLR)

**Typical 8-page structure:**
1. **Abstract** (150-200 words): Problem, method, key results
2. **Introduction** (1 page): Motivation, contribution summary, related work overview
3. **Method** (2-3 pages): Technical approach, architecture, algorithms
4. **Experiments** (2-3 pages): Setup, datasets, baselines, results, ablations
5. **Related Work** (0.5-1 page, often in appendix): Detailed literature comparison
6. **Conclusion** (0.25-0.5 pages): Summary, limitations, future work
7. **References** (within page limit or separate depending on conference)
8. **Appendix/Supplement** (unlimited): Additional experiments, proofs, details

**Key differences from journals:**
- **Contribution bullets**: Often numbered list in intro (e.g., "Our contributions are: (1)... (2)... (3)...")
- **No separate Results/Discussion**: Integrated in Experiments section
- **Ablation studies**: Critical component showing what matters
- **Computational requirements**: Often required (training time, GPUs, memory)
- **Code availability**: Increasingly expected

### Section Length Proportions

| Venue | Intro | Methods | Results/Experiments | Discussion/Conclusion |
|-------|-------|---------|---------------------|----------------------|
| **Nature/Science** | 10% | 15%* | 40% | 35% |
| **Medical (NEJM/JAMA)** | 10% | 25% | 30% | 35% |
| **Field journals** | 20% | 25% | 30% | 25% |
| **ML conferences** | 12-15% | 30-35% | 40-45% | 5-8% |

*Methods often in supplement for Nature/Science

**Key medical journal features:**
- NEJM/Lancet/JAMA: Strict IMRAD; clinical focus; structured Discussion; CONSORT/STROBE compliance
- Clear primary/secondary outcomes; statistical pre-specification

**Key ML conference features:**
- Numbered contribution list in intro
- Method details with pseudocode/equations
- Extensive experiments: main results, ablations, analysis
- Brief conclusion (limitations noted)
- Related work often in appendix

### Writing Style by Venue

| Venue | Audience | Intro Focus | Methods Detail | Results/Experiments | Discussion/Conclusion |
|-------|----------|-------------|----------------|---------------------|----------------------|
| **Nature/Science** | Non-specialists | Broad significance | Brief, supplement | Story-driven | Broad implications |
| **Medical** | Clinicians | Clinical problem | Comprehensive | Primary outcome first | Clinical relevance |
| **Specialized** | Experts | Field context | Full technical | By experiment | Mechanistic depth |
| **ML conferences** | ML researchers | Novel contribution | Reproducible | Baselines, ablations | Brief, limitations |

**ML conference emphasis:**
- **Introduction**: Clear problem statement; numbered contributions; positioning vs. prior work
- **Method**: Mathematical notation; pseudocode; architecture diagrams; complexity analysis
- **Experiments**: Datasets described; multiple baselines; ablation studies; error analysis
- **Conclusion**: Summary; acknowledged limitations; broader impact (if required)

### Evaluation Across Venues

**What gets checked:**
- **Fit**: Appropriate for venue scope and audience
- **Length**: Within limits (strict for conferences)
- **Clarity**: Writing quality sufficient; claims supported
- **Reproducibility**: Methods enable replication
- **Completeness**: All outcomes reported; limitations acknowledged

**Common rejection reasons:**
- Insufficient significance for venue
- Methods lack detail for reproduction
- Results don't support claims
- Discussion overstates findings
- Page/word limits exceeded (conferences strict)

**ML conference specific evaluation:**
- Clear problem formulation and motivation
- Novelty and contribution well-articulated
- Baselines comprehensive and fair
- Ablation studies demonstrate what works
- Code/data availability (increasingly required)
- Reproducibility information (seeds, hyperparameters)

### Quick Adaptation Guide

**Journal → ML conference:**
- Condense intro; add numbered contributions
- Methods: keep concise, add pseudocode
- Combine Results+Discussion → Experiments section
- Add extensive ablations and baseline comparisons
- Brief conclusion with limitations

**ML conference → Journal:**
- Expand introduction with more background
- Separate Methods section with full details
- Split Experiments into Results and Discussion
- Remove contribution numbering
- Expand limitations discussion

**Specialist → Broad journal:**
- Simplify intro; emphasize broad significance
- Move technical methods to supplement
- Story-driven results organization
- Lead discussion with implications

**Broad → Specialist:**
- Add detailed literature review
- Full methods in main text
- Organize results by experiment
- Add mechanistic discussion depth

### Pre-Submission Structure Checklist

**All venues:**
- [ ] Word/page count within limits
- [ ] Section proportions appropriate
- [ ] Writing style matches venue
- [ ] Methods enable reproducibility
- [ ] Limitations acknowledged

**ML conferences add:**
- [ ] Contributions clearly listed
- [ ] Ablation studies included
- [ ] Baselines comprehensive
- [ ] Hyperparameters/seeds reported
- [ ] Code availability statement

---

## Reference: Professional_Report_Formatting

# Professional Report Formatting for Scientific Documents

This reference guide covers professional formatting for scientific reports, technical documents, and white papers. Use the `scientific_report.sty` LaTeX style package for consistent, professional output.

---

## When to Use Professional Report Formatting

### Use This Style For:

- **Research reports** - Internal and external research summaries
- **Technical reports** - Detailed technical documentation and analyses
- **White papers** - Position papers and thought leadership documents
- **Grant reports** - Progress reports and final grant reports
- **Policy briefs** - Research-informed policy recommendations
- **Industry reports** - Technical reports for industry audiences
- **Internal research summaries** - Team and stakeholder communications
- **Feasibility studies** - Technical and research feasibility assessments
- **Project documentation** - Research project deliverables

### Do NOT Use This Style For:

- **Journal manuscripts** → Use `venue-templates` skill for journal-specific formatting
- **Conference papers** → Use `venue-templates` skill for conference requirements
- **Academic theses/dissertations** → Use institutional templates
- **Peer-reviewed submissions** → Follow journal author guidelines

**Key Distinction**: Professional report formatting prioritizes visual appeal and readability for general audiences, while journal manuscripts must follow strict publisher requirements.

---

## Overview of scientific_report.sty

The `scientific_report.sty` package provides:

| Feature | Description |
|---------|-------------|
| Typography | Helvetica font family for modern, professional appearance |
| Color Scheme | Coordinated blues, greens, oranges, and purples |
| Box Environments | Colored boxes for organizing content types |
| Tables | Professional styling with alternating rows |
| Figures | Consistent caption formatting |
| Headers/Footers | Professional page headers and footers |
| Scientific Commands | Shortcuts for p-values, effect sizes, statistics |

### Basic Document Setup

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{scientific_report}

\begin{document}
% Your content here
\end{document}
```

**Compilation**: Use XeLaTeX or LuaLaTeX for proper Helvetica font rendering:
```bash
xelatex document.tex
```

---

## Box Environments for Content Organization

### Purpose and Usage

Colored boxes help readers quickly identify different types of content. Use them strategically to highlight important information.

### Available Box Environments

| Environment | Color | Purpose |
|-------------|-------|---------|
| `keyfindings` | Blue | Major findings, discoveries, key takeaways |
| `methodology` | Green | Methods, procedures, study design |
| `resultsbox` | Blue-green | Statistical results, data highlights |
| `recommendations` | Purple | Recommendations, action items, implications |
| `limitations` | Orange | Limitations, cautions, caveats |
| `criticalnotice` | Red | Critical warnings, safety notices |
| `definition` | Gray | Definitions, notes, supplementary info |
| `executivesummary` | Blue (shadow) | Executive summaries |
| `hypothesis` | Light blue | Research hypotheses |

### Key Findings Box

Use for major findings and important discoveries:

```latex
\begin{keyfindings}[Research Highlights]
Our analysis revealed three significant findings:
\begin{enumerate}
    \item Treatment A was 40% more effective than control (\pvalue{0.001})
    \item Effect sizes were clinically meaningful (\effectsize{d}{0.82})
    \item Benefits persisted at 12-month follow-up
\end{enumerate}
\end{keyfindings}
```

**Best Practices:**
- Use sparingly (1-3 per chapter maximum)
- Reserve for genuinely important findings
- Include specific numbers and statistics
- Write concisely

### Methodology Box

Use for highlighting methods and procedures:

```latex
\begin{methodology}[Study Design]
This double-blind, randomized controlled trial employed a 2×2 factorial
design. Participants (\samplesize{450}) were randomized to one of four
conditions: (1) Treatment A, (2) Treatment B, (3) Combined A+B, or
(4) Placebo control.
\end{methodology}
```

**Best Practices:**
- Summarize key methodological features
- Use at the start of methods sections
- Include sample size and design type
- Keep technical but accessible

### Results Box

Use for highlighting specific statistical results:

```latex
\begin{resultsbox}[Primary Outcome Analysis]
Mixed-effects regression revealed a significant treatment × time
interaction, \effectsize{F(3, 446)}{8.72}, \psig{< 0.001},
$\eta^2_p$ = 0.055, indicating differential improvement across
treatment conditions over the study period.
\end{resultsbox}
```

**Best Practices:**
- Report complete statistical information
- Use scientific notation commands
- Include effect sizes alongside p-values
- One box per major analysis

### Recommendations Box

Use for recommendations and implications:

```latex
\begin{recommendations}[Clinical Practice Guidelines]
Based on our findings, we recommend:
\begin{enumerate}
    \item \textbf{Primary recommendation:} Implement screening protocol
        for high-risk populations.
    \item \textbf{Secondary recommendation:} Adjust treatment intensity
        based on baseline severity scores.
    \item \textbf{Monitoring:} Reassess at 3-month intervals.
\end{enumerate}
\end{recommendations}
```

**Best Practices:**
- Make recommendations specific and actionable
- Prioritize with clear labels
- Link to supporting evidence
- Include implementation guidance

### Limitations Box

Use for limitations, caveats, and cautions:

```latex
\begin{limitations}[Study Limitations]
Several limitations should be considered:
\begin{itemize}
    \item \textbf{Sample:} Participants were recruited from academic
        medical centers, limiting generalizability to community settings.
    \item \textbf{Design:} The observational design precludes causal
        inference about treatment effects.
    \item \textbf{Attrition:} 15% dropout rate may introduce bias.
\end{itemize}
\end{limitations}
```

**Best Practices:**
- Be honest and thorough
- Explain implications of each limitation
- Suggest how future research could address limitations
- Don't over-qualify findings

### Critical Notice Box

Use for critical warnings or safety information:

```latex
\begin{criticalnotice}[Safety Warning]
\textbf{Contraindication:} This intervention is contraindicated for
patients with [condition]. Monitor for [adverse effects] and discontinue
immediately if [symptoms] occur. Report serious adverse events to [contact].
\end{criticalnotice}
```

**Best Practices:**
- Reserve for genuinely critical information
- Be clear and direct
- Include specific actions to take
- Provide contact information if relevant

### Definition Box

Use for definitions and explanatory notes:

```latex
\begin{definition}[Effect Size]
An \textbf{effect size} is a quantitative measure of the magnitude of a
phenomenon. Unlike significance tests, effect sizes are independent of
sample size and allow comparison across studies. Common measures include
Cohen's \textit{d} for mean differences and Pearson's \textit{r} for
correlations.
\end{definition}
```

**Best Practices:**
- Define technical terms at first use
- Keep definitions concise
- Include practical interpretation guidance
- Use for audience-appropriate terms

---

## Professional Table Formatting

### Design Principles

1. **Clean appearance**: Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`)
2. **Alternating rows**: Apply `\rowcolor{tablealt}` to every other row
3. **Clear headers**: Bold headers for column identification
4. **Appropriate precision**: Report statistics to appropriate decimal places
5. **Complete information**: Include sample sizes, units, and notes

### Standard Data Table

```latex
\begin{table}[htbp]
\centering
\caption{Demographic Characteristics by Treatment Group}
\label{tab:demographics}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Characteristic} & \textbf{Treatment} & \textbf{Control} \\
 & (\samplesize{225}) & (\samplesize{225}) \\
\midrule
Age, years, \meansd{M}{SD} & \meansd{42.3}{12.5} & \meansd{43.1}{11.8} \\
\rowcolor{tablealt} Female, n (\%) & 128 (56.9) & 121 (53.8) \\
Education, years, \meansd{M}{SD} & \meansd{14.2}{2.8} & \meansd{14.5}{2.6} \\
\rowcolor{tablealt} Baseline score, \meansd{M}{SD} & \meansd{52.4}{15.3} & \meansd{51.8}{14.9} \\
\bottomrule
\end{tabular}
\figurenote{No significant differences between groups at baseline (all \textit{p} > .10).}
\end{table}
```

### Results Table with Significance Indicators

```latex
\begin{table}[htbp]
\centering
\caption{Treatment Effects on Primary and Secondary Outcomes}
\label{tab:results}
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Outcome} & \textbf{Treatment} & \textbf{Control} & \textbf{Effect} & \textbf{p} \\
 & \meansd{M}{SD} & \meansd{M}{SD} & \textbf{(d)} & \\
\midrule
Primary outcome & \meansd{68.4}{14.2} & \meansd{54.1}{15.8} & 0.95\sigthree & <.001 \\
\rowcolor{tablealt} Secondary A & \meansd{4.2}{1.1} & \meansd{3.5}{1.2} & 0.61\sigtwo & .003 \\
Secondary B & \meansd{22.8}{5.4} & \meansd{21.2}{5.1} & 0.31\sigone & .042 \\
\rowcolor{tablealt} Secondary C & \meansd{8.9}{2.3} & \meansd{8.5}{2.4} & 0.17\signs & .285 \\
\bottomrule
\end{tabular}

\vspace{0.5em}
{\small \siglegend}
\end{table}
```

### Comparison Table with Quality Ratings

```latex
\begin{table}[htbp]
\centering
\caption{Evidence Summary by Study}
\label{tab:evidence}
\begin{tabular}{@{}llccc@{}}
\toprule
\textbf{Study} & \textbf{Design} & \textbf{N} & \textbf{Quality} & \textbf{Evidence} \\
\midrule
Smith et al. (2024) & RCT & 450 & \qualityhigh & \evidencestrong \\
\rowcolor{tablealt} Jones et al. (2023) & Cohort & 1,250 & \qualitymedium & \evidencemoderate \\
Chen et al. (2023) & Case-control & 320 & \qualitymedium & \evidencemoderate \\
\rowcolor{tablealt} Lee et al. (2022) & Cross-sectional & 890 & \qualitylow & \evidenceweak \\
\bottomrule
\end{tabular}
\end{table}
```

---

## Figure and Caption Styling

### Caption Formatting

The style package automatically formats captions with:
- Blue, bold figure labels
- Gray descriptive text
- Centered alignment with margins

### Standard Figure

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/results_comparison.png}
\caption{Comparison of Outcome Scores by Treatment Condition and Time Point}
\label{fig:results}
\end{figure}
```

### Figure with Source Attribution

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{../figures/trend_analysis.png}
\caption{Trends in Key Metrics Over the Study Period}
\figuresource{Study data collected January--December 2024}
\label{fig:trends}
\end{figure}
```

### Figure with Explanatory Note

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{../figures/conceptual_model.png}
\caption{Conceptual Model of Hypothesized Relationships}
\figurenote{Solid arrows indicate primary pathways; dashed arrows indicate moderated relationships. Numbers represent standardized coefficients.}
\label{fig:model}
\end{figure}
```

---

## Color Palette and Visual Hierarchy

### Color Usage Guidelines

| Color | Use For | Avoid Using For |
|-------|---------|-----------------|
| Primary Blue | Headers, important findings | Warnings, cautions |
| Science Green | Methods, positive results | Negative findings |
| Orange | Cautions, limitations | Positive findings |
| Red | Critical warnings | Routine content |
| Purple | Recommendations | Findings, methods |
| Gray | Definitions, notes | Key findings |

### Visual Hierarchy

1. **Executive summary boxes** (shadow effect) - Most prominent
2. **Colored content boxes** - High prominence for key content
3. **Tables with color** - Medium prominence for data
4. **Body text** - Standard prominence
5. **Definition boxes** - Lower prominence for supplementary info

### Accessibility Considerations

- Color palette is designed to be distinguishable for common color vision deficiencies
- All boxes have both color AND structural indicators (borders, backgrounds)
- Text maintains sufficient contrast ratios
- Don't rely solely on color to convey meaning

---

## Typography Guidelines

### Font Specifications

| Element | Font | Size | Color |
|---------|------|------|-------|
| Body text | Helvetica | 11pt | Dark gray (#424242) |
| Chapter titles | Helvetica Bold | Huge | Primary blue (#003366) |
| Section headings | Helvetica Bold | Large | Primary blue (#003366) |
| Subsections | Helvetica Bold | large | Secondary blue (#4A90E2) |
| Subsubsections | Helvetica Bold | normalsize | Dark gray (#424242) |

### Spacing

- Line spacing: 1.15 (for readability)
- Paragraph spacing: 0.5em between paragraphs
- Page margins: 1 inch on all sides

### Best Typography Practices

1. **Consistency**: Use the same formatting for similar elements
2. **Hierarchy**: Use visual weight to indicate importance
3. **Readability**: Adequate spacing and contrast
4. **Professionalism**: Avoid mixing fonts or excessive formatting

---

## Scientific Notation Commands Reference

### Statistical Reporting

| Command | Output | When to Use |
|---------|--------|-------------|
| `\pvalue{0.023}` | *p* = 0.023 | Report p-values |
| `\psig{< 0.001}` | ***p*** = < 0.001 | Significant p-values (bold) |
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] | Confidence intervals |
| `\effectsize{d}{0.75}` | d = 0.75 | Effect sizes |
| `\samplesize{250}` | *n* = 250 | Sample sizes |
| `\meansd{42.5}{8.3}` | 42.5 ± 8.3 | Mean with SD |

### Significance Indicators

| Command | Output | Meaning |
|---------|--------|---------|
| `\sigone` | * | p < 0.05 |
| `\sigtwo` | ** | p < 0.01 |
| `\sigthree` | *** | p < 0.001 |
| `\signs` | ns | not significant |
| `\siglegend` | Full legend | For table footnotes |

### Quality and Evidence Ratings

| Command | Output | Meaning |
|---------|--------|---------|
| `\qualityhigh` | **HIGH** (green) | High quality |
| `\qualitymedium` | **MEDIUM** (orange) | Moderate quality |
| `\qualitylow` | **LOW** (red) | Low quality |
| `\evidencestrong` | **Strong** (green) | Strong evidence |
| `\evidencemoderate` | **Moderate** (orange) | Moderate evidence |
| `\evidenceweak` | **Weak** (red) | Weak evidence |

### Trend Indicators

| Command | Symbol | Meaning |
|---------|--------|---------|
| `\trendup` | ▲ (green) | Increasing trend |
| `\trenddown` | ▼ (red) | Decreasing trend |
| `\trendflat` | → (gray) | Stable/no change |

---

## Complete LaTeX Examples

### Executive Summary Example

```latex
\chapter*{Executive Summary}
\addcontentsline{toc}{chapter}{Executive Summary}

\begin{executivesummary}[Report Highlights]
This report presents findings from a comprehensive study of [topic]
involving \samplesize{450} participants across 12 research sites.
The research addressed [key question] using [methodology].
\end{executivesummary}

\subsection*{Key Findings}

\begin{keyfindings}
\begin{enumerate}
    \item The primary intervention demonstrated a large effect
          (\effectsize{d}{0.82}, \psig{< 0.001}).
    \item Benefits were maintained at 12-month follow-up.
    \item Cost-effectiveness analysis supports implementation.
\end{enumerate}
\end{keyfindings}

\subsection*{Recommendations}

\begin{recommendations}
Based on these findings, we recommend:
\begin{enumerate}
    \item Implement the intervention in [settings].
    \item Train practitioners using the standardized protocol.
    \item Monitor outcomes using the validated measures.
\end{enumerate}
\end{recommendations}
```

### Methods Section Example

```latex
\chapter{Methods}

\begin{methodology}[Study Overview]
This randomized controlled trial employed a parallel-group design with
1:1 allocation to intervention or control conditions. The study was
conducted across 12 sites between January 2023 and December 2024.
\end{methodology}

\section{Participants}

A total of \samplesize{450} participants were enrolled. Eligibility
criteria were:

\begin{itemize}
    \item Age 18--65 years
    \item Diagnosis of [condition] per [criteria]
    \item No contraindications to [intervention]
\end{itemize}

Table~\ref{tab:participants} presents participant characteristics.

\begin{limitations}[Recruitment Challenges]
Recruitment was slower than anticipated due to [reasons]. The final
sample was 10% below target, which may affect statistical power for
secondary analyses.
\end{limitations}
```

### Results Section Example

```latex
\chapter{Results}

\section{Primary Outcome}

\begin{resultsbox}[Primary Analysis]
Mixed-effects regression revealed a significant treatment effect,
\effectsize{F(1, 448)}{42.18}, \psig{< 0.001}, with a large effect
size (\effectsize{d}{0.82}). The treatment group showed significantly
greater improvement (\meansd{16.4}{5.2} points) compared to control
(\meansd{8.1}{4.8} points).
\end{resultsbox}

Figure~\ref{fig:primary} illustrates the treatment effects over time.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/primary_outcome.png}
\caption{Primary Outcome Scores by Treatment Group and Time Point}
\figurenote{Error bars represent 95\% confidence intervals.}
\label{fig:primary}
\end{figure}

\section{Secondary Outcomes}

Results for secondary outcomes are presented in Table~\ref{tab:secondary}.
```

### Discussion Section Example

```latex
\chapter{Discussion}

\section{Summary of Findings}

\begin{keyfindings}[Main Conclusions]
\begin{enumerate}
    \item The intervention was highly effective (primary hypothesis
          \highlight{supported})
    \item Effects were clinically meaningful and durable
    \item Evidence strength: \evidencestrong
\end{enumerate}
\end{keyfindings}

\section{Limitations}

\begin{limitations}
Several limitations warrant consideration:
\begin{itemize}
    \item The sample was predominantly [demographic], limiting
          generalizability.
    \item Attrition was higher in the control group (18\% vs. 12\%).
    \item Self-report measures may be subject to response bias.
\end{itemize}
\end{limitations}

\section{Implications}

\begin{recommendations}[Research Implications]
\begin{enumerate}
    \item Replicate in diverse populations
    \item Investigate mechanisms of change
    \item Test implementation strategies
\end{enumerate}
\end{recommendations}

\begin{recommendations}[Practice Implications]
\begin{enumerate}
    \item Adopt the intervention in [settings]
    \item Train providers using standardized protocols
    \item Monitor fidelity and outcomes
\end{enumerate}
\end{recommendations}
```

---

## Checklist: Professional Report Quality

Before finalizing your report, verify:

### Formatting
- [ ] Using `scientific_report.sty` package
- [ ] Compiled with XeLaTeX or LuaLaTeX
- [ ] Helvetica font rendering correctly
- [ ] Colors displaying properly

### Content Organization
- [ ] Executive summary present and complete
- [ ] Key findings highlighted in boxes
- [ ] Methods clearly described
- [ ] Results properly formatted with statistics
- [ ] Limitations acknowledged
- [ ] Recommendations are specific and actionable

### Tables
- [ ] All tables have captions and labels
- [ ] Alternating row colors applied
- [ ] Significance indicators explained
- [ ] Numbers formatted consistently

### Figures
- [ ] All figures have captions and labels
- [ ] Sources attributed where appropriate
- [ ] Resolution sufficient for printing (300 DPI)
- [ ] Referenced in text

### Statistical Reporting
- [ ] P-values reported appropriately
- [ ] Effect sizes included
- [ ] Confidence intervals where relevant
- [ ] Sample sizes stated

### Professional Appearance
- [ ] Consistent formatting throughout
- [ ] No orphaned headers or widows
- [ ] Page breaks at appropriate locations
- [ ] References complete and formatted

---

## Resources

### Files in This Skill

- `assets/scientific_report.sty` - The LaTeX style package
- `assets/scientific_report_template.tex` - Complete report template
- `assets/REPORT_FORMATTING_GUIDE.md` - Quick reference guide

### Related Skills

- `venue-templates` - For journal manuscripts and conference papers
- `scientific-schematics` - For generating diagrams and figures
- `generate-image` - For creating illustrations and graphics

### External Resources

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) - General LaTeX reference
- [Booktabs Package Documentation](https://ctan.org/pkg/booktabs) - Professional table styling
- [tcolorbox Package Documentation](https://ctan.org/pkg/tcolorbox) - Colored box environments

---

## Reference: Reporting_Guidelines

# Reporting Guidelines for Scientific Studies

## Overview

Reporting guidelines are evidence-based recommendations for what information should be included when reporting specific types of research studies. They provide checklists and flow diagrams to ensure complete, accurate, and transparent reporting, which is essential for readers to assess study validity and for other researchers to replicate the work.

The EQUATOR Network (Enhancing the QUAlity and Transparency Of health Research) maintains a comprehensive library of reporting guidelines. Using appropriate reporting guidelines improves manuscript quality and increases the likelihood of publication acceptance.

## Why Use Reporting Guidelines?

### Benefits

**For authors:**
- Ensures nothing important is forgotten
- Increases acceptance rates
- Improves manuscript organization
- Reduces reviewer requests for additional information

**For readers and reviewers:**
- Enables critical appraisal of study validity
- Facilitates systematic reviews and meta-analyses
- Improves understanding of what was actually done

**For science:**
- Enhances reproducibility
- Reduces research waste
- Improves transparency
- Enables better evidence synthesis

### When to Use

- **During study design**: Many guidelines include protocol versions (e.g., SPIRIT for trial protocols)
- **During manuscript drafting**: Use checklist to ensure all items are covered
- **Before submission**: Verify adherence and often submit checklist with manuscript
- **Many journals require**: Reporting guideline checklists as part of submission

## Major Reporting Guidelines by Study Type

### CONSORT - Randomized Controlled Trials

**Full name:** Consolidated Standards of Reporting Trials

**When to use:** Any randomized controlled trial (RCT), including pilot and feasibility trials

**Latest version:** CONSORT 2010 (updated statement)

**Key components:**
- **Checklist**: 25 items covering title, abstract, introduction, methods, results, discussion
- **Flow diagram**: Participant flow through enrollment, allocation, follow-up, and analysis

**Main checklist items:**
1. Title identifies study as randomized trial
2. Structured abstract
3. Scientific background and rationale
4. Specific objectives and hypotheses
5. Trial design description (parallel, crossover, factorial, etc.)
6. Eligibility criteria for participants
7. Settings and locations of data collection
8. Interventions described in sufficient detail for replication
9. Primary and secondary outcomes defined
10. Sample size determination and power calculation
11. Randomization sequence generation
12. Allocation concealment mechanism
13. Blinding implementation
14. Statistical methods
15. Participant flow with reasons for dropouts
16. Recruitment dates and follow-up dates
17. Baseline characteristics table
18. Analysis results for each outcome
19. Harms and adverse events
20. Trial limitations
21. Generalizability
22. Interpretation consistent with results
23. Trial registration number
24. Full protocol access
25. Funding sources

**Extensions for specific designs:**
- CONSORT for cluster randomized trials
- CONSORT for non-inferiority and equivalence trials
- CONSORT for pragmatic trials
- CONSORT for crossover trials
- CONSORT for N-of-1 trials
- CONSORT for stepped wedge designs

**Where to access:** http://www.consort-statement.org/

### STROBE - Observational Studies

**Full name:** Strengthening the Reporting of Observational Studies in Epidemiology

**When to use:** Cohort studies, case-control studies, and cross-sectional studies

**Latest version:** STROBE 2007 (widely adopted standard)

**Key study designs covered:**
- **Cohort**: Follow exposed and unexposed groups forward in time
- **Case-control**: Compare exposure history between cases and controls
- **Cross-sectional**: Measure exposure and outcome simultaneously

**Main checklist items (22 items):**
1. Title and abstract indicate study design
2. Background and rationale
3. Objectives
4. Study design with rationale
5. Setting, locations, and dates
6. Eligibility criteria and selection methods
7. Variables clearly defined (outcomes, exposures, confounders)
8. Data sources and measurement methods
9. Bias management strategies
10. Study size justification
11. Handling of quantitative variables
12. Statistical methods including confounding and interactions
13. Sensitivity analyses
14. Participant flow with reasons for non-participation
15. Descriptive data including follow-up time
16. Outcome data
17. Main results with unadjusted and adjusted estimates
18. Other analyses (subgroups, sensitivity analyses)
19. Key results summary
20. Limitations with potential bias discussion
21. Interpretation and generalizability
22. Funding sources and role

**Extensions:**
- STROBE-ME (Molecular Epidemiology)
- RECORD (Routinely collected health data)
- STROBE-RDS (Respondent-driven sampling)

**Where to access:** https://www.strobe-statement.org/

### PRISMA - Systematic Reviews and Meta-Analyses

**Full name:** Preferred Reporting Items for Systematic Reviews and Meta-Analyses

**When to use:** Systematic reviews with or without meta-analysis

**Latest version:** PRISMA 2020 (significant update)

**Key components:**
- **Checklist**: 27 items covering all sections
- **Flow diagram**: Study selection process

**Main sections:**
1. **Title**: Identify as systematic review/meta-analysis
2. **Abstract**: Structured summary
3. **Introduction**: Rationale and objectives
4. **Methods**:
   - Eligibility criteria
   - Information sources (databases, dates)
   - Search strategy (full strategy for at least one database)
   - Selection process
   - Data collection process
   - Data items extracted
   - Risk of bias assessment
   - Effect measures
   - Synthesis methods
   - Reporting bias assessment
   - Certainty assessment (e.g., GRADE)
5. **Results**:
   - Study selection flow diagram
   - Study characteristics
   - Risk of bias assessment results
   - Synthesis results (meta-analysis if applicable)
   - Reporting biases
   - Certainty of evidence
6. **Discussion**:
   - Limitations
   - Interpretation
   - Implications

**Extensions:**
- PRISMA for Abstracts
- PRISMA for Protocols (PRISMA-P)
- PRISMA for Network Meta-Analyses
- PRISMA for Scoping Reviews (PRISMA-ScR)
- PRISMA for Individual Patient Data
- PRISMA for Diagnostic Test Accuracy
- PRISMA for Equity-focused reviews

**Where to access:** http://www.prisma-statement.org/

### SPIRIT - Study Protocols for Clinical Trials

**Full name:** Standard Protocol Items: Recommendations for Interventional Trials

**When to use:** Protocols for randomized trials and other planned intervention studies

**Latest version:** SPIRIT 2013

**Purpose:** Ensure trial protocols contain complete descriptions before trial begins

**Main checklist items (33 items):**
- Administrative information (title, trial registration, funding)
- Introduction (background, rationale, objectives)
- Methods: Trial design
  - Study setting
  - Eligibility criteria
  - Interventions in detail
  - Outcomes (primary and secondary)
  - Participant timeline
  - Sample size calculation
  - Recruitment strategy
  - Allocation and randomization
  - Blinding
  - Data collection methods
  - Data management
  - Statistical methods
  - Monitoring (data monitoring committee)
  - Harms reporting
  - Auditing
- Ethics and dissemination
  - Ethics approval
  - Consent procedures
  - Confidentiality
  - Dissemination plans

**Where to access:** https://www.spirit-statement.org/

### STARD - Diagnostic Accuracy Studies

**Full name:** Standards for Reporting of Diagnostic Accuracy Studies

**When to use:** Studies evaluating diagnostic test accuracy

**Latest version:** STARD 2015

**Main checklist items (30 items):**
1. Study design identification
2. Background information and objectives
3. Study design description
4. Participant selection criteria and recruitment
5. Data collection methods
6. Index test description and execution
7. Reference standard description
8. Rationale for choosing reference standard
9. Test result definition and cutoffs
10. Flow of participants with timing
11. Baseline demographic and clinical characteristics
12. Cross-tabulation of index test results by reference standard
13. Estimates of diagnostic accuracy with confidence intervals
14. Handling of indeterminate results
15. Adverse events from testing

**Flow diagram:** Shows participant flow and test results

**Where to access:** https://www.equator-network.org/reporting-guidelines/stard/

### TRIPOD - Prediction Model Studies

**Full name:** Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis

**When to use:** Studies developing, validating, or updating prediction models

**Latest version:** TRIPOD 2015

**Types of studies:**
- Model development only
- Model development with validation
- External validation of existing model
- Model update

**Main checklist items (22 items):**
1. Title identifies study as prediction model study
2. Abstract summarizes key elements
3. Background and objectives
4. Data source and participants
5. Outcome definition
6. Predictors (candidate and selected)
7. Sample size justification
8. Missing data handling
9. Model building procedure
10. Model specification (equation or algorithm)
11. Model performance measures
12. Risk groups if used
13. Participant flow diagram
14. Model development results
15. Model performance
16. Model updating if applicable

**Where to access:** https://www.tripod-statement.org/

### ARRIVE - Animal Research

**Full name:** Animal Research: Reporting of In Vivo Experiments

**When to use:** All in vivo animal studies

**Latest version:** ARRIVE 2.0 (2020 update)

**Two sets of items:**

**ARRIVE Essential 10** (minimum requirements):
1. Study design
2. Sample size calculation
3. Inclusion and exclusion criteria
4. Randomization
5. Blinding
6. Outcome measures
7. Statistical methods
8. Experimental animals (species, strain, sex, age)
9. Experimental procedures
10. Results and interpretation

**ARRIVE Recommended Set** (additional items for full reporting):
- Abstract, background, objectives
- Ethics statement
- Housing and husbandry
- Animal care and monitoring
- Interpretation and generalizability
- Protocol registration
- Data access

**Where to access:** https://arriveguidelines.org/

### CARE - Case Reports

**Full name:** CAse REport Guidelines

**When to use:** Case reports and case series

**Latest version:** CARE 2013

**Main checklist items (13 items):**
1. Title with "case report"
2. Abstract summarizing case
3. Introduction with case background
4. Patient information (demographics, primary concern)
5. Clinical findings
6. Timeline of events
7. Diagnostic assessment
8. Therapeutic intervention
9. Follow-up and outcomes
10. Discussion with strengths and limitations
11. Patient perspective
12. Informed consent

**Where to access:** https://www.care-statement.org/

### SQUIRE - Quality Improvement Studies

**Full name:** Standards for QUality Improvement Reporting Excellence

**When to use:** Healthcare quality improvement reports

**Latest version:** SQUIRE 2.0 (2015)

**Main sections (18 items):**
1. Title and abstract
2. Introduction (problem description, available knowledge, rationale, objectives)
3. Methods (context, intervention, study design, measures, analysis, ethical review)
4. Results (intervention, outcomes)
5. Discussion (summary, interpretation, limitations, conclusions)
6. Other information (funding)

**Where to access:** http://www.squire-statement.org/

### CHEERS - Economic Evaluations

**Full name:** Consolidated Health Economic Evaluation Reporting Standards

**When to use:** Health economic evaluations

**Latest version:** CHEERS 2022 (major update from 2013)

**Main checklist items (28 items):**
1. Title identification as economic evaluation
2. Abstract
3. Background and objectives
4. Target population and subgroups
5. Setting and location
6. Study perspective
7. Comparators
8. Time horizon
9. Discount rate
10. Selection of outcomes
11. Measurement of effectiveness
12. Measurement and valuation of costs
13. Currency and price adjustments
14. Choice of model
15. Assumptions
16. Analytical methods

**Where to access:** https://www.equator-network.org/reporting-guidelines/cheers/

### SRQR - Qualitative Research

**Full name:** Standards for Reporting Qualitative Research

**When to use:** Qualitative and mixed methods research

**Latest version:** SRQR 2014

**Main sections:**
- Title and abstract
- Introduction (problem formulation, purpose)
- Methods (qualitative approach, researcher characteristics, context, sampling strategy, ethical issues, data collection, data analysis, trustworthiness)
- Results (synthesis and interpretation, links to empirical data)
- Discussion (limitations, implications)

**Alternative:** COREQ (Consolidated criteria for reporting qualitative research) for interviews and focus groups

**Where to access:** https://www.equator-network.org/reporting-guidelines/srqr/

## How to Use Reporting Guidelines

### During Study Planning

1. **Identify relevant guideline** based on study design
2. **Review checklist items** that require planning (e.g., randomization, blinding)
3. **Design study** to ensure all required elements will be captured
4. **Consider protocol guidelines** (e.g., SPIRIT for trials)

### During Manuscript Drafting

1. **Download checklist** from guideline website
2. **Work through each item** systematically
3. **Note where each item is addressed** in manuscript (page/line numbers)
4. **Revise manuscript** to include missing items
5. **Use flow diagrams** as appropriate

### Before Submission

1. **Complete formal checklist** with page numbers
2. **Review all items** are adequately addressed
3. **Include checklist** with submission if journal requires
4. **Note guideline adherence** in cover letter or methods

### Example Checklist Entry

```
Item 7: Eligibility criteria for participants, and the settings and locations where the data were collected
Page 6, lines 112-125: "Participants were community-dwelling adults aged 60-85 years with mild cognitive impairment (MCI) as defined by Petersen criteria. Exclusion criteria included dementia diagnosis, major psychiatric disorders, or unstable medical conditions. Recruitment occurred from three memory clinics in Boston, MA, between January 2022 and December 2023."
```

## Finding the Right Guideline

### EQUATOR Network Search

**Website:** https://www.equator-network.org/

**How to use:**
1. Select your study design from the wizard
2. Browse by health research category
3. Search for specific keywords
4. Filter by guideline status (development stage)

### By Study Design

| If your study is a... | Use this guideline |
|----------------------|-------------------|
| Randomized controlled trial | CONSORT |
| Cohort, case-control, or cross-sectional study | STROBE |
| Systematic review or meta-analysis | PRISMA |
| Protocol for a trial | SPIRIT |
| Diagnostic accuracy study | STARD |
| Prediction model study | TRIPOD |
| Animal study | ARRIVE |
| Case report | CARE |
| Quality improvement study | SQUIRE |
| Economic evaluation | CHEERS |
| Qualitative research | SRQR or COREQ |

### Multiple Guidelines

**Some studies may require multiple guidelines:**

**Example 1:** Pilot RCT with qualitative component
- CONSORT for quantitative arm
- SRQR for qualitative component

**Example 2:** Systematic review of diagnostic tests
- PRISMA for review methods
- STARD considerations for included studies

## Extensions and Adaptations

Many reporting guidelines have extensions for specific contexts:

### CONSORT Extensions (examples)

- **CONSORT for Abstracts**: Structured abstracts for RCT reports
- **CONSORT for Harms**: Reporting adverse events
- **CONSORT-EHEALTH**: eHealth interventions
- **CONSORT-SPI**: Social and psychological interventions

### PRISMA Extensions (examples)

- **PRISMA-P**: Protocols for systematic reviews
- **PRISMA for Abstracts**: Conference abstracts
- **PRISMA-NMA**: Network meta-analyses
- **PRISMA-IPD**: Individual patient data reviews
- **PRISMA-S**: Search strategies
- **PRISMA-DTA**: Diagnostic test accuracy reviews

### STROBE Extensions (examples)

- **STROBE-ME**: Molecular epidemiology
- **RECORD**: Routinely collected health data

## Creating Flow Diagrams

### CONSORT Flow Diagram

**Four stages:**
1. **Enrollment**: Assessed for eligibility
2. **Allocation**: Randomly assigned to groups
3. **Follow-up**: Received intervention, lost to follow-up
4. **Analysis**: Included in analysis

**Example:**
```
Assessed for eligibility (n=250)
    ↓
Excluded (n=50)
  • Did not meet criteria (n=30)
  • Declined to participate (n=15)
  • Other reasons (n=5)
    ↓
Randomized (n=200)
    ├─────────────────┬─────────────────┐
    ↓                 ↓                 ↓
Allocated to       Allocated to      Allocated to
Intervention A     Intervention B     Control
(n=67)            (n=66)            (n=67)
    ↓                 ↓                 ↓
Lost to follow-up  Lost to follow-up  Lost to follow-up
(n=3)             (n=5)             (n=2)
    ↓                 ↓                 ↓
Analyzed          Analyzed          Analyzed
(n=64)            (n=61)            (n=65)
```

### PRISMA Flow Diagram

**Stages:**
1. **Identification**: Records from databases and registers
2. **Screening**: Records screened, excluded
3. **Included**: Studies included in review and synthesis

**New features in PRISMA 2020:**
- Separate tracking for database and register searches
- Tracking of duplicate removal
- Clear distinction between reports and studies

## Common Mistakes and How to Avoid Them

### Mistake 1: Not Using Guidelines at All

**Impact:** Missing critical information, lower chance of acceptance

**Solution:** Identify and use appropriate guideline from study planning stage

### Mistake 2: Using Guidelines Only After Manuscript is Complete

**Impact:** May realize key data were not collected or documented

**Solution:** Review guidelines during study design and data collection

### Mistake 3: Incomplete Checklist Completion

**Impact:** Missed items remain unreported

**Solution:** Systematically address every single checklist item

### Mistake 4: Using Outdated Guidelines

**Impact:** Missing recent improvements in reporting standards

**Solution:** Always check for latest version on official guideline website

### Mistake 5: Using Wrong Guideline for Study Design

**Impact:** Important design-specific elements not reported

**Solution:** Carefully match study design to appropriate guideline

### Mistake 6: Not Submitting Checklist When Required

**Impact:** Editorial desk rejection or delays

**Solution:** Check journal submission guidelines and include checklist

### Mistake 7: Generic Reporting Without Specificity

**Impact:** Insufficient detail for replication or appraisal

**Solution:** Provide specific, detailed information for each item

## Journal Requirements

### Many Journals Now Require:

1. **Statement of adherence** to reporting guidelines in Methods
2. **Completed checklist** uploaded as supplementary file
3. **Page/line numbers** on checklist indicating where items are addressed
4. **Flow diagrams** as figures in manuscript

### Example Methods Statement:

```
"This study is reported in accordance with the Strengthening the Reporting of
Observational Studies in Epidemiology (STROBE) statement. A completed STROBE
checklist is provided as Supplementary File 1."
```

### Journals with Strong Requirements:

- PLOS journals (require checklists for specific designs)
- BMJ (requires CONSORT, PRISMA, and others)
- The Lancet (requires adherence statements)
- JAMA and JAMA Network journals (require checklists)
- Nature portfolio journals (encourage guidelines)

## Resources

### Official Guideline Websites

- **EQUATOR Network**: https://www.equator-network.org/
- **CONSORT**: http://www.consort-statement.org/
- **STROBE**: https://www.strobe-statement.org/
- **PRISMA**: http://www.prisma-statement.org/
- **SPIRIT**: https://www.spirit-statement.org/
- **ARRIVE**: https://arriveguidelines.org/
- **CARE**: https://www.care-statement.org/

### Training Materials

- EQUATOR Network provides webinars and training resources
- Many guidelines have explanatory papers published in medical journals
- Universities often provide workshops on reporting guidelines

### Software Tools

- **Some reference managers** can insert reporting guideline citations
- **Covidence, RevMan** for systematic review reporting
- **PRISMA flow diagram generator**: http://prisma.thetacollaborative.ca/

## Checklist: Using Reporting Guidelines

**Before starting your study:**
- [ ] Identified appropriate reporting guideline(s)
- [ ] Reviewed checklist items requiring prospective planning
- [ ] Designed study to capture all required elements
- [ ] Registered protocol if applicable

**During manuscript drafting:**
- [ ] Downloaded latest version of guideline checklist
- [ ] Systematically addressed each checklist item
- [ ] Created required flow diagram
- [ ] Noted where each item is addressed (page/line)

**Before submission:**
- [ ] Completed formal checklist with page numbers
- [ ] Verified all items adequately addressed
- [ ] Included adherence statement in Methods
- [ ] Prepared checklist as supplementary file if required
- [ ] Checked journal-specific requirements
- [ ] Mentioned guideline adherence in cover letter

## Venue-Specific Reporting Requirements

### Reporting Standards by Venue Type

| Venue Type | Guideline Use | Transparency Requirements |
|-----------|--------------|---------------------------|
| **Medical journals** | Mandatory (CONSORT, STROBE, etc.) | Checklist required at submission |
| **PLOS/BMC** | Mandatory for study types | Checklist uploaded as supplement |
| **Nature/Science** | Recommended | Methods completeness emphasized |
| **ML conferences** | No formal guidelines | Reproducibility details required |

### ML Conference Reporting Standards

**NeurIPS/ICML/ICLR reproducibility requirements:**
- **Datasets**: Names, versions, access methods, preprocessing
- **Code**: Availability statement; GitHub common
- **Hyperparameters**: All settings reported (learning rate, batch size, etc.)
- **Seeds**: Random seeds for reproducibility
- **Computational resources**: GPUs used, training time
- **Statistical significance**: Error bars, confidence intervals, multiple runs
- **Broader Impact** statement (NeurIPS): Societal implications

**What to include (typically in appendix):**
- Complete hyperparameter settings
- Training details and convergence criteria
- Hardware specifications
- Software versions (PyTorch 2.0, etc.)
- Dataset splits and any preprocessing
- Evaluation metrics and protocols

### Enforcement and Evaluation

**What gets checked:**
- **Medical journals**: Checklist uploaded; adherence statement in Methods; systematic completeness
- **PLOS/BMC**: Mandatory checklists for certain designs; reproducibility emphasized
- **High-impact**: Methods sufficiency for replication (checklist often not required)
- **ML conferences**: Reproducibility checklist (NeurIPS); code availability increasingly expected

**Common issues leading to rejection:**
- Missing required checklists (medical journals)
- Insufficient methods detail for reproduction
- Missing key information (randomization, blinding, power calculation)
- No data/code availability statement when required

**Methods statement examples:**

**Journal (STROBE):**
```
This study followed STROBE reporting guidelines. Checklist provided in Supplement 1.
```

**ML conference (reproducibility):**
```
Code available at github.com/user/project. All hyperparameters in Appendix A.
Training used 4×A100 GPUs (~20 hours). Seeds: {42, 123, 456}.
```

### Pre-Submission Reporting Checklist

**For clinical trials (medical journals):**
- [ ] CONSORT checklist complete with page numbers
- [ ] Trial registration number in abstract and methods
- [ ] CONSORT flow diagram included
- [ ] Statistical analysis plan described
- [ ] Adherence statement in Methods

**For observational studies (medical/epidemiology):**
- [ ] STROBE checklist complete
- [ ] Study design clearly stated
- [ ] Statistical methods detailed
- [ ] Confounders addressed
- [ ] Adherence statement in Methods

**For systematic reviews:**
- [ ] PRISMA checklist complete
- [ ] PRISMA flow diagram included
- [ ] Protocol registered (PROSPERO)
- [ ] Search strategy documented
- [ ] Risk of bias assessment included

**For ML conference papers:**
- [ ] All datasets named with versions
- [ ] Code availability stated (GitHub link if available)
- [ ] Hyperparameters listed (appendix acceptable)
- [ ] Random seeds reported
- [ ] Computational resources specified
- [ ] Error bars/confidence intervals shown
- [ ] Broader Impact statement (if required)

---

## Reference: Writing_Principles

# Scientific Writing Principles

## Overview

Effective scientific writing requires mastering fundamental principles that ensure clarity, precision, and impact. Unlike creative or narrative writing, scientific writing prioritizes accuracy, conciseness, and objectivity. This guide covers the core principles that distinguish good scientific writing from poor writing and provides practical strategies for improvement.

## The Three Pillars of Scientific Writing

### 1. Clarity

**Definition:** Writing that is immediately understandable to the intended audience without ambiguity or confusion.

**Why it matters:** Science is complex enough without unclear writing adding confusion. Readers should focus on understanding the science, not deciphering the prose.

#### Strategies for Clarity

**Use precise, unambiguous language:**
```
Poor: "The drug seemed to help quite a few patients."
Better: "The drug reduced symptoms in 68% (32/47) of patients."
```

**Define technical terms at first use:**
```
"We measured brain-derived neurotrophic factor (BDNF), a protein involved in
neuronal survival and plasticity."
```

**Maintain logical flow within and between paragraphs:**
- Each paragraph should have one main idea
- Topic sentence introduces the paragraph's focus
- Supporting sentences develop that focus
- Transition sentences connect paragraphs

**Use active voice when it improves clarity:**
```
Passive (less clear): "The samples were analyzed by the researchers."
Active (clearer): "Researchers analyzed the samples."
```

However, passive voice is acceptable and often preferred in Methods when the action is more important than the actor:
```
"Blood samples were collected at baseline and after 6 weeks."
```

**Break up long, complex sentences:**
```
Poor: "The results of our study, which involved 200 participants recruited from
three hospitals and followed for 12 months with assessments every 4 weeks using
validated questionnaires, showed significant improvements in the intervention
group."

Better: "Our study involved 200 participants recruited from three hospitals.
Participants were followed for 12 months with assessments every 4 weeks using
validated questionnaires. The intervention group showed significant improvements."
```

**Use specific verbs:**
```
Weak: "The study looked at depression in adolescents."
Stronger: "The study examined factors contributing to depression in adolescents."
```

#### Common Clarity Problems

**Ambiguous pronouns:**
```
Poor: "Group A received the drug and Group B received placebo. They showed
improvement."
(Who is "they"?)

Better: "Group A received the drug and Group B received placebo. The drug-treated
group showed improvement."
```

**Misplaced modifiers:**
```
Poor: "We measured blood pressure in patients using an automated monitor."
(Are the patients using the monitor, or are we?)

Better: "Using an automated monitor, we measured blood pressure in patients."
```

**Unclear referents:**
```
Poor: "The increase in expression was accompanied by decreased proliferation, which
was unexpected."
(What was unexpected—the decrease, the accompaniment, or both?)

Better: "The increase in expression was accompanied by decreased proliferation.
This inverse relationship was unexpected."
```

### 2. Conciseness

**Definition:** Expressing ideas in the fewest words necessary without sacrificing clarity or completeness.

**Why it matters:** Concise writing respects readers' time. Every unnecessary word is a missed opportunity for clarity and impact. As the principle states: "We value concise writing because we value time."

#### Strategies for Conciseness

**Eliminate redundant words and phrases:**

| Wordy | Concise |
|-------|---------|
| "due to the fact that" | "because" |
| "in order to" | "to" |
| "it is important to note that" | [delete] |
| "a total of 50 participants" | "50 participants" |
| "completely eliminate" | "eliminate" |
| "has been shown to be" | "is" |
| "in the event that" | "if" |
| "at the present time" | "now" or "currently" |
| "conduct an investigation into" | "investigate" |
| "give consideration to" | "consider" |

**Avoid throat-clearing phrases:**
```
Wordy: "It is interesting to note that the results of our study demonstrate that..."
Concise: "Our results demonstrate that..." or "The results show that..."
```

**Use strong verbs instead of noun+verb combinations:**

| Wordy | Concise |
|-------|---------|
| "make a decision" | "decide" |
| "perform an analysis" | "analyze" |
| "conduct a study" | "study" or "studied" |
| "make an assessment" | "assess" |
| "provide information about" | "inform" |

**Eliminate unnecessary intensifiers:**
```
Wordy: "The results were very significant."
Concise: "The results were significant." (p-value conveys the degree)
```

**Avoid repeating information unnecessarily:**
```
Redundant: "The results showed that participants in the intervention group, who
received the treatment intervention, had better outcomes."
Concise: "The intervention group had better outcomes."
```

**Favor shorter constructions:**
```
Wordy: "In spite of the fact that the sample size was small..."
Concise: "Although the sample size was small..."
```

#### Acceptable Length vs. Unnecessary Length

**Not all long sentences are bad:**
```
This detailed sentence is fine: "We analyzed blood samples using liquid
chromatography-tandem mass spectrometry (LC-MS/MS) with a Waters Acquity UPLC
system coupled to a Xevo TQ-S mass spectrometer (Waters Corporation, Milford, MA)."

Why? Because each element is necessary information.
```

**The key question:** Can any word be removed without losing meaning or precision? If yes, remove it.

### 3. Accuracy

**Definition:** Precise, correct representation of data, methods, and interpretations.

**Why it matters:** Scientific credibility depends on accuracy. Inaccurate reporting undermines the entire scientific enterprise.

#### Strategies for Accuracy

**Report exact values with appropriate precision:**
```
Poor: "The mean was about 25."
Better: "The mean was 24.7 ± 3.2 (SD)."
```

**Match precision to measurement capability:**
```
Inappropriate: "Mean age was 45.237 years" (implies false precision)
Appropriate: "Mean age was 45.2 years"
```

**Use consistent terminology throughout:**
```
Inconsistent: Introduction calls it "cognitive function," Methods call it "mental
performance," Results call it "intellectual ability."

Consistent: Use "cognitive function" throughout, or define explicitly: "cognitive
function (also termed mental performance)"
```

**Distinguish observations from interpretations:**
```
Observation: "Mean blood pressure decreased from 145 to 132 mmHg (p=0.003)."
Interpretation: "This suggests the intervention effectively lowers blood pressure."
```

**Be specific about uncertainty:**
```
Vague: "There may be some error in these measurements."
Specific: "Measurements have a standard error of ±2.5 mmHg based on instrument
specifications."
```

**Use correct statistical language:**
```
Incorrect: "The correlation was highly significant (p=0.03)."
Correct: "The correlation was statistically significant (p=0.03)."
(p=0.03 is not "highly" significant; that's reserved for p<0.001)
```

**Verify all numbers:**
- Check that numbers in text match tables/figures
- Verify that n values sum correctly
- Confirm percentages are correctly calculated
- Double-check all statistics

#### Common Accuracy Problems

**Overgeneralization:**
```
Poor: "Exercise prevents depression."
Better: "In our sample, participants randomized to the exercise intervention showed
fewer depressive symptoms than controls (mean difference 3.2 points on the BDI-II,
95% CI: 1.5-4.9, p<0.001)."
```

**Unwarranted causal claims:**
```
Poor (from observational study): "Vitamin D supplementation reduces cancer risk."
Better: "Vitamin D levels were inversely associated with cancer incidence in this
cohort (HR=0.82, 95% CI: 0.71-0.95)."
```

**Imprecise numerical descriptions:**
```
Vague: "Many participants dropped out."
Precise: "15/50 (30%) participants withdrew before study completion."
```

## Additional Key Principles

### 4. Objectivity

**Definition:** Presenting information impartially without bias, exaggeration, or unsupported opinion.

**Strategies:**

**Present results without bias:**
```
Biased: "As expected, our superior method performed better."
Objective: "Method A showed higher accuracy than Method B (87% vs. 76%, p=0.02)."
```

**Acknowledge conflicting evidence:**
```
"Our findings contrast with Smith et al. (2022), who reported no significant effect.
This discrepancy may result from differences in intervention intensity or population
characteristics."
```

**Avoid emotional or evaluative language:**
```
Subjective: "The results were disappointing and concerning."
Objective: "The intervention did not significantly reduce symptoms (p=0.42)."
```

**Distinguish fact from speculation:**
```
"The observed decrease in cell viability was accompanied by increased caspase-3
activity, suggesting that apoptosis may be the primary mechanism of cell death."
(Uses "suggesting" and "may be" to indicate interpretation)
```

### 5. Consistency

**Maintain consistency throughout the manuscript:**

**Terminology:**
- Use the same term for the same concept (not synonyms for variety)
- Define abbreviations at first use and use consistently thereafter
- Use standard nomenclature for genes, proteins, chemicals

**Notation:**
- Statistical notation (p-value format, CI presentation)
- Units of measurement
- Number formatting (decimal places)

**Tense:**
- Past tense for your specific study actions
- Present tense for established facts
- See detailed tense guide in IMRAD structure reference

**Style:**
- Follow journal guidelines consistently
- Citation format
- Heading capitalization
- Number vs. word for numerals

### 6. Logical Organization

**Create a clear "red thread" through the manuscript:**

**Paragraph structure:**
1. Topic sentence (main idea)
2. Supporting sentences (evidence, explanation)
3. Concluding/transition sentence (link to next idea)

**Section flow:**
- Each section builds logically on the previous
- Questions raised in Introduction are answered in Results
- Findings presented in Results are interpreted in Discussion

**Signposting:**
```
"First, we examined..."
"Next, we investigated..."
"Finally, we assessed..."
```

**Parallelism:**
```
Not parallel: "Aims were to (1) measure blood pressure, (2) assessment of
cognitive function, and (3) we wanted to evaluate mood."

Parallel: "Aims were to (1) measure blood pressure, (2) assess cognitive
function, and (3) evaluate mood."
```

## Verb Tense in Scientific Writing

### General Guidelines

**Present tense** for:
- Established facts and general truths
  - "DNA is composed of nucleotides."
- Conclusions you are drawing
  - "These findings suggest that..."
- Referring to figures and tables
  - "Figure 1 shows the distribution..."

**Past tense** for:
- Specific findings from completed research (yours and others')
  - "Smith et al. (2022) found that..."
  - "We observed a significant decrease..."
- Methods you performed
  - "Participants completed questionnaires at baseline."

**Present perfect** for:
- Recent developments with current relevance
  - "Recent studies have demonstrated..."
- Research area background
  - "Several approaches have been proposed..."

### Section-Specific Tense

| Section | Primary Tense | Examples |
|---------|---------------|----------|
| **Abstract - Background** | Present or present perfect | "Depression affects millions" / "Research has shown..." |
| **Abstract - Methods** | Past | "We recruited 100 participants" |
| **Abstract - Results** | Past | "The intervention reduced symptoms" |
| **Abstract - Conclusions** | Present | "These findings suggest..." |
| **Introduction - Background** | Present (facts), present perfect (research) | "Exercise is beneficial" / "Studies have shown..." |
| **Introduction - Gap** | Present or present perfect | "However, little is known..." |
| **Introduction - This study** | Past or present | "We investigated..." / "This study investigates..." |
| **Methods** | Past | "We collected samples..." |
| **Results** | Past | "Mean age was 45 years" |
| **Discussion - Your findings** | Past | "We found that..." |
| **Discussion - Interpretation** | Present | "This suggests..." |
| **Discussion - Prior work** | Past or present | "Smith found..." / "Previous work demonstrates..." |

## Common Writing Pitfalls

### 1. Jargon Overload

**Problem:** Excessive use of technical terms without definition

**Example:**
```
Poor: "We utilized qRT-PCR to quantify mRNA expression via SYBR-Green-based
fluorescence detection following cDNA synthesis from total RNA using oligo-dT primers."

Better: "We quantified mRNA expression using quantitative reverse transcription PCR
(qRT-PCR). Total RNA was reverse transcribed to complementary DNA (cDNA) using
oligo-dT primers, then amplified with SYBR Green fluorescent detection."
```

### 2. Nominalization

**Problem:** Turning verbs into nouns, making writing heavy and indirect

**Examples:**

| Nominalized | Direct |
|-------------|--------|
| "give consideration to" | "consider" |
| "make an assumption" | "assume" |
| "perform an investigation" | "investigate" |
| "conduct an examination" | "examine" |
| "achieve a reduction" | "reduce" |

### 3. Hedging Excessively or Insufficiently

**Excessive hedging** (sounds uncertain):
```
"It could perhaps be possible that the intervention might possibly have some effect
on symptoms under certain conditions."
```

**Insufficient hedging** (overstates conclusions):
```
"The intervention cures depression."
```

**Appropriate hedging:**
```
"The intervention significantly reduced depressive symptoms in this sample,
suggesting it may be effective for treating mild to moderate depression."
```

**Hedging words to use appropriately:**
- Suggests, indicates, implies (not proves, demonstrates for correlational data)
- May, might, could (possibilities)
- Appears to, seems to (observations needing confirmation)
- Likely, probably, possibly (degrees of certainty)

### 4. Anthropomorphism

**Problem:** Attributing human characteristics to non-human entities

**Examples:**

| Anthropomorphic | Scientific |
|----------------|-----------|
| "The study wanted to examine..." | "We aimed to examine..." or "The study examined..." |
| "The data suggest they want..." | "The data suggest that..." |
| "This paper will prove..." | "This paper demonstrates..." |
| "Table 1 tells us..." | "Table 1 shows..." |

### 5. Abbreviation Abuse

**Problems:**
- Too many abbreviations burden the reader
- Abbreviating terms used only once or twice
- Not defining abbreviations at first use

**Guidelines:**
- Only abbreviate terms used ≥3-4 times
- Define at first use in abstract (if used in abstract)
- Define at first use in main text
- Don't abbreviate in title
- Limit to 3-4 new abbreviations per paper when possible
- Use standard abbreviations (DNA, RNA, HIV, etc.) without definition

**Example:**
```
Poor: "We measured Brain-Derived Neurotrophic Factor (BDNF) at baseline. BDNF
levels were elevated."
(Only used twice, abbreviation unnecessary)

Better: "We measured brain-derived neurotrophic factor at baseline. Levels were
elevated."
```

## Specific Sentence-Level Issues

### Dangling Modifiers

**Problem:**
```
"After incubating for 2 hours, we measured absorbance."
(The sentence suggests "we" were incubated)

Better: "After incubating samples for 2 hours, we measured absorbance."
Or: "After 2-hour incubation, we measured absorbance."
```

### Misplaced Commas

**Common errors:**

**Between subject and verb:**
```
Wrong: "The participants in the intervention group, showed improvement."
Right: "The participants in the intervention group showed improvement."
```

**In compound predicates:**
```
Wrong: "We measured blood pressure, and recorded symptoms."
Right: "We measured blood pressure and recorded symptoms."
(No comma before "and" when it doesn't join independent clauses)
```

### Pronoun Agreement

```
Wrong: "Each participant completed their questionnaire."
Right: "Each participant completed his or her questionnaire."
Or better: "Participants completed their questionnaires."
```

### Subject-Verb Agreement

```
Wrong: "The group of participants were heterogeneous."
Right: "The group of participants was heterogeneous."
(Subject is "group" [singular], not "participants")

But: "The participants were heterogeneous." (Plural subject)
```

## Word Choice

### Commonly Confused Words in Scientific Writing

| Often Misused | Correct Usage |
|---------------|---------------|
| **affect / effect** | Affect (verb): influence; Effect (noun): result; Effect (verb): bring about |
| **among / between** | Among: three or more; Between: two |
| **continual / continuous** | Continual: repeated; Continuous: uninterrupted |
| **data is / data are** | Data are (plural); datum is (singular) |
| **fewer / less** | Fewer: countable items; Less: continuous quantities |
| **i.e. / e.g.** | i.e. (that is): restatement; e.g. (for example): examples |
| **imply / infer** | Imply: suggest; Infer: deduce |
| **parameter / variable** | Parameter: population value; Variable: measured characteristic |
| **principal / principle** | Principal: main; Principle: rule or concept |
| **significant** | Reserve for statistical significance, not importance |
| **that / which** | That: restrictive clause; Which: nonrestrictive clause |

### Words to Avoid or Use Carefully

**Avoid informal language:**
- "a lot of" → "many" or "substantial"
- "got" → "obtained" or "became"
- "showed up" → "appeared" or "was evident"

**Avoid vague quantifiers:**
- "some" → specify how many
- "often" → specify frequency
- "recently" → specify timeframe

**Avoid unnecessary modifiers:**
- "very significant" → "significant" (p-value shows degree)
- "quite large" → "large" or specify size
- "rather interesting" → delete or explain why

## Numbers and Units

### When to Use Numerals vs. Words

**Use numerals for:**
- All numbers ≥10
- Numbers with units (5 mg, 3 mL)
- Statistical values (p=0.03, t=2.14)
- Ages, dates, times
- Scores and scales
- Percentages (15%)

**Use words for:**
- Numbers <10 when not connected to units (five participants)
- Numbers beginning a sentence (spell out or restructure)

**Examples:**
```
"Five participants withdrew" OR "There were 5 withdrawals"
(NOT: "5 participants withdrew")

"We tested 15 samples at 3 time points"
"Mean age was 45 years"
```

### Units and Formatting

**Guidelines:**
- Space between number and unit (5 mg, not 5mg)
- No period after units (mg not mg.)
- Use SI units unless field convention differs
- Be consistent in decimal places
- Use commas for thousands in text (12,500 not 12500)

**Ranges:**
- Use en-dash (–) for ranges: 15–20 mg
- Include unit only after second number: 15–20 mg (not 15 mg–20 mg)

## Paragraph Structure

### Ideal Paragraph Length

**Guidelines:**
- 3-7 sentences typically
- One main idea per paragraph
- Too short (<2 sentences): may indicate idea needs development or combining
- Too long (>10 sentences): may need splitting

### Paragraph Coherence

**Techniques:**

**1. Topic sentence:**
```
"Exercise training improves cardiovascular function through multiple mechanisms.
[Following sentences explain these mechanisms]"
```

**2. Transitional phrases:**
- First, second, third, finally
- Furthermore, moreover, in addition
- However, nevertheless, conversely
- Therefore, thus, consequently
- For example, specifically, particularly

**3. Repetition of key terms:**
```
"...this mechanism of action. This mechanism may explain..."
(Not: "...this mechanism. This process may explain...")
```

**4. Parallel structure:**
```
"Group A received the drug. Group B received placebo. Group C received no treatment."
(Not: "Group A received the drug. Placebo was given to Group B. No treatment was
provided to the third group.")
```

## Revision Checklist

### Content Level

- [ ] Does every sentence add value?
- [ ] Are claims supported by data?
- [ ] Is the logic clear and sound?
- [ ] Are interpretations warranted by results?

### Paragraph Level

- [ ] Does each paragraph have one main idea?
- [ ] Are paragraphs in logical order?
- [ ] Are transitions smooth?
- [ ] Is there a clear "red thread"?

### Sentence Level

- [ ] Are sentences clear and concise?
- [ ] Is sentence structure varied?
- [ ] Are there no dangling modifiers?
- [ ] Do subjects and verbs agree?

### Word Level

- [ ] Is word choice precise?
- [ ] Are technical terms defined?
- [ ] Is terminology consistent?
- [ ] Are abbreviations necessary and defined?
- [ ] Are numbers formatted correctly?

### Grammar and Mechanics

- [ ] Is verb tense correct and consistent?
- [ ] Are commas used correctly?
- [ ] Do pronouns agree with antecedents?
- [ ] Is punctuation correct?
- [ ] Is spelling correct (including technical terms)?

## Tools for Improving Writing

### Grammar and Style Checkers

- **Grammarly**: Grammar, style, clarity
- **ProWritingAid**: In-depth writing analysis
- **Hemingway Editor**: Readability, simplification
- **LanguageTool**: Open-source grammar checker

**Caution:** These tools don't understand scientific writing conventions. Use them as a starting point, not final arbiter.

### Readability Metrics

**Flesch Reading Ease:**
- 60-70: acceptable for scientific papers
- <60: may be too complex

**Caution:** Don't sacrifice precision for readability scores designed for general audiences.

### Peer Review

**Most valuable tool:**
- Ask colleagues to read and provide feedback
- Identify unclear passages
- Check logical flow
- Verify interpretations are warranted

## Additional Resources

### Books on Scientific Writing

- *The Elements of Style* by Strunk & White (classic on clear writing)
- *On Writing Well* by William Zinsser
- *Scientific Writing: A Reader and Writer's Guide* by Jean-Luc Lebrun
- *How to Write a Scientific Paper* by George M. Whitesides
- *Style: Lessons in Clarity and Grace* by Joseph Williams

### Online Resources

- **Academic Phrasebank** (University of Manchester): Common academic phrases
- **Purdue OWL**: Grammar, punctuation, style
- **Nature Masterclasses**: Scientific writing courses
- **WritingCenters**: Many universities provide free online resources

### University Writing Centers

Most research universities offer:
- Individual consultations
- Workshops on scientific writing
- Online resources and handouts
- Support for non-native English speakers

## Venue-Specific Writing Styles

### Four Major Writing Style Categories

1. **Broad-audience accessible** (Nature, Science, PNAS)
2. **Clinical-professional** (NEJM, Lancet, JAMA)
3. **Technical-specialist** (field-specific journals)
4. **ML conference** (NeurIPS, ICML, ICLR, CVPR)

### Writing Style Comparison

| Aspect | Nature/Science | Medical | Specialized | ML Conference |
|--------|---------------|---------|-------------|---------------|
| **Sentence length** | 15-20 words | 12-18 words | 18-25 words | 12-20 words |
| **Vocabulary** | Minimal jargon | Clinical terms | Field-specific | Technical + math |
| **Tone** | Engaging, significant | Conservative | Formal | Direct, contribution-focused |
| **Key phrases** | "Here we show" | "We conducted" | "To elucidate" | "We propose", "Our contributions" |

**ML Conference Style:**

**Characteristics:**
- Direct, technical language with mathematical notation
- Contribution-focused (numbered lists common)
- Assumes ML expertise (CNNs, transformers, SGD, etc.)
- Emphasizes novelty and performance gains
- Pseudocode and equations expected

**Example opening (NeurIPS style):**
```
Vision transformers have achieved state-of-the-art performance on image classification,
but their quadratic complexity limits applicability to high-resolution images. We propose
Efficient-ViT, which reduces complexity to O(n log n) while maintaining accuracy. Our
contributions are: (1) a novel sparse attention mechanism, (2) theoretical analysis
showing preserved expressive power, and (3) empirical validation on ImageNet showing
15% speedup with comparable accuracy.
```
- Problem stated with technical context
- Solution previewed
- Numbered contributions
- Quantitative claims

### Key Writing Differences

| Aspect | Nature/Science | Medical | Specialized | ML Conference |
|--------|---------------|---------|-------------|---------------|
| **Paragraph length** | 3-5 sentences | 5-7 sentences | 6-10 sentences | 4-6 sentences |
| **Math/equations** | Minimize | Rare | Moderate | Essential |
| **Active voice** | Preferred | Mixed | Passive OK | Preferred |
| **Hedging** | Moderate | Conservative | Detailed | Minimal (claim gains) |
| **Figure integration** | Tight | Systematic | Detailed | Dense, in-page |

### Evaluation Focus by Venue

| Venue | Key Evaluation Criteria |
|-------|------------------------|
| **Nature/Science** | Accessible to non-specialists? Broad significance clear? Compelling story? |
| **Medical** | Clinical relevance apparent? Professional tone? Methods adequate? |
| **Specialized** | Technical precision? Field expertise shown? Methods detailed? |
| **ML conferences** | Clear contributions? Claims supported by experiments? Reproducible? |

**Common rejection reasons:**
- Poor writing quality/unclear prose
- Inappropriate style for venue
- Overstated claims
- Methods insufficient for reproduction
- Missing key details (baselines, ablations for ML; statistics for journals)

### Quick Style Adaptation Guide

| From → To | Key Changes |
|-----------|-------------|
| **Journal → ML conference** | Add numbered contributions; include equations/pseudocode; emphasize quantitative gains; condense prose |
| **ML conference → Journal** | Remove contribution numbering; expand motivation; separate Results/Discussion; reduce equations in main text |
| **Specialist → Broad** | Simplify language; emphasize broad implications; explain technical concepts; add context for non-experts |
| **Broad → Specialist** | Add technical detail; use field terminology freely; expand mechanistic discussion; cite field literature |
| **Basic science → Clinical** | Add patient/clinical context; use clinical language; emphasize outcomes/implications; cite clinical evidence |

### Pre-Submission Style Checklist

**All venues:**
- [ ] Writing style matches 3-5 recent papers from venue
- [ ] Sentence length appropriate
- [ ] Technical vocabulary level correct
- [ ] Tone consistent with venue
- [ ] No overstated claims

**ML conferences add:**
- [ ] Contributions clearly numbered in intro
- [ ] Mathematical notation correct and consistent
- [ ] Pseudocode/algorithms included where appropriate
- [ ] Claims quantified (e.g., "15% faster", "2.3% accuracy gain")
- [ ] Limitations acknowledged

## Final Thoughts

Effective scientific writing is a skill developed through practice. Key principles:

1. **Clarity** trumps complexity
2. **Conciseness** respects readers' time
3. **Accuracy** builds credibility
4. **Objectivity** maintains scientific integrity
5. **Consistency** aids comprehension
6. **Logical organization** guides readers
7. **Journal-specific adaptation** maximizes publication success

**Remember:** The goal is not to impress readers with vocabulary or complexity, but to communicate your science clearly and precisely so readers can understand, evaluate, and build upon your work. Adapt your writing style to match your target journal's expectations and audience.
