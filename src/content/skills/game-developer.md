---
title: "Game Developer"
description: "Use when building game systems, implementing Unity/Unreal Engine features, or optimizing game performance. Invoke to implement ECS architecture, configure physics systems and colliders, set up multiplayer networking with lag compensation, optimize..."
category: "development"
source: "community"
author: "Community"
tags: ["game", "developer"]
date: 2026-03-20
---

# Game Developer

## Core Workflow

1. **Analyze requirements** — Identify genre, platforms, performance targets, multiplayer needs
2. **Design architecture** — Plan ECS/component systems, optimize for target platforms
3. **Implement** — Build core mechanics, graphics, physics, AI, networking
4. **Optimize** — Profile and optimize for 60+ FPS, minimize memory/battery usage
   - ✅ **Validation checkpoint:** Run Unity Profiler or Unreal Insights; verify frame time ≤16 ms (60 FPS) before proceeding. Identify and resolve CPU/GPU bottlenecks iteratively.
5. **Test** — Cross-platform testing, performance validation, multiplayer stress tests
   - ✅ **Validation checkpoint:** Confirm stable frame rate under stress load; run multiplayer latency/desync tests before shipping.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Unity Development | `references/unity-patterns.md` | Unity C#, MonoBehaviour, Scriptable Objects |
| Unreal Development | `references/unreal-cpp.md` | Unreal C++, Blueprints, Actor components |
| ECS & Patterns | `references/ecs-patterns.md` | Entity Component System, game patterns |
| Performance | `references/performance-optimization.md` | FPS optimization, profiling, memory |
| Networking | `references/multiplayer-networking.md` | Multiplayer, client-server, lag compensation |

## Constraints

### MUST DO
- Target 60+ FPS on all platforms
- Use object pooling for frequent instantiation
- Implement LOD systems for optimization
- Profile performance regularly (CPU, GPU, memory)
- Use async loading for resources
- Implement proper state machines for game logic
- Cache component references (avoid GetComponent in Update)
- Use delta time for frame-independent movement

### MUST NOT DO
- Instantiate/Destroy in tight loops or Update()
- Skip profiling and performance testing
- Use string comparisons for tags (use CompareTag)
- Allocate memory in Update/FixedUpdate loops
- Ignore platform-specific constraints (mobile, console)
- Use Find methods in Update loops
- Hardcode game values (use ScriptableObjects/data files)

## Output Templates

When implementing game features, provide:
1. Core system implementation (ECS component, MonoBehaviour, or Actor)
2. Associated data structures (ScriptableObjects, structs, configs)
3. Performance considerations and optimizations
4. Brief explanation of architecture decisions

## Key Code Patterns

### Object Pooling (Unity C#)
```csharp
public class ObjectPool<T> where T : Component
{
    private readonly Queue<T> _pool = new();
    private readonly T _prefab;
    private readonly Transform _parent;

    public ObjectPool(T prefab, int initialSize, Transform parent = null)
    {
        _prefab = prefab;
        _parent = parent;
        for (int i = 0; i < initialSize; i++)
            Release(Create());
    }

    public T Get()
    {
        T obj = _pool.Count > 0 ? _pool.Dequeue() : Create();
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Release(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }

    private T Create() => Object.Instantiate(_prefab, _parent);
}
```

### Component Caching (Unity C#)
```csharp
public class PlayerController : MonoBehaviour
{
    // Cache all component references in Awake — never call GetComponent in Update
    private Rigidbody _rb;
    private Animator _animator;
    private PlayerInput _input;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _animator = GetComponent<Animator>();
        _input = GetComponent<PlayerInput>();
    }

    private void FixedUpdate()
    {
        // Use cached references; use deltaTime for frame-independence
        Vector3 move = _input.MoveDirection * (speed * Time.fixedDeltaTime);
        _rb.MovePosition(_rb.position + move);
    }
}
```

### State Machine (Unity C#)
```csharp
public abstract class State
{
    public abstract void Enter();
    public abstract void Tick(float deltaTime);
    public abstract void Exit();
}

public class StateMachine
{
    private State _current;

    public void TransitionTo(State next)
    {
        _current?.Exit();
        _current = next;
        _current.Enter();
    }

    public void Tick(float deltaTime) => _current?.Tick(deltaTime);
}

// Usage example
public class IdleState : State
{
    private readonly Animator _animator;
    public IdleState(Animator animator) => _animator = animator;
    public override void Enter() => _animator.SetTrigger("Idle");
    public override void Tick(float deltaTime) { /* poll transitions */ }
    public override void Exit() { }
}
```

---

## Reference: Ecs Patterns

# ECS Architecture and Game Patterns

## Entity Component System (ECS)

```csharp
// Component = pure data (no logic)
public struct PositionComponent
{
    public float X;
    public float Y;
    public float Z;
}

public struct VelocityComponent
{
    public float X;
    public float Y;
    public float Z;
}

public struct HealthComponent
{
    public int Current;
    public int Max;
}

public struct PlayerTag { } // Marker component

// Entity = just an ID
public struct Entity
{
    public int Id;
}

// System = logic operating on components
public class MovementSystem
{
    public void Update(float deltaTime,
        Span<PositionComponent> positions,
        Span<VelocityComponent> velocities)
    {
        for (int i = 0; i < positions.Length; i++)
        {
            positions[i].X += velocities[i].X * deltaTime;
            positions[i].Y += velocities[i].Y * deltaTime;
            positions[i].Z += velocities[i].Z * deltaTime;
        }
    }
}

// Simple ECS World
public class World
{
    private int nextEntityId = 0;
    private Dictionary<int, PositionComponent> positions = new();
    private Dictionary<int, VelocityComponent> velocities = new();
    private Dictionary<int, HealthComponent> healths = new();

    public Entity CreateEntity()
    {
        return new Entity { Id = nextEntityId++ };
    }

    public void AddComponent<T>(Entity entity, T component)
    {
        // Store component by entity ID
    }

    public T GetComponent<T>(Entity entity)
    {
        // Retrieve component for entity
        return default;
    }
}
```

## Object Pool Pattern

