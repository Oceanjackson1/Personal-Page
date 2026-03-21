---
title: "Dnanexus Integration"
description: "DNAnexus cloud genomics platform. Build apps/applets, manage data (upload/download), dxpy Python SDK, run workflows, FASTQ/BAM/VCF, for genomics pipeline development and execution."
category: "devops"
source: "community"
author: "Community"
tags: ["dnanexus", "integration"]
date: 2026-03-20
---

# DNAnexus Integration

## Overview

DNAnexus is a cloud platform for biomedical data analysis and genomics. Build and deploy apps/applets, manage data objects, run workflows, and use the dxpy Python SDK for genomics pipeline development and execution.

## When to Use This Skill

This skill should be used when:
- Creating, building, or modifying DNAnexus apps/applets
- Uploading, downloading, searching, or organizing files and records
- Running analyses, monitoring jobs, creating workflows
- Writing scripts using dxpy to interact with the platform
- Setting up dxapp.json, managing dependencies, using Docker
- Processing FASTQ, BAM, VCF, or other bioinformatics files
- Managing projects, permissions, or platform resources

## Core Capabilities

The skill is organized into five main areas, each with detailed reference documentation:

### 1. App Development

**Purpose**: Create executable programs (apps/applets) that run on the DNAnexus platform.

**Key Operations**:
- Generate app skeleton with `dx-app-wizard`
- Write Python or Bash apps with proper entry points
- Handle input/output data objects
- Deploy with `dx build` or `dx build --app`
- Test apps on the platform

**Common Use Cases**:
- Bioinformatics pipelines (alignment, variant calling)
- Data processing workflows
- Quality control and filtering
- Format conversion tools

**Reference**: See `references/app-development.md` for:
- Complete app structure and patterns
- Python entry point decorators
- Input/output handling with dxpy
- Development best practices
- Common issues and solutions

### 2. Data Operations

**Purpose**: Manage files, records, and other data objects on the platform.

**Key Operations**:
- Upload/download files with `dxpy.upload_local_file()` and `dxpy.download_dxfile()`
- Create and manage records with metadata
- Search for data objects by name, properties, or type
- Clone data between projects
- Manage project folders and permissions

**Common Use Cases**:
- Uploading sequencing data (FASTQ files)
- Organizing analysis results
- Searching for specific samples or experiments
- Backing up data across projects
- Managing reference genomes and annotations

**Reference**: See `references/data-operations.md` for:
- Complete file and record operations
- Data object lifecycle (open/closed states)
- Search and discovery patterns
- Project management
- Batch operations

### 3. Job Execution

**Purpose**: Run analyses, monitor execution, and orchestrate workflows.

**Key Operations**:
- Launch jobs with `applet.run()` or `app.run()`
- Monitor job status and logs
- Create subjobs for parallel processing
- Build and run multi-step workflows
- Chain jobs with output references

**Common Use Cases**:
- Running genomics analyses on sequencing data
- Parallel processing of multiple samples
- Multi-step analysis pipelines
- Monitoring long-running computations
- Debugging failed jobs

**Reference**: See `references/job-execution.md` for:
- Complete job lifecycle and states
- Workflow creation and orchestration
- Parallel execution patterns
- Job monitoring and debugging
- Resource management

### 4. Python SDK (dxpy)

**Purpose**: Programmatic access to DNAnexus platform through Python.

**Key Operations**:
- Work with data object handlers (DXFile, DXRecord, DXApplet, etc.)
- Use high-level functions for common tasks
- Make direct API calls for advanced operations
- Create links and references between objects
- Search and discover platform resources

**Common Use Cases**:
- Automation scripts for data management
- Custom analysis pipelines
- Batch processing workflows
- Integration with external tools
- Data migration and organization

**Reference**: See `references/python-sdk.md` for:
- Complete dxpy class reference
- High-level utility functions
- API method documentation
- Error handling patterns
- Common code patterns

### 5. Configuration and Dependencies

**Purpose**: Configure app metadata and manage dependencies.

**Key Operations**:
- Write dxapp.json with inputs, outputs, and run specs
- Install system packages (execDepends)
- Bundle custom tools and resources
- Use assets for shared dependencies
- Integrate Docker containers
- Configure instance types and timeouts

**Common Use Cases**:
- Defining app input/output specifications
- Installing bioinformatics tools (samtools, bwa, etc.)
- Managing Python package dependencies
- Using Docker images for complex environments
- Selecting computational resources

**Reference**: See `references/configuration.md` for:
- Complete dxapp.json specification
- Dependency management strategies
- Docker integration patterns
- Regional and resource configuration
- Example configurations

## Quick Start Examples

### Upload and Analyze Data

```python
import dxpy

# Upload input file
input_file = dxpy.upload_local_file("sample.fastq", project="project-xxxx")

# Run analysis
job = dxpy.DXApplet("applet-xxxx").run({
    "reads": dxpy.dxlink(input_file.get_id())
})

# Wait for completion
job.wait_on_done()

# Download results
output_id = job.describe()["output"]["aligned_reads"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "aligned.bam")
```

### Search and Download Files

```python
import dxpy

# Find BAM files from a specific experiment
files = dxpy.find_data_objects(
    classname="file",
    name="*.bam",
    properties={"experiment": "exp001"},
    project="project-xxxx"
)

# Download each file
for file_result in files:
    file_obj = dxpy.DXFile(file_result["id"])
    filename = file_obj.describe()["name"]
    dxpy.download_dxfile(file_result["id"], filename)
```

### Create Simple App

```python
# src/my-app.py
import dxpy
import subprocess

@dxpy.entry_point('main')
def main(input_file, quality_threshold=30):
    # Download input
    dxpy.download_dxfile(input_file["$dnanexus_link"], "input.fastq")

    # Process
    subprocess.check_call([
        "quality_filter",
        "--input", "input.fastq",
        "--output", "filtered.fastq",
        "--threshold", str(quality_threshold)
    ])

    # Upload output
    output_file = dxpy.upload_local_file("filtered.fastq")

    return {
        "filtered_reads": dxpy.dxlink(output_file)
    }

dxpy.run()
```

## Workflow Decision Tree

When working with DNAnexus, follow this decision tree:

1. **Need to create a new executable?**
   - Yes → Use **App Development** (references/app-development.md)
   - No → Continue to step 2

2. **Need to manage files or data?**
   - Yes → Use **Data Operations** (references/data-operations.md)
   - No → Continue to step 3

3. **Need to run an analysis or workflow?**
   - Yes → Use **Job Execution** (references/job-execution.md)
   - No → Continue to step 4

4. **Writing Python scripts for automation?**
   - Yes → Use **Python SDK** (references/python-sdk.md)
   - No → Continue to step 5

5. **Configuring app settings or dependencies?**
   - Yes → Use **Configuration** (references/configuration.md)

Often you'll need multiple capabilities together (e.g., app development + configuration, or data operations + job execution).

## Installation and Authentication

### Install dxpy

```bash
uv pip install dxpy
```

### Login to DNAnexus

