---
title: "Kegg Database"
description: "Direct REST API access to KEGG (academic use only). Pathway analysis, gene-pathway mapping, metabolic pathways, drug interactions, ID conversion. For Python workflows with multiple databases, prefer bioservices. Use this for direct HTTP/REST work ..."
category: "research"
source: "community"
author: "Community"
tags: ["kegg", "database"]
date: 2026-03-20
---

# KEGG Database

## Overview

KEGG (Kyoto Encyclopedia of Genes and Genomes) is a comprehensive bioinformatics resource for biological pathway analysis and molecular interaction networks.

**Important**: KEGG API is made available only for academic use by academic users.

## When to Use This Skill

This skill should be used when querying pathways, genes, compounds, enzymes, diseases, and drugs across multiple organisms using KEGG's REST API.

## Quick Start

The skill provides:
1. Python helper functions (`scripts/kegg_api.py`) for all KEGG REST API operations
2. Comprehensive reference documentation (`references/kegg_reference.md`) with detailed API specifications

When users request KEGG data, determine which operation is needed and use the appropriate function from `scripts/kegg_api.py`.

## Core Operations

### 1. Database Information (`kegg_info`)

Retrieve metadata and statistics about KEGG databases.

**When to use**: Understanding database structure, checking available data, getting release information.

**Usage**:
```python
from scripts.kegg_api import kegg_info

# Get pathway database info
info = kegg_info('pathway')

# Get organism-specific info
hsa_info = kegg_info('hsa')  # Human genome
```

**Common databases**: `kegg`, `pathway`, `module`, `brite`, `genes`, `genome`, `compound`, `glycan`, `reaction`, `enzyme`, `disease`, `drug`

### 2. Listing Entries (`kegg_list`)

List entry identifiers and names from KEGG databases.

**When to use**: Getting all pathways for an organism, listing genes, retrieving compound catalogs.

**Usage**:
```python
from scripts.kegg_api import kegg_list

# List all reference pathways
pathways = kegg_list('pathway')

# List human-specific pathways
hsa_pathways = kegg_list('pathway', 'hsa')

# List specific genes (max 10)
genes = kegg_list('hsa:10458+hsa:10459')
```

**Common organism codes**: `hsa` (human), `mmu` (mouse), `dme` (fruit fly), `sce` (yeast), `eco` (E. coli)

### 3. Searching (`kegg_find`)

Search KEGG databases by keywords or molecular properties.

**When to use**: Finding genes by name/description, searching compounds by formula or mass, discovering entries by keywords.

**Usage**:
```python
from scripts.kegg_api import kegg_find

# Keyword search
results = kegg_find('genes', 'p53')
shiga_toxin = kegg_find('genes', 'shiga toxin')

# Chemical formula search (exact match)
compounds = kegg_find('compound', 'C7H10N4O2', 'formula')

# Molecular weight range search
drugs = kegg_find('drug', '300-310', 'exact_mass')
```

**Search options**: `formula` (exact match), `exact_mass` (range), `mol_weight` (range)

### 4. Retrieving Entries (`kegg_get`)

Get complete database entries or specific data formats.

**When to use**: Retrieving pathway details, getting gene/protein sequences, downloading pathway maps, accessing compound structures.

**Usage**:
```python
from scripts.kegg_api import kegg_get

# Get pathway entry
pathway = kegg_get('hsa00010')  # Glycolysis pathway

# Get multiple entries (max 10)
genes = kegg_get(['hsa:10458', 'hsa:10459'])

# Get protein sequence (FASTA)
sequence = kegg_get('hsa:10458', 'aaseq')

# Get nucleotide sequence
nt_seq = kegg_get('hsa:10458', 'ntseq')

# Get compound structure
mol_file = kegg_get('cpd:C00002', 'mol')  # ATP in MOL format

# Get pathway as JSON (single entry only)
pathway_json = kegg_get('hsa05130', 'json')

# Get pathway image (single entry only)
pathway_img = kegg_get('hsa05130', 'image')
```

