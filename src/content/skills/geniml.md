---
title: "Geniml"
description: "This skill should be used when working with genomic interval data (BED files) for machine learning tasks. Use for training region embeddings (Region2Vec, BEDspace), single-cell ATAC-seq analysis (scEmbed), building consensus peaks (universes), or ..."
category: "research"
source: "community"
author: "Community"
tags: ["geniml"]
date: 2026-03-20
---

# Geniml: Genomic Interval Machine Learning

## Overview

Geniml is a Python package for building machine learning models on genomic interval data from BED files. It provides unsupervised methods for learning embeddings of genomic regions, single cells, and metadata labels, enabling similarity searches, clustering, and downstream ML tasks.

## Installation

Install geniml using uv:

```bash
uv uv pip install geniml
```

For ML dependencies (PyTorch, etc.):

```bash
uv uv pip install 'geniml[ml]'
```

Development version from GitHub:

```bash
uv uv pip install git+https://github.com/databio/geniml.git
```

## Core Capabilities

Geniml provides five primary capabilities, each detailed in dedicated reference files:

### 1. Region2Vec: Genomic Region Embeddings

Train unsupervised embeddings of genomic regions using word2vec-style learning.

**Use for:** Dimensionality reduction of BED files, region similarity analysis, feature vectors for downstream ML.

**Workflow:**
1. Tokenize BED files using a universe reference
2. Train Region2Vec model on tokens
3. Generate embeddings for regions

**Reference:** See `references/region2vec.md` for detailed workflow, parameters, and examples.

### 2. BEDspace: Joint Region and Metadata Embeddings

Train shared embeddings for region sets and metadata labels using StarSpace.

**Use for:** Metadata-aware searches, cross-modal queries (region→label or label→region), joint analysis of genomic content and experimental conditions.

**Workflow:**
1. Preprocess regions and metadata
2. Train BEDspace model
3. Compute distances
4. Query across regions and labels

**Reference:** See `references/bedspace.md` for detailed workflow, search types, and examples.

### 3. scEmbed: Single-Cell Chromatin Accessibility Embeddings

Train Region2Vec models on single-cell ATAC-seq data for cell-level embeddings.

**Use for:** scATAC-seq clustering, cell-type annotation, dimensionality reduction of single cells, integration with scanpy workflows.

**Workflow:**
1. Prepare AnnData with peak coordinates
2. Pre-tokenize cells
3. Train scEmbed model
4. Generate cell embeddings
5. Cluster and visualize with scanpy

**Reference:** See `references/scembed.md` for detailed workflow, parameters, and examples.

### 4. Consensus Peaks: Universe Building

Build reference peak sets (universes) from BED file collections using multiple statistical methods.

**Use for:** Creating tokenization references, standardizing regions across datasets, defining consensus features with statistical rigor.

**Workflow:**
1. Combine BED files
2. Generate coverage tracks
3. Build universe using CC, CCF, ML, or HMM method

**Methods:**
- **CC (Coverage Cutoff)**: Simple threshold-based
- **CCF (Coverage Cutoff Flexible)**: Confidence intervals for boundaries
- **ML (Maximum Likelihood)**: Probabilistic modeling of positions
- **HMM (Hidden Markov Model)**: Complex state modeling

**Reference:** See `references/consensus_peaks.md` for method comparison, parameters, and examples.

### 5. Utilities: Supporting Tools

Additional tools for caching, randomization, evaluation, and search.

**Available utilities:**
- **BBClient**: BED file caching for repeated access
- **BEDshift**: Randomization preserving genomic context
- **Evaluation**: Metrics for embedding quality (silhouette, Davies-Bouldin, etc.)
- **Tokenization**: Region tokenization utilities (hard, soft, universe-based)
- **Text2BedNN**: Neural search backends for genomic queries

**Reference:** See `references/utilities.md` for detailed usage of each utility.

## Common Workflows

### Basic Region Embedding Pipeline

```python
from geniml.tokenization import hard_tokenization
from geniml.region2vec import region2vec
from geniml.evaluation import evaluate_embeddings

# Step 1: Tokenize BED files
hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokens/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)

# Step 2: Train Region2Vec
region2vec(
    token_folder='tokens/',
    save_dir='model/',
    num_shufflings=1000,
    embedding_dim=100
)

# Step 3: Evaluate
metrics = evaluate_embeddings(
    embeddings_file='model/embeddings.npy',
    labels_file='metadata.csv'
)
```

### scATAC-seq Analysis Pipeline

