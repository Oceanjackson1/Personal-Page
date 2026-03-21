---
title: "Gget"
description: "Fast CLI/Python queries to 20+ bioinformatics databases. Use for quick lookups: gene info, BLAST searches, AlphaFold structures, enrichment analysis. Best for interactive exploration, simple queries. For batch processing or advanced BLAST use biop..."
category: "research"
source: "community"
author: "Community"
tags: ["gget"]
date: 2026-03-20
---

# gget

## Overview

gget is a command-line bioinformatics tool and Python package providing unified access to 20+ genomic databases and analysis methods. Query gene information, sequence analysis, protein structures, expression data, and disease associations through a consistent interface. All gget modules work both as command-line tools and as Python functions.

**Important**: The databases queried by gget are continuously updated, which sometimes changes their structure. gget modules are tested automatically on a biweekly basis and updated to match new database structures when necessary.

## Installation

Install gget in a clean virtual environment to avoid conflicts:

```bash
# Using uv (recommended)
uv uv pip install gget

# Or using pip
uv pip install --upgrade gget

# In Python/Jupyter
import gget
```

## Quick Start

Basic usage pattern for all modules:

```bash
# Command-line
gget <module> [arguments] [options]

# Python
gget.module(arguments, options)
```

Most modules return:
- **Command-line**: JSON (default) or CSV with `-csv` flag
- **Python**: DataFrame or dictionary

Common flags across modules:
- `-o/--out`: Save results to file
- `-q/--quiet`: Suppress progress information
- `-csv`: Return CSV format (command-line only)

## Module Categories

### 1. Reference & Gene Information

#### gget ref - Reference Genome Downloads

Retrieve download links and metadata for Ensembl reference genomes.

**Parameters**:
- `species`: Genus_species format (e.g., 'homo_sapiens', 'mus_musculus'). Shortcuts: 'human', 'mouse'
- `-w/--which`: Specify return types (gtf, cdna, dna, cds, cdrna, pep). Default: all
- `-r/--release`: Ensembl release number (default: latest)
- `-l/--list_species`: List available vertebrate species
- `-liv/--list_iv_species`: List available invertebrate species
- `-ftp`: Return only FTP links
- `-d/--download`: Download files (requires curl)

**Examples**:
```bash
# List available species
gget ref --list_species

# Get all reference files for human
gget ref homo_sapiens

# Download only GTF annotation for mouse
gget ref -w gtf -d mouse
```

```python
# Python
gget.ref("homo_sapiens")
gget.ref("mus_musculus", which="gtf", download=True)
```

#### gget search - Gene Search

Locate genes by name or description across species.

**Parameters**:
- `searchwords`: One or more search terms (case-insensitive)
- `-s/--species`: Target species (e.g., 'homo_sapiens', 'mouse')
- `-r/--release`: Ensembl release number
- `-t/--id_type`: Return 'gene' (default) or 'transcript'
- `-ao/--andor`: 'or' (default) finds ANY searchword; 'and' requires ALL
- `-l/--limit`: Maximum results to return

**Returns**: ensembl_id, gene_name, ensembl_description, ext_ref_description, biotype, URL

**Examples**:
```bash
# Search for GABA-related genes in human
gget search -s human gaba gamma-aminobutyric

# Find specific gene, require all terms
gget search -s mouse -ao and pax7 transcription
```

```python
# Python
gget.search(["gaba", "gamma-aminobutyric"], species="homo_sapiens")
```

#### gget info - Gene/Transcript Information

Retrieve comprehensive gene and transcript metadata from Ensembl, UniProt, and NCBI.

**Parameters**:
- `ens_ids`: One or more Ensembl IDs (also supports WormBase, Flybase IDs). Limit: ~1000 IDs
- `-n/--ncbi`: Disable NCBI data retrieval
- `-u/--uniprot`: Disable UniProt data retrieval
- `-pdb`: Include PDB identifiers (increases runtime)

**Returns**: UniProt ID, NCBI gene ID, primary gene name, synonyms, protein names, descriptions, biotype, canonical transcript

**Examples**:
```bash
# Get info for multiple genes
gget info ENSG00000034713 ENSG00000104853 ENSG00000170296

# Include PDB IDs
gget info ENSG00000034713 -pdb
```

```python
# Python
gget.info(["ENSG00000034713", "ENSG00000104853"], pdb=True)
```

#### gget seq - Sequence Retrieval

Fetch nucleotide or amino acid sequences for genes and transcripts.

**Parameters**:
- `ens_ids`: One or more Ensembl identifiers
- `-t/--translate`: Fetch amino acid sequences instead of nucleotide
- `-iso/--isoforms`: Return all transcript variants (gene IDs only)

**Returns**: FASTA format sequences

**Examples**:
```bash
# Get nucleotide sequences
gget seq ENSG00000034713 ENSG00000104853

# Get all protein isoforms
gget seq -t -iso ENSG00000034713
```

```python
# Python
gget.seq(["ENSG00000034713"], translate=True, isoforms=True)
```

### 2. Sequence Analysis & Alignment

#### gget blast - BLAST Searches

BLAST nucleotide or amino acid sequences against standard databases.

**Parameters**:
- `sequence`: Sequence string or path to FASTA/.txt file
- `-p/--program`: blastn, blastp, blastx, tblastn, tblastx (auto-detected)
- `-db/--database`:
  - Nucleotide: nt, refseq_rna, pdbnt
  - Protein: nr, swissprot, pdbaa, refseq_protein
- `-l/--limit`: Max hits (default: 50)
- `-e/--expect`: E-value cutoff (default: 10.0)
- `-lcf/--low_comp_filt`: Enable low complexity filtering
- `-mbo/--megablast_off`: Disable MegaBLAST (blastn only)

**Examples**:
```bash
# BLAST protein sequence
gget blast MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# BLAST from file with specific database
gget blast sequence.fasta -db swissprot -l 10
```

```python
# Python
gget.blast("MKWMFK...", database="swissprot", limit=10)
```

#### gget blat - BLAT Searches

Locate genomic positions of sequences using UCSC BLAT.

**Parameters**:
- `sequence`: Sequence string or path to FASTA/.txt file
- `-st/--seqtype`: 'DNA', 'protein', 'translated%20RNA', 'translated%20DNA' (auto-detected)
- `-a/--assembly`: Target assembly (default: 'human'/hg38; options: 'mouse'/mm39, 'zebrafinch'/taeGut2, etc.)

**Returns**: genome, query size, alignment positions, matches, mismatches, alignment percentage

**Examples**:
```bash
# Find genomic location in human
gget blat ATCGATCGATCGATCG

# Search in different assembly
gget blat -a mm39 ATCGATCGATCGATCG
```

```python
# Python
gget.blat("ATCGATCGATCGATCG", assembly="mouse")
```

#### gget muscle - Multiple Sequence Alignment

Align multiple nucleotide or amino acid sequences using Muscle5.

**Parameters**:
- `fasta`: Sequences or path to FASTA/.txt file
- `-s5/--super5`: Use Super5 algorithm for faster processing (large datasets)

**Returns**: Aligned sequences in ClustalW format or aligned FASTA (.afa)

**Examples**:
```bash
# Align sequences from file
gget muscle sequences.fasta -o aligned.afa

# Use Super5 for large dataset
gget muscle large_dataset.fasta -s5
```

```python
# Python
gget.muscle("sequences.fasta", save=True)
```

#### gget diamond - Local Sequence Alignment

Perform fast local protein or translated DNA alignment using DIAMOND.

**Parameters**:
- Query: Sequences (string/list) or FASTA file path
- `--reference`: Reference sequences (string/list) or FASTA file path (required)
- `--sensitivity`: fast, mid-sensitive, sensitive, more-sensitive, very-sensitive (default), ultra-sensitive
- `--threads`: CPU threads (default: 1)
- `--diamond_db`: Save database for reuse
- `--translated`: Enable nucleotide-to-amino acid alignment

**Returns**: Identity percentage, sequence lengths, match positions, gap openings, E-values, bit scores

**Examples**:
```bash
# Align against reference
gget diamond GGETISAWESQME -ref reference.fasta --threads 4

# Save database for reuse
gget diamond query.fasta -ref ref.fasta --diamond_db my_db.dmnd
```

```python
# Python
gget.diamond("GGETISAWESQME", reference="reference.fasta", threads=4)
```

### 3. Structural & Protein Analysis

#### gget pdb - Protein Structures

Query RCSB Protein Data Bank for structure and metadata.

**Parameters**:
- `pdb_id`: PDB identifier (e.g., '7S7U')
- `-r/--resource`: Data type (pdb, entry, pubmed, assembly, entity types)
- `-i/--identifier`: Assembly, entity, or chain ID

**Returns**: PDB format (structures) or JSON (metadata)

**Examples**:
```bash
# Download PDB structure
gget pdb 7S7U -o 7S7U.pdb

# Get metadata
gget pdb 7S7U -r entry
```

```python
# Python
gget.pdb("7S7U", save=True)
```

#### gget alphafold - Protein Structure Prediction

Predict 3D protein structures using simplified AlphaFold2.

**Setup Required**:
```bash
# Install OpenMM first
uv pip install openmm

# Then setup AlphaFold
gget setup alphafold
```

**Parameters**:
- `sequence`: Amino acid sequence (string), multiple sequences (list), or FASTA file. Multiple sequences trigger multimer modeling
- `-mr/--multimer_recycles`: Recycling iterations (default: 3; recommend 20 for accuracy)
- `-mfm/--multimer_for_monomer`: Apply multimer model to single proteins
- `-r/--relax`: AMBER relaxation for top-ranked model
- `plot`: Python-only; generate interactive 3D visualization (default: True)
- `show_sidechains`: Python-only; include side chains (default: True)

**Returns**: PDB structure file, JSON alignment error data, optional 3D visualization

**Examples**:
```bash
# Predict single protein structure
gget alphafold MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# Predict multimer with higher accuracy
gget alphafold sequence1.fasta -mr 20 -r
```

