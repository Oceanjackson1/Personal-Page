---
title: "Pydeseq2"
description: "Differential gene expression analysis (Python DESeq2). Identify DE genes from bulk RNA-seq counts, Wald tests, FDR correction, volcano/MA plots, for RNA-seq analysis."
category: "development"
source: "community"
author: "Community"
tags: ["pydeseq2"]
date: 2026-03-20
---

# PyDESeq2

## Overview

PyDESeq2 is a Python implementation of DESeq2 for differential expression analysis with bulk RNA-seq data. Design and execute complete workflows from data loading through result interpretation, including single-factor and multi-factor designs, Wald tests with multiple testing correction, optional apeGLM shrinkage, and integration with pandas and AnnData.

## When to Use This Skill

This skill should be used when:
- Analyzing bulk RNA-seq count data for differential expression
- Comparing gene expression between experimental conditions (e.g., treated vs control)
- Performing multi-factor designs accounting for batch effects or covariates
- Converting R-based DESeq2 workflows to Python
- Integrating differential expression analysis into Python-based pipelines
- Users mention "DESeq2", "differential expression", "RNA-seq analysis", or "PyDESeq2"

## Quick Start Workflow

For users who want to perform a standard differential expression analysis:

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Load data
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpose to samples × genes
metadata = pd.read_csv("metadata.csv", index_col=0)

# 2. Filter low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 3. Initialize and fit DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)
dds.deseq2()

# 4. Perform statistical testing
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. Access results
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## Core Workflow Steps

### Step 1: Data Preparation

**Input requirements:**
- **Count matrix:** Samples × genes DataFrame with non-negative integer read counts
- **Metadata:** Samples × variables DataFrame with experimental factors

**Common data loading patterns:**

```python
# From CSV (typical format: genes × samples, needs transpose)
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# From TSV
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T

# From AnnData
import anndata as ad
adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(adata.X, index=adata.obs_names, columns=adata.var_names)
metadata = adata.obs
```

**Data filtering:**

```python
# Remove low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# Remove samples with missing metadata
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

### Step 2: Design Specification

The design formula specifies how gene expression is modeled.

**Single-factor designs:**
```python
design = "~condition"  # Simple two-group comparison
```

**Multi-factor designs:**
```python
design = "~batch + condition"  # Control for batch effects
design = "~age + condition"     # Include continuous covariate
design = "~group + condition + group:condition"  # Interaction effects
```

**Design formula guidelines:**
- Use Wilkinson formula notation (R-style)
- Put adjustment variables (e.g., batch) before the main variable of interest
- Ensure variables exist as columns in the metadata DataFrame
- Use appropriate data types (categorical for discrete variables)

### Step 3: DESeq2 Fitting

Initialize the DeseqDataSet and run the complete pipeline:

```python
from pydeseq2.dds import DeseqDataSet

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,  # Refit after removing outliers
    n_cpus=1           # Parallel processing (adjust as needed)
)

# Run the complete DESeq2 pipeline
dds.deseq2()
```

**What `deseq2()` does:**
1. Computes size factors (normalization)
2. Fits genewise dispersions
3. Fits dispersion trend curve
4. Computes dispersion priors
5. Fits MAP dispersions (shrinkage)
6. Fits log fold changes
7. Calculates Cook's distances (outlier detection)
8. Refits if outliers detected (optional)

### Step 4: Statistical Testing

Perform Wald tests to identify differentially expressed genes:

```python
from pydeseq2.ds import DeseqStats

ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],  # Test treated vs control
    alpha=0.05,                # Significance threshold
    cooks_filter=True,         # Filter outliers
    independent_filter=True    # Filter low-power tests
)

ds.summary()
```

**Contrast specification:**
- Format: `[variable, test_level, reference_level]`
- Example: `["condition", "treated", "control"]` tests treated vs control
- If `None`, uses the last coefficient in the design

**Result DataFrame columns:**
- `baseMean`: Mean normalized count across samples
- `log2FoldChange`: Log2 fold change between conditions
- `lfcSE`: Standard error of LFC
- `stat`: Wald test statistic
- `pvalue`: Raw p-value
- `padj`: Adjusted p-value (FDR-corrected via Benjamini-Hochberg)

### Step 5: Optional LFC Shrinkage

Apply shrinkage to reduce noise in fold change estimates:

```python
ds.lfc_shrink()  # Applies apeGLM shrinkage
```

**When to use LFC shrinkage:**
- For visualization (volcano plots, heatmaps)
- For ranking genes by effect size
- When prioritizing genes for follow-up experiments

**Important:** Shrinkage affects only the log2FoldChange values, not the statistical test results (p-values remain unchanged). Use shrunk values for visualization but report unshrunken p-values for significance.

### Step 6: Result Export

Save results and intermediate objects:

```python
import pickle

