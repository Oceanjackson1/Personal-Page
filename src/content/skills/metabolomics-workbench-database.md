---
title: "Metabolomics Workbench Database"
description: "Access NIH Metabolomics Workbench via REST API (4,200+ studies). Query metabolites, RefMet nomenclature, MS/NMR data, m/z searches, study metadata, for metabolomics and biomarker discovery."
category: "research"
source: "community"
author: "Community"
tags: ["metabolomics", "workbench", "database"]
date: 2026-03-20
---

# Metabolomics Workbench Database

## Overview

The Metabolomics Workbench is a comprehensive NIH Common Fund-sponsored platform hosted at UCSD that serves as the primary repository for metabolomics research data. It provides programmatic access to over 4,200 processed studies (3,790+ publicly available), standardized metabolite nomenclature through RefMet, and powerful search capabilities across multiple analytical platforms (GC-MS, LC-MS, NMR).

## When to Use This Skill

This skill should be used when querying metabolite structures, accessing study data, standardizing nomenclature, performing mass spectrometry searches, or retrieving gene/protein-metabolite associations through the Metabolomics Workbench REST API.

## Core Capabilities

### 1. Querying Metabolite Structures and Data

Access comprehensive metabolite information including structures, identifiers, and cross-references to external databases.

**Key operations:**
- Retrieve compound data by various identifiers (PubChem CID, InChI Key, KEGG ID, HMDB ID, etc.)
- Download molecular structures as MOL files or PNG images
- Access standardized compound classifications
- Cross-reference between different metabolite databases

**Example queries:**
```python
import requests

# Get compound information by PubChem CID
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/pubchem_cid/5281365/all/json')

# Download molecular structure as PNG
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/png')

# Get compound name by registry number
response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/11/name/json')
```

### 2. Accessing Study Metadata and Experimental Results

Query metabolomics studies by various criteria and retrieve complete experimental datasets.

**Key operations:**
- Search studies by metabolite, institute, investigator, or title
- Access study summaries, experimental factors, and analysis details
- Retrieve complete experimental data in various formats
- Download mwTab format files for complete study information
- Query untargeted metabolomics data

**Example queries:**
```python
# List all available public studies
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST/available/json')

# Get study summary
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/summary/json')

# Retrieve experimental data
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/data/json')

# Find studies containing a specific metabolite
response = requests.get('https://www.metabolomicsworkbench.org/rest/study/refmet_name/Tyrosine/summary/json')
```

### 3. Standardizing Metabolite Nomenclature with RefMet

Use the RefMet database to standardize metabolite names and access systematic classification across four structural resolution levels.

**Key operations:**
- Match common metabolite names to standardized RefMet names
- Query by chemical formula, exact mass, or InChI Key
- Access hierarchical classification (super class, main class, sub class)
- Retrieve all RefMet entries or filter by classification

**Example queries:**
```python
# Standardize a metabolite name
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/match/citrate/name/json')

# Query by molecular formula
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/formula/C12H24O2/all/json')

# Get all metabolites in a specific class
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/main_class/Fatty%20Acids/all/json')

# Retrieve complete RefMet database
response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/all/json')
```

### 4. Performing Mass Spectrometry Searches

Search for compounds by mass-to-charge ratio (m/z) with specified ion adducts and tolerance levels.

**Key operations:**
- Search precursor ion masses across multiple databases (Metabolomics Workbench, LIPIDS, RefMet)
- Specify ion adduct types (M+H, M-H, M+Na, M+NH4, M+2H, etc.)
- Calculate exact masses for known metabolites with specific adducts
- Set mass tolerance for flexible matching

**Example queries:**
```python
# Search by m/z value with M+H adduct
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/MB/635.52/M+H/0.5/json')

# Calculate exact mass for a metabolite with specific adduct
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/exactmass/PC(34:1)/M+H/json')

# Search across RefMet database
response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/REFMET/200.15/M-H/0.3/json')
```

### 5. Filtering Studies by Analytical and Biological Parameters

Use the MetStat context to find studies matching specific experimental conditions.

**Key operations:**
- Filter by analytical method (LCMS, GCMS, NMR)
- Specify ionization polarity (POSITIVE, NEGATIVE)
- Filter by chromatography type (HILIC, RP, GC)
- Target specific species, sample sources, or diseases
- Combine multiple filters using semicolon-delimited format

