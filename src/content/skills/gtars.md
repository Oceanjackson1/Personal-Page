---
title: "Gtars"
description: "High-performance toolkit for genomic interval analysis in Rust with Python bindings. Use when working with genomic regions, BED files, coverage tracks, overlap detection, tokenization for ML models, or fragment analysis in computational genomics a..."
category: "research"
source: "community"
author: "Community"
tags: ["gtars"]
date: 2026-03-20
---

# Gtars: Genomic Tools and Algorithms in Rust

## Overview

Gtars is a high-performance Rust toolkit for manipulating, analyzing, and processing genomic interval data. It provides specialized tools for overlap detection, coverage analysis, tokenization for machine learning, and reference sequence management.

Use this skill when working with:
- Genomic interval files (BED format)
- Overlap detection between genomic regions
- Coverage track generation (WIG, BigWig)
- Genomic ML preprocessing and tokenization
- Fragment analysis in single-cell genomics
- Reference sequence retrieval and validation

## Installation

### Python Installation

Install gtars Python bindings:

```bash
uv uv pip install gtars
```

### CLI Installation

Install command-line tools (requires Rust/Cargo):

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Or install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust Library

Add to Cargo.toml for Rust projects:

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## Core Capabilities

Gtars is organized into specialized modules, each focused on specific genomic analysis tasks:

### 1. Overlap Detection and IGD Indexing

Efficiently detect overlaps between genomic intervals using the Integrated Genome Database (IGD) data structure.

**When to use:**
- Finding overlapping regulatory elements
- Variant annotation
- Comparing ChIP-seq peaks
- Identifying shared genomic features

**Quick example:**
```python
import gtars

# Build IGD index and query overlaps
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

See `references/overlap.md` for comprehensive overlap detection documentation.

### 2. Coverage Track Generation

Generate coverage tracks from sequencing data with the uniwig module.

**When to use:**
- ATAC-seq accessibility profiles
- ChIP-seq coverage visualization
- RNA-seq read coverage
- Differential coverage analysis

**Quick example:**
```bash
# Generate BigWig coverage track
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

See `references/coverage.md` for detailed coverage analysis workflows.

### 3. Genomic Tokenization

Convert genomic regions into discrete tokens for machine learning applications, particularly for deep learning models on genomic data.

**When to use:**
- Preprocessing for genomic ML models
- Integration with geniml library
- Creating position encodings
- Training transformer models on genomic sequences

**Quick example:**
```python
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

See `references/tokenizers.md` for tokenization documentation.

### 4. Reference Sequence Management

Handle reference genome sequences and compute digests following the GA4GH refget protocol.

**When to use:**
- Validating reference genome integrity
- Extracting specific genomic sequences
- Computing sequence digests
- Cross-reference comparisons

**Quick example:**
```python
# Load reference and extract sequences
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

See `references/refget.md` for reference sequence operations.

### 5. Fragment Processing

Split and analyze fragment files, particularly useful for single-cell genomics data.

**When to use:**
- Processing single-cell ATAC-seq data
- Splitting fragments by cell barcodes
- Cluster-based fragment analysis
- Fragment quality control

**Quick example:**
```bash
# Split fragments by clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

See `references/cli.md` for fragment processing commands.

### 6. Fragment Scoring

Score fragment overlaps against reference datasets.

**When to use:**
- Evaluating fragment enrichment
- Comparing experimental data to references
- Quality metrics computation
- Batch scoring across samples

**Quick example:**
```bash
# Score fragments against reference
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## Common Workflows

### Workflow 1: Peak Overlap Analysis

Identify overlapping genomic features:

```python
import gtars

# Load two region sets
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# Find overlaps
overlapping_peaks = peaks.filter_overlapping(promoters)

# Export results
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### Workflow 2: Coverage Track Pipeline

Generate coverage tracks for visualization:

```bash
# Step 1: Generate coverage
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# Step 2: Convert to BigWig for genome browsers
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### Workflow 3: ML Preprocessing

Prepare genomic data for machine learning:

```python
from gtars.tokenizers import TreeTokenizer
import gtars

# Step 1: Load training regions
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# Step 2: Create tokenizer
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# Step 3: Tokenize regions
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# Step 4: Use tokens in ML pipeline
# (integrate with geniml or custom models)
```

## Python vs CLI Usage

**Use Python API when:**
- Integrating with analysis pipelines
- Need programmatic control
- Working with NumPy/Pandas
- Building custom workflows

**Use CLI when:**
- Quick one-off analyses
- Shell scripting
- Batch processing files
- Prototyping workflows

## Reference Documentation

Comprehensive module documentation:

- **`references/python-api.md`** - Complete Python API reference with RegionSet operations, NumPy integration, and data export
- **`references/overlap.md`** - IGD indexing, overlap detection, and set operations
- **`references/coverage.md`** - Coverage track generation with uniwig
- **`references/tokenizers.md`** - Genomic tokenization for ML applications
- **`references/refget.md`** - Reference sequence management and digests
- **`references/cli.md`** - Command-line interface complete reference

## Integration with geniml

Gtars serves as the foundation for the geniml Python package, providing core genomic interval operations for machine learning workflows. When working on geniml-related tasks, use gtars for data preprocessing and tokenization.

## Performance Characteristics

- **Native Rust performance**: Fast execution with low memory overhead
- **Parallel processing**: Multi-threaded operations for large datasets
- **Memory efficiency**: Streaming and memory-mapped file support
- **Zero-copy operations**: NumPy integration with minimal data copying

## Data Formats

Gtars works with standard genomic formats:

- **BED**: Genomic intervals (3-column or extended)
- **WIG/BigWig**: Coverage tracks
- **FASTA**: Reference sequences
- **Fragment TSV**: Single-cell fragment files with barcodes

## Error Handling and Debugging

Enable verbose logging for troubleshooting:

```python
import gtars

# Enable debug logging
gtars.set_log_level("DEBUG")
```

```bash
# CLI verbose mode
gtars --verbose <command>
```

---

## Reference: Cli

# Command-Line Interface

Gtars provides a comprehensive CLI for genomic interval analysis directly from the terminal.

## Installation

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

## Global Options

```bash
# Display help
gtars --help

# Show version
gtars --version

# Verbose output
gtars --verbose <command>

# Quiet mode
gtars --quiet <command>
```

## IGD Commands

Build and query IGD indexes for overlap detection:

```bash
# Build IGD index
gtars igd build --input regions.bed --output regions.igd

# Query single region
gtars igd query --index regions.igd --region "chr1:1000-2000"

# Query from file
gtars igd query --index regions.igd --query-file queries.bed --output results.bed

# Count overlaps
gtars igd count --index regions.igd --query-file queries.bed
```

## Overlap Commands

Compute overlaps between genomic region sets:

```bash
# Find overlapping regions
gtars overlaprs overlap --set-a regions_a.bed --set-b regions_b.bed --output overlaps.bed

# Count overlaps
gtars overlaprs count --set-a regions_a.bed --set-b regions_b.bed

# Filter regions by overlap
gtars overlaprs filter --input regions.bed --filter overlapping.bed --output filtered.bed

# Subtract regions
gtars overlaprs subtract --set-a regions_a.bed --set-b regions_b.bed --output difference.bed
```

## Uniwig Commands

Generate coverage tracks from genomic intervals:

```bash
# Generate coverage track
gtars uniwig generate --input fragments.bed --output coverage.wig

# Specify resolution
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Generate BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig

# Strand-specific coverage
gtars uniwig generate --input fragments.bed --output forward.wig --strand +
```

## BBCache Commands

Cache and manage BED files from BEDbase.org:

```bash
# Cache BED file from bedbase
gtars bbcache fetch --id <bedbase_id> --output cached.bed

# List cached files
gtars bbcache list

# Clear cache
gtars bbcache clear

# Update cache
gtars bbcache update
```

## Scoring Commands

Score fragment overlaps against reference datasets:

```bash
# Score fragments
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt

# Batch scoring
gtars scoring batch --fragments-dir ./fragments/ --reference reference.bed --output-dir ./scores/

# Score with weights
gtars scoring score --fragments fragments.bed --reference reference.bed --weights weights.txt --output scores.txt
```

## FragSplit Commands

Split fragment files by cell barcodes or clusters:

```bash
# Split by barcode
gtars fragsplit split --input fragments.tsv --barcodes barcodes.txt --output-dir ./split/

# Split by clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./clustered/

# Filter fragments
gtars fragsplit filter --input fragments.tsv --min-fragments 100 --output filtered.tsv
```

## Common Workflows

### Workflow 1: Overlap Analysis Pipeline

```bash
# Step 1: Build IGD index for reference
gtars igd build --input reference_regions.bed --output reference.igd

# Step 2: Query with experimental data
gtars igd query --index reference.igd --query-file experimental.bed --output overlaps.bed

# Step 3: Generate statistics
gtars overlaprs count --set-a experimental.bed --set-b reference_regions.bed
```

### Workflow 2: Coverage Track Generation

```bash
# Step 1: Generate coverage
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Step 2: Convert to BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

### Workflow 3: Fragment Processing

```bash
# Step 1: Filter fragments
gtars fragsplit filter --input raw_fragments.tsv --min-fragments 100 --output filtered.tsv

# Step 2: Split by clusters
gtars fragsplit cluster-split --input filtered.tsv --clusters clusters.txt --output-dir ./by_cluster/

# Step 3: Score against reference
gtars scoring batch --fragments-dir ./by_cluster/ --reference reference.bed --output-dir ./scores/
```

## Input/Output Formats

### BED Format
Standard 3-column or extended BED format:
```
chr1    1000    2000
chr1    3000    4000
chr2    5000    6000
```

### Fragment Format (TSV)
Tab-separated format for single-cell fragments:
```
chr1    1000    2000    BARCODE1
chr1    3000    4000    BARCODE2
chr2    5000    6000    BARCODE1
```

### WIG Format
Wiggle format for coverage tracks:
```
fixedStep chrom=chr1 start=1000 step=10
12
15
18
```

## Performance Options

```bash
# Set thread count
gtars --threads 8 <command>

# Memory limit
gtars --memory-limit 4G <command>

# Buffer size
gtars --buffer-size 10000 <command>
```

## Error Handling

```bash
# Continue on errors
gtars --continue-on-error <command>

# Strict mode (fail on warnings)
gtars --strict <command>

# Log to file
gtars --log-file output.log <command>
```

---

## Reference: Coverage

# Coverage Analysis with Uniwig

The uniwig module generates coverage tracks from sequencing data, providing efficient conversion of genomic intervals to coverage profiles.

## Coverage Track Generation

Create coverage tracks from BED files:

```python
import gtars

# Generate coverage from BED file
coverage = gtars.uniwig.coverage_from_bed("fragments.bed")

# Generate coverage with specific resolution
coverage = gtars.uniwig.coverage_from_bed("fragments.bed", resolution=10)

# Generate strand-specific coverage
fwd_coverage = gtars.uniwig.coverage_from_bed("fragments.bed", strand="+")
rev_coverage = gtars.uniwig.coverage_from_bed("fragments.bed", strand="-")
```

## CLI Usage

Generate coverage tracks from command line:

```bash
# Generate coverage track
gtars uniwig generate --input fragments.bed --output coverage.wig

# Specify resolution
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Generate BigWig format
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig

# Strand-specific coverage
gtars uniwig generate --input fragments.bed --output forward.wig --strand +
gtars uniwig generate --input fragments.bed --output reverse.wig --strand -
```

## Working with Coverage Data

### Accessing Coverage Values

Query coverage at specific positions:

```python
# Get coverage at position
cov = coverage.get_coverage("chr1", 1000)

# Get coverage over range
cov_array = coverage.get_coverage_range("chr1", 1000, 2000)

# Get coverage statistics
mean_cov = coverage.mean_coverage("chr1", 1000, 2000)
max_cov = coverage.max_coverage("chr1", 1000, 2000)
```

### Coverage Operations

Perform operations on coverage tracks:

```python
# Normalize coverage
normalized = coverage.normalize()

