---
title: "Zinc Database"
description: "Access ZINC (230M+ purchasable compounds). Search by ZINC ID/SMILES, similarity searches, 3D-ready structures for docking, analog discovery, for virtual screening and drug discovery."
category: "research"
source: "community"
author: "Community"
tags: ["zinc", "database"]
date: 2026-03-20
---

# ZINC Database

## Overview

ZINC is a freely accessible repository of 230M+ purchasable compounds maintained by UCSF. Search by ZINC ID or SMILES, perform similarity searches, download 3D-ready structures for docking, discover analogs for virtual screening and drug discovery.

## When to Use This Skill

This skill should be used when:

- **Virtual screening**: Finding compounds for molecular docking studies
- **Lead discovery**: Identifying commercially-available compounds for drug development
- **Structure searches**: Performing similarity or analog searches by SMILES
- **Compound retrieval**: Looking up molecules by ZINC IDs or supplier codes
- **Chemical space exploration**: Exploring purchasable chemical diversity
- **Docking studies**: Accessing 3D-ready molecular structures
- **Analog searches**: Finding similar compounds based on structural similarity
- **Supplier queries**: Identifying compounds from specific chemical vendors
- **Random sampling**: Obtaining random compound sets for screening

## Database Versions

ZINC has evolved through multiple versions:

- **ZINC22** (Current): Largest version with 230+ million purchasable compounds and multi-billion scale make-on-demand compounds
- **ZINC20**: Still maintained, focused on lead-like and drug-like compounds
- **ZINC15**: Predecessor version, legacy but still documented

This skill primarily focuses on ZINC22, the most current and comprehensive version.

## Access Methods

### Web Interface

Primary access point: https://zinc.docking.org/
Interactive searching: https://cartblanche22.docking.org/

### API Access

All ZINC22 searches can be performed programmatically via the CartBlanche22 API:

**Base URL**: `https://cartblanche22.docking.org/`

All API endpoints return data in text or JSON format with customizable fields.

## Core Capabilities

### 1. Search by ZINC ID

Retrieve specific compounds using their ZINC identifiers.

**Web interface**: https://cartblanche22.docking.org/search/zincid

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=smiles,zinc_id"
```

**Multiple IDs**:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=smiles,zinc_id,tranche"
```

**Response fields**: `zinc_id`, `smiles`, `sub_id`, `supplier_code`, `catalogs`, `tranche` (includes H-count, LogP, MW, phase)

### 2. Search by SMILES

Find compounds by chemical structure using SMILES notation, with optional distance parameters for analog searching.

**Web interface**: https://cartblanche22.docking.org/search/smiles

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/[email protected]=4-Fadist=4"
```

**Parameters**:
- `smiles`: Query SMILES string (URL-encoded if necessary)
- `dist`: Tanimoto distance threshold (default: 0 for exact match)
- `adist`: Alternative distance parameter for broader searches (default: 0)
- `output_fields`: Comma-separated list of desired output fields

**Example - Exact match**:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1"
```

**Example - Similarity search**:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1&dist=3&output_fields=zinc_id,smiles,tranche"
```

### 3. Search by Supplier Codes

Query compounds from specific chemical suppliers or retrieve all molecules from particular catalogs.

**Web interface**: https://cartblanche22.docking.org/search/catitems

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/catitems.txt:catitem_id=SUPPLIER-CODE-123"
```

**Use cases**:
- Verify compound availability from specific vendors
- Retrieve all compounds from a catalog
- Cross-reference supplier codes with ZINC IDs

### 4. Random Compound Sampling

Generate random compound sets for screening or benchmarking purposes.

**Web interface**: https://cartblanche22.docking.org/search/random

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=100"
```

**Parameters**:
- `count`: Number of random compounds to retrieve (default: 100)
- `subset`: Filter by subset (e.g., 'lead-like', 'drug-like', 'fragment')
- `output_fields`: Customize returned data fields

**Example - Random lead-like molecules**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=1000&subset=lead-like&output_fields=zinc_id,smiles,tranche"
```

## Common Workflows

### Workflow 1: Preparing a Docking Library

1. **Define search criteria** based on target properties or desired chemical space

