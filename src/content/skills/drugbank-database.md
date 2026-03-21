---
title: "Drugbank Database"
description: "Access and analyze comprehensive drug information from the DrugBank database including drug properties, interactions, targets, pathways, chemical structures, and pharmacology data. This skill should be used when working with pharmaceutical data, d..."
category: "research"
source: "community"
author: "Community"
tags: ["drugbank", "database"]
date: 2026-03-20
---

# DrugBank Database

## Overview

DrugBank is a comprehensive bioinformatics and cheminformatics database containing detailed information on drugs and drug targets. This skill enables programmatic access to DrugBank data including ~9,591 drug entries (2,037 FDA-approved small molecules, 241 biotech drugs, 96 nutraceuticals, and 6,000+ experimental compounds) with 200+ data fields per entry.

## Core Capabilities

### 1. Data Access and Authentication

Download and access DrugBank data using Python with proper authentication. The skill provides guidance on:

- Installing and configuring the `drugbank-downloader` package
- Managing credentials securely via environment variables or config files
- Downloading specific or latest database versions
- Opening and parsing XML data efficiently
- Working with cached data to optimize performance

**When to use**: Setting up DrugBank access, downloading database updates, initial project configuration.

**Reference**: See `references/data-access.md` for detailed authentication, download procedures, API access, caching strategies, and troubleshooting.

### 2. Drug Information Queries

Extract comprehensive drug information from the database including identifiers, chemical properties, pharmacology, clinical data, and cross-references to external databases.

**Query capabilities**:
- Search by DrugBank ID, name, CAS number, or keywords
- Extract basic drug information (name, type, description, indication)
- Retrieve chemical properties (SMILES, InChI, molecular formula)
- Get pharmacology data (mechanism of action, pharmacodynamics, ADME)
- Access external identifiers (PubChem, ChEMBL, UniProt, KEGG)
- Build searchable drug datasets and export to DataFrames
- Filter drugs by type (small molecule, biotech, nutraceutical)

**When to use**: Retrieving specific drug information, building drug databases, pharmacology research, literature review, drug profiling.

**Reference**: See `references/drug-queries.md` for XML navigation, query functions, data extraction methods, and performance optimization.

### 3. Drug-Drug Interactions Analysis

Analyze drug-drug interactions (DDIs) including mechanism, clinical significance, and interaction networks for pharmacovigilance and clinical decision support.

**Analysis capabilities**:
- Extract all interactions for specific drugs
- Build bidirectional interaction networks
- Classify interactions by severity and mechanism
- Check interactions between drug pairs
- Identify drugs with most interactions
- Analyze polypharmacy regimens for safety
- Create interaction matrices and network graphs
- Perform community detection in interaction networks
- Calculate interaction risk scores

**When to use**: Polypharmacy safety analysis, clinical decision support, drug interaction prediction, pharmacovigilance research, identifying contraindications.

**Reference**: See `references/interactions.md` for interaction extraction, classification methods, network analysis, and clinical applications.

### 4. Drug Targets and Pathways

Access detailed information about drug-protein interactions including targets, enzymes, transporters, carriers, and biological pathways.

**Target analysis capabilities**:
- Extract drug targets with actions (inhibitor, agonist, antagonist)
- Identify metabolic enzymes (CYP450, Phase II enzymes)
- Analyze transporters (uptake, efflux) for ADME studies
- Map drugs to biological pathways (SMPDB)
- Find drugs targeting specific proteins
- Identify drugs with shared targets for repurposing
- Analyze polypharmacology and off-target effects
- Extract Gene Ontology (GO) terms for targets
- Cross-reference with UniProt for protein data

**When to use**: Mechanism of action studies, drug repurposing research, target identification, pathway analysis, predicting off-target effects, understanding drug metabolism.

**Reference**: See `references/targets-pathways.md` for target extraction, pathway analysis, repurposing strategies, CYP450 profiling, and transporter analysis.

### 5. Chemical Properties and Similarity

Perform structure-based analysis including molecular similarity searches, property calculations, substructure searches, and ADMET predictions.

**Chemical analysis capabilities**:
- Extract chemical structures (SMILES, InChI, molecular formula)
- Calculate physicochemical properties (MW, logP, PSA, H-bonds)
- Apply Lipinski's Rule of Five and Veber's rules
- Calculate Tanimoto similarity between molecules
- Generate molecular fingerprints (Morgan, MACCS, topological)
- Perform substructure searches with SMARTS patterns
- Find structurally similar drugs for repurposing
- Create similarity matrices for drug clustering
- Predict oral absorption and BBB permeability
- Analyze chemical space with PCA and clustering
- Export chemical property databases

**When to use**: Structure-activity relationship (SAR) studies, drug similarity searches, QSAR modeling, drug-likeness assessment, ADMET prediction, chemical space exploration.

**Reference**: See `references/chemical-analysis.md` for structure extraction, similarity calculations, fingerprint generation, ADMET predictions, and chemical space analysis.

## Typical Workflows

### Drug Discovery Workflow
1. Use `data-access.md` to download and access latest DrugBank data
2. Use `drug-queries.md` to build searchable drug database
3. Use `chemical-analysis.md` to find similar compounds
4. Use `targets-pathways.md` to identify shared targets
5. Use `interactions.md` to check safety of candidate combinations

### Polypharmacy Safety Analysis
1. Use `drug-queries.md` to look up patient medications
2. Use `interactions.md` to check all pairwise interactions
3. Use `interactions.md` to classify interaction severity
4. Use `interactions.md` to calculate overall risk score
5. Use `targets-pathways.md` to understand interaction mechanisms

### Drug Repurposing Research
1. Use `targets-pathways.md` to find drugs with shared targets
2. Use `chemical-analysis.md` to find structurally similar drugs
3. Use `drug-queries.md` to extract indication and pharmacology data
4. Use `interactions.md` to assess potential combination therapies

### Pharmacology Study
1. Use `drug-queries.md` to extract drug of interest
2. Use `targets-pathways.md` to identify all protein interactions
3. Use `targets-pathways.md` to map to biological pathways
4. Use `chemical-analysis.md` to predict ADMET properties
5. Use `interactions.md` to identify potential contraindications

## Installation Requirements

### Python Packages
```bash
uv pip install drugbank-downloader  # Core access
uv pip install bioversions          # Latest version detection
uv pip install lxml                 # XML parsing optimization
uv pip install pandas               # Data manipulation
uv pip install rdkit                # Chemical informatics (for similarity)
uv pip install networkx             # Network analysis (for interactions)
uv pip install scikit-learn         # ML/clustering (for chemical space)
```

### Account Setup
1. Create free account at go.drugbank.com
2. Accept license agreement (free for academic use)
3. Obtain username and password credentials
4. Configure credentials as documented in `references/data-access.md`

## Data Version and Reproducibility

Always specify the DrugBank version for reproducible research:

```python
from drugbank_downloader import download_drugbank
path = download_drugbank(version='5.1.10')  # Specify exact version
```

Document the version used in publications and analysis scripts.

## Best Practices

1. **Credentials**: Use environment variables or config files, never hardcode
2. **Versioning**: Specify exact database version for reproducibility
3. **Caching**: Cache parsed data to avoid re-downloading and re-parsing
4. **Namespaces**: Handle XML namespaces properly when parsing
5. **Validation**: Validate chemical structures with RDKit before use
6. **Cross-referencing**: Use external identifiers (UniProt, PubChem) for integration
7. **Clinical Context**: Always consider clinical context when interpreting interaction data
8. **License Compliance**: Ensure proper licensing for your use case

## Reference Documentation

All detailed implementation guidance is organized in modular reference files:

- **references/data-access.md**: Authentication, download, parsing, API access, caching
- **references/drug-queries.md**: XML navigation, query methods, data extraction, indexing
- **references/interactions.md**: DDI extraction, classification, network analysis, safety scoring
- **references/targets-pathways.md**: Target/enzyme/transporter extraction, pathway mapping, repurposing
- **references/chemical-analysis.md**: Structure extraction, similarity, fingerprints, ADMET prediction

Load these references as needed based on your specific analysis requirements.

---

## Reference: Chemical Analysis

# Chemical Properties and Similarity Analysis

## Overview
DrugBank provides extensive chemical property data including molecular structures, physicochemical properties, and calculated descriptors. This information enables structure-based analysis, similarity searches, and QSAR modeling.

## Chemical Identifiers and Structures

### Available Structure Formats
- **SMILES**: Simplified Molecular Input Line Entry System
- **InChI**: International Chemical Identifier
- **InChIKey**: Hashed InChI for database searching
- **Molecular Formula**: Chemical formula (e.g., C9H8O4)
- **IUPAC Name**: Systematic chemical name
- **Traditional Names**: Common names and synonyms

