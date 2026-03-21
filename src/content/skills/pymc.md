---
title: "Pymc"
description: "Bayesian modeling with PyMC. Build hierarchical models, MCMC (NUTS), variational inference, LOO/WAIC comparison, posterior checks, for probabilistic programming and inference."
category: "other"
source: "community"
author: "Community"
tags: ["pymc"]
date: 2026-03-20
---

# PyMC Bayesian Modeling

## Overview

PyMC is a Python library for Bayesian modeling and probabilistic programming. Build, fit, validate, and compare Bayesian models using PyMC's modern API (version 5.x+), including hierarchical models, MCMC sampling (NUTS), variational inference, and model comparison (LOO, WAIC).

## When to Use This Skill

This skill should be used when:
- Building Bayesian models (linear/logistic regression, hierarchical models, time series, etc.)
- Performing MCMC sampling or variational inference
- Conducting prior/posterior predictive checks
- Diagnosing sampling issues (divergences, convergence, ESS)
- Comparing multiple models using information criteria (LOO, WAIC)
- Implementing uncertainty quantification through Bayesian methods
- Working with hierarchical/multilevel data structures
- Handling missing data or measurement error in a principled way

## Standard Bayesian Workflow

Follow this workflow for building and validating Bayesian models:

### 1. Data Preparation

```python
import pymc as pm
import arviz as az
import numpy as np

# Load and prepare data
X = ...  # Predictors
y = ...  # Outcomes

# Standardize predictors for better sampling
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std
```

**Key practices:**
- Standardize continuous predictors (improves sampling efficiency)
- Center outcomes when possible
- Handle missing data explicitly (treat as parameters)
- Use named dimensions with `coords` for clarity

### 2. Model Building

```python
coords = {
    'predictors': ['var1', 'var2', 'var3'],
    'obs_id': np.arange(len(y))
}

with pm.Model(coords=coords) as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear predictor
    mu = alpha + pm.math.dot(X_scaled, beta)

    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y, dims='obs_id')
```

**Key practices:**
- Use weakly informative priors (not flat priors)
- Use `HalfNormal` or `Exponential` for scale parameters
- Use named dimensions (`dims`) instead of `shape` when possible
- Use `pm.Data()` for values that will be updated for predictions

### 3. Prior Predictive Check

**Always validate priors before fitting:**

```python
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000, random_seed=42)

# Visualize
az.plot_ppc(prior_pred, group='prior')
```

**Check:**
- Do prior predictions span reasonable values?
- Are extreme values plausible given domain knowledge?
- If priors generate implausible data, adjust and re-check

### 4. Fit Model

```python
with model:
    # Optional: Quick exploration with ADVI
    # approx = pm.fit(n=20000)

    # Full MCMC inference
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
        idata_kwargs={'log_likelihood': True}  # For model comparison
    )
```

**Key parameters:**
- `draws=2000`: Number of samples per chain
- `tune=1000`: Warmup samples (discarded)
- `chains=4`: Run 4 chains for convergence checking
- `target_accept=0.9`: Higher for difficult posteriors (0.95-0.99)
- Include `log_likelihood=True` for model comparison

### 5. Check Diagnostics

**Use the diagnostic script:**

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata, var_names=['alpha', 'beta', 'sigma'])
```

**Check:**
- **R-hat < 1.01**: Chains have converged
- **ESS > 400**: Sufficient effective samples
- **No divergences**: NUTS sampled successfully
- **Trace plots**: Chains should mix well (fuzzy caterpillar)

**If issues arise:**
- Divergences → Increase `target_accept=0.95`, use non-centered parameterization
- Low ESS → Sample more draws, reparameterize to reduce correlation
- High R-hat → Run longer, check for multimodality

### 6. Posterior Predictive Check

**Validate model fit:**

```python
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True, random_seed=42)

# Visualize
az.plot_ppc(idata)
```

**Check:**
- Do posterior predictions capture observed data patterns?
- Are systematic deviations evident (model misspecification)?
- Consider alternative models if fit is poor

### 7. Analyze Results

```python
# Summary statistics
print(az.summary(idata, var_names=['alpha', 'beta', 'sigma']))

# Posterior distributions
az.plot_posterior(idata, var_names=['alpha', 'beta', 'sigma'])

# Coefficient estimates
az.plot_forest(idata, var_names=['beta'], combined=True)
```

### 8. Make Predictions

```python
X_new = ...  # New predictor values
X_new_scaled = (X_new - X_mean) / X_std

with model:
    pm.set_data({'X_scaled': X_new_scaled})
    post_pred = pm.sample_posterior_predictive(
        idata.posterior,
        var_names=['y_obs'],
        random_seed=42
    )

# Extract prediction intervals
y_pred_mean = post_pred.posterior_predictive['y_obs'].mean(dim=['chain', 'draw'])
y_pred_hdi = az.hdi(post_pred.posterior_predictive, var_names=['y_obs'])
```

## Common Model Patterns

### Linear Regression

For continuous outcomes with linear relationships:

```python
with pm.Model() as linear_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + pm.math.dot(X, beta)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**Use template:** `assets/linear_regression_template.py`

### Logistic Regression

For binary outcomes:

```python
with pm.Model() as logistic_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    logit_p = alpha + pm.math.dot(X, beta)
    y = pm.Bernoulli('y', logit_p=logit_p, observed=y_obs)
```

### Hierarchical Models

For grouped data (use non-centered parameterization):

```python
with pm.Model(coords={'groups': group_names}) as hierarchical_model:
    # Hyperpriors
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    # Group-level (non-centered)
    alpha_offset = pm.Normal('alpha_offset', mu=0, sigma=1, dims='groups')
    alpha = pm.Deterministic('alpha', mu_alpha + sigma_alpha * alpha_offset, dims='groups')

    # Observation-level
    mu = alpha[group_idx]
    sigma = pm.HalfNormal('sigma', sigma=1)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

**Use template:** `assets/hierarchical_model_template.py`

**Critical:** Always use non-centered parameterization for hierarchical models to avoid divergences.

### Poisson Regression

For count data:

```python
with pm.Model() as poisson_model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    log_lambda = alpha + pm.math.dot(X, beta)
    y = pm.Poisson('y', mu=pm.math.exp(log_lambda), observed=y_obs)
```

For overdispersed counts, use `NegativeBinomial` instead.

### Time Series

For autoregressive processes:

```python
with pm.Model() as ar_model:
    sigma = pm.HalfNormal('sigma', sigma=1)
    rho = pm.Normal('rho', mu=0, sigma=0.5, shape=ar_order)
    init_dist = pm.Normal.dist(mu=0, sigma=sigma)

    y = pm.AR('y', rho=rho, sigma=sigma, init_dist=init_dist, observed=y_obs)
