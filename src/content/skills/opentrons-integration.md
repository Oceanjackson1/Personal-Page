---
title: "Opentrons Integration"
description: "Official Opentrons Protocol API for OT-2 and Flex robots. Use when writing protocols specifically for Opentrons hardware with full access to Protocol API v2 features. Best for production Opentrons protocols, official API compatibility. For multi-v..."
category: "writing"
source: "community"
author: "Community"
tags: ["opentrons", "integration"]
date: 2026-03-20
---

# Opentrons Integration

## Overview

Opentrons is a Python-based lab automation platform for Flex and OT-2 robots. Write Protocol API v2 protocols for liquid handling, control hardware modules (heater-shaker, thermocycler), manage labware, for automated pipetting workflows.

## When to Use This Skill

This skill should be used when:
- Writing Opentrons Protocol API v2 protocols in Python
- Automating liquid handling workflows on Flex or OT-2 robots
- Controlling hardware modules (temperature, magnetic, heater-shaker, thermocycler)
- Setting up labware configurations and deck layouts
- Implementing complex pipetting operations (serial dilutions, plate replication, PCR setup)
- Managing tip usage and optimizing protocol efficiency
- Working with multi-channel pipettes for 96-well plate operations
- Simulating and testing protocols before robot execution

## Core Capabilities

### 1. Protocol Structure and Metadata

Every Opentrons protocol follows a standard structure:

```python
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # Use latest available API version
}

# Requirements (optional)
requirements = {
    'robotType': 'Flex',  # or 'OT-2'
    'apiLevel': '2.19'
}

# Run function
def run(protocol: protocol_api.ProtocolContext):
    # Protocol commands go here
    pass
```

**Key elements:**
- Import `protocol_api` from `opentrons`
- Define `metadata` dict with protocolName, author, description, apiLevel
- Optional `requirements` dict for robot type and API version
- Implement `run()` function receiving `ProtocolContext` as parameter
- All protocol logic goes inside the `run()` function

### 2. Loading Hardware

**Loading Instruments (Pipettes):**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load pipette on specific mount
    left_pipette = protocol.load_instrument(
        'p1000_single_flex',  # Instrument name
        'left',               # Mount: 'left' or 'right'
        tip_racks=[tip_rack]  # List of tip rack labware objects
    )
```

Common pipette names:
- Flex: `p50_single_flex`, `p1000_single_flex`, `p50_multi_flex`, `p1000_multi_flex`
- OT-2: `p20_single_gen2`, `p300_single_gen2`, `p1000_single_gen2`, `p20_multi_gen2`, `p300_multi_gen2`

**Loading Labware:**

```python
# Load labware directly on deck
plate = protocol.load_labware(
    'corning_96_wellplate_360ul_flat',  # Labware API name
    'D1',                                # Deck slot (Flex: A1-D3, OT-2: 1-11)
    label='Sample Plate'                 # Optional display label
)

# Load tip rack
tip_rack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')

# Load labware on adapter
adapter = protocol.load_adapter('opentrons_flex_96_tiprack_adapter', 'B1')
tips = adapter.load_labware('opentrons_flex_96_tiprack_200ul')
```

**Loading Modules:**

```python
# Temperature module
temp_module = protocol.load_module('temperature module gen2', 'D3')
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# Magnetic module
mag_module = protocol.load_module('magnetic module gen2', 'C2')
mag_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Heater-Shaker module
hs_module = protocol.load_module('heaterShakerModuleV1', 'D1')
hs_plate = hs_module.load_labware('corning_96_wellplate_360ul_flat')

# Thermocycler module (takes up specific slots automatically)
tc_module = protocol.load_module('thermocyclerModuleV2')
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
```

### 3. Liquid Handling Operations

**Basic Operations:**

```python
# Pick up tip
pipette.pick_up_tip()

# Aspirate (draw liquid in)
pipette.aspirate(
    volume=100,           # Volume in µL
    location=source['A1'] # Well or location object
)

