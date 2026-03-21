---
title: "Fluidsim"
description: "Framework for computational fluid dynamics simulations using Python. Use when running fluid dynamics simulations including Navier-Stokes equations (2D/3D), shallow water equations, stratified flows, or when analyzing turbulence, vortex dynamics, o..."
category: "development"
source: "community"
author: "Community"
tags: ["fluidsim"]
date: 2026-03-20
---

# FluidSim

## Overview

FluidSim is an object-oriented Python framework for high-performance computational fluid dynamics (CFD) simulations. It provides solvers for periodic-domain equations using pseudospectral methods with FFT, delivering performance comparable to Fortran/C++ while maintaining Python's ease of use.

**Key strengths**:
- Multiple solvers: 2D/3D Navier-Stokes, shallow water, stratified flows
- High performance: Pythran/Transonic compilation, MPI parallelization
- Complete workflow: Parameter configuration, simulation execution, output analysis
- Interactive analysis: Python-based post-processing and visualization

## Core Capabilities

### 1. Installation and Setup

Install fluidsim using uv with appropriate feature flags:

```bash
# Basic installation
uv uv pip install fluidsim

# With FFT support (required for most solvers)
uv uv pip install "fluidsim[fft]"

# With MPI for parallel computing
uv uv pip install "fluidsim[fft,mpi]"
```

Set environment variables for output directories (optional):

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

No API keys or authentication required.

See `references/installation.md` for complete installation instructions and environment configuration.

### 2. Running Simulations

Standard workflow consists of five steps:

**Step 1**: Import solver
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**Step 2**: Create and configure parameters
```python
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * 3.14159
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"
```

**Step 3**: Instantiate simulation
```python
sim = Simul(params)
```

**Step 4**: Execute
```python
sim.time_stepping.start()
```

**Step 5**: Analyze results
```python
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```

See `references/simulation_workflow.md` for complete examples, restarting simulations, and cluster deployment.

### 3. Available Solvers

Choose solver based on physical problem:

**2D Navier-Stokes** (`ns2d`): 2D turbulence, vortex dynamics
```python
from fluidsim.solvers.ns2d.solver import Simul
```

**3D Navier-Stokes** (`ns3d`): 3D turbulence, realistic flows
```python
from fluidsim.solvers.ns3d.solver import Simul
```

**Stratified flows** (`ns2d.strat`, `ns3d.strat`): Oceanic/atmospheric flows
```python
from fluidsim.solvers.ns2d.strat.solver import Simul
params.N = 1.0  # Brunt-Väisälä frequency
```

**Shallow water** (`sw1l`): Geophysical flows, rotating systems
```python
from fluidsim.solvers.sw1l.solver import Simul
params.f = 1.0  # Coriolis parameter
```

See `references/solvers.md` for complete solver list and selection guidance.

### 4. Parameter Configuration

Parameters are organized hierarchically and accessed via dot notation:

**Domain and resolution**:
```python
params.oper.nx = 256  # grid points
params.oper.Lx = 2 * pi  # domain size
```

**Physical parameters**:
```python
params.nu_2 = 1e-3  # viscosity
params.nu_4 = 0     # hyperviscosity (optional)
```

**Time stepping**:
```python
params.time_stepping.t_end = 10.0
params.time_stepping.USE_CFL = True  # adaptive time step
params.time_stepping.CFL = 0.5
```

**Initial conditions**:
```python
params.init_fields.type = "noise"  # or "dipole", "vortex", "from_file", "in_script"
```

**Output settings**:
```python
params.output.periods_save.phys_fields = 1.0  # save every 1.0 time units
params.output.periods_save.spectra = 0.5
params.output.periods_save.spatial_means = 0.1
```

The Parameters object raises `AttributeError` for typos, preventing silent configuration errors.

See `references/parameters.md` for comprehensive parameter documentation.

### 5. Output and Analysis

FluidSim produces multiple output types automatically saved during simulation:

**Physical fields**: Velocity, vorticity in HDF5 format
```python
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("vx")
```

**Spatial means**: Time series of volume-averaged quantities
```python
sim.output.spatial_means.plot()
```

**Spectra**: Energy and enstrophy spectra
```python
sim.output.spectra.plot1d()
sim.output.spectra.plot2d()
```

**Load previous simulations**:
```python
from fluidsim import load_sim_for_plot
sim = load_sim_for_plot("simulation_dir")
sim.output.phys_fields.plot()
```

**Advanced visualization**: Open `.h5` files in ParaView or VisIt for 3D visualization.

