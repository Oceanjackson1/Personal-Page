---
title: "Literature Review"
description: "Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). This skill should be used when conducting systematic literature reviews, meta-analyses, research synthesis, or..."
category: "research"
source: "community"
author: "Community"
tags: ["literature", "review"]
date: 2026-03-20
---

# Literature Review

## Overview

Conduct systematic, comprehensive literature reviews following rigorous academic methodology. Search multiple literature databases, synthesize findings thematically, verify all citations for accuracy, and generate professional output documents in markdown and PDF formats.

This skill integrates with multiple scientific skills for database access (gget, bioservices, datacommons-client) and provides specialized tools for citation verification, result aggregation, and document generation.

## When to Use This Skill

Use this skill when:
- Conducting a systematic literature review for research or publication
- Synthesizing current knowledge on a specific topic across multiple sources
- Performing meta-analysis or scoping reviews
- Writing the literature review section of a research paper or thesis
- Investigating the state of the art in a research domain
- Identifying research gaps and future directions
- Requiring verified citations and professional formatting

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every literature review MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Literature reviews without visual elements are incomplete. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., PRISMA flow diagram for systematic reviews)
2. Prefer 2-3 figures for comprehensive reviews (search strategy flowchart, thematic synthesis diagram, conceptual framework)

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
- PRISMA flow diagrams for systematic reviews
- Literature search strategy flowcharts
- Thematic synthesis diagrams
- Research gap visualization maps
- Citation network diagrams
- Conceptual framework illustrations
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Core Workflow

Literature reviews follow a structured, multi-phase workflow:

### Phase 1: Planning and Scoping

1. **Define Research Question**: Use PICO framework (Population, Intervention, Comparison, Outcome) for clinical/biomedical reviews
   - Example: "What is the efficacy of CRISPR-Cas9 (I) for treating sickle cell disease (P) compared to standard care (C)?"

2. **Establish Scope and Objectives**:
   - Define clear, specific research questions
   - Determine review type (narrative, systematic, scoping, meta-analysis)
   - Set boundaries (time period, geographic scope, study types)

3. **Develop Search Strategy**:
   - Identify 2-4 main concepts from research question
   - List synonyms, abbreviations, and related terms for each concept
   - Plan Boolean operators (AND, OR, NOT) to combine terms
   - Select minimum 3 complementary databases

4. **Set Inclusion/Exclusion Criteria**:
   - Date range (e.g., last 10 years: 2015-2024)
   - Language (typically English, or specify multilingual)
   - Publication types (peer-reviewed, preprints, reviews)
   - Study designs (RCTs, observational, in vitro, etc.)
   - Document all criteria clearly

### Phase 2: Systematic Literature Search

1. **Multi-Database Search**:

   Select databases appropriate for the domain:

   **Biomedical & Life Sciences:**
   - Use `gget` skill: `gget search pubmed "search terms"` for PubMed/PMC
   - Use `gget` skill: `gget search biorxiv "search terms"` for preprints
   - Use `bioservices` skill for ChEMBL, KEGG, UniProt, etc.

   **General Scientific Literature:**
   - Search arXiv via direct API (preprints in physics, math, CS, q-bio)
   - Search Semantic Scholar via API (200M+ papers, cross-disciplinary)
   - Use Google Scholar for comprehensive coverage (manual or careful scraping)

   **Specialized Databases:**
   - Use `gget alphafold` for protein structures
   - Use `gget cosmic` for cancer genomics
   - Use `datacommons-client` for demographic/statistical data
   - Use specialized databases as appropriate for the domain

2. **Document Search Parameters**:
   ```markdown
   ## Search Strategy

   ### Database: PubMed
   - **Date searched**: 2024-10-25
   - **Date range**: 2015-01-01 to 2024-10-25
   - **Search string**:
     ```
     ("CRISPR"[Title] OR "Cas9"[Title])
     AND ("sickle cell"[MeSH] OR "SCD"[Title/Abstract])
     AND 2015:2024[Publication Date]
     ```
   - **Results**: 247 articles
   ```

   Repeat for each database searched.

3. **Export and Aggregate Results**:
   - Export results in JSON format from each database
   - Combine all results into a single file
   - Use `scripts/search_databases.py` for post-processing:
     ```bash
     python search_databases.py combined_results.json \
       --deduplicate \
       --format markdown \
       --output aggregated_results.md
     ```

### Phase 3: Screening and Selection

1. **Deduplication**:
   ```bash
   python search_databases.py results.json --deduplicate --output unique_results.json
   ```
   - Removes duplicates by DOI (primary) or title (fallback)
   - Document number of duplicates removed

2. **Title Screening**:
   - Review all titles against inclusion/exclusion criteria
   - Exclude obviously irrelevant studies
   - Document number excluded at this stage

3. **Abstract Screening**:
   - Read abstracts of remaining studies
   - Apply inclusion/exclusion criteria rigorously
   - Document reasons for exclusion

4. **Full-Text Screening**:
   - Obtain full texts of remaining studies
   - Conduct detailed review against all criteria
   - Document specific reasons for exclusion
   - Record final number of included studies

5. **Create PRISMA Flow Diagram**:
   ```
   Initial search: n = X
   ├─ After deduplication: n = Y
   ├─ After title screening: n = Z
   ├─ After abstract screening: n = A
   └─ Included in review: n = B
   ```

### Phase 4: Data Extraction and Quality Assessment

