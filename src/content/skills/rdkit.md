---
title: "Rdkit"
description: "Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure search, 2D/3D generation, similarity, reactions. For standard workflows with simpler interface, use datamol (w..."
category: "workflow"
source: "community"
author: "Community"
tags: ["rdkit"]
date: 2026-03-20
---

# RDKit Cheminformatics Toolkit

## Overview

RDKit is a comprehensive cheminformatics library providing Python APIs for molecular analysis and manipulation. This skill provides guidance for reading/writing molecular structures, calculating descriptors, fingerprinting, substructure searching, chemical reactions, 2D/3D coordinate generation, and molecular visualization. Use this skill for drug discovery, computational chemistry, and cheminformatics research tasks.

## Core Capabilities

### 1. Molecular I/O and Creation

**Reading Molecules:**

Read molecular structures from various formats:

```python
from rdkit import Chem

# From SMILES strings
mol = Chem.MolFromSmiles('Cc1ccccc1')  # Returns Mol object or None

# From MOL files
mol = Chem.MolFromMolFile('path/to/file.mol')

# From MOL blocks (string data)
mol = Chem.MolFromMolBlock(mol_block_string)

# From InChI
mol = Chem.MolFromInchi('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H')
```

**Writing Molecules:**

Convert molecules to text representations:

```python
# To canonical SMILES
smiles = Chem.MolToSmiles(mol)

# To MOL block
mol_block = Chem.MolToMolBlock(mol)

# To InChI
inchi = Chem.MolToInchi(mol)
```

**Batch Processing:**

For processing multiple molecules, use Supplier/Writer objects:

```python
# Read SDF files
suppl = Chem.SDMolSupplier('molecules.sdf')
for mol in suppl:
    if mol is not None:  # Check for parsing errors
        # Process molecule
        pass

# Read SMILES files
suppl = Chem.SmilesMolSupplier('molecules.smi', titleLine=False)

# For large files or compressed data
with gzip.open('molecules.sdf.gz') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Process molecule
        pass

# Multithreaded processing for large datasets
suppl = Chem.MultithreadedSDMolSupplier('molecules.sdf')

# Write molecules to SDF
writer = Chem.SDWriter('output.sdf')
for mol in molecules:
    writer.write(mol)
writer.close()
```

**Important Notes:**
- All `MolFrom*` functions return `None` on failure with error messages
- Always check for `None` before processing molecules
- Molecules are automatically sanitized on import (validates valence, perceives aromaticity)

### 2. Molecular Sanitization and Validation

RDKit automatically sanitizes molecules during parsing, executing 13 steps including valence checking, aromaticity perception, and chirality assignment.

**Sanitization Control:**

```python
# Disable automatic sanitization
mol = Chem.MolFromSmiles('C1=CC=CC=C1', sanitize=False)

# Manual sanitization
Chem.SanitizeMol(mol)

# Detect problems before sanitization
problems = Chem.DetectChemistryProblems(mol)
for problem in problems:
    print(problem.GetType(), problem.Message())

# Partial sanitization (skip specific steps)
from rdkit.Chem import rdMolStandardize
Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL ^ Chem.SANITIZE_PROPERTIES)
```

**Common Sanitization Issues:**
- Atoms with explicit valence exceeding maximum allowed will raise exceptions
- Invalid aromatic rings will cause kekulization errors
- Radical electrons may not be properly assigned without explicit specification

### 3. Molecular Analysis and Properties

**Accessing Molecular Structure:**

```python
# Iterate atoms and bonds
for atom in mol.GetAtoms():
    print(atom.GetSymbol(), atom.GetIdx(), atom.GetDegree())

for bond in mol.GetBonds():
    print(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType())

# Ring information
ring_info = mol.GetRingInfo()
ring_info.NumRings()
ring_info.AtomRings()  # Returns tuples of atom indices

# Check if atom is in ring
atom = mol.GetAtomWithIdx(0)
atom.IsInRing()
atom.IsInRingSize(6)  # Check for 6-membered rings

# Find smallest set of smallest rings (SSSR)
from rdkit.Chem import GetSymmSSSR
rings = GetSymmSSSR(mol)
```

**Stereochemistry:**

```python
# Find chiral centers
from rdkit.Chem import FindMolChiralCenters
chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
# Returns list of (atom_idx, chirality) tuples

# Assign stereochemistry from 3D coordinates
from rdkit.Chem import AssignStereochemistryFrom3D
AssignStereochemistryFrom3D(mol)

# Check bond stereochemistry
bond = mol.GetBondWithIdx(0)
stereo = bond.GetStereo()  # STEREONONE, STEREOZ, STEREOE, etc.
```

**Fragment Analysis:**

```python
# Get disconnected fragments
frags = Chem.GetMolFrags(mol, asMols=True)

# Fragment on specific bonds
from rdkit.Chem import FragmentOnBonds
frag_mol = FragmentOnBonds(mol, [bond_idx1, bond_idx2])

# Count ring systems
from rdkit.Chem.Scaffolds import MurckoScaffold
scaffold = MurckoScaffold.GetScaffoldForMol(mol)
```

### 4. Molecular Descriptors and Properties

**Basic Descriptors:**

```python
from rdkit.Chem import Descriptors

# Molecular weight
mw = Descriptors.MolWt(mol)
exact_mw = Descriptors.ExactMolWt(mol)

# LogP (lipophilicity)
logp = Descriptors.MolLogP(mol)

# Topological polar surface area
tpsa = Descriptors.TPSA(mol)

# Number of hydrogen bond donors/acceptors
hbd = Descriptors.NumHDonors(mol)
hba = Descriptors.NumHAcceptors(mol)

# Number of rotatable bonds
rot_bonds = Descriptors.NumRotatableBonds(mol)

# Number of aromatic rings
aromatic_rings = Descriptors.NumAromaticRings(mol)
```

**Batch Descriptor Calculation:**

```python
# Calculate all descriptors at once
all_descriptors = Descriptors.CalcMolDescriptors(mol)
# Returns dictionary: {'MolWt': 180.16, 'MolLogP': 1.23, ...}

# Get list of available descriptor names
descriptor_names = [desc[0] for desc in Descriptors._descList]
```

**Lipinski's Rule of Five:**

```python
# Check drug-likeness
mw = Descriptors.MolWt(mol) <= 500
logp = Descriptors.MolLogP(mol) <= 5
hbd = Descriptors.NumHDonors(mol) <= 5
hba = Descriptors.NumHAcceptors(mol) <= 10

is_drug_like = mw and logp and hbd and hba
```

### 5. Fingerprints and Molecular Similarity

**Fingerprint Types:**

```python
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem import MACCSkeys

# RDKit topological fingerprint
rdk_gen = rdFingerprintGenerator.GetRDKitFPGenerator(minPath=1, maxPath=7, fpSize=2048)
fp = rdk_gen.GetFingerprint(mol)

# Morgan fingerprints (circular fingerprints, similar to ECFP)
# Modern API using rdFingerprintGenerator
morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp = morgan_gen.GetFingerprint(mol)
# Count-based fingerprint
fp_count = morgan_gen.GetCountFingerprint(mol)

# MACCS keys (166-bit structural key)
fp = MACCSkeys.GenMACCSKeys(mol)

# Atom pair fingerprints
ap_gen = rdFingerprintGenerator.GetAtomPairGenerator()
fp = ap_gen.GetFingerprint(mol)

# Topological torsion fingerprints
tt_gen = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
fp = tt_gen.GetFingerprint(mol)

# Avalon fingerprints (if available)
from rdkit.Avalon import pyAvalonTools
fp = pyAvalonTools.GetAvalonFP(mol)
```

**Similarity Calculation:**

```python
from rdkit import DataStructs
from rdkit.Chem import rdFingerprintGenerator

# Generate fingerprints using generator
mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp1 = mfpgen.GetFingerprint(mol1)
fp2 = mfpgen.GetFingerprint(mol2)

# Calculate Tanimoto similarity
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)

# Calculate similarity for multiple molecules
fps = [mfpgen.GetFingerprint(m) for m in [mol2, mol3, mol4]]
similarities = DataStructs.BulkTanimotoSimilarity(fp1, fps)

# Other similarity metrics
dice = DataStructs.DiceSimilarity(fp1, fp2)
cosine = DataStructs.CosineSimilarity(fp1, fp2)
```

**Clustering and Diversity:**

