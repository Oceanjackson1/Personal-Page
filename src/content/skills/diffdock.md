---
title: "Diffdock"
description: "Diffusion-based molecular docking. Predict protein-ligand binding poses from PDB/SMILES, confidence scores, virtual screening, for structure-based drug design. Not for affinity prediction."
category: "research"
source: "community"
author: "Community"
tags: ["diffdock"]
date: 2026-03-20
---

# DiffDock: Molecular Docking with Diffusion Models

## Overview

DiffDock is a diffusion-based deep learning tool for molecular docking that predicts 3D binding poses of small molecule ligands to protein targets. It represents the state-of-the-art in computational docking, crucial for structure-based drug discovery and chemical biology.

**Core Capabilities:**
- Predict ligand binding poses with high accuracy using deep learning
- Support protein structures (PDB files) or sequences (via ESMFold)
- Process single complexes or batch virtual screening campaigns
- Generate confidence scores to assess prediction reliability
- Handle diverse ligand inputs (SMILES, SDF, MOL2)

**Key Distinction:** DiffDock predicts **binding poses** (3D structure) and **confidence** (prediction certainty), NOT binding affinity (ΔG, Kd). Always combine with scoring functions (GNINA, MM/GBSA) for affinity assessment.

## When to Use This Skill

This skill should be used when:

- "Dock this ligand to a protein" or "predict binding pose"
- "Run molecular docking" or "perform protein-ligand docking"
- "Virtual screening" or "screen compound library"
- "Where does this molecule bind?" or "predict binding site"
- Structure-based drug design or lead optimization tasks
- Tasks involving PDB files + SMILES strings or ligand structures
- Batch docking of multiple protein-ligand pairs

## Installation and Environment Setup

### Check Environment Status

Before proceeding with DiffDock tasks, verify the environment setup:

```bash
# Use the provided setup checker
python scripts/setup_check.py
```

This script validates Python version, PyTorch with CUDA, PyTorch Geometric, RDKit, ESM, and other dependencies.

### Installation Options

**Option 1: Conda (Recommended)**
```bash
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock
conda env create --file environment.yml
conda activate diffdock
```

**Option 2: Docker**
```bash
docker pull rbgcsail/diffdock
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock
micromamba activate diffdock
```

**Important Notes:**
- GPU strongly recommended (10-100x speedup vs CPU)
- First run pre-computes SO(2)/SO(3) lookup tables (~2-5 minutes)
- Model checkpoints (~500MB) download automatically if not present

## Core Workflows

### Workflow 1: Single Protein-Ligand Docking

**Use Case:** Dock one ligand to one protein target

**Input Requirements:**
- Protein: PDB file OR amino acid sequence
- Ligand: SMILES string OR structure file (SDF/MOL2)

**Command:**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)Oc1ccccc1C(=O)O" \
  --out_dir results/single_docking/
```

**Alternative (protein sequence):**
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKF..." \
  --ligand ligand.sdf \
  --out_dir results/sequence_docking/
```

**Output Structure:**
```
results/single_docking/
├── rank_1.sdf          # Top-ranked pose
├── rank_2.sdf          # Second-ranked pose
├── ...
├── rank_10.sdf         # 10th pose (default: 10 samples)
└── confidence_scores.txt
```

### Workflow 2: Batch Processing Multiple Complexes

**Use Case:** Dock multiple ligands to proteins, virtual screening campaigns

**Step 1: Prepare Batch CSV**

Use the provided script to create or validate batch input:

```bash
# Create template
python scripts/prepare_batch_csv.py --create --output batch_input.csv

# Validate existing CSV
python scripts/prepare_batch_csv.py my_input.csv --validate
```

**CSV Format:**
```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFT...
complex3,protein3.pdb,ligand3.sdf,
```

**Required Columns:**
- `complex_name`: Unique identifier
- `protein_path`: PDB file path (leave empty if using sequence)
- `ligand_description`: SMILES string or ligand file path
- `protein_sequence`: Amino acid sequence (leave empty if using PDB)

**Step 2: Run Batch Docking**

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv batch_input.csv \
  --out_dir results/batch/ \
  --batch_size 10
```

**For Large Virtual Screening (>100 compounds):**

Pre-compute protein embeddings for faster processing:
```bash
# Pre-compute embeddings
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# Run with pre-computed embeddings
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/screening/
```

### Workflow 3: Analyzing Results

After docking completes, analyze confidence scores and rank predictions:

```bash
# Analyze all results
python scripts/analyze_results.py results/batch/

