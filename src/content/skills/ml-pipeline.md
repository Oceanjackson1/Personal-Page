---
title: "机器学习管道"
description: "构建端到端机器学习管道，数据处理、模型训练和部署"
category: "devops"
source: "community"
author: "Community"
tags: ["ml", "pipeline"]
date: 2026-03-20
---

# ML Pipeline Expert

Senior ML pipeline engineer specializing in production-grade machine learning infrastructure, orchestration systems, and automated training workflows.

## Core Workflow

1. **Design pipeline architecture** — Map data flow, identify stages, define interfaces between components
2. **Validate data schema** — Run schema checks and distribution validation before any training begins; halt and report on failures
3. **Implement feature engineering** — Build transformation pipelines, feature stores, and validation checks
4. **Orchestrate training** — Configure distributed training, hyperparameter tuning, and resource allocation
5. **Track experiments** — Log metrics, parameters, and artifacts; enable comparison and reproducibility
6. **Validate and deploy** — Run model evaluation gates; implement A/B testing or shadow deployment before promotion

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Feature Engineering | `references/feature-engineering.md` | Feature pipelines, transformations, feature stores, Feast, data validation |
| Training Pipelines | `references/training-pipelines.md` | Training orchestration, distributed training, hyperparameter tuning, resource management |
| Experiment Tracking | `references/experiment-tracking.md` | MLflow, Weights & Biases, experiment logging, model registry |
| Pipeline Orchestration | `references/pipeline-orchestration.md` | Kubeflow Pipelines, Airflow, Prefect, DAG design, workflow automation |
| Model Validation | `references/model-validation.md` | Evaluation strategies, validation workflows, A/B testing, shadow deployment |

## Code Templates

### MLflow Experiment Logging (minimal reproducible example)

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

# Pin random state for reproducibility
SEED = 42
np.random.seed(SEED)

mlflow.set_experiment("my-classifier-experiment")

with mlflow.start_run():
    # Log all hyperparameters — never hardcode silently
    params = {"n_estimators": 100, "max_depth": 5, "random_state": SEED}
    mlflow.log_params(params)

    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Log metrics
    mlflow.log_metric("accuracy", accuracy_score(y_test, preds))
    mlflow.log_metric("f1", f1_score(y_test, preds, average="weighted"))

    # Log and register the model artifact
    mlflow.sklearn.log_model(model, artifact_path="model",
                             registered_model_name="my-classifier")
```

### Kubeflow Pipeline Component (single-step template)

```python
from kfp.v2 import dsl
from kfp.v2.dsl import component, Input, Output, Dataset, Model, Metrics

@component(base_image="python:3.10", packages_to_install=["scikit-learn", "mlflow"])
def train_model(
    train_data: Input[Dataset],
    model_output: Output[Model],
    metrics_output: Output[Metrics],
    n_estimators: int = 100,
    max_depth: int = 5,
):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import pickle, json

    df = pd.read_csv(train_data.path)
    X, y = df.drop("label", axis=1), df["label"]

    model = RandomForestClassifier(n_estimators=n_estimators,
                                   max_depth=max_depth, random_state=42)
    model.fit(X, y)

    with open(model_output.path, "wb") as f:
        pickle.dump(model, f)

    metrics_output.log_metric("train_samples", len(df))


@dsl.pipeline(name="training-pipeline")
def training_pipeline(data_path: str, n_estimators: int = 100):
    train_step = train_model(n_estimators=n_estimators)
    # Chain additional steps (validate, register, deploy) here
```

### Data Validation Checkpoint (Great Expectations style)

```python
import great_expectations as ge

def validate_training_data(df):
    """Run schema and distribution checks. Raise on failure — never skip."""
    gdf = ge.from_pandas(df)
    results = gdf.expect_column_values_to_not_be_null("label")
    results &= gdf.expect_column_values_to_be_between("feature_1", 0, 1)

    if not results["success"]:
        raise ValueError(f"Data validation failed: {results['result']}")
    return df  # safe to proceed to training
```

## Constraints

**Always:**
- Version all data, code, and models explicitly (DVC, Git tags, model registry)
- Pin dependencies and random seeds for reproducible training environments
- Log all hyperparameters, metrics, and artifacts to experiment tracking
- Validate data schema and distribution before training begins
- Use containerized environments; store credentials in secrets managers, never in code
- Implement error handling, retry logic, and pipeline alerting
- Separate training and inference code clearly

**Never:**
- Run training without experiment tracking or without logging hyperparameters
- Deploy a model without recorded validation metrics
- Use non-reproducible random states or skip data validation
- Ignore pipeline failures silently or mix credentials into pipeline code

## Output Format

When implementing a pipeline, provide:
1. Complete pipeline definition (Kubeflow DAG, Airflow DAG, or equivalent) — use the templates above as starting structure
2. Feature engineering code with inline data validation calls
3. Training script with MLflow (or equivalent) experiment logging
4. Model evaluation code with explicit pass/fail thresholds
5. Deployment configuration and rollback strategy
6. Brief explanation of architecture decisions and reproducibility measures

## Knowledge Reference

MLflow, Kubeflow Pipelines, Apache Airflow, Prefect, Feast, Weights & Biases, Neptune, DVC, Great Expectations, Ray, Horovod, Kubernetes, Docker, S3/GCS/Azure Blob, model registry patterns, feature store architecture, distributed training, hyperparameter optimization

---

## Reference: Experiment Tracking

# Experiment Tracking

---

## Overview

Experiment tracking enables reproducibility, comparison, and collaboration in ML development. It captures hyperparameters, metrics, artifacts, and model versions to ensure every experiment can be reproduced and compared.

## When to Use This Reference

- Setting up MLflow for experiment tracking
- Implementing Weights & Biases integration
- Creating model registries and versioning
- Comparing experiments and selecting models
- Building custom tracking solutions

## When NOT to Use

- Quick one-off experiments without reproducibility needs
- Simple scripts without hyperparameters
- Non-ML projects

---

## MLflow Integration

### Basic Experiment Tracking

```python
import mlflow
from mlflow.tracking import MlflowClient
from pathlib import Path
import json

class MLflowTracker:
    """MLflow experiment tracking wrapper."""

    def __init__(
        self,
        experiment_name: str,
        tracking_uri: str = "http://localhost:5000",
        artifact_location: str = None,
    ):
        mlflow.set_tracking_uri(tracking_uri)

        # Create or get experiment
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            self.experiment_id = mlflow.create_experiment(
                experiment_name,
                artifact_location=artifact_location,
            )
        else:
            self.experiment_id = experiment.experiment_id

        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()
        self.run = None

    def start_run(
        self,
        run_name: str = None,
        tags: dict = None,
        nested: bool = False,
    ) -> str:
        """Start a new MLflow run."""
        self.run = mlflow.start_run(
            run_name=run_name,
            experiment_id=self.experiment_id,
            nested=nested,
        )

        if tags:
            mlflow.set_tags(tags)

        return self.run.info.run_id

    def end_run(self, status: str = "FINISHED") -> None:
        """End the current run."""
        mlflow.end_run(status=status)
        self.run = None

    def log_params(self, params: dict) -> None:
        """Log hyperparameters."""
        mlflow.log_params(params)

    def log_metrics(self, metrics: dict, step: int = None) -> None:
        """Log metrics with optional step."""
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)

    def log_artifact(self, local_path: str, artifact_path: str = None) -> None:
        """Log file or directory as artifact."""
        mlflow.log_artifact(local_path, artifact_path)

    def log_model(
        self,
        model,
        artifact_path: str,
        registered_model_name: str = None,
        signature=None,
        input_example=None,
    ) -> str:
        """Log model with optional registration."""
        from mlflow.models import infer_signature

        if signature is None and input_example is not None:
            signature = infer_signature(input_example, model.predict(input_example))

        model_info = mlflow.sklearn.log_model(
            model,
            artifact_path=artifact_path,
            registered_model_name=registered_model_name,
            signature=signature,
            input_example=input_example,
        )

        return model_info.model_uri

# Usage example
def train_with_mlflow(
    model,
    X_train,
    y_train,
    X_val,
    y_val,
    params: dict,
):
    """Complete training run with MLflow tracking."""
    tracker = MLflowTracker("my_experiment")

    tracker.start_run(
        run_name=f"run_{params['model_type']}",
        tags={
            "model_type": params["model_type"],
            "dataset_version": "v1.0",
            "author": "ml-team",
        },
    )

    try:
        # Log parameters
        tracker.log_params(params)

        # Train model
        model.fit(X_train, y_train)

        # Evaluate and log metrics
        train_score = model.score(X_train, y_train)
        val_score = model.score(X_val, y_val)

        tracker.log_metrics({
            "train_accuracy": train_score,
            "val_accuracy": val_score,
        })

        # Log model
        model_uri = tracker.log_model(
            model,
            artifact_path="model",
            registered_model_name="my_model",
            input_example=X_train[:5],
        )

        tracker.end_run()
        return model_uri

    except Exception as e:
        tracker.end_run(status="FAILED")
        raise
```

### PyTorch Model Logging

```python
import mlflow.pytorch
import torch

def log_pytorch_model(
    model: torch.nn.Module,
    artifact_path: str,
    registered_model_name: str = None,
    sample_input: torch.Tensor = None,
) -> str:
    """Log PyTorch model with signature inference."""
    from mlflow.models import infer_signature

    # Create signature from sample input
    signature = None
    if sample_input is not None:
        model.eval()
        with torch.no_grad():
            sample_output = model(sample_input)

        signature = infer_signature(
            sample_input.numpy(),
            sample_output.numpy(),
        )

    model_info = mlflow.pytorch.log_model(
        model,
        artifact_path=artifact_path,
        registered_model_name=registered_model_name,
        signature=signature,
    )

    return model_info.model_uri

def load_pytorch_model(model_uri: str, device: str = "cpu") -> torch.nn.Module:
    """Load PyTorch model from MLflow."""
    model = mlflow.pytorch.load_model(model_uri, map_location=device)
    return model
```

### Model Registry Operations

```python
from mlflow.tracking import MlflowClient
from mlflow.entities.model_registry import ModelVersion

class ModelRegistry:
    """MLflow Model Registry wrapper."""

    def __init__(self, tracking_uri: str = "http://localhost:5000"):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()

    def register_model(
        self,
        model_uri: str,
        name: str,
        tags: dict = None,
        description: str = None,
    ) -> ModelVersion:
        """Register a new model version."""
        result = mlflow.register_model(model_uri, name)

        if tags:
            for key, value in tags.items():
                self.client.set_model_version_tag(name, result.version, key, value)

        if description:
            self.client.update_model_version(
                name,
                result.version,
                description=description,
            )

        return result

    def transition_model_stage(
        self,
        name: str,
        version: str,
        stage: str,
        archive_existing: bool = True,
    ) -> ModelVersion:
        """Transition model to new stage (Staging, Production, Archived)."""
        return self.client.transition_model_version_stage(
            name=name,
            version=version,
            stage=stage,
            archive_existing_versions=archive_existing,
        )

    def get_latest_version(
        self,
        name: str,
        stages: list[str] = None,
    ) -> list[ModelVersion]:
        """Get latest model versions by stage."""
        return self.client.get_latest_versions(name, stages=stages)

    def load_production_model(self, name: str) -> any:
        """Load the production model."""
        model_uri = f"models:/{name}/Production"
        return mlflow.pyfunc.load_model(model_uri)

    def compare_versions(
        self,
        name: str,
        version_a: str,
        version_b: str,
    ) -> dict:
        """Compare two model versions."""
        v_a = self.client.get_model_version(name, version_a)
        v_b = self.client.get_model_version(name, version_b)

        run_a = self.client.get_run(v_a.run_id)
        run_b = self.client.get_run(v_b.run_id)

        return {
            "version_a": {
                "version": version_a,
                "metrics": run_a.data.metrics,
                "params": run_a.data.params,
            },
            "version_b": {
                "version": version_b,
                "metrics": run_b.data.metrics,
                "params": run_b.data.params,
            },
        }
```

---

## Weights & Biases Integration

### Basic W&B Tracking

```python
import wandb
from pathlib import Path

