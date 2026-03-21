---
title: "Brenda Database"
description: "Access BRENDA enzyme database via SOAP API. Retrieve kinetic parameters (Km, kcat), reaction equations, organism data, and substrate-specific enzyme information for biochemical research and metabolic pathway analysis."
category: "research"
source: "community"
author: "Community"
tags: ["brenda", "database"]
date: 2026-03-20
---

# BRENDA Database

## Overview

BRENDA (BRaunschweig ENzyme DAtabase) is the world's most comprehensive enzyme information system, containing detailed enzyme data from scientific literature. Query kinetic parameters (Km, kcat), reaction equations, substrate specificities, organism information, and optimal conditions for enzymes using the official SOAP API. Access over 45,000 enzymes with millions of kinetic data points for biochemical research, metabolic engineering, and enzyme discovery.

## When to Use This Skill

This skill should be used when:
- Searching for enzyme kinetic parameters (Km, kcat, Vmax)
- Retrieving reaction equations and stoichiometry
- Finding enzymes for specific substrates or reactions
- Comparing enzyme properties across different organisms
- Investigating optimal pH, temperature, and conditions
- Accessing enzyme inhibition and activation data
- Supporting metabolic pathway reconstruction and retrosynthesis
- Performing enzyme engineering and optimization studies
- Analyzing substrate specificity and cofactor requirements

## Core Capabilities

### 1. Kinetic Parameter Retrieval

Access comprehensive kinetic data for enzymes:

**Get Km Values by EC Number**:
```python
from brenda_client import get_km_values

# Get Km values for all organisms
km_data = get_km_values("1.1.1.1")  # Alcohol dehydrogenase

# Get Km values for specific organism
km_data = get_km_values("1.1.1.1", organism="Saccharomyces cerevisiae")

# Get Km values for specific substrate
km_data = get_km_values("1.1.1.1", substrate="ethanol")
```

**Parse Km Results**:
```python
for entry in km_data:
    print(f"Km: {entry}")
    # Example output: "organism*Homo sapiens#substrate*ethanol#kmValue*1.2#commentary*"
```

**Extract Specific Information**:
```python
from scripts.brenda_queries import parse_km_entry, extract_organism_data

for entry in km_data:
    parsed = parse_km_entry(entry)
    organism = extract_organism_data(entry)
    print(f"Organism: {parsed['organism']}")
    print(f"Substrate: {parsed['substrate']}")
    print(f"Km value: {parsed['km_value']}")
    print(f"pH: {parsed.get('ph', 'N/A')}")
    print(f"Temperature: {parsed.get('temperature', 'N/A')}")
```

### 2. Reaction Information

Retrieve reaction equations and details:

**Get Reactions by EC Number**:
```python
from brenda_client import get_reactions

# Get all reactions for EC number
reactions = get_reactions("1.1.1.1")

# Filter by organism
reactions = get_reactions("1.1.1.1", organism="Escherichia coli")

# Search specific reaction
reactions = get_reactions("1.1.1.1", reaction="ethanol + NAD+")
```

**Process Reaction Data**:
```python
from scripts.brenda_queries import parse_reaction_entry, extract_substrate_products

for reaction in reactions:
    parsed = parse_reaction_entry(reaction)
    substrates, products = extract_substrate_products(reaction)

    print(f"Reaction: {parsed['reaction']}")
    print(f"Organism: {parsed['organism']}")
    print(f"Substrates: {substrates}")
    print(f"Products: {products}")
```

### 3. Enzyme Discovery

Find enzymes for specific biochemical transformations:

**Find Enzymes by Substrate**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate

# Find enzymes that act on glucose
enzymes = search_enzymes_by_substrate("glucose", limit=20)

for enzyme in enzymes:
    print(f"EC: {enzyme['ec_number']}")
    print(f"Name: {enzyme['enzyme_name']}")
    print(f"Reaction: {enzyme['reaction']}")
```

**Find Enzymes by Product**:
```python
from scripts.brenda_queries import search_enzymes_by_product

# Find enzymes that produce lactate
enzymes = search_enzymes_by_product("lactate", limit=10)
```

**Search by Reaction Pattern**:
```python
from scripts.brenda_queries import search_by_pattern

# Find oxidation reactions
enzymes = search_by_pattern("oxidation", limit=15)
```

### 4. Organism-Specific Enzyme Data

Compare enzyme properties across organisms:

**Get Enzyme Data for Multiple Organisms**:
```python
from scripts.brenda_queries import compare_across_organisms

organisms = ["Escherichia coli", "Saccharomyces cerevisiae", "Homo sapiens"]
comparison = compare_across_organisms("1.1.1.1", organisms)

for org_data in comparison:
    print(f"Organism: {org_data['organism']}")
    print(f"Avg Km: {org_data['average_km']}")
    print(f"Optimal pH: {org_data['optimal_ph']}")
    print(f"Temperature range: {org_data['temperature_range']}")
```

**Find Organisms with Specific Enzyme**:
```python
from scripts.brenda_queries import get_organisms_for_enzyme

