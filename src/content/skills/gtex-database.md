---
title: "Gtex Database"
description: "Query GTEx (Genotype-Tissue Expression) portal for tissue-specific gene expression, eQTLs (expression quantitative trait loci), and sQTLs. Essential for linking GWAS variants to gene regulation, understanding tissue-specific expression, and interp..."
category: "research"
source: "community"
author: "Community"
tags: ["gtex", "database"]
date: 2026-03-20
---

# GTEx Database

## Overview

The Genotype-Tissue Expression (GTEx) project provides a comprehensive resource for studying tissue-specific gene expression and genetic regulation across 54 non-diseased human tissues from nearly 1,000 individuals. GTEx v10 (the latest release) enables researchers to understand how genetic variants regulate gene expression (eQTLs) and splicing (sQTLs) in a tissue-specific manner, which is critical for interpreting GWAS loci and identifying regulatory mechanisms.

**Key resources:**
- GTEx Portal: https://gtexportal.org/
- GTEx API v2: https://gtexportal.org/api/v2/
- Data downloads: https://gtexportal.org/home/downloads/adult-gtex/
- Documentation: https://gtexportal.org/home/documentationPage

## When to Use This Skill

Use GTEx when:

- **GWAS locus interpretation**: Identifying which gene a non-coding GWAS variant regulates via eQTLs
- **Tissue-specific expression**: Comparing gene expression levels across 54 human tissues
- **eQTL colocalization**: Testing if a GWAS signal and an eQTL signal share the same causal variant
- **Multi-tissue eQTL analysis**: Finding variants that regulate expression in multiple tissues
- **Splicing QTLs (sQTLs)**: Identifying variants that affect splicing ratios
- **Tissue specificity analysis**: Determining which tissues express a gene of interest
- **Gene expression exploration**: Retrieving normalized expression levels (TPM) per tissue

## Core Capabilities

### 1. GTEx REST API v2

Base URL: `https://gtexportal.org/api/v2/`

The API returns JSON and does not require authentication. All endpoints support pagination.

```python
import requests

BASE_URL = "https://gtexportal.org/api/v2"

def gtex_get(endpoint, params=None):
    """Make a GET request to the GTEx API."""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. Gene Expression by Tissue

```python
import requests
import pandas as pd

def get_gene_expression_by_tissue(gene_id_or_symbol, dataset_id="gtex_v10"):
    """Get median gene expression across all tissues."""
    url = "https://gtexportal.org/api/v2/expression/medianGeneExpression"
    params = {
        "gencodeId": gene_id_or_symbol,
        "datasetId": dataset_id,
        "itemsPerPage": 100
    }
    response = requests.get(url, params=params)
    data = response.json()

    records = data.get("data", [])
    df = pd.DataFrame(records)
    if not df.empty:
        df = df[["tissueSiteDetailId", "tissueSiteDetail", "median", "unit"]].sort_values(
            "median", ascending=False
        )
    return df

# Example: get expression of APOE across tissues
df = get_gene_expression_by_tissue("ENSG00000130203.10")  # APOE GENCODE ID
# Or use gene symbol (some endpoints accept both)
print(df.head(10))
# Output: tissue name, median TPM, sorted by highest expression
```

### 3. eQTL Lookup

```python
import requests
import pandas as pd

def query_eqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """Query significant eQTLs for a gene, optionally filtered by tissue."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    all_results = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("data", [])
        if not results:
            break
        all_results.extend(results)
        if len(results) < params["itemsPerPage"]:
            break
        page += 1

    df = pd.DataFrame(all_results)
    if not df.empty:
        df = df.sort_values("pval", ascending=True)
    return df

# Example: Find eQTLs for PCSK9
df = query_eqtl("ENSG00000169174.14")
print(df[["snpId", "tissueSiteDetailId", "slope", "pval", "gencodeId"]].head(20))
```

### 4. Single-Tissue eQTL by Variant

```python
import requests

def query_variant_eqtl(variant_id, tissue_id=None, dataset_id="gtex_v10"):
    """Get all eQTL associations for a specific variant."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {
        "variantId": variant_id,  # e.g., "chr1_55516888_G_GA_b38"
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()

