---
title: "Alphafold Database"
description: "Access AlphaFold 200M+ AI-predicted protein structures. Retrieve structures by UniProt ID, download PDB/mmCIF files, analyze confidence metrics (pLDDT, PAE), for drug discovery and structural biology."
category: "research"
source: "community"
author: "Community"
tags: ["alphafold", "database"]
date: 2026-03-20
---

# AlphaFold Database

## Overview

AlphaFold DB is a public repository of AI-predicted 3D protein structures for over 200 million proteins, maintained by DeepMind and EMBL-EBI. Access structure predictions with confidence metrics, download coordinate files, retrieve bulk datasets, and integrate predictions into computational workflows.

## When to Use This Skill

This skill should be used when working with AI-predicted protein structures in scenarios such as:

- Retrieving protein structure predictions by UniProt ID or protein name
- Downloading PDB/mmCIF coordinate files for structural analysis
- Analyzing prediction confidence metrics (pLDDT, PAE) to assess reliability
- Accessing bulk proteome datasets via Google Cloud Platform
- Comparing predicted structures with experimental data
- Performing structure-based drug discovery or protein engineering
- Building structural models for proteins lacking experimental structures
- Integrating AlphaFold predictions into computational pipelines

## Core Capabilities

### 1. Searching and Retrieving Predictions

**Using Biopython (Recommended):**

The Biopython library provides the simplest interface for retrieving AlphaFold structures:

```python
from Bio.PDB import alphafold_db

# Get all predictions for a UniProt accession
predictions = list(alphafold_db.get_predictions("P00520"))

# Download structure file (mmCIF format)
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"Downloaded: {cif_file}")

# Get Structure objects directly
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

**Direct API Access:**

Query predictions using REST endpoints:

```python
import requests

# Get prediction metadata for a UniProt accession
uniprot_id = "P00520"
api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
response = requests.get(api_url)
prediction_data = response.json()

# Extract AlphaFold ID
alphafold_id = prediction_data[0]['entryId']
print(f"AlphaFold ID: {alphafold_id}")
```

**Using UniProt to Find Accessions:**

Search UniProt to find protein accessions first:

```python
import urllib.parse, urllib.request

def get_uniprot_ids(query, query_type='PDB_ID'):
    """Query UniProt to get accession IDs"""
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
        'from': query_type,
        'to': 'ACC',
        'format': 'txt',
        'query': query
    }
    data = urllib.parse.urlencode(params).encode('ascii')
    with urllib.request.urlopen(urllib.request.Request(url, data)) as response:
        return response.read().decode('utf-8').splitlines()

# Example: Find UniProt IDs for a protein name
protein_ids = get_uniprot_ids("hemoglobin", query_type="GENE_NAME")
```

### 2. Downloading Structure Files

AlphaFold provides multiple file formats for each prediction:

**File Types Available:**

- **Model coordinates** (`model_v4.cif`): Atomic coordinates in mmCIF/PDBx format
- **Confidence scores** (`confidence_v4.json`): Per-residue pLDDT scores (0-100)
- **Predicted Aligned Error** (`predicted_aligned_error_v4.json`): PAE matrix for residue pair confidence

**Download URLs:**

```python
import requests

alphafold_id = "AF-P00520-F1"
version = "v4"

# Model coordinates (mmCIF)
model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.cif"
response = requests.get(model_url)
with open(f"{alphafold_id}.cif", "w") as f:
    f.write(response.text)

# Confidence scores (JSON)
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_{version}.json"
response = requests.get(confidence_url)
confidence_data = response.json()

# Predicted Aligned Error (JSON)
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_{version}.json"
response = requests.get(pae_url)
pae_data = response.json()
```

**PDB Format (Alternative):**

```python
# Download as PDB format instead of mmCIF
pdb_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.pdb"
response = requests.get(pdb_url)
with open(f"{alphafold_id}.pdb", "wb") as f:
    f.write(response.content)
```

### 3. Working with Confidence Metrics

AlphaFold predictions include confidence estimates critical for interpretation:

**pLDDT (per-residue confidence):**

```python
import json
import requests

