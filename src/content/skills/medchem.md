---
title: "Medchem"
description: "Medicinal chemistry filters. Apply drug-likeness rules (Lipinski, Veber), PAINS filters, structural alerts, complexity metrics, for compound prioritization and library filtering."
category: "other"
source: "community"
author: "Community"
tags: ["medchem"]
date: 2026-03-20
---

# Medchem

## Overview

Medchem is a Python library for molecular filtering and prioritization in drug discovery workflows. Apply hundreds of well-established and novel molecular filters, structural alerts, and medicinal chemistry rules to efficiently triage and prioritize compound libraries at scale. Rules and filters are context-specific—use as guidelines combined with domain expertise.

## When to Use This Skill

This skill should be used when:
- Applying drug-likeness rules (Lipinski, Veber, etc.) to compound libraries
- Filtering molecules by structural alerts or PAINS patterns
- Prioritizing compounds for lead optimization
- Assessing compound quality and medicinal chemistry properties
- Detecting reactive or problematic functional groups
- Calculating molecular complexity metrics

## Installation

```bash
uv pip install medchem
```

## Core Capabilities

### 1. Medicinal Chemistry Rules

Apply established drug-likeness rules to molecules using the `medchem.rules` module.

**Available Rules:**
- Rule of Five (Lipinski)
- Rule of Oprea
- Rule of CNS
- Rule of leadlike (soft and strict)
- Rule of three
- Rule of Reos
- Rule of drug
- Rule of Veber
- Golden triangle
- PAINS filters

**Single Rule Application:**

```python
import medchem as mc

# Apply Rule of Five to a SMILES string
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
passes = mc.rules.basic_rules.rule_of_five(smiles)
# Returns: True

# Check specific rules
passes_oprea = mc.rules.basic_rules.rule_of_oprea(smiles)
passes_cns = mc.rules.basic_rules.rule_of_cns(smiles)
```

**Multiple Rules with RuleFilters:**

```python
import datamol as dm
import medchem as mc

# Load molecules
mols = [dm.to_mol(smiles) for smiles in smiles_list]

# Create filter with multiple rules
rfilter = mc.rules.RuleFilters(
    rule_list=[
        "rule_of_five",
        "rule_of_oprea",
        "rule_of_cns",
        "rule_of_leadlike_soft"
    ]
)

# Apply filters with parallelization
results = rfilter(
    mols=mols,
    n_jobs=-1,  # Use all CPU cores
    progress=True
)
```

**Result Format:**
Results are returned as dictionaries with pass/fail status and detailed information for each rule.

### 2. Structural Alert Filters

Detect potentially problematic structural patterns using the `medchem.structural` module.

**Available Filters:**

1. **Common Alerts** - General structural alerts derived from ChEMBL curation and literature
2. **NIBR Filters** - Novartis Institutes for BioMedical Research filter set
3. **Lilly Demerits** - Eli Lilly's demerit-based system (275 rules, molecules rejected at >100 demerits)

**Common Alerts:**

```python
import medchem as mc

# Create filter
alert_filter = mc.structural.CommonAlertsFilters()

# Check single molecule
mol = dm.to_mol("c1ccccc1")
has_alerts, details = alert_filter.check_mol(mol)

# Batch filtering with parallelization
results = alert_filter(
    mols=mol_list,
    n_jobs=-1,
    progress=True
)
```

**NIBR Filters:**

```python
import medchem as mc

# Apply NIBR filters
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1)
```

**Lilly Demerits:**

```python
import medchem as mc

# Calculate Lilly demerits
lilly = mc.structural.LillyDemeritsFilters()
results = lilly(mols=mol_list, n_jobs=-1)

# Each result includes demerit score and whether it passes (≤100 demerits)
```

### 3. Functional API for High-Level Operations

The `medchem.functional` module provides convenient functions for common workflows.

**Quick Filtering:**

```python
import medchem as mc

# Apply NIBR filters to a list
filter_ok = mc.functional.nibr_filter(
    mols=mol_list,
    n_jobs=-1
)

# Apply common alerts
alert_results = mc.functional.common_alerts_filter(
    mols=mol_list,
    n_jobs=-1
)
```

### 4. Chemical Groups Detection

Identify specific chemical groups and functional groups using `medchem.groups`.

**Available Groups:**
- Hinge binders
- Phosphate binders
- Michael acceptors
- Reactive groups
- Custom SMARTS patterns

**Usage:**

```python
import medchem as mc

# Create group detector
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])

# Check for matches
has_matches = group.has_match(mol_list)

# Get detailed match information
matches = group.get_matches(mol)
```

### 5. Named Catalogs