# Show top 5 per complex
python scripts/analyze_results.py results/batch/ --top 5

# Filter by confidence threshold
python scripts/analyze_results.py results/batch/ --threshold 0.0

# Export to CSV
python scripts/analyze_results.py results/batch/ --export summary.csv

# Show top 20 predictions across all complexes
python scripts/analyze_results.py results/batch/ --best 20
```

The analysis script:
- Parses confidence scores from all predictions
- Classifies as High (>0), Moderate (-1.5 to 0), or Low (<-1.5)
- Ranks predictions within and across complexes
- Generates statistical summaries
- Exports results to CSV for downstream analysis

## Confidence Score Interpretation

**Understanding Scores:**

| Score Range | Confidence Level | Interpretation |
|------------|------------------|----------------|
| **> 0** | High | Strong prediction, likely accurate |
| **-1.5 to 0** | Moderate | Reasonable prediction, validate carefully |
| **< -1.5** | Low | Uncertain prediction, requires validation |

**Critical Notes:**
1. **Confidence ≠ Affinity**: High confidence means model certainty about structure, NOT strong binding
2. **Context Matters**: Adjust expectations for:
   - Large ligands (>500 Da): Lower confidence expected
   - Multiple protein chains: May decrease confidence
   - Novel protein families: May underperform
3. **Multiple Samples**: Review top 3-5 predictions, look for consensus

**For detailed guidance:** Read `references/confidence_and_limitations.md` using the Read tool

## Parameter Customization

### Using Custom Configuration

Create custom configuration for specific use cases:

```bash
# Copy template
cp assets/custom_inference_config.yaml my_config.yaml

# Edit parameters (see template for presets)
# Then run with custom config
python -m inference \
  --config my_config.yaml \
  --protein_ligand_csv input.csv \
  --out_dir results/
```

### Key Parameters to Adjust

**Sampling Density:**
- `samples_per_complex: 10` → Increase to 20-40 for difficult cases
- More samples = better coverage but longer runtime

**Inference Steps:**
- `inference_steps: 20` → Increase to 25-30 for higher accuracy
- More steps = potentially better quality but slower

**Temperature Parameters (control diversity):**
- `temp_sampling_tor: 7.04` → Increase for flexible ligands (8-10)
- `temp_sampling_tor: 7.04` → Decrease for rigid ligands (5-6)
- Higher temperature = more diverse poses

**Presets Available in Template:**
1. High Accuracy: More samples + steps, lower temperature
2. Fast Screening: Fewer samples, faster
3. Flexible Ligands: Increased torsion temperature
4. Rigid Ligands: Decreased torsion temperature

**For complete parameter reference:** Read `references/parameters_reference.md` using the Read tool

## Advanced Techniques

### Ensemble Docking (Protein Flexibility)

For proteins with known flexibility, dock to multiple conformations:

```python
# Create ensemble CSV
import pandas as pd

conformations = ["conf1.pdb", "conf2.pdb", "conf3.pdb"]
ligand = "CC(=O)Oc1ccccc1C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

Run docking with increased sampling:
```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --samples_per_complex 20 \
  --out_dir results/ensemble/
```

### Integration with Scoring Functions

DiffDock generates poses; combine with other tools for affinity:

**GNINA (Fast neural network scoring):**
```bash
for pose in results/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only
done
```

**MM/GBSA (More accurate, slower):**
Use AmberTools MMPBSA.py or gmx_MMPBSA after energy minimization

**Free Energy Calculations (Most accurate):**
Use OpenMM + OpenFE or GROMACS for FEP/TI calculations

**Recommended Workflow:**
1. DiffDock → Generate poses with confidence scores
2. Visual inspection → Check structural plausibility
3. GNINA or MM/GBSA → Rescore and rank by affinity
4. Experimental validation → Biochemical assays

## Limitations and Scope

**DiffDock IS Designed For:**
- Small molecule ligands (typically 100-1000 Da)
- Drug-like organic compounds
- Small peptides (<20 residues)
- Single or multi-chain proteins

**DiffDock IS NOT Designed For:**
- Large biomolecules (protein-protein docking) → Use DiffDock-PP or AlphaFold-Multimer
- Large peptides (>20 residues) → Use alternative methods
- Covalent docking → Use specialized covalent docking tools
- Binding affinity prediction → Combine with scoring functions
- Membrane proteins → Not specifically trained, use with caution

**For complete limitations:** Read `references/confidence_and_limitations.md` using the Read tool

## Troubleshooting

### Common Issues