# Export results as CSV
ds.results_df.to_csv("deseq2_results.csv")

# Save significant genes only
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# Save DeseqDataSet for later use
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

## Common Analysis Patterns

### Two-Group Comparison

Standard case-control comparison:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

results = ds.results_df
significant = results[results.padj < 0.05]
```

### Multiple Comparisons

Testing multiple treatment groups against control:

```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

treatments = ["treatment_A", "treatment_B", "treatment_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(dds, contrast=["condition", treatment, "control"])
    ds.summary()
    all_results[treatment] = ds.results_df

    sig_count = len(ds.results_df[ds.results_df.padj < 0.05])
    print(f"{treatment}: {sig_count} significant genes")
```

### Accounting for Batch Effects

Control for technical variation:

```python
# Include batch in design
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~batch + condition")
dds.deseq2()

# Test condition while controlling for batch
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

### Continuous Covariates

Include continuous variables like age or dosage:

```python
# Ensure continuous variable is numeric
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~age + condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

## Using the Analysis Script

This skill includes a complete command-line script for standard analyses:

```bash
# Basic usage
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~condition" \
  --contrast condition treated control \
  --output results/

# With additional options
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~batch + condition" \
  --contrast condition treated control \
  --output results/ \
  --min-counts 10 \
  --alpha 0.05 \
  --n-cpus 4 \
  --plots
```

**Script features:**
- Automatic data loading and validation
- Gene and sample filtering
- Complete DESeq2 pipeline execution
- Statistical testing with customizable parameters
- Result export (CSV, pickle)
- Optional visualization (volcano and MA plots)

Refer users to `scripts/run_deseq2_analysis.py` when they need a standalone analysis tool or want to batch process multiple datasets.

## Result Interpretation

### Identifying Significant Genes

```python
# Filter by adjusted p-value
significant = ds.results_df[ds.results_df.padj < 0.05]

# Filter by both significance and effect size
sig_and_large = ds.results_df[
    (ds.results_df.padj < 0.05) &
    (abs(ds.results_df.log2FoldChange) > 1)
]

# Separate up- and down-regulated
upregulated = significant[significant.log2FoldChange > 0]
downregulated = significant[significant.log2FoldChange < 0]

print(f"Upregulated: {len(upregulated)}")
print(f"Downregulated: {len(downregulated)}")
```

### Ranking and Sorting

```python
# Sort by adjusted p-value
top_by_padj = ds.results_df.sort_values("padj").head(20)

# Sort by absolute fold change (use shrunk values)
ds.lfc_shrink()
ds.results_df["abs_lfc"] = abs(ds.results_df.log2FoldChange)
top_by_lfc = ds.results_df.sort_values("abs_lfc", ascending=False).head(20)

# Sort by a combined metric
ds.results_df["score"] = -np.log10(ds.results_df.padj) * abs(ds.results_df.log2FoldChange)
top_combined = ds.results_df.sort_values("score", ascending=False).head(20)
```

### Quality Metrics

```python
# Check normalization (size factors should be close to 1)
print("Size factors:", dds.obsm["size_factors"])

# Examine dispersion estimates
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.title("Dispersion Distribution")
plt.show()

# Check p-value distribution (should be mostly flat with peak near 0)
plt.hist(ds.results_df.pvalue.dropna(), bins=50)
plt.xlabel("P-value")
plt.ylabel("Frequency")
plt.title("P-value Distribution")
plt.show()
```

## Visualization Guidelines

### Volcano Plot

Visualize significance vs effect size:

```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

plt.figure(figsize=(10, 6))
significant = results.padj < 0.05

plt.scatter(
    results.loc[~significant, "log2FoldChange"],
    results.loc[~significant, "-log10(padj)"],
    alpha=0.3, s=10, c='gray', label='Not significant'
)
plt.scatter(
    results.loc[significant, "log2FoldChange"],
    results.loc[significant, "-log10(padj)"],
    alpha=0.6, s=10, c='red', label='padj < 0.05'
)

plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

### MA Plot

Show fold change vs mean expression:

```python
plt.figure(figsize=(10, 6))

plt.scatter(
    np.log10(results.loc[~significant, "baseMean"] + 1),
    results.loc[~significant, "log2FoldChange"],
    alpha=0.3, s=10, c='gray'
)
plt.scatter(
    np.log10(results.loc[significant, "baseMean"] + 1),
    results.loc[significant, "log2FoldChange"],
    alpha=0.6, s=10, c='red'
)

plt.axhline(0, color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

## Troubleshooting Common Issues

### Data Format Problems

**Issue:** "Index mismatch between counts and metadata"

**Solution:** Ensure sample names match exactly
```python
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# Take intersection if needed
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]
```

**Issue:** "All genes have zero counts"

**Solution:** Check if data needs transposition
```python
print(f"Counts shape: {counts_df.shape}")
# If genes > samples, transpose is needed
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### Design Matrix Issues

