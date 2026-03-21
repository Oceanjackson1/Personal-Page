---
title: "Matchms"
description: "Spectral similarity and compound identification for metabolomics. Use for comparing mass spectra, computing similarity scores (cosine, modified cosine), and identifying unknown compounds from spectral libraries. Best for metabolite identification,..."
category: "research"
source: "community"
author: "Community"
tags: ["matchms"]
date: 2026-03-20
---

# Matchms

## Overview

Matchms is an open-source Python library for mass spectrometry data processing and analysis. Import spectra from various formats, standardize metadata, filter peaks, calculate spectral similarities, and build reproducible analytical workflows.

## Core Capabilities

### 1. Importing and Exporting Mass Spectrometry Data

Load spectra from multiple file formats and export processed data:

```python
from matchms.importing import load_from_mgf, load_from_mzml, load_from_msp, load_from_json
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json

# Import spectra
spectra = list(load_from_mgf("spectra.mgf"))
spectra = list(load_from_mzml("data.mzML"))
spectra = list(load_from_msp("library.msp"))

# Export processed spectra
save_as_mgf(spectra, "output.mgf")
save_as_json(spectra, "output.json")
```

**Supported formats:**
- mzML and mzXML (raw mass spectrometry formats)
- MGF (Mascot Generic Format)
- MSP (spectral library format)
- JSON (GNPS-compatible)
- metabolomics-USI references
- Pickle (Python serialization)

For detailed importing/exporting documentation, consult `references/importing_exporting.md`.

### 2. Spectrum Filtering and Processing

Apply comprehensive filters to standardize metadata and refine peak data:

```python
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks

# Apply default metadata harmonization filters
spectrum = default_filters(spectrum)

# Normalize peak intensities
spectrum = normalize_intensities(spectrum)

# Filter peaks by relative intensity
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01, intensity_to=1.0)

# Require minimum peaks
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

**Filter categories:**
- **Metadata processing**: Harmonize compound names, derive chemical structures, standardize adducts, correct charges
- **Peak filtering**: Normalize intensities, select by m/z or intensity, remove precursor peaks
- **Quality control**: Require minimum peaks, validate precursor m/z, ensure metadata completeness
- **Chemical annotation**: Add fingerprints, derive InChI/SMILES, repair structural mismatches

Matchms provides 40+ filters. For the complete filter reference, consult `references/filtering.md`.

### 3. Calculating Spectral Similarities

Compare spectra using various similarity metrics:

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine, CosineHungarian

# Calculate cosine similarity (fast, greedy algorithm)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())

# Calculate modified cosine (accounts for precursor m/z differences)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=ModifiedCosine(tolerance=0.1))

# Get best matches
best_matches = scores.scores_by_query(query_spectra[0], sort=True)[:10]
```

**Available similarity functions:**
- **CosineGreedy/CosineHungarian**: Peak-based cosine similarity with different matching algorithms
- **ModifiedCosine**: Cosine similarity accounting for precursor mass differences
- **NeutralLossesCosine**: Similarity based on neutral loss patterns
- **FingerprintSimilarity**: Molecular structure similarity using fingerprints
- **MetadataMatch**: Compare user-defined metadata fields
- **PrecursorMzMatch/ParentMassMatch**: Simple mass-based filtering

For detailed similarity function documentation, consult `references/similarity.md`.

### 4. Building Processing Pipelines

Create reproducible, multi-step analysis workflows:

```python
from matchms import SpectrumProcessor
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, remove_peaks_around_precursor_mz

# Define a processing pipeline
processor = SpectrumProcessor([
    default_filters,
    normalize_intensities,
    lambda s: select_by_relative_intensity(s, intensity_from=0.01),
    lambda s: remove_peaks_around_precursor_mz(s, mz_tolerance=17)
])

# Apply to all spectra
processed_spectra = [processor(s) for s in spectra]
```

### 5. Working with Spectrum Objects

The core `Spectrum` class contains mass spectral data:

```python
from matchms import Spectrum
import numpy as np

# Create a spectrum
mz = np.array([100.0, 150.0, 200.0, 250.0])
intensities = np.array([0.1, 0.5, 0.9, 0.3])
metadata = {"precursor_mz": 250.5, "ionmode": "positive"}

spectrum = Spectrum(mz=mz, intensities=intensities, metadata=metadata)

# Access spectrum properties
print(spectrum.peaks.mz)           # m/z values
print(spectrum.peaks.intensities)  # Intensity values
print(spectrum.get("precursor_mz")) # Metadata field

# Visualize spectra
spectrum.plot()
spectrum.plot_against(reference_spectrum)
```

### 6. Metadata Management

Standardize and harmonize spectrum metadata:

```python
# Metadata is automatically harmonized
spectrum.set("Precursor_mz", 250.5)  # Gets harmonized to lowercase key
print(spectrum.get("precursor_mz"))   # Returns 250.5

# Derive chemical information
from matchms.filtering import derive_inchi_from_smiles, derive_inchikey_from_inchi
from matchms.filtering import add_fingerprint

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan", nbits=2048)
```

## Common Workflows

For typical mass spectrometry analysis workflows, including:
- Loading and preprocessing spectral libraries
- Matching unknown spectra against reference libraries
- Quality filtering and data cleaning
- Large-scale similarity comparisons
- Network-based spectral clustering

Consult `references/workflows.md` for detailed examples.

## Installation

```bash
uv pip install matchms
```

For molecular structure processing (SMILES, InChI):
```bash
uv pip install matchms[chemistry]
```

## Reference Documentation

Detailed reference documentation is available in the `references/` directory:
- `filtering.md` - Complete filter function reference with descriptions
- `similarity.md` - All similarity metrics and when to use them
- `importing_exporting.md` - File format details and I/O operations
- `workflows.md` - Common analysis patterns and examples

Load these references as needed for detailed information about specific matchms capabilities.

---

## Reference: Filtering

# Matchms Filtering Functions Reference

This document provides a comprehensive reference of all filtering functions available in matchms for processing mass spectrometry data.

## Metadata Processing Filters

### Compound & Chemical Information

**add_compound_name(spectrum)**
- Adds compound name to the correct metadata field
- Standardizes compound name storage location

**clean_compound_name(spectrum)**
- Removes frequently seen unwanted additions from compound names
- Cleans up formatting inconsistencies

**derive_adduct_from_name(spectrum)**
- Extracts adduct information from compound names
- Moves adduct notation to proper metadata field

**derive_formula_from_name(spectrum)**
- Detects chemical formulas in compound names
- Relocates formulas to appropriate metadata field

**derive_annotation_from_compound_name(spectrum)**
- Retrieves SMILES/InChI from PubChem using compound name
- Automatically annotates chemical structures

### Chemical Structure Conversions

**derive_inchi_from_smiles(spectrum)**
- Generates InChI from SMILES strings
- Requires rdkit library

**derive_inchikey_from_inchi(spectrum)**
- Computes InChIKey from InChI
- 27-character hashed identifier

**derive_smiles_from_inchi(spectrum)**
- Creates SMILES from InChI representation
- Requires rdkit library

