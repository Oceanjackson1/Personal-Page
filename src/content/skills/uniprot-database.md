---
title: "Uniprot Database"
description: "Direct REST API access to UniProt. Protein searches, FASTA retrieval, ID mapping, Swiss-Prot/TrEMBL. For Python workflows with multiple databases, prefer bioservices (unified interface to 40+ services). Use this for direct HTTP/REST work or UniPro..."
category: "research"
source: "community"
author: "Community"
tags: ["uniprot", "database"]
date: 2026-03-20
---

# UniProt Database

## Overview

UniProt is the world's leading comprehensive protein sequence and functional information resource. Search proteins by name, gene, or accession, retrieve sequences in FASTA format, perform ID mapping across databases, access Swiss-Prot/TrEMBL annotations via REST API for protein analysis.

## When to Use This Skill

This skill should be used when:
- Searching for protein entries by name, gene symbol, accession, or organism
- Retrieving protein sequences in FASTA or other formats
- Mapping identifiers between UniProt and external databases (Ensembl, RefSeq, PDB, etc.)
- Accessing protein annotations including GO terms, domains, and functional descriptions
- Batch retrieving multiple protein entries efficiently
- Querying reviewed (Swiss-Prot) vs. unreviewed (TrEMBL) protein data
- Streaming large protein datasets
- Building custom queries with field-specific search syntax

## Core Capabilities

### 1. Searching for Proteins

Search UniProt using natural language queries or structured search syntax.

**Common search patterns:**
```python
# Search by protein name
query = "insulin AND organism_name:\"Homo sapiens\""

# Search by gene name
query = "gene:BRCA1 AND reviewed:true"

# Search by accession
query = "accession:P12345"

# Search by sequence length
query = "length:[100 TO 500]"

# Search by taxonomy
query = "taxonomy_id:9606"  # Human proteins

# Search by GO term
query = "go:0005515"  # Protein binding
```

Use the API search endpoint: `https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**Supported formats:** JSON, TSV, Excel, XML, FASTA, RDF, TXT

### 2. Retrieving Individual Protein Entries

Retrieve specific protein entries by accession number.

**Accession number formats:**
- Classic: P12345, Q1AAA9, O15530 (6 characters: letter + 5 alphanumeric)
- Extended: A0A022YWF9 (10 characters for newer entries)

**Retrieve endpoint:** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

Example: `https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. Batch Retrieval and ID Mapping

Map protein identifiers between different database systems and retrieve multiple entries efficiently.

**ID Mapping workflow:**
1. Submit mapping job to: `https://rest.uniprot.org/idmapping/run`
2. Check job status: `https://rest.uniprot.org/idmapping/status/{jobId}`
3. Retrieve results: `https://rest.uniprot.org/idmapping/results/{jobId}`

**Supported databases for mapping:**
- UniProtKB AC/ID
- Gene names
- Ensembl, RefSeq, EMBL
- PDB, AlphaFoldDB
- KEGG, GO terms
- And many more (see `/references/id_mapping_databases.md`)

**Limitations:**
- Maximum 100,000 IDs per job
- Results stored for 7 days

### 4. Streaming Large Result Sets

For large queries that exceed pagination limits, use the stream endpoint:

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

The stream endpoint returns all results without pagination, suitable for downloading complete datasets.

### 5. Customizing Retrieved Fields

Specify exactly which fields to retrieve for efficient data transfer.

**Common fields:**
- `accession` - UniProt accession number
- `id` - Entry name
- `gene_names` - Gene name(s)
- `organism_name` - Organism
- `protein_name` - Protein names
- `sequence` - Amino acid sequence
- `length` - Sequence length
- `go_*` - Gene Ontology annotations
- `cc_*` - Comment fields (function, interaction, etc.)
- `ft_*` - Feature annotations (domains, sites, etc.)

**Example:** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

See `/references/api_fields.md` for complete field list.

## Python Implementation

For programmatic access, use the provided helper script `scripts/uniprot_client.py` which implements:

- `search_proteins(query, format)` - Search UniProt with any query
- `get_protein(accession, format)` - Retrieve single protein entry
- `map_ids(ids, from_db, to_db)` - Map between identifier types
- `batch_retrieve(accessions, format)` - Retrieve multiple entries
- `stream_results(query, format)` - Stream large result sets

**Alternative Python packages:**
- **Unipressed**: Modern, typed Python client for UniProt REST API
- **bioservices**: Comprehensive bioinformatics web services client

## Query Syntax Examples

**Boolean operators:**
```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

**Field-specific searches:**
```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

**Range queries:**
```
length:[100 TO 500]
mass:[50000 TO 100000]
```

**Wildcards:**
```
gene:BRCA*
protein_name:kinase*
```

See `/references/query_syntax.md` for comprehensive syntax documentation.

## Best Practices

