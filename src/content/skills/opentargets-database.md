---
title: "Opentargets Database"
description: "Query Open Targets Platform for target-disease associations, drug target discovery, tractability/safety data, genetics/omics evidence, known drugs, for therapeutic target identification."
category: "research"
source: "community"
author: "Community"
tags: ["opentargets", "database"]
date: 2026-03-20
---

# Open Targets Database

## Overview

The Open Targets Platform is a comprehensive resource for systematic identification and prioritization of potential therapeutic drug targets. It integrates publicly available datasets including human genetics, omics, literature, and chemical data to build and score target-disease associations.

**Key capabilities:**
- Query target (gene) annotations including tractability, safety, expression
- Search for disease-target associations with evidence scores
- Retrieve evidence from multiple data types (genetics, pathways, literature, etc.)
- Find known drugs for diseases and their mechanisms
- Access drug information including clinical trial phases and adverse events
- Evaluate target druggability and therapeutic potential

**Data access:** The platform provides a GraphQL API, web interface, data downloads, and Google BigQuery access. This skill focuses on the GraphQL API for programmatic access.

## When to Use This Skill

This skill should be used when:

- **Target discovery:** Finding potential therapeutic targets for a disease
- **Target assessment:** Evaluating tractability, safety, and druggability of genes
- **Evidence gathering:** Retrieving supporting evidence for target-disease associations
- **Drug repurposing:** Identifying existing drugs that could be repurposed for new indications
- **Competitive intelligence:** Understanding clinical precedence and drug development landscape
- **Target prioritization:** Ranking targets based on genetic evidence and other data types
- **Mechanism research:** Investigating biological pathways and gene functions
- **Biomarker discovery:** Finding genes differentially expressed in disease
- **Safety assessment:** Identifying potential toxicity concerns for drug targets

## Core Workflow

### 1. Search for Entities

Start by finding the identifiers for targets, diseases, or drugs of interest.

**For targets (genes):**
```python
from scripts.query_opentargets import search_entities

# Search by gene symbol or name
results = search_entities("BRCA1", entity_types=["target"])
# Returns: [{"id": "ENSG00000012048", "name": "BRCA1", ...}]
```

**For diseases:**
```python
# Search by disease name
results = search_entities("alzheimer", entity_types=["disease"])
# Returns: [{"id": "EFO_0000249", "name": "Alzheimer disease", ...}]
```

**For drugs:**
```python
# Search by drug name
results = search_entities("aspirin", entity_types=["drug"])
# Returns: [{"id": "CHEMBL25", "name": "ASPIRIN", ...}]
```

**Identifiers used:**
- Targets: Ensembl gene IDs (e.g., `ENSG00000157764`)
- Diseases: EFO (Experimental Factor Ontology) IDs (e.g., `EFO_0000249`)
- Drugs: ChEMBL IDs (e.g., `CHEMBL25`)

### 2. Query Target Information

Retrieve comprehensive target annotations to assess druggability and biology.

```python
from scripts.query_opentargets import get_target_info

target_info = get_target_info("ENSG00000157764", include_diseases=True)

# Access key fields:
# - approvedSymbol: HGNC gene symbol
# - approvedName: Full gene name
# - tractability: Druggability assessments across modalities
# - safetyLiabilities: Known safety concerns
# - geneticConstraint: Constraint scores from gnomAD
# - associatedDiseases: Top disease associations with scores
```

**Key annotations to review:**
- **Tractability:** Small molecule, antibody, PROTAC druggability predictions
- **Safety:** Known toxicity concerns from multiple databases
- **Genetic constraint:** pLI and LOEUF scores indicating essentiality
- **Disease associations:** Diseases linked to the target with evidence scores

Refer to `references/target_annotations.md` for detailed information about all target features.

### 3. Query Disease Information

Get disease details and associated targets/drugs.

```python
from scripts.query_opentargets import get_disease_info

disease_info = get_disease_info("EFO_0000249", include_targets=True)

# Access fields:
# - name: Disease name
# - description: Disease description
# - therapeuticAreas: High-level disease categories
# - associatedTargets: Top targets with association scores
```

### 4. Retrieve Target-Disease Evidence

Get detailed evidence supporting a target-disease association.

```python
from scripts.query_opentargets import get_target_disease_evidence

# Get all evidence
evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249"
)

# Filter by evidence type
genetic_evidence = get_target_disease_evidence(
    ensembl_id="ENSG00000157764",
    efo_id="EFO_0000249",
    data_types=["genetic_association"]
)

# Each evidence record contains:
# - datasourceId: Specific data source (e.g., "gwas_catalog", "chembl")
# - datatypeId: Evidence category (e.g., "genetic_association", "known_drug")
# - score: Evidence strength (0-1)
# - studyId: Original study identifier
# - literature: Associated publications
```

