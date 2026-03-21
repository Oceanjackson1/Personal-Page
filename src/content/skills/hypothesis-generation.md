---
title: "Hypothesis Generation"
description: "Structured hypothesis formulation from observations. Use when you have experimental observations or data and need to formulate testable hypotheses with predictions, propose mechanisms, and design experiments to test them. Follows scientific method..."
category: "research"
source: "community"
author: "Community"
tags: ["hypothesis", "generation"]
date: 2026-03-20
---

# Scientific Hypothesis Generation

## Overview

Hypothesis generation is a systematic process for developing testable explanations. Formulate evidence-based hypotheses from observations, design experiments, explore competing explanations, and develop predictions. Apply this skill for scientific inquiry across domains.

## When to Use This Skill

This skill should be used when:
- Developing hypotheses from observations or preliminary data
- Designing experiments to test scientific questions
- Exploring competing explanations for phenomena
- Formulating testable predictions for research
- Conducting literature-based hypothesis generation
- Planning mechanistic studies across scientific domains

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every hypothesis generation report MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Hypothesis reports without visual elements are incomplete. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., hypothesis framework showing competing explanations)
2. Prefer 2-3 figures for comprehensive reports (mechanistic pathway, experimental design flowchart, prediction decision tree)

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Hypothesis framework diagrams showing competing explanations
- Experimental design flowcharts
- Mechanistic pathway diagrams
- Prediction decision trees
- Causal relationship diagrams
- Theoretical model visualizations
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Workflow

Follow this systematic process to generate robust scientific hypotheses:

### 1. Understand the Phenomenon

Start by clarifying the observation, question, or phenomenon that requires explanation:

- Identify the core observation or pattern that needs explanation
- Define the scope and boundaries of the phenomenon
- Note any constraints or specific contexts
- Clarify what is already known vs. what is uncertain
- Identify the relevant scientific domain(s)

### 2. Conduct Comprehensive Literature Search

Search existing scientific literature to ground hypotheses in current evidence. Use both PubMed (for biomedical topics) and general web search (for broader scientific domains):

**For biomedical topics:**
- Use WebFetch with PubMed URLs to access relevant literature
- Search for recent reviews, meta-analyses, and primary research
- Look for similar phenomena, related mechanisms, or analogous systems

**For all scientific domains:**
- Use WebSearch to find recent papers, preprints, and reviews
- Search for established theories, mechanisms, or frameworks
- Identify gaps in current understanding

**Search strategy:**
- Begin with broad searches to understand the landscape
- Narrow to specific mechanisms, pathways, or theories
- Look for contradictory findings or unresolved debates
- Consult `references/literature_search_strategies.md` for detailed search techniques

### 3. Synthesize Existing Evidence

Analyze and integrate findings from literature search:

- Summarize current understanding of the phenomenon
- Identify established mechanisms or theories that may apply
- Note conflicting evidence or alternative viewpoints
- Recognize gaps, limitations, or unanswered questions
- Identify analogies from related systems or domains

### 4. Generate Competing Hypotheses

Develop 3-5 distinct hypotheses that could explain the phenomenon. Each hypothesis should:

- Provide a mechanistic explanation (not just description)
- Be distinguishable from other hypotheses
- Draw on evidence from the literature synthesis
- Consider different levels of explanation (molecular, cellular, systemic, population, etc.)

**Strategies for generating hypotheses:**
- Apply known mechanisms from analogous systems
- Consider multiple causative pathways
- Explore different scales of explanation
- Question assumptions in existing explanations
- Combine mechanisms in novel ways

### 5. Evaluate Hypothesis Quality

Assess each hypothesis against established quality criteria from `references/hypothesis_quality_criteria.md`:

**Testability:** Can the hypothesis be empirically tested?
**Falsifiability:** What observations would disprove it?
**Parsimony:** Is it the simplest explanation that fits the evidence?
**Explanatory Power:** How much of the phenomenon does it explain?
**Scope:** What range of observations does it cover?
**Consistency:** Does it align with established principles?
**Novelty:** Does it offer new insights beyond existing explanations?

Explicitly note the strengths and weaknesses of each hypothesis.

### 6. Design Experimental Tests

For each viable hypothesis, propose specific experiments or studies to test it. Consult `references/experimental_design_patterns.md` for common approaches:

**Experimental design elements:**
- What would be measured or observed?
- What comparisons or controls are needed?
- What methods or techniques would be used?
- What sample sizes or statistical approaches are appropriate?
- What are potential confounds and how to address them?

**Consider multiple approaches:**
- Laboratory experiments (in vitro, in vivo, computational)
- Observational studies (cross-sectional, longitudinal, case-control)
- Clinical trials (if applicable)
- Natural experiments or quasi-experimental designs

### 7. Formulate Testable Predictions

For each hypothesis, generate specific, quantitative predictions:

- State what should be observed if the hypothesis is correct
- Specify expected direction and magnitude of effects when possible
- Identify conditions under which predictions should hold
- Distinguish predictions between competing hypotheses
- Note predictions that would falsify the hypothesis

### 8. Present Structured Output

Generate a professional LaTeX document using the template in `assets/hypothesis_report_template.tex`. The report should be well-formatted with colored boxes for visual organization and divided into a concise main text with comprehensive appendices.

**Document Structure:**

**Main Text (Maximum 4 pages):**
1. **Executive Summary** - Brief overview in summary box (0.5-1 page)
2. **Competing Hypotheses** - Each hypothesis in its own colored box with brief mechanistic explanation and key evidence (2-2.5 pages for 3-5 hypotheses)
   - **IMPORTANT:** Use `\newpage` before each hypothesis box to prevent content overflow
   - Each box should be ≤0.6 pages maximum
3. **Testable Predictions** - Key predictions in amber boxes (0.5-1 page)
4. **Critical Comparisons** - Priority comparison boxes (0.5-1 page)

Keep main text highly concise - only the most essential information. All details go to appendices.

**Page Break Strategy:**
- Always use `\newpage` before hypothesis boxes to ensure they start on fresh pages
- This prevents content from overflowing off page boundaries
- LaTeX boxes (tcolorbox) do not automatically break across pages

**Appendices (Comprehensive, Detailed):**
- **Appendix A:** Comprehensive literature review with extensive citations
- **Appendix B:** Detailed experimental designs with full protocols
- **Appendix C:** Quality assessment tables and detailed evaluations
- **Appendix D:** Supplementary evidence and analogous systems