2. **Query ZINC22** using appropriate search method:
   ```bash
   # Example: Get drug-like compounds with specific LogP and MW
   curl "https://cartblanche22.docking.org/substance/random.txt:count=10000&subset=drug-like&output_fields=zinc_id,smiles,tranche" > docking_library.txt
   ```

3. **Parse results** to extract ZINC IDs and SMILES:
   ```python
   import pandas as pd

   # Load results
   df = pd.read_csv('docking_library.txt', sep='\t')

   # Filter by properties in tranche data
   # Tranche format: H##P###M###-phase
   # H = H-bond donors, P = LogP*10, M = MW
   ```

4. **Download 3D structures** for docking using ZINC ID or download from file repositories

### Workflow 2: Finding Analogs of a Hit Compound

1. **Obtain SMILES** of the hit compound:
   ```python
   hit_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  # Example: Ibuprofen
   ```

2. **Perform similarity search** with distance threshold:
   ```bash
   curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC(C)Cc1ccc(cc1)C(C)C(=O)O&dist=5&output_fields=zinc_id,smiles,catalogs" > analogs.txt
   ```

3. **Analyze results** to identify purchasable analogs:
   ```python
   import pandas as pd

   analogs = pd.read_csv('analogs.txt', sep='\t')
   print(f"Found {len(analogs)} analogs")
   print(analogs[['zinc_id', 'smiles', 'catalogs']].head(10))
   ```

4. **Retrieve 3D structures** for the most promising analogs

### Workflow 3: Batch Compound Retrieval

1. **Compile list of ZINC IDs** from literature, databases, or previous screens:
   ```python
   zinc_ids = [
       "ZINC000000000001",
       "ZINC000000000002",
       "ZINC000000000003"
   ]
   zinc_ids_str = ",".join(zinc_ids)
   ```

2. **Query ZINC22 API**:
   ```bash
   curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002&output_fields=zinc_id,smiles,supplier_code,catalogs"
   ```

3. **Process results** for downstream analysis or purchasing

### Workflow 4: Chemical Space Sampling

1. **Select subset parameters** based on screening goals:
   - Fragment: MW < 250, good for fragment-based drug discovery
   - Lead-like: MW 250-350, LogP ≤ 3.5
   - Drug-like: MW 350-500, follows Lipinski's Rule of Five

2. **Generate random sample**:
   ```bash
   curl "https://cartblanche22.docking.org/substance/random.txt:count=5000&subset=lead-like&output_fields=zinc_id,smiles,tranche" > chemical_space_sample.txt
   ```

3. **Analyze chemical diversity** and prepare for virtual screening

## Output Fields

Customize API responses with the `output_fields` parameter:

**Available fields**:
- `zinc_id`: ZINC identifier
- `smiles`: SMILES string representation
- `sub_id`: Internal substance ID
- `supplier_code`: Vendor catalog number
- `catalogs`: List of suppliers offering the compound
- `tranche`: Encoded molecular properties (H-count, LogP, MW, reactivity phase)

**Example**:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001&output_fields=zinc_id,smiles,catalogs,tranche"
```

## Tranche System

ZINC organizes compounds into "tranches" based on molecular properties:

**Format**: `H##P###M###-phase`

- **H##**: Number of hydrogen bond donors (00-99)
- **P###**: LogP × 10 (e.g., P035 = LogP 3.5)
- **M###**: Molecular weight in Daltons (e.g., M400 = 400 Da)
- **phase**: Reactivity classification

**Example tranche**: `H05P035M400-0`
- 5 H-bond donors
- LogP = 3.5
- MW = 400 Da
- Reactivity phase 0

Use tranche data to filter compounds by drug-likeness criteria.

## Downloading 3D Structures

For molecular docking, 3D structures are available via file repositories:

**File repository**: https://files.docking.org/zinc22/

Structures are organized by tranches and available in multiple formats:
- MOL2: Multi-molecule format with 3D coordinates
- SDF: Structure-data file format
- DB2.GZ: Compressed database format for DOCK

Refer to ZINC documentation at https://wiki.docking.org for downloading protocols and batch access methods.

## Python Integration

### Using curl with Python

