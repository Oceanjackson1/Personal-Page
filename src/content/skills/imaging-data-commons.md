---
title: "医学影像数据"
description: "NCI 医学影像数据公共资源，癌症影像数据分析"
category: "research"
source: "community"
author: "Community"
tags: ["imaging", "data", "commons"]
date: 2026-03-20
---

# Imaging Data Commons

## Overview

Use the `idc-index` Python package to query and download public cancer imaging data from the National Cancer Institute Imaging Data Commons (IDC). No authentication required for data access.

**Current IDC Data Version: v23** (always verify with `IDCClient().get_idc_version()`)

**Primary tool:** `idc-index` ([GitHub](https://github.com/imagingdatacommons/idc-index))

**CRITICAL - Check package version and upgrade if needed (run this FIRST):**

```python
import idc_index

REQUIRED_VERSION = "0.11.10"  # Must match metadata.idc-index in this file
installed = idc_index.__version__

if installed < REQUIRED_VERSION:
    print(f"Upgrading idc-index from {installed} to {REQUIRED_VERSION}...")
    import subprocess
    subprocess.run(["pip3", "install", "--upgrade", "--break-system-packages", "idc-index"], check=True)
    print("Upgrade complete. Restart Python to use new version.")
else:
    print(f"idc-index {installed} meets requirement ({REQUIRED_VERSION})")
```

**Verify IDC data version and check current data scale:**

```python
from idc_index import IDCClient
client = IDCClient()

# Verify IDC data version (should be "v23")
print(f"IDC data version: {client.get_idc_version()}")

# Get collection count and total series
stats = client.sql_query("""
    SELECT
        COUNT(DISTINCT collection_id) as collections,
        COUNT(DISTINCT analysis_result_id) as analysis_results,
        COUNT(DISTINCT PatientID) as patients,
        COUNT(DISTINCT StudyInstanceUID) as studies,
        COUNT(DISTINCT SeriesInstanceUID) as series,
        SUM(instanceCount) as instances,
        SUM(series_size_MB)/1000000 as size_TB
    FROM index
""")
print(stats)
```

**Core workflow:**
1. Query metadata → `client.sql_query()`
2. Download DICOM files → `client.download_from_selection()`
3. Visualize in browser → `client.get_viewer_URL(seriesInstanceUID=...)`

## When to Use This Skill

- Finding publicly available radiology (CT, MR, PET) or pathology (slide microscopy) images
- Selecting image subsets by cancer type, modality, anatomical site, or other metadata
- Downloading DICOM data from IDC
- Checking data licenses before use in research or commercial applications
- Visualizing medical images in a browser without local DICOM viewer software

## Quick Navigation

**Core Sections (inline):**
- IDC Data Model - Collection and analysis result hierarchy
- Index Tables - Available tables and joining patterns
- Installation - Package setup and version verification
- Core Capabilities - Essential API patterns (query, download, visualize, license, citations, batch)
- Best Practices - Usage guidelines
- Troubleshooting - Common issues and solutions

**Reference Guides (load on demand):**

| Guide | When to Load |
|-------|--------------|
| `index_tables_guide.md` | Complex JOINs, schema discovery, DataFrame access |
| `use_cases.md` | End-to-end workflow examples (training datasets, batch downloads) |
| `sql_patterns.md` | Quick SQL patterns for filter discovery, annotations, size estimation |
| `clinical_data_guide.md` | Clinical/tabular data, imaging+clinical joins, value mapping |
| `cloud_storage_guide.md` | Direct S3/GCS access, versioning, UUID mapping |
| `dicomweb_guide.md` | DICOMweb endpoints, PACS integration |
| `digital_pathology_guide.md` | Slide microscopy (SM), annotations (ANN), pathology workflows |
| `bigquery_guide.md` | Full DICOM metadata, private elements (requires GCP) |
| `cli_guide.md` | Command-line tools (`idc download`, manifest files) |

## IDC Data Model

IDC adds two grouping levels above the standard DICOM hierarchy (Patient → Study → Series → Instance):

- **collection_id**: Groups patients by disease, modality, or research focus (e.g., `tcga_luad`, `nlst`). A patient belongs to exactly one collection.
- **analysis_result_id**: Identifies derived objects (segmentations, annotations, radiomics features) across one or more original collections.

Use `collection_id` to find original imaging data, may include annotations deposited along with the images; use `analysis_result_id` to find AI-generated or expert annotations.

**Key identifiers for queries:**
| Identifier | Scope | Use for |
|------------|-------|---------|
| `collection_id` | Dataset grouping | Filtering by project/study |
| `PatientID` | Patient | Grouping images by patient |
| `StudyInstanceUID` | DICOM study | Grouping of related series, visualization |
| `SeriesInstanceUID` | DICOM series | Grouping of related series, visualization |

## Index Tables

The `idc-index` package provides multiple metadata index tables, accessible via SQL or as pandas DataFrames.

**Complete index table documentation:** Use https://idc-index.readthedocs.io/en/latest/indices_reference.html for quick check of available tables and columns without executing any code.

**Important:** Use `client.indices_overview` to get current table descriptions and column schemas. This is the authoritative source for available columns and their types — always query it when writing SQL or exploring data structure.

### Available Tables

| Table | Row Granularity | Loaded | Description |
|-------|-----------------|--------|-------------|
| `index` | 1 row = 1 DICOM series | Auto | Primary metadata for all current IDC data |
| `prior_versions_index` | 1 row = 1 DICOM series | Auto | Series from previous IDC releases; for downloading deprecated data |
| `collections_index` | 1 row = 1 collection | fetch_index() | Collection-level metadata and descriptions |
| `analysis_results_index` | 1 row = 1 analysis result collection | fetch_index() | Metadata about derived datasets (annotations, segmentations) |
| `clinical_index` | 1 row = 1 clinical data column | fetch_index() | Dictionary mapping clinical table columns to collections |
| `sm_index` | 1 row = 1 slide microscopy series | fetch_index() | Slide Microscopy (pathology) series metadata |
| `sm_instance_index` | 1 row = 1 slide microscopy instance | fetch_index() | Instance-level (SOPInstanceUID) metadata for slide microscopy |
| `seg_index` | 1 row = 1 DICOM Segmentation series | fetch_index() | Segmentation metadata: algorithm, segment count, reference to source image series |
| `ann_index` | 1 row = 1 DICOM ANN series | fetch_index() | Microscopy Bulk Simple Annotations series metadata; references annotated image series |
| `ann_group_index` | 1 row = 1 annotation group | fetch_index() | Detailed annotation group metadata: graphic type, annotation count, property codes, algorithm |
| `contrast_index` | 1 row = 1 series with contrast info | fetch_index() | Contrast agent metadata: agent name, ingredient, administration route (CT, MR, PT, XA, RF) |

**Auto** = loaded automatically when `IDCClient()` is instantiated
**fetch_index()** = requires `client.fetch_index("table_name")` to load

### Joining Tables

**Key columns are not explicitly labeled, the following is a subset that can be used in joins.**

| Join Column | Tables | Use Case |
|-------------|--------|----------|
| `collection_id` | index, prior_versions_index, collections_index, clinical_index | Link series to collection metadata or clinical data |
| `SeriesInstanceUID` | index, prior_versions_index, sm_index, sm_instance_index | Link series across tables; connect to slide microscopy details |
| `StudyInstanceUID` | index, prior_versions_index | Link studies across current and historical data |
| `PatientID` | index, prior_versions_index | Link patients across current and historical data |
| `analysis_result_id` | index, analysis_results_index | Link series to analysis result metadata (annotations, segmentations) |
| `source_DOI` | index, analysis_results_index | Link by publication DOI |
| `crdc_series_uuid` | index, prior_versions_index | Link by CRDC unique identifier |
| `Modality` | index, prior_versions_index | Filter by imaging modality |
| `SeriesInstanceUID` | index, seg_index, ann_index, ann_group_index, contrast_index | Link segmentation/annotation/contrast series to its index metadata |
| `segmented_SeriesInstanceUID` | seg_index → index | Link segmentation to its source image series (join seg_index.segmented_SeriesInstanceUID = index.SeriesInstanceUID) |
| `referenced_SeriesInstanceUID` | ann_index → index | Link annotation to its source image series (join ann_index.referenced_SeriesInstanceUID = index.SeriesInstanceUID) |

**Note:** `Subjects`, `Updated`, and `Description` appear in multiple tables but have different meanings (counts vs identifiers, different update contexts).

For detailed join examples, schema discovery patterns, key columns reference, and DataFrame access, see `references/index_tables_guide.md`.

### Clinical Data Access

```python
# Fetch clinical index (also downloads clinical data tables)
client.fetch_index("clinical_index")

# Query clinical index to find available tables and their columns
tables = client.sql_query("SELECT DISTINCT table_name, column_label FROM clinical_index")

# Load a specific clinical table as DataFrame
clinical_df = client.get_clinical_table("table_name")
```

See `references/clinical_data_guide.md` for detailed workflows including value mapping patterns and joining clinical data with imaging.

## Data Access Options

| Method | Auth Required | Best For |
|--------|---------------|----------|
| `idc-index` | No | Key queries and downloads (recommended) |
| IDC Portal | No | Interactive exploration, manual selection, browser-based download |
| BigQuery | Yes (GCP account) | Complex queries, full DICOM metadata |
| DICOMweb proxy | No | Tool integration via DICOMweb API |
| Cloud storage (S3/GCS) | No | Direct file access, bulk downloads, custom pipelines |

**Cloud storage organization**

IDC maintains all DICOM files in public cloud storage buckets mirrored between AWS S3 and Google Cloud Storage. Files are organized by CRDC UUIDs (not DICOM UIDs) to support versioning.

| Bucket (AWS / GCS) | License | Content |
|--------------------|---------|---------|
| `idc-open-data` / `idc-open-data` | No commercial restriction | >90% of IDC data |
| `idc-open-data-two` / `idc-open-idc1` | No commercial restriction | Collections with potential head scans |
| `idc-open-data-cr` / `idc-open-cr` | Commercial use restricted (CC BY-NC) | ~4% of data |

Files are stored as `<crdc_series_uuid>/<crdc_instance_uuid>.dcm`. Access is free (no egress fees) via AWS CLI, gsutil, or s5cmd with anonymous access. Use `series_aws_url` column from the index for S3 URLs; GCS uses the same path structure.

See `references/cloud_storage_guide.md` for bucket details, access commands, UUID mapping, and versioning.

**DICOMweb access**

IDC data is available via DICOMweb interface (Google Cloud Healthcare API implementation) for integration with PACS systems and DICOMweb-compatible tools.

| Endpoint | Auth | Use Case |
|----------|------|----------|
| Public proxy | No | Testing, moderate queries, daily quota |
| Google Healthcare | Yes (GCP) | Production use, higher quotas |

See `references/dicomweb_guide.md` for endpoint URLs, code examples, supported operations, and implementation details.

## Installation and Setup

**Required (for basic access):**
```bash
pip install --upgrade idc-index
```

**Important:** New IDC data release will always trigger a new version of `idc-index`. Always use `--upgrade` flag while installing, unless an older version is needed for reproducibility.

**IMPORTANT:** IDC data version v23 is current. Always verify your version:
```python
print(client.get_idc_version())  # Should return "v23"
```
If you see an older version, upgrade with: `pip install --upgrade idc-index`

**Tested with:** idc-index 0.11.10 (IDC data version v23)

**Optional (for data analysis):**
```bash
pip install pandas numpy pydicom
```

## Core Capabilities

### 1. Data Discovery and Exploration

Discover what imaging collections and data are available in IDC:

```python
from idc_index import IDCClient

client = IDCClient()

# Get summary statistics from primary index
query = """
SELECT
  collection_id,
  COUNT(DISTINCT PatientID) as patients,
  COUNT(DISTINCT SeriesInstanceUID) as series,
  SUM(series_size_MB) as size_mb
FROM index
GROUP BY collection_id
ORDER BY patients DESC
"""
collections_summary = client.sql_query(query)

# For richer collection metadata, use collections_index
client.fetch_index("collections_index")
collections_info = client.sql_query("""
    SELECT collection_id, CancerTypes, TumorLocations, Species, Subjects, SupportingData
    FROM collections_index
""")

# For analysis results (annotations, segmentations), use analysis_results_index
client.fetch_index("analysis_results_index")
analysis_info = client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Subjects, Collections, Modalities
    FROM analysis_results_index
""")
```

**`collections_index`** provides curated metadata per collection: cancer types, tumor locations, species, subject counts, and supporting data types — without needing to aggregate from the primary index.

**`analysis_results_index`** lists derived datasets (AI segmentations, expert annotations, radiomics features) with their source collections and modalities.

### 2. Querying Metadata with SQL

Query the IDC mini-index using SQL to find specific datasets.

**First, explore available values for filter columns:**
```python
from idc_index import IDCClient

client = IDCClient()

# Check what Modality values exist
modalities = client.sql_query("""
    SELECT DISTINCT Modality, COUNT(*) as series_count
    FROM index
    GROUP BY Modality
    ORDER BY series_count DESC
""")
print(modalities)

# Check what BodyPartExamined values exist for MR modality
body_parts = client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as series_count
    FROM index
    WHERE Modality = 'MR' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined
    ORDER BY series_count DESC
    LIMIT 20
""")
print(body_parts)
```

**Then query with validated filter values:**
```python
# Find breast MRI scans (use actual values from exploration above)
results = client.sql_query("""
    SELECT
      collection_id,
      PatientID,
      SeriesInstanceUID,
      Modality,
      SeriesDescription,
      license_short_name
    FROM index
    WHERE Modality = 'MR'
      AND BodyPartExamined = 'BREAST'
    LIMIT 20
""")

# Access results as pandas DataFrame
for idx, row in results.iterrows():
    print(f"Patient: {row['PatientID']}, Series: {row['SeriesInstanceUID']}")
```

**To filter by cancer type, join with `collections_index`:**
```python
client.fetch_index("collections_index")
results = client.sql_query("""
    SELECT i.collection_id, i.PatientID, i.SeriesInstanceUID, i.Modality
    FROM index i
    JOIN collections_index c ON i.collection_id = c.collection_id
    WHERE c.CancerTypes LIKE '%Breast%'
      AND i.Modality = 'MR'
    LIMIT 20
""")
```

**Available metadata fields** (use `client.indices_overview` for complete list):
- Identifiers: collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID
- Imaging: Modality, BodyPartExamined, Manufacturer, ManufacturerModelName
- Clinical: PatientAge, PatientSex, StudyDate
- Descriptions: StudyDescription, SeriesDescription
- Licensing: license_short_name

**Note:** Cancer type is in `collections_index.CancerTypes`, not in the primary `index` table.

### 3. Downloading DICOM Files

Download imaging data efficiently from IDC's cloud storage:

**Download entire collection:**
```python
from idc_index import IDCClient

client = IDCClient()

# Download small collection (RIDER Pilot ~1GB)
client.download_from_selection(
    collection_id="rider_pilot",
    downloadDir="./data/rider"
)
```

**Download specific series:**
```python
# First, query for series UIDs
series_df = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
      AND collection_id = 'nlst'
    LIMIT 5
""")

# Download only those series
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/lung_ct"
)
```

**Custom directory structure:**

Default `dirTemplate`: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`

```python
# Simplified hierarchy (omit StudyInstanceUID level)
client.download_from_selection(
    collection_id="tcga_luad",
    downloadDir="./data",
    dirTemplate="%collection_id/%PatientID/%Modality"
)
# Results in: ./data/tcga_luad/TCGA-05-4244/CT/

# Flat structure (all files in one directory)
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/flat",
    dirTemplate=""
)
# Results in: ./data/flat/*.dcm
```

**Downloaded file names:**

Individual DICOM files are named using their CRDC instance UUID: `<crdc_instance_uuid>.dcm` (e.g., `0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm`). This UUID-based naming:
- Enables version tracking (UUIDs change when file content changes)
- Matches cloud storage organization (`s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm`)
- Differs from DICOM UIDs (SOPInstanceUID) which are preserved inside the file metadata

To identify files, use the `crdc_instance_uuid` column in queries or read DICOM metadata (SOPInstanceUID) from the files.

### Command-Line Download

The `idc download` command provides command-line access to download functionality without writing Python code. Available after installing `idc-index`.

**Auto-detects input type:** manifest file path, or identifiers (collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID, crdc_series_uuid).

```bash
# Download entire collection
idc download rider_pilot --download-dir ./data

# Download specific series by UID
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Download multiple items (comma-separated)
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# Download from manifest file (auto-detected)
idc download manifest.txt --download-dir ./data
```

**Options:**

| Option | Description |
|--------|-------------|
| `--download-dir` | Output directory (default: current directory) |
| `--dir-template` | Directory hierarchy template (default: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`) |
| `--log-level` | Verbosity: debug, info, warning, error, critical |