**Colored Box Usage:**

Use the custom box environments from `hypothesis_generation.sty`:

- `hypothesisbox1` through `hypothesisbox5` - For each competing hypothesis (blue, green, purple, teal, orange)
- `predictionbox` - For testable predictions (amber)
- `comparisonbox` - For critical comparisons (steel gray)
- `evidencebox` - For supporting evidence highlights (light blue)
- `summarybox` - For executive summary (blue)

**Each hypothesis box should contain (keep concise for 4-page limit):**
- **Mechanistic Explanation:** 1-2 brief paragraphs (6-10 sentences max) explaining HOW and WHY
- **Key Supporting Evidence:** 2-3 bullet points with citations (most important evidence only)
- **Core Assumptions:** 1-2 critical assumptions

All detailed explanations, additional evidence, and comprehensive discussions belong in the appendices.

**Critical Overflow Prevention:**
- Insert `\newpage` before each hypothesis box to start it on a fresh page
- Keep each complete hypothesis box to ≤0.6 pages (approximately 15-20 lines of content)
- If content exceeds this, move additional details to Appendix A
- Never let boxes overflow off page boundaries - this creates unreadable PDFs

**Citation Requirements:**

Aim for extensive citation to support all claims:
- **Main text:** 10-15 key citations for most important evidence only (keep concise for 4-page limit)
- **Appendix A:** 40-70+ comprehensive citations covering all relevant literature
- **Total target:** 50+ references in bibliography

Main text citations should be selective - cite only the most critical papers. All comprehensive citation and detailed literature discussion belongs in the appendices. Use `\citep{author2023}` for parenthetical citations.

**LaTeX Compilation:**

The template requires XeLaTeX or LuaLaTeX for proper rendering:

```bash
xelatex hypothesis_report.tex
bibtex hypothesis_report
xelatex hypothesis_report.tex
xelatex hypothesis_report.tex
```

**Required packages:** The `hypothesis_generation.sty` style package must be in the same directory or LaTeX path. It requires: tcolorbox, xcolor, fontspec, fancyhdr, titlesec, enumitem, booktabs, natbib.

**Page Overflow Prevention:**

To prevent content from overflowing on pages, follow these critical guidelines:

1. **Monitor Box Content Length:** Each hypothesis box should fit comfortably on a single page. If content exceeds ~0.7 pages, it will likely overflow.

2. **Use Strategic Page Breaks:** Insert `\newpage` before boxes that contain substantial content:
   ```latex
   \newpage
   \begin{hypothesisbox1}[Hypothesis 1: Title]
   % Long content here
   \end{hypothesisbox1}
   ```

3. **Keep Main Text Boxes Concise:** For the 4-page main text limit:
   - Each hypothesis box: Maximum 0.5-0.6 pages
   - Mechanistic explanation: 1-2 brief paragraphs only (6-10 sentences max)
   - Key evidence: 2-3 bullet points only
   - Core assumptions: 1-2 items only
   - If content is longer, move details to appendices

4. **Break Long Content:** If a hypothesis requires extensive explanation, split across main text and appendix:
   - Main text box: Brief mechanistic overview + 2-3 key evidence points
   - Appendix A: Detailed mechanism explanation, comprehensive evidence, extended discussion

5. **Test Page Boundaries:** Before each new box, consider if remaining page space is sufficient. If less than 0.6 pages remain, use `\newpage` to start the box on a fresh page.

6. **Appendix Page Management:** In appendices, use `\newpage` between major sections to avoid overflow in detailed content areas.

**Quick Reference:** See `assets/FORMATTING_GUIDE.md` for detailed examples of all box types, color schemes, and common formatting patterns.

## Quality Standards

Ensure all generated hypotheses meet these standards:

- **Evidence-based:** Grounded in existing literature with citations
- **Testable:** Include specific, measurable predictions
- **Mechanistic:** Explain how/why, not just what
- **Comprehensive:** Consider alternative explanations
- **Rigorous:** Include experimental designs to test predictions

## Resources

### references/

- `hypothesis_quality_criteria.md` - Framework for evaluating hypothesis quality (testability, falsifiability, parsimony, explanatory power, scope, consistency)
- `experimental_design_patterns.md` - Common experimental approaches across domains (RCTs, observational studies, lab experiments, computational models)
- `literature_search_strategies.md` - Effective search techniques for PubMed and general scientific sources

### assets/

- `hypothesis_generation.sty` - LaTeX style package providing colored boxes, professional formatting, and custom environments for hypothesis reports
- `hypothesis_report_template.tex` - Complete LaTeX template with main text structure and comprehensive appendix sections
- `FORMATTING_GUIDE.md` - Quick reference guide with examples of all box types, color schemes, citation practices, and troubleshooting tips

### Related Skills

When preparing hypothesis-driven research for publication, consult the **venue-templates** skill for writing style guidance:
- `venue_writing_styles.md` - Master guide comparing styles across venues
- Venue-specific guides for Nature/Science, Cell Press, medical journals, and ML/CS conferences
- `reviewer_expectations.md` - What reviewers look for when evaluating research hypotheses

---

## Reference: Experimental_Design_Patterns

# Experimental Design Patterns

## Common Approaches to Testing Scientific Hypotheses

This reference provides patterns and frameworks for designing experiments across scientific domains. Use these patterns to develop rigorous tests for generated hypotheses.

**Note on Report Structure:** When generating hypothesis reports, mention only the key experimental approach (e.g., "in vivo knockout study" or "prospective cohort design") in the main text hypothesis boxes. Include comprehensive experimental protocols with full methods, controls, sample sizes, statistical approaches, feasibility assessments, and resource requirements in **Appendix B: Detailed Experimental Designs**.

## Design Selection Framework

Choose experimental approaches based on:
- **Nature of hypothesis:** Mechanistic, causal, correlational, descriptive
- **System studied:** In vitro, in vivo, computational, observational
- **Feasibility:** Time, cost, ethics, technical capabilities
- **Evidence needed:** Proof-of-concept, causal demonstration, quantitative relationship

## Laboratory Experimental Designs

### In Vitro Experiments

**When to use:** Testing molecular, cellular, or biochemical mechanisms in controlled systems.

**Common patterns:**