```python
# Butina clustering based on fingerprint similarity
from rdkit.ML.Cluster import Butina

# Calculate distance matrix
dists = []
mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = [mfpgen.GetFingerprint(mol) for mol in mols]
for i in range(len(fps)):
    sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i])
    dists.extend([1-sim for sim in sims])

# Cluster with distance cutoff
clusters = Butina.ClusterData(dists, len(fps), distThresh=0.3, isDistData=True)
```

### 6. Substructure Searching and SMARTS

**Basic Substructure Matching:**

```python
# Define query using SMARTS
query = Chem.MolFromSmarts('[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1')  # Benzene ring

# Check if molecule contains substructure
has_match = mol.HasSubstructMatch(query)

# Get all matches (returns tuple of tuples with atom indices)
matches = mol.GetSubstructMatches(query)

# Get only first match
match = mol.GetSubstructMatch(query)
```

**Common SMARTS Patterns:**

```python
# Primary alcohols
primary_alcohol = Chem.MolFromSmarts('[CH2][OH1]')

# Carboxylic acids
carboxylic_acid = Chem.MolFromSmarts('C(=O)[OH]')

# Amides
amide = Chem.MolFromSmarts('C(=O)N')

# Aromatic heterocycles
aromatic_n = Chem.MolFromSmarts('[nR]')  # Aromatic nitrogen in ring

# Macrocycles (rings > 12 atoms)
macrocycle = Chem.MolFromSmarts('[r{12-}]')
```

**Matching Rules:**
- Unspecified properties in query match any value in target
- Hydrogens are ignored unless explicitly specified
- Charged query atom won't match uncharged target atom
- Aromatic query atom won't match aliphatic target atom (unless query is generic)

### 7. Chemical Reactions

**Reaction SMARTS:**

```python
from rdkit.Chem import AllChem

# Define reaction using SMARTS: reactants >> products
rxn = AllChem.ReactionFromSmarts('[C:1]=[O:2]>>[C:1][O:2]')  # Ketone reduction

# Apply reaction to molecules
reactants = (mol1,)
products = rxn.RunReactants(reactants)

# Products is tuple of tuples (one tuple per product set)
for product_set in products:
    for product in product_set:
        # Sanitize product
        Chem.SanitizeMol(product)
```

**Reaction Features:**
- Atom mapping preserves specific atoms between reactants and products
- Dummy atoms in products are replaced by corresponding reactant atoms
- "Any" bonds inherit bond order from reactants
- Chirality preserved unless explicitly changed

**Reaction Similarity:**

```python
# Generate reaction fingerprints
fp = AllChem.CreateDifferenceFingerprintForReaction(rxn)

# Compare reactions
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
```

### 8. 2D and 3D Coordinate Generation

**2D Coordinate Generation:**

```python
from rdkit.Chem import AllChem

# Generate 2D coordinates for depiction
AllChem.Compute2DCoords(mol)

# Align molecule to template structure
template = Chem.MolFromSmiles('c1ccccc1')
AllChem.Compute2DCoords(template)
AllChem.GenerateDepictionMatching2DStructure(mol, template)
```

**3D Coordinate Generation and Conformers:**

```python
# Generate single 3D conformer using ETKDG
AllChem.EmbedMolecule(mol, randomSeed=42)

# Generate multiple conformers
conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=10, randomSeed=42)

# Optimize geometry with force field
AllChem.UFFOptimizeMolecule(mol)  # UFF force field
AllChem.MMFFOptimizeMolecule(mol)  # MMFF94 force field

# Optimize all conformers
for conf_id in conf_ids:
    AllChem.MMFFOptimizeMolecule(mol, confId=conf_id)

# Calculate RMSD between conformers
from rdkit.Chem import AllChem
rms = AllChem.GetConformerRMS(mol, conf_id1, conf_id2)

# Align molecules
AllChem.AlignMol(probe_mol, ref_mol)
```

**Constrained Embedding:**

```python
# Embed with part of molecule constrained to specific coordinates
AllChem.ConstrainedEmbed(mol, core_mol)
```

### 9. Molecular Visualization

**Basic Drawing:**

```python
from rdkit.Chem import Draw

# Draw single molecule to PIL image
img = Draw.MolToImage(mol, size=(300, 300))
img.save('molecule.png')

# Draw to file directly
Draw.MolToFile(mol, 'molecule.png')

# Draw multiple molecules in grid
mols = [mol1, mol2, mol3, mol4]
img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(200, 200))
```

**Highlighting Substructures:**

```python
# Highlight substructure match
query = Chem.MolFromSmarts('c1ccccc1')
match = mol.GetSubstructMatch(query)

img = Draw.MolToImage(mol, highlightAtoms=match)

# Custom highlight colors
highlight_colors = {atom_idx: (1, 0, 0) for atom_idx in match}  # Red
img = Draw.MolToImage(mol, highlightAtoms=match,
                      highlightAtomColors=highlight_colors)
```

**Customizing Visualization:**

```python
from rdkit.Chem.Draw import rdMolDraw2D

# Create drawer with custom options
drawer = rdMolDraw2D.MolDraw2DCairo(300, 300)
opts = drawer.drawOptions()

# Customize options
opts.addAtomIndices = True
opts.addStereoAnnotation = True
opts.bondLineWidth = 2

# Draw molecule
drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save to file
with open('molecule.png', 'wb') as f:
    f.write(drawer.GetDrawingText())
```

**Jupyter Notebook Integration:**

```python
# Enable inline display in Jupyter
from rdkit.Chem.Draw import IPythonConsole

# Customize default display
IPythonConsole.ipython_useSVG = True  # Use SVG instead of PNG
IPythonConsole.molSize = (300, 300)   # Default size

# Molecules now display automatically
mol  # Shows molecule image
```

**Visualizing Fingerprint Bits:**

```python
# Show what molecular features a fingerprint bit represents
from rdkit.Chem import Draw

# For Morgan fingerprints
bit_info = {}
fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, bitInfo=bit_info)

# Draw environment for specific bit
img = Draw.DrawMorganBit(mol, bit_id, bit_info)
```

### 10. Molecular Modification

**Adding/Removing Hydrogens:**

```python
# Add explicit hydrogens
mol_h = Chem.AddHs(mol)

# Remove explicit hydrogens
mol = Chem.RemoveHs(mol_h)
```

**Kekulization and Aromaticity:**

```python
# Convert aromatic bonds to alternating single/double
Chem.Kekulize(mol)

# Set aromaticity
Chem.SetAromaticity(mol)
```

**Replacing Substructures:**

```python
# Replace substructure with another structure
query = Chem.MolFromSmarts('c1ccccc1')  # Benzene
replacement = Chem.MolFromSmiles('C1CCCCC1')  # Cyclohexane

new_mol = Chem.ReplaceSubstructs(mol, query, replacement)[0]
```

**Neutralizing Charges:**

```python
# Remove formal charges by adding/removing hydrogens
from rdkit.Chem.MolStandardize import rdMolStandardize

# Using Uncharger
uncharger = rdMolStandardize.Uncharger()
mol_neutral = uncharger.uncharge(mol)
```

### 11. Working with Molecular Hashes and Standardization

**Molecular Hashing:**

```python
from rdkit.Chem import rdMolHash

# Generate Murcko scaffold hash
scaffold_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.MurckoScaffold)

# Canonical SMILES hash
canonical_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.CanonicalSmiles)

# Regioisomer hash (ignores stereochemistry)
regio_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.Regioisomer)
```

**Randomized SMILES:**

```python
# Generate random SMILES representations (for data augmentation)
from rdkit.Chem import MolToRandomSmilesVect

random_smiles = MolToRandomSmilesVect(mol, numSmiles=10, randomSeed=42)
```

### 12. Pharmacophore and 3D Features

**Pharmacophore Features:**

```python
from rdkit.Chem import ChemicalFeatures
from rdkit import RDConfig
import os

# Load feature factory
fdef_path = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_path)

# Get pharmacophore features
features = factory.GetFeaturesForMol(mol)

for feat in features:
    print(feat.GetFamily(), feat.GetType(), feat.GetAtomIds())
```

## Common Workflows

### Drug-likeness Analysis

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def analyze_druglikeness(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Calculate Lipinski descriptors
    results = {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol)
    }

    # Check Lipinski's Rule of Five
    results['Lipinski'] = (
        results['MW'] <= 500 and
        results['LogP'] <= 5 and
        results['HBD'] <= 5 and
        results['HBA'] <= 10
    )

    return results