**Major evidence types:**
1. **genetic_association:** GWAS, rare variants, ClinVar, gene burden
2. **somatic_mutation:** Cancer Gene Census, IntOGen, cancer biomarkers
3. **known_drug:** Clinical precedence from approved/clinical drugs
4. **affected_pathway:** CRISPR screens, pathway analyses, gene signatures
5. **rna_expression:** Differential expression from Expression Atlas
6. **animal_model:** Mouse phenotypes from IMPC
7. **literature:** Text-mining from Europe PMC

Refer to `references/evidence_types.md` for detailed descriptions of all evidence types and interpretation guidelines.

### 5. Find Known Drugs

Identify drugs used for a disease and their targets.

```python
from scripts.query_opentargets import get_known_drugs_for_disease

drugs = get_known_drugs_for_disease("EFO_0000249")

# drugs contains:
# - uniqueDrugs: Total number of unique drugs
# - uniqueTargets: Total number of unique targets
# - rows: List of drug-target-indication records with:
#   - drug: {name, drugType, maximumClinicalTrialPhase}
#   - targets: Genes targeted by the drug
#   - phase: Clinical trial phase for this indication
#   - status: Trial status (active, completed, etc.)
#   - mechanismOfAction: How drug works
```

**Clinical phases:**
- Phase 4: Approved drug
- Phase 3: Late-stage clinical trials
- Phase 2: Mid-stage trials
- Phase 1: Early safety trials

### 6. Get Drug Information

Retrieve detailed drug information including mechanisms and indications.

```python
from scripts.query_opentargets import get_drug_info

drug_info = get_drug_info("CHEMBL25")

# Access:
# - name, synonyms: Drug identifiers
# - drugType: Small molecule, antibody, etc.
# - maximumClinicalTrialPhase: Development stage
# - mechanismsOfAction: Target and action type
# - indications: Diseases with trial phases
# - withdrawnNotice: If withdrawn, reasons and countries
```

### 7. Get All Associations for a Target

Find all diseases associated with a target, optionally filtering by score.

```python
from scripts.query_opentargets import get_target_associations

# Get associations with score >= 0.5
associations = get_target_associations(
    ensembl_id="ENSG00000157764",
    min_score=0.5
)

# Each association contains:
# - disease: {id, name}
# - score: Overall association score (0-1)
# - datatypeScores: Breakdown by evidence type
```

**Association scores:**
- Range: 0-1 (higher = stronger evidence)
- Aggregate evidence across all data types using harmonic sum
- NOT confidence scores but relative ranking metrics
- Under-studied diseases may have lower scores despite good evidence

## GraphQL API Details

**For custom queries beyond the provided helper functions**, use the GraphQL API directly or modify `scripts/query_opentargets.py`.

Key information:
- **Endpoint:** `https://api.platform.opentargets.org/api/v4/graphql`
- **Interactive browser:** `https://api.platform.opentargets.org/api/v4/graphql/browser`
- **No authentication required**
- **Request only needed fields** to minimize response size
- **Use pagination** for large result sets: `page: {size: N, index: M}`

Refer to `references/api_reference.md` for:
- Complete endpoint documentation
- Example queries for all entity types
- Error handling patterns
- Best practices for API usage

## Best Practices

### Target Prioritization Strategy

When prioritizing drug targets:

1. **Start with genetic evidence:** Human genetics (GWAS, rare variants) provides strongest disease relevance
2. **Check tractability:** Prefer targets with clinical or discovery precedence
3. **Assess safety:** Review safety liabilities, expression patterns, and genetic constraint
4. **Evaluate clinical precedence:** Known drugs indicate druggability and therapeutic window
5. **Consider multiple evidence types:** Convergent evidence from different sources increases confidence
6. **Validate mechanistically:** Pathway evidence and biological plausibility
7. **Review literature manually:** For critical decisions, examine primary publications

### Evidence Interpretation

**Strong evidence indicators:**
- Multiple independent evidence sources
- High genetic association scores (especially GWAS with L2G > 0.5)
- Clinical precedence from approved drugs
- ClinVar pathogenic variants with disease match
- Mouse models with relevant phenotypes

**Caution flags:**
- Single evidence source only
- Text-mining as sole evidence (requires manual validation)
- Conflicting evidence across sources
- High essentiality + ubiquitous expression (poor therapeutic window)
- Multiple safety liabilities