**Issue: Low confidence scores across all predictions**
- Cause: Large/unusual ligands, unclear binding site, protein flexibility
- Solution: Increase `samples_per_complex` (20-40), try ensemble docking, validate protein structure

**Issue: Out of memory errors**
- Cause: GPU memory insufficient for batch size
- Solution: Reduce `--batch_size 2` or process fewer complexes at once

**Issue: Slow performance**
- Cause: Running on CPU instead of GPU
- Solution: Verify CUDA with `python -c "import torch; print(torch.cuda.is_available())"`, use GPU

**Issue: Unrealistic binding poses**
- Cause: Poor protein preparation, ligand too large, wrong binding site
- Solution: Check protein for missing residues, remove far waters, consider specifying binding site

**Issue: "Module not found" errors**
- Cause: Missing dependencies or wrong environment
- Solution: Run `python scripts/setup_check.py` to diagnose

### Performance Optimization

**For Best Results:**
1. Use GPU (essential for practical use)
2. Pre-compute ESM embeddings for repeated protein use
3. Batch process multiple complexes together
4. Start with default parameters, then tune if needed
5. Validate protein structures (resolve missing residues)
6. Use canonical SMILES for ligands

## Graphical User Interface

For interactive use, launch the web interface:

```bash
python app/main.py
# Navigate to http://localhost:7860
```

Or use the online demo without installation:
- https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## Resources

### Helper Scripts (`scripts/`)

**`prepare_batch_csv.py`**: Create and validate batch input CSV files
- Create templates with example entries
- Validate file paths and SMILES strings
- Check for required columns and format issues

**`analyze_results.py`**: Analyze confidence scores and rank predictions
- Parse results from single or batch runs
- Generate statistical summaries
- Export to CSV for downstream analysis
- Identify top predictions across complexes

**`setup_check.py`**: Verify DiffDock environment setup
- Check Python version and dependencies
- Verify PyTorch and CUDA availability
- Test RDKit and PyTorch Geometric installation
- Provide installation instructions if needed

### Reference Documentation (`references/`)

**`parameters_reference.md`**: Complete parameter documentation
- All command-line options and configuration parameters
- Default values and acceptable ranges
- Temperature parameters for controlling diversity
- Model checkpoint locations and version flags

Read this file when users need:
- Detailed parameter explanations
- Fine-tuning guidance for specific systems
- Alternative sampling strategies

**`confidence_and_limitations.md`**: Confidence score interpretation and tool limitations
- Detailed confidence score interpretation
- When to trust predictions
- Scope and limitations of DiffDock
- Integration with complementary tools
- Troubleshooting prediction quality

Read this file when users need:
- Help interpreting confidence scores
- Understanding when NOT to use DiffDock
- Guidance on combining with other tools
- Validation strategies

**`workflows_examples.md`**: Comprehensive workflow examples
- Detailed installation instructions
- Step-by-step examples for all workflows
- Advanced integration patterns
- Troubleshooting common issues
- Best practices and optimization tips

Read this file when users need:
- Complete workflow examples with code
- Integration with GNINA, OpenMM, or other tools
- Virtual screening workflows
- Ensemble docking procedures

### Assets (`assets/`)

**`batch_template.csv`**: Template for batch processing
- Pre-formatted CSV with required columns
- Example entries showing different input types
- Ready to customize with actual data

**`custom_inference_config.yaml`**: Configuration template
- Annotated YAML with all parameters
- Four preset configurations for common use cases
- Detailed comments explaining each parameter
- Ready to customize and use

## Best Practices

1. **Always verify environment** with `setup_check.py` before starting large jobs
2. **Validate batch CSVs** with `prepare_batch_csv.py` to catch errors early
3. **Start with defaults** then tune parameters based on system-specific needs
4. **Generate multiple samples** (10-40) for robust predictions
5. **Visual inspection** of top poses before downstream analysis
6. **Combine with scoring** functions for affinity assessment
7. **Use confidence scores** for initial ranking, not final decisions
8. **Pre-compute embeddings** for virtual screening campaigns
9. **Document parameters** used for reproducibility
10. **Validate results** experimentally when possible

## Citations

When using DiffDock, cite the appropriate papers:

**DiffDock-L (current default model):**
```
Stärk et al. (2024) "DiffDock-L: Improving Molecular Docking with Diffusion Models"
arXiv:2402.18396
```

**Original DiffDock:**
```
Corso et al. (2023) "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking"
ICLR 2023, arXiv:2210.01776
```

## Additional Resources

