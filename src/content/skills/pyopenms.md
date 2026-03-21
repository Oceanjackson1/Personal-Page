---
title: "Pyopenms"
description: "Complete mass spectrometry analysis platform. Use for proteomics workflows feature detection, peptide identification, protein quantification, and complex LC-MS/MS pipelines. Supports extensive file formats and algorithms. Best for proteomics, comp..."
category: "devops"
source: "community"
author: "Community"
tags: ["pyopenms"]
date: 2026-03-20
---

# PyOpenMS

## Overview

PyOpenMS provides Python bindings to the OpenMS library for computational mass spectrometry, enabling analysis of proteomics and metabolomics data. Use for handling mass spectrometry file formats, processing spectral data, detecting features, identifying peptides/proteins, and performing quantitative analysis.

## Installation

Install using uv:

```bash
uv uv pip install pyopenms
```

Verify installation:

```python
import pyopenms
print(pyopenms.__version__)
```

## Core Capabilities

PyOpenMS organizes functionality into these domains:

### 1. File I/O and Data Formats

Handle mass spectrometry file formats and convert between representations.

**Supported formats**: mzML, mzXML, TraML, mzTab, FASTA, pepXML, protXML, mzIdentML, featureXML, consensusXML, idXML

Basic file reading:

```python
import pyopenms as ms

# Read mzML file
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Access spectra
for spectrum in exp:
    mz, intensity = spectrum.get_peaks()
    print(f"Spectrum: {len(mz)} peaks")
```

**For detailed file handling**: See `references/file_io.md`

### 2. Signal Processing

Process raw spectral data with smoothing, filtering, centroiding, and normalization.

Basic spectrum processing:

```python
# Smooth spectrum with Gaussian filter
gaussian = ms.GaussFilter()
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.1)
gaussian.setParameters(params)
gaussian.filterExperiment(exp)
```

**For algorithm details**: See `references/signal_processing.md`

### 3. Feature Detection

Detect and link features across spectra and samples for quantitative analysis.

```python
# Detect features
ff = ms.FeatureFinder()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

**For complete workflows**: See `references/feature_detection.md`

### 4. Peptide and Protein Identification

Integrate with search engines and process identification results.

**Supported engines**: Comet, Mascot, MSGFPlus, XTandem, OMSSA, Myrimatch

Basic identification workflow:

```python
# Load identification data
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Apply FDR filtering
fdr = ms.FalseDiscoveryRate()
fdr.apply(peptide_ids)
```

**For detailed workflows**: See `references/identification.md`

### 5. Metabolomics Analysis

Perform untargeted metabolomics preprocessing and analysis.

Typical workflow:
1. Load and process raw data
2. Detect features
3. Align retention times across samples
4. Link features to consensus map
5. Annotate with compound databases

**For complete metabolomics workflows**: See `references/metabolomics.md`

## Data Structures

PyOpenMS uses these primary objects:

- **MSExperiment**: Collection of spectra and chromatograms
- **MSSpectrum**: Single mass spectrum with m/z and intensity pairs
- **MSChromatogram**: Chromatographic trace
- **Feature**: Detected chromatographic peak with quality metrics
- **FeatureMap**: Collection of features
- **PeptideIdentification**: Search results for peptides
- **ProteinIdentification**: Search results for proteins

**For detailed documentation**: See `references/data_structures.md`

## Common Workflows

### Quick Start: Load and Explore Data

```python
import pyopenms as ms

# Load mzML file
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# Get basic statistics
print(f"Number of spectra: {exp.getNrSpectra()}")
print(f"Number of chromatograms: {exp.getNrChromatograms()}")

# Examine first spectrum
spec = exp.getSpectrum(0)
print(f"MS level: {spec.getMSLevel()}")
print(f"Retention time: {spec.getRT()}")
mz, intensity = spec.get_peaks()
print(f"Peaks: {len(mz)}")
```

### Parameter Management

Most algorithms use a parameter system:

```python
# Get algorithm parameters
algo = ms.GaussFilter()
params = algo.getParameters()

# View available parameters
for param in params.keys():
    print(f"{param}: {params.getValue(param)}")

# Modify parameters
params.setValue("gaussian_width", 0.2)
algo.setParameters(params)
```

### Export to Pandas

Convert data to pandas DataFrames for analysis:

```python
import pyopenms as ms
import pandas as pd

# Load feature map
fm = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", fm)

# Convert to DataFrame
df = fm.get_df()
print(df.head())
```

## Integration with Other Tools

PyOpenMS integrates with:
- **Pandas**: Export data to DataFrames
- **NumPy**: Work with peak arrays
- **Scikit-learn**: Machine learning on MS data
- **Matplotlib/Seaborn**: Visualization
- **R**: Via rpy2 bridge

## Resources

- **Official documentation**: https://pyopenms.readthedocs.io
- **OpenMS documentation**: https://www.openms.org
- **GitHub**: https://github.com/OpenMS/OpenMS

## References

- `references/file_io.md` - Comprehensive file format handling
- `references/signal_processing.md` - Signal processing algorithms
- `references/feature_detection.md` - Feature detection and linking
- `references/identification.md` - Peptide and protein identification
- `references/metabolomics.md` - Metabolomics-specific workflows
- `references/data_structures.md` - Core objects and data structures

---

## Reference: Data_Structures

# Core Data Structures

## Overview

PyOpenMS uses C++ objects with Python bindings. Understanding these core data structures is essential for effective data manipulation.

## Spectrum and Experiment Objects

### MSExperiment

Container for complete LC-MS experiment data (spectra and chromatograms).

```python
import pyopenms as ms

# Create experiment
exp = ms.MSExperiment()

# Load from file
ms.MzMLFile().load("data.mzML", exp)

# Access properties
print(f"Number of spectra: {exp.getNrSpectra()}")
print(f"Number of chromatograms: {exp.getNrChromatograms()}")

# Get RT range
rts = [spec.getRT() for spec in exp]
print(f"RT range: {min(rts):.1f} - {max(rts):.1f} seconds")

# Access individual spectrum
spec = exp.getSpectrum(0)

# Iterate through spectra
for spec in exp:
    if spec.getMSLevel() == 2:
        print(f"MS2 spectrum at RT {spec.getRT():.2f}")

# Get metadata
exp_settings = exp.getExperimentalSettings()
instrument = exp_settings.getInstrument()
print(f"Instrument: {instrument.getName()}")
```

### MSSpectrum

Individual mass spectrum with m/z and intensity arrays.

```python
# Create empty spectrum
spec = ms.MSSpectrum()

# Get from experiment
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)
spec = exp.getSpectrum(0)

# Basic properties
print(f"MS level: {spec.getMSLevel()}")
print(f"Retention time: {spec.getRT():.2f} seconds")
print(f"Number of peaks: {spec.size()}")

# Get peak data as numpy arrays
mz, intensity = spec.get_peaks()
print(f"m/z range: {mz.min():.2f} - {mz.max():.2f}")
print(f"Max intensity: {intensity.max():.0f}")

# Access individual peaks
for i in range(min(5, spec.size())):  # First 5 peaks
    print(f"Peak {i}: m/z={mz[i]:.4f}, intensity={intensity[i]:.0f}")

# Precursor information (for MS2)
if spec.getMSLevel() == 2:
    precursors = spec.getPrecursors()
    if precursors:
        precursor = precursors[0]
        print(f"Precursor m/z: {precursor.getMZ():.4f}")
        print(f"Precursor charge: {precursor.getCharge()}")
        print(f"Precursor intensity: {precursor.getIntensity():.0f}")

# Set peak data
new_mz = [100.0, 200.0, 300.0]
new_intensity = [1000.0, 2000.0, 1500.0]
spec.set_peaks((new_mz, new_intensity))
```

### MSChromatogram

Chromatographic trace (TIC, XIC, or SRM transition).

```python
# Access chromatogram from experiment
for chrom in exp.getChromatograms():
    print(f"Chromatogram ID: {chrom.getNativeID()}")

    # Get data
    rt, intensity = chrom.get_peaks()

    print(f"  RT points: {len(rt)}")
    print(f"  Max intensity: {intensity.max():.0f}")

    # Precursor info (for XIC)
    precursor = chrom.getPrecursor()
    print(f"  Precursor m/z: {precursor.getMZ():.4f}")