```python
# Python with visualization
gget.alphafold("MKWMFK...", plot=True, show_sidechains=True)

# Multimer prediction
gget.alphafold(["sequence1", "sequence2"], multimer_recycles=20)
```

#### gget elm - Eukaryotic Linear Motifs

Predict Eukaryotic Linear Motifs in protein sequences.

**Setup Required**:
```bash
gget setup elm
```

**Parameters**:
- `sequence`: Amino acid sequence or UniProt Acc
- `-u/--uniprot`: Indicates sequence is UniProt Acc
- `-e/--expand`: Include protein names, organisms, references
- `-s/--sensitivity`: DIAMOND alignment sensitivity (default: "very-sensitive")
- `-t/--threads`: Number of threads (default: 1)

**Returns**: Two outputs:
1. **ortholog_df**: Linear motifs from orthologous proteins
2. **regex_df**: Motifs directly matched in input sequence

**Examples**:
```bash
# Predict motifs from sequence
gget elm LIAQSIGQASFV -o results

# Use UniProt accession with expanded info
gget elm --uniprot Q02410 -e
```

```python
# Python
ortholog_df, regex_df = gget.elm("LIAQSIGQASFV")
```

### 4. Expression & Disease Data

#### gget archs4 - Gene Correlation & Tissue Expression

Query ARCHS4 database for correlated genes or tissue expression data.

**Parameters**:
- `gene`: Gene symbol or Ensembl ID (with `--ensembl` flag)
- `-w/--which`: 'correlation' (default, returns 100 most correlated genes) or 'tissue' (expression atlas)
- `-s/--species`: 'human' (default) or 'mouse' (tissue data only)
- `-e/--ensembl`: Input is Ensembl ID

**Returns**:
- **Correlation mode**: Gene symbols, Pearson correlation coefficients
- **Tissue mode**: Tissue identifiers, min/Q1/median/Q3/max expression values

**Examples**:
```bash
# Get correlated genes
gget archs4 ACE2

# Get tissue expression
gget archs4 -w tissue ACE2
```

```python
# Python
gget.archs4("ACE2", which="tissue")
```

#### gget cellxgene - Single-Cell RNA-seq Data

Query CZ CELLxGENE Discover Census for single-cell data.

**Setup Required**:
```bash
gget setup cellxgene
```

**Parameters**:
- `--gene` (-g): Gene names or Ensembl IDs (case-sensitive! 'PAX7' for human, 'Pax7' for mouse)
- `--tissue`: Tissue type(s)
- `--cell_type`: Specific cell type(s)
- `--species` (-s): 'homo_sapiens' (default) or 'mus_musculus'
- `--census_version` (-cv): Version ("stable", "latest", or dated)
- `--ensembl` (-e): Use Ensembl IDs
- `--meta_only` (-mo): Return metadata only
- Additional filters: disease, development_stage, sex, assay, dataset_id, donor_id, ethnicity, suspension_type

**Returns**: AnnData object with count matrices and metadata (or metadata-only dataframes)

**Examples**:
```bash
# Get single-cell data for specific genes and cell types
gget cellxgene --gene ACE2 ABCA1 --tissue lung --cell_type "mucus secreting cell" -o lung_data.h5ad

# Metadata only
gget cellxgene --gene PAX7 --tissue muscle --meta_only -o metadata.csv
```

```python
# Python
adata = gget.cellxgene(gene=["ACE2", "ABCA1"], tissue="lung", cell_type="mucus secreting cell")
```

#### gget enrichr - Enrichment Analysis

Perform ontology enrichment analysis on gene lists using Enrichr.

**Parameters**:
- `genes`: Gene symbols or Ensembl IDs
- `-db/--database`: Reference database (supports shortcuts: 'pathway', 'transcription', 'ontology', 'diseases_drugs', 'celltypes')
- `-s/--species`: human (default), mouse, fly, yeast, worm, fish
- `-bkg_l/--background_list`: Background genes for comparison
- `-ko/--kegg_out`: Save KEGG pathway images with highlighted genes
- `plot`: Python-only; generate graphical results

**Database Shortcuts**:
- 'pathway' → KEGG_2021_Human
- 'transcription' → ChEA_2016
- 'ontology' → GO_Biological_Process_2021
- 'diseases_drugs' → GWAS_Catalog_2019
- 'celltypes' → PanglaoDB_Augmented_2021

**Examples**:
```bash
# Enrichment analysis for ontology
gget enrichr -db ontology ACE2 AGT AGTR1

# Save KEGG pathways
gget enrichr -db pathway ACE2 AGT AGTR1 -ko ./kegg_images/
```

```python
# Python with plot
gget.enrichr(["ACE2", "AGT", "AGTR1"], database="ontology", plot=True)
```

#### gget bgee - Orthology & Expression

Retrieve orthology and gene expression data from Bgee database.

**Parameters**:
- `ens_id`: Ensembl gene ID or NCBI gene ID (for non-Ensembl species). Multiple IDs supported when `type=expression`
- `-t/--type`: 'orthologs' (default) or 'expression'

**Returns**:
- **Orthologs mode**: Matching genes across species with IDs, names, taxonomic info
- **Expression mode**: Anatomical entities, confidence scores, expression status

**Examples**:
```bash
# Get orthologs
gget bgee ENSG00000169194

# Get expression data
gget bgee ENSG00000169194 -t expression

# Multiple genes
gget bgee ENSBTAG00000047356 ENSBTAG00000018317 -t expression
```

```python
# Python
gget.bgee("ENSG00000169194", type="orthologs")
```

#### gget opentargets - Disease & Drug Associations

Retrieve disease and drug associations from OpenTargets.

**Parameters**:
- Ensembl gene ID (required)
- `-r/--resource`: diseases (default), drugs, tractability, pharmacogenetics, expression, depmap, interactions
- `-l/--limit`: Cap results count
- Filter arguments (vary by resource):
  - drugs: `--filter_disease`
  - pharmacogenetics: `--filter_drug`
  - expression/depmap: `--filter_tissue`, `--filter_anat_sys`, `--filter_organ`
  - interactions: `--filter_protein_a`, `--filter_protein_b`, `--filter_gene_b`

**Examples**:
```bash
# Get associated diseases
gget opentargets ENSG00000169194 -r diseases -l 5

# Get associated drugs
gget opentargets ENSG00000169194 -r drugs -l 10

# Get tissue expression
gget opentargets ENSG00000169194 -r expression --filter_tissue brain
```

```python
# Python
gget.opentargets("ENSG00000169194", resource="diseases", limit=5)
```

#### gget cbio - cBioPortal Cancer Genomics

Plot cancer genomics heatmaps using cBioPortal data.

**Two subcommands**:

**search** - Find study IDs:
```bash
gget cbio search breast lung
```

**plot** - Generate heatmaps:

**Parameters**:
- `-s/--study_ids`: Space-separated cBioPortal study IDs (required)
- `-g/--genes`: Space-separated gene names or Ensembl IDs (required)
- `-st/--stratification`: Column to organize data (tissue, cancer_type, cancer_type_detailed, study_id, sample)
- `-vt/--variation_type`: Data type (mutation_occurrences, cna_nonbinary, sv_occurrences, cna_occurrences, Consequence)
- `-f/--filter`: Filter by column value (e.g., 'study_id:msk_impact_2017')
- `-dd/--data_dir`: Cache directory (default: ./gget_cbio_cache)
- `-fd/--figure_dir`: Output directory (default: ./gget_cbio_figures)
- `-dpi`: Resolution (default: 100)
- `-sh/--show`: Display plot in window
- `-nc/--no_confirm`: Skip download confirmations

**Examples**:
```bash
# Search for studies
gget cbio search esophag ovary

# Create heatmap
gget cbio plot -s msk_impact_2017 -g AKT1 ALK BRAF -st tissue -vt mutation_occurrences
```

```python
# Python
gget.cbio_search(["esophag", "ovary"])
gget.cbio_plot(["msk_impact_2017"], ["AKT1", "ALK"], stratification="tissue")
```

#### gget cosmic - COSMIC Database

Search COSMIC (Catalogue Of Somatic Mutations In Cancer) database.

**Important**: License fees apply for commercial use. Requires COSMIC account credentials.

**Parameters**:
- `searchterm`: Gene name, Ensembl ID, mutation notation, or sample ID
- `-ctp/--cosmic_tsv_path`: Path to downloaded COSMIC TSV file (required for querying)
- `-l/--limit`: Maximum results (default: 100)

**Database download flags**:
- `-d/--download_cosmic`: Activate download mode
- `-gm/--gget_mutate`: Create version for gget mutate
- `-cp/--cosmic_project`: Database type (cancer, census, cell_line, resistance, genome_screen, targeted_screen)
- `-cv/--cosmic_version`: COSMIC version
- `-gv/--grch_version`: Human reference genome (37 or 38)
- `--email`, `--password`: COSMIC credentials

**Examples**:
```bash
# First download database
gget cosmic -d --email user@example.com --password xxx -cp cancer

# Then query
gget cosmic EGFR -ctp cosmic_data.tsv -l 10
```

```python
# Python
gget.cosmic("EGFR", cosmic_tsv_path="cosmic_data.tsv", limit=10)
```

### 5. Additional Tools

#### gget mutate - Generate Mutated Sequences

Generate mutated nucleotide sequences from mutation annotations.

**Parameters**:
- `sequences`: FASTA file path or direct sequence input (string/list)
- `-m/--mutations`: CSV/TSV file or DataFrame with mutation data (required)
- `-mc/--mut_column`: Mutation column name (default: 'mutation')
- `-sic/--seq_id_column`: Sequence ID column (default: 'seq_ID')
- `-mic/--mut_id_column`: Mutation ID column
- `-k/--k`: Length of flanking sequences (default: 30 nucleotides)

**Returns**: Mutated sequences in FASTA format

