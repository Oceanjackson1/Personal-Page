---
title: "Statistical Analysis"
description: "Guided statistical analysis with test selection and reporting. Use when you need help choosing appropriate tests for your data, assumption checking, power analysis, and APA-formatted results. Best for academic research reporting, test selection gu..."
category: "research"
source: "community"
author: "Community"
tags: ["statistical", "analysis"]
date: 2026-03-20
---

# Statistical Analysis

## Overview

Statistical analysis is a systematic process for testing hypotheses and quantifying relationships. Conduct hypothesis tests (t-test, ANOVA, chi-square), regression, correlation, and Bayesian analyses with assumption checks and APA reporting. Apply this skill for academic research.

## When to Use This Skill

This skill should be used when:
- Conducting statistical hypothesis tests (t-tests, ANOVA, chi-square)
- Performing regression or correlation analyses
- Running Bayesian statistical analyses
- Checking statistical assumptions and diagnostics
- Calculating effect sizes and conducting power analyses
- Reporting statistical results in APA format
- Analyzing experimental or observational data for research

---

## Core Capabilities

### 1. Test Selection and Planning
- Choose appropriate statistical tests based on research questions and data characteristics
- Conduct a priori power analyses to determine required sample sizes
- Plan analysis strategies including multiple comparison corrections

### 2. Assumption Checking
- Automatically verify all relevant assumptions before running tests
- Provide diagnostic visualizations (Q-Q plots, residual plots, box plots)
- Recommend remedial actions when assumptions are violated

### 3. Statistical Testing
- Hypothesis testing: t-tests, ANOVA, chi-square, non-parametric alternatives
- Regression: linear, multiple, logistic, with diagnostics
- Correlations: Pearson, Spearman, with confidence intervals
- Bayesian alternatives: Bayesian t-tests, ANOVA, regression with Bayes Factors

### 4. Effect Sizes and Interpretation
- Calculate and interpret appropriate effect sizes for all analyses
- Provide confidence intervals for effect estimates
- Distinguish statistical from practical significance

### 5. Professional Reporting
- Generate APA-style statistical reports
- Create publication-ready figures and tables
- Provide complete interpretation with all required statistics

---

## Workflow Decision Tree

Use this decision tree to determine your analysis path:

```
START
│
├─ Need to SELECT a statistical test?
│  └─ YES → See "Test Selection Guide"
│  └─ NO → Continue
│
├─ Ready to check ASSUMPTIONS?
│  └─ YES → See "Assumption Checking"
│  └─ NO → Continue
│
├─ Ready to run ANALYSIS?
│  └─ YES → See "Running Statistical Tests"
│  └─ NO → Continue
│
└─ Need to REPORT results?
   └─ YES → See "Reporting Results"
```

---

## Test Selection Guide

### Quick Reference: Choosing the Right Test

Use `references/test_selection_guide.md` for comprehensive guidance. Quick reference:

**Comparing Two Groups:**
- Independent, continuous, normal → Independent t-test
- Independent, continuous, non-normal → Mann-Whitney U test
- Paired, continuous, normal → Paired t-test
- Paired, continuous, non-normal → Wilcoxon signed-rank test
- Binary outcome → Chi-square or Fisher's exact test

**Comparing 3+ Groups:**
- Independent, continuous, normal → One-way ANOVA
- Independent, continuous, non-normal → Kruskal-Wallis test
- Paired, continuous, normal → Repeated measures ANOVA
- Paired, continuous, non-normal → Friedman test

**Relationships:**
- Two continuous variables → Pearson (normal) or Spearman correlation (non-normal)
- Continuous outcome with predictor(s) → Linear regression
- Binary outcome with predictor(s) → Logistic regression

**Bayesian Alternatives:**
All tests have Bayesian versions that provide:
- Direct probability statements about hypotheses
- Bayes Factors quantifying evidence
- Ability to support null hypothesis
- See `references/bayesian_statistics.md`

---

## Assumption Checking

### Systematic Assumption Verification

**ALWAYS check assumptions before interpreting test results.**

Use the provided `scripts/assumption_checks.py` module for automated checking:

```python
from scripts.assumption_checks import comprehensive_assumption_check

# Comprehensive check with visualizations
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # Optional: for group comparisons
    alpha=0.05
)
```

This performs:
1. **Outlier detection** (IQR and z-score methods)
2. **Normality testing** (Shapiro-Wilk test + Q-Q plots)
3. **Homogeneity of variance** (Levene's test + box plots)
4. **Interpretation and recommendations**

### Individual Assumption Checks

For targeted checks, use individual functions:

```python
from scripts.assumption_checks import (
    check_normality,
    check_normality_per_group,
    check_homogeneity_of_variance,
    check_linearity,
    detect_outliers
)

# Example: Check normality with visualization
result = check_normality(
    data=df['score'],
    name='Test Score',
    alpha=0.05,
    plot=True
)
print(result['interpretation'])
print(result['recommendation'])
```

### What to Do When Assumptions Are Violated

**Normality violated:**
- Mild violation + n > 30 per group → Proceed with parametric test (robust)
- Moderate violation → Use non-parametric alternative
- Severe violation → Transform data or use non-parametric test

**Homogeneity of variance violated:**
- For t-test → Use Welch's t-test
- For ANOVA → Use Welch's ANOVA or Brown-Forsythe ANOVA
- For regression → Use robust standard errors or weighted least squares

**Linearity violated (regression):**
- Add polynomial terms
- Transform variables
- Use non-linear models or GAM

See `references/assumptions_and_diagnostics.md` for comprehensive guidance.

---

## Running Statistical Tests

### Python Libraries

Primary libraries for statistical analysis:
- **scipy.stats**: Core statistical tests
- **statsmodels**: Advanced regression and diagnostics
- **pingouin**: User-friendly statistical testing with effect sizes
- **pymc**: Bayesian statistical modeling
- **arviz**: Bayesian visualization and diagnostics

### Example Analyses

#### T-Test with Complete Reporting

```python
import pingouin as pg
import numpy as np

# Run independent t-test
result = pg.ttest(group_a, group_b, correction='auto')

# Extract results
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p-val'].values[0]
cohens_d = result['cohen-d'].values[0]
ci_lower = result['CI95%'].values[0][0]
ci_upper = result['CI95%'].values[0][1]

# Report
print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}")
print(f"Cohen's d = {cohens_d:.2f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}]")
```

#### ANOVA with Post-Hoc Tests

```python
import pingouin as pg

# One-way ANOVA
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# If significant, conduct post-hoc tests
if aov['p-unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)

# Effect size
eta_squared = aov['np2'].values[0]  # Partial eta-squared
print(f"Partial η² = {eta_squared:.3f}")
```

#### Linear Regression with Diagnostics

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Fit model
X = sm.add_constant(X_predictors)  # Add intercept
model = sm.OLS(y, X).fit()

# Summary
print(model.summary())

# Check multicollinearity (VIF)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Check assumptions
residuals = model.resid
fitted = model.fittedvalues

# Residual plots
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs fitted
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q plot
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Normal Q-Q')

# Scale-Location
axes[1, 0].scatter(fitted, np.sqrt(np.abs(residuals / residuals.std())), alpha=0.6)
axes[1, 0].set_xlabel('Fitted values')
axes[1, 0].set_ylabel('√|Standardized residuals|')
axes[1, 0].set_title('Scale-Location')

# Residuals histogram
axes[1, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Histogram of Residuals')

plt.tight_layout()
plt.show()
```

#### Bayesian T-Test

```python
import pymc as pm
import arviz as az
import numpy as np

with pm.Model() as model:
    # Priors
    mu1 = pm.Normal('mu_group1', mu=0, sigma=10)
    mu2 = pm.Normal('mu_group2', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group_a)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group_b)

    # Derived quantity
    diff = pm.Deterministic('difference', mu1 - mu2)

    # Sample
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Summarize
print(az.summary(trace, var_names=['difference']))

# Probability that group1 > group2
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(μ₁ > μ₂ | data) = {prob_greater:.3f}")

# Plot posterior
az.plot_posterior(trace, var_names=['difference'], ref_val=0)
```

---

## Effect Sizes

### Always Calculate Effect Sizes

**Effect sizes quantify magnitude, while p-values only indicate existence of an effect.**

See `references/effect_sizes_and_power.md` for comprehensive guidance.

### Quick Reference: Common Effect Sizes

| Test | Effect Size | Small | Medium | Large |
|------|-------------|-------|--------|-------|
| T-test | Cohen's d | 0.20 | 0.50 | 0.80 |
| ANOVA | η²_p | 0.01 | 0.06 | 0.14 |
| Correlation | r | 0.10 | 0.30 | 0.50 |
| Regression | R² | 0.02 | 0.13 | 0.26 |
| Chi-square | Cramér's V | 0.07 | 0.21 | 0.35 |

**Important**: Benchmarks are guidelines. Context matters!

### Calculating Effect Sizes

Most effect sizes are automatically calculated by pingouin:

```python
# T-test returns Cohen's d
result = pg.ttest(x, y)
d = result['cohen-d'].values[0]

# ANOVA returns partial eta-squared
aov = pg.anova(dv='score', between='group', data=df)
eta_p2 = aov['np2'].values[0]

# Correlation: r is already an effect size
corr = pg.corr(x, y)
r = corr['r'].values[0]
```

### Confidence Intervals for Effect Sizes

Always report CIs to show precision:

```python
from pingouin import compute_effsize_from_t

# For t-test
d, ci = compute_effsize_from_t(
    t_statistic,
    nx=len(group1),
    ny=len(group2),
    eftype='cohen'
)
print(f"d = {d:.2f}, 95% CI [{ci[0]:.2f}, {ci[1]:.2f}]")
```

---

## Power Analysis

### A Priori Power Analysis (Study Planning)

Determine required sample size before data collection:

```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    FTestAnovaPower
)

# T-test: What n is needed to detect d = 0.5?
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Required n per group: {n_required:.0f}")

