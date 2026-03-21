---
title: "Denario"
description: "Multiagent AI system for scientific research assistance that automates research workflows from data analysis to publication. This skill should be used when generating research ideas from datasets, developing research methodologies, executing compu..."
category: "research"
source: "community"
author: "Community"
tags: ["denario"]
date: 2026-03-20
---

# Denario

## Overview

Denario is a multiagent AI system designed to automate scientific research workflows from initial data analysis through publication-ready manuscripts. Built on AG2 and LangGraph frameworks, it orchestrates multiple specialized agents to handle hypothesis generation, methodology development, computational analysis, and paper writing.

## When to Use This Skill

Use this skill when:
- Analyzing datasets to generate novel research hypotheses
- Developing structured research methodologies
- Executing computational experiments and generating visualizations
- Conducting literature searches for research context
- Writing journal-formatted LaTeX papers from research results
- Automating the complete research pipeline from data to publication

## Installation

Install denario using uv (recommended):

```bash
uv init
uv add "denario[app]"
```

Or using pip:

```bash
uv pip install "denario[app]"
```

For Docker deployment or building from source, see `references/installation.md`.

## LLM API Configuration

Denario requires API keys from supported LLM providers. Supported providers include:
- Google Vertex AI
- OpenAI
- Other LLM services compatible with AG2/LangGraph

Store API keys securely using environment variables or `.env` files. For detailed configuration instructions including Vertex AI setup, see `references/llm_configuration.md`.

## Core Research Workflow

Denario follows a structured four-stage research pipeline:

### 1. Data Description

Define the research context by specifying available data and tools:

```python
from denario import Denario

den = Denario(project_dir="./my_research")
den.set_data_description("""
Available datasets: time-series data on X and Y
Tools: pandas, sklearn, matplotlib
Research domain: [specify domain]
""")
```

### 2. Idea Generation

Generate research hypotheses from the data description:

```python
den.get_idea()
```

This produces a research question or hypothesis based on the described data. Alternatively, provide a custom idea:

```python
den.set_idea("Custom research hypothesis")
```

### 3. Methodology Development

Develop the research methodology:

```python
den.get_method()
```

This creates a structured approach for investigating the hypothesis. Can also accept markdown files with custom methodologies:

```python
den.set_method("path/to/methodology.md")
```

### 4. Results Generation

Execute computational experiments and generate analysis:

```python
den.get_results()
```

This runs the methodology, performs computations, creates visualizations, and produces findings. Can also provide pre-computed results:

```python
den.set_results("path/to/results.md")
```

### 5. Paper Generation

Create a publication-ready LaTeX paper:

```python
from denario import Journal

den.get_paper(journal=Journal.APS)
```

The generated paper includes proper formatting for the specified journal, integrated figures, and complete LaTeX source.

## Available Journals

Denario supports multiple journal formatting styles:
- `Journal.APS` - American Physical Society format
- Additional journals may be available; check `references/research_pipeline.md` for the complete list

## Launching the GUI

Run the graphical user interface:

```bash
denario run
```

This launches a web-based interface for interactive research workflow management.

## Common Workflows

### End-to-End Research Pipeline

```python
from denario import Denario, Journal

# Initialize project
den = Denario(project_dir="./research_project")

# Define research context
den.set_data_description("""
Dataset: Time-series measurements of [phenomenon]
Available tools: pandas, sklearn, scipy
Research goal: Investigate [research question]
""")

# Generate research idea
den.get_idea()

# Develop methodology
den.get_method()

# Execute analysis
den.get_results()

# Create publication
den.get_paper(journal=Journal.APS)
```

### Hybrid Workflow (Custom + Automated)

```python
# Provide custom research idea
den.set_idea("Investigate the correlation between X and Y using time-series analysis")

# Auto-generate methodology
den.get_method()

# Auto-generate results
den.get_results()

# Generate paper
den.get_paper(journal=Journal.APS)
```

### Literature Search Integration

For literature search functionality and additional workflow examples, see `references/examples.md`.

## Advanced Features

- **Multiagent orchestration**: AG2 and LangGraph coordinate specialized agents for different research tasks
- **Reproducible research**: All stages produce structured outputs that can be version-controlled
- **Journal integration**: Automatic formatting for target publication venues
- **Flexible input**: Manual or automated at each pipeline stage
- **Docker deployment**: Containerized environment with LaTeX and all dependencies

## Detailed References

For comprehensive documentation:
- **Installation options**: `references/installation.md`
- **LLM configuration**: `references/llm_configuration.md`
- **Complete API reference**: `references/research_pipeline.md`
- **Example workflows**: `references/examples.md`