# Load confidence scores
alphafold_id = "AF-P00520-F1"
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
confidence = requests.get(confidence_url).json()

# Extract pLDDT scores
plddt_scores = confidence['confidenceScore']

# Interpret confidence levels
# pLDDT > 90: Very high confidence
# pLDDT 70-90: High confidence
# pLDDT 50-70: Low confidence
# pLDDT < 50: Very low confidence

high_confidence_residues = [i for i, score in enumerate(plddt_scores) if score > 90]
print(f"High confidence residues: {len(high_confidence_residues)}/{len(plddt_scores)}")
```

**PAE (Predicted Aligned Error):**

PAE indicates confidence in relative domain positions:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load PAE matrix
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_v4.json"
pae = requests.get(pae_url).json()

# Visualize PAE matrix
pae_matrix = np.array(pae['distance'])
plt.figure(figsize=(10, 8))
plt.imshow(pae_matrix, cmap='viridis_r', vmin=0, vmax=30)
plt.colorbar(label='PAE (Å)')
plt.title(f'Predicted Aligned Error: {alphafold_id}')
plt.xlabel('Residue')
plt.ylabel('Residue')
plt.savefig(f'{alphafold_id}_pae.png', dpi=300, bbox_inches='tight')

# Low PAE values (<5 Å) indicate confident relative positioning
# High PAE values (>15 Å) suggest uncertain domain arrangements
```

### 4. Bulk Data Access via Google Cloud

For large-scale analyses, use Google Cloud datasets:

**Google Cloud Storage:**

```bash
# Install gsutil
uv pip install gsutil

# List available data
gsutil ls gs://public-datasets-deepmind-alphafold-v4/

# Download entire proteomes (by taxonomy ID)
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar .

# Download specific files
gsutil cp gs://public-datasets-deepmind-alphafold-v4/accession_ids.csv .
```

**BigQuery Metadata Access:**

```python
from google.cloud import bigquery

# Initialize client
client = bigquery.Client()

# Query metadata
query = """
SELECT
  entryId,
  uniprotAccession,
  organismScientificName,
  globalMetricValue,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE organismScientificName = 'Homo sapiens'
  AND fractionPlddtVeryHigh > 0.8
LIMIT 100
"""

results = client.query(query).to_dataframe()
print(f"Found {len(results)} high-confidence human proteins")
```

**Download by Species:**