```

## Feature Objects

### Feature

Detected chromatographic peak with 2D spatial extent (RT-m/z).

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access individual feature
feature = feature_map[0]

# Core properties
print(f"m/z: {feature.getMZ():.4f}")
print(f"RT: {feature.getRT():.2f} seconds")
print(f"Intensity: {feature.getIntensity():.0f}")
print(f"Charge: {feature.getCharge()}")

# Quality metrics
print(f"Overall quality: {feature.getOverallQuality():.3f}")
print(f"Width (RT): {feature.getWidth():.2f}")

# Convex hull (spatial extent)
hull = feature.getConvexHull()
print(f"Hull points: {hull.getHullPoints().size()}")

# Bounding box
bbox = hull.getBoundingBox()
print(f"RT range: {bbox.minPosition()[0]:.2f} - {bbox.maxPosition()[0]:.2f}")
print(f"m/z range: {bbox.minPosition()[1]:.4f} - {bbox.maxPosition()[1]:.4f}")

# Subordinate features (isotopes)
subordinates = feature.getSubordinates()
if subordinates:
    print(f"Isotopic features: {len(subordinates)}")
    for sub in subordinates:
        print(f"  m/z: {sub.getMZ():.4f}, intensity: {sub.getIntensity():.0f}")

# Metadata values
if feature.metaValueExists("label"):
    label = feature.getMetaValue("label")
    print(f"Label: {label}")
```

### FeatureMap

Collection of features from a single LC-MS run.

```python
# Create feature map
feature_map = ms.FeatureMap()

# Load from file
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access properties
print(f"Number of features: {feature_map.size()}")

# Get unique features
print(f"Unique features: {feature_map.getUniqueId()}")

# Metadata
primary_path = feature_map.getPrimaryMSRunPath()
if primary_path:
    print(f"Source file: {primary_path[0].decode()}")

# Iterate through features
for feature in feature_map:
    print(f"Feature: m/z={feature.getMZ():.4f}, RT={feature.getRT():.2f}")

# Add new feature
new_feature = ms.Feature()
new_feature.setMZ(500.0)
new_feature.setRT(300.0)
new_feature.setIntensity(10000.0)
feature_map.push_back(new_feature)

# Sort features
feature_map.sortByRT()  # or sortByMZ(), sortByIntensity()

# Export to pandas
df = feature_map.get_df()
print(df.head())
```

### ConsensusFeature

Feature linked across multiple samples.

```python
# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Access consensus feature
cons_feature = consensus_map[0]

# Consensus properties
print(f"Consensus m/z: {cons_feature.getMZ():.4f}")
print(f"Consensus RT: {cons_feature.getRT():.2f}")
print(f"Consensus intensity: {cons_feature.getIntensity():.0f}")

# Get feature handles (individual map features)
feature_list = cons_feature.getFeatureList()
print(f"Present in {len(feature_list)} maps")

for handle in feature_list:
    map_idx = handle.getMapIndex()
    intensity = handle.getIntensity()
    mz = handle.getMZ()
    rt = handle.getRT()

    print(f"  Map {map_idx}: m/z={mz:.4f}, RT={rt:.2f}, intensity={intensity:.0f}")

# Get unique ID in originating map
for handle in feature_list:
    unique_id = handle.getUniqueId()
    print(f"Unique ID: {unique_id}")
```

### ConsensusMap

Collection of consensus features across samples.

```python
# Create consensus map
consensus_map = ms.ConsensusMap()

# Load from file
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Access properties
print(f"Consensus features: {consensus_map.size()}")

# Column headers (file descriptions)
headers = consensus_map.getColumnHeaders()
print(f"Number of files: {len(headers)}")

for map_idx, description in headers.items():
    print(f"Map {map_idx}:")
    print(f"  Filename: {description.filename}")
    print(f"  Label: {description.label}")
    print(f"  Size: {description.size}")

# Iterate through consensus features
for cons_feature in consensus_map:
    print(f"Consensus feature: m/z={cons_feature.getMZ():.4f}")

# Export to DataFrame
df = consensus_map.get_df()
```

## Identification Objects

### PeptideIdentification

Identification results for a single spectrum.

```python
# Load identifications
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Access peptide identification
peptide_id = peptide_ids[0]

# Spectrum metadata
print(f"RT: {peptide_id.getRT():.2f}")
print(f"m/z: {peptide_id.getMZ():.4f}")

# Identification metadata
print(f"Identifier: {peptide_id.getIdentifier()}")
print(f"Score type: {peptide_id.getScoreType()}")
print(f"Higher score better: {peptide_id.isHigherScoreBetter()}")

# Get peptide hits
hits = peptide_id.getHits()
print(f"Number of hits: {len(hits)}")

for hit in hits:
    print(f"  Sequence: {hit.getSequence().toString()}")
    print(f"  Score: {hit.getScore()}")
    print(f"  Charge: {hit.getCharge()}")
```

### PeptideHit

Individual peptide match to a spectrum.

```python
# Access hit
hit = peptide_id.getHits()[0]

# Sequence information
sequence = hit.getSequence()
print(f"Sequence: {sequence.toString()}")
print(f"Mass: {sequence.getMonoWeight():.4f}")

# Score and rank
print(f"Score: {hit.getScore()}")
print(f"Rank: {hit.getRank()}")

# Charge state
print(f"Charge: {hit.getCharge()}")

# Protein accessions
accessions = hit.extractProteinAccessionsSet()
for acc in accessions:
    print(f"Protein: {acc.decode()}")

# Meta values (additional scores, errors)
if hit.metaValueExists("MS:1002252"):  # mass error
    mass_error = hit.getMetaValue("MS:1002252")
    print(f"Mass error: {mass_error:.4f} ppm")
```

### ProteinIdentification

Protein-level identification information.

```python
# Access protein identification
protein_id = protein_ids[0]

# Search engine info
print(f"Search engine: {protein_id.getSearchEngine()}")
print(f"Search engine version: {protein_id.getSearchEngineVersion()}")

# Search parameters
search_params = protein_id.getSearchParameters()
print(f"Database: {search_params.db}")
print(f"Enzyme: {search_params.digestion_enzyme.getName()}")
print(f"Missed cleavages: {search_params.missed_cleavages}")
print(f"Precursor tolerance: {search_params.precursor_mass_tolerance}")

# Protein hits
hits = protein_id.getHits()
for hit in hits:
    print(f"Accession: {hit.getAccession()}")
    print(f"Score: {hit.getScore()}")
    print(f"Coverage: {hit.getCoverage():.1f}%")
```

### ProteinHit

Individual protein identification.

```python
# Access protein hit
protein_hit = protein_id.getHits()[0]

# Protein information
print(f"Accession: {protein_hit.getAccession()}")
print(f"Description: {protein_hit.getDescription()}")
print(f"Sequence: {protein_hit.getSequence()}")

# Scoring
print(f"Score: {protein_hit.getScore()}")
print(f"Coverage: {protein_hit.getCoverage():.1f}%")

# Rank
print(f"Rank: {protein_hit.getRank()}")
```

## Sequence Objects

### AASequence

Amino acid sequence with modifications.

```python
# Create sequence from string
seq = ms.AASequence.fromString("PEPTIDE")

# Basic properties
print(f"Sequence: {seq.toString()}")
print(f"Length: {seq.size()}")
print(f"Monoisotopic mass: {seq.getMonoWeight():.4f}")
print(f"Average mass: {seq.getAverageWeight():.4f}")

# Individual residues
for i in range(seq.size()):
    residue = seq.getResidue(i)
    print(f"Position {i}: {residue.getOneLetterCode()}")
    print(f"  Mass: {residue.getMonoWeight():.4f}")
    print(f"  Formula: {residue.getFormula().toString()}")

# Modified sequence
mod_seq = ms.AASequence.fromString("PEPTIDEM(Oxidation)K")
print(f"Modified: {mod_seq.isModified()}")

# Check modifications
for i in range(mod_seq.size()):
    residue = mod_seq.getResidue(i)
    if residue.isModified():
        print(f"Modification at {i}: {residue.getModificationName()}")

# N-terminal and C-terminal modifications
term_mod_seq = ms.AASequence.fromString("(Acetyl)PEPTIDE(Amidated)")
```

### EmpiricalFormula

Molecular formula representation.

```python
# Create formula
formula = ms.EmpiricalFormula("C6H12O6")  # Glucose

# Properties
print(f"Formula: {formula.toString()}")
print(f"Monoisotopic mass: {formula.getMonoWeight():.4f}")
print(f"Average mass: {formula.getAverageWeight():.4f}")

# Element composition
print(f"Carbon atoms: {formula.getNumberOf(b'C')}")
print(f"Hydrogen atoms: {formula.getNumberOf(b'H')}")
print(f"Oxygen atoms: {formula.getNumberOf(b'O')}")

# Arithmetic operations
formula2 = ms.EmpiricalFormula("H2O")
combined = formula + formula2  # Add water
print(f"Combined: {combined.toString()}")
```

## Parameter Objects

### Param

Generic parameter container used by algorithms.

```python
# Get algorithm parameters
algo = ms.GaussFilter()
params = algo.getParameters()

# List all parameters
for key in params.keys():
    value = params.getValue(key)
    print(f"{key}: {value}")

# Get specific parameter
gaussian_width = params.getValue("gaussian_width")
print(f"Gaussian width: {gaussian_width}")

# Set parameter
params.setValue("gaussian_width", 0.2)

# Apply modified parameters
algo.setParameters(params)

# Copy parameters
params_copy = ms.Param(params)
```