**Examples**:
```bash
# Single mutation
gget mutate ATCGCTAAGCT -m "c.4G>T"

# Multiple sequences with mutations from file
gget mutate sequences.fasta -m mutations.csv -o mutated.fasta
```

```python
# Python
import pandas as pd
mutations_df = pd.DataFrame({"seq_ID": ["seq1"], "mutation": ["c.4G>T"]})
gget.mutate(["ATCGCTAAGCT"], mutations=mutations_df)
```

#### gget gpt - OpenAI Text Generation

Generate natural language text using OpenAI's API.

**Setup Required**:
```bash
gget setup gpt
```

**Important**: Free tier limited to 3 months after account creation. Set monthly billing limits.

**Parameters**:
- `prompt`: Text input for generation (required)
- `api_key`: OpenAI authentication (required)
- Model configuration: temperature, top_p, max_tokens, frequency_penalty, presence_penalty
- Default model: gpt-3.5-turbo (configurable)

**Examples**:
```bash
gget gpt "Explain CRISPR" --api_key your_key_here
```

```python
# Python
gget.gpt("Explain CRISPR", api_key="your_key_here")
```

#### gget setup - Install Dependencies

Install/download third-party dependencies for specific modules.

**Parameters**:
- `module`: Module name requiring dependency installation
- `-o/--out`: Output folder path (elm module only)

**Modules requiring setup**:
- `alphafold` - Downloads ~4GB of model parameters
- `cellxgene` - Installs cellxgene-census (may not support latest Python)
- `elm` - Downloads local ELM database
- `gpt` - Configures OpenAI integration

**Examples**:
```bash
# Setup AlphaFold
gget setup alphafold

# Setup ELM with custom directory
gget setup elm -o /path/to/elm_data
```

```python
# Python
gget.setup("alphafold")
```

## Common Workflows

### Workflow 1: Gene Discovery to Sequence Analysis

Find and analyze genes of interest:

```python
# 1. Search for genes
results = gget.search(["GABA", "receptor"], species="homo_sapiens")

# 2. Get detailed information
gene_ids = results["ensembl_id"].tolist()
info = gget.info(gene_ids[:5])

# 3. Retrieve sequences
sequences = gget.seq(gene_ids[:5], translate=True)
```

### Workflow 2: Sequence Alignment and Structure

Align sequences and predict structures:

```python
# 1. Align multiple sequences
alignment = gget.muscle("sequences.fasta")

# 2. Find similar sequences
blast_results = gget.blast(my_sequence, database="swissprot", limit=10)

# 3. Predict structure
structure = gget.alphafold(my_sequence, plot=True)

# 4. Find linear motifs
ortholog_df, regex_df = gget.elm(my_sequence)
```

### Workflow 3: Gene Expression and Enrichment

Analyze expression patterns and functional enrichment:

```python
# 1. Get tissue expression
tissue_expr = gget.archs4("ACE2", which="tissue")

# 2. Find correlated genes
correlated = gget.archs4("ACE2", which="correlation")

# 3. Get single-cell data
adata = gget.cellxgene(gene=["ACE2"], tissue="lung", cell_type="epithelial cell")

# 4. Perform enrichment analysis
gene_list = correlated["gene_symbol"].tolist()[:50]
enrichment = gget.enrichr(gene_list, database="ontology", plot=True)
```

### Workflow 4: Disease and Drug Analysis

Investigate disease associations and therapeutic targets:

```python
# 1. Search for genes
genes = gget.search(["breast cancer"], species="homo_sapiens")

# 2. Get disease associations
diseases = gget.opentargets("ENSG00000169194", resource="diseases")

# 3. Get drug associations
drugs = gget.opentargets("ENSG00000169194", resource="drugs")

# 4. Query cancer genomics data
study_ids = gget.cbio_search(["breast"])
gget.cbio_plot(study_ids[:2], ["BRCA1", "BRCA2"], stratification="cancer_type")

# 5. Search COSMIC for mutations
cosmic_results = gget.cosmic("BRCA1", cosmic_tsv_path="cosmic.tsv")
```

### Workflow 5: Comparative Genomics

Compare proteins across species:

```python
# 1. Get orthologs
orthologs = gget.bgee("ENSG00000169194", type="orthologs")

# 2. Get sequences for comparison
human_seq = gget.seq("ENSG00000169194", translate=True)
mouse_seq = gget.seq("ENSMUSG00000026091", translate=True)

# 3. Align sequences
alignment = gget.muscle([human_seq, mouse_seq])

# 4. Compare structures
human_structure = gget.pdb("7S7U")
mouse_structure = gget.alphafold(mouse_seq)
```

### Workflow 6: Building Reference Indices

Prepare reference data for downstream analysis (e.g., kallisto|bustools):

```bash
# 1. List available species
gget ref --list_species

# 2. Download reference files
gget ref -w gtf -w cdna -d homo_sapiens

# 3. Build kallisto index
kallisto index -i transcriptome.idx transcriptome.fasta

# 4. Download genome for alignment
gget ref -w dna -d homo_sapiens
```

## Best Practices

### Data Retrieval
- Use `--limit` to control result sizes for large queries
- Save results with `-o/--out` for reproducibility
- Check database versions/releases for consistency across analyses
- Use `--quiet` in production scripts to reduce output

### Sequence Analysis
- For BLAST/BLAT, start with default parameters, then adjust sensitivity
- Use `gget diamond` with `--threads` for faster local alignment
- Save DIAMOND databases with `--diamond_db` for repeated queries
- For multiple sequence alignment, use `-s5/--super5` for large datasets

### Expression and Disease Data
- Gene symbols are case-sensitive in cellxgene (e.g., 'PAX7' vs 'Pax7')
- Run `gget setup` before first use of alphafold, cellxgene, elm, gpt
- For enrichment analysis, use database shortcuts for convenience
- Cache cBioPortal data with `-dd` to avoid repeated downloads

### Structure Prediction
- AlphaFold multimer predictions: use `-mr 20` for higher accuracy
- Use `-r` flag for AMBER relaxation of final structures
- Visualize results in Python with `plot=True`
- Check PDB database first before running AlphaFold predictions

### Error Handling
- Database structures change; update gget regularly: `uv pip install --upgrade gget`
- Process max ~1000 Ensembl IDs at once with gget info
- For large-scale analyses, implement rate limiting for API queries
- Use virtual environments to avoid dependency conflicts

## Output Formats

### Command-line
- Default: JSON
- CSV: Add `-csv` flag
- FASTA: gget seq, gget mutate
- PDB: gget pdb, gget alphafold
- PNG: gget cbio plot

### Python
- Default: DataFrame or dictionary
- JSON: Add `json=True` parameter
- Save to file: Add `save=True` or specify `out="filename"`
- AnnData: gget cellxgene

## Resources

This skill includes reference documentation for detailed module information:

### references/
- `module_reference.md` - Comprehensive parameter reference for all modules
- `database_info.md` - Information about queried databases and their update frequencies
- `workflows.md` - Extended workflow examples and use cases

For additional help:
- Official documentation: https://pachterlab.github.io/gget/
- GitHub issues: https://github.com/pachterlab/gget/issues
- Citation: Luebbert, L. & Pachter, L. (2023). Efficient querying of genomic reference databases with gget. Bioinformatics. https://doi.org/10.1093/bioinformatics/btac836

---

## Reference: Database_Info

# gget Database Information

Overview of databases queried by gget modules, including update frequencies and important considerations.

## Important Note

The databases queried by gget are continuously being updated, which sometimes changes their structure. gget modules are tested automatically on a biweekly basis and updated to match new database structures when necessary. Always keep gget updated:

```bash
pip install --upgrade gget
```

## Database Directory

### Genomic Reference Databases

#### Ensembl
- **Used by:** gget ref, gget search, gget info, gget seq
- **Description:** Comprehensive genome database with annotations for vertebrate and invertebrate species
- **Update frequency:** Regular releases (numbered); new releases approximately every 3 months
- **Access:** FTP downloads, REST API
- **Website:** https://www.ensembl.org/
- **Notes:**
  - Supports both vertebrate and invertebrate genomes
  - Can specify release number for reproducibility
  - Shortcuts available for common species ('human', 'mouse')

#### UCSC Genome Browser
- **Used by:** gget blat
- **Description:** Genome browser database with BLAT alignment tool
- **Update frequency:** Regular updates with new assemblies
- **Access:** Web service API
- **Website:** https://genome.ucsc.edu/
- **Notes:**
  - Multiple genome assemblies available (hg38, mm39, etc.)
  - BLAT optimized for vertebrate genomes

### Protein & Structure Databases

#### UniProt
- **Used by:** gget info, gget seq (amino acid sequences), gget elm
- **Description:** Universal Protein Resource, comprehensive protein sequence and functional information
- **Update frequency:** Regular releases (weekly for Swiss-Prot, monthly for TrEMBL)
- **Access:** REST API
- **Website:** https://www.uniprot.org/
- **Notes:**
  - Swiss-Prot: manually annotated and reviewed
  - TrEMBL: automatically annotated

#### NCBI (National Center for Biotechnology Information)
- **Used by:** gget info, gget bgee (for non-Ensembl species)
- **Description:** Gene and protein databases with extensive cross-references
- **Update frequency:** Continuous updates
- **Access:** E-utilities API
- **Website:** https://www.ncbi.nlm.nih.gov/
- **Databases:** Gene, Protein, RefSeq

#### RCSB PDB (Protein Data Bank)
- **Used by:** gget pdb
- **Description:** Repository of 3D structural data for proteins and nucleic acids
- **Update frequency:** Weekly updates
- **Access:** REST API
- **Website:** https://www.rcsb.org/
- **Notes:**
  - Experimentally determined structures (X-ray, NMR, cryo-EM)
  - Includes metadata about experiments and publications

#### ELM (Eukaryotic Linear Motif)
- **Used by:** gget elm
- **Description:** Database of functional sites in eukaryotic proteins
- **Update frequency:** Periodic updates
- **Access:** Downloaded database (via gget setup elm)
- **Website:** http://elm.eu.org/
- **Notes:**
  - Requires local download before first use
  - Contains validated motifs and patterns