**Issue:** "Design matrix is not full rank"

**Cause:** Confounded variables (e.g., all treated samples in one batch)

**Solution:** Remove confounded variable or add interaction term
```python
# Check confounding
print(pd.crosstab(metadata.condition, metadata.batch))

# Either simplify design or add interaction
design = "~condition"  # Remove batch
# OR
design = "~condition + batch + condition:batch"  # Model interaction
```

### No Significant Genes

**Diagnostics:**
```python
# Check dispersion distribution
plt.hist(dds.varm["dispersions"], bins=50)
plt.show()

# Check size factors
print(dds.obsm["size_factors"])

# Look at top genes by raw p-value
print(ds.results_df.nsmallest(20, "pvalue"))
```

**Possible causes:**
- Small effect sizes
- High biological variability
- Insufficient sample size
- Technical issues (batch effects, outliers)

## Reference Documentation

For comprehensive details beyond this workflow-oriented guide:

- **API Reference** (`references/api_reference.md`): Complete documentation of PyDESeq2 classes, methods, and data structures. Use when needing detailed parameter information or understanding object attributes.

- **Workflow Guide** (`references/workflow_guide.md`): In-depth guide covering complete analysis workflows, data loading patterns, multi-factor designs, troubleshooting, and best practices. Use when handling complex experimental designs or encountering issues.

Load these references into context when users need:
- Detailed API documentation: `Read references/api_reference.md`
- Comprehensive workflow examples: `Read references/workflow_guide.md`
- Troubleshooting guidance: `Read references/workflow_guide.md` (see Troubleshooting section)

## Key Reminders

1. **Data orientation matters:** Count matrices typically load as genes × samples but need to be samples × genes. Always transpose with `.T` if needed.

2. **Sample filtering:** Remove samples with missing metadata before analysis to avoid errors.

3. **Gene filtering:** Filter low-count genes (e.g., < 10 total reads) to improve power and reduce computational time.

4. **Design formula order:** Put adjustment variables before the variable of interest (e.g., `"~batch + condition"` not `"~condition + batch"`).

5. **LFC shrinkage timing:** Apply shrinkage after statistical testing and only for visualization/ranking purposes. P-values remain based on unshrunken estimates.

6. **Result interpretation:** Use `padj < 0.05` for significance, not raw p-values. The Benjamini-Hochberg procedure controls false discovery rate.

7. **Contrast specification:** The format is `[variable, test_level, reference_level]` where test_level is compared against reference_level.

8. **Save intermediate objects:** Use pickle to save DeseqDataSet objects for later use or additional analyses without re-running the expensive fitting step.

## Installation and Requirements

```bash
uv pip install pydeseq2
```

**System requirements:**
- Python 3.10-3.11
- pandas 1.4.3+
- numpy 1.23.0+
- scipy 1.11.0+
- scikit-learn 1.1.1+
- anndata 0.8.0+

**Optional for visualization:**
- matplotlib
- seaborn

## Additional Resources

- **Official Documentation:** https://pydeseq2.readthedocs.io
- **GitHub Repository:** https://github.com/owkin/PyDESeq2
- **Publication:** Muzellec et al. (2023) Bioinformatics, DOI: 10.1093/bioinformatics/btad547
- **Original DESeq2 (R):** Love et al. (2014) Genome Biology, DOI: 10.1186/s13059-014-0550-8

