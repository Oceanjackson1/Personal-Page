---
title: "Gwas Database"
description: "Query NHGRI-EBI GWAS Catalog for SNP-trait associations. Search variants by rs ID, disease/trait, gene, retrieve p-values and summary statistics, for genetic epidemiology and polygenic risk scores."
category: "research"
source: "community"
author: "Community"
tags: ["gwas", "database"]
date: 2026-03-20
---

# GWAS Catalog Database

## Overview

The GWAS Catalog is a comprehensive repository of published genome-wide association studies maintained by the National Human Genome Research Institute (NHGRI) and the European Bioinformatics Institute (EBI). The catalog contains curated SNP-trait associations from thousands of GWAS publications, including genetic variants, associated traits and diseases, p-values, effect sizes, and full summary statistics for many studies.

## When to Use This Skill

This skill should be used when queries involve:

- **Genetic variant associations**: Finding SNPs associated with diseases or traits
- **SNP lookups**: Retrieving information about specific genetic variants (rs IDs)
- **Trait/disease searches**: Discovering genetic associations for phenotypes
- **Gene associations**: Finding variants in or near specific genes
- **GWAS summary statistics**: Accessing complete genome-wide association data
- **Study metadata**: Retrieving publication and cohort information
- **Population genetics**: Exploring ancestry-specific associations
- **Polygenic risk scores**: Identifying variants for risk prediction models
- **Functional genomics**: Understanding variant effects and genomic context
- **Systematic reviews**: Comprehensive literature synthesis of genetic associations

## Core Capabilities

### 1. Understanding GWAS Catalog Data Structure

The GWAS Catalog is organized around four core entities:

- **Studies**: GWAS publications with metadata (PMID, author, cohort details)
- **Associations**: SNP-trait associations with statistical evidence (p ≤ 5×10⁻⁸)
- **Variants**: Genetic markers (SNPs) with genomic coordinates and alleles
- **Traits**: Phenotypes and diseases (mapped to EFO ontology terms)

**Key Identifiers:**
- Study accessions: `GCST` IDs (e.g., GCST001234)
- Variant IDs: `rs` numbers (e.g., rs7903146) or `variant_id` format
- Trait IDs: EFO terms (e.g., EFO_0001360 for type 2 diabetes)
- Gene symbols: HGNC approved names (e.g., TCF7L2)

### 2. Web Interface Searches

The web interface at https://www.ebi.ac.uk/gwas/ supports multiple search modes:

**By Variant (rs ID):**
```
rs7903146
```
Returns all trait associations for this SNP.

**By Disease/Trait:**
```
type 2 diabetes
Parkinson disease
body mass index
```
Returns all associated genetic variants.

**By Gene:**
```
APOE
TCF7L2
```
Returns variants in or near the gene region.

**By Chromosomal Region:**
```
10:114000000-115000000
```
Returns variants in the specified genomic interval.

**By Publication:**
```
PMID:20581827
Author: McCarthy MI
GCST001234
```
Returns study details and all reported associations.

### 3. REST API Access

The GWAS Catalog provides two REST APIs for programmatic access:

**Base URLs:**
- GWAS Catalog API: `https://www.ebi.ac.uk/gwas/rest/api`
- Summary Statistics API: `https://www.ebi.ac.uk/gwas/summary-statistics/api`

**API Documentation:**
- Main API docs: https://www.ebi.ac.uk/gwas/rest/docs/api
- Summary stats docs: https://www.ebi.ac.uk/gwas/summary-statistics/docs/

**Core Endpoints:**

1. **Studies endpoint** - `/studies/{accessionID}`
   ```python
   import requests

   # Get a specific study
   url = "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   study = response.json()
   ```

2. **Associations endpoint** - `/associations`
   ```python
   # Find associations for a variant
   variant = "rs7903146"
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{variant}/associations"
   params = {"projection": "associationBySnp"}
   response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
   associations = response.json()
   ```

3. **Variants endpoint** - `/singleNucleotidePolymorphisms/{rsID}`
   ```python
   # Get variant details
   url = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7903146"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   variant_info = response.json()
   ```

4. **Traits endpoint** - `/efoTraits/{efoID}`
   ```python
   # Get trait information
   url = "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/EFO_0001360"
   response = requests.get(url, headers={"Content-Type": "application/json"})
   trait_info = response.json()
   ```

### 4. Query Examples and Patterns