# Dispense (expel liquid)
pipette.dispense(
    volume=100,
    location=dest['B1']
)

# Drop tip
pipette.drop_tip()

# Return tip to rack
pipette.return_tip()
```

**Complex Operations:**

```python
# Transfer (combines pick_up, aspirate, dispense, drop_tip)
pipette.transfer(
    volume=100,
    source=source_plate['A1'],
    dest=dest_plate['B1'],
    new_tip='always'  # 'always', 'once', or 'never'
)

# Distribute (one source to multiple destinations)
pipette.distribute(
    volume=50,
    source=reservoir['A1'],
    dest=[plate['A1'], plate['A2'], plate['A3']],
    new_tip='once'
)

# Consolidate (multiple sources to one destination)
pipette.consolidate(
    volume=50,
    source=[plate['A1'], plate['A2'], plate['A3']],
    dest=reservoir['A1'],
    new_tip='once'
)
```

**Advanced Techniques:**

```python
# Mix (aspirate and dispense in same location)
pipette.mix(
    repetitions=3,
    volume=50,
    location=plate['A1']
)

# Air gap (prevent dripping)
pipette.aspirate(100, source['A1'])
pipette.air_gap(20)  # 20µL air gap
pipette.dispense(120, dest['A1'])

# Blow out (expel remaining liquid)
pipette.blow_out(location=dest['A1'].top())

# Touch tip (remove droplets on tip exterior)
pipette.touch_tip(location=plate['A1'])
```

**Flow Rate Control:**

```python
# Set flow rates (µL/s)
pipette.flow_rate.aspirate = 150
pipette.flow_rate.dispense = 300
pipette.flow_rate.blow_out = 400
```

### 4. Accessing Wells and Locations

**Well Access Methods:**

```python
# By name
well_a1 = plate['A1']

# By index
first_well = plate.wells()[0]

# All wells
all_wells = plate.wells()  # Returns list

# By rows
rows = plate.rows()  # Returns list of lists
row_a = plate.rows()[0]  # All wells in row A

# By columns
columns = plate.columns()  # Returns list of lists
column_1 = plate.columns()[0]  # All wells in column 1

# Wells by name (dictionary)
wells_dict = plate.wells_by_name()  # {'A1': Well, 'A2': Well, ...}
```

**Location Methods:**

```python
# Top of well (default: 1mm below top)
pipette.aspirate(100, well.top())
pipette.aspirate(100, well.top(z=5))  # 5mm above top

# Bottom of well (default: 1mm above bottom)
pipette.aspirate(100, well.bottom())
pipette.aspirate(100, well.bottom(z=2))  # 2mm above bottom

# Center of well
pipette.aspirate(100, well.center())
```

### 5. Hardware Module Control

**Temperature Module:**

```python
# Set temperature
temp_module.set_temperature(celsius=4)

# Wait for temperature
temp_module.await_temperature(celsius=4)

# Deactivate
temp_module.deactivate()

# Check status
current_temp = temp_module.temperature  # Current temperature
target_temp = temp_module.target  # Target temperature
```

**Magnetic Module:**

```python
# Engage (raise magnets)
mag_module.engage(height_from_base=10)  # mm from labware base

# Disengage (lower magnets)
mag_module.disengage()

# Check status
is_engaged = mag_module.status  # 'engaged' or 'disengaged'
```

**Heater-Shaker Module:**

```python
# Set temperature
hs_module.set_target_temperature(celsius=37)

# Wait for temperature
hs_module.wait_for_temperature()

# Set shake speed
hs_module.set_and_wait_for_shake_speed(rpm=500)

# Close labware latch
hs_module.close_labware_latch()

# Open labware latch
hs_module.open_labware_latch()

# Deactivate heater
hs_module.deactivate_heater()

# Deactivate shaker
hs_module.deactivate_shaker()
```

**Thermocycler Module:**

```python
# Open lid
tc_module.open_lid()

