---
title: "Pytdc"
description: "Therapeutics Data Commons. AI-ready drug discovery datasets (ADME, toxicity, DTI), benchmarks, scaffold splits, molecular oracles, for therapeutic ML and pharmacological prediction."
category: "other"
source: "community"
author: "Community"
tags: ["pytdc"]
date: 2026-03-20
---

# PyTDC (Therapeutics Data Commons)

## Overview

PyTDC is an open-science platform providing AI-ready datasets and benchmarks for drug discovery and development. Access curated datasets spanning the entire therapeutics pipeline with standardized evaluation metrics and meaningful data splits, organized into three categories: single-instance prediction (molecular/protein properties), multi-instance prediction (drug-target interactions, DDI), and generation (molecule generation, retrosynthesis).

## When to Use This Skill

This skill should be used when:
- Working with drug discovery or therapeutic ML datasets
- Benchmarking machine learning models on standardized pharmaceutical tasks
- Predicting molecular properties (ADME, toxicity, bioactivity)
- Predicting drug-target or drug-drug interactions
- Generating novel molecules with desired properties
- Accessing curated datasets with proper train/test splits (scaffold, cold-split)
- Using molecular oracles for property optimization

## Installation & Setup

Install PyTDC using pip:

```bash
uv pip install PyTDC
```

To upgrade to the latest version:

```bash
uv pip install PyTDC --upgrade
```

Core dependencies (automatically installed):
- numpy, pandas, tqdm, seaborn, scikit_learn, fuzzywuzzy

Additional packages are installed automatically as needed for specific features.

## Quick Start

The basic pattern for accessing any TDC dataset follows this structure:

```python
from tdc.<problem> import <Task>
data = <Task>(name='<Dataset>')
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
df = data.get_data(format='df')
```

Where:
- `<problem>`: One of `single_pred`, `multi_pred`, or `generation`
- `<Task>`: Specific task category (e.g., ADME, DTI, MolGen)
- `<Dataset>`: Dataset name within that task

**Example - Loading ADME data:**

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold')
# Returns dict with 'train', 'valid', 'test' DataFrames
```

## Single-Instance Prediction Tasks

Single-instance prediction involves forecasting properties of individual biomedical entities (molecules, proteins, etc.).

### Available Task Categories

#### 1. ADME (Absorption, Distribution, Metabolism, Excretion)

Predict pharmacokinetic properties of drug molecules.

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')  # Intestinal permeability
# Other datasets: HIA_Hou, Bioavailability_Ma, Lipophilicity_AstraZeneca, etc.
```

**Common ADME datasets:**
- Caco2 - Intestinal permeability
- HIA - Human intestinal absorption
- Bioavailability - Oral bioavailability
- Lipophilicity - Octanol-water partition coefficient
- Solubility - Aqueous solubility
- BBB - Blood-brain barrier penetration
- CYP - Cytochrome P450 metabolism

#### 2. Toxicity (Tox)

Predict toxicity and adverse effects of compounds.

```python
from tdc.single_pred import Tox
data = Tox(name='hERG')  # Cardiotoxicity
# Other datasets: AMES, DILI, Carcinogens_Lagunin, etc.
```

**Common toxicity datasets:**
- hERG - Cardiac toxicity
- AMES - Mutagenicity
- DILI - Drug-induced liver injury
- Carcinogens - Carcinogenicity
- ClinTox - Clinical trial toxicity

#### 3. HTS (High-Throughput Screening)

Bioactivity predictions from screening data.

```python
from tdc.single_pred import HTS
data = HTS(name='SARSCoV2_Vitro_Touret')
```

#### 4. QM (Quantum Mechanics)

Quantum mechanical properties of molecules.

```python
from tdc.single_pred import QM
data = QM(name='QM7')
```

#### 5. Other Single Prediction Tasks

- **Yields**: Chemical reaction yield prediction
- **Epitope**: Epitope prediction for biologics
- **Develop**: Development-stage predictions
- **CRISPROutcome**: Gene editing outcome prediction

### Data Format

Single prediction datasets typically return DataFrames with columns:
- `Drug_ID` or `Compound_ID`: Unique identifier
- `Drug` or `X`: SMILES string or molecular representation
- `Y`: Target label (continuous or binary)

## Multi-Instance Prediction Tasks

Multi-instance prediction involves forecasting properties of interactions between multiple biomedical entities.

### Available Task Categories

#### 1. DTI (Drug-Target Interaction)

Predict binding affinity between drugs and protein targets.

```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split()
```

**Available datasets:**
- BindingDB_Kd - Dissociation constant (52,284 pairs)
- BindingDB_IC50 - Half-maximal inhibitory concentration (991,486 pairs)
- BindingDB_Ki - Inhibition constant (375,032 pairs)
- DAVIS, KIBA - Kinase binding datasets

**Data format:** Drug_ID, Target_ID, Drug (SMILES), Target (sequence), Y (binding affinity)

#### 2. DDI (Drug-Drug Interaction)

Predict interactions between drug pairs.

```python
from tdc.multi_pred import DDI
data = DDI(name='DrugBank')
split = data.get_split()
```

Multi-class classification task predicting interaction types. Dataset contains 191,808 DDI pairs with 1,706 drugs.

#### 3. PPI (Protein-Protein Interaction)

Predict protein-protein interactions.

```python
from tdc.multi_pred import PPI
data = PPI(name='HuRI')
```

#### 4. Other Multi-Prediction Tasks

- **GDA**: Gene-disease associations
- **DrugRes**: Drug resistance prediction
- **DrugSyn**: Drug synergy prediction
- **PeptideMHC**: Peptide-MHC binding
- **AntibodyAff**: Antibody affinity prediction
- **MTI**: miRNA-target interactions
- **Catalyst**: Catalyst prediction
- **TrialOutcome**: Clinical trial outcome prediction

## Generation Tasks

Generation tasks involve creating novel biomedical entities with desired properties.

### 1. Molecular Generation (MolGen)

Generate diverse, novel molecules with desirable chemical properties.

```python
from tdc.generation import MolGen
data = MolGen(name='ChEMBL_V29')
split = data.get_split()
```

Use with oracles to optimize for specific properties:

```python
from tdc import Oracle
oracle = Oracle(name='GSK3B')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')  # Evaluate SMILES
```

