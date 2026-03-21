---
title: "Torchdrug"
description: "PyTorch-native graph neural networks for molecules and proteins. Use when building custom GNN architectures for drug discovery, protein modeling, or knowledge graph reasoning. Best for custom model development, protein property prediction, retrosy..."
category: "research"
source: "community"
author: "Community"
tags: ["torchdrug"]
date: 2026-03-20
---

# TorchDrug

## Overview

TorchDrug is a comprehensive PyTorch-based machine learning toolbox for drug discovery and molecular science. Apply graph neural networks, pre-trained models, and task definitions to molecules, proteins, and biological knowledge graphs, including molecular property prediction, protein modeling, knowledge graph reasoning, molecular generation, retrosynthesis planning, with 40+ curated datasets and 20+ model architectures.

## When to Use This Skill

This skill should be used when working with:

**Data Types:**
- SMILES strings or molecular structures
- Protein sequences or 3D structures (PDB files)
- Chemical reactions and retrosynthesis
- Biomedical knowledge graphs
- Drug discovery datasets

**Tasks:**
- Predicting molecular properties (solubility, toxicity, activity)
- Protein function or structure prediction
- Drug-target binding prediction
- Generating new molecular structures
- Planning chemical synthesis routes
- Link prediction in biomedical knowledge bases
- Training graph neural networks on scientific data

**Libraries and Integration:**
- TorchDrug is the primary library
- Often used with RDKit for cheminformatics
- Compatible with PyTorch and PyTorch Lightning
- Integrates with AlphaFold and ESM for proteins

## Getting Started

### Installation

```bash
uv pip install torchdrug
# Or with optional dependencies
uv pip install torchdrug[full]
```

### Quick Example

```python
from torchdrug import datasets, models, tasks
from torch.utils.data import DataLoader

# Load molecular dataset
dataset = datasets.BBBP("~/molecule-datasets/")
train_set, valid_set, test_set = dataset.split()

# Define GNN model
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True,
    readout="mean"
)

# Create property prediction task
task = tasks.PropertyPrediction(
    model,
    task=dataset.tasks,
    criterion="bce",
    metric=["auroc", "auprc"]
)

# Train with PyTorch
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

for epoch in range(100):
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## Core Capabilities

### 1. Molecular Property Prediction

Predict chemical, physical, and biological properties of molecules from structure.

**Use Cases:**
- Drug-likeness and ADMET properties
- Toxicity screening
- Quantum chemistry properties
- Binding affinity prediction

**Key Components:**
- 20+ molecular datasets (BBBP, HIV, Tox21, QM9, etc.)
- GNN models (GIN, GAT, SchNet)
- PropertyPrediction and MultipleBinaryClassification tasks

**Reference:** See `references/molecular_property_prediction.md` for:
- Complete dataset catalog
- Model selection guide
- Training workflows and best practices
- Feature engineering details

### 2. Protein Modeling

Work with protein sequences, structures, and properties.

**Use Cases:**
- Enzyme function prediction
- Protein stability and solubility
- Subcellular localization
- Protein-protein interactions
- Structure prediction

**Key Components:**
- 15+ protein datasets (EnzymeCommission, GeneOntology, PDBBind, etc.)
- Sequence models (ESM, ProteinBERT, ProteinLSTM)
- Structure models (GearNet, SchNet)
- Multiple task types for different prediction levels

**Reference:** See `references/protein_modeling.md` for:
- Protein-specific datasets
- Sequence vs structure models
- Pre-training strategies
- Integration with AlphaFold and ESM

### 3. Knowledge Graph Reasoning

Predict missing links and relationships in biological knowledge graphs.

**Use Cases:**
- Drug repurposing
- Disease mechanism discovery
- Gene-disease associations
- Multi-hop biomedical reasoning

**Key Components:**
- General KGs (FB15k, WN18) and biomedical (Hetionet)
- Embedding models (TransE, RotatE, ComplEx)
- KnowledgeGraphCompletion task

**Reference:** See `references/knowledge_graphs.md` for:
- Knowledge graph datasets (including Hetionet with 45k biomedical entities)
- Embedding model comparison
- Evaluation metrics and protocols
- Biomedical applications

### 4. Molecular Generation

Generate novel molecular structures with desired properties.

**Use Cases:**
- De novo drug design
- Lead optimization
- Chemical space exploration
- Property-guided generation

**Key Components:**
- Autoregressive generation
- GCPN (policy-based generation)
- GraphAutoregressiveFlow
- Property optimization workflows

**Reference:** See `references/molecular_generation.md` for:
- Generation strategies (unconditional, conditional, scaffold-based)
- Multi-objective optimization
- Validation and filtering
- Integration with property prediction

### 5. Retrosynthesis

Predict synthetic routes from target molecules to starting materials.

**Use Cases:**
- Synthesis planning
- Route optimization
- Synthetic accessibility assessment
- Multi-step planning

**Key Components:**
- USPTO-50k reaction dataset
- CenterIdentification (reaction center prediction)
- SynthonCompletion (reactant prediction)
- End-to-end Retrosynthesis pipeline

**Reference:** See `references/retrosynthesis.md` for:
- Task decomposition (center ID → synthon completion)
- Multi-step synthesis planning
- Commercial availability checking
- Integration with other retrosynthesis tools

### 6. Graph Neural Network Models

Comprehensive catalog of GNN architectures for different data types and tasks.

**Available Models:**
- General GNNs: GCN, GAT, GIN, RGCN, MPNN
- 3D-aware: SchNet, GearNet
- Protein-specific: ESM, ProteinBERT, GearNet
- Knowledge graph: TransE, RotatE, ComplEx, SimplE
- Generative: GraphAutoregressiveFlow

**Reference:** See `references/models_architectures.md` for:
- Detailed model descriptions
- Model selection guide by task and dataset
- Architecture comparisons
- Implementation tips

### 7. Datasets

40+ curated datasets spanning chemistry, biology, and knowledge graphs.

**Categories:**
- Molecular properties (drug discovery, quantum chemistry)
- Protein properties (function, structure, interactions)
- Knowledge graphs (general and biomedical)
- Retrosynthesis reactions

**Reference:** See `references/datasets.md` for:
- Complete dataset catalog with sizes and tasks
- Dataset selection guide
- Loading and preprocessing
- Splitting strategies (random, scaffold)

## Common Workflows

### Workflow 1: Molecular Property Prediction

**Scenario:** Predict blood-brain barrier penetration for drug candidates.

**Steps:**
1. Load dataset: `datasets.BBBP()`
2. Choose model: GIN for molecular graphs
3. Define task: `PropertyPrediction` with binary classification
4. Train with scaffold split for realistic evaluation
5. Evaluate using AUROC and AUPRC

**Navigation:** `references/molecular_property_prediction.md` → Dataset selection → Model selection → Training

### Workflow 2: Protein Function Prediction

**Scenario:** Predict enzyme function from sequence.

**Steps:**
1. Load dataset: `datasets.EnzymeCommission()`
2. Choose model: ESM (pre-trained) or GearNet (with structure)
3. Define task: `PropertyPrediction` with multi-class classification
4. Fine-tune pre-trained model or train from scratch
5. Evaluate using accuracy and per-class metrics

**Navigation:** `references/protein_modeling.md` → Model selection (sequence vs structure) → Pre-training strategies

### Workflow 3: Drug Repurposing via Knowledge Graphs

**Scenario:** Find new disease treatments in Hetionet.

**Steps:**
1. Load dataset: `datasets.Hetionet()`
2. Choose model: RotatE or ComplEx
3. Define task: `KnowledgeGraphCompletion`
4. Train with negative sampling
5. Query for "Compound-treats-Disease" predictions
6. Filter by plausibility and mechanism

**Navigation:** `references/knowledge_graphs.md` → Hetionet dataset → Model selection → Biomedical applications

### Workflow 4: De Novo Molecule Generation

**Scenario:** Generate drug-like molecules optimized for target binding.

**Steps:**
1. Train property predictor on activity data
2. Choose generation approach: GCPN for RL-based optimization
3. Define reward function combining affinity, drug-likeness, synthesizability
4. Generate candidates with property constraints
5. Validate chemistry and filter by drug-likeness
6. Rank by multi-objective scoring

**Navigation:** `references/molecular_generation.md` → Conditional generation → Multi-objective optimization

### Workflow 5: Retrosynthesis Planning

**Scenario:** Plan synthesis route for target molecule.

**Steps:**
1. Load dataset: `datasets.USPTO50k()`
2. Train center identification model (RGCN)
3. Train synthon completion model (GIN)
4. Combine into end-to-end retrosynthesis pipeline
5. Apply recursively for multi-step planning
6. Check commercial availability of building blocks

**Navigation:** `references/retrosynthesis.md` → Task types → Multi-step planning

## Integration Patterns

### With RDKit

Convert between TorchDrug molecules and RDKit:
```python
from torchdrug import data
from rdkit import Chem

# SMILES → TorchDrug molecule
smiles = "CCO"
mol = data.Molecule.from_smiles(smiles)

# TorchDrug → RDKit
rdkit_mol = mol.to_molecule()

# RDKit → TorchDrug
rdkit_mol = Chem.MolFromSmiles(smiles)
mol = data.Molecule.from_molecule(rdkit_mol)
```

### With AlphaFold/ESM

Use predicted structures:
```python
from torchdrug import data

# Load AlphaFold predicted structure
protein = data.Protein.from_pdb("AF-P12345-F1-model_v4.pdb")

# Build graph with spatial edges
graph = protein.residue_graph(
    node_position="ca",
    edge_types=["sequential", "radius"],
    radius_cutoff=10.0
)
```

### With PyTorch Lightning

Wrap tasks for Lightning training:
```python
import pytorch_lightning as pl

class LightningTask(pl.LightningModule):
    def __init__(self, torchdrug_task):
        super().__init__()
        self.task = torchdrug_task

    def training_step(self, batch, batch_idx):
        return self.task(batch)

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## Technical Details

For deep dives into TorchDrug's architecture:

**Core Concepts:** See `references/core_concepts.md` for:
- Architecture philosophy (modular, configurable)
- Data structures (Graph, Molecule, Protein, PackedGraph)
- Model interface and forward function signature
- Task interface (predict, target, forward, evaluate)
- Training workflows and best practices
- Loss functions and metrics
- Common pitfalls and debugging

## Quick Reference Cheat Sheet

**Choose Dataset:**
- Molecular property → `references/datasets.md` → Molecular section
- Protein task → `references/datasets.md` → Protein section
- Knowledge graph → `references/datasets.md` → Knowledge graph section

**Choose Model:**
- Molecules → `references/models_architectures.md` → GNN section → GIN/GAT/SchNet
- Proteins (sequence) → `references/models_architectures.md` → Protein section → ESM
- Proteins (structure) → `references/models_architectures.md` → Protein section → GearNet
- Knowledge graph → `references/models_architectures.md` → KG section → RotatE/ComplEx

**Common Tasks:**
- Property prediction → `references/molecular_property_prediction.md` or `references/protein_modeling.md`
- Generation → `references/molecular_generation.md`
- Retrosynthesis → `references/retrosynthesis.md`
- KG reasoning → `references/knowledge_graphs.md`

**Understand Architecture:**
- Data structures → `references/core_concepts.md` → Data Structures
- Model design → `references/core_concepts.md` → Model Interface
- Task design → `references/core_concepts.md` → Task Interface

## Troubleshooting Common Issues

**Issue: Dimension mismatch errors**
→ Check `model.input_dim` matches `dataset.node_feature_dim`
→ See `references/core_concepts.md` → Essential Attributes

**Issue: Poor performance on molecular tasks**
→ Use scaffold splitting, not random
→ Try GIN instead of GCN
→ See `references/molecular_property_prediction.md` → Best Practices

