---
title: "Scikit Survival"
description: "Comprehensive toolkit for survival analysis and time-to-event modeling in Python using scikit-survival. Use this skill when working with censored survival data, performing time-to-event analysis, fitting Cox models, Random Survival Forests, Gradie..."
category: "development"
source: "community"
author: "Community"
tags: ["scikit", "survival"]
date: 2026-03-20
---

# scikit-survival: Survival Analysis in Python

## Overview

scikit-survival is a Python library for survival analysis built on top of scikit-learn. It provides specialized tools for time-to-event analysis, handling the unique challenge of censored data where some observations are only partially known.

Survival analysis aims to establish connections between covariates and the time of an event, accounting for censored records (particularly right-censored data from studies where participants don't experience events during observation periods).

## When to Use This Skill

Use this skill when:
- Performing survival analysis or time-to-event modeling
- Working with censored data (right-censored, left-censored, or interval-censored)
- Fitting Cox proportional hazards models (standard or penalized)
- Building ensemble survival models (Random Survival Forests, Gradient Boosting)
- Training Survival Support Vector Machines
- Evaluating survival model performance (concordance index, Brier score, time-dependent AUC)
- Estimating Kaplan-Meier or Nelson-Aalen curves
- Analyzing competing risks
- Preprocessing survival data or handling missing values in survival datasets
- Conducting any analysis using the scikit-survival library

## Core Capabilities

### 1. Model Types and Selection

scikit-survival provides multiple model families, each suited for different scenarios:

#### Cox Proportional Hazards Models
**Use for**: Standard survival analysis with interpretable coefficients
- `CoxPHSurvivalAnalysis`: Basic Cox model
- `CoxnetSurvivalAnalysis`: Penalized Cox with elastic net for high-dimensional data
- `IPCRidge`: Ridge regression for accelerated failure time models

**See**: `references/cox-models.md` for detailed guidance on Cox models, regularization, and interpretation

#### Ensemble Methods
**Use for**: High predictive performance with complex non-linear relationships
- `RandomSurvivalForest`: Robust, non-parametric ensemble method
- `GradientBoostingSurvivalAnalysis`: Tree-based boosting for maximum performance
- `ComponentwiseGradientBoostingSurvivalAnalysis`: Linear boosting with feature selection
- `ExtraSurvivalTrees`: Extremely randomized trees for additional regularization

**See**: `references/ensemble-models.md` for comprehensive guidance on ensemble methods, hyperparameter tuning, and when to use each model

#### Survival Support Vector Machines
**Use for**: Medium-sized datasets with margin-based learning
- `FastSurvivalSVM`: Linear SVM optimized for speed
- `FastKernelSurvivalSVM`: Kernel SVM for non-linear relationships
- `HingeLossSurvivalSVM`: SVM with hinge loss
- `ClinicalKernelTransform`: Specialized kernel for clinical + molecular data

**See**: `references/svm-models.md` for detailed SVM guidance, kernel selection, and hyperparameter tuning

#### Model Selection Decision Tree

```
Start
├─ High-dimensional data (p > n)?
│  ├─ Yes → CoxnetSurvivalAnalysis (elastic net)
│  └─ No → Continue
│
├─ Need interpretable coefficients?
│  ├─ Yes → CoxPHSurvivalAnalysis or ComponentwiseGradientBoostingSurvivalAnalysis
│  └─ No → Continue
│
├─ Complex non-linear relationships expected?
│  ├─ Yes
│  │  ├─ Large dataset (n > 1000) → GradientBoostingSurvivalAnalysis
│  │  ├─ Medium dataset → RandomSurvivalForest or FastKernelSurvivalSVM
│  │  └─ Small dataset → RandomSurvivalForest
│  └─ No → CoxPHSurvivalAnalysis or FastSurvivalSVM
│
└─ For maximum performance → Try multiple models and compare
```

### 2. Data Preparation and Preprocessing

Before modeling, properly prepare survival data:

#### Creating Survival Outcomes
```python
from sksurv.util import Surv

# From separate arrays
y = Surv.from_arrays(event=event_array, time=time_array)

# From DataFrame
y = Surv.from_dataframe('event', 'time', df)
```

#### Essential Preprocessing Steps
1. **Handle missing values**: Imputation strategies for features
2. **Encode categorical variables**: One-hot encoding or label encoding
3. **Standardize features**: Critical for SVMs and regularized Cox models
4. **Validate data quality**: Check for negative times, sufficient events per feature
5. **Train-test split**: Maintain similar censoring rates across splits

**See**: `references/data-handling.md` for complete preprocessing workflows, data validation, and best practices

### 3. Model Evaluation

Proper evaluation is critical for survival models. Use appropriate metrics that account for censoring:

#### Concordance Index (C-index)
Primary metric for ranking/discrimination:
- **Harrell's C-index**: Use for low censoring (<40%)
- **Uno's C-index**: Use for moderate to high censoring (>40%) - more robust

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# Harrell's C-index
c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# Uno's C-index (recommended)
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

#### Time-Dependent AUC
Evaluate discrimination at specific time points:

```python
from sksurv.metrics import cumulative_dynamic_auc

times = [365, 730, 1095]  # 1, 2, 3 years
auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)
```

#### Brier Score
Assess both discrimination and calibration:

```python
from sksurv.metrics import integrated_brier_score

ibs = integrated_brier_score(y_train, y_test, survival_functions, times)
```

**See**: `references/evaluation-metrics.md` for comprehensive evaluation guidance, metric selection, and using scorers with cross-validation

### 4. Competing Risks Analysis

Handle situations with multiple mutually exclusive event types:

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks

# Estimate cumulative incidence for each event type
time_points, cif_event1, cif_event2 = cumulative_incidence_competing_risks(y)
```

**Use competing risks when**:
- Multiple mutually exclusive event types exist (e.g., death from different causes)
- Occurrence of one event prevents others
- Need probability estimates for specific event types

**See**: `references/competing-risks.md` for detailed competing risks methods, cause-specific hazard models, and interpretation

### 5. Non-parametric Estimation

Estimate survival functions without parametric assumptions:

#### Kaplan-Meier Estimator
```python
from sksurv.nonparametric import kaplan_meier_estimator

time, survival_prob = kaplan_meier_estimator(y['event'], y['time'])
```

#### Nelson-Aalen Estimator
```python
from sksurv.nonparametric import nelson_aalen_estimator

time, cumulative_hazard = nelson_aalen_estimator(y['event'], y['time'])
```

## Typical Workflows

### Workflow 1: Standard Survival Analysis

```python
from sksurv.datasets import load_breast_cancer
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_ipcw
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load and prepare data
X, y = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Preprocess
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Fit model
estimator = CoxPHSurvivalAnalysis()
estimator.fit(X_train_scaled, y_train)

# 4. Predict
risk_scores = estimator.predict(X_test_scaled)

# 5. Evaluate
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"C-index: {c_index:.3f}")
```

### Workflow 2: High-Dimensional Data with Feature Selection

```python
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import as_concordance_index_ipcw_scorer

# 1. Use penalized Cox for feature selection
estimator = CoxnetSurvivalAnalysis(l1_ratio=0.9)  # Lasso-like

# 2. Tune regularization with cross-validation
param_grid = {'alpha_min_ratio': [0.01, 0.001]}
cv = GridSearchCV(estimator, param_grid,
                  scoring=as_concordance_index_ipcw_scorer(), cv=5)
cv.fit(X, y)

# 3. Identify selected features
best_model = cv.best_estimator_
selected_features = np.where(best_model.coef_ != 0)[0]
```

### Workflow 3: Ensemble Method for Maximum Performance

```python
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import GridSearchCV

# 1. Define parameter grid
param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7]
}

# 2. Grid search
gbs = GradientBoostingSurvivalAnalysis()
cv = GridSearchCV(gbs, param_grid, cv=5,
                  scoring=as_concordance_index_ipcw_scorer(), n_jobs=-1)
cv.fit(X_train, y_train)

# 3. Evaluate best model
best_model = cv.best_estimator_
risk_scores = best_model.predict(X_test)
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

### Workflow 4: Comprehensive Model Comparison

```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM
from sksurv.metrics import concordance_index_ipcw, integrated_brier_score

# Define models
models = {
    'Cox': CoxPHSurvivalAnalysis(),
    'RSF': RandomSurvivalForest(n_estimators=100, random_state=42),
    'GBS': GradientBoostingSurvivalAnalysis(random_state=42),
    'SVM': FastSurvivalSVM(random_state=42)
}

# Evaluate each model
results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    risk_scores = model.predict(X_test_scaled)
    c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
    results[name] = c_index
    print(f"{name}: C-index = {c_index:.3f}")

# Select best model
best_model_name = max(results, key=results.get)
print(f"\nBest model: {best_model_name}")
```