See `references/oracles.md` for all available oracle functions.

### 2. Retrosynthesis (RetroSyn)

Predict reactants needed to synthesize a target molecule.

```python
from tdc.generation import RetroSyn
data = RetroSyn(name='USPTO')
split = data.get_split()
```

Dataset contains 1,939,253 reactions from USPTO database.

### 3. Paired Molecule Generation

Generate molecule pairs (e.g., prodrug-drug pairs).

```python
from tdc.generation import PairMolGen
data = PairMolGen(name='Prodrug')
```

For detailed oracle documentation and molecular generation workflows, refer to `references/oracles.md` and `scripts/molecular_generation.py`.

## Benchmark Groups

Benchmark groups provide curated collections of related datasets for systematic model evaluation.

### ADMET Benchmark Group

```python
from tdc.benchmark_group import admet_group
group = admet_group(path='data/')

# Get benchmark datasets
benchmark = group.get('Caco2_Wang')
predictions = {}

for seed in [1, 2, 3, 4, 5]:
    train, valid = benchmark['train'], benchmark['valid']
    # Train model here
    predictions[seed] = model.predict(benchmark['test'])

# Evaluate with required 5 seeds
results = group.evaluate(predictions)
```

**ADMET Group includes 22 datasets** covering absorption, distribution, metabolism, excretion, and toxicity.

### Other Benchmark Groups

Available benchmark groups include collections for:
- ADMET properties
- Drug-target interactions
- Drug combination prediction
- And more specialized therapeutic tasks

For benchmark evaluation workflows, see `scripts/benchmark_evaluation.py`.

## Data Functions

TDC provides comprehensive data processing utilities organized into four categories.

### 1. Dataset Splits

Retrieve train/validation/test partitions with various strategies:

```python
# Scaffold split (default for most tasks)
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])

# Random split
split = data.get_split(method='random', seed=42, frac=[0.8, 0.1, 0.1])

# Cold split (for DTI/DDI tasks)
split = data.get_split(method='cold_drug', seed=1)  # Unseen drugs in test
split = data.get_split(method='cold_target', seed=1)  # Unseen targets in test
```

**Available split strategies:**
- `random`: Random shuffling
- `scaffold`: Scaffold-based (for chemical diversity)
- `cold_drug`, `cold_target`, `cold_drug_target`: For DTI tasks
- `temporal`: Time-based splits for temporal datasets

### 2. Model Evaluation

Use standardized metrics for evaluation:

```python
from tdc import Evaluator

# For binary classification
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred)

# For regression
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

**Available metrics:** ROC-AUC, PR-AUC, F1, Accuracy, RMSE, MAE, R2, Spearman, Pearson, and more.

### 3. Data Processing

TDC provides 11 key processing utilities:

```python
from tdc.chem_utils import MolConvert

# Molecule format conversion
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

**Processing utilities include:**
- Molecule format conversion (SMILES, SELFIES, PyG, DGL, ECFP, etc.)
- Molecule filters (PAINS, drug-likeness)
- Label binarization and unit conversion
- Data balancing (over/under-sampling)
- Negative sampling for pair data
- Graph transformation
- Entity retrieval (CID to SMILES, UniProt to sequence)

For comprehensive utilities documentation, see `references/utilities.md`.

### 4. Molecule Generation Oracles

TDC provides 17+ oracle functions for molecular optimization:

```python
from tdc import Oracle

# Single oracle
oracle = Oracle(name='DRD2')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# Multiple oracles
oracle = Oracle(name='JNK3')
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

For complete oracle documentation, see `references/oracles.md`.

## Advanced Features

### Retrieve Available Datasets

```python
from tdc.utils import retrieve_dataset_names

# Get all ADME datasets
adme_datasets = retrieve_dataset_names('ADME')

# Get all DTI datasets
dti_datasets = retrieve_dataset_names('DTI')
```

### Label Transformations

```python
# Get label mapping
label_map = data.get_label_map(name='DrugBank')

# Convert labels
from tdc.chem_utils import label_transform
transformed = label_transform(y, from_unit='nM', to_unit='p')
```

### Database Queries

```python
from tdc.utils import cid2smiles, uniprot2seq

# Convert PubChem CID to SMILES
smiles = cid2smiles(2244)

# Convert UniProt ID to amino acid sequence
sequence = uniprot2seq('P12345')
```

## Common Workflows

### Workflow 1: Train a Single Prediction Model

See `scripts/load_and_split_data.py` for a complete example:

```python
from tdc.single_pred import ADME
from tdc import Evaluator

# Load data
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold', seed=42)

train, valid, test = split['train'], split['valid'], split['test']

# Train model (user implements)
# model.fit(train['Drug'], train['Y'])

# Evaluate
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### Workflow 2: Benchmark Evaluation

See `scripts/benchmark_evaluation.py` for a complete example with multiple seeds and proper evaluation protocol.

### Workflow 3: Molecular Generation with Oracles

See `scripts/molecular_generation.py` for an example of goal-directed generation using oracle functions.

## Resources

This skill includes bundled resources for common TDC workflows:

### scripts/

- `load_and_split_data.py`: Template for loading and splitting TDC datasets with various strategies
- `benchmark_evaluation.py`: Template for running benchmark group evaluations with proper 5-seed protocol
- `molecular_generation.py`: Template for molecular generation using oracle functions

### references/

- `datasets.md`: Comprehensive catalog of all available datasets organized by task type
- `oracles.md`: Complete documentation of all 17+ molecule generation oracles
- `utilities.md`: Detailed guide to data processing, splitting, and evaluation utilities

## Additional Resources

- **Official Website**: https://tdcommons.ai
- **Documentation**: https://tdc.readthedocs.io
- **GitHub**: https://github.com/mims-harvard/TDC
- **Paper**: NeurIPS 2021 - "Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development"

---

## Reference: Datasets

# TDC Datasets Comprehensive Catalog

This document provides a comprehensive catalog of all available datasets in the Therapeutics Data Commons, organized by task category.

## Single-Instance Prediction Datasets

### ADME (Absorption, Distribution, Metabolism, Excretion)

