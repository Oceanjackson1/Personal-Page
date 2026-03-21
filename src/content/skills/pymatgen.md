---
title: "Pymatgen 材料科学"
description: "Python 材料基因组学库，晶体结构分析和材料性质计算"
category: "other"
source: "community"
author: "Community"
tags: ["pymatgen"]
date: 2026-03-20
---

# Pymatgen - Python Materials Genomics

## Overview

Pymatgen is a comprehensive Python library for materials analysis that powers the Materials Project. Create, analyze, and manipulate crystal structures and molecules, compute phase diagrams and thermodynamic properties, analyze electronic structure (band structures, DOS), generate surfaces and interfaces, and access Materials Project's database of computed materials. Supports 100+ file formats from various computational codes.

## When to Use This Skill

This skill should be used when:
- Working with crystal structures or molecular systems in materials science
- Converting between structure file formats (CIF, POSCAR, XYZ, etc.)
- Analyzing symmetry, space groups, or coordination environments
- Computing phase diagrams or assessing thermodynamic stability
- Analyzing electronic structure data (band gaps, DOS, band structures)
- Generating surfaces, slabs, or studying interfaces
- Accessing the Materials Project database programmatically
- Setting up high-throughput computational workflows
- Analyzing diffusion, magnetism, or mechanical properties
- Working with VASP, Gaussian, Quantum ESPRESSO, or other computational codes

## Quick Start Guide

### Installation

```bash
# Core pymatgen
uv pip install pymatgen

# With Materials Project API access
uv pip install pymatgen mp-api

# Optional dependencies for extended functionality
uv pip install pymatgen[analysis]  # Additional analysis tools
uv pip install pymatgen[vis]       # Visualization tools
```

### Basic Structure Operations

```python
from pymatgen.core import Structure, Lattice

# Read structure from file (automatic format detection)
struct = Structure.from_file("POSCAR")

# Create structure from scratch
lattice = Lattice.cubic(3.84)
struct = Structure(lattice, ["Si", "Si"], [[0,0,0], [0.25,0.25,0.25]])

# Write to different format
struct.to(filename="structure.cif")

# Basic properties
print(f"Formula: {struct.composition.reduced_formula}")
print(f"Space group: {struct.get_space_group_info()}")
print(f"Density: {struct.density:.2f} g/cm³")
```

### Materials Project Integration

```bash
# Set up API key
export MP_API_KEY="your_api_key_here"
```

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Get structure by material ID
    struct = mpr.get_structure_by_material_id("mp-149")

    # Search for materials
    materials = mpr.materials.summary.search(
        formula="Fe2O3",
        energy_above_hull=(0, 0.05)
    )
```

## Core Capabilities

### 1. Structure Creation and Manipulation

Create structures using various methods and perform transformations.

**From files:**
```python
# Automatic format detection
struct = Structure.from_file("structure.cif")
struct = Structure.from_file("POSCAR")
mol = Molecule.from_file("molecule.xyz")
```

**From scratch:**
```python
from pymatgen.core import Structure, Lattice

# Using lattice parameters
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
struct = Structure(lattice, ["Si", "Si"], coords)

# From space group
struct = Structure.from_spacegroup(
    "Fm-3m",
    Lattice.cubic(3.5),
    ["Si"],
    [[0, 0, 0]]
)
```

**Transformations:**
```python
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation,
    PrimitiveCellTransformation
)

# Create supercell
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# Substitute elements
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# Get primitive cell
trans = PrimitiveCellTransformation()
primitive = trans.apply_transformation(struct)
```

**Reference:** See `references/core_classes.md` for comprehensive documentation of Structure, Lattice, Molecule, and related classes.

### 2. File Format Conversion

Convert between 100+ file formats with automatic format detection.

**Using convenience methods:**
```python
# Read any format
struct = Structure.from_file("input_file")

# Write to any format
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="output.xyz")
```

**Using the conversion script:**
```bash
# Single file conversion
python scripts/structure_converter.py POSCAR structure.cif

# Batch conversion
python scripts/structure_converter.py *.cif --output-dir ./poscar_files --format poscar
```

**Reference:** See `references/io_formats.md` for detailed documentation of all supported formats and code integrations.

### 3. Structure Analysis and Symmetry

Analyze structures for symmetry, coordination, and other properties.

**Symmetry analysis:**
```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)

# Get space group information
print(f"Space group: {sga.get_space_group_symbol()}")
print(f"Number: {sga.get_space_group_number()}")
print(f"Crystal system: {sga.get_crystal_system()}")

# Get conventional/primitive cells
conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()
```

**Coordination environment:**
```python
from pymatgen.analysis.local_env import CrystalNN

cnn = CrystalNN()
neighbors = cnn.get_nn_info(struct, n=0)  # Neighbors of site 0

print(f"Coordination number: {len(neighbors)}")
for neighbor in neighbors:
    site = struct[neighbor['site_index']]
    print(f"  {site.species_string} at {neighbor['weight']:.3f} Å")
```

**Using the analysis script:**
```bash
# Comprehensive analysis
python scripts/structure_analyzer.py POSCAR --symmetry --neighbors

# Export results
python scripts/structure_analyzer.py structure.cif --symmetry --export json
```

**Reference:** See `references/analysis_modules.md` for detailed documentation of all analysis capabilities.

### 4. Phase Diagrams and Thermodynamics

Construct phase diagrams and analyze thermodynamic stability.

**Phase diagram construction:**
```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

# Get entries from Materials Project
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

# Build phase diagram
pd = PhaseDiagram(entries)

# Check stability
from pymatgen.core import Composition
comp = Composition("LiFeO2")

# Find entry for composition
for entry in entries:
    if entry.composition.reduced_formula == comp.reduced_formula:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"Energy above hull: {e_above_hull:.4f} eV/atom")

        if e_above_hull > 0.001:
            # Get decomposition
            decomp = pd.get_decomposition(comp)
            print("Decomposes to:", decomp)

# Plot
plotter = PDPlotter(pd)
plotter.show()
```

**Using the phase diagram script:**
```bash
# Generate phase diagram
python scripts/phase_diagram_generator.py Li-Fe-O --output li_fe_o.png

# Analyze specific composition
python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2" --show
```

**Reference:** See `references/analysis_modules.md` (Phase Diagrams section) and `references/transformations_workflows.md` (Workflow 2) for detailed examples.

### 5. Electronic Structure Analysis

Analyze band structures, density of states, and electronic properties.

**Band structure:**
```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# Read from VASP calculation
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# Analyze
band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct: {band_gap['direct']}")
print(f"Is metal: {bs.is_metal()}")

# Plot
plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

**Density of states:**
```python
from pymatgen.electronic_structure.plotter import DosPlotter

dos = vasprun.complete_dos

# Get element-projected DOS
element_dos = dos.get_element_dos()
for element, element_dos_obj in element_dos.items():
    print(f"{element}: {element_dos_obj.get_gap():.3f} eV")

# Plot
plotter = DosPlotter()
plotter.add_dos("Total DOS", dos)
plotter.show()
```

**Reference:** See `references/analysis_modules.md` (Electronic Structure section) and `references/io_formats.md` (VASP section).

### 6. Surface and Interface Analysis

Generate slabs, analyze surfaces, and study interfaces.

**Slab generation:**
```python
from pymatgen.core.surface import SlabGenerator

# Generate slabs for specific Miller index
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,      # Å
    min_vacuum_size=10.0,    # Å
    center_slab=True
)

slabs = slabgen.get_slabs()

# Write slabs
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_{i}.cif")
```

**Wulff shape construction:**
```python
from pymatgen.analysis.wulff import WulffShape

# Define surface energies
surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}

wulff = WulffShape(struct.lattice, surface_energies)
print(f"Surface area: {wulff.surface_area:.2f} Ų")
print(f"Volume: {wulff.volume:.2f} ų")

wulff.show()
```

**Adsorption site finding:**
```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule

asf = AdsorbateSiteFinder(slab)

# Find sites
ads_sites = asf.find_adsorption_sites()
print(f"On-top sites: {len(ads_sites['ontop'])}")
print(f"Bridge sites: {len(ads_sites['bridge'])}")
print(f"Hollow sites: {len(ads_sites['hollow'])}")

# Add adsorbate
adsorbate = Molecule("O", [[0, 0, 0]])
ads_struct = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])
```

**Reference:** See `references/analysis_modules.md` (Surface and Interface section) and `references/transformations_workflows.md` (Workflows 3 and 9).

### 7. Materials Project Database Access

Programmatically access the Materials Project database.

**Setup:**
1. Get API key from https://next-gen.materialsproject.org/
2. Set environment variable: `export MP_API_KEY="your_key_here"`

**Search and retrieve:**
```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Search by formula
    materials = mpr.materials.summary.search(formula="Fe2O3")

    # Search by chemical system
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # Filter by properties
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Stable/metastable
        band_gap=(1.0, 3.0)            # Semiconducting
    )

    # Get structure
    struct = mpr.get_structure_by_material_id("mp-149")

    # Get band structure
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Get entries for phase diagram
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")
```

**Reference:** See `references/materials_project_api.md` for comprehensive API documentation and examples.

### 8. Computational Workflow Setup

Set up calculations for various electronic structure codes.

**VASP input generation:**
```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet

# Relaxation
relax = MPRelaxSet(struct)
relax.write_input("./relax_calc")

# Static calculation
static = MPStaticSet(struct)
static.write_input("./static_calc")

# Band structure (non-self-consistent)
nscf = MPNonSCFSet(struct, mode="line")
nscf.write_input("./bandstructure_calc")

# Custom parameters
custom = MPRelaxSet(struct, user_incar_settings={"ENCUT": 600})
custom.write_input("./custom_calc")
```

**Other codes:**
```python
# Gaussian
from pymatgen.io.gaussian import GaussianInput

gin = GaussianInput(
    mol,
    functional="B3LYP",
    basis_set="6-31G(d)",
    route_parameters={"Opt": None}
)
gin.write_file("input.gjf")

# Quantum ESPRESSO
from pymatgen.io.pwscf import PWInput

pwin = PWInput(struct, control={"calculation": "scf"})
pwin.write_file("pw.in")
```