**Issue: Protein model not learning**
→ Use pre-trained ESM for sequence tasks
→ Check edge construction for structure models
→ See `references/protein_modeling.md` → Training Workflows

**Issue: Memory errors with large graphs**
→ Reduce batch size
→ Use gradient accumulation
→ See `references/core_concepts.md` → Memory Efficiency

**Issue: Generated molecules are invalid**
→ Add validity constraints
→ Post-process with RDKit validation
→ See `references/molecular_generation.md` → Validation and Filtering

## Resources

**Official Documentation:** https://torchdrug.ai/docs/
**GitHub:** https://github.com/DeepGraphLearning/torchdrug
**Paper:** TorchDrug: A Powerful and Flexible Machine Learning Platform for Drug Discovery

## Summary

Navigate to the appropriate reference file based on your task:

1. **Molecular property prediction** → `molecular_property_prediction.md`
2. **Protein modeling** → `protein_modeling.md`
3. **Knowledge graphs** → `knowledge_graphs.md`
4. **Molecular generation** → `molecular_generation.md`
5. **Retrosynthesis** → `retrosynthesis.md`
6. **Model selection** → `models_architectures.md`
7. **Dataset selection** → `datasets.md`
8. **Technical details** → `core_concepts.md`

Each reference provides comprehensive coverage of its domain with examples, best practices, and common use cases.

---

## Reference: Core_Concepts

# Core Concepts and Technical Details

## Overview

This reference covers TorchDrug's fundamental architecture, design principles, and technical implementation details.

## Architecture Philosophy

### Modular Design

TorchDrug separates concerns into distinct modules:

1. **Representation Models** (models.py): Encode graphs into embeddings
2. **Task Definitions** (tasks.py): Define learning objectives and evaluation
3. **Data Handling** (data.py, datasets.py): Graph structures and datasets
4. **Core Components** (core.py): Base classes and utilities

**Benefits:**
- Reuse representations across tasks
- Mix and match components
- Easy experimentation and prototyping
- Clear separation of concerns

### Configurable System

All components inherit from `core.Configurable`:
- Serialize to configuration dictionaries
- Reconstruct from configurations
- Save and load complete pipelines
- Reproducible experiments

## Core Components

### core.Configurable

Base class for all TorchDrug components.

**Key Methods:**
- `config_dict()`: Serialize to dictionary
- `load_config_dict(config)`: Load from dictionary
- `save(file)`: Save to file
- `load(file)`: Load from file

**Example:**
```python
from torchdrug import core, models

model = models.GIN(input_dim=10, hidden_dims=[256, 256])

# Save configuration
config = model.config_dict()
# {'class': 'GIN', 'input_dim': 10, 'hidden_dims': [256, 256], ...}

# Reconstruct model
model2 = core.Configurable.load_config_dict(config)
```

### core.Registry

Decorator for registering models, tasks, and datasets.

**Usage:**
```python
from torchdrug import core as core_td

@core_td.register("models.CustomModel")
class CustomModel(nn.Module, core_td.Configurable):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, hidden_dim)

    def forward(self, graph, input, all_loss, metric):
        # Model implementation
        pass
```

**Benefits:**
- Models automatically serializable
- String-based model specification
- Easy model lookup and instantiation

## Data Structures

### Graph

Core data structure representing molecular or protein graphs.

**Attributes:**
- `num_node`: Number of nodes
- `num_edge`: Number of edges
- `node_feature`: Node feature tensor [num_node, feature_dim]
- `edge_feature`: Edge feature tensor [num_edge, feature_dim]
- `edge_list`: Edge connectivity [num_edge, 2 or 3]
- `num_relation`: Number of edge types (for multi-relational)

**Methods:**
- `node_mask(mask)`: Select subset of nodes
- `edge_mask(mask)`: Select subset of edges
- `undirected()`: Make graph undirected
- `directed()`: Make graph directed

**Batching:**
- Graphs batched into single disconnected graph
- Automatic batching in DataLoader
- Preserves node/edge indices per graph

### Molecule (extends Graph)

Specialized graph for molecules.

**Additional Attributes:**
- `atom_type`: Atomic numbers
- `bond_type`: Bond types (single, double, triple, aromatic)
- `formal_charge`: Atomic formal charges
- `explicit_hs`: Explicit hydrogen counts

**Methods:**
- `from_smiles(smiles)`: Create from SMILES string
- `from_molecule(mol)`: Create from RDKit molecule
- `to_smiles()`: Convert to SMILES
- `to_molecule()`: Convert to RDKit molecule
- `ion_to_molecule()`: Neutralize charges

**Example:**
```python
from torchdrug import data

# From SMILES
mol = data.Molecule.from_smiles("CCO")

# Atom features
print(mol.atom_type)  # [6, 6, 8] (C, C, O)
print(mol.bond_type)  # [1, 1] (single bonds)
```

### Protein (extends Graph)

Specialized graph for proteins.

**Additional Attributes:**
- `residue_type`: Amino acid types
- `atom_name`: Atom names (CA, CB, etc.)
- `atom_type`: Atomic numbers
- `residue_number`: Residue numbering
- `chain_id`: Chain identifiers

**Methods:**
- `from_pdb(pdb_file)`: Load from PDB file
- `from_sequence(sequence)`: Create from sequence
- `to_pdb(pdb_file)`: Save to PDB file

**Graph Construction:**
- Nodes typically represent residues (not atoms)
- Edges can be sequential, spatial (KNN), or contact-based
- Configurable edge construction strategies

**Example:**
```python
from torchdrug import data

# Load protein
protein = data.Protein.from_pdb("1a3x.pdb")

# Build graph with multiple edge types
graph = protein.residue_graph(
    node_position="ca",  # Use Cα positions
    edge_types=["sequential", "radius"]  # Sequential + spatial edges
)
```

### PackedGraph

Efficient batching structure for heterogeneous graphs.

**Purpose:**
- Batch graphs of different sizes
- Single GPU memory allocation
- Efficient parallel processing

**Attributes:**
- `num_nodes`: List of node counts per graph
- `num_edges`: List of edge counts per graph
- `graph_ind`: Graph index for each node

**Use Cases:**
- Automatic in DataLoader
- Custom batching strategies
- Multi-graph operations

## Model Interface

### Forward Function Signature

All TorchDrug models follow a standardized interface:

```python
def forward(self, graph, input, all_loss=None, metric=None):
    """
    Args:
        graph (Graph): Batch of graphs
        input (Tensor): Node input features
        all_loss (Tensor, optional): Accumulator for losses
        metric (dict, optional): Dictionary for metrics

    Returns:
        dict: Output dictionary with representation keys
    """
    # Model computation
    output = self.layers(graph, input)

    return {
        "node_feature": output,
        "graph_feature": graph_pooling(output)
    }
```

**Key Points:**
- `graph`: Batched graph structure
- `input`: Node features [num_node, input_dim]
- `all_loss`: Accumulated loss (for multi-task)
- `metric`: Shared metric dictionary
- Returns dict with representation types

### Essential Attributes

**All models must define:**
- `input_dim`: Expected input feature dimension
- `output_dim`: Output representation dimension

**Purpose:**
- Automatic dimension checking
- Compose models in pipelines
- Error checking and validation

**Example:**
```python
class CustomModel(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = hidden_dim
        # ... layers ...
```

## Task Interface

### Core Task Methods

All tasks implement these methods:

```python
class CustomTask(tasks.Task):
    def preprocess(self, train_set, valid_set, test_set):
        """Dataset-specific preprocessing (optional)"""
        pass

    def predict(self, batch):
        """Generate predictions for a batch"""
        graph, label = batch
        output = self.model(graph, graph.node_feature)
        pred = self.mlp(output["graph_feature"])
        return pred

    def target(self, batch):
        """Extract ground truth labels"""
        graph, label = batch
        return label

    def forward(self, batch):
        """Compute training loss"""
        pred = self.predict(batch)
        target = self.target(batch)
        loss = self.criterion(pred, target)
        return loss

    def evaluate(self, pred, target):
        """Compute evaluation metrics"""
        metrics = {}
        metrics["auroc"] = compute_auroc(pred, target)
        metrics["auprc"] = compute_auprc(pred, target)
        return metrics
```

### Task Components

**Typical Task Structure:**
1. **Representation Model**: Encodes graph to embeddings
2. **Readout/Prediction Head**: Maps embeddings to predictions
3. **Loss Function**: Training objective
4. **Metrics**: Evaluation measures

**Example:**
```python
from torchdrug import tasks, models

# Representation model
model = models.GIN(input_dim=10, hidden_dims=[256, 256])

# Task wraps model with prediction head
task = tasks.PropertyPrediction(
    model=model,
    task=["task1", "task2"],  # Multi-task
    criterion="bce",
    metric=["auroc", "auprc"],
    num_mlp_layer=2
)
```

## Training Workflow

### Standard Training Loop

```python
import torch
from torch.utils.data import DataLoader
from torchdrug import core, models, tasks, datasets

# 1. Load dataset
dataset = datasets.BBBP("~/datasets/")
train_set, valid_set, test_set = dataset.split()

# 2. Create data loaders
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_set, batch_size=32)

# 3. Define model and task
model = models.GIN(input_dim=dataset.node_feature_dim,
                   hidden_dims=[256, 256, 256])
task = tasks.PropertyPrediction(model, task=dataset.tasks,
                                 criterion="bce", metric=["auroc", "auprc"])

# 4. Setup optimizer
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)

# 5. Training loop
for epoch in range(100):
    # Train
    task.train()
    for batch in train_loader:
        loss = task(batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Validate
    task.eval()
    preds, targets = [], []
    for batch in valid_loader:
        pred = task.predict(batch)
        target = task.target(batch)
        preds.append(pred)
        targets.append(target)

    preds = torch.cat(preds)
    targets = torch.cat(targets)
    metrics = task.evaluate(preds, targets)
    print(f"Epoch {epoch}: {metrics}")
```

### PyTorch Lightning Integration

TorchDrug tasks are compatible with PyTorch Lightning:

```python
import pytorch_lightning as pl

class LightningWrapper(pl.LightningModule):
    def __init__(self, task):
        super().__init__()
        self.task = task

    def training_step(self, batch, batch_idx):
        loss = self.task(batch)
        return loss

    def validation_step(self, batch, batch_idx):
        pred = self.task.predict(batch)
        target = self.task.target(batch)
        return {"pred": pred, "target": target}

    def validation_epoch_end(self, outputs):
        preds = torch.cat([o["pred"] for o in outputs])
        targets = torch.cat([o["target"] for o in outputs])
        metrics = self.task.evaluate(preds, targets)
        self.log_dict(metrics)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
```

## Loss Functions

### Built-in Criteria

**Classification:**
- `"bce"`: Binary cross-entropy
- `"ce"`: Cross-entropy (multi-class)

**Regression:**
- `"mse"`: Mean squared error
- `"mae"`: Mean absolute error

**Knowledge Graph:**
- `"bce"`: Binary classification of triples
- `"ce"`: Cross-entropy ranking loss
- `"margin"`: Margin-based ranking

### Custom Loss

```python
class CustomTask(tasks.Task):
    def forward(self, batch):
        pred = self.predict(batch)
        target = self.target(batch)

        # Custom loss computation
        loss = custom_loss_function(pred, target)

        return loss
```

## Metrics

### Common Metrics

**Classification:**
- **AUROC**: Area under ROC curve
- **AUPRC**: Area under precision-recall curve
- **Accuracy**: Overall accuracy
- **F1**: Harmonic mean of precision and recall

**Regression:**
- **MAE**: Mean absolute error
- **RMSE**: Root mean squared error
- **R²**: Coefficient of determination
- **Pearson**: Pearson correlation

**Ranking (Knowledge Graph):**
- **MR**: Mean rank
- **MRR**: Mean reciprocal rank
- **Hits@K**: Percentage in top K

