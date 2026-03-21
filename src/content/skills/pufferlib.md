---
title: "Pufferlib"
description: "High-performance reinforcement learning framework optimized for speed and scale. Use when you need fast parallel training, vectorized environments, multi-agent systems, or integration with game environments (Atari, Procgen, NetHack). Achieves 2-10..."
category: "development"
source: "community"
author: "Community"
tags: ["pufferlib"]
date: 2026-03-20
---

# PufferLib - High-Performance Reinforcement Learning

## Overview

PufferLib is a high-performance reinforcement learning library designed for fast parallel environment simulation and training. It achieves training at millions of steps per second through optimized vectorization, native multi-agent support, and efficient PPO implementation (PuffeRL). The library provides the Ocean suite of 20+ environments and seamless integration with Gymnasium, PettingZoo, and specialized RL frameworks.

## When to Use This Skill

Use this skill when:
- **Training RL agents** with PPO on any environment (single or multi-agent)
- **Creating custom environments** using the PufferEnv API
- **Optimizing performance** for parallel environment simulation (vectorization)
- **Integrating existing environments** from Gymnasium, PettingZoo, Atari, Procgen, etc.
- **Developing policies** with CNN, LSTM, or custom architectures
- **Scaling RL** to millions of steps per second for faster experimentation
- **Multi-agent RL** with native multi-agent environment support

## Core Capabilities

### 1. High-Performance Training (PuffeRL)

PuffeRL is PufferLib's optimized PPO+LSTM training algorithm achieving 1M-4M steps/second.

**Quick start training:**
```bash
# CLI training
puffer train procgen-coinrun --train.device cuda --train.learning-rate 3e-4

# Distributed training
torchrun --nproc_per_node=4 train.py
```

**Python training loop:**
```python
import pufferlib
from pufferlib import PuffeRL

# Create vectorized environment
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Create trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768
)

# Training loop
for iteration in range(num_iterations):
    trainer.evaluate()  # Collect rollouts
    trainer.train()     # Train on batch
    trainer.mean_and_log()  # Log results
```

**For comprehensive training guidance**, read `references/training.md` for:
- Complete training workflow and CLI options
- Hyperparameter tuning with Protein
- Distributed multi-GPU/multi-node training
- Logger integration (Weights & Biases, Neptune)
- Checkpointing and resume training
- Performance optimization tips
- Curriculum learning patterns

### 2. Environment Development (PufferEnv)

Create custom high-performance environments with the PufferEnv API.

**Basic environment structure:**
```python
import numpy as np
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Define spaces
        self.observation_space = self.make_space((4,))
        self.action_space = self.make_discrete(4)

        self.reset()

    def reset(self):
        # Reset state and return initial observation
        return np.zeros(4, dtype=np.float32)

    def step(self, action):
        # Execute action, compute reward, check done
        obs = self._get_observation()
        reward = self._compute_reward()
        done = self._is_done()
        info = {}

        return obs, reward, done, info
```

**Use the template script:** `scripts/env_template.py` provides complete single-agent and multi-agent environment templates with examples of:
- Different observation space types (vector, image, dict)
- Action space variations (discrete, continuous, multi-discrete)
- Multi-agent environment structure
- Testing utilities

**For complete environment development**, read `references/environments.md` for:
- PufferEnv API details and in-place operation patterns
- Observation and action space definitions
- Multi-agent environment creation
- Ocean suite (20+ pre-built environments)
- Performance optimization (Python to C workflow)
- Environment wrappers and best practices
- Debugging and validation techniques

### 3. Vectorization and Performance

Achieve maximum throughput with optimized parallel simulation.

**Vectorization setup:**
```python
import pufferlib

# Automatic vectorization
env = pufferlib.make('environment_name', num_envs=256, num_workers=8)

# Performance benchmarks:
# - Pure Python envs: 100k-500k SPS
# - C-based envs: 100M+ SPS
# - With training: 400k-4M total SPS
```

**Key optimizations:**
- Shared memory buffers for zero-copy observation passing
- Busy-wait flags instead of pipes/queues
- Surplus environments for async returns
- Multiple environments per worker

**For vectorization optimization**, read `references/vectorization.md` for:
- Architecture and performance characteristics
- Worker and batch size configuration
- Serial vs multiprocessing vs async modes
- Shared memory and zero-copy patterns
- Hierarchical vectorization for large scale
- Multi-agent vectorization strategies
- Performance profiling and troubleshooting

### 4. Policy Development

Build policies as standard PyTorch modules with optional utilities.

**Basic policy structure:**
```python
import torch.nn as nn
from pufferlib.pytorch import layer_init

class Policy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Encoder
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Actor and critic heads
        self.actor = layer_init(nn.Linear(256, num_actions), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

**For complete policy development**, read `references/policies.md` for:
- CNN policies for image observations
- Recurrent policies with optimized LSTM (3x faster inference)
- Multi-input policies for complex observations
- Continuous action policies
- Multi-agent policies (shared vs independent parameters)
- Advanced architectures (attention, residual)
- Observation normalization and gradient clipping
- Policy debugging and testing

### 5. Environment Integration

Seamlessly integrate environments from popular RL frameworks.

**Gymnasium integration:**
```python
import gymnasium as gym
import pufferlib

# Wrap Gymnasium environment
gym_env = gym.make('CartPole-v1')
env = pufferlib.emulate(gym_env, num_envs=256)

# Or use make directly
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

**PettingZoo multi-agent:**
```python
# Multi-agent environment
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_envs=128)
```

**Supported frameworks:**
- Gymnasium / OpenAI Gym
- PettingZoo (parallel and AEC)
- Atari (ALE)
- Procgen
- NetHack / MiniHack
- Minigrid
- Neural MMO
- Crafter
- GPUDrive
- MicroRTS
- Griddly
- And more...

**For integration details**, read `references/integration.md` for:
- Complete integration examples for each framework
- Custom wrappers (observation, reward, frame stacking, action repeat)
- Space flattening and unflattening
- Environment registration
- Compatibility patterns
- Performance considerations
- Integration debugging

## Quick Start Workflow

### For Training Existing Environments

1. Choose environment from Ocean suite or compatible framework
2. Use `scripts/train_template.py` as starting point
3. Configure hyperparameters for your task
4. Run training with CLI or Python script
5. Monitor with Weights & Biases or Neptune
6. Refer to `references/training.md` for optimization

### For Creating Custom Environments

1. Start with `scripts/env_template.py`
2. Define observation and action spaces
3. Implement `reset()` and `step()` methods
4. Test environment locally
5. Vectorize with `pufferlib.emulate()` or `make()`
6. Refer to `references/environments.md` for advanced patterns
7. Optimize with `references/vectorization.md` if needed

### For Policy Development

1. Choose architecture based on observations:
   - Vector observations → MLP policy
   - Image observations → CNN policy
   - Sequential tasks → LSTM policy
   - Complex observations → Multi-input policy
2. Use `layer_init` for proper weight initialization
3. Follow patterns in `references/policies.md`
4. Test with environment before full training

### For Performance Optimization

1. Profile current throughput (steps per second)
2. Check vectorization configuration (num_envs, num_workers)
3. Optimize environment code (in-place ops, numpy vectorization)
4. Consider C implementation for critical paths
5. Use `references/vectorization.md` for systematic optimization

## Resources

### scripts/

**train_template.py** - Complete training script template with:
- Environment creation and configuration
- Policy initialization
- Logger integration (WandB, Neptune)
- Training loop with checkpointing
- Command-line argument parsing
- Multi-GPU distributed training setup

**env_template.py** - Environment implementation templates:
- Single-agent PufferEnv example (grid world)
- Multi-agent PufferEnv example (cooperative navigation)
- Multiple observation/action space patterns
- Testing utilities

### references/

**training.md** - Comprehensive training guide:
- Training workflow and CLI options
- Hyperparameter configuration
- Distributed training (multi-GPU, multi-node)
- Monitoring and logging
- Checkpointing
- Protein hyperparameter tuning
- Performance optimization
- Common training patterns
- Troubleshooting

**environments.md** - Environment development guide:
- PufferEnv API and characteristics
- Observation and action spaces
- Multi-agent environments
- Ocean suite environments
- Custom environment development workflow
- Python to C optimization path
- Third-party environment integration
- Wrappers and best practices
- Debugging

**vectorization.md** - Vectorization optimization:
- Architecture and key optimizations
- Vectorization modes (serial, multiprocessing, async)
- Worker and batch configuration
- Shared memory and zero-copy patterns
- Advanced vectorization (hierarchical, custom)
- Multi-agent vectorization
- Performance monitoring and profiling
- Troubleshooting and best practices

**policies.md** - Policy architecture guide:
- Basic policy structure
- CNN policies for images
- LSTM policies with optimization
- Multi-input policies
- Continuous action policies
- Multi-agent policies
- Advanced architectures (attention, residual)
- Observation processing and unflattening
- Initialization and normalization
- Debugging and testing

**integration.md** - Framework integration guide:
- Gymnasium integration
- PettingZoo integration (parallel and AEC)
- Third-party environments (Procgen, NetHack, Minigrid, etc.)
- Custom wrappers (observation, reward, frame stacking, etc.)
- Space conversion and unflattening
- Environment registration
- Compatibility patterns
- Performance considerations
- Debugging integration

