---
title: "Bioservices"
description: "Unified Python interface to 40+ bioinformatics services. Use when querying multiple databases (UniProt, KEGG, ChEMBL, Reactome) in a single workflow with consistent API. Best for cross-database analysis, ID mapping across services. For quick singl..."
category: "research"
source: "community"
author: "Community"
tags: ["bioservices"]
date: 2026-03-20
---

# BioServices

## Overview

BioServices is a Python package providing programmatic access to approximately 40 bioinformatics web services and databases. Retrieve biological data, perform cross-database queries, map identifiers, analyze sequences, and integrate multiple biological resources in Python workflows. The package handles both REST and SOAP/WSDL protocols transparently.

## When to Use This Skill

This skill should be used when:
- Retrieving protein sequences, annotations, or structures from UniProt, PDB, Pfam
- Analyzing metabolic pathways and gene functions via KEGG or Reactome
- Searching compound databases (ChEBI, ChEMBL, PubChem) for chemical information
- Converting identifiers between different biological databases (KEGG↔UniProt, compound IDs)
- Running sequence similarity searches (BLAST, MUSCLE alignment)
- Querying gene ontology terms (QuickGO, GO annotations)
- Accessing protein-protein interaction data (PSICQUIC, IntactComplex)
- Mining genomic data (BioMart, ArrayExpress, ENA)
- Integrating data from multiple bioinformatics resources in a single workflow

## Core Capabilities

### 1. Protein Analysis

Retrieve protein information, sequences, and functional annotations:

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# Search for protein by name
results = u.search("ZAP70_HUMAN", frmt="tab", columns="id,genes,organism")

# Retrieve FASTA sequence
sequence = u.retrieve("P43403", "fasta")

# Map identifiers between databases
kegg_ids = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
```

**Key methods:**
- `search()`: Query UniProt with flexible search terms
- `retrieve()`: Get protein entries in various formats (FASTA, XML, tab)
- `mapping()`: Convert identifiers between databases

Reference: `references/services_reference.md` for complete UniProt API details.

### 2. Pathway Discovery and Analysis

Access KEGG pathway information for genes and organisms:

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"  # Set to human

# Search for organisms
k.lookfor_organism("droso")  # Find Drosophila species

# Find pathways by name
k.lookfor_pathway("B cell")  # Returns matching pathway IDs

# Get pathways containing specific genes
pathways = k.get_pathway_by_gene("7535", "hsa")  # ZAP70 gene

# Retrieve and parse pathway data
data = k.get("hsa04660")
parsed = k.parse(data)

# Extract pathway interactions
interactions = k.parse_kgml_pathway("hsa04660")
relations = interactions['relations']  # Protein-protein interactions

# Convert to Simple Interaction Format
sif_data = k.pathway2sif("hsa04660")
```

**Key methods:**
- `lookfor_organism()`, `lookfor_pathway()`: Search by name
- `get_pathway_by_gene()`: Find pathways containing genes
- `parse_kgml_pathway()`: Extract structured pathway data
- `pathway2sif()`: Get protein interaction networks

Reference: `references/workflow_patterns.md` for complete pathway analysis workflows.

### 3. Compound Database Searches

Search and cross-reference compounds across multiple databases:

```python
from bioservices import KEGG, UniChem

k = KEGG()

# Search compounds by name
results = k.find("compound", "Geldanamycin")  # Returns cpd:C11222

# Get compound information with database links
compound_info = k.get("cpd:C11222")  # Includes ChEBI links

# Cross-reference KEGG → ChEMBL using UniChem
u = UniChem()
chembl_id = u.get_compound_id_from_kegg("C11222")  # Returns CHEMBL278315
```

**Common workflow:**
1. Search compound by name in KEGG
2. Extract KEGG compound ID
3. Use UniChem for KEGG → ChEMBL mapping
4. ChEBI IDs are often provided in KEGG entries

Reference: `references/identifier_mapping.md` for complete cross-database mapping guide.

### 4. Sequence Analysis

Run BLAST searches and sequence alignments:

```python
from bioservices import NCBIblast

s = NCBIblast(verbose=False)

# Run BLASTP against UniProtKB
jobid = s.run(
    program="blastp",
    sequence=protein_sequence,
    stype="protein",
    database="uniprotkb",
    email="your.email@example.com"  # Required by NCBI
)

# Check job status and retrieve results
s.getStatus(jobid)
results = s.getResult(jobid, "out")
```

**Note:** BLAST jobs are asynchronous. Check status before retrieving results.

### 5. Identifier Mapping

Convert identifiers between different biological databases:

```python
from bioservices import UniProt, KEGG

# UniProt mapping (many database pairs supported)
u = UniProt()
results = u.mapping(
    fr="UniProtKB_AC-ID",  # Source database
    to="KEGG",              # Target database
    query="P43403"          # Identifier(s) to convert
)

# KEGG gene ID → UniProt
kegg_to_uniprot = u.mapping(fr="KEGG", to="UniProtKB_AC-ID", query="hsa:7535")

# For compounds, use UniChem
from bioservices import UniChem
u = UniChem()
chembl_from_kegg = u.get_compound_id_from_kegg("C11222")
```

**Supported mappings (UniProt):**
- UniProtKB ↔ KEGG
- UniProtKB ↔ Ensembl
- UniProtKB ↔ PDB
- UniProtKB ↔ RefSeq
- And many more (see `references/identifier_mapping.md`)

### 6. Gene Ontology Queries

Access GO terms and annotations:

```python
from bioservices import QuickGO

g = QuickGO(verbose=False)

# Retrieve GO term information
term_info = g.Term("GO:0003824", frmt="obo")

# Search annotations
annotations = g.Annotation(protein="P43403", format="tsv")
```

### 7. Protein-Protein Interactions

Query interaction databases via PSICQUIC:

```python
from bioservices import PSICQUIC

s = PSICQUIC(verbose=False)

# Query specific database (e.g., MINT)
interactions = s.query("mint", "ZAP70 AND species:9606")

# List available interaction databases
databases = s.activeDBs
```

**Available databases:** MINT, IntAct, BioGRID, DIP, and 30+ others.

## Multi-Service Integration Workflows

BioServices excels at combining multiple services for comprehensive analysis. Common integration patterns:

### Complete Protein Analysis Pipeline

Execute a full protein characterization workflow:

```bash
python scripts/protein_analysis_workflow.py ZAP70_HUMAN your.email@example.com
```

This script demonstrates:
1. UniProt search for protein entry
2. FASTA sequence retrieval
3. BLAST similarity search
4. KEGG pathway discovery
5. PSICQUIC interaction mapping

### Pathway Network Analysis

Analyze all pathways for an organism:

```bash
python scripts/pathway_analysis.py hsa output_directory/
```

Extracts and analyzes:
- All pathway IDs for organism
- Protein-protein interactions per pathway
- Interaction type distributions
- Exports to CSV/SIF formats

### Cross-Database Compound Search

Map compound identifiers across databases:

```bash
python scripts/compound_cross_reference.py Geldanamycin
```

Retrieves:
- KEGG compound ID
- ChEBI identifier
- ChEMBL identifier
- Basic compound properties

### Batch Identifier Conversion

Convert multiple identifiers at once:

```bash
python scripts/batch_id_converter.py input_ids.txt --from UniProtKB_AC-ID --to KEGG
```

## Best Practices

### Output Format Handling

Different services return data in various formats:
- **XML**: Parse using BeautifulSoup (most SOAP services)
- **Tab-separated (TSV)**: Pandas DataFrames for tabular data
- **Dictionary/JSON**: Direct Python manipulation
- **FASTA**: BioPython integration for sequence analysis

