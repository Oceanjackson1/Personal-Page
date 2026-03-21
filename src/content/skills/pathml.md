---
title: "Pathml"
description: "Full-featured computational pathology toolkit. Use for advanced WSI analysis including multiplexed immunofluorescence (CODEX, Vectra), nucleus segmentation, tissue graph construction, and ML model training on pathology data. Supports 160+ slide fo..."
category: "development"
source: "community"
author: "Community"
tags: ["pathml"]
date: 2026-03-20
---

# PathML

## Overview

PathML is a comprehensive Python toolkit for computational pathology workflows, designed to facilitate machine learning and image analysis for whole-slide pathology images. The framework provides modular, composable tools for loading diverse slide formats, preprocessing images, constructing spatial graphs, training deep learning models, and analyzing multiparametric imaging data from technologies like CODEX and multiplex immunofluorescence.

## When to Use This Skill

Apply this skill for:
- Loading and processing whole-slide images (WSI) in various proprietary formats
- Preprocessing H&E stained tissue images with stain normalization
- Nucleus detection, segmentation, and classification workflows
- Building cell and tissue graphs for spatial analysis
- Training or deploying machine learning models (HoVer-Net, HACTNet) on pathology data
- Analyzing multiparametric imaging (CODEX, Vectra, MERFISH) for spatial proteomics
- Quantifying marker expression from multiplex immunofluorescence
- Managing large-scale pathology datasets with HDF5 storage
- Tile-based analysis and stitching operations

## Core Capabilities

PathML provides six major capability areas documented in detail within reference files:

### 1. Image Loading & Formats

Load whole-slide images from 160+ proprietary formats including Aperio SVS, Hamamatsu NDPI, Leica SCN, Zeiss ZVI, DICOM, and OME-TIFF. PathML automatically handles vendor-specific formats and provides unified interfaces for accessing image pyramids, metadata, and regions of interest.

**See:** `references/image_loading.md` for supported formats, loading strategies, and working with different slide types.

### 2. Preprocessing Pipelines

Build modular preprocessing pipelines by composing transforms for image manipulation, quality control, stain normalization, tissue detection, and mask operations. PathML's Pipeline architecture enables reproducible, scalable preprocessing across large datasets.

**Key transforms:**
- `StainNormalizationHE` - Macenko/Vahadane stain normalization
- `TissueDetectionHE`, `NucleusDetectionHE` - Tissue/nucleus segmentation
- `MedianBlur`, `GaussianBlur` - Noise reduction
- `LabelArtifactTileHE` - Quality control for artifacts

**See:** `references/preprocessing.md` for complete transform catalog, pipeline construction, and preprocessing workflows.

### 3. Graph Construction

Construct spatial graphs representing cellular and tissue-level relationships. Extract features from segmented objects to create graph-based representations suitable for graph neural networks and spatial analysis.

**See:** `references/graphs.md` for graph construction methods, feature extraction, and spatial analysis workflows.

### 4. Machine Learning

Train and deploy deep learning models for nucleus detection, segmentation, and classification. PathML integrates PyTorch with pre-built models (HoVer-Net, HACTNet), custom DataLoaders, and ONNX support for inference.

**Key models:**
- **HoVer-Net** - Simultaneous nucleus segmentation and classification
- **HACTNet** - Hierarchical cell-type classification

**See:** `references/machine_learning.md` for model training, evaluation, inference workflows, and working with public datasets.

### 5. Multiparametric Imaging

Analyze spatial proteomics and gene expression data from CODEX, Vectra, MERFISH, and other multiplex imaging platforms. PathML provides specialized slide classes and transforms for processing multiparametric data, cell segmentation with Mesmer, and quantification workflows.

**See:** `references/multiparametric.md` for CODEX/Vectra workflows, cell segmentation, marker quantification, and integration with AnnData.

### 6. Data Management

Efficiently store and manage large pathology datasets using HDF5 format. PathML handles tiles, masks, metadata, and extracted features in unified storage structures optimized for machine learning workflows.

**See:** `references/data_management.md` for HDF5 integration, tile management, dataset organization, and batch processing strategies.

## Quick Start

### Installation

```bash
# Install PathML
uv pip install pathml

# With optional dependencies for all features
uv pip install pathml[all]
```

### Basic Workflow Example

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline, StainNormalizationHE, TissueDetectionHE

# Load a whole-slide image
wsi = SlideData.from_slide("path/to/slide.svs")

# Create preprocessing pipeline
pipeline = Pipeline([
    TissueDetectionHE(),
    StainNormalizationHE(target='normalize', stain_estimation_method='macenko')
])

# Run pipeline
pipeline.run(wsi)

# Access processed tiles
for tile in wsi.tiles:
    processed_image = tile.image
    tissue_mask = tile.masks['tissue']
```

### Common Workflows

**H&E Image Analysis:**
1. Load WSI with appropriate slide class
2. Apply tissue detection and stain normalization
3. Perform nucleus detection or train segmentation models
4. Extract features and build spatial graphs
5. Conduct downstream analysis

**Multiparametric Imaging (CODEX):**
1. Load CODEX slide with `CODEXSlide`
2. Collapse multi-run channel data
3. Segment cells using Mesmer model
4. Quantify marker expression
5. Export to AnnData for single-cell analysis

**Training ML Models:**
1. Prepare dataset with public pathology data
2. Create PyTorch DataLoader with PathML datasets
3. Train HoVer-Net or custom models
4. Evaluate on held-out test sets
5. Deploy with ONNX for inference

## References to Detailed Documentation

When working on specific tasks, refer to the appropriate reference file for comprehensive information:

- **Loading images:** `references/image_loading.md`
- **Preprocessing workflows:** `references/preprocessing.md`
- **Spatial analysis:** `references/graphs.md`
- **Model training:** `references/machine_learning.md`
- **CODEX/multiplex IF:** `references/multiparametric.md`
- **Data storage:** `references/data_management.md`

## Resources

This skill includes comprehensive reference documentation organized by capability area. Each reference file contains detailed API information, workflow examples, best practices, and troubleshooting guidance for specific PathML functionality.

### references/

Documentation files providing in-depth coverage of PathML capabilities:

- `image_loading.md` - Whole-slide image formats, loading strategies, slide classes
- `preprocessing.md` - Complete transform catalog, pipeline construction, preprocessing workflows
- `graphs.md` - Graph construction methods, feature extraction, spatial analysis
- `machine_learning.md` - Model architectures, training workflows, evaluation, inference
- `multiparametric.md` - CODEX, Vectra, multiplex IF analysis, cell segmentation, quantification
- `data_management.md` - HDF5 storage, tile management, batch processing, dataset organization

Load these references as needed when working on specific computational pathology tasks.

---

## Reference: Data_Management

# Data Management & Storage

## Overview

PathML provides efficient data management solutions for handling large-scale pathology datasets through HDF5 storage, tile management strategies, and optimized batch processing workflows. The framework enables seamless storage and retrieval of images, masks, features, and metadata in formats optimized for machine learning pipelines and downstream analysis.

## HDF5 Integration

HDF5 (Hierarchical Data Format) is the primary storage format for processed PathML data, providing:
- Efficient compression and chunked storage
- Fast random access to subsets of data
- Support for arbitrarily large datasets
- Hierarchical organization of heterogeneous data types
- Cross-platform compatibility

### Saving to HDF5

**Single slide:**
```python
from pathml.core import SlideData

# Load and process slide
wsi = SlideData.from_slide("slide.svs")
wsi.generate_tiles(level=1, tile_size=256, stride=256)

# Run preprocessing pipeline
pipeline.run(wsi)

# Save to HDF5
wsi.to_hdf5("processed_slide.h5")
```

**Multiple slides (SlideDataset):**
```python
from pathml.core import SlideDataset
import glob

# Create dataset
slide_paths = glob.glob("data/*.svs")
dataset = SlideDataset(slide_paths, tile_size=256, stride=256, level=1)

# Process
dataset.run(pipeline, distributed=True, n_workers=8)

# Save entire dataset
dataset.to_hdf5("processed_dataset.h5")
```

### HDF5 File Structure

PathML HDF5 files are organized hierarchically:

```
processed_dataset.h5
├── slide_0/
│   ├── metadata/
│   │   ├── name
│   │   ├── level
│   │   ├── dimensions
│   │   └── ...
│   ├── tiles/
│   │   ├── tile_0/
│   │   │   ├── image  (H, W, C) array
│   │   │   ├── coords  (x, y)
│   │   │   └── masks/
│   │   │       ├── tissue
│   │   │       ├── nucleus
│   │   │       └── ...
│   │   ├── tile_1/
│   │   └── ...
│   └── features/
│       ├── tile_features  (n_tiles, n_features)
│       └── feature_names
├── slide_1/
└── ...
```

### Loading from HDF5

**Load entire slide:**
```python
from pathml.core import SlideData

# Load from HDF5
wsi = SlideData.from_hdf5("processed_slide.h5")

# Access tiles
for tile in wsi.tiles:
    image = tile.image
    masks = tile.masks
    # Process tile...
```

**Load specific tiles:**
```python
# Load only tiles at specific indices
tile_indices = [0, 10, 20, 30]
tiles = wsi.load_tiles_from_hdf5("processed_slide.h5", indices=tile_indices)

for tile in tiles:
    # Process subset...
    pass
```

**Memory-mapped access:**
```python
import h5py

# Open HDF5 file without loading into memory
with h5py.File("processed_dataset.h5", 'r') as f:
    # Access specific data
    tile_0_image = f['slide_0/tiles/tile_0/image'][:]
    tissue_mask = f['slide_0/tiles/tile_0/masks/tissue'][:]

    # Iterate through tiles efficiently
    for tile_key in f['slide_0/tiles'].keys():
        tile_image = f[f'slide_0/tiles/{tile_key}/image'][:]
        # Process without loading all tiles...
```

## Tile Management

### Tile Generation Strategies

**Fixed-size tiles with no overlap:**
```python
wsi.generate_tiles(
    level=1,
    tile_size=256,
    stride=256,  # stride = tile_size → no overlap
    pad=False  # Don't pad edge tiles
)
```
- **Use case:** Standard tile-based processing, classification
- **Pros:** Simple, no redundancy, fast processing
- **Cons:** Edge effects at tile boundaries

**Overlapping tiles:**
```python
wsi.generate_tiles(
    level=1,
    tile_size=256,
    stride=128,  # 50% overlap
    pad=False
)
```
- **Use case:** Segmentation, detection (reduces boundary artifacts)
- **Pros:** Better boundary handling, smoother stitching
- **Cons:** More tiles, redundant computation

**Adaptive tiling based on tissue content:**
```python
from pathml.utils import adaptive_tile_generation

# Generate tiles only in tissue regions
wsi.generate_tiles(level=1, tile_size=256, stride=256)

# Filter to keep only tiles with sufficient tissue
tissue_tiles = []
for tile in wsi.tiles:
    if tile.masks.get('tissue') is not None:
        tissue_coverage = tile.masks['tissue'].sum() / (tile_size**2)
        if tissue_coverage > 0.5:  # Keep tiles with >50% tissue
            tissue_tiles.append(tile)

wsi.tiles = tissue_tiles
```
- **Use case:** Sparse tissue samples, efficiency
- **Pros:** Reduces processing of background tiles
- **Cons:** Requires tissue detection preprocessing step

### Tile Stitching

Reconstruct full slide from processed tiles:

```python
from pathml.utils import stitch_tiles

# Process tiles
for tile in wsi.tiles:
    tile.prediction = model.predict(tile.image)

# Stitch predictions back to full resolution
full_prediction_map = stitch_tiles(
    wsi.tiles,
    output_shape=wsi.level_dimensions[1],  # Use level 1 dimensions
    tile_size=256,
    stride=256,
    method='average'  # 'average', 'max', or 'first'
)

# Visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 15))
plt.imshow(full_prediction_map)
plt.title('Stitched Prediction Map')
plt.axis('off')
plt.show()
```

**Stitching methods:**
- `'average'`: Average overlapping regions (smooth transitions)
- `'max'`: Maximum value in overlapping regions
- `'first'`: Keep first tile's value (no blending)
- `'weighted'`: Distance-weighted blending for smooth boundaries

### Tile Caching

Cache frequently accessed tiles for faster iteration:

```python
from pathml.utils import TileCache

# Create cache
cache = TileCache(max_size_gb=10)

# Cache tiles during first iteration
for i, tile in enumerate(wsi.tiles):
    cache.add(f'tile_{i}', tile.image)
    # Process tile...

# Subsequent iterations use cached data
for i in range(len(wsi.tiles)):
    cached_image = cache.get(f'tile_{i}')
    # Fast access...
```

## Dataset Organization

### Directory Structure for Large Projects

Organize pathology projects with consistent structure:

```
project/
├── raw_slides/
│   ├── cohort1/
│   │   ├── slide001.svs
│   │   ├── slide002.svs
│   │   └── ...
│   └── cohort2/
│       └── ...
├── processed/
│   ├── cohort1/
│   │   ├── slide001.h5
│   │   ├── slide002.h5
│   │   └── ...
│   └── cohort2/
│       └── ...
├── features/
│   ├── cohort1_features.h5
│   └── cohort2_features.h5
├── models/
│   ├── hovernet_checkpoint.pth
│   └── classifier.onnx
├── results/
│   ├── predictions/
│   ├── visualizations/
│   └── metrics.csv
└── metadata/
    ├── clinical_data.csv
    └── slide_manifest.csv
```

### Metadata Management

Store slide-level and cohort-level metadata:

```python
import pandas as pd