organisms = get_organisms_for_enzyme("6.3.5.5")  # Glutamine synthetase
print(f"Found {len(organisms)} organisms with this enzyme")
```

### 5. Environmental Parameters

Access optimal conditions and environmental parameters:

**Get pH and Temperature Data**:
```python
from scripts.brenda_queries import get_environmental_parameters

params = get_environmental_parameters("1.1.1.1")

print(f"Optimal pH range: {params['ph_range']}")
print(f"Optimal temperature: {params['optimal_temperature']}")
print(f"Stability pH: {params['stability_ph']}")
print(f"Temperature stability: {params['temperature_stability']}")
```

**Cofactor Requirements**:
```python
from scripts.brenda_queries import get_cofactor_requirements

cofactors = get_cofactor_requirements("1.1.1.1")
for cofactor in cofactors:
    print(f"Cofactor: {cofactor['name']}")
    print(f"Type: {cofactor['type']}")
    print(f"Concentration: {cofactor['concentration']}")
```

### 6. Substrate Specificity

Analyze enzyme substrate preferences:

**Get Substrate Specificity Data**:
```python
from scripts.brenda_queries import get_substrate_specificity

specificity = get_substrate_specificity("1.1.1.1")

for substrate in specificity:
    print(f"Substrate: {substrate['name']}")
    print(f"Km: {substrate['km']}")
    print(f"Vmax: {substrate['vmax']}")
    print(f"kcat: {substrate['kcat']}")
    print(f"Specificity constant: {substrate['kcat_km_ratio']}")
```

**Compare Substrate Preferences**:
```python
from scripts.brenda_queries import compare_substrate_affinity

comparison = compare_substrate_affinity("1.1.1.1")
sorted_by_km = sorted(comparison, key=lambda x: x['km'])

for substrate in sorted_by_km[:5]:  # Top 5 lowest Km
    print(f"{substrate['name']}: Km = {substrate['km']}")
```

### 7. Inhibition and Activation

Access enzyme regulation data:

**Get Inhibitor Information**:
```python
from scripts.brenda_queries import get_inhibitors

inhibitors = get_inhibitors("1.1.1.1")

for inhibitor in inhibitors:
    print(f"Inhibitor: {inhibitor['name']}")
    print(f"Type: {inhibitor['type']}")
    print(f"Ki: {inhibitor['ki']}")
    print(f"IC50: {inhibitor['ic50']}")
```

**Get Activator Information**:
```python
from scripts.brenda_queries import get_activators

activators = get_activators("1.1.1.1")

for activator in activators:
    print(f"Activator: {activator['name']}")
    print(f"Effect: {activator['effect']}")
    print(f"Mechanism: {activator['mechanism']}")
```

### 8. Enzyme Engineering Support

Find engineering targets and alternatives:

**Find Thermophilic Homologs**:
```python
from scripts.brenda_queries import find_thermophilic_homologs

thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)

for enzyme in thermophilic:
    print(f"Organism: {enzyme['organism']}")
    print(f"Optimal temp: {enzyme['optimal_temperature']}")
    print(f"Km: {enzyme['km']}")
```

**Find Alkaline/ Acid Stable Variants**:
```python
from scripts.brenda_queries import find_ph_stable_variants

alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
acidic = find_ph_stable_variants("1.1.1.1", max_ph=6.0)
```

### 9. Kinetic Modeling

Prepare data for kinetic modeling:

**Get Kinetic Parameters for Modeling**:
```python
from scripts.brenda_queries import get_modeling_parameters

model_data = get_modeling_parameters("1.1.1.1", substrate="ethanol")

print(f"Km: {model_data['km']}")
print(f"Vmax: {model_data['vmax']}")
print(f"kcat: {model_data['kcat']}")
print(f"Enzyme concentration: {model_data['enzyme_conc']}")
print(f"Temperature: {model_data['temperature']}")
print(f"pH: {model_data['ph']}")
```

**Generate Michaelis-Menten Plots**:
```python
from scripts.brenda_visualization import plot_michaelis_menten

# Generate kinetic plots
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

## Installation Requirements

```bash
uv pip install zeep requests pandas matplotlib seaborn
```

## Authentication Setup

BRENDA requires authentication credentials:

1. **Create .env file**:
```
BRENDA_EMAIL=your.email@example.com
BRENDA_PASSWORD=your_brenda_password
```

2. **Or set environment variables**:
```bash
export BRENDA_EMAIL="your.email@example.com"
export BRENDA_PASSWORD="your_brenda_password"
```

3. **Register for BRENDA access**:
   - Visit https://www.brenda-enzymes.org/
   - Create an account
   - Check your email for credentials
   - Note: There's also `BRENDA_EMIAL` (note the typo) for legacy support

## Helper Scripts

This skill includes comprehensive Python scripts for BRENDA database queries:

### scripts/brenda_queries.py

Provides high-level functions for enzyme data analysis:

**Key Functions**:
- `parse_km_entry(entry)`: Parse BRENDA Km data entries
- `parse_reaction_entry(entry)`: Parse reaction data entries
- `extract_organism_data(entry)`: Extract organism-specific information
- `search_enzymes_by_substrate(substrate, limit)`: Find enzymes for substrates
- `search_enzymes_by_product(product, limit)`: Find enzymes producing products
- `compare_across_organisms(ec_number, organisms)`: Compare enzyme properties
- `get_environmental_parameters(ec_number)`: Get pH and temperature data
- `get_cofactor_requirements(ec_number)`: Get cofactor information
- `get_substrate_specificity(ec_number)`: Analyze substrate preferences
- `get_inhibitors(ec_number)`: Get enzyme inhibition data
- `get_activators(ec_number)`: Get enzyme activation data
- `find_thermophilic_homologs(ec_number, min_temp)`: Find heat-stable variants
- `get_modeling_parameters(ec_number, substrate)`: Get parameters for kinetic modeling
- `export_kinetic_data(ec_number, format, filename)`: Export data to file

**Usage**:
```python
from scripts.brenda_queries import search_enzymes_by_substrate, compare_across_organisms

# Search for enzymes
enzymes = search_enzymes_by_substrate("glucose", limit=20)

# Compare across organisms
comparison = compare_across_organisms("1.1.1.1", ["E. coli", "S. cerevisiae"])
```

### scripts/brenda_visualization.py

Provides visualization functions for enzyme data:

**Key Functions**:
- `plot_kinetic_parameters(ec_number)`: Plot Km and kcat distributions
- `plot_organism_comparison(ec_number, organisms)`: Compare organisms
- `plot_pH_profiles(ec_number)`: Plot pH activity profiles
- `plot_temperature_profiles(ec_number)`: Plot temperature activity profiles
- `plot_substrate_specificity(ec_number)`: Visualize substrate preferences
- `plot_michaelis_menten(ec_number, substrate)`: Generate kinetic curves
- `create_heatmap_data(enzymes, parameters)`: Create data for heatmaps
- `generate_summary_plots(ec_number)`: Create comprehensive enzyme overview

**Usage**:
```python
from scripts.brenda_visualization import plot_kinetic_parameters, plot_michaelis_menten

# Plot kinetic parameters
plot_kinetic_parameters("1.1.1.1")

# Generate Michaelis-Menten curve
plot_michaelis_menten("1.1.1.1", substrate="ethanol")
```

### scripts/enzyme_pathway_builder.py

Build enzymatic pathways and retrosynthetic routes:

**Key Functions**:
- `find_pathway_for_product(product, max_steps)`: Find enzymatic pathways
- `build_retrosynthetic_tree(target, depth)`: Build retrosynthetic tree
- `suggest_enzyme_substitutions(ec_number, criteria)`: Suggest enzyme alternatives
- `calculate_pathway_feasibility(pathway)`: Evaluate pathway viability
- `optimize_pathway_conditions(pathway)`: Suggest optimal conditions
- `generate_pathway_report(pathway, filename)`: Create detailed pathway report

**Usage**:
```python
from scripts.enzyme_pathway_builder import find_pathway_for_product, build_retrosynthetic_tree

# Find pathway to product
pathway = find_pathway_for_product("lactate", max_steps=3)

# Build retrosynthetic tree
tree = build_retrosynthetic_tree("lactate", depth=2)
```

## API Rate Limits and Best Practices

**Rate Limits**:
- BRENDA API has moderate rate limiting
- Recommended: 1 request per second for sustained usage
- Maximum: 5 requests per 10 seconds

**Best Practices**:
1. **Cache results**: Store frequently accessed enzyme data locally
2. **Batch queries**: Combine related requests when possible
3. **Use specific searches**: Narrow down by organism, substrate when possible
4. **Handle missing data**: Not all enzymes have complete data
5. **Validate EC numbers**: Ensure EC numbers are in correct format
6. **Implement delays**: Add delays between consecutive requests
7. **Use wildcards wisely**: Use '*' for broader searches when appropriate
8. **Monitor quota**: Track your API usage

**Error Handling**:
```python
from brenda_client import get_km_values, get_reactions
from zeep.exceptions import Fault, TransportError

try:
    km_data = get_km_values("1.1.1.1")
except RuntimeError as e:
    print(f"Authentication error: {e}")
except Fault as e:
    print(f"BRENDA API error: {e}")
except TransportError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Workflows

### Workflow 1: Enzyme Discovery for New Substrate

Find suitable enzymes for a specific substrate:

```python
from brenda_client import get_km_values
from scripts.brenda_queries import search_enzymes_by_substrate, compare_substrate_affinity

# Search for enzymes that act on substrate
substrate = "2-phenylethanol"
enzymes = search_enzymes_by_substrate(substrate, limit=15)

print(f"Found {len(enzymes)} enzymes for {substrate}")
for enzyme in enzymes:
    print(f"EC {enzyme['ec_number']}: {enzyme['enzyme_name']}")

# Get kinetic data for best candidates
if enzymes:
    best_ec = enzymes[0]['ec_number']
    km_data = get_km_values(best_ec, substrate=substrate)

    if km_data:
        print(f"Kinetic data for {best_ec}:")
        for entry in km_data[:3]:  # First 3 entries
            print(f"  {entry}")
