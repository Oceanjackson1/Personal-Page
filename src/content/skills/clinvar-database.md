---
title: "Clinvar Database"
description: "Query NCBI ClinVar for variant clinical significance. Search by gene/position, interpret pathogenicity classifications, access via E-utilities API or FTP, annotate VCFs, for genomic medicine."
category: "research"
source: "community"
author: "Community"
tags: ["clinvar", "database"]
date: 2026-03-20
---

# ClinVar Database

## Overview

ClinVar is NCBI's freely accessible archive of reports on relationships between human genetic variants and phenotypes, with supporting evidence. The database aggregates information about genomic variation and its relationship to human health, providing standardized variant classifications used in clinical genetics and research.

## When to Use This Skill

This skill should be used when:

- Searching for variants by gene, condition, or clinical significance
- Interpreting clinical significance classifications (pathogenic, benign, VUS)
- Accessing ClinVar data programmatically via E-utilities API
- Downloading and processing bulk data from FTP
- Understanding review status and star ratings
- Resolving conflicting variant interpretations
- Annotating variant call sets with clinical significance

## Core Capabilities

### 1. Search and Query ClinVar

#### Web Interface Queries

Search ClinVar using the web interface at https://www.ncbi.nlm.nih.gov/clinvar/

**Common search patterns:**
- By gene: `BRCA1[gene]`
- By clinical significance: `pathogenic[CLNSIG]`
- By condition: `breast cancer[disorder]`
- By variant: `NM_000059.3:c.1310_1313del[variant name]`
- By chromosome: `13[chr]`
- Combined: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### Programmatic Access via E-utilities

Access ClinVar programmatically using NCBI's E-utilities API. Refer to `references/api_reference.md` for comprehensive API documentation including:
- **esearch** - Search for variants matching criteria
- **esummary** - Retrieve variant summaries
- **efetch** - Download full XML records
- **elink** - Find related records in other NCBI databases

**Quick example using curl:**
```bash
# Search for pathogenic BRCA1 variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Best practices:**
- Test queries on the web interface before automating
- Use API keys to increase rate limits from 3 to 10 requests/second
- Implement exponential backoff for rate limit errors
- Set `Entrez.email` when using Biopython

### 2. Interpret Clinical Significance

#### Understanding Classifications

ClinVar uses standardized terminology for variant classifications. Refer to `references/clinical_significance.md` for detailed interpretation guidelines.

**Key germline classification terms (ACMG/AMP):**
- **Pathogenic (P)** - Variant causes disease (~99% probability)
- **Likely Pathogenic (LP)** - Variant likely causes disease (~90% probability)
- **Uncertain Significance (VUS)** - Insufficient evidence to classify
- **Likely Benign (LB)** - Variant likely does not cause disease
- **Benign (B)** - Variant does not cause disease

**Review status (star ratings):**
- ★★★★ Practice guideline - Highest confidence
- ★★★ Expert panel review (e.g., ClinGen) - High confidence
- ★★ Multiple submitters, no conflicts - Moderate confidence
- ★ Single submitter with criteria - Standard weight
- ☆ No assertion criteria - Low confidence

**Critical considerations:**
- Always check review status - prefer ★★★ or ★★★★ ratings
- Conflicting interpretations require manual evaluation
- Classifications may change as new evidence emerges
- VUS (uncertain significance) variants lack sufficient evidence for clinical use

### 3. Download Bulk Data from FTP

#### Access ClinVar FTP Site

Download complete datasets from `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/`

Refer to `references/data_formats.md` for comprehensive documentation on file formats and processing.

**Update schedule:**
- Monthly releases: First Thursday of each month (complete dataset, archived)
- Weekly updates: Every Monday (incremental updates)

#### Available Formats

**XML files** (most comprehensive):
- VCV (Variation) files: `xml/clinvar_variation/` - Variant-centric aggregation
- RCV (Record) files: `xml/RCV/` - Variant-condition pairs
- Include full submission details, evidence, and metadata

**VCF files** (for genomic pipelines):
- GRCh37: `vcf_GRCh37/clinvar.vcf.gz`
- GRCh38: `vcf_GRCh38/clinvar.vcf.gz`
- Limitations: Excludes variants >10kb and complex structural variants

**Tab-delimited files** (for quick analysis):
- `tab_delimited/variant_summary.txt.gz` - Summary of all variants
- `tab_delimited/var_citations.txt.gz` - PubMed citations
- `tab_delimited/cross_references.txt.gz` - Database cross-references

**Example download:**
```bash
# Download latest monthly XML release
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# Download VCF for GRCh38
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. Process and Analyze ClinVar Data

#### Working with XML Files

Process XML files to extract variant details, classifications, and evidence.