**Score interpretation:**
- Scores rank relative strength, not absolute confidence
- Under-studied diseases have lower scores despite potentially valid targets
- Weight expert-curated sources higher than computational predictions
- Check evidence breakdown, not just overall score

### Common Workflows

**Workflow 1: Target Discovery for a Disease**
1. Search for disease → get EFO ID
2. Query disease info with `include_targets=True`
3. Review top targets sorted by association score
4. For promising targets, get detailed target info
5. Examine evidence types supporting each association
6. Assess tractability and safety for prioritized targets

**Workflow 2: Target Validation**
1. Search for target → get Ensembl ID
2. Get comprehensive target info
3. Check tractability (especially clinical precedence)
4. Review safety liabilities and genetic constraint
5. Examine disease associations to understand biology
6. Look for chemical probes or tool compounds
7. Check known drugs targeting gene for mechanism insights

**Workflow 3: Drug Repurposing**
1. Search for disease → get EFO ID
2. Get known drugs for disease
3. For each drug, get detailed drug info
4. Examine mechanisms of action and targets
5. Look for related disease indications
6. Assess clinical trial phases and status
7. Identify repurposing opportunities based on mechanism

**Workflow 4: Competitive Intelligence**
1. Search for target of interest
2. Get associated diseases with evidence
3. For each disease, get known drugs
4. Review clinical phases and development status
5. Identify competitors and their mechanisms
6. Assess clinical precedence and market landscape

## Resources

### Scripts

**scripts/query_opentargets.py**
Helper functions for common API operations:
- `search_entities()` - Search for targets, diseases, or drugs
- `get_target_info()` - Retrieve target annotations
- `get_disease_info()` - Retrieve disease information
- `get_target_disease_evidence()` - Get supporting evidence
- `get_known_drugs_for_disease()` - Find drugs for a disease
- `get_drug_info()` - Retrieve drug details
- `get_target_associations()` - Get all associations for a target
- `execute_query()` - Execute custom GraphQL queries

### References

**references/api_reference.md**
Complete GraphQL API documentation including:
- Endpoint details and authentication
- Available query types (target, disease, drug, search)
- Example queries for all common operations
- Error handling and best practices
- Data licensing and citation requirements

**references/evidence_types.md**
Comprehensive guide to evidence types and data sources:
- Detailed descriptions of all 7 major evidence types
- Scoring methodologies for each source
- Evidence interpretation guidelines
- Strengths and limitations of each evidence type
- Quality assessment recommendations

**references/target_annotations.md**
Complete target annotation reference:
- 12 major annotation categories explained
- Tractability assessment details
- Safety liability sources
- Expression, essentiality, and constraint data
- Interpretation guidelines for target prioritization
- Red flags and green flags for target assessment

## Data Updates and Versioning

The Open Targets Platform is updated **quarterly** with new data releases. The current release (as of October 2025) is available at the API endpoint.

**Release information:** Check https://platform-docs.opentargets.org/release-notes for the latest updates.

**Citation:** When using Open Targets data, cite:
Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.

## Limitations and Considerations

1. **API is for exploratory queries:** For systematic analyses of many targets/diseases, use data downloads or BigQuery
2. **Scores are relative, not absolute:** Association scores rank evidence strength but don't predict clinical success
3. **Under-studied diseases score lower:** Novel or rare diseases may have strong evidence but lower aggregate scores
4. **Evidence quality varies:** Weight expert-curated sources higher than computational predictions
5. **Requires biological interpretation:** Scores and evidence must be interpreted in biological and clinical context
6. **No authentication required:** All data is freely accessible, but cite appropriately

---

## Reference: Api_Reference

# Open Targets Platform API Reference

## API Endpoint

```
https://api.platform.opentargets.org/api/v4/graphql
```

Interactive GraphQL playground with documentation:
```
https://api.platform.opentargets.org/api/v4/graphql/browser
```

## Access Methods

The Open Targets Platform provides multiple access methods:

1. **GraphQL API** - Best for single entity queries and flexible data retrieval
2. **Web Interface** - Interactive platform at https://platform.opentargets.org
3. **Data Downloads** - FTP at https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/
4. **Google BigQuery** - For large-scale systematic queries

## Authentication

No authentication is required for the GraphQL API. All data is freely accessible.

## Rate Limits

For systematic queries involving multiple targets or diseases, use dataset downloads or BigQuery instead of repeated API calls. The API is optimized for single-entity and exploratory queries.

## GraphQL Query Structure

GraphQL queries consist of:
1. Query operation with optional variables
2. Field selection (request only needed fields)
3. Nested entity traversal

### Basic Python Example

