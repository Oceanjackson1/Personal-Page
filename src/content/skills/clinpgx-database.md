---
title: "Clinpgx Database"
description: "Access ClinPGx pharmacogenomics data (successor to PharmGKB). Query gene-drug interactions, CPIC guidelines, allele functions, for precision medicine and genotype-guided dosing decisions."
category: "research"
source: "community"
author: "Community"
tags: ["clinpgx", "database"]
date: 2026-03-20
---

# ClinPGx Database

## Overview

ClinPGx (Clinical Pharmacogenomics Database) is a comprehensive resource for clinical pharmacogenomics information, successor to PharmGKB. It consolidates data from PharmGKB, CPIC, and PharmCAT, providing curated information on how genetic variation affects medication response. Access gene-drug pairs, clinical guidelines, allele functions, and drug labels for precision medicine applications.

## When to Use This Skill

This skill should be used when:

- **Gene-drug interactions**: Querying how genetic variants affect drug metabolism, efficacy, or toxicity
- **CPIC guidelines**: Accessing evidence-based clinical practice guidelines for pharmacogenetics
- **Allele information**: Retrieving allele function, frequency, and phenotype data
- **Drug labels**: Exploring FDA and other regulatory pharmacogenomic drug labeling
- **Pharmacogenomic annotations**: Accessing curated literature on gene-drug-disease relationships
- **Clinical decision support**: Using PharmDOG tool for phenoconversion and custom genotype interpretation
- **Precision medicine**: Implementing pharmacogenomic testing in clinical practice
- **Drug metabolism**: Understanding CYP450 and other pharmacogene functions
- **Personalized dosing**: Finding genotype-guided dosing recommendations
- **Adverse drug reactions**: Identifying genetic risk factors for drug toxicity

## Installation and Setup

### Python API Access

The ClinPGx REST API provides programmatic access to all database resources. Basic setup:

```bash
uv pip install requests
```

### API Endpoint

```python
BASE_URL = "https://api.clinpgx.org/v1/"
```

**Rate Limits**:
- 2 requests per second maximum
- Excessive requests will result in HTTP 429 (Too Many Requests) response

**Authentication**: Not required for basic access

**Data License**: Creative Commons Attribution-ShareAlike 4.0 International License

For substantial API use, notify the ClinPGx team at api@clinpgx.org

## Core Capabilities

### 1. Gene Queries

**Retrieve gene information** including function, clinical annotations, and pharmacogenomic significance:

```python
import requests

# Get gene details
response = requests.get("https://api.clinpgx.org/v1/gene/CYP2D6")
gene_data = response.json()

# Search for genes by name
response = requests.get("https://api.clinpgx.org/v1/gene",
                       params={"q": "CYP"})
genes = response.json()
```

**Key pharmacogenes**:
- **CYP450 enzymes**: CYP2D6, CYP2C19, CYP2C9, CYP3A4, CYP3A5
- **Transporters**: SLCO1B1, ABCB1, ABCG2
- **Other metabolizers**: TPMT, DPYD, NUDT15, UGT1A1
- **Receptors**: OPRM1, HTR2A, ADRB1
- **HLA genes**: HLA-B, HLA-A

### 2. Drug and Chemical Queries

**Retrieve drug information** including pharmacogenomic annotations and mechanisms:

```python
# Get drug details
response = requests.get("https://api.clinpgx.org/v1/chemical/PA448515")  # Warfarin
drug_data = response.json()

# Search drugs by name
response = requests.get("https://api.clinpgx.org/v1/chemical",
                       params={"name": "warfarin"})
drugs = response.json()
```

**Drug categories with pharmacogenomic significance**:
- Anticoagulants (warfarin, clopidogrel)
- Antidepressants (SSRIs, TCAs)
- Immunosuppressants (tacrolimus, azathioprine)
- Oncology drugs (5-fluorouracil, irinotecan, tamoxifen)
- Cardiovascular drugs (statins, beta-blockers)
- Pain medications (codeine, tramadol)
- Antivirals (abacavir)

### 3. Gene-Drug Pair Queries

**Access curated gene-drug relationships** with clinical annotations:

```python
# Get gene-drug pair information
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2D6", "drug": "codeine"})
pair_data = response.json()

# Get all pairs for a gene
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "CYP2C19"})
all_pairs = response.json()
```

**Clinical annotation sources**:
- CPIC (Clinical Pharmacogenetics Implementation Consortium)
- DPWG (Dutch Pharmacogenetics Working Group)
- FDA (Food and Drug Administration) labels
- Peer-reviewed literature summary annotations

### 4. CPIC Guidelines

**Access evidence-based clinical practice guidelines**:

```python
# Get CPIC guideline
response = requests.get("https://api.clinpgx.org/v1/guideline/PA166104939")
guideline = response.json()

# List all CPIC guidelines
response = requests.get("https://api.clinpgx.org/v1/guideline",
                       params={"source": "CPIC"})
guidelines = response.json()
```

**CPIC guideline components**:
- Gene-drug pairs covered
- Clinical recommendations by phenotype
- Evidence levels and strength ratings
- Supporting literature
- Downloadable PDFs and supplementary materials
- Implementation considerations

**Example guidelines**:
- CYP2D6-codeine (avoid in ultra-rapid metabolizers)
- CYP2C19-clopidogrel (alternative therapy for poor metabolizers)
- TPMT-azathioprine (dose reduction for intermediate/poor metabolizers)
- DPYD-fluoropyrimidines (dose adjustment based on activity)
- HLA-B*57:01-abacavir (avoid if positive)

### 5. Allele and Variant Information

**Query allele function and frequency data**:

```python
# Get allele information
response = requests.get("https://api.clinpgx.org/v1/allele/CYP2D6*4")
allele_data = response.json()

# Get all alleles for a gene
response = requests.get("https://api.clinpgx.org/v1/allele",
                       params={"gene": "CYP2D6"})
alleles = response.json()
```

**Allele information includes**:
- Functional status (normal, decreased, no function, increased, uncertain)
- Population frequencies across ethnic groups
- Defining variants (SNPs, indels, CNVs)
- Phenotype assignment
- References to PharmVar and other nomenclature systems

**Phenotype categories**:
- **Ultra-rapid metabolizer** (UM): Increased enzyme activity
- **Normal metabolizer** (NM): Normal enzyme activity
- **Intermediate metabolizer** (IM): Reduced enzyme activity
- **Poor metabolizer** (PM): Little to no enzyme activity

### 6. Variant Annotations

**Access clinical annotations for specific genetic variants**:

```python
# Get variant information
response = requests.get("https://api.clinpgx.org/v1/variant/rs4244285")
variant_data = response.json()

# Search variants by position (if supported)
response = requests.get("https://api.clinpgx.org/v1/variant",
                       params={"chromosome": "10", "position": "94781859"})
variants = response.json()
```

**Variant data includes**:
- rsID and genomic coordinates
- Gene and functional consequence
- Allele associations
- Clinical significance
- Population frequencies
- Literature references

### 7. Clinical Annotations

**Retrieve curated literature annotations** (formerly PharmGKB clinical annotations):

```python
# Get clinical annotations
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"gene": "CYP2D6"})
annotations = response.json()

# Filter by evidence level
response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                       params={"evidenceLevel": "1A"})
high_evidence = response.json()
```

**Evidence levels** (from highest to lowest):
- **Level 1A**: High-quality evidence, CPIC/FDA/DPWG guidelines
- **Level 1B**: High-quality evidence, not yet guideline
- **Level 2A**: Moderate evidence from well-designed studies
- **Level 2B**: Moderate evidence with some limitations
- **Level 3**: Limited or conflicting evidence
- **Level 4**: Case reports or weak evidence

### 8. Drug Labels

**Access pharmacogenomic information from drug labels**:

```python
# Get drug labels with PGx information
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"drug": "warfarin"})
labels = response.json()

# Filter by regulatory source
response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                       params={"source": "FDA"})
fda_labels = response.json()
```

**Label information includes**:
- Testing recommendations
- Dosing guidance by genotype
- Warnings and precautions
- Biomarker information
- Regulatory source (FDA, EMA, PMDA, etc.)

### 9. Pathways

**Explore pharmacokinetic and pharmacodynamic pathways**:

```python
# Get pathway information
response = requests.get("https://api.clinpgx.org/v1/pathway/PA146123006")  # Warfarin pathway
pathway_data = response.json()

# Search pathways by drug
response = requests.get("https://api.clinpgx.org/v1/pathway",
                       params={"drug": "warfarin"})
pathways = response.json()
```

**Pathway diagrams** show:
- Drug metabolism steps
- Enzymes and transporters involved
- Gene variants affecting each step
- Downstream effects on efficacy/toxicity
- Interactions with other pathways

## Query Workflow

### Workflow 1: Clinical Decision Support for Drug Prescription

1. **Identify patient genotype** for relevant pharmacogenes:
   ```python
   # Example: Patient is CYP2C19 *1/*2 (intermediate metabolizer)
   response = requests.get("https://api.clinpgx.org/v1/allele/CYP2C19*2")
   allele_function = response.json()
   ```