# Close lid
tc_module.close_lid()

# Set lid temperature
tc_module.set_lid_temperature(celsius=105)

# Set block temperature
tc_module.set_block_temperature(
    temperature=95,
    hold_time_seconds=30,
    hold_time_minutes=0.5,
    block_max_volume=50  # µL per well
)

# Execute profile (PCR cycling)
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 57, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(
    steps=profile,
    repetitions=30,
    block_max_volume=50
)

# Deactivate
tc_module.deactivate_lid()
tc_module.deactivate_block()
```

**Absorbance Plate Reader:**

```python
# Initialize and read
result = plate_reader.read(wavelengths=[450, 650])

# Access readings
absorbance_data = result  # Dict with wavelength keys
```

### 6. Liquid Tracking and Labeling

**Define Liquids:**

```python
# Define liquid types
water = protocol.define_liquid(
    name='Water',
    description='Ultrapure water',
    display_color='#0000FF'  # Hex color code
)

sample = protocol.define_liquid(
    name='Sample',
    description='Cell lysate sample',
    display_color='#FF0000'
)
```

**Load Liquids into Wells:**

```python
# Load liquid into specific wells
reservoir['A1'].load_liquid(liquid=water, volume=50000)  # µL
plate['A1'].load_liquid(liquid=sample, volume=100)

# Mark wells as empty
plate['B1'].load_empty()
```

### 7. Protocol Control and Utilities

**Execution Control:**

```python
# Pause protocol
protocol.pause(msg='Replace tip box and resume')

# Delay
protocol.delay(seconds=60)
protocol.delay(minutes=5)

# Comment (appears in logs)
protocol.comment('Starting serial dilution')

# Home robot
protocol.home()
```

**Conditional Logic:**

```python
# Check if simulating
if protocol.is_simulating():
    protocol.comment('Running in simulation mode')
else:
    protocol.comment('Running on actual robot')
```

**Rail Lights (Flex only):**

```python
# Turn lights on
protocol.set_rail_lights(on=True)

# Turn lights off
protocol.set_rail_lights(on=False)
```

### 8. Multi-Channel and 8-Channel Pipetting

When using multi-channel pipettes:

```python
# Load 8-channel pipette
multi_pipette = protocol.load_instrument(
    'p300_multi_gen2',
    'left',
    tip_racks=[tips]
)

# Access entire column with single well reference
multi_pipette.transfer(
    volume=100,
    source=source_plate['A1'],  # Accesses entire column 1
    dest=dest_plate['A1']       # Dispenses to entire column 1
)

# Use rows() for row-wise operations
for row in plate.rows():
    multi_pipette.transfer(100, reservoir['A1'], row[0])
```

### 9. Common Protocol Patterns

**Serial Dilution:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'D1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'D2')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D3')

    # Load pipette
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Add diluent to all wells except first
    p300.transfer(100, reservoir['A1'], plate.rows()[0][1:])

    # Serial dilution across row
    p300.transfer(
        100,
        plate.rows()[0][:11],  # Source: wells 0-10
        plate.rows()[0][1:],   # Dest: wells 1-11
        mix_after=(3, 50),     # Mix 3x with 50µL after dispense
        new_tip='always'
    )
```

**Plate Replication:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')
    dest = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D2')

    # Load pipette
    p1000 = protocol.load_instrument('p1000_single_flex', 'left', tip_racks=[tips])

    # Transfer from all wells in source to dest
    p1000.transfer(
        100,
        source.wells(),
        dest.wells(),
        new_tip='always'
    )
