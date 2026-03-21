---
title: "QuTiP 量子模拟"
description: "开放量子系统动力学模拟工具包，量子光学和量子信息"
category: "research"
source: "community"
author: "Community"
tags: ["qutip"]
date: 2026-03-20
---

# QuTiP: Quantum Toolbox in Python

## Overview

QuTiP provides comprehensive tools for simulating and analyzing quantum mechanical systems. It handles both closed (unitary) and open (dissipative) quantum systems with multiple solvers optimized for different scenarios.

## Installation

```bash
uv pip install qutip
```

Optional packages for additional functionality:

```bash
# Quantum information processing (circuits, gates)
uv pip install qutip-qip

# Quantum trajectory viewer
uv pip install qutip-qtrl
```

## Quick Start

```python
from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Create quantum state
psi = basis(2, 0)  # |0⟩ state

# Create operator
H = sigmaz()  # Hamiltonian

# Time evolution
tlist = np.linspace(0, 10, 100)
result = sesolve(H, psi, tlist, e_ops=[sigmaz()])

# Plot results
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

## Core Capabilities

### 1. Quantum Objects and States

Create and manipulate quantum states and operators:

```python
# States
psi = basis(N, n)  # Fock state |n⟩
psi = coherent(N, alpha)  # Coherent state |α⟩
rho = thermal_dm(N, n_avg)  # Thermal density matrix

# Operators
a = destroy(N)  # Annihilation operator
H = num(N)  # Number operator
sx, sy, sz = sigmax(), sigmay(), sigmaz()  # Pauli matrices

# Composite systems
psi_AB = tensor(psi_A, psi_B)  # Tensor product
```

**See** `references/core_concepts.md` for comprehensive coverage of quantum objects, states, operators, and tensor products.

### 2. Time Evolution and Dynamics

Multiple solvers for different scenarios:

```python
# Closed systems (unitary evolution)
result = sesolve(H, psi0, tlist, e_ops=[num(N)])

# Open systems (dissipation)
c_ops = [np.sqrt(0.1) * destroy(N)]  # Collapse operators
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Quantum trajectories (Monte Carlo)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=500, e_ops=[num(N)])
```

**Solver selection guide:**
- `sesolve`: Pure states, unitary evolution
- `mesolve`: Mixed states, dissipation, general open systems
- `mcsolve`: Quantum jumps, photon counting, individual trajectories
- `brmesolve`: Weak system-bath coupling
- `fmmesolve`: Time-periodic Hamiltonians (Floquet)

**See** `references/time_evolution.md` for detailed solver documentation, time-dependent Hamiltonians, and advanced options.

### 3. Analysis and Measurement

Compute physical quantities:

```python
# Expectation values
n_avg = expect(num(N), psi)

# Entropy measures
S = entropy_vn(rho)  # Von Neumann entropy
C = concurrence(rho)  # Entanglement (two qubits)

# Fidelity and distance
F = fidelity(psi1, psi2)
D = tracedist(rho1, rho2)

# Correlation functions
corr = correlation_2op_1t(H, rho0, taulist, c_ops, A, B)
w, S = spectrum_correlation_fft(taulist, corr)

# Steady states
rho_ss = steadystate(H, c_ops)
```

**See** `references/analysis.md` for entropy, fidelity, measurements, correlation functions, and steady state calculations.

### 4. Visualization

Visualize quantum states and dynamics:

```python
# Bloch sphere
b = Bloch()
b.add_states(psi)
b.show()

# Wigner function (phase space)
xvec = np.linspace(-5, 5, 200)
W = wigner(psi, xvec, xvec)
plt.contourf(xvec, xvec, W, 100, cmap='RdBu')

# Fock distribution
plot_fock_distribution(psi)

# Matrix visualization
hinton(rho)  # Hinton diagram
matrix_histogram(H.full())  # 3D bars
```

**See** `references/visualization.md` for Bloch sphere animations, Wigner functions, Q-functions, and matrix visualizations.

### 5. Advanced Methods

Specialized techniques for complex scenarios:

```python
# Floquet theory (periodic Hamiltonians)
T = 2 * np.pi / w_drive
f_modes, f_energies = floquet_modes(H, T, args)
result = fmmesolve(H, psi0, tlist, c_ops, T=T, args=args)

# HEOM (non-Markovian, strong coupling)
from qutip.nonmarkov.heom import HEOMSolver, BosonicBath
bath = BosonicBath(Q, ck_real, vk_real)
hsolver = HEOMSolver(H_sys, [bath], max_depth=5)
result = hsolver.run(rho0, tlist)

# Permutational invariance (identical particles)
psi = dicke(N, j, m)  # Dicke states
Jz = jspin(N, 'z')  # Collective operators
```

**See** `references/advanced.md` for Floquet theory, HEOM, permutational invariance, stochastic solvers, superoperators, and performance optimization.

## Common Workflows

### Simulating a Damped Harmonic Oscillator

```python
# System parameters
N = 20  # Hilbert space dimension
omega = 1.0  # Oscillator frequency
kappa = 0.1  # Decay rate

# Hamiltonian and collapse operators
H = omega * num(N)
c_ops = [np.sqrt(kappa) * destroy(N)]

# Initial state
psi0 = coherent(N, 3.0)

# Time evolution
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Visualize
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨n⟩')
plt.title('Photon Number Decay')
plt.show()
```

### Two-Qubit Entanglement Dynamics

```python
# Create Bell state
psi0 = bell_state('00')

# Local dephasing on each qubit
gamma = 0.1
c_ops = [
    np.sqrt(gamma) * tensor(sigmaz(), qeye(2)),
    np.sqrt(gamma) * tensor(qeye(2), sigmaz())
]

# Track entanglement
def compute_concurrence(t, psi):
    rho = ket2dm(psi) if psi.isket else psi
    return concurrence(rho)

tlist = np.linspace(0, 10, 100)
result = mesolve(qeye([2, 2]), psi0, tlist, c_ops)

# Compute concurrence for each state
C_t = [concurrence(state.proj()) for state in result.states]

plt.plot(tlist, C_t)
plt.xlabel('Time')
plt.ylabel('Concurrence')
plt.title('Entanglement Decay')
plt.show()
```

### Jaynes-Cummings Model

```python
# System parameters
N = 10  # Cavity Fock space
wc = 1.0  # Cavity frequency
wa = 1.0  # Atom frequency
g = 0.05  # Coupling strength

# Operators
a = tensor(destroy(N), qeye(2))  # Cavity
sm = tensor(qeye(N), sigmam())  # Atom

# Hamiltonian (RWA)
H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())

# Initial state: cavity in coherent state, atom in ground state
psi0 = tensor(coherent(N, 2), basis(2, 0))

# Dissipation
kappa = 0.1  # Cavity decay
gamma = 0.05  # Atomic decay
c_ops = [np.sqrt(kappa) * a, np.sqrt(gamma) * sm]

# Observables
n_cav = a.dag() * a
n_atom = sm.dag() * sm

# Evolve
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[n_cav, n_atom])