Access curated collections of chemical structures through `medchem.catalogs`.

**Available Catalogs:**
- Functional groups
- Protecting groups
- Common reagents
- Standard fragments

**Usage:**

```python
import medchem as mc

# Access named catalogs
catalogs = mc.catalogs.NamedCatalogs

# Use catalog for matching
catalog = catalogs.get("functional_groups")
matches = catalog.get_matches(mol)
```

### 6. Molecular Complexity

Calculate complexity metrics that approximate synthetic accessibility using `medchem.complexity`.

**Common Metrics:**
- Bertz complexity
- Whitlock complexity
- Barone complexity

**Usage:**

```python
import medchem as mc

# Calculate complexity
complexity_score = mc.complexity.calculate_complexity(mol)

# Filter by complexity threshold
complex_filter = mc.complexity.ComplexityFilter(max_complexity=500)
results = complex_filter(mols=mol_list)
```

### 7. Constraints Filtering

Apply custom property-based constraints using `medchem.constraints`.

**Example Constraints:**
- Molecular weight ranges
- LogP bounds
- TPSA limits
- Rotatable bond counts

**Usage:**

```python
import medchem as mc

# Define constraints
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140,
    rotatable_bonds_max=10
)

# Apply constraints
results = constraints(mols=mol_list, n_jobs=-1)
```

### 8. Medchem Query Language

Use a specialized query language for complex filtering criteria.

**Query Examples:**
```
# Molecules passing Ro5 AND not having common alerts
"rule_of_five AND NOT common_alerts"

# CNS-like molecules with low complexity
"rule_of_cns AND complexity < 400"

# Leadlike molecules without Lilly demerits
"rule_of_leadlike AND lilly_demerits == 0"
```

**Usage:**

```python
import medchem as mc

# Parse and apply query
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
```

## Workflow Patterns

### Pattern 1: Initial Triage of Compound Library

Filter a large compound collection to identify drug-like candidates.

```python
import datamol as dm
import medchem as mc
import pandas as pd

# Load compound library
df = pd.read_csv("compounds.csv")
mols = [dm.to_mol(smi) for smi in df["smiles"]]

# Apply primary filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_veber"])
rule_results = rule_filter(mols=mols, n_jobs=-1, progress=True)

# Apply structural alerts
alert_filter = mc.structural.CommonAlertsFilters()
alert_results = alert_filter(mols=mols, n_jobs=-1, progress=True)

# Combine results
df["passes_rules"] = rule_results["pass"]
df["has_alerts"] = alert_results["has_alerts"]
df["drug_like"] = df["passes_rules"] & ~df["has_alerts"]

# Save filtered compounds
filtered_df = df[df["drug_like"]]
filtered_df.to_csv("filtered_compounds.csv", index=False)
```

### Pattern 2: Lead Optimization Filtering

Apply stricter criteria during lead optimization.

```python
import medchem as mc

# Create comprehensive filter
filters = {
    "rules": mc.rules.RuleFilters(rule_list=["rule_of_leadlike_strict"]),
    "alerts": mc.structural.NIBRFilters(),
    "lilly": mc.structural.LillyDemeritsFilters(),
    "complexity": mc.complexity.ComplexityFilter(max_complexity=400)
}

# Apply all filters
results = {}
for name, filt in filters.items():
    results[name] = filt(mols=candidate_mols, n_jobs=-1)

# Identify compounds passing all filters
passes_all = all(r["pass"] for r in results.values())
```

### Pattern 3: Identify Specific Chemical Groups

Find molecules containing specific functional groups or scaffolds.

```python
import medchem as mc

# Create group detector for multiple groups
group_detector = mc.groups.ChemicalGroup(
    groups=["hinge_binders", "phosphate_binders"]
)

# Screen library
matches = group_detector.get_all_matches(mol_list)

# Filter molecules with desired groups
mol_with_groups = [mol for mol, match in zip(mol_list, matches) if match]
```

## Best Practices

1. **Context Matters**: Don't blindly apply filters. Understand the biological target and chemical space.

2. **Combine Multiple Filters**: Use rules, structural alerts, and domain knowledge together for better decisions.

3. **Use Parallelization**: For large datasets (>1000 molecules), always use `n_jobs=-1` for parallel processing.

4. **Iterative Refinement**: Start with broad filters (Ro5), then apply more specific criteria (CNS, leadlike) as needed.

5. **Document Filtering Decisions**: Track which molecules were filtered out and why for reproducibility.

6. **Validate Results**: Remember that marketed drugs often fail standard filters—use these as guidelines, not absolute rules.

7. **Consider Prodrugs**: Molecules designed as prodrugs may intentionally violate standard medicinal chemistry rules.