**repair_inchi_inchikey_smiles(spectrum)**
- Corrects misplaced chemical identifiers
- Fixes metadata field confusion

**repair_not_matching_annotation(spectrum)**
- Ensures consistency between SMILES, InChI, and InChIKey
- Validates chemical structure annotations match

**add_fingerprint(spectrum, fingerprint_type="daylight", nbits=2048, radius=2)**
- Generates molecular fingerprints for similarity calculations
- Fingerprint types: "daylight", "morgan1", "morgan2", "morgan3"
- Used with FingerprintSimilarity scoring

### Mass & Charge Information

**add_precursor_mz(spectrum)**
- Normalizes precursor m/z values
- Standardizes precursor mass metadata

**add_parent_mass(spectrum, estimate_from_adduct=True)**
- Calculates neutral parent mass from precursor m/z and adduct
- Can estimate from adduct if not directly available

**correct_charge(spectrum)**
- Aligns charge values with ionmode
- Ensures charge sign matches ionization mode

**make_charge_int(spectrum)**
- Converts charge to integer format
- Standardizes charge representation

**clean_adduct(spectrum)**
- Standardizes adduct notation
- Corrects common adduct formatting issues

**interpret_pepmass(spectrum)**
- Parses pepmass field into component values
- Extracts precursor m/z and intensity from combined field

### Ion Mode & Validation

**derive_ionmode(spectrum)**
- Determines ionmode from adduct information
- Infers positive/negative mode from adduct type

**require_correct_ionmode(spectrum, ion_mode)**
- Filters spectra by specified ionmode
- Returns None if ionmode doesn't match
- Use: `spectrum = require_correct_ionmode(spectrum, "positive")`

**require_precursor_mz(spectrum, minimum_accepted_mz=0.0)**
- Validates precursor m/z presence and value
- Returns None if missing or below threshold

**require_precursor_below_mz(spectrum, maximum_accepted_mz=1000.0)**
- Enforces maximum precursor m/z limit
- Returns None if precursor exceeds threshold

### Retention Information

**add_retention_time(spectrum)**
- Harmonizes retention time as float values
- Standardizes RT metadata field

**add_retention_index(spectrum)**
- Stores retention index in standardized field
- Normalizes RI metadata

### Data Harmonization

**harmonize_undefined_inchi(spectrum, undefined="", aliases=None)**
- Standardizes undefined/empty InChI entries
- Replaces various "unknown" representations with consistent value

**harmonize_undefined_inchikey(spectrum, undefined="", aliases=None)**
- Standardizes undefined/empty InChIKey entries
- Unifies missing data representation

**harmonize_undefined_smiles(spectrum, undefined="", aliases=None)**
- Standardizes undefined/empty SMILES entries
- Consistent handling of missing structural data

### Repair & Quality Functions

**repair_adduct_based_on_smiles(spectrum, mass_tolerance=0.1)**
- Corrects adduct using SMILES and mass matching
- Validates adduct matches calculated mass

**repair_parent_mass_is_mol_wt(spectrum, mass_tolerance=0.1)**
- Converts molecular weight to monoisotopic mass
- Fixes common metadata confusion

**repair_precursor_is_parent_mass(spectrum)**
- Fixes swapped precursor/parent mass values
- Corrects field misassignments

**repair_smiles_of_salts(spectrum, mass_tolerance=0.1)**
- Removes salt components to match parent mass
- Extracts relevant molecular fragment

**require_parent_mass_match_smiles(spectrum, mass_tolerance=0.1)**
- Validates parent mass against SMILES-calculated mass
- Returns None if masses don't match within tolerance

**require_valid_annotation(spectrum)**
- Ensures complete, consistent chemical annotations
- Validates SMILES, InChI, and InChIKey presence and consistency

## Peak Processing Filters

### Normalization & Selection

**normalize_intensities(spectrum)**
- Scales peak intensities to unit height (max = 1.0)
- Essential preprocessing step for similarity calculations

**select_by_intensity(spectrum, intensity_from=0.0, intensity_to=1.0)**
- Retains peaks within specified absolute intensity range
- Filters by raw intensity values

**select_by_relative_intensity(spectrum, intensity_from=0.0, intensity_to=1.0)**
- Keeps peaks within relative intensity bounds
- Filters as fraction of maximum intensity

**select_by_mz(spectrum, mz_from=0.0, mz_to=1000.0)**
- Filters peaks by m/z value range
- Removes peaks outside specified m/z window

### Peak Reduction & Filtering

**reduce_to_number_of_peaks(spectrum, n_max=None, ratio_desired=None)**
- Removes lowest-intensity peaks when exceeding maximum
- Can specify absolute number or ratio
- Use: `spectrum = reduce_to_number_of_peaks(spectrum, n_max=100)`

**remove_peaks_around_precursor_mz(spectrum, mz_tolerance=17)**
- Eliminates peaks within tolerance of precursor
- Removes precursor and isotope peaks
- Common preprocessing for fragment-based similarity

**remove_peaks_outside_top_k(spectrum, k=10, ratio_desired=None)**
- Retains only peaks near k highest-intensity peaks
- Focuses on most informative signals

**require_minimum_number_of_peaks(spectrum, n_required=10)**
- Discards spectra with insufficient peaks
- Quality control filter
- Returns None if peak count below threshold

**require_minimum_number_of_high_peaks(spectrum, n_required=5, intensity_threshold=0.05)**
- Removes spectra lacking high-intensity peaks
- Ensures data quality
- Returns None if insufficient peaks above threshold

### Loss Calculation

**add_losses(spectrum, loss_mz_from=5.0, loss_mz_to=200.0)**
- Derives neutral losses from precursor mass
- Calculates loss = precursor_mz - fragment_mz
- Adds losses to spectrum for NeutralLossesCosine scoring

## Pipeline Functions

**default_filters(spectrum)**
- Applies nine essential metadata filters sequentially:
  1. make_charge_int
  2. add_precursor_mz
  3. add_retention_time
  4. add_retention_index
  5. derive_adduct_from_name
  6. derive_formula_from_name
  7. clean_compound_name
  8. harmonize_undefined_smiles
  9. harmonize_undefined_inchi
- Recommended starting point for metadata harmonization

**SpectrumProcessor(filters)**
- Orchestrates multi-filter pipelines
- Accepts list of filter functions
- Example:
```python
from matchms import SpectrumProcessor
processor = SpectrumProcessor([
    default_filters,
    normalize_intensities,
    lambda s: select_by_relative_intensity(s, intensity_from=0.01)
])
processed = processor(spectrum)
```

## Common Filter Combinations

### Standard Preprocessing Pipeline
```python
from matchms.filtering import (default_filters, normalize_intensities,
                               select_by_relative_intensity,
                               require_minimum_number_of_peaks)

spectrum = default_filters(spectrum)
spectrum = normalize_intensities(spectrum)
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

### Quality Control Pipeline
```python
from matchms.filtering import (require_precursor_mz, require_minimum_number_of_peaks,
                               require_minimum_number_of_high_peaks)

spectrum = require_precursor_mz(spectrum, minimum_accepted_mz=50.0)
if spectrum is None:
    # Spectrum failed quality control
    pass
