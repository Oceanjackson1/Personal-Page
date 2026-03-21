---
title: "Chembl Database"
description: "Query ChEMBL bioactive molecules and drug discovery data. Search compounds by structure/properties, retrieve bioactivity data (IC50, Ki), find inhibitors, perform SAR studies, for medicinal chemistry."
category: "research"
source: "community"
author: "Community"
tags: ["chembl", "database"]
date: 2026-03-20
---

# ChEMBL Database

## Overview

ChEMBL is a manually curated database of bioactive molecules maintained by the European Bioinformatics Institute (EBI), containing over 2 million compounds, 19 million bioactivity measurements, 13,000+ drug targets, and data on approved drugs and clinical candidates. Access and query this data programmatically using the ChEMBL Python client for drug discovery and medicinal chemistry research.

## When to Use This Skill

This skill should be used when:

- **Compound searches**: Finding molecules by name, structure, or properties
- **Target information**: Retrieving data about proteins, enzymes, or biological targets
- **Bioactivity data**: Querying IC50, Ki, EC50, or other activity measurements
- **Drug information**: Looking up approved drugs, mechanisms, or indications
- **Structure searches**: Performing similarity or substructure searches
- **Cheminformatics**: Analyzing molecular properties and drug-likeness
- **Target-ligand relationships**: Exploring compound-target interactions
- **Drug discovery**: Identifying inhibitors, agonists, or bioactive molecules

## Installation and Setup

### Python Client

The ChEMBL Python client is required for programmatic access:

```bash
uv pip install chembl_webresource_client
```

### Basic Usage Pattern

```python
from chembl_webresource_client.new_client import new_client

# Access different endpoints
molecule = new_client.molecule
target = new_client.target
activity = new_client.activity
drug = new_client.drug
```

## Core Capabilities

### 1. Molecule Queries

**Retrieve by ChEMBL ID:**
```python
molecule = new_client.molecule
aspirin = molecule.get('CHEMBL25')
```

**Search by name:**
```python
results = molecule.filter(pref_name__icontains='aspirin')
```

**Filter by properties:**
```python
# Find small molecules (MW <= 500) with favorable LogP
results = molecule.filter(
    molecule_properties__mw_freebase__lte=500,
    molecule_properties__alogp__lte=5
)
```

### 2. Target Queries

**Retrieve target information:**
```python
target = new_client.target
egfr = target.get('CHEMBL203')
```

**Search for specific target types:**
```python
# Find all kinase targets
kinases = target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)
```

### 3. Bioactivity Data

**Query activities for a target:**
```python
activity = new_client.activity
# Find potent EGFR inhibitors
results = activity.filter(
    target_chembl_id='CHEMBL203',
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)
```

**Get all activities for a compound:**
```python
compound_activities = activity.filter(
    molecule_chembl_id='CHEMBL25',
    pchembl_value__isnull=False
)
```

### 4. Structure-Based Searches

**Similarity search:**
```python
similarity = new_client.similarity
# Find compounds similar to aspirin
similar = similarity.filter(
    smiles='CC(=O)Oc1ccccc1C(=O)O',
    similarity=85  # 85% similarity threshold
)
```

**Substructure search:**
```python
substructure = new_client.substructure
# Find compounds containing benzene ring
results = substructure.filter(smiles='c1ccccc1')
```

### 5. Drug Information

**Retrieve drug data:**
```python
drug = new_client.drug
drug_info = drug.get('CHEMBL25')
```

**Get mechanisms of action:**
```python
mechanism = new_client.mechanism
mechanisms = mechanism.filter(molecule_chembl_id='CHEMBL25')
```

**Query drug indications:**
```python
drug_indication = new_client.drug_indication
indications = drug_indication.filter(molecule_chembl_id='CHEMBL25')
```

## Query Workflow

### Workflow 1: Finding Inhibitors for a Target

1. **Identify the target** by searching by name:
   ```python
   targets = new_client.target.filter(pref_name__icontains='EGFR')
   target_id = targets[0]['target_chembl_id']
   ```

2. **Query bioactivity data** for that target:
   ```python
   activities = new_client.activity.filter(
       target_chembl_id=target_id,
       standard_type='IC50',
       standard_value__lte=100
   )
   ```

