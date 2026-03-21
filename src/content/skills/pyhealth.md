---
title: "PyHealth 医疗AI"
description: "医疗健康数据的深度学习工具包，电子健康记录分析"
category: "devops"
source: "community"
author: "Community"
tags: ["pyhealth"]
date: 2026-03-20
---

# PyHealth: Healthcare AI Toolkit

## Overview

PyHealth is a comprehensive Python library for healthcare AI that provides specialized tools, models, and datasets for clinical machine learning. Use this skill when developing healthcare prediction models, processing clinical data, working with medical coding systems, or deploying AI solutions in healthcare settings.

## When to Use This Skill

Invoke this skill when:

- **Working with healthcare datasets**: MIMIC-III, MIMIC-IV, eICU, OMOP, sleep EEG data, medical images
- **Clinical prediction tasks**: Mortality prediction, hospital readmission, length of stay, drug recommendation
- **Medical coding**: Translating between ICD-9/10, NDC, RxNorm, ATC coding systems
- **Processing clinical data**: Sequential events, physiological signals, clinical text, medical images
- **Implementing healthcare models**: RETAIN, SafeDrug, GAMENet, StageNet, Transformer for EHR
- **Evaluating clinical models**: Fairness metrics, calibration, interpretability, uncertainty quantification

## Core Capabilities

PyHealth operates through a modular 5-stage pipeline optimized for healthcare AI:

1. **Data Loading**: Access 10+ healthcare datasets with standardized interfaces
2. **Task Definition**: Apply 20+ predefined clinical prediction tasks or create custom tasks
3. **Model Selection**: Choose from 33+ models (baselines, deep learning, healthcare-specific)
4. **Training**: Train with automatic checkpointing, monitoring, and evaluation
5. **Deployment**: Calibrate, interpret, and validate for clinical use

**Performance**: 3x faster than pandas for healthcare data processing

## Quick Start Workflow

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Load dataset and set task
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Split data
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 3. Create data loaders
train_loader = get_dataloader(train, batch_size=64, shuffle=True)
val_loader = get_dataloader(val, batch_size=64, shuffle=False)
test_loader = get_dataloader(test, batch_size=64, shuffle=False)

# 4. Initialize and train model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    embedding_dim=128
)

trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_score"
)

# 5. Evaluate
results = trainer.evaluate(test_loader)
```

## Detailed Documentation

This skill includes comprehensive reference documentation organized by functionality. Read specific reference files as needed:

### 1. Datasets and Data Structures

**File**: `references/datasets.md`

**Read when:**
- Loading healthcare datasets (MIMIC, eICU, OMOP, sleep EEG, etc.)
- Understanding Event, Patient, Visit data structures
- Processing different data types (EHR, signals, images, text)
- Splitting data for training/validation/testing
- Working with SampleDataset for task-specific formatting

**Key Topics:**
- Core data structures (Event, Patient, Visit)
- 10+ available datasets (EHR, physiological signals, imaging, text)
- Data loading and iteration
- Train/val/test splitting strategies
- Performance optimization for large datasets

### 2. Medical Coding Translation

**File**: `references/medical_coding.md`

**Read when:**
- Translating between medical coding systems
- Working with diagnosis codes (ICD-9-CM, ICD-10-CM, CCS)
- Processing medication codes (NDC, RxNorm, ATC)
- Standardizing procedure codes (ICD-9-PROC, ICD-10-PROC)
- Grouping codes into clinical categories
- Handling hierarchical drug classifications

**Key Topics:**
- InnerMap for within-system lookups
- CrossMap for cross-system translation
- Supported coding systems (ICD, NDC, ATC, CCS, RxNorm)
- Code standardization and hierarchy traversal
- Medication classification by therapeutic class
- Integration with datasets

### 3. Clinical Prediction Tasks

**File**: `references/tasks.md`

**Read when:**
- Defining clinical prediction objectives
- Using predefined tasks (mortality, readmission, drug recommendation)
- Working with EHR, signal, imaging, or text-based tasks
- Creating custom prediction tasks
- Setting up input/output schemas for models
- Applying task-specific filtering logic

**Key Topics:**
- 20+ predefined clinical tasks
- EHR tasks (mortality, readmission, length of stay, drug recommendation)
- Signal tasks (sleep staging, EEG analysis, seizure detection)
- Imaging tasks (COVID-19 chest X-ray classification)
- Text tasks (medical coding, specialty classification)
- Custom task creation patterns

### 4. Models and Architectures

**File**: `references/models.md`

**Read when:**
- Selecting models for clinical prediction
- Understanding model architectures and capabilities
- Choosing between general-purpose and healthcare-specific models
- Implementing interpretable models (RETAIN, AdaCare)
- Working with medication recommendation (SafeDrug, GAMENet)
- Using graph neural networks for healthcare
- Configuring model hyperparameters

**Key Topics:**
- 33+ available models
- General-purpose: Logistic Regression, MLP, CNN, RNN, Transformer, GNN
- Healthcare-specific: RETAIN, SafeDrug, GAMENet, StageNet, AdaCare
- Model selection by task type and data type
- Interpretability considerations
- Computational requirements
- Hyperparameter tuning guidelines

### 5. Data Preprocessing

**File**: `references/preprocessing.md`

**Read when:**
- Preprocessing clinical data for models
- Handling sequential events and time-series data
- Processing physiological signals (EEG, ECG)
- Normalizing lab values and vital signs
- Preparing labels for different task types
- Building feature vocabularies
- Managing missing data and outliers

**Key Topics:**
- 15+ processor types
- Sequence processing (padding, truncation)
- Signal processing (filtering, segmentation)
- Feature extraction and encoding
- Label processors (binary, multi-class, multi-label, regression)
- Text and image preprocessing
- Common preprocessing workflows

### 6. Training and Evaluation

**File**: `references/training_evaluation.md`

**Read when:**
- Training models with the Trainer class
- Evaluating model performance
- Computing clinical metrics
- Assessing model fairness across demographics
- Calibrating predictions for reliability
- Quantifying prediction uncertainty
- Interpreting model predictions
- Preparing models for clinical deployment

**Key Topics:**
- Trainer class (train, evaluate, inference)
- Metrics for binary, multi-class, multi-label, regression tasks
- Fairness metrics for bias assessment
- Calibration methods (Platt scaling, temperature scaling)
- Uncertainty quantification (conformal prediction, MC dropout)
- Interpretability tools (attention visualization, SHAP, ChEFER)
- Complete training pipeline example

## Installation

```bash
uv pip install pyhealth
```

**Requirements:**
- Python ≥ 3.7
- PyTorch ≥ 1.8
- NumPy, pandas, scikit-learn

## Common Use Cases

### Use Case 1: ICU Mortality Prediction

**Objective**: Predict patient mortality in intensive care unit

**Approach:**
1. Load MIMIC-IV dataset → Read `references/datasets.md`
2. Apply mortality prediction task → Read `references/tasks.md`
3. Select interpretable model (RETAIN) → Read `references/models.md`
4. Train and evaluate → Read `references/training_evaluation.md`
5. Interpret predictions for clinical use → Read `references/training_evaluation.md`

### Use Case 2: Safe Medication Recommendation

**Objective**: Recommend medications while avoiding drug-drug interactions

**Approach:**
1. Load EHR dataset (MIMIC-IV or OMOP) → Read `references/datasets.md`
2. Apply drug recommendation task → Read `references/tasks.md`
3. Use SafeDrug model with DDI constraints → Read `references/models.md`
4. Preprocess medication codes → Read `references/medical_coding.md`
5. Evaluate with multi-label metrics → Read `references/training_evaluation.md`

### Use Case 3: Hospital Readmission Prediction

**Objective**: Identify patients at risk of 30-day readmission

**Approach:**
1. Load multi-site EHR data (eICU or OMOP) → Read `references/datasets.md`
2. Apply readmission prediction task → Read `references/tasks.md`
3. Handle class imbalance in preprocessing → Read `references/preprocessing.md`
4. Train Transformer model → Read `references/models.md`
5. Calibrate predictions and assess fairness → Read `references/training_evaluation.md`

### Use Case 4: Sleep Disorder Diagnosis

**Objective**: Classify sleep stages from EEG signals

**Approach:**
1. Load sleep EEG dataset (SleepEDF, SHHS) → Read `references/datasets.md`
2. Apply sleep staging task → Read `references/tasks.md`
3. Preprocess EEG signals (filtering, segmentation) → Read `references/preprocessing.md`
4. Train CNN or RNN model → Read `references/models.md`
5. Evaluate per-stage performance → Read `references/training_evaluation.md`

### Use Case 5: Medical Code Translation

**Objective**: Standardize diagnoses across different coding systems

**Approach:**
1. Read `references/medical_coding.md` for comprehensive guidance
2. Use CrossMap to translate between ICD-9, ICD-10, CCS
3. Group codes into clinically meaningful categories
4. Integrate with dataset processing

### Use Case 6: Clinical Text to ICD Coding

**Objective**: Automatically assign ICD codes from clinical notes

**Approach:**
1. Load MIMIC-III with clinical text → Read `references/datasets.md`
2. Apply ICD coding task → Read `references/tasks.md`
3. Preprocess clinical text → Read `references/preprocessing.md`
4. Use TransformersModel (ClinicalBERT) → Read `references/models.md`
5. Evaluate with multi-label metrics → Read `references/training_evaluation.md`

## Best Practices

### Data Handling

1. **Always split by patient**: Prevent data leakage by ensuring no patient appears in multiple splits
   ```python
   from pyhealth.datasets import split_by_patient
   train, val, test = split_by_patient(dataset, [0.7, 0.1, 0.2])
   ```

2. **Check dataset statistics**: Understand your data before modeling
   ```python
   print(dataset.stats())  # Patients, visits, events, code distributions
   ```

3. **Use appropriate preprocessing**: Match processors to data types (see `references/preprocessing.md`)

### Model Development

1. **Start with baselines**: Establish baseline performance with simple models
   - Logistic Regression for binary/multi-class tasks
   - MLP for initial deep learning baseline

2. **Choose task-appropriate models**:
   - Interpretability needed → RETAIN, AdaCare
   - Drug recommendation → SafeDrug, GAMENet
   - Long sequences → Transformer
   - Graph relationships → GNN

3. **Monitor validation metrics**: Use appropriate metrics for task and handle class imbalance
   - Binary classification: AUROC, AUPRC (especially for rare events)
   - Multi-class: macro-F1 (for imbalanced), weighted-F1
   - Multi-label: Jaccard, example-F1
   - Regression: MAE, RMSE

### Clinical Deployment

1. **Calibrate predictions**: Ensure probabilities are reliable (see `references/training_evaluation.md`)

2. **Assess fairness**: Evaluate across demographic groups to detect bias

3. **Quantify uncertainty**: Provide confidence estimates for predictions

4. **Interpret predictions**: Use attention weights, SHAP, or ChEFER for clinical trust

5. **Validate thoroughly**: Use held-out test sets from different time periods or sites

## Limitations and Considerations

### Data Requirements

- **Large datasets**: Deep learning models require sufficient data (thousands of patients)
- **Data quality**: Missing data and coding errors impact performance
- **Temporal consistency**: Ensure train/test split respects temporal ordering when needed

### Clinical Validation

- **External validation**: Test on data from different hospitals/systems
- **Prospective evaluation**: Validate in real clinical settings before deployment
- **Clinical review**: Have clinicians review predictions and interpretations
- **Ethical considerations**: Address privacy (HIPAA/GDPR), fairness, and safety

### Computational Resources

- **GPU recommended**: For training deep learning models efficiently
- **Memory requirements**: Large datasets may require 16GB+ RAM
- **Storage**: Healthcare datasets can be 10s-100s of GB

## Troubleshooting

### Common Issues

**ImportError for dataset**:
- Ensure dataset files are downloaded and path is correct
- Check PyHealth version compatibility

**Out of memory**:
- Reduce batch size
- Reduce sequence length (`max_seq_length`)
- Use gradient accumulation
- Process data in chunks

**Poor performance**:
- Check class imbalance and use appropriate metrics (AUPRC vs AUROC)
- Verify preprocessing (normalization, missing data handling)
- Increase model capacity or training epochs
- Check for data leakage in train/test split

**Slow training**:
- Use GPU (`device="cuda"`)
- Increase batch size (if memory allows)
- Reduce sequence length
- Use more efficient model (CNN vs Transformer)

### Getting Help

- **Documentation**: https://pyhealth.readthedocs.io/
- **GitHub Issues**: https://github.com/sunlabuiuc/PyHealth/issues
- **Tutorials**: 7 core tutorials + 5 practical pipelines available online

## Example: Complete Workflow

```python
# Complete mortality prediction pipeline
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer

# 1. Load dataset
print("Loading MIMIC-IV dataset...")
dataset = MIMIC4Dataset(root="/data/mimic4")
print(dataset.stats())

# 2. Define task
print("Setting mortality prediction task...")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
print(f"Generated {len(sample_dataset)} samples")

# 3. Split data (by patient to prevent leakage)
print("Splitting data...")
train_ds, val_ds, test_ds = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 4. Create data loaders
train_loader = get_dataloader(train_ds, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_ds, batch_size=64)
test_loader = get_dataloader(test_ds, batch_size=64)

# 5. Initialize interpretable model
print("Initializing RETAIN model...")
model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    hidden_dim=128
)

# 6. Train model
print("Training model...")
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer="Adam",
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",  # Use AUPRC for imbalanced data
    monitor_criterion="max",
    save_path="./checkpoints/mortality_retain"
)

# 7. Evaluate on test set
print("Evaluating on test set...")
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("\nTest Results:")
for metric, value in test_results.items():
    print(f"  {metric}: {value:.4f}")

# 8. Get predictions with attention for interpretation
predictions = trainer.inference(
    test_loader,
    additional_outputs=["visit_attention", "feature_attention"],
    return_patient_ids=True
)

# 9. Analyze a high-risk patient
high_risk_idx = predictions["y_pred"].argmax()
patient_id = predictions["patient_ids"][high_risk_idx]
visit_attn = predictions["visit_attention"][high_risk_idx]
feature_attn = predictions["feature_attention"][high_risk_idx]

print(f"\nHigh-risk patient: {patient_id}")
print(f"Risk score: {predictions['y_pred'][high_risk_idx]:.3f}")
print(f"Most influential visit: {visit_attn.argmax()}")
print(f"Most important features: {feature_attn[visit_attn.argmax()].argsort()[-5:]}")

# 10. Save model for deployment
trainer.save("./models/mortality_retain_final.pt")
print("\nModel saved successfully!")
```

## Resources

For detailed information on each component, refer to the comprehensive reference files in the `references/` directory:

- **datasets.md**: Data structures, loading, and splitting (4,500 words)
- **medical_coding.md**: Code translation and standardization (3,800 words)
- **tasks.md**: Clinical prediction tasks and custom task creation (4,200 words)
- **models.md**: Model architectures and selection guidelines (5,100 words)
- **preprocessing.md**: Data processors and preprocessing workflows (4,600 words)
- **training_evaluation.md**: Training, metrics, calibration, interpretability (5,900 words)

**Total comprehensive documentation**: ~28,000 words across modular reference files.

---

## Reference: Datasets

# PyHealth Datasets and Data Structures

## Core Data Structures

### Event
Individual medical occurrences with attributes including:
- **code**: Medical code (diagnosis, medication, procedure, lab test)
- **vocabulary**: Coding system (ICD-9-CM, NDC, LOINC, etc.)
- **timestamp**: Event occurrence time
- **value**: Numeric value (for labs, vital signs)
- **unit**: Measurement unit

### Patient
Collection of events organized chronologically across visits. Each patient contains:
- **patient_id**: Unique identifier
- **birth_datetime**: Date of birth
- **gender**: Patient gender
- **ethnicity**: Patient ethnicity
- **visits**: List of visit objects

### Visit
Healthcare encounter containing:
- **visit_id**: Unique identifier
- **encounter_time**: Visit timestamp
- **discharge_time**: Discharge timestamp
- **visit_type**: Type of encounter (inpatient, outpatient, emergency)
- **events**: List of events during this visit

## BaseDataset Class

**Key Methods:**
- `get_patient(patient_id)`: Retrieve single patient record
- `iter_patients()`: Iterate through all patients
- `stats()`: Get dataset statistics (patients, visits, events)
- `set_task(task_fn)`: Define prediction task

## Available Datasets

### Electronic Health Record (EHR) Datasets

**MIMIC-III Dataset** (`MIMIC3Dataset`)
- Intensive care unit data from Beth Israel Deaconess Medical Center
- 40,000+ critical care patients
- Diagnoses, procedures, medications, lab results
- Usage: `from pyhealth.datasets import MIMIC3Dataset`

**MIMIC-IV Dataset** (`MIMIC4Dataset`)
- Updated version with 70,000+ patients
- Improved data quality and coverage
- Enhanced demographic and clinical detail
- Usage: `from pyhealth.datasets import MIMIC4Dataset`

**eICU Dataset** (`eICUDataset`)
- Multi-center critical care database
- 200,000+ admissions from 200+ hospitals
- Standardized ICU data across facilities
- Usage: `from pyhealth.datasets import eICUDataset`

**OMOP Dataset** (`OMOPDataset`)
- Observational Medical Outcomes Partnership format
- Standardized common data model
- Interoperability across healthcare systems
- Usage: `from pyhealth.datasets import OMOPDataset`

**EHRShot Dataset** (`EHRShotDataset`)
- Benchmark dataset for few-shot learning
- Specialized for testing model generalization
- Usage: `from pyhealth.datasets import EHRShotDataset`

### Physiological Signal Datasets

**Sleep EEG Datasets:**
- `SleepEDFDataset`: Sleep-EDF database for sleep staging
- `SHHSDataset`: Sleep Heart Health Study data
- `ISRUCDataset`: ISRUC-Sleep database

**Temple University EEG Datasets:**
- `TUEVDataset`: Abnormal EEG events detection
- `TUABDataset`: Abnormal/normal EEG classification
- `TUSZDataset`: Seizure detection

**All signal datasets support:**
- Multi-channel EEG signals
- Standardized sampling rates
- Expert annotations
- Sleep stage or abnormality labels

### Medical Imaging Datasets

**COVID-19 CXR Dataset** (`COVID19CXRDataset`)
- Chest X-ray images for COVID-19 classification
- Multi-class labels (COVID-19, pneumonia, normal)
- Usage: `from pyhealth.datasets import COVID19CXRDataset`

### Text-Based Datasets

**Medical Transcriptions Dataset** (`MedicalTranscriptionsDataset`)
- Clinical notes and transcriptions
- Medical specialty classification
- Text-based prediction tasks
- Usage: `from pyhealth.datasets import MedicalTranscriptionsDataset`

**Cardiology Dataset** (`CardiologyDataset`)
- Cardiac patient records
- Cardiovascular disease prediction
- Usage: `from pyhealth.datasets import CardiologyDataset`

### Preprocessed Datasets

**MIMIC Extract Dataset** (`MIMICExtractDataset`)
- Pre-extracted MIMIC features
- Ready-to-use benchmarking data
- Reduced preprocessing requirements
- Usage: `from pyhealth.datasets import MIMICExtractDataset`

## SampleDataset Class

Converts raw datasets into task-specific formatted samples.

**Purpose:** Transform patient-level data into model-ready input/output pairs

**Key Attributes:**
- `input_schema`: Defines input data structure
- `output_schema`: Defines target labels/predictions
- `samples`: List of processed samples

**Usage Pattern:**
```python
# After setting task on BaseDataset
sample_dataset = dataset.set_task(task_fn)
```

## Data Splitting Functions

**Patient-Level Split** (`split_by_patient`)
- Ensures no patient appears in multiple splits
- Prevents data leakage
- Recommended for clinical prediction tasks

**Visit-Level Split** (`split_by_visit`)
- Splits by individual visits
- Allows same patient across splits (use cautiously)

**Sample-Level Split** (`split_by_sample`)
- Random sample splitting
- Most flexible but may cause leakage

**Parameters:**
- `dataset`: SampleDataset to split
- `ratios`: Tuple of split ratios (e.g., [0.7, 0.1, 0.2])
- `seed`: Random seed for reproducibility

## Common Workflow

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient

# 1. Load dataset
dataset = MIMIC4Dataset(root="/path/to/data")

# 2. Set prediction task
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 3. Split data
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 4. Get statistics
print(dataset.stats())
```

## Performance Notes

- PyHealth is **3x faster than pandas** for healthcare data processing
- Optimized for large-scale EHR datasets
- Memory-efficient patient iteration
- Vectorized operations for feature extraction

---

## Reference: Medical_Coding

# PyHealth Medical Code Translation

## Overview

Healthcare data uses multiple coding systems and standards. PyHealth's MedCode module enables translation and mapping between medical coding systems through ontology lookups and cross-system mappings.