spectrum = require_minimum_number_of_peaks(spectrum, n_required=10)
spectrum = require_minimum_number_of_high_peaks(spectrum, n_required=5)
```

### Chemical Annotation Pipeline
```python
from matchms.filtering import (derive_inchi_from_smiles, derive_inchikey_from_inchi,
                               add_fingerprint, require_valid_annotation)

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan2", nbits=2048)
spectrum = require_valid_annotation(spectrum)
```

### Peak Cleaning Pipeline
```python
from matchms.filtering import (normalize_intensities, remove_peaks_around_precursor_mz,
                               select_by_relative_intensity, reduce_to_number_of_peaks)

spectrum = normalize_intensities(spectrum)
spectrum = remove_peaks_around_precursor_mz(spectrum, mz_tolerance=17)
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
spectrum = reduce_to_number_of_peaks(spectrum, n_max=200)
```

## Notes on Filter Usage

1. **Order matters**: Apply filters in logical sequence (e.g., normalize before relative intensity selection)
2. **Filters return None**: Many filters return None for invalid spectra; check for None before proceeding
3. **Immutability**: Filters typically return modified copies; reassign results to variables
4. **Pipeline efficiency**: Use SpectrumProcessor for consistent multi-spectrum processing
5. **Documentation**: For detailed parameters, see matchms.readthedocs.io/en/latest/api/matchms.filtering.html

---

## Reference: Importing_Exporting

# Matchms Importing and Exporting Reference

This document details all file format support in matchms for loading and saving mass spectrometry data.

## Importing Spectra

Matchms provides dedicated functions for loading spectra from various file formats. All import functions return generators for memory-efficient processing of large files.

### Common Import Pattern

```python
from matchms.importing import load_from_mgf

# Load spectra (returns generator)
spectra_generator = load_from_mgf("spectra.mgf")

# Convert to list for processing
spectra = list(spectra_generator)
```

## Supported Import Formats

### MGF (Mascot Generic Format)

**Function**: `load_from_mgf(filename, metadata_harmonization=True)`

**Description**: Loads spectra from MGF files, a common format for mass spectrometry data exchange.

**Parameters**:
- `filename` (str): Path to MGF file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata key harmonization

**Example**:
```python
from matchms.importing import load_from_mgf

# Load with metadata harmonization
spectra = list(load_from_mgf("data.mgf"))

# Load without harmonization
spectra = list(load_from_mgf("data.mgf", metadata_harmonization=False))
```

**MGF Format**: Text-based format with BEGIN IONS/END IONS blocks containing metadata and peak lists.

---

### MSP (NIST Mass Spectral Library Format)

**Function**: `load_from_msp(filename, metadata_harmonization=True)`

**Description**: Loads spectra from MSP files, commonly used for spectral libraries.

**Parameters**:
- `filename` (str): Path to MSP file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_msp

spectra = list(load_from_msp("library.msp"))
```

**MSP Format**: Text-based format with Name/MW/Comment fields followed by peak lists.

---

### mzML (Mass Spectrometry Markup Language)

**Function**: `load_from_mzml(filename, ms_level=2, metadata_harmonization=True)`

**Description**: Loads spectra from mzML files, the standard XML-based format for raw mass spectrometry data.

**Parameters**:
- `filename` (str): Path to mzML file
- `ms_level` (int, default=2): MS level to extract (1 for MS1, 2 for MS2/tandem)
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_mzml

# Load MS2 spectra (default)
ms2_spectra = list(load_from_mzml("data.mzML"))

# Load MS1 spectra
ms1_spectra = list(load_from_mzml("data.mzML", ms_level=1))
```

**mzML Format**: XML-based standard format containing raw instrument data and rich metadata.

---

### mzXML

**Function**: `load_from_mzxml(filename, ms_level=2, metadata_harmonization=True)`

**Description**: Loads spectra from mzXML files, an earlier XML-based format for mass spectrometry data.

**Parameters**:
- `filename` (str): Path to mzXML file
- `ms_level` (int, default=2): MS level to extract
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_mzxml

spectra = list(load_from_mzxml("data.mzXML"))
```

**mzXML Format**: XML-based format, predecessor to mzML.

---

### JSON (GNPS Format)

**Function**: `load_from_json(filename, metadata_harmonization=True)`

**Description**: Loads spectra from JSON files, particularly GNPS-compatible JSON format.

**Parameters**:
- `filename` (str): Path to JSON file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_json

spectra = list(load_from_json("spectra.json"))
```

**JSON Format**: Structured JSON with spectrum metadata and peak arrays.

---

### Pickle (Python Serialization)

**Function**: `load_from_pickle(filename)`

**Description**: Loads previously saved matchms Spectrum objects from pickle files. Fast loading of preprocessed spectra.

**Parameters**:
- `filename` (str): Path to pickle file

**Example**:
```python
from matchms.importing import load_from_pickle

spectra = list(load_from_pickle("processed_spectra.pkl"))
```

**Use case**: Saving and loading preprocessed spectra for faster subsequent analyses.

---

### USI (Universal Spectrum Identifier)

**Function**: `load_from_usi(usi)`

**Description**: Loads a single spectrum from a metabolomics USI reference.

**Parameters**:
- `usi` (str): Universal Spectrum Identifier string

**Example**:
```python
from matchms.importing import load_from_usi

usi = "mzspec:GNPS:TASK-...:spectrum..."
spectrum = load_from_usi(usi)
```

**USI Format**: Standardized identifier for accessing spectra from online repositories.

---

## Exporting Spectra

Matchms provides functions to save processed spectra to various formats for sharing and archival.

### MGF Export

**Function**: `save_as_mgf(spectra, filename, write_mode='w')`

**Description**: Saves spectra to MGF format.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path
- `write_mode` (str, default='w'): File write mode ('w' for write, 'a' for append)

**Example**:
```python
from matchms.exporting import save_as_mgf

save_as_mgf(processed_spectra, "output.mgf")
```

---

### MSP Export

**Function**: `save_as_msp(spectra, filename, write_mode='w')`

**Description**: Saves spectra to MSP format.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path
- `write_mode` (str, default='w'): File write mode

**Example**:
```python
from matchms.exporting import save_as_msp

save_as_msp(library_spectra, "library.msp")
```

---

### JSON Export

**Function**: `save_as_json(spectra, filename, write_mode='w')`

**Description**: Saves spectra to JSON format (GNPS-compatible).

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path
- `write_mode` (str, default='w'): File write mode

**Example**:
```python
from matchms.exporting import save_as_json

save_as_json(spectra, "spectra.json")
```

---

### Pickle Export

**Function**: `save_as_pickle(spectra, filename)`

**Description**: Saves spectra as Python pickle file. Preserves all Spectrum attributes and is fastest for loading.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path

**Example**:
```python
from matchms.exporting import save_as_pickle

