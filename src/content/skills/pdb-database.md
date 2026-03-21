---
title: "Pdb Database"
description: "Access RCSB PDB for 3D protein/nucleic acid structures. Search by text/sequence/structure, download coordinates (PDB/mmCIF), retrieve metadata, for structural biology and drug discovery."
category: "research"
source: "community"
author: "Community"
tags: ["pdb", "database"]
date: 2026-03-20
---

# PDB Database

## Overview

RCSB PDB is the worldwide repository for 3D structural data of biological macromolecules. Search for structures, retrieve coordinates and metadata, perform sequence and structure similarity searches across 200,000+ experimentally determined structures and computed models.

## When to Use This Skill

This skill should be used when:
- Searching for protein or nucleic acid 3D structures by text, sequence, or structural similarity
- Downloading coordinate files in PDB, mmCIF, or BinaryCIF formats
- Retrieving structural metadata, experimental methods, or quality metrics
- Performing batch operations across multiple structures
- Integrating PDB data into computational workflows for drug discovery, protein engineering, or structural biology research

## Core Capabilities

### 1. Searching for Structures

Find PDB entries using various search criteria:

**Text Search:** Search by protein name, keywords, or descriptions
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**Attribute Search:** Query specific properties (organism, resolution, method, etc.)
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entity_source_organism

# Find human protein structures
query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())
```

**Sequence Similarity:** Find structures similar to a given sequence
```python
from rcsbapi.search import SequenceQuery

query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)
results = list(query())
```

**Structure Similarity:** Find structures with similar 3D geometry
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # Hemoglobin
)
results = list(query())
```

**Combining Queries:** Use logical operators to build complex searches
```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info

# High-resolution human proteins
query1 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
query2 = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
combined_query = query1 & query2  # AND operation
results = list(combined_query())
```

### 2. Retrieving Structure Data

Access detailed information about specific PDB entries:

**Basic Entry Information:**
```python
from rcsbapi.data import Schema, fetch

# Get entry-level data
entry_data = fetch("4HHB", schema=Schema.ENTRY)
print(entry_data["struct"]["title"])
print(entry_data["exptl"][0]["method"])
```

**Polymer Entity Information:**
```python
# Get protein/nucleic acid information
entity_data = fetch("4HHB_1", schema=Schema.POLYMER_ENTITY)
print(entity_data["entity_poly"]["pdbx_seq_one_letter_code"])
```

**Using GraphQL for Flexible Queries:**
```python
from rcsbapi.data import fetch

# Custom GraphQL query
query = """
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
    }
  }
}
"""
data = fetch(query_type="graphql", query=query)
```

### 3. Downloading Structure Files

Retrieve coordinate files in various formats:

**Download Methods:**
- **PDB format** (legacy text format): `https://files.rcsb.org/download/{PDB_ID}.pdb`
- **mmCIF format** (modern standard): `https://files.rcsb.org/download/{PDB_ID}.cif`
- **BinaryCIF** (compressed binary): Use ModelServer API for efficient access
- **Biological assembly**: `https://files.rcsb.org/download/{PDB_ID}.pdb1` (for assembly 1)

**Example Download:**
```python
import requests

pdb_id = "4HHB"

# Download PDB format
pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
response = requests.get(pdb_url)
with open(f"{pdb_id}.pdb", "w") as f:
    f.write(response.text)

# Download mmCIF format
cif_url = f"https://files.rcsb.org/download/{pdb_id}.cif"
response = requests.get(cif_url)
with open(f"{pdb_id}.cif", "w") as f:
    f.write(response.text)
```

### 4. Working with Structure Data

Common operations with retrieved structures:

**Parse and Analyze Coordinates:**
Use BioPython or other structural biology libraries to work with downloaded files:
```python
from Bio.PDB import PDBParser

parser = PDBParser()
structure = parser.get_structure("protein", "4HHB.pdb")

# Iterate through atoms
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())
```

**Extract Metadata:**
```python
from rcsbapi.data import fetch, Schema

# Get experimental details
data = fetch("4HHB", schema=Schema.ENTRY)

resolution = data.get("rcsb_entry_info", {}).get("resolution_combined")
method = data.get("exptl", [{}])[0].get("method")
deposition_date = data.get("rcsb_accession_info", {}).get("deposit_date")

print(f"Resolution: {resolution} Å")
print(f"Method: {method}")
print(f"Deposited: {deposition_date}")
```