```

### Workflow 2: Cross-Organism Enzyme Comparison

Compare enzyme properties across different organisms:

```python
from scripts.brenda_queries import compare_across_organisms, get_environmental_parameters

# Define organisms for comparison
organisms = [
    "Escherichia coli",
    "Saccharomyces cerevisiae",
    "Bacillus subtilis",
    "Thermus thermophilus"
]

# Compare alcohol dehydrogenase
comparison = compare_across_organisms("1.1.1.1", organisms)

print("Cross-organism comparison:")
for org_data in comparison:
    print(f"\n{org_data['organism']}:")
    print(f"  Average Km: {org_data['average_km']}")
    print(f"  Optimal pH: {org_data['optimal_ph']}")
    print(f"  Temperature: {org_data['optimal_temperature']}°C")

# Get detailed environmental parameters
env_params = get_environmental_parameters("1.1.1.1")
print(f"\nOverall optimal pH range: {env_params['ph_range']}")
```

### Workflow 3: Enzyme Engineering Target Identification

Find engineering opportunities for enzyme improvement:

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    find_ph_stable_variants,
    compare_substrate_affinity
)

# Find thermophilic variants for heat stability
thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)
print(f"Found {len(thermophilic)} thermophilic variants")

# Find alkaline-stable variants
alkaline = find_ph_stable_variants("1.1.1.1", min_ph=8.0)
print(f"Found {len(alkaline)} alkaline-stable variants")

# Compare substrate specificities for engineering targets
specificity = compare_substrate_affinity("1.1.1.1")
print("Substrate affinity ranking:")
for i, sub in enumerate(specificity[:5]):
    print(f"  {i+1}. {sub['name']}: Km = {sub['km']}")
```

### Workflow 4: Enzymatic Pathway Construction

Build enzymatic synthesis pathways:

```python
from scripts.enzyme_pathway_builder import (
    find_pathway_for_product,
    build_retrosynthetic_tree,
    calculate_pathway_feasibility
)

# Find pathway to target product
target = "lactate"
pathway = find_pathway_for_product(target, max_steps=3)

if pathway:
    print(f"Found pathway to {target}:")
    for i, step in enumerate(pathway['steps']):
        print(f"  Step {i+1}: {step['reaction']}")
        print(f"    Enzyme: EC {step['ec_number']}")
        print(f"    Organism: {step['organism']}")

# Evaluate pathway feasibility
feasibility = calculate_pathway_feasibility(pathway)
print(f"\nPathway feasibility score: {feasibility['score']}/10")
print(f"Potential issues: {feasibility['warnings']}")
```

### Workflow 5: Kinetic Parameter Analysis

Comprehensive kinetic analysis for enzyme selection:

```python
from brenda_client import get_km_values
from scripts.brenda_queries import parse_km_entry, get_modeling_parameters
from scripts.brenda_visualization import plot_kinetic_parameters

# Get comprehensive kinetic data
ec_number = "1.1.1.1"
km_data = get_km_values(ec_number)

# Analyze kinetic parameters
all_entries = []
for entry in km_data:
    parsed = parse_km_entry(entry)
    if parsed['km_value']:
        all_entries.append(parsed)

print(f"Analyzed {len(all_entries)} kinetic entries")

# Find best kinetic performer
best_km = min(all_entries, key=lambda x: x['km_value'])
print(f"\nBest kinetic performer:")
print(f"  Organism: {best_km['organism']}")
print(f"  Substrate: {best_km['substrate']}")
print(f"  Km: {best_km['km_value']}")

# Get modeling parameters
model_data = get_modeling_parameters(ec_number, substrate=best_km['substrate'])
print(f"\nModeling parameters:")
print(f"  Km: {model_data['km']}")
print(f"  kcat: {model_data['kcat']}")
print(f"  Vmax: {model_data['vmax']}")

# Generate visualization
plot_kinetic_parameters(ec_number)
```

### Workflow 6: Industrial Enzyme Selection

Select enzymes for industrial applications:

```python
from scripts.brenda_queries import (
    find_thermophilic_homologs,
    get_environmental_parameters,
    get_inhibitors
)

# Industrial criteria: high temperature tolerance, organic solvent resistance
target_enzyme = "1.1.1.1"

# Find thermophilic variants
thermophilic = find_thermophilic_homologs(target_enzyme, min_temp=60)
print(f"Thermophilic candidates: {len(thermophilic)}")

# Check solvent tolerance (inhibitor data)
inhibitors = get_inhibitors(target_enzyme)
solvent_tolerant = [
    inv for inv in inhibitors
    if 'ethanol' not in inv['name'].lower() and
       'methanol' not in inv['name'].lower()
]

print(f"Solvent tolerant candidates: {len(solvent_tolerant)}")

# Evaluate top candidates
for candidate in thermophilic[:3]:
    print(f"\nCandidate: {candidate['organism']}")
    print(f"  Optimal temp: {candidate['optimal_temperature']}°C")
    print(f"  Km: {candidate['km']}")
    print(f"  pH range: {candidate.get('ph_range', 'N/A')}")
```