# Slide manifest
manifest = pd.DataFrame({
    'slide_id': ['slide001', 'slide002', 'slide003'],
    'path': ['raw_slides/cohort1/slide001.svs', ...],
    'cohort': ['cohort1', 'cohort1', 'cohort2'],
    'tissue_type': ['breast', 'breast', 'lung'],
    'scanner': ['Aperio', 'Hamamatsu', 'Aperio'],
    'magnification': [40, 40, 20],
    'staining': ['H&E', 'H&E', 'H&E']
})

manifest.to_csv('metadata/slide_manifest.csv', index=False)

# Clinical data
clinical = pd.DataFrame({
    'slide_id': ['slide001', 'slide002', 'slide003'],
    'patient_id': ['P001', 'P002', 'P003'],
    'age': [55, 62, 48],
    'diagnosis': ['invasive', 'in_situ', 'invasive'],
    'stage': ['II', 'I', 'III'],
    'outcome': ['favorable', 'favorable', 'poor']
})

clinical.to_csv('metadata/clinical_data.csv', index=False)

# Load and merge
manifest = pd.read_csv('metadata/slide_manifest.csv')
clinical = pd.read_csv('metadata/clinical_data.csv')
data = manifest.merge(clinical, on='slide_id')
```

## Batch Processing Strategies

### Sequential Processing

Process slides one at a time (memory-efficient):

```python
import glob
from pathml.core import SlideData
from pathml.preprocessing import Pipeline

slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)

for slide_path in slide_paths:
    # Load slide
    wsi = SlideData.from_slide(slide_path)
    wsi.generate_tiles(level=1, tile_size=256, stride=256)

    # Process
    pipeline.run(wsi)

    # Save
    output_path = slide_path.replace('raw_slides', 'processed').replace('.svs', '.h5')
    wsi.to_hdf5(output_path)

    print(f"Processed: {slide_path}")
```

### Parallel Processing with Dask

Process multiple slides in parallel:

```python
from pathml.core import SlideDataset
from dask.distributed import Client, LocalCluster
from pathml.preprocessing import Pipeline

# Start Dask cluster
cluster = LocalCluster(
    n_workers=8,
    threads_per_worker=2,
    memory_limit='8GB',
    dashboard_address=':8787'  # View progress at localhost:8787
)
client = Client(cluster)

# Create dataset
slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)
dataset = SlideDataset(slide_paths, tile_size=256, stride=256, level=1)

# Distribute processing
dataset.run(
    pipeline,
    distributed=True,
    client=client,
    scheduler='distributed'
)

# Save results
for i, slide in enumerate(dataset):
    output_path = slide_paths[i].replace('raw_slides', 'processed').replace('.svs', '.h5')
    slide.to_hdf5(output_path)

client.close()
cluster.close()
```

### Batch Processing with Job Arrays

For HPC clusters (SLURM, PBS):

```python
# submit_jobs.py
import os
import glob

slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)

# Write slide list
with open('slide_list.txt', 'w') as f:
    for path in slide_paths:
        f.write(path + '\n')

# Create SLURM job script
slurm_script = """#!/bin/bash
#SBATCH --array=1-{n_slides}
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=4:00:00
#SBATCH --output=logs/slide_%A_%a.out

# Get slide path for this array task
SLIDE_PATH=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" slide_list.txt)

# Run processing
python process_slide.py --slide_path $SLIDE_PATH
""".format(n_slides=len(slide_paths))

with open('submit_jobs.sh', 'w') as f:
    f.write(slurm_script)

# Submit: sbatch submit_jobs.sh
```

```python
# process_slide.py
import argparse
from pathml.core import SlideData
from pathml.preprocessing import Pipeline

parser = argparse.ArgumentParser()
parser.add_argument('--slide_path', type=str, required=True)
args = parser.parse_args()

# Load and process
wsi = SlideData.from_slide(args.slide_path)
wsi.generate_tiles(level=1, tile_size=256, stride=256)

pipeline = Pipeline([...])
pipeline.run(wsi)

# Save
output_path = args.slide_path.replace('raw_slides', 'processed').replace('.svs', '.h5')
wsi.to_hdf5(output_path)

print(f"Processed: {args.slide_path}")
```

## Feature Extraction and Storage

### Extracting Features

```python
from pathml.core import SlideData
import torch
import numpy as np

# Load pre-trained model for feature extraction
model = torch.load('models/feature_extractor.pth')
model.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Load processed slide
wsi = SlideData.from_hdf5('processed/slide001.h5')

# Extract features for each tile
features = []
coords = []

for tile in wsi.tiles:
    # Preprocess tile
    tile_tensor = torch.from_numpy(tile.image).permute(2, 0, 1).unsqueeze(0).float()
    tile_tensor = tile_tensor.to(device)

    # Extract features
    with torch.no_grad():
        feature_vec = model(tile_tensor).cpu().numpy().flatten()

    features.append(feature_vec)
    coords.append(tile.coords)

features = np.array(features)  # Shape: (n_tiles, feature_dim)
coords = np.array(coords)  # Shape: (n_tiles, 2)
```

### Storing Features in HDF5

```python
import h5py

# Save features
with h5py.File('features/slide001_features.h5', 'w') as f:
    f.create_dataset('features', data=features, compression='gzip')
    f.create_dataset('coords', data=coords)
    f.attrs['feature_dim'] = features.shape[1]
    f.attrs['num_tiles'] = features.shape[0]
    f.attrs['model'] = 'resnet50'

# Load features
with h5py.File('features/slide001_features.h5', 'r') as f:
    features = f['features'][:]
    coords = f['coords'][:]
    feature_dim = f.attrs['feature_dim']
```

### Feature Database for Multiple Slides

```python
# Create consolidated feature database
import h5py
import glob

feature_files = glob.glob('features/*_features.h5')

with h5py.File('features/all_features.h5', 'w') as out_f:
    for i, feature_file in enumerate(feature_files):
        slide_name = feature_file.split('/')[-1].replace('_features.h5', '')

        with h5py.File(feature_file, 'r') as in_f:
            features = in_f['features'][:]
            coords = in_f['coords'][:]

            # Store in consolidated file
            grp = out_f.create_group(f'slide_{i}')
            grp.create_dataset('features', data=features, compression='gzip')
            grp.create_dataset('coords', data=coords)
            grp.attrs['slide_name'] = slide_name

# Query features from all slides
with h5py.File('features/all_features.h5', 'r') as f:
    for slide_key in f.keys():
        slide_name = f[slide_key].attrs['slide_name']
        features = f[f'{slide_key}/features'][:]
        # Process...
```

## Data Versioning

### Version Control with DVC

Use Data Version Control (DVC) for large dataset management:

```bash
# Initialize DVC
dvc init

# Add data directory
dvc add raw_slides/
dvc add processed/

# Commit to git
git add raw_slides.dvc processed.dvc .gitignore
git commit -m "Add raw and processed slides"

# Push data to remote storage (S3, GCS, etc.)
dvc remote add -d storage s3://my-bucket/pathml-data
dvc push

# Pull data on another machine
git pull
dvc pull
```

### Checksums and Validation

Validate data integrity:

```python
import hashlib
import pandas as pd

def compute_checksum(file_path):
    """Compute MD5 checksum of file."""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Create checksum manifest
slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)
checksums = []

for slide_path in slide_paths:
    checksum = compute_checksum(slide_path)
    checksums.append({
        'path': slide_path,
        'checksum': checksum,
        'size_mb': os.path.getsize(slide_path) / 1e6
    })

checksum_df = pd.DataFrame(checksums)
checksum_df.to_csv('metadata/checksums.csv', index=False)

# Validate files
def validate_files(manifest_path):
    manifest = pd.read_csv(manifest_path)
    for _, row in manifest.iterrows():
        current_checksum = compute_checksum(row['path'])
        if current_checksum != row['checksum']:
            print(f"ERROR: Checksum mismatch for {row['path']}")
        else:
            print(f"OK: {row['path']}")

validate_files('metadata/checksums.csv')
```

## Performance Optimization

### Compression Settings

Optimize HDF5 compression for speed vs. size:

```python
import h5py

# Fast compression (less CPU, larger files)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=1  # Level 1-9, lower = faster
    )

# Maximum compression (more CPU, smaller files)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=9
    )

# Balanced (recommended)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=4,
        chunks=True  # Enable chunking for better I/O
    )
```

### Chunking Strategy

Optimize chunked storage for access patterns:

```python
# For tile-based access (access one tile at a time)
with h5py.File('tiles.h5', 'w') as f:
    f.create_dataset(
        'tiles',
        shape=(n_tiles, 256, 256, 3),
        dtype='uint8',
        chunks=(1, 256, 256, 3),  # One tile per chunk
        compression='gzip'
    )

# For channel-based access (access all tiles for one channel)
with h5py.File('tiles.h5', 'w') as f:
    f.create_dataset(
        'tiles',
        shape=(n_tiles, 256, 256, 3),
        dtype='uint8',
        chunks=(n_tiles, 256, 256, 1),  # All tiles for one channel
        compression='gzip'
    )
```

### Memory-Mapped Arrays

Use memory mapping for large arrays:

```python
import numpy as np

# Save as memory-mapped file
features_mmap = np.memmap(
    'features/features.mmap',
    dtype='float32',
    mode='w+',
    shape=(n_tiles, feature_dim)
)

# Populate
for i, tile in enumerate(wsi.tiles):
    features_mmap[i] = extract_features(tile)

# Flush to disk
features_mmap.flush()

# Load without reading into memory
features_mmap = np.memmap(
    'features/features.mmap',
    dtype='float32',
    mode='r',
    shape=(n_tiles, feature_dim)
)

# Access subset efficiently
subset = features_mmap[1000:2000]  # Only loads requested rows
```

## Best Practices

1. **Use HDF5 for processed data:** Save preprocessed tiles and features to HDF5 for fast access

2. **Separate raw and processed data:** Keep original slides separate from processed outputs

3. **Maintain metadata:** Track slide provenance, processing parameters, and clinical annotations

4. **Implement checksums:** Validate data integrity, especially after transfers

5. **Version datasets:** Use DVC or similar tools to version large datasets

6. **Optimize storage:** Balance compression level with I/O performance

7. **Organize by cohort:** Structure directories by study cohort for clarity

8. **Regular backups:** Back up both data and metadata to remote storage

9. **Document processing:** Keep logs of processing steps, parameters, and versions

10. **Monitor disk usage:** Track storage consumption as datasets grow

## Common Issues and Solutions

**Issue: HDF5 files very large**
- Increase compression level: `compression_opts=9`
- Store only necessary data (avoid redundant copies)
- Use appropriate data types (uint8 for images vs. float64)

**Issue: Slow HDF5 read/write**
- Optimize chunk size for access pattern
- Reduce compression level for faster I/O
- Use SSD storage instead of HDD
- Enable parallel HDF5 with MPI

**Issue: Running out of disk space**
- Delete intermediate files after processing
- Compress inactive datasets
- Move old data to archival storage
- Use cloud storage for less-accessed data

**Issue: Data corruption or loss**
- Implement regular backups
- Use RAID for redundancy
- Validate checksums after transfers
- Use version control (DVC)

## Additional Resources

- **HDF5 Documentation:** https://www.hdfgroup.org/solutions/hdf5/
- **h5py:** https://docs.h5py.org/
- **DVC (Data Version Control):** https://dvc.org/
- **Dask:** https://docs.dask.org/
- **PathML Data Management API:** https://pathml.readthedocs.io/en/latest/api_data_reference.html

---

## Reference: Graphs

# Graph Construction & Spatial Analysis

## Overview

PathML provides tools for constructing spatial graphs from tissue images to represent cellular and tissue-level relationships. Graph-based representations enable sophisticated spatial analysis, including neighborhood analysis, cell-cell interaction studies, and graph neural network applications. These graphs capture both morphological features and spatial topology for downstream computational analysis.

## Graph Types

PathML supports construction of multiple graph types:

### Cell Graphs
- Nodes represent individual cells
- Edges represent spatial proximity or biological interactions
- Node features include morphology, marker expression, cell type
- Suitable for single-cell spatial analysis

### Tissue Graphs
- Nodes represent tissue regions or superpixels
- Edges represent spatial adjacency
- Node features include tissue composition, texture features
- Suitable for tissue-level spatial patterns

### Spatial Transcriptomics Graphs
- Nodes represent spatial spots or cells
- Edges encode spatial relationships
- Node features include gene expression profiles
- Suitable for spatial omics analysis

## Graph Construction Workflow

### From Segmentation to Graphs

Convert nucleus or cell segmentation results into spatial graphs:

```python
from pathml.graph import CellGraph
from pathml.preprocessing import Pipeline, SegmentMIF
import numpy as np

# 1. Perform cell segmentation
pipeline = Pipeline([
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])
pipeline.run(slide)

# 2. Extract instance segmentation mask
inst_map = slide.masks['cell_segmentation']

# 3. Build cell graph
cell_graph = CellGraph.from_instance_map(
    inst_map,
    image=slide.image,  # Optional: for extracting visual features
    connectivity='delaunay',  # 'knn', 'radius', or 'delaunay'
    k=5,  # For knn: number of neighbors
    radius=50  # For radius: distance threshold in pixels
)