## Core Classes

### InnerMap
Handles within-system ontology lookups and hierarchical navigation.

**Key Capabilities:**
- Code lookup with attributes (names, descriptions)
- Ancestor/descendant hierarchy traversal
- Code standardization and conversion
- Parent-child relationship navigation

### CrossMap
Manages cross-system mappings between different coding standards.

**Key Capabilities:**
- Translation between coding systems
- Many-to-many relationship handling
- Hierarchical level specification (for medications)
- Bidirectional mapping support

## Supported Coding Systems

### Diagnosis Codes

**ICD-9-CM (International Classification of Diseases, 9th Revision, Clinical Modification)**
- Legacy diagnosis coding system
- Hierarchical structure with 3-5 digit codes
- Used in US healthcare pre-2015
- Usage: `from pyhealth.medcode import InnerMap`
  - `icd9_map = InnerMap.load("ICD9CM")`

**ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification)**
- Current diagnosis coding standard
- Alphanumeric codes (3-7 characters)
- More granular than ICD-9
- Usage: `from pyhealth.medcode import InnerMap`
  - `icd10_map = InnerMap.load("ICD10CM")`

**CCSCM (Clinical Classifications Software for ICD-CM)**
- Groups ICD codes into clinically meaningful categories
- Reduces dimensionality for analysis
- Single-level and multi-level hierarchies
- Usage: `from pyhealth.medcode import CrossMap`
  - `icd_to_ccs = CrossMap.load("ICD9CM", "CCSCM")`

### Procedure Codes

**ICD-9-PROC (ICD-9 Procedure Codes)**
- Inpatient procedure classification
- 3-4 digit numeric codes
- Legacy system (pre-2015)
- Usage: `from pyhealth.medcode import InnerMap`
  - `icd9proc_map = InnerMap.load("ICD9PROC")`

**ICD-10-PROC (ICD-10 Procedure Coding System)**
- Current procedural coding standard
- 7-character alphanumeric codes
- More detailed than ICD-9-PROC
- Usage: `from pyhealth.medcode import InnerMap`
  - `icd10proc_map = InnerMap.load("ICD10PROC")`

**CCSPROC (Clinical Classifications Software for Procedures)**
- Groups procedure codes into categories
- Simplifies procedure analysis
- Usage: `from pyhealth.medcode import CrossMap`
  - `proc_to_ccs = CrossMap.load("ICD9PROC", "CCSPROC")`

### Medication Codes

**NDC (National Drug Code)**
- US FDA drug identification system
- 10 or 11-digit codes
- Product-level specificity (manufacturer, strength, package)
- Usage: `from pyhealth.medcode import InnerMap`
  - `ndc_map = InnerMap.load("NDC")`

**RxNorm**
- Standardized drug terminology
- Normalized drug names and relationships
- Links multiple drug vocabularies
- Usage: `from pyhealth.medcode import CrossMap`
  - `ndc_to_rxnorm = CrossMap.load("NDC", "RXNORM")`

**ATC (Anatomical Therapeutic Chemical Classification)**
- WHO drug classification system
- 5-level hierarchy:
  - **Level 1**: Anatomical main group (1 letter)
  - **Level 2**: Therapeutic subgroup (2 digits)
  - **Level 3**: Pharmacological subgroup (1 letter)
  - **Level 4**: Chemical subgroup (1 letter)
  - **Level 5**: Chemical substance (2 digits)
- Example: "C03CA01" = Furosemide
  - C = Cardiovascular system
  - C03 = Diuretics
  - C03C = High-ceiling diuretics
  - C03CA = Sulfonamides
  - C03CA01 = Furosemide

**Usage:**
```python
from pyhealth.medcode import CrossMap
ndc_to_atc = CrossMap.load("NDC", "ATC")
atc_codes = ndc_to_atc.map("00074-3799-13", level=3)  # Get ATC level 3
```

## Common Operations

### InnerMap Operations

**1. Code Lookup**
```python
from pyhealth.medcode import InnerMap

icd9_map = InnerMap.load("ICD9CM")
info = icd9_map.lookup("428.0")  # Heart failure
# Returns: name, description, additional attributes
```

**2. Ancestor Traversal**
```python
# Get all parent codes in hierarchy
ancestors = icd9_map.get_ancestors("428.0")
# Returns: ["428", "420-429", "390-459"]
```

**3. Descendant Traversal**
```python
# Get all child codes
descendants = icd9_map.get_descendants("428")
# Returns: ["428.0", "428.1", "428.2", ...]
```

**4. Code Standardization**
```python
# Normalize code format
standard_code = icd9_map.standardize("4280")  # Returns "428.0"
```

### CrossMap Operations

**1. Direct Translation**
```python
from pyhealth.medcode import CrossMap

# ICD-9-CM to CCS
icd_to_ccs = CrossMap.load("ICD9CM", "CCSCM")
ccs_codes = icd_to_ccs.map("82101")  # Coronary atherosclerosis
# Returns: ["101"]  # CCS category for coronary atherosclerosis
```

**2. Hierarchical Drug Mapping**
```python
# NDC to ATC at different levels
ndc_to_atc = CrossMap.load("NDC", "ATC")

# Get specific ATC level
atc_level_1 = ndc_to_atc.map("00074-3799-13", level=1)  # Anatomical group
atc_level_3 = ndc_to_atc.map("00074-3799-13", level=3)  # Pharmacological
atc_level_5 = ndc_to_atc.map("00074-3799-13", level=5)  # Chemical substance
```

**3. Bidirectional Mapping**
```python
# Map in either direction
rxnorm_to_ndc = CrossMap.load("RXNORM", "NDC")
ndc_codes = rxnorm_to_ndc.map("197381")  # Get all NDC codes for RxNorm
```

## Workflow Examples

### Example 1: Standardize and Group Diagnoses
```python
from pyhealth.medcode import InnerMap, CrossMap

# Load maps
icd9_map = InnerMap.load("ICD9CM")
icd_to_ccs = CrossMap.load("ICD9CM", "CCSCM")

# Process diagnosis codes
raw_codes = ["4280", "428.0", "42800"]

standardized = [icd9_map.standardize(code) for code in raw_codes]
# All become "428.0"

ccs_categories = [icd_to_ccs.map(code)[0] for code in standardized]
# All map to CCS category "108" (Heart failure)
```

### Example 2: Drug Classification Analysis
```python
from pyhealth.medcode import CrossMap

# Map NDC to ATC for drug class analysis
ndc_to_atc = CrossMap.load("NDC", "ATC")

patient_drugs = ["00074-3799-13", "00074-7286-01", "00456-0765-01"]

# Get therapeutic subgroups (ATC level 2)
drug_classes = []
for ndc in patient_drugs:
    atc_codes = ndc_to_atc.map(ndc, level=2)
    if atc_codes:
        drug_classes.append(atc_codes[0])

# Analyze drug class distribution
```

### Example 3: ICD-9 to ICD-10 Migration
```python
from pyhealth.medcode import CrossMap

# Load ICD-9 to ICD-10 mapping
icd9_to_icd10 = CrossMap.load("ICD9CM", "ICD10CM")

# Convert historical ICD-9 codes
icd9_code = "428.0"
icd10_codes = icd9_to_icd10.map(icd9_code)
# Returns: ["I50.9", "I50.1", ...]  # Multiple possible ICD-10 codes

# Handle one-to-many mappings
for icd10_code in icd10_codes:
    print(f"ICD-9 {icd9_code} -> ICD-10 {icd10_code}")
```

## Integration with Datasets

Medical code translation integrates seamlessly with PyHealth datasets:

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.medcode import CrossMap

# Load dataset
dataset = MIMIC4Dataset(root="/path/to/data")

# Load code mapping
icd_to_ccs = CrossMap.load("ICD10CM", "CCSCM")

# Process patient diagnoses
for patient in dataset.iter_patients():
    for visit in patient.visits:
        diagnosis_events = [e for e in visit.events if e.vocabulary == "ICD10CM"]

        for event in diagnosis_events:
            ccs_codes = icd_to_ccs.map(event.code)
            print(f"Diagnosis {event.code} -> CCS {ccs_codes}")
```

## Use Cases

### Clinical Research
- Standardize diagnoses across different coding systems
- Group related conditions for cohort identification
- Harmonize multi-site studies with different standards

### Drug Safety Analysis
- Classify medications by therapeutic class
- Identify drug-drug interactions at class level
- Analyze polypharmacy patterns

### Healthcare Analytics
- Reduce diagnosis/procedure dimensionality
- Create meaningful clinical categories
- Enable longitudinal analysis across coding system changes

### Machine Learning
- Create consistent feature representations
- Handle vocabulary mismatch in training/test data
- Generate hierarchical embeddings

## Best Practices

1. **Always standardize codes** before mapping to ensure consistent format
2. **Handle one-to-many mappings** appropriately (some codes map to multiple targets)
3. **Specify ATC level** explicitly when mapping drugs to avoid ambiguity
4. **Use CCS categories** to reduce diagnosis/procedure dimensionality
5. **Validate mappings** as some codes may not have direct translations
6. **Document code versions** (ICD-9 vs ICD-10) to maintain data provenance

---

## Reference: Models

# PyHealth Models

## Overview

PyHealth provides 33+ models for healthcare prediction tasks, ranging from simple baselines to state-of-the-art deep learning architectures. Models are organized into general-purpose architectures and healthcare-specific models.

## Model Base Class

All models inherit from `BaseModel` with standard PyTorch functionality:

**Key Attributes:**
- `dataset`: Associated SampleDataset
- `feature_keys`: Input features to use (e.g., ["diagnoses", "medications"])
- `mode`: Task type ("binary", "multiclass", "multilabel", "regression")
- `embedding_dim`: Feature embedding dimension
- `device`: Computation device (CPU/GPU)

**Key Methods:**
- `forward()`: Model forward pass
- `train_step()`: Single training iteration
- `eval_step()`: Single evaluation iteration
- `save()`: Save model checkpoint
- `load()`: Load model checkpoint

## General-Purpose Models

### Baseline Models

**Logistic Regression** (`LogisticRegression`)
- Linear classifier with mean pooling
- Simple baseline for comparison
- Fast training and inference
- Good for interpretability

**Usage:**
```python
from pyhealth.models import LogisticRegression