**Example queries:**
```python
# Find human blood studies on diabetes using LC-MS
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/LCMS;POSITIVE;HILIC;Human;Blood;Diabetes/json')

# Find all human blood studies containing tyrosine
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/;;;Human;Blood;;;Tyrosine/json')

# Filter by analytical method only
response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/GCMS;;;;;;/json')
```

### 6. Accessing Gene and Protein Information

Retrieve gene and protein data associated with metabolic pathways and metabolite metabolism.

**Key operations:**
- Query genes by symbol, name, or ID
- Access protein sequences and annotations
- Cross-reference between gene IDs, RefSeq IDs, and UniProt IDs
- Retrieve gene-metabolite associations

**Example queries:**
```python
# Get gene information by symbol
response = requests.get('https://www.metabolomicsworkbench.org/rest/gene/gene_symbol/ACACA/all/json')

# Retrieve protein data by UniProt ID
response = requests.get('https://www.metabolomicsworkbench.org/rest/protein/uniprot_id/Q13085/all/json')
```

## Common Workflows

### Workflow 1: Finding Studies for a Specific Metabolite

To find all studies containing measurements of a specific metabolite:

1. First standardize the metabolite name using RefMet:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/refmet/match/glucose/name/json')
   ```

2. Use the standardized name to search for studies:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/refmet_name/Glucose/summary/json')
   ```

3. Retrieve experimental data from specific studies:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/data/json')
   ```

### Workflow 2: Identifying Compounds from MS Data

To identify potential compounds from mass spectrometry m/z values:

1. Perform m/z search with appropriate adduct and tolerance:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/moverz/MB/180.06/M+H/0.5/json')
   ```

2. Review candidate compounds from results

3. Retrieve detailed information for candidate compounds:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/{regno}/all/json')
   ```

4. Download structures for confirmation:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/compound/regno/{regno}/png')
   ```

### Workflow 3: Exploring Disease-Specific Metabolomics

To find metabolomics studies for a specific disease and analytical platform:

1. Use MetStat to filter studies:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/metstat/LCMS;POSITIVE;;Human;;Cancer/json')
   ```

2. Review study IDs from results

3. Access detailed study information:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST{ID}/summary/json')
   ```

4. Retrieve complete experimental data:
   ```python
   response = requests.get('https://www.metabolomicsworkbench.org/rest/study/study_id/ST{ID}/data/json')
   ```

## Output Formats

The API supports two primary output formats:
- **JSON** (default): Machine-readable format, ideal for programmatic access
- **TXT**: Human-readable tab-delimited text format

Specify format by appending `/json` or `/txt` to API URLs. When format is omitted, JSON is returned by default.

## Best Practices

1. **Use RefMet for standardization**: Always standardize metabolite names through RefMet before searching studies to ensure consistent nomenclature

2. **Specify appropriate adducts**: When performing m/z searches, use the correct ion adduct type for your analytical method (e.g., M+H for positive mode ESI)

3. **Set reasonable tolerances**: Use appropriate mass tolerance values (typically 0.5 Da for low-resolution, 0.01 Da for high-resolution MS)

4. **Cache reference data**: Consider caching frequently used reference data (RefMet database, compound information) to minimize API calls

5. **Handle pagination**: For large result sets, be prepared to handle multiple data structures in responses

6. **Validate identifiers**: Cross-reference metabolite identifiers across multiple databases when possible to ensure correct compound identification

## Resources

### references/

Detailed API reference documentation is available in `references/api_reference.md`, including:
- Complete REST API endpoint specifications
- All available contexts (compound, study, refmet, metstat, gene, protein, moverz)
- Input/output parameter details
- Ion adduct types for mass spectrometry
- Additional query examples

Load this reference file when detailed API specifications are needed or when working with less common endpoints.

---

## Reference: Api_Reference

# Metabolomics Workbench REST API Reference

## Base URL

All API requests use the following base URL:
```
https://www.metabolomicsworkbench.org/rest/
```

## API Structure

The REST API follows a consistent URL pattern:
```
/context/input_item/input_value/output_item/output_format
```

- **context**: The type of resource to access (study, compound, refmet, metstat, gene, protein, moverz)
- **input_item**: The type of identifier or search parameter
- **input_value**: The specific value to search for
- **output_item**: What data to return (e.g., all, name, summary)
- **output_format**: json or txt (json is default if omitted)