**Reference:** See `references/io_formats.md` (Electronic Structure Code I/O section) and `references/transformations_workflows.md` for workflow examples.

### 9. Advanced Analysis

**Diffraction patterns:**
```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

xrd = XRDCalculator()
pattern = xrd.get_pattern(struct)

# Get peaks
for peak in pattern.hkls:
    print(f"2θ = {peak['2theta']:.2f}°, hkl = {peak['hkl']}")

pattern.plot()
```

**Elastic properties:**
```python
from pymatgen.analysis.elasticity import ElasticTensor

# From elastic tensor matrix
elastic_tensor = ElasticTensor.from_voigt(matrix)

print(f"Bulk modulus: {elastic_tensor.k_voigt:.1f} GPa")
print(f"Shear modulus: {elastic_tensor.g_voigt:.1f} GPa")
print(f"Young's modulus: {elastic_tensor.y_mod:.1f} GPa")
```

**Magnetic ordering:**
```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# Enumerate magnetic orderings
trans = MagOrderingTransformation({"Fe": 5.0})
mag_structs = trans.apply_transformation(struct, return_ranked_list=True)

# Get lowest energy magnetic structure
lowest_energy_struct = mag_structs[0]['structure']
```

**Reference:** See `references/analysis_modules.md` for comprehensive analysis module documentation.

## Bundled Resources

### Scripts (`scripts/`)

Executable Python scripts for common tasks:

- **`structure_converter.py`**: Convert between structure file formats
  - Supports batch conversion and automatic format detection
  - Usage: `python scripts/structure_converter.py POSCAR structure.cif`

- **`structure_analyzer.py`**: Comprehensive structure analysis
  - Symmetry, coordination, lattice parameters, distance matrix
  - Usage: `python scripts/structure_analyzer.py structure.cif --symmetry --neighbors`

- **`phase_diagram_generator.py`**: Generate phase diagrams from Materials Project
  - Stability analysis and thermodynamic properties
  - Usage: `python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2"`

All scripts include detailed help: `python scripts/script_name.py --help`

### References (`references/`)

Comprehensive documentation loaded into context as needed:

- **`core_classes.md`**: Element, Structure, Lattice, Molecule, Composition classes
- **`io_formats.md`**: File format support and code integration (VASP, Gaussian, etc.)
- **`analysis_modules.md`**: Phase diagrams, surfaces, electronic structure, symmetry
- **`materials_project_api.md`**: Complete Materials Project API guide
- **`transformations_workflows.md`**: Transformations framework and common workflows

Load references when detailed information is needed about specific modules or workflows.

## Common Workflows

### High-Throughput Structure Generation

```python
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.io.vasp.sets import MPRelaxSet

# Generate doped structures
base_struct = Structure.from_file("POSCAR")
dopants = ["Mn", "Co", "Ni", "Cu"]

for dopant in dopants:
    trans = SubstitutionTransformation({"Fe": dopant})
    doped_struct = trans.apply_transformation(base_struct)

    # Generate VASP inputs
    vasp_input = MPRelaxSet(doped_struct)
    vasp_input.write_input(f"./calcs/Fe_{dopant}")
```

### Band Structure Calculation Workflow

```python
# 1. Relaxation
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# 2. Static (after relaxation)
relaxed = Structure.from_file("1_relax/CONTCAR")
static = MPStaticSet(relaxed)
static.write_input("./2_static")

# 3. Band structure (non-self-consistent)
nscf = MPNonSCFSet(relaxed, mode="line")
nscf.write_input("./3_bandstructure")

# 4. Analysis
from pymatgen.io.vasp import Vasprun
vasprun = Vasprun("3_bandstructure/vasprun.xml")
bs = vasprun.get_band_structure()
bs.get_band_gap()
```

### Surface Energy Calculation

```python
# 1. Get bulk energy
bulk_vasprun = Vasprun("bulk/vasprun.xml")
bulk_E_per_atom = bulk_vasprun.final_energy / len(bulk)

# 2. Generate and calculate slabs
slabgen = SlabGenerator(bulk, (1,1,1), 10, 15)
slab = slabgen.get_slabs()[0]

MPRelaxSet(slab).write_input("./slab_calc")

# 3. Calculate surface energy (after calculation)
slab_vasprun = Vasprun("slab_calc/vasprun.xml")
E_surf = (slab_vasprun.final_energy - len(slab) * bulk_E_per_atom) / (2 * slab.surface_area)
E_surf *= 16.021766  # Convert eV/Ų to J/m²
```

**More workflows:** See `references/transformations_workflows.md` for 10 detailed workflow examples.

## Best Practices

### Structure Handling

1. **Use automatic format detection**: `Structure.from_file()` handles most formats
2. **Prefer immutable structures**: Use `IStructure` when structure shouldn't change
3. **Check symmetry**: Use `SpacegroupAnalyzer` to reduce to primitive cell
4. **Validate structures**: Check for overlapping atoms or unreasonable bond lengths

### File I/O

1. **Use convenience methods**: `from_file()` and `to()` are preferred
2. **Specify formats explicitly**: When automatic detection fails
3. **Handle exceptions**: Wrap file I/O in try-except blocks
4. **Use serialization**: `as_dict()`/`from_dict()` for version-safe storage

### Materials Project API

1. **Use context manager**: Always use `with MPRester() as mpr:`
2. **Batch queries**: Request multiple items at once
3. **Cache results**: Save frequently used data locally
4. **Filter effectively**: Use property filters to reduce data transfer

### Computational Workflows

1. **Use input sets**: Prefer `MPRelaxSet`, `MPStaticSet` over manual INCAR
2. **Check convergence**: Always verify calculations converged
3. **Track transformations**: Use `TransformedStructure` for provenance
4. **Organize calculations**: Use clear directory structures

### Performance

1. **Reduce symmetry**: Use primitive cells when possible
2. **Limit neighbor searches**: Specify reasonable cutoff radii
3. **Use appropriate methods**: Different analysis tools have different speed/accuracy tradeoffs
4. **Parallelize when possible**: Many operations can be parallelized

## Units and Conventions

Pymatgen uses atomic units throughout:
- **Lengths**: Angstroms (Å)
- **Energies**: Electronvolts (eV)
- **Angles**: Degrees (°)
- **Magnetic moments**: Bohr magnetons (μB)
- **Time**: Femtoseconds (fs)

Convert units using `pymatgen.core.units` when needed.

## Integration with Other Tools

Pymatgen integrates seamlessly with:
- **ASE** (Atomic Simulation Environment)
- **Phonopy** (phonon calculations)
- **BoltzTraP** (transport properties)
- **Atomate/Fireworks** (workflow management)
- **AiiDA** (provenance tracking)
- **Zeo++** (pore analysis)
- **OpenBabel** (molecule conversion)

## Troubleshooting

**Import errors**: Install missing dependencies
```bash
uv pip install pymatgen[analysis,vis]
```

**API key not found**: Set MP_API_KEY environment variable
```bash
export MP_API_KEY="your_key_here"
```

**Structure read failures**: Check file format and syntax
```python
# Try explicit format specification
struct = Structure.from_file("file.txt", fmt="cif")
```

**Symmetry analysis fails**: Structure may have numerical precision issues
```python
# Increase tolerance
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
sga = SpacegroupAnalyzer(struct, symprec=0.1)
```

## Additional Resources

- **Documentation**: https://pymatgen.org/
- **Materials Project**: https://materialsproject.org/
- **GitHub**: https://github.com/materialsproject/pymatgen
- **Forum**: https://matsci.org/
- **Example notebooks**: https://matgenb.materialsvirtuallab.org/

## Version Notes

This skill is designed for pymatgen 2024.x and later. For the Materials Project API, use the `mp-api` package (separate from legacy `pymatgen.ext.matproj`).

Requirements:
- Python 3.10 or higher
- pymatgen >= 2023.x
- mp-api (for Materials Project access)

---

## Reference: Analysis_Modules

# Pymatgen Analysis Modules Reference

This reference documents pymatgen's extensive analysis capabilities for materials characterization, property prediction, and computational analysis.

## Phase Diagrams and Thermodynamics

### Phase Diagram Construction

```python
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
from pymatgen.entries.computed_entries import ComputedEntry

# Create entries (composition and total energy)
entries = [
    ComputedEntry("Fe", -8.4),
    ComputedEntry("O2", -4.9),
    ComputedEntry("FeO", -6.7),
    ComputedEntry("Fe2O3", -8.3),
    ComputedEntry("Fe3O4", -9.1),
]

# Build phase diagram
pd = PhaseDiagram(entries)

# Get stable entries
stable_entries = pd.stable_entries

# Get energy above hull (stability)
entry_to_test = ComputedEntry("Fe2O3", -8.0)
energy_above_hull = pd.get_e_above_hull(entry_to_test)

# Get decomposition products
decomp = pd.get_decomposition(entry_to_test.composition)
# Returns: {entry1: fraction1, entry2: fraction2, ...}

# Get equilibrium reaction energy
rxn_energy = pd.get_equilibrium_reaction_energy(entry_to_test)

# Plot phase diagram
plotter = PDPlotter(pd)
plotter.show()
plotter.write_image("phase_diagram.png")
```

### Chemical Potential Diagrams

```python
from pymatgen.analysis.phase_diagram import ChemicalPotentialDiagram

# Create chemical potential diagram
cpd = ChemicalPotentialDiagram(entries, limits={"O": (-10, 0)})

# Get domains (stability regions)
domains = cpd.domains
```

### Pourbaix Diagrams

Electrochemical phase diagrams with pH and potential axes.

```python
from pymatgen.analysis.pourbaix_diagram import PourbaixDiagram, PourbaixPlotter
from pymatgen.entries.computed_entries import ComputedEntry

# Create entries with corrections for aqueous species
entries = [...]  # Include solids and ions

# Build Pourbaix diagram
pb = PourbaixDiagram(entries)

# Get stable entry at specific pH and potential
stable_entry = pb.get_stable_entry(pH=7, V=0)

# Plot
plotter = PourbaixPlotter(pb)
plotter.show()
```

