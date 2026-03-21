---
title: "Modal"
description: "Run Python code in the cloud with serverless containers, GPUs, and autoscaling. Use when deploying ML models, running batch processing jobs, scheduling compute-intensive tasks, or serving APIs that require GPU acceleration or dynamic scaling."
category: "devops"
source: "community"
author: "Community"
tags: ["modal"]
date: 2026-03-20
---

# Modal

## Overview

Modal is a serverless platform for running Python code in the cloud with minimal configuration. Execute functions on powerful GPUs, scale automatically to thousands of containers, and pay only for compute used.

Modal is particularly suited for AI/ML workloads, high-performance batch processing, scheduled jobs, GPU inference, and serverless APIs. Sign up for free at https://modal.com and receive $30/month in credits.

## When to Use This Skill

Use Modal for:
- Deploying and serving ML models (LLMs, image generation, embedding models)
- Running GPU-accelerated computation (training, inference, rendering)
- Batch processing large datasets in parallel
- Scheduling compute-intensive jobs (daily data processing, model training)
- Building serverless APIs that need automatic scaling
- Scientific computing requiring distributed compute or specialized hardware

## Authentication and Setup

Modal requires authentication via API token.

### Initial Setup

```bash
# Install Modal
uv uv pip install modal

# Authenticate (opens browser for login)
modal token new
```

This creates a token stored in `~/.modal.toml`. The token authenticates all Modal operations.

### Verify Setup

```python
import modal

app = modal.App("test-app")

@app.function()
def hello():
    print("Modal is working!")
```

Run with: `modal run script.py`

## Core Capabilities

Modal provides serverless Python execution through Functions that run in containers. Define compute requirements, dependencies, and scaling behavior declaratively.

### 1. Define Container Images

Specify dependencies and environment for functions using Modal Images.

```python
import modal

# Basic image with Python packages
image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("torch", "transformers", "numpy")
)

app = modal.App("ml-app", image=image)
```

**Common patterns:**
- Install Python packages: `.uv_pip_install("pandas", "scikit-learn")`
- Install system packages: `.apt_install("ffmpeg", "git")`
- Use existing Docker images: `modal.Image.from_registry("nvidia/cuda:12.1.0-base")`
- Add local code: `.add_local_python_source("my_module")`

See `references/images.md` for comprehensive image building documentation.

### 2. Create Functions

Define functions that run in the cloud with the `@app.function()` decorator.

```python
@app.function()
def process_data(file_path: str):
    import pandas as pd
    df = pd.read_csv(file_path)
    return df.describe()
```

**Call functions:**
```python
# From local entrypoint
@app.local_entrypoint()
def main():
    result = process_data.remote("data.csv")
    print(result)
```

Run with: `modal run script.py`

See `references/functions.md` for function patterns, deployment, and parameter handling.

### 3. Request GPUs

Attach GPUs to functions for accelerated computation.

```python
@app.function(gpu="H100")
def train_model():
    import torch
    assert torch.cuda.is_available()
    # GPU-accelerated code here
```

**Available GPU types:**
- `T4`, `L4` - Cost-effective inference
- `A10`, `A100`, `A100-80GB` - Standard training/inference
- `L40S` - Excellent cost/performance balance (48GB)
- `H100`, `H200` - High-performance training
- `B200` - Flagship performance (most powerful)

**Request multiple GPUs:**
```python
@app.function(gpu="H100:8")  # 8x H100 GPUs
def train_large_model():
    pass
```

See `references/gpu.md` for GPU selection guidance, CUDA setup, and multi-GPU configuration.

### 4. Configure Resources

Request CPU cores, memory, and disk for functions.

```python
@app.function(
    cpu=8.0,           # 8 physical cores
    memory=32768,      # 32 GiB RAM
    ephemeral_disk=10240  # 10 GiB disk
)
def memory_intensive_task():
    pass
```

Default allocation: 0.125 CPU cores, 128 MiB memory. Billing based on reservation or actual usage, whichever is higher.

See `references/resources.md` for resource limits and billing details.

### 5. Scale Automatically

Modal autoscales functions from zero to thousands of containers based on demand.

**Process inputs in parallel:**
```python
@app.function()
def analyze_sample(sample_id: int):
    # Process single sample
    return result

@app.local_entrypoint()
def main():
    sample_ids = range(1000)
    # Automatically parallelized across containers
    results = list(analyze_sample.map(sample_ids))
```

**Configure autoscaling:**
```python
@app.function(
    max_containers=100,      # Upper limit
    min_containers=2,        # Keep warm
    buffer_containers=5      # Idle buffer for bursts
)
def inference():
    pass
```

See `references/scaling.md` for autoscaling configuration, concurrency, and scaling limits.

### 6. Store Data Persistently

Use Volumes for persistent storage across function invocations.

```python
volume = modal.Volume.from_name("my-data", create_if_missing=True)

@app.function(volumes={"/data": volume})
def save_results(data):
    with open("/data/results.txt", "w") as f:
        f.write(data)
    volume.commit()  # Persist changes
```

Volumes persist data between runs, store model weights, cache datasets, and share data between functions.

See `references/volumes.md` for volume management, commits, and caching patterns.

### 7. Manage Secrets

Store API keys and credentials securely using Modal Secrets.

```python
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    import os
    token = os.environ["HF_TOKEN"]
    # Use token for authentication
```

**Create secrets in Modal dashboard or via CLI:**
```bash
modal secret create my-secret KEY=value API_TOKEN=xyz
```

See `references/secrets.md` for secret management and authentication patterns.

### 8. Deploy Web Endpoints

Serve HTTP endpoints, APIs, and webhooks with `@modal.web_endpoint()`.

```python
@app.function()
@modal.web_endpoint(method="POST")
def predict(data: dict):
    # Process request
    result = model.predict(data["input"])
    return {"prediction": result}
```

**Deploy with:**
```bash
modal deploy script.py
```

Modal provides HTTPS URL for the endpoint.

See `references/web-endpoints.md` for FastAPI integration, streaming, authentication, and WebSocket support.

### 9. Schedule Jobs

Run functions on a schedule with cron expressions.

```python
@app.function(schedule=modal.Cron("0 2 * * *"))  # Daily at 2 AM
def daily_backup():
    # Backup data
    pass

@app.function(schedule=modal.Period(hours=4))  # Every 4 hours
def refresh_cache():
    # Update cache
    pass
```

Scheduled functions run automatically without manual invocation.

See `references/scheduled-jobs.md` for cron syntax, timezone configuration, and monitoring.

## Common Workflows

### Deploy ML Model for Inference

```python
import modal

# Define dependencies
image = modal.Image.debian_slim().uv_pip_install("torch", "transformers")
app = modal.App("llm-inference", image=image)

# Download model at build time
@app.function()
def download_model():
    from transformers import AutoModel
    AutoModel.from_pretrained("bert-base-uncased")

# Serve model
@app.cls(gpu="L40S")
class Model:
    @modal.enter()
    def load_model(self):
        from transformers import pipeline
        self.pipe = pipeline("text-classification", device="cuda")

    @modal.method()
    def predict(self, text: str):
        return self.pipe(text)

@app.local_entrypoint()
def main():
    model = Model()
    result = model.predict.remote("Modal is great!")
    print(result)
```

### Batch Process Large Dataset

```python
@app.function(cpu=2.0, memory=4096)
def process_file(file_path: str):
    import pandas as pd
    df = pd.read_csv(file_path)
    # Process data
    return df.shape[0]

@app.local_entrypoint()
def main():
    files = ["file1.csv", "file2.csv", ...]  # 1000s of files
    # Automatically parallelized across containers
    for count in process_file.map(files):
        print(f"Processed {count} rows")
```

### Train Model on GPU

```python
@app.function(
    gpu="A100:2",      # 2x A100 GPUs
    timeout=3600       # 1 hour timeout
)
def train_model(config: dict):
    import torch
    # Multi-GPU training code
    model = create_model(config)
    train(model)
    return metrics
```

## Reference Documentation

Detailed documentation for specific features:

- **`references/getting-started.md`** - Authentication, setup, basic concepts
- **`references/images.md`** - Image building, dependencies, Dockerfiles
- **`references/functions.md`** - Function patterns, deployment, parameters
- **`references/gpu.md`** - GPU types, CUDA, multi-GPU configuration
- **`references/resources.md`** - CPU, memory, disk management
- **`references/scaling.md`** - Autoscaling, parallel execution, concurrency
- **`references/volumes.md`** - Persistent storage, data management
- **`references/secrets.md`** - Environment variables, authentication
- **`references/web-endpoints.md`** - APIs, webhooks, endpoints
- **`references/scheduled-jobs.md`** - Cron jobs, periodic tasks
- **`references/examples.md`** - Common patterns for scientific computing

## Best Practices

1. **Pin dependencies** in `.uv_pip_install()` for reproducible builds
2. **Use appropriate GPU types** - L40S for inference, H100/A100 for training
3. **Leverage caching** - Use Volumes for model weights and datasets
4. **Configure autoscaling** - Set `max_containers` and `min_containers` based on workload
5. **Import packages in function body** if not available locally
6. **Use `.map()` for parallel processing** instead of sequential loops
7. **Store secrets securely** - Never hardcode API keys
8. **Monitor costs** - Check Modal dashboard for usage and billing

## Troubleshooting

**"Module not found" errors:**
- Add packages to image with `.uv_pip_install("package-name")`
- Import packages inside function body if not available locally

**GPU not detected:**
- Verify GPU specification: `@app.function(gpu="A100")`
- Check CUDA availability: `torch.cuda.is_available()`

**Function timeout:**
- Increase timeout: `@app.function(timeout=3600)`
- Default timeout is 5 minutes

**Volume changes not persisting:**
- Call `volume.commit()` after writing files
- Verify volume mounted correctly in function decorator

For additional help, see Modal documentation at https://modal.com/docs or join Modal Slack community.

---

## Reference: Api_Reference

# Reference Documentation for Modal

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices

---

## Reference: Examples

# Common Patterns for Scientific Computing

## Machine Learning Model Inference

### Basic Model Serving

```python
import modal

app = modal.App("ml-inference")

image = (
    modal.Image.debian_slim()
    .uv_pip_install("torch", "transformers")
)

@app.cls(
    image=image,
    gpu="L40S",
)
class Model:
    @modal.enter()
    def load_model(self):
        from transformers import AutoModel, AutoTokenizer
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    @modal.method()
    def predict(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).tolist()

@app.local_entrypoint()
def main():
    model = Model()
    result = model.predict.remote("Hello world")
    print(result)
```

### Model Serving with Volume

```python
volume = modal.Volume.from_name("models", create_if_missing=True)
MODEL_PATH = "/models"

@app.cls(
    image=image,
    gpu="A100",
    volumes={MODEL_PATH: volume}
)
class ModelServer:
    @modal.enter()
    def load(self):
        import torch
        self.model = torch.load(f"{MODEL_PATH}/model.pt")
        self.model.eval()

    @modal.method()
    def infer(self, data):
        import torch
        with torch.no_grad():
            return self.model(torch.tensor(data)).tolist()
```

## Batch Processing

### Parallel Data Processing

```python
@app.function(
    image=modal.Image.debian_slim().uv_pip_install("pandas", "numpy"),
    cpu=2.0,
    memory=8192
)
def process_batch(batch_id: int):
    import pandas as pd

    # Load batch
    df = pd.read_csv(f"s3://bucket/batch_{batch_id}.csv")

    # Process
    result = df.apply(lambda row: complex_calculation(row), axis=1)

    # Save result
    result.to_csv(f"s3://bucket/results_{batch_id}.csv")

    return batch_id

@app.local_entrypoint()
def main():
    # Process 100 batches in parallel
    results = list(process_batch.map(range(100)))
    print(f"Processed {len(results)} batches")
```

### Batch Processing with Progress

```python
@app.function()
def process_item(item_id: int):
    # Expensive processing
    result = compute_something(item_id)
    return result

@app.local_entrypoint()
def main():
    items = list(range(1000))

    print(f"Processing {len(items)} items...")
    results = []
    for i, result in enumerate(process_item.map(items)):
        results.append(result)
        if (i + 1) % 100 == 0:
            print(f"Completed {i + 1}/{len(items)}")

    print("All items processed!")
```

## Data Analysis Pipeline

### ETL Pipeline

```python
volume = modal.Volume.from_name("data-pipeline")
DATA_PATH = "/data"

@app.function(
    image=modal.Image.debian_slim().uv_pip_install("pandas", "polars"),
    volumes={DATA_PATH: volume},
    cpu=4.0,
    memory=16384
)
def extract_transform_load():
    import polars as pl

    # Extract
    raw_data = pl.read_csv(f"{DATA_PATH}/raw/*.csv")

    # Transform
    transformed = (
        raw_data
        .filter(pl.col("value") > 0)
        .group_by("category")
        .agg([
            pl.col("value").mean().alias("avg_value"),
            pl.col("value").sum().alias("total_value")
        ])
    )

    # Load
    transformed.write_parquet(f"{DATA_PATH}/processed/data.parquet")
    volume.commit()

    return transformed.shape

@app.function(schedule=modal.Cron("0 2 * * *"))
def daily_pipeline():
    result = extract_transform_load.remote()
    print(f"Processed data shape: {result}")
```

## GPU-Accelerated Computing

### Distributed Training

```python
@app.function(
    gpu="A100:2",
    image=modal.Image.debian_slim().uv_pip_install("torch", "accelerate"),
    timeout=7200,
)
def train_model():
    import torch
    from torch.nn.parallel import DataParallel

    # Load data
    train_loader = get_data_loader()

    # Initialize model
    model = MyModel()
    model = DataParallel(model)
    model = model.cuda()

    # Train
    optimizer = torch.optim.Adam(model.parameters())
    for epoch in range(10):
        for batch in train_loader:
            loss = train_step(model, batch, optimizer)
            print(f"Epoch {epoch}, Loss: {loss}")

    return "Training complete"
```

### GPU Batch Inference

```python
@app.function(
    gpu="L40S",
    image=modal.Image.debian_slim().uv_pip_install("torch", "transformers")
)
def batch_inference(texts: list[str]):
    from transformers import pipeline

    classifier = pipeline("sentiment-analysis", device=0)
    results = classifier(texts, batch_size=32)

    return results

@app.local_entrypoint()
def main():
    # Process 10,000 texts
    texts = load_texts()

    # Split into chunks of 100
    chunks = [texts[i:i+100] for i in range(0, len(texts), 100)]

    # Process in parallel on multiple GPUs
    all_results = []
    for results in batch_inference.map(chunks):
        all_results.extend(results)

    print(f"Processed {len(all_results)} texts")
```

## Scientific Computing

### Molecular Dynamics Simulation

```python
@app.function(
    image=modal.Image.debian_slim().apt_install("openmpi-bin").uv_pip_install("mpi4py", "numpy"),
    cpu=16.0,
    memory=65536,
    timeout=7200,
)
def run_simulation(config: dict):
    import numpy as np

    # Initialize system
    positions = initialize_positions(config["n_particles"])
    velocities = initialize_velocities(config["temperature"])

    # Run MD steps
    for step in range(config["n_steps"]):
        forces = compute_forces(positions)
        velocities += forces * config["dt"]
        positions += velocities * config["dt"]

        if step % 1000 == 0:
            energy = compute_energy(positions, velocities)
            print(f"Step {step}, Energy: {energy}")

    return positions, velocities
```

### Distributed Monte Carlo

```python
@app.function(cpu=2.0)
def monte_carlo_trial(trial_id: int, n_samples: int):
    import random

    count = sum(1 for _ in range(n_samples)
                if random.random()**2 + random.random()**2 <= 1)

    return count

@app.local_entrypoint()
def estimate_pi():
    n_trials = 100
    n_samples_per_trial = 1_000_000

    # Run trials in parallel
    results = list(monte_carlo_trial.map(
        range(n_trials),
        [n_samples_per_trial] * n_trials
    ))

    total_count = sum(results)
    total_samples = n_trials * n_samples_per_trial

    pi_estimate = 4 * total_count / total_samples
    print(f"Estimated π = {pi_estimate}")
```

## Data Processing with Volumes

### Image Processing Pipeline

