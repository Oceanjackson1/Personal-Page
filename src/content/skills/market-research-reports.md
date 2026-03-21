---
title: "Market Research Reports"
description: "Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation with scientific-schematics and generate-image, deep integ..."
category: "research"
source: "community"
author: "Community"
tags: ["market", "research", "reports"]
date: 2026-03-20
---

# Market Research Reports

## Overview

Market research reports are comprehensive strategic documents that analyze industries, markets, and competitive landscapes to inform business decisions, investment strategies, and strategic planning. This skill generates **professional-grade reports of 50+ pages** with extensive visual content, modeled after deliverables from top consulting firms like McKinsey, BCG, Bain, Gartner, and Forrester.

**Key Features:**
- **Comprehensive length**: Reports are designed to be 50+ pages with no token constraints
- **Visual-rich content**: 5-6 key diagrams generated at start (more added as needed during writing)
- **Data-driven analysis**: Deep integration with research-lookup for market data
- **Multi-framework approach**: Porter's Five Forces, PESTLE, SWOT, BCG Matrix, TAM/SAM/SOM
- **Professional formatting**: Consulting-firm quality typography, colors, and layout
- **Actionable recommendations**: Strategic focus with implementation roadmaps

**Output Format:** LaTeX with professional styling, compiled to PDF. Uses the `market_research.sty` style package for consistent, professional formatting.

## When to Use This Skill

This skill should be used when:
- Creating comprehensive market analysis for investment decisions
- Developing industry reports for strategic planning
- Analyzing competitive landscapes and market dynamics
- Conducting market sizing exercises (TAM/SAM/SOM)
- Evaluating market entry opportunities
- Preparing due diligence materials for M&A activities
- Creating thought leadership content for industry positioning
- Developing go-to-market strategy documentation
- Analyzing regulatory and policy impacts on markets
- Building business cases for new product launches

## Visual Enhancement Requirements

**CRITICAL: Market research reports should include key visual content.**

Every report should generate **6 essential visuals** at the start, with additional visuals added as needed during writing. Start with the most critical visualizations to establish the report framework.

### Visual Generation Tools

**Use `scientific-schematics` for:**
- Market growth trajectory charts
- TAM/SAM/SOM breakdown diagrams (concentric circles)
- Porter's Five Forces diagrams
- Competitive positioning matrices
- Market segmentation charts
- Value chain diagrams
- Technology roadmaps
- Risk heatmaps
- Strategic prioritization matrices
- Implementation timelines/Gantt charts
- SWOT analysis diagrams
- BCG Growth-Share matrices

```bash
# Example: Generate a TAM/SAM/SOM diagram
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report

# Example: Generate Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: 'Threat of New Entrants' (top), 'Bargaining Power of Suppliers' (left), 'Bargaining Power of Buyers' (right), 'Threat of Substitutes' (bottom). Each box should show High/Medium/Low rating" \
  -o figures/porters_five_forces.png --doc-type report
```

**Use `generate-image` for:**
- Executive summary hero infographics
- Industry/sector conceptual illustrations
- Abstract technology visualizations
- Cover page imagery

```bash
# Example: Generate executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

### Recommended Visuals by Section (Generate as Needed)

| Section | Priority Visuals | Optional Visuals |
|---------|-----------------|------------------|
| Executive Summary | Executive infographic (START) | - |
| Market Size & Growth | Growth trajectory (START), TAM/SAM/SOM (START) | Regional breakdown, segment growth |
| Competitive Landscape | Porter's Five Forces (START), Positioning matrix (START) | Market share chart, strategic groups |
| Risk Analysis | Risk heatmap (START) | Mitigation matrix |
| Strategic Recommendations | Opportunity matrix | Priority framework |
| Implementation Roadmap | Timeline/Gantt | Milestone tracker |
| Investment Thesis | Financial projections | Scenario analysis |

**Start with 6 priority visuals** (marked as START above), then generate additional visuals as specific sections are written and require visual support.

---

## Report Structure (50+ Pages)

### Front Matter (~5 pages)

#### Cover Page (1 page)
- Report title and subtitle
- Hero visualization (generated)
- Date and classification
- Prepared for / Prepared by

#### Table of Contents (1-2 pages)
- Automated from LaTeX
- List of Figures
- List of Tables

#### Executive Summary (2-3 pages)
- **Market Snapshot Box**: Key metrics at a glance
- **Investment Thesis**: 3-5 bullet point summary
- **Key Findings**: Major discoveries and insights
- **Strategic Recommendations**: Top 3-5 actionable recommendations
- **Executive Summary Infographic**: Visual synthesis of report highlights

---

### Core Analysis (~35 pages)

#### Chapter 1: Market Overview & Definition (4-5 pages)

**Content Requirements:**
- Market definition and scope
- Industry ecosystem mapping
- Key stakeholders and their roles
- Market boundaries and adjacencies
- Historical context and evolution

**Required Visuals (2):**
1. Market ecosystem/value chain diagram
2. Industry structure diagram

**Key Data Points:**
- Market definition criteria
- Included/excluded segments
- Geographic scope
- Time horizon for analysis

---

#### Chapter 2: Market Size & Growth Analysis (6-8 pages)

**Content Requirements:**
- Total Addressable Market (TAM) calculation
- Serviceable Addressable Market (SAM) definition
- Serviceable Obtainable Market (SOM) estimation
- Historical growth analysis (5-10 years)
- Growth projections (5-10 years forward)
- Growth drivers and inhibitors
- Regional market breakdown
- Segment-level analysis

**Required Visuals (4):**
1. Market growth trajectory chart (historical + projected)
2. TAM/SAM/SOM concentric circles diagram
3. Regional market breakdown (pie chart or treemap)
4. Segment growth comparison (bar chart)

**Key Data Points:**
- Current market size (with source)
- CAGR (historical and projected)
- Market size by region
- Market size by segment
- Key assumptions for projections

**Data Sources:**
Use `research-lookup` to find:
- Market research reports (Gartner, Forrester, IDC, etc.)
- Industry association data
- Government statistics
- Company financial reports
- Academic studies

---

#### Chapter 3: Industry Drivers & Trends (5-6 pages)

**Content Requirements:**
- Macroeconomic factors
- Technology trends
- Regulatory drivers
- Social and demographic shifts
- Environmental factors
- Industry-specific trends

**Analysis Frameworks:**
- **PESTLE Analysis**: Political, Economic, Social, Technological, Legal, Environmental
- **Trend Impact Assessment**: Likelihood vs Impact matrix

**Required Visuals (3):**
1. Industry trends timeline or radar chart
2. Driver impact matrix
3. PESTLE analysis diagram

**Key Data Points:**
- Top 5-10 growth drivers with quantified impact
- Emerging trends with timeline
- Disruption factors

---

#### Chapter 4: Competitive Landscape (6-8 pages)

**Content Requirements:**
- Market structure analysis
- Major player profiles
- Market share analysis
- Competitive positioning
- Barriers to entry
- Competitive dynamics

**Analysis Frameworks:**
- **Porter's Five Forces**: Comprehensive industry analysis
- **Competitive Positioning Matrix**: 2x2 matrix on key dimensions
- **Strategic Group Mapping**: Cluster competitors by strategy

**Required Visuals (4):**
1. Porter's Five Forces diagram
2. Market share pie chart or bar chart
3. Competitive positioning matrix (2x2)
4. Strategic group map

**Key Data Points:**
- Market share by company (top 10)
- Competitive intensity rating
- Entry barriers assessment
- Supplier/buyer power assessment

---

#### Chapter 5: Customer Analysis & Segmentation (4-5 pages)

**Content Requirements:**
- Customer segment definitions
- Segment size and growth
- Buying behavior analysis
- Customer needs and pain points
- Decision-making process
- Value drivers by segment

**Analysis Frameworks:**
- **Customer Segmentation Matrix**: Size vs Growth
- **Value Proposition Canvas**: Jobs, Pains, Gains
- **Customer Journey Mapping**: Awareness to Advocacy

**Required Visuals (3):**
1. Customer segmentation breakdown (pie/treemap)
2. Segment attractiveness matrix
3. Customer journey or value proposition diagram

**Key Data Points:**
- Segment sizes and percentages
- Growth rates by segment
- Average deal size / revenue per customer
- Customer acquisition cost by segment

---

#### Chapter 6: Technology & Innovation Landscape (4-5 pages)

**Content Requirements:**
- Current technology stack
- Emerging technologies
- Innovation trends
- Technology adoption curves
- R&D investment analysis
- Patent landscape

**Analysis Frameworks:**
- **Technology Readiness Assessment**: TRL levels
- **Hype Cycle Positioning**: Where technologies sit
- **Technology Roadmap**: Evolution over time

**Required Visuals (2):**
1. Technology roadmap diagram
2. Innovation/adoption curve or hype cycle

**Key Data Points:**
- R&D spending in the industry
- Key technology milestones
- Patent filing trends
- Technology adoption rates

---

#### Chapter 7: Regulatory & Policy Environment (3-4 pages)

**Content Requirements:**
- Current regulatory framework
- Key regulatory bodies
- Compliance requirements
- Upcoming regulatory changes
- Policy trends
- Impact assessment

**Required Visuals (1):**
1. Regulatory timeline or framework diagram

**Key Data Points:**
- Key regulations and effective dates
- Compliance costs
- Regulatory risks
- Policy change probability

---

#### Chapter 8: Risk Analysis (3-4 pages)

**Content Requirements:**
- Market risks
- Competitive risks
- Regulatory risks
- Technology risks
- Operational risks
- Financial risks
- Risk mitigation strategies

**Analysis Frameworks:**
- **Risk Heatmap**: Probability vs Impact
- **Risk Register**: Comprehensive risk inventory
- **Mitigation Matrix**: Risk vs Mitigation strategy

**Required Visuals (2):**
1. Risk heatmap (probability vs impact)
2. Risk mitigation matrix

**Key Data Points:**
- Top 10 risks with ratings
- Risk probability scores
- Impact severity scores
- Mitigation cost estimates

---

### Strategic Recommendations (~10 pages)

#### Chapter 9: Strategic Opportunities & Recommendations (4-5 pages)

**Content Requirements:**
- Opportunity identification
- Opportunity sizing
- Strategic options analysis
- Prioritization framework
- Detailed recommendations
- Success factors

**Analysis Frameworks:**
- **Opportunity Attractiveness Matrix**: Attractiveness vs Ability to Win
- **Strategic Options Framework**: Build, Buy, Partner, Ignore
- **Priority Matrix**: Impact vs Effort

**Required Visuals (3):**
1. Opportunity matrix
2. Strategic options framework
3. Priority/recommendation matrix

**Key Data Points:**
- Opportunity sizes
- Investment requirements
- Expected returns
- Timeline to value

---

#### Chapter 10: Implementation Roadmap (3-4 pages)

**Content Requirements:**
- Phased implementation plan
- Key milestones and deliverables
- Resource requirements
- Timeline and sequencing
- Dependencies and critical path
- Governance structure

**Required Visuals (2):**
1. Implementation timeline/Gantt chart
2. Milestone tracker or phase diagram

**Key Data Points:**
- Phase durations
- Resource requirements
- Key milestones with dates
- Budget allocation by phase

---

#### Chapter 11: Investment Thesis & Financial Projections (3-4 pages)

**Content Requirements:**
- Investment summary
- Financial projections
- Scenario analysis
- Return expectations
- Key assumptions
- Sensitivity analysis

**Required Visuals (2):**
1. Financial projection chart (revenue, growth)
2. Scenario analysis comparison

**Key Data Points:**
- Revenue projections (3-5 years)
- CAGR projections
- ROI/IRR expectations
- Key financial assumptions

---

### Back Matter (~5 pages)

#### Appendix A: Methodology & Data Sources (1-2 pages)
- Research methodology
- Data collection approach
- Data sources and citations
- Limitations and assumptions

#### Appendix B: Detailed Market Data Tables (2-3 pages)
- Comprehensive market data tables
- Regional breakdowns
- Segment details
- Historical data series

#### Appendix C: Company Profiles (1-2 pages)
- Brief profiles of key competitors
- Financial highlights
- Strategic focus areas

#### References/Bibliography
- All sources cited
- BibTeX format for LaTeX

---

## Workflow

### Phase 1: Research & Data Gathering

**Step 1: Define Scope**
- Clarify market definition
- Set geographic boundaries
- Determine time horizon
- Identify key questions to answer

**Step 2: Conduct Deep Research**

Use `research-lookup` extensively to gather market data:

```bash
# Market size and growth data
python skills/research-lookup/scripts/research_lookup.py \
  "What is the current market size and projected growth rate for [MARKET] industry? Include TAM, SAM, SOM estimates and CAGR projections"