# ANOVA: What n is needed to detect f = 0.25?
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,
    ngroups=3,
    alpha=0.05,
    power=0.80
)
print(f"Required n per group: {n_per_group:.0f}")
```

### Sensitivity Analysis (Post-Study)

Determine what effect size you could detect:

```python
# With n=50 per group, what effect could we detect?
detectable_d = tt_ind_solve_power(
    effect_size=None,  # Solve for this
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Study could detect d ≥ {detectable_d:.2f}")
```

**Note**: Post-hoc power analysis (calculating power after study) is generally not recommended. Use sensitivity analysis instead.

See `references/effect_sizes_and_power.md` for detailed guidance.

---

## Reporting Results

### APA Style Statistical Reporting

Follow guidelines in `references/reporting_standards.md`.

### Essential Reporting Elements

1. **Descriptive statistics**: M, SD, n for all groups/variables
2. **Test statistics**: Test name, statistic, df, exact p-value
3. **Effect sizes**: With confidence intervals
4. **Assumption checks**: Which tests were done, results, actions taken
5. **All planned analyses**: Including non-significant findings

### Example Report Templates

#### Independent T-Test

```
Group A (n = 48, M = 75.2, SD = 8.5) scored significantly higher than
Group B (n = 52, M = 68.3, SD = 9.2), t(98) = 3.82, p < .001, d = 0.77,
95% CI [0.36, 1.18], two-tailed. Assumptions of normality (Shapiro-Wilk:
Group A W = 0.97, p = .18; Group B W = 0.96, p = .12) and homogeneity
of variance (Levene's F(1, 98) = 1.23, p = .27) were satisfied.
```

#### One-Way ANOVA

```
A one-way ANOVA revealed a significant main effect of treatment condition
on test scores, F(2, 147) = 8.45, p < .001, η²_p = .10. Post hoc
comparisons using Tukey's HSD indicated that Condition A (M = 78.2,
SD = 7.3) scored significantly higher than Condition B (M = 71.5,
SD = 8.1, p = .002, d = 0.87) and Condition C (M = 70.1, SD = 7.9,
p < .001, d = 1.07). Conditions B and C did not differ significantly
(p = .52, d = 0.18).
```

#### Multiple Regression

```
Multiple linear regression was conducted to predict exam scores from
study hours, prior GPA, and attendance. The overall model was significant,
F(3, 146) = 45.2, p < .001, R² = .48, adjusted R² = .47. Study hours
(B = 1.80, SE = 0.31, β = .35, t = 5.78, p < .001, 95% CI [1.18, 2.42])
and prior GPA (B = 8.52, SE = 1.95, β = .28, t = 4.37, p < .001,
95% CI [4.66, 12.38]) were significant predictors, while attendance was
not (B = 0.15, SE = 0.12, β = .08, t = 1.25, p = .21, 95% CI [-0.09, 0.39]).
Multicollinearity was not a concern (all VIF < 1.5).
```

#### Bayesian Analysis

```
A Bayesian independent samples t-test was conducted using weakly
informative priors (Normal(0, 1) for mean difference). The posterior
distribution indicated that Group A scored higher than Group B
(M_diff = 6.8, 95% credible interval [3.2, 10.4]). The Bayes Factor
BF₁₀ = 45.3 provided very strong evidence for a difference between
groups, with a 99.8% posterior probability that Group A's mean exceeded
Group B's mean. Convergence diagnostics were satisfactory (all R̂ < 1.01,
ESS > 1000).
```

---

## Bayesian Statistics

### When to Use Bayesian Methods

Consider Bayesian approaches when:
- You have prior information to incorporate
- You want direct probability statements about hypotheses
- Sample size is small or planning sequential data collection
- You need to quantify evidence for the null hypothesis
- The model is complex (hierarchical, missing data)

See `references/bayesian_statistics.md` for comprehensive guidance on:
- Bayes' theorem and interpretation
- Prior specification (informative, weakly informative, non-informative)
- Bayesian hypothesis testing with Bayes Factors
- Credible intervals vs. confidence intervals
- Bayesian t-tests, ANOVA, regression, and hierarchical models
- Model convergence checking and posterior predictive checks

### Key Advantages

1. **Intuitive interpretation**: "Given the data, there is a 95% probability the parameter is in this interval"
2. **Evidence for null**: Can quantify support for no effect
3. **Flexible**: No p-hacking concerns; can analyze data as it arrives
4. **Uncertainty quantification**: Full posterior distribution

---

## Resources

This skill includes comprehensive reference materials:

### References Directory

- **test_selection_guide.md**: Decision tree for choosing appropriate statistical tests
- **assumptions_and_diagnostics.md**: Detailed guidance on checking and handling assumption violations
- **effect_sizes_and_power.md**: Calculating, interpreting, and reporting effect sizes; conducting power analyses
- **bayesian_statistics.md**: Complete guide to Bayesian analysis methods
- **reporting_standards.md**: APA-style reporting guidelines with examples

### Scripts Directory

- **assumption_checks.py**: Automated assumption checking with visualizations
  - `comprehensive_assumption_check()`: Complete workflow
  - `check_normality()`: Normality testing with Q-Q plots
  - `check_homogeneity_of_variance()`: Levene's test with box plots
  - `check_linearity()`: Regression linearity checks
  - `detect_outliers()`: IQR and z-score outlier detection

---

## Best Practices

1. **Pre-register analyses** when possible to distinguish confirmatory from exploratory
2. **Always check assumptions** before interpreting results
3. **Report effect sizes** with confidence intervals
4. **Report all planned analyses** including non-significant results
5. **Distinguish statistical from practical significance**
6. **Visualize data** before and after analysis
7. **Check diagnostics** for regression/ANOVA (residual plots, VIF, etc.)
8. **Conduct sensitivity analyses** to assess robustness
9. **Share data and code** for reproducibility
10. **Be transparent** about violations, transformations, and decisions

---

## Common Pitfalls to Avoid

1. **P-hacking**: Don't test multiple ways until something is significant
2. **HARKing**: Don't present exploratory findings as confirmatory
3. **Ignoring assumptions**: Check them and report violations
4. **Confusing significance with importance**: p < .05 ≠ meaningful effect
5. **Not reporting effect sizes**: Essential for interpretation
6. **Cherry-picking results**: Report all planned analyses
7. **Misinterpreting p-values**: They're NOT probability that hypothesis is true
8. **Multiple comparisons**: Correct for family-wise error when appropriate
9. **Ignoring missing data**: Understand mechanism (MCAR, MAR, MNAR)
10. **Overinterpreting non-significant results**: Absence of evidence ≠ evidence of absence

---

## Getting Started Checklist

When beginning a statistical analysis:

- [ ] Define research question and hypotheses
- [ ] Determine appropriate statistical test (use test_selection_guide.md)
- [ ] Conduct power analysis to determine sample size
- [ ] Load and inspect data
- [ ] Check for missing data and outliers
- [ ] Verify assumptions using assumption_checks.py
- [ ] Run primary analysis
- [ ] Calculate effect sizes with confidence intervals
- [ ] Conduct post-hoc tests if needed (with corrections)
- [ ] Create visualizations
- [ ] Write results following reporting_standards.md
- [ ] Conduct sensitivity analyses
- [ ] Share data and code

---

## Support and Further Reading

For questions about:
- **Test selection**: See references/test_selection_guide.md
- **Assumptions**: See references/assumptions_and_diagnostics.md
- **Effect sizes**: See references/effect_sizes_and_power.md
- **Bayesian methods**: See references/bayesian_statistics.md
- **Reporting**: See references/reporting_standards.md

**Key textbooks**:
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics*
- Gelman, A., & Hill, J. (2006). *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Kruschke, J. K. (2014). *Doing Bayesian Data Analysis*

**Online resources**:
- APA Style Guide: https://apastyle.apa.org/
- Statistical Consulting: Cross Validated (stats.stackexchange.com)

---

## Reference: Assumptions_And_Diagnostics

# Statistical Assumptions and Diagnostic Procedures

This document provides comprehensive guidance on checking and validating statistical assumptions for various analyses.

## General Principles

1. **Always check assumptions before interpreting test results**
2. **Use multiple diagnostic methods** (visual + formal tests)
3. **Consider robustness**: Some tests are robust to violations under certain conditions
4. **Document all assumption checks** in analysis reports
5. **Report violations and remedial actions taken**

## Common Assumptions Across Tests

### 1. Independence of Observations

**What it means**: Each observation is independent; measurements on one subject do not influence measurements on another.

**How to check**:
- Review study design and data collection procedures
- For time series: Check autocorrelation (ACF/PACF plots, Durbin-Watson test)
- For clustered data: Consider intraclass correlation (ICC)

**What to do if violated**:
- Use mixed-effects models for clustered/hierarchical data
- Use time series methods for temporally dependent data
- Use generalized estimating equations (GEE) for correlated data

**Critical severity**: HIGH - violations can severely inflate Type I error

---

### 2. Normality

**What it means**: Data or residuals follow a normal (Gaussian) distribution.

**When required**:
- t-tests (for small samples; robust for n > 30 per group)
- ANOVA (for small samples; robust for n > 30 per group)
- Linear regression (for residuals)
- Some correlation tests (Pearson)

**How to check**:

**Visual methods** (primary):
- Q-Q (quantile-quantile) plot: Points should fall on diagonal line
- Histogram with normal curve overlay
- Kernel density plot

**Formal tests** (secondary):
- Shapiro-Wilk test (recommended for n < 50)
- Kolmogorov-Smirnov test
- Anderson-Darling test

**Python implementation**:
```python
from scipy import stats
import matplotlib.pyplot as plt

# Shapiro-Wilk test
statistic, p_value = stats.shapiro(data)

# Q-Q plot
stats.probplot(data, dist="norm", plot=plt)
```

**Interpretation guidance**:
- For n < 30: Both visual and formal tests important
- For 30 ≤ n < 100: Visual inspection primary, formal tests secondary
- For n ≥ 100: Formal tests overly sensitive; rely on visual inspection
- Look for severe skewness, outliers, or bimodality

**What to do if violated**:
- **Mild violations** (slight skewness): Proceed if n > 30 per group
- **Moderate violations**: Use non-parametric alternatives (Mann-Whitney, Kruskal-Wallis, Wilcoxon)
- **Severe violations**:
  - Transform data (log, square root, Box-Cox)
  - Use non-parametric methods
  - Use robust regression methods
  - Consider bootstrapping

**Critical severity**: MEDIUM - parametric tests are often robust to mild violations with adequate sample size

---

### 3. Homogeneity of Variance (Homoscedasticity)

**What it means**: Variances are equal across groups or across the range of predictors.

**When required**:
- Independent samples t-test
- ANOVA
- Linear regression (constant variance of residuals)

**How to check**:

**Visual methods** (primary):
- Box plots by group (for t-test/ANOVA)
- Residuals vs. fitted values plot (for regression) - should show random scatter
- Scale-location plot (square root of standardized residuals vs. fitted)

**Formal tests** (secondary):
- Levene's test (robust to non-normality)
- Bartlett's test (sensitive to non-normality, not recommended)
- Brown-Forsythe test (median-based version of Levene's)
- Breusch-Pagan test (for regression)

**Python implementation**:
```python
from scipy import stats
import pingouin as pg

# Levene's test
statistic, p_value = stats.levene(group1, group2, group3)