save_as_pickle(processed_spectra, "processed.pkl")
```

**Advantages**:
- Fast save and load
- Preserves exact Spectrum state
- No format conversion overhead

**Disadvantages**:
- Not human-readable
- Python-specific (not portable to other languages)
- Pickle format may not be compatible across Python versions

---

## Complete Import/Export Workflow

### Preprocessing and Saving Pipeline

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf, save_as_pickle
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity

# Load raw spectra
spectra = list(load_from_mgf("raw_data.mgf"))

# Process spectra
processed = []
for spectrum in spectra:
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
    if spectrum is not None:
        processed.append(spectrum)

# Save processed spectra (MGF for sharing)
save_as_mgf(processed, "processed_data.mgf")

# Save as pickle for fast reloading
save_as_pickle(processed, "processed_data.pkl")
```

### Format Conversion

```python
from matchms.importing import load_from_mzml
from matchms.exporting import save_as_mgf, save_as_msp

# Convert mzML to MGF
spectra = list(load_from_mzml("data.mzML", ms_level=2))
save_as_mgf(spectra, "data.mgf")

# Convert to MSP library format
save_as_msp(spectra, "data.msp")
```

### Loading from Multiple Files

```python
from matchms.importing import load_from_mgf
import glob

# Load all MGF files in directory
all_spectra = []
for mgf_file in glob.glob("data/*.mgf"):
    spectra = list(load_from_mgf(mgf_file))
    all_spectra.extend(spectra)

print(f"Loaded {len(all_spectra)} spectra from multiple files")
```

### Memory-Efficient Processing

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import default_filters, normalize_intensities

