---
title: "Shap"
description: "Model interpretability and explainability using SHAP (SHapley Additive exPlanations). Use this skill when explaining machine learning model predictions, computing feature importance, generating SHAP plots (waterfall, beeswarm, bar, scatter, force,..."
category: "research"
source: "community"
author: "Community"
tags: ["shap"]
date: 2026-03-20
---

# SHAP (SHapley Additive exPlanations)

## Overview

SHAP is a unified approach to explain machine learning model outputs using Shapley values from cooperative game theory. This skill provides comprehensive guidance for:

- Computing SHAP values for any model type
- Creating visualizations to understand feature importance
- Debugging and validating model behavior
- Analyzing fairness and bias
- Implementing explainable AI in production

SHAP works with all model types: tree-based models (XGBoost, LightGBM, CatBoost, Random Forest), deep learning models (TensorFlow, PyTorch, Keras), linear models, and black-box models.

## When to Use This Skill

**Trigger this skill when users ask about**:
- "Explain which features are most important in my model"
- "Generate SHAP plots" (waterfall, beeswarm, bar, scatter, force, heatmap, etc.)
- "Why did my model make this prediction?"
- "Calculate SHAP values for my model"
- "Visualize feature importance using SHAP"
- "Debug my model's behavior" or "validate my model"
- "Check my model for bias" or "analyze fairness"
- "Compare feature importance across models"
- "Implement explainable AI" or "add explanations to my model"
- "Understand feature interactions"
- "Create model interpretation dashboard"

## Quick Start Guide

### Step 1: Select the Right Explainer

**Decision Tree**:

1. **Tree-based model?** (XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting)
   - Use `shap.TreeExplainer` (fast, exact)

2. **Deep neural network?** (TensorFlow, PyTorch, Keras, CNNs, RNNs, Transformers)
   - Use `shap.DeepExplainer` or `shap.GradientExplainer`

3. **Linear model?** (Linear/Logistic Regression, GLMs)
   - Use `shap.LinearExplainer` (extremely fast)

4. **Any other model?** (SVMs, custom functions, black-box models)
   - Use `shap.KernelExplainer` (model-agnostic but slower)

5. **Unsure?**
   - Use `shap.Explainer` (automatically selects best algorithm)

**See `references/explainers.md` for detailed information on all explainer types.**

### Step 2: Compute SHAP Values

```python
import shap

# Example with tree-based model (XGBoost)
import xgboost as xgb

# Train model
model = xgb.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer(X_test)

# The shap_values object contains:
# - values: SHAP values (feature attributions)
# - base_values: Expected model output (baseline)
# - data: Original feature values
```

### Step 3: Visualize Results

**For Global Understanding** (entire dataset):
```python
# Beeswarm plot - shows feature importance with value distributions
shap.plots.beeswarm(shap_values, max_display=15)

# Bar plot - clean summary of feature importance
shap.plots.bar(shap_values)
```

**For Individual Predictions**:
```python
# Waterfall plot - detailed breakdown of single prediction
shap.plots.waterfall(shap_values[0])

# Force plot - additive force visualization
shap.plots.force(shap_values[0])
```

**For Feature Relationships**:
```python
# Scatter plot - feature-prediction relationship
shap.plots.scatter(shap_values[:, "Feature_Name"])

# Colored by another feature to show interactions
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])
```

**See `references/plots.md` for comprehensive guide on all plot types.**

## Core Workflows

This skill supports several common workflows. Choose the workflow that matches the current task.

### Workflow 1: Basic Model Explanation

**Goal**: Understand what drives model predictions

**Steps**:
1. Train model and create appropriate explainer
2. Compute SHAP values for test set
3. Generate global importance plots (beeswarm or bar)
4. Examine top feature relationships (scatter plots)
5. Explain specific predictions (waterfall plots)

**Example**:
```python
# Step 1-2: Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Step 3: Global importance
shap.plots.beeswarm(shap_values)

# Step 4: Feature relationships
shap.plots.scatter(shap_values[:, "Most_Important_Feature"])

# Step 5: Individual explanation
shap.plots.waterfall(shap_values[0])
```

### Workflow 2: Model Debugging

**Goal**: Identify and fix model issues

**Steps**:
1. Compute SHAP values
2. Identify prediction errors
3. Explain misclassified samples
4. Check for unexpected feature importance (data leakage)
5. Validate feature relationships make sense
6. Check feature interactions

**See `references/workflows.md` for detailed debugging workflow.**

### Workflow 3: Feature Engineering

**Goal**: Use SHAP insights to improve features

**Steps**:
1. Compute SHAP values for baseline model
2. Identify nonlinear relationships (candidates for transformation)
3. Identify feature interactions (candidates for interaction terms)
4. Engineer new features
5. Retrain and compare SHAP values
6. Validate improvements

**See `references/workflows.md` for detailed feature engineering workflow.**

### Workflow 4: Model Comparison

**Goal**: Compare multiple models to select best interpretable option

**Steps**:
1. Train multiple models
2. Compute SHAP values for each
3. Compare global feature importance
4. Check consistency of feature rankings
5. Analyze specific predictions across models
6. Select based on accuracy, interpretability, and consistency

**See `references/workflows.md` for detailed model comparison workflow.**

### Workflow 5: Fairness and Bias Analysis

**Goal**: Detect and analyze model bias across demographic groups

**Steps**:
1. Identify protected attributes (gender, race, age, etc.)
2. Compute SHAP values
3. Compare feature importance across groups
4. Check protected attribute SHAP importance
5. Identify proxy features
6. Implement mitigation strategies if bias found

**See `references/workflows.md` for detailed fairness analysis workflow.**

### Workflow 6: Production Deployment

**Goal**: Integrate SHAP explanations into production systems

**Steps**:
1. Train and save model
2. Create and save explainer
3. Build explanation service
4. Create API endpoints for predictions with explanations
5. Implement caching and optimization
6. Monitor explanation quality

**See `references/workflows.md` for detailed production deployment workflow.**

## Key Concepts

### SHAP Values

**Definition**: SHAP values quantify each feature's contribution to a prediction, measured as the deviation from the expected model output (baseline).

**Properties**:
- **Additivity**: SHAP values sum to difference between prediction and baseline
- **Fairness**: Based on Shapley values from game theory
- **Consistency**: If a feature becomes more important, its SHAP value increases

**Interpretation**:
- Positive SHAP value → Feature pushes prediction higher
- Negative SHAP value → Feature pushes prediction lower
- Magnitude → Strength of feature's impact
- Sum of SHAP values → Total prediction change from baseline

**Example**:
```
Baseline (expected value): 0.30
Feature contributions (SHAP values):
  Age: +0.15
  Income: +0.10
  Education: -0.05
Final prediction: 0.30 + 0.15 + 0.10 - 0.05 = 0.50
```

### Background Data / Baseline

**Purpose**: Represents "typical" input to establish baseline expectations

**Selection**:
- Random sample from training data (50-1000 samples)
- Or use kmeans to select representative samples
- For DeepExplainer/KernelExplainer: 100-1000 samples balances accuracy and speed

**Impact**: Baseline affects SHAP value magnitudes but not relative importance

### Model Output Types

**Critical Consideration**: Understand what your model outputs

- **Raw output**: For regression or tree margins
- **Probability**: For classification probability
- **Log-odds**: For logistic regression (before sigmoid)

**Example**: XGBoost classifiers explain margin output (log-odds) by default. To explain probabilities, use `model_output="probability"` in TreeExplainer.

## Common Patterns

### Pattern 1: Complete Model Analysis

```python
# 1. Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 2. Global importance
shap.plots.beeswarm(shap_values)
shap.plots.bar(shap_values)

# 3. Top feature relationships
top_features = X_test.columns[np.abs(shap_values.values).mean(0).argsort()[-5:]]
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 4. Example predictions
for i in range(5):
    shap.plots.waterfall(shap_values[i])
```

### Pattern 2: Cohort Comparison

```python
# Define cohorts
cohort1_mask = X_test['Group'] == 'A'
cohort2_mask = X_test['Group'] == 'B'

# Compare feature importance
shap.plots.bar({
    "Group A": shap_values[cohort1_mask],
    "Group B": shap_values[cohort2_mask]
})
```

### Pattern 3: Debugging Errors

```python
# Find errors
errors = model.predict(X_test) != y_test
error_indices = np.where(errors)[0]

# Explain errors
for idx in error_indices[:5]:
    print(f"Sample {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # Investigate key features
    shap.plots.scatter(shap_values[:, "Suspicious_Feature"])
```

## Performance Optimization

### Speed Considerations

**Explainer Speed** (fastest to slowest):
1. `LinearExplainer` - Nearly instantaneous
2. `TreeExplainer` - Very fast
3. `DeepExplainer` - Fast for neural networks
4. `GradientExplainer` - Fast for neural networks
5. `KernelExplainer` - Slow (use only when necessary)
6. `PermutationExplainer` - Very slow but accurate

### Optimization Strategies

**For Large Datasets**:
```python
# Compute SHAP for subset
shap_values = explainer(X_test[:1000])

# Or use batching
batch_size = 100
all_shap_values = []
for i in range(0, len(X_test), batch_size):
    batch_shap = explainer(X_test[i:i+batch_size])
    all_shap_values.append(batch_shap)
```

**For Visualizations**:
```python
# Sample subset for plots
shap.plots.beeswarm(shap_values[:1000])

# Adjust transparency for dense plots
shap.plots.scatter(shap_values[:, "Feature"], alpha=0.3)
```

**For Production**:
```python
# Cache explainer
import joblib
joblib.dump(explainer, 'explainer.pkl')
explainer = joblib.load('explainer.pkl')

# Pre-compute for batch predictions
# Only compute top N features for API responses
```