class WandbTracker:
    """Weights & Biases experiment tracking wrapper."""

    def __init__(
        self,
        project: str,
        entity: str = None,
        config: dict = None,
    ):
        self.project = project
        self.entity = entity
        self.config = config
        self.run = None

    def start_run(
        self,
        name: str = None,
        tags: list[str] = None,
        group: str = None,
        job_type: str = "train",
        resume: str = None,
    ) -> wandb.Run:
        """Initialize W&B run."""
        self.run = wandb.init(
            project=self.project,
            entity=self.entity,
            name=name,
            config=self.config,
            tags=tags,
            group=group,
            job_type=job_type,
            resume=resume,
        )
        return self.run

    def log(self, data: dict, step: int = None, commit: bool = True) -> None:
        """Log metrics and data."""
        wandb.log(data, step=step, commit=commit)

    def log_artifact(
        self,
        name: str,
        artifact_type: str,
        path: str,
        metadata: dict = None,
    ) -> wandb.Artifact:
        """Log artifact (model, dataset, etc.)."""
        artifact = wandb.Artifact(
            name=name,
            type=artifact_type,
            metadata=metadata,
        )

        if Path(path).is_dir():
            artifact.add_dir(path)
        else:
            artifact.add_file(path)

        self.run.log_artifact(artifact)
        return artifact

    def log_model(
        self,
        model_path: str,
        name: str,
        metadata: dict = None,
        aliases: list[str] = None,
    ) -> wandb.Artifact:
        """Log model artifact with aliases."""
        artifact = wandb.Artifact(
            name=name,
            type="model",
            metadata=metadata,
        )

        if Path(model_path).is_dir():
            artifact.add_dir(model_path)
        else:
            artifact.add_file(model_path)

        self.run.log_artifact(artifact, aliases=aliases or ["latest"])
        return artifact

    def watch_model(
        self,
        model,
        log: str = "all",
        log_freq: int = 100,
    ) -> None:
        """Watch model for gradient and parameter logging."""
        wandb.watch(model, log=log, log_freq=log_freq)

    def finish(self, exit_code: int = 0) -> None:
        """Finish the run."""
        wandb.finish(exit_code=exit_code)

# Usage with PyTorch
def train_with_wandb(
    model: torch.nn.Module,
    train_loader,
    val_loader,
    config: dict,
):
    """Training with W&B tracking."""
    tracker = WandbTracker(
        project="my-project",
        config=config,
    )

    tracker.start_run(
        name=f"experiment_{config['model_type']}",
        tags=["baseline", config["model_type"]],
        group="hyperparameter_search",
    )

    # Watch model gradients
    tracker.watch_model(model)

    for epoch in range(config["epochs"]):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            # Training step
            loss = train_step(model, data, target)

            tracker.log({
                "train/loss": loss,
                "train/epoch": epoch,
            })

        # Validation
        val_metrics = evaluate(model, val_loader)
        tracker.log({
            "val/loss": val_metrics["loss"],
            "val/accuracy": val_metrics["accuracy"],
            "epoch": epoch,
        })

    # Save and log model
    torch.save(model.state_dict(), "model.pt")
    tracker.log_model(
        "model.pt",
        name="trained_model",
        metadata={"accuracy": val_metrics["accuracy"]},
        aliases=["latest", "best"],
    )

    tracker.finish()
```

### W&B Sweeps for Hyperparameter Tuning

```python
import wandb

sweep_config = {
    "method": "bayes",  # bayes, grid, random
    "metric": {
        "name": "val/loss",
        "goal": "minimize",
    },
    "parameters": {
        "learning_rate": {
            "distribution": "log_uniform_values",
            "min": 1e-5,
            "max": 1e-2,
        },
        "batch_size": {
            "values": [16, 32, 64, 128],
        },
        "hidden_size": {
            "values": [128, 256, 512],
        },
        "dropout": {
            "distribution": "uniform",
            "min": 0.1,
            "max": 0.5,
        },
    },
    "early_terminate": {
        "type": "hyperband",
        "min_iter": 3,
    },
}

def sweep_train():
    """Training function for sweep."""
    with wandb.init() as run:
        config = wandb.config

        model = build_model(
            hidden_size=config.hidden_size,
            dropout=config.dropout,
        )

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=config.learning_rate,
        )

        train_loader = DataLoader(train_dataset, batch_size=config.batch_size)

        for epoch in range(10):
            loss = train_epoch(model, train_loader, optimizer)
            val_loss = evaluate(model, val_loader)

            wandb.log({
                "train/loss": loss,
                "val/loss": val_loss,
                "epoch": epoch,
            })

# Run sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")
wandb.agent(sweep_id, function=sweep_train, count=50)
```

---

## Custom Experiment Tracking

### Lightweight Tracker

```python
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import hashlib
import uuid

@dataclass
class Experiment:
    """Experiment metadata and results."""
    experiment_id: str
    name: str
    params: dict
    metrics: dict = field(default_factory=dict)
    artifacts: list = field(default_factory=list)
    tags: dict = field(default_factory=dict)
    start_time: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    end_time: Optional[str] = None
    status: str = "running"

    def to_dict(self) -> dict:
        return asdict(self)

class SimpleTracker:
    """Lightweight file-based experiment tracker."""

    def __init__(self, experiments_dir: str = "./experiments"):
        self.experiments_dir = Path(experiments_dir)
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        self.current_experiment: Optional[Experiment] = None

    def start_experiment(
        self,
        name: str,
        params: dict,
        tags: dict = None,
    ) -> Experiment:
        """Start a new experiment."""
        experiment_id = str(uuid.uuid4())[:8]

        self.current_experiment = Experiment(
            experiment_id=experiment_id,
            name=name,
            params=params,
            tags=tags or {},
        )

        # Create experiment directory
        exp_dir = self.experiments_dir / experiment_id
        exp_dir.mkdir(exist_ok=True)

        self._save_experiment()
        return self.current_experiment

    def log_metrics(self, metrics: dict, step: int = None) -> None:
        """Log metrics to current experiment."""
        if self.current_experiment is None:
            raise ValueError("No active experiment")

        for key, value in metrics.items():
            if key not in self.current_experiment.metrics:
                self.current_experiment.metrics[key] = []

            self.current_experiment.metrics[key].append({
                "value": value,
                "step": step,
                "timestamp": datetime.utcnow().isoformat(),
            })

        self._save_experiment()

    def log_artifact(self, path: str, name: str = None) -> str:
        """Copy artifact to experiment directory."""
        if self.current_experiment is None:
            raise ValueError("No active experiment")

        import shutil

        source = Path(path)
        artifact_name = name or source.name
        exp_dir = self.experiments_dir / self.current_experiment.experiment_id
        dest = exp_dir / "artifacts" / artifact_name

        dest.parent.mkdir(parents=True, exist_ok=True)

        if source.is_dir():
            shutil.copytree(source, dest)
        else:
            shutil.copy2(source, dest)

        self.current_experiment.artifacts.append(str(dest))
        self._save_experiment()

        return str(dest)

    def end_experiment(self, status: str = "completed") -> None:
        """End current experiment."""
        if self.current_experiment is None:
            return

        self.current_experiment.status = status
        self.current_experiment.end_time = datetime.utcnow().isoformat()
        self._save_experiment()
        self.current_experiment = None

    def _save_experiment(self) -> None:
        """Save experiment to JSON file."""
        if self.current_experiment is None:
            return

        exp_dir = self.experiments_dir / self.current_experiment.experiment_id
        with open(exp_dir / "experiment.json", "w") as f:
            json.dump(self.current_experiment.to_dict(), f, indent=2)

    def load_experiment(self, experiment_id: str) -> Experiment:
        """Load experiment by ID."""
        exp_file = self.experiments_dir / experiment_id / "experiment.json"
        with open(exp_file) as f:
            data = json.load(f)
        return Experiment(**data)

    def list_experiments(self, tags: dict = None) -> list[Experiment]:
        """List all experiments, optionally filtered by tags."""
        experiments = []

        for exp_dir in self.experiments_dir.iterdir():
            if not exp_dir.is_dir():
                continue

            exp_file = exp_dir / "experiment.json"
            if not exp_file.exists():
                continue

            exp = self.load_experiment(exp_dir.name)

            if tags:
                if not all(exp.tags.get(k) == v for k, v in tags.items()):
                    continue

            experiments.append(exp)

        return sorted(experiments, key=lambda x: x.start_time, reverse=True)

    def compare_experiments(self, experiment_ids: list[str]) -> dict:
        """Compare metrics across experiments."""
        comparison = {}

        for exp_id in experiment_ids:
            exp = self.load_experiment(exp_id)
            comparison[exp_id] = {
                "name": exp.name,
                "params": exp.params,
                "final_metrics": {
                    k: v[-1]["value"] if v else None
                    for k, v in exp.metrics.items()
                },
            }

        return comparison
```

---

## Experiment Comparison and Analysis

### Metrics Comparison

```python
import pandas as pd
import matplotlib.pyplot as plt
from mlflow.tracking import MlflowClient

def compare_runs(
    experiment_name: str,
    metric_keys: list[str],
    n_runs: int = 10,
) -> pd.DataFrame:
    """Compare recent runs in an experiment."""
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=n_runs,
    )

    data = []
    for run in runs:
        row = {
            "run_id": run.info.run_id,
            "run_name": run.info.run_name,
            "status": run.info.status,
            "start_time": run.info.start_time,
        }
        row.update(run.data.params)
        row.update({k: run.data.metrics.get(k) for k in metric_keys})
        data.append(row)

    return pd.DataFrame(data)