```python
import requests
import json

# Define the query
query_string = """
  query target($ensemblId: String!){
    target(ensemblId: $ensemblId){
      id
      approvedSymbol
      biotype
      geneticConstraint {
        constraintType
        exp
        obs
        score
      }
    }
  }
"""

# Define variables
variables = {"ensemblId": "ENSG00000169083"}

# Make the request
base_url = "https://api.platform.opentargets.org/api/v4/graphql"
response = requests.post(base_url, json={"query": query_string, "variables": variables})
data = json.loads(response.text)
print(data)
```

## Available Query Endpoints

### /target
Retrieve gene annotations, tractability assessments, and disease associations.

**Common fields:**
- `id` - Ensembl gene ID
- `approvedSymbol` - HGNC gene symbol
- `approvedName` - Full gene name
- `biotype` - Gene type (protein_coding, etc.)
- `tractability` - Druggability assessment
- `safetyLiabilities` - Safety information
- `expressions` - Baseline expression data
- `knownDrugs` - Approved/clinical drugs
- `associatedDiseases` - Disease associations with evidence

### /disease
Retrieve disease/phenotype data, known drugs, and clinical information.

**Common fields:**
- `id` - EFO disease identifier
- `name` - Disease name
- `description` - Disease description
- `therapeuticAreas` - High-level disease categories
- `synonyms` - Alternative names
- `knownDrugs` - Drugs indicated for disease
- `associatedTargets` - Target associations with evidence

### /drug
Retrieve compound details, mechanisms of action, and pharmacovigilance data.

**Common fields:**
- `id` - ChEMBL identifier
- `name` - Drug name
- `drugType` - Small molecule, antibody, etc.
- `maximumClinicalTrialPhase` - Development stage
- `indications` - Disease indications
- `mechanismsOfAction` - Target mechanisms
- `adverseEvents` - Pharmacovigilance data

### /search
Search across all entities (targets, diseases, drugs).

**Parameters:**
- `queryString` - Search term
- `entityNames` - Filter by entity type(s)
- `page` - Pagination

### /associationDiseaseIndirect
Retrieve target-disease associations including indirect evidence from disease descendants in ontology.

**Key fields:**
- `rows` - Association records with scores
- `aggregations` - Aggregated statistics

## Example Queries

### Query 1: Get target information with disease associations

```python
query = """
  query targetInfo($ensemblId: String!) {
    target(ensemblId: $ensemblId) {
      approvedSymbol
      approvedName
      tractability {
        label
        modality
        value
      }
      associatedDiseases(page: {size: 10}) {
        rows {
          disease {
            name
          }
          score
          datatypeScores {
            componentId
            score
          }
        }
      }
    }
  }
"""
variables = {"ensemblId": "ENSG00000157764"}
```

### Query 2: Search for diseases

```python
query = """
  query searchDiseases($queryString: String!) {
    search(queryString: $queryString, entityNames: ["disease"]) {
      hits {
        id
        entity
        name
        description
      }
    }
  }
"""
variables = {"queryString": "alzheimer"}
```

### Query 3: Get evidence for target-disease pair

```python
query = """
  query evidences($ensemblId: String!, $efoId: String!) {
    disease(efoId: $efoId) {
      evidences(ensemblIds: [$ensemblId], size: 100) {
        rows {
          datasourceId
          datatypeId
          score
          studyId
          literature
        }
      }
    }
  }
"""
variables = {"ensemblId": "ENSG00000157764", "efoId": "EFO_0000249"}
```

### Query 4: Get known drugs for a disease

```python
query = """
  query knownDrugs($efoId: String!) {
    disease(efoId: $efoId) {
      knownDrugs {
        uniqueDrugs
        rows {
          drug {
            name
            id
          }
          targets {
            approvedSymbol
          }
          phase
          status
        }
      }
    }
  }
"""
variables = {"efoId": "EFO_0000249"}
```

## Error Handling

GraphQL returns status code 200 even for errors. Check the response structure:

```python
if 'errors' in response_data:
    print(f"GraphQL errors: {response_data['errors']}")
else:
    print(f"Data: {response_data['data']}")
```

## Best Practices

1. **Request only needed fields** - Minimize data transfer and improve response time
2. **Use variables** - Make queries reusable and safer
3. **Handle pagination** - Most list fields support pagination with `page: {size: N, index: M}`
4. **Explore the schema** - Use the GraphQL browser to discover available fields
5. **Batch related queries** - Combine multiple entity fetches in a single query when possible
6. **Cache results** - Store frequently accessed data locally to reduce API calls
7. **Use BigQuery for bulk** - Switch to BigQuery/downloads for systematic analyses

## Data Licensing

All Open Targets Platform data is freely available. When using the data in research or commercial products, cite the latest publication:

Ochoa, D. et al. (2025) Open Targets Platform: facilitating therapeutic hypotheses building in drug discovery. Nucleic Acids Research, 53(D1):D1467-D1477.

---

## Reference: Evidence_Types

# Evidence Types and Data Sources

## Overview

Evidence represents any event or set of events that identifies a target as a potential causal gene or protein for a disease. Evidence is standardized and mapped to:
- **Ensembl gene IDs** for targets
- **EFO (Experimental Factor Ontology)** for diseases/phenotypes

Evidence is organized into **data types** (broader categories) and **data sources** (specific databases/studies).

## Evidence Data Types

### 1. Genetic Association

Evidence from human genetics linking genetic variants to disease phenotypes.

#### Data Sources:

**GWAS (Genome-Wide Association Studies)**
- Population-level common variant associations
- Filtered with Locus-to-Gene (L2G) scores >0.05
- Includes fine-mapping and colocalization data
- Sources: GWAS Catalog, FinnGen, UK Biobank, EBI GWAS

**Gene Burden Tests**
- Rare variant association analyses
- Aggregate effects of multiple rare variants in a gene
- Particularly relevant for Mendelian and rare diseases

**ClinVar Germline**
- Clinical variant interpretations
- Classifications: pathogenic, likely pathogenic, VUS, benign
- Expert-reviewed variant-disease associations

**Genomics England PanelApp**
- Expert gene-disease ratings
- Green (confirmed), amber (probable), red (no evidence)
- Focus on rare diseases and cancer

**Gene2Phenotype**
- Curated gene-disease relationships
- Allelic requirements and inheritance patterns
- Clinical validity assessments

**UniProt Literature & Variants**
- Literature-based gene-disease associations
- Expert-curated from scientific publications

**Orphanet**
- Rare disease gene associations
- Expert-reviewed and maintained

**ClinGen**
- Clinical genome resource classifications
- Gene-disease validity assertions

### 2. Somatic Mutations

Evidence from cancer genomics identifying driver genes and therapeutic targets.

#### Data Sources:

**Cancer Gene Census**
- Expert-curated cancer genes
- Tier classifications (1 = strong evidence, 2 = emerging)
- Mutation types and cancer types

**IntOGen**
- Computational driver gene predictions
- Aggregated from large cohort studies
- Statistical significance of mutations

**ClinVar Somatic**
- Somatic clinical variant interpretations
- Oncogenic/likely oncogenic classifications

**Cancer Biomarkers**
- FDA/EMA approved biomarkers
- Clinical trial biomarkers
- Prognostic and predictive markers

### 3. Known Drugs

Evidence from clinical precedence showing drugs targeting genes for disease indications.

#### Data Source:

**ChEMBL**
- Approved drugs (Phase 4)
- Clinical candidates (Phase 1-3)
- Withdrawn drugs
- Drug-target-indication triplets with mechanism of action

**Clinical Trial Information:**
- `phase`: Maximum clinical trial phase (1, 2, 3, 4)
- `status`: Active, terminated, completed, withdrawn
- `mechanismOfAction`: How drug affects target

### 4. Affected Pathways

Evidence linking genes to disease through pathway perturbations and functional screens.

#### Data Sources:

**CRISPR Screens**
- Genome-scale knockout screens
- Cancer dependency and essentiality data

**Project Score (Cancer Dependency Map)**
- CRISPR-Cas9 fitness screens across cancer cell lines
- Gene essentiality profiles

**SLAPenrich**
- Pathway enrichment analysis
- Somatic mutation pathway impacts

**PROGENy**
- Pathway activity inference
- Signaling pathway perturbations

**Reactome**
- Expert-curated pathway annotations
- Biological pathway representations

**Gene Signatures**
- Expression-based signatures
- Pathway activity patterns

### 5. RNA Expression

Evidence from differential gene expression in disease vs. control tissues.

#### Data Source:

**Expression Atlas**
- Differential expression data
- Baseline expression across tissues/conditions
- RNA-Seq and microarray studies
- Log2 fold-change and p-values

### 6. Animal Models

Evidence from in vivo studies showing phenotypes associated with gene perturbations.

#### Data Source:

**IMPC (International Mouse Phenotyping Consortium)**
- Systematic mouse knockout phenotypes
- Phenotype-disease mappings via ontologies
- Standardized phenotyping procedures

### 7. Literature

Evidence from text-mining of biomedical literature.

#### Data Source:

**Europe PMC**
- Co-occurrence of genes and diseases in abstracts
- Normalized citation counts
- Weighted by publication type and recency

## Evidence Scoring

Each evidence source has its own scoring methodology:

### Score Ranges
- Most scores normalized to 0-1 range
- Higher scores indicate stronger evidence
- Scores are NOT confidence levels but relative strength indicators

### Common Scoring Approaches:

**Binary Classifications:**
- ClinVar: Pathogenic (1.0), Likely pathogenic (0.99), etc.
- Gene2Phenotype: Confirmed/probable ratings
- PanelApp: Green/amber/red classifications

**Statistical Measures:**
- GWAS: L2G scores incorporating multiple lines of evidence
- Gene Burden: Statistical significance of variant aggregation
- Expression: Adjusted p-values and fold-changes

**Clinical Precedence:**
- Known Drugs: Phase weights (Phase 4 = 1.0, Phase 3 = 0.8, etc.)
- Clinical status modifiers

**Computational Predictions:**
- IntOGen: Q-values from driver mutation analysis
- PROGENy/SLAPenrich: Pathway activity/enrichment scores

## Evidence Interpretation Guidelines

### Strengths by Data Type

**Genetic Association** - Strongest human genetic evidence
- Direct link between genetic variation and disease
- Mendelian diseases: high confidence
- GWAS: requires L2G to identify causal gene
- Consider ancestry and population-specific effects

**Somatic Mutations** - Direct evidence in cancer
- Strong for oncology indications
- Driver mutations indicate therapeutic potential
- Consider cancer type specificity

**Known Drugs** - Clinical validation
- Highest confidence: approved drugs (Phase 4)
- Consider mechanism relevance to new indication
- Phase 1-2: early evidence, higher risk

**Affected Pathways** - Mechanistic insights
- Supports biological plausibility
- May not predict clinical success
- Useful for hypothesis generation

**RNA Expression** - Observational evidence
- Correlation, not causation
- May reflect disease consequence vs. cause
- Useful for biomarker identification

**Animal Models** - Translational evidence
- Strong for understanding biology
- Variable translation to human disease
- Most useful when phenotype matches human disease

**Literature** - Exploratory signal
- Text-mining captures research focus
- May reflect publication bias
- Requires manual literature review for validation

### Important Considerations

1. **Multiple evidence types strengthen confidence** - Convergent evidence from different data types provides stronger support

2. **Under-studied diseases score lower** - Novel or rare diseases may have strong evidence but lower aggregate scores due to limited research

3. **Association scores are not probabilities** - Scores rank relative evidence strength, not success probability

4. **Context matters** - Evidence strength depends on:
   - Disease mechanism understanding
   - Target biology and druggability
   - Clinical precedence in related indications
   - Safety considerations

5. **Data source reliability varies** - Weight expert-curated sources (ClinGen, Gene2Phenotype) higher than computational predictions

## Using Evidence in Queries

### Filtering by Data Type

```python
query = """
  query evidenceByType($ensemblId: String!, $efoId: String!, $dataTypes: [String!]) {
    disease(efoId: $efoId) {
      evidences(ensemblIds: [$ensemblId], datatypes: $dataTypes) {
        rows {
          datasourceId
          score
        }
      }
    }
  }
"""
variables = {
    "ensemblId": "ENSG00000157764",
    "efoId": "EFO_0000249",
    "dataTypes": ["genetic_association", "somatic_mutation"]
}
```

### Accessing Data Type Scores

Data type scores aggregate all source scores within that type:

```python
query = """
  query associationScores($ensemblId: String!, $efoId: String!) {
    target(ensemblId: $ensemblId) {
      associatedDiseases(efoIds: [$efoId]) {
        rows {
          disease {
            name
          }
          score
          datatypeScores {
            componentId
            score
          }
        }
      }
    }
  }
"""
```

## Evidence Quality Assessment

When evaluating evidence:

1. **Check multiple sources** - Single source may be unreliable
2. **Prioritize human genetic evidence** - Strongest disease relevance
3. **Consider clinical precedence** - Known drugs indicate druggability
4. **Assess mechanistic support** - Pathway evidence supports biology
5. **Review literature manually** - For critical decisions, read primary publications
6. **Validate in primary databases** - Cross-reference with ClinVar, ClinGen, etc.

---

## Reference: Target_Annotations

# Target Annotations and Features

## Overview

Open Targets defines a target as "any naturally-occurring molecule that can be targeted by a medicinal product." Targets are primarily protein-coding genes identified by Ensembl gene IDs, but also include RNAs and pseudogenes from canonical chromosomes.

## Core Target Annotations

### 1. Tractability Assessment

Tractability evaluates the druggability potential of a target across different modalities.

#### Modalities Assessed:

**Small Molecule**
- Prediction of small molecule druggability
- Based on structural features, chemical precedence
- Buckets: Clinical precedence, Discovery precedence, Predicted tractable