See `references/output_analysis.md` for detailed analysis workflows, parametric study analysis, and data export.

### 6. Advanced Features

**Custom forcing**: Maintain turbulence or drive specific dynamics
```python
params.forcing.enable = True
params.forcing.type = "tcrandom"  # time-correlated random forcing
params.forcing.forcing_rate = 1.0
```

**Custom initial conditions**: Define fields in script
```python
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vx[:] = sin(X) * cos(Y)
sim.time_stepping.start()
```

**MPI parallelization**: Run on multiple processors
```bash
mpirun -np 8 python simulation_script.py
```

**Parametric studies**: Run multiple simulations with different parameters
```python
for nu in [1e-3, 5e-4, 1e-4]:
    params = Simul.create_default_params()
    params.nu_2 = nu
    params.output.sub_directory = f"nu{nu}"
    sim = Simul(params)
    sim.time_stepping.start()
```

See `references/advanced_features.md` for forcing types, custom solvers, cluster submission, and performance optimization.

## Common Use Cases

### 2D Turbulence Study

```python
from fluidsim.solvers.ns2d.solver import Simul
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 512
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-4
params.time_stepping.t_end = 50.0
params.time_stepping.USE_CFL = True
params.init_fields.type = "noise"
params.output.periods_save.phys_fields = 5.0
params.output.periods_save.spectra = 1.0

sim = Simul(params)
sim.time_stepping.start()

# Analyze energy cascade
sim.output.spectra.plot1d(tmin=30.0, tmax=50.0)
```

### Stratified Flow Simulation

```python
from fluidsim.solvers.ns2d.strat.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.N = 2.0  # stratification strength
params.nu_2 = 5e-4
params.time_stepping.t_end = 20.0

# Initialize with dense layer
params.init_fields.type = "in_script"
sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
b = sim.state.state_phys.get_var("b")
b[:] = exp(-((X - 3.14)**2 + (Y - 3.14)**2) / 0.5)
sim.state.statephys_from_statespect()

sim.time_stepping.start()
sim.output.phys_fields.plot("b")
```

### High-Resolution 3D Simulation with MPI

```python
from fluidsim.solvers.ns3d.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = params.oper.nz = 512
params.nu_2 = 1e-5
params.time_stepping.t_end = 10.0
params.init_fields.type = "noise"

sim = Simul(params)
sim.time_stepping.start()
```

Run with:
```bash
mpirun -np 64 python script.py
```

### Taylor-Green Vortex Validation

```python
from fluidsim.solvers.ns2d.solver import Simul
import numpy as np
from math import pi

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 128
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "in_script"

sim = Simul(params)
X, Y = sim.oper.get_XY_loc()
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)
sim.state.statephys_from_statespect()

sim.time_stepping.start()

# Validate energy decay
df = sim.output.spatial_means.load()
# Compare with analytical solution
```

## Quick Reference

**Import solver**: `from fluidsim.solvers.ns2d.solver import Simul`

**Create parameters**: `params = Simul.create_default_params()`

**Set resolution**: `params.oper.nx = params.oper.ny = 256`

**Set viscosity**: `params.nu_2 = 1e-3`

**Set end time**: `params.time_stepping.t_end = 10.0`

**Run simulation**: `sim = Simul(params); sim.time_stepping.start()`

**Plot results**: `sim.output.phys_fields.plot("vorticity")`

**Load simulation**: `sim = load_sim_for_plot("path/to/sim")`

## Resources

**Documentation**: https://fluidsim.readthedocs.io/

**Reference files**:
- `references/installation.md`: Complete installation instructions
- `references/solvers.md`: Available solvers and selection guide
- `references/simulation_workflow.md`: Detailed workflow examples
- `references/parameters.md`: Comprehensive parameter documentation
- `references/output_analysis.md`: Output types and analysis methods
- `references/advanced_features.md`: Forcing, MPI, parametric studies, custom solvers

---

## Reference: Advanced_Features

# Advanced Features

## Custom Forcing

### Forcing Types

FluidSim supports several forcing mechanisms to maintain turbulence or drive specific dynamics.

#### Time-Correlated Random Forcing

Most common for sustained turbulence:

```python
params.forcing.enable = True
params.forcing.type = "tcrandom"
params.forcing.nkmin_forcing = 2  # minimum forced wavenumber
params.forcing.nkmax_forcing = 5  # maximum forced wavenumber
params.forcing.forcing_rate = 1.0  # energy injection rate
params.forcing.tcrandom_time_correlation = 1.0  # correlation time
```

#### Proportional Forcing

Maintains a specific energy distribution:

```python
params.forcing.type = "proportional"
params.forcing.forcing_rate = 1.0
```

#### Custom Forcing in Script

Define forcing directly in the launch script:

```python
params.forcing.enable = True
params.forcing.type = "in_script"

sim = Simul(params)

# Define custom forcing function
def compute_forcing_fft(sim):
    """Compute forcing in Fourier space"""
    forcing_vx_fft = sim.oper.create_arrayK(value=0.)
    forcing_vy_fft = sim.oper.create_arrayK(value=0.)

    # Add custom forcing logic
    # Example: force specific modes
    forcing_vx_fft[10, 10] = 1.0 + 0.5j

    return forcing_vx_fft, forcing_vy_fft

# Override forcing method
sim.forcing.forcing_maker.compute_forcing_fft = lambda: compute_forcing_fft(sim)

# Run simulation
sim.time_stepping.start()
```

## Custom Initial Conditions

### In-Script Initialization

Full control over initial fields:

```python
from math import pi
import numpy as np

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * pi

params.init_fields.type = "in_script"

sim = Simul(params)

# Get coordinate arrays
X, Y = sim.oper.get_XY_loc()

# Define velocity fields
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")

# Taylor-Green vortex
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)

# Initialize state in Fourier space
sim.state.statephys_from_statespect()

# Run simulation
sim.time_stepping.start()
```

### Layer Initialization (Stratified Flows)

Set up density layers:

```python
from fluidsim.solvers.ns2d.strat.solver import Simul

params = Simul.create_default_params()
params.N = 1.0  # stratification
params.init_fields.type = "in_script"

sim = Simul(params)

# Define dense layer
X, Y = sim.oper.get_XY_loc()
b = sim.state.state_phys.get_var("b")  # buoyancy field

# Gaussian density anomaly
x0, y0 = pi, pi
sigma = 0.5
b[:] = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))

sim.state.statephys_from_statespect()
sim.time_stepping.start()
```

## Parallel Computing with MPI

### Running MPI Simulations

Install with MPI support:
```bash
uv pip install "fluidsim[fft,mpi]"
```

Run with MPI:
```bash
mpirun -np 8 python simulation_script.py
```

FluidSim automatically detects MPI and distributes computation.

### MPI-Specific Parameters

```python
# No special parameters needed
# FluidSim handles domain decomposition automatically

# For very large 3D simulations
params.oper.nx = 512
params.oper.ny = 512
params.oper.nz = 512

# Run with: mpirun -np 64 python script.py
```

### Output with MPI

Output files are written from rank 0 processor. Analysis scripts work identically for serial and MPI runs.

## Parametric Studies

### Running Multiple Simulations

Script to generate and run multiple parameter combinations:

```python
from fluidsim.solvers.ns2d.solver import Simul
import numpy as np

# Parameter ranges
viscosities = [1e-3, 5e-4, 1e-4, 5e-5]
resolutions = [128, 256, 512]

for nu in viscosities:
    for nx in resolutions:
        params = Simul.create_default_params()

        # Configure simulation
        params.oper.nx = params.oper.ny = nx
        params.nu_2 = nu
        params.time_stepping.t_end = 10.0

        # Unique output directory
        params.output.sub_directory = f"nu{nu}_nx{nx}"

        # Run simulation
        sim = Simul(params)
        sim.time_stepping.start()
```

### Cluster Submission

Submit multiple jobs to a cluster:

```python
from fluiddyn.clusters.legi import Calcul8 as Cluster

cluster = Cluster()

for nu in viscosities:
    for nx in resolutions:
        script_content = f"""
from fluidsim.solvers.ns2d.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = {nx}
params.nu_2 = {nu}
params.time_stepping.t_end = 10.0
params.output.sub_directory = "nu{nu}_nx{nx}"

sim = Simul(params)
sim.time_stepping.start()
"""

        with open(f"job_nu{nu}_nx{nx}.py", "w") as f:
            f.write(script_content)

        cluster.submit_script(
            f"job_nu{nu}_nx{nx}.py",
            name_run=f"sim_nu{nu}_nx{nx}",
            nb_nodes=1,
            nb_cores_per_node=24,
            walltime="12:00:00"
        )
```

### Analyzing Parametric Studies