## Integration with scikit-learn

scikit-survival fully integrates with scikit-learn's ecosystem:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, GridSearchCV

# Use pipelines
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', CoxPHSurvivalAnalysis())
])

# Use cross-validation
scores = cross_val_score(pipeline, X, y, cv=5,
                         scoring=as_concordance_index_ipcw_scorer())

# Use grid search
param_grid = {'model__alpha': [0.1, 1.0, 10.0]}
cv = GridSearchCV(pipeline, param_grid, cv=5)
cv.fit(X, y)
```

## Best Practices

1. **Always standardize features** for SVMs and regularized Cox models
2. **Use Uno's C-index** instead of Harrell's when censoring > 40%
3. **Report multiple evaluation metrics** (C-index, integrated Brier score, time-dependent AUC)
4. **Check proportional hazards assumption** for Cox models
5. **Use cross-validation** for hyperparameter tuning with appropriate scorers
6. **Validate data quality** before modeling (check for negative times, sufficient events per feature)
7. **Compare multiple model types** to find best performance
8. **Use permutation importance** for Random Survival Forests (not built-in importance)
9. **Consider competing risks** when multiple event types exist
10. **Document censoring mechanism** and rates in analysis

## Common Pitfalls to Avoid

1. **Using Harrell's C-index with high censoring** → Use Uno's C-index
2. **Not standardizing features for SVMs** → Always standardize
3. **Forgetting to pass y_train to concordance_index_ipcw** → Required for IPCW calculation
4. **Treating competing events as censored** → Use competing risks methods
5. **Not checking for sufficient events per feature** → Rule of thumb: 10+ events per feature
6. **Using built-in feature importance for RSF** → Use permutation importance
7. **Ignoring proportional hazards assumption** → Validate or use alternative models
8. **Not using appropriate scorers in cross-validation** → Use as_concordance_index_ipcw_scorer()

## Reference Files

This skill includes detailed reference files for specific topics:

- **`references/cox-models.md`**: Complete guide to Cox proportional hazards models, penalized Cox (CoxNet), IPCRidge, regularization strategies, and interpretation
- **`references/ensemble-models.md`**: Random Survival Forests, Gradient Boosting, hyperparameter tuning, feature importance, and model selection
- **`references/evaluation-metrics.md`**: Concordance index (Harrell's vs Uno's), time-dependent AUC, Brier score, comprehensive evaluation pipelines
- **`references/data-handling.md`**: Data loading, preprocessing workflows, handling missing data, feature encoding, validation checks
- **`references/svm-models.md`**: Survival Support Vector Machines, kernel selection, clinical kernel transform, hyperparameter tuning
- **`references/competing-risks.md`**: Competing risks analysis, cumulative incidence functions, cause-specific hazard models

Load these reference files when detailed information is needed for specific tasks.

## Additional Resources

- **Official Documentation**: https://scikit-survival.readthedocs.io/
- **GitHub Repository**: https://github.com/sebp/scikit-survival
- **Built-in Datasets**: Use `sksurv.datasets` for practice datasets (GBSG2, WHAS500, veterans lung cancer, etc.)
- **API Reference**: Complete list of classes and functions at https://scikit-survival.readthedocs.io/en/stable/api/index.html

## Quick Reference: Key Imports

```python
# Models
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis, IPCRidge
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM, FastKernelSurvivalSVM
from sksurv.tree import SurvivalTree

# Evaluation metrics
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    brier_score,
    integrated_brier_score,
    as_concordance_index_ipcw_scorer,
    as_integrated_brier_score_scorer
)

# Non-parametric estimation
from sksurv.nonparametric import (
    kaplan_meier_estimator,
    nelson_aalen_estimator,
    cumulative_incidence_competing_risks
)

# Data handling
from sksurv.util import Surv
from sksurv.preprocessing import OneHotEncoder, encode_categorical
from sksurv.datasets import load_gbsg2, load_breast_cancer, load_veterans_lung_cancer

# Kernels
from sksurv.kernels import ClinicalKernelTransform
```

---

## Reference: Competing Risks

# Competing Risks Analysis

## Overview

Competing risks occur when subjects can experience one of several mutually exclusive events (event types). When one event occurs, it prevents ("competes with") the occurrence of other events.

### Examples of Competing Risks

**Medical Research:**
- Death from cancer vs. death from cardiovascular disease vs. death from other causes
- Relapse vs. death without relapse in cancer studies
- Different types of infections in transplant patients

**Other Applications:**
- Job termination: retirement vs. resignation vs. termination for cause
- Equipment failure: different failure modes
- Customer churn: different reasons for leaving

### Key Concept: Cumulative Incidence Function (CIF)

The **Cumulative Incidence Function (CIF)** represents the probability of experiencing a specific event type by time *t*, accounting for the presence of competing risks.

**CIF_k(t) = P(T ≤ t, event type = k)**

This differs from the Kaplan-Meier estimator, which would overestimate event probabilities when competing risks are present.

## When to Use Competing Risks Analysis

**Use competing risks when:**
- Multiple mutually exclusive event types exist
- Occurrence of one event prevents others
- Need to estimate probability of specific event types
- Want to understand how covariates affect different event types

**Don't use when:**
- Only one event type of interest (standard survival analysis)
- Events are not mutually exclusive (use recurrent events methods)
- Competing events are extremely rare (can treat as censoring)

## Cumulative Incidence with Competing Risks

### cumulative_incidence_competing_risks Function

Estimates the cumulative incidence function for each event type.

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks
from sksurv.datasets import load_leukemia

# Load data with competing risks
X, y = load_leukemia()
# y has event types: 0=censored, 1=relapse, 2=death

# Compute cumulative incidence for each event type
# Returns: time points, CIF for event 1, CIF for event 2, ...
time_points, cif_1, cif_2 = cumulative_incidence_competing_risks(y)

# Plot cumulative incidence functions
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.step(time_points, cif_1, where='post', label='Relapse', linewidth=2)
plt.step(time_points, cif_2, where='post', label='Death in remission', linewidth=2)
plt.xlabel('Time (weeks)')
plt.ylabel('Cumulative Incidence')
plt.title('Competing Risks: Relapse vs Death')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### Interpretation

- **CIF at time t**: Probability of experiencing that specific event by time t
- **Sum of all CIFs**: Total probability of experiencing any event (all cause)
- **1 - sum of CIFs**: Probability of being event-free and uncensored

## Data Format for Competing Risks

### Creating Structured Array with Event Types

```python
import numpy as np
from sksurv.util import Surv

# Event types: 0 = censored, 1 = event type 1, 2 = event type 2
event_types = np.array([0, 1, 2, 1, 0, 2, 1])
times = np.array([10.2, 5.3, 8.1, 3.7, 12.5, 6.8, 4.2])

# Create survival array
# For competing risks: event=True if any event occurred
# Store event type separately or encode in the event field
y = Surv.from_arrays(
    event=(event_types > 0),  # True if any event
    time=times
)

# Keep event_types for distinguishing between event types
```

### Converting Data with Event Types

```python
import pandas as pd
from sksurv.util import Surv

# Assume data has: time, event_type columns
# event_type: 0=censored, 1=type1, 2=type2, etc.

df = pd.read_csv('competing_risks_data.csv')

# Create survival outcome
y = Surv.from_arrays(
    event=(df['event_type'] > 0),
    time=df['time']
)

# Store event types
event_types = df['event_type'].values
```

## Comparing Cumulative Incidence Between Groups

### Stratified Analysis

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks
import matplotlib.pyplot as plt

# Split by treatment group
mask_treatment = X['treatment'] == 'A'
mask_control = X['treatment'] == 'B'

y_treatment = y[mask_treatment]
y_control = y[mask_control]

# Compute CIF for each group
time_trt, cif1_trt, cif2_trt = cumulative_incidence_competing_risks(y_treatment)
time_ctl, cif1_ctl, cif2_ctl = cumulative_incidence_competing_risks(y_control)

# Plot comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Event type 1
ax1.step(time_trt, cif1_trt, where='post', label='Treatment', linewidth=2)
ax1.step(time_ctl, cif1_ctl, where='post', label='Control', linewidth=2)
ax1.set_xlabel('Time')
ax1.set_ylabel('Cumulative Incidence')
ax1.set_title('Event Type 1')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Event type 2
ax2.step(time_trt, cif2_trt, where='post', label='Treatment', linewidth=2)
ax2.step(time_ctl, cif2_ctl, where='post', label='Control', linewidth=2)
ax2.set_xlabel('Time')
ax2.set_ylabel('Cumulative Incidence')
ax2.set_title('Event Type 2')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Statistical Testing with Competing Risks

### Gray's Test

Compare cumulative incidence functions between groups using Gray's test (available in other packages like lifelines).

```python
# Note: Gray's test not directly available in scikit-survival
# Consider using lifelines or other packages