**Antibody**
- Likelihood of antibody-based therapeutic success
- Cell surface/secreted protein location
- Precedence categories similar to small molecules

**PROTAC (Protein Degradation)**
- Assessment for targeted protein degradation
- E3 ligase compatibility
- Emerging modality category

**Other Modalities**
- Gene therapy, RNA-based therapeutics
- Oligonucleotide approaches

#### Tractability Levels:

1. **Clinical Precedence** - Target of approved/clinical drug with similar mechanism
2. **Discovery Precedence** - Target of tool compounds or compounds in preclinical development
3. **Predicted Tractable** - Computational predictions suggest druggability
4. **Unknown** - Insufficient data to assess

### 2. Safety Liabilities

Safety information aggregated from multiple sources to identify potential toxicity concerns.

#### Data Sources:

**ToxCast**
- High-throughput toxicology screening data
- In vitro assay results
- Toxicity pathway activation

**AOPWiki (Adverse Outcome Pathways)**
- Mechanistic pathways from molecular initiating event to adverse outcome
- Systems toxicology frameworks

**PharmGKB**
- Pharmacogenomic relationships
- Genetic variants affecting drug response and toxicity

**Published Literature**
- Expert-curated safety concerns from publications
- Clinical trial adverse events

#### Safety Flags:

- **Organ toxicity** - Liver, kidney, cardiac effects
- **Target safety liability** - Known on-target toxic effects
- **Off-target effects** - Unintended activity concerns
- **Clinical observations** - Adverse events from drugs targeting gene

### 3. Baseline Expression

Gene/protein expression across tissues and cell types from multiple sources.

#### Data Sources:

**Expression Atlas**
- RNA-Seq expression across tissues/conditions
- Normalized expression levels (TPM, FPKM)
- Differential expression studies

**GTEx (Genotype-Tissue Expression)**
- Comprehensive tissue expression from healthy donors
- Median TPM across 53 tissues
- Expression variation analysis

**Human Protein Atlas**
- Protein expression via immunohistochemistry
- Subcellular localization
- Tissue specificity classifications

#### Expression Metrics:

- **TPM (Transcripts Per Million)** - Normalized RNA abundance
- **Tissue specificity** - Enrichment in specific tissues
- **Protein level** - Correlation with RNA expression
- **Subcellular location** - Where protein is found in cell

### 4. Molecular Interactions

Protein-protein interactions, complex memberships, and molecular partnerships.

#### Interaction Types:

**Physical Interactions**
- Direct protein-protein binding
- Complex components
- Sources: IntAct, BioGRID, STRING

**Pathway Membership**
- Biological pathways from Reactome
- Functional relationships
- Upstream/downstream regulators

**Target Interactors**
- Direct interactors relevant to disease associations
- Context-specific interactions

### 5. Gene Essentiality

Dependency data indicating if gene is essential for cell survival.

#### Data Sources:

**Project Score**
- CRISPR-Cas9 fitness screens
- 300+ cancer cell lines
- Scaled essentiality scores (0-1)

**DepMap Portal**
- Large-scale cancer dependency data
- Genetic and pharmacological perturbations
- Common essential genes identification

#### Essentiality Metrics:

- **Score range**: 0 (non-essential) to 1 (essential)
- **Context**: Cell line specific vs. pan-essential
- **Therapeutic window**: Selectivity between disease and normal cells

### 6. Chemical Probes and Tool Compounds

High-quality small molecules for target validation.

#### Sources:

**Probes & Drugs Portal**
- Chemical probes with characterized selectivity
- Quality ratings and annotations
- Target engagement data

**Structural Genomics Consortium (SGC)**
- Target Enabling Packages (TEPs)
- Comprehensive target reagents
- Freely available to academia

**Probe Criteria:**
- Potency (typically IC50 < 100 nM)
- Selectivity (>30-fold vs. off-targets)
- Cell activity demonstrated
- Negative control available

### 7. Pharmacogenetics

Genetic variants affecting drug response for drugs targeting the gene.

#### Data Source: ClinPGx

**Information Included:**
- Variant-drug pairs
- Clinical annotations (dosing, efficacy, toxicity)
- Evidence level and sources
- PharmGKB cross-references

**Clinical Utility:**
- Dosing adjustments based on genotype
- Contraindications for specific variants
- Efficacy predictors

### 8. Genetic Constraint

Measures of negative selection against variants in the gene.

#### Data Source: gnomAD

**Metrics:**

**pLI (probability of Loss-of-function Intolerance)**
- Range: 0-1
- pLI > 0.9 indicates intolerant to LoF variants
- High pLI suggests essentiality