```csharp
public class ObjectPool<T> where T : class, new()
{
    private readonly Stack<T> pool = new();
    private readonly Func<T> createFunc;
    private readonly Action<T> resetAction;
    private readonly int maxSize;

    public ObjectPool(Func<T> createFunc, Action<T> resetAction, int initialSize = 10, int maxSize = 100)
    {
        this.createFunc = createFunc;
        this.resetAction = resetAction;
        this.maxSize = maxSize;

        // Pre-populate pool
        for (int i = 0; i < initialSize; i++)
        {
            pool.Push(createFunc());
        }
    }

    public T Get()
    {
        if (pool.Count > 0)
            return pool.Pop();

        return createFunc();
    }

    public void Return(T obj)
    {
        if (pool.Count < maxSize)
        {
            resetAction?.Invoke(obj);
            pool.Push(obj);
        }
    }
}

// Usage example
public class BulletManager
{
    private ObjectPool<Bullet> bulletPool;

    public void Initialize()
    {
        bulletPool = new ObjectPool<Bullet>(
            createFunc: () => new Bullet(),
            resetAction: (bullet) => bullet.Reset(),
            initialSize: 50,
            maxSize: 200
        );
    }

    public Bullet SpawnBullet()
    {
        Bullet bullet = bulletPool.Get();
        bullet.Activate();
        return bullet;
    }

    public void ReturnBullet(Bullet bullet)
    {
        bullet.Deactivate();
        bulletPool.Return(bullet);
    }
}
```

## State Machine Pattern

```csharp
public interface IState
{
    void Enter();
    void Update(float deltaTime);
    void Exit();
}

public class StateMachine
{
    private IState currentState;

    public void ChangeState(IState newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState?.Enter();
    }

    public void Update(float deltaTime)
    {
        currentState?.Update(deltaTime);
    }
}

// Example: Enemy AI States
public class IdleState : IState
{
    private readonly EnemyController enemy;

    public IdleState(EnemyController enemy) => this.enemy = enemy;

    public void Enter()
    {
        enemy.PlayAnimation("Idle");
    }

    public void Update(float deltaTime)
    {
        if (enemy.PlayerInRange())
            enemy.StateMachine.ChangeState(new ChaseState(enemy));
    }

    public void Exit() { }
}

public class ChaseState : IState
{
    private readonly EnemyController enemy;

    public ChaseState(EnemyController enemy) => this.enemy = enemy;

    public void Enter()
    {
        enemy.PlayAnimation("Run");
    }

    public void Update(float deltaTime)
    {
        if (!enemy.PlayerInRange())
            enemy.StateMachine.ChangeState(new IdleState(enemy));
        else if (enemy.InAttackRange())
            enemy.StateMachine.ChangeState(new AttackState(enemy));
        else
            enemy.MoveTowardsPlayer(deltaTime);
    }

    public void Exit() { }
}
```

## Command Pattern (Input Handling)

```csharp
public interface ICommand
{
    void Execute();
    void Undo();
}

public class MoveCommand : ICommand
{
    private readonly Transform transform;
    private readonly Vector3 movement;
    private Vector3 previousPosition;

    public MoveCommand(Transform transform, Vector3 movement)
    {
        this.transform = transform;
        this.movement = movement;
    }

    public void Execute()
    {
        previousPosition = transform.position;
        transform.position += movement;
    }

    public void Undo()
    {
        transform.position = previousPosition;
    }
}

public class InputHandler
{
    private Stack<ICommand> commandHistory = new();

    public void ExecuteCommand(ICommand command)
    {
        command.Execute();
        commandHistory.Push(command);
    }

    public void UndoLastCommand()
    {
        if (commandHistory.Count > 0)
        {
            ICommand command = commandHistory.Pop();
            command.Undo();
        }
    }
}
```

## Observer Pattern (Event System)

```csharp
public class GameEvent<T>
{
    private event Action<T> listeners;

    public void Subscribe(Action<T> listener)
    {
        listeners += listener;
    }

    public void Unsubscribe(Action<T> listener)
    {
        listeners -= listener;
    }

    public void Trigger(T data)
    {
        listeners?.Invoke(data);
    }
}

// Event hub
public static class GameEvents
{
    public static readonly GameEvent<int> OnScoreChanged = new();
    public static readonly GameEvent<float> OnHealthChanged = new();
    public static readonly GameEvent<string> OnGameOver = new();
}

// Subscriber
public class UIController
{
    private void OnEnable()
    {
        GameEvents.OnScoreChanged.Subscribe(UpdateScoreDisplay);
        GameEvents.OnHealthChanged.Subscribe(UpdateHealthBar);
    }

    private void OnDisable()
    {
        GameEvents.OnScoreChanged.Unsubscribe(UpdateScoreDisplay);
        GameEvents.OnHealthChanged.Unsubscribe(UpdateHealthBar);
    }

    private void UpdateScoreDisplay(int score)
    {
        // Update UI
    }

    private void UpdateHealthBar(float health)
    {
        // Update UI
    }
}

// Publisher
public class Player
{
    public void TakeDamage(float damage)
    {
        health -= damage;
        GameEvents.OnHealthChanged.Trigger(health);
    }
}
```

## Service Locator Pattern

```csharp
public static class ServiceLocator
{
    private static Dictionary<Type, object> services = new();

    public static void Register<T>(T service)
    {
        services[typeof(T)] = service;
    }

    public static T Get<T>()
    {
        if (services.TryGetValue(typeof(T), out object service))
            return (T)service;

        throw new Exception($"Service {typeof(T)} not found");
    }

    public static bool TryGet<T>(out T service)
    {
        if (services.TryGetValue(typeof(T), out object obj))
        {
            service = (T)obj;
            return true;
        }

        service = default;
        return false;
    }

    public static void Clear()
    {
        services.Clear();
    }
}

// Usage
public class GameInitializer
{
    public void Initialize()
    {
        ServiceLocator.Register<IAudioManager>(new AudioManager());
        ServiceLocator.Register<ISaveSystem>(new SaveSystem());
        ServiceLocator.Register<IInputManager>(new InputManager());
    }
}

public class Player
{
    private IAudioManager audioManager;

    public void Start()
    {
        audioManager = ServiceLocator.Get<IAudioManager>();
    }

    public void PlaySound(string soundName)
    {
        audioManager.PlaySound(soundName);
    }
}
```