**Manifest files:**

Manifest files contain S3 URLs (one per line) and can be:
- Exported from the IDC Portal after cohort selection
- Shared by collaborators for reproducible data access
- Generated programmatically from query results

Format (one S3 URL per line):
```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

**Example: Generate manifest from Python query:**

```python
from idc_index import IDCClient

client = IDCClient()

# Query for series URLs
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

# Save as manifest file
with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

Then download:
```bash
idc download ct_manifest.txt --download-dir ./ct_data
```

### 4. Visualizing IDC Images

View DICOM data in browser without downloading:

```python
from idc_index import IDCClient
import webbrowser

client = IDCClient()

# First query to get valid UIDs
results = client.sql_query("""
    SELECT SeriesInstanceUID, StudyInstanceUID
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")

# View single series
viewer_url = client.get_viewer_URL(seriesInstanceUID=results.iloc[0]['SeriesInstanceUID'])
webbrowser.open(viewer_url)

# View all series in a study (useful for multi-series exams like MRI protocols)
viewer_url = client.get_viewer_URL(studyInstanceUID=results.iloc[0]['StudyInstanceUID'])
webbrowser.open(viewer_url)
```

The method automatically selects OHIF v3 for radiology or SLIM for slide microscopy. Viewing by study is useful when a DICOM Study contains multiple Series (e.g., T1, T2, DWI sequences from a single MRI session).

### 5. Understanding and Checking Licenses

Check data licensing before use (critical for commercial applications):

```python
from idc_index import IDCClient

client = IDCClient()

# Check licenses for all collections
query = """
SELECT DISTINCT
  collection_id,
  license_short_name,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM index
GROUP BY collection_id, license_short_name
ORDER BY collection_id
"""

licenses = client.sql_query(query)
print(licenses)
```

**License types in IDC:**
- **CC BY 4.0** / **CC BY 3.0** (~97% of data) - Allows commercial use with attribution
- **CC BY-NC 4.0** / **CC BY-NC 3.0** (~3% of data) - Non-commercial use only
- **Custom licenses** (rare) - Some collections have specific terms (e.g., NLM Terms and Conditions)

**Important:** Always check the license before using IDC data in publications or commercial applications. Each DICOM file is tagged with its specific license in metadata.

### Generating Citations for Attribution

The `source_DOI` column contains DOIs linking to publications describing how the data was generated. To satisfy attribution requirements, use `citations_from_selection()` to generate properly formatted citations:

```python
from idc_index import IDCClient

client = IDCClient()

# Get citations for a collection (APA format by default)
citations = client.citations_from_selection(collection_id="rider_pilot")
for citation in citations:
    print(citation)

# Get citations for specific series
results = client.sql_query("""
    SELECT SeriesInstanceUID FROM index
    WHERE collection_id = 'tcga_luad' LIMIT 5
""")
citations = client.citations_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values)
)

# Alternative format: BibTeX (for LaTeX documents)
bibtex_citations = client.citations_from_selection(
    collection_id="tcga_luad",
    citation_format=IDCClient.CITATION_FORMAT_BIBTEX
)
```

**Parameters:**
- `collection_id`: Filter by collection(s)
- `patientId`: Filter by patient ID(s)
- `studyInstanceUID`: Filter by study UID(s)
- `seriesInstanceUID`: Filter by series UID(s)
- `citation_format`: Use `IDCClient.CITATION_FORMAT_*` constants:
  - `CITATION_FORMAT_APA` (default) - APA style
  - `CITATION_FORMAT_BIBTEX` - BibTeX for LaTeX
  - `CITATION_FORMAT_JSON` - CSL JSON
  - `CITATION_FORMAT_TURTLE` - RDF Turtle

**Best practice:** When publishing results using IDC data, include the generated citations to properly attribute the data sources and satisfy license requirements.

### 6. Batch Processing and Filtering

Process large datasets efficiently with filtering:

```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()

# Find chest CT scans from GE scanners
query = """
SELECT
  SeriesInstanceUID,
  PatientID,
  collection_id,
  ManufacturerModelName
FROM index
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
  AND license_short_name = 'CC BY 4.0'
LIMIT 100
"""

results = client.sql_query(query)

# Save manifest for later
results.to_csv('lung_ct_manifest.csv', index=False)

# Download in batches to avoid timeout
batch_size = 10
for i in range(0, len(results), batch_size):
    batch = results.iloc[i:i+batch_size]
    client.download_from_selection(
        seriesInstanceUID=list(batch['SeriesInstanceUID'].values),
        downloadDir=f"./data/batch_{i//batch_size}"
    )
```

### 7. Advanced Queries with BigQuery

For queries requiring full DICOM metadata, complex JOINs, clinical data tables, or private DICOM elements, use Google BigQuery. Requires GCP account with billing enabled.

**Quick reference:**
- Dataset: `bigquery-public-data.idc_current.*`
- Main table: `dicom_all` (combined metadata)
- Full metadata: `dicom_metadata` (all DICOM tags)
- Private elements: `OtherElements` column (vendor-specific tags like diffusion b-values)

See `references/bigquery_guide.md` for setup, table schemas, query patterns, private element access, and cost optimization.

**Before using BigQuery**, always check if a specialized index table already has the metadata you need:
1. Use `client.indices_overview` or the [idc-index indices reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html) to discover all available tables and their columns
2. Fetch the relevant index: `client.fetch_index("table_name")`
3. Query locally with `client.sql_query()` (free, no GCP account needed)

Common specialized indices: `seg_index` (segmentations), `ann_index` / `ann_group_index` (microscopy annotations), `sm_index` (slide microscopy), `collections_index` (collection metadata). Only use BigQuery if you need private DICOM elements or attributes not in any index.

### 8. Tool Selection Guide

| Task | Tool | Reference |
|------|------|-----------|
| Programmatic queries & downloads | `idc-index` | This document |
| Interactive exploration | IDC Portal | https://portal.imaging.datacommons.cancer.gov/ |
| Complex metadata queries | BigQuery | `references/bigquery_guide.md` |
| 3D visualization & analysis | SlicerIDCBrowser | https://github.com/ImagingDataCommons/SlicerIDCBrowser |

**Default choice:** Use `idc-index` for most tasks (no auth, easy API, batch downloads).

### 9. Integration with Analysis Pipelines

Integrate IDC data into imaging analysis workflows:

**Read downloaded DICOM files:**
```python
import pydicom
import os

# Read DICOM files from downloaded series
series_dir = "./data/rider/rider_pilot/RIDER-1007893286/CT_1.3.6.1..."

dicom_files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)
               if f.endswith('.dcm')]

# Load first image
ds = pydicom.dcmread(dicom_files[0])
print(f"Patient ID: {ds.PatientID}")
print(f"Modality: {ds.Modality}")
print(f"Image shape: {ds.pixel_array.shape}")
```

**Build 3D volume from CT series:**
```python
import pydicom
import numpy as np
from pathlib import Path

def load_ct_series(series_path):
    """Load CT series as 3D numpy array"""
    files = sorted(Path(series_path).glob('*.dcm'))
    slices = [pydicom.dcmread(str(f)) for f in files]

    # Sort by slice location
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # Stack into 3D array
    volume = np.stack([s.pixel_array for s in slices])

    return volume, slices[0]  # Return volume and first slice for metadata

volume, metadata = load_ct_series("./data/lung_ct/series_dir")
print(f"Volume shape: {volume.shape}")  # (z, y, x)
```

**Integrate with SimpleITK:**
```python
import SimpleITK as sitk
from pathlib import Path

# Read DICOM series
series_path = "./data/ct_series"
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(series_path)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# Apply processing
smoothed = sitk.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=5)

# Save as NIfTI
sitk.WriteImage(smoothed, "processed_volume.nii.gz")
```

## Common Use Cases

See `references/use_cases.md` for complete end-to-end workflow examples including:
- Building deep learning training datasets from lung CT scans
- Comparing image quality across scanner manufacturers
- Previewing data in browser before downloading
- License-aware batch downloads for commercial use

## Best Practices

- **Verify IDC version before generating responses** - Always call `client.get_idc_version()` at the start of a session to confirm you're using the expected data version (currently v23). If using an older version, recommend `pip install --upgrade idc-index`
- **Check licenses before use** - Always query the `license_short_name` field and respect licensing terms (CC BY vs CC BY-NC)
- **Generate citations for attribution** - Use `citations_from_selection()` to get properly formatted citations from `source_DOI` values; include these in publications
- **Start with small queries** - Use `LIMIT` clause when exploring to avoid long downloads and understand data structure
- **Use mini-index for simple queries** - Only use BigQuery when you need comprehensive metadata or complex JOINs
- **Organize downloads with dirTemplate** - Use meaningful directory structures like `%collection_id/%PatientID/%Modality`
- **Cache query results** - Save DataFrames to CSV files to avoid re-querying and ensure reproducibility
- **Estimate size first** - Check collection size before downloading - some collection sizes are in terabytes!
- **Save manifests** - Always save query results with Series UIDs for reproducibility and data provenance
- **Read documentation** - IDC data structure and metadata fields are documented at https://learn.canceridc.dev/
- **Use IDC forum** - Search for questons/answers and ask your questions to the IDC maintainers and users at https://discourse.canceridc.dev/

## Troubleshooting

**Issue: `ModuleNotFoundError: No module named 'idc_index'`**
- **Cause:** idc-index package not installed
- **Solution:** Install with `pip install --upgrade idc-index`

**Issue: Download fails with connection timeout**
- **Cause:** Network instability or large download size
- **Solution:**
  - Download smaller batches (e.g., 10-20 series at a time)
  - Check network connection
  - Use `dirTemplate` to organize downloads by batch
  - Implement retry logic with delays

**Issue: `BigQuery quota exceeded` or billing errors**
- **Cause:** BigQuery requires billing-enabled GCP project
- **Solution:** Use idc-index mini-index for simple queries (no billing required), or see `references/bigquery_guide.md` for cost optimization tips

**Issue: Series UID not found or no data returned**
- **Cause:** Typo in UID, data not in current IDC version, or wrong field name
- **Solution:**
  - Check if data is in current IDC version (some old data may be deprecated)
  - Use `LIMIT 5` to test query first
  - Check field names against metadata schema documentation

**Issue: Downloaded DICOM files won't open**
- **Cause:** Corrupted download or incompatible viewer
- **Solution:**
  - Check DICOM object type (Modality and SOPClassUID attributes) - some object types require specialized tools
  - Verify file integrity (check file sizes)
  - Use pydicom to validate: `pydicom.dcmread(file, force=True)`
  - Try different DICOM viewer (3D Slicer, Horos, RadiAnt, QuPath)
  - Re-download the series

## Common SQL Query Patterns

See `references/sql_patterns.md` for quick-reference SQL patterns including:
- Filter value discovery (modalities, body parts, manufacturers)
- Annotation and segmentation queries (including seg_index, ann_index joins)
- Slide microscopy queries (sm_index patterns)
- Download size estimation
- Clinical data linking

For segmentation and annotation details, also see `references/digital_pathology_guide.md`.

## Related Skills

The following skills complement IDC workflows for downstream analysis and visualization:

### DICOM Processing
- **pydicom** - Read, write, and manipulate downloaded DICOM files. Use for extracting pixel data, reading metadata, anonymization, and format conversion. Essential for working with IDC radiology data (CT, MR, PET).

### Pathology and Slide Microscopy
See `references/digital_pathology_guide.md` for DICOM-compatible tools (highdicom, wsidicom, TIA-Toolbox, Slim viewer).

### Metadata Visualization
- **matplotlib** - Low-level plotting for full customization. Use for creating static figures summarizing IDC query results (bar charts of modalities, histograms of series counts, etc.).
- **seaborn** - Statistical visualization with pandas integration. Use for quick exploration of IDC metadata distributions, relationships between variables, and categorical comparisons with attractive defaults.
- **plotly** - Interactive visualization. Use when you need hover info, zoom, and pan for exploring IDC metadata, or for creating web-embeddable dashboards of collection statistics.

### Data Exploration
- **exploratory-data-analysis** - Comprehensive EDA on scientific data files. Use after downloading IDC data to understand file structure, quality, and characteristics before analysis.

## Resources

### Schema Reference (Primary Source)

**Always use `client.indices_overview` for current column schemas.** This ensures accuracy with the installed idc-index version:

```python
# Get all column names and types for any table
schema = client.indices_overview["index"]["schema"]
columns = [(c['name'], c['type'], c.get('description', '')) for c in schema['columns']]
```

### Reference Documentation

See the Quick Navigation section at the top for the full list of reference guides with decision triggers.

- **[indices_reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html)** - External documentation for index tables (may be ahead of the installed version)

### External Links

- **IDC Portal**: https://portal.imaging.datacommons.cancer.gov/explore/
- **Documentation**: https://learn.canceridc.dev/
- **Tutorials**: https://github.com/ImagingDataCommons/IDC-Tutorials
- **User Forum**: https://discourse.canceridc.dev/
- **idc-index GitHub**: https://github.com/ImagingDataCommons/idc-index
- **Citation**: Fedorov, A., et al. "National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence." RadioGraphics 43.12 (2023). https://doi.org/10.1148/rg.230180

### Skill Updates