## Troubleshooting

### Issue: Wrong explainer choice
**Problem**: Using KernelExplainer for tree models (slow and unnecessary)
**Solution**: Always use TreeExplainer for tree-based models

### Issue: Insufficient background data
**Problem**: DeepExplainer/KernelExplainer with too few background samples
**Solution**: Use 100-1000 representative samples

### Issue: Confusing units
**Problem**: Interpreting log-odds as probabilities
**Solution**: Check model output type; understand whether values are probabilities, log-odds, or raw outputs

### Issue: Plots don't display
**Problem**: Matplotlib backend issues
**Solution**: Ensure backend is set correctly; use `plt.show()` if needed

### Issue: Too many features cluttering plots
**Problem**: Default max_display=10 may be too many or too few
**Solution**: Adjust `max_display` parameter or use feature clustering

### Issue: Slow computation
**Problem**: Computing SHAP for very large datasets
**Solution**: Sample subset, use batching, or ensure using specialized explainer (not KernelExplainer)

## Integration with Other Tools

### Jupyter Notebooks
- Interactive force plots work seamlessly
- Inline plot display with `show=True` (default)
- Combine with markdown for narrative explanations

### MLflow / Experiment Tracking
```python
import mlflow

with mlflow.start_run():
    # Train model
    model = train_model(X_train, y_train)

    # Compute SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # Log plots
    shap.plots.beeswarm(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_beeswarm.png")
    plt.close()

    # Log feature importance metrics
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    for feature, importance in zip(X_test.columns, mean_abs_shap):
        mlflow.log_metric(f"shap_{feature}", importance)
```

### Production APIs
```python
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        prediction = self.model.predict(X)
        shap_values = self.explainer(X)

        return {
            'prediction': prediction[0],
            'base_value': shap_values.base_values[0],
            'feature_contributions': dict(zip(X.columns, shap_values.values[0]))
        }
```

## Reference Documentation

This skill includes comprehensive reference documentation organized by topic:

### references/explainers.md
Complete guide to all explainer classes:
- `TreeExplainer` - Fast, exact explanations for tree-based models
- `DeepExplainer` - Deep learning models (TensorFlow, PyTorch)
- `KernelExplainer` - Model-agnostic (works with any model)
- `LinearExplainer` - Fast explanations for linear models
- `GradientExplainer` - Gradient-based for neural networks
- `PermutationExplainer` - Exact but slow for any model

Includes: Constructor parameters, methods, supported models, when to use, examples, performance considerations.

### references/plots.md
Comprehensive visualization guide:
- **Waterfall plots** - Individual prediction breakdowns
- **Beeswarm plots** - Global importance with value distributions
- **Bar plots** - Clean feature importance summaries
- **Scatter plots** - Feature-prediction relationships and interactions
- **Force plots** - Interactive additive force visualizations
- **Heatmap plots** - Multi-sample comparison grids
- **Violin plots** - Distribution-focused alternatives
- **Decision plots** - Multiclass prediction paths

Includes: Parameters, use cases, examples, best practices, plot selection guide.

### references/workflows.md
Detailed workflows and best practices:
- Basic model explanation workflow
- Model debugging and validation
- Feature engineering guidance
- Model comparison and selection
- Fairness and bias analysis
- Deep learning model explanation
- Production deployment
- Time series model explanation
- Common pitfalls and solutions
- Advanced techniques
- MLOps integration

Includes: Step-by-step instructions, code examples, decision criteria, troubleshooting.

### references/theory.md
Theoretical foundations:
- Shapley values from game theory
- Mathematical formulas and properties
- Connection to other explanation methods (LIME, DeepLIFT, etc.)
- SHAP computation algorithms (Tree SHAP, Kernel SHAP, etc.)
- Conditional expectations and baseline selection
- Interpreting SHAP values
- Interaction values
- Theoretical limitations and considerations

Includes: Mathematical foundations, proofs, comparisons, advanced topics.

## Usage Guidelines

**When to load reference files**:
- Load `explainers.md` when user needs detailed information about specific explainer types or parameters
- Load `plots.md` when user needs detailed visualization guidance or exploring plot options
- Load `workflows.md` when user has complex multi-step tasks (debugging, fairness analysis, production deployment)
- Load `theory.md` when user asks about theoretical foundations, Shapley values, or mathematical details

**Default approach** (without loading references):
- Use this SKILL.md for basic explanations and quick start
- Provide standard workflows and common patterns
- Reference files are available if more detail is needed

**Loading references**:
```python
# To load reference files, use the Read tool with appropriate file path:
# /path/to/shap/references/explainers.md
# /path/to/shap/references/plots.md
# /path/to/shap/references/workflows.md
# /path/to/shap/references/theory.md
```

## Best Practices Summary

1. **Choose the right explainer**: Use specialized explainers (TreeExplainer, DeepExplainer, LinearExplainer) when possible; avoid KernelExplainer unless necessary

2. **Start global, then go local**: Begin with beeswarm/bar plots for overall understanding, then dive into waterfall/scatter plots for details

3. **Use multiple visualizations**: Different plots reveal different insights; combine global (beeswarm) + local (waterfall) + relationship (scatter) views

4. **Select appropriate background data**: Use 50-1000 representative samples from training data

5. **Understand model output units**: Know whether explaining probabilities, log-odds, or raw outputs

6. **Validate with domain knowledge**: SHAP shows model behavior; use domain expertise to interpret and validate

7. **Optimize for performance**: Sample subsets for visualization, batch for large datasets, cache explainers in production

8. **Check for data leakage**: Unexpectedly high feature importance may indicate data quality issues

9. **Consider feature correlations**: Use TreeExplainer's correlation-aware options or feature clustering for redundant features

10. **Remember SHAP shows association, not causation**: Use domain knowledge for causal interpretation

## Installation

```bash
# Basic installation
uv pip install shap

# With visualization dependencies
uv pip install shap matplotlib

# Latest version
uv pip install -U shap
```

**Dependencies**: numpy, pandas, scikit-learn, matplotlib, scipy

**Optional**: xgboost, lightgbm, tensorflow, torch (depending on model types)

## Additional Resources

- **Official Documentation**: https://shap.readthedocs.io/
- **GitHub Repository**: https://github.com/slundberg/shap
- **Original Paper**: Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions"
- **Nature MI Paper**: Lundberg et al. (2020) - "From local explanations to global understanding with explainable AI for trees"

This skill provides comprehensive coverage of SHAP for model interpretability across all use cases and model types.

---

## Reference: Explainers

# SHAP Explainers Reference

This document provides comprehensive information about all SHAP explainer classes, their parameters, methods, and when to use each type.

## Overview

SHAP provides specialized explainers for different model types, each optimized for specific architectures. The general `shap.Explainer` class automatically selects the appropriate algorithm based on the model type.

## Core Explainer Classes

### shap.Explainer (Auto-selector)

**Purpose**: Automatically uses Shapley values to explain any machine learning model or Python function by selecting the most appropriate explainer algorithm.

**Constructor Parameters**:
- `model`: The model to explain (function or model object)
- `masker`: Background data or masker object for feature manipulation
- `algorithm`: Optional override to force specific explainer type
- `output_names`: Names for model outputs
- `feature_names`: Names for input features

**When to Use**: Default choice when unsure which explainer to use; automatically selects the best algorithm based on model type.

### TreeExplainer

**Purpose**: Fast and exact SHAP value computation for tree-based ensemble models using the Tree SHAP algorithm.

**Constructor Parameters**:
- `model`: Tree-based model (XGBoost, LightGBM, CatBoost, PySpark, or scikit-learn trees)
- `data`: Background dataset for feature integration (optional with tree_path_dependent)
- `feature_perturbation`: How to handle dependent features
  - `"interventional"`: Requires background data; follows causal inference rules
  - `"tree_path_dependent"`: No background data needed; uses training examples per leaf
  - `"auto"`: Defaults to interventional if data provided, otherwise tree_path_dependent
- `model_output`: What model output to explain
  - `"raw"`: Standard model output (default)
  - `"probability"`: Probability-transformed output
  - `"log_loss"`: Natural log of loss function
  - Custom method names like `"predict_proba"`
- `feature_names`: Optional feature naming

**Supported Models**:
- XGBoost (xgboost.XGBClassifier, xgboost.XGBRegressor, xgboost.Booster)
- LightGBM (lightgbm.LGBMClassifier, lightgbm.LGBMRegressor, lightgbm.Booster)
- CatBoost (catboost.CatBoostClassifier, catboost.CatBoostRegressor)
- PySpark MLlib tree models
- scikit-learn (DecisionTreeClassifier, DecisionTreeRegressor, RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier, ExtraTreesRegressor, GradientBoostingClassifier, GradientBoostingRegressor)

**Key Methods**:
- `shap_values(X)`: Computes SHAP values for samples; returns arrays where each row represents feature attribution
- `shap_interaction_values(X)`: Estimates interaction effects between feature pairs; provides matrices with main effects and pairwise interactions
- `explain_row(row)`: Explains individual rows with detailed attribution information

**When to Use**:
- Primary choice for all tree-based models
- When exact SHAP values are needed (not approximations)
- When computational speed is important for large datasets
- For models like random forests, gradient boosting, or XGBoost

**Example**:
```python
import shap
import xgboost

# Train model
model = xgboost.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer.shap_values(X_test)

# Compute interaction values
shap_interaction = explainer.shap_interaction_values(X_test)
```

### DeepExplainer

**Purpose**: Approximates SHAP values for deep learning models using an enhanced version of the DeepLIFT algorithm.

**Constructor Parameters**:
- `model`: Framework-dependent specification
  - **TensorFlow**: Tuple of (input_tensor, output_tensor) where output is single-dimensional
  - **PyTorch**: `nn.Module` object or tuple of `(model, layer)` for layer-specific explanations