**Example 1: Find all associations for a disease**
```python
import requests

trait = "EFO_0001360"  # Type 2 diabetes
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Query associations for this trait
url = f"{base_url}/efoTraits/{trait}/associations"
response = requests.get(url, headers={"Content-Type": "application/json"})
associations = response.json()

# Process results
for assoc in associations.get('_embedded', {}).get('associations', []):
    variant = assoc.get('rsId')
    pvalue = assoc.get('pvalue')
    risk_allele = assoc.get('strongestAllele')
    print(f"{variant}: p={pvalue}, risk allele={risk_allele}")
```

**Example 2: Get variant information and all trait associations**
```python
import requests

variant = "rs7903146"
base_url = "https://www.ebi.ac.uk/gwas/rest/api"

# Get variant details
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}"
response = requests.get(url, headers={"Content-Type": "application/json"})
variant_data = response.json()

# Get all associations for this variant
url = f"{base_url}/singleNucleotidePolymorphisms/{variant}/associations"
params = {"projection": "associationBySnp"}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
associations = response.json()

# Extract trait names and p-values
for assoc in associations.get('_embedded', {}).get('associations', []):
    trait = assoc.get('efoTrait')
    pvalue = assoc.get('pvalue')
    print(f"Trait: {trait}, p-value: {pvalue}")
```

**Example 3: Access summary statistics**
```python
import requests

# Query summary statistics API
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"

# Find associations by trait with p-value threshold
trait = "EFO_0001360"  # Type 2 diabetes
p_upper = "0.000000001"  # p < 1e-9
url = f"{base_url}/traits/{trait}/associations"
params = {
    "p_upper": p_upper,
    "size": 100  # Number of results
}
response = requests.get(url, params=params)
results = response.json()

# Process genome-wide significant hits
for hit in results.get('_embedded', {}).get('associations', []):
    variant_id = hit.get('variant_id')
    chromosome = hit.get('chromosome')
    position = hit.get('base_pair_location')
    pvalue = hit.get('p_value')
    print(f"{chromosome}:{position} ({variant_id}): p={pvalue}")
```

**Example 4: Query by chromosomal region**
```python
import requests

# Find variants in a specific genomic region
chromosome = "10"
start_pos = 114000000
end_pos = 115000000

base_url = "https://www.ebi.ac.uk/gwas/rest/api"
url = f"{base_url}/singleNucleotidePolymorphisms/search/findByChromBpLocationRange"
params = {
    "chrom": chromosome,
    "bpStart": start_pos,
    "bpEnd": end_pos
}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
variants_in_region = response.json()
```

### 5. Working with Summary Statistics

The GWAS Catalog hosts full summary statistics for many studies, providing access to all tested variants (not just genome-wide significant hits).

**Access Methods:**
1. **FTP download**: http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/
2. **REST API**: Query-based access to summary statistics
3. **Web interface**: Browse and download via the website

**Summary Statistics API Features:**
- Filter by chromosome, position, p-value
- Query specific variants across studies
- Retrieve effect sizes and allele frequencies
- Access harmonized and standardized data

**Example: Download summary statistics for a study**
```python
import requests
import gzip

# Get available summary statistics
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/studies/GCST001234"
response = requests.get(url)
study_info = response.json()

# Download link is provided in the response
# Alternatively, use FTP:
# ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/
```

### 6. Data Integration and Cross-referencing

The GWAS Catalog provides links to external resources:

**Genomic Databases:**
- Ensembl: Gene annotations and variant consequences
- dbSNP: Variant identifiers and population frequencies
- gnomAD: Population allele frequencies

**Functional Resources:**
- Open Targets: Target-disease associations
- PGS Catalog: Polygenic risk scores
- UCSC Genome Browser: Genomic context

**Phenotype Resources:**
- EFO (Experimental Factor Ontology): Standardized trait terms
- OMIM: Disease gene relationships
- Disease Ontology: Disease hierarchies

**Following Links in API Responses:**
```python
import requests

# API responses include _links for related resources
response = requests.get("https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001234")
study = response.json()

# Follow link to associations
associations_url = study['_links']['associations']['href']
associations_response = requests.get(associations_url)
```

## Query Workflows

### Workflow 1: Exploring Genetic Associations for a Disease

1. **Identify the trait** using EFO terms or free text:
   - Search web interface for disease name
   - Note the EFO ID (e.g., EFO_0001360 for type 2 diabetes)