**Python example with xml.etree:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            variation_id = elem.attrib.get('VariationID')
            # Extract clinical significance, review status, etc.
            elem.clear()  # Free memory
```

#### Working with VCF Files

Annotate variant calls or filter by clinical significance using bcftools or Python.

**Using bcftools:**
```bash
# Filter pathogenic variants
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# Extract specific genes
bcftools view -i 'INFO/GENEINFO~"BRCA"' clinvar.vcf.gz

# Annotate your VCF with ClinVar
bcftools annotate -a clinvar.vcf.gz -c INFO your_variants.vcf
```

**Using PyVCF in Python:**
```python
import vcf

vcf_reader = vcf.Reader(filename='clinvar.vcf.gz')
for record in vcf_reader:
    clnsig = record.INFO.get('CLNSIG', [])
    if 'Pathogenic' in clnsig:
        gene = record.INFO.get('GENEINFO', [''])[0]
        print(f"{record.CHROM}:{record.POS} {gene} - {clnsig}")
```

#### Working with Tab-Delimited Files

Use pandas or command-line tools for rapid filtering and analysis.

**Using pandas:**
```python
import pandas as pd

# Load variant summary
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# Filter pathogenic variants in specific gene
pathogenic_brca = df[
    (df['GeneSymbol'] == 'BRCA1') &
    (df['ClinicalSignificance'].str.contains('Pathogenic', na=False))
]

# Count variants by clinical significance
sig_counts = df['ClinicalSignificance'].value_counts()
```

**Using command-line tools:**
```bash
# Extract pathogenic variants for specific gene
zcat variant_summary.txt.gz | \
  awk -F'\t' '$7=="TP53" && $13~"Pathogenic"' | \
  cut -f1,5,7,13,14
```

### 5. Handle Conflicting Interpretations

When multiple submitters provide different classifications for the same variant, ClinVar reports "Conflicting interpretations of pathogenicity."

**Resolution strategy:**
1. Check review status (star rating) - higher ratings carry more weight
2. Examine evidence and assertion criteria from each submitter
3. Consider submission dates - newer submissions may reflect updated evidence
4. Review population frequency data (e.g., gnomAD) for context
5. Consult expert panel classifications (★★★) when available
6. For clinical use, always defer to a genetics professional

**Search query to exclude conflicts:**
```
TP53[gene] AND pathogenic[CLNSIG] NOT conflicting[RVSTAT]
```

### 6. Track Classification Updates

Variant classifications may change over time as new evidence emerges.

**Why classifications change:**
- New functional studies or clinical data
- Updated population frequency information
- Revised ACMG/AMP guidelines
- Segregation data from additional families

**Best practices:**
- Document ClinVar version and access date for reproducibility
- Re-check classifications periodically for critical variants
- Subscribe to ClinVar mailing list for major updates
- Use monthly archived releases for stable datasets

### 7. Submit Data to ClinVar

Organizations can submit variant interpretations to ClinVar.

**Submission methods:**
- Web submission portal: https://submit.ncbi.nlm.nih.gov/subs/clinvar/
- API submission (requires service account): See `references/api_reference.md`
- Batch submission via Excel templates

**Requirements:**
- Organizational account with NCBI
- Assertion criteria (preferably ACMG/AMP guidelines)
- Supporting evidence for classification

Contact: clinvar@ncbi.nlm.nih.gov for submission account setup.

## Workflow Examples

### Example 1: Identify High-Confidence Pathogenic Variants in a Gene

**Objective:** Find pathogenic variants in CFTR gene with expert panel review.

**Steps:**
1. Search using web interface or E-utilities:
   ```
   CFTR[gene] AND pathogenic[CLNSIG] AND (reviewed by expert panel[RVSTAT] OR practice guideline[RVSTAT])
   ```
2. Review results, noting review status (should be ★★★ or ★★★★)
3. Export variant list or retrieve full records via efetch
4. Cross-reference with clinical presentation if applicable

### Example 2: Annotate VCF with ClinVar Classifications

**Objective:** Add clinical significance annotations to variant calls.

**Steps:**
1. Download appropriate ClinVar VCF (match genome build: GRCh37 or GRCh38):
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi
   ```
2. Annotate using bcftools:
   ```bash
   bcftools annotate -a clinvar.vcf.gz \
     -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT \
     -o annotated_variants.vcf \
     your_variants.vcf
   ```
3. Filter annotated VCF for pathogenic variants:
   ```bash
   bcftools view -i 'INFO/CLNSIG~"Pathogenic"' annotated_variants.vcf
   ```

### Example 3: Analyze Variants for a Specific Disease

**Objective:** Study all variants associated with hereditary breast cancer.