### Rate Limiting and Verbosity

Control API request behavior:

```python
from bioservices import KEGG

k = KEGG(verbose=False)  # Suppress HTTP request details
k.TIMEOUT = 30  # Adjust timeout for slow connections
```

### Error Handling

Wrap service calls in try-except blocks:

```python
try:
    results = u.search("ambiguous_query")
    if results:
        # Process results
        pass
except Exception as e:
    print(f"Search failed: {e}")
```

### Organism Codes

Use standard organism abbreviations:
- `hsa`: Homo sapiens (human)
- `mmu`: Mus musculus (mouse)
- `dme`: Drosophila melanogaster
- `sce`: Saccharomyces cerevisiae (yeast)

List all organisms: `k.list("organism")` or `k.organismIds`

### Integration with Other Tools

BioServices works well with:
- **BioPython**: Sequence analysis on retrieved FASTA data
- **Pandas**: Tabular data manipulation
- **PyMOL**: 3D structure visualization (retrieve PDB IDs)
- **NetworkX**: Network analysis of pathway interactions
- **Galaxy**: Custom tool wrappers for workflow platforms

## Resources

### scripts/

Executable Python scripts demonstrating complete workflows:

- `protein_analysis_workflow.py`: End-to-end protein characterization
- `pathway_analysis.py`: KEGG pathway discovery and network extraction
- `compound_cross_reference.py`: Multi-database compound searching
- `batch_id_converter.py`: Bulk identifier mapping utility

Scripts can be executed directly or adapted for specific use cases.

### references/

Detailed documentation loaded as needed:

- `services_reference.md`: Comprehensive list of all 40+ services with methods
- `workflow_patterns.md`: Detailed multi-step analysis workflows
- `identifier_mapping.md`: Complete guide to cross-database ID conversion

Load references when working with specific services or complex integration tasks.

## Installation

```bash
uv pip install bioservices
```

Dependencies are automatically managed. Package is tested on Python 3.9-3.12.

## Additional Information

For detailed API documentation and advanced features, refer to:
- Official documentation: https://bioservices.readthedocs.io/
- Source code: https://github.com/cokelaer/bioservices
- Service-specific references in `references/services_reference.md`

---

## Reference: Identifier_Mapping

# BioServices: Identifier Mapping Guide

This document provides comprehensive information about converting identifiers between different biological databases using BioServices.

## Table of Contents

