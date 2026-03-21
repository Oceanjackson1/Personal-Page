---
title: "NeuroKit2 神经信号"
description: "神经生理信号处理工具包，ECG、EEG 和 EMG 分析"
category: "development"
source: "community"
author: "Community"
tags: ["neurokit2"]
date: 2026-03-20
---

# NeuroKit2

## Overview

NeuroKit2 is a comprehensive Python toolkit for processing and analyzing physiological signals (biosignals). Use this skill to process cardiovascular, neural, autonomic, respiratory, and muscular signals for psychophysiology research, clinical applications, and human-computer interaction studies.

## When to Use This Skill

Apply this skill when working with:
- **Cardiac signals**: ECG, PPG, heart rate variability (HRV), pulse analysis
- **Brain signals**: EEG frequency bands, microstates, complexity, source localization
- **Autonomic signals**: Electrodermal activity (EDA/GSR), skin conductance responses (SCR)
- **Respiratory signals**: Breathing rate, respiratory variability (RRV), volume per time
- **Muscular signals**: EMG amplitude, muscle activation detection
- **Eye tracking**: EOG, blink detection and analysis
- **Multi-modal integration**: Processing multiple physiological signals simultaneously
- **Complexity analysis**: Entropy measures, fractal dimensions, nonlinear dynamics

## Core Capabilities

### 1. Cardiac Signal Processing (ECG/PPG)

Process electrocardiogram and photoplethysmography signals for cardiovascular analysis. See `references/ecg_cardiac.md` for detailed workflows.

**Primary workflows:**
- ECG processing pipeline: cleaning → R-peak detection → delineation → quality assessment
- HRV analysis across time, frequency, and nonlinear domains
- PPG pulse analysis and quality assessment
- ECG-derived respiration extraction

**Key functions:**
```python
import neurokit2 as nk

# Complete ECG processing pipeline
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Analyze ECG data (event-related or interval-related)
analysis = nk.ecg_analyze(signals, sampling_rate=1000)

# Comprehensive HRV analysis
hrv = nk.hrv(peaks, sampling_rate=1000)  # Time, frequency, nonlinear domains
```

### 2. Heart Rate Variability Analysis

Compute comprehensive HRV metrics from cardiac signals. See `references/hrv.md` for all indices and domain-specific analysis.

**Supported domains:**
- **Time domain**: SDNN, RMSSD, pNN50, SDSD, and derived metrics
- **Frequency domain**: ULF, VLF, LF, HF, VHF power and ratios
- **Nonlinear domain**: Poincaré plot (SD1/SD2), entropy measures, fractal dimensions
- **Specialized**: Respiratory sinus arrhythmia (RSA), recurrence quantification analysis (RQA)

**Key functions:**
```python
# All HRV indices at once
hrv_indices = nk.hrv(peaks, sampling_rate=1000)

# Domain-specific analysis
hrv_time = nk.hrv_time(peaks)
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000)
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
hrv_rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000)
```

### 3. Brain Signal Analysis (EEG)

Analyze electroencephalography signals for frequency power, complexity, and microstate patterns. See `references/eeg.md` for detailed workflows and MNE integration.

**Primary capabilities:**
- Frequency band power analysis (Delta, Theta, Alpha, Beta, Gamma)
- Channel quality assessment and re-referencing
- Source localization (sLORETA, MNE)
- Microstate segmentation and transition dynamics
- Global field power and dissimilarity measures

**Key functions:**
```python
# Power analysis across frequency bands
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'])

# Microstate analysis
microstates = nk.microstates_segment(eeg_data, n_microstates=4, method='kmod')
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)
```

### 4. Electrodermal Activity (EDA)

Process skin conductance signals for autonomic nervous system assessment. See `references/eda.md` for detailed workflows.

**Primary workflows:**
- Signal decomposition into tonic and phasic components
- Skin conductance response (SCR) detection and analysis
- Sympathetic nervous system index calculation
- Autocorrelation and changepoint detection

**Key functions:**
```python
# Complete EDA processing
signals, info = nk.eda_process(eda_signal, sampling_rate=100)

# Analyze EDA data
analysis = nk.eda_analyze(signals, sampling_rate=100)

# Sympathetic nervous system activity
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100)
```

### 5. Respiratory Signal Processing (RSP)

Analyze breathing patterns and respiratory variability. See `references/rsp.md` for detailed workflows.

**Primary capabilities:**
- Respiratory rate calculation and variability analysis
- Breathing amplitude and symmetry assessment
- Respiratory volume per time (fMRI applications)
- Respiratory amplitude variability (RAV)

**Key functions:**
```python
# Complete RSP processing
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100)

# Respiratory rate variability
rrv = nk.rsp_rrv(signals, sampling_rate=100)

# Respiratory volume per time
rvt = nk.rsp_rvt(signals, sampling_rate=100)
```

### 6. Electromyography (EMG)

Process muscle activity signals for activation detection and amplitude analysis. See `references/emg.md` for workflows.

**Key functions:**
```python
# Complete EMG processing
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)

# Muscle activation detection
activation = nk.emg_activation(signals, sampling_rate=1000, method='threshold')
```

### 7. Electrooculography (EOG)

Analyze eye movement and blink patterns. See `references/eog.md` for workflows.

**Key functions:**
```python
# Complete EOG processing
signals, info = nk.eog_process(eog_signal, sampling_rate=500)

# Extract blink features
features = nk.eog_features(signals, sampling_rate=500)
```

### 8. General Signal Processing

Apply filtering, decomposition, and transformation operations to any signal. See `references/signal_processing.md` for comprehensive utilities.

**Key operations:**
- Filtering (lowpass, highpass, bandpass, bandstop)
- Decomposition (EMD, SSA, wavelet)
- Peak detection and correction
- Power spectral density estimation
- Signal interpolation and resampling
- Autocorrelation and synchrony analysis

**Key functions:**
```python
# Filtering
filtered = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=40)

# Peak detection
peaks = nk.signal_findpeaks(signal)

# Power spectral density
psd = nk.signal_psd(signal, sampling_rate=1000)
```

### 9. Complexity and Entropy Analysis

Compute nonlinear dynamics, fractal dimensions, and information-theoretic measures. See `references/complexity.md` for all available metrics.

**Available measures:**
- **Entropy**: Shannon, approximate, sample, permutation, spectral, fuzzy, multiscale
- **Fractal dimensions**: Katz, Higuchi, Petrosian, Sevcik, correlation dimension
- **Nonlinear dynamics**: Lyapunov exponents, Lempel-Ziv complexity, recurrence quantification
- **DFA**: Detrended fluctuation analysis, multifractal DFA
- **Information theory**: Fisher information, mutual information

**Key functions:**
```python
# Multiple complexity metrics at once
complexity_indices = nk.complexity(signal, sampling_rate=1000)

# Specific measures
apen = nk.entropy_approximate(signal)
dfa = nk.fractal_dfa(signal)
lyap = nk.complexity_lyapunov(signal, sampling_rate=1000)
```

### 10. Event-Related Analysis

Create epochs around stimulus events and analyze physiological responses. See `references/epochs_events.md` for workflows.

**Primary capabilities:**
- Epoch creation from event markers
- Event-related averaging and visualization
- Baseline correction options
- Grand average computation with confidence intervals

**Key functions:**
```python
# Find events in signal
events = nk.events_find(trigger_signal, threshold=0.5)

# Create epochs around events
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Average across epochs
grand_average = nk.epochs_average(epochs)
```

### 11. Multi-Signal Integration

Process multiple physiological signals simultaneously with unified output. See `references/bio_module.md` for integration workflows.

**Key functions:**
```python
# Process multiple signals at once
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    emg=emg_signal,
    sampling_rate=1000
)

# Analyze all processed signals
bio_analysis = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

## Analysis Modes

NeuroKit2 automatically selects between two analysis modes based on data duration:

**Event-related analysis** (< 10 seconds):
- Analyzes stimulus-locked responses
- Epoch-based segmentation
- Suitable for experimental paradigms with discrete trials

**Interval-related analysis** (≥ 10 seconds):
- Characterizes physiological patterns over extended periods
- Resting state or continuous activities
- Suitable for baseline measurements and long-term monitoring

Most `*_analyze()` functions automatically choose the appropriate mode.

## Installation

```bash
uv pip install neurokit2
```

For development version:
```bash
uv pip install https://github.com/neuropsychology/NeuroKit/zipball/dev
```

## Common Workflows

### Quick Start: ECG Analysis
```python
import neurokit2 as nk

# Load example data
ecg = nk.ecg_simulate(duration=60, sampling_rate=1000)

# Process ECG
signals, info = nk.ecg_process(ecg, sampling_rate=1000)

# Analyze HRV
hrv = nk.hrv(info['ECG_R_Peaks'], sampling_rate=1000)

# Visualize
nk.ecg_plot(signals, info)
```

### Multi-Modal Analysis
```python
# Process multiple signals
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)

# Analyze all signals
results = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

### Event-Related Potential
```python
# Find events
events = nk.events_find(trigger_channel, threshold=0.5)

# Create epochs
epochs = nk.epochs_create(processed_signals, events,
                          sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Event-related analysis for each signal type
ecg_epochs = nk.ecg_eventrelated(epochs)
eda_epochs = nk.eda_eventrelated(epochs)
```

## References

This skill includes comprehensive reference documentation organized by signal type and analysis method:

- **ecg_cardiac.md**: ECG/PPG processing, R-peak detection, delineation, quality assessment
- **hrv.md**: Heart rate variability indices across all domains
- **eeg.md**: EEG analysis, frequency bands, microstates, source localization
- **eda.md**: Electrodermal activity processing and SCR analysis
- **rsp.md**: Respiratory signal processing and variability
- **ppg.md**: Photoplethysmography signal analysis
- **emg.md**: Electromyography processing and activation detection
- **eog.md**: Electrooculography and blink analysis
- **signal_processing.md**: General signal utilities and transformations
- **complexity.md**: Entropy, fractal, and nonlinear measures
- **epochs_events.md**: Event-related analysis and epoch creation
- **bio_module.md**: Multi-signal integration workflows

Load specific reference files as needed using the Read tool to access detailed function documentation and parameters.

## Additional Resources

- Official Documentation: https://neuropsychology.github.io/NeuroKit/
- GitHub Repository: https://github.com/neuropsychology/NeuroKit
- Publication: Makowski et al. (2021). NeuroKit2: A Python toolbox for neurophysiological signal processing. Behavior Research Methods. https://doi.org/10.3758/s13428-020-01516-y

---

## Reference: Bio_Module

# Multi-Signal Integration (Bio Module)

## Overview

The Bio module provides unified functions for processing and analyzing multiple physiological signals simultaneously. It acts as a wrapper that coordinates signal-specific processing functions and enables integrated multi-modal analysis.

## Multi-Signal Processing

### bio_process()

Process multiple physiological signals simultaneously with a single function call.

```python
bio_signals, bio_info = nk.bio_process(ecg=None, rsp=None, eda=None, emg=None,
                                       ppg=None, eog=None, sampling_rate=1000)
```

**Parameters:**
- `ecg`: ECG signal array (optional)
- `rsp`: Respiratory signal array (optional)
- `eda`: EDA signal array (optional)
- `emg`: EMG signal array (optional)
- `ppg`: PPG signal array (optional)
- `eog`: EOG signal array (optional)
- `sampling_rate`: Sampling rate in Hz (must be consistent across signals or specify per signal)

**Returns:**
- `bio_signals`: Unified DataFrame containing all processed signals with columns:
  - Signal-specific features (e.g., `ECG_Clean`, `ECG_Rate`, `EDA_Phasic`, `RSP_Rate`)
  - All detected events/peaks
  - Derived measures
- `bio_info`: Dictionary with signal-specific information (peak locations, parameters)

**Example:**
```python
# Process ECG, respiration, and EDA simultaneously
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)

# Access processed signals
ecg_clean = bio_signals['ECG_Clean']
rsp_rate = bio_signals['RSP_Rate']
eda_phasic = bio_signals['EDA_Phasic']

# Access detected peaks
ecg_peaks = bio_info['ECG']['ECG_R_Peaks']
rsp_peaks = bio_info['RSP']['RSP_Peaks']
```

**Internal workflow:**
1. Each signal is processed by its dedicated processing function:
   - `ecg_process()` for ECG
   - `rsp_process()` for respiration
   - `eda_process()` for EDA
   - `emg_process()` for EMG
   - `ppg_process()` for PPG
   - `eog_process()` for EOG
2. Results are merged into unified DataFrame
3. Cross-signal features computed (e.g., RSA if both ECG and RSP present)

**Advantages:**
- Simplified API for multi-modal recording
- Unified time base for all signals
- Automatic cross-signal feature computation
- Consistent output format

## Multi-Signal Analysis

### bio_analyze()

Perform comprehensive analysis on processed multi-modal signals.

```python
bio_results = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

**Parameters:**
- `bio_signals`: DataFrame from `bio_process()` or custom processed signals
- `sampling_rate`: Sampling rate (Hz)

**Returns:**
- DataFrame with analysis results for all detected signal types:
  - Interval-related metrics if duration ≥ 10 seconds
  - Event-related metrics if duration < 10 seconds
  - Cross-signal indices (e.g., RSA if ECG + RSP available)

**Computed metrics by signal:**
- **ECG**: Heart rate statistics, HRV indices (time, frequency, nonlinear domains)
- **RSP**: Respiratory rate statistics, RRV, amplitude measures
- **EDA**: SCR count, amplitude, tonic level, sympathetic indices
- **EMG**: Activation count, amplitude statistics
- **PPG**: Similar to ECG (heart rate, HRV)
- **EOG**: Blink count, blink rate

**Cross-signal metrics:**
- **RSA (Respiratory Sinus Arrhythmia)**: If ECG + RSP present
- **Cardiorespiratory coupling**: Phase synchronization indices
- **Multi-modal arousal**: Combined autonomic indices

**Example:**
```python
# Analyze processed signals
results = nk.bio_analyze(bio_signals, sampling_rate=1000)

# Access results
heart_rate_mean = results['ECG_Rate_Mean']
hrv_rmssd = results['HRV_RMSSD']
breathing_rate = results['RSP_Rate_Mean']
scr_count = results['SCR_Peaks_N']
rsa_value = results['RSA']  # If both ECG and RSP present
```

## Cross-Signal Features

When multiple signals are processed together, NeuroKit2 can compute integrated features:

### Respiratory Sinus Arrhythmia (RSA)

Automatically computed when both ECG and respiratory signals are present.

```python
bio_signals, bio_info = nk.bio_process(ecg=ecg, rsp=rsp, sampling_rate=1000)
results = nk.bio_analyze(bio_signals, sampling_rate=1000)

rsa = results['RSA']  # Automatically included
```

**Computation:**
- High-frequency HRV modulation by breathing
- Requires synchronized ECG R-peaks and respiratory signal
- Methods: Porges-Bohrer or peak-to-trough

**Interpretation:**
- Higher RSA: greater parasympathetic (vagal) influence
- Marker of cardiac-respiratory coupling
- Health indicator and emotion regulation capacity

### ECG-Derived Respiration (EDR)

If respiratory signal unavailable, NeuroKit2 can estimate from ECG:

```python
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)

# Extract EDR
edr = nk.ecg_rsp(ecg_signals['ECG_Clean'], sampling_rate=1000)
```

**Use case:**
- Estimate respiration when direct measurement unavailable
- Cross-validate respiratory measurements

### Cardio-EDA Integration

Synchronized cardiac and electrodermal activity:

```python
bio_signals, bio_info = nk.bio_process(ecg=ecg, eda=eda, sampling_rate=1000)

# Both signals available for integrated analysis
ecg_rate = bio_signals['ECG_Rate']
eda_phasic = bio_signals['EDA_Phasic']

# Compute correlations or coupling metrics
correlation = ecg_rate.corr(eda_phasic)
```

## Practical Workflows

### Complete Multi-Modal Recording Analysis

```python
import neurokit2 as nk
import pandas as pd

# 1. Load multi-modal physiological data
ecg = load_ecg()        # Your data loading function
rsp = load_rsp()
eda = load_eda()
emg = load_emg()

# 2. Process all signals simultaneously
bio_signals, bio_info = nk.bio_process(
    ecg=ecg,
    rsp=rsp,
    eda=eda,
    emg=emg,
    sampling_rate=1000
)

# 3. Visualize processed signals
import matplotlib.pyplot as plt

fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)

# ECG
axes[0].plot(bio_signals.index / 1000, bio_signals['ECG_Clean'])
axes[0].set_ylabel('ECG')
axes[0].set_title('Multi-Modal Physiological Recording')

# Respiration
axes[1].plot(bio_signals.index / 1000, bio_signals['RSP_Clean'])
axes[1].set_ylabel('Respiration')

# EDA
axes[2].plot(bio_signals.index / 1000, bio_signals['EDA_Phasic'])
axes[2].set_ylabel('EDA (Phasic)')

# EMG
axes[3].plot(bio_signals.index / 1000, bio_signals['EMG_Amplitude'])
axes[3].set_ylabel('EMG Amplitude')
axes[3].set_xlabel('Time (s)')

plt.tight_layout()
plt.show()

# 4. Analyze all signals
results = nk.bio_analyze(bio_signals, sampling_rate=1000)

# 5. Extract key metrics
print("Heart Rate (mean):", results['ECG_Rate_Mean'])
print("HRV (RMSSD):", results['HRV_RMSSD'])
print("Breathing Rate:", results['RSP_Rate_Mean'])
print("SCRs (count):", results['SCR_Peaks_N'])
print("RSA:", results['RSA'])
```

### Event-Related Multi-Modal Analysis

```python
# 1. Process signals
bio_signals, bio_info = nk.bio_process(ecg=ecg, rsp=rsp, eda=eda, sampling_rate=1000)

# 2. Detect events
events = nk.events_find(trigger_channel, threshold=0.5)

# 3. Create epochs for all signals
epochs = nk.epochs_create(bio_signals, events, sampling_rate=1000,
                          epochs_start=-1.0, epochs_end=10.0,
                          event_labels=event_labels,
                          event_conditions=event_conditions)

# 4. Signal-specific event-related analysis
ecg_eventrelated = nk.ecg_eventrelated(epochs)
rsp_eventrelated = nk.rsp_eventrelated(epochs)
eda_eventrelated = nk.eda_eventrelated(epochs)

# 5. Merge results
all_results = pd.merge(ecg_eventrelated, rsp_eventrelated,
                       left_index=True, right_index=True)
all_results = pd.merge(all_results, eda_eventrelated,
                       left_index=True, right_index=True)

# 6. Statistical comparison by condition
all_results['Condition'] = event_conditions
condition_means = all_results.groupby('Condition').mean()
```

### Different Sampling Rates

Handle signals with different native sampling rates:

```python
# ECG at 1000 Hz, EDA at 100 Hz
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_1000hz,
    eda=eda_100hz,
    sampling_rate=1000  # Target sampling rate
)
# EDA will be automatically resampled to 1000 Hz internally
```

Or process separately and merge:

```python
# Process at native sampling rates
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
eda_signals, eda_info = nk.eda_process(eda, sampling_rate=100)

# Resample to common rate
eda_resampled = nk.signal_resample(eda_signals, sampling_rate=100,
                                   desired_sampling_rate=1000)

# Merge manually
bio_signals = pd.concat([ecg_signals, eda_resampled], axis=1)
```

## Use Cases and Applications

### Comprehensive Psychophysiology Research

Capture multiple dimensions of physiological arousal:

- **Cardiac**: Orienting, attention, emotional valence
- **Respiratory**: Arousal, stress, emotion regulation
- **EDA**: Sympathetic arousal, emotional intensity
- **EMG**: Muscle tension, facial expression, startle

**Example: Emotional picture viewing**
- ECG: Heart rate deceleration during picture viewing (attention)
- EDA: SCRs reflect emotional arousal intensity
- RSP: Breath-holding or changes reflect emotional engagement
- Facial EMG: Corrugator (frown), zygomaticus (smile) for valence

### Stress and Relaxation Assessment

Multi-modal markers provide convergent evidence:

- **Increased stress**: ↑ HR, ↓ HRV, ↑ EDA, ↑ respiration rate, ↑ muscle tension
- **Relaxation**: ↓ HR, ↑ HRV, ↓ EDA, ↓ respiration rate, slow breathing, ↓ muscle tension

**Intervention effectiveness:**
- Compare multi-modal indices before vs. after intervention
- Identify which modalities respond to specific techniques

### Clinical Assessment

**Anxiety disorders:**
- Heightened baseline EDA, HR
- Exaggerated responses to stressors
- Reduced HRV, respiratory variability

**Depression:**
- Altered autonomic balance (↓ HRV)
- Blunted EDA responses
- Irregular respiratory patterns

**PTSD:**
- Hyperarousal (↑ HR, ↑ EDA baseline)
- Exaggerated startle (EMG)
- Altered RSA

### Human-Computer Interaction

Unobtrusive user state assessment:

- **Cognitive load**: ↓ HRV, ↑ EDA, suppressed blinks
- **Frustration**: ↑ HR, ↑ EDA, ↑ muscle tension
- **Engagement**: Moderate arousal, synchronized responses
- **Boredom**: Low arousal, irregular patterns

### Athletic Performance and Recovery

Monitor training load and recovery:

- **Resting HRV**: Daily monitoring for overtraining
- **EDA**: Sympathetic activation and stress
- **Respiration**: Breathing patterns during exercise/recovery
- **Multi-modal integration**: Comprehensive recovery assessment

## Advantages of Multi-Modal Recording

**Convergent validity:**
- Multiple indices converge on same construct (e.g., arousal)
- More robust than single measure

**Discriminant validity:**
- Different signals dissociate under certain conditions
- ECG reflects both sympathetic and parasympathetic
- EDA reflects primarily sympathetic

**System integration:**
- Understand whole-body physiological coordination
- Cross-signal coupling metrics (RSA, coherence)

**Redundancy and robustness:**
- If one signal quality poor, others available
- Cross-validate findings across modalities

**Richer interpretation:**
- HR deceleration + SCR increase = orienting with arousal
- HR acceleration + no SCR = cardiac response without sympathetic arousal

## Considerations

### Hardware and Synchronization

- **Same device**: Signals inherently synchronized
- **Different devices**: Requires common trigger/timestamp
  - Use hardware trigger to mark simultaneous events
  - Software alignment based on event markers
  - Verify synchronization quality (cross-correlate redundant signals)

### Signal Quality Across Modalities

- Not all signals may have equal quality
- Prioritize based on research question
- Document quality issues per signal

### Computational Cost

- Processing multiple signals increases computation time
- Consider processing in batches for large datasets
- Downsample appropriately to reduce load

### Analysis Complexity

- More signals = more variables = more statistical comparisons
- Risk of Type I error (false positives) without correction
- Use multivariate approaches or pre-registered analyses

### Interpretation

- Avoid over-interpretation of complex multi-modal patterns
- Ground in physiological theory
- Replicate findings before strong claims

## References

- Berntson, G. G., Cacioppo, J. T., & Quigley, K. S. (1993). Respiratory sinus arrhythmia: autonomic origins, physiological mechanisms, and psychophysiological implications. Psychophysiology, 30(2), 183-196.
- Cacioppo, J. T., Tassinary, L. G., & Berntson, G. (Eds.). (2017). Handbook of psychophysiology (4th ed.). Cambridge University Press.
- Kreibig, S. D. (2010). Autonomic nervous system activity in emotion: A review. Biological psychology, 84(3), 394-421.
- Laborde, S., Mosley, E., & Thayer, J. F. (2017). Heart rate variability and cardiac vagal tone in psychophysiological research–recommendations for experiment planning, data analysis, and data reporting. Frontiers in psychology, 8, 213.

---

## Reference: Complexity

# Complexity and Entropy Analysis

## Overview

Complexity measures quantify the irregularity, unpredictability, and multiscale structure of time series signals. NeuroKit2 provides comprehensive entropy, fractal dimension, and nonlinear dynamics measures for assessing physiological signal complexity.

## Main Function

### complexity()

Compute multiple complexity metrics simultaneously for exploratory analysis.

```python
complexity_indices = nk.complexity(signal, sampling_rate=1000, show=False)
```

**Returns:**
- DataFrame with numerous complexity measures across categories:
  - Entropy indices
  - Fractal dimensions
  - Nonlinear dynamics measures
  - Information-theoretic metrics

**Use case:**
- Exploratory analysis to identify relevant measures
- Comprehensive signal characterization
- Comparative studies across signals

## Parameter Optimization

Before computing complexity measures, optimal embedding parameters should be determined:

### complexity_delay()

Determine optimal time delay (τ) for phase space reconstruction.

```python
optimal_tau = nk.complexity_delay(signal, delay_max=100, method='fraser1986', show=False)
```

**Methods:**
- `'fraser1986'`: Mutual information first minimum
- `'theiler1990'`: Autocorrelation first zero crossing
- `'casdagli1991'`: Cao's method

**Use for:** Embedding delay in entropy, attractor reconstruction

### complexity_dimension()

Determine optimal embedding dimension (m).

```python
optimal_m = nk.complexity_dimension(signal, delay=None, dimension_max=20,
                                    method='afn', show=False)