**Steps:**
1. Search by condition:
   ```
   hereditary breast cancer[disorder] OR "Breast-ovarian cancer, familial"[disorder]
   ```
2. Download results as CSV or retrieve via E-utilities
3. Filter by review status to prioritize high-confidence variants
4. Analyze distribution across genes (BRCA1, BRCA2, PALB2, etc.)
5. Examine variants with conflicting interpretations separately

### Example 4: Bulk Download and Database Construction

**Objective:** Build a local ClinVar database for analysis pipeline.

**Steps:**
1. Download monthly release for reproducibility:
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_YYYY-MM.xml.gz
   ```
2. Parse XML and load into database (PostgreSQL, MySQL, MongoDB)
3. Index by gene, position, clinical significance, review status
4. Implement version tracking for updates
5. Schedule monthly updates from FTP site

## Important Limitations and Considerations

### Data Quality
- **Not all submissions have equal weight** - Check review status (star ratings)
- **Conflicting interpretations exist** - Require manual evaluation
- **Historical submissions may be outdated** - Newer data may be more accurate
- **VUS classification is not a clinical diagnosis** - Means insufficient evidence

### Scope Limitations
- **Not for direct clinical diagnosis** - Always involve genetics professional
- **Population-specific** - Variant frequencies vary by ancestry
- **Incomplete coverage** - Not all genes or variants are well-studied
- **Version dependencies** - Coordinate genome build (GRCh37/GRCh38) across analyses

### Technical Limitations
- **VCF files exclude large variants** - Variants >10kb not in VCF format
- **Rate limits on API** - 3 req/sec without key, 10 req/sec with API key
- **File sizes** - Full XML releases are multi-GB compressed files
- **No real-time updates** - Website updated weekly, FTP monthly/weekly

## Resources

### Reference Documentation

This skill includes comprehensive reference documentation:

- **`references/api_reference.md`** - Complete E-utilities API documentation with examples for esearch, esummary, efetch, and elink; includes rate limits, authentication, and Python/Biopython code samples

- **`references/clinical_significance.md`** - Detailed guide to interpreting clinical significance classifications, review status star ratings, conflict resolution, and best practices for variant interpretation

- **`references/data_formats.md`** - Documentation for XML, VCF, and tab-delimited file formats; FTP directory structure, processing examples, and format selection guidance

### External Resources

- ClinVar home: https://www.ncbi.nlm.nih.gov/clinvar/
- ClinVar documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/
- E-utilities documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ACMG variant interpretation guidelines: Richards et al., 2015 (PMID: 25741868)
- ClinGen expert panels: https://clinicalgenome.org/

### Contact

For questions about ClinVar or data submission: clinvar@ncbi.nlm.nih.gov

---

## Reference: Api_Reference

# ClinVar API and Data Access Reference

## Overview

ClinVar provides multiple methods for programmatic data access:
- **E-utilities** - NCBI's REST API for searching and retrieving data
- **Entrez Direct** - Command-line tools for UNIX environments
- **FTP Downloads** - Bulk data files in XML, VCF, and tab-delimited formats
- **Submission API** - REST API for submitting variant interpretations

## E-utilities API

### Base URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

### Supported Operations

#### 1. esearch - Search for Records
Search ClinVar using the same query syntax as the web interface.

**Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
```

**Parameters:**
- `db=clinvar` - Database name (required)
- `term=<query>` - Search query (required)
- `retmax=<N>` - Maximum records to return (default: 20)
- `retmode=json` - Return format (json or xml)
- `usehistory=y` - Store results on server for large datasets

**Example Query:**
```bash
# Search for BRCA1 pathogenic variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json&retmax=100"
```

**Common Search Fields:**
- `[gene]` - Gene symbol
- `[CLNSIG]` - Clinical significance (pathogenic, benign, etc.)
- `[disorder]` - Disease/condition name
- `[variant name]` - HGVS expression or variant identifier
- `[chr]` - Chromosome number
- `[Assembly]` - GRCh37 or GRCh38

#### 2. esummary - Retrieve Record Summaries
Get summary information for specific ClinVar records.

**Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
```

**Parameters:**
- `db=clinvar` - Database name (required)
- `id=<UIDs>` - Comma-separated list of ClinVar UIDs
- `retmode=json` - Return format (json or xml)
- `version=2.0` - API version (recommended for JSON)

**Example:**
```bash
# Get summary for specific variant
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=12345&retmode=json&version=2.0"
```

**esummary Output Includes:**
- Accession (RCV/VCV)
- Clinical significance
- Review status
- Gene symbols
- Variant type
- Genomic locations (GRCh37 and GRCh38)
- Associated conditions
- Allele origin (germline/somatic)

#### 3. efetch - Retrieve Full Records
Download complete XML records for detailed analysis.

**Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
```