**Output formats**: `aaseq` (protein FASTA), `ntseq` (nucleotide FASTA), `mol` (MOL format), `kcf` (KCF format), `image` (PNG), `kgml` (XML), `json` (pathway JSON)

**Important**: Image, KGML, and JSON formats allow only one entry at a time.

### 5. ID Conversion (`kegg_conv`)

Convert identifiers between KEGG and external databases.

**When to use**: Integrating KEGG data with other databases, mapping gene IDs, converting compound identifiers.

**Usage**:
```python
from scripts.kegg_api import kegg_conv

# Convert all human genes to NCBI Gene IDs
conversions = kegg_conv('ncbi-geneid', 'hsa')

# Convert specific gene
gene_id = kegg_conv('ncbi-geneid', 'hsa:10458')

# Convert to UniProt
uniprot_id = kegg_conv('uniprot', 'hsa:10458')

# Convert compounds to PubChem
pubchem_ids = kegg_conv('pubchem', 'compound')

# Reverse conversion (NCBI Gene ID to KEGG)
kegg_id = kegg_conv('hsa', 'ncbi-geneid')
```

**Supported conversions**: `ncbi-geneid`, `ncbi-proteinid`, `uniprot`, `pubchem`, `chebi`

### 6. Cross-Referencing (`kegg_link`)

Find related entries within and between KEGG databases.

**When to use**: Finding pathways containing genes, getting genes in a pathway, mapping genes to KO groups, finding compounds in pathways.

**Usage**:
```python
from scripts.kegg_api import kegg_link

# Find pathways linked to human genes
pathways = kegg_link('pathway', 'hsa')

# Get genes in a specific pathway
genes = kegg_link('genes', 'hsa00010')  # Glycolysis genes

# Find pathways containing a specific gene
gene_pathways = kegg_link('pathway', 'hsa:10458')

# Find compounds in a pathway
compounds = kegg_link('compound', 'hsa00010')

# Map genes to KO (orthology) groups
ko_groups = kegg_link('ko', 'hsa:10458')
```

**Common links**: genes ↔ pathway, pathway ↔ compound, pathway ↔ enzyme, genes ↔ ko (orthology)

### 7. Drug-Drug Interactions (`kegg_ddi`)

Check for drug-drug interactions.

**When to use**: Analyzing drug combinations, checking for contraindications, pharmacological research.

**Usage**:
```python
from scripts.kegg_api import kegg_ddi

# Check single drug
interactions = kegg_ddi('D00001')

# Check multiple drugs (max 10)
interactions = kegg_ddi(['D00001', 'D00002', 'D00003'])
```

## Common Analysis Workflows

### Workflow 1: Gene to Pathway Mapping

**Use case**: Finding pathways associated with genes of interest (e.g., for pathway enrichment analysis).

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# Step 1: Find gene ID by name
gene_results = kegg_find('genes', 'p53')

# Step 2: Link gene to pathways
pathways = kegg_link('pathway', 'hsa:7157')  # TP53 gene

# Step 3: Get detailed pathway information
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[1].replace('path:', '')
        pathway_info = kegg_get(pathway_id)
        # Process pathway information
```

### Workflow 2: Pathway Enrichment Context

**Use case**: Getting all genes in organism pathways for enrichment analysis.

```python
from scripts.kegg_api import kegg_list, kegg_link

# Step 1: List all human pathways
pathways = kegg_list('pathway', 'hsa')

# Step 2: For each pathway, get associated genes
for pathway_line in pathways.split('\n'):
    if pathway_line:
        pathway_id = pathway_line.split('\t')[0]
        genes = kegg_link('genes', pathway_id)
        # Process genes for enrichment analysis
```

### Workflow 3: Compound to Pathway Analysis

**Use case**: Finding metabolic pathways containing compounds of interest.

```python
from scripts.kegg_api import kegg_find, kegg_link, kegg_get

# Step 1: Search for compound
compound_results = kegg_find('compound', 'glucose')

# Step 2: Link compound to reactions
reactions = kegg_link('reaction', 'cpd:C00031')  # Glucose

# Step 3: Link reactions to pathways
pathways = kegg_link('pathway', 'rn:R00299')  # Specific reaction

