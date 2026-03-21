---
title: "Latchbio Integration"
description: "Latch platform for bioinformatics workflows. Build pipelines with Latch SDK, @workflow/@task decorators, deploy serverless workflows, LatchFile/LatchDir, Nextflow/Snakemake integration."
category: "devops"
source: "community"
author: "Community"
tags: ["latchbio", "integration"]
date: 2026-03-20
---

# LatchBio Integration

## Overview

Latch is a Python framework for building and deploying bioinformatics workflows as serverless pipelines. Built on Flyte, create workflows with @workflow/@task decorators, manage cloud data with LatchFile/LatchDir, configure resources, and integrate Nextflow/Snakemake pipelines.

## Core Capabilities

The Latch platform provides four main areas of functionality:

### 1. Workflow Creation and Deployment
- Define serverless workflows using Python decorators
- Support for native Python, Nextflow, and Snakemake pipelines
- Automatic containerization with Docker
- Auto-generated no-code user interfaces
- Version control and reproducibility

### 2. Data Management
- Cloud storage abstractions (LatchFile, LatchDir)
- Structured data organization with Registry (Projects → Tables → Records)
- Type-safe data operations with links and enums
- Automatic file transfer between local and cloud
- Glob pattern matching for file selection

### 3. Resource Configuration
- Pre-configured task decorators (@small_task, @large_task, @small_gpu_task, @large_gpu_task)
- Custom resource specifications (CPU, memory, GPU, storage)
- GPU support (K80, V100, A100)
- Timeout and storage configuration
- Cost optimization strategies

### 4. Verified Workflows
- Production-ready pre-built pipelines
- Bulk RNA-seq, DESeq2, pathway analysis
- AlphaFold and ColabFold for protein structure prediction
- Single-cell tools (ArchR, scVelo, emptyDropsR)
- CRISPR analysis, phylogenetics, and more

## Quick Start

### Installation and Setup

```bash
# Install Latch SDK
python3 -m uv pip install latch

# Login to Latch
latch login

# Initialize a new workflow
latch init my-workflow

# Register workflow to platform
latch register my-workflow
```

**Prerequisites:**
- Docker installed and running
- Latch account credentials
- Python 3.8+

### Basic Workflow Example

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    """Process a single file"""
    # Processing logic
    return output_file

@workflow
def my_workflow(input_file: LatchFile) -> LatchFile:
    """
    My bioinformatics workflow

    Args:
        input_file: Input data file
    """
    return process_file(input_file=input_file)
```

## When to Use This Skill

This skill should be used when encountering any of the following scenarios:

**Workflow Development:**
- "Create a Latch workflow for RNA-seq analysis"
- "Deploy my pipeline to Latch"
- "Convert my Nextflow pipeline to Latch"
- "Add GPU support to my workflow"
- Working with `@workflow`, `@task` decorators

**Data Management:**
- "Organize my sequencing data in Latch Registry"
- "How do I use LatchFile and LatchDir?"
- "Set up sample tracking in Latch"
- Working with `latch:///` paths

**Resource Configuration:**
- "Configure GPU for AlphaFold on Latch"
- "My task is running out of memory"
- "How do I optimize workflow costs?"
- Working with task decorators

**Verified Workflows:**
- "Run AlphaFold on Latch"
- "Use DESeq2 for differential expression"
- "Available pre-built workflows"
- Using `latch.verified` module

## Detailed Documentation

This skill includes comprehensive reference documentation organized by capability:

### references/workflow-creation.md
**Read this for:**
- Creating and registering workflows
- Task definition and decorators
- Supporting Python, Nextflow, Snakemake
- Launch plans and conditional sections
- Workflow execution (CLI and programmatic)
- Multi-step and parallel pipelines
- Troubleshooting registration issues

**Key topics:**
- `latch init` and `latch register` commands
- `@workflow` and `@task` decorators
- LatchFile and LatchDir basics
- Type annotations and docstrings
- Launch plans with preset parameters
- Conditional UI sections

### references/data-management.md
**Read this for:**
- Cloud storage with LatchFile and LatchDir
- Registry system (Projects, Tables, Records)
- Linked records and relationships
- Enum and typed columns
- Bulk operations and transactions
- Integration with workflows
- Account and workspace management

**Key topics:**
- `latch:///` path format
- File transfer and glob patterns
- Creating and querying Registry tables
- Column types (string, number, file, link, enum)
- Record CRUD operations
- Workflow-Registry integration

### references/resource-configuration.md
**Read this for:**
- Task resource decorators
- Custom CPU, memory, GPU configuration
- GPU types (K80, V100, A100)
- Timeout and storage settings
- Resource optimization strategies
- Cost-effective workflow design
- Monitoring and debugging

**Key topics:**
- `@small_task`, `@large_task`, `@small_gpu_task`, `@large_gpu_task`
- `@custom_task` with precise specifications
- Multi-GPU configuration
- Resource selection by workload type
- Platform limits and quotas

### references/verified-workflows.md
**Read this for:**
- Pre-built production workflows
- Bulk RNA-seq and DESeq2
- AlphaFold and ColabFold
- Single-cell analysis (ArchR, scVelo)
- CRISPR editing analysis
- Pathway enrichment
- Integration with custom workflows

**Key topics:**
- `latch.verified` module imports
- Available verified workflows
- Workflow parameters and options
- Combining verified and custom steps
- Version management

## Common Workflow Patterns

### Complete RNA-seq Pipeline