# For regression
# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)
```

**Interpretation guidance**:
- Variance ratio (max/min) < 2-3: Generally acceptable
- For ANOVA: Test is robust if groups have equal sizes
- For regression: Look for funnel patterns in residual plots

**What to do if violated**:
- **t-test**: Use Welch's t-test (does not assume equal variances)
- **ANOVA**: Use Welch's ANOVA or Brown-Forsythe ANOVA
- **Regression**:
  - Transform dependent variable (log, square root)
  - Use weighted least squares (WLS)
  - Use robust standard errors (HC3)
  - Use generalized linear models (GLM) with appropriate variance function

**Critical severity**: MEDIUM - tests can be robust with equal sample sizes

---

## Test-Specific Assumptions

### T-Tests

**Assumptions**:
1. Independence of observations
2. Normality (each group for independent t-test; differences for paired t-test)
3. Homogeneity of variance (independent t-test only)

**Diagnostic workflow**:
```python
import scipy.stats as stats
import pingouin as pg

# Check normality for each group
stats.shapiro(group1)
stats.shapiro(group2)

# Check homogeneity of variance
stats.levene(group1, group2)

# If assumptions violated:
# Option 1: Welch's t-test (unequal variances)
pg.ttest(group1, group2, correction=False)  # Welch's

# Option 2: Non-parametric alternative
pg.mwu(group1, group2)  # Mann-Whitney U
```

---

### ANOVA

**Assumptions**:
1. Independence of observations within and between groups
2. Normality in each group
3. Homogeneity of variance across groups

**Additional considerations**:
- For repeated measures ANOVA: Sphericity assumption (Mauchly's test)

**Diagnostic workflow**:
```python
import pingouin as pg

# Check normality per group
for group in df['group'].unique():
    data = df[df['group'] == group]['value']
    stats.shapiro(data)

# Check homogeneity of variance
pg.homoscedasticity(df, dv='value', group='group')

# For repeated measures: Check sphericity
# Automatically tested in pingouin's rm_anova
```

**What to do if sphericity violated** (repeated measures):
- Greenhouse-Geisser correction (ε < 0.75)
- Huynh-Feldt correction (ε > 0.75)
- Use multivariate approach (MANOVA)

---

### Linear Regression

**Assumptions**:
1. **Linearity**: Relationship between X and Y is linear
2. **Independence**: Residuals are independent
3. **Homoscedasticity**: Constant variance of residuals
4. **Normality**: Residuals are normally distributed
5. **No multicollinearity**: Predictors are not highly correlated (multiple regression)

**Diagnostic workflow**:

**1. Linearity**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plots of Y vs each X
# Residuals vs. fitted values (should be randomly scattered)
plt.scatter(fitted_values, residuals)
plt.axhline(y=0, color='r', linestyle='--')
```

**2. Independence**:
```python
from statsmodels.stats.stattools import durbin_watson

# Durbin-Watson test (for time series)
dw_statistic = durbin_watson(residuals)
# Values between 1.5-2.5 suggest independence
```

**3. Homoscedasticity**:
```python
# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)

# Visual: Scale-location plot
plt.scatter(fitted_values, np.sqrt(np.abs(std_residuals)))
```

**4. Normality of residuals**:
```python
# Q-Q plot of residuals
stats.probplot(residuals, dist="norm", plot=plt)

# Shapiro-Wilk test
stats.shapiro(residuals)
```

**5. Multicollinearity**:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each predictor
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

# VIF > 10 indicates severe multicollinearity
# VIF > 5 indicates moderate multicollinearity
```

**What to do if violated**:
- **Non-linearity**: Add polynomial terms, use GAM, or transform variables
- **Heteroscedasticity**: Transform Y, use WLS, use robust SE
- **Non-normal residuals**: Transform Y, use robust methods, check for outliers
- **Multicollinearity**: Remove correlated predictors, use PCA, ridge regression

---

### Logistic Regression

**Assumptions**:
1. **Independence**: Observations are independent
2. **Linearity**: Linear relationship between log-odds and continuous predictors
3. **No perfect multicollinearity**: Predictors not perfectly correlated
4. **Large sample size**: At least 10-20 events per predictor

**Diagnostic workflow**:

**1. Linearity of logit**:
```python
# Box-Tidwell test: Add interaction with log of continuous predictor
# If interaction is significant, linearity violated
```

**2. Multicollinearity**:
```python
# Use VIF as in linear regression
```

**3. Influential observations**:
```python
# Cook's distance, DFBetas, leverage
from statsmodels.stats.outliers_influence import OLSInfluence

influence = OLSInfluence(model)
cooks_d = influence.cooks_distance
```

**4. Model fit**:
```python
# Hosmer-Lemeshow test
# Pseudo R-squared
# Classification metrics (accuracy, AUC-ROC)
```

---

## Outlier Detection

**Methods**:
1. **Visual**: Box plots, scatter plots
2. **Statistical**:
   - Z-scores: |z| > 3 suggests outlier
   - IQR method: Values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
   - Modified Z-score using median absolute deviation (robust to outliers)

**For regression**:
- **Leverage**: High leverage points (hat values)
- **Influence**: Cook's distance > 4/n suggests influential point
- **Outliers**: Studentized residuals > ±3

**What to do**:
1. Investigate data entry errors
2. Consider if outliers are valid observations
3. Report sensitivity analysis (results with and without outliers)
4. Use robust methods if outliers are legitimate

---

## Sample Size Considerations

### Minimum Sample Sizes (Rules of Thumb)

- **T-test**: n ≥ 30 per group for robustness to non-normality
- **ANOVA**: n ≥ 30 per group
- **Correlation**: n ≥ 30 for adequate power
- **Simple regression**: n ≥ 50
- **Multiple regression**: n ≥ 10-20 per predictor (minimum 10 + k predictors)
- **Logistic regression**: n ≥ 10-20 events per predictor

### Small Sample Considerations

For small samples:
- Assumptions become more critical
- Use exact tests when available (Fisher's exact, exact logistic regression)
- Consider non-parametric alternatives
- Use permutation tests or bootstrap methods
- Be conservative with interpretation

---

## Reporting Assumption Checks

When reporting analyses, include:

1. **Statement of assumptions checked**: List all assumptions tested
2. **Methods used**: Describe visual and formal tests employed
3. **Results of diagnostic tests**: Report test statistics and p-values
4. **Assessment**: State whether assumptions were met or violated
5. **Actions taken**: If violated, describe remedial actions (transformations, alternative tests, robust methods)

**Example reporting statement**:
> "Normality was assessed using Shapiro-Wilk tests and Q-Q plots. Data for Group A (W = 0.97, p = .18) and Group B (W = 0.96, p = .12) showed no significant departure from normality. Homogeneity of variance was assessed using Levene's test, which was non-significant (F(1, 58) = 1.23, p = .27), indicating equal variances across groups. Therefore, assumptions for the independent samples t-test were satisfied."

---

## Reference: Bayesian_Statistics

# Bayesian Statistical Analysis

This document provides guidance on conducting and interpreting Bayesian statistical analyses, which offer an alternative framework to frequentist (classical) statistics.

## Bayesian vs. Frequentist Philosophy

### Fundamental Differences

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| **Probability interpretation** | Long-run frequency of events | Degree of belief/uncertainty |
| **Parameters** | Fixed but unknown | Random variables with distributions |
| **Inference** | Based on sampling distributions | Based on posterior distributions |
| **Primary output** | p-values, confidence intervals | Posterior probabilities, credible intervals |
| **Prior information** | Not formally incorporated | Explicitly incorporated via priors |
| **Hypothesis testing** | Reject/fail to reject null | Probability of hypotheses given data |
| **Sample size** | Often requires minimum | Can work with any sample size |
| **Interpretation** | Indirect (probability of data given H₀) | Direct (probability of hypothesis given data) |

### Key Question Difference

**Frequentist**: "If the null hypothesis is true, what is the probability of observing data this extreme or more extreme?"

**Bayesian**: "Given the observed data, what is the probability that the hypothesis is true?"

The Bayesian question is more intuitive and directly addresses what researchers want to know.

---

## Bayes' Theorem

**Formula**:
```
P(θ|D) = P(D|θ) × P(θ) / P(D)
```

**In words**:
```
Posterior = Likelihood × Prior / Evidence
```

Where:
- **θ (theta)**: Parameter of interest (e.g., mean difference, correlation)
- **D**: Observed data
- **P(θ|D)**: Posterior distribution (belief about θ after seeing data)
- **P(D|θ)**: Likelihood (probability of data given θ)
- **P(θ)**: Prior distribution (belief about θ before seeing data)
- **P(D)**: Marginal likelihood/evidence (normalizing constant)

---

## Prior Distributions

### Types of Priors

#### 1. Informative Priors

**When to use**: When you have substantial prior knowledge from:
- Previous studies
- Expert knowledge
- Theory
- Pilot data

**Example**: Meta-analysis shows effect size d ≈ 0.40, SD = 0.15
- Prior: Normal(0.40, 0.15)

**Advantages**:
- Incorporates existing knowledge
- More efficient (smaller samples needed)
- Can stabilize estimates with small data

**Disadvantages**:
- Subjective (but subjectivity can be strength)
- Must be justified and transparent
- May be controversial if strong prior conflicts with data

---

#### 2. Weakly Informative Priors

**When to use**: Default choice for most applications

**Characteristics**:
- Regularizes estimates (prevents extreme values)
- Has minimal influence on posterior with moderate data
- Prevents computational issues

**Example priors**:
- Effect size: Normal(0, 1) or Cauchy(0, 0.707)
- Variance: Half-Cauchy(0, 1)
- Correlation: Uniform(-1, 1) or Beta(2, 2)

**Advantages**:
- Balances objectivity and regularization
- Computationally stable
- Broadly acceptable

---

#### 3. Non-Informative (Flat/Uniform) Priors

**When to use**: When attempting to be "objective"

**Example**: Uniform(-∞, ∞) for any value

**⚠️ Caution**:
- Can lead to improper posteriors
- May produce non-sensible results
- Not truly "non-informative" (still makes assumptions)
- Often not recommended in modern Bayesian practice

**Better alternative**: Use weakly informative priors

---

### Prior Sensitivity Analysis

**Always conduct**: Test how results change with different priors

**Process**:
1. Fit model with default/planned prior
2. Fit model with more diffuse prior
3. Fit model with more concentrated prior
4. Compare posterior distributions

**Reporting**:
- If results are similar: Evidence is robust
- If results differ substantially: Data are not strong enough to overwhelm prior

**Python example**:
```python
import pymc as pm

# Model with different priors
priors = [
    ('weakly_informative', pm.Normal.dist(0, 1)),
    ('diffuse', pm.Normal.dist(0, 10)),
    ('informative', pm.Normal.dist(0.5, 0.3))
]

results = {}
for name, prior in priors:
    with pm.Model():
        effect = pm.Normal('effect', mu=prior.mu, sigma=prior.sigma)
        # ... rest of model
        trace = pm.sample()
        results[name] = trace