## Resources

### references/api_guide.md
Comprehensive API reference covering all medchem modules with detailed function signatures, parameters, and return types.

### references/rules_catalog.md
Complete catalog of available rules, filters, and alerts with descriptions, thresholds, and literature references.

### scripts/filter_molecules.py
Production-ready script for batch filtering workflows. Supports multiple input formats (CSV, SDF, SMILES), configurable filter combinations, and detailed reporting.

**Usage:**
```bash
python scripts/filter_molecules.py input.csv --rules rule_of_five,rule_of_cns --alerts nibr --output filtered.csv
```

## Documentation

Official documentation: https://medchem-docs.datamol.io/
GitHub repository: https://github.com/datamol-io/medchem

---

## Reference: Api_Guide

# Medchem API Reference

Comprehensive reference for all medchem modules and functions.

## Module: medchem.rules

### Class: RuleFilters

Filter molecules based on multiple medicinal chemistry rules.

**Constructor:**
```python
RuleFilters(rule_list: List[str])
```

**Parameters:**
- `rule_list`: List of rule names to apply. See available rules below.

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> Dict
```
- `mols`: List of RDKit molecule objects
- `n_jobs`: Number of parallel jobs (-1 uses all cores)
- `progress`: Show progress bar
- **Returns**: Dictionary with results for each rule

**Example:**
```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_cns"])
results = rfilter(mols=mol_list, n_jobs=-1, progress=True)
```

### Module: medchem.rules.basic_rules

Individual rule functions that can be applied to single molecules.

#### rule_of_five()

```python
rule_of_five(mol: Union[str, Chem.Mol]) -> bool
```

Lipinski's Rule of Five for oral bioavailability.

**Criteria:**
- Molecular weight ≤ 500 Da
- LogP ≤ 5
- H-bond donors ≤ 5
- H-bond acceptors ≤ 10

**Parameters:**
- `mol`: SMILES string or RDKit molecule object

**Returns:** True if molecule passes all criteria

#### rule_of_three()

```python
rule_of_three(mol: Union[str, Chem.Mol]) -> bool
```

Rule of Three for fragment screening libraries.

**Criteria:**
- Molecular weight ≤ 300 Da
- LogP ≤ 3
- H-bond donors ≤ 3
- H-bond acceptors ≤ 3
- Rotatable bonds ≤ 3
- Polar surface area ≤ 60 Ų

#### rule_of_oprea()

```python
rule_of_oprea(mol: Union[str, Chem.Mol]) -> bool
```

Oprea's lead-like criteria for hit-to-lead optimization.

**Criteria:**
- Molecular weight: 200-350 Da
- LogP: -2 to 4
- Rotatable bonds ≤ 7
- Rings ≤ 4

#### rule_of_cns()

```python
rule_of_cns(mol: Union[str, Chem.Mol]) -> bool
```

CNS drug-likeness rules.

**Criteria:**
- Molecular weight ≤ 450 Da
- LogP: -1 to 5
- H-bond donors ≤ 2
- TPSA ≤ 90 Ų

#### rule_of_leadlike_soft()

```python
rule_of_leadlike_soft(mol: Union[str, Chem.Mol]) -> bool
```

Soft lead-like criteria (more permissive).

**Criteria:**
- Molecular weight: 250-450 Da
- LogP: -3 to 4
- Rotatable bonds ≤ 10

#### rule_of_leadlike_strict()

```python
rule_of_leadlike_strict(mol: Union[str, Chem.Mol]) -> bool
```

Strict lead-like criteria (more restrictive).

**Criteria:**
- Molecular weight: 200-350 Da
- LogP: -2 to 3.5
- Rotatable bonds ≤ 7
- Rings: 1-3

#### rule_of_veber()

```python
rule_of_veber(mol: Union[str, Chem.Mol]) -> bool
```

Veber's rules for oral bioavailability.

**Criteria:**
- Rotatable bonds ≤ 10
- TPSA ≤ 140 Ų

#### rule_of_reos()

```python
rule_of_reos(mol: Union[str, Chem.Mol]) -> bool
```

Rapid Elimination Of Swill (REOS) filter.

**Criteria:**
- Molecular weight: 200-500 Da
- LogP: -5 to 5
- H-bond donors: 0-5
- H-bond acceptors: 0-10

#### rule_of_drug()

```python
rule_of_drug(mol: Union[str, Chem.Mol]) -> bool
```

Combined drug-likeness criteria.

**Criteria:**
- Passes Rule of Five
- Passes Veber rules
- No PAINS substructures

#### golden_triangle()

```python
golden_triangle(mol: Union[str, Chem.Mol]) -> bool
```

Golden Triangle for drug-likeness balance.

**Criteria:**
- 200 ≤ MW ≤ 50×LogP + 400
- LogP: -2 to 5

#### pains_filter()

```python
pains_filter(mol: Union[str, Chem.Mol]) -> bool
```

Pan Assay INterference compoundS (PAINS) filter.

**Returns:** True if molecule does NOT contain PAINS substructures

---

## Module: medchem.structural

### Class: CommonAlertsFilters

Filter for common structural alerts derived from ChEMBL and literature.

**Constructor:**
```python
CommonAlertsFilters()
```

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[Dict]
```