# from lifelines.statistics import multivariate_logrank_test
# result = multivariate_logrank_test(times, groups, events, event_of_interest=1)
```

## Modeling with Competing Risks

### Approach 1: Cause-Specific Hazard Models

Fit separate Cox models for each event type, treating other event types as censored.

```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.util import Surv

# Separate outcome for each event type
# Event type 1: treat type 2 as censored
y_event1 = Surv.from_arrays(
    event=(event_types == 1),
    time=times
)

# Event type 2: treat type 1 as censored
y_event2 = Surv.from_arrays(
    event=(event_types == 2),
    time=times
)

# Fit cause-specific models
cox_event1 = CoxPHSurvivalAnalysis()
cox_event1.fit(X, y_event1)

cox_event2 = CoxPHSurvivalAnalysis()
cox_event2.fit(X, y_event2)

# Interpret coefficients for each event type
print("Event Type 1 (e.g., Relapse):")
print(cox_event1.coef_)

print("\nEvent Type 2 (e.g., Death):")
print(cox_event2.coef_)
```

**Interpretation:**
- Separate model for each competing event
- Coefficients show effect on cause-specific hazard for that event type
- A covariate may increase risk for one event type but decrease for another

### Approach 2: Fine-Gray Sub-distribution Hazard Model

Models the cumulative incidence directly (not available directly in scikit-survival, but can use other packages).

```python
# Note: Fine-Gray model not directly in scikit-survival
# Consider using lifelines or rpy2 to access R's cmprsk package

# from lifelines import CRCSplineFitter
# crc = CRCSplineFitter()
# crc.fit(df, event_col='event', duration_col='time')
```

## Practical Example: Complete Competing Risks Analysis

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sksurv.nonparametric import cumulative_incidence_competing_risks
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.util import Surv

# Simulate competing risks data
np.random.seed(42)
n = 200

# Create features
age = np.random.normal(60, 10, n)
treatment = np.random.choice(['A', 'B'], n)

# Simulate event times and types
# Event types: 0=censored, 1=relapse, 2=death
times = np.random.exponential(100, n)
event_types = np.zeros(n, dtype=int)

# Higher age increases both events, treatment A reduces relapse
for i in range(n):
    if times[i] < 150:  # Event occurred
        # Probability of each event type
        p_relapse = 0.6 if treatment[i] == 'B' else 0.4
        event_types[i] = 1 if np.random.rand() < p_relapse else 2
    else:
        times[i] = 150  # Censored at study end

# Create DataFrame
df = pd.DataFrame({
    'time': times,
    'event_type': event_types,
    'age': age,
    'treatment': treatment
})

# Encode treatment
df['treatment_A'] = (df['treatment'] == 'A').astype(int)

# 1. OVERALL CUMULATIVE INCIDENCE
print("=" * 60)
print("OVERALL CUMULATIVE INCIDENCE")
print("=" * 60)

y_all = Surv.from_arrays(event=(df['event_type'] > 0), time=df['time'])
time_points, cif_relapse, cif_death = cumulative_incidence_competing_risks(y_all)

plt.figure(figsize=(10, 6))
plt.step(time_points, cif_relapse, where='post', label='Relapse', linewidth=2)
plt.step(time_points, cif_death, where='post', label='Death', linewidth=2)
plt.xlabel('Time (days)')
plt.ylabel('Cumulative Incidence')
plt.title('Competing Risks: Relapse vs Death')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"5-year relapse incidence: {cif_relapse[-1]:.2%}")
print(f"5-year death incidence: {cif_death[-1]:.2%}")

# 2. STRATIFIED BY TREATMENT
print("\n" + "=" * 60)
print("CUMULATIVE INCIDENCE BY TREATMENT")
print("=" * 60)

for trt in ['A', 'B']:
    mask = df['treatment'] == trt
    y_trt = Surv.from_arrays(
        event=(df.loc[mask, 'event_type'] > 0),
        time=df.loc[mask, 'time']
    )
    time_trt, cif1_trt, cif2_trt = cumulative_incidence_competing_risks(y_trt)
    print(f"\nTreatment {trt}:")
    print(f"  5-year relapse: {cif1_trt[-1]:.2%}")
    print(f"  5-year death: {cif2_trt[-1]:.2%}")

# 3. CAUSE-SPECIFIC MODELS
print("\n" + "=" * 60)
print("CAUSE-SPECIFIC HAZARD MODELS")
print("=" * 60)

X = df[['age', 'treatment_A']]

# Model for relapse (event type 1)
y_relapse = Surv.from_arrays(
    event=(df['event_type'] == 1),
    time=df['time']
)
cox_relapse = CoxPHSurvivalAnalysis()
cox_relapse.fit(X, y_relapse)

print("\nRelapse Model:")
print(f"  Age:        HR = {np.exp(cox_relapse.coef_[0]):.3f}")
print(f"  Treatment A: HR = {np.exp(cox_relapse.coef_[1]):.3f}")

# Model for death (event type 2)
y_death = Surv.from_arrays(
    event=(df['event_type'] == 2),
    time=df['time']
)
cox_death = CoxPHSurvivalAnalysis()
cox_death.fit(X, y_death)

print("\nDeath Model:")
print(f"  Age:        HR = {np.exp(cox_death.coef_[0]):.3f}")
print(f"  Treatment A: HR = {np.exp(cox_death.coef_[1]):.3f}")

print("\n" + "=" * 60)
```

## Important Considerations

### Censoring in Competing Risks

- **Administrative censoring**: Subject still at risk at end of study
- **Loss to follow-up**: Subject leaves study before event
- **Competing event**: Other event occurred - NOT censored for CIF, but censored for cause-specific models

### Choosing Between Cause-Specific and Sub-distribution Models

**Cause-Specific Hazard Models:**
- Easier to interpret
- Direct effect on hazard rate
- Better for understanding etiology
- Can fit with scikit-survival

**Fine-Gray Sub-distribution Models:**
- Models cumulative incidence directly
- Better for prediction and risk stratification
- More appropriate for clinical decision-making
- Requires other packages

### Common Mistakes

**Mistake 1**: Using Kaplan-Meier to estimate event-specific probabilities
- **Wrong**: Kaplan-Meier for event type 1, treating type 2 as censored
- **Correct**: Cumulative incidence function accounting for competing risks

**Mistake 2**: Ignoring competing risks when they're substantial
- If competing event rate > 10-20%, should use competing risks methods

**Mistake 3**: Confusing cause-specific and sub-distribution hazards
- They answer different questions
- Use appropriate model for your research question

## Summary

**Key Functions:**
- `cumulative_incidence_competing_risks`: Estimate CIF for each event type
- Fit separate Cox models for cause-specific hazards
- Use stratified analysis to compare groups

**Best Practices:**
1. Always plot cumulative incidence functions
2. Report both event-specific and overall incidence
3. Use cause-specific models in scikit-survival
4. Consider Fine-Gray models (other packages) for prediction
5. Be explicit about which events are competing vs censored

---

## Reference: Cox Models

# Cox Proportional Hazards Models

## Overview

Cox proportional hazards models are semi-parametric models that relate covariates to the time of an event. The hazard function for individual *i* is expressed as:

**h_i(t) = h_0(t) × exp(β^T x_i)**

where:
- h_0(t) is the baseline hazard function (unspecified)
- β is the vector of coefficients
- x_i is the covariate vector for individual *i*

The key assumption is that the hazard ratio between two individuals is constant over time (proportional hazards).

## CoxPHSurvivalAnalysis

Basic Cox proportional hazards model for survival analysis.

### When to Use
- Standard survival analysis with censored data
- Need interpretable coefficients (log hazard ratios)
- Proportional hazards assumption holds
- Dataset has relatively few features

### Key Parameters
- `alpha`: Regularization parameter (default: 0, no regularization)
- `ties`: Method for handling tied event times ('breslow' or 'efron')
- `n_iter`: Maximum number of iterations for optimization

### Example Usage
```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.datasets import load_gbsg2

# Load data
X, y = load_gbsg2()

# Fit Cox model
estimator = CoxPHSurvivalAnalysis()
estimator.fit(X, y)

# Get coefficients (log hazard ratios)
coefficients = estimator.coef_

# Predict risk scores
risk_scores = estimator.predict(X)
```