2. **Query associations via API:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{efo_id}/associations"
   ```

3. **Filter by significance and population:**
   - Check p-values (genome-wide significant: p ≤ 5×10⁻⁸)
   - Review ancestry information in study metadata
   - Filter by sample size or discovery/replication status

4. **Extract variant details:**
   - rs IDs for each association
   - Effect alleles and directions
   - Effect sizes (odds ratios, beta coefficients)
   - Population allele frequencies

5. **Cross-reference with other databases:**
   - Look up variant consequences in Ensembl
   - Check population frequencies in gnomAD
   - Explore gene function and pathways

### Workflow 2: Investigating a Specific Genetic Variant

1. **Query the variant:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
   ```

2. **Retrieve all trait associations:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
   ```

3. **Analyze pleiotropy:**
   - Identify all traits associated with this variant
   - Review effect directions across traits
   - Look for shared biological pathways

4. **Check genomic context:**
   - Determine nearby genes
   - Identify if variant is in coding/regulatory regions
   - Review linkage disequilibrium with other variants

### Workflow 3: Gene-Centric Association Analysis

1. **Search by gene symbol** in web interface or:
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
   params = {"geneName": gene_symbol}
   ```

2. **Retrieve variants in gene region:**
   - Get chromosomal coordinates for gene
   - Query variants in region
   - Include promoter and regulatory regions (extend boundaries)

3. **Analyze association patterns:**
   - Identify traits associated with variants in this gene
   - Look for consistent associations across studies
   - Review effect sizes and directions

4. **Functional interpretation:**
   - Determine variant consequences (missense, regulatory, etc.)
   - Check expression QTL (eQTL) data
   - Review pathway and network context

### Workflow 4: Systematic Review of Genetic Evidence

1. **Define research question:**
   - Specific trait or disease of interest
   - Population considerations
   - Study design requirements

2. **Comprehensive variant extraction:**
   - Query all associations for trait
   - Set significance threshold
   - Note discovery and replication studies

3. **Quality assessment:**
   - Review study sample sizes
   - Check for population diversity
   - Assess heterogeneity across studies
   - Identify potential biases

4. **Data synthesis:**
   - Aggregate associations across studies
   - Perform meta-analysis if applicable
   - Create summary tables
   - Generate Manhattan or forest plots

5. **Export and documentation:**
   - Download full association data
   - Export summary statistics if needed
   - Document search strategy and date
   - Create reproducible analysis scripts

### Workflow 5: Accessing and Analyzing Summary Statistics

1. **Identify studies with summary statistics:**
   - Browse summary statistics portal
   - Check FTP directory listings
   - Query API for available studies

2. **Download summary statistics:**
   ```bash
   # Via FTP
   wget ftp://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCSTXXXXXX/harmonised/GCSTXXXXXX-harmonised.tsv.gz
   ```

3. **Query via API for specific variants:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chrom}/associations"
   params = {"start": start_pos, "end": end_pos}
   ```

4. **Process and analyze:**
   - Filter by p-value thresholds
   - Extract effect sizes and confidence intervals
   - Perform downstream analyses (fine-mapping, colocalization, etc.)

## Response Formats and Data Fields

**Key Fields in Association Records:**
- `rsId`: Variant identifier (rs number)
- `strongestAllele`: Risk allele for the association
- `pvalue`: Association p-value
- `pvalueText`: P-value as text (may include inequality)
- `orPerCopyNum`: Odds ratio or beta coefficient
- `betaNum`: Effect size (for quantitative traits)
- `betaUnit`: Unit of measurement for beta
- `range`: Confidence interval
- `efoTrait`: Associated trait name
- `mappedLabel`: EFO-mapped trait term

**Study Metadata Fields:**
- `accessionId`: GCST study identifier
- `pubmedId`: PubMed ID
- `author`: First author
- `publicationDate`: Publication date
- `ancestryInitial`: Discovery population ancestry
- `ancestryReplication`: Replication population ancestry
- `sampleSize`: Total sample size

**Pagination:**
Results are paginated (default 20 items per page). Navigate using:
- `size` parameter: Number of results per page
- `page` parameter: Page number (0-indexed)
- `_links` in response: URLs for next/previous pages

## Best Practices

### Query Strategy
- Start with web interface to identify relevant EFO terms and study accessions
- Use API for bulk data extraction and automated analyses
- Implement pagination handling for large result sets
- Cache API responses to minimize redundant requests

### Data Interpretation
- Always check p-value thresholds (genome-wide: 5×10⁻⁸)
- Review ancestry information for population applicability
- Consider sample size when assessing evidence strength
- Check for replication across independent studies
- Be aware of winner's curse in effect size estimates

### Rate Limiting and Ethics
- Respect API usage guidelines (no excessive requests)
- Use summary statistics downloads for genome-wide analyses
- Implement appropriate delays between API calls
- Cache results locally when performing iterative analyses
- Cite the GWAS Catalog in publications

### Data Quality Considerations
- GWAS Catalog curates published associations (may contain inconsistencies)
- Effect sizes reported as published (may need harmonization)
- Some studies report conditional or joint associations
- Check for study overlap when combining results
- Be aware of ascertainment and selection biases

## Python Integration Example

Complete workflow for querying and analyzing GWAS data:

```python
import requests
import pandas as pd
from time import sleep