1. **Extract Key Data** from each included study:
   - Study metadata (authors, year, journal, DOI)
   - Study design and methods
   - Sample size and population characteristics
   - Key findings and results
   - Limitations noted by authors
   - Funding sources and conflicts of interest

2. **Assess Study Quality**:
   - **For RCTs**: Use Cochrane Risk of Bias tool
   - **For observational studies**: Use Newcastle-Ottawa Scale
   - **For systematic reviews**: Use AMSTAR 2
   - Rate each study: High, Moderate, Low, or Very Low quality
   - Consider excluding very low-quality studies

3. **Organize by Themes**:
   - Identify 3-5 major themes across studies
   - Group studies by theme (studies may appear in multiple themes)
   - Note patterns, consensus, and controversies

### Phase 5: Synthesis and Analysis

1. **Create Review Document** from template:
   ```bash
   cp assets/review_template.md my_literature_review.md
   ```

2. **Write Thematic Synthesis** (NOT study-by-study summaries):
   - Organize Results section by themes or research questions
   - Synthesize findings across multiple studies within each theme
   - Compare and contrast different approaches and results
   - Identify consensus areas and points of controversy
   - Highlight the strongest evidence

   Example structure:
   ```markdown
   #### 3.3.1 Theme: CRISPR Delivery Methods

   Multiple delivery approaches have been investigated for therapeutic
   gene editing. Viral vectors (AAV) were used in 15 studies^1-15^ and
   showed high transduction efficiency (65-85%) but raised immunogenicity
   concerns^3,7,12^. In contrast, lipid nanoparticles demonstrated lower
   efficiency (40-60%) but improved safety profiles^16-23^.
   ```

3. **Critical Analysis**:
   - Evaluate methodological strengths and limitations across studies
   - Assess quality and consistency of evidence
   - Identify knowledge gaps and methodological gaps
   - Note areas requiring future research

4. **Write Discussion**:
   - Interpret findings in broader context
   - Discuss clinical, practical, or research implications
   - Acknowledge limitations of the review itself
   - Compare with previous reviews if applicable
   - Propose specific future research directions

### Phase 6: Citation Verification

**CRITICAL**: All citations must be verified for accuracy before final submission.

1. **Verify All DOIs**:
   ```bash
   python scripts/verify_citations.py my_literature_review.md
   ```

   This script:
   - Extracts all DOIs from the document
   - Verifies each DOI resolves correctly
   - Retrieves metadata from CrossRef
   - Generates verification report
   - Outputs properly formatted citations

2. **Review Verification Report**:
   - Check for any failed DOIs
   - Verify author names, titles, and publication details match
   - Correct any errors in the original document
   - Re-run verification until all citations pass

3. **Format Citations Consistently**:
   - Choose one citation style and use throughout (see `references/citation_styles.md`)
   - Common styles: APA, Nature, Vancouver, Chicago, IEEE
   - Use verification script output to format citations correctly
   - Ensure in-text citations match reference list format

### Phase 7: Document Generation

1. **Generate PDF**:
   ```bash
   python scripts/generate_pdf.py my_literature_review.md \
     --citation-style apa \
     --output my_review.pdf
   ```

   Options:
   - `--citation-style`: apa, nature, chicago, vancouver, ieee
   - `--no-toc`: Disable table of contents
   - `--no-numbers`: Disable section numbering
   - `--check-deps`: Check if pandoc/xelatex are installed

2. **Review Final Output**:
   - Check PDF formatting and layout
   - Verify all sections are present
   - Ensure citations render correctly
   - Check that figures/tables appear properly
   - Verify table of contents is accurate

3. **Quality Checklist**:
   - [ ] All DOIs verified with verify_citations.py
   - [ ] Citations formatted consistently
   - [ ] PRISMA flow diagram included (for systematic reviews)
   - [ ] Search methodology fully documented
   - [ ] Inclusion/exclusion criteria clearly stated
   - [ ] Results organized thematically (not study-by-study)
   - [ ] Quality assessment completed
   - [ ] Limitations acknowledged
   - [ ] References complete and accurate
   - [ ] PDF generates without errors

## Database-Specific Search Guidance

### PubMed / PubMed Central

Access via `gget` skill:
```bash
# Search PubMed
gget search pubmed "CRISPR gene editing" -l 100

# Search with filters
# Use PubMed Advanced Search Builder to construct complex queries
# Then execute via gget or direct Entrez API
```

**Search tips**:
- Use MeSH terms: `"sickle cell disease"[MeSH]`
- Field tags: `[Title]`, `[Title/Abstract]`, `[Author]`
- Date filters: `2020:2024[Publication Date]`
- Boolean operators: AND, OR, NOT
- See MeSH browser: https://meshb.nlm.nih.gov/search

### bioRxiv / medRxiv

Access via `gget` skill:
```bash
gget search biorxiv "CRISPR sickle cell" -l 50
```

**Important considerations**:
- Preprints are not peer-reviewed
- Verify findings with caution
- Check if preprint has been published (CrossRef)
- Note preprint version and date

### arXiv

Access via direct API or WebFetch:
```python
# Example search categories:
# q-bio.QM (Quantitative Methods)
# q-bio.GN (Genomics)
# q-bio.MN (Molecular Networks)
# cs.LG (Machine Learning)
# stat.ML (Machine Learning Statistics)

# Search format: category AND terms
search_query = "cat:q-bio.QM AND ti:\"single cell sequencing\""
```

### Semantic Scholar