## Data Formats and Parsing

### BRENDA Response Format

BRENDA returns data in specific formats that need parsing:

**Km Value Format**:
```
organism*Escherichia coli#substrate*ethanol#kmValue*1.2#kmValueMaximum*#commentary*pH 7.4, 25°C#ligandStructureId*#literature*
```

**Reaction Format**:
```
ecNumber*1.1.1.1#organism*Saccharomyces cerevisiae#reaction*ethanol + NAD+ <=> acetaldehyde + NADH + H+#commentary*#literature*
```

### Data Extraction Patterns

```python
import re

def parse_brenda_field(data, field_name):
    """Extract specific field from BRENDA data entry"""
    pattern = f"{field_name}\\*([^#]*)"
    match = re.search(pattern, data)
    return match.group(1) if match else None

def extract_multiple_values(data, field_name):
    """Extract multiple values for a field"""
    pattern = f"{field_name}\\*([^#]*)"
    matches = re.findall(pattern, data)
    return [match for match in matches if match.strip()]
```

## Reference Documentation

For detailed BRENDA documentation, see `references/api_reference.md`. This includes:
- Complete SOAP API method documentation
- Full parameter lists and formats
- EC number structure and validation
- Response format specifications
- Error codes and handling
- Data field definitions
- Literature citation formats

## Troubleshooting

**Authentication Errors**:
- Verify BRENDA_EMAIL and BRENDA_PASSWORD in .env file
- Check for correct spelling (note BRENDA_EMIAL legacy support)
- Ensure BRENDA account is active and has API access

**No Results Returned**:
- Try broader searches with wildcards (*)
- Check EC number format (e.g., "1.1.1.1" not "1.1.1")
- Verify substrate spelling and naming
- Some enzymes may have limited data in BRENDA

**Rate Limiting**:
- Add delays between requests (0.5-1 second)
- Cache results locally
- Use more specific queries to reduce data volume
- Consider batch operations for multiple queries

**Network Errors**:
- Check internet connection
- BRENDA server may be temporarily unavailable
- Try again after a few minutes
- Consider using VPN if geo-restricted

**Data Format Issues**:
- Use the provided parsing functions in scripts
- BRENDA data can be inconsistent in formatting
- Handle missing fields gracefully
- Validate parsed data before use

**Performance Issues**:
- Large queries can be slow; limit search scope
- Use specific organism or substrate filters
- Consider asynchronous processing for batch operations
- Monitor memory usage with large datasets

## Additional Resources

- BRENDA Home: https://www.brenda-enzymes.org/
- BRENDA SOAP API Documentation: https://www.brenda-enzymes.org/soap.php
- Enzyme Commission (EC) Numbers: https://www.qmul.ac.uk/sbcs/iubmb/enzyme/
- Zeep SOAP Client: https://python-zeep.readthedocs.io/
- Enzyme Nomenclature: https://www.iubmb.org/enzyme/

---

## Reference: Api_Reference

# BRENDA Database API Reference

## Overview

This document provides detailed reference information for the BRENDA (BRaunschweig ENzyme DAtabase) SOAP API and the Python client implementation. BRENDA is the world's most comprehensive enzyme information system, containing over 45,000 enzymes with millions of kinetic data points.

## SOAP API Endpoints

### Base WSDL URL
```
https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl
```

### Authentication

All BRENDA API calls require authentication using email and password:

**Parameters:**
- `email`: Your registered BRENDA email address
- `password`: Your BRENDA account password

**Authentication Process:**
1. Password is hashed using SHA-256 before transmission
2. Email and hashed password are included as the first two parameters in every API call
3. Legacy support for `BRENDA_EMIAL` environment variable (note the typo)

## Available SOAP Actions

### getKmValue

Retrieves Michaelis constant (Km) values for enzymes.

**Parameters:**
1. `email`: BRENDA account email
2. `passwordHash`: SHA-256 hashed password
3. `ecNumber*: EC number of the enzyme (wildcards allowed)
4. `organism*: Organism name (wildcards allowed, default: "*")
5. `kmValue*: Km value field (default: "*")
6. `kmValueMaximum*: Maximum Km value field (default: "*")
7. `substrate*: Substrate name (wildcards allowed, default: "*")
8. `commentary*: Commentary field (default: "*")
9. `ligandStructureId*: Ligand structure ID field (default: "*")
10. `literature*: Literature reference field (default: "*")

**Wildcards:**
- `*`: Matches any sequence
- Can be used with partial EC numbers (e.g., "1.1.*")

**Response Format:**
```
organism*Escherichia coli#substrate*glucose#kmValue*0.12#kmValueMaximum*#commentary*pH 7.4, 25°C#ligandStructureId*#literature*
```

**Example Response Fields:**
- `organism`: Source organism
- `substrate`: Substrate name
- `kmValue`: Michaelis constant value (typically in mM)
- `kmValueMaximum`: Maximum Km value (if available)
- `commentary`: Experimental conditions (pH, temperature, etc.)
- `ligandStructureId`: BRENDA ligand structure identifier
- `literature`: Reference to primary literature

