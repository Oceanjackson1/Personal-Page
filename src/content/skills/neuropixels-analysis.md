---
title: "Neuropixels Analysis"
description: "Neuropixels neural recording analysis. Load SpikeGLX/OpenEphys data, preprocess, motion correction, Kilosort4 spike sorting, quality metrics, Allen/IBL curation, AI-assisted visual analysis, for Neuropixels 1.0/2.0 extracellular electrophysiology...."
category: "research"
source: "community"
author: "Community"
tags: ["neuropixels", "analysis"]
date: 2026-03-20
---

# Neuropixels Data Analysis

## Overview

Comprehensive toolkit for analyzing Neuropixels high-density neural recordings using current best practices from SpikeInterface, Allen Institute, and International Brain Laboratory (IBL). Supports the full workflow from raw data to publication-ready curated units.

## When to Use This Skill

This skill should be used when:
- Working with Neuropixels recordings (.ap.bin, .lf.bin, .meta files)
- Loading data from SpikeGLX, Open Ephys, or NWB formats
- Preprocessing neural recordings (filtering, CAR, bad channel detection)
- Detecting and correcting motion/drift in recordings
- Running spike sorting (Kilosort4, SpykingCircus2, Mountainsort5)
- Computing quality metrics (SNR, ISI violations, presence ratio)
- Curating units using Allen/IBL criteria
- Creating visualizations of neural data
- Exporting results to Phy or NWB

## Supported Hardware & Formats

| Probe | Electrodes | Channels | Notes |
|-------|-----------|----------|-------|
| Neuropixels 1.0 | 960 | 384 | Requires phase_shift correction |
| Neuropixels 2.0 (single) | 1280 | 384 | Denser geometry |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | Multi-region recording |

| Format | Extension | Reader |
|--------|-----------|--------|
| SpikeGLX | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()` |
| Open Ephys | `.continuous`, `.oebin` | `si.read_openephys()` |
| NWB | `.nwb` | `si.read_nwb()` |

## Quick Start

### Basic Import and Setup

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# Configure parallel processing
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### Loading Data

```python
# SpikeGLX (most common)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys (common for many labs)
recording = si.read_openephys('/path/to/Record_Node_101/')

# Check available streams
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']

# For testing with subset of data
recording = recording.frame_slice(0, int(60 * recording.get_sampling_frequency()))
```

### Complete Pipeline (One Command)

```python
# Run full analysis pipeline
results = npa.run_pipeline(
    recording,
    output_dir='output/',
    sorter='kilosort4',
    curation_method='allen',
)

# Access results
sorting = results['sorting']
metrics = results['metrics']
labels = results['labels']
```

## Standard Analysis Workflow

### 1. Preprocessing

```python
# Recommended preprocessing chain
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)  # Required for Neuropixels 1.0
bad_ids, _ = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_ids)
rec = si.common_reference(rec, operator='median')

# Or use our wrapper
rec = npa.preprocess(recording)
```

### 2. Check and Correct Drift

```python
# Check for drift (always do this!)
motion_info = npa.estimate_motion(rec, preset='kilosort_like')
npa.plot_drift(rec, motion_info, output='drift_map.png')

# Apply correction if needed
if motion_info['motion'].max() > 10:  # microns
    rec = npa.correct_motion(rec, preset='nonrigid_accurate')
```

### 3. Spike Sorting

```python
# Kilosort4 (recommended, requires GPU)
sorting = si.run_sorter('kilosort4', rec, folder='ks4_output')

# CPU alternatives
sorting = si.run_sorter('tridesclous2', rec, folder='tdc2_output')
sorting = si.run_sorter('spykingcircus2', rec, folder='sc2_output')
sorting = si.run_sorter('mountainsort5', rec, folder='ms5_output')

# Check available sorters
print(si.installed_sorters())
```

### 4. Postprocessing

```python
# Create analyzer and compute all extensions
analyzer = si.create_sorting_analyzer(sorting, rec, sparse=True)

analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0)
analyzer.compute('templates', operators=['average', 'std'])
analyzer.compute('spike_amplitudes')
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)
analyzer.compute('unit_locations', method='monopolar_triangulation')
analyzer.compute('quality_metrics')

metrics = analyzer.get_extension('quality_metrics').get_data()
```

### 5. Curation

```python
# Allen Institute criteria (conservative)
good_units = metrics.query("""
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
""").index.tolist()

# Or use automated curation
labels = npa.curate(metrics, method='allen')  # 'allen', 'ibl', 'strict'
```

### 6. AI-Assisted Curation (For Uncertain Units)

When using this skill with Claude Code, Claude can directly analyze waveform plots and provide expert curation decisions. For programmatic API access:

```python
from anthropic import Anthropic

# Setup API client
client = Anthropic()

# Analyze uncertain units visually
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

for unit_id in uncertain:
    result = npa.analyze_unit_visually(analyzer, unit_id, api_client=client)
    print(f"Unit {unit_id}: {result['classification']}")
    print(f"  Reasoning: {result['reasoning'][:100]}...")
```

**Claude Code Integration**: When running within Claude Code, ask Claude to examine waveform/correlogram plots directly - no API setup required.

### 7. Generate Analysis Report

```python
# Generate comprehensive HTML report with visualizations
report_dir = npa.generate_analysis_report(results, 'output/')
# Opens report.html with summary stats, figures, and unit table

# Print formatted summary to console
npa.print_analysis_summary(results)
```

### 8. Export Results

```python
# Export to Phy for manual review
si.export_to_phy(analyzer, output_folder='phy_export/',
                 compute_pc_features=True, compute_amplitudes=True)

# Export to NWB
from spikeinterface.exporters import export_to_nwb
export_to_nwb(rec, sorting, 'output.nwb')

# Save quality metrics
metrics.to_csv('quality_metrics.csv')
```

## Common Pitfalls and Best Practices

1. **Always check drift** before spike sorting - drift > 10μm significantly impacts quality
2. **Use phase_shift** for Neuropixels 1.0 probes (not needed for 2.0)
3. **Save preprocessed data** to avoid recomputing - use `rec.save(folder='preprocessed/')`
4. **Use GPU** for Kilosort4 - it's 10-50x faster than CPU alternatives
5. **Review uncertain units manually** - automated curation is a starting point
6. **Combine metrics with AI** - use metrics for clear cases, AI for borderline units
7. **Document your thresholds** - different analyses may need different criteria
8. **Export to Phy** for critical experiments - human oversight is valuable

## Key Parameters to Adjust

### Preprocessing
- `freq_min`: Highpass cutoff (300-400 Hz typical)
- `detect_threshold`: Bad channel detection sensitivity

### Motion Correction
- `preset`: 'kilosort_like' (fast) or 'nonrigid_accurate' (better for severe drift)

### Spike Sorting (Kilosort4)
- `batch_size`: Samples per batch (30000 default)
- `nblocks`: Number of drift blocks (increase for long recordings)
- `Th_learned`: Detection threshold (lower = more spikes)

### Quality Metrics
- `snr_threshold`: Signal-to-noise cutoff (3-5 typical)
- `isi_violations_ratio`: Refractory violations (0.01-0.5)
- `presence_ratio`: Recording coverage (0.5-0.95)

## Bundled Resources

### scripts/preprocess_recording.py
Automated preprocessing script:
```bash
python scripts/preprocess_recording.py /path/to/data --output preprocessed/
```

### scripts/run_sorting.py
Run spike sorting:
```bash
python scripts/run_sorting.py preprocessed/ --sorter kilosort4 --output sorting/
```

### scripts/compute_metrics.py
Compute quality metrics and apply curation:
```bash
python scripts/compute_metrics.py sorting/ preprocessed/ --output metrics/ --curation allen
```

### scripts/export_to_phy.py
Export to Phy for manual curation:
```bash
python scripts/export_to_phy.py metrics/analyzer --output phy_export/
```

### assets/analysis_template.py
Complete analysis template. Copy and customize:
```bash
cp assets/analysis_template.py my_analysis.py
# Edit parameters and run
python my_analysis.py
```

### reference/standard_workflow.md
Detailed step-by-step workflow with explanations for each stage.

### reference/api_reference.md
Quick function reference organized by module.

### reference/plotting_guide.md
Comprehensive visualization guide for publication-quality figures.

## Detailed Reference Guides

| Topic | Reference |
|-------|-----------|
| Full workflow | [references/standard_workflow.md](reference/standard_workflow.md) |
| API reference | [references/api_reference.md](reference/api_reference.md) |
| Plotting guide | [references/plotting_guide.md](reference/plotting_guide.md) |
| Preprocessing | [references/PREPROCESSING.md](reference/PREPROCESSING.md) |
| Spike sorting | [references/SPIKE_SORTING.md](reference/SPIKE_SORTING.md) |
| Motion correction | [references/MOTION_CORRECTION.md](reference/MOTION_CORRECTION.md) |
| Quality metrics | [references/QUALITY_METRICS.md](reference/QUALITY_METRICS.md) |
| Automated curation | [references/AUTOMATED_CURATION.md](reference/AUTOMATED_CURATION.md) |
| AI-assisted curation | [references/AI_CURATION.md](reference/AI_CURATION.md) |
| Waveform analysis | [references/ANALYSIS.md](reference/ANALYSIS.md) |

## Installation

```bash
# Core packages
pip install spikeinterface[full] probeinterface neo

# Spike sorters
pip install kilosort          # Kilosort4 (GPU required)
pip install spykingcircus     # SpykingCircus2 (CPU)
pip install mountainsort5     # Mountainsort5 (CPU)

# Our toolkit
pip install neuropixels-analysis

# Optional: AI curation
pip install anthropic

# Optional: IBL tools
pip install ibl-neuropixel ibllib
```

## Project Structure

```
project/
├── raw_data/
│   └── recording_g0/
│       └── recording_g0_imec0/
│           ├── recording_g0_t0.imec0.ap.bin
│           └── recording_g0_t0.imec0.ap.meta
├── preprocessed/           # Saved preprocessed recording
├── motion/                 # Motion estimation results
├── sorting_output/         # Spike sorter output
├── analyzer/               # SortingAnalyzer (waveforms, metrics)
├── phy_export/             # For manual curation
├── ai_curation/            # AI analysis reports
└── results/
    ├── quality_metrics.csv
    ├── curation_labels.json
    └── output.nwb
```

## Additional Resources

- **SpikeInterface Docs**: https://spikeinterface.readthedocs.io/
- **Neuropixels Tutorial**: https://spikeinterface.readthedocs.io/en/stable/how_to/analyze_neuropixels.html
- **Kilosort4 GitHub**: https://github.com/MouseLand/Kilosort
- **IBL Neuropixel Tools**: https://github.com/int-brain-lab/ibl-neuropixel
- **Allen Institute ecephys**: https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell (Automated QC)**: https://github.com/Julie-Fabre/bombcell
- **SpikeAgent (AI Curation)**: https://github.com/SpikeAgent/SpikeAgent

---

## Reference: Ai_Curation

# AI-Assisted Curation Reference

Guide to using AI visual analysis for unit curation, inspired by SpikeAgent's approach.

## Overview

AI-assisted curation uses vision-language models to analyze spike sorting visualizations,
providing expert-level quality assessments similar to human curators.

### Workflow

```
Traditional:  Metrics → Threshold → Labels
AI-Enhanced:  Metrics → AI Visual Analysis → Confidence Score → Labels
```

## Claude Code Integration

When using this skill within Claude Code, Claude can directly analyze waveform plots without requiring API setup. Simply:

1. Generate a unit report or plot
2. Ask Claude to analyze the visualization
3. Claude will provide expert-level curation decisions

Example workflow in Claude Code:
```python
# Generate plots for a unit
npa.plot_unit_summary(analyzer, unit_id=0, output='unit_0_summary.png')

# Then ask Claude: "Please analyze this unit's waveforms and autocorrelogram
# to determine if it's a well-isolated single unit, multi-unit activity, or noise"
```

Claude can assess:
- Waveform consistency and shape
- Refractory period violations from autocorrelograms
- Amplitude stability over time
- Overall unit isolation quality

## Quick Start

### Generate Unit Report

```python
import neuropixels_analysis as npa

# Create visual report for a unit
report = npa.generate_unit_report(analyzer, unit_id=0, output_dir='reports/')

# Report includes:
# - Waveforms, templates, autocorrelogram
# - Amplitudes over time, ISI histogram
# - Quality metrics summary
# - Base64 encoded image for API
```

### AI Visual Analysis

```python
from anthropic import Anthropic

# Setup API client
client = Anthropic()

# Analyze single unit
result = npa.analyze_unit_visually(
    analyzer,
    unit_id=0,
    api_client=client,
    model='claude-opus-4.5',
    task='quality_assessment'
)

print(f"Classification: {result['classification']}")
print(f"Reasoning: {result['reasoning']}")
```

### Batch Analysis

```python
# Analyze all units
results = npa.batch_visual_curation(
    analyzer,
    api_client=client,
    output_dir='ai_curation/',
    progress_callback=lambda i, n: print(f"Progress: {i}/{n}")
)