1. [Overview](#overview)
2. [UniProt Mapping Service](#uniprot-mapping-service)
3. [UniChem Compound Mapping](#unichem-compound-mapping)
4. [KEGG Identifier Conversions](#kegg-identifier-conversions)
5. [Common Mapping Patterns](#common-mapping-patterns)
6. [Troubleshooting](#troubleshooting)

---

## Overview

Biological databases use different identifier systems. Cross-referencing requires mapping between these systems. BioServices provides multiple approaches:

1. **UniProt Mapping**: Comprehensive protein/gene ID conversion
2. **UniChem**: Chemical compound ID mapping
3. **KEGG**: Built-in cross-references in entries
4. **PICR**: Protein identifier cross-reference service

---

## UniProt Mapping Service

The UniProt mapping service is the most comprehensive tool for protein and gene identifier conversion.

### Basic Usage

```python
from bioservices import UniProt

u = UniProt()

# Map single ID
result = u.mapping(
    fr="UniProtKB_AC-ID",    # Source database
    to="KEGG",                # Target database
    query="P43403"            # Identifier to convert
)

print(result)
# Output: {'P43403': ['hsa:7535']}
```

### Batch Mapping

```python
# Map multiple IDs (comma-separated)
ids = ["P43403", "P04637", "P53779"]
result = u.mapping(
    fr="UniProtKB_AC-ID",
    to="KEGG",
    query=",".join(ids)
)

for uniprot_id, kegg_ids in result.items():
    print(f"{uniprot_id} → {kegg_ids}")
```

### Supported Database Pairs

UniProt supports mapping between 100+ database pairs. Key ones include:

#### Protein/Gene Databases

| Source Format | Code | Target Format | Code |
|---------------|------|---------------|------|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | KEGG | `KEGG` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | Ensembl | `Ensembl` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | Ensembl Protein | `Ensembl_Protein` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | Ensembl Transcript | `Ensembl_Transcript` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | RefSeq Protein | `RefSeq_Protein` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | RefSeq Nucleotide | `RefSeq_Nucleotide` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | GeneID (Entrez) | `GeneID` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | HGNC | `HGNC` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | MGI | `MGI` |
| KEGG | `KEGG` | UniProtKB | `UniProtKB` |
| Ensembl | `Ensembl` | UniProtKB | `UniProtKB` |
| GeneID | `GeneID` | UniProtKB | `UniProtKB` |

#### Structural Databases

| Source | Code | Target | Code |
|--------|------|--------|------|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | PDB | `PDB` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | Pfam | `Pfam` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | InterPro | `InterPro` |
| PDB | `PDB` | UniProtKB | `UniProtKB` |

#### Expression & Proteomics

| Source | Code | Target | Code |
|--------|------|--------|------|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | PRIDE | `PRIDE` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | ProteomicsDB | `ProteomicsDB` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | PaxDb | `PaxDb` |

#### Organism-Specific

| Source | Code | Target | Code |
|--------|------|--------|------|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | FlyBase | `FlyBase` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | WormBase | `WormBase` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | SGD | `SGD` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | ZFIN | `ZFIN` |

#### Other Useful Mappings

| Source | Code | Target | Code |
|--------|------|--------|------|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | GO | `GO` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | Reactome | `Reactome` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | STRING | `STRING` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | BioGRID | `BioGRID` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | OMA | `OMA` |

### Complete List of Database Codes

To get the complete, up-to-date list:

```python
from bioservices import UniProt

u = UniProt()

# This information is in the UniProt REST API documentation
# Common patterns:
# - Source databases typically end in source database name
# - UniProtKB uses "UniProtKB_AC-ID" or "UniProtKB"
# - Most other databases use their standard abbreviation
```

### Common Database Codes Reference

**Gene/Protein Identifiers:**
- `UniProtKB_AC-ID`: UniProt accession/ID
- `UniProtKB`: UniProt accession
- `KEGG`: KEGG gene IDs (e.g., hsa:7535)
- `GeneID`: NCBI Gene (Entrez) IDs
- `Ensembl`: Ensembl gene IDs
- `Ensembl_Protein`: Ensembl protein IDs
- `Ensembl_Transcript`: Ensembl transcript IDs
- `RefSeq_Protein`: RefSeq protein IDs (NP_)
- `RefSeq_Nucleotide`: RefSeq nucleotide IDs (NM_)

**Gene Nomenclature:**
- `HGNC`: Human Gene Nomenclature Committee
- `MGI`: Mouse Genome Informatics
- `RGD`: Rat Genome Database
- `SGD`: Saccharomyces Genome Database
- `FlyBase`: Drosophila database
- `WormBase`: C. elegans database
- `ZFIN`: Zebrafish database

**Structure:**
- `PDB`: Protein Data Bank
- `Pfam`: Protein families
- `InterPro`: Protein domains
- `SUPFAM`: Superfamily
- `PROSITE`: Protein motifs

**Pathways & Networks:**
- `Reactome`: Reactome pathways
- `BioCyc`: BioCyc pathways
- `PathwayCommons`: Pathway Commons
- `STRING`: Protein-protein networks
- `BioGRID`: Interaction database

### Mapping Examples

#### UniProt → KEGG

```python
from bioservices import UniProt

u = UniProt()

# Single mapping
result = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
print(result)  # {'P43403': ['hsa:7535']}
```

#### KEGG → UniProt

```python
# Reverse mapping
result = u.mapping(fr="KEGG", to="UniProtKB", query="hsa:7535")
print(result)  # {'hsa:7535': ['P43403']}
```

#### UniProt → Ensembl

```python
# To Ensembl gene IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="Ensembl", query="P43403")
print(result)  # {'P43403': ['ENSG00000115085']}

# To Ensembl protein IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="Ensembl_Protein", query="P43403")
print(result)  # {'P43403': ['ENSP00000381359']}
```

#### UniProt → PDB

```python
# Find 3D structures
result = u.mapping(fr="UniProtKB_AC-ID", to="PDB", query="P04637")
print(result)  # {'P04637': ['1A1U', '1AIE', '1C26', ...]}
```

#### UniProt → RefSeq

```python
# Get RefSeq protein IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="RefSeq_Protein", query="P43403")
print(result)  # {'P43403': ['NP_001070.2']}
```

#### Gene Name → UniProt (via search, then mapping)

```python
# First search for gene
search_result = u.search("gene:ZAP70 AND organism:9606", frmt="tab", columns="id")
lines = search_result.strip().split("\n")
if len(lines) > 1:
    uniprot_id = lines[1].split("\t")[0]

    # Then map to other databases
    kegg_id = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
    print(kegg_id)
```

---

## UniChem Compound Mapping

UniChem specializes in mapping chemical compound identifiers across databases.

### Source Database IDs

| Source ID | Database |
|-----------|----------|
| 1 | ChEMBL |
| 2 | DrugBank |
| 3 | PDB |
| 4 | IUPHAR/BPS Guide to Pharmacology |
| 5 | PubChem |
| 6 | KEGG |
| 7 | ChEBI |
| 8 | NIH Clinical Collection |
| 14 | FDA/SRS |
| 22 | PubChem |

### Basic Usage

```python
from bioservices import UniChem

u = UniChem()

# Get ChEMBL ID from KEGG compound ID
chembl_id = u.get_compound_id_from_kegg("C11222")
print(chembl_id)  # CHEMBL278315
```

### All Compound IDs

```python
# Get all identifiers for a compound
# src_compound_id: compound ID, src_id: source database ID
all_ids = u.get_all_compound_ids("CHEMBL278315", src_id=1)  # 1 = ChEMBL

for mapping in all_ids:
    src_name = mapping['src_name']
    src_compound_id = mapping['src_compound_id']
    print(f"{src_name}: {src_compound_id}")
```

### Specific Database Conversion

```python
# Convert between specific databases
# from_src_id=6 (KEGG), to_src_id=1 (ChEMBL)
result = u.get_src_compound_ids("C11222", from_src_id=6, to_src_id=1)
print(result)
```

### Common Compound Mappings

#### KEGG → ChEMBL

```python
u = UniChem()
chembl_id = u.get_compound_id_from_kegg("C00031")  # D-Glucose
print(f"ChEMBL: {chembl_id}")
```

#### ChEMBL → PubChem

```python
result = u.get_src_compound_ids("CHEMBL278315", from_src_id=1, to_src_id=22)
if result:
    pubchem_id = result[0]['src_compound_id']
    print(f"PubChem: {pubchem_id}")
```

#### ChEBI → DrugBank

```python
result = u.get_src_compound_ids("5292", from_src_id=7, to_src_id=2)
if result:
    drugbank_id = result[0]['src_compound_id']
    print(f"DrugBank: {drugbank_id}")
```

---

## KEGG Identifier Conversions

KEGG entries contain cross-references that can be extracted by parsing.

### Extract Database Links from KEGG Entry

```python
from bioservices import KEGG

k = KEGG()

# Get compound entry
entry = k.get("cpd:C11222")

# Parse for specific database
chebi_id = None
uniprot_ids = []

for line in entry.split("\n"):
    if "ChEBI:" in line:
        # Extract ChEBI ID
        parts = line.split("ChEBI:")
        if len(parts) > 1:
            chebi_id = parts[1].strip().split()[0]

# For genes/proteins
gene_entry = k.get("hsa:7535")
for line in gene_entry.split("\n"):
    if line.startswith("            "):  # Database links section
        if "UniProt:" in line:
            parts = line.split("UniProt:")
            if len(parts) > 1:
                uniprot_id = parts[1].strip()
                uniprot_ids.append(uniprot_id)
```

### KEGG Gene ID Components

KEGG gene IDs have format `organism:gene_id`:

```python
kegg_id = "hsa:7535"
organism, gene_id = kegg_id.split(":")

print(f"Organism: {organism}")  # hsa (human)
print(f"Gene ID: {gene_id}")    # 7535
```

### KEGG Pathway to Genes

```python
k = KEGG()

# Get pathway entry
pathway = k.get("path:hsa04660")

# Parse for gene list
genes = []
in_gene_section = False

for line in pathway.split("\n"):
    if line.startswith("GENE"):
        in_gene_section = True

    if in_gene_section:
        if line.startswith(" " * 12):  # Gene line
            parts = line.strip().split()
            if parts:
                gene_id = parts[0]
                genes.append(f"hsa:{gene_id}")
        elif not line.startswith(" "):
            break

print(f"Found {len(genes)} genes")
```

---

## Common Mapping Patterns

### Pattern 1: Gene Symbol → Multiple Database IDs

```python
from bioservices import UniProt

def gene_symbol_to_ids(gene_symbol, organism="9606"):
    """Convert gene symbol to multiple database IDs."""
    u = UniProt()

    # Search for gene
    query = f"gene:{gene_symbol} AND organism:{organism}"
    result = u.search(query, frmt="tab", columns="id")

    lines = result.strip().split("\n")
    if len(lines) < 2:
        return None

    uniprot_id = lines[1].split("\t")[0]

    # Map to multiple databases
    ids = {
        'uniprot': uniprot_id,
        'kegg': u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id),
        'ensembl': u.mapping(fr="UniProtKB_AC-ID", to="Ensembl", query=uniprot_id),
        'refseq': u.mapping(fr="UniProtKB_AC-ID", to="RefSeq_Protein", query=uniprot_id),
        'pdb': u.mapping(fr="UniProtKB_AC-ID", to="PDB", query=uniprot_id)
    }

    return ids

# Usage
ids = gene_symbol_to_ids("ZAP70")
print(ids)
```

### Pattern 2: Compound Name → All Database IDs

```python
from bioservices import KEGG, UniChem, ChEBI

def compound_name_to_ids(compound_name):
    """Search compound and get all database IDs."""
    k = KEGG()

    # Search KEGG
    results = k.find("compound", compound_name)
    if not results:
        return None

    # Extract KEGG ID
    kegg_id = results.strip().split("\n")[0].split("\t")[0].replace("cpd:", "")

    # Get KEGG entry for ChEBI
    entry = k.get(f"cpd:{kegg_id}")
    chebi_id = None
    for line in entry.split("\n"):
        if "ChEBI:" in line:
            parts = line.split("ChEBI:")
            if len(parts) > 1:
                chebi_id = parts[1].strip().split()[0]
                break

    # Get ChEMBL from UniChem
    u = UniChem()
    try:
        chembl_id = u.get_compound_id_from_kegg(kegg_id)
    except:
        chembl_id = None

    return {
        'kegg': kegg_id,
        'chebi': chebi_id,
        'chembl': chembl_id
    }

# Usage
ids = compound_name_to_ids("Geldanamycin")
print(ids)
```

### Pattern 3: Batch ID Conversion with Error Handling

```python
from bioservices import UniProt

def safe_batch_mapping(ids, from_db, to_db, chunk_size=100):
    """Safely map IDs with error handling and chunking."""
    u = UniProt()
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        query = ",".join(chunk)

        try:
            results = u.mapping(fr=from_db, to=to_db, query=query)
            all_results.update(results)
            print(f"✓ Processed {min(i+chunk_size, len(ids))}/{len(ids)}")

        except Exception as e:
            print(f"✗ Error at chunk {i}: {e}")

            # Try individual IDs in failed chunk
            for single_id in chunk:
                try:
                    result = u.mapping(fr=from_db, to=to_db, query=single_id)
                    all_results.update(result)
                except:
                    all_results[single_id] = None

    return all_results

# Usage
uniprot_ids = ["P43403", "P04637", "P53779", "INVALID123"]
mapping = safe_batch_mapping(uniprot_ids, "UniProtKB_AC-ID", "KEGG")
```

### Pattern 4: Multi-Hop Mapping

Sometimes you need to map through intermediate databases:

```python
from bioservices import UniProt

def multi_hop_mapping(gene_symbol, organism="9606"):
    """Gene symbol → UniProt → KEGG → Pathways."""
    u = UniProt()
    k = KEGG()

    # Step 1: Gene symbol → UniProt
    query = f"gene:{gene_symbol} AND organism:{organism}"
    result = u.search(query, frmt="tab", columns="id")

    lines = result.strip().split("\n")
    if len(lines) < 2:
        return None

    uniprot_id = lines[1].split("\t")[0]

    # Step 2: UniProt → KEGG
    kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
    if not kegg_mapping or uniprot_id not in kegg_mapping:
        return None

    kegg_id = kegg_mapping[uniprot_id][0]

    # Step 3: KEGG → Pathways
    organism_code, gene_id = kegg_id.split(":")
    pathways = k.get_pathway_by_gene(gene_id, organism_code)

    return {
        'gene': gene_symbol,
        'uniprot': uniprot_id,
        'kegg': kegg_id,
        'pathways': pathways
    }

# Usage
result = multi_hop_mapping("TP53")
print(result)
```

---

## Troubleshooting

### Issue 1: No Mapping Found

**Symptom:** Mapping returns empty or None

**Solutions:**
1. Verify source ID exists in source database
2. Check database code spelling
3. Try reverse mapping
4. Some IDs may not have mappings in all databases

```python
result = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")

if not result or 'P43403' not in result:
    print("No mapping found. Try:")
    print("1. Verify ID exists: u.search('P43403')")
    print("2. Check if protein has KEGG annotation")
```

### Issue 2: Too Many IDs in Batch

**Symptom:** Batch mapping fails or times out

**Solution:** Split into smaller chunks

```python
def chunked_mapping(ids, from_db, to_db, chunk_size=50):
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        result = u.mapping(fr=from_db, to=to_db, query=",".join(chunk))
        all_results.update(result)

    return all_results
```

### Issue 3: Multiple Target IDs

**Symptom:** One source ID maps to multiple target IDs

**Solution:** Handle as list

```python
result = u.mapping(fr="UniProtKB_AC-ID", to="PDB", query="P04637")
# Result: {'P04637': ['1A1U', '1AIE', '1C26', ...]}

pdb_ids = result['P04637']
print(f"Found {len(pdb_ids)} PDB structures")

for pdb_id in pdb_ids:
    print(f"  {pdb_id}")
```

### Issue 4: Organism Ambiguity

**Symptom:** Gene symbol maps to multiple organisms

**Solution:** Always specify organism in searches

```python
# Bad: Ambiguous
result = u.search("gene:TP53")  # Many organisms have TP53

# Good: Specific
result = u.search("gene:TP53 AND organism:9606")  # Human only
```

### Issue 5: Deprecated IDs

**Symptom:** Old database IDs don't map

**Solution:** Update to current IDs first

```python
# Check if ID is current
entry = u.retrieve("P43403", frmt="txt")

# Look for secondary accessions
for line in entry.split("\n"):
    if line.startswith("AC"):
        print(line)  # Shows primary and secondary accessions
```

---

## Best Practices

1. **Always validate inputs** before batch processing
2. **Handle None/empty results** gracefully
3. **Use chunking** for large ID lists (50-100 per chunk)
4. **Cache results** for repeated queries
5. **Specify organism** when possible to avoid ambiguity
6. **Log failures** in batch processing for later retry
7. **Add delays** between large batches to respect API limits

```python
import time

def polite_batch_mapping(ids, from_db, to_db):
    """Batch mapping with rate limiting."""
    results = {}

    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        result = u.mapping(fr=from_db, to=to_db, query=",".join(chunk))
        results.update(result)

        time.sleep(0.5)  # Be nice to the API

    return results
```

---

For complete working examples, see:
- `scripts/batch_id_converter.py`: Command-line batch conversion tool
- `workflow_patterns.md`: Integration into larger workflows

---

## Reference: Services_Reference

# BioServices: Complete Services Reference

This document provides a comprehensive reference for all major services available in BioServices, including key methods, parameters, and use cases.

## Protein & Gene Resources

### UniProt

Protein sequence and functional information database.

**Initialization:**
```python
from bioservices import UniProt
u = UniProt(verbose=False)
```

**Key Methods:**

- `search(query, frmt="tab", columns=None, limit=None, sort=None, compress=False, include=False, **kwargs)`
  - Search UniProt with flexible query syntax
  - `frmt`: "tab", "fasta", "xml", "rdf", "gff", "txt"
  - `columns`: Comma-separated list (e.g., "id,genes,organism,length")
  - Returns: String in requested format

- `retrieve(uniprot_id, frmt="txt")`
  - Retrieve specific UniProt entry
  - `frmt`: "txt", "fasta", "xml", "rdf", "gff"
  - Returns: Entry data in requested format

- `mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")`
  - Convert identifiers between databases
  - `fr`/`to`: Database identifiers (see identifier_mapping.md)
  - `query`: Single ID or comma-separated list
  - Returns: Dictionary mapping input to output IDs

- `searchUniProtId(pattern, columns="entry name,length,organism", limit=100)`
  - Convenience method for ID-based searches
  - Returns: Tab-separated values

**Common columns:** id, entry name, genes, organism, protein names, length, sequence, go-id, ec, pathway, interactor

**Use cases:**
- Protein sequence retrieval for BLAST
- Functional annotation lookup
- Cross-database identifier mapping
- Batch protein information retrieval

---

### KEGG (Kyoto Encyclopedia of Genes and Genomes)

Metabolic pathways, genes, and organisms database.

**Initialization:**
```python
from bioservices import KEGG
k = KEGG()
k.organism = "hsa"  # Set default organism
```

**Key Methods:**

- `list(database)`
  - List entries in KEGG database
  - `database`: "organism", "pathway", "module", "disease", "drug", "compound"
  - Returns: Multi-line string with entries

- `find(database, query)`
  - Search database by keywords
  - Returns: List of matching entries with IDs

- `get(entry_id)`
  - Retrieve entry by ID
  - Supports genes, pathways, compounds, etc.
  - Returns: Raw entry text

- `parse(data)`
  - Parse KEGG entry into dictionary
  - Returns: Dict with structured data

- `lookfor_organism(name)`
  - Search organisms by name pattern
  - Returns: List of matching organism codes

- `lookfor_pathway(name)`
  - Search pathways by name
  - Returns: List of pathway IDs

- `get_pathway_by_gene(gene_id, organism)`
  - Find pathways containing gene
  - Returns: List of pathway IDs

- `parse_kgml_pathway(pathway_id)`
  - Parse pathway KGML for interactions
  - Returns: Dict with "entries" and "relations"

- `pathway2sif(pathway_id)`
  - Extract Simple Interaction Format data
  - Filters for activation/inhibition
  - Returns: List of interaction tuples

**Organism codes:**
- hsa: Homo sapiens
- mmu: Mus musculus
- dme: Drosophila melanogaster
- sce: Saccharomyces cerevisiae
- eco: Escherichia coli

**Use cases:**
- Pathway analysis and visualization
- Gene function annotation
- Metabolic network reconstruction
- Protein-protein interaction extraction

---

### HGNC (Human Gene Nomenclature Committee)

Official human gene naming authority.

**Initialization:**
```python
from bioservices import HGNC
h = HGNC()
```

**Key Methods:**
- `search(query)`: Search gene symbols/names
- `fetch(format, query)`: Retrieve gene information

**Use cases:**
- Standardizing human gene names
- Looking up official gene symbols

---

### MyGeneInfo

Gene annotation and query service.

**Initialization:**
```python
from bioservices import MyGeneInfo
m = MyGeneInfo()
```

**Key Methods:**
- `querymany(ids, scopes, fields, species)`: Batch gene queries
- `getgene(geneid)`: Get gene annotation

**Use cases:**
- Batch gene annotation retrieval
- Gene ID conversion

---

## Chemical Compound Resources

### ChEBI (Chemical Entities of Biological Interest)

Dictionary of molecular entities.

**Initialization:**
```python
from bioservices import ChEBI
c = ChEBI()
```

**Key Methods:**
- `getCompleteEntity(chebi_id)`: Full compound information
- `getLiteEntity(chebi_id)`: Basic information
- `getCompleteEntityByList(chebi_ids)`: Batch retrieval

**Use cases:**
- Small molecule information
- Chemical structure data
- Compound property lookup

---

### ChEMBL

Bioactive drug-like compound database.

**Initialization:**
```python
from bioservices import ChEMBL
c = ChEMBL()
```

**Key Methods:**
- `get_molecule_form(chembl_id)`: Compound details
- `get_target(chembl_id)`: Target information
- `get_similarity(chembl_id)`: Get similar compounds for given 
- `get_assays()`: Bioassay data

**Use cases:**
- Drug discovery data
- Find similar compounds  
- Bioactivity information
- Target-compound relationships

---

### UniChem

Chemical identifier mapping service.

**Initialization:**
```python
from bioservices import UniChem
u = UniChem()
```

**Key Methods:**
- `get_compound_id_from_kegg(kegg_id)`: KEGG → ChEMBL
- `get_all_compound_ids(src_compound_id, src_id)`: Get all IDs
- `get_src_compound_ids(src_compound_id, from_src_id, to_src_id)`: Convert IDs

**Source IDs:**
- 1: ChEMBL
- 2: DrugBank
- 3: PDB
- 6: KEGG
- 7: ChEBI
- 22: PubChem

**Use cases:**
- Cross-database compound ID mapping
- Linking chemical databases

---

### PubChem

Chemical compound database from NIH.

**Initialization:**
```python
from bioservices import PubChem
p = PubChem()
```

**Key Methods:**
- `get_compounds(identifier, namespace)`: Retrieve compounds
- `get_properties(properties, identifier, namespace)`: Get properties

**Use cases:**
- Chemical structure retrieval
- Compound property information

---

## Sequence Analysis Tools

### NCBIblast

Sequence similarity searching.

**Initialization:**
```python
from bioservices import NCBIblast
s = NCBIblast(verbose=False)
```

**Key Methods:**
- `run(program, sequence, stype, database, email, **params)`
  - Submit BLAST job
  - `program`: "blastp", "blastn", "blastx", "tblastn", "tblastx"
  - `stype`: "protein" or "dna"
  - `database`: "uniprotkb", "pdb", "refseq_protein", etc.
  - `email`: Required by NCBI
  - Returns: Job ID

- `getStatus(jobid)`
  - Check job status
  - Returns: "RUNNING", "FINISHED", "ERROR"

- `getResult(jobid, result_type)`
  - Retrieve results
  - `result_type`: "out" (default), "ids", "xml"

**Important:** BLAST jobs are asynchronous. Always check status before retrieving results.

**Use cases:**
- Protein homology searches
- Sequence similarity analysis
- Functional annotation by homology

---

## Pathway & Interaction Resources

### Reactome

Pathway database.

**Initialization:**
```python
from bioservices import Reactome
r = Reactome()
```

**Key Methods:**
- `get_pathway_by_id(pathway_id)`: Pathway details
- `search_pathway(query)`: Search pathways

**Use cases:**
- Human pathway analysis
- Biological process annotation

---

### PSICQUIC

Protein interaction query service (federates 30+ databases).

**Initialization:**
```python
from bioservices import PSICQUIC
s = PSICQUIC()
```

**Key Methods:**
- `query(database, query_string)`
  - Query specific interaction database
  - Returns: PSI-MI TAB format

- `activeDBs`
  - Property listing available databases
  - Returns: List of database names

**Available databases:** MINT, IntAct, BioGRID, DIP, InnateDB, MatrixDB, MPIDB, UniProt, and 30+ more

**Query syntax:** Supports AND, OR, species filters
- Example: "ZAP70 AND species:9606"

**Use cases:**
- Protein-protein interaction discovery
- Network analysis
- Interactome mapping

---

### IntactComplex

Protein complex database.

**Initialization:**
```python
from bioservices import IntactComplex
i = IntactComplex()
```

**Key Methods:**
- `search(query)`: Search complexes
- `details(complex_ac)`: Complex details

**Use cases:**
- Protein complex composition
- Multi-protein assembly analysis

---

### OmniPath

Integrated signaling pathway database.

**Initialization:**
```python
from bioservices import OmniPath
o = OmniPath()
```

**Key Methods:**
- `interactions(datasets, organisms)`: Get interactions
- `ptms(datasets, organisms)`: Post-translational modifications

**Use cases:**
- Cell signaling analysis
- Regulatory network mapping

---

## Gene Ontology

### QuickGO

Gene Ontology annotation service.

**Initialization:**
```python
from bioservices import QuickGO
g = QuickGO()
```

**Key Methods:**
- `Term(go_id, frmt="obo")`
  - Retrieve GO term information
  - Returns: Term definition and metadata

- `Annotation(protein=None, goid=None, format="tsv")`
  - Get GO annotations
  - Returns: Annotations in requested format

**GO categories:**
- Biological Process (BP)
- Molecular Function (MF)
- Cellular Component (CC)

**Use cases:**
- Functional annotation
- Enrichment analysis
- GO term lookup

---

## Genomic Resources

### BioMart

Data mining tool for genomic data.

**Initialization:**
```python
from bioservices import BioMart
b = BioMart()
```

**Key Methods:**
- `datasets(dataset)`: List available datasets
- `attributes(dataset)`: List attributes
- `query(query_xml)`: Execute BioMart query

**Use cases:**
- Bulk genomic data retrieval
- Custom genome annotations
- SNP information

---

### ArrayExpress

Gene expression database.

**Initialization:**
```python
from bioservices import ArrayExpress
a = ArrayExpress()
```

**Key Methods:**
- `queryExperiments(keywords)`: Search experiments
- `retrieveExperiment(accession)`: Get experiment data

**Use cases:**
- Gene expression data
- Microarray analysis
- RNA-seq data retrieval

---

### ENA (European Nucleotide Archive)

Nucleotide sequence database.

**Initialization:**
```python
from bioservices import ENA
e = ENA()
```

**Key Methods:**
- `search_data(query)`: Search sequences
- `retrieve_data(accession)`: Retrieve sequences

**Use cases:**
- Nucleotide sequence retrieval
- Genome assembly access

---

## Structural Biology

### PDB (Protein Data Bank)

3D protein structure database.

**Initialization:**
```python
from bioservices import PDB
p = PDB()
```

**Key Methods:**
- `get_file(pdb_id, file_format)`: Download structure files
- `search(query)`: Search structures

**File formats:** pdb, cif, xml

**Use cases:**
- 3D structure retrieval
- Structure-based analysis
- PyMOL visualization

---

### Pfam

Protein family database.

**Initialization:**
```python
from bioservices import Pfam
p = Pfam()
```

**Key Methods:**
- `searchSequence(sequence)`: Find domains in sequence
- `getPfamEntry(pfam_id)`: Domain information

**Use cases:**
- Protein domain identification
- Family classification
- Functional motif discovery

---

## Specialized Resources

### BioModels

Systems biology model repository.

**Initialization:**
```python
from bioservices import BioModels
b = BioModels()
```

**Key Methods:**
- `get_model_by_id(model_id)`: Retrieve SBML model

**Use cases:**
- Systems biology modeling
- SBML model retrieval

---

### COG (Clusters of Orthologous Genes)

Orthologous gene classification.

**Initialization:**
```python
from bioservices import COG
c = COG()
```

**Use cases:**
- Orthology analysis
- Functional classification

---

### BiGG Models

Metabolic network models.

**Initialization:**
```python
from bioservices import BiGG
b = BiGG()
```

**Key Methods:**
- `list_models()`: Available models
- `get_model(model_id)`: Model details

**Use cases:**
- Metabolic network analysis
- Flux balance analysis

---

## General Patterns

### Error Handling

All services may throw exceptions. Wrap calls in try-except:

```python
try:
    result = service.method(params)
    if result:
        # Process result
        pass
except Exception as e:
    print(f"Error: {e}")
```

### Verbosity Control

Most services support `verbose` parameter:
```python
service = Service(verbose=False)  # Suppress HTTP logs
```

### Rate Limiting

Services have timeouts and rate limits:
```python
service.TIMEOUT = 30  # Adjust timeout
service.DELAY = 1     # Delay between requests (if supported)
```

### Output Formats

Common format parameters:
- `frmt`: "xml", "json", "tab", "txt", "fasta"
- `format`: Service-specific variants

### Caching

Some services cache results:
```python
service.CACHE = True  # Enable caching
service.clear_cache()  # Clear cache
```

## Additional Resources

For detailed API documentation:
- Official docs: https://bioservices.readthedocs.io/
- Individual service docs linked from main page
- Source code: https://github.com/cokelaer/bioservices

---

## Reference: Workflow_Patterns

# BioServices: Common Workflow Patterns

This document describes detailed multi-step workflows for common bioinformatics tasks using BioServices.

## Table of Contents

1. [Complete Protein Analysis Pipeline](#complete-protein-analysis-pipeline)
2. [Pathway Discovery and Network Analysis](#pathway-discovery-and-network-analysis)
3. [Compound Multi-Database Search](#compound-multi-database-search)
4. [Batch Identifier Conversion](#batch-identifier-conversion)
5. [Gene Functional Annotation](#gene-functional-annotation)
6. [Protein Interaction Network Construction](#protein-interaction-network-construction)
7. [Multi-Organism Comparative Analysis](#multi-organism-comparative-analysis)

---

## Complete Protein Analysis Pipeline

**Goal:** Given a protein name, retrieve sequence, find homologs, identify pathways, and discover interactions.

**Example:** Analyzing human ZAP70 protein

### Step 1: UniProt Search and Identifier Retrieval

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# Search for protein by name
query = "ZAP70_HUMAN"
results = u.search(query, frmt="tab", columns="id,genes,organism,length")

# Parse results
lines = results.strip().split("\n")
if len(lines) > 1:
    header = lines[0]
    data = lines[1].split("\t")
    uniprot_id = data[0]  # e.g., P43403
    gene_names = data[1]   # e.g., ZAP70

print(f"UniProt ID: {uniprot_id}")
print(f"Gene names: {gene_names}")
```

**Output:**
- UniProt accession: P43403
- Gene name: ZAP70

### Step 2: Sequence Retrieval

```python
# Retrieve FASTA sequence
sequence = u.retrieve(uniprot_id, frmt="fasta")
print(sequence)

# Extract just the sequence string (remove header)
seq_lines = sequence.split("\n")
sequence_only = "".join(seq_lines[1:])  # Skip FASTA header
```

**Output:** Complete protein sequence in FASTA format

### Step 3: BLAST Similarity Search

```python
from bioservices import NCBIblast
import time

s = NCBIblast(verbose=False)

# Submit BLAST job
jobid = s.run(
    program="blastp",
    sequence=sequence_only,
    stype="protein",
    database="uniprotkb",
    email="your.email@example.com"
)

print(f"BLAST Job ID: {jobid}")

# Wait for completion
while True:
    status = s.getStatus(jobid)
    print(f"Status: {status}")
    if status == "FINISHED":
        break
    elif status == "ERROR":
        print("BLAST job failed")
        break
    time.sleep(5)

# Retrieve results
if status == "FINISHED":
    blast_results = s.getResult(jobid, "out")
    print(blast_results[:500])  # Print first 500 characters
```

**Output:** BLAST alignment results showing similar proteins

### Step 4: KEGG Pathway Discovery

```python
from bioservices import KEGG

k = KEGG()

# Get KEGG gene ID from UniProt mapping
kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
print(f"KEGG mapping: {kegg_mapping}")

# Extract KEGG gene ID (e.g., hsa:7535)
if kegg_mapping:
    kegg_gene_id = kegg_mapping[uniprot_id][0] if uniprot_id in kegg_mapping else None

    if kegg_gene_id:
        # Find pathways containing this gene
        organism = kegg_gene_id.split(":")[0]  # e.g., "hsa"
        gene_id = kegg_gene_id.split(":")[1]   # e.g., "7535"

        pathways = k.get_pathway_by_gene(gene_id, organism)
        print(f"Found {len(pathways)} pathways:")

        # Get pathway names
        for pathway_id in pathways:
            pathway_info = k.get(pathway_id)
            # Parse NAME line
            for line in pathway_info.split("\n"):
                if line.startswith("NAME"):
                    pathway_name = line.replace("NAME", "").strip()
                    print(f"  {pathway_id}: {pathway_name}")
                    break
```

**Output:**
- path:hsa04064 - NF-kappa B signaling pathway
- path:hsa04650 - Natural killer cell mediated cytotoxicity
- path:hsa04660 - T cell receptor signaling pathway
- path:hsa04662 - B cell receptor signaling pathway

### Step 5: Protein-Protein Interactions

```python
from bioservices import PSICQUIC

p = PSICQUIC()

# Query MINT database for human (taxid:9606) interactions
query = f"ZAP70 AND species:9606"
interactions = p.query("mint", query)

# Parse PSI-MI TAB format results
if interactions:
    interaction_lines = interactions.strip().split("\n")
    print(f"Found {len(interaction_lines)} interactions")

    # Print first few interactions
    for line in interaction_lines[:5]:
        fields = line.split("\t")
        protein_a = fields[0]
        protein_b = fields[1]
        interaction_type = fields[11]
        print(f"  {protein_a} - {protein_b}: {interaction_type}")
```

**Output:** List of proteins that interact with ZAP70

### Step 6: Gene Ontology Annotation

```python
from bioservices import QuickGO

g = QuickGO()

# Get GO annotations for protein
annotations = g.Annotation(protein=uniprot_id, format="tsv")

if annotations:
    # Parse TSV results
    lines = annotations.strip().split("\n")
    print(f"Found {len(lines)-1} GO annotations")

    # Display first few annotations
    for line in lines[1:6]:  # Skip header
        fields = line.split("\t")
        go_id = fields[6]
        go_term = fields[7]
        go_aspect = fields[8]
        print(f"  {go_id}: {go_term} [{go_aspect}]")
```

**Output:** GO terms annotating ZAP70 function, process, and location

### Complete Pipeline Summary

**Inputs:** Protein name (e.g., "ZAP70_HUMAN")

**Outputs:**
1. UniProt accession and gene name
2. Protein sequence (FASTA)
3. Similar proteins (BLAST results)
4. Biological pathways (KEGG)
5. Interaction partners (PSICQUIC)
6. Functional annotations (GO terms)

**Script:** `scripts/protein_analysis_workflow.py` automates this entire pipeline.

---

## Pathway Discovery and Network Analysis

**Goal:** Analyze all pathways for an organism and extract protein interaction networks.

**Example:** Human (hsa) pathway analysis

### Step 1: Get All Pathways for Organism

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"

# Get all pathway IDs
pathway_ids = k.pathwayIds
print(f"Found {len(pathway_ids)} pathways for {k.organism}")

# Display first few
for pid in pathway_ids[:10]:
    print(f"  {pid}")
```

**Output:** List of ~300 human pathways

### Step 2: Parse Pathway for Interactions

```python
# Analyze specific pathway
pathway_id = "hsa04660"  # T cell receptor signaling

# Get KGML data
kgml_data = k.parse_kgml_pathway(pathway_id)

# Extract entries (genes/proteins)
entries = kgml_data['entries']
print(f"Pathway contains {len(entries)} entries")

# Extract relations (interactions)
relations = kgml_data['relations']
print(f"Found {len(relations)} relations")

# Analyze relation types
relation_types = {}
for rel in relations:
    rel_type = rel.get('name', 'unknown')
    relation_types[rel_type] = relation_types.get(rel_type, 0) + 1

print("\nRelation type distribution:")
for rel_type, count in sorted(relation_types.items()):
    print(f"  {rel_type}: {count}")
```

**Output:**
- Entry count (genes/proteins in pathway)
- Relation count (interactions)
- Distribution of interaction types (activation, inhibition, binding, etc.)

### Step 3: Extract Protein-Protein Interactions

```python
# Filter for specific interaction types
pprel_interactions = [
    rel for rel in relations
    if rel.get('link') == 'PPrel'  # Protein-protein relation
]

print(f"Found {len(pprel_interactions)} protein-protein interactions")

# Extract interaction details
for rel in pprel_interactions[:10]:
    entry1 = rel['entry1']
    entry2 = rel['entry2']
    interaction_type = rel.get('name', 'unknown')

    print(f"  {entry1} -> {entry2}: {interaction_type}")
```

**Output:** Directed protein-protein interactions with types

### Step 4: Convert to Network Format (SIF)

```python
# Get Simple Interaction Format (filters for key interactions)
sif_data = k.pathway2sif(pathway_id)

# SIF format: source, interaction_type, target
print("\nSimple Interaction Format:")
for interaction in sif_data[:10]:
    print(f"  {interaction}")
```

**Output:** Network edges suitable for Cytoscape or NetworkX

### Step 5: Batch Analysis of All Pathways

```python
import pandas as pd

# Analyze all pathways (this takes time!)
all_results = []

for pathway_id in pathway_ids[:50]:  # Limit for example
    try:
        kgml = k.parse_kgml_pathway(pathway_id)

        result = {
            'pathway_id': pathway_id,
            'num_entries': len(kgml.get('entries', [])),
            'num_relations': len(kgml.get('relations', []))
        }

        all_results.append(result)

    except Exception as e:
        print(f"Error parsing {pathway_id}: {e}")

# Create DataFrame
df = pd.DataFrame(all_results)
print(df.describe())

# Find largest pathways
print("\nLargest pathways:")
print(df.nlargest(10, 'num_entries')[['pathway_id', 'num_entries', 'num_relations']])
```

**Output:** Statistical summary of pathway sizes and interaction densities

**Script:** `scripts/pathway_analysis.py` implements this workflow with export options.

---

## Compound Multi-Database Search

**Goal:** Search for compound by name and retrieve identifiers across KEGG, ChEBI, and ChEMBL.

**Example:** Geldanamycin (antibiotic)

### Step 1: Search KEGG Compound Database

```python
from bioservices import KEGG

k = KEGG()

# Search by compound name
compound_name = "Geldanamycin"
results = k.find("compound", compound_name)

print(f"KEGG search results for '{compound_name}':")
print(results)

# Extract compound ID
if results:
    lines = results.strip().split("\n")
    if lines:
        kegg_id = lines[0].split("\t")[0]  # e.g., cpd:C11222
        kegg_id_clean = kegg_id.replace("cpd:", "")  # C11222
        print(f"\nKEGG Compound ID: {kegg_id_clean}")
```

**Output:** KEGG ID (e.g., C11222)

### Step 2: Get KEGG Entry with Database Links

```python
# Retrieve compound entry
compound_entry = k.get(kegg_id)

# Parse entry for database links
chebi_id = None
for line in compound_entry.split("\n"):
    if "ChEBI:" in line:
        # Extract ChEBI ID
        parts = line.split("ChEBI:")
        if len(parts) > 1:
            chebi_id = parts[1].strip().split()[0]
            print(f"ChEBI ID: {chebi_id}")
            break

# Display entry snippet
print("\nKEGG Entry (first 500 chars):")
print(compound_entry[:500])
```

**Output:** ChEBI ID (e.g., 5292) and compound information

### Step 3: Cross-Reference to ChEMBL via UniChem

```python
from bioservices import UniChem

u = UniChem()

# Convert KEGG → ChEMBL
try:
    chembl_id = u.get_compound_id_from_kegg(kegg_id_clean)
    print(f"ChEMBL ID: {chembl_id}")
except Exception as e:
    print(f"UniChem lookup failed: {e}")
    chembl_id = None
```

**Output:** ChEMBL ID (e.g., CHEMBL278315)

### Step 4: Retrieve Detailed Information

```python
# Get ChEBI information
if chebi_id:
    from bioservices import ChEBI
    c = ChEBI()

    try:
        chebi_entity = c.getCompleteEntity(f"CHEBI:{chebi_id}")
        print(f"\nChEBI Formula: {chebi_entity.Formulae}")
        print(f"ChEBI Name: {chebi_entity.chebiAsciiName}")
    except Exception as e:
        print(f"ChEBI lookup failed: {e}")

# Get ChEMBL information
if chembl_id:
    from bioservices import ChEMBL
    chembl = ChEMBL()

    try:
        chembl_compound = chembl.get_compound_by_chemblId(chembl_id)
        print(f"\nChEMBL Molecular Weight: {chembl_compound['molecule_properties']['full_mwt']}")
        print(f"ChEMBL SMILES: {chembl_compound['molecule_structures']['canonical_smiles']}")
    except Exception as e:
        print(f"ChEMBL lookup failed: {e}")
```

**Output:** Chemical properties from multiple databases

### Complete Compound Workflow Summary

**Input:** Compound name (e.g., "Geldanamycin")

**Output:**
- KEGG ID: C11222
- ChEBI ID: 5292
- ChEMBL ID: CHEMBL278315
- Chemical formula
- Molecular weight
- SMILES structure

**Script:** `scripts/compound_cross_reference.py` automates this workflow.

---

## Batch Identifier Conversion

**Goal:** Convert multiple identifiers between databases efficiently.

### Batch UniProt → KEGG Mapping

```python
from bioservices import UniProt

u = UniProt()

# List of UniProt IDs
uniprot_ids = ["P43403", "P04637", "P53779", "Q9Y6K9"]

# Batch mapping (comma-separated)
query_string = ",".join(uniprot_ids)
results = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=query_string)

print("UniProt → KEGG mapping:")
for uniprot_id, kegg_ids in results.items():
    print(f"  {uniprot_id} → {kegg_ids}")
```

**Output:** Dictionary mapping each UniProt ID to KEGG gene IDs

### Batch File Processing

```python
import csv

# Read identifiers from file
def read_ids_from_file(filename):
    with open(filename, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    return ids

# Process in chunks (API limits)
def batch_convert(ids, from_db, to_db, chunk_size=100):
    u = UniProt()
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        query = ",".join(chunk)

        try:
            results = u.mapping(fr=from_db, to=to_db, query=query)
            all_results.update(results)
            print(f"Processed {min(i+chunk_size, len(ids))}/{len(ids)}")
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")

    return all_results

# Write results to CSV
def write_mapping_to_csv(mapping, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source_ID', 'Target_IDs'])

        for source_id, target_ids in mapping.items():
            target_str = ";".join(target_ids) if target_ids else "No mapping"
            writer.writerow([source_id, target_str])

# Example usage
input_ids = read_ids_from_file("uniprot_ids.txt")
mapping = batch_convert(input_ids, "UniProtKB_AC-ID", "KEGG", chunk_size=50)
write_mapping_to_csv(mapping, "uniprot_to_kegg_mapping.csv")
```

**Script:** `scripts/batch_id_converter.py` provides command-line batch conversion.

---

## Gene Functional Annotation

**Goal:** Retrieve comprehensive functional information for a gene.

### Workflow

```python
from bioservices import UniProt, KEGG, QuickGO

# Gene of interest
gene_symbol = "TP53"

# 1. Find UniProt entry
u = UniProt()
search_results = u.search(f"gene:{gene_symbol} AND organism:9606",
                          frmt="tab",
                          columns="id,genes,protein names")

# Extract UniProt ID
lines = search_results.strip().split("\n")
if len(lines) > 1:
    uniprot_id = lines[1].split("\t")[0]
    protein_name = lines[1].split("\t")[2]
    print(f"Protein: {protein_name}")
    print(f"UniProt ID: {uniprot_id}")

# 2. Get KEGG pathways
kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
if uniprot_id in kegg_mapping:
    kegg_id = kegg_mapping[uniprot_id][0]

    k = KEGG()
    organism, gene_id = kegg_id.split(":")
    pathways = k.get_pathway_by_gene(gene_id, organism)

    print(f"\nPathways ({len(pathways)}):")
    for pathway_id in pathways[:5]:
        print(f"  {pathway_id}")

# 3. Get GO annotations
g = QuickGO()
go_annotations = g.Annotation(protein=uniprot_id, format="tsv")

if go_annotations:
    lines = go_annotations.strip().split("\n")
    print(f"\nGO Annotations ({len(lines)-1} total):")

    # Group by aspect
    aspects = {"P": [], "F": [], "C": []}
    for line in lines[1:]:
        fields = line.split("\t")
        go_aspect = fields[8]  # P, F, or C
        go_term = fields[7]
        aspects[go_aspect].append(go_term)

    print(f"  Biological Process: {len(aspects['P'])} terms")
    print(f"  Molecular Function: {len(aspects['F'])} terms")
    print(f"  Cellular Component: {len(aspects['C'])} terms")

# 4. Get protein sequence features
full_entry = u.retrieve(uniprot_id, frmt="txt")
print("\nProtein Features:")
for line in full_entry.split("\n"):
    if line.startswith("FT   DOMAIN"):
        print(f"  {line}")
```

**Output:** Comprehensive annotation including name, pathways, GO terms, and features.

---

## Protein Interaction Network Construction

**Goal:** Build a protein-protein interaction network for a set of proteins.

### Workflow

```python
from bioservices import PSICQUIC
import networkx as nx

# Proteins of interest
proteins = ["ZAP70", "LCK", "LAT", "SLP76", "PLCg1"]

# Initialize PSICQUIC
p = PSICQUIC()

# Build network
G = nx.Graph()

for protein in proteins:
    # Query for human interactions
    query = f"{protein} AND species:9606"

    try:
        results = p.query("intact", query)

        if results:
            lines = results.strip().split("\n")

            for line in lines:
                fields = line.split("\t")
                # Extract protein names (simplified)
                protein_a = fields[4].split(":")[1] if ":" in fields[4] else fields[4]
                protein_b = fields[5].split(":")[1] if ":" in fields[5] else fields[5]

                # Add edge
                G.add_edge(protein_a, protein_b)

    except Exception as e:
        print(f"Error querying {protein}: {e}")

print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Analyze network
print("\nNode degrees:")
for node in proteins:
    if node in G:
        print(f"  {node}: {G.degree(node)} interactions")

# Export for visualization
nx.write_gml(G, "protein_network.gml")
print("\nNetwork exported to protein_network.gml")
```

**Output:** NetworkX graph exported in GML format for Cytoscape visualization.

---

## Multi-Organism Comparative Analysis

**Goal:** Compare pathway or gene presence across multiple organisms.

### Workflow

```python
from bioservices import KEGG

k = KEGG()

# Organisms to compare
organisms = ["hsa", "mmu", "dme", "sce"]  # Human, mouse, fly, yeast
organism_names = {
    "hsa": "Human",
    "mmu": "Mouse",
    "dme": "Fly",
    "sce": "Yeast"
}

# Pathway of interest
pathway_name = "cell cycle"

print(f"Searching for '{pathway_name}' pathway across organisms:\n")

for org in organisms:
    k.organism = org

    # Search pathways
    results = k.lookfor_pathway(pathway_name)

    print(f"{organism_names[org]} ({org}):")
    if results:
        for pathway in results[:3]:  # Show first 3
            print(f"  {pathway}")
    else:
        print("  No matches found")
    print()
```

**Output:** Pathway presence/absence across organisms.

---

## Best Practices for Workflows

### 1. Error Handling

Always wrap service calls:
```python
try:
    result = service.method(params)
    if result:
        # Process
        pass
except Exception as e:
    print(f"Error: {e}")
```

### 2. Rate Limiting

Add delays for batch processing:
```python
import time

for item in items:
    result = service.query(item)
    time.sleep(0.5)  # 500ms delay
```

### 3. Result Validation

Check for empty or unexpected results:
```python
if result and len(result) > 0:
    # Process
    pass
else:
    print("No results returned")
```

### 4. Progress Reporting

For long workflows:
```python
total = len(items)
for i, item in enumerate(items):
    # Process item
    if (i + 1) % 10 == 0:
        print(f"Processed {i+1}/{total}")
```

### 5. Data Export

Save intermediate results:
```python
import json

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Integration with Other Tools

### BioPython Integration

```python
from bioservices import UniProt
from Bio import SeqIO
from io import StringIO

u = UniProt()
fasta_data = u.retrieve("P43403", "fasta")

# Parse with BioPython
fasta_io = StringIO(fasta_data)
record = SeqIO.read(fasta_io, "fasta")

print(f"Sequence length: {len(record.seq)}")
print(f"Description: {record.description}")
```

### Pandas Integration

```python
from bioservices import UniProt
import pandas as pd
from io import StringIO

u = UniProt()
results = u.search("zap70", frmt="tab", columns="id,genes,length,organism")

# Load into DataFrame
df = pd.read_csv(StringIO(results), sep="\t")
print(df.head())
print(df.describe())
```

### NetworkX Integration

See Protein Interaction Network Construction above.

---

For complete working examples, see the scripts in `scripts/` directory.