## Spatial Partitioning (Grid)

```csharp
public class SpatialGrid<T>
{
    private readonly Dictionary<(int, int), List<T>> grid = new();
    private readonly float cellSize;

    public SpatialGrid(float cellSize)
    {
        this.cellSize = cellSize;
    }

    private (int, int) GetCell(Vector2 position)
    {
        int x = Mathf.FloorToInt(position.x / cellSize);
        int y = Mathf.FloorToInt(position.y / cellSize);
        return (x, y);
    }

    public void Insert(Vector2 position, T item)
    {
        var cell = GetCell(position);
        if (!grid.ContainsKey(cell))
            grid[cell] = new List<T>();

        grid[cell].Add(item);
    }

    public List<T> Query(Vector2 position, float radius)
    {
        List<T> results = new();
        int cellRadius = Mathf.CeilToInt(radius / cellSize);

        var centerCell = GetCell(position);

        for (int x = -cellRadius; x <= cellRadius; x++)
        {
            for (int y = -cellRadius; y <= cellRadius; y++)
            {
                var cell = (centerCell.Item1 + x, centerCell.Item2 + y);
                if (grid.TryGetValue(cell, out List<T> items))
                    results.AddRange(items);
            }
        }

        return results;
    }

    public void Clear()
    {
        grid.Clear();
    }
}
```

## Double Buffer Pattern (for Rendering/Physics)

```csharp
public class DoubleBuffer<T>
{
    private T[] buffers = new T[2];
    private int currentIndex = 0;

    public DoubleBuffer(T buffer1, T buffer2)
    {
        buffers[0] = buffer1;
        buffers[1] = buffer2;
    }

    public T Current => buffers[currentIndex];
    public T Next => buffers[1 - currentIndex];

    public void Swap()
    {
        currentIndex = 1 - currentIndex;
    }
}

// Usage for physics
public class PhysicsSimulation
{
    private DoubleBuffer<PhysicsState> stateBuffer;

    public void Update(float deltaTime)
    {
        // Read from current, write to next
        ComputeNextState(stateBuffer.Current, stateBuffer.Next, deltaTime);

        // Swap buffers
        stateBuffer.Swap();
    }
}
```

---

## Reference: Multiplayer Networking

# Multiplayer Networking

## Client-Server Architecture

```csharp
// Server-authoritative model
public class NetworkPlayer
{
    public int PlayerId { get; set; }
    public Vector3 Position { get; set; }
    public Quaternion Rotation { get; set; }
    public float Health { get; set; }

    // Server validates all actions
    public bool TryMove(Vector3 newPosition, float deltaTime)
    {
        float maxDistance = MoveSpeed * deltaTime * 1.1f; // 10% tolerance

        if (Vector3.Distance(Position, newPosition) > maxDistance)
        {
            // Client sent invalid movement - possible cheat
            return false;
        }

        Position = newPosition;
        return true;
    }
}

// Server
public class GameServer
{
    private Dictionary<int, NetworkPlayer> players = new();

    public void ProcessPlayerInput(int playerId, PlayerInput input)
    {
        if (!players.TryGetValue(playerId, out NetworkPlayer player))
            return;

        // Server processes input
        Vector3 newPosition = player.Position + input.Movement;

        if (player.TryMove(newPosition, Time.deltaTime))
        {
            // Broadcast to other clients
            BroadcastPlayerState(player);
        }
        else
        {
            // Send authoritative correction
            SendPositionCorrection(playerId, player.Position);
        }
    }
}
```

## State Synchronization

```csharp
// Network state with interpolation
public class NetworkTransform
{
    // Circular buffer for state history
    private struct State
    {
        public float Timestamp;
        public Vector3 Position;
        public Quaternion Rotation;
    }

    private State[] stateBuffer = new State[32];
    private int bufferIndex = 0;

    public void ReceiveState(float timestamp, Vector3 position, Quaternion rotation)
    {
        stateBuffer[bufferIndex] = new State
        {
            Timestamp = timestamp,
            Position = position,
            Rotation = rotation
        };

        bufferIndex = (bufferIndex + 1) % stateBuffer.Length;
    }

    public void Interpolate(float renderTime)
    {
        // Find two states to interpolate between
        State from = default;
        State to = default;

        for (int i = 0; i < stateBuffer.Length; i++)
        {
            if (stateBuffer[i].Timestamp <= renderTime)
                from = stateBuffer[i];
            else
            {
                to = stateBuffer[i];
                break;
            }
        }

        if (from.Timestamp == 0 || to.Timestamp == 0)
            return;

        // Interpolate between states
        float t = (renderTime - from.Timestamp) / (to.Timestamp - from.Timestamp);
        t = Mathf.Clamp01(t);

        transform.position = Vector3.Lerp(from.Position, to.Position, t);
        transform.rotation = Quaternion.Slerp(from.Rotation, to.Rotation, t);
    }
}
```

## Client-Side Prediction

```csharp
public class PredictivePlayer : MonoBehaviour
{
    private struct InputState
    {
        public int SequenceNumber;
        public float Timestamp;
        public Vector3 Movement;
    }

    private Queue<InputState> pendingInputs = new Queue<InputState>();
    private int sequenceNumber = 0;
    private Vector3 predictedPosition;

    void Update()
    {
        // Gather input
        Vector3 movement = new Vector3(
            Input.GetAxis("Horizontal"),
            0,
            Input.GetAxis("Vertical")
        ) * moveSpeed * Time.deltaTime;

        // Create input state
        InputState input = new InputState
        {
            SequenceNumber = sequenceNumber++,
            Timestamp = Time.time,
            Movement = movement
        };

        // Send to server
        SendInputToServer(input);

        // Apply locally (prediction)
        predictedPosition += movement;
        transform.position = predictedPosition;

        // Store for reconciliation
        pendingInputs.Enqueue(input);
    }

    public void ReceiveServerState(int lastProcessedInput, Vector3 serverPosition)
    {
        // Remove acknowledged inputs
        while (pendingInputs.Count > 0 && pendingInputs.Peek().SequenceNumber <= lastProcessedInput)
        {
            pendingInputs.Dequeue();
        }

        // Start from server position
        predictedPosition = serverPosition;

        // Replay pending inputs (reconciliation)
        foreach (var input in pendingInputs)
        {
            predictedPosition += input.Movement;
        }

        // Smooth correction if needed
        if (Vector3.Distance(transform.position, predictedPosition) > 0.1f)
        {
            // Snap or smooth based on distance
            transform.position = predictedPosition;
        }
    }
}
```