## CoxnetSurvivalAnalysis

Cox model with elastic net penalty for feature selection and regularization.

### When to Use
- High-dimensional data (many features)
- Need automatic feature selection
- Want to handle multicollinearity
- Require sparse models

### Penalty Types
- **Ridge (L2)**: alpha_min_ratio=1.0, l1_ratio=0
  - Shrinks all coefficients
  - Good when all features are relevant

- **Lasso (L1)**: l1_ratio=1.0
  - Performs feature selection (sets coefficients to zero)
  - Good for sparse models

- **Elastic Net**: 0 < l1_ratio < 1
  - Combination of L1 and L2
  - Balances feature selection and grouping

### Key Parameters
- `l1_ratio`: Balance between L1 and L2 penalty (0=Ridge, 1=Lasso)
- `alpha_min_ratio`: Ratio of smallest to largest penalty in regularization path
- `n_alphas`: Number of alphas along regularization path
- `fit_baseline_model`: Whether to fit unpenalized baseline model

### Example Usage
```python
from sksurv.linear_model import CoxnetSurvivalAnalysis

# Fit with elastic net penalty
estimator = CoxnetSurvivalAnalysis(l1_ratio=0.5, alpha_min_ratio=0.01)
estimator.fit(X, y)

# Access regularization path
alphas = estimator.alphas_
coefficients_path = estimator.coef_path_

# Predict with specific alpha
risk_scores = estimator.predict(X, alpha=0.1)
```

### Cross-Validation for Alpha Selection
```python
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import concordance_index_censored

# Define parameter grid
param_grid = {'l1_ratio': [0.1, 0.5, 0.9],
              'alpha_min_ratio': [0.01, 0.001]}

# Grid search with C-index
cv = GridSearchCV(CoxnetSurvivalAnalysis(),
                  param_grid,
                  scoring='concordance_index_ipcw',
                  cv=5)
cv.fit(X, y)

# Best parameters
best_params = cv.best_params_
```

## IPCRidge

Inverse probability of censoring weighted Ridge regression for accelerated failure time models.

### When to Use
- Prefer accelerated failure time (AFT) framework over proportional hazards
- Need to model how features accelerate/decelerate survival time
- High censoring rates
- Want regularization with Ridge penalty

### Key Difference from Cox Models
AFT models assume features multiply survival time by a constant factor, rather than multiplying the hazard rate. The model predicts log survival time directly.

### Example Usage
```python
from sksurv.linear_model import IPCRidge

# Fit IPCRidge model
estimator = IPCRidge(alpha=1.0)
estimator.fit(X, y)

# Predict log survival time
log_time = estimator.predict(X)
```

## Model Comparison and Selection

### Choosing Between Models

**Use CoxPHSurvivalAnalysis when:**
- Small to moderate number of features
- Want interpretable hazard ratios
- Standard survival analysis setting

**Use CoxnetSurvivalAnalysis when:**
- High-dimensional data (p >> n)
- Need feature selection
- Want to identify important predictors
- Presence of multicollinearity

**Use IPCRidge when:**
- AFT framework is more appropriate
- High censoring rates
- Want to model time directly rather than hazard

### Checking Proportional Hazards Assumption

The proportional hazards assumption should be verified using:
- Schoenfeld residuals
- Log-log survival plots
- Statistical tests (available in other packages like lifelines)

If violated, consider:
- Stratification by violating covariates
- Time-varying coefficients
- Alternative models (AFT, parametric models)

## Interpretation

### Cox Model Coefficients
- Positive coefficient: increased hazard (shorter survival)
- Negative coefficient: decreased hazard (longer survival)
- Hazard ratio = exp(β) for one-unit increase in covariate
- Example: β=0.693 → HR=2.0 (doubles the hazard)

### Risk Scores
- Higher risk score = higher risk of event = shorter expected survival
- Risk scores are relative; use survival functions for absolute predictions

---

## Reference: Data Handling

# Data Handling and Preprocessing

## Understanding Survival Data

### The Surv Object

Survival data in scikit-survival is represented using structured arrays with two fields:
- **event**: Boolean indicating whether the event occurred (True) or was censored (False)
- **time**: Time to event or censoring

```python
from sksurv.util import Surv

# Create survival outcome from separate arrays
event = np.array([True, False, True, False, True])
time = np.array([5.2, 10.1, 3.7, 8.9, 6.3])

y = Surv.from_arrays(event=event, time=time)
print(y.dtype)  # [('event', '?'), ('time', '<f8')]
```

### Types of Censoring

**Right Censoring** (most common):
- Subject didn't experience event by end of study
- Subject lost to follow-up
- Subject withdrew from study

**Left Censoring**:
- Event occurred before observation began
- Rare in practice

**Interval Censoring**:
- Event occurred in a known time interval
- Requires specialized methods

scikit-survival primarily handles right-censored data.

## Loading Data

### Built-in Datasets

```python
from sksurv.datasets import (
    load_aids,
    load_breast_cancer,
    load_gbsg2,
    load_veterans_lung_cancer,
    load_whas500
)

# Load dataset
X, y = load_breast_cancer()

# X is pandas DataFrame with features
# y is structured array with 'event' and 'time'
print(f"Features shape: {X.shape}")
print(f"Number of events: {y['event'].sum()}")
print(f"Censoring rate: {1 - y['event'].mean():.2%}")
```

### Loading Custom Data

#### From Pandas DataFrame

```python
import pandas as pd
from sksurv.util import Surv

# Load data
df = pd.read_csv('survival_data.csv')

# Separate features and outcome
X = df.drop(['time', 'event'], axis=1)
y = Surv.from_dataframe('event', 'time', df)
```

#### From CSV with Surv.from_arrays

```python
import numpy as np
import pandas as pd
from sksurv.util import Surv

# Load data
df = pd.read_csv('survival_data.csv')

# Create feature matrix
X = df.drop(['time', 'event'], axis=1)

# Create survival outcome
y = Surv.from_arrays(
    event=df['event'].astype(bool),
    time=df['time'].astype(float)
)
```

### Loading ARFF Files

```python
from sksurv.io import loadarff

# Load ARFF format (Weka format)
data = loadarff('survival_data.arff')

# Extract X and y
X = data[0]  # pandas DataFrame
y = data[1]  # structured array
```

## Data Preprocessing

### Handling Categorical Variables

#### Method 1: OneHotEncoder (scikit-survival)

```python
from sksurv.preprocessing import OneHotEncoder
import pandas as pd

# Identify categorical columns
categorical_cols = ['gender', 'race', 'treatment']

# One-hot encode
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X[categorical_cols])

# Combine with numerical features
numerical_cols = [col for col in X.columns if col not in categorical_cols]
X_processed = pd.concat([X[numerical_cols], X_encoded], axis=1)
```

#### Method 2: encode_categorical

```python
from sksurv.preprocessing import encode_categorical

# Automatically encode all categorical columns
X_encoded = encode_categorical(X)
```

#### Method 3: Pandas get_dummies

```python
import pandas as pd

# One-hot encode categorical variables
X_encoded = pd.get_dummies(X, drop_first=True)
```

### Standardization

Standardization is important for:
- Cox models with regularization
- SVMs
- Models sensitive to feature scales

```python
from sklearn.preprocessing import StandardScaler

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert back to DataFrame
X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
```

### Handling Missing Data

#### Check for Missing Values

```python
# Check missing values
missing = X.isnull().sum()
print(missing[missing > 0])

# Visualize missing data
import seaborn as sns
sns.heatmap(X.isnull(), cbar=False)
```

#### Imputation Strategies

```python
from sklearn.impute import SimpleImputer

# Mean imputation for numerical features
num_imputer = SimpleImputer(strategy='mean')
X_num = X.select_dtypes(include=[np.number])
X_num_imputed = num_imputer.fit_transform(X_num)

# Most frequent for categorical
cat_imputer = SimpleImputer(strategy='most_frequent')
X_cat = X.select_dtypes(include=['object', 'category'])
X_cat_imputed = cat_imputer.fit_transform(X_cat)
```

#### Advanced Imputation

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Iterative imputation
imputer = IterativeImputer(random_state=42)
X_imputed = imputer.fit_transform(X)
```

### Feature Selection

#### Variance Threshold

```python
from sklearn.feature_selection import VarianceThreshold

# Remove low variance features
selector = VarianceThreshold(threshold=0.01)
X_selected = selector.fit_transform(X)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
```

#### Univariate Feature Selection

```python
from sklearn.feature_selection import SelectKBest
from sksurv.util import Surv