```

### Similarity Screening

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs

def similarity_screen(query_smiles, database_smiles, threshold=0.7):
    query_mol = Chem.MolFromSmiles(query_smiles)
    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2)

    hits = []
    for idx, smiles in enumerate(database_smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            if sim >= threshold:
                hits.append((idx, smiles, sim))

    return sorted(hits, key=lambda x: x[2], reverse=True)
```

### Substructure Filtering

```python
from rdkit import Chem

def filter_by_substructure(smiles_list, pattern_smarts):
    query = Chem.MolFromSmarts(pattern_smarts)

    hits = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol and mol.HasSubstructMatch(query):
            hits.append(smiles)

    return hits
```

## Best Practices

### Error Handling

Always check for `None` when parsing molecules:

```python
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    print(f"Failed to parse: {smiles}")
    continue
```

### Performance Optimization

**Use binary formats for storage:**

```python
import pickle

# Pickle molecules for fast loading
with open('molecules.pkl', 'wb') as f:
    pickle.dump(mols, f)

# Load pickled molecules (much faster than reparsing)
with open('molecules.pkl', 'rb') as f:
    mols = pickle.load(f)
```

**Use bulk operations:**

```python
# Calculate fingerprints for all molecules at once
fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2) for mol in mols]

# Use bulk similarity calculations
similarities = DataStructs.BulkTanimotoSimilarity(fps[0], fps[1:])
```

### Thread Safety

RDKit operations are generally thread-safe for:
- Molecule I/O (SMILES, mol blocks)
- Coordinate generation
- Fingerprinting and descriptors
- Substructure searching
- Reactions
- Drawing

**Not thread-safe:** MolSuppliers when accessed concurrently.

### Memory Management

For large datasets:

```python
# Use ForwardSDMolSupplier to avoid loading entire file
with open('large.sdf') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Process one molecule at a time
        pass

# Use MultithreadedSDMolSupplier for parallel processing
suppl = Chem.MultithreadedSDMolSupplier('large.sdf', numWriterThreads=4)
```

## Common Pitfalls

1. **Forgetting to check for None:** Always validate molecules after parsing
2. **Sanitization failures:** Use `DetectChemistryProblems()` to debug
3. **Missing hydrogens:** Use `AddHs()` when calculating properties that depend on hydrogen
4. **2D vs 3D:** Generate appropriate coordinates before visualization or 3D analysis
5. **SMARTS matching rules:** Remember that unspecified properties match anything
6. **Thread safety with MolSuppliers:** Don't share supplier objects across threads

## Resources

### references/

This skill includes detailed API reference documentation:

- `api_reference.md` - Comprehensive listing of RDKit modules, functions, and classes organized by functionality
- `descriptors_reference.md` - Complete list of available molecular descriptors with descriptions
- `smarts_patterns.md` - Common SMARTS patterns for functional groups and structural features

Load these references when needing specific API details, parameter information, or pattern examples.

### scripts/

Example scripts for common RDKit workflows:

- `molecular_properties.py` - Calculate comprehensive molecular properties and descriptors
- `similarity_search.py` - Perform fingerprint-based similarity screening
- `substructure_filter.py` - Filter molecules by substructure patterns

These scripts can be executed directly or used as templates for custom workflows.

---

## Reference: Api_Reference

# RDKit API Reference

This document provides a comprehensive reference for RDKit's Python API, organized by functionality.

## Core Module: rdkit.Chem

The fundamental module for working with molecules.

### Molecule I/O

**Reading Molecules:**

- `Chem.MolFromSmiles(smiles, sanitize=True)` - Parse SMILES string
- `Chem.MolFromSmarts(smarts)` - Parse SMARTS pattern
- `Chem.MolFromMolFile(filename, sanitize=True, removeHs=True)` - Read MOL file
- `Chem.MolFromMolBlock(molblock, sanitize=True, removeHs=True)` - Parse MOL block string
- `Chem.MolFromMol2File(filename, sanitize=True, removeHs=True)` - Read MOL2 file
- `Chem.MolFromMol2Block(molblock, sanitize=True, removeHs=True)` - Parse MOL2 block
- `Chem.MolFromPDBFile(filename, sanitize=True, removeHs=True)` - Read PDB file
- `Chem.MolFromPDBBlock(pdbblock, sanitize=True, removeHs=True)` - Parse PDB block
- `Chem.MolFromInchi(inchi, sanitize=True, removeHs=True)` - Parse InChI string
- `Chem.MolFromSequence(seq, sanitize=True)` - Create molecule from peptide sequence

**Writing Molecules:**

- `Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)` - Convert to SMILES
- `Chem.MolToSmarts(mol, isomericSmarts=False)` - Convert to SMARTS
- `Chem.MolToMolBlock(mol, includeStereo=True, confId=-1)` - Convert to MOL block
- `Chem.MolToMolFile(mol, filename, includeStereo=True, confId=-1)` - Write MOL file
- `Chem.MolToPDBBlock(mol, confId=-1)` - Convert to PDB block
- `Chem.MolToPDBFile(mol, filename, confId=-1)` - Write PDB file
- `Chem.MolToInchi(mol, options='')` - Convert to InChI
- `Chem.MolToInchiKey(mol, options='')` - Generate InChI key
- `Chem.MolToSequence(mol)` - Convert to peptide sequence

**Batch I/O:**

- `Chem.SDMolSupplier(filename, sanitize=True, removeHs=True)` - SDF file reader
- `Chem.ForwardSDMolSupplier(fileobj, sanitize=True, removeHs=True)` - Forward-only SDF reader
- `Chem.MultithreadedSDMolSupplier(filename, numWriterThreads=1)` - Parallel SDF reader
- `Chem.SmilesMolSupplier(filename, delimiter=' ', titleLine=True)` - SMILES file reader
- `Chem.SDWriter(filename)` - SDF file writer
- `Chem.SmilesWriter(filename, delimiter=' ', includeHeader=True)` - SMILES file writer

### Molecular Manipulation

**Sanitization:**

- `Chem.SanitizeMol(mol, sanitizeOps=SANITIZE_ALL, catchErrors=False)` - Sanitize molecule
- `Chem.DetectChemistryProblems(mol, sanitizeOps=SANITIZE_ALL)` - Detect sanitization issues
- `Chem.AssignStereochemistry(mol, cleanIt=True, force=False)` - Assign stereochemistry
- `Chem.FindPotentialStereo(mol)` - Find potential stereocenters
- `Chem.AssignStereochemistryFrom3D(mol, confId=-1)` - Assign stereo from 3D coords

**Hydrogen Management:**

- `Chem.AddHs(mol, explicitOnly=False, addCoords=False)` - Add explicit hydrogens
- `Chem.RemoveHs(mol, implicitOnly=False, updateExplicitCount=False)` - Remove hydrogens
- `Chem.RemoveAllHs(mol)` - Remove all hydrogens

**Aromaticity:**

- `Chem.SetAromaticity(mol, model=AROMATICITY_RDKIT)` - Set aromaticity model
- `Chem.Kekulize(mol, clearAromaticFlags=False)` - Kekulize aromatic bonds
- `Chem.SetConjugation(mol)` - Set conjugation flags

**Fragments:**

- `Chem.GetMolFrags(mol, asMols=False, sanitizeFrags=True)` - Get disconnected fragments
- `Chem.FragmentOnBonds(mol, bondIndices, addDummies=True)` - Fragment on specific bonds
- `Chem.ReplaceSubstructs(mol, query, replacement, replaceAll=False)` - Replace substructures
- `Chem.DeleteSubstructs(mol, query, onlyFrags=False)` - Delete substructures

**Stereochemistry:**

- `Chem.FindMolChiralCenters(mol, includeUnassigned=False, useLegacyImplementation=False)` - Find chiral centers
- `Chem.FindPotentialStereo(mol, cleanIt=True)` - Find potential stereocenters

### Substructure Searching

**Basic Matching:**

- `mol.HasSubstructMatch(query, useChirality=False)` - Check for substructure match
- `mol.GetSubstructMatch(query, useChirality=False)` - Get first match
- `mol.GetSubstructMatches(query, uniquify=True, useChirality=False)` - Get all matches
- `mol.GetSubstructMatches(query, maxMatches=1000)` - Limit number of matches