### Sequence Similarity Databases

#### BLAST Databases (NCBI)
- **Used by:** gget blast
- **Description:** Pre-formatted databases for BLAST searches
- **Update frequency:** Regular updates
- **Access:** NCBI BLAST API
- **Databases:**
  - **Nucleotide:** nt (all GenBank), refseq_rna, pdbnt
  - **Protein:** nr (non-redundant), swissprot, pdbaa, refseq_protein
- **Notes:**
  - nt and nr are very large databases
  - Consider specialized databases for faster, more focused searches

### Expression & Correlation Databases

#### ARCHS4
- **Used by:** gget archs4
- **Description:** Massive mining of publicly available RNA-seq data
- **Update frequency:** Periodic updates with new samples
- **Access:** HTTP API
- **Website:** https://maayanlab.cloud/archs4/
- **Data:**
  - Human and mouse RNA-seq data
  - Correlation matrices
  - Tissue expression atlases
- **Citation:** Lachmann et al., Nature Communications, 2018

#### CZ CELLxGENE Discover
- **Used by:** gget cellxgene
- **Description:** Single-cell RNA-seq data from multiple studies
- **Update frequency:** Continuous additions of new datasets
- **Access:** Census API (via cellxgene-census package)
- **Website:** https://cellxgene.cziscience.com/
- **Data:**
  - Single-cell RNA-seq count matrices
  - Cell type annotations
  - Tissue and disease metadata
- **Notes:**
  - Requires gget setup cellxgene
  - Gene symbols are case-sensitive
  - May not support latest Python versions

#### Bgee
- **Used by:** gget bgee
- **Description:** Gene expression and orthology database
- **Update frequency:** Regular releases
- **Access:** REST API
- **Website:** https://www.bgee.org/
- **Data:**
  - Gene expression across tissues and developmental stages
  - Orthology relationships across species
- **Citation:** Bastian et al., 2021

### Functional & Pathway Databases

#### Enrichr / modEnrichr
- **Used by:** gget enrichr
- **Description:** Gene set enrichment analysis web service
- **Update frequency:** Regular updates to underlying databases
- **Access:** REST API
- **Website:** https://maayanlab.cloud/Enrichr/
- **Databases included:**
  - KEGG pathways
  - Gene Ontology (GO)
  - Transcription factor targets (ChEA)
  - Disease associations (GWAS Catalog)
  - Cell type markers (PanglaoDB)
- **Notes:**
  - Supports multiple model organisms
  - Background gene lists can be provided for custom enrichment

### Disease & Drug Databases

#### Open Targets
- **Used by:** gget opentargets
- **Description:** Integrative platform for disease-target associations
- **Update frequency:** Regular releases (quarterly)
- **Access:** GraphQL API
- **Website:** https://www.opentargets.org/
- **Data:**
  - Disease associations
  - Drug information and clinical trials
  - Target tractability
  - Pharmacogenetics
  - Gene expression
  - DepMap gene-disease effects
  - Protein-protein interactions

#### cBioPortal
- **Used by:** gget cbio
- **Description:** Cancer genomics data portal
- **Update frequency:** Continuous addition of new studies
- **Access:** Web API, downloadable datasets
- **Website:** https://www.cbioportal.org/
- **Data:**
  - Mutations, copy number alterations, structural variants
  - Gene expression
  - Clinical data
- **Notes:**
  - Large datasets; caching recommended
  - Multiple cancer types and studies available

#### COSMIC (Catalogue Of Somatic Mutations In Cancer)
- **Used by:** gget cosmic
- **Description:** Comprehensive cancer mutation database
- **Update frequency:** Regular releases
- **Access:** Download (requires account and license for commercial use)
- **Website:** https://cancer.sanger.ac.uk/cosmic
- **Data:**
  - Somatic mutations in cancer
  - Gene census
  - Cell line data
  - Drug resistance mutations
- **Important:**
  - Free for academic use
  - License fees apply for commercial use
  - Requires COSMIC account credentials
  - Must download database before querying

### AI & Prediction Services

#### AlphaFold2 (DeepMind)
- **Used by:** gget alphafold
- **Description:** Deep learning model for protein structure prediction
- **Model version:** Simplified version for local execution
- **Access:** Local computation (requires model download via gget setup)
- **Website:** https://alphafold.ebi.ac.uk/
- **Notes:**
  - Requires ~4GB model parameters download
  - Requires OpenMM installation
  - Computationally intensive
  - Python version-specific requirements

#### OpenAI API
- **Used by:** gget gpt
- **Description:** Large language model API
- **Update frequency:** New models released periodically
- **Access:** REST API (requires API key)
- **Website:** https://openai.com/
- **Notes:**
  - Default model: gpt-3.5-turbo
  - Free tier limited to 3 months after account creation
  - Set billing limits to control costs

## Data Consistency & Reproducibility

### Version Control
To ensure reproducibility in analyses:

1. **Specify database versions/releases:**
   ```python
   # Use specific Ensembl release
   gget.ref("homo_sapiens", release=110)

   # Use specific Census version
   gget.cellxgene(gene=["PAX7"], census_version="2023-07-25")
   ```

2. **Document gget version:**
   ```python
   import gget
   print(gget.__version__)
   ```

3. **Save raw data:**
   ```python
   # Always save results for reproducibility
   results = gget.search(["ACE2"], species="homo_sapiens")
   results.to_csv("search_results_2025-01-15.csv", index=False)
   ```

### Handling Database Updates

1. **Regular gget updates:**
   - Update gget biweekly to match database structure changes
   - Check release notes for breaking changes

2. **Error handling:**
   - Database structure changes may cause temporary failures
   - Check GitHub issues: https://github.com/pachterlab/gget/issues
   - Update gget if errors occur

3. **API rate limiting:**
   - Implement delays for large-scale queries
   - Use local databases (DIAMOND, COSMIC) when possible
   - Cache results to avoid repeated queries

## Database-Specific Best Practices

### Ensembl
- Use species shortcuts ('human', 'mouse') for convenience
- Specify release numbers for reproducibility
- Check available species with `gget ref --list_species`

### UniProt
- UniProt IDs are more stable than gene names
- Swiss-Prot annotations are manually curated and more reliable
- Use PDB flag in gget info only when needed (increases runtime)

### BLAST/BLAT
- Start with default parameters, then optimize
- Use specialized databases (swissprot, refseq_protein) for focused searches
- Consider E-value cutoffs based on query length

### Expression Databases
- Gene symbols are case-sensitive in CELLxGENE
- ARCHS4 correlation data is based on co-expression patterns
- Consider tissue-specificity when interpreting results

### Cancer Databases
- cBioPortal: cache data locally for repeated analyses
- COSMIC: download appropriate database subset for your needs
- Respect license agreements for commercial use

## Citations

When using gget, cite both the gget publication and the underlying databases:

**gget:**
Luebbert, L. & Pachter, L. (2023). Efficient querying of genomic reference databases with gget. Bioinformatics. https://doi.org/10.1093/bioinformatics/btac836

**Database-specific citations:** Check references/ directory or database websites for appropriate citations.

---

## Reference: Module_Reference

# gget Module Reference

Comprehensive parameter reference for all gget modules.

## Reference & Gene Information Modules

### gget ref
Retrieve Ensembl reference genome FTPs and metadata.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `species` | str | Species in Genus_species format or shortcuts ('human', 'mouse') | Required |
| `-w/--which` | str | File types to return: gtf, cdna, dna, cds, cdrna, pep | All |
| `-r/--release` | int | Ensembl release number | Latest |
| `-od/--out_dir` | str | Output directory path | None |
| `-o/--out` | str | JSON file path for results | None |
| `-l/--list_species` | flag | List available vertebrate species | False |
| `-liv/--list_iv_species` | flag | List available invertebrate species | False |
| `-ftp` | flag | Return only FTP links | False |
| `-d/--download` | flag | Download files (requires curl) | False |
| `-q/--quiet` | flag | Suppress progress information | False |

**Returns:** JSON containing FTP links, Ensembl release numbers, release dates, file sizes

---

### gget search
Search for genes by name or description in Ensembl.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `searchwords` | str/list | Search terms (case-insensitive) | Required |
| `-s/--species` | str | Target species or core database name | Required |
| `-r/--release` | int | Ensembl release number | Latest |
| `-t/--id_type` | str | Return 'gene' or 'transcript' | 'gene' |
| `-ao/--andor` | str | 'or' (ANY term) or 'and' (ALL terms) | 'or' |
| `-l/--limit` | int | Maximum results to return | None |
| `-o/--out` | str | Output file path (CSV/JSON) | None |

**Returns:** ensembl_id, gene_name, ensembl_description, ext_ref_description, biotype, URL

---

### gget info
Get comprehensive gene/transcript metadata from Ensembl, UniProt, and NCBI.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ens_ids` | str/list | Ensembl IDs (WormBase, Flybase also supported) | Required |
| `-o/--out` | str | Output file path (CSV/JSON) | None |
| `-n/--ncbi` | bool | Disable NCBI data retrieval | False |
| `-u/--uniprot` | bool | Disable UniProt data retrieval | False |
| `-pdb` | bool | Include PDB identifiers | False |
| `-csv` | flag | Return CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress display | False |

**Python-specific:**
- `save=True`: Save output to current directory
- `wrap_text=True`: Format dataframe with wrapped text

**Note:** Processing >1000 IDs simultaneously may cause server errors.

**Returns:** UniProt ID, NCBI gene ID, gene name, synonyms, protein names, descriptions, biotype, canonical transcript

---

### gget seq
Retrieve nucleotide or amino acid sequences in FASTA format.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ens_ids` | str/list | Ensembl identifiers | Required |
| `-o/--out` | str | Output file path | stdout |
| `-t/--translate` | flag | Fetch amino acid sequences | False |
| `-iso/--isoforms` | flag | Return all transcript variants | False |
| `-q/--quiet` | flag | Suppress progress information | False |