## Lag Compensation (Server-Side Rewind)

```csharp
public class LagCompensation
{
    private struct HistoricalState
    {
        public float Timestamp;
        public Vector3 Position;
        public Quaternion Rotation;
        public Bounds Hitbox;
    }

    private Dictionary<int, Queue<HistoricalState>> playerHistory = new();
    private const float MaxHistoryTime = 1.0f; // 1 second of history

    public void RecordState(int playerId, Vector3 position, Quaternion rotation, Bounds hitbox)
    {
        if (!playerHistory.ContainsKey(playerId))
            playerHistory[playerId] = new Queue<HistoricalState>();

        var queue = playerHistory[playerId];

        // Add current state
        queue.Enqueue(new HistoricalState
        {
            Timestamp = Time.time,
            Position = position,
            Rotation = rotation,
            Hitbox = hitbox
        });

        // Remove old states
        while (queue.Count > 0 && Time.time - queue.Peek().Timestamp > MaxHistoryTime)
        {
            queue.Dequeue();
        }
    }

    public bool ProcessHitscan(int shooterPlayerId, float clientTimestamp, Ray ray, out int hitPlayerId)
    {
        // Rewind to client's timestamp
        float targetTime = clientTimestamp; // Shooter's perceived time

        foreach (var kvp in playerHistory)
        {
            int playerId = kvp.Key;
            if (playerId == shooterPlayerId) continue; // Don't shoot self

            // Find state at target time
            HistoricalState state = GetStateAtTime(kvp.Value, targetTime);

            // Check raycast against historical hitbox
            if (state.Hitbox.IntersectRay(ray))
            {
                hitPlayerId = playerId;
                return true;
            }
        }

        hitPlayerId = -1;
        return false;
    }

    private HistoricalState GetStateAtTime(Queue<HistoricalState> history, float targetTime)
    {
        HistoricalState closest = default;
        float minDelta = float.MaxValue;

        foreach (var state in history)
        {
            float delta = Mathf.Abs(state.Timestamp - targetTime);
            if (delta < minDelta)
            {
                minDelta = delta;
                closest = state;
            }
        }

        return closest;
    }
}
```

## Network Message Serialization

```csharp
using System;
using System.IO;

// Efficient binary serialization
public class NetworkWriter
{
    private MemoryStream stream = new MemoryStream();
    private BinaryWriter writer;

    public NetworkWriter()
    {
        writer = new BinaryWriter(stream);
    }

    public void WriteInt(int value) => writer.Write(value);
    public void WriteFloat(float value) => writer.Write(value);
    public void WriteBool(bool value) => writer.Write(value);
    public void WriteString(string value) => writer.Write(value);

    public void WriteVector3(Vector3 value)
    {
        writer.Write(value.x);
        writer.Write(value.y);
        writer.Write(value.z);
    }

    // Compressed vector (16-bit per component)
    public void WriteVector3Compressed(Vector3 value, float min, float max)
    {
        writer.Write(CompressFloat(value.x, min, max));
        writer.Write(CompressFloat(value.y, min, max));
        writer.Write(CompressFloat(value.z, min, max));
    }

    private ushort CompressFloat(float value, float min, float max)
    {
        float normalized = Mathf.Clamp01((value - min) / (max - min));
        return (ushort)(normalized * ushort.MaxValue);
    }

    public byte[] ToArray() => stream.ToArray();
}

public class NetworkReader
{
    private BinaryReader reader;

    public NetworkReader(byte[] data)
    {
        reader = new BinaryReader(new MemoryStream(data));
    }

    public int ReadInt() => reader.ReadInt32();
    public float ReadFloat() => reader.ReadSingle();
    public bool ReadBool() => reader.ReadBoolean();
    public string ReadString() => reader.ReadString();

    public Vector3 ReadVector3()
    {
        return new Vector3(
            reader.ReadSingle(),
            reader.ReadSingle(),
            reader.ReadSingle()
        );
    }

    public Vector3 ReadVector3Compressed(float min, float max)
    {
        return new Vector3(
            DecompressFloat(reader.ReadUInt16(), min, max),
            DecompressFloat(reader.ReadUInt16(), min, max),
            DecompressFloat(reader.ReadUInt16(), min, max)
        );
    }

    private float DecompressFloat(ushort value, float min, float max)
    {
        float normalized = value / (float)ushort.MaxValue;
        return min + normalized * (max - min);
    }
}
```

## Interest Management (Relevancy)

```csharp
public class InterestManager
{
    private Dictionary<int, Vector3> playerPositions = new();
    private float relevancyRadius = 100f;

    public HashSet<int> GetRelevantPlayers(int playerId)
    {
        if (!playerPositions.TryGetValue(playerId, out Vector3 playerPos))
            return new HashSet<int>();

        HashSet<int> relevant = new HashSet<int>();

        foreach (var kvp in playerPositions)
        {
            if (kvp.Key == playerId) continue;

            float distance = Vector3.Distance(playerPos, kvp.Value);
            if (distance <= relevancyRadius)
            {
                relevant.Add(kvp.Key);
            }
        }

        return relevant;
    }

    public void BroadcastToRelevant(int senderId, byte[] message)
    {
        var recipients = GetRelevantPlayers(senderId);

        foreach (int recipientId in recipients)
        {
            SendMessage(recipientId, message);
        }
    }
}
```

## Delta Compression

