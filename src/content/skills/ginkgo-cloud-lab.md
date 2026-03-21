---
title: "Ginkgo Cloud Lab"
description: "Submit and manage protocols on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio), a web-based interface for autonomous lab execution on Reconfigurable Automation Carts (RACs). Use when the user wants to run cell-free protein expression (validation or o..."
category: "devops"
source: "community"
author: "Community"
tags: ["ginkgo", "cloud", "lab"]
date: 2026-03-20
---

# Ginkgo Cloud Lab

## Overview

Ginkgo Cloud Lab (https://cloud.ginkgo.bio) provides remote access to Ginkgo Bioworks' autonomous lab infrastructure. Protocols are executed on Reconfigurable Automation Carts (RACs) -- modular units with robotic arms, maglev sample transport, and industrial-grade software spanning 70+ instruments.

The platform also includes **EstiMate**, an AI agent that accepts human-language protocol descriptions and returns feasibility assessments and pricing for custom workflows beyond the listed protocols.

## Available Protocols

### 1. Cell Free Protein Expression Validation

Rapid go/no-go expression screening using reconstituted E. coli CFPS. Submit a FASTA sequence (up to 1800 bp) and receive expression confirmation, baseline titer (mg/L), and initial purity with virtual gel images.

- **Price:** $39/sample | **Turnaround:** 5-10 days | **Status:** Certified
- **Details:** See [references/cell-free-protein-expression-validation.md](references/cell-free-protein-expression-validation.md)

### 2. Cell Free Protein Expression Optimization

DoE-based optimization across up to 24 conditions per protein (lysates, temperatures, chaperones, disulfide enhancers, cofactors). Designed for difficult-to-express and membrane proteins.

- **Price:** $199/sample | **Turnaround:** 6-11 days | **Status:** Certified
- **Details:** See [references/cell-free-protein-expression-optimization.md](references/cell-free-protein-expression-optimization.md)

### 3. Fluorescent Pixel Art Generation

Transform a pixel art image (48x48 to 96x96 px, PNG/SVG) into fluorescent bacterial artwork using up to 11 E. coli strains via acoustic dispensing. Delivered as high-res UV photographs.

- **Price:** $25/plate | **Turnaround:** 5-7 days | **Status:** Beta
- **Details:** See [references/fluorescent-pixel-art-generation.md](references/fluorescent-pixel-art-generation.md)

## General Ordering Workflow

1. Select a protocol at https://cloud.ginkgo.bio/protocols
2. Configure parameters (number of samples/proteins, replicates, plates)
3. Upload input files (FASTA for protein protocols, PNG/SVG for pixel art)
4. Add any special requirements in the Additional Details field
5. Submit and receive a feasibility report and price quote

For protocols not listed above, use the **EstiMate** chat to describe a custom protocol in plain language and receive compatibility assessment and pricing.

## Authentication

Access Ginkgo Cloud Lab at https://cloud.ginkgo.bio. Account creation or institutional access may be required. Contact Ginkgo at cloud@ginkgo.bio for access questions.

## Key Infrastructure

- **RACs (Reconfigurable Automation Carts):** Modular robotic units with high-precision arms and maglev transport
- **Catalyst Software:** Protocol orchestration, scheduling, parameterization, and real-time monitoring
- **70+ integrated instruments:** Sample prep, liquid handling, analytical readouts, storage, incubation
- **Nebula:** Ginkgo's autonomous lab facility in Boston, MA

---

## Reference: Cell Free Protein Expression Optimization

# Cell Free Protein Expression Optimization

**URL:** https://cloud.ginkgo.bio/protocols/cell-free-protein-expression-optimization
**Status:** Ginkgo Certified
**Price:** $199/sample (default: $597 for 1 protein x 3 replicates = 3 samples)
**Turnaround:** 6-11 days

## Overview

Design of Experiment (DoE) approach to expressing protein targets in a proprietary reconstituted E. coli transcription-translation system. Each construct is evaluated in up to 24 reaction conditions per protein, including target-specific additives such as chaperones, disulfide-bond enhancers, and cofactors. Designed for difficult-to-express proteins including membrane proteins and targets with disulfide or cofactor requirements.

## Input

- **DNA sequence** in `.fasta` format

## Output

- **Comparative Yield:** Titer data mapped across all tested variables (lysates, temps, additives)
- **Purity Profiling:** Target protein vs. background impurities to find highest quality yield
- **Optimal Conditions:** Overlaid electropherograms pinpointing the exact formulation for a given sequence

## Automated Workflow

### Phase 1 - Reagent Prep

1. Retrieve plates from 4 deg C
2. Thaw at room temperature
3. PBS backfill

### Phase 2 - CFPS Reaction Setup & Incubation

1. Retrieve plates from 4 deg C
2. Dispense lysate
3. QC plate read
4. Incubate (shaking or static, condition-dependent)

### Phase 3 - Quantification Prep & Read

1. Dispense PBS
2. Unseal plate
3. LabChip quantification
4. Seal plate
5. Store at 4 deg C

## Protocol Parameters

- Payloads & Reagents
- Bravo Stamp
- HiG Centrifuge
- Incubation & Storage

## Optimization Variables

The DoE matrix can span up to 24 conditions per protein, varying:

- **Lysate composition** (different E. coli extract formulations)
- **Temperature** (incubation temperature profiles)
- **Additives:**
  - Chaperones (for folding-challenged targets)
  - Disulfide-bond enhancers (for targets requiring disulfide bridges)
  - Cofactors (metal ions, coenzymes, prosthetic groups)
  - Other target-specific supplements

## Ordering

- **Number of Proteins:** configurable
- **Number of Replicates:** configurable
- **File Upload:** CSV, Excel, FASTA, TXT, PDF, ZIP
- **Additional Details:** free-text field for special requirements

## Certification Milestones

- Dry Run Complete
- Wet Run Complete
- Biovalidation Complete
- App Note Complete

## Use Cases

- Optimizing expression of difficult-to-express proteins
- Membrane protein expression screening
- Identifying optimal conditions for disulfide-bonded proteins
- Cofactor-dependent protein expression
- Systematic exploration of expression parameter space
- Finding the best formulation before scaling up production

---

## Reference: Cell Free Protein Expression Validation

# Cell Free Protein Expression Validation

**URL:** https://cloud.ginkgo.bio/protocols/cell-free-protein-expression-validation
**Status:** Ginkgo Certified
**Price:** $39/sample (default: $936 for 8 proteins x 3 replicates = 24 samples)
**Turnaround:** 5-10 days

## Overview

Fastest path from a protein sequence to a quantitative go/no-go readout on expression. Uses a proprietary reconstituted E. coli transcription-translation (cell-free protein synthesis, CFPS) system. Reactions complete in 4-16 hours. Designed for early-stage screening, novel construct evaluation, and rapid triage of candidate sequences before committing resources to downstream optimization or purification.

## Input

- **DNA sequence** in `.fasta` format
- Sequences up to 1800 bp supported

## Output

- **Expression Confirmation:** Verification of target protein at expected molecular weight
- **Baseline Titer:** Initial quantitative yield measurement (mg/L)
- **Initial Purity:** Percentage of target protein vs. impurities, delivered with virtual gel images

## Automated Workflow

### Phase 1 - CFPS Reaction Setup & Incubation

1. Retrieve plates
2. Stamp DNA templates
3. Seal plate
4. Incubate shaking at 30 deg C

### Phase 2 - Quantification Prep

1. Dispense PBS diluent
2. Seal plate
3. Store at 4 deg C

### Phase 3 - LabChip Quantification

1. Unseal plate
2. LabChip quantification
3. Seal plate
4. Store at 4 deg C

## Protocol Parameters

- Payloads & Reagents
- Bravo Stamp
- HiG Centrifuge
- Incubation & Storage

## Ordering

- **Number of Proteins:** configurable
- **Number of Replicates:** configurable
- **File Upload:** CSV, Excel, FASTA, TXT, PDF, ZIP
- **Additional Details:** free-text field for special requirements

## Certification Milestones

- Dry Run Complete
- Wet Run Complete
- Biovalidation Complete
- App Note Complete

## Use Cases

- Screening candidate protein sequences for expressibility
- Go/no-go decisions before investing in optimization
- Evaluating novel constructs in a cell-free system
- Comparing expression levels across sequence variants

---

## Reference: Fluorescent Pixel Art Generation

# Fluorescent Pixel Art Generation

**URL:** https://cloud.ginkgo.bio/protocols/fluorescent-pixel-art-generation
**Status:** Beta
**Price:** $25/plate
**Turnaround:** 5-7 days

## Overview

Transforms a digital image into a living, fluorescent bacterial artwork printed on an agar omni-tray. Customers submit a pixel art design and colors are mapped to distinct fluorescent E. coli strains. Overnight cultures are prepared from frozen glycerol stocks, diluted, and dispensed onto selective LB-chloramphenicol agar plates via Echo acoustic liquid handling at 50 nL per spot. Plates are incubated at 30 deg C for 16 hours, followed by 4 deg C for 12 hours to stabilize colony morphology and fluorescence. High-resolution photographs are captured under UV illumination and delivered digitally.

## Input

- **Image file:** `.png` or `.svg` format
- **Resolution:** 48x48 to 96x96 pixels
- **Color mapping:** Match image colors to the fluorescent strain palette
- **Orientation:** Confirm plate orientation and multi-plate designs (identical vs. distinct)

## Available Fluorescent E. coli Strains (11 colors)

| Strain/Protein | Color |
|---|---|
| sfGFP | Green |
| mRFP | Red |
| mKO2 | Orange |
| Venus | Yellow |
| Azurite | Blue |
| mClover3 | Bright Green |
| mJuniper | Dark Green |
| mTurquoise2 | Cyan |
| Electra2 | Electric Blue |
| mWasabi | Light Green |
| mScarlet-I | Scarlet |

## Output

- **Digital delivery:** High-resolution UV images in TIFF/JPEG format
- **Optional add-ons:** Framed archival prints

## Automated Workflow

### Phase 1 - Source Plate Preparation

1. Shake source plate
2. Centrifuge source plate
3. Peel source plate seal

### Phase 2 - Acoustic Dispensing (per destination plate)

1. Peel destination seal
2. Echo hit-pick dispensing (50 nL per spot)
3. Seal destination plate
4. Shake destination plate
5. Centrifuge destination
6. Store destination at 30 deg C (16 hr incubation)

### Phase 3 - Source Storage

1. Seal source plate
2. Store source plate

### Post-Processing

1. Transfer to 4 deg C for 12 hours (fluorescence stabilization)
2. UV illumination photography
3. Image processing and delivery

## Ordering

- **Number of Plates:** configurable
- **File Upload:** CSV, Excel, FASTA, TXT, PDF, ZIP, PNG, JPG, GIF, SVG, WEBP
- **Additional Details:** free-text field for special requirements

## Certification Milestones

- Dry Run Complete
- Wet Run Complete
- Biovalidation Complete
- App Note Complete

## Use Cases

- Educational outreach and demonstrations
- Unique scientific art and gifts
- Conference displays and promotional materials
- Lab team celebrations
- Visualizing biological art concepts
