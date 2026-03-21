---
title: "探索性数据分析"
description: "使用 Python 进行全面的探索性数据分析，统计概述和可视化"
category: "research"
source: "community"
author: "Community"
tags: ["exploratory", "data", "analysis"]
date: 2026-03-20
---

# Exploratory Data Analysis

## Overview

Perform comprehensive exploratory data analysis (EDA) on scientific data files across multiple domains. This skill provides automated file type detection, format-specific analysis, data quality assessment, and generates detailed markdown reports suitable for documentation and downstream analysis planning.

**Key Capabilities:**
- Automatic detection and analysis of 200+ scientific file formats
- Comprehensive format-specific metadata extraction
- Data quality and integrity assessment
- Statistical summaries and distributions
- Visualization recommendations
- Downstream analysis suggestions
- Markdown report generation

## When to Use This Skill

Use this skill when:
- User provides a path to a scientific data file for analysis
- User asks to "explore", "analyze", or "summarize" a data file
- User wants to understand the structure and content of scientific data
- User needs a comprehensive report of a dataset before analysis
- User wants to assess data quality or completeness
- User asks what type of analysis is appropriate for a file

## Supported File Categories

The skill has comprehensive coverage of scientific file formats organized into six major categories:

### 1. Chemistry and Molecular Formats (60+ extensions)
Structure files, computational chemistry outputs, molecular dynamics trajectories, and chemical databases.

**File types include:** `.pdb`, `.cif`, `.mol`, `.mol2`, `.sdf`, `.xyz`, `.smi`, `.gro`, `.log`, `.fchk`, `.cube`, `.dcd`, `.xtc`, `.trr`, `.prmtop`, `.psf`, and more.

**Reference file:** `references/chemistry_molecular_formats.md`

### 2. Bioinformatics and Genomics Formats (50+ extensions)
Sequence data, alignments, annotations, variants, and expression data.

**File types include:** `.fasta`, `.fastq`, `.sam`, `.bam`, `.vcf`, `.bed`, `.gff`, `.gtf`, `.bigwig`, `.h5ad`, `.loom`, `.counts`, `.mtx`, and more.

**Reference file:** `references/bioinformatics_genomics_formats.md`

### 3. Microscopy and Imaging Formats (45+ extensions)
Microscopy images, medical imaging, whole slide imaging, and electron microscopy.

**File types include:** `.tif`, `.nd2`, `.lif`, `.czi`, `.ims`, `.dcm`, `.nii`, `.mrc`, `.dm3`, `.vsi`, `.svs`, `.ome.tiff`, and more.

**Reference file:** `references/microscopy_imaging_formats.md`

### 4. Spectroscopy and Analytical Chemistry Formats (35+ extensions)
NMR, mass spectrometry, IR/Raman, UV-Vis, X-ray, chromatography, and other analytical techniques.

**File types include:** `.fid`, `.mzML`, `.mzXML`, `.raw`, `.mgf`, `.spc`, `.jdx`, `.xy`, `.cif` (crystallography), `.wdf`, and more.

**Reference file:** `references/spectroscopy_analytical_formats.md`

### 5. Proteomics and Metabolomics Formats (30+ extensions)
Mass spec proteomics, metabolomics, lipidomics, and multi-omics data.

**File types include:** `.mzML`, `.pepXML`, `.protXML`, `.mzid`, `.mzTab`, `.sky`, `.mgf`, `.msp`, `.h5ad`, and more.

**Reference file:** `references/proteomics_metabolomics_formats.md`

### 6. General Scientific Data Formats (30+ extensions)
Arrays, tables, hierarchical data, compressed archives, and common scientific formats.

**File types include:** `.npy`, `.npz`, `.csv`, `.xlsx`, `.json`, `.hdf5`, `.zarr`, `.parquet`, `.mat`, `.fits`, `.nc`, `.xml`, and more.

**Reference file:** `references/general_scientific_formats.md`

## Workflow

### Step 1: File Type Detection

When a user provides a file path, first identify the file type:

1. Extract the file extension
2. Look up the extension in the appropriate reference file
3. Identify the file category and format description
4. Load format-specific information

**Example:**
```
User: "Analyze data.fastq"
→ Extension: .fastq
→ Category: bioinformatics_genomics
→ Format: FASTQ Format (sequence data with quality scores)
→ Reference: references/bioinformatics_genomics_formats.md
```

### Step 2: Load Format-Specific Information

Based on the file type, read the corresponding reference file to understand:
- **Typical Data:** What kind of data this format contains
- **Use Cases:** Common applications for this format
- **Python Libraries:** How to read the file in Python
- **EDA Approach:** What analyses are appropriate for this data type

Search the reference file for the specific extension (e.g., search for "### .fastq" in `bioinformatics_genomics_formats.md`).

### Step 3: Perform Data Analysis

Use the `scripts/eda_analyzer.py` script OR implement custom analysis:

**Option A: Use the analyzer script**
```python
# The script automatically:
# 1. Detects file type
# 2. Loads reference information
# 3. Performs format-specific analysis
# 4. Generates markdown report

python scripts/eda_analyzer.py <filepath> [output.md]
```

**Option B: Custom analysis in the conversation**
Based on the format information from the reference file, perform appropriate analysis:

For tabular data (CSV, TSV, Excel):
- Load with pandas
- Check dimensions, data types
- Analyze missing values
- Calculate summary statistics
- Identify outliers
- Check for duplicates

For sequence data (FASTA, FASTQ):
- Count sequences
- Analyze length distributions
- Calculate GC content
- Assess quality scores (FASTQ)

For images (TIFF, ND2, CZI):
- Check dimensions (X, Y, Z, C, T)
- Analyze bit depth and value range
- Extract metadata (channels, timestamps, spatial calibration)
- Calculate intensity statistics

For arrays (NPY, HDF5):
- Check shape and dimensions
- Analyze data type
- Calculate statistical summaries
- Check for missing/invalid values

### Step 4: Generate Comprehensive Report

Create a markdown report with the following sections:

#### Required Sections:
1. **Title and Metadata**
   - Filename and timestamp
   - File size and location

2. **Basic Information**
   - File properties
   - Format identification

3. **File Type Details**
   - Format description from reference
   - Typical data content
   - Common use cases
   - Python libraries for reading

4. **Data Analysis**
   - Structure and dimensions
   - Statistical summaries
   - Quality assessment
   - Data characteristics

5. **Key Findings**
   - Notable patterns
   - Potential issues
   - Quality metrics

6. **Recommendations**
   - Preprocessing steps
   - Appropriate analyses
   - Tools and methods
   - Visualization approaches

#### Template Location
Use `assets/report_template.md` as a guide for report structure.

### Step 5: Save Report

Save the markdown report with a descriptive filename:
- Pattern: `{original_filename}_eda_report.md`
- Example: `experiment_data.fastq` → `experiment_data_eda_report.md`

## Detailed Format References

Each reference file contains comprehensive information for dozens of file types. To find information about a specific format:

1. Identify the category from the extension
2. Read the appropriate reference file
3. Search for the section heading matching the extension (e.g., "### .pdb")
4. Extract the format information

### Reference File Structure

Each format entry includes:
- **Description:** What the format is
- **Typical Data:** What it contains
- **Use Cases:** Common applications
- **Python Libraries:** How to read it (with code examples)
- **EDA Approach:** Specific analyses to perform

**Example lookup:**
```markdown
### .pdb - Protein Data Bank
**Description:** Standard format for 3D structures of biological macromolecules
**Typical Data:** Atomic coordinates, residue information, secondary structure
**Use Cases:** Protein structure analysis, molecular visualization, docking
**Python Libraries:**
- `Biopython`: `Bio.PDB`
- `MDAnalysis`: `MDAnalysis.Universe('file.pdb')`
**EDA Approach:**
- Structure validation (bond lengths, angles)
- B-factor distribution
- Missing residues detection
- Ramachandran plots
```

## Best Practices

### Reading Reference Files

Reference files are large (10,000+ words each). To efficiently use them:

1. **Search by extension:** Use grep to find the specific format
   ```python
   import re
   with open('references/chemistry_molecular_formats.md', 'r') as f:
       content = f.read()
       pattern = r'### \.pdb[^#]*?(?=###|\Z)'
       match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
   ```

2. **Extract relevant sections:** Don't load entire reference files into context unnecessarily

3. **Cache format info:** If analyzing multiple files of the same type, reuse the format information

### Data Analysis

1. **Sample large files:** For files with millions of records, analyze a representative sample
2. **Handle errors gracefully:** Many scientific formats require specific libraries; provide clear installation instructions
3. **Validate metadata:** Cross-check metadata consistency (e.g., stated dimensions vs actual data)
4. **Consider data provenance:** Note instrument, software versions, processing steps

### Report Generation

1. **Be comprehensive:** Include all relevant information for downstream analysis
2. **Be specific:** Provide concrete recommendations based on the file type
3. **Be actionable:** Suggest specific next steps and tools
4. **Include code examples:** Show how to load and work with the data

## Examples

### Example 1: Analyzing a FASTQ file

```python
# User provides: "Analyze reads.fastq"

# 1. Detect file type
extension = '.fastq'
category = 'bioinformatics_genomics'

# 2. Read reference info
# Search references/bioinformatics_genomics_formats.md for "### .fastq"

# 3. Perform analysis
from Bio import SeqIO
sequences = list(SeqIO.parse('reads.fastq', 'fastq'))
# Calculate: read count, length distribution, quality scores, GC content

# 4. Generate report
# Include: format description, analysis results, QC recommendations

# 5. Save as: reads_eda_report.md
```

### Example 2: Analyzing a CSV dataset

```python
# User provides: "Explore experiment_results.csv"

# 1. Detect: .csv → general_scientific

# 2. Load reference for CSV format

# 3. Analyze
import pandas as pd
df = pd.read_csv('experiment_results.csv')
# Dimensions, dtypes, missing values, statistics, correlations

# 4. Generate report with:
# - Data structure
# - Missing value patterns
# - Statistical summaries
# - Correlation matrix
# - Outlier detection results

# 5. Save report
```

### Example 3: Analyzing microscopy data

```python
# User provides: "Analyze cells.nd2"

# 1. Detect: .nd2 → microscopy_imaging (Nikon format)

# 2. Read reference for ND2 format
# Learn: multi-dimensional (XYZCT), requires nd2reader

# 3. Analyze
from nd2reader import ND2Reader
with ND2Reader('cells.nd2') as images:
    # Extract: dimensions, channels, timepoints, metadata
    # Calculate: intensity statistics, frame info

# 4. Generate report with:
# - Image dimensions (XY, Z-stacks, time, channels)
# - Channel wavelengths
# - Pixel size and calibration
# - Recommendations for image analysis

# 5. Save report
```

## Troubleshooting

### Missing Libraries

Many scientific formats require specialized libraries:

**Problem:** Import error when trying to read a file

**Solution:** Provide clear installation instructions
```python
try:
    from Bio import SeqIO
except ImportError:
    print("Install Biopython: uv pip install biopython")
```

Common requirements by category:
- **Bioinformatics:** `biopython`, `pysam`, `pyBigWig`
- **Chemistry:** `rdkit`, `mdanalysis`, `cclib`
- **Microscopy:** `tifffile`, `nd2reader`, `aicsimageio`, `pydicom`
- **Spectroscopy:** `nmrglue`, `pymzml`, `pyteomics`
- **General:** `pandas`, `numpy`, `h5py`, `scipy`

### Unknown File Types

If a file extension is not in the references:

1. Ask the user about the file format
2. Check if it's a vendor-specific variant
3. Attempt generic analysis based on file structure (text vs binary)
4. Provide general recommendations

### Large Files

For very large files:

1. Use sampling strategies (first N records)
2. Use memory-mapped access (for HDF5, NPY)
3. Process in chunks (for CSV, FASTQ)
4. Provide estimates based on samples

## Script Usage

The `scripts/eda_analyzer.py` can be used directly:

```bash
# Basic usage
python scripts/eda_analyzer.py data.csv

# Specify output file
python scripts/eda_analyzer.py data.csv output_report.md

# The script will:
# 1. Auto-detect file type
# 2. Load format references
# 3. Perform appropriate analysis
# 4. Generate markdown report
```

The script supports automatic analysis for many common formats, but custom analysis in the conversation provides more flexibility and domain-specific insights.

## Advanced Usage

### Multi-File Analysis

When analyzing multiple related files:
1. Perform individual EDA on each file
2. Create a summary comparison report
3. Identify relationships and dependencies
4. Suggest integration strategies

### Quality Control

For data quality assessment:
1. Check format compliance
2. Validate metadata consistency
3. Assess completeness
4. Identify outliers and anomalies
5. Compare to expected ranges/distributions

### Preprocessing Recommendations

Based on data characteristics, recommend:
1. Normalization strategies
2. Missing value imputation
3. Outlier handling
4. Batch correction
5. Format conversions

## Resources

### scripts/
- `eda_analyzer.py`: Comprehensive analysis script that can be run directly or imported

### references/
- `chemistry_molecular_formats.md`: 60+ chemistry/molecular file formats
- `bioinformatics_genomics_formats.md`: 50+ bioinformatics formats
- `microscopy_imaging_formats.md`: 45+ imaging formats
- `spectroscopy_analytical_formats.md`: 35+ spectroscopy formats
- `proteomics_metabolomics_formats.md`: 30+ omics formats
- `general_scientific_formats.md`: 30+ general formats

### assets/
- `report_template.md`: Comprehensive markdown template for EDA reports

---

## Reference: Bioinformatics_Genomics_Formats

# Bioinformatics and Genomics File Formats Reference

This reference covers file formats used in genomics, transcriptomics, sequence analysis, and related bioinformatics applications.

## Sequence Data Formats

### .fasta / .fa / .fna - FASTA Format
**Description:** Text-based format for nucleotide or protein sequences
**Typical Data:** DNA, RNA, or protein sequences with headers
**Use Cases:** Sequence storage, BLAST searches, alignments
**Python Libraries:**
- `Biopython`: `SeqIO.parse('file.fasta', 'fasta')`
- `pyfaidx`: Fast indexed FASTA access
- `screed`: Fast sequence parsing
**EDA Approach:**
- Sequence count and length distribution
- GC content analysis
- N content (ambiguous bases)
- Sequence ID parsing
- Duplicate detection
- Quality metrics for assemblies (N50, L50)

### .fastq / .fq - FASTQ Format
**Description:** Sequence data with base quality scores
**Typical Data:** Raw sequencing reads with Phred quality scores
**Use Cases:** NGS data, quality control, read mapping
**Python Libraries:**
- `Biopython`: `SeqIO.parse('file.fastq', 'fastq')`
- `pysam`: Fast FASTQ/BAM operations
- `HTSeq`: Sequencing data analysis
**EDA Approach:**
- Read count and length distribution
- Quality score distribution (per-base, per-read)
- GC content and bias
- Duplicate rate estimation
- Adapter contamination detection
- k-mer frequency analysis
- Encoding format validation (Phred33/64)

### .sam - Sequence Alignment/Map
**Description:** Tab-delimited text format for alignments
**Typical Data:** Aligned sequencing reads with mapping quality
**Use Cases:** Read alignment storage, variant calling
**Python Libraries:**
- `pysam`: `pysam.AlignmentFile('file.sam', 'r')`
- `HTSeq`: `HTSeq.SAM_Reader('file.sam')`
**EDA Approach:**
- Mapping rate and quality distribution
- Coverage analysis
- Insert size distribution (paired-end)
- Alignment flags distribution
- CIGAR string patterns
- Mismatch and indel rates
- Duplicate and supplementary alignment counts

### .bam - Binary Alignment/Map
**Description:** Compressed binary version of SAM
**Typical Data:** Aligned reads in compressed format
**Use Cases:** Efficient storage and processing of alignments
**Python Libraries:**
- `pysam`: Full BAM support with indexing
- `bamnostic`: Pure Python BAM reader
**EDA Approach:**
- Same as SAM plus:
- Compression ratio analysis
- Index file (.bai) validation
- Chromosome-wise statistics
- Strand bias detection
- Read group analysis