# Step 4: Get pathway details
pathway_info = kegg_get('map00010')  # Glycolysis
```

### Workflow 4: Cross-Database Integration

**Use case**: Integrating KEGG data with UniProt, NCBI, or PubChem databases.

```python
from scripts.kegg_api import kegg_conv, kegg_get

# Step 1: Convert KEGG gene IDs to external database IDs
uniprot_map = kegg_conv('uniprot', 'hsa')
ncbi_map = kegg_conv('ncbi-geneid', 'hsa')

# Step 2: Parse conversion results
for line in uniprot_map.split('\n'):
    if line:
        kegg_id, uniprot_id = line.split('\t')
        # Use external IDs for integration

# Step 3: Get sequences using KEGG
sequence = kegg_get('hsa:10458', 'aaseq')
```

### Workflow 5: Organism-Specific Pathway Analysis

**Use case**: Comparing pathways across different organisms.

```python
from scripts.kegg_api import kegg_list, kegg_get

# Step 1: List pathways for multiple organisms
human_pathways = kegg_list('pathway', 'hsa')
mouse_pathways = kegg_list('pathway', 'mmu')
yeast_pathways = kegg_list('pathway', 'sce')

# Step 2: Get reference pathway for comparison
ref_pathway = kegg_get('map00010')  # Reference glycolysis

# Step 3: Get organism-specific versions
hsa_glycolysis = kegg_get('hsa00010')
mmu_glycolysis = kegg_get('mmu00010')
```

## Pathway Categories

KEGG organizes pathways into seven major categories. When interpreting pathway IDs or recommending pathways to users:

1. **Metabolism** (e.g., `map00010` - Glycolysis, `map00190` - Oxidative phosphorylation)
2. **Genetic Information Processing** (e.g., `map03010` - Ribosome, `map03040` - Spliceosome)
3. **Environmental Information Processing** (e.g., `map04010` - MAPK signaling, `map02010` - ABC transporters)
4. **Cellular Processes** (e.g., `map04140` - Autophagy, `map04210` - Apoptosis)
5. **Organismal Systems** (e.g., `map04610` - Complement cascade, `map04910` - Insulin signaling)
6. **Human Diseases** (e.g., `map05200` - Pathways in cancer, `map05010` - Alzheimer disease)
7. **Drug Development** (chronological and target-based classifications)

Reference `references/kegg_reference.md` for detailed pathway lists and classifications.

## Important Identifiers and Formats

### Pathway IDs
- `map#####` - Reference pathway (generic, not organism-specific)
- `hsa#####` - Human pathway
- `mmu#####` - Mouse pathway

### Gene IDs
- Format: `organism:gene_number` (e.g., `hsa:10458`)

### Compound IDs
- Format: `cpd:C#####` (e.g., `cpd:C00002` for ATP)

### Drug IDs
- Format: `dr:D#####` (e.g., `dr:D00001`)

### Enzyme IDs
- Format: `ec:EC_number` (e.g., `ec:1.1.1.1`)

### KO (KEGG Orthology) IDs
- Format: `ko:K#####` (e.g., `ko:K00001`)

## API Limitations

Respect these constraints when using the KEGG API:

1. **Entry limits**: Maximum 10 entries per operation (except image/kgml/json: 1 entry only)
2. **Academic use**: API is for academic use only; commercial use requires licensing
3. **HTTP status codes**: Check for 200 (success), 400 (bad request), 404 (not found)
4. **Rate limiting**: No explicit limit, but avoid rapid-fire requests

## Detailed Reference

For comprehensive API documentation, database specifications, organism codes, and advanced usage, refer to `references/kegg_reference.md`. This includes:

- Complete list of KEGG databases
- Detailed API operation syntax
- All organism codes
- HTTP status codes and error handling
- Integration with Biopython and R/Bioconductor
- Best practices for API usage

## Troubleshooting

**404 Not Found**: Entry or database doesn't exist; verify IDs and organism codes
**400 Bad Request**: Syntax error in API call; check parameter formatting
**Empty results**: Search term may not match entries; try broader keywords
**Image/KGML errors**: These formats only work with single entries; remove batch processing