```

## Model Comparison

### Comparing Models

Use LOO or WAIC for model comparison:

```python
from scripts.model_comparison import compare_models, check_loo_reliability

# Fit models with log_likelihood
models = {
    'Model1': idata1,
    'Model2': idata2,
    'Model3': idata3
}

# Compare using LOO
comparison = compare_models(models, ic='loo')

# Check reliability
check_loo_reliability(models)
```

**Interpretation:**
- **Δloo < 2**: Models are similar, choose simpler model
- **2 < Δloo < 4**: Weak evidence for better model
- **4 < Δloo < 10**: Moderate evidence
- **Δloo > 10**: Strong evidence for better model

**Check Pareto-k values:**
- k < 0.7: LOO reliable
- k > 0.7: Consider WAIC or k-fold CV

### Model Averaging

When models are similar, average predictions:

```python
from scripts.model_comparison import model_averaging

averaged_pred, weights = model_averaging(models, var_name='y_obs')
```

## Distribution Selection Guide

### For Priors

**Scale parameters** (σ, τ):
- `pm.HalfNormal('sigma', sigma=1)` - Default choice
- `pm.Exponential('sigma', lam=1)` - Alternative
- `pm.Gamma('sigma', alpha=2, beta=1)` - More informative

**Unbounded parameters**:
- `pm.Normal('theta', mu=0, sigma=1)` - For standardized data
- `pm.StudentT('theta', nu=3, mu=0, sigma=1)` - Robust to outliers

**Positive parameters**:
- `pm.LogNormal('theta', mu=0, sigma=1)`
- `pm.Gamma('theta', alpha=2, beta=1)`

**Probabilities**:
- `pm.Beta('p', alpha=2, beta=2)` - Weakly informative
- `pm.Uniform('p', lower=0, upper=1)` - Non-informative (use sparingly)

**Correlation matrices**:
- `pm.LKJCorr('corr', n=n_vars, eta=2)` - eta=1 uniform, eta>1 prefers identity

### For Likelihoods

**Continuous outcomes**:
- `pm.Normal('y', mu=mu, sigma=sigma)` - Default for continuous data
- `pm.StudentT('y', nu=nu, mu=mu, sigma=sigma)` - Robust to outliers

**Count data**:
- `pm.Poisson('y', mu=lambda)` - Equidispersed counts
- `pm.NegativeBinomial('y', mu=mu, alpha=alpha)` - Overdispersed counts
- `pm.ZeroInflatedPoisson('y', psi=psi, mu=mu)` - Excess zeros

**Binary outcomes**:
- `pm.Bernoulli('y', p=p)` or `pm.Bernoulli('y', logit_p=logit_p)`

**Categorical outcomes**:
- `pm.Categorical('y', p=probs)`

**See:** `references/distributions.md` for comprehensive distribution reference

## Sampling and Inference

### MCMC with NUTS

Default and recommended for most models:

```python
idata = pm.sample(
    draws=2000,
    tune=1000,
    chains=4,
    target_accept=0.9,
    random_seed=42
)
```

**Adjust when needed:**
- Divergences → `target_accept=0.95` or higher
- Slow sampling → Use ADVI for initialization
- Discrete parameters → Use `pm.Metropolis()` for discrete vars

### Variational Inference

Fast approximation for exploration or initialization:

```python
with model:
    approx = pm.fit(n=20000, method='advi')

    # Use for initialization
    start = approx.sample(return_inferencedata=False)[0]
    idata = pm.sample(start=start)
```

**Trade-offs:**
- Much faster than MCMC
- Approximate (may underestimate uncertainty)
- Good for large models or quick exploration

**See:** `references/sampling_inference.md` for detailed sampling guide

## Diagnostic Scripts

### Comprehensive Diagnostics

```python
from scripts.model_diagnostics import create_diagnostic_report

create_diagnostic_report(
    idata,
    var_names=['alpha', 'beta', 'sigma'],
    output_dir='diagnostics/'
)
```

Creates:
- Trace plots
- Rank plots (mixing check)
- Autocorrelation plots
- Energy plots
- ESS evolution
- Summary statistics CSV

### Quick Diagnostic Check

```python
from scripts.model_diagnostics import check_diagnostics

results = check_diagnostics(idata)
```

Checks R-hat, ESS, divergences, and tree depth.

## Common Issues and Solutions

### Divergences

**Symptom:** `idata.sample_stats.diverging.sum() > 0`

**Solutions:**
1. Increase `target_accept=0.95` or `0.99`
2. Use non-centered parameterization (hierarchical models)
3. Add stronger priors to constrain parameters
4. Check for model misspecification

### Low Effective Sample Size

**Symptom:** `ESS < 400`

**Solutions:**
1. Sample more draws: `draws=5000`
2. Reparameterize to reduce posterior correlation
3. Use QR decomposition for regression with correlated predictors

### High R-hat

**Symptom:** `R-hat > 1.01`

**Solutions:**
1. Run longer chains: `tune=2000, draws=5000`
2. Check for multimodality
3. Improve initialization with ADVI

### Slow Sampling

**Solutions:**
1. Use ADVI initialization
2. Reduce model complexity
3. Increase parallelization: `cores=8, chains=8`
4. Use variational inference if appropriate

## Best Practices

### Model Building

1. **Always standardize predictors** for better sampling
2. **Use weakly informative priors** (not flat)
3. **Use named dimensions** (`dims`) for clarity
4. **Non-centered parameterization** for hierarchical models
5. **Check prior predictive** before fitting

### Sampling

1. **Run multiple chains** (at least 4) for convergence
2. **Use `target_accept=0.9`** as baseline (higher if needed)
3. **Include `log_likelihood=True`** for model comparison
4. **Set random seed** for reproducibility

### Validation

1. **Check diagnostics** before interpretation (R-hat, ESS, divergences)
2. **Posterior predictive check** for model validation
3. **Compare multiple models** when appropriate
4. **Report uncertainty** (HDI intervals, not just point estimates)

### Workflow

1. Start simple, add complexity gradually
2. Prior predictive check → Fit → Diagnostics → Posterior predictive check
3. Iterate on model specification based on checks
4. Document assumptions and prior choices

## Resources

This skill includes:

### References (`references/`)

- **`distributions.md`**: Comprehensive catalog of PyMC distributions organized by category (continuous, discrete, multivariate, mixture, time series). Use when selecting priors or likelihoods.

- **`sampling_inference.md`**: Detailed guide to sampling algorithms (NUTS, Metropolis, SMC), variational inference (ADVI, SVGD), and handling sampling issues. Use when encountering convergence problems or choosing inference methods.

- **`workflows.md`**: Complete workflow examples and code patterns for common model types, data preparation, prior selection, and model validation. Use as a cookbook for standard Bayesian analyses.

### Scripts (`scripts/`)

- **`model_diagnostics.py`**: Automated diagnostic checking and report generation. Functions: `check_diagnostics()` for quick checks, `create_diagnostic_report()` for comprehensive analysis with plots.

- **`model_comparison.py`**: Model comparison utilities using LOO/WAIC. Functions: `compare_models()`, `check_loo_reliability()`, `model_averaging()`.

### Templates (`assets/`)

- **`linear_regression_template.py`**: Complete template for Bayesian linear regression with full workflow (data prep, prior checks, fitting, diagnostics, predictions).

- **`hierarchical_model_template.py`**: Complete template for hierarchical/multilevel models with non-centered parameterization and group-level analysis.

## Quick Reference

### Model Building
```python
with pm.Model(coords={'var': names}) as model:
    # Priors
    param = pm.Normal('param', mu=0, sigma=1, dims='var')
    # Likelihood
    y = pm.Normal('y', mu=..., sigma=..., observed=data)
