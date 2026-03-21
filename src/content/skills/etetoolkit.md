---
title: "ETE Toolkit 系统发育"
description: "Python 系统发育分析工具包，进化树构建和可视化"
category: "research"
source: "community"
author: "Community"
tags: ["etetoolkit"]
date: 2026-03-20
---

# ETE Toolkit Skill

## Overview

ETE (Environment for Tree Exploration) is a toolkit for phylogenetic and hierarchical tree analysis. Manipulate trees, analyze evolutionary events, visualize results, and integrate with biological databases for phylogenomic research and clustering analysis.

## Core Capabilities

### 1. Tree Manipulation and Analysis

Load, manipulate, and analyze hierarchical tree structures with support for:

- **Tree I/O**: Read and write Newick, NHX, PhyloXML, and NeXML formats
- **Tree traversal**: Navigate trees using preorder, postorder, or levelorder strategies
- **Topology modification**: Prune, root, collapse nodes, resolve polytomies
- **Distance calculations**: Compute branch lengths and topological distances between nodes
- **Tree comparison**: Calculate Robinson-Foulds distances and identify topological differences

**Common patterns:**

```python
from ete3 import Tree

# Load tree from file
tree = Tree("tree.nw", format=1)

# Basic statistics
print(f"Leaves: {len(tree)}")
print(f"Total nodes: {len(list(tree.traverse()))}")

# Prune to taxa of interest
taxa_to_keep = ["species1", "species2", "species3"]
tree.prune(taxa_to_keep, preserve_branch_length=True)

# Midpoint root
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Save modified tree
tree.write(outfile="rooted_tree.nw")
```

Use `scripts/tree_operations.py` for command-line tree manipulation:

```bash
# Display tree statistics
python scripts/tree_operations.py stats tree.nw

# Convert format
python scripts/tree_operations.py convert tree.nw output.nw --in-format 0 --out-format 1

# Reroot tree
python scripts/tree_operations.py reroot tree.nw rooted.nw --midpoint

# Prune to specific taxa
python scripts/tree_operations.py prune tree.nw pruned.nw --keep-taxa "sp1,sp2,sp3"

# Show ASCII visualization
python scripts/tree_operations.py ascii tree.nw
```

### 2. Phylogenetic Analysis

Analyze gene trees with evolutionary event detection:

- **Sequence alignment integration**: Link trees to multiple sequence alignments (FASTA, Phylip)
- **Species naming**: Automatic or custom species extraction from gene names
- **Evolutionary events**: Detect duplication and speciation events using Species Overlap or tree reconciliation
- **Orthology detection**: Identify orthologs and paralogs based on evolutionary events
- **Gene family analysis**: Split trees by duplications, collapse lineage-specific expansions

**Workflow for gene tree analysis:**

```python
from ete3 import PhyloTree

# Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# Set species naming function
def get_species(gene_name):
    return gene_name.split("_")[0]

tree.set_species_naming_function(get_species)

# Detect evolutionary events
events = tree.get_descendant_evol_events()

# Analyze events
for node in tree.traverse():
    if hasattr(node, "evoltype"):
        if node.evoltype == "D":
            print(f"Duplication at {node.name}")
        elif node.evoltype == "S":
            print(f"Speciation at {node.name}")

# Extract ortholog groups
ortho_groups = tree.get_speciation_trees()
for i, ortho_tree in enumerate(ortho_groups):
    ortho_tree.write(outfile=f"ortholog_group_{i}.nw")
```

**Finding orthologs and paralogs:**

```python
# Find orthologs to query gene
query = tree & "species1_gene1"

orthologs = []
paralogs = []

for event in events:
    if query in event.in_seqs:
        if event.etype == "S":
            orthologs.extend([s for s in event.out_seqs if s != query])
        elif event.etype == "D":
            paralogs.extend([s for s in event.out_seqs if s != query])
```

### 3. NCBI Taxonomy Integration

Integrate taxonomic information from NCBI Taxonomy database:

- **Database access**: Automatic download and local caching of NCBI taxonomy (~300MB)
- **Taxid/name translation**: Convert between taxonomic IDs and scientific names
- **Lineage retrieval**: Get complete evolutionary lineages
- **Taxonomy trees**: Build species trees connecting specified taxa
- **Tree annotation**: Automatically annotate trees with taxonomic information

**Building taxonomy-based trees:**

```python
from ete3 import NCBITaxa

ncbi = NCBITaxa()

# Build tree from species names
species = ["Homo sapiens", "Pan troglodytes", "Mus musculus"]
name2taxid = ncbi.get_name_translator(species)
taxids = [name2taxid[sp][0] for sp in species]

# Get minimal tree connecting taxa
tree = ncbi.get_topology(taxids)

# Annotate nodes with taxonomy info
for node in tree.traverse():
    if hasattr(node, "sci_name"):
        print(f"{node.sci_name} - Rank: {node.rank} - TaxID: {node.taxid}")
```

**Annotating existing trees:**

```python
# Get taxonomy info for tree leaves
for leaf in tree:
    species = extract_species_from_name(leaf.name)
    taxid = ncbi.get_name_translator([species])[species][0]

    # Get lineage
    lineage = ncbi.get_lineage(taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    # Add to node
    leaf.add_feature("taxid", taxid)
    leaf.add_feature("lineage", [names[t] for t in lineage])
```

### 4. Tree Visualization

Create publication-quality tree visualizations:

- **Output formats**: PNG (raster), PDF, and SVG (vector) for publications
- **Layout modes**: Rectangular and circular tree layouts
- **Interactive GUI**: Explore trees interactively with zoom, pan, and search
- **Custom styling**: NodeStyle for node appearance (colors, shapes, sizes)
- **Faces**: Add graphical elements (text, images, charts, heatmaps) to nodes
- **Layout functions**: Dynamic styling based on node properties

**Basic visualization workflow:**

```python
from ete3 import Tree, TreeStyle, NodeStyle

tree = Tree("tree.nw")

# Configure tree style
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
ts.scale = 50  # pixels per branch length unit

# Style nodes
for node in tree.traverse():
    nstyle = NodeStyle()

    if node.is_leaf():
        nstyle["fgcolor"] = "blue"
        nstyle["size"] = 8
    else:
        # Color by support
        if node.support > 0.9:
            nstyle["fgcolor"] = "darkgreen"
        else:
            nstyle["fgcolor"] = "red"
        nstyle["size"] = 5

    node.set_style(nstyle)

# Render to file
tree.render("tree.pdf", tree_style=ts)
tree.render("tree.png", w=800, h=600, units="px", dpi=300)
```

Use `scripts/quick_visualize.py` for rapid visualization:

```bash
# Basic visualization
python scripts/quick_visualize.py tree.nw output.pdf

# Circular layout with custom styling
python scripts/quick_visualize.py tree.nw output.pdf --mode c --color-by-support

# High-resolution PNG
python scripts/quick_visualize.py tree.nw output.png --width 1200 --height 800 --units px --dpi 300

# Custom title and styling
python scripts/quick_visualize.py tree.nw output.pdf --title "Species Phylogeny" --show-support
```

**Advanced visualization with faces:**

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace

tree = Tree("tree.nw")

# Add features to nodes
for leaf in tree:
    leaf.add_feature("habitat", "marine" if "fish" in leaf.name else "land")