# Get labels
ai_labels = {uid: r['classification'] for uid, r in results.items()}
```

## Interactive Curation Session

For human-in-the-loop curation with AI assistance:

```python
# Create session
session = npa.CurationSession.create(
    analyzer,
    output_dir='curation_session/',
    sort_by_confidence=True  # Show uncertain units first
)

# Process units
while True:
    unit = session.current_unit()
    if unit is None:
        break

    print(f"Unit {unit.unit_id}:")
    print(f"  Auto: {unit.auto_classification} (conf: {unit.confidence:.2f})")

    # Generate report
    report = npa.generate_unit_report(analyzer, unit.unit_id)

    # Get AI opinion
    ai_result = npa.analyze_unit_visually(analyzer, unit.unit_id, api_client=client)
    session.set_ai_classification(unit.unit_id, ai_result['classification'])

    # Human decision
    decision = input("Decision (good/mua/noise/skip): ")
    if decision != 'skip':
        session.set_decision(unit.unit_id, decision)

    session.next_unit()

# Export results
labels = session.get_final_labels()
session.export_decisions('final_curation.csv')
```

## Analysis Tasks

### Quality Assessment (Default)

Analyzes waveform shape, refractory period, amplitude stability.

```python
result = npa.analyze_unit_visually(analyzer, uid, task='quality_assessment')
# Returns: 'good', 'mua', or 'noise'
```

### Merge Candidate Detection

Determines if two units should be merged.

```python
result = npa.analyze_unit_visually(analyzer, uid, task='merge_candidate')
# Returns: 'merge' or 'keep_separate'
```

### Drift Assessment

Evaluates motion/drift in the recording.

```python
result = npa.analyze_unit_visually(analyzer, uid, task='drift_assessment')
# Returns drift magnitude and correction recommendation
```

## Custom Prompts

Create custom analysis prompts:

```python
from neuropixels_analysis.ai_curation import create_curation_prompt

# Get base prompt
prompt = create_curation_prompt(
    task='quality_assessment',
    additional_context='Focus on waveform amplitude consistency'
)

# Or fully custom
custom_prompt = """
Analyze this unit and determine if it represents a fast-spiking interneuron.

Look for:
1. Narrow waveform (peak-to-trough < 0.5ms)
2. High firing rate
3. Regular ISI distribution

Classify as: FSI (fast-spiking interneuron) or OTHER
"""

result = npa.analyze_unit_visually(
    analyzer, uid,
    api_client=client,
    custom_prompt=custom_prompt
)
```

## Combining AI with Metrics

Best practice: use both AI and quantitative metrics:

```python
def hybrid_curation(analyzer, metrics, api_client):
    """Combine metrics and AI for robust curation."""
    labels = {}

    for unit_id in metrics.index:
        row = metrics.loc[unit_id]

        # High confidence from metrics alone
        if row['snr'] > 10 and row['isi_violations_ratio'] < 0.001:
            labels[unit_id] = 'good'
            continue

        if row['snr'] < 1.5:
            labels[unit_id] = 'noise'
            continue

        # Uncertain cases: use AI
        result = npa.analyze_unit_visually(
            analyzer, unit_id, api_client=api_client
        )
        labels[unit_id] = result['classification']

    return labels
```

## Session Management

### Resume Session

```python
# Resume interrupted session
session = npa.CurationSession.load('curation_session/20250101_120000/')

# Check progress
summary = session.get_summary()
print(f"Progress: {summary['progress_pct']:.1f}%")
print(f"Remaining: {summary['remaining']} units")

# Continue from where we left off
unit = session.current_unit()
```

### Navigate Session

```python
# Go to specific unit
session.go_to_unit(42)

# Previous/next
session.prev_unit()
session.next_unit()

# Update decision
session.set_decision(42, 'good', notes='Clear refractory period')
```

### Export Results

```python
# Get final labels (priority: human > AI > auto)
labels = session.get_final_labels()

# Export detailed results
df = session.export_decisions('curation_results.csv')

# Summary
summary = session.get_summary()
print(f"Good: {summary['decisions'].get('good', 0)}")
print(f"MUA: {summary['decisions'].get('mua', 0)}")
print(f"Noise: {summary['decisions'].get('noise', 0)}")
```

## Visual Report Components

The generated report includes 6 panels:

| Panel | Content | What to Look For |
|-------|---------|------------------|
| Waveforms | Individual spike waveforms | Consistency, shape |
| Template | Mean ± std | Clean negative peak, physiological shape |
| Autocorrelogram | Spike timing | Gap at 0ms (refractory period) |
| Amplitudes | Amplitude over time | Stability, no drift |
| ISI Histogram | Inter-spike intervals | Refractory gap < 1.5ms |
| Metrics | Quality numbers | SNR, ISI violations, presence |

## API Support

Currently supported APIs:

| Provider | Client | Model Examples |
|----------|--------|----------------|
| Anthropic | `anthropic.Anthropic()` | claude-opus-4.5 |
| OpenAI | `openai.OpenAI()` | gpt-4-vision-preview |
| Google | `google.generativeai` | gemini-pro-vision |

### Anthropic Example

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")
result = npa.analyze_unit_visually(analyzer, uid, api_client=client)
```

### OpenAI Example

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
result = npa.analyze_unit_visually(
    analyzer, uid,
    api_client=client,
    model='gpt-4-vision-preview'
)
```

## Best Practices

1. **Use AI for uncertain cases** - Don't waste API calls on obvious good/noise units
2. **Combine with metrics** - AI should supplement, not replace, quantitative measures
3. **Human oversight** - Review AI decisions, especially for important analyses
4. **Save sessions** - Always use CurationSession to track decisions
5. **Document reasoning** - Use notes field to record decision rationale

## Cost Optimization

```python
# Only use AI for uncertain units
uncertain_units = metrics.query("""
    snr > 2 and snr < 8 and
    isi_violations_ratio > 0.001 and isi_violations_ratio < 0.1
""").index.tolist()

# Batch process only these
results = npa.batch_visual_curation(
    analyzer,
    unit_ids=uncertain_units,
    api_client=client
)
```

## References

- [SpikeAgent](https://github.com/SpikeAgent/SpikeAgent) - AI-powered spike sorting assistant
- [Anthropic Vision API](https://docs.anthropic.com/en/docs/vision)
- [GPT-4 Vision](https://platform.openai.com/docs/guides/vision)

---

## Reference: Analysis

# Post-Processing & Analysis Reference

Comprehensive guide to quality metrics, visualization, and analysis of sorted Neuropixels data.

## Sorting Analyzer

The `SortingAnalyzer` is the central object for post-processing.

### Create Analyzer
```python
import spikeinterface.full as si

# Create analyzer
analyzer = si.create_sorting_analyzer(
    sorting,
    recording,
    sparse=True,                    # Use sparse representation
    format='binary_folder',         # Storage format
    folder='analyzer_output'        # Save location
)
```

### Compute Extensions
```python
# Compute all standard extensions
analyzer.compute('random_spikes')       # Random spike selection
analyzer.compute('waveforms')           # Extract waveforms
analyzer.compute('templates')           # Compute templates
analyzer.compute('noise_levels')        # Noise estimation
analyzer.compute('principal_components')  # PCA
analyzer.compute('spike_amplitudes')    # Amplitude per spike
analyzer.compute('correlograms')        # Auto/cross correlograms
analyzer.compute('unit_locations')      # Unit locations
analyzer.compute('spike_locations')     # Per-spike locations
analyzer.compute('template_similarity') # Template similarity matrix
analyzer.compute('quality_metrics')     # Quality metrics

# Or compute multiple at once
analyzer.compute([
    'random_spikes', 'waveforms', 'templates', 'noise_levels',
    'principal_components', 'spike_amplitudes', 'correlograms',
    'unit_locations', 'quality_metrics'
])
```

### Save and Load
```python
# Save
analyzer.save_as(folder='analyzer_saved', format='binary_folder')

# Load
analyzer = si.load_sorting_analyzer('analyzer_saved')
```

## Quality Metrics

### Compute Metrics
```python
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()
print(qm)
```

### Available Metrics

| Metric | Description | Good Values |
|--------|-------------|-------------|
| `snr` | Signal-to-noise ratio | > 5 |
| `isi_violations_ratio` | ISI violation ratio | < 0.01 (1%) |
| `isi_violations_count` | ISI violation count | Low |
| `presence_ratio` | Fraction of recording with spikes | > 0.9 |
| `firing_rate` | Spikes per second | 0.1-50 Hz |
| `amplitude_cutoff` | Estimated missed spikes | < 0.1 |
| `amplitude_median` | Median spike amplitude | - |
| `amplitude_cv` | Coefficient of variation | < 0.5 |
| `drift_ptp` | Peak-to-peak drift (um) | < 40 |
| `drift_std` | Standard deviation of drift | < 10 |
| `drift_mad` | Median absolute deviation | < 10 |
| `sliding_rp_violation` | Sliding refractory period | < 0.05 |
| `sync_spike_2` | Synchrony with other units | < 0.5 |
| `isolation_distance` | Mahalanobis distance | > 20 |
| `l_ratio` | L-ratio (isolation) | < 0.1 |
| `d_prime` | Discriminability | > 5 |
| `nn_hit_rate` | Nearest neighbor hit rate | > 0.9 |
| `nn_miss_rate` | Nearest neighbor miss rate | < 0.1 |
| `silhouette_score` | Cluster silhouette | > 0.5 |

### Compute Specific Metrics
```python
analyzer.compute(
    'quality_metrics',
    metric_names=['snr', 'isi_violations_ratio', 'presence_ratio', 'firing_rate']
)
```

### Custom Quality Thresholds
```python
qm = analyzer.get_extension('quality_metrics').get_data()

# Define quality criteria
quality_criteria = {
    'snr': ('>', 5),
    'isi_violations_ratio': ('<', 0.01),
    'presence_ratio': ('>', 0.9),
    'firing_rate': ('>', 0.1),
    'amplitude_cutoff': ('<', 0.1),
}

# Filter good units
good_units = qm.query(
    "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
).index.tolist()

print(f"Good units: {len(good_units)}/{len(qm)}")
```

## Waveforms & Templates

### Extract Waveforms
```python
analyzer.compute('waveforms', ms_before=1.5, ms_after=2.5, max_spikes_per_unit=500)

# Get waveforms for a unit
waveforms = analyzer.get_extension('waveforms').get_waveforms(unit_id=0)
print(f"Shape: {waveforms.shape}")  # (n_spikes, n_samples, n_channels)
```

### Compute Templates
```python
analyzer.compute('templates', operators=['average', 'std', 'median'])

# Get template
templates_ext = analyzer.get_extension('templates')
template = templates_ext.get_unit_template(unit_id=0, operator='average')
```

### Template Similarity
```python
analyzer.compute('template_similarity')
sim = analyzer.get_extension('template_similarity').get_data()
# Matrix of cosine similarities between templates
```

## Unit Locations

### Compute Locations
```python
analyzer.compute('unit_locations', method='monopolar_triangulation')
locations = analyzer.get_extension('unit_locations').get_data()
print(locations)  # x, y coordinates per unit
```

### Spike Locations
```python
analyzer.compute('spike_locations', method='center_of_mass')
spike_locs = analyzer.get_extension('spike_locations').get_data()
```

### Location Methods
- `'center_of_mass'` - Fast, less accurate
- `'monopolar_triangulation'` - More accurate, slower
- `'grid_convolution'` - Good balance

## Correlograms

### Auto-correlograms
```python
analyzer.compute('correlograms', window_ms=50, bin_ms=1)
correlograms, bins = analyzer.get_extension('correlograms').get_data()

# correlograms shape: (n_units, n_units, n_bins)
# Auto-correlogram for unit i: correlograms[i, i, :]
# Cross-correlogram units i,j: correlograms[i, j, :]
```

## Visualization

### Probe Map
```python
si.plot_probe_map(recording, with_channel_ids=True)
```

### Unit Templates
```python
# All units
si.plot_unit_templates(analyzer)

# Specific units
si.plot_unit_templates(analyzer, unit_ids=[0, 1, 2])
```

### Waveforms
```python
# Plot waveforms with template
si.plot_unit_waveforms(analyzer, unit_ids=[0])

# Waveform density
si.plot_unit_waveforms_density_map(analyzer, unit_id=0)
```

### Raster Plot
```python
si.plot_rasters(sorting, time_range=(0, 10))  # First 10 seconds
```

### Amplitudes
```python
analyzer.compute('spike_amplitudes')
si.plot_amplitudes(analyzer)

# Distribution
si.plot_all_amplitudes_distributions(analyzer)
```

### Correlograms
```python
# Auto-correlograms
si.plot_autocorrelograms(analyzer, unit_ids=[0, 1, 2])