**Absorption:**
- `Caco2_Wang` - Caco-2 cell permeability (906 compounds)
- `Caco2_AstraZeneca` - Caco-2 permeability from AstraZeneca (700 compounds)
- `HIA_Hou` - Human intestinal absorption (578 compounds)
- `Pgp_Broccatelli` - P-glycoprotein inhibition (1,212 compounds)
- `Bioavailability_Ma` - Oral bioavailability (640 compounds)
- `F20_edrug3d` - Oral bioavailability F>=20% (1,017 compounds)
- `F30_edrug3d` - Oral bioavailability F>=30% (1,017 compounds)

**Distribution:**
- `BBB_Martins` - Blood-brain barrier penetration (1,975 compounds)
- `PPBR_AZ` - Plasma protein binding rate (1,797 compounds)
- `VDss_Lombardo` - Volume of distribution at steady state (1,130 compounds)

**Metabolism:**
- `CYP2C19_Veith` - CYP2C19 inhibition (12,665 compounds)
- `CYP2D6_Veith` - CYP2D6 inhibition (13,130 compounds)
- `CYP3A4_Veith` - CYP3A4 inhibition (12,328 compounds)
- `CYP1A2_Veith` - CYP1A2 inhibition (12,579 compounds)
- `CYP2C9_Veith` - CYP2C9 inhibition (12,092 compounds)
- `CYP2C9_Substrate_CarbonMangels` - CYP2C9 substrate (666 compounds)
- `CYP2D6_Substrate_CarbonMangels` - CYP2D6 substrate (664 compounds)
- `CYP3A4_Substrate_CarbonMangels` - CYP3A4 substrate (667 compounds)

**Excretion:**
- `Half_Life_Obach` - Half-life (667 compounds)
- `Clearance_Hepatocyte_AZ` - Hepatocyte clearance (1,020 compounds)
- `Clearance_Microsome_AZ` - Microsome clearance (1,102 compounds)

**Solubility & Lipophilicity:**
- `Solubility_AqSolDB` - Aqueous solubility (9,982 compounds)
- `Lipophilicity_AstraZeneca` - Lipophilicity (logD) (4,200 compounds)
- `HydrationFreeEnergy_FreeSolv` - Hydration free energy (642 compounds)

### Toxicity

**Organ Toxicity:**
- `hERG` - hERG channel inhibition/cardiotoxicity (648 compounds)
- `hERG_Karim` - hERG blockers extended dataset (13,445 compounds)
- `DILI` - Drug-induced liver injury (475 compounds)
- `Skin_Reaction` - Skin reaction (404 compounds)
- `Carcinogens_Lagunin` - Carcinogenicity (278 compounds)
- `Respiratory_Toxicity` - Respiratory toxicity (278 compounds)

**General Toxicity:**
- `AMES` - Ames mutagenicity (7,255 compounds)
- `LD50_Zhu` - Acute toxicity LD50 (7,385 compounds)
- `ClinTox` - Clinical trial toxicity (1,478 compounds)
- `SkinSensitization` - Skin sensitization (278 compounds)
- `EyeCorrosion` - Eye corrosion (278 compounds)
- `EyeIrritation` - Eye irritation (278 compounds)

**Environmental Toxicity:**
- `Tox21-AhR` - Nuclear receptor signaling (8,169 compounds)
- `Tox21-AR` - Androgen receptor (9,362 compounds)
- `Tox21-AR-LBD` - Androgen receptor ligand binding (8,343 compounds)
- `Tox21-ARE` - Antioxidant response element (6,475 compounds)
- `Tox21-aromatase` - Aromatase inhibition (6,733 compounds)
- `Tox21-ATAD5` - DNA damage (8,163 compounds)
- `Tox21-ER` - Estrogen receptor (7,257 compounds)
- `Tox21-ER-LBD` - Estrogen receptor ligand binding (8,163 compounds)
- `Tox21-HSE` - Heat shock response (8,162 compounds)
- `Tox21-MMP` - Mitochondrial membrane potential (7,394 compounds)
- `Tox21-p53` - p53 pathway (8,163 compounds)
- `Tox21-PPAR-gamma` - PPAR gamma activation (7,396 compounds)

### HTS (High-Throughput Screening)

**SARS-CoV-2:**
- `SARSCoV2_Vitro_Touret` - In vitro antiviral activity (1,484 compounds)
- `SARSCoV2_3CLPro_Diamond` - 3CL protease inhibition (879 compounds)
- `SARSCoV2_Vitro_AlabdulKareem` - In vitro screening (5,953 compounds)

**Other Targets:**
- `Orexin1_Receptor_Butkiewicz` - Orexin receptor screening (4,675 compounds)
- `M1_Receptor_Agonist_Butkiewicz` - M1 receptor agonist (1,700 compounds)
- `M1_Receptor_Antagonist_Butkiewicz` - M1 receptor antagonist (1,700 compounds)
- `HIV_Butkiewicz` - HIV inhibition (40,000+ compounds)
- `ToxCast` - Environmental chemical screening (8,597 compounds)

### QM (Quantum Mechanics)

- `QM7` - Quantum mechanics properties (7,160 molecules)
- `QM8` - Electronic spectra and excited states (21,786 molecules)
- `QM9` - Geometric, energetic, electronic, thermodynamic properties (133,885 molecules)

### Yields

- `Buchwald-Hartwig` - Reaction yield prediction (3,955 reactions)
- `USPTO_Yields` - Yield prediction from USPTO (853,879 reactions)

### Epitope

- `IEDBpep-DiseaseBinder` - Disease-associated epitope binding (6,080 peptides)
- `IEDBpep-NonBinder` - Non-binding peptides (24,320 peptides)

### Develop (Development)

- `Manufacturing` - Manufacturing success prediction
- `Formulation` - Formulation stability

### CRISPROutcome

- `CRISPROutcome_Doench` - Gene editing efficiency prediction (5,310 guide RNAs)

## Multi-Instance Prediction Datasets

### DTI (Drug-Target Interaction)

**Binding Affinity:**
- `BindingDB_Kd` - Dissociation constant (52,284 pairs, 10,665 drugs, 1,413 proteins)
- `BindingDB_IC50` - Half-maximal inhibitory concentration (991,486 pairs, 549,205 drugs, 5,078 proteins)
- `BindingDB_Ki` - Inhibition constant (375,032 pairs, 174,662 drugs, 3,070 proteins)