def plot_metric_comparison(
    runs_df: pd.DataFrame,
    metric: str,
    group_by: str = None,
) -> plt.Figure:
    """Plot metric comparison across runs."""
    fig, ax = plt.subplots(figsize=(10, 6))

    if group_by:
        for group, group_df in runs_df.groupby(group_by):
            ax.bar(group_df["run_name"], group_df[metric], label=str(group))
        ax.legend(title=group_by)
    else:
        ax.bar(runs_df["run_name"], runs_df[metric])

    ax.set_xlabel("Run")
    ax.set_ylabel(metric)
    ax.set_title(f"Comparison of {metric}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig
```

---

## Best Practices

### What to Track

```python
# Always track:
REQUIRED_PARAMS = [
    "learning_rate",
    "batch_size",
    "epochs",
    "model_architecture",
    "optimizer",
    "random_seed",
    "dataset_version",
]

REQUIRED_METRICS = [
    "train_loss",
    "val_loss",
    "train_accuracy",
    "val_accuracy",
]

REQUIRED_ARTIFACTS = [
    "model_checkpoint",
    "training_config",
    "requirements.txt",
]

# Recommended tags
RECOMMENDED_TAGS = {
    "author": "username",
    "environment": "dev|staging|prod",
    "model_type": "classification|regression|etc",
    "dataset": "dataset_name",
    "git_commit": "commit_hash",
}
```

### Experiment Naming Conventions

```python
# Good naming patterns
run_name = f"{model_type}_{dataset}_{timestamp}"
run_name = f"exp_{experiment_number:03d}_{description}"
run_name = f"{feature_flag}_{ablation_type}_{seed}"

# Organize with groups and tags
tags = {
    "project": "recommendation_engine",
    "sprint": "sprint_42",
    "hypothesis": "larger_embedding_helps",
}
```

---

## Related References

- `training-pipelines.md` - Integrating tracking with training
- `model-validation.md` - Validating tracked models
- `pipeline-orchestration.md` - Tracking in automated pipelines

## Cross-Reference Skills

- **DevOps Engineer** - MLflow server deployment
- **Data Engineer** - Artifact storage integration

---

## Reference: Feature Engineering

# Feature Engineering

---

## Overview

Feature engineering transforms raw data into features that improve model performance. Production systems require reproducible transformations, feature versioning, and online/offline consistency through feature stores.

## When to Use This Reference

- Building feature transformation pipelines
- Implementing feature stores (Feast, Tecton, custom)
- Creating data validation workflows
- Designing feature schemas and registries
- Handling feature drift and monitoring

## When NOT to Use

- Simple ad-hoc feature creation (use pandas directly)
- One-time exploratory analysis
- Prototyping with small datasets

---

## Feature Transformation Pipelines

### Scikit-learn Pipeline Pattern

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib

def create_feature_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
) -> ColumnTransformer:
    """Create reproducible feature transformation pipeline."""

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features),
        ],
        remainder='drop',
        verbose_feature_names_out=False,
    )

    return preprocessor

# Usage with versioning
def save_pipeline(pipeline: ColumnTransformer, version: str, path: str) -> str:
    """Save pipeline with version metadata."""
    import hashlib
    import json
    from datetime import datetime

    artifact_path = f"{path}/feature_pipeline_v{version}.joblib"
    metadata_path = f"{path}/feature_pipeline_v{version}_metadata.json"

    joblib.dump(pipeline, artifact_path)

    metadata = {
        "version": version,
        "created_at": datetime.utcnow().isoformat(),
        "feature_names_in": list(pipeline.feature_names_in_),
        "n_features_out": pipeline.n_features_out_,
    }

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    return artifact_path
```

### Custom Transformer Pattern

```python
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract features from datetime columns."""

    def __init__(self, date_column: str, features: list[str] = None):
        self.date_column = date_column
        self.features = features or ['year', 'month', 'day', 'dayofweek', 'hour']

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        dt = pd.to_datetime(X[self.date_column])

        feature_map = {
            'year': dt.dt.year,
            'month': dt.dt.month,
            'day': dt.dt.day,
            'dayofweek': dt.dt.dayofweek,
            'hour': dt.dt.hour,
            'is_weekend': dt.dt.dayofweek.isin([5, 6]).astype(int),
            'quarter': dt.dt.quarter,
        }

        for feature in self.features:
            if feature in feature_map:
                X[f"{self.date_column}_{feature}"] = feature_map[feature]

        return X.drop(columns=[self.date_column])

    def get_feature_names_out(self, input_features=None):
        return [f"{self.date_column}_{f}" for f in self.features]

class TargetEncoder(BaseEstimator, TransformerMixin):
    """Target encoding for high-cardinality categorical features."""

    def __init__(self, columns: list[str], smoothing: float = 1.0):
        self.columns = columns
        self.smoothing = smoothing
        self.encodings_: dict = {}
        self.global_mean_: float = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.global_mean_ = y.mean()

        for col in self.columns:
            stats = y.groupby(X[col]).agg(['mean', 'count'])
            smooth = (stats['count'] * stats['mean'] + self.smoothing * self.global_mean_) / (
                stats['count'] + self.smoothing
            )
            self.encodings_[col] = smooth.to_dict()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for col in self.columns:
            X[f"{col}_encoded"] = X[col].map(self.encodings_[col]).fillna(self.global_mean_)
        return X.drop(columns=self.columns)
```

---

## Feature Store with Feast

### Feature Store Setup

```python
# feature_store.yaml
"""
project: ml_project
registry: data/registry.db
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
offline_store:
  type: file
entity_key_serialization_version: 2
"""

# features/user_features.py
from datetime import timedelta
from feast import Entity, Feature, FeatureView, FileSource, Field
from feast.types import Float32, Int64, String

# Define entity
user = Entity(
    name="user_id",
    description="User identifier",
    join_keys=["user_id"],
)

# Define data source
user_stats_source = FileSource(
    path="data/user_stats.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Define feature view
user_stats_fv = FeatureView(
    name="user_stats",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_purchase_value", dtype=Float32),
        Field(name="days_since_last_purchase", dtype=Int64),
        Field(name="user_segment", dtype=String),
    ],
    source=user_stats_source,
    online=True,
    tags={"team": "ml", "owner": "data-science"},
)
```

### Feature Retrieval Pattern

```python
from feast import FeatureStore
import pandas as pd
from datetime import datetime

class FeatureService:
    """Production feature service with Feast."""

    def __init__(self, repo_path: str = "."):
        self.store = FeatureStore(repo_path=repo_path)

    def get_training_features(
        self,
        entity_df: pd.DataFrame,
        feature_refs: list[str],
    ) -> pd.DataFrame:
        """Get historical features for training."""
        return self.store.get_historical_features(
            entity_df=entity_df,
            features=feature_refs,
        ).to_df()

    def get_online_features(
        self,
        entity_rows: list[dict],
        feature_refs: list[str],
    ) -> dict:
        """Get features for real-time inference."""
        response = self.store.get_online_features(
            entity_rows=entity_rows,
            features=feature_refs,
        )
        return response.to_dict()

    def materialize_features(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        """Materialize features to online store."""
        self.store.materialize(start_date=start_date, end_date=end_date)

# Usage
feature_service = FeatureService()

# Training: historical features
entity_df = pd.DataFrame({
    "user_id": [1, 2, 3],
    "event_timestamp": [datetime(2024, 1, 15)] * 3,
})

training_features = feature_service.get_training_features(
    entity_df=entity_df,
    feature_refs=[
        "user_stats:total_purchases",
        "user_stats:avg_purchase_value",
        "user_stats:days_since_last_purchase",
    ],
)

# Inference: online features
online_features = feature_service.get_online_features(
    entity_rows=[{"user_id": 1}],
    feature_refs=["user_stats:total_purchases", "user_stats:avg_purchase_value"],
)
```

---

## Data Validation with Great Expectations

### Expectation Suite Definition

```python
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.checkpoint import Checkpoint

def create_feature_expectations(context: gx.DataContext) -> ExpectationSuite:
    """Define data quality expectations for features."""

    suite = context.add_expectation_suite("feature_validation_suite")

    # Column existence
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(column="user_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnToExist(column="purchase_amount")
    )

    # Null checks
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id")
    )
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="purchase_amount",
            mostly=0.95,  # Allow 5% nulls
        )
    )

    # Value ranges
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="purchase_amount",
            min_value=0,
            max_value=10000,
        )
    )

    # Uniqueness
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(column="transaction_id")
    )

    # Distribution checks
    suite.add_expectation(
        gx.expectations.ExpectColumnMeanToBeBetween(
            column="purchase_amount",
            min_value=50,
            max_value=500,
        )
    )

    return suite

def validate_features(
    df: pd.DataFrame,
    context: gx.DataContext,
    suite_name: str,
) -> dict:
    """Run validation and return results."""

    datasource = context.sources.add_pandas("runtime_source")
    data_asset = datasource.add_dataframe_asset("runtime_asset")
    batch_request = data_asset.build_batch_request(dataframe=df)

    checkpoint = context.add_or_update_checkpoint(
        name="feature_checkpoint",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": suite_name,
            }
        ],
    )

    result = checkpoint.run()

    return {
        "success": result.success,
        "statistics": result.run_results[list(result.run_results.keys())[0]].get("validation_result").statistics,
        "results": result.to_json_dict(),
    }
```

### Data Drift Detection

```python
from scipy import stats
import numpy as np
from dataclasses import dataclass

@dataclass
class DriftResult:
    feature: str
    drift_detected: bool
    statistic: float
    p_value: float
    method: str

class FeatureDriftDetector:
    """Detect distribution drift in features."""

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
        self.reference_stats: dict = {}

    def fit(self, reference_df: pd.DataFrame, features: list[str]) -> None:
        """Store reference distribution statistics."""
        for feature in features:
            self.reference_stats[feature] = {
                'mean': reference_df[feature].mean(),
                'std': reference_df[feature].std(),
                'values': reference_df[feature].dropna().values,
            }

    def detect_drift(
        self,
        current_df: pd.DataFrame,
        features: list[str],
    ) -> list[DriftResult]:
        """Detect drift using KS test."""
        results = []

        for feature in features:
            if feature not in self.reference_stats:
                continue

            reference_values = self.reference_stats[feature]['values']
            current_values = current_df[feature].dropna().values

            statistic, p_value = stats.ks_2samp(reference_values, current_values)

            results.append(DriftResult(
                feature=feature,
                drift_detected=p_value < self.significance_level,
                statistic=statistic,
                p_value=p_value,
                method='ks_test',
            ))

        return results

    def detect_drift_psi(
        self,
        current_df: pd.DataFrame,
        feature: str,
        bins: int = 10,
    ) -> DriftResult:
        """Detect drift using Population Stability Index."""
        reference = self.reference_stats[feature]['values']
        current = current_df[feature].dropna().values

        # Create bins from reference distribution
        bin_edges = np.percentile(reference, np.linspace(0, 100, bins + 1))
        bin_edges[0] = -np.inf
        bin_edges[-1] = np.inf

        ref_counts = np.histogram(reference, bins=bin_edges)[0] / len(reference)
        cur_counts = np.histogram(current, bins=bin_edges)[0] / len(current)

        # Avoid log(0)
        ref_counts = np.clip(ref_counts, 0.0001, None)
        cur_counts = np.clip(cur_counts, 0.0001, None)

        psi = np.sum((cur_counts - ref_counts) * np.log(cur_counts / ref_counts))

        return DriftResult(
            feature=feature,
            drift_detected=psi > 0.2,  # PSI > 0.2 indicates significant drift
            statistic=psi,
            p_value=np.nan,
            method='psi',
        )
```

---

## Feature Pipeline Integration

### Complete Feature Pipeline

```python
from typing import Protocol
from abc import abstractmethod
import logging

logger = logging.getLogger(__name__)

class FeatureTransformer(Protocol):
    """Protocol for feature transformers."""

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "FeatureTransformer": ...

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame: ...

class FeaturePipeline:
    """Production feature pipeline with validation and monitoring."""

    def __init__(
        self,
        transformers: list[tuple[str, FeatureTransformer]],
        validator: FeatureDriftDetector = None,
        feature_store: FeatureService = None,
    ):
        self.transformers = transformers
        self.validator = validator
        self.feature_store = feature_store
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "FeaturePipeline":
        """Fit all transformers."""
        X_current = X.copy()

        for name, transformer in self.transformers:
            logger.info(f"Fitting transformer: {name}")
            transformer.fit(X_current, y)
            X_current = transformer.transform(X_current)

        if self.validator:
            numeric_cols = X_current.select_dtypes(include=[np.number]).columns.tolist()
            self.validator.fit(X_current, numeric_cols)

        self.is_fitted = True
        return self

    def transform(
        self,
        X: pd.DataFrame,
        validate: bool = True,
    ) -> tuple[pd.DataFrame, list[DriftResult]]:
        """Transform features with optional validation."""
        if not self.is_fitted:
            raise ValueError("Pipeline must be fitted before transform")

        X_current = X.copy()

        for name, transformer in self.transformers:
            logger.info(f"Applying transformer: {name}")
            X_current = transformer.transform(X_current)

        drift_results = []
        if validate and self.validator:
            numeric_cols = X_current.select_dtypes(include=[np.number]).columns.tolist()
            drift_results = self.validator.detect_drift(X_current, numeric_cols)

            drifted = [r.feature for r in drift_results if r.drift_detected]
            if drifted:
                logger.warning(f"Drift detected in features: {drifted}")

        return X_current, drift_results

    def save(self, path: str) -> None:
        """Save pipeline artifacts."""
        import pickle

        with open(f"{path}/feature_pipeline.pkl", 'wb') as f:
            pickle.dump({
                'transformers': self.transformers,
                'validator': self.validator,
                'is_fitted': self.is_fitted,
            }, f)

    @classmethod
    def load(cls, path: str) -> "FeaturePipeline":
        """Load pipeline from artifacts."""
        import pickle

        with open(f"{path}/feature_pipeline.pkl", 'rb') as f:
            data = pickle.load(f)

        pipeline = cls(
            transformers=data['transformers'],
            validator=data['validator'],
        )
        pipeline.is_fitted = data['is_fitted']
        return pipeline
```

---

## Best Practices

### Feature Naming Conventions

```python
# Good: descriptive, includes transformation info
"user_total_purchases_30d"
"product_price_log_scaled"
"category_onehot_electronics"

# Bad: ambiguous, no context
"feature_1"
"x_transformed"
"col"
```

### Feature Documentation

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class FeatureMetadata:
    """Document feature for registry."""
    name: str
    description: str
    dtype: str
    source_table: str
    transformation: str
    owner: str
    created_at: str
    tags: list[str]
    dependencies: list[str]
    freshness_sla: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "dtype": self.dtype,
            "source_table": self.source_table,
            "transformation": self.transformation,
            "owner": self.owner,
            "created_at": self.created_at,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "freshness_sla": self.freshness_sla,
        }
```

---

## Related References

- `training-pipelines.md` - Using features in training workflows
- `experiment-tracking.md` - Logging feature importance and metadata
- `model-validation.md` - Validating model performance on feature sets

## Cross-Reference Skills

- **Pandas Pro** - DataFrame operations for feature engineering
- **Data Engineer** - Data pipeline integration for feature computation

---

## Reference: Model Validation

# Model Validation

---

## Overview

Model validation ensures models meet quality standards before production deployment. It encompasses offline evaluation, online testing, and continuous monitoring to catch performance degradation, data drift, and model failures.

## When to Use This Reference

- Implementing offline model evaluation strategies
- Setting up A/B testing frameworks
- Building shadow deployment pipelines
- Creating model comparison workflows
- Implementing continuous model monitoring

## When NOT to Use

- Quick model prototyping
- One-off analysis without deployment
- Models with no production requirements

---

## Offline Evaluation

### Comprehensive Evaluation Suite

```python
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score,
)