```python
import scanpy as sc
from geniml.scembed import ScEmbed
from geniml.io import tokenize_cells

# Step 1: Load data
adata = sc.read_h5ad('scatac_data.h5ad')

# Step 2: Tokenize cells
tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokens.parquet'
)

# Step 3: Train scEmbed
model = ScEmbed(embedding_dim=100)
model.train(dataset='tokens.parquet', epochs=100)

# Step 4: Generate embeddings
embeddings = model.encode(adata)
adata.obsm['scembed_X'] = embeddings

# Step 5: Cluster with scanpy
sc.pp.neighbors(adata, use_rep='scembed_X')
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

### Universe Building and Evaluation

```bash
# Generate coverage
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# Build universe with coverage cutoff
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50

# Evaluate universe quality
geniml universe evaluate \
  --universe universe.bed \
  --coverage-folder coverage/ \
  --bed-folder bed_files/
```

## CLI Reference

Geniml provides command-line interfaces for major operations:

```bash
# Region2Vec training
geniml region2vec --token-folder tokens/ --save-dir model/ --num-shuffle 1000

# BEDspace preprocessing
geniml bedspace preprocess --input regions/ --metadata labels.csv --universe universe.bed

# BEDspace training
geniml bedspace train --input preprocessed.txt --output model/ --dim 100

# BEDspace search
geniml bedspace search -t r2l -d distances.pkl -q query.bed -n 10

# Universe building
geniml universe build cc --coverage-folder coverage/ --output universe.bed --cutoff 5

# BEDshift randomization
geniml bedshift --input peaks.bed --genome hg38 --preserve-chrom --iterations 100
```

## When to Use Which Tool

**Use Region2Vec when:**
- Working with bulk genomic data (ChIP-seq, ATAC-seq, etc.)
- Need unsupervised embeddings without metadata
- Comparing region sets across experiments
- Building features for downstream supervised learning

**Use BEDspace when:**
- Metadata labels available (cell types, tissues, conditions)
- Need to query regions by metadata or vice versa
- Want joint embedding space for regions and labels
- Building searchable genomic databases

**Use scEmbed when:**
- Analyzing single-cell ATAC-seq data
- Clustering cells by chromatin accessibility
- Annotating cell types from scATAC-seq
- Integration with scanpy is desired

**Use Universe Building when:**
- Need reference peak sets for tokenization
- Combining multiple experiments into consensus
- Want statistically rigorous region definitions
- Building standard references for a project

**Use Utilities when:**
- Need to cache remote BED files (BBClient)
- Generating null models for statistics (BEDshift)
- Evaluating embedding quality (Evaluation)
- Building search interfaces (Text2BedNN)

## Best Practices

### General Guidelines

- **Universe quality is critical**: Invest time in building comprehensive, well-constructed universes
- **Tokenization validation**: Check coverage (>80% ideal) before training
- **Parameter tuning**: Experiment with embedding dimensions, learning rates, and training epochs
- **Evaluation**: Always validate embeddings with multiple metrics and visualizations
- **Documentation**: Record parameters and random seeds for reproducibility

### Performance Considerations

- **Pre-tokenization**: For scEmbed, always pre-tokenize cells for faster training
- **Memory management**: Large datasets may require batch processing or downsampling
- **Computational resources**: ML/HMM universe methods are computationally intensive
- **Model caching**: Use BBClient to avoid repeated downloads

### Integration Patterns

- **With scanpy**: scEmbed embeddings integrate seamlessly as `adata.obsm` entries
- **With BEDbase**: Use BBClient for accessing remote BED repositories
- **With Hugging Face**: Export trained models for sharing and reproducibility
- **With R**: Use reticulate for R integration (see utilities reference)

## Related Projects

Geniml is part of the BEDbase ecosystem:

- **BEDbase**: Unified platform for genomic regions
- **BEDboss**: Processing pipeline for BED files
- **Gtars**: Genomic tools and utilities
- **BBClient**: Client for BEDbase repositories

## Additional Resources

- **Documentation**: https://docs.bedbase.org/geniml/
- **GitHub**: https://github.com/databio/geniml
- **Pre-trained models**: Available on Hugging Face (databio organization)
- **Publications**: Cited in documentation for methodological details

## Troubleshooting

**"Tokenization coverage too low":**
- Check universe quality and completeness
- Adjust p-value threshold (try 1e-6 instead of 1e-9)
- Ensure universe matches genome assembly

**"Training not converging":**
- Adjust learning rate (try 0.01-0.05 range)
- Increase training epochs
- Check data quality and preprocessing

**"Out of memory errors":**
- Reduce batch size for scEmbed
- Process data in chunks
- Use pre-tokenization for single-cell data

**"StarSpace not found" (BEDspace):**
- Install StarSpace separately: https://github.com/facebookresearch/StarSpace
- Set `--path-to-starspace` parameter correctly

For detailed troubleshooting and method-specific issues, consult the appropriate reference file.

---

## Reference: Bedspace

# BEDspace: Joint Region and Metadata Embeddings

## Overview

BEDspace applies the StarSpace model to genomic data, enabling simultaneous training of numerical embeddings for both region sets and their metadata labels in a shared low-dimensional space. This allows for rich queries across regions and metadata.

## When to Use

Use BEDspace when working with:
- Region sets with associated metadata (cell types, tissues, conditions)
- Search tasks requiring metadata-aware similarity
- Cross-modal queries (e.g., "find regions similar to label X")
- Joint analysis of genomic content and experimental conditions

## Workflow

BEDspace consists of four sequential operations:

### 1. Preprocess

Format genomic intervals and metadata for StarSpace training:

```bash
geniml bedspace preprocess \
  --input /path/to/regions/ \
  --metadata labels.csv \
  --universe universe.bed \
  --labels "cell_type,tissue" \
  --output preprocessed.txt
