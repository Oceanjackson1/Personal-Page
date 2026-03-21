---
title: "Ensembl Database"
description: "Query Ensembl genome database REST API for 250+ species. Gene lookups, sequence retrieval, variant analysis, comparative genomics, orthologs, VEP predictions, for genomic research."
category: "research"
source: "community"
author: "Community"
tags: ["ensembl", "database"]
date: 2026-03-20
---

# Ensembl Database

## Overview

Access and query the Ensembl genome database, a comprehensive resource for vertebrate genomic data maintained by EMBL-EBI. The database provides gene annotations, sequences, variants, regulatory information, and comparative genomics data for over 250 species. Current release is 115 (September 2025).

## When to Use This Skill

This skill should be used when:

- Querying gene information by symbol or Ensembl ID
- Retrieving DNA, transcript, or protein sequences
- Analyzing genetic variants using the Variant Effect Predictor (VEP)
- Finding orthologs and paralogs across species
- Accessing regulatory features and genomic annotations
- Converting coordinates between genome assemblies (e.g., GRCh37 to GRCh38)
- Performing comparative genomics analyses
- Integrating Ensembl data into genomic research pipelines

## Core Capabilities

### 1. Gene Information Retrieval

Query gene data by symbol, Ensembl ID, or external database identifiers.

**Common operations:**
- Look up gene information by symbol (e.g., "BRCA2", "TP53")
- Retrieve transcript and protein information
- Get gene coordinates and chromosomal locations
- Access cross-references to external databases (UniProt, RefSeq, etc.)

**Using the ensembl_rest package:**
```python
from ensembl_rest import EnsemblClient

client = EnsemblClient()

# Look up gene by symbol
gene_data = client.symbol_lookup(
    species='human',
    symbol='BRCA2'
)

# Get detailed gene information
gene_info = client.lookup_id(
    id='ENSG00000139618',  # BRCA2 Ensembl ID
    expand=True
)
```

**Direct REST API (no package):**
```python
import requests

server = "https://rest.ensembl.org"

# Symbol lookup
response = requests.get(
    f"{server}/lookup/symbol/homo_sapiens/BRCA2",
    headers={"Content-Type": "application/json"}
)
gene_data = response.json()
```

### 2. Sequence Retrieval

Fetch genomic, transcript, or protein sequences in various formats (JSON, FASTA, plain text).

**Operations:**
- Get DNA sequences for genes or genomic regions
- Retrieve transcript sequences (cDNA)
- Access protein sequences
- Extract sequences with flanking regions or modifications

**Example:**
```python
# Using ensembl_rest package
sequence = client.sequence_id(
    id='ENSG00000139618',  # Gene ID
    content_type='application/json'
)

# Get sequence for a genomic region
region_seq = client.sequence_region(
    species='human',
    region='7:140424943-140624564'  # chromosome:start-end
)
```

### 3. Variant Analysis

Query genetic variation data and predict variant consequences using the Variant Effect Predictor (VEP).

**Capabilities:**
- Look up variants by rsID or genomic coordinates
- Predict functional consequences of variants
- Access population frequency data
- Retrieve phenotype associations

**VEP example:**
```python
# Predict variant consequences
vep_result = client.vep_hgvs(
    species='human',
    hgvs_notation='ENST00000380152.7:c.803C>T'
)

# Query variant by rsID
variant = client.variation_id(
    species='human',
    id='rs699'
)
```

### 4. Comparative Genomics

Perform cross-species comparisons to identify orthologs, paralogs, and evolutionary relationships.

**Operations:**
- Find orthologs (same gene in different species)
- Identify paralogs (related genes in same species)
- Access gene trees showing evolutionary relationships
- Retrieve gene family information

**Example:**
```python
# Find orthologs for a human gene
orthologs = client.homology_ensemblgene(
    id='ENSG00000139618',  # Human BRCA2
    target_species='mouse'
)

# Get gene tree
gene_tree = client.genetree_member_symbol(
    species='human',
    symbol='BRCA2'
)
```

### 5. Genomic Region Analysis

Find all genomic features (genes, transcripts, regulatory elements) in a specific region.

**Use cases:**
- Identify all genes in a chromosomal region
- Find regulatory features (promoters, enhancers)
- Locate variants within a region
- Retrieve structural features

**Example:**
```python
# Find all features in a region
features = client.overlap_region(
    species='human',
    region='7:140424943-140624564',
    feature='gene'
)
```

### 6. Assembly Mapping

Convert coordinates between different genome assemblies (e.g., GRCh37 to GRCh38).

**Important:** Use `https://grch37.rest.ensembl.org` for GRCh37/hg19 queries and `https://rest.ensembl.org` for current assemblies.