## Additional Tools

For interactive pathway visualization and annotation:
- **KEGG Mapper**: https://www.kegg.jp/kegg/mapper/
- **BlastKOALA**: Automated genome annotation
- **GhostKOALA**: Metagenome/metatranscriptome annotation

---

## Reference: Kegg_Reference

# KEGG Database Reference

## Overview

KEGG (Kyoto Encyclopedia of Genes and Genomes) is a comprehensive bioinformatics resource that maintains manually curated pathway maps and molecular interaction networks. It provides "wiring diagrams of molecular interactions, reactions and relations" for understanding biological systems.

**Base URL**: https://rest.kegg.jp
**Official Documentation**: https://www.kegg.jp/kegg/rest/keggapi.html
**Access Restrictions**: KEGG API is made available only for academic use by academic users.

## KEGG Databases

KEGG integrates 16 primary databases organized into systems information, genomic information, chemical information, and health information categories:

### Systems Information
- **PATHWAY**: Manually drawn pathway maps for metabolism, genetic information processing, environmental information processing, cellular processes, organismal systems, human diseases, and drug development
- **MODULE**: Functional units and building blocks of pathways
- **BRITE**: Hierarchical classifications and ontologies

### Genomic Information
- **GENOME**: Complete genomes with annotations
- **GENES**: Gene catalogs for all organisms
- **ORTHOLOGY**: Ortholog groups (KO: KEGG Orthology)
- **SSDB**: Sequence similarity database

### Chemical Information
- **COMPOUND**: Metabolites and other chemical substances
- **GLYCAN**: Glycan structures
- **REACTION**: Chemical reactions
- **RCLASS**: Reaction class (chemical structure transformation patterns)
- **ENZYME**: Enzyme nomenclature
- **NETWORK**: Network variations

### Health Information
- **DISEASE**: Human diseases with genetic and environmental factors
- **DRUG**: Approved drugs with chemical structures and target information
- **DGROUP**: Drug groups

### External Database Links
KEGG cross-references to external databases including:
- **PubMed**: Literature references
- **NCBI Gene**: Gene database
- **UniProt**: Protein sequences
- **PubChem**: Chemical compounds
- **ChEBI**: Chemical entities of biological interest

## REST API Operations

### 1. INFO - Database Metadata

**Syntax**: `/info/<database>`

Retrieves release information and statistics for a database.

**Examples**:
- `/info/kegg` - KEGG system information
- `/info/pathway` - Pathway database information
- `/info/hsa` - Human organism information

### 2. LIST - Entry Listings

**Syntax**: `/list/<database>[/<organism>]`

Lists entry identifiers and associated names.

**Parameters**:
- `database` - Database name (pathway, enzyme, genes, etc.) or entry (hsa:10458)
- `organism` - Optional organism code (e.g., hsa for human, eco for E. coli)

**Examples**:
- `/list/pathway` - All reference pathways
- `/list/pathway/hsa` - Human-specific pathways
- `/list/hsa:10458+ece:Z5100` - Specific gene entries (max 10)

**Organism Codes**: Three or four letter codes
- `hsa` - Homo sapiens (human)
- `mmu` - Mus musculus (mouse)
- `dme` - Drosophila melanogaster (fruit fly)
- `sce` - Saccharomyces cerevisiae (yeast)
- `eco` - Escherichia coli K-12 MG1655

### 3. FIND - Search Entries

**Syntax**: `/find/<database>/<query>[/<option>]`

Searches for entries by keywords or molecular properties.

**Parameters**:
- `database` - Database to search
- `query` - Search term or molecular property
- `option` - Optional: `formula`, `exact_mass`, `mol_weight`

**Search Fields** (database dependent):
- ENTRY, NAME, SYMBOL, GENE_NAME, DESCRIPTION, DEFINITION
- ORGANISM, TAXONOMY, ORTHOLOGY, PATHWAY, etc.