# Select top k features
selector = SelectKBest(k=10)
X_selected = selector.fit_transform(X, y)

# Get selected features
selected_features = X.columns[selector.get_support()]
```

## Complete Preprocessing Pipeline

### Using sklearn Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sksurv.linear_model import CoxPHSurvivalAnalysis

# Create preprocessing and modeling pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', CoxPHSurvivalAnalysis())
])

# Fit pipeline
pipeline.fit(X, y)

# Predict
predictions = pipeline.predict(X_test)
```

### Custom Preprocessing Function

```python
def preprocess_survival_data(X, y=None, scaler=None, encoder=None):
    """
    Complete preprocessing pipeline for survival data

    Parameters:
    -----------
    X : DataFrame
        Feature matrix
    y : structured array, optional
        Survival outcome (for filtering invalid samples)
    scaler : StandardScaler, optional
        Fitted scaler (for test data)
    encoder : OneHotEncoder, optional
        Fitted encoder (for test data)

    Returns:
    --------
    X_processed : DataFrame
        Processed features
    scaler : StandardScaler
        Fitted scaler
    encoder : OneHotEncoder
        Fitted encoder
    """
    from sklearn.preprocessing import StandardScaler
    from sksurv.preprocessing import encode_categorical

    # 1. Handle missing values
    # Remove rows with missing outcome
    if y is not None:
        mask = np.isfinite(y['time']) & (y['time'] > 0)
        X = X[mask]
        y = y[mask]

    # Impute missing features
    X = X.fillna(X.median())

    # 2. Encode categorical variables
    if encoder is None:
        X_processed = encode_categorical(X)
        encoder = None  # encode_categorical doesn't return encoder
    else:
        X_processed = encode_categorical(X)

    # 3. Standardize numerical features
    if scaler is None:
        scaler = StandardScaler()
        X_processed = pd.DataFrame(
            scaler.fit_transform(X_processed),
            columns=X_processed.columns,
            index=X_processed.index
        )
    else:
        X_processed = pd.DataFrame(
            scaler.transform(X_processed),
            columns=X_processed.columns,
            index=X_processed.index
        )

    if y is not None:
        return X_processed, y, scaler, encoder
    else:
        return X_processed, scaler, encoder

# Usage
X_train_processed, y_train_processed, scaler, encoder = preprocess_survival_data(X_train, y_train)
X_test_processed, _, _ = preprocess_survival_data(X_test, scaler=scaler, encoder=encoder)
```

## Data Quality Checks

### Validate Survival Data

```python
def validate_survival_data(y):
    """Check survival data quality"""

    # Check for negative times
    if np.any(y['time'] <= 0):
        print("WARNING: Found non-positive survival times")
        print(f"Negative times: {np.sum(y['time'] <= 0)}")

    # Check for missing values
    if np.any(~np.isfinite(y['time'])):
        print("WARNING: Found missing survival times")
        print(f"Missing times: {np.sum(~np.isfinite(y['time']))}")

    # Censoring rate
    censor_rate = 1 - y['event'].mean()
    print(f"Censoring rate: {censor_rate:.2%}")

    if censor_rate > 0.7:
        print("WARNING: High censoring rate (>70%)")
        print("Consider using Uno's C-index instead of Harrell's")

    # Event rate
    print(f"Number of events: {y['event'].sum()}")
    print(f"Number of censored: {(~y['event']).sum()}")

    # Time statistics
    print(f"Median time: {np.median(y['time']):.2f}")
    print(f"Time range: [{np.min(y['time']):.2f}, {np.max(y['time']):.2f}]")

# Use validation
validate_survival_data(y)
```

### Check for Sufficient Events

```python
def check_events_per_feature(X, y, min_events_per_feature=10):
    """
    Check if there are sufficient events per feature.
    Rule of thumb: at least 10 events per feature for Cox models.
    """
    n_events = y['event'].sum()
    n_features = X.shape[1]
    events_per_feature = n_events / n_features

    print(f"Number of events: {n_events}")
    print(f"Number of features: {n_features}")
    print(f"Events per feature: {events_per_feature:.1f}")

    if events_per_feature < min_events_per_feature:
        print(f"WARNING: Low events per feature ratio (<{min_events_per_feature})")
        print("Consider:")
        print("  - Feature selection")
        print("  - Regularization (CoxnetSurvivalAnalysis)")
        print("  - Collecting more data")

    return events_per_feature

# Use check
check_events_per_feature(X, y)
```

## Train-Test Split

### Random Split

```python
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Stratified Split

Ensure similar censoring rates and time distributions:

```python
from sklearn.model_selection import train_test_split

# Create stratification labels
# Stratify by event status and time quartiles
time_quartiles = pd.qcut(y['time'], q=4, labels=False)
strat_labels = y['event'].astype(int) * 10 + time_quartiles

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=strat_labels, random_state=42
)

# Verify similar distributions
print("Training set:")
print(f"  Censoring rate: {1 - y_train['event'].mean():.2%}")
print(f"  Median time: {np.median(y_train['time']):.2f}")

print("Test set:")
print(f"  Censoring rate: {1 - y_test['event'].mean():.2%}")
print(f"  Median time: {np.median(y_test['time']):.2f}")
```

## Working with Time-Varying Covariates

Note: scikit-survival doesn't directly support time-varying covariates. For such data, consider:
1. Time-stratified analysis
2. Landmarking approach
3. Using other packages (e.g., lifelines)

## Summary: Complete Data Preparation Workflow

```python
from sksurv.util import Surv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sksurv.preprocessing import encode_categorical
import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv('data.csv')

# 2. Create survival outcome
y = Surv.from_dataframe('event', 'time', df)

# 3. Prepare features
X = df.drop(['event', 'time'], axis=1)

# 4. Validate data
validate_survival_data(y)
check_events_per_feature(X, y)

# 5. Handle missing values
X = X.fillna(X.median())

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Encode categorical variables
X_train = encode_categorical(X_train)
X_test = encode_categorical(X_test)

# 8. Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrames
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

# Now ready for modeling!
```

---

## Reference: Ensemble Models

# Ensemble Models for Survival Analysis

## Random Survival Forests

### Overview

Random Survival Forests extend the random forest algorithm to survival analysis with censored data. They build multiple decision trees on bootstrap samples and aggregate predictions.

### How They Work

1. **Bootstrap Sampling**: Each tree is built on a different bootstrap sample of the training data
2. **Feature Randomness**: At each node, only a random subset of features is considered for splitting
3. **Survival Function Estimation**: At terminal nodes, Kaplan-Meier and Nelson-Aalen estimators compute survival functions
4. **Ensemble Aggregation**: Final predictions average survival functions across all trees

### When to Use

- Complex non-linear relationships between features and survival
- No assumptions about functional form needed
- Want robust predictions with minimal tuning
- Need feature importance estimates
- Have sufficient sample size (typically n > 100)

### Key Parameters

- `n_estimators`: Number of trees (default: 100)
  - More trees = more stable predictions but slower
  - Typical range: 100-1000

- `max_depth`: Maximum depth of trees
  - Controls tree complexity
  - None = nodes expanded until pure or min_samples_split

- `min_samples_split`: Minimum samples to split a node (default: 6)
  - Larger values = more regularization

- `min_samples_leaf`: Minimum samples at leaf nodes (default: 3)
  - Prevents overfitting to small groups

- `max_features`: Number of features to consider at each split
  - 'sqrt': sqrt(n_features) - good default
  - 'log2': log2(n_features)
  - None: all features

- `n_jobs`: Number of parallel jobs (-1 uses all processors)

### Example Usage

```python
from sksurv.ensemble import RandomSurvivalForest
from sksurv.datasets import load_breast_cancer

# Load data
X, y = load_breast_cancer()

# Fit Random Survival Forest
rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           max_features="sqrt",
                           n_jobs=-1,
                           random_state=42)
rsf.fit(X, y)

# Predict risk scores
risk_scores = rsf.predict(X)

# Predict survival functions
surv_funcs = rsf.predict_survival_function(X)

# Predict cumulative hazard functions
chf_funcs = rsf.predict_cumulative_hazard_function(X)
```

### Feature Importance

**Important**: Built-in feature importance based on split impurity is not reliable for survival data. Use permutation-based feature importance instead.

```python
from sklearn.inspection import permutation_importance
from sksurv.metrics import concordance_index_censored

# Define scoring function
def score_survival_model(model, X, y):
    prediction = model.predict(X)
    result = concordance_index_censored(y['event'], y['time'], prediction)
    return result[0]