# Process large file without loading all into memory
def process_spectrum(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    return spectrum

# Stream processing
with open("output.mgf", 'w') as outfile:
    for spectrum in load_from_mgf("large_file.mgf"):
        processed = process_spectrum(spectrum)
        if processed is not None:
            # Write immediately without storing in memory
            save_as_mgf([processed], outfile, write_mode='a')
```

## Format Selection Guidelines

**MGF**:
- ✓ Widely supported
- ✓ Human-readable
- ✓ Good for data sharing
- ✓ Moderate file size
- Best for: Data exchange, GNPS uploads, publication data

**MSP**:
- ✓ Spectral library standard
- ✓ Human-readable
- ✓ Good metadata support
- Best for: Reference libraries, NIST format compatibility

**JSON**:
- ✓ Structured format
- ✓ GNPS compatible
- ✓ Easy to parse programmatically
- Best for: Web applications, GNPS integration, structured data

**Pickle**:
- ✓ Fastest save/load
- ✓ Preserves exact state
- ✗ Not portable to other languages
- ✗ Not human-readable
- Best for: Intermediate processing, Python-only workflows

**mzML/mzXML**:
- ✓ Raw instrument data
- ✓ Rich metadata
- ✓ Industry standard
- ✗ Large file size
- ✗ Slower to parse
- Best for: Raw data archival, multi-level MS data

## Metadata Harmonization

The `metadata_harmonization` parameter (available in most import functions) automatically standardizes metadata keys:

```python
# Without harmonization
spectrum = load_from_mgf("data.mgf", metadata_harmonization=False)
# May have: "PRECURSOR_MZ", "Precursor_mz", "precursormz"

# With harmonization (default)
spectrum = load_from_mgf("data.mgf", metadata_harmonization=True)
# Standardized to: "precursor_mz"
```

**Recommended**: Keep harmonization enabled (default) for consistent metadata access across different data sources.

## File Format Specifications

For detailed format specifications:
- **MGF**: http://www.matrixscience.com/help/data_file_help.html
- **MSP**: https://chemdata.nist.gov/mass-spc/ms-search/
- **mzML**: http://www.psidev.info/mzML
- **GNPS JSON**: https://gnps.ucsd.edu/

## Further Reading

For complete API documentation:
https://matchms.readthedocs.io/en/latest/api/matchms.importing.html
https://matchms.readthedocs.io/en/latest/api/matchms.exporting.html

---

## Reference: Similarity

# Matchms Similarity Functions Reference

This document provides detailed information about all similarity scoring methods available in matchms.

## Overview

Matchms provides multiple similarity functions for comparing mass spectra. Use `calculate_scores()` to compute pairwise similarities between reference and query spectra collections.

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy

scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())
```

## Peak-Based Similarity Functions

These functions compare mass spectra based on their peak patterns (m/z and intensity values).

### CosineGreedy

**Description**: Calculates cosine similarity between two spectra using a fast greedy matching algorithm. Peaks are matched within a specified tolerance, and similarity is computed based on matched peak intensities.

**When to use**:
- Fast similarity calculations for large datasets
- General-purpose spectral matching
- When speed is prioritized over mathematically optimal matching

**Parameters**:
- `tolerance` (float, default=0.1): Maximum m/z difference for peak matching (Daltons)
- `mz_power` (float, default=0.0): Exponent for m/z weighting (0 = no weighting)
- `intensity_power` (float, default=1.0): Exponent for intensity weighting

**Example**:
```python
from matchms.similarity import CosineGreedy

similarity_func = CosineGreedy(tolerance=0.1, mz_power=0.0, intensity_power=1.0)
scores = calculate_scores(references, queries, similarity_func)
```

**Output**: Similarity score between 0.0 and 1.0, plus number of matched peaks.

---

### CosineHungarian

**Description**: Calculates cosine similarity using the Hungarian algorithm for optimal peak matching. Provides mathematically optimal peak assignments but is slower than CosineGreedy.

**When to use**:
- When optimal peak matching is required
- High-quality reference library comparisons
- Research requiring reproducible, mathematically rigorous results

**Parameters**:
- `tolerance` (float, default=0.1): Maximum m/z difference for peak matching
- `mz_power` (float, default=0.0): Exponent for m/z weighting
- `intensity_power` (float, default=1.0): Exponent for intensity weighting

**Example**:
```python
from matchms.similarity import CosineHungarian

similarity_func = CosineHungarian(tolerance=0.1)
scores = calculate_scores(references, queries, similarity_func)
```

**Output**: Optimal similarity score between 0.0 and 1.0, plus matched peaks.

**Note**: Slower than CosineGreedy; use for smaller datasets or when accuracy is critical.

---

### ModifiedCosine

**Description**: Extends cosine similarity by accounting for precursor m/z differences. Allows peaks to match after applying a mass shift based on the difference between precursor masses. Useful for comparing spectra of related compounds (isotopes, adducts, analogs).

**When to use**:
- Comparing spectra from different precursor masses
- Identifying structural analogs or derivatives
- Cross-ionization mode comparisons
- When precursor mass differences are meaningful

**Parameters**:
- `tolerance` (float, default=0.1): Maximum m/z difference for peak matching after shift
- `mz_power` (float, default=0.0): Exponent for m/z weighting
- `intensity_power` (float, default=1.0): Exponent for intensity weighting

**Example**:
```python
from matchms.similarity import ModifiedCosine

similarity_func = ModifiedCosine(tolerance=0.1)
scores = calculate_scores(references, queries, similarity_func)
```

**Requirements**: Both spectra must have valid precursor_mz metadata.

---

### NeutralLossesCosine

**Description**: Calculates similarity based on neutral loss patterns rather than fragment m/z values. Neutral losses are derived by subtracting fragment m/z from precursor m/z. Particularly useful for identifying compounds with similar fragmentation patterns.

**When to use**:
- Comparing fragmentation patterns across different precursor masses
- Identifying compounds with similar neutral loss profiles
- Complementary to regular cosine scoring
- Metabolite identification and classification

**Parameters**:
- `tolerance` (float, default=0.1): Maximum neutral loss difference for matching
- `mz_power` (float, default=0.0): Exponent for loss value weighting
- `intensity_power` (float, default=1.0): Exponent for intensity weighting

**Example**:
```python
from matchms.similarity import NeutralLossesCosine
from matchms.filtering import add_losses

# First add losses to spectra
spectra_with_losses = [add_losses(s) for s in spectra]

similarity_func = NeutralLossesCosine(tolerance=0.1)
scores = calculate_scores(references_with_losses, queries_with_losses, similarity_func)
```

**Requirements**:
- Both spectra must have valid precursor_mz metadata
- Use `add_losses()` filter to compute neutral losses before scoring

---

## Structural Similarity Functions

These functions compare molecular structures rather than spectral peaks.

### FingerprintSimilarity

**Description**: Calculates similarity between molecular fingerprints derived from chemical structures (SMILES or InChI). Supports multiple fingerprint types and similarity metrics.

**When to use**:
- Structural similarity without spectral data
- Combining structural and spectral similarity
- Pre-filtering candidates before spectral matching
- Structure-activity relationship studies

**Parameters**:
- `fingerprint_type` (str, default="daylight"): Type of fingerprint
  - `"daylight"`: Daylight fingerprint
  - `"morgan1"`, `"morgan2"`, `"morgan3"`: Morgan fingerprints with radius 1, 2, or 3
- `similarity_measure` (str, default="jaccard"): Similarity metric
  - `"jaccard"`: Jaccard index (intersection / union)
  - `"dice"`: Dice coefficient (2 * intersection / (size1 + size2))
  - `"cosine"`: Cosine similarity

**Example**:
```python
from matchms.similarity import FingerprintSimilarity
from matchms.filtering import add_fingerprint

# Add fingerprints to spectra
spectra_with_fps = [add_fingerprint(s, fingerprint_type="morgan2", nbits=2048)
                    for s in spectra]

similarity_func = FingerprintSimilarity(similarity_measure="jaccard")
scores = calculate_scores(references_with_fps, queries_with_fps, similarity_func)
```

**Requirements**:
- Spectra must have valid SMILES or InChI metadata
- Use `add_fingerprint()` filter to compute fingerprints
- Requires rdkit library

---

## Metadata-Based Similarity Functions

These functions compare metadata fields rather than spectral or structural data.

### MetadataMatch

**Description**: Compares user-defined metadata fields between spectra. Supports exact matching for categorical data and tolerance-based matching for numerical data.

**When to use**:
- Filtering by experimental conditions (collision energy, retention time)
- Instrument-specific matching
- Combining metadata constraints with spectral similarity
- Custom metadata-based filtering

**Parameters**:
- `field` (str): Metadata field name to compare
- `matching_type` (str, default="exact"): Matching method
  - `"exact"`: Exact string/value match
  - `"difference"`: Absolute difference for numerical values
  - `"relative_difference"`: Relative difference for numerical values
- `tolerance` (float, optional): Maximum difference for numerical matching

**Example (Exact matching)**:
```python
from matchms.similarity import MetadataMatch

# Match by instrument type
similarity_func = MetadataMatch(field="instrument_type", matching_type="exact")
scores = calculate_scores(references, queries, similarity_func)
```

**Example (Numerical matching)**:
```python
# Match retention time within 0.5 minutes
similarity_func = MetadataMatch(field="retention_time",
                                matching_type="difference",
                                tolerance=0.5)
scores = calculate_scores(references, queries, similarity_func)
```

**Output**: Returns 1.0 (match) or 0.0 (no match) for exact matching. For numerical matching, returns similarity score based on difference.

---

### PrecursorMzMatch

**Description**: Binary matching based on precursor m/z values. Returns True/False based on whether precursor masses match within specified tolerance.

**When to use**:
- Pre-filtering spectral libraries by precursor mass
- Fast mass-based candidate selection
- Combining with other similarity metrics
- Isobaric compound identification

**Parameters**:
- `tolerance` (float, default=0.1): Maximum m/z difference for matching
- `tolerance_type` (str, default="Dalton"): Tolerance unit
  - `"Dalton"`: Absolute mass difference
  - `"ppm"`: Parts per million (relative)

**Example**:
```python
from matchms.similarity import PrecursorMzMatch

# Match precursor within 0.1 Da
similarity_func = PrecursorMzMatch(tolerance=0.1, tolerance_type="Dalton")
scores = calculate_scores(references, queries, similarity_func)

# Match precursor within 10 ppm
similarity_func = PrecursorMzMatch(tolerance=10, tolerance_type="ppm")
scores = calculate_scores(references, queries, similarity_func)
```

**Output**: 1.0 (match) or 0.0 (no match)

**Requirements**: Both spectra must have valid precursor_mz metadata.

---

### ParentMassMatch

**Description**: Binary matching based on parent mass (neutral mass) values. Similar to PrecursorMzMatch but uses calculated parent mass instead of precursor m/z.

**When to use**:
- Comparing spectra from different ionization modes
- Adduct-independent matching
- Neutral mass-based library searches

**Parameters**:
- `tolerance` (float, default=0.1): Maximum mass difference for matching
- `tolerance_type` (str, default="Dalton"): Tolerance unit ("Dalton" or "ppm")

**Example**:
```python
from matchms.similarity import ParentMassMatch

similarity_func = ParentMassMatch(tolerance=0.1, tolerance_type="Dalton")
scores = calculate_scores(references, queries, similarity_func)
```

**Output**: 1.0 (match) or 0.0 (no match)

**Requirements**: Both spectra must have valid parent_mass metadata.

---

## Combining Multiple Similarity Functions

Combine multiple similarity metrics for robust compound identification:

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine, FingerprintSimilarity

# Calculate multiple similarity scores
cosine_scores = calculate_scores(refs, queries, CosineGreedy())
modified_cosine_scores = calculate_scores(refs, queries, ModifiedCosine())
fingerprint_scores = calculate_scores(refs, queries, FingerprintSimilarity())

# Combine scores with weights
for i, query in enumerate(queries):
    for j, ref in enumerate(refs):
        combined_score = (0.5 * cosine_scores.scores[j, i] +
                         0.3 * modified_cosine_scores.scores[j, i] +
                         0.2 * fingerprint_scores.scores[j, i])
```

## Accessing Scores Results

The `Scores` object provides multiple methods to access results:

```python
# Get best matches for a query
best_matches = scores.scores_by_query(query_spectrum, sort=True)[:10]

# Get scores as numpy array
score_array = scores.scores

# Get scores as pandas DataFrame
import pandas as pd
df = scores.to_dataframe()

# Filter by threshold
high_scores = [(i, j, score) for i, j, score in scores.to_list() if score > 0.7]

# Save scores
scores.to_json("scores.json")
scores.to_pickle("scores.pkl")
```

## Performance Considerations

**Fast methods** (large datasets):
- CosineGreedy
- PrecursorMzMatch
- ParentMassMatch

**Slow methods** (smaller datasets or high accuracy):
- CosineHungarian
- ModifiedCosine (slower than CosineGreedy)
- NeutralLossesCosine
- FingerprintSimilarity (requires fingerprint computation)

**Recommendation**: For large-scale library searches, use PrecursorMzMatch to pre-filter candidates, then apply CosineGreedy or ModifiedCosine to filtered results.

## Common Similarity Workflows

### Standard Library Matching
```python
from matchms.similarity import CosineGreedy

scores = calculate_scores(library_spectra, query_spectra,
                         CosineGreedy(tolerance=0.1))
```

### Multi-Metric Matching
```python
from matchms.similarity import CosineGreedy, ModifiedCosine, FingerprintSimilarity

# Spectral similarity
cosine = calculate_scores(refs, queries, CosineGreedy())
modified = calculate_scores(refs, queries, ModifiedCosine())

# Structural similarity
fingerprint = calculate_scores(refs, queries, FingerprintSimilarity())
```

### Precursor-Filtered Matching
```python
from matchms.similarity import PrecursorMzMatch, CosineGreedy

# First filter by precursor mass
mass_filter = calculate_scores(refs, queries, PrecursorMzMatch(tolerance=0.1))

# Then calculate cosine only for matching precursors
cosine_scores = calculate_scores(refs, queries, CosineGreedy())
```

## Further Reading

For detailed API documentation, parameter descriptions, and mathematical formulations, see:
https://matchms.readthedocs.io/en/latest/api/matchms.similarity.html

---

## Reference: Workflows

# Matchms Common Workflows

This document provides detailed examples of common mass spectrometry analysis workflows using matchms.

## Workflow 1: Basic Spectral Library Matching

Match unknown spectra against a reference library to identify compounds.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks
from matchms import calculate_scores
from matchms.similarity import CosineGreedy

# Load reference library
print("Loading reference library...")
library = list(load_from_mgf("reference_library.mgf"))

# Load query spectra (unknowns)
print("Loading query spectra...")
queries = list(load_from_mgf("unknown_spectra.mgf"))

# Process library spectra
print("Processing library...")
processed_library = []
for spectrum in library:
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
    spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
    if spectrum is not None:
        processed_library.append(spectrum)

# Process query spectra
print("Processing queries...")
processed_queries = []
for spectrum in queries:
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
    spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
    if spectrum is not None:
        processed_queries.append(spectrum)

# Calculate similarities
print("Calculating similarities...")
scores = calculate_scores(references=processed_library,
                         queries=processed_queries,
                         similarity_function=CosineGreedy(tolerance=0.1))

# Get top matches for each query
print("\nTop matches:")
for i, query in enumerate(processed_queries):
    top_matches = scores.scores_by_query(query, sort=True)[:5]

    query_name = query.get("compound_name", f"Query {i}")
    print(f"\n{query_name}:")

    for ref_idx, score in top_matches:
        ref_spectrum = processed_library[ref_idx]
        ref_name = ref_spectrum.get("compound_name", f"Ref {ref_idx}")
        print(f"  {ref_name}: {score:.4f}")
```

---

## Workflow 2: Quality Control and Data Cleaning

Filter and clean spectral data before analysis.

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import (default_filters, normalize_intensities,
                               require_precursor_mz, require_minimum_number_of_peaks,
                               require_minimum_number_of_high_peaks,
                               select_by_relative_intensity, remove_peaks_around_precursor_mz)

# Load spectra
spectra = list(load_from_mgf("raw_data.mgf"))
print(f"Loaded {len(spectra)} raw spectra")

# Apply quality filters
cleaned_spectra = []
for spectrum in spectra:
    # Harmonize metadata
    spectrum = default_filters(spectrum)

    # Quality requirements
    spectrum = require_precursor_mz(spectrum, minimum_accepted_mz=50.0)
    if spectrum is None:
        continue

    spectrum = require_minimum_number_of_peaks(spectrum, n_required=10)
    if spectrum is None:
        continue

    # Clean peaks
    spectrum = normalize_intensities(spectrum)
    spectrum = remove_peaks_around_precursor_mz(spectrum, mz_tolerance=17)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)

    # Require high-quality peaks
    spectrum = require_minimum_number_of_high_peaks(spectrum,
                                                     n_required=5,
                                                     intensity_threshold=0.05)
    if spectrum is None:
        continue

    cleaned_spectra.append(spectrum)