### Extract Chemical Structures
```python
from drugbank_downloader import get_drugbank_root

def get_drug_structures(drugbank_id):
    """Extract chemical structure representations"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            structures = {}

            # Get calculated properties
            calc_props = drug.find('db:calculated-properties', ns)
            if calc_props is not None:
                for prop in calc_props.findall('db:property', ns):
                    kind = prop.find('db:kind', ns).text
                    value = prop.find('db:value', ns).text

                    if kind in ['SMILES', 'InChI', 'InChIKey', 'Molecular Formula', 'IUPAC Name']:
                        structures[kind] = value

            return structures
    return {}

# Usage
structures = get_drug_structures('DB00001')
print(f"SMILES: {structures.get('SMILES')}")
print(f"InChI: {structures.get('InChI')}")
```

## Physicochemical Properties

### Calculated Properties
Properties computed from structure:
- **Molecular Weight**: Exact mass in Daltons
- **logP**: Partition coefficient (lipophilicity)
- **logS**: Aqueous solubility
- **Polar Surface Area (PSA)**: Topological polar surface area
- **H-Bond Donors**: Number of hydrogen bond donors
- **H-Bond Acceptors**: Number of hydrogen bond acceptors
- **Rotatable Bonds**: Number of rotatable bonds
- **Refractivity**: Molar refractivity
- **Polarizability**: Molecular polarizability

### Experimental Properties
Measured properties from literature:
- **Melting Point**: Physical melting point
- **Water Solubility**: Experimental solubility data
- **pKa**: Acid dissociation constant
- **Hydrophobicity**: Experimental logP/logD values

### Extract All Properties
```python
def get_all_properties(drugbank_id):
    """Extract all calculated and experimental properties"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            properties = {
                'calculated': {},
                'experimental': {}
            }

            # Calculated properties
            calc_props = drug.find('db:calculated-properties', ns)
            if calc_props is not None:
                for prop in calc_props.findall('db:property', ns):
                    kind = prop.find('db:kind', ns).text
                    value = prop.find('db:value', ns).text
                    source = prop.find('db:source', ns)
                    properties['calculated'][kind] = {
                        'value': value,
                        'source': source.text if source is not None else None
                    }

            # Experimental properties
            exp_props = drug.find('db:experimental-properties', ns)
            if exp_props is not None:
                for prop in exp_props.findall('db:property', ns):
                    kind = prop.find('db:kind', ns).text
                    value = prop.find('db:value', ns).text
                    properties['experimental'][kind] = value

            return properties
    return {}

# Usage
props = get_all_properties('DB00001')
print(f"Molecular Weight: {props['calculated'].get('Molecular Weight', {}).get('value')}")
print(f"logP: {props['calculated'].get('logP', {}).get('value')}")
```

## Lipinski's Rule of Five Analysis

### Rule of Five Checker
```python
def check_lipinski_rule_of_five(drugbank_id):
    """Check if drug satisfies Lipinski's Rule of Five"""
    props = get_all_properties(drugbank_id)
    calc_props = props.get('calculated', {})

    # Extract values
    mw = float(calc_props.get('Molecular Weight', {}).get('value', 0))
    logp = float(calc_props.get('logP', {}).get('value', 0))
    h_donors = int(calc_props.get('H Bond Donor Count', {}).get('value', 0))
    h_acceptors = int(calc_props.get('H Bond Acceptor Count', {}).get('value', 0))

    # Check rules
    rules = {
        'molecular_weight': mw <= 500,
        'logP': logp <= 5,
        'h_bond_donors': h_donors <= 5,
        'h_bond_acceptors': h_acceptors <= 10
    }

    violations = sum(1 for passes in rules.values() if not passes)

    return {
        'passes': violations <= 1,  # Allow 1 violation
        'violations': violations,
        'rules': rules,
        'values': {
            'molecular_weight': mw,
            'logP': logp,
            'h_bond_donors': h_donors,
            'h_bond_acceptors': h_acceptors
        }
    }

# Usage
ro5 = check_lipinski_rule_of_five('DB00001')
print(f"Passes Ro5: {ro5['passes']} (Violations: {ro5['violations']})")
```

### Veber's Rules
```python
def check_veber_rules(drugbank_id):
    """Check Veber's rules for oral bioavailability"""
    props = get_all_properties(drugbank_id)
    calc_props = props.get('calculated', {})

    psa = float(calc_props.get('Polar Surface Area (PSA)', {}).get('value', 0))
    rotatable = int(calc_props.get('Rotatable Bond Count', {}).get('value', 0))

    rules = {
        'polar_surface_area': psa <= 140,
        'rotatable_bonds': rotatable <= 10
    }

    return {
        'passes': all(rules.values()),
        'rules': rules,
        'values': {
            'psa': psa,
            'rotatable_bonds': rotatable
        }
    }
```

## Chemical Similarity Analysis

### Structure-Based Similarity with RDKit
```python
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs

def calculate_tanimoto_similarity(smiles1, smiles2):
    """Calculate Tanimoto similarity between two molecules"""
    mol1 = Chem.MolFromSmiles(smiles1)
    mol2 = Chem.MolFromSmiles(smiles2)

    if mol1 is None or mol2 is None:
        return None

    # Generate Morgan fingerprints (ECFP4)
    fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=2048)
    fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=2048)

    # Calculate Tanimoto similarity
    similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
    return similarity

# Usage
struct1 = get_drug_structures('DB00001')
struct2 = get_drug_structures('DB00002')

similarity = calculate_tanimoto_similarity(
    struct1.get('SMILES'),
    struct2.get('SMILES')
)
print(f"Tanimoto similarity: {similarity:.3f}")
```

### Find Similar Drugs
```python
def find_similar_drugs(reference_drugbank_id, similarity_threshold=0.7):
    """Find structurally similar drugs in DrugBank"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    # Get reference structure
    ref_structures = get_drug_structures(reference_drugbank_id)
    ref_smiles = ref_structures.get('SMILES')

    if not ref_smiles:
        return []

    similar_drugs = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text

        if drug_id == reference_drugbank_id:
            continue

        # Get SMILES
        drug_structures = get_drug_structures(drug_id)
        drug_smiles = drug_structures.get('SMILES')

        if drug_smiles:
            similarity = calculate_tanimoto_similarity(ref_smiles, drug_smiles)

            if similarity and similarity >= similarity_threshold:
                drug_name = drug.find('db:name', ns).text
                indication = drug.find('db:indication', ns)
                indication_text = indication.text if indication is not None else None

                similar_drugs.append({
                    'drug_id': drug_id,
                    'drug_name': drug_name,
                    'similarity': similarity,
                    'indication': indication_text
                })

    # Sort by similarity
    similar_drugs.sort(key=lambda x: x['similarity'], reverse=True)
    return similar_drugs

# Find similar drugs
similar = find_similar_drugs('DB00001', similarity_threshold=0.7)
for drug in similar[:10]:
    print(f"{drug['drug_name']}: {drug['similarity']:.3f}")
```

### Batch Similarity Matrix
```python
import numpy as np
import pandas as pd

def create_similarity_matrix(drug_ids):
    """Create pairwise similarity matrix for a list of drugs"""
    n = len(drug_ids)
    matrix = np.zeros((n, n))

    # Get all SMILES
    smiles_dict = {}
    for drug_id in drug_ids:
        structures = get_drug_structures(drug_id)
        smiles_dict[drug_id] = structures.get('SMILES')

    # Calculate similarities
    for i, drug1_id in enumerate(drug_ids):
        for j, drug2_id in enumerate(drug_ids):
            if i == j:
                matrix[i, j] = 1.0
            elif i < j:  # Only calculate upper triangle
                smiles1 = smiles_dict[drug1_id]
                smiles2 = smiles_dict[drug2_id]

                if smiles1 and smiles2:
                    sim = calculate_tanimoto_similarity(smiles1, smiles2)
                    matrix[i, j] = sim if sim is not None else 0
                    matrix[j, i] = matrix[i, j]  # Symmetric

    df = pd.DataFrame(matrix, index=drug_ids, columns=drug_ids)
    return df

# Create similarity matrix for a set of drugs
drug_list = ['DB00001', 'DB00002', 'DB00003', 'DB00005']
sim_matrix = create_similarity_matrix(drug_list)
```

## Molecular Fingerprints