1. **Use reviewed entries when possible**: Filter with `reviewed:true` for Swiss-Prot (manually curated) entries
2. **Specify format explicitly**: Choose the most appropriate format (FASTA for sequences, TSV for tabular data, JSON for programmatic parsing)
3. **Use field selection**: Only request fields you need to reduce bandwidth and processing time
4. **Handle pagination**: For large result sets, implement proper pagination or use the stream endpoint
5. **Cache results**: Store frequently accessed data locally to minimize API calls
6. **Rate limiting**: Be respectful of API resources; implement delays for large batch operations
7. **Check data quality**: TrEMBL entries are computational predictions; Swiss-Prot entries are manually reviewed

## Resources

### scripts/
`uniprot_client.py` - Python client with helper functions for common UniProt operations including search, retrieval, ID mapping, and streaming.

### references/
- `api_fields.md` - Complete list of available fields for customizing queries
- `id_mapping_databases.md` - Supported databases for ID mapping operations
- `query_syntax.md` - Comprehensive query syntax with advanced examples
- `api_examples.md` - Code examples in multiple languages (Python, curl, R)

## Additional Resources

- **API Documentation**: https://www.uniprot.org/help/api
- **Interactive API Explorer**: https://www.uniprot.org/api-documentation
- **REST Tutorial**: https://www.uniprot.org/help/uniprot_rest_tutorial
- **Query Syntax Help**: https://www.uniprot.org/help/query-fields
- **SPARQL Endpoint**: https://sparql.uniprot.org/ (for advanced graph queries)

---

## Reference: Api_Examples

# UniProt API Examples

Practical code examples for interacting with the UniProt REST API in multiple languages.

## Python Examples

### Example 1: Basic Search
```python
import requests

# Search for human insulin proteins
url = "https://rest.uniprot.org/uniprotkb/search"
params = {
    "query": "insulin AND organism_id:9606 AND reviewed:true",
    "format": "json",
    "size": 10
}

response = requests.get(url, params=params)
data = response.json()

for result in data['results']:
    print(f"{result['primaryAccession']}: {result['proteinDescription']['recommendedName']['fullName']['value']}")
```

### Example 2: Retrieve Protein Sequence
```python
import requests

# Get human insulin sequence in FASTA format
accession = "P01308"
url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"

response = requests.get(url)
print(response.text)
```

### Example 3: Custom Fields
```python
import requests

# Get specific fields only
url = "https://rest.uniprot.org/uniprotkb/search"
params = {
    "query": "gene:BRCA1 AND reviewed:true",
    "format": "tsv",
    "fields": "accession,gene_names,organism_name,length,cc_function"
}

response = requests.get(url, params=params)
print(response.text)
```

### Example 4: ID Mapping
```python
import requests
import time

def map_uniprot_ids(ids, from_db, to_db):
    # Submit job
    submit_url = "https://rest.uniprot.org/idmapping/run"
    data = {
        "from": from_db,
        "to": to_db,
        "ids": ",".join(ids)
    }

    response = requests.post(submit_url, data=data)
    job_id = response.json()["jobId"]

    # Poll for completion
    status_url = f"https://rest.uniprot.org/idmapping/status/{job_id}"
    while True:
        response = requests.get(status_url)
        status = response.json()
        if "results" in status or "failedIds" in status:
            break
        time.sleep(3)

    # Get results
    results_url = f"https://rest.uniprot.org/idmapping/results/{job_id}"
    response = requests.get(results_url)
    return response.json()

# Map UniProt IDs to PDB
ids = ["P01308", "P04637"]
mapping = map_uniprot_ids(ids, "UniProtKB_AC-ID", "PDB")
print(mapping)
```

### Example 5: Stream Large Results
```python
import requests

# Stream all reviewed human proteins
url = "https://rest.uniprot.org/uniprotkb/stream"
params = {
    "query": "organism_id:9606 AND reviewed:true",
    "format": "fasta"
}

response = requests.get(url, params=params, stream=True)

# Process in chunks
with open("human_proteins.fasta", "w") as f:
    for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
        if chunk:
            f.write(chunk)
```

### Example 6: Pagination
```python
import requests

def get_all_results(query, fields=None):
    """Get all results with pagination"""
    url = "https://rest.uniprot.org/uniprotkb/search"
    all_results = []

    params = {
        "query": query,
        "format": "json",
        "size": 500  # Max size per page
    }

    if fields:
        params["fields"] = ",".join(fields)

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        all_results.extend(data['results'])

        # Check for next page
        if 'next' in data:
            url = data['next']
        else:
            break

    return all_results

# Get all human kinases
results = get_all_results(
    "protein_name:kinase AND organism_id:9606 AND reviewed:true",
    fields=["accession", "gene_names", "protein_name"]
)
print(f"Found {len(results)} proteins")
```

## cURL Examples

### Example 1: Simple Search
```bash
# Search for insulin proteins
curl "https://rest.uniprot.org/uniprotkb/search?query=insulin&format=json&size=5"
```

### Example 2: Get Protein Entry
```bash
# Get human insulin in FASTA format
curl "https://rest.uniprot.org/uniprotkb/P01308.fasta"
```

### Example 3: Custom Fields
```bash
# Get specific fields in TSV format
curl "https://rest.uniprot.org/uniprotkb/search?query=gene:BRCA1&format=tsv&fields=accession,gene_names,length"
```

