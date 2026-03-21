---
title: "Pylabrobot"
description: "Vendor-agnostic lab automation framework. Use when controlling multiple equipment types (Hamilton, Tecan, Opentrons, plate readers, pumps) or needing unified programming across different vendors. Best for complex workflows, multi-vendor setups, si..."
category: "workflow"
source: "community"
author: "Community"
tags: ["pylabrobot"]
date: 2026-03-20
---

# PyLabRobot

## Overview

PyLabRobot is a hardware-agnostic, pure Python Software Development Kit for automated and autonomous laboratories. Use this skill to control liquid handling robots, plate readers, pumps, heater shakers, incubators, centrifuges, and other laboratory automation equipment through a unified Python interface that works across platforms (Windows, macOS, Linux).

## When to Use This Skill

Use this skill when:
- Programming liquid handling robots (Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO)
- Automating laboratory workflows involving pipetting, sample preparation, or analytical measurements
- Managing deck layouts and laboratory resources (plates, tips, containers, troughs)
- Integrating multiple lab devices (liquid handlers, plate readers, heater shakers, pumps)
- Creating reproducible laboratory protocols with state management
- Simulating protocols before running on physical hardware
- Reading plates using BMG CLARIOstar or other supported plate readers
- Controlling temperature, shaking, centrifugation, or other material handling operations
- Working with laboratory automation in Python

## Core Capabilities

PyLabRobot provides comprehensive laboratory automation through six main capability areas, each detailed in the references/ directory:

### 1. Liquid Handling (`references/liquid-handling.md`)

Control liquid handling robots for aspirating, dispensing, and transferring liquids. Key operations include:
- **Basic Operations**: Aspirate, dispense, transfer liquids between wells
- **Tip Management**: Pick up, drop, and track pipette tips automatically
- **Advanced Techniques**: Multi-channel pipetting, serial dilutions, plate replication
- **Volume Tracking**: Automatic tracking of liquid volumes in wells
- **Hardware Support**: Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO, and others

### 2. Resource Management (`references/resources.md`)

Manage laboratory resources in a hierarchical system:
- **Resource Types**: Plates, tip racks, troughs, tubes, carriers, and custom labware
- **Deck Layout**: Assign resources to deck positions with coordinate systems
- **State Management**: Track tip presence, liquid volumes, and resource states
- **Serialization**: Save and load deck layouts and states from JSON files
- **Resource Discovery**: Access wells, tips, and containers through intuitive APIs

### 3. Hardware Backends (`references/hardware-backends.md`)

Connect to diverse laboratory equipment through backend abstraction:
- **Liquid Handlers**: Hamilton STAR (full support), Opentrons OT-2, Tecan EVO
- **Simulation**: ChatterboxBackend for protocol testing without hardware
- **Platform Support**: Works on Windows, macOS, Linux, and Raspberry Pi
- **Backend Switching**: Change robots by swapping backend without rewriting protocols

### 4. Analytical Equipment (`references/analytical-equipment.md`)

Integrate plate readers and analytical instruments:
- **Plate Readers**: BMG CLARIOstar for absorbance, luminescence, fluorescence
- **Scales**: Mettler Toledo integration for mass measurements
- **Integration Patterns**: Combine liquid handlers with analytical equipment
- **Automated Workflows**: Move plates between devices automatically

### 5. Material Handling (`references/material-handling.md`)

Control environmental and material handling equipment:
- **Heater Shakers**: Hamilton HeaterShaker, Inheco ThermoShake
- **Incubators**: Inheco and Thermo Fisher incubators with temperature control
- **Centrifuges**: Agilent VSpin with bucket positioning and spin control
- **Pumps**: Cole Parmer Masterflex for fluid pumping operations
- **Temperature Control**: Set and monitor temperatures during protocols

### 6. Visualization & Simulation (`references/visualization.md`)

Visualize and simulate laboratory protocols:
- **Browser Visualizer**: Real-time 3D visualization of deck state
- **Simulation Mode**: Test protocols without physical hardware
- **State Tracking**: Monitor tip presence and liquid volumes visually
- **Deck Editor**: Graphical tool for designing deck layouts
- **Protocol Validation**: Verify protocols before running on hardware

## Quick Start

To get started with PyLabRobot, install the package and initialize a liquid handler:

```python
# Install PyLabRobot
# uv pip install pylabrobot

# Basic liquid handling setup
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Initialize liquid handler
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Basic operations
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()
```

## Working with References

This skill organizes detailed information across multiple reference files. Load the relevant reference when:
- **Liquid Handling**: Writing pipetting protocols, tip management, transfers
- **Resources**: Defining deck layouts, managing plates/tips, custom labware
- **Hardware Backends**: Connecting to specific robots, switching platforms
- **Analytical Equipment**: Integrating plate readers, scales, or analytical devices
- **Material Handling**: Using heater shakers, incubators, centrifuges, pumps
- **Visualization**: Simulating protocols, visualizing deck states

All reference files can be found in the `references/` directory and contain comprehensive examples, API usage patterns, and best practices.

## Best Practices

When creating laboratory automation protocols with PyLabRobot:

1. **Start with Simulation**: Use ChatterboxBackend and the visualizer to test protocols before running on hardware
2. **Enable Tracking**: Turn on tip tracking and volume tracking for accurate state management
3. **Resource Naming**: Use clear, descriptive names for all resources (plates, tip racks, containers)
4. **State Serialization**: Save deck layouts and states to JSON for reproducibility
5. **Error Handling**: Implement proper async error handling for hardware operations
6. **Temperature Control**: Set temperatures early as heating/cooling takes time
7. **Modular Protocols**: Break complex workflows into reusable functions
8. **Documentation**: Reference official docs at https://docs.pylabrobot.org for latest features

## Common Workflows

### Liquid Transfer Protocol

```python
# Setup
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tip_rack")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Transfer protocol
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(source_plate["A1:H12"], dest_plate["A1:H12"], vols=100)
await lh.drop_tips()
```

### Plate Reading Workflow

```python
# Setup plate reader
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
await pr.setup()

# Set temperature and read
await pr.set_temperature(37)
await pr.open()
# (manually or robotically load plate)
await pr.close()
data = await pr.read_absorbance(wavelength=450)
```

## Additional Resources

- **Official Documentation**: https://docs.pylabrobot.org
- **GitHub Repository**: https://github.com/PyLabRobot/pylabrobot
- **Community Forum**: https://discuss.pylabrobot.org
- **PyPI Package**: https://pypi.org/project/PyLabRobot/

For detailed usage of specific capabilities, refer to the corresponding reference file in the `references/` directory.

---

## Reference: Analytical Equipment

# Analytical Equipment in PyLabRobot

## Overview

PyLabRobot integrates with analytical equipment including plate readers, scales, and other measurement devices. This allows automated workflows that combine liquid handling with analytical measurements.

## Plate Readers

### BMG CLARIOstar (Plus)

The BMG Labtech CLARIOstar and CLARIOstar Plus are microplate readers that measure absorbance, luminescence, and fluorescence.

#### Hardware Setup

**Physical Connections:**
1. IEC C13 power cord to mains power
2. USB-B cable to computer (with security screws on device end)
3. Optional: RS-232 port for plate stacking units

**Communication:**
- Serial connection through FTDI/USB-A at firmware level
- Cross-platform support (Windows, macOS, Linux)

#### Software Setup

```python
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

# Create backend
backend = CLARIOstarBackend()

# Initialize plate reader
pr = PlateReader(
    name="CLARIOstar",
    backend=backend,
    size_x=0.0,    # Physical dimensions not critical for plate readers
    size_y=0.0,
    size_z=0.0
)

# Setup (initializes device)
await pr.setup()

# When done
await pr.stop()
```

#### Basic Operations

**Opening and Closing:**

```python
# Open loading tray
await pr.open()

# (Load plate manually or robotically)

# Close loading tray
await pr.close()
```

**Temperature Control:**

```python
# Set temperature (in Celsius)
await pr.set_temperature(37)

# Note: Reaching temperature is slow
# Set temperature early in protocol
```

**Reading Measurements:**

```python
# Absorbance reading
data = await pr.read_absorbance(wavelength=450)  # nm

# Luminescence reading
data = await pr.read_luminescence()

# Fluorescence reading
data = await pr.read_fluorescence(
    excitation_wavelength=485,  # nm
    emission_wavelength=535     # nm
)
```

#### Data Format

Plate reader methods return array data:

```python
import numpy as np

# Read absorbance
data = await pr.read_absorbance(wavelength=450)

# data is typically a 2D array (8x12 for 96-well plate)
print(f"Data shape: {data.shape}")
print(f"Well A1: {data[0][0]}")
print(f"Well H12: {data[7][11]}")

# Convert to DataFrame for easier handling
import pandas as pd
df = pd.DataFrame(data)
```

#### Integration with Liquid Handler

Combine plate reading with liquid handling:

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

# Initialize liquid handler
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Initialize plate reader
pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
await pr.setup()

# Set temperature early
await pr.set_temperature(37)