# 4. Access graph components
nodes = cell_graph.nodes  # Node features
edges = cell_graph.edges  # Edge list
adjacency = cell_graph.adjacency_matrix  # Adjacency matrix
```

### Connectivity Methods

**K-Nearest Neighbors (KNN):**
```python
# Connect each cell to its k nearest neighbors
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='knn',
    k=5  # Number of neighbors
)
```
- Fixed degree per node
- Captures local neighborhoods
- Simple and interpretable

**Radius-based:**
```python
# Connect cells within a distance threshold
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='radius',
    radius=100,  # Maximum distance in pixels
    distance_metric='euclidean'  # or 'manhattan', 'chebyshev'
)
```
- Variable degree based on density
- Biologically motivated (interaction range)
- Captures physical proximity

**Delaunay Triangulation:**
```python
# Connect cells using Delaunay triangulation
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='delaunay'
)
```
- Creates connected graph from spatial positions
- No isolated nodes (in convex hull)
- Captures spatial tessellation

**Contact-based:**
```python
# Connect cells with touching boundaries
graph = CellGraph.from_instance_map(
    inst_map,
    connectivity='contact',
    dilation=2  # Dilate boundaries to capture near-contacts
)
```
- Physical cell-cell contacts
- Most biologically direct
- Sparse edges for separated cells

## Node Features

### Morphological Features

Extract shape and size features for each cell:

```python
from pathml.graph import extract_morphology_features

# Compute morphological features
morphology_features = extract_morphology_features(
    inst_map,
    features=[
        'area',  # Cell area in pixels
        'perimeter',  # Cell perimeter
        'eccentricity',  # Shape elongation
        'solidity',  # Convexity measure
        'major_axis_length',
        'minor_axis_length',
        'orientation'  # Cell orientation angle
    ]
)

# Add to graph
cell_graph.add_node_features(morphology_features, feature_names=['area', 'perimeter', ...])
```

**Available morphological features:**
- **Area** - Number of pixels
- **Perimeter** - Boundary length
- **Eccentricity** - 0 (circle) to 1 (line)
- **Solidity** - Area / convex hull area
- **Circularity** - 4π × area / perimeter²
- **Major/Minor axis** - Lengths of fitted ellipse axes
- **Orientation** - Angle of major axis
- **Extent** - Area / bounding box area

### Intensity Features

Extract marker expression or intensity statistics:

```python
from pathml.graph import extract_intensity_features

# Extract mean marker intensities per cell
intensity_features = extract_intensity_features(
    inst_map,
    image=multichannel_image,  # Shape: (H, W, C)
    channel_names=['DAPI', 'CD3', 'CD4', 'CD8', 'CD20'],
    statistics=['mean', 'std', 'median', 'max']
)

# Add to graph
cell_graph.add_node_features(
    intensity_features,
    feature_names=['DAPI_mean', 'CD3_mean', ...]
)
```

**Available statistics:**
- **mean** - Average intensity
- **median** - Median intensity
- **std** - Standard deviation
- **max** - Maximum intensity
- **min** - Minimum intensity
- **quantile_25/75** - Quartiles

### Texture Features

Compute texture descriptors for each cell region:

```python
from pathml.graph import extract_texture_features

# Haralick texture features
texture_features = extract_texture_features(
    inst_map,
    image=grayscale_image,
    features='haralick',  # or 'lbp', 'gabor'
    distance=1,
    angles=[0, np.pi/4, np.pi/2, 3*np.pi/4]
)

cell_graph.add_node_features(texture_features)
```

### Cell Type Annotations

Add cell type labels from classification:

```python
# From ML model predictions
cell_types = hovernet_type_predictions  # Array of cell type IDs

cell_graph.add_node_features(
    cell_types,
    feature_names=['cell_type']
)

# One-hot encode cell types
cell_type_onehot = one_hot_encode(cell_types, num_classes=5)
cell_graph.add_node_features(
    cell_type_onehot,
    feature_names=['type_epithelial', 'type_inflammatory', ...]
)
```

## Edge Features

### Spatial Distance

Compute edge features based on spatial relationships:

```python
from pathml.graph import compute_edge_distances

# Add pairwise distances as edge features
distances = compute_edge_distances(
    cell_graph,
    metric='euclidean'  # or 'manhattan', 'chebyshev'
)

cell_graph.add_edge_features(distances, feature_names=['distance'])
```

### Interaction Features

Model biological interactions between cell types:

```python
from pathml.graph import compute_interaction_features

# Cell type co-occurrence along edges
interaction_features = compute_interaction_features(
    cell_graph,
    cell_types=cell_type_labels,
    interaction_type='categorical'  # or 'numerical'
)

cell_graph.add_edge_features(interaction_features)
```

## Graph-Level Features

Aggregate features for entire graph:

```python
from pathml.graph import compute_graph_features

# Topological features
graph_features = compute_graph_features(
    cell_graph,
    features=[
        'num_nodes',
        'num_edges',
        'average_degree',
        'clustering_coefficient',
        'average_path_length',
        'diameter'
    ]
)

# Cell composition features
composition = cell_graph.compute_cell_type_composition(
    cell_type_labels,
    normalize=True  # Proportions
)
```

## Spatial Analysis

### Neighborhood Analysis

Analyze cell neighborhoods and microenvironments:

```python
from pathml.graph import analyze_neighborhoods

# Characterize neighborhoods around each cell
neighborhoods = analyze_neighborhoods(
    cell_graph,
    cell_types=cell_type_labels,
    radius=100,  # Neighborhood radius
    metrics=['diversity', 'density', 'composition']
)

# Neighborhood diversity (Shannon entropy)
diversity = neighborhoods['diversity']

# Cell type composition in each neighborhood
composition = neighborhoods['composition']  # (n_cells, n_cell_types)
```

### Spatial Clustering

Identify spatial clusters of cell types:

```python
from pathml.graph import spatial_clustering
import matplotlib.pyplot as plt

# Detect spatial clusters
clusters = spatial_clustering(
    cell_graph,
    cell_positions,
    method='dbscan',  # or 'kmeans', 'hierarchical'
    eps=50,  # DBSCAN: neighborhood radius
    min_samples=10  # DBSCAN: minimum cluster size
)

# Visualize clusters
plt.scatter(
    cell_positions[:, 0],
    cell_positions[:, 1],
    c=clusters,
    cmap='tab20'
)
plt.title('Spatial Clusters')
plt.show()
```

### Cell-Cell Interaction Analysis

Test for enrichment or depletion of cell type interactions:

```python
from pathml.graph import cell_interaction_analysis

# Test for significant interactions
interaction_results = cell_interaction_analysis(
    cell_graph,
    cell_types=cell_type_labels,
    method='permutation',  # or 'expected'
    n_permutations=1000,
    significance_level=0.05
)

# Interaction scores (positive = attraction, negative = avoidance)
interaction_matrix = interaction_results['scores']

# Visualize with heatmap
import seaborn as sns
sns.heatmap(
    interaction_matrix,
    cmap='RdBu_r',
    center=0,
    xticklabels=cell_type_names,
    yticklabels=cell_type_names
)
plt.title('Cell-Cell Interaction Scores')
plt.show()
```

### Spatial Statistics

Compute spatial statistics and patterns:

```python
from pathml.graph import spatial_statistics

# Ripley's K function for spatial point patterns
ripleys_k = spatial_statistics(
    cell_positions,
    cell_types=cell_type_labels,
    statistic='ripleys_k',
    radii=np.linspace(0, 200, 50)
)

# Nearest neighbor distances
nn_distances = spatial_statistics(
    cell_positions,
    statistic='nearest_neighbor',
    by_cell_type=True
)
```

## Integration with Graph Neural Networks

### Convert to PyTorch Geometric Format

```python
from pathml.graph import to_pyg
import torch
from torch_geometric.data import Data

# Convert to PyTorch Geometric Data object
pyg_data = cell_graph.to_pyg()

# Access components
x = pyg_data.x  # Node features (n_nodes, n_features)
edge_index = pyg_data.edge_index  # Edge connectivity (2, n_edges)
edge_attr = pyg_data.edge_attr  # Edge features (n_edges, n_edge_features)
y = pyg_data.y  # Graph-level label
pos = pyg_data.pos  # Node positions (n_nodes, 2)

# Use with PyTorch Geometric
from torch_geometric.nn import GCNConv

class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

model = GNN(in_channels=pyg_data.num_features, hidden_channels=64, out_channels=5)
output = model(pyg_data)
```

### Graph Dataset for Multiple Slides

```python
from pathml.graph import GraphDataset
from torch_geometric.loader import DataLoader

# Create dataset of graphs from multiple slides
graphs = []
for slide in slides:
    # Build graph for each slide
    cell_graph = CellGraph.from_instance_map(slide.inst_map, ...)
    pyg_graph = cell_graph.to_pyg()
    graphs.append(pyg_graph)

# Create DataLoader
loader = DataLoader(graphs, batch_size=32, shuffle=True)

# Train GNN
for batch in loader:
    output = model(batch)
    loss = criterion(output, batch.y)
    loss.backward()
    optimizer.step()
```

## Visualization

### Graph Visualization

```python
import matplotlib.pyplot as plt
import networkx as nx

# Convert to NetworkX
nx_graph = cell_graph.to_networkx()

# Draw graph with cell positions as layout
pos = {i: cell_graph.positions[i] for i in range(len(cell_graph.nodes))}

plt.figure(figsize=(12, 12))
nx.draw_networkx(
    nx_graph,
    pos=pos,
    node_color=cell_type_labels,
    node_size=50,
    cmap='tab10',
    with_labels=False,
    alpha=0.8
)
plt.axis('equal')
plt.title('Cell Graph')
plt.show()
```

### Overlay on Tissue Image

```python
from pathml.graph import visualize_graph_on_image

# Visualize graph overlaid on tissue
fig, ax = plt.subplots(figsize=(15, 15))
ax.imshow(tissue_image)

# Draw edges
for edge in cell_graph.edges:
    node1, node2 = edge
    pos1 = cell_graph.positions[node1]
    pos2 = cell_graph.positions[node2]
    ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'b-', alpha=0.3, linewidth=0.5)

# Draw nodes colored by type
for cell_type in np.unique(cell_type_labels):
    mask = cell_type_labels == cell_type
    positions = cell_graph.positions[mask]
    ax.scatter(positions[:, 0], positions[:, 1], label=f'Type {cell_type}', s=20)

ax.legend()
ax.axis('off')
plt.title('Cell Graph on Tissue')
plt.show()
```

## Complete Workflow Example

```python
from pathml.core import SlideData, CODEXSlide
from pathml.preprocessing import Pipeline, CollapseRunsCODEX, SegmentMIF
from pathml.graph import CellGraph, extract_morphology_features, extract_intensity_features
import matplotlib.pyplot as plt

# 1. Load and preprocess slide
slide = CODEXSlide('path/to/codex', stain='IF')

pipeline = Pipeline([
    CollapseRunsCODEX(z_slice=2),
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])
pipeline.run(slide)

# 2. Build cell graph
inst_map = slide.masks['cell_segmentation']
cell_graph = CellGraph.from_instance_map(
    inst_map,
    image=slide.image,
    connectivity='knn',
    k=6
)

# 3. Extract features
# Morphological features
morph_features = extract_morphology_features(
    inst_map,
    features=['area', 'perimeter', 'eccentricity', 'solidity']
)
cell_graph.add_node_features(morph_features)

# Intensity features (marker expression)
intensity_features = extract_intensity_features(
    inst_map,
    image=slide.image,
    channel_names=['DAPI', 'CD3', 'CD4', 'CD8', 'CD20'],
    statistics=['mean', 'std']
)
cell_graph.add_node_features(intensity_features)

# 4. Spatial analysis
from pathml.graph import analyze_neighborhoods

neighborhoods = analyze_neighborhoods(
    cell_graph,
    cell_types=cell_type_predictions,
    radius=100,
    metrics=['diversity', 'composition']
)

# 5. Export for GNN
pyg_data = cell_graph.to_pyg()

# 6. Visualize
plt.figure(figsize=(15, 15))
plt.imshow(slide.image)

# Overlay graph
nx_graph = cell_graph.to_networkx()
pos = {i: cell_graph.positions[i] for i in range(cell_graph.num_nodes)}
nx.draw_networkx(
    nx_graph,
    pos=pos,
    node_color=cell_type_predictions,
    cmap='tab10',
    node_size=30,
    with_labels=False
)
plt.axis('off')
plt.title('Cell Graph with Spatial Neighborhood')
plt.show()
```

## Performance Considerations

**Large tissue sections:**
- Build graphs tile-by-tile, then merge
- Use sparse adjacency matrices
- Leverage GPU for feature extraction

**Memory efficiency:**
- Store only necessary edge features
- Use int32/float32 instead of int64/float64
- Batch process multiple slides

**Computational efficiency:**
- Parallelize feature extraction across cells
- Use KNN for faster neighbor queries
- Cache computed features

## Best Practices

1. **Choose appropriate connectivity:** KNN for uniform analysis, radius for physical interactions, contact for direct cell-cell communication

2. **Normalize features:** Scale morphological and intensity features for GNN compatibility

3. **Handle edge effects:** Exclude boundary cells or use tissue masks to define valid regions

4. **Validate graph construction:** Visualize graphs on small regions before large-scale processing

5. **Combine multiple feature types:** Morphology + intensity + texture provides rich representations

6. **Consider tissue context:** Tissue type affects appropriate graph parameters (connectivity, radius)

## Common Issues and Solutions

**Issue: Too many/few edges**
- Adjust k (KNN) or radius (radius-based) parameters
- Verify pixel-to-micron conversion for biological relevance

**Issue: Memory errors with large graphs**
- Process tiles separately and merge graphs
- Use sparse matrix representations
- Reduce edge features to essential ones

**Issue: Missing cells at tissue boundaries**
- Apply edge_correction parameter
- Use tissue masks to exclude invalid regions

**Issue: Inconsistent feature scales**
- Normalize features: `(x - mean) / std`
- Use robust scaling for outliers

## Additional Resources

- **PathML Graph API:** https://pathml.readthedocs.io/en/latest/api_graph_reference.html
- **PyTorch Geometric:** https://pytorch-geometric.readthedocs.io/
- **NetworkX:** https://networkx.org/
- **Spatial Statistics:** Baddeley et al., "Spatial Point Patterns: Methodology and Applications with R"

---

## Reference: Image_Loading

# Image Loading & Formats

## Overview

PathML provides comprehensive support for loading whole-slide images (WSI) from 160+ proprietary medical imaging formats. The framework abstracts vendor-specific complexities through unified slide classes and interfaces, enabling seamless access to image pyramids, metadata, and regions of interest across different file formats.

## Supported Formats

PathML supports the following slide formats:

### Brightfield Microscopy Formats
- **Aperio SVS** (`.svs`) - Leica Biosystems
- **Hamamatsu NDPI** (`.ndpi`) - Hamamatsu Photonics
- **Leica SCN** (`.scn`) - Leica Biosystems
- **Zeiss ZVI** (`.zvi`) - Carl Zeiss
- **3DHISTECH** (`.mrxs`) - 3DHISTECH Ltd.
- **Ventana BIF** (`.bif`) - Roche Ventana
- **Generic tiled TIFF** (`.tif`, `.tiff`)

### Medical Imaging Standards
- **DICOM** (`.dcm`) - Digital Imaging and Communications in Medicine
- **OME-TIFF** (`.ome.tif`, `.ome.tiff`) - Open Microscopy Environment

### Multiparametric Imaging
- **CODEX** - Spatial proteomics imaging
- **Vectra** (`.qptiff`) - Multiplex immunofluorescence
- **MERFISH** - Multiplexed error-robust FISH

PathML leverages OpenSlide and other specialized libraries to handle format-specific nuances automatically.

## Core Classes for Loading Images

### SlideData

`SlideData` is the fundamental class for representing whole-slide images in PathML.

**Loading from file:**
```python
from pathml.core import SlideData