#### 1. Dose-Response Studies
- **Purpose:** Establish quantitative relationship between input and effect
- **Design:** Test multiple concentrations/doses of intervention
- **Key elements:**
  - Negative control (no treatment)
  - Positive control (known effective treatment)
  - Multiple dose levels (typically 5-8 points)
  - Technical replicates (≥3 per condition)
  - Appropriate statistical analysis (curve fitting, IC50/EC50 determination)

**Example application:**
"To test if compound X inhibits enzyme Y, measure enzyme activity at 0, 1, 10, 100, 1000 nM compound X concentrations with n=3 replicates per dose."

#### 2. Gain/Loss of Function Studies
- **Purpose:** Establish causal role of specific component
- **Design:** Add (overexpression) or remove (knockout/knockdown) component
- **Key elements:**
  - Wild-type control
  - Gain-of-function condition (overexpression, constitutive activation)
  - Loss-of-function condition (knockout, knockdown, inhibition)
  - Rescue experiment (restore function to loss-of-function)
  - Measure downstream effects

**Example application:**
"Test if protein X causes phenotype Y by: (1) knocking out X and observing phenotype loss, (2) overexpressing X and observing phenotype enhancement, (3) rescuing knockout with X re-expression."

#### 3. Time-Course Studies
- **Purpose:** Understand temporal dynamics and sequence of events
- **Design:** Measure outcomes at multiple time points
- **Key elements:**
  - Time 0 baseline
  - Early time points (capture rapid changes)
  - Intermediate time points
  - Late time points (steady state)
  - Sufficient replication at each time point

**Example application:**
"Measure protein phosphorylation at 0, 5, 15, 30, 60, 120 minutes after stimulus to determine peak activation timing."

### In Vivo Experiments

**When to use:** Testing hypotheses in whole organisms to assess systemic, physiological, or behavioral effects.

**Common patterns:**

#### 4. Between-Subjects Designs
- **Purpose:** Compare different groups receiving different treatments
- **Design:** Randomly assign subjects to treatment groups
- **Key elements:**
  - Random assignment to groups
  - Appropriate sample size (power analysis)
  - Control group (vehicle, sham, or standard treatment)
  - Blinding (single or double-blind)
  - Standardized conditions across groups

**Example application:**
"Randomly assign 20 mice each to vehicle control or drug treatment groups, measure tumor size weekly for 8 weeks, with experimenters blinded to group assignment."

#### 5. Within-Subjects (Repeated Measures) Designs
- **Purpose:** Each subject serves as own control, reducing inter-subject variability
- **Design:** Same subjects measured across multiple conditions/time points
- **Key elements:**
  - Baseline measurements
  - Counterbalancing (if order effects possible)
  - Washout periods (for sequential treatments)
  - Appropriate repeated-measures statistics

**Example application:**
"Measure cognitive performance in same participants at baseline, after training intervention, and at 3-month follow-up."

#### 6. Factorial Designs
- **Purpose:** Test multiple factors and their interactions simultaneously
- **Design:** Cross all levels of multiple independent variables
- **Key elements:**
  - Clear main effects and interactions
  - Sufficient power for interaction tests
  - Full factorial or fractional factorial as appropriate

**Example application:**
"2×2 design crossing genotype (WT vs. mutant) × treatment (vehicle vs. drug) to test whether drug effect depends on genotype."

### Computational/Modeling Experiments

**When to use:** Testing hypotheses about complex systems, making predictions, or when physical experiments are infeasible.

#### 7. In Silico Simulations
- **Purpose:** Model complex systems, test theoretical predictions
- **Design:** Implement computational model and vary parameters
- **Key elements:**
  - Well-defined model with explicit assumptions
  - Parameter sensitivity analysis
  - Validation against known data
  - Prediction generation for experimental testing

**Example application:**
"Build agent-based model of disease spread, vary transmission rate and intervention timing, compare predictions to empirical epidemic data."

#### 8. Bioinformatics/Meta-Analysis
- **Purpose:** Test hypotheses using existing datasets
- **Design:** Analyze large-scale data or aggregate multiple studies
- **Key elements:**
  - Appropriate statistical corrections (multiple testing)
  - Validation in independent datasets
  - Control for confounds and batch effects
  - Clear inclusion/exclusion criteria

**Example application:**
"Test if gene X expression correlates with survival across 15 cancer datasets (n>5000 patients total), using Cox regression with clinical covariates."

## Observational Study Designs

### When Physical Manipulation is Impossible or Unethical

#### 9. Cross-Sectional Studies
- **Purpose:** Examine associations at a single time point
- **Design:** Measure variables of interest in population at one time
- **Strengths:** Fast, inexpensive, can establish prevalence
- **Limitations:** Cannot establish temporality or causation
- **Key elements:**
  - Representative sampling
  - Standardized measurements
  - Control for confounding variables
  - Appropriate statistical analysis

**Example application:**
"Survey 1000 adults to test association between diet pattern and biomarker X, controlling for age, sex, BMI, and physical activity."

#### 10. Cohort Studies (Prospective/Longitudinal)
- **Purpose:** Establish temporal relationships and potentially causal associations
- **Design:** Follow group over time, measuring exposures and outcomes
- **Strengths:** Can establish temporality, calculate incidence
- **Limitations:** Time-consuming, expensive, subject attrition
- **Key elements:**
  - Baseline exposure assessment
  - Follow-up at defined intervals
  - Minimize loss to follow-up
  - Account for time-varying confounders

**Example application:**
"Follow 5000 initially healthy individuals for 10 years, testing if baseline vitamin D levels predict cardiovascular disease incidence."

#### 11. Case-Control Studies
- **Purpose:** Efficiently study rare outcomes by comparing cases to controls
- **Design:** Identify cases with outcome, select matched controls, compare exposures
- **Strengths:** Efficient for rare diseases, relatively quick
- **Limitations:** Recall bias, selection bias, cannot calculate incidence
- **Key elements:**
  - Clear case definition
  - Appropriate control selection (matching or statistical adjustment)
  - Retrospective exposure assessment
  - Control for confounding

**Example application:**
"Compare 200 patients with rare disease X to 400 matched controls without X, testing if early-life exposure Y differs between groups."

## Clinical Trial Designs