```

**Required files:**
- **Input folder**: Directory containing BED files
- **Metadata CSV**: Must include `file_name` column matching BED filenames, plus metadata columns
- **Universe file**: Reference BED file for tokenization
- **Labels**: Comma-separated list of metadata columns to use

The preprocessing step adds `__label__` prefixes to metadata and converts regions to StarSpace-compatible format.

### 2. Train

Execute StarSpace model on preprocessed data:

```bash
geniml bedspace train \
  --path-to-starspace /path/to/starspace \
  --input preprocessed.txt \
  --output model/ \
  --dim 100 \
  --epochs 50 \
  --lr 0.05
```

**Key training parameters:**
- `--dim`: Embedding dimension (typical: 50-200)
- `--epochs`: Training epochs (typical: 20-100)
- `--lr`: Learning rate (typical: 0.01-0.1)

### 3. Distances

Compute distance metrics between region sets and metadata labels:

```bash
geniml bedspace distances \
  --input model/ \
  --metadata labels.csv \
  --universe universe.bed \
  --output distances.pkl
```

This step creates a distance matrix needed for similarity searches.

### 4. Search

Retrieve similar items across three scenarios:

**Region-to-Label (r2l)**: Query region set → retrieve similar metadata labels
```bash
geniml bedspace search -t r2l -d distances.pkl -q query_regions.bed -n 10
```

**Label-to-Region (l2r)**: Query metadata label → retrieve similar region sets
```bash
geniml bedspace search -t l2r -d distances.pkl -q "T_cell" -n 10
```

**Region-to-Region (r2r)**: Query region set → retrieve similar region sets
```bash
geniml bedspace search -t r2r -d distances.pkl -q query_regions.bed -n 10
```

The `-n` parameter controls the number of results returned.

## Python API

```python
from geniml.bedspace import BEDSpaceModel

# Load trained model
model = BEDSpaceModel.load('model/')

