---
title: "Gene Database"
description: "Query NCBI Gene via E-utilities/Datasets API. Search by symbol/ID, retrieve gene info (RefSeqs, GO, locations, phenotypes), batch lookups, for gene annotation and functional analysis."
category: "research"
source: "community"
author: "Community"
tags: ["gene", "database"]
date: 2026-03-20
---

# Gene Database

## Overview

NCBI Gene is a comprehensive database integrating gene information from diverse species. It provides nomenclature, reference sequences (RefSeqs), chromosomal maps, biological pathways, genetic variations, phenotypes, and cross-references to global genomic resources.

## When to Use This Skill

This skill should be used when working with gene data including searching by gene symbol or ID, retrieving gene sequences and metadata, analyzing gene functions and pathways, or performing batch gene lookups.

## Quick Start

NCBI provides two main APIs for gene data access:

1. **E-utilities** (Traditional): Full-featured API for all Entrez databases with flexible querying
2. **NCBI Datasets API** (Newer): Optimized for gene data retrieval with simplified workflows

Choose E-utilities for complex queries and cross-database searches. Choose Datasets API for straightforward gene data retrieval with metadata and sequences in a single request.

## Common Workflows

### Search Genes by Symbol or Name

To search for genes by symbol or name across organisms:

1. Use the `scripts/query_gene.py` script with E-utilities ESearch
2. Specify the gene symbol and organism (e.g., "BRCA1 in human")
3. The script returns matching Gene IDs

Example query patterns:
- Gene symbol: `insulin[gene name] AND human[organism]`
- Gene with disease: `dystrophin[gene name] AND muscular dystrophy[disease]`
- Chromosome location: `human[organism] AND 17q21[chromosome]`

### Retrieve Gene Information by ID

To fetch detailed information for known Gene IDs:

1. Use `scripts/fetch_gene_data.py` with the Datasets API for comprehensive data
2. Alternatively, use `scripts/query_gene.py` with E-utilities EFetch for specific formats
3. Specify desired output format (JSON, XML, or text)

The Datasets API returns:
- Gene nomenclature and aliases
- Reference sequences (RefSeqs) for transcripts and proteins
- Chromosomal location and mapping
- Gene Ontology (GO) annotations
- Associated publications

### Batch Gene Lookups

For multiple genes simultaneously:

1. Use `scripts/batch_gene_lookup.py` for efficient batch processing
2. Provide a list of gene symbols or IDs
3. Specify the organism for symbol-based queries
4. The script handles rate limiting automatically (10 requests/second with API key)

This workflow is useful for:
- Validating gene lists
- Retrieving metadata for gene panels
- Cross-referencing gene identifiers
- Building gene annotation tables

### Search by Biological Context

To find genes associated with specific biological functions or phenotypes:

1. Use E-utilities with Gene Ontology (GO) terms or phenotype keywords
2. Query by pathway names or disease associations
3. Filter by organism, chromosome, or other attributes

Example searches:
- By GO term: `GO:0006915[biological process]` (apoptosis)
- By phenotype: `diabetes[phenotype] AND mouse[organism]`
- By pathway: `insulin signaling pathway[pathway]`

### API Access Patterns

**Rate Limits:**
- Without API key: 3 requests/second for E-utilities, 5 requests/second for Datasets API
- With API key: 10 requests/second for both APIs

**Authentication:**
Register for a free NCBI API key at https://www.ncbi.nlm.nih.gov/account/ to increase rate limits.

**Error Handling:**
Both APIs return standard HTTP status codes. Common errors include:
- 400: Malformed query or invalid parameters
- 429: Rate limit exceeded
- 404: Gene ID not found

Retry failed requests with exponential backoff.

## Script Usage

### query_gene.py

Query NCBI Gene using E-utilities (ESearch, ESummary, EFetch).

```bash
python scripts/query_gene.py --search "BRCA1" --organism "human"
python scripts/query_gene.py --id 672 --format json
python scripts/query_gene.py --search "insulin[gene] AND diabetes[disease]"
```

### fetch_gene_data.py

Fetch comprehensive gene data using NCBI Datasets API.