```python
from latch import workflow, small_task, large_task
from latch.types import LatchFile, LatchDir

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """Run FastQC"""
    return qc_output

@large_task
def alignment(fastq: LatchFile, genome: str) -> LatchFile:
    """STAR alignment"""
    return bam_output

@small_task
def quantification(bam: LatchFile) -> LatchFile:
    """featureCounts"""
    return counts

@workflow
def rnaseq_pipeline(
    input_fastq: LatchFile,
    genome: str,
    output_dir: LatchDir
) -> LatchFile:
    """RNA-seq analysis pipeline"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc, genome=genome)
    return quantification(bam=aligned)
```

### GPU-Accelerated Workflow

```python
from latch import workflow, small_task, large_gpu_task
from latch.types import LatchFile

@small_task
def preprocess(input_file: LatchFile) -> LatchFile:
    """Prepare data"""
    return processed

@large_gpu_task
def gpu_computation(data: LatchFile) -> LatchFile:
    """GPU-accelerated analysis"""
    return results

@workflow
def gpu_pipeline(input_file: LatchFile) -> LatchFile:
    """Pipeline with GPU tasks"""
    preprocessed = preprocess(input_file=input_file)
    return gpu_computation(data=preprocessed)
```

### Registry-Integrated Workflow

```python
from latch import workflow, small_task
from latch.registry.table import Table
from latch.registry.record import Record
from latch.types import LatchFile

@small_task
def process_and_track(sample_id: str, table_id: str) -> str:
    """Process sample and update Registry"""
    # Get sample from registry
    table = Table.get(table_id=table_id)
    records = Record.list(table_id=table_id, filter={"sample_id": sample_id})
    sample = records[0]

    # Process
    input_file = sample.values["fastq_file"]
    output = process(input_file)

    # Update registry
    sample.update(values={"status": "completed", "result": output})
    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """Workflow integrated with Registry"""
    return process_and_track(sample_id=sample_id, table_id=table_id)
```

## Best Practices

### Workflow Design
1. Use type annotations for all parameters
2. Write clear docstrings (appear in UI)
3. Start with standard task decorators, scale up if needed
4. Break complex workflows into modular tasks
5. Implement proper error handling

### Data Management
6. Use consistent folder structures
7. Define Registry schemas before bulk entry
8. Use linked records for relationships
9. Store metadata in Registry for traceability