Access via direct API (requires API key, or use free tier):
- 200M+ papers across all fields
- Excellent for cross-disciplinary searches
- Provides citation graphs and paper recommendations
- Use for finding highly influential papers

### Specialized Biomedical Databases

Use appropriate skills:
- **ChEMBL**: `bioservices` skill for chemical bioactivity
- **UniProt**: `gget` or `bioservices` skill for protein information
- **KEGG**: `bioservices` skill for pathways and genes
- **COSMIC**: `gget` skill for cancer mutations
- **AlphaFold**: `gget alphafold` for protein structures
- **PDB**: `gget` or direct API for experimental structures

### Citation Chaining

Expand search via citation networks:

1. **Forward citations** (papers citing key papers):
   - Use Google Scholar "Cited by"
   - Use Semantic Scholar or OpenAlex APIs
   - Identifies newer research building on seminal work

2. **Backward citations** (references from key papers):
   - Extract references from included papers
   - Identify highly cited foundational work
   - Find papers cited by multiple included studies

## Citation Style Guide

Detailed formatting guidelines are in `references/citation_styles.md`. Quick reference:

### APA (7th Edition)
- In-text: (Smith et al., 2023)
- Reference: Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Title. *Journal*, *22*(4), 301-318. https://doi.org/10.xxx/yyy

### Nature
- In-text: Superscript numbers^1,2^
- Reference: Smith, J. D., Johnson, M. L. & Williams, K. R. Title. *Nat. Rev. Drug Discov.* **22**, 301-318 (2023).

### Vancouver
- In-text: Superscript numbers^1,2^
- Reference: Smith JD, Johnson ML, Williams KR. Title. Nat Rev Drug Discov. 2023;22(4):301-18.

**Always verify citations** with verify_citations.py before finalizing.

### Prioritizing High-Impact Papers (CRITICAL)

**Always prioritize influential, highly-cited papers from reputable authors and top venues.** Quality matters more than quantity in literature reviews.

#### Citation Count Thresholds

Use citation counts to identify the most impactful papers:

| Paper Age | Citation Threshold | Classification |
|-----------|-------------------|----------------|
| 0-3 years | 20+ citations | Noteworthy |
| 0-3 years | 100+ citations | Highly Influential |
| 3-7 years | 100+ citations | Significant |
| 3-7 years | 500+ citations | Landmark Paper |
| 7+ years | 500+ citations | Seminal Work |
| 7+ years | 1000+ citations | Foundational |

#### Journal and Venue Tiers

Prioritize papers from higher-tier venues:

- **Tier 1 (Always Prefer):** Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS, Nature Medicine, Nature Biotechnology
- **Tier 2 (Strong Preference):** High-impact specialized journals (IF>10), top conferences (NeurIPS, ICML for ML/AI)
- **Tier 3 (Include When Relevant):** Respected specialized journals (IF 5-10)
- **Tier 4 (Use Sparingly):** Lower-impact peer-reviewed venues

#### Author Reputation Assessment

Prefer papers from:
- **Senior researchers** with high h-index (>40 in established fields)
- **Leading research groups** at recognized institutions (Harvard, Stanford, MIT, Oxford, etc.)
- **Authors with multiple Tier-1 publications** in the relevant field
- **Researchers with recognized expertise** (awards, editorial positions, society fellows)

#### Identifying Seminal Papers

For any topic, identify foundational work by:
1. **High citation count** (typically 500+ for papers 5+ years old)
2. **Frequently cited by other included studies** (appears in many reference lists)
3. **Published in Tier-1 venues** (Nature, Science, Cell family)
4. **Written by field pioneers** (often cited as establishing concepts)

## Best Practices

### Search Strategy
1. **Use multiple databases** (minimum 3): Ensures comprehensive coverage
2. **Include preprint servers**: Captures latest unpublished findings
3. **Document everything**: Search strings, dates, result counts for reproducibility
4. **Test and refine**: Run pilot searches, review results, adjust search terms
5. **Sort by citations**: When available, sort search results by citation count to surface influential work first

### Screening and Selection
1. **Use multiple databases** (minimum 3): Ensures comprehensive coverage
2. **Include preprint servers**: Captures latest unpublished findings
3. **Document everything**: Search strings, dates, result counts for reproducibility
4. **Test and refine**: Run pilot searches, review results, adjust search terms

### Screening and Selection
1. **Use clear criteria**: Document inclusion/exclusion criteria before screening
2. **Screen systematically**: Title → Abstract → Full text
3. **Document exclusions**: Record reasons for excluding studies
4. **Consider dual screening**: For systematic reviews, have two reviewers screen independently

### Synthesis
1. **Organize thematically**: Group by themes, NOT by individual studies
2. **Synthesize across studies**: Compare, contrast, identify patterns
3. **Be critical**: Evaluate quality and consistency of evidence
4. **Identify gaps**: Note what's missing or understudied

### Quality and Reproducibility
1. **Assess study quality**: Use appropriate quality assessment tools
2. **Verify all citations**: Run verify_citations.py script
3. **Document methodology**: Provide enough detail for others to reproduce
4. **Follow guidelines**: Use PRISMA for systematic reviews

### Writing
1. **Be objective**: Present evidence fairly, acknowledge limitations
2. **Be systematic**: Follow structured template
3. **Be specific**: Include numbers, statistics, effect sizes where available
4. **Be clear**: Use clear headings, logical flow, thematic organization

## Common Pitfalls to Avoid

