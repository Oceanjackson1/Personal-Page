---
title: "Pysam"
description: "Genomic file toolkit. Read/write SAM/BAM/CRAM alignments, VCF/BCF variants, FASTA/FASTQ sequences, extract regions, calculate coverage, for NGS data processing pipelines."
category: "devops"
source: "community"
author: "Community"
tags: ["pysam"]
date: 2026-03-20
---

# Pysam

## Overview

Pysam is a Python module for reading, manipulating, and writing genomic datasets. Read/write SAM/BAM/CRAM alignment files, VCF/BCF variant files, and FASTA/FASTQ sequences with a Pythonic interface to htslib. Query tabix-indexed files, perform pileup analysis for coverage, and execute samtools/bcftools commands.

## When to Use This Skill

This skill should be used when:
- Working with sequencing alignment files (BAM/CRAM)
- Analyzing genetic variants (VCF/BCF)
- Extracting reference sequences or gene regions
- Processing raw sequencing data (FASTQ)
- Calculating coverage or read depth
- Implementing bioinformatics analysis pipelines
- Quality control of sequencing data
- Variant calling and annotation workflows

## Quick Start

### Installation
```bash
uv pip install pysam
```

### Basic Examples

**Read alignment file:**
```python
import pysam

# Open BAM file and fetch reads in region
samfile = pysam.AlignmentFile("example.bam", "rb")
for read in samfile.fetch("chr1", 1000, 2000):
    print(f"{read.query_name}: {read.reference_start}")
samfile.close()
```

**Read variant file:**
```python
# Open VCF file and iterate variants
vcf = pysam.VariantFile("variants.vcf")
for variant in vcf:
    print(f"{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}")
vcf.close()
```

**Query reference sequence:**
```python
# Open FASTA and extract sequence
fasta = pysam.FastaFile("reference.fasta")
sequence = fasta.fetch("chr1", 1000, 2000)
print(sequence)
fasta.close()
```

## Core Capabilities

### 1. Alignment File Operations (SAM/BAM/CRAM)

Use the `AlignmentFile` class to work with aligned sequencing reads. This is appropriate for analyzing mapping results, calculating coverage, extracting reads, or quality control.

**Common operations:**
- Open and read BAM/SAM/CRAM files
- Fetch reads from specific genomic regions
- Filter reads by mapping quality, flags, or other criteria
- Write filtered or modified alignments
- Calculate coverage statistics
- Perform pileup analysis (base-by-base coverage)
- Access read sequences, quality scores, and alignment information

**Reference:** See `references/alignment_files.md` for detailed documentation on:
- Opening and reading alignment files
- AlignedSegment attributes and methods
- Region-based fetching with `fetch()`
- Pileup analysis for coverage
- Writing and creating BAM files
- Coordinate systems and indexing
- Performance optimization tips

### 2. Variant File Operations (VCF/BCF)

Use the `VariantFile` class to work with genetic variants from variant calling pipelines. This is appropriate for variant analysis, filtering, annotation, or population genetics.

**Common operations:**
- Read and write VCF/BCF files
- Query variants in specific regions
- Access variant information (position, alleles, quality)
- Extract genotype data for samples
- Filter variants by quality, allele frequency, or other criteria
- Annotate variants with additional information
- Subset samples or regions

**Reference:** See `references/variant_files.md` for detailed documentation on:
- Opening and reading variant files
- VariantRecord attributes and methods
- Accessing INFO and FORMAT fields
- Working with genotypes and samples
- Creating and writing VCF files
- Filtering and subsetting variants
- Multi-sample VCF operations

### 3. Sequence File Operations (FASTA/FASTQ)

Use `FastaFile` for random access to reference sequences and `FastxFile` for reading raw sequencing data. This is appropriate for extracting gene sequences, validating variants against reference, or processing raw reads.

**Common operations:**
- Query reference sequences by genomic coordinates
- Extract sequences for genes or regions of interest
- Read FASTQ files with quality scores
- Validate variant reference alleles
- Calculate sequence statistics
- Filter reads by quality or length
- Convert between FASTA and FASTQ formats

**Reference:** See `references/sequence_files.md` for detailed documentation on:
- FASTA file access and indexing
- Extracting sequences by region
- Handling reverse complement for genes
- Reading FASTQ files sequentially
- Quality score conversion and filtering
- Working with tabix-indexed files (BED, GTF, GFF)
- Common sequence processing patterns

### 4. Integrated Bioinformatics Workflows

Pysam excels at integrating multiple file types for comprehensive genomic analyses. Common workflows combine alignment files, variant files, and reference sequences.

**Common workflows:**
- Calculate coverage statistics for specific regions
- Validate variants against aligned reads
- Annotate variants with coverage information
- Extract sequences around variant positions
- Filter alignments or variants based on multiple criteria
- Generate coverage tracks for visualization
- Quality control across multiple data types

**Reference:** See `references/common_workflows.md` for detailed examples of:
- Quality control workflows (BAM statistics, reference consistency)
- Coverage analysis (per-base coverage, low coverage detection)
- Variant analysis (annotation, filtering by read support)
- Sequence extraction (variant contexts, gene sequences)
- Read filtering and subsetting
- Integration patterns (BAM+VCF, VCF+BED, etc.)
- Performance optimization for complex workflows

## Key Concepts

### Coordinate Systems

**Critical:** Pysam uses **0-based, half-open** coordinates (Python convention):
- Start positions are 0-based (first base is position 0)
- End positions are exclusive (not included in the range)
- Region 1000-2000 includes bases 1000-1999 (1000 bases total)

**Exception:** Region strings in `fetch()` follow samtools convention (1-based):
```python
samfile.fetch("chr1", 999, 2000)      # 0-based: positions 999-1999
samfile.fetch("chr1:1000-2000")       # 1-based string: positions 1000-2000
```

**VCF files:** Use 1-based coordinates in the file format, but `VariantRecord.start` is 0-based.

### Indexing Requirements

Random access to specific genomic regions requires index files:
- **BAM files**: Require `.bai` index (create with `pysam.index()`)
- **CRAM files**: Require `.crai` index
- **FASTA files**: Require `.fai` index (create with `pysam.faidx()`)
- **VCF.gz files**: Require `.tbi` tabix index (create with `pysam.tabix_index()`)
- **BCF files**: Require `.csi` index

Without an index, use `fetch(until_eof=True)` for sequential reading.

### File Modes

Specify format when opening files:
- `"rb"` - Read BAM (binary)
- `"r"` - Read SAM (text)
- `"rc"` - Read CRAM
- `"wb"` - Write BAM
- `"w"` - Write SAM
- `"wc"` - Write CRAM

### Performance Considerations