**Data sources:** Ensembl (nucleotide), UniProt (amino acid)

**Returns:** FASTA format sequences

---

## Sequence Analysis & Alignment Modules

### gget blast
BLAST sequences against standard databases.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sequence` | str | Sequence or path to FASTA/.txt | Required |
| `-p/--program` | str | blastn, blastp, blastx, tblastn, tblastx | Auto-detect |
| `-db/--database` | str | nt, refseq_rna, pdbnt, nr, swissprot, pdbaa, refseq_protein | nt or nr |
| `-l/--limit` | int | Max hits returned | 50 |
| `-e/--expect` | float | E-value cutoff | 10.0 |
| `-lcf/--low_comp_filt` | flag | Enable low complexity filtering | False |
| `-mbo/--megablast_off` | flag | Disable MegaBLAST (blastn only) | False |
| `-o/--out` | str | Output file path | None |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** Description, Scientific Name, Common Name, Taxid, Max Score, Total Score, Query Coverage

---

### gget blat
Find genomic positions using UCSC BLAT.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sequence` | str | Sequence or path to FASTA/.txt | Required |
| `-st/--seqtype` | str | 'DNA', 'protein', 'translated%20RNA', 'translated%20DNA' | Auto-detect |
| `-a/--assembly` | str | Target assembly (hg38, mm39, taeGut2, etc.) | 'human'/hg38 |
| `-o/--out` | str | Output file path | None |
| `-csv` | flag | Return CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** genome, query size, alignment start/end, matches, mismatches, alignment percentage

---

### gget muscle
Align multiple sequences using Muscle5.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `fasta` | str/list | Sequences or FASTA file path | Required |
| `-o/--out` | str | Output file path | stdout |
| `-s5/--super5` | flag | Use Super5 algorithm (faster, large datasets) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** ClustalW format alignment or aligned FASTA (.afa)

---

### gget diamond
Fast local protein/translated DNA alignment.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `query` | str/list | Query sequences or FASTA file | Required |
| `--reference` | str/list | Reference sequences or FASTA file | Required |
| `--sensitivity` | str | fast, mid-sensitive, sensitive, more-sensitive, very-sensitive, ultra-sensitive | very-sensitive |
| `--threads` | int | CPU threads | 1 |
| `--diamond_binary` | str | Path to DIAMOND installation | Auto-detect |
| `--diamond_db` | str | Save database for reuse | None |
| `--translated` | flag | Enable nucleotide-to-amino acid alignment | False |
| `-o/--out` | str | Output file path | None |
| `-csv` | flag | CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** Identity %, sequence lengths, match positions, gap openings, E-values, bit scores

---

## Structural & Protein Analysis Modules

### gget pdb
Query RCSB Protein Data Bank.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `pdb_id` | str | PDB identifier (e.g., '7S7U') | Required |
| `-r/--resource` | str | pdb, entry, pubmed, assembly, entity types | 'pdb' |
| `-i/--identifier` | str | Assembly, entity, or chain ID | None |
| `-o/--out` | str | Output file path | stdout |

**Returns:** PDB format (structures) or JSON (metadata)

---

### gget alphafold
Predict 3D protein structures using AlphaFold2.

**Setup:** Requires OpenMM and `gget setup alphafold` (~4GB download)

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sequence` | str/list | Amino acid sequence(s) or FASTA file | Required |
| `-mr/--multimer_recycles` | int | Recycling iterations for multimers | 3 |
| `-o/--out` | str | Output folder path | timestamped |
| `-mfm/--multimer_for_monomer` | flag | Apply multimer model to monomers | False |
| `-r/--relax` | flag | AMBER relaxation for top model | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Python-only:**
- `plot` (bool): Generate 3D visualization (default: True)
- `show_sidechains` (bool): Include side chains (default: True)

**Note:** Multiple sequences automatically trigger multimer modeling

**Returns:** PDB structure file, JSON alignment error data, optional 3D plot

---

### gget elm
Predict Eukaryotic Linear Motifs.

**Setup:** Requires `gget setup elm`

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sequence` | str | Amino acid sequence or UniProt Acc | Required |
| `-s/--sensitivity` | str | DIAMOND alignment sensitivity | very-sensitive |
| `-t/--threads` | int | Number of threads | 1 |
| `-bin/--diamond_binary` | str | Path to DIAMOND binary | Auto-detect |
| `-o/--out` | str | Output directory path | None |
| `-u/--uniprot` | flag | Input is UniProt Acc | False |
| `-e/--expand` | flag | Include protein names, organisms, references | False |
| `-csv` | flag | CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** Two outputs:
1. **ortholog_df**: Motifs from orthologous proteins
2. **regex_df**: Motifs matched in input sequence

---

## Expression & Disease Data Modules

### gget archs4
Query ARCHS4 for gene correlation or tissue expression.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `gene` | str | Gene symbol or Ensembl ID | Required |
| `-w/--which` | str | 'correlation' or 'tissue' | 'correlation' |
| `-s/--species` | str | 'human' or 'mouse' (tissue only) | 'human' |
| `-o/--out` | str | Output file path | None |
| `-e/--ensembl` | flag | Input is Ensembl ID | False |
| `-csv` | flag | CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:**
- **correlation**: Gene symbols, Pearson correlation coefficients (top 100)
- **tissue**: Tissue IDs, min/Q1/median/Q3/max expression

---

### gget cellxgene
Query CZ CELLxGENE Discover Census for single-cell data.

**Setup:** Requires `gget setup cellxgene`

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `--gene` (-g) | list | Gene names or Ensembl IDs (case-sensitive!) | Required |
| `--tissue` | list | Tissue type(s) | None |
| `--cell_type` | list | Cell type(s) | None |
| `--species` (-s) | str | 'homo_sapiens' or 'mus_musculus' | 'homo_sapiens' |
| `--census_version` (-cv) | str | "stable", "latest", or dated version | "stable" |
| `-o/--out` | str | Output file path (required for CLI) | Required |
| `--ensembl` (-e) | flag | Use Ensembl IDs | False |
| `--meta_only` (-mo) | flag | Return metadata only | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Additional filters:** disease, development_stage, sex, assay, dataset_id, donor_id, ethnicity, suspension_type

**Important:** Gene symbols are case-sensitive ('PAX7' for human, 'Pax7' for mouse)

**Returns:** AnnData object with count matrices and metadata

---

### gget enrichr
Perform enrichment analysis using Enrichr/modEnrichr.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `genes` | list | Gene symbols or Ensembl IDs | Required |
| `-db/--database` | str | Reference database or shortcut | Required |
| `-s/--species` | str | human, mouse, fly, yeast, worm, fish | 'human' |
| `-bkg_l/--background_list` | list | Background genes | None |
| `-o/--out` | str | Output file path | None |
| `-ko/--kegg_out` | str | KEGG pathway images directory | None |

**Python-only:**
- `plot` (bool): Generate graphical results

**Database shortcuts:**
- 'pathway' → KEGG_2021_Human
- 'transcription' → ChEA_2016
- 'ontology' → GO_Biological_Process_2021
- 'diseases_drugs' → GWAS_Catalog_2019
- 'celltypes' → PanglaoDB_Augmented_2021

**Returns:** Pathway/function associations with adjusted p-values, overlapping gene counts

---

### gget bgee
Retrieve orthology and expression from Bgee.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ens_id` | str/list | Ensembl or NCBI gene ID | Required |
| `-t/--type` | str | 'orthologs' or 'expression' | 'orthologs' |
| `-o/--out` | str | Output file path | None |
| `-csv` | flag | CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Note:** Multiple IDs supported when `type='expression'`

**Returns:**
- **orthologs**: Genes across species with IDs, names, taxonomic info
- **expression**: Anatomical entities, confidence scores, expression status

---

### gget opentargets
Retrieve disease/drug associations from OpenTargets.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ens_id` | str | Ensembl gene ID | Required |
| `-r/--resource` | str | diseases, drugs, tractability, pharmacogenetics, expression, depmap, interactions | 'diseases' |
| `-l/--limit` | int | Maximum results | None |
| `-o/--out` | str | Output file path | None |
| `-csv` | flag | CSV format (CLI) | False |
| `-q/--quiet` | flag | Suppress progress | False |

**Resource-specific filters:**
- drugs: `--filter_disease`
- pharmacogenetics: `--filter_drug`
- expression/depmap: `--filter_tissue`, `--filter_anat_sys`, `--filter_organ`
- interactions: `--filter_protein_a`, `--filter_protein_b`, `--filter_gene_b`

**Returns:** Disease/drug associations, tractability, pharmacogenetics, expression, DepMap, interactions

---

### gget cbio
Plot cancer genomics heatmaps from cBioPortal.

**Subcommands:** search, plot

**search parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `keywords` | list | Search terms | Required |

**plot parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `-s/--study_ids` | list | cBioPortal study IDs | Required |
| `-g/--genes` | list | Gene names or Ensembl IDs | Required |
| `-st/--stratification` | str | tissue, cancer_type, cancer_type_detailed, study_id, sample | None |
| `-vt/--variation_type` | str | mutation_occurrences, cna_nonbinary, sv_occurrences, cna_occurrences, Consequence | None |
| `-f/--filter` | str | Filter by column value (e.g., 'study_id:msk_impact_2017') | None |
| `-dd/--data_dir` | str | Cache directory | ./gget_cbio_cache |
| `-fd/--figure_dir` | str | Output directory | ./gget_cbio_figures |
| `-t/--title` | str | Custom figure title | None |
| `-dpi` | int | Resolution | 100 |
| `-q/--quiet` | flag | Suppress progress | False |
| `-nc/--no_confirm` | flag | Skip download confirmations | False |
| `-sh/--show` | flag | Display plot in window | False |

**Returns:** PNG heatmap figure

---

### gget cosmic
Search COSMIC database for cancer mutations.

**Important:** License fees for commercial use. Requires COSMIC account.

