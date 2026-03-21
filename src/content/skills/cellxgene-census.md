---
title: "Cellxgene Census"
description: "Query the CELLxGENE Census (61M+ cells) programmatically. Use when you need expression data across tissues, diseases, or cell types from the largest curated single-cell atlas. Best for population-scale queries, reference atlas comparisons. For ana..."
category: "development"
source: "community"
author: "Community"
tags: ["cellxgene", "census"]
date: 2026-03-20
---

# CZ CELLxGENE Census

## Overview

The CZ CELLxGENE Census provides programmatic access to a comprehensive, versioned collection of standardized single-cell genomics data from CZ CELLxGENE Discover. This skill enables efficient querying and analysis of millions of cells across thousands of datasets.

The Census includes:
- **61+ million cells** from human and mouse
- **Standardized metadata** (cell types, tissues, diseases, donors)
- **Raw gene expression** matrices
- **Pre-calculated embeddings** and statistics
- **Integration with PyTorch, scanpy, and other analysis tools**

## When to Use This Skill

This skill should be used when:
- Querying single-cell expression data by cell type, tissue, or disease
- Exploring available single-cell datasets and metadata
- Training machine learning models on single-cell data
- Performing large-scale cross-dataset analyses
- Integrating Census data with scanpy or other analysis frameworks
- Computing statistics across millions of cells
- Accessing pre-calculated embeddings or model predictions

## Installation and Setup

Install the Census API:
```bash
uv pip install cellxgene-census
```

For machine learning workflows, install additional dependencies:
```bash
uv pip install cellxgene-census[experimental]
```

## Core Workflow Patterns

### 1. Opening the Census

Always use the context manager to ensure proper resource cleanup:

```python
import cellxgene_census

# Open latest stable version
with cellxgene_census.open_soma() as census:
    # Work with census data

# Open specific version for reproducibility
with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    # Work with census data
```

**Key points:**
- Use context manager (`with` statement) for automatic cleanup
- Specify `census_version` for reproducible analyses
- Default opens latest "stable" release

### 2. Exploring Census Information

Before querying expression data, explore available datasets and metadata.

**Access summary information:**
```python
# Get summary statistics
summary = census["census_info"]["summary"].read().concat().to_pandas()
print(f"Total cells: {summary['total_cell_count'][0]}")

# Get all datasets
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# Filter datasets by criteria
covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

**Query cell metadata to understand available data:**
```python
# Get unique cell types in a tissue
cell_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["cell_type"]
)
unique_cell_types = cell_metadata["cell_type"].unique()
print(f"Found {len(unique_cell_types)} cell types in brain")

# Count cells by tissue
tissue_counts = cell_metadata.groupby("tissue_general").size()
```

**Important:** Always filter for `is_primary_data == True` to avoid counting duplicate cells unless specifically analyzing duplicates.

### 3. Querying Expression Data (Small to Medium Scale)

For queries returning < 100k cells that fit in memory, use `get_anndata()`:

```python
# Basic query with cell type and tissue filters
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",  # or "Mus musculus"
    obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    obs_column_names=["assay", "disease", "sex", "donor_id"],
)

# Query specific genes with multiple filters
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19', 'FOXP3']",
    obs_value_filter="cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True",
    obs_column_names=["cell_type", "tissue_general", "donor_id"],
)
```

**Filter syntax:**
- Use `obs_value_filter` for cell filtering
- Use `var_value_filter` for gene filtering
- Combine conditions with `and`, `or`
- Use `in` for multiple values: `tissue in ['lung', 'liver']`
- Select only needed columns with `obs_column_names`

**Getting metadata separately:**
```python
# Query cell metadata
cell_metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general", "donor_id"]
)

# Query gene metadata
gene_metadata = cellxgene_census.get_var(
    census, "homo_sapiens",
    value_filter="feature_name in ['CD4', 'CD8A']",
    column_names=["feature_id", "feature_name", "feature_length"]
)
```

### 4. Large-Scale Queries (Out-of-Core Processing)

For queries exceeding available RAM, use `axis_query()` with iterative processing:

```python
import tiledbsoma as soma

# Create axis query
query = census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    )
)

# Iterate through expression matrix in chunks
iterator = query.X("raw").tables()
for batch in iterator:
    # batch is a pyarrow.Table with columns:
    # - soma_data: expression value
    # - soma_dim_0: cell (obs) coordinate
    # - soma_dim_1: gene (var) coordinate
    process_batch(batch)
```

**Computing incremental statistics:**
```python
# Example: Calculate mean expression
n_observations = 0
sum_values = 0.0