print(f"Retained {len(cleaned_spectra)} high-quality spectra")
print(f"Removed {len(spectra) - len(cleaned_spectra)} low-quality spectra")

# Save cleaned data
save_as_mgf(cleaned_spectra, "cleaned_data.mgf")
```

---

## Workflow 3: Multi-Metric Similarity Scoring

Combine multiple similarity metrics for robust compound identification.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import (default_filters, normalize_intensities,
                               derive_inchi_from_smiles, add_fingerprint, add_losses)
from matchms import calculate_scores
from matchms.similarity import (CosineGreedy, ModifiedCosine,
                                NeutralLossesCosine, FingerprintSimilarity)
import numpy as np

# Load spectra
library = list(load_from_mgf("library.mgf"))
queries = list(load_from_mgf("queries.mgf"))

# Process with multiple features
def process_for_multimetric(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)

    # Add chemical fingerprints
    spectrum = derive_inchi_from_smiles(spectrum)
    spectrum = add_fingerprint(spectrum, fingerprint_type="morgan2", nbits=2048)

    # Add neutral losses
    spectrum = add_losses(spectrum, loss_mz_from=5.0, loss_mz_to=200.0)

    return spectrum

processed_library = [process_for_multimetric(s) for s in library if s is not None]
processed_queries = [process_for_multimetric(s) for s in queries if s is not None]

# Calculate multiple similarity scores
print("Calculating Cosine similarity...")
cosine_scores = calculate_scores(processed_library, processed_queries,
                                 CosineGreedy(tolerance=0.1))

print("Calculating Modified Cosine similarity...")
modified_cosine_scores = calculate_scores(processed_library, processed_queries,
                                         ModifiedCosine(tolerance=0.1))

print("Calculating Neutral Losses similarity...")
neutral_losses_scores = calculate_scores(processed_library, processed_queries,
                                        NeutralLossesCosine(tolerance=0.1))

print("Calculating Fingerprint similarity...")
fingerprint_scores = calculate_scores(processed_library, processed_queries,
                                      FingerprintSimilarity(similarity_measure="jaccard"))

# Combine scores with weights
weights = {
    'cosine': 0.4,
    'modified_cosine': 0.3,
    'neutral_losses': 0.2,
    'fingerprint': 0.1
}

# Get combined scores for each query
for i, query in enumerate(processed_queries):
    query_name = query.get("compound_name", f"Query {i}")

    combined_scores = []
    for j, ref in enumerate(processed_library):
        combined = (weights['cosine'] * cosine_scores.scores[j, i] +
                   weights['modified_cosine'] * modified_cosine_scores.scores[j, i] +
                   weights['neutral_losses'] * neutral_losses_scores.scores[j, i] +
                   weights['fingerprint'] * fingerprint_scores.scores[j, i])
        combined_scores.append((j, combined))

    # Sort by combined score
    combined_scores.sort(key=lambda x: x[1], reverse=True)

    print(f"\n{query_name} - Top 3 matches:")
    for ref_idx, score in combined_scores[:3]:
        ref_name = processed_library[ref_idx].get("compound_name", f"Ref {ref_idx}")
        print(f"  {ref_name}: {score:.4f}")
```