## Best Practices

### Memory Management

```python
# For large files, use indexed access instead of full loading
indexed_mzml = ms.IndexedMzMLFileLoader()
indexed_mzml.load("large_file.mzML")

# Access specific spectrum without loading entire file
spec = indexed_mzml.getSpectrumById(100)
```

### Type Conversion

```python
# Convert peak arrays to numpy
import numpy as np

mz, intensity = spec.get_peaks()
# These are already numpy arrays

# Can perform numpy operations
filtered_mz = mz[intensity > 1000]
```

### Object Copying

```python
# Create deep copy
exp_copy = ms.MSExperiment(exp)

# Modifications to copy don't affect original
```

---

## Reference: Feature_Detection

# Feature Detection and Linking

## Overview

Feature detection identifies persistent signals (chromatographic peaks) in LC-MS data. Feature linking combines features across multiple samples for quantitative comparison.

## Feature Detection Basics

A feature represents a chromatographic peak characterized by:
- m/z value (mass-to-charge ratio)
- Retention time (RT)
- Intensity
- Quality score
- Convex hull (spatial extent in RT-m/z space)

## Feature Finding

### Feature Finder Multiples (FFM)

Standard algorithm for feature detection in centroided data:

```python
import pyopenms as ms

# Load centroided data
exp = ms.MSExperiment()
ms.MzMLFile().load("centroided.mzML", exp)

# Create feature finder
ff = ms.FeatureFinder()

# Get default parameters
params = ff.getParameters("centroided")

# Modify key parameters
params.setValue("mass_trace:mz_tolerance", 10.0)  # ppm
params.setValue("mass_trace:min_spectra", 7)  # Min scans per feature
params.setValue("isotopic_pattern:charge_low", 1)
params.setValue("isotopic_pattern:charge_high", 4)

# Run feature detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())

print(f"Detected {features.size()} features")

# Save features
ms.FeatureXMLFile().store("features.featureXML", features)
```

### Feature Finder for Metabolomics

Optimized for small molecules:

```python
# Create feature finder for metabolomics
ff = ms.FeatureFinder()

# Get metabolomics-specific parameters
params = ff.getParameters("centroided")

# Configure for metabolomics
params.setValue("mass_trace:mz_tolerance", 5.0)  # Lower tolerance
params.setValue("mass_trace:min_spectra", 5)
params.setValue("isotopic_pattern:charge_low", 1)  # Mostly singly charged
params.setValue("isotopic_pattern:charge_high", 2)

# Run detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

## Accessing Feature Data

### Iterate Through Features

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access individual features
for feature in feature_map:
    print(f"m/z: {feature.getMZ():.4f}")
    print(f"RT: {feature.getRT():.2f}")
    print(f"Intensity: {feature.getIntensity():.0f}")
    print(f"Charge: {feature.getCharge()}")
    print(f"Quality: {feature.getOverallQuality():.3f}")
    print(f"Width (RT): {feature.getWidth():.2f}")

    # Get convex hull
    hull = feature.getConvexHull()
    print(f"Hull points: {hull.getHullPoints().size()}")
```

### Feature Subordinates (Isotope Pattern)

```python
# Access isotopic pattern
for feature in feature_map:
    # Get subordinate features (isotopes)
    subordinates = feature.getSubordinates()

    if subordinates:
        print(f"Main feature m/z: {feature.getMZ():.4f}")
        for sub in subordinates:
            print(f"  Isotope m/z: {sub.getMZ():.4f}")
            print(f"  Isotope intensity: {sub.getIntensity():.0f}")
```

### Export to Pandas

```python
import pandas as pd

# Convert to DataFrame
df = feature_map.get_df()

print(df.columns)
# Typical columns: RT, mz, intensity, charge, quality

# Analyze features
print(f"Mean intensity: {df['intensity'].mean()}")
print(f"RT range: {df['RT'].min():.1f} - {df['RT'].max():.1f}")
```

## Feature Linking

### Map Alignment

Align retention times before linking:

```python
# Load multiple feature maps
fm1 = ms.FeatureMap()
fm2 = ms.FeatureMap()
ms.FeatureXMLFile().load("sample1.featureXML", fm1)
ms.FeatureXMLFile().load("sample2.featureXML", fm2)

# Create aligner
aligner = ms.MapAlignmentAlgorithmPoseClustering()

# Align maps
fm_aligned = []
transformations = []
aligner.align([fm1, fm2], fm_aligned, transformations)
```

### Feature Linking Algorithm

Link features across samples:

```python
# Create feature grouping algorithm
grouper = ms.FeatureGroupingAlgorithmQT()

# Configure parameters
params = grouper.getParameters()
params.setValue("distance_RT:max_difference", 30.0)  # Max RT difference (s)
params.setValue("distance_MZ:max_difference", 10.0)  # Max m/z difference (ppm)
params.setValue("distance_MZ:unit", "ppm")
grouper.setParameters(params)

# Prepare feature maps
feature_maps = [fm1, fm2, fm3]

# Create consensus map
consensus_map = ms.ConsensusMap()

# Link features
grouper.group(feature_maps, consensus_map)

print(f"Created {consensus_map.size()} consensus features")

# Save consensus map
ms.ConsensusXMLFile().store("consensus.consensusXML", consensus_map)
```

## Consensus Features

### Access Consensus Data

```python
# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Iterate through consensus features
for cons_feature in consensus_map:
    print(f"Consensus m/z: {cons_feature.getMZ():.4f}")
    print(f"Consensus RT: {cons_feature.getRT():.2f}")

    # Get features from individual maps
    for handle in cons_feature.getFeatureList():
        map_idx = handle.getMapIndex()
        intensity = handle.getIntensity()
        print(f"  Sample {map_idx}: intensity {intensity:.0f}")
```

### Consensus Map Metadata

```python
# Access file descriptions (map metadata)
file_descriptions = consensus_map.getColumnHeaders()

for map_idx, description in file_descriptions.items():
    print(f"Map {map_idx}:")
    print(f"  Filename: {description.filename}")
    print(f"  Label: {description.label}")
    print(f"  Size: {description.size}")
```

## Adduct Detection

Identify different ionization forms of the same molecule:

```python
# Create adduct detector
adduct_detector = ms.MetaboliteAdductDecharger()

# Configure parameters
params = adduct_detector.getParameters()
params.setValue("potential_adducts", "[M+H]+,[M+Na]+,[M+K]+,[M-H]-")
params.setValue("charge_min", 1)
params.setValue("charge_max", 1)
params.setValue("max_neutrals", 1)
adduct_detector.setParameters(params)

# Detect adducts
feature_map_out = ms.FeatureMap()
adduct_detector.compute(feature_map, feature_map_out, ms.ConsensusMap())
```

## Complete Feature Detection Workflow

### End-to-End Example

```python
import pyopenms as ms

def feature_detection_workflow(input_files, output_consensus):
    """
    Complete workflow: feature detection and linking across samples.

    Args:
        input_files: List of mzML file paths
        output_consensus: Output consensusXML file path
    """

    feature_maps = []

    # Step 1: Detect features in each file
    for mzml_file in input_files:
        print(f"Processing {mzml_file}...")

        # Load experiment
        exp = ms.MSExperiment()
        ms.MzMLFile().load(mzml_file, exp)

        # Find features
        ff = ms.FeatureFinder()
        params = ff.getParameters("centroided")
        params.setValue("mass_trace:mz_tolerance", 10.0)
        params.setValue("mass_trace:min_spectra", 7)

        features = ms.FeatureMap()
        ff.run("centroided", exp, features, params, ms.FeatureMap())

        # Store filename in feature map
        features.setPrimaryMSRunPath([mzml_file.encode()])

        feature_maps.append(features)
        print(f"  Found {features.size()} features")

    # Step 2: Align retention times
    print("Aligning retention times...")
    aligner = ms.MapAlignmentAlgorithmPoseClustering()
    aligned_maps = []
    transformations = []
    aligner.align(feature_maps, aligned_maps, transformations)

    # Step 3: Link features
    print("Linking features across samples...")
    grouper = ms.FeatureGroupingAlgorithmQT()
    params = grouper.getParameters()
    params.setValue("distance_RT:max_difference", 30.0)
    params.setValue("distance_MZ:max_difference", 10.0)
    params.setValue("distance_MZ:unit", "ppm")
    grouper.setParameters(params)

    consensus_map = ms.ConsensusMap()
    grouper.group(aligned_maps, consensus_map)

    # Save results
    ms.ConsensusXMLFile().store(output_consensus, consensus_map)

    print(f"Created {consensus_map.size()} consensus features")
    print(f"Results saved to {output_consensus}")

    return consensus_map

# Run workflow
input_files = ["sample1.mzML", "sample2.mzML", "sample3.mzML"]
consensus = feature_detection_workflow(input_files, "consensus.consensusXML")
```

## Feature Filtering

### Filter by Quality