### Resource Configuration
10. Right-size resources (don't over-allocate)
11. Use GPU only when algorithms support it
12. Monitor execution metrics and optimize
13. Design for parallel execution when possible

### Development Workflow
14. Test locally with Docker before registration
15. Use version control for workflow code
16. Document resource requirements
17. Profile workflows to determine actual needs

## Troubleshooting

### Common Issues

**Registration Failures:**
- Ensure Docker is running
- Check authentication with `latch login`
- Verify all dependencies in Dockerfile
- Use `--verbose` flag for detailed logs

**Resource Problems:**
- Out of memory: Increase memory in task decorator
- Timeouts: Increase timeout parameter
- Storage issues: Increase ephemeral storage_gib

**Data Access:**
- Use correct `latch:///` path format
- Verify file exists in workspace
- Check permissions for shared workspaces

**Type Errors:**
- Add type annotations to all parameters
- Use LatchFile/LatchDir for file/directory parameters
- Ensure workflow return type matches actual return

## Additional Resources

- **Official Documentation**: https://docs.latch.bio
- **GitHub Repository**: https://github.com/latchbio/latch
- **Slack Community**: Join Latch SDK workspace
- **API Reference**: https://docs.latch.bio/api/latch.html
- **Blog**: https://blog.latch.bio

## Support

For issues or questions:
1. Check documentation links above
2. Search GitHub issues
3. Ask in Slack community
4. Contact support@latch.bio

---

## Reference: Data Management

# Data Management

## Overview
Latch provides comprehensive data management through cloud storage abstractions (LatchFile, LatchDir) and a structured Registry system for organizing experimental data.

## Cloud Storage: LatchFile and LatchDir

### LatchFile

Represents a file in Latch's cloud storage system.

```python
from latch.types import LatchFile

# Create reference to existing file
input_file = LatchFile("latch:///data/sample.fastq")

# Access file properties
file_path = input_file.local_path  # Local path when executing
file_remote = input_file.remote_path  # Cloud storage path
```

### LatchDir

Represents a directory in Latch's cloud storage system.

```python
from latch.types import LatchDir

# Create reference to directory
output_dir = LatchDir("latch:///results/experiment_1")

# Directory operations
all_files = output_dir.glob("*.bam")  # Find files matching pattern
subdirs = output_dir.iterdir()  # List contents
```

### Path Formats

Latch storage uses a special URL scheme:
- **Latch paths**: `latch:///path/to/file`
- **Local paths**: Automatically resolved during workflow execution
- **S3 paths**: Can be used directly if configured

### File Transfer

Files are automatically transferred between local execution and cloud storage:

```python
from latch import small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    # File is automatically downloaded to local execution
    local_path = input_file.local_path

    # Process the file
    with open(local_path, 'r') as f:
        data = f.read()

    # Write output
    output_path = "output.txt"
    with open(output_path, 'w') as f:
        f.write(processed_data)

    # Automatically uploaded back to cloud storage
    return LatchFile(output_path, "latch:///results/output.txt")
```

### Glob Patterns

Find files using pattern matching:

```python
from latch.types import LatchDir

data_dir = LatchDir("latch:///data")

# Find all FASTQ files
fastq_files = data_dir.glob("**/*.fastq")

# Find files in subdirectories
bam_files = data_dir.glob("alignments/**/*.bam")

# Multiple patterns
results = data_dir.glob("*.{bam,sam}")
```

## Registry System

The Registry provides structured data organization with projects, tables, and records.

### Registry Architecture

```
Account/Workspace
└── Projects
    └── Tables
        └── Records
```

### Working with Projects

```python
from latch.registry.project import Project

# Get or create a project
project = Project.create(
    name="RNA-seq Analysis",
    description="Bulk RNA-seq experiments"
)

# List existing projects
all_projects = Project.list()

# Get project by ID
project = Project.get(project_id="proj_123")
```

### Working with Tables

Tables store structured data records:

```python
from latch.registry.table import Table

# Create a table
table = Table.create(
    project_id=project.id,
    name="Samples",
    columns=[
        {"name": "sample_id", "type": "string"},
        {"name": "condition", "type": "string"},
        {"name": "replicate", "type": "number"},
        {"name": "fastq_file", "type": "file"}
    ]
)

# List tables in project
tables = Table.list(project_id=project.id)

# Get table by ID
table = Table.get(table_id="tbl_456")
```

### Column Types

Supported data types:
- `string` - Text data
- `number` - Numeric values (integer or float)
- `boolean` - True/False values
- `date` - Date values
- `file` - LatchFile references
- `directory` - LatchDir references
- `link` - References to records in other tables
- `enum` - Enumerated values from predefined list

### Working with Records

```python
from latch.registry.record import Record

# Create a record
record = Record.create(
    table_id=table.id,
    values={
        "sample_id": "S001",
        "condition": "treated",
        "replicate": 1,
        "fastq_file": LatchFile("latch:///data/S001.fastq")
    }
)

# Bulk create records
records = Record.bulk_create(
    table_id=table.id,
    records=[
        {"sample_id": "S001", "condition": "treated"},
        {"sample_id": "S002", "condition": "control"}
    ]
)

# Query records
all_records = Record.list(table_id=table.id)
filtered = Record.list(
    table_id=table.id,
    filter={"condition": "treated"}
)

# Update record
record.update(values={"replicate": 2})

# Delete record
record.delete()
```

### Linked Records

Create relationships between tables:

```python
# Define table with link column
results_table = Table.create(
    project_id=project.id,
    name="Results",
    columns=[
        {"name": "sample", "type": "link", "target_table": samples_table.id},
        {"name": "alignment_bam", "type": "file"},
        {"name": "gene_counts", "type": "file"}
    ]
)

# Create record with link
result_record = Record.create(
    table_id=results_table.id,
    values={
        "sample": sample_record.id,  # Link to sample record
        "alignment_bam": LatchFile("latch:///results/aligned.bam"),
        "gene_counts": LatchFile("latch:///results/counts.tsv")
    }
)

# Access linked data
sample_data = result_record.values["sample"].resolve()
```

### Enum Columns

Define columns with predefined values:

```python
table = Table.create(
    project_id=project.id,
    name="Experiments",
    columns=[
        {
            "name": "status",
            "type": "enum",
            "options": ["pending", "running", "completed", "failed"]
        }
    ]
)
```

### Transactions and Bulk Updates

Efficiently update multiple records:

```python
from latch.registry.transaction import Transaction

# Start transaction
with Transaction() as txn:
    for record in records:
        record.update(values={"status": "processed"}, transaction=txn)
    # Changes committed when exiting context
```

## Integration with Workflows

### Using Registry in Workflows

```python
from latch import workflow, small_task
from latch.types import LatchFile
from latch.registry.table import Table
from latch.registry.record import Record

@small_task
def process_and_save(sample_id: str, table_id: str) -> str:
    # Get sample from registry
    table = Table.get(table_id=table_id)
    records = Record.list(
        table_id=table_id,
        filter={"sample_id": sample_id}
    )
    sample = records[0]

    # Process file
    input_file = sample.values["fastq_file"]
    # ... processing logic ...

    # Save results back to registry
    sample.update(values={
        "status": "completed",
        "results_file": output_file
    })

    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """Workflow integrated with Registry"""
    return process_and_save(sample_id=sample_id, table_id=table_id)
```

### Automatic Workflow Execution on Data

Configure workflows to run automatically when data is added to Registry folders:

```python
from latch.resources.launch_plan import LaunchPlan

# Create launch plan that watches a folder
launch_plan = LaunchPlan.create(
    workflow_name="rnaseq_pipeline",
    name="auto_process",
    trigger_folder="latch:///incoming_data",
    default_inputs={
        "output_dir": "latch:///results"
    }
)
```

## Account and Workspace Management

### Account Information

```python
from latch.account import Account

# Get current account
account = Account.current()

# Account properties
workspace_id = account.id
workspace_name = account.name
```

### Team Workspaces

Access shared team workspaces:

```python
# List available workspaces
workspaces = Account.list()

# Switch workspace
Account.set_current(workspace_id="ws_789")
```

## Functions for Data Operations

### Joining Data

The `latch.functions` module provides data manipulation utilities:

```python
from latch.functions import left_join, inner_join, outer_join, right_join

# Join tables
combined = left_join(
    left_table=table1,
    right_table=table2,
    on="sample_id"
)
```

### Filtering

```python
from latch.functions import filter_records

# Filter records
filtered = filter_records(
    table=table,
    condition=lambda record: record["replicate"] > 1
)
```

### Secrets Management

Store and retrieve secrets securely:

```python
from latch.functions import get_secret

# Retrieve secret in workflow
api_key = get_secret("api_key")
```

## Best Practices

1. **Path Organization**: Use consistent folder structure (e.g., `/data`, `/results`, `/logs`)
2. **Registry Schema**: Define table schemas before bulk data entry
3. **Linked Records**: Use links to maintain relationships between experiments
4. **Bulk Operations**: Use transactions for updating multiple records
5. **File Naming**: Use consistent, descriptive file naming conventions
6. **Metadata**: Store experimental metadata in Registry for traceability
7. **Validation**: Validate data types when creating records
8. **Cleanup**: Regularly archive or delete unused data

## Common Patterns

### Sample Tracking

```python
# Create samples table
samples = Table.create(
    project_id=project.id,
    name="Samples",
    columns=[
        {"name": "sample_id", "type": "string"},
        {"name": "collection_date", "type": "date"},
        {"name": "raw_fastq_r1", "type": "file"},
        {"name": "raw_fastq_r2", "type": "file"},
        {"name": "status", "type": "enum", "options": ["pending", "processing", "complete"]}
    ]
)
```

### Results Organization

```python
# Create results table linked to samples
results = Table.create(
    project_id=project.id,
    name="Analysis Results",
    columns=[
        {"name": "sample", "type": "link", "target_table": samples.id},
        {"name": "alignment_bam", "type": "file"},
        {"name": "variants_vcf", "type": "file"},
        {"name": "qc_metrics", "type": "file"}
    ]
)
```

---

## Reference: Resource Configuration

# Resource Configuration

## Overview
Latch SDK provides flexible resource configuration for workflow tasks, enabling efficient execution on appropriate compute infrastructure including CPU, GPU, and memory-optimized instances.

## Task Resource Decorators

### Standard Decorators

The SDK provides pre-configured task decorators for common resource requirements:

#### @small_task
Default configuration for lightweight tasks:
```python
from latch import small_task

@small_task
def lightweight_processing():
    """Minimal resource requirements"""
    pass
```

**Use cases:**
- File parsing and manipulation
- Simple data transformations
- Quick QC checks
- Metadata operations

#### @large_task
Increased CPU and memory for intensive computations:
```python
from latch import large_task

@large_task
def intensive_computation():
    """Higher CPU and memory allocation"""
    pass
```

**Use cases:**
- Large file processing
- Complex statistical analyses
- Assembly tasks
- Multi-threaded operations

#### @small_gpu_task
GPU-enabled with minimal resources:
```python
from latch import small_gpu_task

@small_gpu_task
def gpu_inference():
    """GPU-enabled task with basic resources"""
    pass
```

**Use cases:**
- Neural network inference
- Small-scale ML predictions
- GPU-accelerated libraries

#### @large_gpu_task
GPU-enabled with maximum resources:
```python
from latch import large_gpu_task

@large_gpu_task
def gpu_training():
    """GPU with maximum CPU and memory"""
    pass
```

**Use cases:**
- Deep learning model training
- Protein structure prediction (AlphaFold)
- Large-scale GPU computations

### Custom Task Configuration

For precise control, use the `@custom_task` decorator:

```python
from latch import custom_task
from latch.resources.tasks import TaskResources

@custom_task(
    cpu=8,
    memory=32,  # GB
    storage_gib=100,
    timeout=3600,  # seconds
)
def custom_processing():
    """Task with custom resource specifications"""
    pass
```

#### Custom Task Parameters

- **cpu**: Number of CPU cores (integer)
- **memory**: Memory in GB (integer)
- **storage_gib**: Ephemeral storage in GiB (integer)
- **timeout**: Maximum execution time in seconds (integer)
- **gpu**: Number of GPUs (integer, 0 for CPU-only)
- **gpu_type**: Specific GPU model (string, e.g., "nvidia-tesla-v100")

### Advanced Custom Configuration

```python
from latch.resources.tasks import TaskResources

@custom_task(
    cpu=16,
    memory=64,
    storage_gib=500,
    timeout=7200,
    gpu=1,
    gpu_type="nvidia-tesla-a100"
)
def alphafold_prediction():
    """AlphaFold with A100 GPU and high memory"""
    pass
```

## GPU Configuration

### GPU Types

Available GPU options:
- **nvidia-tesla-k80**: Basic GPU for testing
- **nvidia-tesla-v100**: High-performance for training
- **nvidia-tesla-a100**: Latest generation for maximum performance

### Multi-GPU Tasks

```python
from latch import custom_task

@custom_task(
    cpu=32,
    memory=128,
    gpu=4,
    gpu_type="nvidia-tesla-v100"
)
def multi_gpu_training():
    """Distributed training across multiple GPUs"""
    pass
```

## Resource Selection Strategies

### By Computational Requirements

**Memory-Intensive Tasks:**
```python
@custom_task(cpu=4, memory=128)  # High memory, moderate CPU
def genome_assembly():
    pass
```

**CPU-Intensive Tasks:**
```python
@custom_task(cpu=64, memory=32)  # High CPU, moderate memory
def parallel_alignment():
    pass
```

**I/O-Intensive Tasks:**
```python
@custom_task(cpu=8, memory=16, storage_gib=1000)  # Large ephemeral storage
def data_preprocessing():
    pass
```

### By Workflow Phase

**Quick Validation:**
```python
@small_task
def validate_inputs():
    """Fast input validation"""
    pass
```

**Main Computation:**
```python
@large_task
def primary_analysis():
    """Resource-intensive analysis"""
    pass
```

**Result Aggregation:**
```python
@small_task
def aggregate_results():
    """Lightweight result compilation"""
    pass
```

## Workflow Resource Planning

### Complete Pipeline Example

```python
from latch import workflow, small_task, large_task, large_gpu_task
from latch.types import LatchFile

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """QC doesn't need much resources"""
    return qc_output

@large_task
def alignment(fastq: LatchFile) -> LatchFile:
    """Alignment benefits from more CPU"""
    return bam_output

@large_gpu_task
def variant_calling(bam: LatchFile) -> LatchFile:
    """GPU-accelerated variant caller"""
    return vcf_output

@small_task
def generate_report(vcf: LatchFile) -> LatchFile:
    """Simple report generation"""
    return report

@workflow
def genomics_pipeline(input_fastq: LatchFile) -> LatchFile:
    """Resource-optimized genomics pipeline"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc)
    variants = variant_calling(bam=aligned)
    return generate_report(vcf=variants)
```

## Timeout Configuration

### Setting Timeouts

```python
from latch import custom_task

@custom_task(
    cpu=8,
    memory=32,
    timeout=10800  # 3 hours in seconds
)
def long_running_analysis():
    """Analysis with extended timeout"""
    pass
```

### Timeout Best Practices

1. **Estimate conservatively**: Add buffer time beyond expected duration
2. **Monitor actual runtimes**: Adjust based on real execution data
3. **Default timeout**: Most tasks have 1-hour default
4. **Maximum timeout**: Check platform limits for very long jobs

## Storage Configuration

### Ephemeral Storage

Configure temporary storage for intermediate files:

```python
@custom_task(
    cpu=8,
    memory=32,
    storage_gib=500  # 500 GB temporary storage
)
def process_large_dataset():
    """Task with large intermediate files"""
    # Ephemeral storage available at /tmp
    temp_file = "/tmp/intermediate_data.bam"
    pass
```

### Storage Guidelines

- Default storage is typically sufficient for most tasks
- Specify larger storage for tasks with large intermediate files
- Ephemeral storage is cleared after task completion
- Use LatchDir for persistent storage needs

## Cost Optimization

### Resource Efficiency Tips

1. **Right-size resources**: Don't over-allocate
2. **Use appropriate decorators**: Start with standard decorators
3. **GPU only when needed**: GPU tasks cost more
4. **Parallel small tasks**: Better than one large task
5. **Monitor usage**: Review actual resource utilization

### Example: Cost-Effective Design

```python
# INEFFICIENT: All tasks use large resources
@large_task
def validate_input():  # Over-provisioned
    pass

@large_task
def simple_transformation():  # Over-provisioned
    pass

# EFFICIENT: Right-sized resources
@small_task
def validate_input():  # Appropriate
    pass

@small_task
def simple_transformation():  # Appropriate
    pass

@large_task
def intensive_analysis():  # Appropriate
    pass
```

## Monitoring and Debugging

### Resource Usage Monitoring

During workflow execution, monitor:
- CPU utilization
- Memory usage
- GPU utilization (if applicable)
- Execution duration
- Storage consumption

### Common Resource Issues

**Out of Memory (OOM):**
```python
# Solution: Increase memory allocation
@custom_task(cpu=8, memory=64)  # Increased from 32 to 64 GB
def memory_intensive_task():
    pass
```

**Timeout:**
```python
# Solution: Increase timeout
@custom_task(cpu=8, memory=32, timeout=14400)  # 4 hours
def long_task():
    pass
```

**Insufficient Storage:**
```python
# Solution: Increase ephemeral storage
@custom_task(cpu=8, memory=32, storage_gib=1000)
def large_intermediate_files():
    pass
```

## Conditional Resources

Dynamically allocate resources based on input:

```python
from latch import workflow, custom_task
from latch.types import LatchFile

def get_resource_config(file_size_gb: float):
    """Determine resources based on file size"""
    if file_size_gb < 10:
        return {"cpu": 4, "memory": 16}
    elif file_size_gb < 100:
        return {"cpu": 16, "memory": 64}
    else:
        return {"cpu": 32, "memory": 128}

# Note: Resource decorators must be static
# Use multiple task variants for different sizes
@custom_task(cpu=4, memory=16)
def process_small(file: LatchFile) -> LatchFile:
    pass

@custom_task(cpu=16, memory=64)
def process_medium(file: LatchFile) -> LatchFile:
    pass

@custom_task(cpu=32, memory=128)
def process_large(file: LatchFile) -> LatchFile:
    pass
```

## Best Practices Summary

1. **Start small**: Begin with standard decorators, scale up if needed
2. **Profile first**: Run test executions to determine actual needs
3. **GPU sparingly**: Only use GPU when algorithms support it
4. **Parallel design**: Break into smaller tasks when possible
5. **Monitor and adjust**: Review execution metrics and optimize
6. **Document requirements**: Comment why specific resources are needed
7. **Test locally**: Use Docker locally to validate before registration
8. **Consider cost**: Balance performance with cost efficiency

## Platform-Specific Considerations

### Available Resources

Latch platform provides:
- CPU instances: Up to 96 cores
- Memory: Up to 768 GB
- GPUs: K80, V100, A100 variants
- Storage: Configurable ephemeral storage

### Resource Limits

Check current platform limits:
- Maximum CPUs per task
- Maximum memory per task
- Maximum GPU allocation
- Maximum concurrent tasks

### Quotas and Limits

Be aware of workspace quotas:
- Total concurrent executions
- Total resource allocation
- Storage limits
- Execution time limits

Contact Latch support for quota increases if needed.

---

## Reference: Verified Workflows

# Verified Workflows

## Overview
Latch Verified Workflows are production-ready, pre-built bioinformatics pipelines developed and maintained by Latch engineers. These workflows are used by top pharmaceutical companies and biotech firms for research and discovery.

## Available in Python SDK

The `latch.verified` module provides programmatic access to verified workflows from Python code.

### Importing Verified Workflows

```python
from latch.verified import (
    bulk_rnaseq,
    deseq2,
    mafft,
    trim_galore,
    alphafold,
    colabfold
)
```

## Core Verified Workflows

### Bulk RNA-seq Analysis

**Alignment and Quantification:**
```python
from latch.verified import bulk_rnaseq
from latch.types import LatchFile

# Run bulk RNA-seq pipeline
results = bulk_rnaseq(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    fastq_r2=LatchFile("latch:///data/sample_R2.fastq.gz"),
    reference_genome="hg38",
    output_dir="latch:///results/rnaseq"
)
```

**Features:**
- Read quality control with FastQC
- Adapter trimming
- Alignment with STAR or HISAT2
- Gene-level quantification with featureCounts
- MultiQC report generation

### Differential Expression Analysis

**DESeq2:**
```python
from latch.verified import deseq2
from latch.types import LatchFile

# Run differential expression analysis
results = deseq2(
    count_matrix=LatchFile("latch:///data/counts.csv"),
    sample_metadata=LatchFile("latch:///data/metadata.csv"),
    design_formula="~ condition",
    output_dir="latch:///results/deseq2"
)
```

**Features:**
- Normalization and variance stabilization
- Differential expression testing
- MA plots and volcano plots
- PCA visualization
- Annotated results tables

### Pathway Analysis

**Enrichment Analysis:**
```python
from latch.verified import pathway_enrichment

results = pathway_enrichment(
    gene_list=LatchFile("latch:///data/deg_list.txt"),
    organism="human",
    databases=["GO_Biological_Process", "KEGG", "Reactome"],
    output_dir="latch:///results/pathways"
)
```

**Supported Databases:**
- Gene Ontology (GO)
- KEGG pathways
- Reactome
- WikiPathways
- MSigDB collections

### Sequence Alignment

**MAFFT Multiple Sequence Alignment:**
```python
from latch.verified import mafft
from latch.types import LatchFile

aligned = mafft(
    input_fasta=LatchFile("latch:///data/sequences.fasta"),
    algorithm="auto",
    output_format="fasta"
)
```

**Features:**
- Multiple alignment algorithms (FFT-NS-1, FFT-NS-2, G-INS-i, L-INS-i)
- Automatic algorithm selection
- Support for large alignments
- Various output formats

### Adapter and Quality Trimming

**Trim Galore:**
```python
from latch.verified import trim_galore

trimmed = trim_galore(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    fastq_r2=LatchFile("latch:///data/sample_R2.fastq.gz"),
    quality_threshold=20,
    adapter_auto_detect=True
)
```

**Features:**
- Automatic adapter detection
- Quality trimming
- FastQC integration
- Support for single-end and paired-end

## Protein Structure Prediction

### AlphaFold

**Standard AlphaFold:**
```python
from latch.verified import alphafold
from latch.types import LatchFile

structure = alphafold(
    sequence_fasta=LatchFile("latch:///data/protein.fasta"),
    model_preset="monomer",
    use_templates=True,
    output_dir="latch:///results/alphafold"
)
```

**Features:**
- Monomer and multimer prediction
- Template-based modeling option
- MSA generation
- Confidence metrics (pLDDT, PAE)
- PDB structure output

**Model Presets:**
- `monomer`: Single protein chain
- `monomer_casp14`: CASP14 competition version
- `monomer_ptm`: With pTM confidence
- `multimer`: Protein complexes

### ColabFold

**Optimized AlphaFold Alternative:**
```python
from latch.verified import colabfold

structure = colabfold(
    sequence_fasta=LatchFile("latch:///data/protein.fasta"),
    num_models=5,
    use_amber_relax=True,
    output_dir="latch:///results/colabfold"
)
```

**Features:**
- Faster than standard AlphaFold
- MMseqs2-based MSA generation
- Multiple model predictions
- Amber relaxation
- Ranking by confidence

**Advantages:**
- 3-5x faster MSA generation
- Lower compute cost
- Similar accuracy to AlphaFold

## Single-Cell Analysis

### ArchR (scATAC-seq)

**Chromatin Accessibility Analysis:**
```python
from latch.verified import archr

results = archr(
    fragments_file=LatchFile("latch:///data/fragments.tsv.gz"),
    genome="hg38",
    output_dir="latch:///results/archr"
)
```

**Features:**
- Arrow file generation
- Quality control metrics
- Dimensionality reduction
- Clustering
- Peak calling
- Motif enrichment

### scVelo (RNA Velocity)

**RNA Velocity Analysis:**
```python
from latch.verified import scvelo

results = scvelo(
    adata_file=LatchFile("latch:///data/adata.h5ad"),
    mode="dynamical",
    output_dir="latch:///results/scvelo"
)
```

**Features:**
- Spliced/unspliced quantification
- Velocity estimation
- Dynamical modeling
- Trajectory inference
- Visualization

### emptyDropsR (Cell Calling)

**Empty Droplet Detection:**
```python
from latch.verified import emptydrops

filtered_matrix = emptydrops(
    raw_matrix_dir=LatchDir("latch:///data/raw_feature_bc_matrix"),
    fdr_threshold=0.01
)
```

**Features:**
- Distinguish cells from empty droplets
- FDR-based thresholding
- Ambient RNA removal
- Compatible with 10X data

## Gene Editing Analysis

### CRISPResso2

**CRISPR Editing Assessment:**
```python
from latch.verified import crispresso2

results = crispresso2(
    fastq_r1=LatchFile("latch:///data/sample_R1.fastq.gz"),
    amplicon_sequence="AGCTAGCTAG...",
    guide_rna="GCTAGCTAGC",
    output_dir="latch:///results/crispresso"
)
```

**Features:**
- Indel quantification
- Base editing analysis
- Prime editing analysis
- HDR quantification
- Allele frequency plots

## Phylogenetics

### Phylogenetic Tree Construction

```python
from latch.verified import phylogenetics

tree = phylogenetics(
    alignment_file=LatchFile("latch:///data/aligned.fasta"),
    method="maximum_likelihood",
    bootstrap_replicates=1000,
    output_dir="latch:///results/phylo"
)
```

**Features:**
- Multiple tree-building methods
- Bootstrap support
- Tree visualization
- Model selection

## Workflow Integration

### Using Verified Workflows in Custom Pipelines

```python
from latch import workflow, small_task
from latch.verified import bulk_rnaseq, deseq2
from latch.types import LatchFile, LatchDir

@workflow
def complete_rnaseq_analysis(
    fastq_files: List[LatchFile],
    metadata: LatchFile,
    output_dir: LatchDir
) -> LatchFile:
    """
    Complete RNA-seq analysis pipeline using verified workflows
    """
    # Run alignment for each sample
    aligned_samples = []
    for fastq in fastq_files:
        result = bulk_rnaseq(
            fastq_r1=fastq,
            reference_genome="hg38",
            output_dir=output_dir
        )
        aligned_samples.append(result)

    # Aggregate counts and run differential expression
    count_matrix = aggregate_counts(aligned_samples)
    deseq_results = deseq2(
        count_matrix=count_matrix,
        sample_metadata=metadata,
        design_formula="~ condition"
    )

    return deseq_results
```

## Best Practices

### When to Use Verified Workflows

**Use Verified Workflows for:**
1. Standard analysis pipelines
2. Well-established methods
3. Production-ready analyses
4. Reproducible research
5. Validated bioinformatics tools

**Build Custom Workflows for:**
1. Novel analysis methods
2. Custom preprocessing steps
3. Integration with proprietary tools
4. Experimental pipelines
5. Highly specialized workflows

### Combining Verified and Custom

```python
from latch import workflow, small_task
from latch.verified import alphafold
from latch.types import LatchFile

@small_task
def preprocess_sequence(raw_fasta: LatchFile) -> LatchFile:
    """Custom preprocessing"""
    # Custom logic here
    return processed_fasta

@small_task
def postprocess_structure(pdb_file: LatchFile) -> LatchFile:
    """Custom post-analysis"""
    # Custom analysis here
    return analysis_results

@workflow
def custom_structure_pipeline(input_fasta: LatchFile) -> LatchFile:
    """
    Combine custom steps with verified AlphaFold
    """
    # Custom preprocessing
    processed = preprocess_sequence(raw_fasta=input_fasta)

    # Use verified AlphaFold
    structure = alphafold(
        sequence_fasta=processed,
        model_preset="monomer_ptm"
    )

    # Custom post-processing
    results = postprocess_structure(pdb_file=structure)

    return results
```

## Accessing Workflow Documentation

### In-Platform Documentation

Each verified workflow includes:
- Parameter descriptions
- Input/output specifications
- Method details
- Citation information
- Example usage

### Viewing Available Workflows

```python
from latch.verified import list_workflows

# List all available verified workflows
workflows = list_workflows()

for workflow in workflows:
    print(f"{workflow.name}: {workflow.description}")
```

## Version Management

### Workflow Versions

Verified workflows are versioned and maintained:
- Bug fixes and improvements
- New features added
- Backward compatibility maintained
- Version pinning available

### Using Specific Versions

```python
from latch.verified import bulk_rnaseq

# Use specific version
results = bulk_rnaseq(
    fastq_r1=input_file,
    reference_genome="hg38",
    workflow_version="2.1.0"
)
```

## Support and Updates

### Getting Help

- **Documentation**: https://docs.latch.bio
- **Slack Community**: Latch SDK workspace
- **Support**: support@latch.bio
- **GitHub Issues**: Report bugs and request features

### Workflow Updates

Verified workflows receive regular updates:
- Tool version upgrades
- Performance improvements
- Bug fixes
- New features

Subscribe to release notes for update notifications.

## Common Use Cases

### Complete RNA-seq Study

```python
# 1. Quality control and alignment
aligned = bulk_rnaseq(fastq=samples)

# 2. Differential expression
deg = deseq2(counts=aligned)

# 3. Pathway enrichment
pathways = pathway_enrichment(genes=deg)
```

### Protein Structure Analysis

```python
# 1. Predict structure
structure = alphafold(sequence=protein_seq)

# 2. Custom analysis
results = analyze_structure(pdb=structure)
```

### Single-Cell Workflow

```python
# 1. Filter cells
filtered = emptydrops(matrix=raw_counts)

# 2. RNA velocity
velocity = scvelo(adata=filtered)
```

---

## Reference: Workflow Creation

# Workflow Creation and Registration

## Overview
The Latch SDK enables defining serverless bioinformatics workflows using Python decorators and deploying them with automatic containerization and UI generation.

## Installation

Install the Latch SDK:
```bash
python3 -m pip install latch
```

**Prerequisites:**
- Docker must be installed and running locally
- Latch account credentials

## Initializing a New Workflow

Create a new workflow template:
```bash
latch init <workflow-name>
```

This generates a workflow directory with:
- `wf/__init__.py` - Main workflow definition
- `Dockerfile` - Container configuration
- `version` - Version tracking file

## Workflow Definition Structure

### Basic Workflow Example

```python
from latch import workflow
from latch.types import LatchFile, LatchDir

@workflow
def my_workflow(input_file: LatchFile, output_dir: LatchDir) -> LatchFile:
    """
    Workflow description that appears in the UI

    Args:
        input_file: Input file description
        output_dir: Output directory description
    """
    return process_task(input_file, output_dir)
```

### Task Definition

Tasks are the individual computation steps within workflows:

```python
from latch import small_task, large_task

@small_task
def process_task(input_file: LatchFile, output_dir: LatchDir) -> LatchFile:
    """Task-level computation"""
    # Processing logic here
    return output_file
```

### Task Resource Decorators

The SDK provides multiple task decorators for different resource requirements:

- `@small_task` - Default resources for lightweight tasks
- `@large_task` - Increased memory and CPU
- `@small_gpu_task` - GPU-enabled tasks with minimal resources
- `@large_gpu_task` - GPU-enabled tasks with maximum resources
- `@custom_task` - Custom resource specifications

## Registering Workflows

Register the workflow to the Latch platform:
```bash
latch register <workflow-directory>
```

The registration process:
1. Builds Docker container with all dependencies
2. Serializes workflow code
3. Uploads container to registry
4. Generates no-code UI automatically
5. Makes workflow available on the platform

### Registration Output

Upon successful registration:
- Workflow appears in Latch workspace
- Automatic UI is generated with parameter forms
- Version is tracked and containerized
- Workflow can be executed immediately

## Supporting Multiple Pipeline Languages

Latch supports uploading existing pipelines in:
- **Python** - Native Latch SDK workflows
- **Nextflow** - Import existing Nextflow pipelines
- **Snakemake** - Import existing Snakemake pipelines

### Nextflow Integration

Import Nextflow pipelines:
```bash
latch register --nextflow <nextflow-directory>
```

### Snakemake Integration

Import Snakemake pipelines:
```bash
latch register --snakemake <snakemake-directory>
```

## Workflow Execution

### From CLI

Execute a registered workflow:
```bash
latch execute <workflow-name> --input-file <path> --output-dir <path>
```

### From Python

Execute workflows programmatically:
```python
from latch.account import Account
from latch.executions import execute_workflow

account = Account.current()
execution = execute_workflow(
    workflow_name="my_workflow",
    parameters={
        "input_file": "/path/to/file",
        "output_dir": "/path/to/output"
    }
)
```

## Launch Plans

Launch plans define preset parameter configurations:

```python
from latch.resources.launch_plan import LaunchPlan

# Define a launch plan with preset parameters
launch_plan = LaunchPlan.create(
    workflow_name="my_workflow",
    name="default_config",
    default_inputs={
        "input_file": "/data/sample.fastq",
        "output_dir": "/results"
    }
)
```

## Conditional Sections

Create dynamic UIs with conditional parameter sections:

```python
from latch.types import LatchParameter
from latch.resources.conditional import conditional_section

@workflow
def my_workflow(
    mode: str,
    advanced_param: str = conditional_section(
        condition=lambda inputs: inputs.mode == "advanced"
    )
):
    """Workflow with conditional parameters"""
    pass
```

## Best Practices

1. **Type Annotations**: Always use type hints for workflow parameters
2. **Docstrings**: Provide clear docstrings - they populate the UI descriptions
3. **Version Control**: Use semantic versioning for workflow updates
4. **Testing**: Test workflows locally before registration
5. **Resource Sizing**: Start with smaller resource decorators and scale up as needed
6. **Modular Design**: Break complex workflows into reusable tasks
7. **Error Handling**: Implement proper error handling in tasks
8. **Logging**: Use Python logging for debugging and monitoring

## Common Patterns

### Multi-Step Pipeline

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def quality_control(input_file: LatchFile) -> LatchFile:
    """QC step"""
    return qc_output

@small_task
def alignment(qc_file: LatchFile) -> LatchFile:
    """Alignment step"""
    return aligned_output

@workflow
def rnaseq_pipeline(input_fastq: LatchFile) -> LatchFile:
    """RNA-seq analysis pipeline"""
    qc_result = quality_control(input_file=input_fastq)
    aligned = alignment(qc_file=qc_result)
    return aligned
```

### Parallel Processing

```python
from typing import List
from latch import workflow, small_task, map_task
from latch.types import LatchFile

@small_task
def process_sample(sample: LatchFile) -> LatchFile:
    """Process individual sample"""
    return processed_sample

@workflow
def batch_pipeline(samples: List[LatchFile]) -> List[LatchFile]:
    """Process multiple samples in parallel"""
    return map_task(process_sample)(sample=samples)
```

## Troubleshooting

### Common Issues

1. **Docker not running**: Ensure Docker daemon is active
2. **Authentication errors**: Run `latch login` to refresh credentials
3. **Build failures**: Check Dockerfile for missing dependencies
4. **Type errors**: Ensure all parameters have proper type annotations

### Debug Mode

Enable verbose logging during registration:
```bash
latch register --verbose <workflow-directory>
```

## References

- Official Documentation: https://docs.latch.bio
- GitHub Repository: https://github.com/latchbio/latch
- Slack Community: https://join.slack.com/t/latchbiosdk