```

### Sampling
```python
idata = pm.sample(draws=2000, tune=1000, chains=4, target_accept=0.9)
```

### Diagnostics
```python
from scripts.model_diagnostics import check_diagnostics
check_diagnostics(idata)
```

### Model Comparison
```python
from scripts.model_comparison import compare_models
compare_models({'m1': idata1, 'm2': idata2}, ic='loo')
```

### Predictions
```python
with model:
    pm.set_data({'X': X_new})
    pred = pm.sample_posterior_predictive(idata.posterior)
```

## Additional Notes

- PyMC integrates with ArviZ for visualization and diagnostics
- Use `pm.model_to_graphviz(model)` to visualize model structure
- Save results with `idata.to_netcdf('results.nc')`
- Load with `az.from_netcdf('results.nc')`
- For very large models, consider minibatch ADVI or data subsampling

---

## Reference: Distributions

# PyMC Distributions Reference

This reference provides a comprehensive catalog of probability distributions available in PyMC, organized by category. Use this to select appropriate distributions for priors and likelihoods when building Bayesian models.

## Continuous Distributions

Continuous distributions define probability densities over real-valued domains.

### Common Continuous Distributions

**`pm.Normal(name, mu, sigma)`**
- Normal (Gaussian) distribution
- Parameters: `mu` (mean), `sigma` (standard deviation)
- Support: (-∞, ∞)
- Common uses: Default prior for unbounded parameters, likelihood for continuous data with additive noise

**`pm.HalfNormal(name, sigma)`**
- Half-normal distribution (positive half of normal)
- Parameters: `sigma` (standard deviation)
- Support: [0, ∞)
- Common uses: Prior for scale/standard deviation parameters

**`pm.Uniform(name, lower, upper)`**
- Uniform distribution
- Parameters: `lower`, `upper` (bounds)
- Support: [lower, upper]
- Common uses: Weakly informative prior when parameter must be bounded

**`pm.Beta(name, alpha, beta)`**
- Beta distribution
- Parameters: `alpha`, `beta` (shape parameters)
- Support: [0, 1]
- Common uses: Prior for probabilities and proportions

**`pm.Gamma(name, alpha, beta)`**
- Gamma distribution
- Parameters: `alpha` (shape), `beta` (rate)
- Support: (0, ∞)
- Common uses: Prior for positive parameters, rate parameters

**`pm.Exponential(name, lam)`**
- Exponential distribution
- Parameters: `lam` (rate parameter)
- Support: [0, ∞)
- Common uses: Prior for scale parameters, waiting times

**`pm.LogNormal(name, mu, sigma)`**
- Log-normal distribution
- Parameters: `mu`, `sigma` (parameters of underlying normal)
- Support: (0, ∞)
- Common uses: Prior for positive parameters with multiplicative effects

**`pm.StudentT(name, nu, mu, sigma)`**
- Student's t-distribution
- Parameters: `nu` (degrees of freedom), `mu` (location), `sigma` (scale)
- Support: (-∞, ∞)
- Common uses: Robust alternative to normal for outlier-resistant models

**`pm.Cauchy(name, alpha, beta)`**
- Cauchy distribution
- Parameters: `alpha` (location), `beta` (scale)
- Support: (-∞, ∞)
- Common uses: Heavy-tailed alternative to normal

### Specialized Continuous Distributions

**`pm.Laplace(name, mu, b)`** - Laplace (double exponential) distribution

**`pm.AsymmetricLaplace(name, kappa, mu, b)`** - Asymmetric Laplace distribution

**`pm.InverseGamma(name, alpha, beta)`** - Inverse gamma distribution

**`pm.Weibull(name, alpha, beta)`** - Weibull distribution for reliability analysis

**`pm.Logistic(name, mu, s)`** - Logistic distribution

**`pm.LogitNormal(name, mu, sigma)`** - Logit-normal distribution for (0,1) support

**`pm.Pareto(name, alpha, m)`** - Pareto distribution for power-law phenomena

**`pm.ChiSquared(name, nu)`** - Chi-squared distribution

**`pm.ExGaussian(name, mu, sigma, nu)`** - Exponentially modified Gaussian

**`pm.VonMises(name, mu, kappa)`** - Von Mises (circular normal) distribution

**`pm.SkewNormal(name, mu, sigma, alpha)`** - Skew-normal distribution

**`pm.Triangular(name, lower, c, upper)`** - Triangular distribution

**`pm.Gumbel(name, mu, beta)`** - Gumbel distribution for extreme values

**`pm.Rice(name, nu, sigma)`** - Rice (Rician) distribution

**`pm.Moyal(name, mu, sigma)`** - Moyal distribution

**`pm.Kumaraswamy(name, a, b)`** - Kumaraswamy distribution (Beta alternative)

**`pm.Interpolated(name, x_points, pdf_points)`** - Custom distribution from interpolation

## Discrete Distributions

Discrete distributions define probabilities over integer-valued domains.

### Common Discrete Distributions

**`pm.Bernoulli(name, p)`**
- Bernoulli distribution (binary outcome)
- Parameters: `p` (success probability)
- Support: {0, 1}
- Common uses: Binary classification, coin flips

**`pm.Binomial(name, n, p)`**
- Binomial distribution
- Parameters: `n` (number of trials), `p` (success probability)
- Support: {0, 1, ..., n}
- Common uses: Number of successes in fixed trials

**`pm.Poisson(name, mu)`**
- Poisson distribution
- Parameters: `mu` (rate parameter)
- Support: {0, 1, 2, ...}
- Common uses: Count data, rates, occurrences

**`pm.Categorical(name, p)`**
- Categorical distribution
- Parameters: `p` (probability vector)
- Support: {0, 1, ..., K-1}
- Common uses: Multi-class classification

**`pm.DiscreteUniform(name, lower, upper)`**
- Discrete uniform distribution
- Parameters: `lower`, `upper` (bounds)
- Support: {lower, ..., upper}
- Common uses: Uniform prior over finite integers

**`pm.NegativeBinomial(name, mu, alpha)`**
- Negative binomial distribution
- Parameters: `mu` (mean), `alpha` (dispersion)
- Support: {0, 1, 2, ...}
- Common uses: Overdispersed count data

**`pm.Geometric(name, p)`**
- Geometric distribution
- Parameters: `p` (success probability)
- Support: {0, 1, 2, ...}
- Common uses: Number of failures before first success

### Specialized Discrete Distributions

**`pm.BetaBinomial(name, alpha, beta, n)`** - Beta-binomial (overdispersed binomial)

**`pm.HyperGeometric(name, N, k, n)`** - Hypergeometric distribution

**`pm.DiscreteWeibull(name, q, beta)`** - Discrete Weibull distribution

**`pm.OrderedLogistic(name, eta, cutpoints)`** - Ordered logistic for ordinal data

**`pm.OrderedProbit(name, eta, cutpoints)`** - Ordered probit for ordinal data

## Multivariate Distributions

Multivariate distributions define joint probability distributions over vector-valued random variables.

### Common Multivariate Distributions

**`pm.MvNormal(name, mu, cov)`**
- Multivariate normal distribution
- Parameters: `mu` (mean vector), `cov` (covariance matrix)
- Common uses: Correlated continuous variables, Gaussian processes

**`pm.Dirichlet(name, a)`**
- Dirichlet distribution
- Parameters: `a` (concentration parameters)
- Support: Simplex (sums to 1)
- Common uses: Prior for probability vectors, topic modeling

**`pm.Multinomial(name, n, p)`**
- Multinomial distribution
- Parameters: `n` (number of trials), `p` (probability vector)
- Common uses: Count data across multiple categories

**`pm.MvStudentT(name, nu, mu, cov)`**
- Multivariate Student's t-distribution
- Parameters: `nu` (degrees of freedom), `mu` (location), `cov` (scale matrix)
- Common uses: Robust multivariate modeling

### Specialized Multivariate Distributions

**`pm.LKJCorr(name, n, eta)`** - LKJ correlation matrix prior (for correlation matrices)

**`pm.LKJCholeskyCov(name, n, eta, sd_dist)`** - LKJ prior with Cholesky decomposition

**`pm.Wishart(name, nu, V)`** - Wishart distribution (for covariance matrices)

**`pm.InverseWishart(name, nu, V)`** - Inverse Wishart distribution

**`pm.MatrixNormal(name, mu, rowcov, colcov)`** - Matrix normal distribution

**`pm.KroneckerNormal(name, mu, covs, sigma)`** - Kronecker-structured normal

**`pm.CAR(name, mu, W, alpha, tau)`** - Conditional autoregressive (spatial)

**`pm.ICAR(name, W, sigma)`** - Intrinsic conditional autoregressive (spatial)

## Mixture Distributions

Mixture distributions combine multiple component distributions.

**`pm.Mixture(name, w, comp_dists)`**
- General mixture distribution
- Parameters: `w` (weights), `comp_dists` (component distributions)
- Common uses: Clustering, multi-modal data

**`pm.NormalMixture(name, w, mu, sigma)`**
- Mixture of normal distributions
- Common uses: Mixture of Gaussians clustering

### Zero-Inflated and Hurdle Models

**`pm.ZeroInflatedPoisson(name, psi, mu)`** - Excess zeros in count data

**`pm.ZeroInflatedBinomial(name, psi, n, p)`** - Zero-inflated binomial

**`pm.ZeroInflatedNegativeBinomial(name, psi, mu, alpha)`** - Zero-inflated negative binomial

**`pm.HurdlePoisson(name, psi, mu)`** - Hurdle Poisson (two-part model)

**`pm.HurdleGamma(name, psi, alpha, beta)`** - Hurdle gamma

**`pm.HurdleLogNormal(name, psi, mu, sigma)`** - Hurdle log-normal

## Time Series Distributions

Distributions designed for temporal data and sequential modeling.

**`pm.AR(name, rho, sigma, init_dist)`**
- Autoregressive process
- Parameters: `rho` (AR coefficients), `sigma` (innovation std), `init_dist` (initial distribution)
- Common uses: Time series modeling, sequential data

**`pm.GaussianRandomWalk(name, mu, sigma, init_dist)`**
- Gaussian random walk
- Parameters: `mu` (drift), `sigma` (step size), `init_dist` (initial value)
- Common uses: Cumulative processes, random walk priors

**`pm.MvGaussianRandomWalk(name, mu, cov, init_dist)`**
- Multivariate Gaussian random walk

**`pm.GARCH11(name, omega, alpha_1, beta_1)`**
- GARCH(1,1) volatility model
- Common uses: Financial time series, volatility modeling

**`pm.EulerMaruyama(name, dt, sde_fn, sde_pars, init_dist)`**
- Stochastic differential equation via Euler-Maruyama discretization
- Common uses: Continuous-time processes

## Special Distributions

**`pm.Deterministic(name, var)`**
- Deterministic transformation (not a random variable)
- Use for computed quantities derived from other variables

**`pm.Potential(name, logp)`**
- Add arbitrary log-probability contribution
- Use for custom likelihood components or constraints

**`pm.Flat(name)`**
- Improper flat prior (constant density)
- Use sparingly; can cause sampling issues

**`pm.HalfFlat(name)`**
- Improper flat prior on positive reals
- Use sparingly; can cause sampling issues

## Distribution Modifiers

**`pm.Truncated(name, dist, lower, upper)`**
- Truncate any distribution to specified bounds

**`pm.Censored(name, dist, lower, upper)`**
- Handle censored observations (observed bounds, not exact values)

**`pm.CustomDist(name, ..., logp, random)`**
- Define custom distributions with user-specified log-probability and random sampling functions

**`pm.Simulator(name, fn, params, ...)`**
- Custom distributions via simulation (for likelihood-free inference)

## Usage Tips

### Choosing Priors

1. **Scale parameters** (σ, τ): Use `HalfNormal`, `HalfCauchy`, `Exponential`, or `Gamma`
2. **Probabilities**: Use `Beta` or `Uniform(0, 1)`
3. **Unbounded parameters**: Use `Normal` or `StudentT` (for robustness)
4. **Positive parameters**: Use `LogNormal`, `Gamma`, or `Exponential`
5. **Correlation matrices**: Use `LKJCorr`
6. **Count data**: Use `Poisson` or `NegativeBinomial` (for overdispersion)

### Shape Broadcasting

PyMC distributions support NumPy-style broadcasting. Use the `shape` parameter to create vectors or arrays of random variables:

```python
# Vector of 5 independent normals
beta = pm.Normal('beta', mu=0, sigma=1, shape=5)