## Output Formats

- **json**: Machine-readable JSON format (default)
- **txt**: Tab-delimited text format for human readability

## Context 1: Compound

Retrieve metabolite structure and identification data.

### Input Items

| Input Item | Description | Example |
|------------|-------------|---------|
| `regno` | Metabolomics Workbench registry number | 11 |
| `pubchem_cid` | PubChem Compound ID | 5281365 |
| `inchi_key` | International Chemical Identifier Key | WQZGKKKJIJFFOK-GASJEMHNSA-N |
| `formula` | Molecular formula | C6H12O6 |
| `lm_id` | LIPID MAPS ID | LM... |
| `hmdb_id` | Human Metabolome Database ID | HMDB0000122 |
| `kegg_id` | KEGG Compound ID | C00031 |

### Output Items

| Output Item | Description |
|-------------|-------------|
| `all` | All available compound data |
| `classification` | Compound classification |
| `regno` | Registry number |
| `formula` | Molecular formula |
| `exactmass` | Exact mass |
| `inchi_key` | InChI Key |
| `name` | Common name |
| `sys_name` | Systematic name |
| `smiles` | SMILES notation |
| `lm_id` | LIPID MAPS ID |
| `pubchem_cid` | PubChem CID |
| `hmdb_id` | HMDB ID |
| `kegg_id` | KEGG ID |
| `chebi_id` | ChEBI ID |
| `metacyc_id` | MetaCyc ID |
| `molfile` | MOL file structure |
| `png` | PNG image of structure |

### Example Requests

```bash
# Get all compound data by PubChem CID
curl "https://www.metabolomicsworkbench.org/rest/compound/pubchem_cid/5281365/all/json"

# Get compound name by registry number
curl "https://www.metabolomicsworkbench.org/rest/compound/regno/11/name/json"

# Download structure as PNG
curl "https://www.metabolomicsworkbench.org/rest/compound/regno/11/png" -o structure.png

# Get compound by KEGG ID
curl "https://www.metabolomicsworkbench.org/rest/compound/kegg_id/C00031/all/json"

# Get compound by molecular formula
curl "https://www.metabolomicsworkbench.org/rest/compound/formula/C6H12O6/all/json"
```

## Context 2: Study

Access metabolomics research study metadata and experimental results.

### Input Items

| Input Item | Description | Example |
|------------|-------------|---------|
| `study_id` | Study identifier | ST000001 |
| `analysis_id` | Analysis identifier | AN000001 |
| `study_title` | Keywords in study title | diabetes |
| `institute` | Institute name | UCSD |
| `last_name` | Investigator last name | Smith |
| `metabolite_id` | Metabolite registry number | 11 |
| `refmet_name` | RefMet standardized name | Glucose |
| `kegg_id` | KEGG compound ID | C00031 |

### Output Items

| Output Item | Description |
|-------------|-------------|
| `summary` | Study overview and metadata |
| `factors` | Experimental factors and design |
| `analysis` | Analysis methods and parameters |
| `metabolites` | List of measured metabolites |
| `data` | Complete experimental data |
| `mwtab` | Complete study in mwTab format |
| `number_of_metabolites` | Count of metabolites measured |
| `species` | Organism species |
| `disease` | Disease studied |
| `source` | Sample source/tissue type |
| `untarg_studies` | Untargeted study information |
| `untarg_factors` | Untargeted study factors |
| `untarg_data` | Untargeted experimental data |
| `datatable` | Formatted data table |
| `available` | List available studies (use with ST as input_value) |

### Example Requests

```bash
# List all publicly available studies
curl "https://www.metabolomicsworkbench.org/rest/study/study_id/ST/available/json"

# Get study summary
curl "https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/summary/json"

# Get experimental data
curl "https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/data/json"

# Get study factors
curl "https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/factors/json"

# Find studies containing a specific metabolite
curl "https://www.metabolomicsworkbench.org/rest/study/refmet_name/Tyrosine/summary/json"

# Search studies by investigator
curl "https://www.metabolomicsworkbench.org/rest/study/last_name/Smith/summary/json"

# Download complete study in mwTab format
curl "https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/mwtab/txt"
```

## Context 3: RefMet

Query the standardized metabolite nomenclature database with hierarchical classification.

### Input Items