model = LogisticRegression(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary"
)
```

**Multi-Layer Perceptron** (`MLP`)
- Feedforward neural network
- Configurable hidden layers
- Supports mean/sum/max pooling
- Good baseline for structured data

**Parameters:**
- `hidden_dim`: Hidden layer size
- `num_layers`: Number of hidden layers
- `dropout`: Dropout rate
- `pooling`: Aggregation method ("mean", "sum", "max")

**Usage:**
```python
from pyhealth.models import MLP

model = MLP(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    hidden_dim=128,
    num_layers=3,
    dropout=0.5
)
```

### Convolutional Neural Networks

**CNN** (`CNN`)
- Convolutional layers for pattern detection
- Effective for sequential and spatial data
- Captures local temporal patterns
- Parameter efficient

**Architecture:**
- Multiple 1D convolutional layers
- Max pooling for dimension reduction
- Fully connected output layers

**Parameters:**
- `num_filters`: Number of convolutional filters
- `kernel_size`: Convolution kernel size
- `num_layers`: Number of conv layers
- `dropout`: Dropout rate

**Usage:**
```python
from pyhealth.models import CNN

model = CNN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    num_filters=64,
    kernel_size=3,
    num_layers=3
)
```

**Temporal Convolutional Networks** (`TCN`)
- Dilated convolutions for long-range dependencies
- Causal convolutions (no future information leakage)
- Efficient for long sequences
- Good for time-series prediction

**Advantages:**
- Captures long-term dependencies
- Parallelizable (faster than RNNs)
- Stable gradients

### Recurrent Neural Networks

**RNN** (`RNN`)
- Basic recurrent architecture
- Supports LSTM, GRU, RNN variants
- Sequential processing
- Captures temporal dependencies

**Parameters:**
- `rnn_type`: "LSTM", "GRU", or "RNN"
- `hidden_dim`: Hidden state dimension
- `num_layers`: Number of recurrent layers
- `dropout`: Dropout rate
- `bidirectional`: Use bidirectional RNN

**Usage:**
```python
from pyhealth.models import RNN

model = RNN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    rnn_type="LSTM",
    hidden_dim=128,
    num_layers=2,
    bidirectional=True
)
```

**Best for:**
- Sequential clinical events
- Temporal pattern learning
- Variable-length sequences

### Transformer Models

**Transformer** (`Transformer`)
- Self-attention mechanism
- Parallel processing of sequences
- State-of-the-art performance
- Effective for long-range dependencies

**Architecture:**
- Multi-head self-attention
- Position embeddings
- Feed-forward networks
- Layer normalization

**Parameters:**
- `num_heads`: Number of attention heads
- `num_layers`: Number of transformer layers
- `hidden_dim`: Hidden dimension
- `dropout`: Dropout rate
- `max_seq_length`: Maximum sequence length

**Usage:**
```python
from pyhealth.models import Transformer

model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    num_heads=8,
    num_layers=6,
    hidden_dim=256,
    dropout=0.1
)
```

**TransformersModel** (`TransformersModel`)
- Integration with HuggingFace transformers
- Pre-trained language models for clinical text
- Fine-tuning for healthcare tasks
- Examples: BERT, RoBERTa, BioClinicalBERT

**Usage:**
```python
from pyhealth.models import TransformersModel

model = TransformersModel(
    dataset=sample_dataset,
    feature_keys=["text"],
    mode="multiclass",
    pretrained_model="emilyalsentzer/Bio_ClinicalBERT"
)
```

### Graph Neural Networks

**GNN** (`GNN`)
- Graph-based learning
- Models relationships between entities
- Supports GAT (Graph Attention) and GCN (Graph Convolutional)

**Use Cases:**
- Drug-drug interactions
- Patient similarity networks
- Knowledge graph integration
- Comorbidity relationships

**Parameters:**
- `gnn_type`: "GAT" or "GCN"
- `hidden_dim`: Hidden dimension
- `num_layers`: Number of GNN layers
- `dropout`: Dropout rate
- `num_heads`: Attention heads (for GAT)

**Usage:**
```python
from pyhealth.models import GNN

model = GNN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="multilabel",
    gnn_type="GAT",
    hidden_dim=128,
    num_layers=3,
    num_heads=4
)
```

## Healthcare-Specific Models

### Interpretable Clinical Models

**RETAIN** (`RETAIN`)
- Reverse time attention mechanism
- Highly interpretable predictions
- Visit-level and event-level attention
- Identifies influential clinical events

**Key Features:**
- Two-level attention (visits and features)
- Temporal decay modeling
- Clinically meaningful explanations
- Published in NeurIPS 2016

**Usage:**
```python
from pyhealth.models import RETAIN

model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    hidden_dim=128
)

# Get attention weights for interpretation
outputs = model(batch)
visit_attention = outputs["visit_attention"]
feature_attention = outputs["feature_attention"]
```

**Best for:**
- Mortality prediction
- Readmission prediction
- Clinical risk scoring
- Interpretable predictions

**AdaCare** (`AdaCare`)
- Adaptive care model with feature calibration
- Disease-specific attention
- Handles irregular time intervals
- Interpretable feature importance

**ConCare** (`ConCare`)
- Cross-visit convolutional attention
- Temporal convolutional feature extraction
- Multi-level attention mechanism
- Good for longitudinal EHR modeling

### Medication Recommendation Models

**GAMENet** (`GAMENet`)
- Graph-based medication recommendation
- Drug-drug interaction modeling
- Memory network for patient history
- Multi-hop reasoning

**Architecture:**
- Drug knowledge graph
- Memory-augmented neural network
- DDI-aware prediction

**Usage:**
```python
from pyhealth.models import GAMENet

model = GAMENet(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="multilabel",
    embedding_dim=128,
    ddi_adj_path="/path/to/ddi_adjacency_matrix.pkl"
)
```

**MICRON** (`MICRON`)
- Medication recommendation with DDI constraints
- Interaction-aware predictions
- Safety-focused drug selection

**SafeDrug** (`SafeDrug`)
- Safety-aware drug recommendation
- Molecular structure integration
- DDI constraint optimization
- Balances efficacy and safety

**Key Features:**
- Molecular graph encoding
- DDI graph neural network
- Reinforcement learning for safety
- Published in KDD 2021

**Usage:**
```python
from pyhealth.models import SafeDrug

model = SafeDrug(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="multilabel",
    ddi_adj_path="/path/to/ddi_matrix.pkl",
    molecule_path="/path/to/molecule_graphs.pkl"
)
```

**MoleRec** (`MoleRec`)
- Molecular-level drug recommendations
- Sub-structure reasoning
- Fine-grained medication selection

### Disease Progression Models

**StageNet** (`StageNet`)
- Disease stage-aware prediction
- Learns clinical stages automatically
- Stage-adaptive feature extraction
- Effective for chronic disease monitoring

**Architecture:**
- Stage-aware LSTM
- Dynamic stage transitions
- Time-decay mechanism

**Usage:**
```python
from pyhealth.models import StageNet

model = StageNet(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    hidden_dim=128,
    num_stages=3,
    chunk_size=128
)
```

**Best for:**
- ICU mortality prediction
- Chronic disease progression
- Time-varying risk assessment

**Deepr** (`Deepr`)
- Deep recurrent architecture
- Medical concept embeddings
- Temporal pattern learning
- Published in JAMIA

### Advanced Sequential Models

**Agent** (`Agent`)
- Reinforcement learning-based
- Treatment recommendation
- Action-value optimization
- Policy learning for sequential decisions

**GRASP** (`GRASP`)
- Graph-based sequence patterns
- Structural event relationships
- Hierarchical representation learning

**SparcNet** (`SparcNet`)
- Sparse clinical networks
- Efficient feature selection
- Reduced computational cost
- Interpretable predictions

**ContraWR** (`ContraWR`)
- Contrastive learning approach
- Self-supervised pre-training
- Robust representations
- Limited labeled data scenarios

### Medical Entity Linking

**MedLink** (`MedLink`)
- Medical entity linking to knowledge bases
- Clinical concept normalization
- UMLS integration
- Entity disambiguation

### Generative Models

**GAN** (`GAN`)
- Generative Adversarial Networks
- Synthetic EHR data generation
- Privacy-preserving data sharing
- Augmentation for rare conditions

**VAE** (`VAE`)
- Variational Autoencoder
- Patient representation learning
- Anomaly detection
- Latent space exploration

### Social Determinants of Health

**SDOH** (`SDOH`)
- Social determinants integration
- Multi-modal prediction
- Addresses health disparities
- Combines clinical and social data

## Model Selection Guidelines

### By Task Type

**Binary Classification** (Mortality, Readmission)
- Start with: Logistic Regression (baseline)
- Standard: RNN, Transformer
- Interpretable: RETAIN, AdaCare
- Advanced: StageNet

**Multi-Label Classification** (Drug Recommendation)
- Standard: CNN, RNN
- Healthcare-specific: GAMENet, SafeDrug, MICRON, MoleRec
- Graph-based: GNN

**Regression** (Length of Stay)
- Start with: MLP (baseline)
- Sequential: RNN, TCN
- Advanced: Transformer

**Multi-Class Classification** (Medical Coding, Specialty)
- Standard: CNN, RNN, Transformer
- Text-based: TransformersModel (BERT variants)

### By Data Type

**Sequential Events** (Diagnoses, Medications, Procedures)
- RNN, LSTM, GRU
- Transformer
- RETAIN, AdaCare, ConCare

**Time-Series Signals** (EEG, ECG)
- CNN, TCN
- RNN
- Transformer

**Text** (Clinical Notes)
- TransformersModel (ClinicalBERT, BioBERT)
- CNN for shorter text
- RNN for sequential text

**Graphs** (Drug Interactions, Patient Networks)
- GNN (GAT, GCN)
- GAMENet, SafeDrug

**Images** (X-rays, CT scans)
- CNN (ResNet, DenseNet via TransformersModel)
- Vision Transformers

### By Interpretability Needs

**High Interpretability Required:**
- Logistic Regression
- RETAIN
- AdaCare
- SparcNet

**Moderate Interpretability:**
- CNN (filter visualization)
- Transformer (attention visualization)
- GNN (graph attention)

**Black-Box Acceptable:**
- Deep RNN models
- Complex ensembles

## Training Considerations

### Hyperparameter Tuning

**Embedding Dimension:**
- Small datasets: 64-128
- Large datasets: 128-256
- Complex tasks: 256-512

**Hidden Dimension:**
- Proportional to embedding_dim
- Typically 1-2x embedding_dim

**Number of Layers:**
- Start with 2-3 layers
- Deeper for complex patterns
- Watch for overfitting

**Dropout:**
- Start with 0.5
- Reduce if underfitting (0.1-0.3)
- Increase if overfitting (0.5-0.7)

### Computational Requirements

**Memory (GPU):**
- CNN: Low to moderate
- RNN: Moderate (sequence length dependent)
- Transformer: High (quadratic in sequence length)
- GNN: Moderate to high (graph size dependent)

**Training Speed:**
- Fastest: Logistic Regression, MLP, CNN
- Moderate: RNN, GNN
- Slower: Transformer (but parallelizable)

### Best Practices

1. **Start with simple baselines** (Logistic Regression, MLP)
2. **Use appropriate feature keys** based on data availability
3. **Match mode to task output** (binary, multiclass, multilabel, regression)
4. **Consider interpretability requirements** for clinical deployment
5. **Validate on held-out test set** for realistic performance
6. **Monitor for overfitting** especially with complex models
7. **Use pretrained models** when possible (TransformersModel)
8. **Consider computational constraints** for deployment

## Example Workflow

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Prepare data
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Initialize model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications", "procedures"],
    mode="binary",
    embedding_dim=128,
    num_heads=8,
    num_layers=3,
    dropout=0.3
)

# 3. Train model
trainer = Trainer(model=model)
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_score",
    monitor_criterion="max"
)

# 4. Evaluate
results = trainer.evaluate(test_loader)
print(results)
```