---

## Reference: Api_Reference

# PyDESeq2 API Reference

This document provides comprehensive API reference for PyDESeq2 classes, methods, and utilities.

## Core Classes

### DeseqDataSet

The main class for differential expression analysis that handles data processing from normalization through log-fold change fitting.

**Purpose:** Implements dispersion and log fold-change (LFC) estimation for RNA-seq count data.

**Initialization Parameters:**
- `counts`: pandas DataFrame of shape (samples × genes) containing non-negative integer read counts
- `metadata`: pandas DataFrame of shape (samples × variables) with sample annotations
- `design`: str, Wilkinson formula specifying the statistical model (e.g., "~condition", "~group + condition")
- `refit_cooks`: bool, whether to refit parameters after removing Cook's distance outliers (default: True)
- `n_cpus`: int, number of CPUs to use for parallel processing (optional)
- `quiet`: bool, suppress progress messages (default: False)

**Key Methods:**

#### `deseq2()`
Run the complete DESeq2 pipeline for normalization and dispersion/LFC fitting.

**Steps performed:**
1. Compute normalization factors (size factors)
2. Fit genewise dispersions
3. Fit dispersion trend curve
4. Calculate dispersion priors
5. Fit MAP (maximum a posteriori) dispersions
6. Fit log fold changes
7. Calculate Cook's distances for outlier detection
8. Optionally refit if `refit_cooks=True`

**Returns:** None (modifies object in-place)

#### `to_picklable_anndata()`
Convert the DeseqDataSet to an AnnData object that can be saved with pickle.

**Returns:** AnnData object with:
- `X`: count data matrix
- `obs`: sample-level metadata (1D)
- `var`: gene-level metadata (1D)
- `varm`: gene-level multi-dimensional data (e.g., LFC estimates)

**Usage:**
```python
import pickle
with open("result_adata.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

**Attributes (after running deseq2()):**
- `layers`: dict containing various matrices (normalized counts, etc.)
- `varm`: dict containing gene-level results (log fold changes, dispersions, etc.)
- `obsm`: dict containing sample-level information
- `uns`: dict containing global parameters

---

### DeseqStats

Class for performing statistical tests and computing p-values for differential expression.

**Purpose:** Facilitates PyDESeq2 statistical tests using Wald tests and optional LFC shrinkage.

**Initialization Parameters:**
- `dds`: DeseqDataSet object that has been processed with `deseq2()`
- `contrast`: list or None, specifies the contrast for testing
  - Format: `[variable, test_level, reference_level]`
  - Example: `["condition", "treated", "control"]` tests treated vs control
  - If None, uses the last coefficient in the design formula
- `alpha`: float, significance threshold for independent filtering (default: 0.05)
- `cooks_filter`: bool, whether to filter outliers based on Cook's distance (default: True)
- `independent_filter`: bool, whether to perform independent filtering (default: True)
- `n_cpus`: int, number of CPUs for parallel processing (optional)
- `quiet`: bool, suppress progress messages (default: False)

**Key Methods:**

#### `summary()`
Run Wald tests and compute p-values and adjusted p-values.

**Steps performed:**
1. Run Wald statistical tests for specified contrast
2. Optional Cook's distance filtering
3. Optional independent filtering to remove low-power tests
4. Multiple testing correction (Benjamini-Hochberg procedure)

**Returns:** None (results stored in `results_df` attribute)

**Result DataFrame columns:**
- `baseMean`: mean normalized count across all samples
- `log2FoldChange`: log2 fold change between conditions
- `lfcSE`: standard error of the log2 fold change
- `stat`: Wald test statistic
- `pvalue`: raw p-value
- `padj`: adjusted p-value (FDR-corrected)

#### `lfc_shrink(coeff=None)`
Apply shrinkage to log fold changes using the apeGLM method.

**Purpose:** Reduces noise in LFC estimates for better visualization and ranking, especially for genes with low counts or high variability.

**Parameters:**
- `coeff`: str or None, coefficient name to shrink (if None, uses the coefficient from the contrast)

**Important:** Shrinkage is applied only for visualization/ranking purposes. The statistical test results (p-values, adjusted p-values) remain unchanged.

**Returns:** None (updates `results_df` with shrunk LFCs)

**Attributes:**
- `results_df`: pandas DataFrame containing test results (available after `summary()`)

---

## Utility Functions

### `pydeseq2.utils.load_example_data(modality="single-factor")`

Load synthetic example datasets for testing and tutorials.

**Parameters:**
- `modality`: str, either "single-factor" or "multi-factor"

**Returns:** tuple of (counts_df, metadata_df)
- `counts_df`: pandas DataFrame with synthetic count data
- `metadata_df`: pandas DataFrame with sample annotations

---

## Preprocessing Module

The `pydeseq2.preprocessing` module provides utilities for data preparation.

**Common operations:**
- Gene filtering based on minimum read counts
- Sample filtering based on metadata criteria
- Data transformation and normalization

---

## Inference Classes

### Inference
Abstract base class defining the interface for DESeq2-related inference methods.

### DefaultInference
Default implementation of inference methods using scipy, sklearn, and numpy.

**Purpose:** Provides the mathematical implementations for:
- GLM (Generalized Linear Model) fitting
- Dispersion estimation
- Trend curve fitting
- Statistical testing

---

## Data Structure Requirements

### Count Matrix
- **Shape:** (samples × genes)
- **Type:** pandas DataFrame
- **Values:** Non-negative integers (raw read counts)
- **Index:** Sample identifiers (must match metadata index)
- **Columns:** Gene identifiers

### Metadata
- **Shape:** (samples × variables)
- **Type:** pandas DataFrame
- **Index:** Sample identifiers (must match count matrix index)
- **Columns:** Experimental factors (e.g., "condition", "batch", "group")
- **Values:** Categorical or continuous variables used in the design formula

### Important Notes
- Sample order must match between counts and metadata
- Missing values in metadata should be handled before analysis
- Gene names should be unique
- Count files often need transposition: `counts_df = counts_df.T`

---

## Common Workflow Pattern

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Initialize dataset
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)

# 2. Fit dispersions and LFCs
dds.deseq2()

# 3. Perform statistical testing
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],
    alpha=0.05
)
ds.summary()

# 4. Optional: Shrink LFCs for visualization
ds.lfc_shrink()

# 5. Access results
results = ds.results_df
```