1. **Always use indexed files** for random access operations
2. **Use `pileup()` for column-wise analysis** instead of repeated fetch operations
3. **Use `count()` for counting** instead of iterating and counting manually
4. **Process regions in parallel** when analyzing independent genomic regions
5. **Close files explicitly** to free resources
6. **Use `until_eof=True`** for sequential processing without index
7. **Avoid multiple iterators** unless necessary (use `multiple_iterators=True` if needed)

## Common Pitfalls

1. **Coordinate confusion:** Remember 0-based vs 1-based systems in different contexts
2. **Missing indices:** Many operations require index files—create them first
3. **Partial overlaps:** `fetch()` returns reads overlapping region boundaries, not just those fully contained
4. **Iterator scope:** Keep pileup iterator references alive to avoid "PileupProxy accessed after iterator finished" errors
5. **Quality score editing:** Cannot modify `query_qualities` in place after changing `query_sequence`—create a copy first
6. **Stream limitations:** Only stdin/stdout are supported for streaming, not arbitrary Python file objects
7. **Thread safety:** While GIL is released during I/O, comprehensive thread-safety hasn't been fully validated

## Command-Line Tools

Pysam provides access to samtools and bcftools commands:

```python
# Sort BAM file
pysam.samtools.sort("-o", "sorted.bam", "input.bam")

# Index BAM
pysam.samtools.index("sorted.bam")

# View specific region
pysam.samtools.view("-b", "-o", "region.bam", "input.bam", "chr1:1000-2000")

# BCF tools
pysam.bcftools.view("-O", "z", "-o", "output.vcf.gz", "input.vcf")
```

**Error handling:**
```python
try:
    pysam.samtools.sort("-o", "output.bam", "input.bam")
except pysam.SamtoolsError as e:
    print(f"Error: {e}")
```

## Resources

### references/

Detailed documentation for each major capability:

- **alignment_files.md** - Complete guide to SAM/BAM/CRAM operations, including AlignmentFile class, AlignedSegment attributes, fetch operations, pileup analysis, and writing alignments

- **variant_files.md** - Complete guide to VCF/BCF operations, including VariantFile class, VariantRecord attributes, genotype handling, INFO/FORMAT fields, and multi-sample operations

- **sequence_files.md** - Complete guide to FASTA/FASTQ operations, including FastaFile and FastxFile classes, sequence extraction, quality score handling, and tabix-indexed file access

- **common_workflows.md** - Practical examples of integrated bioinformatics workflows combining multiple file types, including quality control, coverage analysis, variant validation, and sequence extraction

## Getting Help

For detailed information on specific operations, refer to the appropriate reference document:

- Working with BAM files or calculating coverage → `alignment_files.md`
- Analyzing variants or genotypes → `variant_files.md`
- Extracting sequences or processing FASTQ → `sequence_files.md`
- Complex workflows integrating multiple file types → `common_workflows.md`

Official documentation: https://pysam.readthedocs.io/

---

## Reference: Alignment_Files

# Working with Alignment Files (SAM/BAM/CRAM)

## Overview

Pysam provides the `AlignmentFile` class for reading and writing SAM/BAM/CRAM formatted files containing aligned sequence data. BAM/CRAM files support compression and random access through indexing.

## Opening Alignment Files

Specify format via mode qualifier:
- `"rb"` - Read BAM (binary)
- `"r"` - Read SAM (text)
- `"rc"` - Read CRAM (compressed)
- `"wb"` - Write BAM
- `"w"` - Write SAM
- `"wc"` - Write CRAM

```python
import pysam

# Reading
samfile = pysam.AlignmentFile("example.bam", "rb")

# Writing (requires template or header)
outfile = pysam.AlignmentFile("output.bam", "wb", template=samfile)
```

### Stream Processing

Use `"-"` as filename for stdin/stdout operations:

```python
# Read from stdin
infile = pysam.AlignmentFile('-', 'rb')

# Write to stdout
outfile = pysam.AlignmentFile('-', 'w', template=infile)
```

**Important:** Pysam does not support reading/writing from true Python file objects—only stdin/stdout streams are supported.

## AlignmentFile Properties

**Header Information:**
- `references` - List of chromosome/contig names
- `lengths` - Corresponding lengths for each reference
- `header` - Complete header as dictionary

```python
samfile = pysam.AlignmentFile("example.bam", "rb")
print(f"References: {samfile.references}")
print(f"Lengths: {samfile.lengths}")
```

## Reading Reads

### fetch() - Region-Based Retrieval

Retrieves reads overlapping specified genomic regions using **0-based coordinates**.

```python
# Fetch specific region
for read in samfile.fetch("chr1", 1000, 2000):
    print(read.query_name, read.reference_start)

# Fetch entire contig
for read in samfile.fetch("chr1"):
    print(read.query_name)

# Fetch without index (sequential read)
for read in samfile.fetch(until_eof=True):
    print(read.query_name)
```

**Important Notes:**
- Requires index (.bai/.crai) for random access
- Returns reads that **overlap** the region (may extend beyond boundaries)
- Use `until_eof=True` for non-indexed files or sequential reading
- By default, only returns mapped reads
- For unmapped reads, use `fetch("*")` or `until_eof=True`

### Multiple Iterators

When using multiple iterators on the same file:

```python
samfile = pysam.AlignmentFile("example.bam", "rb", multiple_iterators=True)
iter1 = samfile.fetch("chr1", 1000, 2000)
iter2 = samfile.fetch("chr2", 5000, 6000)
```

Without `multiple_iterators=True`, a new fetch() call repositions the file pointer and breaks existing iterators.

### count() - Count Reads in Region

```python
# Count all reads
num_reads = samfile.count("chr1", 1000, 2000)

# Count with quality filter
num_quality_reads = samfile.count("chr1", 1000, 2000, quality=20)
```

### count_coverage() - Per-Base Coverage

Returns four arrays (A, C, G, T) with per-base coverage:

```python
coverage = samfile.count_coverage("chr1", 1000, 2000)
a_counts, c_counts, g_counts, t_counts = coverage
```

## AlignedSegment Objects

Each read is represented as an `AlignedSegment` object with these key attributes:

### Read Information
- `query_name` - Read name/ID
- `query_sequence` - Read sequence (bases)
- `query_qualities` - Base quality scores (ASCII-encoded)
- `query_length` - Length of the read

### Mapping Information
- `reference_name` - Chromosome/contig name
- `reference_start` - Start position (0-based, inclusive)
- `reference_end` - End position (0-based, exclusive)
- `mapping_quality` - MAPQ score
- `cigarstring` - CIGAR string (e.g., "100M")
- `cigartuples` - CIGAR as list of (operation, length) tuples