**LOEUF (Loss-of-function Observed/Expected Upper bound Fraction)**
- Lower values indicate greater constraint
- More interpretable than pLI across range

**Missense Constraint**
- Z-scores for missense depletion
- O/E ratios for missense variants

**Interpretation:**
- High constraint suggests important biological function
- May indicate safety concerns if inhibited
- Essential genes often show high constraint

### 9. Comparative Genomics

Cross-species gene conservation and ortholog information.

#### Data Source: Ensembl Compara

**Ortholog Data:**
- Mouse, rat, zebrafish, other model organisms
- Orthology confidence (1:1, 1:many, many:many)
- Percent identity and similarity

**Utility:**
- Model organism studies transferability
- Functional conservation assessment
- Evolution and selective pressure

### 10. Cancer Annotations

Cancer-specific target features for oncology indications.

#### Data Sources:

**Cancer Gene Census**
- Role in cancer (oncogene, TSG, fusion)
- Tier classification (1 = established, 2 = emerging)
- Tumor types and mutation types

**Cancer Hallmarks**
- Functional roles in cancer biology
- Hallmarks: proliferation, apoptosis evasion, metastasis, etc.
- Links to specific cancer processes

**Oncology Clinical Trials**
- Drugs in development targeting gene for cancer
- Trial phases and indications

### 11. Mouse Phenotypes

Phenotypes from mouse knockout/mutation studies.

#### Data Source: MGI (Mouse Genome Informatics)

**Phenotype Data:**
- Knockout phenotypes
- Disease model associations
- Mammalian Phenotype Ontology (MP) terms

**Utility:**
- Predict on-target effects
- Safety liability identification
- Mechanism of action insights

### 12. Pathways

Biological pathway annotations placing target in functional context.

#### Data Source: Reactome

**Pathway Information:**
- Curated biological pathways
- Hierarchical organization
- Pathway diagrams with target position

**Applications:**
- Mechanism hypothesis generation
- Related target identification
- Systems biology analysis

## Using Target Annotations in Queries

### Query Template: Comprehensive Target Profile

```python
query = """
  query targetProfile($ensemblId: String!) {
    target(ensemblId: $ensemblId) {
      id
      approvedSymbol
      approvedName
      biotype

      # Tractability
      tractability {
        label
        modality
        value
      }

      # Safety
      safetyLiabilities {
        event
        effects {
          dosing
          organsAffected
        }
      }

      # Expression
      expressions {
        tissue {
          label
        }
        rna {
          value
          level
        }
        protein {
          level
        }
      }

      # Chemical probes
      chemicalProbes {
        id
        probeminer
        origin
      }

      # Known drugs
      knownDrugs {
        uniqueDrugs
        rows {
          drug {
            name
            maximumClinicalTrialPhase
          }
          phase
          status
        }
      }

      # Genetic constraint
      geneticConstraint {
        constraintType
        score
        exp
        obs
      }

      # Pathways
      pathways {
        pathway
        pathwayId
      }
    }
  }
"""

variables = {"ensemblId": "ENSG00000157764"}
```

## Annotation Interpretation Guidelines

### For Target Prioritization:

1. **Druggability (Tractability):**
   - Clinical precedence >> Discovery precedence > Predicted
   - Consider modality relevant to therapeutic approach
   - Check for existing tool compounds

2. **Safety Assessment:**
   - Review organ toxicity signals
   - Check expression in critical tissues
   - Assess genetic constraint (high = safety concern if inhibited)
   - Evaluate clinical adverse events from drugs

3. **Disease Relevance:**
   - Combine with association scores
   - Check expression in disease-relevant tissues
   - Review pathway context

4. **Validation Readiness:**
   - Chemical probes available?
   - Model organism data supportive?
   - Known drugs provide mechanism insight?

5. **Clinical Path Considerations:**
   - Pharmacogenetic factors
   - Expression pattern (tissue-specific is better for selectivity)
   - Essentiality (non-essential better for safety)

### Red Flags:

- **High essentiality + ubiquitous expression** - Poor therapeutic window
- **Multiple safety liabilities** - Toxicity concerns
- **High genetic constraint (pLI > 0.9)** - Critical gene, inhibition may be harmful
- **No tractability precedence** - Higher risk, longer development
- **Conflicting evidence** - Requires deeper investigation

### Green Flags:

- **Clinical precedence + related indication** - De-risked mechanism
- **Tissue-specific expression** - Better selectivity
- **Chemical probes available** - Faster validation
- **Low essentiality + disease relevance** - Good therapeutic window
- **Multiple evidence types converge** - Higher confidence