# Competitive landscape
python skills/research-lookup/scripts/research_lookup.py \
  "Who are the top 10 competitors in the [MARKET] market? What is their market share and competitive positioning?"

# Industry trends
python skills/research-lookup/scripts/research_lookup.py \
  "What are the major trends and growth drivers in the [MARKET] industry for 2024-2030?"

# Regulatory environment
python skills/research-lookup/scripts/research_lookup.py \
  "What are the key regulations and policy changes affecting the [MARKET] industry?"
```

**Step 3: Data Organization**
- Create `sources/` folder with research notes
- Organize data by section
- Identify data gaps
- Conduct follow-up research as needed

### Phase 2: Analysis & Framework Application

**Step 4: Apply Analysis Frameworks**

For each framework, conduct structured analysis:

- **Market Sizing**: TAM → SAM → SOM with clear assumptions
- **Porter's Five Forces**: Rate each force High/Medium/Low with rationale
- **PESTLE**: Analyze each dimension with trends and impacts
- **SWOT**: Internal strengths/weaknesses, external opportunities/threats
- **Competitive Positioning**: Define axes, plot competitors

**Step 5: Develop Insights**
- Synthesize findings into key insights
- Identify strategic implications
- Develop recommendations
- Prioritize opportunities

### Phase 3: Visual Generation

**Step 6: Generate All Visuals**

Generate visuals BEFORE writing the report. Use the batch generation script:

```bash
# Generate all standard market report visuals
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" \
  --output-dir figures/
```

Or generate individually:

```bash
# 1. Market growth trajectory
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart showing market growth from 2020 to 2034, with historical bars in dark blue (2020-2024) and projected bars in light blue (2025-2034). Y-axis shows market size in billions USD. Include CAGR annotation" \
  -o figures/01_market_growth.png --doc-type report

# 2. TAM/SAM/SOM breakdown
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles diagram. Outer circle TAM Total Addressable Market, middle circle SAM Serviceable Addressable Market, inner circle SOM Serviceable Obtainable Market. Each labeled with acronym and description. Blue gradient" \
  -o figures/02_tam_sam_som.png --doc-type report

# 3. Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: Threat of New Entrants (top), Bargaining Power of Suppliers (left), Bargaining Power of Buyers (right), Threat of Substitutes (bottom). Color code by rating: High=red, Medium=yellow, Low=green" \
  -o figures/03_porters_five_forces.png --doc-type report

# 4. Competitive positioning matrix
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix with X-axis 'Market Focus (Niche to Broad)' and Y-axis 'Solution Approach (Product to Platform)'. Plot 8-10 competitors as labeled circles of varying sizes. Include quadrant labels" \
  -o figures/04_competitive_positioning.png --doc-type report

# 5. Risk heatmap
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact (Low to Critical), Y-axis Probability (Unlikely to Very Likely). Color gradient: Green (low risk) to Red (critical risk). Plot 10-12 risks as labeled points" \
  -o figures/05_risk_heatmap.png --doc-type report

# 6. (Optional) Executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, modern data visualization style, blue and green color scheme, clean minimalist design" \
  --output figures/06_exec_summary.png
```

### Phase 4: Report Writing

**Step 7: Initialize Project Structure**

Create the standard project structure:

```
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── progress.md
├── drafts/
│   └── v1_market_report.tex
├── references/
│   └── references.bib
├── figures/
│   └── [all generated visuals]
├── sources/
│   └── [research notes]
└── final/
```

**Step 8: Write Report Using Template**

Use the `market_report_template.tex` as a starting point. Write each section following the structure guide, ensuring:

- **Comprehensive coverage**: Every subsection addressed
- **Data-driven content**: Claims supported by research
- **Visual integration**: Reference all generated figures
- **Professional tone**: Consulting-style writing
- **No token constraints**: Write fully, don't abbreviate

**Writing Guidelines:**
- Use active voice where possible
- Lead with insights, support with data
- Use numbered lists for recommendations
- Include data sources for all statistics
- Create smooth transitions between sections

### Phase 5: Compilation & Review

**Step 9: Compile LaTeX**

```bash
cd writing_outputs/[project_folder]/drafts/
xelatex v1_market_report.tex
bibtex v1_market_report
xelatex v1_market_report.tex
xelatex v1_market_report.tex
```

**Step 10: Quality Review**

Verify the report meets quality standards:

- [ ] Total page count is 50+ pages
- [ ] All essential visuals (5-6 core + any additional) are included and render correctly
- [ ] Executive summary captures key findings
- [ ] All data points have sources cited
- [ ] Analysis frameworks are properly applied
- [ ] Recommendations are actionable and prioritized
- [ ] No orphaned figures or tables
- [ ] Table of contents, list of figures, list of tables are accurate
- [ ] Bibliography is complete
- [ ] PDF renders without errors

**Step 11: Peer Review**

Use the peer-review skill to evaluate the report:
- Assess comprehensiveness
- Verify data accuracy
- Check logical flow
- Evaluate recommendation quality

---

## Quality Standards

### Page Count Targets

| Section | Minimum Pages | Target Pages |
|---------|---------------|--------------|
| Front Matter | 4 | 5 |
| Market Overview | 4 | 5 |
| Market Size & Growth | 5 | 7 |
| Industry Drivers | 4 | 6 |
| Competitive Landscape | 5 | 7 |
| Customer Analysis | 3 | 5 |
| Technology Landscape | 3 | 5 |
| Regulatory Environment | 2 | 4 |
| Risk Analysis | 2 | 4 |
| Strategic Recommendations | 3 | 5 |
| Implementation Roadmap | 2 | 4 |
| Investment Thesis | 2 | 4 |
| Back Matter | 4 | 5 |
| **TOTAL** | **43** | **66** |

### Visual Quality Requirements

- **Resolution**: All images at 300 DPI minimum
- **Format**: PNG for raster, PDF for vector
- **Accessibility**: Colorblind-friendly palettes
- **Consistency**: Same color scheme throughout
- **Labeling**: All axes, legends, and data points labeled
- **Source Attribution**: Sources cited in figure captions

### Data Quality Requirements

- **Currency**: Data no older than 2 years (prefer current year)
- **Sourcing**: All statistics attributed to specific sources
- **Validation**: Cross-reference multiple sources when possible
- **Assumptions**: All projections state underlying assumptions
- **Limitations**: Acknowledge data limitations and gaps

### Writing Quality Requirements

- **Objectivity**: Present balanced analysis, acknowledge uncertainties
- **Clarity**: Avoid jargon, define technical terms
- **Precision**: Use specific numbers over vague qualifiers
- **Structure**: Clear headings, logical flow, smooth transitions
- **Actionability**: Recommendations are specific and implementable

---

## LaTeX Formatting

### Using the Style Package

The `market_research.sty` package provides professional formatting. Include it in your document:

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{market_research}
```

### Box Environments

Use colored boxes to highlight key content:

```latex
% Key insight box (blue)
\begin{keyinsightbox}[Key Finding]
The market is projected to grow at 15.3% CAGR through 2030.
\end{keyinsightbox}

% Market data box (green)
\begin{marketdatabox}[Market Snapshot]
\begin{itemize}
    \item Market Size (2024): \$45.2B
    \item Projected Size (2030): \$98.7B
    \item CAGR: 15.3%
\end{itemize}
\end{marketdatabox}

% Risk box (orange/warning)
\begin{riskbox}[Critical Risk]
Regulatory changes could impact 40% of market participants.
\end{riskbox}

% Recommendation box (purple)
\begin{recommendationbox}[Strategic Recommendation]
Prioritize market entry in the Asia-Pacific region.
\end{recommendationbox}

% Callout box (gray)
\begin{calloutbox}[Definition]
TAM (Total Addressable Market) represents the total revenue opportunity.
\end{calloutbox}
```

### Figure Formatting

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/market_growth.png}
\caption{Market Growth Trajectory (2020-2030). Source: Industry analysis, company data.}
\label{fig:market_growth}
\end{figure}
```

### Table Formatting

```latex
\begin{table}[htbp]
\centering
\caption{Market Size by Region (2024)}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Region} & \textbf{Size (USD)} & \textbf{Share} & \textbf{CAGR} \\
\midrule
North America & \$18.2B & 40.3\% & 12.5\% \\
\rowcolor{tablealt} Europe & \$12.1B & 26.8\% & 14.2\% \\
Asia-Pacific & \$10.5B & 23.2\% & 18.7\% \\
\rowcolor{tablealt} Rest of World & \$4.4B & 9.7\% & 11.3\% \\
\midrule
\textbf{Total} & \textbf{\$45.2B} & \textbf{100\%} & \textbf{15.3\%} \\
\bottomrule
\end{tabular}
\label{tab:market_by_region}
\end{table}
```

For complete formatting reference, see `assets/FORMATTING_GUIDE.md`.

---

## Integration with Other Skills

This skill works synergistically with:

- **research-lookup**: Essential for gathering market data, statistics, and competitive intelligence
- **scientific-schematics**: Generate all diagrams, charts, and visualizations
- **generate-image**: Create infographics and conceptual illustrations
- **peer-review**: Evaluate report quality and completeness
- **citation-management**: Manage BibTeX references

---

## Example Prompts

### Market Overview Section

```
Write a comprehensive market overview section for the [Electric Vehicle Charging Infrastructure] market. Include:
- Clear market definition and scope
- Industry ecosystem with key stakeholders
- Value chain analysis
- Historical evolution of the market
- Current market dynamics

Generate 2 supporting visuals using scientific-schematics.
```

### Competitive Landscape Section

```
Analyze the competitive landscape for the [Cloud Computing] market. Include:
- Porter's Five Forces analysis with High/Medium/Low ratings
- Top 10 competitors with market share
- Competitive positioning matrix
- Strategic group mapping
- Barriers to entry analysis

Generate 4 supporting visuals including Porter's Five Forces diagram and positioning matrix.
```

### Strategic Recommendations Section

```
Develop strategic recommendations for entering the [Renewable Energy Storage] market. Include:
- 5-7 prioritized recommendations
- Opportunity sizing for each
- Implementation considerations
- Risk factors and mitigations
- Success criteria

Generate 3 supporting visuals including opportunity matrix and priority framework.
```

---

## Checklist: 50+ Page Validation

Before finalizing the report, verify:

### Structure Completeness
- [ ] Cover page with hero visual
- [ ] Table of contents (auto-generated)
- [ ] List of figures (auto-generated)
- [ ] List of tables (auto-generated)
- [ ] Executive summary (2-3 pages)
- [ ] All 11 core chapters present
- [ ] Appendix A: Methodology
- [ ] Appendix B: Data tables
- [ ] Appendix C: Company profiles
- [ ] References/Bibliography

### Visual Completeness (Core 5-6)
- [ ] Market growth trajectory chart (Priority 1)
- [ ] TAM/SAM/SOM diagram (Priority 2)
- [ ] Porter's Five Forces (Priority 3)
- [ ] Competitive positioning matrix (Priority 4)
- [ ] Risk heatmap (Priority 5)
- [ ] Executive summary infographic (Priority 6, optional)

### Additional Visuals (Generate as Needed)
- [ ] Market ecosystem diagram
- [ ] Regional breakdown chart
- [ ] Segment growth chart
- [ ] Industry trends/PESTLE diagram
- [ ] Market share chart
- [ ] Customer segmentation chart
- [ ] Technology roadmap
- [ ] Regulatory timeline
- [ ] Opportunity matrix
- [ ] Implementation timeline
- [ ] Financial projections chart
- [ ] Other section-specific visuals

### Content Quality
- [ ] All statistics have sources
- [ ] Projections include assumptions
- [ ] Frameworks properly applied
- [ ] Recommendations are actionable
- [ ] Writing is professional quality
- [ ] No placeholder or incomplete sections

### Technical Quality
- [ ] PDF compiles without errors
- [ ] All figures render correctly
- [ ] Cross-references work
- [ ] Bibliography complete
- [ ] Page count exceeds 50

---

## Resources

### Reference Files

Load these files for detailed guidance:

- **`references/report_structure_guide.md`**: Detailed section-by-section content requirements
- **`references/visual_generation_guide.md`**: Complete prompts for generating all visual types
- **`references/data_analysis_patterns.md`**: Templates for Porter's, PESTLE, SWOT, etc.

### Assets

- **`assets/market_research.sty`**: LaTeX style package
- **`assets/market_report_template.tex`**: Complete LaTeX template
- **`assets/FORMATTING_GUIDE.md`**: Quick reference for box environments and styling

### Scripts

- **`scripts/generate_market_visuals.py`**: Batch generate all report visuals

---

## Troubleshooting

### Common Issues

**Problem**: Report is under 50 pages
- **Solution**: Expand data tables in appendices, add more detailed company profiles, include additional regional breakdowns

**Problem**: Visuals not rendering
- **Solution**: Check file paths in LaTeX, ensure images are in figures/ folder, verify file extensions

**Problem**: Bibliography missing entries
- **Solution**: Run bibtex after first xelatex pass, check .bib file for syntax errors

**Problem**: Table/figure overflow
- **Solution**: Use `\resizebox` or `adjustbox` package, reduce image width percentage

**Problem**: Poor visual quality from generation
- **Solution**: Use `--doc-type report` flag, increase iterations with `--iterations 5`

---

Use this skill to create comprehensive, visually-rich market research reports that rival top consulting firm deliverables. The combination of deep research, structured frameworks, and extensive visualization produces documents that inform strategic decisions and demonstrate analytical rigor.

---

## Reference: Data_Analysis_Patterns

# Data Analysis Patterns for Market Research

Templates and frameworks for conducting rigorous market analysis.

---

## Market Sizing Frameworks

### TAM/SAM/SOM Analysis

**Total Addressable Market (TAM)** represents the total revenue opportunity if 100% market share was achieved.

#### Top-Down Approach
```
TAM = Total Industry Revenue (from market research reports)