### .cram - CRAM Format
**Description:** Highly compressed alignment format
**Typical Data:** Reference-compressed aligned reads
**Use Cases:** Long-term storage, space-efficient archives
**Python Libraries:**
- `pysam`: CRAM support (requires reference)
- Reference genome must be accessible
**EDA Approach:**
- Compression efficiency vs BAM
- Reference dependency validation
- Lossy vs lossless compression assessment
- Decompression performance
- Similar alignment metrics as BAM

### .bed - Browser Extensible Data
**Description:** Tab-delimited format for genomic features
**Typical Data:** Genomic intervals (chr, start, end) with annotations
**Use Cases:** Peak calling, variant annotation, genome browsing
**Python Libraries:**
- `pybedtools`: `pybedtools.BedTool('file.bed')`
- `pyranges`: `pyranges.read_bed('file.bed')`
- `pandas`: Simple BED reading
**EDA Approach:**
- Feature count and size distribution
- Chromosome distribution
- Strand bias
- Score distribution (if present)
- Overlap and proximity analysis
- Coverage statistics
- Gap analysis between features

### .bedGraph - BED with Graph Data
**Description:** BED format with per-base signal values
**Typical Data:** Continuous-valued genomic data (coverage, signals)
**Use Cases:** Coverage tracks, ChIP-seq signals, methylation
**Python Libraries:**
- `pyBigWig`: Can convert to bigWig
- `pybedtools`: BedGraph operations
**EDA Approach:**
- Signal distribution statistics
- Genome coverage percentage
- Signal dynamics (peaks, valleys)
- Chromosome-wise signal patterns
- Quantile analysis
- Zero-coverage regions

### .bigWig / .bw - Binary BigWig
**Description:** Indexed binary format for genome-wide signal data
**Typical Data:** Continuous genomic signals (compressed and indexed)
**Use Cases:** Efficient genome browser tracks, large-scale data
**Python Libraries:**
- `pyBigWig`: `pyBigWig.open('file.bw')`
- `pybbi`: BigWig/BigBed interface
**EDA Approach:**
- Signal statistics extraction
- Zoom level analysis
- Regional signal extraction
- Efficient genome-wide summaries
- Compression efficiency
- Index structure analysis

### .bigBed / .bb - Binary BigBed
**Description:** Indexed binary BED format
**Typical Data:** Genomic features (compressed and indexed)
**Use Cases:** Large feature sets, genome browsers
**Python Libraries:**
- `pybbi`: BigBed reading
- `pybigtools`: Modern BigBed interface
**EDA Approach:**
- Feature density analysis
- Efficient interval queries
- Zoom level validation
- Index performance metrics
- Feature size statistics

### .gff / .gff3 - General Feature Format
**Description:** Tab-delimited format for genomic annotations
**Typical Data:** Gene models, transcripts, exons, regulatory elements
**Use Cases:** Genome annotation, gene prediction
**Python Libraries:**
- `BCBio.GFF`: Biopython GFF module
- `gffutils`: `gffutils.create_db('file.gff3')`
- `pyranges`: GFF support
**EDA Approach:**
- Feature type distribution (gene, exon, CDS, etc.)
- Gene structure validation
- Strand balance
- Hierarchical relationship validation
- Phase validation for CDS
- Attribute completeness
- Gene model statistics (introns, exons per gene)

### .gtf - Gene Transfer Format
**Description:** GFF2-based format for gene annotations
**Typical Data:** Gene and transcript annotations
**Use Cases:** RNA-seq analysis, gene quantification
**Python Libraries:**
- `pyranges`: `pyranges.read_gtf('file.gtf')`
- `gffutils`: GTF database creation
- `HTSeq`: GTF reading for counts
**EDA Approach:**
- Transcript isoform analysis
- Gene structure completeness
- Exon number distribution
- Transcript length distribution
- TSS and TES analysis
- Biotype distribution
- Overlapping gene detection

### .vcf - Variant Call Format
**Description:** Text format for genetic variants
**Typical Data:** SNPs, indels, structural variants with annotations
**Use Cases:** Variant calling, population genetics, GWAS
**Python Libraries:**
- `pysam`: `pysam.VariantFile('file.vcf')`
- `cyvcf2`: Fast VCF parsing
- `PyVCF`: Older but comprehensive
**EDA Approach:**
- Variant count by type (SNP, indel, SV)
- Quality score distribution
- Allele frequency spectrum
- Transition/transversion ratio
- Heterozygosity rates
- Missing genotype analysis
- Hardy-Weinberg equilibrium
- Annotation completeness (if annotated)

### .bcf - Binary VCF
**Description:** Compressed binary variant format
**Typical Data:** Same as VCF but binary
**Use Cases:** Efficient variant storage and processing
**Python Libraries:**
- `pysam`: Full BCF support
- `cyvcf2`: Optimized BCF reading
**EDA Approach:**
- Same as VCF plus:
- Compression efficiency
- Indexing validation
- Read performance metrics

### .gvcf - Genomic VCF
**Description:** VCF with reference confidence blocks
**Typical Data:** All positions (variant and non-variant)
**Use Cases:** Joint genotyping workflows, GATK
**Python Libraries:**
- `pysam`: GVCF support
- Standard VCF parsers
**EDA Approach:**
- Reference block analysis
- Coverage uniformity
- Variant density
- Genotype quality across genome
- Reference confidence distribution

## RNA-Seq and Expression Data

### .counts - Gene Count Matrix
**Description:** Tab-delimited gene expression counts
**Typical Data:** Gene IDs with read counts per sample
**Use Cases:** RNA-seq quantification, differential expression
**Python Libraries:**
- `pandas`: `pd.read_csv('file.counts', sep='\t')`
- `scanpy` (for single-cell): `sc.read_csv()`
**EDA Approach:**
- Library size distribution
- Detection rate (genes per sample)
- Zero-inflation analysis
- Count distribution (log scale)
- Outlier sample detection
- Correlation between replicates
- PCA for sample relationships

### .tpm / .fpkm - Normalized Expression
**Description:** Normalized gene expression values
**Typical Data:** TPM (transcripts per million) or FPKM values
**Use Cases:** Cross-sample comparison, visualization
**Python Libraries:**
- `pandas`: Standard CSV reading
- `anndata`: For integrated analysis
**EDA Approach:**
- Expression distribution
- Highly expressed gene identification
- Sample clustering
- Batch effect detection
- Coefficient of variation analysis
- Dynamic range assessment

### .mtx - Matrix Market Format
**Description:** Sparse matrix format (common in single-cell)
**Typical Data:** Sparse count matrices (cells × genes)
**Use Cases:** Single-cell RNA-seq, large sparse matrices
**Python Libraries:**
- `scipy.io`: `scipy.io.mmread('file.mtx')`
- `scanpy`: `sc.read_mtx('file.mtx')`
**EDA Approach:**
- Sparsity analysis
- Cell and gene filtering thresholds
- Doublet detection metrics
- Mitochondrial fraction
- UMI count distribution
- Gene detection per cell

### .h5ad - Anndata Format
**Description:** HDF5-based annotated data matrix
**Typical Data:** Expression matrix with metadata (cells, genes)
**Use Cases:** Single-cell RNA-seq analysis with Scanpy
**Python Libraries:**
- `scanpy`: `sc.read_h5ad('file.h5ad')`
- `anndata`: Direct AnnData manipulation
**EDA Approach:**
- Cell and gene counts
- Metadata completeness
- Layer availability (raw, normalized)
- Embedding presence (PCA, UMAP)
- QC metrics distribution
- Batch information
- Cell type annotation coverage

### .loom - Loom Format
**Description:** HDF5-based format for omics data
**Typical Data:** Expression matrices with metadata
**Use Cases:** Single-cell data, RNA velocity analysis
**Python Libraries:**
- `loompy`: `loompy.connect('file.loom')`
- `scanpy`: Can import loom files
**EDA Approach:**
- Layer analysis (spliced, unspliced)
- Row and column attribute exploration
- Graph connectivity analysis
- Cluster assignments
- Velocity-specific metrics

### .rds - R Data Serialization
**Description:** R object storage (often Seurat objects)
**Typical Data:** R analysis results, especially single-cell
**Use Cases:** R-Python data exchange
**Python Libraries:**
- `pyreadr`: `pyreadr.read_r('file.rds')`
- `rpy2`: For full R integration
- Conversion tools to AnnData
**EDA Approach:**
- Object type identification
- Data structure exploration
- Metadata extraction
- Conversion validation

## Alignment and Assembly Formats

### .maf - Multiple Alignment Format
**Description:** Text format for multiple sequence alignments
**Typical Data:** Genome-wide or local multiple alignments
**Use Cases:** Comparative genomics, conservation analysis
**Python Libraries:**
- `Biopython`: `AlignIO.parse('file.maf', 'maf')`
- `bx-python`: MAF-specific tools
**EDA Approach:**
- Alignment block statistics
- Species coverage
- Gap analysis
- Conservation scoring
- Alignment quality metrics
- Block length distribution

### .axt - Pairwise Alignment Format
**Description:** Pairwise alignment format (UCSC)
**Typical Data:** Pairwise genomic alignments
**Use Cases:** Genome comparison, synteny analysis
**Python Libraries:**
- Custom parsers (simple format)
- `bx-python`: AXT support
**EDA Approach:**
- Alignment score distribution
- Identity percentage
- Syntenic block identification
- Gap size analysis
- Coverage statistics

### .chain - Chain Alignment Format
**Description:** Genome coordinate mapping chains
**Typical Data:** Coordinate transformations between genome builds
**Use Cases:** Liftover, coordinate conversion
**Python Libraries:**
- `pyliftover`: Chain file usage
- Custom parsers for chain format
**EDA Approach:**
- Chain score distribution
- Coverage of source genome
- Gap analysis
- Inversion detection
- Mapping quality assessment

### .psl - Pattern Space Layout
**Description:** BLAT/BLAST alignment format
**Typical Data:** Alignment results from BLAT
**Use Cases:** Transcript mapping, similarity searches
**Python Libraries:**
- Custom parsers (tab-delimited)
- `pybedtools`: Can handle PSL
**EDA Approach:**
- Match percentage distribution
- Gap statistics
- Query coverage
- Multiple mapping analysis
- Alignment quality metrics

## Genome Assembly and Annotation

### .agp - Assembly Golden Path
**Description:** Assembly structure description
**Typical Data:** Scaffold composition, gap information
**Use Cases:** Genome assembly representation
**Python Libraries:**
- Custom parsers (simple tab-delimited)
- Assembly analysis tools
**EDA Approach:**
- Scaffold statistics (N50, L50)
- Gap type and size distribution
- Component length analysis
- Assembly contiguity metrics
- Unplaced contig analysis

### .scaffolds / .contigs - Assembly Sequences
**Description:** Assembled sequences (usually FASTA)
**Typical Data:** Assembled genomic sequences
**Use Cases:** Genome assembly output
**Python Libraries:**
- Same as FASTA format
- Assembly-specific tools (QUAST)
**EDA Approach:**
- Assembly statistics (N50, N90, etc.)
- Length distribution
- Coverage analysis
- Gap (N) content
- Duplication assessment
- BUSCO completeness (if annotations available)

### .2bit - Compressed Genome Format
**Description:** UCSC compact genome format
**Typical Data:** Reference genomes (highly compressed)
**Use Cases:** Efficient genome storage and access
**Python Libraries:**
- `py2bit`: `py2bit.open('file.2bit')`
- `twobitreader`: Alternative reader
**EDA Approach:**
- Compression efficiency
- Random access performance
- Sequence extraction validation
- Masked region analysis
- N content and distribution

### .sizes - Chromosome Sizes
**Description:** Simple format with chromosome lengths
**Typical Data:** Tab-delimited chromosome names and sizes
**Use Cases:** Genome browsers, coordinate validation
**Python Libraries:**
- Simple file reading with pandas
- Built into many genomic tools
**EDA Approach:**
- Genome size calculation
- Chromosome count
- Size distribution
- Karyotype validation
- Completeness check against reference

## Phylogenetics and Evolution

### .nwk / .newick - Newick Tree Format
**Description:** Parenthetical tree representation
**Typical Data:** Phylogenetic trees with branch lengths
**Use Cases:** Evolutionary analysis, tree visualization
**Python Libraries:**
- `Biopython`: `Phylo.read('file.nwk', 'newick')`
- `ete3`: `ete3.Tree('file.nwk')`
- `dendropy`: Phylogenetic computing
**EDA Approach:**
- Tree structure analysis (tips, internal nodes)
- Branch length distribution
- Tree balance metrics
- Ultrametricity check
- Bootstrap support analysis
- Topology validation

### .nexus - Nexus Format
**Description:** Rich format for phylogenetic data
**Typical Data:** Alignments, trees, character matrices
**Use Cases:** Phylogenetic software interchange
**Python Libraries:**
- `Biopython`: Nexus support
- `dendropy`: Comprehensive Nexus handling
**EDA Approach:**
- Data block analysis
- Character type distribution
- Tree block validation
- Taxa consistency
- Command block parsing
- Format compliance checking

### .phylip - PHYLIP Format
**Description:** Sequence alignment format (strict/relaxed)
**Typical Data:** Multiple sequence alignments
**Use Cases:** Phylogenetic analysis input
**Python Libraries:**
- `Biopython`: `AlignIO.read('file.phy', 'phylip')`
- `dendropy`: PHYLIP support
**EDA Approach:**
- Alignment dimensions
- Sequence length uniformity
- Gap position analysis
- Informative site calculation
- Format variant detection (strict vs relaxed)

### .paml - PAML Output
**Description:** Output from PAML phylogenetic software
**Typical Data:** Evolutionary model results, dN/dS ratios
**Use Cases:** Molecular evolution analysis
**Python Libraries:**
- Custom parsers for specific PAML programs
- `Biopython`: Basic PAML parsing
**EDA Approach:**
- Model parameter extraction
- Likelihood values
- dN/dS ratio distribution
- Branch-specific results
- Convergence assessment

## Protein and Structure Data

### .embl - EMBL Format
**Description:** Rich sequence annotation format
**Typical Data:** Sequences with extensive annotations
**Use Cases:** Sequence databases, genome records
**Python Libraries:**
- `Biopython`: `SeqIO.read('file.embl', 'embl')`
**EDA Approach:**
- Feature annotation completeness
- Sequence length and type
- Reference information
- Cross-reference validation
- Feature overlap analysis

### .genbank / .gb / .gbk - GenBank Format
**Description:** NCBI's sequence annotation format
**Typical Data:** Annotated sequences with features
**Use Cases:** Sequence databases, annotation transfer
**Python Libraries:**
- `Biopython`: `SeqIO.parse('file.gb', 'genbank')`
**EDA Approach:**
- Feature type distribution
- CDS analysis (start codons, stops)
- Translation validation
- Annotation completeness
- Source organism extraction
- Reference and publication info
- Locus tag consistency

### .sff - Standard Flowgram Format
**Description:** 454/Roche sequencing data format
**Typical Data:** Raw pyrosequencing flowgrams
**Use Cases:** Legacy 454 sequencing data
**Python Libraries:**
- `Biopython`: `SeqIO.parse('file.sff', 'sff')`
- Platform-specific tools
**EDA Approach:**
- Read count and length
- Flowgram signal quality
- Key sequence detection
- Adapter trimming validation
- Quality score distribution

### .hdf5 (Genomics Specific)
**Description:** HDF5 for genomics (10X, Hi-C, etc.)
**Typical Data:** High-throughput genomics data
**Use Cases:** 10X Genomics, spatial transcriptomics
**Python Libraries:**
- `h5py`: Low-level access
- `scanpy`: For 10X data
- `cooler`: For Hi-C data
**EDA Approach:**
- Dataset structure exploration
- Barcode statistics
- UMI counting
- Feature-barcode matrix analysis
- Spatial coordinates (if applicable)

### .cool / .mcool - Cooler Format
**Description:** HDF5-based Hi-C contact matrices
**Typical Data:** Chromatin interaction matrices
**Use Cases:** 3D genome analysis, Hi-C data
**Python Libraries:**
- `cooler`: `cooler.Cooler('file.cool')`
- `hicstraw`: For .hic format
**EDA Approach:**
- Resolution analysis
- Contact matrix statistics
- Distance decay curves
- Compartment analysis
- TAD boundary detection
- Balance factor validation