#### 12. Randomized Controlled Trials (RCTs)
- **Purpose:** Gold standard for testing interventions in humans
- **Design:** Randomly assign participants to treatment or control
- **Key elements:**
  - Randomization (simple, block, or stratified)
  - Concealment of allocation
  - Blinding (participants, providers, assessors)
  - Intention-to-treat analysis
  - Pre-registered protocol and analysis plan

**Example application:**
"Double-blind RCT: randomly assign 300 patients to receive drug X or placebo for 12 weeks, measure primary outcome of symptom improvement."

#### 13. Crossover Trials
- **Purpose:** Each participant receives all treatments in sequence
- **Design:** Participants crossed over between treatments with washout
- **Strengths:** Reduces inter-subject variability, requires fewer participants
- **Limitations:** Order effects, requires reversible conditions, longer duration
- **Key elements:**
  - Adequate washout period
  - Randomized treatment order
  - Carryover effect assessment

**Example application:**
"Crossover trial: participants receive treatment A for 4 weeks, 2-week washout, then treatment B for 4 weeks (randomized order)."

## Advanced Design Considerations

### Sample Size and Statistical Power

**Key questions:**
- What effect size is meaningful to detect?
- What statistical test will be used?
- What alpha (significance level) and beta (power) are appropriate?
- What is expected variability in the measurement?

**General guidelines:**
- Conduct formal power analysis before experiment
- For pilot studies, n≥10 per group minimum
- For definitive studies, aim for ≥80% power
- Account for potential attrition in longitudinal studies

### Controls

**Types of controls:**
- **Negative control:** No intervention (baseline)
- **Positive control:** Known effective intervention (validates system)
- **Vehicle control:** Delivery method without active ingredient
- **Sham control:** Mimics intervention without active component (surgery, etc.)
- **Historical control:** Prior data (weakest, avoid if possible)

### Blinding

**Levels:**
- **Open-label:** No blinding (acceptable for objective measures)
- **Single-blind:** Participants blinded (reduces placebo effects)
- **Double-blind:** Participants and experimenters blinded (reduces bias in assessment)
- **Triple-blind:** Participants, experimenters, and analysts blinded (strongest)

### Replication

**Technical replicates:** Repeated measurements on same sample
- Reduce measurement error
- Typically 2-3 replicates sufficient

**Biological replicates:** Independent samples/subjects
- Address biological variability
- Critical for generalization
- Minimum: n≥3, preferably n≥5-10 per group

**Experimental replicates:** Repeat entire experiment
- Validate findings across time, equipment, operators
- Gold standard for confirming results

### Confound Control

**Strategies:**
- **Randomization:** Distribute confounds evenly across groups
- **Matching:** Pair similar subjects across conditions
- **Blocking:** Group by confound, then randomize within blocks
- **Statistical adjustment:** Measure confounds and adjust in analysis
- **Standardization:** Keep conditions constant across groups

## Selecting Appropriate Design

**Decision tree:**

1. **Can variables be manipulated?**
   - Yes → Experimental design (RCT, lab experiment)
   - No → Observational design (cohort, case-control, cross-sectional)

2. **What is the system?**
   - Cells/molecules → In vitro experiments
   - Whole organisms → In vivo experiments
   - Humans → Clinical trials or observational studies
   - Complex systems → Computational modeling

3. **What is the primary goal?**
   - Mechanism → Gain/loss of function, dose-response
   - Causation → RCT, cohort study with good controls
   - Association → Cross-sectional, case-control
   - Prediction → Modeling, machine learning
   - Temporal dynamics → Time-course, longitudinal

4. **What are the constraints?**
   - Time limited → Cross-sectional, in vitro
   - Budget limited → Computational, observational
   - Ethical concerns → Observational, in vitro
   - Rare outcome → Case-control, meta-analysis

## Integrating Multiple Approaches

Strong hypothesis testing often combines multiple designs:

**Example: Testing if microbiome affects cognitive function**
1. **Observational:** Cohort study showing association between microbiome composition and cognition
2. **Animal model:** Germ-free mice receiving microbiome transplants show cognitive changes
3. **Mechanism:** In vitro studies showing microbial metabolites affect neuronal function
4. **Clinical trial:** RCT of probiotic intervention improving cognitive scores
5. **Computational:** Model predicting which microbiome profiles should affect cognition

**Triangulation approach:**
- Each design addresses different aspects/limitations
- Convergent evidence from multiple approaches strengthens causal claims
- Start with observational/in vitro, then move to definitive causal tests

## Common Pitfalls

- Insufficient sample size (underpowered)
- Lack of appropriate controls
- Confounding variables not accounted for
- Inappropriate statistical tests
- P-hacking or multiple testing without correction
- Lack of blinding when subjective assessments involved
- Failure to replicate findings
- Not pre-registering analysis plans (clinical trials)

## Practical Application for Hypothesis Testing

When designing experiments to test hypotheses:

1. **Match design to hypothesis specifics:** Causal claims require experimental manipulation; associations can use observational designs
2. **Start simple, then elaborate:** Pilot with simple design, then add complexity
3. **Plan controls carefully:** Controls validate the system and isolate the specific effect
4. **Consider feasibility:** Balance ideal design with practical constraints
5. **Plan for multiple experiments:** Rarely does one experiment definitively test a hypothesis
6. **Pre-specify analysis:** Decide statistical tests before data collection
7. **Build in validation:** Independent replication, orthogonal methods, convergent evidence

---

## Reference: Hypothesis_Quality_Criteria

# Hypothesis Quality Criteria

## Framework for Evaluating Scientific Hypotheses

Use these criteria to assess the quality and rigor of generated hypotheses. A robust hypothesis should score well across multiple dimensions.

**Note on Report Structure:** When generating hypothesis reports, provide a brief quality assessment summary in the main text (comparative table with ratings), and include detailed evaluation with strengths, weaknesses, and comprehensive analysis in **Appendix C: Quality Assessment**.

## Core Criteria

### 1. Testability

**Definition:** The hypothesis can be empirically tested through observation or experimentation.

**Evaluation questions:**
- Can specific experiments or observations test this hypothesis?
- Are the predicted outcomes measurable?
- Can the hypothesis be tested with current or near-future methods?
- Are there multiple independent ways to test it?

**Strong testability examples:**
- "Increased expression of protein X will reduce cell proliferation rate by >30%"
- "Patients receiving treatment Y will show 50% reduction in symptom Z within 4 weeks"

**Weak testability examples:**
- "This process is influenced by complex interactions" (vague, no specific prediction)
- "The mechanism involves quantum effects" (if no method to test quantum effects exists)