### Example 4: ID Mapping - Submit Job
```bash
# Submit mapping job
curl -X POST "https://rest.uniprot.org/idmapping/run" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "from=UniProtKB_AC-ID&to=PDB&ids=P01308,P04637"
```

### Example 5: ID Mapping - Get Results
```bash
# Get mapping results (replace JOB_ID)
curl "https://rest.uniprot.org/idmapping/results/JOB_ID"
```

### Example 6: Download All Results
```bash
# Download all human reviewed proteins
curl "https://rest.uniprot.org/uniprotkb/stream?query=organism_id:9606+AND+reviewed:true&format=fasta" \
  -o human_proteins.fasta
```

## R Examples

### Example 1: Basic Search
```r
library(httr)
library(jsonlite)

# Search for insulin proteins
url <- "https://rest.uniprot.org/uniprotkb/search"
query_params <- list(
  query = "insulin AND organism_id:9606",
  format = "json",
  size = 10
)

response <- GET(url, query = query_params)
data <- fromJSON(content(response, "text"))

# Extract accessions and names
proteins <- data$results[, c("primaryAccession", "proteinDescription")]
print(proteins)
```

### Example 2: Get Sequences
```r
library(httr)

# Get protein sequence
accession <- "P01308"
url <- paste0("https://rest.uniprot.org/uniprotkb/", accession, ".fasta")

response <- GET(url)
sequence <- content(response, "text")
cat(sequence)
```

### Example 3: Download to Data Frame
```r
library(httr)
library(readr)

# Get data as TSV
url <- "https://rest.uniprot.org/uniprotkb/search"
query_params <- list(
  query = "gene:BRCA1 AND reviewed:true",
  format = "tsv",
  fields = "accession,gene_names,organism_name,length"
)

response <- GET(url, query = query_params)
data <- read_tsv(content(response, "text"))
print(data)
```

## JavaScript Examples

### Example 1: Fetch API
```javascript
// Search for proteins
async function searchUniProt(query) {
  const url = `https://rest.uniprot.org/uniprotkb/search?query=${encodeURIComponent(query)}&format=json&size=10`;

  const response = await fetch(url);
  const data = await response.json();

  return data.results;
}

// Usage
searchUniProt("insulin AND organism_id:9606")
  .then(results => console.log(results));
```

### Example 2: Get Protein Entry
```javascript
async function getProtein(accession, format = "json") {
  const url = `https://rest.uniprot.org/uniprotkb/${accession}.${format}`;

  const response = await fetch(url);

  if (format === "json") {
    return await response.json();
  } else {
    return await response.text();
  }
}

// Usage
getProtein("P01308", "fasta")
  .then(sequence => console.log(sequence));
```

### Example 3: ID Mapping
```javascript
async function mapIds(ids, fromDb, toDb) {
  // Submit job
  const submitUrl = "https://rest.uniprot.org/idmapping/run";
  const formData = new URLSearchParams({
    from: fromDb,
    to: toDb,
    ids: ids.join(",")
  });

  const submitResponse = await fetch(submitUrl, {
    method: "POST",
    body: formData
  });
  const { jobId } = await submitResponse.json();

  // Poll for completion
  const statusUrl = `https://rest.uniprot.org/idmapping/status/${jobId}`;
  while (true) {
    const statusResponse = await fetch(statusUrl);
    const status = await statusResponse.json();

    if ("results" in status || "failedIds" in status) {
      break;
    }

    await new Promise(resolve => setTimeout(resolve, 3000));
  }

  // Get results
  const resultsUrl = `https://rest.uniprot.org/idmapping/results/${jobId}`;
  const resultsResponse = await fetch(resultsUrl);
  return await resultsResponse.json();
}

// Usage
mapIds(["P01308", "P04637"], "UniProtKB_AC-ID", "PDB")
  .then(mapping => console.log(mapping));
```

## Advanced Examples

### Example: Batch Processing with Rate Limiting
```python
import requests
import time
from typing import List, Dict

class UniProtClient:
    def __init__(self, rate_limit=1.0):
        self.base_url = "https://rest.uniprot.org"
        self.rate_limit = rate_limit
        self.last_request = 0

    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()

    def batch_get_proteins(self, accessions: List[str],
                          batch_size: int = 100) -> List[Dict]:
        """Get proteins in batches"""
        results = []

        for i in range(0, len(accessions), batch_size):
            batch = accessions[i:i + batch_size]
            query = " OR ".join([f"accession:{acc}" for acc in batch])

            self._rate_limit()

            response = requests.get(
                f"{self.base_url}/uniprotkb/search",
                params={
                    "query": query,
                    "format": "json",
                    "size": batch_size
                }
            )

            if response.ok:
                data = response.json()
                results.extend(data.get('results', []))
            else:
                print(f"Error in batch {i//batch_size}: {response.status_code}")

        return results

# Usage
client = UniProtClient(rate_limit=0.5)
accessions = ["P01308", "P04637", "P12345", "Q9Y6K9"]
proteins = client.batch_get_proteins(accessions)
```

### Example: Download with Progress Bar
```python
import requests
from tqdm import tqdm