```bash
dx login
```

This authenticates your session and sets up access to projects and data.

### Verify Installation

```bash
dx --version
dx whoami
```

## Common Patterns

### Pattern 1: Batch Processing

Process multiple files with the same analysis:

```python
# Find all FASTQ files
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# Launch parallel jobs
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# Wait for all completions
for job in jobs:
    job.wait_on_done()
```

### Pattern 2: Multi-Step Pipeline

Chain multiple analyses together:

```python
# Step 1: Quality control
qc_job = qc_applet.run({"reads": input_file})

# Step 2: Alignment (uses QC output)
align_job = align_applet.run({
    "reads": qc_job.get_output_ref("filtered_reads")
})

# Step 3: Variant calling (uses alignment output)
variant_job = variant_applet.run({
    "bam": align_job.get_output_ref("aligned_bam")
})
```

### Pattern 3: Data Organization

Organize analysis results systematically:

```python
# Create organized folder structure
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/experiments/exp001/results", "parents": True}
)

# Upload with metadata
result_file = dxpy.upload_local_file(
    "results.txt",
    project="project-xxxx",
    folder="/experiments/exp001/results",
    properties={
        "experiment": "exp001",
        "sample": "sample1",
        "analysis_date": "2025-10-20"
    },
    tags=["validated", "published"]
)
```

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
2. **Resource Management**: Choose appropriate instance types for workloads
3. **Data Organization**: Use consistent folder structures and metadata
4. **Cost Optimization**: Archive old data, use appropriate storage classes
5. **Documentation**: Include clear descriptions in dxapp.json
6. **Testing**: Test apps with various input types before production use
7. **Version Control**: Use semantic versioning for apps
8. **Security**: Never hardcode credentials in source code
9. **Logging**: Include informative log messages for debugging
10. **Cleanup**: Remove temporary files and failed jobs

## Resources

This skill includes detailed reference documentation:

### references/

- **app-development.md** - Complete guide to building and deploying apps/applets
- **data-operations.md** - File management, records, search, and project operations
- **job-execution.md** - Running jobs, workflows, monitoring, and parallel processing
- **python-sdk.md** - Comprehensive dxpy library reference with all classes and functions
- **configuration.md** - dxapp.json specification and dependency management

Load these references when you need detailed information about specific operations or when working on complex tasks.

## Getting Help

- Official documentation: https://documentation.dnanexus.com/
- API reference: http://autodoc.dnanexus.com/
- GitHub repository: https://github.com/dnanexus/dx-toolkit
- Support: support@dnanexus.com

---

## Reference: App Development

# DNAnexus App Development

## Overview

Apps and applets are executable programs that run on the DNAnexus platform. They can be written in Python or Bash and are deployed with all necessary dependencies and configuration.

## Applets vs Apps

- **Applets**: Data objects that live inside projects. Good for development and testing.
- **Apps**: Versioned, shareable executables that don't live inside projects. Can be published for others to use.

Both are created identically until the final build step. Applets can be converted to apps later.

## Creating an App/Applet

### Using dx-app-wizard

Generate a skeleton app directory structure:

```bash
dx-app-wizard
```

This creates:
- `dxapp.json` - Configuration file
- `src/` - Source code directory
- `resources/` - Bundled dependencies
- `test/` - Test files

### Building and Deploying

Build an applet:
```bash
dx build
```

Build an app:
```bash
dx build --app
```

The build process:
1. Validates dxapp.json configuration
2. Bundles source code and resources
3. Deploys to the platform
4. Returns the applet/app ID

## App Directory Structure

```
my-app/
├── dxapp.json          # Metadata and configuration
├── src/
│   └── my-app.py       # Main executable (Python)
│   └── my-app.sh       # Or Bash script
├── resources/          # Bundled files and dependencies
│   └── tools/
│   └── data/
└── test/               # Test data and scripts
    └── test.json
```

## Python App Structure

### Entry Points

Python apps use the `@dxpy.entry_point()` decorator to define functions:

```python
import dxpy

@dxpy.entry_point('main')
def main(input1, input2):
    # Process inputs
    # Return outputs
    return {
        "output1": result1,
        "output2": result2
    }

dxpy.run()
```

### Input/Output Handling

**Inputs**: DNAnexus data objects are represented as dicts containing links:

```python
@dxpy.entry_point('main')
def main(reads_file):
    # Convert link to handler
    reads_dxfile = dxpy.DXFile(reads_file)

    # Download to local filesystem
    dxpy.download_dxfile(reads_dxfile.get_id(), "reads.fastq")

    # Process file...
```

**Outputs**: Return primitive types directly, convert file outputs to links:

```python
    # Upload result file
    output_file = dxpy.upload_local_file("output.fastq")

    return {
        "trimmed_reads": dxpy.dxlink(output_file)
    }
```

## Bash App Structure

Bash apps use a simpler shell script approach:

```bash
#!/bin/bash
set -e -x -o pipefail

main() {
    # Download inputs
    dx download "$reads_file" -o reads.fastq

    # Process
    process_reads reads.fastq > output.fastq

    # Upload outputs
    trimmed_reads=$(dx upload output.fastq --brief)

    # Set job output
    dx-jobutil-add-output trimmed_reads "$trimmed_reads" --class=file
}
```

## Common Development Patterns

### 1. Bioinformatics Pipeline

Download → Process → Upload pattern:

```python
# Download input
dxpy.download_dxfile(input_file_id, "input.fastq")

# Run analysis
subprocess.check_call(["tool", "input.fastq", "output.bam"])

# Upload result
output = dxpy.upload_local_file("output.bam")
return {"aligned_reads": dxpy.dxlink(output)}
```

### 2. Multi-file Processing

```python
# Process multiple inputs
for file_link in input_files:
    file_handler = dxpy.DXFile(file_link)
    local_path = f"{file_handler.name}"
    dxpy.download_dxfile(file_handler.get_id(), local_path)
    # Process each file...
```

### 3. Parallel Processing

Apps can spawn subjobs for parallel execution:

```python
# Create subjobs
subjobs = []
for item in input_list:
    subjob = dxpy.new_dxjob(
        fn_input={"input": item},
        fn_name="process_item"
    )
    subjobs.append(subjob)

# Collect results
results = [job.get_output_ref("result") for job in subjobs]
```

## Execution Environment

Apps run in isolated Linux VMs (Ubuntu 24.04) with:
- Internet access
- DNAnexus API access
- Temporary scratch space in `/home/dnanexus`
- Input files downloaded to job workspace
- Root access for installing dependencies

## Testing Apps

### Local Testing

Test app logic locally before deploying:

```bash
cd my-app
python src/my-app.py
```

### Platform Testing

Run the applet on the platform:

```bash
dx run applet-xxxx -i input1=file-yyyy
```

Monitor job execution:

```bash
dx watch job-zzzz
```

View job logs:

```bash
dx watch job-zzzz --get-streams
```

## Best Practices