# Cross-correlograms
si.plot_crosscorrelograms(analyzer, unit_ids=[0, 1])
```

### Quality Metrics
```python
# Summary plot
si.plot_quality_metrics(analyzer)

# Specific metric distribution
import matplotlib.pyplot as plt
qm = analyzer.get_extension('quality_metrics').get_data()
plt.hist(qm['snr'], bins=50)
plt.xlabel('SNR')
plt.ylabel('Count')
```

### Unit Locations on Probe
```python
si.plot_unit_locations(analyzer)
```

### Drift Map
```python
si.plot_drift_raster(sorting, recording)
```

### Summary Plot
```python
# Comprehensive unit summary
si.plot_unit_summary(analyzer, unit_id=0)
```

## LFP Analysis

### Load LFP Data
```python
lfp = si.read_spikeglx('/path/to/data', stream_id='imec0.lf')
print(f"LFP: {lfp.get_sampling_frequency()} Hz")
```

### Basic LFP Processing
```python
# Downsample if needed
lfp_ds = si.resample(lfp, resample_rate=1000)

# Common average reference
lfp_car = si.common_reference(lfp_ds, reference='global', operator='median')
```

### Extract LFP Traces
```python
import numpy as np

# Get traces (channels x samples)
traces = lfp.get_traces(start_frame=0, end_frame=30000)

# Specific channels
traces = lfp.get_traces(channel_ids=[0, 1, 2])
```

### Spectral Analysis
```python
from scipy import signal
import matplotlib.pyplot as plt

# Get single channel
trace = lfp.get_traces(channel_ids=[0]).flatten()
fs = lfp.get_sampling_frequency()

# Power spectrum
freqs, psd = signal.welch(trace, fs, nperseg=4096)
plt.semilogy(freqs, psd)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.xlim(0, 100)
```

### Spectrogram
```python
f, t, Sxx = signal.spectrogram(trace, fs, nperseg=2048, noverlap=1024)
plt.pcolormesh(t, f, 10*np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.ylim(0, 100)
plt.colorbar(label='Power (dB)')
```

## Export Formats

### Export to Phy
```python
si.export_to_phy(
    analyzer,
    output_folder='phy_export',
    compute_pc_features=True,
    compute_amplitudes=True,
    copy_binary=True
)
# Then: phy template-gui phy_export/params.py
```

### Export to NWB
```python
from spikeinterface.exporters import export_to_nwb

export_to_nwb(
    recording,
    sorting,
    'output.nwb',
    metadata=dict(
        session_description='Neuropixels recording',
        experimenter='Name',
        lab='Lab name',
        institution='Institution'
    )
)
```

### Export Report
```python
si.export_report(
    analyzer,
    output_folder='report',
    remove_if_exists=True,
    format='html'
)
```

## Complete Analysis Pipeline

```python
import spikeinterface.full as si

def analyze_sorting(recording, sorting, output_dir):
    """Complete post-processing pipeline."""

    # Create analyzer
    analyzer = si.create_sorting_analyzer(
        sorting, recording,
        sparse=True,
        folder=f'{output_dir}/analyzer'
    )

    # Compute all extensions
    print("Computing extensions...")
    analyzer.compute(['random_spikes', 'waveforms', 'templates', 'noise_levels'])
    analyzer.compute(['principal_components', 'spike_amplitudes'])
    analyzer.compute(['correlograms', 'unit_locations', 'template_similarity'])
    analyzer.compute('quality_metrics')

    # Get quality metrics
    qm = analyzer.get_extension('quality_metrics').get_data()

    # Filter good units
    good_units = qm.query(
        "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
    ).index.tolist()

    print(f"Quality filtering: {len(good_units)}/{len(qm)} units passed")

    # Export
    si.export_to_phy(analyzer, f'{output_dir}/phy')
    si.export_report(analyzer, f'{output_dir}/report')

    # Save metrics
    qm.to_csv(f'{output_dir}/quality_metrics.csv')

    return analyzer, qm, good_units

# Usage
analyzer, qm, good_units = analyze_sorting(recording, sorting, 'output/')
```

---

## Reference: Automated_Curation

# Automated Curation Reference

Guide to automated spike sorting curation using Bombcell, UnitRefine, and other tools.

## Why Automated Curation?

Manual curation is:
- **Slow**: Hours per recording session
- **Subjective**: Inter-rater variability
- **Non-reproducible**: Hard to standardize

Automated tools provide consistent, reproducible quality classification.

## Available Tools

| Tool | Classification | Language | Integration |
|------|---------------|----------|-------------|
| **Bombcell** | 4-class (single/multi/noise/non-somatic) | Python/MATLAB | SpikeInterface, Phy |
| **UnitRefine** | Machine learning-based | Python | SpikeInterface |
| **SpikeInterface QM** | Threshold-based | Python | Native |
| **UnitMatch** | Cross-session tracking | Python/MATLAB | Kilosort, Bombcell |

## Bombcell

### Overview

Bombcell classifies units into 4 categories:
1. **Single somatic units** - Well-isolated single neurons
2. **Multi-unit activity (MUA)** - Mixed neuronal signals
3. **Noise** - Non-neural artifacts
4. **Non-somatic** - Axonal or dendritic signals

### Installation

```bash
# Python
pip install bombcell

# Or development version
git clone https://github.com/Julie-Fabre/bombcell.git
cd bombcell/py_bombcell
pip install -e .
```

### Basic Usage (Python)

```python
import bombcell as bc

# Load sorted data (Kilosort output)
kilosort_folder = '/path/to/kilosort/output'
raw_data_path = '/path/to/recording.ap.bin'

# Run Bombcell
results = bc.run_bombcell(
    kilosort_folder,
    raw_data_path,
    sample_rate=30000,
    n_channels=384
)

# Get classifications
unit_labels = results['unit_labels']
# 'good' = single unit, 'mua' = multi-unit, 'noise' = noise
```

### Integration with SpikeInterface

```python
import spikeinterface.full as si

# After spike sorting
sorting = si.run_sorter('kilosort4', recording, output_folder='ks4/')

# Create analyzer and compute required extensions
analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True)
analyzer.compute('waveforms')
analyzer.compute('templates')
analyzer.compute('spike_amplitudes')

# Export to Phy format (Bombcell can read this)
si.export_to_phy(analyzer, output_folder='phy_export/')

# Run Bombcell on Phy export
import bombcell as bc
results = bc.run_bombcell_phy('phy_export/')
```

### Bombcell Metrics

Bombcell computes specific metrics for classification:

| Metric | Description | Used For |
|--------|-------------|----------|
| `peak_trough_ratio` | Waveform shape | Somatic vs non-somatic |
| `spatial_decay` | Amplitude across channels | Noise detection |
| `refractory_period_violations` | ISI violations | Single vs multi |
| `presence_ratio` | Temporal stability | Unit quality |
| `waveform_duration` | Peak-to-trough time | Cell type |

### Custom Thresholds

```python
# Customize classification thresholds
custom_params = {
    'isi_threshold': 0.01,          # ISI violation threshold
    'presence_threshold': 0.9,       # Minimum presence ratio
    'amplitude_threshold': 20,       # Minimum amplitude (μV)
    'spatial_decay_threshold': 40,   # Spatial decay (μm)
}

results = bc.run_bombcell(
    kilosort_folder,
    raw_data_path,
    **custom_params
)
```

## SpikeInterface Auto-Curation

### Threshold-Based Curation

```python
# Compute quality metrics
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()

# Define curation function
def auto_curate(qm):
    labels = {}
    for unit_id in qm.index:
        row = qm.loc[unit_id]

        # Classification logic
        if row['snr'] < 2 or row['presence_ratio'] < 0.5:
            labels[unit_id] = 'noise'
        elif row['isi_violations_ratio'] > 0.1:
            labels[unit_id] = 'mua'
        elif (row['snr'] > 5 and
              row['isi_violations_ratio'] < 0.01 and
              row['presence_ratio'] > 0.9):
            labels[unit_id] = 'good'
        else:
            labels[unit_id] = 'unsorted'

    return labels

unit_labels = auto_curate(qm)

# Filter by label
good_unit_ids = [u for u, l in unit_labels.items() if l == 'good']
sorting_curated = sorting.select_units(good_unit_ids)
```

### Using SpikeInterface Curation Module

```python
from spikeinterface.curation import (
    CurationSorting,
    MergeUnitsSorting,
    SplitUnitSorting
)

# Wrap sorting for curation
curation = CurationSorting(sorting)

# Remove noise units
noise_units = qm[qm['snr'] < 2].index.tolist()
curation.remove_units(noise_units)

# Merge similar units (based on template similarity)
analyzer.compute('template_similarity')
similarity = analyzer.get_extension('template_similarity').get_data()

# Find highly similar pairs
import numpy as np
threshold = 0.9
similar_pairs = np.argwhere(similarity > threshold)
# Merge pairs (careful - requires manual review)

# Get curated sorting
sorting_curated = curation.to_sorting()
```

## UnitMatch: Cross-Session Tracking

Track the same neurons across recording days.

### Installation

```bash
pip install unitmatch
# Or from source
git clone https://github.com/EnnyvanBeest/UnitMatch.git
```

### Usage

```python
# After running Bombcell on multiple sessions
session_folders = [
    '/path/to/session1/kilosort/',
    '/path/to/session2/kilosort/',
    '/path/to/session3/kilosort/',
]

from unitmatch import UnitMatch

# Run UnitMatch
um = UnitMatch(session_folders)
um.run()

# Get matching results
matches = um.get_matches()
# Returns DataFrame with unit IDs matched across sessions

# Assign unique IDs
unique_ids = um.get_unique_ids()
```

### Integration with Workflow

```python
# Typical workflow:
# 1. Spike sort each session
# 2. Run Bombcell for quality control
# 3. Run UnitMatch for cross-session tracking

# Session 1
sorting1 = si.run_sorter('kilosort4', rec1, output_folder='session1/ks4/')
# Run Bombcell
labels1 = bc.run_bombcell('session1/ks4/', raw1_path)

# Session 2
sorting2 = si.run_sorter('kilosort4', rec2, output_folder='session2/ks4/')
labels2 = bc.run_bombcell('session2/ks4/', raw2_path)

# Track units across sessions
um = UnitMatch(['session1/ks4/', 'session2/ks4/'])
matches = um.get_matches()
```

## Semi-Automated Workflow

Combine automated and manual curation:

```python
# Step 1: Automated classification
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()

# Auto-label obvious cases
auto_labels = {}
for unit_id in qm.index:
    row = qm.loc[unit_id]
    if row['snr'] < 1.5:
        auto_labels[unit_id] = 'noise'
    elif row['snr'] > 8 and row['isi_violations_ratio'] < 0.005:
        auto_labels[unit_id] = 'good'
    else:
        auto_labels[unit_id] = 'needs_review'

# Step 2: Export uncertain units for manual review
needs_review = [u for u, l in auto_labels.items() if l == 'needs_review']

# Export only uncertain units to Phy
sorting_review = sorting.select_units(needs_review)
analyzer_review = si.create_sorting_analyzer(sorting_review, recording)
analyzer_review.compute('waveforms')
analyzer_review.compute('templates')
si.export_to_phy(analyzer_review, output_folder='phy_review/')

# Manual review in Phy: phy template-gui phy_review/params.py

# Step 3: Load manual labels and merge
manual_labels = si.read_phy('phy_review/').get_property('quality')
# Combine auto + manual labels for final result
```

## Comparison of Methods

| Method | Pros | Cons |
|--------|------|------|
| **Manual (Phy)** | Gold standard, flexible | Slow, subjective |
| **SpikeInterface QM** | Fast, reproducible | Simple thresholds only |
| **Bombcell** | Multi-class, validated | Requires waveform extraction |
| **UnitRefine** | ML-based, learns from data | Needs training data |

## Best Practices

1. **Always visualize** - Don't blindly trust automated results
2. **Document thresholds** - Record exact parameters used
3. **Validate** - Compare automated vs manual on subset
4. **Be conservative** - When in doubt, exclude the unit
5. **Report methods** - Include curation criteria in publications

## Pipeline Example

```python
def curate_sorting(sorting, recording, output_dir):
    """Complete curation pipeline."""

    # Create analyzer
    analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True,
                                          folder=f'{output_dir}/analyzer')

    # Compute required extensions
    analyzer.compute('random_spikes', max_spikes_per_unit=500)
    analyzer.compute('waveforms')
    analyzer.compute('templates')
    analyzer.compute('noise_levels')
    analyzer.compute('spike_amplitudes')
    analyzer.compute('quality_metrics')

    qm = analyzer.get_extension('quality_metrics').get_data()

    # Auto-classify
    labels = {}
    for unit_id in qm.index:
        row = qm.loc[unit_id]

        if row['snr'] < 2:
            labels[unit_id] = 'noise'
        elif row['isi_violations_ratio'] > 0.1 or row['presence_ratio'] < 0.8:
            labels[unit_id] = 'mua'
        elif (row['snr'] > 5 and
              row['isi_violations_ratio'] < 0.01 and
              row['presence_ratio'] > 0.9 and
              row['amplitude_cutoff'] < 0.1):
            labels[unit_id] = 'good'
        else:
            labels[unit_id] = 'unsorted'

    # Summary
    from collections import Counter
    print("Classification summary:")
    print(Counter(labels.values()))

    # Save labels
    import json
    with open(f'{output_dir}/unit_labels.json', 'w') as f:
        json.dump(labels, f)

    # Return good units
    good_ids = [u for u, l in labels.items() if l == 'good']
    return sorting.select_units(good_ids), labels