## Tips for Success

1. **Start simple**: Begin with Ocean environments or Gymnasium integration before creating custom environments

2. **Profile early**: Measure steps per second from the start to identify bottlenecks

3. **Use templates**: `scripts/train_template.py` and `scripts/env_template.py` provide solid starting points

4. **Read references as needed**: Each reference file is self-contained and focused on a specific capability

5. **Optimize progressively**: Start with Python, profile, then optimize critical paths with C if needed

6. **Leverage vectorization**: PufferLib's vectorization is key to achieving high throughput

7. **Monitor training**: Use WandB or Neptune to track experiments and identify issues early

8. **Test environments**: Validate environment logic before scaling up training

9. **Check existing environments**: Ocean suite provides 20+ pre-built environments

10. **Use proper initialization**: Always use `layer_init` from `pufferlib.pytorch` for policies

## Common Use Cases

### Training on Standard Benchmarks
```python
# Atari
env = pufferlib.make('atari-pong', num_envs=256)

# Procgen
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Minigrid
env = pufferlib.make('minigrid-empty-8x8', num_envs=256)
```

### Multi-Agent Learning
```python
# PettingZoo
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)

# Shared policy for all agents
policy = create_policy(env.observation_space, env.action_space)
trainer = PuffeRL(env=env, policy=policy)
```

### Custom Task Development
```python
# Create custom environment
class MyTask(PufferEnv):
    # ... implement environment ...

# Vectorize and train
env = pufferlib.emulate(MyTask, num_envs=256)
trainer = PuffeRL(env=env, policy=my_policy)
```

### High-Performance Optimization
```python
# Maximize throughput
env = pufferlib.make(
    'my-env',
    num_envs=1024,      # Large batch
    num_workers=16,     # Many workers
    envs_per_worker=64  # Optimize per worker
)
```

## Installation

```bash
uv pip install pufferlib
```

## Documentation

- Official docs: https://puffer.ai/docs.html
- GitHub: https://github.com/PufferAI/PufferLib
- Discord: Community support available

---

## Reference: Environments

# PufferLib Environments Guide

## Overview

PufferLib provides the PufferEnv API for creating high-performance custom environments, and the Ocean suite containing 20+ pre-built environments. Environments support both single-agent and multi-agent scenarios with native vectorization.

## PufferEnv API

### Core Characteristics

PufferEnv is designed for performance through in-place operations:
- Observations, actions, and rewards are initialized from a shared buffer object
- All operations happen in-place to avoid creating and copying arrays
- Native support for both single-agent and multi-agent environments
- Flat observation/action spaces for efficient vectorization

### Creating a PufferEnv

```python
import numpy as np
import pufferlib
from pufferlib import PufferEnv

class MyEnvironment(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Define observation and action spaces
        self.observation_space = self.make_space({
            'image': (84, 84, 3),
            'vector': (10,)
        })

        self.action_space = self.make_discrete(4)  # 4 discrete actions

        # Initialize state
        self.reset()

    def reset(self):
        """Reset environment to initial state."""
        # Reset internal state
        self.agent_pos = np.array([0, 0])
        self.step_count = 0

        # Return initial observation
        obs = {
            'image': np.zeros((84, 84, 3), dtype=np.uint8),
            'vector': np.zeros(10, dtype=np.float32)
        }

        return obs

    def step(self, action):
        """Execute one environment step."""
        # Update state based on action
        self.step_count += 1

        # Calculate reward
        reward = self._compute_reward()

        # Check if episode is done
        done = self.step_count >= 1000

        # Generate observation
        obs = self._get_observation()

        # Additional info
        info = {'episode': {'r': reward, 'l': self.step_count}} if done else {}

        return obs, reward, done, info

    def _compute_reward(self):
        """Compute reward for current state."""
        return 1.0

    def _get_observation(self):
        """Generate observation from current state."""
        return {
            'image': np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8),
            'vector': np.random.randn(10).astype(np.float32)
        }
```

### Observation Spaces

#### Discrete Spaces

```python
# Single discrete value
self.observation_space = self.make_discrete(10)  # Values 0-9

# Dict with discrete values
self.observation_space = self.make_space({
    'position': (1,),  # Continuous
    'type': self.make_discrete(5)  # Discrete
})
```

#### Continuous Spaces

```python
# Box space (continuous)
self.observation_space = self.make_space({
    'image': (84, 84, 3),      # Image
    'vector': (10,),            # Vector
    'scalar': (1,)              # Single value
})
```

#### Multi-Discrete Spaces

```python
# Multiple discrete values
self.observation_space = self.make_multi_discrete([3, 5, 2])  # 3 values, 5 values, 2 values
```

### Action Spaces

```python
# Discrete actions
self.action_space = self.make_discrete(4)  # 4 actions: 0, 1, 2, 3

# Continuous actions
self.action_space = self.make_space((3,))  # 3D continuous action

# Multi-discrete actions
self.action_space = self.make_multi_discrete([3, 3])  # Two 3-way discrete choices
```

## Multi-Agent Environments

PufferLib has native multi-agent support, treating single-agent and multi-agent environments uniformly.

### Multi-Agent PufferEnv

```python
class MultiAgentEnv(PufferEnv):
    def __init__(self, num_agents=4, buf=None):
        super().__init__(buf)

        self.num_agents = num_agents

        # Per-agent observation space
        self.single_observation_space = self.make_space({
            'position': (2,),
            'velocity': (2,),
            'global': (10,)
        })

        # Per-agent action space
        self.single_action_space = self.make_discrete(5)

        self.reset()

    def reset(self):
        """Reset all agents."""
        self.agents = {f'agent_{i}': Agent(i) for i in range(self.num_agents)}

        # Return observations for all agents
        return {
            agent_id: self._get_obs(agent)
            for agent_id, agent in self.agents.items()
        }

    def step(self, actions):
        """Step all agents."""
        # actions is a dict: {agent_id: action}
        observations = {}
        rewards = {}
        dones = {}
        infos = {}

        for agent_id, action in actions.items():
            agent = self.agents[agent_id]

            # Update agent
            agent.update(action)

            # Generate results
            observations[agent_id] = self._get_obs(agent)
            rewards[agent_id] = self._compute_reward(agent)
            dones[agent_id] = agent.is_done()
            infos[agent_id] = {}

        # Check for global done condition
        dones['__all__'] = all(dones.values())

        return observations, rewards, dones, infos
```

## Ocean Environment Suite

PufferLib provides the Ocean suite with 20+ pre-built environments:

### Available Environments

#### Arcade Games
- **Atari**: Classic Atari 2600 games via Arcade Learning Environment
- **Procgen**: Procedurally generated games for generalization testing

#### Grid-Based
- **Minigrid**: Partially observable gridworld environments
- **Crafter**: Open-ended survival crafting game
- **NetHack**: Classic roguelike dungeon crawler
- **MiniHack**: Simplified NetHack variants

#### Multi-Agent
- **PettingZoo**: Multi-agent environment suite (including Butterfly)
- **MAgent**: Large-scale multi-agent scenarios
- **Neural MMO**: Massively multi-agent survival game

#### Specialized
- **Pokemon Red**: Classic Pokemon game environment
- **GPUDrive**: High-performance driving simulator
- **Griddly**: Grid-based game engine
- **MicroRTS**: Real-time strategy game

### Using Ocean Environments

```python
import pufferlib

# Make environment
env = pufferlib.make('procgen-coinrun', num_envs=256)

# With custom configuration
env = pufferlib.make(
    'atari-pong',
    num_envs=128,
    frameskip=4,
    framestack=4
)

# Multi-agent environment
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_agents=4)
```

## Custom Environment Development

### Development Workflow

1. **Prototype in Python**: Start with pure Python PufferEnv
2. **Optimize Critical Paths**: Identify bottlenecks
3. **Implement in C**: Rewrite performance-critical code in C
4. **Create Bindings**: Use Python C API
5. **Compile**: Build as extension module
6. **Register**: Add to Ocean suite

### Performance Benchmarks

- **Pure Python**: 100k-500k steps/second
- **C Implementation**: 100M+ steps/second
- **Training with Python env**: ~400k total SPS
- **Training with C env**: ~4M total SPS

### Python Optimization Tips

```python
# Use NumPy operations instead of Python loops
# Bad
for i in range(len(array)):
    array[i] = array[i] * 2

# Good
array *= 2

# Pre-allocate arrays instead of appending
# Bad
observations = []
for i in range(n):
    observations.append(generate_obs())

# Good
observations = np.empty((n, obs_shape), dtype=np.float32)
for i in range(n):
    observations[i] = generate_obs()

# Use in-place operations
# Bad
new_state = state + delta

# Good
state += delta
```

### C Extension Example

```c
// my_env.c
#include <Python.h>
#include <numpy/arrayobject.h>

// Fast environment step implementation
static PyObject* fast_step(PyObject* self, PyObject* args) {
    PyArrayObject* state;
    int action;

    if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &state, &action)) {
        return NULL;
    }

    // High-performance C implementation
    // ...

    return Py_BuildValue("Ofi", obs, reward, done);
}

static PyMethodDef methods[] = {
    {"fast_step", fast_step, METH_VARARGS, "Fast environment step"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "my_env_c",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_my_env_c(void) {
    import_array();
    return PyModule_Create(&module);
}
```