**Query parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `searchterm` | str | Gene name, Ensembl ID, mutation, sample ID | Required |
| `-ctp/--cosmic_tsv_path` | str | Path to COSMIC TSV file | Required |
| `-l/--limit` | int | Maximum results | 100 |
| `-csv` | flag | CSV format (CLI) | False |

**Download parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `-d/--download_cosmic` | flag | Activate download mode | False |
| `-gm/--gget_mutate` | flag | Create version for gget mutate | False |
| `-cp/--cosmic_project` | str | cancer, census, cell_line, resistance, genome_screen, targeted_screen | None |
| `-cv/--cosmic_version` | str | COSMIC version | Latest |
| `-gv/--grch_version` | int | Human reference genome (37 or 38) | None |
| `--email` | str | COSMIC account email | Required |
| `--password` | str | COSMIC account password | Required |

**Note:** First-time users must download database

**Returns:** Mutation data from COSMIC

---

## Additional Tools

### gget mutate
Generate mutated nucleotide sequences.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sequences` | str/list | FASTA file or sequences | Required |
| `-m/--mutations` | str/df | CSV/TSV file or DataFrame | Required |
| `-mc/--mut_column` | str | Mutation column name | 'mutation' |
| `-sic/--seq_id_column` | str | Sequence ID column | 'seq_ID' |
| `-mic/--mut_id_column` | str | Mutation ID column | None |
| `-k/--k` | int | Length of flanking sequences | 30 |
| `-o/--out` | str | Output FASTA file path | stdout |
| `-q/--quiet` | flag | Suppress progress | False |

**Returns:** Mutated sequences in FASTA format

---

### gget gpt
Generate text using OpenAI's API.

**Setup:** Requires `gget setup gpt` and OpenAI API key

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `prompt` | str | Text input for generation | Required |
| `api_key` | str | OpenAI API key | Required |
| `model` | str | OpenAI model name | gpt-3.5-turbo |
| `temperature` | float | Sampling temperature (0-2) | 1.0 |
| `top_p` | float | Nucleus sampling | 1.0 |
| `max_tokens` | int | Maximum tokens to generate | None |
| `frequency_penalty` | float | Frequency penalty (0-2) | 0 |
| `presence_penalty` | float | Presence penalty (0-2) | 0 |

**Important:** Free tier limited to 3 months. Set billing limits.

**Returns:** Generated text string

---

### gget setup
Install/download dependencies for modules.

**Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `module` | str | Module name | Required |
| `-o/--out` | str | Output folder (elm only) | Package install folder |
| `-q/--quiet` | flag | Suppress progress | False |

**Modules requiring setup:**
- `alphafold` - Downloads ~4GB model parameters
- `cellxgene` - Installs cellxgene-census
- `elm` - Downloads local ELM database
- `gpt` - Configures OpenAI integration

**Returns:** None (installs dependencies)

---

## Reference: Workflows

# gget Workflow Examples

Extended workflow examples demonstrating how to combine multiple gget modules for common bioinformatics tasks.

## Table of Contents
1. [Complete Gene Analysis Pipeline](#complete-gene-analysis-pipeline)
2. [Comparative Structural Biology](#comparative-structural-biology)
3. [Cancer Genomics Analysis](#cancer-genomics-analysis)
4. [Single-Cell Expression Analysis](#single-cell-expression-analysis)
5. [Building Reference Transcriptomes](#building-reference-transcriptomes)
6. [Mutation Impact Assessment](#mutation-impact-assessment)
7. [Drug Target Discovery](#drug-target-discovery)

---

## Complete Gene Analysis Pipeline

Comprehensive analysis of a gene from discovery to functional annotation.

```python
import gget
import pandas as pd

# Step 1: Search for genes of interest
print("Step 1: Searching for GABA receptor genes...")
search_results = gget.search(["GABA", "receptor", "alpha"],
                             species="homo_sapiens",
                             andor="and")
print(f"Found {len(search_results)} genes")

# Step 2: Get detailed information
print("\nStep 2: Getting detailed information...")
gene_ids = search_results["ensembl_id"].tolist()[:5]  # Top 5 genes
gene_info = gget.info(gene_ids, pdb=True)
print(gene_info[["ensembl_id", "gene_name", "uniprot_id", "description"]])

# Step 3: Retrieve sequences
print("\nStep 3: Retrieving sequences...")
nucleotide_seqs = gget.seq(gene_ids)
protein_seqs = gget.seq(gene_ids, translate=True)

# Save sequences
with open("gaba_receptors_nt.fasta", "w") as f:
    f.write(nucleotide_seqs)
with open("gaba_receptors_aa.fasta", "w") as f:
    f.write(protein_seqs)

# Step 4: Get expression data
print("\nStep 4: Getting tissue expression...")
for gene_id, gene_name in zip(gene_ids, gene_info["gene_name"]):
    expr_data = gget.archs4(gene_name, which="tissue")
    print(f"\n{gene_name} expression:")
    print(expr_data.head())

# Step 5: Find correlated genes
print("\nStep 5: Finding correlated genes...")
correlated = gget.archs4(gene_info["gene_name"].iloc[0], which="correlation")
correlated_top = correlated.head(20)
print(correlated_top)

# Step 6: Enrichment analysis on correlated genes
print("\nStep 6: Performing enrichment analysis...")
gene_list = correlated_top["gene_symbol"].tolist()
enrichment = gget.enrichr(gene_list, database="ontology", plot=True)
print(enrichment.head(10))

# Step 7: Get disease associations
print("\nStep 7: Getting disease associations...")
for gene_id, gene_name in zip(gene_ids[:3], gene_info["gene_name"][:3]):
    diseases = gget.opentargets(gene_id, resource="diseases", limit=5)
    print(f"\n{gene_name} disease associations:")
    print(diseases)

# Step 8: Check for orthologs
print("\nStep 8: Finding orthologs...")
orthologs = gget.bgee(gene_ids[0], type="orthologs")
print(orthologs)

print("\nComplete gene analysis pipeline finished!")
```

---

## Comparative Structural Biology

Compare protein structures across species and analyze functional motifs.

```python
import gget

# Define genes for comparison
human_gene = "ENSG00000169174"  # PCSK9
mouse_gene = "ENSMUSG00000044254"  # Pcsk9

print("Comparative Structural Biology Workflow")
print("=" * 50)

# Step 1: Get gene information
print("\n1. Getting gene information...")
human_info = gget.info([human_gene])
mouse_info = gget.info([mouse_gene])

print(f"Human: {human_info['gene_name'].iloc[0]}")
print(f"Mouse: {mouse_info['gene_name'].iloc[0]}")

# Step 2: Retrieve protein sequences
print("\n2. Retrieving protein sequences...")
human_seq = gget.seq(human_gene, translate=True)
mouse_seq = gget.seq(mouse_gene, translate=True)

# Save to file for alignment
with open("pcsk9_sequences.fasta", "w") as f:
    f.write(human_seq)
    f.write("\n")
    f.write(mouse_seq)

# Step 3: Align sequences
print("\n3. Aligning sequences...")
alignment = gget.muscle("pcsk9_sequences.fasta")
print("Alignment completed. Visualizing in ClustalW format:")
print(alignment)

# Step 4: Get existing structures from PDB
print("\n4. Searching PDB for existing structures...")
# Search by sequence using BLAST
pdb_results = gget.blast(human_seq, database="pdbaa", limit=5)
print("Top PDB matches:")
print(pdb_results[["Description", "Max Score", "Query Coverage"]])

# Download top structure
if len(pdb_results) > 0:
    # Extract PDB ID from description (usually format: "PDB|XXXX|...")
    pdb_id = pdb_results.iloc[0]["Description"].split("|")[1]
    print(f"\nDownloading PDB structure: {pdb_id}")
    gget.pdb(pdb_id, save=True)

# Step 5: Predict AlphaFold structures
print("\n5. Predicting structures with AlphaFold...")
# Note: This requires gget setup alphafold and is computationally intensive
# Uncomment to run:
# human_structure = gget.alphafold(human_seq, plot=True)
# mouse_structure = gget.alphafold(mouse_seq, plot=True)
print("(AlphaFold prediction skipped - uncomment to run)")

# Step 6: Identify functional motifs
print("\n6. Identifying functional motifs with ELM...")
# Note: Requires gget setup elm
# Uncomment to run:
# human_ortholog_df, human_regex_df = gget.elm(human_seq)
# print("Human PCSK9 functional motifs:")
# print(human_regex_df)
print("(ELM analysis skipped - uncomment to run)")

# Step 7: Get orthology information
print("\n7. Getting orthology information from Bgee...")
orthologs = gget.bgee(human_gene, type="orthologs")
print("PCSK9 orthologs:")
print(orthologs)

print("\nComparative structural biology workflow completed!")
```

---

## Cancer Genomics Analysis

Analyze cancer-associated genes and their mutations.

```python
import gget
import matplotlib.pyplot as plt

print("Cancer Genomics Analysis Workflow")
print("=" * 50)

# Step 1: Search for cancer-related genes
print("\n1. Searching for breast cancer genes...")
genes = gget.search(["breast", "cancer", "BRCA"],
                    species="homo_sapiens",
                    andor="or",
                    limit=20)
print(f"Found {len(genes)} genes")

# Focus on specific genes
target_genes = ["BRCA1", "BRCA2", "TP53", "PIK3CA", "ESR1"]
print(f"\nAnalyzing: {', '.join(target_genes)}")

# Step 2: Get gene information
print("\n2. Getting gene information...")
gene_search = []
for gene in target_genes:
    result = gget.search([gene], species="homo_sapiens", limit=1)
    if len(result) > 0:
        gene_search.append(result.iloc[0])

gene_df = pd.DataFrame(gene_search)
gene_ids = gene_df["ensembl_id"].tolist()

# Step 3: Get disease associations
print("\n3. Getting disease associations from OpenTargets...")
for gene_id, gene_name in zip(gene_ids, target_genes):
    print(f"\n{gene_name} disease associations:")
    diseases = gget.opentargets(gene_id, resource="diseases", limit=3)
    print(diseases[["disease_name", "overall_score"]])