```python
import subprocess
import json

def query_zinc_by_id(zinc_id, output_fields="zinc_id,smiles,catalogs"):
    """Query ZINC22 by ZINC ID."""
    url = f"https://cartblanche22.docking.org/[email protected]_id={zinc_id}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def search_by_smiles(smiles, dist=0, adist=0, output_fields="zinc_id,smiles"):
    """Search ZINC22 by SMILES with optional distance parameters."""
    url = f"https://cartblanche22.docking.org/smiles.txt:smiles={smiles}&dist={dist}&adist={adist}&output_fields={output_fields}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout

def get_random_compounds(count=100, subset=None, output_fields="zinc_id,smiles,tranche"):
    """Get random compounds from ZINC22."""
    url = f"https://cartblanche22.docking.org/substance/random.txt:count={count}&output_fields={output_fields}"
    if subset:
        url += f"&subset={subset}"
    result = subprocess.run(['curl', url], capture_output=True, text=True)
    return result.stdout
```

### Parsing Results

```python
import pandas as pd
from io import StringIO

# Query ZINC and parse as DataFrame
result = query_zinc_by_id("ZINC000000000001")
df = pd.read_csv(StringIO(result), sep='\t')

# Extract tranche properties
def parse_tranche(tranche_str):
    """Parse ZINC tranche code to extract properties."""
    # Format: H##P###M###-phase
    import re
    match = re.match(r'H(\d+)P(\d+)M(\d+)-(\d+)', tranche_str)
    if match:
        return {
            'h_donors': int(match.group(1)),
            'logP': int(match.group(2)) / 10.0,
            'mw': int(match.group(3)),
            'phase': int(match.group(4))
        }
    return None

df['tranche_props'] = df['tranche'].apply(parse_tranche)
```

## Best Practices

### Query Optimization

- **Start specific**: Begin with exact searches before expanding to similarity searches
- **Use appropriate distance parameters**: Small dist values (1-3) for close analogs, larger (5-10) for diverse analogs
- **Limit output fields**: Request only necessary fields to reduce data transfer
- **Batch queries**: Combine multiple ZINC IDs in a single API call when possible

### Performance Considerations

- **Rate limiting**: Respect server resources; avoid rapid consecutive requests
- **Caching**: Store frequently accessed compounds locally
- **Parallel downloads**: When downloading 3D structures, use parallel wget or aria2c for file repositories
- **Subset filtering**: Use lead-like, drug-like, or fragment subsets to reduce search space

### Data Quality

- **Verify availability**: Supplier catalogs change; confirm compound availability before large orders
- **Check stereochemistry**: SMILES may not fully specify stereochemistry; verify 3D structures
- **Validate structures**: Use cheminformatics tools (RDKit, OpenBabel) to verify structure validity
- **Cross-reference**: When possible, cross-check with other databases (PubChem, ChEMBL)

## Resources

### references/api_reference.md

Comprehensive documentation including:

- Complete API endpoint reference
- URL syntax and parameter specifications
- Advanced query patterns and examples
- File repository organization and access
- Bulk download methods
- Error handling and troubleshooting
- Integration with molecular docking software

Consult this document for detailed technical information and advanced usage patterns.

## Important Disclaimers

### Data Reliability

ZINC explicitly states: **"We do not guarantee the quality of any molecule for any purpose and take no responsibility for errors arising from the use of this database."**

- Compound availability may change without notice
- Structure representations may contain errors
- Supplier information should be verified independently
- Use appropriate validation before experimental work

### Appropriate Use

- ZINC is intended for academic and research purposes in drug discovery
- Verify licensing terms for commercial use
- Respect intellectual property when working with patented compounds
- Follow your institution's guidelines for compound procurement

## Additional Resources

- **ZINC Website**: https://zinc.docking.org/
- **CartBlanche22 Interface**: https://cartblanche22.docking.org/
- **ZINC Wiki**: https://wiki.docking.org/
- **File Repository**: https://files.docking.org/zinc22/
- **GitHub**: https://github.com/docking-org/
- **Primary Publication**: Irwin et al., J. Chem. Inf. Model 2020 (ZINC15)
- **ZINC22 Publication**: Irwin et al., J. Chem. Inf. Model 2023