# GTEx variant ID format: chr{chrom}_{pos}_{ref}_{alt}_b38
# Example: "chr17_43094692_G_A_b38"
```

### 5. Multi-Tissue eQTL (eGenes)

```python
import requests

def get_egenes(tissue_id, dataset_id="gtex_v10"):
    """Get all eGenes (genes with at least one significant eQTL) in a tissue."""
    url = "https://gtexportal.org/api/v2/association/egene"
    params = {
        "tissueSiteDetailId": tissue_id,
        "datasetId": dataset_id,
        "itemsPerPage": 500
    }

    all_egenes = []
    page = 0
    while True:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()
        batch = data.get("data", [])
        if not batch:
            break
        all_egenes.extend(batch)
        if len(batch) < params["itemsPerPage"]:
            break
        page += 1
    return all_egenes

# Example: all eGenes in whole blood
egenes = get_egenes("Whole_Blood")
print(f"Found {len(egenes)} eGenes in Whole Blood")
```

### 6. Tissue List

```python
import requests

def get_tissues(dataset_id="gtex_v10"):
    """Get all available tissues with metadata."""
    url = "https://gtexportal.org/api/v2/dataset/tissueSiteDetail"
    params = {"datasetId": dataset_id, "itemsPerPage": 100}
    response = requests.get(url, params=params)
    return response.json()["data"]

tissues = get_tissues()
# Key fields: tissueSiteDetailId, tissueSiteDetail, colorHex, samplingSite
# Common tissue IDs:
# Whole_Blood, Brain_Cortex, Liver, Kidney_Cortex, Heart_Left_Ventricle,
# Lung, Muscle_Skeletal, Adipose_Subcutaneous, Colon_Transverse, ...
```

### 7. sQTL (Splicing QTLs)

```python
import requests

def query_sqtl(gene_id, tissue_id=None, dataset_id="gtex_v10"):
    """Query significant sQTLs for a gene."""
    url = "https://gtexportal.org/api/v2/association/singleTissueSqtl"
    params = {
        "gencodeId": gene_id,
        "datasetId": dataset_id,
        "itemsPerPage": 250
    }
    if tissue_id:
        params["tissueSiteDetailId"] = tissue_id

    response = requests.get(url, params=params)
    return response.json()
```

## Query Workflows

### Workflow 1: Interpreting a GWAS Variant via eQTLs

1. **Identify the GWAS variant** (rs ID or chromosome position)
2. **Convert to GTEx variant ID format** (`chr{chrom}_{pos}_{ref}_{alt}_b38`)
3. **Query all eQTL associations** for that variant across tissues
4. **Check effect direction**: is the GWAS risk allele the same as the eQTL effect allele?
5. **Prioritize tissues**: select tissues biologically relevant to the disease
6. **Consider colocalization** using `coloc` (R package) with full summary statistics

```python
import requests, pandas as pd

def interpret_gwas_variant(variant_id, dataset_id="gtex_v10"):
    """Find all genes regulated by a GWAS variant."""
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
    params = {"variantId": variant_id, "datasetId": dataset_id, "itemsPerPage": 500}
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data.get("data", []))
    if df.empty:
        return df
    return df[["geneSymbol", "tissueSiteDetailId", "slope", "pval", "maf"]].sort_values("pval")

# Example
results = interpret_gwas_variant("chr1_154453788_A_T_b38")
print(results.groupby("geneSymbol")["tissueSiteDetailId"].count().sort_values(ascending=False))
```

### Workflow 2: Gene Expression Atlas

1. Get median expression for a gene across all tissues
2. Identify the primary expression site(s)
3. Compare with disease-relevant tissues
4. Download raw data for statistical comparisons

### Workflow 3: Tissue-Specific eQTL Analysis

1. Select tissues relevant to your disease
2. Query all eGenes in that tissue
3. Cross-reference with GWAS-significant loci
4. Identify co-localized signals

## Key API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/expression/medianGeneExpression` | Median TPM by tissue for a gene |
| `/expression/geneExpression` | Full distribution of expression per tissue |
| `/association/singleTissueEqtl` | Significant eQTL associations |
| `/association/singleTissueSqtl` | Significant sQTL associations |
| `/association/egene` | eGenes in a tissue |
| `/dataset/tissueSiteDetail` | Available tissues with metadata |
| `/reference/gene` | Gene metadata (GENCODE IDs, coordinates) |
| `/variant/variantPage` | Variant lookup by rsID or position |