```bash
python scripts/fetch_gene_data.py --gene-id 672
python scripts/fetch_gene_data.py --symbol BRCA1 --taxon human
python scripts/fetch_gene_data.py --symbol TP53 --taxon "Homo sapiens" --output json
```

### batch_gene_lookup.py

Process multiple gene queries efficiently.

```bash
python scripts/batch_gene_lookup.py --file gene_list.txt --organism human
python scripts/batch_gene_lookup.py --ids 672,7157,5594 --output results.json
```

## API References

For detailed API documentation including endpoints, parameters, response formats, and examples, refer to:

- `references/api_reference.md` - Comprehensive API documentation for E-utilities and Datasets API
- `references/common_workflows.md` - Additional examples and use case patterns

Search these references when needing specific API endpoint details, parameter options, or response structure information.

## Data Formats

NCBI Gene data can be retrieved in multiple formats:

- **JSON**: Structured data ideal for programmatic processing
- **XML**: Detailed hierarchical format with full metadata
- **GenBank**: Sequence data with annotations
- **FASTA**: Sequence data only
- **Text**: Human-readable summaries

Choose JSON for modern applications, XML for legacy systems requiring detailed metadata, and FASTA for sequence analysis workflows.

## Best Practices

1. **Always specify organism** when searching by gene symbol to avoid ambiguity
2. **Use Gene IDs** for precise lookups when available
3. **Batch requests** when working with multiple genes to minimize API calls
4. **Cache results** locally to reduce redundant queries
5. **Include API key** in scripts for higher rate limits
6. **Handle errors gracefully** with retry logic for transient failures
7. **Validate gene symbols** before batch processing to catch typos

## Resources

This skill includes:

### scripts/
- `query_gene.py` - Query genes using E-utilities (ESearch, ESummary, EFetch)
- `fetch_gene_data.py` - Fetch gene data using NCBI Datasets API
- `batch_gene_lookup.py` - Handle multiple gene queries efficiently

### references/
- `api_reference.md` - Detailed API documentation for both E-utilities and Datasets API
- `common_workflows.md` - Examples of common gene queries and use cases

---

## Reference: Api_Reference

# NCBI Gene API Reference

This document provides detailed API documentation for accessing NCBI Gene database programmatically.

## Table of Contents