- `data`: Background dataset for feature integration
  - **TensorFlow**: numpy arrays or pandas DataFrames
  - **PyTorch**: torch tensors
  - **Recommended size**: 100-1000 samples (not full training set) to balance accuracy and computational cost
- `session` (TensorFlow only): Optional session object; auto-detected if None
- `learning_phase_flags`: Custom learning phase tensors for handling batch norm/dropout during inference

**Supported Frameworks**:
- **TensorFlow**: Full support including Keras models
- **PyTorch**: Complete integration with nn.Module architecture

**Key Methods**:
- `shap_values(X)`: Returns approximate SHAP values for the model applied to data X
- `explain_row(row)`: Explains single rows with attribution values and expected outputs
- `save(file)` / `load(file)`: Serialization support for explainer objects
- `supports_model_with_masker(model, masker)`: Compatibility checker for model types

**When to Use**:
- For deep neural networks in TensorFlow or PyTorch
- When working with convolutional neural networks (CNNs)
- For recurrent neural networks (RNNs) and transformers
- When model-specific explanation is needed for deep learning architectures

**Key Design Feature**:
Variance of expectation estimates scales approximately as 1/√N, where N is the number of background samples, enabling accuracy-efficiency trade-offs.

**Example**:
```python
import shap
import tensorflow as tf

# Assume model is a Keras model
model = tf.keras.models.load_model('my_model.h5')

# Select background samples (subset of training data)
background = X_train[:100]

# Create explainer
explainer = shap.DeepExplainer(model, background)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

### KernelExplainer

**Purpose**: Model-agnostic SHAP value computation using the Kernel SHAP method with weighted linear regression.

**Constructor Parameters**:
- `model`: Function or model object that takes a matrix of samples and returns model outputs
- `data`: Background dataset (numpy array, pandas DataFrame, or sparse matrix) used to simulate missing features
- `feature_names`: Optional list of feature names; automatically derived from DataFrame column names if available
- `link`: Connection function between feature importance and model output
  - `"identity"`: Direct relationship (default)
  - `"logit"`: For probability outputs

**Key Methods**:
- `shap_values(X, **kwargs)`: Calculates SHAP values for sample predictions
  - `nsamples`: Evaluation count per prediction ("auto" or integer); higher values reduce variance
  - `l1_reg`: Feature selection regularization ("num_features(int)", "aic", "bic", or float)
  - Returns arrays where each row sums to the difference between model output and expected value
- `explain_row(row)`: Explains individual predictions with attribution values and expected values
- `save(file)` / `load(file)`: Persist and restore explainer objects

**When to Use**:
- For black-box models where specialized explainers aren't available
- When working with custom prediction functions
- For any model type (neural networks, SVMs, ensemble methods, etc.)
- When model-agnostic explanations are needed
- **Note**: Slower than specialized explainers; use only when no specialized option exists

**Example**:
```python
import shap
from sklearn.svm import SVC

# Train model
model = SVC(probability=True).fit(X_train, y_train)

# Create prediction function
predict_fn = lambda x: model.predict_proba(x)[:, 1]

# Select background samples
background = shap.sample(X_train, 100)

# Create explainer
explainer = shap.KernelExplainer(predict_fn, background)

# Compute SHAP values (may be slow)
shap_values = explainer.shap_values(X_test[:10])
```

### LinearExplainer

**Purpose**: Specialized explainer for linear models that accounts for feature correlations.

**Constructor Parameters**:
- `model`: Linear model or tuple of (coefficients, intercept)
- `masker`: Background data for feature correlation
- `feature_perturbation`: How to handle feature correlations
  - `"interventional"`: Assumes feature independence
  - `"correlation_dependent"`: Accounts for feature correlations

**Supported Models**:
- scikit-learn linear models (LinearRegression, LogisticRegression, Ridge, Lasso, ElasticNet)
- Custom linear models with coefficients and intercept

**When to Use**:
- For linear regression and logistic regression models
- When feature correlations are important to explanation accuracy
- When extremely fast explanations are needed
- For GLMs and other linear model types

**Example**:
```python
import shap
from sklearn.linear_model import LogisticRegression

# Train model
model = LogisticRegression().fit(X_train, y_train)

# Create explainer
explainer = shap.LinearExplainer(model, X_train)

# Compute SHAP values
shap_values = explainer.shap_values(X_test)
```

### GradientExplainer

**Purpose**: Uses expected gradients to approximate SHAP values for neural networks.

**Constructor Parameters**:
- `model`: Deep learning model (TensorFlow or PyTorch)
- `data`: Background samples for integration
- `batch_size`: Batch size for gradient computation
- `local_smoothing`: Amount of noise to add for smoothing (default 0)

**When to Use**:
- As an alternative to DeepExplainer for neural networks
- When gradient-based explanations are preferred
- For differentiable models where gradient information is available

**Example**:
```python
import shap
import torch

# Assume model is a PyTorch model
model = torch.load('model.pt')

# Select background samples
background = X_train[:100]

# Create explainer
explainer = shap.GradientExplainer(model, background)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

### PermutationExplainer

**Purpose**: Approximates Shapley values by iterating through permutations of inputs.

**Constructor Parameters**:
- `model`: Prediction function
- `masker`: Background data or masker object
- `max_evals`: Maximum number of model evaluations per sample

**When to Use**:
- When exact Shapley values are needed but specialized explainers aren't available
- For small feature sets where permutation is tractable
- As a more accurate alternative to KernelExplainer (but slower)

**Example**:
```python
import shap

# Create explainer
explainer = shap.PermutationExplainer(model.predict, X_train)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

## Explainer Selection Guide

**Decision Tree for Choosing an Explainer**:

1. **Is your model tree-based?** (XGBoost, LightGBM, CatBoost, Random Forest, etc.)
   - Yes → Use `TreeExplainer` (fast and exact)
   - No → Continue to step 2

2. **Is your model a deep neural network?** (TensorFlow, PyTorch, Keras)
   - Yes → Use `DeepExplainer` or `GradientExplainer`
   - No → Continue to step 3

3. **Is your model linear?** (Linear/Logistic Regression, GLMs)
   - Yes → Use `LinearExplainer` (extremely fast)
   - No → Continue to step 4

4. **Do you need model-agnostic explanations?**
   - Yes → Use `KernelExplainer` (slower but works with any model)
   - If computational budget allows and high accuracy is needed → Use `PermutationExplainer`

5. **Unsure or want automatic selection?**
   - Use `shap.Explainer` (auto-selects best algorithm)

## Common Parameters Across Explainers

**Background Data / Masker**:
- Purpose: Represents the "typical" input to establish baseline expectations
- Size recommendations: 50-1000 samples (more for complex models)
- Selection: Random sample from training data or kmeans-selected representatives

**Feature Names**:
- Automatically extracted from pandas DataFrames
- Can be manually specified for numpy arrays
- Important for plot interpretability

**Model Output Specification**:
- Raw model output vs. transformed output (probabilities, log-odds)
- Critical for correct interpretation of SHAP values
- Example: For XGBoost classifiers, SHAP explains margin output (log-odds) before logistic transformation

## Performance Considerations

**Speed Ranking** (fastest to slowest):
1. `LinearExplainer` - Nearly instantaneous
2. `TreeExplainer` - Very fast, scales well
3. `DeepExplainer` - Fast for neural networks
4. `GradientExplainer` - Fast for neural networks
5. `KernelExplainer` - Slow, use only when necessary
6. `PermutationExplainer` - Very slow but most accurate for small feature sets

**Memory Considerations**:
- `TreeExplainer`: Low memory overhead
- `DeepExplainer`: Memory proportional to background sample size
- `KernelExplainer`: Can be memory-intensive for large background datasets
- For large datasets: Use batching or sample subsets

## Explainer Output: The Explanation Object

All explainers return `shap.Explanation` objects containing:
- `values`: SHAP values (numpy array)
- `base_values`: Expected model output (baseline)
- `data`: Original feature values
- `feature_names`: Names of features

The Explanation object supports:
- Slicing: `explanation[0]` for first sample
- Array operations: Compatible with numpy operations
- Direct plotting: Can be passed to plot functions

---

## Reference: Plots

# SHAP Visualization Reference

This document provides comprehensive information about all SHAP plotting functions, their parameters, use cases, and best practices for visualizing model explanations.

## Overview

SHAP provides diverse visualization tools for explaining model predictions at both individual and global levels. Each plot type serves specific purposes in understanding feature importance, interactions, and prediction mechanisms.

## Plot Types

### Waterfall Plots

**Purpose**: Display explanations for individual predictions, showing how each feature moves the prediction from the baseline (expected value) toward the final prediction.

**Function**: `shap.plots.waterfall(explanation, max_display=10, show=True)`

**Key Parameters**:
- `explanation`: Single row from an Explanation object (not multiple samples)
- `max_display`: Number of features to show (default: 10); less impactful features collapse into a single "other features" term
- `show`: Whether to display the plot immediately

**Visual Elements**:
- **X-axis**: Shows SHAP values (contribution to prediction)
- **Starting point**: Model's expected value (baseline)
- **Feature contributions**: Red bars (positive) or blue bars (negative) showing how each feature moves the prediction
- **Feature values**: Displayed in gray to the left of feature names
- **Ending point**: Final model prediction

**When to Use**:
- Explaining individual predictions in detail
- Understanding which features drove a specific decision
- Communicating model behavior for single instances (e.g., loan denial, diagnosis)
- Debugging unexpected predictions

**Important Notes**:
- For XGBoost classifiers, predictions are explained in log-odds units (margin output before logistic transformation)
- SHAP values sum to the difference between baseline and final prediction (additivity property)
- Use scatter plots alongside waterfall plots to explore patterns across multiple samples

**Example**:
```python
import shap

# Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Plot waterfall for first prediction
shap.plots.waterfall(shap_values[0])

# Show more features
shap.plots.waterfall(shap_values[0], max_display=20)
```

### Beeswarm Plots

**Purpose**: Information-dense summary of how top features impact model output across the entire dataset, combining feature importance with value distributions.

**Function**: `shap.plots.beeswarm(shap_values, max_display=10, order=Explanation.abs.mean(0), color=None, show=True)`

**Key Parameters**:
- `shap_values`: Explanation object containing multiple samples
- `max_display`: Number of features to display (default: 10)
- `order`: How to rank features
  - `Explanation.abs.mean(0)`: Mean absolute SHAP values (default)
  - `Explanation.abs.max(0)`: Maximum absolute values (highlights outlier impacts)
- `color`: matplotlib colormap; defaults to red-blue scheme
- `show`: Whether to display the plot immediately

**Visual Elements**:
- **Y-axis**: Features ranked by importance
- **X-axis**: SHAP value (impact on model output)
- **Each dot**: Single instance from dataset
- **Dot position (X)**: SHAP value magnitude
- **Dot color**: Original feature value (red = high, blue = low)
- **Dot clustering**: Shows density/distribution of impacts

**When to Use**:
- Summarizing feature importance across entire datasets
- Understanding both average and individual feature impacts
- Identifying feature value patterns and their effects
- Comparing global model behavior across features
- Detecting nonlinear relationships (e.g., higher age → lower income likelihood)

**Practical Variations**:
```python
# Standard beeswarm plot
shap.plots.beeswarm(shap_values)

# Show more features
shap.plots.beeswarm(shap_values, max_display=20)

# Order by maximum absolute values (highlight outliers)
shap.plots.beeswarm(shap_values, order=shap_values.abs.max(0))

# Plot absolute SHAP values with fixed coloring
shap.plots.beeswarm(shap_values.abs, color="shap_red")

# Custom matplotlib colormap
shap.plots.beeswarm(shap_values, color=plt.cm.viridis)
```

### Bar Plots

**Purpose**: Display feature importance as mean absolute SHAP values, providing clean, simple visualizations of global feature impact.

**Function**: `shap.plots.bar(shap_values, max_display=10, clustering=None, clustering_cutoff=0.5, show=True)`

**Key Parameters**:
- `shap_values`: Explanation object (can be single instance, global, or cohorts)
- `max_display`: Maximum number of features/bars to show
- `clustering`: Optional hierarchical clustering object from `shap.utils.hclust`
- `clustering_cutoff`: Threshold for displaying clustering structure (0-1, default: 0.5)

**Plot Types**:

#### Global Bar Plot
Shows overall feature importance across all samples. Importance calculated as mean absolute SHAP value.

```python
# Global feature importance
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)
shap.plots.bar(shap_values)
```

#### Local Bar Plot
Displays SHAP values for a single instance with feature values shown in gray.

```python
# Single prediction explanation
shap.plots.bar(shap_values[0])
```

#### Cohort Bar Plot
Compares feature importance across subgroups by passing a dictionary of Explanation objects.

```python
# Compare cohorts
cohorts = {
    "Group A": shap_values[mask_A],
    "Group B": shap_values[mask_B]
}
shap.plots.bar(cohorts)
```

**Feature Clustering**:
Identifies redundant features using model-based clustering (more accurate than correlation-based methods).

```python
# Add feature clustering
clustering = shap.utils.hclust(X_train, y_train)
shap.plots.bar(shap_values, clustering=clustering)

# Adjust clustering display threshold
shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=0.3)
```

**When to Use**:
- Quick overview of global feature importance
- Comparing feature importance across cohorts or models
- Identifying redundant or correlated features
- Clean, simple visualizations for presentations

### Force Plots

**Purpose**: Additive force visualization showing how features push prediction higher (red) or lower (blue) from baseline.

**Function**: `shap.plots.force(base_value, shap_values, features, feature_names=None, out_names=None, link="identity", matplotlib=False, show=True)`

**Key Parameters**:
- `base_value`: Expected value (baseline prediction)
- `shap_values`: SHAP values for sample(s)
- `features`: Feature values for sample(s)
- `feature_names`: Optional feature names
- `link`: Transform function ("identity" or "logit")
- `matplotlib`: Use matplotlib backend (default: interactive JavaScript)

**Visual Elements**:
- **Baseline**: Starting prediction (expected value)
- **Red arrows**: Features pushing prediction higher
- **Blue arrows**: Features pushing prediction lower
- **Final value**: Resulting prediction

**Interactive Features** (JavaScript mode):
- Hover for detailed feature information
- Multiple samples create stacked visualization
- Can rotate for different perspectives

**When to Use**:
- Interactive exploration of predictions
- Visualizing multiple predictions simultaneously
- Presentations requiring interactive elements
- Understanding prediction composition at a glance

**Example**:
```python
# Single prediction force plot
shap.plots.force(
    shap_values.base_values[0],
    shap_values.values[0],
    X_test.iloc[0],
    matplotlib=True
)

# Multiple predictions (interactive)
shap.plots.force(
    shap_values.base_values,
    shap_values.values,
    X_test
)
```

### Scatter Plots (Dependence Plots)

**Purpose**: Show relationship between feature values and their SHAP values, revealing how feature values impact predictions.

**Function**: `shap.plots.scatter(shap_values, color=None, hist=True, alpha=1, show=True)`

**Key Parameters**:
- `shap_values`: Explanation object, can specify feature with subscript (e.g., `shap_values[:, "Age"]`)
- `color`: Feature to use for coloring points (string name or Explanation object)
- `hist`: Show histogram of feature values on y-axis
- `alpha`: Point transparency (useful for dense plots)

**Visual Elements**:
- **X-axis**: Feature value
- **Y-axis**: SHAP value (impact on prediction)
- **Point color**: Another feature's value (for interaction detection)
- **Histogram**: Distribution of feature values

**When to Use**:
- Understanding feature-prediction relationships
- Detecting nonlinear effects
- Identifying feature interactions
- Validating or discovering patterns in model behavior
- Exploring counterintuitive predictions from waterfall plots

**Interaction Detection**:
Color points by another feature to reveal interactions.

```python
# Basic dependence plot
shap.plots.scatter(shap_values[:, "Age"])

# Color by another feature to show interactions
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])

# Multiple features in one plot
shap.plots.scatter(shap_values[:, ["Age", "Education", "Hours-per-week"]])

# Increase transparency for dense data
shap.plots.scatter(shap_values[:, "Age"], alpha=0.5)
```

### Heatmap Plots

**Purpose**: Visualize SHAP values for multiple samples simultaneously, showing feature impacts across instances.

**Function**: `shap.plots.heatmap(shap_values, instance_order=None, feature_values=None, max_display=10, show=True)`

**Key Parameters**:
- `shap_values`: Explanation object
- `instance_order`: How to order instances (can be Explanation object for custom ordering)
- `feature_values`: Display feature values on hover
- `max_display`: Maximum features to display

**Visual Elements**:
- **Rows**: Individual instances/samples
- **Columns**: Features
- **Cell color**: SHAP value (red = positive, blue = negative)
- **Intensity**: Magnitude of impact

**When to Use**:
- Comparing explanations across multiple instances
- Identifying patterns in feature impacts
- Understanding which features vary most across predictions
- Detecting subgroups or clusters with similar explanation patterns

**Example**:
```python
# Basic heatmap
shap.plots.heatmap(shap_values)

# Order instances by model output
shap.plots.heatmap(shap_values, instance_order=shap_values.sum(1))

# Show specific subset
shap.plots.heatmap(shap_values[:100])
```

### Violin Plots

**Purpose**: Similar to beeswarm plots but uses violin (kernel density) visualization instead of individual dots.

**Function**: `shap.plots.violin(shap_values, features=None, feature_names=None, max_display=10, show=True)`

**When to Use**:
- Alternative to beeswarm when dataset is very large
- Emphasizing distribution density over individual points
- Cleaner visualization for presentations

**Example**:
```python
shap.plots.violin(shap_values)
```

### Decision Plots

**Purpose**: Show prediction paths through cumulative SHAP values, particularly useful for multiclass classification.

**Function**: `shap.plots.decision(base_value, shap_values, features, feature_names=None, feature_order="importance", highlight=None, link="identity", show=True)`

**Key Parameters**:
- `base_value`: Expected value
- `shap_values`: SHAP values for samples
- `features`: Feature values
- `feature_order`: How to order features ("importance" or list)
- `highlight`: Indices of samples to highlight
- `link`: Transform function

**When to Use**:
- Multiclass classification explanations
- Understanding cumulative feature effects
- Comparing prediction paths across samples
- Identifying where predictions diverge

**Example**:
```python
# Decision plot for multiple predictions
shap.plots.decision(
    shap_values.base_values,
    shap_values.values,
    X_test,
    feature_names=X_test.columns.tolist()
)