## Citations

When using ZINC in publications, cite the appropriate version:

**ZINC22**:
Irwin, J. J., et al. "ZINC22—A Free Multi-Billion-Scale Database of Tangible Compounds for Ligand Discovery." *Journal of Chemical Information and Modeling* 2023.

**ZINC15**:
Irwin, J. J., et al. "ZINC15 – Ligand Discovery for Everyone." *Journal of Chemical Information and Modeling* 2020, 60, 6065–6073.

---

## Reference: Api_Reference

# ZINC Database API Reference

## Overview

Complete technical reference for programmatic access to the ZINC database, covering API endpoints, query syntax, parameters, response formats, and advanced usage patterns for ZINC22, ZINC20, and legacy versions.

## Base URLs

### ZINC22 (Current)
- **CartBlanche22 API**: `https://cartblanche22.docking.org/`
- **File Repository**: `https://files.docking.org/zinc22/`
- **Main Website**: `https://zinc.docking.org/`

### ZINC20 (Maintained)
- **API**: `https://zinc20.docking.org/`
- **File Repository**: `https://files.docking.org/zinc20/`

### Documentation
- **Wiki**: `https://wiki.docking.org/`
- **GitHub**: `https://github.com/docking-org/`

## API Endpoints

### 1. Substance Retrieval by ZINC ID

Retrieve compound information using ZINC identifiers.

**Endpoint**: `/substances.txt`

**Parameters**:
- `zinc_id` (required): Single ZINC ID or comma-separated list
- `output_fields` (optional): Comma-separated field names (default: all fields)

**URL Format**:
```
https://cartblanche22.docking.org/substances.txt:zinc_id={ZINC_ID}&output_fields={FIELDS}
```

**Examples**:

Single compound:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=zinc_id,smiles,catalogs"
```

Multiple compounds:
```bash
curl "https://cartblanche22.docking.org/substances.txt:zinc_id=ZINC000000000001,ZINC000000000002,ZINC000000000003&output_fields=zinc_id,smiles,tranche"
```

Batch retrieval from file:
```bash
# Create file with ZINC IDs (one per line or comma-separated)
curl -X POST "https://cartblanche22.docking.org/substances.txt?output_fields=zinc_id,smiles" \
  -F "zinc_id=@zinc_ids.txt"
```

**Response Format** (TSV):
```
zinc_id	smiles	catalogs
ZINC000000000001	CC(C)O	[vendor1,vendor2]
ZINC000000000002	c1ccccc1	[vendor3]
```

### 2. Structure Search by SMILES

Search for compounds by chemical structure with optional similarity thresholds.

**Endpoint**: `/smiles.txt`

**Parameters**:
- `smiles` (required): Query SMILES string (URL-encode if necessary)
- `dist` (optional): Tanimoto distance threshold (0-10, default: 0 = exact)
- `adist` (optional): Alternative distance metric (0-10, default: 0)
- `output_fields` (optional): Comma-separated field names

**URL Format**:
```
https://cartblanche22.docking.org/smiles.txt:smiles={SMILES}&dist={DIST}&adist={ADIST}&output_fields={FIELDS}
```

**Examples**:

Exact structure match:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1&output_fields=zinc_id,smiles"
```