### getReaction

Retrieves reaction equations and stoichiometry for enzymes.

**Parameters:**
1. `email`: BRENDA account email
2. `passwordHash`: SHA-256 hashed password
3. `ecNumber*: EC number of the enzyme (wildcards allowed)
4. `organism*: Organism name (wildcards allowed, default: "*")
5. `reaction*: Reaction equation (wildcards allowed, default: "*")
6. `commentary*: Commentary field (default: "*")
7. `literature*: Literature reference field (default: "*")

**Response Format:**
```
ecNumber*1.1.1.1#organism*Saccharomyces cerevisiae#reaction*ethanol + NAD+ <=> acetaldehyde + NADH + H+#commentary*#literature*
```

**Example Response Fields:**
- `ecNumber`: Enzyme Commission number
- `organism`: Source organism
- `reaction`: Balanced chemical equation (using <=> for equilibrium, -> for direction)
- `commentary`: Additional information
- `literature`: Reference citation

## Data Field Specifications

### EC Number Format

EC numbers follow the standard hierarchical format: `A.B.C.D`

- **A**: Main class (1-6)
  - 1: Oxidoreductases
  - 2: Transferases
  - 3: Hydrolases
  - 4: Lyases
  - 5: Isomerases
  - 6: Ligases
- **B**: Subclass
- **C**: Sub-subclass
- **D**: Serial number

**Examples:**
- `1.1.1.1`: Alcohol dehydrogenase
- `1.1.1.2`: Alcohol dehydrogenase (NADP+)
- `3.2.1.23`: Beta-galactosidase
- `2.7.1.1`: Hexokinase

### Organism Names

Organism names should use proper binomial nomenclature:

**Correct Format:**
- `Escherichia coli`
- `Saccharomyces cerevisiae`
- `Homo sapiens`

**Wildcards:**
- `Escherichia*`: Matches all E. coli strains
- `*coli`: Matches all coli species
- `*`: Matches all organisms

### Substrate Names

Substrate names follow IUPAC or common biochemical conventions:

**Common Formats:**
- Chemical names: `glucose`, `ethanol`, `pyruvate`
- IUPAC names: `β-D-glucose`, `ethanol`, `2-oxopropanoic acid`
- Abbreviations: `ATP`, `NAD+`, `CoA`

**Special Cases:**
- Cofactors: `NAD+`, `NADH`, `NADP+`, `NADPH`
- Metal ions: `Mg2+`, `Zn2+`, `Fe2+`
- Inorganic compounds: `H2O`, `CO2`, `O2`

### Commentary Field Format

Commentary fields contain experimental conditions and other metadata:

**Common Information:**
- **pH**: `pH 7.4`, `pH 6.5-8.0`
- **Temperature**: `25°C`, `37°C`, `50-60°C`
- **Buffer systems**: `phosphate buffer`, `Tris-HCl`
- **Purity**: `purified enzyme`, `crude extract`
- **Assay conditions**: `spectrophotometric`, `radioactive`
- **Inhibition**: `inhibited by heavy metals`, `activated by Mg2+`

**Examples:**
- `pH 7.4, 25°C, phosphate buffer`
- `pH 6.5-8.0 optimum, thermostable enzyme`
- `purified enzyme, specific activity 125 U/mg`
- `inhibited by iodoacetate, activated by Mn2+`

### Reaction Equation Format

Reactions use standard biochemical notation:

**Symbols:**
- `+`: Separate reactants/products
- `<=>`: Reversible reactions
- `->`: Irreversible (directional) reactions
- `=`: Alternative notation for reactions

**Common Patterns:**
- **Oxidation/reduction**: `alcohol + NAD+ <=> aldehyde + NADH + H+`
- **Phosphorylation**: `glucose + ATP <=> glucose-6-phosphate + ADP`
- **Hydrolysis**: `ester + H2O <=> acid + alcohol`
- **Carboxylation**: `acetyl-CoA + CO2 + H2O <=> malonyl-CoA`

**Cofactor Requirements:**
- **Oxidoreductases**: NAD+, NADH, NADP+, NADPH, FAD, FADH2
- **Transferases**: ATP, ADP, GTP, GDP
- **Ligases**: ATP, CoA

## Rate Limiting and Usage

### API Rate Limits

- **Maximum**: 5 requests per second
- **Sustained**: 1 request per second recommended
- **Daily quota**: Varies by account type

### Best Practices

1. **Implement delays**: Add 0.5-1 second between requests
2. **Cache results**: Store frequently accessed data locally
3. **Use specific searches**: Narrow by organism and substrate when possible
4. **Batch operations**: Group related queries
5. **Handle errors gracefully**: Check for HTTP and SOAP errors
6. **Use wildcards judiciously**: Broad searches return large datasets

### Error Handling

**Common SOAP Errors:**
- `Authentication failed`: Check email/password
- `No data found`: Verify EC number, organism, substrate spelling
- `Rate limit exceeded`: Reduce request frequency
- `Invalid parameters`: Check parameter format and order

**Network Errors:**
- Connection timeouts
- SSL/TLS errors
- Service unavailable

## Python Client Reference

### brenda_client Module

#### Core Functions

**`load_env_from_file(path=".env")`**
- **Purpose**: Load environment variables from .env file
- **Parameters**: `path` - Path to .env file (default: ".env")
- **Returns**: None (populates os.environ)

**`_get_credentials() -> tuple[str, str]`**
- **Purpose**: Retrieve BRENDA credentials from environment
- **Returns**: Tuple of (email, password)
- **Raises**: RuntimeError if credentials missing

**`_get_client() -> Client`**
- **Purpose**: Initialize or retrieve SOAP client
- **Returns**: Zeep Client instance
- **Features**: Singleton pattern, custom transport settings

**`_hash_password(password: str) -> str`**
- **Purpose**: Generate SHA-256 hash of password
- **Parameters**: `password` - Plain text password
- **Returns**: Hexadecimal SHA-256 hash

**`call_brenda(action: str, parameters: List[str]) -> str`**
- **Purpose**: Execute BRENDA SOAP action
- **Parameters**:
  - `action` - SOAP action name (e.g., "getKmValue")
  - `parameters` - List of parameters in correct order
- **Returns**: Raw response string from BRENDA

#### Convenience Functions

**`get_km_values(ec_number: str, organism: str = "*", substrate: str = "*") -> List[str]`**
- **Purpose**: Retrieve Km values for specified enzyme
- **Parameters**:
  - `ec_number`: Enzyme Commission number
  - `organism`: Organism name (wildcard allowed, default: "*")
  - `substrate`: Substrate name (wildcard allowed, default: "*")
- **Returns**: List of parsed data strings

**`get_reactions(ec_number: str, organism: str = "*", reaction: str = "*") -> List[str]`**
- **Purpose**: Retrieve reaction data for specified enzyme
- **Parameters**:
  - `ec_number`: Enzyme Commission number
  - `organism`: Organism name (wildcard allowed, default: "*")
  - `reaction`: Reaction pattern (wildcard allowed, default: "*")
- **Returns**: List of reaction data strings

#### Utility Functions

**`split_entries(return_text: str) -> List[str]`**
- **Purpose**: Normalize BRENDA responses to list format
- **Parameters**: `return_text` - Raw response from BRENDA
- **Returns**: List of individual data entries
- **Features**: Handles both string and complex object responses

## Data Structures and Parsing

### Km Entry Structure

**Parsed Km Entry Dictionary:**
```python
{
    'ecNumber': '1.1.1.1',
    'organism': 'Escherichia coli',
    'substrate': 'ethanol',
    'kmValue': '0.12',
    'km_value_numeric': 0.12,  # Extracted numeric value
    'kmValueMaximum': '',
    'commentary': 'pH 7.4, 25°C',
    'ph': 7.4,               # Extracted from commentary
    'temperature': 25.0,      # Extracted from commentary
    'ligandStructureId': '',
    'literature': ''
}
```

### Reaction Entry Structure

**Parsed Reaction Entry Dictionary:**
```python
{
    'ecNumber': '1.1.1.1',
    'organism': 'Saccharomyces cerevisiae',
    'reaction': 'ethanol + NAD+ <=> acetaldehyde + NADH + H+',
    'reactants': ['ethanol', 'NAD+'],
    'products': ['acetaldehyde', 'NADH', 'H+'],
    'commentary': '',
    'literature': ''
}
```

## Query Patterns and Examples

### Basic Queries

**Get all Km values for an enzyme:**
```python
from brenda_client import get_km_values