---

## Workflow 4: Precursor-Filtered Library Search

Pre-filter by precursor mass before spectral matching for faster searches.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import default_filters, normalize_intensities
from matchms import calculate_scores
from matchms.similarity import PrecursorMzMatch, CosineGreedy
import numpy as np

# Load data
library = list(load_from_mgf("large_library.mgf"))
queries = list(load_from_mgf("queries.mgf"))

# Process spectra
processed_library = [normalize_intensities(default_filters(s)) for s in library]
processed_queries = [normalize_intensities(default_filters(s)) for s in queries]

# Step 1: Fast precursor mass filtering
print("Filtering by precursor mass...")
mass_filter = calculate_scores(processed_library, processed_queries,
                               PrecursorMzMatch(tolerance=0.1, tolerance_type="Dalton"))

# Step 2: Calculate cosine only for matching precursors
print("Calculating cosine similarity for filtered candidates...")
cosine_scores = calculate_scores(processed_library, processed_queries,
                                CosineGreedy(tolerance=0.1))

# Step 3: Apply mass filter to cosine scores
for i, query in enumerate(processed_queries):
    candidates = []

    for j, ref in enumerate(processed_library):
        # Only consider if precursor matches
        if mass_filter.scores[j, i] > 0:
            cosine_score = cosine_scores.scores[j, i]
            candidates.append((j, cosine_score))

    # Sort by cosine score
    candidates.sort(key=lambda x: x[1], reverse=True)

    query_name = query.get("compound_name", f"Query {i}")
    print(f"\n{query_name} - Top 5 matches (from {len(candidates)} candidates):")

    for ref_idx, score in candidates[:5]:
        ref_name = processed_library[ref_idx].get("compound_name", f"Ref {ref_idx}")
        ref_mz = processed_library[ref_idx].get("precursor_mz", "N/A")
        print(f"  {ref_name} (m/z {ref_mz}): {score:.4f}")
```

---

## Workflow 5: Building a Reusable Processing Pipeline

Create a standardized pipeline for consistent processing.

```python
from matchms import SpectrumProcessor
from matchms.filtering import (default_filters, normalize_intensities,
                               select_by_relative_intensity,
                               remove_peaks_around_precursor_mz,
                               require_minimum_number_of_peaks,
                               derive_inchi_from_smiles, add_fingerprint)
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_pickle

# Define custom processing pipeline
def create_standard_pipeline():
    """Create a reusable processing pipeline"""
    return SpectrumProcessor([
        default_filters,
        normalize_intensities,
        lambda s: remove_peaks_around_precursor_mz(s, mz_tolerance=17),
        lambda s: select_by_relative_intensity(s, intensity_from=0.01),
        lambda s: require_minimum_number_of_peaks(s, n_required=5),
        derive_inchi_from_smiles,
        lambda s: add_fingerprint(s, fingerprint_type="morgan2")
    ])

# Create pipeline instance
pipeline = create_standard_pipeline()

# Process multiple datasets with same pipeline
datasets = ["dataset1.mgf", "dataset2.mgf", "dataset3.mgf"]

for dataset_file in datasets:
    print(f"\nProcessing {dataset_file}...")

    # Load spectra
    spectra = list(load_from_mgf(dataset_file))

    # Apply pipeline
    processed = []
    for spectrum in spectra:
        result = pipeline(spectrum)
        if result is not None:
            processed.append(result)

    print(f"  Loaded: {len(spectra)}")
    print(f"  Processed: {len(processed)}")

    # Save processed data
    output_file = dataset_file.replace(".mgf", "_processed.pkl")
    save_as_pickle(processed, output_file)
    print(f"  Saved to: {output_file}")
```

---

## Workflow 6: Format Conversion and Standardization

Convert between different mass spectrometry file formats.

```python
from matchms.importing import load_from_mzml, load_from_mgf
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json
from matchms.filtering import default_filters, normalize_intensities

def convert_and_standardize(input_file, output_format="mgf"):
    """
    Load, standardize, and convert mass spectrometry data

    Parameters:
    -----------
    input_file : str
        Input file path (supports .mzML, .mzXML, .mgf)
    output_format : str
        Output format ('mgf', 'msp', or 'json')
    """
    # Determine input format and load
    if input_file.endswith('.mzML') or input_file.endswith('.mzXML'):
        from matchms.importing import load_from_mzml
        spectra = list(load_from_mzml(input_file, ms_level=2))
    elif input_file.endswith('.mgf'):
        spectra = list(load_from_mgf(input_file))
    else:
        raise ValueError(f"Unsupported format: {input_file}")

    print(f"Loaded {len(spectra)} spectra from {input_file}")

    # Standardize
    processed = []
    for spectrum in spectra:
        spectrum = default_filters(spectrum)
        spectrum = normalize_intensities(spectrum)
        if spectrum is not None:
            processed.append(spectrum)

    print(f"Standardized {len(processed)} spectra")

    # Export
    output_file = input_file.rsplit('.', 1)[0] + f'_standardized.{output_format}'

    if output_format == 'mgf':
        save_as_mgf(processed, output_file)
    elif output_format == 'msp':
        save_as_msp(processed, output_file)
    elif output_format == 'json':
        save_as_json(processed, output_file)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    print(f"Saved to {output_file}")
    return processed

# Convert mzML to MGF
convert_and_standardize("raw_data.mzML", output_format="mgf")

# Convert MGF to MSP library format
convert_and_standardize("library.mgf", output_format="msp")
```

---

## Workflow 7: Metadata Enrichment and Validation

Enrich spectra with chemical structure information and validate annotations.

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import (default_filters, derive_inchi_from_smiles,
                               derive_inchikey_from_inchi, derive_smiles_from_inchi,
                               add_fingerprint, repair_not_matching_annotation,
                               require_valid_annotation)

# Load spectra
spectra = list(load_from_mgf("spectra.mgf"))

# Enrich and validate
enriched_spectra = []
validation_failures = []

for i, spectrum in enumerate(spectra):
    # Basic harmonization
    spectrum = default_filters(spectrum)

    # Derive chemical structures
    spectrum = derive_inchi_from_smiles(spectrum)
    spectrum = derive_inchikey_from_inchi(spectrum)
    spectrum = derive_smiles_from_inchi(spectrum)

    # Repair mismatches
    spectrum = repair_not_matching_annotation(spectrum)

    # Add molecular fingerprints
    spectrum = add_fingerprint(spectrum, fingerprint_type="morgan2", nbits=2048)

    # Validate
    validated = require_valid_annotation(spectrum)

    if validated is not None:
        enriched_spectra.append(validated)
    else:
        validation_failures.append(i)

print(f"Successfully enriched: {len(enriched_spectra)}")
print(f"Validation failures: {len(validation_failures)}")

# Save enriched data
save_as_mgf(enriched_spectra, "enriched_spectra.mgf")

# Report failures
if validation_failures:
    print("\nSpectra that failed validation:")
    for idx in validation_failures[:10]:  # Show first 10
        original = spectra[idx]
        name = original.get("compound_name", f"Spectrum {idx}")
        print(f"  - {name}")
```