Similarity search (Tanimoto distance = 3):
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC(C)Cc1ccc(cc1)C(C)C(=O)O&dist=3&output_fields=zinc_id,smiles,catalogs"
```

Broad similarity search:
```bash
curl "https://cartblanche22.docking.org/smiles.txt:smiles=c1ccccc1&dist=5&adist=5&output_fields=zinc_id,smiles,tranche"
```

URL-encoded SMILES (for special characters):
```bash
# Original: CC(=O)Oc1ccccc1C(=O)O
# Encoded: CC%28%3DO%29Oc1ccccc1C%28%3DO%29O
curl "https://cartblanche22.docking.org/smiles.txt:smiles=CC%28%3DO%29Oc1ccccc1C%28%3DO%29O&dist=2"
```

**Distance Parameters Interpretation**:
- `dist=0`: Exact match
- `dist=1-3`: Close analogs (high similarity)
- `dist=4-6`: Moderate analogs
- `dist=7-10`: Diverse chemical space

### 3. Supplier Code Search

Query compounds by vendor catalog numbers.

**Endpoint**: `/catitems.txt`

**Parameters**:
- `catitem_id` (required): Supplier catalog code
- `output_fields` (optional): Comma-separated field names

**URL Format**:
```
https://cartblanche22.docking.org/catitems.txt:catitem_id={SUPPLIER_CODE}&output_fields={FIELDS}
```

**Example**:
```bash
curl "https://cartblanche22.docking.org/catitems.txt:catitem_id=SUPPLIER-12345&output_fields=zinc_id,smiles,supplier_code,catalogs"
```

### 4. Random Compound Sampling

Generate random compound sets with optional filtering by chemical properties.

**Endpoint**: `/substance/random.txt`

**Parameters**:
- `count` (optional): Number of compounds to retrieve (default: 100, max: depends on server)
- `subset` (optional): Filter by predefined subset (e.g., 'lead-like', 'drug-like', 'fragment')
- `output_fields` (optional): Comma-separated field names

**URL Format**:
```
https://cartblanche22.docking.org/substance/random.txt:count={COUNT}&subset={SUBSET}&output_fields={FIELDS}
```

**Examples**:

Random 100 compounds (default):
```bash
curl "https://cartblanche22.docking.org/substance/random.txt"
```

Random lead-like molecules:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=1000&subset=lead-like&output_fields=zinc_id,smiles,tranche"
```

Random drug-like molecules:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=5000&subset=drug-like&output_fields=zinc_id,smiles"
```

Random fragments:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt:count=500&subset=fragment&output_fields=zinc_id,smiles,tranche"
```

**Subset Definitions**:
- `fragment`: MW < 250, suitable for fragment-based drug discovery
- `lead-like`: MW 250-350, LogP ≤ 3.5, rotatable bonds ≤ 7
- `drug-like`: MW 350-500, follows Lipinski's Rule of Five
- `lugs`: Large, unusually good subset (highly curated)

## Output Fields

### Available Fields

Customize API responses using the `output_fields` parameter:

| Field | Description | Example |
|-------|-------------|---------|
| `zinc_id` | ZINC identifier | ZINC000000000001 |
| `smiles` | Canonical SMILES string | CC(C)O |
| `sub_id` | Internal substance ID | 123456 |
| `supplier_code` | Vendor catalog number | AB-1234567 |
| `catalogs` | List of suppliers | [emolecules, mcule, mcule-ultimate] |
| `tranche` | Encoded molecular properties | H02P025M300-0 |
| `mwt` | Molecular weight | 325.45 |
| `logp` | LogP (partition coefficient) | 2.5 |
| `hba` | H-bond acceptors | 4 |
| `hbd` | H-bond donors | 2 |
| `rotatable_bonds` | Rotatable bonds count | 5 |

**Note**: Not all fields are available for all endpoints. Field availability depends on the database version and endpoint.

### Default Fields

If `output_fields` is not specified, endpoints return all available fields in TSV format.

### Custom Field Selection

Request specific fields only:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=zinc_id,smiles"
```

Request multiple fields:
```bash
curl "https://cartblanche22.docking.org/[email protected]_fields=zinc_id,smiles,tranche,catalogs"
```

## Tranche System

ZINC organizes compounds into tranches based on molecular properties for efficient filtering and organization.

### Tranche Code Format

**Pattern**: `H##P###M###-phase`

| Component | Description | Range |
|-----------|-------------|-------|
| H## | Hydrogen bond donors | 00-99 |
| P### | LogP × 10 | 000-999 (e.g., P035 = LogP 3.5) |
| M### | Molecular weight | 000-999 Da |
| phase | Reactivity classification | 0-9 |

### Examples

| Tranche Code | Interpretation |
|--------------|----------------|
| `H00P010M250-0` | 0 H-donors, LogP=1.0, MW=250 Da, phase 0 |
| `H05P035M400-0` | 5 H-donors, LogP=3.5, MW=400 Da, phase 0 |
| `H02P-005M180-0` | 2 H-donors, LogP=-0.5, MW=180 Da, phase 0 |

### Reactivity Phases