Example:
- Global AI Software Market (2024): $184 billion
- Source: Gartner, IDC, or similar
```

#### Bottom-Up Approach
```
TAM = Number of Potential Customers × Average Revenue per Customer

Example:
- Number of enterprises globally: 400 million
- Target segment (large enterprises): 50,000
- Average annual spend on solution: $500,000
- TAM = 50,000 × $500,000 = $25 billion
```

**Serviceable Addressable Market (SAM)** represents the portion of TAM that can be served given product/service capabilities.

```
SAM = TAM × Applicable Segment %

Example:
- TAM: $25 billion
- Geographic constraint (North America only): 40%
- Product fit (enterprise only): 60%
- SAM = $25B × 40% × 60% = $6 billion
```

**Serviceable Obtainable Market (SOM)** represents realistic market share capture.

```
SOM = SAM × Achievable Market Share %

Example:
- SAM: $6 billion
- Conservative market share (5%): $300 million
- Base case market share (10%): $600 million
- Optimistic market share (15%): $900 million
```

### Growth Rate Calculation

#### CAGR (Compound Annual Growth Rate)
```
CAGR = (End Value / Start Value)^(1/n) - 1

Where n = number of years

Example:
- 2020 market size: $10 billion
- 2024 market size: $18 billion
- n = 4 years
- CAGR = (18/10)^(1/4) - 1 = 15.8%
```

#### Year-over-Year Growth
```
YoY Growth = (Current Year - Previous Year) / Previous Year × 100

Example:
- 2023: $15 billion
- 2024: $18 billion
- YoY Growth = (18-15)/15 × 100 = 20%
```

---

## Porter's Five Forces Analysis

### Framework Template

For each force, assess: **HIGH**, **MEDIUM**, or **LOW**

#### 1. Threat of New Entrants

**Factors to evaluate:**
| Factor | Assessment | Notes |
|--------|------------|-------|
| Capital requirements | High/Med/Low | $ required to enter |
| Economies of scale | Strong/Moderate/Weak | Incumbent advantages |
| Brand loyalty | High/Med/Low | Customer switching cost |
| Access to distribution | Easy/Moderate/Difficult | Channel availability |
| Regulatory barriers | High/Med/Low | Licensing, certifications |
| Proprietary technology | Critical/Important/Minor | IP and know-how |
| Expected retaliation | Aggressive/Moderate/Passive | Incumbent response |

**Overall Assessment:** [HIGH/MEDIUM/LOW]

**Key Insights:** [Summary of implications]

#### 2. Bargaining Power of Suppliers

**Factors to evaluate:**
| Factor | Assessment | Notes |
|--------|------------|-------|
| Supplier concentration | High/Med/Low | Number of suppliers |
| Switching costs | High/Med/Low | Cost to change suppliers |
| Supplier differentiation | High/Med/Low | Uniqueness of inputs |
| Forward integration threat | High/Med/Low | Can suppliers compete? |
| Importance to supplier | Critical/Important/Minor | Your share of their revenue |
| Substitute inputs | Many/Some/Few | Alternatives available |

**Overall Assessment:** [HIGH/MEDIUM/LOW]

#### 3. Bargaining Power of Buyers

**Factors to evaluate:**
| Factor | Assessment | Notes |
|--------|------------|-------|
| Buyer concentration | High/Med/Low | Few large vs. many small |
| Purchase volume | Large/Medium/Small | Relative importance |
| Switching costs | Low/Med/High | Cost to change vendors |
| Price sensitivity | High/Med/Low | Focus on price vs. value |
| Backward integration threat | High/Med/Low | Can buyers self-supply? |
| Information availability | Full/Partial/Limited | Market transparency |

**Overall Assessment:** [HIGH/MEDIUM/LOW]

#### 4. Threat of Substitutes

**Factors to evaluate:**
| Factor | Assessment | Notes |
|--------|------------|-------|
| Substitute availability | Many/Some/Few | Number of alternatives |
| Price-performance ratio | Better/Same/Worse | Value comparison |
| Switching costs | Low/Med/High | Friction to substitute |
| Buyer propensity to switch | High/Med/Low | Willingness to change |
| Perceived differentiation | Low/Med/High | Unique value |

**Overall Assessment:** [HIGH/MEDIUM/LOW]

#### 5. Competitive Rivalry

**Factors to evaluate:**
| Factor | Assessment | Notes |
|--------|------------|-------|
| Number of competitors | Many/Several/Few | Market fragmentation |
| Industry growth | Slow/Moderate/Fast | Growth rate impact |
| Fixed costs | High/Med/Low | Pressure to fill capacity |
| Product differentiation | Low/Med/High | Commoditization level |
| Exit barriers | High/Med/Low | Difficulty leaving market |
| Strategic stakes | High/Med/Low | Importance to competitors |

**Overall Assessment:** [HIGH/MEDIUM/LOW]

### Five Forces Summary Table

| Force | Rating | Key Drivers | Implications |
|-------|--------|-------------|--------------|
| New Entrants | [H/M/L] | [Top factors] | [Strategic impact] |
| Supplier Power | [H/M/L] | [Top factors] | [Strategic impact] |
| Buyer Power | [H/M/L] | [Top factors] | [Strategic impact] |
| Substitutes | [H/M/L] | [Top factors] | [Strategic impact] |
| Rivalry | [H/M/L] | [Top factors] | [Strategic impact] |

**Overall Industry Attractiveness:** [ATTRACTIVE / MODERATE / UNATTRACTIVE]

---

## PESTLE Analysis

### Framework Template

#### Political Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| Government stability | | ↑ ↓ → | H/M/L | Short/Med/Long |
| Trade policies | | ↑ ↓ → | H/M/L | |
| Tax regulations | | ↑ ↓ → | H/M/L | |
| Government support | | ↑ ↓ → | H/M/L | |
| Political relations | | ↑ ↓ → | H/M/L | |

**Key Political Implications:** [Summary]

#### Economic Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| GDP growth | X.X% | ↑ ↓ → | H/M/L | |
| Interest rates | X.X% | ↑ ↓ → | H/M/L | |
| Inflation | X.X% | ↑ ↓ → | H/M/L | |
| Exchange rates | | ↑ ↓ → | H/M/L | |
| Consumer spending | | ↑ ↓ → | H/M/L | |
| Unemployment | X.X% | ↑ ↓ → | H/M/L | |

**Key Economic Implications:** [Summary]

#### Social Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| Demographics | | ↑ ↓ → | H/M/L | |
| Cultural attitudes | | ↑ ↓ → | H/M/L | |
| Consumer behavior | | ↑ ↓ → | H/M/L | |
| Education levels | | ↑ ↓ → | H/M/L | |
| Health consciousness | | ↑ ↓ → | H/M/L | |
| Work-life balance | | ↑ ↓ → | H/M/L | |

**Key Social Implications:** [Summary]

#### Technological Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| R&D activity | | ↑ ↓ → | H/M/L | |
| Technology adoption | | ↑ ↓ → | H/M/L | |
| Automation | | ↑ ↓ → | H/M/L | |
| Digital infrastructure | | ↑ ↓ → | H/M/L | |
| Innovation rate | | ↑ ↓ → | H/M/L | |
| Disruptive tech | | ↑ ↓ → | H/M/L | |

**Key Technological Implications:** [Summary]

#### Legal Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| Industry regulations | | ↑ ↓ → | H/M/L | |
| Data protection | | ↑ ↓ → | H/M/L | |
| Employment law | | ↑ ↓ → | H/M/L | |
| Consumer protection | | ↑ ↓ → | H/M/L | |
| IP rights | | ↑ ↓ → | H/M/L | |
| Antitrust | | ↑ ↓ → | H/M/L | |

**Key Legal Implications:** [Summary]

#### Environmental Factors

| Factor | Current State | Trend | Impact | Time Horizon |
|--------|---------------|-------|--------|--------------|
| Climate change | | ↑ ↓ → | H/M/L | |
| Sustainability reqs | | ↑ ↓ → | H/M/L | |
| Resource availability | | ↑ ↓ → | H/M/L | |
| Waste management | | ↑ ↓ → | H/M/L | |
| Carbon regulations | | ↑ ↓ → | H/M/L | |
| Environmental awareness | | ↑ ↓ → | H/M/L | |

**Key Environmental Implications:** [Summary]

---

## SWOT Analysis

### Framework Template

#### Strengths (Internal, Positive)
| Strength | Evidence | Strategic Value |
|----------|----------|-----------------|
| [Strength 1] | [Data/proof] | High/Med/Low |
| [Strength 2] | [Data/proof] | High/Med/Low |
| [Strength 3] | [Data/proof] | High/Med/Low |

**Core Strengths Summary:** [2-3 sentence synthesis]

#### Weaknesses (Internal, Negative)
| Weakness | Evidence | Severity |
|----------|----------|----------|
| [Weakness 1] | [Data/proof] | Critical/Moderate/Minor |
| [Weakness 2] | [Data/proof] | Critical/Moderate/Minor |
| [Weakness 3] | [Data/proof] | Critical/Moderate/Minor |

**Key Vulnerabilities Summary:** [2-3 sentence synthesis]

#### Opportunities (External, Positive)
| Opportunity | Size/Potential | Timeframe |
|-------------|----------------|-----------|
| [Opportunity 1] | $X / High/Med/Low | Short/Med/Long |
| [Opportunity 2] | $X / High/Med/Low | Short/Med/Long |
| [Opportunity 3] | $X / High/Med/Low | Short/Med/Long |

**Priority Opportunities Summary:** [2-3 sentence synthesis]

#### Threats (External, Negative)
| Threat | Likelihood | Impact |
|--------|------------|--------|
| [Threat 1] | High/Med/Low | High/Med/Low |
| [Threat 2] | High/Med/Low | High/Med/Low |
| [Threat 3] | High/Med/Low | High/Med/Low |

**Critical Threats Summary:** [2-3 sentence synthesis]

### SWOT Strategy Matrix

| | **Strengths** | **Weaknesses** |
|---|---------------|----------------|
| **Opportunities** | **SO Strategies** (use strengths to capture opportunities) | **WO Strategies** (overcome weaknesses to capture opportunities) |
| **Threats** | **ST Strategies** (use strengths to mitigate threats) | **WT Strategies** (minimize weaknesses and avoid threats) |

---

## BCG Growth-Share Matrix

### Framework Template

**Axes:**
- X-axis: Relative Market Share (High → Low, logarithmic scale)
- Y-axis: Market Growth Rate (High → Low, typically 10% as midpoint)

### Quadrant Definitions

| Quadrant | Growth | Share | Characteristics | Strategy |
|----------|--------|-------|-----------------|----------|
| **Stars** | High | High | Market leaders in growing markets | Invest to maintain position |
| **Cash Cows** | Low | High | Market leaders in mature markets | Harvest for cash flow |
| **Question Marks** | High | Low | Small share in growing markets | Invest selectively or divest |
| **Dogs** | Low | Low | Small share in mature markets | Divest or minimize investment |

### Product/Business Unit Analysis

| Product/BU | Market Growth | Relative Share | Quadrant | Recommended Strategy |
|------------|---------------|----------------|----------|---------------------|
| [Product A] | X.X% | X.X | Star/Cow/QM/Dog | [Strategy] |
| [Product B] | X.X% | X.X | Star/Cow/QM/Dog | [Strategy] |
| [Product C] | X.X% | X.X | Star/Cow/QM/Dog | [Strategy] |

### Portfolio Balance Assessment

| Quadrant | Number of Products | Revenue % | Investment Priority |
|----------|-------------------|-----------|---------------------|
| Stars | X | X% | High |
| Cash Cows | X | X% | Maintain |
| Question Marks | X | X% | Selective |
| Dogs | X | X% | Low/Divest |

---

## Value Chain Analysis

### Framework Template

#### Primary Activities

| Activity | Description | Value Created | Cost | Competitive Position |
|----------|-------------|---------------|------|---------------------|
| **Inbound Logistics** | Receiving, storing, inventory | | $X | Strong/Average/Weak |
| **Operations** | Manufacturing, assembly | | $X | Strong/Average/Weak |
| **Outbound Logistics** | Distribution, delivery | | $X | Strong/Average/Weak |
| **Marketing & Sales** | Promotion, sales force | | $X | Strong/Average/Weak |
| **Service** | Installation, support, repair | | $X | Strong/Average/Weak |

#### Support Activities

| Activity | Description | Value Created | Cost | Competitive Position |
|----------|-------------|---------------|------|---------------------|
| **Infrastructure** | Management, finance, legal | | $X | Strong/Average/Weak |
| **HR Management** | Recruiting, training, comp | | $X | Strong/Average/Weak |
| **Technology Dev** | R&D, process improvement | | $X | Strong/Average/Weak |
| **Procurement** | Purchasing, supplier mgmt | | $X | Strong/Average/Weak |

### Value Chain Margin Analysis

```
Total Revenue:           $XXX
- Inbound Logistics:     ($XX)
- Operations:            ($XX)
- Outbound Logistics:    ($XX)
- Marketing & Sales:     ($XX)
- Service:               ($XX)
- Support Activities:    ($XX)
= Margin:                $XX (X%)
```

### Competitive Comparison

| Activity | Company | Industry Avg | Best-in-Class | Gap |
|----------|---------|--------------|---------------|-----|
| [Activity] | X% | Y% | Z% | +/-X% |

---

## Competitive Positioning Analysis

### Framework Template

#### Positioning Dimensions

Common positioning dimension pairs:
- Price vs. Quality
- Market Focus (Niche vs. Broad)
- Solution Type (Product vs. Platform)
- Geographic Scope (Regional vs. Global)
- Customer Focus (Enterprise vs. SMB vs. Consumer)
- Innovation Level (Leader vs. Follower)

#### Competitor Mapping

| Competitor | Dimension 1 Score (1-10) | Dimension 2 Score (1-10) | Market Share | Notes |
|------------|-------------------------|-------------------------|--------------|-------|
| Company A | X | X | X% | [Position description] |
| Company B | X | X | X% | [Position description] |
| Company C | X | X | X% | [Position description] |

#### Strategic Group Identification

| Strategic Group | Companies | Characteristics | Market Share |
|-----------------|-----------|-----------------|--------------|
| Group 1: [Name] | A, B, C | [Description] | X% |
| Group 2: [Name] | D, E | [Description] | X% |
| Group 3: [Name] | F, G, H | [Description] | X% |

---

## Risk Assessment Framework

### Risk Identification

#### Risk Categories
1. **Market Risks**: Demand changes, price pressure, market shifts
2. **Competitive Risks**: New entrants, competitor moves, disruption
3. **Regulatory Risks**: New regulations, compliance requirements
4. **Technology Risks**: Obsolescence, security, integration
5. **Operational Risks**: Supply chain, quality, capacity
6. **Financial Risks**: Currency, interest rates, credit
7. **Reputational Risks**: Brand damage, social media, ethics

### Risk Assessment Matrix

| Risk ID | Risk Description | Category | Probability | Impact | Score | Priority |
|---------|------------------|----------|-------------|--------|-------|----------|
| R1 | [Description] | Market | 1-5 | 1-5 | P×I | H/M/L |
| R2 | [Description] | Competitive | 1-5 | 1-5 | P×I | H/M/L |

**Scoring Guide:**
- Probability: 1=Very Unlikely, 2=Unlikely, 3=Possible, 4=Likely, 5=Very Likely
- Impact: 1=Minimal, 2=Minor, 3=Moderate, 4=Major, 5=Severe
- Priority: Score 15-25=High, 8-14=Medium, 1-7=Low

### Risk Mitigation Planning

| Risk ID | Risk | Mitigation Strategy | Owner | Timeline | Cost |
|---------|------|---------------------|-------|----------|------|
| R1 | [Risk] | [Prevention + Response] | [Name] | [Date] | $X |

---

## Financial Analysis Patterns

### Revenue Projection Model

```
Year N Revenue = Year N-1 Revenue × (1 + Growth Rate)