```

**Methods:**
- `'afn'`: Average False Nearest Neighbors
- `'fnn'`: False Nearest Neighbors
- `'correlation'`: Correlation dimension saturation

**Use for:** Entropy calculations, phase space reconstruction

### complexity_tolerance()

Determine optimal tolerance (r) for entropy measures.

```python
optimal_r = nk.complexity_tolerance(signal, method='sd', show=False)
```

**Methods:**
- `'sd'`: Standard deviation-based (0.1-0.25 × SD typical)
- `'maxApEn'`: Maximize ApEn
- `'recurrence'`: Based on recurrence rate

**Use for:** Approximate entropy, sample entropy

### complexity_k()

Determine optimal k parameter for Higuchi fractal dimension.

```python
optimal_k = nk.complexity_k(signal, k_max=20, show=False)
```

**Use for:** Higuchi fractal dimension calculation

## Entropy Measures

Entropy quantifies randomness, unpredictability, and information content.

### entropy_shannon()

Shannon entropy - classical information-theoretic measure.

```python
shannon_entropy = nk.entropy_shannon(signal)
```

**Interpretation:**
- Higher: more random, less predictable
- Lower: more regular, predictable
- Units: bits (information)

**Use cases:**
- General randomness assessment
- Information content
- Signal irregularity

### entropy_approximate()

Approximate Entropy (ApEn) - regularity of patterns.

```python
apen = nk.entropy_approximate(signal, delay=1, dimension=2, tolerance='sd')
```

**Parameters:**
- `delay`: Time delay (τ)
- `dimension`: Embedding dimension (m)
- `tolerance`: Similarity threshold (r)

**Interpretation:**
- Lower ApEn: more regular, self-similar patterns
- Higher ApEn: more complex, irregular
- Sensitive to signal length (≥100-300 points recommended)

**Physiological applications:**
- HRV: reduced ApEn in heart disease
- EEG: altered ApEn in neurological disorders

### entropy_sample()

Sample Entropy (SampEn) - improved ApEn.

```python
sampen = nk.entropy_sample(signal, delay=1, dimension=2, tolerance='sd')
```

**Advantages over ApEn:**
- Less dependent on signal length
- More consistent across recordings
- No self-matching bias

**Interpretation:**
- Same as ApEn but more reliable
- Preferred in most applications

**Typical values:**
- HRV: 0.5-2.5 (context-dependent)
- EEG: 0.3-1.5

### entropy_multiscale()

Multiscale Entropy (MSE) - complexity across temporal scales.

```python
mse = nk.entropy_multiscale(signal, scale=20, dimension=2, tolerance='sd',
                            method='MSEn', show=False)
```

**Methods:**
- `'MSEn'`: Multiscale Sample Entropy
- `'MSApEn'`: Multiscale Approximate Entropy
- `'CMSE'`: Composite Multiscale Entropy
- `'RCMSE'`: Refined Composite Multiscale Entropy

**Interpretation:**
- Entropy at different coarse-graining scales
- Healthy/complex systems: high entropy across multiple scales
- Diseased/simpler systems: reduced entropy, especially at larger scales

**Use cases:**
- Distinguish true complexity from randomness
- White noise: constant across scales
- Pink noise/complexity: structured variation across scales

### entropy_fuzzy()

Fuzzy Entropy - uses fuzzy membership functions.

```python
fuzzen = nk.entropy_fuzzy(signal, delay=1, dimension=2, tolerance='sd', r=0.2)
```

**Advantages:**
- More stable with noisy signals
- Fuzzy boundaries for pattern matching
- Better performance with short signals

### entropy_permutation()

Permutation Entropy - based on ordinal patterns.

```python
perment = nk.entropy_permutation(signal, delay=1, dimension=3)
```

**Method:**
- Encodes signal into ordinal patterns (permutations)
- Counts pattern frequencies
- Robust to noise and non-stationarity

**Interpretation:**
- Lower: more regular ordinal structure
- Higher: more random ordering

**Use cases:**
- EEG analysis
- Anesthesia depth monitoring
- Fast computation

### entropy_spectral()

Spectral Entropy - based on power spectrum.

```python
spec_ent = nk.entropy_spectral(signal, sampling_rate=1000, bands=None)
```

**Method:**
- Normalized Shannon entropy of power spectrum
- Quantifies frequency distribution regularity

**Interpretation:**
- 0: Single frequency (pure tone)
- 1: White noise (flat spectrum)

**Use cases:**
- EEG: spectral distribution changes with states
- Anesthesia monitoring

### entropy_svd()

Singular Value Decomposition Entropy.

```python
svd_ent = nk.entropy_svd(signal, delay=1, dimension=2)
```

**Method:**
- SVD on trajectory matrix
- Entropy of singular value distribution

**Use cases:**
- Attractor complexity
- Deterministic vs. stochastic dynamics

### entropy_differential()

Differential Entropy - continuous analog of Shannon entropy.

```python
diff_ent = nk.entropy_differential(signal)
```

**Use for:** Continuous probability distributions

### Other Entropy Measures

**Tsallis Entropy:**
```python
tsallis = nk.entropy_tsallis(signal, q=2)
```
- Generalized entropy with parameter q
- q=1 reduces to Shannon entropy

**Rényi Entropy:**
```python
renyi = nk.entropy_renyi(signal, alpha=2)
```
- Generalized entropy with parameter α

**Additional specialized entropies:**
- `entropy_attention()`: Attention entropy
- `entropy_grid()`: Grid-based entropy
- `entropy_increment()`: Increment entropy
- `entropy_slope()`: Slope entropy
- `entropy_dispersion()`: Dispersion entropy
- `entropy_symbolicdynamic()`: Symbolic dynamics entropy
- `entropy_range()`: Range entropy
- `entropy_phase()`: Phase entropy
- `entropy_quadratic()`, `entropy_cumulative_residual()`, `entropy_rate()`: Specialized variants

## Fractal Dimension Measures

Fractal dimensions characterize self-similarity and roughness.

### fractal_katz()

Katz Fractal Dimension - waveform complexity.

```python
kfd = nk.fractal_katz(signal)
```

**Interpretation:**
- 1: straight line
- >1: increasing roughness and complexity
- Typical range: 1.0-2.0

**Advantages:**
- Simple, fast computation
- No parameter tuning

### fractal_higuchi()

Higuchi Fractal Dimension - self-similarity.

```python
hfd = nk.fractal_higuchi(signal, k_max=10)
```

**Method:**
- Constructs k new time series from original
- Estimates dimension from length-scale relationship

**Interpretation:**
- Higher HFD: more complex, irregular
- Lower HFD: smoother, more regular

**Use cases:**
- EEG complexity
- HRV analysis
- Epilepsy detection

### fractal_petrosian()

Petrosian Fractal Dimension - rapid estimation.

```python
pfd = nk.fractal_petrosian(signal)
```

**Advantages:**
- Fast computation
- Direct calculation (no curve fitting)

### fractal_sevcik()

Sevcik Fractal Dimension - normalized waveform complexity.

```python
sfd = nk.fractal_sevcik(signal)
```

### fractal_nld()

Normalized Length Density - curve length-based measure.

```python
nld = nk.fractal_nld(signal)
```

### fractal_psdslope()

Power Spectral Density Slope - frequency-domain fractal measure.

```python
slope = nk.fractal_psdslope(signal, sampling_rate=1000)
```

**Method:**
- Linear fit to log-log power spectrum
- Slope β relates to fractal dimension

**Interpretation:**
- β ≈ 0: White noise (random)
- β ≈ -1: Pink noise (1/f, complex)
- β ≈ -2: Brown noise (Brownian motion)

### fractal_hurst()

Hurst Exponent - long-range dependence.

```python
hurst = nk.fractal_hurst(signal, show=False)
```

**Interpretation:**
- H < 0.5: Anti-persistent (mean-reverting)
- H = 0.5: Random walk (white noise)
- H > 0.5: Persistent (trending, long-memory)

**Use cases:**
- Assess long-term correlations
- Financial time series
- HRV analysis

### fractal_correlation()

Correlation Dimension - attractor dimensionality.

```python
corr_dim = nk.fractal_correlation(signal, delay=1, dimension=10, radius=64)
```

**Method:**
- Grassberger-Procaccia algorithm
- Estimates dimension of attractor in phase space

**Interpretation:**
- Low dimension: deterministic, low-dimensional chaos
- High dimension: high-dimensional chaos or noise

### fractal_dfa()

Detrended Fluctuation Analysis - scaling exponent.

```python
dfa_alpha = nk.fractal_dfa(signal, multifractal=False, q=2, show=False)
```

**Interpretation:**
- α < 0.5: Anti-correlated
- α = 0.5: Uncorrelated (white noise)
- α = 1.0: 1/f noise (pink noise, healthy complexity)
- α = 1.5: Brownian noise
- α > 1.0: Persistent long-range correlations

**HRV applications:**
- α1 (short-term, 4-11 beats): Reflects autonomic regulation
- α2 (long-term, >11 beats): Long-range correlations
- Reduced α1: Cardiac pathology

### fractal_mfdfa()

Multifractal DFA - multiscale fractal properties.

```python
mfdfa_results = nk.fractal_mfdfa(signal, q=None, show=False)
```

**Method:**
- Extends DFA to multiple q-orders
- Characterizes multifractal spectrum

**Returns:**
- Generalized Hurst exponents h(q)
- Multifractal spectrum f(α)
- Width indicates multifractality strength

**Use cases:**
- Detect multifractal structure
- HRV multifractality in health vs. disease
- EEG multiscale dynamics

### fractal_tmf()

Multifractal Nonlinearity - deviation from monofractal.

```python
tmf = nk.fractal_tmf(signal)
```

**Interpretation:**
- Quantifies departure from simple scaling
- Higher: more multifractal structure

### fractal_density()

Density Fractal Dimension.

```python
density_fd = nk.fractal_density(signal)
```

### fractal_linelength()

Line Length - total variation measure.

```python
linelength = nk.fractal_linelength(signal)
```

**Use case:**
- Simple complexity proxy
- EEG seizure detection

## Nonlinear Dynamics

### complexity_lyapunov()

Largest Lyapunov Exponent - chaos and divergence.

```python
lyap = nk.complexity_lyapunov(signal, delay=None, dimension=None,
                              sampling_rate=1000, show=False)
```

**Interpretation:**
- λ < 0: Stable fixed point
- λ = 0: Periodic orbit
- λ > 0: Chaotic (nearby trajectories diverge exponentially)

**Use cases:**
- Detect chaos in physiological signals
- HRV: positive Lyapunov suggests nonlinear dynamics
- EEG: epilepsy detection (decreased λ before seizure)

### complexity_lempelziv()

Lempel-Ziv Complexity - algorithmic complexity.

```python
lz = nk.complexity_lempelziv(signal, symbolize='median')
```

**Method:**
- Counts number of distinct patterns
- Coarse-grained measure of randomness

**Interpretation:**
- Lower: repetitive, predictable patterns
- Higher: diverse, unpredictable patterns

**Use cases:**
- EEG: consciousness levels, anesthesia
- HRV: autonomic complexity

### complexity_rqa()

Recurrence Quantification Analysis - phase space recurrences.

```python
rqa_indices = nk.complexity_rqa(signal, delay=1, dimension=3, tolerance='sd')
```

**Metrics:**
- **Recurrence Rate (RR)**: Percentage of recurrent states
- **Determinism (DET)**: Percentage of recurrent points in lines
- **Laminarity (LAM)**: Percentage in vertical structures (laminar states)
- **Trapping Time (TT)**: Average vertical line length
- **Longest diagonal/vertical**: System predictability
- **Entropy (ENTR)**: Shannon entropy of line length distribution

**Interpretation:**
- High DET: deterministic dynamics
- High LAM: system trapped in specific states
- Low RR: random, non-recurrent dynamics

**Use cases:**
- Detect transitions in system dynamics
- Physiological state changes
- Nonlinear time series analysis

### complexity_hjorth()

Hjorth Parameters - time-domain complexity.

```python
hjorth = nk.complexity_hjorth(signal)
```

**Metrics:**
- **Activity**: Variance of signal
- **Mobility**: Proportion of standard deviation of derivative to signal
- **Complexity**: Change in mobility with derivative

**Use cases:**
- EEG feature extraction
- Seizure detection
- Signal characterization

### complexity_decorrelation()

Decorrelation Time - memory duration.

```python
decorr_time = nk.complexity_decorrelation(signal, show=False)
```

**Interpretation:**
- Time lag where autocorrelation drops below threshold
- Shorter: rapid fluctuations, short memory
- Longer: slow fluctuations, long memory

### complexity_relativeroughness()

Relative Roughness - smoothness measure.

```python
roughness = nk.complexity_relativeroughness(signal)
```

## Information Theory

### fisher_information()

Fisher Information - measure of order.

```python
fisher = nk.fisher_information(signal, delay=1, dimension=2)
```

**Interpretation:**
- High: ordered, structured
- Low: disordered, random

**Use cases:**
- Combine with Shannon entropy (Fisher-Shannon plane)
- Characterize system complexity

### fishershannon_information()

Fisher-Shannon Information Product.

```python
fs = nk.fishershannon_information(signal)
```

**Method:**
- Product of Fisher information and Shannon entropy
- Characterizes order-disorder balance

### mutual_information()

Mutual Information - shared information between variables.

```python
mi = nk.mutual_information(signal1, signal2, method='knn')
```

**Methods:**
- `'knn'`: k-nearest neighbors (nonparametric)
- `'kernel'`: Kernel density estimation
- `'binning'`: Histogram-based

**Use cases:**
- Coupling between signals
- Feature selection
- Nonlinear dependence

## Practical Considerations

### Signal Length Requirements

| Measure | Minimum Length | Optimal Length |
|---------|---------------|----------------|
| Shannon entropy | 50 | 200+ |
| ApEn, SampEn | 100-300 | 500-1000 |
| Multiscale entropy | 500 | 1000+ per scale |
| DFA | 500 | 1000+ |
| Lyapunov | 1000 | 5000+ |
| Correlation dimension | 1000 | 5000+ |

### Parameter Selection

**General guidelines:**
- Use parameter optimization functions first
- Or use conventional defaults:
  - Delay (τ): 1 for HRV, autocorrelation first minimum for EEG
  - Dimension (m): 2-3 typical
  - Tolerance (r): 0.2 × SD common

**Sensitivity:**
- Results can be parameter-sensitive
- Report parameters used
- Consider sensitivity analysis

### Normalization and Preprocessing

**Standardization:**
- Many measures sensitive to signal amplitude
- Z-score normalization often recommended
- Detrending may be necessary

**Stationarity:**
- Some measures assume stationarity
- Check with statistical tests (e.g., ADF test)
- Segment non-stationary signals

### Interpretation

**Context-dependent:**
- No universal "good" or "bad" complexity
- Compare within-subject or between groups
- Consider physiological context

**Complexity vs. randomness:**
- Maximum entropy ≠ maximum complexity
- True complexity: structured variability
- White noise: high entropy but low complexity (MSE distinguishes)

## Applications

**Cardiovascular:**
- HRV complexity: reduced in heart disease, aging
- DFA α1: prognostic marker post-MI

**Neuroscience:**
- EEG complexity: consciousness, anesthesia depth
- Entropy: Alzheimer's, epilepsy, sleep stages
- Permutation entropy: anesthesia monitoring

**Psychology:**
- Complexity loss in depression, anxiety
- Increased regularity under stress

**Aging:**
- "Complexity loss" with aging across systems
- Reduced multiscale complexity

**Critical transitions:**
- Complexity changes before state transitions
- Early warning signals (critical slowing down)

## References

- Pincus, S. M. (1991). Approximate entropy as a measure of system complexity. Proceedings of the National Academy of Sciences, 88(6), 2297-2301.
- Richman, J. S., & Moorman, J. R. (2000). Physiological time-series analysis using approximate entropy and sample entropy. American Journal of Physiology-Heart and Circulatory Physiology, 278(6), H2039-H2049.
- Peng, C. K., et al. (1995). Quantification of scaling exponents and crossover phenomena in nonstationary heartbeat time series. Chaos, 5(1), 82-87.
- Costa, M., Goldberger, A. L., & Peng, C. K. (2005). Multiscale entropy analysis of biological signals. Physical review E, 71(2), 021906.
- Grassberger, P., & Procaccia, I. (1983). Measuring the strangeness of strange attractors. Physica D: Nonlinear Phenomena, 9(1-2), 189-208.

---

## Reference: Ecg_Cardiac

# ECG and Cardiac Signal Processing

## Overview

Process electrocardiogram (ECG) and photoplethysmography (PPG) signals for cardiovascular analysis. This module provides comprehensive tools for R-peak detection, waveform delineation, quality assessment, and heart rate analysis.

## Main Processing Pipeline

### ecg_process()

Complete automated ECG processing pipeline that orchestrates multiple steps.

```python
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000, method='neurokit')
```

**Pipeline steps:**
1. Signal cleaning (noise removal)
2. R-peak detection
3. Heart rate calculation
4. Quality assessment
5. QRS delineation (P, Q, S, T waves)
6. Cardiac phase determination

**Returns:**
- `signals`: DataFrame with cleaned ECG, peaks, rate, quality, cardiac phases
- `info`: Dictionary with R-peak locations and processing parameters

**Common methods:**
- `'neurokit'` (default): Comprehensive NeuroKit2 pipeline
- `'biosppy'`: BioSPPy-based processing
- `'pantompkins1985'`: Pan-Tompkins algorithm
- `'hamilton2002'`, `'elgendi2010'`, `'engzeemod2012'`: Alternative methods

## Preprocessing Functions

### ecg_clean()

Remove noise from raw ECG signals using method-specific filtering.

```python
cleaned_ecg = nk.ecg_clean(ecg_signal, sampling_rate=1000, method='neurokit')
```

**Methods:**
- `'neurokit'`: High-pass Butterworth filter (0.5 Hz) + powerline filtering
- `'biosppy'`: FIR filtering between 0.67-45 Hz
- `'pantompkins1985'`: Band-pass 5-15 Hz + derivative-based
- `'hamilton2002'`: Band-pass 8-16 Hz
- `'elgendi2010'`: Band-pass 8-20 Hz
- `'engzeemod2012'`: FIR band-pass 0.5-40 Hz

**Key parameters:**
- `powerline`: Remove 50 or 60 Hz powerline noise (default: 50)

### ecg_peaks()

Detect R-peaks in ECG signals with optional artifact correction.

```python
peaks_dict, info = nk.ecg_peaks(cleaned_ecg, sampling_rate=1000, method='neurokit', correct_artifacts=False)
```

**Available methods (13+ algorithms):**
- `'neurokit'`: Hybrid approach optimized for reliability
- `'pantompkins1985'`: Classic Pan-Tompkins algorithm
- `'hamilton2002'`: Hamilton's adaptive threshold
- `'christov2004'`: Christov's adaptive method
- `'gamboa2008'`: Gamboa's approach
- `'elgendi2010'`: Elgendi's two moving averages
- `'engzeemod2012'`: Modified Engelse-Zeelenberg
- `'kalidas2017'`: XQRS-based
- `'martinez2004'`, `'rodrigues2021'`, `'koka2022'`, `'promac'`: Advanced methods

**Artifact correction:**
Set `correct_artifacts=True` to apply Lipponen & Tarvainen (2019) correction:
- Detects ectopic beats, long/short intervals, missed beats
- Uses threshold-based detection with configurable parameters

**Returns:**
- Dictionary with `'ECG_R_Peaks'` key containing peak indices

### ecg_delineate()

Identify P, Q, S, T waves and their onsets/offsets.

```python
waves, waves_peak = nk.ecg_delineate(cleaned_ecg, rpeaks, sampling_rate=1000, method='dwt')
```

**Methods:**
- `'dwt'` (default): Discrete wavelet transform-based detection
- `'peak'`: Simple peak detection around R-peaks
- `'cwt'`: Continuous wavelet transform (Martinez et al., 2004)

**Detected components:**
- P waves: `ECG_P_Peaks`, `ECG_P_Onsets`, `ECG_P_Offsets`
- Q waves: `ECG_Q_Peaks`
- S waves: `ECG_S_Peaks`
- T waves: `ECG_T_Peaks`, `ECG_T_Onsets`, `ECG_T_Offsets`
- QRS complex: onsets and offsets

**Returns:**
- `waves`: Dictionary with all wave indices
- `waves_peak`: Dictionary with peak amplitudes

### ecg_quality()

Assess ECG signal integrity and quality.

```python
quality = nk.ecg_quality(ecg_signal, rpeaks=None, sampling_rate=1000, method='averageQRS')
```

**Methods:**
- `'averageQRS'` (default): Template matching correlation (Zhao & Zhang, 2018)
  - Returns quality scores 0-1 for each heartbeat
  - Threshold: >0.6 = good quality
- `'zhao2018'`: Multi-index approach using kurtosis, power spectrum distribution

**Use cases:**
- Identify low-quality signal segments
- Filter out noisy heartbeats before analysis
- Validate R-peak detection accuracy

## Analysis Functions

### ecg_analyze()

High-level analysis that automatically selects event-related or interval-related mode.

```python
analysis = nk.ecg_analyze(signals, sampling_rate=1000, method='auto')
```

**Mode selection:**
- Duration < 10 seconds → event-related analysis
- Duration ≥ 10 seconds → interval-related analysis

**Returns:**
DataFrame with cardiac metrics appropriate for the analysis mode.

### ecg_eventrelated()

Analyze stimulus-locked ECG epochs for event-related responses.

```python
results = nk.ecg_eventrelated(epochs)
```

**Computed metrics:**
- `ECG_Rate_Baseline`: Mean heart rate before stimulus
- `ECG_Rate_Min/Max`: Minimum/maximum heart rate during epoch
- `ECG_Phase_Atrial/Ventricular`: Cardiac phase at stimulus onset
- Rate dynamics across epoch time windows

**Use case:**
Experimental paradigms with discrete trials (e.g., stimulus presentations, task events).

### ecg_intervalrelated()

Analyze continuous ECG recordings for resting state or extended periods.

```python
results = nk.ecg_intervalrelated(signals, sampling_rate=1000)
```

**Computed metrics:**
- `ECG_Rate_Mean`: Average heart rate over interval
- Comprehensive HRV metrics (delegates to `hrv()` function)
  - Time domain: SDNN, RMSSD, pNN50, etc.
  - Frequency domain: LF, HF, LF/HF ratio
  - Nonlinear: Poincaré, entropy, fractal measures

**Minimum duration:**
- Basic rate: Any duration
- HRV frequency metrics: ≥60 seconds recommended, 1-5 minutes optimal

## Utility Functions

### ecg_rate()

Compute instantaneous heart rate from R-peak intervals.

```python
heart_rate = nk.ecg_rate(peaks, sampling_rate=1000, desired_length=None)
```

**Method:**
- Calculates inter-beat intervals (IBIs) between consecutive R-peaks
- Converts to beats per minute (BPM): 60 / IBI
- Interpolates to match signal length if `desired_length` specified

**Returns:**
- Array of instantaneous heart rate values

### ecg_phase()

Determine atrial and ventricular systole/diastole phases.

```python
cardiac_phase = nk.ecg_phase(ecg_cleaned, rpeaks, delineate_info)
```

**Phases computed:**
- `ECG_Phase_Atrial`: Atrial systole (1) vs. diastole (0)
- `ECG_Phase_Ventricular`: Ventricular systole (1) vs. diastole (0)
- `ECG_Phase_Completion_Atrial/Ventricular`: Percentage of phase completion (0-1)

**Use case:**
- Cardiac-locked stimulus presentation
- Psychophysiology experiments timing events to cardiac cycle

### ecg_segment()

Extract individual heartbeats for morphological analysis.

```python
heartbeats = nk.ecg_segment(ecg_cleaned, rpeaks, sampling_rate=1000)
```

**Returns:**
- Dictionary of epochs, each containing one heartbeat
- Centered on R-peak with configurable pre/post windows
- Useful for beat-to-beat morphology comparison

### ecg_invert()

Detect and correct inverted ECG signals automatically.

```python
corrected_ecg, is_inverted = nk.ecg_invert(ecg_signal, sampling_rate=1000)
```

**Method:**
- Analyzes QRS complex polarity
- Flips signal if predominantly negative
- Returns corrected signal and inversion status

### ecg_rsp()

Extract ECG-derived respiration (EDR) as respiratory proxy signal.

```python
edr_signal = nk.ecg_rsp(ecg_cleaned, sampling_rate=1000, method='vangent2019')
```

**Methods:**
- `'vangent2019'`: Bandpass filtering 0.1-0.4 Hz
- `'charlton2016'`: Bandpass 0.15-0.4 Hz
- `'soni2019'`: Bandpass 0.08-0.5 Hz

**Use case:**
- Estimate respiration when direct respiratory signal unavailable
- Multi-modal physiological analysis

## Simulation and Visualization

### ecg_simulate()

Generate synthetic ECG signals for testing and validation.

```python
synthetic_ecg = nk.ecg_simulate(duration=10, sampling_rate=1000, heart_rate=70, method='ecgsyn', noise=0.01)
```

**Methods:**
- `'ecgsyn'`: Realistic dynamical model (McSharry et al., 2003)
  - Simulates P-QRS-T complex morphology
  - Physiologically plausible waveforms
- `'simple'`: Faster wavelet-based approximation
  - Gaussian-like QRS complexes
  - Less realistic but computationally efficient

**Key parameters:**
- `heart_rate`: Average BPM (default: 70)
- `heart_rate_std`: Heart rate variability magnitude (default: 1)
- `noise`: Gaussian noise level (default: 0.01)
- `random_state`: Seed for reproducibility

### ecg_plot()

Visualize processed ECG with detected R-peaks and signal quality.

```python
nk.ecg_plot(signals, info)
```

**Displays:**
- Raw and cleaned ECG signals
- Detected R-peaks overlaid
- Heart rate trace
- Signal quality indicators

## ECG-Specific Considerations

### Sampling Rate Recommendations
- **Minimum**: 250 Hz for basic R-peak detection
- **Recommended**: 500-1000 Hz for waveform delineation
- **High-resolution**: 2000+ Hz for detailed morphology analysis

### Signal Duration Requirements
- **R-peak detection**: Any duration (≥2 beats minimum)
- **Basic heart rate**: ≥10 seconds
- **HRV time domain**: ≥60 seconds
- **HRV frequency domain**: 1-5 minutes (optimal)
- **Ultra-low frequency HRV**: ≥24 hours

### Common Issues and Solutions

**Poor R-peak detection:**
- Try different methods: `method='pantompkins1985'` often robust
- Ensure adequate sampling rate (≥250 Hz)
- Check for inverted ECG: use `ecg_invert()`
- Apply artifact correction: `correct_artifacts=True`

**Noisy signal:**
- Use appropriate cleaning method for noise type
- Adjust powerline frequency if outside US/Europe
- Consider signal quality assessment before analysis

**Missing waveform components:**
- Increase sampling rate (≥500 Hz for delineation)
- Try different delineation methods (`'dwt'`, `'peak'`, `'cwt'`)
- Verify signal quality with `ecg_quality()`

## Integration with Other Signals

### ECG + RSP: Respiratory Sinus Arrhythmia
```python
# Process both signals
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=1000)