## Datasets Available

| ID | Description |
|----|-------------|
| `gtex_v10` | GTEx v10 (current; ~960 donors, 54 tissues) |
| `gtex_v8` | GTEx v8 (838 donors, 49 tissues) — older but widely cited |

## Best Practices

- **Use GENCODE IDs** (e.g., `ENSG00000130203.10`) for gene queries; the `.version` suffix matters for some endpoints
- **GTEx variant IDs** use the format `chr{chrom}_{pos}_{ref}_{alt}_b38` (GRCh38) — different from rs IDs
- **Handle pagination**: Large queries (e.g., all eGenes) require iterating through pages
- **Tissue nomenclature**: Use `tissueSiteDetailId` (e.g., `Whole_Blood`) not display names for API calls
- **FDR correction**: GTEx uses FDR < 0.05 (q-value) as the significance threshold for eQTLs
- **Effect alleles**: The `slope` field is the effect of the alternative allele; positive = higher expression with alt allele

## Data Downloads (for large-scale analysis)

For genome-wide analyses, download full summary statistics rather than using the API:

```bash
# All significant eQTLs (v10)
wget https://storage.googleapis.com/adult-gtex/bulk-qtl/v10/single-tissue-cis-qtl/GTEx_Analysis_v10_eQTL.tar

# Normalized expression matrices
wget https://storage.googleapis.com/adult-gtex/bulk-gex/v10/rna-seq/GTEx_Analysis_v10_RNASeQCv2.4.2_gene_reads.gct.gz
```

## Additional Resources

- **GTEx Portal**: https://gtexportal.org/
- **API documentation**: https://gtexportal.org/api/v2/
- **Data downloads**: https://gtexportal.org/home/downloads/adult-gtex/
- **GitHub**: https://github.com/broadinstitute/gtex-pipeline
- **Citation**: GTEx Consortium (2020) Science. PMID: 32913098

---

## Reference: Api_Reference

# GTEx API v2 Reference

## Base URL

```
https://gtexportal.org/api/v2/
```

All endpoints accept GET requests. Responses are JSON. No authentication required.

## Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `gencodeId` | GENCODE gene ID with version | `ENSG00000130203.10` |
| `geneSymbol` | Gene symbol | `APOE` |
| `variantId` | GTEx variant ID | `chr17_45413693_C_T_b38` |
| `tissueSiteDetailId` | Tissue identifier | `Whole_Blood` |
| `datasetId` | Dataset version | `gtex_v10` |
| `itemsPerPage` | Results per page | `250` |
| `page` | Page number (0-indexed) | `0` |

## Endpoint Reference

### Expression Endpoints

#### `GET /expression/medianGeneExpression`

Median TPM expression for a gene across tissues.

**Parameters:** `gencodeId`, `datasetId`, `itemsPerPage`

**Response fields:**
```json
{
  "data": [
    {
      "gencodeId": "ENSG00000130203.10",
      "geneSymbol": "APOE",
      "tissueSiteDetailId": "Liver",
      "tissueSiteDetail": "Liver",
      "median": 2847.9,
      "unit": "TPM",
      "datasetId": "gtex_v10"
    }
  ]
}
```

#### `GET /expression/geneExpression`

Full expression distribution (box plot data) per tissue.

**Parameters:** `gencodeId`, `tissueSiteDetailId`, `datasetId`

**Response fields:**
- `data[].tissueExpressionData.data`: array of TPM values per sample

### Association (QTL) Endpoints

#### `GET /association/singleTissueEqtl`