# Plot
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
axes[0].plot(tlist, result.expect[0])
axes[0].set_ylabel('⟨n_cavity⟩')
axes[1].plot(tlist, result.expect[1])
axes[1].set_ylabel('⟨n_atom⟩')
axes[1].set_xlabel('Time')
plt.tight_layout()
plt.show()
```

## Tips for Efficient Simulations

1. **Truncate Hilbert spaces**: Use smallest dimension that captures dynamics
2. **Choose appropriate solver**: `sesolve` for pure states is faster than `mesolve`
3. **Time-dependent terms**: String format (e.g., `'cos(w*t)'`) is fastest
4. **Store only needed data**: Use `e_ops` instead of storing all states
5. **Adjust tolerances**: Balance accuracy with computation time via `Options`
6. **Parallel trajectories**: `mcsolve` automatically uses multiple CPUs
7. **Check convergence**: Vary `ntraj`, Hilbert space size, and tolerances

## Troubleshooting

**Memory issues**: Reduce Hilbert space dimension, use `store_final_state` option, or consider Krylov methods

**Slow simulations**: Use string-based time-dependence, increase tolerances slightly, or try `method='bdf'` for stiff problems

**Numerical instabilities**: Decrease time steps (`nsteps` option), increase tolerances, or check Hamiltonian/operators are properly defined

**Import errors**: Ensure QuTiP is installed correctly; quantum gates require `qutip-qip` package

## References

This skill includes detailed reference documentation:

- **`references/core_concepts.md`**: Quantum objects, states, operators, tensor products, composite systems
- **`references/time_evolution.md`**: All solvers (sesolve, mesolve, mcsolve, brmesolve, etc.), time-dependent Hamiltonians, solver options
- **`references/visualization.md`**: Bloch sphere, Wigner functions, Q-functions, Fock distributions, matrix plots
- **`references/analysis.md`**: Expectation values, entropy, fidelity, entanglement measures, correlation functions, steady states
- **`references/advanced.md`**: Floquet theory, HEOM, permutational invariance, stochastic methods, superoperators, performance tips

## External Resources

- Documentation: https://qutip.readthedocs.io/
- Tutorials: https://qutip.org/qutip-tutorials/
- API Reference: https://qutip.readthedocs.io/en/stable/apidoc/apidoc.html
- GitHub: https://github.com/qutip/qutip

---

## Reference: Advanced

# QuTiP Advanced Features

## Floquet Theory

For time-periodic Hamiltonians H(t + T) = H(t).

### Floquet Modes and Quasi-Energies

```python
from qutip import *
import numpy as np

# Time-periodic Hamiltonian
w_d = 1.0  # Drive frequency
T = 2 * np.pi / w_d  # Period

H0 = sigmaz()
H1 = sigmax()
H = [H0, [H1, 'cos(w*t)']]
args = {'w': w_d}

# Calculate Floquet modes and quasi-energies
f_modes, f_energies = floquet_modes(H, T, args)

print("Quasi-energies:", f_energies)
print("Floquet modes:", f_modes)
```

### Floquet States at Time t

```python
# Get Floquet state at specific time
t = 1.0
f_states_t = floquet_states(f_modes, f_energies, t)
```

### Floquet State Decomposition

```python
# Decompose initial state in Floquet basis
psi0 = basis(2, 0)
f_coeff = floquet_state_decomposition(f_modes, f_energies, psi0)
```

### Floquet-Markov Master Equation

```python
# Time evolution with dissipation
c_ops = [np.sqrt(0.1) * sigmam()]
tlist = np.linspace(0, 20, 200)

result = fmmesolve(H, psi0, tlist, c_ops, e_ops=[sigmaz()], T=T, args=args)

# Plot results
import matplotlib.pyplot as plt
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

### Floquet Tensor

```python
# Floquet tensor (generalized Bloch-Redfield)
A_ops = [[sigmaz(), lambda w: 0.1 * w if w > 0 else 0]]

# Build Floquet tensor
R, U = floquet_markov_mesolve(H, psi0, tlist, A_ops, e_ops=[sigmaz()],
                               T=T, args=args)
```

### Effective Hamiltonian

```python
# Time-averaged effective Hamiltonian
H_eff = floquet_master_equation_steadystate(H, c_ops, T, args)
```

## Hierarchical Equations of Motion (HEOM)

For non-Markovian open quantum systems with strong system-bath coupling.

### Basic HEOM Setup

```python
from qutip import heom

# System Hamiltonian
H_sys = sigmaz()

# Bath correlation function (exponential)
Q = sigmax()  # System-bath coupling operator
ck_real = [0.1]  # Coupling strengths
vk_real = [0.5]  # Bath frequencies

# HEOM bath
bath = heom.BosonicBath(Q, ck_real, vk_real)

# Initial state
rho0 = basis(2, 0) * basis(2, 0).dag()

# Create HEOM solver
max_depth = 5
hsolver = heom.HEOMSolver(H_sys, [bath], max_depth=max_depth)

# Time evolution
tlist = np.linspace(0, 10, 100)
result = hsolver.run(rho0, tlist)

# Extract reduced system density matrix
rho_sys = [r.extract_state(0) for r in result.states]
```

### Multiple Baths

```python
# Define multiple baths
bath1 = heom.BosonicBath(sigmax(), [0.1], [0.5])
bath2 = heom.BosonicBath(sigmay(), [0.05], [1.0])

hsolver = heom.HEOMSolver(H_sys, [bath1, bath2], max_depth=5)
```

### Drude-Lorentz Spectral Density

```python
# Common in condensed matter physics
from qutip.nonmarkov.heom import DrudeLorentzBath

lam = 0.1  # Reorganization energy
gamma = 0.5  # Bath cutoff frequency
T = 1.0  # Temperature (in energy units)
Nk = 2  # Number of Matsubara terms

bath = DrudeLorentzBath(Q, lam, gamma, T, Nk)
```

### HEOM Options

```python
options = heom.HEOMSolver.Options(
    nsteps=2000,
    store_states=True,
    rtol=1e-7,
    atol=1e-9
)

hsolver = heom.HEOMSolver(H_sys, [bath], max_depth=5, options=options)
```

## Permutational Invariance

For identical particle systems (e.g., spin ensembles).

### Dicke States

```python
from qutip import dicke

# Dicke state |j, m⟩ for N spins
N = 10  # Number of spins
j = N/2  # Total angular momentum
m = 0   # z-component

psi = dicke(N, j, m)
```

### Permutation-Invariant Operators

```python
from qutip.piqs import jspin

# Collective spin operators
N = 10
Jx = jspin(N, 'x')
Jy = jspin(N, 'y')
Jz = jspin(N, 'z')
Jp = jspin(N, '+')
Jm = jspin(N, '-')
```

### PIQS Dynamics

```python
from qutip.piqs import Dicke

# Setup Dicke model
N = 10
emission = 1.0
dephasing = 0.5
pumping = 0.0
collective_emission = 0.0

system = Dicke(N=N, emission=emission, dephasing=dephasing,
               pumping=pumping, collective_emission=collective_emission)

# Initial state
psi0 = dicke(N, N/2, N/2)  # All spins up

# Time evolution
tlist = np.linspace(0, 10, 100)
result = system.solve(psi0, tlist, e_ops=[Jz])
```

## Non-Markovian Monte Carlo

Quantum trajectories with memory effects.

```python
from qutip import nm_mcsolve

# Non-Markovian bath correlation
def bath_correlation(t1, t2):
    tau = abs(t2 - t1)
    return np.exp(-tau / 2.0) * np.cos(tau)

# System setup
H = sigmaz()
c_ops = [sigmax()]
psi0 = basis(2, 0)
tlist = np.linspace(0, 10, 100)

# Solve with memory
result = nm_mcsolve(H, psi0, tlist, c_ops, sc_ops=[],
                     bath_corr=bath_correlation, ntraj=500,
                     e_ops=[sigmaz()])
```

## Stochastic Solvers with Measurements