```csharp
public class DeltaCompressor
{
    private Dictionary<int, NetworkPlayer> lastSentState = new();

    public byte[] CompressState(NetworkPlayer current)
    {
        if (!lastSentState.TryGetValue(current.PlayerId, out NetworkPlayer previous))
        {
            // First time - send full state
            return SerializeFullState(current);
        }

        NetworkWriter writer = new NetworkWriter();
        byte flags = 0;

        // Only send changed fields
        if (Vector3.Distance(current.Position, previous.Position) > 0.01f)
        {
            flags |= 1 << 0; // Position changed
            writer.WriteVector3Compressed(current.Position, -1000f, 1000f);
        }

        if (Quaternion.Angle(current.Rotation, previous.Rotation) > 1f)
        {
            flags |= 1 << 1; // Rotation changed
            writer.WriteQuaternionCompressed(current.Rotation);
        }

        if (Mathf.Abs(current.Health - previous.Health) > 0.1f)
        {
            flags |= 1 << 2; // Health changed
            writer.WriteFloat(current.Health);
        }

        // Prepend flags
        byte[] data = writer.ToArray();
        byte[] result = new byte[data.Length + 1];
        result[0] = flags;
        Array.Copy(data, 0, result, 1, data.Length);

        // Update last sent state
        lastSentState[current.PlayerId] = current;

        return result;
    }
}
```

## Network Performance Best Practices

**Bandwidth optimization:**
- Compress position/rotation data
- Use delta compression
- Implement relevancy system
- Limit update rate based on distance
- Batch multiple updates into single packet

**Latency optimization:**
- Client-side prediction for local player
- Server reconciliation for corrections
- Entity interpolation for other players
- Lag compensation for hitscan weapons

**Target metrics:**
- Latency: < 100ms
- Tick rate: 20-60 Hz (depends on game type)
- Packet size: < 1200 bytes (avoid fragmentation)
- Update rate: 10-20 Hz for distant objects, 60 Hz for nearby

**Security considerations:**
- Server-authoritative for all game logic
- Validate all client inputs
- Rate limiting to prevent flooding
- Encrypt sensitive data
- Anti-cheat measures (sanity checks, statistical analysis)

---

## Reference: Performance Optimization

# Performance Optimization

## Profiling First

```csharp
using UnityEngine.Profiling;

public class PerformanceMonitor : MonoBehaviour
{
    private void Update()
    {
        // CPU profiling
        Profiler.BeginSample("Enemy AI Update");
        UpdateEnemyAI();
        Profiler.EndSample();

        // Memory profiling
        long allocatedMemory = Profiler.GetTotalAllocatedMemoryLong();
        long reservedMemory = Profiler.GetTotalReservedMemoryLong();

        // FPS calculation
        float fps = 1.0f / Time.unscaledDeltaTime;
    }
}
```

## Memory Optimization

```csharp
// BAD: Allocates garbage every frame
void Update()
{
    string status = "Health: " + health + " / " + maxHealth; // Boxing + allocation
    Vector3 direction = transform.position - target.position; // Allocation
    var enemies = GameObject.FindGameObjectsWithTag("Enemy"); // Allocation
}

// GOOD: Zero allocations
private StringBuilder statusBuilder = new StringBuilder(50);
private Vector3 directionCache;
private List<Enemy> enemyCache = new List<Enemy>(100);

void Update()
{
    // Reuse StringBuilder
    statusBuilder.Clear();
    statusBuilder.Append("Health: ").Append(health).Append(" / ").Append(maxHealth);

    // Reuse Vector3
    directionCache = transform.position - target.position;

    // Cache references (done in Start)
    foreach (var enemy in enemyCache)
    {
        enemy.UpdateLogic();
    }
}
```

## Draw Call Batching

```csharp
// Static batching (for non-moving objects)
public class StaticBatchHelper : MonoBehaviour
{
    void Start()
    {
        // Mark objects as static in Inspector OR
        GameObject[] staticObjects = GameObject.FindGameObjectsWithTag("StaticProp");
        StaticBatchingUtility.Combine(staticObjects, gameObject);
    }
}

// Dynamic batching requirements:
// - Same material
// - Vertex count < 300
// - Same scale (non-uniform scale breaks batching)
// - No lightmaps

// GPU Instancing (for many identical objects)
// Add to shader: #pragma multi_compile_instancing
// Add to material: Enable GPU Instancing checkbox
// Use Graphics.DrawMeshInstanced or Graphics.RenderMeshInstanced
```

## LOD (Level of Detail) System

```csharp
using UnityEngine;

public class LODSetup : MonoBehaviour
{
    void SetupLOD()
    {
        LODGroup lodGroup = gameObject.AddComponent<LODGroup>();

        // LOD 0: 0% - 60% screen height (high detail)
        LOD[] lods = new LOD[3];
        lods[0] = new LOD(0.6f, GetRenderers("LOD0"));

        // LOD 1: 60% - 30% screen height (medium detail)
        lods[1] = new LOD(0.3f, GetRenderers("LOD1"));

        // LOD 2: 30% - 10% screen height (low detail)
        lods[2] = new LOD(0.1f, GetRenderers("LOD2"));

        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();
    }

    private Renderer[] GetRenderers(string lodName)
    {
        // Return renderers for specific LOD level
        return transform.Find(lodName).GetComponentsInChildren<Renderer>();
    }
}
```

## Occlusion Culling

```csharp
// Setup in Unity:
// 1. Mark static objects as "Occluder Static" and "Occludee Static"
// 2. Window > Rendering > Occlusion Culling
// 3. Bake occlusion data

// Runtime check
public class OcclusionCheck : MonoBehaviour
{
    private Camera mainCamera;

    void Start()
    {
        mainCamera = Camera.main;
    }

    void Update()
    {
        // Check if object is visible to camera
        Plane[] planes = GeometryUtility.CalculateFrustumPlanes(mainCamera);
        Bounds bounds = GetComponent<Renderer>().bounds;

        if (GeometryUtility.TestPlanesAABB(planes, bounds))
        {
            // Object is in camera frustum
            UpdateVisibleObject();
        }
    }
}
```

## Object Pooling (Performance-Focused)