# Smooth coverage
smoothed = coverage.smooth(window_size=10)

# Combine coverage tracks
combined = coverage1.add(coverage2)

# Compute coverage difference
diff = coverage1.subtract(coverage2)
```

## Output Formats

Uniwig supports multiple output formats:

### WIG Format

Standard wiggle format:
```
fixedStep chrom=chr1 start=1000 step=1
12
15
18
22
...
```

### BigWig Format

Binary format for efficient storage and access:
```bash
# Generate BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

### BedGraph Format

Flexible format for variable coverage:
```
chr1    1000    1001    12
chr1    1001    1002    15
chr1    1002    1003    18
```

## Use Cases

### ATAC-seq Analysis

Generate chromatin accessibility profiles:

```python
# Generate ATAC-seq coverage
atac_fragments = gtars.RegionSet.from_bed("atac_fragments.bed")
coverage = gtars.uniwig.coverage_from_bed("atac_fragments.bed", resolution=1)

# Identify accessible regions
peaks = coverage.call_peaks(threshold=10)
```

### ChIP-seq Peak Visualization

Create coverage tracks for ChIP-seq data:

```bash
# Generate coverage for visualization
gtars uniwig generate --input chip_seq_fragments.bed \
                      --output chip_coverage.bw \
                      --format bigwig
```

### RNA-seq Coverage

Compute read coverage for RNA-seq:

```python
# Generate strand-specific RNA-seq coverage
fwd = gtars.uniwig.coverage_from_bed("rnaseq.bed", strand="+")
rev = gtars.uniwig.coverage_from_bed("rnaseq.bed", strand="-")

# Export for IGV
fwd.to_bigwig("rnaseq_fwd.bw")
rev.to_bigwig("rnaseq_rev.bw")
```

### Differential Coverage Analysis

Compare coverage between samples:

```python
# Generate coverage for two samples
control = gtars.uniwig.coverage_from_bed("control.bed")
treatment = gtars.uniwig.coverage_from_bed("treatment.bed")

# Compute fold change
fold_change = treatment.divide(control)

# Find differential regions
diff_regions = fold_change.find_regions(threshold=2.0)
```

## Performance Optimization

- Use appropriate resolution for data scale
- BigWig format recommended for large datasets
- Parallel processing available for multiple chromosomes
- Memory-efficient streaming for large files

---

## Reference: Overlap

# Overlap Detection and IGD

The overlaprs module provides efficient overlap detection between genomic intervals using the Integrated Genome Database (IGD) data structure.

## IGD Index

IGD (Integrated Genome Database) is a specialized data structure for fast genomic interval queries and overlap detection.

### Building an IGD Index

Create indexes from genomic region files:

```python
import gtars

# Build IGD index from BED file
igd = gtars.igd.build_index("regions.bed")

# Save index for reuse
igd.save("regions.igd")

# Load existing index
igd = gtars.igd.load_index("regions.igd")
```

### Querying Overlaps

Find overlapping regions efficiently:

```python
# Query a single region
overlaps = igd.query("chr1", 1000, 2000)

# Query multiple regions
results = []
for chrom, start, end in query_regions:
    overlaps = igd.query(chrom, start, end)
    results.append(overlaps)

# Get overlap counts only
count = igd.count_overlaps("chr1", 1000, 2000)
```

## CLI Usage

The overlaprs command-line tool provides overlap detection:

```bash
# Find overlaps between two BED files
gtars overlaprs query --index regions.bed --query query_regions.bed

# Count overlaps
gtars overlaprs count --index regions.bed --query query_regions.bed

# Output overlapping regions
gtars overlaprs overlap --index regions.bed --query query_regions.bed --output overlaps.bed
```

### IGD CLI Commands

Build and query IGD indexes:

```bash
# Build IGD index
gtars igd build --input regions.bed --output regions.igd

# Query IGD index
gtars igd query --index regions.igd --region "chr1:1000-2000"

# Batch query from file
gtars igd query --index regions.igd --query-file queries.bed --output results.bed
```