try:
    # Prepare samples with liquid handler
    tip_rack = TIP_CAR_480_A00(name="tips")
    reagent_plate = Cos_96_DW_1mL(name="reagents")
    assay_plate = Cos_96_DW_1mL(name="assay")

    lh.deck.assign_child_resource(tip_rack, rails=1)
    lh.deck.assign_child_resource(reagent_plate, rails=10)
    lh.deck.assign_child_resource(assay_plate, rails=15)

    # Transfer samples
    await lh.pick_up_tips(tip_rack["A1:H1"])
    await lh.transfer(
        reagent_plate["A1:H12"],
        assay_plate["A1:H12"],
        vols=100
    )
    await lh.drop_tips()

    # Move plate to reader (manual or robotic arm)
    print("Move assay plate to plate reader")
    input("Press Enter when plate is loaded...")

    # Read plate
    await pr.open()
    # (plate loaded here)
    await pr.close()

    data = await pr.read_absorbance(wavelength=450)
    print(f"Absorbance data: {data}")

finally:
    await lh.stop()
    await pr.stop()
```

#### Advanced Features

**Development Status:**

Some CLARIOstar features are under development:
- Spectral scanning
- Injector needle control
- Detailed measurement parameter configuration
- Well-specific reading patterns

Check current documentation for latest feature support.

#### Best Practices

1. **Temperature Control**: Set temperature early as heating is slow
2. **Plate Loading**: Ensure plate is properly seated before closing
3. **Measurement Selection**: Choose appropriate wavelengths for your assay
4. **Data Validation**: Check measurement quality and expected ranges
5. **Error Handling**: Handle timeout and communication errors
6. **Maintenance**: Keep optics clean per manufacturer guidelines

#### Example: Complete Plate Reading Workflow

```python
async def run_plate_reading_assay():
    """Complete workflow with sample prep and reading"""

    # Initialize equipment
    lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
    pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())

    await lh.setup()
    await pr.setup()

    # Set plate reader temperature
    await pr.set_temperature(37)

    try:
        # Define resources
        tip_rack = TIP_CAR_480_A00(name="tips")
        samples = Cos_96_DW_1mL(name="samples")
        assay_plate = Cos_96_DW_1mL(name="assay")
        substrate = Trough_100ml(name="substrate")

        lh.deck.assign_child_resource(tip_rack, rails=1)
        lh.deck.assign_child_resource(substrate, rails=5)
        lh.deck.assign_child_resource(samples, rails=10)
        lh.deck.assign_child_resource(assay_plate, rails=15)

        # Transfer samples
        await lh.pick_up_tips(tip_rack["A1:H1"])
        await lh.transfer(
            samples["A1:H12"],
            assay_plate["A1:H12"],
            vols=50
        )
        await lh.drop_tips()

        # Add substrate
        await lh.pick_up_tips(tip_rack["A2:H2"])
        for col in range(1, 13):
            await lh.transfer(
                substrate["channel_1"],
                assay_plate[f"A{col}:H{col}"],
                vols=50
            )
        await lh.drop_tips()

        # Incubate (if needed)
        # await asyncio.sleep(300)  # 5 minutes

        # Move to plate reader
        print("Transfer assay plate to CLARIOstar")
        input("Press Enter when ready...")

        await pr.open()
        input("Press Enter when plate is loaded...")
        await pr.close()

        # Read absorbance
        data = await pr.read_absorbance(wavelength=450)

        # Process results
        import pandas as pd
        df = pd.DataFrame(
            data,
            index=[f"{r}" for r in "ABCDEFGH"],
            columns=[f"{c}" for c in range(1, 13)]
        )

        print("Absorbance Results:")
        print(df)

        # Save results
        df.to_csv("plate_reading_results.csv")

        return df

    finally:
        await lh.stop()
        await pr.stop()

# Run assay
results = await run_plate_reading_assay()
```

## Scales

### Mettler Toledo Scales

PyLabRobot supports Mettler Toledo scales for mass measurements.

#### Setup

```python
from pylabrobot.scales import Scale
from pylabrobot.scales.mettler_toledo_backend import MettlerToledoBackend

# Create scale
scale = Scale(
    name="analytical_scale",
    backend=MettlerToledoBackend()
)

await scale.setup()
```

#### Operations

```python
# Get weight measurement
weight = await scale.get_weight()  # Returns weight in grams
print(f"Weight: {weight} g")

# Tare (zero) the scale
await scale.tare()

# Get multiple measurements
weights = []
for i in range(5):
    w = await scale.get_weight()
    weights.append(w)
    await asyncio.sleep(1)

average_weight = sum(weights) / len(weights)
print(f"Average weight: {average_weight} g")
```

#### Integration with Liquid Handler

```python
# Weigh samples during protocol
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
scale = Scale(name="scale", backend=MettlerToledoBackend())

await lh.setup()
await scale.setup()

try:
    # Tare scale
    await scale.tare()

    # Dispense liquid
    await lh.pick_up_tips(tip_rack["A1"])
    await lh.aspirate(reagent["A1"], vols=1000)

    # (Move to scale position)

    # Dispense and weigh
    await lh.dispense(container, vols=1000)
    weight = await scale.get_weight()

    print(f"Dispensed weight: {weight} g")

    # Calculate actual volume (assuming density = 1 g/mL for water)
    actual_volume = weight * 1000  # Convert g to µL
    print(f"Actual volume: {actual_volume} µL")

    await lh.drop_tips()

finally:
    await lh.stop()
    await scale.stop()
```

## Other Analytical Devices

### Flow Cytometers

Some flow cytometer integrations are in development. Check current documentation for support status.

### Spectrophotometers

Additional spectrophotometer models may be supported. Check documentation for current device compatibility.

## Multi-Device Workflows

### Coordinating Multiple Devices

```python
async def multi_device_workflow():
    """Coordinate liquid handler, plate reader, and scale"""

    # Initialize all devices
    lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
    pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
    scale = Scale(name="scale", backend=MettlerToledoBackend())

    await lh.setup()
    await pr.setup()
    await scale.setup()

    try:
        # 1. Weigh reagent
        await scale.tare()
        # (place container on scale)
        reagent_weight = await scale.get_weight()

        # 2. Prepare samples with liquid handler
        await lh.pick_up_tips(tip_rack["A1:H1"])
        await lh.transfer(source["A1:H12"], dest["A1:H12"], vols=100)
        await lh.drop_tips()

        # 3. Read plate
        await pr.open()
        # (load plate)
        await pr.close()
        data = await pr.read_absorbance(wavelength=450)

        return {
            "reagent_weight": reagent_weight,
            "absorbance_data": data
        }

    finally:
        await lh.stop()
        await pr.stop()
        await scale.stop()
```

## Best Practices

1. **Device Initialization**: Setup all devices at start of protocol
2. **Error Handling**: Handle communication errors gracefully
3. **Cleanup**: Always call `stop()` on all devices
4. **Timing**: Account for device-specific timing (temperature equilibration, measurement time)
5. **Calibration**: Follow manufacturer calibration procedures
6. **Data Validation**: Verify measurements are within expected ranges
7. **Documentation**: Record device settings and parameters
8. **Integration Testing**: Test multi-device workflows thoroughly
9. **Concurrent Operations**: Use async to overlap operations when possible
10. **Data Storage**: Save raw data with metadata (timestamps, settings)

## Common Patterns

### Kinetic Plate Reading

```python
async def kinetic_reading(num_reads: int, interval: int):
    """Perform kinetic plate reading"""

    pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
    await pr.setup()

    try:
        await pr.set_temperature(37)
        await pr.open()
        # (load plate)
        await pr.close()

        results = []
        for i in range(num_reads):
            data = await pr.read_absorbance(wavelength=450)
            timestamp = time.time()
            results.append({
                "read_number": i + 1,
                "timestamp": timestamp,
                "data": data
            })

            if i < num_reads - 1:
                await asyncio.sleep(interval)

        return results

    finally:
        await pr.stop()