## Troubleshooting

Common issues and solutions:
- **API key errors**: Ensure environment variables are set correctly (see `references/llm_configuration.md`)
- **LaTeX compilation**: Install TeX distribution or use Docker image with pre-installed LaTeX
- **Package conflicts**: Use virtual environments or Docker for isolation
- **Python version**: Requires Python 3.12 or higher

---

## Reference: Examples

# Denario Examples

## Complete End-to-End Research Example

This example demonstrates a full research pipeline from data to publication.

### Setup

```python
from denario import Denario, Journal
import os

# Create project directory
os.makedirs("climate_research", exist_ok=True)
den = Denario(project_dir="./climate_research")
```

### Define Research Context

```python
den.set_data_description("""
Available data: Global temperature anomaly dataset (1880-2023)
- Monthly mean temperature deviations from 1951-1980 baseline
- Global coverage with land and ocean measurements
- Format: CSV with columns [year, month, temperature_anomaly]

Available tools:
- pandas for data manipulation
- scipy for statistical analysis
- sklearn for regression modeling
- matplotlib and seaborn for visualization

Research domain: Climate science
Research goal: Quantify and characterize long-term global warming trends

Data source: NASA GISTEMP
Known characteristics: Strong autocorrelation, seasonal patterns, missing data pre-1900
""")
```

### Execute Full Pipeline

```python
# Generate research idea
den.get_idea()
# Output: "Quantify the rate of global temperature increase using
# linear regression and assess acceleration in warming trends"

# Develop methodology
den.get_method()
# Output: Creates methodology including:
# - Time-series preprocessing
# - Linear trend analysis
# - Moving average smoothing
# - Statistical significance testing
# - Visualization of trends

# Execute analysis
den.get_results()
# Output: Runs the analysis, generates:
# - Computed trend: +0.18°C per decade
# - Statistical tests: p < 0.001
# - Figure 1: Temperature anomaly over time with trend line
# - Figure 2: Decadal averages
# - Figure 3: Acceleration analysis

# Generate publication
den.get_paper(journal=Journal.APS)
# Output: Creates formatted LaTeX paper with:
# - Title, abstract, introduction
# - Methods section
# - Results with embedded figures
# - Discussion and conclusions
# - References
```

### Review Outputs

```bash
tree climate_research/
# climate_research/
# ├── data_description.txt
# ├── idea.md
# ├── methodology.md
# ├── results.md
# ├── figures/
# │   ├── temperature_trend.png
# │   ├── decadal_averages.png
# │   └── acceleration_analysis.png
# ├── paper.tex
# └── paper.pdf
```

## Enhancing Input Descriptions

Improve data descriptions for better idea generation.

### Basic Description

```python
den = Denario(project_dir="./enhanced_input")

# Start with minimal description
den.set_data_description("Gene expression data from cancer patients")
```

### Enhanced Description

```python
# Enhance with specifics
den.set_data_description("""
Dataset: Gene expression microarray data from breast cancer patients
- Sample size: 500 patients (250 responders, 250 non-responders to therapy)
- Features: Expression levels of 20,000 genes
- Format: CSV matrix (samples × genes)
- Clinical metadata: Age, tumor stage, treatment response, survival time

Available analytical tools:
- pandas for data processing
- sklearn for machine learning (PCA, random forests, SVM)
- lifelines for survival analysis
- matplotlib/seaborn for visualization

Research objectives:
- Identify gene signatures predictive of treatment response
- Discover potential therapeutic targets
- Validate findings using cross-validation

Data characteristics:
- Normalized log2 expression values
- Some missing data (<5% of values)
- Batch effects corrected
""")

den.get_idea()
# Now generates more specific and relevant research ideas
```

## Literature Search Integration

Incorporate existing research into your workflow.

### Example: Finding Related Work

```python
den = Denario(project_dir="./literature_review")

# Define research area
den.set_data_description("""
Research area: Machine learning for protein structure prediction
Available data: Protein sequence database with known structures
Tools: Biopython, TensorFlow, scikit-learn
""")

# Generate idea
den.set_idea("Develop a deep learning model for predicting protein secondary structure from amino acid sequences")

# NOTE: Literature search functionality would be integrated here
# The specific API for literature search should be checked in denario's documentation
# Example conceptual usage:
# den.search_literature(keywords=["protein structure prediction", "deep learning", "LSTM"])
# This would inform methodology and provide citations for the paper
```

## Generate Research Ideas from Data

Focus on idea generation without full pipeline execution.