## Structure Analysis

### Structure Matching and Comparison

```python
from pymatgen.analysis.structure_matcher import StructureMatcher

matcher = StructureMatcher()

# Check if structures match
is_match = matcher.fit(struct1, struct2)

# Get mapping between structures
mapping = matcher.get_mapping(struct1, struct2)

# Group similar structures
grouped = matcher.group_structures([struct1, struct2, struct3, ...])
```

### Ewald Summation

Calculate electrostatic energy of ionic structures.

```python
from pymatgen.analysis.ewald import EwaldSummation

ewald = EwaldSummation(struct)
total_energy = ewald.total_energy  # In eV
forces = ewald.forces  # Forces on each site
```

### Symmetry Analysis

```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)

# Get space group information
spacegroup_symbol = sga.get_space_group_symbol()  # e.g., "Fm-3m"
spacegroup_number = sga.get_space_group_number()   # e.g., 225
crystal_system = sga.get_crystal_system()           # e.g., "cubic"

# Get symmetrized structure
sym_struct = sga.get_symmetrized_structure()
equivalent_sites = sym_struct.equivalent_sites

# Get conventional/primitive cells
conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()

# Get symmetry operations
symmetry_ops = sga.get_symmetry_operations()
```

## Local Environment Analysis

### Coordination Environment

```python
from pymatgen.analysis.local_env import (
    VoronoiNN,           # Voronoi tessellation
    CrystalNN,           # Crystal-based
    MinimumDistanceNN,   # Distance cutoff
    BrunnerNN_real,      # Brunner method
)

# Voronoi nearest neighbors
voronoi = VoronoiNN()
neighbors = voronoi.get_nn_info(struct, n=0)  # Neighbors of site 0

# CrystalNN (recommended for most cases)
crystalnn = CrystalNN()
neighbors = crystalnn.get_nn_info(struct, n=0)

# Analyze all sites
for i, site in enumerate(struct):
    neighbors = voronoi.get_nn_info(struct, i)
    coordination_number = len(neighbors)
    print(f"Site {i} ({site.species_string}): CN = {coordination_number}")
```

### Coordination Geometry (ChemEnv)

Detailed coordination environment identification.

```python
from pymatgen.analysis.chemenv.coordination_environments.coordination_geometry_finder import LocalGeometryFinder
from pymatgen.analysis.chemenv.coordination_environments.chemenv_strategies import SimplestChemenvStrategy

lgf = LocalGeometryFinder()
lgf.setup_structure(struct)

# Get coordination environment for site
se = lgf.compute_structure_environments(only_indices=[0])
strategy = SimplestChemenvStrategy()
lse = strategy.get_site_coordination_environment(se[0])

print(f"Coordination: {lse}")
```

### Bond Valence Sum

```python
from pymatgen.analysis.bond_valence import BVAnalyzer

bva = BVAnalyzer()

# Calculate oxidation states
valences = bva.get_valences(struct)

# Get structure with oxidation states
struct_with_oxi = bva.get_oxi_state_decorated_structure(struct)
```

## Surface and Interface Analysis

### Surface (Slab) Generation

```python
from pymatgen.core.surface import SlabGenerator, generate_all_slabs

# Generate slabs for a specific Miller index
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,     # Minimum slab thickness (Å)
    min_vacuum_size=10.0,   # Minimum vacuum thickness (Å)
    center_slab=True
)

slabs = slabgen.get_slabs()

# Generate all slabs up to a Miller index
all_slabs = generate_all_slabs(
    struct,
    max_index=2,
    min_slab_size=10.0,
    min_vacuum_size=10.0
)
```

### Wulff Shape Construction

```python
from pymatgen.analysis.wulff import WulffShape

# Define surface energies (J/m²)
surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}

wulff = WulffShape(struct.lattice, surface_energies, symm_reduce=True)

# Get effective radius and surface area
effective_radius = wulff.effective_radius
surface_area = wulff.surface_area
volume = wulff.volume

# Visualize
wulff.show()
```

### Adsorption Site Finding

```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder

asf = AdsorbateSiteFinder(slab)

# Find adsorption sites
ads_sites = asf.find_adsorption_sites()
# Returns dictionary: {"ontop": [...], "bridge": [...], "hollow": [...]}

# Generate structures with adsorbates
from pymatgen.core import Molecule
adsorbate = Molecule("O", [[0, 0, 0]])

ads_structs = asf.generate_adsorption_structures(
    adsorbate,
    repeat=[2, 2, 1],  # Supercell to reduce adsorbate coverage
)
```

### Interface Construction

```python
from pymatgen.analysis.interfaces.coherent_interfaces import CoherentInterfaceBuilder

# Build interface between two materials
builder = CoherentInterfaceBuilder(
    substrate_structure=substrate,
    film_structure=film,
    substrate_miller=(0, 0, 1),
    film_miller=(1, 1, 1),
)

interfaces = builder.get_interfaces()
```

## Magnetism

### Magnetic Structure Analysis

```python
from pymatgen.analysis.magnetism import CollinearMagneticStructureAnalyzer

analyzer = CollinearMagneticStructureAnalyzer(struct)

# Get magnetic ordering
ordering = analyzer.ordering  # e.g., "FM" (ferromagnetic), "AFM", "FiM"

# Get magnetic space group
mag_space_group = analyzer.get_structure_with_spin().get_space_group_info()
```

### Magnetic Ordering Enumeration

```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# Enumerate possible magnetic orderings
mag_trans = MagOrderingTransformation({"Fe": 5.0})  # Magnetic moment in μB
transformed_structures = mag_trans.apply_transformation(struct, return_ranked_list=True)
```

## Electronic Structure Analysis

### Band Structure Analysis

```python
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from pymatgen.electronic_structure.plotter import BSPlotter

# Read band structure from VASP calculation
from pymatgen.io.vasp import Vasprun
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# Get band gap
band_gap = bs.get_band_gap()
# Returns: {'energy': gap_value, 'direct': True/False, 'transition': '...'}

# Check if metal
is_metal = bs.is_metal()

# Get VBM and CBM
vbm = bs.get_vbm()
cbm = bs.get_cbm()

# Plot band structure
plotter = BSPlotter(bs)
plotter.show()
plotter.save_plot("band_structure.png")
```

### Density of States (DOS)

```python
from pymatgen.electronic_structure.dos import CompleteDos
from pymatgen.electronic_structure.plotter import DosPlotter

# Read DOS from VASP calculation
vasprun = Vasprun("vasprun.xml")
dos = vasprun.complete_dos

# Get total DOS
total_dos = dos.densities

# Get projected DOS
pdos = dos.get_element_dos()  # By element
site_dos = dos.get_site_dos(struct[0])  # For specific site
spd_dos = dos.get_spd_dos()  # By orbital (s, p, d)

# Plot DOS
plotter = DosPlotter()
plotter.add_dos("Total", dos)
plotter.show()
```

### Fermi Surface

```python
from pymatgen.electronic_structure.boltztrap2 import BoltztrapRunner

runner = BoltztrapRunner(struct, nelec=n_electrons)
runner.run()

# Get transport properties at different temperatures
results = runner.get_results()
```

## Diffraction

### X-ray Diffraction (XRD)

```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

xrd = XRDCalculator()

pattern = xrd.get_pattern(struct, two_theta_range=(0, 90))

# Get peak data
for peak in pattern.hkls:
    print(f"2θ = {peak['2theta']:.2f}°, hkl = {peak['hkl']}, I = {peak['intensity']:.1f}")

# Plot pattern
pattern.plot()
```

### Neutron Diffraction

```python
from pymatgen.analysis.diffraction.neutron import NDCalculator

nd = NDCalculator()
pattern = nd.get_pattern(struct)
```

## Elasticity and Mechanical Properties

```python
from pymatgen.analysis.elasticity import ElasticTensor, Stress, Strain

# Create elastic tensor from matrix
elastic_tensor = ElasticTensor([[...]])  # 6x6 or 3x3x3x3 matrix

# Get mechanical properties
bulk_modulus = elastic_tensor.k_voigt  # Voigt bulk modulus (GPa)
shear_modulus = elastic_tensor.g_voigt  # Shear modulus (GPa)
youngs_modulus = elastic_tensor.y_mod  # Young's modulus (GPa)

# Apply strain
strain = Strain([[0.01, 0, 0], [0, 0, 0], [0, 0, 0]])
stress = elastic_tensor.calculate_stress(strain)
```

## Reaction Analysis

### Reaction Computation

```python
from pymatgen.analysis.reaction_calculator import ComputedReaction

reactants = [ComputedEntry("Fe", -8.4), ComputedEntry("O2", -4.9)]
products = [ComputedEntry("Fe2O3", -8.3)]

rxn = ComputedReaction(reactants, products)

# Get balanced equation
balanced_rxn = rxn.normalized_repr  # e.g., "2 Fe + 1.5 O2 -> Fe2O3"

# Get reaction energy
energy = rxn.calculated_reaction_energy  # eV per formula unit
```

### Reaction Path Finding

```python
from pymatgen.analysis.path_finder import ChgcarPotential, NEBPathfinder

# Read charge density
chgcar_potential = ChgcarPotential.from_file("CHGCAR")

# Find diffusion path
neb_path = NEBPathfinder(
    start_struct,
    end_struct,
    relax_sites=[i for i in range(len(start_struct))],
    v=chgcar_potential
)

images = neb_path.images  # Interpolated structures for NEB
```

## Molecular Analysis

### Bond Analysis

```python
# Get covalent bonds
bonds = mol.get_covalent_bonds()

for bond in bonds:
    print(f"{bond.site1.species_string} - {bond.site2.species_string}: {bond.length:.2f} Å")
```

### Molecule Graph

```python
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.analysis.local_env import OpenBabelNN

# Build molecule graph
mg = MoleculeGraph.with_local_env_strategy(mol, OpenBabelNN())

# Get fragments
fragments = mg.get_disconnected_fragments()

# Find rings
rings = mg.find_rings()
```