3. **Extract compound IDs** and retrieve details:
   ```python
   compound_ids = [act['molecule_chembl_id'] for act in activities]
   compounds = [new_client.molecule.get(cid) for cid in compound_ids]
   ```

### Workflow 2: Analyzing a Known Drug

1. **Get drug information**:
   ```python
   drug_info = new_client.drug.get('CHEMBL1234')
   ```

2. **Retrieve mechanisms**:
   ```python
   mechanisms = new_client.mechanism.filter(molecule_chembl_id='CHEMBL1234')
   ```

3. **Find all bioactivities**:
   ```python
   activities = new_client.activity.filter(molecule_chembl_id='CHEMBL1234')
   ```

### Workflow 3: Structure-Activity Relationship (SAR) Study

1. **Find similar compounds**:
   ```python
   similar = new_client.similarity.filter(smiles='query_smiles', similarity=80)
   ```

2. **Get activities for each compound**:
   ```python
   for compound in similar:
       activities = new_client.activity.filter(
           molecule_chembl_id=compound['molecule_chembl_id']
       )
   ```

3. **Analyze property-activity relationships** using molecular properties from results.

## Filter Operators

ChEMBL supports Django-style query filters:

- `__exact` - Exact match
- `__iexact` - Case-insensitive exact match
- `__contains` / `__icontains` - Substring matching
- `__startswith` / `__endswith` - Prefix/suffix matching
- `__gt`, `__gte`, `__lt`, `__lte` - Numeric comparisons
- `__range` - Value in range
- `__in` - Value in list
- `__isnull` - Null/not null check

## Data Export and Analysis

Convert results to pandas DataFrame for analysis:

```python
import pandas as pd

activities = new_client.activity.filter(target_chembl_id='CHEMBL203')
df = pd.DataFrame(list(activities))

# Analyze results
print(df['standard_value'].describe())
print(df.groupby('standard_type').size())
```

## Performance Optimization

### Caching

The client automatically caches results for 24 hours. Configure caching:

```python
from chembl_webresource_client.settings import Settings

# Disable caching
Settings.Instance().CACHING = False

# Adjust cache expiration (seconds)
Settings.Instance().CACHE_EXPIRE = 86400
```

### Lazy Evaluation

Queries execute only when data is accessed. Convert to list to force execution:

```python
# Query is not executed yet
results = molecule.filter(pref_name__icontains='aspirin')

# Force execution
results_list = list(results)
```

### Pagination

Results are paginated automatically. Iterate through all results:

```python
for activity in new_client.activity.filter(target_chembl_id='CHEMBL203'):
    # Process each activity
    print(activity['molecule_chembl_id'])
```

## Common Use Cases

### Find Kinase Inhibitors

```python
# Identify kinase targets
kinases = new_client.target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)

# Get potent inhibitors
for kinase in kinases[:5]:  # First 5 kinases
    activities = new_client.activity.filter(
        target_chembl_id=kinase['target_chembl_id'],
        standard_type='IC50',
        standard_value__lte=50
    )
```

### Explore Drug Repurposing

```python
# Get approved drugs
drugs = new_client.drug.filter()

# For each drug, find all targets
for drug in drugs[:10]:
    mechanisms = new_client.mechanism.filter(
        molecule_chembl_id=drug['molecule_chembl_id']
    )
```

### Virtual Screening

```python
# Find compounds with desired properties
candidates = new_client.molecule.filter(
    molecule_properties__mw_freebase__range=[300, 500],
    molecule_properties__alogp__lte=5,
    molecule_properties__hba__lte=10,
    molecule_properties__hbd__lte=5
)
```

## Resources

### scripts/example_queries.py

Ready-to-use Python functions demonstrating common ChEMBL query patterns:

- `get_molecule_info()` - Retrieve molecule details by ID
- `search_molecules_by_name()` - Name-based molecule search
- `find_molecules_by_properties()` - Property-based filtering
- `get_bioactivity_data()` - Query bioactivities for targets
- `find_similar_compounds()` - Similarity searching
- `substructure_search()` - Substructure matching
- `get_drug_info()` - Retrieve drug information
- `find_kinase_inhibitors()` - Specialized kinase inhibitor search
- `export_to_dataframe()` - Convert results to pandas DataFrame

Consult this script for implementation details and usage examples.