### .hic - Hi-C Binary Format
**Description:** Juicer binary Hi-C format
**Typical Data:** Multi-resolution Hi-C matrices
**Use Cases:** Hi-C analysis with Juicer tools
**Python Libraries:**
- `hicstraw`: `hicstraw.HiCFile('file.hic')`
- `straw`: C++ library with Python bindings
**EDA Approach:**
- Available resolutions
- Normalization methods
- Contact statistics
- Chromosomal interactions
- Quality metrics

### .bw (ChIP-seq / ATAC-seq specific)
**Description:** BigWig files for epigenomics
**Typical Data:** Coverage or enrichment signals
**Use Cases:** ChIP-seq, ATAC-seq, DNase-seq
**Python Libraries:**
- `pyBigWig`: Standard bigWig access
**EDA Approach:**
- Peak enrichment patterns
- Background signal analysis
- Sample correlation
- Signal-to-noise ratio
- Library complexity metrics

### .narrowPeak / .broadPeak - ENCODE Peak Formats
**Description:** BED-based formats for peaks
**Typical Data:** Peak calls with scores and p-values
**Use Cases:** ChIP-seq peak calling output
**Python Libraries:**
- `pybedtools`: BED-compatible
- Custom parsers for peak-specific fields
**EDA Approach:**
- Peak count and width distribution
- Signal value distribution
- Q-value and p-value analysis
- Peak summit analysis
- Overlap with known features
- Motif enrichment preparation

### .wig - Wiggle Format
**Description:** Dense continuous genomic data
**Typical Data:** Coverage or signal tracks
**Use Cases:** Genome browser visualization
**Python Libraries:**
- `pyBigWig`: Can convert to bigWig
- Custom parsers for wiggle format
**EDA Approach:**
- Signal statistics
- Coverage metrics
- Format variant (fixedStep vs variableStep)
- Span parameter analysis
- Conversion efficiency to bigWig

### .ab1 - Sanger Sequencing Trace
**Description:** Binary chromatogram format
**Typical Data:** Sanger sequencing traces
**Use Cases:** Capillary sequencing validation
**Python Libraries:**
- `Biopython`: `SeqIO.read('file.ab1', 'abi')`
- `tracy` tools: For quality assessment
**EDA Approach:**
- Base calling quality
- Trace quality scores
- Mixed base detection
- Primer and vector detection
- Read length and quality region
- Heterozygosity detection

### .scf - Standard Chromatogram Format
**Description:** Sanger sequencing chromatogram
**Typical Data:** Base calls and confidence values
**Use Cases:** Sequencing trace analysis
**Python Libraries:**
- `Biopython`: SCF format support
**EDA Approach:**
- Similar to AB1 format
- Quality score profiles
- Peak height ratios
- Signal-to-noise metrics

### .idx - Index Files (Generic)
**Description:** Index files for various formats
**Typical Data:** Fast random access indices
**Use Cases:** Efficient data access (BAM, VCF, etc.)
**Python Libraries:**
- Format-specific libraries handle indices
- `pysam`: Auto-handles BAI, CSI indices
**EDA Approach:**
- Index completeness validation
- Binning strategy analysis
- Access performance metrics
- Index size vs data size ratio

---

## Reference: Chemistry_Molecular_Formats

# Chemistry and Molecular File Formats Reference

This reference covers file formats commonly used in computational chemistry, cheminformatics, molecular modeling, and related fields.

## Structure File Formats

### .pdb - Protein Data Bank
**Description:** Standard format for 3D structures of biological macromolecules
**Typical Data:** Atomic coordinates, residue information, secondary structure, crystal structure data
**Use Cases:** Protein structure analysis, molecular visualization, docking studies
**Python Libraries:**
- `Biopython`: `Bio.PDB`
- `MDAnalysis`: `MDAnalysis.Universe('file.pdb')`
- `PyMOL`: `pymol.cmd.load('file.pdb')`
- `ProDy`: `prody.parsePDB('file.pdb')`
**EDA Approach:**
- Structure validation (bond lengths, angles, clashes)
- Secondary structure analysis
- B-factor distribution
- Missing residues/atoms detection
- Ramachandran plots for validation
- Surface area and volume calculations

### .cif - Crystallographic Information File
**Description:** Structured data format for crystallographic information
**Typical Data:** Unit cell parameters, atomic coordinates, symmetry operations, experimental data
**Use Cases:** Crystal structure determination, structural biology, materials science
**Python Libraries:**
- `gemmi`: `gemmi.cif.read_file('file.cif')`
- `PyCifRW`: `CifFile.ReadCif('file.cif')`
- `Biopython`: `Bio.PDB.MMCIFParser()`
**EDA Approach:**
- Data completeness check
- Resolution and quality metrics
- Unit cell parameter analysis
- Symmetry group validation
- Atomic displacement parameters
- R-factors and validation metrics

### .mol - MDL Molfile
**Description:** Chemical structure file format by MDL/Accelrys
**Typical Data:** 2D/3D coordinates, atom types, bond orders, charges
**Use Cases:** Chemical database storage, cheminformatics, drug design
**Python Libraries:**
- `RDKit`: `Chem.MolFromMolFile('file.mol')`
- `Open Babel`: `pybel.readfile('mol', 'file.mol')`
- `ChemoPy`: For descriptor calculation
**EDA Approach:**
- Molecular property calculation (MW, logP, TPSA)
- Functional group analysis
- Ring system detection
- Stereochemistry validation
- 2D/3D coordinate consistency
- Valence and charge validation

### .mol2 - Tripos Mol2
**Description:** Complete 3D molecular structure format with atom typing
**Typical Data:** Coordinates, SYBYL atom types, bond types, charges, substructures
**Use Cases:** Molecular docking, QSAR studies, drug discovery
**Python Libraries:**
- `RDKit`: `Chem.MolFromMol2File('file.mol2')`
- `Open Babel`: `pybel.readfile('mol2', 'file.mol2')`
- `MDAnalysis`: Can parse mol2 topology
**EDA Approach:**
- Atom type distribution
- Partial charge analysis
- Bond type statistics
- Substructure identification
- Conformational analysis
- Energy minimization status check

### .sdf - Structure Data File
**Description:** Multi-structure file format with associated data
**Typical Data:** Multiple molecular structures with properties/annotations
**Use Cases:** Chemical databases, virtual screening, compound libraries
**Python Libraries:**
- `RDKit`: `Chem.SDMolSupplier('file.sdf')`
- `Open Babel`: `pybel.readfile('sdf', 'file.sdf')`
- `PandasTools` (RDKit): For DataFrame integration
**EDA Approach:**
- Dataset size and diversity metrics
- Property distribution analysis (MW, logP, etc.)
- Structural diversity (Tanimoto similarity)
- Missing data assessment
- Outlier detection in properties
- Scaffold analysis

### .xyz - XYZ Coordinates
**Description:** Simple Cartesian coordinate format
**Typical Data:** Atom types and 3D coordinates
**Use Cases:** Quantum chemistry, geometry optimization, molecular dynamics
**Python Libraries:**
- `ASE`: `ase.io.read('file.xyz')`
- `Open Babel`: `pybel.readfile('xyz', 'file.xyz')`
- `cclib`: For parsing QM outputs with xyz
**EDA Approach:**
- Geometry analysis (bond lengths, angles, dihedrals)
- Center of mass calculation
- Moment of inertia
- Molecular size metrics
- Coordinate validation
- Symmetry detection

### .smi / .smiles - SMILES String
**Description:** Line notation for chemical structures
**Typical Data:** Text representation of molecular structure
**Use Cases:** Chemical databases, literature mining, data exchange
**Python Libraries:**
- `RDKit`: `Chem.MolFromSmiles(smiles)`
- `Open Babel`: Can parse SMILES
- `DeepChem`: For ML on SMILES
**EDA Approach:**
- SMILES syntax validation
- Descriptor calculation from SMILES
- Fingerprint generation
- Substructure searching
- Tautomer enumeration
- Stereoisomer handling

### .pdbqt - AutoDock PDBQT
**Description:** Modified PDB format for AutoDock docking
**Typical Data:** Coordinates, partial charges, atom types for docking
**Use Cases:** Molecular docking, virtual screening
**Python Libraries:**
- `Meeko`: For PDBQT preparation
- `Open Babel`: Can read PDBQT
- `ProDy`: Limited PDBQT support
**EDA Approach:**
- Charge distribution analysis
- Rotatable bond identification
- Atom type validation
- Coordinate quality check
- Hydrogen placement validation
- Torsion definition analysis

### .mae - Maestro Format
**Description:** Schrödinger's proprietary molecular structure format
**Typical Data:** Structures, properties, annotations from Schrödinger suite
**Use Cases:** Drug discovery, molecular modeling with Schrödinger tools
**Python Libraries:**
- `schrodinger.structure`: Requires Schrödinger installation
- Custom parsers for basic reading
**EDA Approach:**
- Property extraction and analysis
- Structure quality metrics
- Conformer analysis
- Docking score distributions
- Ligand efficiency metrics

### .gro - GROMACS Coordinate File
**Description:** Molecular structure file for GROMACS MD simulations
**Typical Data:** Atom positions, velocities, box vectors
**Use Cases:** Molecular dynamics simulations, GROMACS workflows
**Python Libraries:**
- `MDAnalysis`: `Universe('file.gro')`
- `MDTraj`: `mdtraj.load_gro('file.gro')`
- `GromacsWrapper`: For GROMACS integration
**EDA Approach:**
- System composition analysis
- Box dimension validation
- Atom position distribution
- Velocity distribution (if present)
- Density calculation
- Solvation analysis

## Computational Chemistry Output Formats

### .log - Gaussian Log File
**Description:** Output from Gaussian quantum chemistry calculations
**Typical Data:** Energies, geometries, frequencies, orbitals, populations
**Use Cases:** QM calculations, geometry optimization, frequency analysis
**Python Libraries:**
- `cclib`: `cclib.io.ccread('file.log')`
- `GaussianRunPack`: For Gaussian workflows
- Custom parsers with regex
**EDA Approach:**
- Convergence analysis
- Energy profile extraction
- Vibrational frequency analysis
- Orbital energy levels
- Population analysis (Mulliken, NBO)
- Thermochemistry data extraction

### .out - Quantum Chemistry Output
**Description:** Generic output file from various QM packages
**Typical Data:** Calculation results, energies, properties
**Use Cases:** QM calculations across different software
**Python Libraries:**
- `cclib`: Universal parser for QM outputs
- `ASE`: Can read some output formats
**EDA Approach:**
- Software-specific parsing
- Convergence criteria check
- Energy and gradient trends
- Basis set and method validation
- Computational cost analysis

### .wfn / .wfx - Wavefunction Files
**Description:** Wavefunction data for quantum chemical analysis
**Typical Data:** Molecular orbitals, basis sets, density matrices
**Use Cases:** Electron density analysis, QTAIM analysis
**Python Libraries:**
- `Multiwfn`: Interface via Python
- `Horton`: For wavefunction analysis
- Custom parsers for specific formats
**EDA Approach:**
- Orbital population analysis
- Electron density distribution
- Critical point analysis (QTAIM)
- Molecular orbital visualization
- Bonding analysis

### .fchk - Gaussian Formatted Checkpoint
**Description:** Formatted checkpoint file from Gaussian
**Typical Data:** Complete wavefunction data, results, geometry
**Use Cases:** Post-processing Gaussian calculations
**Python Libraries:**
- `cclib`: Can parse fchk files
- `GaussView` Python API (if available)
- Custom parsers
**EDA Approach:**
- Wavefunction quality assessment
- Property extraction
- Basis set information
- Gradient and Hessian analysis
- Natural orbital analysis

### .cube - Gaussian Cube File
**Description:** Volumetric data on a 3D grid
**Typical Data:** Electron density, molecular orbitals, ESP on grid
**Use Cases:** Visualization of volumetric properties
**Python Libraries:**
- `cclib`: `cclib.io.ccread('file.cube')`
- `ase.io`: `ase.io.read('file.cube')`
- `pyquante`: For cube file manipulation
**EDA Approach:**
- Grid dimension and spacing analysis
- Value distribution statistics
- Isosurface value determination
- Integration over volume
- Comparison between different cubes

## Molecular Dynamics Formats

### .dcd - Binary Trajectory
**Description:** Binary trajectory format (CHARMM, NAMD)
**Typical Data:** Time series of atomic coordinates
**Use Cases:** MD trajectory analysis
**Python Libraries:**
- `MDAnalysis`: `Universe(topology, 'traj.dcd')`
- `MDTraj`: `mdtraj.load_dcd('traj.dcd', top='topology.pdb')`
- `PyTraj` (Amber): Limited support
**EDA Approach:**
- RMSD/RMSF analysis
- Trajectory length and frame count
- Coordinate range and drift
- Periodic boundary handling
- File integrity check
- Time step validation

### .xtc - Compressed Trajectory
**Description:** GROMACS compressed trajectory format
**Typical Data:** Compressed coordinates from MD simulations
**Use Cases:** Space-efficient MD trajectory storage
**Python Libraries:**
- `MDAnalysis`: `Universe(topology, 'traj.xtc')`
- `MDTraj`: `mdtraj.load_xtc('traj.xtc', top='topology.pdb')`
**EDA Approach:**
- Compression ratio assessment
- Precision loss evaluation
- RMSD over time
- Structural stability metrics
- Sampling frequency analysis

### .trr - GROMACS Trajectory
**Description:** Full precision GROMACS trajectory
**Typical Data:** Coordinates, velocities, forces from MD
**Use Cases:** High-precision MD analysis
**Python Libraries:**
- `MDAnalysis`: Full support
- `MDTraj`: Can read trr files
- `GromacsWrapper`
**EDA Approach:**
- Full system dynamics analysis
- Energy conservation check (with velocities)
- Force analysis
- Temperature and pressure validation
- System equilibration assessment

### .nc / .netcdf - Amber NetCDF Trajectory
**Description:** Network Common Data Form trajectory
**Typical Data:** MD coordinates, velocities, forces
**Use Cases:** Amber MD simulations, large trajectory storage
**Python Libraries:**
- `MDAnalysis`: NetCDF support
- `PyTraj`: Native Amber analysis
- `netCDF4`: Low-level access
**EDA Approach:**
- Metadata extraction
- Trajectory statistics
- Time series analysis
- Replica exchange analysis
- Multi-dimensional data extraction

### .top - GROMACS Topology
**Description:** Molecular topology for GROMACS
**Typical Data:** Atom types, bonds, angles, force field parameters
**Use Cases:** MD simulation setup and analysis
**Python Libraries:**
- `ParmEd`: `parmed.load_file('system.top')`
- `MDAnalysis`: Can parse topology
- Custom parsers for specific fields
**EDA Approach:**
- Force field parameter validation
- System composition
- Bond/angle/dihedral distribution
- Charge neutrality check
- Molecule type enumeration

### .psf - Protein Structure File (CHARMM)
**Description:** Topology file for CHARMM/NAMD
**Typical Data:** Atom connectivity, types, charges
**Use Cases:** CHARMM/NAMD MD simulations
**Python Libraries:**
- `MDAnalysis`: Native PSF support
- `ParmEd`: Can read PSF files
**EDA Approach:**
- Topology validation
- Connectivity analysis
- Charge distribution
- Atom type statistics
- Segment analysis

### .prmtop - Amber Parameter/Topology
**Description:** Amber topology and parameter file
**Typical Data:** System topology, force field parameters
**Use Cases:** Amber MD simulations
**Python Libraries:**
- `ParmEd`: `parmed.load_file('system.prmtop')`
- `PyTraj`: Native Amber support
**EDA Approach:**
- Force field completeness
- Parameter validation
- System size and composition
- Periodic box information
- Atom mask creation for analysis