def query_gwas_catalog(trait_id, p_threshold=5e-8):
    """
    Query GWAS Catalog for trait associations

    Args:
        trait_id: EFO trait identifier (e.g., 'EFO_0001360')
        p_threshold: P-value threshold for filtering

    Returns:
        pandas DataFrame with association results
    """
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"

    headers = {"Content-Type": "application/json"}
    results = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        for assoc in associations:
            pvalue = assoc.get('pvalue')
            if pvalue and float(pvalue) <= p_threshold:
                results.append({
                    'variant': assoc.get('rsId'),
                    'pvalue': pvalue,
                    'risk_allele': assoc.get('strongestAllele'),
                    'or_beta': assoc.get('orPerCopyNum') or assoc.get('betaNum'),
                    'trait': assoc.get('efoTrait'),
                    'pubmed_id': assoc.get('pubmedId')
                })

        page += 1
        sleep(0.1)  # Rate limiting

    return pd.DataFrame(results)

# Example usage
df = query_gwas_catalog('EFO_0001360')  # Type 2 diabetes
print(df.head())
print(f"\nTotal associations: {len(df)}")
print(f"Unique variants: {df['variant'].nunique()}")
```

## Resources

### references/api_reference.md

Comprehensive API documentation including:
- Detailed endpoint specifications for both APIs
- Complete list of query parameters and filters
- Response format specifications and field descriptions
- Advanced query examples and patterns
- Error handling and troubleshooting
- Integration with external databases

Consult this reference when:
- Constructing complex API queries
- Understanding response structures
- Implementing pagination or batch operations
- Troubleshooting API errors
- Exploring advanced filtering options

### Training Materials

The GWAS Catalog team provides workshop materials:
- GitHub repository: https://github.com/EBISPOT/GWAS_Catalog-workshop
- Jupyter notebooks with example queries
- Google Colab integration for cloud execution

## Important Notes

### Data Updates
- The GWAS Catalog is updated regularly with new publications
- Re-run queries periodically for comprehensive coverage
- Summary statistics are added as studies release data
- EFO mappings may be updated over time

### Citation Requirements
When using GWAS Catalog data, cite:
- Sollis E, et al. (2023) The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. Nucleic Acids Research. PMID: 37953337
- Include access date and version when available
- Cite original studies when discussing specific findings

### Limitations
- Not all GWAS publications are included (curation criteria apply)
- Full summary statistics available for subset of studies
- Effect sizes may require harmonization across studies
- Population diversity is growing but historically limited
- Some associations represent conditional or joint effects

### Data Access
- Web interface: Free, no registration required
- REST APIs: Free, no API key needed
- FTP downloads: Open access
- Rate limiting applies to API (be respectful)

## Additional Resources

- **GWAS Catalog website**: https://www.ebi.ac.uk/gwas/
- **Documentation**: https://www.ebi.ac.uk/gwas/docs
- **API documentation**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **Summary Statistics API**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **FTP site**: http://ftp.ebi.ac.uk/pub/databases/gwas/
- **Training materials**: https://github.com/EBISPOT/GWAS_Catalog-workshop
- **PGS Catalog** (polygenic scores): https://www.pgscatalog.org/
- **Help and support**: gwas-info@ebi.ac.uk

---

## Reference: Api_Reference

# GWAS Catalog API Reference

Comprehensive reference for the GWAS Catalog REST APIs, including endpoint specifications, query parameters, response formats, and advanced usage patterns.

## Table of Contents

- [API Overview](#api-overview)
- [Authentication and Rate Limiting](#authentication-and-rate-limiting)
- [GWAS Catalog REST API](#gwas-catalog-rest-api)
- [Summary Statistics API](#summary-statistics-api)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)
- [Advanced Query Patterns](#advanced-query-patterns)
- [Integration Examples](#integration-examples)

## API Overview

The GWAS Catalog provides two complementary REST APIs:

1. **GWAS Catalog REST API**: Access to curated SNP-trait associations, studies, and metadata
2. **Summary Statistics API**: Access to full GWAS summary statistics (all tested variants)

Both APIs use RESTful design principles with JSON responses in HAL (Hypertext Application Language) format, which includes `_links` for resource navigation.

### Base URLs

```
GWAS Catalog API:         https://www.ebi.ac.uk/gwas/rest/api
Summary Statistics API:   https://www.ebi.ac.uk/gwas/summary-statistics/api
```

### Version Information

The GWAS Catalog REST API v2.0 was released in 2024, with significant improvements:
- New endpoints (publications, genes, genomic context, ancestries)
- Enhanced data exposure (cohorts, background traits, licenses)
- Improved query capabilities
- Better performance and documentation

The previous API version remains available until May 2026 for backward compatibility.

## Authentication and Rate Limiting

### Authentication

**No authentication required** - Both APIs are open access and do not require API keys or registration.

### Rate Limiting

While no explicit rate limits are documented, follow best practices:
- Implement delays between consecutive requests (e.g., 0.1-0.5 seconds)
- Use pagination for large result sets
- Cache responses locally
- Use bulk downloads (FTP) for genome-wide data
- Avoid hammering the API with rapid consecutive requests

**Example with rate limiting:**
```python
import requests
from time import sleep