## Third-Party Environment Integration

### Gymnasium Environments

```python
import gymnasium as gym
import pufferlib

# Wrap Gymnasium environment
gym_env = gym.make('CartPole-v1')
puffer_env = pufferlib.emulate(gym_env, num_envs=256)

# Or use make directly
env = pufferlib.make('gym-CartPole-v1', num_envs=256)
```

### PettingZoo Environments

```python
from pettingzoo.butterfly import pistonball_v6
import pufferlib

# Wrap PettingZoo environment
pz_env = pistonball_v6.env()
puffer_env = pufferlib.emulate(pz_env, num_envs=128)

# Or use make directly
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)
```

### Custom Wrappers

```python
class CustomWrapper(pufferlib.PufferEnv):
    """Wrapper to modify environment behavior."""

    def __init__(self, base_env, buf=None):
        super().__init__(buf)
        self.base_env = base_env
        self.observation_space = base_env.observation_space
        self.action_space = base_env.action_space

    def reset(self):
        obs = self.base_env.reset()
        # Modify observation
        return self._process_obs(obs)

    def step(self, action):
        # Modify action
        modified_action = self._process_action(action)

        obs, reward, done, info = self.base_env.step(modified_action)

        # Modify outputs
        obs = self._process_obs(obs)
        reward = self._process_reward(reward)

        return obs, reward, done, info
```

## Environment Best Practices

### State Management

```python
# Store minimal state, compute on demand
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.agent_pos = np.zeros(2)  # Minimal state

    def _get_observation(self):
        # Compute full observation on demand
        observation = np.zeros((84, 84, 3), dtype=np.uint8)
        self._render_scene(observation, self.agent_pos)
        return observation
```

### Reward Scaling

```python
# Normalize rewards to reasonable range
def step(self, action):
    # ... environment logic ...

    # Scale large rewards
    raw_reward = compute_raw_reward()
    reward = np.clip(raw_reward / 100.0, -10, 10)

    return obs, reward, done, info
```

### Episode Termination

```python
def step(self, action):
    # ... environment logic ...

    # Multiple termination conditions
    timeout = self.step_count >= self.max_steps
    success = self._check_success()
    failure = self._check_failure()

    done = timeout or success or failure

    info = {
        'TimeLimit.truncated': timeout,
        'success': success
    }

    return obs, reward, done, info
```

### Memory Efficiency

```python
# Reuse buffers instead of allocating new ones
class MemoryEfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate observation buffer
        self._obs_buffer = np.zeros((84, 84, 3), dtype=np.uint8)

    def _get_observation(self):
        # Reuse buffer, modify in place
        self._render_scene(self._obs_buffer)
        return self._obs_buffer  # Return view, not copy
```

## Debugging Environments

### Validation Checks

```python
# Add assertions to catch bugs
def step(self, action):
    assert self.action_space.contains(action), f"Invalid action: {action}"

    obs, reward, done, info = self._step_impl(action)

    assert self.observation_space.contains(obs), "Invalid observation"
    assert np.isfinite(reward), "Non-finite reward"

    return obs, reward, done, info
```

### Rendering

```python
class DebuggableEnv(PufferEnv):
    def __init__(self, buf=None, render_mode=None):
        super().__init__(buf)
        self.render_mode = render_mode

    def render(self):
        """Render environment for debugging."""
        if self.render_mode == 'human':
            # Display to screen
            self._display_scene()
        elif self.render_mode == 'rgb_array':
            # Return image
            return self._render_to_array()
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def step(self, action):
    logger.debug(f"Step {self.step_count}: action={action}")

    obs, reward, done, info = self._step_impl(action)

    if done:
        logger.info(f"Episode finished: reward={self.total_reward}")

    return obs, reward, done, info
```

---

## Reference: Integration

# PufferLib Integration Guide

## Overview

PufferLib provides an emulation layer that enables seamless integration with popular RL frameworks including Gymnasium, OpenAI Gym, PettingZoo, and many specialized environment libraries. The emulation layer flattens observation and action spaces for efficient vectorization while maintaining compatibility.

## Gymnasium Integration

### Basic Gymnasium Environments

```python
import gymnasium as gym
import pufferlib

# Method 1: Direct wrapping
gym_env = gym.make('CartPole-v1')
puffer_env = pufferlib.emulate(gym_env, num_envs=256)

# Method 2: Using make
env = pufferlib.make('gym-CartPole-v1', num_envs=256)

# Method 3: Custom Gymnasium environment
class MyGymEnv(gym.Env):
    def __init__(self):
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(4,))
        self.action_space = gym.spaces.Discrete(2)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self.observation_space.sample(), {}

    def step(self, action):
        obs = self.observation_space.sample()
        reward = 1.0
        terminated = False
        truncated = False
        info = {}
        return obs, reward, terminated, truncated, info

# Wrap custom environment
puffer_env = pufferlib.emulate(MyGymEnv, num_envs=128)
```

### Atari Environments

```python
import gymnasium as gym
from gymnasium.wrappers import AtariPreprocessing, FrameStack
import pufferlib

# Standard Atari setup
def make_atari_env(env_name='ALE/Pong-v5'):
    env = gym.make(env_name)
    env = AtariPreprocessing(env, frame_skip=4)
    env = FrameStack(env, num_stack=4)
    return env

# Vectorize with PufferLib
env = pufferlib.emulate(make_atari_env, num_envs=256)

# Or use built-in
env = pufferlib.make('atari-pong', num_envs=256, frameskip=4, framestack=4)
```

### Complex Observation Spaces

```python
import gymnasium as gym
from gymnasium.spaces import Dict, Box, Discrete
import pufferlib

class ComplexObsEnv(gym.Env):
    def __init__(self):
        # Dict observation space
        self.observation_space = Dict({
            'image': Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8),
            'vector': Box(low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32),
            'discrete': Discrete(5)
        })
        self.action_space = Discrete(4)

    def reset(self, seed=None, options=None):
        return {
            'image': np.zeros((84, 84, 3), dtype=np.uint8),
            'vector': np.zeros(10, dtype=np.float32),
            'discrete': 0
        }, {}

    def step(self, action):
        obs = {
            'image': np.random.randint(0, 256, (84, 84, 3), dtype=np.uint8),
            'vector': np.random.randn(10).astype(np.float32),
            'discrete': np.random.randint(0, 5)
        }
        return obs, 1.0, False, False, {}

# PufferLib automatically flattens and unflattens complex spaces
env = pufferlib.emulate(ComplexObsEnv, num_envs=128)
```

## PettingZoo Integration

### Parallel Environments

```python
from pettingzoo.butterfly import pistonball_v6
import pufferlib

# Wrap PettingZoo parallel environment
pz_env = pistonball_v6.parallel_env()
puffer_env = pufferlib.emulate(pz_env, num_envs=128)

# Or use make directly
env = pufferlib.make('pettingzoo-pistonball', num_envs=128)
```

### AEC (Agent Environment Cycle) Environments

```python
from pettingzoo.classic import chess_v5
import pufferlib

# Wrap AEC environment (PufferLib handles conversion to parallel)
aec_env = chess_v5.env()
puffer_env = pufferlib.emulate(aec_env, num_envs=64)

# Works with any PettingZoo AEC environment
env = pufferlib.make('pettingzoo-chess', num_envs=64)
```

### Multi-Agent Training

```python
import pufferlib
from pufferlib import PuffeRL

# Create multi-agent environment
env = pufferlib.make('pettingzoo-knights-archers-zombies', num_envs=128)

# Shared policy for all agents
policy = create_policy(env.observation_space, env.action_space)

# Train
trainer = PuffeRL(env=env, policy=policy)

for iteration in range(num_iterations):
    # Observations are dicts: {agent_id: batch_obs}
    rollout = trainer.evaluate()

    # Train on multi-agent data
    trainer.train()
    trainer.mean_and_log()
```

## Third-Party Environments

### Procgen

```python
import pufferlib

# Procgen environments
env = pufferlib.make('procgen-coinrun', num_envs=256, distribution_mode='easy')

# Custom configuration
env = pufferlib.make(
    'procgen-coinrun',
    num_envs=256,
    num_levels=200,  # Number of unique levels
    start_level=0,   # Starting level seed
    distribution_mode='hard'
)
```

### NetHack

```python
import pufferlib

# NetHack Learning Environment
env = pufferlib.make('nethack', num_envs=128)

# MiniHack variants
env = pufferlib.make('minihack-corridor', num_envs=128)
env = pufferlib.make('minihack-room', num_envs=128)
```

### Minigrid

```python
import pufferlib

# Minigrid environments
env = pufferlib.make('minigrid-empty-8x8', num_envs=256)
env = pufferlib.make('minigrid-doorkey-8x8', num_envs=256)
env = pufferlib.make('minigrid-multiroom', num_envs=256)
```

### Neural MMO

```python
import pufferlib

# Large-scale multi-agent environment
env = pufferlib.make(
    'neuralmmo',
    num_envs=64,
    num_agents=128,  # Agents per environment
    map_size=128
)
```