# Compute RSA
rsa = nk.hrv_rsa(ecg_info['ECG_R_Peaks'], rsp_signals['RSP_Clean'], sampling_rate=1000)
```

### Multi-modal Integration
```python
# Process multiple signals at once
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)
```

## References

- Pan, J., & Tompkins, W. J. (1985). A real-time QRS detection algorithm. IEEE transactions on biomedical engineering, 32(3), 230-236.
- Hamilton, P. (2002). Open source ECG analysis. Computers in cardiology, 101-104.
- Martinez, J. P., Almeida, R., Olmos, S., Rocha, A. P., & Laguna, P. (2004). A wavelet-based ECG delineator: evaluation on standard databases. IEEE Transactions on biomedical engineering, 51(4), 570-581.
- Lipponen, J. A., & Tarvainen, M. P. (2019). A robust algorithm for heart rate variability time series artefact correction using novel beat classification. Journal of medical engineering & technology, 43(3), 173-181.

---

## Reference: Eda

# Electrodermal Activity (EDA) Analysis

## Overview

Electrodermal Activity (EDA), also known as Galvanic Skin Response (GSR) or Skin Conductance (SC), measures the electrical conductance of the skin, reflecting sympathetic nervous system arousal and sweat gland activity. EDA is widely used in psychophysiology, affective computing, and lie detection.

## Main Processing Pipeline

### eda_process()

Automated processing of raw EDA signals returning tonic/phasic decomposition and SCR features.

```python
signals, info = nk.eda_process(eda_signal, sampling_rate=100, method='neurokit')
```

**Pipeline steps:**
1. Signal cleaning (low-pass filtering)
2. Tonic-phasic decomposition
3. Skin conductance response (SCR) detection
4. SCR feature extraction (onset, peak, amplitude, rise/recovery times)

**Returns:**
- `signals`: DataFrame with:
  - `EDA_Clean`: Filtered signal
  - `EDA_Tonic`: Slow-varying baseline
  - `EDA_Phasic`: Fast-varying responses
  - `SCR_Onsets`, `SCR_Peaks`, `SCR_Height`: Response markers
  - `SCR_Amplitude`, `SCR_RiseTime`, `SCR_RecoveryTime`: Response features
- `info`: Dictionary with processing parameters

**Methods:**
- `'neurokit'`: cvxEDA decomposition + neurokit peak detection
- `'biosppy'`: Median smoothing + biosppy approach

## Preprocessing Functions

### eda_clean()

Remove noise through low-pass filtering.

```python
cleaned_eda = nk.eda_clean(eda_signal, sampling_rate=100, method='neurokit')
```

**Methods:**
- `'neurokit'`: Low-pass Butterworth filter (3 Hz cutoff)
- `'biosppy'`: Low-pass Butterworth filter (5 Hz cutoff)

**Automatic skipping:**
- If sampling rate < 7 Hz, cleaning is skipped (already low-pass)

**Rationale:**
- EDA frequency content typically 0-3 Hz
- Remove high-frequency noise and motion artifacts
- Preserve slow SCRs (typical rise time 1-3 seconds)

### eda_phasic()

Decompose EDA into tonic (slow baseline) and phasic (rapid responses) components.

```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='cvxeda')
```

**Methods:**

**1. cvxEDA (default, recommended):**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='cvxeda')
```
- Convex optimization approach (Greco et al., 2016)
- Sparse phasic driver model
- Most physiologically accurate
- Computationally intensive but superior decomposition

**2. Median smoothing:**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='smoothmedian')
```
- Median filter with configurable window
- Fast, simple
- Less accurate than cvxEDA

**3. High-pass filtering (Biopac's Acqknowledge):**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='highpass')
```
- High-pass filter (0.05 Hz) extracts phasic
- Fast computation
- Tonic derived by subtraction

**4. SparsEDA:**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='sparseda')
```
- Sparse deconvolution approach
- Alternative optimization method

**Returns:**
- `tonic`: Slow-varying skin conductance level (SCL)
- `phasic`: Fast skin conductance responses (SCRs)

**Physiological interpretation:**
- **Tonic (SCL)**: Baseline arousal, general activation, hydration
- **Phasic (SCR)**: Event-related responses, orienting, emotional reactions

### eda_peaks()

Detect Skin Conductance Responses (SCRs) in phasic component.

```python
peaks, info = nk.eda_peaks(eda_phasic, sampling_rate=100, method='neurokit',
                           amplitude_min=0.1)
```

**Methods:**
- `'neurokit'`: Optimized for reliability, configurable thresholds
- `'gamboa2008'`: Gamboa's algorithm
- `'kim2004'`: Kim's approach
- `'vanhalem2020'`: Van Halem's method
- `'nabian2018'`: Nabian's algorithm

**Key parameters:**
- `amplitude_min`: Minimum SCR amplitude (default: 0.1 µS)
  - Too low: false positives from noise
  - Too high: miss small but valid responses
- `rise_time_max`: Maximum rise time (default: 2 seconds)
- `rise_time_min`: Minimum rise time (default: 0.01 seconds)

**Returns:**
- Dictionary with:
  - `SCR_Onsets`: Indices where SCR begins
  - `SCR_Peaks`: Indices of peak amplitude
  - `SCR_Height`: Peak height above baseline
  - `SCR_Amplitude`: Onset-to-peak amplitude
  - `SCR_RiseTime`: Onset-to-peak duration
  - `SCR_RecoveryTime`: Peak-to-recovery duration (50% decay)

**SCR timing conventions:**
- **Latency**: 1-3 seconds after stimulus (typical)
- **Rise time**: 0.5-3 seconds
- **Recovery time**: 2-10 seconds (to 50% recovery)
- **Minimum amplitude**: 0.01-0.05 µS (detection threshold)

### eda_fixpeaks()

Correct detected SCR peaks (currently placeholder for EDA).

```python
corrected_peaks = nk.eda_fixpeaks(peaks)
```

**Note:** Less critical for EDA than cardiac signals due to slower dynamics.

## Analysis Functions

### eda_analyze()

Automatically select appropriate analysis type based on data duration.

```python
analysis = nk.eda_analyze(signals, sampling_rate=100)
```

**Mode selection:**
- Duration < 10 seconds → `eda_eventrelated()`
- Duration ≥ 10 seconds → `eda_intervalrelated()`

**Returns:**
- DataFrame with EDA metrics appropriate for analysis mode

### eda_eventrelated()

Analyze stimulus-locked EDA epochs for event-related responses.

```python
results = nk.eda_eventrelated(epochs)
```

**Computed metrics (per epoch):**
- `EDA_SCR`: Presence of SCR (binary: 0 or 1)
- `SCR_Amplitude`: Maximum SCR amplitude during epoch
- `SCR_Magnitude`: Mean phasic activity
- `SCR_Peak_Amplitude`: Onset-to-peak amplitude
- `SCR_RiseTime`: Time to peak from onset
- `SCR_RecoveryTime`: Time to 50% recovery
- `SCR_Latency`: Delay from stimulus to SCR onset
- `EDA_Tonic`: Mean tonic level during epoch

**Typical parameters:**
- Epoch duration: 0-10 seconds post-stimulus
- Baseline: -1 to 0 seconds pre-stimulus
- Expected SCR latency: 1-3 seconds

**Use cases:**
- Emotional stimulus processing (images, sounds)
- Cognitive load assessment (mental arithmetic)
- Anticipation and prediction error
- Orienting responses

### eda_intervalrelated()

Analyze extended EDA recordings for overall arousal and activation patterns.

```python
results = nk.eda_intervalrelated(signals, sampling_rate=100)
```

**Computed metrics:**
- `SCR_Peaks_N`: Number of SCRs detected
- `SCR_Peaks_Amplitude_Mean`: Average SCR amplitude
- `EDA_Tonic_Mean`, `EDA_Tonic_SD`: Tonic level statistics
- `EDA_Sympathetic`: Sympathetic nervous system index
- `EDA_SympatheticN`: Normalized sympathetic index
- `EDA_Autocorrelation`: Temporal structure (lag 4 seconds)
- `EDA_Phasic_*`: Mean, SD, min, max of phasic component

**Recording duration:**
- **Minimum**: 10 seconds
- **Recommended**: 60+ seconds for stable SCR rate
- **Sympathetic index**: ≥64 seconds required

**Use cases:**
- Resting state arousal assessment
- Stress level monitoring
- Baseline sympathetic activity
- Long-term affective state

## Specialized Analysis Functions

### eda_sympathetic()

Derive sympathetic nervous system activity from frequency band (0.045-0.25 Hz).

```python
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100, method='posada',
                                  show=False)
```

**Methods:**
- `'posada'`: Posada-Quintero method (2016)
  - Spectral power in 0.045-0.25 Hz band
  - Validated against other autonomic measures
- `'ghiasi'`: Ghiasi method (2018)
  - Alternative frequency-based approach

**Requirements:**
- **Minimum duration**: 64 seconds
- Sufficient for frequency resolution in target band

**Returns:**
- `EDA_Sympathetic`: Sympathetic index (absolute)
- `EDA_SympatheticN`: Normalized sympathetic index (0-1)

**Interpretation:**
- Higher values: increased sympathetic arousal
- Reflects tonic sympathetic activity, not phasic responses
- Complements SCR analysis

**Use cases:**
- Stress assessment
- Arousal monitoring over time
- Cognitive load measurement
- Complementary to HRV for autonomic balance

### eda_autocor()

Compute autocorrelation to assess temporal structure of EDA signal.

```python
autocorr = nk.eda_autocor(eda_phasic, sampling_rate=100, lag=4)
```

**Parameters:**
- `lag`: Time lag in seconds (default: 4 seconds)

**Interpretation:**
- High autocorrelation: persistent, slowly-varying signal
- Low autocorrelation: rapid, uncorrelated fluctuations
- Reflects temporal regularity of SCRs

**Use case:**
- Assess signal quality
- Characterize response patterns
- Distinguish sustained vs. transient arousal

### eda_changepoints()

Detect abrupt shifts in mean and variance of EDA signal.

```python
changepoints = nk.eda_changepoints(eda_phasic, penalty=10000, show=False)
```

**Method:**
- Penalty-based segmentation
- Identifies transitions between states

**Parameters:**
- `penalty`: Controls sensitivity (default: 10,000)
  - Higher penalty: fewer, more robust changepoints
  - Lower penalty: more sensitive to small changes

**Returns:**
- Indices of detected changepoints
- Optional visualization of segments

**Use cases:**
- Identify state transitions in continuous monitoring
- Segment data by arousal level
- Detect phase changes in experiments
- Automated epoch definition

## Visualization

### eda_plot()

Create static or interactive visualizations of processed EDA.

```python
nk.eda_plot(signals, info, static=True)
```

**Displays:**
- Raw and cleaned EDA signal
- Tonic and phasic components
- Detected SCR onsets, peaks, and recovery
- Sympathetic index time course (if computed)

**Interactive mode (`static=False`):**
- Plotly-based interactive exploration
- Zoom, pan, hover for details
- Export to image formats

## Simulation and Testing

### eda_simulate()

Generate synthetic EDA signals with configurable parameters.

```python
synthetic_eda = nk.eda_simulate(duration=10, sampling_rate=100, scr_number=3,
                                noise=0.01, drift=0.01)
```

**Parameters:**
- `duration`: Signal length in seconds
- `sampling_rate`: Sampling frequency (Hz)
- `scr_number`: Number of SCRs to include
- `noise`: Gaussian noise level
- `drift`: Slow baseline drift magnitude
- `random_state`: Seed for reproducibility

**Returns:**
- Synthetic EDA signal with realistic SCR morphology

**Use cases:**
- Algorithm testing and validation
- Educational demonstrations
- Method comparison

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 10 Hz (adequate for slow SCRs)
- **Standard**: 20-100 Hz (most commercial systems)
- **High-resolution**: 1000 Hz (research-grade, oversampled)

### Recording Duration
- **SCR detection**: ≥10 seconds (depends on stimulus)
- **Event-related**: Typically 10-20 seconds per trial
- **Interval-related**: ≥60 seconds for stable estimates
- **Sympathetic index**: ≥64 seconds (frequency resolution)

### Electrode Placement
- **Standard sites**:
  - Palmar: distal/middle phalanges (fingers)
  - Plantar: sole of foot
- **High density**: Thenar/hypothenar eminence
- **Avoid**: Hairy skin, low sweat gland density areas
- **Bilateral**: Left vs. right hand (typically similar)

### Signal Quality Issues

**Flat signal (no variation):**
- Check electrode contact and gel
- Verify proper placement on sweat gland-rich areas
- Allow 5-10 minute adaptation period

**Excessive noise:**
- Movement artifacts: minimize participant motion
- Electrical interference: check grounding, shielding
- Thermal effects: control room temperature

**Baseline drift:**
- Normal: slow changes over minutes
- Excessive: electrode polarization, poor contact
- Solution: use `eda_phasic()` to separate tonic drift

**Non-responders:**
- ~5-10% of population have minimal EDA
- Genetic/physiological variation
- Not indicative of equipment failure

### Best Practices

**Preprocessing workflow:**
```python
# 1. Clean signal
cleaned = nk.eda_clean(eda_raw, sampling_rate=100, method='neurokit')

# 2. Decompose tonic/phasic
tonic, phasic = nk.eda_phasic(cleaned, sampling_rate=100, method='cvxeda')

# 3. Detect SCRs
signals, info = nk.eda_peaks(phasic, sampling_rate=100, amplitude_min=0.05)

# 4. Analyze
analysis = nk.eda_analyze(signals, sampling_rate=100)
```

**Event-related workflow:**
```python
# 1. Process signal
signals, info = nk.eda_process(eda_raw, sampling_rate=100)

# 2. Find events
events = nk.events_find(trigger_channel, threshold=0.5)

# 3. Create epochs (-1 to 10 seconds around stimulus)
epochs = nk.epochs_create(signals, events, sampling_rate=100,
                          epochs_start=-1, epochs_end=10)

# 4. Event-related analysis
results = nk.eda_eventrelated(epochs)

# 5. Statistical analysis
# Compare SCR amplitude across conditions
```

## Clinical and Research Applications

**Emotion and affective science:**
- Arousal dimension of emotion (not valence)
- Emotional picture viewing
- Music-induced emotion
- Fear conditioning

**Cognitive processes:**
- Mental workload and effort
- Attention and vigilance
- Decision-making and uncertainty
- Error processing

**Clinical populations:**
- Anxiety disorders: heightened baseline, exaggerated responses
- PTSD: fear conditioning, extinction deficits
- Autism: atypical arousal patterns
- Psychopathy: reduced fear responses

**Applied settings:**
- Lie detection (polygraph)
- User experience research
- Driver monitoring
- Stress assessment in real-world settings

**Neuroimaging integration:**
- fMRI: EDA correlates with amygdala, insula activity
- Concurrent recording during brain imaging
- Autonomic-brain coupling

## Interpretation Guidelines

**SCR amplitude:**
- **0.01-0.05 µS**: Small but detectable
- **0.05-0.2 µS**: Moderate response
- **>0.2 µS**: Large response
- **Context-dependent**: Normalize within-subject

**SCR frequency:**
- **Resting**: 1-3 SCRs per minute (typical)
- **Stressed**: >5 SCRs per minute
- **Non-specific SCRs**: Spontaneous (no identifiable stimulus)

**Tonic SCL:**
- **Range**: 2-20 µS (highly variable across individuals)
- **Within-subject changes** more interpretable than absolute levels
- **Increases**: arousal, stress, cognitive load
- **Decreases**: relaxation, habituation

## References

- Boucsein, W. (2012). Electrodermal activity (2nd ed.). Springer Science & Business Media.
- Greco, A., Valenza, G., & Scilingo, E. P. (2016). cvxEDA: A convex optimization approach to electrodermal activity processing. IEEE Transactions on Biomedical Engineering, 63(4), 797-804.
- Posada-Quintero, H. F., Florian, J. P., Orjuela-Cañón, A. D., Aljama-Corrales, T., Charleston-Villalobos, S., & Chon, K. H. (2016). Power spectral density analysis of electrodermal activity for sympathetic function assessment. Annals of biomedical engineering, 44(10), 3124-3135.
- Dawson, M. E., Schell, A. M., & Filion, D. L. (2017). The electrodermal system. In Handbook of psychophysiology (pp. 217-243). Cambridge University Press.

---

## Reference: Eeg

# EEG Analysis and Microstates

## Overview

Analyze electroencephalography (EEG) signals for frequency band power, channel quality assessment, source localization, and microstate identification. NeuroKit2 integrates with MNE-Python for comprehensive EEG processing workflows.

## Core EEG Functions

### eeg_power()

Compute power across standard frequency bands for specified channels.

```python
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'],
                     frequency_bands={'Delta': (0.5, 4),
                                     'Theta': (4, 8),
                                     'Alpha': (8, 13),
                                     'Beta': (13, 30),
                                     'Gamma': (30, 45)})