## Spectroscopy

### X-ray Absorption Spectroscopy (XAS)

```python
from pymatgen.analysis.xas.spectrum import XAS

# Read XAS spectrum
xas = XAS.from_file("xas.dat")

# Normalize and process
xas.normalize()
```

## Additional Analysis Tools

### Grain Boundaries

```python
from pymatgen.analysis.gb.grain import GrainBoundaryGenerator

gb_gen = GrainBoundaryGenerator(struct)
gb_structures = gb_gen.generate_grain_boundaries(
    rotation_axis=[0, 0, 1],
    rotation_angle=36.87,  # degrees
)
```

### Prototypes and Structure Matching

```python
from pymatgen.analysis.prototypes import AflowPrototypeMatcher

matcher = AflowPrototypeMatcher()
prototype = matcher.get_prototypes(struct)
```

## Best Practices

1. **Start simple**: Use basic analysis before advanced methods
2. **Validate results**: Cross-check analysis with multiple methods
3. **Consider symmetry**: Use `SpacegroupAnalyzer` to reduce computational cost
4. **Check convergence**: Ensure input structures are well-converged
5. **Use appropriate methods**: Different analyses have different accuracy/speed tradeoffs
6. **Visualize results**: Use built-in plotters for quick validation
7. **Save intermediate results**: Complex analyses can be time-consuming

---

## Reference: Core_Classes

# Pymatgen Core Classes Reference

This reference documents the fundamental classes in `pymatgen.core` that form the foundation for materials analysis.

## Architecture Principles

Pymatgen follows an object-oriented design where elements, sites, and structures are represented as objects. The framework emphasizes periodic boundary conditions for crystal representation while maintaining flexibility for molecular systems.

**Unit Conventions**: All units in pymatgen are typically assumed to be in atomic units:
- Lengths: angstroms (Å)
- Energies: electronvolts (eV)
- Angles: degrees

## Element and Periodic Table

### Element
Represents periodic table elements with comprehensive properties.

**Creation methods:**
```python
from pymatgen.core import Element

# Create from symbol
si = Element("Si")
# Create from atomic number
si = Element.from_Z(14)
# Create from name
si = Element.from_name("silicon")
```

**Key properties:**
- `atomic_mass`: Atomic mass in amu
- `atomic_radius`: Atomic radius in angstroms
- `electronegativity`: Pauling electronegativity
- `ionization_energy`: First ionization energy in eV
- `common_oxidation_states`: List of common oxidation states
- `is_metal`, `is_halogen`, `is_noble_gas`, etc.: Boolean properties
- `X`: Element symbol as string

### Species
Extends Element for charged ions and specific oxidation states.

```python
from pymatgen.core import Species

# Create an Fe2+ ion
fe2 = Species("Fe", 2)
# Or with explicit sign
fe2 = Species("Fe", +2)
```

### DummySpecies
Placeholder atoms for special structural representations (e.g., vacancies).

```python
from pymatgen.core import DummySpecies

vacancy = DummySpecies("X")
```

## Composition

Represents chemical formulas and compositions, enabling chemical analysis and manipulation.

### Creation
```python
from pymatgen.core import Composition

# From string formula
comp = Composition("Fe2O3")
# From dictionary
comp = Composition({"Fe": 2, "O": 3})
# From weight dictionary
comp = Composition.from_weight_dict({"Fe": 111.69, "O": 48.00})
```

### Key methods
- `get_reduced_formula_and_factor()`: Returns reduced formula and multiplication factor
- `oxi_state_guesses()`: Attempts to determine oxidation states
- `replace(replacements_dict)`: Replace elements
- `add_charges_from_oxi_state_guesses()`: Infer and add oxidation states
- `is_element`: Check if composition is a single element

### Key properties
- `weight`: Molecular weight
- `reduced_formula`: Reduced chemical formula
- `hill_formula`: Formula in Hill notation (C, H, then alphabetical)
- `num_atoms`: Total number of atoms
- `chemical_system`: Alphabetically sorted elements (e.g., "Fe-O")
- `element_composition`: Dictionary of element to amount

## Lattice

Defines unit cell geometry for crystal structures.

### Creation
```python
from pymatgen.core import Lattice

# From lattice parameters
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)

# From matrix (row vectors are lattice vectors)
lattice = Lattice([[3.84, 0, 0],
                   [0, 3.84, 0],
                   [0, 0, 3.84]])

# Cubic lattice
lattice = Lattice.cubic(3.84)
# Hexagonal lattice
lattice = Lattice.hexagonal(a=2.95, c=4.68)
```

### Key methods
- `get_niggli_reduced_lattice()`: Returns Niggli-reduced lattice
- `get_distance_and_image(frac_coords1, frac_coords2)`: Distance between fractional coordinates with periodic boundary conditions
- `get_all_distances(frac_coords1, frac_coords2)`: Distances including periodic images

### Key properties
- `volume`: Volume of the unit cell (Å³)
- `abc`: Lattice parameters (a, b, c) as tuple
- `angles`: Lattice angles (alpha, beta, gamma) as tuple
- `matrix`: 3x3 matrix of lattice vectors
- `reciprocal_lattice`: Reciprocal lattice object
- `is_orthogonal`: Whether lattice vectors are orthogonal

## Sites

### Site
Represents an atomic position in non-periodic systems.

```python
from pymatgen.core import Site

site = Site("Si", [0.0, 0.0, 0.0])  # Species and Cartesian coordinates
```

### PeriodicSite
Represents an atomic position in a periodic lattice with fractional coordinates.

```python
from pymatgen.core import PeriodicSite

site = PeriodicSite("Si", [0.5, 0.5, 0.5], lattice)  # Species, fractional coords, lattice
```

**Key methods:**
- `distance(other_site)`: Distance to another site
- `is_periodic_image(other_site)`: Check if sites are periodic images

**Key properties:**
- `species`: Species or element at the site
- `coords`: Cartesian coordinates
- `frac_coords`: Fractional coordinates (for PeriodicSite)
- `x`, `y`, `z`: Individual Cartesian coordinates

## Structure

Represents a crystal structure as a collection of periodic sites. `Structure` is mutable, while `IStructure` is immutable.

### Creation
```python
from pymatgen.core import Structure, Lattice

# From scratch
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
struct = Structure(lattice, ["Si", "Si"], coords)

# From file (automatic format detection)
struct = Structure.from_file("POSCAR")
struct = Structure.from_file("structure.cif")

# From spacegroup
struct = Structure.from_spacegroup("Fm-3m", Lattice.cubic(3.5),
                                   ["Si"], [[0, 0, 0]])
```

### File I/O
```python
# Write to file (format inferred from extension)
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="structure.xyz")

# Get string representation
cif_string = struct.to(fmt="cif")
poscar_string = struct.to(fmt="poscar")
```

### Key methods

**Structure modification:**
- `append(species, coords)`: Add a site
- `insert(i, species, coords)`: Insert site at index
- `remove_sites(indices)`: Remove sites by index
- `replace(i, species)`: Replace species at index
- `apply_strain(strain)`: Apply strain to structure
- `perturb(distance)`: Randomly perturb atomic positions
- `make_supercell(scaling_matrix)`: Create supercell
- `get_primitive_structure()`: Get primitive cell

**Analysis:**
- `get_distance(i, j)`: Distance between sites i and j
- `get_neighbors(site, r)`: Get neighbors within radius r
- `get_all_neighbors(r)`: Get all neighbors for all sites
- `get_space_group_info()`: Get space group information
- `matches(other_struct)`: Check if structures match

**Interpolation:**
- `interpolate(end_structure, nimages)`: Interpolate between structures

### Key properties
- `lattice`: Lattice object
- `species`: List of species at each site
- `sites`: List of PeriodicSite objects
- `num_sites`: Number of sites
- `volume`: Volume of the structure
- `density`: Density in g/cm³
- `composition`: Composition object
- `formula`: Chemical formula
- `distance_matrix`: Matrix of pairwise distances

## Molecule

Represents non-periodic collections of atoms. `Molecule` is mutable, while `IMolecule` is immutable.

### Creation
```python
from pymatgen.core import Molecule

# From scratch
coords = [[0.00, 0.00, 0.00],
          [0.00, 0.00, 1.08]]
mol = Molecule(["C", "O"], coords)

# From file
mol = Molecule.from_file("molecule.xyz")
mol = Molecule.from_file("molecule.mol")
```

### Key methods
- `get_covalent_bonds()`: Returns bonds based on covalent radii
- `get_neighbors(site, r)`: Get neighbors within radius
- `get_zmatrix()`: Get Z-matrix representation
- `get_distance(i, j)`: Distance between sites
- `get_centered_molecule()`: Center molecule at origin

### Key properties
- `species`: List of species
- `sites`: List of Site objects
- `num_sites`: Number of atoms
- `charge`: Total charge of molecule
- `spin_multiplicity`: Spin multiplicity
- `center_of_mass`: Center of mass coordinates

## Serialization

All core objects implement `as_dict()` and `from_dict()` methods for robust JSON/YAML persistence.

```python
# Serialize to dictionary
struct_dict = struct.as_dict()

# Write to JSON
import json
with open("structure.json", "w") as f:
    json.dump(struct_dict, f)

# Read from JSON
with open("structure.json", "r") as f:
    struct_dict = json.load(f)
    struct = Structure.from_dict(struct_dict)
```

This approach addresses limitations of Python pickling and maintains compatibility across pymatgen versions.

## Additional Core Classes

### CovalentBond
Represents bonds in molecules.

**Key properties:**
- `length`: Bond length
- `get_bond_order()`: Returns bond order (single, double, triple)

### Ion
Represents charged ionic species with oxidation states.

```python
from pymatgen.core import Ion

# Create Fe2+ ion
fe2_ion = Ion.from_formula("Fe2+")
```

### Interface
Represents substrate-film combinations for heterojunction analysis.

### GrainBoundary
Represents crystallographic grain boundaries.

### Spectrum
Represents spectroscopic data with methods for normalization and processing.