### Crafter

```python
import pufferlib

# Open-ended crafting environment
env = pufferlib.make('crafter', num_envs=128)
```

### GPUDrive

```python
import pufferlib

# GPU-accelerated driving simulator
env = pufferlib.make(
    'gpudrive',
    num_envs=1024,  # Can handle many environments on GPU
    num_vehicles=8
)
```

### MicroRTS

```python
import pufferlib

# Real-time strategy game
env = pufferlib.make(
    'microrts',
    num_envs=128,
    map_size=16,
    max_steps=2000
)
```

### Griddly

```python
import pufferlib

# Grid-based games
env = pufferlib.make('griddly-clusters', num_envs=256)
env = pufferlib.make('griddly-sokoban', num_envs=256)
```

## Custom Wrappers

### Observation Wrappers

```python
import numpy as np
import pufferlib
from pufferlib import PufferEnv

class NormalizeObservations(pufferlib.Wrapper):
    """Normalize observations to zero mean and unit variance."""

    def __init__(self, env):
        super().__init__(env)
        self.obs_mean = np.zeros(env.observation_space.shape)
        self.obs_std = np.ones(env.observation_space.shape)
        self.count = 0

    def reset(self):
        obs = self.env.reset()
        return self._normalize(obs)

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return self._normalize(obs), reward, done, info

    def _normalize(self, obs):
        # Update running statistics
        self.count += 1
        delta = obs - self.obs_mean
        self.obs_mean += delta / self.count
        self.obs_std = np.sqrt(((self.count - 1) * self.obs_std ** 2 + delta * (obs - self.obs_mean)) / self.count)

        # Normalize
        return (obs - self.obs_mean) / (self.obs_std + 1e-8)
```

### Reward Wrappers

```python
class RewardShaping(pufferlib.Wrapper):
    """Add shaped rewards to environment."""

    def __init__(self, env, shaping_fn):
        super().__init__(env)
        self.shaping_fn = shaping_fn

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        # Add shaped reward
        shaped_reward = reward + self.shaping_fn(obs, action)

        return obs, shaped_reward, done, info

# Usage
def proximity_shaping(obs, action):
    """Reward agent for getting closer to goal."""
    goal_pos = np.array([10, 10])
    agent_pos = obs[:2]
    distance = np.linalg.norm(goal_pos - agent_pos)
    return -0.1 * distance

env = pufferlib.make('myenv', num_envs=128)
env = RewardShaping(env, proximity_shaping)
```

### Frame Stacking

```python
class FrameStack(pufferlib.Wrapper):
    """Stack frames for temporal context."""

    def __init__(self, env, num_stack=4):
        super().__init__(env)
        self.num_stack = num_stack
        self.frames = None

    def reset(self):
        obs = self.env.reset()

        # Initialize frame stack
        self.frames = np.repeat(obs[np.newaxis], self.num_stack, axis=0)

        return self._get_obs()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        # Update frame stack
        self.frames = np.roll(self.frames, shift=-1, axis=0)
        self.frames[-1] = obs

        if done:
            self.frames = None

        return self._get_obs(), reward, done, info

    def _get_obs(self):
        return self.frames
```

### Action Repeat

```python
class ActionRepeat(pufferlib.Wrapper):
    """Repeat actions for multiple steps."""

    def __init__(self, env, repeat=4):
        super().__init__(env)
        self.repeat = repeat

    def step(self, action):
        total_reward = 0.0
        done = False

        for _ in range(self.repeat):
            obs, reward, done, info = self.env.step(action)
            total_reward += reward

            if done:
                break

        return obs, total_reward, done, info
```

## Space Conversion

### Flattening Spaces

PufferLib automatically flattens complex observation/action spaces:

```python
from gymnasium.spaces import Dict, Box, Discrete
import pufferlib

# Complex space
original_space = Dict({
    'image': Box(0, 255, (84, 84, 3), dtype=np.uint8),
    'vector': Box(-np.inf, np.inf, (10,), dtype=np.float32),
    'discrete': Discrete(5)
})

# Automatically flattened by PufferLib
# Observations are presented as flat arrays for efficient processing
# But can be unflattened when needed for policy processing
```

### Unflattening for Policies

```python
from pufferlib.pytorch import unflatten_observations

class PolicyWithUnflatten(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()
        self.observation_space = observation_space
        # ... policy architecture ...

    def forward(self, flat_observations):
        # Unflatten to original structure
        observations = unflatten_observations(
            flat_observations,
            self.observation_space
        )

        # Now observations is a dict with 'image', 'vector', 'discrete'
        image_features = self.image_encoder(observations['image'])
        vector_features = self.vector_encoder(observations['vector'])
        # ...
```

## Environment Registration

### Registering Custom Environments

```python
import pufferlib

# Register environment for easy access
pufferlib.register(
    id='my-custom-env',
    entry_point='my_package.envs:MyEnvironment',
    kwargs={'param1': 'value1'}
)

# Now can use with make
env = pufferlib.make('my-custom-env', num_envs=256)
```

### Registering in Ocean Suite

To add your environment to Ocean:

```python
# In ocean/environment.py
OCEAN_REGISTRY = {
    'my-env': {
        'entry_point': 'my_package.envs:MyEnvironment',
        'kwargs': {
            'default_param': 'default_value'
        }
    }
}
```

## Compatibility Patterns

### Gymnasium to PufferLib

```python
import gymnasium as gym
import pufferlib

# Standard Gymnasium environment
class GymEnv(gym.Env):
    def reset(self, seed=None, options=None):
        return observation, info

    def step(self, action):
        return observation, reward, terminated, truncated, info

# Convert to PufferEnv
puffer_env = pufferlib.emulate(GymEnv, num_envs=128)
```

### PettingZoo to PufferLib

```python
from pettingzoo import ParallelEnv
import pufferlib

# PettingZoo parallel environment
class PZEnv(ParallelEnv):
    def reset(self, seed=None, options=None):
        return {agent: obs for agent, obs in ...}, {agent: info for agent in ...}

    def step(self, actions):
        return observations, rewards, terminations, truncations, infos

# Convert to PufferEnv
puffer_env = pufferlib.emulate(PZEnv, num_envs=128)
```

### Legacy Gym (v0.21) to PufferLib

```python
import gym  # Old gym
import pufferlib

# Legacy gym environment (returns done instead of terminated/truncated)
class LegacyEnv(gym.Env):
    def reset(self):
        return observation

    def step(self, action):
        return observation, reward, done, info

# PufferLib handles legacy format automatically
puffer_env = pufferlib.emulate(LegacyEnv, num_envs=128)
```

## Performance Considerations

### Efficient Integration

```python
# Fast: Use built-in integrations when available
env = pufferlib.make('procgen-coinrun', num_envs=256)

# Slower: Generic wrapper (still fast, but overhead)
import gymnasium as gym
gym_env = gym.make('CartPole-v1')
env = pufferlib.emulate(gym_env, num_envs=256)

# Slowest: Nested wrappers add overhead
import gymnasium as gym
gym_env = gym.make('CartPole-v1')
gym_env = SomeWrapper(gym_env)
gym_env = AnotherWrapper(gym_env)
env = pufferlib.emulate(gym_env, num_envs=256)
```

### Minimize Wrapper Overhead

```python
# BAD: Too many wrappers
env = gym.make('CartPole-v1')
env = Wrapper1(env)
env = Wrapper2(env)
env = Wrapper3(env)
puffer_env = pufferlib.emulate(env, num_envs=256)

# GOOD: Combine wrapper logic
class CombinedWrapper(gym.Wrapper):
    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)
        # Apply all transformations at once
        obs = self._transform_obs(obs)
        reward = self._transform_reward(reward)
        return obs, reward, done, truncated, info

env = gym.make('CartPole-v1')
env = CombinedWrapper(env)
puffer_env = pufferlib.emulate(env, num_envs=256)
```

## Debugging Integration

### Verify Environment Compatibility

```python
def test_environment(env, num_steps=100):
    """Test environment for common issues."""
    # Test reset
    obs = env.reset()
    assert env.observation_space.contains(obs), "Invalid initial observation"

    # Test steps
    for _ in range(num_steps):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

        assert env.observation_space.contains(obs), "Invalid observation"
        assert isinstance(reward, (int, float)), "Invalid reward type"
        assert isinstance(done, bool), "Invalid done type"
        assert isinstance(info, dict), "Invalid info type"

        if done:
            obs = env.reset()

    print("✓ Environment passed compatibility test")

# Test before vectorizing
test_environment(MyEnvironment())
```

### Compare Outputs

```python
# Verify PufferLib emulation matches original
import gymnasium as gym
import pufferlib
import numpy as np

gym_env = gym.make('CartPole-v1')
puffer_env = pufferlib.emulate(lambda: gym.make('CartPole-v1'), num_envs=1)

# Test with same seed
gym_env.reset(seed=42)
puffer_obs = puffer_env.reset()

for _ in range(100):
    action = gym_env.action_space.sample()

    gym_obs, gym_reward, gym_done, gym_truncated, gym_info = gym_env.step(action)
    puffer_obs, puffer_reward, puffer_done, puffer_info = puffer_env.step(np.array([action]))

    # Compare outputs (accounting for batch dimension)
    assert np.allclose(gym_obs, puffer_obs[0])
    assert gym_reward == puffer_reward[0]
    assert gym_done == puffer_done[0]
```