```python
import os
import pandas as pd
from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt

results = []

# Collect data from all simulations
for sim_dir in os.listdir("simulations"):
    sim_path = f"simulations/{sim_dir}"
    if not os.path.isdir(sim_path):
        continue

    try:
        sim = load_sim_for_plot(sim_path)

        # Extract parameters
        nu = sim.params.nu_2
        nx = sim.params.oper.nx

        # Extract results
        df = sim.output.spatial_means.load()
        final_energy = df["E"].iloc[-1]
        mean_energy = df["E"].mean()

        results.append({
            "nu": nu,
            "nx": nx,
            "final_energy": final_energy,
            "mean_energy": mean_energy
        })
    except Exception as e:
        print(f"Error loading {sim_dir}: {e}")

# Analyze results
results_df = pd.DataFrame(results)

# Plot results
plt.figure(figsize=(10, 6))
for nx in results_df["nx"].unique():
    subset = results_df[results_df["nx"] == nx]
    plt.plot(subset["nu"], subset["mean_energy"],
             marker="o", label=f"nx={nx}")

plt.xlabel("Viscosity")
plt.ylabel("Mean Energy")
plt.xscale("log")
plt.legend()
plt.savefig("parametric_study_results.png")
```

## Custom Solvers

### Extending Existing Solvers

Create a new solver by inheriting from an existing one:

```python
from fluidsim.solvers.ns2d.solver import Simul as SimulNS2D
from fluidsim.base.setofvariables import SetOfVariables

class SimulCustom(SimulNS2D):
    """Custom solver with additional physics"""

    @staticmethod
    def _complete_params_with_default(params):
        """Add custom parameters"""
        SimulNS2D._complete_params_with_default(params)
        params._set_child("custom", {"param1": 0.0})

    def __init__(self, params):
        super().__init__(params)
        # Custom initialization

    def tendencies_nonlin(self, state_spect=None):
        """Override to add custom tendencies"""
        tendencies = super().tendencies_nonlin(state_spect)

        # Add custom terms
        # tendencies.vx_fft += custom_term_vx
        # tendencies.vy_fft += custom_term_vy

        return tendencies
```

Use the custom solver:
```python
params = SimulCustom.create_default_params()
# Configure params...
sim = SimulCustom(params)
sim.time_stepping.start()
```

## Online Visualization

Display fields during simulation:

```python
params.output.ONLINE_PLOT_OK = True
params.output.periods_plot.phys_fields = 1.0  # plot every 1.0 time units
params.output.phys_fields.field_to_plot = "vorticity"

sim = Simul(params)
sim.time_stepping.start()
```

Plots appear in real-time during execution.

## Checkpoint and Restart

### Automatic Checkpointing

```python
params.output.periods_save.phys_fields = 1.0  # save every 1.0 time units
```

Fields are saved automatically during simulation.

### Manual Checkpointing

```python
# During simulation
sim.output.phys_fields.save()
```

### Restarting from Checkpoint

```python
params = Simul.create_default_params()
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "simulation_dir/state_phys_t5.000.h5"
params.time_stepping.t_end = 20.0  # extend simulation

sim = Simul(params)
sim.time_stepping.start()
```

## Memory and Performance Optimization

### Reduce Memory Usage

```python
# Disable unnecessary outputs
params.output.periods_save.spectra = 0  # disable spectra saving
params.output.periods_save.spect_energy_budg = 0  # disable energy budget

# Reduce spatial field saves
params.output.periods_save.phys_fields = 10.0  # save less frequently
```

### Optimize FFT Performance

```python
import os

# Select FFT library
os.environ["FLUIDSIM_TYPE_FFT2D"] = "fft2d.with_fftw"
os.environ["FLUIDSIM_TYPE_FFT3D"] = "fft3d.with_fftw"

# Or use MKL if available
# os.environ["FLUIDSIM_TYPE_FFT2D"] = "fft2d.with_mkl"
```

### Time Step Optimization

```python
# Use adaptive time stepping
params.time_stepping.USE_CFL = True
params.time_stepping.CFL = 0.8  # slightly larger CFL for faster runs

# Use efficient time scheme
params.time_stepping.type_time_scheme = "RK4"  # 4th order Runge-Kutta
```

---

## Reference: Installation

# FluidSim Installation

## Requirements

- Python >= 3.9
- Virtual environment recommended

## Installation Methods

### Basic Installation

Install fluidsim using uv:

```bash
uv pip install fluidsim
```

### With FFT Support (Required for Pseudospectral Solvers)

Most fluidsim solvers use Fourier-based methods and require FFT libraries:

```bash
uv pip install "fluidsim[fft]"
```

This installs fluidfft and pyfftw dependencies.

### With MPI and FFT (For Parallel Simulations)

For high-performance parallel computing:

```bash
uv pip install "fluidsim[fft,mpi]"
```

Note: This triggers local compilation of mpi4py.