### Example: Brainstorming Research Questions

```python
den = Denario(project_dir="./idea_generation")

# Provide comprehensive data description
den.set_data_description("""
Available datasets:
1. Social media sentiment data (1M tweets, 2020-2023)
2. Stock market prices (S&P 500, daily, 2020-2023)
3. Economic indicators (GDP, unemployment, inflation)

Tools: pandas, sklearn, statsmodels, Prophet, VADER sentiment analysis

Domain: Computational social science and finance
Research interests: Market prediction, sentiment analysis, causal inference
""")

# Generate multiple ideas (conceptual - depends on denario API)
den.get_idea()

# Review the generated idea in idea.md
# Decide whether to proceed or regenerate
```

## Writing a Paper from Existing Results

Use denario for paper generation when analysis is already complete.

### Example: Formatting Existing Research

```python
den = Denario(project_dir="./paper_generation")

# Provide all components manually
den.set_data_description("""
Completed analysis of traffic pattern data from urban sensors
Dataset: 6 months of traffic flow measurements from 100 intersections
Analysis completed using R and Python
""")

den.set_idea("""
Research question: Optimize traffic light timing using reinforcement learning
to reduce congestion and improve traffic flow efficiency
""")

den.set_method("""
# Methodology

## Data Collection
Traffic flow data collected from 100 intersections in downtown area from
January-June 2023. Measurements include vehicle counts, wait times, and
queue lengths at 1-minute intervals.

## Model Development
Developed a Deep Q-Network (DQN) reinforcement learning agent to optimize
traffic light timing. State space includes current queue lengths and
historical flow patterns. Actions correspond to light timing adjustments.

## Training
Trained the agent using historical data with a reward function based on
total wait time reduction. Used experience replay and target networks for
stable learning.

## Validation
Validated using held-out test data and compared against:
- Current fixed-timing system
- Actuated control system
- Alternative RL algorithms (A3C, PPO)

## Metrics
- Average wait time reduction
- Total throughput improvement
- Queue length distribution
- Computational efficiency
""")

den.set_results("""
# Results

## Training Performance
The DQN agent converged after 500,000 training episodes. Training time: 12 hours
on NVIDIA V100 GPU.

## Wait Time Reduction
- Current system: Average wait time 45.2 seconds
- DQN system: Average wait time 32.8 seconds
- Improvement: 27.4% reduction (p < 0.001)

## Throughput Analysis
- Vehicles processed per hour increased from 2,850 to 3,420 (+20%)
- Peak hour congestion reduced by 35%

## Comparison with Baselines
- Actuated control: 38.1 seconds average wait (DQN still 14% better)
- A3C: 34.5 seconds (DQN slightly better, 5%)
- PPO: 33.2 seconds (DQN marginally better, 1%)

## Queue Length Analysis
Maximum queue length reduced from 42 vehicles to 28 vehicles during peak hours.

## Figures
- Figure 1: Training curve showing convergence
- Figure 2: Wait time distribution comparison
- Figure 3: Throughput over time of day
- Figure 4: Heatmap of queue lengths across intersections
""")

# Generate publication-ready paper
den.get_paper(journal=Journal.APS)
```

## Fast Mode with Gemini

Use Google's Gemini models for faster execution.

### Example: Rapid Prototyping

```python
# Configure for fast mode (conceptual - check denario documentation)
# This would involve setting appropriate LLM backend

den = Denario(project_dir="./fast_research")

# Same workflow, optimized for speed
den.set_data_description("""
Quick analysis needed: Monthly sales data (2 years)
Goal: Identify seasonal patterns and forecast next quarter
Tools: pandas, Prophet
""")

# Fast execution
den.get_idea()
den.get_method()
den.get_results()
den.get_paper()

# Trade-off: Faster execution, potentially less detailed analysis
```

## Hybrid Workflow: Custom Idea + Automated Method

Combine manual and automated approaches.

### Example: Directed Research

```python
den = Denario(project_dir="./hybrid_workflow")

# Describe data
den.set_data_description("""
Medical imaging dataset: 10,000 chest X-rays
Labels: Normal, pneumonia, COVID-19
Format: 224x224 grayscale PNG files
Tools: TensorFlow, Keras, scikit-learn, OpenCV
""")

# Provide specific research direction
den.set_idea("""
Develop a transfer learning approach using pre-trained ResNet50 for multi-class
classification of chest X-rays, with focus on interpretability using Grad-CAM
to identify diagnostic regions
""")

# Let denario develop the methodology
den.get_method()

# Review methodology, then execute
den.get_results()

# Generate paper
den.get_paper(journal=Journal.APS)
```