def query_with_rate_limit(url, delay=0.1):
    response = requests.get(url)
    sleep(delay)
    return response.json()
```

## GWAS Catalog REST API

The main API provides access to curated GWAS associations, studies, variants, and traits.

### Core Endpoints

#### 1. Studies

**Get all studies:**
```
GET /studies
```

**Get specific study:**
```
GET /studies/{accessionId}
```

**Search studies:**
```
GET /studies/search/findByPublicationIdPubmedId?pubmedId={pmid}
GET /studies/search/findByDiseaseTrait?diseaseTrait={trait}
```

**Query Parameters:**
- `page`: Page number (0-indexed)
- `size`: Results per page (default: 20)
- `sort`: Sort field (e.g., `publicationDate,desc`)

**Example:**
```python
import requests

# Get a specific study
url = "https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795"
response = requests.get(url, headers={"Content-Type": "application/json"})
study = response.json()

print(f"Title: {study.get('title')}")
print(f"PMID: {study.get('publicationInfo', {}).get('pubmedId')}")
print(f"Sample size: {study.get('initialSampleSize')}")
```

**Response Fields:**
- `accessionId`: Study identifier (GCST ID)
- `title`: Study title
- `publicationInfo`: Publication details including PMID
- `initialSampleSize`: Discovery cohort description
- `replicationSampleSize`: Replication cohort description
- `ancestries`: Population ancestry information
- `genotypingTechnologies`: Array or sequencing platforms
- `_links`: Links to related resources

#### 2. Associations

**Get all associations:**
```
GET /associations
```

**Get specific association:**
```
GET /associations/{associationId}
```

**Get associations for a trait:**
```
GET /efoTraits/{efoId}/associations
```

**Get associations for a variant:**
```
GET /singleNucleotidePolymorphisms/{rsId}/associations
```

**Query Parameters:**
- `projection`: Response projection (e.g., `associationBySnp`)
- `page`, `size`, `sort`: Pagination controls

**Example:**
```python
import requests

# Find all associations for type 2 diabetes
trait_id = "EFO_0001360"
url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{trait_id}/associations"
params = {"size": 100, "page": 0}
response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
data = response.json()

associations = data.get('_embedded', {}).get('associations', [])
print(f"Found {len(associations)} associations")
```

**Response Fields:**
- `rsId`: Variant identifier
- `strongestAllele`: Risk or effect allele
- `pvalue`: Association p-value
- `pvalueText`: P-value as reported (may include inequality)
- `pvalueMantissa`: Mantissa of p-value
- `pvalueExponent`: Exponent of p-value
- `orPerCopyNum`: Odds ratio per allele copy
- `betaNum`: Effect size (quantitative traits)
- `betaUnit`: Unit of measurement
- `range`: Confidence interval
- `standardError`: Standard error
- `efoTrait`: Trait name
- `mappedLabel`: EFO standardized term
- `studyId`: Associated study accession

#### 3. Variants (Single Nucleotide Polymorphisms)

**Get variant details:**
```
GET /singleNucleotidePolymorphisms/{rsId}
```

**Search variants:**
```
GET /singleNucleotidePolymorphisms/search/findByRsId?rsId={rsId}
GET /singleNucleotidePolymorphisms/search/findByChromBpLocationRange?chrom={chr}&bpStart={start}&bpEnd={end}
GET /singleNucleotidePolymorphisms/search/findByGene?geneName={gene}
```

**Example:**
```python
import requests