## Environment Configuration

### Output Directories

Set environment variables to control where simulation data is stored:

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

### FFT Method Selection

Specify FFT implementation (optional):

```bash
export FLUIDSIM_TYPE_FFT2D=fft2d.with_fftw
export FLUIDSIM_TYPE_FFT3D=fft3d.with_fftw
```

## Verification

Test the installation:

```bash
pytest --pyargs fluidsim
```

## No Authentication Required

FluidSim does not require API keys or authentication tokens.

---

## Reference: Output_Analysis

# Output and Analysis

## Output Types

FluidSim automatically saves several types of output during simulations.

### Physical Fields

**File format**: HDF5 (`.h5`)

**Location**: `simulation_dir/state_phys_t*.h5`

**Contents**: Velocity, vorticity, and other physical space fields at specific times

**Access**:
```python
sim.output.phys_fields.plot()
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("vx")
sim.output.phys_fields.plot("div")  # check divergence

# Save manually
sim.output.phys_fields.save()

# Get data
vorticity = sim.state.state_phys.get_var("rot")
```

### Spatial Means

**File format**: Text file (`.txt`)

**Location**: `simulation_dir/spatial_means.txt`

**Contents**: Volume-averaged quantities vs time (energy, enstrophy, etc.)

**Access**:
```python
sim.output.spatial_means.plot()

# Load from file
from fluidsim import load_sim_for_plot
sim = load_sim_for_plot("simulation_dir")
sim.output.spatial_means.load()
spatial_means_data = sim.output.spatial_means
```

### Spectra

**File format**: HDF5 (`.h5`)

**Location**: `simulation_dir/spectra_*.h5`

**Contents**: Energy and enstrophy spectra vs wavenumber

**Access**:
```python
sim.output.spectra.plot1d()  # 1D spectrum
sim.output.spectra.plot2d()  # 2D spectrum

# Load spectra data
spectra = sim.output.spectra.load2d_mean()
```

### Spectral Energy Budget

**File format**: HDF5 (`.h5`)

**Location**: `simulation_dir/spect_energy_budg_*.h5`

**Contents**: Energy transfer between scales

**Access**:
```python
sim.output.spect_energy_budg.plot()
```

## Post-Processing

### Loading Simulations for Analysis

#### Fast Loading (Read-Only)

```python
from fluidsim import load_sim_for_plot

sim = load_sim_for_plot("simulation_dir")

# Access all output types
sim.output.phys_fields.plot()
sim.output.spatial_means.plot()
sim.output.spectra.plot1d()
```

Use this for quick visualization and analysis. Does not initialize full simulation state.

#### Full State Loading

```python
from fluidsim import load_state_phys_file

sim = load_state_phys_file("simulation_dir/state_phys_t10.000.h5")

# Can continue simulation
sim.time_stepping.start()
```

### Visualization Tools

#### Built-in Plotting

FluidSim provides basic plotting through matplotlib:

```python
# Physical fields
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.animate("vorticity")

# Time series
sim.output.spatial_means.plot()

# Spectra
sim.output.spectra.plot1d()
```

#### Advanced Visualization

For publication-quality or 3D visualization:

**ParaView**: Open `.h5` files directly
```bash
paraview simulation_dir/state_phys_t*.h5
```

**VisIt**: Similar to ParaView for large datasets

**Custom Python**:
```python
import h5py
import matplotlib.pyplot as plt

# Load field manually
with h5py.File("state_phys_t10.000.h5", "r") as f:
    vx = f["state_phys"]["vx"][:]
    vy = f["state_phys"]["vy"][:]

# Custom plotting
plt.contourf(vx)
plt.show()
```

## Analysis Examples

### Energy Evolution

```python
from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt

sim = load_sim_for_plot("simulation_dir")
df = sim.output.spatial_means.load()

plt.figure()
plt.plot(df["t"], df["E"], label="Kinetic Energy")
plt.xlabel("Time")
plt.ylabel("Energy")
plt.legend()
plt.show()
```

### Spectral Analysis

```python
sim = load_sim_for_plot("simulation_dir")

# Plot energy spectrum
sim.output.spectra.plot1d(tmin=5.0, tmax=10.0)  # average over time range

# Get spectral data
k, E_k = sim.output.spectra.load1d_mean(tmin=5.0, tmax=10.0)

# Check for power law
import numpy as np
log_k = np.log(k)
log_E = np.log(E_k)
# fit power law in inertial range
```

### Parametric Study Analysis

When running multiple simulations with different parameters:

```python
import os
import pandas as pd
from fluidsim import load_sim_for_plot

# Collect results from multiple simulations
results = []
for sim_dir in os.listdir("simulations"):
    if not os.path.isdir(f"simulations/{sim_dir}"):
        continue

    sim = load_sim_for_plot(f"simulations/{sim_dir}")

    # Extract key metrics
    df = sim.output.spatial_means.load()
    final_energy = df["E"].iloc[-1]

    # Get parameters
    nu = sim.params.nu_2

    results.append({
        "nu": nu,
        "final_energy": final_energy,
        "sim_dir": sim_dir
    })

# Analyze results
results_df = pd.DataFrame(results)
results_df.plot(x="nu", y="final_energy", logx=True)
```

### Field Manipulation

```python
sim = load_sim_for_plot("simulation_dir")

# Load specific time
sim.output.phys_fields.set_of_phys_files.update_times()
times = sim.output.phys_fields.set_of_phys_files.times

# Load field at specific time
field_file = sim.output.phys_fields.get_field_to_plot(time=5.0)
vorticity = field_file.get_var("rot")

# Compute derived quantities
import numpy as np
vorticity_rms = np.sqrt(np.mean(vorticity**2))
vorticity_max = np.max(np.abs(vorticity))
```

## Output Directory Structure

```
simulation_dir/
├── params_simul.xml         # Simulation parameters
├── stdout.txt               # Standard output log
├── state_phys_t*.h5         # Physical fields at different times
├── spatial_means.txt        # Time series of spatial averages
├── spectra_*.h5            # Spectral data
├── spect_energy_budg_*.h5  # Energy budget data
└── info_solver.txt         # Solver information
```

## Performance Monitoring

```python
# During simulation, check progress
sim.output.print_stdout.complete_timestep()

# After simulation, review performance
sim.output.print_stdout.plot_deltat()  # plot time step evolution
sim.output.print_stdout.plot_clock_times()  # plot computation time
```

## Data Export

Convert fluidsim output to other formats:

```python
import h5py
import numpy as np

# Export to numpy array
with h5py.File("state_phys_t10.000.h5", "r") as f:
    vx = f["state_phys"]["vx"][:]
    np.save("vx.npy", vx)

# Export to CSV
df = sim.output.spatial_means.load()
df.to_csv("spatial_means.csv", index=False)
```

---

## Reference: Parameters

# Parameter Configuration

## Parameters Object

The `Parameters` object is hierarchical and organized into logical groups. Access using dot notation:

```python
params = Simul.create_default_params()
params.group.subgroup.parameter = value
```

## Key Parameter Groups

### Operators (`params.oper`)

Define domain and resolution:

```python
params.oper.nx = 256  # number of grid points in x
params.oper.ny = 256  # number of grid points in y
params.oper.nz = 128  # number of grid points in z (3D only)

params.oper.Lx = 2 * pi  # domain length in x
params.oper.Ly = 2 * pi  # domain length in y
params.oper.Lz = pi      # domain length in z (3D only)

params.oper.coef_dealiasing = 2./3.  # dealiasing cutoff (default 2/3)
```

**Resolution guidance**: Use powers of 2 for optimal FFT performance (128, 256, 512, 1024, etc.)

### Physical Parameters

#### Viscosity

```python
params.nu_2 = 1e-3  # Laplacian viscosity (negative Laplacian)
params.nu_4 = 0     # hyperviscosity (optional)
params.nu_8 = 0     # hyper-hyperviscosity (very high wavenumber damping)
```

Higher-order viscosity (`nu_4`, `nu_8`) damps high wavenumbers without affecting large scales.

#### Stratification (Stratified Solvers)

```python
params.N = 1.0  # Brunt-Väisälä frequency (buoyancy frequency)
```

#### Rotation (Shallow Water)

```python
params.f = 1.0  # Coriolis parameter
params.c2 = 10.0  # squared phase velocity (gravity wave speed)
```

### Time Stepping (`params.time_stepping`)

```python
params.time_stepping.t_end = 10.0  # simulation end time
params.time_stepping.it_end = 100  # or maximum iterations

params.time_stepping.deltat0 = 0.01  # initial time step
params.time_stepping.USE_CFL = True  # adaptive CFL-based time step
params.time_stepping.CFL = 0.5  # CFL number (if USE_CFL=True)

params.time_stepping.type_time_scheme = "RK4"  # or "RK2", "Euler"
```

**Recommended**: Use `USE_CFL=True` with `CFL=0.5` for adaptive time stepping.

### Initial Fields (`params.init_fields`)