## Time-Series Analysis Example

Specialized example for temporal data.

### Example: Economic Forecasting

```python
den = Denario(project_dir="./time_series_analysis")

den.set_data_description("""
Dataset: Monthly unemployment rates (US, 1950-2023)
Additional features: GDP growth, inflation, interest rates
Format: Multivariate time-series DataFrame
Tools: statsmodels, Prophet, pmdarima, sklearn

Analysis goals:
- Model unemployment trends
- Forecast next 12 months
- Identify leading indicators
- Assess forecast uncertainty

Data characteristics:
- Seasonal patterns (annual cycles)
- Structural breaks (recessions)
- Autocorrelation present
- Non-stationary (unit root)
""")

den.get_idea()
# Might generate: "Develop a SARIMAX model incorporating economic indicators
# as exogenous variables to forecast unemployment with confidence intervals"

den.get_method()
den.get_results()
den.get_paper(journal=Journal.APS)
```

## Machine Learning Pipeline Example

Complete ML workflow with validation.

### Example: Predictive Modeling

```python
den = Denario(project_dir="./ml_pipeline")

den.set_data_description("""
Dataset: Customer churn prediction
- 50,000 customers, 30 features (demographics, usage patterns, service history)
- Binary target: churned (1) or retained (0)
- Imbalanced: 20% churn rate
- Features: Numerical and categorical mixed

Available tools:
- pandas for preprocessing
- sklearn for modeling (RF, XGBoost, logistic regression)
- imblearn for handling imbalance
- SHAP for feature importance

Goals:
- Build predictive model for churn
- Identify key churn factors
- Provide actionable insights
- Achieve >85% AUC-ROC
""")

den.get_idea()
# Might generate: "Develop an ensemble model combining XGBoost and Random Forest
# with SMOTE oversampling, and use SHAP values to identify interpretable
# churn risk factors"

den.get_method()
# Will include: train/test split, cross-validation, hyperparameter tuning,
# performance metrics, feature importance analysis

den.get_results()
# Executes full ML pipeline, generates:
# - Model performance metrics
# - ROC curves
# - Feature importance plots
# - Confusion matrices

den.get_paper(journal=Journal.APS)
```

## Tips for Effective Usage

### Provide Rich Context

More context → better ideas and methodologies:

```python
# Include:
# - Data characteristics (size, format, quality issues)
# - Available tools and libraries
# - Domain-specific knowledge
# - Research objectives and constraints
# - Known challenges or considerations
```

### Iterate on Intermediate Outputs

Review and refine at each stage:

```python
# Generate
den.get_idea()

# Review idea.md
# If needed, refine:
den.set_idea("Refined version of the idea")

# Continue
den.get_method()
# Review methodology.md
# Refine if needed, then proceed
```

### Save Your Workflow

Document the complete pipeline:

```python
# Save workflow script
with open("research_workflow.py", "w") as f:
    f.write("""
from denario import Denario, Journal

den = Denario(project_dir="./project")
den.set_data_description("...")
den.get_idea()
den.get_method()
den.get_results()
den.get_paper(journal=Journal.APS)
""")
```

### Use Version Control

Track research evolution:

```bash
cd project_dir
git init
git add .
git commit -m "Initial data description"

# After each stage
git add .
git commit -m "Generated research idea"
# ... continue committing after each stage
```

---

## Reference: Installation

# Installation Guide

## System Requirements

- **Python**: Version 3.12 or higher (required)
- **Operating System**: Linux, macOS, or Windows
- **Virtual Environment**: Recommended for isolation
- **LaTeX**: Required for paper generation (or use Docker)

## Installation Methods

### Method 1: Using uv (Recommended)

The uv package manager provides fast, reliable dependency resolution:

```bash
# Initialize a new project
uv init

# Add denario with app support
uv add "denario[app]"
```

### Method 2: Alternative Installation

Alternative installation using pip:

```bash
# Create virtual environment (recommended)
python3 -m venv denario_env
source denario_env/bin/activate  # On Windows: denario_env\Scripts\activate

# Install denario
uv pip install "denario[app]"
```

### Method 3: Building from Source

For development or customization:

```bash
# Clone the repository
git clone https://github.com/AstroPilot-AI/Denario.git
cd Denario

# Create virtual environment
python3 -m venv Denario_env
source Denario_env/bin/activate

# Install in editable mode
uv pip install -e .
```

### Method 4: Docker Deployment

Docker provides a complete environment with all dependencies including LaTeX:

```bash
# Pull the official image
docker pull pablovd/denario:latest

# Run the container with GUI
docker run -p 8501:8501 --rm pablovd/denario:latest

# Run with environment variables (for API keys)
docker run -p 8501:8501 --env-file .env --rm pablovd/denario:latest
```

Access the GUI at `http://localhost:8501` after the container starts.

## Verifying Installation

After installation, verify denario is available:

```python
# Test import
python -c "from denario import Denario; print('Denario installed successfully')"
```

Or check the version:

```bash
python -c "import denario; print(denario.__version__)"
```

## Launching the Application

### Command-Line Interface

Run the graphical user interface:

```bash
denario run
```

This launches a web-based Streamlit application for interactive research workflow management.

### Programmatic Usage

Use denario directly in Python scripts:

```python
from denario import Denario

den = Denario(project_dir="./my_project")
# Continue with workflow...
```

## Dependencies

Denario automatically installs key dependencies:

- **AG2**: Agent orchestration framework
- **LangGraph**: Graph-based agent workflows
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning tools
- **matplotlib/seaborn**: Visualization
- **streamlit**: GUI framework (with `[app]` extra)

## LaTeX Setup

For paper generation, LaTeX must be available:

### Linux
```bash
sudo apt-get install texlive-full
```

### macOS
```bash
brew install --cask mactex
```

### Windows
Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/).

### Docker Alternative
The Docker image includes a complete LaTeX installation, eliminating manual setup.

## Troubleshooting Installation

### Python Version Issues

Ensure Python 3.12+:
```bash
python --version
```

If older, install a newer version or use pyenv for version management.

### Virtual Environment Activation

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Permission Errors

Use `--user` flag or virtual environments:
```bash
uv pip install --user "denario[app]"
```

### Docker Port Conflicts

If port 8501 is in use, map to a different port:
```bash
docker run -p 8502:8501 --rm pablovd/denario:latest
```

### Package Conflicts

Create a fresh virtual environment to avoid dependency conflicts.

## Updating Denario

### uv
```bash
uv add --upgrade denario
```

### pip
```bash
uv pip install --upgrade "denario[app]"
```

### Docker
```bash
docker pull pablovd/denario:latest
```

## Uninstallation

### uv
```bash
uv remove denario
```

### pip
```bash
uv pip uninstall denario
```

### Docker
```bash
docker rmi pablovd/denario:latest
```

---

## Reference: Llm_Configuration

# LLM API Configuration

## Overview

Denario requires API credentials from supported LLM providers to power its multiagent research system. The system is built on AG2 and LangGraph, which support multiple LLM backends.

## Supported LLM Providers

### Google Vertex AI
- Full integration with Google's Vertex AI platform
- Supports Gemini and PaLM models
- Requires Google Cloud project setup

### OpenAI
- GPT-4, GPT-3.5, and other OpenAI models
- Direct API integration

### Other Providers
- Any LLM compatible with AG2/LangGraph frameworks
- Anthropic Claude (via compatible interfaces)
- Azure OpenAI
- Custom model endpoints

## Obtaining API Keys

### Google Vertex AI

1. **Create Google Cloud Project**
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing

2. **Enable Vertex AI API**
   - Go to "APIs & Services" → "Library"
   - Search for "Vertex AI API"
   - Click "Enable"

3. **Create Service Account**
   - Navigate to "IAM & Admin" → "Service Accounts"
   - Create service account with Vertex AI permissions
   - Download JSON key file

4. **Set up authentication**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

### OpenAI