---

## Reference: Preprocessing

# PyHealth Data Preprocessing and Processors

## Overview

PyHealth provides comprehensive data processing utilities to transform raw healthcare data into model-ready formats. Processors handle feature extraction, sequence processing, signal transformation, and label preparation.

## Processor Base Class

All processors inherit from `Processor` with standard interface:

**Key Methods:**
- `__call__()`: Transform input data
- `get_input_info()`: Return processed input schema
- `get_output_info()`: Return processed output schema

## Core Processor Types

### Feature Processors

**FeatureProcessor** (`FeatureProcessor`)
- Base class for feature extraction
- Handles vocabulary building
- Embedding preparation
- Feature encoding

**Common Operations:**
- Medical code tokenization
- Categorical encoding
- Feature normalization
- Missing value handling

**Usage:**
```python
from pyhealth.data import FeatureProcessor

processor = FeatureProcessor(
    vocabulary="diagnoses",
    min_freq=5,  # Minimum code frequency
    max_vocab_size=10000
)

processed_features = processor(raw_features)
```

### Sequence Processors

**SequenceProcessor** (`SequenceProcessor`)
- Processes sequential clinical events
- Temporal ordering preservation
- Sequence padding/truncation
- Time gap encoding

**Key Features:**
- Variable-length sequence handling
- Temporal feature extraction
- Sequence statistics computation

**Parameters:**
- `max_seq_length`: Maximum sequence length (truncate if longer)
- `padding`: Padding strategy ("pre" or "post")
- `truncating`: Truncation strategy ("pre" or "post")

**Usage:**
```python
from pyhealth.data import SequenceProcessor

processor = SequenceProcessor(
    max_seq_length=100,
    padding="post",
    truncating="post"
)

# Process diagnosis sequences
processed_seq = processor(diagnosis_sequences)
```

**NestedSequenceProcessor** (`NestedSequenceProcessor`)
- Handles hierarchical sequences (e.g., visits containing events)
- Two-level processing (visit-level and event-level)
- Preserves nested structure

**Use Cases:**
- EHR with visits containing multiple events
- Multi-level temporal modeling
- Hierarchical attention models

**Structure:**
```python
# Input: [[visit1_events], [visit2_events], ...]
# Output: Processed nested sequences with proper padding
```

### Numeric Data Processors

**NestedFloatsProcessor** (`NestedFloatsProcessor`)
- Processes nested numeric arrays
- Lab values, vital signs, measurements
- Multi-level numeric features

**Operations:**
- Normalization
- Standardization
- Missing value imputation
- Outlier handling

**Usage:**
```python
from pyhealth.data import NestedFloatsProcessor

processor = NestedFloatsProcessor(
    normalization="z-score",  # or "min-max"
    fill_missing="mean"  # imputation strategy
)

processed_labs = processor(lab_values)
```

**TensorProcessor** (`TensorProcessor`)
- Converts data to PyTorch tensors
- Type handling (long, float, etc.)
- Device placement (CPU/GPU)

**Parameters:**
- `dtype`: Tensor data type
- `device`: Computation device

### Time-Series Processors

**TimeseriesProcessor** (`TimeseriesProcessor`)
- Handles temporal data with timestamps
- Time gap computation
- Temporal feature engineering
- Irregular sampling handling

**Extracted Features:**
- Time since previous event
- Time to next event
- Event frequency
- Temporal patterns

**Usage:**
```python
from pyhealth.data import TimeseriesProcessor

processor = TimeseriesProcessor(
    time_unit="hour",  # "day", "hour", "minute"
    compute_gaps=True,
    compute_frequency=True
)

processed_ts = processor(timestamps, events)
```

**SignalProcessor** (`SignalProcessor`)
- Physiological signal processing
- EEG, ECG, PPG signals
- Filtering and preprocessing

**Operations:**
- Bandpass filtering
- Artifact removal
- Segmentation
- Feature extraction (frequency, amplitude)

**Usage:**
```python
from pyhealth.data import SignalProcessor

processor = SignalProcessor(
    sampling_rate=256,  # Hz
    bandpass_filter=(0.5, 50),  # Hz range
    segment_length=30  # seconds
)

processed_signal = processor(raw_eeg_signal)
```

### Image Processors

**ImageProcessor** (`ImageProcessor`)
- Medical image preprocessing
- Normalization and resizing
- Augmentation support
- Format standardization

**Operations:**
- Resize to standard dimensions
- Normalization (mean/std)
- Windowing (for CT/MRI)
- Data augmentation

**Usage:**
```python
from pyhealth.data import ImageProcessor

processor = ImageProcessor(
    image_size=(224, 224),
    normalization="imagenet",  # or custom mean/std
    augmentation=True
)

processed_image = processor(raw_image)
```

## Label Processors

### Binary Classification

**BinaryLabelProcessor** (`BinaryLabelProcessor`)
- Binary classification labels (0/1)
- Handles positive/negative classes
- Class weighting for imbalance

**Usage:**
```python
from pyhealth.data import BinaryLabelProcessor

processor = BinaryLabelProcessor(
    positive_class=1,
    class_weight="balanced"
)

processed_labels = processor(raw_labels)
```

### Multi-Class Classification

**MultiClassLabelProcessor** (`MultiClassLabelProcessor`)
- Multi-class classification (mutually exclusive classes)
- Label encoding
- Class balancing

**Parameters:**
- `num_classes`: Number of classes
- `class_weight`: Weighting strategy

**Usage:**
```python
from pyhealth.data import MultiClassLabelProcessor

processor = MultiClassLabelProcessor(
    num_classes=5,  # e.g., sleep stages: W, N1, N2, N3, REM
    class_weight="balanced"
)

processed_labels = processor(raw_labels)
```

### Multi-Label Classification

**MultiLabelProcessor** (`MultiLabelProcessor`)
- Multi-label classification (multiple labels per sample)
- Binary encoding for each label
- Label co-occurrence handling

**Use Cases:**
- Drug recommendation (multiple drugs)
- ICD coding (multiple diagnoses)
- Comorbidity prediction

**Usage:**
```python
from pyhealth.data import MultiLabelProcessor

processor = MultiLabelProcessor(
    num_labels=100,  # total possible labels
    threshold=0.5  # prediction threshold
)

processed_labels = processor(raw_label_sets)
```

### Regression

**RegressionLabelProcessor** (`RegressionLabelProcessor`)
- Continuous value prediction
- Target scaling and normalization
- Outlier handling

**Use Cases:**
- Length of stay prediction
- Lab value prediction
- Risk score estimation

**Usage:**
```python
from pyhealth.data import RegressionLabelProcessor

processor = RegressionLabelProcessor(
    normalization="z-score",  # or "min-max"
    clip_outliers=True,
    outlier_std=3  # clip at 3 standard deviations
)

processed_targets = processor(raw_values)
```

## Specialized Processors

### Text Processing

**TextProcessor** (`TextProcessor`)
- Clinical text preprocessing
- Tokenization
- Vocabulary building
- Sequence encoding

**Operations:**
- Lowercasing
- Punctuation removal
- Medical abbreviation handling
- Token frequency filtering

**Usage:**
```python
from pyhealth.data import TextProcessor

processor = TextProcessor(
    tokenizer="word",  # or "sentencepiece", "bpe"
    lowercase=True,
    max_vocab_size=50000,
    min_freq=5
)

processed_text = processor(clinical_notes)
```

### Model-Specific Processors

**StageNetProcessor** (`StageNetProcessor`)
- Specialized preprocessing for StageNet model
- Chunk-based sequence processing
- Stage-aware feature extraction

**Usage:**
```python
from pyhealth.data import StageNetProcessor

processor = StageNetProcessor(
    chunk_size=128,
    num_stages=3
)

processed_data = processor(sequential_data)
```

**StageNetTensorProcessor** (`StageNetTensorProcessor`)
- Tensor conversion for StageNet
- Proper batching and padding
- Stage mask generation

### Raw Data Processing

**RawProcessor** (`RawProcessor`)
- Minimal preprocessing
- Pass-through for pre-processed data
- Custom preprocessing scenarios

**Usage:**
```python
from pyhealth.data import RawProcessor

processor = RawProcessor()
processed_data = processor(data)  # Minimal transformation
```

## Sample-Level Processing

**SampleProcessor** (`SampleProcessor`)
- Processes complete samples (input + output)
- Coordinates multiple processors
- End-to-end preprocessing pipeline

**Workflow:**
1. Apply input processors to features
2. Apply output processors to labels
3. Combine into model-ready samples

**Usage:**
```python
from pyhealth.data import SampleProcessor

processor = SampleProcessor(
    input_processors={
        "diagnoses": SequenceProcessor(max_seq_length=50),
        "medications": SequenceProcessor(max_seq_length=30),
        "labs": NestedFloatsProcessor(normalization="z-score")
    },
    output_processor=BinaryLabelProcessor()
)

processed_sample = processor(raw_sample)
```

## Dataset-Level Processing

**DatasetProcessor** (`DatasetProcessor`)
- Processes entire datasets
- Batch processing
- Parallel processing support
- Caching for efficiency

**Operations:**
- Apply processors to all samples
- Generate vocabulary from dataset
- Compute dataset statistics
- Save processed data

