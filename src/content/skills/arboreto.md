---
title: "Arboreto"
description: "Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). Use when analyzing transcriptomics data (bulk RNA-seq, single-cell RNA-seq) to identify transcription factor-target gene relationships a..."
category: "development"
source: "community"
author: "Community"
tags: ["arboreto"]
date: 2026-03-20
---

# Arboreto

## Overview

Arboreto is a computational library for inferring gene regulatory networks (GRNs) from gene expression data using parallelized algorithms that scale from single machines to multi-node clusters.

**Core capability**: Identify which transcription factors (TFs) regulate which target genes based on expression patterns across observations (cells, samples, conditions).

## Quick Start

Install arboreto:
```bash
uv pip install arboreto
```

Basic GRN inference:
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data (genes as columns)
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Infer regulatory network
    network = grnboost2(expression_data=expression_matrix)

    # Save results (TF, target, importance)
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

**Critical**: Always use `if __name__ == '__main__':` guard because Dask spawns new processes.

## Core Capabilities

### 1. Basic GRN Inference

For standard GRN inference workflows including:
- Input data preparation (Pandas DataFrame or NumPy array)
- Running inference with GRNBoost2 or GENIE3
- Filtering by transcription factors
- Output format and interpretation

**See**: `references/basic_inference.md`

**Use the ready-to-run script**: `scripts/basic_grn_inference.py` for standard inference tasks:
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
```

### 2. Algorithm Selection

Arboreto provides two algorithms:

**GRNBoost2 (Recommended)**:
- Fast gradient boosting-based inference
- Optimized for large datasets (10k+ observations)
- Default choice for most analyses

**GENIE3**:
- Random Forest-based inference
- Original multiple regression approach
- Use for comparison or validation

Quick comparison:
```python
from arboreto.algo import grnboost2, genie3

# Fast, recommended
network_grnboost = grnboost2(expression_data=matrix)

# Classic algorithm
network_genie3 = genie3(expression_data=matrix)
```

**For detailed algorithm comparison, parameters, and selection guidance**: `references/algorithms.md`

### 3. Distributed Computing

Scale inference from local multi-core to cluster environments:

**Local (default)** - Uses all available cores automatically:
```python
network = grnboost2(expression_data=matrix)
```

**Custom local client** - Control resources:
```python
from distributed import LocalCluster, Client

local_cluster = LocalCluster(n_workers=10, memory_limit='8GB')
client = Client(local_cluster)

network = grnboost2(expression_data=matrix, client_or_address=client)

client.close()
local_cluster.close()
```

**Cluster computing** - Connect to remote Dask scheduler:
```python
from distributed import Client

client = Client('tcp://scheduler:8786')
network = grnboost2(expression_data=matrix, client_or_address=client)
```

**For cluster setup, performance optimization, and large-scale workflows**: `references/distributed_computing.md`

## Installation

```bash
uv pip install arboreto
```

**Dependencies**: scipy, scikit-learn, numpy, pandas, dask, distributed

## Common Use Cases

### Single-Cell RNA-seq Analysis
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load single-cell expression matrix (cells x genes)
    sc_data = pd.read_csv('scrna_counts.tsv', sep='\t')

    # Infer cell-type-specific regulatory network
    network = grnboost2(expression_data=sc_data, seed=42)

    # Filter high-confidence links
    high_confidence = network[network['importance'] > 0.5]
    high_confidence.to_csv('grn_high_confidence.tsv', sep='\t', index=False)
```

### Bulk RNA-seq with TF Filtering
```python
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load data
    expression_data = pd.read_csv('rnaseq_tpm.tsv', sep='\t')
    tf_names = load_tf_names('human_tfs.txt')

    # Infer with TF restriction
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        seed=123
    )

    network.to_csv('tf_target_network.tsv', sep='\t', index=False)
```

### Comparative Analysis (Multiple Conditions)
```python
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Infer networks for different conditions
    conditions = ['control', 'treatment_24h', 'treatment_48h']

    for condition in conditions:
        data = pd.read_csv(f'{condition}_expression.tsv', sep='\t')
        network = grnboost2(expression_data=data, seed=42)
        network.to_csv(f'{condition}_network.tsv', sep='\t', index=False)
```

## Output Interpretation

Arboreto returns a DataFrame with regulatory links:

| Column | Description |
|--------|-------------|
| `TF` | Transcription factor (regulator) |
| `target` | Target gene |
| `importance` | Regulatory importance score (higher = stronger) |

**Filtering strategy**:
- Top N links per target gene
- Importance threshold (e.g., > 0.5)
- Statistical significance testing (permutation tests)

## Integration with pySCENIC