```python
# Filter features by quality score
filtered_features = ms.FeatureMap()

for feature in feature_map:
    if feature.getOverallQuality() > 0.5:  # Quality threshold
        filtered_features.push_back(feature)

print(f"Kept {filtered_features.size()} high-quality features")
```

### Filter by Intensity

```python
# Keep only intense features
min_intensity = 10000

filtered_features = ms.FeatureMap()
for feature in feature_map:
    if feature.getIntensity() >= min_intensity:
        filtered_features.push_back(feature)
```

### Filter by m/z Range

```python
# Extract features in specific m/z range
mz_min = 200.0
mz_max = 800.0

filtered_features = ms.FeatureMap()
for feature in feature_map:
    mz = feature.getMZ()
    if mz_min <= mz <= mz_max:
        filtered_features.push_back(feature)
```

## Feature Annotation

### Add Identification Information

```python
# Annotate features with peptide identifications
# Load identifications
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Create ID mapper
mapper = ms.IDMapper()

# Map IDs to features
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotations
for feature in feature_map:
    peptide_ids_for_feature = feature.getPeptideIdentifications()
    if peptide_ids_for_feature:
        print(f"Feature at {feature.getMZ():.4f} m/z identified")
```

## Best Practices

### Parameter Optimization

Optimize parameters for your data type:

```python
# Test different tolerance values
mz_tolerances = [5.0, 10.0, 20.0]  # ppm

for tol in mz_tolerances:
    ff = ms.FeatureFinder()
    params = ff.getParameters("centroided")
    params.setValue("mass_trace:mz_tolerance", tol)

    features = ms.FeatureMap()
    ff.run("centroided", exp, features, params, ms.FeatureMap())

    print(f"Tolerance {tol} ppm: {features.size()} features")
```

### Visual Inspection

Export features for visualization:

```python
# Convert to DataFrame for plotting
df = feature_map.get_df()

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(df['RT'], df['mz'], s=df['intensity']/1000, alpha=0.5)
plt.xlabel('Retention Time (s)')
plt.ylabel('m/z')
plt.title('Feature Map')
plt.colorbar(label='Intensity (scaled)')
plt.show()
```

---

## Reference: File_Io

# File I/O and Data Formats

## Overview

PyOpenMS supports multiple mass spectrometry file formats for reading and writing. This guide covers file handling strategies and format-specific operations.

## Supported Formats

### Spectrum Data Formats

- **mzML**: Standard XML-based format for mass spectrometry data
- **mzXML**: Earlier XML-based format
- **mzData**: XML format (deprecated but supported)

### Identification Formats

- **idXML**: OpenMS native identification format
- **mzIdentML**: Standard XML format for identification data
- **pepXML**: X! Tandem format
- **protXML**: Protein identification format

### Feature and Quantitation Formats

- **featureXML**: OpenMS format for detected features
- **consensusXML**: Format for consensus features across samples
- **mzTab**: Tab-delimited format for reporting

### Sequence and Library Formats

- **FASTA**: Protein/peptide sequences
- **TraML**: Transition lists for targeted experiments

## Reading mzML Files

### In-Memory Loading

Load entire file into memory (suitable for smaller files):

```python
import pyopenms as ms

# Create experiment container
exp = ms.MSExperiment()

# Load file
ms.MzMLFile().load("sample.mzML", exp)

# Access data
print(f"Spectra: {exp.getNrSpectra()}")
print(f"Chromatograms: {exp.getNrChromatograms()}")
```

### Indexed Access

Efficient random access for large files:

```python
# Create indexed access
indexed_mzml = ms.IndexedMzMLFileLoader()
indexed_mzml.load("large_file.mzML")

# Get specific spectrum by index
spec = indexed_mzml.getSpectrumById(100)

# Access by native ID
spec = indexed_mzml.getSpectrumByNativeId("scan=5000")
```

### Streaming Access

Memory-efficient processing for very large files:

```python
# Define consumer function
class SpectrumProcessor(ms.MSExperimentConsumer):
    def __init__(self):
        super().__init__()
        self.count = 0

    def consumeSpectrum(self, spec):
        # Process spectrum
        if spec.getMSLevel() == 2:
            self.count += 1

# Stream file
consumer = SpectrumProcessor()
ms.MzMLFile().transform("large.mzML", consumer)
print(f"Processed {consumer.count} MS2 spectra")
```

### Cached Access

Balance between memory usage and speed:

```python
# Use on-disk caching
options = ms.CachedmzML()
options.setMetaDataOnly(False)

exp = ms.MSExperiment()
ms.CachedmzMLHandler().load("sample.mzML", exp, options)
```

## Writing mzML Files

### Basic Writing

```python
# Create or modify experiment
exp = ms.MSExperiment()
# ... add spectra ...

# Write to file
ms.MzMLFile().store("output.mzML", exp)
```

### Compression Options

```python
# Configure compression
file_handler = ms.MzMLFile()

options = ms.PeakFileOptions()
options.setCompression(True)  # Enable compression
file_handler.setOptions(options)

file_handler.store("compressed.mzML", exp)
```

## Reading Identification Data

### idXML Format

```python
# Load identification results
protein_ids = []
peptide_ids = []

ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Access peptide identifications
for peptide_id in peptide_ids:
    print(f"RT: {peptide_id.getRT()}")
    print(f"MZ: {peptide_id.getMZ()}")

    # Get peptide hits
    for hit in peptide_id.getHits():
        print(f"  Sequence: {hit.getSequence().toString()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Charge: {hit.getCharge()}")
```

### mzIdentML Format

```python
# Read mzIdentML
protein_ids = []
peptide_ids = []

ms.MzIdentMLFile().load("results.mzid", protein_ids, peptide_ids)
```

### pepXML Format

```python
# Load pepXML
protein_ids = []
peptide_ids = []

ms.PepXMLFile().load("results.pep.xml", protein_ids, peptide_ids)
```

## Reading Feature Data

### featureXML

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access features
for feature in feature_map:
    print(f"RT: {feature.getRT()}")
    print(f"MZ: {feature.getMZ()}")
    print(f"Intensity: {feature.getIntensity()}")
    print(f"Quality: {feature.getOverallQuality()}")
```

### consensusXML

```python
# Load consensus features
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Access consensus features
for consensus_feature in consensus_map:
    print(f"RT: {consensus_feature.getRT()}")
    print(f"MZ: {consensus_feature.getMZ()}")

    # Get feature handles (sub-features from different maps)
    for handle in consensus_feature.getFeatureList():
        map_index = handle.getMapIndex()
        intensity = handle.getIntensity()
        print(f"  Map {map_index}: {intensity}")
```

## Reading FASTA Files

```python
# Load protein sequences
fasta_entries = []
ms.FASTAFile().load("database.fasta", fasta_entries)

for entry in fasta_entries:
    print(f"Identifier: {entry.identifier}")
    print(f"Description: {entry.description}")
    print(f"Sequence: {entry.sequence}")
```

## Reading TraML Files

```python
# Load transition lists for targeted experiments
targeted_exp = ms.TargetedExperiment()
ms.TraMLFile().load("transitions.TraML", targeted_exp)

# Access transitions
for transition in targeted_exp.getTransitions():
    print(f"Precursor MZ: {transition.getPrecursorMZ()}")
    print(f"Product MZ: {transition.getProductMZ()}")
```

## Writing mzTab Files

```python
# Create mzTab for reporting
mztab = ms.MzTab()

# Add metadata
metadata = mztab.getMetaData()
metadata.mz_tab_version.set("1.0.0")
metadata.title.set("Proteomics Analysis Results")

# Add protein data
protein_section = mztab.getProteinSectionRows()
# ... populate protein data ...

# Write to file
ms.MzTabFile().store("report.mzTab", mztab)
```

## Format Conversion

### mzXML to mzML

```python
# Read mzXML
exp = ms.MSExperiment()
ms.MzXMLFile().load("data.mzXML", exp)

# Write as mzML
ms.MzMLFile().store("data.mzML", exp)
```

### Extract Chromatograms from mzML

```python
# Load experiment
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Extract specific chromatogram
for chrom in exp.getChromatograms():
    if chrom.getNativeID() == "TIC":
        rt, intensity = chrom.get_peaks()
        print(f"TIC has {len(rt)} data points")
```

## File Metadata

### Access mzML Metadata

```python
# Load file
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# Get experimental settings
exp_settings = exp.getExperimentalSettings()

# Instrument info
instrument = exp_settings.getInstrument()
print(f"Instrument: {instrument.getName()}")
print(f"Model: {instrument.getModel()}")

# Sample info
sample = exp_settings.getSample()
print(f"Sample name: {sample.getName()}")

# Source files
for source_file in exp_settings.getSourceFiles():
    print(f"Source: {source_file.getNameOfFile()}")