| Input Item | Description | Example |
|------------|-------------|---------|
| `name` | Metabolite name | glucose |
| `inchi_key` | InChI Key | WQZGKKKJIJFFOK-GASJEMHNSA-N |
| `pubchem_cid` | PubChem CID | 5793 |
| `exactmass` | Exact mass | 180.0634 |
| `formula` | Molecular formula | C6H12O6 |
| `super_class` | Super class name | Organic compounds |
| `main_class` | Main class name | Carbohydrates |
| `sub_class` | Sub class name | Monosaccharides |
| `match` | Name matching/standardization | citrate |
| `refmet_id` | RefMet identifier | 12345 |
| `all` | Retrieve all RefMet entries | (no value needed) |

### Output Items

| Output Item | Description |
|-------------|-------------|
| `all` | All available RefMet data |
| `name` | Standardized RefMet name |
| `inchi_key` | InChI Key |
| `pubchem_cid` | PubChem CID |
| `exactmass` | Exact mass |
| `formula` | Molecular formula |
| `sys_name` | Systematic name |
| `super_class` | Super class classification |
| `main_class` | Main class classification |
| `sub_class` | Sub class classification |
| `refmet_id` | RefMet identifier |

### Example Requests

```bash
# Standardize a metabolite name
curl "https://www.metabolomicsworkbench.org/rest/refmet/match/citrate/name/json"

# Get all RefMet data for a metabolite
curl "https://www.metabolomicsworkbench.org/rest/refmet/name/Glucose/all/json"

# Query by molecular formula
curl "https://www.metabolomicsworkbench.org/rest/refmet/formula/C6H12O6/all/json"

# Get all metabolites in a main class
curl "https://www.metabolomicsworkbench.org/rest/refmet/main_class/Fatty%20Acids/all/json"

# Query by exact mass
curl "https://www.metabolomicsworkbench.org/rest/refmet/exactmass/180.0634/all/json"

# Download complete RefMet database
curl "https://www.metabolomicsworkbench.org/rest/refmet/all/json"
```

### RefMet Classification Hierarchy

RefMet provides four-level structural resolution:

1. **Super Class**: Broadest categorization (e.g., "Organic compounds", "Lipids")
2. **Main Class**: Major biochemical categories (e.g., "Fatty Acids", "Carbohydrates")
3. **Sub Class**: More specific groupings (e.g., "Monosaccharides", "Amino acids")
4. **Individual Metabolite**: Specific compound with standardized name

## Context 4: MetStat

Filter studies by analytical and biological parameters using semicolon-delimited format.

### Format

```
/metstat/ANALYSIS_TYPE;POLARITY;CHROMATOGRAPHY;SPECIES;SAMPLE_SOURCE;DISEASE;KEGG_ID;REFMET_NAME
```

### Parameters

| Position | Parameter | Options |
|----------|-----------|---------|
| 1 | Analysis Type | LCMS, GCMS, NMR, MS, ICPMS |
| 2 | Polarity | POSITIVE, NEGATIVE |
| 3 | Chromatography | HILIC, RP (Reverse Phase), GC, IC |
| 4 | Species | Human, Mouse, Rat, etc. |
| 5 | Sample Source | Blood, Plasma, Serum, Urine, Liver, etc. |
| 6 | Disease | Diabetes, Cancer, Alzheimer, etc. |
| 7 | KEGG ID | C00031, etc. |
| 8 | RefMet Name | Glucose, Tyrosine, etc. |

**Note**: Use empty positions (consecutive semicolons) to skip parameters. All parameters are optional.

### Example Requests

```bash
# Human blood diabetes studies with LC-MS HILIC positive mode
curl "https://www.metabolomicsworkbench.org/rest/metstat/LCMS;POSITIVE;HILIC;Human;Blood;Diabetes/json"

# All human blood studies containing tyrosine
curl "https://www.metabolomicsworkbench.org/rest/metstat/;;;Human;Blood;;;Tyrosine/json"

# All GC-MS studies regardless of other parameters
curl "https://www.metabolomicsworkbench.org/rest/metstat/GCMS;;;;;;/json"

# Mouse liver studies
curl "https://www.metabolomicsworkbench.org/rest/metstat/;;;Mouse;Liver;;/json"

# All studies measuring glucose
curl "https://www.metabolomicsworkbench.org/rest/metstat/;;;;;;;Glucose/json"
```