@dataclass
class ClassificationMetrics:
    """Classification model metrics."""
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float]
    pr_auc: Optional[float]
    confusion_matrix: np.ndarray

    def to_dict(self) -> dict:
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "roc_auc": self.roc_auc,
            "pr_auc": self.pr_auc,
        }

@dataclass
class RegressionMetrics:
    """Regression model metrics."""
    mse: float
    rmse: float
    mae: float
    r2: float
    mape: Optional[float]

    def to_dict(self) -> dict:
        return {
            "mse": self.mse,
            "rmse": self.rmse,
            "mae": self.mae,
            "r2": self.r2,
            "mape": self.mape,
        }

class ModelEvaluator:
    """Comprehensive model evaluation."""

    def __init__(self, task_type: str = "classification"):
        self.task_type = task_type

    def evaluate_classification(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
        average: str = "weighted",
    ) -> ClassificationMetrics:
        """Evaluate classification model."""
        roc_auc = None
        pr_auc = None

        if y_prob is not None:
            if len(np.unique(y_true)) == 2:
                # Binary classification
                if y_prob.ndim == 2:
                    y_prob_pos = y_prob[:, 1]
                else:
                    y_prob_pos = y_prob
                roc_auc = roc_auc_score(y_true, y_prob_pos)
                pr_auc = average_precision_score(y_true, y_prob_pos)
            else:
                # Multiclass
                roc_auc = roc_auc_score(
                    y_true, y_prob, multi_class="ovr", average=average
                )

        return ClassificationMetrics(
            accuracy=accuracy_score(y_true, y_pred),
            precision=precision_score(y_true, y_pred, average=average, zero_division=0),
            recall=recall_score(y_true, y_pred, average=average, zero_division=0),
            f1=f1_score(y_true, y_pred, average=average, zero_division=0),
            roc_auc=roc_auc,
            pr_auc=pr_auc,
            confusion_matrix=confusion_matrix(y_true, y_pred),
        )

    def evaluate_regression(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> RegressionMetrics:
        """Evaluate regression model."""
        mse = mean_squared_error(y_true, y_pred)

        # MAPE (handle zero values)
        mask = y_true != 0
        if mask.any():
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        else:
            mape = None

        return RegressionMetrics(
            mse=mse,
            rmse=np.sqrt(mse),
            mae=mean_absolute_error(y_true, y_pred),
            r2=r2_score(y_true, y_pred),
            mape=mape,
        )

    def evaluate_by_segment(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        segments: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
    ) -> dict:
        """Evaluate model performance by segment."""
        results = {}

        for segment in np.unique(segments):
            mask = segments == segment

            if self.task_type == "classification":
                segment_prob = y_prob[mask] if y_prob is not None else None
                metrics = self.evaluate_classification(
                    y_true[mask], y_pred[mask], segment_prob
                )
            else:
                metrics = self.evaluate_regression(y_true[mask], y_pred[mask])

            results[segment] = metrics.to_dict()

        return results
```

### Cross-Validation Framework

```python
from sklearn.model_selection import (
    KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score
)
import numpy as np
from typing import Callable

class CrossValidator:
    """Cross-validation framework for model evaluation."""

    def __init__(
        self,
        n_splits: int = 5,
        shuffle: bool = True,
        random_state: int = 42,
    ):
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def validate_classification(
        self,
        model,
        X: np.ndarray,
        y: np.ndarray,
        stratified: bool = True,
    ) -> dict:
        """Run stratified k-fold cross-validation for classification."""
        if stratified:
            cv = StratifiedKFold(
                n_splits=self.n_splits,
                shuffle=self.shuffle,
                random_state=self.random_state,
            )
        else:
            cv = KFold(
                n_splits=self.n_splits,
                shuffle=self.shuffle,
                random_state=self.random_state,
            )

        evaluator = ModelEvaluator("classification")
        fold_metrics = []

        for fold, (train_idx, val_idx) in enumerate(cv.split(X, y)):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            # Clone and train model
            from sklearn.base import clone
            fold_model = clone(model)
            fold_model.fit(X_train, y_train)

            y_pred = fold_model.predict(X_val)
            y_prob = None
            if hasattr(fold_model, "predict_proba"):
                y_prob = fold_model.predict_proba(X_val)

            metrics = evaluator.evaluate_classification(y_val, y_pred, y_prob)
            fold_metrics.append(metrics.to_dict())

        return self._aggregate_cv_results(fold_metrics)

    def validate_time_series(
        self,
        model,
        X: np.ndarray,
        y: np.ndarray,
        gap: int = 0,
    ) -> dict:
        """Run time series cross-validation."""
        cv = TimeSeriesSplit(n_splits=self.n_splits, gap=gap)
        evaluator = ModelEvaluator("regression")
        fold_metrics = []

        for train_idx, val_idx in cv.split(X):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            from sklearn.base import clone
            fold_model = clone(model)
            fold_model.fit(X_train, y_train)

            y_pred = fold_model.predict(X_val)
            metrics = evaluator.evaluate_regression(y_val, y_pred)
            fold_metrics.append(metrics.to_dict())

        return self._aggregate_cv_results(fold_metrics)

    def _aggregate_cv_results(self, fold_metrics: list[dict]) -> dict:
        """Aggregate metrics across folds."""
        keys = fold_metrics[0].keys()
        aggregated = {}

        for key in keys:
            values = [m[key] for m in fold_metrics if m[key] is not None]
            if values:
                aggregated[key] = {
                    "mean": np.mean(values),
                    "std": np.std(values),
                    "min": np.min(values),
                    "max": np.max(values),
                    "values": values,
                }

        return aggregated
```

---

## Model Comparison

### Statistical Comparison

```python
from scipy import stats
import numpy as np
from dataclasses import dataclass

@dataclass
class ComparisonResult:
    """Model comparison statistical result."""
    model_a_mean: float
    model_b_mean: float
    difference: float
    p_value: float
    significant: bool
    confidence_interval: tuple[float, float]
    test_used: str

class ModelComparator:
    """Statistical comparison of model performance."""

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level

    def paired_t_test(
        self,
        scores_a: np.ndarray,
        scores_b: np.ndarray,
    ) -> ComparisonResult:
        """Paired t-test for CV score comparison."""
        statistic, p_value = stats.ttest_rel(scores_a, scores_b)

        differences = scores_a - scores_b
        mean_diff = np.mean(differences)
        std_diff = np.std(differences, ddof=1)
        n = len(differences)

        # 95% confidence interval
        t_critical = stats.t.ppf(1 - self.significance_level / 2, n - 1)
        margin = t_critical * std_diff / np.sqrt(n)
        ci = (mean_diff - margin, mean_diff + margin)

        return ComparisonResult(
            model_a_mean=np.mean(scores_a),
            model_b_mean=np.mean(scores_b),
            difference=mean_diff,
            p_value=p_value,
            significant=p_value < self.significance_level,
            confidence_interval=ci,
            test_used="paired_t_test",
        )

    def wilcoxon_test(
        self,
        scores_a: np.ndarray,
        scores_b: np.ndarray,
    ) -> ComparisonResult:
        """Wilcoxon signed-rank test (non-parametric)."""
        statistic, p_value = stats.wilcoxon(scores_a, scores_b)

        differences = scores_a - scores_b
        mean_diff = np.mean(differences)

        # Bootstrap confidence interval
        ci = self._bootstrap_ci(differences)

        return ComparisonResult(
            model_a_mean=np.mean(scores_a),
            model_b_mean=np.mean(scores_b),
            difference=mean_diff,
            p_value=p_value,
            significant=p_value < self.significance_level,
            confidence_interval=ci,
            test_used="wilcoxon",
        )

    def mcnemar_test(
        self,
        y_true: np.ndarray,
        pred_a: np.ndarray,
        pred_b: np.ndarray,
    ) -> ComparisonResult:
        """McNemar's test for classifier comparison."""
        # Build contingency table
        correct_a = (pred_a == y_true)
        correct_b = (pred_b == y_true)

        # b: A correct, B wrong; c: A wrong, B correct
        b = np.sum(correct_a & ~correct_b)
        c = np.sum(~correct_a & correct_b)

        if b + c < 25:
            # Use exact binomial test for small samples
            p_value = stats.binom_test(b, b + c, 0.5)
        else:
            # Use chi-square approximation
            statistic = (abs(b - c) - 1) ** 2 / (b + c)
            p_value = 1 - stats.chi2.cdf(statistic, 1)

        acc_a = np.mean(correct_a)
        acc_b = np.mean(correct_b)

        return ComparisonResult(
            model_a_mean=acc_a,
            model_b_mean=acc_b,
            difference=acc_a - acc_b,
            p_value=p_value,
            significant=p_value < self.significance_level,
            confidence_interval=(None, None),
            test_used="mcnemar",
        )

    def _bootstrap_ci(
        self,
        data: np.ndarray,
        n_bootstrap: int = 10000,
        alpha: float = 0.05,
    ) -> tuple[float, float]:
        """Calculate bootstrap confidence interval."""
        bootstrapped_means = []

        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrapped_means.append(np.mean(sample))

        lower = np.percentile(bootstrapped_means, alpha / 2 * 100)
        upper = np.percentile(bootstrapped_means, (1 - alpha / 2) * 100)

        return (lower, upper)
```

---

## A/B Testing

### Online Experiment Framework

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import numpy as np
import hashlib
import json

@dataclass
class Experiment:
    """A/B test experiment configuration."""
    experiment_id: str
    name: str
    control_model: str
    treatment_model: str
    traffic_split: float  # Fraction to treatment
    start_time: datetime
    end_time: Optional[datetime]
    metrics: list[str]
    minimum_sample_size: int
    status: str = "active"

class ABTestRouter:
    """Route traffic between control and treatment."""

    def __init__(self, experiment: Experiment):
        self.experiment = experiment

    def get_variant(self, user_id: str) -> str:
        """Deterministically assign user to variant."""
        # Hash user_id for consistent assignment
        hash_input = f"{self.experiment.experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        normalized = hash_value / (2**128)

        if normalized < self.experiment.traffic_split:
            return "treatment"
        return "control"

    def get_model(self, user_id: str) -> str:
        """Get model to use for user."""
        variant = self.get_variant(user_id)

        if variant == "treatment":
            return self.experiment.treatment_model
        return self.experiment.control_model

class ABTestAnalyzer:
    """Analyze A/B test results."""

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level

    def analyze_conversion(
        self,
        control_conversions: int,
        control_total: int,
        treatment_conversions: int,
        treatment_total: int,
    ) -> dict:
        """Analyze conversion rate experiment."""
        control_rate = control_conversions / control_total
        treatment_rate = treatment_conversions / treatment_total

        # Two-proportion z-test
        pooled_rate = (control_conversions + treatment_conversions) / (
            control_total + treatment_total
        )
        se = np.sqrt(
            pooled_rate * (1 - pooled_rate) * (1/control_total + 1/treatment_total)
        )

        z_stat = (treatment_rate - control_rate) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Relative lift
        lift = (treatment_rate - control_rate) / control_rate if control_rate > 0 else 0

        # Confidence interval for difference
        se_diff = np.sqrt(
            control_rate * (1 - control_rate) / control_total +
            treatment_rate * (1 - treatment_rate) / treatment_total
        )
        z_critical = stats.norm.ppf(1 - self.significance_level / 2)
        ci = (
            (treatment_rate - control_rate) - z_critical * se_diff,
            (treatment_rate - control_rate) + z_critical * se_diff,
        )

        return {
            "control_rate": control_rate,
            "treatment_rate": treatment_rate,
            "absolute_difference": treatment_rate - control_rate,
            "relative_lift": lift,
            "p_value": p_value,
            "significant": p_value < self.significance_level,
            "confidence_interval": ci,
            "control_sample_size": control_total,
            "treatment_sample_size": treatment_total,
        }

    def analyze_continuous_metric(
        self,
        control_values: np.ndarray,
        treatment_values: np.ndarray,
    ) -> dict:
        """Analyze continuous metric (e.g., revenue, time)."""
        control_mean = np.mean(control_values)
        treatment_mean = np.mean(treatment_values)

        # Welch's t-test (unequal variances)
        statistic, p_value = stats.ttest_ind(
            treatment_values, control_values, equal_var=False
        )

        lift = (treatment_mean - control_mean) / control_mean if control_mean > 0 else 0

        # Confidence interval
        se_diff = np.sqrt(
            np.var(control_values) / len(control_values) +
            np.var(treatment_values) / len(treatment_values)
        )
        t_critical = stats.t.ppf(
            1 - self.significance_level / 2,
            min(len(control_values), len(treatment_values)) - 1
        )
        ci = (
            (treatment_mean - control_mean) - t_critical * se_diff,
            (treatment_mean - control_mean) + t_critical * se_diff,
        )

        return {
            "control_mean": control_mean,
            "treatment_mean": treatment_mean,
            "absolute_difference": treatment_mean - control_mean,
            "relative_lift": lift,
            "p_value": p_value,
            "significant": p_value < self.significance_level,
            "confidence_interval": ci,
            "control_sample_size": len(control_values),
            "treatment_sample_size": len(treatment_values),
        }

    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        power: float = 0.8,
    ) -> int:
        """Calculate required sample size per variant."""
        alpha = self.significance_level
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)

        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)

        p_bar = (p1 + p2) / 2

        n = (
            (z_alpha * np.sqrt(2 * p_bar * (1 - p_bar)) +
             z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 /
            (p2 - p1) ** 2
        )

        return int(np.ceil(n))
```

---

## Shadow Deployment

### Shadow Mode Pipeline

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

@dataclass
class PredictionComparison:
    """Comparison of production and shadow predictions."""
    request_id: str
    timestamp: datetime
    production_prediction: Any
    shadow_prediction: Any
    production_latency_ms: float
    shadow_latency_ms: float
    agreement: bool
    features: Optional[dict] = None

class ShadowDeployment:
    """Shadow deployment for model validation."""

    def __init__(
        self,
        production_model,
        shadow_model,
        log_path: str = "/var/log/shadow_predictions.jsonl",
    ):
        self.production_model = production_model
        self.shadow_model = shadow_model
        self.log_path = log_path
        self.comparisons: list[PredictionComparison] = []

    def predict(
        self,
        features: dict,
        request_id: str = None,
    ) -> Any:
        """Get production prediction, run shadow in parallel."""
        import time
        import uuid
        import concurrent.futures

        request_id = request_id or str(uuid.uuid4())

        # Production prediction (synchronous, used for response)
        prod_start = time.time()
        production_pred = self.production_model.predict(features)
        prod_latency = (time.time() - prod_start) * 1000

        # Shadow prediction (async, logged but not returned)
        def run_shadow():
            shadow_start = time.time()
            shadow_pred = self.shadow_model.predict(features)
            shadow_latency = (time.time() - shadow_start) * 1000
            return shadow_pred, shadow_latency

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_shadow)

            try:
                shadow_pred, shadow_latency = future.result(timeout=5.0)

                comparison = PredictionComparison(
                    request_id=request_id,
                    timestamp=datetime.utcnow(),
                    production_prediction=production_pred,
                    shadow_prediction=shadow_pred,
                    production_latency_ms=prod_latency,
                    shadow_latency_ms=shadow_latency,
                    agreement=self._check_agreement(production_pred, shadow_pred),
                    features=features,
                )

                self._log_comparison(comparison)

            except concurrent.futures.TimeoutError:
                logger.warning(f"Shadow prediction timed out for {request_id}")

        return production_pred

    def _check_agreement(self, prod_pred: Any, shadow_pred: Any) -> bool:
        """Check if predictions agree."""
        if isinstance(prod_pred, (list, np.ndarray)):
            return np.allclose(prod_pred, shadow_pred, rtol=1e-3)
        return prod_pred == shadow_pred

    def _log_comparison(self, comparison: PredictionComparison) -> None:
        """Log comparison to file."""
        log_entry = {
            "request_id": comparison.request_id,
            "timestamp": comparison.timestamp.isoformat(),
            "production_prediction": str(comparison.production_prediction),
            "shadow_prediction": str(comparison.shadow_prediction),
            "production_latency_ms": comparison.production_latency_ms,
            "shadow_latency_ms": comparison.shadow_latency_ms,
            "agreement": comparison.agreement,
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        self.comparisons.append(comparison)

    def analyze_shadow_performance(self) -> dict:
        """Analyze shadow model performance."""
        if not self.comparisons:
            return {}

        agreements = [c.agreement for c in self.comparisons]
        prod_latencies = [c.production_latency_ms for c in self.comparisons]
        shadow_latencies = [c.shadow_latency_ms for c in self.comparisons]

        return {
            "total_comparisons": len(self.comparisons),
            "agreement_rate": np.mean(agreements),
            "production_latency_p50": np.percentile(prod_latencies, 50),
            "production_latency_p99": np.percentile(prod_latencies, 99),
            "shadow_latency_p50": np.percentile(shadow_latencies, 50),
            "shadow_latency_p99": np.percentile(shadow_latencies, 99),
            "latency_difference_mean": np.mean(
                [s - p for s, p in zip(shadow_latencies, prod_latencies)]
            ),
        }
```

---

## Validation Pipeline Integration

### Complete Validation Workflow

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class ValidationStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

@dataclass
class ValidationResult:
    """Result of a validation check."""
    check_name: str
    status: ValidationStatus
    message: str
    details: Optional[dict] = None

class ModelValidator:
    """Complete model validation workflow."""

    def __init__(
        self,
        accuracy_threshold: float = 0.8,
        latency_threshold_ms: float = 100,
        drift_threshold: float = 0.2,
    ):
        self.accuracy_threshold = accuracy_threshold
        self.latency_threshold_ms = latency_threshold_ms
        self.drift_threshold = drift_threshold
        self.results: list[ValidationResult] = []

    def validate_performance(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> ValidationResult:
        """Validate model performance metrics."""
        evaluator = ModelEvaluator("classification")
        metrics = evaluator.evaluate_classification(y_true, y_pred)

        if metrics.accuracy >= self.accuracy_threshold:
            status = ValidationStatus.PASSED
            message = f"Accuracy {metrics.accuracy:.4f} meets threshold"
        else:
            status = ValidationStatus.FAILED
            message = f"Accuracy {metrics.accuracy:.4f} below threshold {self.accuracy_threshold}"

        result = ValidationResult(
            check_name="performance",
            status=status,
            message=message,
            details=metrics.to_dict(),
        )
        self.results.append(result)
        return result

    def validate_latency(
        self,
        model,
        sample_input: np.ndarray,
        n_iterations: int = 100,
    ) -> ValidationResult:
        """Validate inference latency."""
        import time

        latencies = []
        for _ in range(n_iterations):
            start = time.time()
            model.predict(sample_input)
            latencies.append((time.time() - start) * 1000)

        p50 = np.percentile(latencies, 50)
        p99 = np.percentile(latencies, 99)

        if p99 <= self.latency_threshold_ms:
            status = ValidationStatus.PASSED
            message = f"P99 latency {p99:.2f}ms meets threshold"
        elif p50 <= self.latency_threshold_ms:
            status = ValidationStatus.WARNING
            message = f"P50 OK but P99 {p99:.2f}ms exceeds threshold"
        else:
            status = ValidationStatus.FAILED
            message = f"P99 latency {p99:.2f}ms exceeds threshold"

        result = ValidationResult(
            check_name="latency",
            status=status,
            message=message,
            details={"p50_ms": p50, "p99_ms": p99, "mean_ms": np.mean(latencies)},
        )
        self.results.append(result)
        return result

    def validate_data_compatibility(
        self,
        model,
        expected_features: list[str],
        sample_data: pd.DataFrame,
    ) -> ValidationResult:
        """Validate model accepts expected input format."""
        missing_features = set(expected_features) - set(sample_data.columns)
        extra_features = set(sample_data.columns) - set(expected_features)

        if missing_features:
            status = ValidationStatus.FAILED
            message = f"Missing features: {missing_features}"
        elif extra_features:
            status = ValidationStatus.WARNING
            message = f"Extra features will be ignored: {extra_features}"
        else:
            status = ValidationStatus.PASSED
            message = "All expected features present"

        # Try inference
        try:
            model.predict(sample_data[expected_features].head(1))
        except Exception as e:
            status = ValidationStatus.FAILED
            message = f"Inference failed: {str(e)}"

        result = ValidationResult(
            check_name="data_compatibility",
            status=status,
            message=message,
            details={
                "missing_features": list(missing_features),
                "extra_features": list(extra_features),
            },
        )
        self.results.append(result)
        return result

    def validate_vs_baseline(
        self,
        y_true: np.ndarray,
        new_pred: np.ndarray,
        baseline_pred: np.ndarray,
    ) -> ValidationResult:
        """Validate new model vs baseline."""
        comparator = ModelComparator()
        comparison = comparator.mcnemar_test(y_true, new_pred, baseline_pred)

        new_acc = accuracy_score(y_true, new_pred)
        baseline_acc = accuracy_score(y_true, baseline_pred)

        if new_acc >= baseline_acc:
            if comparison.significant:
                status = ValidationStatus.PASSED
                message = f"Significant improvement: {new_acc:.4f} vs {baseline_acc:.4f}"
            else:
                status = ValidationStatus.WARNING
                message = f"Improvement not significant: {new_acc:.4f} vs {baseline_acc:.4f}"
        else:
            if comparison.significant:
                status = ValidationStatus.FAILED
                message = f"Significant regression: {new_acc:.4f} vs {baseline_acc:.4f}"
            else:
                status = ValidationStatus.WARNING
                message = f"Minor regression: {new_acc:.4f} vs {baseline_acc:.4f}"

        result = ValidationResult(
            check_name="baseline_comparison",
            status=status,
            message=message,
            details={
                "new_accuracy": new_acc,
                "baseline_accuracy": baseline_acc,
                "p_value": comparison.p_value,
            },
        )
        self.results.append(result)
        return result

    def get_summary(self) -> dict:
        """Get validation summary."""
        passed = sum(1 for r in self.results if r.status == ValidationStatus.PASSED)
        warnings = sum(1 for r in self.results if r.status == ValidationStatus.WARNING)
        failed = sum(1 for r in self.results if r.status == ValidationStatus.FAILED)

        overall_status = (
            ValidationStatus.FAILED if failed > 0
            else ValidationStatus.WARNING if warnings > 0
            else ValidationStatus.PASSED
        )

        return {
            "overall_status": overall_status.value,
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
            "results": [
                {
                    "check": r.check_name,
                    "status": r.status.value,
                    "message": r.message,
                }
                for r in self.results
            ],
        }
```

---

## Best Practices

### Validation Checklist

```python
VALIDATION_CHECKLIST = {
    "offline": [
        "Accuracy/performance metrics meet threshold",
        "Cross-validation shows consistent performance",
        "Model outperforms or matches baseline",
        "Metrics stable across data segments",
    ],
    "pre_deployment": [
        "Inference latency within SLA",
        "Memory usage acceptable",
        "Input/output schema validated",
        "Model serialization/loading works",
    ],
    "shadow": [
        "Shadow predictions logged successfully",
        "Agreement rate with production acceptable",
        "No latency regression",
        "Error rate within bounds",
    ],
    "ab_test": [
        "Sufficient sample size reached",
        "Statistical significance achieved",
        "No negative impact on guardrail metrics",
        "Business metrics improved",
    ],
}
```

---

## Related References

- `training-pipelines.md` - Model training before validation
- `experiment-tracking.md` - Logging validation results
- `pipeline-orchestration.md` - Automated validation workflows
- `feature-engineering.md` - Feature validation

## Cross-Reference Skills

- **Data Engineer** - Data quality validation
- **DevOps Engineer** - Deployment pipeline integration

---

## Reference: Pipeline Orchestration

# Pipeline Orchestration

---

## Overview

Pipeline orchestration automates the end-to-end ML workflow from data ingestion through model deployment. Orchestrators manage dependencies, handle failures, enable scheduling, and provide observability across complex multi-step pipelines.

## When to Use This Reference

- Building Kubeflow Pipelines for ML workflows
- Creating Airflow DAGs for data and ML pipelines
- Implementing Prefect flows for modern orchestration
- Designing pipeline DAGs and component dependencies
- Setting up scheduled retraining workflows

## When NOT to Use

- Simple linear scripts without dependencies
- One-off data processing tasks
- Interactive development and experimentation

---

## Kubeflow Pipelines

### Pipeline Definition (KFP v2)

```python
from kfp import dsl
from kfp.dsl import Input, Output, Artifact, Dataset, Model, Metrics
from kfp import compiler
from typing import NamedTuple

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn"],
)
def load_data(
    data_path: str,
    output_dataset: Output[Dataset],
) -> None:
    """Load and validate raw data."""
    import pandas as pd

    df = pd.read_parquet(data_path)

    # Basic validation
    assert len(df) > 0, "Dataset is empty"
    assert "target" in df.columns, "Missing target column"

    df.to_parquet(output_dataset.path)
    output_dataset.metadata["num_rows"] = len(df)
    output_dataset.metadata["num_features"] = len(df.columns) - 1

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn"],
)
def preprocess_data(
    input_dataset: Input[Dataset],
    train_dataset: Output[Dataset],
    test_dataset: Output[Dataset],
    test_size: float = 0.2,
    random_state: int = 42,
) -> None:
    """Preprocess and split data."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    df = pd.read_parquet(input_dataset.path)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df["target"] = y_train.values
    train_df.to_parquet(train_dataset.path)

    test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_df["target"] = y_test.values
    test_df.to_parquet(test_dataset.path)

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "joblib"],
)
def train_model(
    train_dataset: Input[Dataset],
    model_artifact: Output[Model],
    n_estimators: int = 100,
    max_depth: int = 10,
) -> None:
    """Train RandomForest model."""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib

    df = pd.read_parquet(train_dataset.path)
    X = df.drop("target", axis=1)
    y = df["target"]

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
    )
    model.fit(X, y)

    joblib.dump(model, model_artifact.path)
    model_artifact.metadata["n_estimators"] = n_estimators
    model_artifact.metadata["max_depth"] = max_depth

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "joblib"],
)
def evaluate_model(
    model_artifact: Input[Model],
    test_dataset: Input[Dataset],
    metrics: Output[Metrics],
    threshold: float = 0.8,
) -> NamedTuple("Outputs", [("passed", bool), ("accuracy", float)]):
    """Evaluate model and check threshold."""
    import pandas as pd
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    import joblib
    from collections import namedtuple

    model = joblib.load(model_artifact.path)
    df = pd.read_parquet(test_dataset.path)
    X = df.drop("target", axis=1)
    y = df["target"]

    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)
    precision = precision_score(y, predictions, average="weighted")
    recall = recall_score(y, predictions, average="weighted")
    f1 = f1_score(y, predictions, average="weighted")

    metrics.log_metric("accuracy", accuracy)
    metrics.log_metric("precision", precision)
    metrics.log_metric("recall", recall)
    metrics.log_metric("f1_score", f1)

    passed = accuracy >= threshold

    Outputs = namedtuple("Outputs", ["passed", "accuracy"])
    return Outputs(passed, accuracy)

@dsl.component(
    base_image="python:3.11-slim",
    packages_to_install=["google-cloud-storage"],
)
def deploy_model(
    model_artifact: Input[Model],
    model_name: str,
    endpoint: str,
) -> str:
    """Deploy model to serving endpoint."""
    from google.cloud import storage
    import shutil

    # Copy model to GCS
    bucket_name = endpoint.split("/")[2]
    model_path = f"models/{model_name}/model.joblib"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    blob.upload_from_filename(model_artifact.path)

    return f"gs://{bucket_name}/{model_path}"

@dsl.pipeline(
    name="ml-training-pipeline",
    description="End-to-end ML training pipeline",
)
def ml_pipeline(
    data_path: str,
    n_estimators: int = 100,
    max_depth: int = 10,
    accuracy_threshold: float = 0.8,
    model_name: str = "classifier",
    endpoint: str = "gs://ml-models/serving",
) -> None:
    """Complete ML training pipeline."""

    load_task = load_data(data_path=data_path)

    preprocess_task = preprocess_data(
        input_dataset=load_task.outputs["output_dataset"],
    )

    train_task = train_model(
        train_dataset=preprocess_task.outputs["train_dataset"],
        n_estimators=n_estimators,
        max_depth=max_depth,
    )

    evaluate_task = evaluate_model(
        model_artifact=train_task.outputs["model_artifact"],
        test_dataset=preprocess_task.outputs["test_dataset"],
        threshold=accuracy_threshold,
    )

    with dsl.If(evaluate_task.outputs["passed"] == True):
        deploy_model(
            model_artifact=train_task.outputs["model_artifact"],
            model_name=model_name,
            endpoint=endpoint,
        )

# Compile pipeline
if __name__ == "__main__":
    compiler.Compiler().compile(
        ml_pipeline,
        "ml_pipeline.yaml",
    )
```

### Running Kubeflow Pipelines

```python
from kfp.client import Client

def run_pipeline(
    pipeline_file: str,
    experiment_name: str,
    run_name: str,
    parameters: dict,
) -> str:
    """Submit pipeline run to Kubeflow."""
    client = Client(host="https://kubeflow.example.com/pipeline")

    # Create or get experiment
    experiment = client.create_experiment(name=experiment_name)

    # Submit run
    run = client.create_run_from_pipeline_package(
        pipeline_file=pipeline_file,
        experiment_id=experiment.experiment_id,
        run_name=run_name,
        arguments=parameters,
    )

    return run.run_id

def schedule_pipeline(
    pipeline_file: str,
    experiment_name: str,
    schedule_name: str,
    cron_expression: str,
    parameters: dict,
) -> str:
    """Create recurring pipeline run."""
    client = Client(host="https://kubeflow.example.com/pipeline")

    experiment = client.create_experiment(name=experiment_name)

    # Create recurring run
    job = client.create_recurring_run(
        experiment_id=experiment.experiment_id,
        job_name=schedule_name,
        pipeline_package_path=pipeline_file,
        cron_expression=cron_expression,
        enabled=True,
        parameters=parameters,
    )

    return job.id
```

---

## Apache Airflow

### ML Pipeline DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import json

default_args = {
    "owner": "ml-team",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}

def load_data(**context):
    """Load data from source."""
    import pandas as pd

    data_path = context["params"]["data_path"]
    df = pd.read_parquet(data_path)

    # Push to XCom for downstream tasks
    output_path = f"/tmp/data_{context['run_id']}.parquet"
    df.to_parquet(output_path)

    context["ti"].xcom_push(key="data_path", value=output_path)
    context["ti"].xcom_push(key="num_rows", value=len(df))

    return output_path

def preprocess_data(**context):
    """Preprocess and split data."""
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    input_path = context["ti"].xcom_pull(key="data_path", task_ids="load_data")
    df = pd.read_parquet(input_path)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save processed data
    train_path = f"/tmp/train_{context['run_id']}.parquet"
    test_path = f"/tmp/test_{context['run_id']}.parquet"

    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df["target"] = y_train.values
    train_df.to_parquet(train_path)

    test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_df["target"] = y_test.values
    test_df.to_parquet(test_path)

    context["ti"].xcom_push(key="train_path", value=train_path)
    context["ti"].xcom_push(key="test_path", value=test_path)

def train_model(**context):
    """Train ML model."""
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib

    train_path = context["ti"].xcom_pull(key="train_path", task_ids="preprocess_data")
    df = pd.read_parquet(train_path)

    X = df.drop("target", axis=1)
    y = df["target"]

    params = context["params"]
    model = RandomForestClassifier(
        n_estimators=params.get("n_estimators", 100),
        max_depth=params.get("max_depth", 10),
        random_state=42,
    )
    model.fit(X, y)

    model_path = f"/tmp/model_{context['run_id']}.joblib"
    joblib.dump(model, model_path)

    context["ti"].xcom_push(key="model_path", value=model_path)

def evaluate_model(**context):
    """Evaluate model and return metrics."""
    import pandas as pd
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    import joblib

    model_path = context["ti"].xcom_pull(key="model_path", task_ids="train_model")
    test_path = context["ti"].xcom_pull(key="test_path", task_ids="preprocess_data")

    model = joblib.load(model_path)
    df = pd.read_parquet(test_path)

    X = df.drop("target", axis=1)
    y = df["target"]

    predictions = model.predict(X)

    metrics = {
        "accuracy": accuracy_score(y, predictions),
        "precision": precision_score(y, predictions, average="weighted"),
        "recall": recall_score(y, predictions, average="weighted"),
    }

    context["ti"].xcom_push(key="metrics", value=metrics)

    return metrics

def check_metrics_threshold(**context):
    """Branch based on model performance."""
    metrics = context["ti"].xcom_pull(key="metrics", task_ids="evaluate_model")
    threshold = context["params"].get("accuracy_threshold", 0.8)

    if metrics["accuracy"] >= threshold:
        return "deploy_model"
    return "skip_deployment"

def deploy_model(**context):
    """Deploy model to production."""
    import shutil

    model_path = context["ti"].xcom_pull(key="model_path", task_ids="train_model")
    metrics = context["ti"].xcom_pull(key="metrics", task_ids="evaluate_model")

    # In production, this would upload to model registry/serving
    deploy_path = f"/models/production/model_{context['run_id']}.joblib"
    shutil.copy(model_path, deploy_path)

    return {
        "model_path": deploy_path,
        "metrics": metrics,
        "deployed_at": datetime.utcnow().isoformat(),
    }

with DAG(
    dag_id="ml_training_pipeline",
    default_args=default_args,
    description="End-to-end ML training pipeline",
    schedule_interval="0 2 * * *",  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ml", "training", "production"],
    params={
        "data_path": "s3://data-bucket/training_data.parquet",
        "n_estimators": 100,
        "max_depth": 10,
        "accuracy_threshold": 0.8,
    },
) as dag:

    start = EmptyOperator(task_id="start")

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    preprocess = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    check_threshold = BranchPythonOperator(
        task_id="check_metrics_threshold",
        python_callable=check_metrics_threshold,
    )

    deploy = PythonOperator(
        task_id="deploy_model",
        python_callable=deploy_model,
    )

    skip = EmptyOperator(task_id="skip_deployment")

    end = EmptyOperator(
        task_id="end",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    start >> load >> preprocess >> train >> evaluate >> check_threshold
    check_threshold >> [deploy, skip] >> end
```

---

## Prefect

### Modern Flow-Based Pipeline

```python
from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd

@task(
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
)
def load_data(data_path: str) -> pd.DataFrame:
    """Load data with caching."""
    logger = get_run_logger()
    logger.info(f"Loading data from {data_path}")

    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df)} rows")

    return df