### references/api_reference.md

Comprehensive API documentation including:

- Complete endpoint listing (molecule, target, activity, assay, drug, etc.)
- All filter operators and query patterns
- Molecular properties and bioactivity fields
- Advanced query examples
- Configuration and performance tuning
- Error handling and rate limiting

Refer to this document when detailed API information is needed or when troubleshooting queries.

## Important Notes

### Data Reliability

- ChEMBL data is manually curated but may contain inconsistencies
- Always check `data_validity_comment` field in activity records
- Be aware of `potential_duplicate` flags

### Units and Standards

- Bioactivity values use standard units (nM, uM, etc.)
- `pchembl_value` provides normalized activity (-log scale)
- Check `standard_type` to understand measurement type (IC50, Ki, EC50, etc.)

### Rate Limiting

- Respect ChEMBL's fair usage policies
- Use caching to minimize repeated requests
- Consider bulk downloads for large datasets
- Avoid hammering the API with rapid consecutive requests

### Chemical Structure Formats

- SMILES strings are the primary structure format
- InChI keys available for compounds
- SVG images can be generated via the image endpoint

## Additional Resources

- ChEMBL website: https://www.ebi.ac.uk/chembl/
- API documentation: https://www.ebi.ac.uk/chembl/api/data/docs
- Python client GitHub: https://github.com/chembl/chembl_webresource_client
- Interface documentation: https://chembl.gitbook.io/chembl-interface-documentation/
- Example notebooks: https://github.com/chembl/notebooks

---

## Reference: Api_Reference

# ChEMBL Web Services API Reference

## Overview

ChEMBL is a manually curated database of bioactive molecules with drug-like properties maintained by the European Bioinformatics Institute (EBI). It contains information about compounds, targets, assays, bioactivity data, and approved drugs.

The ChEMBL database contains:
- Over 2 million compound records
- Over 1.4 million assay records
- Over 19 million activity values
- Information on 13,000+ drug targets
- Data on 16,000+ approved drugs and clinical candidates

## Python Client Installation

```bash
pip install chembl_webresource_client
```

## Key Resources and Endpoints

ChEMBL provides access to 30+ specialized endpoints:

### Core Data Types

- **molecule** - Compound structures, properties, and synonyms
- **target** - Protein and non-protein biological targets
- **activity** - Bioassay measurement results
- **assay** - Experimental assay details
- **drug** - Approved pharmaceutical information
- **mechanism** - Drug mechanism of action data
- **document** - Literature sources and references
- **cell_line** - Cell line information
- **tissue** - Tissue types
- **protein_class** - Protein classification
- **target_component** - Target component details
- **compound_structural_alert** - Structural alerts for toxicity

## Query Patterns and Filters

### Filter Operators

The API supports Django-style filter operators:

- `__exact` - Exact match
- `__iexact` - Case-insensitive exact match
- `__contains` - Contains substring
- `__icontains` - Case-insensitive contains
- `__startswith` - Starts with prefix
- `__endswith` - Ends with suffix
- `__gt` - Greater than
- `__gte` - Greater than or equal
- `__lt` - Less than
- `__lte` - Less than or equal
- `__range` - Value in range
- `__in` - Value in list
- `__isnull` - Is null/not null
- `__regex` - Regular expression match
- `__search` - Full text search

### Example Filter Queries

**Molecular weight filtering:**
```python
molecules.filter(molecule_properties__mw_freebase__lte=300)
```

**Name pattern matching:**
```python
molecules.filter(pref_name__endswith='nib')
```

**Multiple conditions:**
```python
molecules.filter(
    molecule_properties__mw_freebase__lte=300,
    pref_name__endswith='nib'
)
```

## Chemical Structure Searches

### Substructure Search
Search for compounds containing a specific substructure using SMILES:

```python
from chembl_webresource_client.new_client import new_client
similarity = new_client.similarity
results = similarity.filter(smiles='CC(=O)Oc1ccccc1C(=O)O', similarity=70)
```

### Similarity Search
Find compounds similar to a query structure:

```python
similarity = new_client.similarity
results = similarity.filter(smiles='CC(=O)Oc1ccccc1C(=O)O', similarity=85)
```

## Common Data Retrieval Patterns