### .inpcrd / .rst7 - Amber Coordinates
**Description:** Amber coordinate/restart file
**Typical Data:** Atomic coordinates, velocities, box info
**Use Cases:** Starting coordinates for Amber MD
**Python Libraries:**
- `ParmEd`: Works with prmtop
- `PyTraj`: Amber coordinate reading
**EDA Approach:**
- Coordinate validity
- System initialization check
- Box vector validation
- Velocity distribution (if restart)
- Energy minimization status

## Spectroscopy and Analytical Data

### .jcamp / .jdx - JCAMP-DX
**Description:** Joint Committee on Atomic and Molecular Physical Data eXchange
**Typical Data:** Spectroscopic data (IR, NMR, MS, UV-Vis)
**Use Cases:** Spectroscopy data exchange and archiving
**Python Libraries:**
- `jcamp`: `jcamp.jcamp_reader('file.jdx')`
- `nmrglue`: For NMR JCAMP files
- Custom parsers for specific subtypes
**EDA Approach:**
- Peak detection and analysis
- Baseline correction assessment
- Signal-to-noise calculation
- Spectral range validation
- Integration analysis
- Comparison with reference spectra

### .mzML - Mass Spectrometry Markup Language
**Description:** Standard XML format for mass spectrometry data
**Typical Data:** MS/MS spectra, chromatograms, metadata
**Use Cases:** Proteomics, metabolomics, mass spectrometry workflows
**Python Libraries:**
- `pymzml`: `pymzml.run.Reader('file.mzML')`
- `pyteomics`: `pyteomics.mzml.read('file.mzML')`
- `MSFileReader` wrappers
**EDA Approach:**
- Scan count and types
- MS level distribution
- Retention time range
- m/z range and resolution
- Peak intensity distribution
- Data completeness
- Quality control metrics

### .mzXML - Mass Spectrometry XML
**Description:** Open XML format for MS data
**Typical Data:** Mass spectra, retention times, peak lists
**Use Cases:** Legacy MS data, metabolomics
**Python Libraries:**
- `pymzml`: Can read mzXML
- `pyteomics.mzxml`
- `lxml` for direct XML parsing
**EDA Approach:**
- Similar to mzML
- Version compatibility check
- Conversion quality assessment
- Peak picking validation

### .raw - Vendor Raw Data
**Description:** Proprietary instrument data files (Thermo, Bruker, etc.)
**Typical Data:** Raw instrument signals, unprocessed data
**Use Cases:** Direct instrument data access
**Python Libraries:**
- `pymsfilereader`: For Thermo RAW files
- `ThermoRawFileParser`: CLI wrapper
- Vendor-specific APIs (Thermo, Bruker Compass)
**EDA Approach:**
- Instrument method extraction
- Raw signal quality
- Calibration status
- Scan function analysis
- Chromatographic quality metrics

### .d - Agilent Data Directory
**Description:** Agilent's data folder structure
**Typical Data:** LC-MS, GC-MS data and metadata
**Use Cases:** Agilent instrument data processing
**Python Libraries:**
- `agilent-reader`: Community tools
- `Chemstation` Python integration
- Custom directory parsing
**EDA Approach:**
- Directory structure validation
- Method parameter extraction
- Signal file integrity
- Calibration curve analysis
- Sequence information extraction

### .fid - NMR Free Induction Decay
**Description:** Raw NMR time-domain data
**Typical Data:** Time-domain NMR signal
**Use Cases:** NMR processing and analysis
**Python Libraries:**
- `nmrglue`: `nmrglue.bruker.read_fid('fid')`
- `nmrstarlib`: For NMR-STAR files
**EDA Approach:**
- Signal decay analysis
- Noise level assessment
- Acquisition parameter validation
- Apodization function selection
- Zero-filling optimization
- Phasing parameter estimation

### .ft - NMR Frequency-Domain Data
**Description:** Processed NMR spectrum
**Typical Data:** Frequency-domain NMR data
**Use Cases:** NMR analysis and interpretation
**Python Libraries:**
- `nmrglue`: Comprehensive NMR support
- `pyNMR`: For processing
**EDA Approach:**
- Peak picking and integration
- Chemical shift calibration
- Multiplicity analysis
- Coupling constant extraction
- Spectral quality metrics
- Reference compound identification

### .spc - Spectroscopy File
**Description:** Thermo Galactic spectroscopy format
**Typical Data:** IR, Raman, UV-Vis spectra
**Use Cases:** Spectroscopic data from various instruments
**Python Libraries:**
- `spc`: `spc.File('file.spc')`
- Custom parsers for binary format
**EDA Approach:**
- Spectral resolution
- Wavelength/wavenumber range
- Baseline characterization
- Peak identification
- Derivative spectra calculation

## Chemical Database Formats

### .inchi - International Chemical Identifier
**Description:** Text identifier for chemical substances
**Typical Data:** Layered chemical structure representation
**Use Cases:** Chemical database keys, structure searching
**Python Libraries:**
- `RDKit`: `Chem.MolFromInchi(inchi)`
- `Open Babel`: InChI conversion
**EDA Approach:**
- InChI validation
- Layer analysis
- Stereochemistry verification
- InChI key generation
- Structure round-trip validation

### .cdx / .cdxml - ChemDraw Exchange
**Description:** ChemDraw drawing file format
**Typical Data:** 2D chemical structures with annotations
**Use Cases:** Chemical drawing, publication figures
**Python Libraries:**
- `RDKit`: Can import some CDXML
- `Open Babel`: Limited support
- `ChemDraw` Python API (commercial)
**EDA Approach:**
- Structure extraction
- Annotation preservation
- Style consistency
- 2D coordinate validation

### .cml - Chemical Markup Language
**Description:** XML-based chemical structure format
**Typical Data:** Chemical structures, reactions, properties
**Use Cases:** Semantic chemical data representation
**Python Libraries:**
- `RDKit`: CML support
- `Open Babel`: Good CML support
- `lxml`: For XML parsing
**EDA Approach:**
- XML schema validation
- Namespace handling
- Property extraction
- Reaction scheme analysis
- Metadata completeness

### .rxn - MDL Reaction File
**Description:** Chemical reaction structure file
**Typical Data:** Reactants, products, reaction arrows
**Use Cases:** Reaction databases, synthesis planning
**Python Libraries:**
- `RDKit`: `Chem.ReactionFromRxnFile('file.rxn')`
- `Open Babel`: Reaction support
**EDA Approach:**
- Reaction balancing validation
- Atom mapping analysis
- Reagent identification
- Stereochemistry changes
- Reaction classification

### .rdf - Reaction Data File
**Description:** Multi-reaction file format
**Typical Data:** Multiple reactions with data
**Use Cases:** Reaction databases
**Python Libraries:**
- `RDKit`: RDF reading capabilities
- Custom parsers
**EDA Approach:**
- Reaction yield statistics
- Condition analysis
- Success rate patterns
- Reagent frequency analysis

## Computational Output and Data

### .hdf5 / .h5 - Hierarchical Data Format
**Description:** Container for scientific data arrays
**Typical Data:** Large arrays, metadata, hierarchical organization
**Use Cases:** Large dataset storage, computational results
**Python Libraries:**
- `h5py`: `h5py.File('file.h5', 'r')`
- `pytables`: Advanced HDF5 interface
- `pandas`: Can read HDF5
**EDA Approach:**
- Dataset structure exploration
- Array shape and dtype analysis
- Metadata extraction
- Memory-efficient data sampling
- Chunk optimization analysis
- Compression ratio assessment

### .pkl / .pickle - Python Pickle
**Description:** Serialized Python objects
**Typical Data:** Any Python object (molecules, dataframes, models)
**Use Cases:** Intermediate data storage, model persistence
**Python Libraries:**
- `pickle`: Built-in serialization
- `joblib`: Enhanced pickling for large arrays
- `dill`: Extended pickle support
**EDA Approach:**
- Object type inspection
- Size and complexity analysis
- Version compatibility check
- Security validation (trusted source)
- Deserialization testing

### .npy / .npz - NumPy Arrays
**Description:** NumPy array binary format
**Typical Data:** Numerical arrays (coordinates, features, matrices)
**Use Cases:** Fast numerical data I/O
**Python Libraries:**
- `numpy`: `np.load('file.npy')`
- Direct memory mapping for large files
**EDA Approach:**
- Array shape and dimensions
- Data type and precision
- Statistical summary (mean, std, range)
- Missing value detection
- Outlier identification
- Memory footprint analysis

### .mat - MATLAB Data File
**Description:** MATLAB workspace data
**Typical Data:** Arrays, structures from MATLAB
**Use Cases:** MATLAB-Python data exchange
**Python Libraries:**
- `scipy.io`: `scipy.io.loadmat('file.mat')`
- `h5py`: For v7.3 MAT files
**EDA Approach:**
- Variable extraction and types
- Array dimension analysis
- Structure field exploration
- MATLAB version compatibility
- Data type conversion validation

### .csv - Comma-Separated Values
**Description:** Tabular data in text format
**Typical Data:** Chemical properties, experimental data, descriptors
**Use Cases:** Data exchange, analysis, machine learning
**Python Libraries:**
- `pandas`: `pd.read_csv('file.csv')`
- `csv`: Built-in module
- `polars`: Fast CSV reading
**EDA Approach:**
- Data types inference
- Missing value patterns
- Statistical summaries
- Correlation analysis
- Distribution visualization
- Outlier detection

### .json - JavaScript Object Notation
**Description:** Structured text data format
**Typical Data:** Chemical properties, metadata, API responses
**Use Cases:** Data interchange, configuration, web APIs
**Python Libraries:**
- `json`: Built-in JSON support
- `pandas`: `pd.read_json()`
- `ujson`: Faster JSON parsing
**EDA Approach:**
- Schema validation
- Nesting depth analysis
- Key-value distribution
- Data type consistency
- Array length statistics

### .parquet - Apache Parquet
**Description:** Columnar storage format
**Typical Data:** Large tabular datasets efficiently
**Use Cases:** Big data, efficient columnar analytics
**Python Libraries:**
- `pandas`: `pd.read_parquet('file.parquet')`
- `pyarrow`: Direct parquet access
- `fastparquet`: Alternative implementation
**EDA Approach:**
- Column statistics from metadata
- Partition analysis
- Compression efficiency
- Row group structure
- Fast sampling for large files
- Schema evolution tracking

---

## Reference: General_Scientific_Formats

# General Scientific Data Formats Reference

This reference covers general-purpose scientific data formats used across multiple disciplines.

## Numerical and Array Data

### .npy - NumPy Array
**Description:** Binary NumPy array format
**Typical Data:** N-dimensional arrays of any data type
**Use Cases:** Fast I/O for numerical data, intermediate results
**Python Libraries:**
- `numpy`: `np.load('file.npy')`, `np.save()`
- Memory-mapped access: `np.load('file.npy', mmap_mode='r')`
**EDA Approach:**
- Array shape and dimensionality
- Data type and precision
- Statistical summary (mean, std, min, max, percentiles)
- Missing or invalid values (NaN, inf)
- Memory footprint
- Value distribution and histogram
- Sparsity analysis
- Correlation structure (if 2D)

### .npz - Compressed NumPy Archive
**Description:** Multiple NumPy arrays in one file
**Typical Data:** Collections of related arrays
**Use Cases:** Saving multiple arrays together, compressed storage
**Python Libraries:**
- `numpy`: `np.load('file.npz')` returns dict-like object
- `np.savez()` or `np.savez_compressed()`
**EDA Approach:**
- List of contained arrays
- Individual array analysis
- Relationships between arrays
- Total file size and compression ratio
- Naming conventions
- Data consistency checks

### .csv - Comma-Separated Values
**Description:** Plain text tabular data
**Typical Data:** Experimental measurements, results tables
**Use Cases:** Universal data exchange, spreadsheet export
**Python Libraries:**
- `pandas`: `pd.read_csv('file.csv')`
- `csv`: Built-in module
- `polars`: High-performance CSV reading
- `numpy`: `np.loadtxt()` or `np.genfromtxt()`
**EDA Approach:**
- Row and column counts
- Data type inference
- Missing value patterns and frequency
- Column statistics (numeric: mean, std; categorical: frequencies)
- Outlier detection
- Correlation matrix
- Duplicate row detection
- Header and index validation
- Encoding issues detection

### .tsv / .tab - Tab-Separated Values
**Description:** Tab-delimited tabular data
**Typical Data:** Similar to CSV but tab-separated
**Use Cases:** Bioinformatics, text processing output
**Python Libraries:**
- `pandas`: `pd.read_csv('file.tsv', sep='\t')`
**EDA Approach:**
- Same as CSV format
- Tab vs space validation
- Quote handling

### .xlsx / .xls - Excel Spreadsheets
**Description:** Microsoft Excel binary/XML formats
**Typical Data:** Tabular data with formatting, formulas
**Use Cases:** Lab notebooks, data entry, reports
**Python Libraries:**
- `pandas`: `pd.read_excel('file.xlsx')`
- `openpyxl`: Full Excel file manipulation
- `xlrd`: Reading .xls (legacy)
**EDA Approach:**
- Sheet enumeration and names
- Per-sheet data analysis
- Formula evaluation
- Merged cells handling
- Hidden rows/columns
- Data validation rules
- Named ranges
- Formatting-only cells detection

### .json - JavaScript Object Notation
**Description:** Hierarchical text data format
**Typical Data:** Nested data structures, metadata
**Use Cases:** API responses, configuration, results
**Python Libraries:**
- `json`: Built-in module
- `pandas`: `pd.read_json()`
- `ujson`: Faster JSON parsing
**EDA Approach:**
- Schema inference
- Nesting depth
- Key-value distribution
- Array lengths
- Data type consistency
- Missing keys
- Duplicate detection
- Size and complexity metrics

### .xml - Extensible Markup Language
**Description:** Hierarchical markup format
**Typical Data:** Structured data with metadata
**Use Cases:** Standards-based data exchange, APIs
**Python Libraries:**
- `lxml`: `lxml.etree.parse()`
- `xml.etree.ElementTree`: Built-in XML
- `xmltodict`: Convert XML to dict
**EDA Approach:**
- Schema/DTD validation
- Element hierarchy and depth
- Namespace handling
- Attribute vs element content
- CDATA sections
- Text content extraction
- Sibling and child counts

### .yaml / .yml - YAML
**Description:** Human-readable data serialization
**Typical Data:** Configuration, metadata, parameters
**Use Cases:** Experiment configurations, pipelines
**Python Libraries:**
- `yaml`: `yaml.safe_load()` or `yaml.load()`
- `ruamel.yaml`: YAML 1.2 support
**EDA Approach:**
- Configuration structure
- Data type handling
- List and dict depth
- Anchor and alias usage
- Multi-document files
- Comments preservation
- Validation against schema

### .toml - TOML Configuration
**Description:** Configuration file format
**Typical Data:** Settings, parameters
**Use Cases:** Python package configuration, settings
**Python Libraries:**
- `tomli` / `tomllib`: TOML reading (tomllib in Python 3.11+)
- `toml`: Reading and writing
**EDA Approach:**
- Section structure
- Key-value pairs
- Data type inference
- Nested table validation
- Required vs optional fields

### .ini - INI Configuration
**Description:** Simple configuration format
**Typical Data:** Application settings
**Use Cases:** Legacy configurations, simple settings
**Python Libraries:**
- `configparser`: Built-in INI parser
**EDA Approach:**
- Section enumeration
- Key-value extraction
- Type conversion
- Comment handling
- Case sensitivity

## Binary and Compressed Data

### .hdf5 / .h5 - Hierarchical Data Format 5
**Description:** Container for large scientific datasets
**Typical Data:** Multi-dimensional arrays, metadata, groups
**Use Cases:** Large datasets, multi-modal data, parallel I/O
**Python Libraries:**
- `h5py`: `h5py.File('file.h5', 'r')`
- `pytables`: Advanced HDF5 interface
- `pandas`: HDF5 storage via HDFStore
**EDA Approach:**
- Group and dataset hierarchy
- Dataset shapes and dtypes
- Attributes and metadata
- Compression and chunking strategy
- Memory-efficient sampling
- Dataset relationships
- File size and efficiency
- Access patterns optimization