@task(retries=2)
def preprocess_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocess and split data."""
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    logger = get_run_logger()

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df["target"] = y_train.values

    test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_df["target"] = y_test.values

    logger.info(f"Train: {len(train_df)}, Test: {len(test_df)}")

    return train_df, test_df

@task
def train_model(
    train_df: pd.DataFrame,
    n_estimators: int = 100,
    max_depth: int = 10,
):
    """Train RandomForest model."""
    from sklearn.ensemble import RandomForestClassifier

    logger = get_run_logger()

    X = train_df.drop("target", axis=1)
    y = train_df["target"]

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
        n_jobs=-1,
    )

    logger.info("Training model...")
    model.fit(X, y)
    logger.info("Training complete")

    return model

@task
def evaluate_model(model, test_df: pd.DataFrame) -> dict:
    """Evaluate model and create artifact."""
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score,
        f1_score, classification_report
    )

    logger = get_run_logger()

    X = test_df.drop("target", axis=1)
    y = test_df["target"]

    predictions = model.predict(X)

    metrics = {
        "accuracy": accuracy_score(y, predictions),
        "precision": precision_score(y, predictions, average="weighted"),
        "recall": recall_score(y, predictions, average="weighted"),
        "f1_score": f1_score(y, predictions, average="weighted"),
    }

    logger.info(f"Metrics: {metrics}")

    # Create markdown artifact for Prefect UI
    report = classification_report(y, predictions)
    markdown = f"""