## Python API

### Overlap Detection

Compute overlaps between region sets:

```python
import gtars

# Load two region sets
set_a = gtars.RegionSet.from_bed("regions_a.bed")
set_b = gtars.RegionSet.from_bed("regions_b.bed")

# Find overlaps
overlaps = set_a.overlap(set_b)

# Get regions from A that overlap with B
overlapping_a = set_a.filter_overlapping(set_b)

# Get regions from A that don't overlap with B
non_overlapping_a = set_a.filter_non_overlapping(set_b)
```

### Overlap Statistics

Calculate overlap metrics:

```python
# Count overlaps
overlap_count = set_a.count_overlaps(set_b)

# Calculate overlap fraction
overlap_fraction = set_a.overlap_fraction(set_b)

# Get overlap coverage
coverage = set_a.overlap_coverage(set_b)
```

## Performance Characteristics

IGD provides efficient querying:
- **Index construction**: O(n log n) where n is number of regions
- **Query time**: O(k + log n) where k is number of overlaps
- **Memory efficient**: Compact representation of genomic intervals

## Use Cases

### Regulatory Element Analysis

Identify overlap between genomic features:

```python
# Find transcription factor binding sites overlapping promoters
tfbs = gtars.RegionSet.from_bed("chip_seq_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

overlapping_tfbs = tfbs.filter_overlapping(promoters)
print(f"Found {len(overlapping_tfbs)} TFBS in promoters")
```

### Variant Annotation

Annotate variants with overlapping features:

```python
# Check which variants overlap with coding regions
variants = gtars.RegionSet.from_bed("variants.bed")
cds = gtars.RegionSet.from_bed("coding_sequences.bed")

coding_variants = variants.filter_overlapping(cds)
```

### Chromatin State Analysis

Compare chromatin states across samples:

```python
# Find regions with consistent chromatin states
sample1 = gtars.RegionSet.from_bed("sample1_peaks.bed")
sample2 = gtars.RegionSet.from_bed("sample2_peaks.bed")

consistent_regions = sample1.overlap(sample2)
```

---

## Reference: Python Api

# Python API Reference

Comprehensive reference for gtars Python bindings.

## Installation

```bash
# Install gtars Python package
uv pip install gtars

# Or with pip
pip install gtars
```

## Core Classes

### RegionSet

Manage collections of genomic intervals:

```python
import gtars

# Create from BED file
regions = gtars.RegionSet.from_bed("regions.bed")

# Create from coordinates
regions = gtars.RegionSet([
    ("chr1", 1000, 2000),
    ("chr1", 3000, 4000),
    ("chr2", 5000, 6000)
])

# Access regions
for region in regions:
    print(f"{region.chromosome}:{region.start}-{region.end}")

# Get region count
num_regions = len(regions)

# Get total coverage
total_coverage = regions.total_coverage()
```

### Region Operations

Perform operations on region sets:

```python
# Sort regions
sorted_regions = regions.sort()

# Merge overlapping regions
merged = regions.merge()

# Filter by size
large_regions = regions.filter_by_size(min_size=1000)

# Filter by chromosome
chr1_regions = regions.filter_by_chromosome("chr1")
```

### Set Operations

Perform set operations on genomic regions:

```python
# Load two region sets
set_a = gtars.RegionSet.from_bed("set_a.bed")
set_b = gtars.RegionSet.from_bed("set_b.bed")

# Union
union = set_a.union(set_b)

# Intersection
intersection = set_a.intersect(set_b)

# Difference
difference = set_a.subtract(set_b)

# Symmetric difference
sym_diff = set_a.symmetric_difference(set_b)
```

## Data Export

### Writing BED Files

Export regions to BED format:

```python
# Write to BED file
regions.to_bed("output.bed")

# Write with scores
regions.to_bed("output.bed", scores=score_array)

# Write with names
regions.to_bed("output.bed", names=name_list)
```

### Format Conversion

Convert between formats:

```python
# BED to JSON
regions = gtars.RegionSet.from_bed("input.bed")
regions.to_json("output.json")

# JSON to BED
regions = gtars.RegionSet.from_json("input.json")
regions.to_bed("output.bed")
```

## NumPy Integration

Seamless integration with NumPy arrays:

```python
import numpy as np

# Export to NumPy arrays
starts = regions.starts_array()  # NumPy array of start positions
ends = regions.ends_array()      # NumPy array of end positions
sizes = regions.sizes_array()    # NumPy array of region sizes

# Create from NumPy arrays
chromosomes = ["chr1"] * len(starts)
regions = gtars.RegionSet.from_arrays(chromosomes, starts, ends)
```

## Parallel Processing

Leverage parallel processing for large datasets:

```python
# Enable parallel processing
regions = gtars.RegionSet.from_bed("large_file.bed", parallel=True)

# Parallel operations
result = regions.parallel_apply(custom_function)
```

## Memory Management

Efficient memory usage for large datasets:

```python
# Stream large BED files
for chunk in gtars.RegionSet.stream_bed("large_file.bed", chunk_size=10000):
    process_chunk(chunk)

# Memory-mapped mode
regions = gtars.RegionSet.from_bed("large_file.bed", mmap=True)
```

## Error Handling

Handle common errors:

```python
try:
    regions = gtars.RegionSet.from_bed("file.bed")
except gtars.FileNotFoundError:
    print("File not found")
except gtars.InvalidFormatError as e:
    print(f"Invalid BED format: {e}")
except gtars.ParseError as e:
    print(f"Parse error at line {e.line}: {e.message}")
```

## Configuration

Configure gtars behavior:

```python
# Set global options
gtars.set_option("parallel.threads", 4)
gtars.set_option("memory.limit", "4GB")
gtars.set_option("warnings.strict", True)

# Context manager for temporary options
with gtars.option_context("parallel.threads", 8):
    # Use 8 threads for this block
    regions = gtars.RegionSet.from_bed("large_file.bed", parallel=True)
```

## Logging

Enable logging for debugging:

```python
import logging

# Enable gtars logging
gtars.set_log_level("DEBUG")

# Or use Python logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("gtars")
```

## Performance Tips

- Use parallel processing for large datasets
- Enable memory-mapped mode for very large files
- Stream data when possible to reduce memory usage
- Pre-sort regions before operations when applicable
- Use NumPy arrays for numerical computations
- Cache frequently accessed data

---

## Reference: Refget

# Reference Sequence Management

The refget module handles reference sequence retrieval and digest computation, following the refget protocol for sequence identification.

## RefgetStore

RefgetStore manages reference sequences and their digests:

```python
import gtars

# Create RefgetStore
store = gtars.RefgetStore()

# Add sequence
store.add_sequence("chr1", sequence_data)

# Retrieve sequence
seq = store.get_sequence("chr1")

# Get sequence digest
digest = store.get_digest("chr1")
```

## Sequence Digests

Compute and verify sequence digests:

```python
# Compute digest for sequence
from gtars.refget import compute_digest

digest = compute_digest(sequence_data)

# Verify digest matches
is_valid = store.verify_digest("chr1", expected_digest)
```

## Integration with Reference Genomes

Work with standard reference genomes:

```python
# Load reference genome
store = gtars.RefgetStore.from_fasta("hg38.fa")

# Get chromosome sequences
chr1 = store.get_sequence("chr1")
chr2 = store.get_sequence("chr2")

# Get subsequence
region_seq = store.get_subsequence("chr1", 1000, 2000)
```

## CLI Usage

Manage reference sequences from command line:

```bash
# Compute digest for FASTA file
gtars refget digest --input genome.fa --output digests.txt

# Verify sequence digest
gtars refget verify --sequence sequence.fa --digest expected_digest
```

## Refget Protocol Compliance

The refget module follows the GA4GH refget protocol:

### Digest Computation

Digests are computed using SHA-512 truncated to 48 bytes:

```python
# Compute refget-compliant digest
digest = gtars.refget.compute_digest(sequence)
# Returns: "SQ.abc123..."
```