iterator = query.X("raw").tables()
for batch in iterator:
    values = batch["soma_data"].to_numpy()
    n_observations += len(values)
    sum_values += values.sum()

mean_expression = sum_values / n_observations
```

### 5. Machine Learning with PyTorch

For training models, use the experimental PyTorch integration:

```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    # Create dataloader
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Training loop
    for epoch in range(num_epochs):
        for batch in dataloader:
            X = batch["X"]  # Gene expression tensor
            labels = batch["obs"]["cell_type"]  # Cell type labels

            # Forward pass
            outputs = model(X)
            loss = criterion(outputs, labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

**Train/test splitting:**
```python
from cellxgene_census.experimental.ml import ExperimentDataset

# Create dataset from experiment
dataset = ExperimentDataset(
    experiment_axis_query,
    layer_name="raw",
    obs_column_names=["cell_type"],
    batch_size=128,
)

# Split into train and test
train_dataset, test_dataset = dataset.random_split(
    split=[0.8, 0.2],
    seed=42
)
```

### 6. Integration with Scanpy

Seamlessly integrate Census data with scanpy workflows:

```python
import scanpy as sc

# Load data from Census
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
)

# Standard scanpy workflow
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Dimensionality reduction
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Visualization
sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

### 7. Multi-Dataset Integration

Query and integrate multiple datasets:

```python
# Strategy 1: Query multiple tissues separately
tissues = ["lung", "liver", "kidney"]
adatas = []

for tissue in tissues:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    adata.obs["tissue"] = tissue
    adatas.append(adata)

# Concatenate
combined = adatas[0].concatenate(adatas[1:])

# Strategy 2: Query multiple datasets directly
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
)
```

## Key Concepts and Best Practices

### Always Filter for Primary Data
Unless analyzing duplicates, always include `is_primary_data == True` in queries to avoid counting cells multiple times:
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### Specify Census Version for Reproducibility
Always specify the Census version in production analyses:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### Estimate Query Size Before Loading
For large queries, first check the number of cells to avoid memory issues:
```python
# Get cell count
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["soma_joinid"]
)
n_cells = len(metadata)
print(f"Query will return {n_cells:,} cells")

# If too large (>100k), use out-of-core processing
```

### Use tissue_general for Broader Groupings
The `tissue_general` field provides coarser categories than `tissue`, useful for cross-tissue analyses:
```python
# Broader grouping
obs_value_filter="tissue_general == 'immune system'"

# Specific tissue
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### Select Only Needed Columns
Minimize data transfer by specifying only required metadata columns:
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # Not all columns
```

### Check Dataset Presence for Gene-Specific Queries
When analyzing specific genes, verify which datasets measured them:
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### Two-Step Workflow: Explore Then Query
First explore metadata to understand available data, then query expression:
```python
# Step 1: Explore what's available
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general"]
)
print(metadata.value_counts())

# Step 2: Query based on findings
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
)
```

## Available Metadata Fields

### Cell Metadata (obs)
Key fields for filtering:
- `cell_type`, `cell_type_ontology_term_id`
- `tissue`, `tissue_general`, `tissue_ontology_term_id`
- `disease`, `disease_ontology_term_id`
- `assay`, `assay_ontology_term_id`
- `donor_id`, `sex`, `self_reported_ethnicity`
- `development_stage`, `development_stage_ontology_term_id`
- `dataset_id`
- `is_primary_data` (Boolean: True = unique cell)

### Gene Metadata (var)
- `feature_id` (Ensembl gene ID, e.g., "ENSG00000161798")
- `feature_name` (Gene symbol, e.g., "FOXP2")
- `feature_length` (Gene length in base pairs)

## Reference Documentation

This skill includes detailed reference documentation:

### references/census_schema.md
Comprehensive documentation of:
- Census data structure and organization
- All available metadata fields
- Value filter syntax and operators
- SOMA object types
- Data inclusion criteria

**When to read:** When you need detailed schema information, full list of metadata fields, or complex filter syntax.

### references/common_patterns.md
Examples and patterns for:
- Exploratory queries (metadata only)
- Small-to-medium queries (AnnData)
- Large queries (out-of-core processing)
- PyTorch integration
- Scanpy integration workflows
- Multi-dataset integration
- Best practices and common pitfalls

**When to read:** When implementing specific query patterns, looking for code examples, or troubleshooting common issues.

## Common Use Cases

### Use Case 1: Explore Cell Types in a Tissue
```python
with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### Use Case 2: Query Marker Gene Expression
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### Use Case 3: Train Cell Type Classifier
```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Train model
    for epoch in range(epochs):
        for batch in dataloader:
            # Training logic
            pass
```