### Multi-Task Metrics

For multi-label or multi-task:
- Metrics computed per task
- Macro-average across tasks
- Can weight by task importance

## Data Transforms

### Molecule Transforms

```python
from torchdrug import transforms

# Add virtual node connected to all atoms
transform1 = transforms.VirtualNode()

# Add virtual edges
transform2 = transforms.VirtualEdge()

# Compose transforms
transform = transforms.Compose([transform1, transform2])

dataset = datasets.BBBP("~/datasets/", transform=transform)
```

### Protein Transforms

```python
# Add edges based on spatial proximity
transform = transforms.TruncateProtein(max_length=500)

dataset = datasets.Fold("~/datasets/", transform=transform)
```

## Best Practices

### Memory Efficiency

1. **Gradient Accumulation**: For large models
2. **Mixed Precision**: FP16 training
3. **Batch Size Tuning**: Balance speed and memory
4. **Data Loading**: Multiple workers for I/O

### Reproducibility

1. **Set Seeds**: PyTorch, NumPy, Python random
2. **Deterministic Operations**: `torch.use_deterministic_algorithms(True)`
3. **Save Configurations**: Use `core.Configurable`
4. **Version Control**: Track TorchDrug version

### Debugging

1. **Check Dimensions**: Verify `input_dim` and `output_dim`
2. **Validate Batching**: Print batch statistics
3. **Monitor Gradients**: Watch for vanishing/exploding
4. **Overfit Small Batch**: Ensure model capacity

### Performance Optimization

1. **GPU Utilization**: Monitor with `nvidia-smi`
2. **Profile Code**: Use PyTorch profiler
3. **Optimize Data Loading**: Prefetch, pin memory
4. **Compile Models**: Use TorchScript if possible

## Advanced Topics

### Multi-Task Learning

Train single model on multiple related tasks:
```python
task = tasks.PropertyPrediction(
    model,
    task=["task1", "task2", "task3"],
    criterion="bce",
    metric=["auroc"],
    task_weight=[1.0, 1.0, 2.0]  # Weight task 3 more
)
```

### Transfer Learning

1. Pre-train on large dataset
2. Fine-tune on target dataset
3. Optionally freeze early layers

### Self-Supervised Pre-training

Use pre-training tasks:
- `AttributeMasking`: Mask node features
- `EdgePrediction`: Predict edge existence
- `ContextPrediction`: Contrastive learning

### Custom Layers

Extend TorchDrug with custom GNN layers:
```python
from torchdrug import layers

class CustomConv(layers.MessagePassingBase):
    def message(self, graph, input):
        # Custom message function
        pass

    def aggregate(self, graph, message):
        # Custom aggregation
        pass

    def combine(self, input, update):
        # Custom combination
        pass
```

## Common Pitfalls

1. **Forgetting `input_dim` and `output_dim`**: Models won't compose
2. **Not Batching Properly**: Use PackedGraph for variable-sized graphs
3. **Data Leakage**: Be careful with scaffold splits and pre-training
4. **Ignoring Edge Features**: Bonds/spatial info can be critical
5. **Wrong Evaluation Metrics**: Match metrics to task (AUROC for imbalanced)
6. **Insufficient Regularization**: Use dropout, weight decay, early stopping
7. **Not Validating Chemistry**: Generated molecules must be valid
8. **Overfitting Small Datasets**: Use pre-training or simpler models

---

## Reference: Datasets

# Datasets Reference

## Overview

TorchDrug provides 40+ curated datasets across multiple domains: molecular property prediction, protein modeling, knowledge graph reasoning, and retrosynthesis. All datasets support lazy loading, automatic downloading, and customizable feature extraction.

## Molecular Property Prediction Datasets

### Drug Discovery Classification

| Dataset | Size | Task | Classes | Description |
|---------|------|------|---------|-------------|
| **BACE** | 1,513 | Binary | 2 | β-secretase inhibition for Alzheimer's |
| **BBBP** | 2,039 | Binary | 2 | Blood-brain barrier penetration |
| **HIV** | 41,127 | Binary | 2 | Inhibition of HIV replication |
| **ClinTox** | 1,478 | Multi-label | 2 | Clinical trial toxicity |
| **SIDER** | 1,427 | Multi-label | 27 | Side effects by system organ class |
| **Tox21** | 7,831 | Multi-label | 12 | Toxicity across 12 targets |
| **ToxCast** | 8,576 | Multi-label | 617 | High-throughput toxicology |
| **MUV** | 93,087 | Multi-label | 17 | Unbiased validation for screening |

**Key Features:**
- All use scaffold splits for realistic evaluation
- Binary classification metrics: AUROC, AUPRC
- Multi-label handles missing values

**Use Cases:**
- Drug safety prediction
- Virtual screening
- ADMET property prediction

### Drug Discovery Regression

| Dataset | Size | Property | Units | Description |
|---------|------|----------|-------|-------------|
| **ESOL** | 1,128 | Solubility | log(mol/L) | Water solubility |
| **FreeSolv** | 642 | Hydration | kcal/mol | Hydration free energy |
| **Lipophilicity** | 4,200 | LogD | - | Octanol/water distribution |
| **SAMPL** | 643 | Solvation | kcal/mol | Solvation free energies |

**Metrics:** MAE, RMSE, R²
**Use Cases:** ADME optimization, lead optimization

### Quantum Chemistry

| Dataset | Size | Properties | Description |
|---------|------|------------|-------------|
| **QM7** | 7,165 | 1 | Atomization energy |
| **QM8** | 21,786 | 12 | Electronic spectra, excited states |
| **QM9** | 133,885 | 12 | Geometric, energetic, electronic, thermodynamic |
| **PCQM4M** | 3.8M | 1 | Large-scale HOMO-LUMO gap |

**Properties (QM9):**
- Dipole moment
- Isotropic polarizability
- HOMO/LUMO energies
- Internal energy, enthalpy, free energy
- Heat capacity
- Electronic spatial extent

**Use Cases:**
- Quantum property prediction
- Method development benchmarking
- Pre-training molecular models

### Large Molecule Databases

| Dataset | Size | Description | Use Case |
|---------|------|-------------|----------|
| **ZINC250k** | 250,000 | Drug-like molecules | Generative model training |
| **ZINC2M** | 2,000,000 | Drug-like molecules | Large-scale pre-training |
| **ChEMBL** | Millions | Bioactive molecules | Property prediction, generation |

## Protein Datasets

### Function Prediction

| Dataset | Size | Task | Classes | Description |
|---------|------|------|---------|-------------|
| **EnzymeCommission** | 17,562 | Multi-class | 7 levels | EC number classification |
| **GeneOntology** | 46,796 | Multi-label | 489 | GO term prediction (BP/MF/CC) |
| **BetaLactamase** | 5,864 | Regression | - | Enzyme activity levels |
| **Fluorescence** | 54,025 | Regression | - | GFP fluorescence intensity |
| **Stability** | 53,614 | Regression | - | Thermostability (ΔΔG) |

**Features:**
- Sequence and/or structure input
- Evolutionary information available
- Multiple train/test splits

**Use Cases:**
- Protein engineering
- Function annotation
- Enzyme design

### Localization and Solubility

| Dataset | Size | Task | Classes | Description |
|---------|------|------|---------|-------------|
| **Solubility** | 62,478 | Binary | 2 | Protein solubility |
| **BinaryLocalization** | 22,168 | Binary | 2 | Membrane vs soluble |
| **SubcellularLocalization** | 8,943 | Multi-class | 10 | Subcellular compartment |

**Use Cases:**
- Protein expression optimization
- Target identification
- Cell biology

### Structure Prediction

| Dataset | Size | Task | Description |
|---------|------|------|-------------|
| **Fold** | 16,712 | Multi-class (1,195) | Structural fold recognition |
| **SecondaryStructure** | 8,678 | Sequence labeling | 3-state or 8-state prediction |
| **ProteinNet** | Varied | Contact prediction | Residue-residue contacts |

**Use Cases:**
- Structure prediction pipelines
- Fold recognition
- Contact map generation

### Protein Interactions

| Dataset | Size | Positives | Negatives | Description |
|---------|------|-----------|-----------|-------------|
| **HumanPPI** | 1,412 proteins | 6,584 | - | Human protein interactions |
| **YeastPPI** | 2,018 proteins | 6,451 | - | Yeast protein interactions |
| **PPIAffinity** | 2,156 pairs | - | - | Binding affinity values |

**Use Cases:**
- PPI prediction
- Network biology
- Drug target identification

### Protein-Ligand Binding

| Dataset | Size | Type | Description |
|---------|------|------|-------------|
| **BindingDB** | ~1.5M | Affinity | Comprehensive binding data |
| **PDBBind** | 20,000+ | 3D complexes | Structure-based binding |
| - Refined Set | 5,316 | High quality | Curated crystal structures |
| - Core Set | 285 | Benchmark | Diverse test set |

**Use Cases:**
- Binding affinity prediction
- Structure-based drug design
- Scoring function development

### Large Protein Databases

| Dataset | Size | Description |
|---------|------|-------------|
| **AlphaFoldDB** | 200M+ | Predicted structures for most known proteins |
| **UniProt** | Integration | Sequence and annotation data |

## Knowledge Graph Datasets

### General Knowledge

| Dataset | Entities | Relations | Triples | Domain |
|---------|----------|-----------|---------|--------|
| **FB15k** | 14,951 | 1,345 | 592,213 | Freebase (general knowledge) |
| **FB15k-237** | 14,541 | 237 | 310,116 | Filtered Freebase |
| **WN18** | 40,943 | 18 | 151,442 | WordNet (lexical) |
| **WN18RR** | 40,943 | 11 | 93,003 | Filtered WordNet |

**Relation Types (FB15k-237):**
- `/people/person/nationality`
- `/film/film/genre`
- `/location/location/contains`
- `/business/company/founders`
- Many more...

**Use Cases:**
- Link prediction
- Relation extraction
- Knowledge base completion

### Biomedical Knowledge

| Dataset | Entities | Relations | Triples | Description |
|---------|----------|-----------|---------|-------------|
| **Hetionet** | 45,158 | 24 | 2,250,197 | Integrates 29 biomedical databases |

**Entity Types in Hetionet:**
- Genes (20,945)
- Compounds (1,552)
- Diseases (137)
- Anatomy (400)
- Pathways (1,822)
- Pharmacologic classes
- Side effects
- Symptoms
- Molecular functions
- Biological processes
- Cellular components

**Relation Types:**
- Compound-binds-Gene
- Gene-associates-Disease
- Disease-presents-Symptom
- Compound-treats-Disease
- Compound-causes-Side effect
- Gene-participates-Pathway
- And 18 more...

**Use Cases:**
- Drug repurposing
- Disease mechanism discovery
- Target identification
- Multi-hop reasoning in biomedicine

## Citation Network Datasets

| Dataset | Nodes | Edges | Classes | Description |
|---------|-------|-------|---------|-------------|
| **Cora** | 2,708 | 5,429 | 7 | Machine learning papers |
| **CiteSeer** | 3,327 | 4,732 | 6 | Computer science papers |
| **PubMed** | 19,717 | 44,338 | 3 | Biomedical papers |

**Use Cases:**
- Node classification
- GNN baseline comparisons
- Method development

## Retrosynthesis Datasets

| Dataset | Size | Description |
|---------|------|-------------|
| **USPTO-50k** | 50,017 | Curated patent reactions, single-step |

**Features:**
- Product → Reactants mapping
- Atom mapping for reaction centers
- Canonicalized SMILES
- Balanced across reaction types

**Splits:**
- Train: ~40,000
- Validation: ~5,000
- Test: ~5,000

**Use Cases:**
- Retrosynthesis prediction
- Reaction type classification
- Synthetic route planning