### Molecular Properties

**Atom Methods:**

- `atom.GetSymbol()` - Atomic symbol
- `atom.GetAtomicNum()` - Atomic number
- `atom.GetDegree()` - Number of bonds
- `atom.GetTotalDegree()` - Including hydrogens
- `atom.GetFormalCharge()` - Formal charge
- `atom.GetNumRadicalElectrons()` - Radical electrons
- `atom.GetIsAromatic()` - Aromaticity flag
- `atom.GetHybridization()` - Hybridization (SP, SP2, SP3, etc.)
- `atom.GetIdx()` - Atom index
- `atom.IsInRing()` - In any ring
- `atom.IsInRingSize(size)` - In ring of specific size
- `atom.GetChiralTag()` - Chirality tag

**Bond Methods:**

- `bond.GetBondType()` - Bond type (SINGLE, DOUBLE, TRIPLE, AROMATIC)
- `bond.GetBeginAtomIdx()` - Starting atom index
- `bond.GetEndAtomIdx()` - Ending atom index
- `bond.GetIsConjugated()` - Conjugation flag
- `bond.GetIsAromatic()` - Aromaticity flag
- `bond.IsInRing()` - In any ring
- `bond.GetStereo()` - Stereochemistry (STEREONONE, STEREOZ, STEREOE, etc.)

**Molecule Methods:**

- `mol.GetNumAtoms(onlyExplicit=True)` - Number of atoms
- `mol.GetNumHeavyAtoms()` - Number of heavy atoms
- `mol.GetNumBonds()` - Number of bonds
- `mol.GetAtoms()` - Iterator over atoms
- `mol.GetBonds()` - Iterator over bonds
- `mol.GetAtomWithIdx(idx)` - Get specific atom
- `mol.GetBondWithIdx(idx)` - Get specific bond
- `mol.GetRingInfo()` - Ring information object

**Ring Information:**

- `Chem.GetSymmSSSR(mol)` - Get smallest set of smallest rings
- `Chem.GetSSSR(mol)` - Alias for GetSymmSSSR
- `ring_info.NumRings()` - Number of rings
- `ring_info.AtomRings()` - Tuples of atom indices in rings
- `ring_info.BondRings()` - Tuples of bond indices in rings

## rdkit.Chem.AllChem

Extended chemistry functionality.

### 2D/3D Coordinate Generation

- `AllChem.Compute2DCoords(mol, canonOrient=True, clearConfs=True)` - Generate 2D coordinates
- `AllChem.EmbedMolecule(mol, maxAttempts=0, randomSeed=-1, useRandomCoords=False)` - Generate 3D conformer
- `AllChem.EmbedMultipleConfs(mol, numConfs=10, maxAttempts=0, randomSeed=-1)` - Generate multiple conformers
- `AllChem.ConstrainedEmbed(mol, core, useTethers=True)` - Constrained embedding
- `AllChem.GenerateDepictionMatching2DStructure(mol, reference, refPattern=None)` - Align to template

### Force Field Optimization

- `AllChem.UFFOptimizeMolecule(mol, maxIters=200, confId=-1)` - UFF optimization
- `AllChem.MMFFOptimizeMolecule(mol, maxIters=200, confId=-1, mmffVariant='MMFF94')` - MMFF optimization
- `AllChem.UFFGetMoleculeForceField(mol, confId=-1)` - Get UFF force field object
- `AllChem.MMFFGetMoleculeForceField(mol, pyMMFFMolProperties, confId=-1)` - Get MMFF force field

### Conformer Analysis

- `AllChem.GetConformerRMS(mol, confId1, confId2, prealigned=False)` - Calculate RMSD
- `AllChem.GetConformerRMSMatrix(mol, prealigned=False)` - RMSD matrix
- `AllChem.AlignMol(prbMol, refMol, prbCid=-1, refCid=-1)` - Align molecules
- `AllChem.AlignMolConformers(mol)` - Align all conformers

### Reactions

- `AllChem.ReactionFromSmarts(smarts, useSmiles=False)` - Create reaction from SMARTS
- `reaction.RunReactants(reactants)` - Apply reaction
- `reaction.RunReactant(reactant, reactionIdx)` - Apply to specific reactant
- `AllChem.CreateDifferenceFingerprintForReaction(reaction)` - Reaction fingerprint

### Fingerprints

- `AllChem.GetMorganFingerprint(mol, radius, useFeatures=False)` - Morgan fingerprint
- `AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=2048)` - Morgan bit vector
- `AllChem.GetHashedMorganFingerprint(mol, radius, nBits=2048)` - Hashed Morgan
- `AllChem.GetErGFingerprint(mol)` - ErG fingerprint

## rdkit.Chem.Descriptors

Molecular descriptor calculations.

### Common Descriptors

- `Descriptors.MolWt(mol)` - Molecular weight
- `Descriptors.ExactMolWt(mol)` - Exact molecular weight
- `Descriptors.HeavyAtomMolWt(mol)` - Heavy atom molecular weight
- `Descriptors.MolLogP(mol)` - LogP (lipophilicity)
- `Descriptors.MolMR(mol)` - Molar refractivity
- `Descriptors.TPSA(mol)` - Topological polar surface area
- `Descriptors.NumHDonors(mol)` - Hydrogen bond donors
- `Descriptors.NumHAcceptors(mol)` - Hydrogen bond acceptors
- `Descriptors.NumRotatableBonds(mol)` - Rotatable bonds
- `Descriptors.NumAromaticRings(mol)` - Aromatic rings
- `Descriptors.NumSaturatedRings(mol)` - Saturated rings
- `Descriptors.NumAliphaticRings(mol)` - Aliphatic rings
- `Descriptors.NumAromaticHeterocycles(mol)` - Aromatic heterocycles
- `Descriptors.NumRadicalElectrons(mol)` - Radical electrons
- `Descriptors.NumValenceElectrons(mol)` - Valence electrons

### Batch Calculation

- `Descriptors.CalcMolDescriptors(mol)` - Calculate all descriptors as dictionary

### Descriptor Lists

- `Descriptors._descList` - List of (name, function) tuples for all descriptors

## rdkit.Chem.Draw

Molecular visualization.

### Image Generation

- `Draw.MolToImage(mol, size=(300,300), kekulize=True, wedgeBonds=True, highlightAtoms=None)` - Generate PIL image
- `Draw.MolToFile(mol, filename, size=(300,300), kekulize=True, wedgeBonds=True)` - Save to file
- `Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(200,200), legends=None)` - Grid of molecules
- `Draw.MolsMatrixToGridImage(mols, molsPerRow=3, subImgSize=(200,200), legends=None)` - Nested grid
- `Draw.ReactionToImage(rxn, subImgSize=(200,200))` - Reaction image

### Fingerprint Visualization

- `Draw.DrawMorganBit(mol, bitId, bitInfo, whichExample=0)` - Visualize Morgan bit
- `Draw.DrawMorganBits(bits, mol, bitInfo, molsPerRow=3)` - Multiple Morgan bits
- `Draw.DrawRDKitBit(mol, bitId, bitInfo, whichExample=0)` - Visualize RDKit bit

### IPython Integration

- `Draw.IPythonConsole` - Module for Jupyter integration
- `Draw.IPythonConsole.ipython_useSVG` - Use SVG (True) or PNG (False)
- `Draw.IPythonConsole.molSize` - Default molecule image size

### Drawing Options

- `rdMolDraw2D.MolDrawOptions()` - Get drawing options object
  - `.addAtomIndices` - Show atom indices
  - `.addBondIndices` - Show bond indices
  - `.addStereoAnnotation` - Show stereochemistry
  - `.bondLineWidth` - Line width
  - `.highlightBondWidthMultiplier` - Highlight width
  - `.minFontSize` - Minimum font size
  - `.maxFontSize` - Maximum font size

## rdkit.Chem.rdMolDescriptors

Additional descriptor calculations.