### Continuous Measurement

```python
# Homodyne detection
sc_ops = [np.sqrt(0.1) * destroy(N)]  # Measurement operator

result = ssesolve(H, psi0, tlist, sc_ops=sc_ops,
                   e_ops=[num(N)], ntraj=100,
                   noise=11)  # 11 for homodyne

# Heterodyne detection
result = ssesolve(H, psi0, tlist, sc_ops=sc_ops,
                   e_ops=[num(N)], ntraj=100,
                   noise=12)  # 12 for heterodyne
```

### Photon Counting

```python
# Quantum jump times
result = mcsolve(H, psi0, tlist, c_ops, ntraj=50,
                 options=Options(store_states=True))

# Extract measurement times
for i, jump_times in enumerate(result.col_times):
    print(f"Trajectory {i} jump times: {jump_times}")
    print(f"Which operator: {result.col_which[i]}")
```

## Krylov Subspace Methods

Efficient for large systems.

```python
from qutip import krylovsolve

# Use Krylov solver
result = krylovsolve(H, psi0, tlist, krylov_dim=10, e_ops=[num(N)])
```

## Bloch-Redfield Master Equation

For weak system-bath coupling.

```python
# Bath spectral density
def ohmic_spectrum(w):
    if w >= 0:
        return 0.1 * w  # Ohmic
    else:
        return 0

# Coupling operators and spectra
a_ops = [[sigmax(), ohmic_spectrum]]

# Solve
result = brmesolve(H, psi0, tlist, a_ops, e_ops=[sigmaz()])
```

### Temperature-Dependent Bath

```python
def thermal_spectrum(w):
    # Bose-Einstein distribution
    T = 1.0  # Temperature
    if abs(w) < 1e-10:
        return 0.1 * T
    n_th = 1 / (np.exp(abs(w)/T) - 1)
    if w >= 0:
        return 0.1 * w * (n_th + 1)
    else:
        return 0.1 * abs(w) * n_th

a_ops = [[sigmax(), thermal_spectrum]]
result = brmesolve(H, psi0, tlist, a_ops, e_ops=[sigmaz()])
```

## Superoperators and Quantum Channels

### Superoperator Representations

```python
# Liouvillian
L = liouvillian(H, c_ops)

# Convert between representations
from qutip import (spre, spost, sprepost,
                    super_to_choi, choi_to_super,
                    super_to_kraus, kraus_to_super)

# Superoperator forms
L_spre = spre(H)  # Left multiplication
L_spost = spost(H)  # Right multiplication
L_sprepost = sprepost(H, H.dag())

# Choi matrix
choi = super_to_choi(L)

# Kraus operators
kraus = super_to_kraus(L)
```

### Quantum Channels

```python
# Depolarizing channel
p = 0.1  # Error probability
K0 = np.sqrt(1 - 3*p/4) * qeye(2)
K1 = np.sqrt(p/4) * sigmax()
K2 = np.sqrt(p/4) * sigmay()
K3 = np.sqrt(p/4) * sigmaz()

kraus_ops = [K0, K1, K2, K3]
E = kraus_to_super(kraus_ops)

# Apply channel
rho_out = E * operator_to_vector(rho_in)
rho_out = vector_to_operator(rho_out)
```

### Amplitude Damping

```python
# T1 decay
gamma = 0.1
K0 = Qobj([[1, 0], [0, np.sqrt(1 - gamma)]])
K1 = Qobj([[0, np.sqrt(gamma)], [0, 0]])

E_damping = kraus_to_super([K0, K1])
```

### Phase Damping

```python
# T2 dephasing
gamma = 0.1
K0 = Qobj([[1, 0], [0, np.sqrt(1 - gamma/2)]])
K1 = Qobj([[0, 0], [0, np.sqrt(gamma/2)]])

E_dephasing = kraus_to_super([K0, K1])
```

## Quantum Trajectories Analysis

### Extract Individual Trajectories

```python
options = Options(store_states=True, store_final_state=False)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=100, options=options)

# Access individual trajectories
for i in range(len(result.states)):
    trajectory = result.states[i]  # List of states for trajectory i
    # Analyze trajectory
```

### Trajectory Statistics

```python
# Mean and standard deviation
result = mcsolve(H, psi0, tlist, c_ops, e_ops=[num(N)], ntraj=500)

n_mean = result.expect[0]
n_std = result.std_expect[0]

# Photon number distribution at final time
final_states = [result.states[i][-1] for i in range(len(result.states))]
```

## Time-Dependent Terms Advanced

### QobjEvo

```python
from qutip import QobjEvo

# Time-dependent Hamiltonian with QobjEvo
def drive(t, args):
    return args['A'] * np.exp(-t/args['tau']) * np.sin(args['w'] * t)

H0 = num(N)
H1 = destroy(N) + create(N)
args = {'A': 1.0, 'w': 1.0, 'tau': 5.0}

H_td = QobjEvo([H0, [H1, drive]], args=args)

# Can update args without recreating
H_td.arguments({'A': 2.0, 'w': 1.5, 'tau': 10.0})
```

### Compiled Time-Dependent Terms

```python
# Fastest method (requires Cython)
H = [num(N), [destroy(N) + create(N), 'A * exp(-t/tau) * sin(w*t)']]
args = {'A': 1.0, 'w': 1.0, 'tau': 5.0}

# QuTiP compiles this for speed
result = sesolve(H, psi0, tlist, args=args)
```

### Callback Functions

```python
# Advanced control
def time_dependent_coeff(t, args):
    # Access solver state if needed
    return complex_function(t, args)

H = [H0, [H1, time_dependent_coeff]]
```

## Parallel Processing

### Parallel Map

```python
from qutip import parallel_map

# Define task
def simulate(gamma):
    c_ops = [np.sqrt(gamma) * destroy(N)]
    result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
    return result.expect[0]

# Run in parallel
gamma_values = np.linspace(0, 1, 20)
results = parallel_map(simulate, gamma_values, num_cpus=4)
```

### Serial Map (for debugging)

```python
from qutip import serial_map

# Same interface but runs serially
results = serial_map(simulate, gamma_values)
```

## File I/O

### Save/Load Quantum Objects

```python
# Save
H.save('hamiltonian.qu')
psi.save('state.qu')

# Load
H_loaded = qload('hamiltonian.qu')
psi_loaded = qload('state.qu')
```

### Save/Load Results

```python
# Save simulation results
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
result.save('simulation.dat')

# Load results
from qutip import Result
loaded_result = Result.load('simulation.dat')
```

### Export to MATLAB

```python
# Export to .mat file
H.matlab_export('hamiltonian.mat', 'H')
```

## Solver Options

### Fine-Tuning Solvers

```python
options = Options()

# Integration parameters
options.nsteps = 10000  # Max internal steps
options.rtol = 1e-8     # Relative tolerance
options.atol = 1e-10    # Absolute tolerance

# Method selection
options.method = 'adams'  # Non-stiff (default)
# options.method = 'bdf'  # Stiff problems

# Storage options
options.store_states = True
options.store_final_state = True

# Progress
options.progress_bar = True

# Random number seed (for reproducibility)
options.seeds = 12345

result = mesolve(H, psi0, tlist, c_ops, options=options)
```

### Debugging

```python
# Enable detailed output
options.verbose = True

# Memory tracking
options.num_cpus = 1  # Easier debugging
```

## Performance Tips