# Get all alcohol dehydrogenase Km values
km_data = get_km_values("1.1.1.1")
```

**Get Km values for specific organism:**
```python
# Get human alcohol dehydrogenase Km values
human_km = get_km_values("1.1.1.1", organism="Homo sapiens")
```

**Get Km values for specific substrate:**
```python
# Get Km for ethanol oxidation
ethanol_km = get_km_values("1.1.1.1", substrate="ethanol")
```

### Wildcard Searches

**Search for enzyme families:**
```python
# All alcohol dehydrogenases
alcohol_dehydrogenases = get_km_values("1.1.1.*")

# All hexokinases
hexokinases = get_km_values("2.7.1.*")
```

**Search for organism groups:**
```python
# All E. coli strains
e_coli_enzymes = get_km_values("*", organism="Escherichia coli")

# All Bacillus species
bacillus_enzymes = get_km_values("*", organism="Bacillus*")
```

### Combined Searches

**Specific enzyme-substrate combination:**
```python
# Get Km values for glucose oxidation in yeast
glucose_km = get_km_values("1.1.1.1",
                          organism="Saccharomyces cerevisiae",
                          substrate="glucose")
```

### Reaction Queries

**Get all reactions for an enzyme:**
```python
from brenda_client import get_reactions

reactions = get_reactions("1.1.1.1")
```

**Search for reactions with specific substrates:**
```python
# Find reactions involving glucose
glucose_reactions = get_reactions("*", reaction="*glucose*")
```

## Data Analysis Patterns

### Kinetic Parameter Analysis

**Extract numeric Km values:**
```python
from scripts.brenda_queries import parse_km_entry