---

## Version Compatibility

PyDESeq2 aims to match the default settings of DESeq2 v1.34.0. Some differences may exist as it is a from-scratch reimplementation in Python.

**Tested with:**
- Python 3.10-3.11
- anndata 0.8.0+
- numpy 1.23.0+
- pandas 1.4.3+
- scikit-learn 1.1.1+
- scipy 1.11.0+

---

## Reference: Workflow_Guide

# PyDESeq2 Workflow Guide

This document provides detailed step-by-step workflows for common PyDESeq2 analysis patterns.

## Table of Contents
1. [Complete Differential Expression Analysis](#complete-differential-expression-analysis)
2. [Data Loading and Preparation](#data-loading-and-preparation)
3. [Single-Factor Analysis](#single-factor-analysis)
4. [Multi-Factor Analysis](#multi-factor-analysis)
5. [Result Export and Visualization](#result-export-and-visualization)
6. [Common Patterns and Best Practices](#common-patterns-and-best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Complete Differential Expression Analysis

### Overview
A standard PyDESeq2 analysis consists of 12 main steps across two phases:

**Phase 1: Read Counts Modeling (Steps 1-7)**
- Normalization and dispersion estimation
- Log fold-change fitting
- Outlier detection

**Phase 2: Statistical Analysis (Steps 8-12)**
- Wald testing
- Multiple testing correction
- Optional LFC shrinkage

### Full Workflow Code

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Load data
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpose if needed
metadata = pd.read_csv("metadata.csv", index_col=0)

# Filter low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# Remove samples with missing metadata
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]

# Initialize DeseqDataSet
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)

# Run normalization and fitting
dds.deseq2()

# Perform statistical testing
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],
    alpha=0.05,
    cooks_filter=True,
    independent_filter=True
)
ds.summary()

# Optional: Apply LFC shrinkage for visualization
ds.lfc_shrink()

# Access results
results = ds.results_df
print(results.head())
```

---

## Data Loading and Preparation

### Loading CSV Files

Count data typically comes in genes × samples format but needs to be transposed:

```python
import pandas as pd

# Load count matrix (genes × samples)
counts_df = pd.read_csv("counts.csv", index_col=0)

# Transpose to samples × genes
counts_df = counts_df.T

# Load metadata (already in samples × variables format)
metadata = pd.read_csv("metadata.csv", index_col=0)
```

### Loading from Other Formats

**From TSV:**
```python
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T
metadata = pd.read_csv("metadata.tsv", sep="\t", index_col=0)
```

**From saved pickle:**
```python
import pickle

with open("counts.pkl", "rb") as f:
    counts_df = pickle.load(f)

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)
```

**From AnnData:**
```python
import anndata as ad

adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(
    adata.X,
    index=adata.obs_names,
    columns=adata.var_names
)
metadata = adata.obs
```

### Data Filtering

**Filter genes with low counts:**
```python
# Remove genes with fewer than 10 total reads
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]
```

**Filter samples with missing metadata:**
```python
# Remove samples where 'condition' column is NA
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