- `rdMolDescriptors.CalcNumRings(mol)` - Number of rings
- `rdMolDescriptors.CalcNumAromaticRings(mol)` - Aromatic rings
- `rdMolDescriptors.CalcNumAliphaticRings(mol)` - Aliphatic rings
- `rdMolDescriptors.CalcNumSaturatedRings(mol)` - Saturated rings
- `rdMolDescriptors.CalcNumHeterocycles(mol)` - Heterocycles
- `rdMolDescriptors.CalcNumAromaticHeterocycles(mol)` - Aromatic heterocycles
- `rdMolDescriptors.CalcNumSpiroAtoms(mol)` - Spiro atoms
- `rdMolDescriptors.CalcNumBridgeheadAtoms(mol)` - Bridgehead atoms
- `rdMolDescriptors.CalcFractionCsp3(mol)` - Fraction of sp3 carbons
- `rdMolDescriptors.CalcLabuteASA(mol)` - Labute accessible surface area
- `rdMolDescriptors.CalcTPSA(mol)` - TPSA
- `rdMolDescriptors.CalcMolFormula(mol)` - Molecular formula

## rdkit.Chem.Scaffolds

Scaffold analysis.

### Murcko Scaffolds

- `MurckoScaffold.GetScaffoldForMol(mol)` - Get Murcko scaffold
- `MurckoScaffold.MakeScaffoldGeneric(mol)` - Generic scaffold
- `MurckoScaffold.MurckoDecompose(mol)` - Decompose to scaffold and sidechains

## rdkit.Chem.rdMolHash

Molecular hashing and standardization.

- `rdMolHash.MolHash(mol, hashFunction)` - Generate hash
  - `rdMolHash.HashFunction.AnonymousGraph` - Anonymized structure
  - `rdMolHash.HashFunction.CanonicalSmiles` - Canonical SMILES
  - `rdMolHash.HashFunction.ElementGraph` - Element graph
  - `rdMolHash.HashFunction.MurckoScaffold` - Murcko scaffold
  - `rdMolHash.HashFunction.Regioisomer` - Regioisomer (no stereo)
  - `rdMolHash.HashFunction.NetCharge` - Net charge
  - `rdMolHash.HashFunction.HetAtomProtomer` - Heteroatom protomer
  - `rdMolHash.HashFunction.HetAtomTautomer` - Heteroatom tautomer

## rdkit.Chem.MolStandardize

Molecule standardization.

- `rdMolStandardize.Normalize(mol)` - Normalize functional groups
- `rdMolStandardize.Reionize(mol)` - Fix ionization state
- `rdMolStandardize.RemoveFragments(mol)` - Remove small fragments
- `rdMolStandardize.Cleanup(mol)` - Full cleanup (normalize + reionize + remove)
- `rdMolStandardize.Uncharger()` - Create uncharger object
  - `.uncharge(mol)` - Remove charges
- `rdMolStandardize.TautomerEnumerator()` - Enumerate tautomers
  - `.Enumerate(mol)` - Generate tautomers
  - `.Canonicalize(mol)` - Get canonical tautomer

## rdkit.DataStructs

Fingerprint similarity and operations.

### Similarity Metrics

- `DataStructs.TanimotoSimilarity(fp1, fp2)` - Tanimoto coefficient
- `DataStructs.DiceSimilarity(fp1, fp2)` - Dice coefficient
- `DataStructs.CosineSimilarity(fp1, fp2)` - Cosine similarity
- `DataStructs.SokalSimilarity(fp1, fp2)` - Sokal similarity
- `DataStructs.KulczynskiSimilarity(fp1, fp2)` - Kulczynski similarity
- `DataStructs.McConnaugheySimilarity(fp1, fp2)` - McConnaughey similarity

### Bulk Operations

- `DataStructs.BulkTanimotoSimilarity(fp, fps)` - Tanimoto for list of fingerprints
- `DataStructs.BulkDiceSimilarity(fp, fps)` - Dice for list
- `DataStructs.BulkCosineSimilarity(fp, fps)` - Cosine for list

### Distance Metrics

- `DataStructs.TanimotoDistance(fp1, fp2)` - 1 - Tanimoto
- `DataStructs.DiceDistance(fp1, fp2)` - 1 - Dice

## rdkit.Chem.AtomPairs

Atom pair fingerprints.

- `Pairs.GetAtomPairFingerprint(mol, minLength=1, maxLength=30)` - Atom pair fingerprint
- `Pairs.GetAtomPairFingerprintAsBitVect(mol, minLength=1, maxLength=30, nBits=2048)` - As bit vector
- `Pairs.GetHashedAtomPairFingerprint(mol, nBits=2048, minLength=1, maxLength=30)` - Hashed version

## rdkit.Chem.Torsions

Topological torsion fingerprints.

- `Torsions.GetTopologicalTorsionFingerprint(mol, targetSize=4)` - Torsion fingerprint
- `Torsions.GetTopologicalTorsionFingerprintAsIntVect(mol, targetSize=4)` - As int vector
- `Torsions.GetHashedTopologicalTorsionFingerprint(mol, nBits=2048, targetSize=4)` - Hashed version

## rdkit.Chem.MACCSkeys

MACCS structural keys.

- `MACCSkeys.GenMACCSKeys(mol)` - Generate 166-bit MACCS keys

## rdkit.Chem.ChemicalFeatures

Pharmacophore features.

- `ChemicalFeatures.BuildFeatureFactory(featureFile)` - Create feature factory
- `factory.GetFeaturesForMol(mol)` - Get pharmacophore features
- `feature.GetFamily()` - Feature family (Donor, Acceptor, etc.)
- `feature.GetType()` - Feature type
- `feature.GetAtomIds()` - Atoms involved in feature

## rdkit.ML.Cluster.Butina

Clustering algorithms.

- `Butina.ClusterData(distances, nPts, distThresh, isDistData=True)` - Butina clustering
  - Returns tuple of tuples with cluster members

## rdkit.Chem.rdFingerprintGenerator

Modern fingerprint generation API (RDKit 2020.09+).

- `rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)` - Morgan generator
- `rdFingerprintGenerator.GetRDKitFPGenerator(minPath=1, maxPath=7, fpSize=2048)` - RDKit FP generator
- `rdFingerprintGenerator.GetAtomPairGenerator(minDistance=1, maxDistance=30)` - Atom pair generator
- `generator.GetFingerprint(mol)` - Generate fingerprint
- `generator.GetCountFingerprint(mol)` - Count-based fingerprint

## Common Parameters

### Sanitization Operations

- `SANITIZE_NONE` - No sanitization
- `SANITIZE_ALL` - All operations (default)
- `SANITIZE_CLEANUP` - Basic cleanup
- `SANITIZE_PROPERTIES` - Calculate properties
- `SANITIZE_SYMMRINGS` - Symmetrize rings
- `SANITIZE_KEKULIZE` - Kekulize aromatic rings
- `SANITIZE_FINDRADICALS` - Find radical electrons
- `SANITIZE_SETAROMATICITY` - Set aromaticity
- `SANITIZE_SETCONJUGATION` - Set conjugation
- `SANITIZE_SETHYBRIDIZATION` - Set hybridization
- `SANITIZE_CLEANUPCHIRALITY` - Cleanup chirality

### Bond Types

- `BondType.SINGLE` - Single bond
- `BondType.DOUBLE` - Double bond
- `BondType.TRIPLE` - Triple bond
- `BondType.AROMATIC` - Aromatic bond
- `BondType.DATIVE` - Dative bond
- `BondType.UNSPECIFIED` - Unspecified

### Hybridization

- `HybridizationType.S` - S
- `HybridizationType.SP` - SP
- `HybridizationType.SP2` - SP2
- `HybridizationType.SP3` - SP3
- `HybridizationType.SP3D` - SP3D
- `HybridizationType.SP3D2` - SP3D2

### Chirality

- `ChiralType.CHI_UNSPECIFIED` - Unspecified
- `ChiralType.CHI_TETRAHEDRAL_CW` - Clockwise
- `ChiralType.CHI_TETRAHEDRAL_CCW` - Counter-clockwise

## Installation

```bash
# Using conda (recommended)
conda install -c conda-forge rdkit

# Using pip
pip install rdkit-pypi
```

## Importing

```python
# Core functionality
from rdkit import Chem
from rdkit.Chem import AllChem

# Descriptors
from rdkit.Chem import Descriptors

# Drawing
from rdkit.Chem import Draw

# Similarity
from rdkit import DataStructs
```

---

## Reference: Descriptors_Reference

# RDKit Molecular Descriptors Reference

Complete reference for molecular descriptors available in RDKit's `Descriptors` module.

## Usage

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles('CCO')

# Calculate individual descriptor
mw = Descriptors.MolWt(mol)