km_data = get_km_values("1.1.1.1", substrate="ethanol")
numeric_kms = []

for entry in km_data:
    parsed = parse_km_entry(entry)
    if 'km_value_numeric' in parsed:
        numeric_kms.append(parsed['km_value_numeric'])

if numeric_kms:
    print(f"Average Km: {sum(numeric_kms)/len(numeric_kms):.3f}")
    print(f"Range: {min(numeric_kms):.3f} - {max(numeric_kms):.3f}")
```

### Organism Comparison

**Compare enzyme properties across organisms:**
```python
from scripts.brenda_queries import compare_across_organisms

organisms = ["Escherichia coli", "Saccharomyces cerevisiae", "Homo sapiens"]
comparison = compare_across_organisms("1.1.1.1", organisms)

for org_data in comparison:
    if org_data.get('data_points', 0) > 0:
        print(f"{org_data['organism']}: {org_data['average_km']:.3f}")
```

### Substrate Specificity

**Analyze substrate preferences:**
```python
from scripts.brenda_queries import get_substrate_specificity

specificity = get_substrate_specificity("1.1.1.1")

for substrate_data in specificity[:5]:  # Top 5
    print(f"{substrate_data['name']}: Km = {substrate_data['km']:.3f}")
```

## Integration Examples

### Metabolic Pathway Construction

**Build enzymatic pathway:**
```python
from scripts.enzyme_pathway_builder import find_pathway_for_product

# Find pathway for lactate production
pathway = find_pathway_for_product("lactate", max_steps=3)

for step in pathway['steps']:
    print(f"Step {step['step_number']}: {step['substrate']} -> {step['product']}")
    print(f"Enzymes available: {len(step['enzymes'])}")
```

### Enzyme Engineering Support

**Find thermostable variants:**
```python
from scripts.brenda_queries import find_thermophilic_homologs

thermophilic = find_thermophilic_homologs("1.1.1.1", min_temp=50)

for enzyme in thermophilic:
    print(f"{enzyme['organism']}: {enzyme['optimal_temperature']}°C")
```

### Kinetic Modeling

**Extract parameters for modeling:**
```python
from scripts.brenda_queries import get_modeling_parameters

model_data = get_modeling_parameters("1.1.1.1", substrate="ethanol")

print(f"Km: {model_data['km']}")
print(f"Vmax: {model_data['vmax']}")
print(f"Optimal conditions: pH {model_data['ph']}, {model_data['temperature']}°C")
```

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Check BRENDA_EMAIL and BRENDA_PASSWORD environment variables
- Verify account is active and has API access
- Note legacy BRENDA_EMIAL support (typo in variable name)

**No Data Returned:**
- Verify EC number format (e.g., "1.1.1.1", not "1.1.1")
- Check spelling of organism and substrate names
- Try wildcards for broader searches
- Some enzymes may have limited data in BRENDA

**Rate Limiting:**
- Implement delays between requests
- Cache results locally
- Use more specific queries to reduce data volume
- Consider batch operations

**Data Format Issues:**
- Use provided parsing functions
- Handle missing fields gracefully
- BRENDA data format can be inconsistent
- Validate parsed data before use

### Performance Optimization

**Query Efficiency:**
- Use specific EC numbers when known
- Limit by organism or substrate to reduce result size
- Cache frequently accessed data
- Batch similar requests

**Memory Management:**
- Process large datasets in chunks
- Use generators for large result sets
- Clear parsed data when no longer needed

**Network Optimization:**
- Implement retry logic for network errors
- Use appropriate timeouts
- Monitor request frequency

## Additional Resources

### Official Documentation

- **BRENDA Website**: https://www.brenda-enzymes.org/
- **SOAP API Documentation**: https://www.brenda-enzymes.org/soap.php
- **Enzyme Nomenclature**: https://www.iubmb.org/enzyme/
- **EC Number Database**: https://www.qmul.ac.uk/sbcs/iubmb/enzyme/

### Related Libraries

- **Zeep (SOAP Client)**: https://python-zeep.readthedocs.io/
- **PubChemPy**: https://pubchempy.readthedocs.io/
- **BioPython**: https://biopython.org/
- **RDKit**: https://www.rdkit.org/

### Data Formats

- **Enzyme Commission Numbers**: IUBMB enzyme classification
- **IUPAC Nomenclature**: Chemical naming conventions
- **Biochemical Reactions**: Standard equation notation
- **Kinetic Parameters**: Michaelis-Menten kinetics

### Community Resources

- **BRENDA Help Desk**: Support via official website
- **Bioinformatics Forums**: Stack Overflow, Biostars
- **GitHub Issues**: Project-specific bug reports
- **Research Papers**: Primary literature for enzyme data

---

*This API reference covers the core functionality of the BRENDA SOAP API and Python client. For complete details on available data fields and query patterns, consult the official BRENDA documentation.*