This skill version is available in skill metadata. To check for updates:
- Visit the [releases page](https://github.com/ImagingDataCommons/idc-claude-skill/releases)
- Watch the repository on GitHub (Watch → Custom → Releases)

---

## Reference: Bigquery_Guide

# BigQuery Guide for IDC

**Tested with:** IDC data version v23

For most queries and downloads, use `idc-index` (see main SKILL.md). This guide covers BigQuery for advanced use cases requiring full DICOM metadata or complex joins.

## Prerequisites

**Requirements:**
1. Google account
2. Google Cloud project with billing enabled (first 1 TB/month free)
3. `google-cloud-bigquery` Python package or BigQuery console access

**Authentication setup:**
```bash
# Install Google Cloud SDK, then:
gcloud auth application-default login
```

## When to Use BigQuery

Use BigQuery instead of `idc-index` when you need:
- Full DICOM metadata (all 4000+ tags, not just the ~50 in idc-index)
- Complex joins across clinical data tables
- DICOM sequence attributes (nested structures)
- Queries on fields not in the idc-index mini-index
- Private DICOM elements (vendor-specific tags in OtherElements column)

## Accessing IDC in BigQuery

### Dataset Structure

All IDC tables are in the `bigquery-public-data` BigQuery project.

**Current version (recommended for exploration):**
- `bigquery-public-data.idc_current.*`
- `bigquery-public-data.idc_current_clinical.*`

**Versioned datasets (recommended for reproducibility):**

- `bigquery-public-data.idc_v{IDC version}.*`
- `bigquery-public-data.idc_v{IDC version}_clinical.*`

Always use versioned datasets for reproducible research!

## Key Tables

### dicom_all
Primary table joining complete DICOM metadata with IDC-specific columns (collection_id, gcs_url, license). Contains all DICOM tags from `dicom_metadata` plus collection and administrative metadata. See [dicom_all.sql](https://github.com/ImagingDataCommons/etl_flow/blob/master/bq/generate_tables_and_views/derived_tables/BQ_Table_Building/derived_data_views/sql/dicom_all.sql) for the exact derivation.

```sql
SELECT 
  collection_id,
  PatientID,
  StudyInstanceUID, 
  SeriesInstanceUID,
  Modality,
  BodyPartExamined,
  SeriesDescription,
  gcs_url,
  license_short_name
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
LIMIT 10
```

### Derived Tables

**segmentations** - DICOM Segmentation objects
```sql
SELECT *
FROM `bigquery-public-data.idc_current.segmentations`
LIMIT 10
```

**measurement_groups** - SR TID1500 measurement groups
**qualitative_measurements** - Coded evaluations
**quantitative_measurements** - Numeric measurements

### Collection Metadata

**original_collections_metadata** - Collection-level descriptions

```sql
SELECT
  collection_id,
  CancerTypes,
  TumorLocations,
  Subjects,
  src.source_doi,
  src.ImageTypes,
  src.license.license_short_name
FROM `bigquery-public-data.idc_current.original_collections_metadata`,
UNNEST(Sources) AS src
WHERE CancerTypes LIKE '%Lung%'
```

## Common Query Patterns

### Find Collections by Criteria

```sql
SELECT 
  collection_id,
  COUNT(DISTINCT PatientID) as patient_count,
  COUNT(DISTINCT SeriesInstanceUID) as series_count,
  ARRAY_AGG(DISTINCT Modality) as modalities
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE BodyPartExamined LIKE '%BRAIN%'
GROUP BY collection_id
HAVING patient_count > 50
ORDER BY patient_count DESC
```

### Get Download URLs

```sql
SELECT
  SeriesInstanceUID,
  gcs_url
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'rider_pilot'
  AND Modality = 'CT'
```

### Find Studies with Multiple Modalities

```sql
SELECT
  StudyInstanceUID,
  ARRAY_AGG(DISTINCT Modality) as modalities,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM `bigquery-public-data.idc_current.dicom_all`
GROUP BY StudyInstanceUID
HAVING ARRAY_LENGTH(ARRAY_AGG(DISTINCT Modality)) > 1
LIMIT 100
```

### License Filtering

```sql
SELECT
  collection_id,
  license_short_name,
  COUNT(*) as instance_count
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE license_short_name = 'CC BY 4.0'
GROUP BY collection_id, license_short_name
```

### Find Segmentations with Source Images

```sql
SELECT
  src.collection_id,
  seg.SeriesInstanceUID as seg_series,
  seg.SegmentedPropertyType,
  src.SeriesInstanceUID as source_series,
  src.Modality as source_modality
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.dicom_all` src
  ON seg.segmented_SeriesInstanceUID = src.SeriesInstanceUID
WHERE src.collection_id = 'qin_prostate_repeatability'
LIMIT 10
```

## Private DICOM Elements

Private DICOM elements are vendor-specific attributes not defined in the DICOM standard. They often contain essential acquisition parameters (like diffusion b-values, gradient directions, or scanner-specific settings) that are critical for image interpretation and analysis.

### Understanding Private Elements

**How private elements work:**
- Private elements use odd-numbered group numbers (e.g., 0019, 0043, 2001)
- Each vendor reserves blocks of 256 elements using Private Creator identifiers at positions (gggg,0010-00FF)
- For example, GE uses Private Creator "GEMS_PARM_01" at (0043,0010) to reserve elements (0043,1000-10FF)

**Standard vs. private tags:** Some parameters exist in both forms:
| Parameter | Standard Tag | GE | Siemens | Philips |
|-----------|--------------|-----|---------|---------|
| Diffusion b-value | (0018,9087) | (0043,1039) | (0019,100C) | (2001,1003) |
| Private Creator | - | GEMS_PARM_01 | SIEMENS CSA HEADER | Philips Imaging |

Older scanners typically populate only private tags; newer scanners may use standard tags. Always check both.

**Challenges with private elements:**
- Require manufacturer DICOM Conformance Statements to interpret
- Tag meanings can change between software versions
- May be removed during de-identification for HIPAA compliance
- Value encoding varies (string vs. numeric, different units)

### Accessing Private Elements in BigQuery

Private elements are stored in the `OtherElements` column of `dicom_all` as an array of structs with `Tag` and `Data` fields.

**Tag notation:** DICOM notation (0043,1039) becomes BigQuery format `Tag_00431039`.

### Private Element Query Patterns

#### Discover Available Private Tags

List all non-empty private tags for a collection:

```sql
SELECT
  other_elements.Tag,
  COUNT(*) AS instance_count,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS LIMIT 5) AS sample_values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
  AND ARRAY_LENGTH(other_elements.Data) > 0
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY other_elements.Tag
ORDER BY instance_count DESC
```

For a specific series:

```sql
SELECT
  other_elements.Tag,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS) AS values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE SeriesInstanceUID = '1.3.6.1.4.1.14519.5.2.1.7311.5101.206828891270520544417996275680'
  AND ARRAY_LENGTH(other_elements.Data) > 0
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY other_elements.Tag
```

To identify the Private Creator for a tag, look for the reservation element in the same group. For example, if you find `Tag_00431039`, the Private Creator is at `Tag_00430010` (the tag that reserves block 10xx in group 0043).

#### Identify Equipment Manufacturer

Determine what equipment produced the data to find the correct DICOM Conformance Statement:

```sql
SELECT DISTINCT Manufacturer, ManufacturerModelName
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
```

#### Access Private Element Values

Use `UNNEST` to access individual private elements:

```sql
SELECT
  SeriesInstanceUID,
  SeriesDescription,
  other_elements.Data[SAFE_OFFSET(0)] AS b_value
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND other_elements.Tag = 'Tag_00431039'
LIMIT 10
```

#### Aggregate Values by Series

Collect all unique values across slices in a series:

```sql
SELECT
  SeriesInstanceUID,
  ANY_VALUE(SeriesDescription) AS SeriesDescription,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)]) AS b_values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND other_elements.Tag = 'Tag_00431039'
GROUP BY SeriesInstanceUID
```

#### Combine Standard and Private Filters

Filter using both standard DICOM attributes and private element values:

```sql
SELECT
  PatientID,
  SeriesInstanceUID,
  ANY_VALUE(SeriesDescription) AS SeriesDescription,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)]) AS b_values,
  COUNT(DISTINCT SOPInstanceUID) AS n_slices
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
  AND other_elements.Tag = 'Tag_00431039'
  AND ImageType[SAFE_OFFSET(0)] = 'ORIGINAL'
  AND other_elements.Data[SAFE_OFFSET(0)] = '1400'
GROUP BY PatientID, SeriesInstanceUID
ORDER BY PatientID
```

#### Cross-Collection Analysis

Survey usage of a private tag across all IDC collections:

```sql
SELECT
  collection_id,
  ARRAY_TO_STRING(ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS), ', ') AS values_found,
  ARRAY_AGG(DISTINCT Manufacturer IGNORE NULLS) AS manufacturers
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE other_elements.Tag = 'Tag_00431039'
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY collection_id
ORDER BY collection_id
```

### Workflow: Finding and Using Private Tags

1. **Discover available private tags** in your collection using the discovery query above
2. **Identify the manufacturer** to know which conformance statement to consult
3. **Find the DICOM Conformance Statement** from the manufacturer's website (see Resources below)
4. **Search the conformance statement** for the parameter you need (e.g., "b_value", "gradient") to understand what each tag contains
5. **Convert tag to BigQuery format:** (gggg,eeee) → `Tag_ggggeeee`
6. **Query and verify** results visually in the IDC Viewer

### Data Quality Notes

- Some collections show unrealistic values (e.g., b-value "1000000600") indicating encoding issues or different conventions
- IDC data is de-identified; private tags containing PHI may have been removed or modified
- The same tag may have different meanings across software versions
- Always verify query results visually using the [IDC Viewer](https://viewer.imaging.datacommons.cancer.gov/) before large-scale analysis

### Private Element Resources

**Manufacturer DICOM Conformance Statements:**
- [GE Healthcare MR](https://www.gehealthcare.com/products/interoperability/dicom/magnetic-resonance-imaging-dicom-conformance-statements)
- [Siemens MR](https://www.siemens-healthineers.com/services/it-standards/dicom-conformance-statements-magnetic-resonance)
- [Siemens CT](https://www.siemens-healthineers.com/services/it-standards/dicom-conformance-statements-computed-tomography)

**DICOM Standard:**
- [Part 5 Section 7.8 - Private Data Elements](https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_7.8.html)
- [Part 15 Appendix E - De-identification Profiles](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html)

**Community Resources:**
- [NAMIC Wiki: DWI/DTI DICOM](https://www.na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI) - comprehensive vendor comparison for diffusion imaging
- [StandardizeBValue](https://github.com/nslay/StandardizeBValue) - tool to extract vendor b-values to standard tags

## Using Query Results with idc-index

Combine BigQuery for complex queries with idc-index for downloads (no GCP auth needed for downloads):

```python
from google.cloud import bigquery
from idc_index import IDCClient

# Initialize BigQuery client
# Requires: pip install google-cloud-bigquery
# Auth: gcloud auth application-default login
# Project: needed for billing even on public datasets (free tier applies)
bq_client = bigquery.Client(project="your-gcp-project-id")

# Query for series with specific criteria
query = """
SELECT DISTINCT SeriesInstanceUID
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'tcga_luad'
  AND Modality = 'CT'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
LIMIT 100
"""

df = bq_client.query(query).to_dataframe()
print(f"Found {len(df)} GE CT series")

# Download with idc-index (no GCP auth required)
idc_client = IDCClient()
idc_client.download_from_selection(
    seriesInstanceUID=list(df['SeriesInstanceUID'].values),
    downloadDir="./tcga_luad_thin_ct"
)
```

## Cost and Optimization

**Pricing:** $5 per TB scanned (first 1 TB/month free). Most users stay within free tier.

**Minimize data scanned:**
- Select only needed columns (not `SELECT *`)
- Filter early with `WHERE` clauses
- Use `LIMIT` when testing
- Use `dicom_all` instead of `dicom_metadata` when possible (smaller)
- Preview queries in BQ console (free, shows bytes to scan)

**Check cost before running:**
```python
query_job = client.query(query, job_config=bigquery.QueryJobConfig(dry_run=True))
print(f"Query will scan {query_job.total_bytes_processed / 1e9:.2f} GB")
```

**Use materialized tables:** IDC provides both views (`table_name_view`) and materialized tables (`table_name`). Always use the materialized tables (faster, lower cost).

## Clinical Data

Clinical data is in separate datasets with collection-specific tables. All clinical data available via `idc-index` is also available in BigQuery, with the same content and structure. Use BigQuery when you need complex cross-collection queries or joins that aren't possible with the local `idc-index` tables.

**Datasets:**
- `bigquery-public-data.idc_current_clinical` - current release (for exploration)
- `bigquery-public-data.idc_v{version}_clinical` - versioned datasets (for reproducibility)

Currently there are ~130 clinical tables representing ~70 collections. Not all collections have clinical data (started in IDC v11).

### Clinical Table Naming

Most collections use a single table: `<collection_id>_clinical`

**Exception:** ACRIN collections use multiple tables for different data types (e.g., `acrin_6698_A0`, `acrin_6698_A1`, etc.).

### Metadata Tables

Two metadata tables help navigate clinical data:

**table_metadata** - Collection-level information:
```sql
SELECT
  collection_id,
  table_name,
  table_description
FROM `bigquery-public-data.idc_current_clinical.table_metadata`
WHERE collection_id = 'nlst'
```

**column_metadata** - Attribute-level details with value mappings:
```sql
SELECT
  collection_id,
  table_name,
  column,
  column_label,
  data_type,
  values
FROM `bigquery-public-data.idc_current_clinical.column_metadata`
WHERE collection_id = 'nlst'
  AND column_label LIKE '%stage%'
```

The `values` field contains observed attribute values with their descriptions (same as in `idc-index` clinical_index).

### Common Clinical Queries

**List available clinical tables:**
```sql
SELECT table_name
FROM `bigquery-public-data.idc_current_clinical.INFORMATION_SCHEMA.TABLES`
WHERE table_name NOT IN ('table_metadata', 'column_metadata')
```

**Find collections with specific clinical attributes:**
```sql
SELECT DISTINCT collection_id, table_name, column, column_label
FROM `bigquery-public-data.idc_current_clinical.column_metadata`
WHERE LOWER(column_label) LIKE '%chemotherapy%'
```

**Query clinical data for a collection:**
```sql
-- Example: NLST cancer staging data
SELECT
  dicom_patient_id,
  clinical_stag,
  path_stag,
  de_stag
FROM `bigquery-public-data.idc_current_clinical.nlst_canc`
WHERE clinical_stag IS NOT NULL
LIMIT 10
```

**Join clinical with imaging data:**
```sql
SELECT
  d.PatientID,
  d.StudyInstanceUID,
  d.Modality,
  c.clinical_stag,
  c.path_stag
FROM `bigquery-public-data.idc_current.dicom_all` d
JOIN `bigquery-public-data.idc_current_clinical.nlst_canc` c
  ON d.PatientID = c.dicom_patient_id
WHERE d.collection_id = 'nlst'
  AND d.Modality = 'CT'
  AND c.clinical_stag = '400'  -- Stage IV