# 3x4 matrix of independent gammas
tau = pm.Gamma('tau', alpha=2, beta=1, shape=(3, 4))
```

### Using dims for Named Dimensions

Instead of shape, use `dims` for more readable models:

```python
with pm.Model(coords={'predictors': ['age', 'income', 'education']}) as model:
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
```

---

## Reference: Sampling_Inference

# PyMC Sampling and Inference Methods

This reference covers the sampling algorithms and inference methods available in PyMC for posterior inference.

## MCMC Sampling Methods

### Primary Sampling Function

**`pm.sample(draws=1000, tune=1000, chains=4, **kwargs)`**

The main interface for MCMC sampling in PyMC.

**Key Parameters:**
- `draws`: Number of samples to draw per chain (default: 1000)
- `tune`: Number of tuning/warmup samples (default: 1000, discarded)
- `chains`: Number of parallel chains (default: 4)
- `cores`: Number of CPU cores to use (default: all available)
- `target_accept`: Target acceptance rate for step size tuning (default: 0.8, increase to 0.9-0.95 for difficult posteriors)
- `random_seed`: Random seed for reproducibility
- `return_inferencedata`: Return ArviZ InferenceData object (default: True)
- `idata_kwargs`: Additional kwargs for InferenceData creation (e.g., `{"log_likelihood": True}` for model comparison)

**Returns:** InferenceData object containing posterior samples, sampling statistics, and diagnostics

**Example:**
```python
with pm.Model() as model:
    # ... define model ...
    idata = pm.sample(draws=2000, tune=1000, chains=4, target_accept=0.9)