**Important:** `cigartuples` format differs from SAM specification. Operations are integers:
- 0 = M (match/mismatch)
- 1 = I (insertion)
- 2 = D (deletion)
- 3 = N (skipped reference)
- 4 = S (soft clipping)
- 5 = H (hard clipping)
- 6 = P (padding)
- 7 = = (sequence match)
- 8 = X (sequence mismatch)

### Flags and Status
- `flag` - SAM flag as integer
- `is_paired` - Is read paired?
- `is_proper_pair` - Is read in a proper pair?
- `is_unmapped` - Is read unmapped?
- `mate_is_unmapped` - Is mate unmapped?
- `is_reverse` - Is read on reverse strand?
- `mate_is_reverse` - Is mate on reverse strand?
- `is_read1` - Is this read1?
- `is_read2` - Is this read2?
- `is_secondary` - Is secondary alignment?
- `is_qcfail` - Did read fail QC?
- `is_duplicate` - Is read a duplicate?
- `is_supplementary` - Is supplementary alignment?

### Tags and Optional Fields
- `get_tag(tag)` - Get value of optional field
- `set_tag(tag, value)` - Set optional field
- `has_tag(tag)` - Check if tag exists
- `get_tags()` - Get all tags as list of tuples

```python
for read in samfile.fetch("chr1", 1000, 2000):
    if read.has_tag("NM"):
        edit_distance = read.get_tag("NM")
        print(f"{read.query_name}: NM={edit_distance}")
```

## Writing Alignment Files

### Creating Header

```python
header = {
    'HD': {'VN': '1.0'},
    'SQ': [
        {'LN': 1575, 'SN': 'chr1'},
        {'LN': 1584, 'SN': 'chr2'}
    ]
}

outfile = pysam.AlignmentFile("output.bam", "wb", header=header)
```

### Creating AlignedSegment Objects

```python
# Create new read
a = pysam.AlignedSegment()
a.query_name = "read001"
a.query_sequence = "AGCTTAGCTAGCTACCTATATCTTGGTCTTGGCCG"
a.flag = 0
a.reference_id = 0  # Index into header['SQ']
a.reference_start = 100
a.mapping_quality = 20
a.cigar = [(0, 35)]  # 35M
a.query_qualities = pysam.qualitystring_to_array("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

# Write to file
outfile.write(a)
```

### Converting Between Formats

```python
# BAM to SAM
infile = pysam.AlignmentFile("input.bam", "rb")
outfile = pysam.AlignmentFile("output.sam", "w", template=infile)
for read in infile:
    outfile.write(read)
infile.close()
outfile.close()
```

## Pileup Analysis

The `pileup()` method provides **column-wise** (position-by-position) analysis across a region:

```python
for pileupcolumn in samfile.pileup("chr1", 1000, 2000):
    print(f"Position {pileupcolumn.pos}: coverage = {pileupcolumn.nsegments}")

    for pileupread in pileupcolumn.pileups:
        if not pileupread.is_del and not pileupread.is_refskip:
            # Query position is the position in the read
            base = pileupread.alignment.query_sequence[pileupread.query_position]
            print(f"  {pileupread.alignment.query_name}: {base}")
```

**Key attributes:**
- `pileupcolumn.pos` - 0-based reference position
- `pileupcolumn.nsegments` - Number of reads covering position
- `pileupread.alignment` - The AlignedSegment object
- `pileupread.query_position` - Position in the read (None for deletions)
- `pileupread.is_del` - Is this a deletion?
- `pileupread.is_refskip` - Is this a reference skip (N in CIGAR)?

**Important:** Keep iterator references alive. The error "PileupProxy accessed after iterator finished" occurs when iterators go out of scope prematurely.

## Coordinate System

**Critical:** Pysam uses **0-based, half-open** coordinates (Python convention):
- `reference_start` is 0-based (first base is 0)
- `reference_end` is exclusive (not included in range)
- Region from 1000-2000 includes bases 1000-1999

**Exception:** Region strings in `fetch()` and `pileup()` follow samtools conventions (1-based):
```python
# These are equivalent:
samfile.fetch("chr1", 999, 2000)  # Python style: 0-based
samfile.fetch("chr1:1000-2000")   # samtools style: 1-based
```

## Indexing

Create BAM index:
```python
pysam.index("example.bam")
```

Or use command-line interface:
```python
pysam.samtools.index("example.bam")
```

## Performance Tips

1. **Use indexed access** when querying specific regions repeatedly
2. **Use `pileup()` for column-wise analysis** instead of repeated fetch operations
3. **Use `fetch(until_eof=True)` for sequential reading** of non-indexed files
4. **Avoid multiple iterators** unless necessary (performance cost)
5. **Use `count()` for simple counting** instead of iterating and counting manually

## Common Pitfalls

1. **Partial overlaps:** `fetch()` returns reads that overlap region boundaries—implement explicit filtering if exact boundaries are needed
2. **Quality score editing:** Cannot edit `query_qualities` in place after modifying `query_sequence`. Create a copy first: `quals = read.query_qualities`
3. **Missing index:** `fetch()` without `until_eof=True` requires an index file
4. **Thread safety:** While pysam releases GIL during I/O, comprehensive thread-safety hasn't been fully validated
5. **Iterator scope:** Keep pileup iterator references alive to avoid "PileupProxy accessed after iterator finished" errors

---

## Reference: Common_Workflows

# Common Bioinformatics Workflows with Pysam

## Overview

This document provides practical examples of common bioinformatics workflows using pysam, demonstrating how to combine different file types and operations.

## Quality Control Workflows

### Calculate BAM Statistics

```python
import pysam

def calculate_bam_stats(bam_file):
    """Calculate basic statistics for BAM file."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    stats = {
        "total_reads": 0,
        "mapped_reads": 0,
        "unmapped_reads": 0,
        "paired_reads": 0,
        "proper_pairs": 0,
        "duplicates": 0,
        "total_bases": 0,
        "mapped_bases": 0
    }

    for read in samfile.fetch(until_eof=True):
        stats["total_reads"] += 1

        if read.is_unmapped:
            stats["unmapped_reads"] += 1
        else:
            stats["mapped_reads"] += 1
            stats["mapped_bases"] += read.query_alignment_length

        if read.is_paired:
            stats["paired_reads"] += 1
            if read.is_proper_pair:
                stats["proper_pairs"] += 1

        if read.is_duplicate:
            stats["duplicates"] += 1

        stats["total_bases"] += read.query_length

    samfile.close()

    # Calculate derived statistics
    stats["mapping_rate"] = stats["mapped_reads"] / stats["total_reads"] if stats["total_reads"] > 0 else 0
    stats["duplication_rate"] = stats["duplicates"] / stats["total_reads"] if stats["total_reads"] > 0 else 0

    return stats
```