Arboreto is a core component of the SCENIC pipeline for single-cell regulatory network analysis:

```python
# Step 1: Use arboreto for GRN inference
from arboreto.algo import grnboost2
network = grnboost2(expression_data=sc_data, tf_names=tf_list)

# Step 2: Use pySCENIC for regulon identification and activity scoring
# (See pySCENIC documentation for downstream analysis)
```

## Reproducibility

Always set a seed for reproducible results:
```python
network = grnboost2(expression_data=matrix, seed=777)
```

Run multiple seeds for robustness analysis:
```python
from distributed import LocalCluster, Client

if __name__ == '__main__':
    client = Client(LocalCluster())

    seeds = [42, 123, 777]
    networks = []

    for seed in seeds:
        net = grnboost2(expression_data=matrix, client_or_address=client, seed=seed)
        networks.append(net)

    # Combine networks and filter consensus links
    consensus = analyze_consensus(networks)
```

## Troubleshooting

**Memory errors**: Reduce dataset size by filtering low-variance genes or use distributed computing

**Slow performance**: Use GRNBoost2 instead of GENIE3, enable distributed client, filter TF list

**Dask errors**: Ensure `if __name__ == '__main__':` guard is present in scripts

**Empty results**: Check data format (genes as columns), verify TF names match gene names

---

## Reference: Algorithms

# GRN Inference Algorithms

Arboreto provides two algorithms for gene regulatory network (GRN) inference, both based on the multiple regression approach.

## Algorithm Overview

Both algorithms follow the same inference strategy:
1. For each target gene in the dataset, train a regression model
2. Identify the most important features (potential regulators) from the model
3. Emit these features as candidate regulators with importance scores

The key difference is **computational efficiency** and the underlying regression method.

## GRNBoost2 (Recommended)

**Purpose**: Fast GRN inference for large-scale datasets using gradient boosting.

### When to Use
- **Large datasets**: Tens of thousands of observations (e.g., single-cell RNA-seq)
- **Time-constrained analysis**: Need faster results than GENIE3
- **Default choice**: GRNBoost2 is the flagship algorithm and recommended for most use cases

### Technical Details
- **Method**: Stochastic gradient boosting with early-stopping regularization
- **Performance**: Significantly faster than GENIE3 on large datasets
- **Output**: Same format as GENIE3 (TF-target-importance triplets)

### Usage
```python
from arboreto.algo import grnboost2

network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=42  # For reproducibility
)
```

### Parameters
```python
grnboost2(
    expression_data,           # Required: pandas DataFrame or numpy array
    gene_names=None,           # Required for numpy arrays
    tf_names='all',            # List of TF names or 'all'
    verbose=False,             # Print progress messages
    client_or_address='local', # Dask client or scheduler address
    seed=None                  # Random seed for reproducibility
)
```

## GENIE3

**Purpose**: Classic Random Forest-based GRN inference, serving as the conceptual blueprint.

### When to Use
- **Smaller datasets**: When dataset size allows for longer computation
- **Comparison studies**: When comparing with published GENIE3 results
- **Validation**: To validate GRNBoost2 results

### Technical Details
- **Method**: Random Forest or ExtraTrees regression
- **Foundation**: Original multiple regression GRN inference strategy
- **Trade-off**: More computationally expensive but well-established

### Usage
```python
from arboreto.algo import genie3

network = genie3(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=42
)
```

### Parameters
```python
genie3(
    expression_data,           # Required: pandas DataFrame or numpy array
    gene_names=None,           # Required for numpy arrays
    tf_names='all',            # List of TF names or 'all'
    verbose=False,             # Print progress messages
    client_or_address='local', # Dask client or scheduler address
    seed=None                  # Random seed for reproducibility
)
```

## Algorithm Comparison

| Feature | GRNBoost2 | GENIE3 |
|---------|-----------|--------|
| **Speed** | Fast (optimized for large data) | Slower |
| **Method** | Gradient boosting | Random Forest |
| **Best for** | Large-scale data (10k+ observations) | Small-medium datasets |
| **Output format** | Same | Same |
| **Inference strategy** | Multiple regression | Multiple regression |
| **Recommended** | Yes (default choice) | For comparison/validation |

## Advanced: Custom Regressor Parameters

For advanced users, pass custom scikit-learn regressor parameters:

```python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

# Custom GRNBoost2 parameters
custom_grnboost2 = grnboost2(
    expression_data=expression_matrix,
    regressor_type='GBM',
    regressor_kwargs={
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1
    }
)

# Custom GENIE3 parameters
custom_genie3 = genie3(
    expression_data=expression_matrix,
    regressor_type='RF',
    regressor_kwargs={
        'n_estimators': 1000,
        'max_features': 'sqrt'
    }
)
```