2. **Query gene-drug pairs** for medication of interest:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   pair_info = response.json()
   ```

3. **Retrieve CPIC guideline** for dosing recommendations:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/guideline",
                          params={"gene": "CYP2C19", "drug": "clopidogrel"})
   guideline = response.json()
   # Recommendation: Alternative antiplatelet therapy for IM/PM
   ```

4. **Check drug label** for regulatory guidance:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/drugLabel",
                          params={"drug": "clopidogrel"})
   label = response.json()
   ```

### Workflow 2: Gene Panel Analysis

1. **Get list of pharmacogenes** in clinical panel:
   ```python
   pgx_panel = ["CYP2C19", "CYP2D6", "CYP2C9", "TPMT", "DPYD", "SLCO1B1"]
   ```

2. **For each gene, retrieve all drug interactions**:
   ```python
   all_interactions = {}
   for gene in pgx_panel:
       response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                              params={"gene": gene})
       all_interactions[gene] = response.json()
   ```

3. **Filter for CPIC guideline-level evidence**:
   ```python
   for gene, pairs in all_interactions.items():
       for pair in pairs:
           if pair.get('cpicLevel'):  # Has CPIC guideline
               print(f"{gene} - {pair['drug']}: {pair['cpicLevel']}")
   ```

4. **Generate patient report** with actionable pharmacogenomic findings.

### Workflow 3: Drug Safety Assessment

1. **Query drug for PGx associations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/chemical",
                          params={"name": "abacavir"})
   drug_id = response.json()[0]['id']
   ```

2. **Get clinical annotations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"drug": drug_id})
   annotations = response.json()
   ```

3. **Check for HLA associations** and toxicity risk:
   ```python
   for annotation in annotations:
       if 'HLA' in annotation.get('genes', []):
           print(f"Toxicity risk: {annotation['phenotype']}")
           print(f"Evidence level: {annotation['evidenceLevel']}")
   ```

4. **Retrieve screening recommendations** from guidelines and labels.

### Workflow 4: Research Analysis - Population Pharmacogenomics

1. **Get allele frequencies** for population comparison:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/allele",
                          params={"gene": "CYP2D6"})
   alleles = response.json()
   ```

2. **Extract population-specific frequencies**:
   ```python
   populations = ['European', 'African', 'East Asian', 'Latino']
   frequency_data = {}
   for allele in alleles:
       allele_name = allele['name']
       frequency_data[allele_name] = {
           pop: allele.get(f'{pop}_frequency', 'N/A')
           for pop in populations
       }
   ```

3. **Calculate phenotype distributions** by population:
   ```python
   # Combine allele frequencies with function to predict phenotypes
   phenotype_dist = calculate_phenotype_frequencies(frequency_data)
   ```

4. **Analyze implications** for drug dosing in diverse populations.

### Workflow 5: Literature Evidence Review

1. **Search for gene-drug pair**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   pair = response.json()
   ```

2. **Retrieve all clinical annotations**:
   ```python
   response = requests.get("https://api.clinpgx.org/v1/clinicalAnnotation",
                          params={"gene": "TPMT", "drug": "azathioprine"})
   annotations = response.json()
   ```

3. **Filter by evidence level and publication date**:
   ```python
   high_quality = [a for a in annotations
                   if a['evidenceLevel'] in ['1A', '1B', '2A']]
   ```

4. **Extract PMIDs** and retrieve full references:
   ```python
   pmids = [a['pmid'] for a in high_quality if 'pmid' in a]
   # Use PubMed skill to retrieve full citations
   ```

## Rate Limiting and Best Practices

### Rate Limit Compliance

```python
import time

def rate_limited_request(url, params=None, delay=0.5):
    """Make API request with rate limiting (2 req/sec max)"""
    response = requests.get(url, params=params)
    time.sleep(delay)  # Wait 0.5 seconds between requests
    return response

# Use in loops
genes = ["CYP2D6", "CYP2C19", "CYP2C9"]
for gene in genes:
    response = rate_limited_request(
        "https://api.clinpgx.org/v1/gene/" + gene
    )
    data = response.json()