```

**PCR Setup:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load thermocycler
    tc_mod = protocol.load_module('thermocyclerModuleV2')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    # Load tips and reagents
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'C1')
    reagents = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D1')

    # Load pipette
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Open thermocycler lid
    tc_mod.open_lid()

    # Distribute master mix
    p300.distribute(
        20,
        reagents['A1'],
        tc_plate.wells(),
        new_tip='once'
    )

    # Add samples (example for first 8 wells)
    for i, well in enumerate(tc_plate.wells()[:8]):
        p300.transfer(5, reagents.wells()[i+1], well, new_tip='always')

    # Run PCR
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)

    # PCR profile
    tc_mod.set_block_temperature(95, hold_time_seconds=180)

    profile = [
        {'temperature': 95, 'hold_time_seconds': 15},
        {'temperature': 60, 'hold_time_seconds': 30},
        {'temperature': 72, 'hold_time_seconds': 30}
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)

    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)

    tc_mod.deactivate_lid()
    tc_mod.open_lid()
```

## Best Practices

1. **Always specify API level**: Use the latest stable API version in metadata
2. **Use meaningful labels**: Label labware for easier identification in logs
3. **Check tip availability**: Ensure sufficient tips for protocol completion
4. **Add comments**: Use `protocol.comment()` for debugging and logging
5. **Simulate first**: Always test protocols in simulation before running on robot
6. **Handle errors gracefully**: Add pauses for manual intervention when needed
7. **Consider timing**: Use delays when protocols require incubation periods
8. **Track liquids**: Use liquid tracking for better setup validation
9. **Optimize tip usage**: Use `new_tip='once'` when appropriate to save tips
10. **Control flow rates**: Adjust flow rates for viscous or volatile liquids

## Troubleshooting

**Common Issues:**

- **Out of tips**: Verify tip rack capacity matches protocol requirements
- **Labware collisions**: Check deck layout for spatial conflicts
- **Volume errors**: Ensure volumes don't exceed well or pipette capacities
- **Module not responding**: Verify module is properly connected and firmware is updated
- **Inaccurate volumes**: Calibrate pipettes and check for air bubbles
- **Protocol fails in simulation**: Check API version compatibility and labware definitions

## Resources

For detailed API documentation, see `references/api_reference.md` in this skill directory.

For example protocol templates, see `scripts/` directory.

---

## Reference: Api_Reference

# Opentrons Python Protocol API v2 Reference

## Protocol Context Methods

### Labware Management

| Method | Description | Returns |
|--------|-------------|---------|
| `load_labware(name, location, label=None, namespace=None, version=None)` | Load labware onto deck | Labware object |
| `load_adapter(name, location, namespace=None, version=None)` | Load adapter onto deck | Labware object |
| `load_labware_from_definition(definition, location, label=None)` | Load custom labware from JSON | Labware object |
| `load_labware_on_adapter(name, adapter, label=None)` | Load labware on adapter | Labware object |
| `load_labware_by_name(name, location, label=None, namespace=None, version=None)` | Alternative load method | Labware object |
| `load_lid_stack(load_name, location, quantity=None)` | Load lid stack (Flex only) | Labware object |

### Instrument Management

| Method | Description | Returns |
|--------|-------------|---------|
| `load_instrument(instrument_name, mount, tip_racks=None, replace=False)` | Load pipette | InstrumentContext |

### Module Management

| Method | Description | Returns |
|--------|-------------|---------|
| `load_module(module_name, location=None, configuration=None)` | Load hardware module | ModuleContext |

### Liquid Management

| Method | Description | Returns |
|--------|-------------|---------|
| `define_liquid(name, description=None, display_color=None)` | Define liquid type | Liquid object |

### Execution Control

| Method | Description | Returns |
|--------|-------------|---------|
| `pause(msg=None)` | Pause protocol execution | None |
| `resume()` | Resume after pause | None |
| `delay(seconds=0, minutes=0, msg=None)` | Delay execution | None |
| `comment(msg)` | Add comment to protocol log | None |
| `home()` | Home all axes | None |
| `set_rail_lights(on)` | Control rail lights (Flex only) | None |

### Protocol Properties