**Kinase Binding:**
- `DAVIS` - Davis kinase binding dataset (30,056 pairs, 68 drugs, 442 proteins)
- `KIBA` - KIBA kinase binding dataset (118,254 pairs, 2,111 drugs, 229 proteins)

**Binary Interaction:**
- `BindingDB_Patent` - Patent-derived DTI (8,503 pairs)
- `BindingDB_Approval` - FDA-approved drug DTI (1,649 pairs)

### DDI (Drug-Drug Interaction)

- `DrugBank` - Drug-drug interactions (191,808 pairs, 1,706 drugs)
- `TWOSIDES` - Side effect-based DDI (4,649,441 pairs, 645 drugs)

### PPI (Protein-Protein Interaction)

- `HuRI` - Human reference protein interactome (52,569 interactions)
- `STRING` - Protein functional associations (19,247 interactions)

### GDA (Gene-Disease Association)

- `DisGeNET` - Gene-disease associations (81,746 pairs)
- `PrimeKG_GDA` - Gene-disease from PrimeKG knowledge graph

### DrugRes (Drug Response/Resistance)

- `GDSC1` - Genomics of Drug Sensitivity in Cancer v1 (178,000 pairs)
- `GDSC2` - Genomics of Drug Sensitivity in Cancer v2 (125,000 pairs)

### DrugSyn (Drug Synergy)

- `DrugComb` - Drug combination synergy (345,502 combinations)
- `DrugCombDB` - Drug combination database (448,555 combinations)
- `OncoPolyPharmacology` - Oncology drug combinations (22,737 combinations)

### PeptideMHC

- `MHC1_NetMHCpan` - MHC class I binding (184,983 pairs)
- `MHC2_NetMHCIIpan` - MHC class II binding (134,281 pairs)

### AntibodyAff (Antibody Affinity)

- `Protein_SAbDab` - Antibody-antigen affinity (1,500+ pairs)

### MTI (miRNA-Target Interaction)

- `miRTarBase` - Experimentally validated miRNA-target interactions (380,639 pairs)

### Catalyst

- `USPTO_Catalyst` - Catalyst prediction for reactions (11,000+ reactions)

### TrialOutcome

- `TrialOutcome_WuXi` - Clinical trial outcome prediction (3,769 trials)

## Generation Datasets

### MolGen (Molecular Generation)

- `ChEMBL_V29` - Drug-like molecules from ChEMBL (1,941,410 molecules)
- `ZINC` - ZINC database subset (100,000+ molecules)
- `GuacaMol` - Goal-directed benchmark molecules
- `Moses` - Molecular sets benchmark (1,936,962 molecules)

### RetroSyn (Retrosynthesis)

- `USPTO` - Retrosynthesis from USPTO patents (1,939,253 reactions)
- `USPTO-50K` - Curated USPTO subset (50,000 reactions)

### PairMolGen (Paired Molecule Generation)

- `Prodrug` - Prodrug to drug transformations (1,000+ pairs)
- `Metabolite` - Drug to metabolite transformations

## Using retrieve_dataset_names

To programmatically access all available datasets for a specific task:

```python
from tdc.utils import retrieve_dataset_names

# Get all datasets for a specific task
adme_datasets = retrieve_dataset_names('ADME')
tox_datasets = retrieve_dataset_names('Tox')
dti_datasets = retrieve_dataset_names('DTI')
hts_datasets = retrieve_dataset_names('HTS')
```

## Dataset Statistics

Access dataset statistics directly:

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')

# Print basic statistics
data.print_stats()

# Get label distribution
data.label_distribution()
```

## Loading Datasets

All datasets follow the same loading pattern:

```python
from tdc.<problem_type> import <TaskType>
data = <TaskType>(name='<DatasetName>')

# Get full dataset
df = data.get_data(format='df')  # or 'dict', 'DeepPurpose', etc.

# Get train/valid/test split
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
```

## Notes

- Dataset sizes and statistics are approximate and may be updated
- New datasets are regularly added to TDC
- Some datasets may require additional dependencies
- Check the official TDC website for the most up-to-date dataset list: https://tdcommons.ai/overview/

---

## Reference: Oracles

# TDC Molecule Generation Oracles

Oracles are functions that evaluate the quality of generated molecules across specific dimensions. TDC provides 17+ oracle functions for molecular optimization tasks in de novo drug design.

## Overview

Oracles measure molecular properties and serve two main purposes:

1. **Goal-Directed Generation**: Optimize molecules to maximize/minimize specific properties
2. **Distribution Learning**: Evaluate whether generated molecules match desired property distributions

## Using Oracles

### Basic Usage

```python
from tdc import Oracle

# Initialize oracle
oracle = Oracle(name='GSK3B')

# Evaluate single molecule (SMILES string)
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# Evaluate multiple molecules
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

### Oracle Categories

TDC oracles are organized into several categories based on the molecular property being evaluated.

## Biochemical Oracles

Predict binding affinity or activity against biological targets.

### Target-Specific Oracles

**DRD2 - Dopamine Receptor D2**
```python
oracle = Oracle(name='DRD2')
score = oracle(smiles)
```
- Measures binding affinity to DRD2 receptor
- Important for neurological and psychiatric drug development
- Higher scores indicate stronger binding

**GSK3B - Glycogen Synthase Kinase-3 Beta**
```python
oracle = Oracle(name='GSK3B')
score = oracle(smiles)
```
- Predicts GSK3β inhibition
- Relevant for Alzheimer's, diabetes, and cancer research
- Higher scores indicate better inhibition

**JNK3 - c-Jun N-terminal Kinase 3**
```python
oracle = Oracle(name='JNK3')
score = oracle(smiles)
```
- Measures JNK3 kinase inhibition
- Target for neurodegenerative diseases
- Higher scores indicate stronger inhibition

**5HT2A - Serotonin 2A Receptor**
```python
oracle = Oracle(name='5HT2A')
score = oracle(smiles)
```
- Predicts serotonin receptor binding
- Important for psychiatric medications
- Higher scores indicate stronger binding

**ACE - Angiotensin-Converting Enzyme**
```python
oracle = Oracle(name='ACE')
score = oracle(smiles)
```
- Measures ACE inhibition
- Target for hypertension treatment
- Higher scores indicate better inhibition