### Sequence Retrieval

Retrieve sequences by digest:

```python
# Get sequence by refget digest
seq = store.get_sequence_by_digest("SQ.abc123...")
```

## Use Cases

### Reference Validation

Verify reference genome integrity:

```python
# Compute digests for reference
store = gtars.RefgetStore.from_fasta("reference.fa")
digests = {chrom: store.get_digest(chrom) for chrom in store.chromosomes}

# Compare with expected digests
for chrom, expected in expected_digests.items():
    actual = digests[chrom]
    if actual != expected:
        print(f"Mismatch for {chrom}: {actual} != {expected}")
```

### Sequence Extraction

Extract specific genomic regions:

```python
# Extract regions of interest
store = gtars.RefgetStore.from_fasta("hg38.fa")

regions = [
    ("chr1", 1000, 2000),
    ("chr2", 5000, 6000),
    ("chr3", 10000, 11000)
]

sequences = [store.get_subsequence(c, s, e) for c, s, e in regions]
```

### Cross-Reference Comparison

Compare sequences across different references:

```python
# Load two reference versions
hg19 = gtars.RefgetStore.from_fasta("hg19.fa")
hg38 = gtars.RefgetStore.from_fasta("hg38.fa")

# Compare digests
for chrom in hg19.chromosomes:
    digest_19 = hg19.get_digest(chrom)
    digest_38 = hg38.get_digest(chrom)
    if digest_19 != digest_38:
        print(f"{chrom} differs between hg19 and hg38")
```

## Performance Notes

- Sequences loaded on demand
- Digests cached after computation
- Efficient subsequence extraction
- Memory-mapped file support for large genomes

---

## Reference: Tokenizers

# Genomic Tokenizers

Tokenizers convert genomic regions into discrete tokens for machine learning applications, particularly useful for training genomic deep learning models.

## Python API

### Creating a Tokenizer

Load tokenizer configurations from various sources:

```python
import gtars

# From BED file
tokenizer = gtars.tokenizers.TreeTokenizer.from_bed_file("regions.bed")

# From configuration file
tokenizer = gtars.tokenizers.TreeTokenizer.from_config("tokenizer_config.yaml")

# From region string
tokenizer = gtars.tokenizers.TreeTokenizer.from_region_string("chr1:1000-2000")
```

### Tokenizing Genomic Regions

Convert genomic coordinates to tokens:

```python
# Tokenize a single region
token = tokenizer.tokenize("chr1", 1000, 2000)

# Tokenize multiple regions
tokens = []
for chrom, start, end in regions:
    token = tokenizer.tokenize(chrom, start, end)
    tokens.append(token)
```

### Token Properties

Access token information:

```python
# Get token ID
token_id = token.id

# Get genomic coordinates
chrom = token.chromosome
start = token.start
end = token.end

# Get token metadata
metadata = token.metadata
```

## Use Cases

### Machine Learning Preprocessing

Tokenizers are essential for preparing genomic data for ML models:

1. **Sequence modeling**: Convert genomic intervals into discrete tokens for transformer models
2. **Position encoding**: Create consistent positional encodings across datasets
3. **Data augmentation**: Generate alternative tokenizations for training

### Integration with geniml

The tokenizers module integrates seamlessly with the geniml library for genomic ML:

```python
# Tokenize regions for geniml
from gtars.tokenizers import TreeTokenizer
import geniml

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
tokens = [tokenizer.tokenize(r.chrom, r.start, r.end) for r in regions]

# Use tokens in geniml models
model = geniml.Model(vocab_size=tokenizer.vocab_size)
```

## Configuration Format

Tokenizer configuration files support YAML format:

```yaml
# tokenizer_config.yaml
type: tree
resolution: 1000  # Token resolution in base pairs
chromosomes:
  - chr1
  - chr2
  - chr3
options:
  overlap_handling: merge
  gap_threshold: 100
```

## Performance Considerations

- TreeTokenizer uses efficient data structures for fast tokenization
- Batch tokenization is recommended for large datasets
- Pre-loading tokenizers reduces overhead for repeated operations