```python
volume = modal.Volume.from_name("images")
IMAGE_PATH = "/images"

@app.function(
    image=modal.Image.debian_slim().uv_pip_install("Pillow", "numpy"),
    volumes={IMAGE_PATH: volume}
)
def process_image(filename: str):
    from PIL import Image
    import numpy as np

    # Load image
    img = Image.open(f"{IMAGE_PATH}/raw/{filename}")

    # Process
    img_array = np.array(img)
    processed = apply_filters(img_array)

    # Save
    result_img = Image.fromarray(processed)
    result_img.save(f"{IMAGE_PATH}/processed/{filename}")

    return filename

@app.function(volumes={IMAGE_PATH: volume})
def process_all_images():
    import os

    # Get all images
    filenames = os.listdir(f"{IMAGE_PATH}/raw")

    # Process in parallel
    results = list(process_image.map(filenames))

    volume.commit()
    return f"Processed {len(results)} images"
```

## Web API for Scientific Computing

```python
image = modal.Image.debian_slim().uv_pip_install("fastapi[standard]", "numpy", "scipy")

@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
def compute_statistics(data: dict):
    import numpy as np
    from scipy import stats

    values = np.array(data["values"])

    return {
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "skewness": float(stats.skew(values)),
        "kurtosis": float(stats.kurtosis(values))
    }
```

## Scheduled Data Collection

```python
@app.function(
    schedule=modal.Cron("*/30 * * * *"),  # Every 30 minutes
    secrets=[modal.Secret.from_name("api-keys")],
    volumes={"/data": modal.Volume.from_name("sensor-data")}
)
def collect_sensor_data():
    import requests
    import json
    from datetime import datetime

    # Fetch from API
    response = requests.get(
        "https://api.example.com/sensors",
        headers={"Authorization": f"Bearer {os.environ['API_KEY']}"}
    )

    data = response.json()

    # Save with timestamp
    timestamp = datetime.now().isoformat()
    with open(f"/data/{timestamp}.json", "w") as f:
        json.dump(data, f)

    volume.commit()

    return f"Collected {len(data)} sensor readings"
```

## Best Practices

### Use Classes for Stateful Workloads

```python
@app.cls(gpu="A100")
class ModelService:
    @modal.enter()
    def setup(self):
        # Load once, reuse across requests
        self.model = load_heavy_model()

    @modal.method()
    def predict(self, x):
        return self.model(x)
```

### Batch Similar Workloads

```python
@app.function()
def process_many(items: list):
    # More efficient than processing one at a time
    return [process(item) for item in items]
```

### Use Volumes for Large Datasets

```python
# Store large datasets in volumes, not in image
volume = modal.Volume.from_name("dataset")

@app.function(volumes={"/data": volume})
def train():
    data = load_from_volume("/data/training.parquet")
    model = train_model(data)
```

### Profile Before Scaling to GPUs

```python
# Test on CPU first
@app.function(cpu=4.0)
def test_pipeline():
    ...

# Then scale to GPU if needed
@app.function(gpu="A100")
def gpu_pipeline():
    ...
```

---

## Reference: Functions

# Modal Functions

## Basic Function Definition

Decorate Python functions with `@app.function()`:

```python
import modal

app = modal.App(name="my-app")

@app.function()
def my_function():
    print("Hello from Modal!")
    return "result"
```

## Calling Functions

### Remote Execution

Call `.remote()` to run on Modal:

```python
@app.local_entrypoint()
def main():
    result = my_function.remote()
    print(result)
```

### Local Execution

Call `.local()` to run locally (useful for testing):

```python
result = my_function.local()
```

## Function Parameters

Functions accept standard Python arguments:

```python
@app.function()
def process(x: int, y: str):
    return f"{y}: {x * 2}"

@app.local_entrypoint()
def main():
    result = process.remote(42, "answer")
```

## Deployment

### Ephemeral Apps

Run temporarily:
```bash
modal run script.py
```

### Deployed Apps

Deploy persistently:
```bash
modal deploy script.py
```

Access deployed functions from other code:

```python
f = modal.Function.from_name("my-app", "my_function")
result = f.remote(args)
```

## Entrypoints

### Local Entrypoint

Code that runs on local machine:

```python
@app.local_entrypoint()
def main():
    result = my_function.remote()
    print(result)
```

### Remote Entrypoint

Use `@app.function()` without local_entrypoint - runs entirely on Modal:

```python
@app.function()
def train_model():
    # All code runs in Modal
    ...
```

Invoke with:
```bash
modal run script.py::app.train_model
```

## Argument Parsing

Entrypoints with primitive type arguments get automatic CLI parsing:

```python
@app.local_entrypoint()
def main(foo: int, bar: str):
    some_function.remote(foo, bar)
```

Run with:
```bash
modal run script.py --foo 1 --bar "hello"
```

For custom parsing, accept variable-length arguments:

```python
import argparse

@app.function()
def train(*arglist):
    parser = argparse.ArgumentParser()
    parser.add_argument("--foo", type=int)
    args = parser.parse_args(args=arglist)
```

## Function Configuration

Common parameters:

```python
@app.function(
    image=my_image,           # Custom environment
    gpu="A100",               # GPU type
    cpu=2.0,                  # CPU cores
    memory=4096,              # Memory in MB
    timeout=3600,             # Timeout in seconds
    retries=3,                # Number of retries
    secrets=[my_secret],      # Environment secrets
    volumes={"/data": vol},   # Persistent storage
)
def my_function():
    ...
```

## Parallel Execution

### Map

Run function on multiple inputs in parallel:

```python
@app.function()
def evaluate_model(x):
    return x ** 2

@app.local_entrypoint()
def main():
    inputs = list(range(100))
    for result in evaluate_model.map(inputs):
        print(result)
```

### Starmap

For functions with multiple arguments:

```python
@app.function()
def add(a, b):
    return a + b

@app.local_entrypoint()
def main():
    results = list(add.starmap([(1, 2), (3, 4)]))
    # [3, 7]
```

### Exception Handling

```python
results = my_func.map(
    range(3),
    return_exceptions=True,
    wrap_returned_exceptions=False
)
# [0, 1, Exception('error')]
```

## Async Functions

Define async functions:

```python
@app.function()
async def async_function(x: int):
    await asyncio.sleep(1)
    return x * 2

@app.local_entrypoint()
async def main():
    result = await async_function.remote.aio(42)
```

## Generator Functions

Return iterators for streaming results:

```python
@app.function()
def generate_data():
    for i in range(10):
        yield i

@app.local_entrypoint()
def main():
    for value in generate_data.remote_gen():
        print(value)
```

## Spawning Functions

Submit functions for background execution:

```python
@app.function()
def process_job(data):
    # Long-running job
    return result

@app.local_entrypoint()
def main():
    # Spawn without waiting
    call = process_job.spawn(data)

    # Get result later
    result = call.get(timeout=60)
```

## Programmatic Execution

Run apps programmatically:

```python
def main():
    with modal.enable_output():
        with app.run():
            result = some_function.remote()
```

## Specifying Entrypoint

With multiple functions, specify which to run:

```python
@app.function()
def f():
    print("Function f")

@app.function()
def g():
    print("Function g")
```

Run specific function:
```bash
modal run script.py::app.f
modal run script.py::app.g
```

---

## Reference: Getting Started

# Getting Started with Modal

## Sign Up

Sign up for free at https://modal.com and get $30/month of credits.

## Authentication

Set up authentication using the Modal CLI:

```bash
modal token new
```

This creates credentials in `~/.modal.toml`. Alternatively, set environment variables:
- `MODAL_TOKEN_ID`
- `MODAL_TOKEN_SECRET`

## Basic Concepts

### Modal is Serverless

Modal is a serverless platform - only pay for resources used and spin up containers on demand in seconds.

### Core Components

**App**: Represents an application running on Modal, grouping one or more Functions for atomic deployment.

**Function**: Acts as an independent unit that scales up and down independently. No containers run (and no charges) when there are no live inputs.

**Image**: The environment code runs in - a container snapshot with dependencies installed.

## First Modal App

Create a file `hello_modal.py`:

```python
import modal

app = modal.App(name="hello-modal")

@app.function()
def hello():
    print("Hello from Modal!")
    return "success"

@app.local_entrypoint()
def main():
    hello.remote()
```