Apply common alerts filter to a list of molecules.

**Returns:** List of dictionaries with keys:
- `has_alerts`: Boolean indicating if molecule has alerts
- `alert_details`: List of matched alert patterns
- `num_alerts`: Number of alerts found

```python
check_mol(mol: Chem.Mol) -> Tuple[bool, List[str]]
```

Check a single molecule for structural alerts.

**Returns:** Tuple of (has_alerts, list_of_alert_names)

### Class: NIBRFilters

Novartis NIBR medicinal chemistry filters.

**Constructor:**
```python
NIBRFilters()
```

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[bool]
```

Apply NIBR filters to molecules.

**Returns:** List of booleans (True if molecule passes)

### Class: LillyDemeritsFilters

Eli Lilly's demerit-based structural alert system (275 rules).

**Constructor:**
```python
LillyDemeritsFilters()
```

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[Dict]
```

Calculate Lilly demerits for molecules.

**Returns:** List of dictionaries with keys:
- `demerits`: Total demerit score
- `passes`: Boolean (True if demerits ≤ 100)
- `matched_patterns`: List of matched patterns with scores

---

## Module: medchem.functional

High-level functional API for common operations.

### nibr_filter()

```python
nibr_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

Apply NIBR filters using functional API.

**Parameters:**
- `mols`: List of molecules
- `n_jobs`: Parallelization level

**Returns:** List of pass/fail booleans

### common_alerts_filter()

```python
common_alerts_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

Apply common alerts filter using functional API.

**Returns:** List of results dictionaries

### lilly_demerits_filter()