# Calculate all descriptors at once
all_desc = Descriptors.CalcMolDescriptors(mol)
```

## Molecular Weight and Mass

### MolWt
Average molecular weight of the molecule.
```python
Descriptors.MolWt(mol)
```

### ExactMolWt
Exact molecular weight using isotopic composition.
```python
Descriptors.ExactMolWt(mol)
```

### HeavyAtomMolWt
Average molecular weight ignoring hydrogens.
```python
Descriptors.HeavyAtomMolWt(mol)
```

## Lipophilicity

### MolLogP
Wildman-Crippen LogP (octanol-water partition coefficient).
```python
Descriptors.MolLogP(mol)
```

### MolMR
Wildman-Crippen molar refractivity.
```python
Descriptors.MolMR(mol)
```

## Polar Surface Area

### TPSA
Topological polar surface area (TPSA) based on fragment contributions.
```python
Descriptors.TPSA(mol)
```

### LabuteASA
Labute's Approximate Surface Area (ASA).
```python
Descriptors.LabuteASA(mol)
```

## Hydrogen Bonding

### NumHDonors
Number of hydrogen bond donors (N-H and O-H).
```python
Descriptors.NumHDonors(mol)
```

### NumHAcceptors
Number of hydrogen bond acceptors (N and O).
```python
Descriptors.NumHAcceptors(mol)
```

### NOCount
Number of N and O atoms.
```python
Descriptors.NOCount(mol)
```

### NHOHCount
Number of N-H and O-H bonds.
```python
Descriptors.NHOHCount(mol)
```

## Atom Counts

### HeavyAtomCount
Number of heavy atoms (non-hydrogen).
```python
Descriptors.HeavyAtomCount(mol)
```

### NumHeteroatoms
Number of heteroatoms (non-C and non-H).
```python
Descriptors.NumHeteroatoms(mol)
```

### NumValenceElectrons
Total number of valence electrons.
```python
Descriptors.NumValenceElectrons(mol)
```

### NumRadicalElectrons
Number of radical electrons.
```python
Descriptors.NumRadicalElectrons(mol)
```

## Ring Descriptors

### RingCount
Number of rings.
```python
Descriptors.RingCount(mol)
```

### NumAromaticRings
Number of aromatic rings.
```python
Descriptors.NumAromaticRings(mol)
```

### NumSaturatedRings
Number of saturated rings.
```python
Descriptors.NumSaturatedRings(mol)
```

### NumAliphaticRings
Number of aliphatic (non-aromatic) rings.
```python
Descriptors.NumAliphaticRings(mol)
```

### NumAromaticCarbocycles
Number of aromatic carbocycles (rings with only carbons).
```python
Descriptors.NumAromaticCarbocycles(mol)
```

### NumAromaticHeterocycles
Number of aromatic heterocycles (rings with heteroatoms).
```python
Descriptors.NumAromaticHeterocycles(mol)
```

### NumSaturatedCarbocycles
Number of saturated carbocycles.
```python
Descriptors.NumSaturatedCarbocycles(mol)
```

### NumSaturatedHeterocycles
Number of saturated heterocycles.
```python
Descriptors.NumSaturatedHeterocycles(mol)
```

### NumAliphaticCarbocycles
Number of aliphatic carbocycles.
```python
Descriptors.NumAliphaticCarbocycles(mol)
```

### NumAliphaticHeterocycles
Number of aliphatic heterocycles.
```python
Descriptors.NumAliphaticHeterocycles(mol)
```

## Rotatable Bonds

### NumRotatableBonds
Number of rotatable bonds (flexibility).
```python
Descriptors.NumRotatableBonds(mol)
```

## Aromatic Atoms

### NumAromaticAtoms
Number of aromatic atoms.
```python
Descriptors.NumAromaticAtoms(mol)
```

## Fraction Descriptors

### FractionCsp3
Fraction of carbons that are sp3 hybridized.
```python
Descriptors.FractionCsp3(mol)
```

## Complexity Descriptors

### BertzCT
Bertz complexity index.
```python
Descriptors.BertzCT(mol)
```

### Ipc
Information content (complexity measure).
```python
Descriptors.Ipc(mol)
```

## Kappa Shape Indices

Molecular shape descriptors based on graph invariants.

### Kappa1
First kappa shape index.
```python
Descriptors.Kappa1(mol)
```

### Kappa2
Second kappa shape index.
```python
Descriptors.Kappa2(mol)
```

### Kappa3
Third kappa shape index.
```python
Descriptors.Kappa3(mol)
```

## Chi Connectivity Indices

Molecular connectivity indices.

### Chi0, Chi1, Chi2, Chi3, Chi4
Simple chi connectivity indices.
```python
Descriptors.Chi0(mol)
Descriptors.Chi1(mol)
Descriptors.Chi2(mol)
Descriptors.Chi3(mol)
Descriptors.Chi4(mol)
```

### Chi0n, Chi1n, Chi2n, Chi3n, Chi4n
Valence-modified chi connectivity indices.
```python
Descriptors.Chi0n(mol)
Descriptors.Chi1n(mol)
Descriptors.Chi2n(mol)
Descriptors.Chi3n(mol)
Descriptors.Chi4n(mol)
```

### Chi0v, Chi1v, Chi2v, Chi3v, Chi4v
Valence chi connectivity indices.
```python
Descriptors.Chi0v(mol)
Descriptors.Chi1v(mol)
Descriptors.Chi2v(mol)
Descriptors.Chi3v(mol)
Descriptors.Chi4v(mol)
```

## Hall-Kier Alpha

### HallKierAlpha
Hall-Kier alpha value (molecular flexibility).
```python
Descriptors.HallKierAlpha(mol)
```

## Balaban's J Index

### BalabanJ
Balaban's J index (branching descriptor).
```python
Descriptors.BalabanJ(mol)
```

## EState Indices

Electrotopological state indices.

### MaxEStateIndex
Maximum E-state value.
```python
Descriptors.MaxEStateIndex(mol)
```

### MinEStateIndex
Minimum E-state value.
```python
Descriptors.MinEStateIndex(mol)
```

### MaxAbsEStateIndex
Maximum absolute E-state value.
```python
Descriptors.MaxAbsEStateIndex(mol)
```

### MinAbsEStateIndex
Minimum absolute E-state value.
```python
Descriptors.MinAbsEStateIndex(mol)
```

## Partial Charges

### MaxPartialCharge
Maximum partial charge.
```python
Descriptors.MaxPartialCharge(mol)
```

### MinPartialCharge
Minimum partial charge.
```python
Descriptors.MinPartialCharge(mol)
```

### MaxAbsPartialCharge
Maximum absolute partial charge.
```python
Descriptors.MaxAbsPartialCharge(mol)
```

### MinAbsPartialCharge
Minimum absolute partial charge.
```python
Descriptors.MinAbsPartialCharge(mol)
```

## Fingerprint Density

Measures the density of molecular fingerprints.

### FpDensityMorgan1
Morgan fingerprint density at radius 1.
```python
Descriptors.FpDensityMorgan1(mol)
```

### FpDensityMorgan2
Morgan fingerprint density at radius 2.
```python
Descriptors.FpDensityMorgan2(mol)
```

### FpDensityMorgan3
Morgan fingerprint density at radius 3.
```python
Descriptors.FpDensityMorgan3(mol)
```

## PEOE VSA Descriptors

Partial Equalization of Orbital Electronegativities (PEOE) VSA descriptors.

### PEOE_VSA1 through PEOE_VSA14
MOE-type descriptors using partial charges and surface area contributions.
```python
Descriptors.PEOE_VSA1(mol)
# ... through PEOE_VSA14
```

## SMR VSA Descriptors

Molecular refractivity VSA descriptors.

### SMR_VSA1 through SMR_VSA10
MOE-type descriptors using MR contributions and surface area.
```python
Descriptors.SMR_VSA1(mol)
# ... through SMR_VSA10
```

## SLogP VSA Descriptors

LogP VSA descriptors.

### SLogP_VSA1 through SLogP_VSA12
MOE-type descriptors using LogP contributions and surface area.
```python
Descriptors.SLogP_VSA1(mol)
# ... through SLogP_VSA12
```

## EState VSA Descriptors

### EState_VSA1 through EState_VSA11
MOE-type descriptors using E-state indices and surface area.
```python
Descriptors.EState_VSA1(mol)
# ... through EState_VSA11
```

## VSA Descriptors

van der Waals surface area descriptors.

### VSA_EState1 through VSA_EState10
EState VSA descriptors.
```python
Descriptors.VSA_EState1(mol)
# ... through VSA_EState10
```

## BCUT Descriptors

Burden-CAS-University of Texas eigenvalue descriptors.

### BCUT2D_MWHI
Highest eigenvalue of Burden matrix weighted by molecular weight.
```python
Descriptors.BCUT2D_MWHI(mol)
```

### BCUT2D_MWLOW
Lowest eigenvalue of Burden matrix weighted by molecular weight.
```python
Descriptors.BCUT2D_MWLOW(mol)
```

### BCUT2D_CHGHI
Highest eigenvalue weighted by partial charges.
```python
Descriptors.BCUT2D_CHGHI(mol)
```

### BCUT2D_CHGLO
Lowest eigenvalue weighted by partial charges.
```python
Descriptors.BCUT2D_CHGLO(mol)
```

### BCUT2D_LOGPHI
Highest eigenvalue weighted by LogP.
```python
Descriptors.BCUT2D_LOGPHI(mol)
```

### BCUT2D_LOGPLOW
Lowest eigenvalue weighted by LogP.
```python
Descriptors.BCUT2D_LOGPLOW(mol)
```

### BCUT2D_MRHI
Highest eigenvalue weighted by molar refractivity.
```python
Descriptors.BCUT2D_MRHI(mol)
```

### BCUT2D_MRLOW
Lowest eigenvalue weighted by molar refractivity.
```python
Descriptors.BCUT2D_MRLOW(mol)
```

## Autocorrelation Descriptors

### AUTOCORR2D
2D autocorrelation descriptors (if enabled).
Various autocorrelation indices measuring spatial distribution of properties.

## MQN Descriptors

Molecular Quantum Numbers - 42 simple descriptors.

### mqn1 through mqn42
Integer descriptors counting various molecular features.
```python
# Access via CalcMolDescriptors
desc = Descriptors.CalcMolDescriptors(mol)
mqns = {k: v for k, v in desc.items() if k.startswith('mqn')}
```

## QED

### qed
Quantitative Estimate of Drug-likeness.
```python
Descriptors.qed(mol)
```

## Lipinski's Rule of Five

Check drug-likeness using Lipinski's criteria:

```python
def lipinski_rule_of_five(mol):
    mw = Descriptors.MolWt(mol) <= 500
    logp = Descriptors.MolLogP(mol) <= 5
    hbd = Descriptors.NumHDonors(mol) <= 5
    hba = Descriptors.NumHAcceptors(mol) <= 10
    return mw and logp and hbd and hba