Run with:
```bash
modal run hello_modal.py
```

## Running Apps

### Ephemeral Apps (Development)

Run temporarily with `modal run`:
```bash
modal run script.py
```

The app stops when the script exits. Use `--detach` to keep running after client exits.

### Deployed Apps (Production)

Deploy persistently with `modal deploy`:
```bash
modal deploy script.py
```

View deployed apps at https://modal.com/apps or with:
```bash
modal app list
```

Stop deployed apps:
```bash
modal app stop app-name
```

## Key Features

- **Fast prototyping**: Write Python, run on GPUs in seconds
- **Serverless APIs**: Create web endpoints with a decorator
- **Scheduled jobs**: Run cron jobs in the cloud
- **GPU inference**: Access T4, L4, A10, A100, H100, H200, B200 GPUs
- **Distributed volumes**: Persistent storage for ML models
- **Sandboxes**: Secure containers for untrusted code

---

## Reference: Gpu

# GPU Acceleration on Modal

## Quick Start

Run functions on GPUs with the `gpu` parameter:

```python
import modal

image = modal.Image.debian_slim().pip_install("torch")
app = modal.App(image=image)

@app.function(gpu="A100")
def run():
    import torch
    assert torch.cuda.is_available()
```

## Available GPU Types

Modal supports the following GPUs:

- `T4` - Entry-level GPU
- `L4` - Balanced performance and cost
- `A10` - Up to 4 GPUs, 96 GB total
- `A100` - 40GB or 80GB variants
- `A100-40GB` - Specific 40GB variant
- `A100-80GB` - Specific 80GB variant
- `L40S` - 48 GB, excellent for inference
- `H100` / `H100!` - Top-tier Hopper architecture
- `H200` - Improved Hopper with more memory
- `B200` - Latest Blackwell architecture

See https://modal.com/pricing for pricing.

## GPU Count

Request multiple GPUs per container with `:n` syntax:

```python
@app.function(gpu="H100:8")
def run_llama_405b():
    # 8 H100 GPUs available
    ...
```

Supported counts:
- B200, H200, H100, A100, L4, T4, L40S: up to 8 GPUs (up to 1,536 GB)
- A10: up to 4 GPUs (up to 96 GB)

Note: Requesting >2 GPUs may result in longer wait times.

## GPU Selection Guide

**For Inference (Recommended)**: Start with L40S
- Excellent cost/performance
- 48 GB memory
- Good for LLaMA, Stable Diffusion, etc.

**For Training**: Consider H100 or A100
- High compute throughput
- Large memory for batch processing

**For Memory-Bound Tasks**: H200 or A100-80GB
- More memory capacity
- Better for large models

## B200 GPUs

NVIDIA's flagship Blackwell chip:

```python
@app.function(gpu="B200:8")
def run_deepseek():
    # Most powerful option
    ...
```

## H200 and H100 GPUs

Hopper architecture GPUs with excellent software support:

```python
@app.function(gpu="H100")
def train():
    ...
```

### Automatic H200 Upgrades

Modal may upgrade `gpu="H100"` to H200 at no extra cost. H200 provides:
- 141 GB memory (vs 80 GB for H100)
- 4.8 TB/s bandwidth (vs 3.35 TB/s)

To avoid automatic upgrades (e.g., for benchmarking):
```python
@app.function(gpu="H100!")
def benchmark():
    ...
```

## A100 GPUs

Ampere architecture with 40GB or 80GB variants:

```python
# May be automatically upgraded to 80GB
@app.function(gpu="A100")
def qwen_7b():
    ...

# Specific variants
@app.function(gpu="A100-40GB")
def model_40gb():
    ...

@app.function(gpu="A100-80GB")
def llama_70b():
    ...
```

## GPU Fallbacks

Specify multiple GPU types with fallback:

```python
@app.function(gpu=["H100", "A100-40GB:2"])
def run_on_80gb():
    # Tries H100 first, falls back to 2x A100-40GB
    ...
```

Modal respects ordering and allocates most preferred available GPU.

## Multi-GPU Training

Modal supports multi-GPU training on a single node. Multi-node training is in closed beta.

### PyTorch Example

For frameworks that re-execute entrypoints, use subprocess or specific strategies:

```python
@app.function(gpu="A100:2")
def train():
    import subprocess
    import sys
    subprocess.run(
        ["python", "train.py"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )
```

For PyTorch Lightning, set strategy to `ddp_spawn` or `ddp_notebook`.

## Performance Considerations

**Memory-Bound vs Compute-Bound**:
- Running models with small batch sizes is memory-bound
- Newer GPUs have faster arithmetic than memory access
- Speedup from newer hardware may not justify cost for memory-bound workloads

**Optimization**:
- Use batching when possible
- Consider L40S before jumping to H100/B200
- Profile to identify bottlenecks

---

## Reference: Images

# Modal Images

## Overview

Modal Images define the environment code runs in - containers with dependencies installed. Images are built from method chains starting from a base image.

## Base Images

Start with a base image and chain methods:

```python
image = (
    modal.Image.debian_slim(python_version="3.13")
    .apt_install("git")
    .uv_pip_install("torch<3")
    .env({"HALT_AND_CATCH_FIRE": "0"})
    .run_commands("git clone https://github.com/modal-labs/agi")
)
```

Available base images:
- `Image.debian_slim()` - Debian Linux with Python
- `Image.micromamba()` - Base with Micromamba package manager
- `Image.from_registry()` - Pull from Docker Hub, ECR, etc.
- `Image.from_dockerfile()` - Build from existing Dockerfile

## Installing Python Packages

### With uv (Recommended)

Use `.uv_pip_install()` for fast package installation:

```python
image = (
    modal.Image.debian_slim()
    .uv_pip_install("pandas==2.2.0", "numpy")
)
```

### With pip

Fallback to standard pip if needed:

```python
image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install("pandas==2.2.0", "numpy")
)
```

Pin dependencies tightly (e.g., `"torch==2.8.0"`) for reproducibility.

## Installing System Packages

Install Linux packages with apt:

```python
image = modal.Image.debian_slim().apt_install("git", "curl")
```

## Setting Environment Variables

Pass a dictionary to `.env()`:

```python
image = modal.Image.debian_slim().env({"PORT": "6443"})
```

## Running Shell Commands

Execute commands during image build:

```python
image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .run_commands("git clone https://github.com/modal-labs/gpu-glossary")
)
```

## Running Python Functions at Build Time

Download model weights or perform setup:

```python
def download_models():
    import diffusers
    model_name = "segmind/small-sd"
    pipe = diffusers.StableDiffusionPipeline.from_pretrained(model_name)

hf_cache = modal.Volume.from_name("hf-cache")

image = (
    modal.Image.debian_slim()
    .pip_install("diffusers[torch]", "transformers")
    .run_function(
        download_models,
        secrets=[modal.Secret.from_name("huggingface-secret")],
        volumes={"/root/.cache/huggingface": hf_cache},
    )
)
```

## Adding Local Files

### Add Files or Directories

```python
image = modal.Image.debian_slim().add_local_dir(
    "/user/erikbern/.aws",
    remote_path="/root/.aws"
)
```

By default, files are added at container startup. Use `copy=True` to include in built image.

### Add Python Source

Add importable Python modules:

```python
image = modal.Image.debian_slim().add_local_python_source("local_module")

@app.function(image=image)
def f():
    import local_module
    local_module.do_stuff()
```

## Using Existing Container Images

### From Public Registry

```python
sklearn_image = modal.Image.from_registry("huanjason/scikit-learn")

@app.function(image=sklearn_image)
def fit_knn():
    from sklearn.neighbors import KNeighborsClassifier
    ...
```

Can pull from Docker Hub, Nvidia NGC, AWS ECR, GitHub ghcr.io.

### From Private Registry

Use Modal Secrets for authentication:

**Docker Hub**:
```python
secret = modal.Secret.from_name("my-docker-secret")
image = modal.Image.from_registry(
    "private-repo/image:tag",
    secret=secret
)
```

**AWS ECR**:
```python
aws_secret = modal.Secret.from_name("my-aws-secret")
image = modal.Image.from_aws_ecr(
    "000000000000.dkr.ecr.us-east-1.amazonaws.com/my-private-registry:latest",
    secret=aws_secret,
)
```