LIMIT 20
```

**Cross-collection clinical search:**
```sql
-- Find all collections with staging information
SELECT
  cm.collection_id,
  cm.table_name,
  cm.column,
  cm.column_label
FROM `bigquery-public-data.idc_current_clinical.column_metadata` cm
WHERE LOWER(cm.column_label) LIKE '%stage%'
ORDER BY cm.collection_id
```

### Key Column: dicom_patient_id

Every clinical table includes `dicom_patient_id`, which matches the DICOM `PatientID` attribute in imaging tables. This is the join key between clinical and imaging data.

**Note:** Clinical table schemas vary significantly by collection. Always check available columns first:
```sql
SELECT column_name, data_type
FROM `bigquery-public-data.idc_current_clinical.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'nlst_canc'
```

See `references/clinical_data_guide.md` for detailed workflows using `idc-index`, which provides the same clinical data without requiring BigQuery authentication.

## Important Notes

- Tables are read-only (public dataset)
- Schema changes between IDC versions
- Use versioned datasets for reproducibility
- Some DICOM sequences >15 levels deep are not extracted
- Very large sequences (>1MB) may be truncated
- Always check data license before use

## Common Errors

**Issue: Billing must be enabled**
- Cause: BigQuery requires a billing-enabled GCP project
- Solution: Enable billing in Google Cloud Console or use idc-index mini-index instead

**Issue: Query exceeds resource limits**
- Cause: Query scans too much data or is too complex
- Solution: Add more specific WHERE filters, use LIMIT, break into smaller queries

**Issue: Column not found**
- Cause: Field name typo or not in selected table
- Solution: Check table schema first with `INFORMATION_SCHEMA.COLUMNS`

**Issue: Permission denied**
- Cause: Not authenticated to Google Cloud
- Solution: Run `gcloud auth application-default login` or set GOOGLE_APPLICATION_CREDENTIALS

## Resources