```csharp
public class OptimizedPool<T> where T : Component
{
    private readonly Stack<T> available = new Stack<T>();
    private readonly HashSet<T> inUse = new HashSet<T>();
    private readonly T prefab;
    private readonly Transform parent;

    public OptimizedPool(T prefab, int initialSize, Transform parent = null)
    {
        this.prefab = prefab;
        this.parent = parent;

        // Pre-warm pool
        for (int i = 0; i < initialSize; i++)
        {
            T instance = Object.Instantiate(prefab, parent);
            instance.gameObject.SetActive(false);
            available.Push(instance);
        }
    }

    public T Get()
    {
        T instance;

        if (available.Count > 0)
        {
            instance = available.Pop();
        }
        else
        {
            // Pool exhausted, create new
            instance = Object.Instantiate(prefab, parent);
        }

        instance.gameObject.SetActive(true);
        inUse.Add(instance);
        return instance;
    }

    public void Return(T instance)
    {
        if (inUse.Remove(instance))
        {
            instance.gameObject.SetActive(false);
            available.Push(instance);
        }
    }

    public void Clear()
    {
        foreach (var instance in inUse)
            Object.Destroy(instance.gameObject);

        foreach (var instance in available)
            Object.Destroy(instance.gameObject);

        inUse.Clear();
        available.Clear();
    }
}
```

## Physics Optimization

```csharp
public class PhysicsOptimization : MonoBehaviour
{
    void Start()
    {
        // Use layers for collision filtering
        // Edit > Project Settings > Physics > Layer Collision Matrix

        // Use trigger colliders when possible (cheaper than collision)
        // Use simple collider shapes (sphere, box > capsule > mesh)

        // Disable unnecessary physics
        Rigidbody rb = GetComponent<Rigidbody>();
        rb.sleepThreshold = 0.1f; // Allow sleeping
        rb.interpolation = RigidbodyInterpolation.None; // Only if needed

        // Use fixed timestep wisely
        // Edit > Project Settings > Time > Fixed Timestep (default 0.02 = 50 fps)
    }

    // Raycasts: cache and limit
    private RaycastHit hitInfo;
    private float raycastInterval = 0.1f;
    private float nextRaycast;

    void Update()
    {
        if (Time.time >= nextRaycast)
        {
            // Use layers to filter raycasts
            int layerMask = 1 << LayerMask.NameToLayer("Ground");

            if (Physics.Raycast(transform.position, Vector3.down, out hitInfo, 10f, layerMask))
            {
                // Process hit
            }

            nextRaycast = Time.time + raycastInterval;
        }
    }
}
```

## Texture and Material Optimization

```csharp
// Texture atlasing
public class TextureAtlas : MonoBehaviour
{
    // Combine multiple textures into one atlas
    // Reduces draw calls significantly
    // Use Sprite Atlas or Texture Packer

    void PackTextures()
    {
        Texture2D[] textures = new Texture2D[10]; // Your textures
        Texture2D atlas = new Texture2D(2048, 2048);

        // Pack textures into atlas
        Rect[] uvs = atlas.PackTextures(textures, 2, 2048);

        // Update UV coordinates on meshes
    }
}

// Material sharing
public class MaterialSharing : MonoBehaviour
{
    void Start()
    {
        // BAD: Creates material instance
        Renderer renderer = GetComponent<Renderer>();
        renderer.material.color = Color.red; // Breaks batching!

        // GOOD: Share material
        Material sharedMat = renderer.sharedMaterial;
        // Modify material asset directly (affects all instances)
    }
}
```

## Update Optimization

```csharp
// Stagger updates to reduce per-frame cost
public class StaggeredUpdate : MonoBehaviour
{
    private static int updateOffset = 0;
    private int myOffset;

    void Start()
    {
        myOffset = updateOffset++;
    }

    void Update()
    {
        // Only update every 5th frame, staggered
        if ((Time.frameCount + myOffset) % 5 == 0)
        {
            ExpensiveUpdate();
        }
    }

    void ExpensiveUpdate()
    {
        // AI logic, pathfinding, etc.
    }
}

// Distance-based update rates
public class DistanceBasedUpdate : MonoBehaviour
{
    private Transform player;
    private float updateInterval;
    private float nextUpdate;

    void Update()
    {
        if (Time.time < nextUpdate) return;

        float distance = Vector3.Distance(transform.position, player.position);

        // Update more frequently when close
        if (distance < 10f)
            updateInterval = 0.05f; // 20 fps
        else if (distance < 50f)
            updateInterval = 0.1f; // 10 fps
        else
            updateInterval = 0.5f; // 2 fps

        PerformUpdate();
        nextUpdate = Time.time + updateInterval;
    }
}
```

## Async Loading

```csharp
using UnityEngine.SceneManagement;
using System.Collections;

public class AsyncLoader : MonoBehaviour
{
    public IEnumerator LoadSceneAsync(string sceneName)
    {
        AsyncOperation asyncLoad = SceneManager.LoadSceneAsync(sceneName);
        asyncLoad.allowSceneActivation = false;

        while (!asyncLoad.isDone)
        {
            // Loading progress
            float progress = Mathf.Clamp01(asyncLoad.progress / 0.9f);

            // When ready, activate
            if (asyncLoad.progress >= 0.9f)
            {
                // Wait for player input or fade completion
                yield return new WaitForSeconds(1f);
                asyncLoad.allowSceneActivation = true;
            }

            yield return null;
        }
    }

    public IEnumerator LoadAssetAsync<T>(string path) where T : Object
    {
        ResourceRequest request = Resources.LoadAsync<T>(path);

        while (!request.isDone)
        {
            yield return null;
        }

        T asset = request.asset as T;
        // Use asset
    }
}
```

## Performance Checklist

**Target: 60 FPS (16.67ms per frame)**

CPU Budget:
- Game logic: 5-7ms
- Rendering: 3-5ms
- Physics: 2-3ms
- Scripts: 2-3ms

Optimization priorities:
1. Profile first (Profiler, Frame Debugger)
2. Reduce draw calls (batching, instancing)
3. Optimize expensive Update loops
4. Use object pooling
5. Implement LOD systems
6. Enable occlusion culling
7. Optimize texture sizes and compression
8. Minimize garbage collection (allocations)
9. Use async loading
10. Implement distance-based update rates

---

## Reference: Unity Patterns

# Unity Development Patterns

## MonoBehaviour Best Practices