def download_with_progress(query, output_file, format="fasta"):
    """Download results with progress bar"""
    url = "https://rest.uniprot.org/uniprotkb/stream"
    params = {
        "query": query,
        "format": format
    }

    response = requests.get(url, params=params, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(output_file, 'wb') as f, \
         tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))

# Usage
download_with_progress(
    "organism_id:9606 AND reviewed:true",
    "human_proteome.fasta"
)
```

## Resources

- API Documentation: https://www.uniprot.org/help/api
- Interactive API Explorer: https://www.uniprot.org/api-documentation
- Python client (Unipressed): https://github.com/multimeric/Unipressed
- Bioservices package: https://bioservices.readthedocs.io/

---

## Reference: Api_Fields

# UniProt API Fields Reference

Complete list of available fields for customizing UniProt API queries. Use these fields with the `fields` parameter to retrieve only the data you need.

## Usage

Add fields parameter to your query:
```
https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length
```

Multiple fields are comma-separated. No spaces after commas.

## Core Fields

### Identification
- `accession` - Primary accession number (e.g., P12345)
- `id` - Entry name (e.g., INSR_HUMAN)
- `uniprotkb_id` - Same as id
- `entryType` - REVIEWED (Swiss-Prot) or UNREVIEWED (TrEMBL)

### Protein Names
- `protein_name` - Recommended and alternative protein names
- `gene_names` - Gene name(s)
- `gene_primary` - Primary gene name
- `gene_synonym` - Gene synonyms
- `gene_oln` - Ordered locus names
- `gene_orf` - ORF names

### Organism Information
- `organism_name` - Organism scientific name
- `organism_id` - NCBI taxonomy identifier
- `lineage` - Taxonomic lineage
- `virus_hosts` - Virus host organisms (for viral proteins)

### Sequence Information
- `sequence` - Amino acid sequence
- `length` - Sequence length
- `mass` - Molecular mass (Daltons)
- `fragment` - Whether entry is a fragment
- `checksum` - Sequence CRC64 checksum

## Annotation Fields

### Function and Biology
- `cc_function` - Function description
- `cc_catalytic_activity` - Catalytic activity
- `cc_activity_regulation` - Activity regulation
- `cc_pathway` - Metabolic pathway information
- `cc_cofactor` - Cofactor information

### Interaction and Localization
- `cc_interaction` - Protein-protein interactions
- `cc_subunit` - Subunit structure
- `cc_subcellular_location` - Subcellular location
- `cc_tissue_specificity` - Tissue specificity
- `cc_developmental_stage` - Developmental stage expression

### Disease and Phenotype
- `cc_disease` - Disease associations
- `cc_disruption_phenotype` - Disruption phenotype
- `cc_allergen` - Allergen information
- `cc_toxic_dose` - Toxic dose information

### Post-translational Modifications
- `cc_ptm` - Post-translational modifications
- `cc_mass_spectrometry` - Mass spectrometry data

### Other Comments
- `cc_alternative_products` - Alternative products (isoforms)
- `cc_polymorphism` - Polymorphism information
- `cc_rna_editing` - RNA editing
- `cc_caution` - Caution notes
- `cc_miscellaneous` - Miscellaneous information
- `cc_similarity` - Sequence similarities
- `cc_sequence_caution` - Sequence caution
- `cc_web_resource` - Web resources

## Feature Fields (ft_)

### Molecular Processing
- `ft_signal` - Signal peptide
- `ft_transit` - Transit peptide
- `ft_init_met` - Initiator methionine
- `ft_propep` - Propeptide
- `ft_chain` - Chain (mature protein)
- `ft_peptide` - Peptide

### Regions and Sites
- `ft_domain` - Domain
- `ft_repeat` - Repeat
- `ft_ca_bind` - Calcium binding
- `ft_zn_fing` - Zinc finger
- `ft_dna_bind` - DNA binding
- `ft_np_bind` - Nucleotide binding
- `ft_region` - Region of interest
- `ft_coiled` - Coiled coil
- `ft_motif` - Short sequence motif
- `ft_compbias` - Compositional bias

### Sites and Modifications
- `ft_act_site` - Active site
- `ft_metal` - Metal binding
- `ft_binding` - Binding site
- `ft_site` - Site
- `ft_mod_res` - Modified residue
- `ft_lipid` - Lipidation
- `ft_carbohyd` - Glycosylation
- `ft_disulfid` - Disulfide bond
- `ft_crosslnk` - Cross-link

### Structural Features
- `ft_helix` - Helix
- `ft_strand` - Beta strand
- `ft_turn` - Turn
- `ft_transmem` - Transmembrane region
- `ft_intramem` - Intramembrane region
- `ft_topo_dom` - Topological domain

### Variation and Conflict
- `ft_variant` - Natural variant
- `ft_var_seq` - Alternative sequence
- `ft_mutagen` - Mutagenesis
- `ft_unsure` - Unsure residue
- `ft_conflict` - Sequence conflict
- `ft_non_cons` - Non-consecutive residues
- `ft_non_ter` - Non-terminal residue
- `ft_non_std` - Non-standard residue

## Gene Ontology (GO)

- `go` - All GO terms
- `go_p` - Biological process
- `go_c` - Cellular component
- `go_f` - Molecular function
- `go_id` - GO term identifiers

## Cross-References (xref_)

### Sequence Databases
- `xref_embl` - EMBL/GenBank/DDBJ
- `xref_refseq` - RefSeq
- `xref_ccds` - CCDS
- `xref_pir` - PIR

### 3D Structure Databases
- `xref_pdb` - Protein Data Bank
- `xref_pcddb` - PCD database
- `xref_alphafolddb` - AlphaFold database
- `xref_smr` - SWISS-MODEL Repository

### Protein Family/Domain Databases
- `xref_interpro` - InterPro
- `xref_pfam` - Pfam
- `xref_prosite` - PROSITE
- `xref_smart` - SMART

### Genome Databases
- `xref_ensembl` - Ensembl
- `xref_ensemblgenomes` - Ensembl Genomes
- `xref_geneid` - Entrez Gene
- `xref_kegg` - KEGG

### Organism-Specific Databases
- `xref_mgi` - MGI (mouse)
- `xref_rgd` - RGD (rat)
- `xref_flybase` - FlyBase (fly)
- `xref_wormbase` - WormBase (worm)
- `xref_xenbase` - Xenbase (frog)
- `xref_zfin` - ZFIN (zebrafish)

### Pathway Databases
- `xref_reactome` - Reactome
- `xref_signor` - SIGNOR
- `xref_signalink` - SignaLink

### Disease Databases
- `xref_disgenet` - DisGeNET
- `xref_malacards` - MalaCards
- `xref_omim` - OMIM
- `xref_orphanet` - Orphanet

### Drug Databases
- `xref_chembl` - ChEMBL
- `xref_drugbank` - DrugBank
- `xref_guidetopharmacology` - Guide to Pharmacology

### Expression Databases
- `xref_bgee` - Bgee
- `xref_expressionetatlas` - Expression Atlas
- `xref_genevisible` - Genevisible

## Metadata Fields

### Dates
- `date_created` - Entry creation date
- `date_modified` - Last modification date
- `date_sequence_modified` - Last sequence modification date

### Evidence and Quality
- `annotation_score` - Annotation score (1-5)
- `protein_existence` - Protein existence level
- `reviewed` - Whether entry is reviewed (Swiss-Prot)

### Literature
- `lit_pubmed_id` - PubMed identifiers
- `lit_doi` - DOI identifiers

### Proteomics
- `proteome` - Proteome identifier
- `tools` - Tools used for annotation

## Retrieving Available Fields Programmatically

Use the configuration endpoint to get all available fields:
```bash
curl https://rest.uniprot.org/configure/uniprotkb/result-fields
```

Or in Python:
```python
import requests
response = requests.get("https://rest.uniprot.org/configure/uniprotkb/result-fields")
fields = response.json()
```

## Common Field Combinations

### Basic protein information
```
fields=accession,id,protein_name,gene_names,organism_name,length
```

### Sequence and structure
```
fields=accession,sequence,length,mass,xref_pdb,xref_alphafolddb
```

### Functional annotation
```
fields=accession,protein_name,cc_function,cc_catalytic_activity,cc_pathway,go
```

### Disease information
```
fields=accession,protein_name,gene_names,cc_disease,xref_omim,xref_malacards
```

### Expression patterns
```
fields=accession,gene_names,cc_tissue_specificity,cc_developmental_stage,xref_bgee
```

### Complete annotation
```
fields=accession,id,protein_name,gene_names,organism_name,sequence,length,cc_*,ft_*,go,xref_pdb
```

## Notes

1. **Wildcards**: Some fields support wildcards (e.g., `cc_*` for all comment fields, `ft_*` for all features)

2. **Performance**: Requesting fewer fields improves response time and reduces bandwidth

3. **Format dependency**: Some fields may be formatted differently depending on output format (JSON vs TSV)

4. **Null values**: Fields without data may be omitted from response (JSON) or empty (TSV)

5. **Arrays vs strings**: In JSON format, many fields return arrays of objects rather than simple strings

## Resources

- Interactive field explorer: https://www.uniprot.org/api-documentation
- API fields endpoint: https://rest.uniprot.org/configure/uniprotkb/result-fields
- Return fields documentation: https://www.uniprot.org/help/return_fields

---

## Reference: Id_Mapping_Databases

# UniProt ID Mapping Databases

Complete list of databases supported by the UniProt ID Mapping service. Use these database names when calling the ID mapping API.

## Retrieving Database List Programmatically

```python
import requests
response = requests.get("https://rest.uniprot.org/configure/idmapping/fields")
databases = response.json()
```

## UniProt Databases

### UniProtKB
- `UniProtKB_AC-ID` - UniProt accession and ID
- `UniProtKB` - UniProt Knowledgebase
- `UniProtKB-Swiss-Prot` - Reviewed (Swiss-Prot)
- `UniProtKB-TrEMBL` - Unreviewed (TrEMBL)
- `UniParc` - UniProt Archive
- `UniRef50` - UniRef 50% identity clusters
- `UniRef90` - UniRef 90% identity clusters
- `UniRef100` - UniRef 100% identity clusters

## Sequence Databases

### Nucleotide Sequence
- `EMBL` - EMBL/GenBank/DDBJ
- `EMBL-CDS` - EMBL coding sequences
- `RefSeq_Nucleotide` - RefSeq nucleotide sequences
- `CCDS` - Consensus CDS

### Protein Sequence
- `RefSeq_Protein` - RefSeq protein sequences
- `PIR` - Protein Information Resource

## Gene Databases

- `GeneID` - Entrez Gene
- `Gene_Name` - Gene name
- `Gene_Synonym` - Gene synonym
- `Gene_OrderedLocusName` - Ordered locus name
- `Gene_ORFName` - ORF name

## Genome Databases

### General
- `Ensembl` - Ensembl
- `EnsemblGenomes` - Ensembl Genomes
- `EnsemblGenomes_PRO` - Ensembl Genomes protein
- `EnsemblGenomes_TRS` - Ensembl Genomes transcript
- `Ensembl_PRO` - Ensembl protein
- `Ensembl_TRS` - Ensembl transcript

### Organism-Specific
- `KEGG` - KEGG Genes
- `PATRIC` - PATRIC
- `UCSC` - UCSC Genome Browser
- `VectorBase` - VectorBase
- `WBParaSite` - WormBase ParaSite

## Structure Databases

- `PDB` - Protein Data Bank
- `AlphaFoldDB` - AlphaFold Database
- `BMRB` - Biological Magnetic Resonance Data Bank
- `PDBsum` - PDB summary
- `SASBDB` - Small Angle Scattering Biological Data Bank
- `SMR` - SWISS-MODEL Repository

## Protein Family and Domain Databases

- `InterPro` - InterPro
- `Pfam` - Pfam protein families
- `PROSITE` - PROSITE
- `SMART` - SMART domains
- `CDD` - Conserved Domain Database
- `HAMAP` - HAMAP
- `PANTHER` - PANTHER
- `PRINTS` - PRINTS
- `ProDom` - ProDom
- `SFLD` - Structure-Function Linkage Database
- `SUPFAM` - SUPERFAMILY
- `TIGRFAMs` - TIGRFAMs

## Organism-Specific Databases

### Model Organisms
- `MGI` - Mouse Genome Informatics
- `RGD` - Rat Genome Database
- `FlyBase` - FlyBase (Drosophila)
- `WormBase` - WormBase (C. elegans)
- `Xenbase` - Xenbase (Xenopus)
- `ZFIN` - Zebrafish Information Network
- `dictyBase` - dictyBase (Dictyostelium)
- `EcoGene` - EcoGene (E. coli)
- `SGD` - Saccharomyces Genome Database (yeast)
- `PomBase` - PomBase (S. pombe)
- `TAIR` - The Arabidopsis Information Resource

### Human-Specific
- `HGNC` - HUGO Gene Nomenclature Committee
- `CCDS` - Consensus Coding Sequence Database

## Pathway Databases

- `Reactome` - Reactome
- `BioCyc` - BioCyc
- `PlantReactome` - Plant Reactome
- `SIGNOR` - SIGNOR
- `SignaLink` - SignaLink

## Enzyme and Metabolism

- `EC` - Enzyme Commission number
- `BRENDA` - BRENDA enzyme database
- `SABIO-RK` - SABIO-RK (biochemical reactions)
- `MetaCyc` - MetaCyc

## Disease and Phenotype Databases

- `OMIM` - Online Mendelian Inheritance in Man
- `MIM` - MIM (same as OMIM)
- `OrphaNet` - Orphanet (rare diseases)
- `DisGeNET` - DisGeNET
- `MalaCards` - MalaCards
- `CTD` - Comparative Toxicogenomics Database
- `OpenTargets` - Open Targets

## Drug and Chemical Databases

- `ChEMBL` - ChEMBL
- `DrugBank` - DrugBank
- `DrugCentral` - DrugCentral
- `GuidetoPHARMACOLOGY` - Guide to Pharmacology
- `SwissLipids` - SwissLipids

## Gene Expression Databases

- `Bgee` - Bgee gene expression
- `ExpressionAtlas` - Expression Atlas
- `Genevisible` - Genevisible
- `CleanEx` - CleanEx

## Proteomics Databases

- `PRIDE` - PRIDE proteomics
- `PeptideAtlas` - PeptideAtlas
- `ProteomicsDB` - ProteomicsDB
- `CPTAC` - CPTAC
- `jPOST` - jPOST
- `MassIVE` - MassIVE
- `MaxQB` - MaxQB
- `PaxDb` - PaxDb
- `TopDownProteomics` - Top Down Proteomics

## Protein-Protein Interaction

- `STRING` - STRING
- `BioGRID` - BioGRID
- `IntAct` - IntAct
- `MINT` - MINT
- `DIP` - Database of Interacting Proteins
- `ComplexPortal` - Complex Portal

## Ontologies

- `GO` - Gene Ontology
- `GeneTree` - Ensembl GeneTree
- `HOGENOM` - HOGENOM
- `HOVERGEN` - HOVERGEN
- `KO` - KEGG Orthology
- `OMA` - OMA orthology
- `OrthoDB` - OrthoDB
- `TreeFam` - TreeFam

## Other Specialized Databases

### Glycosylation
- `GlyConnect` - GlyConnect
- `GlyGen` - GlyGen

### Protein Modifications
- `PhosphoSitePlus` - PhosphoSitePlus
- `iPTMnet` - iPTMnet

### Antibodies
- `Antibodypedia` - Antibodypedia
- `DNASU` - DNASU

### Protein Localization
- `COMPARTMENTS` - COMPARTMENTS
- `NeXtProt` - NeXtProt (human proteins)

### Evolution and Phylogeny
- `eggNOG` - eggNOG
- `GeneTree` - Ensembl GeneTree
- `InParanoid` - InParanoid

### Technical Resources
- `PRO` - Protein Ontology
- `GenomeRNAi` - GenomeRNAi
- `PubMed` - PubMed literature references

## Common Mapping Scenarios

### Example 1: UniProt to PDB
```python
from_db = "UniProtKB_AC-ID"
to_db = "PDB"
ids = ["P01308", "P04637"]
```

### Example 2: Gene Name to UniProt
```python
from_db = "Gene_Name"
to_db = "UniProtKB"
ids = ["BRCA1", "TP53", "INSR"]
```

### Example 3: UniProt to Ensembl
```python
from_db = "UniProtKB_AC-ID"
to_db = "Ensembl"
ids = ["P12345"]
```

### Example 4: RefSeq to UniProt
```python
from_db = "RefSeq_Protein"
to_db = "UniProtKB"
ids = ["NP_000207.1"]
```

### Example 5: UniProt to GO Terms
```python
from_db = "UniProtKB_AC-ID"
to_db = "GO"
ids = ["P01308"]
```

## Usage Notes

1. **Database names are case-sensitive**: Use exact names as listed

2. **Many-to-many mappings**: One ID may map to multiple target IDs

3. **Failed mappings**: Some IDs may not have mappings; check the `failedIds` field in results

4. **Batch size limit**: Maximum 100,000 IDs per job

5. **Result expiration**: Results are stored for 7 days

6. **Bidirectional mapping**: Most databases support mapping in both directions

## API Endpoints

### Get available databases
```
GET https://rest.uniprot.org/configure/idmapping/fields
```

### Submit mapping job
```
POST https://rest.uniprot.org/idmapping/run
Content-Type: application/x-www-form-urlencoded