**Parameters:**
- `db=clinvar` - Database name (required)
- `id=<UIDs>` - Comma-separated ClinVar UIDs
- `rettype=vcv` or `rettype=rcv` - Record type

**Example:**
```bash
# Fetch full VCV record
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&id=12345&rettype=vcv"
```

#### 4. elink - Find Related Records
Link ClinVar records to other NCBI databases.

**Endpoint:**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi
```

**Available Links:**
- clinvar_pubmed - Link to PubMed citations
- clinvar_gene - Link to Gene database
- clinvar_medgen - Link to MedGen (conditions)
- clinvar_snp - Link to dbSNP

**Example:**
```bash
# Find PubMed articles for a variant
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=clinvar&db=pubmed&id=12345"
```

### Workflow Example: Complete Search and Retrieval

```bash
# Step 1: Search for variants
SEARCH_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=CFTR[gene]+AND+pathogenic[CLNSIG]&retmode=json&retmax=10"

# Step 2: Parse IDs from search results
# (Extract id list from JSON response)

# Step 3: Retrieve summaries
SUMMARY_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=<ids>&retmode=json&version=2.0"

# Step 4: Fetch full records if needed
FETCH_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&id=<ids>&rettype=vcv"
```

## Entrez Direct (Command-Line)

Install Entrez Direct for command-line access:
```bash
sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
```

### Common Commands

**Search:**
```bash
esearch -db clinvar -query "BRCA1[gene] AND pathogenic[CLNSIG]"
```

**Pipeline Search to Summary:**
```bash
esearch -db clinvar -query "TP53[gene]" | \
  efetch -format docsum | \
  xtract -pattern DocumentSummary -element AccessionVersion Title
```

**Count Results:**
```bash
esearch -db clinvar -query "breast cancer[disorder]" | \
  efilter -status reviewed | \
  efetch -format docsum
```

## Rate Limits and Best Practices

### Rate Limits
- **Without API Key:** 3 requests/second
- **With API Key:** 10 requests/second
- Large datasets: Use `usehistory=y` to avoid repeated queries

### API Key Setup
1. Register for NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Generate API key in account settings
3. Add `&api_key=<YOUR_KEY>` to all requests

### Best Practices
- Test queries on web interface before automation
- Use `usehistory` for large result sets (>500 records)
- Implement exponential backoff for rate limit errors
- Cache results when appropriate
- Use batch requests instead of individual queries
- Respect NCBI servers - don't submit large jobs during peak US hours

## Python Example with Biopython

```python
from Bio import Entrez

# Set email (required by NCBI)
Entrez.email = "your.email@example.com"

# Search ClinVar
def search_clinvar(query, retmax=100):
    handle = Entrez.esearch(db="clinvar", term=query, retmax=retmax)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

# Get summaries
def get_summaries(id_list):
    ids = ",".join(id_list)
    handle = Entrez.esummary(db="clinvar", id=ids, retmode="json")
    record = Entrez.read(handle)
    handle.close()
    return record