```csharp
using UnityEngine;
using System.Collections.Generic;

public class EnemyController : MonoBehaviour
{
    // Serialize private fields for Inspector
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private Transform target;

    // Cache component references
    private Rigidbody rb;
    private Animator animator;

    private void Awake()
    {
        // Cache components in Awake
        rb = GetComponent<Rigidbody>();
        animator = GetComponent<Animator>();
    }

    private void Start()
    {
        // Initialize after all Awake calls complete
        if (target == null)
            target = GameObject.FindGameObjectWithTag("Player").transform;
    }

    private void FixedUpdate()
    {
        // Physics calculations in FixedUpdate
        Vector3 direction = (target.position - transform.position).normalized;
        rb.MovePosition(transform.position + direction * moveSpeed * Time.fixedDeltaTime);
    }

    private void OnDisable()
    {
        // Clean up when disabled
        StopAllCoroutines();
    }
}
```

## ScriptableObjects for Data

```csharp
[CreateAssetMenu(fileName = "WeaponData", menuName = "Game/Weapon")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float fireRate;
    public GameObject projectilePrefab;
    public AudioClip fireSound;

    // Methods can contain logic
    public float GetDamageMultiplier(float distance)
    {
        return Mathf.Max(0.5f, 1f - (distance / 100f));
    }
}

// Usage in MonoBehaviour
public class Weapon : MonoBehaviour
{
    [SerializeField] private WeaponData weaponData;
    private float nextFireTime;

    public void Fire()
    {
        if (Time.time < nextFireTime) return;

        // Use data from ScriptableObject
        Instantiate(weaponData.projectilePrefab, transform.position, transform.rotation);
        nextFireTime = Time.time + 1f / weaponData.fireRate;
    }
}
```

## Object Pooling Pattern

```csharp
public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int poolSize = 20;

    private Queue<GameObject> pool = new Queue<GameObject>();

    private void Start()
    {
        // Pre-instantiate objects
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }

        // Expand pool if needed
        return Instantiate(prefab);
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}

// Pooled object example
public class Bullet : MonoBehaviour
{
    private ObjectPool pool;

    public void Initialize(ObjectPool pool)
    {
        this.pool = pool;
    }

    private void OnCollisionEnter(Collision collision)
    {
        // Return to pool instead of destroying
        pool.Return(gameObject);
    }
}
```

## Event System Pattern

```csharp
using System;
using UnityEngine.Events;

// Event definition
[Serializable]
public class HealthChangedEvent : UnityEvent<int, int> { } // current, max

public class Health : MonoBehaviour
{
    [SerializeField] private int maxHealth = 100;
    private int currentHealth;

    // UnityEvent visible in Inspector
    public HealthChangedEvent onHealthChanged;
    public UnityEvent onDeath;

    private void Start()
    {
        currentHealth = maxHealth;
        onHealthChanged?.Invoke(currentHealth, maxHealth);
    }

    public void TakeDamage(int damage)
    {
        currentHealth = Mathf.Max(0, currentHealth - damage);
        onHealthChanged?.Invoke(currentHealth, maxHealth);

        if (currentHealth <= 0)
            onDeath?.Invoke();
    }
}

// C# event alternative for performance
public static class GameEvents
{
    public static event Action<int> OnScoreChanged;
    public static event Action<string> OnGameOver;

    public static void TriggerScoreChanged(int score) => OnScoreChanged?.Invoke(score);
    public static void TriggerGameOver(string reason) => OnGameOver?.Invoke(reason);
}
```

## Coroutines Best Practices

```csharp
using System.Collections;

public class TimedAbility : MonoBehaviour
{
    // Cache WaitForSeconds to avoid GC
    private WaitForSeconds cooldownWait = new WaitForSeconds(5f);
    private Coroutine currentAbility;

    public void ActivateAbility()
    {
        // Stop previous coroutine if running
        if (currentAbility != null)
            StopCoroutine(currentAbility);

        currentAbility = StartCoroutine(AbilityCoroutine());
    }

    private IEnumerator AbilityCoroutine()
    {
        // Activate ability
        Debug.Log("Ability activated");

        // Wait for duration
        yield return cooldownWait;

        // Cooldown complete
        Debug.Log("Ability ready");
        currentAbility = null;
    }

    // Animation-based coroutine
    private IEnumerator LerpPosition(Vector3 target, float duration)
    {
        Vector3 start = transform.position;
        float elapsed = 0f;

        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float t = elapsed / duration;
            transform.position = Vector3.Lerp(start, target, t);
            yield return null; // Wait one frame
        }

        transform.position = target; // Ensure exact final position
    }
}
```

## Singleton Pattern (Use Sparingly)

```csharp
public class GameManager : MonoBehaviour
{
    private static GameManager instance;
    public static GameManager Instance => instance;

    private void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

## Performance Tips

- Cache `GetComponent<T>()` calls in Awake/Start
- Use `CompareTag()` instead of `tag == "TagName"`
- Use object pooling for frequently instantiated objects
- Avoid `Camera.main` in Update (cache the reference)
- Use `FixedUpdate` for physics, `Update` for input/logic
- Disable components instead of GameObjects when possible
- Use `StringBuilder` for string concatenation in loops

---

## Reference: Unreal Cpp

# Unreal Engine C++ Development

## Actor Component Pattern

```cpp
// Header file: MyCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MyCharacter.generated.h"

UCLASS()
class MYGAME_API AMyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMyCharacter();

protected:
    virtual void BeginPlay() override;

public:
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

private:
    // Exposed to Blueprints
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Movement", meta = (AllowPrivateAccess = "true"))
    float WalkSpeed = 600.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    class UCameraComponent* CameraComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    class USpringArmComponent* SpringArm;

    void MoveForward(float Value);
    void MoveRight(float Value);
};
```

```cpp
// Implementation: MyCharacter.cpp
#include "MyCharacter.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

AMyCharacter::AMyCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    // Create components
    SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
    SpringArm->SetupAttachment(RootComponent);
    SpringArm->TargetArmLength = 300.0f;
    SpringArm->bUsePawnControlRotation = true;

    CameraComponent = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    CameraComponent->SetupAttachment(SpringArm, USpringArmComponent::SocketName);
}