## Dataset Usage Patterns

### Loading Datasets

```python
from torchdrug import datasets

# Basic loading
dataset = datasets.BBBP("~/molecule-datasets/")

# With transforms
from torchdrug import transforms
transform = transforms.VirtualNode()
dataset = datasets.BBBP("~/molecule-datasets/", transform=transform)

# Protein dataset
dataset = datasets.EnzymeCommission("~/protein-datasets/")

# Knowledge graph
dataset = datasets.FB15k237("~/kg-datasets/")
```

### Data Splitting

```python
# Random split
train, valid, test = dataset.split([0.8, 0.1, 0.1])

# Scaffold split (for molecules)
from torchdrug import utils
train, valid, test = dataset.split(
    utils.scaffold_split(dataset, [0.8, 0.1, 0.1])
)

# Predefined splits (some datasets)
train, valid, test = dataset.split()
```

### Feature Extraction

**Node Features (Molecules):**
- Atom type (one-hot or embedding)
- Formal charge
- Hybridization
- Aromaticity
- Number of hydrogens
- Chirality

**Edge Features (Molecules):**
- Bond type (single, double, triple, aromatic)
- Stereochemistry
- Conjugation
- Ring membership

**Node Features (Proteins):**
- Amino acid type (one-hot)
- Physicochemical properties
- Position in sequence
- Secondary structure
- Solvent accessibility

**Edge Features (Proteins):**
- Edge type (sequential, spatial, contact)
- Distance
- Angles and dihedrals

## Choosing Datasets

### By Task

**Molecular Property Prediction:**
- Start with BBBP or HIV (medium size, clear task)
- Use QM9 for quantum properties
- ESOL/FreeSolv for regression

**Protein Function:**
- EnzymeCommission (well-defined classes)
- GeneOntology (comprehensive annotations)

**Drug Safety:**
- Tox21 (standard benchmark)
- ClinTox (clinical relevance)

**Structure-Based:**
- PDBBind (protein-ligand)
- ProteinNet (structure prediction)

**Knowledge Graph:**
- FB15k-237 (standard benchmark)
- Hetionet (biomedical applications)

**Generation:**
- ZINC250k (training)
- QM9 (with properties)

**Retrosynthesis:**
- USPTO-50k (only choice)

### By Size and Resources

**Small (<5k, for testing):**
- BACE, FreeSolv, ClinTox
- Core set of PDBBind

**Medium (5k-100k):**
- BBBP, HIV, ESOL, Tox21
- EnzymeCommission, Fold
- FB15k-237, WN18RR

**Large (>100k):**
- QM9, MUV, PCQM4M
- GeneOntology, AlphaFoldDB
- ZINC2M, BindingDB

### By Domain

**Drug Discovery:** BBBP, HIV, Tox21, ESOL, ZINC
**Quantum Chemistry:** QM7, QM8, QM9, PCQM4M
**Protein Engineering:** Fluorescence, Stability, Solubility
**Structural Biology:** Fold, PDBBind, ProteinNet, AlphaFoldDB
**Biomedical:** Hetionet, GeneOntology, EnzymeCommission
**Retrosynthesis:** USPTO-50k

## Best Practices

1. **Start Small**: Test on small datasets before scaling
2. **Scaffold Split**: Use for realistic drug discovery evaluation
3. **Balanced Metrics**: Use AUROC + AUPRC for imbalanced data
4. **Multiple Runs**: Report mean ± std over multiple random seeds
5. **Data Leakage**: Be careful with pre-trained models
6. **Domain Knowledge**: Understand what you're predicting
7. **Validation**: Always use held-out test set
8. **Preprocessing**: Standardize features, handle missing values

---

## Reference: Knowledge_Graphs

# Knowledge Graph Reasoning

## Overview

Knowledge graphs represent structured information as entities and relations in a graph format. TorchDrug provides comprehensive support for knowledge graph completion (link prediction) using embedding-based models and neural reasoning approaches.

## Available Datasets

### General Knowledge Graphs

**FB15k (Freebase subset):**
- 14,951 entities
- 1,345 relation types
- 592,213 triples
- General world knowledge from Freebase

**FB15k-237:**
- 14,541 entities
- 237 relation types
- 310,116 triples
- Filtered version removing inverse relations
- More challenging benchmark

**WN18 (WordNet):**
- 40,943 entities (word senses)
- 18 relation types (lexical relations)
- 151,442 triples
- Linguistic knowledge graph

**WN18RR:**
- 40,943 entities
- 11 relation types
- 93,003 triples
- Filtered WordNet removing easy inverse patterns

### Biomedical Knowledge Graphs

**Hetionet:**
- 45,158 entities (genes, compounds, diseases, pathways, etc.)
- 24 relation types (treats, causes, binds, etc.)
- 2,250,197 edges
- Integrates 29 public biomedical databases
- Designed for drug repurposing and disease understanding

## Task: KnowledgeGraphCompletion

The primary task for knowledge graphs is link prediction - given a head entity and relation, predict the tail entity (or vice versa).

### Task Modes

**Head Prediction:**
- Given (?, relation, tail), predict head entity
- "What can cause Disease X?"

**Tail Prediction:**
- Given (head, relation, ?), predict tail entity
- "What diseases does Gene X cause?"

**Both:**
- Predict both head and tail
- Standard evaluation protocol

### Evaluation Metrics

**Ranking Metrics:**
- **Mean Rank (MR)**: Average rank of correct entity
- **Mean Reciprocal Rank (MRR)**: Average of 1/rank
- **Hits@K**: Percentage of correct entities in top K predictions
  - Typically reported for K=1, 3, 10

**Filtered vs Raw:**
- **Filtered**: Remove other known true triples from ranking
- **Raw**: Rank among all possible entities
- Filtered is standard for evaluation

## Embedding Models

### Translational Models

**TransE (Translation Embedding):**
- Represents relations as translations in embedding space
- h + r ≈ t (head + relation ≈ tail)
- Simple and effective baseline
- Works well for 1-to-1 relations
- Struggles with N-to-N relations

**RotatE (Rotation Embedding):**
- Relations as rotations in complex space
- Better handles symmetric and inverse relations
- State-of-the-art on many benchmarks
- Can model composition patterns

### Semantic Matching Models

**DistMult:**
- Bilinear scoring function
- Handles symmetric relations naturally
- Cannot model asymmetric relations
- Fast and memory efficient

**ComplEx:**
- Complex-valued embeddings
- Models asymmetric and inverse relations
- Better than DistMult for most graphs
- Balances expressiveness and efficiency

**SimplE:**
- Extends DistMult with inverse relations
- Fully expressive (can represent any relation pattern)
- Two embeddings per entity (canonical and inverse)

### Neural Logic Models

**NeuralLP (Neural Logic Programming):**
- Learns logical rules through differentiable operations
- Interprets predictions via learned rules
- Good for sparse knowledge graphs
- Computationally more expensive

**KBGAT (Knowledge Base Graph Attention):**
- Graph attention networks for KG completion
- Learns entity representations from neighborhood
- Handles unseen entities through inductive learning
- Better for incomplete graphs

## Training Workflow

### Basic Pipeline

```python
from torchdrug import datasets, models, tasks, core

# Load dataset
dataset = datasets.FB15k237("~/kg-datasets/")

# Define model
model = models.RotatE(
    num_entity=dataset.num_entity,
    num_relation=dataset.num_relation,
    embedding_dim=2000,
    max_score=9
)

# Define task
task = tasks.KnowledgeGraphCompletion(
    model,
    num_negative=128,
    adversarial_temperature=2,
    criterion="bce"
)

# Train with PyTorch Lightning or custom loop
```

### Negative Sampling

**Strategies:**
- **Uniform**: Sample entities uniformly at random
- **Self-Adversarial**: Weight samples by current model's scores
- **Type-Constrained**: Sample only valid entity types for relation

**Parameters:**
- `num_negative`: Number of negative samples per positive triple
- `adversarial_temperature`: Temperature for self-adversarial weighting
- Higher temperature = more focus on hard negatives

### Loss Functions

**Binary Cross-Entropy (BCE):**
- Treats each triple independently
- Balanced classification between positive and negative

**Margin Loss:**
- Ensures positive scores higher than negative by margin
- `max(0, margin + score_neg - score_pos)`

**Logistic Loss:**
- Smooth version of margin loss
- Better gradient properties

## Model Selection Guide

### By Relation Patterns

**1-to-1 Relations:**
- TransE works well
- Any model will likely succeed

**1-to-N Relations:**
- DistMult, ComplEx, SimplE
- Avoid TransE

**N-to-1 Relations:**
- DistMult, ComplEx, SimplE
- Avoid TransE

**N-to-N Relations:**
- ComplEx, SimplE, RotatE
- Most challenging pattern

**Symmetric Relations:**
- DistMult, ComplEx
- RotatE with proper initialization

**Antisymmetric Relations:**
- ComplEx, SimplE, RotatE
- Avoid DistMult

**Inverse Relations:**
- ComplEx, SimplE, RotatE
- Important for bidirectional reasoning

**Composition:**
- RotatE (best)
- TransE (reasonable)
- Captures multi-hop paths

### By Dataset Characteristics

**Small Graphs (< 50k entities):**
- ComplEx or SimplE
- Lower embedding dimensions (200-500)

**Large Graphs (> 100k entities):**
- DistMult for efficiency
- RotatE for accuracy
- Higher dimensions (500-2000)

**Sparse Graphs:**
- NeuralLP (learns rules from limited data)
- Pre-train embeddings on larger graphs

**Dense, Complete Graphs:**
- Any embedding model works well
- Choose based on relation patterns

**Biomedical/Domain Graphs:**
- Consider type constraints in sampling
- Use domain-specific negative sampling
- Hetionet benefits from relation-specific models

## Advanced Techniques

### Multi-Hop Reasoning

Chain multiple relations to answer complex queries:
- "What drugs treat diseases caused by gene X?"
- Requires path-based or rule-based reasoning
- NeuralLP naturally supports this

### Temporal Knowledge Graphs

Extend to time-varying facts:
- Add temporal information to triples
- Predict future facts
- Requires temporal encoding in models

### Few-Shot Learning

Handle relations with few examples:
- Meta-learning approaches
- Transfer from related relations
- Important for emerging knowledge

### Inductive Learning

Generalize to unseen entities:
- KBGAT and other GNN-based methods
- Use entity features/descriptions
- Critical for evolving knowledge graphs

## Biomedical Applications

### Drug Repurposing

Predict "drug treats disease" links in Hetionet:
1. Train on known drug-disease associations
2. Predict new treatment candidates
3. Filter by mechanism (gene, pathway involvement)
4. Validate predictions experimentally

### Disease Gene Discovery

Identify genes associated with diseases:
1. Model gene-disease-pathway networks
2. Predict missing gene-disease links
3. Incorporate protein interactions, expression data
4. Prioritize candidates for validation

### Protein Function Prediction

Link proteins to biological processes:
1. Integrate protein interactions, GO terms
2. Predict missing GO annotations
3. Transfer function from similar proteins

## Common Issues and Solutions

**Issue: Poor performance on specific relation types**
- Solution: Analyze relation patterns, choose appropriate model, or use relation-specific models

**Issue: Overfitting on small graphs**
- Solution: Reduce embedding dimension, increase regularization, or use simpler models

**Issue: Slow training on large graphs**
- Solution: Reduce negative samples, use DistMult for efficiency, or implement mini-batch training

**Issue: Cannot handle new entities**
- Solution: Use inductive models (KBGAT), incorporate entity features, or pre-compute embeddings for new entities based on their neighbors

## Best Practices

1. Start with ComplEx or RotatE for most tasks
2. Use self-adversarial negative sampling
3. Tune embedding dimension (typically 500-2000)
4. Apply regularization to prevent overfitting
5. Use filtered evaluation metrics
6. Analyze performance per relation type
7. Consider relation-specific models for heterogeneous graphs
8. Validate predictions with domain experts