- **GitHub Repository**: https://github.com/gcorso/DiffDock
- **Online Demo**: https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web
- **DiffDock-L Paper**: https://arxiv.org/abs/2402.18396
- **Original Paper**: https://arxiv.org/abs/2210.01776

---

## Reference: Confidence_And_Limitations

# DiffDock Confidence Scores and Limitations

This document provides detailed guidance on interpreting DiffDock confidence scores and understanding the tool's limitations.

## Confidence Score Interpretation

DiffDock generates a confidence score for each predicted binding pose. This score indicates the model's certainty about the prediction.

### Score Ranges

| Score Range | Confidence Level | Interpretation |
|------------|------------------|----------------|
| **> 0** | High confidence | Strong prediction, likely accurate binding pose |
| **-1.5 to 0** | Moderate confidence | Reasonable prediction, may need validation |
| **< -1.5** | Low confidence | Uncertain prediction, requires careful validation |

### Important Notes on Confidence Scores

1. **Not Binding Affinity**: Confidence scores reflect prediction certainty, NOT binding affinity strength
   - High confidence = model is confident about the structure
   - Does NOT indicate strong/weak binding affinity

2. **Context-Dependent**: Confidence scores should be adjusted based on system complexity:
   - **Lower expectations** for:
     - Large ligands (>500 Da)
     - Protein complexes with many chains
     - Unbound protein conformations (may require conformational changes)
     - Novel protein families not well-represented in training data

   - **Higher expectations** for:
     - Drug-like small molecules (150-500 Da)
     - Single-chain proteins or well-defined binding sites
     - Proteins similar to those in training data (PDBBind, BindingMOAD)

3. **Multiple Predictions**: DiffDock generates multiple samples per complex (default: 10)
   - Review top-ranked predictions (by confidence)
   - Consider clustering similar poses
   - High-confidence consensus across multiple samples strengthens prediction

## What DiffDock Predicts

### ✅ DiffDock DOES Predict
- **Binding poses**: 3D spatial orientation of ligand in protein binding site
- **Confidence scores**: Model's certainty about predictions
- **Multiple conformations**: Various possible binding modes

### ❌ DiffDock DOES NOT Predict
- **Binding affinity**: Strength of protein-ligand interaction (ΔG, Kd, Ki)
- **Binding kinetics**: On/off rates, residence time
- **ADMET properties**: Absorption, distribution, metabolism, excretion, toxicity
- **Selectivity**: Relative binding to different targets

## Scope and Limitations

### Designed For
- **Small molecule docking**: Organic compounds typically 100-1000 Da
- **Protein targets**: Single or multi-chain proteins
- **Small peptides**: Short peptide ligands (< ~20 residues)
- **Small nucleic acids**: Short oligonucleotides

### NOT Designed For
- **Large biomolecules**: Full protein-protein interactions
  - Use DiffDock-PP, AlphaFold-Multimer, or RoseTTAFold2NA instead
- **Large peptides/proteins**: >20 residues as ligands
- **Covalent docking**: Irreversible covalent bond formation
- **Metalloprotein specifics**: May not accurately handle metal coordination
- **Membrane proteins**: Not specifically trained on membrane-embedded proteins

### Training Data Considerations

DiffDock was trained on:
- **PDBBind**: Diverse protein-ligand complexes
- **BindingMOAD**: Multi-domain protein structures

**Implications**:
- Best performance on proteins/ligands similar to training data
- May underperform on:
  - Novel protein families
  - Unusual ligand chemotypes
  - Allosteric sites not well-represented in training data

## Validation and Complementary Tools

### Recommended Workflow

1. **Generate poses with DiffDock**
   - Use confidence scores for initial ranking
   - Consider multiple high-confidence predictions

2. **Visual Inspection**
   - Examine protein-ligand interactions in molecular viewer
   - Check for reasonable:
     - Hydrogen bonds
     - Hydrophobic interactions
     - Steric complementarity
     - Electrostatic interactions

3. **Scoring and Refinement** (choose one or more):
   - **GNINA**: Deep learning-based scoring function
   - **Molecular mechanics**: Energy minimization and refinement
   - **MM/GBSA or MM/PBSA**: Binding free energy estimation
   - **Free energy calculations**: FEP or TI for accurate affinity prediction

4. **Experimental Validation**
   - Biochemical assays (IC50, Kd measurements)
   - Structural validation (X-ray crystallography, cryo-EM)

### Tools for Binding Affinity Assessment

DiffDock should be combined with these tools for affinity prediction:

- **GNINA**: Fast, accurate scoring function
  - Github: github.com/gnina/gnina

- **AutoDock Vina**: Classical docking and scoring
  - Website: vina.scripps.edu

- **Free Energy Calculations**:
  - OpenMM + OpenFE
  - GROMACS + ABFE/RBFE protocols

- **MM/GBSA Tools**:
  - MMPBSA.py (AmberTools)
  - gmx_MMPBSA

## Performance Optimization

### For Best Results

1. **Protein Preparation**:
   - Remove water molecules far from binding site
   - Resolve missing residues if possible
   - Consider protonation states at physiological pH

2. **Ligand Input**:
   - Provide reasonable 3D conformers when using structure files
   - Use canonical SMILES for consistent results
   - Pre-process with RDKit if needed

3. **Computational Resources**:
   - GPU strongly recommended (10-100x speedup)
   - First run pre-computes lookup tables (takes a few minutes)
   - Batch processing more efficient than single predictions

4. **Parameter Tuning**:
   - Increase `samples_per_complex` for difficult cases (20-40)
   - Adjust temperature parameters for diversity/accuracy trade-off
   - Use pre-computed ESM embeddings for repeated predictions

## Common Issues and Troubleshooting

### Low Confidence Scores
- **Large/flexible ligands**: Consider splitting into fragments or use alternative methods
- **Multiple binding sites**: May predict multiple locations with distributed confidence
- **Protein flexibility**: Consider using ensemble of protein conformations

### Unrealistic Predictions
- **Clashes**: May indicate need for protein preparation or refinement
- **Surface binding**: Check if true binding site is blocked or unclear
- **Unusual poses**: Consider increasing samples to explore more conformations

### Slow Performance
- **Use GPU**: Essential for reasonable runtime
- **Pre-compute embeddings**: Reuse ESM embeddings for same protein
- **Batch processing**: More efficient than sequential individual predictions
- **Reduce samples**: Lower `samples_per_complex` for quick screening

## Citation and Further Reading

For methodology details and benchmarking results, see:

1. **Original DiffDock Paper** (ICLR 2023):
   - "DiffDock: Diffusion Steps, Twists, and Turns for Molecular Docking"
   - Corso et al., arXiv:2210.01776

2. **DiffDock-L Paper** (2024):
   - Enhanced model with improved generalization
   - Stärk et al., arXiv:2402.18396

3. **PoseBusters Benchmark**:
   - Rigorous docking evaluation framework
   - Used for DiffDock validation

---

## Reference: Parameters_Reference

# DiffDock Configuration Parameters Reference

This document provides comprehensive details on all DiffDock configuration parameters and command-line options.

## Model & Checkpoint Settings

### Model Paths
- **`--model_dir`**: Directory containing the score model checkpoint
  - Default: `./workdir/v1.1/score_model`
  - DiffDock-L model (current default)

- **`--confidence_model_dir`**: Directory containing the confidence model checkpoint
  - Default: `./workdir/v1.1/confidence_model`

- **`--ckpt`**: Name of the score model checkpoint file
  - Default: `best_ema_inference_epoch_model.pt`

- **`--confidence_ckpt`**: Name of the confidence model checkpoint file
  - Default: `best_model_epoch75.pt`

### Model Version Flags
- **`--old_score_model`**: Use original DiffDock model instead of DiffDock-L
  - Default: `false` (uses DiffDock-L)

- **`--old_filtering_model`**: Use legacy confidence filtering approach
  - Default: `true`

## Input/Output Options

### Input Specification
- **`--protein_path`**: Path to protein PDB file
  - Example: `--protein_path protein.pdb`
  - Alternative to `--protein_sequence`

- **`--protein_sequence`**: Amino acid sequence for ESMFold folding
  - Automatically generates protein structure from sequence
  - Alternative to `--protein_path`

- **`--ligand`**: Ligand specification (SMILES string or file path)
  - SMILES string: `--ligand "COc(cc1)ccc1C#N"`
  - File path: `--ligand ligand.sdf` or `.mol2`

- **`--protein_ligand_csv`**: CSV file for batch processing
  - Required columns: `complex_name`, `protein_path`, `ligand_description`, `protein_sequence`
  - Example: `--protein_ligand_csv data/protein_ligand_example.csv`

### Output Control
- **`--out_dir`**: Output directory for predictions
  - Example: `--out_dir results/user_predictions/`

- **`--save_visualisation`**: Export predicted molecules as SDF files
  - Enables visualization of results

## Inference Parameters