```

### Sampling Algorithms

PyMC automatically selects appropriate samplers based on model structure, but you can specify algorithms manually.

#### NUTS (No-U-Turn Sampler)

**Default algorithm** for continuous parameters. Highly efficient Hamiltonian Monte Carlo variant.

- Automatically tunes step size and mass matrix
- Adaptive: explores posterior geometry during tuning
- Best for smooth, continuous posteriors
- Can struggle with high correlation or multimodality

**Manual specification:**
```python
with model:
    idata = pm.sample(step=pm.NUTS(target_accept=0.95))
```

**When to adjust:**
- Increase `target_accept` (0.9-0.99) if seeing divergences
- Use `init='adapt_diag'` for faster initialization (default)
- Use `init='jitter+adapt_diag'` for difficult initializations

#### Metropolis

General-purpose Metropolis-Hastings sampler.

- Works for both continuous and discrete variables
- Less efficient than NUTS for smooth continuous posteriors
- Useful for discrete parameters or non-differentiable models
- Requires manual tuning

**Example:**
```python
with model:
    idata = pm.sample(step=pm.Metropolis())
```

#### Slice Sampler

Slice sampling for univariate distributions.

- No tuning required
- Good for difficult univariate posteriors
- Can be slow for high dimensions

**Example:**
```python
with model:
    idata = pm.sample(step=pm.Slice())
```

#### CompoundStep

Combine different samplers for different parameters.

**Example:**
```python
with model:
    # Use NUTS for continuous params, Metropolis for discrete
    step1 = pm.NUTS([continuous_var1, continuous_var2])
    step2 = pm.Metropolis([discrete_var])
    idata = pm.sample(step=[step1, step2])
```

### Sampling Diagnostics

PyMC automatically computes diagnostics. Check these before trusting results:

#### Effective Sample Size (ESS)

Measures independent information in correlated samples.

- **Rule of thumb**: ESS > 400 per chain (1600 total for 4 chains)
- Low ESS indicates high autocorrelation
- Access via: `az.ess(idata)`

#### R-hat (Gelman-Rubin statistic)

Measures convergence across chains.

- **Rule of thumb**: R-hat < 1.01 for all parameters
- R-hat > 1.01 indicates non-convergence
- Access via: `az.rhat(idata)`

#### Divergences

Indicate regions where NUTS struggled.

- **Rule of thumb**: 0 divergences (or very few)
- Divergences suggest biased samples
- **Fix**: Increase `target_accept`, reparameterize, or use stronger priors
- Access via: `idata.sample_stats.diverging.sum()`

#### Energy Plot

Visualizes Hamiltonian Monte Carlo energy transitions.

```python
az.plot_energy(idata)
```

Good separation between energy distributions indicates healthy sampling.

### Handling Sampling Issues

#### Divergences

```python
# Increase target acceptance rate
idata = pm.sample(target_accept=0.95)

# Or reparameterize using non-centered parameterization
# Bad (centered):
mu = pm.Normal('mu', 0, 1)
sigma = pm.HalfNormal('sigma', 1)
x = pm.Normal('x', mu, sigma, observed=data)

# Good (non-centered):
mu = pm.Normal('mu', 0, 1)
sigma = pm.HalfNormal('sigma', 1)
x_offset = pm.Normal('x_offset', 0, 1, observed=(data - mu) / sigma)
```

#### Slow Sampling

```python
# Use fewer tuning steps if model is simple
idata = pm.sample(tune=500)

# Increase cores for parallelization
idata = pm.sample(cores=8, chains=8)

# Use variational inference for initialization
with model:
    approx = pm.fit()  # Run ADVI
    idata = pm.sample(start=approx.sample(return_inferencedata=False)[0])
```

#### High Autocorrelation

```python
# Increase draws
idata = pm.sample(draws=5000)