# Compute permutation importance
perm_importance = permutation_importance(
    rsf, X, y,
    n_repeats=10,
    random_state=42,
    scoring=score_survival_model
)

# Get feature importance
feature_importance = perm_importance.importances_mean
```

## Gradient Boosting Survival Analysis

### Overview

Gradient boosting builds an ensemble by sequentially adding weak learners that correct errors of previous learners. The model is: **f(x) = Σ β_m g(x; θ_m)**

### Model Types

#### GradientBoostingSurvivalAnalysis

Uses regression trees as base learners. Can capture complex non-linear relationships.

**When to Use:**
- Need to model complex non-linear relationships
- Want high predictive performance
- Have sufficient data to avoid overfitting
- Can tune hyperparameters carefully

#### ComponentwiseGradientBoostingSurvivalAnalysis

Uses component-wise least squares as base learners. Produces linear models with automatic feature selection.

**When to Use:**
- Want interpretable linear model
- Need automatic feature selection (like Lasso)
- Have high-dimensional data
- Prefer sparse models

### Loss Functions

#### Cox's Partial Likelihood (default)

Maintains proportional hazards framework but replaces linear model with additive ensemble model.

**Appropriate for:**
- Standard survival analysis settings
- When proportional hazards is reasonable
- Most use cases

#### Accelerated Failure Time (AFT)

Assumes features accelerate or decelerate survival time by a constant factor. Loss function: **(1/n) Σ ω_i (log y_i - f(x_i))²**

**Appropriate for:**
- AFT framework preferred over proportional hazards
- Want to model time directly
- Need to interpret effects on survival time

### Regularization Strategies

Three main techniques prevent overfitting:

1. **Learning Rate** (`learning_rate < 1`)
   - Shrinks contribution of each base learner
   - Smaller values need more iterations but better generalization
   - Typical range: 0.01 - 0.1

2. **Dropout** (`dropout_rate > 0`)
   - Randomly drops previous learners during training
   - Forces learners to be more robust
   - Typical range: 0.01 - 0.2

3. **Subsampling** (`subsample < 1`)
   - Uses random subset of data for each iteration
   - Adds randomness and reduces overfitting
   - Typical range: 0.5 - 0.9

**Recommendation**: Combine small learning rate with early stopping for best performance.

### Key Parameters

- `loss`: Loss function ('coxph' or 'ipcwls')
- `learning_rate`: Shrinks contribution of each tree (default: 0.1)
- `n_estimators`: Number of boosting iterations (default: 100)
- `subsample`: Fraction of samples for each iteration (default: 1.0)
- `dropout_rate`: Dropout rate for learners (default: 0.0)
- `max_depth`: Maximum depth of trees (default: 3)
- `min_samples_split`: Minimum samples to split node (default: 2)
- `min_samples_leaf`: Minimum samples at leaf (default: 1)
- `max_features`: Features to consider at each split

### Example Usage

```python
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit gradient boosting model
gbs = GradientBoostingSurvivalAnalysis(
    loss='coxph',
    learning_rate=0.05,
    n_estimators=200,
    subsample=0.8,
    dropout_rate=0.1,
    max_depth=3,
    random_state=42
)
gbs.fit(X_train, y_train)

# Predict risk scores
risk_scores = gbs.predict(X_test)

# Predict survival functions
surv_funcs = gbs.predict_survival_function(X_test)

# Predict cumulative hazard functions
chf_funcs = gbs.predict_cumulative_hazard_function(X_test)
```

### Early Stopping

Use validation set to prevent overfitting:

```python
from sklearn.model_selection import train_test_split

# Create train/validation split
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Fit with early stopping
gbs = GradientBoostingSurvivalAnalysis(
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=3,
    validation_fraction=0.2,
    n_iter_no_change=10,
    random_state=42
)
gbs.fit(X_tr, y_tr)

# Number of iterations used
print(f"Used {gbs.n_estimators_} iterations")
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0]
}

cv = GridSearchCV(
    GradientBoostingSurvivalAnalysis(),
    param_grid,
    scoring='concordance_index_ipcw',
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

best_model = cv.best_estimator_
```

## ComponentwiseGradientBoostingSurvivalAnalysis

### Overview

Uses component-wise least squares, producing sparse linear models with automatic feature selection similar to Lasso.

### When to Use

- Want interpretable linear model
- Need automatic feature selection
- Have high-dimensional data with many irrelevant features
- Prefer coefficient-based interpretation

### Example Usage

```python
from sksurv.ensemble import ComponentwiseGradientBoostingSurvivalAnalysis

# Fit componentwise boosting
cgbs = ComponentwiseGradientBoostingSurvivalAnalysis(
    loss='coxph',
    learning_rate=0.1,
    n_estimators=100
)
cgbs.fit(X, y)

# Get selected features and coefficients
coef = cgbs.coef_
selected_features = [i for i, c in enumerate(coef) if c != 0]
```

## ExtraSurvivalTrees

Extremely randomized survival trees - similar to Random Survival Forest but with additional randomness in split selection.

### When to Use

- Want even more regularization than Random Survival Forest
- Have limited data
- Need faster training

### Key Difference

Instead of finding the best split for selected features, it randomly selects split points, adding more diversity to the ensemble.

```python
from sksurv.ensemble import ExtraSurvivalTrees

est = ExtraSurvivalTrees(n_estimators=100, random_state=42)
est.fit(X, y)
```

## Model Comparison

| Model | Complexity | Interpretability | Performance | Speed |
|-------|-----------|------------------|-------------|-------|
| Random Survival Forest | Medium | Low | High | Medium |
| GradientBoostingSurvivalAnalysis | High | Low | Highest | Slow |
| ComponentwiseGradientBoostingSurvivalAnalysis | Low | High | Medium | Fast |
| ExtraSurvivalTrees | Medium | Low | Medium-High | Fast |

**General Recommendations:**
- **Best overall performance**: GradientBoostingSurvivalAnalysis with tuning
- **Best balance**: RandomSurvivalForest
- **Best interpretability**: ComponentwiseGradientBoostingSurvivalAnalysis
- **Fastest training**: ExtraSurvivalTrees

---

## Reference: Evaluation Metrics

# Evaluation Metrics for Survival Models

## Overview

Evaluating survival models requires specialized metrics that account for censored data. scikit-survival provides three main categories of metrics:
1. Concordance Index (C-index)
2. Time-dependent ROC and AUC
3. Brier Score

## Concordance Index (C-index)

### What It Measures

The concordance index measures the rank correlation between predicted risk scores and observed event times. It represents the probability that, for a random pair of subjects, the model correctly orders their survival times.

**Range**: 0 to 1
- 0.5 = random predictions
- 1.0 = perfect concordance
- Typical good performance: 0.7-0.8

### Two Implementations

#### Harrell's C-index (concordance_index_censored)

The traditional estimator, simpler but has limitations.

**When to Use:**
- Low censoring rates (< 40%)
- Quick evaluation during development
- Comparing models on same dataset

**Limitations:**
- Becomes increasingly biased with high censoring rates
- Overestimates performance starting at approximately 49% censoring

```python
from sksurv.metrics import concordance_index_censored

# Compute Harrell's C-index
result = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)
c_index = result[0]
print(f"Harrell's C-index: {c_index:.3f}")
```

#### Uno's C-index (concordance_index_ipcw)

Inverse probability of censoring weighted (IPCW) estimator that corrects for censoring bias.

**When to Use:**
- Moderate to high censoring rates (> 40%)
- Need unbiased estimates
- Comparing models across different datasets
- Publishing results (more robust)

**Advantages:**
- Remains stable even with high censoring
- More reliable estimates
- Less biased

```python
from sksurv.metrics import concordance_index_ipcw

# Compute Uno's C-index
# Requires training data for IPCW calculation
c_index, concordant, discordant, tied_risk = concordance_index_ipcw(
    y_train, y_test, risk_scores
)
print(f"Uno's C-index: {c_index:.3f}")
```

### Choosing Between Harrell's and Uno's

**Use Uno's C-index when:**
- Censoring rate > 40%
- Need most accurate estimates
- Comparing models from different studies
- Publishing research

**Use Harrell's C-index when:**
- Low censoring rates
- Quick model comparisons during development
- Computational efficiency is critical

### Example Comparison

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# Harrell's C-index
harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# Uno's C-index
uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]

print(f"Harrell's C-index: {harrell:.3f}")
print(f"Uno's C-index: {uno:.3f}")
```

## Time-Dependent ROC and AUC

### What It Measures

Time-dependent AUC evaluates model discrimination at specific time points. It distinguishes subjects who experience events by time *t* from those who don't.