```

## Best Practices

### Memory Management

For large files:
1. Use indexed or streaming access instead of full in-memory loading
2. Process data in chunks
3. Clear data structures when no longer needed

```python
# Good for large files
indexed_mzml = ms.IndexedMzMLFileLoader()
indexed_mzml.load("huge_file.mzML")

# Process spectra one at a time
for i in range(indexed_mzml.getNrSpectra()):
    spec = indexed_mzml.getSpectrumById(i)
    # Process spectrum
    # Spectrum automatically cleaned up after processing
```

### Error Handling

```python
try:
    exp = ms.MSExperiment()
    ms.MzMLFile().load("data.mzML", exp)
except Exception as e:
    print(f"Failed to load file: {e}")
```

### File Validation

```python
# Check if file exists and is readable
import os

if os.path.exists("data.mzML") and os.path.isfile("data.mzML"):
    exp = ms.MSExperiment()
    ms.MzMLFile().load("data.mzML", exp)
else:
    print("File not found")
```

---

## Reference: Identification

# Peptide and Protein Identification

## Overview

PyOpenMS supports peptide/protein identification through integration with search engines and provides tools for post-processing identification results including FDR control, protein inference, and annotation.

## Supported Search Engines

PyOpenMS integrates with these search engines:

- **Comet**: Fast tandem MS search
- **Mascot**: Commercial search engine
- **MSGFPlus**: Spectral probability-based search
- **XTandem**: Open-source search tool
- **OMSSA**: NCBI search engine
- **Myrimatch**: High-throughput search
- **MSFragger**: Ultra-fast search

## Reading Identification Data

### idXML Format

```python
import pyopenms as ms

# Load identification results
protein_ids = []
peptide_ids = []

ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

print(f"Protein identifications: {len(protein_ids)}")
print(f"Peptide identifications: {len(peptide_ids)}")
```

### Access Peptide Identifications

```python
# Iterate through peptide IDs
for peptide_id in peptide_ids:
    # Spectrum metadata
    print(f"RT: {peptide_id.getRT():.2f}")
    print(f"m/z: {peptide_id.getMZ():.4f}")

    # Get peptide hits (ranked by score)
    hits = peptide_id.getHits()
    print(f"Number of hits: {len(hits)}")

    for hit in hits:
        sequence = hit.getSequence()
        print(f"  Sequence: {sequence.toString()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Charge: {hit.getCharge()}")
        print(f"  Mass error (ppm): {hit.getMetaValue('mass_error_ppm')}")

        # Get modifications
        if sequence.isModified():
            for i in range(sequence.size()):
                residue = sequence.getResidue(i)
                if residue.isModified():
                    print(f"    Modification at position {i}: {residue.getModificationName()}")
```

### Access Protein Identifications

```python
# Access protein-level information
for protein_id in protein_ids:
    # Search parameters
    search_params = protein_id.getSearchParameters()
    print(f"Search engine: {protein_id.getSearchEngine()}")
    print(f"Database: {search_params.db}")

    # Protein hits
    hits = protein_id.getHits()
    for hit in hits:
        print(f"  Accession: {hit.getAccession()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Coverage: {hit.getCoverage()}")
        print(f"  Sequence: {hit.getSequence()}")
```

## False Discovery Rate (FDR)

### FDR Filtering

Apply FDR filtering to control false positives:

```python
# Create FDR object
fdr = ms.FalseDiscoveryRate()

# Apply FDR at PSM level
fdr.apply(peptide_ids)

# Filter by FDR threshold
fdr_threshold = 0.01  # 1% FDR
filtered_peptide_ids = []

for peptide_id in peptide_ids:
    # Keep hits below FDR threshold
    filtered_hits = []
    for hit in peptide_id.getHits():
        if hit.getScore() <= fdr_threshold:  # Lower score = better
            filtered_hits.append(hit)

    if filtered_hits:
        peptide_id.setHits(filtered_hits)
        filtered_peptide_ids.append(peptide_id)

print(f"Peptides passing FDR: {len(filtered_peptide_ids)}")
```

### Score Transformation

Convert scores to q-values:

```python
# Apply score transformation
fdr.apply(peptide_ids)

# Access q-values
for peptide_id in peptide_ids:
    for hit in peptide_id.getHits():
        q_value = hit.getMetaValue("q-value")
        print(f"Sequence: {hit.getSequence().toString()}, q-value: {q_value}")
```

## Protein Inference

### ID Mapper

Map peptide identifications to proteins:

```python
# Create mapper
mapper = ms.IDMapper()

# Map to features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Annotate features with IDs
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotated features
for feature in feature_map:
    pep_ids = feature.getPeptideIdentifications()
    if pep_ids:
        for pep_id in pep_ids:
            for hit in pep_id.getHits():
                print(f"Feature {feature.getMZ():.4f}: {hit.getSequence().toString()}")
```

### Protein Grouping

Group proteins by shared peptides:

```python
# Create protein inference algorithm
inference = ms.BasicProteinInferenceAlgorithm()

# Run inference
inference.run(peptide_ids, protein_ids)

# Access protein groups
for protein_id in protein_ids:
    hits = protein_id.getHits()
    if len(hits) > 1:
        print("Protein group:")
        for hit in hits:
            print(f"  {hit.getAccession()}")
```

## Peptide Sequence Handling

### AASequence Object

Work with peptide sequences:

```python
# Create peptide sequence
seq = ms.AASequence.fromString("PEPTIDE")

print(f"Sequence: {seq.toString()}")
print(f"Monoisotopic mass: {seq.getMonoWeight():.4f}")
print(f"Average mass: {seq.getAverageWeight():.4f}")
print(f"Length: {seq.size()}")

# Access individual amino acids
for i in range(seq.size()):
    residue = seq.getResidue(i)
    print(f"Position {i}: {residue.getOneLetterCode()}, mass: {residue.getMonoWeight():.4f}")
```

### Modified Sequences

Handle post-translational modifications:

```python
# Sequence with modifications
mod_seq = ms.AASequence.fromString("PEPTIDEM(Oxidation)K")

print(f"Modified sequence: {mod_seq.toString()}")
print(f"Mass with mods: {mod_seq.getMonoWeight():.4f}")

# Check if modified
print(f"Is modified: {mod_seq.isModified()}")

# Get modification info
for i in range(mod_seq.size()):
    residue = mod_seq.getResidue(i)
    if residue.isModified():
        print(f"Residue {residue.getOneLetterCode()} at position {i}")
        print(f"  Modification: {residue.getModificationName()}")
```

### Peptide Digestion

Simulate enzymatic digestion:

```python
# Create digestion enzyme
enzyme = ms.ProteaseDigestion()
enzyme.setEnzyme("Trypsin")

# Set missed cleavages
enzyme.setMissedCleavages(2)

# Digest protein sequence
protein_seq = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"

# Get peptides
peptides = []
enzyme.digest(ms.AASequence.fromString(protein_seq), peptides)

print(f"Generated {len(peptides)} peptides")
for peptide in peptides[:5]:  # Show first 5
    print(f"  {peptide.toString()}, mass: {peptide.getMonoWeight():.2f}")
```

## Theoretical Spectrum Generation

### Fragment Ion Calculation

Generate theoretical fragment ions:

```python
# Create peptide
peptide = ms.AASequence.fromString("PEPTIDE")

# Generate b and y ions
fragments = []
ms.TheoreticalSpectrumGenerator().getSpectrum(fragments, peptide, 1, 1)

print(f"Generated {fragments.size()} fragment ions")

# Access fragments
mz, intensity = fragments.get_peaks()
for m, i in zip(mz[:10], intensity[:10]):  # Show first 10
    print(f"m/z: {m:.4f}, intensity: {i}")
```

## Complete Identification Workflow

### End-to-End Example

```python
import pyopenms as ms

def identification_workflow(spectrum_file, fasta_file, output_file):
    """
    Complete identification workflow with FDR control.

    Args:
        spectrum_file: Input mzML file
        fasta_file: Protein database (FASTA)
        output_file: Output idXML file
    """

    # Step 1: Load spectra
    exp = ms.MSExperiment()
    ms.MzMLFile().load(spectrum_file, exp)
    print(f"Loaded {exp.getNrSpectra()} spectra")

    # Step 2: Configure search parameters
    search_params = ms.SearchParameters()
    search_params.db = fasta_file
    search_params.precursor_mass_tolerance = 10.0  # ppm
    search_params.fragment_mass_tolerance = 0.5  # Da
    search_params.enzyme = "Trypsin"
    search_params.missed_cleavages = 2
    search_params.modifications = ["Oxidation (M)", "Carbamidomethyl (C)"]

    # Step 3: Run search (example with Comet adapter)
    # Note: Requires search engine to be installed
    # comet = ms.CometAdapter()
    # protein_ids, peptide_ids = comet.search(exp, search_params)

    # For this example, load pre-computed results
    protein_ids = []
    peptide_ids = []
    ms.IdXMLFile().load("raw_identifications.idXML", protein_ids, peptide_ids)

    print(f"Initial peptide IDs: {len(peptide_ids)}")

    # Step 4: Apply FDR filtering
    fdr = ms.FalseDiscoveryRate()
    fdr.apply(peptide_ids)

    # Filter by 1% FDR
    filtered_peptide_ids = []
    for peptide_id in peptide_ids:
        filtered_hits = []
        for hit in peptide_id.getHits():
            q_value = hit.getMetaValue("q-value")
            if q_value <= 0.01:
                filtered_hits.append(hit)

        if filtered_hits:
            peptide_id.setHits(filtered_hits)
            filtered_peptide_ids.append(peptide_id)

    print(f"Peptides after FDR (1%): {len(filtered_peptide_ids)}")

    # Step 5: Protein inference
    inference = ms.BasicProteinInferenceAlgorithm()
    inference.run(filtered_peptide_ids, protein_ids)

    print(f"Identified proteins: {len(protein_ids)}")

    # Step 6: Save results
    ms.IdXMLFile().store(output_file, protein_ids, filtered_peptide_ids)
    print(f"Results saved to {output_file}")

    return protein_ids, filtered_peptide_ids