Or bottom-up:
Revenue = Customers × Revenue per Customer × Retention Rate
        + New Customers × Revenue per Customer × (1 - Churn Rate)
```

### Scenario Analysis Template

| Metric | Conservative | Base Case | Optimistic |
|--------|--------------|-----------|------------|
| Market Growth | X% | Y% | Z% |
| Market Share | X% | Y% | Z% |
| Pricing | $X | $Y | $Z |
| Gross Margin | X% | Y% | Z% |
| **Revenue Y5** | $X | $Y | $Z |
| **EBITDA Y5** | $X | $Y | $Z |

### Key Financial Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Gross Margin | (Revenue - COGS) / Revenue | X% |
| EBITDA Margin | EBITDA / Revenue | X% |
| Customer Acquisition Cost | Sales & Marketing / New Customers | $X |
| Lifetime Value | ARPU × Gross Margin × Lifetime | $X |
| LTV/CAC Ratio | LTV / CAC | >3x |
| Payback Period | CAC / (ARPU × Gross Margin × 12) | <X months |

---

## Data Collection Checklist

### Market Size Data
- [ ] Current market size (with year and source)
- [ ] Historical market size (5-10 years)
- [ ] Market growth projections (5-10 years)
- [ ] CAGR (historical and projected)
- [ ] Regional breakdown
- [ ] Segment breakdown

### Competitive Data
- [ ] Market share by company (top 10)
- [ ] Revenue by competitor
- [ ] Growth rates by competitor
- [ ] Strategic moves (M&A, partnerships, launches)
- [ ] Pricing information
- [ ] Product/service offerings

### Customer Data
- [ ] Customer segments and sizes
- [ ] Segment growth rates
- [ ] Average deal size by segment
- [ ] Customer acquisition cost
- [ ] Customer lifetime value
- [ ] Churn rates

### Industry Data
- [ ] Key industry trends
- [ ] Regulatory developments
- [ ] Technology trends
- [ ] Economic indicators
- [ ] Demographic trends

---

## Research Sources

### Primary Research
- Customer interviews
- Expert interviews
- Surveys
- Focus groups

### Secondary Research
- Market research reports (Gartner, Forrester, IDC, McKinsey)
- Industry associations
- Government statistics
- Company annual reports
- SEC filings (10-K, 10-Q)
- Earnings call transcripts
- Trade publications
- Academic journals
- News articles

### Data Validation
- Cross-reference multiple sources
- Check date currency (prefer <2 years old)
- Verify methodology
- Note confidence levels
- Document assumptions

---

## Reference: Report_Structure_Guide

# Market Research Report Structure Guide

Detailed guidance for writing each section of a comprehensive market research report.

---

## Front Matter

### Cover Page

**Purpose:** Create a strong first impression and communicate report scope.

**Required Elements:**
- Report title (clear, specific to market being analyzed)
- Subtitle (e.g., "Comprehensive Market Analysis Report")
- Hero visualization (executive summary infographic or market-relevant image)
- Date of publication
- Prepared by / Author organization
- Classification (Confidential, Internal Use, Public)
- Report type identifier

**Best Practices:**
- Title should include market name and geography if relevant
- Use professional, high-quality hero image
- Keep design clean and uncluttered
- Include version number if applicable

---

### Table of Contents

**Auto-generated in LaTeX.** Ensure all chapters, sections, and subsections use proper commands for inclusion.

**Include:**
- List of Figures (all visualizations with page numbers)
- List of Tables (all data tables with page numbers)

---

### Executive Summary (2-3 pages)

**Purpose:** Provide a standalone summary that allows busy executives to understand key findings without reading the full report.

**Required Sections:**

#### Market Snapshot Box
Key metrics displayed prominently:
- Current market size with year
- Projected market size with year
- CAGR (compound annual growth rate)
- Largest segment and market share
- Fastest growing region and growth rate
- Key adoption/penetration metrics

#### Investment Thesis / Why This Matters
3-5 bullet points explaining:
- Why this market is attractive
- Key factors driving opportunity
- Timing considerations
- Risk-adjusted assessment

#### Key Findings Summary
Organized by theme:
- Market Dynamics (2-3 points)
- Competitive Landscape (2-3 points)
- Growth Drivers (2-3 points)
- Risk Factors (2-3 points)

#### Strategic Recommendations
Top 5 actionable recommendations, each with:
- Clear action statement
- Expected outcome
- Priority level (immediate, near-term, medium-term)

**Visual Requirements:**
- 1-2 visuals maximum
- Executive summary infographic strongly recommended
- Key metrics visualization

**Writing Guidelines:**
- Write this section LAST after completing all analysis
- Every statement should be supported by analysis in the main report
- Use specific numbers, not vague qualifiers
- Lead with most important findings
- Keep paragraphs short (2-4 sentences)

---

## Core Analysis Chapters

### Chapter 1: Market Overview & Definition (4-5 pages)

**Purpose:** Establish clear boundaries and context for the analysis.

#### Section 1.1: Market Definition

**Content Requirements:**
- Precise definition of the market being analyzed
- Products/services included in scope
- Products/services explicitly excluded
- Industry classification codes (NAICS, SIC, GICS if applicable)
- Relationship to adjacent markets

**Writing Approach:**
- Begin with a clear, one-paragraph definition
- Use a callout box to highlight the formal definition
- Explain the rationale for scope decisions
- Address common misconceptions about market boundaries

#### Section 1.2: Scope and Boundaries

**Cover:**
- Geographic scope (global, regional, specific countries)
- Product/service scope with specific categories
- Time horizon (historical period + forecast period)
- Customer segments included

#### Section 1.3: Industry Ecosystem

**Content Requirements:**
- Value chain from inputs to end users
- Key stakeholders at each stage
- Relationships and dependencies between stakeholders
- Information flows
- Money flows
- Power dynamics

**Required Visual:** Industry ecosystem/value chain diagram

**Writing Approach:**
- Start with overview of the ecosystem
- Describe each stakeholder category in detail
- Explain how value is created and captured
- Identify where power concentrates in the value chain

#### Section 1.4: Market Structure

**Content Requirements:**
- Market concentration analysis (HHI, CR4, CR8)
- Industry lifecycle stage assessment
- Market fragmentation analysis
- Vertical integration analysis

#### Section 1.5: Historical Context

**Content Requirements:**
- When the market emerged
- Key milestones in market development
- Major disruptions and shifts
- Evolution of competitive dynamics
- How customer needs have changed

**Required Visuals (2 total):**
1. Industry ecosystem diagram
2. Market structure or industry lifecycle diagram

---

### Chapter 2: Market Size & Growth Analysis (6-8 pages)

**Purpose:** Provide comprehensive quantitative analysis of market opportunity.

#### Section 2.1: Total Addressable Market (TAM)

**Content Requirements:**
- Current market size with source and methodology
- Historical market size (5-10 years back)
- Projected market size (5-10 years forward)
- Year-over-year growth rates
- CAGR (historical and projected)

**Data Table Required:**
Year-by-year market projections table showing:
- Year
- Market size (USD)
- YoY growth rate
- Cumulative CAGR

**Writing Approach:**
- State the bottom line first (total opportunity)
- Provide historical context
- Explain projection methodology
- State key assumptions
- Cite multiple sources where possible

#### Section 2.2: Serviceable Addressable Market (SAM)

**Content Requirements:**
- Definition of SAM for this market
- SAM calculation methodology
- Segment breakdown within SAM
- Growth rates by segment

**Data Table Required:**
Segment analysis table showing:
- Segment name
- 2024 value
- 2034 value
- CAGR
- Market share

#### Section 2.3: Serviceable Obtainable Market (SOM)

**Content Requirements:**
- Realistic market share scenarios
- Conservative estimate with assumptions
- Base case estimate with assumptions
- Optimistic estimate with assumptions
- Factors affecting market share capture

**Required Visual:** TAM/SAM/SOM concentric circles diagram

#### Section 2.4: Regional Market Analysis

**Content Requirements:**
- Market size by region
- Growth rates by region
- Regional market share
- Regional drivers and differences
- Detailed analysis of top 3-4 regions

**Required Visual:** Regional breakdown chart (pie or treemap)

**Regions to cover:**
- North America (with US/Canada breakdown if relevant)
- Europe (with key country breakdown)
- Asia-Pacific (with China, Japan, India focus)
- Latin America
- Middle East & Africa

#### Section 2.5: Segment Analysis

**Content Requirements:**
- Definition of market segments
- Size of each segment
- Growth rate of each segment
- Key drivers for each segment
- Competitive dynamics by segment

**Required Visual:** Segment growth comparison chart

**Required Visuals (4 total):**
1. Market growth trajectory chart
2. TAM/SAM/SOM diagram
3. Regional breakdown chart
4. Segment growth comparison chart

---

### Chapter 3: Industry Drivers & Trends (5-6 pages)

**Purpose:** Identify and analyze factors driving market growth and evolution.

#### Section 3.1: Primary Growth Drivers

**Content Requirements:**
- Identification of 5-10 key growth drivers
- Quantified impact assessment for each
- Timeline for impact
- Evidence and data supporting each driver

**For each driver, include:**
- Clear description
- Mechanism of impact on market
- Quantified impact estimate
- Timeline (immediate, 1-3 years, 3-5 years)
- Supporting data/evidence

**Required Visual:** Driver impact matrix (probability vs. impact)

#### Section 3.2: PESTLE Analysis

Comprehensive analysis of external factors:

**Political:**
- Government policies affecting the market
- Political stability in key markets
- Trade policies and tariffs
- Government support programs

**Economic:**
- Economic growth trends
- Interest rate environment
- Inflation impacts
- Currency effects
- Consumer spending trends

**Social:**
- Demographic trends
- Cultural shifts
- Consumer behavior changes
- Workforce trends
- Health and wellness trends

**Technological:**
- Enabling technologies
- Digital transformation
- Automation trends
- Technology adoption curves

**Legal:**
- Regulatory requirements
- Compliance costs
- Intellectual property considerations
- Employment regulations

**Environmental:**
- Sustainability requirements
- Environmental regulations
- Climate impacts
- Resource availability

**Required Visual:** PESTLE analysis diagram

#### Section 3.3: Emerging Trends

**Content Requirements:**
- Identification of 5-8 emerging trends
- Timeline for each trend
- Expected impact on market
- Companies/regions leading each trend

**Required Visual:** Trends timeline or radar chart

#### Section 3.4: Growth Inhibitors

**Content Requirements:**
- Factors slowing market growth
- Barriers to adoption
- Resource constraints
- Competitive pressures
- Regulatory hurdles

**Required Visuals (3 total):**
1. Driver impact matrix
2. PESTLE analysis diagram
3. Trends timeline

---

### Chapter 4: Competitive Landscape (6-8 pages)

**Purpose:** Provide comprehensive analysis of competitive dynamics.

#### Section 4.1: Market Structure Analysis

**Content Requirements:**
- Number of competitors
- Market concentration (HHI index)
- CR4 and CR8 ratios
- Market fragmentation assessment
- Competitive intensity rating

#### Section 4.2: Porter's Five Forces Analysis

**For each force, provide:**
- Rating: High / Medium / Low
- Key factors driving the rating
- Supporting evidence
- Strategic implications

**Forces:**
1. Threat of New Entrants
2. Bargaining Power of Suppliers
3. Bargaining Power of Buyers
4. Threat of Substitutes
5. Competitive Rivalry

**Required Visual:** Porter's Five Forces diagram

**Writing Approach:**
- Rate each force clearly
- Provide 3-5 supporting factors per force
- Include data where available
- Discuss strategic implications

#### Section 4.3: Market Share Analysis

**Content Requirements:**
- Top 10 companies by market share
- Market share trends (3-5 year view)
- Share gains/losses by company
- Regional market share variations

**Required Visual:** Market share pie chart or bar chart

**Data Table Required:**
Top 10 companies showing:
- Rank
- Company name
- Revenue/market size
- Market share %
- YoY growth/trend

#### Section 4.4: Competitive Positioning

**Content Requirements:**
- Key dimensions of competition
- Positioning of major players
- Competitive advantages by company
- Strategic moves and announcements

**Required Visual:** Competitive positioning matrix (2x2)

**Common positioning dimensions:**
- Market focus (niche vs. broad)
- Solution approach (product vs. platform)
- Price positioning (premium vs. value)
- Geographic focus (regional vs. global)
- Customer focus (enterprise vs. SMB)

#### Section 4.5: Strategic Groups

**Content Requirements:**
- Identification of strategic groups
- Companies in each group
- Mobility barriers between groups
- Competitive dynamics within groups

**Required Visual:** Strategic group map

#### Section 4.6: Competitive Dynamics

**Content Requirements:**
- Recent M&A activity
- Partnership announcements
- Product launches
- Pricing trends
- Geographic expansion

#### Section 4.7: Barriers to Entry

**Content Requirements:**
- Capital requirements
- Regulatory barriers
- Technology barriers
- Brand and reputation
- Distribution access
- Economies of scale
- Switching costs

**Required Visuals (4 total):**
1. Porter's Five Forces diagram
2. Market share chart
3. Competitive positioning matrix
4. Strategic group map

---

### Chapter 5: Customer Analysis & Segmentation (4-5 pages)

**Purpose:** Understand customer needs, behaviors, and segment attractiveness.

#### Section 5.1: Customer Segmentation

**Content Requirements:**
- Definition of customer segments
- Segment sizes and market share
- Segment characteristics
- Segment growth rates

**Required Visual:** Customer segmentation breakdown

**Common segmentation approaches:**
- By company size (Enterprise, Mid-market, SMB, Consumer)
- By industry vertical
- By geography
- By buying behavior
- By needs/use cases

#### Section 5.2: Segment Attractiveness Analysis

**Content Requirements:**
- Attractiveness criteria
- Segment scoring/ranking
- Investment implications
- Prioritization recommendations

**Required Visual:** Segment attractiveness matrix

**Attractiveness factors:**
- Segment size
- Growth rate
- Profitability
- Competitive intensity
- Accessibility
- Strategic fit

#### Section 5.3: Customer Needs Analysis

**For each segment, identify:**
- Functional needs (what the product must do)
- Emotional needs (how it makes them feel)
- Social needs (how it affects their relationships)
- Key pain points
- Unmet needs

#### Section 5.4: Buying Behavior

**Content Requirements:**
- Purchase triggers
- Decision-making process
- Key decision makers and influencers
- Evaluation criteria
- Purchase channels
- Buying cycle length
- Price sensitivity

#### Section 5.5: Customer Journey

**Required Visual:** Customer journey map

**Journey stages to cover:**
1. Awareness
2. Consideration
3. Decision
4. Implementation/Onboarding
5. Usage
6. Advocacy/Renewal

**Required Visuals (3 total):**
1. Customer segmentation breakdown
2. Segment attractiveness matrix
3. Customer journey map

---

### Chapter 6: Technology & Innovation Landscape (4-5 pages)

**Purpose:** Analyze technology trends and innovation dynamics.

#### Section 6.1: Current Technology Stack

**Content Requirements:**
- Core technologies in use
- Infrastructure requirements
- Integration landscape
- Technology maturity levels

#### Section 6.2: Technology Roadmap

**Content Requirements:**
- Near-term evolution (1-2 years)
- Medium-term evolution (3-5 years)
- Long-term evolution (5-10 years)
- Key milestones and inflection points

**Required Visual:** Technology roadmap diagram

#### Section 6.3: Emerging Technologies

**For each emerging technology, cover:**
- Technology description
- Current maturity level (TRL or similar)
- Expected timeline to mainstream
- Potential impact on market
- Leading companies/regions

**Common emerging technologies to assess:**
- Artificial intelligence/ML
- Cloud computing
- IoT/Connected devices
- Blockchain
- Automation/Robotics
- Domain-specific technologies

#### Section 6.4: Innovation Trends

**Content Requirements:**
- R&D investment levels in industry
- Patent filing trends
- Startup activity and funding
- Corporate innovation initiatives
- University/research partnerships

**Required Visual:** Innovation/adoption curve or hype cycle

#### Section 6.5: Technology Adoption Barriers

**Content Requirements:**
- Technical complexity
- Integration challenges
- Cost barriers
- Skills gaps
- Security/privacy concerns
- Change management challenges

**Required Visuals (2 total):**
1. Technology roadmap diagram
2. Innovation/adoption curve

---

### Chapter 7: Regulatory & Policy Environment (3-4 pages)

**Purpose:** Analyze regulatory framework and policy impacts.

#### Section 7.1: Current Regulatory Framework

**Content Requirements:**
- Key regulations affecting the market
- Regulatory bodies and their roles
- Compliance requirements
- Enforcement mechanisms
- Penalties for non-compliance

#### Section 7.2: Regulatory Timeline

**Required Visual:** Regulatory timeline

**Content Requirements:**
- Historical regulatory milestones
- Recent regulatory changes
- Upcoming regulations
- Expected future developments

#### Section 7.3: Regulatory Impact Analysis

**Content Requirements:**
- Compliance costs
- Market access implications
- Competitive implications
- Product/service requirements
- Operating restrictions

#### Section 7.4: Policy Trends

**Content Requirements:**
- Government priorities
- Funding initiatives
- Trade policies
- Environmental policies
- Industry-specific policies

#### Section 7.5: Regional Regulatory Differences

**Content Requirements:**
- Comparison of regulations by region
- Harmonization efforts
- Key differences to navigate
- Best practices for compliance

**Required Visuals (1 total):**
1. Regulatory timeline

---

### Chapter 8: Risk Analysis (3-4 pages)

**Purpose:** Identify, assess, and propose mitigations for key risks.

#### Section 8.1: Risk Overview

**Content Requirements:**
- Risk categories covered
- Risk assessment methodology
- Overall risk profile assessment

#### Section 8.2: Risk Assessment

**Required Visual:** Risk heatmap (probability vs. impact)

**Risk categories to cover:**
- Market risks
- Competitive risks
- Regulatory risks
- Technology risks
- Operational risks
- Financial risks
- Reputational risks

**For each risk, include:**
- Risk description
- Probability rating (Low/Medium/High)
- Impact rating (Low/Medium/High)
- Overall risk rating
- Contributing factors
- Early warning indicators

**Data Table Required:**
Risk register showing:
- Risk name
- Category
- Probability
- Impact
- Overall rating
- Owner

#### Section 8.3: Detailed Risk Analysis

Provide detailed analysis of top 5-10 risks, including:
- Full description of the risk
- Scenarios that could trigger it
- Potential consequences
- Affected stakeholders
- Timeline considerations

#### Section 8.4: Risk Mitigation Strategies

**Required Visual:** Risk mitigation matrix

**For each major risk, provide:**
- Prevention strategies
- Detection mechanisms
- Response plans
- Recovery approaches
- Contingency plans

**Required Visuals (2 total):**
1. Risk heatmap
2. Risk mitigation matrix

---

## Strategic Recommendations Chapters

### Chapter 9: Strategic Opportunities & Recommendations (4-5 pages)

**Purpose:** Synthesize analysis into actionable strategic guidance.

#### Section 9.1: Opportunity Analysis

**Required Visual:** Opportunity matrix (attractiveness vs. ability to win)

**Content Requirements:**
- Identification of 5-8 strategic opportunities
- Sizing of each opportunity
- Attractiveness assessment
- Ability to win assessment
- Prioritization

#### Section 9.2: Detailed Opportunity Analysis

For each top opportunity, provide:
- Description and scope
- Market size potential
- Growth trajectory
- Key success factors
- Required capabilities
- Investment requirements
- Expected returns
- Timeline to value

#### Section 9.3: Strategic Options Analysis

**Content Requirements:**
- Build (organic development) options
- Buy (M&A) options
- Partner (strategic alliances) options
- Decision framework for each opportunity

#### Section 9.4: Prioritized Recommendations

**Required Visual:** Recommendation priority matrix (impact vs. effort)

**Structure recommendations in tiers:**

**Tier 1: Immediate Priority**
- Actions to take in next 0-6 months
- Quick wins with high impact
- Foundation-setting activities

**Tier 2: Near-Term (6-12 months)**
- Build on Tier 1 actions
- Larger investments
- Capability development

**Tier 3: Medium-Term (1-2 years)**
- Strategic initiatives
- Major investments
- Transformational changes

**For each recommendation:**
- Clear action statement
- Rationale (why this matters)
- Expected outcome
- Investment required
- Timeline
- Success metrics
- Dependencies

#### Section 9.5: Success Factors

**Content Requirements:**
- Critical success factors for implementation
- Organizational capabilities required
- Resource requirements
- External dependencies
- Timing considerations

**Required Visuals (3 total):**
1. Opportunity matrix
2. Strategic options framework
3. Recommendation priority matrix

---

### Chapter 10: Implementation Roadmap (3-4 pages)

**Purpose:** Provide actionable implementation guidance.

#### Section 10.1: Implementation Overview

**Content Requirements:**
- Phased approach description
- Overall timeline
- Key dependencies
- Critical path items

#### Section 10.2: Phased Implementation Plan

**Required Visual:** Implementation timeline/Gantt chart

**For each phase:**
- Phase name and duration
- Objectives
- Key activities
- Deliverables
- Resources required
- Dependencies
- Success criteria

**Typical phases:**
- Phase 1: Foundation (months 1-6)
- Phase 2: Build (months 4-12)
- Phase 3: Scale (months 10-18)
- Phase 4: Optimize (months 16-24)

#### Section 10.3: Key Milestones

**Required Visual:** Milestone tracker

**Data Table Required:**
Milestone table showing:
- Milestone name
- Target date
- Owner
- Success criteria
- Dependencies

#### Section 10.4: Resource Requirements

**Content Requirements:**
- Team structure and roles
- Budget allocation by phase
- Technology requirements
- External support needs
- Training requirements

#### Section 10.5: Governance Structure

**Content Requirements:**
- Decision-making authority
- Reporting structure
- Review cadence
- Escalation paths
- Change management process

**Required Visuals (2 total):**
1. Implementation timeline/Gantt
2. Milestone tracker

---

### Chapter 11: Investment Thesis & Financial Projections (3-4 pages)

**Purpose:** Provide financial framework for decision-making.

#### Section 11.1: Investment Summary

**Content Requirements:**
- Summary of investment opportunity
- Key value drivers
- Expected returns
- Investment timeline
- Risk-adjusted assessment

#### Section 11.2: Financial Projections

**Required Visual:** Financial projections chart

**Data Table Required:**
5-year projections showing:
- Revenue
- Growth rate
- Gross margin
- EBITDA
- EBITDA margin
- Key operating metrics

#### Section 11.3: Scenario Analysis

**Required Visual:** Scenario comparison chart

**Three scenarios:**
- Conservative: Lower growth, higher costs
- Base Case: Expected performance
- Optimistic: Favorable conditions

**For each scenario:**
- Key assumptions
- Revenue projections
- Profitability projections
- Investment requirements
- Return metrics

#### Section 11.4: Key Assumptions

**Document all assumptions:**
- Market growth assumptions
- Market share assumptions
- Pricing assumptions
- Cost assumptions
- Timing assumptions
- Competitive assumptions

#### Section 11.5: Sensitivity Analysis

**Content Requirements:**
- Key variables affecting returns
- Sensitivity to market growth
- Sensitivity to pricing
- Sensitivity to timing
- Break-even analysis

#### Section 11.6: Return Expectations

**Content Requirements:**
- ROI projections
- Payback period
- IRR estimates
- NPV analysis
- Multiple analysis (if applicable)

**Required Visuals (2 total):**
1. Financial projections chart
2. Scenario comparison chart

---

## Back Matter

### Appendix A: Methodology & Data Sources

**Content Requirements:**
- Research methodology description
- Primary research methods
- Secondary research sources
- Data collection timeframe
- Analytical frameworks used
- Limitations and assumptions

### Appendix B: Detailed Market Data

**Content Requirements:**
- Comprehensive data tables
- Year-by-year market data
- Regional breakdowns
- Segment details
- Historical data series

### Appendix C: Company Profiles

**For each major company:**
- Company overview
- Headquarters and key locations
- Revenue and employee count
- Market position
- Key products/services
- Recent developments
- Strategic focus

### References/Bibliography

**All sources cited:**
- Market research reports
- Industry publications
- Government data
- Company reports
- Academic sources
- News articles

---

## Quality Checklist

Before finalizing, verify:

- [ ] All required sections are complete
- [ ] All data points have sources
- [ ] All 25-30 visuals are included
- [ ] Executive summary captures key findings
- [ ] Recommendations are actionable
- [ ] Financial projections are internally consistent
- [ ] No placeholder content remains
- [ ] Page count exceeds 50 pages
- [ ] Table of contents is accurate
- [ ] All cross-references work
- [ ] Bibliography is complete

---

## Reference: Visual_Generation_Guide

# Visual Generation Guide for Market Research Reports

Complete prompts and guidance for generating visualizations in market research reports.

---

## Overview

Market research reports should start with **5-6 essential visuals** to establish the analytical framework. Additional visuals can be generated as needed when writing specific sections. This guide provides ready-to-use prompts for the `scientific-schematics` and `generate-image` skills.

### Core Visuals (Generate First - Priority 1-6)

Start every market report by generating these 5-6 core visuals:

1. **Market Growth Trajectory Chart** - Shows market size trends
2. **TAM/SAM/SOM Diagram** - Market opportunity breakdown
3. **Porter's Five Forces** - Competitive dynamics framework
4. **Competitive Positioning Matrix** - Strategic positioning
5. **Risk Heatmap** - Risk assessment visualization
6. **Executive Summary Infographic** (optional) - Report overview

### Extended Visuals (Generate as Needed - Priority 7+)

Additional visuals can be generated during writing when specific sections require visual support:
- Regional breakdown charts
- Segment analysis
- Customer journey maps
- Technology roadmaps
- Regulatory timelines
- Financial projections
- Implementation timelines

### Tool Selection

| Visual Type | Tool | Rationale |
|-------------|------|-----------|
| Charts (bar, line, pie) | scientific-schematics | Precise data representation |
| Diagrams (flow, structure) | scientific-schematics | Clear technical layouts |
| Matrices (2x2, positioning) | scientific-schematics | Strategic frameworks |
| Timelines | scientific-schematics | Sequential information |
| Infographics | generate-image | Creative visual synthesis |
| Conceptual illustrations | generate-image | Abstract concepts |

---

## Visual Naming Convention

### Core Visuals (Generate First)
```
figures/
├── 01_market_growth_trajectory.png      # PRIORITY 1
├── 02_tam_sam_som.png                   # PRIORITY 2
├── 03_porters_five_forces.png           # PRIORITY 3
├── 04_competitive_positioning.png       # PRIORITY 4
├── 05_risk_heatmap.png                  # PRIORITY 5
└── 06_exec_summary_infographic.png      # PRIORITY 6 (optional)
```

### Extended Visuals (Generate as Needed)
```
figures/
├── 07_industry_ecosystem.png
├── 08_regional_breakdown.png
├── 09_segment_growth.png
├── 10_driver_impact_matrix.png
├── 11_pestle_analysis.png
├── 12_trends_timeline.png
├── 13_market_share.png
├── 14_strategic_groups.png
├── 15_customer_segments.png
├── 16_segment_attractiveness.png
├── 17_customer_journey.png
├── 18_technology_roadmap.png
├── 19_innovation_curve.png
├── 20_regulatory_timeline.png
├── 21_risk_mitigation.png
├── 22_opportunity_matrix.png
├── 23_recommendation_priority.png
├── 24_implementation_timeline.png
├── 25_milestone_tracker.png
├── 26_financial_projections.png
└── 27_scenario_analysis.png
```

---

## CORE VISUALS (Priority 1-6) - Generate These First

### Priority 1: Market Growth Trajectory Chart

**Tool:** scientific-schematics

**Purpose:** Foundation visual showing historical and projected market size

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart market growth 2020 to 2034. Historical bars 2020-2024 in dark blue, projected bars 2025-2034 in light blue. Y-axis billions USD, X-axis years. CAGR annotation. Data labels on each bar. Vertical dashed line between 2024 and 2025. Title: Market Growth Trajectory. Professional white background" \
  -o figures/01_market_growth_trajectory.png --doc-type report
```