### 2. Falsifiability

**Definition:** Clear conditions or observations would disprove the hypothesis (Popperian criterion).

**Evaluation questions:**
- What specific observations would prove this hypothesis wrong?
- Are the falsifying conditions realistic to observe?
- Is the hypothesis stated clearly enough to be disproven?
- Can null results meaningfully falsify the hypothesis?

**Strong falsifiability examples:**
- "If we knock out gene X, phenotype Y will disappear" (can be falsified if phenotype persists)
- "Drug A will outperform placebo in 80% of patients" (clear falsification threshold)

**Weak falsifiability examples:**
- "Multiple factors contribute to the outcome" (too vague to falsify)
- "The effect may vary depending on context" (built-in escape clauses)

### 3. Parsimony (Occam's Razor)

**Definition:** Among competing hypotheses with equal explanatory power, prefer the simpler explanation.

**Evaluation questions:**
- Does the hypothesis invoke the minimum number of entities/mechanisms needed?
- Are all proposed elements necessary to explain the phenomenon?
- Could a simpler mechanism account for the observations?
- Does it avoid unnecessary assumptions?

**Parsimony considerations:**
- Simple ≠ simplistic; complexity is justified when evidence demands it
- Established mechanisms are "simpler" than novel, unproven ones
- Direct mechanisms are simpler than elaborate multi-step pathways
- One well-supported mechanism beats multiple speculative ones

### 4. Explanatory Power

**Definition:** The hypothesis accounts for a substantial portion of the observed phenomenon.

**Evaluation questions:**
- How much of the observed data does this hypothesis explain?
- Does it account for both typical and atypical observations?
- Can it explain related phenomena beyond the immediate observation?
- Does it resolve apparent contradictions in existing data?

**Strong explanatory power indicators:**
- Explains multiple independent observations
- Accounts for quantitative relationships, not just qualitative patterns
- Resolves previously puzzling findings
- Makes sense of seemingly contradictory results

**Limited explanatory power indicators:**
- Only explains part of the phenomenon
- Requires additional hypotheses for complete explanation
- Leaves major observations unexplained

### 5. Scope

**Definition:** The range of phenomena and contexts the hypothesis can address.

**Evaluation questions:**
- Does it apply only to the specific case or to broader situations?
- Can it generalize across conditions, species, or systems?
- Does it connect to larger theoretical frameworks?
- What are its boundaries and limitations?

**Broader scope (generally preferable):**
- Applies across multiple experimental conditions
- Generalizes to related systems or species
- Connects phenomenon to established principles

**Narrower scope (acceptable if explicitly defined):**
- Limited to specific conditions or contexts
- Requires different mechanisms in different settings
- Context-dependent with clear boundaries

### 6. Consistency with Established Knowledge

**Definition:** Alignment with well-supported theories, principles, and empirical findings.

**Evaluation questions:**
- Is it consistent with established physical, chemical, or biological principles?
- Does it align with or reasonably extend current theories?
- If contradicting established knowledge, is there strong justification?
- Does it require violating well-supported laws or findings?

**Levels of consistency:**
- **Fully consistent:** Applies established mechanisms in new context
- **Mostly consistent:** Extends current understanding in plausible ways
- **Partially inconsistent:** Contradicts some findings but has explanatory value
- **Highly inconsistent:** Requires rejecting well-established principles (requires exceptional evidence)

### 7. Novelty and Insight

**Definition:** The hypothesis offers new understanding beyond merely restating known facts.

**Evaluation questions:**
- Does it provide new mechanistic insight?
- Does it challenge assumptions or conventional wisdom?
- Does it suggest unexpected connections or relationships?
- Does it open new research directions?

**Novel contributions:**
- Proposes previously unconsidered mechanisms
- Reframes the problem in a productive way
- Connects disparate observations
- Suggests non-obvious testable predictions

**Note:** Novelty alone doesn't make a hypothesis valuable; it must also be testable, parsimonious, and explanatory.

## Comparative Evaluation

When evaluating multiple competing hypotheses:

### Trade-offs and Balancing

Hypotheses often involve trade-offs:
- More parsimonious but less explanatory power
- Broader scope but less testable with current methods
- Novel insights but less consistent with current knowledge

**Evaluation approach:**
- No hypothesis needs to be perfect on all dimensions
- Identify each hypothesis's strengths and weaknesses
- Consider which criteria are most important for the specific phenomenon
- Note which hypotheses are most immediately testable
- Identify which would be most informative if supported

### Distinguishability

**Key question:** Can experiments distinguish between competing hypotheses?

- Identify predictions that differ between hypotheses
- Prioritize hypotheses that make distinct predictions
- Note which experiments would most efficiently narrow the field
- Consider whether hypotheses could all be partially correct

## Common Pitfalls

### Untestable Hypotheses
- Too vague to generate specific predictions
- Invoke unobservable or unmeasurable entities
- Require technology that doesn't exist

### Unfalsifiable Hypotheses
- Built-in escape clauses ("may or may not occur")
- Post-hoc explanations that fit any outcome
- No specification of what would disprove them

### Overly Complex Hypotheses
- Invoke multiple unproven mechanisms
- Add unnecessary steps or entities
- Complexity not justified by explanatory gains

### Just-So Stories
- Plausible narratives without testable predictions
- Explain observations but don't predict new ones
- Impossible to distinguish from alternative stories

## Practical Application

When generating hypotheses:

1. **Draft initial hypotheses** focusing on mechanistic explanations
2. **Apply quality criteria** to identify weaknesses
3. **Refine hypotheses** to improve testability and clarity
4. **Develop specific predictions** to enhance testability and falsifiability
5. **Compare systematically** across all criteria
6. **Prioritize for testing** based on distinguishability and feasibility

Remember: The goal is not a perfect hypothesis, but a set of testable, falsifiable, informative hypotheses that advance understanding of the phenomenon.

---

## Reference: Literature_Search_Strategies

# Literature Search Strategies

## Effective Techniques for Finding Scientific Evidence

Comprehensive literature search is essential for grounding hypotheses in existing evidence. This reference provides strategies for both PubMed (biomedical literature) and general scientific search.

## Search Strategy Framework

### Three-Phase Approach

1. **Broad exploration:** Understand the landscape and identify key concepts
2. **Focused searching:** Target specific mechanisms, theories, or findings
3. **Citation mining:** Follow references and related articles from key papers