# Load a whole-slide image
wsi = SlideData.from_slide("path/to/slide.svs")

# Load with specific backend
wsi = SlideData.from_slide("path/to/slide.svs", backend="openslide")

# Load from OME-TIFF
wsi = SlideData.from_slide("path/to/slide.ome.tiff", backend="bioformats")
```

**Key attributes:**
- `wsi.slide` - Backend slide object (OpenSlide, BioFormats, etc.)
- `wsi.tiles` - Collection of image tiles
- `wsi.metadata` - Slide metadata dictionary
- `wsi.level_dimensions` - Image pyramid level dimensions
- `wsi.level_downsamples` - Downsample factors for each pyramid level

**Methods:**
- `wsi.generate_tiles()` - Generate tiles from the slide
- `wsi.read_region()` - Read a specific region at a given level
- `wsi.get_thumbnail()` - Get a thumbnail image

### SlideType

`SlideType` is an enumeration defining supported slide backends:

```python
from pathml.core import SlideType

# Available backends
SlideType.OPENSLIDE  # For most WSI formats (SVS, NDPI, etc.)
SlideType.BIOFORMATS  # For OME-TIFF and other formats
SlideType.DICOM  # For DICOM WSI
SlideType.VectraQPTIFF  # For Vectra multiplex IF
```

### Specialized Slide Classes

PathML provides specialized slide classes for specific imaging modalities:

**CODEXSlide:**
```python
from pathml.core import CODEXSlide

# Load CODEX spatial proteomics data
codex_slide = CODEXSlide(
    path="path/to/codex_dir",
    stain="IF",  # Immunofluorescence
    backend="bioformats"
)
```

**VectraSlide:**
```python
from pathml.core import types

# Load Vectra multiplex IF data
vectra_slide = SlideData.from_slide(
    "path/to/vectra.qptiff",
    backend=SlideType.VectraQPTIFF
)
```

**MultiparametricSlide:**
```python
from pathml.core import MultiparametricSlide

# Generic multiparametric imaging
mp_slide = MultiparametricSlide(path="path/to/multiparametric_data")
```

## Loading Strategies

### Tile-Based Loading

For large WSI files, tile-based loading enables memory-efficient processing:

```python
from pathml.core import SlideData

# Load slide
wsi = SlideData.from_slide("path/to/slide.svs")

# Generate tiles at specific magnification level
wsi.generate_tiles(
    level=0,  # Pyramid level (0 = highest resolution)
    tile_size=256,  # Tile dimensions in pixels
    stride=256,  # Spacing between tiles (256 = no overlap)
    pad=False  # Whether to pad edge tiles
)

# Iterate over tiles
for tile in wsi.tiles:
    image = tile.image  # numpy array
    coords = tile.coords  # (x, y) coordinates
    # Process tile...
```

**Overlapping tiles:**
```python
# Generate tiles with 50% overlap
wsi.generate_tiles(
    level=0,
    tile_size=256,
    stride=128  # 50% overlap
)
```

### Region-Based Loading

Extract specific regions of interest directly:

```python
# Read region at specific location and level
region = wsi.read_region(
    location=(10000, 15000),  # (x, y) in level 0 coordinates
    level=1,  # Pyramid level
    size=(512, 512)  # Width, height in pixels
)

# Returns numpy array
```

### Pyramid Level Selection

Whole-slide images are stored in multi-resolution pyramids. Select the appropriate level based on desired magnification:

```python
# Inspect available levels
print(wsi.level_dimensions)  # [(width0, height0), (width1, height1), ...]
print(wsi.level_downsamples)  # [1.0, 4.0, 16.0, ...]

# Load at lower resolution for faster processing
wsi.generate_tiles(level=2, tile_size=256)  # Use level 2 (16x downsampled)
```

**Common pyramid levels:**
- Level 0: Full resolution (e.g., 40x magnification)
- Level 1: 4x downsampled (e.g., 10x magnification)
- Level 2: 16x downsampled (e.g., 2.5x magnification)
- Level 3: 64x downsampled (thumbnail)

### Thumbnail Loading

Generate low-resolution thumbnails for visualization and quality control:

```python
# Get thumbnail
thumbnail = wsi.get_thumbnail(size=(1024, 1024))

# Display with matplotlib
import matplotlib.pyplot as plt
plt.imshow(thumbnail)
plt.axis('off')
plt.show()
```

## Batch Loading with SlideDataset

Process multiple slides efficiently using `SlideDataset`:

```python
from pathml.core import SlideDataset
import glob

# Create dataset from multiple slides
slide_paths = glob.glob("data/*.svs")
dataset = SlideDataset(
    slide_paths,
    tile_size=256,
    stride=256,
    level=0
)

# Iterate over all tiles from all slides
for tile in dataset:
    image = tile.image
    slide_id = tile.slide_id
    # Process tile...
```

**With preprocessing pipeline:**
```python
from pathml.preprocessing import Pipeline, StainNormalizationHE

# Create pipeline
pipeline = Pipeline([
    StainNormalizationHE(target='normalize')
])

# Apply to entire dataset
dataset = SlideDataset(slide_paths)
dataset.run(pipeline, distributed=True, n_workers=8)
```

## Metadata Access

Extract slide metadata including acquisition parameters, magnification, and vendor-specific information:

```python
# Access metadata
metadata = wsi.metadata

# Common metadata fields
print(metadata.get('openslide.objective-power'))  # Magnification
print(metadata.get('openslide.mpp-x'))  # Microns per pixel X
print(metadata.get('openslide.mpp-y'))  # Microns per pixel Y
print(metadata.get('openslide.vendor'))  # Scanner vendor

# Slide dimensions
print(wsi.level_dimensions[0])  # (width, height) at level 0
```

## Working with DICOM Slides

PathML supports DICOM WSI through specialized handling:

```python
from pathml.core import SlideData, SlideType

# Load DICOM WSI
dicom_slide = SlideData.from_slide(
    "path/to/slide.dcm",
    backend=SlideType.DICOM
)

# DICOM-specific metadata
print(dicom_slide.metadata.get('PatientID'))
print(dicom_slide.metadata.get('StudyDate'))
```

## Working with OME-TIFF

OME-TIFF provides an open standard for multi-dimensional imaging:

```python
from pathml.core import SlideData

# Load OME-TIFF
ome_slide = SlideData.from_slide(
    "path/to/slide.ome.tiff",
    backend="bioformats"
)

# Access channel information for multi-channel images
n_channels = ome_slide.shape[2]  # Number of channels
```

## Performance Considerations

### Memory Management

For large WSI files (often >1GB), use tile-based loading to avoid memory exhaustion:

```python
# Efficient: Tile-based processing
wsi.generate_tiles(level=1, tile_size=256)
for tile in wsi.tiles:
    process_tile(tile)  # Process one tile at a time

# Inefficient: Loading entire slide into memory
full_image = wsi.read_region((0, 0), level=0, wsi.level_dimensions[0])  # May crash
```

### Distributed Processing

Use Dask for parallel processing across multiple workers:

```python
from pathml.core import SlideDataset
from dask.distributed import Client

# Start Dask client
client = Client(n_workers=8, threads_per_worker=2)

# Process dataset in parallel
dataset = SlideDataset(slide_paths)
dataset.run(pipeline, distributed=True, client=client)
```

### Level Selection

Balance resolution and performance by selecting appropriate pyramid levels:

- **Level 0:** Use for final analysis requiring maximum detail
- **Level 1-2:** Use for most preprocessing and model training
- **Level 3+:** Use for thumbnails, quality control, and rapid exploration

## Common Issues and Solutions

**Issue: Slide fails to load**
- Verify file format is supported
- Check file permissions and path
- Try different backend: `backend="bioformats"` or `backend="openslide"`

**Issue: Out of memory errors**
- Use tile-based loading instead of full-slide loading
- Process at lower pyramid level (e.g., level=1 or level=2)
- Reduce tile_size parameter
- Enable distributed processing with Dask

**Issue: Color inconsistencies across slides**
- Apply stain normalization preprocessing (see `preprocessing.md`)
- Check scanner metadata for calibration information
- Use `StainNormalizationHE` transform in preprocessing pipeline

**Issue: Metadata missing or incorrect**
- Different vendors store metadata in different locations
- Use `wsi.metadata` to inspect available fields
- Some formats may have limited metadata support

## Best Practices

1. **Always inspect pyramid structure** before processing: Check `level_dimensions` and `level_downsamples` to understand available resolutions

2. **Use appropriate pyramid levels**: Process at level 1-2 for most tasks; reserve level 0 for final high-resolution analysis

3. **Tile with overlap** for segmentation tasks: Use stride < tile_size to avoid edge artifacts

4. **Verify magnification consistency**: Check `openslide.objective-power` metadata when combining slides from different sources

5. **Handle vendor-specific formats**: Use specialized slide classes (CODEXSlide, VectraSlide) for multiparametric data

6. **Implement quality control**: Generate thumbnails and inspect for artifacts before processing

7. **Use distributed processing** for large datasets: Leverage Dask for parallel processing across multiple workers

## Example Workflows

### Loading and Inspecting a New Slide

```python
from pathml.core import SlideData
import matplotlib.pyplot as plt

# Load slide
wsi = SlideData.from_slide("path/to/slide.svs")

# Inspect properties
print(f"Dimensions: {wsi.level_dimensions}")
print(f"Downsamples: {wsi.level_downsamples}")
print(f"Magnification: {wsi.metadata.get('openslide.objective-power')}")

# Generate thumbnail for QC
thumbnail = wsi.get_thumbnail(size=(1024, 1024))
plt.imshow(thumbnail)
plt.title(f"Slide: {wsi.name}")
plt.axis('off')
plt.show()
```

### Processing Multiple Slides

```python
from pathml.core import SlideDataset
from pathml.preprocessing import Pipeline, TissueDetectionHE
import glob

# Find all slides
slide_paths = glob.glob("data/slides/*.svs")

# Create pipeline
pipeline = Pipeline([TissueDetectionHE()])

# Process all slides
dataset = SlideDataset(
    slide_paths,
    tile_size=512,
    stride=512,
    level=1
)

# Run pipeline with distributed processing
dataset.run(pipeline, distributed=True, n_workers=8)

# Save processed data
dataset.to_hdf5("processed_dataset.h5")
```

### Loading CODEX Multiparametric Data

```python
from pathml.core import CODEXSlide
from pathml.preprocessing import Pipeline, CollapseRunsCODEX, SegmentMIF

# Load CODEX slide
codex = CODEXSlide("path/to/codex_dir", stain="IF")

# Create CODEX-specific pipeline
pipeline = Pipeline([
    CollapseRunsCODEX(z_slice=2),  # Select z-slice
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])

# Process
pipeline.run(codex)
```

## Additional Resources

- **PathML Documentation:** https://pathml.readthedocs.io/
- **OpenSlide:** https://openslide.org/ (underlying library for WSI formats)
- **Bio-Formats:** https://www.openmicroscopy.org/bio-formats/ (alternative backend)
- **DICOM Standard:** https://www.dicomstandard.org/

---

## Reference: Machine_Learning

# Machine Learning

## Overview

PathML provides comprehensive machine learning capabilities for computational pathology, including pre-built models for nucleus detection and segmentation, PyTorch-integrated training workflows, public dataset access, and ONNX-based inference deployment. The framework seamlessly bridges image preprocessing with deep learning to enable end-to-end pathology ML pipelines.

## Pre-Built Models

PathML includes state-of-the-art pre-trained models for nucleus analysis:

### HoVer-Net

**HoVer-Net** (Horizontal and Vertical Network) performs simultaneous nucleus instance segmentation and classification.

**Architecture:**
- Encoder-decoder structure with three prediction branches:
  - **Nuclear Pixel (NP)** - Binary segmentation of nuclear regions
  - **Horizontal-Vertical (HV)** - Distance maps to nucleus centroids
  - **Classification (NC)** - Nucleus type classification

**Nucleus types:**
1. Epithelial
2. Inflammatory
3. Connective/Soft tissue
4. Dead/Necrotic
5. Background

**Usage:**
```python
from pathml.ml import HoVerNet
import torch