---

## Reference: Models_Architectures

# Models and Architectures

## Overview

TorchDrug provides a comprehensive collection of pre-built model architectures for various graph-based learning tasks. This reference catalogs all available models with their characteristics, use cases, and implementation details.

## Graph Neural Networks

### GCN (Graph Convolutional Network)

**Type:** Spatial message passing
**Paper:** Semi-Supervised Classification with Graph Convolutional Networks (Kipf & Welling, 2017)

**Characteristics:**
- Simple and efficient aggregation
- Normalized adjacency matrix convolution
- Works well for homophilic graphs
- Good baseline for many tasks

**Best For:**
- Initial experiments and baselines
- When computational efficiency is important
- Graphs with clear local structure

**Parameters:**
- `input_dim`: Node feature dimension
- `hidden_dims`: List of hidden layer dimensions
- `edge_input_dim`: Edge feature dimension (optional)
- `batch_norm`: Apply batch normalization
- `activation`: Activation function (relu, elu, etc.)
- `dropout`: Dropout rate

**Use Cases:**
- Molecular property prediction
- Citation network classification
- Social network analysis

### GAT (Graph Attention Network)

**Type:** Attention-based message passing
**Paper:** Graph Attention Networks (Veličković et al., 2018)

**Characteristics:**
- Learns attention weights for neighbors
- Different importance for different neighbors
- Multi-head attention for robustness
- Handles varying node degrees naturally

**Best For:**
- When neighbor importance varies
- Heterogeneous graphs
- Interpretable predictions

**Parameters:**
- `input_dim`, `hidden_dims`: Standard dimensions
- `num_heads`: Number of attention heads
- `negative_slope`: LeakyReLU slope
- `concat`: Concatenate or average multi-head outputs

**Use Cases:**
- Protein-protein interaction prediction
- Molecule generation with attention to reactive sites
- Knowledge graph reasoning with relation importance

### GIN (Graph Isomorphism Network)

**Type:** Maximally powerful message passing
**Paper:** How Powerful are Graph Neural Networks? (Xu et al., 2019)

**Characteristics:**
- Theoretically most expressive GNN architecture
- Injective aggregation function
- Can distinguish graph structures GCN cannot
- Often best performance on molecular tasks

**Best For:**
- Molecular property prediction (state-of-the-art)
- Tasks requiring structural discrimination
- Graph classification

**Parameters:**
- `input_dim`, `hidden_dims`: Standard dimensions
- `edge_input_dim`: Include edge features
- `batch_norm`: Typically use true
- `readout`: Graph pooling ("sum", "mean", "max")
- `eps`: Learnable or fixed epsilon

**Use Cases:**
- Drug property prediction (BBBP, HIV, etc.)
- Molecular generation
- Reaction prediction

### RGCN (Relational Graph Convolutional Network)

**Type:** Multi-relational message passing
**Paper:** Modeling Relational Data with Graph Convolutional Networks (Schlichtkrull et al., 2018)

**Characteristics:**
- Handles multiple edge/relation types
- Relation-specific weight matrices
- Basis decomposition for parameter efficiency
- Essential for knowledge graphs

**Best For:**
- Knowledge graph reasoning
- Heterogeneous molecular graphs
- Multi-relational data

**Parameters:**
- `num_relation`: Number of relation types
- `hidden_dims`: Layer dimensions
- `num_bases`: Basis decomposition (reduce parameters)

**Use Cases:**
- Knowledge graph completion
- Retrosynthesis (different bond types)
- Protein interaction networks

### MPNN (Message Passing Neural Network)

**Type:** General message passing framework
**Paper:** Neural Message Passing for Quantum Chemistry (Gilmer et al., 2017)

**Characteristics:**
- Flexible message and update functions
- Edge features in message computation
- GRU updates for node hidden states
- Set2Set readout for graph representation

**Best For:**
- Quantum chemistry predictions
- Tasks with important edge information
- When node states evolve over multiple iterations

**Parameters:**
- `input_dim`, `hidden_dim`: Feature dimensions
- `edge_input_dim`: Edge feature dimension
- `num_layer`: Message passing iterations
- `num_mlp_layer`: MLP layers in message function

**Use Cases:**
- QM9 quantum property prediction
- Molecular dynamics
- 3D conformation-aware tasks

### SchNet (Continuous-Filter Convolutional Network)

**Type:** 3D geometry-aware convolution
**Paper:** SchNet: A continuous-filter convolutional neural network (Schütt et al., 2017)

**Characteristics:**
- Operates on 3D atomic coordinates
- Continuous filter convolutions
- Rotation and translation invariant
- Excellent for quantum chemistry

**Best For:**
- 3D molecular structure tasks
- Quantum property prediction
- Protein structure analysis
- Energy and force prediction

**Parameters:**
- `input_dim`: Atom features
- `hidden_dims`: Layer dimensions
- `num_gaussian`: RBF basis functions for distances
- `cutoff`: Interaction cutoff distance

**Use Cases:**
- QM9 property prediction
- Molecular dynamics simulations
- Protein-ligand binding with structures
- Crystal property prediction

### ChebNet (Chebyshev Spectral CNN)

**Type:** Spectral convolution
**Paper:** Convolutional Neural Networks on Graphs (Defferrard et al., 2016)

**Characteristics:**
- Spectral graph convolution
- Chebyshev polynomial approximation
- Captures global graph structure
- Computationally efficient

**Best For:**
- Tasks requiring global information
- When graph Laplacian is informative
- Theoretical analysis

**Parameters:**
- `input_dim`, `hidden_dims`: Dimensions
- `num_cheb`: Order of Chebyshev polynomial

**Use Cases:**
- Citation network classification
- Brain network analysis
- Signal processing on graphs

### NFP (Neural Fingerprint)

**Type:** Molecular fingerprint learning
**Paper:** Convolutional Networks on Graphs for Learning Molecular Fingerprints (Duvenaud et al., 2015)

**Characteristics:**
- Learns differentiable molecular fingerprints
- Alternative to hand-crafted fingerprints (ECFP)
- Circular convolutions like ECFP
- Interpretable learned features

**Best For:**
- Molecular similarity learning
- Property prediction with limited data
- When interpretability is important

**Parameters:**
- `input_dim`, `output_dim`: Feature dimensions
- `hidden_dims`: Layer dimensions
- `num_layer`: Circular convolution depth

**Use Cases:**
- Virtual screening
- Molecular similarity search
- QSAR modeling

## Protein-Specific Models

### GearNet (Geometry-Aware Relational Graph Network)

**Type:** Protein structure encoder
**Paper:** Protein Representation Learning by Geometric Structure Pretraining (Zhang et al., 2023)

**Characteristics:**
- Incorporates 3D geometric information
- Multiple edge types (sequential, spatial, KNN)
- Designed specifically for proteins
- State-of-the-art on protein tasks

**Best For:**
- Protein structure prediction
- Protein function prediction
- Protein-protein interaction
- Any task with protein 3D structures

**Parameters:**
- `input_dim`: Residue features
- `hidden_dims`: Layer dimensions
- `num_relation`: Edge types (sequence, radius, KNN)
- `edge_input_dim`: Geometric features (distances, angles)
- `batch_norm`: Typically true

**Use Cases:**
- Enzyme function prediction (EnzymeCommission)
- Protein fold recognition
- Contact prediction
- Binding site identification

### ESM (Evolutionary Scale Modeling)

**Type:** Protein language model (transformer)
**Paper:** Biological structure and function emerge from scaling unsupervised learning (Rives et al., 2021)

**Characteristics:**
- Pre-trained on 250M+ protein sequences
- Captures evolutionary and structural information
- Transformer architecture
- Transfer learning for downstream tasks

**Best For:**
- Any sequence-based protein task
- When no structure available
- Transfer learning with limited data

**Variants:**
- ESM-1b: 650M parameters
- ESM-2: Multiple sizes (8M to 15B parameters)

**Use Cases:**
- Protein function prediction
- Variant effect prediction
- Protein design
- Structure prediction (ESMFold)

### ProteinBERT

**Type:** Masked language model for proteins

**Characteristics:**
- BERT-style pre-training
- Masked amino acid prediction
- Bidirectional context
- Good for sequence-based tasks

**Use Cases:**
- Function annotation
- Subcellular localization
- Stability prediction

### ProteinCNN / ProteinResNet

**Type:** Convolutional networks for sequences

**Characteristics:**
- 1D convolutions on sequences
- Local pattern recognition
- Faster than transformers
- Good for motif detection

**Use Cases:**
- Binding site prediction
- Secondary structure prediction
- Domain identification

### ProteinLSTM

**Type:** Recurrent network for sequences

**Characteristics:**
- Bidirectional LSTM
- Captures long-range dependencies
- Sequential processing
- Good baseline for sequence tasks

**Use Cases:**
- Order prediction
- Sequential annotation
- Time-series protein data

## Knowledge Graph Models

### TransE (Translation Embedding)

**Type:** Translation-based embedding
**Paper:** Translating Embeddings for Modeling Multi-relational Data (Bordes et al., 2013)

**Characteristics:**
- h + r ≈ t (head + relation ≈ tail)
- Simple and interpretable
- Works well for 1-to-1 relations
- Memory efficient

**Best For:**
- Large knowledge graphs
- Initial experiments
- Interpretable embeddings

**Parameters:**
- `num_entity`, `num_relation`: Graph size
- `embedding_dim`: Embedding dimensions (typically 50-500)

### RotatE (Rotation Embedding)

**Type:** Rotation in complex space
**Paper:** RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space (Sun et al., 2019)

**Characteristics:**
- Relations as rotations in complex space
- Handles symmetric, antisymmetric, inverse, composition
- State-of-the-art on many benchmarks

**Best For:**
- Most knowledge graph tasks
- Complex relation patterns
- When accuracy is critical

**Parameters:**
- `num_entity`, `num_relation`: Graph size
- `embedding_dim`: Must be even (complex embeddings)
- `max_score`: Score clipping value

### DistMult

**Type:** Bilinear model

**Characteristics:**
- Symmetric relation modeling
- Fast and efficient
- Cannot model antisymmetric relations

**Best For:**
- Symmetric relations (e.g., "similar to")
- When speed is critical
- Large-scale graphs

### ComplEx

**Type:** Complex-valued embeddings

**Characteristics:**
- Handles asymmetric and symmetric relations
- Better than DistMult for most graphs
- Good balance of expressiveness and efficiency

**Best For:**
- General knowledge graph completion
- Mixed relation types
- When RotatE is too complex

### SimplE

**Type:** Enhanced embedding model

**Characteristics:**
- Two embeddings per entity (canonical + inverse)
- Fully expressive
- Slightly more parameters than ComplEx

**Best For:**
- When full expressiveness needed
- Inverse relations are important

## Generative Models

### GraphAutoregressiveFlow

**Type:** Normalizing flow for molecules

**Characteristics:**
- Exact likelihood computation
- Invertible transformations
- Stable training (no adversarial)
- Conditional generation support

**Best For:**
- Molecular generation
- Density estimation
- Interpolation between molecules

**Parameters:**
- `input_dim`: Atom features
- `hidden_dims`: Coupling layers
- `num_flow`: Number of flow transformations

**Use Cases:**
- De novo drug design
- Chemical space exploration
- Property-targeted generation

## Pre-training Models

### InfoGraph

**Type:** Contrastive learning

**Characteristics:**
- Maximizes mutual information
- Graph-level and node-level contrast
- Unsupervised pre-training
- Good for small datasets

**Use Cases:**
- Pre-train molecular encoders
- Few-shot learning
- Transfer learning

### MultiviewContrast

**Type:** Multi-view contrastive learning for proteins