# Example usage
variant_ids = search_clinvar("BRCA2[gene] AND pathogenic[CLNSIG]")
summaries = get_summaries(variant_ids)
```

## Error Handling

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad request (check query syntax)
- `429` - Too many requests (rate limited)
- `500` - Server error (retry with exponential backoff)

### Error Response Example
```xml
<ERROR>Empty id list - nothing to do</ERROR>
```

## Additional Resources

- NCBI E-utilities documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ClinVar web services: https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/
- Entrez Direct cookbook: https://www.ncbi.nlm.nih.gov/books/NBK179288/

---

## Reference: Clinical_Significance

# ClinVar Clinical Significance Interpretation Guide

## Overview

ClinVar uses standardized terminology to describe the clinical significance of genetic variants. Understanding these classifications is critical for interpreting variant reports and making informed research or clinical decisions.

## Important Disclaimer

**ClinVar data is NOT intended for direct diagnostic use or medical decision-making without review by a genetics professional.** The interpretations in ClinVar represent submitted data from various sources and should be evaluated in the context of the specific patient and clinical scenario.

## Three Classification Categories

ClinVar represents three distinct types of variant classifications:

1. **Germline variants** - Inherited variants related to Mendelian diseases and drug responses
2. **Somatic variants (Clinical Impact)** - Acquired variants with therapeutic implications
3. **Somatic variants (Oncogenicity)** - Acquired variants related to cancer development

## Germline Variant Classifications

### Standard ACMG/AMP Terms

These are the five core terms recommended by the American College of Medical Genetics and Genomics (ACMG) and Association for Molecular Pathology (AMP):

| Term | Abbreviation | Meaning | Probability |
|------|--------------|---------|-------------|
| **Pathogenic** | P | Variant causes disease | ~99% |
| **Likely Pathogenic** | LP | Variant likely causes disease | ~90% |
| **Uncertain Significance** | VUS | Insufficient evidence to classify | N/A |
| **Likely Benign** | LB | Variant likely does not cause disease | ~90% non-pathogenic |
| **Benign** | B | Variant does not cause disease | ~99% non-pathogenic |

### Low-Penetrance and Risk Allele Terms

ClinGen recommends additional terms for variants with incomplete penetrance or risk associations:

- **Pathogenic, low penetrance** - Disease-causing but not all carriers develop disease
- **Likely pathogenic, low penetrance** - Probably disease-causing with incomplete penetrance
- **Established risk allele** - Confirmed association with increased disease risk
- **Likely risk allele** - Probable association with increased disease risk
- **Uncertain risk allele** - Unclear risk association

### Additional Classification Terms

- **Drug response** - Variants affecting medication efficacy or metabolism
- **Association** - Statistical association with trait/disease
- **Protective** - Variants that reduce disease risk
- **Affects** - Variants that affect a biological function
- **Other** - Classifications that don't fit standard categories
- **Not provided** - No classification submitted

### Special Considerations

**Recessive Disorders:**
A disease-causing variant for an autosomal recessive disorder should be classified as "Pathogenic," even though heterozygous carriers will not develop disease. The classification describes the variant's effect, not the carrier status.

**Compound Heterozygotes:**
Each variant is classified independently. Two "Likely Pathogenic" variants in trans can together cause recessive disease, but each maintains its individual classification.

## Somatic Variant Classifications

### Clinical Impact (AMP/ASCO/CAP Tiers)

Based on guidelines from the Association for Molecular Pathology (AMP), American Society of Clinical Oncology (ASCO), and College of American Pathologists (CAP):

| Tier | Meaning |
|------|---------|
| **Tier I - Strong** | Variants with strong clinical significance - FDA-approved therapies or professional guidelines |
| **Tier II - Potential** | Variants with potential clinical actionability - emerging evidence |
| **Tier III - Uncertain** | Variants of unknown clinical significance |
| **Tier IV - Benign/Likely Benign** | Variants with no therapeutic implications |

### Oncogenicity (ClinGen/CGC/VICC)

Based on standards from ClinGen, Cancer Genomics Consortium (CGC), and Variant Interpretation for Cancer Consortium (VICC):

| Term | Meaning |
|------|---------|
| **Oncogenic** | Variant drives cancer development |
| **Likely Oncogenic** | Variant probably drives cancer development |
| **Uncertain Significance** | Insufficient evidence for oncogenicity |
| **Likely Benign** | Variant probably does not drive cancer |
| **Benign** | Variant does not drive cancer |

## Review Status and Star Ratings

ClinVar assigns review status ratings to indicate the strength of evidence behind classifications:

| Stars | Review Status | Description | Weight |
|-------|---------------|-------------|--------|
| ★★★★ | **Practice Guideline** | Reviewed by expert panel with published guidelines | Highest |
| ★★★ | **Expert Panel Review** | Reviewed by expert panel (e.g., ClinGen) | High |
| ★★ | **Multiple Submitters, No Conflicts** | ≥2 submitters with same classification | Moderate |
| ★ | **Criteria Provided, Single Submitter** | One submitter with supporting evidence | Standard |
| ☆ | **No Assertion Criteria** | Classification without documented criteria | Lowest |
| ☆ | **No Assertion Provided** | No classification submitted | None |

### What the Stars Mean

- **4 stars**: Highest confidence - vetted by expert panels, used in clinical practice guidelines
- **3 stars**: High confidence - expert panel review (e.g., ClinGen Variant Curation Expert Panel)
- **2 stars**: Moderate confidence - consensus among multiple independent submitters
- **1 star**: Single submitter with evidence - quality depends on submitter expertise
- **0 stars**: Low confidence - insufficient evidence or no criteria provided

## Conflicting Interpretations

### What Constitutes a Conflict?

As of June 2022, conflicts are reported between:
- Pathogenic/likely pathogenic **vs.** Uncertain significance
- Pathogenic/likely pathogenic **vs.** Benign/likely benign
- Uncertain significance **vs.** Benign/likely benign

### Conflict Resolution

When conflicts exist, ClinVar reports:
- **"Conflicting interpretations of pathogenicity"** - Disagreement on clinical significance
- Individual submissions are displayed so users can evaluate evidence
- Higher review status (more stars) carries more weight
- More recent submissions may reflect updated evidence

### Handling Conflicts in Research

When encountering conflicts:
1. Check the review status (star rating) of each interpretation
2. Examine the evidence and criteria provided by each submitter
3. Consider the date of submission (more recent may reflect new data)
4. Review population frequency data and functional studies
5. Consult expert panel classifications when available

## Aggregate Classifications

ClinVar calculates an aggregate classification when multiple submitters provide interpretations:

### No Conflicts
When all submitters agree (within the same category):
- Display: Single classification term
- Confidence: Higher with more submitters

### With Conflicts
When submitters disagree:
- Display: "Conflicting interpretations of pathogenicity"
- Details: All individual submissions shown
- Resolution: Users must evaluate evidence themselves

## Interpretation Best Practices

### For Researchers

1. **Always check review status** - Prefer variants with ★★★ or ★★★★ ratings
2. **Review submission details** - Examine evidence supporting classification
3. **Consider publication date** - Newer classifications may incorporate recent data
4. **Check assertion criteria** - Variants with ACMG criteria are more reliable
5. **Verify in context** - Population, ethnicity, and phenotype matter
6. **Follow up on conflicts** - Investigate discrepancies before making conclusions

### For Variant Annotation Pipelines

1. Prioritize higher review status classifications
2. Flag conflicting interpretations for manual review
3. Track classification changes over time
4. Include population frequency data alongside ClinVar classifications
5. Document ClinVar version and access date

### Red Flags

Be cautious with variants that have:
- Zero or one star rating
- Conflicting interpretations without resolution
- Classification as VUS (uncertain significance)
- Very old submission dates without updates
- Classification based on in silico predictions alone

## Common Query Patterns

### Search for High-Confidence Pathogenic Variants

```
BRCA1[gene] AND pathogenic[CLNSIG] AND practice guideline[RVSTAT]
```

### Filter by Review Status

```
TP53[gene] AND (reviewed by expert panel[RVSTAT] OR practice guideline[RVSTAT])
```

### Exclude Conflicting Interpretations

```
CFTR[gene] AND pathogenic[CLNSIG] NOT conflicting[RVSTAT]
```

## Updates and Reclassifications

### Why Classifications Change

Variants may be reclassified due to:
- New functional studies
- Additional population data (e.g., gnomAD)
- Updated ACMG guidelines
- Clinical evidence from more patients
- Segregation data from families

### Tracking Changes

- ClinVar maintains submission history
- Version-controlled VCV/RCV accessions
- Monthly updates to classifications
- Reclassifications can go in either direction (upgrade or downgrade)

## Key Resources

- ACMG/AMP Variant Interpretation Guidelines: Richards et al., 2015
- ClinGen Sequence Variant Interpretation Working Group: https://clinicalgenome.org/
- ClinVar Clinical Significance Documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/clinsig/
- Review Status Documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/

---

## Reference: Data_Formats

# ClinVar Data Formats and FTP Access

## Overview

ClinVar provides bulk data downloads in multiple formats to support different research workflows. Data is distributed via FTP and updated on regular schedules.

## FTP Access

### Base URL
```
ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/
```

### Update Schedule

- **Monthly Releases**: First Thursday of each month
  - Complete dataset with comprehensive documentation
  - Archived indefinitely for reproducibility
  - Includes release notes

- **Weekly Updates**: Every Monday
  - Incremental updates to monthly release
  - Retained until next monthly release
  - Allows synchronization with ClinVar website

### Directory Structure

```
pub/clinvar/
├── xml/                          # XML data files
│   ├── clinvar_variation/       # VCV files (variant-centric)
│   │   ├── weekly_release/      # Weekly updates
│   │   └── archive/             # Monthly archives
│   └── RCV/                     # RCV files (variant-condition pairs)
│       ├── weekly_release/
│       └── archive/
├── vcf_GRCh37/                  # VCF files (GRCh37/hg19)
├── vcf_GRCh38/                  # VCF files (GRCh38/hg38)
├── tab_delimited/               # Tab-delimited summary files
│   ├── variant_summary.txt.gz
│   ├── var_citations.txt.gz
│   └── cross_references.txt.gz
└── README.txt                   # Format documentation
```

## Data Formats

### 1. XML Format (Primary Distribution)

XML provides the most comprehensive data with full submission details, evidence, and metadata.

#### VCV (Variation) Files
- **Purpose**: Variant-centric aggregation
- **Location**: `xml/clinvar_variation/`
- **Accession format**: VCV000000001.1
- **Best for**: Queries focused on specific variants regardless of condition
- **File naming**: `ClinVarVariationRelease_YYYY-MM-DD.xml.gz`

**VCV Record Structure:**
```xml
<VariationArchive VariationID="12345" VariationType="single nucleotide variant">
  <VariationName>NM_000059.3(BRCA2):c.1310_1313del (p.Lys437fs)</VariationName>
  <InterpretedRecord>
    <Interpretations>
      <InterpretedConditionList>
        <InterpretedCondition>Breast-ovarian cancer, familial 2</InterpretedCondition>
      </InterpretedConditionList>
      <ClinicalSignificance>Pathogenic</ClinicalSignificance>
      <ReviewStatus>reviewed by expert panel</ReviewStatus>
    </Interpretations>
  </InterpretedRecord>
  <ClinicalAssertionList>
    <!-- Individual submissions -->
  </ClinicalAssertionList>