**Question answered**: "How well does the model predict who will have an event by time t?"

### When to Use

- Predicting event occurrence within specific time windows
- Clinical decision-making at specific timepoints (e.g., 5-year survival)
- Want to evaluate performance across different time horizons
- Need both discrimination and timing information

### Key Function: cumulative_dynamic_auc

```python
from sksurv.metrics import cumulative_dynamic_auc

# Define evaluation times
times = [365, 730, 1095, 1460, 1825]  # 1, 2, 3, 4, 5 years

# Compute time-dependent AUC
auc, mean_auc = cumulative_dynamic_auc(
    y_train, y_test, risk_scores, times
)

# Plot AUC over time
import matplotlib.pyplot as plt
plt.plot(times, auc, marker='o')
plt.xlabel('Time (days)')
plt.ylabel('Time-dependent AUC')
plt.title('Model Discrimination Over Time')
plt.show()

print(f"Mean AUC: {mean_auc:.3f}")
```

### Interpretation

- **AUC at time t**: Probability model correctly ranks a subject who had event by time t above one who didn't
- **Varying AUC over time**: Indicates model performance changes with time horizon
- **Mean AUC**: Overall summary of discrimination across all time points

### Example: Comparing Models

```python
# Compare two models
auc1, mean_auc1 = cumulative_dynamic_auc(y_train, y_test, risk_scores1, times)
auc2, mean_auc2 = cumulative_dynamic_auc(y_train, y_test, risk_scores2, times)

plt.plot(times, auc1, marker='o', label='Model 1')
plt.plot(times, auc2, marker='s', label='Model 2')
plt.xlabel('Time (days)')
plt.ylabel('Time-dependent AUC')
plt.legend()
plt.show()
```

## Brier Score

### What It Measures

Brier score extends mean squared error to survival data with censoring. It measures both discrimination (ranking) and calibration (accuracy of predicted probabilities).

**Formula**: **(1/n) Σ (S(t|x_i) - I(T_i > t))²**

where S(t|x_i) is predicted survival probability at time t for subject i.

**Range**: 0 to 1
- 0 = perfect predictions
- Lower is better
- Typical good performance: < 0.2

### When to Use

- Need calibration assessment (not just ranking)
- Want to evaluate predicted probabilities, not just risk scores
- Comparing models that output survival functions
- Clinical applications requiring probability estimates

### Key Functions

#### brier_score: Single Time Point

```python
from sksurv.metrics import brier_score

# Compute Brier score at specific time
time_point = 1825  # 5 years
surv_probs = model.predict_survival_function(X_test)
# Extract survival probability at time_point for each subject
surv_at_t = [fn(time_point) for fn in surv_probs]

bs = brier_score(y_train, y_test, surv_at_t, time_point)[1]
print(f"Brier score at {time_point} days: {bs:.3f}")
```

#### integrated_brier_score: Summary Across Time

```python
from sksurv.metrics import integrated_brier_score

# Compute integrated Brier score
times = [365, 730, 1095, 1460, 1825]
surv_probs = model.predict_survival_function(X_test)

ibs = integrated_brier_score(y_train, y_test, surv_probs, times)
print(f"Integrated Brier Score: {ibs:.3f}")
```

### Interpretation

- **Brier score at time t**: Expected squared difference between predicted and actual survival at time t
- **Integrated Brier Score**: Weighted average of Brier scores across time
- **Lower values = better predictions**

### Comparison with Null Model

Always compare against a baseline (e.g., Kaplan-Meier):

```python
from sksurv.nonparametric import kaplan_meier_estimator

# Compute Kaplan-Meier baseline
time_km, surv_km = kaplan_meier_estimator(y_train['event'], y_train['time'])

# Predict with KM for each test subject
surv_km_test = [surv_km[time_km <= time_point][-1] if any(time_km <= time_point) else 1.0
                for _ in range(len(X_test))]

bs_km = brier_score(y_train, y_test, surv_km_test, time_point)[1]
bs_model = brier_score(y_train, y_test, surv_at_t, time_point)[1]

print(f"Kaplan-Meier Brier Score: {bs_km:.3f}")
print(f"Model Brier Score: {bs_model:.3f}")
print(f"Improvement: {(bs_km - bs_model) / bs_km * 100:.1f}%")
```

## Using Metrics with Cross-Validation

### Concordance Index Scorer

```python
from sklearn.model_selection import cross_val_score
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Create scorer
scorer = as_concordance_index_ipcw_scorer()

# Perform cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring=scorer)
print(f"Mean C-index: {scores.mean():.3f} (±{scores.std():.3f})")
```

### Integrated Brier Score Scorer

```python
from sksurv.metrics import as_integrated_brier_score_scorer

# Define time points for evaluation
times = np.percentile(y['time'][y['event']], [25, 50, 75])

# Create scorer
scorer = as_integrated_brier_score_scorer(times)

# Perform cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring=scorer)
print(f"Mean IBS: {scores.mean():.3f} (±{scores.std():.3f})")
```

## Model Selection with GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'min_samples_split': [10, 20, 30],
    'max_depth': [None, 10, 20]
}

# Create scorer
scorer = as_concordance_index_ipcw_scorer()