1. **Single database search**: Misses relevant papers; always search multiple databases
2. **No search documentation**: Makes review irreproducible; document all searches
3. **Study-by-study summary**: Lacks synthesis; organize thematically instead
4. **Unverified citations**: Leads to errors; always run verify_citations.py
5. **Too broad search**: Yields thousands of irrelevant results; refine with specific terms
6. **Too narrow search**: Misses relevant papers; include synonyms and related terms
7. **Ignoring preprints**: Misses latest findings; include bioRxiv, medRxiv, arXiv
8. **No quality assessment**: Treats all evidence equally; assess and report quality
9. **Publication bias**: Only positive results published; note potential bias
10. **Outdated search**: Field evolves rapidly; clearly state search date

## Example Workflow

Complete workflow for a biomedical literature review:

```bash
# 1. Create review document from template
cp assets/review_template.md crispr_sickle_cell_review.md

# 2. Search multiple databases using appropriate skills
# - Use gget skill for PubMed, bioRxiv
# - Use direct API access for arXiv, Semantic Scholar
# - Export results in JSON format

# 3. Aggregate and process results
python scripts/search_databases.py combined_results.json \
  --deduplicate \
  --rank citations \
  --year-start 2015 \
  --year-end 2024 \
  --format markdown \
  --output search_results.md \
  --summary

# 4. Screen results and extract data
# - Manually screen titles, abstracts, full texts
# - Extract key data into the review document
# - Organize by themes

# 5. Write the review following template structure
# - Introduction with clear objectives
# - Detailed methodology section
# - Results organized thematically
# - Critical discussion
# - Clear conclusions

# 6. Verify all citations
python scripts/verify_citations.py crispr_sickle_cell_review.md

# Review the citation report
cat crispr_sickle_cell_review_citation_report.json

# Fix any failed citations and re-verify
python scripts/verify_citations.py crispr_sickle_cell_review.md

# 7. Generate professional PDF
python scripts/generate_pdf.py crispr_sickle_cell_review.md \
  --citation-style nature \
  --output crispr_sickle_cell_review.pdf

# 8. Review final PDF and markdown outputs
```

## Integration with Other Skills

This skill works seamlessly with other scientific skills:

### Database Access Skills
- **gget**: PubMed, bioRxiv, COSMIC, AlphaFold, Ensembl, UniProt
- **bioservices**: ChEMBL, KEGG, Reactome, UniProt, PubChem
- **datacommons-client**: Demographics, economics, health statistics

### Analysis Skills
- **pydeseq2**: RNA-seq differential expression (for methods sections)
- **scanpy**: Single-cell analysis (for methods sections)
- **anndata**: Single-cell data (for methods sections)
- **biopython**: Sequence analysis (for background sections)

### Visualization Skills
- **matplotlib**: Generate figures and plots for review
- **seaborn**: Statistical visualizations

### Writing Skills
- **brand-guidelines**: Apply institutional branding to PDF
- **internal-comms**: Adapt review for different audiences

## Resources

### Bundled Resources

**Scripts:**
- `scripts/verify_citations.py`: Verify DOIs and generate formatted citations
- `scripts/generate_pdf.py`: Convert markdown to professional PDF
- `scripts/search_databases.py`: Process, deduplicate, and format search results

**References:**
- `references/citation_styles.md`: Detailed citation formatting guide (APA, Nature, Vancouver, Chicago, IEEE)
- `references/database_strategies.md`: Comprehensive database search strategies

**Assets:**
- `assets/review_template.md`: Complete literature review template with all sections

### External Resources

**Guidelines:**
- PRISMA (Systematic Reviews): http://www.prisma-statement.org/
- Cochrane Handbook: https://training.cochrane.org/handbook
- AMSTAR 2 (Review Quality): https://amstar.ca/

**Tools:**
- MeSH Browser: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Boolean Search Guide: https://www.ncbi.nlm.nih.gov/books/NBK3827/

**Citation Styles:**
- APA Style: https://apastyle.apa.org/
- Nature Portfolio: https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver: https://www.nlm.nih.gov/bsd/uniform_requirements.html

## Dependencies

### Required Python Packages
```bash
pip install requests  # For citation verification
```