### Before You Search

**Clarify search goals:**
- What aspects of the phenomenon need evidence?
- What types of studies are most relevant (reviews, primary research, methods)?
- What time frame is relevant (recent only, or historical context)?
- What level of evidence is needed (mechanistic, correlational, causal)?

## PubMed Search Strategies

### When to Use PubMed

Use WebFetch with PubMed URLs for:
- Biomedical and life sciences research
- Clinical studies and medical literature
- Molecular, cellular, and physiological mechanisms
- Disease etiology and pathology
- Drug and therapeutic research

### Effective PubMed Search Techniques

#### 1. Start with Review Articles

**Why:** Reviews synthesize literature, identify key concepts, and provide comprehensive reference lists.

**Search strategy:**
- Add "review" to search terms
- Use PubMed filters: Article Type → Review, Systematic Review, Meta-Analysis
- Look for recent reviews (last 2-5 years)

**Example searches:**
- `https://pubmed.ncbi.nlm.nih.gov/?term=wound+healing+diabetes+review`
- `https://pubmed.ncbi.nlm.nih.gov/?term=gut+microbiome+cognition+systematic+review`

#### 2. Use MeSH Terms (Medical Subject Headings)

**Why:** MeSH terms are standardized vocabulary that captures concept variations.

**Strategy:**
- PubMed auto-suggests MeSH terms
- Helps find papers using different terminology for same concept
- More comprehensive than keyword-only searches

**Example:**
- Instead of just "heart attack," use MeSH term "Myocardial Infarction"
- Captures papers using "MI," "heart attack," "cardiac infarction," etc.

#### 3. Boolean Operators and Advanced Syntax

**AND:** Narrow search (all terms must be present)
- `diabetes AND wound healing AND inflammation`

**OR:** Broaden search (any term can be present)
- `(Alzheimer OR dementia) AND gut microbiome`

**NOT:** Exclude terms
- `cancer treatment NOT surgery`

**Quotes:** Exact phrases
- `"oxidative stress"`

**Wildcards:** Variations
- `gene*` finds gene, genes, genetic, genetics

#### 4. Filter by Publication Type and Date

**Publication types:**
- Clinical Trial
- Meta-Analysis
- Systematic Review
- Research Support, NIH
- Randomized Controlled Trial

**Date filters:**
- Recent work (last 2-5 years): Cutting-edge findings
- Historical work: Foundational studies
- Specific time periods: Track development of understanding

#### 5. Use "Similar Articles" and "Cited By"

**Strategy:**
- Find one highly relevant paper
- Click "Similar articles" for related work
- Use cited by tools to find newer work building on it

### PubMed Search Examples by Hypothesis Goal

**Mechanistic understanding:**
```
https://pubmed.ncbi.nlm.nih.gov/?term=(mechanism+OR+pathway)+AND+[phenomenon]+AND+(molecular+OR+cellular)
```

**Causal relationships:**
```
https://pubmed.ncbi.nlm.nih.gov/?term=[exposure]+AND+[outcome]+AND+(randomized+controlled+trial+OR+cohort+study)
```

**Biomarkers and associations:**
```
https://pubmed.ncbi.nlm.nih.gov/?term=[biomarker]+AND+[disease]+AND+(association+OR+correlation+OR+prediction)
```

**Treatment effectiveness:**
```
https://pubmed.ncbi.nlm.nih.gov/?term=[intervention]+AND+[condition]+AND+(efficacy+OR+effectiveness+OR+clinical+trial)
```

## General Scientific Web Search Strategies

### When to Use Web Search

Use WebSearch for:
- Non-biomedical sciences (physics, chemistry, materials, earth sciences)
- Interdisciplinary topics
- Recent preprints and unpublished work
- Grey literature (technical reports, conference proceedings)
- Broader context and cross-domain analogies

### Effective Web Search Techniques

#### 1. Use Domain-Specific Search Terms

**Include field-specific terminology:**
- Chemistry: "mechanism," "reaction pathway," "synthesis"
- Physics: "model," "theory," "experimental validation"
- Materials science: "properties," "characterization," "synthesis"
- Ecology: "population dynamics," "community structure"

#### 2. Target Academic Sources

**Search operators:**
- `site:arxiv.org` - Preprints (physics, CS, math, quantitative biology)
- `site:biorxiv.org` - Biology preprints
- `site:edu` - Academic institutions
- `filetype:pdf` - Academic papers (often)

**Example searches:**
- `superconductivity high temperature mechanism site:arxiv.org`
- `CRISPR off-target effects site:biorxiv.org`

#### 3. Search for Authors and Labs

**When you find a relevant paper:**
- Search for the authors' other work
- Find their lab website for unpublished work
- Identify key research groups in the field

#### 4. Use Google Scholar Approaches

**Strategies:**
- Use "Cited by" to find newer related work
- Use "Related articles" to expand search
- Set date ranges to focus on recent work
- Use author: operator to find specific researchers

#### 5. Combine General and Specific Terms

**Structure:**
- Specific phenomenon + general concept
- "tomato plant growth" + "bacterial promotion"
- "cognitive decline" + "gut microbiome"

**Boolean logic:**
- Use quotes for exact phrases: `"spike protein mutation"`
- Use OR for alternatives: `(transmissibility OR transmission rate)`
- Combine: `"spike protein" AND (transmissibility OR virulence) AND mutation`

## Cross-Database Search Strategies

### Comprehensive Literature Search Workflow

1. **Start with reviews (PubMed or Web Search):**
   - Identify key concepts and terminology
   - Note influential papers and researchers
   - Understand current state of field

2. **Focused primary research (PubMed):**
   - Search for specific mechanisms
   - Find experimental evidence
   - Identify methodologies

3. **Broaden with web search:**
   - Find related work in other fields
   - Locate recent preprints
   - Identify analogous systems

4. **Citation mining:**
   - Follow references from key papers
   - Use "cited by" to find recent work
   - Track influential studies

5. **Iterative refinement:**
   - Add new terms discovered in papers
   - Narrow if too many results
   - Broaden if too few relevant results

## Topic-Specific Search Strategies

### Mechanisms and Pathways

**Goal:** Understand how something works

**Search components:**
- Phenomenon + "mechanism"
- Phenomenon + "pathway"
- Phenomenon + specific molecules/pathways suspected

