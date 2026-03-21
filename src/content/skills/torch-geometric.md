---
title: "Torch Geometric"
description: "Graph Neural Networks (PyG). Node/graph classification, link prediction, GCN, GAT, GraphSAGE, heterogeneous graphs, molecular property prediction, for geometric deep learning."
category: "research"
source: "community"
author: "Community"
tags: ["torch", "geometric"]
date: 2026-03-20
---

# PyTorch Geometric (PyG)

## Overview

PyTorch Geometric is a library built on PyTorch for developing and training Graph Neural Networks (GNNs). Apply this skill for deep learning on graphs and irregular structures, including mini-batch processing, multi-GPU training, and geometric deep learning applications.

## When to Use This Skill

This skill should be used when working with:
- **Graph-based machine learning**: Node classification, graph classification, link prediction
- **Molecular property prediction**: Drug discovery, chemical property prediction
- **Social network analysis**: Community detection, influence prediction
- **Citation networks**: Paper classification, recommendation systems
- **3D geometric data**: Point clouds, meshes, molecular structures
- **Heterogeneous graphs**: Multi-type nodes and edges (e.g., knowledge graphs)
- **Large-scale graph learning**: Neighbor sampling, distributed training

## Quick Start

### Installation

```bash
uv pip install torch_geometric
```

For additional dependencies (sparse operations, clustering):
```bash
uv pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-${TORCH}+${CUDA}.html
```

### Basic Graph Creation

```python
import torch
from torch_geometric.data import Data

# Create a simple graph with 3 nodes
edge_index = torch.tensor([[0, 1, 1, 2],  # source nodes
                           [1, 0, 2, 1]], dtype=torch.long)  # target nodes
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)  # node features

data = Data(x=x, edge_index=edge_index)
print(f"Nodes: {data.num_nodes}, Edges: {data.num_edges}")
```

### Loading a Benchmark Dataset

```python
from torch_geometric.datasets import Planetoid

# Load Cora citation network
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]  # Get the first (and only) graph

print(f"Dataset: {dataset}")
print(f"Nodes: {data.num_nodes}, Edges: {data.num_edges}")
print(f"Features: {data.num_node_features}, Classes: {dataset.num_classes}")
```

## Core Concepts

### Data Structure

PyG represents graphs using the `torch_geometric.data.Data` class with these key attributes:

- **`data.x`**: Node feature matrix `[num_nodes, num_node_features]`
- **`data.edge_index`**: Graph connectivity in COO format `[2, num_edges]`
- **`data.edge_attr`**: Edge feature matrix `[num_edges, num_edge_features]` (optional)
- **`data.y`**: Target labels for nodes or graphs
- **`data.pos`**: Node spatial positions `[num_nodes, num_dimensions]` (optional)
- **Custom attributes**: Can add any attribute (e.g., `data.train_mask`, `data.batch`)

**Important**: These attributes are not mandatory—extend Data objects with custom attributes as needed.

### Edge Index Format

Edges are stored in COO (coordinate) format as a `[2, num_edges]` tensor:
- First row: source node indices
- Second row: target node indices

```python
# Edge list: (0→1), (1→0), (1→2), (2→1)
edge_index = torch.tensor([[0, 1, 1, 2],
                           [1, 0, 2, 1]], dtype=torch.long)
```

### Mini-Batch Processing

PyG handles batching by creating block-diagonal adjacency matrices, concatenating multiple graphs into one large disconnected graph:

- Adjacency matrices are stacked diagonally
- Node features are concatenated along the node dimension
- A `batch` vector maps each node to its source graph
- No padding needed—computationally efficient

```python
from torch_geometric.loader import DataLoader

loader = DataLoader(dataset, batch_size=32, shuffle=True)
for batch in loader:
    print(f"Batch size: {batch.num_graphs}")
    print(f"Total nodes: {batch.num_nodes}")
    # batch.batch maps nodes to graphs
```

## Building Graph Neural Networks

### Message Passing Paradigm

GNNs in PyG follow a neighborhood aggregation scheme:
1. Transform node features
2. Propagate messages along edges
3. Aggregate messages from neighbors
4. Update node representations

### Using Pre-Built Layers

PyG provides 40+ convolutional layers. Common ones include:

**GCNConv** (Graph Convolutional Network):
```python
from torch_geometric.nn import GCNConv
import torch.nn.functional as F

class GCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GATConv** (Graph Attention Network):
```python
from torch_geometric.nn import GATConv

class GAT(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GATConv(num_features, 8, heads=8, dropout=0.6)
        self.conv2 = GATConv(8 * 8, num_classes, heads=1, concat=False, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GraphSAGE**:
```python
from torch_geometric.nn import SAGEConv

class GraphSAGE(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = SAGEConv(num_features, 64)
        self.conv2 = SAGEConv(64, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

### Custom Message Passing Layers

For custom layers, inherit from `MessagePassing`:

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class CustomConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')  # "add", "mean", or "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        # Add self-loops to adjacency matrix
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        # Transform node features
        x = self.lin(x)

        # Compute normalization
        row, col = edge_index
        deg = degree(col, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]

        # Propagate messages
        return self.propagate(edge_index, x=x, norm=norm)

    def message(self, x_j, norm):
        # x_j: features of source nodes
        return norm.view(-1, 1) * x_j
```

Key methods:
- **`forward()`**: Main entry point
- **`message()`**: Constructs messages from source to target nodes
- **`aggregate()`**: Aggregates messages (usually don't override—set `aggr` parameter)
- **`update()`**: Updates node embeddings after aggregation

**Variable naming convention**: Appending `_i` or `_j` to tensor names automatically maps them to target or source nodes.

## Working with Datasets

### Loading Built-in Datasets

PyG provides extensive benchmark datasets:

```python
# Citation networks (node classification)
from torch_geometric.datasets import Planetoid
dataset = Planetoid(root='/tmp/Cora', name='Cora')  # or 'CiteSeer', 'PubMed'

# Graph classification
from torch_geometric.datasets import TUDataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')

# Molecular datasets
from torch_geometric.datasets import QM9
dataset = QM9(root='/tmp/QM9')

# Large-scale datasets
from torch_geometric.datasets import Reddit
dataset = Reddit(root='/tmp/Reddit')
```

Check `references/datasets_reference.md` for a comprehensive list.

### Creating Custom Datasets

For datasets that fit in memory, inherit from `InMemoryDataset`:

```python
from torch_geometric.data import InMemoryDataset, Data
import torch

class MyOwnDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return ['my_data.csv']  # Files needed in raw_dir

    @property
    def processed_file_names(self):
        return ['data.pt']  # Files in processed_dir

    def download(self):
        # Download raw data to self.raw_dir
        pass

    def process(self):
        # Read data, create Data objects
        data_list = []

        # Example: Create a simple graph
        edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
        x = torch.randn(2, 16)
        y = torch.tensor([0], dtype=torch.long)

        data = Data(x=x, edge_index=edge_index, y=y)
        data_list.append(data)

        # Apply pre_filter and pre_transform
        if self.pre_filter is not None:
            data_list = [d for d in data_list if self.pre_filter(d)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(d) for d in data_list]

        # Save processed data
        self.save(data_list, self.processed_paths[0])
```

For large datasets that don't fit in memory, inherit from `Dataset` and implement `len()` and `get(idx)`.

### Loading Graphs from CSV

```python
import pandas as pd
import torch
from torch_geometric.data import HeteroData

# Load nodes
nodes_df = pd.read_csv('nodes.csv')
x = torch.tensor(nodes_df[['feat1', 'feat2']].values, dtype=torch.float)

# Load edges
edges_df = pd.read_csv('edges.csv')
edge_index = torch.tensor([edges_df['source'].values,
                           edges_df['target'].values], dtype=torch.long)

data = Data(x=x, edge_index=edge_index)
```

## Training Workflows

### Node Classification (Single Graph)

```python
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid

# Load dataset
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]

# Create model
model = GCN(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# Training
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

# Evaluation
model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print(f'Test Accuracy: {acc:.4f}')
```

### Graph Classification (Multiple Graphs)

```python
from torch_geometric.datasets import TUDataset
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool

class GraphClassifier(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 64)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)

        # Global pooling (aggregate node features to graph-level)
        x = global_mean_pool(x, batch)

        x = self.lin(x)
        return F.log_softmax(x, dim=1)

# Load dataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')
loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = GraphClassifier(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training
model.train()
for epoch in range(100):
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        out = model(batch)
        loss = F.nll_loss(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {total_loss / len(loader):.4f}')
```

### Large-Scale Graphs with Neighbor Sampling

For large graphs, use `NeighborLoader` to sample subgraphs:

```python
from torch_geometric.loader import NeighborLoader

# Create a neighbor sampler
train_loader = NeighborLoader(
    data,
    num_neighbors=[25, 10],  # Sample 25 neighbors for 1st hop, 10 for 2nd hop
    batch_size=128,
    input_nodes=data.train_mask,
)

# Training
model.train()
for batch in train_loader:
    optimizer.zero_grad()
    out = model(batch)
    # Only compute loss on seed nodes (first batch_size nodes)
    loss = F.nll_loss(out[:batch.batch_size], batch.y[:batch.batch_size])
    loss.backward()
    optimizer.step()
```

**Important**:
- Output subgraphs are directed
- Node indices are relabeled (0 to batch.num_nodes - 1)
- Only use seed node predictions for loss computation
- Sampling beyond 2-3 hops is generally not feasible

## Advanced Features

### Heterogeneous Graphs

For graphs with multiple node and edge types, use `HeteroData`:

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# Add node features for different types
data['paper'].x = torch.randn(100, 128)  # 100 papers with 128 features
data['author'].x = torch.randn(200, 64)  # 200 authors with 64 features

# Add edges for different types (source_type, edge_type, target_type)
data['author', 'writes', 'paper'].edge_index = torch.randint(0, 200, (2, 500))
data['paper', 'cites', 'paper'].edge_index = torch.randint(0, 100, (2, 300))

print(data)
```

Convert homogeneous models to heterogeneous:

```python
from torch_geometric.nn import to_hetero

# Define homogeneous model
model = GNN(...)

# Convert to heterogeneous
model = to_hetero(model, data.metadata(), aggr='sum')

# Use as normal
out = model(data.x_dict, data.edge_index_dict)
```

Or use `HeteroConv` for custom edge-type-specific operations:

```python
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv

class HeteroGNN(torch.nn.Module):
    def __init__(self, metadata):
        super().__init__()
        self.conv1 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(-1, 64),
            ('author', 'writes', 'paper'): SAGEConv((-1, -1), 64),
        }, aggr='sum')

        self.conv2 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(64, 32),
            ('author', 'writes', 'paper'): SAGEConv((64, 64), 32),
        }, aggr='sum')

    def forward(self, x_dict, edge_index_dict):
        x_dict = self.conv1(x_dict, edge_index_dict)
        x_dict = {key: F.relu(x) for key, x in x_dict.items()}
        x_dict = self.conv2(x_dict, edge_index_dict)
        return x_dict