### Required System Tools
```bash
# For PDF generation
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# For LaTeX (PDF generation)
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

Check dependencies:
```bash
python scripts/generate_pdf.py --check-deps
```

## Summary

This literature-review skill provides:

1. **Systematic methodology** following academic best practices
2. **Multi-database integration** via existing scientific skills
3. **Citation verification** ensuring accuracy and credibility
4. **Professional output** in markdown and PDF formats
5. **Comprehensive guidance** covering the entire review process
6. **Quality assurance** with verification and validation tools
7. **Reproducibility** through detailed documentation requirements

Conduct thorough, rigorous literature reviews that meet academic standards and provide comprehensive synthesis of current knowledge in any domain.

---

## Reference: Citation_Styles

# Citation Styles Reference

This document provides detailed guidelines for formatting citations in various academic styles commonly used in literature reviews.

## APA Style (7th Edition)

### Journal Articles

**Format**: Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. *Title of Periodical*, *volume*(issue), page range. https://doi.org/xx.xxx/yyyy

**Example**: Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Machine learning approaches in drug discovery. *Nature Reviews Drug Discovery*, *22*(4), 301-318. https://doi.org/10.1038/nrd.2023.001

### Books

**Format**: Author, A. A. (Year). *Title of work: Capital letter also for subtitle*. Publisher Name. https://doi.org/xxxx

**Example**: Kumar, V., Abbas, A. K., & Aster, J. C. (2021). *Robbins and Cotran pathologic basis of disease* (10th ed.). Elsevier.

### Book Chapters

**Format**: Author, A. A., & Author, B. B. (Year). Title of chapter. In E. E. Editor & F. F. Editor (Eds.), *Title of book* (pp. xx-xx). Publisher.

**Example**: Brown, P. O., & Botstein, D. (2020). Exploring the new world of the genome with DNA microarrays. In M. B. Eisen & P. O. Brown (Eds.), *DNA microarrays: A molecular cloning manual* (pp. 1-45). Cold Spring Harbor Laboratory Press.

### Preprints

**Format**: Author, A. A., & Author, B. B. (Year). Title of preprint. *Repository Name*. https://doi.org/xxxx

**Example**: Zhang, Y., Chen, L., & Wang, H. (2024). Novel therapeutic targets in Alzheimer's disease. *bioRxiv*. https://doi.org/10.1101/2024.01.001

### Conference Papers

**Format**: Author, A. A. (Year, Month day-day). Title of paper. In E. E. Editor (Ed.), *Title of conference proceedings* (pp. xx-xx). Publisher. https://doi.org/xxxx

---

## Nature Style

### Journal Articles

**Format**: Author, A. A., Author, B. B. & Author, C. C. Title of article. *J. Name* **volume**, page range (year).

**Example**: Smith, J. D., Johnson, M. L. & Williams, K. R. Machine learning approaches in drug discovery. *Nat. Rev. Drug Discov.* **22**, 301-318 (2023).

### Books

**Format**: Author, A. A. & Author, B. B. *Book Title* (Publisher, Year).

**Example**: Kumar, V., Abbas, A. K. & Aster, J. C. *Robbins and Cotran Pathologic Basis of Disease* 10th edn (Elsevier, 2021).

### Multiple Authors

- 1-2 authors: List all
- 3+ authors: List first author followed by "et al."

**Example**: Zhang, Y. et al. Novel therapeutic targets in Alzheimer's disease. *bioRxiv* https://doi.org/10.1101/2024.01.001 (2024).

---

## Chicago Style (Author-Date)

### Journal Articles

**Format**: Author, First Name Middle Initial. Year. "Article Title." *Journal Title* volume, no. issue (Month): page range. https://doi.org/xxxx.

**Example**: Smith, John D., Mary L. Johnson, and Karen R. Williams. 2023. "Machine Learning Approaches in Drug Discovery." *Nature Reviews Drug Discovery* 22, no. 4 (April): 301-318. https://doi.org/10.1038/nrd.2023.001.

### Books

**Format**: Author, First Name Middle Initial. Year. *Book Title: Subtitle*. Edition. Place: Publisher.

**Example**: Kumar, Vinay, Abul K. Abbas, and Jon C. Aster. 2021. *Robbins and Cotran Pathologic Basis of Disease*. 10th ed. Philadelphia: Elsevier.

---

## Vancouver Style (Numbered)

### Journal Articles

**Format**: Author AA, Author BB, Author CC. Title of article. Abbreviated Journal Name. Year;volume(issue):page range.

**Example**: Smith JD, Johnson ML, Williams KR. Machine learning approaches in drug discovery. Nat Rev Drug Discov. 2023;22(4):301-18.

### Books

**Format**: Author AA, Author BB. Title of book. Edition. Place: Publisher; Year.

**Example**: Kumar V, Abbas AK, Aster JC. Robbins and Cotran pathologic basis of disease. 10th ed. Philadelphia: Elsevier; 2021.

### Citation in Text

Use superscript numbers in order of appearance: "Recent studies^1,2^ have shown..."

---

## IEEE Style

### Journal Articles

**Format**: [#] A. A. Author, B. B. Author, and C. C. Author, "Title of article," *Abbreviated Journal Name*, vol. x, no. x, pp. xxx-xxx, Month Year.

**Example**: [1] J. D. Smith, M. L. Johnson, and K. R. Williams, "Machine learning approaches in drug discovery," *Nat. Rev. Drug Discov.*, vol. 22, no. 4, pp. 301-318, Apr. 2023.

### Books

**Format**: [#] A. A. Author, *Title of Book*, xth ed. City, State: Publisher, Year.

**Example**: [2] V. Kumar, A. K. Abbas, and J. C. Aster, *Robbins and Cotran Pathologic Basis of Disease*, 10th ed. Philadelphia, PA: Elsevier, 2021.

---

## Common Abbreviations for Journal Names

- Nature: Nat.
- Science: Science
- Cell: Cell
- Nature Reviews Drug Discovery: Nat. Rev. Drug Discov.
- Journal of the American Chemical Society: J. Am. Chem. Soc.
- Proceedings of the National Academy of Sciences: Proc. Natl. Acad. Sci. U.S.A.
- PLOS ONE: PLoS ONE
- Bioinformatics: Bioinformatics
- Nucleic Acids Research: Nucleic Acids Res.

---

## DOI Best Practices

1. **Always verify DOIs**: Use the verify_citations.py script to check all DOIs
2. **Format as URLs**: https://doi.org/10.xxxx/yyyy (preferred over doi:10.xxxx/yyyy)
3. **No period after DOI**: DOI should be the last element without trailing punctuation
4. **Resolve redirects**: Check that DOIs resolve to the correct article

---

## In-Text Citation Guidelines

### APA Style
- (Smith et al., 2023)
- Smith et al. (2023) demonstrated...
- Multiple citations: (Brown, 2022; Smith et al., 2023; Zhang, 2024)

### Nature Style
- Superscript numbers: Recent studies^1,2^ have shown...
- Or: Recent studies (refs 1,2) have shown...

### Chicago Style
- (Smith, Johnson, and Williams 2023)
- Smith, Johnson, and Williams (2023) found...

---

## Reference List Organization

### By Citation Style
- **APA, Chicago**: Alphabetical by first author's last name
- **Nature, Vancouver, IEEE**: Numerical order of first appearance in text

### Hanging Indents
Most styles use hanging indents where the first line is flush left and subsequent lines are indented.

### Consistency
Maintain consistent formatting throughout:
- Capitalization (title case vs. sentence case)
- Journal name abbreviations
- DOI presentation
- Author name format

---

## Reference: Database_Strategies

# Literature Database Search Strategies

This document provides comprehensive guidance for searching multiple literature databases systematically and effectively.

## Available Databases and Skills

### Biomedical & Life Sciences

#### PubMed / PubMed Central
- **Access**: Use `gget` skill or WebFetch tool
- **Coverage**: 35M+ citations in biomedical literature
- **Best for**: Clinical studies, biomedical research, genetics, molecular biology
- **Search tips**: Use MeSH terms, Boolean operators (AND, OR, NOT), field tags [Title], [Author]
- **Example**: `"CRISPR"[Title] AND "gene editing"[Title/Abstract] AND 2020:2024[Publication Date]`

#### bioRxiv / medRxiv
- **Access**: Use `gget` skill or direct API
- **Coverage**: Preprints in biology and medicine
- **Best for**: Latest unpublished research, cutting-edge findings
- **Note**: Not peer-reviewed; verify findings with caution
- **Search tips**: Search by category (bioinformatics, genomics, etc.)

### General Scientific Literature

#### arXiv
- **Access**: Direct API access
- **Coverage**: Preprints in physics, mathematics, computer science, quantitative biology
- **Best for**: Computational methods, bioinformatics algorithms, theoretical work
- **Categories**: q-bio (Quantitative Biology), cs.LG (Machine Learning), stat.ML (Statistics)
- **Search format**: `cat:q-bio.QM AND title:"single cell"`

#### Semantic Scholar
- **Access**: Direct API (requires API key)
- **Coverage**: 200M+ papers across all fields
- **Best for**: Cross-disciplinary searches, citation graphs, paper recommendations
- **Features**: Influential citations, paper summaries, related papers
- **Rate limits**: 100 requests/5 minutes with API key

#### Google Scholar
- **Access**: Web scraping (use cautiously) or manual search
- **Coverage**: Comprehensive across all fields
- **Best for**: Finding highly cited papers, conference proceedings, theses
- **Limitations**: No official API, rate limiting
- **Export**: Use "Cite" feature for formatted citations

### Specialized Databases

#### ChEMBL / PubChem
- **Access**: Use `gget` skill or `bioservices` skill
- **Coverage**: Chemical compounds, bioactivity data, drug molecules
- **Best for**: Drug discovery, chemical biology, medicinal chemistry
- **ChEMBL**: 2M+ compounds, bioactivity data
- **PubChem**: 110M+ compounds, assay data

#### UniProt
- **Access**: Use `gget` skill or `bioservices` skill
- **Coverage**: Protein sequence and functional information
- **Best for**: Protein research, sequence analysis, functional annotations
- **Search by**: Protein name, gene name, organism, function

#### KEGG (Kyoto Encyclopedia of Genes and Genomes)
- **Access**: Use `bioservices` skill
- **Coverage**: Pathways, diseases, drugs, genes
- **Best for**: Pathway analysis, systems biology, metabolic research

#### COSMIC (Catalogue of Somatic Mutations in Cancer)
- **Access**: Use `gget` skill or direct download
- **Coverage**: Cancer genomics, somatic mutations
- **Best for**: Cancer research, mutation analysis

#### AlphaFold Database
- **Access**: Use `gget` skill with `alphafold` command
- **Coverage**: 200M+ protein structure predictions
- **Best for**: Structural biology, protein modeling

#### PDB (Protein Data Bank)
- **Access**: Use `gget` or direct API
- **Coverage**: Experimental 3D structures of proteins, nucleic acids
- **Best for**: Structural biology, drug design, molecular modeling

### Citation & Reference Management

#### OpenAlex
- **Access**: Direct API (free, no key required)
- **Coverage**: 250M+ works, comprehensive metadata
- **Best for**: Citation analysis, author disambiguation, institutional research
- **Features**: Open access, excellent for bibliometrics

#### Dimensions
- **Access**: Free tier available
- **Coverage**: Publications, grants, patents, clinical trials
- **Best for**: Research impact, funding analysis, translational research

---

## Search Strategy Framework

### 1. Define Research Question (PICO Framework)

For clinical/biomedical reviews:
- **P**opulation: Who is the study about?
- **I**ntervention: What is being tested?
- **C**omparison: What is it compared to?
- **O**utcome: What are the results?

**Example**: "What is the efficacy of CRISPR-Cas9 gene therapy (I) for treating sickle cell disease (P) compared to standard care (C) in improving patient outcomes (O)?"

### 2. Develop Search Terms

#### Primary Concepts
Identify 2-4 main concepts from your research question.

**Example**:
- Concept 1: CRISPR, Cas9, gene editing
- Concept 2: sickle cell disease, SCD, hemoglobin disorders
- Concept 3: gene therapy, therapeutic editing

#### Synonyms & Related Terms
List alternative terms, abbreviations, and related concepts.

**Tool**: Use MeSH (Medical Subject Headings) browser for standardized terms

#### Boolean Operators
- **AND**: Narrows search (must include both terms)
- **OR**: Broadens search (includes either term)
- **NOT**: Excludes terms

**Example**: `(CRISPR OR Cas9 OR "gene editing") AND ("sickle cell" OR SCD) AND therapy`

#### Wildcards & Truncation
- `*` or `%`: Matches any characters
- `?`: Matches single character

**Example**: `genom*` matches genomic, genomics, genome

### 3. Set Inclusion/Exclusion Criteria

#### Inclusion Criteria
- **Date range**: e.g., 2015-2024 (last 10 years)
- **Language**: English (or specify multilingual)
- **Publication type**: Peer-reviewed articles, reviews, preprints
- **Study design**: RCTs, cohort studies, meta-analyses
- **Population**: Human, animal models, in vitro

#### Exclusion Criteria
- Case reports (n<5)
- Conference abstracts without full text
- Non-original research (editorials, commentaries)
- Duplicate publications
- Retracted articles

### 4. Database Selection Strategy

#### Multi-Database Approach
Search at least 3 complementary databases:

1. **Primary database**: PubMed (biomedical) or arXiv (computational)
2. **Preprint server**: bioRxiv/medRxiv or arXiv
3. **Comprehensive database**: Semantic Scholar or Google Scholar
4. **Specialized database**: ChEMBL, UniProt, or field-specific

#### Database-Specific Syntax

| Database | Field Tags | Example |
|----------|-----------|---------|
| PubMed | [Title], [Author], [MeSH] | "CRISPR"[Title] AND 2020:2024[DP] |
| arXiv | ti:, au:, cat: | ti:"machine learning" AND cat:q-bio.QM |
| Semantic Scholar | title:, author:, year: | title:"deep learning" year:2020-2024 |

---

## Search Execution Workflow

### Phase 1: Pilot Search
1. Run initial search with broad terms
2. Review first 50 results for relevance
3. Note common keywords and MeSH terms
4. Refine search strategy

### Phase 2: Comprehensive Search
1. Execute refined searches across all selected databases
2. Export results in standard format (RIS, BibTeX, JSON)
3. Document search strings and date for each database
4. Record number of results per database

### Phase 3: Deduplication
1. Import all results into a single file
2. Use `search_databases.py --deduplicate` to remove duplicates
3. Identify duplicates by DOI (primary) or title (fallback)
4. Keep the version with most complete metadata

### Phase 4: Screening
1. **Title screening**: Review titles, exclude obviously irrelevant
2. **Abstract screening**: Read abstracts, apply inclusion/exclusion criteria
3. **Full-text screening**: Obtain and review full texts
4. Document reasons for exclusion at each stage

### Phase 5: Quality Assessment
1. Assess study quality using appropriate tools:
   - **RCTs**: Cochrane Risk of Bias tool
   - **Observational**: Newcastle-Ottawa Scale
   - **Systematic reviews**: AMSTAR 2
2. Grade quality of evidence (high, moderate, low, very low)
3. Consider excluding very low-quality studies

---

## Search Documentation Template

### Required Documentation
All searches must be documented for reproducibility:

```markdown
## Search Strategy