## Choosing the Right Algorithm

**Decision guide**:

1. **Start with GRNBoost2** - It's faster and handles large datasets better
2. **Use GENIE3 if**:
   - Comparing with existing GENIE3 publications
   - Dataset is small-medium sized
   - Validating GRNBoost2 results

Both algorithms produce comparable regulatory networks with the same output format, making them interchangeable for most analyses.

---

## Reference: Basic_Inference

# Basic GRN Inference with Arboreto

## Input Data Requirements

Arboreto requires gene expression data in one of two formats:

### Pandas DataFrame (Recommended)
- **Rows**: Observations (cells, samples, conditions)
- **Columns**: Genes (with gene names as column headers)
- **Format**: Numeric expression values

Example:
```python
import pandas as pd

# Load expression matrix with genes as columns
expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')
# Columns: ['gene1', 'gene2', 'gene3', ...]
# Rows: observation data
```

### NumPy Array
- **Shape**: (observations, genes)
- **Requirement**: Separately provide gene names list matching column order

Example:
```python
import numpy as np

expression_matrix = np.genfromtxt('expression_data.tsv', delimiter='\t', skip_header=1)
with open('expression_data.tsv') as f:
    gene_names = [gene.strip() for gene in f.readline().split('\t')]

assert expression_matrix.shape[1] == len(gene_names)
```

## Transcription Factors (TFs)

Optionally provide a list of transcription factor names to restrict regulatory inference:

```python
from arboreto.utils import load_tf_names

# Load from file (one TF per line)
tf_names = load_tf_names('transcription_factors.txt')

# Or define directly
tf_names = ['TF1', 'TF2', 'TF3']
```

If not provided, all genes are considered potential regulators.

## Basic Inference Workflow

### Using Pandas DataFrame

```python
import pandas as pd
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression data
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # Load transcription factors (optional)
    tf_names = load_tf_names('tf_list.txt')

    # Run GRN inference
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names  # Optional
    )

    # Save results
    network.to_csv('network_output.tsv', sep='\t', index=False, header=False)
```

**Critical**: The `if __name__ == '__main__':` guard is required because Dask spawns new processes internally.

### Using NumPy Array

```python
import numpy as np
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Load expression matrix
    expression_matrix = np.genfromtxt('expression_data.tsv', delimiter='\t', skip_header=1)

    # Extract gene names from header
    with open('expression_data.tsv') as f:
        gene_names = [gene.strip() for gene in f.readline().split('\t')]

    # Verify dimensions match
    assert expression_matrix.shape[1] == len(gene_names)

    # Run inference with explicit gene names
    network = grnboost2(
        expression_data=expression_matrix,
        gene_names=gene_names,
        tf_names=tf_names
    )

    network.to_csv('network_output.tsv', sep='\t', index=False, header=False)
```

## Output Format

Arboreto returns a Pandas DataFrame with three columns:

| Column | Description |
|--------|-------------|
| `TF` | Transcription factor (regulator) gene name |
| `target` | Target gene name |
| `importance` | Regulatory importance score (higher = stronger regulation) |

Example output:
```
TF1    gene5    0.856
TF2    gene12   0.743
TF1    gene8    0.621
```

## Setting Random Seed

For reproducible results, provide a seed parameter:

```python
network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=777
)
```

## Algorithm Selection

Use `grnboost2()` for most cases (faster, handles large datasets):
```python
from arboreto.algo import grnboost2
network = grnboost2(expression_data=expression_matrix)
```

Use `genie3()` for comparison or specific requirements:
```python
from arboreto.algo import genie3
network = genie3(expression_data=expression_matrix)
```

See `references/algorithms.md` for detailed algorithm comparison.

---

## Reference: Distributed_Computing

# Distributed Computing with Arboreto

Arboreto leverages Dask for parallelized computation, enabling efficient GRN inference from single-machine multi-core processing to multi-node cluster environments.

## Computation Architecture

GRN inference is inherently parallelizable:
- Each target gene's regression model can be trained independently
- Arboreto represents computation as a Dask task graph
- Tasks are distributed across available computational resources

## Local Multi-Core Processing (Default)

By default, arboreto uses all available CPU cores on the local machine:

```python
from arboreto.algo import grnboost2

# Automatically uses all local cores
network = grnboost2(expression_data=expression_matrix, tf_names=tf_names)
```

This is sufficient for most use cases and requires no additional configuration.

## Custom Local Dask Client

For fine-grained control over local resources, create a custom Dask client:

```python
from distributed import LocalCluster, Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Configure local cluster
    local_cluster = LocalCluster(
        n_workers=10,              # Number of worker processes
        threads_per_worker=1,       # Threads per worker
        memory_limit='8GB'          # Memory limit per worker
    )

    # Create client
    custom_client = Client(local_cluster)

    # Run inference with custom client
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=custom_client
    )

    # Clean up
    custom_client.close()
    local_cluster.close()
```

### Benefits of Custom Client
- **Resource control**: Limit CPU and memory usage
- **Multiple runs**: Reuse same client for different parameter sets
- **Monitoring**: Access Dask dashboard for performance insights

## Multiple Inference Runs with Same Client

Reuse a single Dask client for multiple inference runs with different parameters:

```python
from distributed import LocalCluster, Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Initialize client once
    local_cluster = LocalCluster(n_workers=8, threads_per_worker=1)
    client = Client(local_cluster)

    # Run multiple inferences
    network_seed1 = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client,
        seed=666
    )

    network_seed2 = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client,
        seed=777
    )

    # Different algorithms with same client
    from arboreto.algo import genie3
    network_genie3 = genie3(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=client
    )

    # Clean up once
    client.close()
    local_cluster.close()
```

## Distributed Cluster Computing

For very large datasets, connect to a remote Dask distributed scheduler running on a cluster:

### Step 1: Set Up Dask Scheduler (on cluster head node)
```bash
dask-scheduler
# Output: Scheduler at tcp://10.118.224.134:8786
```

### Step 2: Start Dask Workers (on cluster compute nodes)
```bash
dask-worker tcp://10.118.224.134:8786
```

### Step 3: Connect from Client
```python
from distributed import Client
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # Connect to remote scheduler
    scheduler_address = 'tcp://10.118.224.134:8786'
    cluster_client = Client(scheduler_address)

    # Run inference on cluster
    network = grnboost2(
        expression_data=expression_matrix,
        tf_names=tf_names,
        client_or_address=cluster_client
    )

    cluster_client.close()
```

### Cluster Configuration Best Practices

**Worker configuration**:
```bash
dask-worker tcp://scheduler:8786 \
    --nprocs 4 \              # Number of processes per node
    --nthreads 1 \            # Threads per process
    --memory-limit 16GB       # Memory per process
```

**For large-scale inference**:
- Use more workers with moderate memory rather than fewer workers with large memory
- Set `threads_per_worker=1` to avoid GIL contention in scikit-learn
- Monitor memory usage to prevent workers from being killed

## Monitoring and Debugging

### Dask Dashboard

Access the Dask dashboard for real-time monitoring:

```python
from distributed import Client

client = Client()  # Prints dashboard URL
# Dashboard available at: http://localhost:8787/status
```

The dashboard shows:
- **Task progress**: Number of tasks completed/pending
- **Resource usage**: CPU, memory per worker
- **Task stream**: Real-time visualization of computation
- **Performance**: Bottleneck identification

### Verbose Output

Enable verbose logging to track inference progress:

```python
network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    verbose=True
)
```

## Performance Optimization Tips

### 1. Data Format
- **Use Pandas DataFrame when possible**: More efficient than NumPy for Dask operations
- **Reduce data size**: Filter low-variance genes before inference

### 2. Worker Configuration
- **CPU-bound tasks**: Set `threads_per_worker=1`, increase `n_workers`
- **Memory-bound tasks**: Increase `memory_limit` per worker

### 3. Cluster Setup
- **Network**: Ensure high-bandwidth, low-latency network between nodes
- **Storage**: Use shared filesystem or object storage for large datasets
- **Scheduling**: Allocate dedicated nodes to avoid resource contention

### 4. Transcription Factor Filtering
- **Limit TF list**: Providing specific TF names reduces computation
```python
# Full search (slow)
network = grnboost2(expression_data=matrix)

# Filtered search (faster)
network = grnboost2(expression_data=matrix, tf_names=known_tfs)
```

## Example: Large-Scale Single-Cell Analysis

Complete workflow for processing single-cell RNA-seq data on a cluster:

```python
from distributed import Client
from arboreto.algo import grnboost2
import pandas as pd

if __name__ == '__main__':
    # Connect to cluster
    client = Client('tcp://cluster-scheduler:8786')

    # Load large single-cell dataset (50,000 cells x 20,000 genes)
    expression_data = pd.read_csv('scrnaseq_data.tsv', sep='\t')

    # Load cell-type-specific TFs
    tf_names = pd.read_csv('tf_list.txt', header=None)[0].tolist()

    # Run distributed inference
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        client_or_address=client,
        verbose=True,
        seed=42
    )

    # Save results
    network.to_csv('grn_results.tsv', sep='\t', index=False)

    client.close()
```

This approach enables analysis of datasets that would be impractical on a single machine.