---

### Priority 2: TAM/SAM/SOM Diagram

**Tool:** scientific-schematics

**Purpose:** Market opportunity sizing visualization

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles. Outer circle TAM Total Addressable Market. Middle circle SAM Serviceable Addressable Market. Inner circle SOM Serviceable Obtainable Market. Each labeled with acronym, full name, placeholder for dollar value. Arrows pointing to each with descriptions. Blue gradient darkest outer to lightest inner. White background professional appearance" \
  -o figures/02_tam_sam_som.png --doc-type report
```

---

### Priority 3: Porter's Five Forces Diagram

**Tool:** scientific-schematics

**Purpose:** Competitive dynamics framework

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram. Center box Competitive Rivalry with rating. Four surrounding boxes with arrows to center: Top Threat of New Entrants, Left Bargaining Power Suppliers, Right Bargaining Power Buyers, Bottom Threat of Substitutes. Color code HIGH red, MEDIUM yellow, LOW green. Include 2-3 key factors per box. Professional appearance" \
  -o figures/03_porters_five_forces.png --doc-type report
```

---

### Priority 4: Competitive Positioning Matrix

**Tool:** scientific-schematics

**Purpose:** Strategic positioning of key market players

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix. X-axis Market Focus Niche to Broad. Y-axis Solution Approach Product to Platform. Quadrants: Upper-right Platform Leaders, Upper-left Niche Platforms, Lower-right Product Leaders, Lower-left Specialists. Plot 8-10 company circles with names. Circle size = market share. Legend for sizes. Professional appearance" \
  -o figures/04_competitive_positioning.png --doc-type report