# Run workflow
protein_ids, peptide_ids = identification_workflow(
    "spectra.mzML",
    "database.fasta",
    "identifications_fdr.idXML"
)
```

## Spectral Library Search

### Library Matching

```python
# Load spectral library
library = ms.MSPFile()
library_spectra = []
library.load("spectral_library.msp", library_spectra)

# Load experimental spectra
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Compare spectra
spectra_compare = ms.SpectraSTSimilarityScore()

for exp_spec in exp:
    if exp_spec.getMSLevel() == 2:
        best_match_score = 0
        best_match_lib = None

        for lib_spec in library_spectra:
            score = spectra_compare.operator()(exp_spec, lib_spec)
            if score > best_match_score:
                best_match_score = score
                best_match_lib = lib_spec

        if best_match_score > 0.7:  # Threshold
            print(f"Match found: score {best_match_score:.3f}")
```

## Best Practices

### Decoy Database

Use target-decoy approach for FDR calculation:

```python
# Generate decoy database
decoy_generator = ms.DecoyGenerator()

# Load target database
fasta_entries = []
ms.FASTAFile().load("target.fasta", fasta_entries)

# Generate decoys
decoy_entries = []
for entry in fasta_entries:
    decoy_entry = decoy_generator.reverseProtein(entry)
    decoy_entries.append(decoy_entry)

# Save combined database
all_entries = fasta_entries + decoy_entries
ms.FASTAFile().store("target_decoy.fasta", all_entries)
```

### Score Interpretation

Understand score types from different engines:

```python
# Interpret scores based on search engine
for peptide_id in peptide_ids:
    search_engine = peptide_id.getIdentifier()

    for hit in peptide_id.getHits():
        score = hit.getScore()

        # Score interpretation varies by engine
        if "Comet" in search_engine:
            # Comet: higher E-value = worse
            print(f"E-value: {score}")
        elif "Mascot" in search_engine:
            # Mascot: higher score = better
            print(f"Ion score: {score}")
```

---

## Reference: Metabolomics

# Metabolomics Workflows

## Overview

PyOpenMS provides specialized tools for untargeted metabolomics analysis including feature detection optimized for small molecules, adduct grouping, compound identification, and integration with metabolomics databases.

## Untargeted Metabolomics Pipeline

### Complete Workflow

```python
import pyopenms as ms

def metabolomics_pipeline(input_files, output_dir):
    """
    Complete untargeted metabolomics workflow.

    Args:
        input_files: List of mzML file paths (one per sample)
        output_dir: Directory for output files
    """

    # Step 1: Peak picking and feature detection
    feature_maps = []

    for mzml_file in input_files:
        print(f"Processing {mzml_file}...")

        # Load data
        exp = ms.MSExperiment()
        ms.MzMLFile().load(mzml_file, exp)

        # Peak picking if needed
        if not exp.getSpectrum(0).isSorted():
            picker = ms.PeakPickerHiRes()
            exp_picked = ms.MSExperiment()
            picker.pickExperiment(exp, exp_picked)
            exp = exp_picked

        # Feature detection
        ff = ms.FeatureFinder()
        params = ff.getParameters("centroided")

        # Metabolomics-specific parameters
        params.setValue("mass_trace:mz_tolerance", 5.0)  # ppm, tighter for metabolites
        params.setValue("mass_trace:min_spectra", 5)
        params.setValue("isotopic_pattern:charge_low", 1)
        params.setValue("isotopic_pattern:charge_high", 2)  # Mostly singly charged

        features = ms.FeatureMap()
        ff.run("centroided", exp, features, params, ms.FeatureMap())

        features.setPrimaryMSRunPath([mzml_file.encode()])
        feature_maps.append(features)

        print(f"  Detected {features.size()} features")

    # Step 2: Adduct detection and grouping
    print("Detecting adducts...")
    adduct_grouped_maps = []

    adduct_detector = ms.MetaboliteAdductDecharger()
    params = adduct_detector.getParameters()
    params.setValue("potential_adducts", "[M+H]+,[M+Na]+,[M+K]+,[M+NH4]+,[M-H]-,[M+Cl]-")
    params.setValue("charge_min", 1)
    params.setValue("charge_max", 1)
    adduct_detector.setParameters(params)

    for fm in feature_maps:
        fm_out = ms.FeatureMap()
        adduct_detector.compute(fm, fm_out, ms.ConsensusMap())
        adduct_grouped_maps.append(fm_out)

    # Step 3: RT alignment
    print("Aligning retention times...")
    aligner = ms.MapAlignmentAlgorithmPoseClustering()

    params = aligner.getParameters()
    params.setValue("max_num_peaks_considered", 1000)
    params.setValue("pairfinder:distance_MZ:max_difference", 10.0)
    params.setValue("pairfinder:distance_MZ:unit", "ppm")
    aligner.setParameters(params)

    aligned_maps = []
    transformations = []
    aligner.align(adduct_grouped_maps, aligned_maps, transformations)

    # Step 4: Feature linking
    print("Linking features...")
    grouper = ms.FeatureGroupingAlgorithmQT()

    params = grouper.getParameters()
    params.setValue("distance_RT:max_difference", 60.0)  # seconds
    params.setValue("distance_MZ:max_difference", 5.0)  # ppm
    params.setValue("distance_MZ:unit", "ppm")
    grouper.setParameters(params)

    consensus_map = ms.ConsensusMap()
    grouper.group(aligned_maps, consensus_map)

    print(f"Created {consensus_map.size()} consensus features")

    # Step 5: Gap filling (fill missing values)
    print("Filling gaps...")
    # Gap filling not directly available in Python API
    # Would use TOPP tool FeatureFinderMetaboIdent

    # Step 6: Export results
    consensus_file = f"{output_dir}/consensus.consensusXML"
    ms.ConsensusXMLFile().store(consensus_file, consensus_map)

    # Export to CSV for downstream analysis
    df = consensus_map.get_df()
    csv_file = f"{output_dir}/metabolite_table.csv"
    df.to_csv(csv_file, index=False)

    print(f"Results saved to {output_dir}")

    return consensus_map

# Run pipeline
input_files = ["sample1.mzML", "sample2.mzML", "sample3.mzML"]
consensus = metabolomics_pipeline(input_files, "output")
```

## Adduct Detection

### Configure Adduct Types

```python
# Create adduct detector
adduct_detector = ms.MetaboliteAdductDecharger()

# Configure common adducts
params = adduct_detector.getParameters()

# Positive mode adducts
positive_adducts = [
    "[M+H]+",
    "[M+Na]+",
    "[M+K]+",
    "[M+NH4]+",
    "[2M+H]+",
    "[M+H-H2O]+"
]

# Negative mode adducts
negative_adducts = [
    "[M-H]-",
    "[M+Cl]-",
    "[M+FA-H]-",  # Formate
    "[2M-H]-"
]

# Set for positive mode
params.setValue("potential_adducts", ",".join(positive_adducts))
params.setValue("charge_min", 1)
params.setValue("charge_max", 1)
params.setValue("max_neutrals", 1)
adduct_detector.setParameters(params)

# Apply adduct detection
feature_map_out = ms.FeatureMap()
adduct_detector.compute(feature_map, feature_map_out, ms.ConsensusMap())
```

### Access Adduct Information

```python
# Check adduct annotations
for feature in feature_map_out:
    # Get adduct type if annotated
    if feature.metaValueExists("adduct"):
        adduct = feature.getMetaValue("adduct")
        neutral_mass = feature.getMetaValue("neutral_mass")
        print(f"m/z: {feature.getMZ():.4f}")
        print(f"  Adduct: {adduct}")
        print(f"  Neutral mass: {neutral_mass:.4f}")
```

## Compound Identification

### Mass-Based Annotation

```python
# Annotate features with compound database
from pyopenms import MassDecomposition