## Context 5: Moverz

Perform mass spectrometry precursor ion searches by m/z value.

### Format for m/z Search

```
/moverz/DATABASE/mass/adduct/tolerance/format
```

- **DATABASE**: MB (Metabolomics Workbench), LIPIDS, REFMET
- **mass**: m/z value (e.g., 635.52)
- **adduct**: Ion adduct type (see table below)
- **tolerance**: Mass tolerance in Daltons (e.g., 0.5)
- **format**: json or txt

### Format for Exact Mass Calculation

```
/moverz/exactmass/metabolite_name/adduct/format
```

### Ion Adduct Types

#### Positive Mode Adducts

| Adduct | Description | Example Use |
|--------|-------------|-------------|
| `M+H` | Protonated molecule | Most common positive ESI |
| `M+Na` | Sodium adduct | Common in ESI |
| `M+K` | Potassium adduct | Less common ESI |
| `M+NH4` | Ammonium adduct | Common with ammonium salts |
| `M+2H` | Doubly protonated | Multiply charged ions |
| `M+H-H2O` | Dehydrated protonated | Loss of water |
| `M+2Na-H` | Disodium minus hydrogen | Multiple sodium |
| `M+CH3OH+H` | Methanol adduct | Methanol in mobile phase |
| `M+ACN+H` | Acetonitrile adduct | ACN in mobile phase |
| `M+ACN+Na` | ACN + sodium | ACN and sodium |

#### Negative Mode Adducts

| Adduct | Description | Example Use |
|--------|-------------|-------------|
| `M-H` | Deprotonated molecule | Most common negative ESI |
| `M+Cl` | Chloride adduct | Chlorinated mobile phases |
| `M+FA-H` | Formate adduct | Formic acid in mobile phase |
| `M+HAc-H` | Acetate adduct | Acetic acid in mobile phase |
| `M-H-H2O` | Deprotonated minus water | Water loss |
| `M-2H` | Doubly deprotonated | Multiply charged ions |
| `M+Na-2H` | Sodium minus two protons | Mixed charge states |

#### Uncharged

| Adduct | Description |
|--------|-------------|
| `M` | Uncharged molecule | Direct ionization methods |

### Example Requests

```bash
# Search for compounds with m/z 635.52 (M+H) in MB database
curl "https://www.metabolomicsworkbench.org/rest/moverz/MB/635.52/M+H/0.5/json"

# Search in RefMet with negative mode
curl "https://www.metabolomicsworkbench.org/rest/moverz/REFMET/200.15/M-H/0.3/json"

# Search lipids database
curl "https://www.metabolomicsworkbench.org/rest/moverz/LIPIDS/760.59/M+Na/0.5/json"

# Calculate exact mass for known metabolite
curl "https://www.metabolomicsworkbench.org/rest/moverz/exactmass/PC(34:1)/M+H/json"

# High-resolution MS search (tight tolerance)
curl "https://www.metabolomicsworkbench.org/rest/moverz/MB/180.0634/M+H/0.01/json"
```

## Context 6: Gene

Access gene information from the Metabolome Gene/Protein (MGP) database.

### Input Items

| Input Item | Description | Example |
|------------|-------------|---------|
| `mgp_id` | MGP database ID | MGP001 |
| `gene_id` | NCBI Gene ID | 31 |
| `gene_name` | Full gene name | acetyl-CoA carboxylase |
| `gene_symbol` | Gene symbol | ACACA |
| `taxid` | Taxonomy ID | 9606 (human) |

### Output Items

| Output Item | Description |
|-------------|-------------|
| `all` | All gene information |
| `mgp_id` | MGP identifier |
| `gene_id` | NCBI Gene ID |
| `gene_name` | Full gene name |
| `gene_symbol` | Gene symbol |
| `gene_synonyms` | Alternative names |
| `alt_names` | Alternative nomenclature |
| `chromosome` | Chromosomal location |
| `map_location` | Genetic map position |
| `summary` | Gene description |
| `taxid` | Taxonomy ID |
| `species` | Species short name |
| `species_long` | Full species name |

### Example Requests

```bash
# Get gene information by symbol
curl "https://www.metabolomicsworkbench.org/rest/gene/gene_symbol/ACACA/all/json"

# Get gene by NCBI Gene ID
curl "https://www.metabolomicsworkbench.org/rest/gene/gene_id/31/all/json"

# Search by gene name
curl "https://www.metabolomicsworkbench.org/rest/gene/gene_name/carboxylase/summary/json"
```