| Property | Description | Type |
|----------|-------------|------|
| `deck` | Deck layout | Deck object |
| `fixed_trash` | Fixed trash location (OT-2) | TrashBin object |
| `loaded_labwares` | Dictionary of loaded labware | Dict |
| `loaded_instruments` | Dictionary of loaded instruments | Dict |
| `loaded_modules` | Dictionary of loaded modules | Dict |
| `is_simulating()` | Check if protocol is simulating | Bool |
| `bundled_data` | Access to bundled data files | Dict |
| `params` | Runtime parameters | ParametersContext |

## Instrument Context (Pipette) Methods

### Tip Management

| Method | Description | Returns |
|--------|-------------|---------|
| `pick_up_tip(location=None, presses=None, increment=None)` | Pick up tip | InstrumentContext |
| `drop_tip(location=None, home_after=True)` | Drop tip in trash | InstrumentContext |
| `return_tip(home_after=True)` | Return tip to rack | InstrumentContext |
| `reset_tipracks()` | Reset tip tracking | None |

### Liquid Handling - Basic

| Method | Description | Returns |
|--------|-------------|---------|
| `aspirate(volume=None, location=None, rate=1.0)` | Aspirate liquid | InstrumentContext |
| `dispense(volume=None, location=None, rate=1.0, push_out=None)` | Dispense liquid | InstrumentContext |
| `blow_out(location=None)` | Expel remaining liquid | InstrumentContext |
| `touch_tip(location=None, radius=1.0, v_offset=-1.0, speed=60.0)` | Remove droplets from tip | InstrumentContext |
| `mix(repetitions=1, volume=None, location=None, rate=1.0)` | Mix liquid | InstrumentContext |
| `air_gap(volume=None, height=None)` | Create air gap | InstrumentContext |

### Liquid Handling - Complex

| Method | Description | Returns |
|--------|-------------|---------|
| `transfer(volume, source, dest, **kwargs)` | Transfer liquid | InstrumentContext |
| `distribute(volume, source, dest, **kwargs)` | Distribute from one to many | InstrumentContext |
| `consolidate(volume, source, dest, **kwargs)` | Consolidate from many to one | InstrumentContext |

**transfer(), distribute(), consolidate() kwargs:**
- `new_tip`: 'always', 'once', or 'never'
- `trash`: True/False - trash tips after use
- `touch_tip`: True/False - touch tip after aspirate/dispense
- `blow_out`: True/False - blow out after dispense
- `mix_before`: (repetitions, volume) tuple
- `mix_after`: (repetitions, volume) tuple
- `disposal_volume`: Extra volume for contamination prevention
- `carryover`: True/False - enable multi-transfer for large volumes
- `gradient`: (start_concentration, end_concentration) for gradients

### Movement and Positioning

| Method | Description | Returns |
|--------|-------------|---------|
| `move_to(location, force_direct=False, minimum_z_height=None, speed=None)` | Move to location | InstrumentContext |
| `home()` | Home pipette axes | None |

### Pipette Properties

| Property | Description | Type |
|----------|-------------|------|
| `default_speed` | Default movement speed | Float |
| `min_volume` | Minimum pipette volume | Float |
| `max_volume` | Maximum pipette volume | Float |
| `current_volume` | Current volume in tip | Float |
| `has_tip` | Check if tip is attached | Bool |
| `name` | Pipette name | String |
| `model` | Pipette model | String |
| `mount` | Mount location | String |
| `channels` | Number of channels | Int |
| `tip_racks` | Associated tip racks | List |
| `trash_container` | Trash location | TrashBin object |
| `starting_tip` | Starting tip for protocol | Well object |
| `flow_rate` | Flow rate settings | FlowRates object |

### Flow Rate Properties

Access via `pipette.flow_rate`:

| Property | Description | Units |
|----------|-------------|-------|
| `aspirate` | Aspirate flow rate | µL/s |
| `dispense` | Dispense flow rate | µL/s |
| `blow_out` | Blow out flow rate | µL/s |

## Labware Methods

### Well Access

