---
title: "Qiskit 量子计算"
description: "IBM 量子计算 SDK，量子电路设计、模拟和真机执行"
category: "other"
source: "community"
author: "Community"
tags: ["qiskit"]
date: 2026-03-20
---

# Qiskit

## Overview

Qiskit is the world's most popular open-source quantum computing framework with 13M+ downloads. Build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and analyze results. Supports IBM Quantum (100+ qubit systems), IonQ, Amazon Braket, and other providers.

**Key Features:**
- 83x faster transpilation than competitors
- 29% fewer two-qubit gates in optimized circuits
- Backend-agnostic execution (local simulators or cloud hardware)
- Comprehensive algorithm libraries for optimization, chemistry, and ML

## Quick Start

### Installation

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### First Circuit

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create Bell state (entangled qubits)
qc = QuantumCircuit(2)
qc.h(0)           # Hadamard on qubit 0
qc.cx(0, 1)       # CNOT from qubit 0 to 1
qc.measure_all()  # Measure both qubits

# Run locally
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### Visualization

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # Circuit diagram
plot_histogram(counts)   # Results histogram
```

## Core Capabilities

### 1. Setup and Installation
For detailed installation, authentication, and IBM Quantum account setup:
- **See `references/setup.md`**

Topics covered:
- Installation with uv
- Python environment setup
- IBM Quantum account and API token configuration
- Local vs. cloud execution

### 2. Building Quantum Circuits
For constructing quantum circuits with gates, measurements, and composition:
- **See `references/circuits.md`**

Topics covered:
- Creating circuits with QuantumCircuit
- Single-qubit gates (H, X, Y, Z, rotations, phase gates)
- Multi-qubit gates (CNOT, SWAP, Toffoli)
- Measurements and barriers
- Circuit composition and properties
- Parameterized circuits for variational algorithms

### 3. Primitives (Sampler and Estimator)
For executing quantum circuits and computing results:
- **See `references/primitives.md`**

Topics covered:
- **Sampler**: Get bitstring measurements and probability distributions
- **Estimator**: Compute expectation values of observables
- V2 interface (StatevectorSampler, StatevectorEstimator)
- IBM Quantum Runtime primitives for hardware
- Sessions and Batch modes
- Parameter binding

### 4. Transpilation and Optimization
For optimizing circuits and preparing for hardware execution:
- **See `references/transpilation.md`**

Topics covered:
- Why transpilation is necessary
- Optimization levels (0-3)
- Six transpilation stages (init, layout, routing, translation, optimization, scheduling)
- Advanced features (virtual permutation elision, gate cancellation)
- Common parameters (initial_layout, approximation_degree, seed)
- Best practices for efficient circuits

### 5. Visualization
For displaying circuits, results, and quantum states:
- **See `references/visualization.md`**

Topics covered:
- Circuit drawings (text, matplotlib, LaTeX)
- Result histograms
- Quantum state visualization (Bloch sphere, state city, QSphere)
- Backend topology and error maps
- Customization and styling
- Saving publication-quality figures

### 6. Hardware Backends
For running on simulators and real quantum computers:
- **See `references/backends.md`**

Topics covered:
- IBM Quantum backends and authentication
- Backend properties and status
- Running on real hardware with Runtime primitives
- Job management and queuing
- Session mode (iterative algorithms)
- Batch mode (parallel jobs)
- Local simulators (StatevectorSampler, Aer)
- Third-party providers (IonQ, Amazon Braket)
- Error mitigation strategies

### 7. Qiskit Patterns Workflow
For implementing the four-step quantum computing workflow:
- **See `references/patterns.md`**

Topics covered:
- **Map**: Translate problems to quantum circuits
- **Optimize**: Transpile for hardware
- **Execute**: Run with primitives
- **Post-process**: Extract and analyze results
- Complete VQE example
- Session vs. Batch execution
- Common workflow patterns

### 8. Quantum Algorithms and Applications
For implementing specific quantum algorithms:
- **See `references/algorithms.md`**

Topics covered:
- **Optimization**: VQE, QAOA, Grover's algorithm
- **Chemistry**: Molecular ground states, excited states, Hamiltonians
- **Machine Learning**: Quantum kernels, VQC, QNN
- **Algorithm libraries**: Qiskit Nature, Qiskit ML, Qiskit Optimization
- Physics simulations and benchmarking

## Workflow Decision Guide

**If you need to:**

- Install Qiskit or set up IBM Quantum account → `references/setup.md`
- Build a new quantum circuit → `references/circuits.md`
- Understand gates and circuit operations → `references/circuits.md`
- Run circuits and get measurements → `references/primitives.md`
- Compute expectation values → `references/primitives.md`
- Optimize circuits for hardware → `references/transpilation.md`
- Visualize circuits or results → `references/visualization.md`
- Execute on IBM Quantum hardware → `references/backends.md`
- Connect to third-party providers → `references/backends.md`
- Implement end-to-end quantum workflow → `references/patterns.md`
- Build specific algorithm (VQE, QAOA, etc.) → `references/algorithms.md`
- Solve chemistry or optimization problems → `references/algorithms.md`

## Best Practices

### Development Workflow

1. **Start with simulators**: Test locally before using hardware
   ```python
   from qiskit.primitives import StatevectorSampler
   sampler = StatevectorSampler()
   ```

2. **Always transpile**: Optimize circuits before execution
   ```python
   from qiskit import transpile
   qc_optimized = transpile(qc, backend=backend, optimization_level=3)
   ```

3. **Use appropriate primitives**:
   - Sampler for bitstrings (optimization algorithms)
   - Estimator for expectation values (chemistry, physics)

4. **Choose execution mode**:
   - Session: Iterative algorithms (VQE, QAOA)
   - Batch: Independent parallel jobs
   - Single job: One-off experiments

### Performance Optimization

- Use optimization_level=3 for production
- Minimize two-qubit gates (major error source)
- Test with noisy simulators before hardware
- Save and reuse transpiled circuits
- Monitor convergence in variational algorithms

### Hardware Execution

- Check backend status before submitting
- Use least_busy() for testing
- Save job IDs for later retrieval
- Apply error mitigation (resilience_level)
- Start with fewer shots, increase for final runs

## Common Patterns

### Pattern 1: Simple Circuit Execution

```python
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### Pattern 2: Hardware Execution with Transpilation

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc_optimized = transpile(qc, backend=backend, optimization_level=3)

sampler = Sampler(backend)
job = sampler.run([qc_optimized], shots=1024)
result = job.result()
```

### Pattern 3: Variational Algorithm (VQE)

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from scipy.optimize import minimize

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    def cost_function(params):
        bound_qc = ansatz.assign_parameters(params)
        qc_isa = transpile(bound_qc, backend=backend)
        result = estimator.run([(qc_isa, hamiltonian)]).result()
        return result[0].data.evs

    result = minimize(cost_function, initial_params, method='COBYLA')
```

## Additional Resources

- **Official Docs**: https://quantum.ibm.com/docs
- **Qiskit Textbook**: https://qiskit.org/learn
- **API Reference**: https://docs.quantum.ibm.com/api/qiskit
- **Patterns Guide**: https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns

---

## Reference: Algorithms

# Quantum Algorithms and Applications

Qiskit supports a wide range of quantum algorithms for optimization, chemistry, machine learning, and physics simulations.

## Table of Contents