# Read every 30 seconds for 10 minutes
results = await kinetic_reading(num_reads=20, interval=30)
```

## Additional Resources

- Plate Reading Documentation: https://docs.pylabrobot.org/user_guide/02_analytical/
- BMG CLARIOstar Guide: https://docs.pylabrobot.org/user_guide/02_analytical/plate-reading/bmg-clariostar.html
- API Reference: https://docs.pylabrobot.org/api/pylabrobot.plate_reading.html
- Supported Equipment: https://docs.pylabrobot.org/user_guide/machines.html

---

## Reference: Hardware Backends

# Hardware Backends in PyLabRobot

## Overview

PyLabRobot uses a backend abstraction system that allows the same protocol code to run on different liquid handling robots and platforms. Backends handle device-specific communication while the `LiquidHandler` frontend provides a unified interface.

## Backend Architecture

### How Backends Work

1. **Frontend**: `LiquidHandler` class provides high-level API
2. **Backend**: Device-specific class handles hardware communication
3. **Protocol**: Same code works across different backends

```python
# Same protocol code
await lh.pick_up_tips(tip_rack["A1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()

# Works with any backend (STAR, Opentrons, simulation, etc.)
```

### Backend Interface

All backends inherit from `LiquidHandlerBackend` and implement:
- `setup()`: Initialize connection to hardware
- `stop()`: Close connection and cleanup
- Device-specific command methods (aspirate, dispense, etc.)

## Supported Backends

### Hamilton STAR (Full Support)

The Hamilton STAR and STARlet liquid handling robots have full PyLabRobot support.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Create STAR backend
backend = STAR()

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

**Platform Support:**
- Windows ✅
- macOS ✅
- Linux ✅
- Raspberry Pi ✅

**Communication:**
- USB connection to robot
- Direct firmware commands
- No Hamilton software required

**Features:**
- Full liquid handling operations
- CO-RE tip support
- 96-channel head support (if equipped)
- Temperature control
- Carrier and rail-based positioning

**Deck Types:**
```python
from pylabrobot.resources import STARLetDeck, STARDeck

# For STARlet (smaller deck)
deck = STARLetDeck()

# For STAR (full deck)
deck = STARDeck()
```

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL

# Initialize
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")

# Assign to rails
lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(plate, rails=10)

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()

await lh.stop()
```

### Opentrons OT-2 (Supported)

The Opentrons OT-2 is supported through the Opentrons HTTP API.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsBackend
from pylabrobot.resources import OTDeck

# Create Opentrons backend (requires robot IP address)
backend = OpentronsBackend(host="192.168.1.100")  # Replace with your robot's IP

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=OTDeck())
await lh.setup()
```

**Platform Support:**
- Any platform with network access to OT-2

**Communication:**
- HTTP API over network
- Requires robot IP address
- No Opentrons app required

**Features:**
- 8-channel pipette support
- Single-channel pipette support
- Standard OT-2 deck layout
- Coordinate-based positioning

**Limitations:**
- Uses older Opentrons HTTP API
- Some features may be limited compared to STAR

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import OpentronsBackend
from pylabrobot.resources import OTDeck

# Initialize with robot IP
lh = LiquidHandler(
    backend=OpentronsBackend(host="192.168.1.100"),
    deck=OTDeck()
)
await lh.setup()

# Load deck layout
lh.deck = Deck.load_from_json_file("opentrons_layout.json")

# Execute protocol
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()

await lh.stop()
```

### Tecan EVO (Work in Progress)

Support for Tecan EVO liquid handling robots is under development.

**Current Status:**
- Work-in-progress
- Basic commands may be available
- Check documentation for current feature support

**Setup (when available):**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import TecanBackend
from pylabrobot.resources import TecanDeck

backend = TecanBackend()
lh = LiquidHandler(backend=backend, deck=TecanDeck())
```

### Hamilton Vantage (Mostly Supported)

Hamilton Vantage has "mostly" complete support.

**Setup:**

```python
from pylabrobot.liquid_handling.backends import Vantage
from pylabrobot.resources import VantageDeck

lh = LiquidHandler(backend=Vantage(), deck=VantageDeck())
```

**Features:**
- Similar to STAR support
- Some advanced features may be limited

## Simulation Backend

### ChatterboxBackend (Simulation)

Test protocols without physical hardware using the simulation backend.

**Setup:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck

# Create simulation backend
backend = ChatterboxBackend(num_channels=8)

# Initialize liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
await lh.setup()
```

**Features:**
- No hardware required
- Simulates all liquid handling operations
- Works with visualizer for real-time feedback
- Validates protocol logic
- Tracks tips and volumes

**Use Cases:**
- Protocol development and testing
- Training and education
- CI/CD pipeline testing
- Debugging without hardware access

**Example:**

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable tracking for simulation
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize with simulation backend
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(plate, rails=10)

# Set initial volumes
for well in plate.children:
    well.tracker.set_liquids([(None, 200)])

# Run simulated protocol
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(plate["A1:H1"], plate["A2:H2"], vols=100)
await lh.drop_tips()

# Check results
print(f"A1 volume: {plate['A1'].tracker.get_volume()} µL")  # 100 µL
print(f"A2 volume: {plate['A2'].tracker.get_volume()} µL")  # 100 µL

await lh.stop()
```

## Switching Backends

### Backend-Agnostic Protocols

Write protocols that work with any backend:

```python
def get_backend(robot_type: str):
    """Factory function to create appropriate backend"""
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STAR
        return STAR()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsBackend
        return OpentronsBackend(host="192.168.1.100")
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
        return ChatterboxBackend()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

def get_deck(robot_type: str):
    """Factory function to create appropriate deck"""
    if robot_type == "star":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.resources import OTDeck
        return OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.resources import STARLetDeck
        return STARLetDeck()
    else:
        raise ValueError(f"Unknown robot type: {robot_type}")

# Use in protocol
robot_type = "simulation"  # Change to "star" or "opentrons" as needed
backend = get_backend(robot_type)
deck = get_deck(robot_type)

lh = LiquidHandler(backend=backend, deck=deck)
await lh.setup()

# Protocol code works with any backend
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(plate["A1"], plate["A2"], vols=100)
await lh.drop_tips()
```

### Development Workflow

1. **Develop**: Write protocol using ChatterboxBackend
2. **Test**: Run with visualizer to validate logic
3. **Verify**: Test on simulation with real deck layout
4. **Deploy**: Switch to hardware backend (STAR, Opentrons)

```python
# Development
lh = LiquidHandler(backend=ChatterboxBackend(), deck=STARLetDeck())

# ... develop protocol ...

# Production (just change backend)
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
```

## Backend Configuration

### Custom Backend Parameters

Some backends accept configuration parameters:

```python
# Opentrons with custom parameters
backend = OpentronsBackend(
    host="192.168.1.100",
    port=31950  # Default Opentrons API port
)

# ChatterboxBackend with custom channels
backend = ChatterboxBackend(
    num_channels=8  # 8-channel simulation
)
```

### Connection Troubleshooting

**Hamilton STAR:**
- Ensure USB cable is connected
- Check that no other software is using the robot
- Verify firmware is up to date
- On macOS/Linux, may need USB permissions

**Opentrons OT-2:**
- Verify robot IP address is correct
- Check network connectivity (ping robot)
- Ensure robot is powered on
- Confirm Opentrons app is not blocking API access

**General:**
- Use `await lh.setup()` to test connection
- Check error messages for specific issues
- Ensure proper permissions for device access

## Backend-Specific Features

### Hamilton STAR Specific

```python
# Access backend directly for hardware-specific features
star_backend = lh.backend

# Hamilton-specific commands (if needed)
# Most operations should go through LiquidHandler interface
```

### Opentrons Specific

```python
# Opentrons-specific configuration
ot_backend = lh.backend

# Access OT-2 API directly if needed (advanced)
# Most operations should go through LiquidHandler interface
```

## Best Practices

1. **Abstract Hardware**: Write backend-agnostic protocols when possible
2. **Test in Simulation**: Always test with ChatterboxBackend first
3. **Factory Pattern**: Use factory functions to create backends
4. **Error Handling**: Handle connection errors gracefully
5. **Documentation**: Document which backends your protocol supports
6. **Configuration**: Use config files for backend parameters
7. **Version Control**: Track backend versions and compatibility
8. **Cleanup**: Always call `await lh.stop()` to release hardware
9. **Single Connection**: Only one program should connect to hardware at a time
10. **Platform Testing**: Test on target platform before deployment

## Common Patterns

### Multi-Backend Support

```python
import asyncio
from typing import Literal

async def run_protocol(
    robot_type: Literal["star", "opentrons", "simulation"],
    visualize: bool = False
):
    """Run protocol on specified backend"""

    # Create backend
    if robot_type == "star":
        from pylabrobot.liquid_handling.backends import STAR
        backend = STAR()
        deck = STARLetDeck()
    elif robot_type == "opentrons":
        from pylabrobot.liquid_handling.backends import OpentronsBackend
        backend = OpentronsBackend(host="192.168.1.100")
        deck = OTDeck()
    elif robot_type == "simulation":
        from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
        backend = ChatterboxBackend()
        deck = STARLetDeck()

    # Initialize
    lh = LiquidHandler(backend=backend, deck=deck)
    await lh.setup()

    try:
        # Load deck layout (backend-agnostic)
        # lh.deck = Deck.load_from_json_file(f"{robot_type}_layout.json")

        # Execute protocol (backend-agnostic)
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        print("Protocol completed successfully!")

    finally:
        await lh.stop()

# Run on different backends
await run_protocol("simulation")      # Test in simulation
await run_protocol("star")            # Run on Hamilton STAR
await run_protocol("opentrons")       # Run on Opentrons OT-2
```

## Additional Resources

- Backend Documentation: https://docs.pylabrobot.org/user_guide/backends.html
- Supported Machines: https://docs.pylabrobot.org/user_guide/machines.html
- API Reference: https://docs.pylabrobot.org/api/pylabrobot.liquid_handling.backends.html
- GitHub Examples: https://github.com/PyLabRobot/pylabrobot/tree/main/examples

---

## Reference: Liquid Handling

# Liquid Handling with PyLabRobot

## Overview

The liquid handling module (`pylabrobot.liquid_handling`) provides a unified interface for controlling liquid handling robots. The `LiquidHandler` class serves as the main interface for all pipetting operations, working across different hardware platforms through backend abstraction.

## Basic Setup

### Initializing a Liquid Handler

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Create liquid handler with STAR backend
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# When done
await lh.stop()
```

### Switching Between Backends

Change robots by swapping the backend without rewriting protocols:

```python
# Hamilton STAR
from pylabrobot.liquid_handling.backends import STAR
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())

# Opentrons OT-2
from pylabrobot.liquid_handling.backends import OpentronsBackend
lh = LiquidHandler(backend=OpentronsBackend(host="192.168.1.100"), deck=OTDeck())

# Simulation (no hardware required)
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
lh = LiquidHandler(backend=ChatterboxBackend(), deck=STARLetDeck())
```

## Core Operations

### Tip Management

Picking up and dropping tips is fundamental to liquid handling operations:

```python
# Pick up tips from specific positions
await lh.pick_up_tips(tip_rack["A1"])           # Single tip
await lh.pick_up_tips(tip_rack["A1:H1"])        # Row of 8 tips
await lh.pick_up_tips(tip_rack["A1:A12"])       # Column of 12 tips

# Drop tips
await lh.drop_tips()                             # Drop at current location
await lh.drop_tips(waste)                        # Drop at specific location

# Return tips to original rack
await lh.return_tips()
```

**Tip Tracking**: Enable automatic tip tracking to monitor tip usage:

```python
from pylabrobot.resources import set_tip_tracking
set_tip_tracking(True)  # Enable globally
```

### Aspirating Liquids

Draw liquid from wells or containers:

```python
# Basic aspiration
await lh.aspirate(plate["A1"], vols=100)         # 100 µL from A1

# Multiple wells with same volume
await lh.aspirate(plate["A1:H1"], vols=100)      # 100 µL from each well

# Multiple wells with different volumes
await lh.aspirate(
    plate["A1:A3"],
    vols=[100, 150, 200]                          # Different volumes
)

# Advanced parameters
await lh.aspirate(
    plate["A1"],
    vols=100,
    flow_rate=50,                                 # µL/s
    liquid_height=5,                              # mm from bottom
    blow_out_air_volume=10                        # µL air
)
```

### Dispensing Liquids

Dispense liquid into wells or containers:

```python
# Basic dispensing
await lh.dispense(plate["A2"], vols=100)         # 100 µL to A2

# Multiple wells
await lh.dispense(plate["A1:H1"], vols=100)      # 100 µL to each

# Different volumes
await lh.dispense(
    plate["A1:A3"],
    vols=[100, 150, 200]
)

# Advanced parameters
await lh.dispense(
    plate["A2"],
    vols=100,
    flow_rate=50,                                 # µL/s
    liquid_height=2,                              # mm from bottom
    blow_out_air_volume=10                        # µL air
)
```

### Transferring Liquids

Transfer combines aspirate and dispense in a single operation:

```python
# Basic transfer
await lh.transfer(
    source=source_plate["A1"],
    dest=dest_plate["A1"],
    vols=100
)

# Multiple transfers (same tips)
await lh.transfer(
    source=source_plate["A1:H1"],
    dest=dest_plate["A1:H1"],
    vols=100
)

# Different volumes per well
await lh.transfer(
    source=source_plate["A1:A3"],
    dest=dest_plate["B1:B3"],
    vols=[50, 100, 150]
)

# With tip handling
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source=source_plate["A1:H12"],
    dest=dest_plate["A1:H12"],
    vols=100
)
await lh.drop_tips()
```

## Advanced Techniques

### Serial Dilutions

Create serial dilutions across plate rows or columns:

```python
# 2-fold serial dilution
source_vols = [100, 50, 50, 50, 50, 50, 50, 50]
dest_vols = [0, 50, 50, 50, 50, 50, 50, 50]

# Add diluent first
await lh.pick_up_tips(tip_rack["A1"])
await lh.transfer(
    source=buffer["A1"],
    dest=plate["A2:A8"],
    vols=50
)
await lh.drop_tips()

# Perform serial dilution
await lh.pick_up_tips(tip_rack["A2"])
for i in range(7):
    await lh.aspirate(plate[f"A{i+1}"], vols=50)
    await lh.dispense(plate[f"A{i+2}"], vols=50)
    # Mix
    await lh.aspirate(plate[f"A{i+2}"], vols=50)
    await lh.dispense(plate[f"A{i+2}"], vols=50)
await lh.drop_tips()
```

### Plate Replication

Copy an entire plate layout to another plate:

```python
# Setup tips
await lh.pick_up_tips(tip_rack["A1:H1"])

# Replicate 96-well plate (12 columns)
for col in range(1, 13):
    await lh.transfer(
        source=source_plate[f"A{col}:H{col}"],
        dest=dest_plate[f"A{col}:H{col}"],
        vols=100
    )

await lh.drop_tips()
```

### Multi-Channel Pipetting

Use multiple channels simultaneously for parallel operations:

```python
# 8-channel transfer (entire row)
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source=source_plate["A1:H1"],
    dest=dest_plate["A1:H1"],
    vols=100
)
await lh.drop_tips()

# Process entire plate with 8-channel
for col in range(1, 13):
    await lh.pick_up_tips(tip_rack[f"A{col}:H{col}"])
    await lh.transfer(
        source=source_plate[f"A{col}:H{col}"],
        dest=dest_plate[f"A{col}:H{col}"],
        vols=100
    )
    await lh.drop_tips()
```

### Mixing Liquids

Mix liquids by repeatedly aspirating and dispensing:

```python
# Mix by aspiration/dispensing
await lh.pick_up_tips(tip_rack["A1"])

# Mix 5 times
for _ in range(5):
    await lh.aspirate(plate["A1"], vols=80)
    await lh.dispense(plate["A1"], vols=80)

await lh.drop_tips()
```

## Volume Tracking

Track liquid volumes in wells automatically:

```python
from pylabrobot.resources import set_volume_tracking

# Enable volume tracking globally
set_volume_tracking(True)

# Set initial volumes
plate["A1"].tracker.set_liquids([(None, 200)])  # 200 µL

# After aspirating 100 µL
await lh.aspirate(plate["A1"], vols=100)
print(plate["A1"].tracker.get_volume())  # 100 µL

# Check remaining volume
remaining = plate["A1"].tracker.get_volume()
```

## Liquid Classes

Define liquid properties for optimal pipetting:

```python
# Liquid classes control aspiration/dispense parameters
from pylabrobot.liquid_handling import LiquidClass

# Create custom liquid class
water = LiquidClass(
    name="Water",
    aspiration_flow_rate=100,
    dispense_flow_rate=150,
    aspiration_mix_flow_rate=100,
    dispense_mix_flow_rate=100,
    air_transport_retract_dist=10
)

# Use with operations
await lh.aspirate(
    plate["A1"],
    vols=100,
    liquid_class=water
)
```

## Error Handling

Handle errors in liquid handling operations:

```python
try:
    await lh.setup()
    await lh.pick_up_tips(tip_rack["A1"])
    await lh.transfer(source["A1"], dest["A1"], vols=100)
    await lh.drop_tips()
except Exception as e:
    print(f"Error during liquid handling: {e}")
    # Attempt to drop tips if holding them
    try:
        await lh.drop_tips()
    except:
        pass
finally:
    await lh.stop()
```

## Best Practices

1. **Always Setup and Stop**: Call `await lh.setup()` before operations and `await lh.stop()` when done
2. **Enable Tracking**: Use tip tracking and volume tracking for accurate state management
3. **Tip Management**: Always pick up tips before aspirating and drop them when done
4. **Flow Rates**: Adjust flow rates based on liquid viscosity and vessel type
5. **Liquid Height**: Set appropriate aspiration/dispense heights to avoid splashing
6. **Error Handling**: Use try/finally blocks to ensure proper cleanup
7. **Test in Simulation**: Use ChatterboxBackend to test protocols before running on hardware
8. **Volume Limits**: Respect tip volume limits and well capacities
9. **Mixing**: Mix after dispensing viscous liquids or when accuracy is critical
10. **Documentation**: Document liquid classes and custom parameters for reproducibility

## Common Patterns

### Complete Liquid Handling Protocol

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

try:
    # Define resources
    tip_rack = TIP_CAR_480_A00(name="tips")
    source = Cos_96_DW_1mL(name="source")
    dest = Cos_96_DW_1mL(name="dest")

    # Assign to deck
    lh.deck.assign_child_resource(tip_rack, rails=1)
    lh.deck.assign_child_resource(source, rails=10)
    lh.deck.assign_child_resource(dest, rails=15)

    # Set initial volumes
    for well in source.children:
        well.tracker.set_liquids([(None, 200)])

    # Execute protocol
    await lh.pick_up_tips(tip_rack["A1:H1"])
    await lh.transfer(
        source=source["A1:H12"],
        dest=dest["A1:H12"],
        vols=100
    )
    await lh.drop_tips()

finally:
    await lh.stop()
```

## Hardware-Specific Notes

### Hamilton STAR

- Supports full liquid handling capabilities
- Uses USB connection for communication
- Firmware commands executed directly
- Supports CO-RE (Compressed O-Ring Expansion) tips

### Opentrons OT-2

- Requires IP address for network connection
- Uses HTTP API for communication
- Limited to 8-channel and single-channel pipettes
- Simpler deck layout compared to STAR

### Tecan EVO

- Work-in-progress support
- Similar capabilities to Hamilton STAR
- Check current compatibility status in documentation

## Additional Resources

- Official Liquid Handling Guide: https://docs.pylabrobot.org/user_guide/basic.html
- API Reference: https://docs.pylabrobot.org/api/pylabrobot.liquid_handling.html
- Example Protocols: https://github.com/PyLabRobot/pylabrobot/tree/main/examples

---

## Reference: Material Handling

# Material Handling Equipment in PyLabRobot

## Overview

PyLabRobot integrates with material handling equipment including heater shakers, incubators, centrifuges, and pumps. These devices enable environmental control, sample preparation, and automated workflows beyond basic liquid handling.

## Heater Shakers

### Hamilton HeaterShaker

The Hamilton HeaterShaker provides temperature control and orbital shaking for microplates.

#### Setup

```python
from pylabrobot.heating_shaking import HeaterShaker
from pylabrobot.heating_shaking.hamilton import HamiltonHeaterShakerBackend

# Create heater shaker
hs = HeaterShaker(
    name="heater_shaker_1",
    backend=HamiltonHeaterShakerBackend(),
    size_x=156.0,
    size_y=  156.0,
    size_z=18.0
)

await hs.setup()
```

#### Operations

**Temperature Control:**

```python
# Set temperature (Celsius)
await hs.set_temperature(37)

# Get current temperature
temp = await hs.get_temperature()
print(f"Current temperature: {temp}°C")

# Turn off heating
await hs.set_temperature(None)
```

**Shaking Control:**

```python
# Start shaking (RPM)
await hs.set_shake_rate(300)  # 300 RPM

# Stop shaking
await hs.set_shake_rate(0)
```

**Plate Operations:**

```python
# Lock plate in position
await hs.lock_plate()

# Unlock plate
await hs.unlock_plate()
```

#### Integration with Liquid Handler

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Initialize devices
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
hs = HeaterShaker(name="hs", backend=HamiltonHeaterShakerBackend())

await lh.setup()
await hs.setup()

try:
    # Assign heater shaker to deck
    lh.deck.assign_child_resource(hs, rails=8)

    # Prepare samples
    tip_rack = TIP_CAR_480_A00(name="tips")
    plate = Cos_96_DW_1mL(name="plate")

    lh.deck.assign_child_resource(tip_rack, rails=1)

    # Place plate on heater shaker
    hs.assign_child_resource(plate, location=(0, 0, 0))

    # Transfer reagents to plate on heater shaker
    await lh.pick_up_tips(tip_rack["A1:H1"])
    await lh.transfer(reagent["A1:H1"], plate["A1:H1"], vols=100)
    await lh.drop_tips()

    # Lock plate and start incubation
    await hs.lock_plate()
    await hs.set_temperature(37)
    await hs.set_shake_rate(300)

    # Incubate
    import asyncio
    await asyncio.sleep(600)  # 10 minutes

    # Stop shaking and heating
    await hs.set_shake_rate(0)
    await hs.set_temperature(None)
    await hs.unlock_plate()

finally:
    await lh.stop()
    await hs.stop()
```

#### Multiple Heater Shakers

The HamiltonHeaterShakerBackend handles multiple units:

```python
# Backend automatically manages multiple heater shakers
hs1 = HeaterShaker(name="hs1", backend=HamiltonHeaterShakerBackend())
hs2 = HeaterShaker(name="hs2", backend=HamiltonHeaterShakerBackend())

await hs1.setup()
await hs2.setup()

# Assign to different deck positions
lh.deck.assign_child_resource(hs1, rails=8)
lh.deck.assign_child_resource(hs2, rails=12)

# Control independently
await hs1.set_temperature(37)
await hs2.set_temperature(42)
```

### Inheco ThermoShake

The Inheco ThermoShake provides temperature control and shaking.

#### Setup

```python
from pylabrobot.heating_shaking import HeaterShaker
from pylabrobot.heating_shaking.inheco import InhecoThermoShakeBackend

hs = HeaterShaker(
    name="thermoshake",
    backend=InhecoThermoShakeBackend(),
    size_x=156.0,
    size_y=156.0,
    size_z=18.0
)

await hs.setup()
```

#### Operations

Similar to Hamilton HeaterShaker:

```python
# Temperature control
await hs.set_temperature(37)
temp = await hs.get_temperature()

# Shaking control
await hs.set_shake_rate(300)

# Plate locking
await hs.lock_plate()
await hs.unlock_plate()
```

## Incubators

### Inheco Incubators

PyLabRobot supports various Inheco incubator models for temperature-controlled plate storage.

#### Supported Models

- Inheco Single Plate Incubator
- Inheco Multi-Plate Incubators
- Other Inheco temperature controllers

#### Setup

```python
from pylabrobot.temperature_control import TemperatureController
from pylabrobot.temperature_control.inheco import InhecoBackend

# Create incubator
incubator = TemperatureController(
    name="incubator",
    backend=InhecoBackend(),
    size_x=156.0,
    size_y=156.0,
    size_z=50.0
)

await incubator.setup()
```

#### Operations

```python
# Set temperature
await incubator.set_temperature(37)

# Get temperature
temp = await incubator.get_temperature()
print(f"Incubator temperature: {temp}°C")

# Turn off
await incubator.set_temperature(None)
```

### Thermo Fisher Cytomat Incubators

Cytomat incubators provide automated plate storage with temperature and CO2 control.

#### Setup

```python
from pylabrobot.incubation import Incubator
from pylabrobot.incubation.cytomat_backend import CytomatBackend

incubator = Incubator(
    name="cytomat",
    backend=CytomatBackend()
)

await incubator.setup()
```

#### Operations

```python
# Store plate
await incubator.store_plate(plate_id="plate_001", position=1)

# Retrieve plate
await incubator.retrieve_plate(position=1)

# Set environmental conditions
await incubator.set_temperature(37)
await incubator.set_co2(5.0)  # 5% CO2
```

## Centrifuges

### Agilent VSpin

The Agilent VSpin is a vacuum-assisted centrifuge for plate processing.

#### Setup

```python
from pylabrobot.centrifuge import Centrifuge
from pylabrobot.centrifuge.vspin import VSpinBackend

centrifuge = Centrifuge(
    name="vspin",
    backend=VSpinBackend()
)

await centrifuge.setup()
```

#### Operations

**Door Control:**

```python
# Open door
await centrifuge.open_door()

# Close door
await centrifuge.close_door()

# Lock door
await centrifuge.lock_door()

# Unlock door
await centrifuge.unlock_door()
```

**Bucket Positioning:**

```python
# Move bucket to loading position
await centrifuge.move_bucket_to_loading()

# Move bucket to home position
await centrifuge.move_bucket_to_home()
```

**Spinning:**

```python
# Run centrifuge
await centrifuge.spin(
    speed=2000,      # RPM
    duration=300     # seconds
)

# Stop spinning
await centrifuge.stop_spin()
```

#### Integration Example

```python
async def centrifuge_workflow():
    """Complete centrifugation workflow"""

    lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
    centrifuge = Centrifuge(name="vspin", backend=VSpinBackend())

    await lh.setup()
    await centrifuge.setup()

    try:
        # Prepare samples
        await lh.pick_up_tips(tip_rack["A1:H1"])
        await lh.transfer(samples["A1:H12"], plate["A1:H12"], vols=200)
        await lh.drop_tips()

        # Load into centrifuge
        print("Move plate to centrifuge")
        await centrifuge.open_door()
        await centrifuge.move_bucket_to_loading()
        input("Press Enter when plate is loaded...")

        await centrifuge.move_bucket_to_home()
        await centrifuge.close_door()
        await centrifuge.lock_door()

        # Centrifuge
        await centrifuge.spin(speed=2000, duration=300)

        # Unload
        await centrifuge.unlock_door()
        await centrifuge.open_door()
        await centrifuge.move_bucket_to_loading()
        input("Press Enter when plate is removed...")

        await centrifuge.move_bucket_to_home()
        await centrifuge.close_door()

    finally:
        await lh.stop()
        await centrifuge.stop()
```

## Pumps

### Cole Parmer Masterflex

PyLabRobot supports Cole Parmer Masterflex peristaltic pumps for fluid transfer.

#### Setup

```python
from pylabrobot.pumps import Pump
from pylabrobot.pumps.cole_parmer import ColeParmerMasterflexBackend

pump = Pump(
    name="masterflex",
    backend=ColeParmerMasterflexBackend()
)

await pump.setup()
```

#### Operations

**Running Pump:**

```python
# Run for duration
await pump.run_for_duration(
    duration=10,      # seconds
    speed=50          # % of maximum
)

# Run continuously
await pump.start(speed=50)

# Stop pump
await pump.stop()
```

**Volume-Based Pumping:**

```python
# Pump specific volume (requires calibration)
await pump.pump_volume(
    volume=10,        # mL
    speed=50          # % of maximum
)
```

#### Calibration

```python
# Calibrate pump for volume accuracy
# (requires known volume measurement)
await pump.run_for_duration(duration=60, speed=50)
actual_volume = 25.3  # mL measured

pump.calibrate(duration=60, speed=50, volume=actual_volume)
```

### Agrowtek Pump Array

Support for Agrowtek pump arrays for multiple simultaneous fluid transfers.

#### Setup

```python
from pylabrobot.pumps import PumpArray
from pylabrobot.pumps.agrowtek import AgrowtekBackend

pump_array = PumpArray(
    name="agrowtek",
    backend=AgrowtekBackend(),
    num_pumps=8
)

await pump_array.setup()
```

#### Operations

```python
# Run specific pump
await pump_array.run_pump(
    pump_number=1,
    duration=10,
    speed=50
)

# Run multiple pumps simultaneously
await pump_array.run_pumps(
    pump_numbers=[1, 2, 3],
    duration=10,
    speed=50
)
```

## Multi-Device Protocols

### Complex Workflow Example

```python
async def complex_workflow():
    """Multi-device automated workflow"""

    # Initialize all devices
    lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
    hs = HeaterShaker(name="hs", backend=HamiltonHeaterShakerBackend())
    centrifuge = Centrifuge(name="vspin", backend=VSpinBackend())
    pump = Pump(name="pump", backend=ColeParmerMasterflexBackend())

    await lh.setup()
    await hs.setup()
    await centrifuge.setup()
    await pump.setup()

    try:
        # 1. Sample preparation
        await lh.pick_up_tips(tip_rack["A1:H1"])
        await lh.transfer(samples["A1:H12"], plate["A1:H12"], vols=100)
        await lh.drop_tips()

        # 2. Add reagent via pump
        await pump.pump_volume(volume=50, speed=50)

        # 3. Mix on heater shaker
        await hs.lock_plate()
        await hs.set_temperature(37)
        await hs.set_shake_rate(300)
        await asyncio.sleep(600)  # 10 min incubation
        await hs.set_shake_rate(0)
        await hs.set_temperature(None)
        await hs.unlock_plate()

        # 4. Centrifuge
        await centrifuge.open_door()
        # (load plate)
        await centrifuge.close_door()
        await centrifuge.spin(speed=2000, duration=180)
        await centrifuge.open_door()
        # (unload plate)

        # 5. Transfer supernatant
        await lh.pick_up_tips(tip_rack["A2:H2"])
        await lh.transfer(
            plate["A1:H12"],
            output_plate["A1:H12"],
            vols=80
        )
        await lh.drop_tips()

    finally:
        await lh.stop()
        await hs.stop()
        await centrifuge.stop()
        await pump.stop()
```

## Best Practices

1. **Device Initialization**: Setup all devices at protocol start
2. **Sequential Operations**: Material handling often requires sequential steps
3. **Safety**: Always unlock/open doors before manual plate handling
4. **Temperature Equilibration**: Allow time for devices to reach temperature
5. **Error Handling**: Handle device errors gracefully with try/finally
6. **State Verification**: Check device state before operations
7. **Timing**: Account for device-specific delays (heating, centrifugation)
8. **Maintenance**: Follow manufacturer maintenance schedules
9. **Calibration**: Regularly calibrate pumps and temperature controllers
10. **Documentation**: Record all device settings and parameters

## Common Patterns

### Temperature-Controlled Incubation

```python
async def incubate_with_shaking(
    plate,
    temperature: float,
    shake_rate: int,
    duration: int
):
    """Incubate plate with temperature and shaking"""

    hs = HeaterShaker(name="hs", backend=HamiltonHeaterShakerBackend())
    await hs.setup()

    try:
        # Assign plate to heater shaker
        hs.assign_child_resource(plate, location=(0, 0, 0))

        # Start incubation
        await hs.lock_plate()
        await hs.set_temperature(temperature)
        await hs.set_shake_rate(shake_rate)

        # Wait
        await asyncio.sleep(duration)

        # Stop
        await hs.set_shake_rate(0)
        await hs.set_temperature(None)
        await hs.unlock_plate()

    finally:
        await hs.stop()

# Use in protocol
await incubate_with_shaking(
    plate=assay_plate,
    temperature=37,
    shake_rate=300,
    duration=600  # 10 minutes
)
```

### Automated Plate Processing

```python
async def process_plates(plate_list: list):
    """Process multiple plates through workflow"""

    lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
    hs = HeaterShaker(name="hs", backend=HamiltonHeaterShakerBackend())

    await lh.setup()
    await hs.setup()

    try:
        for i, plate in enumerate(plate_list):
            print(f"Processing plate {i+1}/{len(plate_list)}")

            # Transfer samples
            await lh.pick_up_tips(tip_rack[f"A{i+1}:H{i+1}"])
            await lh.transfer(
                source[f"A{i+1}:H{i+1}"],
                plate["A1:H1"],
                vols=100
            )
            await lh.drop_tips()

            # Incubate
            hs.assign_child_resource(plate, location=(0, 0, 0))
            await hs.lock_plate()
            await hs.set_temperature(37)
            await hs.set_shake_rate(300)
            await asyncio.sleep(300)  # 5 min
            await hs.set_shake_rate(0)
            await hs.set_temperature(None)
            await hs.unlock_plate()
            hs.unassign_child_resource(plate)

    finally:
        await lh.stop()
        await hs.stop()
```

## Additional Resources

- Material Handling Documentation: https://docs.pylabrobot.org/user_guide/01_material-handling/
- Heater Shakers: https://docs.pylabrobot.org/user_guide/01_material-handling/heating_shaking/
- API Reference: https://docs.pylabrobot.org/api/
- Supported Equipment: https://docs.pylabrobot.org/user_guide/machines.html

---

## Reference: Resources

# Resource Management in PyLabRobot

## Overview

Resources in PyLabRobot represent laboratory equipment, labware, or components used in protocols. The resource system provides a hierarchical structure for managing plates, tip racks, troughs, tubes, carriers, and other labware with precise spatial positioning and state tracking.

## Resource Basics

### What is a Resource?

A resource represents:
- A piece of labware (plate, tip rack, trough, tube)
- Equipment (liquid handler, plate reader)
- A part of labware (well, tip)
- A container of labware (deck, carrier)

All resources inherit from the base `Resource` class and form a tree structure (arborescence) with parent-child relationships.

### Resource Attributes

Every resource requires:
- **name**: Unique identifier for the resource
- **size_x, size_y, size_z**: Dimensions in millimeters (cuboid representation)
- **location**: Coordinate relative to parent's origin (optional, set when assigned)

```python
from pylabrobot.resources import Resource

# Create a basic resource
resource = Resource(
    name="my_resource",
    size_x=127.76,  # mm
    size_y=85.48,   # mm
    size_z=14.5     # mm
)
```

## Resource Types

### Plates

Microplates with wells for holding liquids:

```python
from pylabrobot.resources import (
    Cos_96_DW_1mL,      # 96-well plate, 1mL deep well
    Cos_96_DW_500ul,    # 96-well plate, 500µL
    Plate_384_Sq,       # 384-well square plate
    Cos_96_PCR          # 96-well PCR plate
)

# Create plate
plate = Cos_96_DW_1mL(name="sample_plate")

# Access wells
well_a1 = plate["A1"]                  # Single well
row_a = plate["A1:H1"]                 # Entire row (A1-H1)
col_1 = plate["A1:A12"]                # Entire column (A1-A12)
range_wells = plate["A1:C3"]           # Range of wells
all_wells = plate.children             # All wells as list
```

### Tip Racks

Containers holding pipette tips:

```python
from pylabrobot.resources import (
    TIP_CAR_480_A00,    # 96 standard tips
    HTF_L,              # Hamilton tips, filtered
    TipRack             # Generic tip rack
)

# Create tip rack
tip_rack = TIP_CAR_480_A00(name="tips")

# Access tips
tip_a1 = tip_rack["A1"]                # Single tip position
tips_row = tip_rack["A1:H1"]           # Row of tips
tips_col = tip_rack["A1:A12"]          # Column of tips

# Check tip presence (requires tip tracking enabled)
from pylabrobot.resources import set_tip_tracking
set_tip_tracking(True)

has_tip = tip_rack["A1"].tracker.has_tip
```

### Troughs

Reservoir containers for reagents:

```python
from pylabrobot.resources import Trough_100ml

# Create trough
trough = Trough_100ml(name="buffer")

# Access channels
channel_1 = trough["channel_1"]
all_channels = trough.children
```

### Tubes

Individual tubes or tube racks:

```python
from pylabrobot.resources import Tube, TubeRack

# Create tube rack
tube_rack = TubeRack(name="samples")

# Access tubes
tube_a1 = tube_rack["A1"]
```

### Carriers

Platforms that hold plates, tips, or other labware:

```python
from pylabrobot.resources import (
    PlateCarrier,
    TipCarrier,
    MFXCarrier
)

# Carriers provide positions for labware
carrier = PlateCarrier(name="plate_carrier")

# Assign plate to carrier
plate = Cos_96_DW_1mL(name="plate")
carrier.assign_child_resource(plate, location=(0, 0, 0))
```

## Deck Management

### Working with Decks

The deck represents the robot's work surface:

```python
from pylabrobot.resources import STARLetDeck, OTDeck

# Hamilton STARlet deck
deck = STARLetDeck()

# Opentrons OT-2 deck
deck = OTDeck()
```

### Assigning Resources to Deck

Resources are assigned to specific deck positions using rails or coordinates:

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.resources import STARLetDeck, TIP_CAR_480_A00, Cos_96_DW_1mL

lh = LiquidHandler(backend=backend, deck=STARLetDeck())

# Assign using rail positions (Hamilton STAR)
tip_rack = TIP_CAR_480_A00(name="tips")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Assign using coordinates (x, y, z in mm)
lh.deck.assign_child_resource(
    resource=tip_rack,
    location=(100, 200, 0)
)
```

### Unassigning Resources

Remove resources from deck:

```python
# Unassign specific resource
lh.deck.unassign_child_resource(tip_rack)

# Access assigned resources
all_resources = lh.deck.children
resource_names = [r.name for r in lh.deck.children]
```

## Coordinate System

PyLabRobot uses a right-handed Cartesian coordinate system:

- **X-axis**: Left to right (increasing rightward)
- **Y-axis**: Front to back (increasing toward back)
- **Z-axis**: Down to up (increasing upward)
- **Origin**: Bottom-front-left corner of parent

### Location Calculations

```python
# Get absolute location (relative to deck/root)
absolute_loc = plate.get_absolute_location()

# Get location relative to another resource
relative_loc = well.get_location_wrt(deck)

# Get location relative to parent
parent_relative = plate.location
```

## State Management

### Tracking Liquid Volumes

Track liquid volumes in wells and containers:

```python
from pylabrobot.resources import set_volume_tracking

# Enable volume tracking globally
set_volume_tracking(True)

# Set liquid in well
plate["A1"].tracker.set_liquids([
    (None, 200)  # (liquid_type, volume_in_uL)
])

# Multiple liquids
plate["A2"].tracker.set_liquids([
    ("water", 100),
    ("ethanol", 50)
])

# Get current volume
volume = plate["A1"].tracker.get_volume()  # Returns total volume

# Get liquids
liquids = plate["A1"].tracker.get_liquids()  # Returns list of (type, vol) tuples
```

### Tracking Tip Presence

Track which tips are present in tip racks:

```python
from pylabrobot.resources import set_tip_tracking

# Enable tip tracking globally
set_tip_tracking(True)

# Check if tip is present
has_tip = tip_rack["A1"].tracker.has_tip

# Tips are automatically tracked when using pick_up_tips/drop_tips
await lh.pick_up_tips(tip_rack["A1"])  # Marks tip as absent
await lh.return_tips()                  # Marks tip as present
```

## Serialization

### Saving and Loading Resources

Save resource definitions and states to JSON:

```python
# Save resource definition
plate.save("plate_definition.json")

# Load resource from JSON
from pylabrobot.resources import Plate
plate = Plate.load_from_json_file("plate_definition.json")

# Save deck layout
lh.deck.save("deck_layout.json")

# Load deck layout
from pylabrobot.resources import Deck
deck = Deck.load_from_json_file("deck_layout.json")
```

### State Serialization

Save and restore resource states separately from definitions:

```python
# Save state (tip presence, liquid volumes)
state = plate.serialize_state()
with open("plate_state.json", "w") as f:
    json.dump(state, f)

# Load state
with open("plate_state.json", "r") as f:
    state = json.load(f)
plate.load_state(state)

# Save all states in hierarchy
all_states = lh.deck.serialize_all_state()

# Load all states
lh.deck.load_all_state(all_states)
```

## Custom Resources

### Defining Custom Labware

Create custom labware when built-in resources don't match your equipment:

```python
from pylabrobot.resources import Plate, Well

# Define custom plate
class CustomPlate(Plate):
    def __init__(self, name: str):
        super().__init__(
            name=name,
            size_x=127.76,
            size_y=85.48,
            size_z=14.5,
            num_items_x=12,  # 12 columns
            num_items_y=8,   # 8 rows
            dx=9.0,          # Well spacing X
            dy=9.0,          # Well spacing Y
            dz=0.0,          # Well spacing Z (usually 0)
            item_dx=9.0,     # Distance between well centers X
            item_dy=9.0      # Distance between well centers Y
        )

# Use custom plate
custom_plate = CustomPlate(name="my_custom_plate")
```

### Custom Wells

Define custom well geometry:

```python
from pylabrobot.resources import Well

# Create custom well
well = Well(
    name="custom_well",
    size_x=8.0,
    size_y=8.0,
    size_z=10.5,
    max_volume=200,      # µL
    bottom_shape="flat"  # or "v", "u"
)
```

## Resource Discovery

### Finding Resources

Navigate the resource hierarchy:

```python
# Get all wells in a plate
wells = plate.children

# Find resource by name
resource = lh.deck.get_resource("plate_name")

# Iterate through resources
for resource in lh.deck.children:
    print(f"{resource.name}: {resource.get_absolute_location()}")

# Get wells by pattern
wells_a = [w for w in plate.children if w.name.startswith("A")]
```

### Resource Metadata

Access resource information:

```python
# Resource properties
print(f"Name: {plate.name}")
print(f"Size: {plate.size_x} x {plate.size_y} x {plate.size_z} mm")
print(f"Location: {plate.get_absolute_location()}")
print(f"Parent: {plate.parent.name if plate.parent else None}")
print(f"Children: {len(plate.children)}")

# Type checking
from pylabrobot.resources import Plate, TipRack
if isinstance(resource, Plate):
    print("This is a plate")
elif isinstance(resource, TipRack):
    print("This is a tip rack")
```

## Best Practices

1. **Unique Names**: Use descriptive, unique names for all resources
2. **Enable Tracking**: Turn on tip and volume tracking for accurate state management
3. **Coordinate Validation**: Verify resource positions don't overlap on deck
4. **State Serialization**: Save deck layouts and states for reproducible protocols
5. **Resource Cleanup**: Unassign resources when no longer needed
6. **Custom Resources**: Define custom labware when built-in options don't match
7. **Documentation**: Document custom resource dimensions and properties
8. **Type Checking**: Use isinstance() to verify resource types before operations
9. **Hierarchy Navigation**: Use parent/children relationships to navigate resource tree
10. **JSON Storage**: Store deck layouts in JSON for version control and sharing

## Common Patterns

### Complete Deck Setup

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import (
    STARLetDeck,
    TIP_CAR_480_A00,
    Cos_96_DW_1mL,
    Trough_100ml,
    set_tip_tracking,
    set_volume_tracking
)

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Initialize liquid handler
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Define resources
tip_rack_1 = TIP_CAR_480_A00(name="tips_1")
tip_rack_2 = TIP_CAR_480_A00(name="tips_2")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")
buffer = Trough_100ml(name="buffer")

# Assign to deck
lh.deck.assign_child_resource(tip_rack_1, rails=1)
lh.deck.assign_child_resource(tip_rack_2, rails=2)
lh.deck.assign_child_resource(buffer, rails=5)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Set initial volumes
for well in source_plate.children:
    well.tracker.set_liquids([(None, 200)])

buffer["channel_1"].tracker.set_liquids([(None, 50000)])  # 50 mL

# Save deck layout
lh.deck.save("my_protocol_deck.json")

# Save initial state
import json
with open("initial_state.json", "w") as f:
    json.dump(lh.deck.serialize_all_state(), f)
```

### Loading Saved Deck

```python
from pylabrobot.resources import Deck

# Load deck from file
deck = Deck.load_from_json_file("my_protocol_deck.json")

# Load state
import json
with open("initial_state.json", "r") as f:
    state = json.load(f)
deck.load_all_state(state)

# Use with liquid handler
lh = LiquidHandler(backend=STAR(), deck=deck)
await lh.setup()

# Access resources by name
source_plate = deck.get_resource("source")
dest_plate = deck.get_resource("dest")
```

## Additional Resources

- Resource Documentation: https://docs.pylabrobot.org/resources/introduction.html
- Custom Resources Guide: https://docs.pylabrobot.org/resources/custom-resources.html
- API Reference: https://docs.pylabrobot.org/api/pylabrobot.resources.html
- Deck Layouts: https://github.com/PyLabRobot/pylabrobot/tree/main/pylabrobot/resources/deck

---

## Reference: Visualization

# Visualization & Simulation in PyLabRobot

## Overview

PyLabRobot provides visualization and simulation tools for developing, testing, and validating laboratory protocols without physical hardware. The visualizer offers real-time 3D visualization of deck state, while simulation backends enable protocol testing and validation.

## The Visualizer

### What is the Visualizer?

The PyLabRobot Visualizer is a browser-based tool that:
- Displays 3D visualization of the deck layout
- Shows real-time tip presence and liquid volumes
- Works with both simulated and physical robots
- Provides interactive deck state inspection
- Enables visual protocol validation

### Starting the Visualizer

The visualizer runs as a web server and displays in your browser:

```python
from pylabrobot.visualizer import Visualizer

# Create visualizer
vis = Visualizer()

# Start web server (opens browser automatically)
await vis.start()

# Stop visualizer
await vis.stop()
```

**Default Settings:**
- Port: 1234 (http://localhost:1234)
- Opens browser automatically when started

### Connecting Liquid Handler to Visualizer

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import STARLetDeck
from pylabrobot.visualizer import Visualizer

# Create visualizer
vis = Visualizer()
await vis.start()

# Create liquid handler with simulation backend
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)

# Connect liquid handler to visualizer
lh.visualizer = vis

await lh.setup()

# Now all operations are visualized in real-time
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1:H1"], vols=100)
await lh.dispense(plate["A2:H2"], vols=100)
await lh.drop_tips()
```

### Tracking Features

#### Enable Tracking

For the visualizer to display tips and liquids, enable tracking:

```python
from pylabrobot.resources import set_tip_tracking, set_volume_tracking

# Enable globally (before creating resources)
set_tip_tracking(True)
set_volume_tracking(True)
```

#### Setting Initial Liquids

Define initial liquid contents for visualization:

```python
# Set liquid in a single well
plate["A1"].tracker.set_liquids([
    (None, 200)  # (liquid_type, volume_in_µL)
])

# Set multiple liquids in one well
plate["A2"].tracker.set_liquids([
    ("water", 100),
    ("ethanol", 50)
])

# Set liquids in multiple wells
for well in plate["A1:H1"]:
    well.tracker.set_liquids([(None, 200)])

# Set liquids in entire plate
for well in plate.children:
    well.tracker.set_liquids([("sample", 150)])
```

#### Visualizing Tip Presence

```python
# Tips are automatically tracked when using pick_up/drop operations
await lh.pick_up_tips(tip_rack["A1:H1"])  # Tips shown as absent in visualizer
await lh.return_tips()                     # Tips shown as present in visualizer
```

### Complete Visualizer Example

```python
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
from pylabrobot.resources import (
    STARLetDeck,
    TIP_CAR_480_A00,
    Cos_96_DW_1mL,
    set_tip_tracking,
    set_volume_tracking
)
from pylabrobot.visualizer import Visualizer

# Enable tracking
set_tip_tracking(True)
set_volume_tracking(True)

# Create visualizer
vis = Visualizer()
await vis.start()

# Create liquid handler
lh = LiquidHandler(
    backend=ChatterboxBackend(num_channels=8),
    deck=STARLetDeck()
)
lh.visualizer = vis
await lh.setup()

# Define resources
tip_rack = TIP_CAR_480_A00(name="tips")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

# Assign to deck
lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Set initial volumes
for well in source_plate.children:
    well.tracker.set_liquids([("sample", 200)])

# Execute protocol with visualization
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(
    source_plate["A1:H12"],
    dest_plate["A1:H12"],
    vols=100
)
await lh.drop_tips()

# Keep visualizer open to inspect final state
input("Press Enter to close visualizer...")

# Cleanup
await lh.stop()
await vis.stop()
```

## Deck Layout Editor

### Using the Deck Editor

PyLabRobot includes a graphical deck layout editor:

**Features:**
- Visual deck design interface
- Drag-and-drop resource placement
- Edit initial liquid states
- Set tip presence
- Save/load layouts as JSON

**Usage:**
- Accessed through the visualizer interface
- Create layouts graphically instead of code
- Export to JSON for use in protocols

### Loading Deck Layouts

```python
from pylabrobot.resources import Deck

# Load deck from JSON file
deck = Deck.load_from_json_file("my_deck_layout.json")

# Use with liquid handler
lh = LiquidHandler(backend=backend, deck=deck)
await lh.setup()

# Resources are already assigned
source = deck.get_resource("source")
dest = deck.get_resource("dest")
tip_rack = deck.get_resource("tips")
```

## Simulation

### ChatterboxBackend

The ChatterboxBackend simulates liquid handling operations:

**Features:**
- No hardware required
- Validates protocol logic
- Tracks tips and volumes
- Supports all liquid handling operations
- Works with visualizer

**Setup:**

```python
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend

# Create simulation backend
backend = ChatterboxBackend(
    num_channels=8  # Simulate 8-channel pipette
)

# Use with liquid handler
lh = LiquidHandler(backend=backend, deck=STARLetDeck())
```

### Simulation Use Cases

#### Protocol Development

```python
async def develop_protocol():
    """Develop protocol using simulation"""

    # Use simulation for development
    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )

    # Connect visualizer
    vis = Visualizer()
    await vis.start()
    lh.visualizer = vis

    await lh.setup()

    try:
        # Develop and test protocol
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        print("Protocol development complete!")

    finally:
        await lh.stop()
        await vis.stop()