---

## Workflow 8: Large-Scale Library Comparison

Compare two large spectral libraries efficiently.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import default_filters, normalize_intensities
from matchms import calculate_scores
from matchms.similarity import CosineGreedy
import numpy as np

# Load two libraries
print("Loading libraries...")
library1 = list(load_from_mgf("library1.mgf"))
library2 = list(load_from_mgf("library2.mgf"))

# Process
processed_lib1 = [normalize_intensities(default_filters(s)) for s in library1]
processed_lib2 = [normalize_intensities(default_filters(s)) for s in library2]

# Calculate all-vs-all similarities
print("Calculating similarities...")
scores = calculate_scores(processed_lib1, processed_lib2,
                         CosineGreedy(tolerance=0.1))

# Find high-similarity pairs (potential duplicates or similar compounds)
threshold = 0.8
similar_pairs = []

for i, spec1 in enumerate(processed_lib1):
    for j, spec2 in enumerate(processed_lib2):
        score = scores.scores[i, j]
        if score >= threshold:
            similar_pairs.append({
                'lib1_idx': i,
                'lib2_idx': j,
                'lib1_name': spec1.get("compound_name", f"L1_{i}"),
                'lib2_name': spec2.get("compound_name", f"L2_{j}"),
                'similarity': score
            })

# Sort by similarity
similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)

print(f"\nFound {len(similar_pairs)} pairs with similarity >= {threshold}")
print("\nTop 10 most similar pairs:")
for pair in similar_pairs[:10]:
    print(f"{pair['lib1_name']} <-> {pair['lib2_name']}: {pair['similarity']:.4f}")

# Export to CSV
import pandas as pd
df = pd.DataFrame(similar_pairs)
df.to_csv("library_comparison.csv", index=False)
print("\nFull results saved to library_comparison.csv")
```

---

## Workflow 9: Ion Mode Specific Processing

Process positive and negative mode spectra separately.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import (default_filters, normalize_intensities,
                               require_correct_ionmode, derive_ionmode)
from matchms.exporting import save_as_mgf

# Load mixed mode spectra
spectra = list(load_from_mgf("mixed_modes.mgf"))

# Separate by ion mode
positive_spectra = []
negative_spectra = []
unknown_mode = []

for spectrum in spectra:
    # Harmonize and derive ion mode
    spectrum = default_filters(spectrum)
    spectrum = derive_ionmode(spectrum)

    # Separate by mode
    ionmode = spectrum.get("ionmode")

    if ionmode == "positive":
        spectrum = normalize_intensities(spectrum)
        positive_spectra.append(spectrum)
    elif ionmode == "negative":
        spectrum = normalize_intensities(spectrum)
        negative_spectra.append(spectrum)
    else:
        unknown_mode.append(spectrum)

print(f"Positive mode: {len(positive_spectra)}")
print(f"Negative mode: {len(negative_spectra)}")
print(f"Unknown mode: {len(unknown_mode)}")

# Save separated data
save_as_mgf(positive_spectra, "positive_mode.mgf")
save_as_mgf(negative_spectra, "negative_mode.mgf")

# Process mode-specific analyses
from matchms import calculate_scores
from matchms.similarity import CosineGreedy

if len(positive_spectra) > 1:
    print("\nCalculating positive mode similarities...")
    pos_scores = calculate_scores(positive_spectra, positive_spectra,
                                  CosineGreedy(tolerance=0.1))

if len(negative_spectra) > 1:
    print("Calculating negative mode similarities...")
    neg_scores = calculate_scores(negative_spectra, negative_spectra,
                                  CosineGreedy(tolerance=0.1))
```

---

## Workflow 10: Automated Compound Identification Report

Generate a detailed compound identification report.

```python
from matchms.importing import load_from_mgf
from matchms.filtering import default_filters, normalize_intensities
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine
import pandas as pd

def identify_compounds(query_file, library_file, output_csv="identification_report.csv"):
    """
    Automated compound identification with detailed report
    """
    # Load data
    print("Loading data...")
    queries = list(load_from_mgf(query_file))
    library = list(load_from_mgf(library_file))

    # Process
    proc_queries = [normalize_intensities(default_filters(s)) for s in queries]
    proc_library = [normalize_intensities(default_filters(s)) for s in library]

    # Calculate similarities
    print("Calculating similarities...")
    cosine_scores = calculate_scores(proc_library, proc_queries, CosineGreedy())
    modified_scores = calculate_scores(proc_library, proc_queries, ModifiedCosine())

    # Generate report
    results = []
    for i, query in enumerate(proc_queries):
        query_name = query.get("compound_name", f"Unknown_{i}")
        query_mz = query.get("precursor_mz", "N/A")

        # Get top 5 matches
        cosine_matches = cosine_scores.scores_by_query(query, sort=True)[:5]

        for rank, (lib_idx, cos_score) in enumerate(cosine_matches, 1):
            ref = proc_library[lib_idx]
            mod_score = modified_scores.scores[lib_idx, i]

            results.append({
                'Query': query_name,
                'Query_mz': query_mz,
                'Rank': rank,
                'Match': ref.get("compound_name", f"Ref_{lib_idx}"),
                'Match_mz': ref.get("precursor_mz", "N/A"),
                'Cosine_Score': cos_score,
                'Modified_Cosine': mod_score,
                'InChIKey': ref.get("inchikey", "N/A")
            })

    # Create DataFrame and save
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\nReport saved to {output_csv}")

    # Summary statistics
    print("\nSummary:")
    high_confidence = len(df[df['Cosine_Score'] >= 0.8])
    medium_confidence = len(df[(df['Cosine_Score'] >= 0.6) & (df['Cosine_Score'] < 0.8)])
    low_confidence = len(df[df['Cosine_Score'] < 0.6])

    print(f"  High confidence (≥0.8): {high_confidence}")
    print(f"  Medium confidence (0.6-0.8): {medium_confidence}")
    print(f"  Low confidence (<0.6): {low_confidence}")

    return df

# Run identification
report = identify_compounds("unknowns.mgf", "reference_library.mgf")
```

---

## Best Practices

1. **Always process both queries and references**: Apply the same filters to ensure consistent comparison
2. **Save intermediate results**: Use pickle format for fast reloading of processed spectra
3. **Monitor memory usage**: Use generators for large files instead of loading all at once
4. **Validate data quality**: Apply quality filters before similarity calculations
5. **Choose appropriate similarity metrics**: CosineGreedy for speed, ModifiedCosine for related compounds
6. **Combine multiple metrics**: Use multiple similarity scores for robust identification
7. **Filter by precursor mass first**: Dramatically speeds up large library searches
8. **Document your pipeline**: Save processing parameters for reproducibility

## Further Resources

- matchms documentation: https://matchms.readthedocs.io
- GNPS platform: https://gnps.ucsd.edu
- matchms GitHub: https://github.com/matchms/matchms