1. **Use sparse matrices**: QuTiP does this automatically
2. **Minimize Hilbert space**: Truncate when possible
3. **Choose right solver**:
   - Pure states: `sesolve` faster than `mesolve`
   - Stochastic: `mcsolve` for quantum jumps
   - Periodic: Floquet methods
4. **Time-dependent terms**: String format fastest
5. **Expectation values**: Only compute needed observables
6. **Parallel trajectories**: `mcsolve` uses all CPUs
7. **Krylov methods**: For very large systems
8. **Memory**: Use `store_final_state` instead of `store_states` when possible

---

## Reference: Analysis

# QuTiP Analysis and Measurement

## Expectation Values

### Basic Expectation Values

```python
from qutip import *
import numpy as np

# Single operator
psi = coherent(N, 2)
n_avg = expect(num(N), psi)

# Multiple operators
ops = [num(N), destroy(N), create(N)]
results = expect(ops, psi)  # Returns list
```

### Expectation Values for Density Matrices

```python
# Works with both pure states and density matrices
rho = thermal_dm(N, 2)
n_avg = expect(num(N), rho)
```

### Variance

```python
# Calculate variance of observable
var_n = variance(num(N), psi)

# Manual calculation
var_n = expect(num(N)**2, psi) - expect(num(N), psi)**2
```

### Time-Dependent Expectation Values

```python
# During time evolution
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])
n_t = result.expect[0]  # Array of ⟨n⟩ at each time
```

## Entropy Measures

### Von Neumann Entropy

```python
from qutip import entropy_vn

# Density matrix entropy
rho = thermal_dm(N, 2)
S = entropy_vn(rho)  # Returns S = -Tr(ρ log₂ ρ)
```

### Linear Entropy

```python
from qutip import entropy_linear

# Linear entropy S_L = 1 - Tr(ρ²)
S_L = entropy_linear(rho)
```

### Entanglement Entropy

```python
# For bipartite systems
psi = bell_state('00')
rho = psi.proj()

# Trace out subsystem B to get reduced density matrix
rho_A = ptrace(rho, 0)

# Entanglement entropy
S_ent = entropy_vn(rho_A)
```

### Mutual Information

```python
from qutip import entropy_mutual

# For bipartite state ρ_AB
I = entropy_mutual(rho, [0, 1])  # I(A:B) = S(A) + S(B) - S(AB)
```

### Conditional Entropy

```python
from qutip import entropy_conditional

# S(A|B) = S(AB) - S(B)
S_cond = entropy_conditional(rho, 0)  # Entropy of subsystem 0 given subsystem 1
```

## Fidelity and Distance Measures

### State Fidelity

```python
from qutip import fidelity

# Fidelity between two states
psi1 = coherent(N, 2)
psi2 = coherent(N, 2.1)

F = fidelity(psi1, psi2)  # Returns value in [0, 1]
```

### Process Fidelity

```python
from qutip import process_fidelity

# Fidelity between two processes (superoperators)
U_ideal = (-1j * H * t).expm()
U_actual = mesolve(H, basis(N, 0), [0, t], c_ops).states[-1]

F_proc = process_fidelity(U_ideal, U_actual)
```

### Trace Distance

```python
from qutip import tracedist

# Trace distance D = (1/2) Tr|ρ₁ - ρ₂|
rho1 = coherent_dm(N, 2)
rho2 = thermal_dm(N, 2)

D = tracedist(rho1, rho2)  # Returns value in [0, 1]
```

### Hilbert-Schmidt Distance

```python
from qutip import hilbert_dist

# Hilbert-Schmidt distance
D_HS = hilbert_dist(rho1, rho2)
```

### Bures Distance

```python
from qutip import bures_dist

# Bures distance
D_B = bures_dist(rho1, rho2)
```

### Bures Angle

```python
from qutip import bures_angle

# Bures angle
angle = bures_angle(rho1, rho2)
```

## Entanglement Measures

### Concurrence

```python
from qutip import concurrence

# For two-qubit states
psi = bell_state('00')
rho = psi.proj()

C = concurrence(rho)  # C = 1 for maximally entangled states
```

### Negativity

```python
from qutip import negativity

# Negativity (partial transpose criterion)
N_ent = negativity(rho, 0)  # Partial transpose w.r.t. subsystem 0

# Logarithmic negativity
from qutip import logarithmic_negativity
E_N = logarithmic_negativity(rho, 0)
```

### Entangling Power

```python
from qutip import entangling_power

# For unitary gates
U = cnot()
E_pow = entangling_power(U)
```

## Purity Measures

### Purity

```python
# Purity P = Tr(ρ²)
P = (rho * rho).tr()

# For pure states: P = 1
# For maximally mixed: P = 1/d
```

### Checking State Properties

```python
# Is state pure?
is_pure = abs((rho * rho).tr() - 1.0) < 1e-10

# Is operator Hermitian?
H.isherm

# Is operator unitary?
U.check_isunitary()
```

## Measurement

### Projective Measurement

```python
from qutip import measurement

# Measure in computational basis
psi = (basis(2, 0) + basis(2, 1)).unit()

# Perform measurement
result, state_after = measurement.measure(psi, None)  # Random outcome

# Specific measurement operator
M = basis(2, 0).proj()
prob = measurement.measure_povm(psi, [M, qeye(2) - M])
```

### Measurement Statistics

```python
from qutip import measurement_statistics

# Get all possible outcomes and probabilities
outcomes, probabilities = measurement_statistics(psi, [M0, M1])
```

### Observable Measurement

```python
from qutip import measure_observable

# Measure observable and get result + collapsed state
result, state_collapsed = measure_observable(psi, sigmaz())
```

### POVM Measurements

```python
from qutip import measure_povm

# Positive Operator-Valued Measure
E_0 = Qobj([[0.8, 0], [0, 0.2]])
E_1 = Qobj([[0.2, 0], [0, 0.8]])

result, state_after = measure_povm(psi, [E_0, E_1])
```

## Coherence Measures

### l1-norm Coherence

```python
from qutip import coherence_l1norm

# l1-norm of off-diagonal elements
C_l1 = coherence_l1norm(rho)
```

## Correlation Functions

### Two-Time Correlation

```python
from qutip import correlation_2op_1t, correlation_2op_2t

# Single-time correlation ⟨A(t+τ)B(t)⟩
A = destroy(N)
B = create(N)
taulist = np.linspace(0, 10, 200)

corr = correlation_2op_1t(H, rho0, taulist, c_ops, A, B)

# Two-time correlation ⟨A(t)B(τ)⟩
tlist = np.linspace(0, 10, 100)
corr_2t = correlation_2op_2t(H, rho0, tlist, taulist, c_ops, A, B)
```

### Three-Operator Correlation

```python
from qutip import correlation_3op_1t

# ⟨A(t)B(t+τ)C(t)⟩
C_op = num(N)
corr_3 = correlation_3op_1t(H, rho0, taulist, c_ops, A, B, C_op)
```

### Four-Operator Correlation

```python
from qutip import correlation_4op_1t

# ⟨A(0)B(τ)C(τ)D(0)⟩
D_op = create(N)
corr_4 = correlation_4op_1t(H, rho0, taulist, c_ops, A, B, C_op, D_op)
```

## Spectrum Analysis

### FFT Spectrum

```python
from qutip import spectrum_correlation_fft

# Power spectrum from correlation function
w, S = spectrum_correlation_fft(taulist, corr)
```

### Direct Spectrum Calculation

```python
from qutip import spectrum

# Emission/absorption spectrum
wlist = np.linspace(0, 2, 200)
spec = spectrum(H, wlist, c_ops, A, B)
```