**Key methods:**
- `normalize(mode="max")`: Normalize spectrum
- `smear(sigma)`: Apply Gaussian smearing

## Best Practices

1. **Immutability**: Use immutable versions (`IStructure`, `IMolecule`) when structures shouldn't be modified
2. **Serialization**: Prefer `as_dict()`/`from_dict()` over pickle for long-term storage
3. **Units**: Always work in atomic units (Å, eV) - conversions are available in `pymatgen.core.units`
4. **File I/O**: Use `from_file()` for automatic format detection
5. **Coordinates**: Pay attention to whether methods expect Cartesian or fractional coordinates

---

## Reference: Io_Formats

# Pymatgen I/O and File Format Reference

This reference documents pymatgen's extensive input/output capabilities for reading and writing structural and computational data across 100+ file formats.

## General I/O Philosophy

Pymatgen provides a unified interface for file operations through the `from_file()` and `to()` methods, with automatic format detection based on file extensions.

### Reading Files

```python
from pymatgen.core import Structure, Molecule

# Automatic format detection
struct = Structure.from_file("POSCAR")
struct = Structure.from_file("structure.cif")
mol = Molecule.from_file("molecule.xyz")

# Explicit format specification
struct = Structure.from_file("file.txt", fmt="cif")
```

### Writing Files

```python
# Write to file (format inferred from extension)
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="structure.xyz")

# Get string representation without writing
cif_string = struct.to(fmt="cif")
poscar_string = struct.to(fmt="poscar")
```

## Structure File Formats

### CIF (Crystallographic Information File)
Standard format for crystallographic data.

```python
from pymatgen.io.cif import CifParser, CifWriter

# Reading
parser = CifParser("structure.cif")
structure = parser.get_structures()[0]  # Returns list of structures

# Writing
writer = CifWriter(struct)
writer.write_file("output.cif")

# Or using convenience methods
struct = Structure.from_file("structure.cif")
struct.to(filename="output.cif")
```

**Key features:**
- Supports symmetry information
- Can contain multiple structures
- Preserves space group and symmetry operations
- Handles partial occupancies

### POSCAR/CONTCAR (VASP)
VASP's structure format.

```python
from pymatgen.io.vasp import Poscar

# Reading
poscar = Poscar.from_file("POSCAR")
structure = poscar.structure

# Writing
poscar = Poscar(struct)
poscar.write_file("POSCAR")

# Or using convenience methods
struct = Structure.from_file("POSCAR")
struct.to(filename="POSCAR")
```

**Key features:**
- Supports selective dynamics
- Can include velocities (XDATCAR format)
- Preserves lattice and coordinate precision

### XYZ
Simple molecular coordinates format.

```python
# For molecules
mol = Molecule.from_file("molecule.xyz")
mol.to(filename="output.xyz")

# For structures (Cartesian coordinates)
struct.to(filename="structure.xyz")
```

### PDB (Protein Data Bank)
Common format for biomolecules.

```python
mol = Molecule.from_file("protein.pdb")
mol.to(filename="output.pdb")
```

### JSON/YAML
Serialization via dictionaries.

```python
import json
import yaml

# JSON
with open("structure.json", "w") as f:
    json.dump(struct.as_dict(), f)

with open("structure.json", "r") as f:
    struct = Structure.from_dict(json.load(f))

# YAML
with open("structure.yaml", "w") as f:
    yaml.dump(struct.as_dict(), f)

with open("structure.yaml", "r") as f:
    struct = Structure.from_dict(yaml.safe_load(f))
```

## Electronic Structure Code I/O

### VASP

The most comprehensive integration in pymatgen.

#### Input Files

```python
from pymatgen.io.vasp.inputs import Incar, Poscar, Potcar, Kpoints, VaspInput

# INCAR (calculation parameters)
incar = Incar.from_file("INCAR")
incar = Incar({"ENCUT": 520, "ISMEAR": 0, "SIGMA": 0.05})
incar.write_file("INCAR")

# KPOINTS (k-point mesh)
from pymatgen.io.vasp.inputs import Kpoints
kpoints = Kpoints.automatic(20)  # 20x20x20 Gamma-centered mesh
kpoints = Kpoints.automatic_density(struct, 1000)  # By density
kpoints.write_file("KPOINTS")

# POTCAR (pseudopotentials)
potcar = Potcar(["Fe_pv", "O"])  # Specify functional variants

# Complete input set
vasp_input = VaspInput(incar, kpoints, poscar, potcar)
vasp_input.write_input("./vasp_calc")
```

#### Output Files

```python
from pymatgen.io.vasp.outputs import Vasprun, Outcar, Oszicar, Eigenval

# vasprun.xml (comprehensive output)
vasprun = Vasprun("vasprun.xml")
final_structure = vasprun.final_structure
energy = vasprun.final_energy
band_structure = vasprun.get_band_structure()
dos = vasprun.complete_dos

# OUTCAR
outcar = Outcar("OUTCAR")
magnetization = outcar.total_mag
elastic_tensor = outcar.elastic_tensor

# OSZICAR (convergence information)
oszicar = Oszicar("OSZICAR")
```

#### Input Sets

Pymatgen provides pre-configured input sets for common calculations:

```python
from pymatgen.io.vasp.sets import (
    MPRelaxSet,      # Materials Project relaxation
    MPStaticSet,     # Static calculation
    MPNonSCFSet,     # Non-self-consistent (band structure)
    MPSOCSet,        # Spin-orbit coupling
    MPHSERelaxSet,   # HSE06 hybrid functional
)

# Create input set
relax = MPRelaxSet(struct)
relax.write_input("./relax_calc")

# Customize parameters
static = MPStaticSet(struct, user_incar_settings={"ENCUT": 600})
static.write_input("./static_calc")
```

### Gaussian

Quantum chemistry package integration.

```python
from pymatgen.io.gaussian import GaussianInput, GaussianOutput

# Input
gin = GaussianInput(
    mol,
    charge=0,
    spin_multiplicity=1,
    functional="B3LYP",
    basis_set="6-31G(d)",
    route_parameters={"Opt": None, "Freq": None}
)
gin.write_file("input.gjf")

# Output
gout = GaussianOutput("output.log")
final_mol = gout.final_structure
energy = gout.final_energy
frequencies = gout.frequencies
```

### LAMMPS

Classical molecular dynamics.

```python
from pymatgen.io.lammps.data import LammpsData
from pymatgen.io.lammps.inputs import LammpsInputFile

# Structure to LAMMPS data file
lammps_data = LammpsData.from_structure(struct)
lammps_data.write_file("data.lammps")

# LAMMPS input script
lammps_input = LammpsInputFile.from_file("in.lammps")
```

### Quantum ESPRESSO

```python
from pymatgen.io.pwscf import PWInput, PWOutput

# Input
pwin = PWInput(
    struct,
    control={"calculation": "scf"},
    system={"ecutwfc": 50, "ecutrho": 400},
    electrons={"conv_thr": 1e-8}
)
pwin.write_file("pw.in")

# Output
pwout = PWOutput("pw.out")
final_structure = pwout.final_structure
energy = pwout.final_energy
```

### ABINIT

```python
from pymatgen.io.abinit import AbinitInput

abin = AbinitInput(struct, pseudos)
abin.set_vars(ecut=10, nband=10)
abin.write("abinit.in")
```

### CP2K

```python
from pymatgen.io.cp2k.inputs import Cp2kInput
from pymatgen.io.cp2k.outputs import Cp2kOutput

# Input
cp2k_input = Cp2kInput.from_file("cp2k.inp")

# Output
cp2k_output = Cp2kOutput("cp2k.out")
```

### FEFF (XAS/XANES)

```python
from pymatgen.io.feff import FeffInput

feff_input = FeffInput(struct, absorbing_atom="Fe")
feff_input.write_file("feff.inp")
```

### LMTO (Stuttgart TB-LMTO-ASA)

```python
from pymatgen.io.lmto import LMTOCtrl

ctrl = LMTOCtrl.from_file("CTRL")
ctrl.structure
```

### Q-Chem

```python
from pymatgen.io.qchem.inputs import QCInput
from pymatgen.io.qchem.outputs import QCOutput

# Input
qc_input = QCInput(
    mol,
    rem={"method": "B3LYP", "basis": "6-31G*", "job_type": "opt"}
)
qc_input.write_file("mol.qin")

# Output
qc_output = QCOutput("mol.qout")
```

### Exciting

```python
from pymatgen.io.exciting import ExcitingInput

exc_input = ExcitingInput(struct)
exc_input.write_file("input.xml")
```

### ATAT (Alloy Theoretic Automated Toolkit)

```python
from pymatgen.io.atat import Mcsqs

mcsqs = Mcsqs(struct)
mcsqs.write_input(".")
```

## Special Purpose Formats

### Phonopy

```python
from pymatgen.io.phonopy import get_phonopy_structure, get_pmg_structure

# Convert to phonopy structure
phonopy_struct = get_phonopy_structure(struct)

# Convert from phonopy
struct = get_pmg_structure(phonopy_struct)
```

### ASE (Atomic Simulation Environment)

```python
from pymatgen.io.ase import AseAtomsAdaptor

adaptor = AseAtomsAdaptor()

# Pymatgen to ASE
atoms = adaptor.get_atoms(struct)

# ASE to Pymatgen
struct = adaptor.get_structure(atoms)
```

### Zeo++ (Porous Materials)

```python
from pymatgen.io.zeopp import get_voronoi_nodes, get_high_accuracy_voronoi_nodes

# Analyze pore structure
vor_nodes = get_voronoi_nodes(struct)
```

### BabelMolAdaptor (OpenBabel)

```python
from pymatgen.io.babel import BabelMolAdaptor

adaptor = BabelMolAdaptor(mol)

# Convert to different formats
pdb_str = adaptor.pdbstring
sdf_str = adaptor.write_file("mol.sdf", file_format="sdf")

# Generate 3D coordinates
adaptor.add_hydrogen()
adaptor.make3d()
```

## Alchemy and Transformation I/O

### TransformedStructure

Structures that track their transformation history.