```

#### Protocol Validation

```python
async def validate_protocol():
    """Validate protocol logic without hardware"""

    set_tip_tracking(True)
    set_volume_tracking(True)

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Setup resources
        tip_rack = TIP_CAR_480_A00(name="tips")
        plate = Cos_96_DW_1mL(name="plate")

        lh.deck.assign_child_resource(tip_rack, rails=1)
        lh.deck.assign_child_resource(plate, rails=10)

        # Set initial state
        for well in plate.children:
            well.tracker.set_liquids([(None, 200)])

        # Execute protocol
        await lh.pick_up_tips(tip_rack["A1:H1"])

        # Test different volumes
        test_volumes = [50, 100, 150]
        for i, vol in enumerate(test_volumes):
            await lh.transfer(
                plate[f"A{i+1}:H{i+1}"],
                plate[f"A{i+4}:H{i+4}"],
                vols=vol
            )

        await lh.drop_tips()

        # Validate volumes
        for i, vol in enumerate(test_volumes):
            for row in "ABCDEFGH":
                well = plate[f"{row}{i+4}"]
                actual_vol = well.tracker.get_volume()
                assert actual_vol == vol, f"Volume mismatch in {well.name}"

        print("✓ Protocol validation passed!")

    finally:
        await lh.stop()