### Check Reference Consistency

```python
def check_bam_reference_consistency(bam_file, fasta_file):
    """Verify that BAM reads match reference genome."""
    samfile = pysam.AlignmentFile(bam_file, "rb")
    fasta = pysam.FastaFile(fasta_file)

    mismatches = 0
    total_checked = 0

    for read in samfile.fetch():
        if read.is_unmapped:
            continue

        # Get reference sequence for aligned region
        ref_seq = fasta.fetch(
            read.reference_name,
            read.reference_start,
            read.reference_end
        )

        # Get read sequence aligned to reference
        aligned_pairs = read.get_aligned_pairs(with_seq=True)

        for query_pos, ref_pos, ref_base in aligned_pairs:
            if query_pos is not None and ref_pos is not None and ref_base is not None:
                read_base = read.query_sequence[query_pos]
                if read_base.upper() != ref_base.upper():
                    mismatches += 1
                total_checked += 1

        if total_checked >= 10000:  # Sample first 10k positions
            break

    samfile.close()
    fasta.close()

    error_rate = mismatches / total_checked if total_checked > 0 else 0
    return {
        "positions_checked": total_checked,
        "mismatches": mismatches,
        "error_rate": error_rate
    }
```

## Coverage Analysis

### Calculate Per-Base Coverage

```python
def calculate_coverage(bam_file, chrom, start, end):
    """Calculate coverage for each position in region."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    # Initialize coverage array
    length = end - start
    coverage = [0] * length

    # Count coverage at each position
    for pileupcolumn in samfile.pileup(chrom, start, end):
        if start <= pileupcolumn.pos < end:
            coverage[pileupcolumn.pos - start] = pileupcolumn.nsegments

    samfile.close()

    return coverage
```

### Identify Low Coverage Regions

```python
def find_low_coverage_regions(bam_file, chrom, start, end, min_coverage=10):
    """Find regions with coverage below threshold."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    low_coverage_regions = []
    in_low_region = False
    region_start = None

    for pileupcolumn in samfile.pileup(chrom, start, end):
        pos = pileupcolumn.pos
        if pos < start or pos >= end:
            continue

        coverage = pileupcolumn.nsegments

        if coverage < min_coverage:
            if not in_low_region:
                region_start = pos
                in_low_region = True
        else:
            if in_low_region:
                low_coverage_regions.append((region_start, pos))
                in_low_region = False

    # Close last region if still open
    if in_low_region:
        low_coverage_regions.append((region_start, end))

    samfile.close()

    return low_coverage_regions
```

### Calculate Coverage Statistics

```python
def coverage_statistics(bam_file, chrom, start, end):
    """Calculate coverage statistics for region."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    coverages = []

    for pileupcolumn in samfile.pileup(chrom, start, end):
        if start <= pileupcolumn.pos < end:
            coverages.append(pileupcolumn.nsegments)

    samfile.close()

    if not coverages:
        return None

    coverages.sort()
    n = len(coverages)

    return {
        "mean": sum(coverages) / n,
        "median": coverages[n // 2],
        "min": coverages[0],
        "max": coverages[-1],
        "positions": n
    }
```

## Variant Analysis

### Extract Variants in Regions

```python
def extract_variants_in_genes(vcf_file, bed_file):
    """Extract variants overlapping gene regions."""
    vcf = pysam.VariantFile(vcf_file)
    bed = pysam.TabixFile(bed_file)

    variants_by_gene = {}

    for gene in bed.fetch(parser=pysam.asBed()):
        gene_name = gene.name
        variants_by_gene[gene_name] = []

        # Find variants in gene region
        for variant in vcf.fetch(gene.contig, gene.start, gene.end):
            variant_info = {
                "chrom": variant.chrom,
                "pos": variant.pos,
                "ref": variant.ref,
                "alt": variant.alts,
                "qual": variant.qual
            }
            variants_by_gene[gene_name].append(variant_info)

    vcf.close()
    bed.close()

    return variants_by_gene
```

### Annotate Variants with Coverage

```python
def annotate_variants_with_coverage(vcf_file, bam_file, output_file):
    """Add coverage information to variants."""
    vcf = pysam.VariantFile(vcf_file)
    samfile = pysam.AlignmentFile(bam_file, "rb")

    # Add DP to header if not present
    if "DP" not in vcf.header.info:
        vcf.header.info.add("DP", "1", "Integer", "Total Depth from BAM")

    outvcf = pysam.VariantFile(output_file, "w", header=vcf.header)

    for variant in vcf:
        # Get coverage at variant position
        coverage = samfile.count(
            variant.chrom,
            variant.pos - 1,  # Convert to 0-based
            variant.pos
        )

        # Add to INFO field
        variant.info["DP"] = coverage

        outvcf.write(variant)

    vcf.close()
    samfile.close()
    outvcf.close()
```

### Filter Variants by Read Support

```python
def filter_variants_by_support(vcf_file, bam_file, output_file, min_alt_reads=3):
    """Filter variants requiring minimum alternate allele support."""
    vcf = pysam.VariantFile(vcf_file)
    samfile = pysam.AlignmentFile(bam_file, "rb")
    outvcf = pysam.VariantFile(output_file, "w", header=vcf.header)

    for variant in vcf:
        # Count reads supporting each allele
        allele_counts = {variant.ref: 0}
        for alt in variant.alts:
            allele_counts[alt] = 0

        # Pileup at variant position
        for pileupcolumn in samfile.pileup(
            variant.chrom,
            variant.pos - 1,
            variant.pos
        ):
            if pileupcolumn.pos == variant.pos - 1:  # 0-based
                for pileupread in pileupcolumn.pileups:
                    if not pileupread.is_del and not pileupread.is_refskip:
                        base = pileupread.alignment.query_sequence[
                            pileupread.query_position
                        ]
                        if base in allele_counts:
                            allele_counts[base] += 1

        # Check if any alt allele has sufficient support
        has_support = any(
            allele_counts.get(alt, 0) >= min_alt_reads
            for alt in variant.alts
        )

        if has_support:
            outvcf.write(variant)

    vcf.close()
    samfile.close()
    outvcf.close()
```

## Sequence Extraction

### Extract Sequences Around Variants