# Model Evaluation Report

## Metrics
| Metric | Value |
|--------|-------|
| Accuracy | {metrics['accuracy']:.4f} |
| Precision | {metrics['precision']:.4f} |
| Recall | {metrics['recall']:.4f} |
| F1 Score | {metrics['f1_score']:.4f} |

## Classification Report
```
{report}
```
"""
    create_markdown_artifact(
        key="model-evaluation",
        markdown=markdown,
        description="Model evaluation metrics",
    )

    return metrics

@task
def deploy_model(model, metrics: dict, threshold: float) -> bool:
    """Deploy model if metrics pass threshold."""
    import joblib
    from datetime import datetime

    logger = get_run_logger()

    if metrics["accuracy"] < threshold:
        logger.warning(
            f"Model accuracy {metrics['accuracy']:.4f} below threshold {threshold}"
        )
        return False

    # Save model
    model_path = f"/models/model_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.joblib"
    joblib.dump(model, model_path)
    logger.info(f"Model deployed to {model_path}")

    return True

@flow(
    name="ml-training-pipeline",
    description="End-to-end ML training pipeline",
    retries=1,
    retry_delay_seconds=300,
)
def ml_training_flow(
    data_path: str,
    n_estimators: int = 100,
    max_depth: int = 10,
    accuracy_threshold: float = 0.8,
) -> dict:
    """Main ML training flow."""
    logger = get_run_logger()
    logger.info("Starting ML training pipeline")

    # Load and preprocess
    df = load_data(data_path)
    train_df, test_df = preprocess_data(df)

    # Train and evaluate
    model = train_model(train_df, n_estimators, max_depth)
    metrics = evaluate_model(model, test_df)

    # Deploy if threshold met
    deployed = deploy_model(model, metrics, accuracy_threshold)

    return {
        "metrics": metrics,
        "deployed": deployed,
    }

# Deployment configuration
if __name__ == "__main__":
    from prefect.deployments import Deployment
    from prefect.server.schemas.schedules import CronSchedule

    deployment = Deployment.build_from_flow(
        flow=ml_training_flow,
        name="daily-training",
        schedule=CronSchedule(cron="0 2 * * *"),
        parameters={
            "data_path": "s3://data/training.parquet",
            "n_estimators": 100,
            "max_depth": 10,
            "accuracy_threshold": 0.8,
        },
        tags=["ml", "production"],
        work_queue_name="ml-queue",
    )

    deployment.apply()
```

---

## DAG Design Patterns

### Parallel Processing Pattern

```python
from prefect import flow, task, unmapped
from typing import List

@task
def process_partition(partition_id: int, data_path: str) -> dict:
    """Process single data partition."""
    # Process partition
    return {"partition_id": partition_id, "records_processed": 1000}

@task
def aggregate_results(results: List[dict]) -> dict:
    """Aggregate parallel processing results."""
    total_records = sum(r["records_processed"] for r in results)
    return {"total_records": total_records}

@flow
def parallel_processing_flow(data_path: str, num_partitions: int = 4):
    """Process data in parallel partitions."""

    # Map over partitions
    partition_results = process_partition.map(
        partition_id=range(num_partitions),
        data_path=unmapped(data_path),
    )

    # Aggregate results
    final_result = aggregate_results(partition_results)

    return final_result
```

### Conditional Branching Pattern

```python
from prefect import flow, task

@task
def check_data_quality(df) -> bool:
    """Check if data meets quality standards."""
    null_ratio = df.isnull().sum().sum() / df.size
    return null_ratio < 0.1

@task
def handle_poor_quality(df):
    """Handle data that fails quality checks."""
    # Impute, clean, or alert
    pass

@task
def process_good_quality(df):
    """Process data that passes quality checks."""
    pass

@flow
def conditional_flow(data_path: str):
    """Flow with conditional branching."""
    df = load_data(data_path)
    quality_ok = check_data_quality(df)

    if quality_ok:
        result = process_good_quality(df)
    else:
        result = handle_poor_quality(df)

    return result
```

### Error Handling Pattern

```python
from prefect import flow, task
from prefect.states import Failed

@task
def risky_operation():
    """Operation that might fail."""
    import random
    if random.random() < 0.3:
        raise ValueError("Random failure")
    return "success"

@task
def fallback_operation():
    """Fallback when primary fails."""
    return "fallback_result"

@task
def send_alert(error: Exception):
    """Send alert on failure."""
    # Send to Slack, PagerDuty, etc.
    pass

@flow
def resilient_flow():
    """Flow with error handling."""
    try:
        result = risky_operation()
    except Exception as e:
        send_alert(e)
        result = fallback_operation()

    return result
```

---

## Best Practices

### Pipeline Configuration

```yaml
# pipeline_config.yaml
pipeline:
  name: ml-training
  version: "1.0.0"
  description: "Production ML training pipeline"

stages:
  - name: load_data
    timeout: 300
    retries: 3

  - name: preprocess
    timeout: 600
    retries: 2
    depends_on: [load_data]

  - name: train
    timeout: 3600
    retries: 1
    depends_on: [preprocess]
    resources:
      cpu: 4
      memory: 16Gi
      gpu: 1

  - name: evaluate
    timeout: 300
    depends_on: [train]

  - name: deploy
    timeout: 300
    depends_on: [evaluate]
    condition: "evaluate.metrics.accuracy >= 0.8"

schedule:
  cron: "0 2 * * *"
  timezone: "UTC"

notifications:
  on_failure:
    - slack: "#ml-alerts"
    - email: ml-team@company.com
  on_success:
    - slack: "#ml-notifications"
```

### Idempotency Guidelines

```python
# Good: Idempotent operations
def process_data(run_id: str, data_path: str):
    """Idempotent data processing."""
    output_path = f"s3://processed/{run_id}/data.parquet"

    # Check if already processed
    if file_exists(output_path):
        return output_path

    # Process and save
    df = pd.read_parquet(data_path)
    processed = transform(df)
    processed.to_parquet(output_path)

    return output_path
```

---

## Related References

- `training-pipelines.md` - Training components for pipelines
- `experiment-tracking.md` - Logging pipeline runs
- `feature-engineering.md` - Feature pipeline components
- `model-validation.md` - Validation stages in pipelines

## Cross-Reference Skills

- **DevOps Engineer** - CI/CD for pipeline deployment
- **Kubernetes Specialist** - Running pipelines on K8s
- **Cloud Architect** - Cloud infrastructure for orchestration

---

## Reference: Training Pipelines

# Training Pipelines

---

## Overview

Training pipelines orchestrate the end-to-end model training process including data loading, distributed training, hyperparameter optimization, and artifact management. Production pipelines require reproducibility, scalability, and proper resource management.

## When to Use This Reference

- Setting up distributed training with PyTorch/TensorFlow
- Implementing hyperparameter tuning (Optuna, Ray Tune)
- Managing GPU/TPU resources for training
- Building reproducible training environments
- Creating checkpointing and fault-tolerant training

## When NOT to Use

- Quick model prototyping (use notebooks)
- Small models that fit in memory on single GPU
- One-off experiments without production requirements

---

## PyTorch Training Pipeline

### Complete Training Script

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import json

logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Training hyperparameters and settings."""
    model_name: str
    batch_size: int = 32
    learning_rate: float = 1e-4
    weight_decay: float = 0.01
    epochs: int = 10
    warmup_steps: int = 100
    max_grad_norm: float = 1.0
    seed: int = 42
    checkpoint_dir: str = "./checkpoints"
    log_every_n_steps: int = 100
    eval_every_n_steps: int = 500
    save_every_n_steps: int = 1000
    mixed_precision: bool = True
    gradient_accumulation_steps: int = 1

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d: dict) -> "TrainingConfig":
        return cls(**d)