| Method | Description | Returns |
|--------|-------------|---------|
| `wells()` | Get all wells | List[Well] |
| `wells_by_name()` | Get wells dictionary | Dict[str, Well] |
| `rows()` | Get wells by row | List[List[Well]] |
| `columns()` | Get wells by column | List[List[Well]] |
| `rows_by_name()` | Get rows dictionary | Dict[str, List[Well]] |
| `columns_by_name()` | Get columns dictionary | Dict[str, List[Well]] |

### Labware Properties

| Property | Description | Type |
|----------|-------------|------|
| `name` | Labware name | String |
| `parent` | Parent location | Location object |
| `quirks` | Labware quirks list | List |
| `magdeck_engage_height` | Magnetic module height | Float |
| `uri` | Labware URI | String |
| `calibrated_offset` | Calibration offset | Point |

## Well Methods and Properties

### Liquid Operations

| Method | Description | Returns |
|--------|-------------|---------|
| `load_liquid(liquid, volume)` | Load liquid into well | None |
| `load_empty()` | Mark well as empty | None |
| `from_center_cartesian(x, y, z)` | Get location from center | Location |

### Location Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `top(z=0)` | Get location at top of well | Location |
| `bottom(z=0)` | Get location at bottom of well | Location |
| `center()` | Get location at center of well | Location |

### Well Properties

| Property | Description | Type |
|----------|-------------|------|
| `diameter` | Well diameter (circular) | Float |
| `length` | Well length (rectangular) | Float |
| `width` | Well width (rectangular) | Float |
| `depth` | Well depth | Float |
| `max_volume` | Maximum volume | Float |
| `display_name` | Display name | String |
| `has_tip` | Check if tip present | Bool |

## Module Contexts

### Temperature Module

| Method | Description | Returns |
|--------|-------------|---------|
| `set_temperature(celsius)` | Set target temperature | None |
| `await_temperature(celsius)` | Wait for temperature | None |
| `deactivate()` | Turn off temperature control | None |
| `load_labware(name, label=None, namespace=None, version=None)` | Load labware on module | Labware |

**Properties:**
- `temperature`: Current temperature (°C)
- `target`: Target temperature (°C)
- `status`: 'idle', 'holding', 'cooling', or 'heating'
- `labware`: Loaded labware

### Magnetic Module

| Method | Description | Returns |
|--------|-------------|---------|
| `engage(height_from_base=None, offset=None, height=None)` | Engage magnets | None |
| `disengage()` | Disengage magnets | None |
| `load_labware(name, label=None, namespace=None, version=None)` | Load labware on module | Labware |

**Properties:**
- `status`: 'engaged' or 'disengaged'
- `labware`: Loaded labware

### Heater-Shaker Module

| Method | Description | Returns |
|--------|-------------|---------|
| `set_target_temperature(celsius)` | Set heater target | None |
| `wait_for_temperature()` | Wait for temperature | None |
| `set_and_wait_for_temperature(celsius)` | Set and wait | None |
| `deactivate_heater()` | Turn off heater | None |
| `set_and_wait_for_shake_speed(rpm)` | Set shake speed | None |
| `deactivate_shaker()` | Turn off shaker | None |
| `open_labware_latch()` | Open latch | None |
| `close_labware_latch()` | Close latch | None |
| `load_labware(name, label=None, namespace=None, version=None)` | Load labware on module | Labware |

**Properties:**
- `temperature`: Current temperature (°C)
- `target_temperature`: Target temperature (°C)
- `current_speed`: Current shake speed (rpm)
- `target_speed`: Target shake speed (rpm)
- `labware_latch_status`: 'idle_open', 'idle_closed', 'opening', 'closing'
- `status`: Module status
- `labware`: Loaded labware

### Thermocycler Module