**Usage:**
```python
from pyhealth.data import DatasetProcessor

processor = DatasetProcessor(
    sample_processor=sample_processor,
    num_workers=4,  # parallel processing
    cache_dir="/path/to/cache"
)

processed_dataset = processor(raw_dataset)
```

## Common Preprocessing Workflows

### Workflow 1: EHR Mortality Prediction

```python
from pyhealth.data import (
    SequenceProcessor,
    BinaryLabelProcessor,
    SampleProcessor
)

# Define processors
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=50),
    "medications": SequenceProcessor(max_seq_length=30),
    "procedures": SequenceProcessor(max_seq_length=20)
}

output_processor = BinaryLabelProcessor(class_weight="balanced")

# Combine into sample processor
sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)

# Process dataset
processed_samples = [sample_processor(s) for s in raw_samples]
```

### Workflow 2: Sleep Staging from EEG

```python
from pyhealth.data import (
    SignalProcessor,
    MultiClassLabelProcessor,
    SampleProcessor
)

# Signal preprocessing
signal_processor = SignalProcessor(
    sampling_rate=100,
    bandpass_filter=(0.3, 35),  # EEG frequency range
    segment_length=30  # 30-second epochs
)

# Label processing
label_processor = MultiClassLabelProcessor(
    num_classes=5,  # W, N1, N2, N3, REM
    class_weight="balanced"
)

# Combine
sample_processor = SampleProcessor(
    input_processors={"signal": signal_processor},
    output_processor=label_processor
)
```

### Workflow 3: Drug Recommendation

```python
from pyhealth.data import (
    SequenceProcessor,
    MultiLabelProcessor,
    SampleProcessor
)

# Input processing
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=50),
    "previous_medications": SequenceProcessor(max_seq_length=40)
}

# Multi-label output (multiple drugs)
output_processor = MultiLabelProcessor(
    num_labels=150,  # number of possible drugs
    threshold=0.5
)

sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)
```

### Workflow 4: Length of Stay Prediction

```python
from pyhealth.data import (
    SequenceProcessor,
    NestedFloatsProcessor,
    RegressionLabelProcessor,
    SampleProcessor
)

# Process different feature types
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=30),
    "procedures": SequenceProcessor(max_seq_length=20),
    "labs": NestedFloatsProcessor(
        normalization="z-score",
        fill_missing="mean"
    )
}

# Regression target
output_processor = RegressionLabelProcessor(
    normalization="log",  # log-transform LOS
    clip_outliers=True
)

sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)
```

## Best Practices

### Sequence Processing

1. **Choose appropriate max_seq_length**: Balance between context and computation
   - Short sequences (20-50): Fast, less context
   - Medium sequences (50-100): Good balance
   - Long sequences (100+): More context, slower

2. **Truncation strategy**:
   - "post": Keep most recent events (recommended for clinical prediction)
   - "pre": Keep earliest events

3. **Padding strategy**:
   - "post": Pad at end (standard)
   - "pre": Pad at beginning

### Feature Encoding

1. **Vocabulary size**: Limit to frequent codes
   - `min_freq=5`: Include codes appearing ≥5 times
   - `max_vocab_size=10000`: Cap total vocabulary size

2. **Handle rare codes**: Group into "unknown" category

3. **Missing values**:
   - Imputation (mean, median, forward-fill)
   - Indicator variables
   - Special tokens

### Normalization

1. **Numeric features**: Always normalize
   - Z-score: Standard scaling (mean=0, std=1)
   - Min-max: Range scaling [0, 1]

2. **Compute statistics on training set only**: Prevent data leakage

3. **Apply same normalization to val/test sets**

### Class Imbalance

1. **Use class weighting**: `class_weight="balanced"`

2. **Consider oversampling**: For very rare positive cases

3. **Evaluate with appropriate metrics**: AUROC, AUPRC, F1

### Performance Optimization

1. **Cache processed data**: Save preprocessing results

2. **Parallel processing**: Use `num_workers` for DataLoader

3. **Batch processing**: Process multiple samples at once

4. **Feature selection**: Remove low-information features

### Validation

1. **Check processed shapes**: Ensure correct dimensions

2. **Verify value ranges**: After normalization

3. **Inspect samples**: Manually review processed data

4. **Monitor memory usage**: Especially for large datasets

## Troubleshooting

### Common Issues

**Memory Error:**
- Reduce `max_seq_length`
- Use smaller batches
- Process data in chunks
- Enable caching to disk

**Slow Processing:**
- Enable parallel processing (`num_workers`)
- Cache preprocessed data
- Reduce feature dimensionality
- Use more efficient data types

**Shape Mismatch:**
- Check sequence lengths
- Verify padding configuration
- Ensure consistent processor settings

**NaN Values:**
- Handle missing data explicitly
- Check normalization parameters
- Verify imputation strategy

**Class Imbalance:**
- Use class weighting
- Consider oversampling
- Adjust decision threshold
- Use appropriate evaluation metrics

---

## Reference: Tasks

# PyHealth Clinical Prediction Tasks

## Overview

PyHealth provides 20+ predefined clinical prediction tasks for common healthcare AI applications. Each task function transforms raw patient data into structured input-output pairs for model training.

## Task Function Structure

All task functions inherit from `BaseTask` and provide:

- **input_schema**: Defines input features (diagnoses, medications, labs, etc.)
- **output_schema**: Defines prediction targets (labels, values)
- **pre_filter()**: Optional patient/visit filtering logic

**Usage Pattern:**
```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn

dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
```

## Electronic Health Record (EHR) Tasks

### Mortality Prediction

**Purpose:** Predict patient death risk at next visit or within specified timeframe

**MIMIC-III Mortality** (`mortality_prediction_mimic3_fn`)
- Predicts death at next hospital visit
- Binary classification task
- Input: Historical diagnoses, procedures, medications
- Output: Binary label (deceased/alive)

**MIMIC-IV Mortality** (`mortality_prediction_mimic4_fn`)
- Updated version for MIMIC-IV dataset
- Enhanced feature set
- Improved label quality

**eICU Mortality** (`mortality_prediction_eicu_fn`)
- Multi-center ICU mortality prediction
- Accounts for hospital-level variation

**OMOP Mortality** (`mortality_prediction_omop_fn`)
- Standardized mortality prediction
- Works with OMOP common data model

**In-Hospital Mortality** (`inhospital_mortality_prediction_mimic4_fn`)
- Predicts death during current hospitalization
- Real-time risk assessment
- Earlier prediction window than next-visit mortality

**StageNet Mortality** (`mortality_prediction_mimic4_fn_stagenet`)
- Specialized for StageNet model architecture
- Temporal stage-aware prediction

### Hospital Readmission Prediction

**Purpose:** Identify patients at risk of hospital readmission within specified timeframe (typically 30 days)

**MIMIC-III Readmission** (`readmission_prediction_mimic3_fn`)
- 30-day readmission prediction
- Binary classification
- Input: Diagnosis history, medications, demographics
- Output: Binary label (readmitted/not readmitted)

**MIMIC-IV Readmission** (`readmission_prediction_mimic4_fn`)
- Enhanced readmission features
- Improved temporal modeling

**eICU Readmission** (`readmission_prediction_eicu_fn`)
- ICU-specific readmission risk
- Multi-site data

**OMOP Readmission** (`readmission_prediction_omop_fn`)
- Standardized readmission prediction

### Length of Stay Prediction

**Purpose:** Estimate hospital stay duration for resource planning and patient management

**MIMIC-III Length of Stay** (`length_of_stay_prediction_mimic3_fn`)
- Regression task
- Input: Admission diagnoses, vitals, demographics
- Output: Continuous value (days)

**MIMIC-IV Length of Stay** (`length_of_stay_prediction_mimic4_fn`)
- Enhanced features for LOS prediction
- Better temporal granularity

**eICU Length of Stay** (`length_of_stay_prediction_eicu_fn`)
- ICU stay duration prediction
- Multi-hospital data

**OMOP Length of Stay** (`length_of_stay_prediction_omop_fn`)
- Standardized LOS prediction

### Drug Recommendation

**Purpose:** Suggest appropriate medications based on patient history and current conditions

**MIMIC-III Drug Recommendation** (`drug_recommendation_mimic3_fn`)
- Multi-label classification
- Input: Diagnoses, previous medications, demographics
- Output: Set of recommended drug codes
- Considers drug-drug interactions

**MIMIC-IV Drug Recommendation** (`drug_recommendation_mimic4_fn`)
- Updated medication data
- Enhanced interaction modeling

**eICU Drug Recommendation** (`drug_recommendation_eicu_fn`)
- Critical care medication recommendations

**OMOP Drug Recommendation** (`drug_recommendation_omop_fn`)
- Standardized drug recommendation

**Key Considerations:**
- Handles polypharmacy scenarios
- Multi-label prediction (multiple drugs per patient)
- Can integrate with SafeDrug/GAMENet models for safety-aware recommendations

## Specialized Clinical Tasks

### Medical Coding

**MIMIC-III ICD-9 Coding** (`icd9_coding_mimic3_fn`)
- Assigns ICD-9 diagnosis/procedure codes to clinical notes
- Multi-label text classification
- Input: Clinical text/documentation
- Output: Set of ICD-9 codes
- Supports both diagnosis and procedure coding

### Patient Linkage

**MIMIC-III Patient Linking** (`patient_linkage_mimic3_fn`)
- Record matching and deduplication
- Binary classification (same patient or not)
- Input: Demographic and clinical features from two records
- Output: Match probability

## Physiological Signal Tasks

### Sleep Staging

**Purpose:** Classify sleep stages from EEG/physiological signals for sleep disorder diagnosis

**ISRUC Sleep Staging** (`sleep_staging_isruc_fn`)
- Multi-class classification (Wake, N1, N2, N3, REM)
- Input: Multi-channel EEG signals
- Output: Sleep stage per epoch (typically 30 seconds)

**SleepEDF Sleep Staging** (`sleep_staging_sleepedf_fn`)
- Standard sleep staging task
- PSG signal processing

**SHHS Sleep Staging** (`sleep_staging_shhs_fn`)
- Large-scale sleep study data
- Population-level sleep analysis

**Standardized Labels:**
- Wake (W)
- Non-REM Stage 1 (N1)
- Non-REM Stage 2 (N2)
- Non-REM Stage 3 (N3/Deep Sleep)
- REM (Rapid Eye Movement)

### EEG Analysis