```python
from pymatgen.alchemy.materials import TransformedStructure
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation
)

# Create transformed structure
ts = TransformedStructure(struct, [])
ts.append_transformation(SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]]))
ts.append_transformation(SubstitutionTransformation({"Fe": "Mn"}))

# Write with history
ts.write_vasp_input("./calc_dir")

# Read from SNL (Structure Notebook Language)
ts = TransformedStructure.from_snl(snl)
```

## Batch Operations

### CifTransmuter

Process multiple CIF files.

```python
from pymatgen.alchemy.transmuters import CifTransmuter

transmuter = CifTransmuter.from_filenames(
    ["structure1.cif", "structure2.cif"],
    [SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])]
)

# Write all structures
transmuter.write_vasp_input("./batch_calc")
```

### PoscarTransmuter

Similar for POSCAR files.

```python
from pymatgen.alchemy.transmuters import PoscarTransmuter

transmuter = PoscarTransmuter.from_filenames(
    ["POSCAR1", "POSCAR2"],
    [transformation1, transformation2]
)
```

## Best Practices

1. **Automatic format detection**: Use `from_file()` and `to()` methods whenever possible
2. **Error handling**: Always wrap file I/O in try-except blocks
3. **Format-specific parsers**: Use specialized parsers (e.g., `Vasprun`) for detailed output analysis
4. **Input sets**: Prefer pre-configured input sets over manual parameter specification
5. **Serialization**: Use JSON/YAML for long-term storage and version control
6. **Batch processing**: Use transmuters for applying transformations to multiple structures

## Supported Format Summary

### Structure formats:
CIF, POSCAR/CONTCAR, XYZ, PDB, XSF, PWMAT, Res, CSSR, JSON, YAML

### Electronic structure codes:
VASP, Gaussian, LAMMPS, Quantum ESPRESSO, ABINIT, CP2K, FEFF, Q-Chem, LMTO, Exciting, NWChem, AIMS, Crystallographic data formats

### Molecular formats:
XYZ, PDB, MOL, SDF, PQR, via OpenBabel (many additional formats)

### Special purpose:
Phonopy, ASE, Zeo++, Lobster, BoltzTraP

---

## Reference: Materials_Project_Api

# Materials Project API Reference

This reference documents how to access and use the Materials Project database through pymatgen's API integration.

## Overview

The Materials Project is a comprehensive database of computed materials properties, containing data on hundreds of thousands of inorganic crystals and molecules. The API provides programmatic access to this data through the `MPRester` client.

## Installation and Setup

The Materials Project API client is now in a separate package:

```bash
pip install mp-api
```

### Getting an API Key

1. Visit https://next-gen.materialsproject.org/
2. Create an account or log in
3. Navigate to your dashboard/settings
4. Generate an API key
5. Store it as an environment variable:

```bash
export MP_API_KEY="your_api_key_here"
```

Or add to your shell configuration file (~/.bashrc, ~/.zshrc, etc.)

## Basic Usage

### Initialization

```python
from mp_api.client import MPRester

# Using environment variable (recommended)
with MPRester() as mpr:
    # Perform queries
    pass

# Or explicitly pass API key
with MPRester("your_api_key_here") as mpr:
    # Perform queries
    pass
```

**Important**: Always use the `with` context manager to ensure sessions are properly closed.

## Querying Materials Data

### Search by Formula

```python
with MPRester() as mpr:
    # Get all materials with formula
    materials = mpr.materials.summary.search(formula="Fe2O3")

    for mat in materials:
        print(f"Material ID: {mat.material_id}")
        print(f"Formula: {mat.formula_pretty}")
        print(f"Energy above hull: {mat.energy_above_hull} eV/atom")
        print(f"Band gap: {mat.band_gap} eV")
        print()
```

### Search by Material ID

```python
with MPRester() as mpr:
    # Get specific material
    material = mpr.materials.summary.search(material_ids=["mp-149"])[0]

    print(f"Formula: {material.formula_pretty}")
    print(f"Space group: {material.symmetry.symbol}")
    print(f"Density: {material.density} g/cm³")
```

### Search by Chemical System

```python
with MPRester() as mpr:
    # Get all materials in Fe-O system
    materials = mpr.materials.summary.search(chemsys="Fe-O")

    # Get materials in ternary system
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")
```

### Search by Elements

```python
with MPRester() as mpr:
    # Materials containing Fe and O
    materials = mpr.materials.summary.search(elements=["Fe", "O"])

    # Materials containing ONLY Fe and O (excluding others)
    materials = mpr.materials.summary.search(
        elements=["Fe", "O"],
        exclude_elements=True
    )
```

## Getting Structures

### Structure from Material ID

```python
with MPRester() as mpr:
    # Get structure
    structure = mpr.get_structure_by_material_id("mp-149")

    # Get multiple structures
    structures = mpr.get_structures(["mp-149", "mp-510", "mp-19017"])
```

### All Structures for a Formula

```python
with MPRester() as mpr:
    # Get all Fe2O3 structures
    materials = mpr.materials.summary.search(formula="Fe2O3")

    for mat in materials:
        structure = mpr.get_structure_by_material_id(mat.material_id)
        print(f"{mat.material_id}: {structure.get_space_group_info()}")
```

## Advanced Queries

### Property Filtering

```python
with MPRester() as mpr:
    # Materials with specific property ranges
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Stable or near-stable
        band_gap=(1.0, 3.0),           # Semiconducting
    )

    # Magnetic materials
    materials = mpr.materials.summary.search(
        elements=["Fe"],
        is_magnetic=True
    )

    # Metals only
    materials = mpr.materials.summary.search(
        chemsys="Fe-Ni",
        is_metal=True
    )
```

### Sorting and Limiting

```python
with MPRester() as mpr:
    # Get most stable materials
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        sort_fields=["energy_above_hull"],
        num_chunks=1,
        chunk_size=10  # Limit to 10 results
    )
```

## Electronic Structure Data

### Band Structure

```python
with MPRester() as mpr:
    # Get band structure
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Analyze band structure
    if bs:
        print(f"Band gap: {bs.get_band_gap()}")
        print(f"Is metal: {bs.is_metal()}")
        print(f"Direct gap: {bs.get_band_gap()['direct']}")

        # Plot
        from pymatgen.electronic_structure.plotter import BSPlotter
        plotter = BSPlotter(bs)
        plotter.show()
```

### Density of States

```python
with MPRester() as mpr:
    # Get DOS
    dos = mpr.get_dos_by_material_id("mp-149")

    if dos:
        # Get band gap from DOS
        gap = dos.get_gap()
        print(f"Band gap from DOS: {gap} eV")

        # Plot DOS
        from pymatgen.electronic_structure.plotter import DosPlotter
        plotter = DosPlotter()
        plotter.add_dos("Total DOS", dos)
        plotter.show()
```

### Fermi Surface

```python
with MPRester() as mpr:
    # Get electronic structure data for Fermi surface
    bs = mpr.get_bandstructure_by_material_id("mp-149", line_mode=False)
```

## Thermodynamic Data

### Phase Diagram Construction

```python
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

with MPRester() as mpr:
    # Get entries for phase diagram
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

    # Build phase diagram
    pd = PhaseDiagram(entries)

    # Plot
    plotter = PDPlotter(pd)
    plotter.show()
```

### Pourbaix Diagram

```python
from pymatgen.analysis.pourbaix_diagram import PourbaixDiagram, PourbaixPlotter

with MPRester() as mpr:
    # Get entries for Pourbaix diagram
    entries = mpr.get_pourbaix_entries(["Fe"])

    # Build Pourbaix diagram
    pb = PourbaixDiagram(entries)

    # Plot
    plotter = PourbaixPlotter(pb)
    plotter.show()
```

### Formation Energy

```python
with MPRester() as mpr:
    materials = mpr.materials.summary.search(material_ids=["mp-149"])

    for mat in materials:
        print(f"Formation energy: {mat.formation_energy_per_atom} eV/atom")
        print(f"Energy above hull: {mat.energy_above_hull} eV/atom")
```

## Elasticity and Mechanical Properties

```python
with MPRester() as mpr:
    # Search for materials with elastic data
    materials = mpr.materials.elasticity.search(
        chemsys="Fe-O",
        bulk_modulus_vrh=(100, 300)  # GPa
    )

    for mat in materials:
        print(f"{mat.material_id}: K = {mat.bulk_modulus_vrh} GPa")
```

## Dielectric Properties

```python
with MPRester() as mpr:
    # Get dielectric data
    materials = mpr.materials.dielectric.search(
        material_ids=["mp-149"]
    )

    for mat in materials:
        print(f"Dielectric constant: {mat.e_electronic}")
        print(f"Refractive index: {mat.n}")
```

## Piezoelectric Properties

```python
with MPRester() as mpr:
    # Get piezoelectric materials
    materials = mpr.materials.piezoelectric.search(
        piezoelectric_modulus=(1, 100)
    )
```

## Surface Properties

```python
with MPRester() as mpr:
    # Get surface data
    surfaces = mpr.materials.surface_properties.search(
        material_ids=["mp-149"]
    )
```

## Molecule Data (For Molecular Materials)

```python
with MPRester() as mpr:
    # Search molecules
    molecules = mpr.molecules.summary.search(
        formula="H2O"
    )

    for mol in molecules:
        print(f"Molecule ID: {mol.molecule_id}")
        print(f"Formula: {mol.formula_pretty}")
```

## Bulk Data Download

### Download All Data for Materials

```python
with MPRester() as mpr:
    # Get comprehensive data
    materials = mpr.materials.summary.search(
        material_ids=["mp-149"],
        fields=[
            "material_id",
            "formula_pretty",
            "structure",
            "energy_above_hull",
            "band_gap",
            "density",
            "symmetry",
            "elasticity",
            "magnetic_ordering"
        ]
    )
```

## Provenance and Calculation Details

```python
with MPRester() as mpr:
    # Get calculation details
    materials = mpr.materials.summary.search(
        material_ids=["mp-149"],
        fields=["material_id", "origins"]
    )

    for mat in materials:
        print(f"Origins: {mat.origins}")
```