### 5. Batch Operations

Process multiple structures efficiently:

```python
from rcsbapi.data import fetch, Schema

pdb_ids = ["4HHB", "1MBN", "1GZX"]  # Hemoglobin, myoglobin, etc.

results = {}
for pdb_id in pdb_ids:
    try:
        data = fetch(pdb_id, schema=Schema.ENTRY)
        results[pdb_id] = {
            "title": data["struct"]["title"],
            "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
            "organism": data.get("rcsb_entity_source_organism", [{}])[0].get("scientific_name")
        }
    except Exception as e:
        print(f"Error fetching {pdb_id}: {e}")

# Display results
for pdb_id, info in results.items():
    print(f"\n{pdb_id}: {info['title']}")
    print(f"  Resolution: {info['resolution']} Å")
    print(f"  Organism: {info['organism']}")
```

## Python Package Installation

Install the official RCSB PDB Python API client:

```bash
# Current recommended package
uv pip install rcsb-api

# For legacy code (deprecated, use rcsb-api instead)
uv pip install rcsbsearchapi
```

The `rcsb-api` package provides unified access to both Search and Data APIs through the `rcsbapi.search` and `rcsbapi.data` modules.

## Common Use Cases

### Drug Discovery
- Search for structures of drug targets
- Analyze ligand binding sites
- Compare protein-ligand complexes
- Identify similar binding pockets

### Protein Engineering
- Find homologous structures for modeling
- Analyze sequence-structure relationships
- Compare mutant structures
- Study protein stability and dynamics

### Structural Biology Research
- Download structures for computational analysis
- Build structure-based alignments
- Analyze structural features (secondary structure, domains)
- Compare experimental methods and quality metrics

### Education and Visualization
- Retrieve structures for teaching
- Generate molecular visualizations
- Explore structure-function relationships
- Study evolutionary conservation

## Key Concepts

**PDB ID:** Unique 4-character identifier (e.g., "4HHB") for each structure entry. AlphaFold and ModelArchive entries start with "AF_" or "MA_" prefixes.

**mmCIF/PDBx:** Modern file format that uses key-value structure, replacing legacy PDB format for large structures.

**Biological Assembly:** The functional form of a macromolecule, which may contain multiple copies of chains from the asymmetric unit.

**Resolution:** Measure of detail in crystallographic structures (lower values = higher detail). Typical range: 1.5-3.5 Å for high-quality structures.

**Entity:** A unique molecular component in a structure (protein chain, DNA, ligand, etc.).

## Resources

This skill includes reference documentation in the `references/` directory:

### references/api_reference.md
Comprehensive API documentation covering:
- Detailed API endpoint specifications
- Advanced query patterns and examples
- Data schema reference
- Rate limiting and best practices
- Troubleshooting common issues

Use this reference when you need in-depth information about API capabilities, complex query construction, or detailed data schema information.

## Additional Resources

- **RCSB PDB Website:** https://www.rcsb.org
- **PDB-101 Educational Portal:** https://pdb101.rcsb.org
- **API Documentation:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Python Package Docs:** https://rcsbapi.readthedocs.io/
- **Data API Documentation:** https://data.rcsb.org/
- **GitHub Repository:** https://github.com/rcsb/py-rcsb-api

---

## Reference: Api_Reference

# RCSB PDB API Reference

This document provides detailed information about the RCSB Protein Data Bank APIs, including advanced usage patterns, data schemas, and best practices.

## API Overview

RCSB PDB provides multiple programmatic interfaces:

1. **Data API** - Retrieve PDB data when you have an identifier
2. **Search API** - Find identifiers matching specific search criteria
3. **ModelServer API** - Access macromolecular model subsets
4. **VolumeServer API** - Retrieve volumetric data subsets
5. **Sequence Coordinates API** - Obtain alignments between structural and sequence databases
6. **Alignment API** - Perform structure alignment computations

## Data API

### Core Data Objects

The Data API organizes information hierarchically:

- **core_entry**: PDB entries or Computed Structure Models (CSM IDs start with AF_ or MA_)
- **core_polymer_entity**: Protein, DNA, and RNA entities
- **core_nonpolymer_entity**: Ligands, cofactors, ions
- **core_branched_entity**: Oligosaccharides
- **core_assembly**: Biological assemblies
- **core_polymer_entity_instance**: Individual chains
- **core_chem_comp**: Chemical components