1. **Error Handling**: Use try-except blocks and provide informative error messages
2. **Logging**: Print progress and debug information to stdout/stderr
3. **Validation**: Validate inputs before processing
4. **Cleanup**: Remove temporary files when done
5. **Documentation**: Include clear descriptions in dxapp.json
6. **Testing**: Test with various input types and edge cases
7. **Versioning**: Use semantic versioning for apps

## Common Issues

### File Not Found
Ensure files are properly downloaded before accessing:
```python
dxpy.download_dxfile(file_id, local_path)
# Now safe to open local_path
```

### Out of Memory
Specify larger instance type in dxapp.json systemRequirements

### Timeout
Increase timeout in dxapp.json or split into smaller jobs

### Permission Errors
Ensure app has necessary permissions in dxapp.json

---

## Reference: Configuration

# DNAnexus App Configuration and Dependencies

## Overview

This guide covers configuring apps through dxapp.json metadata and managing dependencies including system packages, Python libraries, and Docker containers.

## dxapp.json Structure

The `dxapp.json` file is the configuration file for DNAnexus apps and applets. It defines metadata, inputs, outputs, execution requirements, and dependencies.

### Minimal Example

```json
{
  "name": "my-app",
  "title": "My Analysis App",
  "summary": "Performs analysis on input files",
  "dxapi": "1.0.0",
  "version": "1.0.0",
  "inputSpec": [],
  "outputSpec": [],
  "runSpec": {
    "interpreter": "python3",
    "file": "src/my-app.py",
    "distribution": "Ubuntu",
    "release": "24.04"
  }
}
```

## Metadata Fields

### Required Fields

```json
{
  "name": "my-app",           // Unique identifier (lowercase, numbers, hyphens, underscores)
  "title": "My App",          // Human-readable name
  "summary": "One line description",
  "dxapi": "1.0.0"           // API version
}
```

### Optional Metadata

```json
{
  "version": "1.0.0",        // Semantic version (required for apps)
  "description": "Extended description...",
  "developerNotes": "Implementation notes...",
  "categories": [            // For app discovery
    "Read Mapping",
    "Variation Calling"
  ],
  "details": {               // Arbitrary metadata
    "contactEmail": "dev@example.com",
    "upstreamVersion": "2.1.0",
    "citations": ["doi:10.1000/example"],
    "changelog": {
      "1.0.0": "Initial release"
    }
  }
}
```

## Input Specification

Define input parameters:

```json
{
  "inputSpec": [
    {
      "name": "reads",
      "label": "Input reads",
      "class": "file",
      "patterns": ["*.fastq", "*.fastq.gz"],
      "optional": false,
      "help": "FASTQ file containing sequencing reads"
    },
    {
      "name": "quality_threshold",
      "label": "Quality threshold",
      "class": "int",
      "default": 30,
      "optional": true,
      "help": "Minimum base quality score"
    },
    {
      "name": "reference",
      "label": "Reference genome",
      "class": "file",
      "patterns": ["*.fa", "*.fasta"],
      "suggestions": [
        {
          "name": "Human GRCh38",
          "project": "project-xxxx",
          "path": "/references/human_g1k_v37.fasta"
        }
      ]
    }
  ]
}
```

### Input Classes

- `file` - File object
- `record` - Record object
- `applet` - Applet reference
- `string` - Text string
- `int` - Integer number
- `float` - Floating point number
- `boolean` - True/false
- `hash` - Key-value mapping
- `array:class` - Array of specified class

### Input Options

- `name` - Parameter name (required)
- `class` - Data type (required)
- `optional` - Whether parameter is optional (default: false)
- `default` - Default value for optional parameters
- `label` - Display name in UI
- `help` - Description text
- `patterns` - File name patterns (for files)
- `suggestions` - Pre-defined reference data
- `choices` - Allowed values (for strings/numbers)
- `group` - UI grouping

## Output Specification

Define output parameters:

```json
{
  "outputSpec": [
    {
      "name": "aligned_reads",
      "label": "Aligned reads",
      "class": "file",
      "patterns": ["*.bam"],
      "help": "BAM file with aligned reads"
    },
    {
      "name": "mapping_stats",
      "label": "Mapping statistics",
      "class": "record",
      "help": "Record containing alignment statistics"
    }
  ]
}
```

## Run Specification

Define how the app executes:

```json
{
  "runSpec": {
    "interpreter": "python3",        // or "bash"
    "file": "src/my-app.py",         // Entry point script
    "distribution": "Ubuntu",
    "release": "24.04",
    "version": "0",                   // Distribution version
    "execDepends": [                  // System packages
      {"name": "samtools"},
      {"name": "bwa"}
    ],
    "bundledDepends": [              // Bundled resources
      {"name": "scripts.tar.gz", "id": {"$dnanexus_link": "file-xxxx"}}
    ],
    "assetDepends": [                // Asset dependencies
      {"name": "asset-name", "id": {"$dnanexus_link": "record-xxxx"}}
    ],
    "systemRequirements": {
      "*": {
        "instanceType": "mem2_ssd1_v2_x4"
      }
    },
    "headJobOnDemand": true,
    "restartableEntryPoints": ["main"]
  }
}
```

## System Requirements

### Instance Type Selection

```json
{
  "systemRequirements": {
    "main": {
      "instanceType": "mem2_ssd1_v2_x8"
    },
    "process": {
      "instanceType": "mem3_ssd1_v2_x16"
    }
  }
}
```

**Common instance types**:
- `mem1_ssd1_v2_x2` - 2 cores, 3.9 GB RAM
- `mem1_ssd1_v2_x4` - 4 cores, 7.8 GB RAM
- `mem2_ssd1_v2_x4` - 4 cores, 15.6 GB RAM
- `mem2_ssd1_v2_x8` - 8 cores, 31.2 GB RAM
- `mem3_ssd1_v2_x8` - 8 cores, 62.5 GB RAM
- `mem3_ssd1_v2_x16` - 16 cores, 125 GB RAM

### Cluster Specifications

For distributed computing:

```json
{
  "systemRequirements": {
    "main": {
      "clusterSpec": {
        "type": "spark",
        "version": "3.1.2",
        "initialInstanceCount": 3,
        "instanceType": "mem1_ssd1_v2_x4",
        "bootstrapScript": "bootstrap.sh"
      }
    }
  }
}
```

## Regional Options

Deploy apps across regions:

```json
{
  "regionalOptions": {
    "aws:us-east-1": {
      "systemRequirements": {
        "*": {"instanceType": "mem2_ssd1_v2_x4"}
      },
      "assetDepends": [
        {"id": "record-xxxx"}
      ]
    },
    "azure:westus": {
      "systemRequirements": {
        "*": {"instanceType": "azure:mem2_ssd1_x4"}
      }
    }
  }
}
```

## Dependency Management

### System Packages (execDepends)

Install Ubuntu packages at runtime:

```json
{
  "runSpec": {
    "execDepends": [
      {"name": "samtools"},
      {"name": "bwa"},
      {"name": "python3-pip"},
      {"name": "r-base", "version": "4.0.0"}
    ]
  }
}
```