**Characteristics:**
- Contrasts different views of proteins
- Geometric pre-training
- Uses 3D structure information
- Excellent for protein models

**Use Cases:**
- Pre-train GearNet on protein structures
- Transfer to property prediction
- Limited labeled data scenarios

## Model Selection Guide

### By Task Type

**Molecular Property Prediction:**
1. GIN (first choice)
2. GAT (interpretability)
3. SchNet (3D available)

**Protein Tasks:**
1. ESM (sequence only)
2. GearNet (structure available)
3. ProteinBERT (sequence, lighter than ESM)

**Knowledge Graphs:**
1. RotatE (best performance)
2. ComplEx (good balance)
3. TransE (large graphs, efficiency)

**Molecular Generation:**
1. GraphAutoregressiveFlow (exact likelihood)
2. GCPN with GIN backbone (property optimization)

**Retrosynthesis:**
1. GIN (synthon completion)
2. RGCN (center identification with bond types)

### By Dataset Size

**Small (< 1k):**
- Use pre-trained models (ESM for proteins)
- Simpler architectures (GCN, ProteinCNN)
- Heavy regularization

**Medium (1k-100k):**
- GIN for molecules
- GAT for interpretability
- Standard training

**Large (> 100k):**
- Any model works
- Deeper architectures
- Can train from scratch

### By Computational Budget

**Low:**
- GCN (simplest)
- DistMult (KG)
- ProteinLSTM

**Medium:**
- GIN
- GAT
- ComplEx

**High:**
- ESM (large)
- SchNet (3D)
- RotatE with high dim

## Implementation Tips

1. **Start Simple**: Begin with GCN or GIN baseline
2. **Use Pre-trained**: ESM for proteins, InfoGraph for molecules
3. **Tune Depth**: 3-5 layers typically sufficient
4. **Batch Normalization**: Usually helps (except KG embeddings)
5. **Residual Connections**: Important for deep networks
6. **Readout Function**: "mean" usually works well
7. **Edge Features**: Include when available (bonds, distances)
8. **Regularization**: Dropout, weight decay, early stopping

---

## Reference: Molecular_Generation

# Molecular Generation

## Overview

Molecular generation involves creating novel molecular structures with desired properties. TorchDrug supports both unconditional generation (exploring chemical space) and conditional generation (optimizing for specific properties).

## Task Types

### AutoregressiveGeneration

Generates molecules step-by-step by sequentially adding atoms and bonds. This approach enables fine-grained control and property optimization during generation.

**Key Features:**
- Sequential atom-by-bond construction
- Supports property optimization during generation
- Can incorporate chemical validity constraints
- Enables multi-objective optimization

**Generation Strategies:**
1. **Beam Search**: Keep top-k candidates at each step
2. **Sampling**: Probabilistic selection for diversity
3. **Greedy**: Always select highest probability action

**Property Optimization:**
- Reward shaping based on desired properties
- Real-time constraint satisfaction
- Multi-objective balancing (e.g., potency + drug-likeness)

### GCPNGeneration (Graph Convolutional Policy Network)

Uses reinforcement learning to generate molecules optimized for specific properties.

**Components:**
1. **Policy Network**: Decides which action to take (add atom, add bond)
2. **Reward Function**: Evaluates generated molecule quality
3. **Training**: Reinforcement learning with policy gradient

**Advantages:**
- Direct optimization of non-differentiable objectives
- Can incorporate complex domain knowledge
- Balances exploration and exploitation

**Applications:**
- Drug design with specific targets
- Material discovery with property constraints
- Multi-objective molecular optimization

## Generative Models

### GraphAutoregressiveFlow

Normalizing flow model for molecular generation with exact likelihood computation.

**Architecture:**
- Coupling layers transform simple distribution to complex molecular distribution
- Invertible transformations enable density estimation
- Supports conditional generation