### REST API Endpoints

Base URL: `https://data.rcsb.org/rest/v1/`

**Entry Data:**
```
GET https://data.rcsb.org/rest/v1/core/entry/{entry_id}
```

**Polymer Entity:**
```
GET https://data.rcsb.org/rest/v1/core/polymer_entity/{entry_id}_{entity_id}
```

**Assembly:**
```
GET https://data.rcsb.org/rest/v1/core/assembly/{entry_id}/{assembly_id}
```

**Examples:**
```bash
# Get entry data for hemoglobin
curl https://data.rcsb.org/rest/v1/core/entry/4HHB

# Get first polymer entity
curl https://data.rcsb.org/rest/v1/core/polymer_entity/4HHB_1

# Get biological assembly 1
curl https://data.rcsb.org/rest/v1/core/assembly/4HHB/1
```

### GraphQL API

Endpoint: `https://data.rcsb.org/graphql`

The GraphQL API enables flexible data retrieval, allowing you to grab any piece of data from any level of the hierarchy in a single query.

**Example Query:**
```graphql
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
      polymer_entity_count
    }
    rcsb_accession_info {
      deposit_date
      initial_release_date
    }
  }
}
```

**Python Example:**
```python
import requests

query = """
{
  polymer_entity(entity_id: "4HHB_1") {
    rcsb_polymer_entity {
      pdbx_description
      formula_weight
    }
    entity_poly {
      pdbx_seq_one_letter_code
      pdbx_strand_id
    }
    rcsb_entity_source_organism {
      ncbi_taxonomy_id
      scientific_name
    }
  }
}
"""

response = requests.post(
    "https://data.rcsb.org/graphql",
    json={"query": query}
)
data = response.json()
```

### Common Data Fields

**Entry Level:**
- `struct.title` - Structure title/description
- `exptl[].method` - Experimental method (X-RAY DIFFRACTION, NMR, ELECTRON MICROSCOPY, etc.)
- `rcsb_entry_info.resolution_combined` - Resolution in Ångströms
- `rcsb_entry_info.deposited_atom_count` - Total number of atoms
- `rcsb_accession_info.deposit_date` - Deposition date
- `rcsb_accession_info.initial_release_date` - Release date

**Polymer Entity Level:**
- `entity_poly.pdbx_seq_one_letter_code` - Primary sequence
- `rcsb_polymer_entity.formula_weight` - Molecular weight
- `rcsb_entity_source_organism.scientific_name` - Source organism
- `rcsb_entity_source_organism.ncbi_taxonomy_id` - NCBI taxonomy ID

**Assembly Level:**
- `rcsb_assembly_info.polymer_entity_count` - Number of polymer entities
- `rcsb_assembly_info.assembly_id` - Assembly identifier

## Search API

### Query Types

The Search API supports seven primary query types:

1. **TextQuery** - Full-text search
2. **AttributeQuery** - Property-based search
3. **SequenceQuery** - Sequence similarity search
4. **SequenceMotifQuery** - Motif pattern search
5. **StructSimilarityQuery** - 3D structure similarity
6. **StructMotifQuery** - Structural motif search
7. **ChemSimilarityQuery** - Chemical similarity search

### AttributeQuery Operators

Available operators for AttributeQuery:

- `exact_match` - Exact string match
- `contains_words` - Contains all words
- `contains_phrase` - Contains exact phrase
- `equals` - Numerical equality
- `greater` - Greater than (numerical)
- `greater_or_equal` - Greater than or equal
- `less` - Less than (numerical)
- `less_or_equal` - Less than or equal
- `range` - Numerical range (closed interval)
- `exists` - Field has a value
- `in` - Value in list

### Common Searchable Attributes

**Resolution and Quality:**
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info

# High-resolution structures
query = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)
```

**Experimental Method:**
```python
from rcsbapi.search.attrs import exptl

query = AttributeQuery(
    attribute=exptl.method,
    operator="exact_match",
    value="X-RAY DIFFRACTION"
)
```

**Organism:**
```python
from rcsbapi.search.attrs import rcsb_entity_source_organism

query = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
```

**Molecular Weight:**
```python
from rcsbapi.search.attrs import rcsb_polymer_entity