# Load pre-trained model
model = HoVerNet(
    num_types=5,  # Number of nucleus types
    mode='fast',  # 'fast' or 'original'
    pretrained=True  # Load pre-trained weights
)

# Move to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Inference on tile
tile_image = torch.from_numpy(tile.image).permute(2, 0, 1).unsqueeze(0).float()
tile_image = tile_image.to(device)

with torch.no_grad():
    output = model(tile_image)

# Output contains:
# - output['np']: Nuclear pixel predictions
# - output['hv']: Horizontal-vertical maps
# - output['nc']: Classification predictions
```

**Post-processing:**
```python
from pathml.ml import hovernet_postprocess

# Convert model outputs to instance segmentation
instance_map, type_map = hovernet_postprocess(
    np_pred=output['np'],
    hv_pred=output['hv'],
    nc_pred=output['nc']
)

# instance_map: Each nucleus has unique ID
# type_map: Each nucleus assigned a type (1-5)
```

### HACTNet

**HACTNet** (Hierarchical Cell-Type Network) performs hierarchical nucleus classification with uncertainty quantification.

**Features:**
- Hierarchical classification (coarse to fine-grained types)
- Uncertainty estimation for predictions
- Improved performance on imbalanced datasets

```python
from pathml.ml import HACTNet

# Load model
model = HACTNet(
    num_classes_coarse=3,
    num_classes_fine=8,
    pretrained=True
)

# Inference
output = model(tile_image)
coarse_pred = output['coarse']  # Broad categories
fine_pred = output['fine']  # Specific cell types
uncertainty = output['uncertainty']  # Prediction confidence
```

## Training Workflows

### Dataset Preparation

PathML provides PyTorch-compatible dataset classes:

**TileDataset:**
```python
from pathml.ml import TileDataset
from pathml.core import SlideDataset

# Create dataset from processed slides
tile_dataset = TileDataset(
    slide_dataset,
    tile_size=256,
    transform=None  # Optional augmentation transforms
)

# Access tiles
image, label = tile_dataset[0]
```

**DataModule Integration:**
```python
from pathml.ml import PathMLDataModule

# Create train/val/test splits
data_module = PathMLDataModule(
    train_dataset=train_tile_dataset,
    val_dataset=val_tile_dataset,
    test_dataset=test_tile_dataset,
    batch_size=32,
    num_workers=4
)

# Use with PyTorch Lightning
trainer = pl.Trainer(max_epochs=100)
trainer.fit(model, data_module)
```

### Training HoVer-Net

Complete workflow for training HoVer-Net on custom data:

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from pathml.ml import HoVerNet
from pathml.ml.datasets import PanNukeDataModule

# 1. Prepare data
data_module = PanNukeDataModule(
    data_dir='path/to/pannuke',
    batch_size=8,
    num_workers=4,
    tissue_types=['Breast', 'Colon']  # Specific tissue types
)

# 2. Initialize model
model = HoVerNet(
    num_types=5,
    mode='fast',
    pretrained=False  # Train from scratch or use pretrained=True for fine-tuning
)

# 3. Define loss function
class HoVerNetLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse_loss = nn.MSELoss()
        self.bce_loss = nn.BCEWithLogitsLoss()
        self.ce_loss = nn.CrossEntropyLoss()

    def forward(self, output, target):
        # Nuclear pixel branch loss
        np_loss = self.bce_loss(output['np'], target['np'])

        # Horizontal-vertical branch loss
        hv_loss = self.mse_loss(output['hv'], target['hv'])

        # Classification branch loss
        nc_loss = self.ce_loss(output['nc'], target['nc'])

        # Combined loss
        total_loss = np_loss + hv_loss + 2.0 * nc_loss
        return total_loss, {'np': np_loss, 'hv': hv_loss, 'nc': nc_loss}

criterion = HoVerNetLoss()

# 4. Configure optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-4,
    weight_decay=1e-5
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.5,
    patience=10
)

# 5. Training loop
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0

    for batch in data_module.train_dataloader():
        images = batch['image'].to(device)
        targets = {
            'np': batch['np_map'].to(device),
            'hv': batch['hv_map'].to(device),
            'nc': batch['type_map'].to(device)
        }

        optimizer.zero_grad()
        outputs = model(images)
        loss, loss_dict = criterion(outputs, targets)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch in data_module.val_dataloader():
            images = batch['image'].to(device)
            targets = {
                'np': batch['np_map'].to(device),
                'hv': batch['hv_map'].to(device),
                'nc': batch['type_map'].to(device)
            }
            outputs = model(images)
            loss, _ = criterion(outputs, targets)
            val_loss += loss.item()

    scheduler.step(val_loss)

    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"  Train Loss: {train_loss/len(data_module.train_dataloader()):.4f}")
    print(f"  Val Loss: {val_loss/len(data_module.val_dataloader()):.4f}")

    # Save checkpoint
    if (epoch + 1) % 10 == 0:
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': val_loss,
        }, f'hovernet_checkpoint_epoch_{epoch+1}.pth')
```

### PyTorch Lightning Integration

PathML models integrate with PyTorch Lightning for streamlined training:

```python
import pytorch_lightning as pl
from pathml.ml import HoVerNet
from pathml.ml.datasets import PanNukeDataModule

class HoVerNetModule(pl.LightningModule):
    def __init__(self, num_types=5, lr=1e-4):
        super().__init__()
        self.model = HoVerNet(num_types=num_types, pretrained=True)
        self.lr = lr
        self.criterion = HoVerNetLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        images = batch['image']
        targets = {
            'np': batch['np_map'],
            'hv': batch['hv_map'],
            'nc': batch['type_map']
        }
        outputs = self(images)
        loss, loss_dict = self.criterion(outputs, targets)

        # Log metrics
        self.log('train_loss', loss, prog_bar=True)
        for key, val in loss_dict.items():
            self.log(f'train_{key}_loss', val)

        return loss

    def validation_step(self, batch, batch_idx):
        images = batch['image']
        targets = {
            'np': batch['np_map'],
            'hv': batch['hv_map'],
            'nc': batch['type_map']
        }
        outputs = self(images)
        loss, loss_dict = self.criterion(outputs, targets)

        self.log('val_loss', loss, prog_bar=True)
        for key, val in loss_dict.items():
            self.log(f'val_{key}_loss', val)

        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }

# Train with PyTorch Lightning
data_module = PanNukeDataModule(data_dir='path/to/pannuke', batch_size=8)
model = HoVerNetModule(num_types=5, lr=1e-4)

trainer = pl.Trainer(
    max_epochs=100,
    accelerator='gpu',
    devices=1,
    callbacks=[
        pl.callbacks.ModelCheckpoint(monitor='val_loss', mode='min'),
        pl.callbacks.EarlyStopping(monitor='val_loss', patience=20)
    ]
)

trainer.fit(model, data_module)
```

## Public Datasets

PathML provides convenient access to public pathology datasets:

### PanNuke Dataset

**PanNuke** contains 7,901 histology image patches from 19 tissue types with nucleus annotations for 5 cell types.

```python
from pathml.ml.datasets import PanNukeDataModule

# Load PanNuke dataset
pannuke = PanNukeDataModule(
    data_dir='path/to/pannuke',
    batch_size=16,
    num_workers=4,
    tissue_types=None,  # Use all tissue types, or specify list
    fold='all'  # 'fold1', 'fold2', 'fold3', or 'all'
)

# Access dataloaders
train_loader = pannuke.train_dataloader()
val_loader = pannuke.val_dataloader()
test_loader = pannuke.test_dataloader()

# Batch structure
for batch in train_loader:
    images = batch['image']  # Shape: (B, 3, 256, 256)
    inst_map = batch['inst_map']  # Instance segmentation map
    type_map = batch['type_map']  # Cell type map
    np_map = batch['np_map']  # Nuclear pixel map
    hv_map = batch['hv_map']  # Horizontal-vertical distance maps
    tissue_type = batch['tissue_type']  # Tissue category
```

**Tissue types available:**
Breast, Colon, Prostate, Lung, Kidney, Stomach, Bladder, Esophagus, Cervix, Liver, Thyroid, Head & Neck, Testis, Adrenal, Pancreas, Bile Duct, Ovary, Skin, Uterus

### TCGA Datasets

Access The Cancer Genome Atlas datasets:

```python
from pathml.ml.datasets import TCGADataModule

# Load TCGA dataset
tcga = TCGADataModule(
    data_dir='path/to/tcga',
    cancer_type='BRCA',  # Breast cancer
    batch_size=32,
    tile_size=224
)
```

### Custom Dataset Integration

Create custom datasets for PathML workflows:

```python
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path

class CustomPathologyDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = Path(data_dir)
        self.image_paths = list(self.data_dir.glob('images/*.png'))
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image
        image_path = self.image_paths[idx]
        image = np.array(Image.open(image_path))

        # Load corresponding annotation
        annot_path = self.data_dir / 'annotations' / f'{image_path.stem}.npy'
        annotation = np.load(annot_path)

        # Apply transforms
        if self.transform:
            image = self.transform(image)

        return {
            'image': torch.from_numpy(image).permute(2, 0, 1).float(),
            'annotation': torch.from_numpy(annotation).long(),
            'path': str(image_path)
        }

# Use in PathML workflow
dataset = CustomPathologyDataset('path/to/data')
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=4)
```

## Data Augmentation