void AMyCharacter::BeginPlay()
{
    Super::BeginPlay();

    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
}

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis("MoveForward", this, &AMyCharacter::MoveForward);
    PlayerInputComponent->BindAxis("MoveRight", this, &AMyCharacter::MoveRight);
    PlayerInputComponent->BindAxis("Turn", this, &APawn::AddControllerYawInput);
    PlayerInputComponent->BindAxis("LookUp", this, &APawn::AddControllerPitchInput);
}

void AMyCharacter::MoveForward(float Value)
{
    if (Controller && Value != 0.0f)
    {
        const FRotator Rotation = Controller->GetControlRotation();
        const FRotator YawRotation(0, Rotation.Yaw, 0);
        const FVector Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
        AddMovementInput(Direction, Value);
    }
}
```

## Blueprint Callable Functions

```cpp
UCLASS()
class MYGAME_API UHealthComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHealthComponent();

protected:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Health")
    float MaxHealth = 100.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Health")
    float CurrentHealth;

    // Event dispatcher for Blueprint
    UPROPERTY(BlueprintAssignable, Category = "Health")
    FOnHealthChangedSignature OnHealthChanged;

public:
    // Callable from Blueprint
    UFUNCTION(BlueprintCallable, Category = "Health")
    void TakeDamage(float Damage);

    UFUNCTION(BlueprintCallable, Category = "Health")
    void Heal(float Amount);

    UFUNCTION(BlueprintPure, Category = "Health")
    float GetHealthPercent() const { return CurrentHealth / MaxHealth; }

    // Native event that can be overridden in Blueprint
    UFUNCTION(BlueprintNativeEvent, Category = "Health")
    void OnDeath();
    virtual void OnDeath_Implementation();
};

// Event delegate
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnHealthChangedSignature, float, Health, float, MaxHealth);
```

## Actor Component System

```cpp
// Custom Actor Component
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class MYGAME_API UInventoryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UInventoryComponent();

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY(EditAnywhere, Category = "Inventory")
    int32 MaxSlots = 20;

    UPROPERTY()
    TArray<class UItemData*> Items;

public:
    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool AddItem(UItemData* Item);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    bool RemoveItem(UItemData* Item);

    UFUNCTION(BlueprintPure, Category = "Inventory")
    int32 GetItemCount() const { return Items.Num(); }
};
```

## Timers and Async Operations

```cpp
class AWeapon : public AActor
{
private:
    FTimerHandle FireRateTimer;

    UPROPERTY(EditAnywhere, Category = "Weapon")
    float FireRate = 0.2f; // Seconds between shots

public:
    void StartFiring()
    {
        Fire(); // Immediate first shot
        GetWorldTimerManager().SetTimer(FireRateTimer, this, &AWeapon::Fire, FireRate, true);
    }

    void StopFiring()
    {
        GetWorldTimerManager().ClearTimer(FireRateTimer);
    }

    void Fire()
    {
        // Spawn projectile
        FVector Location = GetActorLocation();
        FRotator Rotation = GetActorRotation();
        GetWorld()->SpawnActor<AProjectile>(ProjectileClass, Location, Rotation);
    }
};
```

## Object Pooling in Unreal

```cpp
UCLASS()
class APooledActor : public AActor
{
    GENERATED_BODY()

private:
    bool bIsActive = false;

public:
    void Activate()
    {
        bIsActive = true;
        SetActorHiddenInGame(false);
        SetActorEnableCollision(true);
        SetActorTickEnabled(true);
    }

    void Deactivate()
    {
        bIsActive = false;
        SetActorHiddenInGame(true);
        SetActorEnableCollision(false);
        SetActorTickEnabled(false);
    }

    bool IsActive() const { return bIsActive; }
};

UCLASS()
class AObjectPool : public AActor
{
    GENERATED_BODY()

private:
    UPROPERTY(EditAnywhere, Category = "Pool")
    TSubclassOf<APooledActor> PooledClass;

    UPROPERTY(EditAnywhere, Category = "Pool")
    int32 PoolSize = 50;

    UPROPERTY()
    TArray<APooledActor*> Pool;

protected:
    virtual void BeginPlay() override
    {
        Super::BeginPlay();

        // Pre-spawn pool
        for (int32 i = 0; i < PoolSize; i++)
        {
            APooledActor* Actor = GetWorld()->SpawnActor<APooledActor>(PooledClass);
            Actor->Deactivate();
            Pool.Add(Actor);
        }
    }

public:
    APooledActor* GetPooledActor()
    {
        for (APooledActor* Actor : Pool)
        {
            if (!Actor->IsActive())
            {
                Actor->Activate();
                return Actor;
            }
        }

        // Expand pool if needed
        APooledActor* NewActor = GetWorld()->SpawnActor<APooledActor>(PooledClass);
        Pool.Add(NewActor);
        NewActor->Activate();
        return NewActor;
    }

    void ReturnToPool(APooledActor* Actor)
    {
        Actor->Deactivate();
    }
};
```

## Data Assets and Structures

```cpp
// Data structure
USTRUCT(BlueprintType)
struct FWeaponStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FName WeaponName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float Damage = 10.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    float FireRate = 0.5f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 MagazineSize = 30;
};

// Data asset
UCLASS()
class UWeaponDataAsset : public UDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
    FWeaponStats Stats;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
    TSubclassOf<class AProjectile> ProjectileClass;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
    USoundBase* FireSound;
};
```

## Smart Pointers

```cpp
// Use TSharedPtr for shared ownership
TSharedPtr<FGameData> GameData = MakeShared<FGameData>();

// Use TWeakPtr to avoid circular references
TWeakPtr<AActor> WeakActorRef = SharedActorPtr;

// Use TUniquePtr for exclusive ownership
TUniquePtr<FComplexSystem> System = MakeUnique<FComplexSystem>();
```

## Performance Best Practices

- Use `UPROPERTY()` for garbage collection (don't use raw pointers for UObjects)
- Cache component references in `BeginPlay()`
- Use `PrimaryActorTick.bCanEverTick = false` if Tick not needed
- Prefer Timers over Tick for periodic updates
- Use `BlueprintPure` for getter functions (no execution pin)
- Profile with Unreal Insights and stat commands (`stat fps`, `stat unit`, `stat game`)
- Use forward declarations in headers, includes in .cpp files
- Implement object pooling for frequently spawned actors