# Step 4: Get drug associations
print("\n4. Getting drug associations...")
for gene_id, gene_name in zip(gene_ids[:3], target_genes[:3]):
    print(f"\n{gene_name} drug associations:")
    drugs = gget.opentargets(gene_id, resource="drugs", limit=3)
    if len(drugs) > 0:
        print(drugs[["drug_name", "drug_type", "max_phase_for_all_diseases"]])

# Step 5: Search cBioPortal for studies
print("\n5. Searching cBioPortal for breast cancer studies...")
studies = gget.cbio_search(["breast", "cancer"])
print(f"Found {len(studies)} studies")
print(studies[:5])

# Step 6: Create cancer genomics heatmap
print("\n6. Creating cancer genomics heatmap...")
if len(studies) > 0:
    # Select relevant studies
    selected_studies = studies[:2]  # Top 2 studies

    gget.cbio_plot(
        selected_studies,
        target_genes,
        stratification="cancer_type",
        variation_type="mutation_occurrences",
        show=False
    )
    print("Heatmap saved to ./gget_cbio_figures/")

# Step 7: Query COSMIC database (requires setup)
print("\n7. Querying COSMIC database...")
# Note: Requires COSMIC account and database download
# Uncomment to run:
# for gene in target_genes[:2]:
#     cosmic_results = gget.cosmic(
#         gene,
#         cosmic_tsv_path="cosmic_cancer.tsv",
#         limit=10
#     )
#     print(f"\n{gene} mutations in COSMIC:")
#     print(cosmic_results)
print("(COSMIC query skipped - requires database download)")

# Step 8: Enrichment analysis
print("\n8. Performing pathway enrichment...")
enrichment = gget.enrichr(target_genes, database="pathway", plot=True)
print("\nTop enriched pathways:")
print(enrichment.head(10))

print("\nCancer genomics analysis completed!")
```

---

## Single-Cell Expression Analysis

Analyze single-cell RNA-seq data for specific cell types and tissues.

```python
import gget
import scanpy as sc

print("Single-Cell Expression Analysis Workflow")
print("=" * 50)

# Note: Requires gget setup cellxgene

# Step 1: Define genes and cell types of interest
genes_of_interest = ["ACE2", "TMPRSS2", "CD4", "CD8A"]
tissue = "lung"
cell_types = ["type ii pneumocyte", "macrophage", "t cell"]

print(f"\nAnalyzing genes: {', '.join(genes_of_interest)}")
print(f"Tissue: {tissue}")
print(f"Cell types: {', '.join(cell_types)}")

# Step 2: Get metadata first
print("\n1. Retrieving metadata...")
metadata = gget.cellxgene(
    gene=genes_of_interest,
    tissue=tissue,
    species="homo_sapiens",
    meta_only=True
)
print(f"Found {len(metadata)} datasets")
print(metadata.head())

# Step 3: Download count matrices
print("\n2. Downloading single-cell data...")
# Note: This can be a large download
adata = gget.cellxgene(
    gene=genes_of_interest,
    tissue=tissue,
    species="homo_sapiens",
    census_version="stable"
)
print(f"AnnData shape: {adata.shape}")
print(f"Genes: {adata.n_vars}")
print(f"Cells: {adata.n_obs}")

# Step 4: Basic QC and filtering with scanpy
print("\n3. Performing quality control...")
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
print(f"After QC - Cells: {adata.n_obs}, Genes: {adata.n_vars}")

# Step 5: Normalize and log-transform
print("\n4. Normalizing data...")
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

# Step 6: Calculate gene expression statistics
print("\n5. Calculating expression statistics...")
for gene in genes_of_interest:
    if gene in adata.var_names:
        expr = adata[:, gene].X.toarray().flatten()
        print(f"\n{gene} expression:")
        print(f"  Mean: {expr.mean():.3f}")
        print(f"  Median: {np.median(expr):.3f}")
        print(f"  % expressing: {(expr > 0).sum() / len(expr) * 100:.1f}%")

# Step 7: Get tissue expression from ARCHS4 for comparison
print("\n6. Getting bulk tissue expression from ARCHS4...")
for gene in genes_of_interest:
    tissue_expr = gget.archs4(gene, which="tissue")
    lung_expr = tissue_expr[tissue_expr["tissue"] == "lung"]
    if len(lung_expr) > 0:
        print(f"\n{gene} in lung (ARCHS4):")
        print(f"  Median: {lung_expr['median'].iloc[0]:.3f}")

# Step 8: Enrichment analysis
print("\n7. Performing enrichment analysis...")
enrichment = gget.enrichr(genes_of_interest, database="celltypes", plot=True)
print("\nTop cell type associations:")
print(enrichment.head(10))

# Step 9: Get disease associations
print("\n8. Getting disease associations...")
for gene in genes_of_interest:
    gene_search = gget.search([gene], species="homo_sapiens", limit=1)
    if len(gene_search) > 0:
        gene_id = gene_search["ensembl_id"].iloc[0]
        diseases = gget.opentargets(gene_id, resource="diseases", limit=3)
        print(f"\n{gene} disease associations:")
        print(diseases[["disease_name", "overall_score"]])

print("\nSingle-cell expression analysis completed!")
```

---

## Building Reference Transcriptomes

Prepare reference data for RNA-seq analysis pipelines.

```bash
#!/bin/bash
# Reference transcriptome building workflow

echo "Reference Transcriptome Building Workflow"
echo "=========================================="

# Step 1: List available species
echo -e "\n1. Listing available species..."
gget ref --list_species > available_species.txt
echo "Available species saved to available_species.txt"

# Step 2: Download reference files for human
echo -e "\n2. Downloading human reference files..."
SPECIES="homo_sapiens"
RELEASE=110  # Specify release for reproducibility

# Download GTF annotation
echo "Downloading GTF annotation..."
gget ref -w gtf -r $RELEASE -d $SPECIES -o human_ref_gtf.json

# Download cDNA sequences
echo "Downloading cDNA sequences..."
gget ref -w cdna -r $RELEASE -d $SPECIES -o human_ref_cdna.json

# Download protein sequences
echo "Downloading protein sequences..."
gget ref -w pep -r $RELEASE -d $SPECIES -o human_ref_pep.json

# Step 3: Build kallisto index (if kallisto is installed)
echo -e "\n3. Building kallisto index..."
if command -v kallisto &> /dev/null; then
    # Get cDNA FASTA file from download
    CDNA_FILE=$(ls *.cdna.all.fa.gz)
    if [ -f "$CDNA_FILE" ]; then
        kallisto index -i transcriptome.idx $CDNA_FILE
        echo "Kallisto index created: transcriptome.idx"
    else
        echo "cDNA FASTA file not found"
    fi
else
    echo "kallisto not installed, skipping index building"
fi

# Step 4: Download genome for alignment-based methods
echo -e "\n4. Downloading genome sequence..."
gget ref -w dna -r $RELEASE -d $SPECIES -o human_ref_dna.json

# Step 5: Get gene information for genes of interest
echo -e "\n5. Getting information for specific genes..."
gget search -s $SPECIES "TP53 BRCA1 BRCA2" -o key_genes.csv

echo -e "\nReference transcriptome building completed!"
```

```python
# Python version
import gget
import json

print("Reference Transcriptome Building Workflow")
print("=" * 50)

# Configuration
species = "homo_sapiens"
release = 110
genes_of_interest = ["TP53", "BRCA1", "BRCA2", "MYC", "EGFR"]

# Step 1: Get reference information
print("\n1. Getting reference information...")
ref_info = gget.ref(species, release=release)

# Save reference information
with open("reference_info.json", "w") as f:
    json.dump(ref_info, f, indent=2)
print("Reference information saved to reference_info.json")

# Step 2: Download specific files
print("\n2. Downloading reference files...")
# GTF annotation
gget.ref(species, which="gtf", release=release, download=True)
# cDNA sequences
gget.ref(species, which="cdna", release=release, download=True)

# Step 3: Get information for genes of interest
print(f"\n3. Getting information for {len(genes_of_interest)} genes...")
gene_data = []
for gene in genes_of_interest:
    result = gget.search([gene], species=species, limit=1)
    if len(result) > 0:
        gene_data.append(result.iloc[0])

# Get detailed info
if gene_data:
    gene_ids = [g["ensembl_id"] for g in gene_data]
    detailed_info = gget.info(gene_ids)
    detailed_info.to_csv("genes_of_interest_info.csv", index=False)
    print("Gene information saved to genes_of_interest_info.csv")

# Step 4: Get sequences
print("\n4. Retrieving sequences...")
sequences_nt = gget.seq(gene_ids)
sequences_aa = gget.seq(gene_ids, translate=True)

with open("key_genes_nucleotide.fasta", "w") as f:
    f.write(sequences_nt)
with open("key_genes_protein.fasta", "w") as f:
    f.write(sequences_aa)

print("\nReference transcriptome building completed!")
print(f"Files created:")
print("  - reference_info.json")
print("  - genes_of_interest_info.csv")
print("  - key_genes_nucleotide.fasta")
print("  - key_genes_protein.fasta")
```

---

## Mutation Impact Assessment

Analyze the impact of genetic mutations on protein structure and function.

```python
import gget
import pandas as pd

print("Mutation Impact Assessment Workflow")
print("=" * 50)

# Define mutations to analyze
mutations = [
    {"gene": "TP53", "mutation": "c.818G>A", "description": "R273H hotspot"},
    {"gene": "EGFR", "mutation": "c.2573T>G", "description": "L858R activating"},
]

# Step 1: Get gene information
print("\n1. Getting gene information...")
for mut in mutations:
    results = gget.search([mut["gene"]], species="homo_sapiens", limit=1)
    if len(results) > 0:
        mut["ensembl_id"] = results["ensembl_id"].iloc[0]
        print(f"{mut['gene']}: {mut['ensembl_id']}")