### Pseudo-Modes

```python
from qutip import spectrum_pi

# Spectrum with pseudo-mode decomposition
spec_pi = spectrum_pi(H, rho0, wlist, c_ops, A, B)
```

## Steady State Analysis

### Finding Steady State

```python
from qutip import steadystate

# Find steady state ∂ρ/∂t = 0
rho_ss = steadystate(H, c_ops)

# Different methods
rho_ss = steadystate(H, c_ops, method='direct')  # Default
rho_ss = steadystate(H, c_ops, method='eigen')   # Eigenvalue
rho_ss = steadystate(H, c_ops, method='svd')     # SVD
rho_ss = steadystate(H, c_ops, method='power')   # Power method
```

### Steady State Properties

```python
# Verify it's steady
L = liouvillian(H, c_ops)
assert (L * operator_to_vector(rho_ss)).norm() < 1e-10

# Compute steady-state expectation values
n_ss = expect(num(N), rho_ss)
```

## Quantum Fisher Information

```python
from qutip import qfisher

# Quantum Fisher information
F_Q = qfisher(rho, num(N))  # w.r.t. generator num(N)
```

## Matrix Analysis

### Eigenanalysis

```python
# Eigenvalues and eigenvectors
evals, ekets = H.eigenstates()

# Just eigenvalues
evals = H.eigenenergies()

# Ground state
E0, psi0 = H.groundstate()
```

### Matrix Functions

```python
# Matrix exponential
U = (H * t).expm()

# Matrix logarithm
log_rho = rho.logm()

# Matrix square root
sqrt_rho = rho.sqrtm()

# Matrix power
rho_squared = rho ** 2
```

### Singular Value Decomposition

```python
# SVD of operator
U, S, Vh = H.svd()
```

### Permutations

```python
from qutip import permute

# Permute subsystems
rho_permuted = permute(rho, [1, 0])  # Swap subsystems
```

## Partial Operations

### Partial Trace

```python
# Reduce to subsystem
rho_A = ptrace(rho_AB, 0)  # Keep subsystem 0
rho_B = ptrace(rho_AB, 1)  # Keep subsystem 1

# Keep multiple subsystems
rho_AC = ptrace(rho_ABC, [0, 2])  # Keep 0 and 2, trace out 1
```

### Partial Transpose

```python
from qutip import partial_transpose

# Partial transpose (for entanglement detection)
rho_pt = partial_transpose(rho, [0, 1])  # Transpose subsystem 0

# Check if entangled (PPT criterion)
evals = rho_pt.eigenenergies()
is_entangled = any(evals < -1e-10)
```

## Quantum State Tomography

### State Reconstruction

```python
from qutip_qip.tomography import state_tomography

# Prepare measurement results
# measurements = ... (experimental data)

# Reconstruct density matrix
rho_reconstructed = state_tomography(measurements, basis='Pauli')
```

### Process Tomography

```python
from qutip_qip.tomography import qpt

# Characterize quantum process
chi = qpt(U_gate, method='lstsq')  # Chi matrix representation
```

## Random Quantum Objects

Useful for testing and Monte Carlo simulations.

```python
# Random state vector
psi_rand = rand_ket(N)

# Random density matrix
rho_rand = rand_dm(N)

# Random Hermitian operator
H_rand = rand_herm(N)

# Random unitary
U_rand = rand_unitary(N)

# With specific properties
rho_rank2 = rand_dm(N, rank=2)  # Rank-2 density matrix
H_sparse = rand_herm(N, density=0.1)  # 10% non-zero elements
```

## Useful Checks

```python
# Check if operator is Hermitian
H.isherm

# Check if state is normalized
abs(psi.norm() - 1.0) < 1e-10

# Check if density matrix is physical
rho.tr() ≈ 1 and all(rho.eigenenergies() >= 0)

# Check if operators commute
commutator(A, B).norm() < 1e-10
```

---

## Reference: Core_Concepts

# QuTiP Core Concepts

## Quantum Objects (Qobj)

All quantum objects in QuTiP are represented by the `Qobj` class:

```python
from qutip import *

# Create a quantum object
psi = basis(2, 0)  # Ground state of 2-level system
rho = fock_dm(5, 2)  # Density matrix for n=2 Fock state
H = sigmaz()  # Pauli Z operator
```

Key attributes:
- `.dims` - Dimension structure
- `.shape` - Matrix dimensions
- `.type` - Type (ket, bra, oper, super)
- `.isherm` - Check if Hermitian
- `.dag()` - Hermitian conjugate
- `.tr()` - Trace
- `.norm()` - Norm

## States

### Basis States

```python
# Fock (number) states
n = 2  # Excitation level
N = 10  # Hilbert space dimension
psi = basis(N, n)  # or fock(N, n)

# Coherent states
alpha = 1 + 1j
coherent(N, alpha)

# Thermal states (density matrices)
n_avg = 2.0  # Average photon number
thermal_dm(N, n_avg)
```

### Spin States

```python
# Spin-1/2 states
spin_state(1/2, 1/2)  # Spin up
spin_coherent(1/2, theta, phi)  # Coherent spin state

# Multi-qubit computational basis
basis([2,2,2], [0,1,0])  # |010⟩ for 3 qubits
```

### Composite States

```python
# Tensor products
psi1 = basis(2, 0)
psi2 = basis(2, 1)
tensor(psi1, psi2)  # |01⟩

# Bell states
bell_state('00')  # (|00⟩ + |11⟩)/√2
maximally_mixed_dm(2)  # Maximally mixed state
```

## Operators

### Creation/Annihilation

```python
N = 10
a = destroy(N)  # Annihilation operator
a_dag = create(N)  # Creation operator
num = num(N)  # Number operator (a†a)
```

### Pauli Matrices

```python
sigmax()  # σx
sigmay()  # σy
sigmaz()  # σz
sigmap()  # σ+ = (σx + iσy)/2
sigmam()  # σ- = (σx - iσy)/2
```

### Angular Momentum

```python
# Spin operators for arbitrary j
j = 1  # Spin-1
jmat(j, 'x')  # Jx
jmat(j, 'y')  # Jy
jmat(j, 'z')  # Jz
jmat(j, '+')  # J+
jmat(j, '-')  # J-
```

### Displacement and Squeezing

```python
alpha = 1 + 1j
displace(N, alpha)  # Displacement operator D(α)

z = 0.5  # Squeezing parameter
squeeze(N, z)  # Squeezing operator S(z)
```

## Tensor Products and Composition

### Building Composite Systems

```python
# Tensor product of operators
H1 = sigmaz()
H2 = sigmax()
H_total = tensor(H1, H2)

# Identity operators
qeye([2, 2])  # Identity for two qubits

# Partial application
# σz ⊗ I for 3-qubit system
tensor(sigmaz(), qeye(2), qeye(2))
```

### Partial Trace

```python
# Composite system state
rho = bell_state('00').proj()  # |Φ+⟩⟨Φ+|

# Trace out subsystem
rho_A = ptrace(rho, 0)  # Trace out subsystem 0
rho_B = ptrace(rho, 1)  # Trace out subsystem 1
```

## Expectation Values and Measurements

```python
# Expectation values
psi = coherent(N, alpha)
expect(num, psi)  # ⟨n⟩

# For multiple operators
ops = [a, a_dag, num]
expect(ops, psi)  # Returns list

# Variance
variance(num, psi)  # Var(n) = ⟨n²⟩ - ⟨n⟩²
```

## Superoperators and Liouvillians