# Get variant information
rs_id = "rs7903146"
url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
response = requests.get(url, headers={"Content-Type": "application/json"})
variant = response.json()

print(f"rsID: {variant.get('rsId')}")
print(f"Location: chr{variant.get('locations', [{}])[0].get('chromosomeName')}:{variant.get('locations', [{}])[0].get('chromosomePosition')}")
```

**Response Fields:**
- `rsId`: rs number
- `merged`: Indicates if variant merged with another
- `functionalClass`: Variant consequence
- `locations`: Array of genomic locations
  - `chromosomeName`: Chromosome number
  - `chromosomePosition`: Base pair position
  - `region`: Genomic region information
- `genomicContexts`: Nearby genes
- `lastUpdateDate`: Last modification date

#### 4. Traits (EFO Terms)

**Get trait information:**
```
GET /efoTraits/{efoId}
```

**Search traits:**
```
GET /efoTraits/search/findByEfoUri?uri={efoUri}
GET /efoTraits/search/findByTraitIgnoreCase?trait={traitName}
```

**Example:**
```python
import requests

# Get trait details
trait_id = "EFO_0001360"
url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{trait_id}"
response = requests.get(url, headers={"Content-Type": "application/json"})
trait = response.json()

print(f"Trait: {trait.get('trait')}")
print(f"EFO URI: {trait.get('uri')}")
```

#### 5. Publications

**Get publication information:**
```
GET /publications
GET /publications/{publicationId}
GET /publications/search/findByPubmedId?pubmedId={pmid}
```

#### 6. Genes

**Get gene information:**
```
GET /genes
GET /genes/{geneId}
GET /genes/search/findByGeneName?geneName={symbol}
```

### Pagination and Navigation

All list endpoints support pagination:

```python
import requests

def get_all_associations(trait_id):
    """Retrieve all associations for a trait with pagination"""
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"
    all_associations = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        all_associations.extend(associations)
        page += 1

    return all_associations
```

### HAL Links

Responses include `_links` for resource navigation:

```python
import requests

# Get study and follow links to associations
response = requests.get("https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001795")
study = response.json()

# Follow link to associations
associations_url = study['_links']['associations']['href']
associations_response = requests.get(associations_url)
associations = associations_response.json()
```

## Summary Statistics API

Access full GWAS summary statistics for studies that have deposited complete data.

### Base URL
```
https://www.ebi.ac.uk/gwas/summary-statistics/api
```

### Core Endpoints

#### 1. Studies

**Get all studies with summary statistics:**
```
GET /studies
```

**Get specific study:**
```
GET /studies/{gcstId}
```

#### 2. Traits

**Get trait information:**
```
GET /traits/{efoId}
```

**Get associations for a trait:**
```
GET /traits/{efoId}/associations
```

**Query Parameters:**
- `p_lower`: Lower p-value threshold
- `p_upper`: Upper p-value threshold
- `size`: Number of results
- `page`: Page number

**Example:**
```python
import requests

# Find highly significant associations for a trait
trait_id = "EFO_0001360"
base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/traits/{trait_id}/associations"
params = {
    "p_upper": "0.000000001",  # p < 1e-9
    "size": 100
}
response = requests.get(url, params=params)
results = response.json()
```

#### 3. Chromosomes

**Get associations by chromosome:**
```
GET /chromosomes/{chromosome}/associations
```

**Query by genomic region:**
```
GET /chromosomes/{chromosome}/associations?start={start}&end={end}
```

**Example:**
```python
import requests

# Query variants in a specific region
chromosome = "10"
start_pos = 114000000
end_pos = 115000000