query = AttributeQuery(
    attribute=rcsb_polymer_entity.formula_weight,
    operator="range",
    value=(10000, 50000)  # 10-50 kDa
)
```

**Release Date:**
```python
from rcsbapi.search.attrs import rcsb_accession_info

# Structures released in 2024
query = AttributeQuery(
    attribute=rcsb_accession_info.initial_release_date,
    operator="range",
    value=("2024-01-01", "2024-12-31")
)
```

### Sequence Similarity Search

Search for structures with similar sequences using MMseqs2:

```python
from rcsbapi.search import SequenceQuery

# Basic sequence search
query = SequenceQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9
)

# With sequence type specified
query = SequenceQuery(
    value="ACGTACGTACGT",
    evalue_cutoff=1e-5,
    identity_cutoff=0.8,
    sequence_type="dna"  # or "rna" or "protein"
)
```

### Structure Similarity Search

Find structures with similar 3D geometry using BioZernike:

```python
from rcsbapi.search import StructSimilarityQuery

# Search by entry
query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"
)

# Search by chain
query = StructSimilarityQuery(
    structure_search_type="chain",
    entry_id="4HHB",
    chain_id="A"
)

# Search by assembly
query = StructSimilarityQuery(
    structure_search_type="assembly",
    entry_id="4HHB",
    assembly_id="1"
)
```

### Combining Queries

Use Python bitwise operators to combine queries:

```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info, rcsb_entity_source_organism

# AND operation (&)
query1 = TextQuery("kinase")
query2 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
combined = query1 & query2

# OR operation (|)
organism1 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Homo sapiens"
)
organism2 = AttributeQuery(
    attribute=rcsb_entity_source_organism.scientific_name,
    operator="exact_match",
    value="Mus musculus"
)
combined = organism1 | organism2

# NOT operation (~)
all_structures = TextQuery("protein")
low_res = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="greater",
    value=3.0
)
high_res_only = all_structures & (~low_res)

# Complex combinations
high_res_human_kinases = (
    TextQuery("kinase") &
    AttributeQuery(
        attribute=rcsb_entity_source_organism.scientific_name,
        operator="exact_match",
        value="Homo sapiens"
    ) &
    AttributeQuery(
        attribute=rcsb_entry_info.resolution_combined,
        operator="less",
        value=2.5
    )
)
```

### Return Types

Control what information is returned:

```python
from rcsbapi.search import TextQuery, ReturnType

query = TextQuery("hemoglobin")

# Return PDB IDs (default)
results = list(query())  # ['4HHB', '1A3N', ...]

# Return entry IDs with scores
results = list(query(return_type=ReturnType.ENTRY, return_scores=True))
# [{'identifier': '4HHB', 'score': 0.95}, ...]

# Return polymer entities
results = list(query(return_type=ReturnType.POLYMER_ENTITY))
# ['4HHB_1', '4HHB_2', ...]
```

## File Download URLs

### Structure Files

**PDB Format (legacy):**
```
https://files.rcsb.org/download/{PDB_ID}.pdb
```

**mmCIF Format (modern standard):**
```
https://files.rcsb.org/download/{PDB_ID}.cif
```

**Structure Factors:**
```
https://files.rcsb.org/download/{PDB_ID}-sf.cif
```

**Biological Assembly:**
```
https://files.rcsb.org/download/{PDB_ID}.pdb1  # Assembly 1
https://files.rcsb.org/download/{PDB_ID}.pdb2  # Assembly 2
```

**FASTA Sequence:**
```
https://www.rcsb.org/fasta/entry/{PDB_ID}
```

### Python Download Helper

```python
import requests

def download_pdb_file(pdb_id, format="pdb", output_dir="."):
    """
    Download PDB structure file.

    Args:
        pdb_id: 4-character PDB ID
        format: 'pdb' or 'cif'
        output_dir: Directory to save file
    """
    base_url = "https://files.rcsb.org/download"
    url = f"{base_url}/{pdb_id}.{format}"

    response = requests.get(url)
    if response.status_code == 200:
        output_path = f"{output_dir}/{pdb_id}.{format}"
        with open(output_path, "w") as f:
            f.write(response.text)
        print(f"Downloaded {pdb_id}.{format}")
        return output_path
    else:
        print(f"Error downloading {pdb_id}: {response.status_code}")
        return None