> ⚠️ **Security Note**: The example below uses `shell=True` for simplicity. In production environments, prefer using `subprocess.run()` with a list of arguments to prevent command injection vulnerabilities. See [Python subprocess security](https://docs.python.org/3/library/subprocess.html#security-considerations).

```python
import subprocess
import shlex

def download_proteome(taxonomy_id, output_dir="./proteomes"):
    """Download all AlphaFold predictions for a species"""
    # Validate taxonomy_id is an integer to prevent injection
    if not isinstance(taxonomy_id, int):
        raise ValueError("taxonomy_id must be an integer")
    
    pattern = f"gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-{taxonomy_id}-*_v4.tar"
    # Use list form instead of shell=True for security
    subprocess.run(["gsutil", "-m", "cp", pattern, f"{output_dir}/"], check=True)

# Download E. coli proteome (tax ID: 83333)
download_proteome(83333)

# Download human proteome (tax ID: 9606)
download_proteome(9606)
```

### 5. Parsing and Analyzing Structures

Work with downloaded AlphaFold structures using BioPython:

```python
from Bio.PDB import MMCIFParser, PDBIO
import numpy as np

# Parse mmCIF file
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# Extract coordinates
coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:  # Alpha carbons only
                coords.append(residue['CA'].get_coord())

coords = np.array(coords)
print(f"Structure has {len(coords)} residues")

# Calculate distances
from scipy.spatial.distance import pdist, squareform
distance_matrix = squareform(pdist(coords))

# Identify contacts (< 8 Å)
contacts = np.where((distance_matrix > 0) & (distance_matrix < 8))
print(f"Number of contacts: {len(contacts[0]) // 2}")
```

**Extract B-factors (pLDDT values):**

AlphaFold stores pLDDT scores in the B-factor column:

```python
from Bio.PDB import MMCIFParser

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# Extract pLDDT from B-factors
plddt_scores = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                plddt_scores.append(residue['CA'].get_bfactor())

# Identify high-confidence regions
high_conf_regions = [(i, score) for i, score in enumerate(plddt_scores, 1) if score > 90]
print(f"High confidence residues: {len(high_conf_regions)}")
```

### 6. Batch Processing Multiple Proteins

Process multiple predictions efficiently:

```python
from Bio.PDB import alphafold_db
import pandas as pd

uniprot_ids = ["P00520", "P12931", "P04637"]  # Multiple proteins
results = []

for uniprot_id in uniprot_ids:
    try:
        # Get prediction
        predictions = list(alphafold_db.get_predictions(uniprot_id))

        if predictions:
            pred = predictions[0]

            # Download structure
            cif_file = alphafold_db.download_cif_for(pred, directory="./batch_structures")

            # Get confidence data
            alphafold_id = pred['entryId']
            conf_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
            conf_data = requests.get(conf_url).json()

            # Calculate statistics
            plddt_scores = conf_data['confidenceScore']
            avg_plddt = np.mean(plddt_scores)
            high_conf_fraction = sum(1 for s in plddt_scores if s > 90) / len(plddt_scores)

            results.append({
                'uniprot_id': uniprot_id,
                'alphafold_id': alphafold_id,
                'avg_plddt': avg_plddt,
                'high_conf_fraction': high_conf_fraction,
                'length': len(plddt_scores)
            })
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

# Create summary DataFrame
df = pd.DataFrame(results)
print(df)
```

## Installation and Setup

### Python Libraries

```bash
# Install Biopython for structure access
uv pip install biopython

# Install requests for API access
uv pip install requests

# For visualization and analysis
uv pip install numpy matplotlib pandas scipy

# For Google Cloud access (optional)
uv pip install google-cloud-bigquery gsutil
```

### 3D-Beacons API Alternative

AlphaFold can also be accessed via the 3D-Beacons federated API:

```python
import requests

# Query via 3D-Beacons
uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
af_structures = [s for s in data['structures'] if s['provider'] == 'AlphaFold DB']
```

## Common Use Cases

### Structural Proteomics
- Download complete proteome predictions for analysis
- Identify high-confidence structural regions across proteins
- Compare predicted structures with experimental data
- Build structural models for protein families

### Drug Discovery
- Retrieve target protein structures for docking studies
- Analyze binding site conformations
- Identify druggable pockets in predicted structures
- Compare structures across homologs

### Protein Engineering
- Identify stable/unstable regions using pLDDT
- Design mutations in high-confidence regions
- Analyze domain architectures using PAE
- Model protein variants and mutations

### Evolutionary Studies
- Compare ortholog structures across species
- Analyze conservation of structural features
- Study domain evolution patterns
- Identify functionally important regions

## Key Concepts

**UniProt Accession:** Primary identifier for proteins (e.g., "P00520"). Required for querying AlphaFold DB.

**AlphaFold ID:** Internal identifier format: `AF-[UniProt accession]-F[fragment number]` (e.g., "AF-P00520-F1").

**pLDDT (predicted Local Distance Difference Test):** Per-residue confidence metric (0-100). Higher values indicate more confident predictions.

**PAE (Predicted Aligned Error):** Matrix indicating confidence in relative positions between residue pairs. Low values (<5 Å) suggest confident relative positioning.

**Database Version:** Current version is v4. File URLs include version suffix (e.g., `model_v4.cif`).

**Fragment Number:** Large proteins may be split into fragments. Fragment number appears in AlphaFold ID (e.g., F1, F2).

## Confidence Interpretation Guidelines

**pLDDT Thresholds:**
- **>90**: Very high confidence - suitable for detailed analysis
- **70-90**: High confidence - generally reliable backbone structure
- **50-70**: Low confidence - use with caution, flexible regions
- **<50**: Very low confidence - likely disordered or unreliable

**PAE Guidelines:**
- **<5 Å**: Confident relative positioning of domains
- **5-10 Å**: Moderate confidence in arrangement
- **>15 Å**: Uncertain relative positions, domains may be mobile

## Resources

### references/api_reference.md

Comprehensive API documentation covering:
- Complete REST API endpoint specifications
- File format details and data schemas
- Google Cloud dataset structure and access patterns
- Advanced query examples and batch processing strategies
- Rate limiting, caching, and best practices
- Troubleshooting common issues

Consult this reference for detailed API information, bulk download strategies, or when working with large-scale datasets.

## Important Notes

### Data Usage and Attribution

- AlphaFold DB is freely available under CC-BY-4.0 license
- Cite: Jumper et al. (2021) Nature and Varadi et al. (2022) Nucleic Acids Research
- Predictions are computational models, not experimental structures
- Always assess confidence metrics before downstream analysis

### Version Management

- Current database version: v4 (as of 2024-2025)
- File URLs include version suffix (e.g., `_v4.cif`)
- Check for database updates regularly
- Older versions may be deprecated over time

### Data Quality Considerations

- High pLDDT doesn't guarantee functional accuracy
- Low confidence regions may be disordered in vivo
- PAE indicates relative domain confidence, not absolute positioning
- Predictions lack ligands, post-translational modifications, and cofactors
- Multi-chain complexes are not predicted (single chains only)

### Performance Tips

- Use Biopython for simple single-protein access
- Use Google Cloud for bulk downloads (much faster than individual files)
- Cache downloaded files locally to avoid repeated downloads
- BigQuery free tier: 1 TB processed data per month
- Consider network bandwidth for large-scale downloads

## Additional Resources

- **AlphaFold DB Website:** https://alphafold.ebi.ac.uk/
- **API Documentation:** https://alphafold.ebi.ac.uk/api-docs
- **Google Cloud Dataset:** https://cloud.google.com/blog/products/ai-machine-learning/alphafold-protein-structure-database
- **3D-Beacons API:** https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/
- **AlphaFold Papers:**
  - Nature (2021): https://doi.org/10.1038/s41586-021-03819-2
  - Nucleic Acids Research (2024): https://doi.org/10.1093/nar/gkad1011
- **Biopython Documentation:** https://biopython.org/docs/dev/api/Bio.PDB.alphafold_db.html
- **GitHub Repository:** https://github.com/google-deepmind/alphafold

---

## Reference: Api_Reference

# AlphaFold Database API Reference

This document provides comprehensive technical documentation for programmatic access to the AlphaFold Protein Structure Database.

## Table of Contents

1. [REST API Endpoints](#rest-api-endpoints)
2. [File Access Patterns](#file-access-patterns)
3. [Data Schemas](#data-schemas)
4. [Google Cloud Access](#google-cloud-access)
5. [BigQuery Schema](#bigquery-schema)
6. [Best Practices](#best-practices)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)

---

## REST API Endpoints

### Base URL

```
https://alphafold.ebi.ac.uk/api/
```

### 1. Get Prediction by UniProt Accession

**Endpoint:** `/prediction/{uniprot_id}`

**Method:** GET

**Description:** Retrieve AlphaFold prediction metadata for a given UniProt accession.

**Parameters:**
- `uniprot_id` (required): UniProt accession (e.g., "P00520")

**Example Request:**
```bash
curl https://alphafold.ebi.ac.uk/api/prediction/P00520
```

**Example Response:**
```json
[
  {
    "entryId": "AF-P00520-F1",
    "gene": "ABL1",
    "uniprotAccession": "P00520",
    "uniprotId": "ABL1_HUMAN",
    "uniprotDescription": "Tyrosine-protein kinase ABL1",
    "taxId": 9606,
    "organismScientificName": "Homo sapiens",
    "uniprotStart": 1,
    "uniprotEnd": 1130,
    "uniprotSequence": "MLEICLKLVGCKSKKGLSSSSSCYLEEALQRPVASDFEPQGLSEAARWNSKENLLAGPSENDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNHNGEWCEAQTKNGQGWVPSNYITPVNSLEKHSWYHGPVSRNAAEYLLSSGINGSFLVRESESSPGQRSISLRYEGRVYHYRINTASDGKLYVSSESRFNTLAELVHHHSTVADGLITTLHYPAPKRNKPTVYGVSPNYDKWEMERTDITMKHKLGGGQYGEVYEGVWKKYSLTVAVKTLKEDTMEVEEFLKEAAVMKEIKHPNLVQLLGVCTREPPFYIITEFMTYGNLLDYLRECNRQEVNAVVLLYMATQISSAMEYLEKKNFIHRDLAARNCLVGENHLVKVADFGLSRLMTGDTYTAHAGAKFPIKWTAPESLAYNKFSIKSDVWAFGVLLWEIATYGMSPYPGIDLSQVYELLEKDYRMERPEGCPEKVYELMRACWQWNPSDRPSFAEIHQAFETMFQESSISDEVEKELGKQGVRGAVSTLLQAPELPTKTRTSRRAAEHRDTTDVPEMPHSKGQGESDPLDHEPAVSPLLPRKERGPPEGGLNEDERLLPKDKKTNLFSALIKKKKKTAPTPPKRSSSFREMDGQPERRGAGEEEGRDISNGALAFTPLDTADPAKSPKPSNGAGVPNGALRESGGSGFRSPHLWKKSSTLTSSRLATGEEEGGGSSSKRFLRSCSASCVPHGAKDTEWRSVTLPRDLQSTGRQFDSSTFGGHKSEKPALPRKRAGENRSDQVTRGTVTPPPRLVKKNEEAADEVFKDIMESSPGSSPPNLTPKPLRRQVTVAPASGLPHKEEAGKGSALGTPAAAEPVTPTSKAGSGAPGGTSKGPAEESRVRRHKHSSESPGRDKGKLSRLKPAPPPPPAASAGKAGGKPSQSPSQEAAGEAVLGAKTKATSLVDAVNSDAAKPSQPGEGLKKPVLPATPKPQSAKPSGTPISPAPVPSTLPSASSALAGDQPSSTAFIPLISTRVSLRKTRQPPERIASGAITKGVVLDSTEALCLAISRNSEQMASHSAVLEAGKNLYTFCVSYVDSIQQMRNKFAFREAINKLENNLRELQICPATAGSGPAATQDFSKLLSSVKEISDIVQR",
    "modelCreatedDate": "2021-07-01",
    "latestVersion": 4,
    "allVersions": [1, 2, 3, 4],
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.cif",
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.bcif",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.pdb",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v4.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v4.json"
  }
]
```

**Response Fields:**
- `entryId`: AlphaFold internal identifier (format: AF-{uniprot}-F{fragment})
- `gene`: Gene symbol
- `uniprotAccession`: UniProt accession
- `uniprotId`: UniProt entry name
- `uniprotDescription`: Protein description
- `taxId`: NCBI taxonomy identifier
- `organismScientificName`: Species scientific name
- `uniprotStart/uniprotEnd`: Residue range covered
- `uniprotSequence`: Full protein sequence
- `modelCreatedDate`: Initial prediction date
- `latestVersion`: Current model version number
- `allVersions`: List of available versions
- `cifUrl/bcifUrl/pdbUrl`: Structure file download URLs
- `paeImageUrl`: PAE visualization image URL
- `paeDocUrl`: PAE data JSON URL

### 2. 3D-Beacons Integration

AlphaFold is integrated into the 3D-Beacons network for federated structure access.

**Endpoint:** `https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json`

**Example:**
```python
import requests

uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
alphafold_structures = [
    s for s in data['structures']
    if s['provider'] == 'AlphaFold DB'
]
```

---

## File Access Patterns

### Direct File Downloads

All AlphaFold files are accessible via direct URLs without authentication.

**URL Pattern:**
```
https://alphafold.ebi.ac.uk/files/{alphafold_id}-{file_type}_{version}.{extension}
```

**Components:**
- `{alphafold_id}`: Entry identifier (e.g., "AF-P00520-F1")
- `{file_type}`: Type of file (see below)
- `{version}`: Database version (e.g., "v4")
- `{extension}`: File format extension

### Available File Types

#### 1. Model Coordinates

**mmCIF Format (Recommended):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.cif
```
- Standard crystallographic format
- Contains full metadata
- Supports large structures
- File size: Variable (100KB - 10MB typical)

**Binary CIF Format:**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.bcif
```
- Compressed binary version of mmCIF
- Smaller file size (~70% reduction)
- Faster parsing
- Requires specialized parser

**PDB Format (Legacy):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v4.pdb
```
- Traditional PDB text format
- Limited to 99,999 atoms
- Widely supported by older tools
- File size: Similar to mmCIF

#### 2. Confidence Metrics

**Per-Residue Confidence (JSON):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-confidence_v4.json
```

**Structure:**
```json
{
  "confidenceScore": [87.5, 91.2, 93.8, ...],
  "confidenceCategory": ["high", "very_high", "very_high", ...]
}
```

**Fields:**
- `confidenceScore`: Array of pLDDT values (0-100) for each residue
- `confidenceCategory`: Categorical classification (very_low, low, high, very_high)

#### 3. Predicted Aligned Error (JSON)

```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v4.json
```

**Structure:**
```json
{
  "distance": [[0, 2.3, 4.5, ...], [2.3, 0, 3.1, ...], ...],
  "max_predicted_aligned_error": 31.75
}
```

**Fields:**
- `distance`: N×N matrix of PAE values in Ångströms
- `max_predicted_aligned_error`: Maximum PAE value in the matrix

#### 4. PAE Visualization (PNG)

```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v4.png
```
- Pre-rendered PAE heatmap
- Useful for quick visual assessment
- Resolution: Variable based on protein size

### Batch Download Strategy

For downloading multiple files efficiently, use concurrent downloads with proper error handling and rate limiting to respect server resources.

---

## Data Schemas

### Coordinate File (mmCIF) Schema

AlphaFold mmCIF files contain:

**Key Data Categories:**
- `_entry`: Entry-level metadata
- `_struct`: Structure title and description
- `_entity`: Molecular entity information
- `_atom_site`: Atomic coordinates and properties
- `_pdbx_struct_assembly`: Biological assembly info

**Important Fields in `_atom_site`:**
- `group_PDB`: "ATOM" for all records
- `id`: Atom serial number
- `label_atom_id`: Atom name (e.g., "CA", "N", "C")
- `label_comp_id`: Residue name (e.g., "ALA", "GLY")
- `label_seq_id`: Residue sequence number
- `Cartn_x/y/z`: Cartesian coordinates (Ångströms)
- `B_iso_or_equiv`: B-factor (contains pLDDT score)

**pLDDT in B-factor Column:**
AlphaFold stores per-residue confidence (pLDDT) in the B-factor field. This allows standard structure viewers to color by confidence automatically.

### Confidence JSON Schema

```json
{
  "confidenceScore": [
    87.5,   // Residue 1 pLDDT
    91.2,   // Residue 2 pLDDT
    93.8    // Residue 3 pLDDT
    // ... one value per residue
  ],
  "confidenceCategory": [
    "high",      // Residue 1 category
    "very_high", // Residue 2 category
    "very_high"  // Residue 3 category
    // ... one category per residue
  ]
}
```

**Confidence Categories:**
- `very_high`: pLDDT > 90
- `high`: 70 < pLDDT ≤ 90
- `low`: 50 < pLDDT ≤ 70
- `very_low`: pLDDT ≤ 50

### PAE JSON Schema

```json
{
  "distance": [
    [0.0, 2.3, 4.5, ...],     // PAE from residue 1 to all residues
    [2.3, 0.0, 3.1, ...],     // PAE from residue 2 to all residues
    [4.5, 3.1, 0.0, ...]      // PAE from residue 3 to all residues
    // ... N×N matrix for N residues
  ],
  "max_predicted_aligned_error": 31.75
}
```

**Interpretation:**
- `distance[i][j]`: Expected position error (Ångströms) of residue j if the predicted and true structures were aligned on residue i
- Lower values indicate more confident relative positioning
- Diagonal is always 0 (residue aligned to itself)
- Matrix is not symmetric: distance[i][j] ≠ distance[j][i]

---

## Google Cloud Access

AlphaFold DB is hosted on Google Cloud Platform for bulk access.

### Cloud Storage Bucket

**Bucket:** `gs://public-datasets-deepmind-alphafold-v4`

**Directory Structure:**
```
gs://public-datasets-deepmind-alphafold-v4/
├── accession_ids.csv              # Index of all entries (13.5 GB)
├── sequences.fasta                # All protein sequences (16.5 GB)
└── proteomes/                     # Grouped by species (1M+ archives)
```

### Installing gsutil

```bash
# Using pip
pip install gsutil

# Or install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
```

### Downloading Proteomes

**By Taxonomy ID:**

```bash
# Download all archives for a species
TAX_ID=9606  # Human
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-${TAX_ID}-*_v4.tar .
```

---

## BigQuery Schema

AlphaFold metadata is available in BigQuery for SQL-based queries.

**Dataset:** `bigquery-public-data.deepmind_alphafold`
**Table:** `metadata`

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `entryId` | STRING | AlphaFold entry ID |
| `uniprotAccession` | STRING | UniProt accession |
| `gene` | STRING | Gene symbol |
| `organismScientificName` | STRING | Species scientific name |
| `taxId` | INTEGER | NCBI taxonomy ID |
| `globalMetricValue` | FLOAT | Overall quality metric |
| `fractionPlddtVeryHigh` | FLOAT | Fraction with pLDDT ≥ 90 |
| `isReviewed` | BOOLEAN | Swiss-Prot reviewed status |
| `sequenceLength` | INTEGER | Protein sequence length |

### Example Query

```sql
SELECT
  entryId,
  uniprotAccession,
  gene,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE
  taxId = 9606  -- Homo sapiens
  AND fractionPlddtVeryHigh > 0.8
  AND isReviewed = TRUE
ORDER BY fractionPlddtVeryHigh DESC
LIMIT 100;
```

---

## Best Practices

### 1. Caching Strategy

Always cache downloaded files locally to avoid repeated downloads.

### 2. Error Handling

Implement robust error handling for API requests with retry logic for transient failures.

### 3. Bulk Processing

For processing many proteins, use concurrent downloads with appropriate rate limiting.

### 4. Version Management

Always specify and track database versions in your code (current: v4).

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response normally |
| 404 | Not Found | No AlphaFold prediction for this UniProt ID |
| 429 | Too Many Requests | Implement rate limiting and retry with backoff |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Wait and retry later |

---

## Rate Limiting

### Recommendations

- Limit to **10 concurrent requests** maximum
- Add **100-200ms delay** between sequential requests
- Use Google Cloud for bulk downloads instead of REST API
- Cache all downloaded data locally

---

## Additional Resources

- **AlphaFold GitHub:** https://github.com/google-deepmind/alphafold
- **Google Cloud Documentation:** https://cloud.google.com/datasets/alphafold
- **3D-Beacons Documentation:** https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/docs
- **Biopython Tutorial:** https://biopython.org/wiki/AlphaFold

## Version History

- **v1** (2021): Initial release with ~350K structures
- **v2** (2022): Expanded to 200M+ structures
- **v3** (2023): Updated models and expanded coverage
- **v4** (2024): Current version with improved confidence metrics

## Citation

When using AlphaFold DB in publications, cite:

1. Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583–589 (2021).
2. Varadi, M. et al. AlphaFold Protein Structure Database in 2024: providing structure coverage for over 214 million protein sequences. Nucleic Acids Res. 52, D368–D375 (2024).