**Examples**:
- `/find/genes/shiga toxin` - Keyword search in genes
- `/find/compound/C7H10N4O2/formula` - Exact formula match
- `/find/drug/300-310/exact_mass` - Mass range search (300-310 Da)
- `/find/compound/300-310/mol_weight` - Molecular weight range

### 4. GET - Retrieve Entries

**Syntax**: `/get/<entry>[+<entry>...][/<option>]`

Retrieves full database entries or specific data formats.

**Parameters**:
- `entry` - Entry ID(s) (max 10, joined with +)
- `option` - Output format (optional)

**Output Options**:
- `aaseq` - Amino acid sequences (FASTA)
- `ntseq` - Nucleotide sequences (FASTA)
- `mol` - MOL format (compounds/drugs)
- `kcf` - KCF format (KEGG Chemical Function, compounds/drugs)
- `image` - PNG image (pathway maps, single entry only)
- `kgml` - KGML XML (pathway structure, single entry only)
- `json` - JSON format (pathway only, single entry only)

**Examples**:
- `/get/hsa00010` - Glycolysis pathway (human)
- `/get/hsa:10458+ece:Z5100` - Multiple genes (max 10)
- `/get/hsa:10458/aaseq` - Protein sequence
- `/get/cpd:C00002` - ATP compound entry
- `/get/hsa05130/json` - Pathways in cancer as JSON
- `/get/hsa05130/image` - Pathway map as PNG

**Image Restrictions**: Only one entry allowed with image option

### 5. CONV - ID Conversion

**Syntax**: `/conv/<target_db>/<source_db>`

Converts identifiers between KEGG and external databases.

**Supported Conversions**:
- `ncbi-geneid` ↔ KEGG genes
- `ncbi-proteinid` ↔ KEGG genes
- `uniprot` ↔ KEGG genes
- `pubchem` ↔ KEGG compounds/drugs
- `chebi` ↔ KEGG compounds/drugs

**Examples**:
- `/conv/ncbi-geneid/hsa` - All human genes to NCBI Gene IDs
- `/conv/hsa/ncbi-geneid` - NCBI Gene IDs to human genes (reverse)
- `/conv/uniprot/hsa:10458` - Specific gene to UniProt
- `/conv/pubchem/compound` - All compounds to PubChem IDs

### 6. LINK - Cross-References

**Syntax**: `/link/<target_db>/<source_db>`

Finds related entries within and between KEGG databases.

**Common Links**:
- genes ↔ pathway
- pathway ↔ compound
- pathway ↔ enzyme
- genes ↔ orthology (KO)
- compound ↔ reaction

**Examples**:
- `/link/pathway/hsa` - All pathways linked to human genes
- `/link/genes/hsa00010` - Genes in glycolysis pathway
- `/link/pathway/hsa:10458` - Pathways containing specific gene
- `/link/compound/hsa00010` - Compounds in pathway

### 7. DDI - Drug-Drug Interactions

**Syntax**: `/ddi/<drug>[+<drug>...]`

Retrieves drug-drug interaction information extracted from Japanese drug labels.

**Parameters**:
- `drug` - Drug entry ID(s) (max 10, joined with +)

**Examples**:
- `/ddi/D00001` - Interactions for single drug
- `/ddi/D00001+D00002` - Interactions between multiple drugs

## Pathway Classification

KEGG organizes pathways into seven major categories:

### 1. Metabolism
Carbohydrate, energy, lipid, nucleotide, amino acid, glycan biosynthesis and metabolism, cofactor and vitamin metabolism, terpenoid and polyketide metabolism, secondary metabolite biosynthesis, xenobiotics biodegradation

**Example pathways**:
- `map00010` - Glycolysis / Gluconeogenesis
- `map00020` - Citrate cycle (TCA cycle)
- `map00190` - Oxidative phosphorylation

### 2. Genetic Information Processing
Transcription, translation, folding/sorting/degradation, replication and repair

**Example pathways**:
- `map03010` - Ribosome
- `map03020` - RNA polymerase
- `map03040` - Spliceosome

### 3. Environmental Information Processing
Membrane transport, signal transduction