```

---

## Bayesian Hypothesis Testing

### Bayes Factor (BF)

**What it is**: Ratio of evidence for two competing hypotheses

**Formula**:
```
BF₁₀ = P(D|H₁) / P(D|H₀)
```

**Interpretation**:

| BF₁₀ | Evidence |
|------|----------|
| >100 | Decisive for H₁ |
| 30-100 | Very strong for H₁ |
| 10-30 | Strong for H₁ |
| 3-10 | Moderate for H₁ |
| 1-3 | Anecdotal for H₁ |
| 1 | No evidence |
| 1/3-1 | Anecdotal for H₀ |
| 1/10-1/3 | Moderate for H₀ |
| 1/30-1/10 | Strong for H₀ |
| 1/100-1/30 | Very strong for H₀ |
| <1/100 | Decisive for H₀ |

**Advantages over p-values**:
1. Can provide evidence for null hypothesis
2. Not dependent on sampling intentions (no "peeking" problem)
3. Directly quantifies evidence
4. Can be updated with more data

**Python calculation**:
```python
import pingouin as pg

# Note: Limited BF support in Python
# Better options: R packages (BayesFactor), JASP software

# Approximate BF from t-statistic
# Using Jeffreys-Zellner-Siow prior
from scipy import stats

def bf_from_t(t, n1, n2, r_scale=0.707):
    """
    Approximate Bayes Factor from t-statistic
    r_scale: Cauchy prior scale (default 0.707 for medium effect)
    """
    # This is simplified; use dedicated packages for accurate calculation
    df = n1 + n2 - 2
    # Implementation requires numerical integration
    pass
```

---

### Region of Practical Equivalence (ROPE)

**Purpose**: Define range of negligible effect sizes

**Process**:
1. Define ROPE (e.g., d ∈ [-0.1, 0.1] for negligible effects)
2. Calculate % of posterior inside ROPE
3. Make decision:
   - >95% in ROPE: Accept practical equivalence
   - >95% outside ROPE: Reject equivalence
   - Otherwise: Inconclusive

**Advantage**: Directly tests for practical significance

**Python example**:
```python
# Define ROPE
rope_lower, rope_upper = -0.1, 0.1

# Calculate % of posterior in ROPE
in_rope = np.mean((posterior_samples > rope_lower) &
                  (posterior_samples < rope_upper))

print(f"{in_rope*100:.1f}% of posterior in ROPE")
```

---

## Bayesian Estimation

### Credible Intervals

**What it is**: Interval containing parameter with X% probability

**95% Credible Interval interpretation**:
> "There is a 95% probability that the true parameter lies in this interval."

**This is what people THINK confidence intervals mean** (but don't in frequentist framework)

**Types**:

#### Equal-Tailed Interval (ETI)
- 2.5th to 97.5th percentile
- Simple to calculate
- May not include mode for skewed distributions

#### Highest Density Interval (HDI)
- Narrowest interval containing 95% of distribution
- Always includes mode
- Better for skewed distributions

**Python calculation**:
```python
import arviz as az

# Equal-tailed interval
eti = np.percentile(posterior_samples, [2.5, 97.5])

# HDI
hdi = az.hdi(posterior_samples, hdi_prob=0.95)
```

---

### Posterior Distributions

**Interpreting posterior distributions**:

1. **Central tendency**:
   - Mean: Average posterior value
   - Median: 50th percentile
   - Mode: Most probable value (MAP - Maximum A Posteriori)

2. **Uncertainty**:
   - SD: Spread of posterior
   - Credible intervals: Quantify uncertainty

3. **Shape**:
   - Symmetric: Similar to normal
   - Skewed: Asymmetric uncertainty
   - Multimodal: Multiple plausible values

**Visualization**:
```python
import matplotlib.pyplot as plt
import arviz as az

# Posterior plot with HDI
az.plot_posterior(trace, hdi_prob=0.95)

# Trace plot (check convergence)
az.plot_trace(trace)

# Forest plot (multiple parameters)
az.plot_forest(trace)
```

---

## Common Bayesian Analyses

### Bayesian T-Test

**Purpose**: Compare two groups (Bayesian alternative to t-test)

**Outputs**:
1. Posterior distribution of mean difference
2. 95% credible interval
3. Bayes Factor (BF₁₀)
4. Probability of directional hypothesis (e.g., P(μ₁ > μ₂))

**Python implementation**:
```python
import pymc as pm
import arviz as az

# Bayesian independent samples t-test
with pm.Model() as model:
    # Priors for group means
    mu1 = pm.Normal('mu1', mu=0, sigma=10)
    mu2 = pm.Normal('mu2', mu=0, sigma=10)

    # Prior for pooled standard deviation
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group1)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group2)

    # Derived quantity: mean difference
    diff = pm.Deterministic('diff', mu1 - mu2)

    # Sample posterior
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Analyze results
print(az.summary(trace, var_names=['mu1', 'mu2', 'diff']))

# Probability that group1 > group2
prob_greater = np.mean(trace.posterior['diff'].values > 0)
print(f"P(μ₁ > μ₂) = {prob_greater:.3f}")

# Plot posterior
az.plot_posterior(trace, var_names=['diff'], ref_val=0)
```

---

### Bayesian ANOVA

**Purpose**: Compare three or more groups

**Model**:
```python
import pymc as pm

with pm.Model() as anova_model:
    # Hyperpriors
    mu_global = pm.Normal('mu_global', mu=0, sigma=10)
    sigma_between = pm.HalfNormal('sigma_between', sigma=5)
    sigma_within = pm.HalfNormal('sigma_within', sigma=5)

    # Group means (hierarchical)
    group_means = pm.Normal('group_means',
                            mu=mu_global,
                            sigma=sigma_between,
                            shape=n_groups)

    # Likelihood
    y = pm.Normal('y',
                  mu=group_means[group_idx],
                  sigma=sigma_within,
                  observed=data)

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Posterior contrasts
contrast_1_2 = trace.posterior['group_means'][:,:,0] - trace.posterior['group_means'][:,:,1]
```

---

### Bayesian Correlation

**Purpose**: Estimate correlation between two variables

**Advantage**: Provides distribution of correlation values

**Python implementation**:
```python
import pymc as pm

with pm.Model() as corr_model:
    # Prior on correlation
    rho = pm.Uniform('rho', lower=-1, upper=1)

    # Convert to covariance matrix
    cov_matrix = pm.math.stack([[1, rho],
                                [rho, 1]])

    # Likelihood (bivariate normal)
    obs = pm.MvNormal('obs',
                     mu=[0, 0],
                     cov=cov_matrix,
                     observed=np.column_stack([x, y]))

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Summarize correlation
print(az.summary(trace, var_names=['rho']))

# Probability that correlation is positive
prob_positive = np.mean(trace.posterior['rho'].values > 0)
```

---

### Bayesian Linear Regression

**Purpose**: Model relationship between predictors and outcome

**Advantages**:
- Uncertainty in all parameters
- Natural regularization (via priors)
- Can incorporate prior knowledge
- Credible intervals for predictions

**Python implementation**:
```python
import pymc as pm

with pm.Model() as regression_model:
    # Priors for coefficients
    alpha = pm.Normal('alpha', mu=0, sigma=10)  # Intercept
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Expected value
    mu = alpha + pm.math.dot(X, beta)

    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)

    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Posterior predictive checks
with regression_model:
    ppc = pm.sample_posterior_predictive(trace)

az.plot_ppc(ppc)

# Predictions with uncertainty
with regression_model:
    pm.set_data({'X': X_new})
    posterior_pred = pm.sample_posterior_predictive(trace)
```

---

## Hierarchical (Multilevel) Models

**When to use**:
- Nested/clustered data (students within schools)
- Repeated measures
- Meta-analysis
- Varying effects across groups

**Key concept**: Partial pooling
- Complete pooling: Ignore groups (biased)
- No pooling: Analyze groups separately (high variance)
- Partial pooling: Borrow strength across groups (Bayesian)

**Example: Varying intercepts**:
```python
with pm.Model() as hierarchical_model:
    # Hyperpriors
    mu_global = pm.Normal('mu_global', mu=0, sigma=10)
    sigma_between = pm.HalfNormal('sigma_between', sigma=5)
    sigma_within = pm.HalfNormal('sigma_within', sigma=5)

    # Group-level intercepts
    alpha = pm.Normal('alpha',
                     mu=mu_global,
                     sigma=sigma_between,
                     shape=n_groups)

    # Likelihood
    y_obs = pm.Normal('y_obs',
                     mu=alpha[group_idx],
                     sigma=sigma_within,
                     observed=y)

    trace = pm.sample()
```

---

## Model Comparison

### Methods

#### 1. Bayes Factor
- Directly compares model evidence
- Sensitive to prior specification
- Can be computationally intensive

#### 2. Information Criteria

**WAIC (Widely Applicable Information Criterion)**:
- Bayesian analog of AIC
- Lower is better
- Accounts for effective number of parameters

**LOO (Leave-One-Out Cross-Validation)**:
- Estimates out-of-sample prediction error
- Lower is better
- More robust than WAIC

**Python calculation**:
```python
import arviz as az

# Calculate WAIC and LOO
waic = az.waic(trace)
loo = az.loo(trace)

print(f"WAIC: {waic.elpd_waic:.2f}")
print(f"LOO: {loo.elpd_loo:.2f}")

# Compare multiple models
comparison = az.compare({
    'model1': trace1,
    'model2': trace2,
    'model3': trace3
})
print(comparison)
```

---

## Checking Bayesian Models

### 1. Convergence Diagnostics

**R-hat (Gelman-Rubin statistic)**:
- Compares within-chain and between-chain variance
- Values close to 1.0 indicate convergence
- R-hat < 1.01: Good
- R-hat > 1.05: Poor convergence

**Effective Sample Size (ESS)**:
- Number of independent samples
- Higher is better
- ESS > 400 per chain recommended

**Trace plots**:
- Should look like "fuzzy caterpillar"
- No trends, no stuck chains

**Python checking**:
```python
# Automatic summary with diagnostics
print(az.summary(trace, var_names=['parameter']))

# Visual diagnostics
az.plot_trace(trace)
az.plot_rank(trace)  # Rank plots
```

---

### 2. Posterior Predictive Checks

**Purpose**: Does model generate data similar to observed data?

**Process**:
1. Generate predictions from posterior
2. Compare to actual data
3. Look for systematic discrepancies

**Python implementation**:
```python
with model:
    ppc = pm.sample_posterior_predictive(trace)

# Visual check
az.plot_ppc(ppc, num_pp_samples=100)