## Working with Entries

### ComputedEntry for Thermodynamic Analysis

```python
with MPRester() as mpr:
    # Get entries (includes energy and composition)
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

    # Entries can be used directly in phase diagram analysis
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    pd = PhaseDiagram(entries)

    # Check stability
    for entry in entries[:5]:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"{entry.composition.reduced_formula}: {e_above_hull:.3f} eV/atom")
```

## Rate Limiting and Best Practices

### Rate Limits

The Materials Project API has rate limits to ensure fair usage:
- Be mindful of request frequency
- Use batch queries when possible
- Cache results locally for repeated analysis

### Efficient Querying

```python
# Bad: Multiple separate queries
with MPRester() as mpr:
    for mp_id in ["mp-149", "mp-510", "mp-19017"]:
        struct = mpr.get_structure_by_material_id(mp_id)  # 3 API calls

# Good: Single batch query
with MPRester() as mpr:
    structs = mpr.get_structures(["mp-149", "mp-510", "mp-19017"])  # 1 API call
```

### Caching Results

```python
import json

# Save results for later use
with MPRester() as mpr:
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # Save to file
    with open("li_fe_o_materials.json", "w") as f:
        json.dump([mat.dict() for mat in materials], f)

# Load cached results
with open("li_fe_o_materials.json", "r") as f:
    cached_data = json.load(f)
```

## Error Handling

```python
from mp_api.client.core.client import MPRestError

try:
    with MPRester() as mpr:
        materials = mpr.materials.summary.search(material_ids=["invalid-id"])
except MPRestError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Use Cases

### Finding Stable Compounds

```python
with MPRester() as mpr:
    # Get all stable compounds in a chemical system
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.001)  # Essentially on convex hull
    )

    print(f"Found {len(materials)} stable compounds")
    for mat in materials:
        print(f"  {mat.formula_pretty} ({mat.material_id})")
```

### Battery Material Screening

```python
with MPRester() as mpr:
    # Screen for potential cathode materials
    materials = mpr.materials.summary.search(
        elements=["Li"],  # Must contain Li
        energy_above_hull=(0, 0.05),  # Near stable
        band_gap=(0, 0.5),  # Metallic or small gap
    )

    print(f"Found {len(materials)} potential cathode materials")
```

### Finding Materials with Specific Crystal Structure

```python
with MPRester() as mpr:
    # Find materials with specific space group
    materials = mpr.materials.summary.search(
        chemsys="Fe-O",
        spacegroup_number=167  # R-3c (corundum structure)
    )
```

## Integration with Other Pymatgen Features

All data retrieved from the Materials Project can be directly used with pymatgen's analysis tools:

```python
with MPRester() as mpr:
    # Get structure
    struct = mpr.get_structure_by_material_id("mp-149")

    # Use with pymatgen analysis
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    sga = SpacegroupAnalyzer(struct)

    # Generate surfaces
    from pymatgen.core.surface import SlabGenerator
    slabgen = SlabGenerator(struct, (1,0,0), 10, 10)
    slabs = slabgen.get_slabs()

    # Phase diagram analysis
    entries = mpr.get_entries_in_chemsys(struct.composition.chemical_system)
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    pd = PhaseDiagram(entries)
```

## Additional Resources

- **API Documentation**: https://docs.materialsproject.org/
- **Materials Project Website**: https://next-gen.materialsproject.org/
- **GitHub**: https://github.com/materialsproject/api
- **Forum**: https://matsci.org/

## Best Practices Summary

1. **Always use context manager**: Use `with MPRester() as mpr:`
2. **Store API key as environment variable**: Never hardcode API keys
3. **Batch queries**: Request multiple items at once when possible
4. **Cache results**: Save frequently used data locally
5. **Handle errors**: Wrap API calls in try-except blocks
6. **Be specific**: Use filters to limit results and reduce data transfer
7. **Check data availability**: Not all properties are available for all materials

---

## Reference: Transformations_Workflows

# Pymatgen Transformations and Common Workflows

This reference documents pymatgen's transformation framework and provides recipes for common materials science workflows.

## Transformation Framework

Transformations provide a systematic way to modify structures while tracking the history of modifications.

### Standard Transformations

Located in `pymatgen.transformations.standard_transformations`.

#### SupercellTransformation

Create supercells with arbitrary scaling matrices.

```python
from pymatgen.transformations.standard_transformations import SupercellTransformation

# Simple 2x2x2 supercell
trans = SupercellTransformation([[2,0,0], [0,2,0], [0,0,2]])
new_struct = trans.apply_transformation(struct)

# Non-orthogonal supercell
trans = SupercellTransformation([[2,1,0], [0,2,0], [0,0,2]])
new_struct = trans.apply_transformation(struct)
```

#### SubstitutionTransformation

Replace species in a structure.

```python
from pymatgen.transformations.standard_transformations import SubstitutionTransformation

# Replace all Fe with Mn
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# Partial substitution (50% Fe -> Mn)
trans = SubstitutionTransformation({"Fe": {"Mn": 0.5, "Fe": 0.5}})
new_struct = trans.apply_transformation(struct)
```

#### RemoveSpeciesTransformation

Remove specific species from structure.

```python
from pymatgen.transformations.standard_transformations import RemoveSpeciesTransformation

trans = RemoveSpeciesTransformation(["H"])  # Remove all hydrogen
new_struct = trans.apply_transformation(struct)
```

#### OrderDisorderedStructureTransformation

Order disordered structures with partial occupancies.

```python
from pymatgen.transformations.standard_transformations import OrderDisorderedStructureTransformation

trans = OrderDisorderedStructureTransformation()
new_struct = trans.apply_transformation(disordered_struct)
```

#### PrimitiveCellTransformation

Convert to primitive cell.

```python
from pymatgen.transformations.standard_transformations import PrimitiveCellTransformation

trans = PrimitiveCellTransformation()
primitive_struct = trans.apply_transformation(struct)
```

#### ConventionalCellTransformation

Convert to conventional cell.

```python
from pymatgen.transformations.standard_transformations import ConventionalCellTransformation

trans = ConventionalCellTransformation()
conventional_struct = trans.apply_transformation(struct)
```

#### RotationTransformation

Rotate structure.

```python
from pymatgen.transformations.standard_transformations import RotationTransformation

# Rotate by axis and angle
trans = RotationTransformation([0, 0, 1], 45)  # 45° around z-axis
new_struct = trans.apply_transformation(struct)
```

#### ScaleToRelaxedTransformation

Scale lattice to match a relaxed structure.

```python
from pymatgen.transformations.standard_transformations import ScaleToRelaxedTransformation

trans = ScaleToRelaxedTransformation(relaxed_struct)
scaled_struct = trans.apply_transformation(unrelaxed_struct)
```

### Advanced Transformations

Located in `pymatgen.transformations.advanced_transformations`.

#### EnumerateStructureTransformation

Enumerate all symmetrically distinct ordered structures from a disordered structure.

```python
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation

# Enumerate structures up to max 8 atoms per unit cell
trans = EnumerateStructureTransformation(max_cell_size=8)
structures = trans.apply_transformation(struct, return_ranked_list=True)

# Returns list of ranked structures
for s in structures[:5]:  # Top 5 structures
    print(f"Energy: {s['energy']}, Structure: {s['structure']}")
```

#### MagOrderingTransformation

Enumerate magnetic orderings.

```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# Specify magnetic moments for each species
trans = MagOrderingTransformation({"Fe": 5.0, "Ni": 2.0})
mag_structures = trans.apply_transformation(struct, return_ranked_list=True)
```

#### DopingTransformation

Systematically dope a structure.

```python
from pymatgen.transformations.advanced_transformations import DopingTransformation

# Replace 12.5% of Fe sites with Mn
trans = DopingTransformation("Mn", min_length=10)
doped_structs = trans.apply_transformation(struct, return_ranked_list=True)
```

#### ChargeBalanceTransformation

Balance charge in a structure by oxidation state manipulation.

```python
from pymatgen.transformations.advanced_transformations import ChargeBalanceTransformation

trans = ChargeBalanceTransformation("Li")
charged_struct = trans.apply_transformation(struct)
```

#### SlabTransformation

Generate surface slabs.

```python
from pymatgen.transformations.advanced_transformations import SlabTransformation

trans = SlabTransformation(
    miller_index=[1, 0, 0],
    min_slab_size=10,
    min_vacuum_size=10,
    shift=0,
    lll_reduce=True
)
slab = trans.apply_transformation(struct)
```

### Chaining Transformations

```python
from pymatgen.alchemy.materials import TransformedStructure

# Create transformed structure that tracks history
ts = TransformedStructure(struct, [])

# Apply multiple transformations
ts.append_transformation(SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]]))
ts.append_transformation(SubstitutionTransformation({"Fe": "Mn"}))
ts.append_transformation(PrimitiveCellTransformation())

# Get final structure
final_struct = ts.final_structure

# View transformation history
print(ts.history)
```

## Common Workflows

### Workflow 1: High-Throughput Structure Generation

Generate multiple structures for screening studies.

```python
from pymatgen.core import Structure
from pymatgen.transformations.standard_transformations import (
    SubstitutionTransformation,
    SupercellTransformation
)
from pymatgen.io.vasp.sets import MPRelaxSet

# Starting structure
base_struct = Structure.from_file("POSCAR")

# Define substitutions
dopants = ["Mn", "Co", "Ni", "Cu"]
structures = {}

for dopant in dopants:
    # Create substituted structure
    trans = SubstitutionTransformation({"Fe": dopant})
    new_struct = trans.apply_transformation(base_struct)

    # Generate VASP inputs
    vasp_input = MPRelaxSet(new_struct)
    vasp_input.write_input(f"./calcs/Fe_{dopant}")

    structures[dopant] = new_struct

print(f"Generated {len(structures)} structures")
```

### Workflow 2: Phase Diagram Construction

Build and analyze phase diagrams from Materials Project data.

```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
from pymatgen.core import Composition

# Get data from Materials Project
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