# Usage
sorting_curated, labels = curate_sorting(sorting, recording, 'output/')
```

## References

- [Bombcell GitHub](https://github.com/Julie-Fabre/bombcell)
- [UnitMatch GitHub](https://github.com/EnnyvanBeest/UnitMatch)
- [SpikeInterface Curation](https://spikeinterface.readthedocs.io/en/stable/modules/curation.html)
- Fabre et al. (2023) "Bombcell: automated curation and cell classification"
- van Beest et al. (2024) "UnitMatch: tracking neurons across days with high-density probes"

---

## Reference: Motion_Correction

# Motion/Drift Correction Reference

Mechanical drift during acute probe insertion is a major challenge for Neuropixels recordings. This guide covers detection, estimation, and correction of motion artifacts.

## Why Motion Correction Matters

- Neuropixels probes can drift 10-100+ μm during recording
- Uncorrected drift leads to:
  - Units appearing/disappearing mid-recording
  - Waveform amplitude changes
  - Incorrect spike-unit assignments
  - Reduced unit yield

## Detection: Check Before Sorting

**Always visualize drift before running spike sorting!**

```python
import spikeinterface.full as si
from spikeinterface.sortingcomponents.peak_detection import detect_peaks
from spikeinterface.sortingcomponents.peak_localization import localize_peaks

# Preprocess first (don't whiten - affects peak localization)
rec = si.highpass_filter(recording, freq_min=400.)
rec = si.common_reference(rec, operator='median', reference='global')

# Detect peaks
noise_levels = si.get_noise_levels(rec, return_in_uV=False)
peaks = detect_peaks(
    rec,
    method='locally_exclusive',
    noise_levels=noise_levels,
    detect_threshold=5,
    radius_um=50.,
    n_jobs=8,
    chunk_duration='1s',
    progress_bar=True
)

# Localize peaks
peak_locations = localize_peaks(
    rec, peaks,
    method='center_of_mass',
    n_jobs=8,
    chunk_duration='1s'
)

# Visualize drift
si.plot_drift_raster_map(
    peaks=peaks,
    peak_locations=peak_locations,
    recording=rec,
    clim=(-200, 0)  # Adjust color limits
)
```

### Interpreting Drift Plots

| Pattern | Interpretation | Action |
|---------|---------------|--------|
| Horizontal bands, stable | No significant drift | Skip correction |
| Diagonal bands (slow) | Gradual settling drift | Use motion correction |
| Rapid jumps | Brain pulsation or movement | Use non-rigid correction |
| Chaotic patterns | Severe instability | Consider discarding segment |

## Motion Correction Methods

### Quick Correction (Recommended Start)

```python
# Simple one-liner with preset
rec_corrected = si.correct_motion(
    recording=rec,
    preset='nonrigid_fast_and_accurate'
)
```

### Available Presets

| Preset | Speed | Accuracy | Best For |
|--------|-------|----------|----------|
| `rigid_fast` | Fast | Low | Quick check, small drift |
| `kilosort_like` | Medium | Good | Kilosort-compatible results |
| `nonrigid_accurate` | Slow | High | Publication-quality |
| `nonrigid_fast_and_accurate` | Medium | High | **Recommended default** |
| `dredge` | Slow | Highest | Best results, complex drift |
| `dredge_fast` | Medium | High | DREDge with less compute |

### Full Control Pipeline

```python
from spikeinterface.sortingcomponents.motion import (
    estimate_motion,
    interpolate_motion
)

# Step 1: Estimate motion
motion, temporal_bins, spatial_bins = estimate_motion(
    rec,
    peaks,
    peak_locations,
    method='decentralized',
    direction='y',
    rigid=False,          # Non-rigid for Neuropixels
    win_step_um=50,       # Spatial window step
    win_sigma_um=150,     # Spatial smoothing
    bin_s=2.0,            # Temporal bin size
    progress_bar=True
)

# Step 2: Visualize motion estimate
si.plot_motion(
    motion,
    temporal_bins,
    spatial_bins,
    recording=rec
)

# Step 3: Apply correction via interpolation
rec_corrected = interpolate_motion(
    recording=rec,
    motion=motion,
    temporal_bins=temporal_bins,
    spatial_bins=spatial_bins,
    border_mode='force_extrapolate'
)
```

### Save Motion Estimate

```python
# Save for later use
import numpy as np
np.savez('motion_estimate.npz',
         motion=motion,
         temporal_bins=temporal_bins,
         spatial_bins=spatial_bins)

# Load later
data = np.load('motion_estimate.npz')
motion = data['motion']
temporal_bins = data['temporal_bins']
spatial_bins = data['spatial_bins']
```

## DREDge: State-of-the-Art Method

DREDge (Decentralized Registration of Electrophysiology Data) is currently the best-performing motion correction method.

### Using DREDge Preset

```python
# AP-band motion estimation
rec_corrected = si.correct_motion(rec, preset='dredge')

# Or compute explicitly
motion, motion_info = si.compute_motion(
    rec,
    preset='dredge',
    output_motion_info=True,
    folder='motion_output/',
    **job_kwargs
)
```

### LFP-Based Motion Estimation

For very fast drift or when AP-band estimation fails:

```python
# Load LFP stream
lfp = si.read_spikeglx('/path/to/data', stream_name='imec0.lf')

# Estimate motion from LFP (faster, handles rapid drift)
motion_lfp, motion_info = si.compute_motion(
    lfp,
    preset='dredge_lfp',
    output_motion_info=True
)

# Apply to AP recording
rec_corrected = interpolate_motion(
    recording=rec,  # AP recording
    motion=motion_lfp,
    temporal_bins=motion_info['temporal_bins'],
    spatial_bins=motion_info['spatial_bins']
)
```

## Integration with Spike Sorting

### Option 1: Pre-correction (Recommended)

```python
# Correct before sorting
rec_corrected = si.correct_motion(rec, preset='nonrigid_fast_and_accurate')

# Save corrected recording
rec_corrected = rec_corrected.save(folder='preprocessed_motion_corrected/',
                                    format='binary', n_jobs=8)

# Run spike sorting on corrected data
sorting = si.run_sorter('kilosort4', rec_corrected, output_folder='ks4/')
```

### Option 2: Let Kilosort Handle It

Kilosort 2.5+ has built-in drift correction:

```python
sorting = si.run_sorter(
    'kilosort4',
    rec,  # Not motion corrected
    output_folder='ks4/',
    nblocks=5,  # Non-rigid blocks for drift correction
    do_correction=True  # Enable Kilosort's drift correction
)
```

### Option 3: Post-hoc Correction

```python
# Sort first
sorting = si.run_sorter('kilosort4', rec, output_folder='ks4/')

# Then estimate motion from sorted spikes
# (More accurate as it uses actual spike times)
from spikeinterface.sortingcomponents.motion import estimate_motion_from_sorting

motion = estimate_motion_from_sorting(sorting, rec)
```

## Parameters Deep Dive

### Peak Detection

```python
peaks = detect_peaks(
    rec,
    method='locally_exclusive',  # Best for dense probes
    noise_levels=noise_levels,
    detect_threshold=5,          # Lower = more peaks (noisier estimate)
    radius_um=50.,               # Exclusion radius
    exclude_sweep_ms=0.1,        # Temporal exclusion
)
```

### Motion Estimation

```python
motion = estimate_motion(
    rec, peaks, peak_locations,
    method='decentralized',      # 'decentralized' or 'iterative_template'
    direction='y',               # Along probe axis
    rigid=False,                 # False for non-rigid
    bin_s=2.0,                   # Temporal resolution (seconds)
    win_step_um=50,              # Spatial window step
    win_sigma_um=150,            # Spatial smoothing sigma
    margin_um=0,                 # Margin at probe edges
    win_scale_um=150,            # Window scale for weights
)
```

## Troubleshooting

### Over-correction (Wavy Patterns)

```python
# Increase temporal smoothing
motion = estimate_motion(..., bin_s=5.0)  # Larger bins

# Or use rigid correction for small drift
motion = estimate_motion(..., rigid=True)
```

### Under-correction (Drift Remains)

```python
# Decrease spatial window for finer non-rigid estimate
motion = estimate_motion(..., win_step_um=25, win_sigma_um=75)

# Use more peaks
peaks = detect_peaks(..., detect_threshold=4)  # Lower threshold
```

### Edge Artifacts

```python
rec_corrected = interpolate_motion(
    rec, motion, temporal_bins, spatial_bins,
    border_mode='force_extrapolate',  # or 'remove_channels'
    spatial_interpolation_method='kriging'
)
```

## Validation

After correction, re-visualize to confirm:

```python
# Re-detect peaks on corrected recording
peaks_corrected = detect_peaks(rec_corrected, ...)
peak_locations_corrected = localize_peaks(rec_corrected, peaks_corrected, ...)

# Plot before/after comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Before
si.plot_drift_raster_map(peaks, peak_locations, rec, ax=axes[0])
axes[0].set_title('Before Correction')

# After
si.plot_drift_raster_map(peaks_corrected, peak_locations_corrected,
                         rec_corrected, ax=axes[1])
axes[1].set_title('After Correction')
```

## References

- [SpikeInterface Motion Correction Docs](https://spikeinterface.readthedocs.io/en/stable/modules/motion_correction.html)
- [Handle Drift Tutorial](https://spikeinterface.readthedocs.io/en/stable/how_to/handle_drift.html)
- [DREDge GitHub](https://github.com/evarol/DREDge)
- Windolf et al. (2023) "DREDge: robust motion correction for high-density extracellular recordings"

---

## Reference: Preprocessing

# Neuropixels Preprocessing Reference

Comprehensive preprocessing techniques for Neuropixels neural recordings.

## Standard Preprocessing Pipeline

```python
import spikeinterface.full as si

# Load raw data
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# 1. Phase shift correction (for Neuropixels 1.0)
rec = si.phase_shift(recording)

# 2. Bandpass filter for spike detection
rec = si.bandpass_filter(rec, freq_min=300, freq_max=6000)

# 3. Common median reference (removes correlated noise)
rec = si.common_reference(rec, reference='global', operator='median')

# 4. Remove bad channels (optional)
rec = si.remove_bad_channels(rec, bad_channel_ids=bad_channels)
```

## Filtering Options

### Bandpass Filter
```python
# Standard AP band
rec = si.bandpass_filter(recording, freq_min=300, freq_max=6000)

# Wider band (preserve more waveform shape)
rec = si.bandpass_filter(recording, freq_min=150, freq_max=7500)

# Filter parameters
rec = si.bandpass_filter(
    recording,
    freq_min=300,
    freq_max=6000,
    filter_order=5,
    ftype='butter',  # 'butter', 'bessel', or 'cheby1'
    margin_ms=5.0    # Prevent edge artifacts
)
```

### Highpass Filter Only
```python
rec = si.highpass_filter(recording, freq_min=300)
```

### Notch Filter (Remove Line Noise)
```python
# Remove 60Hz and harmonics
rec = si.notch_filter(recording, freq=60, q=30)
rec = si.notch_filter(rec, freq=120, q=30)
rec = si.notch_filter(rec, freq=180, q=30)
```

## Reference Schemes

### Common Median Reference (Recommended)
```python
# Global median reference
rec = si.common_reference(recording, reference='global', operator='median')

# Per-shank reference (multi-shank probes)
rec = si.common_reference(recording, reference='global', operator='median',
                          groups=recording.get_channel_groups())
```

### Common Average Reference
```python
rec = si.common_reference(recording, reference='global', operator='average')
```

### Local Reference
```python
# Reference by local groups of channels
rec = si.common_reference(recording, reference='local', local_radius=(30, 100))
```

## Bad Channel Detection & Removal

### Automatic Detection
```python
# Detect bad channels
bad_channel_ids, channel_labels = si.detect_bad_channels(
    recording,
    method='coherence+psd',
    dead_channel_threshold=-0.5,
    noisy_channel_threshold=1.0,
    outside_channel_threshold=-0.3,
    n_neighbors=11
)