```

**Standard frequency bands:**
- **Delta (0.5-4 Hz)**: Deep sleep, unconscious processes
- **Theta (4-8 Hz)**: Drowsiness, meditation, memory encoding
- **Alpha (8-13 Hz)**: Relaxed wakefulness, eyes closed
- **Beta (13-30 Hz)**: Active thinking, focus, anxiety
- **Gamma (30-45 Hz)**: Cognitive processing, binding

**Returns:**
- DataFrame with power values for each channel × frequency band combination
- Columns: `Channel_Band` (e.g., 'Fz_Alpha', 'Cz_Beta')

**Use cases:**
- Resting state analysis
- Cognitive state classification
- Sleep staging
- Meditation or neurofeedback monitoring

### eeg_badchannels()

Identify problematic channels using statistical outlier detection.

```python
bad_channels = nk.eeg_badchannels(eeg_data, sampling_rate=250, bad_threshold=2)
```

**Detection methods:**
- Standard deviation outliers across channels
- Correlation with other channels
- Flat or dead channels
- Channels with excessive noise

**Parameters:**
- `bad_threshold`: Z-score threshold for outlier detection (default: 2)

**Returns:**
- List of channel names identified as problematic

**Use case:**
- Quality control before analysis
- Automatic bad channel rejection
- Interpolation or exclusion decisions

### eeg_rereference()

Re-express voltage measurements relative to different reference points.

```python
rereferenced = nk.eeg_rereference(eeg_data, reference='average', robust=False)
```

**Reference types:**
- `'average'`: Average reference (mean of all electrodes)
- `'REST'`: Reference Electrode Standardization Technique
- `'bipolar'`: Differential recording between electrode pairs
- Specific channel name: Use single electrode as reference

**Common references:**
- **Average reference**: Most common for high-density EEG
- **Linked mastoids**: Traditional clinical EEG
- **Vertex (Cz)**: Sometimes used in ERP research
- **REST**: Approximates infinity reference

**Returns:**
- Re-referenced EEG data

### eeg_gfp()

Compute Global Field Power - the standard deviation of all electrodes at each time point.

```python
gfp = nk.eeg_gfp(eeg_data)
```

**Interpretation:**
- High GFP: Strong, synchronized brain activity across regions
- Low GFP: Weak or desynchronized activity
- GFP peaks: Points of stable topography, used for microstate detection

**Use cases:**
- Identify periods of stable topographic patterns
- Select time points for microstate analysis
- Event-related potential (ERP) visualization

### eeg_diss()

Measure topographic dissimilarity between electric field configurations.

```python
dissimilarity = nk.eeg_diss(eeg_data1, eeg_data2, method='gfp')
```

**Methods:**
- GFP-based: Normalized difference
- Spatial correlation
- Cosine distance

**Use case:**
- Compare topographies between conditions
- Microstate transition analysis
- Template matching

## Source Localization

### eeg_source()

Perform source reconstruction to estimate brain-level activity from scalp recordings.

```python
sources = nk.eeg_source(eeg_data, method='sLORETA')
```

**Methods:**
- `'sLORETA'`: Standardized Low-Resolution Electromagnetic Tomography
  - Zero localization error for point sources
  - Good spatial resolution
- `'MNE'`: Minimum Norm Estimate
  - Fast, well-established
  - Bias toward superficial sources
- `'dSPM'`: Dynamic Statistical Parametric Mapping
  - Normalized MNE
- `'eLORETA'`: Exact LORETA
  - Improved localization accuracy

**Requirements:**
- Forward model (lead field matrix)
- Co-registered electrode positions
- Head model (boundary element or spherical)

**Returns:**
- Source space activity estimates

### eeg_source_extract()

Extract activity from specific anatomical brain regions.

```python
regional_activity = nk.eeg_source_extract(sources, regions=['PFC', 'MTL', 'Parietal'])
```

**Region options:**
- Standard atlases: Desikan-Killiany, Destrieux, AAL
- Custom ROIs
- Brodmann areas

**Returns:**
- Time series for each region
- Averaged or principal component across voxels

**Use cases:**
- Region-of-interest analysis
- Functional connectivity
- Source-level statistics

## Microstate Analysis

Microstates are brief (80-120 ms) periods of stable brain topography, representing coordinated neural networks. Typically 4-7 microstate classes (often labeled A, B, C, D) with distinct functions.

### microstates_segment()

Identify and extract microstates using clustering algorithms.

```python
microstates = nk.microstates_segment(eeg_data, n_microstates=4, sampling_rate=250,
                                      method='kmod', normalize=True)
```

**Methods:**
- `'kmod'` (default): Modified k-means optimized for EEG topographies
  - Polarity-invariant clustering
  - Most common in microstate literature
- `'kmeans'`: Standard k-means clustering
- `'kmedoids'`: K-medoids (more robust to outliers)
- `'pca'`: Principal component analysis
- `'ica'`: Independent component analysis
- `'aahc'`: Atomize and agglomerate hierarchical clustering

**Parameters:**
- `n_microstates`: Number of microstate classes (typically 4-7)
- `normalize`: Normalize topographies (recommended: True)
- `n_inits`: Number of random initializations (increase for stability)

**Returns:**
- Dictionary with:
  - `'maps'`: Microstate template topographies
  - `'labels'`: Microstate label at each time point
  - `'gfp'`: Global field power
  - `'gev'`: Global explained variance

### microstates_findnumber()

Estimate the optimal number of microstates.

```python
optimal_k = nk.microstates_findnumber(eeg_data, show=True)
```

**Criteria:**
- **Global Explained Variance (GEV)**: Percentage of variance explained
  - Elbow method: find "knee" in GEV curve
  - Typically 70-80% GEV achieved
- **Krzanowski-Lai (KL) Criterion**: Statistical measure balancing fit and parsimony
  - Maximum KL indicates optimal k

**Typical range:** 4-7 microstates
- 4 microstates: Classic A, B, C, D states
- 5-7 microstates: Finer-grained decomposition

### microstates_classify()

Reorder microstates based on anterior-posterior and left-right channel values.

```python
classified = nk.microstates_classify(microstates)
```

**Purpose:**
- Standardize microstate labels across subjects
- Match conventional A, B, C, D topographies:
  - **A**: Left-right orientation, parieto-occipital
  - **B**: Right-left orientation, fronto-temporal
  - **C**: Anterior-posterior orientation, frontal-central
  - **D**: Fronto-central, anterior-posterior (inverse of C)

**Returns:**
- Reordered microstate maps and labels

### microstates_clean()

Preprocess EEG data for microstate extraction.

```python
cleaned_eeg = nk.microstates_clean(eeg_data, sampling_rate=250)
```

**Preprocessing steps:**
- Bandpass filtering (typically 2-20 Hz)
- Artifact rejection
- Bad channel interpolation
- Re-referencing to average

**Rationale:**
- Microstates reflect large-scale network activity
- High-frequency and low-frequency artifacts can distort topographies

### microstates_peaks()

Identify GFP peaks for microstate analysis.

```python
peak_indices = nk.microstates_peaks(eeg_data, sampling_rate=250)
```

**Purpose:**
- Microstates typically analyzed at GFP peaks
- Peaks represent moments of maximal, stable topographic activity
- Reduces computational load and noise sensitivity

**Returns:**
- Indices of GFP local maxima

### microstates_static()

Compute temporal properties of individual microstates.

```python
static_metrics = nk.microstates_static(microstates)
```

**Metrics:**
- **Duration (ms)**: Mean time spent in each microstate
  - Typical: 80-120 ms
  - Reflects stability and persistence
- **Occurrence (per second)**: Frequency of microstate appearances
  - How often each state is entered
- **Coverage (%)**: Percentage of total time in each microstate
  - Relative dominance
- **Global Explained Variance (GEV)**: Variance explained by each class
  - Quality of template fit

**Returns:**
- DataFrame with metrics for each microstate class

**Interpretation:**
- Changes in duration: altered network stability
- Changes in occurrence: shifting state dynamics
- Changes in coverage: dominance of specific networks

### microstates_dynamic()

Analyze transition patterns between microstates.

```python
dynamic_metrics = nk.microstates_dynamic(microstates)
```

**Metrics:**
- **Transition matrix**: Probability of transitioning from state i to state j
  - Reveals preferential sequences
- **Transition rate**: Overall transition frequency
  - Higher rate: more rapid switching
- **Entropy**: Randomness of transitions
  - High entropy: unpredictable switching
  - Low entropy: stereotyped sequences
- **Markov test**: Are transitions history-dependent?

**Returns:**
- Dictionary with transition statistics

**Use cases:**
- Identify abnormal microstate sequences in clinical populations
- Network dynamics and flexibility
- State-dependent information processing

### microstates_plot()

Visualize microstate topographies and time course.

```python
nk.microstates_plot(microstates, eeg_data)
```

**Displays:**
- Topographic maps for each microstate class
- GFP trace with microstate labels
- Transition plot showing state sequences
- Statistical summary

## MNE Integration Utilities

### mne_data()

Access sample datasets from MNE-Python.

```python
raw = nk.mne_data(dataset='sample', directory=None)
```

**Available datasets:**
- `'sample'`: Multi-modal (MEG/EEG) example
- `'ssvep'`: Steady-state visual evoked potentials
- `'eegbci'`: Motor imagery BCI dataset

### mne_to_df() / mne_to_dict()

Convert MNE objects to NeuroKit-compatible formats.

```python
df = nk.mne_to_df(raw)
data_dict = nk.mne_to_dict(epochs)
```

**Use case:**
- Work with MNE-processed data in NeuroKit2
- Convert between formats for analysis

### mne_channel_add() / mne_channel_extract()

Manage individual channels in MNE objects.

```python
# Extract specific channels
subset = nk.mne_channel_extract(raw, ['Fz', 'Cz', 'Pz'])

# Add derived channels
raw_with_eog = nk.mne_channel_add(raw, new_channel_data, ch_name='EOG')
```

### mne_crop()

Trim recordings by time or samples.

```python
cropped = nk.mne_crop(raw, tmin=10, tmax=100)
```

### mne_templateMRI()

Provide template anatomy for source localization.

```python
subjects_dir = nk.mne_templateMRI()
```

**Use case:**
- Source analysis without individual MRI
- Group-level source localization
- fsaverage template brain

### eeg_simulate()

Generate synthetic EEG signals for testing.

```python
synthetic_eeg = nk.eeg_simulate(duration=60, sampling_rate=250, n_channels=32)
```

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 100 Hz for basic power analysis
- **Standard**: 250-500 Hz for most applications
- **High-resolution**: 1000+ Hz for detailed temporal dynamics

### Recording Duration
- **Power analysis**: ≥2 minutes for stable estimates
- **Microstates**: ≥2-5 minutes, longer preferred
- **Resting state**: 3-10 minutes typical
- **Event-related**: Depends on trial count (≥30 trials per condition)

### Artifact Management
- **Eye blinks**: Remove with ICA or regression
- **Muscle artifacts**: High-pass filter (≥1 Hz) or manual rejection
- **Bad channels**: Detect and interpolate before analysis
- **Line noise**: Notch filter at 50/60 Hz

### Best Practices

**Power analysis:**
```python
# 1. Clean data
cleaned = nk.signal_filter(eeg_data, sampling_rate=250, lowcut=0.5, highcut=45)

# 2. Identify and interpolate bad channels
bad = nk.eeg_badchannels(cleaned, sampling_rate=250)
# Interpolate bad channels using MNE

# 3. Re-reference
rereferenced = nk.eeg_rereference(cleaned, reference='average')

# 4. Compute power
power = nk.eeg_power(rereferenced, sampling_rate=250, channels=channel_list)
```

**Microstate workflow:**
```python
# 1. Preprocess
cleaned = nk.microstates_clean(eeg_data, sampling_rate=250)

# 2. Determine optimal number of states
optimal_k = nk.microstates_findnumber(cleaned, show=True)

# 3. Segment microstates
microstates = nk.microstates_segment(cleaned, n_microstates=optimal_k,
                                     sampling_rate=250, method='kmod')

# 4. Classify to standard labels
microstates = nk.microstates_classify(microstates)

# 5. Compute temporal metrics
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)

# 6. Visualize
nk.microstates_plot(microstates, cleaned)
```

## Clinical and Research Applications

**Cognitive neuroscience:**
- Attention, working memory, executive function
- Language processing
- Sensory perception

**Clinical populations:**
- Epilepsy: seizure detection, localization
- Alzheimer's disease: slowing of EEG, microstate alterations
- Schizophrenia: altered microstates, especially state C
- ADHD: increased theta/beta ratio
- Depression: frontal alpha asymmetry

**Consciousness research:**
- Anesthesia monitoring
- Disorders of consciousness
- Sleep staging

**Neurofeedback:**
- Real-time frequency band training
- Alpha enhancement for relaxation
- Beta enhancement for focus

## References

- Michel, C. M., & Koenig, T. (2018). EEG microstates as a tool for studying the temporal dynamics of whole-brain neuronal networks: A review. Neuroimage, 180, 577-593.
- Pascual-Marqui, R. D., Michel, C. M., & Lehmann, D. (1995). Segmentation of brain electrical activity into microstates: model estimation and validation. IEEE Transactions on Biomedical Engineering, 42(7), 658-665.
- Gramfort, A., Luessi, M., Larson, E., Engemann, D. A., Strohmeier, D., Brodbeck, C., ... & Hämäläinen, M. (2013). MEG and EEG data analysis with MNE-Python. Frontiers in neuroscience, 7, 267.

---

## Reference: Emg

# Electromyography (EMG) Analysis

## Overview

Electromyography (EMG) measures electrical activity produced by skeletal muscles during contraction. EMG analysis in NeuroKit2 focuses on amplitude estimation, muscle activation detection, and temporal dynamics for psychophysiology and motor control research.

## Main Processing Pipeline

### emg_process()

Automated EMG signal processing pipeline.

```python
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)
```

**Pipeline steps:**
1. Signal cleaning (high-pass filtering, detrending)
2. Amplitude envelope extraction
3. Muscle activation detection
4. Onset and offset identification

**Returns:**
- `signals`: DataFrame with:
  - `EMG_Clean`: Filtered EMG signal
  - `EMG_Amplitude`: Linear envelope (smoothed rectified signal)
  - `EMG_Activity`: Binary activation indicator (0/1)
  - `EMG_Onsets`: Activation onset markers
  - `EMG_Offsets`: Activation offset markers
- `info`: Dictionary with activation parameters

**Typical workflow:**
- Process raw EMG → Extract amplitude → Detect activations → Analyze features

## Preprocessing Functions

### emg_clean()

Apply filtering to remove noise and prepare for amplitude extraction.

```python
cleaned_emg = nk.emg_clean(emg_signal, sampling_rate=1000)
```

**Filtering approach (BioSPPy method):**
- Fourth-order Butterworth high-pass filter (100 Hz)
- Removes low-frequency movement artifacts and baseline drift
- Removes DC offset
- Signal detrending

**Rationale:**
- EMG frequency content: 20-500 Hz (dominant: 50-150 Hz)
- High-pass at 100 Hz isolates muscle activity
- Removes ECG contamination (especially in trunk muscles)
- Removes motion artifacts (<20 Hz)

**EMG signal characteristics:**
- Random, zero-mean oscillations during contraction
- Higher amplitude = stronger contraction
- Raw EMG: both positive and negative deflections

## Feature Extraction

### emg_amplitude()

Compute linear envelope representing muscle contraction intensity.

```python
amplitude = nk.emg_amplitude(cleaned_emg, sampling_rate=1000)
```

**Method:**
1. Full-wave rectification (absolute value)
2. Low-pass filtering (smooth envelope)
3. Downsampling (optional)

**Linear envelope:**
- Smooth curve following EMG amplitude modulation
- Represents muscle force/activation level
- Suitable for further analysis (activation detection, integration)

**Typical smoothing:**
- Low-pass filter: 10-20 Hz cutoff
- Moving average: 50-200 ms window
- Balance: responsiveness vs. smoothness

## Activation Detection

### emg_activation()

Detect periods of muscle activation (onsets and offsets).

```python
activity, info = nk.emg_activation(emg_amplitude, sampling_rate=1000, method='threshold',
                                   threshold='auto', duration_min=0.05)
```

**Methods:**

**1. Threshold-based (default):**
```python
activity = nk.emg_activation(amplitude, method='threshold', threshold='auto')
```
- Compares amplitude to threshold
- `threshold='auto'`: Automatic based on signal statistics (e.g., mean + 1 SD)
- `threshold=0.1`: Manual absolute threshold
- Simple, fast, widely used

**2. Gaussian Mixture Model (GMM):**
```python
activity = nk.emg_activation(amplitude, method='mixture', n_clusters=2)
```
- Unsupervised clustering: active vs. rest
- Adaptive to signal characteristics
- More robust to varying baseline

**3. Changepoint detection:**
```python
activity = nk.emg_activation(amplitude, method='changepoint')
```
- Detects abrupt transitions in signal properties
- Identifies activation/deactivation points
- Useful for complex temporal patterns

**4. Bimodality (Silva et al., 2013):**
```python
activity = nk.emg_activation(amplitude, method='bimodal')
```
- Tests for bimodal distribution (active vs. rest)
- Determines optimal separation threshold
- Statistically principled

**Key parameters:**
- `duration_min`: Minimum activation duration (seconds)
  - Filters brief spurious activations
  - Typical: 50-100 ms
- `threshold`: Activation threshold (method-dependent)

**Returns:**
- `activity`: Binary array (0 = rest, 1 = active)
- `info`: Dictionary with onset/offset indices

**Activation metrics:**
- **Onset**: Transition from rest to activity
- **Offset**: Transition from activity to rest
- **Duration**: Time between onset and offset
- **Burst**: Single period of continuous activation

## Analysis Functions

### emg_analyze()

Automatically select event-related or interval-related analysis.

```python
analysis = nk.emg_analyze(signals, sampling_rate=1000)
```

**Mode selection:**
- Duration < 10 seconds → event-related
- Duration ≥ 10 seconds → interval-related

### emg_eventrelated()

Analyze EMG responses to discrete events/stimuli.

```python
results = nk.emg_eventrelated(epochs)
```

**Computed metrics (per epoch):**
- `EMG_Activation`: Presence of activation (binary)
- `EMG_Amplitude_Mean`: Average amplitude during epoch
- `EMG_Amplitude_Max`: Peak amplitude
- `EMG_Bursts`: Number of activation bursts
- `EMG_Onset_Latency`: Time from event to first activation (if applicable)

**Use cases:**
- Startle response (orbicularis oculi EMG)
- Facial EMG during emotional stimuli (corrugator, zygomaticus)
- Motor response latencies
- Muscle reactivity paradigms

### emg_intervalrelated()

Analyze extended EMG recordings.

```python
results = nk.emg_intervalrelated(signals, sampling_rate=1000)
```

**Computed metrics:**
- `EMG_Bursts_N`: Total number of activation bursts
- `EMG_Amplitude_Mean`: Mean amplitude across entire interval
- `EMG_Activation_Duration`: Total time in active state
- `EMG_Rest_Duration`: Total time in rest state

**Use cases:**
- Resting muscle tension assessment
- Chronic pain or stress-related muscle activity
- Fatigue monitoring during sustained tasks
- Postural muscle assessment

## Simulation and Visualization

### emg_simulate()

Generate synthetic EMG signals for testing.

```python
synthetic_emg = nk.emg_simulate(duration=10, sampling_rate=1000, burst_number=3,
                                noise=0.1, random_state=42)
```

**Parameters:**
- `burst_number`: Number of activation bursts to include
- `noise`: Background noise level
- `random_state`: Reproducibility seed

**Generated features:**
- Random EMG-like oscillations during bursts
- Realistic frequency content
- Variable burst timing and amplitude

**Use cases:**
- Algorithm validation
- Detection parameter tuning
- Educational demonstrations

### emg_plot()

Visualize processed EMG signal.

```python
nk.emg_plot(signals, info, static=True)
```

**Displays:**
- Raw and cleaned EMG signal
- Amplitude envelope
- Detected activation periods
- Onset/offset markers

**Interactive mode:** Set `static=False` for Plotly visualization

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 500 Hz (Nyquist for 250 Hz upper frequency)
- **Standard**: 1000 Hz (most research applications)
- **High-resolution**: 2000-4000 Hz (detailed motor unit studies)
- **Surface EMG**: 1000-2000 Hz typical
- **Intramuscular EMG**: 10,000+ Hz for single motor units

### Recording Duration
- **Event-related**: Depends on paradigm (e.g., 2-5 seconds per trial)
- **Sustained contraction**: Seconds to minutes
- **Fatigue studies**: Minutes to hours
- **Chronic monitoring**: Days (wearable EMG)

### Electrode Placement

**Surface EMG (most common):**
- Bipolar configuration (two electrodes over muscle belly)
- Reference/ground electrode over electrically neutral site (bone)
- Skin preparation: clean, abrade, reduce impedance
- Inter-electrode distance: 10-20 mm (SENIAM standards)

**Muscle-specific guidelines:**
- Follow SENIAM (Surface EMG for Non-Invasive Assessment of Muscles) recommendations
- Palpate muscle during contraction to locate belly
- Align electrodes with muscle fiber direction

**Common muscles in psychophysiology:**
- **Corrugator supercilii**: Frowning, negative affect (above eyebrow)
- **Zygomaticus major**: Smiling, positive affect (cheek)
- **Orbicularis oculi**: Startle response, fear (around eye)
- **Masseter**: Jaw clenching, stress (jaw muscle)
- **Trapezius**: Shoulder tension, stress (upper back)
- **Frontalis**: Forehead tension, surprise

### Signal Quality Issues

**ECG contamination:**
- Common in trunk and proximal muscles
- High-pass filtering (>100 Hz) usually sufficient
- If persistent: template subtraction, ICA

**Motion artifacts:**
- Low-frequency disturbances
- Electrode cable movement
- Secure electrodes, minimize cable motion

**Electrode issues:**
- Poor contact: high impedance, low amplitude
- Sweat: gradual amplitude increase, instability
- Hair: clean or shave area

**Cross-talk:**
- Adjacent muscle activity bleeding into recording
- Careful electrode placement
- Small inter-electrode distance

### Best Practices

**Standard workflow:**
```python
# 1. Clean signal (high-pass filter, detrend)
cleaned = nk.emg_clean(emg_raw, sampling_rate=1000)