</VariationArchive>
```

#### RCV (Record) Files
- **Purpose**: Variant-condition pair aggregation
- **Location**: `xml/RCV/`
- **Accession format**: RCV000000001.1
- **Best for**: Queries focused on variant-disease relationships
- **File naming**: `ClinVarRCVRelease_YYYY-MM-DD.xml.gz`

**Key differences from VCV:**
- One RCV per variant-condition combination
- A single variant may have multiple RCV records (different conditions)
- More focused on clinical interpretation per disease

#### SCV (Submission) Records
- **Format**: Individual submissions within VCV/RCV records
- **Accession format**: SCV000000001.1
- **Content**: Submitter-specific interpretations and evidence

### 2. VCF Format

Variant Call Format files for genomic analysis pipelines.

#### Locations
- **GRCh37/hg19**: `vcf_GRCh37/clinvar.vcf.gz`
- **GRCh38/hg38**: `vcf_GRCh38/clinvar.vcf.gz`

#### Content Limitations
- **Included**: Simple alleles with precise genomic coordinates
- **Excluded**:
  - Variants >10 kb
  - Cytogenetic variants
  - Complex structural variants
  - Variants without precise breakpoints

#### VCF INFO Fields

Key INFO fields in ClinVar VCF:

| Field | Description |
|-------|-------------|
| **ALLELEID** | ClinVar allele identifier |
| **CLNSIG** | Clinical significance |
| **CLNREVSTAT** | Review status |
| **CLNDN** | Condition name(s) |
| **CLNVC** | Variant type (SNV, deletion, etc.) |
| **CLNVCSO** | Sequence ontology term |
| **GENEINFO** | Gene symbol:gene ID |
| **MC** | Molecular consequence |
| **RS** | dbSNP rsID |
| **AF_ESP** | Allele frequency (ESP) |
| **AF_EXAC** | Allele frequency (ExAC) |
| **AF_TGP** | Allele frequency (1000 Genomes) |

#### Example VCF Line
```
#CHROM  POS     ID      REF  ALT  QUAL  FILTER  INFO
13      32339912  rs80357382  A    G    .     .     ALLELEID=38447;CLNDN=Breast-ovarian_cancer,_familial_2;CLNSIG=Pathogenic;CLNREVSTAT=reviewed_by_expert_panel;GENEINFO=BRCA2:675
```

### 3. Tab-Delimited Format

Summary files for quick analysis and database loading.

#### variant_summary.txt
Primary summary file with selected metadata for all genome-mapped variants.

**Key Columns:**
- `VariationID` - ClinVar variation identifier
- `Type` - Variant type (SNV, indel, CNV, etc.)
- `Name` - Variant name (typically HGVS)
- `GeneID` - NCBI Gene ID
- `GeneSymbol` - Gene symbol
- `ClinicalSignificance` - Classification
- `ReviewStatus` - Star rating level
- `LastEvaluated` - Date of last review
- `RS# (dbSNP)` - dbSNP rsID if available
- `Chromosome` - Chromosome
- `PositionVCF` - Position (GRCh38)
- `ReferenceAlleleVCF` - Reference allele
- `AlternateAlleleVCF` - Alternate allele
- `Assembly` - Reference assembly (GRCh37/GRCh38)
- `PhenotypeIDS` - MedGen/OMIM/Orphanet IDs
- `Origin` - Germline, somatic, de novo, etc.
- `SubmitterCategories` - Submitter types (clinical, research, etc.)