# Query similar items
results = model.search(
    query="T_cell",
    search_type="l2r",
    top_k=10
)
```

## Best Practices

- **Metadata structure**: Ensure metadata CSV includes `file_name` column that exactly matches BED filenames (without path)
- **Label selection**: Choose informative metadata columns that capture biological variation of interest
- **Universe consistency**: Use the same universe file across preprocessing, distances, and any subsequent analyses
- **Validation**: Preprocess and check output format before investing in training
- **StarSpace installation**: Install StarSpace separately as it's an external dependency

## Output Interpretation

Search results return items ranked by similarity in the joint embedding space:
- **r2l**: Identifies metadata labels characterizing your query regions
- **l2r**: Finds region sets matching your metadata criteria
- **r2r**: Discovers region sets with similar genomic content

## Requirements

BEDspace requires StarSpace to be installed separately. Download from: https://github.com/facebookresearch/StarSpace

---

## Reference: Consensus_Peaks

# Consensus Peaks: Universe Building

## Overview

Geniml provides tools for building genomic "universes" — standardized reference sets of consensus peaks from collections of BED files. These universes represent genomic regions where analyzed datasets show significant coverage overlap, serving as reference vocabularies for tokenization and analysis.

## When to Use

Use consensus peak creation when:
- Building reference peak sets from multiple experiments
- Creating universe files for Region2Vec or BEDspace tokenization
- Standardizing genomic regions across a collection of datasets
- Defining regions of interest with statistical significance

## Workflow

### Step 1: Combine BED Files

Merge all BED files into a single combined file:

```bash
cat /path/to/bed/files/*.bed > combined_files.bed
```

### Step 2: Generate Coverage Tracks

Create bigWig coverage tracks using uniwig with a smoothing window:

```bash
uniwig -m 25 combined_files.bed chrom.sizes coverage/
```

**Parameters:**
- `-m 25`: Smoothing window size (25bp typical for chromatin accessibility)
- `chrom.sizes`: Chromosome sizes file for your genome
- `coverage/`: Output directory for bigWig files

The smoothing window helps reduce noise and creates more robust peak boundaries.

### Step 3: Build Universe

Use one of four methods to construct the consensus peaks:

## Universe-Building Methods

### 1. Coverage Cutoff (CC)

The simplest approach using a fixed coverage threshold:

```bash
geniml universe build cc \
  --coverage-folder coverage/ \
  --output-file universe_cc.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50
```

**Parameters:**
- `--cutoff`: Coverage threshold (1 = union; file count = intersection)
- `--merge`: Distance for merging adjacent peaks (bp)
- `--filter-size`: Minimum peak size for inclusion (bp)

**Use when:** Simple threshold-based selection is sufficient

### 2. Coverage Cutoff Flexible (CCF)

Creates confidence intervals around likelihood cutoffs for boundaries and region cores:

```bash
geniml universe build ccf \
  --coverage-folder coverage/ \
  --output-file universe_ccf.bed \
  --cutoff 5 \
  --confidence 0.95 \
  --merge 100 \
  --filter-size 50
```

**Additional parameters:**
- `--confidence`: Confidence level for flexible boundaries (0-1)

**Use when:** Uncertainty in peak boundaries should be captured

### 3. Maximum Likelihood (ML)

Builds probabilistic models accounting for region start/end positions:

```bash
geniml universe build ml \
  --coverage-folder coverage/ \
  --output-file universe_ml.bed \
  --merge 100 \
  --filter-size 50 \
  --model-type gaussian
```

**Parameters:**
- `--model-type`: Distribution for likelihood estimation (gaussian, poisson)

**Use when:** Statistical modeling of peak locations is important

### 4. Hidden Markov Model (HMM)

Models genomic regions as hidden states with coverage as emissions:

```bash
geniml universe build hmm \
  --coverage-folder coverage/ \
  --output-file universe_hmm.bed \
  --states 3 \
  --merge 100 \
  --filter-size 50
```

**Parameters:**
- `--states`: Number of HMM hidden states (typically 2-5)

**Use when:** Complex patterns of genomic states should be captured

## Python API

```python
from geniml.universe import build_universe

# Build using coverage cutoff method
universe = build_universe(
    coverage_folder='coverage/',
    method='cc',
    cutoff=5,
    merge_distance=100,
    min_size=50,
    output_file='universe.bed'
)
```

## Method Comparison

| Method | Complexity | Flexibility | Computational Cost | Best For |
|--------|------------|-------------|-------------------|----------|
| CC | Low | Low | Low | Quick reference sets |
| CCF | Medium | Medium | Medium | Boundary uncertainty |
| ML | High | High | High | Statistical rigor |
| HMM | High | High | Very High | Complex patterns |

## Best Practices

### Choosing a Method

1. **Start with CC**: Quick and interpretable for initial exploration
2. **Use CCF**: When peak boundaries are uncertain or noisy
3. **Apply ML**: For publication-quality statistical analysis
4. **Deploy HMM**: When modeling complex chromatin states

### Parameter Selection

**Coverage cutoff:**
- `cutoff = 1`: Union of all peaks (most permissive)
- `cutoff = n_files`: Intersection (most stringent)
- `cutoff = 0.5 * n_files`: Moderate consensus (typical choice)

**Merge distance:**
- ATAC-seq: 100-200bp
- ChIP-seq (narrow peaks): 50-100bp
- ChIP-seq (broad peaks): 500-1000bp

**Filter size:**
- Minimum 30bp to avoid artifacts
- 50-100bp typical for most assays
- Larger for broad histone marks

### Quality Control

After building, assess universe quality:

```python
from geniml.evaluation import assess_universe

metrics = assess_universe(
    universe_file='universe.bed',
    coverage_folder='coverage/',
    bed_files='bed_files/'
)

print(f"Number of regions: {metrics['n_regions']}")
print(f"Mean region size: {metrics['mean_size']:.1f}bp")
print(f"Coverage of input peaks: {metrics['coverage']:.1%}")
```

**Key metrics:**
- **Region count**: Should capture major features without excessive fragmentation
- **Size distribution**: Should match expected biology (e.g., ~500bp for ATAC-seq)
- **Input coverage**: Proportion of original peaks represented (typically >80%)

## Output Format

Consensus peaks are saved as BED files with three required columns:

```
chr1    1000    1500
chr1    2000    2800
chr2    500     1000
```

Additional columns may include confidence scores or state annotations depending on the method.

## Common Workflows

### For Region2Vec

1. Build universe using preferred method
2. Use universe as tokenization reference
3. Tokenize BED files
4. Train Region2Vec model

### For BEDspace

1. Build universe from all datasets
2. Use universe in preprocessing step
3. Train BEDspace with metadata
4. Query across regions and labels

### For scEmbed

1. Create universe from bulk or aggregated scATAC-seq
2. Use for cell tokenization
3. Train scEmbed model
4. Generate cell embeddings

## Troubleshooting

**Too few regions:** Lower cutoff threshold or reduce filter size

**Too many regions:** Raise cutoff threshold, increase merge distance, or increase filter size

**Noisy boundaries:** Use CCF or ML methods instead of CC

**Long computation:** Start with CC method for quick results, then refine with ML/HMM if needed

---

## Reference: Region2Vec

# Region2Vec: Genomic Region Embeddings

## Overview

Region2Vec generates unsupervised embeddings of genomic regions and region sets from BED files. It maps genomic regions to a vocabulary, creates sentences through concatenation, and applies word2vec training to learn meaningful representations.

## When to Use

Use Region2Vec when working with:
- BED file collections requiring dimensionality reduction
- Genomic region similarity analysis
- Downstream ML tasks requiring region feature vectors
- Comparative analysis across multiple genomic datasets

## Workflow

### Step 1: Prepare Data

Gather BED files in a source folder. Optionally specify a file list (default uses all files in the directory). Prepare a universe file as the reference vocabulary for tokenization.

### Step 2: Tokenization

Run hard tokenization to convert genomic regions into tokens:

```python
from geniml.tokenization import hard_tokenization

src_folder = '/path/to/raw/bed/files'
dst_folder = '/path/to/tokenized_files'
universe_file = '/path/to/universe_file.bed'

hard_tokenization(src_folder, dst_folder, universe_file, 1e-9)
```

The final parameter (1e-9) is the p-value threshold for tokenization overlap significance.

### Step 3: Train Region2Vec Model

Execute Region2Vec training on the tokenized files:

```python
from geniml.region2vec import region2vec

region2vec(
    token_folder=dst_folder,
    save_dir='./region2vec_model',
    num_shufflings=1000,
    embedding_dim=100,
    context_len=50,
    window_size=5,
    init_lr=0.025
)
```

## Key Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `init_lr` | Initial learning rate | 0.01 - 0.05 |
| `window_size` | Context window size | 3 - 10 |
| `num_shufflings` | Number of shuffling iterations | 500 - 2000 |
| `embedding_dim` | Dimension of output embeddings | 50 - 300 |
| `context_len` | Context length for training | 30 - 100 |

## CLI Usage

```bash
geniml region2vec --token-folder /path/to/tokens \
  --save-dir ./region2vec_model \
  --num-shuffle 1000 \
  --embed-dim 100 \
  --context-len 50 \
  --window-size 5 \
  --init-lr 0.025
```

## Best Practices

- **Parameter tuning**: Frequently tune `init_lr`, `window_size`, `num_shufflings`, and `embedding_dim` for optimal performance on your specific dataset
- **Universe file**: Use a comprehensive universe file that covers all regions of interest in your analysis
- **Validation**: Always validate tokenization output before proceeding to training
- **Resources**: Training can be computationally intensive; monitor memory usage with large datasets

## Output

The trained model saves embeddings that can be used for:
- Similarity searches across genomic regions
- Clustering region sets
- Feature vectors for downstream ML tasks
- Visualization via dimensionality reduction (t-SNE, UMAP)

---

## Reference: Scembed

# scEmbed: Single-Cell Embedding Generation

## Overview

scEmbed trains Region2Vec models on single-cell ATAC-seq datasets to generate cell embeddings for clustering and analysis. It provides an unsupervised machine learning framework for representing and analyzing scATAC-seq data in low-dimensional space.

## When to Use

Use scEmbed when working with:
- Single-cell ATAC-seq (scATAC-seq) data requiring clustering
- Cell-type annotation tasks
- Dimensionality reduction for single-cell chromatin accessibility
- Integration with scanpy workflows for downstream analysis

## Workflow

### Step 1: Data Preparation

Input data must be in AnnData format with `.var` attributes containing `chr`, `start`, and `end` values for peaks.

**Starting from raw data** (barcodes.txt, peaks.bed, matrix.mtx):

```python
import scanpy as sc
import pandas as pd
import scipy.io
import anndata

# Load data
barcodes = pd.read_csv('barcodes.txt', header=None, names=['barcode'])
peaks = pd.read_csv('peaks.bed', sep='\t', header=None,
                    names=['chr', 'start', 'end'])
matrix = scipy.io.mmread('matrix.mtx').tocsr()

# Create AnnData
adata = anndata.AnnData(X=matrix.T, obs=barcodes, var=peaks)
adata.write('scatac_data.h5ad')
```

### Step 2: Pre-tokenization

Convert genomic regions into tokens using gtars utilities. This creates a parquet file with tokenized cells for faster training:

```python
from geniml.io import tokenize_cells

tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokenized_cells.parquet'
)
```

**Benefits of pre-tokenization:**
- Faster training iterations
- Reduced memory requirements
- Reusable tokenized data for multiple training runs

### Step 3: Model Training

Train the scEmbed model using tokenized data:

```python
from geniml.scembed import ScEmbed
from geniml.region2vec import Region2VecDataset

# Load tokenized dataset
dataset = Region2VecDataset('tokenized_cells.parquet')

# Initialize and train model
model = ScEmbed(
    embedding_dim=100,
    window_size=5,
    negative_samples=5
)

model.train(
    dataset=dataset,
    epochs=100,
    batch_size=256,
    learning_rate=0.025
)

# Save model
model.save('scembed_model/')
```

### Step 4: Generate Cell Embeddings

Use the trained model to generate embeddings for cells:

```python
from geniml.scembed import ScEmbed

# Load trained model
model = ScEmbed.from_pretrained('scembed_model/')

# Generate embeddings for AnnData object
embeddings = model.encode(adata)

# Add to AnnData for downstream analysis
adata.obsm['scembed_X'] = embeddings
```

### Step 5: Downstream Analysis

Integrate with scanpy for clustering and visualization:

```python
import scanpy as sc

# Use scEmbed embeddings for neighborhood graph
sc.pp.neighbors(adata, use_rep='scembed_X')

# Cluster cells
sc.tl.leiden(adata, resolution=0.5)

# Compute UMAP for visualization
sc.tl.umap(adata)

# Plot results
sc.pl.umap(adata, color='leiden')
```

## Key Parameters

### Training Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `embedding_dim` | Dimension of cell embeddings | 50 - 200 |
| `window_size` | Context window for training | 3 - 10 |
| `negative_samples` | Number of negative samples | 5 - 20 |
| `epochs` | Training epochs | 50 - 200 |
| `batch_size` | Training batch size | 128 - 512 |
| `learning_rate` | Initial learning rate | 0.01 - 0.05 |

### Tokenization Parameters

- **Universe file**: Reference BED file defining the genomic vocabulary
- **Overlap threshold**: Minimum overlap for peak-universe matching (typically 1e-9)

## Pre-trained Models

Pre-trained scEmbed models are available on Hugging Face for common reference datasets. Load them using:

```python
from geniml.scembed import ScEmbed

# Load pre-trained model
model = ScEmbed.from_pretrained('databio/scembed-pbmc-10k')

# Generate embeddings
embeddings = model.encode(adata)
```

## Best Practices

- **Data quality**: Use filtered peak-barcode matrices, not raw counts
- **Pre-tokenization**: Always pre-tokenize to improve training efficiency
- **Parameter tuning**: Adjust `embedding_dim` and training epochs based on dataset size
- **Validation**: Use known cell-type markers to validate clustering quality
- **Integration**: Combine with scanpy for comprehensive single-cell analysis
- **Model sharing**: Export trained models to Hugging Face for reproducibility

## Example Dataset

The 10x Genomics PBMC 10k dataset (10,000 peripheral blood mononuclear cells) serves as a standard benchmark:
- Contains diverse immune cell types
- Well-characterized cell populations
- Available from 10x Genomics website

## Cell-Type Annotation

After clustering, annotate cell types using k-nearest neighbors (KNN) with reference datasets:

```python
from geniml.scembed import annotate_celltypes

# Annotate using reference
annotations = annotate_celltypes(
    query_adata=adata,
    reference_adata=reference,
    embedding_key='scembed_X',
    k=10
)

adata.obs['cell_type'] = annotations
```

## Output

scEmbed produces:
- Low-dimensional cell embeddings (stored in `adata.obsm`)
- Trained model files for reuse
- Compatible format for scanpy downstream analysis
- Optional export to Hugging Face for sharing

---

## Reference: Utilities

# Geniml Utilities and Additional Tools

## BBClient: BED File Caching

### Overview

BBClient provides efficient caching of BED files from remote sources, enabling faster repeated access and integration with R workflows.

### When to Use

Use BBClient when:
- Repeatedly accessing BED files from remote databases
- Working with BEDbase repositories
- Integrating genomic data with R pipelines
- Need local caching for performance

### Python Usage

```python
from geniml.bbclient import BBClient

# Initialize client
client = BBClient(cache_folder='~/.bedcache')

# Fetch and cache BED file
bed_file = client.load_bed(bed_id='GSM123456')

# Access cached file
regions = client.get_regions('GSM123456')
```

### R Integration

```r
library(reticulate)
geniml <- import("geniml.bbclient")

# Initialize client
client <- geniml$BBClient(cache_folder='~/.bedcache')

# Load BED file
bed_file <- client$load_bed(bed_id='GSM123456')
```

### Best Practices

- Configure cache directory with sufficient storage
- Use consistent cache locations across analyses
- Clear cache periodically to remove unused files

---

## BEDshift: BED File Randomization

### Overview

BEDshift provides tools for randomizing BED files while preserving genomic context, essential for generating null distributions and statistical testing.

### When to Use

Use BEDshift when:
- Creating null models for statistical testing
- Generating control datasets
- Assessing significance of genomic overlaps
- Benchmarking analysis methods

### Usage

```python
from geniml.bedshift import bedshift

# Randomize BED file preserving chromosome distribution
randomized = bedshift(
    input_bed='peaks.bed',
    genome='hg38',
    preserve_chrom=True,
    n_iterations=100
)
```

### CLI Usage

```bash
geniml bedshift \
  --input peaks.bed \
  --genome hg38 \
  --preserve-chrom \
  --iterations 100 \
  --output randomized_peaks.bed
```

### Randomization Strategies

**Preserve chromosome distribution:**
```python
bedshift(input_bed, genome, preserve_chrom=True)
```
Maintains regions on same chromosomes as original.

**Preserve distance distribution:**
```python
bedshift(input_bed, genome, preserve_distance=True)
```
Maintains inter-region distances.

**Preserve region sizes:**
```python
bedshift(input_bed, genome, preserve_size=True)
```
Keeps original region lengths.

### Best Practices

- Choose randomization strategy matching null hypothesis
- Generate multiple iterations for robust statistics
- Validate randomized output maintains desired properties
- Document randomization parameters for reproducibility

---

## Evaluation: Model Assessment Tools

### Overview

Geniml provides evaluation utilities for assessing embedding quality and model performance.

### When to Use

Use evaluation tools when:
- Validating trained embeddings
- Comparing different models
- Assessing clustering quality
- Publishing model results

### Embedding Evaluation

```python
from geniml.evaluation import evaluate_embeddings

# Evaluate Region2Vec embeddings
metrics = evaluate_embeddings(
    embeddings_file='region2vec_model/embeddings.npy',
    labels_file='metadata.csv',
    metrics=['silhouette', 'davies_bouldin', 'calinski_harabasz']
)

print(f"Silhouette score: {metrics['silhouette']:.3f}")
print(f"Davies-Bouldin index: {metrics['davies_bouldin']:.3f}")
```

### Clustering Metrics

**Silhouette score:** Measures cluster cohesion and separation (-1 to 1, higher better)

**Davies-Bouldin index:** Average similarity between clusters (≥0, lower better)

**Calinski-Harabasz score:** Ratio of between/within cluster dispersion (higher better)

### scEmbed Cell-Type Annotation Evaluation

```python
from geniml.evaluation import evaluate_annotation

# Evaluate cell-type predictions
results = evaluate_annotation(
    predicted=adata.obs['predicted_celltype'],
    true=adata.obs['true_celltype'],
    metrics=['accuracy', 'f1', 'confusion_matrix']
)

print(f"Accuracy: {results['accuracy']:.1%}")
print(f"F1 score: {results['f1']:.3f}")
```

### Best Practices

- Use multiple complementary metrics
- Compare against baseline models
- Report metrics on held-out test data
- Visualize embeddings (UMAP/t-SNE) alongside metrics

---

## Tokenization: Region Tokenization Utilities

### Overview

Tokenization converts genomic regions into discrete tokens using a reference universe, enabling word2vec-style training.

### When to Use

Tokenization is a required preprocessing step for:
- Region2Vec training
- scEmbed model training
- Any embedding method requiring discrete tokens

### Hard Tokenization

Strict overlap-based tokenization:

```python
from geniml.tokenization import hard_tokenization

hard_tokenization(
    src_folder='bed_files/',
    dst_folder='tokenized/',
    universe_file='universe.bed',
    p_value_threshold=1e-9
)
```

**Parameters:**
- `p_value_threshold`: Significance level for overlap (typically 1e-9 or 1e-6)

### Soft Tokenization

Probabilistic tokenization allowing partial matches:

```python
from geniml.tokenization import soft_tokenization

soft_tokenization(
    src_folder='bed_files/',
    dst_folder='tokenized/',
    universe_file='universe.bed',
    overlap_threshold=0.5
)
```

**Parameters:**
- `overlap_threshold`: Minimum overlap fraction (0-1)

### Universe-Based Tokenization

Map regions to universe tokens with custom parameters:

```python
from geniml.tokenization import universe_tokenization

universe_tokenization(
    bed_file='peaks.bed',
    universe_file='universe.bed',
    output_file='tokens.txt',
    method='hard',
    threshold=1e-9
)
```

### Best Practices

- **Universe quality**: Use comprehensive, well-constructed universes
- **Threshold selection**: More stringent (lower p-value) for higher confidence
- **Validation**: Check tokenization coverage (what % of regions tokenized)
- **Consistency**: Use same universe and parameters across related analyses

### Tokenization Coverage

Check how well regions tokenize:

```python
from geniml.tokenization import check_coverage

coverage = check_coverage(
    bed_file='peaks.bed',
    universe_file='universe.bed',
    threshold=1e-9
)

print(f"Tokenization coverage: {coverage:.1%}")
```

Aim for >80% coverage for reliable training.

---

## Text2BedNN: Search Backend

### Overview

Text2BedNN creates neural network-based search backends for querying genomic regions using natural language or metadata.

### When to Use

Use Text2BedNN when:
- Building search interfaces for genomic databases
- Enabling natural language queries over BED files
- Creating metadata-aware search systems
- Deploying interactive genomic search applications

### Workflow

**Step 1: Prepare embeddings**

Train BEDspace or Region2Vec model with metadata.

**Step 2: Build search index**

```python
from geniml.search import build_search_index

build_search_index(
    embeddings_file='bedspace_model/embeddings.npy',
    metadata_file='metadata.csv',
    output_dir='search_backend/'
)
```

**Step 3: Query the index**

```python
from geniml.search import SearchBackend

backend = SearchBackend.load('search_backend/')

# Natural language query
results = backend.query(
    text="T cell regulatory regions",
    top_k=10
)

# Metadata query
results = backend.query(
    metadata={'cell_type': 'T_cell', 'tissue': 'blood'},
    top_k=10
)
```

### Best Practices

- Train embeddings with rich metadata for better search
- Index large collections for comprehensive coverage
- Validate search relevance on known queries
- Deploy with API for interactive applications

---

## Additional Tools

### I/O Utilities

```python
from geniml.io import read_bed, write_bed, load_universe

# Read BED file
regions = read_bed('peaks.bed')

# Write BED file
write_bed(regions, 'output.bed')

# Load universe
universe = load_universe('universe.bed')
```

### Model Utilities

```python
from geniml.models import save_model, load_model

# Save trained model
save_model(model, 'my_model/')

# Load model
model = load_model('my_model/')
```

### Common Patterns

**Pipeline workflow:**
```python
# 1. Build universe
universe = build_universe(coverage_folder='coverage/', method='cc', cutoff=5)

# 2. Tokenize
hard_tokenization(src_folder='beds/', dst_folder='tokens/',
                   universe_file='universe.bed', p_value_threshold=1e-9)

# 3. Train embeddings
region2vec(token_folder='tokens/', save_dir='model/', num_shufflings=1000)

# 4. Evaluate
metrics = evaluate_embeddings(embeddings_file='model/embeddings.npy',
                               labels_file='metadata.csv')
```

This modular design allows flexible composition of geniml tools for diverse genomic ML workflows.