# Reparameterize to reduce correlation
# Consider using QR decomposition for regression models
```

## Variational Inference

Faster approximate inference for large models or quick exploration.

### ADVI (Automatic Differentiation Variational Inference)

**`pm.fit(n=10000, method='advi', **kwargs)`**

Approximates posterior with simpler distribution (typically mean-field Gaussian).

**Key Parameters:**
- `n`: Number of iterations (default: 10000)
- `method`: VI algorithm ('advi', 'fullrank_advi', 'svgd')
- `random_seed`: Random seed

**Returns:** Approximation object for sampling and analysis

**Example:**
```python
with model:
    approx = pm.fit(n=50000)
    # Draw samples from approximation
    idata = approx.sample(1000)
    # Or sample for MCMC initialization
    start = approx.sample(return_inferencedata=False)[0]
```

**Trade-offs:**
- **Pros**: Much faster than MCMC, scales to large data
- **Cons**: Approximate, may miss posterior structure, underestimates uncertainty

### Full-Rank ADVI

Captures correlations between parameters.

```python
with model:
    approx = pm.fit(method='fullrank_advi')
```

More accurate than mean-field but slower.

### SVGD (Stein Variational Gradient Descent)

Non-parametric variational inference.

```python
with model:
    approx = pm.fit(method='svgd', n=20000)
```

Better captures multimodality but more computationally expensive.

## Prior and Posterior Predictive Sampling

### Prior Predictive Sampling

Sample from the prior distribution (before seeing data).

**`pm.sample_prior_predictive(samples=500, **kwargs)`**

**Purpose:**
- Validate priors are reasonable
- Check implied predictions before fitting
- Ensure model generates plausible data

**Example:**
```python
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000)

# Visualize prior predictions
az.plot_ppc(prior_pred, group='prior')
```

### Posterior Predictive Sampling

Sample from posterior predictive distribution (after fitting).

**`pm.sample_posterior_predictive(trace, **kwargs)`**

**Purpose:**
- Model validation via posterior predictive checks
- Generate predictions for new data
- Assess goodness-of-fit

**Example:**
```python
with model:
    # After sampling
    idata = pm.sample()

    # Add posterior predictive samples
    pm.sample_posterior_predictive(idata, extend_inferencedata=True)

# Posterior predictive check
az.plot_ppc(idata)
```

### Predictions for New Data

Update data and sample predictive distribution:

```python
with model:
    # Original model fit
    idata = pm.sample()

    # Update with new predictor values
    pm.set_data({'X': X_new})

    # Sample predictions
    post_pred_new = pm.sample_posterior_predictive(
        idata.posterior,
        var_names=['y_pred']
    )
```

## Maximum A Posteriori (MAP) Estimation

Find posterior mode (point estimate).

**`pm.find_MAP(start=None, method='L-BFGS-B', **kwargs)`**

**When to use:**
- Quick point estimates
- Initialization for MCMC
- When full posterior not needed

**Example:**
```python
with model:
    map_estimate = pm.find_MAP()
    print(map_estimate)
```

**Limitations:**
- Doesn't quantify uncertainty
- Can find local optima in multimodal posteriors
- Sensitive to prior specification

## Inference Recommendations

### Standard Workflow

1. **Start with ADVI** for quick exploration:
   ```python
   approx = pm.fit(n=20000)
   ```

2. **Run MCMC** for full inference:
   ```python
   idata = pm.sample(draws=2000, tune=1000)
   ```

3. **Check diagnostics**:
   ```python
   az.summary(idata, var_names=['~mu_log__'])  # Exclude transformed vars
   ```

4. **Sample posterior predictive**:
   ```python
   pm.sample_posterior_predictive(idata, extend_inferencedata=True)
   ```

### Choosing Inference Method

| Scenario | Recommended Method |
|----------|-------------------|
| Small-medium models, need full uncertainty | MCMC with NUTS |
| Large models, initial exploration | ADVI |
| Discrete parameters | Metropolis or marginalize |
| Hierarchical models with divergences | Non-centered parameterization + NUTS |
| Very large data | Minibatch ADVI |
| Quick point estimates | MAP or ADVI |

### Reparameterization Tricks

**Non-centered parameterization** for hierarchical models:

```python
# Centered (can cause divergences):
mu = pm.Normal('mu', 0, 10)
sigma = pm.HalfNormal('sigma', 1)
theta = pm.Normal('theta', mu, sigma, shape=n_groups)

# Non-centered (better sampling):
mu = pm.Normal('mu', 0, 10)
sigma = pm.HalfNormal('sigma', 1)
theta_offset = pm.Normal('theta_offset', 0, 1, shape=n_groups)
theta = pm.Deterministic('theta', mu + sigma * theta_offset)
```

**QR decomposition** for correlated predictors:

```python
import numpy as np

# QR decomposition
Q, R = np.linalg.qr(X)

with pm.Model():
    # Uncorrelated coefficients
    beta_tilde = pm.Normal('beta_tilde', 0, 1, shape=p)

    # Transform back to original scale
    beta = pm.Deterministic('beta', pm.math.solve(R, beta_tilde))

    mu = pm.math.dot(Q, beta_tilde)
    sigma = pm.HalfNormal('sigma', 1)
    y = pm.Normal('y', mu, sigma, observed=y_obs)
```

## Advanced Sampling

### Sequential Monte Carlo (SMC)

For complex posteriors or model evidence estimation:

```python
with model:
    idata = pm.sample_smc(draws=2000, chains=4)
```

Good for multimodal posteriors or when NUTS struggles.

### Custom Initialization

Provide starting values:

```python
start = {'mu': 0, 'sigma': 1}
with model:
    idata = pm.sample(start=start)
```

Or use MAP estimate:

```python
with model:
    start = pm.find_MAP()
    idata = pm.sample(start=start)
```

---

## Reference: Workflows

# PyMC Workflows and Common Patterns

This reference provides standard workflows and patterns for building, validating, and analyzing Bayesian models in PyMC.

## Standard Bayesian Workflow

### Complete Workflow Template

```python
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# 1. PREPARE DATA
# ===============
X = ...  # Predictor variables
y = ...  # Observed outcomes

# Standardize predictors for better sampling
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)

# 2. BUILD MODEL
# ==============
with pm.Model() as model:
    # Define coordinates for named dimensions
    coords = {
        'predictors': ['var1', 'var2', 'var3'],
        'obs_id': np.arange(len(y))
    }

    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear predictor
    mu = alpha + pm.math.dot(X_scaled, beta)

    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y, dims='obs_id')

# 3. PRIOR PREDICTIVE CHECK
# ==========================
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000, random_seed=42)

# Visualize prior predictions
az.plot_ppc(prior_pred, group='prior', num_pp_samples=100)
plt.title('Prior Predictive Check')
plt.show()