base_url = "https://www.ebi.ac.uk/gwas/summary-statistics/api"
url = f"{base_url}/chromosomes/{chromosome}/associations"
params = {
    "start": start_pos,
    "end": end_pos,
    "size": 1000
}
response = requests.get(url, params=params)
variants = response.json()
```

#### 4. Variants

**Get specific variant across studies:**
```
GET /variants/{variantId}
```

**Search by variant ID:**
```
GET /variants/{variantId}/associations
```

### Response Fields

**Association Fields:**
- `variant_id`: Variant identifier
- `chromosome`: Chromosome number
- `base_pair_location`: Position (bp)
- `effect_allele`: Effect allele
- `other_allele`: Reference allele
- `effect_allele_frequency`: Allele frequency
- `beta`: Effect size
- `standard_error`: Standard error
- `p_value`: P-value
- `ci_lower`: Lower confidence interval
- `ci_upper`: Upper confidence interval
- `odds_ratio`: Odds ratio (case-control studies)
- `study_accession`: GCST ID

## Response Formats

### Content Type

All API requests should include the header:
```
Content-Type: application/json
```

### HAL Format

Responses follow the HAL (Hypertext Application Language) specification:

```json
{
  "_embedded": {
    "associations": [
      {
        "rsId": "rs7903146",
        "pvalue": 1.2e-30,
        "efoTrait": "type 2 diabetes",
        "_links": {
          "self": {
            "href": "https://www.ebi.ac.uk/gwas/rest/api/associations/12345"
          }
        }
      }
    ]
  },
  "_links": {
    "self": {
      "href": "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/EFO_0001360/associations?page=0"
    },
    "next": {
      "href": "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/EFO_0001360/associations?page=1"
    }
  },
  "page": {
    "size": 20,
    "totalElements": 1523,
    "totalPages": 77,
    "number": 0
  }
}
```

### Page Metadata

Paginated responses include page information:
- `size`: Items per page
- `totalElements`: Total number of results
- `totalPages`: Total number of pages
- `number`: Current page number (0-indexed)

## Error Handling

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "timestamp": "2025-10-19T12:00:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "No association found with id: 12345",
  "path": "/gwas/rest/api/associations/12345"
}
```

### Error Handling Example

```python
import requests

def safe_api_request(url, params=None):
    """Make API request with error handling"""
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error - check network")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
```

## Advanced Query Patterns

### 1. Cross-referencing Variants and Traits

```python
import requests

def get_variant_pleiotropy(rs_id):
    """Get all traits associated with a variant"""
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/singleNucleotidePolymorphisms/{rs_id}/associations"
    params = {"projection": "associationBySnp"}

    response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
    data = response.json()

    traits = {}
    for assoc in data.get('_embedded', {}).get('associations', []):
        trait = assoc.get('efoTrait')
        pvalue = assoc.get('pvalue')
        if trait:
            if trait not in traits or float(pvalue) < float(traits[trait]):
                traits[trait] = pvalue

    return traits

# Example usage
pleiotropy = get_variant_pleiotropy('rs7903146')
for trait, pval in sorted(pleiotropy.items(), key=lambda x: float(x[1])):
    print(f"{trait}: p={pval}")
```

### 2. Filtering by P-value Threshold

```python
import requests

def get_significant_associations(trait_id, p_threshold=5e-8):
    """Get genome-wide significant associations"""
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/efoTraits/{trait_id}/associations"

    results = []
    page = 0

    while True:
        params = {"page": page, "size": 100}
        response = requests.get(url, params=params, headers={"Content-Type": "application/json"})

        if response.status_code != 200:
            break

        data = response.json()
        associations = data.get('_embedded', {}).get('associations', [])

        if not associations:
            break

        for assoc in associations:
            pvalue = assoc.get('pvalue')
            if pvalue and float(pvalue) <= p_threshold:
                results.append(assoc)

        page += 1

    return results
```

### 3. Combining Main and Summary Statistics APIs

```python
import requests

def get_complete_variant_data(rs_id):
    """Get variant data from both APIs"""
    main_url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"

    # Get basic variant info
    response = requests.get(main_url, headers={"Content-Type": "application/json"})
    variant_info = response.json()

    # Get associations
    assoc_url = f"{main_url}/associations"
    response = requests.get(assoc_url, headers={"Content-Type": "application/json"})
    associations = response.json()

    # Could also query summary statistics API for this variant
    # across all studies with summary data

    return {
        "variant": variant_info,
        "associations": associations
    }
```

### 4. Genomic Region Queries