### Generate Different Fingerprint Types
```python
from rdkit.Chem import MACCSkeys
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem.Fingerprints import FingerprintMols

def generate_fingerprints(smiles):
    """Generate multiple types of molecular fingerprints"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    fingerprints = {
        'morgan_fp': AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048),
        'maccs_keys': MACCSkeys.GenMACCSKeys(mol),
        'topological_fp': FingerprintMols.FingerprintMol(mol),
        'atom_pairs': Pairs.GetAtomPairFingerprint(mol)
    }

    return fingerprints

# Generate fingerprints for a drug
structures = get_drug_structures('DB00001')
fps = generate_fingerprints(structures.get('SMILES'))
```

### Substructure Search
```python
from rdkit.Chem import Fragments

def search_substructure(substructure_smarts):
    """Find drugs containing a specific substructure"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    pattern = Chem.MolFromSmarts(substructure_smarts)
    if pattern is None:
        print("Invalid SMARTS pattern")
        return []

    matching_drugs = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        structures = get_drug_structures(drug_id)
        smiles = structures.get('SMILES')

        if smiles:
            mol = Chem.MolFromSmiles(smiles)
            if mol and mol.HasSubstructMatch(pattern):
                drug_name = drug.find('db:name', ns).text
                matching_drugs.append({
                    'drug_id': drug_id,
                    'drug_name': drug_name
                })

    return matching_drugs

# Example: Find drugs with benzene ring
benzene_drugs = search_substructure('c1ccccc1')
print(f"Found {len(benzene_drugs)} drugs with benzene ring")
```

## ADMET Property Prediction

### Predict Absorption
```python
def predict_oral_absorption(drugbank_id):
    """Predict oral absorption based on physicochemical properties"""
    props = get_all_properties(drugbank_id)
    calc_props = props.get('calculated', {})

    mw = float(calc_props.get('Molecular Weight', {}).get('value', 0))
    logp = float(calc_props.get('logP', {}).get('value', 0))
    psa = float(calc_props.get('Polar Surface Area (PSA)', {}).get('value', 0))
    h_donors = int(calc_props.get('H Bond Donor Count', {}).get('value', 0))

    # Simple absorption prediction
    good_absorption = (
        mw <= 500 and
        -0.5 <= logp <= 5.0 and
        psa <= 140 and
        h_donors <= 5
    )

    absorption_score = 0
    if mw <= 500:
        absorption_score += 25
    if -0.5 <= logp <= 5.0:
        absorption_score += 25
    if psa <= 140:
        absorption_score += 25
    if h_donors <= 5:
        absorption_score += 25

    return {
        'predicted_absorption': 'good' if good_absorption else 'poor',
        'absorption_score': absorption_score,
        'properties': {
            'molecular_weight': mw,
            'logP': logp,
            'psa': psa,
            'h_donors': h_donors
        }
    }
```

### BBB Permeability Prediction
```python
def predict_bbb_permeability(drugbank_id):
    """Predict blood-brain barrier permeability"""
    props = get_all_properties(drugbank_id)
    calc_props = props.get('calculated', {})

    mw = float(calc_props.get('Molecular Weight', {}).get('value', 0))
    logp = float(calc_props.get('logP', {}).get('value', 0))
    psa = float(calc_props.get('Polar Surface Area (PSA)', {}).get('value', 0))
    h_donors = int(calc_props.get('H Bond Donor Count', {}).get('value', 0))

    # BBB permeability criteria (simplified)
    bbb_permeable = (
        mw <= 450 and
        logp <= 5.0 and
        psa <= 90 and
        h_donors <= 3
    )

    return {
        'bbb_permeable': bbb_permeable,
        'properties': {
            'molecular_weight': mw,
            'logP': logp,
            'psa': psa,
            'h_donors': h_donors
        }
    }
```

## Chemical Space Analysis

### Principal Component Analysis
```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def perform_chemical_space_pca(drug_ids):
    """Perform PCA on chemical descriptor space"""
    # Extract properties for all drugs
    properties_list = []
    valid_ids = []

    for drug_id in drug_ids:
        props = get_all_properties(drug_id)
        calc_props = props.get('calculated', {})

        try:
            prop_vector = [
                float(calc_props.get('Molecular Weight', {}).get('value', 0)),
                float(calc_props.get('logP', {}).get('value', 0)),
                float(calc_props.get('Polar Surface Area (PSA)', {}).get('value', 0)),
                int(calc_props.get('H Bond Donor Count', {}).get('value', 0)),
                int(calc_props.get('H Bond Acceptor Count', {}).get('value', 0)),
                int(calc_props.get('Rotatable Bond Count', {}).get('value', 0)),
            ]
            properties_list.append(prop_vector)
            valid_ids.append(drug_id)
        except (ValueError, TypeError):
            continue

    # Perform PCA
    X = np.array(properties_list)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Create DataFrame
    df = pd.DataFrame({
        'drug_id': valid_ids,
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1]
    })

    return df, pca

# Visualize chemical space
# drug_list = [all approved drugs]
# pca_df, pca_model = perform_chemical_space_pca(drug_list)
```

### Clustering by Chemical Properties
```python
from sklearn.cluster import KMeans

def cluster_drugs_by_properties(drug_ids, n_clusters=10):
    """Cluster drugs based on chemical properties"""
    properties_list = []
    valid_ids = []

    for drug_id in drug_ids:
        props = get_all_properties(drug_id)
        calc_props = props.get('calculated', {})

        try:
            prop_vector = [
                float(calc_props.get('Molecular Weight', {}).get('value', 0)),
                float(calc_props.get('logP', {}).get('value', 0)),
                float(calc_props.get('Polar Surface Area (PSA)', {}).get('value', 0)),
                int(calc_props.get('H Bond Donor Count', {}).get('value', 0)),
                int(calc_props.get('H Bond Acceptor Count', {}).get('value', 0)),
            ]
            properties_list.append(prop_vector)
            valid_ids.append(drug_id)
        except (ValueError, TypeError):
            continue

    X = np.array(properties_list)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    df = pd.DataFrame({
        'drug_id': valid_ids,
        'cluster': clusters
    })

    return df, kmeans
```

## Export Chemical Data

### Create Chemical Property Database
```python
def export_chemical_properties(output_file='drugbank_chemical_properties.csv'):
    """Export all chemical properties to CSV"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    all_properties = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        drug_name = drug.find('db:name', ns).text

        props = get_all_properties(drug_id)
        calc_props = props.get('calculated', {})

        property_dict = {
            'drug_id': drug_id,
            'drug_name': drug_name,
            'smiles': calc_props.get('SMILES', {}).get('value'),
            'inchi': calc_props.get('InChI', {}).get('value'),
            'inchikey': calc_props.get('InChIKey', {}).get('value'),
            'molecular_weight': calc_props.get('Molecular Weight', {}).get('value'),
            'logP': calc_props.get('logP', {}).get('value'),
            'psa': calc_props.get('Polar Surface Area (PSA)', {}).get('value'),
            'h_donors': calc_props.get('H Bond Donor Count', {}).get('value'),
            'h_acceptors': calc_props.get('H Bond Acceptor Count', {}).get('value'),
            'rotatable_bonds': calc_props.get('Rotatable Bond Count', {}).get('value'),
        }

        all_properties.append(property_dict)

    df = pd.DataFrame(all_properties)
    df.to_csv(output_file, index=False)
    print(f"Exported {len(all_properties)} drug properties to {output_file}")

# Usage
export_chemical_properties()
```

## Best Practices

1. **Structure Validation**: Always validate SMILES/InChI before use with RDKit
2. **Multiple Descriptors**: Use multiple fingerprint types for comprehensive similarity
3. **Threshold Selection**: Tanimoto >0.85 = very similar, 0.7-0.85 = similar, <0.7 = different
4. **Rule Application**: Lipinski's Ro5 and Veber's rules are guidelines, not absolute cutoffs
5. **ADMET Prediction**: Use computational predictions as screening, validate experimentally
6. **Chemical Space**: Visualize chemical space to understand drug diversity
7. **Standardization**: Standardize molecules (neutralize, remove salts) before comparison
8. **Performance**: Cache computed fingerprints for large-scale similarity searches

---

## Reference: Data Access

# DrugBank Data Access

## Authentication and Setup

### Account Creation
DrugBank requires user authentication to access data:
1. Create account at go.drugbank.com
2. Accept the license agreement (free for academic use, paid for commercial)
3. Obtain username and password credentials

### Credential Management

**Environment Variables (Recommended)**
```bash
export DRUGBANK_USERNAME="your_username"
export DRUGBANK_PASSWORD="your_password"
```

**Configuration File**
Create `~/.config/drugbank.ini`:
```ini
[drugbank]
username = your_username
password = your_password
```