# 4. FIT MODEL
# ============
with model:
    # Quick VI exploration (optional)
    approx = pm.fit(n=20000, random_seed=42)

    # Full MCMC inference
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
        idata_kwargs={'log_likelihood': True}  # For model comparison
    )

# 5. CHECK DIAGNOSTICS
# ====================
# Summary statistics
print(az.summary(idata, var_names=['alpha', 'beta', 'sigma']))

# R-hat and ESS
summary = az.summary(idata)
if (summary['r_hat'] > 1.01).any():
    print("WARNING: Some R-hat values > 1.01, chains may not have converged")

if (summary['ess_bulk'] < 400).any():
    print("WARNING: Some ESS values < 400, consider more samples")

# Check divergences
divergences = idata.sample_stats.diverging.sum().item()
print(f"Number of divergences: {divergences}")

# Trace plots
az.plot_trace(idata, var_names=['alpha', 'beta', 'sigma'])
plt.tight_layout()
plt.show()

# 6. POSTERIOR PREDICTIVE CHECK
# ==============================
with model:
    pm.sample_posterior_predictive(idata, extend_inferencedata=True, random_seed=42)

# Visualize fit
az.plot_ppc(idata, num_pp_samples=100)
plt.title('Posterior Predictive Check')
plt.show()

# 7. ANALYZE RESULTS
# ==================
# Posterior distributions
az.plot_posterior(idata, var_names=['alpha', 'beta', 'sigma'])
plt.tight_layout()
plt.show()

# Forest plot for coefficients
az.plot_forest(idata, var_names=['beta'], combined=True)
plt.title('Coefficient Estimates')
plt.show()

# 8. PREDICTIONS FOR NEW DATA
# ============================
X_new = ...  # New predictor values
X_new_scaled = (X_new - X.mean(axis=0)) / X.std(axis=0)

with model:
    # Update data
    pm.set_data({'X': X_new_scaled})

    # Sample predictions
    post_pred = pm.sample_posterior_predictive(
        idata.posterior,
        var_names=['y_obs'],
        random_seed=42
    )

# Prediction intervals
y_pred_mean = post_pred.posterior_predictive['y_obs'].mean(dim=['chain', 'draw'])
y_pred_hdi = az.hdi(post_pred.posterior_predictive, var_names=['y_obs'])

# 9. SAVE RESULTS
# ===============
idata.to_netcdf('model_results.nc')  # Save for later
```

## Model Building Patterns

### Linear Regression

```python
with pm.Model() as linear_model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear predictor
    mu = alpha + pm.math.dot(X, beta)

    # Likelihood
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs)
```

### Logistic Regression

```python
with pm.Model() as logistic_model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    # Linear predictor
    logit_p = alpha + pm.math.dot(X, beta)

    # Likelihood
    y = pm.Bernoulli('y', logit_p=logit_p, observed=y_obs)
```

### Hierarchical/Multilevel Model

```python
with pm.Model(coords={'group': group_names, 'obs': np.arange(n_obs)}) as hierarchical_model:
    # Hyperpriors
    mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)

    mu_beta = pm.Normal('mu_beta', mu=0, sigma=10)
    sigma_beta = pm.HalfNormal('sigma_beta', sigma=1)

    # Group-level parameters (non-centered)
    alpha_offset = pm.Normal('alpha_offset', mu=0, sigma=1, dims='group')
    alpha = pm.Deterministic('alpha', mu_alpha + sigma_alpha * alpha_offset, dims='group')

    beta_offset = pm.Normal('beta_offset', mu=0, sigma=1, dims='group')
    beta = pm.Deterministic('beta', mu_beta + sigma_beta * beta_offset, dims='group')

    # Observation-level model
    mu = alpha[group_idx] + beta[group_idx] * X

    sigma = pm.HalfNormal('sigma', sigma=1)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=y_obs, dims='obs')
```

### Poisson Regression (Count Data)

```python
with pm.Model() as poisson_model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10, shape=n_predictors)

    # Linear predictor on log scale
    log_lambda = alpha + pm.math.dot(X, beta)

    # Likelihood
    y = pm.Poisson('y', mu=pm.math.exp(log_lambda), observed=y_obs)
```

### Time Series (Autoregressive)

```python
with pm.Model() as ar_model:
    # Innovation standard deviation
    sigma = pm.HalfNormal('sigma', sigma=1)

    # AR coefficients
    rho = pm.Normal('rho', mu=0, sigma=0.5, shape=ar_order)

    # Initial distribution
    init_dist = pm.Normal.dist(mu=0, sigma=sigma)

    # AR process
    y = pm.AR('y', rho=rho, sigma=sigma, init_dist=init_dist, observed=y_obs)
```

### Mixture Model

```python
with pm.Model() as mixture_model:
    # Component weights
    w = pm.Dirichlet('w', a=np.ones(n_components))

    # Component parameters
    mu = pm.Normal('mu', mu=0, sigma=10, shape=n_components)
    sigma = pm.HalfNormal('sigma', sigma=1, shape=n_components)

    # Mixture
    components = [pm.Normal.dist(mu=mu[i], sigma=sigma[i]) for i in range(n_components)]
    y = pm.Mixture('y', w=w, comp_dists=components, observed=y_obs)
```

## Data Preparation Best Practices

### Standardization

Standardize continuous predictors for better sampling:

```python
# Standardize
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std

# Model with scaled data
with pm.Model() as model:
    beta_scaled = pm.Normal('beta_scaled', 0, 1)
    # ... rest of model ...

# Transform back to original scale
beta_original = beta_scaled / X_std
alpha_original = alpha - (beta_scaled * X_mean / X_std).sum()
```

### Handling Missing Data

Treat missing values as parameters:

```python
# Identify missing values
missing_idx = np.isnan(X)
X_observed = np.where(missing_idx, 0, X)  # Placeholder

with pm.Model() as model:
    # Prior for missing values
    X_missing = pm.Normal('X_missing', mu=0, sigma=1, shape=missing_idx.sum())

    # Combine observed and imputed
    X_complete = pm.math.switch(missing_idx.flatten(), X_missing, X_observed.flatten())

    # ... rest of model using X_complete ...
```

### Centering and Scaling

For regression models, center predictors and outcome:

```python
# Center
X_centered = X - X.mean(axis=0)
y_centered = y - y.mean()

with pm.Model() as model:
    # Simpler prior on intercept
    alpha = pm.Normal('alpha', mu=0, sigma=1)  # Intercept near 0 when centered
    beta = pm.Normal('beta', mu=0, sigma=1, shape=n_predictors)

    mu = alpha + pm.math.dot(X_centered, beta)
    sigma = pm.HalfNormal('sigma', sigma=1)

    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_centered)