```

### Error Handling

```python
def safe_api_call(url, params=None, max_retries=3):
    """API call with error handling and retries"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limit exceeded
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

### Caching Results

```python
import json
from pathlib import Path

def cached_query(cache_file, api_func, *args, **kwargs):
    """Cache API results to avoid repeated queries"""
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = api_func(*args, **kwargs)

    with open(cache_path, 'w') as f:
        json.dump(result, f, indent=2)

    return result

# Usage
gene_data = cached_query(
    'cyp2d6_cache.json',
    rate_limited_request,
    "https://api.clinpgx.org/v1/gene/CYP2D6"
)
```

## PharmDOG Tool

PharmDOG (formerly DDRx) is ClinPGx's clinical decision support tool for interpreting pharmacogenomic test results:

**Key features**:
- **Phenoconversion calculator**: Adjusts phenotype predictions for drug-drug interactions affecting CYP2D6
- **Custom genotypes**: Input patient genotypes to get phenotype predictions
- **QR code sharing**: Generate shareable patient reports
- **Flexible guidance sources**: Select which guidelines to apply (CPIC, DPWG, FDA)
- **Multi-drug analysis**: Assess multiple medications simultaneously

**Access**: Available at https://www.clinpgx.org/pharmacogenomic-decision-support

**Use cases**:
- Clinical interpretation of PGx panel results
- Medication review for patients with known genotypes
- Patient education materials
- Point-of-care decision support

## Resources

### scripts/query_clinpgx.py

Python script with ready-to-use functions for common ClinPGx queries:

- `get_gene_info(gene_symbol)` - Retrieve gene details
- `get_drug_info(drug_name)` - Get drug information
- `get_gene_drug_pairs(gene, drug)` - Query gene-drug interactions
- `get_cpic_guidelines(gene, drug)` - Retrieve CPIC guidelines
- `get_alleles(gene)` - Get all alleles for a gene
- `get_clinical_annotations(gene, drug, evidence_level)` - Query literature annotations
- `get_drug_labels(drug)` - Retrieve pharmacogenomic drug labels
- `search_variants(rsid)` - Search by variant rsID
- `export_to_dataframe(data)` - Convert results to pandas DataFrame

Consult this script for implementation examples with proper rate limiting and error handling.

### references/api_reference.md

Comprehensive API documentation including:

- Complete endpoint listing with parameters
- Request/response format specifications
- Example queries for each endpoint
- Filter operators and search patterns
- Data schema definitions
- Rate limiting details
- Authentication requirements (if any)
- Troubleshooting common errors

Refer to this document when detailed API information is needed or when constructing complex queries.

## Important Notes

### Data Sources and Integration

ClinPGx consolidates multiple authoritative sources:
- **PharmGKB**: Curated pharmacogenomics knowledge base (now part of ClinPGx)
- **CPIC**: Evidence-based clinical implementation guidelines
- **PharmCAT**: Allele calling and phenotype interpretation tool
- **DPWG**: Dutch pharmacogenetics guidelines
- **FDA/EMA labels**: Regulatory pharmacogenomic information

As of July 2025, all PharmGKB URLs redirect to corresponding ClinPGx pages.

### Clinical Implementation Considerations

- **Evidence levels**: Always check evidence strength before clinical application
- **Population differences**: Allele frequencies vary significantly across populations
- **Phenoconversion**: Consider drug-drug interactions that affect enzyme activity
- **Multi-gene effects**: Some drugs affected by multiple pharmacogenes
- **Non-genetic factors**: Age, organ function, drug interactions also affect response
- **Testing limitations**: Not all clinically relevant alleles detected by all assays

### Data Updates

- ClinPGx continuously updates with new evidence and guidelines
- Check publication dates for clinical annotations
- Monitor ClinPGx Blog (https://blog.clinpgx.org/) for announcements
- CPIC guidelines updated as new evidence emerges
- PharmVar provides nomenclature updates for allele definitions

### API Stability

- API endpoints are relatively stable but may change during development
- Parameters and response formats subject to modification
- Monitor API changelog and ClinPGx blog for updates
- Consider version pinning for production applications
- Test API changes in development before production deployment

## Common Use Cases

### Pre-emptive Pharmacogenomic Testing

Query all clinically actionable gene-drug pairs to guide panel selection:

```python
# Get all CPIC guideline pairs
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"cpicLevel": "A"})  # Level A recommendations
actionable_pairs = response.json()
```

### Medication Therapy Management

Review patient medications against known genotypes:

```python
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}
medications = ["clopidogrel", "simvastatin", "escitalopram"]

for med in medications:
    for gene in patient_genes:
        response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                               params={"gene": gene, "drug": med})
        # Check for interactions and dosing guidance
```

### Clinical Trial Eligibility

Screen for pharmacogenomic contraindications:

```python
# Check for HLA-B*57:01 before abacavir trial
response = requests.get("https://api.clinpgx.org/v1/geneDrugPair",
                       params={"gene": "HLA-B", "drug": "abacavir"})
pair_info = response.json()
# CPIC: Do not use if HLA-B*57:01 positive
```

## Additional Resources

- **ClinPGx website**: https://www.clinpgx.org/
- **ClinPGx Blog**: https://blog.clinpgx.org/
- **API documentation**: https://api.clinpgx.org/
- **CPIC website**: https://cpicpgx.org/
- **PharmCAT**: https://pharmcat.clinpgx.org/
- **ClinGen**: https://clinicalgenome.org/
- **Contact**: api@clinpgx.org (for substantial API use)

---

## Reference: Api_Reference

# ClinPGx API Reference

Complete reference documentation for the ClinPGx REST API.

## Base URL

```
https://api.clinpgx.org/v1/
```

## Rate Limiting

- **Maximum rate**: 2 requests per second
- **Enforcement**: Requests exceeding the limit will receive HTTP 429 (Too Many Requests)
- **Best practice**: Implement 500ms delay between requests (0.5 seconds)
- **Recommendation**: For substantial API use, contact api@clinpgx.org

## Authentication

No authentication is required for basic API access. All endpoints are publicly accessible.

## Data License

All data accessed through the API is subject to:
- Creative Commons Attribution-ShareAlike 4.0 International License
- ClinPGx Data Usage Policy

## Response Format

All successful responses return JSON with appropriate HTTP status codes:
- `200 OK`: Successful request
- `404 Not Found`: Resource does not exist
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Core Endpoints

### 1. Gene Endpoint

Retrieve pharmacogene information including function, variants, and clinical significance.

#### Get Gene by Symbol

```http
GET /v1/gene/{gene_symbol}
```

**Parameters:**
- `gene_symbol` (path, required): Gene symbol (e.g., CYP2D6, TPMT, DPYD)

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/gene/CYP2D6"
```

**Example Response:**
```json
{
  "id": "PA126",
  "symbol": "CYP2D6",
  "name": "cytochrome P450 family 2 subfamily D member 6",
  "chromosome": "22",
  "chromosomeLocation": "22q13.2",
  "function": "Drug metabolism",
  "description": "Highly polymorphic gene encoding enzyme...",
  "clinicalAnnotations": [...],
  "relatedDrugs": [...]
}
```

#### Search Genes

```http
GET /v1/gene?q={search_term}
```

**Parameters:**
- `q` (query, optional): Search term for gene name or symbol

**Example:**
```bash
curl "https://api.clinpgx.org/v1/gene?q=CYP"
```

### 2. Chemical/Drug Endpoint

Access drug and chemical compound information including pharmacogenomic annotations.

#### Get Drug by ID

```http
GET /v1/chemical/{drug_id}
```

**Parameters:**
- `drug_id` (path, required): ClinPGx drug identifier (e.g., PA448515)

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/chemical/PA448515"
```

#### Search Drugs by Name

```http
GET /v1/chemical?name={drug_name}
```

**Parameters:**
- `name` (query, optional): Drug name or synonym

**Example:**
```bash
curl "https://api.clinpgx.org/v1/chemical?name=warfarin"
```

**Example Response:**
```json
[
  {
    "id": "PA448515",
    "name": "warfarin",
    "genericNames": ["warfarin sodium"],
    "tradeNames": ["Coumadin", "Jantoven"],
    "drugClasses": ["Anticoagulants"],
    "indication": "Prevention of thrombosis",
    "relatedGenes": ["CYP2C9", "VKORC1", "CYP4F2"]
  }
]
```

### 3. Gene-Drug Pair Endpoint

Query curated gene-drug interaction relationships with clinical annotations.

#### Get Gene-Drug Pairs

```http
GET /v1/geneDrugPair?gene={gene}&drug={drug}
```

**Parameters:**
- `gene` (query, optional): Gene symbol
- `drug` (query, optional): Drug name
- `cpicLevel` (query, optional): Filter by CPIC recommendation level (A, B, C, D)

**Example Requests:**
```bash
# Get all pairs for a gene
curl "https://api.clinpgx.org/v1/geneDrugPair?gene=CYP2D6"

# Get specific gene-drug pair
curl "https://api.clinpgx.org/v1/geneDrugPair?gene=CYP2D6&drug=codeine"

# Get all CPIC Level A pairs
curl "https://api.clinpgx.org/v1/geneDrugPair?cpicLevel=A"
```

**Example Response:**
```json
[
  {
    "gene": "CYP2D6",
    "drug": "codeine",
    "sources": ["CPIC", "FDA", "DPWG"],
    "cpicLevel": "A",
    "evidenceLevel": "1A",
    "clinicalAnnotationCount": 45,
    "hasGuideline": true,
    "guidelineUrl": "https://www.clinpgx.org/guideline/..."
  }
]
```

### 4. Guideline Endpoint

Access clinical practice guidelines from CPIC, DPWG, and other sources.

#### Get Guidelines

```http
GET /v1/guideline?source={source}&gene={gene}&drug={drug}
```

**Parameters:**
- `source` (query, optional): Guideline source (CPIC, DPWG, FDA)
- `gene` (query, optional): Gene symbol
- `drug` (query, optional): Drug name

**Example Requests:**
```bash
# Get all CPIC guidelines
curl "https://api.clinpgx.org/v1/guideline?source=CPIC"

# Get guideline for specific gene-drug
curl "https://api.clinpgx.org/v1/guideline?gene=CYP2C19&drug=clopidogrel"
```

#### Get Guideline by ID

```http
GET /v1/guideline/{guideline_id}
```

**Example:**
```bash
curl "https://api.clinpgx.org/v1/guideline/PA166104939"
```

**Example Response:**
```json
{
  "id": "PA166104939",
  "name": "CPIC Guideline for CYP2C19 and Clopidogrel",
  "source": "CPIC",
  "genes": ["CYP2C19"],
  "drugs": ["clopidogrel"],
  "recommendationLevel": "A",
  "lastUpdated": "2023-08-01",
  "summary": "Alternative antiplatelet therapy recommended for...",
  "recommendations": [...],
  "pdfUrl": "https://www.clinpgx.org/...",
  "pmid": "23400754"
}
```

### 5. Allele Endpoint

Query allele definitions, functions, and population frequencies.

#### Get All Alleles for a Gene

```http
GET /v1/allele?gene={gene_symbol}
```

**Parameters:**
- `gene` (query, required): Gene symbol

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/allele?gene=CYP2D6"
```

**Example Response:**
```json
[
  {
    "name": "CYP2D6*1",
    "gene": "CYP2D6",
    "function": "Normal function",
    "activityScore": 1.0,
    "frequencies": {
      "European": 0.42,
      "African": 0.37,
      "East Asian": 0.50,
      "Latino": 0.44
    },
    "definingVariants": ["Reference allele"],
    "pharmVarId": "PV00001"
  },
  {
    "name": "CYP2D6*4",
    "gene": "CYP2D6",
    "function": "No function",
    "activityScore": 0.0,
    "frequencies": {
      "European": 0.20,
      "African": 0.05,
      "East Asian": 0.01,
      "Latino": 0.10
    },
    "definingVariants": ["rs3892097"],
    "pharmVarId": "PV00004"
  }
]
```

#### Get Specific Allele

```http
GET /v1/allele/{allele_name}
```

**Parameters:**
- `allele_name` (path, required): Allele name with star nomenclature (e.g., CYP2D6*4)

**Example:**
```bash
curl "https://api.clinpgx.org/v1/allele/CYP2D6*4"
```

### 6. Variant Endpoint

Search for genetic variants and their pharmacogenomic annotations.

#### Get Variant by rsID

```http
GET /v1/variant/{rsid}
```

**Parameters:**
- `rsid` (path, required): dbSNP reference SNP ID

**Example Request:**
```bash
curl "https://api.clinpgx.org/v1/variant/rs4244285"
```

**Example Response:**
```json
{
  "rsid": "rs4244285",
  "chromosome": "10",
  "position": 94781859,
  "gene": "CYP2C19",
  "alleles": ["CYP2C19*2"],
  "consequence": "Splice site variant",
  "clinicalSignificance": "Pathogenic - reduced enzyme activity",
  "frequencies": {
    "European": 0.15,
    "African": 0.18,
    "East Asian": 0.29,
    "Latino": 0.12
  },
  "references": [...]
}
```

#### Search Variants by Position

```http
GET /v1/variant?chromosome={chr}&position={pos}
```

**Parameters:**
- `chromosome` (query, optional): Chromosome number (1-22, X, Y)
- `position` (query, optional): Genomic position (GRCh38)

**Example:**
```bash
curl "https://api.clinpgx.org/v1/variant?chromosome=10&position=94781859"
```

### 7. Clinical Annotation Endpoint

Access curated literature annotations for gene-drug-phenotype relationships.

#### Get Clinical Annotations

```http
GET /v1/clinicalAnnotation?gene={gene}&drug={drug}&evidenceLevel={level}
```

**Parameters:**
- `gene` (query, optional): Gene symbol
- `drug` (query, optional): Drug name
- `evidenceLevel` (query, optional): Evidence level (1A, 1B, 2A, 2B, 3, 4)
- `phenotype` (query, optional): Phenotype or outcome

**Example Requests:**
```bash
# Get all annotations for a gene
curl "https://api.clinpgx.org/v1/clinicalAnnotation?gene=CYP2D6"

# Get high-quality evidence only
curl "https://api.clinpgx.org/v1/clinicalAnnotation?evidenceLevel=1A"

# Get annotations for specific gene-drug pair
curl "https://api.clinpgx.org/v1/clinicalAnnotation?gene=TPMT&drug=azathioprine"
```

**Example Response:**
```json
[
  {
    "id": "PA166153683",
    "gene": "CYP2D6",
    "drug": "codeine",
    "phenotype": "Reduced analgesic effect",
    "evidenceLevel": "1A",
    "annotation": "Poor metabolizers have reduced conversion...",
    "pmid": "24618998",
    "studyType": "Clinical trial",
    "population": "European",
    "sources": ["CPIC"]
  }
]
```

**Evidence Levels:**
- **1A**: High-quality evidence from guidelines (CPIC, FDA, DPWG)
- **1B**: High-quality evidence not yet guideline
- **2A**: Moderate evidence from well-designed studies
- **2B**: Moderate evidence with some limitations
- **3**: Limited or conflicting evidence
- **4**: Case reports or weak evidence

### 8. Drug Label Endpoint

Retrieve regulatory drug label information with pharmacogenomic content.

#### Get Drug Labels

```http
GET /v1/drugLabel?drug={drug_name}&source={source}
```

**Parameters:**
- `drug` (query, required): Drug name
- `source` (query, optional): Regulatory source (FDA, EMA, PMDA, Health Canada)

**Example Requests:**
```bash
# Get all labels for warfarin
curl "https://api.clinpgx.org/v1/drugLabel?drug=warfarin"

# Get only FDA labels
curl "https://api.clinpgx.org/v1/drugLabel?drug=warfarin&source=FDA"
```

**Example Response:**
```json
[
  {
    "id": "DL001234",
    "drug": "warfarin",
    "source": "FDA",
    "sections": {
      "testing": "Consider CYP2C9 and VKORC1 genotyping...",
      "dosing": "Dose adjustment based on genotype...",
      "warnings": "Risk of bleeding in certain genotypes"
    },
    "biomarkers": ["CYP2C9", "VKORC1"],
    "testingRecommended": true,
    "labelUrl": "https://dailymed.nlm.nih.gov/...",
    "lastUpdated": "2024-01-15"
  }
]
```

### 9. Pathway Endpoint

Access pharmacokinetic and pharmacodynamic pathway diagrams and information.

#### Get Pathway by ID

```http
GET /v1/pathway/{pathway_id}
```

**Parameters:**
- `pathway_id` (path, required): ClinPGx pathway identifier

**Example:**
```bash
curl "https://api.clinpgx.org/v1/pathway/PA146123006"
```

#### Search Pathways

```http
GET /v1/pathway?drug={drug_name}&gene={gene}
```

**Parameters:**
- `drug` (query, optional): Drug name
- `gene` (query, optional): Gene symbol

**Example:**
```bash
curl "https://api.clinpgx.org/v1/pathway?drug=warfarin"
```

**Example Response:**
```json
{
  "id": "PA146123006",
  "name": "Warfarin Pharmacokinetics and Pharmacodynamics",
  "drugs": ["warfarin"],
  "genes": ["CYP2C9", "VKORC1", "CYP4F2", "GGCX"],
  "description": "Warfarin is metabolized primarily by CYP2C9...",
  "diagramUrl": "https://www.clinpgx.org/pathway/...",
  "steps": [
    {
      "step": 1,
      "process": "Absorption",
      "genes": []
    },
    {
      "step": 2,
      "process": "Metabolism",
      "genes": ["CYP2C9", "CYP2C19"]
    },
    {
      "step": 3,
      "process": "Target interaction",
      "genes": ["VKORC1"]
    }
  ]
}
```

## Query Patterns and Examples

### Common Query Patterns

#### 1. Patient Medication Review

Query all gene-drug pairs for a patient's medications:

```python
import requests

patient_meds = ["clopidogrel", "simvastatin", "codeine"]
patient_genes = {"CYP2C19": "*1/*2", "CYP2D6": "*1/*1", "SLCO1B1": "*1/*5"}

for med in patient_meds:
    for gene in patient_genes:
        response = requests.get(
            "https://api.clinpgx.org/v1/geneDrugPair",
            params={"gene": gene, "drug": med}
        )
        pairs = response.json()
        # Check for interactions
```

#### 2. Actionable Gene Panel

Find all genes with CPIC Level A recommendations:

```python
response = requests.get(
    "https://api.clinpgx.org/v1/geneDrugPair",
    params={"cpicLevel": "A"}
)
actionable_pairs = response.json()

genes = set(pair['gene'] for pair in actionable_pairs)
print(f"Panel should include: {sorted(genes)}")
```

#### 3. Population Frequency Analysis

Compare allele frequencies across populations:

```python
alleles = requests.get(
    "https://api.clinpgx.org/v1/allele",
    params={"gene": "CYP2D6"}
).json()

# Calculate phenotype frequencies
pm_freq = {}  # Poor metabolizer frequencies
for allele in alleles:
    if allele['function'] == 'No function':
        for pop, freq in allele['frequencies'].items():
            pm_freq[pop] = pm_freq.get(pop, 0) + freq
```

#### 4. Drug Safety Screen

Check for high-risk gene-drug associations:

```python
# Screen for HLA-B*57:01 before abacavir
response = requests.get(
    "https://api.clinpgx.org/v1/geneDrugPair",
    params={"gene": "HLA-B", "drug": "abacavir"}
)
pair = response.json()[0]

if pair['cpicLevel'] == 'A':
    print("CRITICAL: Do not use if HLA-B*57:01 positive")
```

## Error Handling

### Common Error Responses

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Gene 'INVALID' does not exist"
}
```

#### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 2 requests per second allowed"
}
```

### Recommended Error Handling Pattern

```python
import requests
import time

def safe_query(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                time.sleep(0.5)  # Rate limiting
                return response.json()
            elif response.status_code == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif response.status_code == 404:
                print("Resource not found")
                return None
            else:
                response.raise_for_status()

        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise

    return None
```

## Best Practices

### Rate Limiting
- Implement 500ms delay between requests (2 requests/second maximum)
- Use exponential backoff for rate limit errors
- Consider caching results for frequently accessed data
- For bulk operations, contact api@clinpgx.org

### Caching Strategy
```python
import json
from pathlib import Path

def cached_query(cache_file, query_func, *args, **kwargs):
    cache_path = Path(cache_file)

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    result = query_func(*args, **kwargs)

    if result:
        with open(cache_path, 'w') as f:
            json.dump(result, f)

    return result
```

### Batch Processing
```python
import time

def batch_gene_query(genes, delay=0.5):
    results = {}
    for gene in genes:
        response = requests.get(f"https://api.clinpgx.org/v1/gene/{gene}")
        if response.status_code == 200:
            results[gene] = response.json()
        time.sleep(delay)
    return results
```

## Data Schema Definitions

### Gene Object
```typescript
{
  id: string;              // ClinPGx gene ID
  symbol: string;          // HGNC gene symbol
  name: string;            // Full gene name
  chromosome: string;      // Chromosome location
  function: string;        // Pharmacogenomic function
  clinicalAnnotations: number;  // Count of annotations
  relatedDrugs: string[];  // Associated drugs
}
```

### Drug Object
```typescript
{
  id: string;              // ClinPGx drug ID
  name: string;            // Generic name
  tradeNames: string[];    // Brand names
  drugClasses: string[];   // Therapeutic classes
  indication: string;      // Primary indication
  relatedGenes: string[];  // Pharmacogenes
}
```

### Gene-Drug Pair Object
```typescript
{
  gene: string;            // Gene symbol
  drug: string;            // Drug name
  sources: string[];       // CPIC, FDA, DPWG, etc.
  cpicLevel: string;       // A, B, C, D
  evidenceLevel: string;   // 1A, 1B, 2A, 2B, 3, 4
  hasGuideline: boolean;   // Has clinical guideline
}
```

### Allele Object
```typescript
{
  name: string;            // Allele name (e.g., CYP2D6*4)
  gene: string;            // Gene symbol
  function: string;        // Normal/decreased/no/increased/uncertain
  activityScore: number;   // 0.0 to 2.0+
  frequencies: {           // Population frequencies
    [population: string]: number;
  };
  definingVariants: string[];  // rsIDs or descriptions
}
```

## API Stability and Versioning

### Current Status
- API version: v1
- Stability: Beta - endpoints stable, parameters may change
- Monitor: https://blog.clinpgx.org/ for updates

### Migration from PharmGKB
As of July 2025, PharmGKB URLs redirect to ClinPGx. Update references:
- Old: `https://api.pharmgkb.org/`
- New: `https://api.clinpgx.org/`

### Future Changes
- Watch for API v2 announcements
- Breaking changes will be announced on ClinPGx Blog
- Consider version pinning for production applications

## Support and Contact

- **API Issues**: api@clinpgx.org
- **Documentation**: https://api.clinpgx.org/
- **General Questions**: https://www.clinpgx.org/page/faqs
- **Blog**: https://blog.clinpgx.org/
- **CPIC Guidelines**: https://cpicpgx.org/

## Related Resources

- **PharmCAT**: Pharmacogenomic variant calling and annotation tool
- **PharmVar**: Pharmacogene allele nomenclature database
- **CPIC**: Clinical Pharmacogenetics Implementation Consortium
- **DPWG**: Dutch Pharmacogenetics Working Group
- **ClinGen**: Clinical Genome Resource