```

### Transforms

Apply transforms to modify graph structure or features:

```python
from torch_geometric.transforms import NormalizeFeatures, AddSelfLoops, Compose

# Single transform
transform = NormalizeFeatures()
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)

# Compose multiple transforms
transform = Compose([
    AddSelfLoops(),
    NormalizeFeatures(),
])
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)
```

Common transforms:
- **Structure**: `ToUndirected`, `AddSelfLoops`, `RemoveSelfLoops`, `KNNGraph`, `RadiusGraph`
- **Features**: `NormalizeFeatures`, `NormalizeScale`, `Center`
- **Sampling**: `RandomNodeSplit`, `RandomLinkSplit`
- **Positional Encoding**: `AddLaplacianEigenvectorPE`, `AddRandomWalkPE`

See `references/transforms_reference.md` for the full list.

### Model Explainability

PyG provides explainability tools to understand model predictions:

```python
from torch_geometric.explain import Explainer, GNNExplainer

# Create explainer
explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',  # or 'phenomenon'
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='log_probs',
    ),
)

# Generate explanation for a specific node
node_idx = 10
explanation = explainer(data.x, data.edge_index, index=node_idx)

# Visualize
print(f'Node {node_idx} explanation:')
print(f'Important edges: {explanation.edge_mask.topk(5).indices}')
print(f'Important features: {explanation.node_mask[node_idx].topk(5).indices}')
```

### Pooling Operations

For hierarchical graph representations:

```python
from torch_geometric.nn import TopKPooling, global_mean_pool