Apply augmentations to improve model generalization:

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Define augmentation pipeline
train_transform = A.Compose([
    A.RandomRotate90(p=0.5),
    A.Flip(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.5),
    A.GaussianBlur(blur_limit=(3, 7), p=0.3),
    A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50, p=0.3),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

val_transform = A.Compose([
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

# Apply to dataset
train_dataset = TileDataset(slide_dataset, transform=train_transform)
val_dataset = TileDataset(val_slide_dataset, transform=val_transform)
```

## Model Evaluation

### Metrics

Evaluate model performance with pathology-specific metrics:

```python
from pathml.ml.metrics import (
    dice_coefficient,
    aggregated_jaccard_index,
    panoptic_quality
)

# Dice coefficient for segmentation
dice = dice_coefficient(pred_mask, true_mask)

# Aggregated Jaccard Index (AJI) for instance segmentation
aji = aggregated_jaccard_index(pred_inst, true_inst)

# Panoptic Quality (PQ) for joint segmentation and classification
pq, sq, rq = panoptic_quality(pred_inst, true_inst, pred_types, true_types)

print(f"Dice: {dice:.4f}")
print(f"AJI: {aji:.4f}")
print(f"PQ: {pq:.4f}, SQ: {sq:.4f}, RQ: {rq:.4f}")
```

### Evaluation Loop

```python
from pathml.ml.metrics import evaluate_hovernet

# Comprehensive HoVer-Net evaluation
model.eval()
all_preds = []
all_targets = []

with torch.no_grad():
    for batch in test_loader:
        images = batch['image'].to(device)
        outputs = model(images)

        # Post-process predictions
        for i in range(len(images)):
            inst_pred, type_pred = hovernet_postprocess(
                outputs['np'][i],
                outputs['hv'][i],
                outputs['nc'][i]
            )
            all_preds.append({'inst': inst_pred, 'type': type_pred})
            all_targets.append({
                'inst': batch['inst_map'][i],
                'type': batch['type_map'][i]
            })

# Compute metrics
results = evaluate_hovernet(all_preds, all_targets)

print(f"Detection F1: {results['detection_f1']:.4f}")
print(f"Classification Accuracy: {results['classification_acc']:.4f}")
print(f"Panoptic Quality: {results['pq']:.4f}")
```

## ONNX Inference

Deploy models using ONNX for production inference:

### Export to ONNX

```python
import torch
from pathml.ml import HoVerNet

# Load trained model
model = HoVerNet(num_types=5, pretrained=True)
model.eval()

# Create dummy input
dummy_input = torch.randn(1, 3, 256, 256)

# Export to ONNX
torch.onnx.export(
    model,
    dummy_input,
    'hovernet_model.onnx',
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['np_output', 'hv_output', 'nc_output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'np_output': {0: 'batch_size'},
        'hv_output': {0: 'batch_size'},
        'nc_output': {0: 'batch_size'}
    }
)
```

### ONNX Runtime Inference

```python
import onnxruntime as ort
import numpy as np

# Load ONNX model
session = ort.InferenceSession('hovernet_model.onnx')

# Prepare input
input_name = session.get_inputs()[0].name
tile_image = preprocess_tile(tile)  # Normalize, transpose to (1, 3, H, W)

# Run inference
outputs = session.run(None, {input_name: tile_image})
np_output, hv_output, nc_output = outputs

# Post-process
inst_map, type_map = hovernet_postprocess(np_output, hv_output, nc_output)
```

### Batch Inference Pipeline

```python
from pathml.core import SlideData
from pathml.preprocessing import Pipeline
import onnxruntime as ort

def run_onnx_inference_pipeline(slide_path, onnx_model_path):
    # Load slide
    wsi = SlideData.from_slide(slide_path)
    wsi.generate_tiles(level=1, tile_size=256, stride=256)

    # Load ONNX model
    session = ort.InferenceSession(onnx_model_path)
    input_name = session.get_inputs()[0].name

    # Inference on all tiles
    results = []
    for tile in wsi.tiles:
        # Preprocess
        tile_array = preprocess_tile(tile.image)

        # Inference
        outputs = session.run(None, {input_name: tile_array})

        # Post-process
        inst_map, type_map = hovernet_postprocess(*outputs)

        results.append({
            'coords': tile.coords,
            'instance_map': inst_map,
            'type_map': type_map
        })

    return results

# Run on slide
results = run_onnx_inference_pipeline('slide.svs', 'hovernet_model.onnx')
```

## Transfer Learning

Fine-tune pre-trained models on custom datasets:

```python
from pathml.ml import HoVerNet

# Load pre-trained model
model = HoVerNet(num_types=5, pretrained=True)

# Freeze encoder layers for initial training
for name, param in model.named_parameters():
    if 'encoder' in name:
        param.requires_grad = False

# Fine-tune only decoder and classification heads
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-4
)

# Train for a few epochs
train_for_n_epochs(model, train_loader, optimizer, num_epochs=10)

# Unfreeze all layers for full fine-tuning
for param in model.parameters():
    param.requires_grad = True

# Continue training with lower learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
train_for_n_epochs(model, train_loader, optimizer, num_epochs=50)
```

## Best Practices

1. **Use pre-trained models when available:**
   - Start with pretrained=True for better initialization
   - Fine-tune on domain-specific data

2. **Apply appropriate data augmentation:**
   - Rotate, flip for orientation invariance
   - Color jitter to handle staining variations
   - Elastic deformation for biological variability

3. **Monitor multiple metrics:**
   - Track detection, segmentation, and classification separately
   - Use domain-specific metrics (AJI, PQ) beyond standard accuracy

4. **Handle class imbalance:**
   - Weighted loss functions for rare cell types
   - Oversampling minority classes
   - Focal loss for hard examples

5. **Validate on diverse tissue types:**
   - Ensure generalization across different tissues
   - Test on held-out anatomical sites

6. **Optimize for inference:**
   - Export to ONNX for faster deployment
   - Batch tiles for efficient GPU utilization
   - Use mixed precision (FP16) when possible

7. **Save checkpoints regularly:**
   - Keep best model based on validation metrics
   - Save optimizer state for training resumption

## Common Issues and Solutions

**Issue: Poor segmentation at nucleus boundaries**
- Use HV maps (horizontal-vertical) to separate touching nuclei
- Increase weight of HV loss term
- Apply morphological post-processing

**Issue: Misclassification of similar cell types**
- Increase classification loss weight
- Add hierarchical classification (HACTNet)
- Augment training data for confused classes

**Issue: Training unstable or not converging**
- Reduce learning rate
- Use gradient clipping: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Check for data preprocessing issues

**Issue: Out of memory during training**
- Reduce batch size
- Use gradient accumulation
- Enable mixed precision training: `torch.cuda.amp`

**Issue: Model overfits to training data**
- Increase data augmentation
- Add dropout layers
- Reduce model capacity
- Use early stopping based on validation loss

## Additional Resources

- **PathML ML API:** https://pathml.readthedocs.io/en/latest/api_ml_reference.html
- **HoVer-Net Paper:** Graham et al., "HoVer-Net: Simultaneous Segmentation and Classification of Nuclei in Multi-Tissue Histology Images," Medical Image Analysis, 2019
- **PanNuke Dataset:** https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke
- **PyTorch Lightning:** https://www.pytorchlightning.ai/
- **ONNX Runtime:** https://onnxruntime.ai/

---

## Reference: Multiparametric

# Multiparametric Imaging

## Overview

PathML provides specialized support for multiparametric imaging technologies that simultaneously measure multiple markers at single-cell resolution. These techniques include CODEX, Vectra multiplex immunofluorescence, MERFISH, and other spatial proteomics and transcriptomics platforms. PathML handles the unique data structures, processing requirements, and quantification workflows specific to each technology.

## Supported Technologies

### CODEX (CO-Detection by indEXing)
- Cyclic immunofluorescence imaging
- 40+ protein markers simultaneously
- Single-cell spatial proteomics
- Multi-cycle acquisition with antibody barcoding

### Vectra Polaris
- Multispectral multiplex immunofluorescence
- 6-8 markers per slide
- Spectral unmixing
- Whole-slide scanning

### MERFISH (Multiplexed Error-Robust FISH)
- Spatial transcriptomics
- 100s-1000s of genes
- Single-molecule resolution
- Error-correcting barcodes

### Other Platforms
- CycIF (Cyclic Immunofluorescence)
- IMC (Imaging Mass Cytometry)
- MIBI (Multiplexed Ion Beam Imaging)

## CODEX Workflows

### Loading CODEX Data

CODEX data is typically organized in multi-channel image stacks from multiple acquisition cycles:

```python
from pathml.core import CODEXSlide

# Load CODEX dataset
codex_slide = CODEXSlide(
    path='path/to/codex_directory',
    stain='IF',  # Immunofluorescence
    backend='bioformats'
)

# Inspect channels and cycles
print(f"Number of channels: {codex_slide.num_channels}")
print(f"Channel names: {codex_slide.channel_names}")
print(f"Number of cycles: {codex_slide.num_cycles}")
print(f"Image shape: {codex_slide.shape}")
```

**CODEX directory structure:**
```
codex_directory/
├── cyc001_reg001/
│   ├── 1_00001_Z001_CH1.tif
│   ├── 1_00001_Z001_CH2.tif
│   └── ...
├── cyc002_reg001/
│   └── ...
└── channelnames.txt
```

### CODEX Preprocessing Pipeline

Complete pipeline for CODEX data processing:

```python
from pathml.preprocessing import Pipeline, CollapseRunsCODEX, SegmentMIF, QuantifyMIF

# Create CODEX-specific pipeline
codex_pipeline = Pipeline([
    # 1. Collapse multi-cycle data
    CollapseRunsCODEX(
        z_slice=2,  # Select focal plane from z-stack
        run_order=None,  # Automatic cycle ordering, or specify [0, 1, 2, ...]
        method='max'  # 'max', 'mean', or 'median' across cycles
    ),

    # 2. Cell segmentation using Mesmer
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',  # Or other membrane/cytoplasm marker
        model='mesmer',
        image_resolution=0.377,  # Microns per pixel
        compartment='whole-cell'  # 'nuclear', 'cytoplasm', or 'whole-cell'
    ),

    # 3. Quantify marker expression per cell
    QuantifyMIF(
        segmentation_mask_name='cell_segmentation',
        markers=[
            'DAPI', 'CD3', 'CD4', 'CD8', 'CD20', 'CD45',
            'CD68', 'PD1', 'PDL1', 'Ki67', 'panCK'
        ],
        output_format='anndata'
    )
])

# Run pipeline
codex_pipeline.run(codex_slide)

# Access results
segmentation_mask = codex_slide.masks['cell_segmentation']
cell_data = codex_slide.cell_data  # AnnData object
```

### CollapseRunsCODEX

Consolidates multi-cycle CODEX acquisitions into a single multi-channel image:

```python
from pathml.preprocessing import CollapseRunsCODEX

transform = CollapseRunsCODEX(
    z_slice=2,  # Select which z-plane (0-indexed)
    run_order=[0, 1, 2, 3],  # Order of acquisition cycles
    method='max',  # Aggregation method across cycles
    background_subtract=True,  # Subtract background fluorescence
    channel_mapping=None  # Optional: remap channel order
)
```

**Parameters:**
- `z_slice`: Which focal plane to extract from z-stacks (typically middle slice)
- `run_order`: Order of cycles; None for automatic detection
- `method`: How to combine channels from multiple cycles ('max', 'mean', 'median')
- `background_subtract`: Whether to subtract background fluorescence

**Output:** Single multi-channel image with all markers (H, W, C)

### Cell Segmentation with Mesmer

DeepCell Mesmer provides accurate cell segmentation for multiparametric imaging:

```python
from pathml.preprocessing import SegmentMIF

transform = SegmentMIF(
    nuclear_channel='DAPI',  # Nuclear marker (required)
    cytoplasm_channel='CD45',  # Cytoplasm/membrane marker (required)
    model='mesmer',  # DeepCell Mesmer model
    image_resolution=0.377,  # Microns per pixel (important for accuracy)
    compartment='whole-cell',  # Segmentation output
    min_cell_size=50,  # Minimum cell size in pixels
    max_cell_size=1000  # Maximum cell size in pixels
)
```

**Choosing cytoplasm channel:**
- **CD45**: Pan-leukocyte marker (good for immune-rich tissues)
- **panCK**: Pan-cytokeratin (good for epithelial tissues)
- **CD298/b2m**: Universal membrane marker
- **Combination**: Average multiple membrane markers

**Compartment options:**
- `'whole-cell'`: Full cell segmentation (nucleus + cytoplasm)
- `'nuclear'`: Nuclear segmentation only
- `'cytoplasm'`: Cytoplasmic compartment only

### Remote Segmentation

Use DeepCell cloud API for segmentation without local GPU:

```python
from pathml.preprocessing import SegmentMIFRemote

transform = SegmentMIFRemote(
    nuclear_channel='DAPI',
    cytoplasm_channel='CD45',
    model='mesmer',
    api_url='https://deepcell.org/api/predict',
    timeout=300  # Timeout in seconds
)
```

### Marker Quantification

Extract single-cell marker expression from segmented images:

```python
from pathml.preprocessing import QuantifyMIF

transform = QuantifyMIF(
    segmentation_mask_name='cell_segmentation',
    markers=['DAPI', 'CD3', 'CD4', 'CD8', 'CD20', 'CD68', 'panCK'],
    output_format='anndata',  # or 'dataframe'
    statistics=['mean', 'median', 'std', 'total'],  # Aggregation methods
    compartments=['whole-cell', 'nuclear', 'cytoplasm']  # If multiple masks
)
```

**Output:** AnnData object with:
- `adata.X`: Marker expression matrix (cells × markers)
- `adata.obs`: Cell metadata (cell ID, coordinates, area, etc.)
- `adata.var`: Marker metadata
- `adata.obsm['spatial']`: Cell centroid coordinates

### Integration with AnnData

Process multiple CODEX slides into unified AnnData object:

```python
from pathml.core import SlideDataset
import anndata as ad

# Process multiple slides
slide_paths = ['slide1', 'slide2', 'slide3']
dataset = SlideDataset(
    [CODEXSlide(p, stain='IF') for p in slide_paths]
)

# Run pipeline on all slides
dataset.run(codex_pipeline, distributed=True, n_workers=8)

# Combine into single AnnData
adatas = []
for slide in dataset:
    adata = slide.cell_data
    adata.obs['slide_id'] = slide.name
    adatas.append(adata)

# Concatenate
combined_adata = ad.concat(adatas, join='outer', label='batch', keys=slide_paths)

# Save for downstream analysis
combined_adata.write('codex_dataset.h5ad')
```

## Vectra Workflows

### Loading Vectra Data

Vectra stores data in proprietary `.qptiff` format:

```python
from pathml.core import SlideData, SlideType

# Load Vectra slide
vectra_slide = SlideData.from_slide(
    'path/to/slide.qptiff',
    backend=SlideType.VectraQPTIFF
)

# Access spectral channels
print(f"Channels: {vectra_slide.channel_names}")
```

### Vectra Preprocessing

```python
from pathml.preprocessing import Pipeline, CollapseRunsVectra, SegmentMIF, QuantifyMIF

vectra_pipeline = Pipeline([
    # 1. Process Vectra multi-channel data
    CollapseRunsVectra(
        wavelengths=[520, 540, 570, 620, 670, 780],  # Emission wavelengths
        unmix=True,  # Apply spectral unmixing
        autofluorescence_correction=True
    ),

    # 2. Cell segmentation
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='FITC',
        model='mesmer',
        image_resolution=0.5
    ),

    # 3. Quantification
    QuantifyMIF(
        segmentation_mask_name='cell_segmentation',
        markers=['DAPI', 'CD3', 'CD8', 'PD1', 'PDL1', 'panCK'],
        output_format='anndata'
    )
])

vectra_pipeline.run(vectra_slide)
```

## Downstream Analysis

### Cell Type Annotation

Annotate cells based on marker expression:

```python
import anndata as ad
import numpy as np

# Load quantified data
adata = ad.read_h5ad('codex_dataset.h5ad')

# Define cell types by marker thresholds
def annotate_cell_types(adata, thresholds):
    cell_types = np.full(adata.n_obs, 'Unknown', dtype=object)

    # T cells: CD3+
    cd3_pos = adata[:, 'CD3'].X.flatten() > thresholds['CD3']
    cell_types[cd3_pos] = 'T cell'

    # CD4 T cells: CD3+ CD4+ CD8-
    cd4_tcells = (
        (adata[:, 'CD3'].X.flatten() > thresholds['CD3']) &
        (adata[:, 'CD4'].X.flatten() > thresholds['CD4']) &
        (adata[:, 'CD8'].X.flatten() < thresholds['CD8'])
    )
    cell_types[cd4_tcells] = 'CD4 T cell'

    # CD8 T cells: CD3+ CD8+ CD4-
    cd8_tcells = (
        (adata[:, 'CD3'].X.flatten() > thresholds['CD3']) &
        (adata[:, 'CD8'].X.flatten() > thresholds['CD8']) &
        (adata[:, 'CD4'].X.flatten() < thresholds['CD4'])
    )
    cell_types[cd8_tcells] = 'CD8 T cell'

    # B cells: CD20+
    b_cells = adata[:, 'CD20'].X.flatten() > thresholds['CD20']
    cell_types[b_cells] = 'B cell'

    # Macrophages: CD68+
    macrophages = adata[:, 'CD68'].X.flatten() > thresholds['CD68']
    cell_types[macrophages] = 'Macrophage'

    # Tumor cells: panCK+
    tumor = adata[:, 'panCK'].X.flatten() > thresholds['panCK']
    cell_types[tumor] = 'Tumor'

    return cell_types

# Apply annotation
thresholds = {
    'CD3': 0.5,
    'CD4': 0.4,
    'CD8': 0.4,
    'CD20': 0.3,
    'CD68': 0.3,
    'panCK': 0.5
}