# Load compound database (example structure)
# In practice, use external database like HMDB, METLIN

compound_db = [
    {"name": "Glucose", "formula": "C6H12O6", "mass": 180.0634},
    {"name": "Citric acid", "formula": "C6H8O7", "mass": 192.0270},
    # ... more compounds
]

# Annotate features
mass_tolerance = 5.0  # ppm

for feature in feature_map:
    observed_mz = feature.getMZ()

    # Calculate neutral mass (assuming [M+H]+)
    neutral_mass = observed_mz - 1.007276  # Proton mass

    # Search database
    for compound in compound_db:
        mass_error_ppm = abs(neutral_mass - compound["mass"]) / compound["mass"] * 1e6

        if mass_error_ppm <= mass_tolerance:
            print(f"Potential match: {compound['name']}")
            print(f"  Observed m/z: {observed_mz:.4f}")
            print(f"  Expected mass: {compound['mass']:.4f}")
            print(f"  Error: {mass_error_ppm:.2f} ppm")
```

### MS/MS-Based Identification

```python
# Load MS2 data
exp = ms.MSExperiment()
ms.MzMLFile().load("data_with_ms2.mzML", exp)

# Extract MS2 spectra
ms2_spectra = []
for spec in exp:
    if spec.getMSLevel() == 2:
        ms2_spectra.append(spec)

print(f"Found {len(ms2_spectra)} MS2 spectra")

# Match to spectral library
# (Requires external tool or custom implementation)
```

## Data Normalization

### Total Ion Current (TIC) Normalization

```python
import numpy as np

# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Calculate TIC per sample
n_samples = len(consensus_map.getColumnHeaders())
tic_per_sample = np.zeros(n_samples)

for cons_feature in consensus_map:
    for handle in cons_feature.getFeatureList():
        map_idx = handle.getMapIndex()
        tic_per_sample[map_idx] += handle.getIntensity()

print("TIC per sample:", tic_per_sample)

# Normalize to median TIC
median_tic = np.median(tic_per_sample)
normalization_factors = median_tic / tic_per_sample

print("Normalization factors:", normalization_factors)

# Apply normalization
consensus_map_normalized = ms.ConsensusMap(consensus_map)
for cons_feature in consensus_map_normalized:
    feature_list = cons_feature.getFeatureList()
    for handle in feature_list:
        map_idx = handle.getMapIndex()
        normalized_intensity = handle.getIntensity() * normalization_factors[map_idx]
        handle.setIntensity(normalized_intensity)
```

## Quality Control

### Coefficient of Variation (CV) Filtering

```python
import pandas as pd
import numpy as np

# Export to pandas
df = consensus_map.get_df()

# Assume QC samples are columns with 'QC' in name
qc_cols = [col for col in df.columns if 'QC' in col]

if qc_cols:
    # Calculate CV for each feature in QC samples
    qc_data = df[qc_cols]
    cv = (qc_data.std(axis=1) / qc_data.mean(axis=1)) * 100

    # Filter features with CV < 30% in QC samples
    good_features = df[cv < 30]

    print(f"Features before CV filter: {len(df)}")
    print(f"Features after CV filter: {len(good_features)}")
```

### Blank Filtering

```python
# Remove features present in blank samples
blank_cols = [col for col in df.columns if 'Blank' in col]
sample_cols = [col for col in df.columns if 'Sample' in col]

if blank_cols and sample_cols:
    # Calculate mean intensity in blanks and samples
    blank_mean = df[blank_cols].mean(axis=1)
    sample_mean = df[sample_cols].mean(axis=1)

    # Keep features with 3x higher intensity in samples than blanks
    ratio = sample_mean / (blank_mean + 1)  # Add 1 to avoid division by zero
    filtered_df = df[ratio > 3]

    print(f"Features before blank filtering: {len(df)}")
    print(f"Features after blank filtering: {len(filtered_df)}")
```

## Missing Value Imputation

```python
import pandas as pd
import numpy as np

# Load data
df = consensus_map.get_df()

# Replace zeros with NaN
df = df.replace(0, np.nan)

# Count missing values
missing_per_feature = df.isnull().sum(axis=1)
print(f"Features with >50% missing: {sum(missing_per_feature > len(df.columns)/2)}")

# Simple imputation: replace with minimum value
for col in df.columns:
    if df[col].dtype in [np.float64, np.int64]:
        min_val = df[col].min() / 2  # Half minimum
        df[col].fillna(min_val, inplace=True)
```

## Metabolite Table Export

### Create Analysis-Ready Table

```python
import pandas as pd

def create_metabolite_table(consensus_map, output_file):
    """
    Create metabolite quantification table for statistical analysis.
    """

    # Get column headers (file descriptions)
    headers = consensus_map.getColumnHeaders()

    # Initialize data structure
    data = {
        'mz': [],
        'rt': [],
        'feature_id': []
    }

    # Add sample columns
    for map_idx, header in headers.items():
        sample_name = header.label or f"Sample_{map_idx}"
        data[sample_name] = []

    # Extract feature data
    for idx, cons_feature in enumerate(consensus_map):
        data['mz'].append(cons_feature.getMZ())
        data['rt'].append(cons_feature.getRT())
        data['feature_id'].append(f"F{idx:06d}")

        # Initialize intensities
        intensities = {map_idx: 0.0 for map_idx in headers.keys()}

        # Fill in measured intensities
        for handle in cons_feature.getFeatureList():
            map_idx = handle.getMapIndex()
            intensities[map_idx] = handle.getIntensity()

        # Add to data structure
        for map_idx, header in headers.items():
            sample_name = header.label or f"Sample_{map_idx}"
            data[sample_name].append(intensities[map_idx])

    # Create DataFrame
    df = pd.DataFrame(data)

    # Sort by RT
    df = df.sort_values('rt')

    # Save to CSV
    df.to_csv(output_file, index=False)

    print(f"Metabolite table with {len(df)} features saved to {output_file}")

    return df

# Create table
df = create_metabolite_table(consensus_map, "metabolite_table.csv")
```

## Integration with External Tools

### Export for MetaboAnalyst

```python
def export_for_metaboanalyst(df, output_file):
    """
    Format data for MetaboAnalyst input.

    Requires sample names as columns, features as rows.
    """

    # Transpose DataFrame
    # Remove metadata columns
    sample_cols = [col for col in df.columns if col not in ['mz', 'rt', 'feature_id']]

    # Extract sample data
    sample_data = df[sample_cols]

    # Transpose (samples as rows, features as columns)
    df_transposed = sample_data.T

    # Add feature identifiers as column names
    df_transposed.columns = df['feature_id']

    # Save
    df_transposed.to_csv(output_file)

    print(f"MetaboAnalyst format saved to {output_file}")

# Export
export_for_metaboanalyst(df, "for_metaboanalyst.csv")
```

## Best Practices

### Sample Size and Replicates

- Include QC samples (pooled sample) every 5-10 injections
- Run blank samples to identify contamination
- Use at least 3 biological replicates per group
- Randomize sample injection order

### Parameter Optimization

Test parameters on pooled QC sample:

```python
# Test different mass trace parameters
mz_tolerances = [3.0, 5.0, 10.0]
min_spectra_values = [3, 5, 7]

for tol in mz_tolerances:
    for min_spec in min_spectra_values:
        ff = ms.FeatureFinder()
        params = ff.getParameters("centroided")
        params.setValue("mass_trace:mz_tolerance", tol)
        params.setValue("mass_trace:min_spectra", min_spec)

        features = ms.FeatureMap()
        ff.run("centroided", exp, features, params, ms.FeatureMap())

        print(f"tol={tol}, min_spec={min_spec}: {features.size()} features")
```

### Retention Time Windows

Adjust based on chromatographic method:

```python
# For 10-minute LC gradient
params.setValue("distance_RT:max_difference", 30.0)  # 30 seconds

# For 60-minute LC gradient
params.setValue("distance_RT:max_difference", 90.0)  # 90 seconds
```

---

## Reference: Signal_Processing

# Signal Processing

## Overview

PyOpenMS provides algorithms for processing raw mass spectrometry data including smoothing, filtering, peak picking, centroiding, normalization, and deconvolution.

## Algorithm Pattern

Most signal processing algorithms follow a standard pattern:

```python
import pyopenms as ms

# 1. Create algorithm instance
algo = ms.AlgorithmName()

# 2. Get and modify parameters
params = algo.getParameters()
params.setValue("parameter_name", value)
algo.setParameters(params)

# 3. Apply to data
algo.filterExperiment(exp)  # or filterSpectrum(spec)
```

## Smoothing

### Gaussian Filter

Apply Gaussian smoothing to reduce noise:

```python
# Create Gaussian filter
gaussian = ms.GaussFilter()

# Configure parameters
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.2)  # Width in m/z or RT units
params.setValue("ppm_tolerance", 10.0)  # For m/z dimension
params.setValue("use_ppm_tolerance", "true")
gaussian.setParameters(params)