**Direct Specification**
```python
# Pass credentials directly (not recommended for production)
download_drugbank(username="user", password="pass")
```

## Python Package Installation

### drugbank-downloader
Primary tool for programmatic access:
```bash
pip install drugbank-downloader
```

**Requirements:** Python >=3.9

### Optional Dependencies
```bash
pip install bioversions  # For automatic latest version detection
pip install lxml  # For XML parsing optimization
```

## Data Download Methods

### Download Full Database
```python
from drugbank_downloader import download_drugbank

# Download specific version
path = download_drugbank(version='5.1.7')
# Returns: ~/.data/drugbank/5.1.7/full database.xml.zip

# Download latest version (requires bioversions)
path = download_drugbank()
```

### Custom Storage Location
```python
# Custom prefix for storage
path = download_drugbank(prefix=['custom', 'location', 'drugbank'])
# Stores at: ~/.data/custom/location/drugbank/[version]/
```

### Verify Download
```python
import os
if os.path.exists(path):
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"Downloaded successfully: {size_mb:.1f} MB")
```

## Working with Downloaded Data

### Open Zipped XML Without Extraction
```python
from drugbank_downloader import open_drugbank
import xml.etree.ElementTree as ET

# Open file directly from zip
with open_drugbank() as file:
    tree = ET.parse(file)
    root = tree.getroot()
```

### Parse XML Tree
```python
from drugbank_downloader import parse_drugbank, get_drugbank_root

# Get parsed tree
tree = parse_drugbank()

# Get root element directly
root = get_drugbank_root()
```

### CLI Usage
```bash
# Download using command line
drugbank_downloader --username USER --password PASS

# Download latest version
drugbank_downloader
```

## Data Formats and Versions

### Available Formats
- **XML**: Primary format, most comprehensive data
- **JSON**: Available via API (requires separate API key)
- **CSV/TSV**: Export from web interface or parse XML
- **SQL**: Database dumps available for download

### Version Management
```python
# Specify exact version for reproducibility
path = download_drugbank(version='5.1.10')

# List cached versions
from pathlib import Path
drugbank_dir = Path.home() / '.data' / 'drugbank'
if drugbank_dir.exists():
    versions = [d.name for d in drugbank_dir.iterdir() if d.is_dir()]
    print(f"Cached versions: {versions}")
```

### Version History
- **Version 6.0** (2024): Latest release, expanded drug entries
- **Version 5.1.x** (2019-2023): Incremental updates
- **Version 5.0** (2017): ~9,591 drug entries
- **Version 4.0** (2014): Added metabolite structures
- **Version 3.0** (2011): Added transporter and pathway data
- **Version 2.0** (2009): Added interactions and ADMET

## API Access

### REST API Endpoints
```python
import requests

# Query by DrugBank ID
drug_id = "DB00001"
url = f"https://go.drugbank.com/drugs/{drug_id}.json"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    drug_data = response.json()
```

### Rate Limits
- **Development Key**: 3,000 requests/month
- **Production Key**: Custom limits based on license
- **Best Practice**: Cache results locally to minimize API calls

### Regional Scoping
DrugBank API is scoped by region:
- **USA**: FDA-approved drugs
- **Canada**: Health Canada-approved drugs
- **EU**: EMA-approved drugs

Specify region in API requests when applicable.

## Data Caching Strategy

### Intermediate Results
```python
import pickle
from pathlib import Path

# Cache parsed data
cache_file = Path("drugbank_parsed.pkl")

if cache_file.exists():
    with open(cache_file, 'rb') as f:
        data = pickle.load(f)
else:
    # Parse and process
    root = get_drugbank_root()
    data = process_drugbank_data(root)

    # Save cache
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
```

### Version-Specific Caching
```python
version = "5.1.10"
cache_file = Path(f"drugbank_{version}_processed.pkl")
# Ensures cache invalidation when version changes
```

## Troubleshooting

### Common Issues

**Authentication Failures**
- Verify credentials are correct
- Check license agreement is accepted
- Ensure account has not expired

**Download Failures**
- Check internet connectivity
- Verify sufficient disk space (~1-2 GB needed)
- Try specifying an older version if latest fails

**Parsing Errors**
- Ensure complete download (check file size)
- Verify XML is not corrupted
- Use lxml parser for better error handling

### Error Handling
```python
from drugbank_downloader import download_drugbank
import logging

logging.basicConfig(level=logging.INFO)

try:
    path = download_drugbank()
    print(f"Success: {path}")
except Exception as e:
    print(f"Download failed: {e}")
    # Fallback: specify older stable version
    path = download_drugbank(version='5.1.7')
```

## Best Practices

1. **Version Specification**: Always specify exact version for reproducible research
2. **Credential Security**: Use environment variables, never hardcode credentials
3. **Caching**: Cache intermediate processing results to avoid re-parsing
4. **Documentation**: Document which DrugBank version was used in analysis
5. **License Compliance**: Ensure proper licensing for your use case
6. **Local Storage**: Keep local copies to reduce download frequency
7. **Error Handling**: Implement robust error handling for network issues

---

## Reference: Drug Queries

# Drug Information Queries

## Overview
DrugBank provides comprehensive drug information with 200+ data fields per entry including chemical properties, pharmacology, mechanisms of action, and clinical data.

## Database Contents

### Drug Categories
- **FDA-Approved Small Molecules**: ~2,037 drugs
- **Biotech/Biologic Drugs**: ~241 entries
- **Nutraceuticals**: ~96 compounds
- **Experimental Drugs**: ~6,000+ compounds
- **Withdrawn/Discontinued**: Historical drugs with safety data

### Data Fields (200+ per entry)
- **Identifiers**: DrugBank ID, CAS number, UNII, PubChem CID
- **Names**: Generic, brand, synonyms, IUPAC
- **Chemical**: Structure (SMILES, InChI), formula, molecular weight
- **Pharmacology**: Indication, mechanism of action, pharmacodynamics
- **Pharmacokinetics**: Absorption, distribution, metabolism, excretion (ADME)
- **Toxicity**: LD50, adverse effects, contraindications
- **Clinical**: Dosage forms, routes of administration, half-life
- **Targets**: Proteins, enzymes, transporters, carriers
- **Interactions**: Drug-drug, drug-food interactions
- **References**: Citations to literature and clinical studies

## XML Structure Navigation

### Basic XML Structure
```xml
<drugbank>
  <drug type="small molecule" created="..." updated="...">
    <drugbank-id primary="true">DB00001</drugbank-id>
    <name>Lepirudin</name>
    <description>...</description>
    <cas-number>...</cas-number>
    <synthesis-reference>...</synthesis-reference>
    <indication>...</indication>
    <pharmacodynamics>...</pharmacodynamics>
    <mechanism-of-action>...</mechanism-of-action>
    <toxicity>...</toxicity>
    <metabolism>...</metabolism>
    <absorption>...</absorption>
    <half-life>...</half-life>
    <protein-binding>...</protein-binding>
    <route-of-elimination>...</route-of-elimination>
    <calculated-properties>...</calculated-properties>
    <experimental-properties>...</experimental-properties>
    <targets>...</targets>
    <enzymes>...</enzymes>
    <transporters>...</transporters>
    <drug-interactions>...</drug-interactions>
  </drug>
</drugbank>
```

### Namespaces
DrugBank XML uses namespaces. Handle them properly:
```python
import xml.etree.ElementTree as ET

# Define namespace
ns = {'db': 'http://www.drugbank.ca'}

# Query with namespace
root = get_drugbank_root()
drugs = root.findall('db:drug', ns)
```

## Query by Drug Identifier

### Query by DrugBank ID
```python
from drugbank_downloader import get_drugbank_root

def get_drug_by_id(drugbank_id):
    """Retrieve drug entry by DrugBank ID (e.g., 'DB00001')"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            return drug
    return None

# Example usage
drug = get_drug_by_id('DB00001')
if drug:
    name = drug.find('db:name', ns).text
    print(f"Drug: {name}")
```

### Query by Name
```python
def get_drug_by_name(drug_name):
    """Find drug by name (case-insensitive)"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drug_name_lower = drug_name.lower()

    for drug in root.findall('db:drug', ns):
        name_elem = drug.find('db:name', ns)
        if name_elem is not None and name_elem.text.lower() == drug_name_lower:
            return drug

        # Also check synonyms
        for synonym in drug.findall('.//db:synonym', ns):
            if synonym.text and synonym.text.lower() == drug_name_lower:
                return drug
    return None

# Example
drug = get_drug_by_name('Aspirin')
```