---

## Reference: Policies

# PufferLib Policies Guide

## Overview

PufferLib policies are standard PyTorch modules with optional utilities for observation processing and LSTM integration. The framework provides default architectures and tools while allowing full flexibility in policy design.

## Policy Architecture

### Basic Policy Structure

```python
import torch
import torch.nn as nn
from pufferlib.pytorch import layer_init

class BasicPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        self.observation_space = observation_space
        self.action_space = action_space

        # Encoder network
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Policy head (actor)
        self.actor = layer_init(nn.Linear(256, action_space.n), std=0.01)

        # Value head (critic)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        """Forward pass through policy."""
        # Encode observations
        features = self.encoder(observations)

        # Get action logits and value
        logits = self.actor(features)
        value = self.critic(features)

        return logits, value

    def get_action(self, observations, deterministic=False):
        """Sample action from policy."""
        logits, value = self.forward(observations)

        if deterministic:
            action = logits.argmax(dim=-1)
        else:
            dist = torch.distributions.Categorical(logits=logits)
            action = dist.sample()

        return action, value
```

### Layer Initialization

PufferLib provides `layer_init` for proper weight initialization:

```python
from pufferlib.pytorch import layer_init

# Default orthogonal initialization
layer = layer_init(nn.Linear(256, 256))

# Custom standard deviation
actor_head = layer_init(nn.Linear(256, num_actions), std=0.01)
critic_head = layer_init(nn.Linear(256, 1), std=1.0)

# Works with any layer type
conv = layer_init(nn.Conv2d(3, 32, kernel_size=8, stride=4))
```

## CNN Policies

For image-based observations:

```python
class CNNPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # CNN encoder for images
        self.encoder = nn.Sequential(
            layer_init(nn.Conv2d(3, 32, kernel_size=8, stride=4)),
            nn.ReLU(),
            layer_init(nn.Conv2d(32, 64, kernel_size=4, stride=2)),
            nn.ReLU(),
            layer_init(nn.Conv2d(64, 64, kernel_size=3, stride=1)),
            nn.ReLU(),
            nn.Flatten(),
            layer_init(nn.Linear(64 * 7 * 7, 512)),
            nn.ReLU()
        )

        self.actor = layer_init(nn.Linear(512, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(512, 1), std=1.0)

    def forward(self, observations):
        # Normalize pixel values
        x = observations.float() / 255.0

        features = self.encoder(x)
        logits = self.actor(features)
        value = self.critic(features)

        return logits, value
```

### Efficient CNN Architecture

```python
class EfficientCNN(nn.Module):
    """Optimized CNN for Atari-style games."""

    def __init__(self, observation_space, action_space):
        super().__init__()

        in_channels = observation_space.shape[0]  # Typically 4 for framestack

        self.network = nn.Sequential(
            layer_init(nn.Conv2d(in_channels, 32, 8, stride=4)),
            nn.ReLU(),
            layer_init(nn.Conv2d(32, 64, 4, stride=2)),
            nn.ReLU(),
            layer_init(nn.Conv2d(64, 64, 3, stride=1)),
            nn.ReLU(),
            nn.Flatten()
        )

        # Calculate feature size
        with torch.no_grad():
            sample = torch.zeros(1, *observation_space.shape)
            n_features = self.network(sample).shape[1]

        self.fc = layer_init(nn.Linear(n_features, 512))
        self.actor = layer_init(nn.Linear(512, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(512, 1), std=1.0)

    def forward(self, x):
        x = x.float() / 255.0
        x = self.network(x)
        x = torch.relu(self.fc(x))

        return self.actor(x), self.critic(x)
```

## Recurrent Policies (LSTM)

PufferLib provides optimized LSTM integration with automatic recurrence handling:

```python
from pufferlib.pytorch import LSTMWrapper

class RecurrentPolicy(nn.Module):
    def __init__(self, observation_space, action_space, hidden_size=256):
        super().__init__()

        # Observation encoder
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 128)),
            nn.ReLU()
        )

        # LSTM layer
        self.lstm = nn.LSTM(128, hidden_size, num_layers=1)

        # Policy and value heads
        self.actor = layer_init(nn.Linear(hidden_size, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(hidden_size, 1), std=1.0)

        # Hidden state
        self.hidden_size = hidden_size

    def forward(self, observations, state=None):
        """
        Args:
            observations: (batch, obs_dim)
            state: Optional (h, c) tuple for LSTM

        Returns:
            logits, value, new_state
        """
        batch_size = observations.shape[0]

        # Encode observations
        features = self.encoder(observations)

        # Initialize hidden state if needed
        if state is None:
            h = torch.zeros(1, batch_size, self.hidden_size, device=features.device)
            c = torch.zeros(1, batch_size, self.hidden_size, device=features.device)
            state = (h, c)

        # LSTM forward
        features = features.unsqueeze(0)  # Add sequence dimension
        lstm_out, new_state = self.lstm(features, state)
        lstm_out = lstm_out.squeeze(0)

        # Get outputs
        logits = self.actor(lstm_out)
        value = self.critic(lstm_out)

        return logits, value, new_state
```

### LSTM Optimization

PufferLib's LSTM optimization uses LSTMCell during rollouts and LSTM during training for up to 3x faster inference:

```python
class OptimizedLSTMPolicy(nn.Module):
    def __init__(self, observation_space, action_space, hidden_size=256):
        super().__init__()

        self.encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 128)),
            nn.ReLU()
        )

        # Use LSTMCell for step-by-step inference
        self.lstm_cell = nn.LSTMCell(128, hidden_size)

        # Use LSTM for batch training
        self.lstm = nn.LSTM(128, hidden_size, num_layers=1)

        self.actor = layer_init(nn.Linear(hidden_size, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(hidden_size, 1), std=1.0)

        self.hidden_size = hidden_size

    def encode_observations(self, observations, state):
        """Fast inference using LSTMCell."""
        features = self.encoder(observations)

        if state is None:
            h = torch.zeros(observations.shape[0], self.hidden_size, device=features.device)
            c = torch.zeros(observations.shape[0], self.hidden_size, device=features.device)
        else:
            h, c = state

        # Step-by-step with LSTMCell (faster for inference)
        h, c = self.lstm_cell(features, (h, c))

        logits = self.actor(h)
        value = self.critic(h)

        return logits, value, (h, c)

    def decode_actions(self, observations, actions, state):
        """Batch training using LSTM."""
        seq_len, batch_size = observations.shape[:2]

        # Reshape for LSTM
        obs_flat = observations.reshape(seq_len * batch_size, -1)
        features = self.encoder(obs_flat)
        features = features.reshape(seq_len, batch_size, -1)

        if state is None:
            h = torch.zeros(1, batch_size, self.hidden_size, device=features.device)
            c = torch.zeros(1, batch_size, self.hidden_size, device=features.device)
            state = (h, c)

        # Batch processing with LSTM (faster for training)
        lstm_out, new_state = self.lstm(features, state)

        # Flatten back
        lstm_out = lstm_out.reshape(seq_len * batch_size, -1)

        logits = self.actor(lstm_out)
        value = self.critic(lstm_out)

        return logits, value, new_state
```

## Multi-Input Policies

For environments with multiple observation types:

```python
class MultiInputPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Separate encoders for different observation types
        self.image_encoder = nn.Sequential(
            layer_init(nn.Conv2d(3, 32, 8, stride=4)),
            nn.ReLU(),
            layer_init(nn.Conv2d(32, 64, 4, stride=2)),
            nn.ReLU(),
            nn.Flatten()
        )

        self.vector_encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space['vector'].shape[0], 128)),
            nn.ReLU()
        )

        # Combine features
        combined_size = 64 * 9 * 9 + 128  # Image features + vector features
        self.combiner = nn.Sequential(
            layer_init(nn.Linear(combined_size, 512)),
            nn.ReLU()
        )

        self.actor = layer_init(nn.Linear(512, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(512, 1), std=1.0)

    def forward(self, observations):
        # Process each observation type
        image_features = self.image_encoder(observations['image'].float() / 255.0)
        vector_features = self.vector_encoder(observations['vector'])

        # Combine
        combined = torch.cat([image_features, vector_features], dim=-1)
        features = self.combiner(combined)

        return self.actor(features), self.critic(features)
```

## Continuous Action Policies

For continuous control tasks:

```python
class ContinuousPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        self.encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

        # Mean of action distribution
        self.actor_mean = layer_init(nn.Linear(256, action_space.shape[0]), std=0.01)

        # Log std of action distribution
        self.actor_logstd = nn.Parameter(torch.zeros(1, action_space.shape[0]))

        # Value head
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        features = self.encoder(observations)

        action_mean = self.actor_mean(features)
        action_std = torch.exp(self.actor_logstd)

        value = self.critic(features)

        return action_mean, action_std, value

    def get_action(self, observations, deterministic=False):
        action_mean, action_std, value = self.forward(observations)

        if deterministic:
            return action_mean, value
        else:
            dist = torch.distributions.Normal(action_mean, action_std)
            action = dist.sample()
            return torch.tanh(action), value  # Bound actions to [-1, 1]
```