### From Dockerfile

```python
image = modal.Image.from_dockerfile("Dockerfile")

@app.function(image=image)
def fit():
    import sklearn
    ...
```

Can still extend with other image methods after importing.

## Using Micromamba

For coordinated installation of Python and system packages:

```python
numpyro_pymc_image = (
    modal.Image.micromamba()
    .micromamba_install("pymc==5.10.4", "numpyro==0.13.2", channels=["conda-forge"])
)
```

## GPU Support at Build Time

Run build steps on GPU instances:

```python
image = (
    modal.Image.debian_slim()
    .pip_install("bitsandbytes", gpu="H100")
)
```

## Image Caching

Images are cached per layer. Breaking cache on one layer causes cascading rebuilds for subsequent layers.

Define frequently-changing layers last to maximize cache reuse.

### Force Rebuild

```python
image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install("slack-sdk", force_build=True)
)
```

Or set environment variable:
```bash
MODAL_FORCE_BUILD=1 modal run ...
```

## Handling Different Local/Remote Packages

Import packages only available remotely inside function bodies:

```python
@app.function(image=image)
def my_function():
    import pandas as pd  # Only imported remotely
    df = pd.DataFrame()
    ...
```

Or use the imports context manager:

```python
pandas_image = modal.Image.debian_slim().pip_install("pandas")

with pandas_image.imports():
    import pandas as pd

@app.function(image=pandas_image)
def my_function():
    df = pd.DataFrame()
```

## Fast Pull from Registry with eStargz

Improve pull performance with eStargz compression:

```bash
docker buildx build --tag "<registry>/<namespace>/<repo>:<version>" \
  --output type=registry,compression=estargz,force-compression=true,oci-mediatypes=true \
  .
```

Supported registries:
- AWS ECR
- Docker Hub
- Google Artifact Registry

---

## Reference: Resources

# CPU, Memory, and Disk Resources

## Default Resources

Each Modal container has default reservations:
- **CPU**: 0.125 cores
- **Memory**: 128 MiB

Containers can exceed minimum if worker has available resources.

## CPU Cores

Request CPU cores as floating-point number:

```python
@app.function(cpu=8.0)
def my_function():
    # Guaranteed access to at least 8 physical cores
    ...
```

Values correspond to physical cores, not vCPUs.

Modal sets multi-threading environment variables based on CPU reservation:
- `OPENBLAS_NUM_THREADS`
- `OMP_NUM_THREADS`
- `MKL_NUM_THREADS`

## Memory

Request memory in megabytes (integer):

```python
@app.function(memory=32768)
def my_function():
    # Guaranteed access to at least 32 GiB RAM
    ...
```

## Resource Limits

### CPU Limits

Default soft CPU limit: request + 16 cores
- Default request: 0.125 cores → default limit: 16.125 cores
- Above limit, host throttles CPU usage

Set explicit CPU limit:

```python
cpu_request = 1.0
cpu_limit = 4.0

@app.function(cpu=(cpu_request, cpu_limit))
def f():
    ...
```

### Memory Limits

Set hard memory limit to OOM kill containers at threshold:

```python
mem_request = 1024  # MB
mem_limit = 2048    # MB

@app.function(memory=(mem_request, mem_limit))
def f():
    # Container killed if exceeds 2048 MB
    ...
```

Useful for catching memory leaks early.

### Disk Limits

Running containers have access to many GBs of SSD disk, limited by:
1. Underlying worker's SSD capacity
2. Per-container disk quota (100s of GBs)

Hitting limits causes `OSError` on disk writes.

Request larger disk with `ephemeral_disk`:

```python
@app.function(ephemeral_disk=10240)  # 10 GiB
def process_large_files():
    ...
```

Maximum disk size: 3.0 TiB (3,145,728 MiB)
Intended use: dataset processing

## Billing

Charged based on whichever is higher: reservation or actual usage.

Disk requests increase memory request at 20:1 ratio:
- Requesting 500 GiB disk → increases memory request to 25 GiB (if not already higher)

## Maximum Requests

Modal enforces maximums at Function creation time. Requests exceeding maximum will be rejected with `InvalidError`.

Contact support if you need higher limits.

## Example: Resource Configuration

```python
@app.function(
    cpu=4.0,              # 4 physical cores
    memory=16384,         # 16 GiB RAM
    ephemeral_disk=51200, # 50 GiB disk
    timeout=3600,         # 1 hour timeout
)
def process_data():
    # Heavy processing with large files
    ...
```

## Monitoring Resource Usage

View resource usage in Modal dashboard:
- CPU utilization
- Memory usage
- Disk usage
- GPU metrics (if applicable)

Access via https://modal.com/apps

---

## Reference: Scaling

# Scaling Out on Modal

## Automatic Autoscaling

Every Modal Function corresponds to an autoscaling pool of containers. Modal's autoscaler:
- Spins up containers when no capacity available
- Spins down containers when resources idle
- Scales to zero by default when no inputs to process

Autoscaling decisions are made quickly and frequently.

## Parallel Execution with `.map()`

Run function repeatedly with different inputs in parallel:

```python
@app.function()
def evaluate_model(x):
    return x ** 2

@app.local_entrypoint()
def main():
    inputs = list(range(100))
    # Runs 100 inputs in parallel across containers
    for result in evaluate_model.map(inputs):
        print(result)
```

### Multiple Arguments with `.starmap()`

For functions with multiple arguments:

```python
@app.function()
def add(a, b):
    return a + b

@app.local_entrypoint()
def main():
    results = list(add.starmap([(1, 2), (3, 4)]))
    # [3, 7]
```

### Exception Handling

```python
@app.function()
def may_fail(a):
    if a == 2:
        raise Exception("error")
    return a ** 2

@app.local_entrypoint()
def main():
    results = list(may_fail.map(
        range(3),
        return_exceptions=True,
        wrap_returned_exceptions=False
    ))
    # [0, 1, Exception('error')]
```

## Autoscaling Configuration

Configure autoscaler behavior with parameters:

```python
@app.function(
    max_containers=100,      # Upper limit on containers
    min_containers=2,        # Keep warm even when inactive
    buffer_containers=5,     # Maintain buffer while active
    scaledown_window=60,     # Max idle time before scaling down (seconds)
)
def my_function():
    ...
```