# Usage
download_pdb_file("4HHB", format="pdb")
download_pdb_file("4HHB", format="cif")
```

## Rate Limiting and Best Practices

### Rate Limits

- The API implements rate limiting to ensure fair usage
- If you exceed the limit, you'll receive a 429 HTTP error code
- Recommended starting point: a few requests per second
- Use exponential backoff to find acceptable request rates

### Exponential Backoff Implementation

```python
import time
import requests

def fetch_with_retry(url, max_retries=5, initial_delay=1):
    """
    Fetch URL with exponential backoff on rate limit errors.

    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
    """
    delay = initial_delay

    for attempt in range(max_retries):
        response = requests.get(url)

        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print(f"Rate limited. Waiting {delay}s before retry...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            response.raise_for_status()

    raise Exception(f"Failed after {max_retries} retries")
```

### Batch Processing Best Practices

1. **Use Search API first** to get list of IDs, then fetch data
2. **Cache results** to avoid redundant queries
3. **Process in chunks** rather than all at once
4. **Add delays** between requests to respect rate limits
5. **Use GraphQL** for complex queries to minimize requests

```python
import time
from rcsbapi.search import TextQuery
from rcsbapi.data import fetch, Schema

def batch_fetch_structures(query, delay=0.5):
    """
    Fetch structures matching a query with rate limiting.

    Args:
        query: Search query object
        delay: Delay between requests in seconds
    """
    # Get list of IDs
    pdb_ids = list(query())
    print(f"Found {len(pdb_ids)} structures")

    # Fetch data for each
    results = {}
    for i, pdb_id in enumerate(pdb_ids):
        try:
            data = fetch(pdb_id, schema=Schema.ENTRY)
            results[pdb_id] = data
            print(f"Fetched {i+1}/{len(pdb_ids)}: {pdb_id}")
            time.sleep(delay)  # Rate limiting
        except Exception as e:
            print(f"Error fetching {pdb_id}: {e}")

    return results
```

## Advanced Use Cases

### Finding Drug-Target Complexes

```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_polymer_entity, rcsb_nonpolymer_entity_instance_container_identifiers

# Find structures with specific drug molecule
query = AttributeQuery(
    attribute=rcsb_nonpolymer_entity_instance_container_identifiers.comp_id,
    operator="exact_match",
    value="ATP"  # or other ligand code
)

results = list(query())
print(f"Found {len(results)} structures with ATP")
```

### Filtering by Resolution and R-factor

```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_entry_info, refine

# High-quality X-ray structures
resolution_query = AttributeQuery(
    attribute=rcsb_entry_info.resolution_combined,
    operator="less",
    value=2.0
)

rfactor_query = AttributeQuery(
    attribute=refine.ls_R_factor_R_free,
    operator="less",
    value=0.25
)

high_quality = resolution_query & rfactor_query
results = list(high_quality())
```

### Finding Recent Structures

```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search.attrs import rcsb_accession_info

# Structures released in last month
import datetime

one_month_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
today = datetime.date.today().isoformat()

query = AttributeQuery(
    attribute=rcsb_accession_info.initial_release_date,
    operator="range",
    value=(one_month_ago, today)
)

recent_structures = list(query())
```

## Troubleshooting

### Common Errors

**404 Not Found:**
- PDB ID doesn't exist or is obsolete
- Check if ID is correct (case-sensitive)
- Verify entry hasn't been superseded

**429 Too Many Requests:**
- Rate limit exceeded
- Implement exponential backoff
- Reduce request frequency

**500 Internal Server Error:**
- Temporary server issue
- Retry after short delay
- Check RCSB PDB status page

**Empty Results:**
- Query too restrictive
- Check attribute names and operators
- Verify data exists for searched field

### Debugging Tips

```python
# Enable verbose output for searches
from rcsbapi.search import TextQuery

query = TextQuery("hemoglobin")
print(query.to_dict())  # See query structure

# Check query JSON
import json
print(json.dumps(query.to_dict(), indent=2))

# Test with curl
import subprocess
result = subprocess.run(
    ["curl", "https://data.rcsb.org/rest/v1/core/entry/4HHB"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

## Additional Resources

- **API Documentation:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Data API Redoc:** https://data.rcsb.org/redoc/index.html
- **GraphQL Schema:** https://data.rcsb.org/graphql
- **Python Package Docs:** https://rcsbapi.readthedocs.io/
- **GitHub Issues:** https://github.com/rcsb/py-rcsb-api/issues
- **Community Forum:** https://www.rcsb.org/help