### Query by CAS Number
```python
def get_drug_by_cas(cas_number):
    """Find drug by CAS registry number"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        cas_elem = drug.find('db:cas-number', ns)
        if cas_elem is not None and cas_elem.text == cas_number:
            return drug
    return None
```

## Extract Specific Information

### Basic Drug Information
```python
def extract_basic_info(drug):
    """Extract essential drug information"""
    ns = {'db': 'http://www.drugbank.ca'}

    info = {
        'drugbank_id': drug.find('db:drugbank-id[@primary="true"]', ns).text,
        'name': drug.find('db:name', ns).text,
        'type': drug.get('type'),
        'cas_number': get_text_safe(drug.find('db:cas-number', ns)),
        'description': get_text_safe(drug.find('db:description', ns)),
        'indication': get_text_safe(drug.find('db:indication', ns)),
    }
    return info

def get_text_safe(element):
    """Safely get text from element, return None if not found"""
    return element.text if element is not None else None
```

### Chemical Properties
```python
def extract_chemical_properties(drug):
    """Extract chemical structure and properties"""
    ns = {'db': 'http://www.drugbank.ca'}

    properties = {}

    # Calculated properties
    calc_props = drug.find('db:calculated-properties', ns)
    if calc_props is not None:
        for prop in calc_props.findall('db:property', ns):
            kind = prop.find('db:kind', ns).text
            value = prop.find('db:value', ns).text
            properties[kind] = value

    # Experimental properties
    exp_props = drug.find('db:experimental-properties', ns)
    if exp_props is not None:
        for prop in exp_props.findall('db:property', ns):
            kind = prop.find('db:kind', ns).text
            value = prop.find('db:value', ns).text
            properties[f"{kind}_experimental"] = value

    return properties

# Common properties to extract:
# - SMILES
# - InChI
# - InChIKey
# - Molecular Formula
# - Molecular Weight
# - logP (partition coefficient)
# - Water Solubility
# - Melting Point
# - pKa
```

### Pharmacology Information
```python
def extract_pharmacology(drug):
    """Extract pharmacological information"""
    ns = {'db': 'http://www.drugbank.ca'}

    pharm = {
        'indication': get_text_safe(drug.find('db:indication', ns)),
        'pharmacodynamics': get_text_safe(drug.find('db:pharmacodynamics', ns)),
        'mechanism_of_action': get_text_safe(drug.find('db:mechanism-of-action', ns)),
        'toxicity': get_text_safe(drug.find('db:toxicity', ns)),
        'metabolism': get_text_safe(drug.find('db:metabolism', ns)),
        'absorption': get_text_safe(drug.find('db:absorption', ns)),
        'half_life': get_text_safe(drug.find('db:half-life', ns)),
        'protein_binding': get_text_safe(drug.find('db:protein-binding', ns)),
        'route_of_elimination': get_text_safe(drug.find('db:route-of-elimination', ns)),
        'volume_of_distribution': get_text_safe(drug.find('db:volume-of-distribution', ns)),
        'clearance': get_text_safe(drug.find('db:clearance', ns)),
    }
    return pharm
```

### External Identifiers
```python
def extract_external_identifiers(drug):
    """Extract cross-references to other databases"""
    ns = {'db': 'http://www.drugbank.ca'}

    identifiers = {}

    external_ids = drug.find('db:external-identifiers', ns)
    if external_ids is not None:
        for ext_id in external_ids.findall('db:external-identifier', ns):
            resource = ext_id.find('db:resource', ns).text
            identifier = ext_id.find('db:identifier', ns).text
            identifiers[resource] = identifier

    return identifiers

# Common external databases:
# - PubChem Compound
# - PubChem Substance
# - ChEMBL
# - ChEBI
# - UniProtKB
# - KEGG Drug
# - PharmGKB
# - RxCUI (RxNorm)
# - ZINC
```

## Building Drug Datasets

### Create Drug Dictionary
```python
def build_drug_database():
    """Build searchable dictionary of all drugs"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drug_db = {}

    for drug in root.findall('db:drug', ns):
        db_id = drug.find('db:drugbank-id[@primary="true"]', ns).text

        drug_info = {
            'id': db_id,
            'name': get_text_safe(drug.find('db:name', ns)),
            'type': drug.get('type'),
            'description': get_text_safe(drug.find('db:description', ns)),
            'cas': get_text_safe(drug.find('db:cas-number', ns)),
            'indication': get_text_safe(drug.find('db:indication', ns)),
        }

        drug_db[db_id] = drug_info

    return drug_db

# Create searchable database
drugs = build_drug_database()
print(f"Total drugs: {len(drugs)}")
```

### Export to DataFrame
```python
import pandas as pd

def create_drug_dataframe():
    """Create pandas DataFrame of drug information"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drugs_data = []

    for drug in root.findall('db:drug', ns):
        drug_dict = {
            'drugbank_id': drug.find('db:drugbank-id[@primary="true"]', ns).text,
            'name': get_text_safe(drug.find('db:name', ns)),
            'type': drug.get('type'),
            'cas_number': get_text_safe(drug.find('db:cas-number', ns)),
            'description': get_text_safe(drug.find('db:description', ns)),
            'indication': get_text_safe(drug.find('db:indication', ns)),
        }
        drugs_data.append(drug_dict)

    df = pd.DataFrame(drugs_data)
    return df

# Usage
df = create_drug_dataframe()
df.to_csv('drugbank_drugs.csv', index=False)
```

### Filter by Drug Type
```python
def filter_by_type(drug_type='small molecule'):
    """Get drugs of specific type"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    filtered_drugs = []

    for drug in root.findall('db:drug', ns):
        if drug.get('type') == drug_type:
            db_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
            name = get_text_safe(drug.find('db:name', ns))
            filtered_drugs.append({'id': db_id, 'name': name})

    return filtered_drugs

# Get all biotech drugs
biotech_drugs = filter_by_type('biotech')
```

### Search by Keyword
```python
def search_drugs_by_keyword(keyword, field='indication'):
    """Search drugs by keyword in specific field"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    results = []
    keyword_lower = keyword.lower()

    for drug in root.findall('db:drug', ns):
        field_elem = drug.find(f'db:{field}', ns)
        if field_elem is not None and field_elem.text:
            if keyword_lower in field_elem.text.lower():
                db_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
                name = get_text_safe(drug.find('db:name', ns))
                results.append({
                    'id': db_id,
                    'name': name,
                    field: field_elem.text[:200]  # First 200 chars
                })

    return results

# Example: Find drugs for cancer treatment
cancer_drugs = search_drugs_by_keyword('cancer', 'indication')
```

## Performance Optimization

### Indexing for Faster Queries
```python
def build_indexes():
    """Build indexes for faster lookups"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    # Index by ID, name, and CAS
    id_index = {}
    name_index = {}
    cas_index = {}

    for drug in root.findall('db:drug', ns):
        db_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        id_index[db_id] = drug

        name = get_text_safe(drug.find('db:name', ns))
        if name:
            name_index[name.lower()] = drug

        cas = get_text_safe(drug.find('db:cas-number', ns))
        if cas:
            cas_index[cas] = drug

    return {'id': id_index, 'name': name_index, 'cas': cas_index}

# Build once, query many times
indexes = build_indexes()
drug = indexes['name'].get('aspirin')
```

---

## Reference: Interactions

# Drug-Drug Interactions

## Overview
DrugBank provides comprehensive drug-drug interaction (DDI) data including mechanism, severity, and clinical significance. This information is critical for pharmacovigilance, clinical decision support, and drug safety research.

## Interaction Data Structure

### XML Structure
```xml
<drug-interactions>
  <drug-interaction>
    <drugbank-id>DB00001</drugbank-id>
    <name>Warfarin</name>
    <description>The risk or severity of adverse effects can be increased...</description>
  </drug-interaction>
  <drug-interaction>
    <drugbank-id>DB00002</drugbank-id>
    <name>Aspirin</name>
    <description>May increase the anticoagulant activities...</description>
  </drug-interaction>
</drug-interactions>
```

### Interaction Components
- **drugbank-id**: DrugBank ID of interacting drug
- **name**: Name of interacting drug
- **description**: Detailed description of interaction mechanism and clinical significance

## Extract Drug Interactions

### Basic Interaction Extraction
```python
from drugbank_downloader import get_drugbank_root

def get_drug_interactions(drugbank_id):
    """Get all interactions for a specific drug"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    # Find the drug
    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            interactions = []

            # Extract interactions
            ddi_elem = drug.find('db:drug-interactions', ns)
            if ddi_elem is not None:
                for interaction in ddi_elem.findall('db:drug-interaction', ns):
                    interaction_data = {
                        'partner_id': interaction.find('db:drugbank-id', ns).text,
                        'partner_name': interaction.find('db:name', ns).text,
                        'description': interaction.find('db:description', ns).text
                    }
                    interactions.append(interaction_data)

            return interactions
    return []

# Example usage
interactions = get_drug_interactions('DB00001')
print(f"Found {len(interactions)} interactions")
```