**MAPK - Mitogen-Activated Protein Kinase**
```python
oracle = Oracle(name='MAPK')
score = oracle(smiles)
```
- Predicts MAPK inhibition
- Target for cancer and inflammatory diseases

**CDK - Cyclin-Dependent Kinase**
```python
oracle = Oracle(name='CDK')
score = oracle(smiles)
```
- Measures CDK inhibition
- Important for cancer drug development

**P38 - p38 MAP Kinase**
```python
oracle = Oracle(name='P38')
score = oracle(smiles)
```
- Predicts p38 MAPK inhibition
- Target for inflammatory diseases

**PARP1 - Poly (ADP-ribose) Polymerase 1**
```python
oracle = Oracle(name='PARP1')
score = oracle(smiles)
```
- Measures PARP1 inhibition
- Target for cancer treatment (DNA repair mechanism)

**PIK3CA - Phosphatidylinositol-4,5-Bisphosphate 3-Kinase**
```python
oracle = Oracle(name='PIK3CA')
score = oracle(smiles)
```
- Predicts PIK3CA inhibition
- Important target in oncology

## Physicochemical Oracles

Evaluate drug-like properties and ADME characteristics.

### Drug-Likeness Oracles

**QED - Quantitative Estimate of Drug-likeness**
```python
oracle = Oracle(name='QED')
score = oracle(smiles)
```
- Combines multiple physicochemical properties
- Score ranges from 0 (non-drug-like) to 1 (drug-like)
- Based on Bickerton et al. criteria

**Lipinski - Rule of Five**
```python
oracle = Oracle(name='Lipinski')
score = oracle(smiles)
```
- Number of Lipinski rule violations
- Rules: MW ≤ 500, logP ≤ 5, HBD ≤ 5, HBA ≤ 10
- Score of 0 means fully compliant

### Molecular Properties

**SA - Synthetic Accessibility**
```python
oracle = Oracle(name='SA')
score = oracle(smiles)
```
- Estimates ease of synthesis
- Score ranges from 1 (easy) to 10 (difficult)
- Lower scores indicate easier synthesis

**LogP - Octanol-Water Partition Coefficient**
```python
oracle = Oracle(name='LogP')
score = oracle(smiles)
```
- Measures lipophilicity
- Important for membrane permeability
- Typical drug-like range: 0-5

**MW - Molecular Weight**
```python
oracle = Oracle(name='MW')
score = oracle(smiles)
```
- Returns molecular weight in Daltons
- Drug-like range typically 150-500 Da

## Composite Oracles

Combine multiple properties for multi-objective optimization.

**Isomer Meta**
```python
oracle = Oracle(name='Isomer_Meta')
score = oracle(smiles)
```
- Evaluates specific isomeric properties
- Used for stereochemistry optimization

**Median Molecules**
```python
oracle = Oracle(name='Median1', 'Median2')
score = oracle(smiles)
```
- Tests ability to generate molecules with median properties
- Useful for distribution learning benchmarks

**Rediscovery**
```python
oracle = Oracle(name='Rediscovery')
score = oracle(smiles)
```
- Measures similarity to known reference molecules
- Tests ability to regenerate existing drugs

**Similarity**
```python
oracle = Oracle(name='Similarity')
score = oracle(smiles)
```
- Computes structural similarity to target molecules
- Based on molecular fingerprints (typically Tanimoto similarity)

**Uniqueness**
```python
oracle = Oracle(name='Uniqueness')
scores = oracle(smiles_list)
```
- Measures diversity in generated molecule set
- Returns fraction of unique molecules

**Novelty**
```python
oracle = Oracle(name='Novelty')
scores = oracle(smiles_list, training_set)
```
- Measures how different generated molecules are from training set
- Higher scores indicate more novel structures

## Specialized Oracles

**ASKCOS - Retrosynthesis Scoring**
```python
oracle = Oracle(name='ASKCOS')
score = oracle(smiles)
```
- Evaluates synthetic feasibility using retrosynthesis
- Requires ASKCOS backend (IBM RXN)
- Scores based on retrosynthetic route availability

**Docking Score**
```python
oracle = Oracle(name='Docking')
score = oracle(smiles)
```
- Molecular docking score against target protein
- Requires protein structure and docking software
- Lower scores typically indicate better binding

**Vina - AutoDock Vina Score**
```python
oracle = Oracle(name='Vina')
score = oracle(smiles)
```
- Uses AutoDock Vina for protein-ligand docking
- Predicts binding affinity in kcal/mol
- More negative scores indicate stronger binding

## Multi-Objective Optimization

Combine multiple oracles for multi-property optimization:

```python
from tdc import Oracle

# Initialize multiple oracles
qed_oracle = Oracle(name='QED')
sa_oracle = Oracle(name='SA')
drd2_oracle = Oracle(name='DRD2')

# Define custom scoring function
def multi_objective_score(smiles):
    qed = qed_oracle(smiles)
    sa = 1 / (1 + sa_oracle(smiles))  # Invert SA (lower is better)
    drd2 = drd2_oracle(smiles)

    # Weighted combination
    return 0.3 * qed + 0.3 * sa + 0.4 * drd2

# Evaluate molecule
score = multi_objective_score('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

## Oracle Performance Considerations

### Speed
- **Fast**: QED, SA, LogP, MW, Lipinski (rule-based calculations)
- **Medium**: Target-specific ML models (DRD2, GSK3B, etc.)
- **Slow**: Docking-based oracles (Vina, ASKCOS)

### Reliability
- Oracles are ML models trained on specific datasets
- May not generalize to all chemical spaces
- Use multiple oracles to validate results

### Batch Processing
```python
# Efficient batch evaluation
oracle = Oracle(name='GSK3B')
smiles_list = ['SMILES1', 'SMILES2', ..., 'SMILES1000']
scores = oracle(smiles_list)  # Faster than individual calls
```

## Common Workflows

### Goal-Directed Generation
```python
from tdc import Oracle
from tdc.generation import MolGen

# Load training data
data = MolGen(name='ChEMBL_V29')
train_smiles = data.get_data()['Drug'].tolist()

# Initialize oracle
oracle = Oracle(name='GSK3B')

# Generate molecules (user implements generative model)
# generated_smiles = generator.generate(n=1000)