### Diffusion Steps
- **`--inference_steps`**: Number of planned inference iterations
  - Default: `20`
  - Higher values may improve accuracy but increase runtime

- **`--actual_steps`**: Actual diffusion steps executed
  - Default: `19`

- **`--no_final_step_noise`**: Omit noise at the final diffusion step
  - Default: `true`

### Sampling Settings
- **`--samples_per_complex`**: Number of samples to generate per complex
  - Default: `10`
  - More samples provide better coverage but increase computation

- **`--sigma_schedule`**: Noise schedule type
  - Default: `expbeta` (exponential-beta)

- **`--initial_noise_std_proportion`**: Initial noise standard deviation scaling
  - Default: `1.46`

### Temperature Parameters

#### Sampling Temperatures (Controls diversity of predictions)
- **`--temp_sampling_tr`**: Translation sampling temperature
  - Default: `1.17`

- **`--temp_sampling_rot`**: Rotation sampling temperature
  - Default: `2.06`

- **`--temp_sampling_tor`**: Torsion sampling temperature
  - Default: `7.04`

#### Psi Angle Temperatures
- **`--temp_psi_tr`**: Translation psi temperature
  - Default: `0.73`

- **`--temp_psi_rot`**: Rotation psi temperature
  - Default: `0.90`

- **`--temp_psi_tor`**: Torsion psi temperature
  - Default: `0.59`

#### Sigma Data Temperatures
- **`--temp_sigma_data_tr`**: Translation data distribution scaling
  - Default: `0.93`

- **`--temp_sigma_data_rot`**: Rotation data distribution scaling
  - Default: `0.75`

- **`--temp_sigma_data_tor`**: Torsion data distribution scaling
  - Default: `0.69`

## Processing Options

### Performance
- **`--batch_size`**: Processing batch size
  - Default: `10`
  - Larger values increase throughput but require more memory

- **`--tqdm`**: Enable progress bar visualization
  - Useful for monitoring long-running jobs

### Protein Structure
- **`--chain_cutoff`**: Maximum number of protein chains to process
  - Example: `--chain_cutoff 10`
  - Useful for large multi-chain complexes

- **`--esm_embeddings_path`**: Path to pre-computed ESM2 protein embeddings
  - Speeds up inference by reusing embeddings
  - Optional optimization

### Dataset Options
- **`--split`**: Dataset split to use (train/test/val)
  - Used for evaluation on standard benchmarks

## Advanced Flags

### Debugging & Testing
- **`--no_model`**: Disable model inference (debugging)
  - Default: `false`

- **`--no_random`**: Disable randomization
  - Default: `false`
  - Useful for reproducibility testing

### Alternative Sampling
- **`--ode`**: Use ODE solver instead of SDE
  - Default: `false`
  - Alternative sampling approach

- **`--different_schedules`**: Use different noise schedules per component
  - Default: `false`

### Error Handling
- **`--limit_failures`**: Maximum allowed failures before stopping
  - Default: `5`

## Configuration File

All parameters can be specified in a YAML configuration file (typically `default_inference_args.yaml`) or overridden via command line:

```bash
python -m inference --config default_inference_args.yaml --samples_per_complex 20
```

Command-line arguments take precedence over configuration file values.

---

## Reference: Workflows_Examples

# DiffDock Workflows and Examples

This document provides practical workflows and usage examples for common DiffDock tasks.

## Installation and Setup

### Conda Installation (Recommended)

```bash
# Clone repository
git clone https://github.com/gcorso/DiffDock.git
cd DiffDock

# Create conda environment
conda env create --file environment.yml
conda activate diffdock
```

### Docker Installation

```bash
# Pull Docker image
docker pull rbgcsail/diffdock

# Run container with GPU support
docker run -it --gpus all --entrypoint /bin/bash rbgcsail/diffdock

# Inside container, activate environment
micromamba activate diffdock
```

### First Run
The first execution pre-computes SO(2) and SO(3) lookup tables, taking a few minutes. Subsequent runs start immediately.

## Workflow 1: Single Protein-Ligand Docking

### Using PDB File and SMILES String

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path examples/protein.pdb \
  --ligand "COc1ccc(C(=O)Nc2ccccc2)cc1" \
  --out_dir results/single_docking/
```

**Output Structure**:
```
results/single_docking/
├── index_0_rank_1.sdf       # Top-ranked prediction
├── index_0_rank_2.sdf       # Second-ranked prediction
├── ...
├── index_0_rank_10.sdf      # 10th prediction (if samples_per_complex=10)
└── confidence_scores.txt    # Scores for all predictions
```

### Using Ligand Structure File

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand ligand.sdf \
  --out_dir results/ligand_file/
```