### Database: PubMed
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**:
  ```
  ("CRISPR"[Title] OR "Cas9"[Title] OR "gene editing"[Title/Abstract])
  AND ("sickle cell disease"[MeSH] OR "SCD"[Title/Abstract])
  AND ("gene therapy"[MeSH] OR "therapeutic editing"[Title/Abstract])
  AND 2015:2024[Publication Date]
  AND English[Language]
  ```
- **Results**: 247 articles
- **After deduplication**: 189 articles

### Database: bioRxiv
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**: "CRISPR" AND "sickle cell" (in title/abstract)
- **Results**: 34 preprints
- **After deduplication**: 28 preprints

### Total Unique Articles
- **Combined results**: 217 unique articles
- **After title screening**: 156 articles
- **After abstract screening**: 89 articles
- **After full-text screening**: 52 articles included in review
```

---

## Advanced Search Techniques

### Prioritizing High-Impact Papers (CRITICAL)

**Always prioritize papers based on citation count, venue quality, and author reputation.** Quality matters more than quantity.

#### Citation Metrics in Database Searches

Use citation counts to identify influential work:

| Paper Age | Citations | Classification |
|-----------|-----------|----------------|
| 0-3 years | 20+ | Noteworthy |
| 0-3 years | 100+ | Highly Influential |
| 3-7 years | 100+ | Significant |
| 3-7 years | 500+ | Landmark |
| 7+ years | 500+ | Seminal |
| 7+ years | 1000+ | Foundational |

**Database-Specific Citation Features:**
- **Google Scholar:** Sort by citation count, use "Cited by" feature
- **Semantic Scholar:** "Highly Influential Citations" metric, citation velocity
- **OpenAlex:** Citation counts, citation context analysis
- **PubMed:** Use "Cited by" in PMC, check citation counts via Google Scholar

#### Filtering by Journal Quality

Prioritize papers from higher-tier venues:

**Tier 1 (Always Prefer):**
- Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS
- Nature Medicine, Nature Biotechnology, Nature Methods
- Search tip: `source:Nature` or `journal:Nature` in Google Scholar

**Tier 2 (High Priority):**
- High-impact specialized journals (Impact Factor >10)
- Top conferences: NeurIPS, ICML, ICLR, CVPR, ACL

**Tier 3 (Include When Relevant):**
- Respected field-specific journals (IF 5-10)

**PubMed Journal Filtering:**
```
"Nature"[Journal] OR "Science"[Journal] OR "Cell"[Journal]
```

**Google Scholar Journal Filtering:**
```
source:Nature source:Science source:Cell
```

#### Leveraging "Cited by" Features

**Finding Influential Work:**
1. Start with a known key paper
2. Click "Cited by" to find papers that cite it
3. Sort citing papers by their citation count
4. Highly-cited citing papers indicate important follow-up work

**Identifying Seminal Papers:**
1. Search your topic broadly
2. Note which papers appear repeatedly in reference lists
3. Papers cited by many of your results are likely seminal
4. Check citation counts to confirm influence

**Semantic Scholar Features:**
- "Highly Influential Citations" shows citations that significantly built on the paper
- "Citation Velocity" shows recent citation growth
- Paper recommendations based on citation networks

### Citation Chaining

#### Forward Citation Search
Find papers that cite a key paper:
- Use Google Scholar "Cited by" feature
- Use OpenAlex or Semantic Scholar APIs
- Identifies newer research building on seminal work
- **Tip:** Sort by citation count to find the most influential follow-up work

#### Backward Citation Search
Review references in key papers:
- Extract references from included papers
- Search for highly cited references (500+ citations for older papers)
- Identifies foundational research
- **Tip:** Focus on references that appear in multiple papers' bibliographies

### Snowball Sampling
1. Start with 3-5 highly relevant papers **from Tier-1 venues**
2. Extract all their references
3. Check which references are cited by multiple papers
4. Review those high-overlap references - these are likely seminal
5. Repeat for newly identified key papers
6. **Prioritize papers with high citation counts** at each step

### Author Search
Follow prolific and reputable authors in the field:
- Search by author name across databases
- Check author profiles (ORCID, Google Scholar) for h-index and publication venues
- Review recent publications and preprints
- **Prefer authors with multiple Tier-1 publications** and high h-index (>40)
- Look for senior authors who are recognized field leaders

### Related Article Features
Many databases suggest related articles:
- PubMed "Similar articles"
- Semantic Scholar "Recommended papers"
- Use to discover papers missed by keyword search
- **Filter recommendations by citation count and venue quality**

---

## Quality Control Checklist

### Before Searching
- [ ] Research question clearly defined
- [ ] PICO criteria established (if applicable)
- [ ] Search terms and synonyms listed
- [ ] Inclusion/exclusion criteria documented
- [ ] Target databases selected (minimum 3)
- [ ] Date range determined

### During Searching
- [ ] Search string tested and refined
- [ ] Results exported with complete metadata
- [ ] Search parameters documented
- [ ] Number of results recorded per database
- [ ] Search date recorded

### After Searching
- [ ] Duplicates removed
- [ ] Screening protocol followed
- [ ] Reasons for exclusion documented
- [ ] Quality assessment completed
- [ ] All citations verified with verify_citations.py
- [ ] Search methodology documented in review

---

## Common Pitfalls to Avoid

1. **Too narrow search**: Missing relevant papers
   - Solution: Include synonyms, related terms, broader concepts

2. **Too broad search**: Thousands of irrelevant results
   - Solution: Add specific concepts with AND, use field tags

3. **Single database**: Incomplete coverage
   - Solution: Search minimum 3 complementary databases

4. **Ignoring preprints**: Missing latest findings
   - Solution: Include bioRxiv, medRxiv, or arXiv

5. **No documentation**: Irreproducible search
   - Solution: Document every search string, date, and result count

6. **Manual deduplication**: Time-consuming and error-prone
   - Solution: Use search_databases.py script

7. **Unverified citations**: Broken DOIs, incorrect metadata
   - Solution: Run verify_citations.py on final reference list

8. **Publication bias**: Only including published positive results
   - Solution: Search trial registries, contact authors for unpublished data

---

## Example Multi-Database Search Workflow

```python
# Example workflow using available skills

# 1. Search PubMed via gget
search_term = "CRISPR AND sickle cell disease"
# Use gget search pubmed search_term

# 2. Search bioRxiv
# Use gget search biorxiv search_term

# 3. Search arXiv for computational papers
# Search arXiv with: cat:q-bio AND "CRISPR" AND "sickle cell"

# 4. Search Semantic Scholar via API
# Use semantic scholar API with search query

# 5. Aggregate and deduplicate results
# python search_databases.py combined_results.json --deduplicate --format markdown --output review_papers.md

# 6. Verify all citations
# python verify_citations.py review_papers.md

# 7. Generate final PDF
# python generate_pdf.py review_papers.md --citation-style nature
```

---

## Resources

### MeSH Browser
https://meshb.nlm.nih.gov/search

### Boolean Search Tutorial
https://www.ncbi.nlm.nih.gov/books/NBK3827/

### Citation Style Guides
See references/citation_styles.md in this skill

### PRISMA Guidelines
Preferred Reporting Items for Systematic Reviews and Meta-Analyses:
http://www.prisma-statement.org/