**Example:**
```python
from ensembl_rest import AssemblyMapper

# Map coordinates from GRCh37 to GRCh38
mapper = AssemblyMapper(
    species='human',
    asm_from='GRCh37',
    asm_to='GRCh38'
)

mapped = mapper.map(chrom='7', start=140453136, end=140453136)
```

## API Best Practices

### Rate Limiting

The Ensembl REST API has rate limits. Follow these practices:

1. **Respect rate limits:** Maximum 15 requests per second for anonymous users
2. **Handle 429 responses:** When rate-limited, check the `Retry-After` header and wait
3. **Use batch endpoints:** When querying multiple items, use batch endpoints where available
4. **Cache results:** Store frequently accessed data to reduce API calls

### Error Handling

Always implement proper error handling:

```python
import requests
import time

def query_ensembl(endpoint, params=None, max_retries=3):
    server = "https://rest.ensembl.org"
    headers = {"Content-Type": "application/json"}

    for attempt in range(max_retries):
        response = requests.get(
            f"{server}{endpoint}",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            # Rate limited - wait and retry
            retry_after = int(response.headers.get('Retry-After', 1))
            time.sleep(retry_after)
        else:
            response.raise_for_status()

    raise Exception(f"Failed after {max_retries} attempts")
```

## Installation

### Python Package (Recommended)

```bash
uv pip install ensembl_rest
```

The `ensembl_rest` package provides a Pythonic interface to all Ensembl REST API endpoints.

### Direct REST API

No installation needed - use standard HTTP libraries like `requests`:

```bash
uv pip install requests
```

## Resources

### references/

- `api_endpoints.md`: Comprehensive documentation of all 17 API endpoint categories with examples and parameters

### scripts/

- `ensembl_query.py`: Reusable Python script for common Ensembl queries with built-in rate limiting and error handling

## Common Workflows

### Workflow 1: Gene Annotation Pipeline

1. Look up gene by symbol to get Ensembl ID
2. Retrieve transcript information
3. Get protein sequences for all transcripts
4. Find orthologs in other species
5. Export results

### Workflow 2: Variant Analysis

1. Query variant by rsID or coordinates
2. Use VEP to predict functional consequences
3. Check population frequencies
4. Retrieve phenotype associations
5. Generate report

### Workflow 3: Comparative Analysis

1. Start with gene of interest in reference species
2. Find orthologs in target species
3. Retrieve sequences for all orthologs
4. Compare gene structures and features
5. Analyze evolutionary conservation

## Species and Assembly Information

To query available species and assemblies:

```python
# List all available species
species_list = client.info_species()

# Get assembly information for a species
assembly_info = client.info_assembly(species='human')
```

Common species identifiers:
- Human: `homo_sapiens` or `human`
- Mouse: `mus_musculus` or `mouse`
- Zebrafish: `danio_rerio` or `zebrafish`
- Fruit fly: `drosophila_melanogaster`

## Additional Resources

- **Official Documentation:** https://rest.ensembl.org/documentation
- **Python Package Docs:** https://ensemblrest.readthedocs.io
- **EBI Training:** https://www.ebi.ac.uk/training/online/courses/ensembl-rest-api/
- **Ensembl Browser:** https://useast.ensembl.org
- **GitHub Examples:** https://github.com/Ensembl/ensembl-rest/wiki

---

## Reference: Api_Endpoints

# Ensembl REST API Endpoints Reference

Comprehensive documentation of all 17 API endpoint categories available in the Ensembl REST API (Release 115, September 2025).

**Base URLs:**
- Current assemblies: `https://rest.ensembl.org`
- GRCh37/hg19 (human): `https://grch37.rest.ensembl.org`

**Rate Limits:**
- Anonymous: 15 requests/second
- Registered: 55,000 requests/hour

## 1. Archive

Retrieve historical information about retired Ensembl identifiers.

**GET /archive/id/:id**
- Retrieve archived entries for a retired identifier
- Example: `/archive/id/ENSG00000157764` (retired gene ID)

## 2. Comparative Genomics

Access gene trees, genomic alignments, and homology data across species.

**GET /alignment/region/:species/:region**
- Get genomic alignments for a region
- Example: `/alignment/region/human/2:106040000-106040050:1?species_set_group=mammals`

**GET /genetree/id/:id**
- Retrieve gene tree for a gene family
- Example: `/genetree/id/ENSGT00390000003602`

**GET /genetree/member/id/:id**
- Get gene tree by member gene ID
- Example: `/genetree/member/id/ENSG00000139618`

**GET /homology/id/:id**
- Find orthologs and paralogs for a gene
- Parameters: `target_species`, `type` (orthologues, paralogues, all)
- Example: `/homology/id/ENSG00000139618?target_species=mouse`