## Observation Processing

PufferLib provides utilities for unflattening observations:

```python
from pufferlib.pytorch import unflatten_observations

class PolicyWithUnflatten(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        self.observation_space = observation_space

        # Define encoders for each observation component
        self.encoders = nn.ModuleDict({
            'image': self._make_image_encoder(),
            'vector': self._make_vector_encoder()
        })

        # ... rest of policy ...

    def forward(self, flat_observations):
        # Unflatten observations into structured format
        observations = unflatten_observations(
            flat_observations,
            self.observation_space
        )

        # Process each component
        image_features = self.encoders['image'](observations['image'])
        vector_features = self.encoders['vector'](observations['vector'])

        # Combine and continue...
```

## Multi-Agent Policies

### Shared Parameters

All agents use the same policy:

```python
class SharedMultiAgentPolicy(nn.Module):
    def __init__(self, observation_space, action_space, num_agents):
        super().__init__()

        self.num_agents = num_agents

        # Single policy shared across all agents
        self.encoder = nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 256)),
            nn.ReLU()
        )

        self.actor = layer_init(nn.Linear(256, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def forward(self, observations):
        """
        Args:
            observations: (batch * num_agents, obs_dim)
        Returns:
            logits: (batch * num_agents, num_actions)
            values: (batch * num_agents, 1)
        """
        features = self.encoder(observations)
        return self.actor(features), self.critic(features)
```

### Independent Parameters

Each agent has its own policy:

```python
class IndependentMultiAgentPolicy(nn.Module):
    def __init__(self, observation_space, action_space, num_agents):
        super().__init__()

        self.num_agents = num_agents

        # Separate policy for each agent
        self.policies = nn.ModuleList([
            self._make_policy(observation_space, action_space)
            for _ in range(num_agents)
        ])

    def _make_policy(self, observation_space, action_space):
        return nn.Sequential(
            layer_init(nn.Linear(observation_space.shape[0], 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU()
        )

    def forward(self, observations, agent_ids):
        """
        Args:
            observations: (batch, obs_dim)
            agent_ids: (batch,) which agent each obs belongs to
        """
        outputs = []
        for agent_id in range(self.num_agents):
            mask = agent_ids == agent_id
            if mask.any():
                agent_obs = observations[mask]
                agent_out = self.policies[agent_id](agent_obs)
                outputs.append(agent_out)

        return torch.cat(outputs, dim=0)
```

## Advanced Architectures

### Attention-Based Policy

```python
class AttentionPolicy(nn.Module):
    def __init__(self, observation_space, action_space, d_model=256, nhead=8):
        super().__init__()

        self.encoder = layer_init(nn.Linear(observation_space.shape[0], d_model))

        self.attention = nn.MultiheadAttention(d_model, nhead, batch_first=True)

        self.actor = layer_init(nn.Linear(d_model, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(d_model, 1), std=1.0)

    def forward(self, observations):
        # Encode
        features = self.encoder(observations)

        # Self-attention
        features = features.unsqueeze(1)  # Add sequence dimension
        attn_out, _ = self.attention(features, features, features)
        attn_out = attn_out.squeeze(1)

        return self.actor(attn_out), self.critic(attn_out)
```

### Residual Policy

```python
class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            layer_init(nn.Linear(dim, dim)),
            nn.ReLU(),
            layer_init(nn.Linear(dim, dim))
        )

    def forward(self, x):
        return x + self.block(x)

class ResidualPolicy(nn.Module):
    def __init__(self, observation_space, action_space, num_blocks=4):
        super().__init__()

        dim = 256

        self.encoder = layer_init(nn.Linear(observation_space.shape[0], dim))

        self.blocks = nn.Sequential(
            *[ResidualBlock(dim) for _ in range(num_blocks)]
        )

        self.actor = layer_init(nn.Linear(dim, action_space.n), std=0.01)
        self.critic = layer_init(nn.Linear(dim, 1), std=1.0)

    def forward(self, observations):
        x = torch.relu(self.encoder(observations))
        x = self.blocks(x)
        return self.actor(x), self.critic(x)
```

## Policy Best Practices

### Initialization

```python
# Always use layer_init for proper initialization
good_layer = layer_init(nn.Linear(256, 256))

# Use small std for actor head (more stable early training)
actor = layer_init(nn.Linear(256, num_actions), std=0.01)

# Use std=1.0 for critic head
critic = layer_init(nn.Linear(256, 1), std=1.0)
```

### Observation Normalization

```python
class NormalizedPolicy(nn.Module):
    def __init__(self, observation_space, action_space):
        super().__init__()

        # Running statistics for normalization
        self.obs_mean = nn.Parameter(torch.zeros(observation_space.shape[0]), requires_grad=False)
        self.obs_std = nn.Parameter(torch.ones(observation_space.shape[0]), requires_grad=False)

        # ... rest of policy ...

    def forward(self, observations):
        # Normalize observations
        normalized_obs = (observations - self.obs_mean) / (self.obs_std + 1e-8)

        # Continue with normalized observations
        return self.policy(normalized_obs)

    def update_normalization(self, observations):
        """Update running statistics."""
        self.obs_mean.data = observations.mean(dim=0)
        self.obs_std.data = observations.std(dim=0)
```

### Gradient Clipping

```python
# PufferLib trainer handles gradient clipping automatically
trainer = PuffeRL(
    env=env,
    policy=policy,
    max_grad_norm=0.5  # Clip gradients to this norm
)
```

### Model Compilation

```python
# Enable torch.compile for faster training (PyTorch 2.0+)
policy = MyPolicy(observation_space, action_space)

# Compile the model
policy = torch.compile(policy, mode='reduce-overhead')

# Use with trainer
trainer = PuffeRL(env=env, policy=policy, compile=True)
```

## Debugging Policies

### Check Output Shapes

```python
def test_policy_shapes(policy, observation_space, batch_size=32):
    """Verify policy output shapes."""
    # Create dummy observations
    obs = torch.randn(batch_size, *observation_space.shape)

    # Forward pass
    logits, value = policy(obs)

    # Check shapes
    assert logits.shape == (batch_size, policy.action_space.n)
    assert value.shape == (batch_size, 1)

    print("✓ Policy shapes correct")
```

### Verify Gradients

```python
def check_gradients(policy, observation_space):
    """Check that gradients flow properly."""
    obs = torch.randn(1, *observation_space.shape, requires_grad=True)

    logits, value = policy(obs)

    # Backward pass
    loss = logits.sum() + value.sum()
    loss.backward()

    # Check gradients exist
    for name, param in policy.named_parameters():
        if param.grad is None:
            print(f"⚠ No gradient for {name}")
        elif torch.isnan(param.grad).any():
            print(f"⚠ NaN gradient for {name}")
        else:
            print(f"✓ Gradient OK for {name}")
```

---

## Reference: Training

# PufferLib Training Guide

## Overview

PuffeRL is PufferLib's high-performance training algorithm based on CleanRL's PPO with LSTMs, enhanced with proprietary research improvements. It achieves training at millions of steps per second through optimized vectorization and efficient implementation.

## Training Workflow

### Basic Training Loop

The PuffeRL trainer provides three core methods:

```python
# Collect environment interactions
rollout_data = trainer.evaluate()

# Train on collected batch
train_metrics = trainer.train()

# Aggregate and log results
trainer.mean_and_log()
```

### CLI Training

Quick start training via command line:

```bash
# Basic training
puffer train environment_name --train.device cuda --train.learning-rate 0.001

# Custom configuration
puffer train environment_name \
    --train.device cuda \
    --train.batch-size 32768 \
    --train.learning-rate 0.0003 \
    --train.num-iterations 10000
```

### Python Training Script

```python
import pufferlib
from pufferlib import PuffeRL

# Initialize environment
env = pufferlib.make('environment_name', num_envs=256)

# Create trainer
trainer = PuffeRL(
    env=env,
    policy=my_policy,
    device='cuda',
    learning_rate=3e-4,
    batch_size=32768,
    n_epochs=4,
    gamma=0.99,
    gae_lambda=0.95,
    clip_coef=0.2,
    ent_coef=0.01,
    vf_coef=0.5,
    max_grad_norm=0.5
)

# Training loop
for iteration in range(num_iterations):
    # Collect rollouts
    rollout_data = trainer.evaluate()

    # Train on batch
    train_metrics = trainer.train()

    # Log results
    trainer.mean_and_log()
```

## Key Training Parameters

### Core Hyperparameters

- **learning_rate**: Learning rate for optimizer (default: 3e-4)
- **batch_size**: Number of timesteps per training batch (default: 32768)
- **n_epochs**: Number of training epochs per batch (default: 4)
- **num_envs**: Number of parallel environments (default: 256)
- **num_steps**: Steps per environment per rollout (default: 128)

### PPO Parameters

- **gamma**: Discount factor (default: 0.99)
- **gae_lambda**: Lambda for GAE calculation (default: 0.95)
- **clip_coef**: PPO clipping coefficient (default: 0.2)
- **ent_coef**: Entropy coefficient for exploration (default: 0.01)
- **vf_coef**: Value function loss coefficient (default: 0.5)
- **max_grad_norm**: Maximum gradient norm for clipping (default: 0.5)