# Evaluate generated molecules
scores = oracle(generated_smiles)
best_molecules = [(s, score) for s, score in zip(generated_smiles, scores)]
best_molecules.sort(key=lambda x: x[1], reverse=True)

print(f"Top 10 molecules:")
for smiles, score in best_molecules[:10]:
    print(f"{smiles}: {score:.3f}")
```

### Distribution Learning
```python
from tdc import Oracle
import numpy as np

# Initialize oracle
oracle = Oracle(name='QED')

# Evaluate training set
train_scores = oracle(train_smiles)
train_mean = np.mean(train_scores)
train_std = np.std(train_scores)

# Evaluate generated set
gen_scores = oracle(generated_smiles)
gen_mean = np.mean(gen_scores)
gen_std = np.std(gen_scores)

# Compare distributions
print(f"Training: μ={train_mean:.3f}, σ={train_std:.3f}")
print(f"Generated: μ={gen_mean:.3f}, σ={gen_std:.3f}")
```

## Integration with TDC Benchmarks

```python
from tdc.generation import MolGen

# Use with GuacaMol benchmark
data = MolGen(name='GuacaMol')

# Oracles are automatically integrated
# Each GuacaMol task has associated oracle
benchmark_results = data.evaluate_guacamol(
    generated_molecules=your_molecules,
    oracle_name='GSK3B'
)
```

## Notes

- Oracle scores are predictions, not experimental measurements
- Always validate top candidates experimentally
- Different oracles may have different score ranges and interpretations
- Some oracles require additional dependencies or API access
- Check oracle documentation for specific details: https://tdcommons.ai/functions/oracles/

## Adding Custom Oracles

To create custom oracle functions:

```python
class CustomOracle:
    def __init__(self):
        # Initialize your model/method
        pass

    def __call__(self, smiles):
        # Implement your scoring logic
        # Return score or list of scores
        pass

# Use like built-in oracles
custom_oracle = CustomOracle()
score = custom_oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

## References

- TDC Oracles Documentation: https://tdcommons.ai/functions/oracles/
- GuacaMol Paper: "GuacaMol: Benchmarking Models for de Novo Molecular Design"
- MOSES Paper: "Molecular Sets (MOSES): A Benchmarking Platform for Molecular Generation Models"

---

## Reference: Utilities

# TDC Utilities and Data Functions

This document provides comprehensive documentation for TDC's data processing, evaluation, and utility functions.

## Overview

TDC provides utilities organized into four main categories:
1. **Dataset Splits** - Train/validation/test partitioning strategies
2. **Model Evaluation** - Standardized performance metrics
3. **Data Processing** - Molecule conversion, filtering, and transformation
4. **Entity Retrieval** - Database queries and conversions

## 1. Dataset Splits

Dataset splitting is crucial for evaluating model generalization. TDC provides multiple splitting strategies designed for therapeutic ML.

### Basic Split Usage

```python
from tdc.single_pred import ADME

data = ADME(name='Caco2_Wang')

# Get split with default parameters
split = data.get_split()
# Returns: {'train': DataFrame, 'valid': DataFrame, 'test': DataFrame}

# Customize split parameters
split = data.get_split(
    method='scaffold',
    seed=42,
    frac=[0.7, 0.1, 0.2]
)
```

### Split Methods

#### Random Split
Random shuffling of data - suitable for general ML tasks.

```python
split = data.get_split(method='random', seed=1)
```

**When to use:**
- Baseline model evaluation
- When chemical/temporal structure is not important
- Quick prototyping

**Not recommended for:**
- Realistic drug discovery scenarios
- Evaluating generalization to new chemical matter

#### Scaffold Split
Splits based on molecular scaffolds (Bemis-Murcko scaffolds) - ensures test molecules are structurally distinct from training.

```python
split = data.get_split(method='scaffold', seed=1)
```

**When to use:**
- Default for most single prediction tasks
- Evaluating generalization to new chemical series
- Realistic drug discovery scenarios

**How it works:**
1. Extract Bemis-Murcko scaffold from each molecule
2. Group molecules by scaffold
3. Assign scaffolds to train/valid/test sets
4. Ensures test molecules have unseen scaffolds

#### Cold Splits (DTI/DDI Tasks)
For multi-instance prediction, cold splits ensure test set contains unseen drugs, targets, or both.

**Cold Drug Split:**
```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split(method='cold_drug', seed=1)
```
- Test set contains drugs not seen during training
- Evaluates generalization to new compounds

**Cold Target Split:**
```python
split = data.get_split(method='cold_target', seed=1)
```
- Test set contains targets not seen during training
- Evaluates generalization to new proteins

**Cold Drug-Target Split:**
```python
split = data.get_split(method='cold_drug_target', seed=1)
```
- Test set contains novel drug-target pairs
- Most challenging evaluation scenario

#### Temporal Split
For datasets with temporal information - ensures test data is from later time points.

```python
split = data.get_split(method='temporal', seed=1)
```

**When to use:**
- Datasets with time stamps
- Simulating prospective prediction
- Clinical trial outcome prediction

### Custom Split Fractions

```python
# 80% train, 10% valid, 10% test
split = data.get_split(method='scaffold', frac=[0.8, 0.1, 0.1])

# 70% train, 15% valid, 15% test
split = data.get_split(method='scaffold', frac=[0.7, 0.15, 0.15])
```

### Stratified Splits

For classification tasks with imbalanced labels:

```python
split = data.get_split(method='scaffold', stratified=True)
```

Maintains label distribution across train/valid/test sets.

## 2. Model Evaluation

TDC provides standardized evaluation metrics for different task types.

### Basic Evaluator Usage

```python
from tdc import Evaluator

# Initialize evaluator
evaluator = Evaluator(name='ROC-AUC')

# Evaluate predictions
score = evaluator(y_true, y_pred)
```

### Classification Metrics

#### ROC-AUC
Receiver Operating Characteristic - Area Under Curve

```python
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred_proba)
```

**Best for:**
- Binary classification
- Imbalanced datasets
- Overall discriminative ability

**Range:** 0-1 (higher is better, 0.5 is random)

#### PR-AUC
Precision-Recall Area Under Curve

```python
evaluator = Evaluator(name='PR-AUC')
score = evaluator(y_true, y_pred_proba)
```

**Best for:**
- Highly imbalanced datasets
- When positive class is rare
- Complements ROC-AUC