**Key Features:**
- Exact likelihood computation (vs. VAE's approximate likelihood)
- Stable training (vs. GAN's adversarial training)
- Efficient sampling through invertible transformations
- Can generate molecules with specified properties

**Training:**
- Maximum likelihood on molecule dataset
- Optional property prediction head for conditional generation
- Typically trained on ZINC or QM9

**Use Cases:**
- Generating diverse drug-like molecules
- Interpolation between known molecules
- Density estimation for molecular space

## Generation Workflows

### Unconditional Generation

Generate diverse molecules without specific property targets.

**Workflow:**
1. Train generative model on molecule dataset (e.g., ZINC250k)
2. Sample from learned distribution
3. Post-process for validity and uniqueness
4. Evaluate diversity metrics

**Evaluation Metrics:**
- **Validity**: Percentage of chemically valid molecules
- **Uniqueness**: Percentage of unique molecules among valid
- **Novelty**: Percentage not in training set
- **Diversity**: Internal diversity using fingerprint similarity

### Conditional Generation

Generate molecules optimized for specific properties.

**Property Targets:**
- **Drug-likeness**: LogP, QED, Lipinski's rule of five
- **Synthesizability**: SA score, retrosynthesis feasibility
- **Bioactivity**: Predicted IC50, binding affinity
- **ADMET**: Absorption, distribution, metabolism, excretion, toxicity
- **Multi-objective**: Balance multiple properties simultaneously

**Workflow:**
1. Define reward function combining property objectives
2. Train GCPN or condition flow model on properties
3. Generate molecules with desired property ranges
4. Validate generated molecules (in silico → wet lab)

### Scaffold-Based Generation

Generate molecules around a fixed scaffold or core structure.

**Applications:**
- Lead optimization keeping core pharmacophore
- R-group enumeration for SAR studies
- Fragment linking and growing

**Approaches:**
- Mask scaffold during training
- Condition generation on scaffold
- Post-generation grafting

### Fragment-Based Generation

Build molecules from validated fragments.

**Benefits:**
- Ensures drug-like substructures
- Reduces search space
- Incorporates medicinal chemistry knowledge

**Methods:**
- Fragment library as building blocks
- Vocabulary-based generation
- Fragment linking with learned linkers

## Property Optimization Strategies

### Single-Objective Optimization

Maximize or minimize a single property (e.g., binding affinity).

**Approach:**
- Define scalar reward function
- Use GCPN with RL training
- Generate and rank candidates

**Challenges:**
- May sacrifice other important properties
- Risk of adversarial examples (valid but non-drug-like)
- Need constraints on drug-likeness

### Multi-Objective Optimization

Balance multiple competing objectives (e.g., potency, selectivity, synthesizability).

**Weighting Approaches:**
- **Linear combination**: w1×prop1 + w2×prop2 + ...
- **Pareto optimization**: Find non-dominated solutions
- **Constraint satisfaction**: Threshold on secondary objectives

**Example Objectives:**
- High binding affinity (target)
- Low binding affinity (off-targets)
- High synthesizability (SA score)
- Drug-like properties (QED)
- Low molecular weight

**Workflow:**
```python
from torchdrug import tasks

# Define multi-objective reward
def reward_function(mol):
    affinity_score = predict_binding(mol)
    druglikeness = calculate_qed(mol)
    synthesizability = sa_score(mol)

    # Weighted combination
    reward = 0.5 * affinity_score + 0.3 * druglikeness + 0.2 * (1 - synthesizability)
    return reward

# GCPN task with custom reward
task = tasks.GCPNGeneration(
    model,
    reward_function=reward_function,
    criterion="ppo"  # Proximal policy optimization
)
```

### Constraint-Based Generation

Generate molecules satisfying hard constraints.

**Common Constraints:**
- Molecular weight range
- LogP range
- Number of rotatable bonds
- Ring count limits
- Substructure inclusion/exclusion
- Synthetic accessibility threshold

**Implementation:**
- Validity checking during generation
- Early stopping for invalid molecules
- Penalty terms in reward function

## Training Considerations

### Dataset Selection

**ZINC (Drug-like compounds):**
- ZINC250k: 250,000 compounds
- ZINC2M: 2 million compounds
- Pre-filtered for drug-likeness
- Good for drug discovery applications

**QM9 (Small organic molecules):**
- 133,885 molecules
- Includes quantum properties
- Good for property prediction models

**ChEMBL (Bioactive molecules):**
- Millions of bioactive compounds
- Activity data available
- Target-specific generation

**Custom Datasets:**
- Focus on specific chemical space
- Include expert knowledge
- Domain-specific constraints

### Data Augmentation

**SMILES Augmentation:**
- Generate multiple SMILES for same molecule
- Helps model learn canonical representations
- Improves robustness

**Graph Augmentation:**
- Random node/edge masking
- Subgraph sampling
- Motif substitution

### Model Architecture Choices

**For Small Molecules (<30 atoms):**
- Simpler architectures sufficient
- Faster training and generation
- GCN or GIN backbone

**For Drug-like Molecules:**
- Deeper architectures (4-6 layers)
- Attention mechanisms help
- Consider molecular fingerprints

**For Macrocycles/Polymers:**
- Handle larger graphs
- Ring closure mechanisms important
- Long-range dependencies

## Validation and Filtering

### In Silico Validation

**Chemical Validity:**
- Valence rules
- Aromaticity rules
- Charge neutrality
- Stable substructures

**Drug-likeness Filters:**
- Lipinski's rule of five
- Veber's rules
- PAINS filters (pan-assay interference compounds)
- BRENK filters (toxic/reactive substructures)

**Synthesizability:**
- SA score (synthetic accessibility)
- Retrosynthesis prediction
- Commercial availability of precursors

**Property Prediction:**
- ADMET properties
- Toxicity prediction
- Off-target binding
- Metabolic stability

### Ranking and Selection

**Criteria:**
1. Predicted target affinity
2. Drug-likeness score
3. Synthesizability
4. Novelty (dissimilarity to known actives)
5. Diversity (within generated set)
6. Predicted ADMET properties

**Selection Strategies:**
- Pareto frontier selection
- Weighted scoring
- Clustering and representative selection
- Active learning for wet lab validation

## Best Practices

1. **Start Simple**: Begin with unconditional generation, then add constraints
2. **Validate Chemistry**: Always check for valid molecules and drug-likeness
3. **Diverse Training Data**: Use large, diverse datasets for better generalization
4. **Multi-Objective**: Consider multiple properties from the start
5. **Iterative Refinement**: Generate → validate → retrain with feedback
6. **Domain Expert Review**: Consult medicinal chemists before synthesis
7. **Benchmark**: Compare against known actives and random samples
8. **Synthesizability**: Prioritize molecules that can actually be made
9. **Explainability**: Understand why model generates certain structures
10. **Wet Lab Validation**: Ultimately validate promising candidates experimentally

## Common Applications

### Drug Discovery
- Lead generation for novel targets
- Lead optimization around active scaffolds
- Bioisostere replacement
- Fragment elaboration

### Materials Science
- Polymer design with target properties
- Catalyst discovery
- Energy storage materials
- Photovoltaic materials

### Chemical Biology
- Probe molecule design
- Degrader (PROTAC) design
- Molecular glue discovery

## Integration with Other Tools

**Docking:**
- Generate molecules → Dock to target → Retrain with docking scores

**Retrosynthesis:**
- Filter generated molecules by synthetic accessibility
- Plan synthesis routes for top candidates

**Property Prediction:**
- Use trained property prediction models as reward functions
- Multi-task learning with generation and prediction

**Active Learning:**
- Generate candidates → Predict properties → Synthesize best → Retrain

---

## Reference: Molecular_Property_Prediction

# Molecular Property Prediction

## Overview

Molecular property prediction involves predicting chemical, physical, or biological properties of molecules from their structure. TorchDrug provides comprehensive support for both classification and regression tasks on molecular graphs.

## Available Datasets

### Drug Discovery Datasets

**Classification Tasks:**
- **BACE** (1,513 molecules): Binary classification for β-secretase inhibition
- **BBBP** (2,039 molecules): Blood-brain barrier penetration prediction
- **HIV** (41,127 molecules): Ability to inhibit HIV replication
- **Tox21** (7,831 molecules): Toxicity prediction across 12 targets
- **ToxCast** (8,576 molecules): Toxicology screening
- **ClinTox** (1,478 molecules): Clinical trial toxicity
- **SIDER** (1,427 molecules): Drug side effects (27 system organ classes)
- **MUV** (93,087 molecules): Maximum unbiased validation for virtual screening

**Regression Tasks:**
- **ESOL** (1,128 molecules): Water solubility prediction
- **FreeSolv** (642 molecules): Hydration free energy
- **Lipophilicity** (4,200 molecules): Octanol/water distribution coefficient
- **SAMPL** (643 molecules): Solvation free energies

### Large-Scale Datasets

- **QM7** (7,165 molecules): Quantum mechanical properties
- **QM8** (21,786 molecules): Electronic spectra and excited state properties
- **QM9** (133,885 molecules): Geometric, energetic, electronic, and thermodynamic properties
- **PCQM4M** (3,803,453 molecules): Large-scale quantum chemistry dataset
- **ZINC250k/2M** (250k/2M molecules): Drug-like compounds for generative modeling

## Task Types

### PropertyPrediction

Standard task for graph-level property prediction supporting both classification and regression.

**Key Parameters:**
- `model`: Graph representation model (GNN)
- `task`: "node", "edge", or "graph" level prediction
- `criterion`: Loss function ("mse", "bce", "ce")
- `metric`: Evaluation metrics ("mae", "rmse", "auroc", "auprc")
- `num_mlp_layer`: Number of MLP layers for readout

**Example Workflow:**
```python
import torch
from torchdrug import core, models, tasks, datasets

# Load dataset
dataset = datasets.BBBP("~/molecule-datasets/")

# Define model
model = models.GIN(input_dim=dataset.node_feature_dim,
                   hidden_dims=[256, 256, 256, 256],
                   edge_input_dim=dataset.edge_feature_dim,
                   batch_norm=True, readout="mean")

# Define task
task = tasks.PropertyPrediction(model, task=dataset.tasks,
                                 criterion="bce",
                                 metric=("auprc", "auroc"))
```

### MultipleBinaryClassification

Specialized task for multi-label scenarios where each molecule can have multiple binary labels (e.g., Tox21, SIDER).

**Key Features:**
- Handles missing labels gracefully
- Computes metrics per label and averaged
- Supports weighted loss for imbalanced datasets

## Model Selection

### Recommended Models by Task

**Small Molecules (< 1000 molecules):**
- GIN (Graph Isomorphism Network)
- SchNet (for 3D structures)

**Medium Datasets (1k-100k molecules):**
- GCN, GAT, or GIN
- NFP (Neural Fingerprint)
- MPNN (Message Passing Neural Network)

**Large Datasets (> 100k molecules):**
- Pre-trained models with fine-tuning
- InfoGraph or MultiviewContrast for self-supervised pre-training
- GIN with deeper architectures

**3D Structure Available:**
- SchNet (continuous-filter convolutions)
- GearNet (geometry-aware relational graph)

## Feature Engineering

### Node Features

TorchDrug automatically extracts atom features:
- Atom type
- Formal charge
- Explicit/implicit hydrogens
- Hybridization
- Aromaticity
- Chirality

### Edge Features

Bond features include:
- Bond type (single, double, triple, aromatic)
- Stereochemistry
- Conjugation
- Ring membership

### Custom Features

Add custom node/edge features using transforms:
```python
from torchdrug import data, transforms

# Add custom features
transform = transforms.VirtualNode()  # Add virtual node
dataset = datasets.BBBP("~/molecule-datasets/",
                        transform=transform)
```

## Training Workflow

### Basic Pipeline

1. **Load Dataset**: Choose appropriate dataset
2. **Split Data**: Use scaffold split for drug discovery
3. **Define Model**: Select GNN architecture
4. **Create Task**: Configure loss and metrics
5. **Setup Optimizer**: Adam typically works well
6. **Train**: Use PyTorch Lightning or custom loop

### Data Splitting Strategies

**Random Split**: Standard train/val/test split
**Scaffold Split**: Group molecules by Bemis-Murcko scaffolds (recommended for drug discovery)
**Stratified Split**: Maintain label distribution across splits

### Best Practices

- Use scaffold splitting for realistic drug discovery evaluation
- Apply data augmentation (virtual nodes, edges) for small datasets
- Monitor multiple metrics (AUROC, AUPRC for classification; MAE, RMSE for regression)
- Use early stopping based on validation performance
- Consider ensemble methods for critical applications
- Pre-train on large datasets before fine-tuning on small datasets

## Common Issues and Solutions

**Issue: Poor performance on imbalanced datasets**
- Solution: Use weighted loss, focal loss, or over/under-sampling

**Issue: Overfitting on small datasets**
- Solution: Increase regularization, use simpler models, apply data augmentation, or pre-train on larger datasets

**Issue: Large memory consumption**
- Solution: Reduce batch size, use gradient accumulation, or implement graph sampling

**Issue: Slow training**
- Solution: Use GPU acceleration, optimize data loading with multiple workers, or use mixed precision training

---

## Reference: Protein_Modeling

# Protein Modeling

## Overview

TorchDrug provides extensive support for protein-related tasks including sequence analysis, structure prediction, property prediction, and protein-protein interactions. Proteins are represented as graphs where nodes are amino acid residues and edges represent spatial or sequential relationships.

## Available Datasets

### Protein Function Prediction

**Enzyme Function:**
- **EnzymeCommission** (17,562 proteins): EC number classification (7 levels)
- **BetaLactamase** (5,864 sequences): Enzyme activity prediction

**Protein Characteristics:**
- **Fluorescence** (54,025 sequences): GFP fluorescence intensity
- **Stability** (53,614 sequences): Thermostability prediction
- **Solubility** (62,478 sequences): Protein solubility classification
- **BinaryLocalization** (22,168 proteins): Subcellular localization (membrane vs. soluble)
- **SubcellularLocalization** (8,943 proteins): 10-class localization prediction

**Gene Ontology:**
- **GeneOntology** (46,796 proteins): GO term prediction across biological process, molecular function, and cellular component

### Protein Structure Prediction

- **Fold** (16,712 proteins): Structural fold classification (1,195 classes)
- **SecondaryStructure** (8,678 proteins): 3-state or 8-state secondary structure prediction
- **ContactPrediction** via ProteinNet: Residue-residue contact maps

### Protein Interaction

**Protein-Protein Interactions:**
- **HumanPPI** (1,412 proteins, 6,584 interactions): Human protein interaction network
- **YeastPPI** (2,018 proteins, 6,451 interactions): Yeast protein interaction network
- **PPIAffinity** (2,156 protein pairs): Binding affinity measurements

**Protein-Ligand Binding:**
- **BindingDB** (~1.5M entries): Comprehensive binding affinity database
- **PDBBind** (20,000+ complexes): 3D structure-based binding data
  - Refined set: High-quality crystal structures
  - Core set: Diverse benchmark set

### Large-Scale Protein Databases

- **AlphaFoldDB**: Access to 200M+ predicted protein structures
- **ProteinNet**: Standardized dataset for structure prediction

## Task Types

### NodePropertyPrediction

Predict properties at the residue (node) level, such as secondary structure or contact maps.

**Use Cases:**
- Secondary structure prediction (helix, sheet, coil)
- Residue-level disorder prediction
- Post-translational modification sites
- Binding site prediction

### PropertyPrediction

Predict protein-level properties like function, stability, or localization.

**Use Cases:**
- Enzyme function classification
- Subcellular localization
- Protein stability prediction
- Gene ontology term prediction

### InteractionPrediction

Predict interactions between protein pairs or protein-ligand pairs.

**Key Features:**
- Handles both sequence and structure inputs
- Supports symmetric (PPI) and asymmetric (protein-ligand) interactions
- Multiple negative sampling strategies

### ContactPrediction

Specialized task for predicting spatial proximity between residues in folded structures.

**Applications:**
- Structure prediction from sequence
- Protein folding pathway analysis
- Validation of predicted structures

## Protein Representation Models

### Sequence-Based Models

**ESM (Evolutionary Scale Modeling):**
- Pre-trained transformer model on 250M sequences
- State-of-the-art for sequence-only tasks
- Available in multiple sizes (ESM-1b, ESM-2)
- Captures evolutionary and structural information

**ProteinBERT:**
- BERT-style masked language model
- Pre-trained on UniProt sequences
- Good for transfer learning

**ProteinLSTM:**
- Bidirectional LSTM for sequence encoding
- Lightweight and fast
- Good baseline for sequence tasks

**ProteinCNN / ProteinResNet:**
- Convolutional architectures
- Capture local sequence patterns
- Faster than transformer models

### Structure-Based Models

**GearNet (Geometry-Aware Relational Graph Network):**
- Incorporates 3D geometric information
- Edge types based on sequential, radius, and K-nearest neighbors
- State-of-the-art for structure-based tasks
- Supports both backbone and full-atom representations

**GCN/GAT/GIN on Protein Graphs:**
- Standard GNN architectures adapted for proteins
- Flexible edge definitions (sequence, spatial, contact)

**SchNet:**
- Continuous-filter convolutions
- Handles 3D coordinates directly
- Good for structure prediction and protein-ligand binding

### Feature-Based Models

**Statistic Features:**
- Amino acid composition
- Sequence length statistics
- Motif counts

**Physicochemical Features:**
- Hydrophobicity scales
- Charge properties
- Secondary structure propensity
- Molecular weight, pI

## Protein Graph Construction

### Edge Types

**Sequential Edges:**
- Connect adjacent residues in sequence
- Captures primary structure

**Spatial Edges:**
- K-nearest neighbors in 3D space
- Radius cutoff (e.g., Cα atoms within 10Å)
- Captures tertiary structure

**Contact Edges:**
- Based on heavy atom distances
- Typically < 8Å threshold

### Node Features

**Residue Identity:**
- One-hot encoding of 20 amino acids
- Learned embeddings

**Position Information:**
- 3D coordinates (Cα, N, C, O)
- Backbone angles (phi, psi, omega)
- Relative spatial position encodings

**Physicochemical Properties:**
- Hydrophobicity
- Charge
- Size
- Secondary structure

## Training Workflows

### Pre-training Strategies

**Self-Supervised Pre-training:**
- Masked residue prediction (like BERT)
- Distance prediction between residues
- Angle prediction (phi, psi, omega)
- Dihedral angle prediction
- Contact map prediction

**Pre-trained Model Usage:**
```python
from torchdrug import models

# Load pre-trained ESM
model = models.ESM(path="esm1b_t33_650M_UR50S.pt")

# Fine-tune on downstream task
task = tasks.PropertyPrediction(
    model, task=["stability"],
    criterion="mse", metric=["mae", "rmse"]
)
```

### Multi-Task Learning

Train on multiple related tasks simultaneously:
- Joint prediction of function, localization, and stability
- Improves generalization and data efficiency
- Shares representations across tasks

### Best Practices

**For Sequence-Only Tasks:**
1. Start with pre-trained ESM or ProteinBERT
2. Fine-tune with small learning rate (1e-5 to 1e-4)
3. Use frozen embeddings for small datasets
4. Apply dropout for regularization

**For Structure-Based Tasks:**
1. Use GearNet with multiple edge types
2. Include geometric features (angles, dihedrals)
3. Pre-train on large structure databases
4. Use data augmentation (rotations, crops)

**For Small Datasets:**
1. Transfer learning from pre-trained models
2. Multi-task learning with related tasks
3. Data augmentation (sequence mutations, structure perturbations)
4. Strong regularization (dropout, weight decay)

## Common Use Cases

### Enzyme Engineering
- Predict enzyme activity from sequence
- Design mutations to improve stability
- Screen for desired catalytic properties

### Antibody Design
- Predict binding affinity
- Optimize antibody sequences
- Predict immunogenicity

### Drug Target Identification
- Predict protein function
- Identify druggable sites
- Analyze protein-ligand interactions

### Protein Structure Prediction
- Predict secondary structure from sequence
- Generate contact maps for tertiary structure
- Refine AlphaFold predictions

## Integration with Other Tools

### AlphaFold Integration

Load AlphaFold-predicted structures:
```python
from torchdrug import data

# Load AlphaFold structure
protein = data.Protein.from_pdb("alphafold_structure.pdb")

# Use in TorchDrug workflows
```

### ESMFold Integration

Use ESMFold for structure prediction, then analyze with TorchDrug models.

### Rosetta/PyRosetta

Generate structures with Rosetta, import to TorchDrug for analysis.

---

## Reference: Retrosynthesis

# Retrosynthesis

## Overview

Retrosynthesis is the process of planning synthetic routes from target molecules back to commercially available starting materials. TorchDrug provides tools for learning-based retrosynthesis prediction, breaking down the complex task into manageable subtasks.

## Available Datasets

### USPTO-50K

The standard benchmark dataset for retrosynthesis derived from US patent literature.

**Statistics:**
- 50,017 reaction examples
- Single-step reactions
- Filtered for quality and canonicalization
- Contains atom mapping for reaction center identification

**Reaction Types:**
- Diverse organic reactions
- Drug-like transformations
- Well-balanced across common reaction classes

**Data Splits:**
- Training: ~40k reactions
- Validation: ~5k reactions
- Test: ~5k reactions

**Format:**
- Product → Reactants
- SMILES representation
- Atom-mapped reactions for training

## Task Types

TorchDrug decomposes retrosynthesis into a multi-step pipeline:

### 1. CenterIdentification

Identifies the reaction center - which bonds were formed/broken in the forward reaction.

**Input:** Product molecule
**Output:** Probability for each bond of being part of reaction center

**Purpose:**
- Locate where chemistry happened
- Guide subsequent synthon generation
- Reduce search space dramatically

**Model Architecture:**
- Graph neural network on product molecule
- Edge-level classification
- Attention mechanisms to highlight reactive regions

**Evaluation Metrics:**
- **Top-K Accuracy**: Correct reaction center in top K predictions
- **Bond-level F1**: Precision and recall for bond predictions

### 2. SynthonCompletion

Given the product and identified reaction center, predict the reactant structures (synthons).

**Input:**
- Product molecule
- Identified reaction center (broken/formed bonds)

**Output:**
- Predicted reactant molecules (synthons)

**Process:**
1. Break bonds at reaction center
2. Modify atom environments (valence, charges)
3. Determine leaving groups and protecting groups
4. Generate complete reactant structures

**Challenges:**
- Multiple valid reactant sets
- Stereospecificity
- Atom environment changes (hybridization, charge)
- Leaving group selection

**Evaluation:**
- **Exact Match**: Generated reactants exactly match ground truth
- **Top-K Accuracy**: Correct reactants in top K predictions
- **Chemical Validity**: Generated molecules are valid

### 3. Retrosynthesis (End-to-End)

Combines center identification and synthon completion into a unified pipeline.

**Input:** Target product molecule
**Output:** Ranked list of reactant sets (synthesis pathways)

**Workflow:**
1. Identify top-K reaction centers
2. For each center, generate reactant candidates
3. Rank combinations by model confidence
4. Filter for commercial availability and feasibility

**Advantages:**
- Single model to train and deploy
- Joint optimization of subtasks
- Error propagation from center identification accounted for

## Training Workflows

### Basic Pipeline

```python
from torchdrug import datasets, models, tasks

# Load dataset
dataset = datasets.USPTO50k("~/retro-datasets/")

# For center identification
model_center = models.RGCN(
    input_dim=dataset.node_feature_dim,
    num_relation=dataset.num_bond_type,
    hidden_dims=[256, 256, 256]
)

task_center = tasks.CenterIdentification(
    model_center,
    top_k=3  # Consider top 3 reaction centers
)

# For synthon completion
model_synthon = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256]
)

task_synthon = tasks.SynthonCompletion(
    model_synthon,
    center_topk=3,  # Use top 3 from center identification
    num_synthon_beam=5  # Beam search for synthon generation
)

# End-to-end
task_retro = tasks.Retrosynthesis(
    model=model_center,
    synthon_model=model_synthon,
    center_topk=5,
    num_synthon_beam=10
)
```

### Transfer Learning

Pre-train on large reaction datasets (e.g., USPTO-full with 1M+ reactions), then fine-tune on specific reaction classes.

**Benefits:**
- Better generalization to rare reaction types
- Improved performance on small datasets
- Learn general reaction patterns

### Multi-Task Learning

Train jointly on:
- Forward reaction prediction
- Retrosynthesis
- Reaction type classification
- Yield prediction

**Advantages:**
- Shared representations of chemistry
- Better sample efficiency
- Improved robustness

## Model Architectures

### Graph Neural Networks

**RGCN (Relational Graph Convolutional Network):**
- Handles multiple bond types (single, double, triple, aromatic)
- Edge-type-specific transformations
- Good for reaction center identification

**GIN (Graph Isomorphism Network):**
- Powerful message passing
- Captures structural patterns
- Works well for synthon completion

**GAT (Graph Attention Network):**
- Attention weights highlight important atoms/bonds
- Interpretable reaction center predictions
- Flexible for various reaction types

### Sequence-Based Models

**Transformer Models:**
- SMILES-to-SMILES translation
- Can capture long-range dependencies
- Require large datasets

**LSTM/GRU:**
- Sequence generation for reactants
- Autoregressive decoding
- Good for small molecules

### Hybrid Approaches

Combine graph and sequence representations:
- Graph encoder for products
- Sequence decoder for reactants
- Best of both representations

## Reaction Chemistry Considerations

### Reaction Classes

**Common Transformations:**
- C-C bond formation (coupling, addition)
- Functional group interconversions (oxidation, reduction)
- Heterocycle synthesis (cyclizations)
- Protection/deprotection
- Aromatic substitutions

**Rare Reactions:**
- Novel coupling methods
- Complex rearrangements
- Multi-component reactions

### Selectivity Issues

**Regioselectivity:**
- Which position reacts on molecule
- Requires understanding of electronics and sterics

**Stereoselectivity:**
- Control of stereochemistry
- Diastereoselectivity and enantioselectivity
- Critical for drug synthesis

**Chemoselectivity:**
- Which functional group reacts
- Requires protecting group strategies

### Reaction Conditions

While TorchDrug focuses on reaction connectivity, consider:
- Temperature and pressure
- Catalysts and reagents
- Solvents
- Reaction time
- Work-up and purification

## Multi-Step Synthesis Planning

### Single-Step Retrosynthesis

Predict immediate precursors for target molecule.

**Use Case:**
- Late-stage transformations
- Simple molecules (1-2 steps from commercial)
- Initial route scouting

### Multi-Step Planning

Recursively apply retrosynthesis to each predicted reactant until reaching commercial building blocks.

**Tree Search Strategies:**

**Breadth-First Search:**
- Explore all routes to same depth
- Find shortest routes
- Memory intensive

**Depth-First Search:**
- Follow each route to completion
- Memory efficient
- May miss optimal routes

**Monte Carlo Tree Search (MCTS):**
- Balance exploration and exploitation
- Guided by model confidence
- State-of-the-art for multi-step planning

**A\* Search:**
- Heuristic-guided search
- Optimizes for cost, complexity, or feasibility
- Efficient for finding best routes

### Route Scoring

Rank synthetic routes by:
1. **Number of Steps**: Fewer is better (efficiency)
2. **Convergent vs Linear**: Convergent routes preferred
3. **Commercial Availability**: How many steps to buyable compounds
4. **Reaction Feasibility**: Likelihood each step works
5. **Overall Yield**: Estimated end-to-end yield
6. **Cost**: Reagents, labor, equipment
7. **Green Chemistry**: Environmental impact, safety

### Stopping Criteria

Stop retrosynthesis when reaching:
- **Commercial Compounds**: Available from vendors (e.g., Sigma-Aldrich, Enamine)
- **Building Blocks**: Standard synthetic intermediates
- **Max Depth**: e.g., 6-10 steps
- **Low Confidence**: Model uncertainty too high

## Validation and Filtering

### Chemical Validity

Check each predicted reaction:
- Reactants are valid molecules
- Reaction is chemically reasonable
- Atom mapping is consistent
- Stoichiometry balances

### Synthetic Feasibility

**Filters:**
- Reaction precedent (literature examples)
- Functional group compatibility
- Typical reaction conditions
- Expected yield ranges

**Expert Systems:**
- Rule-based validation (e.g., ARChem Route Designer)
- Check for incompatible functional groups
- Identify protection/deprotection needs

### Commercial Availability

**Databases:**
- eMolecules: 10M+ commercial compounds
- ZINC: Annotated with vendor info
- Reaxys: Commercially available building blocks

**Considerations:**
- Cost per gram
- Purity and quality
- Lead time for delivery
- Minimum order quantities

## Integration with Other Tools

### Reaction Prediction (Forward)

Train forward reaction prediction models to validate retrosynthetic proposals:
- Predict products from proposed reactants
- Validate reaction feasibility
- Estimate yields

### Retrosynthesis Software

**Integration with:**
- SciFinder (CAS)
- Reaxys (Elsevier)
- ARChem Route Designer
- IBM RXN for Chemistry

**TorchDrug as Component:**
- Use TorchDrug models within larger planning systems
- Combine ML predictions with rule-based systems
- Hybrid AI + expert system approaches

### Experimental Validation

**High-Throughput Screening:**
- Rapid testing of predicted reactions
- Automated synthesis platforms
- Feedback loop to improve models

**Robotic Synthesis:**
- Automated execution of planned routes
- Real-time optimization
- Data generation for model improvement

## Best Practices

1. **Ensemble Predictions**: Use multiple models for robustness
2. **Reaction Validation**: Always validate with chemistry rules
3. **Commercial Check**: Verify building block availability early
4. **Diversity**: Generate multiple diverse routes, not just top-1
5. **Expert Review**: Have chemists evaluate proposed routes
6. **Literature Search**: Check for precedents of key steps
7. **Iterative Refinement**: Update models with experimental feedback
8. **Interpretability**: Understand why model suggests each step
9. **Edge Cases**: Handle unusual functional groups and scaffolds
10. **Benchmarking**: Compare against known synthesis routes

## Common Applications

### Drug Synthesis Planning

- Small molecule drugs
- Natural product total synthesis
- Late-stage functionalization strategies

### Library Enumeration

- Virtual library design
- Retrosynthetic filtering of generated molecules
- Prioritize synthesizable compounds

### Process Chemistry

- Route scouting for large-scale synthesis
- Cost optimization
- Green chemistry alternatives

### Synthetic Method Development

- Identify gaps in synthetic methodology
- Guide development of new reactions
- Expand retrosynthesis model capabilities

## Challenges and Future Directions

### Current Limitations

- Limited to single-step predictions (most models)
- Doesn't consider reaction conditions explicitly
- Stereochemistry handling is challenging
- Rare reaction types underrepresented

### Active Research Areas

- End-to-end multi-step planning
- Incorporation of reaction conditions
- Stereoselective retrosynthesis
- Integration with robotics for closed-loop optimization
- Semi-template methods (balance templates and templates-free)
- Uncertainty quantification for predictions

### Emerging Techniques

- Large language models for chemistry (ChemGPT, MolT5)
- Reinforcement learning for route optimization
- Graph transformers for long-range interactions
- Self-supervised pre-training on reaction databases