### .zarr - Chunked Array Storage
**Description:** Cloud-optimized chunked arrays
**Typical Data:** Large N-dimensional arrays
**Use Cases:** Cloud storage, parallel computing, streaming
**Python Libraries:**
- `zarr`: `zarr.open('file.zarr')`
- `xarray`: Zarr backend support
**EDA Approach:**
- Array metadata and dimensions
- Chunk size optimization
- Compression codec and ratio
- Synchronizer and store type
- Multi-scale hierarchies
- Parallel access performance
- Attribute metadata

### .gz / .gzip - Gzip Compressed
**Description:** Compressed data files
**Typical Data:** Any compressed text or binary
**Use Cases:** Compression for storage/transfer
**Python Libraries:**
- `gzip`: Built-in gzip module
- `pandas`: Automatic gzip handling in read functions
**EDA Approach:**
- Compression ratio
- Original file type detection
- Decompression validation
- Header information
- Multi-member archives

### .bz2 - Bzip2 Compressed
**Description:** Bzip2 compression
**Typical Data:** Highly compressed files
**Use Cases:** Better compression than gzip
**Python Libraries:**
- `bz2`: Built-in bz2 module
- Automatic handling in pandas
**EDA Approach:**
- Compression efficiency
- Decompression time
- Content validation

### .zip - ZIP Archive
**Description:** Archive with multiple files
**Typical Data:** Collections of files
**Use Cases:** File distribution, archiving
**Python Libraries:**
- `zipfile`: Built-in ZIP support
- `pandas`: Can read zipped CSVs
**EDA Approach:**
- Archive member listing
- Compression method per file
- Total vs compressed size
- Directory structure
- File type distribution
- Extraction validation

### .tar / .tar.gz - TAR Archive
**Description:** Unix tape archive
**Typical Data:** Multiple files and directories
**Use Cases:** Software distribution, backups
**Python Libraries:**
- `tarfile`: Built-in TAR support
**EDA Approach:**
- Member file listing
- Compression (if .tar.gz, .tar.bz2)
- Directory structure
- Permissions preservation
- Extraction testing

## Time Series and Waveform Data

### .wav - Waveform Audio
**Description:** Audio waveform data
**Typical Data:** Acoustic signals, audio recordings
**Use Cases:** Acoustic analysis, ultrasound, signal processing
**Python Libraries:**
- `scipy.io.wavfile`: `scipy.io.wavfile.read()`
- `wave`: Built-in module
- `soundfile`: Enhanced audio I/O
**EDA Approach:**
- Sample rate and duration
- Bit depth and channels
- Amplitude distribution
- Spectral analysis (FFT)
- Signal-to-noise ratio
- Clipping detection
- Frequency content

### .mat - MATLAB Data
**Description:** MATLAB workspace variables
**Typical Data:** Arrays, structures, cells
**Use Cases:** MATLAB-Python interoperability
**Python Libraries:**
- `scipy.io`: `scipy.io.loadmat()`
- `h5py`: For MATLAB v7.3 files (HDF5-based)
- `mat73`: Pure Python for v7.3
**EDA Approach:**
- Variable names and types
- Array dimensions
- Structure field exploration
- Cell array handling
- Sparse matrix detection
- MATLAB version compatibility
- Metadata extraction

### .edf - European Data Format
**Description:** Time series data (especially medical)
**Typical Data:** EEG, physiological signals
**Use Cases:** Medical signal storage
**Python Libraries:**
- `pyedflib`: EDF/EDF+ reading and writing
- `mne`: Neurophysiology data (supports EDF)
**EDA Approach:**
- Signal count and names
- Sampling frequencies
- Signal ranges and units
- Recording duration
- Annotation events
- Data quality (saturation, noise)
- Patient/study information

### .csv (Time Series)
**Description:** CSV with timestamp column
**Typical Data:** Time-indexed measurements
**Use Cases:** Sensor data, monitoring, experiments
**Python Libraries:**
- `pandas`: `pd.read_csv()` with `parse_dates`
**EDA Approach:**
- Temporal range and resolution
- Sampling regularity
- Missing time points
- Trend and seasonality
- Stationarity tests
- Autocorrelation
- Anomaly detection

## Geospatial and Environmental Data

### .shp - Shapefile
**Description:** Geospatial vector data
**Typical Data:** Geographic features (points, lines, polygons)
**Use Cases:** GIS analysis, spatial data
**Python Libraries:**
- `geopandas`: `gpd.read_file('file.shp')`
- `fiona`: Lower-level shapefile access
- `pyshp`: Pure Python shapefile reader
**EDA Approach:**
- Geometry type and count
- Coordinate reference system
- Bounding box
- Attribute table analysis
- Geometry validity
- Spatial distribution
- Multi-part features
- Associated files (.shx, .dbf, .prj)

### .geojson - GeoJSON
**Description:** JSON format for geographic data
**Typical Data:** Features with geometry and properties
**Use Cases:** Web mapping, spatial analysis
**Python Libraries:**
- `geopandas`: Native GeoJSON support
- `json`: Parse as JSON then process
**EDA Approach:**
- Feature count and types
- CRS specification
- Bounding box calculation
- Property schema
- Geometry complexity
- Nesting structure

### .tif / .tiff (Geospatial)
**Description:** GeoTIFF with spatial reference
**Typical Data:** Satellite imagery, DEMs, rasters
**Use Cases:** Remote sensing, terrain analysis
**Python Libraries:**
- `rasterio`: `rasterio.open('file.tif')`
- `gdal`: Geospatial Data Abstraction Library
- `xarray` with `rioxarray`: N-D geospatial arrays
**EDA Approach:**
- Raster dimensions and resolution
- Band count and descriptions
- Coordinate reference system
- Geotransform parameters
- NoData value handling
- Pixel value distribution
- Histogram analysis
- Overviews and pyramids

### .nc / .netcdf - Network Common Data Form
**Description:** Self-describing array-based data
**Typical Data:** Climate, atmospheric, oceanographic data
**Use Cases:** Scientific datasets, model output
**Python Libraries:**
- `netCDF4`: `netCDF4.Dataset('file.nc')`
- `xarray`: `xr.open_dataset('file.nc')`
**EDA Approach:**
- Variable enumeration
- Dimension analysis
- Time series properties
- Spatial coverage
- Attribute metadata (CF conventions)
- Coordinate systems
- Chunking and compression
- Data quality flags

### .grib / .grib2 - Gridded Binary
**Description:** Meteorological data format
**Typical Data:** Weather forecasts, climate data
**Use Cases:** Numerical weather prediction
**Python Libraries:**
- `pygrib`: GRIB file reading
- `xarray` with `cfgrib`: GRIB to xarray
**EDA Approach:**
- Message inventory
- Parameter and level types
- Spatial grid specification
- Temporal coverage
- Ensemble members
- Forecast vs analysis
- Data packing and precision

### .hdf4 - HDF4 Format
**Description:** Older HDF format
**Typical Data:** NASA Earth Science data
**Use Cases:** Satellite data (MODIS, etc.)
**Python Libraries:**
- `pyhdf`: HDF4 access
- `gdal`: Can read HDF4
**EDA Approach:**
- Scientific dataset listing
- Vdata and attributes
- Dimension scales
- Metadata extraction
- Quality flags
- Conversion to HDF5 or NetCDF

## Specialized Scientific Formats

### .fits - Flexible Image Transport System
**Description:** Astronomy data format
**Typical Data:** Images, tables, spectra from telescopes
**Use Cases:** Astronomical observations
**Python Libraries:**
- `astropy.io.fits`: `fits.open('file.fits')`
- `fitsio`: Alternative FITS library
**EDA Approach:**
- HDU (Header Data Unit) structure
- Image dimensions and WCS
- Header keyword analysis
- Table column descriptions
- Data type and scaling
- FITS convention compliance
- Checksum validation

### .asdf - Advanced Scientific Data Format
**Description:** Next-gen data format for astronomy
**Typical Data:** Complex hierarchical scientific data
**Use Cases:** James Webb Space Telescope data
**Python Libraries:**
- `asdf`: `asdf.open('file.asdf')`
**EDA Approach:**
- Tree structure exploration
- Schema validation
- Internal vs external arrays
- Compression methods
- YAML metadata
- Version compatibility

### .root - ROOT Data Format
**Description:** CERN ROOT framework format
**Typical Data:** High-energy physics data
**Use Cases:** Particle physics experiments
**Python Libraries:**
- `uproot`: Pure Python ROOT reading
- `ROOT`: Official PyROOT bindings
**EDA Approach:**
- TTree structure
- Branch types and entries
- Histogram inventory
- Event loop statistics
- File compression
- Split level analysis

### .txt - Plain Text Data
**Description:** Generic text-based data
**Typical Data:** Tab/space-delimited, custom formats
**Use Cases:** Simple data exchange, logs
**Python Libraries:**
- `pandas`: `pd.read_csv()` with custom delimiters
- `numpy`: `np.loadtxt()`, `np.genfromtxt()`
- Built-in file reading
**EDA Approach:**
- Format detection (delimiter, header)
- Data type inference
- Comment line handling
- Missing value codes
- Column alignment
- Encoding detection

### .dat - Generic Data File
**Description:** Binary or text data
**Typical Data:** Instrument output, custom formats
**Use Cases:** Various scientific instruments
**Python Libraries:**
- Format-specific: requires knowledge of structure
- `numpy`: `np.fromfile()` for binary
- `struct`: Parse binary structures
**EDA Approach:**
- Binary vs text determination
- Header detection
- Record structure inference
- Endianness
- Data type patterns
- Validation with documentation

### .log - Log Files
**Description:** Text logs from software/instruments
**Typical Data:** Timestamped events, messages
**Use Cases:** Troubleshooting, experiment tracking
**Python Libraries:**
- Built-in file reading
- `pandas`: Structured log parsing
- Regular expressions for parsing
**EDA Approach:**
- Log level distribution
- Timestamp parsing
- Error and warning frequency
- Event sequencing
- Pattern recognition
- Anomaly detection
- Session boundaries

---

## Reference: Microscopy_Imaging_Formats

# Microscopy and Imaging File Formats Reference

This reference covers file formats used in microscopy, medical imaging, remote sensing, and scientific image analysis.

## Microscopy-Specific Formats

### .tif / .tiff - Tagged Image File Format
**Description:** Flexible image format supporting multiple pages and metadata
**Typical Data:** Microscopy images, z-stacks, time series, multi-channel
**Use Cases:** Fluorescence microscopy, confocal imaging, biological imaging
**Python Libraries:**
- `tifffile`: `tifffile.imread('file.tif')` - Microscopy TIFF support
- `PIL/Pillow`: `Image.open('file.tif')` - Basic TIFF
- `scikit-image`: `io.imread('file.tif')`
- `AICSImageIO`: Multi-format microscopy reader
**EDA Approach:**
- Image dimensions and bit depth
- Multi-page/z-stack analysis
- Metadata extraction (OME-TIFF)
- Channel analysis and intensity distributions
- Temporal dynamics (time-lapse)
- Pixel size and spatial calibration
- Histogram analysis per channel
- Dynamic range utilization

### .nd2 - Nikon NIS-Elements
**Description:** Proprietary Nikon microscope format
**Typical Data:** Multi-dimensional microscopy (XYZCT)
**Use Cases:** Nikon microscope data, confocal, widefield
**Python Libraries:**
- `nd2reader`: `ND2Reader('file.nd2')`
- `pims`: `pims.ND2_Reader('file.nd2')`
- `AICSImageIO`: Universal reader
**EDA Approach:**
- Experiment metadata extraction
- Channel configurations
- Time-lapse frame analysis
- Z-stack depth and spacing
- XY stage positions
- Laser settings and power
- Pixel binning information
- Acquisition timestamps

### .lif - Leica Image Format
**Description:** Leica microscope proprietary format
**Typical Data:** Multi-experiment, multi-dimensional images
**Use Cases:** Leica confocal and widefield data
**Python Libraries:**
- `readlif`: `readlif.LifFile('file.lif')`
- `AICSImageIO`: LIF support
- `python-bioformats`: Via Bio-Formats
**EDA Approach:**
- Multiple experiment detection
- Image series enumeration
- Metadata per experiment
- Channel and timepoint structure
- Physical dimensions extraction
- Objective and detector information
- Scan settings analysis

### .czi - Carl Zeiss Image
**Description:** Zeiss microscope format
**Typical Data:** Multi-dimensional microscopy with rich metadata
**Use Cases:** Zeiss confocal, lightsheet, widefield
**Python Libraries:**
- `czifile`: `czifile.CziFile('file.czi')`
- `AICSImageIO`: CZI support
- `pylibCZIrw`: Official Zeiss library
**EDA Approach:**
- Scene and position analysis
- Mosaic tile structure
- Channel wavelength information
- Acquisition mode detection
- Scaling and calibration
- Instrument configuration
- ROI definitions

### .oib / .oif - Olympus Image Format
**Description:** Olympus microscope formats
**Typical Data:** Confocal and multiphoton imaging
**Use Cases:** Olympus FluoView data
**Python Libraries:**
- `AICSImageIO`: OIB/OIF support
- `python-bioformats`: Via Bio-Formats
**EDA Approach:**
- Directory structure validation (OIF)
- Metadata file parsing
- Channel configuration
- Scan parameters
- Objective and filter information
- PMT settings

### .vsi - Olympus VSI
**Description:** Olympus slide scanner format
**Typical Data:** Whole slide imaging, large mosaics
**Use Cases:** Virtual microscopy, pathology
**Python Libraries:**
- `openslide-python`: `openslide.OpenSlide('file.vsi')`
- `AICSImageIO`: VSI support
**EDA Approach:**
- Pyramid level analysis
- Tile structure and overlap
- Macro and label images
- Magnification levels
- Whole slide statistics
- Region detection

### .ims - Imaris Format
**Description:** Bitplane Imaris HDF5-based format
**Typical Data:** Large 3D/4D microscopy datasets
**Use Cases:** 3D rendering, time-lapse analysis
**Python Libraries:**
- `h5py`: Direct HDF5 access
- `imaris_ims_file_reader`: Specialized reader
**EDA Approach:**
- Resolution level analysis
- Time point structure
- Channel organization
- Dataset hierarchy
- Thumbnail generation
- Memory-mapped access strategies
- Chunking optimization

### .lsm - Zeiss LSM
**Description:** Legacy Zeiss confocal format
**Typical Data:** Confocal laser scanning microscopy
**Use Cases:** Older Zeiss confocal data
**Python Libraries:**
- `tifffile`: LSM support (TIFF-based)
- `python-bioformats`: LSM reading
**EDA Approach:**
- Similar to TIFF with LSM-specific metadata
- Scan speed and resolution
- Laser lines and power
- Detector gain and offset
- LUT information

### .stk - MetaMorph Stack
**Description:** MetaMorph image stack format
**Typical Data:** Time-lapse or z-stack sequences
**Use Cases:** MetaMorph software output
**Python Libraries:**
- `tifffile`: STK is TIFF-based
- `python-bioformats`: STK support
**EDA Approach:**
- Stack dimensionality
- Plane metadata
- Timing information
- Stage positions
- UIC tags parsing

### .dv - DeltaVision
**Description:** Applied Precision DeltaVision format
**Typical Data:** Deconvolution microscopy
**Use Cases:** DeltaVision microscope data
**Python Libraries:**
- `mrc`: Can read DV (MRC-related)
- `AICSImageIO`: DV support
**EDA Approach:**
- Wave information (channels)
- Extended header analysis
- Lens and magnification
- Deconvolution status
- Time stamps per section

### .mrc - Medical Research Council
**Description:** Electron microscopy format
**Typical Data:** EM images, cryo-EM, tomography
**Use Cases:** Structural biology, electron microscopy
**Python Libraries:**
- `mrcfile`: `mrcfile.open('file.mrc')`
- `EMAN2`: EM-specific tools
**EDA Approach:**
- Volume dimensions
- Voxel size and units
- Origin and map statistics
- Symmetry information
- Extended header analysis
- Density statistics
- Header consistency validation