### Bidirectional Interaction Mapping
```python
def build_interaction_network():
    """Build complete interaction network (all drug pairs)"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    interaction_network = {}

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text

        ddi_elem = drug.find('db:drug-interactions', ns)
        if ddi_elem is not None:
            interactions = []
            for interaction in ddi_elem.findall('db:drug-interaction', ns):
                partner_id = interaction.find('db:drugbank-id', ns).text
                interactions.append(partner_id)

            interaction_network[drug_id] = interactions

    return interaction_network

# Usage
network = build_interaction_network()
```

## Analyze Interaction Patterns

### Count Interactions per Drug
```python
def rank_drugs_by_interactions():
    """Rank drugs by number of known interactions"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drug_interaction_counts = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        drug_name = drug.find('db:name', ns).text

        ddi_elem = drug.find('db:drug-interactions', ns)
        count = 0
        if ddi_elem is not None:
            count = len(ddi_elem.findall('db:drug-interaction', ns))

        drug_interaction_counts.append({
            'id': drug_id,
            'name': drug_name,
            'interaction_count': count
        })

    # Sort by count
    drug_interaction_counts.sort(key=lambda x: x['interaction_count'], reverse=True)
    return drug_interaction_counts

# Get top 10 drugs with most interactions
top_drugs = rank_drugs_by_interactions()[:10]
for drug in top_drugs:
    print(f"{drug['name']}: {drug['interaction_count']} interactions")
```

### Find Common Interaction Partners
```python
def find_common_interactors(drugbank_id1, drugbank_id2):
    """Find drugs that interact with both specified drugs"""
    interactions1 = set(i['partner_id'] for i in get_drug_interactions(drugbank_id1))
    interactions2 = set(i['partner_id'] for i in get_drug_interactions(drugbank_id2))

    common = interactions1.intersection(interactions2)
    return list(common)

# Example
common = find_common_interactors('DB00001', 'DB00002')
print(f"Common interacting drugs: {len(common)}")
```

### Check Specific Drug Pair
```python
def check_interaction(drug1_id, drug2_id):
    """Check if two drugs interact and get details"""
    interactions = get_drug_interactions(drug1_id)

    for interaction in interactions:
        if interaction['partner_id'] == drug2_id:
            return interaction

    # Check reverse direction
    interactions_reverse = get_drug_interactions(drug2_id)
    for interaction in interactions_reverse:
        if interaction['partner_id'] == drug1_id:
            return interaction

    return None

# Usage
interaction = check_interaction('DB00001', 'DB00002')
if interaction:
    print(f"Interaction found: {interaction['description']}")
else:
    print("No interaction found")
```

## Interaction Classification

### Parse Interaction Descriptions
```python
import re

def classify_interaction_severity(description):
    """Classify interaction severity based on description keywords"""
    description_lower = description.lower()

    # Severity indicators
    if any(word in description_lower for word in ['contraindicated', 'avoid', 'should not']):
        return 'major'
    elif any(word in description_lower for word in ['may increase', 'can increase', 'risk']):
        return 'moderate'
    elif any(word in description_lower for word in ['may decrease', 'minor', 'monitor']):
        return 'minor'
    else:
        return 'unknown'

def classify_interaction_mechanism(description):
    """Extract interaction mechanism from description"""
    description_lower = description.lower()

    mechanisms = []

    if 'metabolism' in description_lower or 'cyp' in description_lower:
        mechanisms.append('metabolic')
    if 'absorption' in description_lower:
        mechanisms.append('absorption')
    if 'excretion' in description_lower or 'renal' in description_lower:
        mechanisms.append('excretion')
    if 'synergistic' in description_lower or 'additive' in description_lower:
        mechanisms.append('pharmacodynamic')
    if 'protein binding' in description_lower:
        mechanisms.append('protein_binding')

    return mechanisms if mechanisms else ['unspecified']
```

### Categorize Interactions
```python
def categorize_drug_interactions(drugbank_id):
    """Categorize interactions by severity and mechanism"""
    interactions = get_drug_interactions(drugbank_id)

    categorized = {
        'major': [],
        'moderate': [],
        'minor': [],
        'unknown': []
    }

    for interaction in interactions:
        severity = classify_interaction_severity(interaction['description'])
        interaction['severity'] = severity
        interaction['mechanisms'] = classify_interaction_mechanism(interaction['description'])
        categorized[severity].append(interaction)

    return categorized

# Usage
categorized = categorize_drug_interactions('DB00001')
print(f"Major: {len(categorized['major'])}")
print(f"Moderate: {len(categorized['moderate'])}")
print(f"Minor: {len(categorized['minor'])}")
```

## Build Interaction Matrix

### Create Pairwise Interaction Matrix
```python
import pandas as pd
import numpy as np

def create_interaction_matrix(drug_ids):
    """Create binary interaction matrix for specified drugs"""
    n = len(drug_ids)
    matrix = np.zeros((n, n), dtype=int)

    # Build index mapping
    id_to_idx = {drug_id: idx for idx, drug_id in enumerate(drug_ids)}

    # Fill matrix
    for i, drug_id in enumerate(drug_ids):
        interactions = get_drug_interactions(drug_id)
        for interaction in interactions:
            partner_id = interaction['partner_id']
            if partner_id in id_to_idx:
                j = id_to_idx[partner_id]
                matrix[i, j] = 1
                matrix[j, i] = 1  # Symmetric

    df = pd.DataFrame(matrix, index=drug_ids, columns=drug_ids)
    return df

# Example: Create matrix for top 100 drugs
top_100_drugs = [drug['id'] for drug in rank_drugs_by_interactions()[:100]]
interaction_matrix = create_interaction_matrix(top_100_drugs)
```

### Export Interaction Network
```python
def export_interaction_network_csv(output_file='drugbank_interactions.csv'):
    """Export all interactions as edge list (CSV)"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    edges = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        drug_name = drug.find('db:name', ns).text

        ddi_elem = drug.find('db:drug-interactions', ns)
        if ddi_elem is not None:
            for interaction in ddi_elem.findall('db:drug-interaction', ns):
                partner_id = interaction.find('db:drugbank-id', ns).text
                partner_name = interaction.find('db:name', ns).text
                description = interaction.find('db:description', ns).text

                edges.append({
                    'drug1_id': drug_id,
                    'drug1_name': drug_name,
                    'drug2_id': partner_id,
                    'drug2_name': partner_name,
                    'description': description
                })

    df = pd.DataFrame(edges)
    df.to_csv(output_file, index=False)
    print(f"Exported {len(edges)} interactions to {output_file}")

# Usage
export_interaction_network_csv()
```

## Network Analysis

### Graph Representation
```python
import networkx as nx

def build_interaction_graph():
    """Build NetworkX graph of drug interactions"""
    network = build_interaction_network()

    G = nx.Graph()

    # Add nodes and edges
    for drug_id, partners in network.items():
        G.add_node(drug_id)
        for partner_id in partners:
            G.add_edge(drug_id, partner_id)

    return G

# Build graph
G = build_interaction_graph()
print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# Network statistics
density = nx.density(G)
print(f"Network density: {density:.4f}")

# Find highly connected drugs (hubs)
degree_dict = dict(G.degree())
top_hubs = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 hubs:", top_hubs)
```

### Community Detection
```python
def detect_interaction_communities():
    """Detect communities in interaction network"""
    G = build_interaction_graph()

    # Louvain community detection
    from networkx.algorithms import community
    communities = community.louvain_communities(G)

    print(f"Detected {len(communities)} communities")

    # Analyze communities
    for i, comm in enumerate(communities[:5], 1):  # Top 5 communities
        print(f"Community {i}: {len(comm)} drugs")

    return communities

# Usage
communities = detect_interaction_communities()
```

## Clinical Applications

### Polypharmacy Analysis
```python
def check_polypharmacy_interactions(drug_list):
    """Check for interactions in a drug regimen"""
    print(f"Checking interactions for {len(drug_list)} drugs...")

    all_interactions = []

    # Check all pairs
    for i, drug1 in enumerate(drug_list):
        for drug2 in drug_list[i+1:]:
            interaction = check_interaction(drug1, drug2)
            if interaction:
                interaction['drug1'] = drug1
                interaction['drug2'] = drug2
                all_interactions.append(interaction)

    return all_interactions

# Example: Check patient drug regimen
patient_drugs = ['DB00001', 'DB00002', 'DB00005', 'DB00009']
interactions = check_polypharmacy_interactions(patient_drugs)

print(f"\nFound {len(interactions)} interactions:")
for interaction in interactions:
    print(f"\n{interaction['drug1']} + {interaction['drug2']}")
    print(f"  {interaction['description'][:100]}...")
```