| Phase | Description |
|-------|-------------|
| 0 | Unreactive (preferred for screening) |
| 1-9 | Increasing reactivity (PAINS, reactive groups) |

### Parsing Tranches in Python

```python
import re

def parse_tranche(tranche_str):
    """
    Parse ZINC tranche code.

    Args:
        tranche_str: Tranche code (e.g., "H05P035M400-0")

    Returns:
        dict with h_donors, logp, mw, phase
    """
    pattern = r'H(\d+)P(-?\d+)M(\d+)-(\d+)'
    match = re.match(pattern, tranche_str)

    if not match:
        return None

    return {
        'h_donors': int(match.group(1)),
        'logp': int(match.group(2)) / 10.0,
        'mw': int(match.group(3)),
        'phase': int(match.group(4))
    }

# Example usage
tranche = "H05P035M400-0"
props = parse_tranche(tranche)
print(props)  # {'h_donors': 5, 'logp': 3.5, 'mw': 400, 'phase': 0}
```

### Filtering by Tranches

Download specific tranches from file repositories:
```bash
# Download all compounds in a specific tranche
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
```

## File Repository Access

### Directory Structure

ZINC22 3D structures are organized hierarchically by H-bond donors:

```
https://files.docking.org/zinc22/
├── H00/
│   ├── H00P010M200-0.db2.gz
│   ├── H00P020M250-0.db2.gz
│   └── ...
├── H01/
├── H02/
└── ...
```

### File Formats

| Extension | Format | Description |
|-----------|--------|-------------|
| `.db2.gz` | DOCK database | Compressed multi-conformer DB for DOCK |
| `.mol2.gz` | MOL2 | Multi-molecule format with 3D coordinates |
| `.sdf.gz` | SDF | Structure-Data File format |
| `.smi` | SMILES | Plain text SMILES with ZINC IDs |

### Downloading 3D Structures

**Single tranche**:
```bash
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
```

**Multiple tranches** (parallel download with aria2c):
```bash
# Create URL list
cat > tranche_urls.txt <<EOF
https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
https://files.docking.org/zinc22/H05/H05P040M400-0.db2.gz
EOF

# Download in parallel
aria2c -i tranche_urls.txt -x 8 -j 4
```

**Recursive download** (use with caution - large data):
```bash
wget -r -np -nH --cut-dirs=1 -A "*.db2.gz" \
  https://files.docking.org/zinc22/H05/
```

### Extracting Structures

```bash
# Decompress
gunzip H05P035M400-0.db2.gz

# Convert to other formats using OpenBabel
obabel H05P035M400-0.db2 -O output.sdf
obabel H05P035M400-0.db2 -O output.mol2
```

## Advanced Query Patterns

### Combining Multiple Search Criteria

**Python wrapper for complex queries**:

```python
import subprocess
import pandas as pd
from io import StringIO

def advanced_zinc_search(smiles=None, zinc_ids=None, dist=0,
                         subset=None, count=None, output_fields=None):
    """
    Flexible ZINC search with multiple criteria.

    Args:
        smiles: SMILES string for structure search
        zinc_ids: List of ZINC IDs for batch retrieval
        dist: Distance parameter for similarity (0-10)
        subset: Subset filter (lead-like, drug-like, fragment)
        count: Number of random compounds
        output_fields: List of fields to return

    Returns:
        pandas DataFrame with results
    """
    if output_fields is None:
        output_fields = ['zinc_id', 'smiles', 'tranche', 'catalogs']

    fields_str = ','.join(output_fields)

    # Structure search
    if smiles:
        url = f"https://cartblanche22.docking.org/smiles.txt:smiles={smiles}&dist={dist}&output_fields={fields_str}"

    # Batch retrieval
    elif zinc_ids:
        zinc_ids_str = ','.join(zinc_ids)
        url = f"https://cartblanche22.docking.org/substances.txt:zinc_id={zinc_ids_str}&output_fields={fields_str}"

    # Random sampling
    elif count:
        url = f"https://cartblanche22.docking.org/substance/random.txt:count={count}&output_fields={fields_str}"
        if subset:
            url += f"&subset={subset}"

    else:
        raise ValueError("Must specify smiles, zinc_ids, or count")

    # Execute query
    result = subprocess.run(['curl', '-s', url],
                          capture_output=True, text=True)

    # Parse to DataFrame
    df = pd.read_csv(StringIO(result.stdout), sep='\t')

    return df
```