from={from_db}&to={to_db}&ids={comma_separated_ids}
```

### Check job status
```
GET https://rest.uniprot.org/idmapping/status/{jobId}
```

### Get results
```
GET https://rest.uniprot.org/idmapping/results/{jobId}
```

## Resources

- ID Mapping tool: https://www.uniprot.org/id-mapping
- API documentation: https://www.uniprot.org/help/id_mapping
- Programmatic access: https://www.uniprot.org/help/api_idmapping

---

## Reference: Query_Syntax

# UniProt Query Syntax Reference

Comprehensive guide to UniProt search query syntax for constructing complex searches.

## Basic Syntax

### Simple Queries
```
insulin
kinase
```

### Field-Specific Searches
```
gene:BRCA1
accession:P12345
organism_name:human
protein_name:kinase
```

## Boolean Operators

### AND (both terms must be present)
```
insulin AND diabetes
kinase AND human
gene:BRCA1 AND reviewed:true
```

### OR (either term can be present)
```
diabetes OR insulin
(cancer OR tumor) AND human
```

### NOT (exclude terms)
```
kinase NOT human
protein_name:kinase NOT organism_name:mouse
```

### Grouping with Parentheses
```
(diabetes OR insulin) AND reviewed:true
(gene:BRCA1 OR gene:BRCA2) AND organism_id:9606
```

## Common Search Fields

### Identification
- `accession:P12345` - UniProt accession number
- `id:INSR_HUMAN` - Entry name
- `gene:BRCA1` - Gene name
- `gene_exact:BRCA1` - Exact gene name match

### Organism/Taxonomy
- `organism_name:human` - Organism name
- `organism_name:"Homo sapiens"` - Exact organism name (use quotes for multi-word)
- `organism_id:9606` - NCBI taxonomy ID
- `taxonomy_id:9606` - Same as organism_id
- `taxonomy_name:"Homo sapiens"` - Taxonomy name

### Protein Information
- `protein_name:insulin` - Protein name
- `protein_name:"insulin receptor"` - Exact protein name
- `reviewed:true` - Only Swiss-Prot (reviewed) entries
- `reviewed:false` - Only TrEMBL (unreviewed) entries

### Sequence Properties
- `length:[100 TO 500]` - Sequence length range
- `mass:[50000 TO 100000]` - Molecular mass in Daltons
- `sequence:MVLSPADKTNVK` - Exact sequence match
- `fragment:false` - Exclude fragment sequences

### Gene Ontology (GO)
- `go:0005515` - GO term ID (0005515 = protein binding)
- `go_f:* ` - Any molecular function
- `go_p:*` - Any biological process
- `go_c:*` - Any cellular component

### Annotations
- `annotation:(type:signal)` - Has signal peptide annotation
- `annotation:(type:transmem)` - Has transmembrane region
- `cc_function:*` - Has function comment
- `cc_interaction:*` - Has interaction comment
- `ft_domain:*` - Has domain feature

### Database Cross-References
- `xref:pdb` - Has PDB structure
- `xref:ensembl` - Has Ensembl reference
- `database:pdb` - Same as xref
- `database:(type:pdb)` - Alternative syntax

### Protein Families and Domains
- `family:"protein kinase"` - Protein family
- `keyword:"Protein kinase"` - Keyword annotation
- `cc_similarity:*` - Has similarity comment

## Range Queries

### Numeric Ranges
```
length:[100 TO 500]          # Between 100 and 500
mass:[* TO 50000]            # Less than or equal to 50000
created:[2023-01-01 TO *]   # Created after Jan 1, 2023
```

### Date Ranges
```
created:[2023-01-01 TO 2023-12-31]
modified:[2024-01-01 TO *]
```

## Wildcards

### Single Character (?)
```
gene:BRCA?      # Matches BRCA1, BRCA2, etc.
```

### Multiple Characters (*)
```
gene:BRCA*      # Matches BRCA1, BRCA2, BRCA1P1, etc.
protein_name:kinase*
organism_name:Homo*
```

## Advanced Searches

### Existence Queries
```
cc_function:*              # Has any function annotation
ft_domain:*                # Has any domain feature
xref:pdb                   # Has PDB structure
```

### Combined Complex Queries
```
# Human reviewed kinases with PDB structure
(protein_name:kinase OR family:kinase) AND organism_id:9606 AND reviewed:true AND xref:pdb