# Perform grid search
cv = GridSearchCV(
    RandomSurvivalForest(random_state=42),
    param_grid,
    scoring=scorer,
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best parameters: {cv.best_params_}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

## Comprehensive Model Evaluation

### Recommended Evaluation Pipeline

```python
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    integrated_brier_score
)

def evaluate_survival_model(model, X_train, X_test, y_train, y_test):
    """Comprehensive evaluation of survival model"""

    # Get predictions
    risk_scores = model.predict(X_test)
    surv_funcs = model.predict_survival_function(X_test)

    # 1. Concordance Index (both versions)
    c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]
    c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]

    # 2. Time-dependent AUC
    times = np.percentile(y_test['time'][y_test['event']], [25, 50, 75])
    auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)

    # 3. Integrated Brier Score
    ibs = integrated_brier_score(y_train, y_test, surv_funcs, times)

    # Print results
    print("=" * 50)
    print("Model Evaluation Results")
    print("=" * 50)
    print(f"Harrell's C-index:  {c_harrell:.3f}")
    print(f"Uno's C-index:      {c_uno:.3f}")
    print(f"Mean AUC:           {mean_auc:.3f}")
    print(f"Integrated Brier:   {ibs:.3f}")
    print("=" * 50)

    return {
        'c_harrell': c_harrell,
        'c_uno': c_uno,
        'mean_auc': mean_auc,
        'ibs': ibs,
        'time_auc': dict(zip(times, auc))
    }

# Use the evaluation function
results = evaluate_survival_model(model, X_train, X_test, y_train, y_test)
```

## Choosing the Right Metric

### Decision Guide

**Use C-index (Uno's) when:**
- Primary goal is ranking/discrimination
- Don't need calibrated probabilities
- Standard survival analysis setting
- Most common choice

**Use Time-dependent AUC when:**
- Need discrimination at specific time points
- Clinical decisions at specific horizons
- Want to understand how performance varies over time

**Use Brier Score when:**
- Need calibrated probability estimates
- Both discrimination AND calibration important
- Clinical decision-making requiring probabilities
- Want comprehensive assessment

**Best Practice**: Report multiple metrics for comprehensive evaluation. At minimum, report:
- Uno's C-index (discrimination)
- Integrated Brier Score (discrimination + calibration)
- Time-dependent AUC at clinically relevant time points

---

## Reference: Svm Models

# Survival Support Vector Machines

## Overview

Survival Support Vector Machines (SVMs) adapt the traditional SVM framework to survival analysis with censored data. They optimize a ranking objective that encourages correct ordering of survival times.

### Core Idea

SVMs for survival analysis learn a function f(x) that produces risk scores, where the optimization ensures that subjects with shorter survival times receive higher risk scores than those with longer times.

## When to Use Survival SVMs

**Appropriate for:**
- Medium-sized datasets (typically 100-10,000 samples)
- Need for non-linear decision boundaries (kernel SVMs)
- Want margin-based learning with regularization
- Have well-defined feature space

**Not ideal for:**
- Very large datasets (>100,000 samples) - ensemble methods may be faster
- Need interpretable coefficients - use Cox models instead
- Require survival function estimates - use Random Survival Forest
- Very high dimensional data - use regularized Cox or gradient boosting

## Model Types

### FastSurvivalSVM

Linear survival SVM optimized for speed using coordinate descent.

**When to Use:**
- Linear relationships expected
- Large datasets where speed matters
- Want fast training and prediction

**Key Parameters:**
- `alpha`: Regularization parameter (default: 1.0)
  - Higher = more regularization
- `rank_ratio`: Trade-off between ranking and regression (default: 1.0)
- `max_iter`: Maximum iterations (default: 20)
- `tol`: Tolerance for stopping criterion (default: 1e-5)

```python
from sksurv.svm import FastSurvivalSVM

# Fit linear survival SVM
estimator = FastSurvivalSVM(alpha=1.0, max_iter=100, tol=1e-5, random_state=42)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### FastKernelSurvivalSVM

Kernel survival SVM for non-linear relationships.

**When to Use:**
- Non-linear relationships between features and survival
- Medium-sized datasets
- Can afford longer training time for better performance

**Kernel Options:**
- `'linear'`: Linear kernel, equivalent to FastSurvivalSVM
- `'poly'`: Polynomial kernel
- `'rbf'`: Radial basis function (Gaussian) kernel - most common
- `'sigmoid'`: Sigmoid kernel
- Custom kernel function

**Key Parameters:**
- `alpha`: Regularization parameter (default: 1.0)
- `kernel`: Kernel function (default: 'rbf')
- `gamma`: Kernel coefficient for rbf, poly, sigmoid
- `degree`: Degree for polynomial kernel
- `coef0`: Independent term for poly and sigmoid
- `rank_ratio`: Trade-off parameter (default: 1.0)
- `max_iter`: Maximum iterations (default: 20)

```python
from sksurv.svm import FastKernelSurvivalSVM

# Fit RBF kernel survival SVM
estimator = FastKernelSurvivalSVM(
    alpha=1.0,
    kernel='rbf',
    gamma='scale',
    max_iter=50,
    random_state=42
)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### HingeLossSurvivalSVM

Survival SVM using hinge loss, more similar to classification SVM.

**When to Use:**
- Want hinge loss instead of squared hinge
- Sparse solutions desired
- Similar behavior to classification SVMs

**Key Parameters:**
- `alpha`: Regularization parameter
- `fit_intercept`: Whether to fit intercept term (default: False)

```python
from sksurv.svm import HingeLossSurvivalSVM

# Fit hinge loss SVM
estimator = HingeLossSurvivalSVM(alpha=1.0, fit_intercept=False, random_state=42)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### NaiveSurvivalSVM

Original formulation of survival SVM using quadratic programming.

**When to Use:**
- Small datasets
- Research/benchmarking purposes
- Other methods don't converge

**Limitations:**
- Slower than Fast variants
- Less scalable

```python
from sksurv.svm import NaiveSurvivalSVM

# Fit naive SVM (slower)
estimator = NaiveSurvivalSVM(alpha=1.0, random_state=42)
estimator.fit(X, y)

# Predict
risk_scores = estimator.predict(X_test)
```

### MinlipSurvivalAnalysis

Survival analysis using minimizing Lipschitz constant approach.

**When to Use:**
- Want different optimization objective
- Research applications
- Alternative to standard survival SVMs

```python
from sksurv.svm import MinlipSurvivalAnalysis

# Fit Minlip model
estimator = MinlipSurvivalAnalysis(alpha=1.0, random_state=42)
estimator.fit(X, y)

# Predict
risk_scores = estimator.predict(X_test)
```

## Hyperparameter Tuning

### Tuning Alpha (Regularization)

```python
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Define parameter grid
param_grid = {
    'alpha': [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
}

# Grid search
cv = GridSearchCV(
    FastSurvivalSVM(),
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best alpha: {cv.best_params_['alpha']}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

### Tuning Kernel Parameters

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid for kernel SVM
param_grid = {
    'alpha': [0.1, 1.0, 10.0],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1.0]
}

# Grid search
cv = GridSearchCV(
    FastKernelSurvivalSVM(kernel='rbf'),
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best parameters: {cv.best_params_}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

## Clinical Kernel Transform

### ClinicalKernelTransform

Special kernel that combines clinical features with molecular data for improved predictions in medical applications.

**Use Case:**
- Have both clinical variables (age, stage, etc.) and high-dimensional molecular data (gene expression, genomics)
- Clinical features should have different weighting
- Want to integrate heterogeneous data types

**Key Parameters:**
- `fit_once`: Whether to fit kernel once or refit during cross-validation (default: False)
- Clinical features should be passed separately from molecular features

```python
from sksurv.kernels import ClinicalKernelTransform
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.pipeline import make_pipeline

# Separate clinical and molecular features
clinical_features = ['age', 'stage', 'grade']
X_clinical = X[clinical_features]
X_molecular = X.drop(clinical_features, axis=1)

# Create pipeline with clinical kernel
estimator = make_pipeline(
    ClinicalKernelTransform(),
    FastKernelSurvivalSVM()
)

# Fit model
# ClinicalKernelTransform expects tuple (clinical, molecular)
X_combined = list(zip(X_clinical.values, X_molecular.values))
estimator.fit(X_combined, y)
```

## Practical Examples

### Example 1: Linear SVM with Cross-Validation

```python
from sksurv.svm import FastSurvivalSVM
from sklearn.model_selection import cross_val_score
from sksurv.metrics import as_concordance_index_ipcw_scorer
from sklearn.preprocessing import StandardScaler

# Standardize features (important for SVMs!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create model
svm = FastSurvivalSVM(alpha=1.0, max_iter=100, random_state=42)

# Cross-validation
scores = cross_val_score(
    svm, X_scaled, y,
    cv=5,
    scoring=as_concordance_index_ipcw_scorer(),
    n_jobs=-1
)

print(f"Mean C-index: {scores.mean():.3f} (±{scores.std():.3f})")
```

### Example 2: Kernel SVM with Different Kernels

```python
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.model_selection import train_test_split
from sksurv.metrics import concordance_index_ipcw

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Compare different kernels
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
results = {}

for kernel in kernels:
    # Fit model
    svm = FastKernelSurvivalSVM(kernel=kernel, alpha=1.0, random_state=42)
    svm.fit(X_train_scaled, y_train)

    # Predict
    risk_scores = svm.predict(X_test_scaled)

    # Evaluate
    c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
    results[kernel] = c_index

    print(f"{kernel:10s}: C-index = {c_index:.3f}")

# Best kernel
best_kernel = max(results, key=results.get)
print(f"\nBest kernel: {best_kernel} (C-index = {results[best_kernel]:.3f})")
```

### Example 3: Full Pipeline with Hyperparameter Tuning

```python
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', FastKernelSurvivalSVM(kernel='rbf'))
])

# Define parameter grid
param_grid = {
    'svm__alpha': [0.1, 1.0, 10.0],
    'svm__gamma': ['scale', 0.01, 0.1, 1.0]
}

# Grid search
cv = GridSearchCV(
    pipeline,
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1,
    verbose=1
)
cv.fit(X_train, y_train)

# Best model
best_model = cv.best_estimator_
print(f"Best parameters: {cv.best_params_}")
print(f"Best CV C-index: {cv.best_score_:.3f}")

# Evaluate on test set
risk_scores = best_model.predict(X_test)
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"Test C-index: {c_index:.3f}")
```

## Important Considerations

### Feature Scaling

**CRITICAL**: Always standardize features before using SVMs!

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### Computational Complexity

- **FastSurvivalSVM**: O(n × p) per iteration - fast
- **FastKernelSurvivalSVM**: O(n² × p) - slower, scales quadratically
- **NaiveSurvivalSVM**: O(n³) - very slow for large datasets

For large datasets (>10,000 samples), prefer:
- FastSurvivalSVM (linear)
- Gradient Boosting
- Random Survival Forest

### When SVMs May Not Be Best Choice

- **Very large datasets**: Ensemble methods are faster
- **Need survival functions**: Use Random Survival Forest or Cox models
- **Need interpretability**: Use Cox models
- **Very high dimensional**: Use penalized Cox (Coxnet) or gradient boosting with feature selection

## Model Selection Guide

| Model | Speed | Non-linearity | Scalability | Interpretability |
|-------|-------|---------------|-------------|------------------|
| FastSurvivalSVM | Fast | No | High | Medium |
| FastKernelSurvivalSVM | Medium | Yes | Medium | Low |
| HingeLossSurvivalSVM | Fast | No | High | Medium |
| NaiveSurvivalSVM | Slow | No | Low | Medium |

**General Recommendations:**
- Start with **FastSurvivalSVM** for baseline
- Try **FastKernelSurvivalSVM** with RBF if non-linearity expected
- Use grid search to tune alpha and gamma
- Always standardize features
- Compare with Random Survival Forest and Gradient Boosting