print(f"Bad channels: {bad_channel_ids}")
print(f"Labels: {dict(zip(bad_channel_ids, channel_labels))}")
```

### Remove Bad Channels
```python
rec_clean = si.remove_bad_channels(recording, bad_channel_ids=bad_channel_ids)
```

### Interpolate Bad Channels
```python
rec_interp = si.interpolate_bad_channels(recording, bad_channel_ids=bad_channel_ids)
```

## Motion Correction

### Estimate Motion
```python
# Estimate motion (drift)
motion, temporal_bins, spatial_bins = si.estimate_motion(
    recording,
    method='decentralized',
    rigid=False,              # Non-rigid motion estimation
    win_step_um=50,           # Spatial window step
    win_sigma_um=150,         # Spatial window sigma
    progress_bar=True
)
```

### Apply Motion Correction
```python
rec_corrected = si.correct_motion(
    recording,
    motion,
    temporal_bins,
    spatial_bins,
    interpolate_motion_border=True
)
```

### Motion Visualization
```python
si.plot_motion(motion, temporal_bins, spatial_bins)
```

## Probe-Specific Processing

### Neuropixels 1.0
```python
# Phase shift correction (different ADC per channel)
rec = si.phase_shift(recording)

# Then standard pipeline
rec = si.bandpass_filter(rec, freq_min=300, freq_max=6000)
rec = si.common_reference(rec, reference='global', operator='median')
```

### Neuropixels 2.0
```python
# No phase shift needed (single ADC)
rec = si.bandpass_filter(recording, freq_min=300, freq_max=6000)
rec = si.common_reference(rec, reference='global', operator='median')
```

### Multi-Shank (Neuropixels 2.0 4-shank)
```python
# Reference per shank
groups = recording.get_channel_groups()  # Returns shank assignments
rec = si.common_reference(recording, reference='global', operator='median', groups=groups)
```

## Whitening

```python
# Whiten data (decorrelate channels)
rec_whitened = si.whiten(recording, mode='local', local_radius_um=100)

# Global whitening
rec_whitened = si.whiten(recording, mode='global')
```

## Artifact Removal

### Remove Stimulation Artifacts
```python
# Define artifact times (in samples)
triggers = [10000, 20000, 30000]  # Sample indices

rec = si.remove_artifacts(
    recording,
    triggers,
    ms_before=0.5,
    ms_after=3.0,
    mode='cubic'  # 'zeros', 'linear', 'cubic'
)
```

### Blank Saturation Periods
```python
rec = si.blank_staturation(recording, threshold=0.95, fill_value=0)
```

## Saving Preprocessed Data

### Binary Format (Recommended)
```python
rec_preprocessed.save(folder='preprocessed/', format='binary', n_jobs=4)
```

### Zarr Format (Compressed)
```python
rec_preprocessed.save(folder='preprocessed.zarr', format='zarr')
```

### Save as Recording Extractor
```python
# Save for later use
rec_preprocessed.save(folder='preprocessed/', format='binary')

# Load later
rec_loaded = si.load_extractor('preprocessed/')
```

## Complete Pipeline Example

```python
import spikeinterface.full as si

def preprocess_neuropixels(data_path, output_path):
    """Standard Neuropixels preprocessing pipeline."""

    # Load data
    recording = si.read_spikeglx(data_path, stream_id='imec0.ap')
    print(f"Loaded: {recording.get_num_channels()} channels, "
          f"{recording.get_total_duration():.1f}s")

    # Phase shift (NP 1.0 only)
    rec = si.phase_shift(recording)

    # Filter
    rec = si.bandpass_filter(rec, freq_min=300, freq_max=6000)

    # Detect and remove bad channels
    bad_ids, _ = si.detect_bad_channels(rec)
    if len(bad_ids) > 0:
        print(f"Removing {len(bad_ids)} bad channels: {bad_ids}")
        rec = si.interpolate_bad_channels(rec, bad_ids)

    # Common reference
    rec = si.common_reference(rec, reference='global', operator='median')

    # Save
    rec.save(folder=output_path, format='binary', n_jobs=4)
    print(f"Saved to: {output_path}")

    return rec

# Usage
rec_preprocessed = preprocess_neuropixels(
    '/path/to/spikeglx/data',
    '/path/to/preprocessed'
)
```

## Performance Tips

```python
# Use parallel processing
rec.save(folder='output/', n_jobs=-1)  # Use all cores

# Use job kwargs for memory management
job_kwargs = dict(n_jobs=8, chunk_duration='1s', progress_bar=True)
rec.save(folder='output/', **job_kwargs)

# Set global job kwargs
si.set_global_job_kwargs(n_jobs=8, chunk_duration='1s')
```

---

## Reference: Quality_Metrics

# Quality Metrics Reference

Comprehensive guide to unit quality assessment using SpikeInterface metrics and Allen/IBL standards.

## Overview

Quality metrics assess three aspects of sorted units:

| Category | Question | Key Metrics |
|----------|----------|-------------|
| **Contamination** (Type I) | Are spikes from multiple neurons? | ISI violations, SNR |
| **Completeness** (Type II) | Are we missing spikes? | Amplitude cutoff, presence ratio |
| **Stability** | Is the unit stable over time? | Drift metrics, amplitude CV |

## Computing Quality Metrics

```python
import spikeinterface.full as si

# Create analyzer with computed waveforms
analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True)
analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.5, ms_after=2.0)
analyzer.compute('templates')
analyzer.compute('noise_levels')
analyzer.compute('spike_amplitudes')
analyzer.compute('principal_components', n_components=5)

# Compute all quality metrics
analyzer.compute('quality_metrics')

# Or compute specific metrics
analyzer.compute('quality_metrics', metric_names=[
    'firing_rate', 'snr', 'isi_violations_ratio',
    'presence_ratio', 'amplitude_cutoff'
])

# Get results
qm = analyzer.get_extension('quality_metrics').get_data()
print(qm.columns.tolist())  # Available metrics
```

## Metric Definitions & Thresholds

### Contamination Metrics

#### ISI Violations Ratio
Fraction of spikes violating refractory period. All neurons have a ~1.5ms refractory period.

```python
# Compute with custom refractory period
analyzer.compute('quality_metrics',
                 metric_names=['isi_violations_ratio'],
                 isi_threshold_ms=1.5,
                 min_isi_ms=0.0)
```

| Value | Interpretation |
|-------|---------------|
| < 0.01 | Excellent (well-isolated single unit) |
| 0.01 - 0.1 | Good (minor contamination) |
| 0.1 - 0.5 | Moderate (multi-unit activity likely) |
| > 0.5 | Poor (likely multi-unit) |

**Reference:** Hill et al. (2011) J Neurosci 31:8699-8705

#### Signal-to-Noise Ratio (SNR)
Ratio of peak waveform amplitude to background noise.

```python
analyzer.compute('quality_metrics', metric_names=['snr'])
```

| Value | Interpretation |
|-------|---------------|
| > 10 | Excellent |
| 5 - 10 | Good |
| 2 - 5 | Acceptable |
| < 2 | Poor (may be noise) |

#### Isolation Distance
Mahalanobis distance to nearest cluster in PCA space.

```python
analyzer.compute('quality_metrics',
                 metric_names=['isolation_distance'],
                 n_neighbors=4)
```

| Value | Interpretation |
|-------|---------------|
| > 50 | Well-isolated |
| 20 - 50 | Moderately isolated |
| < 20 | Poorly isolated |

#### L-ratio
Contamination measure based on Mahalanobis distances.

| Value | Interpretation |
|-------|---------------|
| < 0.05 | Well-isolated |
| 0.05 - 0.1 | Acceptable |
| > 0.1 | Contaminated |

#### D-prime
Discriminability between unit and nearest neighbor.

| Value | Interpretation |
|-------|---------------|
| > 8 | Excellent separation |
| 5 - 8 | Good separation |
| < 5 | Poor separation |

### Completeness Metrics

#### Amplitude Cutoff
Estimates fraction of spikes below detection threshold.

```python
analyzer.compute('quality_metrics',
                 metric_names=['amplitude_cutoff'],
                 peak_sign='neg')  # 'neg', 'pos', or 'both'
```

| Value | Interpretation |
|-------|---------------|
| < 0.01 | Excellent (nearly complete) |
| 0.01 - 0.1 | Good |
| 0.1 - 0.2 | Moderate (some missed spikes) |
| > 0.2 | Poor (many missed spikes) |

**For precise timing analyses:** Use < 0.01

#### Presence Ratio
Fraction of recording time with detected spikes.

```python
analyzer.compute('quality_metrics',
                 metric_names=['presence_ratio'],
                 bin_duration_s=60)  # 1-minute bins
```

| Value | Interpretation |
|-------|---------------|
| > 0.99 | Excellent |
| 0.9 - 0.99 | Good |
| 0.8 - 0.9 | Acceptable |
| < 0.8 | Unit may have drifted out |

### Stability Metrics

#### Drift Metrics
Measure unit movement over time.

```python
analyzer.compute('quality_metrics',
                 metric_names=['drift_ptp', 'drift_std', 'drift_mad'])
```

| Metric | Description | Good Value |
|--------|-------------|------------|
| `drift_ptp` | Peak-to-peak drift (μm) | < 40 |
| `drift_std` | Standard deviation of drift | < 10 |
| `drift_mad` | Median absolute deviation | < 10 |

#### Amplitude CV
Coefficient of variation of spike amplitudes.

| Value | Interpretation |
|-------|---------------|
| < 0.25 | Very stable |
| 0.25 - 0.5 | Acceptable |
| > 0.5 | Unstable (drift or contamination) |

### Cluster Quality Metrics

#### Silhouette Score
Cluster cohesion vs separation (-1 to 1).

| Value | Interpretation |
|-------|---------------|
| > 0.5 | Well-defined cluster |
| 0.25 - 0.5 | Moderate |
| < 0.25 | Overlapping clusters |

#### Nearest-Neighbor Metrics

```python
analyzer.compute('quality_metrics',
                 metric_names=['nn_hit_rate', 'nn_miss_rate'],
                 n_neighbors=4)
```

| Metric | Description | Good Value |
|--------|-------------|------------|
| `nn_hit_rate` | Fraction of spikes with same-unit neighbors | > 0.9 |
| `nn_miss_rate` | Fraction of spikes with other-unit neighbors | < 0.1 |

## Standard Filtering Criteria

### Allen Institute Defaults

```python
# Allen Visual Coding / Behavior defaults
allen_query = """
    presence_ratio > 0.95 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
"""
good_units = qm.query(allen_query).index.tolist()
```

### IBL Standards

```python
# IBL reproducible ephys criteria
ibl_query = """
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.1 and
    amplitude_cutoff < 0.1 and
    firing_rate > 0.1
"""
good_units = qm.query(ibl_query).index.tolist()
```

### Strict Single-Unit Criteria

```python
# For precise timing / spike-timing analyses
strict_query = """
    snr > 5 and
    presence_ratio > 0.99 and
    isi_violations_ratio < 0.01 and
    amplitude_cutoff < 0.01 and
    isolation_distance > 20 and
    drift_ptp < 40
"""
single_units = qm.query(strict_query).index.tolist()
```

### Multi-Unit Activity (MUA)

```python
# Include multi-unit activity
mua_query = """
    snr > 2 and
    presence_ratio > 0.5 and
    isi_violations_ratio < 1.0
"""
all_units = qm.query(mua_query).index.tolist()
```

## Visualization

### Quality Metric Summary

```python
# Plot all metrics
si.plot_quality_metrics(analyzer)
```

### Individual Metric Distributions

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

metrics = ['snr', 'isi_violations_ratio', 'presence_ratio',
           'amplitude_cutoff', 'firing_rate', 'drift_ptp']

for ax, metric in zip(axes.flat, metrics):
    ax.hist(qm[metric].dropna(), bins=50, edgecolor='black')
    ax.set_xlabel(metric)
    ax.set_ylabel('Count')
    # Add threshold line
    if metric == 'snr':
        ax.axvline(5, color='r', linestyle='--', label='threshold')
    elif metric == 'isi_violations_ratio':
        ax.axvline(0.01, color='r', linestyle='--')
    elif metric == 'presence_ratio':
        ax.axvline(0.9, color='r', linestyle='--')

plt.tight_layout()
```

### Unit Quality Summary

```python
# Comprehensive unit summary plot
si.plot_unit_summary(analyzer, unit_id=0)
```

### Quality vs Firing Rate

```python
fig, ax = plt.subplots()
scatter = ax.scatter(qm['firing_rate'], qm['snr'],
                     c=qm['isi_violations_ratio'],
                     cmap='RdYlGn_r', alpha=0.6)
ax.set_xlabel('Firing Rate (Hz)')
ax.set_ylabel('SNR')
plt.colorbar(scatter, label='ISI Violations')
ax.set_xscale('log')
```

## Compute All Metrics at Once