### .dm3 / .dm4 - Gatan Digital Micrograph
**Description:** Gatan TEM/STEM format
**Typical Data:** Transmission electron microscopy
**Use Cases:** TEM imaging and analysis
**Python Libraries:**
- `hyperspy`: `hs.load('file.dm3')`
- `ncempy`: `ncempy.io.dm.dmReader('file.dm3')`
**EDA Approach:**
- Microscope parameters
- Energy dispersive spectroscopy data
- Diffraction patterns
- Calibration information
- Tag structure analysis
- Image series handling

### .eer - Electron Event Representation
**Description:** Direct electron detector format
**Typical Data:** Electron counting data from detectors
**Use Cases:** Cryo-EM data collection
**Python Libraries:**
- `mrcfile`: Some EER support
- Vendor-specific tools (Gatan, TFS)
**EDA Approach:**
- Event counting statistics
- Frame rate and dose
- Detector configuration
- Motion correction assessment
- Gain reference validation

### .ser - TIA Series
**Description:** FEI/TFS TIA format
**Typical Data:** EM image series
**Use Cases:** FEI/Thermo Fisher EM data
**Python Libraries:**
- `hyperspy`: SER support
- `ncempy`: TIA reader
**EDA Approach:**
- Series structure
- Calibration data
- Acquisition metadata
- Time stamps
- Multi-dimensional data organization

## Medical and Biological Imaging

### .dcm - DICOM
**Description:** Digital Imaging and Communications in Medicine
**Typical Data:** Medical images with patient/study metadata
**Use Cases:** Clinical imaging, radiology, CT, MRI, PET
**Python Libraries:**
- `pydicom`: `pydicom.dcmread('file.dcm')`
- `SimpleITK`: `sitk.ReadImage('file.dcm')`
- `nibabel`: Limited DICOM support
**EDA Approach:**
- Patient metadata extraction (anonymization check)
- Modality-specific analysis
- Series and study organization
- Slice thickness and spacing
- Window/level settings
- Hounsfield units (CT)
- Image orientation and position
- Multi-frame analysis

### .nii / .nii.gz - NIfTI
**Description:** Neuroimaging Informatics Technology Initiative
**Typical Data:** Brain imaging, fMRI, structural MRI
**Use Cases:** Neuroimaging research, brain analysis
**Python Libraries:**
- `nibabel`: `nibabel.load('file.nii')`
- `nilearn`: Neuroimaging with ML
- `SimpleITK`: NIfTI support
**EDA Approach:**
- Volume dimensions and voxel size
- Affine transformation matrix
- Time series analysis (fMRI)
- Intensity distribution
- Brain extraction quality
- Registration assessment
- Orientation validation
- Header information consistency

### .mnc - MINC Format
**Description:** Medical Image NetCDF
**Typical Data:** Medical imaging (predecessor to NIfTI)
**Use Cases:** Legacy neuroimaging data
**Python Libraries:**
- `pyminc`: MINC-specific tools
- `nibabel`: MINC support
**EDA Approach:**
- Similar to NIfTI
- NetCDF structure exploration
- Dimension ordering
- Metadata extraction

### .nrrd - Nearly Raw Raster Data
**Description:** Medical imaging format with detached header
**Typical Data:** Medical images, research imaging
**Use Cases:** 3D Slicer, ITK-based applications
**Python Libraries:**
- `pynrrd`: `nrrd.read('file.nrrd')`
- `SimpleITK`: NRRD support
**EDA Approach:**
- Header field analysis
- Encoding format
- Dimension and spacing
- Orientation matrix
- Compression assessment
- Endianness handling

### .mha / .mhd - MetaImage
**Description:** MetaImage format (ITK)
**Typical Data:** Medical/scientific 3D images
**Use Cases:** ITK/SimpleITK applications
**Python Libraries:**
- `SimpleITK`: Native MHA/MHD support
- `itk`: Direct ITK integration
**EDA Approach:**
- Header-data file pairing (MHD)
- Transform matrix
- Element spacing
- Compression format
- Data type and dimensions

### .hdr / .img - Analyze Format
**Description:** Legacy medical imaging format
**Typical Data:** Brain imaging (pre-NIfTI)
**Use Cases:** Old neuroimaging datasets
**Python Libraries:**
- `nibabel`: Analyze support
- Conversion to NIfTI recommended
**EDA Approach:**
- Header-image pairing validation
- Byte order issues
- Conversion to modern formats
- Metadata limitations

## Scientific Image Formats

### .png - Portable Network Graphics
**Description:** Lossless compressed image format
**Typical Data:** 2D images, screenshots, processed data
**Use Cases:** Publication figures, lossless storage
**Python Libraries:**
- `PIL/Pillow`: `Image.open('file.png')`
- `scikit-image`: `io.imread('file.png')`
- `imageio`: `imageio.imread('file.png')`
**EDA Approach:**
- Bit depth analysis (8-bit, 16-bit)
- Color mode (grayscale, RGB, palette)
- Metadata (PNG chunks)
- Transparency handling
- Compression efficiency
- Histogram analysis

### .jpg / .jpeg - Joint Photographic Experts Group
**Description:** Lossy compressed image format
**Typical Data:** Natural images, photos
**Use Cases:** Visualization, web graphics (not raw data)
**Python Libraries:**
- `PIL/Pillow`: Standard JPEG support
- `scikit-image`: JPEG reading
**EDA Approach:**
- Compression artifacts detection
- Quality factor estimation
- Color space (RGB, grayscale)
- EXIF metadata
- Quantization table analysis
- Note: Not suitable for quantitative analysis

### .bmp - Bitmap Image
**Description:** Uncompressed raster image
**Typical Data:** Simple images, screenshots
**Use Cases:** Compatibility, simple storage
**Python Libraries:**
- `PIL/Pillow`: BMP support
- `scikit-image`: BMP reading
**EDA Approach:**
- Color depth
- Palette analysis (if indexed)
- File size efficiency
- Pixel format validation

### .gif - Graphics Interchange Format
**Description:** Image format with animation support
**Typical Data:** Animated images, simple graphics
**Use Cases:** Animations, time-lapse visualization
**Python Libraries:**
- `PIL/Pillow`: GIF support
- `imageio`: Better GIF animation support
**EDA Approach:**
- Frame count and timing
- Palette limitations (256 colors)
- Loop count
- Disposal method
- Transparency handling

### .svg - Scalable Vector Graphics
**Description:** XML-based vector graphics
**Typical Data:** Vector drawings, plots, diagrams
**Use Cases:** Publication-quality figures, plots
**Python Libraries:**
- `svgpathtools`: Path manipulation
- `cairosvg`: Rasterization
- `lxml`: XML parsing
**EDA Approach:**
- Element structure analysis
- Style information
- Viewbox and dimensions
- Path complexity
- Text element extraction
- Layer organization

### .eps - Encapsulated PostScript
**Description:** Vector graphics format
**Typical Data:** Publication figures
**Use Cases:** Legacy publication graphics
**Python Libraries:**
- `PIL/Pillow`: Basic EPS rasterization
- `ghostscript` via subprocess
**EDA Approach:**
- Bounding box information
- Preview image validation
- Font embedding
- Conversion to modern formats

### .pdf (Images)
**Description:** Portable Document Format with images
**Typical Data:** Publication figures, multi-page documents
**Use Cases:** Publication, data presentation
**Python Libraries:**
- `PyMuPDF/fitz`: `fitz.open('file.pdf')`
- `pdf2image`: Rasterization
- `pdfplumber`: Text and layout extraction
**EDA Approach:**
- Page count
- Image extraction
- Resolution and DPI
- Embedded fonts and metadata
- Compression methods
- Image vs vector content

### .fig - MATLAB Figure
**Description:** MATLAB figure file
**Typical Data:** MATLAB plots and figures
**Use Cases:** MATLAB data visualization
**Python Libraries:**
- Custom parsers (MAT file structure)
- Conversion to other formats
**EDA Approach:**
- Figure structure
- Data extraction from plots
- Axes and label information
- Plot type identification

### .hdf5 (Imaging Specific)
**Description:** HDF5 for large imaging datasets
**Typical Data:** High-content screening, large microscopy
**Use Cases:** BigDataViewer, large-scale imaging
**Python Libraries:**
- `h5py`: Universal HDF5 access
- Imaging-specific readers (BigDataViewer)
**EDA Approach:**
- Dataset hierarchy
- Chunk and compression strategy
- Multi-resolution pyramid
- Metadata organization
- Memory-mapped access
- Parallel I/O performance

### .zarr - Chunked Array Storage
**Description:** Cloud-optimized array storage
**Typical Data:** Large imaging datasets, OME-ZARR
**Use Cases:** Cloud microscopy, large-scale analysis
**Python Libraries:**
- `zarr`: `zarr.open('file.zarr')`
- `ome-zarr-py`: OME-ZARR support
**EDA Approach:**
- Chunk size optimization
- Compression codec analysis
- Multi-scale representation
- Array dimensions and dtype
- Metadata structure (OME)
- Cloud access patterns

### .raw - Raw Image Data
**Description:** Unformatted binary pixel data
**Typical Data:** Raw detector output
**Use Cases:** Custom imaging systems
**Python Libraries:**
- `numpy`: `np.fromfile()` with dtype
- `imageio`: Raw format plugins
**EDA Approach:**
- Dimensions determination (external info needed)
- Byte order and data type
- Header presence detection
- Pixel value range
- Noise characteristics

### .bin - Binary Image Data
**Description:** Generic binary image format
**Typical Data:** Raw or custom-formatted images
**Use Cases:** Instrument-specific outputs
**Python Libraries:**
- `numpy`: Custom binary reading
- `struct`: For structured binary data
**EDA Approach:**
- Format specification required
- Header parsing (if present)
- Data type inference
- Dimension extraction
- Validation with known parameters

## Image Analysis Formats

### .roi - ImageJ ROI
**Description:** ImageJ region of interest format
**Typical Data:** Geometric ROIs, selections
**Use Cases:** ImageJ/Fiji analysis workflows
**Python Libraries:**
- `read-roi`: `read_roi.read_roi_file('file.roi')`
- `roifile`: ROI manipulation
**EDA Approach:**
- ROI type analysis (rectangle, polygon, etc.)
- Coordinate extraction
- ROI properties (area, perimeter)
- Group analysis (ROI sets)
- Z-position and time information

### .zip (ROI sets)
**Description:** ZIP archive of ImageJ ROIs
**Typical Data:** Multiple ROI files
**Use Cases:** Batch ROI analysis
**Python Libraries:**
- `read-roi`: `read_roi.read_roi_zip('file.zip')`
- Standard `zipfile` module
**EDA Approach:**
- ROI count in set
- ROI type distribution
- Spatial distribution
- Overlapping ROI detection
- Naming conventions

### .ome.tif / .ome.tiff - OME-TIFF
**Description:** TIFF with OME-XML metadata
**Typical Data:** Standardized microscopy with rich metadata
**Use Cases:** Bio-Formats compatible storage
**Python Libraries:**
- `tifffile`: OME-TIFF support
- `AICSImageIO`: OME reading
- `python-bioformats`: Bio-Formats integration
**EDA Approach:**
- OME-XML validation
- Physical dimensions extraction
- Channel naming and wavelengths
- Plane positions (Z, C, T)
- Instrument metadata
- Bio-Formats compatibility

### .ome.zarr - OME-ZARR
**Description:** OME-NGFF specification on ZARR
**Typical Data:** Next-generation file format for bioimaging
**Use Cases:** Cloud-native imaging, large datasets
**Python Libraries:**
- `ome-zarr-py`: Official implementation
- `zarr`: Underlying array storage
**EDA Approach:**
- Multiscale resolution levels
- Metadata compliance with OME-NGFF spec
- Coordinate transformations
- Label and ROI handling
- Cloud storage optimization
- Chunk access patterns

### .klb - Keller Lab Block
**Description:** Fast microscopy format for large data
**Typical Data:** Lightsheet microscopy, time-lapse
**Use Cases:** High-throughput imaging
**Python Libraries:**
- `pyklb`: KLB reading and writing
**EDA Approach:**
- Compression efficiency
- Block structure
- Multi-resolution support
- Read performance benchmarking
- Metadata extraction

### .vsi - Whole Slide Imaging
**Description:** Virtual slide format (multiple vendors)
**Typical Data:** Pathology slides, large mosaics
**Use Cases:** Digital pathology
**Python Libraries:**
- `openslide-python`: Multi-format WSI
- `tiffslide`: Pure Python alternative
**EDA Approach:**
- Pyramid level count
- Downsampling factors
- Associated images (macro, label)
- Tile size and overlap
- MPP (microns per pixel)
- Background detection
- Tissue segmentation

### .ndpi - Hamamatsu NanoZoomer
**Description:** Hamamatsu slide scanner format
**Typical Data:** Whole slide pathology images
**Use Cases:** Digital pathology workflows
**Python Libraries:**
- `openslide-python`: NDPI support
**EDA Approach:**
- Multi-resolution pyramid
- Lens and objective information
- Scan area and magnification
- Focal plane information
- Tissue detection

### .svs - Aperio ScanScope
**Description:** Aperio whole slide format
**Typical Data:** Digital pathology slides
**Use Cases:** Pathology image analysis
**Python Libraries:**
- `openslide-python`: SVS support
**EDA Approach:**
- Pyramid structure
- MPP calibration
- Label and macro images
- Compression quality
- Thumbnail generation

### .scn - Leica SCN
**Description:** Leica slide scanner format
**Typical Data:** Whole slide imaging
**Use Cases:** Digital pathology
**Python Libraries:**
- `openslide-python`: SCN support
**EDA Approach:**
- Tile structure analysis
- Collection organization
- Metadata extraction
- Magnification levels

---

## Reference: Proteomics_Metabolomics_Formats

# Proteomics and Metabolomics File Formats Reference

This reference covers file formats specific to proteomics, metabolomics, lipidomics, and related omics workflows.

## Mass Spectrometry-Based Proteomics

### .mzML - Mass Spectrometry Markup Language
**Description:** Standard XML format for MS data
**Typical Data:** MS1 and MS2 spectra, retention times, intensities
**Use Cases:** Proteomics, metabolomics pipelines
**Python Libraries:**
- `pymzml`: `pymzml.run.Reader('file.mzML')`
- `pyteomics.mzml`: `pyteomics.mzml.read('file.mzML')`
- `pyopenms`: OpenMS Python bindings
**EDA Approach:**
- Scan count and MS level distribution
- Total ion chromatogram (TIC) analysis
- Base peak chromatogram (BPC)
- m/z coverage and resolution
- Retention time range
- Precursor selection patterns
- Data completeness
- Quality control metrics (lock mass, standards)

### .mzXML - Legacy MS XML Format
**Description:** Older XML-based MS format
**Typical Data:** Mass spectra with metadata
**Use Cases:** Legacy proteomics data
**Python Libraries:**
- `pyteomics.mzxml`
- `pymzml`: Can read mzXML
**EDA Approach:**
- Similar to mzML
- Format version compatibility
- Conversion quality validation
- Metadata preservation check

### .mzIdentML - Peptide Identification Format
**Description:** PSI standard for peptide identifications
**Typical Data:** Peptide-spectrum matches, proteins, scores
**Use Cases:** Search engine results, proteomics workflows
**Python Libraries:**
- `pyteomics.mzid`
- `pyopenms`: MzIdentML support
**EDA Approach:**
- PSM count and score distribution
- FDR calculation and filtering
- Modification analysis
- Missed cleavage statistics
- Protein inference results
- Search parameters validation
- Decoy hit analysis
- Rank-1 vs lower ranks

### .pepXML - Trans-Proteomic Pipeline Peptide XML
**Description:** TPP format for peptide identifications
**Typical Data:** Search results with statistical validation
**Use Cases:** Proteomics database search output
**Python Libraries:**
- `pyteomics.pepxml`
**EDA Approach:**
- Search engine comparison
- Score distributions (XCorr, expect value, etc.)
- Charge state analysis
- Modification frequencies
- PeptideProphet probabilities
- Protein coverage
- Spectral counting

### .protXML - Protein Inference Results
**Description:** TPP protein-level identifications
**Typical Data:** Protein groups, probabilities, peptides
**Use Cases:** Protein-level analysis
**Python Libraries:**
- `pyteomics.protxml`
**EDA Approach:**
- Protein group statistics
- Parsimonious protein sets
- ProteinProphet probabilities
- Coverage and peptide count per protein
- Unique vs shared peptides
- Protein molecular weight distribution
- GO term enrichment preparation