1. [E-utilities API](#e-utilities-api)
2. [NCBI Datasets API](#ncbi-datasets-api)
3. [Authentication and Rate Limits](#authentication-and-rate-limits)
4. [Error Handling](#error-handling)

---

## E-utilities API

E-utilities (Entrez Programming Utilities) provide a stable interface to NCBI's Entrez databases.

### Base URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

### Common Parameters

- `db` - Database name (use `gene` for Gene database)
- `api_key` - API key for higher rate limits
- `retmode` - Return format (json, xml, text)
- `retmax` - Maximum number of records to return

### ESearch - Search Database

Search for genes matching a text query.

**Endpoint:** `esearch.fcgi`

**Parameters:**
- `db=gene` (required) - Database to search
- `term` (required) - Search query
- `retmax` - Maximum results (default: 20)
- `retmode` - json or xml (default: xml)
- `usehistory=y` - Store results on history server for large result sets

**Query Syntax:**
- Gene symbol: `BRCA1[gene]` or `BRCA1[gene name]`
- Organism: `human[organism]` or `9606[taxid]`
- Combine terms: `BRCA1[gene] AND human[organism]`
- Disease: `muscular dystrophy[disease]`
- Chromosome: `17q21[chromosome]`
- GO terms: `GO:0006915[biological process]`

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=BRCA1[gene]+AND+human[organism]&retmode=json"
```

**Response Format (JSON):**

```json
{
  "esearchresult": {
    "count": "1",
    "retmax": "1",
    "retstart": "0",
    "idlist": ["672"],
    "translationset": [],
    "querytranslation": "BRCA1[Gene Name] AND human[Organism]"
  }
}
```

### ESummary - Document Summaries

Retrieve document summaries for Gene IDs.

**Endpoint:** `esummary.fcgi`

**Parameters:**
- `db=gene` (required) - Database
- `id` (required) - Comma-separated Gene IDs (up to 500)
- `retmode` - json or xml (default: xml)

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=672&retmode=json"
```

**Response Format (JSON):**

```json
{
  "result": {
    "672": {
      "uid": "672",
      "name": "BRCA1",
      "description": "BRCA1 DNA repair associated",
      "organism": {
        "scientificname": "Homo sapiens",
        "commonname": "human",
        "taxid": 9606
      },
      "chromosome": "17",
      "geneticsource": "genomic",
      "maplocation": "17q21.31",
      "nomenclaturesymbol": "BRCA1",
      "nomenclaturename": "BRCA1 DNA repair associated"
    }
  }
}
```

### EFetch - Full Records

Fetch detailed gene records in various formats.

**Endpoint:** `efetch.fcgi`

**Parameters:**
- `db=gene` (required) - Database
- `id` (required) - Comma-separated Gene IDs
- `retmode` - xml, text, asn.1 (default: xml)
- `rettype` - gene_table, docsum

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id=672&retmode=xml"
```

**XML Response:** Contains detailed gene information including:
- Gene nomenclature
- Sequence locations
- Transcript variants
- Protein products
- Gene Ontology annotations
- Cross-references
- Publications

### ELink - Related Records

Find related records in Gene or other databases.

**Endpoint:** `elink.fcgi`

**Parameters:**
- `dbfrom=gene` (required) - Source database
- `db` (required) - Target database (gene, nuccore, protein, pubmed, etc.)
- `id` (required) - Gene ID(s)

**Example Request:**

```bash
# Get related PubMed articles
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=pubmed&id=672&retmode=json"
```

### EInfo - Database Information

Get information about the Gene database.

**Endpoint:** `einfo.fcgi`

**Parameters:**
- `db=gene` - Database to query

**Example Request:**

```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=gene&retmode=json"
```

---

## NCBI Datasets API

The Datasets API provides streamlined access to gene data with metadata and sequences.

### Base URL

```
https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene
```

### Authentication

Include API key in request headers:

```
api-key: YOUR_API_KEY
```

### Get Gene by ID

Retrieve gene data by Gene ID.

**Endpoint:** `GET /gene/id/{gene_id}`

**Example Request:**

```bash
curl "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/id/672"
```

**Response Format (JSON):**

```json
{
  "genes": [
    {
      "gene": {
        "gene_id": "672",
        "symbol": "BRCA1",
        "description": "BRCA1 DNA repair associated",
        "tax_name": "Homo sapiens",
        "taxid": 9606,
        "chromosomes": ["17"],
        "type": "protein-coding",
        "synonyms": ["BRCC1", "FANCS", "PNCA4", "RNF53"],
        "nomenclature_authority": {
          "authority": "HGNC",
          "identifier": "HGNC:1100"
        },
        "genomic_ranges": [
          {
            "accession_version": "NC_000017.11",
            "range": [
              {
                "begin": 43044295,
                "end": 43170245,
                "orientation": "minus"
              }
            ]
          }
        ],
        "transcripts": [
          {
            "accession_version": "NM_007294.4",
            "length": 7207
          }
        ]
      }
    }
  ]
}
```

### Get Gene by Symbol

Retrieve gene data by symbol and organism.

**Endpoint:** `GET /gene/symbol/{symbol}/taxon/{taxon}`

**Parameters:**
- `{symbol}` - Gene symbol (e.g., BRCA1)
- `{taxon}` - Taxon ID (e.g., 9606 for human)

**Example Request:**

```bash
curl "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/symbol/BRCA1/taxon/9606"
```

### Get Multiple Genes

Retrieve data for multiple genes.

**Endpoint:** `POST /gene/id`

**Request Body:**

```json
{
  "gene_ids": ["672", "7157", "5594"]
}
```

**Example Request:**

```bash
curl -X POST "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/id" \
  -H "Content-Type: application/json" \
  -d '{"gene_ids": ["672", "7157", "5594"]}'
```

---

## Authentication and Rate Limits

### Obtaining an API Key

1. Create an NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Navigate to Settings → API Key Management
3. Generate a new API key
4. Include the key in requests

### Rate Limits

**E-utilities:**
- Without API key: 3 requests/second
- With API key: 10 requests/second

**Datasets API:**
- Without API key: 5 requests/second
- With API key: 10 requests/second

### Usage Guidelines

1. **Include email in requests:** Add `&email=your@email.com` to E-utilities requests
2. **Implement rate limiting:** Use delays between requests
3. **Use POST for large queries:** When working with many IDs
4. **Cache results:** Store frequently accessed data locally
5. **Handle errors gracefully:** Implement retry logic with exponential backoff

---

## Error Handling

### HTTP Status Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters or malformed query
- `404 Not Found` - Gene ID or symbol not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error (retry with backoff)

### E-utilities Error Messages

E-utilities return errors in the response body:

**XML format:**
```xml
<ERROR>Empty id list - nothing to do</ERROR>
```

**JSON format:**
```json
{
  "error": "Invalid db name"
}
```

### Common Errors

1. **Empty Result Set**
   - Cause: Gene symbol or ID not found
   - Solution: Verify spelling, check organism filter

2. **Rate Limit Exceeded**
   - Cause: Too many requests
   - Solution: Add delays, use API key

3. **Invalid Query Syntax**
   - Cause: Malformed search term
   - Solution: Use proper field tags (e.g., `[gene]`, `[organism]`)

4. **Timeout**
   - Cause: Large result set or slow connection
   - Solution: Use History Server, reduce result size

### Retry Strategy

Implement exponential backoff for failed requests:

```python
import time

def retry_request(func, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise
```

---

## Common Taxon IDs

| Organism | Scientific Name | Taxon ID |
|----------|----------------|----------|
| Human | Homo sapiens | 9606 |
| Mouse | Mus musculus | 10090 |
| Rat | Rattus norvegicus | 10116 |
| Zebrafish | Danio rerio | 7955 |
| Fruit fly | Drosophila melanogaster | 7227 |
| C. elegans | Caenorhabditis elegans | 6239 |
| Yeast | Saccharomyces cerevisiae | 4932 |
| Arabidopsis | Arabidopsis thaliana | 3702 |
| E. coli | Escherichia coli | 562 |

---

## Additional Resources

- **E-utilities Documentation:** https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Datasets API Documentation:** https://www.ncbi.nlm.nih.gov/datasets/docs/v2/
- **Gene Database Help:** https://www.ncbi.nlm.nih.gov/gene/
- **API Key Registration:** https://www.ncbi.nlm.nih.gov/account/

---

## Reference: Common_Workflows

# Common Gene Database Workflows

This document provides examples of common workflows and use cases for working with NCBI Gene database.

## Table of Contents

1. [Disease Gene Discovery](#disease-gene-discovery)
2. [Gene Annotation Pipeline](#gene-annotation-pipeline)
3. [Cross-Species Gene Comparison](#cross-species-gene-comparison)
4. [Pathway Analysis](#pathway-analysis)
5. [Variant Analysis](#variant-analysis)
6. [Publication Mining](#publication-mining)

---

## Disease Gene Discovery

### Use Case

Identify genes associated with a specific disease or phenotype.

### Workflow

1. **Search by disease name**

```bash
# Find genes associated with Alzheimer's disease
python scripts/query_gene.py --search "Alzheimer disease[disease]" --organism human --max-results 50
```

2. **Filter by chromosome location**

```bash
# Find genes on chromosome 17 associated with breast cancer
python scripts/query_gene.py --search "breast cancer[disease] AND 17[chromosome]" --organism human
```

3. **Retrieve detailed information**

```python
# Python example: Get gene details for disease-associated genes
import json
from scripts.query_gene import esearch, esummary

# Search for genes
query = "diabetes[disease] AND human[organism]"
gene_ids = esearch(query, retmax=100, api_key="YOUR_KEY")

# Get summaries
summaries = esummary(gene_ids, api_key="YOUR_KEY")

# Extract relevant information
for gene_id in gene_ids:
    if gene_id in summaries['result']:
        gene = summaries['result'][gene_id]
        print(f"{gene['name']}: {gene['description']}")
```

### Expected Output

- List of genes with disease associations
- Gene symbols, descriptions, and chromosomal locations
- Related publications and clinical annotations

---

## Gene Annotation Pipeline

### Use Case

Annotate a list of gene identifiers with comprehensive metadata.

### Workflow

1. **Prepare gene list**

Create a file `genes.txt` with gene symbols (one per line):
```
BRCA1
TP53
EGFR
KRAS
```

2. **Batch lookup**

```bash
python scripts/batch_gene_lookup.py --file genes.txt --organism human --output annotations.json --api-key YOUR_KEY
```

3. **Parse results**

```python
import json

with open('annotations.json', 'r') as f:
    genes = json.load(f)

for gene in genes:
    if 'gene_id' in gene:
        print(f"Symbol: {gene['symbol']}")
        print(f"ID: {gene['gene_id']}")
        print(f"Description: {gene['description']}")
        print(f"Location: chr{gene['chromosome']}:{gene['map_location']}")
        print()
```

4. **Enrich with sequence data**

```bash
# Get detailed data including sequences for specific genes
python scripts/fetch_gene_data.py --gene-id 672 --verbose > BRCA1_detailed.json
```

### Use Cases

- Creating gene annotation tables for publications
- Validating gene lists before analysis
- Building gene reference databases
- Quality control for genomic pipelines

---

## Cross-Species Gene Comparison

### Use Case

Find orthologs or compare the same gene across different species.

### Workflow

1. **Search for gene in multiple organisms**

```bash
# Find TP53 in human
python scripts/fetch_gene_data.py --symbol TP53 --taxon human

# Find TP53 in mouse
python scripts/fetch_gene_data.py --symbol TP53 --taxon mouse

# Find TP53 in zebrafish
python scripts/fetch_gene_data.py --symbol TP53 --taxon zebrafish
```

2. **Compare gene IDs across species**

```python
# Compare gene information across species
species = {
    'human': '9606',
    'mouse': '10090',
    'rat': '10116'
}

gene_symbol = 'TP53'

for organism, taxon_id in species.items():
    # Fetch gene data
    # ... (use fetch_gene_by_symbol)
    print(f"{organism}: {gene_data}")
```

3. **Find orthologs using ELink**

```bash
# Get HomoloGene links for a gene
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=homologene&id=7157&retmode=json"
```

### Applications

- Evolutionary studies
- Model organism research
- Comparative genomics
- Cross-species experimental design

---

## Pathway Analysis

### Use Case

Identify genes involved in specific biological pathways or processes.

### Workflow

1. **Search by Gene Ontology (GO) term**

```bash
# Find genes involved in apoptosis
python scripts/query_gene.py --search "GO:0006915[biological process]" --organism human --max-results 100
```

2. **Search by pathway name**

```bash
# Find genes in insulin signaling pathway
python scripts/query_gene.py --search "insulin signaling pathway[pathway]" --organism human
```

3. **Get pathway-related genes**

```python
# Example: Get all genes in a specific pathway
import urllib.request
import json

# Search for pathway genes
query = "MAPK signaling pathway[pathway] AND human[organism]"
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term={query}&retmode=json&retmax=200"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    gene_ids = data['esearchresult']['idlist']

print(f"Found {len(gene_ids)} genes in MAPK signaling pathway")
```

4. **Batch retrieve gene details**

```bash
# Get details for all pathway genes
python scripts/batch_gene_lookup.py --ids 5594,5595,5603,5604 --output mapk_genes.json
```

### Applications

- Pathway enrichment analysis
- Gene set analysis
- Systems biology studies
- Drug target identification

---

## Variant Analysis

### Use Case

Find genes with clinically relevant variants or disease-associated mutations.

### Workflow

1. **Search for genes with clinical variants**

```bash
# Find genes with pathogenic variants
python scripts/query_gene.py --search "pathogenic[clinical significance]" --organism human --max-results 50
```

2. **Link to ClinVar database**

```bash
# Get ClinVar records for a gene
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=clinvar&id=672&retmode=json"
```

3. **Search for pharmacogenomic genes**

```bash
# Find genes associated with drug response
python scripts/query_gene.py --search "pharmacogenomic[property]" --organism human
```

4. **Get variant summary data**

```python
# Example: Get genes with known variants
from scripts.query_gene import esearch, efetch

# Search for genes with variants
gene_ids = esearch("has variants[filter] AND human[organism]", retmax=100)

# Fetch detailed records
for gene_id in gene_ids[:10]:  # First 10
    data = efetch([gene_id], retmode='xml')
    # Parse XML for variant information
    print(f"Gene {gene_id} variant data...")
```

### Applications

- Clinical genetics
- Precision medicine
- Pharmacogenomics
- Genetic counseling

---

## Publication Mining

### Use Case

Find genes mentioned in recent publications or link genes to literature.

### Workflow

1. **Search genes mentioned in specific publications**

```bash
# Find genes mentioned in papers about CRISPR
python scripts/query_gene.py --search "CRISPR[text word]" --organism human --max-results 100
```

2. **Get PubMed articles for a gene**

```bash
# Get all publications for BRCA1
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=pubmed&id=672&retmode=json"
```

3. **Search by author or journal**

```bash
# Find genes studied by specific research group
python scripts/query_gene.py --search "Smith J[author] AND 2024[pdat]" --organism human
```

4. **Extract gene-publication relationships**

```python
# Example: Build gene-publication network
from scripts.query_gene import esearch, esummary
import urllib.request
import json

# Get gene
gene_id = '672'

# Get publications for gene
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=pubmed&id={gene_id}&retmode=json"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

# Extract PMIDs
pmids = []
for linkset in data.get('linksets', []):
    for linksetdb in linkset.get('linksetdbs', []):
        pmids.extend(linksetdb.get('links', []))

print(f"Gene {gene_id} has {len(pmids)} publications")
```

### Applications

- Literature reviews
- Grant writing
- Knowledge base construction
- Trend analysis in genomics research

---

## Advanced Patterns

### Combining Multiple Searches

```python
# Example: Find genes at intersection of multiple criteria
def find_genes_multi_criteria(organism='human'):
    # Criteria 1: Disease association
    disease_genes = set(esearch("diabetes[disease] AND human[organism]"))

    # Criteria 2: Chromosome location
    chr_genes = set(esearch("11[chromosome] AND human[organism]"))

    # Criteria 3: Gene type
    coding_genes = set(esearch("protein coding[gene type] AND human[organism]"))

    # Intersection
    candidates = disease_genes & chr_genes & coding_genes

    return list(candidates)
```

### Rate-Limited Batch Processing

```python
import time

def process_genes_with_rate_limit(gene_ids, batch_size=200, delay=0.1):
    results = []

    for i in range(0, len(gene_ids), batch_size):
        batch = gene_ids[i:i + batch_size]

        # Process batch
        batch_results = esummary(batch)
        results.append(batch_results)

        # Rate limit
        time.sleep(delay)

    return results
```

### Error Handling and Retry

```python
import time

def robust_gene_fetch(gene_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            data = fetch_gene_by_id(gene_id)
            return data
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                time.sleep(wait)
            else:
                print(f"Failed to fetch gene {gene_id}: {e}")
                return None
```

---

## Tips and Best Practices

1. **Start Specific, Then Broaden**: Begin with precise queries and expand if needed
2. **Use Organism Filters**: Always specify organism for gene symbol searches
3. **Validate Results**: Check gene IDs and symbols for accuracy
4. **Cache Frequently Used Data**: Store common queries locally
5. **Monitor Rate Limits**: Use API keys and implement delays
6. **Combine APIs**: Use E-utilities for search, Datasets API for detailed data
7. **Handle Ambiguity**: Gene symbols may refer to different genes in different species
8. **Check Data Currency**: Gene annotations are updated regularly
9. **Use Batch Operations**: Process multiple genes together when possible
10. **Document Your Queries**: Keep records of search terms and parameters