# 2. Extract amplitude envelope
amplitude = nk.emg_amplitude(cleaned, sampling_rate=1000)

# 3. Detect activation periods
activity, info = nk.emg_activation(amplitude, sampling_rate=1000,
                                   method='threshold', threshold='auto')

# 4. Comprehensive processing (alternative)
signals, info = nk.emg_process(emg_raw, sampling_rate=1000)

# 5. Analyze
analysis = nk.emg_analyze(signals, sampling_rate=1000)
```

**Normalization:**
```python
# Maximum voluntary contraction (MVC) normalization
mvc_amplitude = np.max(mvc_emg_amplitude)  # From separate MVC trial
normalized_emg = (amplitude / mvc_amplitude) * 100  # Express as % MVC

# Common in ergonomics, exercise physiology
# Allows comparison across individuals and sessions
```

## Clinical and Research Applications

**Psychophysiology:**
- **Facial EMG**: Emotional valence (smile vs. frown)
- **Startle response**: Fear, surprise, defensive reactivity
- **Stress**: Chronic muscle tension (trapezius, masseter)

**Motor control and rehabilitation:**
- Gait analysis
- Movement disorders (tremor, dystonia)
- Stroke rehabilitation (muscle re-activation)
- Prosthetic control (myoelectric)

**Ergonomics and occupational health:**
- Work-related musculoskeletal disorders
- Postural assessment
- Repetitive strain injury risk

**Sports science:**
- Muscle activation patterns during exercise
- Fatigue assessment (median frequency shift)
- Training optimization

**Biofeedback:**
- Relaxation training (reduce muscle tension)
- Neuromuscular re-education
- Chronic pain management

**Sleep medicine:**
- Chin EMG for REM sleep atonia
- Periodic limb movements
- Bruxism (teeth grinding)

## Advanced EMG Analysis (Beyond NeuroKit2 Basic Functions)

**Frequency domain:**
- Median frequency shift during fatigue
- Power spectrum analysis
- Requires longer segments (≥1 second per analysis window)

**Motor unit identification:**
- Intramuscular EMG
- Spike detection and sorting
- Firing rate analysis
- Requires high sampling rates (10+ kHz)

**Muscle coordination:**
- Co-contraction indices
- Synergy analysis
- Multi-muscle integration

## Interpretation Guidelines

**Amplitude (linear envelope):**
- Higher amplitude ≈ stronger contraction (not perfectly linear)
- Relationship to force: sigmoid, influenced by many factors
- Within-subject comparisons most reliable

**Activation threshold:**
- Automatic thresholds: convenient but verify visually
- Manual thresholds: may be needed for non-standard muscles
- Resting baseline: should be near zero (if not, check electrodes)

**Burst characteristics:**
- **Phasic**: Brief bursts (startle, rapid movements)
- **Tonic**: Sustained activation (postural, sustained grip)
- **Rhythmic**: Repeated bursts (tremor, walking)

## References

- Fridlund, A. J., & Cacioppo, J. T. (1986). Guidelines for human electromyographic research. Psychophysiology, 23(5), 567-589.
- Hermens, H. J., Freriks, B., Disselhorst-Klug, C., & Rau, G. (2000). Development of recommendations for SEMG sensors and sensor placement procedures. Journal of electromyography and Kinesiology, 10(5), 361-374.
- Silva, H., Scherer, R., Sousa, J., & Londral, A. (2013). Towards improving the ssability of electromyographic interfaces. Journal of Oral Rehabilitation, 40(6), 456-465.
- Tassinary, L. G., Cacioppo, J. T., & Vanman, E. J. (2017). The skeletomotor system: Surface electromyography. In Handbook of psychophysiology (pp. 267-299). Cambridge University Press.

---

## Reference: Eog

# Electrooculography (EOG) Analysis

## Overview

Electrooculography (EOG) measures eye movements and blinks by detecting electrical potential differences generated by eye position changes. EOG is used in sleep studies, attention research, reading analysis, and artifact correction for EEG.

## Main Processing Pipeline

### eog_process()

Automated EOG signal processing pipeline.

```python
signals, info = nk.eog_process(eog_signal, sampling_rate=500, method='neurokit')
```

**Pipeline steps:**
1. Signal cleaning (filtering)
2. Blink detection
3. Blink rate calculation

**Returns:**
- `signals`: DataFrame with:
  - `EOG_Clean`: Filtered EOG signal
  - `EOG_Blinks`: Binary blink markers (0/1)
  - `EOG_Rate`: Instantaneous blink rate (blinks/min)
- `info`: Dictionary with blink indices and parameters

**Methods:**
- `'neurokit'`: NeuroKit2 optimized approach (default)
- `'agarwal2019'`: Agarwal et al. (2019) algorithm
- `'mne'`: MNE-Python method
- `'brainstorm'`: Brainstorm toolbox approach
- `'kong1998'`: Kong et al. (1998) method

## Preprocessing Functions

### eog_clean()

Prepare raw EOG signal for blink detection.

```python
cleaned_eog = nk.eog_clean(eog_signal, sampling_rate=500, method='neurokit')
```

**Methods:**
- `'neurokit'`: Butterworth filtering optimized for EOG
- `'agarwal2019'`: Alternative filtering
- `'mne'`: MNE-Python preprocessing
- `'brainstorm'`: Brainstorm approach
- `'kong1998'`: Kong's method

**Typical filtering:**
- Low-pass: 10-20 Hz (remove high-frequency noise)
- High-pass: 0.1-1 Hz (remove DC drift)
- Preserves blink waveform (typical duration 100-400 ms)

**EOG signal characteristics:**
- **Blinks**: Large amplitude, stereotyped waveform (200-400 ms)
- **Saccades**: Rapid step-like deflections (20-80 ms)
- **Smooth pursuit**: Slow ramp-like changes
- **Baseline**: Stable when eyes fixated

## Blink Detection

### eog_peaks()

Detect eye blinks in EOG signal.

```python
blinks, info = nk.eog_peaks(cleaned_eog, sampling_rate=500, method='neurokit',
                            threshold=0.33)
```

**Methods:**
- `'neurokit'`: Amplitude and duration criteria (default)
- `'mne'`: MNE-Python blink detection
- `'brainstorm'`: Brainstorm approach
- `'blinker'`: BLINKER algorithm (Kleifges et al., 2017)

**Key parameters:**
- `threshold`: Amplitude threshold (fraction of max amplitude)
  - Typical: 0.2-0.5
  - Lower: more sensitive (may include false positives)
  - Higher: more conservative (may miss small blinks)

**Returns:**
- Dictionary with `'EOG_Blinks'` key containing blink peak indices

**Blink characteristics:**
- **Frequency**: 15-20 blinks/min (resting, comfortable)
- **Duration**: 100-400 ms (mean ~200 ms)
- **Amplitude**: Varies with electrode placement and individual factors
- **Waveform**: Biphasic or triphasic

### eog_findpeaks()

Low-level blink detection with multiple algorithms.

```python
blinks_dict = nk.eog_findpeaks(cleaned_eog, sampling_rate=500, method='neurokit')
```

**Use cases:**
- Custom parameter tuning
- Algorithm comparison
- Research method development

## Feature Extraction

### eog_features()

Extract characteristics of individual blinks.

```python
features = nk.eog_features(signals, sampling_rate=500)
```

**Computed features:**
- **Amplitude velocity ratio (AVR)**: Peak velocity / amplitude
  - Discriminates blinks from artifacts
- **Blink-amplitude ratio**: Consistency of blink amplitudes
- **Duration metrics**: Blink duration statistics (mean, SD)
- **Peak amplitude**: Maximum deflection
- **Peak velocity**: Maximum rate of change

**Use cases:**
- Blink quality assessment
- Drowsiness detection (blink duration increases when sleepy)
- Neurological assessment (altered blink dynamics in disease)

### eog_rate()

Compute blink frequency (blinks per minute).

```python
blink_rate = nk.eog_rate(blinks, sampling_rate=500, desired_length=None)
```

**Method:**
- Calculate inter-blink intervals
- Convert to blinks per minute
- Interpolate to match signal length

**Typical blink rates:**
- **Resting**: 15-20 blinks/min
- **Reading/visual tasks**: 5-10 blinks/min (suppressed)
- **Conversation**: 20-30 blinks/min
- **Stress/dry eyes**: >30 blinks/min
- **Drowsiness**: Variable, longer blinks

## Analysis Functions

### eog_analyze()

Automatically select event-related or interval-related analysis.

```python
analysis = nk.eog_analyze(signals, sampling_rate=500)
```

**Mode selection:**
- Duration < 10 seconds → event-related
- Duration ≥ 10 seconds → interval-related

### eog_eventrelated()

Analyze blink patterns relative to specific events.

```python
results = nk.eog_eventrelated(epochs)
```

**Computed metrics (per epoch):**
- `EOG_Blinks_N`: Number of blinks during epoch
- `EOG_Rate_Mean`: Average blink rate
- `EOG_Blink_Presence`: Binary (any blinks occurred)
- Temporal distribution of blinks across epoch

**Use cases:**
- Blink-locked ERP contamination assessment
- Attention and engagement during stimuli
- Visual task difficulty (suppressed blinks during demanding tasks)
- Spontaneous blinks after stimulus offset

### eog_intervalrelated()

Analyze blink patterns over extended periods.

```python
results = nk.eog_intervalrelated(signals, sampling_rate=500)
```

**Computed metrics:**
- `EOG_Blinks_N`: Total number of blinks
- `EOG_Rate_Mean`: Average blink rate (blinks/min)
- `EOG_Rate_SD`: Blink rate variability
- `EOG_Duration_Mean`: Average blink duration (if available)
- `EOG_Amplitude_Mean`: Average blink amplitude (if available)

**Use cases:**
- Resting state blink patterns
- Drowsiness or fatigue monitoring (increased duration)
- Sustained attention tasks (suppressed rate)
- Dry eye assessment (increased rate, incomplete blinks)

## Simulation and Visualization

### eog_plot()

Visualize processed EOG signal and detected blinks.

```python
nk.eog_plot(signals, info)
```

**Displays:**
- Raw and cleaned EOG signal
- Detected blink markers
- Blink rate time course

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 100 Hz (basic blink detection)
- **Standard**: 250-500 Hz (research applications)
- **High-resolution**: 1000 Hz (detailed waveform analysis, saccades)
- **Sleep studies**: 200-250 Hz typical

### Recording Duration
- **Blink detection**: Any duration (≥1 blink)
- **Blink rate estimation**: ≥60 seconds for stable estimate
- **Event-related**: Depends on paradigm (seconds per trial)
- **Sleep EOG**: Hours (full night)

### Electrode Placement

**Standard configurations:**

**Horizontal EOG (HEOG):**
- Two electrodes: lateral canthi (outer corners) of left and right eyes
- Measures horizontal eye movements (saccades, smooth pursuit)
- Bipolar recording (left - right)

**Vertical EOG (VEOG):**
- Two electrodes: above and below one eye (typically right)
- Measures vertical eye movements and blinks
- Bipolar recording (above - below)

**Sleep EOG:**
- Often uses slightly different placement (temple area)
- E1: 1 cm lateral and 1 cm below outer canthus of left eye
- E2: 1 cm lateral and 1 cm above outer canthus of right eye
- Captures both horizontal and vertical movements

**EEG contamination removal:**
- Frontal electrodes (Fp1, Fp2) can serve as EOG proxies
- ICA-based EOG artifact removal common in EEG preprocessing

### Common Issues and Solutions

**Electrode issues:**
- Poor contact: low amplitude, noise
- Skin preparation: clean, light abrasion
- Conductive gel: ensure good contact

**Artifacts:**
- Muscle activity (especially frontalis): high-frequency noise
- Movement: cable artifacts, head motion
- Electrical noise: 50/60 Hz hum (ground properly)

**Saturation:**
- Large saccades may saturate amplifier
- Adjust gain or voltage range
- More common with low-resolution systems

### Best Practices

**Standard workflow:**
```python
# 1. Clean signal
cleaned = nk.eog_clean(eog_raw, sampling_rate=500, method='neurokit')

# 2. Detect blinks
blinks, info = nk.eog_peaks(cleaned, sampling_rate=500, method='neurokit')

# 3. Extract features
features = nk.eog_features(signals, sampling_rate=500)

# 4. Comprehensive processing (alternative)
signals, info = nk.eog_process(eog_raw, sampling_rate=500)

# 5. Analyze
analysis = nk.eog_analyze(signals, sampling_rate=500)
```

**EEG artifact correction workflow:**
```python
# Option 1: Regression-based removal
# Identify EOG components from cleaned EOG signal
# Regress out EOG from EEG channels

# Option 2: ICA-based removal (preferred)
# 1. Run ICA on EEG data including EOG channels
# 2. Identify ICA components correlated with EOG
# 3. Remove EOG components from EEG data
# NeuroKit2 integrates with MNE for this workflow
```

## Clinical and Research Applications

**EEG artifact correction:**
- Blinks contaminate frontal EEG channels
- ICA or regression methods remove EOG artifacts
- Essential for ERP studies

**Sleep staging:**
- Rapid eye movements (REMs) during REM sleep
- Slow rolling eye movements during drowsiness
- Sleep onset and stage transitions

**Attention and cognitive load:**
- Blink rate suppressed during demanding tasks
- Blinks cluster at task boundaries (natural breakpoints)
- Spontaneous blink as indicator of attention shifts

**Fatigue and drowsiness monitoring:**
- Increased blink duration when sleepy
- Slower eyelid closures
- Partial or incomplete blinks
- Driver monitoring applications

**Reading and visual processing:**
- Blinks suppressed during reading
- Eye movements during saccades (line changes)
- Fatigue effects on reading efficiency

**Neurological disorders:**
- **Parkinson's disease**: Reduced spontaneous blink rate
- **Schizophrenia**: Increased blink rate
- **Tourette syndrome**: Excessive blinking (tics)
- **Dry eye syndrome**: Increased, incomplete blinks

**Affective and social cognition:**
- Blink synchrony in social interaction
- Emotional modulation of blink rate
- Blink-related potentials in ERPs

**Human-computer interaction:**
- Gaze tracking preprocessing
- Attention monitoring
- User engagement assessment

## Eye Movement Types Detectable with EOG

**Blinks:**
- Large amplitude, brief duration (100-400 ms)
- NeuroKit2 primary focus
- Vertical EOG most sensitive

**Saccades:**
- Rapid, ballistic eye movements (20-80 ms)
- Step-like voltage deflections
- Horizontal or vertical
- Require higher sampling rates for detailed analysis

**Smooth pursuit:**
- Slow tracking of moving objects
- Ramp-like voltage changes
- Lower amplitude than saccades

**Fixations:**
- Stable gaze
- Baseline EOG with small oscillations
- Duration varies (200-600 ms typical in reading)

**Note:** Detailed saccade/fixation analysis typically requires eye tracking (infrared, video-based). EOG useful for blinks and gross eye movements.

## Interpretation Guidelines

**Blink rate:**
- **Normal resting**: 15-20 blinks/min
- **<10 blinks/min**: Visual task engagement, concentration
- **>30 blinks/min**: Stress, dry eyes, fatigue
- **Context-dependent**: Task demands, lighting, screen use

**Blink duration:**
- **Normal**: 100-400 ms (mean ~200 ms)
- **Prolonged**: Drowsiness, fatigue (>500 ms)
- **Short**: Normal alertness

**Blink amplitude:**
- Varies with electrode placement and individuals
- Within-subject comparisons most reliable
- Incomplete blinks: reduced amplitude (dry eye, fatigue)

**Temporal patterns:**
- **Clustered blinks**: Transitions between tasks or cognitive states
- **Suppressed blinks**: Active visual processing, sustained attention
- **Post-stimulus blinks**: After completing visual processing

## References

- Kleifges, K., Bigdely-Shamlo, N., Kerick, S. E., & Robbins, K. A. (2017). BLINKER: Automated extraction of ocular indices from EEG enabling large-scale analysis. Frontiers in Neuroscience, 11, 12.
- Agarwal, M., & Sivakumar, R. (2019). Blink: A fully automated unsupervised algorithm for eye-blink detection in EEG signals. In 2019 57th Annual Allerton Conference on Communication, Control, and Computing (pp. 1113-1121). IEEE.
- Kong, X., & Wilson, G. F. (1998). A new EOG-based eyeblink detection algorithm. Behavior Research Methods, Instruments, & Computers, 30(4), 713-719.
- Schleicher, R., Galley, N., Briest, S., & Galley, L. (2008). Blinks and saccades as indicators of fatigue in sleepiness warnings: Looking tired? Ergonomics, 51(7), 982-1010.

---

## Reference: Epochs_Events

# Epochs and Event-Related Analysis

## Overview

Event-related analysis examines physiological responses time-locked to specific stimuli or events. NeuroKit2 provides tools for event detection, epoch creation, averaging, and event-related feature extraction across all signal types.

## Event Detection

### events_find()

Automatically detect events/triggers in a signal based on threshold crossings or changes.

```python
events = nk.events_find(event_channel, threshold=0.5, threshold_keep='above',
                        duration_min=1, inter_min=0)
```

**Parameters:**
- `threshold`: Detection threshold value
- `threshold_keep`: `'above'` or `'below'` threshold
- `duration_min`: Minimum event duration (samples) to keep
- `inter_min`: Minimum interval between events (samples)

**Returns:**
- Dictionary with:
  - `'onset'`: Event onset indices
  - `'offset'`: Event offset indices (if applicable)
  - `'duration'`: Event durations
  - `'label'`: Event labels (if multiple event types)

**Common use cases:**

**TTL triggers from experiments:**
```python
# Trigger channel: 0V baseline, 5V pulses during events
events = nk.events_find(trigger_channel, threshold=2.5, threshold_keep='above')
```

**Button presses:**
```python
# Detect when button signal goes high
button_events = nk.events_find(button_signal, threshold=0.5, threshold_keep='above',
                               duration_min=10)  # Debounce
```

**State changes:**
```python
# Detect periods above/below threshold
high_arousal = nk.events_find(eda_signal, threshold='auto', duration_min=100)
```

### events_plot()

Visualize event timing relative to signals.

```python
nk.events_plot(events, signal)
```

**Displays:**
- Signal trace
- Event markers (vertical lines or shaded regions)
- Event labels

**Use case:**
- Verify event detection accuracy
- Inspect temporal distribution of events
- Quality control before epoching

## Epoch Creation

### epochs_create()

Create epochs (segments) of data around events for event-related analysis.

```python
epochs = nk.epochs_create(data, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0,
                          event_labels=None, event_conditions=None,
                          baseline_correction=False)
```

**Parameters:**
- `data`: DataFrame with signals or single signal
- `events`: Event indices or dictionary from `events_find()`
- `sampling_rate`: Signal sampling rate (Hz)
- `epochs_start`: Start time relative to event (seconds, negative = before)
- `epochs_end`: End time relative to event (seconds, positive = after)
- `event_labels`: List of labels for each event (optional)
- `event_conditions`: List of condition names for each event (optional)
- `baseline_correction`: If True, subtract baseline mean from each epoch

**Returns:**
- Dictionary of DataFrames, one per epoch
- Each DataFrame contains signal data with time relative to event (Index=0 at event onset)
- Includes `'Label'` and `'Condition'` columns if provided

**Typical epoch windows:**
- **Visual ERP**: -0.2 to 1.0 seconds (200 ms baseline, 1 s post-stimulus)
- **Cardiac orienting**: -1.0 to 10 seconds (capture anticipation and response)
- **EMG startle**: -0.1 to 0.5 seconds (brief response)
- **EDA SCR**: -1.0 to 10 seconds (1-3 s latency, slow recovery)

### Event Labels and Conditions

Organize events by type and experimental conditions:

```python
# Example: Emotional picture experiment
event_times = [1000, 2500, 4200, 5800]  # Event onsets in samples
event_labels = ['trial1', 'trial2', 'trial3', 'trial4']
event_conditions = ['positive', 'negative', 'positive', 'neutral']

epochs = nk.epochs_create(signals, events=event_times, sampling_rate=1000,
                          epochs_start=-1, epochs_end=5,
                          event_labels=event_labels,
                          event_conditions=event_conditions)
```

**Access epochs:**
```python
# Epoch by number
epoch_1 = epochs['1']

# Filter by condition
positive_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'positive'}
```

### Baseline Correction

Remove pre-stimulus baseline from epochs to isolate event-related changes:

**Automatic (during epoch creation):**
```python
epochs = nk.epochs_create(data, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0,
                          baseline_correction=True)  # Subtracts mean of entire baseline
```

**Manual (after epoch creation):**
```python
# Subtract baseline period mean
baseline_start = -0.5  # seconds
baseline_end = 0.0     # seconds

for key, epoch in epochs.items():
    baseline_mask = (epoch.index >= baseline_start) & (epoch.index < baseline_end)
    baseline_mean = epoch[baseline_mask].mean()
    epochs[key] = epoch - baseline_mean
```

**When to baseline correct:**
- **ERPs**: Always (isolates event-related change)
- **Cardiac/EDA**: Usually (removes inter-individual baseline differences)
- **Absolute measures**: Sometimes not desired (e.g., analyzing absolute amplitude)

## Epoch Analysis and Visualization

### epochs_plot()

Visualize individual or averaged epochs.

```python
nk.epochs_plot(epochs, column='ECG_Rate', condition=None, show=True)
```

**Parameters:**
- `column`: Which signal column to plot
- `condition`: Plot only specific condition (optional)

**Displays:**
- Individual epoch traces (semi-transparent)
- Average across epochs (bold line)
- Optional: Shaded error (SEM or SD)

**Use cases:**
- Visualize event-related responses
- Compare conditions
- Identify outlier epochs

### epochs_average()

Compute grand average across epochs with statistics.

```python
average_epochs = nk.epochs_average(epochs, output='dict')
```

**Parameters:**
- `output`: `'dict'` (default) or `'df'` (DataFrame)

**Returns:**
- Dictionary or DataFrame with:
  - `'Mean'`: Average across epochs at each time point
  - `'SD'`: Standard deviation
  - `'SE'`: Standard error of mean
  - `'CI_lower'`, `'CI_upper'`: 95% confidence intervals

**Use case:**
- Compute event-related potentials (ERPs)
- Grand average cardiac/EDA/EMG responses
- Group-level analysis

**Condition-specific averaging:**
```python
# Separate averages by condition
positive_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'positive'}
negative_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'negative'}