### Lindblad Form

```python
# System Hamiltonian
H = num

# Collapse operators (dissipation)
c_ops = [np.sqrt(0.1) * a]  # Decay rate 0.1

# Liouvillian superoperator
L = liouvillian(H, c_ops)

# Alternative: explicit form
L = -1j * (spre(H) - spost(H)) + lindblad_dissipator(a, a)
```

### Superoperator Representations

```python
# Kraus representation
kraus_to_super(kraus_ops)

# Choi matrix
choi_to_super(choi_matrix)

# Chi (process) matrix
chi_to_super(chi_matrix)

# Conversions
super_to_choi(L)
choi_to_kraus(choi_matrix)
```

## Quantum Gates (requires qutip-qip)

```python
from qutip_qip.operations import *

# Single-qubit gates
hadamard_transform()  # Hadamard
rx(np.pi/2)  # X-rotation
ry(np.pi/2)  # Y-rotation
rz(np.pi/2)  # Z-rotation
phasegate(np.pi/4)  # Phase gate
snot()  # Hadamard (alternative)

# Two-qubit gates
cnot()  # CNOT
swap()  # SWAP
iswap()  # iSWAP
sqrtswap()  # √SWAP
berkeley()  # Berkeley gate
swapalpha(alpha)  # SWAP^α

# Three-qubit gates
fredkin()  # Controlled-SWAP
toffoli()  # Controlled-CNOT

# Expanding to multi-qubit systems
N = 3  # Total qubits
target = 1
controls = [0, 2]
gate_expand_2toN(cnot(), N, [controls[0], target])
```

## Common Hamiltonians

### Jaynes-Cummings Model

```python
# Cavity mode
N = 10
a = tensor(destroy(N), qeye(2))

# Atom
sm = tensor(qeye(N), sigmam())

# Hamiltonian
wc = 1.0  # Cavity frequency
wa = 1.0  # Atom frequency
g = 0.05  # Coupling strength
H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())
```

### Driven Systems

```python
# Time-dependent Hamiltonian
H0 = sigmaz()
H1 = sigmax()

def drive(t, args):
    return np.sin(args['w'] * t)

H = [H0, [H1, drive]]
args = {'w': 1.0}
```

### Spin Chains

```python
# Heisenberg chain
N_spins = 5
J = 1.0  # Exchange coupling

# Build Hamiltonian
H = 0
for i in range(N_spins - 1):
    # σᵢˣσᵢ₊₁ˣ + σᵢʸσᵢ₊₁ʸ + σᵢᶻσᵢ₊₁ᶻ
    H += J * (
        tensor_at([sigmax()], i, N_spins) * tensor_at([sigmax()], i+1, N_spins) +
        tensor_at([sigmay()], i, N_spins) * tensor_at([sigmay()], i+1, N_spins) +
        tensor_at([sigmaz()], i, N_spins) * tensor_at([sigmaz()], i+1, N_spins)
    )
```

## Useful Utility Functions

```python
# Generate random quantum objects
rand_ket(N)  # Random ket
rand_dm(N)  # Random density matrix
rand_herm(N)  # Random Hermitian operator
rand_unitary(N)  # Random unitary

# Commutator and anti-commutator
commutator(A, B)  # [A, B]
anti_commutator(A, B)  # {A, B}

# Matrix exponential
(-1j * H * t).expm()  # e^(-iHt)

# Eigenvalues and eigenvectors
H.eigenstates()  # Returns (eigenvalues, eigenvectors)
H.eigenenergies()  # Returns only eigenvalues
H.groundstate()  # Ground state energy and state
```

---

## Reference: Time_Evolution

# QuTiP Time Evolution and Dynamics Solvers

## Overview

QuTiP provides multiple solvers for quantum dynamics:
- `sesolve` - Schrödinger equation (unitary evolution)
- `mesolve` - Master equation (open systems with dissipation)
- `mcsolve` - Monte Carlo (quantum trajectories)
- `brmesolve` - Bloch-Redfield master equation
- `fmmesolve` - Floquet-Markov master equation
- `ssesolve/smesolve` - Stochastic Schrödinger/master equations

## Schrödinger Equation Solver (sesolve)

For closed quantum systems evolving unitarily.

### Basic Usage

```python
from qutip import *
import numpy as np

# System setup
N = 10
psi0 = basis(N, 0)  # Initial state
H = num(N)  # Hamiltonian

# Time points
tlist = np.linspace(0, 10, 100)

# Solve
result = sesolve(H, psi0, tlist)

# Access results
states = result.states  # List of states at each time
final_state = result.states[-1]
```

### With Expectation Values

```python
# Operators to compute expectation values
e_ops = [num(N), destroy(N), create(N)]

result = sesolve(H, psi0, tlist, e_ops=e_ops)

# Access expectation values
n_t = result.expect[0]  # ⟨n⟩(t)
a_t = result.expect[1]  # ⟨a⟩(t)
```

### Time-Dependent Hamiltonians

```python
# Method 1: String-based (faster, requires Cython)
H = [num(N), [destroy(N) + create(N), 'cos(w*t)']]
args = {'w': 1.0}
result = sesolve(H, psi0, tlist, args=args)

# Method 2: Function-based
def drive(t, args):
    return np.exp(-t/args['tau']) * np.sin(args['w'] * t)

H = [num(N), [destroy(N) + create(N), drive]]
args = {'w': 1.0, 'tau': 5.0}
result = sesolve(H, psi0, tlist, args=args)

# Method 3: QobjEvo (most flexible)
from qutip import QobjEvo
H_td = QobjEvo([num(N), [destroy(N) + create(N), drive]], args=args)
result = sesolve(H_td, psi0, tlist)
```

## Master Equation Solver (mesolve)

For open quantum systems with dissipation and decoherence.

### Basic Usage

```python
# System Hamiltonian
H = num(N)

# Collapse operators (Lindblad operators)
kappa = 0.1  # Decay rate
c_ops = [np.sqrt(kappa) * destroy(N)]

# Initial state
psi0 = coherent(N, 2.0)

# Solve
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Result is a density matrix evolution
rho_t = result.states  # List of density matrices
n_t = result.expect[0]  # ⟨n⟩(t)
```

### Multiple Dissipation Channels

```python
# Photon loss
kappa = 0.1
# Dephasing
gamma = 0.05
# Thermal excitation
nth = 0.5  # Thermal photon number

c_ops = [
    np.sqrt(kappa * (1 + nth)) * destroy(N),  # Thermal decay
    np.sqrt(kappa * nth) * create(N),  # Thermal excitation
    np.sqrt(gamma) * num(N)  # Pure dephasing
]

result = mesolve(H, psi0, tlist, c_ops)
```

### Time-Dependent Dissipation

```python
# Time-dependent decay rate
def kappa_t(t, args):
    return args['k0'] * (1 + np.sin(args['w'] * t))

c_ops = [[np.sqrt(1.0) * destroy(N), kappa_t]]
args = {'k0': 0.1, 'w': 1.0}

result = mesolve(H, psi0, tlist, c_ops, args=args)
```

## Monte Carlo Solver (mcsolve)

Simulates quantum trajectories for open systems.

### Basic Usage

```python
# Same setup as mesolve
H = num(N)
c_ops = [np.sqrt(0.1) * destroy(N)]
psi0 = coherent(N, 2.0)

# Number of trajectories
ntraj = 500

result = mcsolve(H, psi0, tlist, c_ops, e_ops=[num(N)], ntraj=ntraj)

# Results averaged over trajectories
n_avg = result.expect[0]
n_std = result.std_expect[0]  # Standard deviation

# Individual trajectories (if options.store_states=True)
options = Options(store_states=True)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=ntraj, options=options)
trajectories = result.states  # List of trajectory lists
```