```python
def extract_variant_contexts(vcf_file, fasta_file, output_file, window=50):
    """Extract reference sequences around variants."""
    vcf = pysam.VariantFile(vcf_file)
    fasta = pysam.FastaFile(fasta_file)

    with open(output_file, 'w') as out:
        for variant in vcf:
            # Get sequence context
            start = max(0, variant.pos - window - 1)  # Convert to 0-based
            end = variant.pos + window

            context = fasta.fetch(variant.chrom, start, end)

            # Mark variant position
            var_pos_in_context = variant.pos - 1 - start

            out.write(f">{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}\n")
            out.write(context[:var_pos_in_context].lower())
            out.write(context[var_pos_in_context:var_pos_in_context+len(variant.ref)].upper())
            out.write(context[var_pos_in_context+len(variant.ref):].lower())
            out.write("\n")

    vcf.close()
    fasta.close()
```

### Extract Gene Sequences

```python
def extract_gene_sequences(bed_file, fasta_file, output_fasta):
    """Extract sequences for genes from BED file."""
    bed = pysam.TabixFile(bed_file)
    fasta = pysam.FastaFile(fasta_file)

    with open(output_fasta, 'w') as out:
        for gene in bed.fetch(parser=pysam.asBed()):
            sequence = fasta.fetch(gene.contig, gene.start, gene.end)

            # Handle strand
            if hasattr(gene, 'strand') and gene.strand == '-':
                # Reverse complement
                complement = str.maketrans("ATGCatgcNn", "TACGtacgNn")
                sequence = sequence.translate(complement)[::-1]

            out.write(f">{gene.name} {gene.contig}:{gene.start}-{gene.end}\n")

            # Write sequence in 60-character lines
            for i in range(0, len(sequence), 60):
                out.write(sequence[i:i+60] + "\n")

    bed.close()
    fasta.close()
```

## Read Filtering and Subsetting

### Filter BAM by Region and Quality

```python
def filter_bam(input_bam, output_bam, chrom, start, end, min_mapq=20):
    """Filter BAM file by region and mapping quality."""
    infile = pysam.AlignmentFile(input_bam, "rb")
    outfile = pysam.AlignmentFile(output_bam, "wb", template=infile)

    for read in infile.fetch(chrom, start, end):
        if read.mapping_quality >= min_mapq and not read.is_duplicate:
            outfile.write(read)

    infile.close()
    outfile.close()

    # Create index
    pysam.index(output_bam)
```

### Extract Reads for Specific Variants

```python
def extract_reads_at_variants(bam_file, vcf_file, output_bam, window=100):
    """Extract reads overlapping variant positions."""
    samfile = pysam.AlignmentFile(bam_file, "rb")
    vcf = pysam.VariantFile(vcf_file)
    outfile = pysam.AlignmentFile(output_bam, "wb", template=samfile)

    # Collect all reads (using set to avoid duplicates)
    reads_to_keep = set()

    for variant in vcf:
        start = max(0, variant.pos - window - 1)
        end = variant.pos + window

        for read in samfile.fetch(variant.chrom, start, end):
            reads_to_keep.add(read.query_name)

    # Write all reads
    samfile.close()
    samfile = pysam.AlignmentFile(bam_file, "rb")

    for read in samfile.fetch(until_eof=True):
        if read.query_name in reads_to_keep:
            outfile.write(read)

    samfile.close()
    vcf.close()
    outfile.close()

    pysam.index(output_bam)
```

## Integration Workflows

### Create Coverage Track from BAM

```python
def create_coverage_bedgraph(bam_file, output_file, chrom=None):
    """Create bedGraph coverage track from BAM."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    chroms = [chrom] if chrom else samfile.references

    with open(output_file, 'w') as out:
        out.write("track type=bedGraph name=\"Coverage\"\n")

        for chrom in chroms:
            current_cov = None
            region_start = None

            for pileupcolumn in samfile.pileup(chrom):
                pos = pileupcolumn.pos
                cov = pileupcolumn.nsegments

                if cov != current_cov:
                    # Write previous region
                    if current_cov is not None:
                        out.write(f"{chrom}\t{region_start}\t{pos}\t{current_cov}\n")

                    # Start new region
                    current_cov = cov
                    region_start = pos

            # Write final region
            if current_cov is not None:
                out.write(f"{chrom}\t{region_start}\t{pos+1}\t{current_cov}\n")

    samfile.close()
```

### Merge Multiple VCF Files

```python
def merge_vcf_samples(vcf_files, output_file):
    """Merge multiple single-sample VCFs."""
    # Open all input files
    vcf_readers = [pysam.VariantFile(f) for f in vcf_files]

    # Create merged header
    merged_header = vcf_readers[0].header.copy()
    for vcf in vcf_readers[1:]:
        for sample in vcf.header.samples:
            merged_header.samples.add(sample)

    outvcf = pysam.VariantFile(output_file, "w", header=merged_header)

    # Get all variant positions
    all_variants = {}
    for vcf in vcf_readers:
        for variant in vcf:
            key = (variant.chrom, variant.pos, variant.ref, variant.alts)
            if key not in all_variants:
                all_variants[key] = []
            all_variants[key].append(variant)

    # Write merged variants
    for key, variants in sorted(all_variants.items()):
        # Create merged record from first variant
        merged = outvcf.new_record(
            contig=variants[0].chrom,
            start=variants[0].start,
            stop=variants[0].stop,
            alleles=variants[0].alleles
        )

        # Add genotypes from all samples
        for variant in variants:
            for sample in variant.samples:
                merged.samples[sample].update(variant.samples[sample])

        outvcf.write(merged)

    # Close all files
    for vcf in vcf_readers:
        vcf.close()
    outvcf.close()
```

## Performance Tips for Workflows

1. **Use indexed files** for all random access operations
2. **Process regions in parallel** when analyzing multiple independent regions
3. **Stream data when possible** - avoid loading entire files into memory
4. **Close files explicitly** to free resources
5. **Use `until_eof=True`** for sequential processing of entire files
6. **Batch operations** on the same file to minimize I/O
7. **Consider memory usage** with pileup operations on high-coverage regions
8. **Use count() instead of pileup()** when only counts are needed

## Common Integration Patterns

1. **BAM + Reference**: Verify alignments, extract aligned sequences
2. **BAM + VCF**: Validate variants, calculate allele frequencies
3. **VCF + BED**: Annotate variants with gene/region information
4. **BAM + BED**: Calculate coverage statistics for specific regions
5. **FASTA + VCF**: Extract variant context sequences
6. **Multiple BAMs**: Compare coverage or variants across samples
7. **BAM + FASTQ**: Extract unaligned reads for re-alignment

---

## Reference: Sequence_Files

# Working with Sequence Files (FASTA/FASTQ)

## FASTA Files

### Overview

Pysam provides the `FastaFile` class for indexed, random access to FASTA reference sequences. FASTA files must be indexed with `samtools faidx` before use.

### Opening FASTA Files

```python
import pysam

# Open indexed FASTA file
fasta = pysam.FastaFile("reference.fasta")

# Automatically looks for reference.fasta.fai index
```