Significant single-tissue cis-eQTLs.

**Parameters:** `gencodeId` OR `variantId`, `tissueSiteDetailId` (optional), `datasetId`

**Response fields:**
```json
{
  "data": [
    {
      "gencodeId": "ENSG00000169174.14",
      "geneSymbol": "PCSK9",
      "variantId": "chr1_55516888_G_GA_b38",
      "snpId": "rs72646508",
      "tissueSiteDetailId": "Liver",
      "slope": -0.342,
      "slopeStandardError": 0.051,
      "pval": 3.2e-11,
      "qval": 2.1e-8,
      "maf": 0.089,
      "datasetId": "gtex_v10"
    }
  ]
}
```

**Key fields:**
- `slope`: effect of alt allele on expression (log2 scale after rank normalization)
- `pval`: nominal p-value
- `qval`: FDR-adjusted q-value
- `maf`: minor allele frequency in the GTEx cohort

#### `GET /association/singleTissueSqtl`

Significant single-tissue sQTLs (splicing).

**Parameters:** Same as eQTL endpoint

#### `GET /association/egene`

All eGenes (genes with ≥1 significant eQTL) in a tissue.

**Parameters:** `tissueSiteDetailId`, `datasetId`

**Response fields:** gene ID, gene symbol, best eQTL variant, p-value, q-value

### Dataset/Metadata Endpoints

#### `GET /dataset/tissueSiteDetail`

List of all available tissues.

**Parameters:** `datasetId`, `itemsPerPage`

**Response fields:**
- `tissueSiteDetailId`: API identifier (use this in queries)
- `tissueSiteDetail`: Display name
- `colorHex`: Color for visualization
- `samplingSite`: Anatomical location

#### `GET /reference/gene`

Gene metadata from GENCODE.

**Parameters:** `geneSymbol` OR `gencodeId`, `referenceGenomeId` (GRCh38)

### Variant Endpoints

#### `GET /variant/variantPage`

Variant metadata and lookup.

**Parameters:** `snpId` (rsID) OR `variantId`

## Tissue IDs Reference (Common Tissues)

| ID | Display Name |
|----|-------------|
| `Whole_Blood` | Whole Blood |
| `Brain_Cortex` | Brain - Cortex |
| `Brain_Hippocampus` | Brain - Hippocampus |
| `Brain_Frontal_Cortex_BA9` | Brain - Frontal Cortex (BA9) |
| `Liver` | Liver |
| `Kidney_Cortex` | Kidney - Cortex |
| `Heart_Left_Ventricle` | Heart - Left Ventricle |
| `Lung` | Lung |
| `Muscle_Skeletal` | Muscle - Skeletal |
| `Adipose_Subcutaneous` | Adipose - Subcutaneous |
| `Colon_Transverse` | Colon - Transverse |
| `Small_Intestine_Terminal_Ileum` | Small Intestine - Terminal Ileum |
| `Skin_Sun_Exposed_Lower_leg` | Skin - Sun Exposed (Lower leg) |
| `Thyroid` | Thyroid |
| `Nerve_Tibial` | Nerve - Tibial |
| `Artery_Coronary` | Artery - Coronary |
| `Artery_Aorta` | Artery - Aorta |
| `Pancreas` | Pancreas |
| `Pituitary` | Pituitary |
| `Spleen` | Spleen |
| `Prostate` | Prostate |
| `Ovary` | Ovary |
| `Uterus` | Uterus |
| `Testis` | Testis |

## Error Handling

```python
import requests
from requests.exceptions import HTTPError, Timeout

def safe_gtex_query(endpoint, params):
    url = f"https://gtexportal.org/api/v2/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(f"HTTP error {e.response.status_code}: {e.response.text}")
    except Timeout:
        print("Request timed out")
    except Exception as e:
        print(f"Error: {e}")
    return None
```

## Rate Limiting

GTEx API does not publish explicit rate limits but:
- Add 0.5–1s delays between bulk queries
- Use data downloads for genome-wide analyses instead of API
- Cache results locally for repeated queries