### Use Case 4: Cross-Tissue Analysis
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # Analyze macrophage differences across tissues
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```

## Troubleshooting

### Query Returns Too Many Cells
- Add more specific filters to reduce scope
- Use `tissue` instead of `tissue_general` for finer granularity
- Filter by specific `dataset_id` if known
- Switch to out-of-core processing for large queries

### Memory Errors
- Reduce query scope with more restrictive filters
- Select fewer genes with `var_value_filter`
- Use out-of-core processing with `axis_query()`
- Process data in batches

### Duplicate Cells in Results
- Always include `is_primary_data == True` in filters
- Check if intentionally querying across multiple datasets

### Gene Not Found
- Verify gene name spelling (case-sensitive)
- Try Ensembl ID with `feature_id` instead of `feature_name`
- Check dataset presence matrix to see if gene was measured
- Some genes may have been filtered during Census construction

### Version Inconsistencies
- Always specify `census_version` explicitly
- Use same version across all analyses
- Check release notes for version-specific changes

---

## Reference: Census_Schema

# CZ CELLxGENE Census Data Schema Reference

## Overview

The CZ CELLxGENE Census is a versioned collection of single-cell data built on the TileDB-SOMA framework. This reference documents the data structure, available metadata fields, and query syntax.

## High-Level Structure

The Census is organized as a `SOMACollection` with two main components:

### 1. census_info
Summary information including:
- **summary**: Build date, cell counts, dataset statistics
- **datasets**: All datasets from CELLxGENE Discover with metadata
- **summary_cell_counts**: Cell counts stratified by metadata categories

### 2. census_data
Organism-specific `SOMAExperiment` objects:
- **"homo_sapiens"**: Human single-cell data
- **"mus_musculus"**: Mouse single-cell data

## Data Structure Per Organism

Each organism experiment contains:

### obs (Cell Metadata)
Cell-level annotations stored as a `SOMADataFrame`. Access via:
```python
census["census_data"]["homo_sapiens"].obs
```

### ms["RNA"] (Measurement)
RNA measurement data including:
- **X**: Data matrices with layers:
  - `raw`: Raw count data
  - `normalized`: (if available) Normalized counts
- **var**: Gene metadata
- **feature_dataset_presence_matrix**: Sparse boolean array showing which genes were measured in each dataset

## Cell Metadata Fields (obs)

### Required/Core Fields

**Identity & Dataset:**
- `soma_joinid`: Unique integer identifier for joins
- `dataset_id`: Source dataset identifier
- `is_primary_data`: Boolean flag (True = unique cell, False = duplicate across datasets)

**Cell Type:**
- `cell_type`: Human-readable cell type name
- `cell_type_ontology_term_id`: Standardized ontology term (e.g., "CL:0000236")

**Tissue:**
- `tissue`: Specific tissue name
- `tissue_general`: Broader tissue category (useful for grouping)
- `tissue_ontology_term_id`: Standardized ontology term

**Assay:**
- `assay`: Sequencing technology used
- `assay_ontology_term_id`: Standardized ontology term

**Disease:**
- `disease`: Disease status or condition
- `disease_ontology_term_id`: Standardized ontology term

**Donor:**
- `donor_id`: Unique donor identifier
- `sex`: Biological sex (male, female, unknown)
- `self_reported_ethnicity`: Ethnicity information
- `development_stage`: Life stage (adult, child, embryonic, etc.)
- `development_stage_ontology_term_id`: Standardized ontology term

**Organism:**
- `organism`: Scientific name (Homo sapiens, Mus musculus)
- `organism_ontology_term_id`: Standardized ontology term

**Technical:**
- `suspension_type`: Sample preparation type (cell, nucleus, na)

## Gene Metadata Fields (var)

Access via:
```python
census["census_data"]["homo_sapiens"].ms["RNA"].var
```

**Available Fields:**
- `soma_joinid`: Unique integer identifier for joins
- `feature_id`: Ensembl gene ID (e.g., "ENSG00000161798")
- `feature_name`: Gene symbol (e.g., "FOXP2")
- `feature_length`: Gene length in base pairs

## Value Filter Syntax

Queries use Python-like expressions for filtering. The syntax is processed by TileDB-SOMA.

### Comparison Operators
- `==`: Equal to
- `!=`: Not equal to
- `<`, `>`, `<=`, `>=`: Numeric comparisons
- `in`: Membership test (e.g., `feature_id in ['ENSG00000161798', 'ENSG00000188229']`)

### Logical Operators
- `and`, `&`: Logical AND
- `or`, `|`: Logical OR

### Examples

**Single condition:**
```python
value_filter="cell_type == 'B cell'"
```

**Multiple conditions with AND:**
```python
value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True"
```

**Using IN for multiple values:**
```python
value_filter="tissue in ['lung', 'liver', 'kidney']"
```

**Complex condition:**
```python
value_filter="(cell_type == 'neuron' or cell_type == 'astrocyte') and disease != 'normal'"
```

**Filtering genes:**
```python
var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']"
```

## Data Inclusion Criteria

The Census includes all data from CZ CELLxGENE Discover meeting:

1. **Species**: Human (*Homo sapiens*) or mouse (*Mus musculus*)
2. **Technology**: Approved sequencing technologies for RNA
3. **Count Type**: Raw counts only (no processed/normalized-only data)
4. **Metadata**: Standardized following CELLxGENE schema
5. **Both spatial and non-spatial data**: Includes traditional and spatial transcriptomics

## Important Data Characteristics

### Duplicate Cells
Cells may appear across multiple datasets. Use `is_primary_data == True` to filter for unique cells in most analyses.

### Count Types
The Census includes:
- **Molecule counts**: From UMI-based methods
- **Full-gene sequencing read counts**: From non-UMI methods
These may need different normalization approaches.

### Versioning
Census releases are versioned (e.g., "2023-07-25", "stable"). Always specify version for reproducible analysis:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

## Dataset Presence Matrix

Access which genes were measured in each dataset:
```python
presence_matrix = census["census_data"]["homo_sapiens"].ms["RNA"]["feature_dataset_presence_matrix"]
```

This sparse boolean matrix helps understand:
- Gene coverage across datasets
- Which datasets to include for specific gene analyses
- Technical batch effects related to gene coverage

## SOMA Object Types

Core TileDB-SOMA objects used:
- **DataFrame**: Tabular data (obs, var)
- **SparseNDArray**: Sparse matrices (X layers, presence matrix)
- **DenseNDArray**: Dense arrays (less common)
- **Collection**: Container for related objects
- **Experiment**: Top-level container for measurements
- **SOMAScene**: Spatial transcriptomics scenes
- **obs_spatial_presence**: Spatial data availability

---

## Reference: Common_Patterns

# Common Query Patterns and Best Practices

## Query Pattern Categories

### 1. Exploratory Queries (Metadata Only)

Use when exploring available data without loading expression matrices.

**Pattern: Get unique cell types in a tissue**
```python
import cellxgene_census