### Photon Counting

```python
# Track quantum jumps
result = mcsolve(H, psi0, tlist, c_ops, ntraj=ntraj, options=options)

# Access jump times and which operator caused the jump
for traj in result.col_times:
    print(f"Jump times: {traj}")

for traj in result.col_which:
    print(f"Jump operator indices: {traj}")
```

## Bloch-Redfield Solver (brmesolve)

For weak system-bath coupling in the secular approximation.

```python
# System Hamiltonian
H = sigmaz()

# Coupling operators and spectral density
a_ops = [[sigmax(), lambda w: 0.1 * w if w > 0 else 0]]  # Ohmic bath

psi0 = basis(2, 0)
result = brmesolve(H, psi0, tlist, a_ops, e_ops=[sigmaz(), sigmax()])
```

## Floquet Solver (fmmesolve)

For time-periodic Hamiltonians.

```python
# Time-periodic Hamiltonian
w_d = 1.0  # Drive frequency
H0 = sigmaz()
H1 = sigmax()
H = [H0, [H1, 'cos(w*t)']]
args = {'w': w_d}

# Floquet modes and quasi-energies
T = 2 * np.pi / w_d  # Period
f_modes, f_energies = floquet_modes(H, T, args)

# Initial state in Floquet basis
psi0 = basis(2, 0)

# Dissipation in Floquet basis
c_ops = [np.sqrt(0.1) * sigmam()]

result = fmmesolve(H, psi0, tlist, c_ops, e_ops=[num(2)], T=T, args=args)
```

## Stochastic Solvers

### Stochastic Schrödinger Equation (ssesolve)

```python
# Diffusion operator
sc_ops = [np.sqrt(0.1) * destroy(N)]

# Heterodyne detection
result = ssesolve(H, psi0, tlist, sc_ops=sc_ops, e_ops=[num(N)],
                   ntraj=500, noise=1)  # noise=1 for heterodyne
```

### Stochastic Master Equation (smesolve)

```python
result = smesolve(H, psi0, tlist, c_ops=[], sc_ops=sc_ops,
                   e_ops=[num(N)], ntraj=500)
```

## Propagators

### Time-Evolution Operator

```python
# Evolution operator U(t) such that ψ(t) = U(t)ψ(0)
U = (-1j * H * t).expm()
psi_t = U * psi0

# For master equation (superoperator propagator)
L = liouvillian(H, c_ops)
U_super = (L * t).expm()
rho_t = vector_to_operator(U_super * operator_to_vector(rho0))
```

### Propagator Function

```python
# Generate propagators for multiple times
U_list = propagator(H, tlist, c_ops)

# Apply to states
psi_t = [U_list[i] * psi0 for i in range(len(tlist))]
```

## Steady State Solutions

### Direct Steady State

```python
# Find steady state of Liouvillian
rho_ss = steadystate(H, c_ops)

# Check it's steady
L = liouvillian(H, c_ops)
assert (L * operator_to_vector(rho_ss)).norm() < 1e-10
```

### Pseudo-Inverse Method

```python
# For degenerate steady states
rho_ss = steadystate(H, c_ops, method='direct')
# or 'eigen', 'svd', 'power'
```

## Correlation Functions

### Two-Time Correlation

```python
# ⟨A(t+τ)B(t)⟩
A = destroy(N)
B = create(N)

# Emission spectrum
taulist = np.linspace(0, 10, 200)
corr = correlation_2op_1t(H, None, taulist, c_ops, A, B)

# Power spectrum
w, S = spectrum_correlation_fft(taulist, corr)
```

### Multi-Time Correlation

```python
# ⟨A(t3)B(t2)C(t1)⟩
corr = correlation_3op_1t(H, None, taulist, c_ops, A, B, C)
```

## Solver Options

```python
from qutip import Options

options = Options()
options.nsteps = 10000  # Max internal steps
options.atol = 1e-8  # Absolute tolerance
options.rtol = 1e-6  # Relative tolerance
options.method = 'adams'  # or 'bdf' for stiff problems
options.store_states = True  # Store all states
options.store_final_state = True  # Store only final state

result = mesolve(H, psi0, tlist, c_ops, options=options)
```

### Progress Bar

```python
options.progress_bar = True
result = mesolve(H, psi0, tlist, c_ops, options=options)
```

## Saving and Loading Results

```python
# Save results
result.save("my_simulation.dat")

# Load results
from qutip import Result
loaded_result = Result.load("my_simulation.dat")
```

## Tips for Efficient Simulations

1. **Sparse matrices**: QuTiP automatically uses sparse matrices
2. **Small Hilbert spaces**: Truncate when possible
3. **Time-dependent terms**: String format is fastest (requires compilation)
4. **Parallel trajectories**: mcsolve automatically parallelizes
5. **Convergence**: Check by varying `ntraj`, `nsteps`, tolerances
6. **Solver selection**:
   - Pure states: Use `sesolve` (faster)
   - Mixed states/dissipation: Use `mesolve`
   - Noise/measurements: Use `mcsolve`
   - Weak coupling: Use `brmesolve`
   - Periodic driving: Use Floquet methods

---

## Reference: Visualization

# QuTiP Visualization

## Bloch Sphere

Visualize qubit states on the Bloch sphere.

### Basic Usage

```python
from qutip import *
import matplotlib.pyplot as plt

# Create Bloch sphere
b = Bloch()

# Add states
psi = (basis(2, 0) + basis(2, 1)).unit()
b.add_states(psi)

# Add vectors
b.add_vectors([1, 0, 0])  # X-axis

# Display
b.show()
```

### Multiple States

```python
# Add multiple states
states = [(basis(2, 0) + basis(2, 1)).unit(),
          (basis(2, 0) + 1j*basis(2, 1)).unit()]
b.add_states(states)

# Add points
b.add_points([[0, 1, 0], [0, -1, 0]])

# Customize colors
b.point_color = ['r', 'g']
b.point_marker = ['o', 's']
b.point_size = [20, 20]

b.show()
```

### Animation

```python
# Animate state evolution
states = result.states  # From sesolve/mesolve

b = Bloch()
b.vector_color = ['r']
b.view = [-40, 30]  # Viewing angle

# Create animation
from matplotlib.animation import FuncAnimation

def animate(i):
    b.clear()
    b.add_states(states[i])
    b.make_sphere()
    return b.axes

anim = FuncAnimation(b.fig, animate, frames=len(states),
                      interval=50, blit=False, repeat=True)
plt.show()
```

### Customization

```python
b = Bloch()

# Sphere appearance
b.sphere_color = '#FFDDDD'
b.sphere_alpha = 0.1
b.frame_alpha = 0.1

# Axes
b.xlabel = ['$|+\\\\rangle$', '$|-\\\\rangle$']
b.ylabel = ['$|+i\\\\rangle$', '$|-i\\\\rangle$']
b.zlabel = ['$|0\\\\rangle$', '$|1\\\\rangle$']

# Font sizes
b.font_size = 20
b.font_color = 'black'

# View angle
b.view = [-60, 30]

# Save figure
b.save('bloch.png')
```

## Wigner Function

Phase-space quasi-probability distribution.

### Basic Calculation