```python
params.init_fields.type = "noise"  # initialization method
```

**Available types**:
- `"noise"`: Random noise
- `"dipole"`: Vortex dipole
- `"vortex"`: Single vortex
- `"taylor_green"`: Taylor-Green vortex
- `"from_file"`: Load from file
- `"in_script"`: Define in script

#### From File

```python
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "path/to/state_file.h5"
```

#### In Script

```python
params.init_fields.type = "in_script"

# Define initialization after creating sim
sim = Simul(params)

# Access state fields
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")

# Set fields
X, Y = sim.oper.get_XY_loc()
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)

# Run simulation
sim.time_stepping.start()
```

### Output Settings (`params.output`)

#### Output Directory

```python
params.output.sub_directory = "my_simulation"
```

Directory created within `$FLUIDSIM_PATH` or current directory.

#### Save Periods

```python
params.output.periods_save.phys_fields = 1.0  # save fields every 1.0 time units
params.output.periods_save.spectra = 0.5      # save spectra
params.output.periods_save.spatial_means = 0.1  # save spatial averages
params.output.periods_save.spect_energy_budg = 0.5  # spectral energy budget
```

Set to `0` to disable a particular output type.

#### Print Control

```python
params.output.periods_print.print_stdout = 0.5  # print status every 0.5 time units
```

#### Online Plotting

```python
params.output.periods_plot.phys_fields = 2.0  # plot every 2.0 time units

# Must also enable the output module
params.output.ONLINE_PLOT_OK = True
params.output.phys_fields.field_to_plot = "vorticity"  # or "vx", "vy", etc.
```

### Forcing (`params.forcing`)

Add forcing terms to maintain energy:

```python
params.forcing.enable = True
params.forcing.type = "tcrandom"  # time-correlated random forcing

# Forcing parameters
params.forcing.nkmax_forcing = 5  # maximum forced wavenumber
params.forcing.nkmin_forcing = 2  # minimum forced wavenumber
params.forcing.forcing_rate = 1.0  # energy injection rate
```

**Common forcing types**:
- `"tcrandom"`: Time-correlated random forcing
- `"proportional"`: Proportional forcing (maintains specific spectrum)
- `"in_script"`: Custom forcing defined in script

## Parameter Safety

The Parameters object raises `AttributeError` when accessing non-existent parameters:

```python
params.nu_2 = 1e-3  # OK
params.nu2 = 1e-3   # ERROR: AttributeError
```

This prevents typos that would be silently ignored in text-based configuration files.

## Viewing All Parameters

```python
# Print all parameters
params._print_as_xml()

# Get as dictionary
param_dict = params._make_dict()
```

## Saving Parameter Configuration

Parameters are automatically saved with simulation output:

```python
params._save_as_xml("simulation_params.xml")
params._save_as_json("simulation_params.json")
```

---

## Reference: Simulation_Workflow

# Simulation Workflow

## Standard Workflow

Follow these steps to run a fluidsim simulation:

### 1. Import Solver

```python
from fluidsim.solvers.ns2d.solver import Simul

# Or use dynamic import
import fluidsim
Simul = fluidsim.import_simul_class_from_key("ns2d")
```

### 2. Create Default Parameters

```python
params = Simul.create_default_params()
```

This returns a hierarchical `Parameters` object containing all simulation settings.

### 3. Configure Parameters

Modify parameters as needed. The Parameters object prevents typos by raising `AttributeError` for non-existent parameters:

```python
# Domain and resolution
params.oper.nx = 256  # grid points in x
params.oper.ny = 256  # grid points in y
params.oper.Lx = 2 * pi  # domain size x
params.oper.Ly = 2 * pi  # domain size y

# Physical parameters
params.nu_2 = 1e-3  # viscosity (negative Laplacian)

# Time stepping
params.time_stepping.t_end = 10.0  # end time
params.time_stepping.deltat0 = 0.01  # initial time step
params.time_stepping.USE_CFL = True  # adaptive time step

# Initial conditions
params.init_fields.type = "noise"  # or "dipole", "vortex", etc.

# Output settings
params.output.periods_save.phys_fields = 1.0  # save every 1.0 time units
params.output.periods_save.spectra = 0.5
params.output.periods_save.spatial_means = 0.1
```

### 4. Instantiate Simulation

```python
sim = Simul(params)
```

This initializes:
- Operators (FFT, differential operators)
- State variables (velocity, vorticity, etc.)
- Output handlers
- Time stepping scheme

### 5. Run Simulation

```python
sim.time_stepping.start()
```