Packages are installed using `apt-get` from Ubuntu repositories.

### Python Dependencies

#### Option 1: Install via pip in execDepends

```json
{
  "runSpec": {
    "execDepends": [
      {"name": "python3-pip"}
    ]
  }
}
```

Then in your app script:
```python
import subprocess
subprocess.check_call(["pip", "install", "numpy==1.24.0", "pandas==2.0.0"])
```

#### Option 2: Requirements file

Create `resources/requirements.txt`:
```
numpy==1.24.0
pandas==2.0.0
scikit-learn==1.3.0
```

In your app:
```python
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
```

### Bundled Dependencies

Include custom tools or libraries in the app:

**File structure**:
```
my-app/
├── dxapp.json
├── src/
│   └── my-app.py
└── resources/
    ├── tools/
    │   └── custom_tool
    └── scripts/
        └── helper.py
```

Access resources in app:
```python
import os

# Resources are in parent directory
resources_dir = os.path.join(os.path.dirname(__file__), "..", "resources")
tool_path = os.path.join(resources_dir, "tools", "custom_tool")

# Run bundled tool
subprocess.check_call([tool_path, "arg1", "arg2"])
```

### Asset Dependencies

Assets are pre-built bundles of dependencies that can be shared across apps.

#### Using Assets

```json
{
  "runSpec": {
    "assetDepends": [
      {
        "name": "bwa-asset",
        "id": {"$dnanexus_link": "record-xxxx"}
      }
    ]
  }
}
```

Assets are mounted at runtime and accessible via environment variable:
```python
import os
asset_dir = os.environ.get("DX_ASSET_BWA")
bwa_path = os.path.join(asset_dir, "bin", "bwa")
```

#### Creating Assets

Create asset directory:
```bash
mkdir bwa-asset
cd bwa-asset
# Install software
./configure --prefix=$PWD/usr/local
make && make install
```

Build asset:
```bash
dx build_asset bwa-asset --destination=project-xxxx:/assets/
```

## Docker Integration

### Using Docker Images

```json
{
  "runSpec": {
    "interpreter": "python3",
    "file": "src/my-app.py",
    "distribution": "Ubuntu",
    "release": "24.04",
    "systemRequirements": {
      "*": {
        "instanceType": "mem2_ssd1_v2_x4"
      }
    },
    "execDepends": [
      {"name": "docker.io"}
    ]
  }
}
```

Use Docker in app:
```python
import subprocess

# Pull Docker image
subprocess.check_call(["docker", "pull", "biocontainers/samtools:v1.9"])

# Run command in container
subprocess.check_call([
    "docker", "run",
    "-v", f"{os.getcwd()}:/data",
    "biocontainers/samtools:v1.9",
    "samtools", "view", "/data/input.bam"
])
```

### Docker as Base Image

For apps that run entirely in Docker:

```json
{
  "runSpec": {
    "interpreter": "bash",
    "file": "src/wrapper.sh",
    "distribution": "Ubuntu",
    "release": "24.04",
    "execDepends": [
      {"name": "docker.io"}
    ]
  }
}
```

## Access Requirements

Request special permissions:

```json
{
  "access": {
    "network": ["*"],           // Internet access
    "project": "CONTRIBUTE",    // Project write access
    "allProjects": "VIEW",      // Read other projects
    "developer": true           // Advanced permissions
  }
}
```

**Network access**:
- `["*"]` - Full internet
- `["github.com", "pypi.org"]` - Specific domains

## Timeout Configuration

```json
{
  "runSpec": {
    "timeoutPolicy": {
      "*": {
        "days": 1,
        "hours": 12,
        "minutes": 30
      }
    }
  }
}
```

## Example: Complete dxapp.json

```json
{
  "name": "rna-seq-pipeline",
  "title": "RNA-Seq Analysis Pipeline",
  "summary": "Aligns RNA-seq reads and quantifies gene expression",
  "description": "Comprehensive RNA-seq pipeline using STAR aligner and featureCounts",
  "version": "1.0.0",
  "dxapi": "1.0.0",
  "categories": ["Read Mapping", "RNA-Seq"],

  "inputSpec": [
    {
      "name": "reads",
      "label": "FASTQ reads",
      "class": "array:file",
      "patterns": ["*.fastq.gz", "*.fq.gz"],
      "help": "Single-end or paired-end RNA-seq reads"
    },
    {
      "name": "reference_genome",
      "label": "Reference genome",
      "class": "file",
      "patterns": ["*.fa", "*.fasta"],
      "suggestions": [
        {
          "name": "Human GRCh38",
          "project": "project-reference",
          "path": "/genomes/GRCh38.fa"
        }
      ]
    },
    {
      "name": "gtf_file",
      "label": "Gene annotation (GTF)",
      "class": "file",
      "patterns": ["*.gtf", "*.gtf.gz"]
    }
  ],

  "outputSpec": [
    {
      "name": "aligned_bam",
      "label": "Aligned reads (BAM)",
      "class": "file",
      "patterns": ["*.bam"]
    },
    {
      "name": "counts",
      "label": "Gene counts",
      "class": "file",
      "patterns": ["*.counts.txt"]
    },
    {
      "name": "qc_report",
      "label": "QC report",
      "class": "file",
      "patterns": ["*.html"]
    }
  ],

  "runSpec": {
    "interpreter": "python3",
    "file": "src/rna-seq-pipeline.py",
    "distribution": "Ubuntu",
    "release": "24.04",

    "execDepends": [
      {"name": "python3-pip"},
      {"name": "samtools"},
      {"name": "subread"}
    ],

    "assetDepends": [
      {
        "name": "star-aligner",
        "id": {"$dnanexus_link": "record-star-asset"}
      }
    ],

    "systemRequirements": {
      "main": {
        "instanceType": "mem3_ssd1_v2_x16"
      }
    },

    "timeoutPolicy": {
      "*": {"hours": 8}
    }
  },

  "access": {
    "network": ["*"]
  },

  "details": {
    "contactEmail": "support@example.com",
    "upstreamVersion": "STAR 2.7.10a, Subread 2.0.3",
    "citations": ["doi:10.1093/bioinformatics/bts635"]
  }
}
```

## Best Practices

1. **Version Management**: Use semantic versioning for apps
2. **Instance Type**: Start with smaller instances, scale up as needed
3. **Dependencies**: Document all dependencies clearly
4. **Error Messages**: Provide helpful error messages for invalid inputs
5. **Testing**: Test with various input types and sizes
6. **Documentation**: Write clear descriptions and help text
7. **Resources**: Bundle frequently-used tools to avoid repeated downloads
8. **Docker**: Use Docker for complex dependency chains
9. **Assets**: Create assets for heavy dependencies shared across apps
10. **Timeouts**: Set reasonable timeouts based on expected runtime
11. **Network Access**: Request only necessary network permissions
12. **Region Support**: Use regionalOptions for multi-region apps

## Common Patterns

### Bioinformatics Tool