# Highlight specific instances
shap.plots.decision(
    shap_values.base_values,
    shap_values.values,
    X_test,
    highlight=[0, 5, 10]
)
```

## Plot Selection Guide

**For Individual Predictions**:
- **Waterfall**: Best for detailed, sequential explanation
- **Force**: Good for interactive exploration
- **Bar (local)**: Simple, clean single-prediction importance

**For Global Understanding**:
- **Beeswarm**: Information-dense summary with value distributions
- **Bar (global)**: Clean, simple importance ranking
- **Violin**: Distribution-focused alternative to beeswarm

**For Feature Relationships**:
- **Scatter**: Understand feature-prediction relationships and interactions
- **Heatmap**: Compare patterns across multiple instances

**For Multiple Samples**:
- **Heatmap**: Grid view of SHAP values
- **Force (stacked)**: Interactive multi-sample visualization
- **Decision**: Prediction paths for multiclass problems

**For Cohort Comparison**:
- **Bar (cohort)**: Clean comparison of feature importance
- **Multiple beeswarms**: Side-by-side distribution comparisons

## Visualization Best Practices

**1. Start Global, Then Go Local**:
- Begin with beeswarm or bar plot to understand global patterns
- Dive into waterfall or scatter plots for specific instances or features

**2. Use Multiple Plot Types**:
- Different plots reveal different insights
- Combine waterfall (individual) + scatter (relationship) + beeswarm (global)

**3. Adjust max_display**:
- Default (10) is good for presentations
- Increase (20-30) for detailed analysis
- Consider clustering for redundant features

**4. Color Meaningfully**:
- Use default red-blue for SHAP values (red = positive, blue = negative)
- Color scatter plots by interacting features
- Custom colormaps for specific domains

**5. Consider Audience**:
- Technical audience: Beeswarm, scatter, heatmap
- Non-technical audience: Waterfall, bar, force plots
- Interactive presentations: Force plots with JavaScript

**6. Save High-Quality Figures**:
```python
import matplotlib.pyplot as plt

# Create plot
shap.plots.beeswarm(shap_values, show=False)

# Save with high DPI
plt.savefig('shap_plot.png', dpi=300, bbox_inches='tight')
plt.close()
```

**7. Handle Large Datasets**:
- Sample subset for visualization (e.g., `shap_values[:1000]`)
- Use violin instead of beeswarm for very large datasets
- Adjust alpha for scatter plots with many points

## Common Patterns and Workflows

**Pattern 1: Complete Model Explanation**
```python
# 1. Global importance
shap.plots.beeswarm(shap_values)

# 2. Top feature relationships
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 3. Example predictions
for i in interesting_indices:
    shap.plots.waterfall(shap_values[i])
```

**Pattern 2: Model Comparison**
```python
# Compute SHAP for multiple models
shap_model1 = explainer1(X_test)
shap_model2 = explainer2(X_test)

# Compare feature importance
shap.plots.bar({
    "Model 1": shap_model1,
    "Model 2": shap_model2
})
```

**Pattern 3: Subgroup Analysis**
```python
# Define cohorts
male_mask = X_test['Sex'] == 'Male'
female_mask = X_test['Sex'] == 'Female'

# Compare cohorts
shap.plots.bar({
    "Male": shap_values[male_mask],
    "Female": shap_values[female_mask]
})

# Separate beeswarm plots
shap.plots.beeswarm(shap_values[male_mask])
shap.plots.beeswarm(shap_values[female_mask])
```

**Pattern 4: Debugging Predictions**
```python
# Identify outliers or errors
errors = (model.predict(X_test) != y_test)
error_indices = np.where(errors)[0]