### Creating FASTA Index

```python
# Create index using pysam
pysam.faidx("reference.fasta")

# Or using samtools command
pysam.samtools.faidx("reference.fasta")
```

This creates a `.fai` index file required for random access.

### FastaFile Properties

```python
fasta = pysam.FastaFile("reference.fasta")

# List of reference sequences
references = fasta.references
print(f"References: {references}")

# Get lengths
lengths = fasta.lengths
print(f"Lengths: {lengths}")

# Get specific sequence length
chr1_length = fasta.get_reference_length("chr1")
```

### Fetching Sequences

#### Fetch by Region

Uses **0-based, half-open** coordinates:

```python
# Fetch specific region
sequence = fasta.fetch("chr1", 1000, 2000)
print(f"Sequence: {sequence}")  # Returns 1000 bases

# Fetch entire chromosome
chr1_seq = fasta.fetch("chr1")

# Fetch using region string (1-based)
sequence = fasta.fetch(region="chr1:1001-2000")
```

**Important:** Numeric arguments use 0-based coordinates, region strings use 1-based coordinates (samtools convention).

#### Common Use Cases

```python
# Get sequence at variant position
def get_variant_context(fasta, chrom, pos, window=10):
    """Get sequence context around a variant position (1-based)."""
    start = max(0, pos - window - 1)  # Convert to 0-based
    end = pos + window
    return fasta.fetch(chrom, start, end)

# Get sequence for gene coordinates
def get_gene_sequence(fasta, chrom, start, end, strand):
    """Get gene sequence with strand awareness."""
    seq = fasta.fetch(chrom, start, end)

    if strand == "-":
        # Reverse complement
        complement = str.maketrans("ATGCatgc", "TACGtacg")
        seq = seq.translate(complement)[::-1]

    return seq

# Check reference allele
def check_ref_allele(fasta, chrom, pos, expected_ref):
    """Verify reference allele at position (1-based pos)."""
    actual = fasta.fetch(chrom, pos-1, pos)  # Convert to 0-based
    return actual.upper() == expected_ref.upper()
```

### Extracting Multiple Regions

```python
# Extract multiple regions efficiently
regions = [
    ("chr1", 1000, 2000),
    ("chr1", 5000, 6000),
    ("chr2", 10000, 11000)
]

sequences = {}
for chrom, start, end in regions:
    seq_id = f"{chrom}:{start}-{end}"
    sequences[seq_id] = fasta.fetch(chrom, start, end)
```

### Working with Ambiguous Bases

FASTA files may contain IUPAC ambiguity codes:

- N = any base
- R = A or G (purine)
- Y = C or T (pyrimidine)
- S = G or C (strong)
- W = A or T (weak)
- K = G or T (keto)
- M = A or C (amino)
- B = C, G, or T (not A)
- D = A, G, or T (not C)
- H = A, C, or T (not G)
- V = A, C, or G (not T)

```python
# Handle ambiguous bases
def count_ambiguous(sequence):
    """Count non-ATGC bases."""
    return sum(1 for base in sequence.upper() if base not in "ATGC")

# Remove regions with too many Ns
def has_quality_sequence(fasta, chrom, start, end, max_n_frac=0.1):
    """Check if region has acceptable N content."""
    seq = fasta.fetch(chrom, start, end)
    n_count = seq.upper().count('N')
    return (n_count / len(seq)) <= max_n_frac
```

## FASTQ Files

### Overview

Pysam provides `FastxFile` (or `FastqFile`) for reading FASTQ files containing raw sequencing reads with quality scores. FASTQ files do not support random access—only sequential reading.

### Opening FASTQ Files

```python
import pysam

# Open FASTQ file
fastq = pysam.FastxFile("reads.fastq")

# Works with compressed files
fastq_gz = pysam.FastxFile("reads.fastq.gz")
```

### Reading FASTQ Records

```python
fastq = pysam.FastxFile("reads.fastq")

for read in fastq:
    print(f"Name: {read.name}")
    print(f"Sequence: {read.sequence}")
    print(f"Quality: {read.quality}")
    print(f"Comment: {read.comment}")  # Optional header comment
```

**FastqProxy attributes:**
- `name` - Read identifier (without @ prefix)
- `sequence` - DNA/RNA sequence
- `quality` - ASCII-encoded quality string
- `comment` - Optional comment from header line
- `get_quality_array()` - Convert quality string to numeric array

### Quality Score Conversion

```python
# Convert quality string to numeric values
for read in fastq:
    qual_array = read.get_quality_array()
    mean_quality = sum(qual_array) / len(qual_array)
    print(f"{read.name}: mean Q = {mean_quality:.1f}")
```

Quality scores are Phred-scaled (typically Phred+33 encoding):
- Q = -10 * log10(P_error)
- ASCII 33 ('!') = Q0
- ASCII 43 ('+') = Q10
- ASCII 63 ('?') = Q30

### Common FASTQ Processing Workflows

#### Quality Filtering

```python
def filter_by_quality(input_fastq, output_fastq, min_mean_quality=20):
    """Filter reads by mean quality score."""
    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            for read in infile:
                qual_array = read.get_quality_array()
                mean_q = sum(qual_array) / len(qual_array)

                if mean_q >= min_mean_quality:
                    # Write in FASTQ format
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

#### Length Filtering

```python
def filter_by_length(input_fastq, output_fastq, min_length=50):
    """Filter reads by minimum length."""
    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            kept = 0
            for read in infile:
                if len(read.sequence) >= min_length:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
                    kept += 1
    print(f"Kept {kept} reads")
```

#### Calculate Quality Statistics

```python
def calculate_fastq_stats(fastq_file):
    """Calculate basic statistics for FASTQ file."""
    total_reads = 0
    total_bases = 0
    quality_sum = 0

    with pysam.FastxFile(fastq_file) as fastq:
        for read in fastq:
            total_reads += 1
            read_length = len(read.sequence)
            total_bases += read_length

            qual_array = read.get_quality_array()
            quality_sum += sum(qual_array)

    return {
        "total_reads": total_reads,
        "total_bases": total_bases,
        "mean_read_length": total_bases / total_reads if total_reads > 0 else 0,
        "mean_quality": quality_sum / total_bases if total_bases > 0 else 0
    }
```

#### Extract Reads by Name

```python
def extract_reads_by_name(fastq_file, read_names, output_file):
    """Extract specific reads by name."""
    read_set = set(read_names)

    with pysam.FastxFile(fastq_file) as infile:
        with open(output_file, 'w') as outfile:
            for read in infile:
                if read.name in read_set:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

#### Convert FASTQ to FASTA