```json
{
  "inputSpec": [
    {"name": "input_file", "class": "file", "patterns": ["*.bam"]},
    {"name": "threads", "class": "int", "default": 4, "optional": true}
  ],
  "runSpec": {
    "execDepends": [{"name": "tool-name"}],
    "systemRequirements": {
      "main": {"instanceType": "mem2_ssd1_v2_x8"}
    }
  }
}
```

### Python Data Analysis

```json
{
  "runSpec": {
    "interpreter": "python3",
    "execDepends": [
      {"name": "python3-pip"}
    ],
    "systemRequirements": {
      "main": {"instanceType": "mem2_ssd1_v2_x4"}
    }
  }
}
```

### Docker-based App

```json
{
  "runSpec": {
    "interpreter": "bash",
    "execDepends": [
      {"name": "docker.io"}
    ],
    "systemRequirements": {
      "main": {"instanceType": "mem2_ssd1_v2_x8"}
    }
  },
  "access": {
    "network": ["*"]
  }
}
```

---

## Reference: Data Operations

# DNAnexus Data Operations

## Overview

DNAnexus provides comprehensive data management capabilities for files, records, databases, and other data objects. All data operations can be performed via the Python SDK (dxpy) or command-line interface (dx).

## Data Object Types

### Files
Binary or text data stored on the platform.

### Records
Structured data objects with arbitrary JSON details and metadata.

### Databases
Structured database objects for relational data.

### Applets and Apps
Executable programs (covered in app-development.md).

### Workflows
Multi-step analysis pipelines.

## Data Object Lifecycle

### States

**Open State**: Data can be modified
- Files: Contents can be written
- Records: Details can be updated
- Applets: Created in closed state by default

**Closed State**: Data becomes immutable
- File contents are fixed
- Metadata fields are locked (types, details, links, visibility)
- Objects are ready for sharing and analysis

### Transitions

```
Create (open) → Modify → Close (immutable)
```

Most objects start open and require explicit closure:
```python
# Close a file
file_obj.close()
```

Some objects can be created and closed in one operation:
```python
# Create closed record
record = dxpy.new_dxrecord(details={...}, close=True)
```

## File Operations

### Uploading Files

**From local file**:
```python
import dxpy

# Upload a file
file_obj = dxpy.upload_local_file("data.txt", project="project-xxxx")
print(f"Uploaded: {file_obj.get_id()}")
```

**With metadata**:
```python
file_obj = dxpy.upload_local_file(
    "data.txt",
    name="my_data",
    project="project-xxxx",
    folder="/results",
    properties={"sample": "sample1", "type": "raw"},
    tags=["experiment1", "batch2"]
)
```

**Streaming upload**:
```python
# For large files or generated data
file_obj = dxpy.new_dxfile(project="project-xxxx", name="output.txt")
file_obj.write("Line 1\n")
file_obj.write("Line 2\n")
file_obj.close()
```

### Downloading Files

**To local file**:
```python
# Download by ID
dxpy.download_dxfile("file-xxxx", "local_output.txt")

# Download using handler
file_obj = dxpy.DXFile("file-xxxx")
dxpy.download_dxfile(file_obj.get_id(), "local_output.txt")
```

**Read file contents**:
```python
file_obj = dxpy.DXFile("file-xxxx")
with file_obj.open_file() as f:
    contents = f.read()
```

**Download to specific directory**:
```python
dxpy.download_dxfile("file-xxxx", "/path/to/directory/filename.txt")
```

### File Metadata

**Get file information**:
```python
file_obj = dxpy.DXFile("file-xxxx")
describe = file_obj.describe()

print(f"Name: {describe['name']}")
print(f"Size: {describe['size']} bytes")
print(f"State: {describe['state']}")
print(f"Created: {describe['created']}")
```

**Update file metadata**:
```python
file_obj.set_properties({"experiment": "exp1", "version": "v2"})
file_obj.add_tags(["validated", "published"])
file_obj.rename("new_name.txt")
```

## Record Operations

Records store structured metadata with arbitrary JSON.

### Creating Records

```python
# Create a record
record = dxpy.new_dxrecord(
    name="sample_metadata",
    types=["SampleMetadata"],
    details={
        "sample_id": "S001",
        "tissue": "blood",
        "age": 45,
        "conditions": ["diabetes"]
    },
    project="project-xxxx",
    close=True
)
```

### Reading Records

```python
record = dxpy.DXRecord("record-xxxx")
describe = record.describe()

# Access details
details = record.get_details()
sample_id = details["sample_id"]
tissue = details["tissue"]
```

### Updating Records

```python
# Record must be open to update
record = dxpy.DXRecord("record-xxxx")
details = record.get_details()
details["processed"] = True
record.set_details(details)
record.close()
```

## Search and Discovery

### Finding Data Objects

**Search by name**:
```python
results = dxpy.find_data_objects(
    name="*.fastq",
    project="project-xxxx",
    folder="/raw_data"
)

for result in results:
    print(f"{result['describe']['name']}: {result['id']}")
```

**Search by properties**:
```python
results = dxpy.find_data_objects(
    classname="file",
    properties={"sample": "sample1", "type": "processed"},
    project="project-xxxx"
)
```

**Search by type**:
```python
# Find all records of specific type
results = dxpy.find_data_objects(
    classname="record",
    typename="SampleMetadata",
    project="project-xxxx"
)
```

**Search with state filter**:
```python
# Find only closed files
results = dxpy.find_data_objects(
    classname="file",
    state="closed",
    project="project-xxxx"
)
```

### System-wide Search

```python
# Search across all accessible projects
results = dxpy.find_data_objects(
    name="important_data.txt",
    describe=True  # Include full descriptions
)
```

## Cloning and Copying

### Clone Data Between Projects

```python
# Clone file to another project
new_file = dxpy.DXFile("file-xxxx").clone(
    project="project-yyyy",
    folder="/imported_data"
)
```

### Clone Multiple Objects

```python
# Clone folder contents
files = dxpy.find_data_objects(
    classname="file",
    project="project-xxxx",
    folder="/results"
)

for file in files:
    file_obj = dxpy.DXFile(file['id'])
    file_obj.clone(project="project-yyyy", folder="/backup")
```

## Project Management

### Creating Projects

```python
# Create a new project
project = dxpy.api.project_new({
    "name": "My Analysis Project",
    "description": "RNA-seq analysis for experiment X"
})

project_id = project['id']
```

### Project Permissions

```python
# Invite user to project
dxpy.api.project_invite(
    project_id,
    {
        "invitee": "user-xxxx",
        "level": "CONTRIBUTE"  # VIEW, UPLOAD, CONTRIBUTE, ADMINISTER
    }
)
```

### List Projects

```python
# List accessible projects
projects = dxpy.find_projects(describe=True)

for proj in projects:
    desc = proj['describe']
    print(f"{desc['name']}: {proj['id']}")
```

## Folder Operations

### Creating Folders

```python
# Create nested folders
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/analysis/batch1/results", "parents": True}
)
```

### Moving Objects

```python
# Move file to different folder
file_obj = dxpy.DXFile("file-xxxx", project="project-xxxx")
file_obj.move("/new_location")
```