```

---

### Priority 5: Risk Heatmap

**Tool:** scientific-schematics

**Purpose:** Visual risk assessment matrix

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact Low Medium High Critical. Y-axis Probability Unlikely Possible Likely Very Likely. Cell colors: Green low risk, Yellow medium, Orange high, Red critical. Plot 10-12 numbered risks R1 R2 etc as labeled points. Legend with risk names. Professional clear" \
  -o figures/05_risk_heatmap.png --doc-type report
```

---

### Priority 6: Executive Summary Infographic (Optional)

**Tool:** generate-image

**Purpose:** High-level visual synthesis for cover or executive summary

**Command:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Executive summary infographic for market research, one page layout, central large metric showing market size, four quadrants showing growth rate key players top segments regional leaders, modern flat design, professional blue and green color scheme, clean white background, corporate business aesthetic" \
  --output figures/06_exec_summary_infographic.png
```

---

## EXTENDED VISUALS - Generate During Writing as Needed

The following visuals can be generated when writing specific chapters that require them.

---

## Front Matter Visuals

### Extended: Cover Image / Hero Visual

**Tool:** generate-image

**Prompt:**
```
Professional executive summary infographic for [MARKET NAME] market research report. 
Modern data visualization style showing key metrics: market size, growth rate, key players.
Blue and green color scheme matching corporate design.
Clean minimalist design with icons.
High resolution, publication quality.
No text overlays, image only.
```

**Command:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for [MARKET] market research report, modern data visualization style, key metrics display, blue and green corporate color scheme, clean minimalist design with icons, high resolution publication quality" \
  --output figures/01_cover_image.png
```

### 2. Executive Summary Infographic

**Tool:** generate-image

**Prompt:**
```
One-page executive summary infographic showing:
- Large central metric: $XX billion market size
- Four quadrants with: Growth Rate, Key Players, Top Segments, Regional Leaders
- Modern flat design with data visualization elements
- Professional blue (#003366) and green (#008060) color scheme
- Clean white background
- Business/corporate aesthetic
```

**Command:**
```bash
python skills/generate-image/scripts/generate_image.py \
  "Executive summary infographic for market research, one page layout, central large metric showing market size, four quadrants showing growth rate key players top segments regional leaders, modern flat design, professional blue and green color scheme, clean white background, corporate business aesthetic" \
  --output figures/02_exec_summary_infographic.png
```

---

## Chapter 1: Market Overview Visuals

### 3. Industry Ecosystem Diagram

**Tool:** scientific-schematics

**Prompt:**
```
Industry ecosystem value chain diagram showing horizontal flow from left to right:
[Suppliers/Inputs] → [Manufacturers/Processors] → [Distributors/Channels] → [End Users/Customers]

At each stage, show 3-4 example player types in smaller boxes below.
Use arrows to show product/service flow (solid) and money flow (dashed).
Include regulatory bodies as oversight layer above the chain.
Professional blue color scheme.
Clean white background.
All text clearly readable.
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Industry ecosystem value chain diagram. Horizontal flow left to right: Suppliers box → Manufacturers box → Distributors box → End Users box. Below each main box show 3-4 smaller boxes with example player types. Solid arrows for product flow, dashed arrows for money flow. Regulatory oversight layer above. Professional blue color scheme, white background, clear labels" \
  -o figures/03_industry_ecosystem.png --doc-type report
```