# Quantitative checks
obs_mean = np.mean(observed_data)
pred_means = [np.mean(sample) for sample in ppc.posterior_predictive['y_obs']]
p_value = np.mean(pred_means >= obs_mean)  # Bayesian p-value
```

---

## Reporting Bayesian Results

### Example T-Test Report

> "A Bayesian independent samples t-test was conducted to compare groups A and B. Weakly informative priors were used: Normal(0, 1) for the mean difference and Half-Cauchy(0, 1) for the pooled standard deviation. The posterior distribution of the mean difference had a mean of 5.2 (95% CI [2.3, 8.1]), indicating that Group A scored higher than Group B. The Bayes Factor BF₁₀ = 23.5 provided strong evidence for a difference between groups, and there was a 99.7% probability that Group A's mean exceeded Group B's mean."

### Example Regression Report

> "A Bayesian linear regression was fitted with weakly informative priors (Normal(0, 10) for coefficients, Half-Cauchy(0, 5) for residual SD). The model explained substantial variance (R² = 0.47, 95% CI [0.38, 0.55]). Study hours (β = 0.52, 95% CI [0.38, 0.66]) and prior GPA (β = 0.31, 95% CI [0.17, 0.45]) were credible predictors (95% CIs excluded zero). Posterior predictive checks showed good model fit. Convergence diagnostics were satisfactory (all R-hat < 1.01, ESS > 1000)."

---

## Advantages and Limitations

### Advantages

1. **Intuitive interpretation**: Direct probability statements about parameters
2. **Incorporates prior knowledge**: Uses all available information
3. **Flexible**: Handles complex models easily
4. **No p-hacking**: Can look at data as it arrives
5. **Quantifies uncertainty**: Full posterior distribution
6. **Small samples**: Works with any sample size

### Limitations

1. **Computational**: Requires MCMC sampling (can be slow)
2. **Prior specification**: Requires thought and justification
3. **Complexity**: Steeper learning curve
4. **Software**: Fewer tools than frequentist methods
5. **Communication**: May need to educate reviewers/readers

---

## Key Python Packages

- **PyMC**: Full Bayesian modeling framework
- **ArviZ**: Visualization and diagnostics
- **Bambi**: High-level interface for regression models
- **PyStan**: Python interface to Stan
- **TensorFlow Probability**: Bayesian inference with TensorFlow

---

## When to Use Bayesian Methods

**Use Bayesian when**:
- You have prior information to incorporate
- You want direct probability statements
- Sample size is small
- Model is complex (hierarchical, missing data, etc.)
- You want to update analysis as data arrives

**Frequentist may be sufficient when**:
- Standard analysis with large sample
- No prior information
- Computational resources limited
- Reviewers unfamiliar with Bayesian methods

---

## Reference: Effect_Sizes_And_Power

# Effect Sizes and Power Analysis

This document provides guidance on calculating, interpreting, and reporting effect sizes, as well as conducting power analyses for study planning.

## Why Effect Sizes Matter

1. **Statistical significance ≠ practical significance**: p-values only tell if an effect exists, not how large it is
2. **Sample size dependent**: With large samples, trivial effects become "significant"
3. **Interpretation**: Effect sizes provide magnitude and practical importance
4. **Meta-analysis**: Effect sizes enable combining results across studies
5. **Power analysis**: Required for sample size determination

**Golden rule**: ALWAYS report effect sizes alongside p-values.

---

## Effect Sizes by Analysis Type

### T-Tests and Mean Differences

#### Cohen's d (Standardized Mean Difference)

**Formula**:
- Independent groups: d = (M₁ - M₂) / SD_pooled
- Paired groups: d = M_diff / SD_diff

**Interpretation** (Cohen, 1988):
- Small: |d| = 0.20
- Medium: |d| = 0.50
- Large: |d| = 0.80

**Context-dependent interpretation**:
- In education: d = 0.40 is typical for successful interventions
- In psychology: d = 0.40 is considered meaningful
- In medicine: Small effect sizes can be clinically important

**Python calculation**:
```python
import pingouin as pg
import numpy as np

# Independent t-test with effect size
result = pg.ttest(group1, group2, correction=False)
cohens_d = result['cohen-d'].values[0]

# Manual calculation
mean_diff = np.mean(group1) - np.mean(group2)
pooled_std = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)
cohens_d = mean_diff / pooled_std

# Paired t-test
result = pg.ttest(pre, post, paired=True)
cohens_d = result['cohen-d'].values[0]
```

**Confidence intervals for d**:
```python
from pingouin import compute_effsize_from_t

d, ci = compute_effsize_from_t(t_statistic, nx=n1, ny=n2, eftype='cohen')
```

---

#### Hedges' g (Bias-Corrected d)

**Why use it**: Cohen's d has slight upward bias with small samples (n < 20)

**Formula**: g = d × correction_factor, where correction_factor = 1 - 3/(4df - 1)

**Python calculation**:
```python
result = pg.ttest(group1, group2, correction=False)
hedges_g = result['hedges'].values[0]
```

**Use Hedges' g when**:
- Sample sizes are small (n < 20 per group)
- Conducting meta-analyses (standard in meta-analysis)

---

#### Glass's Δ (Delta)

**When to use**: When one group is a control with known variability

**Formula**: Δ = (M₁ - M₂) / SD_control

**Use cases**:
- Clinical trials (use control group SD)
- When treatment affects variability

---

### ANOVA

#### Eta-squared (η²)

**What it measures**: Proportion of total variance explained by factor

**Formula**: η² = SS_effect / SS_total

**Interpretation**:
- Small: η² = 0.01 (1% of variance)
- Medium: η² = 0.06 (6% of variance)
- Large: η² = 0.14 (14% of variance)

**Limitation**: Biased with multiple factors (sums to > 1.0)

**Python calculation**:
```python
import pingouin as pg

# One-way ANOVA
aov = pg.anova(dv='value', between='group', data=df)
eta_squared = aov['SS'][0] / aov['SS'].sum()

# Or use pingouin directly
aov = pg.anova(dv='value', between='group', data=df, detailed=True)
eta_squared = aov['np2'][0]  # Note: pingouin reports partial eta-squared
```

---

#### Partial Eta-squared (η²_p)

**What it measures**: Proportion of variance explained by factor, excluding other factors

**Formula**: η²_p = SS_effect / (SS_effect + SS_error)

**Interpretation**: Same benchmarks as η²

**When to use**: Multi-factor ANOVA (standard in factorial designs)

**Python calculation**:
```python
aov = pg.anova(dv='value', between=['factor1', 'factor2'], data=df)
# pingouin reports partial eta-squared by default
partial_eta_sq = aov['np2']
```

---

#### Omega-squared (ω²)

**What it measures**: Less biased estimate of population variance explained

**Why use it**: η² overestimates effect size; ω² provides better population estimate

**Formula**: ω² = (SS_effect - df_effect × MS_error) / (SS_total + MS_error)

**Interpretation**: Same benchmarks as η², but typically smaller values

**Python calculation**:
```python
def omega_squared(aov_table):
    ss_effect = aov_table.loc[0, 'SS']
    ss_total = aov_table['SS'].sum()
    ms_error = aov_table.loc[aov_table.index[-1], 'MS']  # Residual MS
    df_effect = aov_table.loc[0, 'DF']

    omega_sq = (ss_effect - df_effect * ms_error) / (ss_total + ms_error)
    return omega_sq
```

---

#### Cohen's f

**What it measures**: Effect size for ANOVA (analogous to Cohen's d)

**Formula**: f = √(η² / (1 - η²))

**Interpretation**:
- Small: f = 0.10
- Medium: f = 0.25
- Large: f = 0.40

**Python calculation**:
```python
eta_squared = 0.06  # From ANOVA
cohens_f = np.sqrt(eta_squared / (1 - eta_squared))
```

**Use in power analysis**: Required for ANOVA power calculations

---

### Correlation

#### Pearson's r / Spearman's ρ

**Interpretation**:
- Small: |r| = 0.10
- Medium: |r| = 0.30
- Large: |r| = 0.50

**Important notes**:
- r² = coefficient of determination (proportion of variance explained)
- r = 0.30 means 9% shared variance (0.30² = 0.09)
- Consider direction (positive/negative) and context

**Python calculation**:
```python
import pingouin as pg

# Pearson correlation with CI
result = pg.corr(x, y, method='pearson')
r = result['r'].values[0]
ci = [result['CI95%'][0][0], result['CI95%'][0][1]]

# Spearman correlation
result = pg.corr(x, y, method='spearman')
rho = result['r'].values[0]
```

---

### Regression

#### R² (Coefficient of Determination)

**What it measures**: Proportion of variance in Y explained by model

**Interpretation**:
- Small: R² = 0.02
- Medium: R² = 0.13
- Large: R² = 0.26

**Context-dependent**:
- Physical sciences: R² > 0.90 expected
- Social sciences: R² > 0.30 considered good
- Behavior prediction: R² > 0.10 may be meaningful

**Python calculation**:
```python
from sklearn.metrics import r2_score
from statsmodels.api import OLS

# Using statsmodels
model = OLS(y, X).fit()
r_squared = model.rsquared
adjusted_r_squared = model.rsquared_adj

# Manual
r_squared = 1 - (SS_residual / SS_total)
```

---

#### Adjusted R²

**Why use it**: R² artificially increases when adding predictors; adjusted R² penalizes model complexity

**Formula**: R²_adj = 1 - (1 - R²) × (n - 1) / (n - k - 1)

**When to use**: Always report alongside R² for multiple regression

---

#### Standardized Regression Coefficients (β)

**What it measures**: Effect of one-SD change in predictor on outcome (in SD units)

**Interpretation**: Similar to Cohen's d
- Small: |β| = 0.10
- Medium: |β| = 0.30
- Large: |β| = 0.50

**Python calculation**:
```python
from scipy import stats

# Standardize variables first
X_std = (X - X.mean()) / X.std()
y_std = (y - y.mean()) / y.std()

model = OLS(y_std, X_std).fit()
beta = model.params
```

---

#### f² (Cohen's f-squared for Regression)

**What it measures**: Effect size for individual predictors or model comparison

**Formula**: f² = R²_AB - R²_A / (1 - R²_AB)

Where:
- R²_AB = R² for full model with predictor
- R²_A = R² for reduced model without predictor

**Interpretation**:
- Small: f² = 0.02
- Medium: f² = 0.15
- Large: f² = 0.35

**Python calculation**:
```python
# Compare two nested models
model_full = OLS(y, X_full).fit()
model_reduced = OLS(y, X_reduced).fit()

r2_full = model_full.rsquared
r2_reduced = model_reduced.rsquared

f_squared = (r2_full - r2_reduced) / (1 - r2_full)
```

---

### Categorical Data Analysis

#### Cramér's V

**What it measures**: Association strength for χ² test (works for any table size)

**Formula**: V = √(χ² / (n × (k - 1)))

Where k = min(rows, columns)

**Interpretation** (for k > 2):
- Small: V = 0.07
- Medium: V = 0.21
- Large: V = 0.35

**For 2×2 tables**: Use phi coefficient (φ)

**Python calculation**:
```python
from scipy.stats.contingency import association