### Removing Objects

```python
# Remove file from project (not permanent deletion)
dxpy.api.project_remove_objects(
    "project-xxxx",
    {"objects": ["file-xxxx"]}
)

# Permanent deletion
file_obj = dxpy.DXFile("file-xxxx")
file_obj.remove()
```

## Archival

### Archive Data

Archived data is moved to cheaper long-term storage:

```python
# Archive a file
dxpy.api.project_archive(
    "project-xxxx",
    {"files": ["file-xxxx"]}
)
```

### Unarchive Data

```python
# Unarchive when needed
dxpy.api.project_unarchive(
    "project-xxxx",
    {"files": ["file-xxxx"]}
)
```

## Batch Operations

### Upload Multiple Files

```python
import os

# Upload all files in directory
for filename in os.listdir("./data"):
    filepath = os.path.join("./data", filename)
    if os.path.isfile(filepath):
        dxpy.upload_local_file(
            filepath,
            project="project-xxxx",
            folder="/batch_upload"
        )
```

### Download Multiple Files

```python
# Download all files from folder
files = dxpy.find_data_objects(
    classname="file",
    project="project-xxxx",
    folder="/results"
)

for file in files:
    file_obj = dxpy.DXFile(file['id'])
    filename = file_obj.describe()['name']
    dxpy.download_dxfile(file['id'], f"./downloads/{filename}")
```

## Best Practices

1. **Close Files**: Always close files after writing to make them accessible
2. **Use Properties**: Tag data with meaningful properties for easier discovery
3. **Organize Folders**: Use logical folder structures
4. **Clean Up**: Remove temporary or obsolete data
5. **Batch Operations**: Group operations when processing many objects
6. **Error Handling**: Check object states before operations
7. **Permissions**: Verify project permissions before data operations
8. **Archive Old Data**: Use archival for long-term storage cost savings

---

## Reference: Job Execution

# DNAnexus Job Execution and Workflows

## Overview

Jobs are the fundamental execution units on DNAnexus. When an applet or app runs, a job is created and executed on a worker node in an isolated Linux environment with constant API access.

## Job Types

### Origin Jobs
Initially created by users or automated systems.

### Master Jobs
Result from directly launching an executable (app/applet).

### Child Jobs
Spawned by parent jobs for parallel processing or sub-workflows.

## Running Jobs

### Running an Applet

**Basic execution**:
```python
import dxpy

# Run an applet
job = dxpy.DXApplet("applet-xxxx").run({
    "input1": {"$dnanexus_link": "file-yyyy"},
    "input2": "parameter_value"
})

print(f"Job ID: {job.get_id()}")
```

**Using command line**:
```bash
dx run applet-xxxx -i input1=file-yyyy -i input2="value"
```

### Running an App

```python
# Run an app by name
job = dxpy.DXApp(name="my-app").run({
    "reads": {"$dnanexus_link": "file-xxxx"},
    "quality_threshold": 30
})
```

### Specifying Execution Parameters

```python
job = dxpy.DXApplet("applet-xxxx").run(
    applet_input={
        "input_file": {"$dnanexus_link": "file-yyyy"}
    },
    project="project-zzzz",  # Output project
    folder="/results",        # Output folder
    name="My Analysis Job",   # Job name
    instance_type="mem2_hdd2_x4",  # Override instance type
    priority="high"           # Job priority
)
```

## Job Monitoring

### Checking Job Status

```python
job = dxpy.DXJob("job-xxxx")
state = job.describe()["state"]

# States: idle, waiting_on_input, runnable, running, done, failed, terminated
print(f"Job state: {state}")
```

**Using command line**:
```bash
dx watch job-xxxx
```

### Waiting for Job Completion

```python
# Block until job completes
job.wait_on_done()

# Check if successful
if job.describe()["state"] == "done":
    output = job.describe()["output"]
    print(f"Job completed: {output}")
else:
    print("Job failed")
```

### Getting Job Output

```python
job = dxpy.DXJob("job-xxxx")

# Wait for completion
job.wait_on_done()

# Get outputs
output = job.describe()["output"]
output_file_id = output["result_file"]["$dnanexus_link"]

# Download result
dxpy.download_dxfile(output_file_id, "result.txt")
```

### Job Output References

Create references to job outputs before they complete:

```python
# Launch first job
job1 = dxpy.DXApplet("applet-1").run({"input": "..."})

# Launch second job using output reference
job2 = dxpy.DXApplet("applet-2").run({
    "input": dxpy.dxlink(job1.get_output_ref("output_name"))
})
```

## Job Logs

### Viewing Logs

**Command line**:
```bash
dx watch job-xxxx --get-streams
```

**Programmatically**:
```python
import sys

# Get job logs
job = dxpy.DXJob("job-xxxx")
log = dxpy.api.job_get_log(job.get_id())

for log_entry in log["loglines"]:
    print(log_entry)
```

## Parallel Execution

### Creating Subjobs

```python
@dxpy.entry_point('main')
def main(input_files):
    # Create subjobs for parallel processing
    subjobs = []

    for input_file in input_files:
        subjob = dxpy.new_dxjob(
            fn_input={"file": input_file},
            fn_name="process_file"
        )
        subjobs.append(subjob)

    # Collect results
    results = []
    for subjob in subjobs:
        result = subjob.get_output_ref("processed_file")
        results.append(result)

    return {"all_results": results}

@dxpy.entry_point('process_file')
def process_file(file):
    # Process single file
    # ...
    return {"processed_file": output_file}
```

### Scatter-Gather Pattern

```python
# Scatter: Process items in parallel
scatter_jobs = []
for item in items:
    job = dxpy.new_dxjob(
        fn_input={"item": item},
        fn_name="process_item"
    )
    scatter_jobs.append(job)

# Gather: Combine results
gather_job = dxpy.new_dxjob(
    fn_input={
        "results": [job.get_output_ref("result") for job in scatter_jobs]
    },
    fn_name="combine_results"
)
```

## Workflows

Workflows combine multiple apps/applets into multi-step pipelines.

### Creating a Workflow

```python
# Create workflow
workflow = dxpy.new_dxworkflow(
    name="My Analysis Pipeline",
    project="project-xxxx"
)

# Add stages
stage1 = workflow.add_stage(
    dxpy.DXApplet("applet-1"),
    name="Quality Control",
    folder="/qc"
)

stage2 = workflow.add_stage(
    dxpy.DXApplet("applet-2"),
    name="Alignment",
    folder="/alignment"
)

# Connect stages
stage2.set_input("reads", stage1.get_output_ref("filtered_reads"))

# Close workflow
workflow.close()
```

### Running a Workflow

```python
# Run workflow
analysis = workflow.run({
    "stage-xxxx.input1": {"$dnanexus_link": "file-yyyy"}
})

# Monitor analysis (collection of jobs)
analysis.wait_on_done()

# Get workflow outputs
outputs = analysis.describe()["output"]
```