**Example Usage:**
```bash
# Extract all pathogenic BRCA1 variants
zcat variant_summary.txt.gz | \
  awk -F'\t' '$7=="BRCA1" && $13~"Pathogenic"' | \
  cut -f1,7,13,14
```

#### var_citations.txt
Cross-references to PubMed articles, dbSNP, and dbVar.

**Columns:**
- `AlleleID` - ClinVar allele ID
- `VariationID` - ClinVar variation ID
- `rs` - dbSNP rsID
- `nsv/esv` - dbVar IDs
- `PubMedID` - PubMed citation

#### cross_references.txt
Database cross-references with modification dates.

**Columns:**
- `VariationID`
- `Database` (OMIM, UniProtKB, GTR, etc.)
- `Identifier`
- `DateLastModified`

## Choosing the Right Format

### Use XML when:
- Need complete submission details
- Want to track evidence and criteria
- Building comprehensive variant databases
- Require full metadata and relationships

### Use VCF when:
- Integrating with genomic analysis pipelines
- Annotating variant calls from sequencing
- Need genomic coordinates for overlap analysis
- Working with standard bioinformatics tools

### Use Tab-Delimited when:
- Quick database queries and filters
- Loading into spreadsheets or databases
- Simple data extraction and statistics
- Don't need full evidence details