# Explain errors
for idx in error_indices[:5]:
    print(f"Sample {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # Explore key features
    shap.plots.scatter(shap_values[:, "Key_Feature"])
```

## Integration with Notebooks and Reports

**Jupyter Notebooks**:
- Interactive force plots work seamlessly
- Use `show=True` (default) for inline display
- Combine with markdown explanations

**Static Reports**:
- Use matplotlib backend for force plots
- Save figures programmatically
- Prefer waterfall and bar plots for clarity

**Web Applications**:
- Export force plots as HTML
- Use shap.save_html() for interactive visualizations
- Consider generating plots on-demand

## Troubleshooting Visualizations

**Issue**: Plots don't display
- **Solution**: Ensure matplotlib backend is set correctly; use `plt.show()` if needed

**Issue**: Too many features cluttering plot
- **Solution**: Reduce `max_display` parameter or use feature clustering

**Issue**: Colors reversed or confusing
- **Solution**: Check model output type (probability vs. log-odds) and use appropriate link function

**Issue**: Slow plotting with large datasets
- **Solution**: Sample subset of data; use `shap_values[:1000]` for visualization

**Issue**: Feature names missing
- **Solution**: Ensure feature_names are in Explanation object or pass explicitly to plot functions

---

## Reference: Theory

# SHAP Theoretical Foundation

This document explains the theoretical foundations of SHAP (SHapley Additive exPlanations), including Shapley values from game theory, the principles that make SHAP unique, and connections to other explanation methods.

## Game Theory Origins

### Shapley Values

SHAP is grounded in **Shapley values**, a solution concept from cooperative game theory developed by Lloyd Shapley in 1951.

**Core Concept**:
In cooperative game theory, players collaborate to achieve a total payoff, and the question is: how should this payoff be fairly distributed among players?

**Mapping to Machine Learning**:
- **Players** → Input features
- **Game** → Model prediction task
- **Payoff** → Model output (prediction value)
- **Coalition** → Subset of features with known values
- **Fair Distribution** → Attributing prediction to features

### The Shapley Value Formula

For a feature $i$, its Shapley value $\phi_i$ is:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F|-|S|-1)!}{|F|!} [f(S \cup \{i\}) - f(S)]$$

Where:
- $F$ is the set of all features
- $S$ is a subset of features not including $i$
- $f(S)$ is the model's expected output given only features in $S$
- $|S|$ is the size of subset $S$

**Interpretation**:
The Shapley value averages the marginal contribution of feature $i$ across all possible feature coalitions (subsets). The contribution is weighted by how likely each coalition is to occur.

### Key Properties of Shapley Values

**1. Efficiency (Additivity)**:
$$\sum_{i=1}^{n} \phi_i = f(x) - f(\emptyset)$$

The sum of all SHAP values equals the difference between the model's prediction for the instance and the expected value (baseline).

This is why SHAP waterfall plots always sum to the total prediction change.

**2. Symmetry**:
If two features $i$ and $j$ contribute equally to all coalitions, then $\phi_i = \phi_j$.

Features with identical effects receive identical attribution.

**3. Dummy**:
If a feature $i$ doesn't change the model output for any coalition, then $\phi_i = 0$.

Irrelevant features receive zero attribution.

**4. Monotonicity**:
If a feature's marginal contribution increases across coalitions, its Shapley value increases.

## From Game Theory to Machine Learning

### The Challenge

Computing exact Shapley values requires evaluating the model on all possible feature coalitions:
- For $n$ features, there are $2^n$ possible coalitions
- For 50 features, this is over 1 quadrillion evaluations

This exponential complexity makes exact computation intractable for most real-world models.

### SHAP's Solution: Additive Feature Attribution

SHAP connects Shapley values to **additive feature attribution methods**, enabling efficient computation.

**Additive Feature Attribution Model**:
$$g(z') = \phi_0 + \sum_{i=1}^{M} \phi_i z'_i$$

Where:
- $g$ is the explanation model
- $z' \in \{0,1\}^M$ indicates feature presence/absence
- $\phi_i$ is the attribution to feature $i$
- $\phi_0$ is the baseline (expected value)

SHAP proves that **Shapley values are the only attribution values satisfying three desirable properties**: local accuracy, missingness, and consistency.

## SHAP Properties and Guarantees

### Local Accuracy

**Property**: The explanation matches the model's output:
$$f(x) = g(x') = \phi_0 + \sum_{i=1}^{M} \phi_i x'_i$$

**Interpretation**: SHAP values exactly account for the model's prediction. This enables waterfall plots to precisely decompose predictions.

### Missingness

**Property**: If a feature is missing (not observed), its attribution is zero:
$$x'_i = 0 \Rightarrow \phi_i = 0$$

**Interpretation**: Only features that are present contribute to explanations.

### Consistency

**Property**: If a model changes so a feature's marginal contribution increases (or stays the same) for all inputs, that feature's attribution should not decrease.

**Interpretation**: If a feature becomes more important to the model, its SHAP value reflects this. This enables meaningful model comparisons.

## SHAP as a Unified Framework

SHAP unifies several existing explanation methods by showing they're special cases of Shapley values under specific assumptions.

### LIME (Local Interpretable Model-agnostic Explanations)

**LIME's Approach**: Fit a local linear model around a prediction using perturbed samples.

**Connection to SHAP**: LIME approximates Shapley values but with suboptimal sample weighting. SHAP uses theoretically optimal weights derived from Shapley value formula.

**Key Difference**: LIME's loss function and sampling don't guarantee consistency or exact additivity; SHAP does.

### DeepLIFT

**DeepLIFT's Approach**: Backpropagate contributions through neural networks by comparing to reference activations.

**Connection to SHAP**: DeepExplainer uses DeepLIFT but averages over multiple reference samples to approximate conditional expectations, yielding Shapley values.

### Layer-Wise Relevance Propagation (LRP)

**LRP's Approach**: Decompose neural network predictions by propagating relevance scores backward through layers.

**Connection to SHAP**: LRP is a special case of SHAP with specific propagation rules. SHAP generalizes these rules with Shapley value theory.

### Integrated Gradients

**Integrated Gradients' Approach**: Integrate gradients along path from baseline to input.

**Connection to SHAP**: When using a single reference point, Integrated Gradients approximates SHAP values for smooth models.

## SHAP Computation Methods

Different SHAP explainers use specialized algorithms to compute Shapley values efficiently for specific model types.

### Tree SHAP (TreeExplainer)

**Innovation**: Exploits tree structure to compute exact Shapley values in polynomial time instead of exponential.

**Algorithm**:
- Traverses each tree path from root to leaf
- Computes feature contributions using tree splits and weights
- Aggregates across all trees in ensemble

**Complexity**: $O(TLD^2)$ where $T$ = number of trees, $L$ = max leaves, $D$ = max depth

**Key Advantage**: Exact Shapley values computed efficiently for tree-based models (XGBoost, LightGBM, Random Forest, etc.)

### Kernel SHAP (KernelExplainer)

**Innovation**: Uses weighted linear regression to estimate Shapley values for any model.

**Algorithm**:
- Samples coalitions (feature subsets) according to Shapley kernel weights
- Evaluates model on each coalition (missing features replaced by background values)
- Fits weighted linear model to estimate feature attributions

**Complexity**: $O(n \cdot 2^M)$ but approximates with fewer samples

**Key Advantage**: Model-agnostic; works with any prediction function

**Trade-off**: Slower than specialized explainers; approximate rather than exact

### Deep SHAP (DeepExplainer)

**Innovation**: Combines DeepLIFT with Shapley value sampling.

**Algorithm**:
- Computes DeepLIFT attributions for each reference sample
- Averages attributions across multiple reference samples
- Approximates conditional expectations: $E[f(x) | x_S]$

**Complexity**: $O(n \cdot m)$ where $m$ = number of reference samples

**Key Advantage**: Efficiently approximates Shapley values for deep neural networks

### Linear SHAP (LinearExplainer)

**Innovation**: Closed-form Shapley values for linear models.

**Algorithm**:
- For independent features: $\phi_i = w_i \cdot (x_i - E[x_i])$
- For correlated features: Adjusts for feature covariance

**Complexity**: $O(n)$ - nearly instantaneous

**Key Advantage**: Exact Shapley values with minimal computation

## Understanding Conditional Expectations

### The Core Challenge

Computing $f(S)$ (model output given only features in $S$) requires handling missing features.

**Question**: How should we represent "missing" features when the model requires all features as input?

### Two Approaches

**1. Interventional (Marginal) Approach**:
- Replace missing features with values from background dataset
- Estimates: $E[f(x) | x_S]$ by marginalizing over $x_{\bar{S}}$
- Interpretation: "What would the model predict if we didn't know features $\bar{S}$?"

**2. Observational (Conditional) Approach**:
- Use conditional distribution: $E[f(x) | x_S = x_S^*]$
- Accounts for feature dependencies
- Interpretation: "What would the model predict for similar instances with features $S = x_S^*$?"

**Trade-offs**:
- **Interventional**: Simpler, assumes feature independence, matches causal interpretation
- **Observational**: More accurate for correlated features, requires conditional distribution estimation

**TreeExplainer** supports both via `feature_perturbation` parameter.

## Baseline (Expected Value) Selection

The **baseline** $\phi_0 = E[f(x)]$ represents the model's average prediction.

### Computing the Baseline

**For TreeExplainer**:
- With background data: Average prediction on background dataset
- With tree_path_dependent: Weighted average using tree leaf distributions

**For DeepExplainer / KernelExplainer**:
- Average prediction on background samples

### Importance of Baseline

- SHAP values measure deviation from baseline
- Different baselines → different SHAP values (but still sum correctly)
- Choose baseline representative of "typical" or "neutral" input
- Common choices: Training set mean, median, or mode

## Interpreting SHAP Values

### Units and Scale

**SHAP values have the same units as the model output**:
- Regression: Same units as target variable (dollars, temperature, etc.)
- Classification (log-odds): Log-odds units
- Classification (probability): Probability units (if model output transformed)

**Magnitude**: Higher absolute SHAP value = stronger feature impact

**Sign**:
- Positive SHAP value = Feature pushes prediction higher
- Negative SHAP value = Feature pushes prediction lower

### Additive Decomposition

For a prediction $f(x)$:
$$f(x) = E[f(X)] + \sum_{i=1}^{n} \phi_i(x)$$

**Example**:
- Expected value (baseline): 0.3
- SHAP values: {Age: +0.15, Income: +0.10, Education: -0.05}
- Prediction: $0.3 + 0.15 + 0.10 - 0.05 = 0.50$

### Global vs. Local Importance

**Local (Instance-level)**:
- SHAP values for single prediction: $\phi_i(x)$
- Explains: "Why did the model predict $f(x)$ for this instance?"
- Visualization: Waterfall, force plots

**Global (Dataset-level)**:
- Average absolute SHAP values: $E[|\phi_i(x)|]$
- Explains: "Which features are most important overall?"
- Visualization: Beeswarm, bar plots

**Key Insight**: Global importance is the aggregation of local importances, maintaining consistency between instance and dataset explanations.

## SHAP vs. Other Feature Importance Methods

### Comparison with Permutation Importance

**Permutation Importance**:
- Shuffles a feature and measures accuracy drop
- Global metric only (no instance-level explanations)
- Can be misleading with correlated features

**SHAP**:
- Provides both local and global importance
- Handles feature correlations through coalitional averaging
- Consistent: Additive property guarantees sum to prediction

### Comparison with Feature Coefficients (Linear Models)

**Feature Coefficients** ($w_i$):
- Measure impact per unit change in feature
- Don't account for feature scale or distribution

**SHAP for Linear Models**:
- $\phi_i = w_i \cdot (x_i - E[x_i])$
- Accounts for feature value relative to average
- More interpretable for comparing features with different units/scales

### Comparison with Tree Feature Importance (Gini/Split-based)

**Gini/Split Importance**:
- Based on training process (purity gain or frequency of splits)
- Biased toward high-cardinality features
- No instance-level explanations
- Can be misleading (importance ≠ predictive power)

**SHAP (Tree SHAP)**:
- Based on model output (prediction behavior)
- Fair attribution through Shapley values
- Provides instance-level explanations
- Consistent and theoretically grounded

## Interactions and Higher-Order Effects

### SHAP Interaction Values

Standard SHAP captures main effects. **SHAP interaction values** capture pairwise interactions.

**Formula for Interaction**:
$$\phi_{i,j} = \sum_{S \subseteq F \setminus \{i,j\}} \frac{|S|!(|F|-|S|-2)!}{2(|F|-1)!} \Delta_{ij}(S)$$

Where $\Delta_{ij}(S)$ is the interaction effect of features $i$ and $j$ given coalition $S$.

**Interpretation**:
- $\phi_{i,i}$: Main effect of feature $i$
- $\phi_{i,j}$ ($i \neq j$): Interaction effect between features $i$ and $j$

**Property**:
$$\phi_i = \phi_{i,i} + \sum_{j \neq i} \phi_{i,j}$$

Main SHAP value equals main effect plus half of all pairwise interactions involving feature $i$.

### Computing Interactions

**TreeExplainer** supports exact interaction computation:
```python
explainer = shap.TreeExplainer(model)
shap_interaction_values = explainer.shap_interaction_values(X)
```

**Limitation**: Exponentially complex for other explainers (only practical for tree models)

## Theoretical Limitations and Considerations

### Computational Complexity

**Exact Computation**: $O(2^n)$ - intractable for large $n$

**Specialized Algorithms**:
- Tree SHAP: $O(TLD^2)$ - efficient for trees
- Deep SHAP, Kernel SHAP: Approximations required

**Implication**: For non-tree models with many features, explanations may be approximate.

### Feature Independence Assumption

**Kernel SHAP and Basic Implementation**: Assume features can be independently manipulated

**Challenge**: Real features are often correlated (e.g., height and weight)

**Solutions**:
- Use observational approach (conditional expectations)
- TreeExplainer with correlation-aware perturbation
- Feature grouping for highly correlated features

### Out-of-Distribution Samples

**Issue**: Creating coalitions by replacing features may create unrealistic samples (outside training distribution)

**Example**: Setting "Age=5" and "Has PhD=Yes" simultaneously

**Implication**: SHAP values reflect model behavior on potentially unrealistic inputs

**Mitigation**: Use observational approach or carefully selected background data

### Causality

**SHAP measures association, not causation**

SHAP answers: "How does the model's prediction change with this feature?"
SHAP does NOT answer: "What would happen if we changed this feature in reality?"

**Example**:
- SHAP: "Hospital stay length increases prediction of mortality" (association)
- Causality: "Longer hospital stays cause higher mortality" (incorrect!)

**Implication**: Use domain knowledge to interpret SHAP causally; SHAP alone doesn't establish causation.

## Advanced Theoretical Topics

### SHAP as Optimal Credit Allocation

SHAP is the unique attribution method satisfying:
1. **Local accuracy**: Explanation matches model
2. **Missingness**: Absent features have zero attribution
3. **Consistency**: Attribution reflects feature importance changes

**Proof**: Lundberg & Lee (2017) showed Shapley values are the only solution satisfying these axioms.

### Connection to Functional ANOVA

SHAP values correspond to first-order terms in functional ANOVA decomposition:
$$f(x) = f_0 + \sum_i f_i(x_i) + \sum_{i,j} f_{ij}(x_i, x_j) + ...$$

Where $f_i(x_i)$ captures main effect of feature $i$, and $\phi_i \approx f_i(x_i)$.

### Relationship to Sensitivity Analysis

SHAP generalizes sensitivity analysis:
- **Sensitivity Analysis**: $\frac{\partial f}{\partial x_i}$ (local gradient)
- **SHAP**: Integrated sensitivity over feature coalition space

Gradient-based methods (GradientExplainer, Integrated Gradients) approximate SHAP using derivatives.

## Practical Implications of Theory

### Why Use SHAP?

1. **Theoretical Guarantees**: Only method with consistency, local accuracy, and missingness
2. **Unified Framework**: Connects and generalizes multiple explanation methods
3. **Additive Decomposition**: Predictions precisely decompose into feature contributions
4. **Model Comparison**: Consistency enables comparing feature importance across models
5. **Versatility**: Works with any model type (with appropriate explainer)

### When to Be Cautious

1. **Computational Cost**: May be slow for complex models without specialized explainers
2. **Feature Correlation**: Standard approaches may create unrealistic samples
3. **Interpretation**: Requires understanding baseline, units, and assumptions
4. **Causality**: SHAP doesn't imply causation; use domain knowledge
5. **Approximations**: Non-tree methods use approximations; understand accuracy trade-offs

## References and Further Reading

**Foundational Papers**:
- Shapley, L. S. (1951). "A value for n-person games"
- Lundberg, S. M., & Lee, S. I. (2017). "A Unified Approach to Interpreting Model Predictions" (NeurIPS)
- Lundberg, S. M., et al. (2020). "From local explanations to global understanding with explainable AI for trees" (Nature Machine Intelligence)

**Key Concepts**:
- Cooperative game theory and Shapley values
- Additive feature attribution methods
- Conditional expectation estimation
- Tree SHAP algorithm and polynomial-time computation

This theoretical foundation explains why SHAP is a principled, versatile, and powerful tool for model interpretation.

---

## Reference: Workflows

# SHAP Workflows and Best Practices

This document provides comprehensive workflows, best practices, and common use cases for using SHAP in various model interpretation scenarios.

## Basic Workflow Structure

Every SHAP analysis follows a general workflow:

1. **Train Model**: Build and train the machine learning model
2. **Select Explainer**: Choose appropriate explainer based on model type
3. **Compute SHAP Values**: Generate explanations for test samples
4. **Visualize Results**: Use plots to understand feature impacts
5. **Interpret and Act**: Draw conclusions and make decisions

## Workflow 1: Basic Model Explanation

**Use Case**: Understanding feature importance and prediction behavior for a trained model

```python
import shap
import pandas as pd
from sklearn.model_selection import train_test_split

# Step 1: Load and split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Step 2: Train model (example with XGBoost)
import xgboost as xgb
model = xgb.XGBClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# Step 3: Create explainer
explainer = shap.TreeExplainer(model)

# Step 4: Compute SHAP values
shap_values = explainer(X_test)

# Step 5: Visualize global importance
shap.plots.beeswarm(shap_values, max_display=15)

# Step 6: Examine top features in detail
shap.plots.scatter(shap_values[:, "Feature1"])
shap.plots.scatter(shap_values[:, "Feature2"], color=shap_values[:, "Feature1"])

# Step 7: Explain individual predictions
shap.plots.waterfall(shap_values[0])
```

**Key Decisions**:
- Explainer type based on model architecture
- Background dataset size (for DeepExplainer, KernelExplainer)
- Number of samples to explain (all test set vs. subset)

## Workflow 2: Model Debugging and Validation

**Use Case**: Identifying and fixing model issues, validating expected behavior

```python
# Step 1: Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Step 2: Identify prediction errors
predictions = model.predict(X_test)
errors = predictions != y_test
error_indices = np.where(errors)[0]

# Step 3: Analyze errors
print(f"Total errors: {len(error_indices)}")
print(f"Error rate: {len(error_indices) / len(y_test):.2%}")

# Step 4: Explain misclassified samples
for idx in error_indices[:10]:  # First 10 errors
    print(f"\n=== Error {idx} ===")
    print(f"Prediction: {predictions[idx]}, Actual: {y_test.iloc[idx]}")
    shap.plots.waterfall(shap_values[idx])

# Step 5: Check if model learned correct patterns
# Look for unexpected feature importance
shap.plots.beeswarm(shap_values)

# Step 6: Investigate specific feature relationships
# Verify nonlinear relationships make sense
for feature in model.feature_importances_.argsort()[-5:]:  # Top 5 features
    feature_name = X_test.columns[feature]
    shap.plots.scatter(shap_values[:, feature_name])

# Step 7: Validate feature interactions
# Check if interactions align with domain knowledge
shap.plots.scatter(shap_values[:, "Feature1"], color=shap_values[:, "Feature2"])
```

**Common Issues to Check**:
- Data leakage (feature with suspiciously high importance)
- Spurious correlations (unexpected feature relationships)
- Target leakage (features that shouldn't be predictive)
- Biases (disproportionate impact on certain groups)

## Workflow 3: Feature Engineering Guidance

**Use Case**: Using SHAP insights to improve feature engineering

```python
# Step 1: Initial model with baseline features
model_v1 = train_model(X_train_v1, y_train)
explainer_v1 = shap.TreeExplainer(model_v1)
shap_values_v1 = explainer_v1(X_test_v1)

# Step 2: Identify feature engineering opportunities
shap.plots.beeswarm(shap_values_v1)

# Check for:
# - Nonlinear relationships (candidates for transformation)
shap.plots.scatter(shap_values_v1[:, "Age"])  # Maybe age^2 or age bins?

# - Feature interactions (candidates for interaction terms)
shap.plots.scatter(shap_values_v1[:, "Income"], color=shap_values_v1[:, "Education"])
# Maybe create Income * Education interaction?

# Step 3: Engineer new features based on insights
X_train_v2 = X_train_v1.copy()
X_train_v2['Age_squared'] = X_train_v2['Age'] ** 2
X_train_v2['Income_Education'] = X_train_v2['Income'] * X_train_v2['Education']

# Step 4: Retrain with engineered features
model_v2 = train_model(X_train_v2, y_train)
explainer_v2 = shap.TreeExplainer(model_v2)
shap_values_v2 = explainer_v2(X_test_v2)

# Step 5: Compare feature importance
shap.plots.bar({
    "Baseline": shap_values_v1,
    "With Engineered Features": shap_values_v2
})

# Step 6: Validate improvement
print(f"V1 Score: {model_v1.score(X_test_v1, y_test):.4f}")
print(f"V2 Score: {model_v2.score(X_test_v2, y_test):.4f}")
```

**Feature Engineering Insights from SHAP**:
- Strong nonlinear patterns → Try transformations (log, sqrt, polynomial)
- Color-coded interactions in scatter → Create interaction terms
- Redundant features in clustering → Remove or combine
- Unexpected importance → Investigate for data quality issues

## Workflow 4: Model Comparison and Selection

**Use Case**: Comparing multiple models to select the best interpretable model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb

# Step 1: Train multiple models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000).fit(X_train, y_train),
    'Random Forest': RandomForestClassifier(n_estimators=100).fit(X_train, y_train),
    'XGBoost': xgb.XGBClassifier(n_estimators=100).fit(X_train, y_train)
}

# Step 2: Compute SHAP values for each model
shap_values_dict = {}
for name, model in models.items():
    if name == 'Logistic Regression':
        explainer = shap.LinearExplainer(model, X_train)
    else:
        explainer = shap.TreeExplainer(model)
    shap_values_dict[name] = explainer(X_test)

# Step 3: Compare global feature importance
shap.plots.bar(shap_values_dict)

# Step 4: Compare model scores
for name, model in models.items():
    score = model.score(X_test, y_test)
    print(f"{name}: {score:.4f}")

# Step 5: Check consistency of feature importance
for feature in X_test.columns[:5]:  # Top 5 features
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for idx, (name, shap_vals) in enumerate(shap_values_dict.items()):
        plt.sca(axes[idx])
        shap.plots.scatter(shap_vals[:, feature], show=False)
        plt.title(f"{name} - {feature}")
    plt.tight_layout()
    plt.show()

# Step 6: Analyze specific predictions across models
sample_idx = 0
for name, shap_vals in shap_values_dict.items():
    print(f"\n=== {name} ===")
    shap.plots.waterfall(shap_vals[sample_idx])

# Step 7: Decision based on:
# - Accuracy/Performance
# - Interpretability (consistent feature importance)
# - Deployment constraints
# - Stakeholder requirements
```

**Model Selection Criteria**:
- **Accuracy vs. Interpretability**: Sometimes simpler models with SHAP are preferable
- **Feature Consistency**: Models agreeing on feature importance are more trustworthy
- **Explanation Quality**: Clear, actionable explanations
- **Computational Cost**: TreeExplainer is faster than KernelExplainer

## Workflow 5: Fairness and Bias Analysis

**Use Case**: Detecting and analyzing model bias across demographic groups

```python
# Step 1: Identify protected attributes
protected_attr = 'Gender'  # or 'Race', 'Age_Group', etc.

# Step 2: Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Step 3: Compare feature importance across groups
groups = X_test[protected_attr].unique()
cohorts = {
    f"{protected_attr}={group}": shap_values[X_test[protected_attr] == group]
    for group in groups
}
shap.plots.bar(cohorts)

# Step 4: Check if protected attribute has high SHAP importance
# (should be low/zero for fair models)
protected_importance = np.abs(shap_values[:, protected_attr].values).mean()
print(f"{protected_attr} mean |SHAP|: {protected_importance:.4f}")

# Step 5: Analyze predictions for each group
for group in groups:
    mask = X_test[protected_attr] == group
    group_shap = shap_values[mask]

    print(f"\n=== {protected_attr} = {group} ===")
    print(f"Sample size: {mask.sum()}")
    print(f"Positive prediction rate: {(model.predict(X_test[mask]) == 1).mean():.2%}")

    # Visualize
    shap.plots.beeswarm(group_shap, max_display=10)

# Step 6: Check for proxy features
# Features correlated with protected attribute that shouldn't have high importance
# Example: 'Zip_Code' might be proxy for race
proxy_features = ['Zip_Code', 'Last_Name_Prefix']  # Domain-specific
for feature in proxy_features:
    if feature in X_test.columns:
        importance = np.abs(shap_values[:, feature].values).mean()
        print(f"Potential proxy '{feature}' importance: {importance:.4f}")

# Step 7: Mitigation strategies if bias found
# - Remove protected attribute and proxies
# - Add fairness constraints during training
# - Post-process predictions to equalize outcomes
# - Use different model architecture
```

**Fairness Metrics to Check**:
- **Demographic Parity**: Similar positive prediction rates across groups
- **Equal Opportunity**: Similar true positive rates across groups
- **Feature Importance Parity**: Similar feature rankings across groups
- **Protected Attribute Importance**: Should be minimal

## Workflow 6: Deep Learning Model Explanation

**Use Case**: Explaining neural network predictions with DeepExplainer

```python
import tensorflow as tf
import shap

# Step 1: Load or build neural network
model = tf.keras.models.load_model('my_model.h5')

# Step 2: Select background dataset
# Use subset (100-1000 samples) from training data
background = X_train[:100]

# Step 3: Create DeepExplainer
explainer = shap.DeepExplainer(model, background)

# Step 4: Compute SHAP values (may take time)
# Explain subset of test data
test_subset = X_test[:50]
shap_values = explainer.shap_values(test_subset)

# Step 5: Handle multi-output models
# For binary classification, shap_values is a list [class_0_values, class_1_values]
# For regression, it's a single array
if isinstance(shap_values, list):
    # Focus on positive class
    shap_values_positive = shap_values[1]
    shap_exp = shap.Explanation(
        values=shap_values_positive,
        base_values=explainer.expected_value[1],
        data=test_subset
    )
else:
    shap_exp = shap.Explanation(
        values=shap_values,
        base_values=explainer.expected_value,
        data=test_subset
    )

# Step 6: Visualize
shap.plots.beeswarm(shap_exp)
shap.plots.waterfall(shap_exp[0])

# Step 7: For image/text data, use specialized plots
# Image: shap.image_plot
# Text: shap.plots.text (for transformers)
```

**Deep Learning Considerations**:
- Background dataset size affects accuracy and speed
- Multi-output handling (classification vs. regression)
- Specialized plots for image/text data
- Computational cost (consider GPU acceleration)

## Workflow 7: Production Deployment

**Use Case**: Integrating SHAP explanations into production systems

```python
import joblib
import shap

# Step 1: Train and save model
model = train_model(X_train, y_train)
joblib.dump(model, 'model.pkl')

# Step 2: Create and save explainer
explainer = shap.TreeExplainer(model)
joblib.dump(explainer, 'explainer.pkl')

# Step 3: Create explanation service
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        """
        Returns prediction and explanation
        """
        # Prediction
        prediction = self.model.predict(X)

        # SHAP values
        shap_values = self.explainer(X)

        # Format explanation
        explanations = []
        for i in range(len(X)):
            exp = {
                'prediction': prediction[i],
                'base_value': shap_values.base_values[i],
                'shap_values': dict(zip(X.columns, shap_values.values[i])),
                'feature_values': X.iloc[i].to_dict()
            }
            explanations.append(exp)

        return explanations

    def get_top_features(self, X, n=5):
        """
        Returns top N features for each prediction
        """
        shap_values = self.explainer(X)

        top_features = []
        for i in range(len(X)):
            # Get absolute SHAP values
            abs_shap = np.abs(shap_values.values[i])

            # Sort and get top N
            top_indices = abs_shap.argsort()[-n:][::-1]
            top_feature_names = X.columns[top_indices].tolist()
            top_shap_values = shap_values.values[i][top_indices].tolist()

            top_features.append({
                'features': top_feature_names,
                'shap_values': top_shap_values
            })

        return top_features

# Step 4: Usage in API
service = ExplanationService('model.pkl', 'explainer.pkl')

# Example API endpoint
def predict_endpoint(input_data):
    X = pd.DataFrame([input_data])
    explanations = service.predict_with_explanation(X)
    return {
        'prediction': explanations[0]['prediction'],
        'explanation': explanations[0]
    }

# Step 5: Generate static explanations for batch predictions
def batch_explain_and_save(X_batch, output_dir):
    shap_values = explainer(X_batch)

    # Save global plot
    shap.plots.beeswarm(shap_values, show=False)
    plt.savefig(f'{output_dir}/global_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Save individual explanations
    for i in range(min(100, len(X_batch))):  # First 100
        shap.plots.waterfall(shap_values[i], show=False)
        plt.savefig(f'{output_dir}/explanation_{i}.png', dpi=300, bbox_inches='tight')
        plt.close()
```

**Production Best Practices**:
- Cache explainers to avoid recomputation
- Batch explanations when possible
- Limit explanation complexity (top N features)
- Monitor explanation latency
- Version explainers alongside models
- Consider pre-computing explanations for common inputs

## Workflow 8: Time Series Model Explanation

**Use Case**: Explaining time series forecasting models

```python
# Step 1: Prepare data with time-based features
# Example: Predicting next day's sales
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['Lag_1'] = df['Sales'].shift(1)
df['Lag_7'] = df['Sales'].shift(7)
df['Rolling_Mean_7'] = df['Sales'].rolling(7).mean()

# Step 2: Train model
features = ['DayOfWeek', 'Month', 'Lag_1', 'Lag_7', 'Rolling_Mean_7']
X_train, X_test, y_train, y_test = train_test_split(df[features], df['Sales'])
model = xgb.XGBRegressor().fit(X_train, y_train)

# Step 3: Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Step 4: Analyze temporal patterns
# Which features drive predictions at different times?
shap.plots.beeswarm(shap_values)

# Step 5: Check lagged feature importance
# Lag features should have high importance for time series
lag_features = ['Lag_1', 'Lag_7', 'Rolling_Mean_7']
for feature in lag_features:
    shap.plots.scatter(shap_values[:, feature])

# Step 6: Explain specific predictions
# E.g., why was Monday's forecast so different?
monday_mask = X_test['DayOfWeek'] == 0
shap.plots.waterfall(shap_values[monday_mask][0])

# Step 7: Validate seasonality understanding
shap.plots.scatter(shap_values[:, 'Month'])
```

**Time Series Considerations**:
- Lagged features and their importance
- Rolling statistics interpretation
- Seasonal patterns in SHAP values
- Avoiding data leakage in feature engineering

## Common Pitfalls and Solutions

### Pitfall 1: Wrong Explainer Choice
**Problem**: Using KernelExplainer for tree models (slow and unnecessary)
**Solution**: Always use TreeExplainer for tree-based models

### Pitfall 2: Insufficient Background Data
**Problem**: DeepExplainer/KernelExplainer with too few background samples
**Solution**: Use 100-1000 representative samples

### Pitfall 3: Misinterpreting Log-Odds
**Problem**: Confusion about units (probability vs. log-odds)
**Solution**: Check model output type; use link="logit" when needed

### Pitfall 4: Ignoring Feature Correlations
**Problem**: Interpreting features as independent when they're correlated
**Solution**: Use feature clustering; understand domain relationships

### Pitfall 5: Overfitting to Explanations
**Problem**: Feature engineering based solely on SHAP without validation
**Solution**: Always validate improvements with cross-validation

### Pitfall 6: Data Leakage Undetected
**Problem**: Not noticing unexpected feature importance indicating leakage
**Solution**: Validate SHAP results against domain knowledge

### Pitfall 7: Computational Constraints Ignored
**Problem**: Computing SHAP for entire large dataset
**Solution**: Use sampling, batching, or subset analysis

## Advanced Techniques

### Technique 1: SHAP Interaction Values
Capture pairwise feature interactions:
```python
explainer = shap.TreeExplainer(model)
shap_interaction_values = explainer.shap_interaction_values(X_test)

# Analyze specific interaction
feature1_idx = 0
feature2_idx = 3
interaction = shap_interaction_values[:, feature1_idx, feature2_idx]
print(f"Interaction strength: {np.abs(interaction).mean():.4f}")
```

### Technique 2: Partial Dependence with SHAP
Combine partial dependence plots with SHAP:
```python
from sklearn.inspection import partial_dependence

# SHAP dependence
shap.plots.scatter(shap_values[:, "Feature1"])

# Partial dependence (model-agnostic)
pd_result = partial_dependence(model, X_test, features=["Feature1"])
plt.plot(pd_result['grid_values'][0], pd_result['average'][0])
```

### Technique 3: Conditional Expectations
Analyze SHAP values conditioned on other features:
```python
# High Income group
high_income = X_test['Income'] > X_test['Income'].median()
shap.plots.beeswarm(shap_values[high_income])

# Low Income group
low_income = X_test['Income'] <= X_test['Income'].median()
shap.plots.beeswarm(shap_values[low_income])
```

### Technique 4: Feature Clustering for Redundancy
```python
# Create hierarchical clustering
clustering = shap.utils.hclust(X_train, y_train)

# Visualize with clustering
shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=0.5)

# Identify redundant features to remove
# Features with distance < 0.1 are highly redundant
```

## Integration with MLOps

**Experiment Tracking**:
```python
import mlflow

# Log SHAP values
with mlflow.start_run():
    # Train model
    model = train_model(X_train, y_train)

    # Compute SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # Log plots
    shap.plots.beeswarm(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_beeswarm.png")
    plt.close()

    # Log feature importance as metrics
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    for feature, importance in zip(X_test.columns, mean_abs_shap):
        mlflow.log_metric(f"shap_{feature}", importance)
```

**Model Monitoring**:
```python
# Track SHAP distribution drift over time
def compute_shap_summary(shap_values):
    return {
        'mean': shap_values.values.mean(axis=0),
        'std': shap_values.values.std(axis=0),
        'percentiles': np.percentile(shap_values.values, [25, 50, 75], axis=0)
    }

# Compute baseline
baseline_summary = compute_shap_summary(shap_values_train)

# Monitor production data
production_summary = compute_shap_summary(shap_values_production)

# Detect drift
drift_detected = np.abs(
    production_summary['mean'] - baseline_summary['mean']
) > threshold
```

This comprehensive workflows document covers the most common and advanced use cases for SHAP in practice.