Parameters:
- **max_containers**: Upper limit on total containers
- **min_containers**: Minimum kept warm even when inactive
- **buffer_containers**: Buffer size while function active (additional inputs won't need to queue)
- **scaledown_window**: Maximum idle duration before scale down (seconds)

Trade-offs:
- Larger warm pool/buffer → Higher cost, lower latency
- Longer scaledown window → Less churn for infrequent requests

## Dynamic Autoscaler Updates

Update autoscaler settings without redeployment:

```python
f = modal.Function.from_name("my-app", "f")
f.update_autoscaler(max_containers=100)
```

Settings revert to decorator configuration on next deploy, or are overridden by further updates:

```python
f.update_autoscaler(min_containers=2, max_containers=10)
f.update_autoscaler(min_containers=4)  # max_containers=10 still in effect
```

### Time-Based Scaling

Adjust warm pool based on time of day:

```python
@app.function()
def inference_server():
    ...

@app.function(schedule=modal.Cron("0 6 * * *", timezone="America/New_York"))
def increase_warm_pool():
    inference_server.update_autoscaler(min_containers=4)

@app.function(schedule=modal.Cron("0 22 * * *", timezone="America/New_York"))
def decrease_warm_pool():
    inference_server.update_autoscaler(min_containers=0)
```

### For Classes

Update autoscaler for specific parameter instances:

```python
MyClass = modal.Cls.from_name("my-app", "MyClass")
obj = MyClass(model_version="3.5")
obj.update_autoscaler(buffer_containers=2)  # type: ignore
```

## Input Concurrency

Process multiple inputs per container with `@modal.concurrent`:

```python
@app.function()
@modal.concurrent(max_inputs=100)
def my_function(input: str):
    # Container can handle up to 100 concurrent inputs
    ...
```

Ideal for I/O-bound workloads:
- Database queries
- External API requests
- Remote Modal Function calls

### Concurrency Mechanisms

**Synchronous Functions**: Separate threads (must be thread-safe)

```python
@app.function()
@modal.concurrent(max_inputs=10)
def sync_function():
    time.sleep(1)  # Must be thread-safe
```

**Async Functions**: Separate asyncio tasks (must not block event loop)

```python
@app.function()
@modal.concurrent(max_inputs=10)
async def async_function():
    await asyncio.sleep(1)  # Must not block event loop
```

### Target vs Max Inputs

```python
@app.function()
@modal.concurrent(
    max_inputs=120,    # Hard limit
    target_inputs=100  # Autoscaler target
)
def my_function(input: str):
    # Allow 20% burst above target
    ...
```

Autoscaler aims for `target_inputs`, but containers can burst to `max_inputs` during scale-up.

## Scaling Limits

Modal enforces limits per function:
- 2,000 pending inputs (not yet assigned to containers)
- 25,000 total inputs (running + pending)

For `.spawn()` async jobs: up to 1 million pending inputs.

Exceeding limits returns `Resource Exhausted` error - retry later.

Each `.map()` invocation: max 1,000 concurrent inputs.

## Async Usage

Use async APIs for arbitrary parallel execution patterns:

```python
@app.function()
async def async_task(x):
    await asyncio.sleep(1)
    return x * 2

@app.local_entrypoint()
async def main():
    tasks = [async_task.remote.aio(i) for i in range(100)]
    results = await asyncio.gather(*tasks)
```

## Common Gotchas

**Incorrect**: Using Python's builtin map (runs sequentially)
```python
# DON'T DO THIS
results = map(evaluate_model, inputs)
```

**Incorrect**: Calling function first
```python
# DON'T DO THIS
results = evaluate_model(inputs).map()
```

**Correct**: Call .map() on Modal function object
```python
# DO THIS
results = evaluate_model.map(inputs)
```

---

## Reference: Scheduled Jobs

# Scheduled Jobs and Cron

## Basic Scheduling

Schedule functions to run automatically at regular intervals or specific times.

### Simple Daily Schedule

```python
import modal

app = modal.App()

@app.function(schedule=modal.Period(days=1))
def daily_task():
    print("Running daily task")
    # Process data, send reports, etc.
```

Deploy to activate:
```bash
modal deploy script.py
```

Function runs every 24 hours from deployment time.

## Schedule Types

### Period Schedules

Run at fixed intervals from deployment time:

```python
# Every 5 hours
@app.function(schedule=modal.Period(hours=5))
def every_5_hours():
    ...

# Every 30 minutes
@app.function(schedule=modal.Period(minutes=30))
def every_30_minutes():
    ...

# Every day
@app.function(schedule=modal.Period(days=1))
def daily():
    ...
```

**Note**: Redeploying resets the period timer.

### Cron Schedules

Run at specific times using cron syntax:

```python
# Every Monday at 8 AM UTC
@app.function(schedule=modal.Cron("0 8 * * 1"))
def weekly_report():
    ...

# Daily at 6 AM New York time
@app.function(schedule=modal.Cron("0 6 * * *", timezone="America/New_York"))
def morning_report():
    ...

# Every hour on the hour
@app.function(schedule=modal.Cron("0 * * * *"))
def hourly():
    ...

# Every 15 minutes
@app.function(schedule=modal.Cron("*/15 * * * *"))
def quarter_hourly():
    ...
```

**Cron syntax**: `minute hour day month day_of_week`
- Minute: 0-59
- Hour: 0-23
- Day: 1-31
- Month: 1-12
- Day of week: 0-6 (0 = Sunday)

### Timezone Support

Specify timezone for cron schedules:

```python
@app.function(schedule=modal.Cron("0 9 * * *", timezone="Europe/London"))
def uk_morning_task():
    ...

@app.function(schedule=modal.Cron("0 17 * * 5", timezone="Asia/Tokyo"))
def friday_evening_jp():
    ...
```

## Deployment

### Deploy Scheduled Functions

```bash
modal deploy script.py
```

Scheduled functions persist until explicitly stopped.

### Programmatic Deployment

```python
if __name__ == "__main__":
    app.deploy()
```

## Monitoring

### View Execution Logs

Check https://modal.com/apps for:
- Past execution logs
- Execution history
- Failure notifications

### Run Manually

Trigger scheduled function immediately via dashboard "Run now" button.

## Schedule Management

### Pausing Schedules

Schedules cannot be paused. To stop:
1. Remove `schedule` parameter
2. Redeploy app

### Updating Schedules

Change schedule parameters and redeploy:

```python
# Update from daily to weekly
@app.function(schedule=modal.Period(days=7))
def task():
    ...
```

```bash
modal deploy script.py
```

## Common Patterns

### Data Pipeline

```python
@app.function(
    schedule=modal.Cron("0 2 * * *"),  # 2 AM daily
    timeout=3600,                       # 1 hour timeout
)
def etl_pipeline():
    # Extract data from sources
    data = extract_data()

    # Transform data
    transformed = transform_data(data)

    # Load to warehouse
    load_to_warehouse(transformed)
```

### Model Retraining

```python
volume = modal.Volume.from_name("models")

@app.function(
    schedule=modal.Cron("0 0 * * 0"),  # Weekly on Sunday midnight
    gpu="A100",
    timeout=7200,                       # 2 hours
    volumes={"/models": volume}
)
def retrain_model():
    # Load latest data
    data = load_training_data()

    # Train model
    model = train(data)

    # Save new model
    save_model(model, "/models/latest.pt")
    volume.commit()
```

### Report Generation

```python
@app.function(
    schedule=modal.Cron("0 9 * * 1"),  # Monday 9 AM
    secrets=[modal.Secret.from_name("email-creds")]
)
def weekly_report():
    # Generate report
    report = generate_analytics_report()

    # Send email
    send_email(
        to="team@company.com",
        subject="Weekly Analytics Report",
        body=report
    )
```

### Data Cleanup

```python
@app.function(schedule=modal.Period(hours=6))
def cleanup_old_data():
    # Remove data older than 30 days
    cutoff = datetime.now() - timedelta(days=30)
    delete_old_records(cutoff)
```

## Configuration with Secrets and Volumes

Scheduled functions support all function parameters:

```python
vol = modal.Volume.from_name("data")
secret = modal.Secret.from_name("api-keys")

@app.function(
    schedule=modal.Cron("0 */6 * * *"),  # Every 6 hours
    secrets=[secret],
    volumes={"/data": vol},
    cpu=4.0,
    memory=16384,
)
def sync_data():
    import os

    api_key = os.environ["API_KEY"]

    # Fetch from external API
    data = fetch_external_data(api_key)

    # Save to volume
    with open("/data/latest.json", "w") as f:
        json.dump(data, f)

    vol.commit()
```

## Dynamic Scheduling

Update schedules programmatically:

```python
@app.function()
def main_task():
    ...

@app.function(schedule=modal.Cron("0 6 * * *", timezone="America/New_York"))
def enable_high_traffic_mode():
    main_task.update_autoscaler(min_containers=5)

@app.function(schedule=modal.Cron("0 22 * * *", timezone="America/New_York"))
def disable_high_traffic_mode():
    main_task.update_autoscaler(min_containers=0)
```

## Error Handling

Scheduled functions that fail will:
- Show failure in dashboard
- Send notifications (configurable)
- Retry on next scheduled run

```python
@app.function(
    schedule=modal.Cron("0 * * * *"),
    retries=3,  # Retry failed runs
    timeout=1800
)
def robust_task():
    try:
        perform_task()
    except Exception as e:
        # Log error
        print(f"Task failed: {e}")
        # Optionally send alert
        send_alert(f"Scheduled task failed: {e}")
        raise
```

## Best Practices

1. **Set timeouts**: Always specify timeout for scheduled functions
2. **Use appropriate schedules**: Period for relative timing, Cron for absolute
3. **Monitor failures**: Check dashboard regularly for failed runs
4. **Idempotent operations**: Design tasks to handle reruns safely
5. **Resource limits**: Set appropriate CPU/memory for scheduled workloads
6. **Timezone awareness**: Specify timezone for cron schedules

---

## Reference: Secrets

# Secrets and Environment Variables

## Creating Secrets

### Via Dashboard

Create secrets at https://modal.com/secrets

Templates available for:
- Database credentials (Postgres, MongoDB)
- Cloud providers (AWS, GCP, Azure)
- ML platforms (Weights & Biases, Hugging Face)
- And more

### Via CLI

```bash
# Create secret with key-value pairs
modal secret create my-secret KEY1=value1 KEY2=value2

# Use environment variables
modal secret create db-secret PGHOST=uri PGPASSWORD="$PGPASSWORD"

# List secrets
modal secret list

# Delete secret
modal secret delete my-secret
```

### Programmatically

From dictionary:

```python
if modal.is_local():
    local_secret = modal.Secret.from_dict({"FOO": os.environ["LOCAL_FOO"]})
else:
    local_secret = modal.Secret.from_dict({})

@app.function(secrets=[local_secret])
def some_function():
    import os
    print(os.environ["FOO"])
```

From .env file:

```python
@app.function(secrets=[modal.Secret.from_dotenv()])
def some_function():
    import os
    print(os.environ["USERNAME"])
```

## Using Secrets

Inject secrets into functions:

```python
@app.function(secrets=[modal.Secret.from_name("my-secret")])
def some_function():
    import os
    secret_key = os.environ["MY_PASSWORD"]
    # Use secret
    ...
```

### Multiple Secrets

```python
@app.function(secrets=[
    modal.Secret.from_name("database-creds"),
    modal.Secret.from_name("api-keys"),
])
def other_function():
    # All keys from both secrets available
    ...
```

Later secrets override earlier ones if keys clash.

## Environment Variables

### Reserved Runtime Variables

**All Containers**:
- `MODAL_CLOUD_PROVIDER` - Cloud provider (AWS/GCP/OCI)
- `MODAL_IMAGE_ID` - Image ID
- `MODAL_REGION` - Region identifier (e.g., us-east-1)
- `MODAL_TASK_ID` - Container task ID

**Function Containers**:
- `MODAL_ENVIRONMENT` - Modal Environment name
- `MODAL_IS_REMOTE` - Set to '1' in remote containers
- `MODAL_IDENTITY_TOKEN` - OIDC token for function identity

**Sandbox Containers**:
- `MODAL_SANDBOX_ID` - Sandbox ID

### Setting Environment Variables

Via Image:

```python
image = modal.Image.debian_slim().env({"PORT": "6443"})

@app.function(image=image)
def my_function():
    import os
    port = os.environ["PORT"]
```

Via Secrets:

```python
secret = modal.Secret.from_dict({"API_KEY": "secret-value"})

@app.function(secrets=[secret])
def my_function():
    import os
    api_key = os.environ["API_KEY"]
```

## Common Secret Patterns

### AWS Credentials

```python
aws_secret = modal.Secret.from_name("my-aws-secret")

@app.function(secrets=[aws_secret])
def use_aws():
    import boto3
    s3 = boto3.client('s3')
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY automatically used
```

### Hugging Face Token

```python
hf_secret = modal.Secret.from_name("huggingface")

@app.function(secrets=[hf_secret])
def download_model():
    from transformers import AutoModel
    # HF_TOKEN automatically used for authentication
    model = AutoModel.from_pretrained("private-model")
```

### Database Credentials

```python
db_secret = modal.Secret.from_name("postgres-creds")

@app.function(secrets=[db_secret])
def query_db():
    import psycopg2
    conn = psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )
```

## Best Practices

1. **Never hardcode secrets** - Always use Modal Secrets
2. **Use specific secrets** - Create separate secrets for different purposes
3. **Rotate secrets regularly** - Update secrets periodically
4. **Minimal scope** - Only attach secrets to functions that need them
5. **Environment-specific** - Use different secrets for dev/staging/prod

## Security Notes

- Secrets are encrypted at rest
- Only available to functions that explicitly request them
- Not logged or exposed in dashboards
- Can be scoped to specific environments

---

## Reference: Volumes

# Modal Volumes

## Overview

Modal Volumes provide high-performance distributed file systems for Modal applications. Designed for write-once, read-many workloads like ML model weights and distributed data processing.

## Creating Volumes

### Via CLI

```bash
modal volume create my-volume
```

For Volumes v2 (beta):
```bash
modal volume create --version=2 my-volume
```

### From Code

```python
vol = modal.Volume.from_name("my-volume", create_if_missing=True)

# For v2
vol = modal.Volume.from_name("my-volume", create_if_missing=True, version=2)
```

## Using Volumes

Attach to functions via mount points:

```python
vol = modal.Volume.from_name("my-volume")

@app.function(volumes={"/data": vol})
def run():
    with open("/data/xyz.txt", "w") as f:
        f.write("hello")
    vol.commit()  # Persist changes
```

## Commits and Reloads

### Commits

Persist changes to Volume:

```python
@app.function(volumes={"/data": vol})
def write_data():
    with open("/data/file.txt", "w") as f:
        f.write("data")
    vol.commit()  # Make changes visible to other containers
```

**Background commits**: Modal automatically commits Volume changes every few seconds and on container shutdown.

### Reloads

Fetch latest changes from other containers:

```python
@app.function(volumes={"/data": vol})
def read_data():
    vol.reload()  # Fetch latest changes
    with open("/data/file.txt", "r") as f:
        content = f.read()
```

At container creation, latest Volume state is mounted. Reload needed to see subsequent commits from other containers.

## Uploading Files

### Batch Upload (Efficient)

```python
vol = modal.Volume.from_name("my-volume")

with vol.batch_upload() as batch:
    batch.put_file("local-path.txt", "/remote-path.txt")
    batch.put_directory("/local/directory/", "/remote/directory")
    batch.put_file(io.BytesIO(b"some data"), "/foobar")
```

### Via Image

```python
image = modal.Image.debian_slim().add_local_dir(
    local_path="/home/user/my_dir",
    remote_path="/app"
)

@app.function(image=image)
def process():
    # Files available at /app
    ...
```

## Downloading Files

### Via CLI

```bash
modal volume get my-volume remote.txt local.txt
```

Max file size via CLI: No limit
Max file size via dashboard: 16 MB

### Via Python SDK

```python
vol = modal.Volume.from_name("my-volume")

for data in vol.read_file("path.txt"):
    print(data)
```

## Volume Performance

### Volumes v1

Best for:
- <50,000 files (recommended)
- <500,000 files (hard limit)
- Sequential access patterns
- <5 concurrent writers

### Volumes v2 (Beta)

Improved for:
- Unlimited files
- Hundreds of concurrent writers
- Random access patterns
- Large files (up to 1 TiB)

Current v2 limits:
- Max file size: 1 TiB
- Max files per directory: 32,768
- Unlimited directory depth

## Model Storage

### Saving Model Weights

```python
volume = modal.Volume.from_name("model-weights", create_if_missing=True)
MODEL_DIR = "/models"

@app.function(volumes={MODEL_DIR: volume})
def train():
    model = train_model()
    save_model(f"{MODEL_DIR}/my_model.pt", model)
    volume.commit()
```

### Loading Model Weights

```python
@app.function(volumes={MODEL_DIR: volume})
def inference(model_id: str):
    try:
        model = load_model(f"{MODEL_DIR}/{model_id}")
    except NotFound:
        volume.reload()  # Fetch latest models
        model = load_model(f"{MODEL_DIR}/{model_id}")
    return model.run(request)
```

## Model Checkpointing

Save checkpoints during long training jobs:

```python
volume = modal.Volume.from_name("checkpoints")
VOL_PATH = "/vol"

@app.function(
    gpu="A10G",
    timeout=2*60*60,  # 2 hours
    volumes={VOL_PATH: volume}
)
def finetune():
    from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

    training_args = Seq2SeqTrainingArguments(
        output_dir=str(VOL_PATH / "model"),  # Checkpoints saved to Volume
        save_steps=100,
        # ... more args
    )

    trainer = Seq2SeqTrainer(model=model, args=training_args, ...)
    trainer.train()
```

Background commits ensure checkpoints persist even if training is interrupted.

## CLI Commands

```bash
# List files
modal volume ls my-volume

# Upload
modal volume put my-volume local.txt remote.txt

# Download
modal volume get my-volume remote.txt local.txt

# Copy within Volume
modal volume cp my-volume src.txt dst.txt

# Delete
modal volume rm my-volume file.txt

# List all volumes
modal volume list

# Delete volume
modal volume delete my-volume
```

## Ephemeral Volumes

Create temporary volumes that are garbage collected:

```python
with modal.Volume.ephemeral() as vol:
    sb = modal.Sandbox.create(
        volumes={"/cache": vol},
        app=my_app,
    )
    # Use volume
    # Automatically cleaned up when context exits
```

## Concurrent Access

### Concurrent Reads

Multiple containers can read simultaneously without issues.

### Concurrent Writes

Supported but:
- Avoid modifying same files concurrently
- Last write wins (data loss possible)
- v1: Limit to ~5 concurrent writers
- v2: Hundreds of concurrent writers supported

## Volume Errors

### "Volume Busy"

Cannot reload when files are open:

```python
# WRONG
f = open("/vol/data.txt", "r")
volume.reload()  # ERROR: volume busy
```

```python
# CORRECT
with open("/vol/data.txt", "r") as f:
    data = f.read()
# File closed before reload
volume.reload()
```

### "File Not Found"

Remember to use mount point:

```python
# WRONG - file saved to local disk
with open("/xyz.txt", "w") as f:
    f.write("data")

# CORRECT - file saved to Volume
with open("/data/xyz.txt", "w") as f:
    f.write("data")
```

## Upgrading from v1 to v2

No automated migration currently. Manual steps:

1. Create new v2 Volume
2. Copy data using `cp` or `rsync`
3. Update app to use new Volume

```bash
modal volume create --version=2 my-volume-v2
modal shell --volume my-volume --volume my-volume-v2

# In shell:
cp -rp /mnt/my-volume/. /mnt/my-volume-v2/.
sync /mnt/my-volume-v2
```

Warning: Deployed apps reference Volumes by ID. Re-deploy after creating new Volume.

---

## Reference: Web Endpoints

# Web Endpoints

## Quick Start

Create web endpoint with single decorator:

```python
image = modal.Image.debian_slim().pip_install("fastapi[standard]")

@app.function(image=image)
@modal.fastapi_endpoint()
def hello():
    return "Hello world!"
```

## Development and Deployment

### Development with `modal serve`

```bash
modal serve server.py
```

Creates ephemeral app with live-reloading. Changes to endpoints appear almost immediately.

### Deployment with `modal deploy`

```bash
modal deploy server.py
```

Creates persistent endpoint with stable URL.

## Simple Endpoints

### Query Parameters

```python
@app.function(image=image)
@modal.fastapi_endpoint()
def square(x: int):
    return {"square": x**2}
```

Call with:
```bash
curl "https://workspace--app-square.modal.run?x=42"
```

### POST Requests

```python
@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
def square(item: dict):
    return {"square": item['x']**2}
```

Call with:
```bash
curl -X POST -H 'Content-Type: application/json' \
  --data '{"x": 42}' \
  https://workspace--app-square.modal.run
```

### Pydantic Models

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    qty: int = 42

@app.function()
@modal.fastapi_endpoint(method="POST")
def process(item: Item):
    return {"processed": item.name, "quantity": item.qty}
```

## ASGI Apps (FastAPI, Starlette, FastHTML)

Serve full ASGI applications:

```python
image = modal.Image.debian_slim().pip_install("fastapi[standard]")

@app.function(image=image)
@modal.concurrent(max_inputs=100)
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI

    web_app = FastAPI()

    @web_app.get("/")
    async def root():
        return {"message": "Hello"}

    @web_app.post("/echo")
    async def echo(request: Request):
        body = await request.json()
        return body

    return web_app
```

## WSGI Apps (Flask, Django)

Serve synchronous web frameworks:

```python
image = modal.Image.debian_slim().pip_install("flask")

@app.function(image=image)
@modal.concurrent(max_inputs=100)
@modal.wsgi_app()
def flask_app():
    from flask import Flask, request

    web_app = Flask(__name__)

    @web_app.post("/echo")
    def echo():
        return request.json

    return web_app
```

## Non-ASGI Web Servers

For frameworks with custom network binding:

> ⚠️ **Security Note**: The example below uses `shell=True` for simplicity. In production environments, prefer using `subprocess.Popen()` with a list of arguments to prevent command injection vulnerabilities.

```python
@app.function()
@modal.concurrent(max_inputs=100)
@modal.web_server(8000)
def my_server():
    import subprocess
    # Must bind to 0.0.0.0, not 127.0.0.1
    # Use list form instead of shell=True for security
    subprocess.Popen(["python", "-m", "http.server", "-d", "/", "8000"])
```

## Streaming Responses

Use FastAPI's `StreamingResponse`:

```python
import time

def event_generator():
    for i in range(10):
        yield f"data: event {i}\n\n".encode()
        time.sleep(0.5)

@app.function(image=modal.Image.debian_slim().pip_install("fastapi[standard]"))
@modal.fastapi_endpoint()
def stream():
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### Streaming from Modal Functions

```python
@app.function(gpu="any")
def process_gpu():
    for i in range(10):
        yield f"data: result {i}\n\n".encode()
        time.sleep(1)

@app.function(image=modal.Image.debian_slim().pip_install("fastapi[standard]"))
@modal.fastapi_endpoint()
def hook():
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        process_gpu.remote_gen(),
        media_type="text/event-stream"
    )
```

### With .map()

```python
@app.function()
def process_segment(i):
    return f"segment {i}\n"

@app.function(image=modal.Image.debian_slim().pip_install("fastapi[standard]"))
@modal.fastapi_endpoint()
def stream_parallel():
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        process_segment.map(range(10)),
        media_type="text/plain"
    )
```

## WebSockets

Supported with `@web_server`, `@asgi_app`, and `@wsgi_app`. Maintains single function call per connection. Use with `@modal.concurrent` for multiple simultaneous connections.

Full WebSocket protocol (RFC 6455) supported. Messages up to 2 MiB each.

## Authentication

### Proxy Auth Tokens

First-class authentication via Modal:

```python
@app.function()
@modal.fastapi_endpoint()
def protected():
    return "authenticated!"
```

Protect with tokens in settings, pass in headers:
- `Modal-Key`
- `Modal-Secret`

### Bearer Token Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_scheme = HTTPBearer()

@app.function(secrets=[modal.Secret.from_name("auth-token")])
@modal.fastapi_endpoint()
async def protected(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    import os
    if token.credentials != os.environ["AUTH_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return "success!"
```

### Client IP Address

```python
from fastapi import Request

@app.function()
@modal.fastapi_endpoint()
def get_ip(request: Request):
    return f"Your IP: {request.client.host}"
```

## Web Endpoint URLs

### Auto-Generated URLs

Format: `https://<workspace>--<app>-<function>.modal.run`

With environment suffix: `https://<workspace>-<suffix>--<app>-<function>.modal.run`

### Custom Labels

```python
@app.function()
@modal.fastapi_endpoint(label="api")
def handler():
    ...
# URL: https://workspace--api.modal.run
```

### Programmatic URL Retrieval

```python
@app.function()
@modal.fastapi_endpoint()
def my_endpoint():
    url = my_endpoint.get_web_url()
    return {"url": url}

# From deployed function
f = modal.Function.from_name("app-name", "my_endpoint")
url = f.get_web_url()
```

### Custom Domains

Available on Team and Enterprise plans:

```python
@app.function()
@modal.fastapi_endpoint(custom_domains=["api.example.com"])
def hello(message: str):
    return {"message": f"hello {message}"}
```

Multiple domains:
```python
@modal.fastapi_endpoint(custom_domains=["api.example.com", "api.example.net"])
```

Wildcard domains:
```python
@modal.fastapi_endpoint(custom_domains=["*.example.com"])
```

TLS certificates automatically generated and renewed.

## Performance

### Cold Starts

First request may experience cold start (few seconds). Modal keeps containers alive for subsequent requests.

### Scaling

- Autoscaling based on traffic
- Use `@modal.concurrent` for multiple requests per container
- Beyond concurrency limit, additional containers spin up
- Requests queue when at max containers

### Rate Limits

Default: 200 requests/second with 5-second burst multiplier
- Excess returns 429 status code
- Contact support to increase limits

### Size Limits

- Request body: up to 4 GiB
- Response body: unlimited
- WebSocket messages: up to 2 MiB