**Examples:**
- `diabetic wound healing mechanism inflammation`
- `autophagy pathway cancer`

### Associations and Correlations

**Goal:** Find what factors are related

**Search components:**
- Variable A + Variable B + "association"
- Variable A + Variable B + "correlation"
- Variable A + "predicts" + Variable B

**Examples:**
- `vitamin D cardiovascular disease association`
- `gut microbiome diversity predicts cognitive function`

### Interventions and Treatments

**Goal:** Evidence for what works

**Search components:**
- Intervention + condition + "efficacy"
- Intervention + condition + "randomized controlled trial"
- Intervention + condition + "treatment outcome"

**Examples:**
- `probiotic intervention depression randomized controlled trial`
- `exercise intervention cognitive decline efficacy`

### Methods and Techniques

**Goal:** How to test hypothesis

**Search components:**
- Method name + application area
- "How to measure" + phenomenon
- Technique + validation

**Examples:**
- `CRISPR screen cancer drug resistance`
- `measure protein-protein interaction methods`

### Analogous Systems

**Goal:** Find insights from related phenomena

**Search components:**
- Mechanism + different system
- Similar phenomenon + different organism/condition

**Examples:**
- If studying plant-microbe symbiosis: search `nitrogen fixation rhizobia legumes`
- If studying drug resistance: search `antibiotic resistance evolution mechanisms`

## Evaluating Paper Impact and Quality

### Citation Count Significance

Citation counts indicate influence and importance in the field. Interpret citations relative to paper age and field norms:

| Paper Age | Citations | Interpretation |
|-----------|-----------|----------------|
| 0-3 years | 20+ | Noteworthy - gaining traction |
| 0-3 years | 100+ | Highly Influential - significant impact already |
| 3-7 years | 100+ | Significant - established contribution |
| 3-7 years | 500+ | Landmark - major contribution to field |
| 7+ years | 500+ | Seminal - widely recognized important work |
| 7+ years | 1000+ | Foundational - field-defining paper |

**Field-specific considerations:**
- Biomedical/clinical: Higher citation norms (NEJM papers often 1000+)
- Computer Science: Conference citations matter more than journals
- Mathematics/Physics: Lower citation norms, longer citation half-lives
- Social Sciences: Moderate citation norms, high book citation rates

### Journal Impact Factor Guidance

**Tier 1 - Premier Venues (Always Prefer):**
- **General Science:** Nature (IF ~65), Science (IF ~55), Cell (IF ~65), PNAS (IF ~12)
- **Medicine:** NEJM (IF ~175), Lancet (IF ~170), JAMA (IF ~120), BMJ (IF ~93)
- **Field Flagships:** Nature Medicine, Nature Biotechnology, Nature Methods, Nature Genetics

**Tier 2 - High-Impact Specialized (Strong Preference):**
- Impact Factor >10
- Examples: JAMA Internal Medicine, Annals of Internal Medicine, Circulation, Blood
- Top ML/AI conferences: NeurIPS, ICML, ICLR (equivalent to IF 15-25)

**Tier 3 - Respected Specialized (Include When Relevant):**
- Impact Factor 5-10
- Established society journals
- Well-indexed specialty journals

**Tier 4 - Other Peer-Reviewed (Use Sparingly):**
- Impact Factor <5
- Only cite if directly relevant AND no better source exists

### Author Track Record Evaluation

Prefer papers from established researchers:

**Strong Author Indicators:**
- **High h-index:** >40 in established fields, >20 for early-career stars
- **Multiple Tier-1 publications:** Track record in Nature/Science/Cell family
- **Institutional affiliation:** Leading research universities and institutes
- **Recognition:** Awards, fellowships, editorial positions
- **First/last authorship:** On multiple highly-cited papers

**How to Check Author Reputation:**
1. Google Scholar profile: Check h-index, i10-index, total citations
2. PubMed: Search author name, review publication venues
3. Institutional page: Check position, awards, grants
4. ORCID profile: Full publication history

### Conference Ranking Awareness (Computer Science/AI)

For ML/AI and computer science topics, conference rankings matter:

**A* (Flagship) - Equivalent to Nature/Science:**
- NeurIPS (Neural Information Processing Systems)
- ICML (International Conference on Machine Learning)
- ICLR (International Conference on Learning Representations)
- CVPR (Computer Vision and Pattern Recognition)
- ACL (Association for Computational Linguistics)

**A (Excellent) - Equivalent to Tier-2 Journals:**
- AAAI, IJCAI (AI general)
- EMNLP, NAACL (NLP)
- ECCV, ICCV (Computer Vision)
- SIGKDD, WWW (Data Mining)

**B (Good) - Equivalent to Tier-3 Journals:**
- COLING, CoNLL (NLP)
- WACV, BMVC (Computer Vision)
- Most ACM/IEEE specialized conferences

## Evaluating Source Quality

### Primary Research Quality Indicators

**Strong quality signals:**
- Published in Tier-1 or Tier-2 venues
- High citation count for paper age
- Written by established researchers with strong track records
- Large sample sizes (for statistical power)
- Pre-registered studies (reduces bias)
- Appropriate controls and methods
- Consistent with other findings
- Transparent data and methods

**Red flags:**
- Published in predatory or low-impact journals
- Written by authors with no established track record
- No peer review (use cautiously)
- Conflicts of interest not disclosed
- Methods not clearly described
- Extraordinary claims without extraordinary evidence
- Contradicts large body of evidence without explanation

### Review Quality Indicators

**Systematic reviews (highest quality):**
- Published in Tier-1/2 venues (Cochrane, Nature Reviews, Annual Reviews)
- Pre-defined search strategy
- Explicit inclusion/exclusion criteria
- Quality assessment of included studies
- Quantitative synthesis (meta-analysis)

**Narrative reviews (variable quality):**
- Expert synthesis of field
- May have selection bias
- Useful for context and framing
- Check author expertise and citations
- Prefer reviews in Tier-1/2 journals by field leaders

## Time Management in Literature Search

### Allocate Search Time Appropriately

**For straightforward hypotheses (30-60 min):**
- 1-2 broad review articles
- 3-5 targeted primary research papers
- Quick web search for recent developments

**For complex hypotheses (1-3 hours):**
- Multiple reviews for different aspects
- 10-15 primary research papers
- Systematic search across databases
- Citation mining from key papers