```python
def fastq_to_fasta(fastq_file, fasta_file):
    """Convert FASTQ to FASTA (discards quality scores)."""
    with pysam.FastxFile(fastq_file) as infile:
        with open(fasta_file, 'w') as outfile:
            for read in infile:
                outfile.write(f">{read.name}\n")
                outfile.write(f"{read.sequence}\n")
```

#### Subsample FASTQ

```python
import random

def subsample_fastq(input_fastq, output_fastq, fraction=0.1, seed=42):
    """Randomly subsample reads from FASTQ file."""
    random.seed(seed)

    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            for read in infile:
                if random.random() < fraction:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

## Tabix-Indexed Files

### Overview

Pysam provides `TabixFile` for accessing tabix-indexed genomic data files (BED, GFF, GTF, generic tab-delimited).

### Opening Tabix Files

```python
import pysam

# Open tabix-indexed file
tabix = pysam.TabixFile("annotations.bed.gz")

# File must be bgzip-compressed and tabix-indexed
```

### Creating Tabix Index

```python
# Index a file
pysam.tabix_index("annotations.bed", preset="bed", force=True)
# Creates annotations.bed.gz and annotations.bed.gz.tbi

# Presets available: bed, gff, vcf
```

### Fetching Records

```python
tabix = pysam.TabixFile("annotations.bed.gz")

# Fetch region
for row in tabix.fetch("chr1", 1000000, 2000000):
    print(row)  # Returns tab-delimited string

# Parse with specific parser
for row in tabix.fetch("chr1", 1000000, 2000000, parser=pysam.asBed()):
    print(f"Interval: {row.contig}:{row.start}-{row.end}")

# Available parsers: asBed(), asGTF(), asVCF(), asTuple()
```

### Working with BED Files

```python
bed = pysam.TabixFile("regions.bed.gz")

# Access BED fields by name
for interval in bed.fetch("chr1", 1000000, 2000000, parser=pysam.asBed()):
    print(f"Region: {interval.contig}:{interval.start}-{interval.end}")
    print(f"Name: {interval.name}")
    print(f"Score: {interval.score}")
    print(f"Strand: {interval.strand}")
```

### Working with GTF/GFF Files

```python
gtf = pysam.TabixFile("annotations.gtf.gz")

# Access GTF fields
for feature in gtf.fetch("chr1", 1000000, 2000000, parser=pysam.asGTF()):
    print(f"Feature: {feature.feature}")
    print(f"Gene: {feature.gene_id}")
    print(f"Transcript: {feature.transcript_id}")
    print(f"Coordinates: {feature.start}-{feature.end}")
```

## Performance Tips

### FASTA
1. **Always use indexed FASTA** files (create .fai with samtools faidx)
2. **Batch fetch operations** when extracting multiple regions
3. **Cache frequently accessed sequences** in memory
4. **Use appropriate window sizes** to avoid loading excessive sequence data

### FASTQ
1. **Stream processing** - FASTQ files are read sequentially, process on-the-fly
2. **Use compressed FASTQ.gz** to save disk space (pysam handles transparently)
3. **Avoid loading entire file** into memory—process read-by-read
4. **For large files**, consider parallel processing with file splitting

### Tabix
1. **Always bgzip and tabix-index** files before region queries
2. **Use appropriate presets** when creating indices
3. **Specify parser** for named field access
4. **Batch queries** to same file to avoid re-opening

## Common Pitfalls

1. **FASTA coordinate system:** fetch() uses 0-based coordinates, region strings use 1-based
2. **Missing index:** FASTA random access requires .fai index file
3. **FASTQ sequential only:** Cannot do random access or region-based queries on FASTQ
4. **Quality encoding:** Assume Phred+33 unless specified otherwise
5. **Tabix compression:** Must use bgzip, not regular gzip, for tabix indexing
6. **Parser requirement:** TabixFile needs explicit parser for named field access
7. **Case sensitivity:** FASTA sequences preserve case—use .upper() or .lower() for consistent comparisons

---

## Reference: Variant_Files

# Working with Variant Files (VCF/BCF)

## Overview

Pysam provides the `VariantFile` class for reading and writing VCF (Variant Call Format) and BCF (binary VCF) files. These files contain information about genetic variants, including SNPs, indels, and structural variants.

## Opening Variant Files

```python
import pysam

# Reading VCF
vcf = pysam.VariantFile("example.vcf")

# Reading BCF (binary, compressed)
bcf = pysam.VariantFile("example.bcf")

# Reading compressed VCF
vcf_gz = pysam.VariantFile("example.vcf.gz")

# Writing
outvcf = pysam.VariantFile("output.vcf", "w", header=vcf.header)
```

## VariantFile Properties

**Header Information:**
- `header` - Complete VCF header with metadata
- `header.contigs` - Dictionary of contigs/chromosomes
- `header.samples` - List of sample names
- `header.filters` - Dictionary of FILTER definitions
- `header.info` - Dictionary of INFO field definitions
- `header.formats` - Dictionary of FORMAT field definitions

```python
vcf = pysam.VariantFile("example.vcf")

# List samples
print(f"Samples: {list(vcf.header.samples)}")

# List contigs
for contig in vcf.header.contigs:
    print(f"{contig}: length={vcf.header.contigs[contig].length}")

# List INFO fields
for info in vcf.header.info:
    print(f"{info}: {vcf.header.info[info].description}")
```

## Reading Variant Records

### Iterate All Variants

```python
for variant in vcf:
    print(f"{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}")
```

### Fetch Specific Region

Requires tabix index (.tbi) for VCF.gz or index for BCF:

```python
# Fetch variants in region (1-based coordinates for region string)
for variant in vcf.fetch("chr1", 1000000, 2000000):
    print(f"{variant.chrom}:{variant.pos} {variant.id}")

# Using region string (1-based)
for variant in vcf.fetch("chr1:1000000-2000000"):
    print(variant.pos)
```

**Note:** Uses **1-based coordinates** in `fetch()` calls to match VCF specification.

## VariantRecord Objects

Each variant is represented as a `VariantRecord` object:

### Position Information
- `chrom` - Chromosome/contig name
- `pos` - Position (1-based)
- `start` - Start position (0-based)
- `stop` - Stop position (0-based, exclusive)
- `id` - Variant ID (e.g., rsID)

### Allele Information
- `ref` - Reference allele
- `alts` - Tuple of alternate alleles
- `alleles` - Tuple of all alleles (ref + alts)

### Quality and Filtering
- `qual` - Quality score (QUAL field)
- `filter` - Filter status

### INFO Fields

Access INFO fields as dictionary:

```python
for variant in vcf:
    # Check if field exists
    if "DP" in variant.info:
        depth = variant.info["DP"]
        print(f"Depth: {depth}")

    # Get all INFO keys
    print(f"INFO fields: {variant.info.keys()}")

    # Access specific fields
    if "AF" in variant.info:
        allele_freq = variant.info["AF"]
        print(f"Allele frequency: {allele_freq}")