# Step 2: Get sequences
print("\n2. Retrieving wild-type sequences...")
for mut in mutations:
    # Get nucleotide sequence
    nt_seq = gget.seq(mut["ensembl_id"])
    mut["wt_sequence"] = nt_seq

    # Get protein sequence
    aa_seq = gget.seq(mut["ensembl_id"], translate=True)
    mut["wt_protein"] = aa_seq

# Step 3: Generate mutated sequences
print("\n3. Generating mutated sequences...")
# Create mutation dataframe for gget mutate
mut_df = pd.DataFrame({
    "seq_ID": [m["gene"] for m in mutations],
    "mutation": [m["mutation"] for m in mutations]
})

# For each mutation
for mut in mutations:
    # Extract sequence from FASTA
    lines = mut["wt_sequence"].split("\n")
    seq = "".join(lines[1:])

    # Create single mutation df
    single_mut = pd.DataFrame({
        "seq_ID": [mut["gene"]],
        "mutation": [mut["mutation"]]
    })

    # Generate mutated sequence
    mutated = gget.mutate([seq], mutations=single_mut)
    mut["mutated_sequence"] = mutated

print("Mutated sequences generated")

# Step 4: Get existing structure information
print("\n4. Getting structure information...")
for mut in mutations:
    # Get info with PDB IDs
    info = gget.info([mut["ensembl_id"]], pdb=True)

    if "pdb_id" in info.columns and pd.notna(info["pdb_id"].iloc[0]):
        pdb_ids = info["pdb_id"].iloc[0].split(";")
        print(f"\n{mut['gene']} PDB structures: {', '.join(pdb_ids[:3])}")

        # Download first structure
        if len(pdb_ids) > 0:
            pdb_id = pdb_ids[0].strip()
            mut["pdb_id"] = pdb_id
            gget.pdb(pdb_id, save=True)
    else:
        print(f"\n{mut['gene']}: No PDB structure available")
        mut["pdb_id"] = None

# Step 5: Predict structures with AlphaFold (optional)
print("\n5. Predicting structures with AlphaFold...")
# Note: Requires gget setup alphafold and is computationally intensive
# Uncomment to run:
# for mut in mutations:
#     print(f"Predicting {mut['gene']} wild-type structure...")
#     wt_structure = gget.alphafold(mut["wt_protein"])
#
#     print(f"Predicting {mut['gene']} mutant structure...")
#     # Would need to translate mutated sequence first
#     # mutant_structure = gget.alphafold(mutated_protein)
print("(AlphaFold prediction skipped - uncomment to run)")

# Step 6: Find functional motifs
print("\n6. Identifying functional motifs...")
# Note: Requires gget setup elm
# Uncomment to run:
# for mut in mutations:
#     ortholog_df, regex_df = gget.elm(mut["wt_protein"])
#     print(f"\n{mut['gene']} functional motifs:")
#     print(regex_df)
print("(ELM analysis skipped - uncomment to run)")

# Step 7: Get disease associations
print("\n7. Getting disease associations...")
for mut in mutations:
    diseases = gget.opentargets(
        mut["ensembl_id"],
        resource="diseases",
        limit=5
    )
    print(f"\n{mut['gene']} ({mut['description']}) disease associations:")
    print(diseases[["disease_name", "overall_score"]])

# Step 8: Query COSMIC for mutation frequency
print("\n8. Querying COSMIC database...")
# Note: Requires COSMIC database download
# Uncomment to run:
# for mut in mutations:
#     cosmic_results = gget.cosmic(
#         mut["mutation"],
#         cosmic_tsv_path="cosmic_cancer.tsv",
#         limit=10
#     )
#     print(f"\n{mut['gene']} {mut['mutation']} in COSMIC:")
#     print(cosmic_results)
print("(COSMIC query skipped - requires database download)")

print("\nMutation impact assessment completed!")
```

---

## Drug Target Discovery

Identify and validate potential drug targets for specific diseases.

```python
import gget
import pandas as pd

print("Drug Target Discovery Workflow")
print("=" * 50)

# Step 1: Search for disease-related genes
disease = "alzheimer"
print(f"\n1. Searching for {disease} disease genes...")
genes = gget.search([disease], species="homo_sapiens", limit=50)
print(f"Found {len(genes)} potential genes")

# Step 2: Get detailed information
print("\n2. Getting detailed gene information...")
gene_ids = genes["ensembl_id"].tolist()[:20]  # Top 20
gene_info = gget.info(gene_ids[:10])  # Limit to avoid timeout

# Step 3: Get disease associations from OpenTargets
print("\n3. Getting disease associations...")
disease_scores = []
for gene_id, gene_name in zip(gene_info["ensembl_id"], gene_info["gene_name"]):
    diseases = gget.opentargets(gene_id, resource="diseases", limit=10)

    # Filter for Alzheimer's disease
    alzheimer = diseases[diseases["disease_name"].str.contains("Alzheimer", case=False, na=False)]

    if len(alzheimer) > 0:
        disease_scores.append({
            "ensembl_id": gene_id,
            "gene_name": gene_name,
            "disease_score": alzheimer["overall_score"].max()
        })

disease_df = pd.DataFrame(disease_scores).sort_values("disease_score", ascending=False)
print("\nTop disease-associated genes:")
print(disease_df.head(10))

# Step 4: Get tractability information
print("\n4. Assessing target tractability...")
top_targets = disease_df.head(5)
for _, row in top_targets.iterrows():
    tractability = gget.opentargets(
        row["ensembl_id"],
        resource="tractability"
    )
    print(f"\n{row['gene_name']} tractability:")
    print(tractability)

# Step 5: Get expression data
print("\n5. Getting tissue expression data...")
for _, row in top_targets.iterrows():
    # Brain expression from OpenTargets
    expression = gget.opentargets(
        row["ensembl_id"],
        resource="expression",
        filter_tissue="brain"
    )
    print(f"\n{row['gene_name']} brain expression:")
    print(expression)

    # Tissue expression from ARCHS4
    tissue_expr = gget.archs4(row["gene_name"], which="tissue")
    brain_expr = tissue_expr[tissue_expr["tissue"].str.contains("brain", case=False, na=False)]
    print(f"ARCHS4 brain expression:")
    print(brain_expr)

# Step 6: Check for existing drugs
print("\n6. Checking for existing drugs...")
for _, row in top_targets.iterrows():
    drugs = gget.opentargets(row["ensembl_id"], resource="drugs", limit=5)
    print(f"\n{row['gene_name']} drug associations:")
    if len(drugs) > 0:
        print(drugs[["drug_name", "drug_type", "max_phase_for_all_diseases"]])
    else:
        print("No drugs found")

# Step 7: Get protein-protein interactions
print("\n7. Getting protein-protein interactions...")
for _, row in top_targets.iterrows():
    interactions = gget.opentargets(
        row["ensembl_id"],
        resource="interactions",
        limit=10
    )
    print(f"\n{row['gene_name']} interacts with:")
    if len(interactions) > 0:
        print(interactions[["gene_b_symbol", "interaction_score"]])

# Step 8: Enrichment analysis
print("\n8. Performing pathway enrichment...")
gene_list = top_targets["gene_name"].tolist()
enrichment = gget.enrichr(gene_list, database="pathway", plot=True)
print("\nTop enriched pathways:")
print(enrichment.head(10))

# Step 9: Get structure information
print("\n9. Getting structure information...")
for _, row in top_targets.iterrows():
    info = gget.info([row["ensembl_id"]], pdb=True)

    if "pdb_id" in info.columns and pd.notna(info["pdb_id"].iloc[0]):
        pdb_ids = info["pdb_id"].iloc[0].split(";")
        print(f"\n{row['gene_name']} PDB structures: {', '.join(pdb_ids[:3])}")
    else:
        print(f"\n{row['gene_name']}: No PDB structure available")
        # Could predict with AlphaFold
        print(f"  Consider AlphaFold prediction")

# Step 10: Generate target summary report
print("\n10. Generating target summary report...")
report = []
for _, row in top_targets.iterrows():
    report.append({
        "Gene": row["gene_name"],
        "Ensembl ID": row["ensembl_id"],
        "Disease Score": row["disease_score"],
        "Target Status": "High Priority"
    })

report_df = pd.DataFrame(report)
report_df.to_csv("drug_targets_report.csv", index=False)
print("\nTarget report saved to drug_targets_report.csv")

print("\nDrug target discovery workflow completed!")
```

---

## Tips for Workflow Development

### Error Handling
```python
import gget

def safe_gget_call(func, *args, **kwargs):
    """Wrapper for gget calls with error handling"""
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        print(f"Error in {func.__name__}: {str(e)}")
        return None

# Usage
result = safe_gget_call(gget.search, ["ACE2"], species="homo_sapiens")
if result is not None:
    print(result)
```

### Rate Limiting
```python
import time
import gget

def rate_limited_queries(gene_ids, delay=1):
    """Query multiple genes with rate limiting"""
    results = []
    for i, gene_id in enumerate(gene_ids):
        print(f"Querying {i+1}/{len(gene_ids)}: {gene_id}")
        result = gget.info([gene_id])
        results.append(result)

        if i < len(gene_ids) - 1:  # Don't sleep after last query
            time.sleep(delay)

    return pd.concat(results, ignore_index=True)
```

### Caching Results
```python
import os
import pickle
import gget

def cached_gget(cache_file, func, *args, **kwargs):
    """Cache gget results to avoid repeated queries"""
    if os.path.exists(cache_file):
        print(f"Loading from cache: {cache_file}")
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    result = func(*args, **kwargs)

    with open(cache_file, "wb") as f:
        pickle.dump(result, f)
    print(f"Saved to cache: {cache_file}")

    return result

# Usage
result = cached_gget("ace2_info.pkl", gget.info, ["ENSG00000130234"])
```

---

These workflows demonstrate how to combine multiple gget modules for comprehensive bioinformatics analyses. Adapt them to your specific research questions and data types.