## Accession Types and Identifiers

### VCV (Variation Archive)
- **Format**: VCV000012345.6 (ID.version)
- **Scope**: Aggregates all data for a single variant
- **Versioning**: Increments when variant data changes

### RCV (Record)
- **Format**: RCV000056789.4
- **Scope**: One variant-condition interpretation
- **Versioning**: Increments when interpretation changes

### SCV (Submission)
- **Format**: SCV000098765.2
- **Scope**: Individual submitter's interpretation
- **Versioning**: Increments when submission updates

### Other Identifiers
- **VariationID**: Stable numeric identifier for variants
- **AlleleID**: Stable numeric identifier for alleles
- **dbSNP rsID**: Cross-reference to dbSNP (when available)

## File Processing Tips

### XML Processing

**Python with xml.etree:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            # Process variant
            variation_id = elem.attrib.get('VariationID')
            # Extract data
            elem.clear()  # Free memory
```

**Command-line with xmllint:**
```bash
# Extract pathogenic variants
zcat ClinVarVariationRelease.xml.gz | \
  xmllint --xpath "//VariationArchive[.//ClinicalSignificance[text()='Pathogenic']]" -
```

### VCF Processing

**Using bcftools:**
```bash
# Filter by clinical significance
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# Extract specific genes
bcftools view -i 'INFO/GENEINFO~"BRCA"' clinvar.vcf.gz

# Annotate your VCF
bcftools annotate -a clinvar.vcf.gz -c INFO your_variants.vcf
```

**Using PyVCF:**
```python
import vcf

vcf_reader = vcf.Reader(filename='clinvar.vcf.gz')
for record in vcf_reader:
    clnsig = record.INFO.get('CLNSIG', [])
    if 'Pathogenic' in clnsig:
        print(f"{record.CHROM}:{record.POS} - {clnsig}")
```

### Tab-Delimited Processing

**Using pandas:**
```python
import pandas as pd

# Read variant summary
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# Filter pathogenic variants
pathogenic = df[df['ClinicalSignificance'].str.contains('Pathogenic', na=False)]

# Group by gene
gene_counts = pathogenic.groupby('GeneSymbol').size().sort_values(ascending=False)
```

## Data Quality Considerations

### Known Limitations

1. **VCF files exclude large variants** - Variants >10 kb not included
2. **Historical data may be less accurate** - Older submissions had fewer standardization requirements
3. **Conflicting interpretations exist** - Multiple submitters may disagree
4. **Not all variants have genomic coordinates** - Some HGVS expressions can't be mapped

### Validation Recommendations

- Cross-reference multiple data formats when possible
- Check review status (prefer ★★★ or ★★★★ ratings)
- Verify genomic coordinates against current genome builds
- Consider population frequency data (gnomAD) for context
- Review submission dates - newer data may be more accurate

## Bulk Download Scripts

### Download Latest Monthly Release

```bash
#!/bin/bash
# Download latest ClinVar monthly XML release

BASE_URL="ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation"

# Get latest file
LATEST=$(curl -s ${BASE_URL}/ | \
         grep -oP 'ClinVarVariationRelease_\d{4}-\d{2}\.xml\.gz' | \
         tail -1)

# Download
wget ${BASE_URL}/${LATEST}
```

### Download All Formats

```bash
#!/bin/bash
# Download ClinVar in all formats

FTP_BASE="ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar"

# XML
wget ${FTP_BASE}/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# VCF (both assemblies)
wget ${FTP_BASE}/vcf_GRCh37/clinvar.vcf.gz
wget ${FTP_BASE}/vcf_GRCh38/clinvar.vcf.gz

# Tab-delimited
wget ${FTP_BASE}/tab_delimited/variant_summary.txt.gz
wget ${FTP_BASE}/tab_delimited/var_citations.txt.gz
```

## Additional Resources

- ClinVar FTP Primer: https://www.ncbi.nlm.nih.gov/clinvar/docs/ftp_primer/
- XML Schema Documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/xml_schemas/
- VCF Specification: https://samtools.github.io/hts-specs/VCFv4.3.pdf
- Release Notes: https://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/README.txt