```python
lilly_demerits_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

Calculate Lilly demerits using functional API.

---

## Module: medchem.groups

### Class: ChemicalGroup

Detect specific chemical groups in molecules.

**Constructor:**
```python
ChemicalGroup(groups: List[str], custom_smarts: Optional[Dict[str, str]] = None)
```

**Parameters:**
- `groups`: List of predefined group names
- `custom_smarts`: Dictionary mapping custom group names to SMARTS patterns

**Predefined Groups:**
- `"hinge_binders"`: Kinase hinge binding motifs
- `"phosphate_binders"`: Phosphate binding groups
- `"michael_acceptors"`: Michael acceptor electrophiles
- `"reactive_groups"`: General reactive functionalities

**Methods:**

```python
has_match(mols: List[Chem.Mol]) -> List[bool]
```

Check if molecules contain any of the specified groups.

```python
get_matches(mol: Chem.Mol) -> Dict[str, List[Tuple]]
```

Get detailed match information for a single molecule.

**Returns:** Dictionary mapping group names to lists of atom indices

```python
get_all_matches(mols: List[Chem.Mol]) -> List[Dict]
```

Get match information for all molecules.

**Example:**
```python
group = mc.groups.ChemicalGroup(groups=["hinge_binders", "phosphate_binders"])
matches = group.get_all_matches(mol_list)
```

---

## Module: medchem.catalogs

### Class: NamedCatalogs

Access to curated chemical catalogs.

**Available Catalogs:**
- `"functional_groups"`: Common functional groups
- `"protecting_groups"`: Protecting group structures
- `"reagents"`: Common reagents
- `"fragments"`: Standard fragments

**Usage:**
```python
catalog = mc.catalogs.NamedCatalogs.get("functional_groups")
matches = catalog.get_matches(mol)
```

---

## Module: medchem.complexity

Calculate molecular complexity metrics.

### calculate_complexity()

```python
calculate_complexity(mol: Chem.Mol, method: str = "bertz") -> float
```

Calculate complexity score for a molecule.

**Parameters:**
- `mol`: RDKit molecule
- `method`: Complexity metric ("bertz", "whitlock", "barone")

**Returns:** Complexity score (higher = more complex)

### Class: ComplexityFilter

Filter molecules by complexity threshold.

**Constructor:**
```python
ComplexityFilter(max_complexity: float, method: str = "bertz")
```

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

Filter molecules exceeding complexity threshold.

---

## Module: medchem.constraints

### Class: Constraints

Apply custom property-based constraints.

**Constructor:**
```python
Constraints(
    mw_range: Optional[Tuple[float, float]] = None,
    logp_range: Optional[Tuple[float, float]] = None,
    tpsa_max: Optional[float] = None,
    tpsa_range: Optional[Tuple[float, float]] = None,
    hbd_max: Optional[int] = None,
    hba_max: Optional[int] = None,
    rotatable_bonds_max: Optional[int] = None,
    rings_range: Optional[Tuple[int, int]] = None,
    aromatic_rings_max: Optional[int] = None,
)
```

**Parameters:** All parameters are optional. Specify only the constraints needed.

**Methods:**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

Apply constraints to molecules.

**Returns:** List of dictionaries with keys:
- `passes`: Boolean indicating if all constraints pass
- `violations`: List of constraint names that failed

**Example:**
```python
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140
)
results = constraints(mols=mol_list, n_jobs=-1)
```

---

## Module: medchem.query

Query language for complex filtering.

### parse()

```python
parse(query: str) -> Query
```

Parse a medchem query string into a Query object.

**Query Syntax:**
- Operators: `AND`, `OR`, `NOT`
- Comparisons: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Properties: `complexity`, `lilly_demerits`, `mw`, `logp`, `tpsa`
- Rules: `rule_of_five`, `rule_of_cns`, etc.
- Filters: `common_alerts`, `nibr_filter`, `pains_filter`

**Example Queries:**
```python
"rule_of_five AND NOT common_alerts"
"rule_of_cns AND complexity < 400"
"mw > 200 AND mw < 500 AND logp < 5"
"(rule_of_five OR rule_of_oprea) AND NOT pains_filter"
```

### Class: Query

**Methods:**

```python
apply(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

Apply parsed query to molecules.

**Example:**
```python
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
passing_mols = [mol for mol, passes in zip(mol_list, results) if passes]
```

---

## Module: medchem.utils

Utility functions for working with molecules.

### batch_process()

```python
batch_process(
    mols: List[Chem.Mol],
    func: Callable,
    n_jobs: int = 1,
    progress: bool = False,
    batch_size: Optional[int] = None
) -> List
```

Process molecules in parallel batches.

**Parameters:**
- `mols`: List of molecules
- `func`: Function to apply to each molecule
- `n_jobs`: Number of parallel workers
- `progress`: Show progress bar
- `batch_size`: Size of processing batches

### standardize_mol()

```python
standardize_mol(mol: Chem.Mol) -> Chem.Mol
```

Standardize molecule representation (sanitize, neutralize charges, etc.).

---

## Common Patterns

### Pattern: Parallel Processing

All filters support parallelization:

```python
# Use all CPU cores
results = filter_object(mols=mol_list, n_jobs=-1, progress=True)

# Use specific number of cores
results = filter_object(mols=mol_list, n_jobs=4, progress=True)
```

### Pattern: Combining Multiple Filters

```python
import medchem as mc

# Apply multiple filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five"])
alert_filter = mc.structural.CommonAlertsFilters()
lilly_filter = mc.structural.LillyDemeritsFilters()

# Get results
rule_results = rule_filter(mols=mol_list, n_jobs=-1)
alert_results = alert_filter(mols=mol_list, n_jobs=-1)
lilly_results = lilly_filter(mols=mol_list, n_jobs=-1)

# Combine criteria
passing_mols = [
    mol for i, mol in enumerate(mol_list)
    if rule_results[i]["passes"]
    and not alert_results[i]["has_alerts"]
    and lilly_results[i]["passes"]
]
```

### Pattern: Working with DataFrames

```python
import pandas as pd
import datamol as dm
import medchem as mc

# Load data
df = pd.read_csv("molecules.csv")
df["mol"] = df["smiles"].apply(dm.to_mol)

# Apply filters
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_cns"])
results = rfilter(mols=df["mol"].tolist(), n_jobs=-1)

# Add results to dataframe
df["passes_ro5"] = [r["rule_of_five"] for r in results]
df["passes_cns"] = [r["rule_of_cns"] for r in results]

# Filter dataframe
filtered_df = df[df["passes_ro5"] & df["passes_cns"]]
```

---

## Reference: Rules_Catalog

# Medchem Rules and Filters Catalog

Comprehensive catalog of all available medicinal chemistry rules, structural alerts, and filters in medchem.

## Table of Contents

1. [Drug-Likeness Rules](#drug-likeness-rules)
2. [Lead-Likeness Rules](#lead-likeness-rules)
3. [Fragment Rules](#fragment-rules)
4. [CNS Rules](#cns-rules)
5. [Structural Alert Filters](#structural-alert-filters)
6. [Chemical Group Patterns](#chemical-group-patterns)

---

## Drug-Likeness Rules

### Rule of Five (Lipinski)

**Reference:** Lipinski et al., Adv Drug Deliv Rev (1997) 23:3-25

**Purpose:** Predict oral bioavailability

**Criteria:**
- Molecular Weight ≤ 500 Da
- LogP ≤ 5
- Hydrogen Bond Donors ≤ 5
- Hydrogen Bond Acceptors ≤ 10

**Usage:**
```python
mc.rules.basic_rules.rule_of_five(mol)
```

**Notes:**
- One of the most widely used filters in drug discovery
- About 90% of orally active drugs comply with these rules
- Exceptions exist, especially for natural products and antibiotics

---

### Rule of Veber

**Reference:** Veber et al., J Med Chem (2002) 45:2615-2623

**Purpose:** Additional criteria for oral bioavailability

**Criteria:**
- Rotatable Bonds ≤ 10
- Topological Polar Surface Area (TPSA) ≤ 140 Ų

**Usage:**
```python
mc.rules.basic_rules.rule_of_veber(mol)
```

**Notes:**
- Complements Rule of Five
- TPSA correlates with cell permeability
- Rotatable bonds affect molecular flexibility

---

### Rule of Drug

**Purpose:** Combined drug-likeness assessment

**Criteria:**
- Passes Rule of Five
- Passes Veber rules
- Does not contain PAINS substructures

**Usage:**
```python
mc.rules.basic_rules.rule_of_drug(mol)
```

---

### REOS (Rapid Elimination Of Swill)

**Reference:** Walters & Murcko, Adv Drug Deliv Rev (2002) 54:255-271

**Purpose:** Filter out compounds unlikely to be drugs

**Criteria:**
- Molecular Weight: 200-500 Da
- LogP: -5 to 5
- Hydrogen Bond Donors: 0-5
- Hydrogen Bond Acceptors: 0-10

**Usage:**
```python
mc.rules.basic_rules.rule_of_reos(mol)
```

---

### Golden Triangle

**Reference:** Johnson et al., J Med Chem (2009) 52:5487-5500

**Purpose:** Balance lipophilicity and molecular weight

**Criteria:**
- 200 ≤ MW ≤ 50 × LogP + 400
- LogP: -2 to 5

**Usage:**
```python
mc.rules.basic_rules.golden_triangle(mol)
```

**Notes:**
- Defines optimal physicochemical space
- Visual representation resembles a triangle on MW vs LogP plot

---

## Lead-Likeness Rules

### Rule of Oprea

**Reference:** Oprea et al., J Chem Inf Comput Sci (2001) 41:1308-1315

**Purpose:** Identify lead-like compounds for optimization

**Criteria:**
- Molecular Weight: 200-350 Da
- LogP: -2 to 4
- Rotatable Bonds ≤ 7
- Number of Rings ≤ 4

**Usage:**
```python
mc.rules.basic_rules.rule_of_oprea(mol)
```

**Rationale:** Lead compounds should have "room to grow" during optimization

---

### Rule of Leadlike (Soft)

**Purpose:** Permissive lead-like criteria

**Criteria:**
- Molecular Weight: 250-450 Da
- LogP: -3 to 4
- Rotatable Bonds ≤ 10

**Usage:**
```python
mc.rules.basic_rules.rule_of_leadlike_soft(mol)
```

---

### Rule of Leadlike (Strict)

**Purpose:** Restrictive lead-like criteria

**Criteria:**
- Molecular Weight: 200-350 Da
- LogP: -2 to 3.5
- Rotatable Bonds ≤ 7
- Number of Rings: 1-3

**Usage:**
```python
mc.rules.basic_rules.rule_of_leadlike_strict(mol)
```

---

## Fragment Rules

### Rule of Three

**Reference:** Congreve et al., Drug Discov Today (2003) 8:876-877

**Purpose:** Screen fragment libraries for fragment-based drug discovery

**Criteria:**
- Molecular Weight ≤ 300 Da
- LogP ≤ 3
- Hydrogen Bond Donors ≤ 3
- Hydrogen Bond Acceptors ≤ 3
- Rotatable Bonds ≤ 3
- Polar Surface Area ≤ 60 Ų

**Usage:**
```python
mc.rules.basic_rules.rule_of_three(mol)
```

**Notes:**
- Fragments are grown into leads during optimization
- Lower complexity allows more starting points

---

## CNS Rules

### Rule of CNS

**Purpose:** Central nervous system drug-likeness

**Criteria:**
- Molecular Weight ≤ 450 Da
- LogP: -1 to 5
- Hydrogen Bond Donors ≤ 2
- TPSA ≤ 90 Ų

**Usage:**
```python
mc.rules.basic_rules.rule_of_cns(mol)
```

**Rationale:**
- Blood-brain barrier penetration requires specific properties
- Lower TPSA and HBD count improve BBB permeability
- Tight constraints reflect CNS challenges

---

## Structural Alert Filters

### PAINS (Pan Assay INterference compoundS)

**Reference:** Baell & Holloway, J Med Chem (2010) 53:2719-2740

**Purpose:** Identify compounds that interfere with assays

**Categories:**
- Catechols
- Quinones
- Rhodanines
- Hydroxyphenylhydrazones
- Alkyl/aryl aldehydes
- Michael acceptors (specific patterns)

**Usage:**
```python
mc.rules.basic_rules.pains_filter(mol)
# Returns True if NO PAINS found
```

**Notes:**
- PAINS compounds show activity in multiple assays through non-specific mechanisms
- Common false positives in screening campaigns
- Should be deprioritized in lead selection

---

### Common Alerts Filters

**Source:** Derived from ChEMBL curation and medicinal chemistry literature

**Purpose:** Flag common problematic structural patterns

**Alert Categories:**
1. **Reactive Groups**
   - Epoxides
   - Aziridines
   - Acid halides
   - Isocyanates

2. **Metabolic Liabilities**
   - Hydrazines
   - Thioureas
   - Anilines (certain patterns)

3. **Aggregators**
   - Polyaromatic systems
   - Long aliphatic chains

4. **Toxicophores**
   - Nitro aromatics
   - Aromatic N-oxides
   - Certain heterocycles

**Usage:**
```python
alert_filter = mc.structural.CommonAlertsFilters()
has_alerts, details = alert_filter.check_mol(mol)
```

**Return Format:**
```python
{
    "has_alerts": True,
    "alert_details": ["reactive_epoxide", "metabolic_hydrazine"],
    "num_alerts": 2
}
```

---

### NIBR Filters

**Source:** Novartis Institutes for BioMedical Research

**Purpose:** Industrial medicinal chemistry filtering rules

**Features:**
- Proprietary filter set developed from Novartis experience
- Balances drug-likeness with practical medicinal chemistry
- Includes both structural alerts and property filters

**Usage:**
```python
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1)
```

**Return Format:** Boolean list (True = passes)

---

### Lilly Demerits Filter

**Reference:** Based on Eli Lilly medicinal chemistry rules

**Source:** 275 structural patterns accumulated over 18 years

**Purpose:** Identify assay interference and problematic functionalities

**Mechanism:**
- Each matched pattern adds demerits
- Molecules with >100 demerits are rejected
- Some patterns add 10-50 demerits, others add 100+ (instant rejection)

**Demerit Categories:**

1. **High Demerits (>50):**
   - Known toxic groups
   - Highly reactive functionalities
   - Strong metal chelators

2. **Medium Demerits (20-50):**
   - Metabolic liabilities
   - Aggregation-prone structures
   - Frequent hitters

3. **Low Demerits (5-20):**
   - Minor concerns
   - Context-dependent issues

**Usage:**
```python
lilly_filter = mc.structural.LillyDemeritsFilters()
results = lilly_filter(mols=mol_list, n_jobs=-1)
```

**Return Format:**
```python
{
    "demerits": 35,
    "passes": True,  # (demerits ≤ 100)
    "matched_patterns": [
        {"pattern": "phenolic_ester", "demerits": 20},
        {"pattern": "aniline_derivative", "demerits": 15}
    ]
}
```

---

## Chemical Group Patterns

### Hinge Binders

**Purpose:** Identify kinase hinge-binding motifs

**Common Patterns:**
- Aminopyridines
- Aminopyrimidines
- Indazoles
- Benzimidazoles

**Usage:**
```python
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])
has_hinge = group.has_match(mol_list)
```

**Application:** Kinase inhibitor design

---

### Phosphate Binders

**Purpose:** Identify phosphate-binding groups

**Common Patterns:**
- Basic amines in specific geometries
- Guanidinium groups
- Arginine mimetics

**Usage:**
```python
group = mc.groups.ChemicalGroup(groups=["phosphate_binders"])
```

**Application:** Kinase inhibitors, phosphatase inhibitors

---

### Michael Acceptors

**Purpose:** Identify electrophilic Michael acceptor groups

**Common Patterns:**
- α,β-Unsaturated carbonyls
- α,β-Unsaturated nitriles
- Vinyl sulfones
- Acrylamides

**Usage:**
```python
group = mc.groups.ChemicalGroup(groups=["michael_acceptors"])
```

**Notes:**
- Can be desirable for covalent inhibitors
- Often flagged as reactive alerts in screening

---

### Reactive Groups

**Purpose:** Identify generally reactive functionalities

**Common Patterns:**
- Epoxides
- Aziridines
- Acyl halides
- Isocyanates
- Sulfonyl chlorides

**Usage:**
```python
group = mc.groups.ChemicalGroup(groups=["reactive_groups"])
```

---

## Custom SMARTS Patterns

Define custom structural patterns using SMARTS:

```python
custom_patterns = {
    "my_warhead": "[C;H0](=O)C(F)(F)F",  # Trifluoromethyl ketone
    "my_scaffold": "c1ccc2c(c1)ncc(n2)N",  # Aminobenzimidazole
}

group = mc.groups.ChemicalGroup(
    groups=["hinge_binders"],
    custom_smarts=custom_patterns
)
```

---

## Filter Selection Guidelines

### Initial Screening (High-Throughput)

Recommended filters:
- Rule of Five
- PAINS filter
- Common Alerts (permissive settings)

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "pains_filter"])
alert_filter = mc.structural.CommonAlertsFilters()
```

---

### Hit-to-Lead

Recommended filters:
- Rule of Oprea or Leadlike (soft)
- NIBR filters
- Lilly Demerits

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_oprea"])
nibr_filter = mc.structural.NIBRFilters()
lilly_filter = mc.structural.LillyDemeritsFilters()
```

---

### Lead Optimization

Recommended filters:
- Rule of Drug
- Leadlike (strict)
- Full structural alert analysis
- Complexity filters

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_drug", "rule_of_leadlike_strict"])
alert_filter = mc.structural.CommonAlertsFilters()
complexity_filter = mc.complexity.ComplexityFilter(max_complexity=400)
```

---

### CNS Targets

Recommended filters:
- Rule of CNS
- Reduced PAINS criteria (CNS-focused)
- BBB permeability constraints

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_cns"])
constraints = mc.constraints.Constraints(
    tpsa_max=90,
    hbd_max=2,
    mw_range=(300, 450)
)
```

---

### Fragment-Based Drug Discovery

Recommended filters:
- Rule of Three
- Minimal complexity
- Basic reactive group check

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_three"])
complexity_filter = mc.complexity.ComplexityFilter(max_complexity=250)
```

---

## Important Considerations

### False Positives and False Negatives

**Filters are guidelines, not absolutes:**

1. **False Positives** (good drugs flagged):
   - ~10% of marketed drugs fail Rule of Five
   - Natural products often violate standard rules
   - Prodrugs intentionally break rules
   - Antibiotics and antivirals frequently non-compliant

2. **False Negatives** (bad compounds passing):
   - Passing filters doesn't guarantee success
   - Target-specific issues not captured
   - In vivo properties not fully predicted

### Context-Specific Application

**Different contexts require different criteria:**

- **Target Class:** Kinases vs GPCRs vs ion channels have different optimal spaces
- **Modality:** Small molecules vs PROTACs vs molecular glues
- **Administration Route:** Oral vs IV vs topical
- **Disease Area:** CNS vs oncology vs infectious disease
- **Stage:** Screening vs hit-to-lead vs lead optimization

### Complementing with Machine Learning

Modern approaches combine rules with ML:

```python
# Rule-based pre-filtering
rule_results = mc.rules.RuleFilters(rule_list=["rule_of_five"])(mols)
filtered_mols = [mol for mol, r in zip(mols, rule_results) if r["passes"]]

# ML model scoring on filtered set
ml_scores = ml_model.predict(filtered_mols)

# Combined decision
final_candidates = [
    mol for mol, score in zip(filtered_mols, ml_scores)
    if score > threshold
]
```

---

## References

1. Lipinski CA et al. Adv Drug Deliv Rev (1997) 23:3-25
2. Veber DF et al. J Med Chem (2002) 45:2615-2623
3. Oprea TI et al. J Chem Inf Comput Sci (2001) 41:1308-1315
4. Congreve M et al. Drug Discov Today (2003) 8:876-877
5. Baell JB & Holloway GA. J Med Chem (2010) 53:2719-2740
6. Johnson TW et al. J Med Chem (2009) 52:5487-5500
7. Walters WP & Murcko MA. Adv Drug Deliv Rev (2002) 54:255-271
8. Hann MM & Oprea TI. Curr Opin Chem Biol (2004) 8:255-263
9. Rishton GM. Drug Discov Today (1997) 2:382-384