adata.obs['cell_type'] = annotate_cell_types(adata, thresholds)

# Visualize cell type composition
import matplotlib.pyplot as plt
cell_type_counts = adata.obs['cell_type'].value_counts()
plt.figure(figsize=(10, 6))
cell_type_counts.plot(kind='bar')
plt.xlabel('Cell Type')
plt.ylabel('Count')
plt.title('Cell Type Composition')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Clustering

Unsupervised clustering to identify cell populations:

```python
import scanpy as sc

# Preprocessing for clustering
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.scale(adata, max_value=10)

# PCA
sc.tl.pca(adata, n_comps=50)

# Neighborhood graph
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)

# UMAP embedding
sc.tl.umap(adata)

# Leiden clustering
sc.tl.leiden(adata, resolution=0.5)

# Visualize
sc.pl.umap(adata, color=['leiden', 'CD3', 'CD8', 'CD20', 'panCK'])
```

### Spatial Visualization

Visualize cells in spatial context:

```python
import matplotlib.pyplot as plt

# Spatial scatter plot
fig, ax = plt.subplots(figsize=(15, 15))

# Color by cell type
cell_types = adata.obs['cell_type'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(cell_types)))

for i, cell_type in enumerate(cell_types):
    mask = adata.obs['cell_type'] == cell_type
    coords = adata.obsm['spatial'][mask]
    ax.scatter(
        coords[:, 0],
        coords[:, 1],
        c=[colors[i]],
        label=cell_type,
        s=5,
        alpha=0.7
    )

ax.legend(markerscale=2)
ax.set_xlabel('X (pixels)')
ax.set_ylabel('Y (pixels)')
ax.set_title('Spatial Cell Type Distribution')
ax.axis('equal')
plt.tight_layout()
plt.show()
```

### Spatial Neighborhood Analysis

Analyze cell neighborhoods and interactions:

```python
import squidpy as sq

# Calculate spatial neighborhood enrichment
sq.gr.spatial_neighbors(adata, coord_type='generic', spatial_key='spatial')

# Neighborhood enrichment test
sq.gr.nhood_enrichment(adata, cluster_key='cell_type')

# Visualize interaction matrix
sq.pl.nhood_enrichment(adata, cluster_key='cell_type')

# Co-occurrence score
sq.gr.co_occurrence(adata, cluster_key='cell_type')
sq.pl.co_occurrence(
    adata,
    cluster_key='cell_type',
    clusters=['CD8 T cell', 'Tumor'],
    figsize=(8, 8)
)
```

### Spatial Autocorrelation

Test for spatial clustering of markers:

```python
# Moran's I spatial autocorrelation
sq.gr.spatial_autocorr(
    adata,
    mode='moran',
    genes=['CD3', 'CD8', 'PD1', 'PDL1', 'panCK']
)

# Visualize
results = adata.uns['moranI']
print(results.head())
```

## MERFISH Workflows

### Loading MERFISH Data

```python
from pathml.core import MERFISHSlide

# Load MERFISH dataset
merfish_slide = MERFISHSlide(
    path='path/to/merfish_data',
    fov_size=2048,  # Field of view size
    microns_per_pixel=0.108
)
```

### MERFISH Processing

```python
from pathml.preprocessing import Pipeline, DecodeMERFISH, SegmentMIF

merfish_pipeline = Pipeline([
    # 1. Decode barcodes to genes
    DecodeMERFISH(
        codebook='path/to/codebook.csv',
        error_correction=True,
        distance_threshold=0.5
    ),

    # 2. Cell segmentation
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='polyT',  # poly(T) stain for cell boundaries
        model='mesmer'
    ),

    # 3. Assign transcripts to cells
    AssignTranscripts(
        segmentation_mask_name='cell_segmentation',
        transcript_coords='decoded_spots'
    )
])

merfish_pipeline.run(merfish_slide)

# Output: AnnData with gene counts per cell
gene_expression = merfish_slide.cell_data
```

## Quality Control

### Segmentation Quality

```python
from pathml.utils import assess_segmentation_quality

# Check segmentation quality metrics
qc_metrics = assess_segmentation_quality(
    segmentation_mask,
    image,
    metrics=['cell_count', 'mean_cell_size', 'size_distribution']
)

print(f"Total cells: {qc_metrics['cell_count']}")
print(f"Mean cell size: {qc_metrics['mean_cell_size']:.1f} pixels")

# Visualize
import matplotlib.pyplot as plt
plt.hist(qc_metrics['cell_sizes'], bins=50)
plt.xlabel('Cell Size (pixels)')
plt.ylabel('Frequency')
plt.title('Cell Size Distribution')
plt.show()
```

### Marker Expression QC

```python
import scanpy as sc

# Load AnnData
adata = ad.read_h5ad('codex_dataset.h5ad')

# Calculate QC metrics
adata.obs['total_intensity'] = adata.X.sum(axis=1)
adata.obs['n_markers_detected'] = (adata.X > 0).sum(axis=1)

# Filter low-quality cells
adata = adata[adata.obs['total_intensity'] > 100, :]
adata = adata[adata.obs['n_markers_detected'] >= 3, :]

# Visualize
sc.pl.violin(adata, ['total_intensity', 'n_markers_detected'], multi_panel=True)
```

## Batch Processing

Process large multiparametric datasets efficiently:

```python
from pathml.core import SlideDataset
from pathml.preprocessing import Pipeline
from dask.distributed import Client
import glob

# Start Dask cluster
client = Client(n_workers=16, threads_per_worker=2, memory_limit='8GB')

# Find all CODEX slides
slide_dirs = glob.glob('data/codex_slides/*/')

# Create dataset
codex_slides = [CODEXSlide(d, stain='IF') for d in slide_dirs]
dataset = SlideDataset(codex_slides)

# Run pipeline in parallel
dataset.run(
    codex_pipeline,
    distributed=True,
    client=client,
    scheduler='distributed'
)

# Save processed data
for i, slide in enumerate(dataset):
    slide.cell_data.write(f'processed/slide_{i}.h5ad')

client.close()
```

## Integration with Other Tools

### Export to Spatial Analysis Tools

```python
# Export to Giotto
def export_to_giotto(adata, output_dir):
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Expression matrix
    pd.DataFrame(
        adata.X.T,
        index=adata.var_names,
        columns=adata.obs_names
    ).to_csv(f'{output_dir}/expression.csv')

    # Cell coordinates
    pd.DataFrame(
        adata.obsm['spatial'],
        columns=['x', 'y'],
        index=adata.obs_names
    ).to_csv(f'{output_dir}/spatial_locs.csv')

# Export to Seurat
def export_to_seurat(adata, output_file):
    adata.write_h5ad(output_file)
    # Read in R with: library(Seurat); ReadH5AD(output_file)
```

## Best Practices

1. **Channel selection for segmentation:**
   - Use brightest, most consistent nuclear marker (usually DAPI)
   - Choose membrane/cytoplasm marker based on tissue type
   - Test multiple options to optimize segmentation

2. **Background subtraction:**
   - Apply before quantification to reduce autofluorescence
   - Use blank/control images to model background

3. **Quality control:**
   - Visualize segmentation on sample regions
   - Check cell size distributions for outliers
   - Validate marker expression ranges

4. **Cell type annotation:**
   - Start with canonical markers (CD3, CD20, panCK)
   - Use multiple markers for robust classification
   - Consider unsupervised clustering to discover populations

5. **Spatial analysis:**
   - Account for tissue architecture (epithelium, stroma, etc.)
   - Consider local density when interpreting interactions
   - Use permutation tests for statistical significance

6. **Batch effects:**
   - Include batch information in AnnData.obs
   - Apply batch correction if combining multiple experiments
   - Visualize batch effects with UMAP colored by batch

## Common Issues and Solutions

**Issue: Poor segmentation quality**
- Verify nuclear and cytoplasm channels are correctly specified
- Adjust image_resolution parameter to match actual resolution
- Try different cytoplasm markers
- Manually tune min/max cell size parameters

**Issue: Low marker intensity**
- Check for background subtraction artifacts
- Verify channel names match actual channels
- Inspect raw images for technical issues (focus, exposure)

**Issue: Cell type annotations don't match expectations**
- Adjust marker thresholds (too high/low)
- Visualize marker distributions to set data-driven thresholds
- Check for antibody specificity issues

**Issue: Spatial analysis shows no significant interactions**
- Increase neighborhood radius
- Check for sufficient cell numbers per type
- Verify spatial coordinates are correctly scaled

## Additional Resources

- **PathML Multiparametric API:** https://pathml.readthedocs.io/en/latest/api_multiparametric_reference.html
- **CODEX:** https://www.akoyabio.com/codex/
- **Vectra:** https://www.akoyabio.com/vectra/
- **DeepCell Mesmer:** https://www.deepcell.org/
- **Scanpy:** https://scanpy.readthedocs.io/ (single-cell analysis)
- **Squidpy:** https://squidpy.readthedocs.io/ (spatial omics analysis)

---

## Reference: Preprocessing

# Preprocessing Pipelines & Transforms

## Overview

PathML provides a modular preprocessing architecture based on composable transforms organized into pipelines. Transforms are individual operations that modify images, create masks, or extract features. Pipelines chain transforms together to create reproducible, scalable preprocessing workflows for computational pathology.

## Pipeline Architecture

### Pipeline Class

The `Pipeline` class composes a sequence of transforms applied consecutively:

```python
from pathml.preprocessing import Pipeline, Transform1, Transform2

# Create pipeline
pipeline = Pipeline([
    Transform1(param1=value1),
    Transform2(param2=value2),
    # ... more transforms
])

# Run on a single slide
pipeline.run(slide_data)

# Run on a dataset
pipeline.run(dataset, distributed=True, n_workers=8)
```

**Key features:**
- Sequential execution of transforms
- Automatic handling of tiles and masks
- Distributed processing support with Dask
- Reproducible workflows with serializable configuration

### Transform Base Class

All transforms inherit from the `Transform` base class and implement:
- `apply()` - Core transformation logic
- `input_type` - Expected input (tile, mask, etc.)
- `output_type` - Produced output

## Transform Categories

PathML provides transforms in six major categories:

1. **Image Modification** - Blur, rescale, histogram equalization
2. **Mask Creation** - Tissue detection, nucleus detection, thresholding
3. **Mask Modification** - Morphological operations on masks
4. **Stain Processing** - H&E stain normalization and separation
5. **Quality Control** - Artifact detection, white space labeling
6. **Specialized** - Multiparametric imaging, cell segmentation

## Image Modification Transforms

### Blur Operations

Apply various blurring kernels for noise reduction:

**MedianBlur:**
```python
from pathml.preprocessing import MedianBlur

# Apply median filter
transform = MedianBlur(kernel_size=5)
```
- Effective for salt-and-pepper noise
- Preserves edges better than Gaussian blur

**GaussianBlur:**
```python
from pathml.preprocessing import GaussianBlur

# Apply Gaussian blur
transform = GaussianBlur(kernel_size=5, sigma=1.0)
```
- Smooth noise reduction
- Adjustable sigma controls blur strength

**BoxBlur:**
```python
from pathml.preprocessing import BoxBlur

# Apply box filter
transform = BoxBlur(kernel_size=5)
```
- Fastest blur operation
- Uniform averaging within kernel

### Intensity Adjustments

**RescaleIntensity:**
```python
from pathml.preprocessing import RescaleIntensity

# Rescale intensity to [0, 255]
transform = RescaleIntensity(
    in_range=(0, 1.0),
    out_range=(0, 255)
)
```

**HistogramEqualization:**
```python
from pathml.preprocessing import HistogramEqualization

# Global histogram equalization
transform = HistogramEqualization()
```
- Enhances global contrast
- Spreads out intensity distribution

**AdaptiveHistogramEqualization (CLAHE):**
```python
from pathml.preprocessing import AdaptiveHistogramEqualization

# Contrast Limited Adaptive Histogram Equalization
transform = AdaptiveHistogramEqualization(
    clip_limit=0.03,
    tile_grid_size=(8, 8)
)
```
- Enhances local contrast
- Prevents over-amplification with clip_limit
- Better for images with varying local contrast

### Superpixel Processing

**SuperpixelInterpolation:**
```python
from pathml.preprocessing import SuperpixelInterpolation

# Divide into superpixels using SLIC
transform = SuperpixelInterpolation(
    n_segments=100,
    compactness=10.0
)
```
- Segments image into perceptually meaningful regions
- Useful for feature extraction and segmentation

## Mask Creation Transforms

### H&E Tissue and Nucleus Detection

**TissueDetectionHE:**
```python
from pathml.preprocessing import TissueDetectionHE

# Detect tissue regions in H&E slides
transform = TissueDetectionHE(
    use_saturation=True,  # Use HSV saturation channel
    threshold=10,  # Intensity threshold
    min_region_size=500  # Minimum tissue region size in pixels
)
```
- Creates binary tissue mask
- Filters small regions and artifacts
- Stores mask in `tile.masks['tissue']`

**NucleusDetectionHE:**
```python
from pathml.preprocessing import NucleusDetectionHE

# Detect nuclei in H&E images
transform = NucleusDetectionHE(
    stain='hematoxylin',  # Use hematoxylin channel
    threshold=0.3,
    min_nucleus_size=10
)
```
- Separates hematoxylin stain
- Thresholds to create nucleus mask
- Stores mask in `tile.masks['nucleus']`

### Binary Thresholding

**BinaryThreshold:**
```python
from pathml.preprocessing import BinaryThreshold

# Threshold using Otsu's method
transform = BinaryThreshold(
    method='otsu',  # 'otsu' or manual threshold value
    invert=False
)

# Or specify manual threshold
transform = BinaryThreshold(threshold=128)
```