### Performance Parameters

- **device**: Computing device ('cuda' or 'cpu')
- **compile**: Use torch.compile for faster training (default: True)
- **num_workers**: Number of vectorization workers (default: auto)

## Distributed Training

### Multi-GPU Training

Use torchrun for distributed training across multiple GPUs:

```bash
torchrun --nproc_per_node=4 train.py \
    --train.device cuda \
    --train.batch-size 131072
```

### Multi-Node Training

For distributed training across multiple nodes:

```bash
# On main node (rank 0)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=0 \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py

# On worker nodes (rank 1, 2, 3)
torchrun --nproc_per_node=8 \
    --nnodes=4 \
    --node_rank=NODE_RANK \
    --master_addr=MASTER_IP \
    --master_port=29500 \
    train.py
```

## Monitoring and Logging

### Logger Integration

PufferLib supports multiple logging backends:

#### Weights & Biases

```python
from pufferlib import WandbLogger

logger = WandbLogger(
    project='my_project',
    entity='my_team',
    name='experiment_name',
    config=trainer_config
)

trainer = PuffeRL(env, policy, logger=logger)
```

#### Neptune

```python
from pufferlib import NeptuneLogger

logger = NeptuneLogger(
    project='my_team/my_project',
    name='experiment_name',
    api_token='YOUR_TOKEN'
)

trainer = PuffeRL(env, policy, logger=logger)
```

#### No Logger

```python
from pufferlib import NoLogger

trainer = PuffeRL(env, policy, logger=NoLogger())
```

### Key Metrics

Training logs include:

- **Performance Metrics**:
  - Steps per second (SPS)
  - Training throughput
  - Wall-clock time per iteration

- **Learning Metrics**:
  - Episode rewards (mean, min, max)
  - Episode lengths
  - Value function loss
  - Policy loss
  - Entropy
  - Explained variance
  - Clipfrac

- **Environment Metrics**:
  - Environment-specific rewards
  - Success rates
  - Custom metrics

### Terminal Dashboard

PufferLib provides a real-time terminal dashboard showing:
- Training progress
- Current SPS
- Episode statistics
- Loss values
- GPU utilization

## Checkpointing

### Saving Checkpoints

```python
# Save checkpoint
trainer.save_checkpoint('checkpoint.pt')

# Save with additional metadata
trainer.save_checkpoint(
    'checkpoint.pt',
    metadata={'iteration': iteration, 'best_reward': best_reward}
)
```

### Loading Checkpoints

```python
# Load checkpoint
trainer.load_checkpoint('checkpoint.pt')

# Resume training
for iteration in range(resume_iteration, num_iterations):
    trainer.evaluate()
    trainer.train()
    trainer.mean_and_log()
```

## Hyperparameter Tuning with Protein

The Protein system enables automatic hyperparameter and reward tuning:

```python
from pufferlib import Protein

# Define search space
search_space = {
    'learning_rate': [1e-4, 3e-4, 1e-3],
    'batch_size': [16384, 32768, 65536],
    'ent_coef': [0.001, 0.01, 0.1],
    'clip_coef': [0.1, 0.2, 0.3]
}

# Run hyperparameter search
protein = Protein(
    env_name='environment_name',
    search_space=search_space,
    num_trials=100,
    metric='mean_reward'
)

best_config = protein.optimize()
```

## Performance Optimization Tips

### Maximizing Throughput

1. **Batch Size**: Increase batch_size to fully utilize GPU
2. **Num Envs**: Balance between CPU and GPU utilization
3. **Compile**: Enable torch.compile for 10-20% speedup
4. **Workers**: Adjust num_workers based on environment complexity
5. **Device**: Always use 'cuda' for neural network training

### Environment Speed

- Pure Python environments: ~100k-500k SPS
- C-based environments: ~4M SPS
- With training overhead: ~1M-4M total SPS

### Memory Management

- Reduce batch_size if running out of GPU memory
- Decrease num_envs if running out of CPU memory
- Use gradient accumulation for large effective batch sizes

## Common Training Patterns

### Curriculum Learning

```python
# Start with easy tasks, gradually increase difficulty
difficulty_levels = [0.1, 0.3, 0.5, 0.7, 1.0]

for difficulty in difficulty_levels:
    env = pufferlib.make('environment_name', difficulty=difficulty)
    trainer = PuffeRL(env, policy)

    for iteration in range(iterations_per_level):
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

### Reward Shaping

```python
# Wrap environment with custom reward shaping
class RewardShapedEnv(pufferlib.PufferEnv):
    def step(self, actions):
        obs, rewards, dones, infos = super().step(actions)

        # Add shaped rewards
        shaped_rewards = rewards + 0.1 * proximity_bonus

        return obs, shaped_rewards, dones, infos
```

### Multi-Stage Training

```python
# Train in multiple stages with different configurations
stages = [
    {'learning_rate': 1e-3, 'iterations': 1000},   # Exploration
    {'learning_rate': 3e-4, 'iterations': 5000},   # Main training
    {'learning_rate': 1e-4, 'iterations': 2000}    # Fine-tuning
]

for stage in stages:
    trainer.learning_rate = stage['learning_rate']
    for iteration in range(stage['iterations']):
        trainer.evaluate()
        trainer.train()
        trainer.mean_and_log()
```

## Troubleshooting

### Low Performance

- Check environment is vectorized correctly
- Verify GPU utilization with `nvidia-smi`
- Increase batch_size to saturate GPU
- Enable compile mode
- Profile with `torch.profiler`

### Training Instability

- Reduce learning_rate
- Decrease batch_size
- Increase num_envs for more diverse samples
- Add entropy coefficient for more exploration
- Check reward scaling

### Memory Issues

- Reduce batch_size or num_envs
- Use gradient accumulation
- Disable compile mode if causing OOM
- Check for memory leaks in custom environments

---

## Reference: Vectorization

# PufferLib Vectorization Guide

## Overview

PufferLib's vectorization system enables high-performance parallel environment simulation, achieving millions of steps per second through optimized implementation inspired by EnvPool. The system supports both synchronous and asynchronous vectorization with minimal overhead.

## Vectorization Architecture

### Key Optimizations

1. **Shared Memory Buffer**: Single unified buffer across all environments (unlike Gymnasium's per-environment buffers)
2. **Busy-Wait Flags**: Workers busy-wait on unlocked flags rather than using pipes/queues
3. **Zero-Copy Batching**: Contiguous worker subsets return observations without copying
4. **Surplus Environments**: Simulates more environments than batch size for async returns
5. **Multiple Envs per Worker**: Optimizes performance for lightweight environments

### Performance Characteristics

- **Pure Python environments**: 100k-500k SPS
- **C-based environments**: 100M+ SPS
- **With training**: 400k-4M total SPS
- **Vectorization overhead**: <5% with optimal configuration

## Creating Vectorized Environments

### Basic Vectorization

```python
import pufferlib

# Automatic vectorization
env = pufferlib.make('environment_name', num_envs=256)

# With explicit configuration
env = pufferlib.make(
    'environment_name',
    num_envs=256,
    num_workers=8,
    envs_per_worker=32
)
```

### Manual Vectorization

```python
from pufferlib import PufferEnv
from pufferlib.vectorization import Serial, Multiprocessing

# Serial vectorization (single process)
vec_env = Serial(
    env_creator=lambda: MyEnvironment(),
    num_envs=16
)

# Multiprocessing vectorization
vec_env = Multiprocessing(
    env_creator=lambda: MyEnvironment(),
    num_envs=256,
    num_workers=8
)
```

## Vectorization Modes

### Serial Vectorization

Best for debugging and lightweight environments:

```python
from pufferlib.vectorization import Serial

vec_env = Serial(
    env_creator=env_creator_fn,
    num_envs=16
)

# All environments run in main process
# No multiprocessing overhead
# Easier debugging with standard tools
```

**When to use:**
- Development and debugging
- Very fast environments (< 1μs per step)
- Small number of environments (< 32)
- Single-threaded profiling

### Multiprocessing Vectorization

Best for most production use cases:

```python
from pufferlib.vectorization import Multiprocessing

vec_env = Multiprocessing(
    env_creator=env_creator_fn,
    num_envs=256,
    num_workers=8,
    envs_per_worker=32
)

# Parallel execution across workers
# True parallelism for CPU-bound environments
# Scales to hundreds of environments
```

**When to use:**
- Production training
- CPU-intensive environments
- Large-scale parallel simulation
- Maximizing throughput

### Async Vectorization

For environments with variable step times:

```python
vec_env = Multiprocessing(
    env_creator=env_creator_fn,
    num_envs=256,
    num_workers=8,
    mode='async',
    surplus_envs=32  # Simulate extra environments
)

# Returns batches as soon as ready
# Better GPU utilization
# Handles variable environment speeds
```

**When to use:**
- Variable environment step times
- Maximizing GPU utilization
- Network-based environments
- External simulators

## Optimizing Vectorization Performance

### Worker Configuration

```python
import multiprocessing