### Interaction Risk Score
```python
def calculate_interaction_risk_score(drug_list):
    """Calculate overall interaction risk for drug combination"""
    interactions = check_polypharmacy_interactions(drug_list)

    severity_weights = {'major': 3, 'moderate': 2, 'minor': 1, 'unknown': 1}

    total_score = 0
    for interaction in interactions:
        severity = classify_interaction_severity(interaction['description'])
        total_score += severity_weights[severity]

    return {
        'total_interactions': len(interactions),
        'risk_score': total_score,
        'average_severity': total_score / len(interactions) if interactions else 0
    }

# Usage
risk = calculate_interaction_risk_score(patient_drugs)
print(f"Risk Score: {risk['risk_score']}, Avg Severity: {risk['average_severity']:.2f}")
```

## Best Practices

1. **Bidirectional Checking**: Always check interactions in both directions (A→B and B→A)
2. **Context Matters**: Consider clinical context when interpreting interaction significance
3. **Up-to-date Data**: Use latest DrugBank version for most current interaction data
4. **Severity Classification**: Implement custom classification based on your clinical needs
5. **Network Analysis**: Use graph analysis to identify high-risk drug combinations
6. **Clinical Validation**: Cross-reference with clinical guidelines and literature
7. **Documentation**: Document DrugBank version and analysis methods for reproducibility

---

## Reference: Targets Pathways

# Drug Targets and Pathways

## Overview
DrugBank provides comprehensive information about drug-protein interactions including targets, enzymes, transporters, and carriers. This data is essential for understanding drug mechanisms, identifying repurposing opportunities, and predicting off-target effects.

## Protein Interaction Categories

### Target Proteins
Primary proteins that drugs bind to produce therapeutic effects:
- **Receptors**: G-protein coupled receptors, nuclear receptors, ion channels
- **Enzymes**: Kinases, proteases, phosphatases
- **Transporters**: Used as targets (not just for ADME)
- **Other**: Structural proteins, DNA/RNA

### Metabolic Enzymes
Enzymes involved in drug metabolism:
- **Cytochrome P450 enzymes**: CYP3A4, CYP2D6, CYP2C9, etc.
- **Phase II enzymes**: UGTs, SULTs, GSTs
- **Esterases and peptidases**

### Transporters
Proteins involved in drug transport across membranes:
- **Uptake transporters**: OATPs, OCTs
- **Efflux transporters**: P-glycoprotein, BCRP, MRPs
- **Other**: SLC and ABC transporter families

### Carriers
Plasma proteins that bind and transport drugs:
- **Albumin**: Major drug carrier in blood
- **Alpha-1-acid glycoprotein**
- **Lipoproteins**
- **Specific binding proteins**: SHBG, CBG, etc.

## XML Data Structure

### Target Element Structure
```xml
<targets>
  <target>
    <id>BE0000001</id>
    <name>Prothrombin</name>
    <organism>Humans</organism>
    <actions>
      <action>inhibitor</action>
    </actions>
    <known-action>yes</known-action>
    <polypeptide id="P00734" source="Swiss-Prot">
      <name>Prothrombin</name>
      <general-function>Serine-type endopeptidase activity</general-function>
      <specific-function>Thrombin plays a role in...</specific-function>
      <gene-name>F2</gene-name>
      <organism>Homo sapiens</organism>
      <external-identifiers>
        <external-identifier>
          <resource>UniProtKB</resource>
          <identifier>P00734</identifier>
        </external-identifier>
      </external-identifiers>
      <amino-acid-sequence>MAHVRGLQLP...</amino-acid-sequence>
      <pfams>...</pfams>
      <go-classifiers>...</go-classifiers>
    </polypeptide>
  </target>
</targets>
```

## Extract Target Information

### Get Drug Targets
```python
from drugbank_downloader import get_drugbank_root

def get_drug_targets(drugbank_id):
    """Extract all targets for a drug"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            targets = []

            targets_elem = drug.find('db:targets', ns)
            if targets_elem is not None:
                for target in targets_elem.findall('db:target', ns):
                    target_data = extract_target_details(target, ns)
                    targets.append(target_data)

            return targets
    return []

def extract_target_details(target, ns):
    """Extract detailed target information"""
    target_data = {
        'id': target.find('db:id', ns).text,
        'name': target.find('db:name', ns).text,
        'organism': target.find('db:organism', ns).text,
        'known_action': target.find('db:known-action', ns).text,
    }

    # Extract actions
    actions_elem = target.find('db:actions', ns)
    if actions_elem is not None:
        actions = [action.text for action in actions_elem.findall('db:action', ns)]
        target_data['actions'] = actions

    # Extract polypeptide info
    polypeptide = target.find('db:polypeptide', ns)
    if polypeptide is not None:
        target_data['uniprot_id'] = polypeptide.get('id')
        target_data['gene_name'] = get_text_safe(polypeptide.find('db:gene-name', ns))
        target_data['general_function'] = get_text_safe(polypeptide.find('db:general-function', ns))
        target_data['specific_function'] = get_text_safe(polypeptide.find('db:specific-function', ns))

    return target_data

def get_text_safe(element):
    return element.text if element is not None else None
```

### Get All Protein Interactions
```python
def get_all_protein_interactions(drugbank_id):
    """Get targets, enzymes, transporters, and carriers for a drug"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            interactions = {
                'targets': extract_protein_list(drug.find('db:targets', ns), ns),
                'enzymes': extract_protein_list(drug.find('db:enzymes', ns), ns),
                'transporters': extract_protein_list(drug.find('db:transporters', ns), ns),
                'carriers': extract_protein_list(drug.find('db:carriers', ns), ns),
            }
            return interactions
    return None

def extract_protein_list(parent_elem, ns):
    """Extract list of proteins from parent element"""
    if parent_elem is None:
        return []

    proteins = []
    # Same structure for targets, enzymes, transporters, carriers
    for protein_elem in parent_elem:
        protein_data = extract_target_details(protein_elem, ns)
        proteins.append(protein_data)

    return proteins

# Usage
interactions = get_all_protein_interactions('DB00001')
print(f"Targets: {len(interactions['targets'])}")
print(f"Enzymes: {len(interactions['enzymes'])}")
print(f"Transporters: {len(interactions['transporters'])}")
print(f"Carriers: {len(interactions['carriers'])}")
```

## Build Target-Drug Networks

### Create Target-Drug Matrix
```python
import pandas as pd

def build_drug_target_matrix():
    """Build matrix of drugs vs targets"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drug_target_pairs = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        drug_name = drug.find('db:name', ns).text

        targets_elem = drug.find('db:targets', ns)
        if targets_elem is not None:
            for target in targets_elem.findall('db:target', ns):
                target_id = target.find('db:id', ns).text
                target_name = target.find('db:name', ns).text

                # Get UniProt ID if available
                polypeptide = target.find('db:polypeptide', ns)
                uniprot_id = polypeptide.get('id') if polypeptide is not None else None

                drug_target_pairs.append({
                    'drug_id': drug_id,
                    'drug_name': drug_name,
                    'target_id': target_id,
                    'target_name': target_name,
                    'uniprot_id': uniprot_id
                })

    df = pd.DataFrame(drug_target_pairs)
    return df

# Usage
dt_matrix = build_drug_target_matrix()
dt_matrix.to_csv('drug_target_matrix.csv', index=False)
```

### Find Drugs Targeting Specific Protein
```python
def find_drugs_for_target(target_name):
    """Find all drugs that target a specific protein"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    drugs_for_target = []
    target_name_lower = target_name.lower()

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text
        drug_name = drug.find('db:name', ns).text

        targets_elem = drug.find('db:targets', ns)
        if targets_elem is not None:
            for target in targets_elem.findall('db:target', ns):
                tgt_name = target.find('db:name', ns).text
                if target_name_lower in tgt_name.lower():
                    drugs_for_target.append({
                        'drug_id': drug_id,
                        'drug_name': drug_name,
                        'target_name': tgt_name
                    })
                    break  # Found match, move to next drug

    return drugs_for_target

# Example: Find drugs targeting kinases
kinase_drugs = find_drugs_for_target('kinase')
print(f"Found {len(kinase_drugs)} drugs targeting kinases")
```