**Filter by multiple criteria:**
```python
# Keep only samples that meet all criteria
mask = (
    ~metadata.condition.isna() &
    (metadata.batch.isin(["batch1", "batch2"])) &
    (metadata.age >= 18)
)
counts_df = counts_df.loc[mask]
metadata = metadata.loc[mask]
```

### Data Validation

**Check data structure:**
```python
print(f"Counts shape: {counts_df.shape}")  # Should be (samples, genes)
print(f"Metadata shape: {metadata.shape}")  # Should be (samples, variables)
print(f"Indices match: {all(counts_df.index == metadata.index)}")

# Check for negative values
assert (counts_df >= 0).all().all(), "Counts must be non-negative"

# Check for non-integer values
assert counts_df.applymap(lambda x: x == int(x)).all().all(), "Counts must be integers"
```

---

## Single-Factor Analysis

### Simple Two-Group Comparison

Compare treated vs control samples:

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Design: model expression as a function of condition
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition"
)

dds.deseq2()

# Test treated vs control
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"]
)
ds.summary()

# Results
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

### Multiple Pairwise Comparisons

When comparing multiple groups:

```python
# Test each treatment vs control
treatments = ["treated_A", "treated_B", "treated_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(
        dds,
        contrast=["condition", treatment, "control"]
    )
    ds.summary()
    all_results[treatment] = ds.results_df

# Compare results across treatments
for name, results in all_results.items():
    sig = results[results.padj < 0.05]
    print(f"{name}: {len(sig)} significant genes")
```

---

## Multi-Factor Analysis

### Two-Factor Design

Account for batch effects while testing condition:

```python
# Design includes both batch and condition
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~batch + condition"
)

dds.deseq2()

# Test condition effect while controlling for batch
ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"]
)
ds.summary()
```

### Interaction Effects

Test whether treatment effect differs between groups:

```python
# Design includes interaction term
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~group + condition + group:condition"
)

dds.deseq2()

# Test the interaction term
ds = DeseqStats(dds, contrast=["group:condition", ...])
ds.summary()
```

### Continuous Covariates

Include continuous variables like age:

```python
# Ensure age is numeric in metadata
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~age + condition"
)

dds.deseq2()
```

---

## Result Export and Visualization

### Saving Results

**Export as CSV:**
```python
# Save statistical results
ds.results_df.to_csv("deseq2_results.csv")

# Save significant genes only
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# Save with sorted results
sorted_results = ds.results_df.sort_values("padj")
sorted_results.to_csv("sorted_results.csv")
```

**Save DeseqDataSet:**
```python
import pickle

# Save as AnnData for later use
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

**Load saved results:**
```python
# Load results
results = pd.read_csv("deseq2_results.csv", index_col=0)

# Load AnnData
with open("dds_result.pkl", "rb") as f:
    adata = pickle.load(f)
```

### Basic Visualization

**Volcano plot:**
```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(
    results.log2FoldChange,
    results["-log10(padj)"],
    alpha=0.5,
    s=10
)
plt.axhline(-np.log10(0.05), color='red', linestyle='--', label='padj=0.05')
plt.axvline(1, color='gray', linestyle='--')
plt.axvline(-1, color='gray', linestyle='--')
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