# Calculate optimal workers
num_cpus = multiprocessing.cpu_count()

# Conservative (leave headroom for training)
num_workers = num_cpus - 2

# Aggressive (maximize environment throughput)
num_workers = num_cpus

# With hyperthreading
num_workers = num_cpus // 2  # Physical cores only
```

### Envs Per Worker

```python
# Fast environments (< 10μs per step)
envs_per_worker = 64  # More envs per worker

# Medium environments (10-100μs per step)
envs_per_worker = 32  # Balanced

# Slow environments (> 100μs per step)
envs_per_worker = 16  # Fewer envs per worker

# Calculate from target batch size
batch_size = 32768
num_workers = 8
envs_per_worker = batch_size // num_workers
```

### Batch Size Tuning

```python
# Small batch (< 8k): Good for fast iteration
batch_size = 4096
num_envs = 256
steps_per_env = batch_size // num_envs  # 16 steps

# Medium batch (8k-32k): Good balance
batch_size = 16384
num_envs = 512
steps_per_env = 32

# Large batch (> 32k): Maximum throughput
batch_size = 65536
num_envs = 1024
steps_per_env = 64
```

## Shared Memory Optimization

### Buffer Management

PufferLib uses shared memory for zero-copy observation passing:

```python
import numpy as np
from multiprocessing import shared_memory

class OptimizedEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Environment will use provided shared buffer
        self.observation_space = self.make_space({'obs': (84, 84, 3)})

        # Observations written directly to shared memory
        self._obs_buffer = None

    def reset(self):
        # Write to shared memory in-place
        if self._obs_buffer is None:
            self._obs_buffer = np.zeros((84, 84, 3), dtype=np.uint8)

        self._render_to_buffer(self._obs_buffer)
        return {'obs': self._obs_buffer}

    def step(self, action):
        # In-place updates only
        self._update_state(action)
        self._render_to_buffer(self._obs_buffer)

        return {'obs': self._obs_buffer}, reward, done, info
```

### Zero-Copy Patterns

```python
# BAD: Creates copies
def get_observation(self):
    obs = np.zeros((84, 84, 3))
    # ... fill obs ...
    return obs.copy()  # Unnecessary copy!

# GOOD: Reuses buffer
def get_observation(self):
    # Use pre-allocated buffer
    self._render_to_buffer(self._obs_buffer)
    return self._obs_buffer  # No copy

# BAD: Allocates new arrays
def step(self, action):
    new_state = self.state + action  # Allocates
    self.state = new_state
    return obs, reward, done, info

# GOOD: In-place operations
def step(self, action):
    self.state += action  # In-place
    return obs, reward, done, info
```

## Advanced Vectorization

### Custom Vectorization

```python
from pufferlib.vectorization import VectorEnv

class CustomVectorEnv(VectorEnv):
    """Custom vectorization implementation."""

    def __init__(self, env_creator, num_envs, **kwargs):
        super().__init__()

        self.envs = [env_creator() for _ in range(num_envs)]
        self.num_envs = num_envs

    def reset(self):
        """Reset all environments."""
        observations = [env.reset() for env in self.envs]
        return self._stack_obs(observations)

    def step(self, actions):
        """Step all environments."""
        results = [env.step(action) for env, action in zip(self.envs, actions)]

        obs, rewards, dones, infos = zip(*results)

        return (
            self._stack_obs(obs),
            np.array(rewards),
            np.array(dones),
            list(infos)
        )

    def _stack_obs(self, observations):
        """Stack observations into batch."""
        return np.stack(observations, axis=0)
```

### Hierarchical Vectorization

For very large-scale parallelism:

```python
# Outer: Multiprocessing vectorization (8 workers)
# Inner: Each worker runs serial vectorization (32 envs)
# Total: 256 parallel environments

def create_serial_vec_env():
    return Serial(
        env_creator=lambda: MyEnvironment(),
        num_envs=32
    )

outer_vec_env = Multiprocessing(
    env_creator=create_serial_vec_env,
    num_envs=8,  # 8 serial vec envs
    num_workers=8
)

# Total environments: 8 * 32 = 256
```

## Multi-Agent Vectorization

### Native Multi-Agent Support

PufferLib treats multi-agent environments as first-class citizens:

```python
# Multi-agent environment automatically vectorized
env = pufferlib.make(
    'pettingzoo-knights-archers-zombies',
    num_envs=128,
    num_agents=4
)

# Observations: {agent_id: [batch_obs]} for each agent
# Actions: {agent_id: [batch_actions]} for each agent
# Rewards: {agent_id: [batch_rewards]} for each agent
```

### Custom Multi-Agent Vectorization

```python
class MultiAgentVectorEnv(VectorEnv):
    def step(self, actions):
        """
        Args:
            actions: Dict of {agent_id: [batch_actions]}

        Returns:
            observations: Dict of {agent_id: [batch_obs]}
            rewards: Dict of {agent_id: [batch_rewards]}
            dones: Dict of {agent_id: [batch_dones]}
            infos: List of dicts
        """
        # Distribute actions to environments
        env_actions = self._distribute_actions(actions)

        # Step each environment
        results = [env.step(act) for env, act in zip(self.envs, env_actions)]

        # Collect and batch results
        return self._batch_results(results)
```

## Performance Monitoring

### Profiling Vectorization

```python
import time

def profile_vectorization(vec_env, num_steps=10000):
    """Profile vectorization performance."""
    start = time.time()

    vec_env.reset()

    for _ in range(num_steps):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    elapsed = time.time() - start
    sps = (num_steps * vec_env.num_envs) / elapsed

    print(f"Steps per second: {sps:,.0f}")
    print(f"Time per step: {elapsed/num_steps*1000:.2f}ms")

    return sps
```

### Bottleneck Analysis

```python
import cProfile
import pstats

def analyze_bottlenecks(vec_env):
    """Identify vectorization bottlenecks."""
    profiler = cProfile.Profile()

    profiler.enable()

    vec_env.reset()
    for _ in range(1000):
        actions = vec_env.action_space.sample()
        vec_env.step(actions)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

### Real-Time Monitoring

```python
class MonitoredVectorEnv(VectorEnv):
    """Vector environment with performance monitoring."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.step_times = []
        self.step_count = 0

    def step(self, actions):
        start = time.perf_counter()

        result = super().step(actions)

        elapsed = time.perf_counter() - start
        self.step_times.append(elapsed)
        self.step_count += 1

        # Log every 1000 steps
        if self.step_count % 1000 == 0:
            mean_time = np.mean(self.step_times[-1000:])
            sps = self.num_envs / mean_time
            print(f"SPS: {sps:,.0f} | Step time: {mean_time*1000:.2f}ms")

        return result
```

## Troubleshooting

### Low Throughput

```python
# Check configuration
print(f"Num envs: {vec_env.num_envs}")
print(f"Num workers: {vec_env.num_workers}")
print(f"Envs per worker: {vec_env.num_envs // vec_env.num_workers}")

# Profile single environment
single_env = MyEnvironment()
single_sps = profile_single_env(single_env)
print(f"Single env SPS: {single_sps:,.0f}")

# Compare vectorized
vec_sps = profile_vectorization(vec_env)
print(f"Vectorized SPS: {vec_sps:,.0f}")
print(f"Speedup: {vec_sps / single_sps:.1f}x")
```

### Memory Issues

```python
# Reduce number of environments
num_envs = 128  # Instead of 256

# Reduce envs per worker
envs_per_worker = 16  # Instead of 32

# Use Serial mode for debugging
vec_env = Serial(env_creator, num_envs=16)
```

### Synchronization Problems

```python
# Ensure thread-safe operations
import threading

class ThreadSafeEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)
        self.lock = threading.Lock()

    def step(self, action):
        with self.lock:
            return super().step(action)
```

## Best Practices

### Configuration Guidelines

```python
# Start conservative
config = {
    'num_envs': 64,
    'num_workers': 4,
    'envs_per_worker': 16
}

# Scale up iteratively
config = {
    'num_envs': 256,     # 4x increase
    'num_workers': 8,     # 2x increase
    'envs_per_worker': 32 # 2x increase
}

# Monitor and adjust
if sps < target_sps:
    # Try increasing num_envs or num_workers
    pass
if memory_usage > threshold:
    # Reduce num_envs or envs_per_worker
    pass
```

### Environment Design

```python
# Minimize per-step allocations
class EfficientEnv(PufferEnv):
    def __init__(self, buf=None):
        super().__init__(buf)

        # Pre-allocate all buffers
        self._obs = np.zeros((84, 84, 3), dtype=np.uint8)
        self._state = np.zeros(10, dtype=np.float32)

    def step(self, action):
        # Use pre-allocated buffers
        self._update_state_inplace(action)
        self._render_to_obs()

        return self._obs, reward, done, info
```

### Testing

```python
# Test vectorization matches serial
serial_env = Serial(env_creator, num_envs=4)
vec_env = Multiprocessing(env_creator, num_envs=4, num_workers=2)

# Run parallel and verify results match
serial_env.seed(42)
vec_env.seed(42)

serial_obs = serial_env.reset()
vec_obs = vec_env.reset()

assert np.allclose(serial_obs, vec_obs), "Vectorization mismatch!"
```