**Using command line**:
```bash
dx run workflow-xxxx -i stage-1.input=file-yyyy
```

## Job Permissions and Context

### Workspace Context

Jobs run in a workspace project with cloned input data:
- Jobs require `CONTRIBUTE` permission to workspace
- Jobs need `VIEW` access to source projects
- All charges accumulate to the originating project

### Data Requirements

Jobs cannot start until:
1. All input data objects are in `closed` state
2. Required permissions are available
3. Resources are allocated

Output objects must reach `closed` state before workspace cleanup.

## Job Lifecycle

```
Created → Waiting on Input → Runnable → Running → Done/Failed
```

**States**:
- `idle`: Job created but not yet queued
- `waiting_on_input`: Waiting for input data objects to close
- `runnable`: Ready to run, waiting for resources
- `running`: Currently executing
- `done`: Completed successfully
- `failed`: Execution failed
- `terminated`: Manually stopped

## Error Handling

### Job Failure

```python
job = dxpy.DXJob("job-xxxx")
job.wait_on_done()

desc = job.describe()
if desc["state"] == "failed":
    print(f"Job failed: {desc.get('failureReason', 'Unknown')}")
    print(f"Failure message: {desc.get('failureMessage', '')}")
```

### Retry Failed Jobs

```python
# Rerun failed job
new_job = dxpy.DXApplet(desc["applet"]).run(
    desc["originalInput"],
    project=desc["project"]
)
```

### Terminating Jobs

```python
# Stop a running job
job = dxpy.DXJob("job-xxxx")
job.terminate()
```

**Using command line**:
```bash
dx terminate job-xxxx
```

## Resource Management

### Instance Types

Specify computational resources:

```python
# Run with specific instance type
job = dxpy.DXApplet("applet-xxxx").run(
    {"input": "..."},
    instance_type="mem3_ssd1_v2_x8"  # 8 cores, high memory, SSD
)
```

Common instance types:
- `mem1_ssd1_v2_x4` - 4 cores, standard memory
- `mem2_ssd1_v2_x8` - 8 cores, high memory
- `mem3_ssd1_v2_x16` - 16 cores, very high memory
- `mem1_ssd1_v2_x36` - 36 cores for parallel workloads

### Timeout Settings

Set maximum execution time:

```python
job = dxpy.DXApplet("applet-xxxx").run(
    {"input": "..."},
    timeout="24h"  # Maximum runtime
)
```

## Job Tagging and Metadata

### Add Job Tags

```python
job = dxpy.DXApplet("applet-xxxx").run(
    {"input": "..."},
    tags=["experiment1", "batch2", "production"]
)
```

### Add Job Properties

```python
job = dxpy.DXApplet("applet-xxxx").run(
    {"input": "..."},
    properties={
        "experiment": "exp001",
        "sample": "sample1",
        "batch": "batch2"
    }
)
```

### Finding Jobs

```python
# Find jobs by tag
jobs = dxpy.find_jobs(
    project="project-xxxx",
    tags=["experiment1"],
    describe=True
)

for job in jobs:
    print(f"{job['describe']['name']}: {job['id']}")
```

## Best Practices

1. **Job Naming**: Use descriptive names for easier tracking
2. **Tags and Properties**: Tag jobs for organization and searchability
3. **Resource Selection**: Choose appropriate instance types for workload
4. **Error Handling**: Check job state and handle failures gracefully
5. **Parallel Processing**: Use subjobs for independent parallel tasks
6. **Workflows**: Use workflows for complex multi-step analyses
7. **Monitoring**: Monitor long-running jobs and check logs for issues
8. **Cost Management**: Use appropriate instance types to balance cost/performance
9. **Timeouts**: Set reasonable timeouts to prevent runaway jobs
10. **Cleanup**: Remove failed or obsolete jobs

## Debugging Tips

1. **Check Logs**: Always review job logs for error messages
2. **Verify Inputs**: Ensure input files are closed and accessible
3. **Test Locally**: Test logic locally before deploying to platform
4. **Start Small**: Test with small datasets before scaling up
5. **Monitor Resources**: Check if job is running out of memory or disk space
6. **Instance Type**: Try larger instance if job fails due to resources

---

## Reference: Python Sdk

# DNAnexus Python SDK (dxpy)

## Overview

The dxpy library provides Python bindings to interact with the DNAnexus Platform. It's available both within the DNAnexus Execution Environment (for apps running on the platform) and for external scripts accessing the API.

## Installation

```bash
# Install dxpy
pip install dxpy

# Or using conda
conda install -c bioconda dxpy
```

**Requirements**: Python 3.8 or higher

## Authentication

### Login

```bash
# Login via command line
dx login
```

### API Token

```python
import dxpy

# Set authentication token
dxpy.set_security_context({
    "auth_token_type": "Bearer",
    "auth_token": "YOUR_API_TOKEN"
})
```

### Environment Variables

```bash
# Set token via environment
export DX_SECURITY_CONTEXT='{"auth_token": "YOUR_TOKEN", "auth_token_type": "Bearer"}'
```

## Core Classes

### DXFile

Handler for file objects.

```python
import dxpy

# Get file handler
file_obj = dxpy.DXFile("file-xxxx")

# Get file info
desc = file_obj.describe()
print(f"Name: {desc['name']}")
print(f"Size: {desc['size']} bytes")

# Download file
dxpy.download_dxfile(file_obj.get_id(), "local_file.txt")

# Read file contents
with file_obj.open_file() as f:
    contents = f.read()

# Update metadata
file_obj.set_properties({"key": "value"})
file_obj.add_tags(["tag1", "tag2"])
file_obj.rename("new_name.txt")

# Close file
file_obj.close()
```

### DXRecord

Handler for record objects.

```python
# Create record
record = dxpy.new_dxrecord(
    name="metadata",
    types=["Metadata"],
    details={"key": "value"},
    project="project-xxxx",
    close=True
)

# Get record handler
record = dxpy.DXRecord("record-xxxx")

# Get details
details = record.get_details()

# Update details (must be open)
record.set_details({"updated": True})
record.close()
```

### DXApplet

Handler for applet objects.

```python
# Get applet
applet = dxpy.DXApplet("applet-xxxx")

# Get applet info
desc = applet.describe()
print(f"Name: {desc['name']}")
print(f"Version: {desc.get('version', 'N/A')}")

# Run applet
job = applet.run({
    "input1": {"$dnanexus_link": "file-yyyy"},
    "param1": "value"
})
```

### DXApp

Handler for app objects.

```python
# Get app by name
app = dxpy.DXApp(name="my-app")

# Or by ID
app = dxpy.DXApp("app-xxxx")

# Run app
job = app.run({
    "input": {"$dnanexus_link": "file-yyyy"}
})
```

### DXWorkflow

Handler for workflow objects.

```python
# Create workflow
workflow = dxpy.new_dxworkflow(
    name="My Pipeline",
    project="project-xxxx"
)

# Add stage
stage = workflow.add_stage(
    dxpy.DXApplet("applet-xxxx"),
    name="Step 1"
)

# Set stage input
stage.set_input("input1", {"$dnanexus_link": "file-yyyy"})

# Close workflow
workflow.close()

# Run workflow
analysis = workflow.run({})
```