### .pride.xml - PRIDE XML Format
**Description:** Proteomics Identifications Database format
**Typical Data:** Complete proteomics experiment data
**Use Cases:** Public data deposition (legacy)
**Python Libraries:**
- `pyteomics.pride`
- Custom XML parsers
**EDA Approach:**
- Experiment metadata extraction
- Identification completeness
- Cross-linking to spectra
- Protocol information
- Instrument details

### .tsv / .csv (Proteomics)
**Description:** Tab or comma-separated proteomics results
**Typical Data:** Peptide or protein quantification tables
**Use Cases:** MaxQuant, Proteome Discoverer, Skyline output
**Python Libraries:**
- `pandas`: `pd.read_csv()` or `pd.read_table()`
**EDA Approach:**
- Identification counts
- Quantitative value distributions
- Missing value patterns
- Intensity-based analysis
- Label-free quantification assessment
- Isobaric tag ratio analysis
- Coefficient of variation
- Batch effects

### .msf - Thermo MSF Database
**Description:** Proteome Discoverer results database
**Typical Data:** SQLite database with search results
**Use Cases:** Thermo Proteome Discoverer workflows
**Python Libraries:**
- `sqlite3`: Database access
- Custom MSF parsers
**EDA Approach:**
- Database schema exploration
- Peptide and protein tables
- Score thresholds
- Quantification data
- Processing node information
- Confidence levels

### .pdResult - Proteome Discoverer Result
**Description:** Proteome Discoverer study results
**Typical Data:** Comprehensive search and quantification
**Use Cases:** PD study exports
**Python Libraries:**
- Vendor tools for conversion
- Export to TSV for Python analysis
**EDA Approach:**
- Study design validation
- Result filtering criteria
- Quantitative comparison groups
- Imputation strategies

### .pep.xml - Peptide Summary
**Description:** Compact peptide identification format
**Typical Data:** Peptide sequences, modifications, scores
**Use Cases:** Downstream analysis input
**Python Libraries:**
- `pyteomics`: XML parsing
**EDA Approach:**
- Unique peptide counting
- PTM site localization
- Retention time predictability
- Charge state preferences

## Quantitative Proteomics

### .sky - Skyline Document
**Description:** Skyline targeted proteomics document
**Typical Data:** Transition lists, chromatograms, results
**Use Cases:** Targeted proteomics (SRM/MRM/PRM)
**Python Libraries:**
- `skyline`: Python API (limited)
- Export to CSV for analysis
**EDA Approach:**
- Transition selection validation
- Chromatographic peak quality
- Interference detection
- Retention time consistency
- Calibration curve assessment
- Replicate correlation
- LOD/LOQ determination

### .sky.zip - Zipped Skyline Document
**Description:** Skyline document with external files
**Typical Data:** Complete Skyline analysis
**Use Cases:** Sharing Skyline projects
**Python Libraries:**
- `zipfile`: Extract for processing
**EDA Approach:**
- Document structure
- External file references
- Result export and analysis

### .wiff - SCIEX WIFF Format
**Description:** SCIEX instrument data with quantitation
**Typical Data:** LC-MS/MS with MRM transitions
**Use Cases:** SCIEX QTRAP, TripleTOF data
**Python Libraries:**
- Vendor tools (limited Python access)
- Conversion to mzML
**EDA Approach:**
- MRM transition performance
- Dwell time optimization
- Cycle time analysis
- Peak integration quality

### .raw (Thermo)
**Description:** Thermo raw instrument file
**Typical Data:** Full MS data from Orbitrap, Q Exactive
**Use Cases:** Label-free and TMT quantification
**Python Libraries:**
- `pymsfilereader`: Thermo RawFileReader
- `ThermoRawFileParser`: Cross-platform CLI
**EDA Approach:**
- MS1 and MS2 acquisition rates
- AGC target and fill times
- Resolution settings
- Isolation window validation
- SPS ion selection (TMT)
- Contamination assessment

### .d (Agilent)
**Description:** Agilent data directory
**Typical Data:** LC-MS and GC-MS data
**Use Cases:** Agilent instrument workflows
**Python Libraries:**
- Community parsers
- Export to mzML
**EDA Approach:**
- Method consistency
- Calibration status
- Sequence run information
- Retention time stability

## Metabolomics and Lipidomics

### .mzML (Metabolomics)
**Description:** Standard MS format for metabolomics
**Typical Data:** Full scan MS, targeted MS/MS
**Use Cases:** Untargeted and targeted metabolomics
**Python Libraries:**
- Same as proteomics mzML tools
**EDA Approach:**
- Feature detection quality
- Mass accuracy assessment
- Retention time alignment
- Blank subtraction
- QC sample consistency
- Isotope pattern validation
- Adduct formation analysis
- In-source fragmentation check

### .cdf / .netCDF - ANDI-MS
**Description:** Analytical Data Interchange for MS
**Typical Data:** GC-MS, LC-MS chromatography data
**Use Cases:** Metabolomics, GC-MS workflows
**Python Libraries:**
- `netCDF4`: Low-level access
- `pyopenms`: CDF support
- `xcms` via R integration
**EDA Approach:**
- TIC and extracted ion chromatograms
- Peak detection across samples
- Retention index calculation
- Mass spectral matching
- Library search preparation

### .msp - Mass Spectral Format (NIST)
**Description:** NIST spectral library format
**Typical Data:** Reference mass spectra
**Use Cases:** Metabolite identification, library matching
**Python Libraries:**
- `matchms`: Spectral matching
- Custom MSP parsers
**EDA Approach:**
- Library coverage
- Metadata completeness (InChI, SMILES)
- Spectral quality metrics
- Collision energy standardization
- Precursor type annotation

### .mgf (Metabolomics)
**Description:** Mascot Generic Format for MS/MS
**Typical Data:** MS/MS spectra for metabolite ID
**Use Cases:** Spectral library searching
**Python Libraries:**
- `matchms`: Metabolomics spectral analysis
- `pyteomics.mgf`
**EDA Approach:**
- Spectrum quality filtering
- Precursor isolation purity
- Fragment m/z accuracy
- Neutral loss patterns
- MS/MS completeness

### .nmrML - NMR Markup Language
**Description:** Standard XML format for NMR metabolomics
**Typical Data:** 1D/2D NMR spectra with metadata
**Use Cases:** NMR-based metabolomics
**Python Libraries:**
- `nmrml2isa`: Format conversion
- Custom XML parsers
**EDA Approach:**
- Spectral quality metrics
- Binning consistency
- Reference compound validation
- pH and temperature effects
- Metabolite identification confidence

### .json (Metabolomics)
**Description:** JSON format for metabolomics results
**Typical Data:** Feature tables, annotations, metadata
**Use Cases:** GNPS, MetaboAnalyst, web tools
**Python Libraries:**
- `json`: Standard library
- `pandas`: JSON normalization
**EDA Approach:**
- Feature annotation coverage
- GNPS clustering results
- Molecular networking statistics
- Adduct and in-source fragment linkage
- Putative identification confidence

### .txt (Metabolomics Tables)
**Description:** Tab-delimited feature tables
**Typical Data:** m/z, RT, intensities across samples
**Use Cases:** MZmine, XCMS, MS-DIAL output
**Python Libraries:**
- `pandas`: Text file reading
**EDA Approach:**
- Feature count and quality
- Missing value imputation
- Data normalization assessment
- Batch correction validation
- PCA and clustering for QC
- Fold change calculations
- Statistical test preparation

### .featureXML - OpenMS Feature Format
**Description:** OpenMS detected features
**Typical Data:** LC-MS features with quality scores
**Use Cases:** OpenMS workflows
**Python Libraries:**
- `pyopenms`: FeatureXML support
**EDA Approach:**
- Feature detection parameters
- Quality metrics per feature
- Isotope pattern fitting
- Charge state assignment
- FWHM and asymmetry

### .consensusXML - OpenMS Consensus Features
**Description:** Linked features across samples
**Typical Data:** Aligned features with group info
**Use Cases:** Multi-sample LC-MS analysis
**Python Libraries:**
- `pyopenms`: ConsensusXML reading
**EDA Approach:**
- Feature correspondence quality
- Retention time alignment
- Missing value patterns
- Intensity normalization needs
- Batch-wise feature agreement

### .idXML - OpenMS Identification Format
**Description:** Peptide/metabolite identifications
**Typical Data:** MS/MS identifications with scores
**Use Cases:** OpenMS ID workflows
**Python Libraries:**
- `pyopenms`: IdXML support
**EDA Approach:**
- Identification rate
- Score distribution
- Spectral match quality
- False discovery assessment
- Annotation transfer validation

## Lipidomics-Specific Formats

### .lcb - LipidCreator Batch
**Description:** LipidCreator transition list
**Typical Data:** Lipid transitions for targeted MS
**Use Cases:** Targeted lipidomics
**Python Libraries:**
- Export to CSV for processing
**EDA Approach:**
- Transition coverage per lipid class
- Retention time prediction
- Collision energy optimization
- Class-specific fragmentation patterns

### .mzTab - Proteomics/Metabolomics Tabular Format
**Description:** PSI tabular summary format
**Typical Data:** Protein/peptide/metabolite quantification
**Use Cases:** Publication and data sharing
**Python Libraries:**
- `pyteomics.mztab`
- `pandas` for TSV-like structure
**EDA Approach:**
- Data completeness
- Metadata section validation
- Quantification method
- Identification confidence
- Software and parameters
- Quality metrics summary

### .csv (LipidSearch, LipidMatch)
**Description:** Lipid identification results
**Typical Data:** Lipid annotations, grades, intensities
**Use Cases:** Lipidomics software output
**Python Libraries:**
- `pandas`: CSV reading
**EDA Approach:**
- Lipid class distribution
- Identification grade/confidence
- Fatty acid composition analysis
- Double bond and chain length patterns
- Intensity correlations
- Normalization to internal standards

### .sdf (Metabolomics)
**Description:** Structure data file for metabolites
**Typical Data:** Chemical structures with properties
**Use Cases:** Metabolite database creation
**Python Libraries:**
- `RDKit`: `Chem.SDMolSupplier('file.sdf')`
**EDA Approach:**
- Structure validation
- Property calculation (logP, MW, TPSA)
- Molecular formula consistency
- Tautomer enumeration
- Retention time prediction features

### .mol (Metabolomics)
**Description:** Single molecule structure files
**Typical Data:** Metabolite chemical structure
**Use Cases:** Structure-based searches
**Python Libraries:**
- `RDKit`: `Chem.MolFromMolFile('file.mol')`
**EDA Approach:**
- Structure correctness
- Stereochemistry validation
- Charge state
- Implicit hydrogen handling

## Data Processing and Analysis

### .h5 / .hdf5 (Omics)
**Description:** HDF5 for large omics datasets
**Typical Data:** Feature matrices, spectra, metadata
**Use Cases:** Large-scale studies, cloud computing
**Python Libraries:**
- `h5py`: HDF5 access
- `anndata`: For single-cell proteomics
**EDA Approach:**
- Dataset organization
- Chunking and compression
- Metadata structure
- Efficient data access patterns
- Sample and feature annotations

### .Rdata / .rds - R Objects
**Description:** Serialized R analysis objects
**Typical Data:** Processed omics results from R packages
**Use Cases:** xcms, CAMERA, MSnbase workflows
**Python Libraries:**
- `pyreadr`: `pyreadr.read_r('file.Rdata')`
- `rpy2`: R-Python integration
**EDA Approach:**
- Object structure exploration
- Data extraction
- Method parameter review
- Conversion to Python-native formats

### .mzTab-M - Metabolomics mzTab
**Description:** mzTab specific to metabolomics
**Typical Data:** Small molecule quantification
**Use Cases:** Metabolomics data sharing
**Python Libraries:**
- `pyteomics.mztab`: Can parse mzTab-M
**EDA Approach:**
- Small molecule evidence
- Feature quantification
- Database references (HMDB, KEGG, etc.)
- Adduct and charge annotation
- MS level information

### .parquet (Omics)
**Description:** Columnar storage for large tables
**Typical Data:** Feature matrices, metadata
**Use Cases:** Efficient big data omics
**Python Libraries:**
- `pandas`: `pd.read_parquet()`
- `pyarrow`: Direct parquet access
**EDA Approach:**
- Compression efficiency
- Column-wise statistics
- Partition structure
- Schema validation
- Fast filtering and aggregation

### .pkl (Omics Models)
**Description:** Pickled Python objects
**Typical Data:** ML models, processed data
**Use Cases:** Workflow intermediate storage
**Python Libraries:**
- `pickle`: Standard serialization
- `joblib`: Enhanced pickling
**EDA Approach:**
- Object type and structure
- Model parameters
- Feature importance (if ML model)
- Data shapes and types
- Deserialization validation

### .zarr (Omics)
**Description:** Chunked, compressed array storage
**Typical Data:** Multi-dimensional omics data
**Use Cases:** Cloud-optimized analysis
**Python Libraries:**
- `zarr`: Array storage
**EDA Approach:**
- Chunk optimization
- Compression codecs
- Multi-scale data
- Parallel access patterns
- Metadata annotations

---

## Reference: Spectroscopy_Analytical_Formats

# Spectroscopy and Analytical Chemistry File Formats Reference

This reference covers file formats used in various spectroscopic techniques and analytical chemistry instrumentation.

## NMR Spectroscopy

### .fid - NMR Free Induction Decay
**Description:** Raw time-domain NMR data from Bruker, Agilent, JEOL
**Typical Data:** Complex time-domain signal
**Use Cases:** NMR spectroscopy, structure elucidation
**Python Libraries:**
- `nmrglue`: `nmrglue.bruker.read_fid('fid')` or `nmrglue.varian.read_fid('fid')`
- `nmrstarlib`: NMR data handling
**EDA Approach:**
- Time-domain signal decay
- Sampling rate and acquisition time
- Number of data points
- Signal-to-noise ratio estimation
- Baseline drift assessment
- Digital filter effects
- Acquisition parameter validation
- Apodization function selection

### .ft / .ft1 / .ft2 - NMR Frequency Domain
**Description:** Fourier-transformed NMR spectrum
**Typical Data:** Processed frequency-domain data
**Use Cases:** NMR analysis, peak integration
**Python Libraries:**
- `nmrglue`: Frequency domain reading
- Custom processing pipelines
**EDA Approach:**
- Peak picking and integration
- Chemical shift range
- Baseline correction quality
- Phase correction assessment
- Reference peak identification
- Spectral resolution
- Artifacts detection
- Multiplicity analysis

### .1r / .2rr - Bruker NMR Processed Data
**Description:** Bruker processed spectrum (real part)
**Typical Data:** 1D or 2D processed NMR spectra
**Use Cases:** NMR data analysis with Bruker software
**Python Libraries:**
- `nmrglue`: Bruker format support
**EDA Approach:**
- Processing parameters review
- Window function effects
- Zero-filling assessment
- Linear prediction validation
- Spectral artifacts

### .dx - NMR JCAMP-DX
**Description:** JCAMP-DX format for NMR
**Typical Data:** Standardized NMR spectrum
**Use Cases:** Data exchange between software
**Python Libraries:**
- `jcamp`: JCAMP reader
- `nmrglue`: Can import JCAMP
**EDA Approach:**
- Format compliance
- Metadata completeness
- Peak table validation
- Integration values
- Compound identification info

### .mnova - Mnova Format
**Description:** Mestrelab Research Mnova format
**Typical Data:** NMR data with processing info
**Use Cases:** Mnova software workflows
**Python Libraries:**
- `nmrglue`: Limited Mnova support
- Conversion tools to standard formats
**EDA Approach:**
- Multi-spectrum handling
- Processing pipeline review
- Quantification data
- Structure assignment

## Mass Spectrometry