**Range:** 0-1 (higher is better)

#### F1 Score
Harmonic mean of precision and recall

```python
evaluator = Evaluator(name='F1')
score = evaluator(y_true, y_pred_binary)
```

**Best for:**
- Balance between precision and recall
- Multi-class classification

**Range:** 0-1 (higher is better)

#### Accuracy
Fraction of correct predictions

```python
evaluator = Evaluator(name='Accuracy')
score = evaluator(y_true, y_pred_binary)
```

**Best for:**
- Balanced datasets
- Simple baseline metric

**Not recommended for:** Imbalanced datasets

#### Cohen's Kappa
Agreement between predictions and ground truth, accounting for chance

```python
evaluator = Evaluator(name='Kappa')
score = evaluator(y_true, y_pred_binary)
```

**Range:** -1 to 1 (higher is better, 0 is random)

### Regression Metrics

#### RMSE - Root Mean Squared Error
```python
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

**Best for:**
- Continuous predictions
- Penalizes large errors heavily

**Range:** 0-∞ (lower is better)

#### MAE - Mean Absolute Error
```python
evaluator = Evaluator(name='MAE')
score = evaluator(y_true, y_pred)
```

**Best for:**
- Continuous predictions
- More robust to outliers than RMSE

**Range:** 0-∞ (lower is better)

#### R² - Coefficient of Determination
```python
evaluator = Evaluator(name='R2')
score = evaluator(y_true, y_pred)
```

**Best for:**
- Variance explained by model
- Comparing different models

**Range:** -∞ to 1 (higher is better, 1 is perfect)

#### MSE - Mean Squared Error
```python
evaluator = Evaluator(name='MSE')
score = evaluator(y_true, y_pred)
```

**Range:** 0-∞ (lower is better)

### Ranking Metrics

#### Spearman Correlation
Rank correlation coefficient

```python
evaluator = Evaluator(name='Spearman')
score = evaluator(y_true, y_pred)
```

**Best for:**
- Ranking tasks
- Non-linear relationships
- Ordinal data

**Range:** -1 to 1 (higher is better)

#### Pearson Correlation
Linear correlation coefficient

```python
evaluator = Evaluator(name='Pearson')
score = evaluator(y_true, y_pred)
```

**Best for:**
- Linear relationships
- Continuous data

**Range:** -1 to 1 (higher is better)

### Multi-Label Classification

```python
evaluator = Evaluator(name='Micro-F1')
score = evaluator(y_true_multilabel, y_pred_multilabel)
```

Available: `Micro-F1`, `Macro-F1`, `Micro-AUPR`, `Macro-AUPR`

### Benchmark Group Evaluation

For benchmark groups, evaluation requires multiple seeds:

```python
from tdc.benchmark_group import admet_group

group = admet_group(path='data/')
benchmark = group.get('Caco2_Wang')

# Predictions must be dict with seeds as keys
predictions = {}
for seed in [1, 2, 3, 4, 5]:
    # Train model and predict
    predictions[seed] = model_predictions

# Evaluate with mean and std across seeds
results = group.evaluate(predictions)
print(results)  # {'Caco2_Wang': [mean_score, std_score]}
```

## 3. Data Processing

TDC provides 11 comprehensive data processing utilities.

### Molecule Format Conversion

Convert between ~15 molecular representations.

```python
from tdc.chem_utils import MolConvert

# SMILES to PyTorch Geometric
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# SMILES to DGL
converter = MolConvert(src='SMILES', dst='DGL')
dgl_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# SMILES to Morgan Fingerprint (ECFP)
converter = MolConvert(src='SMILES', dst='ECFP')
fingerprint = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

**Available formats:**
- **Text**: SMILES, SELFIES, InChI
- **Fingerprints**: ECFP (Morgan), MACCS, RDKit, AtomPair, TopologicalTorsion
- **Graphs**: PyG (PyTorch Geometric), DGL (Deep Graph Library)
- **3D**: Graph3D, Coulomb Matrix, Distance Matrix

**Batch conversion:**
```python
converter = MolConvert(src='SMILES', dst='PyG')
graphs = converter(['SMILES1', 'SMILES2', 'SMILES3'])
```

### Molecule Filters

Remove non-drug-like molecules using curated chemical rules.

```python
from tdc.chem_utils import MolFilter

# Initialize filter with rules
mol_filter = MolFilter(
    rules=['PAINS', 'BMS'],  # Chemical filter rules
    property_filters_dict={
        'MW': (150, 500),      # Molecular weight range
        'LogP': (-0.4, 5.6),   # Lipophilicity range
        'HBD': (0, 5),         # H-bond donors
        'HBA': (0, 10)         # H-bond acceptors
    }
)

# Filter molecules
filtered_smiles = mol_filter(smiles_list)
```

**Available filter rules:**
- `PAINS` - Pan-Assay Interference Compounds
- `BMS` - Bristol-Myers Squibb HTS deck filters
- `Glaxo` - GlaxoSmithKline filters
- `Dundee` - University of Dundee filters
- `Inpharmatica` - Inpharmatica filters
- `LINT` - Pfizer LINT filters

### Label Distribution Visualization

```python
# Visualize label distribution
data.label_distribution()

# Print statistics
data.print_stats()
```

Displays histogram and computes mean, median, std for continuous labels.

### Label Binarization

Convert continuous labels to binary using threshold.

```python
from tdc.utils import binarize

# Binarize with threshold
binary_labels = binarize(y_continuous, threshold=5.0, order='ascending')
# order='ascending': values >= threshold become 1
# order='descending': values <= threshold become 1
```

### Label Units Conversion

Transform between measurement units.

```python
from tdc.chem_utils import label_transform

# Convert nM to pKd
y_pkd = label_transform(y_nM, from_unit='nM', to_unit='p')

# Convert μM to nM
y_nM = label_transform(y_uM, from_unit='uM', to_unit='nM')
```

**Available conversions:**
- Binding affinity: nM, μM, pKd, pKi, pIC50
- Log transformations
- Natural log conversions

### Label Meaning

Get interpretable descriptions for labels.

```python
# Get label mapping
label_map = data.get_label_map(name='DrugBank')
print(label_map)
# {0: 'No interaction', 1: 'Increased effect', 2: 'Decreased effect', ...}
```

### Data Balancing