## Context 7: Protein

Retrieve protein sequence and annotation data.

### Input Items

| Input Item | Description | Example |
|------------|-------------|---------|
| `mgp_id` | MGP database ID | MGP001 |
| `gene_id` | NCBI Gene ID | 31 |
| `gene_name` | Gene name | acetyl-CoA carboxylase |
| `gene_symbol` | Gene symbol | ACACA |
| `taxid` | Taxonomy ID | 9606 |
| `mrna_id` | mRNA identifier | NM_001093.3 |
| `refseq_id` | RefSeq ID | NP_001084 |
| `protein_gi` | GenInfo Identifier | 4557237 |
| `uniprot_id` | UniProt ID | Q13085 |
| `protein_entry` | Protein entry name | ACACA_HUMAN |
| `protein_name` | Protein name | Acetyl-CoA carboxylase |

### Output Items

| Output Item | Description |
|-------------|-------------|
| `all` | All protein information |
| `mgp_id` | MGP identifier |
| `gene_id` | NCBI Gene ID |
| `gene_name` | Gene name |
| `gene_symbol` | Gene symbol |
| `taxid` | Taxonomy ID |
| `species` | Species short name |
| `species_long` | Full species name |
| `mrna_id` | mRNA identifier |
| `refseq_id` | RefSeq protein ID |
| `protein_gi` | GenInfo Identifier |
| `uniprot_id` | UniProt accession |
| `protein_entry` | Protein entry name |
| `protein_name` | Full protein name |
| `seqlength` | Sequence length |
| `seq` | Amino acid sequence |
| `is_identical_to` | Identical sequences |

### Example Requests

```bash
# Get protein information by UniProt ID
curl "https://www.metabolomicsworkbench.org/rest/protein/uniprot_id/Q13085/all/json"

# Get protein by gene symbol
curl "https://www.metabolomicsworkbench.org/rest/protein/gene_symbol/ACACA/all/json"

# Get protein sequence
curl "https://www.metabolomicsworkbench.org/rest/protein/uniprot_id/Q13085/seq/json"

# Search by RefSeq ID
curl "https://www.metabolomicsworkbench.org/rest/protein/refseq_id/NP_001084/all/json"
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid parameters or malformed request
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

When no results are found, the API typically returns an empty array or object rather than an error code.

## Rate Limiting

As of 2025, the Metabolomics Workbench REST API does not enforce strict rate limits for reasonable use. However, best practices include:

- Implementing delays between bulk requests
- Caching frequently accessed reference data
- Using appropriate batch sizes for large-scale queries

## Additional Resources

- **Interactive REST URL Creator**: https://www.metabolomicsworkbench.org/tools/mw_rest.php
- **Official API Specification**: https://www.metabolomicsworkbench.org/tools/MWRestAPIv1.1.pdf
- **Python Library**: mwtab package for Python users
- **R Package**: metabolomicsWorkbenchR (Bioconductor)
- **Julia Package**: MetabolomicsWorkbenchAPI.jl

## Python Example: Complete Workflow

```python
import requests
import json

# 1. Standardize metabolite name using RefMet
metabolite = "citrate"
response = requests.get(f'https://www.metabolomicsworkbench.org/rest/refmet/match/{metabolite}/name/json')
standardized_name = response.json()['name']

# 2. Search for studies containing this metabolite
response = requests.get(f'https://www.metabolomicsworkbench.org/rest/study/refmet_name/{standardized_name}/summary/json')
studies = response.json()

# 3. Get detailed data from a specific study
study_id = studies[0]['study_id']
response = requests.get(f'https://www.metabolomicsworkbench.org/rest/study/study_id/{study_id}/data/json')
data = response.json()

# 4. Perform m/z search for compound identification
mz_value = 180.06
response = requests.get(f'https://www.metabolomicsworkbench.org/rest/moverz/MB/{mz_value}/M+H/0.5/json')
matches = response.json()

# 5. Get compound structure
regno = matches[0]['regno']
response = requests.get(f'https://www.metabolomicsworkbench.org/rest/compound/regno/{regno}/png')
with open('structure.png', 'wb') as f:
    f.write(response.content)
```