```python
# Create state
psi = coherent(N, alpha)

# Calculate Wigner function
xvec = np.linspace(-5, 5, 200)
W = wigner(psi, xvec, xvec)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
cont = ax.contourf(xvec, xvec, W, 100, cmap='RdBu')
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
plt.colorbar(cont, ax=ax)
plt.show()
```

### Special Colormap

```python
# Wigner colormap emphasizes negative values
from qutip import wigner_cmap

W = wigner(psi, xvec, xvec)

fig, ax = plt.subplots()
cont = ax.contourf(xvec, xvec, W, 100, cmap=wigner_cmap(W))
ax.set_title('Wigner Function')
plt.colorbar(cont)
plt.show()
```

### 3D Surface Plot

```python
from mpl_toolkits.mplot3d import Axes3D

X, Y = np.meshgrid(xvec, xvec)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, W, cmap='RdBu', alpha=0.8)
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
ax.set_zlabel('W(α)')
plt.show()
```

### Comparing States

```python
# Compare different states
states = [coherent(N, 2), fock(N, 2), thermal_dm(N, 2)]
titles = ['Coherent', 'Fock', 'Thermal']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, (state, title) in enumerate(zip(states, titles)):
    W = wigner(state, xvec, xvec)
    cont = axes[i].contourf(xvec, xvec, W, 100, cmap='RdBu')
    axes[i].set_title(title)
    axes[i].set_xlabel('Re(α)')
    if i == 0:
        axes[i].set_ylabel('Im(α)')

plt.tight_layout()
plt.show()
```

## Q-Function (Husimi)

Smoothed phase-space distribution (always positive).

### Basic Usage

```python
from qutip import qfunc

Q = qfunc(psi, xvec, xvec)

fig, ax = plt.subplots()
cont = ax.contourf(xvec, xvec, Q, 100, cmap='viridis')
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
ax.set_title('Q-Function')
plt.colorbar(cont)
plt.show()
```

### Efficient Batch Calculation

```python
from qutip import QFunc

# For calculating Q-function at many points
qf = QFunc(rho)
Q = qf.eval(xvec, xvec)
```

## Fock State Probability Distribution

Visualize photon number distribution.

### Basic Histogram

```python
from qutip import plot_fock_distribution

# Single state
psi = coherent(N, 2)
fig, ax = plot_fock_distribution(psi)
ax.set_title('Coherent State')
plt.show()
```

### Comparing Distributions

```python
states = {
    'Coherent': coherent(20, 2),
    'Thermal': thermal_dm(20, 2),
    'Fock': fock(20, 2)
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (title, state) in zip(axes, states.items()):
    plot_fock_distribution(state, fig=fig, ax=ax)
    ax.set_title(title)
    ax.set_ylim([0, 0.3])

plt.tight_layout()
plt.show()
```

### Time Evolution

```python
# Show evolution of photon distribution
result = mesolve(H, psi0, tlist, c_ops)

# Plot at different times
times_to_plot = [0, 5, 10, 15]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, t_idx in zip(axes, times_to_plot):
    plot_fock_distribution(result.states[t_idx], fig=fig, ax=ax)
    ax.set_title(f't = {tlist[t_idx]:.1f}')
    ax.set_ylim([0, 1])

plt.tight_layout()
plt.show()
```

## Matrix Visualization

### Hinton Diagram

Visualize matrix structure with weighted squares.

```python
from qutip import hinton

# Density matrix
rho = bell_state('00').proj()

hinton(rho)
plt.title('Bell State Density Matrix')
plt.show()
```

### Matrix Histogram

3D bar plot of matrix elements.

```python
from qutip import matrix_histogram

# Show real and imaginary parts
H = sigmaz()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

matrix_histogram(H.full(), xlabels=['0', '1'], ylabels=['0', '1'],
                 fig=fig, ax=axes[0])
axes[0].set_title('Real Part')

matrix_histogram(H.full(), bar_type='imag', xlabels=['0', '1'],
                 ylabels=['0', '1'], fig=fig, ax=axes[1])
axes[1].set_title('Imaginary Part')

plt.tight_layout()
plt.show()
```

### Complex Phase Diagram

```python
# Visualize complex matrix elements
rho = coherent_dm(10, 2)

# Plot complex elements
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Absolute value
matrix_histogram(rho.full(), bar_type='abs', fig=fig, ax=axes[0])
axes[0].set_title('Absolute Value')

# Phase
matrix_histogram(rho.full(), bar_type='phase', fig=fig, ax=axes[1])
axes[1].set_title('Phase')

plt.tight_layout()
plt.show()
```

## Energy Level Diagrams

```python
# Visualize energy eigenvalues
H = num(N) + 0.1 * (create(N) + destroy(N))**2

# Get eigenvalues and eigenvectors
evals, ekets = H.eigenstates()

# Plot energy levels
fig, ax = plt.subplots(figsize=(8, 6))

for i, E in enumerate(evals[:10]):
    ax.hlines(E, 0, 1, linewidth=2)
    ax.text(1.1, E, f'|{i}⟩', va='center')

ax.set_ylabel('Energy')
ax.set_xlim([-0.2, 1.5])
ax.set_xticks([])
ax.set_title('Energy Spectrum')
plt.show()
```

## Quantum Process Tomography

Visualize quantum channel/gate action.

```python
from qutip.qip.operations import cnot
from qutip_qip.tomography import qpt, qpt_plot_combined

# Define process (e.g., CNOT gate)
U = cnot()

# Perform QPT
chi = qpt(U, method='choicm')

# Visualize
fig = qpt_plot_combined(chi)
plt.show()
```

## Expectation Values Over Time

```python
# Standard plotting of expectation values
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

fig, ax = plt.subplots()
ax.plot(tlist, result.expect[0])
ax.set_xlabel('Time')
ax.set_ylabel('⟨n⟩')
ax.set_title('Photon Number Evolution')
ax.grid(True)
plt.show()
```

### Multiple Observables

```python
# Plot multiple expectation values
e_ops = [a.dag() * a, a + a.dag(), 1j * (a - a.dag())]
labels = ['⟨n⟩', '⟨X⟩', '⟨P⟩']

result = mesolve(H, psi0, tlist, c_ops, e_ops=e_ops)

fig, axes = plt.subplots(3, 1, figsize=(8, 9))

for i, (ax, label) in enumerate(zip(axes, labels)):
    ax.plot(tlist, result.expect[i])
    ax.set_ylabel(label)
    ax.grid(True)

axes[-1].set_xlabel('Time')
plt.tight_layout()
plt.show()
```

## Correlation Functions and Spectra

```python
# Two-time correlation function
taulist = np.linspace(0, 10, 200)
corr = correlation_2op_1t(H, rho0, taulist, c_ops, a.dag(), a)

# Plot correlation
fig, ax = plt.subplots()
ax.plot(taulist, np.real(corr))
ax.set_xlabel('τ')
ax.set_ylabel('⟨a†(τ)a(0)⟩')
ax.set_title('Correlation Function')
plt.show()

# Power spectrum
from qutip import spectrum_correlation_fft

w, S = spectrum_correlation_fft(taulist, corr)

fig, ax = plt.subplots()
ax.plot(w, S)
ax.set_xlabel('Frequency')
ax.set_ylabel('S(ω)')
ax.set_title('Power Spectrum')
plt.show()
```

## Saving Figures

```python
# High-resolution saves
fig.savefig('my_plot.png', dpi=300, bbox_inches='tight')
fig.savefig('my_plot.pdf', bbox_inches='tight')
fig.savefig('my_plot.svg', bbox_inches='tight')
```