### 4. Market Structure Diagram

**Tool:** scientific-schematics

**Prompt:**
```
Market structure diagram showing concentric rectangles:
- Center: Core Market (labeled with market name)
- Second layer: Adjacent Markets (labeled with 4-5 adjacent market names)
- Third layer: Enabling Technologies (labeled with key technologies)
- Outer layer: Regulatory Framework

Use different shades of blue for each layer.
Include small icons or labels for key elements.
Professional appearance.
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Market structure diagram with concentric rectangles. Center: Core Market [MARKET NAME]. Second layer: Adjacent Markets with 4-5 labels. Third layer: Enabling Technologies with key tech labels. Outer layer: Regulatory Framework. Different blue shades for each layer, professional appearance, clear labels" \
  -o figures/03b_market_structure.png --doc-type report
```

---

## Chapter 2: Market Size & Growth Visuals

### 5. Market Growth Trajectory Chart

**Tool:** scientific-schematics

**Prompt:**
```
Bar chart showing market growth from 2020 to 2034.
Historical years (2020-2024): Dark blue bars
Projected years (2025-2034): Light blue bars
Y-axis: Market size in billions USD (0 to $XXX)
X-axis: Years
Include CAGR annotation showing "XX.X% CAGR (2024-2034)"
Data labels on top of each bar
Vertical dashed line separating historical from projected
Title: "[MARKET NAME] Market Growth Trajectory"
Professional appearance, white background
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart market growth 2020 to 2034. Historical bars 2020-2024 in dark blue, projected bars 2025-2034 in light blue. Y-axis billions USD, X-axis years. CAGR annotation XX.X% (2024-2034). Data labels on each bar. Vertical dashed line between 2024 and 2025. Title: Market Growth Trajectory. Professional white background" \
  -o figures/04_market_growth_trajectory.png --doc-type report
```

### 6. TAM/SAM/SOM Diagram

**Tool:** scientific-schematics

**Prompt:**
```
TAM SAM SOM concentric circles diagram:
- Outer circle: TAM (Total Addressable Market) - $XXX billion
- Middle circle: SAM (Serviceable Addressable Market) - $XX billion  
- Inner circle: SOM (Serviceable Obtainable Market) - $X billion

Each circle labeled with:
- Acronym in bold
- Full name
- Dollar value

Arrows pointing to each circle with descriptions
Use blue color gradient (darkest for TAM, lightest for SOM)
Professional appearance
White background
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles. Outer circle TAM Total Addressable Market [VALUE]B. Middle circle SAM Serviceable Addressable Market [VALUE]B. Inner circle SOM Serviceable Obtainable Market [VALUE]B. Each labeled with acronym, full name, dollar value. Arrows pointing to each with descriptions. Blue gradient darkest outer to lightest inner. White background professional" \
  -o figures/05_tam_sam_som.png --doc-type report
```

### 7. Regional Market Breakdown

**Tool:** scientific-schematics

**Prompt:**
```
Pie chart OR treemap showing regional market breakdown:
- North America: XX% ($X.XB) - Dark blue
- Europe: XX% ($X.XB) - Medium blue
- Asia-Pacific: XX% ($X.XB) - Teal
- Latin America: X% ($X.XB) - Light blue
- Middle East & Africa: X% ($X.XB) - Gray blue

Include both percentage and dollar value for each region
Legend on right side
Title: "Market Size by Region (2024)"
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Pie chart regional market breakdown. North America XX% dark blue, Europe XX% medium blue, Asia-Pacific XX% teal, Latin America XX% light blue, Middle East Africa XX% gray blue. Show percentage and dollar value for each slice. Legend on right. Title: Market Size by Region 2024. Professional appearance" \
  -o figures/06_regional_breakdown.png --doc-type report
```

### 8. Segment Growth Comparison

**Tool:** scientific-schematics

**Prompt:**
```
Horizontal bar chart comparing segment growth rates:
- Y-axis: Segment names (5-7 segments)
- X-axis: CAGR percentage (0% to 30%)
- Bars colored by growth rate: Green (highest) to blue (lowest)
- Data labels showing exact percentage on each bar
- Sort segments from highest to lowest growth
- Title: "Segment Growth Rate Comparison (CAGR 2024-2034)"
- Include average line or marker
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Horizontal bar chart segment growth comparison. Y-axis 5-7 segment names, X-axis CAGR percentage 0-30%. Bars colored green highest to blue lowest. Data labels with exact percentages. Sorted highest to lowest. Title: Segment Growth Rate Comparison CAGR 2024-2034. Include market average line" \
  -o figures/07_segment_growth.png --doc-type report
```

---

## Chapter 3: Industry Drivers & Trends Visuals

### 9. Driver Impact Matrix

**Tool:** scientific-schematics

**Prompt:**
```
2x2 matrix for market driver assessment:
- X-axis: Impact on Market (Low → High)
- Y-axis: Probability of Occurrence (Low → High)
- Upper-right quadrant: "CRITICAL DRIVERS" (red/orange background)
- Upper-left quadrant: "MONITOR" (yellow background)
- Lower-right quadrant: "WATCH CAREFULLY" (yellow background)
- Lower-left quadrant: "LOWER PRIORITY" (green background)

Plot 8-10 drivers as labeled circles:
- Size of circle represents current market impact
- Position based on ratings

Include legend for circle sizes
Professional appearance with clear labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 matrix driver impact assessment. X-axis Impact Low to High, Y-axis Probability Low to High. Quadrants: Upper-right CRITICAL DRIVERS red, Upper-left MONITOR yellow, Lower-right WATCH CAREFULLY yellow, Lower-left LOWER PRIORITY green. Plot 8-10 labeled driver circles at appropriate positions. Circle size indicates current impact. Professional clear labels" \
  -o figures/08_driver_impact_matrix.png --doc-type report
```

### 10. PESTLE Analysis Diagram

**Tool:** scientific-schematics

**Prompt:**
```
PESTLE analysis hexagonal diagram:
- Center hexagon: "[MARKET NAME]" 
- Six surrounding hexagons connected to center:
  - Political (red/orange)
  - Economic (blue)
  - Social (green)
  - Technological (orange)
  - Legal (purple)
  - Environmental (teal)

Each outer hexagon contains 2-3 key bullet points
Connecting lines between center and outer hexagons
Professional appearance
Clear, readable text in each hexagon
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "PESTLE hexagonal diagram. Center hexagon labeled MARKET. Six surrounding hexagons: Political red, Economic blue, Social green, Technological orange, Legal purple, Environmental teal. Each outer hexagon has 2-3 bullet points of key factors. Lines connecting center to each. Professional appearance clear readable text" \
  -o figures/09_pestle_analysis.png --doc-type report
```

### 11. Industry Trends Timeline

**Tool:** scientific-schematics

**Prompt:**
```
Horizontal timeline showing emerging trends from 2024 to 2030:
- Main horizontal axis with year markers
- Plot 6-8 trends at different points on timeline
- Each trend shown with:
  - Icon or symbol
  - Trend name
  - Brief 3-5 word description below

Color-code by trend category:
- Technology trends: Blue
- Market trends: Green
- Regulatory trends: Orange

Include "Current" marker at 2024
Professional appearance with clear labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Horizontal timeline 2024 to 2030. Plot 6-8 emerging trends at different years. Each trend with icon, name, brief description. Color code: Technology trends blue, Market trends green, Regulatory trends orange. Current marker at 2024. Professional clear labels" \
  -o figures/10_trends_timeline.png --doc-type report
```

---

## Chapter 4: Competitive Landscape Visuals

### 12. Porter's Five Forces Diagram

**Tool:** scientific-schematics

**Prompt:**
```
Porter's Five Forces diagram with center and four surrounding boxes:

Center box: "Competitive Rivalry" with rating [HIGH/MEDIUM/LOW]

Surrounding boxes connected by arrows:
- Top: "Threat of New Entrants" [RATING]
- Left: "Bargaining Power of Suppliers" [RATING]
- Right: "Bargaining Power of Buyers" [RATING]
- Bottom: "Threat of Substitutes" [RATING]

Color-code ratings:
- HIGH: Red/orange background
- MEDIUM: Yellow background
- LOW: Green background

Arrows pointing toward center
Include key factors as bullet points in each box
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram. Center box Competitive Rivalry [RATING]. Four surrounding boxes with arrows to center: Top Threat of New Entrants [RATING], Left Bargaining Power Suppliers [RATING], Right Bargaining Power Buyers [RATING], Bottom Threat of Substitutes [RATING]. Color code HIGH red, MEDIUM yellow, LOW green. Include 2-3 key factors per box. Professional appearance" \
  -o figures/11_porters_five_forces.png --doc-type report
```

### 13. Market Share Chart

**Tool:** scientific-schematics

**Prompt:**
```
Pie chart or donut chart showing market share:
- Top 10 companies with distinct colors
- Company A: XX% (largest slice, dark blue)
- Company B: XX% (medium blue)
- [Continue for top 10]
- Others: XX% (gray)

Include:
- Percentage labels on each slice
- Company names in legend or on slices
- Total market size annotation
- Title: "Market Share by Company (2024)"

Professional appearance
Colorblind-friendly palette
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Pie chart market share top 10 companies. Company A XX% dark blue, Company B XX% medium blue, [list companies and shares], Others XX% gray. Percentage labels on slices. Legend with company names. Total market size annotation. Title: Market Share by Company 2024. Colorblind-friendly colors professional" \
  -o figures/12_market_share.png --doc-type report
```

### 14. Competitive Positioning Matrix

**Tool:** scientific-schematics

**Prompt:**
```
2x2 competitive positioning matrix:
- X-axis: Market Focus (Niche ← → Broad)
- Y-axis: Solution Approach (Product ← → Platform)

Quadrant labels:
- Upper-right: "Platform Leaders"
- Upper-left: "Niche Platforms"
- Lower-right: "Product Leaders"
- Lower-left: "Specialists"

Plot 8-10 companies as labeled circles:
- Circle size represents market share
- Position based on strategy

Include legend for circle sizes
Company name labels
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix. X-axis Market Focus Niche to Broad. Y-axis Solution Approach Product to Platform. Quadrants: Upper-right Platform Leaders, Upper-left Niche Platforms, Lower-right Product Leaders, Lower-left Specialists. Plot 8-10 company circles with names. Circle size = market share. Legend for sizes. Professional" \
  -o figures/13_competitive_positioning.png --doc-type report
```

### 15. Strategic Group Map

**Tool:** scientific-schematics

**Prompt:**
```
Strategic group map showing competitor clusters:
- X-axis: Geographic Scope (Regional ← → Global)
- Y-axis: Product Breadth (Narrow ← → Broad)

Draw 4-5 oval "bubbles" representing strategic groups:
- Each bubble contains 2-4 company names
- Bubble size represents collective market share of group
- Different colors for each strategic group

Label each strategic group:
- "Global Generalists"
- "Regional Specialists"
- "Focused Innovators"
- etc.

Professional appearance
Clear company name labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Strategic group map. X-axis Geographic Scope Regional to Global. Y-axis Product Breadth Narrow to Broad. Draw 4-5 oval bubbles for strategic groups. Each bubble contains 2-4 company names. Bubble size = collective market share. Label groups: Global Generalists, Regional Specialists, Focused Innovators etc. Different colors per group. Professional clear labels" \
  -o figures/14_strategic_groups.png --doc-type report
```

---

## Chapter 5: Customer Analysis Visuals

### 16. Customer Segmentation Breakdown

**Tool:** scientific-schematics

**Prompt:**
```
Treemap or pie chart showing customer segments:
- Large Enterprise: XX% (dark blue)
- Mid-Market: XX% (medium blue)
- SMB: XX% (light blue)
- Consumer: XX% (teal)

Size represents market share
Include for each segment:
- Segment name
- Percentage
- Dollar value

Title: "Customer Segmentation by Market Share"
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Treemap customer segmentation. Large Enterprise XX% dark blue, Mid-Market XX% medium blue, SMB XX% light blue, Consumer XX% teal. Each segment shows name percentage dollar value. Title: Customer Segmentation by Market Share. Professional appearance" \
  -o figures/15_customer_segments.png --doc-type report
```

### 17. Segment Attractiveness Matrix

**Tool:** scientific-schematics