# Apply to experiment
gaussian.filterExperiment(exp)

# Or apply to single spectrum
spec = exp.getSpectrum(0)
gaussian.filterSpectrum(spec)
```

### Savitzky-Golay Filter

Polynomial smoothing that preserves peak shapes:

```python
# Create Savitzky-Golay filter
sg_filter = ms.SavitzkyGolayFilter()

# Configure parameters
params = sg_filter.getParameters()
params.setValue("frame_length", 11)  # Window size (must be odd)
params.setValue("polynomial_order", 4)  # Polynomial degree
sg_filter.setParameters(params)

# Apply smoothing
sg_filter.filterExperiment(exp)
```

## Peak Picking and Centroiding

### Peak Picker High Resolution

Detect peaks in high-resolution data:

```python
# Create peak picker
peak_picker = ms.PeakPickerHiRes()

# Configure parameters
params = peak_picker.getParameters()
params.setValue("signal_to_noise", 3.0)  # S/N threshold
params.setValue("spacing_difference", 1.5)  # Minimum peak spacing
peak_picker.setParameters(params)

# Pick peaks
exp_picked = ms.MSExperiment()
peak_picker.pickExperiment(exp, exp_picked)
```

### Peak Picker for CWT

Continuous wavelet transform-based peak picking:

```python
# Create CWT peak picker
cwt_picker = ms.PeakPickerCWT()

# Configure parameters
params = cwt_picker.getParameters()
params.setValue("signal_to_noise", 1.0)
params.setValue("peak_width", 0.15)  # Expected peak width
cwt_picker.setParameters(params)

# Pick peaks
cwt_picker.pickExperiment(exp, exp_picked)
```

## Normalization

### Normalizer

Normalize peak intensities within spectra:

```python
# Create normalizer
normalizer = ms.Normalizer()

# Configure normalization method
params = normalizer.getParameters()
params.setValue("method", "to_one")  # Options: "to_one", "to_TIC"
normalizer.setParameters(params)

# Apply normalization
normalizer.filterExperiment(exp)
```

## Peak Filtering

### Threshold Mower

Remove peaks below intensity threshold:

```python
# Create threshold filter
mower = ms.ThresholdMower()

# Configure threshold
params = mower.getParameters()
params.setValue("threshold", 1000.0)  # Absolute intensity threshold
mower.setParameters(params)

# Apply filter
mower.filterExperiment(exp)
```

### Window Mower

Keep only highest peaks in sliding windows:

```python
# Create window mower
window_mower = ms.WindowMower()

# Configure parameters
params = window_mower.getParameters()
params.setValue("windowsize", 50.0)  # Window size in m/z
params.setValue("peakcount", 2)  # Keep top N peaks per window
window_mower.setParameters(params)

# Apply filter
window_mower.filterExperiment(exp)
```

### N Largest Peaks

Keep only the N most intense peaks:

```python
# Create N largest filter
n_largest = ms.NLargest()

# Configure parameters
params = n_largest.getParameters()
params.setValue("n", 200)  # Keep 200 most intense peaks
n_largest.setParameters(params)

# Apply filter
n_largest.filterExperiment(exp)
```

## Baseline Reduction

### Morphological Filter

Remove baseline using morphological operations:

```python
# Create morphological filter
morph_filter = ms.MorphologicalFilter()

# Configure parameters
params = morph_filter.getParameters()
params.setValue("struc_elem_length", 3.0)  # Structuring element size
params.setValue("method", "tophat")  # Method: "tophat", "bothat", "erosion", "dilation"
morph_filter.setParameters(params)

# Apply filter
morph_filter.filterExperiment(exp)
```

## Spectrum Merging

### Spectra Merger

Combine multiple spectra into one:

```python
# Create merger
merger = ms.SpectraMerger()

# Configure parameters
params = merger.getParameters()
params.setValue("average_gaussian:spectrum_type", "profile")
params.setValue("average_gaussian:rt_FWHM", 5.0)  # RT window
merger.setParameters(params)

# Merge spectra
merger.mergeSpectraBlockWise(exp)
```

## Deconvolution

### Charge Deconvolution

Determine charge states and convert to neutral masses:

```python
# Create feature deconvoluter
deconvoluter = ms.FeatureDeconvolution()

# Configure parameters
params = deconvoluter.getParameters()
params.setValue("charge_min", 1)
params.setValue("charge_max", 4)
params.setValue("potential_charge_states", "1,2,3,4")
deconvoluter.setParameters(params)

# Apply deconvolution
feature_map_out = ms.FeatureMap()
deconvoluter.compute(exp, feature_map, feature_map_out, ms.ConsensusMap())
```

### Isotope Deconvolution

Remove isotopic patterns:

```python
# Create isotope wavelet transform
isotope_wavelet = ms.IsotopeWaveletTransform()

# Configure parameters
params = isotope_wavelet.getParameters()
params.setValue("max_charge", 3)
params.setValue("intensity_threshold", 10.0)
isotope_wavelet.setParameters(params)

# Apply transformation
isotope_wavelet.transform(exp)
```

## Retention Time Alignment

### Map Alignment

Align retention times across multiple runs:

```python
# Create map aligner
aligner = ms.MapAlignmentAlgorithmPoseClustering()

# Load multiple experiments
exp1 = ms.MSExperiment()
exp2 = ms.MSExperiment()
ms.MzMLFile().load("run1.mzML", exp1)
ms.MzMLFile().load("run2.mzML", exp2)

# Create reference
reference = ms.MSExperiment()

# Align experiments
transformations = []
aligner.align(exp1, exp2, transformations)

# Apply transformation
transformer = ms.MapAlignmentTransformer()
transformer.transformRetentionTimes(exp2, transformations[0])
```

## Mass Calibration

### Internal Calibration

Calibrate mass axis using known reference masses:

```python
# Create internal calibration
calibration = ms.InternalCalibration()

# Set reference masses
reference_masses = [500.0, 1000.0, 1500.0]  # Known m/z values

# Calibrate
calibration.calibrate(exp, reference_masses)
```

## Quality Control

### Spectrum Statistics

Calculate quality metrics:

```python
# Get spectrum
spec = exp.getSpectrum(0)

# Calculate statistics
mz, intensity = spec.get_peaks()

# Total ion current
tic = sum(intensity)

# Base peak
base_peak_intensity = max(intensity)
base_peak_mz = mz[intensity.argmax()]

print(f"TIC: {tic}")
print(f"Base peak: {base_peak_mz} m/z at {base_peak_intensity}")
```

## Spectrum Preprocessing Pipeline

### Complete Preprocessing Example

```python
import pyopenms as ms

def preprocess_experiment(input_file, output_file):
    """Complete preprocessing pipeline."""

    # Load data
    exp = ms.MSExperiment()
    ms.MzMLFile().load(input_file, exp)

    # 1. Smooth with Gaussian filter
    gaussian = ms.GaussFilter()
    gaussian.filterExperiment(exp)

    # 2. Pick peaks
    picker = ms.PeakPickerHiRes()
    exp_picked = ms.MSExperiment()
    picker.pickExperiment(exp, exp_picked)

    # 3. Normalize intensities
    normalizer = ms.Normalizer()
    params = normalizer.getParameters()
    params.setValue("method", "to_TIC")
    normalizer.setParameters(params)
    normalizer.filterExperiment(exp_picked)

    # 4. Filter low-intensity peaks
    mower = ms.ThresholdMower()
    params = mower.getParameters()
    params.setValue("threshold", 10.0)
    mower.setParameters(params)
    mower.filterExperiment(exp_picked)

    # Save processed data
    ms.MzMLFile().store(output_file, exp_picked)

    return exp_picked

# Run pipeline
exp_processed = preprocess_experiment("raw_data.mzML", "processed_data.mzML")
```

## Best Practices

### Parameter Optimization

Test parameters on representative data:

```python
# Try different Gaussian widths
widths = [0.1, 0.2, 0.5]

for width in widths:
    exp_test = ms.MSExperiment()
    ms.MzMLFile().load("test_data.mzML", exp_test)

    gaussian = ms.GaussFilter()
    params = gaussian.getParameters()
    params.setValue("gaussian_width", width)
    gaussian.setParameters(params)
    gaussian.filterExperiment(exp_test)

    # Evaluate quality
    # ... add evaluation code ...
```

### Preserve Original Data

Keep original data for comparison:

```python
# Load original
exp_original = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp_original)

# Create copy for processing
exp_processed = ms.MSExperiment(exp_original)

# Process copy
gaussian = ms.GaussFilter()
gaussian.filterExperiment(exp_processed)

# Original remains unchanged
```

### Profile vs Centroid Data

Check data type before processing:

```python
# Check if spectrum is centroided
spec = exp.getSpectrum(0)

if spec.isSorted():
    # Likely centroided
    print("Centroid data")
else:
    # Likely profile
    print("Profile data - apply peak picking")
```