1. **Create OpenAI Account**
   - Visit [platform.openai.com](https://platform.openai.com/)
   - Sign up or log in

2. **Generate API Key**
   - Navigate to API Keys section
   - Click "Create new secret key"
   - Copy and store securely

3. **Set environment variable**
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Storing API Keys

### Method 1: Environment Variables (Recommended)

**Linux/macOS:**
```bash
export OPENAI_API_KEY="your-key-here"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile` for persistence.

**Windows:**
```bash
set OPENAI_API_KEY=your-key-here
```

Or use System Properties → Environment Variables for persistence.

### Method 2: .env Files

Create a `.env` file in your project directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4

# Google Vertex AI Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id

# Optional: Model preferences
DEFAULT_MODEL=gpt-4
TEMPERATURE=0.7
```

Load the environment file in Python:

```python
from dotenv import load_dotenv
load_dotenv()

from denario import Denario
den = Denario(project_dir="./project")
```

### Method 3: Docker Environment Files

For Docker deployments, pass environment variables:

```bash
# Using --env-file flag
docker run -p 8501:8501 --env-file .env --rm pablovd/denario:latest

# Using -e flag for individual variables
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
  -v /local/path/to/creds.json:/credentials.json \
  --rm pablovd/denario:latest
```

## Vertex AI Detailed Setup

### Prerequisites
- Google Cloud account with billing enabled
- gcloud CLI installed (optional but recommended)

### Step-by-Step Configuration

1. **Install Google Cloud SDK (if not using Docker)**
   ```bash
   # Linux/macOS
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Authenticate gcloud**
   ```bash
   gcloud auth application-default login
   ```

3. **Set project**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Enable required APIs**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable compute.googleapis.com
   ```

5. **Create service account (alternative to gcloud auth)**
   ```bash
   gcloud iam service-accounts create denario-service-account \
     --display-name="Denario AI Service Account"

   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:denario-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"

   gcloud iam service-accounts keys create credentials.json \
     --iam-account=denario-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

6. **Configure denario to use Vertex AI**
   ```python
   import os
   os.environ['GOOGLE_CLOUD_PROJECT'] = 'YOUR_PROJECT_ID'
   os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credentials.json'

   from denario import Denario
   den = Denario(project_dir="./research")
   ```

## Model Selection

Configure which models denario uses for different tasks:

```python
# In your code
from denario import Denario

# Example configuration (if supported by denario API)
den = Denario(
    project_dir="./project",
    # Model configuration may vary based on denario version
)
```

Check denario's documentation for specific model selection APIs.

## Cost Management

### Monitoring Costs

- **OpenAI**: Track usage at [platform.openai.com/usage](https://platform.openai.com/usage)
- **Google Cloud**: Monitor in Cloud Console → Billing
- Set up billing alerts to avoid unexpected charges

### Cost Optimization Tips

1. **Use appropriate model tiers**
   - GPT-3.5 for simpler tasks
   - GPT-4 for complex reasoning

2. **Batch operations**
   - Process multiple research tasks in single sessions

3. **Cache results**
   - Reuse generated ideas, methods, and results when possible

4. **Set token limits**
   - Configure maximum token usage for cost control

## Security Best Practices

### Do NOT commit API keys to version control

Add to `.gitignore`:
```gitignore
.env
*.json  # If storing credentials
credentials.json
service-account-key.json
```

### Rotate keys regularly
- Generate new API keys periodically
- Revoke old keys after rotation

### Use least privilege access
- Grant only necessary permissions to service accounts
- Use separate keys for development and production

### Encrypt sensitive files
- Store credential files in encrypted volumes
- Use cloud secret management services for production

## Troubleshooting

### "API key not found" errors
- Verify environment variables are set: `echo $OPENAI_API_KEY`
- Check `.env` file is in correct directory
- Ensure `load_dotenv()` is called before importing denario

### Vertex AI authentication failures
- Verify `GOOGLE_APPLICATION_CREDENTIALS` points to valid JSON file
- Check service account has required permissions
- Ensure APIs are enabled in Google Cloud project

### Rate limiting issues
- Implement exponential backoff
- Reduce concurrent requests
- Upgrade API plan if needed

### Docker environment variable issues
- Use `docker run --env-file .env` to pass environment
- Mount credential files with `-v` flag
- Check environment inside container: `docker exec <container> env`

---

## Reference: Research_Pipeline

# Research Pipeline API Reference

## Core Classes

### Denario

The main class for orchestrating research workflows.

#### Initialization

```python
from denario import Denario

den = Denario(project_dir="path/to/project")
```

**Parameters:**
- `project_dir` (str): Path to the research project directory where all outputs will be stored

#### Methods

##### set_data_description()

Define the research context by describing available data and analytical tools.

```python
den.set_data_description(description: str)
```

**Parameters:**
- `description` (str): Text describing the dataset, available tools, research domain, and any relevant context

**Example:**
```python
den.set_data_description("""
Available data: Time-series temperature measurements from 2010-2023
Tools: pandas, scipy, sklearn, matplotlib
Domain: Climate science
Research interest: Identifying seasonal patterns and long-term trends
""")
```

**Purpose:** This establishes the foundation for automated idea generation by providing context about what data is available and what analyses are feasible.

##### get_idea()

Generate research hypotheses based on the data description.

```python
den.get_idea()
```

**Returns:** Research idea/hypothesis (stored internally in project directory)

**Output:** Creates a file containing the generated research question or hypothesis

**Example:**
```python
den.get_idea()
# Generates ideas like: "Investigate the correlation between seasonal temperature
# variations and long-term warming trends using time-series decomposition"
```

##### set_idea()

Manually specify a research idea instead of generating one.

```python
den.set_idea(idea: str)
```

**Parameters:**
- `idea` (str): The research hypothesis or question to investigate

**Example:**
```python
den.set_idea("Analyze the impact of El Niño events on regional temperature anomalies")
```

**Use case:** When you have a specific research direction and want to skip automated idea generation.

##### get_method()

Develop a research methodology based on the idea and data description.

```python
den.get_method()
```

**Returns:** Methodology document (stored internally in project directory)

**Output:** Creates a structured methodology including:
- Analytical approach
- Statistical methods to apply
- Validation strategies
- Expected outputs

**Example:**
```python
den.get_method()
# Generates methodology: "Apply seasonal decomposition, compute correlation coefficients,
# perform statistical significance tests, generate visualization plots..."
```

##### set_method()

Provide a custom methodology instead of generating one.

```python
den.set_method(method: str)
den.set_method(method: Path)  # Can also accept file paths
```

**Parameters:**
- `method` (str or Path): Methodology description or path to markdown file containing methodology

**Example:**
```python
# From string
den.set_method("""
1. Apply seasonal decomposition using STL
2. Compute Pearson correlation coefficients
3. Perform Mann-Kendall trend test
4. Generate time-series plots with confidence intervals
""")

# From file
den.set_method("methodology.md")
```

##### get_results()

Execute the methodology, perform computations, and generate results.

```python
den.get_results()
```

**Returns:** Results document with analysis outputs (stored internally in project directory)

**Output:** Creates results including:
- Computed statistics
- Generated figures and visualizations
- Data tables
- Analysis findings

**Example:**
```python
den.get_results()
# Executes the methodology, runs analyses, creates plots, compiles findings
```

**Note:** This is where the actual computational work happens. The agent executes code to perform the analyses specified in the methodology.

##### set_results()

Provide pre-computed results instead of generating them.

```python
den.set_results(results: str)
den.set_results(results: Path)  # Can also accept file paths
```

**Parameters:**
- `results` (str or Path): Results description or path to markdown file containing results

**Example:**
```python
# From string
den.set_results("""
Analysis Results:
- Correlation coefficient: 0.78 (p < 0.001)
- Seasonal amplitude: 5.2°C
- Long-term trend: +0.15°C per decade
- Figure 1: Seasonal decomposition (see attached)
""")

# From file
den.set_results("results.md")
```

**Use case:** When analyses were performed externally or when iterating on paper writing without re-running computations.

##### get_paper()

Generate a publication-ready LaTeX paper with the research findings.

```python
den.get_paper(journal: Journal = None)
```

**Parameters:**
- `journal` (Journal, optional): Target journal for formatting. Defaults to generic format.

**Returns:** LaTeX paper with proper formatting (stored in project directory)

**Output:** Creates:
- Complete LaTeX source file
- Compiled PDF (if LaTeX is available)
- Integrated figures and tables
- Properly formatted bibliography

**Example:**
```python
from denario import Journal

den.get_paper(journal=Journal.APS)
# Generates paper.tex and paper.pdf formatted for APS journals
```

### Journal Enum

Enumeration of supported journal formats.

```python
from denario import Journal
```

#### Available Journals

- `Journal.APS` - American Physical Society format
  - Suitable for Physical Review, Physical Review Letters, etc.
  - Uses RevTeX document class

Additional journal formats may be available. Check the latest denario documentation for the complete list.

#### Usage

```python
from denario import Denario, Journal

den = Denario(project_dir="./research")
# ... complete workflow ...
den.get_paper(journal=Journal.APS)
```

## Workflow Patterns

### Fully Automated Pipeline

Let denario handle every stage:

```python
from denario import Denario, Journal

den = Denario(project_dir="./automated_research")

# Define context
den.set_data_description("""
Dataset: Sensor readings from IoT devices
Tools: pandas, numpy, sklearn, matplotlib
Goal: Anomaly detection in sensor networks
""")

# Automate entire pipeline
den.get_idea()        # Generate research idea
den.get_method()      # Develop methodology
den.get_results()     # Execute analysis
den.get_paper(journal=Journal.APS)  # Create paper
```

### Custom Idea, Automated Execution

Provide your research question, automate the rest:

```python
den = Denario(project_dir="./custom_idea")

den.set_data_description("Dataset: Financial time-series data...")

# Manual idea
den.set_idea("Investigate predictive models for stock market volatility using LSTM networks")

# Automated execution
den.get_method()
den.get_results()
den.get_paper(journal=Journal.APS)
```

### Fully Manual with Template Generation

Use denario only for paper formatting:

```python
den = Denario(project_dir="./manual_research")

# Provide everything manually
den.set_data_description("Pre-existing dataset description...")
den.set_idea("Pre-defined research hypothesis")
den.set_method("methodology.md")  # Load from file
den.set_results("results.md")      # Load from file

# Generate formatted paper
den.get_paper(journal=Journal.APS)
```

### Iterative Refinement

Refine specific stages without re-running everything:

```python
den = Denario(project_dir="./iterative")

# Initial run
den.set_data_description("Dataset description...")
den.get_idea()
den.get_method()
den.get_results()

# Refine methodology after reviewing results
den.set_method("""
Revised methodology:
- Use different statistical test
- Add sensitivity analysis
- Include cross-validation
""")

# Re-run only downstream stages
den.get_results()  # Re-execute with new method
den.get_paper(journal=Journal.APS)
```

## Project Directory Structure

After running a complete workflow, the project directory contains:

```
project_dir/
├── data_description.txt    # Input: data context
├── idea.md                 # Generated or provided research idea
├── methodology.md          # Generated or provided methodology
├── results.md              # Generated or provided results
├── figures/                # Generated visualizations
│   ├── figure_1.png
│   ├── figure_2.png
│   └── ...
├── paper.tex               # Generated LaTeX source
├── paper.pdf               # Compiled PDF (if LaTeX available)
└── logs/                   # Agent execution logs
    └── ...
```

## Advanced Features

### Multiagent Orchestration

Denario uses AG2 and LangGraph frameworks to coordinate multiple specialized agents:

- **Idea Agent**: Generates research hypotheses from data descriptions
- **Method Agent**: Develops analytical methodologies
- **Execution Agent**: Runs computations and creates visualizations
- **Writing Agent**: Produces publication-ready manuscripts

These agents collaborate automatically, with each stage building on previous outputs.

### Integration with Scientific Tools

Denario integrates with common scientific Python libraries:

- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **scipy**: Scientific computing and statistics
- **matplotlib/seaborn**: Visualization
- **numpy**: Numerical operations

When generating results, denario can automatically write and execute code using these libraries.

### Reproducibility

All stages produce structured outputs saved to the project directory:

- Version control friendly (markdown and LaTeX)
- Auditable (logs of agent decisions and code execution)
- Reproducible (saved methodologies can be re-run)

### Literature Search

Denario includes capabilities for literature searches to provide context for research ideas and methodology development. See `examples.md` for literature search workflows.

## Error Handling

### Common Issues

**Missing data description:**
```python
den = Denario(project_dir="./project")
den.get_idea()  # Error: must call set_data_description() first
```

**Solution:** Always set data description before generating ideas.

**Missing prerequisite stages:**
```python
den = Denario(project_dir="./project")
den.get_results()  # Error: must have idea and method first
```

**Solution:** Follow the workflow order or manually set prerequisite stages.

**LaTeX compilation errors:**
```python
den.get_paper()  # May fail if LaTeX not installed
```

**Solution:** Install LaTeX distribution or use Docker image with pre-installed LaTeX.

## Best Practices

### Data Description Quality

Provide detailed context for better idea generation:

```python
# Good: Detailed and specific
den.set_data_description("""
Dataset: 10 years of daily temperature readings from 50 weather stations
Format: CSV with columns [date, station_id, temperature, humidity]
Tools available: pandas, scipy, sklearn, matplotlib, seaborn
Domain: Climatology
Research interests: Climate change, seasonal patterns, regional variations
Known challenges: Missing data in 2015, station 23 has calibration issues
""")

# Bad: Too vague
den.set_data_description("Temperature data from weather stations")
```

### Methodology Validation

Review generated methodologies before executing:

```python
den.get_method()
# Review the methodology.md file in project_dir
# If needed, refine with set_method()
```

### Incremental Development

Build the research pipeline incrementally:

```python
# Stage 1: Validate idea generation
den.set_data_description("...")
den.get_idea()
# Review idea.md, adjust if needed

# Stage 2: Validate methodology
den.get_method()
# Review methodology.md, adjust if needed

# Stage 3: Execute and validate results
den.get_results()
# Review results.md and figures/

# Stage 4: Generate paper
den.get_paper(journal=Journal.APS)
```

### Version Control Integration

Initialize git in project directory for tracking:

```bash
cd project_dir
git init
git add .
git commit -m "Initial research workflow"
```

Commit after each stage to track the evolution of your research.