**GET /homology/symbol/:species/:symbol**
- Find homologs by gene symbol
- Example: `/homology/symbol/human/BRCA2?target_species=mouse`

## 3. Cross References

Link external database identifiers to Ensembl objects.

**GET /xrefs/id/:id**
- Get external references for Ensembl ID
- Example: `/xrefs/id/ENSG00000139618`

**GET /xrefs/symbol/:species/:symbol**
- Get cross-references by gene symbol
- Example: `/xrefs/symbol/human/BRCA2`

**GET /xrefs/name/:species/:name**
- Search for objects by external name
- Example: `/xrefs/name/human/NP_000050`

## 4. Information

Query metadata about species, assemblies, biotypes, and database versions.

**GET /info/species**
- List all available species
- Returns species names, assemblies, taxonomy IDs

**GET /info/assembly/:species**
- Get assembly information for a species
- Example: `/info/assembly/human` (returns GRCh38.p14)

**GET /info/assembly/:species/:region**
- Get detailed information about a chromosomal region
- Example: `/info/assembly/human/X`

**GET /info/biotypes/:species**
- List all available biotypes (gene types)
- Example: `/info/biotypes/human`

**GET /info/analysis/:species**
- List available analysis types
- Example: `/info/analysis/human`

**GET /info/data**
- Get general information about the current Ensembl release

## 5. Linkage Disequilibrium (LD)

Calculate linkage disequilibrium between variants.

**GET /ld/:species/:id/:population_name**
- Calculate LD for a variant
- Example: `/ld/human/rs1042522/1000GENOMES:phase_3:KHV`

**GET /ld/pairwise/:species/:id1/:id2**
- Calculate LD between two variants
- Example: `/ld/pairwise/human/rs1042522/rs11540652`

## 6. Lookup

Identify species and database information for identifiers.

**GET /lookup/id/:id**
- Look up object by Ensembl ID
- Parameter: `expand` (include child objects)
- Example: `/lookup/id/ENSG00000139618?expand=1`

**POST /lookup/id**
- Batch lookup multiple IDs
- Submit JSON array of IDs
- Example: `{"ids": ["ENSG00000139618", "ENSG00000157764"]}`

**GET /lookup/symbol/:species/:symbol**
- Look up gene by symbol
- Parameter: `expand` (include transcripts)
- Example: `/lookup/symbol/human/BRCA2?expand=1`

## 7. Mapping

Convert coordinates between assemblies, cDNA, CDS, and protein positions.

**GET /map/cdna/:id/:region**
- Map cDNA coordinates to genomic
- Example: `/map/cdna/ENST00000288602/100..300`

**GET /map/cds/:id/:region**
- Map CDS coordinates to genomic
- Example: `/map/cds/ENST00000288602/1..300`

**GET /map/translation/:id/:region**
- Map protein coordinates to genomic
- Example: `/map/translation/ENSP00000288602/1..100`

**GET /map/:species/:asm_one/:region/:asm_two**
- Map coordinates between assemblies
- Example: `/map/human/GRCh37/7:140453136..140453136/GRCh38`

**POST /map/:species/:asm_one/:asm_two**
- Batch assembly mapping
- Submit JSON array of regions

## 8. Ontologies and Taxonomy

Search biological ontologies and taxonomic classifications.

**GET /ontology/id/:id**
- Get ontology term information
- Example: `/ontology/id/GO:0005515`

**GET /ontology/name/:name**
- Search ontology by term name
- Example: `/ontology/name/protein%20binding`

**GET /taxonomy/classification/:id**
- Get taxonomic classification
- Example: `/taxonomy/classification/9606` (human)

**GET /taxonomy/id/:id**
- Get taxonomy information by ID
- Example: `/taxonomy/id/9606`

## 9. Overlap

Find genomic features overlapping a region.

**GET /overlap/id/:id**
- Get features overlapping a gene/transcript
- Parameters: `feature` (gene, transcript, cds, exon, repeat, etc.)
- Example: `/overlap/id/ENSG00000139618?feature=transcript`

**GET /overlap/region/:species/:region**
- Get all features in a genomic region
- Parameters: `feature` (gene, transcript, variation, regulatory, etc.)
- Example: `/overlap/region/human/7:140424943..140624564?feature=gene`

**GET /overlap/translation/:id**
- Get protein features
- Example: `/overlap/translation/ENSP00000288602`

## 10. Phenotype Annotations

Retrieve disease and trait associations.

**GET /phenotype/accession/:species/:accession**
- Get phenotypes by ontology accession
- Example: `/phenotype/accession/human/EFO:0003767`

**GET /phenotype/gene/:species/:gene**
- Get phenotype associations for a gene
- Example: `/phenotype/gene/human/ENSG00000139618`