### Foreground Detection

**ForegroundDetection:**
```python
from pathml.preprocessing import ForegroundDetection

# Detect foreground regions
transform = ForegroundDetection(
    threshold=0.5,
    min_region_size=1000,  # Minimum size in pixels
    use_saturation=True
)
```

## Mask Modification Transforms

Apply morphological operations to clean up masks:

**MorphOpen:**
```python
from pathml.preprocessing import MorphOpen

# Remove small objects and noise
transform = MorphOpen(
    kernel_size=5,
    mask_name='tissue'  # Which mask to modify
)
```
- Erosion followed by dilation
- Removes small objects and noise

**MorphClose:**
```python
from pathml.preprocessing import MorphClose

# Fill small holes
transform = MorphClose(
    kernel_size=5,
    mask_name='tissue'
)
```
- Dilation followed by erosion
- Fills small holes in mask

## Stain Normalization

### StainNormalizationHE

Normalize H&E staining across slides to account for variations in staining procedure and scanners:

```python
from pathml.preprocessing import StainNormalizationHE

# Normalize to reference slide
transform = StainNormalizationHE(
    target='normalize',  # 'normalize', 'hematoxylin', or 'eosin'
    stain_estimation_method='macenko',  # 'macenko' or 'vahadane'
    tissue_mask_name=None  # Optional tissue mask for better estimation
)
```

**Target modes:**
- `'normalize'` - Normalize both stains to reference
- `'hematoxylin'` - Extract hematoxylin channel only
- `'eosin'` - Extract eosin channel only

**Stain estimation methods:**
- `'macenko'` - Macenko et al. 2009 method (faster, more stable)
- `'vahadane'` - Vahadane et al. 2016 method (more accurate, slower)

**Advanced parameters:**
```python
transform = StainNormalizationHE(
    target='normalize',
    stain_estimation_method='macenko',
    target_od=None,  # Optical density matrix for reference (optional)
    target_concentrations=None,  # Target stain concentrations (optional)
    regularizer=0.1,  # Regularization for vahadane method
    background_intensity=240  # Background intensity level
)
```

**Workflow:**
1. Convert RGB to optical density (OD)
2. Estimate stain matrix (H&E vectors)
3. Decompose into stain concentrations
4. Normalize to reference stain distribution
5. Reconstruct normalized RGB image

**Example with tissue mask:**
```python
from pathml.preprocessing import Pipeline, TissueDetectionHE, StainNormalizationHE

pipeline = Pipeline([
    TissueDetectionHE(),  # Create tissue mask first
    StainNormalizationHE(
        target='normalize',
        stain_estimation_method='macenko',
        tissue_mask_name='tissue'  # Use tissue mask for better estimation
    )
])
```

## Quality Control Transforms

### Artifact Detection

**LabelArtifactTileHE:**
```python
from pathml.preprocessing import LabelArtifactTileHE

# Label tiles containing artifacts
transform = LabelArtifactTileHE(
    pen_threshold=0.5,  # Threshold for pen marking detection
    bubble_threshold=0.5  # Threshold for bubble detection
)
```
- Detects pen markings, bubbles, and other artifacts
- Labels affected tiles for filtering

**LabelWhiteSpaceHE:**
```python
from pathml.preprocessing import LabelWhiteSpaceHE

# Label tiles with excessive white space
transform = LabelWhiteSpaceHE(
    threshold=0.9,  # Fraction of white pixels
    mask_name='white_space'
)
```
- Identifies tiles with mostly background
- Useful for filtering uninformative tiles

## Multiparametric Imaging Transforms

### Cell Segmentation

**SegmentMIF:**
```python
from pathml.preprocessing import SegmentMIF

# Segment cells using Mesmer deep learning model
transform = SegmentMIF(
    nuclear_channel='DAPI',  # Nuclear marker channel name
    cytoplasm_channel='CD45',  # Cytoplasm marker channel name
    model='mesmer',  # Deep learning segmentation model
    image_resolution=0.5,  # Microns per pixel
    compartment='whole-cell'  # 'nuclear', 'cytoplasm', or 'whole-cell'
)
```
- Uses DeepCell Mesmer model for cell segmentation
- Requires nuclear and cytoplasm channel specification
- Produces instance segmentation masks

**SegmentMIFRemote:**
```python
from pathml.preprocessing import SegmentMIFRemote

# Remote inference using DeepCell API
transform = SegmentMIFRemote(
    nuclear_channel='DAPI',
    cytoplasm_channel='CD45',
    model='mesmer',
    api_url='https://deepcell.org/api'
)
```
- Same functionality as SegmentMIF but uses remote API
- No local GPU required
- Suitable for batch processing

### Marker Quantification

**QuantifyMIF:**
```python
from pathml.preprocessing import QuantifyMIF

# Quantify marker expression per cell
transform = QuantifyMIF(
    segmentation_mask_name='cell_segmentation',
    markers=['CD3', 'CD4', 'CD8', 'CD20', 'CD45'],
    output_format='anndata'  # or 'dataframe'
)
```
- Extracts mean marker intensity per segmented cell
- Computes morphological features (area, perimeter, etc.)
- Outputs AnnData object for downstream single-cell analysis

### CODEX/Vectra Specific

**CollapseRunsCODEX:**
```python
from pathml.preprocessing import CollapseRunsCODEX

# Consolidate multi-run CODEX data
transform = CollapseRunsCODEX(
    z_slice=2,  # Select specific z-slice
    run_order=[0, 1, 2]  # Order of acquisition runs
)
```
- Merges channels from multiple CODEX acquisition runs
- Selects focal plane from z-stacks

**CollapseRunsVectra:**
```python
from pathml.preprocessing import CollapseRunsVectra

# Process Vectra multiplex IF data
transform = CollapseRunsVectra(
    wavelengths=[520, 570, 620, 670, 780]  # Emission wavelengths
)
```

## Building Comprehensive Pipelines

### Basic H&E Preprocessing Pipeline

```python
from pathml.preprocessing import (
    Pipeline,
    TissueDetectionHE,
    StainNormalizationHE,
    NucleusDetectionHE,
    MedianBlur,
    LabelWhiteSpaceHE
)

pipeline = Pipeline([
    # 1. Quality control
    LabelWhiteSpaceHE(threshold=0.9),

    # 2. Noise reduction
    MedianBlur(kernel_size=3),

    # 3. Tissue detection
    TissueDetectionHE(min_region_size=500),

    # 4. Stain normalization
    StainNormalizationHE(
        target='normalize',
        stain_estimation_method='macenko',
        tissue_mask_name='tissue'
    ),

    # 5. Nucleus detection
    NucleusDetectionHE(threshold=0.3)
])
```

### CODEX Multiparametric Pipeline

```python
from pathml.preprocessing import (
    Pipeline,
    CollapseRunsCODEX,
    SegmentMIF,
    QuantifyMIF
)

codex_pipeline = Pipeline([
    # 1. Consolidate multi-run data
    CollapseRunsCODEX(z_slice=2),

    # 2. Cell segmentation
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer',
        image_resolution=0.377
    ),

    # 3. Quantify markers
    QuantifyMIF(
        segmentation_mask_name='cell_segmentation',
        markers=['CD3', 'CD4', 'CD8', 'CD20', 'PD1', 'PDL1'],
        output_format='anndata'
    )
])
```

### Advanced Pipeline with Quality Control

```python
from pathml.preprocessing import (
    Pipeline,
    LabelWhiteSpaceHE,
    LabelArtifactTileHE,
    TissueDetectionHE,
    MorphOpen,
    MorphClose,
    StainNormalizationHE,
    AdaptiveHistogramEqualization
)

advanced_pipeline = Pipeline([
    # Stage 1: Quality control
    LabelWhiteSpaceHE(threshold=0.85),
    LabelArtifactTileHE(pen_threshold=0.5, bubble_threshold=0.5),

    # Stage 2: Tissue detection
    TissueDetectionHE(threshold=10, min_region_size=1000),
    MorphOpen(kernel_size=5, mask_name='tissue'),
    MorphClose(kernel_size=7, mask_name='tissue'),

    # Stage 3: Stain normalization
    StainNormalizationHE(
        target='normalize',
        stain_estimation_method='vahadane',
        tissue_mask_name='tissue'
    ),

    # Stage 4: Contrast enhancement
    AdaptiveHistogramEqualization(clip_limit=0.03, tile_grid_size=(8, 8))
])
```

## Running Pipelines

### Single Slide Processing

```python
from pathml.core import SlideData

# Load slide
wsi = SlideData.from_slide("slide.svs")

# Generate tiles
wsi.generate_tiles(level=1, tile_size=256, stride=256)

# Run pipeline
pipeline.run(wsi)

# Access processed data
for tile in wsi.tiles:
    normalized_image = tile.image
    tissue_mask = tile.masks.get('tissue')
    nucleus_mask = tile.masks.get('nucleus')
```

### Batch Processing with Distributed Execution

```python
from pathml.core import SlideDataset
from dask.distributed import Client
import glob

# Start Dask client
client = Client(n_workers=8, threads_per_worker=2, memory_limit='4GB')

# Create dataset
slide_paths = glob.glob("data/*.svs")
dataset = SlideDataset(
    slide_paths,
    tile_size=512,
    stride=512,
    level=1
)

# Run pipeline in parallel
dataset.run(
    pipeline,
    distributed=True,
    client=client
)

# Save results
dataset.to_hdf5("processed_dataset.h5")

client.close()
```

### Conditional Pipeline Execution

Execute transforms only on tiles meeting specific criteria:

```python
# Filter tiles before processing
wsi.generate_tiles(level=1, tile_size=256)

# Run pipeline only on tissue tiles
for tile in wsi.tiles:
    if tile.masks.get('tissue') is not None:
        pipeline.run(tile)
```

## Performance Optimization

### Memory Management

```python
# Process large datasets in batches
batch_size = 100
for i in range(0, len(slide_paths), batch_size):
    batch_paths = slide_paths[i:i+batch_size]
    batch_dataset = SlideDataset(batch_paths)
    batch_dataset.run(pipeline, distributed=True)
    batch_dataset.to_hdf5(f"batch_{i}.h5")
```

### GPU Acceleration

Certain transforms leverage GPU acceleration when available:

```python
import torch

# Check GPU availability
print(f"CUDA available: {torch.cuda.is_available()}")

# Transforms that benefit from GPU:
# - SegmentMIF (Mesmer deep learning model)
# - StainNormalizationHE (matrix operations)
```

### Parallel Workers Configuration

```python
from dask.distributed import Client

# CPU-bound tasks (image processing)
client = Client(
    n_workers=8,
    threads_per_worker=1,  # Use processes, not threads
    memory_limit='8GB'
)

# GPU tasks (deep learning inference)
client = Client(
    n_workers=2,  # Fewer workers for GPU
    threads_per_worker=4,
    processes=True
)
```

## Custom Transforms

Create custom preprocessing operations by subclassing `Transform`:

```python
from pathml.preprocessing.transforms import Transform
import numpy as np

class CustomTransform(Transform):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def apply(self, tile):
        # Access tile image
        image = tile.image

        # Apply custom operation
        processed = self.custom_operation(image, self.param1, self.param2)

        # Update tile
        tile.image = processed

        return tile

    def custom_operation(self, image, param1, param2):
        # Implement custom logic
        return processed_image

# Use in pipeline
pipeline = Pipeline([
    CustomTransform(param1=10, param2=0.5),
    # ... other transforms
])
```

## Best Practices

1. **Order transforms appropriately:**
   - Quality control first (LabelWhiteSpace, LabelArtifact)
   - Noise reduction early (Blur)
   - Tissue detection before stain normalization
   - Stain normalization before color-dependent operations

2. **Use tissue masks for stain normalization:**
   - Improves accuracy by excluding background
   - `TissueDetectionHE()` then `StainNormalizationHE(tissue_mask_name='tissue')`

3. **Apply morphological operations to clean masks:**
   - `MorphOpen` to remove small false positives
   - `MorphClose` to fill small gaps

4. **Leverage distributed processing for large datasets:**
   - Use Dask for parallel execution
   - Configure workers based on available resources

5. **Save intermediate results:**
   - Store processed data to HDF5 for reuse
   - Avoid reprocessing computationally expensive transforms

6. **Validate preprocessing on sample images:**
   - Visualize intermediate steps
   - Tune parameters on representative samples before batch processing

7. **Handle edge cases:**
   - Check for empty masks before downstream operations
   - Validate tile quality before expensive computations

## Common Issues and Solutions

**Issue: Stain normalization produces artifacts**
- Use tissue mask to exclude background
- Try different stain estimation method (macenko vs. vahadane)
- Verify optical density parameters match your images

**Issue: Out of memory during pipeline execution**
- Reduce number of Dask workers
- Decrease tile size
- Process images at lower pyramid level
- Enable memory_limit parameter in Dask client

**Issue: Tissue detection misses tissue regions**
- Adjust threshold parameter
- Use saturation channel: `use_saturation=True`
- Reduce min_region_size to capture smaller tissue fragments

**Issue: Nucleus detection is inaccurate**
- Verify stain separation quality (visualize hematoxylin channel)
- Adjust threshold parameter
- Apply stain normalization before nucleus detection

## Additional Resources

- **PathML Preprocessing API:** https://pathml.readthedocs.io/en/latest/api_preprocessing_reference.html
- **Stain Normalization Methods:**
  - Macenko et al. 2009: "A method for normalizing histology slides for quantitative analysis"
  - Vahadane et al. 2016: "Structure-Preserving Color Normalization and Sparse Stain Separation"
- **DeepCell Mesmer:** https://www.deepcell.org/ (cell segmentation model)