### DXJob

Handler for job objects.

```python
# Get job
job = dxpy.DXJob("job-xxxx")

# Get job info
desc = job.describe()
print(f"State: {desc['state']}")
print(f"Name: {desc['name']}")

# Wait for completion
job.wait_on_done()

# Get output
output = desc.get("output", {})

# Terminate job
job.terminate()
```

### DXProject

Handler for project objects.

```python
# Get project
project = dxpy.DXProject("project-xxxx")

# Get project info
desc = project.describe()
print(f"Name: {desc['name']}")
print(f"Region: {desc.get('region', 'N/A')}")

# List folder contents
contents = project.list_folder("/data")
print(f"Objects: {contents['objects']}")
print(f"Folders: {contents['folders']}")
```

## High-Level Functions

### File Operations

```python
# Upload file
file_obj = dxpy.upload_local_file(
    "local_file.txt",
    project="project-xxxx",
    folder="/data",
    name="uploaded_file.txt"
)

# Download file
dxpy.download_dxfile("file-xxxx", "downloaded.txt")

# Upload string as file
file_obj = dxpy.upload_string("Hello World", project="project-xxxx")
```

### Creating Data Objects

```python
# New file
file_obj = dxpy.new_dxfile(
    project="project-xxxx",
    name="output.txt"
)
file_obj.write("content")
file_obj.close()

# New record
record = dxpy.new_dxrecord(
    name="metadata",
    details={"key": "value"},
    project="project-xxxx"
)
```

### Search Functions

```python
# Find data objects
results = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx",
    folder="/raw_data",
    describe=True
)

for result in results:
    print(f"{result['describe']['name']}: {result['id']}")

# Find projects
projects = dxpy.find_projects(
    name="*analysis*",
    describe=True
)

# Find jobs
jobs = dxpy.find_jobs(
    project="project-xxxx",
    created_after="2025-01-01",
    state="failed"
)

# Find apps
apps = dxpy.find_apps(
    category="Read Mapping"
)
```

### Links and References

```python
# Create link to data object
link = dxpy.dxlink("file-xxxx")
# Returns: {"$dnanexus_link": "file-xxxx"}

# Create link with project
link = dxpy.dxlink("file-xxxx", "project-yyyy")

# Get job output reference (for chaining jobs)
output_ref = job.get_output_ref("output_name")
```

## API Methods

### Direct API Calls

For operations not covered by high-level functions:

```python
# Call API method directly
result = dxpy.api.project_new({
    "name": "New Project",
    "description": "Created via API"
})

project_id = result["id"]

# File describe
file_desc = dxpy.api.file_describe("file-xxxx")

# System find data objects
results = dxpy.api.system_find_data_objects({
    "class": "file",
    "project": "project-xxxx",
    "name": {"regexp": ".*\\.bam$"}
})
```

### Common API Methods

```python
# Project operations
dxpy.api.project_invite("project-xxxx", {"invitee": "user-yyyy", "level": "VIEW"})
dxpy.api.project_new_folder("project-xxxx", {"folder": "/new_folder"})

# File operations
dxpy.api.file_close("file-xxxx")
dxpy.api.file_remove("file-xxxx")

# Job operations
dxpy.api.job_terminate("job-xxxx")
dxpy.api.job_get_log("job-xxxx")
```

## App Development Functions

### Entry Points

```python
import dxpy

@dxpy.entry_point('main')
def main(input1, input2):
    """Main entry point for app"""
    # Process inputs
    result = process(input1, input2)

    # Return outputs
    return {
        "output1": result
    }

# Required at end of app code
dxpy.run()
```

### Creating Subjobs

```python
# Spawn subjob within app
subjob = dxpy.new_dxjob(
    fn_input={"input": value},
    fn_name="helper_function"
)

# Get output reference
output_ref = subjob.get_output_ref("result")

@dxpy.entry_point('helper_function')
def helper_function(input):
    # Process
    return {"result": output}
```

## Error Handling

### Exception Types

```python
import dxpy
from dxpy.exceptions import DXError, DXAPIError

try:
    file_obj = dxpy.DXFile("file-xxxx")
    desc = file_obj.describe()
except DXAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.code}")
except DXError as e:
    print(f"General Error: {e}")
```

### Common Exceptions

- `DXAPIError`: API request failed
- `DXError`: General DNAnexus error
- `ResourceNotFound`: Object doesn't exist
- `PermissionDenied`: Insufficient permissions
- `InvalidInput`: Invalid input parameters

## Utility Functions

### Getting Handlers

```python
# Get handler from ID/link
handler = dxpy.get_handler("file-xxxx")
# Returns DXFile, DXRecord, etc. based on object class

# Bind handler to project
handler = dxpy.DXFile("file-xxxx", project="project-yyyy")
```

### Describe Methods

```python
# Describe any object
desc = dxpy.describe("file-xxxx")
print(desc)

# Describe with fields
desc = dxpy.describe("file-xxxx", fields={"name": True, "size": True})
```

## Configuration

### Setting Project Context

```python
# Set default project
dxpy.set_workspace_id("project-xxxx")

# Get current project
project_id = dxpy.WORKSPACE_ID
```

### Setting Region

```python
# Set API server
dxpy.set_api_server_info(host="api.dnanexus.com", port=443)
```

## Best Practices

1. **Use High-Level Functions**: Prefer `upload_local_file()` over manual file creation
2. **Handler Reuse**: Create handlers once and reuse them
3. **Batch Operations**: Use find functions to process multiple objects
4. **Error Handling**: Always wrap API calls in try-except blocks
5. **Close Objects**: Remember to close files and records after modifications
6. **Project Context**: Set workspace context for apps
7. **API Token Security**: Never hardcode tokens in source code
8. **Describe Fields**: Request only needed fields to reduce latency
9. **Search Filters**: Use specific filters to narrow search results
10. **Link Format**: Use `dxpy.dxlink()` for consistent link creation

## Common Patterns

### Upload and Process Pattern

```python
# Upload input
input_file = dxpy.upload_local_file("data.txt", project="project-xxxx")

# Run analysis
job = dxpy.DXApplet("applet-xxxx").run({
    "input": dxpy.dxlink(input_file.get_id())
})

# Wait and download result
job.wait_on_done()
output_id = job.describe()["output"]["result"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "result.txt")
```

### Batch File Processing

```python
# Find all FASTQ files
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# Process each file
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# Wait for all jobs
for job in jobs:
    job.wait_on_done()
    print(f"Job {job.get_id()} completed")
```

### Workflow with Dependencies

```python
# Job 1
job1 = applet1.run({"input": data})

# Job 2 depends on job1 output
job2 = applet2.run({
    "input": job1.get_output_ref("result")
})

# Job 3 depends on job2
job3 = applet3.run({
    "input": job2.get_output_ref("processed")
})

# Wait for final result
job3.wait_on_done()
```