```

### Sample Genotype Data

Access sample data through `samples` dictionary:

```python
for variant in vcf:
    for sample_name in variant.samples:
        sample = variant.samples[sample_name]

        # Genotype (GT field)
        gt = sample["GT"]
        print(f"{sample_name} genotype: {gt}")

        # Other FORMAT fields
        if "DP" in sample:
            print(f"{sample_name} depth: {sample['DP']}")
        if "GQ" in sample:
            print(f"{sample_name} quality: {sample['GQ']}")

        # Alleles for this genotype
        alleles = sample.alleles
        print(f"{sample_name} alleles: {alleles}")

        # Phasing
        if sample.phased:
            print(f"{sample_name} is phased")
```

**Genotype representation:**
- `(0, 0)` - Homozygous reference
- `(0, 1)` - Heterozygous
- `(1, 1)` - Homozygous alternate
- `(None, None)` - Missing genotype
- Phased: `(0|1)` vs unphased: `(0/1)`

## Writing Variant Files

### Creating Header

```python
header = pysam.VariantHeader()

# Add contigs
header.contigs.add("chr1", length=248956422)
header.contigs.add("chr2", length=242193529)

# Add INFO fields
header.add_line('##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">')
header.add_line('##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">')

# Add FORMAT fields
header.add_line('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">')
header.add_line('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">')

# Add samples
header.add_sample("sample1")
header.add_sample("sample2")

# Create output file
outvcf = pysam.VariantFile("output.vcf", "w", header=header)
```

### Creating Variant Records

```python
# Create new variant
record = outvcf.new_record()
record.chrom = "chr1"
record.pos = 100000
record.id = "rs123456"
record.ref = "A"
record.alts = ("G",)
record.qual = 30
record.filter.add("PASS")

# Set INFO fields
record.info["DP"] = 100
record.info["AF"] = (0.25,)

# Set genotype data
record.samples["sample1"]["GT"] = (0, 1)
record.samples["sample1"]["DP"] = 50
record.samples["sample2"]["GT"] = (0, 0)
record.samples["sample2"]["DP"] = 50

# Write to file
outvcf.write(record)
```

## Filtering Variants

### Basic Filtering

```python
# Filter by quality
for variant in vcf:
    if variant.qual >= 30:
        print(f"High quality variant: {variant.chrom}:{variant.pos}")

# Filter by depth
for variant in vcf:
    if "DP" in variant.info and variant.info["DP"] >= 20:
        print(f"High depth variant: {variant.chrom}:{variant.pos}")

# Filter by allele frequency
for variant in vcf:
    if "AF" in variant.info:
        for af in variant.info["AF"]:
            if af >= 0.01:
                print(f"Common variant: {variant.chrom}:{variant.pos}")
```

### Filtering by Genotype

```python
# Find variants where sample has alternate allele
for variant in vcf:
    sample = variant.samples["sample1"]
    gt = sample["GT"]

    # Check if has alternate allele
    if gt and any(allele and allele > 0 for allele in gt):
        print(f"Sample has alt allele: {variant.chrom}:{variant.pos}")

    # Check if homozygous alternate
    if gt == (1, 1):
        print(f"Homozygous alt: {variant.chrom}:{variant.pos}")
```

### Filter Field

```python
# Check FILTER status
for variant in vcf:
    if "PASS" in variant.filter or len(variant.filter) == 0:
        print(f"Passed filters: {variant.chrom}:{variant.pos}")
    else:
        print(f"Failed: {variant.filter.keys()}")
```

## Indexing VCF Files

Create tabix index for compressed VCF:

```python
# Compress and index
pysam.tabix_index("example.vcf", preset="vcf", force=True)
# Creates example.vcf.gz and example.vcf.gz.tbi
```

Or use bcftools for BCF:

```python
pysam.bcftools.index("example.bcf")
```

## Common Workflows

### Extract Variants for Specific Samples

```python
invcf = pysam.VariantFile("input.vcf")
samples_to_keep = ["sample1", "sample3"]

# Create new header with subset of samples
new_header = invcf.header.copy()
new_header.samples.clear()
for sample in samples_to_keep:
    new_header.samples.add(sample)

outvcf = pysam.VariantFile("output.vcf", "w", header=new_header)

for variant in invcf:
    # Create new record
    new_record = outvcf.new_record(
        contig=variant.chrom,
        start=variant.start,
        stop=variant.stop,
        alleles=variant.alleles,
        id=variant.id,
        qual=variant.qual,
        filter=variant.filter,
        info=variant.info
    )

    # Copy genotype data for selected samples
    for sample in samples_to_keep:
        new_record.samples[sample].update(variant.samples[sample])

    outvcf.write(new_record)
```

### Calculate Allele Frequencies

```python
vcf = pysam.VariantFile("example.vcf")

for variant in vcf:
    total_alleles = 0
    alt_alleles = 0

    for sample_name in variant.samples:
        gt = variant.samples[sample_name]["GT"]
        if gt and None not in gt:
            total_alleles += 2
            alt_alleles += sum(1 for allele in gt if allele > 0)

    if total_alleles > 0:
        af = alt_alleles / total_alleles
        print(f"{variant.chrom}:{variant.pos} AF={af:.4f}")
```

### Convert VCF to Summary Table

```python
import csv

vcf = pysam.VariantFile("example.vcf")

with open("variants.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "DP"])

    for variant in vcf:
        writer.writerow([
            variant.chrom,
            variant.pos,
            variant.id or ".",
            variant.ref,
            ",".join(variant.alts) if variant.alts else ".",
            variant.qual or ".",
            variant.info.get("DP", ".")
        ])
```

## Performance Tips

1. **Use BCF format** for better compression and faster access than VCF
2. **Index files** with tabix for efficient region queries
3. **Filter early** to reduce processing of irrelevant variants
4. **Use INFO fields efficiently** - check existence before accessing
5. **Batch write operations** when creating VCF files

## Common Pitfalls

1. **Coordinate systems:** VCF uses 1-based coordinates, but VariantRecord.start is 0-based
2. **Missing data:** Always check if INFO/FORMAT fields exist before accessing
3. **Genotype tuples:** Genotypes are tuples, not lists—handle None values for missing data
4. **Allele indexing:** In genotype (0, 1), 0=REF, 1=first ALT, 2=second ALT, etc.
5. **Index requirement:** Region-based `fetch()` requires tabix index for VCF.gz
6. **Header modification:** When subsetting samples, properly update header and copy FORMAT fields