**Usage examples**:

```python
# Find similar compounds
df = advanced_zinc_search(
    smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    dist=3,
    output_fields=['zinc_id', 'smiles', 'catalogs']
)

# Batch retrieval
zinc_ids = ["ZINC000000000001", "ZINC000000000002"]
df = advanced_zinc_search(zinc_ids=zinc_ids)

# Random drug-like set
df = advanced_zinc_search(
    count=1000,
    subset='drug-like',
    output_fields=['zinc_id', 'smiles', 'tranche']
)
```

### Property-Based Filtering

Filter compounds by molecular properties using tranche data:

```python
def filter_by_properties(df, mw_range=None, logp_range=None,
                        max_hbd=None, phase=0):
    """
    Filter DataFrame by molecular properties.

    Args:
        df: DataFrame with 'tranche' column
        mw_range: Tuple (min_mw, max_mw)
        logp_range: Tuple (min_logp, max_logp)
        max_hbd: Maximum H-bond donors
        phase: Reactivity phase (0 = unreactive)

    Returns:
        Filtered DataFrame
    """
    # Parse tranches
    df['tranche_props'] = df['tranche'].apply(parse_tranche)
    df['mw'] = df['tranche_props'].apply(lambda x: x['mw'] if x else None)
    df['logp'] = df['tranche_props'].apply(lambda x: x['logp'] if x else None)
    df['hbd'] = df['tranche_props'].apply(lambda x: x['h_donors'] if x else None)
    df['phase'] = df['tranche_props'].apply(lambda x: x['phase'] if x else None)

    # Apply filters
    mask = pd.Series([True] * len(df))

    if mw_range:
        mask &= (df['mw'] >= mw_range[0]) & (df['mw'] <= mw_range[1])

    if logp_range:
        mask &= (df['logp'] >= logp_range[0]) & (df['logp'] <= logp_range[1])

    if max_hbd is not None:
        mask &= df['hbd'] <= max_hbd

    if phase is not None:
        mask &= df['phase'] == phase

    return df[mask]

# Example: Get drug-like compounds with specific properties
df = advanced_zinc_search(count=10000, subset='drug-like')
filtered = filter_by_properties(
    df,
    mw_range=(300, 450),
    logp_range=(1.0, 4.0),
    max_hbd=3,
    phase=0
)
```

## Rate Limiting and Best Practices

### Rate Limiting

ZINC does not publish explicit rate limits, but users should:

- **Avoid rapid-fire requests**: Space out queries by at least 1 second
- **Use batch operations**: Query multiple ZINC IDs in single request
- **Cache results**: Store frequently accessed data locally
- **Off-peak usage**: Perform large downloads during off-peak hours (UTC nights/weekends)

### Etiquette

```python
import time

def polite_zinc_query(query_func, *args, delay=1.0, **kwargs):
    """Wrapper to add delay between queries."""
    result = query_func(*args, **kwargs)
    time.sleep(delay)
    return result
```

### Error Handling

```python
def robust_zinc_query(url, max_retries=3, timeout=30):
    """
    Query ZINC with retry logic.

    Args:
        url: Full ZINC API URL
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Query results or None on failure
    """
    import subprocess
    import time

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['curl', '-s', '--max-time', str(timeout), url],
                capture_output=True,
                text=True,
                check=True
            )

            # Check for empty or error responses
            if not result.stdout or 'error' in result.stdout.lower():
                raise ValueError("Invalid response")

            return result.stdout

        except (subprocess.CalledProcessError, ValueError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts")
                return None
```

## Integration with Molecular Docking

### Preparing DOCK6 Libraries

```bash
# 1. Download tranche files
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz

# 2. Decompress
gunzip H05P035M400-0.db2.gz

# 3. Use directly with DOCK6
dock6 -i dock.in -o dock.out -l H05P035M400-0.db2
```

### AutoDock Vina Integration