```python
# Full quality metrics computation
all_metric_names = [
    # Firing properties
    'firing_rate', 'presence_ratio',
    # Waveform
    'snr', 'amplitude_cutoff', 'amplitude_cv_median', 'amplitude_cv_range',
    # ISI
    'isi_violations_ratio', 'isi_violations_count',
    # Drift
    'drift_ptp', 'drift_std', 'drift_mad',
    # Isolation (require PCA)
    'isolation_distance', 'l_ratio', 'd_prime',
    # Nearest neighbor (require PCA)
    'nn_hit_rate', 'nn_miss_rate',
    # Cluster quality
    'silhouette_score',
    # Synchrony
    'sync_spike_2', 'sync_spike_4', 'sync_spike_8',
]

# Compute PCA first (required for some metrics)
analyzer.compute('principal_components', n_components=5)

# Compute metrics
analyzer.compute('quality_metrics', metric_names=all_metric_names)
qm = analyzer.get_extension('quality_metrics').get_data()

# Save to CSV
qm.to_csv('quality_metrics.csv')
```

## Custom Metrics

```python
from spikeinterface.qualitymetrics import compute_firing_rates, compute_snrs

# Compute individual metrics
firing_rates = compute_firing_rates(sorting)
snrs = compute_snrs(analyzer)

# Add custom metric to DataFrame
qm['custom_score'] = qm['snr'] * qm['presence_ratio'] / (qm['isi_violations_ratio'] + 0.001)
```

## References

- [SpikeInterface Quality Metrics](https://spikeinterface.readthedocs.io/en/latest/modules/qualitymetrics.html)
- [Allen Institute ecephys_quality_metrics](https://allensdk.readthedocs.io/en/latest/_static/examples/nb/ecephys_quality_metrics.html)
- Hill et al. (2011) "Quality metrics to accompany spike sorting of extracellular signals"
- Siegle et al. (2021) "Survey of spiking in the mouse visual system reveals functional hierarchy"

---

## Reference: Spike_Sorting

# Spike Sorting Reference

Comprehensive guide to spike sorting Neuropixels data.

## Available Sorters

| Sorter | GPU Required | Speed | Quality | Best For |
|--------|--------------|-------|---------|----------|
| **Kilosort4** | Yes (CUDA) | Fast | Excellent | Production use |
| **Kilosort3** | Yes (CUDA) | Fast | Very Good | Legacy compatibility |
| **Kilosort2.5** | Yes (CUDA) | Fast | Good | Older pipelines |
| **SpykingCircus2** | No | Medium | Good | CPU-only systems |
| **Mountainsort5** | No | Medium | Good | Small recordings |
| **Tridesclous2** | No | Medium | Good | Interactive sorting |

## Kilosort4 (Recommended)

### Installation
```bash
pip install kilosort
```

### Basic Usage
```python
import spikeinterface.full as si

# Run Kilosort4
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4_output',
    verbose=True
)

print(f"Found {len(sorting.unit_ids)} units")
```

### Custom Parameters
```python
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4_output',
    # Detection
    Th_universal=9,        # Spike detection threshold
    Th_learned=8,          # Learned threshold
    # Templates
    dmin=15,               # Min vertical distance between templates (um)
    dminx=12,              # Min horizontal distance (um)
    nblocks=5,             # Number of non-rigid blocks
    # Clustering
    max_channel_distance=None,  # Max distance for template channel
    # Output
    do_CAR=False,          # Skip CAR (done in preprocessing)
    skip_kilosort_preprocessing=True,
    save_extra_kwargs=True
)
```

### Kilosort4 Full Parameters
```python
# Get all available parameters
params = si.get_default_sorter_params('kilosort4')
print(params)

# Key parameters:
ks4_params = {
    # Detection
    'Th_universal': 9,      # Universal threshold for spike detection
    'Th_learned': 8,        # Threshold for learned templates
    'spkTh': -6,            # Spike threshold during extraction

    # Clustering
    'dmin': 15,             # Min distance between clusters (um)
    'dminx': 12,            # Min horizontal distance (um)
    'nblocks': 5,           # Blocks for non-rigid drift correction

    # Templates
    'n_templates': 6,       # Number of universal templates per group
    'nt': 61,               # Number of time samples in template

    # Performance
    'batch_size': 60000,    # Batch size in samples
    'nfilt_factor': 8,      # Factor for number of filters
}
```

## Kilosort3

### Usage
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_output',
    # Key parameters
    detect_threshold=6,
    projection_threshold=[9, 9],
    preclust_threshold=8,
    car=False,  # CAR done in preprocessing
    freq_min=300,
)
```

## SpykingCircus2 (CPU-Only)

### Installation
```bash
pip install spykingcircus
```

### Usage
```python
sorting = si.run_sorter(
    'spykingcircus2',
    recording,
    output_folder='sc2_output',
    # Parameters
    detect_threshold=5,
    selection_method='all',
)
```

## Mountainsort5 (CPU-Only)

### Installation
```bash
pip install mountainsort5
```

### Usage
```python
sorting = si.run_sorter(
    'mountainsort5',
    recording,
    output_folder='ms5_output',
    # Parameters
    detect_threshold=5.0,
    scheme='2',  # '1', '2', or '3'
)
```

## Running Multiple Sorters

### Compare Sorters
```python
# Run multiple sorters
sorting_ks4 = si.run_sorter('kilosort4', recording, output_folder='ks4/')
sorting_sc2 = si.run_sorter('spykingcircus2', recording, output_folder='sc2/')
sorting_ms5 = si.run_sorter('mountainsort5', recording, output_folder='ms5/')

# Compare results
comparison = si.compare_multiple_sorters(
    [sorting_ks4, sorting_sc2, sorting_ms5],
    name_list=['KS4', 'SC2', 'MS5']
)

# Get agreement scores
agreement = comparison.get_agreement_sorting()
```

### Ensemble Sorting
```python
# Create consensus sorting
sorting_ensemble = si.create_ensemble_sorting(
    [sorting_ks4, sorting_sc2, sorting_ms5],
    voting_method='agreement',
    min_agreement=2  # Unit must be found by at least 2 sorters
)
```

## Sorting in Docker/Singularity

### Using Docker
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_docker/',
    docker_image='spikeinterface/kilosort3-compiled-base:latest',
    verbose=True
)
```

### Using Singularity
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_singularity/',
    singularity_image='/path/to/kilosort3.sif',
    verbose=True
)
```

## Long Recording Strategy

### Concatenate Recordings
```python
# Multiple recording files
recordings = [
    si.read_spikeglx(f'/path/to/recording_{i}', stream_id='imec0.ap')
    for i in range(3)
]

# Concatenate
recording_concat = si.concatenate_recordings(recordings)

# Sort
sorting = si.run_sorter('kilosort4', recording_concat, output_folder='ks4/')

# Split back by original recording
sortings_split = si.split_sorting(sorting, recording_concat)
```

### Sort by Segment
```python
# For very long recordings, sort segments separately
from pathlib import Path

segments_output = Path('sorting_segments')
sortings = []

for i, segment in enumerate(recording.split_by_times([0, 3600, 7200, 10800])):
    sorting_seg = si.run_sorter(
        'kilosort4',
        segment,
        output_folder=segments_output / f'segment_{i}'
    )
    sortings.append(sorting_seg)
```

## Post-Sorting Curation

### Manual Curation with Phy
```python
# Export to Phy format
analyzer = si.create_sorting_analyzer(sorting, recording)
analyzer.compute(['random_spikes', 'waveforms', 'templates'])
si.export_to_phy(analyzer, output_folder='phy_export/')

# Open Phy
# Run in terminal: phy template-gui phy_export/params.py
```

### Load Phy Curation
```python
# After manual curation in Phy
sorting_curated = si.read_phy('phy_export/')

# Or apply Phy labels
sorting_curated = si.apply_phy_curation(sorting, 'phy_export/')
```

### Automatic Curation
```python
# Remove units below quality threshold
analyzer = si.create_sorting_analyzer(sorting, recording)
analyzer.compute('quality_metrics')

qm = analyzer.get_extension('quality_metrics').get_data()

# Define quality criteria
query = "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
good_unit_ids = qm.query(query).index.tolist()

sorting_clean = sorting.select_units(good_unit_ids)
print(f"Kept {len(good_unit_ids)}/{len(sorting.unit_ids)} units")
```

## Sorting Metrics

### Check Sorter Output
```python
# Basic stats
print(f"Units found: {len(sorting.unit_ids)}")
print(f"Total spikes: {sorting.get_total_num_spikes()}")

# Per-unit spike counts
for unit_id in sorting.unit_ids[:10]:
    n_spikes = len(sorting.get_unit_spike_train(unit_id))
    print(f"Unit {unit_id}: {n_spikes} spikes")
```

### Firing Rates
```python
# Compute firing rates
duration = recording.get_total_duration()
for unit_id in sorting.unit_ids:
    n_spikes = len(sorting.get_unit_spike_train(unit_id))
    fr = n_spikes / duration
    print(f"Unit {unit_id}: {fr:.2f} Hz")
```

## Troubleshooting

### Common Issues

**Out of GPU Memory**
```python
# Reduce batch size
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    batch_size=30000  # Smaller batch
)
```

**Too Few Units Found**
```python
# Lower detection threshold
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    Th_universal=7,  # Lower from default 9
    Th_learned=6
)
```

**Too Many Units (Over-splitting)**
```python
# Increase minimum distance between templates
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    dmin=20,   # Increase from 15
    dminx=16   # Increase from 12
)
```

**Check GPU Availability**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

---

## Reference: Api_Reference

# API Reference

Quick reference for neuropixels_analysis functions organized by module.

## Core Module

### load_recording

```python
npa.load_recording(
    path: str,
    format: str = 'auto',  # 'spikeglx', 'openephys', 'nwb'
    stream_id: str = None,  # e.g., 'imec0.ap'
) -> Recording
```

Load Neuropixels recording from various formats.

### run_pipeline

```python
npa.run_pipeline(
    recording: Recording,
    output_dir: str,
    sorter: str = 'kilosort4',
    preprocess: bool = True,
    correct_motion: bool = True,
    postprocess: bool = True,
    curate: bool = True,
    curation_method: str = 'allen',
) -> dict
```

Run complete analysis pipeline. Returns dictionary with all results.

## Preprocessing Module

### preprocess

```python
npa.preprocess(
    recording: Recording,
    freq_min: float = 300,
    freq_max: float = 6000,
    phase_shift: bool = True,
    common_ref: bool = True,
    bad_channel_detection: bool = True,
) -> Recording
```

Apply standard preprocessing chain.

### detect_bad_channels

```python
npa.detect_bad_channels(
    recording: Recording,
    method: str = 'coherence+psd',
    **kwargs,
) -> list
```

Detect and return list of bad channel IDs.

### apply_filters

```python
npa.apply_filters(
    recording: Recording,
    freq_min: float = 300,
    freq_max: float = 6000,
    filter_type: str = 'bandpass',
) -> Recording
```

Apply frequency filters.

### common_reference

```python
npa.common_reference(
    recording: Recording,
    operator: str = 'median',
    reference: str = 'global',
) -> Recording
```

Apply common reference (CMR/CAR).

## Motion Module

### check_drift

```python
npa.check_drift(
    recording: Recording,
    plot: bool = True,
    output: str = None,
) -> dict
```

Check recording for drift. Returns drift statistics.

### estimate_motion

```python
npa.estimate_motion(
    recording: Recording,
    preset: str = 'kilosort_like',
    **kwargs,
) -> dict
```

Estimate motion without applying correction.

### correct_motion

```python
npa.correct_motion(
    recording: Recording,
    preset: str = 'nonrigid_accurate',
    folder: str = None,
    **kwargs,
) -> Recording
```

Apply motion correction.

**Presets:**
- `'kilosort_like'`: Fast, rigid correction
- `'nonrigid_accurate'`: Slower, better for severe drift
- `'nonrigid_fast_and_accurate'`: Balanced option

## Sorting Module

### run_sorting

```python
npa.run_sorting(
    recording: Recording,
    sorter: str = 'kilosort4',
    output_folder: str = None,
    sorter_params: dict = None,
    **kwargs,
) -> Sorting
```

Run spike sorter.

**Supported sorters:**
- `'kilosort4'`: GPU-based, recommended
- `'kilosort3'`: Legacy, requires MATLAB
- `'spykingcircus2'`: CPU-based alternative
- `'mountainsort5'`: Fast, good for short recordings

### compare_sorters

```python
npa.compare_sorters(
    sortings: list,
    delta_time: float = 0.4,  # ms
    match_score: float = 0.5,
) -> Comparison
```

Compare results from multiple sorters.

## Postprocessing Module

### create_analyzer

```python
npa.create_analyzer(
    sorting: Sorting,
    recording: Recording,
    output_folder: str = None,
    sparse: bool = True,
) -> SortingAnalyzer
```

Create SortingAnalyzer for postprocessing.

### postprocess

```python
npa.postprocess(
    sorting: Sorting,
    recording: Recording,
    output_folder: str = None,
    compute_all: bool = True,
    n_jobs: int = -1,
) -> tuple[SortingAnalyzer, DataFrame]
```

Full postprocessing. Returns (analyzer, metrics).

### compute_quality_metrics

```python
npa.compute_quality_metrics(
    analyzer: SortingAnalyzer,
    metric_names: list = None,  # None = all
    **kwargs,
) -> DataFrame
```

Compute quality metrics for all units.

**Available metrics:**
- `snr`: Signal-to-noise ratio
- `isi_violations_ratio`: ISI violations
- `presence_ratio`: Recording presence
- `amplitude_cutoff`: Amplitude distribution cutoff
- `firing_rate`: Average firing rate
- `amplitude_cv`: Amplitude coefficient of variation
- `sliding_rp_violation`: Sliding window refractory violations
- `d_prime`: Isolation quality
- `nearest_neighbor`: Nearest-neighbor overlap

## Curation Module

### curate

```python
npa.curate(
    metrics: DataFrame,
    method: str = 'allen',  # 'allen', 'ibl', 'strict', 'custom'
    **thresholds,
) -> dict
```

Apply automated curation. Returns {unit_id: label}.

### auto_classify

```python
npa.auto_classify(
    metrics: DataFrame,
    snr_threshold: float = 5.0,
    isi_threshold: float = 0.01,
    presence_threshold: float = 0.9,
) -> dict
```

Classify units based on custom thresholds.

### filter_units

```python
npa.filter_units(
    sorting: Sorting,
    labels: dict,
    keep: list = ['good'],
) -> Sorting
```

Filter sorting to keep only specified labels.

## AI Curation Module

### generate_unit_report

```python
npa.generate_unit_report(
    analyzer: SortingAnalyzer,
    unit_id: int,
    output_dir: str = None,
    figsize: tuple = (16, 12),
) -> dict
```

Generate visual report for AI analysis.

Returns:
- `'image_path'`: Path to saved figure
- `'image_base64'`: Base64 encoded image
- `'metrics'`: Quality metrics dict
- `'unit_id'`: Unit ID

### analyze_unit_visually

```python
npa.analyze_unit_visually(
    analyzer: SortingAnalyzer,
    unit_id: int,
    api_client: Any = None,
    model: str = 'claude-opus-4.5',
    task: str = 'quality_assessment',
    custom_prompt: str = None,
) -> dict
```

Analyze unit using vision-language model.

**Tasks:**
- `'quality_assessment'`: Classify as good/mua/noise
- `'merge_candidate'`: Check if units should merge
- `'drift_assessment'`: Assess motion/drift

### batch_visual_curation

```python
npa.batch_visual_curation(
    analyzer: SortingAnalyzer,
    unit_ids: list = None,
    api_client: Any = None,
    model: str = 'claude-opus-4.5',
    output_dir: str = None,
    progress_callback: callable = None,
) -> dict
```

Run visual curation on multiple units.

### CurationSession

```python
session = npa.CurationSession.create(
    analyzer: SortingAnalyzer,
    output_dir: str,
    session_id: str = None,
    unit_ids: list = None,
    sort_by_confidence: bool = True,
)