# Cancer-related proteins excluding mice
(disease:cancer OR keyword:cancer) NOT organism_name:mouse

# Membrane proteins with signal peptides
annotation:(type:transmem) AND annotation:(type:signal) AND reviewed:true

# Recently updated human proteins
organism_id:9606 AND modified:[2024-01-01 TO *] AND reviewed:true
```

## Field-Specific Examples

### Protein Names
```
protein_name:"insulin receptor"    # Exact phrase
protein_name:insulin*              # Starts with insulin
recommended_name:insulin           # Recommended name only
alternative_name:insulin           # Alternative names only
```

### Genes
```
gene:BRCA1                        # Gene symbol
gene_exact:BRCA1                  # Exact gene match
olnName:BRCA1                     # Ordered locus name
orfName:BRCA1                     # ORF name
```

### Organisms
```
organism_name:human               # Common name
organism_name:"Homo sapiens"      # Scientific name
organism_id:9606                  # Taxonomy ID
lineage:primates                  # Taxonomic lineage
```

### Features
```
ft_signal:*                       # Signal peptide
ft_transmem:*                     # Transmembrane region
ft_domain:"Protein kinase"        # Specific domain
ft_binding:*                      # Binding site
ft_site:*                         # Any site
```

### Comments (cc_)
```
cc_function:*                     # Function description
cc_catalytic_activity:*           # Catalytic activity
cc_pathway:*                      # Pathway involvement
cc_interaction:*                  # Protein interactions
cc_subcellular_location:*         # Subcellular location
cc_tissue_specificity:*           # Tissue specificity
cc_disease:cancer                 # Disease association
```

## Tips and Best Practices

1. **Use quotes for exact phrases**: `organism_name:"Homo sapiens"` not `organism_name:Homo sapiens`

2. **Filter by review status**: Add `AND reviewed:true` for high-quality Swiss-Prot entries

3. **Combine wildcards carefully**: `*kinase*` may be too broad; `kinase*` is more specific

4. **Use parentheses for complex logic**: `(A OR B) AND (C OR D)` is clearer than `A OR B AND C OR D`

5. **Numeric ranges are inclusive**: `length:[100 TO 500]` includes both 100 and 500

6. **Field prefixes**: Learn common prefixes:
   - `cc_` = Comments
   - `ft_` = Features
   - `go_` = Gene Ontology
   - `xref_` = Cross-references

7. **Check field names**: Use the API's `/configure/uniprotkb/result-fields` endpoint to see all available fields

## Query Validation

Test queries using:
- **Web interface**: https://www.uniprot.org/uniprotkb
- **API**: https://rest.uniprot.org/uniprotkb/search?query=YOUR_QUERY
- **API documentation**: https://www.uniprot.org/help/query-fields

## Common Patterns

### Find well-characterized proteins
```
reviewed:true AND xref:pdb AND cc_function:*
```

### Find disease-associated proteins
```
cc_disease:* AND organism_id:9606 AND reviewed:true
```

### Find proteins with experimental evidence
```
existence:"Evidence at protein level" AND reviewed:true
```

### Find secreted proteins
```
cc_subcellular_location:secreted AND reviewed:true
```

### Find drug targets
```
keyword:"Pharmaceutical" OR keyword:"Drug target"
```

## Resources

- Full query field reference: https://www.uniprot.org/help/query-fields
- API query documentation: https://www.uniprot.org/help/api_queries
- Text search documentation: https://www.uniprot.org/help/text-search