```python
import requests

def query_region(chromosome, start, end, p_threshold=None):
    """Query variants in genomic region"""
    # From main API
    base_url = "https://www.ebi.ac.uk/gwas/rest/api"
    url = f"{base_url}/singleNucleotidePolymorphisms/search/findByChromBpLocationRange"
    params = {
        "chrom": chromosome,
        "bpStart": start,
        "bpEnd": end,
        "size": 1000
    }

    response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
    variants = response.json()

    # Can also query summary statistics API
    sumstats_url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chromosome}/associations"
    sumstats_params = {"start": start, "end": end, "size": 1000}
    if p_threshold:
        sumstats_params["p_upper"] = str(p_threshold)

    sumstats_response = requests.get(sumstats_url, params=sumstats_params)
    sumstats = sumstats_response.json()

    return {
        "catalog_variants": variants,
        "summary_stats": sumstats
    }
```

## Integration Examples

### Complete Workflow: Disease Genetic Architecture

```python
import requests
import pandas as pd
from time import sleep

class GWASCatalogQuery:
    def __init__(self):
        self.base_url = "https://www.ebi.ac.uk/gwas/rest/api"
        self.headers = {"Content-Type": "application/json"}

    def get_trait_associations(self, trait_id, p_threshold=5e-8):
        """Get all associations for a trait"""
        url = f"{self.base_url}/efoTraits/{trait_id}/associations"
        results = []
        page = 0

        while True:
            params = {"page": page, "size": 100}
            response = requests.get(url, params=params, headers=self.headers)

            if response.status_code != 200:
                break

            data = response.json()
            associations = data.get('_embedded', {}).get('associations', [])

            if not associations:
                break

            for assoc in associations:
                pvalue = assoc.get('pvalue')
                if pvalue and float(pvalue) <= p_threshold:
                    results.append({
                        'rs_id': assoc.get('rsId'),
                        'pvalue': float(pvalue),
                        'risk_allele': assoc.get('strongestAllele'),
                        'or_beta': assoc.get('orPerCopyNum') or assoc.get('betaNum'),
                        'study': assoc.get('studyId'),
                        'pubmed_id': assoc.get('pubmedId')
                    })

            page += 1
            sleep(0.1)

        return pd.DataFrame(results)

    def get_variant_details(self, rs_id):
        """Get detailed variant information"""
        url = f"{self.base_url}/singleNucleotidePolymorphisms/{rs_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

    def get_gene_associations(self, gene_name):
        """Get variants associated with a gene"""
        url = f"{self.base_url}/singleNucleotidePolymorphisms/search/findByGene"
        params = {"geneName": gene_name}
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        return None

# Example usage
gwas = GWASCatalogQuery()

# Query type 2 diabetes associations
df = gwas.get_trait_associations('EFO_0001360')
print(f"Found {len(df)} genome-wide significant associations")
print(f"Unique variants: {df['rs_id'].nunique()}")

# Get top variants
top_variants = df.nsmallest(10, 'pvalue')
print("\nTop 10 variants:")
print(top_variants[['rs_id', 'pvalue', 'risk_allele']])

# Get details for top variant
if len(top_variants) > 0:
    top_rs = top_variants.iloc[0]['rs_id']
    variant_info = gwas.get_variant_details(top_rs)
    if variant_info:
        loc = variant_info.get('locations', [{}])[0]
        print(f"\n{top_rs} location: chr{loc.get('chromosomeName')}:{loc.get('chromosomePosition')}")
```

### FTP Download Integration

```python
import requests
from pathlib import Path

def download_summary_statistics(gcst_id, output_dir="."):
    """Download summary statistics from FTP"""
    # FTP URL pattern
    ftp_base = "http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics"

    # Try harmonised file first
    harmonised_url = f"{ftp_base}/{gcst_id}/harmonised/{gcst_id}-harmonised.tsv.gz"

    output_path = Path(output_dir) / f"{gcst_id}.tsv.gz"

    try:
        response = requests.get(harmonised_url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded {gcst_id} to {output_path}")
        return output_path

    except requests.exceptions.HTTPError:
        print(f"Harmonised file not found for {gcst_id}")
        return None

# Example usage
download_summary_statistics("GCST001234", output_dir="./sumstats")
```

## Additional Resources

- **Interactive API Documentation**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **Summary Statistics API Docs**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **Workshop Materials**: https://github.com/EBISPOT/GWAS_Catalog-workshop
- **Blog Post on API v2**: https://ebispot.github.io/gwas-blog/rest-api-v2-release/
- **R Package (gwasrapidd)**: https://cran.r-project.org/package=gwasrapidd