**Abnormality Detection** (`abnormality_detection_tuab_fn`)
- Binary classification (normal/abnormal EEG)
- Clinical screening application
- Input: Multi-channel EEG recordings
- Output: Binary label

**Event Detection** (`event_detection_tuev_fn`)
- Identify specific EEG events (spikes, seizures)
- Multi-class classification
- Input: EEG time series
- Output: Event type and timing

**Seizure Detection** (`seizure_detection_tusz_fn`)
- Specialized epileptic seizure detection
- Critical for epilepsy monitoring
- Input: Continuous EEG
- Output: Seizure/non-seizure classification

## Medical Imaging Tasks

### COVID-19 Chest X-ray Classification

**COVID-19 CXR** (`covid_classification_cxr_fn`)
- Multi-class image classification
- Classes: COVID-19, bacterial pneumonia, viral pneumonia, normal
- Input: Chest X-ray images
- Output: Disease classification

## Text-Based Tasks

### Medical Transcription Classification

**Medical Specialty Classification** (`medical_transcription_classification_fn`)
- Classify clinical notes by medical specialty
- Multi-class text classification
- Input: Clinical transcription text
- Output: Medical specialty (Cardiology, Neurology, etc.)

## Custom Task Creation

### Creating Custom Tasks

Define custom prediction tasks by specifying input/output schemas:

```python
from pyhealth.tasks import BaseTask

def custom_task_fn(patient):
    """Custom prediction task"""

    # Define input features
    samples = []

    for i, visit in enumerate(patient.visits):
        # Skip if not enough history
        if i < 2:
            continue

        # Create input from historical visits
        input_info = {
            "diagnoses": [],
            "medications": [],
            "procedures": []
        }

        # Collect features from previous visits
        for past_visit in patient.visits[:i]:
            for event in past_visit.events:
                if event.vocabulary == "ICD10CM":
                    input_info["diagnoses"].append(event.code)
                elif event.vocabulary == "NDC":
                    input_info["medications"].append(event.code)

        # Define prediction target
        # Example: predict specific outcome at current visit
        output_info = {
            "label": 1 if some_condition else 0
        }

        samples.append({
            "patient_id": patient.patient_id,
            "visit_id": visit.visit_id,
            "input_info": input_info,
            "output_info": output_info
        })

    return samples

# Apply custom task
sample_dataset = dataset.set_task(custom_task_fn)
```

### Task Function Components

1. **Input Schema Definition**
   - Specify which features to extract
   - Define feature types (codes, sequences, values)
   - Set temporal windows

2. **Output Schema Definition**
   - Define prediction targets
   - Set label types (binary, multi-class, multi-label, regression)
   - Specify evaluation metrics

3. **Filtering Logic**
   - Exclude patients/visits with insufficient data
   - Apply inclusion/exclusion criteria
   - Handle missing data

4. **Sample Generation**
   - Create input-output pairs
   - Maintain patient/visit identifiers
   - Preserve temporal ordering

## Task Selection Guidelines

### Clinical Prediction Tasks
**Use when:** Working with structured EHR data (diagnoses, medications, procedures)

**Datasets:** MIMIC-III, MIMIC-IV, eICU, OMOP

**Common tasks:**
- Mortality prediction for risk stratification
- Readmission prediction for care transition planning
- Length of stay for resource allocation
- Drug recommendation for clinical decision support

### Signal Processing Tasks
**Use when:** Working with physiological time-series data

**Datasets:** SleepEDF, SHHS, ISRUC, TUEV, TUAB, TUSZ

**Common tasks:**
- Sleep staging for sleep disorder diagnosis
- EEG abnormality detection for screening
- Seizure detection for epilepsy monitoring

### Imaging Tasks
**Use when:** Working with medical images

**Datasets:** COVID-19 CXR

**Common tasks:**
- Disease classification from radiographs
- Abnormality detection

### Text Tasks
**Use when:** Working with clinical notes and documentation

**Datasets:** Medical Transcriptions, MIMIC-III (with notes)

**Common tasks:**
- Medical coding from clinical text
- Specialty classification
- Clinical information extraction

## Task Output Structure

All task functions return `SampleDataset` with:

```python
sample = {
    "patient_id": "unique_patient_id",
    "visit_id": "unique_visit_id",  # if applicable
    "input_info": {
        # Input features (diagnoses, medications, etc.)
    },
    "output_info": {
        # Prediction targets (labels, values)
    }
}
```

## Integration with Models

Tasks define the input/output contract for models:

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.models import Transformer

# 1. Create task-specific dataset
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Model automatically adapts to task schema
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",  # matches task output
)
```

## Best Practices

1. **Match task to clinical question**: Choose predefined tasks when available for standardized benchmarking

2. **Consider temporal windows**: Ensure sufficient history for meaningful predictions

3. **Handle class imbalance**: Many clinical outcomes are rare (mortality, readmission)

4. **Validate clinical relevance**: Ensure prediction windows align with clinical decision-making timelines

5. **Use appropriate metrics**: Different tasks require different evaluation metrics (AUROC for binary, macro-F1 for multi-class)

6. **Document exclusion criteria**: Track which patients/visits are filtered and why

7. **Preserve patient privacy**: Always use de-identified data and follow HIPAA/GDPR guidelines

---

## Reference: Training_Evaluation

# PyHealth Training, Evaluation, and Interpretability

## Overview

PyHealth provides comprehensive tools for training models, evaluating predictions, ensuring model reliability, and interpreting results for clinical applications.

## Trainer Class

### Core Functionality

The `Trainer` class manages the complete model training and evaluation workflow with PyTorch integration.

**Initialization:**
```python
from pyhealth.trainer import Trainer

trainer = Trainer(
    model=model,  # PyHealth or PyTorch model
    device="cuda",  # or "cpu"
)
```

### Training

**train() method**

Trains models with comprehensive monitoring and checkpointing.

**Parameters:**
- `train_dataloader`: Training data loader
- `val_dataloader`: Validation data loader (optional)
- `test_dataloader`: Test data loader (optional)
- `epochs`: Number of training epochs
- `optimizer`: Optimizer instance or class
- `learning_rate`: Learning rate (default: 1e-3)
- `weight_decay`: L2 regularization (default: 0)
- `max_grad_norm`: Gradient clipping threshold
- `monitor`: Metric to monitor (e.g., "pr_auc_score")
- `monitor_criterion`: "max" or "min"
- `save_path`: Checkpoint save directory

**Usage:**
```python
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    test_dataloader=test_loader,
    epochs=50,
    optimizer=torch.optim.Adam,
    learning_rate=1e-3,
    weight_decay=1e-5,
    max_grad_norm=5.0,
    monitor="pr_auc_score",
    monitor_criterion="max",
    save_path="./checkpoints"
)
```

**Training Features:**

1. **Automatic Checkpointing**: Saves best model based on monitored metric

2. **Early Stopping**: Stops training if no improvement

3. **Gradient Clipping**: Prevents exploding gradients

4. **Progress Tracking**: Displays training progress and metrics

5. **Multi-GPU Support**: Automatic device placement

### Inference

**inference() method**

Performs predictions on datasets.

**Parameters:**
- `dataloader`: Data loader for inference
- `additional_outputs`: List of additional outputs to return
- `return_patient_ids`: Return patient identifiers

**Usage:**
```python
predictions = trainer.inference(
    dataloader=test_loader,
    additional_outputs=["attention_weights", "embeddings"],
    return_patient_ids=True
)
```

**Returns:**
- `y_pred`: Model predictions
- `y_true`: Ground truth labels
- `patient_ids`: Patient identifiers (if requested)
- Additional outputs (if specified)

### Evaluation

**evaluate() method**

Computes comprehensive evaluation metrics.

**Parameters:**
- `dataloader`: Data loader for evaluation
- `metrics`: List of metric functions

**Usage:**
```python
from pyhealth.metrics import binary_metrics_fn

results = trainer.evaluate(
    dataloader=test_loader,
    metrics=["accuracy", "pr_auc_score", "roc_auc_score", "f1_score"]
)

print(results)
# Output: {'accuracy': 0.85, 'pr_auc_score': 0.78, 'roc_auc_score': 0.82, 'f1_score': 0.73}
```

### Checkpoint Management

**save() method**
```python
trainer.save("./models/best_model.pt")
```

**load() method**
```python
trainer.load("./models/best_model.pt")
```

## Evaluation Metrics

### Binary Classification Metrics

**Available Metrics:**
- `accuracy`: Overall accuracy
- `precision`: Positive predictive value
- `recall`: Sensitivity/True positive rate
- `f1_score`: F1 score (harmonic mean of precision and recall)
- `roc_auc_score`: Area under ROC curve
- `pr_auc_score`: Area under precision-recall curve
- `cohen_kappa`: Inter-rater reliability

**Usage:**
```python
from pyhealth.metrics import binary_metrics_fn

# Comprehensive binary metrics
metrics = binary_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    metrics=["accuracy", "f1_score", "pr_auc_score", "roc_auc_score"]
)
```

**Threshold Selection:**
```python
# Default threshold: 0.5
predictions_binary = (predictions > 0.5).astype(int)

# Optimal threshold by F1
from sklearn.metrics import f1_score
thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = [f1_score(y_true, (y_pred > t).astype(int)) for t in thresholds]
optimal_threshold = thresholds[np.argmax(f1_scores)]
```

**Best Practices:**
- **Use AUROC**: Overall model discrimination
- **Use AUPRC**: Especially for imbalanced classes
- **Use F1**: Balance precision and recall
- **Report confidence intervals**: Bootstrap resampling

### Multi-Class Classification Metrics

**Available Metrics:**
- `accuracy`: Overall accuracy
- `macro_f1`: Unweighted mean F1 across classes
- `micro_f1`: Global F1 (total TP, FP, FN)
- `weighted_f1`: Weighted mean F1 by class frequency
- `cohen_kappa`: Multi-class kappa

**Usage:**
```python
from pyhealth.metrics import multiclass_metrics_fn

metrics = multiclass_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    metrics=["accuracy", "macro_f1", "weighted_f1"]
)
```

**Per-Class Metrics:**
```python
from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred,
    target_names=["Wake", "N1", "N2", "N3", "REM"]))
```

**Confusion Matrix:**
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
```

### Multi-Label Classification Metrics

**Available Metrics:**
- `jaccard_score`: Intersection over union
- `hamming_loss`: Fraction of incorrect labels
- `example_f1`: F1 per example (micro average)
- `label_f1`: F1 per label (macro average)