avg_positive = nk.epochs_average(positive_epochs)
avg_negative = nk.epochs_average(negative_epochs)
```

### epochs_to_df()

Convert epochs dictionary to unified DataFrame.

```python
epochs_df = nk.epochs_to_df(epochs)
```

**Returns:**
- Single DataFrame with all epochs stacked
- Includes `'Epoch'`, `'Time'`, `'Label'`, `'Condition'` columns
- Facilitates statistical analysis and plotting with pandas/seaborn

**Use case:**
- Prepare data for mixed-effects models
- Plotting with seaborn/plotly
- Export to R or statistical software

### epochs_to_array()

Convert epochs to 3D NumPy array.

```python
epochs_array = nk.epochs_to_array(epochs, column='ECG_Rate')
```

**Returns:**
- 3D array: (n_epochs, n_timepoints, n_columns)

**Use case:**
- Machine learning input (epoched features)
- Custom array-based analysis
- Statistical tests on array data

## Signal-Specific Event-Related Analysis

NeuroKit2 provides specialized event-related analysis for each signal type:

### ECG Event-Related
```python
ecg_epochs = nk.epochs_create(ecg_signals, events, sampling_rate=1000,
                              epochs_start=-1, epochs_end=10)
ecg_results = nk.ecg_eventrelated(ecg_epochs)
```

**Computed metrics:**
- `ECG_Rate_Baseline`: Heart rate before event
- `ECG_Rate_Min/Max`: Minimum/maximum rate during epoch
- `ECG_Phase_*`: Cardiac phase at event onset
- Rate dynamics across time windows

### EDA Event-Related
```python
eda_epochs = nk.epochs_create(eda_signals, events, sampling_rate=100,
                              epochs_start=-1, epochs_end=10)
eda_results = nk.eda_eventrelated(eda_epochs)
```

**Computed metrics:**
- `EDA_SCR`: Presence of SCR (binary)
- `SCR_Amplitude`: Maximum SCR amplitude
- `SCR_Latency`: Time to SCR onset
- `SCR_RiseTime`, `SCR_RecoveryTime`
- `EDA_Tonic`: Mean tonic level

### RSP Event-Related
```python
rsp_epochs = nk.epochs_create(rsp_signals, events, sampling_rate=100,
                              epochs_start=-0.5, epochs_end=5)
rsp_results = nk.rsp_eventrelated(rsp_epochs)
```

**Computed metrics:**
- `RSP_Rate_Mean`: Average breathing rate
- `RSP_Amplitude_Mean`: Average breath depth
- `RSP_Phase`: Respiratory phase at event
- Rate/amplitude dynamics

### EMG Event-Related
```python
emg_epochs = nk.epochs_create(emg_signals, events, sampling_rate=1000,
                              epochs_start=-0.1, epochs_end=1.0)
emg_results = nk.emg_eventrelated(emg_epochs)
```

**Computed metrics:**
- `EMG_Activation`: Presence of activation
- `EMG_Amplitude_Mean/Max`: Amplitude statistics
- `EMG_Onset_Latency`: Time to activation onset
- `EMG_Bursts`: Number of activation bursts

### EOG Event-Related
```python
eog_epochs = nk.epochs_create(eog_signals, events, sampling_rate=500,
                              epochs_start=-0.5, epochs_end=2.0)
eog_results = nk.eog_eventrelated(eog_epochs)
```

**Computed metrics:**
- `EOG_Blinks_N`: Number of blinks during epoch
- `EOG_Rate_Mean`: Blink rate
- Temporal blink distribution

### PPG Event-Related
```python
ppg_epochs = nk.epochs_create(ppg_signals, events, sampling_rate=100,
                              epochs_start=-1, epochs_end=10)
ppg_results = nk.ppg_eventrelated(ppg_epochs)
```

**Computed metrics:**
- Similar to ECG: rate dynamics, phase information

## Practical Workflows

### Complete Event-Related Analysis Pipeline

```python
import neurokit2 as nk

# 1. Process physiological signals
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
eda_signals, eda_info = nk.eda_process(eda, sampling_rate=100)

# 2. Align sampling rates if needed
eda_signals_resampled = nk.signal_resample(eda_signals, sampling_rate=100,
                                           desired_sampling_rate=1000)

# 3. Merge signals into single DataFrame
signals = pd.concat([ecg_signals, eda_signals_resampled], axis=1)

# 4. Detect events
events = nk.events_find(trigger_channel, threshold=0.5)

# 5. Add event labels and conditions
event_labels = ['trial1', 'trial2', 'trial3', ...]
event_conditions = ['condition_A', 'condition_B', 'condition_A', ...]

# 6. Create epochs
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-1.0, epochs_end=5.0,
                          event_labels=event_labels,
                          event_conditions=event_conditions,
                          baseline_correction=True)

# 7. Signal-specific event-related analysis
ecg_results = nk.ecg_eventrelated(epochs)
eda_results = nk.eda_eventrelated(epochs)

# 8. Merge results
results = pd.merge(ecg_results, eda_results, left_index=True, right_index=True)

# 9. Statistical analysis by condition
results['Condition'] = event_conditions
condition_comparison = results.groupby('Condition').mean()
```

### Handling Multiple Event Types

```python
# Different event types with different markers
event_type1 = nk.events_find(trigger_ch1, threshold=0.5)
event_type2 = nk.events_find(trigger_ch2, threshold=0.5)

# Combine events with labels
all_events = np.concatenate([event_type1['onset'], event_type2['onset']])
event_labels = ['type1'] * len(event_type1['onset']) + ['type2'] * len(event_type2['onset'])

# Sort by time
sort_idx = np.argsort(all_events)
all_events = all_events[sort_idx]
event_labels = [event_labels[i] for i in sort_idx]

# Create epochs
epochs = nk.epochs_create(signals, all_events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=3.0,
                          event_labels=event_labels)

# Separate by type
type1_epochs = {k: v for k, v in epochs.items() if v['Label'][0] == 'type1'}
type2_epochs = {k: v for k, v in epochs.items() if v['Label'][0] == 'type2'}
```

### Quality Control and Artifact Rejection

```python
# Remove epochs with excessive noise or artifacts
clean_epochs = {}
for key, epoch in epochs.items():
    # Example: reject if EDA amplitude too high (movement artifact)
    if epoch['EDA_Phasic'].abs().max() < 5.0:  # Threshold
        # Example: reject if heart rate change too large (invalid)
        if epoch['ECG_Rate'].max() - epoch['ECG_Rate'].min() < 50:
            clean_epochs[key] = epoch

print(f"Kept {len(clean_epochs)}/{len(epochs)} epochs")

# Analyze clean epochs
results = nk.ecg_eventrelated(clean_epochs)
```

## Statistical Considerations

### Sample Size
- **ERP/averaging**: 20-30+ trials per condition minimum
- **Individual trial analysis**: Mixed-effects models handle variable trial counts
- **Group comparisons**: Pilot data for power analysis

### Time Window Selection
- **A priori hypotheses**: Pre-register time windows based on literature
- **Exploratory**: Use full epoch, correct for multiple comparisons
- **Avoid**: Selecting windows based on observed data (circular)

### Baseline Period
- Should be free of anticipatory effects
- Sufficient duration for stable estimate (500-1000 ms typical)
- Shorter for fast dynamics (e.g., startle: 100 ms sufficient)

### Condition Comparison
- Repeated measures ANOVA for within-subject designs
- Mixed-effects models for unbalanced data
- Permutation tests for non-parametric comparisons
- Correct for multiple comparisons (time points/signals)

## Common Applications

**Cognitive psychology:**
- P300 ERP analysis
- Error-related negativity (ERN)
- Attentional blink
- Working memory load effects

**Affective neuroscience:**
- Emotional picture viewing (EDA, HR, facial EMG)
- Fear conditioning (HR deceleration, SCR)
- Valence/arousal dimensions

**Clinical research:**
- Startle response (orbicularis oculi EMG)
- Orienting response (HR deceleration)
- Anticipation and prediction error

**Psychophysiology:**
- Cardiac defense response
- Orienting vs. defensive reflexes
- Respiratory changes during emotion

**Human-computer interaction:**
- User engagement during events
- Surprise/violation of expectation
- Cognitive load during task events

## References

- Luck, S. J. (2014). An introduction to the event-related potential technique (2nd ed.). MIT press.
- Bradley, M. M., & Lang, P. J. (2000). Measuring emotion: Behavior, feeling, and physiology. In R. D. Lane & L. Nadel (Eds.), Cognitive neuroscience of emotion (pp. 242-276). Oxford University Press.
- Boucsein, W. (2012). Electrodermal activity (2nd ed.). Springer.
- Gratton, G., Coles, M. G., & Donchin, E. (1983). A new method for off-line removal of ocular artifact. Electroencephalography and clinical neurophysiology, 55(4), 468-484.

---

## Reference: Hrv

# Heart Rate Variability (HRV) Analysis

## Overview

Heart Rate Variability (HRV) reflects the variation in time intervals between consecutive heartbeats, providing insights into autonomic nervous system regulation, cardiovascular health, and psychological state. NeuroKit2 provides comprehensive HRV analysis across time, frequency, and nonlinear domains.

## Main Function

### hrv()

Compute all available HRV indices at once across all domains.

```python
hrv_indices = nk.hrv(peaks, sampling_rate=1000, show=False)
```

**Input:**
- `peaks`: Dictionary with `'ECG_R_Peaks'` key or array of R-peak indices
- `sampling_rate`: Signal sampling rate in Hz

**Returns:**
- DataFrame with HRV indices from all domains:
  - Time domain metrics
  - Frequency domain power spectra
  - Nonlinear complexity measures

**This is a convenience wrapper** that combines:
- `hrv_time()`
- `hrv_frequency()`
- `hrv_nonlinear()`

## Time Domain Analysis

### hrv_time()

Compute time-domain HRV metrics based on inter-beat intervals (IBIs).

```python
hrv_time = nk.hrv_time(peaks, sampling_rate=1000)
```

### Key Metrics

**Basic interval statistics:**
- `HRV_MeanNN`: Mean of NN intervals (ms)
- `HRV_SDNN`: Standard deviation of NN intervals (ms)
  - Reflects total HRV, captures all cyclic components
  - Requires ≥5 min for short-term, ≥24 hr for long-term
- `HRV_RMSSD`: Root mean square of successive differences (ms)
  - High-frequency variability, reflects parasympathetic activity
  - More stable with shorter recordings

**Successive difference measures:**
- `HRV_SDSD`: Standard deviation of successive differences (ms)
  - Similar to RMSSD, correlated with parasympathetic activity
- `HRV_pNN50`: Percentage of successive NN intervals differing >50ms
  - Parasympathetic indicator, may be insensitive in some populations
- `HRV_pNN20`: Percentage of successive NN intervals differing >20ms
  - More sensitive alternative to pNN50

**Range measures:**
- `HRV_MinNN`, `HRV_MaxNN`: Minimum and maximum NN intervals (ms)
- `HRV_CVNN`: Coefficient of variation (SDNN/MeanNN)
  - Normalized measure, useful for cross-subject comparison
- `HRV_CVSD`: Coefficient of variation of successive differences (RMSSD/MeanNN)

**Median-based statistics:**
- `HRV_MedianNN`: Median NN interval (ms)
  - Robust to outliers
- `HRV_MadNN`: Median absolute deviation of NN intervals
  - Robust dispersion measure
- `HRV_MCVNN`: Median-based coefficient of variation

**Advanced time-domain:**
- `HRV_IQRNN`: Interquartile range of NN intervals
- `HRV_pNN10`, `HRV_pNN25`, `HRV_pNN40`: Additional percentile thresholds
- `HRV_TINN`: Triangular interpolation of NN interval histogram
- `HRV_HTI`: HRV triangular index (total NN intervals / histogram height)

### Recording Duration Requirements
- **Ultra-short (< 5 min)**: RMSSD, pNN50 most reliable
- **Short-term (5 min)**: Standard for clinical use, all time-domain valid
- **Long-term (24 hr)**: Required for SDNN interpretation, captures circadian rhythms

## Frequency Domain Analysis

### hrv_frequency()

Analyze HRV power across frequency bands using spectral analysis.

```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, ulf=(0, 0.0033), vlf=(0.0033, 0.04),
                            lf=(0.04, 0.15), hf=(0.15, 0.4), vhf=(0.4, 0.5),
                            psd_method='welch', normalize=True)
```

### Frequency Bands

**Ultra-Low Frequency (ULF): 0-0.0033 Hz**
- Requires ≥24 hour recording
- Circadian rhythms, thermoregulation
- Slow metabolic processes

**Very-Low Frequency (VLF): 0.0033-0.04 Hz**
- Requires ≥5 minute recording
- Thermoregulation, hormonal fluctuations
- Renin-angiotensin system, peripheral vasomotor activity

**Low Frequency (LF): 0.04-0.15 Hz**
- Mixed sympathetic and parasympathetic influences
- Baroreceptor reflex activity
- Blood pressure regulation (10-second rhythm)

**High Frequency (HF): 0.15-0.4 Hz**
- Parasympathetic (vagal) activity
- Respiratory sinus arrhythmia
- Synchronized with breathing (respiratory rate range)

**Very-High Frequency (VHF): 0.4-0.5 Hz**
- Rarely used, may reflect measurement noise
- Requires careful interpretation

### Key Metrics

**Absolute power (ms²):**
- `HRV_ULF`, `HRV_VLF`, `HRV_LF`, `HRV_HF`, `HRV_VHF`: Power in each band
- `HRV_TP`: Total power (variance of NN intervals)
- `HRV_LFHF`: LF/HF ratio (sympathovagal balance)

**Normalized power:**
- `HRV_LFn`: LF power / (LF + HF) - normalized LF
- `HRV_HFn`: HF power / (LF + HF) - normalized HF
- `HRV_LnHF`: Natural logarithm of HF (log-normal distribution)

**Peak frequencies:**
- `HRV_LFpeak`, `HRV_HFpeak`: Frequency of maximum power in each band
- Useful for identifying dominant oscillations

### Power Spectral Density Methods

**Welch's method (default):**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='welch')
```
- Windowed FFT with overlap
- Smoother spectra, reduced variance
- Good for standard HRV analysis

**Lomb-Scargle periodogram:**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='lomb')
```
- Handles unevenly sampled data
- No interpolation required
- Better for noisy or artifact-containing data

**Multitaper method:**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='multitapers')
```
- Superior spectral estimation
- Reduced variance with minimal bias
- Computationally intensive

**Burg autoregressive:**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='burg', order=16)
```
- Parametric method
- Smooth spectra with well-defined peaks
- Requires order selection

### Interpretation Guidelines

**LF/HF Ratio:**
- Traditionally interpreted as sympathovagal balance
- **Caution**: Recent evidence questions this interpretation
- LF reflects both sympathetic and parasympathetic influences
- Context-dependent: controlled respiration affects HF

**HF Power:**
- Reliable parasympathetic indicator
- Increases with: rest, relaxation, deep breathing
- Decreases with: stress, anxiety, sympathetic activation

**Recording Requirements:**
- **Minimum**: 60 seconds for LF/HF estimation
- **Recommended**: 2-5 minutes for short-term HRV
- **Optimal**: 5 minutes per Task Force standards
- **Long-term**: 24 hours for ULF analysis

## Nonlinear Domain Analysis

### hrv_nonlinear()

Compute complexity, entropy, and fractal measures reflecting autonomic dynamics.

```python
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
```

### Poincaré Plot Indices

**Poincaré plot**: NN(i+1) vs NN(i) scatter plot geometry

- `HRV_SD1`: Standard deviation perpendicular to line of identity (ms)
  - Short-term HRV, fast beat-to-beat variability
  - Reflects parasympathetic activity
  - Mathematically related to RMSSD: SD1 ≈ RMSSD/√2

- `HRV_SD2`: Standard deviation along line of identity (ms)
  - Long-term HRV, slow variability
  - Reflects sympathetic and parasympathetic activity
  - Related to SDNN

- `HRV_SD1SD2`: Ratio SD1/SD2
  - Balance between short and long-term variability
  - <1: predominantly long-term variability

- `HRV_SD2SD1`: Ratio SD2/SD1
  - Inverse of SD1SD2

- `HRV_S`: Area of ellipse (π × SD1 × SD2)
  - Total HRV magnitude

- `HRV_CSI`: Cardiac Sympathetic Index (SD2/SD1)
  - Proposed sympathetic indicator

- `HRV_CVI`: Cardiac Vagal Index (log10(SD1 × SD2))
  - Proposed parasympathetic indicator

- `HRV_CSI_Modified`: Modified CSI (SD2²/(SD1 × SD2))

### Heart Rate Asymmetry

Analyzes whether heart rate accelerations and decelerations contribute differently to HRV.

- `HRV_GI`: Guzik's Index - asymmetry of short-term variability
- `HRV_SI`: Slope Index - asymmetry of long-term variability
- `HRV_AI`: Area Index - overall asymmetry
- `HRV_PI`: Porta's Index - percentage of decelerations
- `HRV_C1d`, `HRV_C2d`: Deceleration contributions
- `HRV_C1a`, `HRV_C2a`: Acceleration contributions
- `HRV_SD1d`, `HRV_SD1a`: Poincaré SD1 for decelerations/accelerations
- `HRV_SD2d`, `HRV_SD2a`: Poincaré SD2 for decelerations/accelerations

**Interpretation:**
- Healthy individuals: asymmetry present (more/larger decelerations)
- Clinical populations: reduced asymmetry
- Reflects differential autonomic control of acceleration vs. deceleration

### Entropy Measures

**Approximate Entropy (ApEn):**
- `HRV_ApEn`: Regularity measure, lower = more regular/predictable
- Sensitive to data length, order m, tolerance r

**Sample Entropy (SampEn):**
- `HRV_SampEn`: Improved ApEn, less dependent on data length
- More consistent with short recordings
- Lower values = more regular patterns

**Multiscale Entropy (MSE):**
- `HRV_MSE`: Complexity across multiple time scales
- Distinguishes true complexity from randomness

**Fuzzy Entropy:**
- `HRV_FuzzyEn`: Fuzzy membership functions for pattern matching
- More stable with short data

**Shannon Entropy:**
- `HRV_ShanEn`: Information-theoretic randomness measure

### Fractal Measures

**Detrended Fluctuation Analysis (DFA):**
- `HRV_DFA_alpha1`: Short-term fractal scaling exponent (4-11 beats)
  - α1 > 1: correlations, reduced in heart disease
  - α1 ≈ 1: pink noise, healthy
  - α1 < 0.5: anti-correlations

- `HRV_DFA_alpha2`: Long-term fractal scaling exponent (>11 beats)
  - Reflects long-range correlations

- `HRV_DFA_alpha1alpha2`: Ratio α1/α2

**Correlation Dimension:**
- `HRV_CorDim`: Dimensionality of attractor in phase space
- Indicates system complexity

**Higuchi Fractal Dimension:**
- `HRV_HFD`: Complexity and self-similarity
- Higher values = more complex, irregular

**Petrosian Fractal Dimension:**
- `HRV_PFD`: Alternative complexity measure
- Computationally efficient

**Katz Fractal Dimension:**
- `HRV_KFD`: Waveform complexity

### Heart Rate Fragmentation

Quantifies abnormal short-term fluctuations reflecting autonomic dysregulation.

- `HRV_PIP`: Percentage of inflection points
  - Normal: ~50%, Fragmented: >70%
- `HRV_IALS`: Inverse average length of acceleration/deceleration segments
- `HRV_PSS`: Percentage of short segments (<3 beats)
- `HRV_PAS`: Percentage of NN intervals in alternation segments

**Clinical relevance:**
- Increased fragmentation associated with cardiovascular risk
- Independent predictor beyond traditional HRV metrics

### Other Nonlinear Metrics

- `HRV_Hurst`: Hurst exponent (long-range dependence)
- `HRV_LZC`: Lempel-Ziv complexity (algorithmic complexity)
- `HRV_MFDFA`: Multifractal DFA indices

## Specialized HRV Functions

### hrv_rsa()

Respiratory Sinus Arrhythmia - heart rate modulation by breathing.

```python
rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000, method='porges1980')
```

**Methods:**
- `'porges1980'`: Porges-Bohrer method (band-pass filtered HR around breathing frequency)
- `'harrison2021'`: Peak-to-trough RSA (max-min HR per breath cycle)

**Requirements:**
- Both ECG and respiratory signals
- Synchronized timing
- At least several breath cycles

**Returns:**
- `RSA`: RSA magnitude (beats/min or similar units depending on method)

### hrv_rqa()

Recurrence Quantification Analysis - nonlinear dynamics from phase space reconstruction.

```python
rqa = nk.hrv_rqa(peaks, sampling_rate=1000)
```

**Metrics:**
- `RQA_RR`: Recurrence rate - system predictability
- `RQA_DET`: Determinism - percentage of recurrent points forming lines
- `RQA_LMean`, `RQA_LMax`: Average and maximum diagonal line length
- `RQA_ENTR`: Shannon entropy of line lengths - complexity
- `RQA_LAM`: Laminarity - system trapped in specific states
- `RQA_TT`: Trapping time - duration in laminar states

**Use case:**
- Detect transitions in physiological states
- Assess system determinism vs. stochasticity

## Interval Processing

### intervals_process()

Preprocess RR-intervals before HRV analysis.

```python
processed_intervals = nk.intervals_process(rr_intervals, interpolate=False,
                                           interpolate_sampling_rate=1000)
```

**Operations:**
- Removes physiologically implausible intervals
- Optional: interpolates to regular sampling
- Optional: detrending to remove slow trends

**Use case:**
- When working with pre-extracted RR intervals
- Cleaning intervals from external devices
- Preparing data for frequency-domain analysis

### intervals_to_peaks()

Convert interval data (RR, NN) to peak indices for HRV analysis.

```python
peaks_dict = nk.intervals_to_peaks(rr_intervals, sampling_rate=1000)
```

**Use case:**
- Import data from external HRV devices
- Work with interval data from commercial systems
- Convert between interval and peak representations

## Practical Considerations

### Minimum Recording Duration

| Analysis | Minimum Duration | Optimal Duration |
|----------|-----------------|------------------|
| RMSSD, pNN50 | 30 sec | 5 min |
| SDNN | 5 min | 5 min (short), 24 hr (long) |
| LF, HF power | 2 min | 5 min |
| VLF power | 5 min | 10+ min |
| ULF power | 24 hr | 24 hr |
| Nonlinear (ApEn, SampEn) | 100-300 beats | 500+ beats |
| DFA | 300 beats | 1000+ beats |

### Artifact Management

**Preprocessing:**
```python
# Detect R-peaks with artifact correction
peaks, info = nk.ecg_peaks(cleaned_ecg, sampling_rate=1000, correct_artifacts=True)