- [Understanding the BigQuery DICOM schema](https://docs.cloud.google.com/healthcare-api/docs/how-tos/dicom-bigquery-schema)
- [BigQuery Query Syntax](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [Kaggle Intro to SQL](https://www.kaggle.com/learn/intro-to-sql)
- [Sample BigQuery queries of IDC data](https://github.com/ImagingDataCommons/idc-bigquery-cookbook)

---

## Reference: Cli_Guide

# idc-index Command Line Interface Guide

The `idc-index` package provides command-line tools for downloading DICOM data from the NCI Imaging Data Commons without writing Python code.

## Installation

```bash
pip install --upgrade idc-index
```

After installation, the `idc` command is available in your terminal.

## Available Commands

| Command | Purpose |
|---------|---------|
| `idc download` | General-purpose download with auto-detection of input type |
| `idc download-from-manifest` | Download from manifest file with validation and progress tracking |
| `idc download-from-selection` | Filter-based download with multiple criteria |

---

## idc download

General-purpose download command that intelligently interprets input. It determines whether the input corresponds to a manifest file path or a list of identifiers (collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID, crdc_series_uuid).

### Usage

```bash
# Download entire collection
idc download rider_pilot --download-dir ./data

# Download specific series by UID
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Download multiple items (comma-separated)
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# Download from manifest file (auto-detected by file extension)
idc download manifest.txt --download-dir ./data
```

### Options

| Option | Description |
|--------|-------------|
| `--download-dir` | Destination directory (default: current directory) |
| `--dir-template` | Directory hierarchy template (default: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`) |
| `--log-level` | Verbosity: debug, info, warning, error, critical |

### Directory Template Variables

Use these variables in `--dir-template` to organize downloads:

- `%collection_id` - Collection identifier
- `%PatientID` - Patient identifier
- `%StudyInstanceUID` - Study UID
- `%SeriesInstanceUID` - Series UID
- `%Modality` - Imaging modality (CT, MR, PT, etc.)

**Examples:**

```bash
# Flat structure (all files in one directory)
idc download rider_pilot --download-dir ./data --dir-template ""

# Simplified hierarchy
idc download rider_pilot --download-dir ./data --dir-template "%collection_id/%PatientID/%Modality"
```

---

## idc download-from-manifest

Specialized for downloading from manifest files with built-in validation, progress tracking, and resume capability.

### Usage

```bash
# Basic download from manifest
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data

# With progress bar and validation
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --show-progress-bar

# Resume interrupted download with s5cmd sync
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### Options

| Option | Description |
|--------|-------------|
| `--manifest-file` | **Required.** Path to manifest file containing S3 URLs |
| `--download-dir` | **Required.** Destination directory |
| `--validate-manifest` | Validate manifest before download (enabled by default) |
| `--show-progress-bar` | Display download progress |
| `--use-s5cmd-sync` | Enable resumable downloads - skips already-downloaded files |
| `--quiet` | Suppress subprocess output |
| `--dir-template` | Directory hierarchy template |
| `--log-level` | Logging verbosity |

### Manifest File Format

Manifest files contain S3 URLs, one per line:

```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

**How to get a manifest file:**

1. **IDC Portal**: Export cohort selection as manifest
2. **Python query**: Generate from SQL results

```python
from idc_index import IDCClient

client = IDCClient()
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

---

## idc download-from-selection

Download data using filter criteria. Filters are applied sequentially.

### Usage

```bash
# Download by collection
idc download-from-selection --collection-id rider_pilot --download-dir ./data

# Download specific series
idc download-from-selection --series-instance-uid "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Multiple filters
idc download-from-selection --collection-id nlst --patient-id "100004" --download-dir ./data

# Dry run - see what would be downloaded without actually downloading
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data
```

### Options

| Option | Description |
|--------|-------------|
| `--download-dir` | **Required.** Destination directory |
| `--collection-id` | Filter by collection identifier |
| `--patient-id` | Filter by patient identifier |
| `--study-instance-uid` | Filter by study UID |
| `--series-instance-uid` | Filter by series UID |
| `--crdc-series-uuid` | Filter by CRDC UUID |
| `--dry-run` | Calculate cohort size without downloading |
| `--show-progress-bar` | Display download progress |
| `--use-s5cmd-sync` | Enable resumable downloads |
| `--dir-template` | Directory hierarchy template |

### Dry Run for Size Estimation

Use `--dry-run` to estimate download size before committing:

```bash
idc download-from-selection --collection-id nlst --dry-run --download-dir ./data
```

This shows:
- Number of series matching filters
- Total download size
- No files are downloaded

---

## Common Workflows

### 1. Download Small Collection for Testing

```bash
# rider_pilot is ~1GB - good for testing
idc download rider_pilot --download-dir ./test_data
```

### 2. Large Dataset with Progress and Resume

```bash
# Use s5cmd sync for large downloads - can resume if interrupted
idc download-from-selection \
    --collection-id nlst \
    --download-dir ./nlst_data \
    --show-progress-bar \
    --use-s5cmd-sync
```

### 3. Estimate Size Before Download

```bash
# Check size first
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data

# Then download if size is acceptable
idc download-from-selection --collection-id tcga_luad --download-dir ./data
```

### 4. Download Specific Modality via Python + CLI

```python
# First, query for series UIDs in Python
from idc_index import IDCClient

client = IDCClient()
results = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE collection_id = 'nlst'
      AND Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
    LIMIT 50
""")

# Save to manifest
results['SeriesInstanceUID'].to_csv('my_series.csv', index=False, header=False)
```

```bash
# Then download via CLI
idc download my_series.csv --download-dir ./lung_ct
```

---

## Built-in Safety Features

The CLI includes several safety features:

- **Disk space checking**: Verifies sufficient space before starting downloads
- **Manifest validation**: Validates manifest file format by default
- **Progress tracking**: Optional progress bar for monitoring large downloads
- **Resume capability**: Use `--use-s5cmd-sync` to continue interrupted downloads

---

## Troubleshooting

### Download Interrupted

Use `--use-s5cmd-sync` to resume:

```bash
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### Connection Timeout

For unstable networks, download in smaller batches using Python to generate multiple manifests, then download sequentially.

---

## See Also

- [idc-index Documentation](https://idc-index.readthedocs.io/)
- [IDC Portal](https://portal.imaging.datacommons.cancer.gov/) - Interactive cohort building
- [IDC Tutorials](https://github.com/ImagingDataCommons/IDC-Tutorials)

---

## Reference: Clinical_Data_Guide

# Clinical Data Guide for IDC

**Tested with:** idc-index 0.11.7 (IDC data version v23)

Clinical data (demographics, diagnoses, therapies, lab tests, staging) accompanies many IDC imaging collections. This guide covers how to discover, access, and integrate clinical data with imaging data using `idc-index`.

## When to Use This Guide

Use this guide when you need to:
- Find what clinical metadata is available for a collection
- Filter patients by clinical criteria (e.g., cancer stage, treatment history)
- Join clinical attributes with imaging data for cohort selection
- Understand and decode coded values in clinical tables

For basic clinical data access, see the "Clinical Data Access" section in the main SKILL.md. This guide provides detailed workflows and advanced patterns.

## Prerequisites

```bash
pip install --upgrade idc-index
```

No BigQuery credentials required - clinical data is packaged with `idc-index`.

## Understanding Clinical Data in IDC

### What is Clinical Data?

Clinical data refers to non-imaging information that accompanies medical images:
- Patient demographics (age, sex, race)
- Clinical history (diagnoses, surgeries, therapies)
- Lab tests and pathology results
- Cancer staging (clinical and pathological)
- Treatment outcomes

### Data Organization

Clinical data in IDC comes from collection-specific spreadsheets provided by data submitters. IDC parses these into queryable tables accessible via `idc-index`.

**Important characteristics:**
- Clinical data is **not harmonized** across collections (terms and formats vary)
- Not all collections have clinical data (check availability first)
- All data is **anonymized** - `dicom_patient_id` links to imaging

### The clinical_index Table

The `clinical_index` serves as a dictionary/catalog of all available clinical data:

| Column | Purpose | Use For |
|--------|---------|---------|
| `collection_id` | Collection identifier | Filtering by collection |
| `table_name` | Full BigQuery table reference | BigQuery queries (if needed) |
| `short_table_name` | Short name | `get_clinical_table()` method |
| `column` | Column name in table | Selecting data columns |
| `column_label` | Human-readable description | Searching for concepts |
| `values` | Observed attribute values for the column | Interpreting coded values |

### The `values` Column

The `values` column contains an array of observed attribute values for the column defined in the `column` field. Each entry has:
- **option_code**: The actual value observed in that column
- **option_description**: Human-readable description of that value (from data dictionary if available, otherwise `None`)

For ACRIN collections, value descriptions come from provided data dictionaries. For other collections, they are derived from inspection of the actual data values.

**Note:** For columns with >20 unique values, the `values` array is left empty (`[]`) for simplicity.

## Core Workflow

### Step 1: Fetch Clinical Index

```python
from idc_index import IDCClient

client = IDCClient()
client.fetch_index('clinical_index')

# View available columns
print(client.clinical_index.columns.tolist())
```

### Step 2: Discover Available Clinical Data

```python
# List all collections with clinical data
collections_with_clinical = client.clinical_index["collection_id"].unique().tolist()
print(f"{len(collections_with_clinical)} collections have clinical data")

# Find clinical attributes for a specific collection
nlst_columns = client.clinical_index[client.clinical_index['collection_id']=='nlst']
nlst_columns[['short_table_name', 'column', 'column_label', 'values']]
```

### Step 3: Search for Specific Attributes

```python
# Search by keyword in column_label (case-insensitive)
stage_attrs = client.clinical_index[
    client.clinical_index["column_label"].str.contains("[Ss]tage", na=False)
]
stage_attrs[["collection_id", "short_table_name", "column", "column_label"]]
```

### Step 4: Load Clinical Table

```python
# Load table using short_table_name
nlst_canc_df = client.get_clinical_table("nlst_canc")

# Examine structure
print(f"Rows: {len(nlst_canc_df)}, Columns: {len(nlst_canc_df.columns)}")
nlst_canc_df.head()
```

### Step 5: Map Coded Values to Descriptions

Many clinical attributes use coded values. The `values` column in `clinical_index` contains an array of observed values with their descriptions (when available).

```python
# Get the clinical_index rows for NLST
nlst_clinical_columns = client.clinical_index[client.clinical_index['collection_id']=='nlst']

# Get observed values for a specific column
# Filter to the row for 'clinical_stag' and extract the values array
clinical_stag_values = nlst_clinical_columns[
    nlst_clinical_columns['column']=='clinical_stag'
]['values'].values[0]

# View the observed values and their descriptions
print(clinical_stag_values)
# Output: array([{'option_code': '.M', 'option_description': 'Missing'},
#                {'option_code': '110', 'option_description': 'Stage IA'},
#                {'option_code': '120', 'option_description': 'Stage IB'}, ...])

# Create mapping dictionary from codes to descriptions
mapping_dict = {item['option_code']: item['option_description'] for item in clinical_stag_values}

# Apply to DataFrame - convert column to string first for consistent matching
nlst_canc_df['clinical_stag_meaning'] = nlst_canc_df['clinical_stag'].astype(str).map(mapping_dict)
```

### Step 6: Join with Imaging Data

The `dicom_patient_id` column links clinical data to imaging. It matches the `PatientID` column in the imaging index.

```python
# Pandas merge approach
import pandas as pd

# Get NLST CT imaging data
nlst_imaging = client.index[(client.index['collection_id']=='nlst') & (client.index['Modality']=='CT')]

# Join with clinical data
merged = pd.merge(
    nlst_imaging[['PatientID', 'StudyInstanceUID']].drop_duplicates(),
    nlst_canc_df[['dicom_patient_id', 'clinical_stag', 'clinical_stag_meaning']],
    left_on='PatientID',
    right_on='dicom_patient_id',
    how='inner'
)
```

```python
# SQL join approach
query = """
SELECT
  index.PatientID,
  index.StudyInstanceUID,
  index.Modality,
  nlst_canc.clinical_stag
FROM index
JOIN nlst_canc ON index.PatientID = nlst_canc.dicom_patient_id
WHERE index.collection_id = 'nlst' AND index.Modality = 'CT'
"""
results = client.sql_query(query)
```

## Common Use Cases

### Use Case 1: Select Patients by Cancer Stage

```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()
client.fetch_index('clinical_index')

# Load clinical table
nlst_canc = client.get_clinical_table("nlst_canc")

# Select Stage IV patients (code '400')
stage_iv_patients = nlst_canc[nlst_canc['clinical_stag'] == '400']['dicom_patient_id']

# Get CT imaging studies for these patients
stage_iv_studies = pd.merge(
    client.index[(client.index['collection_id']=='nlst') & (client.index['Modality']=='CT')],
    stage_iv_patients,
    left_on='PatientID',
    right_on='dicom_patient_id',
    how='inner'
)['StudyInstanceUID'].drop_duplicates()

print(f"Found {len(stage_iv_studies)} CT studies for Stage IV patients")
```

### Use Case 2: Find Collections with Specific Clinical Attributes

```python
# Find collections with chemotherapy information
chemo_collections = client.clinical_index[
    client.clinical_index["column_label"].str.contains("[Cc]hemotherapy", na=False)
]["collection_id"].unique()

print(f"Collections with chemotherapy data: {list(chemo_collections)}")
```

### Use Case 3: Examine Observed Values for a Clinical Attribute

```python
# Find what values have been observed for a specific attribute
chemotherapy_rows = client.clinical_index[
    (client.clinical_index["collection_id"] == "hcc_tace_seg") &
    (client.clinical_index["column"] == "chemotherapy")
]

# Get the observed values array
values_list = chemotherapy_rows["values"].tolist()
print(values_list)
# Output: [[{'option_code': 'Cisplastin', 'option_description': None},
#           {'option_code': 'Cisplatin, Mitomycin-C', 'option_description': None}, ...]]
```

### Use Case 4: Generate Viewer URLs for Selected Patients

```python
import random

# Get studies for a sample Stage IV patient
sample_patient = stage_iv_patients.iloc[0]
studies = client.index[client.index['PatientID'] == sample_patient]['StudyInstanceUID'].unique()

# Generate viewer URL
if len(studies) > 0:
    viewer_url = client.get_viewer_URL(studyInstanceUID=studies[0])
    print(viewer_url)
```

## Key Concepts

### column vs column_label

- **column**: Use for selecting data from tables (programmatic access)
- **column_label**: Use for searching/understanding what data means (human-readable)

Some collections (like `c4kc_kits`) have identical column and column_label. Others (like ACRIN collections) have cryptic column names but descriptive labels.

### option_code vs option_description

The `values` array contains observed attribute values:
- **option_code**: The actual value observed in the column (what you filter on)
- **option_description**: Human-readable description (from data dictionary if available, otherwise `None`)

### dicom_patient_id

Every clinical table includes `dicom_patient_id`, which matches the `PatientID` column in the imaging index. This is the key for joining clinical and imaging data.

## Troubleshooting

### Issue: Clinical table not found

**Cause:** Using wrong table name or table doesn't exist for collection

**Solution:** Query clinical_index first to find available tables:
```python
client.clinical_index[client.clinical_index['collection_id']=='your_collection']['short_table_name'].unique()
```

### Issue: Empty values array

**Cause:** The `values` array is left empty when a column has >20 unique values

**Solution:** Load the clinical table and examine unique values directly:
```python
clinical_df = client.get_clinical_table("table_name")
clinical_df['column_name'].unique()
```

### Issue: Coded values not in mapping

**Cause:** Some values may be missing from the dictionary (e.g., empty strings, special codes like `.M` for missing)

**Solution:** Handle unmapped values gracefully:
```python
df['meaning'] = df['code'].astype(str).map(mapping_dict).fillna('Unknown/Missing')
```

### Issue: No matching patients when joining

**Cause:** Clinical data may include patients without images, or vice versa

**Solution:** Verify patient overlap before joining:
```python
imaging_patients = set(client.index[client.index['collection_id']=='nlst']['PatientID'].unique())
clinical_patients = set(clinical_df['dicom_patient_id'].unique())
overlap = imaging_patients & clinical_patients
print(f"Patients with both imaging and clinical data: {len(overlap)}")
```

## Resources

**IDC Documentation:**
- [Clinical data organization](https://learn.canceridc.dev/data/organization-of-data/clinical) - How clinical data is organized in IDC
- [Clinical data dashboard](https://datastudio.google.com/u/0/reporting/04cf5976-4ea0-4fee-a749-8bfd162f2e87/page/p_s7mk6eybqc) - Visual summary of available clinical data
- [idc-index clinical_index documentation](https://idc-index.readthedocs.io/en/latest/column_descriptions.html#clinical-index)

**Related Guides:**
- `bigquery_guide.md` - Advanced clinical queries via BigQuery
- Main SKILL.md - Core IDC workflows

**IDC Tutorials:**
- [clinical_data_intro.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/advanced_topics/clinical_data_intro.ipynb)
- [exploring_clinical_data.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/getting_started/exploring_clinical_data.ipynb)
- [nlst_clinical_data.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/collections_demos/nlst_clinical_data.ipynb)

---

## Reference: Cloud_Storage_Guide

# Cloud Storage Guide for IDC

IDC maintains all DICOM files in public cloud storage buckets mirrored between Google Cloud Storage (GCS) and AWS S3. This guide covers bucket organization, file structure, access methods, and versioning.

## When to Use Direct Cloud Storage Access

Use direct bucket access when you need:
- Maximum download performance with parallel transfers
- Integration with cloud-native workflows (e.g., running analysis on cloud VMs)
- Programmatic access from tools like s5cmd or gsutil
- Access to specific file versions for reproducibility

For most use cases, `idc-index` is simpler and recommended -— it uses s5cmd internally to download from these same S3 buckets, handling the UUID lookups automatically. Use direct cloud storage when you need raw file access, custom parallelization, or are building cloud-native pipelines.

## Storage Buckets

IDC organizes data across multiple buckets based on licensing and content type. All buckets are mirrored between AWS and GCS with identical content and file paths.

### Bucket Summary

| Purpose | AWS S3 Bucket | GCS Bucket | License | Content |
|---------|---------------|------------|---------|---------|
| Primary data | `idc-open-data` | `idc-open-data` | No commercial restriction | >90% of IDC data |
| Head scans | `idc-open-data-two` | `idc-open-idc1` | No commercial restriction | Collections potentially containing head imaging |
| Commercial-restricted | `idc-open-data-cr` | `idc-open-cr` | Commercial use restricted (CC BY-NC) | ~4% of data |

**Notes:**
- All AWS buckets are in AWS region `us-east-1`
- Prior to IDC v19, GCS used `public-datasets-idc` (now superseded by `idc-open-data`)
- The head scans bucket exists for potential future policy changes regarding facial imaging data
- **Important** Use `idc-index` to get license information - do not rely on bucket name! 

### Why Multiple Buckets?

1. **Licensing separation**: Data with commercial-use restrictions (CC BY-NC) is isolated in `idc-open-data-cr` / `idc-open-cr` to prevent accidental commercial use
2. **Head scan handling**: Collections labeled by TCIA as potentially containing head scans are in separate buckets (`idc-open-data-two` / `idc-open-idc1`) for potential future policy compliance
3. **Historical reasons**: The bucket structure evolved as IDC grew and partnered with different cloud programs

## File Organization Within Buckets

Files are organized by CRDC UUIDs, not DICOM UIDs. This enables versioning while maintaining consistent paths across cloud providers.

### Directory Structure

```
<bucket>/
└── <crdc_series_uuid>/
    ├── <crdc_instance_uuid_1>.dcm
    ├── <crdc_instance_uuid_2>.dcm
    └── ...
```

**Example path:**
```
s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm
```

- `7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9` = series UUID (folder)
- `0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm` = instance UUID (file)

### CRDC UUIDs vs DICOM UIDs

| Identifier Type | Format | Changes When | Use For |
|-----------------|--------|--------------|---------|
| DICOM UID (e.g., SeriesInstanceUID) | Numeric (e.g., `1.3.6.1.4...`) | Never (included in DICOM metadata) | Clinical identification, DICOMweb queries |
| CRDC UUID (e.g., crdc_series_uuid) | UUID (e.g., `e127d258-37c2-...`) | Content changes | File paths, versioning, reproducibility |

**Key insight:** A single DICOM SeriesInstanceUID may have multiple CRDC series UUIDs across IDC versions if the series content changed (instances added/removed, metadata corrected). The CRDC UUID uniquely identifies a specific version of the data.

### Mapping DICOM UIDs to File Paths

Use `idc-index` to get file URLs from DICOM identifiers:

```python
from idc_index import IDCClient

client = IDCClient()

# Get all file URLs for a series
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"
urls = client.get_series_file_URLs(seriesInstanceUID=series_uid)

for url in urls[:3]:
    print(url)
# Returns S3 URLs like: s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm
```

Or query the index directly for URL columns:

```python
# Get series-level URL (points to folder)
result = client.sql_query("""
    SELECT SeriesInstanceUID, series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 3
""")

print(result[['SeriesInstanceUID', 'series_aws_url']])
```

**Available URL column in index:**
- `series_aws_url`: S3 URL to series folder (e.g., `s3://idc-open-data/uuid/*`)

GCS URLs follow the same path structure—replace `s3://` with `gs://` (e.g., `gs://idc-open-data/uuid/*`). When using `idc-index` download methods, GCS access is handled internally.

## Accessing Cloud Storage

All IDC buckets support free egress (no download fees) through partnerships with AWS Open Data and Google Public Data programs. No authentication required.

### AWS S3 Access

**Using AWS CLI (no account required):**
```bash
# List bucket contents
aws s3 ls --no-sign-request s3://idc-open-data/

# List files in a series folder
aws s3 ls --no-sign-request s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/

# Download a single file
aws s3 cp --no-sign-request \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm \
    ./local_file.dcm

# Download entire series folder
aws s3 cp --no-sign-request --recursive \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ \
    ./series_folder/
```

**Using s5cmd (faster for bulk downloads):**
```bash
# Install s5cmd
# macOS: brew install s5cmd
# Linux: download from https://github.com/peak/s5cmd/releases

# Download specific series
s5cmd --no-sign-request cp 's3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/*' ./local_folder/

# Download from manifest file
s5cmd --no-sign-request run manifest.txt
```

**s5cmd manifest format:** The `s5cmd run` command expects one s5cmd command per line, not just URLs:
```
cp s3://idc-open-data/uuid1/instance1.dcm ./local_folder/
cp s3://idc-open-data/uuid1/instance2.dcm ./local_folder/
cp s3://idc-open-data/uuid2/instance3.dcm ./local_folder/
```

IDC Portal exports manifests in this format. When creating manifests programmatically, use `idc-index` download methods (which handle this internally) rather than constructing manifests manually.

### GCS Access

**Using gsutil:**
```bash
# List bucket contents
gsutil ls gs://idc-open-data/

# Download a series folder
gsutil -m cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

**Using gcloud storage (newer CLI):**
```bash
gcloud storage cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

### Python Direct Access

```python
import s3fs
import gcsfs
from idc_index import IDCClient

# First, get a file URL from idc-index
client = IDCClient()
result = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")
# series_aws_url is like: s3://idc-open-data/<uuid>/*
series_url = result['series_aws_url'].iloc[0]
series_path = series_url.replace('s3://', '').rstrip('/*')  # e.g., "idc-open-data/<uuid>"

# AWS S3 access
s3 = s3fs.S3FileSystem(anon=True)
files = s3.ls(series_path)
with s3.open(files[0], 'rb') as f:
    data = f.read()

# GCS access (same path structure as AWS)
gcs = gcsfs.GCSFileSystem(token='anon')
files = gcs.ls(series_path)
with gcs.open(files[0], 'rb') as f:
    data = f.read()
```

## Versioning and Reproducibility

IDC releases new data versions every 2-4 months. The versioning system ensures reproducibility by preserving all historical data.

### How Versioning Works

1. **Snapshots**: Each IDC version (v1, v2, ..., v23, etc.) represents a complete snapshot of all data at release time
2. **UUID-based**: When data changes, new CRDC UUIDs are assigned; old UUIDs remain accessible
3. **Cumulative buckets**: All versions coexist in the same buckets—old series folders

**Version change scenarios:**
| Change Type | DICOM UID | CRDC UUID | Effect |
|-------------|-----------|-----------|--------|
| New series added | New | New | New folder in bucket |
| Instance added to series | Same | New series UUID | New folder, instances may be duplicated |
| Metadata corrected | Same or new | New | New folder with updated files |
| Series removed | N/A | N/A | Old folder remains, not in current index |

**Data removal caveat:** In rare circumstances (e.g., data owner request, PHI incident), data may be removed from IDC entirely, including from all historical versions.

**BigQuery versioned datasets (metadata only, not file storage):**

For querying version-specific metadata, BigQuery provides versioned tables. See `bigquery_guide.md` for details.
- `bigquery-public-data.idc_current` — alias to latest version
- `bigquery-public-data.idc_v23` — specific version (replace 23 with desired version)

### Reproducing a Previous Analysis

The simplest way to ensure reproducibility is to save the `crdc_series_uuid` values of the data you use at analysis time:

```python
from idc_index import IDCClient
import json

client = IDCClient()

# Select data for your analysis
selection = client.sql_query("""
    SELECT crdc_series_uuid
    FROM index
    WHERE collection_id = 'tcga_luad'
      AND Modality = 'CT'
    LIMIT 10
""")
series_uuids = list(selection['crdc_series_uuid'])

# Download the data
client.download_from_selection(seriesInstanceUID=series_uuids, downloadDir="./data")

# Save a manifest for reproducibility
manifest = {
    "crdc_series_uuids": series_uuids,
    "download_date": "2024-01-15",
    "idc_version": client.get_idc_version(),
    "description": "CT scans for lung cancer analysis"
}
with open("analysis_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# Later, reproduce the exact dataset:
with open("analysis_manifest.json") as f:
    manifest = json.load(f)
client.download_from_selection(
    seriesInstanceUID=manifest["crdc_series_uuids"],
    downloadDir="./reproduced_data"
)
```

Since `crdc_series_uuid` identifies an immutable version of each series, saving these UUIDs guarantees you can retrieve the exact same files later.

## Relationship Between Buckets, Versions, and Other Access Methods

### Data Coverage Comparison

| Access Method | Buckets Included | Coverage | Versions |
|---------------|------------------|----------|----------|
| Direct bucket access | All 3 buckets | 100% | All historical |
| `idc-index` download | All 3 buckets | 100% | Current + prior_versions_index |
| IDC Portal | All 3 buckets | 100% | Current only |
| DICOMweb public proxy | All 3 buckets | 100% | Current only |
| Google Healthcare DICOM | `idc-open-data` only | ~96% | Current only |

**Important:** The Google Healthcare API DICOM store only replicates data from `idc-open-data`. Data in `idc-open-data-two` and `idc-open-data-cr` (approximately 4% of total) is not available via Google Healthcare DICOMweb endpoint.

## Best Practices

- **Use `idc-index` for discovery**: Query metadata first, then access buckets with known UUIDs
- **Download defaults to AWS buckets**: request GCS if needed
- **Save manifests**: Store the `series_aws_url` or `crdc_series_uuid` values for reproducibility
- **Check licenses**: Query `license_short_name` before commercial use; CC-NC data requires non-commercial use
- **Use current version unless reproducing**: The `index` table has current data; use `prior_versions_index` only for exact reproducibility

## Troubleshooting

### Issue: "Access Denied" when accessing buckets
- **Cause:** Using signed requests or wrong bucket name
- **Solution:** Use `--no-sign-request` flag with AWS CLI, or `anon=True` with Python libraries

### Issue: File not found at expected path
- **Cause:** Using DICOM UID instead of CRDC UUID, or data changed in newer version
- **Solution:** Query `idc-index` for current `series_aws_url`, or check `prior_versions_index` for historical paths

### Issue: Downloaded files don't match expected series
- **Cause:** Series was revised in a newer IDC version
- **Solution:** Use `prior_versions_index` to find the exact version you need; compare `crdc_series_uuid` values

### Issue: Some data missing from Google Healthcare DICOMweb
- **Cause:** Google Healthcare only mirrors `idc-open-data` bucket (~96% of data)
- **Solution:** Use IDC public proxy for 100% coverage, or access buckets directly

## Resources

**IDC Documentation:**
- [Files and metadata](https://learn.canceridc.dev/data/organization-of-data/files-and-metadata) - Bucket organization details
- [Data versioning](https://learn.canceridc.dev/data/data-versioning) - Versioning scheme explanation
- [Resolving GUIDs and UUIDs](https://learn.canceridc.dev/data/organization-of-data/guids-and-uuids) - CRDC UUID documentation
- [Direct loading from cloud](https://learn.canceridc.dev/data/downloading-data/direct-loading) - Python examples for cloud access

**AWS Resources:**
- [NCI IDC on AWS Open Data Registry](https://registry.opendata.aws/nci-imaging-data-commons/) - Bucket ARNs and access info
- [s5cmd](https://github.com/peak/s5cmd) - High-performance S3 client (used internally by idc-index)
- [AWS CLI S3 commands](https://docs.aws.amazon.com/cli/latest/reference/s3/) - Standard AWS command-line interface
- [Boto3 S3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) - AWS SDK for Python

**Google Cloud Resources:**
- [gsutil tool](https://cloud.google.com/storage/docs/gsutil) - Google Cloud Storage command-line tool
- [gcloud storage commands](https://cloud.google.com/sdk/gcloud/reference/storage) - Modern GCS CLI (recommended over gsutil)
- [Google Cloud Storage Python client](https://cloud.google.com/python/docs/reference/storage/latest) - GCS SDK for Python

**Related Guides:**
- `dicomweb_guide.md` - DICOMweb API access (alternative to direct bucket access)
- `bigquery_guide.md` - Advanced metadata queries including versioned datasets

---

## Reference: Dicomweb_Guide

# DICOMweb Guide for IDC

IDC provides DICOMweb access through Google Cloud Healthcare API DICOM stores. This guide covers the implementation specifics and usage patterns.

## When to Use DICOMweb

Use DICOMweb when you need:
- Integration with PACS systems or DICOMweb-compatible tools
- Streaming metadata without downloading full files
- Building custom viewers or web applications
- Using existing DICOMweb client libraries (OHIF, dicomweb-client, etc.)

For most use cases, `idc-index` is simpler and recommended. Use DICOMweb when you specifically need the DICOMweb protocol.

## Endpoints

### Public Proxy (No Authentication)

```
https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb
```

- **100% data coverage** - Contains all IDC data from all storage buckets
- Points to the latest IDC version automatically
- **Updates immediately** on new IDC releases
- Per-IP daily quota (suitable for testing and moderate use)
- No authentication required
- Read-only access
- Note: "viewer-only-no-downloads" in URL is legacy naming with no functional meaning

### Google Healthcare API (Requires Authentication)

```
https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v{VERSION}/dicomWeb
```

Replace `{VERSION}` with the IDC release number. To find the current version:

```python
from idc_index import IDCClient
client = IDCClient()
print(client.get_idc_version())  # e.g., "23" for v23
```

- **~96% data coverage** - Only replicates data from `idc-open-data` bucket (missing ~4% from other buckets)
- **Updates 1-2 weeks after** IDC releases
- Requires authentication and provides higher quotas
- Better performance (no proxy routing)
- Each release gets a new versioned store

See [Content Coverage Differences](#content-coverage-differences) and [Authentication](#authentication-for-google-healthcare-api) sections below.

## Content Coverage Differences

**Important:** The two DICOMweb endpoints have different data coverage. The IDC public proxy contains MORE data than the authenticated Google Healthcare endpoint.

### Coverage Summary

| Endpoint | Coverage | Missing Data |
|----------|----------|--------------|
| **IDC Public Proxy** | 100% | None |
| **Google Healthcare API** | ~96% | ~4% (two buckets not replicated) |

### What's Missing from Google Healthcare?

The Google Healthcare DICOM store **only replicates data from the `idc-open-data` S3 bucket**. It does not include data from two additional buckets:

- `idc-open-data-cr`
- `idc-open-data-two`

These missing buckets typically contain several thousand series each, representing approximately 4% of total IDC data. The exact counts vary by IDC version.

See `cloud_storage_guide.md` for details on bucket organization, file structure, and direct access methods.

### Update Timing

- **IDC Public Proxy**: Updates immediately when new IDC versions are released
- **Google Healthcare**: Updates 1-2 weeks after each new IDC version release

Between releases, both endpoints remain current. The 1-2 week delay only occurs during the transition period after a new IDC version is published.

**Warning from IDC documentation:** *"Google-hosted DICOM store may not contain the latest version of IDC data!"* - Check during the weeks following a new release.

### Choosing the Right Endpoint

**Use IDC Public Proxy when:**
- You need complete data coverage (100%)
- You need the absolute latest data immediately after a new version release
- You don't want to set up GCP authentication
- Your usage fits within per-IP quotas (can request increases via support@canceridc.dev)
- You're accessing slide microscopy images frame-by-frame

**Use Google Healthcare API when:**
- The ~4% missing data doesn't affect your use case
- You need higher quotas for heavy usage
- You want better performance (direct access, no proxy routing)

### Checking Your Data Availability

Before choosing an endpoint, verify whether your data might be in the missing buckets:

```python
from idc_index import IDCClient

client = IDCClient()

# Check which buckets contain your collection's data
results = client.sql_query("""
    SELECT series_aws_url, COUNT(*) as series_count
    FROM index
    WHERE collection_id = 'your_collection_id'
    GROUP BY series_aws_url
""")

print(results)

# Look for URLs containing 'idc-open-data-cr' or 'idc-open-data-two'
# If present, that data won't be available in Google Healthcare endpoint
```

## Implementation Details

IDC DICOMweb is provided through Google Cloud Healthcare API DICOM stores. The implementation follows DICOM PS3.18 Web Services with specific characteristics documented in the [Google Healthcare DICOM conformance statement](https://docs.cloud.google.com/healthcare-api/docs/dicom).

### Supported Operations

| Service | Description | Supported |
|---------|-------------|-----------|
| QIDO-RS | Search for DICOM objects | Yes |
| WADO-RS | Retrieve DICOM objects and metadata | Yes |
| STOW-RS | Store DICOM objects | No (IDC is read-only) |

**Not supported:** URI Service, Worklist Service, Non-Patient Instance Service, Capabilities Transactions

### Searchable DICOM Tags (QIDO-RS)

The implementation supports a limited set of searchable tags:

| Level | Searchable Tags |
|-------|-----------------|
| Study | StudyInstanceUID, PatientName, PatientID, AccessionNumber, ReferringPhysicianName, StudyDate |
| Series | All study tags + SeriesInstanceUID, Modality |
| Instance | All series tags + SOPInstanceUID |

**Important:** Only exact matching is supported, except for:
- StudyDate: supports range queries
- PatientName: supports fuzzy matching

### Query Limitations

- Maximum results: 5,000 for studies/series searches; 50,000 for instances
- Maximum offset: 1,000,000
- DICOM sequence tags larger than ~1 MB are not returned in metadata (BulkDataURI provided instead)

## Code Examples

All examples use the public proxy endpoint. For authenticated access to Google Healthcare, see the [authentication section](#authentication-for-google-healthcare-api).

### Finding UIDs with idc-index

Use `idc-index` to discover data, then use DICOMweb for metadata access:

```python
from idc_index import IDCClient

client = IDCClient()

# Find studies of interest
results = client.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, PatientID, Modality
    FROM index
    WHERE collection_id = 'tcga_luad' AND Modality = 'CT'
    LIMIT 5
""")

# Use these UIDs with DICOMweb
study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Study: {study_uid}")
print(f"Series: {series_uid}")
```

### QIDO-RS: Search by UID

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

# Search for a specific study
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
response = requests.get(
    f"{base_url}/studies",
    params={"StudyInstanceUID": study_uid},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    studies = response.json()
    print(f"Found {len(studies)} study")
```

### QIDO-RS: List Series in a Study

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    series_list = response.json()
    for series in series_list:
        # DICOM tags are returned as hex codes
        series_uid = series.get("0020000E", {}).get("Value", [None])[0]
        modality = series.get("00080060", {}).get("Value", [None])[0]
        description = series.get("0008103E", {}).get("Value", [""])[0]
        print(f"{modality}: {description}")
```

### QIDO-RS: List Instances in a Series

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/instances",
    params={"limit": 10},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Found {len(instances)} instances")
    for inst in instances[:3]:
        sop_uid = inst.get("00080018", {}).get("Value", [None])[0]
        print(f"  SOPInstanceUID: {sop_uid}")
```

### WADO-RS: Retrieve Series Metadata

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Retrieved metadata for {len(instances)} instances")

    # Extract image dimensions from first instance
    if instances:
        inst = instances[0]
        rows = inst.get("00280010", {}).get("Value", [None])[0]
        cols = inst.get("00280011", {}).get("Value", [None])[0]
        print(f"Image dimensions: {rows} x {cols}")
```

### Combined Workflow: idc-index Discovery + DICOMweb Metadata

```python
from idc_index import IDCClient
import requests

# Use idc-index for efficient discovery
idc = IDCClient()
results = idc.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, Modality, SeriesDescription
    FROM index
    WHERE collection_id = 'nlst' AND Modality = 'CT'
    LIMIT 1
""")

study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Found: {results.iloc[0]['SeriesDescription']}")

# Use DICOMweb to stream metadata without downloading files
base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    metadata = response.json()
    print(f"Retrieved metadata for {len(metadata)} instances without downloading files")
```

## Common DICOM Tags Reference

DICOMweb returns tags as hexadecimal codes. Common tags:

| Tag | Name | Description |
|-----|------|-------------|
| 00080018 | SOPInstanceUID | Unique instance identifier |
| 00080020 | StudyDate | Date study was performed |
| 00080060 | Modality | Imaging modality (CT, MR, PT, etc.) |
| 0008103E | SeriesDescription | Description of series |
| 00100020 | PatientID | Patient identifier |
| 0020000D | StudyInstanceUID | Unique study identifier |
| 0020000E | SeriesInstanceUID | Unique series identifier |
| 00280010 | Rows | Image height in pixels |
| 00280011 | Columns | Image width in pixels |

## Authentication for Google Healthcare API

To use the Google Healthcare endpoint with higher quotas:

```python
from google.auth import default
from google.auth.transport.requests import Request
import requests

# Get credentials (requires gcloud auth)
credentials, project = default()
credentials.refresh(Request())

# Build authenticated request
base_url = "https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v23/dicomWeb"

response = requests.get(
    f"{base_url}/studies",
    params={"limit": 5},
    headers={
        "Authorization": f"Bearer {credentials.token}",
        "Accept": "application/dicom+json"
    }
)
```

**Prerequisites:**
1. Google Cloud SDK installed (`gcloud`)
2. Authenticated: `gcloud auth application-default login`
3. Account has access to public Google Cloud datasets

## Troubleshooting

### Issue: 400 Bad Request on search queries
- **Cause:** Using unsupported search parameters. The implementation only supports specific DICOM tags for filtering.
- **Solution:** Use UID-based queries (StudyInstanceUID, SeriesInstanceUID). For filtering by Modality or other attributes, use `idc-index` to discover UIDs first, then query DICOMweb with specific UIDs.

### Issue: 403 Forbidden on Google Healthcare endpoint
- **Cause:** Missing authentication or insufficient permissions
- **Solution:** Run `gcloud auth application-default login` and ensure your account has access

### Issue: 429 Too Many Requests
- **Cause:** Rate limit exceeded
- **Solution:** Add delays between requests, reduce `limit` values, or use authenticated endpoint for higher quotas

### Issue: 204 No Content for valid UIDs
- **Cause:** UID may be from an older IDC version not in current data, or data is in buckets not replicated by Google Healthcare
- **Solution:**
  - Verify UID exists using `idc-index` query first
  - Check if data is in `idc-open-data-cr` or `idc-open-data-two` buckets (not available in Google Healthcare endpoint)
  - Switch to IDC public proxy for 100% coverage
  - During new version releases, Google Healthcare may lag 1-2 weeks behind

### Issue: Large metadata responses slow to parse
- **Cause:** Series with many instances returns large JSON
- **Solution:** Use `limit` parameter on instance queries, or query specific instances by SOPInstanceUID

### Issue: Response missing expected attributes
- **Cause:** DICOM sequences larger than ~1 MB are excluded from metadata responses
- **Solution:** Retrieve the full DICOM instance using WADO-RS instance retrieval if you need all attributes

## Resources

**IDC Documentation:**
- [IDC DICOM Stores](https://learn.canceridc.dev/data/organization-of-data/dicom-stores) - Data coverage and bucket details
- [IDC DICOMweb Access](https://learn.canceridc.dev/data/downloading-data/dicomweb-access) - Endpoint usage and differences
- [IDC Proxy Policy](https://learn.canceridc.dev/portal/proxy-policy) - Quota policies and usage restrictions
- [IDC User Guide](https://learn.canceridc.dev/) - Complete documentation

**DICOMweb Standards and Tools:**
- [Google Healthcare DICOM Conformance Statement](https://docs.cloud.google.com/healthcare-api/docs/dicom)
- [DICOMweb Standard](https://www.dicomstandard.org/using/dicomweb)
- [dicomweb-client Python library](https://dicomweb-client.readthedocs.io/)

**Related Guides:**
- `cloud_storage_guide.md` - Direct bucket access, file organization, CRDC UUIDs, and versioning
- `bigquery_guide.md` - Advanced metadata queries with full DICOM attributes

---

## Reference: Digital_Pathology_Guide

# Digital Pathology Guide for IDC

**Tested with:** IDC data version v23, idc-index 0.11.10

For general IDC queries and downloads, use `idc-index` (see main SKILL.md). This guide covers slide microscopy (SM) imaging, microscopy bulk simple annotations (ANN), and segmentations (SEG) in the context of digital pathology in IDC.

## Index Tables for Digital Pathology

Five specialized index tables provide curated metadata without needing BigQuery:

| Table | Row Granularity | Description |
|-------|-----------------|-------------|
| `sm_index` | 1 row = 1 SM series | Slide Microscopy series metadata: container/slide ID, tissue type, anatomic structure, diagnosis, lens power, pixel spacing, image dimensions |
| `sm_instance_index` | 1 row = 1 SM instance | Instance-level (SOPInstanceUID) metadata for individual slide images |
| `seg_index` | 1 row = 1 SEG series | DICOM Segmentation metadata: algorithm, segment count, reference to source series. Used for both radiology and pathology — filter by source Modality to find pathology-specific segmentations |
| `ann_index` | 1 row = 1 ANN series | Microscopy Bulk Simple Annotations series metadata; includes `referenced_SeriesInstanceUID` linking to the annotated slide |
| `ann_group_index` | 1 row = 1 annotation group | Annotation group details: `AnnotationGroupLabel`, `GraphicType`, `NumberOfAnnotations`, `AlgorithmName`, property codes |

All require `client.fetch_index("table_name")` before querying. Use `client.indices_overview` to inspect column schemas programmatically.

## Slide Microscopy Queries

### Basic SM metadata

```python
from idc_index import IDCClient
client = IDCClient()

# sm_index has detailed metadata; join with index for collection_id
client.fetch_index("sm_index")
client.sql_query("""
    SELECT i.collection_id, COUNT(*) as slides,
           MIN(s.min_PixelSpacing_2sf) as min_resolution
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    GROUP BY i.collection_id
    ORDER BY slides DESC
""")
```

### Find SM series with specific properties

```python
# Find high-resolution slides with specific objective lens power
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        i.collection_id,
        i.PatientID,
        s.ObjectiveLensPower,
        s.min_PixelSpacing_2sf
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE s.ObjectiveLensPower >= 40
    ORDER BY s.min_PixelSpacing_2sf
    LIMIT 20
""")
```

### Filter by specimen preparation

The `sm_index` includes staining, embedding, and fixative metadata. These columns are **arrays** (e.g., `[hematoxylin stain, water soluble eosin stain]` for H&E) — use `array_to_string()` with `LIKE` or `list_contains()` to filter.

```python
# Find H&E-stained slides in a collection
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        i.PatientID,
        s.staining_usingSubstance_CodeMeaning as staining,
        s.embeddingMedium_CodeMeaning as embedding,
        s.tissueFixative_CodeMeaning as fixative
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
      AND array_to_string(s.staining_usingSubstance_CodeMeaning, ', ') LIKE '%hematoxylin%'
    LIMIT 10
""")
```

```python
# Compare FFPE vs frozen slides across collections
client.sql_query("""
    SELECT
        i.collection_id,
        s.embeddingMedium_CodeMeaning as embedding,
        COUNT(*) as slide_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    GROUP BY i.collection_id, embedding
    ORDER BY i.collection_id, slide_count DESC
""")
```

## Identifying Tumor vs Normal Slides

The `sm_index` table provides two ways to identify tissue type:

| Column | Use Case |
|--------|----------|
| `primaryAnatomicStructureModifier_CodeMeaning` | Structured tissue type from DICOM specimen metadata (e.g., `Neoplasm, Primary`, `Normal`, `Tumor`, `Neoplasm, Metastatic`). Works across all collections with SM data. |
| `ContainerIdentifier` | Slide/container identifier. For TCGA collections, contains the [TCGA barcode](https://docs.gdc.cancer.gov/Encyclopedia/pages/TCGA_Barcode/) where the [sample type code](https://gdc.cancer.gov/resources-tcga-users/tcga-code-tables/sample-type-codes) (positions 14-15) encodes tissue origin: `01`-`09` = tumor, `10`-`19` = normal. |

### Using structured tissue type metadata

```python
from idc_index import IDCClient
client = IDCClient()
client.fetch_index("sm_index")

# Discover tissue type values across all SM data
client.sql_query("""
    SELECT
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count
    FROM sm_index s
    WHERE s.primaryAnatomicStructureModifier_CodeMeaning IS NOT NULL
    GROUP BY tissue_type
    ORDER BY slide_count DESC
""")
```

#### Example: Tumor vs normal slides in TCGA-BRCA

```python
# Tissue type breakdown for TCGA-BRCA
client.sql_query("""
    SELECT
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count,
        COUNT(DISTINCT i.PatientID) as patient_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    GROUP BY tissue_type
    ORDER BY slide_count DESC
""")
# Returns: Neoplasm, Primary (2704 slides), Normal (399 slides)
```

### Using TCGA barcode (TCGA collections only)

For TCGA collections, `ContainerIdentifier` contains the slide barcode (e.g., `TCGA-E9-A3X8-01A-03-TSC`). Extract the sample type code to classify tissue:

```python
# Parse sample type from TCGA barcode
client.sql_query("""
    SELECT
        SUBSTRING(SPLIT_PART(s.ContainerIdentifier, '-', 4), 1, 2) as sample_type_code,
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    GROUP BY sample_type_code, tissue_type
    ORDER BY sample_type_code
""")
# Returns: 01 → Neoplasm, Primary (2704), 06 → None (8), 11 → Normal (399)
```

The barcode approach catches cases where structured metadata is NULL (e.g., `06` = Metastatic slides have `primaryAnatomicStructureModifier_CodeMeaning` = NULL in TCGA-BRCA).

## Annotation Queries (ANN)

DICOM Microscopy Bulk Simple Annotations (Modality = 'ANN') are annotations **on** slide microscopy images. They appear in `ann_index` (series-level) and `ann_group_index` (group-level detail). Each ANN series references the slide it annotates via `referenced_SeriesInstanceUID`.

### Basic annotation discovery

```python
# Find annotation series and their referenced images
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")

client.sql_query("""
    SELECT
        a.SeriesInstanceUID as ann_series,
        a.AnnotationCoordinateType,
        a.referenced_SeriesInstanceUID as source_series
    FROM ann_index a
    LIMIT 10
""")
```

### Annotation group statistics

```python
# Get annotation group details (graphic types, counts, algorithms)
client.sql_query("""
    SELECT
        GraphicType,
        SUM(NumberOfAnnotations) as total_annotations,
        COUNT(*) as group_count
    FROM ann_group_index
    GROUP BY GraphicType
    ORDER BY total_annotations DESC
""")
```

### Find annotations with source slide context

```python
# Find annotations with their source slide microscopy context
client.sql_query("""
    SELECT
        i.collection_id,
        g.GraphicType,
        g.AnnotationPropertyType_CodeMeaning,
        g.AlgorithmName,
        g.NumberOfAnnotations
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.referenced_SeriesInstanceUID = i.SeriesInstanceUID
    WHERE g.AlgorithmName IS NOT NULL
    LIMIT 10
""")
```

## Segmentations on Slide Microscopy

DICOM Segmentations (Modality = 'SEG') are used for both radiology (e.g., organ segmentations on CT) and pathology (e.g., tissue region segmentations on whole slide images). Use `seg_index.segmented_SeriesInstanceUID` to find the source series, then filter by source Modality to isolate pathology segmentations.

```python
# Find segmentations whose source is a slide microscopy image
client.fetch_index("seg_index")
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        seg.SeriesInstanceUID as seg_series,
        seg.AlgorithmName,
        seg.total_segments,
        src.collection_id,
        src.Modality as source_modality
    FROM seg_index seg
    JOIN index src ON seg.segmented_SeriesInstanceUID = src.SeriesInstanceUID
    WHERE src.Modality = 'SM'
    LIMIT 20
""")
```

## Finding Pre-Computed Analysis Results

IDC hosts derived datasets (nuclei segmentations, TIL maps, AI annotations) identified by `analysis_result_id` in the main `index` table. Use `analysis_results_index` to discover what's available for pathology.

```python
from idc_index import IDCClient
client = IDCClient()
client.fetch_index("analysis_results_index")

# Find analysis results that include pathology annotations or segmentations
client.sql_query("""
    SELECT
        ar.analysis_result_id,
        ar.analysis_result_title,
        ar.Modalities,
        ar.Subjects,
        ar.Collections
    FROM analysis_results_index ar
    WHERE ar.Modalities LIKE '%ANN%' OR ar.Modalities LIKE '%SEG%'
    ORDER BY ar.Subjects DESC
""")
```

### Find analysis results for a specific slide

```python
# Find all derived data (annotations, segmentations) for TCGA-BRCA slides
client.fetch_index("ann_index")
client.sql_query("""
    SELECT
        i.analysis_result_id,
        i.PatientID,
        a.referenced_SeriesInstanceUID as source_slide,
        g.AnnotationGroupLabel,
        g.NumberOfAnnotations,
        g.AlgorithmName
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    LIMIT 10
""")
```

Annotation objects can also contain per-annotation **measurements** (e.g., nucleus area, eccentricity) stored within the DICOM file. These are not in the index tables — extract them after download using [highdicom](https://github.com/ImagingDataCommons/highdicom) (`ann.get_annotation_groups()`, `group.get_measurements()`). See the [microscopy_dicom_ann_intro](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/pathomics/microscopy_dicom_ann_intro.ipynb) tutorial for a worked example including spatial analysis and cellularity computation.

## Filter by AnnotationGroupLabel

`AnnotationGroupLabel` is the most direct column for finding annotation groups by name or semantic content. Use `LIKE` with wildcards for text search.

### Simple label filtering

```python
# Find annotation groups by label (e.g., groups mentioning "blast")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        g.SeriesInstanceUID,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        g.AlgorithmName
    FROM ann_group_index g
    WHERE LOWER(g.AnnotationGroupLabel) LIKE '%blast%'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

### Label filtering with collection context

```python
# Find annotation groups matching a label within a specific collection
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        i.collection_id,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        g.AnnotationPropertyType_CodeMeaning
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
      AND LOWER(g.AnnotationGroupLabel) LIKE '%keyword%'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

## Annotations on Slide Microscopy (SM + ANN Cross-Reference)

When looking for annotations related to slide microscopy data, use both SM and ANN tables together. The `ann_index.referenced_SeriesInstanceUID` links each annotation series to its source slide.

```python
# Find slide microscopy images and their annotations in a collection
client.fetch_index("sm_index")
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        i.collection_id,
        s.ObjectiveLensPower,
        g.AnnotationGroupLabel,
        g.NumberOfAnnotations,
        g.GraphicType
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN sm_index s ON a.referenced_SeriesInstanceUID = s.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

## Join Patterns

### SM join (slide microscopy details with collection context)

```python
client.fetch_index("sm_index")
result = client.sql_query("""
    SELECT i.collection_id, i.PatientID, s.ObjectiveLensPower, s.min_PixelSpacing_2sf
    FROM index i
    JOIN sm_index s ON i.SeriesInstanceUID = s.SeriesInstanceUID
    LIMIT 10
""")
```

### ANN join (annotation groups with collection context)

```python
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
result = client.sql_query("""
    SELECT
        i.collection_id,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        a.referenced_SeriesInstanceUID as source_series
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    LIMIT 10
""")
```

## Related Tools

The following tools work with DICOM format for digital pathology workflows:

**Python Libraries:**
- [highdicom](https://github.com/ImagingDataCommons/highdicom) - High-level DICOM abstractions for Python. Create and read DICOM Segmentations (SEG), Structured Reports (SR), and parametric maps for pathology and radiology. Developed by IDC.
- [wsidicom](https://github.com/imi-bigpicture/wsidicom) - Python package for reading DICOM WSI datasets. Parses metadata into easy-to-use dataclasses for whole slide image analysis.
- [TIA-Toolbox](https://github.com/TissueImageAnalytics/tiatoolbox) - End-to-end computational pathology library with DICOM support via `DICOMWSIReader`. Provides tile extraction, feature extraction, and pretrained deep learning models.
- [EZ-WSI-DICOMweb](https://github.com/GoogleCloudPlatform/EZ-WSI-DICOMweb) - Extract image patches from DICOM whole slide images via DICOMweb. Designed for AI/ML workflows with cloud DICOM stores.

**Viewers:**
- [Slim](https://github.com/ImagingDataCommons/slim) - Web-based DICOM slide microscopy viewer and annotation tool. Supports brightfield and multiplexed immunofluorescence imaging via DICOMweb. Developed by IDC.
- [QuPath](https://qupath.github.io/) - Cross-platform open source software for whole slide image analysis. Supports DICOM WSI via Bio-Formats and OpenSlide (v0.4.0+).

**Conversion:**
- [dicom_wsi](https://github.com/Steven-N-Hart/dicom_wsi) - Python implementation for converting proprietary WSI formats to DICOM-compliant files.

---

## Reference: Index_Tables_Guide

# Index Tables Guide for IDC

**Tested with:** idc-index 0.11.9 (IDC data version v23)

This guide covers the structure and access patterns for IDC index tables: programmatic schema discovery, DataFrame access, and join column references. For the overview of available tables and their purposes, see the "Index Tables" section in the main SKILL.md.

**Complete index table documentation:** https://idc-index.readthedocs.io/en/latest/indices_reference.html

## When to Use This Guide

Load this guide when you need to:
- Discover table schemas and column types programmatically
- Access index tables as pandas DataFrames (not via SQL)
- Understand key columns and join relationships between tables

For SQL query examples (filter discovery, finding annotations, size estimation), see `references/sql_patterns.md`.

## Prerequisites

```bash
pip install --upgrade idc-index
```

## Accessing Index Tables

### Via SQL (recommended for filtering/aggregation)

```python
from idc_index import IDCClient
client = IDCClient()

# Query the primary index (always available)
results = client.sql_query("SELECT * FROM index WHERE Modality = 'CT' LIMIT 10")

# Fetch and query additional indices
client.fetch_index("collections_index")
collections = client.sql_query("SELECT collection_id, CancerTypes, TumorLocations FROM collections_index")

client.fetch_index("analysis_results_index")
analysis = client.sql_query("SELECT * FROM analysis_results_index LIMIT 5")
```

### As pandas DataFrames (direct access)

```python
# Primary index (always available after client initialization)
df = client.index

# Fetch and access on-demand indices
client.fetch_index("sm_index")
sm_df = client.sm_index
```

## Discovering Table Schemas

The `indices_overview` dictionary contains complete schema information for all tables. **Always consult this when writing queries or exploring data structure.**

**DICOM attribute mapping:** Many columns are populated directly from DICOM attributes in the source files. The column description in the schema indicates when a column corresponds to a DICOM attribute (e.g., "DICOM Modality attribute" or references a DICOM tag). This allows leveraging DICOM knowledge when querying — standard DICOM attribute names like `PatientID`, `StudyInstanceUID`, `Modality`, `BodyPartExamined` work as expected.

```python
from idc_index import IDCClient
client = IDCClient()

# List all available indices with descriptions
for name, info in client.indices_overview.items():
    print(f"\n{name}:")
    print(f"  Installed: {info['installed']}")
    print(f"  Description: {info['description']}")

# Get complete schema for a specific index (columns, types, descriptions)
schema = client.indices_overview["index"]["schema"]
print(f"\nTable: {schema['table_description']}")
print("\nColumns:")
for col in schema['columns']:
    desc = col.get('description', 'No description')
    # Description indicates if column is from DICOM attribute
    print(f"  {col['name']} ({col['type']}): {desc}")

# Find columns that are DICOM attributes (check description for "DICOM" reference)
dicom_cols = [c['name'] for c in schema['columns'] if 'DICOM' in c.get('description', '').upper()]
print(f"\nDICOM-sourced columns: {dicom_cols}")
```

**Alternative: use `get_index_schema()` method:**
```python
schema = client.get_index_schema("index")
# Returns same schema dict: {'table_description': ..., 'columns': [...]}
```

## Key Columns Reference

Most common columns in the primary `index` table (use `indices_overview` for complete list and descriptions):

| Column | Type | DICOM | Description |
|--------|------|-------|-------------|
| `collection_id` | STRING | No | IDC collection identifier |
| `analysis_result_id` | STRING | No | If applicable, indicates what analysis results collection given series is part of |
| `source_DOI` | STRING | No | DOI linking to dataset details; use for learning more about the content and for attribution (see citations below) |
| `PatientID` | STRING | Yes | Patient identifier |
| `StudyInstanceUID` | STRING | Yes | DICOM Study UID |
| `SeriesInstanceUID` | STRING | Yes | DICOM Series UID — use for downloads/viewing |
| `Modality` | STRING | Yes | Imaging modality (CT, MR, PT, SM, SEG, ANN, RTSTRUCT, etc.) |
| `BodyPartExamined` | STRING | Yes | Anatomical region |
| `SeriesDescription` | STRING | Yes | Description of the series |
| `Manufacturer` | STRING | Yes | Equipment manufacturer |
| `StudyDate` | STRING | Yes | Date study was performed |
| `PatientSex` | STRING | Yes | Patient sex |
| `PatientAge` | STRING | Yes | Patient age at time of study |
| `license_short_name` | STRING | No | License type (CC BY 4.0, CC BY-NC 4.0, etc.) |
| `series_size_MB` | FLOAT | No | Size of series in megabytes |
| `instanceCount` | INTEGER | No | Number of DICOM instances in series |

**DICOM = Yes**: Column value extracted from the DICOM attribute with the same name. Refer to the [DICOM standard](https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html) for numeric tag mappings. Use standard DICOM knowledge for expected values and formats.

## Join Column Reference

Use this table to identify join columns between index tables. Always call `client.fetch_index("table_name")` before using a table in SQL.

| Table A | Table B | Join Condition |
|---------|---------|----------------|
| `index` | `collections_index` | `index.collection_id = collections_index.collection_id` |
| `index` | `sm_index` | `index.SeriesInstanceUID = sm_index.SeriesInstanceUID` |
| `index` | `seg_index` | `index.SeriesInstanceUID = seg_index.segmented_SeriesInstanceUID` |
| `index` | `ann_index` | `index.SeriesInstanceUID = ann_index.SeriesInstanceUID` |
| `ann_index` | `ann_group_index` | `ann_index.SeriesInstanceUID = ann_group_index.SeriesInstanceUID` |
| `index` | `clinical_index` | `index.collection_id = clinical_index.collection_id` (then filter by patient) |
| `index` | `contrast_index` | `index.SeriesInstanceUID = contrast_index.SeriesInstanceUID` |

For complete query examples using these joins, see `references/sql_patterns.md`.

## Troubleshooting

**Issue:** Column not found in table
- **Cause:** Column name misspelled or doesn't exist in that table
- **Solution:** Use `client.indices_overview["table_name"]["schema"]["columns"]` to list available columns

**Issue:** DataFrame access returns None
- **Cause:** Index not fetched or property name incorrect
- **Solution:** Fetch first with `client.fetch_index()`, then access via property matching the index name

## Resources

- Complete index table documentation: https://idc-index.readthedocs.io/en/latest/indices_reference.html
- `references/sql_patterns.md` for query examples using these tables
- `references/clinical_data_guide.md` for clinical data workflows
- `references/digital_pathology_guide.md` for pathology-specific indices

---

## Reference: Sql_Patterns

# SQL Query Patterns for IDC

**Tested with:** idc-index 0.11.9 (IDC data version v23)

Quick reference for common SQL query patterns when working with IDC data. For detailed examples with context, see the "Core Capabilities" section in the main SKILL.md.

## When to Use This Guide

Load this guide when you need quick-reference SQL patterns for:
- Discovering available filter values (modalities, body parts, manufacturers)
- Finding annotations and segmentations across collections
- Querying slide microscopy and annotation data
- Estimating download sizes before download
- Linking imaging data to clinical data

For table schemas, DataFrame access, and join column references, see `references/index_tables_guide.md`.

## Prerequisites

```bash
pip install --upgrade idc-index
```

```python
from idc_index import IDCClient
client = IDCClient()
```

## Discover Available Filter Values

```python
# What modalities exist?
client.sql_query("SELECT DISTINCT Modality FROM index")

# What body parts for a specific modality?
client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as n
    FROM index WHERE Modality = 'CT' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined ORDER BY n DESC
""")

# What manufacturers for MR?
client.sql_query("""
    SELECT DISTINCT Manufacturer, COUNT(*) as n
    FROM index WHERE Modality = 'MR'
    GROUP BY Manufacturer ORDER BY n DESC
""")
```

## Find Annotations and Segmentations

**Note:** Not all image-derived objects belong to analysis result collections. Some annotations are deposited alongside original images. Use DICOM Modality or SOPClassUID to find all derived objects regardless of collection type.

```python
# Find ALL segmentations and structure sets by DICOM Modality
# SEG = DICOM Segmentation, RTSTRUCT = Radiotherapy Structure Set
client.sql_query("""
    SELECT collection_id, Modality, COUNT(*) as series_count
    FROM index
    WHERE Modality IN ('SEG', 'RTSTRUCT')
    GROUP BY collection_id, Modality
    ORDER BY series_count DESC
""")

# Find segmentations for a specific collection (includes non-analysis-result items)
client.sql_query("""
    SELECT SeriesInstanceUID, SeriesDescription, analysis_result_id
    FROM index
    WHERE collection_id = 'tcga_luad' AND Modality = 'SEG'
""")

# List analysis result collections (curated derived datasets)
client.fetch_index("analysis_results_index")
client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Collections, Modalities
    FROM analysis_results_index
""")

# Find analysis results for a specific source collection
client.sql_query("""
    SELECT analysis_result_id, analysis_result_title
    FROM analysis_results_index
    WHERE Collections LIKE '%tcga_luad%'
""")

# Use seg_index for detailed DICOM Segmentation metadata
client.fetch_index("seg_index")

# Get segmentation statistics by algorithm
client.sql_query("""
    SELECT AlgorithmName, AlgorithmType, COUNT(*) as seg_count
    FROM seg_index
    WHERE AlgorithmName IS NOT NULL
    GROUP BY AlgorithmName, AlgorithmType
    ORDER BY seg_count DESC
    LIMIT 10
""")

# Find segmentations for specific source images (e.g., chest CT)
client.sql_query("""
    SELECT
        s.SeriesInstanceUID as seg_series,
        s.AlgorithmName,
        s.total_segments,
        s.segmented_SeriesInstanceUID as source_series
    FROM seg_index s
    JOIN index src ON s.segmented_SeriesInstanceUID = src.SeriesInstanceUID
    WHERE src.Modality = 'CT' AND src.BodyPartExamined = 'CHEST'
    LIMIT 10
""")

# Find TotalSegmentator results with source image context
client.sql_query("""
    SELECT
        seg_info.collection_id,
        COUNT(DISTINCT s.SeriesInstanceUID) as seg_count,
        SUM(s.total_segments) as total_segments
    FROM seg_index s
    JOIN index seg_info ON s.SeriesInstanceUID = seg_info.SeriesInstanceUID
    WHERE s.AlgorithmName LIKE '%TotalSegmentator%'
    GROUP BY seg_info.collection_id
    ORDER BY seg_count DESC
""")

# Use ann_index and ann_group_index for Microscopy Bulk Simple Annotations
# ann_group_index has AnnotationGroupLabel, GraphicType, NumberOfAnnotations, AlgorithmName
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT g.AnnotationGroupLabel, g.GraphicType, g.NumberOfAnnotations, i.collection_id
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE g.AlgorithmName IS NOT NULL
    LIMIT 10
""")
# See references/digital_pathology_guide.md for AnnotationGroupLabel filtering, SM+ANN joins, and more
```

## Query Slide Microscopy and Annotation Data

Use `sm_index` for slide microscopy metadata and `ann_index`/`ann_group_index` for annotations on slides (DICOM ANN objects). Filter annotation groups by `AnnotationGroupLabel` to find annotations by name.

```python
client.fetch_index("sm_index")
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")

# Example: find annotation groups by label within a collection
client.sql_query("""
    SELECT g.AnnotationGroupLabel, g.GraphicType, g.NumberOfAnnotations
    FROM ann_group_index g
    JOIN index i ON g.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
      AND LOWER(g.AnnotationGroupLabel) LIKE '%keyword%'
""")
```

See `references/digital_pathology_guide.md` for SM queries, ANN filtering patterns, SM+ANN cross-references, and join examples.

## Estimate Download Size

```python
# Size for specific criteria
client.sql_query("""
    SELECT SUM(series_size_MB) as total_mb, COUNT(*) as series_count
    FROM index
    WHERE collection_id = 'nlst' AND Modality = 'CT'
""")
```

## Link to Clinical Data

```python
client.fetch_index("clinical_index")

# Find collections with clinical data and their tables
client.sql_query("""
    SELECT collection_id, table_name, COUNT(DISTINCT column_label) as columns
    FROM clinical_index
    GROUP BY collection_id, table_name
    ORDER BY collection_id
""")
```

See `references/clinical_data_guide.md` for complete patterns including value mapping and patient cohort selection.

## Troubleshooting

**Issue:** Query returns error "table not found"
- **Cause:** Index not fetched before query
- **Solution:** Call `client.fetch_index("table_name")` before using tables other than the primary `index`

**Issue:** LIKE pattern not matching expected results
- **Cause:** Case sensitivity or whitespace
- **Solution:** Use `LOWER(column)` for case-insensitive matching, `TRIM()` for whitespace

**Issue:** JOIN returns fewer rows than expected
- **Cause:** NULL values in join columns or no matching records
- **Solution:** Use `LEFT JOIN` to include rows without matches, check for NULLs with `IS NOT NULL`

## Resources

- `references/index_tables_guide.md` for table schemas, DataFrame access, and join column references
- `references/clinical_data_guide.md` for clinical data patterns and value mapping
- `references/digital_pathology_guide.md` for pathology-specific queries
- `references/bigquery_guide.md` for advanced queries requiring full DICOM metadata

---

## Reference: Use_Cases

# Common Use Cases for IDC

**Tested with:** idc-index 0.11.9 (IDC data version v23)

This guide provides complete end-to-end workflow examples for common IDC use cases. Each use case demonstrates the full workflow from query to download with best practices.

## When to Use This Guide

Load this guide when you need:
- Complete end-to-end workflow examples for training dataset creation
- Patterns for multi-step data selection and download workflows
- Examples of license-aware data handling for commercial use
- Visualization workflows for data preview before download

For core API patterns (query, download, visualize, citations), see the "Core Capabilities" section in the main SKILL.md.

## Prerequisites

```bash
pip install --upgrade idc-index
```

## Use Case 1: Find and Download Lung CT Scans for Deep Learning

**Objective:** Build training dataset of lung CT scans from NLST collection

**Steps:**
```python
from idc_index import IDCClient

client = IDCClient()

# 1. Query for lung CT scans with specific criteria
query = """
SELECT
  PatientID,
  SeriesInstanceUID,
  SeriesDescription
FROM index
WHERE collection_id = 'nlst'
  AND Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND license_short_name = 'CC BY 4.0'
ORDER BY PatientID
LIMIT 100
"""

results = client.sql_query(query)
print(f"Found {len(results)} series from {results['PatientID'].nunique()} patients")

# 2. Download data organized by patient
client.download_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values),
    downloadDir="./training_data",
    dirTemplate="%collection_id/%PatientID/%SeriesInstanceUID"
)

# 3. Save manifest for reproducibility
results.to_csv('training_manifest.csv', index=False)
```

## Use Case 2: Query Brain MRI by Manufacturer for Quality Study

**Objective:** Compare image quality across different MRI scanner manufacturers

**Steps:**
```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()

# Query for brain MRI grouped by manufacturer
query = """
SELECT
  Manufacturer,
  ManufacturerModelName,
  COUNT(DISTINCT SeriesInstanceUID) as num_series,
  COUNT(DISTINCT PatientID) as num_patients
FROM index
WHERE Modality = 'MR'
  AND BodyPartExamined LIKE '%BRAIN%'
GROUP BY Manufacturer, ManufacturerModelName
HAVING num_series >= 10
ORDER BY num_series DESC
"""

manufacturers = client.sql_query(query)
print(manufacturers)

# Download sample from each manufacturer for comparison
for _, row in manufacturers.head(3).iterrows():
    mfr = row['Manufacturer']
    model = row['ManufacturerModelName']

    query = f"""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Manufacturer = '{mfr}'
      AND ManufacturerModelName = '{model}'
      AND Modality = 'MR'
      AND BodyPartExamined LIKE '%BRAIN%'
    LIMIT 5
    """

    series = client.sql_query(query)
    client.download_from_selection(
        seriesInstanceUID=list(series['SeriesInstanceUID'].values),
        downloadDir=f"./quality_study/{mfr.replace(' ', '_')}"
    )
```

## Use Case 3: Visualize Series Without Downloading

**Objective:** Preview imaging data before committing to download

```python
from idc_index import IDCClient
import webbrowser

client = IDCClient()

series_list = client.sql_query("""
    SELECT SeriesInstanceUID, PatientID, SeriesDescription
    FROM index
    WHERE collection_id = 'acrin_nsclc_fdg_pet' AND Modality = 'PT'
    LIMIT 10
""")

# Preview each in browser
for _, row in series_list.iterrows():
    viewer_url = client.get_viewer_URL(seriesInstanceUID=row['SeriesInstanceUID'])
    print(f"Patient {row['PatientID']}: {row['SeriesDescription']}")
    print(f"  View at: {viewer_url}")
    # webbrowser.open(viewer_url)  # Uncomment to open automatically
```

For additional visualization options, see the [IDC Portal getting started guide](https://learn.canceridc.dev/portal/getting-started) or [SlicerIDCBrowser](https://github.com/ImagingDataCommons/SlicerIDCBrowser) for 3D Slicer integration.

## Use Case 4: License-Aware Batch Download for Commercial Use

**Objective:** Download only CC-BY licensed data suitable for commercial applications

**Steps:**
```python
from idc_index import IDCClient

client = IDCClient()

# Query ONLY for CC BY licensed data (allows commercial use with attribution)
query = """
SELECT
  SeriesInstanceUID,
  collection_id,
  PatientID,
  Modality
FROM index
WHERE license_short_name LIKE 'CC BY%'
  AND license_short_name NOT LIKE '%NC%'
  AND Modality IN ('CT', 'MR')
  AND BodyPartExamined IN ('CHEST', 'BRAIN', 'ABDOMEN')
LIMIT 200
"""

cc_by_data = client.sql_query(query)

print(f"Found {len(cc_by_data)} CC BY licensed series")
print(f"Collections: {cc_by_data['collection_id'].unique()}")

# Download with license verification
client.download_from_selection(
    seriesInstanceUID=list(cc_by_data['SeriesInstanceUID'].values),
    downloadDir="./commercial_dataset",
    dirTemplate="%collection_id/%Modality/%PatientID/%SeriesInstanceUID"
)

# Save license information
cc_by_data.to_csv('commercial_dataset_manifest_CC-BY_ONLY.csv', index=False)
```

## Resources

- Main SKILL.md for core API patterns (query, download, visualize)
- `references/clinical_data_guide.md` for clinical data integration workflows
- `references/sql_patterns.md` for additional SQL query patterns
- `references/index_tables_guide.md` for complex join patterns