**Prompt:**
```
2x2 segment attractiveness matrix:
- X-axis: Segment Size (Small ← → Large)
- Y-axis: Growth Rate (Low ← → High)

Quadrant labels and actions:
- Upper-right: "PRIORITY - Invest Heavily"
- Upper-left: "INVEST TO GROW"
- Lower-right: "HARVEST"
- Lower-left: "DEPRIORITIZE"

Plot customer segments as labeled circles
Circle size represents profitability
Different colors for each segment
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 segment attractiveness matrix. X-axis Segment Size Small to Large. Y-axis Growth Rate Low to High. Quadrants: Upper-right PRIORITY Invest Heavily, Upper-left INVEST TO GROW, Lower-right HARVEST, Lower-left DEPRIORITIZE. Plot customer segments as circles. Circle size = profitability. Different colors. Professional" \
  -o figures/16_segment_attractiveness.png --doc-type report
```

### 18. Customer Journey Map

**Tool:** scientific-schematics

**Prompt:**
```
Customer journey horizontal flowchart showing 5-6 stages:
Awareness → Consideration → Decision → Implementation → Usage → Advocacy

For each stage, show three rows:
1. Key Activities (what customer does)
2. Pain Points (challenges faced)
3. Touchpoints (how they interact)

Use icons for each stage
Color gradient from light to dark as journey progresses
Professional appearance
Clear labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Customer journey horizontal flowchart. 5 stages left to right: Awareness, Consideration, Decision, Implementation, Usage, Advocacy. Each stage shows Key Activities, Pain Points, Touchpoints in rows below. Icons for each stage. Color gradient light to dark. Professional clear labels" \
  -o figures/17_customer_journey.png --doc-type report
```

---

## Chapter 6: Technology Landscape Visuals

### 19. Technology Roadmap

**Tool:** scientific-schematics

**Prompt:**
```
Technology roadmap timeline from 2024 to 2030:
Three parallel horizontal tracks:
1. Core Technology (blue) - current foundation
2. Emerging Technology (green) - developing capabilities
3. Enabling Technology (orange) - infrastructure/support

Each track shows milestones and technology introductions as markers
Vertical lines connect related technologies across tracks
Timeline markers for each year
Technology names labeled at introduction points
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Technology roadmap 2024 to 2030. Three parallel horizontal tracks: Core Technology blue, Emerging Technology green, Enabling Technology orange. Milestones and tech introductions marked on each track. Vertical lines connect related tech. Year markers. Technology names labeled. Professional appearance" \
  -o figures/18_technology_roadmap.png --doc-type report
```

### 20. Innovation/Adoption Curve

**Tool:** scientific-schematics

**Prompt:**
```
Gartner Hype Cycle or Technology Adoption Curve:
Five phases from left to right:
1. Innovation Trigger (rising)
2. Peak of Inflated Expectations (peak)
3. Trough of Disillusionment (bottom)
4. Slope of Enlightenment (rising)
5. Plateau of Productivity (stable)

Plot 6-8 technologies at different positions on the curve
Each technology labeled with name
Color-code by technology category
Professional appearance
Clear axis labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Gartner Hype Cycle curve. Five phases: Innovation Trigger rising, Peak of Inflated Expectations at top, Trough of Disillusionment at bottom, Slope of Enlightenment rising, Plateau of Productivity stable. Plot 6-8 technologies on curve with labels. Color by category. Professional clear labels" \
  -o figures/19_innovation_curve.png --doc-type report
```

---

## Chapter 7: Regulatory Environment Visuals

### 21. Regulatory Timeline

**Tool:** scientific-schematics

**Prompt:**
```
Regulatory timeline from 2020 to 2028:
Horizontal timeline with year markers
Mark key regulatory events:
- Past regulations (dark blue markers, solid)
- Current regulations (green marker at current year)
- Upcoming regulations (light blue markers, dashed)

Each marker shows:
- Regulation name
- Effective date
- Brief description (5-7 words)

Vertical "NOW" line at current year (2024)
Group by region if multiple jurisdictions
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Regulatory timeline 2020 to 2028. Past regulations dark blue solid markers, current green marker, upcoming light blue dashed. Each shows regulation name, date, brief description. Vertical NOW line at 2024. Professional appearance clear labels" \
  -o figures/20_regulatory_timeline.png --doc-type report
```

---

## Chapter 8: Risk Analysis Visuals

### 22. Risk Heatmap

**Tool:** scientific-schematics

**Prompt:**
```
Risk assessment heatmap/matrix:
- X-axis: Impact (Low → Medium → High → Critical)
- Y-axis: Probability (Unlikely → Possible → Likely → Very Likely)

Color gradient for cells:
- Green: Low risk (low probability, low impact)
- Yellow: Medium risk
- Orange: High risk
- Red: Critical risk (high probability, high impact)

Plot 10-12 risks as labeled points/circles in appropriate cells
Risk labels should be clearly readable
Include risk numbers (R1, R2, etc.)
Legend linking numbers to risk names
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact Low Medium High Critical. Y-axis Probability Unlikely Possible Likely Very Likely. Cell colors: Green low risk, Yellow medium, Orange high, Red critical. Plot 10-12 numbered risks R1 R2 etc as labeled points. Legend with risk names. Professional clear" \
  -o figures/21_risk_heatmap.png --doc-type report
```

### 23. Risk Mitigation Framework

**Tool:** scientific-schematics

**Prompt:**
```
Risk mitigation diagram showing risks and their mitigations:
Left column: Risks (in red/orange boxes)
Right column: Mitigation Strategies (in green/blue boxes)

Connect each risk to its mitigation(s) with arrows
Group risks by category (Market, Regulatory, Technology, etc.)
Include both prevention and response strategies

Risk severity indicated by box color intensity
Professional appearance
Clear labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk mitigation diagram. Left column risks in orange/red boxes. Right column mitigation strategies in green/blue boxes. Arrows connecting risks to mitigations. Group by category. Risk severity by color intensity. Include prevention and response. Professional clear labels" \
  -o figures/22_risk_mitigation.png --doc-type report
```

---

## Chapter 9: Strategic Recommendations Visuals

### 24. Opportunity Matrix

**Tool:** scientific-schematics

**Prompt:**
```
2x2 opportunity assessment matrix:
- X-axis: Market Attractiveness (Low ← → High)
- Y-axis: Ability to Win (Low ← → High)

Quadrant labels and strategies:
- Upper-right: "PURSUE AGGRESSIVELY" (green)
- Upper-left: "BUILD CAPABILITIES" (yellow)
- Lower-right: "SELECTIVE INVESTMENT" (yellow)
- Lower-left: "AVOID/DIVEST" (red)

Plot 6-8 opportunities as labeled circles
Circle size represents opportunity size ($)
Include opportunity names
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 opportunity matrix. X-axis Market Attractiveness Low to High. Y-axis Ability to Win Low to High. Quadrants: Upper-right PURSUE AGGRESSIVELY green, Upper-left BUILD CAPABILITIES yellow, Lower-right SELECTIVE INVESTMENT yellow, Lower-left AVOID red. Plot 6-8 opportunity circles with labels. Size = opportunity value. Professional" \
  -o figures/23_opportunity_matrix.png --doc-type report
```

### 25. Recommendation Priority Matrix

**Tool:** scientific-schematics

**Prompt:**
```
2x2 priority matrix for recommendations:
- X-axis: Effort/Investment (Low ← → High)
- Y-axis: Impact/Value (Low ← → High)

Quadrant labels:
- Upper-left: "QUICK WINS" (green) - Do First
- Upper-right: "MAJOR PROJECTS" (blue) - Plan Carefully
- Lower-left: "FILL-INS" (gray) - Do If Time
- Lower-right: "THANKLESS TASKS" (red) - Avoid

Plot 6-8 recommendations as labeled points
Number recommendations by priority
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 priority matrix. X-axis Effort Low to High. Y-axis Impact Low to High. Quadrants: Upper-left QUICK WINS green Do First, Upper-right MAJOR PROJECTS blue Plan Carefully, Lower-left FILL-INS gray Do If Time, Lower-right THANKLESS TASKS red Avoid. Plot 6-8 numbered recommendations. Professional" \
  -o figures/24_recommendation_priority.png --doc-type report
```

---

## Chapter 10: Implementation Roadmap Visuals

### 26. Implementation Timeline/Gantt

**Tool:** scientific-schematics

**Prompt:**
```
Gantt chart style implementation timeline over 24 months:
Four phases shown as horizontal bars:
- Phase 1: Foundation (Months 1-6) - Dark blue
- Phase 2: Build (Months 4-12) - Medium blue
- Phase 3: Scale (Months 10-18) - Teal
- Phase 4: Optimize (Months 16-24) - Light blue

Phases overlap as shown in dates
Key milestones marked as diamonds on timeline
Month markers on X-axis
Phase names on Y-axis
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Gantt chart implementation 24 months. Phase 1 Foundation months 1-6 dark blue. Phase 2 Build months 4-12 medium blue. Phase 3 Scale months 10-18 teal. Phase 4 Optimize months 16-24 light blue. Overlapping bars. Key milestones as diamonds. Month markers X-axis. Professional" \
  -o figures/25_implementation_timeline.png --doc-type report
```

### 27. Milestone Tracker

**Tool:** scientific-schematics

**Prompt:**
```
Milestone tracker showing 8-10 key milestones on horizontal timeline:
Each milestone shows:
- Date/Month
- Milestone name
- Status indicator:
  - Completed: Green checkmark ✓
  - In Progress: Yellow circle ○
  - Upcoming: Gray circle ○

Group milestones by phase
Connect milestones with timeline line
Include phase labels above timeline
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Milestone tracker horizontal timeline 8-10 milestones. Each shows date, name, status: Completed green check, In Progress yellow circle, Upcoming gray circle. Group by phase. Phase labels above. Connected timeline line. Professional" \
  -o figures/26_milestone_tracker.png --doc-type report
```

---

## Chapter 11: Investment Thesis Visuals

### 28. Financial Projections Chart

**Tool:** scientific-schematics

**Prompt:**
```
Combined bar and line chart showing 5-year financial projections:
- Bar chart: Revenue by year (primary Y-axis, in $M)
- Line chart: Growth rate overlay (secondary Y-axis, in %)

Three scenarios shown:
- Conservative: Gray bars
- Base Case: Blue bars
- Optimistic: Green bars

X-axis: Year 1 through Year 5
Include data labels on bars
Legend for scenarios and growth line
Title: "Financial Projections (5-Year)"
Professional appearance
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Combined bar and line chart 5-year projections. Bar chart revenue primary Y-axis dollars. Line chart growth rate secondary Y-axis percent. Three scenarios: Conservative gray, Base Case blue, Optimistic green. X-axis Year 1-5. Data labels. Legend. Title Financial Projections 5-Year. Professional" \
  -o figures/27_financial_projections.png --doc-type report
```

### 29. Scenario Analysis Comparison

**Tool:** scientific-schematics

**Prompt:**
```
Grouped bar chart comparing three scenarios across key metrics:
X-axis: Metrics (Revenue Y5, EBITDA Y5, Market Share, ROI)
Y-axis: Value (scale appropriate for each metric)

Three bars per metric:
- Conservative: Gray
- Base Case: Blue
- Optimistic: Green

Data labels on each bar
Legend for scenarios
Title: "Scenario Analysis Comparison"
Professional appearance
Clear metric labels
```

**Command:**
```bash
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Grouped bar chart scenario comparison. X-axis metrics: Revenue Y5, EBITDA Y5, Market Share, ROI. Three bars per metric: Conservative gray, Base Case blue, Optimistic green. Data labels. Legend. Title Scenario Analysis Comparison. Professional clear labels" \
  -o figures/28_scenario_analysis.png --doc-type report
```

---

## Batch Generation Script

For convenience, use the `generate_market_visuals.py` script to batch generate visuals:

```bash
# Generate core 5-6 visuals only (recommended for starting reports)
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "Electric Vehicle Charging Infrastructure" \
  --output-dir figures/

# Generate all 27 visuals (core + extended, for comprehensive coverage)
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "Electric Vehicle Charging Infrastructure" \
  --output-dir figures/ \
  --all

# Skip already generated files
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "Your Market" \
  --output-dir figures/ \
  --skip-existing
```

**Default behavior**: Generates only the 5-6 core priority visuals. Use `--all` flag if you need comprehensive visual coverage for all sections.

---

## Quality Checklist

Before including visuals in the report, verify:

- [ ] All text is readable at intended size
- [ ] Colors are consistent across all visuals
- [ ] Color scheme is colorblind-friendly
- [ ] Data labels are accurate
- [ ] Legends are clear and complete
- [ ] Titles are descriptive
- [ ] Sources are noted where applicable
- [ ] Resolution is 300 DPI or higher
- [ ] File format is PNG
- [ ] Naming convention is followed