with cellxgene_census.open_soma() as census:
    cell_metadata = cellxgene_census.get_obs(
        census,
        "homo_sapiens",
        value_filter="tissue_general == 'brain' and is_primary_data == True",
        column_names=["cell_type"]
    )
    unique_cell_types = cell_metadata["cell_type"].unique()
    print(f"Found {len(unique_cell_types)} unique cell types")
```

**Pattern: Count cells by condition**
```python
cell_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="disease != 'normal' and is_primary_data == True",
    column_names=["disease", "tissue_general"]
)
counts = cell_metadata.groupby(["disease", "tissue_general"]).size()
```

**Pattern: Explore dataset information**
```python
# Access datasets table
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# Filter for specific criteria
covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

### 2. Small-to-Medium Queries (AnnData)

Use `get_anndata()` when results fit in memory (typically < 100k cells).

**Pattern: Tissue-specific cell type query**
```python
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    obs_column_names=["assay", "disease", "sex", "donor_id"],
)
```

**Pattern: Gene-specific query with multiple genes**
```python
marker_genes = ["CD4", "CD8A", "CD19", "FOXP3"]

# First get gene IDs
gene_metadata = cellxgene_census.get_var(
    census, "homo_sapiens",
    value_filter=f"feature_name in {marker_genes}",
    column_names=["feature_id", "feature_name"]
)
gene_ids = gene_metadata["feature_id"].tolist()

# Query with gene filter
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    var_value_filter=f"feature_id in {gene_ids}",
    obs_value_filter="cell_type == 'T cell' and is_primary_data == True",
)
```

**Pattern: Multi-tissue query**
```python
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
    obs_column_names=["cell_type", "tissue_general", "dataset_id"],
)
```

**Pattern: Disease-specific query**
```python
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and tissue_general == 'lung' and is_primary_data == True",
)
```

### 3. Large Queries (Out-of-Core Processing)

Use `axis_query()` for queries that exceed available RAM.

**Pattern: Iterative processing**
```python
import pyarrow as pa

# Create query
query = census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    )
)

# Iterate through X matrix in chunks
iterator = query.X("raw").tables()
for batch in iterator:
    # Process batch (a pyarrow.Table)
    # batch has columns: soma_data, soma_dim_0, soma_dim_1
    process_batch(batch)
```