```

#### Testing Edge Cases

```python
async def test_edge_cases():
    """Test protocol edge cases in simulation"""

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Test 1: Empty well aspiration
        try:
            await lh.aspirate(empty_plate["A1"], vols=100)
            print("✗ Should have raised error for empty well")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

        # Test 2: Overfilling well
        try:
            await lh.dispense(small_well, vols=1000)  # Too much
            print("✗ Should have raised error for overfilling")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

        # Test 3: Tip capacity
        try:
            await lh.aspirate(large_volume_well, vols=2000)  # Exceeds tip capacity
            print("✗ Should have raised error for tip capacity")
        except Exception as e:
            print(f"✓ Correctly raised error: {e}")

    finally:
        await lh.stop()
```

### CI/CD Integration

Use simulation for automated testing:

```python
# test_protocols.py
import pytest
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend

@pytest.mark.asyncio
async def test_transfer_protocol():
    """Test liquid transfer protocol"""

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    await lh.setup()

    try:
        # Setup
        tip_rack = TIP_CAR_480_A00(name="tips")
        plate = Cos_96_DW_1mL(name="plate")

        lh.deck.assign_child_resource(tip_rack, rails=1)
        lh.deck.assign_child_resource(plate, rails=10)

        # Set initial volumes
        plate["A1"].tracker.set_liquids([(None, 200)])

        # Execute
        await lh.pick_up_tips(tip_rack["A1"])
        await lh.transfer(plate["A1"], plate["A2"], vols=100)
        await lh.drop_tips()

        # Assert
        assert plate["A1"].tracker.get_volume() == 100
        assert plate["A2"].tracker.get_volume() == 100

    finally:
        await lh.stop()