# Or manually process intervals
processed = nk.intervals_process(rr_intervals, interpolate=False)
```

**Quality checks:**
- Visual inspection of tachogram (NN intervals over time)
- Identify physiologically implausible intervals (<300 ms or >2000 ms)
- Check for sudden jumps or missing beats
- Assess signal quality before analysis

### Standardization and Comparison

**Task Force Standards (1996):**
- 5-minute recordings for short-term
- Supine, controlled breathing recommended
- 24-hour for long-term assessment

**Normalization:**
- Consider age, sex, fitness level effects
- Time of day and circadian effects
- Body position (supine vs. standing)
- Breathing rate and depth

**Inter-individual variability:**
- HRV has large between-subject variation
- Within-subject changes more interpretable
- Baseline comparisons preferred

## Clinical and Research Applications

**Cardiovascular health:**
- Reduced HRV: risk factor for cardiac events
- SDNN, DFA alpha1: prognostic indicators
- Post-MI monitoring

**Psychological state:**
- Anxiety/stress: reduced HRV (especially RMSSD, HF)
- Depression: altered autonomic balance
- PTSD: fragmentation indices

**Athletic performance:**
- Training load monitoring via daily RMSSD
- Overtraining: reduced HRV
- Recovery assessment

**Neuroscience:**
- Emotion regulation studies
- Cognitive load assessment
- Brain-heart axis research

**Aging:**
- HRV decreases with age
- Complexity measures decline
- Baseline reference needed

## References

- Task Force of the European Society of Cardiology. (1996). Heart rate variability: standards of measurement, physiological interpretation and clinical use. Circulation, 93(5), 1043-1065.
- Shaffer, F., & Ginsberg, J. P. (2017). An overview of heart rate variability metrics and norms. Frontiers in public health, 5, 258.
- Peng, C. K., Havlin, S., Stanley, H. E., & Goldberger, A. L. (1995). Quantification of scaling exponents and crossover phenomena in nonstationary heartbeat time series. Chaos, 5(1), 82-87.
- Guzik, P., Piskorski, J., Krauze, T., Wykretowicz, A., & Wysocki, H. (2006). Heart rate asymmetry by Poincaré plots of RR intervals. Biomedizinische Technik/Biomedical Engineering, 51(4), 272-275.
- Costa, M., Goldberger, A. L., & Peng, C. K. (2005). Multiscale entropy analysis of biological signals. Physical review E, 71(2), 021906.

---

## Reference: Ppg

# Photoplethysmography (PPG) Analysis

## Overview

Photoplethysmography (PPG) measures blood volume changes in microvascular tissue using optical sensors. PPG is widely used in wearable devices, pulse oximeters, and clinical monitors for heart rate, pulse characteristics, and cardiovascular assessment.

## Main Processing Pipeline

### ppg_process()

Automated PPG signal processing pipeline.

```python
signals, info = nk.ppg_process(ppg_signal, sampling_rate=100, method='elgendi')
```

**Pipeline steps:**
1. Signal cleaning (filtering)
2. Systolic peak detection
3. Heart rate calculation
4. Signal quality assessment

**Returns:**
- `signals`: DataFrame with:
  - `PPG_Clean`: Filtered PPG signal
  - `PPG_Peaks`: Systolic peak markers
  - `PPG_Rate`: Instantaneous heart rate (BPM)
  - `PPG_Quality`: Signal quality indicator
- `info`: Dictionary with peak indices and parameters

**Methods:**
- `'elgendi'`: Elgendi et al. (2013) algorithm (default, robust)
- `'nabian2018'`: Nabian et al. (2018) approach

## Preprocessing Functions

### ppg_clean()

Prepare raw PPG signal for peak detection.

```python
cleaned_ppg = nk.ppg_clean(ppg_signal, sampling_rate=100, method='elgendi')
```

**Methods:**

**1. Elgendi (default):**
- Butterworth bandpass filter (0.5-8 Hz)
- Removes baseline drift and high-frequency noise
- Optimized for peak detection reliability

**2. Nabian2018:**
- Alternative filtering approach
- Different frequency characteristics

**PPG signal characteristics:**
- **Systolic peak**: Rapid upstroke, sharp peak (cardiac ejection)
- **Dicrotic notch**: Secondary peak (aortic valve closure)
- **Baseline**: Slow drift due to respiration, movement, perfusion

### ppg_peaks()

Detect systolic peaks in PPG signal.

```python
peaks, info = nk.ppg_peaks(cleaned_ppg, sampling_rate=100, method='elgendi',
                           correct_artifacts=False)
```

**Methods:**
- `'elgendi'`: Two moving averages with dynamic thresholding
- `'bishop'`: Bishop's algorithm
- `'nabian2018'`: Nabian's approach
- `'scipy'`: Simple scipy peak detection

**Artifact correction:**
- Set `correct_artifacts=True` for physiological plausibility checks
- Removes spurious peaks based on inter-beat interval outliers

**Returns:**
- Dictionary with `'PPG_Peaks'` key containing peak indices

**Typical inter-beat intervals:**
- Resting adult: 600-1200 ms (50-100 BPM)
- Athlete: Can be longer (bradycardia)
- Stressed/exercising: Shorter (<600 ms, >100 BPM)

### ppg_findpeaks()

Low-level peak detection with algorithm comparison.

```python
peaks_dict = nk.ppg_findpeaks(cleaned_ppg, sampling_rate=100, method='elgendi')
```

**Use case:**
- Custom parameter tuning
- Algorithm testing
- Research method development

## Analysis Functions

### ppg_analyze()

Automatically select event-related or interval-related analysis.

```python
analysis = nk.ppg_analyze(signals, sampling_rate=100)
```

**Mode selection:**
- Duration < 10 seconds → event-related
- Duration ≥ 10 seconds → interval-related

### ppg_eventrelated()

Analyze PPG responses to discrete events/stimuli.

```python
results = nk.ppg_eventrelated(epochs)
```

**Computed metrics (per epoch):**
- `PPG_Rate_Baseline`: Heart rate before event
- `PPG_Rate_Min/Max`: Minimum/maximum heart rate during epoch
- Rate dynamics across epoch time windows

**Use cases:**
- Cardiovascular responses to emotional stimuli
- Cognitive load assessment
- Stress reactivity paradigms

### ppg_intervalrelated()

Analyze extended PPG recordings.

```python
results = nk.ppg_intervalrelated(signals, sampling_rate=100)
```

**Computed metrics:**
- `PPG_Rate_Mean`: Average heart rate
- Heart rate variability (HRV) metrics
  - Delegates to `hrv()` function
  - Time, frequency, and nonlinear domains

**Recording duration:**
- Minimum: 60 seconds for basic rate
- HRV analysis: 2-5 minutes recommended

**Use cases:**
- Resting state cardiovascular assessment
- Wearable device data analysis
- Long-term heart rate monitoring

## Quality Assessment

### ppg_quality()

Assess signal quality and reliability.

```python
quality = nk.ppg_quality(ppg_signal, sampling_rate=100, method='averageQRS')
```

**Methods:**

**1. averageQRS (default):**
- Template matching approach
- Correlates each pulse with average template
- Returns quality scores 0-1 per beat
- Threshold: >0.6 = acceptable quality

**2. dissimilarity:**
- Topographic dissimilarity measures
- Detects morphological changes

**Use cases:**
- Identify corrupted segments
- Filter low-quality data before analysis
- Validate peak detection accuracy

**Common quality issues:**
- Motion artifacts: abrupt signal changes
- Poor sensor contact: low amplitude, noise
- Vasoconstriction: reduced signal amplitude (cold, stress)

## Utility Functions

### ppg_segment()

Extract individual pulses for morphological analysis.

```python
pulses = nk.ppg_segment(cleaned_ppg, peaks, sampling_rate=100)
```

**Returns:**
- Dictionary of pulse epochs, each centered on systolic peak
- Enables pulse-to-pulse comparison
- Morphology analysis across conditions

**Use cases:**
- Pulse wave analysis
- Arterial stiffness proxies
- Vascular aging assessment

### ppg_methods()

Document preprocessing methods used in analysis.

```python
methods_info = nk.ppg_methods(method='elgendi')
```

**Returns:**
- String documenting the processing pipeline
- Useful for methods sections in publications

## Simulation and Visualization

### ppg_simulate()

Generate synthetic PPG signals for testing.

```python
synthetic_ppg = nk.ppg_simulate(duration=60, sampling_rate=100, heart_rate=70,
                                noise=0.1, random_state=42)
```

**Parameters:**
- `heart_rate`: Mean BPM (default: 70)
- `heart_rate_std`: HRV magnitude
- `noise`: Gaussian noise level
- `random_state`: Reproducibility seed

**Use cases:**
- Algorithm validation
- Parameter optimization
- Educational demonstrations

### ppg_plot()

Visualize processed PPG signal.

```python
nk.ppg_plot(signals, info, static=True)
```

**Displays:**
- Raw and cleaned PPG signal
- Detected systolic peaks
- Instantaneous heart rate trace
- Signal quality indicators

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 20 Hz (basic heart rate)
- **Standard**: 50-100 Hz (most wearables)
- **High-resolution**: 200-500 Hz (research, pulse wave analysis)
- **Excessive**: >1000 Hz (unnecessary for PPG)

### Recording Duration
- **Heart rate**: ≥10 seconds (few beats)
- **HRV analysis**: 2-5 minutes minimum
- **Long-term monitoring**: Hours to days (wearables)

### Sensor Placement

**Common sites:**
- **Fingertip**: Highest signal quality, most common
- **Earlobe**: Less motion artifact, clinical use
- **Wrist**: Wearable devices (smartwatches)
- **Forehead**: Reflectance mode, medical monitoring

**Transmittance vs. Reflectance:**
- **Transmittance**: Light passes through tissue (fingertip, earlobe)
  - Higher signal quality
  - Less motion artifact
- **Reflectance**: Light reflected from tissue (wrist, forehead)
  - More susceptible to noise
  - Convenient for wearables

### Common Issues and Solutions

**Low signal amplitude:**
- Poor perfusion: warm hands, increase blood flow
- Sensor contact: adjust placement, clean skin
- Vasoconstriction: environmental temperature, stress

**Motion artifacts:**
- Dominant issue in wearables
- Adaptive filtering, accelerometer-based correction
- Template matching, outlier rejection

**Baseline drift:**
- Respiratory modulation (normal)
- Movement or pressure changes
- High-pass filtering or detrending

**Missing peaks:**
- Low-quality signal: check sensor contact
- Algorithm parameters: adjust threshold
- Try alternative detection methods

### Best Practices

**Standard workflow:**
```python
# 1. Clean signal
cleaned = nk.ppg_clean(ppg_raw, sampling_rate=100, method='elgendi')

# 2. Detect peaks with artifact correction
peaks, info = nk.ppg_peaks(cleaned, sampling_rate=100, correct_artifacts=True)

# 3. Assess quality
quality = nk.ppg_quality(cleaned, sampling_rate=100)

# 4. Comprehensive processing (alternative)
signals, info = nk.ppg_process(ppg_raw, sampling_rate=100)

# 5. Analyze
analysis = nk.ppg_analyze(signals, sampling_rate=100)
```

**HRV from PPG:**
```python
# Process PPG signal
signals, info = nk.ppg_process(ppg_raw, sampling_rate=100)

# Extract peaks and compute HRV
hrv_indices = nk.hrv(info['PPG_Peaks'], sampling_rate=100)

# PPG-derived HRV is valid but may differ slightly from ECG-derived HRV
# Differences due to pulse arrival time, vascular properties
```

## Clinical and Research Applications

**Wearable health monitoring:**
- Consumer smartwatches and fitness trackers
- Continuous heart rate monitoring
- Sleep tracking and activity assessment

**Clinical monitoring:**
- Pulse oximetry (SpO₂ + heart rate)
- Perioperative monitoring
- Critical care heart rate assessment

**Cardiovascular assessment:**
- Pulse wave analysis
- Arterial stiffness proxies (pulse arrival time)
- Vascular aging indices

**Autonomic function:**
- HRV from PPG (PPG-HRV)
- Stress and recovery monitoring
- Mental workload assessment

**Remote patient monitoring:**
- Telemedicine applications
- Home-based health tracking
- Chronic disease management

**Affective computing:**
- Emotion recognition from physiological signals
- User experience research
- Human-computer interaction

## PPG vs. ECG

**Advantages of PPG:**
- Non-invasive, no electrodes
- Convenient for long-term monitoring
- Low cost, miniaturizable
- Suitable for wearables

**Disadvantages of PPG:**
- More susceptible to motion artifacts
- Lower signal quality in poor perfusion
- Pulse arrival time delay from heart
- Cannot assess cardiac electrical activity

**HRV comparison:**
- PPG-HRV generally valid for time/frequency domains
- May differ slightly due to pulse transit time variability
- ECG preferred for clinical HRV when available
- PPG acceptable for research and consumer applications

## Interpretation Guidelines

**Heart rate from PPG:**
- Same interpretation as ECG-derived heart rate
- Slight delay (pulse arrival time) is negligible for rate calculation
- Motion artifacts more common: validate with signal quality

**Pulse amplitude:**
- Reflects peripheral perfusion
- Increases: vasodilation, warmth
- Decreases: vasoconstriction, cold, stress, poor contact

**Pulse morphology:**
- Systolic peak: Cardiac ejection
- Dicrotic notch: Aortic valve closure, arterial compliance
- Aging/stiffness: Earlier, more prominent dicrotic notch

## References

- Elgendi, M. (2012). On the analysis of fingertip photoplethysmogram signals. Current cardiology reviews, 8(1), 14-25.
- Elgendi, M., Norton, I., Brearley, M., Abbott, D., & Schuurmans, D. (2013). Systolic peak detection in acceleration photoplethysmograms measured from emergency responders in tropical conditions. PloS one, 8(10), e76585.
- Allen, J. (2007). Photoplethysmography and its application in clinical physiological measurement. Physiological measurement, 28(3), R1.
- Tamura, T., Maeda, Y., Sekine, M., & Yoshida, M. (2014). Wearable photoplethysmographic sensors—past and present. Electronics, 3(2), 282-302.

---

## Reference: Rsp

# Respiratory Signal Processing

## Overview

Respiratory signal processing in NeuroKit2 enables analysis of breathing patterns, respiratory rate, amplitude, and variability. Respiration is closely linked to cardiac activity (respiratory sinus arrhythmia), emotional state, and cognitive processes.

## Main Processing Pipeline

### rsp_process()

Automated processing of respiratory signals with peak/trough detection and feature extraction.

```python
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100, method='khodadad2018')
```

**Pipeline steps:**
1. Signal cleaning (noise removal, filtering)
2. Peak (exhalation) and trough (inhalation) detection
3. Respiratory rate calculation
4. Amplitude computation
5. Phase determination (inspiration/expiration)
6. Respiratory volume per time (RVT)

**Returns:**
- `signals`: DataFrame with:
  - `RSP_Clean`: Filtered respiratory signal
  - `RSP_Peaks`, `RSP_Troughs`: Extrema markers
  - `RSP_Rate`: Instantaneous breathing rate (breaths/min)
  - `RSP_Amplitude`: Breath-to-breath amplitude
  - `RSP_Phase`: Inspiration (0) vs. expiration (1)
  - `RSP_Phase_Completion`: Phase completion percentage (0-1)
  - `RSP_RVT`: Respiratory volume per time
- `info`: Dictionary with peak/trough indices

**Methods:**
- `'khodadad2018'`: Khodadad et al. algorithm (default, robust)
- `'biosppy'`: BioSPPy-based processing (alternative)

## Preprocessing Functions

### rsp_clean()

Remove noise and smooth respiratory signal.

```python
cleaned_rsp = nk.rsp_clean(rsp_signal, sampling_rate=100, method='khodadad2018')
```

**Methods:**

**1. Khodadad2018 (default):**
- Butterworth low-pass filter
- Removes high-frequency noise
- Preserves breathing waveform

**2. BioSPPy:**
- Alternative filtering approach
- Similar performance to Khodadad

**3. Hampel filter:**
```python
cleaned_rsp = nk.rsp_clean(rsp_signal, sampling_rate=100, method='hampel')
```
- Median-based outlier removal
- Robust to artifacts and spikes
- Preserves sharp transitions

**Typical respiratory frequency:**
- Adults at rest: 12-20 breaths/min (0.2-0.33 Hz)
- Children: faster rates
- During exercise: up to 40-60 breaths/min

### rsp_peaks()

Identify inhalation troughs and exhalation peaks in respiratory signal.

```python
peaks, info = nk.rsp_peaks(cleaned_rsp, sampling_rate=100, method='khodadad2018')
```

**Detection methods:**
- `'khodadad2018'`: Optimized for clean signals
- `'biosppy'`: Alternative approach
- `'scipy'`: Simple scipy-based detection

**Returns:**
- Dictionary with:
  - `RSP_Peaks`: Indices of exhalation peaks (maximum points)
  - `RSP_Troughs`: Indices of inhalation troughs (minimum points)

**Respiratory cycle definition:**
- **Inhalation**: Trough → Peak (air flows in, chest/abdomen expands)
- **Exhalation**: Peak → Trough (air flows out, chest/abdomen contracts)

### rsp_findpeaks()

Low-level peak detection with multiple algorithm options.

```python
peaks_dict = nk.rsp_findpeaks(cleaned_rsp, sampling_rate=100, method='scipy')
```

**Methods:**
- `'scipy'`: Scipy's find_peaks
- Custom threshold-based algorithms

**Use case:**
- Fine-tuned peak detection
- Custom parameter adjustment
- Algorithm comparison

### rsp_fixpeaks()

Correct detected peak/trough anomalies (e.g., missed or false detections).

```python
corrected_peaks = nk.rsp_fixpeaks(peaks, sampling_rate=100)
```

**Corrections:**
- Remove physiologically implausible intervals
- Interpolate missing peaks
- Remove artifact-related false peaks

## Feature Extraction Functions

### rsp_rate()

Compute instantaneous breathing rate (breaths per minute).

```python
rate = nk.rsp_rate(peaks, sampling_rate=100, desired_length=None)
```

**Method:**
- Calculate inter-breath intervals from peak/trough timing
- Convert to breaths per minute (BPM)
- Interpolate to match signal length

**Typical values:**
- Resting adult: 12-20 BPM
- Slow breathing: <10 BPM (meditation, relaxation)
- Fast breathing: >25 BPM (exercise, anxiety)

### rsp_amplitude()

Compute breath-to-breath amplitude (peak-to-trough difference).

```python
amplitude = nk.rsp_amplitude(cleaned_rsp, peaks)
```

**Interpretation:**
- Larger amplitude: deeper breaths (tidal volume increase)
- Smaller amplitude: shallow breaths
- Variable amplitude: irregular breathing pattern

**Clinical relevance:**
- Reduced amplitude: restrictive lung disease, chest wall rigidity
- Increased amplitude: compensatory hyperventilation

### rsp_phase()

Determine inspiration/expiration phases and completion percentage.

```python
phase, completion = nk.rsp_phase(cleaned_rsp, peaks, sampling_rate=100)
```

**Returns:**
- `RSP_Phase`: Binary (0 = inspiration, 1 = expiration)
- `RSP_Phase_Completion`: Continuous 0-1 indicating phase progress

**Use cases:**
- Respiratory-gated stimulus presentation
- Phase-locked averaging
- Respiratory-cardiac coupling analysis

### rsp_symmetry()

Analyze breath symmetry patterns (peak-trough balance, rise-decay timing).

```python
symmetry = nk.rsp_symmetry(cleaned_rsp, peaks)
```

**Metrics:**
- Peak-trough symmetry: Are peaks and troughs equally spaced?
- Rise-decay symmetry: Is inhalation time equal to exhalation time?

**Interpretation:**
- Symmetric: normal, relaxed breathing
- Asymmetric: effortful breathing, airway obstruction

## Advanced Analysis Functions

### rsp_rrv()

Respiratory Rate Variability - analogous to heart rate variability.

```python
rrv_indices = nk.rsp_rrv(peaks, sampling_rate=100)
```

**Time-domain metrics:**
- `RRV_SDBB`: Standard deviation of breath-to-breath intervals
- `RRV_RMSSD`: Root mean square of successive differences
- `RRV_MeanBB`: Mean breath-to-breath interval

**Frequency-domain metrics:**
- Power in frequency bands (if applicable)

**Interpretation:**
- Higher RRV: flexible, adaptive breathing control
- Lower RRV: rigid, constrained breathing
- Altered RRV: anxiety, respiratory disorders, autonomic dysfunction

**Recording duration:**
- Minimum: 2-3 minutes
- Optimal: 5-10 minutes for stable estimates

### rsp_rvt()

Respiratory Volume per Time - fMRI confound regressor.

```python
rvt = nk.rsp_rvt(cleaned_rsp, peaks, sampling_rate=100)
```

**Calculation:**
- Derivative of respiratory signal
- Captures rate of volume change
- Correlates with BOLD signal fluctuations

**Use cases:**
- fMRI artifact correction
- Neuroimaging preprocessing
- Respiratory confound regression

**Reference:**
- Birn, R. M., et al. (2008). Separating respiratory-variation-related fluctuations from neuronal-activity-related fluctuations in fMRI. NeuroImage, 31(4), 1536-1548.

### rsp_rav()

Respiratory Amplitude Variability indices.

```python
rav = nk.rsp_rav(amplitude, sampling_rate=100)
```

**Metrics:**
- Standard deviation of amplitudes
- Coefficient of variation
- Range of amplitudes

**Interpretation:**
- High RAV: irregular depth (sighing, arousal changes)
- Low RAV: stable, controlled breathing

## Analysis Functions

### rsp_analyze()

Automatically select event-related or interval-related analysis.

```python
analysis = nk.rsp_analyze(signals, sampling_rate=100)
```

**Mode selection:**
- Duration < 10 seconds → event-related
- Duration ≥ 10 seconds → interval-related

### rsp_eventrelated()

Analyze respiratory responses to specific events/stimuli.

```python
results = nk.rsp_eventrelated(epochs)
```

**Computed metrics (per epoch):**
- `RSP_Rate_Mean`: Average breathing rate during epoch
- `RSP_Rate_Min/Max`: Minimum/maximum rate
- `RSP_Amplitude_Mean`: Average breath depth
- `RSP_Phase`: Respiratory phase at event onset
- Dynamics of rate and amplitude across epoch

**Use cases:**
- Respiratory changes during emotional stimuli
- Anticipatory breathing before task events
- Breath-holding or hyperventilation paradigms

### rsp_intervalrelated()

Analyze extended respiratory recordings.

```python
results = nk.rsp_intervalrelated(signals, sampling_rate=100)
```

**Computed metrics:**
- `RSP_Rate_Mean`: Average breathing rate
- `RSP_Rate_SD`: Variability in rate
- `RSP_Amplitude_Mean`: Average breath depth
- RRV indices (if sufficient data)
- RAV indices

**Recording duration:**
- Minimum: 60 seconds
- Optimal: 5-10 minutes

**Use cases:**
- Resting state breathing patterns
- Baseline respiratory assessment
- Stress or relaxation monitoring

## Simulation and Visualization

### rsp_simulate()

Generate synthetic respiratory signals for testing.

```python
synthetic_rsp = nk.rsp_simulate(duration=60, sampling_rate=100, respiratory_rate=15,
                                method='sinusoidal', noise=0.1, random_state=42)