class Trainer:
    """Production-grade PyTorch trainer."""

    def __init__(
        self,
        model: nn.Module,
        config: TrainingConfig,
        train_dataloader: DataLoader,
        eval_dataloader: Optional[DataLoader] = None,
        experiment_tracker=None,
    ):
        self.model = model
        self.config = config
        self.train_dataloader = train_dataloader
        self.eval_dataloader = eval_dataloader
        self.tracker = experiment_tracker

        self._setup_device()
        self._setup_training()
        self._setup_checkpointing()

    def _setup_device(self) -> None:
        """Configure device and move model."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

        if self.config.mixed_precision and self.device.type == "cuda":
            self.scaler = torch.amp.GradScaler("cuda")
        else:
            self.scaler = None

        logger.info(f"Training on device: {self.device}")

    def _setup_training(self) -> None:
        """Initialize optimizer and scheduler."""
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay,
        )

        total_steps = len(self.train_dataloader) * self.config.epochs
        self.scheduler = CosineAnnealingLR(
            self.optimizer,
            T_max=total_steps,
            eta_min=self.config.learning_rate * 0.01,
        )

        self.global_step = 0
        self.best_eval_loss = float("inf")

    def _setup_checkpointing(self) -> None:
        """Create checkpoint directory."""
        self.checkpoint_dir = Path(self.config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _set_seed(self) -> None:
        """Set random seeds for reproducibility."""
        import random
        import numpy as np

        torch.manual_seed(self.config.seed)
        torch.cuda.manual_seed_all(self.config.seed)
        np.random.seed(self.config.seed)
        random.seed(self.config.seed)
        torch.backends.cudnn.deterministic = True

    def train(self) -> dict:
        """Run training loop."""
        self._set_seed()
        self.model.train()

        metrics_history = []

        for epoch in range(self.config.epochs):
            epoch_loss = 0.0
            num_batches = 0

            for batch_idx, batch in enumerate(self.train_dataloader):
                loss = self._training_step(batch)
                epoch_loss += loss
                num_batches += 1

                if self.global_step % self.config.log_every_n_steps == 0:
                    self._log_metrics({
                        "train/loss": loss,
                        "train/lr": self.scheduler.get_last_lr()[0],
                        "train/epoch": epoch,
                    })

                if (
                    self.eval_dataloader
                    and self.global_step % self.config.eval_every_n_steps == 0
                ):
                    eval_metrics = self.evaluate()
                    self._log_metrics(eval_metrics)

                    if eval_metrics["eval/loss"] < self.best_eval_loss:
                        self.best_eval_loss = eval_metrics["eval/loss"]
                        self.save_checkpoint("best")

                if self.global_step % self.config.save_every_n_steps == 0:
                    self.save_checkpoint(f"step_{self.global_step}")

            avg_epoch_loss = epoch_loss / num_batches
            logger.info(f"Epoch {epoch}: avg_loss={avg_epoch_loss:.4f}")
            metrics_history.append({"epoch": epoch, "loss": avg_epoch_loss})

        self.save_checkpoint("final")

        return {
            "best_eval_loss": self.best_eval_loss,
            "final_train_loss": avg_epoch_loss,
            "total_steps": self.global_step,
            "metrics_history": metrics_history,
        }

    def _training_step(self, batch: dict) -> float:
        """Execute single training step."""
        batch = {k: v.to(self.device) for k, v in batch.items()}

        if self.scaler:
            with torch.amp.autocast("cuda"):
                outputs = self.model(**batch)
                loss = outputs.loss / self.config.gradient_accumulation_steps
            self.scaler.scale(loss).backward()
        else:
            outputs = self.model(**batch)
            loss = outputs.loss / self.config.gradient_accumulation_steps
            loss.backward()

        if (self.global_step + 1) % self.config.gradient_accumulation_steps == 0:
            if self.scaler:
                self.scaler.unscale_(self.optimizer)

            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                self.config.max_grad_norm,
            )

            if self.scaler:
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                self.optimizer.step()

            self.scheduler.step()
            self.optimizer.zero_grad()

        self.global_step += 1
        return loss.item() * self.config.gradient_accumulation_steps

    @torch.no_grad()
    def evaluate(self) -> dict:
        """Run evaluation loop."""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0

        for batch in self.eval_dataloader:
            batch = {k: v.to(self.device) for k, v in batch.items()}

            if self.scaler:
                with torch.amp.autocast("cuda"):
                    outputs = self.model(**batch)
            else:
                outputs = self.model(**batch)

            total_loss += outputs.loss.item()
            num_batches += 1

        self.model.train()

        return {
            "eval/loss": total_loss / num_batches,
            "eval/step": self.global_step,
        }

    def save_checkpoint(self, name: str) -> Path:
        """Save model checkpoint."""
        checkpoint_path = self.checkpoint_dir / name

        torch.save({
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict(),
            "global_step": self.global_step,
            "best_eval_loss": self.best_eval_loss,
            "config": self.config.to_dict(),
        }, checkpoint_path / "checkpoint.pt")

        # Save config separately for easy loading
        with open(checkpoint_path / "config.json", "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)

        logger.info(f"Saved checkpoint: {checkpoint_path}")
        return checkpoint_path

    def load_checkpoint(self, checkpoint_path: Path) -> None:
        """Load model checkpoint."""
        checkpoint = torch.load(checkpoint_path / "checkpoint.pt", map_location=self.device)

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        self.global_step = checkpoint["global_step"]
        self.best_eval_loss = checkpoint["best_eval_loss"]

        logger.info(f"Loaded checkpoint from step {self.global_step}")

    def _log_metrics(self, metrics: dict) -> None:
        """Log metrics to tracker and console."""
        if self.tracker:
            self.tracker.log_metrics(metrics, step=self.global_step)

        logger.info(f"Step {self.global_step}: {metrics}")
```

---

## Distributed Training

### PyTorch Distributed Data Parallel

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler
import os

def setup_distributed() -> tuple[int, int, int]:
    """Initialize distributed training environment."""
    if "RANK" in os.environ:
        rank = int(os.environ["RANK"])
        local_rank = int(os.environ["LOCAL_RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
    else:
        rank = 0
        local_rank = 0
        world_size = 1

    if world_size > 1:
        dist.init_process_group(
            backend="nccl",
            init_method="env://",
            world_size=world_size,
            rank=rank,
        )
        torch.cuda.set_device(local_rank)

    return rank, local_rank, world_size

def cleanup_distributed() -> None:
    """Cleanup distributed training."""
    if dist.is_initialized():
        dist.destroy_process_group()

class DistributedTrainer(Trainer):
    """Trainer with DDP support."""

    def __init__(self, *args, **kwargs):
        self.rank, self.local_rank, self.world_size = setup_distributed()
        super().__init__(*args, **kwargs)

    def _setup_device(self) -> None:
        """Configure device for distributed training."""
        if self.world_size > 1:
            self.device = torch.device(f"cuda:{self.local_rank}")
            self.model = self.model.to(self.device)
            self.model = DDP(
                self.model,
                device_ids=[self.local_rank],
                output_device=self.local_rank,
                find_unused_parameters=False,
            )
        else:
            super()._setup_device()

        if self.config.mixed_precision and self.device.type == "cuda":
            self.scaler = torch.amp.GradScaler("cuda")
        else:
            self.scaler = None

    def save_checkpoint(self, name: str) -> Path:
        """Only save on rank 0."""
        if self.rank == 0:
            return super().save_checkpoint(name)
        return None

    def _log_metrics(self, metrics: dict) -> None:
        """Only log on rank 0."""
        if self.rank == 0:
            super()._log_metrics(metrics)

def create_distributed_dataloader(
    dataset: Dataset,
    batch_size: int,
    world_size: int,
    rank: int,
    shuffle: bool = True,
) -> DataLoader:
    """Create DataLoader with distributed sampler."""
    sampler = DistributedSampler(
        dataset,
        num_replicas=world_size,
        rank=rank,
        shuffle=shuffle,
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=4,
        pin_memory=True,
        drop_last=True,
    )
```

### Launch Script

```bash
#!/bin/bash
# launch_distributed.sh

NUM_GPUS=4
MASTER_PORT=29500

torchrun \
    --nproc_per_node=$NUM_GPUS \
    --master_port=$MASTER_PORT \
    train.py \
    --config config/training_config.yaml
```

---

## Hyperparameter Tuning

### Optuna Integration

```python
import optuna
from optuna.trial import Trial
from optuna.integration import PyTorchLightningPruningCallback
import mlflow

def create_objective(
    train_dataset: Dataset,
    eval_dataset: Dataset,
    model_class: type,
) -> callable:
    """Create Optuna objective function."""

    def objective(trial: Trial) -> float:
        # Sample hyperparameters
        config = TrainingConfig(
            model_name="tuned_model",
            learning_rate=trial.suggest_float("lr", 1e-5, 1e-3, log=True),
            batch_size=trial.suggest_categorical("batch_size", [16, 32, 64]),
            weight_decay=trial.suggest_float("weight_decay", 1e-5, 1e-2, log=True),
            epochs=trial.suggest_int("epochs", 3, 10),
            warmup_steps=trial.suggest_int("warmup_steps", 0, 500),
        )

        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
        eval_loader = DataLoader(eval_dataset, batch_size=config.batch_size)

        # Create model
        model = model_class(
            hidden_size=trial.suggest_categorical("hidden_size", [128, 256, 512]),
            num_layers=trial.suggest_int("num_layers", 2, 6),
            dropout=trial.suggest_float("dropout", 0.1, 0.5),
        )

        # Train
        trainer = Trainer(
            model=model,
            config=config,
            train_dataloader=train_loader,
            eval_dataloader=eval_loader,
        )

        # Report intermediate values for pruning
        for epoch in range(config.epochs):
            trainer.train_epoch()
            eval_loss = trainer.evaluate()["eval/loss"]

            trial.report(eval_loss, epoch)

            if trial.should_prune():
                raise optuna.TrialPruned()

        return trainer.best_eval_loss

    return objective

def run_hyperparameter_search(
    train_dataset: Dataset,
    eval_dataset: Dataset,
    model_class: type,
    n_trials: int = 100,
    study_name: str = "hpo_study",
) -> optuna.Study:
    """Run hyperparameter optimization with Optuna."""

    # Create study with pruning
    pruner = optuna.pruners.MedianPruner(
        n_startup_trials=5,
        n_warmup_steps=3,
        interval_steps=1,
    )

    study = optuna.create_study(
        study_name=study_name,
        direction="minimize",
        pruner=pruner,
        storage=f"sqlite:///{study_name}.db",
        load_if_exists=True,
    )

    objective = create_objective(train_dataset, eval_dataset, model_class)

    study.optimize(
        objective,
        n_trials=n_trials,
        timeout=3600 * 12,  # 12 hours
        n_jobs=1,  # Sequential for GPU
        show_progress_bar=True,
    )

    # Log best results
    logger.info(f"Best trial: {study.best_trial.params}")
    logger.info(f"Best value: {study.best_value}")

    return study
```

### Ray Tune Integration

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.optuna import OptunaSearch
from ray.air import RunConfig, CheckpointConfig

def train_fn(config: dict) -> None:
    """Training function for Ray Tune."""
    from ray.train import report, get_checkpoint

    training_config = TrainingConfig(
        model_name="ray_tune_model",
        learning_rate=config["lr"],
        batch_size=config["batch_size"],
        weight_decay=config["weight_decay"],
        epochs=config["epochs"],
    )

    # Build model and dataloaders
    model = build_model(config["hidden_size"], config["num_layers"])
    train_loader, eval_loader = build_dataloaders(config["batch_size"])

    trainer = Trainer(
        model=model,
        config=training_config,
        train_dataloader=train_loader,
        eval_dataloader=eval_loader,
    )

    # Resume from checkpoint if available
    checkpoint = get_checkpoint()
    if checkpoint:
        with checkpoint.as_directory() as checkpoint_dir:
            trainer.load_checkpoint(Path(checkpoint_dir))

    for epoch in range(training_config.epochs):
        trainer.train_epoch()
        metrics = trainer.evaluate()

        # Report metrics to Ray Tune
        report(
            {"loss": metrics["eval/loss"], "epoch": epoch},
            checkpoint=Checkpoint.from_directory(trainer.checkpoint_dir),
        )

def run_ray_tune(num_samples: int = 50) -> tune.ResultGrid:
    """Run hyperparameter search with Ray Tune."""

    search_space = {
        "lr": tune.loguniform(1e-5, 1e-3),
        "batch_size": tune.choice([16, 32, 64]),
        "weight_decay": tune.loguniform(1e-5, 1e-2),
        "hidden_size": tune.choice([128, 256, 512]),
        "num_layers": tune.randint(2, 7),
        "epochs": 10,
    }

    scheduler = ASHAScheduler(
        metric="loss",
        mode="min",
        max_t=10,
        grace_period=2,
        reduction_factor=3,
    )

    tuner = tune.Tuner(
        tune.with_resources(train_fn, {"gpu": 1}),
        param_space=search_space,
        tune_config=tune.TuneConfig(
            num_samples=num_samples,
            scheduler=scheduler,
            search_alg=OptunaSearch(),
        ),
        run_config=RunConfig(
            name="hpo_experiment",
            checkpoint_config=CheckpointConfig(
                num_to_keep=3,
                checkpoint_frequency=1,
            ),
        ),
    )

    results = tuner.fit()
    best_result = results.get_best_result("loss", "min")

    logger.info(f"Best config: {best_result.config}")
    logger.info(f"Best loss: {best_result.metrics['loss']}")

    return results
```

---

## Resource Management

### GPU Memory Optimization

```python
import torch
from contextlib import contextmanager

@contextmanager
def gpu_memory_manager():
    """Context manager for GPU memory cleanup."""
    try:
        yield
    finally:
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def get_gpu_memory_usage() -> dict:
    """Get current GPU memory statistics."""
    if not torch.cuda.is_available():
        return {"available": False}

    return {
        "allocated": torch.cuda.memory_allocated() / 1e9,
        "reserved": torch.cuda.memory_reserved() / 1e9,
        "max_allocated": torch.cuda.max_memory_allocated() / 1e9,
    }

class GradientCheckpointing:
    """Enable gradient checkpointing for memory efficiency."""

    @staticmethod
    def enable(model: nn.Module, checkpoint_layers: list[str] = None) -> None:
        """Enable gradient checkpointing on specified layers."""
        if hasattr(model, "gradient_checkpointing_enable"):
            model.gradient_checkpointing_enable()
            return

        # Manual checkpointing for custom models
        from torch.utils.checkpoint import checkpoint

        def create_custom_forward(module):
            def custom_forward(*inputs):
                return checkpoint(module._original_forward, *inputs, use_reentrant=False)
            return custom_forward

        for name, module in model.named_modules():
            if checkpoint_layers and name not in checkpoint_layers:
                continue
            if hasattr(module, "forward"):
                module._original_forward = module.forward
                module.forward = create_custom_forward(module)
```

### Batch Size Finder

```python
def find_optimal_batch_size(
    model: nn.Module,
    sample_batch: dict,
    device: torch.device,
    min_batch_size: int = 1,
    max_batch_size: int = 256,
) -> int:
    """Find maximum batch size that fits in GPU memory."""

    model = model.to(device)
    optimal_batch_size = min_batch_size

    for batch_size in [2**i for i in range(int(np.log2(max_batch_size)) + 1)]:
        if batch_size < min_batch_size:
            continue

        try:
            # Create batch of target size
            batch = {
                k: v.repeat(batch_size // v.size(0) + 1, *[1] * (v.dim() - 1))[:batch_size]
                for k, v in sample_batch.items()
            }
            batch = {k: v.to(device) for k, v in batch.items()}

            # Forward pass
            with torch.amp.autocast("cuda"):
                outputs = model(**batch)
                loss = outputs.loss

            # Backward pass
            loss.backward()
            model.zero_grad()

            torch.cuda.empty_cache()
            optimal_batch_size = batch_size

        except RuntimeError as e:
            if "out of memory" in str(e):
                torch.cuda.empty_cache()
                break
            raise

    logger.info(f"Optimal batch size: {optimal_batch_size}")
    return optimal_batch_size
```

---

## Best Practices

### Training Configuration Management

```yaml
# config/training_config.yaml
model:
  name: transformer
  hidden_size: 512
  num_layers: 6
  dropout: 0.1

training:
  batch_size: 32
  learning_rate: 1e-4
  weight_decay: 0.01
  epochs: 10
  mixed_precision: true
  gradient_accumulation_steps: 4

distributed:
  enabled: true
  backend: nccl

checkpointing:
  save_every_n_steps: 1000
  keep_n_checkpoints: 3

logging:
  log_every_n_steps: 100
  eval_every_n_steps: 500
```

### Reproducibility Checklist

```python
def ensure_reproducibility(seed: int) -> None:
    """Set all random seeds for reproducibility."""
    import random
    import numpy as np
    import os

    # Python
    random.seed(seed)

    # NumPy
    np.random.seed(seed)

    # PyTorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # CUDA
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Environment
    os.environ["PYTHONHASHSEED"] = str(seed)

    logger.info(f"Set all random seeds to {seed}")
```

---

## Related References

- `feature-engineering.md` - Feature preparation for training
- `experiment-tracking.md` - Logging training metrics
- `pipeline-orchestration.md` - Orchestrating training pipelines
- `model-validation.md` - Validating trained models

## Cross-Reference Skills

- **DevOps Engineer** - CI/CD for training pipelines
- **Kubernetes Specialist** - K8s-based training infrastructure