```

## Best Practices

1. **Always Use Simulation First**: Develop and test protocols in simulation before running on hardware
2. **Enable Tracking**: Turn on tip and volume tracking for accurate visualization
3. **Set Initial States**: Define initial liquid volumes for realistic simulation
4. **Visual Inspection**: Use visualizer to verify deck layout and protocol execution
5. **Validate Logic**: Test edge cases and error conditions in simulation
6. **Automated Testing**: Integrate simulation into CI/CD pipelines
7. **Save Layouts**: Use JSON to save and share deck layouts
8. **Document States**: Record initial states for reproducibility
9. **Interactive Development**: Keep visualizer open during development
10. **Protocol Refinement**: Iterate in simulation before hardware runs

## Common Patterns

### Development to Production Workflow

```python
import os

# Configuration
USE_HARDWARE = os.getenv("USE_HARDWARE", "false").lower() == "true"

# Create appropriate backend
if USE_HARDWARE:
    from pylabrobot.liquid_handling.backends import STAR
    backend = STAR()
    print("Running on Hamilton STAR hardware")
else:
    from pylabrobot.liquid_handling.backends.simulation import ChatterboxBackend
    backend = ChatterboxBackend()
    print("Running in simulation mode")

# Rest of protocol is identical
lh = LiquidHandler(backend=backend, deck=STARLetDeck())