# Build phase diagram
pd = PhaseDiagram(entries)

# Analyze specific composition
comp = Composition("LiFeO2")
e_above_hull = pd.get_e_above_hull(entries[0])

# Get decomposition products
decomp = pd.get_decomposition(comp)
print(f"Decomposition: {decomp}")

# Visualize
plotter = PDPlotter(pd)
plotter.show()
```

### Workflow 3: Surface Energy Calculation

Calculate surface energies from slab calculations.

```python
from pymatgen.core.surface import SlabGenerator, generate_all_slabs
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet
from pymatgen.core import Structure

# Read bulk structure
bulk = Structure.from_file("bulk_POSCAR")

# Get bulk energy (from previous calculation)
from pymatgen.io.vasp import Vasprun
bulk_vasprun = Vasprun("bulk/vasprun.xml")
bulk_energy_per_atom = bulk_vasprun.final_energy / len(bulk)

# Generate slabs
miller_indices = [(1,0,0), (1,1,0), (1,1,1)]
surface_energies = {}

for miller in miller_indices:
    slabgen = SlabGenerator(
        bulk,
        miller_index=miller,
        min_slab_size=10,
        min_vacuum_size=15,
        center_slab=True
    )

    slab = slabgen.get_slabs()[0]

    # Write VASP input for slab
    relax = MPRelaxSet(slab)
    relax.write_input(f"./slab_{miller[0]}{miller[1]}{miller[2]}")

    # After calculation, compute surface energy:
    # slab_vasprun = Vasprun(f"slab_{miller[0]}{miller[1]}{miller[2]}/vasprun.xml")
    # slab_energy = slab_vasprun.final_energy
    # n_atoms = len(slab)
    # area = slab.surface_area  # in Ų
    #
    # # Surface energy (J/m²)
    # surf_energy = (slab_energy - n_atoms * bulk_energy_per_atom) / (2 * area)
    # surf_energy *= 16.021766  # Convert eV/Ų to J/m²
    # surface_energies[miller] = surf_energy

print(f"Set up calculations for {len(miller_indices)} surfaces")
```

### Workflow 4: Band Structure Calculation

Complete workflow for band structure calculations.

```python
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet
from pymatgen.symmetry.bandstructure import HighSymmKpath

# Step 1: Relaxation
struct = Structure.from_file("initial_POSCAR")
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# After relaxation, read structure
relaxed_struct = Structure.from_file("1_relax/CONTCAR")

# Step 2: Static calculation
static = MPStaticSet(relaxed_struct)
static.write_input("./2_static")

# Step 3: Band structure (non-self-consistent)
kpath = HighSymmKpath(relaxed_struct)
nscf = MPNonSCFSet(relaxed_struct, mode="line")  # Band structure mode
nscf.write_input("./3_bandstructure")

# After calculations, analyze
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

vasprun = Vasprun("3_bandstructure/vasprun.xml")
bs = vasprun.get_band_structure(line_mode=True)

print(f"Band gap: {bs.get_band_gap()}")

plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

### Workflow 5: Molecular Dynamics Setup

Set up and analyze molecular dynamics simulations.

```python
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MVLRelaxSet
from pymatgen.io.vasp.inputs import Incar

# Read structure
struct = Structure.from_file("POSCAR")

# Create 2x2x2 supercell for MD
from pymatgen.transformations.standard_transformations import SupercellTransformation
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# Set up VASP input
md_input = MVLRelaxSet(supercell)

# Modify INCAR for MD
incar = md_input.incar
incar.update({
    "IBRION": 0,      # Molecular dynamics
    "NSW": 1000,      # Number of steps
    "POTIM": 2,       # Time step (fs)
    "TEBEG": 300,     # Initial temperature (K)
    "TEEND": 300,     # Final temperature (K)
    "SMASS": 0,       # NVT ensemble
    "MDALGO": 2,      # Nose-Hoover thermostat
})

md_input.incar = incar
md_input.write_input("./md_calc")
```

### Workflow 6: Diffusion Analysis

Analyze ion diffusion from AIMD trajectories.

```python
from pymatgen.io.vasp import Xdatcar
from pymatgen.analysis.diffusion.analyzer import DiffusionAnalyzer

# Read trajectory from XDATCAR
xdatcar = Xdatcar("XDATCAR")
structures = xdatcar.structures

# Analyze diffusion for specific species (e.g., Li)
analyzer = DiffusionAnalyzer.from_structures(
    structures,
    specie="Li",
    temperature=300,  # K
    time_step=2,      # fs
    step_skip=10      # Skip initial equilibration
)

# Get diffusivity
diffusivity = analyzer.diffusivity  # cm²/s
conductivity = analyzer.conductivity  # mS/cm

# Get mean squared displacement
msd = analyzer.msd

# Plot MSD
analyzer.plot_msd()

print(f"Diffusivity: {diffusivity:.2e} cm²/s")
print(f"Conductivity: {conductivity:.2e} mS/cm")
```

### Workflow 7: Structure Prediction and Enumeration

Predict and enumerate possible structures.

```python
from pymatgen.core import Structure, Lattice
from pymatgen.transformations.advanced_transformations import (
    EnumerateStructureTransformation,
    SubstitutionTransformation
)

# Start with a known structure type (e.g., rocksalt)
lattice = Lattice.cubic(4.2)
struct = Structure.from_spacegroup("Fm-3m", lattice, ["Li", "O"], [[0,0,0], [0.5,0.5,0.5]])

# Create disordered structure
from pymatgen.core import Species
species_on_site = {Species("Li"): 0.5, Species("Na"): 0.5}
struct[0] = species_on_site  # Mixed occupancy on Li site

# Enumerate all ordered structures
trans = EnumerateStructureTransformation(max_cell_size=4)
ordered_structs = trans.apply_transformation(struct, return_ranked_list=True)

print(f"Found {len(ordered_structs)} distinct ordered structures")

# Write all structures
for i, s_dict in enumerate(ordered_structs[:10]):  # Top 10
    s_dict['structure'].to(filename=f"ordered_struct_{i}.cif")
```

### Workflow 8: Elastic Constant Calculation

Calculate elastic constants using the stress-strain method.

```python
from pymatgen.core import Structure
from pymatgen.transformations.standard_transformations import DeformStructureTransformation
from pymatgen.io.vasp.sets import MPStaticSet

# Read equilibrium structure
struct = Structure.from_file("relaxed_POSCAR")

# Generate deformed structures
strains = [0.00, 0.01, 0.02, -0.01, -0.02]  # Applied strains
deformation_sets = []

for strain in strains:
    # Apply strain in different directions
    trans = DeformStructureTransformation([[1+strain, 0, 0], [0, 1, 0], [0, 0, 1]])
    deformed = trans.apply_transformation(struct)

    # Set up VASP calculation
    static = MPStaticSet(deformed)
    static.write_input(f"./strain_{strain:.2f}")

# After calculations, fit stress vs strain to get elastic constants
# from pymatgen.analysis.elasticity import ElasticTensor
# ... (collect stress tensors from OUTCAR)
# elastic_tensor = ElasticTensor.from_stress_list(stress_list)
```

### Workflow 9: Adsorption Energy Calculation

Calculate adsorption energies on surfaces.

```python
from pymatgen.core import Structure, Molecule
from pymatgen.core.surface import SlabGenerator
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.io.vasp.sets import MPRelaxSet

# Generate slab
bulk = Structure.from_file("bulk_POSCAR")
slabgen = SlabGenerator(bulk, (1,1,1), 10, 10)
slab = slabgen.get_slabs()[0]

# Find adsorption sites
asf = AdsorbateSiteFinder(slab)
ads_sites = asf.find_adsorption_sites()

# Create adsorbate
adsorbate = Molecule("O", [[0, 0, 0]])

# Generate structures with adsorbate
ads_structs = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])

# Set up calculations
relax_slab = MPRelaxSet(slab)
relax_slab.write_input("./slab")

relax_ads = MPRelaxSet(ads_structs)
relax_ads.write_input("./slab_with_adsorbate")

# After calculations:
# E_ads = E(slab+adsorbate) - E(slab) - E(adsorbate_gas)
```

### Workflow 10: High-Throughput Materials Screening

Screen materials database for specific properties.

```python
from mp_api.client import MPRester
from pymatgen.core import Structure
import pandas as pd

# Define screening criteria
def screen_material(material):
    """Screen for potential battery cathode materials"""
    criteria = {
        "has_li": "Li" in material.composition.elements,
        "stable": material.energy_above_hull < 0.05,
        "good_voltage": 2.5 < material.formation_energy_per_atom < 4.5,
        "electronically_conductive": material.band_gap < 0.5
    }
    return all(criteria.values()), criteria

# Query Materials Project
with MPRester() as mpr:
    # Get potential materials
    materials = mpr.materials.summary.search(
        elements=["Li"],
        energy_above_hull=(0, 0.05),
    )

    results = []
    for mat in materials:
        passes, criteria = screen_material(mat)
        if passes:
            results.append({
                "material_id": mat.material_id,
                "formula": mat.formula_pretty,
                "energy_above_hull": mat.energy_above_hull,
                "band_gap": mat.band_gap,
            })

    # Save results
    df = pd.DataFrame(results)
    df.to_csv("screened_materials.csv", index=False)

    print(f"Found {len(results)} promising materials")
```

## Best Practices for Workflows

1. **Modular design**: Break workflows into discrete steps
2. **Error handling**: Check file existence and calculation convergence
3. **Documentation**: Track transformation history using `TransformedStructure`
4. **Version control**: Store input parameters and scripts in git
5. **Automation**: Use workflow managers (Fireworks, AiiDA) for complex pipelines
6. **Data management**: Organize calculations in clear directory structures
7. **Validation**: Always validate intermediate results before proceeding

## Integration with Workflow Tools

Pymatgen integrates with several workflow management systems:

- **Atomate**: Pre-built VASP workflows
- **Fireworks**: Workflow execution engine
- **AiiDA**: Provenance tracking and workflow management
- **Custodian**: Error correction and job monitoring

These tools provide robust automation for production calculations.