```

## Batch Descriptor Calculation

Calculate all descriptors at once:

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles('CCO')

# Get all descriptors as dictionary
all_descriptors = Descriptors.CalcMolDescriptors(mol)

# Access specific descriptor
mw = all_descriptors['MolWt']
logp = all_descriptors['MolLogP']

# Get list of available descriptor names
from rdkit.Chem import Descriptors
descriptor_names = [desc[0] for desc in Descriptors._descList]
```

## Descriptor Categories Summary

1. **Physicochemical**: MolWt, MolLogP, MolMR, TPSA
2. **Topological**: BertzCT, BalabanJ, Kappa indices
3. **Electronic**: Partial charges, E-state indices
4. **Shape**: Kappa indices, BCUT descriptors
5. **Connectivity**: Chi indices
6. **2D Fingerprints**: FpDensity descriptors
7. **Atom counts**: Heavy atoms, heteroatoms, rings
8. **Drug-likeness**: QED, Lipinski parameters
9. **Flexibility**: NumRotatableBonds, HallKierAlpha
10. **Surface area**: VSA-based descriptors

## Common Use Cases

### Drug-likeness Screening

```python
def screen_druglikeness(mol):
    return {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol),
        'AromaticRings': Descriptors.NumAromaticRings(mol),
        'QED': Descriptors.qed(mol)
    }
```

### Lead-like Filtering

```python
def is_leadlike(mol):
    mw = 250 <= Descriptors.MolWt(mol) <= 350
    logp = Descriptors.MolLogP(mol) <= 3.5
    rot_bonds = Descriptors.NumRotatableBonds(mol) <= 7
    return mw and logp and rot_bonds
```

### Diversity Analysis

```python
def molecular_complexity(mol):
    return {
        'BertzCT': Descriptors.BertzCT(mol),
        'NumRings': Descriptors.RingCount(mol),
        'NumRotBonds': Descriptors.NumRotatableBonds(mol),
        'FractionCsp3': Descriptors.FractionCsp3(mol),
        'NumAromaticRings': Descriptors.NumAromaticRings(mol)
    }
```

## Tips

1. **Use batch calculation** for multiple descriptors to avoid redundant computations
2. **Check for None** - some descriptors may return None for invalid molecules
3. **Normalize descriptors** for machine learning applications
4. **Select relevant descriptors** - not all 200+ descriptors are useful for every task
5. **Consider 3D descriptors** separately (require 3D coordinates)
6. **Validate ranges** - check if descriptor values are in expected ranges

---

## Reference: Smarts_Patterns

# Common SMARTS Patterns for RDKit

This document provides a collection of commonly used SMARTS patterns for substructure searching in RDKit.

## Functional Groups

### Alcohols

```python
# Primary alcohol
'[CH2][OH1]'

# Secondary alcohol
'[CH1]([OH1])[CH3,CH2]'

# Tertiary alcohol
'[C]([OH1])([C])([C])[C]'

# Any alcohol
'[OH1][C]'

# Phenol
'c[OH1]'
```

### Aldehydes and Ketones

```python
# Aldehyde
'[CH1](=O)'

# Ketone
'[C](=O)[C]'

# Any carbonyl
'[C](=O)'
```

### Carboxylic Acids and Derivatives

```python
# Carboxylic acid
'C(=O)[OH1]'
'[CX3](=O)[OX2H1]'  # More specific

# Ester
'C(=O)O[C]'
'[CX3](=O)[OX2][C]'  # More specific

# Amide
'C(=O)N'
'[CX3](=O)[NX3]'  # More specific

# Acyl chloride
'C(=O)Cl'

# Anhydride
'C(=O)OC(=O)'
```

### Amines

```python
# Primary amine
'[NH2][C]'

# Secondary amine
'[NH1]([C])[C]'

# Tertiary amine
'[N]([C])([C])[C]'

# Aromatic amine (aniline)
'c[NH2]'

# Any amine
'[NX3]'
```

### Ethers

```python
# Aliphatic ether
'[C][O][C]'

# Aromatic ether
'c[O][C,c]'
```

### Halides

```python
# Alkyl halide
'[C][F,Cl,Br,I]'

# Aryl halide
'c[F,Cl,Br,I]'

# Specific halides
'[C]F'  # Fluoride
'[C]Cl'  # Chloride
'[C]Br'  # Bromide
'[C]I'  # Iodide
```

### Nitriles and Nitro Groups

```python
# Nitrile
'C#N'

# Nitro group
'[N+](=O)[O-]'

# Nitro on aromatic
'c[N+](=O)[O-]'
```

### Thiols and Sulfides

```python
# Thiol
'[C][SH1]'

# Sulfide
'[C][S][C]'

# Disulfide
'[C][S][S][C]'

# Sulfoxide
'[C][S](=O)[C]'

# Sulfone
'[C][S](=O)(=O)[C]'
```

## Ring Systems

### Simple Rings

```python
# Benzene ring
'c1ccccc1'
'[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1'  # Explicit atoms

# Cyclohexane
'C1CCCCC1'

# Cyclopentane
'C1CCCC1'

# Any 3-membered ring
'[r3]'

# Any 4-membered ring
'[r4]'

# Any 5-membered ring
'[r5]'

# Any 6-membered ring
'[r6]'

# Any 7-membered ring
'[r7]'
```

### Aromatic Rings

```python
# Aromatic carbon in ring
'[cR]'

# Aromatic nitrogen in ring (pyridine, etc.)
'[nR]'

# Aromatic oxygen in ring (furan, etc.)
'[oR]'

# Aromatic sulfur in ring (thiophene, etc.)
'[sR]'

# Any aromatic ring
'a1aaaaa1'
```

### Heterocycles

```python
# Pyridine
'n1ccccc1'

# Pyrrole
'n1cccc1'

# Furan
'o1cccc1'

# Thiophene
's1cccc1'

# Imidazole
'n1cncc1'

# Pyrimidine
'n1cnccc1'

# Thiazole
'n1ccsc1'

# Oxazole
'n1ccoc1'
```