# Navigation
session.current_unit() -> UnitCuration
session.next_unit() -> UnitCuration
session.prev_unit() -> UnitCuration
session.go_to_unit(unit_id: int) -> UnitCuration

# Decisions
session.set_decision(unit_id, decision, notes='')
session.set_ai_classification(unit_id, classification)

# Export
session.get_final_labels() -> dict
session.export_decisions(output_path) -> DataFrame
session.get_summary() -> dict

# Persistence
session.save()
session = npa.CurationSession.load(session_dir)
```

## Visualization Module

### plot_drift

```python
npa.plot_drift(
    recording: Recording,
    motion: dict = None,
    output: str = None,
    figsize: tuple = (12, 8),
)
```

Plot drift/motion map.

### plot_quality_metrics

```python
npa.plot_quality_metrics(
    analyzer: SortingAnalyzer,
    metrics: DataFrame = None,
    output: str = None,
)
```

Plot quality metrics overview.

### plot_unit_summary

```python
npa.plot_unit_summary(
    analyzer: SortingAnalyzer,
    unit_id: int,
    output: str = None,
)
```

Plot comprehensive unit summary.

## SpikeInterface Integration

All neuropixels_analysis functions work with SpikeInterface objects:

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# SpikeInterface recording works with npa functions
recording = si.read_spikeglx('/path/')
rec = npa.preprocess(recording)

# Access SpikeInterface directly for advanced usage
rec_filtered = si.bandpass_filter(recording, freq_min=300, freq_max=6000)
```

## Common Parameters

### Recording parameters
- `freq_min`: Highpass cutoff (Hz)
- `freq_max`: Lowpass cutoff (Hz)
- `n_jobs`: Parallel jobs (-1 = all cores)

### Sorting parameters
- `output_folder`: Where to save results
- `sorter_params`: Dict of sorter-specific params

### Quality metric thresholds
- `snr_threshold`: SNR cutoff (typically 5)
- `isi_threshold`: ISI violations cutoff (typically 0.01)
- `presence_threshold`: Presence ratio cutoff (typically 0.9)

---

## Reference: Plotting_Guide

# Plotting Guide

Comprehensive guide for creating publication-quality visualizations from Neuropixels data.

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np
import spikeinterface.full as si
import spikeinterface.widgets as sw
import neuropixels_analysis as npa

# High-quality settings
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
```

## Drift and Motion Plots

### Basic Drift Map

```python
# Using npa
npa.plot_drift(recording, output='drift_map.png')

# Using SpikeInterface widgets
from spikeinterface.preprocessing import detect_peaks, localize_peaks

peaks = detect_peaks(recording, method='locally_exclusive')
peak_locations = localize_peaks(recording, peaks, method='center_of_mass')

sw.plot_drift_raster_map(
    peaks=peaks,
    peak_locations=peak_locations,
    recording=recording,
    clim=(-50, 50),
)
plt.savefig('drift_raster.png', bbox_inches='tight')
```

### Motion Estimate Visualization

```python
motion_info = npa.estimate_motion(recording)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Motion over time
ax = axes[0]
for i in range(motion_info['motion'].shape[1]):
    ax.plot(motion_info['temporal_bins'], motion_info['motion'][:, i], alpha=0.5)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Motion (um)')
ax.set_title('Estimated Motion')

# Motion histogram
ax = axes[1]
ax.hist(motion_info['motion'].flatten(), bins=50, edgecolor='black')
ax.set_xlabel('Motion (um)')
ax.set_ylabel('Count')
ax.set_title('Motion Distribution')

plt.tight_layout()
plt.savefig('motion_analysis.png', dpi=300)
```

## Waveform Plots

### Single Unit Waveforms

```python
unit_id = 0

# Basic waveforms
sw.plot_unit_waveforms(analyzer, unit_ids=[unit_id])
plt.savefig(f'unit_{unit_id}_waveforms.png')

# With density map
sw.plot_unit_waveform_density_map(analyzer, unit_ids=[unit_id])
plt.savefig(f'unit_{unit_id}_density.png')
```

### Template Comparison

```python
# Compare multiple units
unit_ids = [0, 1, 2, 3]
sw.plot_unit_templates(analyzer, unit_ids=unit_ids)
plt.savefig('template_comparison.png')
```

### Waveforms on Probe

```python
# Show waveforms spatially on probe
sw.plot_unit_waveforms_on_probe(
    analyzer,
    unit_ids=[unit_id],
    plot_channels=True,
)
plt.savefig(f'unit_{unit_id}_probe.png')
```

## Quality Metrics Visualization

### Metrics Overview

```python
npa.plot_quality_metrics(analyzer, metrics, output='quality_overview.png')
```

### Metrics Distribution

```python
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

metric_names = ['snr', 'isi_violations_ratio', 'presence_ratio',
                'amplitude_cutoff', 'firing_rate', 'amplitude_cv']

for ax, metric in zip(axes.flat, metric_names):
    if metric in metrics.columns:
        values = metrics[metric].dropna()
        ax.hist(values, bins=30, edgecolor='black', alpha=0.7)
        ax.axvline(values.median(), color='red', linestyle='--', label='median')
        ax.set_xlabel(metric)
        ax.set_ylabel('Count')
        ax.legend()

plt.tight_layout()
plt.savefig('metrics_distribution.png', dpi=300)
```

### Metrics Scatter Matrix

```python
import pandas as pd

key_metrics = ['snr', 'isi_violations_ratio', 'presence_ratio', 'firing_rate']
pd.plotting.scatter_matrix(
    metrics[key_metrics],
    figsize=(10, 10),
    alpha=0.5,
    diagonal='hist',
)
plt.savefig('metrics_scatter.png', dpi=300)
```

### Metrics vs Labels

```python
labels_series = pd.Series(labels)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, metric in zip(axes, ['snr', 'isi_violations_ratio', 'presence_ratio']):
    for label in ['good', 'mua', 'noise']:
        mask = labels_series == label
        if mask.any():
            ax.hist(metrics.loc[mask.index[mask], metric],
                   alpha=0.5, label=label, bins=20)
    ax.set_xlabel(metric)
    ax.legend()

plt.tight_layout()
plt.savefig('metrics_by_label.png', dpi=300)
```

## Correlogram Plots

### Autocorrelogram

```python
sw.plot_autocorrelograms(
    analyzer,
    unit_ids=[unit_id],
    window_ms=50,
    bin_ms=1,
)
plt.savefig(f'unit_{unit_id}_acg.png')
```

### Cross-correlograms

```python
unit_pairs = [(0, 1), (0, 2), (1, 2)]
sw.plot_crosscorrelograms(
    analyzer,
    unit_pairs=unit_pairs,
    window_ms=50,
    bin_ms=1,
)
plt.savefig('crosscorrelograms.png')
```

### Correlogram Matrix

```python
sw.plot_autocorrelograms(
    analyzer,
    unit_ids=analyzer.sorting.unit_ids[:10],  # First 10 units
)
plt.savefig('acg_matrix.png')
```

## Spike Train Plots

### Raster Plot

```python
sw.plot_rasters(
    sorting,
    time_range=(0, 30),  # First 30 seconds
    unit_ids=unit_ids[:5],
)
plt.savefig('raster.png')
```

### Firing Rate Over Time

```python
unit_id = 0
spike_train = sorting.get_unit_spike_train(unit_id)
fs = recording.get_sampling_frequency()
times = spike_train / fs

# Compute firing rate histogram
bin_width = 1.0  # seconds
bins = np.arange(0, recording.get_total_duration(), bin_width)
hist, _ = np.histogram(times, bins=bins)
firing_rate = hist / bin_width

plt.figure(figsize=(12, 3))
plt.bar(bins[:-1], firing_rate, width=bin_width, edgecolor='none')
plt.xlabel('Time (s)')
plt.ylabel('Firing rate (Hz)')
plt.title(f'Unit {unit_id} firing rate')
plt.savefig(f'unit_{unit_id}_firing_rate.png', dpi=300)
```

## Probe and Location Plots

### Probe Layout

```python
sw.plot_probe_map(recording, with_channel_ids=True)
plt.savefig('probe_layout.png')
```

### Unit Locations on Probe

```python
sw.plot_unit_locations(analyzer, with_channel_ids=True)
plt.savefig('unit_locations.png')
```

### Spike Locations

```python
sw.plot_spike_locations(analyzer, unit_ids=[unit_id])
plt.savefig(f'unit_{unit_id}_spike_locations.png')
```

## Amplitude Plots

### Amplitudes Over Time

```python
sw.plot_amplitudes(
    analyzer,
    unit_ids=[unit_id],
    plot_histograms=True,
)
plt.savefig(f'unit_{unit_id}_amplitudes.png')
```

### Amplitude Distribution

```python
amplitudes = analyzer.get_extension('spike_amplitudes').get_data()
spike_vector = sorting.to_spike_vector()
unit_idx = list(sorting.unit_ids).index(unit_id)
unit_mask = spike_vector['unit_index'] == unit_idx
unit_amps = amplitudes[unit_mask]

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(unit_amps, bins=50, edgecolor='black', alpha=0.7)
ax.axvline(np.median(unit_amps), color='red', linestyle='--', label='median')
ax.set_xlabel('Amplitude (uV)')
ax.set_ylabel('Count')
ax.set_title(f'Unit {unit_id} Amplitude Distribution')
ax.legend()
plt.savefig(f'unit_{unit_id}_amp_dist.png', dpi=300)
```

## ISI Plots

### ISI Histogram

```python
sw.plot_isi_distribution(
    analyzer,
    unit_ids=[unit_id],
    window_ms=100,
    bin_ms=1,
)
plt.savefig(f'unit_{unit_id}_isi.png')
```

### ISI with Refractory Markers

```python
spike_train = sorting.get_unit_spike_train(unit_id)
fs = recording.get_sampling_frequency()
isis = np.diff(spike_train) / fs * 1000  # ms

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(isis[isis < 100], bins=100, edgecolor='black', alpha=0.7)
ax.axvline(1.5, color='red', linestyle='--', label='1.5ms refractory')
ax.axvline(3.0, color='orange', linestyle='--', label='3ms threshold')
ax.set_xlabel('ISI (ms)')
ax.set_ylabel('Count')
ax.set_title(f'Unit {unit_id} ISI Distribution')
ax.legend()
plt.savefig(f'unit_{unit_id}_isi_detailed.png', dpi=300)
```

## Summary Plots

### Unit Summary Panel

```python
npa.plot_unit_summary(analyzer, unit_id, output=f'unit_{unit_id}_summary.png')
```

### Manual Multi-Panel Summary

```python
fig = plt.figure(figsize=(16, 12))