```

## Prior Selection Guidelines

### Weakly Informative Priors

Use when you have limited prior knowledge:

```python
# For standardized predictors
beta = pm.Normal('beta', mu=0, sigma=1)

# For scale parameters
sigma = pm.HalfNormal('sigma', sigma=1)

# For probabilities
p = pm.Beta('p', alpha=2, beta=2)  # Slight preference for middle values
```

### Informative Priors

Use domain knowledge:

```python
# Effect size from literature: Cohen's d ≈ 0.3
beta = pm.Normal('beta', mu=0.3, sigma=0.1)

# Physical constraint: probability between 0.7-0.9
p = pm.Beta('p', alpha=8, beta=2)  # Check with prior predictive!
```

### Prior Predictive Checks

Always validate priors:

```python
with model:
    prior_pred = pm.sample_prior_predictive(samples=1000)

# Check if predictions are reasonable
print(f"Prior predictive range: {prior_pred.prior_predictive['y'].min():.2f} to {prior_pred.prior_predictive['y'].max():.2f}")
print(f"Observed range: {y_obs.min():.2f} to {y_obs.max():.2f}")

# Visualize
az.plot_ppc(prior_pred, group='prior')
```

## Model Comparison Workflow

### Comparing Multiple Models

```python
import arviz as az

# Fit multiple models
models = {}
idatas = {}

# Model 1: Simple linear
with pm.Model() as models['linear']:
    # ... define model ...
    idatas['linear'] = pm.sample(idata_kwargs={'log_likelihood': True})

# Model 2: With interaction
with pm.Model() as models['interaction']:
    # ... define model ...
    idatas['interaction'] = pm.sample(idata_kwargs={'log_likelihood': True})

# Model 3: Hierarchical
with pm.Model() as models['hierarchical']:
    # ... define model ...
    idatas['hierarchical'] = pm.sample(idata_kwargs={'log_likelihood': True})

# Compare using LOO
comparison = az.compare(idatas, ic='loo')
print(comparison)

# Visualize comparison
az.plot_compare(comparison)
plt.show()

# Check LOO reliability
for name, idata in idatas.items():
    loo = az.loo(idata, pointwise=True)
    high_pareto_k = (loo.pareto_k > 0.7).sum().item()
    if high_pareto_k > 0:
        print(f"Warning: {name} has {high_pareto_k} observations with high Pareto-k")
```

### Model Weights

```python
# Get model weights (pseudo-BMA)
weights = comparison['weight'].values

print("Model probabilities:")
for name, weight in zip(comparison.index, weights):
    print(f"  {name}: {weight:.2%}")

# Model averaging (weighted predictions)
def weighted_predictions(idatas, weights):
    preds = []
    for (name, idata), weight in zip(idatas.items(), weights):
        pred = idata.posterior_predictive['y_obs'].mean(dim=['chain', 'draw'])
        preds.append(weight * pred)
    return sum(preds)

averaged_pred = weighted_predictions(idatas, weights)
```

## Diagnostics and Troubleshooting

### Diagnosing Sampling Problems

```python
def diagnose_sampling(idata, var_names=None):
    """Comprehensive sampling diagnostics"""

    # Check convergence
    summary = az.summary(idata, var_names=var_names)

    print("=== Convergence Diagnostics ===")
    bad_rhat = summary[summary['r_hat'] > 1.01]
    if len(bad_rhat) > 0:
        print(f"⚠️  {len(bad_rhat)} variables with R-hat > 1.01")
        print(bad_rhat[['r_hat']])
    else:
        print("✓ All R-hat values < 1.01")

    # Check effective sample size
    print("\n=== Effective Sample Size ===")
    low_ess = summary[summary['ess_bulk'] < 400]
    if len(low_ess) > 0:
        print(f"⚠️  {len(low_ess)} variables with ESS < 400")
        print(low_ess[['ess_bulk', 'ess_tail']])
    else:
        print("✓ All ESS values > 400")

    # Check divergences
    print("\n=== Divergences ===")
    divergences = idata.sample_stats.diverging.sum().item()
    if divergences > 0:
        print(f"⚠️  {divergences} divergent transitions")
        print("   Consider: increase target_accept, reparameterize, or stronger priors")
    else:
        print("✓ No divergences")

    # Check tree depth
    print("\n=== NUTS Statistics ===")
    max_treedepth = idata.sample_stats.tree_depth.max().item()
    hits_max = (idata.sample_stats.tree_depth == max_treedepth).sum().item()
    if hits_max > 0:
        print(f"⚠️  Hit max treedepth {hits_max} times")
        print("   Consider: reparameterize or increase max_treedepth")
    else:
        print(f"✓ No max treedepth issues (max: {max_treedepth})")

    return summary

# Usage
diagnose_sampling(idata, var_names=['alpha', 'beta', 'sigma'])
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| Divergences | Increase `target_accept=0.95`, use non-centered parameterization |
| Low ESS | Sample more draws, reparameterize to reduce correlation |
| High R-hat | Run longer chains, check for multimodality, improve initialization |
| Slow sampling | Use ADVI initialization, reparameterize, reduce model complexity |
| Biased posterior | Check prior predictive, ensure likelihood is correct |

## Using Named Dimensions (dims)

### Benefits of dims

- More readable code
- Easier subsetting and analysis
- Better xarray integration

```python
# Define coordinates
coords = {
    'predictors': ['age', 'income', 'education'],
    'groups': ['A', 'B', 'C'],
    'time': pd.date_range('2020-01-01', periods=100, freq='D')
}

with pm.Model(coords=coords) as model:
    # Use dims instead of shape
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    alpha = pm.Normal('alpha', mu=0, sigma=1, dims='groups')
    y = pm.Normal('y', mu=0, sigma=1, dims=['groups', 'time'], observed=data)

# After sampling, dimensions are preserved
idata = pm.sample()

# Easy subsetting
beta_age = idata.posterior['beta'].sel(predictors='age')
group_A = idata.posterior['alpha'].sel(groups='A')
```

## Saving and Loading Results

```python
# Save InferenceData
idata.to_netcdf('results.nc')

# Load InferenceData
loaded_idata = az.from_netcdf('results.nc')

# Save model for later predictions
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'idata': idata}, f)

# Load model
with open('model.pkl', 'rb') as f:
    saved = pickle.load(f)
    model = saved['model']
    idata = saved['idata']
```