### .mzML - Mass Spectrometry Markup Language
**Description:** Standard XML-based MS format
**Typical Data:** MS spectra, chromatograms, metadata
**Use Cases:** Proteomics, metabolomics, lipidomics
**Python Libraries:**
- `pymzml`: `pymzml.run.Reader('file.mzML')`
- `pyteomics.mzml`: `pyteomics.mzml.read('file.mzML')`
- `MSFileReader`: Various wrappers
**EDA Approach:**
- Scan count and MS level distribution
- Retention time range and TIC
- m/z range and resolution
- Precursor ion selection
- Fragmentation patterns
- Instrument configuration
- Quality control metrics
- Data completeness

### .mzXML - Mass Spectrometry XML
**Description:** Legacy XML MS format
**Typical Data:** Mass spectra and chromatograms
**Use Cases:** Proteomics workflows (older)
**Python Libraries:**
- `pyteomics.mzxml`
- `pymzml`: Can read mzXML
**EDA Approach:**
- Similar to mzML
- Version compatibility
- Conversion quality assessment

### .mzData - mzData Format
**Description:** Legacy PSI MS format
**Typical Data:** Mass spectrometry data
**Use Cases:** Legacy data archives
**Python Libraries:**
- `pyteomics`: Limited support
- Conversion to mzML recommended
**EDA Approach:**
- Format conversion validation
- Data completeness
- Metadata extraction

### .raw - Vendor Raw Files (Thermo, Agilent, Bruker)
**Description:** Proprietary instrument data
**Typical Data:** Raw mass spectra and metadata
**Use Cases:** Direct instrument output
**Python Libraries:**
- `pymsfilereader`: Thermo RAW files
- `ThermoRawFileParser`: CLI wrapper
- Vendor-specific APIs
**EDA Approach:**
- Method parameter extraction
- Instrument performance metrics
- Calibration status
- Scan function analysis
- MS/MS quality metrics
- Dynamic exclusion evaluation

### .d - Agilent Data Directory
**Description:** Agilent MS data folder
**Typical Data:** LC-MS, GC-MS with methods
**Use Cases:** Agilent MassHunter workflows
**Python Libraries:**
- Community parsers
- Chemstation integration
**EDA Approach:**
- Directory structure validation
- Method parameters
- Calibration curves
- Sequence metadata
- Signal quality metrics

### .wiff - AB SCIEX Data
**Description:** AB SCIEX/SCIEX instrument format
**Typical Data:** Mass spectrometry data
**Use Cases:** SCIEX instrument workflows
**Python Libraries:**
- Vendor SDKs (limited Python support)
- Conversion tools
**EDA Approach:**
- Experiment type identification
- Scan properties
- Quantitation data
- Multi-experiment structure

### .mgf - Mascot Generic Format
**Description:** Peak list format for MS/MS
**Typical Data:** Precursor and fragment masses
**Use Cases:** Peptide identification, database searches
**Python Libraries:**
- `pyteomics.mgf`: `pyteomics.mgf.read('file.mgf')`
- `pyopenms`: MGF support
**EDA Approach:**
- Spectrum count
- Charge state distribution
- Precursor m/z and intensity
- Fragment peak count
- Mass accuracy
- Title and metadata parsing

### .pkl - Peak List (Binary)
**Description:** Binary peak list format
**Typical Data:** Serialized MS/MS spectra
**Use Cases:** Software-specific storage
**Python Libraries:**
- `pickle`: Standard deserialization
- `pyteomics`: PKL support
**EDA Approach:**
- Data structure inspection
- Conversion to standard formats
- Metadata preservation

### .ms1 / .ms2 - MS1/MS2 Formats
**Description:** Simple text format for MS data
**Typical Data:** MS1 and MS2 scans
**Use Cases:** Database searching, proteomics
**Python Libraries:**
- `pyteomics.ms1` and `ms2`
- Simple text parsing
**EDA Approach:**
- Scan count by level
- Retention time series
- Charge state analysis
- m/z range coverage

### .pepXML - Peptide XML
**Description:** TPP peptide identification format
**Typical Data:** Peptide-spectrum matches
**Use Cases:** Proteomics search results
**Python Libraries:**
- `pyteomics.pepxml`
**EDA Approach:**
- Search result statistics
- Score distribution
- Modification analysis
- FDR assessment
- Enzyme specificity

### .protXML - Protein XML
**Description:** TPP protein inference format
**Typical Data:** Protein identifications
**Use Cases:** Proteomics protein-level results
**Python Libraries:**
- `pyteomics.protxml`
**EDA Approach:**
- Protein group analysis
- Coverage statistics
- Confidence scoring
- Parsimony analysis

### .msp - NIST MS Search Format
**Description:** NIST spectral library format
**Typical Data:** Reference mass spectra
**Use Cases:** Spectral library searching
**Python Libraries:**
- `matchms`: Spectral library handling
- Custom parsers
**EDA Approach:**
- Library size and coverage
- Metadata completeness
- Peak count statistics
- Compound annotation quality

## Infrared and Raman Spectroscopy

### .spc - Galactic SPC
**Description:** Thermo Galactic spectroscopy format
**Typical Data:** IR, Raman, UV-Vis spectra
**Use Cases:** Various spectroscopy instruments
**Python Libraries:**
- `spc`: `spc.File('file.spc')`
- `specio`: Multi-format reader
**EDA Approach:**
- Wavenumber/wavelength range
- Data point density
- Multi-spectrum handling
- Baseline characteristics
- Peak identification
- Absorbance/transmittance mode
- Instrument information

### .spa - Thermo Nicolet
**Description:** Thermo Fisher FTIR format
**Typical Data:** FTIR spectra
**Use Cases:** OMNIC software data
**Python Libraries:**
- Custom binary parsers
- Conversion to JCAMP or SPC
**EDA Approach:**
- Interferogram vs spectrum
- Background spectrum validation
- Atmospheric compensation
- Resolution and scan number
- Sample information

### .0 - Bruker OPUS
**Description:** Bruker OPUS FTIR format (numbered files)
**Typical Data:** FTIR spectra and metadata
**Use Cases:** Bruker FTIR instruments
**Python Libraries:**
- `brukeropusreader`: OPUS format parser
- `specio`: OPUS support
**EDA Approach:**
- Multiple block types (AB, ScSm, etc.)
- Sample and reference spectra
- Instrument parameters
- Optical path configuration
- Beam splitter and detector info

### .dpt - Data Point Table
**Description:** Simple XY data format
**Typical Data:** Generic spectroscopic data
**Use Cases:** Renishaw Raman, generic exports
**Python Libraries:**
- `pandas`: CSV-like reading
- Text parsing
**EDA Approach:**
- X-axis type (wavelength, wavenumber, Raman shift)
- Y-axis units (intensity, absorbance, etc.)
- Data point spacing
- Header information
- Multi-column data handling

### .wdf - Renishaw Raman
**Description:** Renishaw WiRE data format
**Typical Data:** Raman spectra and maps
**Use Cases:** Renishaw Raman microscopy
**Python Libraries:**
- `renishawWiRE`: WDF reader
- Custom parsers for WDF format
**EDA Approach:**
- Spectral vs mapping data
- Laser wavelength
- Accumulation and exposure time
- Spatial coordinates (mapping)
- Z-scan data
- Baseline and cosmic ray correction

### .txt (Spectroscopy)
**Description:** Generic text export from instruments
**Typical Data:** Wavelength/wavenumber and intensity
**Use Cases:** Universal data exchange
**Python Libraries:**
- `pandas`: Text file reading
- `numpy`: Simple array loading
**EDA Approach:**
- Delimiter and format detection
- Header parsing
- Units identification
- Multiple spectrum handling
- Metadata extraction from comments

## UV-Visible Spectroscopy

### .asd / .asc - ASD Binary/ASCII
**Description:** ASD FieldSpec spectroradiometer
**Typical Data:** Hyperspectral UV-Vis-NIR data
**Use Cases:** Remote sensing, reflectance spectroscopy
**Python Libraries:**
- `spectral.io.asd`: ASD format support
- Custom parsers
**EDA Approach:**
- Wavelength range (UV to NIR)
- Reference spectrum validation
- Dark current correction
- Integration time
- GPS metadata (if present)
- Reflectance vs radiance

### .sp - Perkin Elmer
**Description:** Perkin Elmer UV/Vis format
**Typical Data:** UV-Vis spectrophotometer data
**Use Cases:** PE Lambda instruments
**Python Libraries:**
- Custom parsers
- Conversion to standard formats
**EDA Approach:**
- Scan parameters
- Baseline correction
- Multi-wavelength scans
- Time-based measurements
- Sample/reference handling

### .csv (Spectroscopy)
**Description:** CSV export from UV-Vis instruments
**Typical Data:** Wavelength and absorbance/transmittance
**Use Cases:** Universal format for UV-Vis data
**Python Libraries:**
- `pandas`: Native CSV support
**EDA Approach:**
- Lambda max identification
- Beer's law compliance
- Baseline offset
- Path length correction
- Concentration calculations

## X-ray and Diffraction

### .cif - Crystallographic Information File
**Description:** Crystal structure and diffraction data
**Typical Data:** Unit cell, atomic positions, structure factors
**Use Cases:** Crystallography, materials science
**Python Libraries:**
- `gemmi`: `gemmi.cif.read_file('file.cif')`
- `PyCifRW`: CIF reading/writing
- `pymatgen`: Materials structure analysis
**EDA Approach:**
- Crystal system and space group
- Unit cell parameters
- Atomic positions and occupancy
- Thermal parameters
- R-factors and refinement quality
- Completeness and redundancy
- Structure validation

### .hkl - Reflection Data
**Description:** Miller indices and intensities
**Typical Data:** Integrated diffraction intensities
**Use Cases:** Crystallographic refinement
**Python Libraries:**
- Custom parsers (format dependent)
- Crystallography packages (CCP4, etc.)
**EDA Approach:**
- Resolution range
- Completeness by shell
- I/sigma distribution
- Systematic absences
- Twinning detection
- Wilson plot

### .mtz - MTZ Format (CCP4)
**Description:** Binary crystallographic data
**Typical Data:** Reflections, phases, structure factors
**Use Cases:** Macromolecular crystallography
**Python Libraries:**
- `gemmi`: MTZ support
- `cctbx`: Comprehensive crystallography
**EDA Approach:**
- Column types and data
- Resolution limits
- R-factors (Rwork, Rfree)
- Phase probability distribution
- Map coefficients
- Batch information

### .xy / .xye - Powder Diffraction
**Description:** 2-theta vs intensity data
**Typical Data:** Powder X-ray diffraction patterns
**Use Cases:** Phase identification, Rietveld refinement
**Python Libraries:**
- `pandas`: Simple XY reading
- `pymatgen`: XRD pattern analysis
**EDA Approach:**
- 2-theta range
- Peak positions and intensities
- Background modeling
- Peak width analysis (strain/size)
- Phase identification via matching
- Preferred orientation effects

### .raw (XRD)
**Description:** Vendor-specific XRD raw data
**Typical Data:** XRD patterns with metadata
**Use Cases:** Bruker, PANalytical, Rigaku instruments
**Python Libraries:**
- Vendor-specific parsers
- Conversion tools
**EDA Approach:**
- Scan parameters (step size, time)
- Sample alignment
- Incident beam setup
- Detector configuration
- Background scan validation

### .gsa / .gsas - GSAS Format
**Description:** General Structure Analysis System
**Typical Data:** Powder diffraction for Rietveld
**Use Cases:** Rietveld refinement
**Python Libraries:**
- GSAS-II Python interface
- Custom parsers
**EDA Approach:**
- Histogram data
- Instrument parameters
- Phase information
- Refinement constraints
- Profile function parameters

## Electron Spectroscopy

### .vms - VG Scienta
**Description:** VG Scienta spectrometer format
**Typical Data:** XPS, UPS, ARPES spectra
**Use Cases:** Photoelectron spectroscopy
**Python Libraries:**
- Custom parsers for VMS
- `specio`: Multi-format support
**EDA Approach:**
- Binding energy calibration
- Pass energy and resolution
- Photoelectron line identification
- Satellite peak analysis
- Background subtraction quality
- Fermi edge position

### .spe - WinSpec/SPE Format
**Description:** Princeton Instruments/Roper Scientific
**Typical Data:** CCD spectra, Raman, PL
**Use Cases:** Spectroscopy with CCD detectors
**Python Libraries:**
- `spe2py`: SPE file reader
- `spe_loader`: Alternative parser
**EDA Approach:**
- CCD frame analysis
- Wavelength calibration
- Dark frame subtraction
- Cosmic ray identification
- Readout noise
- Accumulation statistics

### .pxt - Princeton PTI
**Description:** Photon Technology International
**Typical Data:** Fluorescence, phosphorescence spectra
**Use Cases:** Fluorescence spectroscopy
**Python Libraries:**
- Custom parsers
- Text-based format variants
**EDA Approach:**
- Excitation and emission spectra
- Quantum yield calculations
- Time-resolved measurements
- Temperature-dependent data
- Correction factors applied

### .dat (Spectroscopy Generic)
**Description:** Generic binary or text spectroscopy data
**Typical Data:** Various spectroscopic measurements
**Use Cases:** Many instruments use .dat extension
**Python Libraries:**
- Format-specific identification needed
- `numpy`, `pandas` for known formats
**EDA Approach:**
- Format detection (binary vs text)
- Header identification
- Data structure inference
- Units and axis labels
- Instrument signature detection

## Chromatography

### .chrom - Chromatogram Data
**Description:** Generic chromatography format
**Typical Data:** Retention time vs signal
**Use Cases:** HPLC, GC, LC-MS
**Python Libraries:**
- Vendor-specific parsers
- `pandas` for text exports
**EDA Approach:**
- Retention time range
- Peak detection and integration
- Baseline drift
- Resolution between peaks
- Signal-to-noise ratio
- Tailing factor

### .ch - ChemStation
**Description:** Agilent ChemStation format
**Typical Data:** Chromatograms and method parameters
**Use Cases:** Agilent HPLC and GC systems
**Python Libraries:**
- `agilent-chemstation`: Community tools
- Binary format parsers
**EDA Approach:**
- Method validation
- Integration parameters
- Calibration curve
- Sample sequence information
- Instrument status

### .arw - Empower (Waters)
**Description:** Waters Empower format
**Typical Data:** UPLC/HPLC chromatograms
**Use Cases:** Waters instrument data
**Python Libraries:**
- Vendor tools (limited Python access)
- Database extraction tools
**EDA Approach:**
- Audit trail information
- Processing methods
- Compound identification
- Quantitation results
- System suitability tests

### .lcd - Shimadzu LabSolutions
**Description:** Shimadzu chromatography format
**Typical Data:** GC/HPLC data
**Use Cases:** Shimadzu instruments
**Python Libraries:**
- Vendor-specific parsers
**EDA Approach:**
- Method parameters
- Peak purity analysis
- Spectral data (if PDA)
- Quantitative results

## Other Analytical Techniques

### .dta - DSC/TGA Data
**Description:** Thermal analysis data (TA Instruments)
**Typical Data:** Temperature vs heat flow or mass
**Use Cases:** Differential scanning calorimetry, thermogravimetry
**Python Libraries:**
- Custom parsers for TA formats
- `pandas` for exported data
**EDA Approach:**
- Transition temperature identification
- Enthalpy calculations
- Mass loss steps
- Heating rate effects
- Baseline determination
- Purity assessment

### .run - ICP-MS/ICP-OES
**Description:** Elemental analysis data
**Typical Data:** Element concentrations or counts
**Use Cases:** Inductively coupled plasma MS/OES
**Python Libraries:**
- Vendor-specific tools
- Custom parsers
**EDA Approach:**
- Element detection and quantitation
- Internal standard performance
- Spike recovery
- Dilution factor corrections
- Isotope ratios
- LOD/LOQ calculations

### .exp - Electrochemistry Data
**Description:** Electrochemical experiment data
**Typical Data:** Potential vs current or charge
**Use Cases:** Cyclic voltammetry, chronoamperometry
**Python Libraries:**
- Custom parsers per instrument (CHI, Gamry, etc.)
- `galvani`: Biologic EC-Lab files
**EDA Approach:**
- Redox peak identification
- Peak potential and current
- Scan rate effects
- Electron transfer kinetics
- Background subtraction
- Capacitance calculations