**For contentious topics (3+ hours):**
- Systematic review approach
- Identify competing perspectives
- Track historical development
- Cross-reference findings

### Diminishing Returns

**Signs you've searched enough:**
- Finding the same papers repeatedly
- New searches yield mostly irrelevant papers
- Sufficient evidence to support/contextualize hypotheses
- Multiple independent lines of evidence converge

**When to search more:**
- Major gaps in understanding remain
- Conflicting evidence needs resolution
- Hypothesis seems inconsistent with literature
- Need specific methodological information

## Documenting Search Results

### Information to Capture

**For each relevant paper:**
- Full citation (authors, year, journal, title)
- Key findings relevant to hypothesis
- Study design and methods
- Limitations noted by authors
- How it relates to hypothesis

### Organizing Findings

**Group by:**
- Supporting evidence for hypothesis A, B, C
- Methodological approaches
- Conflicting findings requiring explanation
- Gaps in current knowledge

**Synthesis notes:**
- What is well-established?
- What is controversial or uncertain?
- What analogies exist in other systems?
- What methods are commonly used?

### Citation Organization for Hypothesis Reports

**For report structure:** Organize citations for two audiences:

**Main Text (15-20 key citations):**
- Most influential papers (highly cited, seminal studies)
- Recent definitive evidence (last 2-3 years)
- Key papers directly supporting each hypothesis (3-5 per hypothesis)
- Major reviews synthesizing the field

**Appendix A: Comprehensive Literature Review (40-60+ citations):**
- **Historical context:** Foundational papers establishing field
- **Current understanding:** Recent reviews and meta-analyses
- **Hypothesis-specific evidence:** 8-15 papers per hypothesis covering:
  - Direct supporting evidence
  - Analogous mechanisms in related systems
  - Methodological precedents
  - Theoretical framework papers
- **Conflicting findings:** Papers representing different viewpoints
- **Knowledge gaps:** Papers identifying limitations or unanswered questions

**Target citation density:** Aim for 50+ total references to provide comprehensive support for all claims and demonstrate thorough literature grounding.

**Grouping strategy for Appendix A:**
1. Background and context papers
2. Current understanding and established mechanisms
3. Evidence supporting each hypothesis (separate subsections)
4. Contradictory or alternative findings
5. Methodological and technical papers

## Practical Search Workflow

### Step-by-Step Process

1. **Define search goals (5 min):**
   - What aspects of phenomenon need evidence?
   - What would support or refute hypotheses?

2. **Broad review search (15-20 min):**
   - Find 1-3 review articles
   - Skim abstracts for relevance
   - Note key concepts and terminology

3. **Targeted primary research (30-45 min):**
   - Search for specific mechanisms/evidence
   - Read abstracts, scan figures and conclusions
   - Follow most promising references

4. **Cross-domain search (15-30 min):**
   - Look for analogies in other systems
   - Find recent preprints
   - Identify emerging trends

5. **Citation mining (15-30 min):**
   - Follow references from key papers
   - Use "cited by" for recent work
   - Identify seminal studies

6. **Synthesize findings (20-30 min):**
   - Summarize evidence for each hypothesis
   - Note patterns and contradictions
   - Identify knowledge gaps

### Iteration and Refinement

**When initial search is insufficient:**
- Broaden terms if too few results
- Add specific mechanisms/pathways if too many results
- Try alternative terminology
- Search for related phenomena
- Consult review articles for better search terms

**Red flags requiring more search:**
- Only finding weak or indirect evidence
- All evidence comes from single lab or source
- Evidence seems inconsistent with basic principles
- Major aspects of phenomenon lack any relevant literature

## Common Search Pitfalls

### Pitfalls to Avoid

1. **Confirmation bias:** Only seeking evidence supporting preferred hypothesis
   - **Solution:** Actively search for contradicting evidence

2. **Recency bias:** Only considering recent work, missing foundational studies
   - **Solution:** Include historical searches, track development of ideas

3. **Too narrow:** Missing relevant work due to restrictive terms
   - **Solution:** Use OR operators, try alternative terminology

4. **Too broad:** Overwhelmed by irrelevant results
   - **Solution:** Add specific terms, use filters, combine concepts with AND

5. **Single database:** Missing important work in other fields
   - **Solution:** Search both PubMed and general web, try domain-specific databases

6. **Stopping too soon:** Insufficient evidence to ground hypotheses
   - **Solution:** Set minimum targets (e.g., 2 reviews + 5 primary papers per hypothesis aspect)

7. **Cherry-picking:** Citing only supportive papers
   - **Solution:** Represent full spectrum of evidence, acknowledge contradictions

## Special Cases

### Emerging Topics (Limited Literature)

**When little published work exists:**
- Search for analogous phenomena in related systems
- Look for preprints (arXiv, bioRxiv)
- Find conference abstracts and posters
- Identify theoretical frameworks that may apply
- Note the limited evidence in hypothesis generation

### Controversial Topics (Conflicting Literature)

**When evidence is contradictory:**
- Systematically document both sides
- Look for methodological differences explaining conflict
- Check for temporal trends (has understanding shifted?)
- Identify what would resolve the controversy
- Generate hypotheses explaining the discrepancy

### Interdisciplinary Topics

**When spanning multiple fields:**
- Search each field's primary databases
- Use field-specific terminology for each domain
- Look for bridging papers that cite across fields
- Consider consulting domain experts
- Translate concepts between disciplines carefully

## Integration with Hypothesis Generation

### Using Literature to Inform Hypotheses

**Direct applications:**
- Established mechanisms to apply to new contexts
- Known pathways relevant to phenomenon
- Similar phenomena in related systems
- Validated methods for testing

**Indirect applications:**
- Analogies from different systems
- Theoretical frameworks to apply
- Gaps suggesting novel mechanisms
- Contradictions requiring resolution

### Balancing Literature Dependence

**Too literature-dependent:**
- Hypotheses merely restate known mechanisms
- No novel insights or predictions
- "Hypotheses" are actually established facts

**Too literature-independent:**
- Hypotheses ignore relevant evidence
- Propose implausible mechanisms
- Reinvent already-tested ideas
- Inconsistent with established principles

**Optimal balance:**
- Grounded in existing evidence
- Extend understanding in novel ways
- Acknowledge both supporting and challenging evidence
- Generate testable predictions beyond current knowledge