The simulation runs until `t_end` or specified number of iterations.

### 6. Analyze Results During/After Simulation

```python
# Plot physical fields
sim.output.phys_fields.plot()
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("div")

# Plot spatial means
sim.output.spatial_means.plot()

# Plot spectra
sim.output.spectra.plot1d()
sim.output.spectra.plot2d()
```

## Loading Previous Simulations

### Quick Loading (For Plotting Only)

```python
from fluidsim import load_sim_for_plot

sim = load_sim_for_plot("path/to/simulation")
sim.output.phys_fields.plot()
sim.output.spatial_means.plot()
```

Fast loading without full state initialization. Use for post-processing.

### Full State Loading (For Restarting)

```python
from fluidsim import load_state_phys_file

sim = load_state_phys_file("path/to/state_file.h5")
sim.time_stepping.start()  # continue simulation
```

Loads complete state for continuing simulations.

## Restarting Simulations

To restart from a saved state:

```python
params = Simul.create_default_params()
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "path/to/state_file.h5"

# Optionally modify parameters for the continuation
params.time_stepping.t_end = 20.0  # extend simulation

sim = Simul(params)
sim.time_stepping.start()
```

## Running on Clusters

FluidSim integrates with cluster submission systems:

```python
from fluiddyn.clusters.legi import Calcul8 as Cluster

# Configure cluster job
cluster = Cluster()
cluster.submit_script(
    "my_simulation.py",
    name_run="my_job",
    nb_nodes=4,
    nb_cores_per_node=24,
    walltime="24:00:00"
)
```

Script should contain standard workflow steps (import, configure, run).

## Complete Example

```python
from fluidsim.solvers.ns2d.solver import Simul
from math import pi

# Create and configure parameters
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "dipole"
params.output.periods_save.phys_fields = 1.0

# Run simulation
sim = Simul(params)
sim.time_stepping.start()

# Analyze results
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```

---

## Reference: Solvers

# FluidSim Solvers

FluidSim provides multiple solvers for different fluid dynamics equations. All solvers work on periodic domains using pseudospectral methods with FFT.

## Available Solvers

### 2D Incompressible Navier-Stokes

**Solver key**: `ns2d`

**Import**:
```python
from fluidsim.solvers.ns2d.solver import Simul
# or dynamically
Simul = fluidsim.import_simul_class_from_key("ns2d")
```

**Use for**: 2D turbulence studies, vortex dynamics, fundamental fluid flow simulations

**Key features**: Energy and enstrophy cascades, vorticity dynamics

### 3D Incompressible Navier-Stokes

**Solver key**: `ns3d`

**Import**:
```python
from fluidsim.solvers.ns3d.solver import Simul
```

**Use for**: 3D turbulence, realistic fluid flow simulations, high-resolution DNS

**Key features**: Full 3D turbulence dynamics, parallel computing support

### Stratified Flows (2D/3D)

**Solver keys**: `ns2d.strat`, `ns3d.strat`

**Import**:
```python
from fluidsim.solvers.ns2d.strat.solver import Simul  # 2D
from fluidsim.solvers.ns3d.strat.solver import Simul  # 3D
```

**Use for**: Oceanic and atmospheric flows, density-driven flows

**Key features**: Boussinesq approximation, buoyancy effects, constant Brunt-Väisälä frequency

**Parameters**: Set stratification via `params.N` (Brunt-Väisälä frequency)

### Shallow Water Equations

**Solver key**: `sw1l` (one-layer)

**Import**:
```python
from fluidsim.solvers.sw1l.solver import Simul
```

**Use for**: Geophysical flows, tsunami modeling, rotating flows

**Key features**: Rotating frame support, geostrophic balance

**Parameters**: Set rotation via `params.f` (Coriolis parameter)

### Föppl-von Kármán Equations

**Solver key**: `fvk` (elastic plate equations)

**Import**:
```python
from fluidsim.solvers.fvk.solver import Simul
```

**Use for**: Elastic plate dynamics, fluid-structure interaction studies

## Solver Selection Guide

Choose a solver based on the physical problem:

1. **2D turbulence, quick testing**: Use `ns2d`
2. **3D flows, realistic simulations**: Use `ns3d`
3. **Density-stratified flows**: Use `ns2d.strat` or `ns3d.strat`
4. **Geophysical flows, rotating systems**: Use `sw1l`
5. **Elastic plates**: Use `fvk`

## Modified Versions

Many solvers have modified versions with additional physics:
- Forcing terms
- Different boundary conditions
- Additional scalar fields

Check `fluidsim.solvers` module for complete list.