```bash
# 1. Download MOL2 format
wget https://files.docking.org/zinc22/H05/H05P035M400-0.mol2.gz
gunzip H05P035M400-0.mol2.gz

# 2. Convert to PDBQT using prepare_ligand script
prepare_ligand4.py -l H05P035M400-0.mol2 -o ligands.pdbqt -A hydrogens

# 3. Run Vina
vina --receptor protein.pdbqt --ligand ligands.pdbqt \
     --center_x 25.0 --center_y 25.0 --center_z 25.0 \
     --size_x 20.0 --size_y 20.0 --size_z 20.0
```

### RDKit Integration

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import pandas as pd

def process_zinc_results(zinc_df):
    """
    Process ZINC results with RDKit.

    Args:
        zinc_df: DataFrame with SMILES column

    Returns:
        DataFrame with calculated properties
    """
    # Convert SMILES to molecules
    zinc_df['mol'] = zinc_df['smiles'].apply(Chem.MolFromSmiles)

    # Calculate properties
    zinc_df['mw'] = zinc_df['mol'].apply(Descriptors.MolWt)
    zinc_df['logp'] = zinc_df['mol'].apply(Descriptors.MolLogP)
    zinc_df['hbd'] = zinc_df['mol'].apply(Descriptors.NumHDonors)
    zinc_df['hba'] = zinc_df['mol'].apply(Descriptors.NumHAcceptors)
    zinc_df['tpsa'] = zinc_df['mol'].apply(Descriptors.TPSA)
    zinc_df['rotatable'] = zinc_df['mol'].apply(Descriptors.NumRotatableBonds)

    # Generate 3D conformers
    for mol in zinc_df['mol']:
        if mol:
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)

    return zinc_df

# Save to SDF for docking
def save_to_sdf(zinc_df, output_file):
    """Save molecules to SDF file."""
    writer = Chem.SDWriter(output_file)
    for idx, row in zinc_df.iterrows():
        if row['mol']:
            row['mol'].SetProp('ZINC_ID', row['zinc_id'])
            writer.write(row['mol'])
    writer.close()
```

## Troubleshooting

### Common Issues

**Issue**: Empty or no results
- **Solution**: Check SMILES syntax, verify ZINC IDs exist, try broader similarity search

**Issue**: Timeout errors
- **Solution**: Reduce result count, use batch queries, try during off-peak hours

**Issue**: Invalid SMILES encoding
- **Solution**: URL-encode special characters (use `urllib.parse.quote()` in Python)

**Issue**: Tranche files not found
- **Solution**: Verify tranche code format, check file repository structure

### Debug Mode

```python
def debug_zinc_query(url):
    """Print query details for debugging."""
    print(f"Query URL: {url}")

    result = subprocess.run(['curl', '-v', url],
                          capture_output=True, text=True)

    print(f"Status: {result.returncode}")
    print(f"Stderr: {result.stderr}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"First 500 chars:\n{result.stdout[:500]}")

    return result.stdout
```

## Version Differences

### ZINC22 vs ZINC20 vs ZINC15

| Feature | ZINC22 | ZINC20 | ZINC15 |
|---------|--------|--------|--------|
| Compounds | 230M+ purchasable | Focused on leads | ~750M total |
| API | CartBlanche22 | Similar | REST-like |
| Tranches | Yes | Yes | Yes |
| 3D Structures | Yes | Yes | Yes |
| Status | Current, growing | Maintained | Legacy |

### API Compatibility

Most query patterns work across versions, but URLs differ:
- ZINC22: `cartblanche22.docking.org`
- ZINC20: `zinc20.docking.org`
- ZINC15: `zinc15.docking.org`

## Additional Resources

- **ZINC Wiki**: https://wiki.docking.org/
- **ZINC22 Documentation**: https://wiki.docking.org/index.php/Category:ZINC22
- **ZINC API Guide**: https://wiki.docking.org/index.php/ZINC_api
- **File Access Guide**: https://wiki.docking.org/index.php/ZINC22:Getting_started
- **Publications**:
  - ZINC22: J. Chem. Inf. Model. 2023
  - ZINC15: J. Chem. Inf. Model. 2020, 60, 6065-6073
- **Support**: Contact via ZINC website or GitHub issues