class HierarchicalGNN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.pool1 = TopKPooling(64, ratio=0.8)
        self.conv2 = GCNConv(64, 64)
        self.pool2 = TopKPooling(64, ratio=0.8)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = F.relu(self.conv1(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool1(x, edge_index, None, batch)

        x = F.relu(self.conv2(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool2(x, edge_index, None, batch)

        x = global_mean_pool(x, batch)
        x = self.lin(x)
        return F.log_softmax(x, dim=1)
```

## Common Patterns and Best Practices

### Check Graph Properties

```python
# Undirected check
from torch_geometric.utils import is_undirected
print(f"Is undirected: {is_undirected(data.edge_index)}")

# Connected components
from torch_geometric.utils import connected_components
print(f"Connected components: {connected_components(data.edge_index)}")

# Contains self-loops
from torch_geometric.utils import contains_self_loops
print(f"Has self-loops: {contains_self_loops(data.edge_index)}")
```

### GPU Training

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
data = data.to(device)

# For DataLoader
for batch in loader:
    batch = batch.to(device)
    # Train...
```

### Save and Load Models

```python
# Save
torch.save(model.state_dict(), 'model.pth')

# Load
model = GCN(num_features, num_classes)
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

### Layer Capabilities

When choosing layers, consider these capabilities:
- **SparseTensor**: Supports efficient sparse matrix operations
- **edge_weight**: Handles one-dimensional edge weights
- **edge_attr**: Processes multi-dimensional edge features
- **Bipartite**: Works with bipartite graphs (different source/target dimensions)
- **Lazy**: Enables initialization without specifying input dimensions

See the GNN cheatsheet at `references/layer_capabilities.md`.

## Resources

### Bundled References

This skill includes detailed reference documentation:

- **`references/layers_reference.md`**: Complete listing of all 40+ GNN layers with descriptions and capabilities
- **`references/datasets_reference.md`**: Comprehensive dataset catalog organized by category
- **`references/transforms_reference.md`**: All available transforms and their use cases
- **`references/api_patterns.md`**: Common API patterns and coding examples

### Scripts

Utility scripts are provided in `scripts/`:

- **`scripts/visualize_graph.py`**: Visualize graph structure using networkx and matplotlib
- **`scripts/create_gnn_template.py`**: Generate boilerplate code for common GNN architectures
- **`scripts/benchmark_model.py`**: Benchmark model performance on standard datasets

Execute scripts directly or read them for implementation patterns.

### Official Resources

- **Documentation**: https://pytorch-geometric.readthedocs.io/
- **GitHub**: https://github.com/pyg-team/pytorch_geometric
- **Tutorials**: https://pytorch-geometric.readthedocs.io/en/latest/get_started/introduction.html
- **Examples**: https://github.com/pyg-team/pytorch_geometric/tree/master/examples

---

## Reference: Datasets_Reference

# PyTorch Geometric Datasets Reference

This document provides a comprehensive catalog of all datasets available in `torch_geometric.datasets`.

## Citation Networks

### Planetoid
**Usage**: Node classification, semi-supervised learning
**Networks**: Cora, CiteSeer, PubMed
**Description**: Citation networks where nodes are papers and edges are citations
- **Cora**: 2,708 nodes, 5,429 edges, 7 classes, 1,433 features
- **CiteSeer**: 3,327 nodes, 4,732 edges, 6 classes, 3,703 features
- **PubMed**: 19,717 nodes, 44,338 edges, 3 classes, 500 features

```python
from torch_geometric.datasets import Planetoid
dataset = Planetoid(root='/tmp/Cora', name='Cora')
```

### Coauthor
**Usage**: Node classification on collaboration networks
**Networks**: CS, Physics
**Description**: Co-authorship networks from Microsoft Academic Graph
- **CS**: 18,333 nodes, 81,894 edges, 15 classes (computer science)
- **Physics**: 34,493 nodes, 247,962 edges, 5 classes (physics)

```python
from torch_geometric.datasets import Coauthor
dataset = Coauthor(root='/tmp/CS', name='CS')
```

### Amazon
**Usage**: Node classification on product networks
**Networks**: Computers, Photo
**Description**: Amazon co-purchase networks where nodes are products
- **Computers**: 13,752 nodes, 245,861 edges, 10 classes
- **Photo**: 7,650 nodes, 119,081 edges, 8 classes

```python
from torch_geometric.datasets import Amazon
dataset = Amazon(root='/tmp/Computers', name='Computers')
```

### CitationFull
**Usage**: Citation network analysis
**Networks**: Cora, Cora_ML, DBLP, PubMed
**Description**: Full citation networks without sampling

```python
from torch_geometric.datasets import CitationFull
dataset = CitationFull(root='/tmp/Cora', name='Cora')
```

## Graph Classification

### TUDataset
**Usage**: Graph classification, graph kernel benchmarks
**Description**: Collection of 120+ graph classification datasets
- **MUTAG**: 188 graphs, 2 classes (molecular compounds)
- **PROTEINS**: 1,113 graphs, 2 classes (protein structures)
- **ENZYMES**: 600 graphs, 6 classes (protein enzymes)
- **IMDB-BINARY**: 1,000 graphs, 2 classes (social networks)
- **REDDIT-BINARY**: 2,000 graphs, 2 classes (discussion threads)
- **COLLAB**: 5,000 graphs, 3 classes (scientific collaborations)
- **NCI1**: 4,110 graphs, 2 classes (chemical compounds)
- **DD**: 1,178 graphs, 2 classes (protein structures)

```python
from torch_geometric.datasets import TUDataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')
```

### MoleculeNet
**Usage**: Molecular property prediction
**Datasets**: Over 10 molecular benchmark datasets
**Description**: Comprehensive molecular machine learning benchmarks
- **ESOL**: Aqueous solubility (regression)
- **FreeSolv**: Hydration free energy (regression)
- **Lipophilicity**: Octanol/water distribution (regression)
- **BACE**: Binding results (classification)
- **BBBP**: Blood-brain barrier penetration (classification)
- **HIV**: HIV inhibition (classification)
- **Tox21**: Toxicity prediction (multi-task classification)
- **ToxCast**: Toxicology forecasting (multi-task classification)
- **SIDER**: Side effects (multi-task classification)
- **ClinTox**: Clinical trial toxicity (multi-task classification)

```python
from torch_geometric.datasets import MoleculeNet
dataset = MoleculeNet(root='/tmp/ESOL', name='ESOL')
```

## Molecular and Chemical Datasets

### QM7b
**Usage**: Molecular property prediction (quantum mechanics)
**Description**: 7,211 molecules with up to 7 heavy atoms
- Properties: Atomization energies, electronic properties

```python
from torch_geometric.datasets import QM7b
dataset = QM7b(root='/tmp/QM7b')
```

### QM9
**Usage**: Molecular property prediction (quantum mechanics)
**Description**: ~130,000 molecules with up to 9 heavy atoms (C, O, N, F)
- Properties: 19 quantum chemical properties including HOMO, LUMO, gap, energy

```python
from torch_geometric.datasets import QM9
dataset = QM9(root='/tmp/QM9')
```

### ZINC
**Usage**: Molecular generation, property prediction
**Description**: ~250,000 drug-like molecular graphs
- Properties: Constrained solubility, molecular weight

```python
from torch_geometric.datasets import ZINC
dataset = ZINC(root='/tmp/ZINC', subset=True)
```

### AQSOL
**Usage**: Aqueous solubility prediction
**Description**: ~10,000 molecules with solubility measurements

```python
from torch_geometric.datasets import AQSOL
dataset = AQSOL(root='/tmp/AQSOL')
```

### MD17
**Usage**: Molecular dynamics, force field learning
**Description**: Molecular dynamics trajectories for small molecules
- Molecules: Benzene, Uracil, Naphthalene, Aspirin, Salicylic acid, etc.

```python
from torch_geometric.datasets import MD17
dataset = MD17(root='/tmp/MD17', name='benzene')
```

### PCQM4Mv2
**Usage**: Large-scale molecular property prediction
**Description**: 3.8M molecules from PubChem for quantum chemistry
- Part of OGB Large-Scale Challenge

```python
from torch_geometric.datasets import PCQM4Mv2
dataset = PCQM4Mv2(root='/tmp/PCQM4Mv2')
```

## Social Networks

### Reddit
**Usage**: Large-scale node classification
**Description**: Reddit posts from September 2014
- 232,965 nodes, 11,606,919 edges, 41 classes
- Features: TF-IDF of post content

```python
from torch_geometric.datasets import Reddit
dataset = Reddit(root='/tmp/Reddit')
```

### Reddit2
**Usage**: Large-scale node classification
**Description**: Updated Reddit dataset with more posts

```python
from torch_geometric.datasets import Reddit2
dataset = Reddit2(root='/tmp/Reddit2')
```

### Twitch
**Usage**: Node classification, social network analysis
**Networks**: DE, EN, ES, FR, PT, RU
**Description**: Twitch user networks by language

```python
from torch_geometric.datasets import Twitch
dataset = Twitch(root='/tmp/Twitch', name='DE')
```

### Facebook
**Usage**: Social network analysis, node classification
**Description**: Facebook page-page networks

```python
from torch_geometric.datasets import FacebookPagePage
dataset = FacebookPagePage(root='/tmp/Facebook')
```

### GitHub
**Usage**: Social network analysis
**Description**: GitHub developer networks

```python
from torch_geometric.datasets import GitHub
dataset = GitHub(root='/tmp/GitHub')
```

## Knowledge Graphs

### Entities
**Usage**: Link prediction, knowledge graph embeddings
**Datasets**: AIFB, MUTAG, BGS, AM
**Description**: RDF knowledge graphs with typed relations

```python
from torch_geometric.datasets import Entities
dataset = Entities(root='/tmp/AIFB', name='AIFB')
```

### WordNet18
**Usage**: Link prediction on semantic networks
**Description**: Subset of WordNet with 18 relations
- 40,943 entities, 151,442 triplets

```python
from torch_geometric.datasets import WordNet18
dataset = WordNet18(root='/tmp/WordNet18')
```

### WordNet18RR
**Usage**: Link prediction (no inverse relations)
**Description**: Refined version without inverse relations

```python
from torch_geometric.datasets import WordNet18RR
dataset = WordNet18RR(root='/tmp/WordNet18RR')
```

### FB15k-237
**Usage**: Link prediction on Freebase
**Description**: Subset of Freebase with 237 relations
- 14,541 entities, 310,116 triplets

```python
from torch_geometric.datasets import FB15k_237
dataset = FB15k_237(root='/tmp/FB15k')
```

## Heterogeneous Graphs

### OGB_MAG
**Usage**: Heterogeneous graph learning, node classification
**Description**: Microsoft Academic Graph with multiple node/edge types
- Node types: paper, author, institution, field of study
- 1M+ nodes, 21M+ edges

```python
from torch_geometric.datasets import OGB_MAG
dataset = OGB_MAG(root='/tmp/OGB_MAG')
```

### MovieLens
**Usage**: Recommendation systems, link prediction
**Versions**: 100K, 1M, 10M, 20M
**Description**: User-movie rating networks
- Node types: user, movie
- Edge types: rates

```python
from torch_geometric.datasets import MovieLens
dataset = MovieLens(root='/tmp/MovieLens', model_name='100k')
```

### IMDB
**Usage**: Heterogeneous graph learning
**Description**: IMDB movie network
- Node types: movie, actor, director

```python
from torch_geometric.datasets import IMDB
dataset = IMDB(root='/tmp/IMDB')
```

### DBLP
**Usage**: Heterogeneous graph learning, node classification
**Description**: DBLP bibliography network
- Node types: author, paper, term, conference

```python
from torch_geometric.datasets import DBLP
dataset = DBLP(root='/tmp/DBLP')
```

### LastFM
**Usage**: Heterogeneous recommendation
**Description**: LastFM music network
- Node types: user, artist, tag

```python
from torch_geometric.datasets import LastFM
dataset = LastFM(root='/tmp/LastFM')
```

## Temporal Graphs

### BitcoinOTC
**Usage**: Temporal link prediction, trust networks
**Description**: Bitcoin OTC trust network over time

```python
from torch_geometric.datasets import BitcoinOTC
dataset = BitcoinOTC(root='/tmp/BitcoinOTC')
```

### ICEWS18
**Usage**: Temporal knowledge graph completion
**Description**: Integrated Crisis Early Warning System events

```python
from torch_geometric.datasets import ICEWS18
dataset = ICEWS18(root='/tmp/ICEWS18')
```

### GDELT
**Usage**: Temporal event forecasting
**Description**: Global Database of Events, Language, and Tone

```python
from torch_geometric.datasets import GDELT
dataset = GDELT(root='/tmp/GDELT')
```

### JODIEDataset
**Usage**: Dynamic graph learning
**Datasets**: Reddit, Wikipedia, MOOC, LastFM
**Description**: Temporal interaction networks

```python
from torch_geometric.datasets import JODIEDataset
dataset = JODIEDataset(root='/tmp/JODIE', name='Reddit')
```

## 3D Meshes and Point Clouds

### ShapeNet
**Usage**: 3D shape classification and segmentation
**Description**: Large-scale 3D CAD model dataset
- 16,881 models across 16 categories
- Part-level segmentation labels

```python
from torch_geometric.datasets import ShapeNet
dataset = ShapeNet(root='/tmp/ShapeNet', categories=['Airplane'])
```

### ModelNet
**Usage**: 3D shape classification
**Versions**: ModelNet10, ModelNet40
**Description**: CAD models for 3D object classification
- ModelNet10: 4,899 models, 10 categories
- ModelNet40: 12,311 models, 40 categories

```python
from torch_geometric.datasets import ModelNet
dataset = ModelNet(root='/tmp/ModelNet', name='10')
```

### FAUST
**Usage**: 3D shape matching, correspondence
**Description**: Human body scans for shape analysis
- 100 meshes of 10 people in 10 poses

```python
from torch_geometric.datasets import FAUST
dataset = FAUST(root='/tmp/FAUST')
```

### CoMA
**Usage**: 3D mesh deformation
**Description**: Facial expression meshes
- 20,466 3D face scans with expressions

```python
from torch_geometric.datasets import CoMA
dataset = CoMA(root='/tmp/CoMA')
```

### S3DIS
**Usage**: 3D semantic segmentation
**Description**: Stanford Large-Scale 3D Indoor Spaces
- 6 areas, 271 rooms, point cloud data

```python
from torch_geometric.datasets import S3DIS
dataset = S3DIS(root='/tmp/S3DIS', test_area=6)
```

## Image and Vision Datasets

### MNISTSuperpixels
**Usage**: Graph-based image classification
**Description**: MNIST images as superpixel graphs
- 70,000 graphs (60k train, 10k test)

```python
from torch_geometric.datasets import MNISTSuperpixels
dataset = MNISTSuperpixels(root='/tmp/MNIST')
```

### Flickr
**Usage**: Image description, node classification
**Description**: Flickr image network
- 89,250 nodes, 899,756 edges

```python
from torch_geometric.datasets import Flickr
dataset = Flickr(root='/tmp/Flickr')
```

### PPI
**Usage**: Protein-protein interaction prediction
**Description**: Multi-graph protein interaction networks
- 24 graphs, 2,373 nodes total

```python
from torch_geometric.datasets import PPI
dataset = PPI(root='/tmp/PPI', split='train')
```

## Small Classic Graphs

### KarateClub
**Usage**: Community detection, visualization
**Description**: Zachary's karate club network
- 34 nodes, 78 edges, 2 communities

```python
from torch_geometric.datasets import KarateClub
dataset = KarateClub()
```

## Open Graph Benchmark (OGB)

PyG integrates seamlessly with OGB datasets:

### Node Property Prediction
- **ogbn-products**: Amazon product network (2.4M nodes)
- **ogbn-proteins**: Protein association network (132K nodes)
- **ogbn-arxiv**: Citation network (169K nodes)
- **ogbn-papers100M**: Large citation network (111M nodes)
- **ogbn-mag**: Heterogeneous academic graph

### Link Property Prediction
- **ogbl-ppa**: Protein association networks
- **ogbl-collab**: Collaboration networks
- **ogbl-ddi**: Drug-drug interaction network
- **ogbl-citation2**: Citation network
- **ogbl-wikikg2**: Wikidata knowledge graph

### Graph Property Prediction
- **ogbg-molhiv**: Molecular HIV activity prediction
- **ogbg-molpcba**: Molecular bioassays (multi-task)
- **ogbg-ppa**: Protein function prediction
- **ogbg-code2**: Code abstract syntax trees

```python
from torch_geometric.datasets import OGB_MAG, OGB_PPA
# or
from ogb.nodeproppred import PygNodePropPredDataset
dataset = PygNodePropPredDataset(name='ogbn-arxiv')
```

## Synthetic Datasets

### FakeDataset
**Usage**: Testing, debugging
**Description**: Generates random graph data

```python
from torch_geometric.datasets import FakeDataset
dataset = FakeDataset(num_graphs=100, avg_num_nodes=50)
```

### StochasticBlockModelDataset
**Usage**: Community detection benchmarks
**Description**: Graphs generated from stochastic block models

```python
from torch_geometric.datasets import StochasticBlockModelDataset
dataset = StochasticBlockModelDataset(root='/tmp/SBM', num_graphs=1000)
```

### ExplainerDataset
**Usage**: Testing explainability methods
**Description**: Synthetic graphs with known explanation ground truth

```python
from torch_geometric.datasets import ExplainerDataset
dataset = ExplainerDataset(num_graphs=1000)
```

## Materials Science

### QM8
**Usage**: Molecular property prediction
**Description**: Electronic properties of small molecules

```python
from torch_geometric.datasets import QM8
dataset = QM8(root='/tmp/QM8')
```

## Biological Networks

### PPI (Protein-Protein Interaction)
Already listed above under Image and Vision Datasets

### STRING
**Usage**: Protein interaction networks
**Description**: Known and predicted protein-protein interactions

```python
# Available through external sources or custom loading
```

## Usage Tips

1. **Start with small datasets**: Use Cora, KarateClub, or ENZYMES for prototyping
2. **Citation networks**: Planetoid datasets are perfect for node classification
3. **Graph classification**: TUDataset provides diverse benchmarks
4. **Molecular**: QM9, ZINC, MoleculeNet for chemistry applications
5. **Large-scale**: Use Reddit, OGB datasets with NeighborLoader
6. **Heterogeneous**: OGB_MAG, MovieLens, IMDB for multi-type graphs
7. **Temporal**: JODIE, ICEWS for dynamic graph learning
8. **3D**: ShapeNet, ModelNet, S3DIS for geometric learning

## Common Patterns

### Loading with Transforms
```python
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import NormalizeFeatures

dataset = Planetoid(root='/tmp/Cora', name='Cora',
                    transform=NormalizeFeatures())
```

### Train/Val/Test Splits
```python
# For datasets with pre-defined splits
data = dataset[0]
train_data = data[data.train_mask]
val_data = data[data.val_mask]
test_data = data[data.test_mask]

# For graph classification
from torch_geometric.loader import DataLoader
train_dataset = dataset[:int(len(dataset) * 0.8)]
test_dataset = dataset[int(len(dataset) * 0.8):]
train_loader = DataLoader(train_dataset, batch_size=32)
```

### Custom Data Loading
```python
from torch_geometric.data import Data, Dataset

class MyCustomDataset(Dataset):
    def __init__(self, root, transform=None):
        super().__init__(root, transform)
        # Your initialization

    def len(self):
        return len(self.data_list)

    def get(self, idx):
        # Load and return data object
        return self.data_list[idx]
```

---

## Reference: Layers_Reference

# PyTorch Geometric Neural Network Layers Reference

This document provides a comprehensive reference of all neural network layers available in `torch_geometric.nn`.

## Layer Capability Flags

When selecting layers, consider these capability flags:

- **SparseTensor**: Supports `torch_sparse.SparseTensor` format for efficient sparse operations
- **edge_weight**: Handles one-dimensional edge weight data
- **edge_attr**: Processes multi-dimensional edge feature information
- **Bipartite**: Works with bipartite graphs (different source/target node dimensions)
- **Static**: Operates on static graphs with batched node features
- **Lazy**: Enables initialization without specifying input channel dimensions

## Convolutional Layers

### Standard Graph Convolutions

**GCNConv** - Graph Convolutional Network layer
- Implements spectral graph convolution with symmetric normalization
- Supports: SparseTensor, edge_weight, Bipartite, Lazy
- Use for: Citation networks, social networks, general graph learning
- Example: `GCNConv(in_channels, out_channels, improved=False, cached=True)`

**SAGEConv** - GraphSAGE layer
- Inductive learning via neighborhood sampling and aggregation
- Supports: SparseTensor, Bipartite, Lazy
- Use for: Large graphs, inductive learning, heterogeneous features
- Example: `SAGEConv(in_channels, out_channels, aggr='mean')`

**GATConv** - Graph Attention Network layer
- Multi-head attention mechanism for adaptive neighbor weighting
- Supports: SparseTensor, edge_attr, Bipartite, Static, Lazy
- Use for: Tasks requiring variable neighbor importance
- Example: `GATConv(in_channels, out_channels, heads=8, dropout=0.6)`

**GraphConv** - Simple graph convolution (Morris et al.)
- Basic message passing with optional edge weights
- Supports: SparseTensor, edge_weight, Bipartite, Lazy
- Use for: Baseline models, simple graph structures
- Example: `GraphConv(in_channels, out_channels, aggr='add')`

**GINConv** - Graph Isomorphism Network layer
- Maximally powerful GNN for graph isomorphism testing
- Supports: Bipartite
- Use for: Graph classification, molecular property prediction
- Example: `GINConv(nn.Sequential(nn.Linear(in_channels, out_channels), nn.ReLU()))`

**TransformerConv** - Graph Transformer layer
- Combines graph structure with transformer attention
- Supports: SparseTensor, Bipartite, Lazy
- Use for: Long-range dependencies, complex graphs
- Example: `TransformerConv(in_channels, out_channels, heads=8, beta=True)`

**ChebConv** - Chebyshev spectral graph convolution
- Uses Chebyshev polynomials for efficient spectral filtering
- Supports: SparseTensor, edge_weight, Bipartite, Lazy
- Use for: Spectral graph learning, efficient convolutions
- Example: `ChebConv(in_channels, out_channels, K=3)`

**SGConv** - Simplified Graph Convolution
- Pre-computes fixed number of propagation steps
- Supports: SparseTensor, edge_weight, Bipartite, Lazy
- Use for: Fast training, shallow models
- Example: `SGConv(in_channels, out_channels, K=2)`

**APPNP** - Approximate Personalized Propagation of Neural Predictions
- Separates feature transformation from propagation
- Supports: SparseTensor, edge_weight, Lazy
- Use for: Deep propagation without oversmoothing
- Example: `APPNP(K=10, alpha=0.1)`

**ARMAConv** - ARMA graph convolution
- Uses ARMA filters for graph filtering
- Supports: SparseTensor, edge_weight, Bipartite, Lazy
- Use for: Advanced spectral methods
- Example: `ARMAConv(in_channels, out_channels, num_stacks=3, num_layers=2)`

**GATv2Conv** - Improved Graph Attention Network
- Fixes static attention computation issue in GAT
- Supports: SparseTensor, edge_attr, Bipartite, Static, Lazy
- Use for: Better attention learning than original GAT
- Example: `GATv2Conv(in_channels, out_channels, heads=8)`

**SuperGATConv** - Self-supervised Graph Attention
- Adds self-supervised attention mechanism
- Supports: SparseTensor, edge_attr, Bipartite, Static, Lazy
- Use for: Self-supervised learning, limited labels
- Example: `SuperGATConv(in_channels, out_channels, heads=8)`

**GMMConv** - Gaussian Mixture Model Convolution
- Uses Gaussian kernels in pseudo-coordinate space
- Supports: Bipartite
- Use for: Point clouds, spatial data
- Example: `GMMConv(in_channels, out_channels, dim=3, kernel_size=5)`

**SplineConv** - Spline-based convolution
- B-spline basis functions for spatial filtering
- Supports: Bipartite
- Use for: Irregular grids, continuous spaces
- Example: `SplineConv(in_channels, out_channels, dim=2, kernel_size=5)`

**NNConv** - Neural Network Convolution
- Edge features processed by neural networks
- Supports: edge_attr, Bipartite
- Use for: Rich edge features, molecular graphs
- Example: `NNConv(in_channels, out_channels, nn=edge_nn, aggr='mean')`

**CGConv** - Crystal Graph Convolution
- Designed for crystalline materials
- Supports: Bipartite
- Use for: Materials science, crystal structures
- Example: `CGConv(in_channels, dim=3, batch_norm=True)`

**EdgeConv** - Edge Convolution (Dynamic Graph CNN)
- Dynamically computes edges based on feature space
- Supports: Static
- Use for: Point clouds, dynamic graphs
- Example: `EdgeConv(nn=edge_nn, aggr='max')`

**PointNetConv** - PointNet++ convolution
- Local and global feature learning for point clouds
- Use for: 3D point cloud processing
- Example: `PointNetConv(local_nn, global_nn)`

**ResGatedGraphConv** - Residual Gated Graph Convolution
- Gating mechanism with residual connections
- Supports: edge_attr, Bipartite, Lazy
- Use for: Deep GNNs, complex features
- Example: `ResGatedGraphConv(in_channels, out_channels)`

**GENConv** - Generalized Graph Convolution
- Generalizes multiple GNN variants
- Supports: SparseTensor, edge_weight, edge_attr, Bipartite, Lazy
- Use for: Flexible architecture exploration
- Example: `GENConv(in_channels, out_channels, aggr='softmax', num_layers=2)`

**FiLMConv** - Feature-wise Linear Modulation
- Conditions on global features
- Supports: Bipartite, Lazy
- Use for: Conditional generation, multi-task learning
- Example: `FiLMConv(in_channels, out_channels, num_relations=5)`

**PANConv** - Path Attention Network
- Attention over multi-hop paths
- Supports: SparseTensor, Lazy
- Use for: Complex connectivity patterns
- Example: `PANConv(in_channels, out_channels, filter_size=3)`

**ClusterGCNConv** - Cluster-GCN convolution
- Efficient training via graph clustering
- Supports: edge_attr, Lazy
- Use for: Very large graphs
- Example: `ClusterGCNConv(in_channels, out_channels)`

**MFConv** - Multi-scale Feature Convolution
- Aggregates features at multiple scales
- Supports: SparseTensor, Lazy
- Use for: Multi-scale patterns
- Example: `MFConv(in_channels, out_channels)`

**RGCNConv** - Relational Graph Convolution
- Handles multiple edge types
- Supports: SparseTensor, edge_weight, Lazy
- Use for: Knowledge graphs, heterogeneous graphs
- Example: `RGCNConv(in_channels, out_channels, num_relations=10)`

**FAConv** - Frequency Adaptive Convolution
- Adaptive filtering in spectral domain
- Supports: SparseTensor, Lazy
- Use for: Spectral graph learning
- Example: `FAConv(in_channels, eps=0.1, dropout=0.5)`

### Molecular and 3D Convolutions

**SchNet** - Continuous-filter convolutional layer
- Designed for molecular dynamics
- Use for: Molecular property prediction, 3D molecules
- Example: `SchNet(hidden_channels=128, num_filters=64, num_interactions=6)`

**DimeNet** - Directional Message Passing
- Uses directional information and angles
- Use for: 3D molecular structures, chemical properties
- Example: `DimeNet(hidden_channels=128, out_channels=1, num_blocks=6)`

**PointTransformerConv** - Point cloud transformer
- Transformer for 3D point clouds
- Use for: 3D vision, point cloud segmentation
- Example: `PointTransformerConv(in_channels, out_channels)`

### Hypergraph Convolutions

**HypergraphConv** - Hypergraph convolution
- Operates on hyperedges (edges connecting multiple nodes)
- Supports: Lazy
- Use for: Multi-way relationships, chemical reactions
- Example: `HypergraphConv(in_channels, out_channels)`

**HGTConv** - Heterogeneous Graph Transformer
- Transformer for heterogeneous graphs with multiple types
- Supports: Lazy
- Use for: Heterogeneous networks, knowledge graphs
- Example: `HGTConv(in_channels, out_channels, metadata, heads=8)`

## Aggregation Operators

**Aggr** - Base aggregation class
- Flexible aggregation across nodes

**SumAggregation** - Sum aggregation
- Example: `SumAggregation()`

**MeanAggregation** - Mean aggregation
- Example: `MeanAggregation()`

**MaxAggregation** - Max aggregation
- Example: `MaxAggregation()`

**SoftmaxAggregation** - Softmax-weighted aggregation
- Learnable attention weights
- Example: `SoftmaxAggregation(learn=True)`

**PowerMeanAggregation** - Power mean aggregation
- Learnable power parameter
- Example: `PowerMeanAggregation(learn=True)`

**LSTMAggregation** - LSTM-based aggregation
- Sequential processing of neighbors
- Example: `LSTMAggregation(in_channels, out_channels)`

**SetTransformerAggregation** - Set Transformer aggregation
- Transformer for permutation-invariant aggregation
- Example: `SetTransformerAggregation(in_channels, out_channels)`

**MultiAggregation** - Multiple aggregations
- Combines multiple aggregation methods
- Example: `MultiAggregation(['mean', 'max', 'std'])`

## Pooling Layers

### Global Pooling

**global_mean_pool** - Global mean pooling
- Averages node features per graph
- Example: `global_mean_pool(x, batch)`

**global_max_pool** - Global max pooling
- Max over node features per graph
- Example: `global_max_pool(x, batch)`

**global_add_pool** - Global sum pooling
- Sums node features per graph
- Example: `global_add_pool(x, batch)`

**global_sort_pool** - Global sort pooling
- Sorts and concatenates top-k nodes
- Example: `global_sort_pool(x, batch, k=30)`

**GlobalAttention** - Global attention pooling
- Learnable attention weights for aggregation
- Example: `GlobalAttention(gate_nn)`

**Set2Set** - Set2Set pooling
- LSTM-based attention mechanism
- Example: `Set2Set(in_channels, processing_steps=3)`

### Hierarchical Pooling

**TopKPooling** - Top-k pooling
- Keeps top-k nodes based on projection scores
- Example: `TopKPooling(in_channels, ratio=0.5)`

**SAGPooling** - Self-Attention Graph Pooling
- Uses self-attention for node selection
- Example: `SAGPooling(in_channels, ratio=0.5)`

**ASAPooling** - Adaptive Structure Aware Pooling
- Structure-aware node selection
- Example: `ASAPooling(in_channels, ratio=0.5)`

**PANPooling** - Path Attention Pooling
- Attention over paths for pooling
- Example: `PANPooling(in_channels, ratio=0.5)`

**EdgePooling** - Edge contraction pooling
- Pools by contracting edges
- Example: `EdgePooling(in_channels)`

**MemPooling** - Memory-based pooling
- Learnable cluster assignments
- Example: `MemPooling(in_channels, out_channels, heads=4, num_clusters=10)`

**avg_pool** / **max_pool** - Average/Max pool with clustering
- Pools nodes within clusters
- Example: `avg_pool(cluster, data)`

## Normalization Layers

**BatchNorm** - Batch normalization
- Normalizes features across batch
- Example: `BatchNorm(in_channels)`

**LayerNorm** - Layer normalization
- Normalizes features per sample
- Example: `LayerNorm(in_channels)`

**InstanceNorm** - Instance normalization
- Normalizes per sample and graph
- Example: `InstanceNorm(in_channels)`

**GraphNorm** - Graph normalization
- Graph-specific normalization
- Example: `GraphNorm(in_channels)`

**PairNorm** - Pair normalization
- Prevents oversmoothing in deep GNNs
- Example: `PairNorm(scale_individually=False)`

**MessageNorm** - Message normalization
- Normalizes messages during passing
- Example: `MessageNorm(learn_scale=True)`

**DiffGroupNorm** - Differentiable Group Normalization
- Learnable grouping for normalization
- Example: `DiffGroupNorm(in_channels, groups=10)`

## Model Architectures

### Pre-Built Models

**GCN** - Complete Graph Convolutional Network
- Multi-layer GCN with dropout
- Example: `GCN(in_channels, hidden_channels, num_layers, out_channels)`

**GraphSAGE** - Complete GraphSAGE model
- Multi-layer SAGE with dropout
- Example: `GraphSAGE(in_channels, hidden_channels, num_layers, out_channels)`

**GIN** - Complete Graph Isomorphism Network
- Multi-layer GIN for graph classification
- Example: `GIN(in_channels, hidden_channels, num_layers, out_channels)`

**GAT** - Complete Graph Attention Network
- Multi-layer GAT with attention
- Example: `GAT(in_channels, hidden_channels, num_layers, out_channels, heads=8)`

**PNA** - Principal Neighbourhood Aggregation
- Combines multiple aggregators and scalers
- Example: `PNA(in_channels, hidden_channels, num_layers, out_channels)`

**EdgeCNN** - Edge Convolution CNN
- Dynamic graph CNN for point clouds
- Example: `EdgeCNN(out_channels, num_layers=3, k=20)`

### Auto-Encoders

**GAE** - Graph Auto-Encoder
- Encodes graphs into latent space
- Example: `GAE(encoder)`

**VGAE** - Variational Graph Auto-Encoder
- Probabilistic graph encoding
- Example: `VGAE(encoder)`

**ARGA** - Adversarially Regularized Graph Auto-Encoder
- GAE with adversarial regularization
- Example: `ARGA(encoder, discriminator)`

**ARGVA** - Adversarially Regularized Variational Graph Auto-Encoder
- VGAE with adversarial regularization
- Example: `ARGVA(encoder, discriminator)`

### Knowledge Graph Embeddings

**TransE** - Translating embeddings
- Learns entity and relation embeddings
- Example: `TransE(num_nodes, num_relations, hidden_channels)`

**RotatE** - Rotational embeddings
- Embeddings in complex space
- Example: `RotatE(num_nodes, num_relations, hidden_channels)`

**ComplEx** - Complex embeddings
- Complex-valued embeddings
- Example: `ComplEx(num_nodes, num_relations, hidden_channels)`

**DistMult** - Bilinear diagonal model
- Simplified bilinear model
- Example: `DistMult(num_nodes, num_relations, hidden_channels)`

## Utility Layers

**Sequential** - Sequential container
- Chains multiple layers
- Example: `Sequential('x, edge_index', [(GCNConv(16, 64), 'x, edge_index -> x'), nn.ReLU()])`

**JumpingKnowledge** - Jumping knowledge connections
- Combines representations from all layers
- Modes: 'cat', 'max', 'lstm'
- Example: `JumpingKnowledge(mode='cat')`

**DeepGCNLayer** - Deep GCN layer wrapper
- Enables very deep GNNs with skip connections
- Example: `DeepGCNLayer(conv, norm, act, block='res+', dropout=0.1)`

**MLP** - Multi-layer perceptron
- Standard feedforward network
- Example: `MLP([in_channels, 64, 64, out_channels], dropout=0.5)`

**Linear** - Lazy linear layer
- Linear transformation with lazy initialization
- Example: `Linear(in_channels, out_channels, bias=True)`

## Dense Layers

For dense (non-sparse) graph representations:

**DenseGCNConv** - Dense GCN layer
**DenseSAGEConv** - Dense SAGE layer
**DenseGINConv** - Dense GIN layer
**DenseGraphConv** - Dense graph convolution

These are useful when working with small, fully-connected, or densely represented graphs.

## Usage Tips

1. **Start simple**: Begin with GCNConv or GATConv for most tasks
2. **Consider data type**: Use molecular layers (SchNet, DimeNet) for 3D structures
3. **Check capabilities**: Match layer capabilities to your data (edge features, bipartite, etc.)
4. **Deep networks**: Use normalization (PairNorm, LayerNorm) and JumpingKnowledge for deep GNNs
5. **Large graphs**: Use scalable layers (SAGE, Cluster-GCN) with neighbor sampling
6. **Heterogeneous**: Use RGCNConv, HGTConv, or to_hetero() conversion
7. **Lazy initialization**: Use lazy layers when input dimensions vary or are unknown

## Common Patterns

### Basic GNN
```python
from torch_geometric.nn import GCNConv, global_mean_pool

class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return global_mean_pool(x, batch)
```

### Deep GNN with Normalization
```python
class DeepGNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, num_layers, out_channels):
        super().__init__()
        self.convs = torch.nn.ModuleList()
        self.norms = torch.nn.ModuleList()

        self.convs.append(GCNConv(in_channels, hidden_channels))
        self.norms.append(LayerNorm(hidden_channels))

        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
            self.norms.append(LayerNorm(hidden_channels))

        self.convs.append(GCNConv(hidden_channels, out_channels))
        self.jk = JumpingKnowledge(mode='cat')

    def forward(self, x, edge_index, batch):
        xs = []
        for conv, norm in zip(self.convs[:-1], self.norms):
            x = conv(x, edge_index)
            x = norm(x)
            x = F.relu(x)
            xs.append(x)

        x = self.convs[-1](x, edge_index)
        xs.append(x)

        x = self.jk(xs)
        return global_mean_pool(x, batch)
```

---

## Reference: Transforms_Reference

# PyTorch Geometric Transforms Reference

This document provides a comprehensive reference of all transforms available in `torch_geometric.transforms`.

## Overview

Transforms modify `Data` or `HeteroData` objects before or during training. Apply them via:

```python
# During dataset loading
dataset = MyDataset(root='/tmp', transform=MyTransform())

# Apply to individual data
transform = MyTransform()
data = transform(data)

# Compose multiple transforms
from torch_geometric.transforms import Compose
transform = Compose([Transform1(), Transform2(), Transform3()])
```

## General Transforms

### NormalizeFeatures
**Purpose**: Row-normalizes node features to sum to 1
**Use case**: Feature scaling, probability-like features
```python
from torch_geometric.transforms import NormalizeFeatures
transform = NormalizeFeatures()
```

### ToDevice
**Purpose**: Transfers data to specified device (CPU/GPU)
**Use case**: GPU training, device management
```python
from torch_geometric.transforms import ToDevice
transform = ToDevice('cuda')
```

### RandomNodeSplit
**Purpose**: Creates train/val/test node masks
**Use case**: Node classification splits
**Parameters**: `split='train_rest'`, `num_splits`, `num_val`, `num_test`
```python
from torch_geometric.transforms import RandomNodeSplit
transform = RandomNodeSplit(num_val=0.1, num_test=0.2)
```

### RandomLinkSplit
**Purpose**: Creates train/val/test edge splits
**Use case**: Link prediction
**Parameters**: `num_val`, `num_test`, `is_undirected`, `split_labels`
```python
from torch_geometric.transforms import RandomLinkSplit
transform = RandomLinkSplit(num_val=0.1, num_test=0.2)
```

### IndexToMask
**Purpose**: Converts indices to boolean masks
**Use case**: Data preprocessing
```python
from torch_geometric.transforms import IndexToMask
transform = IndexToMask()
```

### MaskToIndex
**Purpose**: Converts boolean masks to indices
**Use case**: Data preprocessing
```python
from torch_geometric.transforms import MaskToIndex
transform = MaskToIndex()
```

### FixedPoints
**Purpose**: Samples a fixed number of points
**Use case**: Point cloud subsampling
**Parameters**: `num`, `replace`, `allow_duplicates`
```python
from torch_geometric.transforms import FixedPoints
transform = FixedPoints(1024)
```

### ToDense
**Purpose**: Converts to dense adjacency matrices
**Use case**: Small graphs, dense operations
```python
from torch_geometric.transforms import ToDense
transform = ToDense(num_nodes=100)
```

### ToSparseTensor
**Purpose**: Converts edge_index to SparseTensor
**Use case**: Efficient sparse operations
**Parameters**: `remove_edge_index`, `fill_cache`
```python
from torch_geometric.transforms import ToSparseTensor
transform = ToSparseTensor()
```

## Graph Structure Transforms

### ToUndirected
**Purpose**: Converts directed graph to undirected
**Use case**: Undirected graph algorithms
**Parameters**: `reduce='add'` (how to handle duplicate edges)
```python
from torch_geometric.transforms import ToUndirected
transform = ToUndirected()
```

### AddSelfLoops
**Purpose**: Adds self-loops to all nodes
**Use case**: GCN-style convolutions
**Parameters**: `fill_value` (edge attribute for self-loops)
```python
from torch_geometric.transforms import AddSelfLoops
transform = AddSelfLoops()
```

### RemoveSelfLoops
**Purpose**: Removes all self-loops
**Use case**: Cleaning graph structure
```python
from torch_geometric.transforms import RemoveSelfLoops
transform = RemoveSelfLoops()
```

### RemoveIsolatedNodes
**Purpose**: Removes nodes without edges
**Use case**: Graph cleaning
```python
from torch_geometric.transforms import RemoveIsolatedNodes
transform = RemoveIsolatedNodes()
```

### RemoveDuplicatedEdges
**Purpose**: Removes duplicate edges
**Use case**: Graph cleaning
```python
from torch_geometric.transforms import RemoveDuplicatedEdges
transform = RemoveDuplicatedEdges()
```

### LargestConnectedComponents
**Purpose**: Keeps only the largest connected component
**Use case**: Focus on main graph structure
**Parameters**: `num_components` (how many components to keep)
```python
from torch_geometric.transforms import LargestConnectedComponents
transform = LargestConnectedComponents(num_components=1)
```

### KNNGraph
**Purpose**: Creates edges based on k-nearest neighbors
**Use case**: Point clouds, spatial data
**Parameters**: `k`, `loop`, `force_undirected`, `flow`
```python
from torch_geometric.transforms import KNNGraph
transform = KNNGraph(k=6)
```

### RadiusGraph
**Purpose**: Creates edges within a radius
**Use case**: Point clouds, spatial data
**Parameters**: `r`, `loop`, `max_num_neighbors`, `flow`
```python
from torch_geometric.transforms import RadiusGraph
transform = RadiusGraph(r=0.1)
```

### Delaunay
**Purpose**: Computes Delaunay triangulation
**Use case**: 2D/3D spatial graphs
```python
from torch_geometric.transforms import Delaunay
transform = Delaunay()
```

### FaceToEdge
**Purpose**: Converts mesh faces to edges
**Use case**: Mesh processing
```python
from torch_geometric.transforms import FaceToEdge
transform = FaceToEdge()
```

### LineGraph
**Purpose**: Converts graph to its line graph
**Use case**: Edge-centric analysis
**Parameters**: `force_directed`
```python
from torch_geometric.transforms import LineGraph
transform = LineGraph()
```

### GDC
**Purpose**: Graph Diffusion Convolution preprocessing
**Use case**: Improved message passing
**Parameters**: `self_loop_weight`, `normalization_in`, `normalization_out`, `diffusion_kwargs`
```python
from torch_geometric.transforms import GDC
transform = GDC(self_loop_weight=1, normalization_in='sym',
                diffusion_kwargs=dict(method='ppr', alpha=0.15))
```

### SIGN
**Purpose**: Scalable Inception Graph Neural Networks preprocessing
**Use case**: Efficient multi-scale features
**Parameters**: `K` (number of hops)
```python
from torch_geometric.transforms import SIGN
transform = SIGN(K=3)
```

## Feature Transforms

### OneHotDegree
**Purpose**: One-hot encodes node degree
**Use case**: Degree as feature
**Parameters**: `max_degree`, `cat` (concatenate with existing features)
```python
from torch_geometric.transforms import OneHotDegree
transform = OneHotDegree(max_degree=100)
```

### LocalDegreeProfile
**Purpose**: Appends local degree profile
**Use case**: Structural node features
```python
from torch_geometric.transforms import LocalDegreeProfile
transform = LocalDegreeProfile()
```

### Constant
**Purpose**: Adds constant features to nodes
**Use case**: Featureless graphs
**Parameters**: `value`, `cat`
```python
from torch_geometric.transforms import Constant
transform = Constant(value=1.0)
```

### TargetIndegree
**Purpose**: Saves in-degree as target
**Use case**: Degree prediction
**Parameters**: `norm`, `max_value`
```python
from torch_geometric.transforms import TargetIndegree
transform = TargetIndegree(norm=False)
```

### AddRandomWalkPE
**Purpose**: Adds random walk positional encoding
**Use case**: Positional information
**Parameters**: `walk_length`, `attr_name`
```python
from torch_geometric.transforms import AddRandomWalkPE
transform = AddRandomWalkPE(walk_length=20)
```

### AddLaplacianEigenvectorPE
**Purpose**: Adds Laplacian eigenvector positional encoding
**Use case**: Spectral positional information
**Parameters**: `k` (number of eigenvectors), `attr_name`
```python
from torch_geometric.transforms import AddLaplacianEigenvectorPE
transform = AddLaplacianEigenvectorPE(k=10)
```

### AddMetaPaths
**Purpose**: Adds meta-path induced edges
**Use case**: Heterogeneous graphs
**Parameters**: `metapaths`, `drop_orig_edges`, `drop_unconnected_nodes`
```python
from torch_geometric.transforms import AddMetaPaths
metapaths = [[('author', 'paper'), ('paper', 'author')]]  # Co-authorship
transform = AddMetaPaths(metapaths)
```

### SVDFeatureReduction
**Purpose**: Reduces feature dimensionality via SVD
**Use case**: Dimensionality reduction
**Parameters**: `out_channels`
```python
from torch_geometric.transforms import SVDFeatureReduction
transform = SVDFeatureReduction(out_channels=64)
```

## Vision/Spatial Transforms

### Center
**Purpose**: Centers node positions
**Use case**: Point cloud preprocessing
```python
from torch_geometric.transforms import Center
transform = Center()
```

### NormalizeScale
**Purpose**: Normalizes positions to unit sphere
**Use case**: Point cloud normalization
```python
from torch_geometric.transforms import NormalizeScale
transform = NormalizeScale()
```

### NormalizeRotation
**Purpose**: Rotates to principal components
**Use case**: Rotation-invariant learning
**Parameters**: `max_points`
```python
from torch_geometric.transforms import NormalizeRotation
transform = NormalizeRotation()
```

### Distance
**Purpose**: Saves Euclidean distance as edge attribute
**Use case**: Spatial graphs
**Parameters**: `norm`, `max_value`, `cat`
```python
from torch_geometric.transforms import Distance
transform = Distance(norm=False, cat=False)
```

### Cartesian
**Purpose**: Saves relative Cartesian coordinates as edge attributes
**Use case**: Spatial relationships
**Parameters**: `norm`, `max_value`, `cat`
```python
from torch_geometric.transforms import Cartesian
transform = Cartesian(norm=False)
```

### Polar
**Purpose**: Saves polar coordinates as edge attributes
**Use case**: 2D spatial graphs
**Parameters**: `norm`, `max_value`, `cat`
```python
from torch_geometric.transforms import Polar
transform = Polar(norm=False)
```

### Spherical
**Purpose**: Saves spherical coordinates as edge attributes
**Use case**: 3D spatial graphs
**Parameters**: `norm`, `max_value`, `cat`
```python
from torch_geometric.transforms import Spherical
transform = Spherical(norm=False)
```

### LocalCartesian
**Purpose**: Saves coordinates in local coordinate system
**Use case**: Local spatial features
**Parameters**: `norm`, `cat`
```python
from torch_geometric.transforms import LocalCartesian
transform = LocalCartesian()
```

### PointPairFeatures
**Purpose**: Computes point pair features
**Use case**: 3D registration, correspondence
**Parameters**: `cat`
```python
from torch_geometric.transforms import PointPairFeatures
transform = PointPairFeatures()
```

## Data Augmentation

### RandomJitter
**Purpose**: Randomly jitters node positions
**Use case**: Point cloud augmentation
**Parameters**: `translate`, `scale`
```python
from torch_geometric.transforms import RandomJitter
transform = RandomJitter(0.01)
```

### RandomFlip
**Purpose**: Randomly flips positions along axis
**Use case**: Geometric augmentation
**Parameters**: `axis`, `p` (probability)
```python
from torch_geometric.transforms import RandomFlip
transform = RandomFlip(axis=0, p=0.5)
```

### RandomScale
**Purpose**: Randomly scales positions
**Use case**: Scale augmentation
**Parameters**: `scales` (min, max)
```python
from torch_geometric.transforms import RandomScale
transform = RandomScale((0.9, 1.1))
```

### RandomRotate
**Purpose**: Randomly rotates positions
**Use case**: Rotation augmentation
**Parameters**: `degrees` (range), `axis` (rotation axis)
```python
from torch_geometric.transforms import RandomRotate
transform = RandomRotate(degrees=15, axis=2)
```

### RandomShear
**Purpose**: Randomly shears positions
**Use case**: Geometric augmentation
**Parameters**: `shear` (range)
```python
from torch_geometric.transforms import RandomShear
transform = RandomShear(0.1)
```

### RandomTranslate
**Purpose**: Randomly translates positions
**Use case**: Translation augmentation
**Parameters**: `translate` (range)
```python
from torch_geometric.transforms import RandomTranslate
transform = RandomTranslate(0.1)
```

### LinearTransformation
**Purpose**: Applies linear transformation matrix
**Use case**: Custom geometric transforms
**Parameters**: `matrix`
```python
from torch_geometric.transforms import LinearTransformation
import torch
matrix = torch.eye(3)
transform = LinearTransformation(matrix)
```

## Mesh Processing

### SamplePoints
**Purpose**: Samples points uniformly from mesh
**Use case**: Mesh to point cloud conversion
**Parameters**: `num`, `remove_faces`, `include_normals`
```python
from torch_geometric.transforms import SamplePoints
transform = SamplePoints(num=1024)
```

### GenerateMeshNormals
**Purpose**: Generates face/vertex normals
**Use case**: Mesh processing
```python
from torch_geometric.transforms import GenerateMeshNormals
transform = GenerateMeshNormals()
```

### FaceToEdge
**Purpose**: Converts mesh faces to edges
**Use case**: Mesh to graph conversion
**Parameters**: `remove_faces`
```python
from torch_geometric.transforms import FaceToEdge
transform = FaceToEdge()
```

## Sampling and Splitting

### GridSampling
**Purpose**: Clusters points in voxel grid
**Use case**: Point cloud downsampling
**Parameters**: `size` (voxel size), `start`, `end`
```python
from torch_geometric.transforms import GridSampling
transform = GridSampling(size=0.1)
```

### FixedPoints
**Purpose**: Samples fixed number of points
**Use case**: Uniform point cloud size
**Parameters**: `num`, `replace`, `allow_duplicates`
```python
from torch_geometric.transforms import FixedPoints
transform = FixedPoints(num=2048, replace=False)
```

### RandomScale
**Purpose**: Randomly scales by sampling from range
**Use case**: Scale augmentation (already listed above)

### VirtualNode
**Purpose**: Adds a virtual node connected to all nodes
**Use case**: Global information propagation
```python
from torch_geometric.transforms import VirtualNode
transform = VirtualNode()
```

## Specialized Transforms

### ToSLIC
**Purpose**: Converts images to superpixel graphs (SLIC algorithm)
**Use case**: Image as graph
**Parameters**: `num_segments`, `compactness`, `add_seg`, `add_img`
```python
from torch_geometric.transforms import ToSLIC
transform = ToSLIC(num_segments=75)
```

### GCNNorm
**Purpose**: Applies GCN-style normalization to edges
**Use case**: Preprocessing for GCN
**Parameters**: `add_self_loops`
```python
from torch_geometric.transforms import GCNNorm
transform = GCNNorm(add_self_loops=True)
```

### LaplacianLambdaMax
**Purpose**: Computes largest Laplacian eigenvalue
**Use case**: ChebConv preprocessing
**Parameters**: `normalization`, `is_undirected`
```python
from torch_geometric.transforms import LaplacianLambdaMax
transform = LaplacianLambdaMax(normalization='sym')
```

### NormalizeRotation
**Purpose**: Rotates mesh/point cloud to align with principal axes
**Use case**: Canonical orientation
**Parameters**: `max_points`
```python
from torch_geometric.transforms import NormalizeRotation
transform = NormalizeRotation()
```

## Compose and Apply

### Compose
**Purpose**: Chains multiple transforms
**Use case**: Complex preprocessing pipelines
```python
from torch_geometric.transforms import Compose
transform = Compose([
    Center(),
    NormalizeScale(),
    KNNGraph(k=6),
    Distance(norm=False),
])
```

### BaseTransform
**Purpose**: Base class for custom transforms
**Use case**: Implementing custom transforms
```python
from torch_geometric.transforms import BaseTransform

class MyTransform(BaseTransform):
    def __init__(self, param):
        self.param = param

    def __call__(self, data):
        # Modify data
        data.x = data.x * self.param
        return data
```

## Common Transform Combinations

### Node Classification Preprocessing
```python
transform = Compose([
    NormalizeFeatures(),
    RandomNodeSplit(num_val=0.1, num_test=0.2),
])
```

### Point Cloud Processing
```python
transform = Compose([
    Center(),
    NormalizeScale(),
    RandomRotate(degrees=15, axis=2),
    RandomJitter(0.01),
    KNNGraph(k=6),
    Distance(norm=False),
])
```

### Mesh to Graph
```python
transform = Compose([
    FaceToEdge(remove_faces=True),
    GenerateMeshNormals(),
    Distance(norm=True),
])
```

### Graph Structure Enhancement
```python
transform = Compose([
    ToUndirected(),
    AddSelfLoops(),
    RemoveIsolatedNodes(),
    GCNNorm(),
])
```

### Heterogeneous Graph Preprocessing
```python
transform = Compose([
    AddMetaPaths(metapaths=[
        [('author', 'paper'), ('paper', 'author')],
        [('author', 'paper'), ('paper', 'conference'), ('conference', 'paper'), ('paper', 'author')]
    ]),
    RandomNodeSplit(split='train_rest', num_val=0.1, num_test=0.2),
])
```

### Link Prediction
```python
transform = Compose([
    NormalizeFeatures(),
    RandomLinkSplit(num_val=0.1, num_test=0.2, is_undirected=True),
])
```

## Usage Tips

1. **Order matters**: Apply structural transforms before feature transforms
2. **Caching**: Some transforms (like GDC) are expensive—apply once
3. **Augmentation**: Use Random* transforms during training only
4. **Compose sparingly**: Too many transforms slow down data loading
5. **Custom transforms**: Inherit from `BaseTransform` for custom logic
6. **Pre-transforms**: Apply expensive transforms once during dataset processing:
   ```python
   dataset = MyDataset(root='/tmp', pre_transform=ExpensiveTransform())
   ```
7. **Dynamic transforms**: Apply cheap transforms during training:
   ```python
   dataset = MyDataset(root='/tmp', transform=CheapTransform())
   ```

## Performance Considerations

**Expensive transforms** (apply as pre_transform):
- GDC
- SIGN
- KNNGraph (for large point clouds)
- AddLaplacianEigenvectorPE
- SVDFeatureReduction

**Cheap transforms** (apply as transform):
- NormalizeFeatures
- ToUndirected
- AddSelfLoops
- Random* augmentations
- ToDevice

**Example**:
```python
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import Compose, GDC, NormalizeFeatures

# Expensive preprocessing done once
pre_transform = GDC(
    self_loop_weight=1,
    normalization_in='sym',
    diffusion_kwargs=dict(method='ppr', alpha=0.15)
)

# Cheap transform applied each time
transform = NormalizeFeatures()

dataset = Planetoid(
    root='/tmp/Cora',
    name='Cora',
    pre_transform=pre_transform,
    transform=transform
)
```