Handle class imbalance via over/under-sampling.

```python
from tdc.utils import balance

# Oversample minority class
X_balanced, y_balanced = balance(X, y, method='oversample')

# Undersample majority class
X_balanced, y_balanced = balance(X, y, method='undersample')
```

### Graph Transformation for Pair Data

Convert paired data to graph representations.

```python
from tdc.utils import create_graph_from_pairs

# Create graph from drug-drug pairs
graph = create_graph_from_pairs(
    pairs=ddi_pairs,  # [(drug1, drug2, label), ...]
    format='edge_list'  # or 'PyG', 'DGL'
)
```

### Negative Sampling

Generate negative samples for binary tasks.

```python
from tdc.utils import negative_sample

# Generate negative samples for DTI
negative_pairs = negative_sample(
    positive_pairs=known_interactions,
    all_drugs=drug_list,
    all_targets=target_list,
    ratio=1.0  # Negative:positive ratio
)
```

**Use cases:**
- Drug-target interaction prediction
- Drug-drug interaction tasks
- Creating balanced datasets

### Entity Retrieval

Convert between database identifiers.

#### PubChem CID to SMILES
```python
from tdc.utils import cid2smiles

smiles = cid2smiles(2244)  # Aspirin
# Returns: 'CC(=O)Oc1ccccc1C(=O)O'
```

#### UniProt ID to Amino Acid Sequence
```python
from tdc.utils import uniprot2seq

sequence = uniprot2seq('P12345')
# Returns: 'MVKVYAPASS...'
```

#### Batch Retrieval
```python
# Multiple CIDs
smiles_list = [cid2smiles(cid) for cid in [2244, 5090, 6323]]

# Multiple UniProt IDs
sequences = [uniprot2seq(uid) for uid in ['P12345', 'Q9Y5S9']]
```

## 4. Advanced Utilities

### Retrieve Dataset Names

```python
from tdc.utils import retrieve_dataset_names

# Get all datasets for a task
adme_datasets = retrieve_dataset_names('ADME')
dti_datasets = retrieve_dataset_names('DTI')
tox_datasets = retrieve_dataset_names('Tox')

print(f"ADME datasets: {adme_datasets}")
```

### Fuzzy Search

TDC supports fuzzy matching for dataset names:

```python
from tdc.single_pred import ADME

# These all work (typo-tolerant)
data = ADME(name='Caco2_Wang')
data = ADME(name='caco2_wang')
data = ADME(name='Caco2')  # Partial match
```

### Data Format Options

```python
# Pandas DataFrame (default)
df = data.get_data(format='df')

# Dictionary
data_dict = data.get_data(format='dict')

# DeepPurpose format (for DeepPurpose library)
dp_format = data.get_data(format='DeepPurpose')

# PyG/DGL graphs (if applicable)
graphs = data.get_data(format='PyG')
```

### Data Loader Utilities

```python
from tdc.utils import create_fold

# Create cross-validation folds
folds = create_fold(data, fold=5, seed=42)
# Returns list of (train_idx, test_idx) tuples

# Iterate through folds
for i, (train_idx, test_idx) in enumerate(folds):
    train_data = data.iloc[train_idx]
    test_data = data.iloc[test_idx]
    # Train and evaluate
```

## Common Workflows

### Workflow 1: Complete Data Pipeline

```python
from tdc.single_pred import ADME
from tdc import Evaluator
from tdc.chem_utils import MolConvert, MolFilter

# 1. Load data
data = ADME(name='Caco2_Wang')

# 2. Filter molecules
mol_filter = MolFilter(rules=['PAINS'])
filtered_data = data.get_data()
filtered_data = filtered_data[
    filtered_data['Drug'].apply(lambda x: mol_filter([x]))
]

# 3. Split data
split = data.get_split(method='scaffold', seed=42)
train, valid, test = split['train'], split['valid'], split['test']

# 4. Convert to graph representations
converter = MolConvert(src='SMILES', dst='PyG')
train_graphs = converter(train['Drug'].tolist())

# 5. Train model (user implements)
# model.fit(train_graphs, train['Y'])

# 6. Evaluate
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### Workflow 2: Multi-Task Learning Preparation

```python
from tdc.benchmark_group import admet_group
from tdc.chem_utils import MolConvert

# Load benchmark group
group = admet_group(path='data/')

# Get multiple datasets
datasets = ['Caco2_Wang', 'HIA_Hou', 'Bioavailability_Ma']
all_data = {}

for dataset_name in datasets:
    benchmark = group.get(dataset_name)
    all_data[dataset_name] = benchmark

# Prepare for multi-task learning
converter = MolConvert(src='SMILES', dst='ECFP')
# Process each dataset...
```

### Workflow 3: DTI Cold Split Evaluation

```python
from tdc.multi_pred import DTI
from tdc import Evaluator

# Load DTI data
data = DTI(name='BindingDB_Kd')

# Cold drug split
split = data.get_split(method='cold_drug', seed=42)
train, test = split['train'], split['test']

# Verify no drug overlap
train_drugs = set(train['Drug_ID'])
test_drugs = set(test['Drug_ID'])
assert len(train_drugs & test_drugs) == 0, "Drug leakage detected!"

# Train and evaluate
# model.fit(train)
evaluator = Evaluator(name='RMSE')
# score = evaluator(test['Y'], predictions)
```

## Best Practices

1. **Always use meaningful splits** - Use scaffold or cold splits for realistic evaluation
2. **Multiple seeds** - Run experiments with multiple seeds for robust results
3. **Appropriate metrics** - Choose metrics that match your task and dataset characteristics
4. **Data filtering** - Remove PAINS and non-drug-like molecules before training
5. **Format conversion** - Convert molecules to appropriate format for your model
6. **Batch processing** - Use batch operations for efficiency with large datasets

## Performance Tips

- Convert molecules in batch mode for faster processing
- Cache converted representations to avoid recomputation
- Use appropriate data formats for your framework (PyG, DGL, etc.)
- Filter data early in the pipeline to reduce computation

## References

- TDC Documentation: https://tdc.readthedocs.io
- Data Functions: https://tdcommons.ai/fct_overview/
- Evaluation Metrics: https://tdcommons.ai/functions/model_eval/
- Data Splits: https://tdcommons.ai/functions/data_split/