# Cramér's V
cramers_v = association(contingency_table, method='cramer')

# Phi coefficient (for 2x2)
phi = association(contingency_table, method='pearson')
```

---

#### Odds Ratio (OR) and Risk Ratio (RR)

**For 2×2 contingency tables**:

|           | Outcome + | Outcome - |
|-----------|-----------|-----------|
| Exposed   | a         | b         |
| Unexposed | c         | d         |

**Odds Ratio**: OR = (a/b) / (c/d) = ad / bc

**Interpretation**:
- OR = 1: No association
- OR > 1: Positive association (increased odds)
- OR < 1: Negative association (decreased odds)
- OR = 2: Twice the odds
- OR = 0.5: Half the odds

**Risk Ratio**: RR = (a/(a+b)) / (c/(c+d))

**When to use**:
- Cohort studies: Use RR (more interpretable)
- Case-control studies: Use OR (RR not available)
- Logistic regression: OR is natural output

**Python calculation**:
```python
import statsmodels.api as sm

# From contingency table
odds_ratio = (a * d) / (b * c)

# Confidence interval
table = np.array([[a, b], [c, d]])
oddsratio, pvalue = stats.fisher_exact(table)

# From logistic regression
model = sm.Logit(y, X).fit()
odds_ratios = np.exp(model.params)  # Exponentiate coefficients
ci = np.exp(model.conf_int())  # Exponentiate CIs
```

---

### Bayesian Effect Sizes

#### Bayes Factor (BF)

**What it measures**: Ratio of evidence for alternative vs. null hypothesis

**Interpretation**:
- BF₁₀ = 1: Equal evidence for H₁ and H₀
- BF₁₀ = 3: H₁ is 3× more likely than H₀ (moderate evidence)
- BF₁₀ = 10: H₁ is 10× more likely than H₀ (strong evidence)
- BF₁₀ = 100: H₁ is 100× more likely than H₀ (decisive evidence)
- BF₁₀ = 0.33: H₀ is 3× more likely than H₁
- BF₁₀ = 0.10: H₀ is 10× more likely than H₁

**Classification** (Jeffreys, 1961):
- 1-3: Anecdotal evidence
- 3-10: Moderate evidence
- 10-30: Strong evidence
- 30-100: Very strong evidence
- >100: Decisive evidence

**Python calculation**:
```python
import pingouin as pg

# Bayesian t-test
result = pg.ttest(group1, group2, correction=False)
# Note: pingouin doesn't include BF; use other packages

# Using JASP or BayesFactor (R) via rpy2
# Or implement using numerical integration
```

---

## Power Analysis

### Concepts

**Statistical power**: Probability of detecting an effect if it exists (1 - β)

**Conventional standards**:
- Power = 0.80 (80% chance of detecting effect)
- α = 0.05 (5% Type I error rate)

**Four interconnected parameters** (given 3, can solve for 4th):
1. Sample size (n)
2. Effect size (d, f, etc.)
3. Significance level (α)
4. Power (1 - β)

---

### A Priori Power Analysis (Planning)

**Purpose**: Determine required sample size before study

**Steps**:
1. Specify expected effect size (from literature, pilot data, or minimum meaningful effect)
2. Set α level (typically 0.05)
3. Set desired power (typically 0.80)
4. Calculate required n

**Python implementation**:
```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    zt_ind_solve_power,
    FTestAnovaPower,
    NormalIndPower
)

# T-test power analysis
n_required = tt_ind_solve_power(
    effect_size=0.5,  # Cohen's d
    alpha=0.05,
    power=0.80,
    ratio=1.0,  # Equal group sizes
    alternative='two-sided'
)

# ANOVA power analysis
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,  # Cohen's f
    ngroups=3,
    alpha=0.05,
    power=0.80
)

# Correlation power analysis
from pingouin import power_corr
n_required = power_corr(r=0.30, power=0.80, alpha=0.05)
```

---

### Post Hoc Power Analysis (After Study)

**⚠️ CAUTION**: Post hoc power is controversial and often not recommended

**Why it's problematic**:
- Observed power is a direct function of p-value
- If p > 0.05, power is always low
- Provides no additional information beyond p-value
- Can be misleading

**When it might be acceptable**:
- Study planning for future research
- Using effect size from multiple studies (not just your own)
- Explicit goal is sample size for replication

**Better alternatives**:
- Report confidence intervals for effect sizes
- Conduct sensitivity analysis
- Report minimum detectable effect size

---

### Sensitivity Analysis

**Purpose**: Determine minimum detectable effect size given study parameters

**When to use**: After study is complete, to understand study's capability

**Python implementation**:
```python
# What effect size could we detect with n=50 per group?
detectable_effect = tt_ind_solve_power(
    effect_size=None,  # Solve for this
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)