1. [Optimization Algorithms](#optimization-algorithms)
2. [Chemistry and Materials Science](#chemistry-and-materials-science)
3. [Machine Learning](#machine-learning)
4. [Algorithm Libraries](#algorithm-libraries)

## Optimization Algorithms

### Variational Quantum Eigensolver (VQE)

VQE finds the minimum eigenvalue of a Hamiltonian using a hybrid quantum-classical approach.

**Use Cases:**
- Molecular ground state energy
- Combinatorial optimization
- Materials simulation

**Implementation:**
```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator, Session
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

def vqe_algorithm(hamiltonian, ansatz, backend, initial_params):
    """
    Run VQE algorithm

    Args:
        hamiltonian: Observable (SparsePauliOp)
        ansatz: Parameterized quantum circuit
        backend: Quantum backend
        initial_params: Initial parameter values
    """

    with Session(backend=backend) as session:
        estimator = Estimator(session=session)

        def cost_function(params):
            # Bind parameters to circuit
            bound_circuit = ansatz.assign_parameters(params)

            # Transpile for hardware
            qc_isa = transpile(bound_circuit, backend=backend, optimization_level=3)

            # Compute expectation value
            job = estimator.run([(qc_isa, hamiltonian)])
            result = job.result()
            energy = result[0].data.evs

            return energy

        # Classical optimization
        result = minimize(
            cost_function,
            initial_params,
            method='COBYLA',
            options={'maxiter': 100}
        )

    return result.fun, result.x

# Example: H2 molecule Hamiltonian
hamiltonian = SparsePauliOp(
    ["IIII", "ZZII", "IIZZ", "ZZZI", "IZZI"],
    coeffs=[-0.8, 0.17, 0.17, -0.24, 0.17]
)

# Create ansatz
qc = QuantumCircuit(4)
# ... define ansatz structure ...

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

energy, params = vqe_algorithm(hamiltonian, qc, backend, np.random.rand(10))
print(f"Ground state energy: {energy}")
```

### Quantum Approximate Optimization Algorithm (QAOA)

QAOA solves combinatorial optimization problems like MaxCut, TSP, and graph coloring.

**Use Cases:**
- MaxCut problems
- Portfolio optimization
- Vehicle routing
- Scheduling problems

**Implementation:**
```python
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import networkx as nx

def qaoa_maxcut(graph, p, backend):
    """
    QAOA for MaxCut problem

    Args:
        graph: NetworkX graph
        p: Number of QAOA layers
        backend: Quantum backend
    """
    num_qubits = len(graph.nodes())
    qc = QuantumCircuit(num_qubits)

    # Initial superposition
    qc.h(range(num_qubits))

    # Alternating layers
    betas = [Parameter(f'β_{i}') for i in range(p)]
    gammas = [Parameter(f'γ_{i}') for i in range(p)]

    for i in range(p):
        # Problem Hamiltonian (MaxCut)
        for edge in graph.edges():
            u, v = edge
            qc.cx(u, v)
            qc.rz(2 * gammas[i], v)
            qc.cx(u, v)

        # Mixer Hamiltonian
        for qubit in range(num_qubits):
            qc.rx(2 * betas[i], qubit)

    qc.measure_all()
    return qc, betas + gammas

# Example: MaxCut on 4-node graph
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

qaoa_circuit, params = qaoa_maxcut(G, p=2, backend=backend)

# Run with Sampler and optimize parameters
# ... (similar to VQE optimization loop)
```

### Grover's Algorithm

Quantum search algorithm providing quadratic speedup for unstructured search.

**Use Cases:**
- Database search
- SAT solving
- Finding marked items

**Implementation:**
```python
from qiskit import QuantumCircuit

def grover_oracle(marked_states):
    """Create oracle that marks target states"""
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)

    for target in marked_states:
        # Flip phase of target state
        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

        # Multi-controlled Z
        qc.h(num_qubits - 1)
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        qc.h(num_qubits - 1)

        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

    return qc

def grover_diffusion(num_qubits):
    """Create Grover diffusion operator"""
    qc = QuantumCircuit(num_qubits)

    qc.h(range(num_qubits))
    qc.x(range(num_qubits))

    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)

    qc.x(range(num_qubits))
    qc.h(range(num_qubits))

    return qc

def grover_algorithm(marked_states, num_iterations):
    """Complete Grover's algorithm"""
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)

    # Initialize superposition
    qc.h(range(num_qubits))

    # Grover iterations
    oracle = grover_oracle(marked_states)
    diffusion = grover_diffusion(num_qubits)

    for _ in range(num_iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffusion, inplace=True)

    qc.measure_all()
    return qc

# Search for state |101⟩ in 3-qubit space
marked = ['101']
iterations = int(np.pi/4 * np.sqrt(2**3))  # Optimal iterations
qc_grover = grover_algorithm(marked, iterations)
```

## Chemistry and Materials Science

### Molecular Ground State Energy

**Install Qiskit Nature:**
```bash
uv pip install qiskit-nature qiskit-nature-pyscf
```

**Example: H2 Molecule**
```python
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock

# Define molecule
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0
)

# Get electronic structure problem
problem = driver.run()

# Map fermionic operators to qubits
mapper = JordanWignerMapper()
hamiltonian = mapper.map(problem.hamiltonian.second_q_op())

# Create initial state
num_particles = problem.num_particles
num_spatial_orbitals = problem.num_spatial_orbitals

init_state = HartreeFock(
    num_spatial_orbitals,
    num_particles,
    mapper
)

# Create ansatz
ansatz = UCCSD(
    num_spatial_orbitals,
    num_particles,
    mapper,
    initial_state=init_state
)

# Run VQE
energy, params = vqe_algorithm(
    hamiltonian,
    ansatz,
    backend,
    np.zeros(ansatz.num_parameters)
)

# Add nuclear repulsion energy
total_energy = energy + problem.nuclear_repulsion_energy
print(f"Ground state energy: {total_energy} Ha")
```

### Different Molecular Mappers

```python
# Jordan-Wigner mapping
jw_mapper = JordanWignerMapper()
ham_jw = jw_mapper.map(problem.hamiltonian.second_q_op())

# Parity mapping (often more efficient)
parity_mapper = ParityMapper()
ham_parity = parity_mapper.map(problem.hamiltonian.second_q_op())

# Bravyi-Kitaev mapping
from qiskit_nature.second_q.mappers import BravyiKitaevMapper
bk_mapper = BravyiKitaevMapper()
ham_bk = bk_mapper.map(problem.hamiltonian.second_q_op())
```

### Excited States

```python
from qiskit_nature.second_q.algorithms import QEOM

# Quantum Equation of Motion for excited states
qeom = QEOM(estimator, ansatz, 'sd')  # Singles and doubles excitations
excited_states = qeom.solve(problem)
```

## Machine Learning

### Quantum Kernels

Quantum computers can compute kernel functions for machine learning.

**Install Qiskit Machine Learning:**
```bash
uv pip install qiskit-machine-learning
```

**Example: Classification with Quantum Kernel**
```python
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit.circuit.library import ZZFeatureMap
from sklearn.svm import SVC
import numpy as np

# Create feature map
num_features = 2
feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)

# Create quantum kernel
fidelity = ComputeUncompute(sampler=sampler)
qkernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)

# Use with scikit-learn
X_train = np.random.rand(50, 2)
y_train = np.random.choice([0, 1], 50)

# Compute kernel matrix
kernel_matrix = qkernel.evaluate(X_train)

# Train SVM with quantum kernel
svc = SVC(kernel='precomputed')
svc.fit(kernel_matrix, y_train)

# Predict
X_test = np.random.rand(10, 2)
kernel_test = qkernel.evaluate(X_test, X_train)
predictions = svc.predict(kernel_test)
```

### Variational Quantum Classifier (VQC)

```python
from qiskit_machine_learning.algorithms import VQC
from qiskit.circuit.library import RealAmplitudes

# Create feature map and ansatz
feature_map = ZZFeatureMap(2)
ansatz = RealAmplitudes(2, reps=1)

# Create VQC
vqc = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer='COBYLA'
)

# Train
vqc.fit(X_train, y_train)

# Predict
predictions = vqc.predict(X_test)
accuracy = vqc.score(X_test, y_test)
```

### Quantum Neural Networks (QNN)

```python
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit.circuit import QuantumCircuit, Parameter

# Create parameterized circuit
qc = QuantumCircuit(2)
params = [Parameter(f'θ_{i}') for i in range(4)]

# Network structure
for i, param in enumerate(params[:2]):
    qc.ry(param, i)

qc.cx(0, 1)

for i, param in enumerate(params[2:]):
    qc.ry(param, i)

qc.measure_all()

# Create QNN
qnn = SamplerQNN(
    circuit=qc,
    sampler=sampler,
    input_params=[],  # No input parameters for this example
    weight_params=params
)

# Use with PyTorch or TensorFlow for training
```

## Algorithm Libraries

### Qiskit Algorithms

Standard implementations of quantum algorithms:

```bash
uv pip install qiskit-algorithms
```

**Available Algorithms:**
- Amplitude Estimation
- Phase Estimation
- Shor's Algorithm
- Quantum Fourier Transform
- HHL (Linear systems)

**Example: Quantum Phase Estimation**
```python
from qiskit.circuit.library import QFT
from qiskit_algorithms import PhaseEstimation

# Create unitary operator
num_qubits = 3
unitary = QuantumCircuit(num_qubits)
# ... define unitary ...

# Phase estimation
pe = PhaseEstimation(num_evaluation_qubits=3, quantum_instance=backend)
result = pe.estimate(unitary=unitary, state_preparation=initial_state)
```

### Qiskit Optimization

Optimization problem solvers:

```bash
uv pip install qiskit-optimization
```

**Supported Problems:**
- Quadratic programs
- Integer programming
- Linear programming
- Constraint satisfaction

**Example: Portfolio Optimization**
```python
from qiskit_optimization.applications import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA

# Define portfolio problem
returns = [0.1, 0.15, 0.12]  # Expected returns
covariances = [[1, 0.5, 0.3], [0.5, 1, 0.4], [0.3, 0.4, 1]]
budget = 2  # Number of assets to select

portfolio = PortfolioOptimization(
    expected_returns=returns,
    covariances=covariances,
    budget=budget
)

# Convert to quadratic program
qp = portfolio.to_quadratic_program()

# Solve with QAOA
qaoa = QAOA(sampler=sampler, optimizer='COBYLA', reps=2)
optimizer = MinimumEigenOptimizer(qaoa)

result = optimizer.solve(qp)
print(f"Optimal portfolio: {result.x}")
```

## Physics Simulations

### Time Evolution

```python
from qiskit.synthesis import SuzukiTrotter
from qiskit.quantum_info import SparsePauliOp

# Define Hamiltonian
hamiltonian = SparsePauliOp(["XX", "YY", "ZZ"], coeffs=[1.0, 1.0, 1.0])

# Time evolution
time = 1.0
evolution_gate = SuzukiTrotter(order=2, reps=10).synthesize(
    hamiltonian,
    time
)

qc = QuantumCircuit(2)
qc.append(evolution_gate, range(2))
```

### Partial Differential Equations

**Use Case:** Quantum algorithms for solving PDEs with potential exponential speedup.

```python
# Quantum PDE solver implementation
# Requires advanced techniques like HHL algorithm
# and amplitude encoding of solution vectors
```

## Benchmarking

### Benchpress Toolkit

Benchmark quantum algorithms:

```python
# Benchpress provides standardized benchmarks
# for comparing quantum algorithm performance

# Examples:
# - Quantum volume circuits
# - Random circuit sampling
# - Application-specific benchmarks
```

## Best Practices

### 1. Start Simple
Begin with small problem instances to validate your approach:
```python
# Test with 2-3 qubits first
# Scale up after confirming correctness
```

### 2. Use Simulators for Development
```python
from qiskit.primitives import StatevectorSampler

# Develop with local simulator
sampler_sim = StatevectorSampler()

# Switch to hardware for production
# sampler_hw = Sampler(backend)
```

### 3. Monitor Convergence
```python
convergence_data = []

def tracked_cost_function(params):
    energy = cost_function(params)
    convergence_data.append(energy)
    return energy

# Plot convergence after optimization
import matplotlib.pyplot as plt
plt.plot(convergence_data)
plt.xlabel('Iteration')
plt.ylabel('Energy')
plt.show()
```

### 4. Parameter Initialization
```python
# Use problem-specific initialization when possible
# Random initialization
initial_params = np.random.uniform(0, 2*np.pi, num_params)

# Or use classical preprocessing
# initial_params = classical_solution_to_params(classical_result)
```

### 5. Save Intermediate Results
```python
import json

checkpoint = {
    'iteration': iteration,
    'params': params.tolist(),
    'energy': energy,
    'timestamp': time.time()
}

with open(f'checkpoint_{iteration}.json', 'w') as f:
    json.dump(checkpoint, f)
```

## Resources and Further Reading

**Official Documentation:**
- [Qiskit Textbook](https://qiskit.org/learn)
- [Qiskit Nature Documentation](https://qiskit.org/ecosystem/nature)
- [Qiskit Machine Learning Documentation](https://qiskit.org/ecosystem/machine-learning)
- [Qiskit Optimization Documentation](https://qiskit.org/ecosystem/optimization)

**Research Papers:**
- VQE: Peruzzo et al., Nature Communications (2014)
- QAOA: Farhi et al., arXiv:1411.4028
- Quantum Kernels: Havlíček et al., Nature (2019)

---

## Reference: Backends

# Hardware Backends and Execution

Qiskit is backend-agnostic and supports execution on simulators and real quantum hardware from multiple providers.

## Backend Types

### Local Simulators
- Run on your machine
- No account required
- Perfect for development and testing

### Cloud-Based Hardware
- IBM Quantum (100+ qubit systems)
- IonQ (trapped ion)
- Amazon Braket (Rigetti, IonQ, Oxford Quantum Circuits)
- Other providers via plugins

## IBM Quantum Backends

### Connecting to IBM Quantum

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# First time: save credentials
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_TOKEN"
)

# Subsequent sessions: load credentials
service = QiskitRuntimeService()
```

### Listing Available Backends

```python
# List all available backends
backends = service.backends()
for backend in backends:
    print(f"{backend.name}: {backend.num_qubits} qubits")

# Filter by minimum qubits
backends_127q = service.backends(min_num_qubits=127)

# Get specific backend
backend = service.backend("ibm_brisbane")
backend = service.least_busy()  # Get least busy backend
```

### Backend Properties

```python
backend = service.backend("ibm_brisbane")

# Basic info
print(f"Name: {backend.name}")
print(f"Qubits: {backend.num_qubits}")
print(f"Version: {backend.version}")
print(f"Status: {backend.status()}")

# Coupling map (qubit connectivity)
print(backend.coupling_map)

# Basis gates
print(backend.configuration().basis_gates)

# Qubit properties
print(backend.qubit_properties(0))  # Properties of qubit 0
```

### Checking Backend Status

```python
status = backend.status()
print(f"Operational: {status.operational}")
print(f"Pending jobs: {status.pending_jobs}")
print(f"Status message: {status.status_msg}")
```

## Running on IBM Quantum Hardware

### Using Runtime Primitives

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Create and transpile circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Transpile for backend
transpiled_qc = transpile(qc, backend=backend, optimization_level=3)

# Run with Sampler
sampler = Sampler(backend)
job = sampler.run([transpiled_qc], shots=1024)

# Retrieve results
result = job.result()
counts = result[0].data.meas.get_counts()
print(counts)
```

### Job Management

```python
# Submit job
job = sampler.run([qc], shots=1024)

# Get job ID (save for later retrieval)
job_id = job.job_id()
print(f"Job ID: {job_id}")

# Check job status
print(job.status())

# Wait for completion
result = job.result()

# Retrieve job later
service = QiskitRuntimeService()
retrieved_job = service.job(job_id)
result = retrieved_job.result()
```

### Job Queuing

```python
# Check queue position
job_status = job.status()
print(f"Queue position: {job.queue_position()}")

# Cancel job if needed
job.cancel()
```

## Session Mode

Use sessions for iterative algorithms (VQE, QAOA) to reduce queue time:

```python
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Session(backend=backend) as session:
    sampler = Sampler(session=session)

    # Multiple iterations in same session
    for iteration in range(10):
        # Parameterized circuit
        qc = create_parameterized_circuit(params[iteration])
        job = sampler.run([qc], shots=1024)
        result = job.result()

        # Update parameters based on results
        params[iteration + 1] = optimize(result)
```

Session benefits:
- Reduced queue waiting between iterations
- Guaranteed backend availability during session
- Better for variational algorithms

## Batch Mode

Use batch mode for independent parallel jobs:

```python
from qiskit_ibm_runtime import Batch, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)

    # Submit multiple independent jobs
    jobs = []
    for qc in circuit_list:
        job = sampler.run([qc], shots=1024)
        jobs.append(job)

    # Collect all results
    results = [job.result() for job in jobs]
```

## Local Simulators

### StatevectorSampler (Ideal Simulation)

```python
from qiskit.primitives import StatevectorSampler

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### Aer Simulator (Realistic Noise)

```python
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

# Ideal simulation
simulator = AerSimulator()

# Simulate with backend noise model
backend = service.backend("ibm_brisbane")
noisy_simulator = AerSimulator.from_backend(backend)

# Run simulation
transpiled_qc = transpile(qc, simulator)
sampler = Sampler(simulator)
job = sampler.run([transpiled_qc], shots=1024)
result = job.result()
```

### Aer GPU Acceleration

```python
# Use GPU for faster simulation
simulator = AerSimulator(method='statevector', device='GPU')
```

## Third-Party Providers

### IonQ

IonQ offers trapped-ion quantum computers with all-to-all connectivity:

```python
from qiskit_ionq import IonQProvider

provider = IonQProvider("YOUR_IONQ_API_TOKEN")

# List IonQ backends
backends = provider.backends()
backend = provider.get_backend("ionq_qpu")

# Run circuit
job = backend.run(qc, shots=1024)
result = job.result()
```

### Amazon Braket

```python
from qiskit_braket_provider import BraketProvider

provider = BraketProvider()

# List available devices
backends = provider.backends()

# Use specific device
backend = provider.get_backend("Rigetti")
job = backend.run(qc, shots=1024)
result = job.result()
```

## Error Mitigation

### Measurement Error Mitigation

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler, Options

# Configure error mitigation
options = Options()
options.resilience_level = 1  # 0=none, 1=minimal, 2=moderate, 3=heavy

sampler = Sampler(backend, options=options)
job = sampler.run([qc], shots=1024)
result = job.result()
```

### Error Mitigation Levels

- **Level 0**: No mitigation
- **Level 1**: Readout error mitigation
- **Level 2**: Level 1 + gate error mitigation
- **Level 3**: Level 2 + advanced techniques

**Qiskit's Samplomatic package** can reduce sampling overhead by up to 100x with probabilistic error cancellation.

### Zero Noise Extrapolation (ZNE)

```python
options = Options()
options.resilience_level = 2
options.resilience.zne_mitigation = True

sampler = Sampler(backend, options=options)
```

## Monitoring Usage and Costs

### Check Account Usage

```python
# For IBM Quantum
service = QiskitRuntimeService()

# Check remaining credits
print(service.usage())
```

### Estimate Job Cost

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

backend = service.backend("ibm_brisbane")

# Estimate job cost
estimator = Estimator(backend)
# Cost depends on circuit complexity and shots
```

## Best Practices

### 1. Always Transpile Before Running

```python
# Bad: Run without transpilation
job = sampler.run([qc], shots=1024)

# Good: Transpile first
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
job = sampler.run([qc_transpiled], shots=1024)
```

### 2. Test with Simulators First

```python
# Test with noisy simulator before hardware
noisy_sim = AerSimulator.from_backend(backend)
qc_test = transpile(qc, noisy_sim, optimization_level=3)

# Verify results look reasonable
# Then run on hardware
```

### 3. Use Appropriate Shot Counts

```python
# For optimization algorithms: fewer shots (100-1000)
# For final measurements: more shots (10000+)

# Adaptive shots based on stage
shots_optimization = 500
shots_final = 10000
```

### 4. Choose Backend Strategically

```python
# For testing: Use least busy backend
backend = service.least_busy(min_num_qubits=5)

# For production: Use backend matching requirements
backend = service.backend("ibm_brisbane")  # 127 qubits
```

### 5. Use Sessions for Variational Algorithms

Sessions are ideal for VQE, QAOA, and other iterative algorithms.

### 6. Monitor Job Status

```python
import time

job = sampler.run([qc], shots=1024)

while job.status().name not in ['DONE', 'ERROR', 'CANCELLED']:
    print(f"Status: {job.status().name}")
    time.sleep(10)

result = job.result()
```

## Troubleshooting

### Issue: "Backend not found"
```python
# List available backends
print([b.name for b in service.backends()])
```

### Issue: "Invalid credentials"
```python
# Re-save credentials
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_TOKEN",
    overwrite=True
)
```

### Issue: Long queue times
```python
# Use least busy backend
backend = service.least_busy(min_num_qubits=5)

# Or use batch mode for multiple independent jobs
```

### Issue: Job fails with "Circuit too large"
```python
# Reduce circuit complexity
# Use higher transpilation optimization
qc_opt = transpile(qc, backend=backend, optimization_level=3)
```

## Backend Comparison

| Provider | Connectivity | Gate Set | Notes |
|----------|-------------|----------|--------|
| IBM Quantum | Limited | CX, RZ, SX, X | 100+ qubit systems, high quality |
| IonQ | All-to-all | GPI, GPI2, MS | Trapped ion, low error rates |
| Rigetti | Limited | CZ, RZ, RX | Superconducting qubits |
| Oxford Quantum Circuits | Limited | ECR, RZ, SX | Coaxmon technology |

---

## Reference: Circuits

# Quantum Circuit Building

## Creating a Quantum Circuit

Create circuits using the `QuantumCircuit` class:

```python
from qiskit import QuantumCircuit

# Create a circuit with 3 qubits
qc = QuantumCircuit(3)

# Create a circuit with 3 qubits and 3 classical bits
qc = QuantumCircuit(3, 3)
```

## Single-Qubit Gates

### Pauli Gates

```python
qc.x(0)   # NOT/Pauli-X gate on qubit 0
qc.y(1)   # Pauli-Y gate on qubit 1
qc.z(2)   # Pauli-Z gate on qubit 2
```

### Hadamard Gate

Creates superposition:

```python
qc.h(0)   # Hadamard gate on qubit 0
```

### Phase Gates

```python
qc.s(0)   # S gate (√Z)
qc.t(0)   # T gate (√S)
qc.p(π/4, 0)   # Phase gate with custom angle
```

### Rotation Gates

```python
from math import pi

qc.rx(pi/2, 0)   # Rotation around X-axis
qc.ry(pi/4, 1)   # Rotation around Y-axis
qc.rz(pi/3, 2)   # Rotation around Z-axis
```

## Multi-Qubit Gates

### CNOT (Controlled-NOT)

```python
qc.cx(0, 1)   # CNOT with control=0, target=1
```

### Controlled Gates

```python
qc.cy(0, 1)   # Controlled-Y
qc.cz(0, 1)   # Controlled-Z
qc.ch(0, 1)   # Controlled-Hadamard
```

### SWAP Gate

```python
qc.swap(0, 1)   # Swap qubits 0 and 1
```

### Toffoli (CCX) Gate

```python
qc.ccx(0, 1, 2)   # Toffoli with controls=0,1 and target=2
```

## Measurements

Add measurements to read qubit states:

```python
# Measure all qubits
qc.measure_all()

# Measure specific qubits to specific classical bits
qc.measure(0, 0)   # Measure qubit 0 to classical bit 0
qc.measure([0, 1], [0, 1])   # Measure qubits 0,1 to bits 0,1
```

## Circuit Composition

### Combining Circuits

```python
qc1 = QuantumCircuit(2)
qc1.h(0)

qc2 = QuantumCircuit(2)
qc2.cx(0, 1)

# Compose circuits
qc_combined = qc1.compose(qc2)
```

### Tensor Product

```python
qc1 = QuantumCircuit(1)
qc1.h(0)

qc2 = QuantumCircuit(1)
qc2.x(0)

# Create larger circuit from smaller ones
qc_tensor = qc1.tensor(qc2)   # Results in 2-qubit circuit
```

## Barriers and Labels

```python
qc.barrier()   # Add visual barrier in circuit
qc.barrier([0, 1])   # Barrier on specific qubits

# Add labels for clarity
qc.barrier(label="Initialization")
```

## Circuit Properties

```python
print(qc.num_qubits)   # Number of qubits
print(qc.num_clbits)   # Number of classical bits
print(qc.depth())      # Circuit depth
print(qc.size())       # Total gate count
print(qc.count_ops())  # Dictionary of gate counts
```

## Example: Bell State

Create entanglement between two qubits:

```python
qc = QuantumCircuit(2)
qc.h(0)           # Superposition on qubit 0
qc.cx(0, 1)       # Entangle qubit 0 and 1
qc.measure_all()  # Measure both qubits
```

## Example: Quantum Fourier Transform (QFT)

```python
from math import pi

def qft(n):
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j+1, n):
            qc.cp(pi/2**(k-j), k, j)
    return qc

# Create 3-qubit QFT
qc_qft = qft(3)
```

## Parameterized Circuits

Create circuits with parameters for variational algorithms:

```python
from qiskit.circuit import Parameter

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)

# Bind parameter value
qc_bound = qc.assign_parameters({theta: pi/4})
```

## Circuit Operations

```python
# Inverse of a circuit
qc_inverse = qc.inverse()

# Decompose gates to basis gates
qc_decomposed = qc.decompose()

# Draw circuit (returns string or diagram)
print(qc.draw())
print(qc.draw('mpl'))   # Matplotlib figure
```

---

## Reference: Patterns

# Qiskit Patterns: The Four-Step Workflow

Qiskit Patterns provide a general framework for solving domain-specific quantum computing problems in four stages: Map, Optimize, Execute, and Post-process.

## Overview

The patterns framework enables seamless composition of quantum capabilities and supports heterogeneous computing infrastructure (CPU/GPU/QPU). Execute locally, through cloud services, or via Qiskit Serverless.

## The Four Steps

```
Problem → [Map] → [Optimize] → [Execute] → [Post-process] → Solution
```

### 1. Map
Translate classical problems into quantum circuits and operators

### 2. Optimize
Prepare circuits for target hardware through transpilation

### 3. Execute
Run circuits on quantum hardware using primitives

### 4. Post-process
Extract and refine results with classical computation

## Step 1: Map

### Goal
Transform domain-specific problems into quantum representations (circuits, operators, Hamiltonians).

### Key Decisions

**Choose Output Type:**
- **Sampler**: For bitstring outputs (optimization, search)
- **Estimator**: For expectation values (chemistry, physics)

**Design Circuit Structure:**
```python
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

# Example: Parameterized circuit for VQE
def create_ansatz(num_qubits, depth):
    qc = QuantumCircuit(num_qubits)
    params = []

    for d in range(depth):
        # Rotation layer
        for i in range(num_qubits):
            theta = Parameter(f'θ_{d}_{i}')
            params.append(theta)
            qc.ry(theta, i)

        # Entanglement layer
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)

    return qc, params

ansatz, params = create_ansatz(num_qubits=4, depth=2)
```

### Considerations

- **Hardware topology**: Design with backend coupling map in mind
- **Gate efficiency**: Minimize two-qubit gates
- **Measurement basis**: Determine required measurements

### Domain-Specific Examples

**Chemistry: Molecular Hamiltonian**
```python
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

# Define molecule
driver = PySCFDriver(atom='H 0 0 0; H 0 0 0.735', basis='sto3g')
problem = driver.run()

# Map to qubit Hamiltonian
mapper = JordanWignerMapper()
hamiltonian = mapper.map(problem.hamiltonian)
```

**Optimization: QAOA Circuit**
```python
from qiskit.circuit import QuantumCircuit, Parameter

def qaoa_circuit(graph, p):
    """Create QAOA circuit for MaxCut problem"""
    num_qubits = len(graph.nodes())
    qc = QuantumCircuit(num_qubits)

    # Initial superposition
    qc.h(range(num_qubits))

    # Alternating layers
    betas = [Parameter(f'β_{i}') for i in range(p)]
    gammas = [Parameter(f'γ_{i}') for i in range(p)]

    for i in range(p):
        # Problem Hamiltonian
        for edge in graph.edges():
            qc.cx(edge[0], edge[1])
            qc.rz(2 * gammas[i], edge[1])
            qc.cx(edge[0], edge[1])

        # Mixer Hamiltonian
        qc.rx(2 * betas[i], range(num_qubits))

    return qc
```

## Step 2: Optimize

### Goal
Transform abstract circuits to hardware-compatible ISA (Instruction Set Architecture) circuits.

### Transpilation

```python
from qiskit import transpile

# Basic transpilation
qc_isa = transpile(qc, backend=backend, optimization_level=3)

# With specific initial layout
qc_isa = transpile(
    qc,
    backend=backend,
    optimization_level=3,
    initial_layout=[0, 2, 4, 6],  # Map to specific physical qubits
    seed_transpiler=42  # Reproducibility
)
```

### Pre-optimization Tips

1. **Test with simulators first**:
```python
from qiskit_aer import AerSimulator

sim = AerSimulator.from_backend(backend)
qc_test = transpile(qc, sim, optimization_level=3)
print(f"Estimated depth: {qc_test.depth()}")
```

2. **Analyze transpilation results**:
```python
print(f"Original gates: {qc.size()}")
print(f"Transpiled gates: {qc_isa.size()}")
print(f"Two-qubit gates: {qc_isa.count_ops().get('cx', 0)}")
```

3. **Consider circuit cutting** for large circuits:
```python
# For circuits too large for available hardware
# Use circuit cutting techniques to split into smaller subcircuits
```

## Step 3: Execute

### Goal
Run ISA circuits on quantum hardware using primitives.

### Using Sampler

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Transpile first
qc_isa = transpile(qc, backend=backend, optimization_level=3)

# Execute
sampler = Sampler(backend)
job = sampler.run([qc_isa], shots=10000)
result = job.result()
counts = result[0].data.meas.get_counts()
```

### Using Estimator

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit.quantum_info import SparsePauliOp

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Transpile
qc_isa = transpile(qc, backend=backend, optimization_level=3)

# Define observable
observable = SparsePauliOp(["ZZZZ", "XXXX"])

# Execute
estimator = Estimator(backend)
job = estimator.run([(qc_isa, observable)])
result = job.result()
expectation_value = result[0].data.evs
```

### Execution Modes

**Session Mode (Iterative):**
```python
from qiskit_ibm_runtime import Session

with Session(backend=backend) as session:
    sampler = Sampler(session=session)

    # Multiple iterations
    for iteration in range(max_iterations):
        qc_iteration = update_circuit(params[iteration])
        qc_isa = transpile(qc_iteration, backend=backend)

        job = sampler.run([qc_isa], shots=1000)
        result = job.result()

        # Update parameters
        params[iteration + 1] = optimize_params(result)
```

**Batch Mode (Parallel):**
```python
from qiskit_ibm_runtime import Batch

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)

    # Submit all jobs at once
    jobs = []
    for qc in circuit_list:
        qc_isa = transpile(qc, backend=backend)
        job = sampler.run([qc_isa], shots=1000)
        jobs.append(job)

    # Collect results
    results = [job.result() for job in jobs]
```

### Error Mitigation

```python
from qiskit_ibm_runtime import Options

options = Options()
options.resilience_level = 2  # 0=none, 1=light, 2=moderate, 3=heavy
options.optimization_level = 3

sampler = Sampler(backend, options=options)
```

## Step 4: Post-process

### Goal
Extract meaningful results from quantum measurements using classical computation.

### Result Processing

**For Sampler (Bitstrings):**
```python
counts = result[0].data.meas.get_counts()

# Convert to probabilities
total_shots = sum(counts.values())
probabilities = {state: count/total_shots for state, count in counts.items()}

# Find most probable state
max_state = max(counts, key=counts.get)
print(f"Most probable state: {max_state} ({counts[max_state]}/{total_shots})")
```

**For Estimator (Expectation Values):**
```python
expectation_value = result[0].data.evs
std_dev = result[0].data.stds  # Standard deviation

print(f"Energy: {expectation_value} ± {std_dev}")
```

### Domain-Specific Post-Processing

**Chemistry: Ground State Energy**
```python
def post_process_chemistry(result, nuclear_repulsion):
    """Extract ground state energy"""
    electronic_energy = result[0].data.evs
    total_energy = electronic_energy + nuclear_repulsion
    return total_energy
```

**Optimization: MaxCut Solution**
```python
def post_process_maxcut(counts, graph):
    """Find best cut from measurement results"""
    def compute_cut_value(bitstring, graph):
        cut_value = 0
        for edge in graph.edges():
            if bitstring[edge[0]] != bitstring[edge[1]]:
                cut_value += 1
        return cut_value

    # Find bitstring with maximum cut
    best_cut = 0
    best_string = None

    for bitstring, count in counts.items():
        cut = compute_cut_value(bitstring, graph)
        if cut > best_cut:
            best_cut = cut
            best_string = bitstring

    return best_string, best_cut
```

### Advanced Post-Processing

**Error Mitigation Post-Processing:**
```python
# Apply additional classical error mitigation
from qiskit.result import marginal_counts

# Marginalize to relevant qubits
relevant_qubits = [0, 1, 2]
marginal = marginal_counts(counts, indices=relevant_qubits)
```

**Statistical Analysis:**
```python
import numpy as np

def analyze_results(results_list):
    """Analyze multiple runs for statistics"""
    energies = [r[0].data.evs for r in results_list]

    mean_energy = np.mean(energies)
    std_energy = np.std(energies)
    confidence_interval = 1.96 * std_energy / np.sqrt(len(energies))

    return {
        'mean': mean_energy,
        'std': std_energy,
        '95% CI': (mean_energy - confidence_interval, mean_energy + confidence_interval)
    }
```

**Visualization:**
```python
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Visualize results
plot_histogram(counts, figsize=(12, 6))
plt.title("Measurement Results")
plt.show()
```

## Complete Example: VQE for Chemistry

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator, Session
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# 1. MAP: Create parameterized circuit
def create_ansatz(num_qubits):
    qc = QuantumCircuit(num_qubits)
    params = []

    for i in range(num_qubits):
        theta = f'θ_{i}'
        params.append(theta)
        qc.ry(theta, i)

    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)

    return qc, params

# Define Hamiltonian (example: H2 molecule)
hamiltonian = SparsePauliOp(["IIZZ", "ZZII", "XXII", "IIXX"], coeffs=[0.3, 0.3, 0.1, 0.1])

# 2. OPTIMIZE: Connect and prepare
service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

ansatz, param_names = create_ansatz(num_qubits=4)

# 3. EXECUTE: Run VQE
def cost_function(params):
    # Bind parameters
    bound_circuit = ansatz.assign_parameters({param_names[i]: params[i] for i in range(len(params))})

    # Transpile
    qc_isa = transpile(bound_circuit, backend=backend, optimization_level=3)

    # Execute
    job = estimator.run([(qc_isa, hamiltonian)])
    result = job.result()
    energy = result[0].data.evs

    return energy

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    # Classical optimization loop
    initial_params = np.random.random(len(param_names)) * 2 * np.pi
    result = minimize(cost_function, initial_params, method='COBYLA')

# 4. POST-PROCESS: Extract ground state energy
ground_state_energy = result.fun
optimized_params = result.x

print(f"Ground state energy: {ground_state_energy}")
print(f"Optimized parameters: {optimized_params}")
```

## Best Practices

### 1. Iterate Locally First
Test the full workflow with simulators before using hardware:
```python
from qiskit.primitives import StatevectorEstimator

estimator = StatevectorEstimator()
# Test workflow locally
```

### 2. Use Sessions for Iterative Algorithms
VQE, QAOA, and other variational algorithms benefit from sessions.

### 3. Choose Appropriate Shots
- Development/testing: 100-1000 shots
- Production: 10,000+ shots

### 4. Monitor Convergence
```python
energies = []

def cost_function_with_tracking(params):
    energy = cost_function(params)
    energies.append(energy)
    print(f"Iteration {len(energies)}: E = {energy}")
    return energy
```

### 5. Save Results
```python
import json

results_data = {
    'energy': float(ground_state_energy),
    'parameters': optimized_params.tolist(),
    'iterations': len(energies),
    'backend': backend.name
}

with open('vqe_results.json', 'w') as f:
    json.dump(results_data, f, indent=2)
```

## Qiskit Serverless

For large-scale workflows, use Qiskit Serverless for distributed computation:

```python
from qiskit_serverless import ServerlessClient, QiskitFunction

client = ServerlessClient()

# Define serverless function
@QiskitFunction()
def run_vqe_serverless(hamiltonian, ansatz):
    # Your VQE implementation
    pass

# Execute remotely
job = run_vqe_serverless(hamiltonian, ansatz)
result = job.result()
```

## Common Workflow Patterns

### Pattern 1: Parameter Sweep
```python
# Map → Optimize once → Execute many → Post-process
qc_isa = transpile(parameterized_circuit, backend=backend)

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)
    results = []

    for param_set in parameter_sweep:
        bound_qc = qc_isa.assign_parameters(param_set)
        job = sampler.run([bound_qc], shots=1000)
        results.append(job.result())
```

### Pattern 2: Iterative Refinement
```python
# Map → (Optimize → Execute → Post-process) repeated
with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    for iteration in range(max_iter):
        qc = update_circuit(params)
        qc_isa = transpile(qc, backend=backend)

        result = estimator.run([(qc_isa, observable)]).result()
        params = update_params(result)
```

### Pattern 3: Ensemble Measurement
```python
# Map → Optimize → Execute many observables → Post-process
qc_isa = transpile(qc, backend=backend)

observables = [obs1, obs2, obs3, obs4]
jobs = [(qc_isa, obs) for obs in observables]

estimator = Estimator(backend)
result = estimator.run(jobs).result()
expectation_values = [r.data.evs for r in result]
```

---

## Reference: Primitives

# Qiskit Primitives

Primitives are the fundamental building blocks for executing quantum circuits. Qiskit provides two main primitives: **Sampler** (for measuring bitstrings) and **Estimator** (for computing expectation values).

## Primitive Types

### Sampler
Calculates probabilities or quasi-probabilities of bitstrings from quantum circuits. Use when you need:
- Measurement outcomes
- Output probability distributions
- Sampling from quantum states

### Estimator
Computes expectation values of observables for quantum circuits. Use when you need:
- Energy calculations
- Observable measurements
- Variational algorithm optimization

## V2 Interface (Current Standard)

Qiskit uses V2 primitives (BaseSamplerV2, BaseEstimatorV2) as the current standard. V1 primitives are legacy.

## Sampler Primitive

### StatevectorSampler (Local Simulation)

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run with Sampler
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()

# Access results
counts = result[0].data.meas.get_counts()
print(counts)  # e.g., {'00': 523, '11': 501}
```

### Multiple Circuits

```python
qc1 = QuantumCircuit(2)
qc1.h(0)
qc1.measure_all()

qc2 = QuantumCircuit(2)
qc2.x(0)
qc2.measure_all()

# Run multiple circuits
sampler = StatevectorSampler()
job = sampler.run([qc1, qc2], shots=1000)
results = job.result()

# Access individual results
counts1 = results[0].data.meas.get_counts()
counts2 = results[1].data.meas.get_counts()
```

### Using Parameters

```python
from qiskit.circuit import Parameter

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
qc.measure_all()

# Run with parameter values
sampler = StatevectorSampler()
param_values = [[0], [np.pi/4], [np.pi/2]]
result = sampler.run([(qc, param_values)], shots=1024).result()
```

## Estimator Primitive

### StatevectorEstimator (Local Simulation)

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# Create circuit WITHOUT measurements
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Define observable
observable = SparsePauliOp(["ZZ", "XX"])

# Run Estimator
estimator = StatevectorEstimator()
result = estimator.run([(qc, observable)]).result()

# Access expectation values
exp_value = result[0].data.evs
print(f"Expectation value: {exp_value}")
```

### Multiple Observables

```python
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(2)
qc.h(0)

obs1 = SparsePauliOp(["ZZ"])
obs2 = SparsePauliOp(["XX"])

estimator = StatevectorEstimator()
result = estimator.run([(qc, obs1), (qc, obs2)]).result()

ev1 = result[0].data.evs
ev2 = result[1].data.evs
```

### Parameterized Estimator

```python
from qiskit.circuit import Parameter
import numpy as np

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)

observable = SparsePauliOp(["Z"])

# Run with multiple parameter values
estimator = StatevectorEstimator()
param_values = [[0], [np.pi/4], [np.pi/2], [np.pi]]
result = estimator.run([(qc, observable, param_values)]).result()
```

## IBM Quantum Runtime Primitives

For running on real hardware, use runtime primitives:

### Runtime Sampler

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run on real hardware
sampler = Sampler(backend)
job = sampler.run([qc], shots=1024)
result = job.result()
counts = result[0].data.meas.get_counts()
```

### Runtime Estimator

```python
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
from qiskit.quantum_info import SparsePauliOp

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

observable = SparsePauliOp(["ZZ"])

# Run on real hardware
estimator = Estimator(backend)
job = estimator.run([(qc, observable)])
result = job.result()
exp_value = result[0].data.evs
```

## Sessions for Iterative Workloads

Sessions group multiple jobs to reduce queue wait times:

```python
from qiskit_ibm_runtime import Session

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Session(backend=backend) as session:
    sampler = Sampler(session=session)

    # Run multiple jobs in session
    job1 = sampler.run([qc1], shots=1024)
    result1 = job1.result()

    job2 = sampler.run([qc2], shots=1024)
    result2 = job2.result()
```

## Batch Mode for Parallel Jobs

Batch mode runs independent jobs in parallel:

```python
from qiskit_ibm_runtime import Batch

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)

    # Submit multiple independent jobs
    job1 = sampler.run([qc1], shots=1024)
    job2 = sampler.run([qc2], shots=1024)

    # Retrieve results when ready
    result1 = job1.result()
    result2 = job2.result()
```

## Result Processing

### Sampler Results

```python
result = sampler.run([qc], shots=1024).result()

# Get counts
counts = result[0].data.meas.get_counts()

# Get probabilities
probs = {k: v/1024 for k, v in counts.items()}

# Get metadata
metadata = result[0].metadata
```

### Estimator Results

```python
result = estimator.run([(qc, observable)]).result()

# Expectation value
exp_val = result[0].data.evs

# Standard deviation (if available)
std_dev = result[0].data.stds

# Metadata
metadata = result[0].metadata
```

## Differences from V1 Primitives

**V2 Improvements:**
- More flexible parameter binding
- Better result structure
- Improved performance
- Cleaner API design

**Migration from V1:**
- Use `StatevectorSampler` instead of `Sampler`
- Use `StatevectorEstimator` instead of `Estimator`
- Result access changed from `.result().quasi_dists[0]` to `.result()[0].data.meas.get_counts()`

---

## Reference: Setup

# Qiskit Setup and Installation

## Installation

Install Qiskit using uv:

```bash
uv pip install qiskit
```

For visualization capabilities:

```bash
uv pip install "qiskit[visualization]" matplotlib
```

## Python Environment Setup

Create and activate a virtual environment to isolate dependencies:

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

## Supported Python Versions

Check the [Qiskit PyPI page](https://pypi.org/project/qiskit/) for currently supported Python versions. As of 2025, Qiskit typically supports Python 3.8+.

## IBM Quantum Account Setup

To run circuits on real IBM Quantum hardware, you need an IBM Quantum account and API token.

### Creating an Account

1. Visit [IBM Quantum Platform](https://quantum.ibm.com/)
2. Sign up for a free account
3. Navigate to your account settings to retrieve your API token

### Configuring Authentication

Save your IBM Quantum credentials:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save credentials (first time only)
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_TOKEN"
)

# Later sessions - load saved credentials
service = QiskitRuntimeService()
```

### Environment Variable Method

Alternatively, set the API token as an environment variable:

```bash
export QISKIT_IBM_TOKEN="YOUR_IBM_QUANTUM_TOKEN"
```

## Local Development (No Account Required)

You can build and test quantum circuits locally without an IBM Quantum account using simulators:

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run locally with simulator
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
```

## Verifying Installation

Test your installation:

```python
import qiskit
print(qiskit.__version__)

from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
print("Qiskit installed successfully!")
```

---

## Reference: Transpilation

# Circuit Transpilation and Optimization

Transpilation is the process of rewriting a quantum circuit to match the topology and gate set of a specific quantum device, while optimizing for execution on noisy quantum computers.

## Why Transpilation?

**Problem**: Abstract quantum circuits may use gates not available on hardware and assume all-to-all qubit connectivity.

**Solution**: Transpilation transforms circuits to:
1. Use only hardware-native gates (basis gates)
2. Respect physical qubit connectivity
3. Minimize circuit depth and gate count
4. Optimize for reduced errors on noisy devices

## Basic Transpilation

### Simple Transpile

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

# Transpile for a specific backend
transpiled_qc = transpile(qc, backend=backend)
```

### Optimization Levels

Choose optimization level 0-3:

```python
# Level 0: No optimization (fastest)
qc_0 = transpile(qc, backend=backend, optimization_level=0)

# Level 1: Light optimization
qc_1 = transpile(qc, backend=backend, optimization_level=1)

# Level 2: Moderate optimization (default)
qc_2 = transpile(qc, backend=backend, optimization_level=2)

# Level 3: Heavy optimization (slowest, best results)
qc_3 = transpile(qc, backend=backend, optimization_level=3)
```

**Qiskit SDK v2.2** provides **83x faster transpilation** compared to competitors.

## Transpilation Stages

The transpiler pipeline consists of six stages:

### 1. Init Stage
- Validates circuit instructions
- Translates multi-qubit gates to standard form

### 2. Layout Stage
- Maps virtual qubits to physical qubits
- Considers qubit connectivity and error rates

```python
from qiskit.transpiler import CouplingMap

# Define custom coupling
coupling = CouplingMap([(0, 1), (1, 2), (2, 3)])
qc_transpiled = transpile(qc, coupling_map=coupling)
```

### 3. Routing Stage
- Inserts SWAP gates to satisfy connectivity constraints
- Minimizes additional SWAP overhead

### 4. Translation Stage
- Converts gates to hardware basis gates
- Typical basis: {RZ, SX, X, CX}

```python
# Specify basis gates
basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
qc_transpiled = transpile(qc, basis_gates=basis_gates)
```

### 5. Optimization Stage
- Reduces gate count and circuit depth
- Applies gate cancellation and commutation rules
- Uses **virtual permutation elision** (levels 2-3)
- Finds separable operations to decompose

### 6. Scheduling Stage
- Adds timing information for pulse-level control

## Advanced Optimization Features

### Virtual Permutation Elision

At optimization levels 2-3, Qiskit analyzes commutation structure to eliminate unnecessary SWAP gates by tracking virtual qubit permutations.

### Gate Cancellation

Identifies and removes pairs of gates that cancel:
- X-X → I
- H-H → I
- CNOT-CNOT → I

### Numerical Decomposition

Splits two-qubit gates that can be expressed as separable one-qubit operations.

## Common Transpilation Parameters

### Initial Layout

Specify which physical qubits to use:

```python
# Use specific physical qubits
initial_layout = [0, 2, 4]  # Maps circuit qubits 0,1,2 to physical qubits 0,2,4
qc_transpiled = transpile(qc, backend=backend, initial_layout=initial_layout)
```

### Approximation Degree

Trade accuracy for fewer gates (0.0 = max approximation, 1.0 = no approximation):

```python
# Allow 5% approximation error for fewer gates
qc_transpiled = transpile(qc, backend=backend, approximation_degree=0.95)
```

### Seed for Reproducibility

```python
qc_transpiled = transpile(qc, backend=backend, seed_transpiler=42)
```

### Scheduling Method

```python
# Add timing constraints
qc_transpiled = transpile(
    qc,
    backend=backend,
    scheduling_method='alap'  # As Late As Possible
)
```

## Transpiling for Simulators

Even for simulators, transpilation can optimize circuits:

```python
from qiskit_aer import AerSimulator

simulator = AerSimulator()
qc_optimized = transpile(qc, backend=simulator, optimization_level=3)

# Compare gate counts
print(f"Original: {qc.size()} gates")
print(f"Optimized: {qc_optimized.size()} gates")
```

## Target-Aware Transpilation

Use `Target` objects for detailed backend specifications:

```python
from qiskit.transpiler import Target

# Transpile with target specification
qc_transpiled = transpile(qc, target=backend.target)
```

## Circuit Analysis After Transpilation

```python
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)

# Analyze results
print(f"Depth: {qc_transpiled.depth()}")
print(f"Gate count: {qc_transpiled.size()}")
print(f"Operations: {qc_transpiled.count_ops()}")

# Check two-qubit gate count (major error source)
two_qubit_gates = qc_transpiled.count_ops().get('cx', 0)
print(f"Two-qubit gates: {two_qubit_gates}")
```

**Qiskit produces circuits with 29% fewer two-qubit gates** than leading alternatives, significantly reducing errors.

## Multiple Circuit Transpilation

Transpile multiple circuits efficiently:

```python
circuits = [qc1, qc2, qc3]
transpiled_circuits = transpile(
    circuits,
    backend=backend,
    optimization_level=3
)
```

## Pre-transpilation Best Practices

### 1. Design with Hardware Topology in Mind

Consider backend coupling map when designing circuits:

```python
# Check backend coupling
print(backend.coupling_map)

# Design circuits that align with coupling
```

### 2. Use Native Gates When Possible

Some backends support gates beyond {CX, RZ, SX, X}:

```python
# Check available basis gates
print(backend.configuration().basis_gates)
```

### 3. Minimize Two-Qubit Gates

Two-qubit gates have significantly higher error rates:
- Design algorithms to minimize CNOT gates
- Use gate identities to reduce counts

### 4. Test with Simulators First

```python
from qiskit_aer import AerSimulator

# Test transpilation locally
sim_backend = AerSimulator.from_backend(backend)
qc_test = transpile(qc, backend=sim_backend, optimization_level=3)
```

## Transpilation for Different Providers

### IBM Quantum

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")
qc_transpiled = transpile(qc, backend=backend)
```

### IonQ

```python
# IonQ has all-to-all connectivity, different basis gates
basis_gates = ['gpi', 'gpi2', 'ms']
qc_transpiled = transpile(qc, basis_gates=basis_gates)
```

### Amazon Braket

Transpilation depends on specific device (Rigetti, IonQ, etc.)

## Performance Tips

1. **Cache transpiled circuits** - Transpilation is expensive, reuse when possible
2. **Use appropriate optimization level** - Level 3 is slow but best for production
3. **Leverage v2.2 speed improvements** - Update to latest Qiskit for 83x speedup
4. **Parallelize transpilation** - Qiskit automatically parallelizes when transpiling multiple circuits

## Common Issues and Solutions

### Issue: Circuit too deep after transpilation
**Solution**: Use higher optimization level or redesign circuit with fewer layers

### Issue: Too many SWAP gates inserted
**Solution**: Adjust initial_layout to better match qubit topology

### Issue: Transpilation takes too long
**Solution**: Reduce optimization level or update to Qiskit v2.2+ for speed improvements

### Issue: Unexpected gate decompositions
**Solution**: Check basis_gates and consider specifying custom decomposition rules

---

## Reference: Visualization

# Visualization in Qiskit

Qiskit provides comprehensive visualization tools for quantum circuits, measurement results, and quantum states.

## Installation

Install visualization dependencies:

```bash
uv pip install "qiskit[visualization]" matplotlib
```

## Circuit Visualization

### Text-Based Drawings

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

# Simple text output
print(qc.draw())

# Text with more detail
print(qc.draw('text', fold=-1))  # Don't fold long circuits
```

### Matplotlib Drawings

```python
# High-quality matplotlib figure
qc.draw('mpl')

# Save to file
fig = qc.draw('mpl')
fig.savefig('circuit.png', dpi=300, bbox_inches='tight')
```

### LaTeX Drawings

```python
# Generate LaTeX circuit diagram
qc.draw('latex')

# Save LaTeX source
latex_source = qc.draw('latex_source')
with open('circuit.tex', 'w') as f:
    f.write(latex_source)
```

## Customizing Circuit Drawings

### Styling Options

```python
from qiskit.visualization import circuit_drawer

# Reverse qubit order
qc.draw('mpl', reverse_bits=True)

# Fold long circuits
qc.draw('mpl', fold=20)  # Fold at 20 columns

# Show idle wires
qc.draw('mpl', idle_wires=False)

# Add initial state
qc.draw('mpl', initial_state=True)
```

### Color Customization

```python
style = {
    'displaycolor': {
        'h': ('#FA74A6', '#000000'),     # Hadamard: pink
        'cx': ('#A8D0DB', '#000000'),    # CNOT: light blue
        'measure': ('#F7E7B4', '#000000') # Measure: yellow
    }
}

qc.draw('mpl', style=style)
```

## Result Visualization

### Histogram of Counts

```python
from qiskit.visualization import plot_histogram
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()

# Plot histogram
plot_histogram(counts)

# Compare multiple experiments
counts1 = {'00': 500, '11': 524}
counts2 = {'00': 480, '11': 544}
plot_histogram([counts1, counts2], legend=['Run 1', 'Run 2'])

# Save figure
fig = plot_histogram(counts)
fig.savefig('histogram.png', dpi=300, bbox_inches='tight')
```

### Histogram Options

```python
# Customize colors
plot_histogram(counts, color=['#1f77b4', '#ff7f0e'])

# Sort by value
plot_histogram(counts, sort='value')

# Set bar labels
plot_histogram(counts, bar_labels=True)

# Set target distribution (for comparison)
target = {'00': 0.5, '11': 0.5}
plot_histogram(counts, target=target)
```

## State Visualization

### Bloch Sphere

Visualize single-qubit states on the Bloch sphere:

```python
from qiskit.visualization import plot_bloch_vector
from qiskit.quantum_info import Statevector
import numpy as np

# Visualize a specific state vector
# State |+⟩: equal superposition of |0⟩ and |1⟩
state = Statevector.from_label('+')
plot_bloch_vector(state.to_bloch())

# Custom vector
plot_bloch_vector([0, 1, 0])  # |+⟩ state on X-axis
```

### Multi-Qubit Bloch Sphere

```python
from qiskit.visualization import plot_bloch_multivector

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

state = Statevector.from_instruction(qc)
plot_bloch_multivector(state)
```

### State City Plot

Visualize state amplitudes as a 3D city:

```python
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(3)
qc.h(range(3))
state = Statevector.from_instruction(qc)

plot_state_city(state)

# Customize
plot_state_city(state, color=['#FF6B6B', '#4ECDC4'])
```

### QSphere

Visualize quantum states on a sphere:

```python
from qiskit.visualization import plot_state_qsphere

state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

### Hinton Diagram

Display state amplitudes:

```python
from qiskit.visualization import plot_state_hinton

state = Statevector.from_instruction(qc)
plot_state_hinton(state)
```

## Density Matrix Visualization

```python
from qiskit.visualization import plot_state_density
from qiskit.quantum_info import DensityMatrix

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

state = DensityMatrix.from_instruction(qc)
plot_state_density(state)
```

## Gate Map Visualization

Visualize backend coupling map:

```python
from qiskit.visualization import plot_gate_map
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Show qubit connectivity
plot_gate_map(backend)

# Show with error rates
plot_gate_map(backend, plot_error_rates=True)
```

## Error Map Visualization

Display backend error rates:

```python
from qiskit.visualization import plot_error_map

plot_error_map(backend)
```

## Circuit Properties Display

```python
from qiskit.visualization import plot_circuit_layout

# Show how circuit maps to physical qubits
transpiled_qc = transpile(qc, backend=backend)
plot_circuit_layout(transpiled_qc, backend)
```

## Pulse Visualization

For pulse-level control:

```python
from qiskit import pulse
from qiskit.visualization import pulse_drawer

# Create pulse schedule
with pulse.build(backend) as schedule:
    pulse.play(pulse.Gaussian(duration=160, amp=0.1, sigma=40), pulse.drive_channel(0))

# Visualize
schedule.draw()
```

## Interactive Widgets (Jupyter)

### Circuit Composer Widget

```python
from qiskit.tools.jupyter import QuantumCircuitComposer

composer = QuantumCircuitComposer()
composer.show()
```

### Interactive State Visualization

```python
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Enable interactive mode
plt.ion()
plot_histogram(counts)
plt.show()
```

## Comparison Plots

### Multiple Histograms

```python
# Compare results from different backends
counts_sim = {'00': 500, '11': 524}
counts_hw = {'00': 480, '01': 20, '10': 24, '11': 500}

plot_histogram(
    [counts_sim, counts_hw],
    legend=['Simulator', 'Hardware'],
    figsize=(12, 6)
)
```

### Before/After Transpilation

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

# Original circuit
qc.draw('mpl', ax=ax1)
ax1.set_title('Original Circuit')

# Transpiled circuit
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
qc_transpiled.draw('mpl', ax=ax2)
ax2.set_title('Transpiled Circuit')

plt.tight_layout()
plt.show()
```

## Saving Visualizations

### Save to Various Formats

```python
# PNG
fig = qc.draw('mpl')
fig.savefig('circuit.png', dpi=300, bbox_inches='tight')

# PDF
fig.savefig('circuit.pdf', bbox_inches='tight')

# SVG (vector graphics)
fig.savefig('circuit.svg', bbox_inches='tight')

# Histogram
hist_fig = plot_histogram(counts)
hist_fig.savefig('results.png', dpi=300, bbox_inches='tight')
```

## Styling Best Practices

### Publication-Quality Figures

```python
import matplotlib.pyplot as plt

# Set matplotlib style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'sans-serif'

# Create high-quality visualization
fig = qc.draw('mpl', style='iqp')
fig.savefig('publication_circuit.png', dpi=600, bbox_inches='tight')
```

### Available Styles

```python
# Default style
qc.draw('mpl')

# IQP style (IBM Quantum)
qc.draw('mpl', style='iqp')

# Colorblind-friendly
qc.draw('mpl', style='bw')  # Black and white
```

## Troubleshooting Visualization

### Common Issues

**Issue**: "No module named 'matplotlib'"
```bash
uv pip install matplotlib
```

**Issue**: Circuit too large to display
```python
# Use folding
qc.draw('mpl', fold=50)

# Or export to file instead of displaying
fig = qc.draw('mpl')
fig.savefig('large_circuit.png', dpi=150, bbox_inches='tight')
```

**Issue**: Jupyter notebook not displaying plots
```python
# Add magic command at notebook start
%matplotlib inline
```

**Issue**: LaTeX visualization not working
```bash
# Install LaTeX support
uv pip install pylatexenc
```