**Example pathways**:
- `map02010` - ABC transporters
- `map04010` - MAPK signaling pathway

### 4. Cellular Processes
Transport and catabolism, cell growth and death, cellular community, cell motility

**Example pathways**:
- `map04140` - Autophagy
- `map04210` - Apoptosis

### 5. Organismal Systems
Immune, endocrine, circulatory, digestive, nervous, sensory, development, environmental adaptation

**Example pathways**:
- `map04610` - Complement and coagulation cascades
- `map04910` - Insulin signaling pathway

### 6. Human Diseases
Cancer, immune diseases, neurodegenerative diseases, cardiovascular diseases, metabolic diseases, infectious diseases

**Example pathways**:
- `map05200` - Pathways in cancer
- `map05010` - Alzheimer disease

### 7. Drug Development
Chronological classification and target-based classification

## Common Identifiers and Naming

### Pathway IDs
- `map#####` - Reference pathway (generic)
- `hsa#####` - Human-specific pathway
- `mmu#####` - Mouse-specific pathway
- Format: organism code + 5-digit number

### Gene IDs
- `hsa:10458` - Human gene (organism:gene_id)
- Format: organism code + colon + gene number

### Compound IDs
- `cpd:C00002` - ATP
- Format: cpd:C#####

### Drug IDs
- `dr:D00001` - Drug entry
- Format: dr:D#####

### Enzyme IDs
- `ec:1.1.1.1` - Alcohol dehydrogenase
- Format: ec:EC_number

### KO (KEGG Orthology) IDs
- `ko:K00001` - Ortholog group
- Format: ko:K#####

## API Limitations and Best Practices

### Rate Limits and Restrictions
- Maximum 10 entries per single operation (except image/kgml: 1 entry)
- Academic use only - commercial use requires separate licensing
- No explicit rate limit documented, but avoid rapid-fire requests

### HTTP Status Codes
- `200` - Success
- `400` - Bad request (syntax error in query)
- `404` - Not found (entry or database doesn't exist)

### Best Practices
1. Always check HTTP status codes in responses
2. For bulk operations, batch entries using + (up to 10)
3. Cache results locally to reduce API calls
4. Use specific organism codes when possible for faster results
5. For pathway visualization, use the web interface or KGML/JSON formats
6. Parse tab-delimited output carefully (consistent format across operations)

## Integration with Other Tools

### Biopython Integration
Biopython provides `Bio.KEGG.REST` module for easier Python integration:
```python
from Bio.KEGG import REST
result = REST.kegg_list("pathway").read()
```

### KEGGREST (R/Bioconductor)
R users can use the KEGGREST package:
```r
library(KEGGREST)
pathways <- keggList("pathway")
```

## Common Analysis Workflows

### Workflow 1: Gene to Pathway Mapping
1. Get gene ID(s) from your organism
2. Use `/link/pathway/<gene_id>` to find associated pathways
3. Use `/get/<pathway_id>` to retrieve detailed pathway information

### Workflow 2: Pathway Enrichment Context
1. Use `/list/pathway/<org>` to get all organism pathways
2. Use `/link/genes/<pathway_id>` to get genes in each pathway
3. Perform statistical enrichment analysis

### Workflow 3: Compound to Reaction Mapping
1. Use `/find/compound/<name>` to find compound ID
2. Use `/link/reaction/<compound_id>` to find reactions
3. Use `/link/pathway/<reaction_id>` to find pathways containing reactions

### Workflow 4: ID Conversion for Integration
1. Use `/conv/uniprot/<org>` to map KEGG genes to UniProt
2. Use `/conv/ncbi-geneid/<org>` to map to NCBI Gene IDs
3. Integrate with other databases using converted IDs

## Additional Resources

- **KEGG Mapper**: https://www.kegg.jp/kegg/mapper/ - Interactive pathway mapping
- **BlastKOALA**: Automated annotation for sequenced genomes
- **GhostKOALA**: Annotation for metagenomes and metatranscriptomes
- **KEGG Modules**: https://www.kegg.jp/kegg/module.html
- **KEGG Brite**: https://www.kegg.jp/kegg/brite.html