print(f"With n=50 per group, we could detect d ≥ {detectable_effect:.2f}")
```

---

## Reporting Effect Sizes

### APA Style Guidelines

**T-test example**:
> "Group A (M = 75.2, SD = 8.5) scored significantly higher than Group B (M = 68.3, SD = 9.2), t(98) = 3.82, p < .001, d = 0.77, 95% CI [0.36, 1.18]."

**ANOVA example**:
> "There was a significant main effect of treatment condition on test scores, F(2, 87) = 8.45, p < .001, η²p = .16. Post hoc comparisons using Tukey's HSD revealed..."

**Correlation example**:
> "There was a moderate positive correlation between study time and exam scores, r(148) = .42, p < .001, 95% CI [.27, .55]."

**Regression example**:
> "The regression model significantly predicted exam scores, F(3, 146) = 45.2, p < .001, R² = .48. Study hours (β = .52, p < .001) and prior GPA (β = .31, p < .001) were significant predictors."

**Bayesian example**:
> "A Bayesian independent samples t-test provided strong evidence for a difference between groups, BF₁₀ = 23.5, indicating the data are 23.5 times more likely under H₁ than H₀."

---

## Effect Size Pitfalls

1. **Don't only rely on benchmarks**: Context matters; small effects can be meaningful
2. **Report confidence intervals**: CIs show precision of effect size estimate
3. **Distinguish statistical vs. practical significance**: Large n can make trivial effects "significant"
4. **Consider cost-benefit**: Even small effects may be valuable if intervention is low-cost
5. **Multiple outcomes**: Effect sizes vary across outcomes; report all
6. **Don't cherry-pick**: Report effects for all planned analyses
7. **Publication bias**: Published effects are often overestimated

---

## Quick Reference Table

| Analysis | Effect Size | Small | Medium | Large |
|----------|-------------|-------|--------|-------|
| T-test | Cohen's d | 0.20 | 0.50 | 0.80 |
| ANOVA | η², ω² | 0.01 | 0.06 | 0.14 |
| ANOVA | Cohen's f | 0.10 | 0.25 | 0.40 |
| Correlation | r, ρ | 0.10 | 0.30 | 0.50 |
| Regression | R² | 0.02 | 0.13 | 0.26 |
| Regression | f² | 0.02 | 0.15 | 0.35 |
| Chi-square | Cramér's V | 0.07 | 0.21 | 0.35 |
| Chi-square (2×2) | φ | 0.10 | 0.30 | 0.50 |

---

## Resources

- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.)
- Lakens, D. (2013). Calculating and reporting effect sizes
- Ellis, P. D. (2010). *The Essential Guide to Effect Sizes*

---

## Reference: Reporting_Standards

# Statistical Reporting Standards

This document provides guidelines for reporting statistical analyses according to APA (American Psychological Association) style and general best practices for academic publications.

## General Principles

1. **Transparency**: Report enough detail for replication
2. **Completeness**: Include all planned analyses and outcomes
3. **Honesty**: Report non-significant findings and violations
4. **Clarity**: Write for your audience, define technical terms
5. **Reproducibility**: Provide code, data, or supplements when possible

---

## Pre-Registration and Planning

### What to Report (Ideally Before Data Collection)

1. **Hypotheses**: Clearly stated, directional when appropriate
2. **Sample size justification**: Power analysis or other rationale
3. **Data collection stopping rule**: When will you stop collecting data?
4. **Variables**: All variables collected (not just those analyzed)
5. **Exclusion criteria**: Rules for excluding participants/data points
6. **Statistical analyses**: Planned tests, including:
   - Primary analysis
   - Secondary analyses
   - Exploratory analyses (labeled as such)
   - Handling of missing data
   - Multiple comparison corrections
   - Assumption checks

**Why pre-register?**
- Prevents HARKing (Hypothesizing After Results are Known)
- Distinguishes confirmatory from exploratory analyses
- Increases credibility and reproducibility

**Platforms**: OSF, AsPredicted, ClinicalTrials.gov

---

## Methods Section

### Participants

**What to report**:
- Total N, including excluded participants
- Relevant demographics (age, gender, etc.)
- Recruitment method
- Inclusion/exclusion criteria
- Attrition/dropout with reasons

**Example**:
> "Participants were 150 undergraduate students (98 female, 52 male; M_age = 19.4 years, SD = 1.2, range 18-24) recruited from psychology courses in exchange for course credit. Five participants were excluded due to incomplete data (n = 3) or failing attention checks (n = 2), resulting in a final sample of 145."

### Design

**What to report**:
- Study design (between-subjects, within-subjects, mixed)
- Independent variables and levels
- Dependent variables
- Control variables/covariates
- Randomization procedure
- Blinding (single-blind, double-blind)

**Example**:
> "A 2 (feedback: positive vs. negative) × 2 (timing: immediate vs. delayed) between-subjects factorial design was used. Participants were randomly assigned to conditions using a computer-generated randomization sequence. The primary outcome was task performance measured as number of correct responses (0-20 scale)."

### Measures

**What to report**:
- Full name of measure/instrument
- Number of items
- Scale/response format
- Scoring method
- Reliability (Cronbach's α, ICC, etc.)
- Validity evidence (if applicable)

**Example**:
> "Depression was assessed using the Beck Depression Inventory-II (BDI-II; Beck et al., 1996), a 21-item self-report measure rated on a 4-point scale (0-3). Total scores range from 0 to 63, with higher scores indicating greater depression severity. The BDI-II demonstrated excellent internal consistency in this sample (α = .91)."

### Procedure

**What to report**:
- Step-by-step description of what participants did
- Timing and duration
- Instructions given
- Any manipulations or interventions

**Example**:
> "Participants completed the study online via Qualtrics. After providing informed consent, they completed demographic questions, were randomly assigned to one of four conditions, completed the experimental task (approximately 15 minutes), and finished with the outcome measures and debriefing. The entire session lasted approximately 30 minutes."

### Data Analysis

**What to report**:
- Software used (with version)
- Significance level (α)
- Tail(s) of tests (one-tailed or two-tailed)
- Assumption checks conducted
- Missing data handling
- Outlier treatment
- Multiple comparison corrections
- Effect size measures used

**Example**:
> "All analyses were conducted using Python 3.10 with scipy 1.11 and statsmodels 0.14. An alpha level of .05 was used for all significance tests. Assumptions of normality and homogeneity of variance were assessed using Shapiro-Wilk and Levene's tests, respectively. Missing data (< 2% for all variables) were handled using listwise deletion. Outliers beyond 3 SD from the mean were winsorized. For the primary ANOVA, partial eta-squared (η²_p) is reported as the effect size measure. Post hoc comparisons used Tukey's HSD to control family-wise error rate."

---

## Results Section

### Descriptive Statistics

**What to report**:
- Sample size (for each group if applicable)
- Measures of central tendency (M, Mdn)
- Measures of variability (SD, IQR, range)
- Confidence intervals (when appropriate)

**Example (continuous outcome)**:
> "Group A (n = 48) had a mean score of 75.2 (SD = 8.5, 95% CI [72.7, 77.7]), while Group B (n = 52) scored 68.3 (SD = 9.2, 95% CI [65.7, 70.9])."

**Example (categorical outcome)**:
> "Of the 145 participants, 89 (61.4%) chose Option A, 42 (29.0%) chose Option B, and 14 (9.7%) chose Option C."

**Tables for descriptive statistics**:
- Use tables for multiple variables or groups
- Include M, SD, and n (minimum)
- Can include range, skewness, kurtosis if relevant

---

### Assumption Checks

**What to report**:
- Which assumptions were tested
- Results of diagnostic tests
- Whether assumptions were met
- Actions taken if violated

**Example**:
> "Normality was assessed using Shapiro-Wilk tests. Data for Group A (W = 0.97, p = .18) and Group B (W = 0.96, p = .12) did not significantly deviate from normality. Levene's test indicated homogeneity of variance, F(1, 98) = 1.23, p = .27. Therefore, assumptions for the independent samples t-test were satisfied."

**Example (violated)**:
> "Shapiro-Wilk tests indicated significant departure from normality for Group C (W = 0.89, p = .003). Therefore, the non-parametric Mann-Whitney U test was used instead of the independent samples t-test."

---

### Inferential Statistics

#### T-Tests

**What to report**:
- Test statistic (t)
- Degrees of freedom
- p-value (exact if p > .001, otherwise p < .001)
- Effect size (Cohen's d or Hedges' g) with CI
- Direction of effect
- Whether test was one- or two-tailed

**Format**: t(df) = value, p = value, d = value, 95% CI [lower, upper]

**Example (independent t-test)**:
> "Group A (M = 75.2, SD = 8.5) scored significantly higher than Group B (M = 68.3, SD = 9.2), t(98) = 3.82, p < .001, d = 0.77, 95% CI [0.36, 1.18], two-tailed."

**Example (paired t-test)**:
> "Scores increased significantly from pretest (M = 65.4, SD = 10.2) to posttest (M = 71.8, SD = 9.7), t(49) = 4.21, p < .001, d = 0.64, 95% CI [0.33, 0.95]."

**Example (Welch's t-test)**:
> "Due to unequal variances, Welch's t-test was used. Group A scored significantly higher than Group B, t(94.3) = 3.65, p < .001, d = 0.74."

**Example (non-significant)**:
> "There was no significant difference between Group A (M = 72.1, SD = 8.3) and Group B (M = 70.5, SD = 8.9), t(98) = 0.91, p = .36, d = 0.18, 95% CI [-0.21, 0.57]."

---

#### ANOVA

**What to report**:
- F statistic
- Degrees of freedom (effect, error)
- p-value
- Effect size (η², η²_p, or ω²)
- Means and SDs for all groups
- Post hoc test results (if significant)

**Format**: F(df_effect, df_error) = value, p = value, η²_p = value

**Example (one-way ANOVA)**:
> "There was a significant main effect of treatment condition on test scores, F(2, 147) = 8.45, p < .001, η²_p = .10. Post hoc comparisons using Tukey's HSD revealed that Condition A (M = 78.2, SD = 7.3) scored significantly higher than Condition B (M = 71.5, SD = 8.1, p = .002, d = 0.87) and Condition C (M = 70.1, SD = 7.9, p < .001, d = 1.07). Conditions B and C did not differ significantly (p = .52, d = 0.18)."

**Example (factorial ANOVA)**:
> "A 2 (feedback: positive vs. negative) × 2 (timing: immediate vs. delayed) between-subjects ANOVA revealed a significant main effect of feedback, F(1, 146) = 12.34, p < .001, η²_p = .08, but no significant main effect of timing, F(1, 146) = 2.10, p = .15, η²_p = .01. Critically, the interaction was significant, F(1, 146) = 6.78, p = .01, η²_p = .04. Simple effects analysis showed that positive feedback improved performance for immediate timing (M_diff = 8.2, p < .001) but not for delayed timing (M_diff = 1.3, p = .42)."

**Example (repeated measures ANOVA)**:
> "A one-way repeated measures ANOVA revealed a significant effect of time point on anxiety scores, F(2, 98) = 15.67, p < .001, η²_p = .24. Mauchly's test indicated that the assumption of sphericity was violated, χ²(2) = 8.45, p = .01, therefore Greenhouse-Geisser corrected values are reported (ε = 0.87). Pairwise comparisons with Bonferroni correction showed..."

---

#### Correlation

**What to report**:
- Correlation coefficient (r or ρ)
- Sample size
- p-value
- Direction and strength
- Confidence interval
- Coefficient of determination (r²) if relevant

**Format**: r(df) = value, p = value, 95% CI [lower, upper]

**Example (Pearson)**:
> "There was a moderate positive correlation between study time and exam score, r(148) = .42, p < .001, 95% CI [.27, .55], indicating that 18% of the variance in exam scores was shared with study time (r² = .18)."

**Example (Spearman)**:
> "A Spearman rank-order correlation revealed a significant positive association between class rank and motivation, ρ(118) = .38, p < .001, 95% CI [.21, .52]."

**Example (non-significant)**:
> "There was no significant correlation between age and reaction time, r(98) = -.12, p = .23, 95% CI [-.31, .08]."

---

#### Regression

**What to report**:
- Overall model fit (R², adjusted R², F-test)
- Coefficients (B, SE, β, t, p) for each predictor
- Effect sizes
- Confidence intervals for coefficients
- Variance inflation factors (if multicollinearity assessed)

**Format**: B = value, SE = value, β = value, t = value, p = value, 95% CI [lower, upper]

**Example (simple regression)**:
> "Simple linear regression showed that study hours significantly predicted exam scores, F(1, 148) = 42.5, p < .001, R² = .22. Specifically, each additional hour of study was associated with a 2.4-point increase in exam score (B = 2.40, SE = 0.37, β = .47, t = 6.52, p < .001, 95% CI [1.67, 3.13])."

**Example (multiple regression)**:
> "Multiple linear regression was conducted to predict exam scores from study hours, prior GPA, and attendance. The overall model was significant, F(3, 146) = 45.2, p < .001, R² = .48, adjusted R² = .47. Study hours (B = 1.80, SE = 0.31, β = .35, t = 5.78, p < .001, 95% CI [1.18, 2.42]) and prior GPA (B = 8.52, SE = 1.95, β = .28, t = 4.37, p < .001, 95% CI [4.66, 12.38]) were significant predictors, but attendance was not (B = 0.15, SE = 0.12, β = .08, t = 1.25, p = .21, 95% CI [-0.09, 0.39]). Multicollinearity was not a concern, as all VIF values were below 1.5."

**Example (logistic regression)**:
> "Logistic regression was conducted to predict pass/fail status from study hours. The overall model was significant, χ²(1) = 28.7, p < .001, Nagelkerke R² = .31. Each additional study hour increased the odds of passing by 1.35 times (OR = 1.35, 95% CI [1.18, 1.54], p < .001). The model correctly classified 76% of cases (sensitivity = 81%, specificity = 68%)."

---

#### Chi-Square Tests

**What to report**:
- χ² statistic
- Degrees of freedom
- p-value
- Effect size (Cramér's V or φ)
- Observed and expected frequencies (or percentages)

**Format**: χ²(df, N = total) = value, p = value, Cramér's V = value

**Example (2×2)**:
> "A chi-square test of independence revealed a significant association between treatment group and outcome, χ²(1, N = 150) = 8.45, p = .004, φ = .24. Specifically, 72% of participants in the treatment group improved compared to 48% in the control group."

**Example (larger table)**:
> "A chi-square test examined the relationship between education level (high school, bachelor's, graduate) and political affiliation (liberal, moderate, conservative). The association was significant, χ²(4, N = 300) = 18.7, p = .001, Cramér's V = .18, indicating a small to moderate association."

**Example (Fisher's exact)**:
> "Due to expected cell counts below 5, Fisher's exact test was used. The association between treatment and outcome was significant, p = .018 (two-tailed), OR = 3.42, 95% CI [1.21, 9.64]."

---

#### Non-Parametric Tests

**Mann-Whitney U**:
> "A Mann-Whitney U test indicated that Group A (Mdn = 75, IQR = 10) had significantly higher scores than Group B (Mdn = 68, IQR = 12), U = 845, z = 3.21, p = .001, r = .32."

**Wilcoxon signed-rank**:
> "A Wilcoxon signed-rank test showed that scores increased significantly from pretest (Mdn = 65, IQR = 15) to posttest (Mdn = 72, IQR = 14), z = 3.89, p < .001, r = .39."

**Kruskal-Wallis**:
> "A Kruskal-Wallis test revealed significant differences among the three conditions, H(2) = 15.7, p < .001, η² = .09. Follow-up pairwise comparisons with Bonferroni correction showed..."

---

#### Bayesian Statistics

**What to report**:
- Prior distributions used
- Posterior estimates (mean/median, credible intervals)
- Bayes Factor (if hypothesis testing)
- Convergence diagnostics (R-hat, ESS)
- Posterior predictive checks

**Example (Bayesian t-test)**:
> "A Bayesian independent samples t-test was conducted using weakly informative priors (Normal(0, 1) for mean difference). The posterior distribution of the mean difference had a mean of 6.8 (95% credible interval [3.2, 10.4]), indicating that Group A scored higher than Group B. The Bayes Factor BF₁₀ = 45.3 provided very strong evidence for a difference between groups. There was a 99.8% posterior probability that Group A's mean exceeded Group B's mean."

**Example (Bayesian regression)**:
> "A Bayesian linear regression was fitted with weakly informative priors (Normal(0, 10) for coefficients, Half-Cauchy(0, 5) for residual SD). The model showed that study hours credibly predicted exam scores (β = 0.52, 95% CI [0.38, 0.66]; 0 not included in interval). All convergence diagnostics were satisfactory (R-hat < 1.01, ESS > 1000 for all parameters). Posterior predictive checks indicated adequate model fit."

---

## Effect Sizes

### Always Report

**Why**:
- p-values don't indicate magnitude
- Required by APA and most journals
- Essential for meta-analysis
- Informs practical significance

**Which effect size?**
- T-tests: Cohen's d or Hedges' g
- ANOVA: η², η²_p, or ω²
- Correlation: r (already is an effect size)
- Regression: β (standardized), R², f²
- Chi-square: Cramér's V or φ

**With confidence intervals**:
- Always report CIs for effect sizes when possible
- Shows precision of estimate
- More informative than point estimate alone

---

## Figures and Tables

### When to Use Tables vs. Figures

**Tables**:
- Exact values needed
- Many variables/conditions
- Descriptive statistics
- Regression coefficients
- Correlation matrices

**Figures**:
- Patterns and trends
- Distributions
- Interactions
- Comparisons across groups
- Time series

### Figure Guidelines

**General**:
- Clear, readable labels
- Sufficient font size (≥ 10pt)
- High resolution (≥ 300 dpi for publications)
- Monochrome-friendly (colorblind-accessible)
- Error bars (SE or 95% CI; specify which!)
- Legend when needed

**Common figure types**:
- Bar charts: Group comparisons (include error bars)
- Box plots: Distributions, outliers
- Scatter plots: Correlations, relationships
- Line graphs: Change over time, interactions
- Violin plots: Distributions (better than box plots)

**Example figure caption**:
> "Figure 1. Mean exam scores by study condition. Error bars represent 95% confidence intervals. * p < .05, ** p < .01, *** p < .001."

### Table Guidelines

**General**:
- Clear column and row labels
- Consistent decimal places (usually 2)
- Horizontal lines only (not vertical)
- Notes below table for clarifications
- Statistical symbols in italics (p, M, SD, F, t, r)

**Example table**:

**Table 1**
*Descriptive Statistics and Intercorrelations*

| Variable | M | SD | 1 | 2 | 3 |
|----------|---|----|----|----|----|
| 1. Study hours | 5.2 | 2.1 | — | | |
| 2. Prior GPA | 3.1 | 0.5 | .42** | — | |
| 3. Exam score | 75.3 | 10.2 | .47*** | .52*** | — |

*Note*. N = 150. ** p < .01. *** p < .001.

---

## Common Mistakes to Avoid

1. **Reporting p = .000**: Report p < .001 instead
2. **Omitting effect sizes**: Always include them
3. **Not reporting assumption checks**: Describe tests and outcomes
4. **Confusing statistical and practical significance**: Discuss both
5. **Only reporting significant results**: Report all planned analyses
6. **Using "prove" or "confirm"**: Use "support" or "consistent with"
7. **Saying "marginally significant" for .05 < p < .10**: Either significant or not
8. **Reporting only one decimal for p-values**: Use two (p = .03, not p = .0)
9. **Not specifying one- vs. two-tailed**: Always clarify
10. **Inconsistent rounding**: Be consistent throughout

---

## Null Results

### How to Report Non-Significant Findings

**Don't say**:
- "There was no effect"
- "X and Y are unrelated"
- "Groups are equivalent"

**Do say**:
- "There was no significant difference"
- "The effect was not statistically significant"
- "We did not find evidence for a relationship"

**Include**:
- Exact p-value (not just "ns" or "p > .05")
- Effect size (shows magnitude even if not significant)
- Confidence interval (may include meaningful values)
- Power analysis (was study adequately powered?)

**Example**:
> "Contrary to our hypothesis, there was no significant difference in creativity scores between the music (M = 72.1, SD = 8.3) and silence (M = 70.5, SD = 8.9) conditions, t(98) = 0.91, p = .36, d = 0.18, 95% CI [-0.21, 0.57]. A post hoc sensitivity analysis revealed that the study had 80% power to detect an effect of d = 0.57 or larger, suggesting the null finding may reflect insufficient power to detect small effects."

---

## Reproducibility

### Materials to Share

1. **Data**: De-identified raw data (or aggregate if sensitive)
2. **Code**: Analysis scripts
3. **Materials**: Stimuli, measures, protocols
4. **Supplements**: Additional analyses, tables

**Where to share**:
- Open Science Framework (OSF)
- GitHub (for code)
- Journal supplements
- Institutional repository

**In paper**:
> "Data, analysis code, and materials are available at https://osf.io/xxxxx/"

---

## Checklist for Statistical Reporting

- [ ] Sample size and demographics
- [ ] Study design clearly described
- [ ] All measures described with reliability
- [ ] Procedure detailed
- [ ] Software and versions specified
- [ ] Alpha level stated
- [ ] Assumption checks reported
- [ ] Descriptive statistics (M, SD, n)
- [ ] Test statistics with df and p-values
- [ ] Effect sizes with confidence intervals
- [ ] All planned analyses reported (including non-significant)
- [ ] Figures/tables properly formatted and labeled
- [ ] Multiple comparisons corrections described
- [ ] Missing data handling explained
- [ ] Limitations discussed
- [ ] Data/code availability statement

---

## Additional Resources

- APA Publication Manual (7th edition)
- CONSORT guidelines (for RCTs)
- STROBE guidelines (for observational studies)
- PRISMA guidelines (for systematic reviews/meta-analyses)
- Wilkinson & Task Force on Statistical Inference (1999). Statistical methods in psychology journals.

---

## Reference: Test_Selection_Guide

# Statistical Test Selection Guide

This guide provides a decision tree for selecting appropriate statistical tests based on research questions, data types, and study designs.

## Decision Tree for Test Selection

### 1. Comparing Groups

#### Two Independent Groups
- **Continuous outcome, normally distributed**: Independent samples t-test
- **Continuous outcome, non-normal**: Mann-Whitney U test (Wilcoxon rank-sum test)
- **Binary outcome**: Chi-square test or Fisher's exact test (if expected counts < 5)
- **Ordinal outcome**: Mann-Whitney U test

#### Two Paired/Dependent Groups
- **Continuous outcome, normally distributed**: Paired t-test
- **Continuous outcome, non-normal**: Wilcoxon signed-rank test
- **Binary outcome**: McNemar's test
- **Ordinal outcome**: Wilcoxon signed-rank test

#### Three or More Independent Groups
- **Continuous outcome, normally distributed, equal variances**: One-way ANOVA
- **Continuous outcome, normally distributed, unequal variances**: Welch's ANOVA
- **Continuous outcome, non-normal**: Kruskal-Wallis H test
- **Binary/categorical outcome**: Chi-square test
- **Ordinal outcome**: Kruskal-Wallis H test

#### Three or More Paired/Dependent Groups
- **Continuous outcome, normally distributed**: Repeated measures ANOVA
- **Continuous outcome, non-normal**: Friedman test
- **Binary outcome**: Cochran's Q test

#### Multiple Factors (Factorial Designs)
- **Continuous outcome**: Two-way ANOVA (or higher-way ANOVA)
- **With covariates**: ANCOVA
- **Mixed within and between factors**: Mixed ANOVA

### 2. Relationships Between Variables

#### Two Continuous Variables
- **Linear relationship, bivariate normal**: Pearson correlation
- **Monotonic relationship or non-normal**: Spearman rank correlation
- **Rank-based data**: Spearman or Kendall's tau

#### One Continuous Outcome, One or More Predictors
- **Single continuous predictor**: Simple linear regression
- **Multiple continuous/categorical predictors**: Multiple linear regression
- **Categorical predictors**: ANOVA/ANCOVA framework
- **Non-linear relationships**: Polynomial regression or generalized additive models (GAM)

#### Binary Outcome
- **Single predictor**: Logistic regression
- **Multiple predictors**: Multiple logistic regression
- **Rare events**: Exact logistic regression or Firth's method

#### Count Outcome
- **Poisson-distributed**: Poisson regression
- **Overdispersed counts**: Negative binomial regression
- **Zero-inflated**: Zero-inflated Poisson/negative binomial

#### Time-to-Event Outcome
- **Comparing survival curves**: Log-rank test
- **Modeling with covariates**: Cox proportional hazards regression
- **Parametric survival models**: Weibull, exponential, log-normal

### 3. Agreement and Reliability

#### Inter-Rater Reliability
- **Categorical ratings, 2 raters**: Cohen's kappa
- **Categorical ratings, >2 raters**: Fleiss' kappa or Krippendorff's alpha
- **Continuous ratings**: Intraclass correlation coefficient (ICC)

#### Test-Retest Reliability
- **Continuous measurements**: ICC or Pearson correlation
- **Internal consistency**: Cronbach's alpha

#### Agreement Between Methods
- **Continuous measurements**: Bland-Altman analysis
- **Categorical classifications**: Cohen's kappa

### 4. Categorical Data Analysis

#### Contingency Tables
- **2x2 table**: Chi-square test or Fisher's exact test
- **Larger than 2x2**: Chi-square test
- **Ordered categories**: Cochran-Armitage trend test
- **Paired categories**: McNemar's test (2x2) or McNemar-Bowker test (larger)

### 5. Bayesian Alternatives

Any of the above tests can be performed using Bayesian methods:
- **Group comparisons**: Bayesian t-test, Bayesian ANOVA
- **Correlations**: Bayesian correlation
- **Regression**: Bayesian linear/logistic regression

**Advantages of Bayesian approaches:**
- Provides probability of hypotheses given data
- Naturally incorporates prior information
- Provides credible intervals instead of confidence intervals
- No p-value interpretation issues

## Key Considerations

### Sample Size
- Small samples (n < 30): Consider non-parametric tests or exact methods
- Very large samples: Even small effects may be statistically significant; focus on effect sizes

### Multiple Comparisons
- When conducting multiple tests, adjust for multiple comparisons using:
  - Bonferroni correction (conservative)
  - Holm-Bonferroni (less conservative)
  - False Discovery Rate (FDR) control (Benjamini-Hochberg)
  - Tukey HSD for post-hoc ANOVA comparisons

### Missing Data
- Complete case analysis (listwise deletion)
- Multiple imputation
- Maximum likelihood methods
- Ensure missing data mechanism is understood (MCAR, MAR, MNAR)

### Effect Sizes
- Always report effect sizes alongside p-values
- See `effect_sizes_and_power.md` for guidance

### Study Design Considerations
- Randomized controlled trials: Standard parametric/non-parametric tests
- Observational studies: Consider confounding and use regression/matching
- Clustered/nested data: Use mixed-effects models or GEE
- Time series: Use time series methods (ARIMA, etc.)