**GET /phenotype/region/:species/:region**
- Get phenotypes in genomic region
- Example: `/phenotype/region/human/7:140424943-140624564`

**GET /phenotype/term/:species/:term**
- Search phenotypes by term
- Example: `/phenotype/term/human/cancer`

## 11. Regulation

Access regulatory feature and binding motif data.

**GET /regulatory/species/:species/microarray/:microarray/:probe**
- Get microarray probe information
- Example: `/regulatory/species/human/microarray/HumanWG_6_V2/ILMN_1773626`

**GET /species/:species/binding_matrix/:binding_matrix_id**
- Get transcription factor binding matrix
- Example: `/species/human/binding_matrix/ENSPFM0001`

## 12. Sequence

Retrieve genomic, transcript, and protein sequences.

**GET /sequence/id/:id**
- Get sequence by ID
- Parameters: `type` (genomic, cds, cdna, protein), `format` (json, fasta, text)
- Example: `/sequence/id/ENSG00000139618?type=genomic`

**POST /sequence/id**
- Batch sequence retrieval
- Example: `{"ids": ["ENSG00000139618", "ENSG00000157764"]}`

**GET /sequence/region/:species/:region**
- Get genomic sequence for region
- Parameters: `coord_system`, `format`
- Example: `/sequence/region/human/7:140424943..140624564?format=fasta`

**POST /sequence/region/:species**
- Batch region sequence retrieval

## 13. Transcript Haplotypes

Compute transcript haplotypes from phased genotypes.

**GET /transcript_haplotypes/:species/:id**
- Get transcript haplotypes
- Example: `/transcript_haplotypes/human/ENST00000288602`

## 14. Variant Effect Predictor (VEP)

Predict functional consequences of variants.

**GET /vep/:species/hgvs/:hgvs_notation**
- Predict variant effects using HGVS notation
- Parameters: numerous VEP options
- Example: `/vep/human/hgvs/ENST00000288602:c.803C>T`

**POST /vep/:species/hgvs**
- Batch VEP analysis with HGVS
- Example: `{"hgvs_notations": ["ENST00000288602:c.803C>T"]}`

**GET /vep/:species/id/:id**
- Predict effects for variant ID
- Example: `/vep/human/id/rs699`

**POST /vep/:species/id**
- Batch VEP by variant IDs

**GET /vep/:species/region/:region/:allele**
- Predict effects for region and allele
- Example: `/vep/human/region/7:140453136:C/T`

**POST /vep/:species/region**
- Batch VEP by regions

## 15. Variation

Query genetic variation data and associated publications.

**GET /variation/:species/:id**
- Get variant information by ID
- Parameters: `pops` (include population frequencies), `genotypes`
- Example: `/variation/human/rs699?pops=1`

**POST /variation/:species**
- Batch variant queries
- Example: `{"ids": ["rs699", "rs6025"]}`

**GET /variation/:species/pmcid/:pmcid**
- Get variants from PubMed Central article
- Example: `/variation/human/pmcid/PMC5002951`

**GET /variation/:species/pmid/:pmid**
- Get variants from PubMed article
- Example: `/variation/human/pmid/26318936`

## 16. Variation GA4GH

Access genomic variation data using GA4GH standards.

**POST /ga4gh/beacon**
- Query beacon for variant presence

**GET /ga4gh/features/:id**
- Get feature by ID in GA4GH format

**POST /ga4gh/features/search**
- Search features using GA4GH protocol

**POST /ga4gh/variants/search**
- Search variants using GA4GH protocol

## Response Formats

Most endpoints support multiple response formats:
- **JSON** (default): `Content-Type: application/json`
- **FASTA**: For sequence data
- **XML**: Some endpoints support XML
- **Text**: Plain text output

Specify format using:
1. `Content-Type` header
2. URL parameter: `content-type=text/x-fasta`
3. File extension: `/sequence/id/ENSG00000139618.fasta`

## Common Parameters

Many endpoints share these parameters:

- **expand**: Include child objects (transcripts, proteins)
- **format**: Output format (json, xml, fasta)
- **db_type**: Database type (core, otherfeatures, variation)
- **object_type**: Type of object to return
- **species**: Species name (can be common or scientific)

## Error Codes

- **200**: Success
- **400**: Bad request (invalid parameters)
- **404**: Not found (ID doesn't exist)
- **429**: Rate limit exceeded
- **500**: Internal server error

## Best Practices

1. **Use batch endpoints** for multiple queries (more efficient)
2. **Cache responses** to minimize API calls
3. **Check rate limit headers** in responses
4. **Handle 429 errors** by respecting `Retry-After` header
5. **Use appropriate content types** for sequence data
6. **Specify assembly** when querying older genome versions
7. **Enable expand parameter** when you need full object details