**Pattern: Incremental statistics (mean/variance)**
```python
# Using Welford's online algorithm
n = 0
mean = 0
M2 = 0

iterator = query.X("raw").tables()
for batch in iterator:
    values = batch["soma_data"].to_numpy()
    for x in values:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2

variance = M2 / (n - 1) if n > 1 else 0
```

### 4. PyTorch Integration (Machine Learning)

Use `experiment_dataloader()` for training models.

**Pattern: Create training dataloader**
```python
from cellxgene_census.experimental.ml import experiment_dataloader
import torch

with cellxgene_census.open_soma() as census:
    # Create dataloader
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Training loop
    for epoch in range(num_epochs):
        for batch in dataloader:
            X = batch["X"]  # Gene expression
            labels = batch["obs"]["cell_type"]  # Cell type labels
            # Train model...
```

**Pattern: Train/test split**
```python
from cellxgene_census.experimental.ml import ExperimentDataset

# Create dataset from query
dataset = ExperimentDataset(
    experiment_axis_query,
    layer_name="raw",
    obs_column_names=["cell_type"],
    batch_size=128,
)

# Split data
train_dataset, test_dataset = dataset.random_split(
    split=[0.8, 0.2],
    seed=42
)

# Create loaders
train_loader = experiment_dataloader(train_dataset)
test_loader = experiment_dataloader(test_dataset)
```

### 5. Integration Workflows

**Pattern: Scanpy integration**
```python
import scanpy as sc

# Load data
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and is_primary_data == True",
)

# Standard scanpy workflow
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
sc.pl.umap(adata, color=["cell_type", "tissue_general"])
```

**Pattern: Multi-dataset integration**
```python
# Query multiple datasets separately
datasets_to_integrate = ["dataset_id_1", "dataset_id_2", "dataset_id_3"]

adatas = []
for dataset_id in datasets_to_integrate:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"dataset_id == '{dataset_id}' and is_primary_data == True",
    )
    adatas.append(adata)

# Integrate using scanorama, harmony, or other tools
import scanpy.external as sce
sce.pp.scanorama_integrate(adatas)
```

## Best Practices

### 1. Always Filter for Primary Data
Unless specifically analyzing duplicates, always include `is_primary_data == True`:
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### 2. Specify Census Version
For reproducible analysis, always specify the Census version:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### 3. Use Context Manager
Always use the context manager to ensure proper cleanup:
```python
with cellxgene_census.open_soma() as census:
    # Your code here
```

### 4. Select Only Needed Columns
Minimize data transfer by selecting only required metadata columns:
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # Not all columns
```

### 5. Check Dataset Presence for Gene Queries
When analyzing specific genes, check which datasets measured them:
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### 6. Use tissue_general for Broader Queries
`tissue_general` provides coarser groupings than `tissue`, useful for cross-tissue analyses:
```python
# Better for broad queries
obs_value_filter="tissue_general == 'immune system'"

# Use specific tissue when needed
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### 7. Combine Metadata Exploration with Expression Queries
First explore metadata to understand available data, then query expression:
```python
# Step 1: Explore
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19'",
    column_names=["cell_type", "tissue_general"]
)
print(metadata.value_counts())

# Step 2: Query based on findings
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
)
```

### 8. Memory Management for Large Queries
For large queries, check estimated size before loading:
```python
# Get cell count first
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["soma_joinid"]
)
n_cells = len(metadata)
print(f"Query will return {n_cells} cells")

# If too large, use out-of-core processing or further filtering
```

### 9. Leverage Ontology Terms for Consistency
When possible, use ontology term IDs instead of free text:
```python
# More reliable than cell_type == 'B cell' across datasets
obs_value_filter="cell_type_ontology_term_id == 'CL:0000236'"
```

### 10. Batch Processing Pattern
For systematic analyses across multiple conditions:
```python
tissues = ["lung", "liver", "kidney", "heart"]
results = {}

for tissue in tissues:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    # Perform analysis
    results[tissue] = analyze(adata)
```

## Common Pitfalls to Avoid

1. **Not filtering for is_primary_data**: Leads to counting duplicate cells
2. **Loading too much data**: Use metadata queries to estimate size first
3. **Not using context manager**: Can cause resource leaks
4. **Inconsistent versioning**: Results not reproducible without specifying version
5. **Overly broad queries**: Start with focused queries, expand as needed
6. **Ignoring dataset presence**: Some genes not measured in all datasets
7. **Wrong count normalization**: Be aware of UMI vs read count differences