### Find Drugs with Shared Targets
```python
def find_shared_targets(drug1_id, drug2_id):
    """Find common targets between two drugs"""
    targets1 = get_drug_targets(drug1_id)
    targets2 = get_drug_targets(drug2_id)

    # Compare by UniProt ID if available, otherwise by name
    targets1_ids = set()
    for t in targets1:
        if t.get('uniprot_id'):
            targets1_ids.add(t['uniprot_id'])
        else:
            targets1_ids.add(t['name'])

    targets2_ids = set()
    for t in targets2:
        if t.get('uniprot_id'):
            targets2_ids.add(t['uniprot_id'])
        else:
            targets2_ids.add(t['name'])

    shared = targets1_ids.intersection(targets2_ids)
    return list(shared)

# Usage for drug repurposing
shared = find_shared_targets('DB00001', 'DB00002')
print(f"Shared targets: {shared}")
```

## Pathway Analysis

### Extract Pathway Information
```python
def get_drug_pathways(drugbank_id):
    """Extract pathway information for a drug"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            pathways = []

            pathways_elem = drug.find('db:pathways', ns)
            if pathways_elem is not None:
                for pathway in pathways_elem.findall('db:pathway', ns):
                    pathway_data = {
                        'smpdb_id': pathway.find('db:smpdb-id', ns).text,
                        'name': pathway.find('db:name', ns).text,
                        'category': pathway.find('db:category', ns).text,
                    }

                    # Extract drugs in pathway
                    drugs_elem = pathway.find('db:drugs', ns)
                    if drugs_elem is not None:
                        pathway_drugs = []
                        for drug_elem in drugs_elem.findall('db:drug', ns):
                            pathway_drugs.append(drug_elem.find('db:drugbank-id', ns).text)
                        pathway_data['drugs'] = pathway_drugs

                    # Extract enzymes in pathway
                    enzymes_elem = pathway.find('db:enzymes', ns)
                    if enzymes_elem is not None:
                        pathway_enzymes = []
                        for enzyme in enzymes_elem.findall('db:uniprot-id', ns):
                            pathway_enzymes.append(enzyme.text)
                        pathway_data['enzymes'] = pathway_enzymes

                    pathways.append(pathway_data)

            return pathways
    return []
```

### Build Pathway Network
```python
def build_pathway_drug_network():
    """Build network of pathways and drugs"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    pathway_network = {}

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text

        pathways_elem = drug.find('db:pathways', ns)
        if pathways_elem is not None:
            for pathway in pathways_elem.findall('db:pathway', ns):
                pathway_id = pathway.find('db:smpdb-id', ns).text
                pathway_name = pathway.find('db:name', ns).text

                if pathway_id not in pathway_network:
                    pathway_network[pathway_id] = {
                        'name': pathway_name,
                        'drugs': []
                    }

                pathway_network[pathway_id]['drugs'].append(drug_id)

    return pathway_network
```

## Target-Based Drug Repurposing

### Find Drugs with Similar Target Profiles
```python
def find_similar_target_profiles(drugbank_id, min_shared_targets=2):
    """Find drugs with similar target profiles for repurposing"""
    reference_targets = get_drug_targets(drugbank_id)
    reference_target_ids = set(t.get('uniprot_id') or t['name'] for t in reference_targets)

    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    similar_drugs = []

    for drug in root.findall('db:drug', ns):
        drug_id = drug.find('db:drugbank-id[@primary="true"]', ns).text

        if drug_id == drugbank_id:
            continue

        drug_targets = get_drug_targets(drug_id)
        drug_target_ids = set(t.get('uniprot_id') or t['name'] for t in drug_targets)

        shared = reference_target_ids.intersection(drug_target_ids)

        if len(shared) >= min_shared_targets:
            drug_name = drug.find('db:name', ns).text
            indication = get_text_safe(drug.find('db:indication', ns))

            similar_drugs.append({
                'drug_id': drug_id,
                'drug_name': drug_name,
                'shared_targets': len(shared),
                'total_targets': len(drug_target_ids),
                'overlap_ratio': len(shared) / len(drug_target_ids) if drug_target_ids else 0,
                'indication': indication,
                'shared_target_names': list(shared)
            })

    # Sort by overlap ratio
    similar_drugs.sort(key=lambda x: x['overlap_ratio'], reverse=True)
    return similar_drugs

# Example: Find repurposing candidates
candidates = find_similar_target_profiles('DB00001', min_shared_targets=2)
for drug in candidates[:5]:
    print(f"{drug['drug_name']}: {drug['shared_targets']} shared targets")
```

### Polypharmacology Analysis
```python
def analyze_polypharmacology(drugbank_id):
    """Analyze on-target and off-target effects"""
    targets = get_drug_targets(drugbank_id)

    analysis = {
        'total_targets': len(targets),
        'known_action_targets': [],
        'unknown_action_targets': [],
        'target_classes': {},
        'organisms': {}
    }

    for target in targets:
        if target.get('known_action') == 'yes':
            analysis['known_action_targets'].append(target)
        else:
            analysis['unknown_action_targets'].append(target)

        # Count by organism
        organism = target.get('organism', 'Unknown')
        analysis['organisms'][organism] = analysis['organisms'].get(organism, 0) + 1

    return analysis

# Usage
poly_analysis = analyze_polypharmacology('DB00001')
print(f"Total targets: {poly_analysis['total_targets']}")
print(f"Known action: {len(poly_analysis['known_action_targets'])}")
print(f"Unknown action: {len(poly_analysis['unknown_action_targets'])}")
```

## Enzyme and Transporter Analysis

### CYP450 Interaction Analysis
```python
def analyze_cyp450_metabolism(drugbank_id):
    """Analyze CYP450 enzyme involvement"""
    interactions = get_all_protein_interactions(drugbank_id)
    enzymes = interactions['enzymes']

    cyp_enzymes = []
    for enzyme in enzymes:
        gene_name = enzyme.get('gene_name', '')
        if gene_name and gene_name.startswith('CYP'):
            cyp_enzymes.append({
                'gene': gene_name,
                'name': enzyme['name'],
                'actions': enzyme.get('actions', [])
            })

    return cyp_enzymes

# Check CYP involvement
cyp_data = analyze_cyp450_metabolism('DB00001')
for cyp in cyp_data:
    print(f"{cyp['gene']}: {cyp['actions']}")
```

### Transporter Substrate Analysis
```python
def analyze_transporter_substrates(drugbank_id):
    """Identify transporter involvement for ADME"""
    interactions = get_all_protein_interactions(drugbank_id)
    transporters = interactions['transporters']

    transporter_info = {
        'efflux': [],
        'uptake': [],
        'other': []
    }

    for transporter in transporters:
        name = transporter['name'].lower()
        gene = transporter.get('gene_name', '').upper()

        if 'p-glycoprotein' in name or gene == 'ABCB1':
            transporter_info['efflux'].append(transporter)
        elif 'oatp' in name or 'slco' in gene.lower():
            transporter_info['uptake'].append(transporter)
        else:
            transporter_info['other'].append(transporter)

    return transporter_info
```

## GO Term and Protein Function Analysis

### Extract GO Terms
```python
def get_target_go_terms(drugbank_id):
    """Extract Gene Ontology terms for drug targets"""
    root = get_drugbank_root()
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', ns):
        primary_id = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id is not None and primary_id.text == drugbank_id:
            go_terms = []

            targets_elem = drug.find('db:targets', ns)
            if targets_elem is not None:
                for target in targets_elem.findall('db:target', ns):
                    polypeptide = target.find('db:polypeptide', ns)
                    if polypeptide is not None:
                        go_classifiers = polypeptide.find('db:go-classifiers', ns)
                        if go_classifiers is not None:
                            for go_class in go_classifiers.findall('db:go-classifier', ns):
                                go_term = {
                                    'category': go_class.find('db:category', ns).text,
                                    'description': go_class.find('db:description', ns).text,
                                }
                                go_terms.append(go_term)

            return go_terms
    return []
```

## Best Practices

1. **UniProt Cross-Reference**: Use UniProt IDs for accurate protein matching across databases
2. **Action Classification**: Pay attention to action types (inhibitor, agonist, antagonist, etc.)
3. **Known vs Unknown**: Distinguish between validated targets and predicted/unknown interactions
4. **Organism Specificity**: Consider organism when analyzing target data
5. **Polypharmacology**: Account for multiple targets when predicting drug effects
6. **Pathway Context**: Use pathway data to understand systemic effects
7. **CYP450 Profiling**: Essential for predicting drug-drug interactions
8. **Transporter Analysis**: Critical for understanding bioavailability and tissue distribution
