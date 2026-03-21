---
title: "Monarch Database"
description: "Query the Monarch Initiative knowledge graph for disease-gene-phenotype associations across species. Integrates OMIM, ORPHANET, HPO, ClinVar, and model organism databases. Use for rare disease gene discovery, phenotype-to-gene mapping, cross-speci..."
category: "research"
source: "community"
author: "Community"
tags: ["monarch", "database"]
date: 2026-03-20
---

# Monarch Initiative Database

## Overview

The Monarch Initiative (https://monarchinitiative.org/) is a multi-species integrated knowledgebase that links genes, diseases, and phenotypes across humans and model organisms. It integrates data from over 40 sources including OMIM, ORPHANET, HPO (Human Phenotype Ontology), ClinVar, MGI (Mouse Genome Informatics), ZFIN (Zebrafish), RGD (Rat), FlyBase, and WormBase.

Monarch enables:
- Mapping phenotypes across species to identify candidate disease genes
- Finding all genes associated with a disease or phenotype
- Discovering model organisms for human diseases
- Navigating the HPO hierarchy for phenotype ontology queries

**Key resources:**
- Monarch portal: https://monarchinitiative.org/
- Monarch API v3: https://api-v3.monarchinitiative.org/v3/
- API docs: https://api-v3.monarchinitiative.org/v3/docs
- HPO browser: https://hpo.jax.org/

## When to Use This Skill

Use Monarch when:

- **Rare disease gene discovery**: What genes are associated with my patient's phenotypes (HPO terms)?
- **Phenotype similarity**: Are two diseases similar based on their phenotypic profiles?
- **Cross-species modeling**: Are there mouse/zebrafish models for my disease of interest?
- **HPO term lookup**: Retrieve HPO term names, definitions, and ontology hierarchy
- **Disease-phenotype mapping**: List all HPO terms associated with a specific disease
- **Gene-phenotype associations**: What phenotypes are caused by variants in a gene?
- **Ortholog-phenotype mapping**: Use animal model phenotypes to infer human gene function

## Core Capabilities

### 1. Monarch API v3

Base URL: `https://api-v3.monarchinitiative.org/v3/`

```python
import requests

BASE_URL = "https://api-v3.monarchinitiative.org/v3"

def monarch_get(endpoint, params=None):
    """Make a GET request to the Monarch API."""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()
```

### 2. Phenotype-to-Gene Association (Pheno2Gene)

```python
def get_genes_for_phenotypes(hpo_ids, limit=50, offset=0):
    """
    Find genes associated with a list of HPO phenotype terms.
    Core use case: rare disease differential diagnosis.

    Args:
        hpo_ids: List of HPO term IDs (e.g., ["HP:0001250", "HP:0004322"])
        limit: Maximum number of results
    """
    params = {
        "terms": hpo_ids,
        "limit": limit,
        "offset": offset
    }
    return monarch_get("semsim/termset-pairwise-similarity/analyze", params)

def phenotype_to_gene(hpo_ids):
    """
    Return genes whose phenotypes match the given HPO terms.
    Uses semantic similarity scoring.
    """
    # Use the /association endpoint for direct phenotype-gene links
    all_genes = []
    for hpo_id in hpo_ids:
        data = monarch_get("association/all", {
            "subject": hpo_id,
            "predicate": "biolink:has_phenotype",
            "category": "biolink:GeneToPhenotypicFeatureAssociation",
            "limit": 50
        })
        for assoc in data.get("items", []):
            all_genes.append({
                "phenotype_id": hpo_id,
                "gene_id": assoc.get("object", {}).get("id"),
                "gene_name": assoc.get("object", {}).get("name"),
                "evidence": assoc.get("evidence_type")
            })
    return all_genes

# Example: Find genes associated with seizures and short stature
hpo_terms = ["HP:0001250", "HP:0004322"]  # Seizures, Short stature
genes = phenotype_to_gene(hpo_terms)
```

### 3. Disease-to-Gene Associations

```python
def get_genes_for_disease(disease_id, limit=100):
    """
    Get all genes associated with a disease.
    Disease IDs: OMIM:146300, MONDO:0007739, ORPHANET:558, etc.
    """
    params = {
        "object": disease_id,
        "category": "biolink:DiseaseToDiseaseAssociation",
        "limit": limit
    }
    # Use the gene-disease association endpoint
    gene_params = {
        "subject": disease_id,
        "category": "biolink:GeneToPhenotypicFeatureAssociation",
        "limit": limit
    }

    data = monarch_get("association/all", {
        "object": disease_id,
        "predicate": "biolink:has_phenotype",
        "limit": limit
    })
    return data

def get_disease_genes(disease_id, limit=100):
    """Get genes causally linked to a disease."""
    data = monarch_get("association/all", {
        "subject_category": "biolink:Gene",
        "object": disease_id,
        "predicate": "biolink:causes",
        "limit": limit
    })
    return data.get("items", [])

# MONDO disease IDs (preferred over OMIM for cross-ontology queries)
# MONDO:0007739 - Huntington disease
# MONDO:0009061 - Cystic fibrosis
# OMIM:104300 - Alzheimer disease, susceptibility to, type 1
```

### 4. Gene-to-Phenotype and Disease

```python
def get_phenotypes_for_gene(gene_id, limit=100):
    """
    Get all phenotypes associated with a gene.
    Gene IDs: HGNC:7884, NCBIGene:4137, etc.
    """
    data = monarch_get("association/all", {
        "subject": gene_id,
        "predicate": "biolink:has_phenotype",
        "limit": limit
    })
    return data.get("items", [])

def get_diseases_for_gene(gene_id, limit=100):
    """Get diseases caused by variants in a gene."""
    data = monarch_get("association/all", {
        "subject": gene_id,
        "object_category": "biolink:Disease",
        "limit": limit
    })
    return data.get("items", [])

# Example: What diseases does BRCA1 cause?
brca1_diseases = get_diseases_for_gene("HGNC:1100")
for assoc in brca1_diseases:
    print(f"  {assoc.get('object', {}).get('name')} ({assoc.get('object', {}).get('id')})")
```

### 5. HPO Term Lookup

```python
def get_hpo_term(hpo_id):
    """Fetch information about an HPO term."""
    return monarch_get(f"entity/{hpo_id}")

def search_hpo_terms(query, limit=20):
    """Search for HPO terms by name."""
    params = {
        "q": query,
        "category": "biolink:PhenotypicFeature",
        "limit": limit
    }
    return monarch_get("search", params)

# Example: look up the HPO term for seizures
seizure_term = get_hpo_term("HP:0001250")
print(f"Name: {seizure_term.get('name')}")
print(f"Definition: {seizure_term.get('description')}")

# Search for related terms
epilepsy_terms = search_hpo_terms("epilepsy")
for term in epilepsy_terms.get("items", [])[:5]:
    print(f"  {term['id']}: {term['name']}")
```

### 6. Semantic Similarity (Disease Comparison)

```python
def compare_disease_phenotypes(disease_id_1, disease_id_2):
    """
    Compare two diseases by semantic similarity of their phenotype profiles.
    Returns similarity score using HPO hierarchy.
    """
    params = {
        "subjects": [disease_id_1],
        "objects": [disease_id_2],
        "metric": "ancestor_information_content"
    }
    return monarch_get("semsim/compare", params)

# Example: Compare Dravet syndrome with CDKL5-deficiency disorder
similarity = compare_disease_phenotypes("MONDO:0100135", "MONDO:0014917")
```

### 7. Cross-Species Orthologs

```python
def get_orthologs(gene_id, species=None):
    """
    Get orthologs of a human gene in model organisms.
    Useful for finding animal models of human diseases.
    """
    params = {"limit": 50}
    if species:
        params["subject_taxon"] = species

    data = monarch_get("association/all", {
        "subject": gene_id,
        "predicate": "biolink:orthologous_to",
        "limit": 50
    })
    return data.get("items", [])

# NCBI Taxonomy IDs for common model organisms:
# Mouse: 10090 (Mus musculus)
# Zebrafish: 7955 (Danio rerio)
# Fruit fly: 7227 (Drosophila melanogaster)
# C. elegans: 6239
# Rat: 10116 (Rattus norvegicus)
```

### 8. Full Workflow: Rare Disease Gene Prioritization

```python
import requests
import pandas as pd

def rare_disease_gene_finder(patient_hpo_terms, candidate_gene_ids=None, top_n=20):
    """
    Find genes that match a patient's HPO phenotype profile.

    Args:
        patient_hpo_terms: List of HPO IDs from clinical assessment
        candidate_gene_ids: Optional list to restrict search
        top_n: Number of top candidates to return
    """
    BASE_URL = "https://api-v3.monarchinitiative.org/v3"

    # 1. Find genes associated with each phenotype
    gene_phenotype_counts = {}

    for hpo_id in patient_hpo_terms:
        data = requests.get(
            f"{BASE_URL}/association/all",
            params={
                "object": hpo_id,
                "subject_category": "biolink:Gene",
                "limit": 100
            }
        ).json()

        for item in data.get("items", []):
            gene_id = item.get("subject", {}).get("id")
            gene_name = item.get("subject", {}).get("name")
            if gene_id:
                if gene_id not in gene_phenotype_counts:
                    gene_phenotype_counts[gene_id] = {"name": gene_name, "count": 0, "phenotypes": []}
                gene_phenotype_counts[gene_id]["count"] += 1
                gene_phenotype_counts[gene_id]["phenotypes"].append(hpo_id)

    # 2. Rank by number of matching phenotypes
    ranked = sorted(gene_phenotype_counts.items(),
                    key=lambda x: -x[1]["count"])[:top_n]

    results = []
    for gene_id, info in ranked:
        results.append({
            "gene_id": gene_id,
            "gene_name": info["name"],
            "matching_phenotypes": info["count"],
            "total_patient_phenotypes": len(patient_hpo_terms),
            "phenotype_overlap": info["count"] / len(patient_hpo_terms),
            "matching_hpo_terms": info["phenotypes"]
        })

    return pd.DataFrame(results)

# Example usage
patient_phenotypes = [
    "HP:0001250",  # Seizures
    "HP:0004322",  # Short stature
    "HP:0001252",  # Hypotonia
    "HP:0000252",  # Microcephaly
    "HP:0001263",  # Global developmental delay
]
candidates = rare_disease_gene_finder(patient_phenotypes)
print(candidates[["gene_name", "matching_phenotypes", "phenotype_overlap"]].to_string())
```

## Query Workflows

### Workflow 1: HPO-Based Differential Diagnosis

1. Extract HPO terms from clinical notes or genetics consultation
2. Run phenotype-to-gene query against Monarch
3. Rank candidate genes by number of matching phenotypes
4. Cross-reference with gnomAD (constraint scores) and ClinVar (variant evidence)
5. Prioritize genes with high pLI and known pathogenic variants

### Workflow 2: Disease Model Discovery

1. Identify gene or disease of interest
2. Query Monarch for cross-species orthologs
3. Find phenotype associations in model organism databases
4. Identify experimental models that recapitulate human disease features

### Workflow 3: Phenotype Annotation of Novel Genes

1. For a gene with unknown function, query all known phenotype associations
2. Map to HPO hierarchy to understand affected body systems
3. Cross-reference with OMIM and ORPHANET for disease links

## Common Identifier Prefixes

| Prefix | Namespace | Example |
|--------|-----------|---------|
| `HP:` | Human Phenotype Ontology | HP:0001250 (Seizures) |
| `MONDO:` | Monarch Disease Ontology | MONDO:0007739 |
| `OMIM:` | OMIM disease | OMIM:104300 |
| `ORPHANET:` | Orphanet rare disease | ORPHANET:558 |
| `HGNC:` | HGNC gene symbol | HGNC:7884 |
| `NCBIGene:` | NCBI gene ID | NCBIGene:4137 |
| `ENSEMBL:` | Ensembl gene | ENSEMBL:ENSG... |
| `MGI:` | Mouse gene | MGI:1338833 |
| `ZFIN:` | Zebrafish gene | ZFIN:ZDB-GENE... |

## Best Practices

- **Use MONDO IDs** for diseases — they unify OMIM/ORPHANET/MESH identifiers
- **Use HPO IDs** for phenotypes — the standard for clinical phenotype description
- **Handle pagination**: Large queries may require iterating with offset parameter
- **Semantic similarity is better than exact match**: Ancestor HPO terms catch related phenotypes
- **Cross-validate with ClinVar and OMIM**: Monarch aggregates many sources; quality varies
- **Use HGNC IDs for genes**: More stable than gene symbols across database versions

## Additional Resources

- **Monarch portal**: https://monarchinitiative.org/
- **API v3 docs**: https://api-v3.monarchinitiative.org/v3/docs
- **HPO browser**: https://hpo.jax.org/
- **MONDO ontology**: https://mondo.monarchinitiative.org/
- **Citation**: Shefchek KA et al. (2020) Nucleic Acids Research. PMID: 31701156
- **Phenomizer** (HPO-based diagnosis): https://compbio.charite.de/phenomizer/

---

## Reference: Phenotype_Ontology

# HPO and Disease Ontology Reference for Monarch

## Human Phenotype Ontology (HPO)

### HPO Structure

HPO is organized hierarchically:
- **Root**: HP:0000001 (All)
  - HP:0000118 (Phenotypic abnormality)
    - HP:0000478 (Abnormality of the eye)
    - HP:0000707 (Abnormality of the nervous system)
    - HP:0001507 (Growth abnormality)
    - HP:0001626 (Abnormality of the cardiovascular system)
    - etc.

### Top-Level HPO Categories

| HPO ID | Name |
|--------|------|
| HP:0000924 | Abnormality of the skeletal system |
| HP:0000707 | Abnormality of the nervous system |
| HP:0000478 | Abnormality of the eye |
| HP:0000598 | Abnormality of the ear |
| HP:0001507 | Growth abnormality |
| HP:0001626 | Abnormality of the cardiovascular system |
| HP:0002086 | Abnormality of the respiratory system |
| HP:0001939 | Abnormality of metabolism/homeostasis |
| HP:0002664 | Neoplasm |
| HP:0000818 | Abnormality of the endocrine system |
| HP:0000119 | Abnormality of the genitourinary system |
| HP:0001197 | Abnormality of prenatal development/birth |

### Common HPO Terms in Rare Disease Genetics

#### Neurological
| HPO ID | Term |
|--------|------|
| HP:0001250 | Seizures |
| HP:0001251 | Ataxia |
| HP:0001252 | Muscular hypotonia |
| HP:0001263 | Global developmental delay |
| HP:0001270 | Motor delay |
| HP:0002167 | Neurological speech impairment |
| HP:0000716 | Depressivity |
| HP:0000729 | Autistic behavior |
| HP:0001332 | Dystonia |
| HP:0002071 | Abnormality of extrapyramidal motor function |

#### Growth/Morphology
| HPO ID | Term |
|--------|------|
| HP:0004322 | Short stature |
| HP:0001508 | Failure to thrive |
| HP:0000252 | Microcephaly |
| HP:0000256 | Macrocephaly |
| HP:0001511 | Intrauterine growth retardation |

#### Facial Features
| HPO ID | Term |
|--------|------|
| HP:0000324 | Facial asymmetry |
| HP:0001249 | Intellectual disability |
| HP:0000219 | Thin upper lip vermilion |
| HP:0000303 | Mandibular prognathia |
| HP:0000463 | Anteverted nares |

#### Metabolic
| HPO ID | Term |
|--------|------|
| HP:0001943 | Hypoglycemia |
| HP:0001944 | Hyperglycemia (Diabetes mellitus) |
| HP:0000822 | Hypertension |
| HP:0001712 | Left ventricular hypertrophy |

## MONDO Disease Ontology

MONDO integrates disease classifications from multiple sources:
- OMIM (Mendelian diseases)
- ORPHANET (rare diseases)
- MeSH (medical subject headings)
- SNOMED CT
- DOID (Disease Ontology)
- EFO (Experimental Factor Ontology)

### Key MONDO IDs for Common Rare Diseases

| MONDO ID | Disease | OMIM |
|----------|---------|------|
| MONDO:0007739 | Huntington disease | OMIM:143100 |
| MONDO:0009061 | Cystic fibrosis | OMIM:219700 |
| MONDO:0008608 | Down syndrome | OMIM:190685 |
| MONDO:0019391 | Fragile X syndrome | OMIM:300624 |
| MONDO:0010726 | Rett syndrome | OMIM:312750 |
| MONDO:0014517 | Dravet syndrome | OMIM:607208 |
| MONDO:0024522 | SCN1A-related epilepsy | — |
| MONDO:0014817 | CHARGE syndrome | OMIM:214800 |
| MONDO:0009764 | Marfan syndrome | OMIM:154700 |
| MONDO:0013282 | Alpha-1-antitrypsin deficiency | OMIM:613490 |

### OMIM ID Patterns

- **Phenotype only**: OMIM number alone (e.g., OMIM:104300)
- **Gene and phenotype**: Same gene, multiple phenotype entries
- **Phenotype series**: Grouped phenotypes at a locus

```python
import requests

def omim_to_mondo(omim_id):
    """Convert OMIM ID to MONDO ID via Monarch API."""
    search_id = f"OMIM:{omim_id}" if not omim_id.startswith("OMIM:") else omim_id
    data = requests.get(
        f"https://api-v3.monarchinitiative.org/v3/entity/{search_id}"
    ).json()
    # Check for same_as/equivalent_id links to MONDO
    return data
```

## Association Evidence Codes

Monarch associations include evidence types:

| Code | Evidence Type |
|------|--------------|
| `IEA` | Inferred from electronic annotation |
| `TAS` | Traceable author statement |
| `IMP` | Inferred from mutant phenotype |
| `IGI` | Inferred from genetic interaction |
| `IDA` | Inferred from direct assay |
| `ISS` | Inferred from sequence or structural similarity |
| `IBA` | Inferred from biological aspect of ancestor |

Higher-quality evidence: IDA > TAS > IMP > IEA

## Semantic Similarity Metrics

Monarch supports multiple similarity metrics:

| Metric | Description | Use case |
|--------|-------------|---------|
| `ancestor_information_content` | IC of most informative common ancestor (MICA) | Disease similarity |
| `jaccard_similarity` | Overlap coefficient | Simple set comparison |
| `cosine` | Cosine similarity of IC vectors | Large-scale comparisons |
| `phenodigm` | Combined MICA + Jaccard | Model organism matching |

```python
import requests

def compute_disease_similarity(disease_ids_1, disease_ids_2, metric="ancestor_information_content"):
    """Compute semantic similarity between two sets of disease phenotypes."""
    # Get phenotype sets for each disease
    url = "https://api-v3.monarchinitiative.org/v3/semsim/compare"
    params = {
        "subjects": disease_ids_1,
        "objects": disease_ids_2,
        "metric": metric
    }
    response = requests.get(url, params=params)
    return response.json()
```