### Get Molecule by ChEMBL ID
```python
molecule = new_client.molecule.get('CHEMBL25')
```

### Get Target Information
```python
target = new_client.target.get('CHEMBL240')
```

### Get Activity Data
```python
activities = new_client.activity.filter(
    target_chembl_id='CHEMBL240',
    standard_type='IC50',
    standard_value__lte=100
)
```

### Get Drug Information
```python
drug = new_client.drug.get('CHEMBL1234')
```

## Response Formats

The API supports multiple response formats:
- JSON (default)
- XML
- YAML

## Caching and Performance

The Python client automatically caches results locally:
- **Default cache duration**: 24 hours
- **Cache location**: Local file system
- **Lazy evaluation**: Queries execute only when data is accessed

### Configuration Settings

```python
from chembl_webresource_client.settings import Settings

# Disable caching
Settings.Instance().CACHING = False

# Adjust cache expiration (in seconds)
Settings.Instance().CACHE_EXPIRE = 86400  # 24 hours

# Set timeout
Settings.Instance().TIMEOUT = 30

# Set retries
Settings.Instance().TOTAL_RETRIES = 3
```

## Molecular Properties

Common molecular properties available:

- `mw_freebase` - Molecular weight
- `alogp` - Calculated LogP
- `hba` - Hydrogen bond acceptors
- `hbd` - Hydrogen bond donors
- `psa` - Polar surface area
- `rtb` - Rotatable bonds
- `ro3_pass` - Rule of 3 compliance
- `num_ro5_violations` - Lipinski rule of 5 violations
- `cx_most_apka` - Most acidic pKa
- `cx_most_bpka` - Most basic pKa
- `molecular_species` - Molecular species
- `full_mwt` - Full molecular weight

## Bioactivity Data Fields

Key bioactivity fields:

- `standard_type` - Activity type (IC50, Ki, Kd, EC50, etc.)
- `standard_value` - Numerical activity value
- `standard_units` - Units (nM, uM, etc.)
- `pchembl_value` - Normalized activity value (-log scale)
- `activity_comment` - Activity annotations
- `data_validity_comment` - Data validity flags
- `potential_duplicate` - Duplicate flag

## Target Information Fields

Target data includes:

- `target_chembl_id` - ChEMBL target identifier
- `pref_name` - Preferred target name
- `target_type` - Type (PROTEIN, ORGANISM, etc.)
- `organism` - Target organism
- `tax_id` - NCBI taxonomy ID
- `target_components` - Component details

## Advanced Query Examples

### Find Kinase Inhibitors
```python
# Get kinase targets
targets = new_client.target.filter(
    target_type='SINGLE PROTEIN',
    pref_name__icontains='kinase'
)

# Get activities for these targets
activities = new_client.activity.filter(
    target_chembl_id__in=[t['target_chembl_id'] for t in targets],
    standard_type='IC50',
    standard_value__lte=100
)
```

### Retrieve Drug Mechanisms
```python
mechanisms = new_client.mechanism.filter(
    molecule_chembl_id='CHEMBL25'
)
```

### Get Compound Bioactivities
```python
activities = new_client.activity.filter(
    molecule_chembl_id='CHEMBL25',
    pchembl_value__isnull=False
)
```

## Image Generation

ChEMBL can generate SVG images of molecular structures:

```python
from chembl_webresource_client.new_client import new_client
image = new_client.image
svg = image.get('CHEMBL25')
```

## Pagination

Results are paginated automatically. To iterate through all results:

```python
activities = new_client.activity.filter(target_chembl_id='CHEMBL240')
for activity in activities:
    print(activity)
```

## Error Handling

Common errors:
- **404**: Resource not found
- **503**: Service temporarily unavailable
- **Timeout**: Request took too long

The client automatically retries failed requests based on `TOTAL_RETRIES` setting.

## Rate Limiting

ChEMBL has fair usage policies:
- Be respectful with query frequency
- Use caching to minimize repeated requests
- Consider bulk downloads for large datasets

## Additional Resources

- Official API documentation: https://www.ebi.ac.uk/chembl/api/data/docs
- Python client GitHub: https://github.com/chembl/chembl_webresource_client
- ChEMBL interface docs: https://chembl.gitbook.io/chembl-interface-documentation/
- Example notebooks: https://github.com/chembl/notebooks