# Layout function
def layout(node):
    if node.is_leaf():
        # Add colored circle
        color = "blue" if node.habitat == "marine" else "green"
        circle = CircleFace(radius=5, color=color)
        node.add_face(circle, column=0, position="aligned")

        # Add label
        label = TextFace(node.name, fsize=10)
        node.add_face(label, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("annotated_tree.pdf", tree_style=ts)
```

### 5. Clustering Analysis

Analyze hierarchical clustering results with data integration:

- **ClusterTree**: Specialized class for clustering dendrograms
- **Data matrix linking**: Connect tree leaves to numerical profiles
- **Cluster metrics**: Silhouette coefficient, Dunn index, inter/intra-cluster distances
- **Validation**: Test cluster quality with different distance metrics
- **Heatmap visualization**: Display data matrices alongside trees

**Clustering workflow:**

```python
from ete3 import ClusterTree

# Load tree with data matrix
matrix = """#Names\tSample1\tSample2\tSample3
Gene1\t1.5\t2.3\t0.8
Gene2\t0.9\t1.1\t1.8
Gene3\t2.1\t2.5\t0.5"""

tree = ClusterTree("((Gene1,Gene2),Gene3);", text_array=matrix)

# Evaluate cluster quality
for node in tree.traverse():
    if not node.is_leaf():
        silhouette = node.get_silhouette()
        dunn = node.get_dunn()

        print(f"Cluster: {node.name}")
        print(f"  Silhouette: {silhouette:.3f}")
        print(f"  Dunn index: {dunn:.3f}")

# Visualize with heatmap
tree.show("heatmap")
```

### 6. Tree Comparison

Quantify topological differences between trees:

- **Robinson-Foulds distance**: Standard metric for tree comparison
- **Normalized RF**: Scale-invariant distance (0.0 to 1.0)
- **Partition analysis**: Identify unique and shared bipartitions
- **Consensus trees**: Analyze support across multiple trees
- **Batch comparison**: Compare multiple trees pairwise

**Compare two trees:**

```python
from ete3 import Tree

tree1 = Tree("tree1.nw")
tree2 = Tree("tree2.nw")

# Calculate RF distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = tree1.robinson_foulds(tree2)

print(f"RF distance: {rf}/{max_rf}")
print(f"Normalized RF: {rf/max_rf:.3f}")
print(f"Common leaves: {len(common_leaves)}")

# Find unique partitions
unique_t1 = parts_t1 - parts_t2
unique_t2 = parts_t2 - parts_t1

print(f"Unique to tree1: {len(unique_t1)}")
print(f"Unique to tree2: {len(unique_t2)}")
```

**Compare multiple trees:**

```python
import numpy as np

trees = [Tree(f"tree{i}.nw") for i in range(4)]

# Create distance matrix
n = len(trees)
dist_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(i+1, n):
        rf, max_rf, _, _, _ = trees[i].robinson_foulds(trees[j])
        norm_rf = rf / max_rf if max_rf > 0 else 0
        dist_matrix[i, j] = norm_rf
        dist_matrix[j, i] = norm_rf
```

## Installation and Setup

Install ETE toolkit:

```bash
# Basic installation
uv pip install ete3

# With external dependencies for rendering (optional but recommended)
# On macOS:
brew install qt@5

# On Ubuntu/Debian:
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg

# For full features including GUI
uv pip install ete3[gui]
```

**First-time NCBI Taxonomy setup:**

The first time NCBITaxa is instantiated, it automatically downloads the NCBI taxonomy database (~300MB) to `~/.etetoolkit/taxa.sqlite`. This happens only once:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()  # Downloads database on first run
```

Update taxonomy database:

```python
ncbi.update_taxonomy_database()  # Download latest NCBI data
```

## Common Use Cases

### Use Case 1: Phylogenomic Pipeline

Complete workflow from gene tree to ortholog identification:

```python
from ete3 import PhyloTree, NCBITaxa

# 1. Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# 2. Configure species naming
tree.set_species_naming_function(lambda x: x.split("_")[0])

# 3. Detect evolutionary events
tree.get_descendant_evol_events()

# 4. Annotate with taxonomy
ncbi = NCBITaxa()
for leaf in tree:
    if leaf.species in species_to_taxid:
        taxid = species_to_taxid[leaf.species]
        lineage = ncbi.get_lineage(taxid)
        leaf.add_feature("lineage", lineage)

# 5. Extract ortholog groups
ortho_groups = tree.get_speciation_trees()

# 6. Save and visualize
for i, ortho in enumerate(ortho_groups):
    ortho.write(outfile=f"ortho_{i}.nw")
```

### Use Case 2: Tree Preprocessing and Formatting

Batch process trees for analysis:

```bash
# Convert format
python scripts/tree_operations.py convert input.nw output.nw --in-format 0 --out-format 1

# Root at midpoint
python scripts/tree_operations.py reroot input.nw rooted.nw --midpoint

# Prune to focal taxa
python scripts/tree_operations.py prune rooted.nw pruned.nw --keep-taxa taxa_list.txt

# Get statistics
python scripts/tree_operations.py stats pruned.nw
```

### Use Case 3: Publication-Quality Figures

Create styled visualizations:

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

# Define clade colors
clade_colors = {
    "Mammals": "red",
    "Birds": "blue",
    "Fish": "green"
}

def layout(node):
    # Highlight clades
    if node.is_leaf():
        for clade, color in clade_colors.items():
            if clade in node.name:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color
                nstyle["size"] = 8
                node.set_style(nstyle)
    else:
        # Add support values
        if node.support > 0.95:
            support = TextFace(f"{node.support:.2f}", fsize=8)
            node.add_face(support, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_scale = True

# Render for publication
tree.render("figure.pdf", w=200, units="mm", tree_style=ts)
tree.render("figure.svg", tree_style=ts)  # Editable vector
```

### Use Case 4: Automated Tree Analysis

Process multiple trees systematically:

```python
from ete3 import Tree
import os

input_dir = "trees"
output_dir = "processed"

for filename in os.listdir(input_dir):
    if filename.endswith(".nw"):
        tree = Tree(os.path.join(input_dir, filename))

        # Standardize: midpoint root, resolve polytomies
        midpoint = tree.get_midpoint_outgroup()
        tree.set_outgroup(midpoint)
        tree.resolve_polytomy(recursive=True)

        # Filter low support branches
        for node in tree.traverse():
            if hasattr(node, 'support') and node.support < 0.5:
                if not node.is_leaf() and not node.is_root():
                    node.delete()

        # Save processed tree
        output_file = os.path.join(output_dir, f"processed_{filename}")
        tree.write(outfile=output_file)
```

## Reference Documentation

For comprehensive API documentation, code examples, and detailed guides, refer to the following resources in the `references/` directory:

- **`api_reference.md`**: Complete API documentation for all ETE classes and methods (Tree, PhyloTree, ClusterTree, NCBITaxa), including parameters, return types, and code examples
- **`workflows.md`**: Common workflow patterns organized by task (tree operations, phylogenetic analysis, tree comparison, taxonomy integration, clustering analysis)
- **`visualization.md`**: Comprehensive visualization guide covering TreeStyle, NodeStyle, Faces, layout functions, and advanced visualization techniques

Load these references when detailed information is needed:

```python
# To use API reference
# Read references/api_reference.md for complete method signatures and parameters

# To implement workflows
# Read references/workflows.md for step-by-step workflow examples

# To create visualizations
# Read references/visualization.md for styling and rendering options
```

## Troubleshooting

**Import errors:**

```bash
# If "ModuleNotFoundError: No module named 'ete3'"
uv pip install ete3

# For GUI and rendering issues
uv pip install ete3[gui]
```

**Rendering issues:**

If `tree.render()` or `tree.show()` fails with Qt-related errors, install system dependencies:

```bash
# macOS
brew install qt@5

# Ubuntu/Debian
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

**NCBI Taxonomy database:**

If database download fails or becomes corrupted:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()  # Redownload database
```

**Memory issues with large trees:**

For very large trees (>10,000 leaves), use iterators instead of list comprehensions:

```python
# Memory-efficient iteration
for leaf in tree.iter_leaves():
    process(leaf)

# Instead of
for leaf in tree.get_leaves():  # Loads all into memory
    process(leaf)
```

## Newick Format Reference

ETE supports multiple Newick format specifications (0-100):

- **Format 0**: Flexible with branch lengths (default)
- **Format 1**: With internal node names
- **Format 2**: With bootstrap/support values
- **Format 5**: Internal node names + branch lengths
- **Format 8**: All features (names, distances, support)
- **Format 9**: Leaf names only
- **Format 100**: Topology only

Specify format when reading/writing:

```python
tree = Tree("tree.nw", format=1)
tree.write(outfile="output.nw", format=5)
```

NHX (New Hampshire eXtended) format preserves custom features:

```python
tree.write(outfile="tree.nhx", features=["habitat", "temperature", "depth"])
```

## Best Practices

1. **Preserve branch lengths**: Use `preserve_branch_length=True` when pruning for phylogenetic analysis
2. **Cache content**: Use `get_cached_content()` for repeated access to node contents on large trees
3. **Use iterators**: Employ `iter_*` methods for memory-efficient processing of large trees
4. **Choose appropriate traversal**: Postorder for bottom-up analysis, preorder for top-down
5. **Validate monophyly**: Always check returned clade type (monophyletic/paraphyletic/polyphyletic)
6. **Vector formats for publication**: Use PDF or SVG for publication figures (scalable, editable)
7. **Interactive testing**: Use `tree.show()` to test visualizations before rendering to file
8. **PhyloTree for phylogenetics**: Use PhyloTree class for gene trees and evolutionary analysis
9. **Copy method selection**: "newick" for speed, "cpickle" for full fidelity, "deepcopy" for complex objects
10. **NCBI query caching**: Store NCBI taxonomy query results to avoid repeated database access

---

## Reference: Api_Reference

# ETE Toolkit API Reference

## Overview

ETE (Environment for Tree Exploration) is a Python toolkit for phylogenetic tree manipulation, analysis, and visualization. This reference covers the main classes and methods.

## Core Classes

### TreeNode (alias: Tree)

The fundamental class representing tree structures with hierarchical node organization.

**Constructor:**
```python
from ete3 import Tree
t = Tree(newick=None, format=0, dist=None, support=None, name=None)
```

**Parameters:**
- `newick`: Newick string or file path
- `format`: Newick format (0-100). Common formats:
  - `0`: Flexible format with branch lengths and names
  - `1`: With internal node names
  - `2`: With bootstrap/support values
  - `5`: Internal node names and branch lengths
  - `8`: All features (names, distances, support)
  - `9`: Leaf names only
  - `100`: Topology only
- `dist`: Branch length to parent (default: 1.0)
- `support`: Bootstrap/confidence value (default: 1.0)
- `name`: Node identifier

### PhyloTree

Specialized class for phylogenetic analysis, extending TreeNode.

**Constructor:**
```python
from ete3 import PhyloTree
t = PhyloTree(newick=None, alignment=None, alg_format='fasta',
              sp_naming_function=None, format=0)
```

**Additional Parameters:**
- `alignment`: Path to alignment file or alignment string
- `alg_format`: 'fasta' or 'phylip'
- `sp_naming_function`: Custom function to extract species from node names

### ClusterTree

Class for hierarchical clustering analysis.

**Constructor:**
```python
from ete3 import ClusterTree
t = ClusterTree(newick, text_array=None)
```

**Parameters:**
- `text_array`: Tab-delimited matrix with column headers and row names

### NCBITaxa

Class for NCBI taxonomy database operations.

**Constructor:**
```python
from ete3 import NCBITaxa
ncbi = NCBITaxa(dbfile=None)
```

First instantiation downloads ~300MB NCBI taxonomy database to `~/.etetoolkit/taxa.sqlite`.

## Node Properties

### Basic Attributes

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `name` | str | Node identifier | "NoName" |
| `dist` | float | Branch length to parent | 1.0 |
| `support` | float | Bootstrap/confidence value | 1.0 |
| `up` | TreeNode | Parent node reference | None |
| `children` | list | Child nodes | [] |

### Custom Features

Add any custom data to nodes:
```python
node.add_feature("custom_name", value)
node.add_features(feature1=value1, feature2=value2)
```

Access features:
```python
value = node.custom_name
# or
value = getattr(node, "custom_name", default_value)
```

## Navigation & Traversal

### Basic Navigation

```python
# Check node type
node.is_leaf()          # Returns True if terminal node
node.is_root()          # Returns True if root node
len(node)               # Number of leaves under node

# Get relatives
parent = node.up
children = node.children
root = node.get_tree_root()
```

### Traversal Strategies

```python
# Three traversal strategies
for node in tree.traverse("preorder"):    # Root → Left → Right
    print(node.name)

for node in tree.traverse("postorder"):   # Left → Right → Root
    print(node.name)

for node in tree.traverse("levelorder"):  # Level by level
    print(node.name)

# Exclude root
for node in tree.iter_descendants("postorder"):
    print(node.name)
```

### Getting Nodes

```python
# Get all leaves
leaves = tree.get_leaves()
for leaf in tree:  # Shortcut iteration
    print(leaf.name)

# Get all descendants
descendants = tree.get_descendants()

# Get ancestors
ancestors = node.get_ancestors()

# Get specific nodes by attribute
nodes = tree.search_nodes(name="NodeA")
node = tree & "NodeA"  # Shortcut syntax

# Get leaves by name
leaves = tree.get_leaves_by_name("LeafA")

# Get common ancestor
ancestor = tree.get_common_ancestor("LeafA", "LeafB", "LeafC")

# Custom filtering
filtered = [n for n in tree.traverse() if n.dist > 0.5 and n.is_leaf()]
```

### Iterator Methods (Memory Efficient)

```python
# For large trees, use iterators
for match in tree.iter_search_nodes(name="X"):
    if some_condition:
        break  # Stop early

for leaf in tree.iter_leaves():
    process(leaf)

for descendant in node.iter_descendants():
    process(descendant)
```

## Tree Construction & Modification

### Creating Trees from Scratch

```python
# Empty tree
t = Tree()

# Add children
child1 = t.add_child(name="A", dist=1.0)
child2 = t.add_child(name="B", dist=2.0)

# Add siblings
sister = child1.add_sister(name="C", dist=1.5)

# Populate with random topology
t.populate(10)  # Creates 10 random leaves
t.populate(5, names_library=["A", "B", "C", "D", "E"])
```

### Removing & Deleting Nodes

```python
# Detach: removes entire subtree
node.detach()
# or
parent.remove_child(node)

# Delete: removes node, reconnects children to parent
node.delete()
# or
parent.remove_child(node)
```

### Pruning

Keep only specified leaves:
```python
# Keep only these leaves, remove all others
tree.prune(["A", "B", "C"])

# Preserve original branch lengths
tree.prune(["A", "B", "C"], preserve_branch_length=True)
```

### Tree Concatenation

```python
# Attach one tree as child of another
t1 = Tree("(A,(B,C));")
t2 = Tree("((D,E),(F,G));")
A = t1 & "A"
A.add_child(t2)
```

### Tree Copying

```python
# Four copy methods
copy1 = tree.copy()  # Default: cpickle (preserves types)
copy2 = tree.copy("newick")  # Fastest: basic topology
copy3 = tree.copy("newick-extended")  # Includes custom features as text
copy4 = tree.copy("deepcopy")  # Slowest: handles complex objects
```

## Tree Operations

### Rooting

```python
# Set outgroup (reroot tree)
outgroup_node = tree & "OutgroupLeaf"
tree.set_outgroup(outgroup_node)

# Midpoint rooting
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Unroot tree
tree.unroot()
```

### Resolving Polytomies

```python
# Resolve multifurcations to bifurcations
tree.resolve_polytomy(recursive=False)  # Single node only
tree.resolve_polytomy(recursive=True)   # Entire tree
```

### Ladderize

```python
# Sort branches by size
tree.ladderize()
tree.ladderize(direction=1)  # Ascending order
```

### Convert to Ultrametric

```python
# Make all leaves equidistant from root
tree.convert_to_ultrametric()
tree.convert_to_ultrametric(tree_length=100)  # Specific total length
```

## Distance & Comparison

### Distance Calculations

```python
# Branch length distance between nodes
dist = tree.get_distance("A", "B")
dist = nodeA.get_distance(nodeB)

# Topology-only distance (count nodes)
dist = tree.get_distance("A", "B", topology_only=True)

# Farthest node
farthest, distance = node.get_farthest_node()
farthest_leaf, distance = node.get_farthest_leaf()
```

### Monophyly Testing

```python
# Check if values form monophyletic group
is_mono, clade_type, base_node = tree.check_monophyly(
    values=["A", "B", "C"],
    target_attr="name"
)
# Returns: (bool, "monophyletic"|"paraphyletic"|"polyphyletic", node)

# Get all monophyletic clades
monophyletic_nodes = tree.get_monophyletic(
    values=["A", "B", "C"],
    target_attr="name"
)
```

### Tree Comparison

```python
# Robinson-Foulds distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = t1.robinson_foulds(t2)
print(f"RF distance: {rf}/{max_rf}")

# Normalized RF distance
result = t1.compare(t2)
norm_rf = result["norm_rf"]  # 0.0 to 1.0
ref_edges = result["ref_edges_in_source"]
```

## Input/Output

### Reading Trees

```python
# From string
t = Tree("(A:1,(B:1,(C:1,D:1):0.5):0.5);")

# From file
t = Tree("tree.nw")

# With format
t = Tree("tree.nw", format=1)
```

### Writing Trees

```python
# To string
newick = tree.write()
newick = tree.write(format=1)
newick = tree.write(format=1, features=["support", "custom_feature"])

# To file
tree.write(outfile="output.nw")
tree.write(format=5, outfile="output.nw", features=["name", "dist"])

# Custom leaf function (for collapsing)
def is_leaf(node):
    return len(node) <= 3  # Treat small clades as leaves

newick = tree.write(is_leaf_fn=is_leaf)
```

### Tree Rendering

```python
# Show interactive GUI
tree.show()

# Render to file (PNG, PDF, SVG)
tree.render("tree.png")
tree.render("tree.pdf", w=200, units="mm")
tree.render("tree.svg", dpi=300)

# ASCII representation
print(tree)
print(tree.get_ascii(show_internal=True, compact=False))
```

## Performance Optimization

### Caching Content

For frequent access to node contents:
```python
# Cache all node contents
node2content = tree.get_cached_content()

# Fast lookup
for node in tree.traverse():
    leaves = node2content[node]
    print(f"Node has {len(leaves)} leaves")
```

### Precomputing Distances

```python
# For multiple distance queries
node2dist = {}
for node in tree.traverse():
    node2dist[node] = node.get_distance(tree)
```

## PhyloTree-Specific Methods

### Sequence Alignment

```python
# Link alignment
tree.link_to_alignment("alignment.fasta", alg_format="fasta")

# Access sequences
for leaf in tree:
    print(f"{leaf.name}: {leaf.sequence}")
```

### Species Naming

```python
# Default: first 3 letters
# Custom function
def get_species(node_name):
    return node_name.split("_")[0]

tree.set_species_naming_function(get_species)

# Manual setting
for leaf in tree:
    leaf.species = extract_species(leaf.name)
```

### Evolutionary Events

```python
# Detect duplication/speciation events
events = tree.get_descendant_evol_events()

for node in tree.traverse():
    if hasattr(node, "evoltype"):
        print(f"{node.name}: {node.evoltype}")  # "D" or "S"

# With species tree
species_tree = Tree("(human, (chimp, gorilla));")
events = tree.get_descendant_evol_events(species_tree=species_tree)
```

### Gene Tree Operations

```python
# Get species trees from duplicated gene families
species_trees = tree.get_speciation_trees()

# Split by duplication events
subtrees = tree.split_by_dups()

# Collapse lineage-specific expansions
tree.collapse_lineage_specific_expansions()
```

## NCBITaxa Methods

### Database Operations

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()

# Update database
ncbi.update_taxonomy_database()
```

### Querying Taxonomy

```python
# Get taxid from name
taxid = ncbi.get_name_translator(["Homo sapiens"])
# Returns: {'Homo sapiens': [9606]}

# Get name from taxid
names = ncbi.get_taxid_translator([9606, 9598])
# Returns: {9606: 'Homo sapiens', 9598: 'Pan troglodytes'}

# Get rank
rank = ncbi.get_rank([9606])
# Returns: {9606: 'species'}

# Get lineage
lineage = ncbi.get_lineage(9606)
# Returns: [1, 131567, 2759, ..., 9606]

# Get descendants
descendants = ncbi.get_descendant_taxa("Primates")
descendants = ncbi.get_descendant_taxa("Primates", collapse_subspecies=True)
```

### Building Taxonomy Trees

```python
# Get minimal tree connecting taxa
tree = ncbi.get_topology([9606, 9598, 9593])  # Human, chimp, gorilla

# Annotate tree with taxonomy
tree.annotate_ncbi_taxa()

# Access taxonomy info
for node in tree.traverse():
    print(f"{node.sci_name} ({node.taxid}) - Rank: {node.rank}")
```

## ClusterTree Methods

### Linking to Data

```python
# Link matrix to tree
tree.link_to_arraytable(matrix_string)

# Access profiles
for leaf in tree:
    print(leaf.profile)  # Numerical array
```

### Cluster Metrics

```python
# Get silhouette coefficient
silhouette = tree.get_silhouette()

# Get Dunn index
dunn = tree.get_dunn()

# Inter/intra cluster distances
inter = node.intercluster_dist
intra = node.intracluster_dist

# Standard deviation
dev = node.deviation
```

### Distance Metrics

Supported metrics:
- `"euclidean"`: Euclidean distance
- `"pearson"`: Pearson correlation
- `"spearman"`: Spearman rank correlation

```python
tree.dist_to(node2, metric="pearson")
```

## Common Error Handling

```python
# Check if tree is empty
if tree.children:
    print("Tree has children")

# Check if node exists
nodes = tree.search_nodes(name="X")
if nodes:
    node = nodes[0]

# Safe feature access
value = getattr(node, "feature_name", default_value)

# Check format compatibility
try:
    tree.write(format=1)
except:
    print("Tree lacks internal node names")
```

## Best Practices

1. **Use appropriate traversal**: Postorder for bottom-up, preorder for top-down
2. **Cache for repeated access**: Use `get_cached_content()` for frequent queries
3. **Use iterators for large trees**: Memory-efficient processing
4. **Preserve branch lengths**: Use `preserve_branch_length=True` when pruning
5. **Choose copy method wisely**: "newick" for speed, "cpickle" for full fidelity
6. **Validate monophyly**: Check returned clade type (monophyletic/paraphyletic/polyphyletic)
7. **Use PhyloTree for phylogenetics**: Specialized methods for evolutionary analysis
8. **Cache NCBI queries**: Store results to avoid repeated database access

---

## Reference: Visualization

# ETE Toolkit Visualization Guide

Complete guide to tree visualization with ETE Toolkit.

## Table of Contents
1. [Rendering Basics](#rendering-basics)
2. [TreeStyle Configuration](#treestyle-configuration)
3. [Node Styling](#node-styling)
4. [Faces](#faces)
5. [Layout Functions](#layout-functions)
6. [Advanced Visualization](#advanced-visualization)

---

## Rendering Basics

### Output Formats

ETE supports three main output formats:

```python
from ete3 import Tree

tree = Tree("tree.nw")

# PNG (raster, good for presentations)
tree.render("output.png", w=800, h=600, units="px", dpi=300)

# PDF (vector, good for publications)
tree.render("output.pdf", w=200, units="mm")

# SVG (vector, editable)
tree.render("output.svg")
```

### Units and Dimensions

```python
# Pixels
tree.render("tree.png", w=1200, h=800, units="px")

# Millimeters
tree.render("tree.pdf", w=210, h=297, units="mm")  # A4 size

# Inches
tree.render("tree.pdf", w=8.5, h=11, units="in")  # US Letter

# Auto-size (aspect ratio preserved)
tree.render("tree.pdf", w=200, units="mm")  # Height auto-calculated
```

### Interactive Visualization

```python
from ete3 import Tree

tree = Tree("tree.nw")

# Launch GUI
# - Zoom with mouse wheel
# - Pan by dragging
# - Search with Ctrl+F
# - Export from menu
# - Edit node properties
tree.show()
```

---

## TreeStyle Configuration

### Basic TreeStyle Options

```python
from ete3 import Tree, TreeStyle

tree = Tree("tree.nw")
ts = TreeStyle()

# Display options
ts.show_leaf_name = True          # Show leaf names
ts.show_branch_length = True      # Show branch lengths
ts.show_branch_support = True     # Show support values
ts.show_scale = True              # Show scale bar

# Branch length scaling
ts.scale = 50                     # Pixels per branch length unit
ts.min_leaf_separation = 10       # Minimum space between leaves (pixels)

# Layout orientation
ts.rotation = 0                   # 0=left-to-right, 90=top-to-bottom
ts.branch_vertical_margin = 10    # Vertical spacing between branches

# Tree shape
ts.mode = "r"                     # "r"=rectangular (default), "c"=circular

tree.render("tree.pdf", tree_style=ts)
```

### Circular Trees

```python
from ete3 import Tree, TreeStyle

tree = Tree("tree.nw")
ts = TreeStyle()

# Circular mode
ts.mode = "c"
ts.arc_start = 0      # Starting angle (degrees)
ts.arc_span = 360     # Angular span (degrees, 360=full circle)

# For semicircle
ts.arc_start = -180
ts.arc_span = 180

tree.render("circular_tree.pdf", tree_style=ts)
```

### Title and Legend

```python
from ete3 import Tree, TreeStyle, TextFace

tree = Tree("tree.nw")
ts = TreeStyle()

# Add title
title = TextFace("Phylogenetic Tree of Species", fsize=20, bold=True)
ts.title.add_face(title, column=0)

# Add legend
ts.legend.add_face(TextFace("Red nodes: High support", fsize=10), column=0)
ts.legend.add_face(TextFace("Blue nodes: Low support", fsize=10), column=0)

# Legend position
ts.legend_position = 1  # 1=top-right, 2=top-left, 3=bottom-left, 4=bottom-right

tree.render("tree_with_legend.pdf", tree_style=ts)
```

### Custom Background

```python
from ete3 import Tree, TreeStyle

tree = Tree("tree.nw")
ts = TreeStyle()

# Background color
ts.bgcolor = "#f0f0f0"  # Light gray background

# Tree border
ts.show_border = True

tree.render("tree_background.pdf", tree_style=ts)
```

---

## Node Styling

### NodeStyle Properties

```python
from ete3 import Tree, NodeStyle

tree = Tree("tree.nw")

for node in tree.traverse():
    nstyle = NodeStyle()

    # Node size and shape
    nstyle["size"] = 10                # Node size in pixels
    nstyle["shape"] = "circle"         # "circle", "square", "sphere"

    # Colors
    nstyle["fgcolor"] = "blue"         # Foreground color (node itself)
    nstyle["bgcolor"] = "lightblue"    # Background color (only for sphere)

    # Line style for branches
    nstyle["hz_line_type"] = 0         # 0=solid, 1=dashed, 2=dotted
    nstyle["vt_line_type"] = 0         # Vertical line type
    nstyle["hz_line_color"] = "black"  # Horizontal line color
    nstyle["vt_line_color"] = "black"  # Vertical line color
    nstyle["hz_line_width"] = 2        # Line width in pixels
    nstyle["vt_line_width"] = 2

    node.set_style(nstyle)

tree.render("styled_tree.pdf")
```

### Conditional Styling

```python
from ete3 import Tree, NodeStyle

tree = Tree("tree.nw")

# Style based on node properties
for node in tree.traverse():
    nstyle = NodeStyle()

    if node.is_leaf():
        # Leaf node style
        nstyle["size"] = 8
        nstyle["fgcolor"] = "darkgreen"
        nstyle["shape"] = "circle"
    else:
        # Internal node style based on support
        if node.support > 0.9:
            nstyle["size"] = 6
            nstyle["fgcolor"] = "red"
            nstyle["shape"] = "sphere"
        else:
            nstyle["size"] = 4
            nstyle["fgcolor"] = "gray"
            nstyle["shape"] = "circle"

    # Style branches by length
    if node.dist > 1.0:
        nstyle["hz_line_width"] = 3
        nstyle["hz_line_color"] = "blue"
    else:
        nstyle["hz_line_width"] = 1
        nstyle["hz_line_color"] = "black"

    node.set_style(nstyle)

tree.render("conditional_styled_tree.pdf")
```

### Hiding Nodes

```python
from ete3 import Tree, NodeStyle

tree = Tree("tree.nw")

# Hide specific nodes
for node in tree.traverse():
    if node.support < 0.5:  # Hide low support nodes
        nstyle = NodeStyle()
        nstyle["draw_descendants"] = False  # Don't draw this node's subtree
        nstyle["size"] = 0                   # Make node invisible
        node.set_style(nstyle)

tree.render("filtered_tree.pdf")
```

---

## Faces

Faces are graphical elements attached to nodes. They appear at specific positions around nodes.

### Face Positions

- `"branch-right"`: Right side of branch (after node)
- `"branch-top"`: Above branch
- `"branch-bottom"`: Below branch
- `"aligned"`: Aligned column at tree edge (for leaves)

### TextFace

```python
from ete3 import Tree, TreeStyle, TextFace

tree = Tree("tree.nw")

def layout(node):
    if node.is_leaf():
        # Add species name
        name_face = TextFace(node.name, fsize=12, fgcolor="black")
        node.add_face(name_face, column=0, position="branch-right")

        # Add additional text
        info_face = TextFace(f"Length: {node.dist:.3f}", fsize=8, fgcolor="gray")
        node.add_face(info_face, column=1, position="branch-right")
    else:
        # Add support value
        if node.support:
            support_face = TextFace(f"{node.support:.2f}", fsize=8, fgcolor="red")
            node.add_face(support_face, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False  # We're adding custom names

tree.render("tree_textfaces.pdf", tree_style=ts)
```

### AttrFace

Display node attributes directly:

```python
from ete3 import Tree, TreeStyle, AttrFace

tree = Tree("tree.nw")

# Add custom attributes
for leaf in tree:
    leaf.add_feature("habitat", "aquatic" if "fish" in leaf.name else "terrestrial")
    leaf.add_feature("temperature", 20)

def layout(node):
    if node.is_leaf():
        # Display attribute directly
        habitat_face = AttrFace("habitat", fsize=10)
        node.add_face(habitat_face, column=0, position="aligned")

        temp_face = AttrFace("temperature", fsize=10)
        node.add_face(temp_face, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout

tree.render("tree_attrfaces.pdf", tree_style=ts)
```

### CircleFace

```python
from ete3 import Tree, TreeStyle, CircleFace, TextFace

tree = Tree("tree.nw")

# Annotate with habitat
for leaf in tree:
    leaf.add_feature("habitat", "marine" if "fish" in leaf.name else "land")

def layout(node):
    if node.is_leaf():
        # Colored circle based on habitat
        color = "blue" if node.habitat == "marine" else "green"
        circle = CircleFace(radius=5, color=color, style="circle")
        node.add_face(circle, column=0, position="aligned")

        # Label
        name = TextFace(node.name, fsize=10)
        node.add_face(name, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("tree_circles.pdf", tree_style=ts)
```

### ImgFace

Add images to nodes:

```python
from ete3 import Tree, TreeStyle, ImgFace, TextFace

tree = Tree("tree.nw")

def layout(node):
    if node.is_leaf():
        # Add species image
        img_path = f"images/{node.name}.png"  # Path to image
        try:
            img_face = ImgFace(img_path, width=50, height=50)
            node.add_face(img_face, column=0, position="aligned")
        except:
            pass  # Skip if image doesn't exist

        # Add name
        name_face = TextFace(node.name, fsize=10)
        node.add_face(name_face, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("tree_images.pdf", tree_style=ts)
```

### BarChartFace

```python
from ete3 import Tree, TreeStyle, BarChartFace, TextFace

tree = Tree("tree.nw")

# Add data for bar charts
for leaf in tree:
    leaf.add_feature("values", [1.2, 2.3, 0.5, 1.8])  # Multiple values

def layout(node):
    if node.is_leaf():
        # Add bar chart
        chart = BarChartFace(
            node.values,
            width=100,
            height=40,
            colors=["red", "blue", "green", "orange"],
            labels=["A", "B", "C", "D"]
        )
        node.add_face(chart, column=0, position="aligned")

        # Add name
        name = TextFace(node.name, fsize=10)
        node.add_face(name, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("tree_barcharts.pdf", tree_style=ts)
```

### PieChartFace

```python
from ete3 import Tree, TreeStyle, PieChartFace, TextFace

tree = Tree("tree.nw")

# Add data
for leaf in tree:
    leaf.add_feature("proportions", [25, 35, 40])  # Percentages

def layout(node):
    if node.is_leaf():
        # Add pie chart
        pie = PieChartFace(
            node.proportions,
            width=30,
            height=30,
            colors=["red", "blue", "green"]
        )
        node.add_face(pie, column=0, position="aligned")

        name = TextFace(node.name, fsize=10)
        node.add_face(name, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("tree_piecharts.pdf", tree_style=ts)
```

### SequenceFace (for alignments)

```python
from ete3 import PhyloTree, TreeStyle, SeqMotifFace

tree = PhyloTree("tree.nw")
tree.link_to_alignment("alignment.fasta")

def layout(node):
    if node.is_leaf():
        # Display sequence
        seq_face = SeqMotifFace(node.sequence, seq_format="seq")
        node.add_face(seq_face, column=0, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = True

tree.render("tree_alignment.pdf", tree_style=ts)
```

---

## Layout Functions

Layout functions are Python functions that modify node appearance during rendering.

### Basic Layout Function

```python
from ete3 import Tree, TreeStyle, TextFace

tree = Tree("tree.nw")

def my_layout(node):
    """Called for every node before rendering"""

    if node.is_leaf():
        # Add text to leaves
        name_face = TextFace(node.name.upper(), fsize=12, fgcolor="blue")
        node.add_face(name_face, column=0, position="branch-right")
    else:
        # Add support to internal nodes
        if node.support:
            support_face = TextFace(f"BS: {node.support:.0f}", fsize=8)
            node.add_face(support_face, column=0, position="branch-top")

# Apply layout function
ts = TreeStyle()
ts.layout_fn = my_layout
ts.show_leaf_name = False

tree.render("tree_custom_layout.pdf", tree_style=ts)
```

### Dynamic Styling in Layout

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

def layout(node):
    # Modify node style dynamically
    nstyle = NodeStyle()

    # Color by clade
    if "clade_A" in [l.name for l in node.get_leaves()]:
        nstyle["bgcolor"] = "lightblue"
    elif "clade_B" in [l.name for l in node.get_leaves()]:
        nstyle["bgcolor"] = "lightgreen"

    node.set_style(nstyle)

    # Add faces based on features
    if hasattr(node, "annotation"):
        text = TextFace(node.annotation, fsize=8)
        node.add_face(text, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout

tree.render("tree_dynamic.pdf", tree_style=ts)
```

### Multiple Column Layout

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace

tree = Tree("tree.nw")

# Add features
for leaf in tree:
    leaf.add_feature("habitat", "aquatic")
    leaf.add_feature("temp", 20)
    leaf.add_feature("depth", 100)

def layout(node):
    if node.is_leaf():
        # Column 0: Name
        name = TextFace(node.name, fsize=10)
        node.add_face(name, column=0, position="aligned")

        # Column 1: Habitat indicator
        color = "blue" if node.habitat == "aquatic" else "brown"
        circle = CircleFace(radius=5, color=color)
        node.add_face(circle, column=1, position="aligned")

        # Column 2: Temperature
        temp = TextFace(f"{node.temp}°C", fsize=8)
        node.add_face(temp, column=2, position="aligned")

        # Column 3: Depth
        depth = TextFace(f"{node.depth}m", fsize=8)
        node.add_face(depth, column=3, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("tree_columns.pdf", tree_style=ts)
```

---

## Advanced Visualization

### Highlighting Clades

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

# Define clades to highlight
clade_members = {
    "Clade_A": ["species1", "species2", "species3"],
    "Clade_B": ["species4", "species5"]
}

def layout(node):
    # Check if node is ancestor of specific clade
    node_leaves = set([l.name for l in node.get_leaves()])

    for clade_name, members in clade_members.items():
        if set(members).issubset(node_leaves):
            # This node is ancestor of the clade
            nstyle = NodeStyle()
            nstyle["bgcolor"] = "yellow"
            nstyle["size"] = 0

            # Add label
            if set(members) == node_leaves:  # Exact match
                label = TextFace(clade_name, fsize=14, bold=True, fgcolor="red")
                node.add_face(label, column=0, position="branch-top")

            node.set_style(nstyle)
            break

ts = TreeStyle()
ts.layout_fn = layout

tree.render("tree_highlighted_clades.pdf", tree_style=ts)
```

### Collapsing Clades

```python
from ete3 import Tree, TreeStyle, TextFace, NodeStyle

tree = Tree("tree.nw")

# Define which clades to collapse
clades_to_collapse = ["clade1_species1", "clade1_species2"]

def layout(node):
    if not node.is_leaf():
        node_leaves = [l.name for l in node.get_leaves()]

        # Check if this is a clade we want to collapse
        if all(l in clades_to_collapse for l in node_leaves):
            # Collapse by hiding descendants
            nstyle = NodeStyle()
            nstyle["draw_descendants"] = False
            nstyle["size"] = 20
            nstyle["fgcolor"] = "steelblue"
            nstyle["shape"] = "sphere"
            node.set_style(nstyle)

            # Add label showing what's collapsed
            label = TextFace(f"[{len(node_leaves)} species]", fsize=10)
            node.add_face(label, column=0, position="branch-right")

ts = TreeStyle()
ts.layout_fn = layout

tree.render("tree_collapsed.pdf", tree_style=ts)
```

### Heat Map Visualization

```python
from ete3 import Tree, TreeStyle, RectFace, TextFace
import numpy as np

tree = Tree("tree.nw")

# Generate random data for heatmap
for leaf in tree:
    leaf.add_feature("data", np.random.rand(10))  # 10 data points

def layout(node):
    if node.is_leaf():
        # Add name
        name = TextFace(node.name, fsize=8)
        node.add_face(name, column=0, position="aligned")

        # Add heatmap cells
        for i, value in enumerate(node.data):
            # Color based on value
            intensity = int(255 * value)
            color = f"#{255-intensity:02x}{intensity:02x}00"  # Green-red gradient

            rect = RectFace(width=20, height=15, fgcolor=color, bgcolor=color)
            node.add_face(rect, column=i+1, position="aligned")

# Add column headers
ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

# Add header
for i in range(10):
    header = TextFace(f"C{i+1}", fsize=8, fgcolor="gray")
    ts.aligned_header.add_face(header, column=i+1)

tree.render("tree_heatmap.pdf", tree_style=ts)
```

### Phylogenetic Events Visualization

```python
from ete3 import PhyloTree, TreeStyle, TextFace, NodeStyle

tree = PhyloTree("gene_tree.nw")
tree.set_species_naming_function(lambda x: x.split("_")[0])
tree.get_descendant_evol_events()

def layout(node):
    # Style based on evolutionary event
    if hasattr(node, "evoltype"):
        nstyle = NodeStyle()

        if node.evoltype == "D":  # Duplication
            nstyle["fgcolor"] = "red"
            nstyle["size"] = 10
            nstyle["shape"] = "square"

            label = TextFace("DUP", fsize=8, fgcolor="red", bold=True)
            node.add_face(label, column=0, position="branch-top")

        elif node.evoltype == "S":  # Speciation
            nstyle["fgcolor"] = "blue"
            nstyle["size"] = 6
            nstyle["shape"] = "circle"

        node.set_style(nstyle)

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = True

tree.render("gene_tree_events.pdf", tree_style=ts)
```

### Custom Tree with Legend

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace, NodeStyle

tree = Tree("tree.nw")

# Categorize species
for leaf in tree:
    if "fish" in leaf.name.lower():
        leaf.add_feature("category", "fish")
    elif "bird" in leaf.name.lower():
        leaf.add_feature("category", "bird")
    else:
        leaf.add_feature("category", "mammal")

category_colors = {
    "fish": "blue",
    "bird": "green",
    "mammal": "red"
}

def layout(node):
    if node.is_leaf():
        # Color by category
        nstyle = NodeStyle()
        nstyle["fgcolor"] = category_colors[node.category]
        nstyle["size"] = 10
        node.set_style(nstyle)

ts = TreeStyle()
ts.layout_fn = layout

# Add legend
ts.legend.add_face(TextFace("Legend:", fsize=12, bold=True), column=0)
for category, color in category_colors.items():
    circle = CircleFace(radius=5, color=color)
    ts.legend.add_face(circle, column=0)
    label = TextFace(f" {category.capitalize()}", fsize=10)
    ts.legend.add_face(label, column=1)

ts.legend_position = 1

tree.render("tree_with_legend.pdf", tree_style=ts)
```

---

## Best Practices

1. **Use layout functions** for complex visualizations - they're called during rendering
2. **Set `show_leaf_name = False`** when using custom name faces
3. **Use aligned position** for columnar data at leaf level
4. **Choose appropriate units**: pixels for screen, mm/inches for print
5. **Use vector formats (PDF/SVG)** for publications
6. **Precompute styling** when possible - layout functions should be fast
7. **Test interactively** with `show()` before rendering to file
8. **Use NodeStyle for permanent** changes, layout functions for rendering-time changes
9. **Align faces in columns** for clean, organized appearance
10. **Add legends** to explain colors and symbols used

---

## Reference: Workflows

# ETE Toolkit Common Workflows

This document provides complete workflows for common tasks using the ETE Toolkit.

## Table of Contents
1. [Basic Tree Operations](#basic-tree-operations)
2. [Phylogenetic Analysis](#phylogenetic-analysis)
3. [Tree Comparison](#tree-comparison)
4. [Taxonomy Integration](#taxonomy-integration)
5. [Clustering Analysis](#clustering-analysis)
6. [Tree Visualization](#tree-visualization)

---

## Basic Tree Operations

### Loading and Exploring a Tree

```python
from ete3 import Tree

# Load tree from file
tree = Tree("my_tree.nw", format=1)

# Display ASCII representation
print(tree.get_ascii(show_internal=True))

# Get basic statistics
print(f"Number of leaves: {len(tree)}")
print(f"Total nodes: {len(list(tree.traverse()))}")
print(f"Tree depth: {tree.get_farthest_leaf()[1]}")

# List all leaf names
for leaf in tree:
    print(leaf.name)
```

### Extracting and Saving Subtrees

```python
from ete3 import Tree

tree = Tree("full_tree.nw")

# Get subtree rooted at specific node
node = tree.search_nodes(name="MyNode")[0]
subtree = node.copy()

# Save subtree to file
subtree.write(outfile="subtree.nw", format=1)

# Extract monophyletic clade
species_of_interest = ["species1", "species2", "species3"]
ancestor = tree.get_common_ancestor(species_of_interest)
clade = ancestor.copy()
clade.write(outfile="clade.nw")
```

### Pruning Trees to Specific Taxa

```python
from ete3 import Tree

tree = Tree("large_tree.nw")

# Keep only taxa of interest
taxa_to_keep = ["taxon1", "taxon2", "taxon3", "taxon4"]
tree.prune(taxa_to_keep, preserve_branch_length=True)

# Save pruned tree
tree.write(outfile="pruned_tree.nw")
```

### Rerooting Trees

```python
from ete3 import Tree

tree = Tree("unrooted_tree.nw")

# Method 1: Root by outgroup
outgroup = tree & "Outgroup_species"
tree.set_outgroup(outgroup)

# Method 2: Midpoint rooting
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Save rooted tree
tree.write(outfile="rooted_tree.nw")
```

### Annotating Nodes with Custom Data

```python
from ete3 import Tree

tree = Tree("tree.nw")

# Add features to nodes based on metadata
metadata = {
    "species1": {"habitat": "marine", "temperature": 20},
    "species2": {"habitat": "freshwater", "temperature": 15},
}

for leaf in tree:
    if leaf.name in metadata:
        leaf.add_features(**metadata[leaf.name])

# Query annotated features
for leaf in tree:
    if hasattr(leaf, "habitat"):
        print(f"{leaf.name}: {leaf.habitat}, {leaf.temperature}°C")

# Save with custom features (NHX format)
tree.write(outfile="annotated_tree.nhx", features=["habitat", "temperature"])
```

### Modifying Tree Topology

```python
from ete3 import Tree

tree = Tree("tree.nw")

# Remove a clade
node_to_remove = tree & "unwanted_clade"
node_to_remove.detach()

# Collapse a node (delete but keep children)
node_to_collapse = tree & "low_support_node"
node_to_collapse.delete()

# Add a new species to existing clade
target_clade = tree & "target_node"
new_leaf = target_clade.add_child(name="new_species", dist=0.5)

# Resolve polytomies
tree.resolve_polytomy(recursive=True)

# Save modified tree
tree.write(outfile="modified_tree.nw")
```

---

## Phylogenetic Analysis

### Complete Gene Tree Analysis with Alignment

```python
from ete3 import PhyloTree

# Load gene tree and link alignment
tree = PhyloTree("gene_tree.nw", format=1)
tree.link_to_alignment("alignment.fasta", alg_format="fasta")

# Set species naming function (e.g., gene_species format)
def extract_species(node_name):
    return node_name.split("_")[0]

tree.set_species_naming_function(extract_species)

# Access sequences
for leaf in tree:
    print(f"{leaf.name} ({leaf.species})")
    print(f"Sequence: {leaf.sequence[:50]}...")
```

### Detecting Duplication and Speciation Events

```python
from ete3 import PhyloTree, Tree

# Load gene tree
gene_tree = PhyloTree("gene_tree.nw")

# Set species naming
gene_tree.set_species_naming_function(lambda x: x.split("_")[0])

# Option 1: Species Overlap algorithm (no species tree needed)
events = gene_tree.get_descendant_evol_events()

# Option 2: Tree reconciliation (requires species tree)
species_tree = Tree("species_tree.nw")
events = gene_tree.get_descendant_evol_events(species_tree=species_tree)

# Analyze events
duplications = 0
speciations = 0

for node in gene_tree.traverse():
    if hasattr(node, "evoltype"):
        if node.evoltype == "D":
            duplications += 1
            print(f"Duplication at node {node.name}")
        elif node.evoltype == "S":
            speciations += 1

print(f"\nTotal duplications: {duplications}")
print(f"Total speciations: {speciations}")
```

### Extracting Orthologs and Paralogs

```python
from ete3 import PhyloTree

gene_tree = PhyloTree("gene_tree.nw")
gene_tree.set_species_naming_function(lambda x: x.split("_")[0])

# Detect evolutionary events
events = gene_tree.get_descendant_evol_events()

# Find all orthologs to a query gene
query_gene = gene_tree & "species1_gene1"

orthologs = []
paralogs = []

for event in events:
    if query_gene in event.in_seqs:
        if event.etype == "S":  # Speciation
            orthologs.extend([s for s in event.out_seqs if s != query_gene])
        elif event.etype == "D":  # Duplication
            paralogs.extend([s for s in event.out_seqs if s != query_gene])

print(f"Orthologs of {query_gene.name}:")
for ortholog in set(orthologs):
    print(f"  {ortholog.name}")

print(f"\nParalogs of {query_gene.name}:")
for paralog in set(paralogs):
    print(f"  {paralog.name}")
```

### Splitting Gene Families by Duplication Events

```python
from ete3 import PhyloTree

gene_tree = PhyloTree("gene_family.nw")
gene_tree.set_species_naming_function(lambda x: x.split("_")[0])
gene_tree.get_descendant_evol_events()

# Split into individual gene families
subfamilies = gene_tree.split_by_dups()

print(f"Gene family split into {len(subfamilies)} subfamilies")

for i, subtree in enumerate(subfamilies):
    subtree.write(outfile=f"subfamily_{i}.nw")
    species = set([leaf.species for leaf in subtree])
    print(f"Subfamily {i}: {len(subtree)} genes from {len(species)} species")
```

### Collapsing Lineage-Specific Expansions

```python
from ete3 import PhyloTree

gene_tree = PhyloTree("expanded_tree.nw")
gene_tree.set_species_naming_function(lambda x: x.split("_")[0])

# Collapse lineage-specific duplications
gene_tree.collapse_lineage_specific_expansions()

print("After collapsing expansions:")
print(gene_tree.get_ascii())

gene_tree.write(outfile="collapsed_tree.nw")
```

### Testing Monophyly

```python
from ete3 import Tree

tree = Tree("tree.nw")

# Test if a group is monophyletic
target_species = ["species1", "species2", "species3"]
is_mono, clade_type, base_node = tree.check_monophyly(
    values=target_species,
    target_attr="name"
)

if is_mono:
    print(f"Group is monophyletic")
    print(f"MRCA: {base_node.name}")
elif clade_type == "paraphyletic":
    print(f"Group is paraphyletic")
elif clade_type == "polyphyletic":
    print(f"Group is polyphyletic")

# Get all monophyletic clades of a specific type
# Annotate leaves first
for leaf in tree:
    if leaf.name.startswith("species"):
        leaf.add_feature("type", "typeA")
    else:
        leaf.add_feature("type", "typeB")

mono_clades = tree.get_monophyletic(values=["typeA"], target_attr="type")
print(f"Found {len(mono_clades)} monophyletic clades of typeA")
```

---

## Tree Comparison

### Computing Robinson-Foulds Distance

```python
from ete3 import Tree

tree1 = Tree("tree1.nw")
tree2 = Tree("tree2.nw")

# Compute RF distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = tree1.robinson_foulds(tree2)

print(f"Robinson-Foulds distance: {rf}")
print(f"Maximum RF distance: {max_rf}")
print(f"Normalized RF: {rf/max_rf:.3f}")
print(f"Common leaves: {len(common_leaves)}")

# Find unique partitions
unique_in_t1 = parts_t1 - parts_t2
unique_in_t2 = parts_t2 - parts_t1

print(f"\nPartitions unique to tree1: {len(unique_in_t1)}")
print(f"Partitions unique to tree2: {len(unique_in_t2)}")
```

### Comparing Multiple Trees

```python
from ete3 import Tree
import numpy as np

# Load multiple trees
tree_files = ["tree1.nw", "tree2.nw", "tree3.nw", "tree4.nw"]
trees = [Tree(f) for f in tree_files]

# Create distance matrix
n = len(trees)
dist_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(i+1, n):
        rf, max_rf, _, _, _ = trees[i].robinson_foulds(trees[j])
        norm_rf = rf / max_rf if max_rf > 0 else 0
        dist_matrix[i, j] = norm_rf
        dist_matrix[j, i] = norm_rf

print("Normalized RF distance matrix:")
print(dist_matrix)

# Find most similar pair
min_dist = float('inf')
best_pair = None

for i in range(n):
    for j in range(i+1, n):
        if dist_matrix[i, j] < min_dist:
            min_dist = dist_matrix[i, j]
            best_pair = (i, j)

print(f"\nMost similar trees: {tree_files[best_pair[0]]} and {tree_files[best_pair[1]]}")
print(f"Distance: {min_dist:.3f}")
```

### Finding Consensus Topology

```python
from ete3 import Tree

# Load multiple bootstrap trees
bootstrap_trees = [Tree(f"bootstrap_{i}.nw") for i in range(100)]

# Get reference tree (first tree)
ref_tree = bootstrap_trees[0].copy()

# Count bipartitions
bipartition_counts = {}

for tree in bootstrap_trees:
    rf, max_rf, common, parts_ref, parts_tree = ref_tree.robinson_foulds(tree)
    for partition in parts_tree:
        bipartition_counts[partition] = bipartition_counts.get(partition, 0) + 1

# Filter by support threshold
threshold = 70  # 70% support
supported_bipartitions = {
    k: v for k, v in bipartition_counts.items()
    if (v / len(bootstrap_trees)) * 100 >= threshold
}

print(f"Bipartitions with >{threshold}% support: {len(supported_bipartitions)}")
```

---

## Taxonomy Integration

### Building Species Trees from NCBI Taxonomy

```python
from ete3 import NCBITaxa

ncbi = NCBITaxa()

# Define species of interest
species = ["Homo sapiens", "Pan troglodytes", "Gorilla gorilla",
           "Mus musculus", "Rattus norvegicus"]

# Get taxids
name2taxid = ncbi.get_name_translator(species)
taxids = [name2taxid[sp][0] for sp in species]

# Build tree
tree = ncbi.get_topology(taxids)

# Annotate with taxonomy info
for node in tree.traverse():
    if hasattr(node, "sci_name"):
        print(f"{node.sci_name} - Rank: {node.rank} - TaxID: {node.taxid}")

# Save tree
tree.write(outfile="species_tree.nw")
```

### Annotating Existing Tree with NCBI Taxonomy

```python
from ete3 import Tree, NCBITaxa

tree = Tree("species_tree.nw")
ncbi = NCBITaxa()

# Map leaf names to species names (adjust as needed)
leaf_to_species = {
    "Hsap_gene1": "Homo sapiens",
    "Ptro_gene1": "Pan troglodytes",
    "Mmur_gene1": "Microcebus murinus",
}

# Get taxids
all_species = list(set(leaf_to_species.values()))
name2taxid = ncbi.get_name_translator(all_species)

# Annotate leaves
for leaf in tree:
    if leaf.name in leaf_to_species:
        species_name = leaf_to_species[leaf.name]
        taxid = name2taxid[species_name][0]

        # Add taxonomy info
        leaf.add_feature("species", species_name)
        leaf.add_feature("taxid", taxid)

        # Get full lineage
        lineage = ncbi.get_lineage(taxid)
        names = ncbi.get_taxid_translator(lineage)
        leaf.add_feature("lineage", [names[t] for t in lineage])

        print(f"{leaf.name}: {species_name} (taxid: {taxid})")
```

### Querying NCBI Taxonomy

```python
from ete3 import NCBITaxa

ncbi = NCBITaxa()

# Get all primates
primates_taxid = ncbi.get_name_translator(["Primates"])["Primates"][0]
all_primates = ncbi.get_descendant_taxa(primates_taxid, collapse_subspecies=True)

print(f"Total primate species: {len(all_primates)}")

# Get names for subset
taxid2name = ncbi.get_taxid_translator(all_primates[:10])
for taxid, name in taxid2name.items():
    rank = ncbi.get_rank([taxid])[taxid]
    print(f"{name} ({rank})")

# Get lineage for specific species
human_taxid = 9606
lineage = ncbi.get_lineage(human_taxid)
ranks = ncbi.get_rank(lineage)
names = ncbi.get_taxid_translator(lineage)

print("\nHuman lineage:")
for taxid in lineage:
    print(f"{ranks[taxid]:15s} {names[taxid]}")
```

---

## Clustering Analysis

### Analyzing Hierarchical Clustering Results

```python
from ete3 import ClusterTree

# Load clustering tree with data matrix
matrix = """#Names\tSample1\tSample2\tSample3\tSample4
Gene1\t1.5\t2.3\t0.8\t1.2
Gene2\t0.9\t1.1\t1.8\t2.1
Gene3\t2.1\t2.5\t0.5\t0.9
Gene4\t0.7\t0.9\t2.2\t2.4"""

tree = ClusterTree("((Gene1,Gene2),(Gene3,Gene4));", text_array=matrix)

# Calculate cluster quality metrics
for node in tree.traverse():
    if not node.is_leaf():
        # Silhouette coefficient
        silhouette = node.get_silhouette()

        # Dunn index
        dunn = node.get_dunn()

        # Distances
        inter = node.intercluster_dist
        intra = node.intracluster_dist

        print(f"Node: {node.name}")
        print(f"  Silhouette: {silhouette:.3f}")
        print(f"  Dunn index: {dunn:.3f}")
        print(f"  Intercluster distance: {inter:.3f}")
        print(f"  Intracluster distance: {intra:.3f}")
```

### Validating Clusters

```python
from ete3 import ClusterTree

matrix = """#Names\tCol1\tCol2\tCol3
ItemA\t1.2\t0.5\t0.8
ItemB\t1.3\t0.6\t0.9
ItemC\t0.1\t2.5\t2.3
ItemD\t0.2\t2.6\t2.4"""

tree = ClusterTree("((ItemA,ItemB),(ItemC,ItemD));", text_array=matrix)

# Test different distance metrics
metrics = ["euclidean", "pearson", "spearman"]

for metric in metrics:
    print(f"\nUsing {metric} distance:")

    for node in tree.traverse():
        if not node.is_leaf():
            silhouette = node.get_silhouette(distance=metric)

            # Positive silhouette = good clustering
            # Negative silhouette = poor clustering
            quality = "good" if silhouette > 0 else "poor"

            print(f"  Cluster {node.name}: {silhouette:.3f} ({quality})")
```

---

## Tree Visualization

### Basic Tree Rendering

```python
from ete3 import Tree, TreeStyle

tree = Tree("tree.nw")

# Create tree style
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True
ts.scale = 50  # pixels per branch length unit

# Render to file
tree.render("tree_output.pdf", tree_style=ts)
tree.render("tree_output.png", tree_style=ts, w=800, h=600, units="px")
tree.render("tree_output.svg", tree_style=ts)
```

### Customizing Node Appearance

```python
from ete3 import Tree, TreeStyle, NodeStyle

tree = Tree("tree.nw")

# Define node styles
for node in tree.traverse():
    nstyle = NodeStyle()

    if node.is_leaf():
        nstyle["fgcolor"] = "blue"
        nstyle["size"] = 10
    else:
        nstyle["fgcolor"] = "red"
        nstyle["size"] = 5

    if node.support > 0.9:
        nstyle["shape"] = "sphere"
    else:
        nstyle["shape"] = "circle"

    node.set_style(nstyle)

# Render
ts = TreeStyle()
tree.render("styled_tree.pdf", tree_style=ts)
```

### Adding Faces to Nodes

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace, AttrFace

tree = Tree("tree.nw")

# Add features to nodes
for leaf in tree:
    leaf.add_feature("habitat", "marine" if "fish" in leaf.name else "terrestrial")
    leaf.add_feature("temp", 20)

# Layout function to add faces
def layout(node):
    if node.is_leaf():
        # Add text face
        name_face = TextFace(node.name, fsize=10)
        node.add_face(name_face, column=0, position="branch-right")

        # Add colored circle based on habitat
        color = "blue" if node.habitat == "marine" else "green"
        circle_face = CircleFace(radius=5, color=color)
        node.add_face(circle_face, column=1, position="branch-right")

        # Add attribute face
        temp_face = AttrFace("temp", fsize=8)
        node.add_face(temp_face, column=2, position="branch-right")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False  # We're adding custom names

tree.render("tree_with_faces.pdf", tree_style=ts)
```

### Circular Tree Layout

```python
from ete3 import Tree, TreeStyle

tree = Tree("tree.nw")

ts = TreeStyle()
ts.mode = "c"  # Circular mode
ts.arc_start = 0  # Degrees
ts.arc_span = 360  # Full circle
ts.show_leaf_name = True

tree.render("circular_tree.pdf", tree_style=ts)
```

### Interactive Exploration

```python
from ete3 import Tree

tree = Tree("tree.nw")

# Launch GUI (allows zooming, searching, modifying)
# Changes persist after closing
tree.show()

# Can save changes made in GUI
tree.write(outfile="modified_tree.nw")
```

---

## Advanced Workflows

### Complete Phylogenomic Pipeline

```python
from ete3 import PhyloTree, NCBITaxa, TreeStyle

# 1. Load gene tree
gene_tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# 2. Set species naming
gene_tree.set_species_naming_function(lambda x: x.split("_")[0])

# 3. Detect evolutionary events
gene_tree.get_descendant_evol_events()

# 4. Annotate with NCBI taxonomy
ncbi = NCBITaxa()
species_set = set([leaf.species for leaf in gene_tree])
name2taxid = ncbi.get_name_translator(list(species_set))

for leaf in gene_tree:
    if leaf.species in name2taxid:
        taxid = name2taxid[leaf.species][0]
        lineage = ncbi.get_lineage(taxid)
        names = ncbi.get_taxid_translator(lineage)
        leaf.add_feature("lineage", [names[t] for t in lineage])

# 5. Identify and save ortholog groups
ortho_groups = gene_tree.get_speciation_trees()

for i, ortho_tree in enumerate(ortho_groups):
    ortho_tree.write(outfile=f"ortholog_group_{i}.nw")

# 6. Visualize with evolutionary events marked
def layout(node):
    from ete3 import TextFace
    if hasattr(node, "evoltype"):
        if node.evoltype == "D":
            dup_face = TextFace("DUPLICATION", fsize=8, fgcolor="red")
            node.add_face(dup_face, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = True
gene_tree.render("annotated_gene_tree.pdf", tree_style=ts)

print(f"Pipeline complete. Found {len(ortho_groups)} ortholog groups.")
```

### Batch Processing Multiple Trees

```python
from ete3 import Tree
import os

input_dir = "input_trees"
output_dir = "processed_trees"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".nw"):
        # Load tree
        tree = Tree(os.path.join(input_dir, filename))

        # Process: root, prune, annotate
        midpoint = tree.get_midpoint_outgroup()
        tree.set_outgroup(midpoint)

        # Filter by branch length
        to_remove = []
        for node in tree.traverse():
            if node.dist < 0.001 and not node.is_root():
                to_remove.append(node)

        for node in to_remove:
            node.delete()

        # Save processed tree
        output_file = os.path.join(output_dir, f"processed_{filename}")
        tree.write(outfile=output_file)

        print(f"Processed {filename}")
```