| Method | Description | Returns |
|--------|-------------|---------|
| `open_lid()` | Open lid | None |
| `close_lid()` | Close lid | None |
| `set_lid_temperature(celsius)` | Set lid temperature | None |
| `deactivate_lid()` | Turn off lid heater | None |
| `set_block_temperature(temperature, hold_time_seconds=0, hold_time_minutes=0, ramp_rate=None, block_max_volume=None)` | Set block temperature | None |
| `deactivate_block()` | Turn off block | None |
| `execute_profile(steps, repetitions, block_max_volume=None)` | Run temperature profile | None |
| `load_labware(name, label=None, namespace=None, version=None)` | Load labware on module | Labware |

**Profile step format:**
```python
{'temperature': 95, 'hold_time_seconds': 30, 'hold_time_minutes': 0}
```

**Properties:**
- `block_temperature`: Current block temperature (°C)
- `block_target_temperature`: Target block temperature (°C)
- `lid_temperature`: Current lid temperature (°C)
- `lid_target_temperature`: Target lid temperature (°C)
- `lid_position`: 'open', 'closed', 'in_between'
- `ramp_rate`: Block temperature ramp rate (°C/s)
- `status`: Module status
- `labware`: Loaded labware

### Absorbance Plate Reader Module

| Method | Description | Returns |
|--------|-------------|---------|
| `initialize(mode, wavelengths)` | Initialize reader | None |
| `read(export_filename=None)` | Read plate | Dict |
| `close_lid()` | Close lid | None |
| `open_lid()` | Open lid | None |
| `load_labware(name, label=None, namespace=None, version=None)` | Load labware on module | Labware |

**Read modes:**
- `'single'`: Single wavelength
- `'multi'`: Multiple wavelengths

**Properties:**
- `is_lid_on`: Lid status
- `labware`: Loaded labware

## Common Labware API Names

### Plates

- `corning_96_wellplate_360ul_flat`
- `nest_96_wellplate_100ul_pcr_full_skirt`
- `nest_96_wellplate_200ul_flat`
- `biorad_96_wellplate_200ul_pcr`
- `appliedbiosystems_384_wellplate_40ul`

### Reservoirs

- `nest_12_reservoir_15ml`
- `nest_1_reservoir_195ml`
- `usascientific_12_reservoir_22ml`

### Tip Racks

**Flex:**
- `opentrons_flex_96_tiprack_50ul`
- `opentrons_flex_96_tiprack_200ul`
- `opentrons_flex_96_tiprack_1000ul`

**OT-2:**
- `opentrons_96_tiprack_20ul`
- `opentrons_96_tiprack_300ul`
- `opentrons_96_tiprack_1000ul`

### Tube Racks

- `opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical`
- `opentrons_24_tuberack_nest_1.5ml_snapcap`
- `opentrons_24_tuberack_nest_1.5ml_screwcap`
- `opentrons_15_tuberack_falcon_15ml_conical`

### Adapters

- `opentrons_flex_96_tiprack_adapter`
- `opentrons_96_deep_well_adapter`
- `opentrons_aluminum_flat_bottom_plate`

## Error Handling

Common exceptions:

- `OutOfTipsError`: No tips available
- `LabwareNotLoadedError`: Labware not loaded on deck
- `InvalidContainerError`: Invalid labware specification
- `InstrumentNotLoadedError`: Pipette not loaded
- `InvalidVolumeError`: Volume out of range

## Simulation and Debugging

Check simulation status:
```python
if protocol.is_simulating():
    protocol.comment('Running in simulation')
```

Access bundled data files:
```python
data_file = protocol.bundled_data['data.csv']
with open(data_file) as f:
    data = f.read()
```

## Version Compatibility

API Level compatibility:

| API Level | Features |
|-----------|----------|
| 2.19 | Latest features, Flex support |
| 2.18 | Absorbance plate reader |
| 2.17 | Liquid tracking improvements |
| 2.16 | Flex 8-channel partial tip pickup |
| 2.15 | Heater-Shaker Gen1 |
| 2.13 | Temperature Module Gen2 |
| 2.0-2.12 | Core OT-2 functionality |

Always use the latest stable API version for new protocols.