```

**Methods:**
- `'sinusoidal'`: Simple sinusoidal oscillation (fast)
- `'breathmetrics'`: Advanced realistic breathing model (slower, more accurate)

**Parameters:**
- `respiratory_rate`: Breaths per minute (default: 15)
- `noise`: Gaussian noise level
- `random_state`: Seed for reproducibility

**Use cases:**
- Algorithm validation
- Parameter tuning
- Educational demonstrations

### rsp_plot()

Visualize processed respiratory signal.

```python
nk.rsp_plot(signals, info, static=True)
```

**Displays:**
- Raw and cleaned respiratory signal
- Detected peaks and troughs
- Instantaneous breathing rate
- Phase markers

**Interactive mode:** Set `static=False` for Plotly visualization

## Practical Considerations

### Sampling Rate Recommendations
- **Minimum**: 10 Hz (adequate for rate estimation)
- **Standard**: 50-100 Hz (research-grade)
- **High-resolution**: 1000 Hz (typically unnecessary, oversampled)

### Recording Duration
- **Rate estimation**: ≥10 seconds (few breaths)
- **RRV analysis**: ≥2-3 minutes
- **Resting state**: 5-10 minutes
- **Circadian patterns**: Hours to days

### Signal Acquisition Methods

**Strain gauge/piezoelectric belt:**
- Chest or abdominal expansion
- Most common
- Comfortable, non-invasive

**Thermistor/thermocouple:**
- Nasal/oral airflow temperature
- Direct airflow measurement
- Can be intrusive

**Capnography:**
- End-tidal CO₂ measurement
- Gold standard for physiology
- Expensive, clinical settings

**Impedance pneumography:**
- Derived from ECG electrodes
- Convenient for multi-modal recording
- Less accurate than dedicated sensors

### Common Issues and Solutions

**Irregular breathing:**
- Normal in awake, resting humans
- Sighs, yawns, speech, swallowing cause variability
- Exclude artifacts or model as events

**Shallow breathing:**
- Low signal amplitude
- Check sensor placement and tightness
- Increase gain if available

**Movement artifacts:**
- Spikes or discontinuities
- Minimize participant movement
- Use robust peak detection (Hampel filter)

**Talking/coughing:**
- Disrupts natural breathing pattern
- Annotate and exclude from analysis
- Or model as separate event types

### Best Practices

**Standard workflow:**
```python
# 1. Clean signal
cleaned = nk.rsp_clean(rsp_raw, sampling_rate=100, method='khodadad2018')

# 2. Detect peaks/troughs
peaks, info = nk.rsp_peaks(cleaned, sampling_rate=100)

# 3. Extract features
rate = nk.rsp_rate(peaks, sampling_rate=100, desired_length=len(cleaned))
amplitude = nk.rsp_amplitude(cleaned, peaks)
phase = nk.rsp_phase(cleaned, peaks, sampling_rate=100)

# 4. Comprehensive processing (alternative)
signals, info = nk.rsp_process(rsp_raw, sampling_rate=100)

# 5. Analyze
analysis = nk.rsp_analyze(signals, sampling_rate=100)
```

**Respiratory-cardiac integration:**
```python
# Process both signals
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=100)

# Respiratory sinus arrhythmia (RSA)
rsa = nk.hrv_rsa(ecg_info['ECG_R_Peaks'], rsp_signals['RSP_Clean'], sampling_rate=1000)

# Or use bio_process for multi-signal integration
bio_signals, bio_info = nk.bio_process(ecg=ecg, rsp=rsp, sampling_rate=1000)
```

## Clinical and Research Applications

**Psychophysiology:**
- Emotion and arousal (rapid, shallow breathing during stress)
- Relaxation interventions (slow, deep breathing)
- Respiratory biofeedback

**Anxiety and panic disorders:**
- Hyperventilation during panic attacks
- Altered breathing patterns
- Breathing retraining therapy effectiveness

**Sleep medicine:**
- Sleep apnea detection
- Breathing pattern abnormalities
- Sleep stage correlates

**Cardiorespiratory coupling:**
- Respiratory sinus arrhythmia (HRV modulation by breathing)
- Heart-lung interaction
- Autonomic nervous system assessment

**Neuroimaging:**
- fMRI artifact correction (RVT regressor)
- BOLD signal confound removal
- Respiratory-related brain activity

**Meditation and mindfulness:**
- Breath awareness training
- Slow breathing practices (resonance frequency ~6 breaths/min)
- Physiological markers of relaxation

**Athletic performance:**
- Breathing efficiency
- Training adaptations
- Recovery monitoring

## Interpretation Guidelines

**Breathing rate:**
- **Normal**: 12-20 BPM (adults at rest)
- **Slow**: <10 BPM (relaxation, meditation, sleep)
- **Fast**: >25 BPM (exercise, anxiety, pain, fever)

**Breathing amplitude:**
- Tidal volume typically 400-600 mL at rest
- Deep breathing: 2-3 L
- Shallow breathing: <300 mL

**Respiratory patterns:**
- **Normal**: Smooth, regular sinusoidal
- **Cheyne-Stokes**: Crescendo-decrescendo with apneas (clinical pathology)
- **Ataxic**: Completely irregular (brainstem lesion)

## References

- Khodadad, D., Nordebo, S., Müller, B., Waldmann, A., Yerworth, R., Becher, T., ... & Bayford, R. (2018). A review of tissue substitutes for ultrasound imaging. Ultrasound in medicine & biology, 44(9), 1807-1823.
- Grossman, P., & Taylor, E. W. (2007). Toward understanding respiratory sinus arrhythmia: Relations to cardiac vagal tone, evolution and biobehavioral functions. Biological psychology, 74(2), 263-285.
- Birn, R. M., Diamond, J. B., Smith, M. A., & Bandettini, P. A. (2006). Separating respiratory-variation-related fluctuations from neuronal-activity-related fluctuations in fMRI. NeuroImage, 31(4), 1536-1548.

---

## Reference: Signal_Processing

# General Signal Processing

## Overview

NeuroKit2 provides comprehensive signal processing utilities applicable to any time series data. These functions support filtering, transformation, peak detection, decomposition, and analysis operations that work across all signal types.

## Preprocessing Functions

### signal_filter()

Apply frequency-domain filtering to remove noise or isolate frequency bands.

```python
filtered = nk.signal_filter(signal, sampling_rate=1000, lowcut=None, highcut=None,
                            method='butterworth', order=5)
```

**Filter types (via lowcut/highcut combinations):**

**Lowpass** (highcut only):
```python
lowpass = nk.signal_filter(signal, sampling_rate=1000, highcut=50)
```
- Removes frequencies above highcut
- Smooths signal, removes high-frequency noise

**Highpass** (lowcut only):
```python
highpass = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5)
```
- Removes frequencies below lowcut
- Removes baseline drift, DC offset

**Bandpass** (both lowcut and highcut):
```python
bandpass = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=50)
```
- Retains frequencies between lowcut and highcut
- Isolates specific frequency band

**Bandstop/Notch** (powerline removal):
```python
notch = nk.signal_filter(signal, sampling_rate=1000, method='powerline', powerline=50)
```
- Removes 50 or 60 Hz powerline noise
- Narrow notch filter

**Methods:**
- `'butterworth'` (default): Smooth frequency response, flat passband
- `'bessel'`: Linear phase, minimal ringing
- `'chebyshev1'`: Steeper rolloff, ripple in passband
- `'chebyshev2'`: Steeper rolloff, ripple in stopband
- `'elliptic'`: Steepest rolloff, ripple in both bands
- `'powerline'`: Notch filter for 50/60 Hz

**Order parameter:**
- Higher order: Steeper transition, more ringing
- Lower order: Gentler transition, less ringing
- Typical: 2-5 for physiological signals

### signal_sanitize()

Remove invalid values (NaN, inf) and optionally interpolate.

```python
clean_signal = nk.signal_sanitize(signal, interpolate=True)
```

**Use cases:**
- Handle missing data points
- Remove artifacts marked as NaN
- Prepare signal for algorithms requiring continuous data

### signal_resample()

Change sampling rate of signal (upsample or downsample).

```python
resampled = nk.signal_resample(signal, sampling_rate=1000, desired_sampling_rate=500,
                               method='interpolation')
```

**Methods:**
- `'interpolation'`: Cubic spline interpolation
- `'FFT'`: Frequency-domain resampling
- `'poly'`: Polyphase filtering (best for downsampling)

**Use cases:**
- Match sampling rates across multi-modal recordings
- Reduce data size (downsample)
- Increase temporal resolution (upsample)

### signal_fillmissing()

Interpolate missing or invalid data points.

```python
filled = nk.signal_fillmissing(signal, method='linear')
```

**Methods:**
- `'linear'`: Linear interpolation
- `'nearest'`: Nearest neighbor
- `'pad'`: Forward/backward fill
- `'cubic'`: Cubic spline
- `'polynomial'`: Polynomial fitting

## Transformation Functions

### signal_detrend()

Remove slow trends from signal.

```python
detrended = nk.signal_detrend(signal, method='polynomial', order=1)
```

**Methods:**
- `'polynomial'`: Fit and subtract polynomial (order 1 = linear)
- `'loess'`: Locally weighted regression
- `'tarvainen2002'`: Smoothness priors detrending

**Use cases:**
- Remove baseline drift
- Stabilize mean before analysis
- Prepare for stationarity-assuming algorithms

### signal_decompose()

Decompose signal into constituent components.

```python
components = nk.signal_decompose(signal, sampling_rate=1000, method='emd')
```

**Methods:**

**Empirical Mode Decomposition (EMD):**
```python
components = nk.signal_decompose(signal, sampling_rate=1000, method='emd')
```
- Data-adaptive decomposition into Intrinsic Mode Functions (IMFs)
- Each IMF represents different frequency content (high to low)
- No predefined basis functions

**Singular Spectrum Analysis (SSA):**
```python
components = nk.signal_decompose(signal, method='ssa')
```
- Decomposes into trend, oscillations, and noise
- Based on eigenvalue decomposition of trajectory matrix

**Wavelet decomposition:**
- Time-frequency representation
- Localized in both time and frequency

**Returns:**
- Dictionary with component signals
- Trend, oscillatory components, residual

**Use cases:**
- Isolate physiological rhythms
- Separate signal from noise
- Multi-scale analysis

### signal_recompose()

Reconstruct signal from decomposed components.

```python
reconstructed = nk.signal_recompose(components, indices=[1, 2, 3])
```

**Use case:**
- Selective reconstruction after decomposition
- Remove specific IMFs or components
- Adaptive filtering

### signal_binarize()

Convert continuous signal to binary (0/1) based on threshold.

```python
binary = nk.signal_binarize(signal, method='threshold', threshold=0.5)
```

**Methods:**
- `'threshold'`: Simple threshold
- `'median'`: Median-based
- `'mean'`: Mean-based
- `'quantile'`: Percentile-based

**Use case:**
- Event detection from continuous signal
- Trigger extraction
- State classification

### signal_distort()

Add controlled noise or artifacts for testing.

```python
distorted = nk.signal_distort(signal, sampling_rate=1000, noise_amplitude=0.1,
                              noise_frequency=50, artifacts_amplitude=0.5)
```

**Parameters:**
- `noise_amplitude`: Gaussian noise level
- `noise_frequency`: Sinusoidal interference (e.g., powerline)
- `artifacts_amplitude`: Random spike artifacts
- `artifacts_number`: Number of artifacts to add

**Use cases:**
- Algorithm robustness testing
- Preprocessing method evaluation
- Realistic data simulation

### signal_interpolate()

Interpolate signal at new time points or fill gaps.

```python
interpolated = nk.signal_interpolate(x_values, y_values, x_new=None, method='quadratic')
```

**Methods:**
- `'linear'`, `'quadratic'`, `'cubic'`: Polynomial interpolation
- `'nearest'`: Nearest neighbor
- `'monotone_cubic'`: Preserves monotonicity

**Use case:**
- Convert irregular samples to regular grid
- Upsample for visualization
- Align signals with different time bases

### signal_merge()

Combine multiple signals with different sampling rates.

```python
merged = nk.signal_merge(signal1, signal2, time1=None, time2=None, sampling_rate=None)
```

**Use case:**
- Multi-modal signal integration
- Combine data from different devices
- Synchronize based on timestamps

### signal_flatline()

Identify periods of constant signal (artifacts or sensor failure).

```python
flatline_mask = nk.signal_flatline(signal, duration=5.0, sampling_rate=1000)
```

**Returns:**
- Binary mask where True indicates flatline periods
- Duration threshold prevents false positives from normal stability

### signal_noise()

Add various types of noise to signal.

```python
noisy = nk.signal_noise(signal, sampling_rate=1000, noise_type='gaussian',
                        amplitude=0.1)
```

**Noise types:**
- `'gaussian'`: White noise
- `'pink'`: 1/f noise (common in physiological signals)
- `'brown'`: Brownian (random walk)
- `'powerline'`: Sinusoidal interference (50/60 Hz)

### signal_surrogate()

Generate surrogate signals preserving certain properties.

```python
surrogate = nk.signal_surrogate(signal, method='IAAFT')
```

**Methods:**
- `'IAAFT'`: Iterated Amplitude Adjusted Fourier Transform
  - Preserves amplitude distribution and power spectrum
- `'random_shuffle'`: Random permutation (null hypothesis testing)

**Use case:**
- Nonlinearity testing
- Null hypothesis generation for statistical tests

## Peak Detection and Correction

### signal_findpeaks()

Detect local maxima (peaks) in signal.

```python
peaks_dict = nk.signal_findpeaks(signal, height_min=None, height_max=None,
                                 relative_height_min=None, relative_height_max=None)
```

**Key parameters:**
- `height_min/max`: Absolute amplitude thresholds
- `relative_height_min/max`: Relative to signal range (0-1)
- `threshold`: Minimum prominence
- `distance`: Minimum samples between peaks

**Returns:**
- Dictionary with:
  - `'Peaks'`: Peak indices
  - `'Height'`: Peak amplitudes
  - `'Distance'`: Inter-peak intervals

**Use cases:**
- Generic peak detection for any signal
- R-peaks, respiratory peaks, pulse peaks
- Event detection

### signal_fixpeaks()

Correct detected peaks for artifacts and anomalies.

```python
corrected = nk.signal_fixpeaks(peaks, sampling_rate=1000, iterative=True,
                               method='Kubios', interval_min=None, interval_max=None)
```

**Methods:**
- `'Kubios'`: Kubios HRV software method (default)
- `'Malik1996'`: Task Force Standards (1996)
- `'Kamath1993'`: Kamath's approach

**Corrections:**
- Remove physiologically implausible intervals
- Interpolate missing peaks
- Remove extra detected peaks (duplicates)

**Use case:**
- Artifact correction in R-R intervals
- Improve HRV analysis quality
- Respiratory or pulse peak correction

## Analysis Functions

### signal_rate()

Compute instantaneous rate from event occurrences (peaks).

```python
rate = nk.signal_rate(peaks, sampling_rate=1000, desired_length=None)
```

**Method:**
- Calculate inter-event intervals
- Convert to events per minute
- Interpolate to match desired length

**Use case:**
- Heart rate from R-peaks
- Breathing rate from respiratory peaks
- Any periodic event rate

### signal_period()

Find dominant period/frequency in signal.

```python
period = nk.signal_period(signal, sampling_rate=1000, method='autocorrelation',
                          show=False)
```

**Methods:**
- `'autocorrelation'`: Peak in autocorrelation function
- `'powerspectraldensity'`: Peak in frequency spectrum

**Returns:**
- Period in samples or seconds
- Frequency (1/period) in Hz

**Use case:**
- Detect dominant rhythm
- Estimate fundamental frequency
- Breathing rate, heart rate estimation

### signal_phase()

Compute instantaneous phase of signal.

```python
phase = nk.signal_phase(signal, method='hilbert')
```

**Methods:**
- `'hilbert'`: Hilbert transform (analytic signal)
- `'wavelet'`: Wavelet-based phase

**Returns:**
- Phase in radians (-π to π) or 0 to 1 (normalized)

**Use cases:**
- Phase-locked analysis
- Synchronization measures
- Phase-amplitude coupling

### signal_psd()

Compute Power Spectral Density.

```python
psd, freqs = nk.signal_psd(signal, sampling_rate=1000, method='welch',
                           max_frequency=None, show=False)
```

**Methods:**
- `'welch'`: Welch's periodogram (windowed FFT, default)
- `'multitapers'`: Multitaper method (superior spectral estimation)
- `'lomb'`: Lomb-Scargle (unevenly sampled data)
- `'burg'`: Autoregressive (parametric)

**Returns:**
- `psd`: Power at each frequency (units²/Hz)
- `freqs`: Frequency bins (Hz)

**Use case:**
- Frequency content analysis
- HRV frequency domain
- Spectral signatures

### signal_power()

Compute power in specific frequency bands.

```python
power_dict = nk.signal_power(signal, sampling_rate=1000, frequency_bands={
    'VLF': (0.003, 0.04),
    'LF': (0.04, 0.15),
    'HF': (0.15, 0.4)
}, method='welch')
```

**Returns:**
- Dictionary with absolute and relative power per band
- Peak frequencies

**Use case:**
- HRV frequency analysis
- EEG band power
- Rhythm quantification

### signal_autocor()

Compute autocorrelation function.

```python
autocorr = nk.signal_autocor(signal, lag=1000, show=False)
```

**Interpretation:**
- High autocorrelation at lag: signal repeats every lag samples
- Periodic signals: peaks at multiples of period
- Random signals: rapid decay to zero

**Use cases:**
- Detect periodicity
- Assess temporal structure
- Memory in signal

### signal_zerocrossings()

Count zero crossings (sign changes).

```python
n_crossings = nk.signal_zerocrossings(signal)
```

**Interpretation:**
- More crossings: higher frequency content
- Related to dominant frequency (rough estimate)

**Use case:**
- Simple frequency estimation
- Signal regularity assessment

### signal_changepoints()

Detect abrupt changes in signal properties (mean, variance).

```python
changepoints = nk.signal_changepoints(signal, penalty=10, method='pelt', show=False)
```

**Methods:**
- `'pelt'`: Pruned Exact Linear Time (fast, exact)
- `'binseg'`: Binary segmentation (faster, approximate)

**Parameters:**
- `penalty`: Controls sensitivity (higher = fewer changepoints)

**Returns:**
- Indices of detected changepoints
- Segments between changepoints

**Use cases:**
- Segment signal into states
- Detect transitions (e.g., sleep stages, arousal states)
- Automatic epoch definition

### signal_synchrony()

Assess synchronization between two signals.

```python
sync = nk.signal_synchrony(signal1, signal2, method='correlation')
```

**Methods:**
- `'correlation'`: Pearson correlation
- `'coherence'`: Frequency-domain coherence
- `'mutual_information'`: Information-theoretic measure
- `'phase'`: Phase locking value

**Use cases:**
- Heart-brain coupling
- Inter-brain synchrony
- Multi-channel coordination

### signal_smooth()

Apply smoothing to reduce noise.

```python
smoothed = nk.signal_smooth(signal, method='convolution', kernel='boxzen', size=10)
```

**Methods:**
- `'convolution'`: Apply kernel (boxcar, Gaussian, etc.)
- `'median'`: Median filter (robust to outliers)
- `'savgol'`: Savitzky-Golay filter (preserves peaks)
- `'loess'`: Locally weighted regression

**Kernel types (for convolution):**
- `'boxcar'`: Simple moving average
- `'gaussian'`: Gaussian-weighted average
- `'hann'`, `'hamming'`, `'blackman'`: Windowing functions

**Use cases:**
- Noise reduction
- Trend extraction
- Visualization enhancement

### signal_timefrequency()

Time-frequency representation (spectrogram).

```python
tf, time, freq = nk.signal_timefrequency(signal, sampling_rate=1000, method='stft',
                                        max_frequency=50, show=False)
```

**Methods:**
- `'stft'`: Short-Time Fourier Transform
- `'cwt'`: Continuous Wavelet Transform

**Returns:**
- `tf`: Time-frequency matrix (power at each time-frequency point)
- `time`: Time bins
- `freq`: Frequency bins

**Use cases:**
- Non-stationary signal analysis
- Time-varying frequency content
- EEG/MEG time-frequency analysis

## Simulation

### signal_simulate()

Generate various synthetic signals for testing.

```python
signal = nk.signal_simulate(duration=10, sampling_rate=1000, frequency=[5, 10],
                            amplitude=[1.0, 0.5], noise=0.1)
```

**Signal types:**
- Sinusoidal oscillations (specify frequencies)
- Multiple frequency components
- Gaussian noise
- Combinations

**Use cases:**
- Algorithm testing
- Method validation
- Educational demonstrations

## Visualization

### signal_plot()

Visualize signal and optional markers.

```python
nk.signal_plot(signal, sampling_rate=1000, peaks=None, show=True)
```

**Features:**
- Time axis in seconds
- Peak markers
- Multiple subplots for signal arrays

## Practical Tips

**Choosing filter parameters:**
- **Lowcut**: Set below lowest frequency of interest
- **Highcut**: Set above highest frequency of interest
- **Order**: Start with 2-5, increase if transition too slow
- **Method**: Butterworth is safe default

**Handling edge effects:**
- Filtering introduces artifacts at signal edges
- Pad signal before filtering, then trim
- Or discard initial/final seconds

**Dealing with gaps:**
- Small gaps: `signal_fillmissing()` with interpolation
- Large gaps: Segment signal, analyze separately
- Mark gaps as NaN, use interpolation carefully

**Combining operations:**
```python
# Typical preprocessing pipeline
signal = nk.signal_sanitize(raw_signal)  # Remove invalid values
signal = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=40)  # Bandpass
signal = nk.signal_detrend(signal, method='polynomial', order=1)  # Remove linear trend
```

**Performance considerations:**
- Filtering: FFT-based methods faster for long signals
- Resampling: Downsample early in pipeline to speed up
- Large datasets: Process in chunks if memory-limited

## References

- Virtanen, P., et al. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature methods, 17(3), 261-272.
- Tarvainen, M. P., Ranta-aho, P. O., & Karjalainen, P. A. (2002). An advanced detrending method with application to HRV analysis. IEEE Transactions on Biomedical Engineering, 49(2), 172-175.
- Huang, N. E., et al. (1998). The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society of London A, 454(1971), 903-995.