**Supported ligand formats**: SDF, MOL2, or any format readable by RDKit

## Workflow 2: Protein Sequence to Structure Docking

### Using ESMFold for Protein Folding

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_sequence "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPTLVTTFSYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITHGMDELYK" \
  --ligand "CC(C)Cc1ccc(cc1)C(C)C(=O)O" \
  --out_dir results/sequence_docking/
```

**Use Cases**:
- Protein structure not available in PDB
- Modeling mutations or variants
- De novo protein design validation

**Note**: ESMFold folding adds computation time (30s-5min depending on sequence length)

## Workflow 3: Batch Processing Multiple Complexes

### Prepare CSV File

Create `complexes.csv` with required columns:

```csv
complex_name,protein_path,ligand_description,protein_sequence
complex1,proteins/protein1.pdb,CC(=O)Oc1ccccc1C(=O)O,
complex2,,COc1ccc(C#N)cc1,MSKGEELFTGVVPILVELDGDVNGHKF...
complex3,proteins/protein3.pdb,ligands/ligand3.sdf,
```

**Column Descriptions**:
- `complex_name`: Unique identifier for the complex
- `protein_path`: Path to PDB file (leave empty if using sequence)
- `ligand_description`: SMILES string or path to ligand file
- `protein_sequence`: Amino acid sequence (leave empty if using PDB)

### Run Batch Docking

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv complexes.csv \
  --out_dir results/batch_predictions/ \
  --batch_size 10
```

**Output Structure**:
```
results/batch_predictions/
├── complex1/
│   ├── rank_1.sdf
│   ├── rank_2.sdf
│   └── ...
├── complex2/
│   ├── rank_1.sdf
│   └── ...
└── complex3/
    └── ...
```

## Workflow 4: High-Throughput Virtual Screening

### Setup for Screening Large Ligand Libraries

```python
# generate_screening_csv.py
import pandas as pd

# Load ligand library
ligands = pd.read_csv("ligand_library.csv")  # Contains SMILES

# Create DiffDock input
screening_data = {
    "complex_name": [f"screen_{i}" for i in range(len(ligands))],
    "protein_path": ["target_protein.pdb"] * len(ligands),
    "ligand_description": ligands["smiles"].tolist(),
    "protein_sequence": [""] * len(ligands)
}

df = pd.DataFrame(screening_data)
df.to_csv("screening_input.csv", index=False)
```

### Run Screening

```bash
# Pre-compute ESM embeddings for faster screening
python datasets/esm_embedding_preparation.py \
  --protein_ligand_csv screening_input.csv \
  --out_file protein_embeddings.pt

# Run docking with pre-computed embeddings
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv screening_input.csv \
  --esm_embeddings_path protein_embeddings.pt \
  --out_dir results/virtual_screening/ \
  --batch_size 32
```

### Post-Processing: Extract Top Hits

```python
# analyze_screening_results.py
import os
import pandas as pd

results = []
results_dir = "results/virtual_screening/"

for complex_dir in os.listdir(results_dir):
    confidence_file = os.path.join(results_dir, complex_dir, "confidence_scores.txt")
    if os.path.exists(confidence_file):
        with open(confidence_file) as f:
            scores = [float(line.strip()) for line in f]
            top_score = max(scores)
            results.append({"complex": complex_dir, "top_confidence": top_score})

# Sort by confidence
df = pd.DataFrame(results)
df_sorted = df.sort_values("top_confidence", ascending=False)

# Get top 100 hits
top_hits = df_sorted.head(100)
top_hits.to_csv("top_hits.csv", index=False)
```

## Workflow 5: Ensemble Docking with Protein Flexibility

### Prepare Protein Ensemble

```python
# For proteins with known flexibility, use multiple conformations
# Example: Using MD snapshots or crystal structures

# create_ensemble_csv.py
import pandas as pd

conformations = [
    "protein_conf1.pdb",
    "protein_conf2.pdb",
    "protein_conf3.pdb",
    "protein_conf4.pdb"
]

ligand = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"

data = {
    "complex_name": [f"ensemble_{i}" for i in range(len(conformations))],
    "protein_path": conformations,
    "ligand_description": [ligand] * len(conformations),
    "protein_sequence": [""] * len(conformations)
}

pd.DataFrame(data).to_csv("ensemble_input.csv", index=False)
```

### Run Ensemble Docking

```bash
python -m inference \
  --config default_inference_args.yaml \
  --protein_ligand_csv ensemble_input.csv \
  --out_dir results/ensemble_docking/ \
  --samples_per_complex 20  # More samples per conformation
```

## Workflow 6: Integration with Downstream Analysis

### Example: DiffDock + GNINA Rescoring

```bash
# 1. Run DiffDock
python -m inference \
  --config default_inference_args.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)OC1=CC=CC=C1C(=O)O" \
  --out_dir results/diffdock_poses/ \
  --save_visualisation

# 2. Rescore with GNINA
for pose in results/diffdock_poses/*.sdf; do
    gnina -r protein.pdb -l "$pose" --score_only -o "${pose%.sdf}_gnina.sdf"
done
```

### Example: DiffDock + OpenMM Energy Minimization

```python
# minimize_poses.py
from openmm import app, LangevinIntegrator, Platform
from openmm.app import ForceField, Modeller, PDBFile
from rdkit import Chem
import os

# Load protein
protein = PDBFile('protein.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

# Process each DiffDock pose
pose_dir = 'results/diffdock_poses/'
for pose_file in os.listdir(pose_dir):
    if pose_file.endswith('.sdf'):
        # Load ligand
        mol = Chem.SDMolSupplier(os.path.join(pose_dir, pose_file))[0]

        # Combine protein + ligand
        modeller = Modeller(protein.topology, protein.positions)
        # ... add ligand to modeller ...

        # Create system and minimize
        system = forcefield.createSystem(modeller.topology)
        integrator = LangevinIntegrator(300, 1.0, 0.002)
        simulation = app.Simulation(modeller.topology, system, integrator)
        simulation.minimizeEnergy(maxIterations=1000)

        # Save minimized structure
        positions = simulation.context.getState(getPositions=True).getPositions()
        PDBFile.writeFile(simulation.topology, positions,
                         open(f"minimized_{pose_file}.pdb", 'w'))
```

## Workflow 7: Using the Graphical Interface

### Launch Web Interface

```bash
python app/main.py
```

### Access Interface
Navigate to `http://localhost:7860` in web browser

### Features
- Upload protein PDB or enter sequence
- Input ligand SMILES or upload structure
- Adjust inference parameters via GUI
- Visualize results interactively
- Download predictions directly

### Online Alternative
Use the Hugging Face Spaces demo without local installation:
- URL: https://huggingface.co/spaces/reginabarzilaygroup/DiffDock-Web

## Advanced Configuration

### Custom Inference Settings

Create custom YAML configuration:

```yaml
# custom_inference.yaml
# Model settings
model_dir: ./workdir/v1.1/score_model
confidence_model_dir: ./workdir/v1.1/confidence_model

# Sampling parameters
samples_per_complex: 20  # More samples for better coverage
inference_steps: 25      # More steps for accuracy

# Temperature adjustments (increase for more diversity)
temp_sampling_tr: 1.3
temp_sampling_rot: 2.2
temp_sampling_tor: 7.5

# Output
save_visualisation: true
```

Use custom configuration:

```bash
python -m inference \
  --config custom_inference.yaml \
  --protein_path protein.pdb \
  --ligand "CC(=O)OC1=CC=CC=C1C(=O)O" \
  --out_dir results/custom_config/
```

## Troubleshooting Common Issues

### Issue: Out of Memory Errors

**Solution**: Reduce batch size
```bash
python -m inference ... --batch_size 2
```

### Issue: Slow Performance

**Solution**: Ensure GPU usage
```python
import torch
print(torch.cuda.is_available())  # Should return True
```

### Issue: Poor Predictions for Large Ligands

**Solution**: Increase sampling diversity
```bash
python -m inference ... --samples_per_complex 40 --temp_sampling_tor 9.0
```

### Issue: Protein with Many Chains

**Solution**: Limit chains or isolate binding site
```bash
python -m inference ... --chain_cutoff 4
```

Or pre-process PDB to include only relevant chains.

## Best Practices Summary

1. **Start Simple**: Test with single complex before batch processing
2. **GPU Essential**: Use GPU for reasonable performance
3. **Multiple Samples**: Generate 10-40 samples for robust predictions
4. **Validate Results**: Use molecular visualization and complementary scoring
5. **Consider Confidence**: Use confidence scores for initial ranking, not final decisions
6. **Iterate Parameters**: Adjust temperature/steps for specific systems
7. **Pre-compute Embeddings**: For repeated use of same protein
8. **Combine Tools**: Integrate with scoring functions and energy minimization