# Waveforms
ax1 = fig.add_subplot(2, 3, 1)
wfs = analyzer.get_extension('waveforms').get_waveforms(unit_id)
for i in range(min(50, wfs.shape[0])):
    ax1.plot(wfs[i, :, 0], 'k', alpha=0.1, linewidth=0.5)
template = wfs.mean(axis=0)[:, 0]
ax1.plot(template, 'b', linewidth=2)
ax1.set_title('Waveforms')

# Template
ax2 = fig.add_subplot(2, 3, 2)
templates_ext = analyzer.get_extension('templates')
template = templates_ext.get_unit_template(unit_id, operator='average')
template_std = templates_ext.get_unit_template(unit_id, operator='std')
x = range(template.shape[0])
ax2.plot(x, template[:, 0], 'b', linewidth=2)
ax2.fill_between(x, template[:, 0] - template_std[:, 0],
                 template[:, 0] + template_std[:, 0], alpha=0.3)
ax2.set_title('Template')

# Autocorrelogram
ax3 = fig.add_subplot(2, 3, 3)
correlograms = analyzer.get_extension('correlograms')
ccg, bins = correlograms.get_data()
unit_idx = list(sorting.unit_ids).index(unit_id)
ax3.bar(bins[:-1], ccg[unit_idx, unit_idx, :], width=bins[1]-bins[0], color='gray')
ax3.axvline(0, color='r', linestyle='--', alpha=0.5)
ax3.set_title('Autocorrelogram')

# Amplitudes
ax4 = fig.add_subplot(2, 3, 4)
amps_ext = analyzer.get_extension('spike_amplitudes')
amps = amps_ext.get_data()
spike_vector = sorting.to_spike_vector()
unit_mask = spike_vector['unit_index'] == unit_idx
unit_times = spike_vector['sample_index'][unit_mask] / fs
unit_amps = amps[unit_mask]
ax4.scatter(unit_times, unit_amps, s=1, alpha=0.3)
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Amplitude')
ax4.set_title('Amplitudes')

# ISI
ax5 = fig.add_subplot(2, 3, 5)
isis = np.diff(sorting.get_unit_spike_train(unit_id)) / fs * 1000
ax5.hist(isis[isis < 100], bins=50, color='gray', edgecolor='black')
ax5.axvline(1.5, color='r', linestyle='--')
ax5.set_xlabel('ISI (ms)')
ax5.set_title('ISI Distribution')

# Metrics
ax6 = fig.add_subplot(2, 3, 6)
unit_metrics = metrics.loc[unit_id]
text_lines = [f"{k}: {v:.4f}" for k, v in unit_metrics.items() if not np.isnan(v)]
ax6.text(0.1, 0.9, '\n'.join(text_lines[:8]), transform=ax6.transAxes,
         verticalalignment='top', fontsize=10, family='monospace')
ax6.axis('off')
ax6.set_title('Metrics')

plt.tight_layout()
plt.savefig(f'unit_{unit_id}_full_summary.png', dpi=300)
```

## Publication-Quality Settings

### Figure Sizes

```python
# Single column (3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 3))

# Double column (7 inches)
fig, ax = plt.subplots(figsize=(7, 4))

# Full page
fig, ax = plt.subplots(figsize=(7, 9))
```

### Font Settings

```python
plt.rcParams.update({
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'font.family': 'Arial',
})
```

### Export Settings

```python
# For publications
plt.savefig('figure.pdf', format='pdf', bbox_inches='tight')
plt.savefig('figure.svg', format='svg', bbox_inches='tight')

# High-res PNG
plt.savefig('figure.png', dpi=600, bbox_inches='tight', facecolor='white')
```

### Color Palettes

```python
# Colorblind-friendly
colors = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#F0E442']

# For good/mua/noise
label_colors = {'good': '#2ecc71', 'mua': '#f39c12', 'noise': '#e74c3c'}
```

---

## Reference: Standard_Workflow

# Standard Neuropixels Analysis Workflow

Complete step-by-step guide for analyzing Neuropixels recordings from raw data to curated units.

## Overview

This reference documents the complete analysis pipeline:

```
Raw Recording → Preprocessing → Motion Correction → Spike Sorting →
Postprocessing → Quality Metrics → Curation → Export
```

## 1. Data Loading

### Supported Formats

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# SpikeGLX (most common)
recording = si.read_spikeglx('/path/to/run/', stream_id='imec0.ap')

# Open Ephys
recording = si.read_openephys('/path/to/experiment/')

# NWB format
recording = si.read_nwb('/path/to/file.nwb')

# Or use our convenience wrapper
recording = npa.load_recording('/path/to/data/', format='spikeglx')
```

### Verify Recording Properties

```python
# Basic properties
print(f"Channels: {recording.get_num_channels()}")
print(f"Duration: {recording.get_total_duration():.1f}s")
print(f"Sampling rate: {recording.get_sampling_frequency()}Hz")

# Probe geometry
print(f"Probe: {recording.get_probe().name}")

# Channel locations
locations = recording.get_channel_locations()
```

## 2. Preprocessing

### Standard Preprocessing Chain

```python
# Option 1: Full pipeline (recommended)
rec_preprocessed = npa.preprocess(recording)

# Option 2: Step-by-step control
rec = si.bandpass_filter(recording, freq_min=300, freq_max=6000)
rec = si.phase_shift(rec)  # Correct ADC phase
bad_channels = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_channels)
rec = si.common_reference(rec, operator='median')
rec_preprocessed = rec
```

### IBL-Style Destriping

For recordings with strong artifacts:

```python
from ibldsp.voltage import decompress_destripe_cbin

# IBL destriping (very effective)
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)
rec = si.highpass_spatial_filter(rec)  # Destriping
rec = si.common_reference(rec, reference='global', operator='median')
```

### Save Preprocessed Data

```python
# Save for reuse (speeds up iteration)
rec_preprocessed.save(folder='preprocessed/', n_jobs=4)
```

## 3. Motion/Drift Correction

### Check if Correction Needed

```python
# Estimate motion
motion_info = npa.estimate_motion(rec_preprocessed, preset='kilosort_like')

# Visualize drift
npa.plot_drift(rec_preprocessed, motion_info, output='drift_map.png')

# Check magnitude
if motion_info['motion'].max() > 10:  # microns
    print("Significant drift detected - correction recommended")
```

### Apply Correction

```python
# DREDge-based correction (default)
rec_corrected = npa.correct_motion(
    rec_preprocessed,
    preset='nonrigid_accurate',  # or 'kilosort_like' for speed
)

# Or full control
from spikeinterface.preprocessing import correct_motion

rec_corrected = correct_motion(
    rec_preprocessed,
    preset='nonrigid_accurate',
    folder='motion_output/',
    output_motion=True,
)
```

## 4. Spike Sorting

### Recommended: Kilosort4

```python
# Run Kilosort4 (requires GPU)
sorting = npa.run_sorting(
    rec_corrected,
    sorter='kilosort4',
    output_folder='sorting_KS4/',
)

# With custom parameters
sorting = npa.run_sorting(
    rec_corrected,
    sorter='kilosort4',
    output_folder='sorting_KS4/',
    sorter_params={
        'batch_size': 30000,
        'nblocks': 5,  # For nonrigid drift
        'Th_learned': 8,  # Detection threshold
    },
)
```

### Alternative Sorters

```python
# SpykingCircus2 (CPU-based)
sorting = npa.run_sorting(rec_corrected, sorter='spykingcircus2')

# Mountainsort5 (fast, good for short recordings)
sorting = npa.run_sorting(rec_corrected, sorter='mountainsort5')
```

### Compare Multiple Sorters

```python
# Run multiple sorters
sortings = {}
for sorter in ['kilosort4', 'spykingcircus2']:
    sortings[sorter] = npa.run_sorting(rec_corrected, sorter=sorter)

# Compare results
comparison = npa.compare_sorters(list(sortings.values()))
agreement_matrix = comparison.get_agreement_matrix()
```

## 5. Postprocessing

### Create Analyzer

```python
# Create sorting analyzer (central object for all postprocessing)
analyzer = npa.create_analyzer(
    sorting,
    rec_corrected,
    output_folder='analyzer/',
)

# Compute all standard extensions
analyzer = npa.postprocess(
    sorting,
    rec_corrected,
    output_folder='analyzer/',
    compute_all=True,  # Waveforms, templates, metrics, etc.
)
```

### Compute Individual Extensions

```python
# Waveforms
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0, max_spikes_per_unit=500)

# Templates
analyzer.compute('templates', operators=['average', 'std'])

# Spike amplitudes
analyzer.compute('spike_amplitudes')

# Correlograms
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)

# Unit locations
analyzer.compute('unit_locations', method='monopolar_triangulation')

# Spike locations
analyzer.compute('spike_locations', method='center_of_mass')
```

## 6. Quality Metrics

### Compute All Metrics

```python
# Compute comprehensive metrics
metrics = npa.compute_quality_metrics(
    analyzer,
    metric_names=[
        'snr',
        'isi_violations_ratio',
        'presence_ratio',
        'amplitude_cutoff',
        'firing_rate',
        'amplitude_cv',
        'sliding_rp_violation',
        'd_prime',
        'nearest_neighbor',
    ],
)

# View metrics
print(metrics.head())
```

### Key Metrics Explained

| Metric | Good Value | Description |
|--------|------------|-------------|
| `snr` | > 5 | Signal-to-noise ratio |
| `isi_violations_ratio` | < 0.01 | Refractory period violations |
| `presence_ratio` | > 0.9 | Fraction of recording with spikes |
| `amplitude_cutoff` | < 0.1 | Estimated missed spikes |
| `firing_rate` | > 0.1 Hz | Average firing rate |

## 7. Curation

### Automated Curation

```python
# Allen Institute criteria
labels = npa.curate(metrics, method='allen')

# IBL criteria
labels = npa.curate(metrics, method='ibl')

# Custom thresholds
labels = npa.curate(
    metrics,
    snr_threshold=5,
    isi_violations_threshold=0.01,
    presence_threshold=0.9,
)
```

### AI-Assisted Curation

```python
from anthropic import Anthropic

# Setup API
client = Anthropic()

# Visual analysis for uncertain units
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

for unit_id in uncertain:
    result = npa.analyze_unit_visually(analyzer, unit_id, api_client=client)
    labels[unit_id] = result['classification']
```

### Interactive Curation Session

```python
# Create session
session = npa.CurationSession.create(analyzer, output_dir='curation/')

# Review units
while session.current_unit():
    unit = session.current_unit()
    report = npa.generate_unit_report(analyzer, unit.unit_id)

    # Your decision
    decision = input(f"Unit {unit.unit_id}: ")
    session.set_decision(unit.unit_id, decision)
    session.next_unit()

# Export
labels = session.get_final_labels()
```

## 8. Export Results

### Export to Phy

```python
from spikeinterface.exporters import export_to_phy

export_to_phy(
    analyzer,
    output_folder='phy_export/',
    copy_binary=True,
)
```

### Export to NWB

```python
from spikeinterface.exporters import export_to_nwb

export_to_nwb(
    analyzer,
    nwbfile_path='results.nwb',
    metadata={
        'session_description': 'Neuropixels recording',
        'experimenter': 'Lab Name',
    },
)
```

### Save Quality Summary

```python
# Save metrics CSV
metrics.to_csv('quality_metrics.csv')

# Save labels
import json
with open('curation_labels.json', 'w') as f:
    json.dump(labels, f, indent=2)

# Generate summary report
npa.plot_quality_metrics(analyzer, metrics, output='quality_summary.png')
```

## Full Pipeline Example

```python
import neuropixels_analysis as npa

# Load
recording = npa.load_recording('/data/experiment/', format='spikeglx')

# Preprocess
rec = npa.preprocess(recording)

# Motion correction
rec = npa.correct_motion(rec)

# Sort
sorting = npa.run_sorting(rec, sorter='kilosort4')

# Postprocess
analyzer, metrics = npa.postprocess(sorting, rec)

# Curate
labels = npa.curate(metrics, method='allen')

# Export good units
good_units = [uid for uid, label in labels.items() if label == 'good']
print(f"Good units: {len(good_units)}/{len(labels)}")
```

## Tips for Success

1. **Always visualize drift** before deciding on motion correction
2. **Save preprocessed data** to avoid recomputing
3. **Compare multiple sorters** for critical experiments
4. **Review uncertain units manually** - don't trust automated curation blindly
5. **Document your parameters** for reproducibility
6. **Use GPU** for Kilosort4 (10-50x faster than CPU alternatives)