**MA plot:**
```python
plt.figure(figsize=(10, 6))
plt.scatter(
    np.log10(results.baseMean + 1),
    results.log2FoldChange,
    alpha=0.5,
    s=10,
    c=(results.padj < 0.05),
    cmap='bwr'
)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

---

## Common Patterns and Best Practices

### 1. Data Preprocessing Checklist

Before running PyDESeq2:
- ✓ Ensure counts are non-negative integers
- ✓ Verify samples × genes orientation
- ✓ Check that sample names match between counts and metadata
- ✓ Remove or handle missing metadata values
- ✓ Filter low-count genes (typically < 10 total reads)
- ✓ Verify experimental factors are properly encoded

### 2. Design Formula Best Practices

**Order matters:** Put adjustment variables before the variable of interest
```python
# Correct: control for batch, test condition
design = "~batch + condition"

# Less ideal: condition listed first
design = "~condition + batch"
```

**Use categorical for discrete variables:**
```python
# Ensure proper data types
metadata["condition"] = metadata["condition"].astype("category")
metadata["batch"] = metadata["batch"].astype("category")
```

### 3. Statistical Testing Guidelines

**Set appropriate alpha:**
```python
# Standard significance threshold
ds = DeseqStats(dds, alpha=0.05)

# More stringent for exploratory analysis
ds = DeseqStats(dds, alpha=0.01)
```

**Use independent filtering:**
```python
# Recommended: filter low-power tests
ds = DeseqStats(dds, independent_filter=True)

# Only disable if you have specific reasons
ds = DeseqStats(dds, independent_filter=False)
```

### 4. LFC Shrinkage

**When to use:**
- For visualization (volcano plots, heatmaps)
- For ranking genes by effect size
- When prioritizing genes for follow-up

**When NOT to use:**
- For reporting statistical significance (use unshrunken p-values)
- For gene set enrichment analysis (typically uses unshrunken values)

```python
# Save both versions
ds.results_df.to_csv("results_unshrunken.csv")
ds.lfc_shrink()
ds.results_df.to_csv("results_shrunken.csv")
```

### 5. Memory Management

For large datasets:
```python
# Use parallel processing
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    n_cpus=4  # Adjust based on available cores
)

# Process in batches if needed
# (split genes into chunks, analyze separately, combine results)
```

---

## Troubleshooting

### Error: Index mismatch between counts and metadata

**Problem:** Sample names don't match
```
KeyError: Sample names in counts and metadata don't match
```

**Solution:**
```python
# Check indices
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# Align if needed
common_samples = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common_samples]
metadata = metadata.loc[common_samples]
```

### Error: All genes have zero counts

**Problem:** Data might need transposition
```
ValueError: All genes have zero total counts
```

**Solution:**
```python
# Check data orientation
print(f"Counts shape: {counts_df.shape}")

# If genes > samples, likely needs transpose
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### Warning: Many genes filtered out

**Problem:** Too many low-count genes removed

**Check:**
```python
# See distribution of gene counts
print(counts_df.sum(axis=0).describe())

# Visualize
import matplotlib.pyplot as plt
plt.hist(counts_df.sum(axis=0), bins=50, log=True)
plt.xlabel("Total counts per gene")
plt.ylabel("Frequency")
plt.show()
```

**Adjust filtering if needed:**
```python
# Try lower threshold
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 5]
```

### Error: Design matrix is not full rank

**Problem:** Confounded design (e.g., all treated samples in one batch)

**Solution:**
```python
# Check design confounding
print(pd.crosstab(metadata.condition, metadata.batch))

# Either remove confounded variable or add interaction term
design = "~condition"  # Drop batch
# OR
design = "~condition + batch + condition:batch"  # Add interaction
```

### Issue: No significant genes found

**Possible causes:**
1. Small effect sizes
2. High biological variability
3. Insufficient sample size
4. Technical issues (batch effects, outliers)

**Diagnostics:**
```python
# Check dispersion estimates
import matplotlib.pyplot as plt
dispersions = dds.varm["dispersions"]
plt.hist(dispersions, bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.show()

# Check size factors (should be close to 1)
print("Size factors:", dds.obsm["size_factors"])

# Look at top genes even if not significant
top_genes = ds.results_df.nsmallest(20, "pvalue")
print(top_genes)
```

### Memory errors on large datasets

**Solutions:**
```python
# 1. Use fewer CPUs (paradoxically can help)
dds = DeseqDataSet(..., n_cpus=1)

# 2. Filter more aggressively
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 20]

# 3. Process in batches
# Split analysis by gene subsets and combine results
```