if not USE_HARDWARE:
    # Enable visualizer for simulation
    vis = Visualizer()
    await vis.start()
    lh.visualizer = vis

await lh.setup()

# Protocol execution
# ... (same code for hardware and simulation)

# Run with: USE_HARDWARE=false python protocol.py  # Simulation
# Run with: USE_HARDWARE=true python protocol.py   # Hardware
```

### Visual Protocol Verification

```python
async def visual_verification():
    """Run protocol with visual verification pauses"""

    vis = Visualizer()
    await vis.start()

    lh = LiquidHandler(
        backend=ChatterboxBackend(),
        deck=STARLetDeck()
    )
    lh.visualizer = vis
    await lh.setup()

    try:
        # Step 1
        await lh.pick_up_tips(tip_rack["A1:H1"])
        input("Press Enter to continue...")

        # Step 2
        await lh.aspirate(source["A1:H1"], vols=100)
        input("Press Enter to continue...")

        # Step 3
        await lh.dispense(dest["A1:H1"], vols=100)
        input("Press Enter to continue...")

        # Step 4
        await lh.drop_tips()
        input("Press Enter to finish...")

    finally:
        await lh.stop()
        await vis.stop()
```

## Troubleshooting

### Visualizer Not Updating

- Ensure `lh.visualizer = vis` is set before operations
- Check that tracking is enabled globally
- Verify visualizer is running (`vis.start()`)
- Refresh browser if connection is lost

### Tracking Not Working

```python
# Must enable tracking BEFORE creating resources
set_tip_tracking(True)
set_volume_tracking(True)

# Then create resources
tip_rack = TIP_CAR_480_A00(name="tips")
plate = Cos_96_DW_1mL(name="plate")
```

### Simulation Errors

- Simulation validates operations (e.g., can't aspirate from empty well)
- Use try/except to handle validation errors
- Check initial states are set correctly
- Verify volumes don't exceed capacities

## Additional Resources

- Visualizer Documentation: https://docs.pylabrobot.org/user_guide/using-the-visualizer.html (if available)
- Simulation Guide: https://docs.pylabrobot.org/user_guide/simulation.html (if available)
- API Reference: https://docs.pylabrobot.org/api/pylabrobot.visualizer.html
- GitHub Examples: https://github.com/PyLabRobot/pylabrobot/tree/main/examples