### Fused Rings

```python
# Naphthalene
'c1ccc2ccccc2c1'

# Indole
'c1ccc2[nH]ccc2c1'

# Quinoline
'n1cccc2ccccc12'

# Benzimidazole
'c1ccc2[nH]cnc2c1'

# Purine
'n1cnc2ncnc2c1'
```

### Macrocycles

```python
# Rings with 8 or more atoms
'[r{8-}]'

# Rings with 9-15 atoms
'[r{9-15}]'

# Rings with more than 12 atoms (macrocycles)
'[r{12-}]'
```

## Specific Structural Features

### Aliphatic vs Aromatic

```python
# Aliphatic carbon
'[C]'

# Aromatic carbon
'[c]'

# Aliphatic carbon in ring
'[CR]'

# Aromatic carbon (alternative)
'[cR]'
```

### Stereochemistry

```python
# Tetrahedral center with clockwise chirality
'[C@]'

# Tetrahedral center with counterclockwise chirality
'[C@@]'

# Any chiral center
'[C@,C@@]'

# E double bond
'C/C=C/C'

# Z double bond
'C/C=C\\C'
```

### Hybridization

```python
# SP hybridization (triple bond)
'[CX2]'

# SP2 hybridization (double bond or aromatic)
'[CX3]'

# SP3 hybridization (single bonds)
'[CX4]'
```

### Charge

```python
# Positive charge
'[+]'

# Negative charge
'[-]'

# Specific charge
'[+1]'
'[-1]'
'[+2]'

# Positively charged nitrogen
'[N+]'

# Negatively charged oxygen
'[O-]'

# Carboxylate anion
'C(=O)[O-]'

# Ammonium cation
'[N+]([C])([C])([C])[C]'
```

## Pharmacophore Features

### Hydrogen Bond Donors

```python
# Hydroxyl
'[OH]'

# Amine
'[NH,NH2]'

# Amide NH
'[N][C](=O)'

# Any H-bond donor
'[OH,NH,NH2,NH3+]'
```

### Hydrogen Bond Acceptors

```python
# Carbonyl oxygen
'[O]=[C,S,P]'

# Ether oxygen
'[OX2]'

# Ester oxygen
'C(=O)[O]'

# Nitrogen acceptor
'[N;!H0]'

# Any H-bond acceptor
'[O,N]'
```

### Hydrophobic Groups

```python
# Alkyl chain (4+ carbons)
'CCCC'

# Branched alkyl
'C(C)(C)C'

# Aromatic rings (hydrophobic)
'c1ccccc1'
```

### Aromatic Interactions

```python
# Benzene for pi-pi stacking
'c1ccccc1'

# Heterocycle for pi-pi
'[a]1[a][a][a][a][a]1'

# Any aromatic ring
'[aR]'
```

## Drug-like Fragments

### Lipinski Fragments

```python
# Aromatic ring with substituents
'c1cc(*)ccc1'

# Aliphatic chain
'CCCC'

# Ether linkage
'[C][O][C]'

# Amine (basic center)
'[N]([C])([C])'
```

### Common Scaffolds

```python
# Benzamide
'c1ccccc1C(=O)N'

# Sulfonamide
'S(=O)(=O)N'

# Urea
'[N][C](=O)[N]'

# Guanidine
'[N]C(=[N])[N]'

# Phosphate
'P(=O)([O-])([O-])[O-]'
```

### Privileged Structures

```python
# Biphenyl
'c1ccccc1-c2ccccc2'

# Benzopyran
'c1ccc2OCCCc2c1'

# Piperazine
'N1CCNCC1'

# Piperidine
'N1CCCCC1'

# Morpholine
'N1CCOCC1'
```

## Reactive Groups

### Electrophiles

```python
# Acyl chloride
'C(=O)Cl'

# Alkyl halide
'[C][Cl,Br,I]'

# Epoxide
'C1OC1'

# Michael acceptor
'C=C[C](=O)'
```

### Nucleophiles

```python
# Primary amine
'[NH2][C]'

# Thiol
'[SH][C]'

# Alcohol
'[OH][C]'
```

## Toxicity Alerts (PAINS)

```python
# Rhodanine
'S1C(=O)NC(=S)C1'

# Catechol
'c1ccc(O)c(O)c1'

# Quinone
'O=C1C=CC(=O)C=C1'

# Hydroquinone
'OC1=CC=C(O)C=C1'

# Alkyl halide (reactive)
'[C][I,Br]'

# Michael acceptor (reactive)
'C=CC(=O)[C,N]'
```

## Metal Binding

```python
# Carboxylate (metal chelator)
'C(=O)[O-]'

# Hydroxamic acid
'C(=O)N[OH]'

# Catechol (iron chelator)
'c1c(O)c(O)ccc1'

# Thiol (metal binding)
'[SH]'

# Histidine-like (metal binding)
'c1ncnc1'
```

## Size and Complexity Filters

```python
# Long aliphatic chains (>6 carbons)
'CCCCCCC'

# Highly branched (quaternary carbon)
'C(C)(C)(C)C'

# Multiple rings
'[R]~[R]'  # Two rings connected

# Spiro center
'[C]12[C][C][C]1[C][C]2'
```

## Special Patterns

### Atom Counts

```python
# Any atom
'[*]'

# Heavy atom (not H)
'[!H]'

# Carbon
'[C,c]'

# Heteroatom
'[!C;!H]'

# Halogen
'[F,Cl,Br,I]'
```

### Bond Types

```python
# Single bond
'C-C'

# Double bond
'C=C'

# Triple bond
'C#C'

# Aromatic bond
'c:c'

# Any bond
'C~C'
```

### Ring Membership

```python
# In any ring
'[R]'

# Not in ring
'[!R]'

# In exactly one ring
'[R1]'

# In exactly two rings
'[R2]'

# Ring bond
'[R]~[R]'
```

### Degree and Connectivity

```python
# Total degree 1 (terminal atom)
'[D1]'

# Total degree 2 (chain)
'[D2]'

# Total degree 3 (branch point)
'[D3]'

# Total degree 4 (highly branched)
'[D4]'

# Connected to exactly 2 carbons
'[C]([C])[C]'
```

## Usage Examples

```python
from rdkit import Chem

# Create SMARTS query
pattern = Chem.MolFromSmarts('[CH2][OH1]')  # Primary alcohol

# Search molecule
mol = Chem.MolFromSmiles('CCO')
matches = mol.GetSubstructMatches(pattern)

# Multiple patterns
patterns = {
    'alcohol': '[OH1][C]',
    'amine': '[NH2,NH1][C]',
    'carboxylic_acid': 'C(=O)[OH1]'
}

# Check for functional groups
for name, smarts in patterns.items():
    query = Chem.MolFromSmarts(smarts)
    if mol.HasSubstructMatch(query):
        print(f"Found {name}")
```

## Tips for Writing SMARTS

1. **Be specific when needed:** Use atom properties [CX3] instead of just [C]
2. **Use brackets for clarity:** [C] is different from C (aromatic)
3. **Consider aromaticity:** lowercase letters (c, n, o) are aromatic
4. **Check ring membership:** [R] for in-ring, [!R] for not in-ring
5. **Use recursive SMARTS:** $(...) for complex patterns
6. **Test patterns:** Always validate SMARTS on known molecules
7. **Start simple:** Build complex patterns incrementally

## Common SMARTS Syntax

- `[C]` - Aliphatic carbon
- `[c]` - Aromatic carbon
- `[CX4]` - Carbon with 4 connections (sp3)
- `[CX3]` - Carbon with 3 connections (sp2)
- `[CX2]` - Carbon with 2 connections (sp)
- `[CH3]` - Methyl group
- `[R]` - In ring
- `[r6]` - In 6-membered ring
- `[r{5-7}]` - In 5, 6, or 7-membered ring
- `[D2]` - Degree 2 (2 neighbors)
- `[+]` - Positive charge
- `[-]` - Negative charge
- `[!C]` - Not carbon
- `[#6]` - Element with atomic number 6 (carbon)
- `~` - Any bond type
- `-` - Single bond
- `=` - Double bond
- `#` - Triple bond
- `:` - Aromatic bond
- `@` - Clockwise chirality
- `@@` - Counter-clockwise chirality