**Usage:**
```python
from pyhealth.metrics import multilabel_metrics_fn

# y_pred: [n_samples, n_labels] binary matrix
metrics = multilabel_metrics_fn(
    y_true=label_matrix,
    y_pred=pred_matrix,
    metrics=["jaccard_score", "example_f1", "label_f1"]
)
```

**Drug Recommendation Metrics:**
```python
# Jaccard similarity (intersection/union)
jaccard = len(set(true_drugs) & set(pred_drugs)) / len(set(true_drugs) | set(pred_drugs))

# Precision@k: Precision for top-k predictions
def precision_at_k(y_true, y_pred, k=10):
    top_k_pred = y_pred.argsort()[-k:]
    return len(set(y_true) & set(top_k_pred)) / k
```

### Regression Metrics

**Available Metrics:**
- `mean_absolute_error`: Average absolute error
- `mean_squared_error`: Average squared error
- `root_mean_squared_error`: RMSE
- `r2_score`: Coefficient of determination

**Usage:**
```python
from pyhealth.metrics import regression_metrics_fn

metrics = regression_metrics_fn(
    y_true=true_values,
    y_pred=predictions,
    metrics=["mae", "rmse", "r2"]
)
```

**Percentage Error Metrics:**
```python
# Mean Absolute Percentage Error
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Median Absolute Percentage Error (robust to outliers)
medape = np.median(np.abs((y_true - y_pred) / y_true)) * 100
```

### Fairness Metrics

**Purpose:** Assess model bias across demographic groups

**Available Metrics:**
- `demographic_parity`: Equal positive prediction rates
- `equalized_odds`: Equal TPR and FPR across groups
- `equal_opportunity`: Equal TPR across groups
- `predictive_parity`: Equal PPV across groups

**Usage:**
```python
from pyhealth.metrics import fairness_metrics_fn

fairness_results = fairness_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    sensitive_attributes=demographics,  # e.g., race, gender
    metrics=["demographic_parity", "equalized_odds"]
)
```

**Example:**
```python
# Evaluate fairness across gender
male_mask = (demographics == "male")
female_mask = (demographics == "female")

male_tpr = recall_score(y_true[male_mask], y_pred[male_mask])
female_tpr = recall_score(y_true[female_mask], y_pred[female_mask])

tpr_disparity = abs(male_tpr - female_tpr)
print(f"TPR disparity: {tpr_disparity:.3f}")
```

## Calibration and Uncertainty Quantification

### Model Calibration

**Purpose:** Ensure predicted probabilities match actual frequencies

**Calibration Plot:**
```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

fraction_of_positives, mean_predicted_value = calibration_curve(
    y_true, y_prob, n_bins=10
)

plt.plot(mean_predicted_value, fraction_of_positives, marker='o')
plt.plot([0, 1], [0, 1], linestyle='--', label='Perfect calibration')
plt.xlabel('Mean predicted probability')
plt.ylabel('Fraction of positives')
plt.legend()
```

**Expected Calibration Error (ECE):**
```python
def expected_calibration_error(y_true, y_prob, n_bins=10):
    """Compute ECE"""
    bins = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins) - 1

    ece = 0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracy = y_true[mask].mean()
            bin_confidence = y_prob[mask].mean()
            ece += mask.sum() / len(y_true) * abs(bin_accuracy - bin_confidence)

    return ece
```

**Calibration Methods:**

1. **Platt Scaling**: Logistic regression on validation predictions
```python
from sklearn.linear_model import LogisticRegression

calibrator = LogisticRegression()
calibrator.fit(val_predictions.reshape(-1, 1), val_labels)
calibrated_probs = calibrator.predict_proba(test_predictions.reshape(-1, 1))[:, 1]
```

2. **Isotonic Regression**: Non-parametric calibration
```python
from sklearn.isotonic import IsotonicRegression

calibrator = IsotonicRegression(out_of_bounds='clip')
calibrator.fit(val_predictions, val_labels)
calibrated_probs = calibrator.predict(test_predictions)
```

3. **Temperature Scaling**: Scale logits before softmax
```python
def find_temperature(logits, labels):
    """Find optimal temperature parameter"""
    from scipy.optimize import minimize

    def nll(temp):
        scaled_logits = logits / temp
        probs = torch.softmax(scaled_logits, dim=1)
        return F.cross_entropy(probs, labels).item()

    result = minimize(nll, x0=1.0, method='BFGS')
    return result.x[0]

temperature = find_temperature(val_logits, val_labels)
calibrated_logits = test_logits / temperature
```

### Uncertainty Quantification

**Conformal Prediction:**

Provide prediction sets with guaranteed coverage.

**Usage:**
```python
from pyhealth.metrics import prediction_set_metrics_fn

# Calibrate on validation set
scores = 1 - val_predictions[np.arange(len(val_labels)), val_labels]
quantile_level = np.quantile(scores, 0.9)  # 90% coverage

# Generate prediction sets on test set
prediction_sets = test_predictions > (1 - quantile_level)

# Evaluate
metrics = prediction_set_metrics_fn(
    y_true=test_labels,
    prediction_sets=prediction_sets,
    metrics=["coverage", "average_size"]
)
```

**Monte Carlo Dropout:**

Estimate uncertainty through dropout at inference.

```python
def predict_with_uncertainty(model, dataloader, num_samples=20):
    """Predict with uncertainty using MC dropout"""
    model.train()  # Keep dropout active

    predictions = []
    for _ in range(num_samples):
        batch_preds = []
        for batch in dataloader:
            with torch.no_grad():
                output = model(batch)
                batch_preds.append(output)
        predictions.append(torch.cat(batch_preds))

    predictions = torch.stack(predictions)
    mean_pred = predictions.mean(dim=0)
    std_pred = predictions.std(dim=0)  # Uncertainty

    return mean_pred, std_pred
```

**Ensemble Uncertainty:**

```python
# Train multiple models
models = [train_model(seed=i) for i in range(5)]

# Predict with ensemble
ensemble_preds = []
for model in models:
    pred = model.predict(test_data)
    ensemble_preds.append(pred)

mean_pred = np.mean(ensemble_preds, axis=0)
std_pred = np.std(ensemble_preds, axis=0)  # Uncertainty
```

## Interpretability

### Attention Visualization

**For Transformer and RETAIN models:**

```python
# Get attention weights during inference
outputs = trainer.inference(
    test_loader,
    additional_outputs=["attention_weights"]
)

attention = outputs["attention_weights"]

# Visualize attention for sample
import matplotlib.pyplot as plt
import seaborn as sns

sample_idx = 0
sample_attention = attention[sample_idx]  # [seq_length, seq_length]

sns.heatmap(sample_attention, cmap='viridis')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.title('Attention Weights')
plt.show()
```

**RETAIN Interpretation:**

```python
# RETAIN provides visit-level and feature-level attention
visit_attention = outputs["visit_attention"]  # Which visits are important
feature_attention = outputs["feature_attention"]  # Which features are important

# Find most influential visit
most_important_visit = visit_attention[sample_idx].argmax()

# Find most influential features in that visit
important_features = feature_attention[sample_idx, most_important_visit].argsort()[-10:]
```

### Feature Importance

**Permutation Importance:**

```python
from sklearn.inspection import permutation_importance

def get_predictions(model, X):
    return model.predict(X)

result = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    scoring='roc_auc'
)

# Sort features by importance
indices = result.importances_mean.argsort()[::-1]
for i in indices[:10]:
    print(f"{feature_names[i]}: {result.importances_mean[i]:.3f}")
```

**SHAP Values:**

```python
import shap

# Create explainer
explainer = shap.DeepExplainer(model, train_data)

# Compute SHAP values
shap_values = explainer.shap_values(test_data)

# Visualize
shap.summary_plot(shap_values, test_data, feature_names=feature_names)
```

### ChEFER (Clinical Health Event Feature Extraction and Ranking)

**PyHealth's Interpretability Tool:**

```python
from pyhealth.explain import ChEFER

explainer = ChEFER(model=model, dataset=test_dataset)

# Get feature importance for prediction
importance_scores = explainer.explain(
    patient_id="patient_123",
    visit_id="visit_456"
)

# Visualize top features
explainer.plot_importance(importance_scores, top_k=20)
```

## Complete Training Pipeline Example

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer
from pyhealth.metrics import binary_metrics_fn

# 1. Load and prepare data
dataset = MIMIC4Dataset(root="/path/to/mimic4")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Split data
train_data, val_data, test_data = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 3. Create data loaders
train_loader = get_dataloader(train_data, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_data, batch_size=64, shuffle=False)
test_loader = get_dataloader(test_data, batch_size=64, shuffle=False)

# 4. Initialize model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    num_heads=8,
    num_layers=3,
    dropout=0.3
)

# 5. Train model
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer=torch.optim.Adam,
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",
    monitor_criterion="max",
    save_path="./checkpoints/mortality_model"
)

# 6. Evaluate on test set
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("Test Results:")
for metric, value in test_results.items():
    print(f"{metric}: {value:.4f}")

# 7. Get predictions for analysis
predictions = trainer.inference(test_loader, return_patient_ids=True)
y_pred, y_true, patient_ids = predictions

# 8. Calibration analysis
from sklearn.calibration import calibration_curve

fraction_pos, mean_pred = calibration_curve(y_true, y_pred, n_bins=10)
ece = expected_calibration_error(y_true, y_pred)
print(f"Expected Calibration Error: {ece:.4f}")

# 9. Save final model
trainer.save("./models/mortality_transformer_final.pt")
```

## Best Practices

### Training

1. **Monitor multiple metrics**: Track both loss and task-specific metrics
2. **Use validation set**: Prevent overfitting with early stopping
3. **Gradient clipping**: Stabilize training (max_grad_norm=5.0)
4. **Learning rate scheduling**: Reduce LR on plateau
5. **Checkpoint best model**: Save based on validation performance

### Evaluation

1. **Use task-appropriate metrics**: AUROC/AUPRC for binary, macro-F1 for imbalanced multi-class
2. **Report confidence intervals**: Bootstrap or cross-validation
3. **Stratified evaluation**: Report metrics by subgroups
4. **Clinical metrics**: Include clinically relevant thresholds
5. **Fairness assessment**: Evaluate across demographic groups

### Deployment

1. **Calibrate predictions**: Ensure probabilities are reliable
2. **Quantify uncertainty**: Provide confidence estimates
3. **Monitor performance**: Track metrics in production
4. **Handle distribution shift**: Detect when data changes
5. **Interpretability**: Provide explanations for predictions
