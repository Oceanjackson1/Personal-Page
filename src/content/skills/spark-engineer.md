---
title: "Spark Engineer"
description: "Use when writing Spark jobs, debugging performance issues, or configuring cluster settings for Apache Spark applications, distributed data processing pipelines, or big data workloads. Invoke to write DataFrame transformations, optimize Spark SQL q..."
category: "devops"
source: "community"
author: "Community"
tags: ["spark", "engineer"]
date: 2026-03-20
---

# Spark Engineer

Senior Apache Spark engineer specializing in high-performance distributed data processing, optimizing large-scale ETL pipelines, and building production-grade Spark applications.

## Core Workflow

1. **Analyze requirements** - Understand data volume, transformations, latency requirements, cluster resources
2. **Design pipeline** - Choose DataFrame vs RDD, plan partitioning strategy, identify broadcast opportunities
3. **Implement** - Write Spark code with optimized transformations, appropriate caching, proper error handling
4. **Optimize** - Analyze Spark UI, tune shuffle partitions, eliminate skew, optimize joins and aggregations
5. **Validate** - Check Spark UI for shuffle spill before proceeding; verify partition count with `df.rdd.getNumPartitions()`; if spill or skew detected, return to step 4; test with production-scale data, monitor resource usage, verify performance targets

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Spark SQL & DataFrames | `references/spark-sql-dataframes.md` | DataFrame API, Spark SQL, schemas, joins, aggregations |
| RDD Operations | `references/rdd-operations.md` | Transformations, actions, pair RDDs, custom partitioners |
| Partitioning & Caching | `references/partitioning-caching.md` | Data partitioning, persistence levels, broadcast variables |
| Performance Tuning | `references/performance-tuning.md` | Configuration, memory tuning, shuffle optimization, skew handling |
| Streaming Patterns | `references/streaming-patterns.md` | Structured Streaming, watermarks, stateful operations, sinks |

## Code Examples

### Quick-Start Mini-Pipeline (PySpark)

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType

spark = SparkSession.builder \
    .appName("example-pipeline") \
    .config("spark.sql.shuffle.partitions", "400") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Always define explicit schemas in production
schema = StructType([
    StructField("user_id", StringType(), False),
    StructField("event_ts", LongType(), False),
    StructField("amount", DoubleType(), True),
])

df = spark.read.schema(schema).parquet("s3://bucket/events/")

result = df \
    .filter(F.col("amount").isNotNull()) \
    .groupBy("user_id") \
    .agg(F.sum("amount").alias("total_amount"), F.count("*").alias("event_count"))

# Verify partition count before writing
print(f"Partition count: {result.rdd.getNumPartitions()}")

result.write.mode("overwrite").parquet("s3://bucket/output/")
```

### Broadcast Join (small dimension table < 200 MB)

```python
from pyspark.sql.functions import broadcast

# Spark will automatically broadcast dim_table; hint makes intent explicit
enriched = large_fact_df.join(broadcast(dim_df), on="product_id", how="left")
```

### Handling Data Skew with Salting

```python
import pyspark.sql.functions as F

SALT_BUCKETS = 50

# Add salt to the skewed key on both sides
skewed_df = skewed_df.withColumn("salt", (F.rand() * SALT_BUCKETS).cast("int")) \
    .withColumn("salted_key", F.concat(F.col("skewed_key"), F.lit("_"), F.col("salt")))

other_df = other_df.withColumn("salt", F.explode(F.array([F.lit(i) for i in range(SALT_BUCKETS)]))) \
    .withColumn("salted_key", F.concat(F.col("skewed_key"), F.lit("_"), F.col("salt")))

result = skewed_df.join(other_df, on="salted_key", how="inner") \
    .drop("salt", "salted_key")
```

### Correct Caching Pattern

```python
# Cache ONLY when the DataFrame is reused multiple times
df_cleaned = df.filter(...).withColumn(...).cache()
df_cleaned.count()  # Materialize immediately; check Spark UI for spill

report_a = df_cleaned.groupBy("region").agg(...)
report_b = df_cleaned.groupBy("product").agg(...)

df_cleaned.unpersist()  # Release when done
```

## Constraints

### MUST DO
- Use DataFrame API over RDD for structured data processing
- Define explicit schemas for production pipelines
- Partition data appropriately (200-1000 partitions per executor core)
- Cache intermediate results only when reused multiple times
- Use broadcast joins for small dimension tables (<200MB)
- Handle data skew with salting or custom partitioning
- Monitor Spark UI for shuffle, spill, and GC metrics
- Test with production-scale data volumes

### MUST NOT DO
- Use collect() on large datasets (causes OOM)
- Skip schema definition and rely on inference in production
- Cache every DataFrame without measuring benefit
- Ignore shuffle partition tuning (default 200 often wrong)
- Use UDFs when built-in functions available (10-100x slower)
- Process small files without coalescing (small file problem)
- Run transformations without understanding lazy evaluation
- Ignore data skew warnings in Spark UI

## Output Templates

When implementing Spark solutions, provide:
1. Complete Spark code (PySpark or Scala) with type hints/types
2. Configuration recommendations (executors, memory, shuffle partitions)
3. Partitioning strategy explanation
4. Performance analysis (expected shuffle size, memory usage)
5. Monitoring recommendations (key Spark UI metrics to watch)

## Knowledge Reference

Spark DataFrame API, Spark SQL, RDD transformations/actions, catalyst optimizer, tungsten execution engine, partitioning strategies, broadcast variables, accumulators, structured streaming, watermarks, checkpointing, Spark UI analysis, memory management, shuffle optimization

---

## Reference: Partitioning Caching

# Partitioning and Caching

---

## Partitioning Fundamentals

### Why Partitioning Matters

- **Parallelism**: Each partition runs on a separate task
- **Data locality**: Minimize data movement across network
- **Memory efficiency**: Right-sized partitions prevent OOM
- **Join performance**: Co-partitioned data avoids shuffle

### Partition Count Guidelines

```python
# Rule of thumb: 2-4 partitions per CPU core
# For 100 executor cores: 200-400 partitions

# Check current partitions
print(f"Number of partitions: {df.rdd.getNumPartitions()}")

# Recommended formula
total_cores = num_executors * cores_per_executor
recommended_partitions = total_cores * 2 to 4

# Target partition size: 128MB - 256MB per partition
# For 100GB data with 128MB target: ~800 partitions
```

### Optimal Partition Sizes

| Data Volume | Target Partition Size | Partition Count |
|-------------|----------------------|-----------------|
| < 1GB | 64MB | 8-16 |
| 1-10GB | 128MB | 8-80 |
| 10-100GB | 128-256MB | 40-800 |
| 100GB-1TB | 256MB | 400-4000 |
| > 1TB | 256MB | 4000+ |

---

## DataFrame Partitioning

### Repartition (Full Shuffle)

```python
from pyspark.sql import functions as F

# Repartition to specific number
df_repart = df.repartition(200)

# Repartition by column(s) - same keys go to same partition
df_repart = df.repartition("user_id")
df_repart = df.repartition("user_id", "date")

# Repartition with count and columns
df_repart = df.repartition(100, "user_id")

# Range partitioning (for sorted access patterns)
df_range = df.repartitionByRange(100, "date")
```

```scala
// Scala repartition
val dfRepart = df.repartition(200)
val dfByCol = df.repartition($"user_id")
val dfRange = df.repartitionByRange(100, $"date")
```

### Coalesce (No Shuffle)

```python
# Reduce partitions without shuffle - efficient!
# Use after filtering reduces data significantly
df_coalesced = df.coalesce(50)

# Common pattern: filter then coalesce
df_filtered = df.filter(F.col("active") == True)
# If filter reduced data by 80%, reduce partitions too
df_optimized = df_filtered.coalesce(40)  # From 200 to 40
```

**When to use:**
- `repartition(n)`: Increase partitions, need even distribution, partition by column
- `coalesce(n)`: Decrease partitions only (no shuffle benefit)
- `repartitionByRange()`: Need sorted partitions for range queries

### Checking Partition Distribution

```python
from pyspark.sql import functions as F

# Check partition count
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Check partition sizes (row counts)
partition_counts = df.withColumn("partition_id", F.spark_partition_id()) \
    .groupBy("partition_id") \
    .count() \
    .orderBy("partition_id")

partition_counts.show()

# Get partition statistics
stats = partition_counts.agg(
    F.min("count").alias("min_rows"),
    F.max("count").alias("max_rows"),
    F.avg("count").alias("avg_rows"),
    F.stddev("count").alias("stddev")
)
stats.show()

# Identify skew: max/avg ratio > 3 indicates skew
```

---

## Shuffle Partitions

### Configuration

```python
# Default shuffle partitions (200) - often suboptimal
spark.conf.set("spark.sql.shuffle.partitions", 200)

# For small data (<10GB), reduce
spark.conf.set("spark.sql.shuffle.partitions", 50)

# For large data (>100GB), increase
spark.conf.set("spark.sql.shuffle.partitions", 2000)

# Adaptive Query Execution (Spark 3.0+) - dynamic partition sizing
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionSize", "64MB")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB")
```

### AQE Automatic Optimization (Spark 3.x)

```python
# Enable full AQE suite
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Auto-coalesce shuffle partitions
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.parallelismFirst", "false")

# Handle skewed partitions automatically
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", 5)
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# Local shuffle reader (avoid remote reads when possible)
spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")
```

**Spark UI Check:** With AQE, check "Adaptive" badge in SQL tab. View coalesced partition counts in stage details.

---

## Caching and Persistence

### When to Cache

**Cache when:**
- DataFrame is reused multiple times in same job
- DataFrame is expensive to compute (complex joins/aggregations)
- Iterative algorithms (ML training loops)
- Interactive exploration in notebooks

**Do NOT cache when:**
- DataFrame used only once
- Data doesn't fit in cluster memory
- Source data is already fast (local SSD, columnar formats)
- Storage level causes excessive GC

### Persistence Levels

```python
from pyspark import StorageLevel

# Memory only (default for cache())
df.cache()  # Equivalent to persist(MEMORY_AND_DISK)
df.persist()  # Same as cache()

# Specific storage levels
df.persist(StorageLevel.MEMORY_ONLY)         # Fast, may lose partitions
df.persist(StorageLevel.MEMORY_AND_DISK)     # Spill to disk if needed
df.persist(StorageLevel.MEMORY_ONLY_SER)     # Serialized, less memory, slower
df.persist(StorageLevel.MEMORY_AND_DISK_SER) # Serialized with disk spill
df.persist(StorageLevel.DISK_ONLY)           # Only disk, slowest
df.persist(StorageLevel.OFF_HEAP)            # Off-heap memory

# With replication (for fault tolerance)
df.persist(StorageLevel.MEMORY_AND_DISK_2)   # 2x replication

# Unpersist when done
df.unpersist()
df.unpersist(blocking=True)  # Wait for completion
```

```scala
// Scala persistence
import org.apache.spark.storage.StorageLevel

df.cache()
df.persist(StorageLevel.MEMORY_AND_DISK_SER)
df.unpersist()
```

### Storage Level Selection Guide

| Storage Level | Use When |
|---------------|----------|
| MEMORY_ONLY | Enough memory, need fastest access |
| MEMORY_AND_DISK | Default, safe for most cases |
| MEMORY_ONLY_SER | Memory constrained, CPU available |
| MEMORY_AND_DISK_SER | Large data, memory constrained |
| DISK_ONLY | Very large data, memory scarce |
| OFF_HEAP | Using Tungsten off-heap memory |

### Caching Best Practices

```python
# Pattern 1: Cache after expensive transformation
expensive_df = source_df \
    .join(lookup_df, "key") \
    .groupBy("category").agg(F.sum("amount"))

expensive_df.cache()

# Trigger caching with action
expensive_df.count()

# Reuse cached data
result1 = expensive_df.filter(F.col("category") == "A")
result2 = expensive_df.filter(F.col("category") == "B")

# Clean up
expensive_df.unpersist()

# Pattern 2: Cache at checkpoint in iterative algorithm
for iteration in range(100):
    df = df.transform(update_function)
    if iteration % 10 == 0:
        df.cache()
        df.count()  # Materialize
        df.unpersist()  # Clean previous

# Pattern 3: Checkpoint to break lineage (long pipelines)
spark.sparkContext.setCheckpointDir("hdfs://path/checkpoints/")
df.checkpoint()  # Truncates lineage, saves to reliable storage
```

### Monitoring Cache Usage

```python
# Check if DataFrame is cached
print(df.storageLevel)  # StorageLevel(False, False, False, False, 1) = not cached

# Check storage tab in Spark UI for:
# - Size in Memory
# - Size on Disk
# - Fraction Cached (should be 100%)
```

**Spark UI Check:** Storage tab shows cached RDDs/DataFrames. Monitor "Fraction Cached" - if < 100%, memory is insufficient.

---

## Broadcast Variables

### When to Use Broadcast

- Small lookup tables (< 200MB)
- Dimension tables joined to large fact tables
- Configuration data used across all tasks
- Avoiding shuffle in map-side joins

### DataFrame Broadcast Join

```python
from pyspark.sql.functions import broadcast

# Explicit broadcast hint
large_df = spark.read.parquet("s3://bucket/transactions/")  # 100GB
small_df = spark.read.parquet("s3://bucket/categories/")    # 50MB

# Broadcast small table for efficient join
result = large_df.join(broadcast(small_df), "category_id")

# Auto-broadcast threshold configuration
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 100 * 1024 * 1024)  # 100MB

# Disable auto-broadcast (force sort-merge join)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
```

### RDD Broadcast Variables

```python
# Create broadcast variable
lookup_dict = {"A": 1, "B": 2, "C": 3}
broadcast_lookup = spark.sparkContext.broadcast(lookup_dict)

# Use in transformation
def enrich_with_lookup(row):
    lookup = broadcast_lookup.value
    return Row(
        id=row.id,
        code=row.code,
        value=lookup.get(row.code, 0)
    )

enriched_rdd = df.rdd.map(enrich_with_lookup)

# Clean up
broadcast_lookup.unpersist()
broadcast_lookup.destroy()
```

### Broadcast Size Limits

```python
# Maximum broadcast size (default 8GB, adjustable)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 200 * 1024 * 1024)  # 200MB

# For larger broadcasts
spark.conf.set("spark.driver.maxResultSize", "4g")

# Monitor broadcast time in Spark UI
# Long broadcast time indicates table too large
```

**Warning:** Broadcasting tables > 200MB can cause driver OOM and slow broadcast. Use sort-merge join instead.

---

## Partitioning Strategies for Common Patterns

### Time-Series Data

```python
# Partition by date for time-range queries
df_partitioned = df.repartition("date")

# Range partition for ordered access
df_range = df.repartitionByRange(365, "date")  # One year

# Write partitioned by date
df.write.partitionBy("year", "month", "day").parquet("s3://bucket/data/")

# Read with partition pruning
df = spark.read.parquet("s3://bucket/data/") \
    .filter(F.col("year") == 2024)  # Only reads 2024 partitions
```

### User/Entity Data

```python
# Partition by user_id for user-specific queries
df_user_partitioned = df.repartition(1000, "user_id")

# Co-partition for efficient joins
users_partitioned = users.repartition(1000, "user_id")
orders_partitioned = orders.repartition(1000, "user_id")

# Join without shuffle (if partitioners match)
joined = users_partitioned.join(orders_partitioned, "user_id")
```

### Skewed Data

```python
# Salt skewed keys
salt_buckets = 10

# Add salt to skewed table
salted_df = large_df.withColumn(
    "salted_key",
    F.concat(
        F.col("join_key"),
        F.lit("_"),
        (F.monotonically_increasing_id() % salt_buckets).cast("string")
    )
)

# Explode small table to match
from pyspark.sql.functions import explode, array, lit

small_exploded = small_df.withColumn(
    "salt",
    explode(array([lit(i) for i in range(salt_buckets)]))
).withColumn(
    "salted_key",
    F.concat(F.col("join_key"), F.lit("_"), F.col("salt").cast("string"))
)

# Join on salted key
result = salted_df.join(small_exploded, "salted_key")
```

---

## File Partitioning (Write Optimization)

### Hive-Style Partitioning

```python
# Write with partitioning
df.write \
    .mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet("s3://bucket/data/")

# Result directory structure:
# s3://bucket/data/year=2024/month=01/part-*.parquet
# s3://bucket/data/year=2024/month=02/part-*.parquet

# Read with partition discovery
df = spark.read.parquet("s3://bucket/data/")
# Columns year, month automatically added from path
```

### Bucketing (Hash-Based File Partitioning)

```python
# Write bucketed table for optimized joins
df.write \
    .mode("overwrite") \
    .bucketBy(100, "user_id") \
    .sortBy("timestamp") \
    .saveAsTable("bucketed_orders")

# Read bucketed table
orders = spark.table("bucketed_orders")
users = spark.table("bucketed_users")  # Same bucket count

# Bucket join - no shuffle if buckets match
result = orders.join(users, "user_id")
```

**Note:** Bucketing requires Hive metastore and saveAsTable. Doesn't work with direct file writes.

### Controlling Output Files

```python
# Control number of output files
# One file per partition
df.coalesce(1).write.parquet("s3://bucket/output/")

# Multiple files per partition (for large partitions)
df.repartition(100).write.parquet("s3://bucket/output/")

# Max records per file
df.write \
    .option("maxRecordsPerFile", 1000000) \
    .parquet("s3://bucket/output/")
```

---

## Spark UI Analysis for Partitioning/Caching

### Jobs Tab

- Check if cached data shows "(cached)" in DAG
- Look for skipped stages (using cached data)

### Stages Tab

- **Shuffle Write Size**: Large values indicate repartition opportunities
- **Shuffle Read Size**: Should be similar across tasks (no skew)
- **Task Duration Distribution**: Wide variance indicates partition imbalance

### Storage Tab

- **Size in Memory**: Actual cached size
- **Size on Disk**: Spilled size
- **Fraction Cached**: Should be 100% if memory sufficient

### SQL Tab

- Look for "BroadcastExchange" - indicates broadcast join
- Look for "ShuffleExchange" - indicates data movement
- Check "Rows Output" at each stage for data flow

---

## Common Anti-Patterns

```python
# BAD: Caching without measuring benefit
for table in all_tables:
    spark.read.parquet(table).cache()  # Wastes memory

# GOOD: Cache only if reused
expensive_df.cache()
result1 = expensive_df.groupBy("a").count()
result2 = expensive_df.groupBy("b").count()
expensive_df.unpersist()

# BAD: Too many small partitions
df.repartition(10000)  # Creates scheduling overhead

# GOOD: Right-size partitions (128MB-256MB each)
df.repartition(100)

# BAD: Too few partitions for large data
df.coalesce(1)  # Single partition can't parallelize

# GOOD: Maintain parallelism
df.coalesce(max(1, target_size))

# BAD: Repartition before filter
df.repartition(1000).filter(F.col("active") == True)  # Shuffles then filters

# GOOD: Filter then coalesce
df.filter(F.col("active") == True).coalesce(100)  # Filter first, then resize

# BAD: Broadcasting large table
result = large.join(broadcast(also_large), "key")  # OOM risk

# GOOD: Let Spark decide or use sort-merge
result = large.join(also_large, "key")  # Sort-merge join
```

---

## Best Practices Summary

1. **Target 128-256MB partitions** - Not too small (overhead) or large (OOM)
2. **Use 2-4 partitions per core** - Maximize parallelism
3. **Enable AQE in Spark 3.x** - Automatic partition optimization
4. **Cache only reused DataFrames** - Measure before caching everything
5. **Use MEMORY_AND_DISK** - Safe default storage level
6. **Broadcast tables < 200MB** - Avoid shuffle for small dimension tables
7. **Coalesce after filters** - Reduce partitions when data shrinks
8. **Repartition for joins** - Co-partition related tables
9. **Partition writes by filter columns** - Enable partition pruning
10. **Monitor Storage tab** - Ensure cache fits in memory

---

## Reference: Performance Tuning

# Performance Tuning

---

## Cluster Sizing

### Executor Configuration

```python
# Key executor configurations
spark.conf.set("spark.executor.instances", 10)      # Number of executors
spark.conf.set("spark.executor.cores", 4)           # Cores per executor
spark.conf.set("spark.executor.memory", "16g")      # Memory per executor

# Dynamic allocation (recommended for varying workloads)
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", 2)
spark.conf.set("spark.dynamicAllocation.maxExecutors", 100)
spark.conf.set("spark.dynamicAllocation.executorIdleTimeout", "60s")
```

### Sizing Guidelines

| Cluster Size | Executor Memory | Executor Cores | Instances |
|--------------|-----------------|----------------|-----------|
| Small (dev) | 4-8GB | 2-4 | 2-5 |
| Medium | 8-16GB | 4-5 | 10-50 |
| Large | 16-32GB | 5-8 | 50-200 |
| Very Large | 32-64GB | 8-16 | 200+ |

**Rules of thumb:**
- 5 cores per executor is optimal (avoids HDFS I/O bottleneck)
- Leave 1 core per node for OS/YARN
- Leave 1GB per node for overhead
- executor.memoryOverhead = max(384MB, 10% of executor.memory)

### Memory Configuration

```python
# Executor memory breakdown
spark.conf.set("spark.executor.memory", "16g")
spark.conf.set("spark.executor.memoryOverhead", "2g")  # For off-heap, network buffers

# Memory fractions (default values usually good)
spark.conf.set("spark.memory.fraction", 0.6)           # Unified memory pool
spark.conf.set("spark.memory.storageFraction", 0.5)    # Cache vs execution split

# Off-heap memory (for large data)
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "8g")
```

---

## Shuffle Optimization

### Shuffle Configuration

```python
# Number of shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", 200)  # Adjust based on data size

# Shuffle behavior
spark.conf.set("spark.shuffle.compress", "true")              # Compress shuffle data
spark.conf.set("spark.shuffle.spill.compress", "true")        # Compress spill data
spark.conf.set("spark.io.compression.codec", "lz4")           # Fast compression

# Shuffle file management
spark.conf.set("spark.shuffle.file.buffer", "64k")            # Buffer for shuffle writes
spark.conf.set("spark.shuffle.io.maxRetries", 3)              # Retry failed fetches
spark.conf.set("spark.shuffle.io.retryWait", "5s")            # Wait between retries

# Sort-based shuffle (default in Spark 2.0+)
spark.conf.set("spark.shuffle.sort.bypassMergeThreshold", 200)
```

### Reducing Shuffle Size

```python
from pyspark.sql import functions as F

# 1. Filter before join/aggregation
df_filtered = df.filter(F.col("date") >= "2024-01-01")
result = df_filtered.groupBy("category").count()

# 2. Use broadcast for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")  # No shuffle for small_df

# 3. Select only needed columns before shuffle
df_slim = df.select("key", "value")  # Not all 50 columns
result = df_slim.groupBy("key").sum("value")

# 4. Use reduceByKey over groupByKey (RDD)
# BAD: groupByKey shuffles all values
counts = rdd.groupByKey().mapValues(len)
# GOOD: reduceByKey combines locally first
counts = rdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)

# 5. Coalesce after filter reduces data
df_filtered = df.filter(condition).coalesce(50)  # Reduce partitions without shuffle
```

### Spark UI Shuffle Metrics

In Stages tab, check:
- **Shuffle Write Size**: Total data written for shuffle
- **Shuffle Read Size**: Total data read from shuffle
- **Shuffle Read Blocked Time**: Time waiting for shuffle data
- **Shuffle Spill (Memory)**: Data spilled to memory
- **Shuffle Spill (Disk)**: Data spilled to disk (bad, increase memory)

---

## Data Skew Handling

### Identifying Skew

```python
from pyspark.sql import functions as F

# Check key distribution
key_counts = df.groupBy("join_key").count()
key_counts.orderBy(F.desc("count")).show(20)

# Summary statistics
stats = key_counts.agg(
    F.min("count").alias("min"),
    F.max("count").alias("max"),
    F.avg("count").alias("avg"),
    F.percentile_approx("count", 0.99).alias("p99")
)
stats.show()

# Skew ratio: max/avg > 10 indicates severe skew
```

**Spark UI indicators:**
- Few tasks taking much longer than others
- Task duration histogram shows long tail
- Some partitions much larger than others

### Skew Solutions

#### 1. Adaptive Query Execution (Spark 3.x)

```python
# Enable AQE skew handling
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", 5)
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# AQE will automatically split skewed partitions
result = large_df.join(another_df, "key")
```

#### 2. Salting Technique

```python
from pyspark.sql import functions as F

# Identify skewed keys
skewed_keys = ["NULL", "UNKNOWN", "DEFAULT"]
salt_buckets = 20

# Salt the skewed keys in large table
large_salted = large_df.withColumn(
    "salted_key",
    F.when(
        F.col("join_key").isin(skewed_keys),
        F.concat(F.col("join_key"), F.lit("_"), (F.rand() * salt_buckets).cast("int").cast("string"))
    ).otherwise(F.col("join_key"))
)

# Explode small table for skewed keys only
from pyspark.sql.functions import explode, array, lit, when

small_exploded = small_df.withColumn(
    "salted_key",
    F.when(
        F.col("join_key").isin(skewed_keys),
        F.explode(F.array([F.concat(F.col("join_key"), F.lit("_"), F.lit(i)) for i in range(salt_buckets)]))
    ).otherwise(F.col("join_key"))
)

# Join on salted key
result = large_salted.join(small_exploded, "salted_key")
```

#### 3. Broadcast Join for Skewed Keys

```python
from pyspark.sql.functions import broadcast

# Separate skewed and non-skewed data
skewed_keys = ["NULL", "UNKNOWN"]

large_skewed = large_df.filter(F.col("join_key").isin(skewed_keys))
large_normal = large_df.filter(~F.col("join_key").isin(skewed_keys))

small_skewed = small_df.filter(F.col("join_key").isin(skewed_keys))
small_normal = small_df.filter(~F.col("join_key").isin(skewed_keys))

# Broadcast join for skewed (small result expected)
result_skewed = large_skewed.join(broadcast(small_skewed), "join_key")

# Regular join for non-skewed
result_normal = large_normal.join(small_normal, "join_key")

# Union results
final_result = result_skewed.union(result_normal)
```

#### 4. Iterative Broadcast for Large Skewed Keys

```python
# For extremely skewed single keys
skewed_key_value = "NULL"

# Process skewed key separately with broadcast
skewed_large = large_df.filter(F.col("join_key") == skewed_key_value)
skewed_small = small_df.filter(F.col("join_key") == skewed_key_value)
result_skewed = skewed_large.crossJoin(broadcast(skewed_small))

# Process rest normally
normal_large = large_df.filter(F.col("join_key") != skewed_key_value)
normal_small = small_df.filter(F.col("join_key") != skewed_key_value)
result_normal = normal_large.join(normal_small, "join_key")

# Combine
final = result_skewed.union(result_normal)
```

---

## Memory Tuning

### Memory Pressure Symptoms

| Symptom | Cause | Solution |
|---------|-------|----------|
| Long GC pauses | Too much cached data | Reduce cache, use serialized storage |
| Spill to disk | Partitions too large | Increase partitions, add memory |
| OOM on driver | Large collect/broadcast | Reduce data to driver |
| OOM on executor | Large partitions | Repartition, increase memory |

### Garbage Collection Tuning

```python
# GC options (set via spark-submit --conf)
# For executor JVM
spark.conf.set("spark.executor.extraJavaOptions",
    "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:ConcGCThreads=4")

# For driver JVM
spark.conf.set("spark.driver.extraJavaOptions",
    "-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35")

# Monitor GC in Spark UI
# Executors tab shows GC Time for each executor
# Target: GC Time < 10% of total task time
```

### Reducing Memory Pressure

```python
# 1. Use serialized caching
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK_SER)

# 2. Kryo serialization (faster, more compact)
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# 3. Avoid UDFs that create objects
# BAD: Creates Python objects
@udf("string")
def process(x):
    return x.upper()  # String allocation

# GOOD: Use built-in
df.withColumn("upper", F.upper("column"))

# 4. Use mapPartitions with generators
def efficient_process(iterator):
    for row in iterator:
        yield transform(row)  # No list allocation

result = df.rdd.mapPartitions(efficient_process)

# 5. Release cached data promptly
df.unpersist()
```

### Driver Memory Issues

```python
# Increase driver memory
spark.conf.set("spark.driver.memory", "8g")
spark.conf.set("spark.driver.maxResultSize", "4g")

# Avoid large collects
# BAD
all_data = df.collect()  # Pulls everything to driver

# GOOD
sample = df.take(1000)  # Small sample
df.write.parquet("s3://output/")  # Write distributed
```

---

## Join Optimization

### Join Strategy Selection

```python
# Broadcast Hash Join - small table (< 200MB)
from pyspark.sql.functions import broadcast
result = large.join(broadcast(small), "key")

# Sort Merge Join - large tables, equi-join
# Default for non-broadcast joins
result = large1.join(large2, "key")

# Shuffle Hash Join - medium tables, memory-constrained
spark.conf.set("spark.sql.join.preferSortMergeJoin", "false")

# Cartesian Product - cross join (avoid if possible)
result = df1.crossJoin(df2)

# Bucket Join - pre-bucketed tables (no shuffle)
# Requires saveAsTable with bucketBy
```

### Join Hints (Spark 3.0+)

```python
# Broadcast hint
result = df1.join(df2.hint("broadcast"), "key")

# Shuffle merge hint
result = df1.hint("merge").join(df2, "key")

# Shuffle hash hint
result = df1.hint("shuffle_hash").join(df2, "key")

# Shuffle replicate NL hint (for small-large joins)
result = df1.hint("shuffle_replicate_nl").join(df2, "key")
```

### Checking Join Plan

```python
# View physical plan
df1.join(df2, "key").explain(True)

# Look for:
# - BroadcastHashJoin (best for small tables)
# - SortMergeJoin (good for large-large joins)
# - BroadcastNestedLoopJoin (avoid, expensive)
# - CartesianProduct (avoid unless intentional)
```

---

## I/O Optimization

### Reading Data

```python
# Parquet (best for Spark)
df = spark.read.parquet("s3://bucket/data/")

# Optimize Parquet reading
spark.conf.set("spark.sql.parquet.filterPushdown", "true")
spark.conf.set("spark.sql.parquet.mergeSchema", "false")  # Faster if schema consistent

# Partition pruning - filter on partition columns
df = spark.read.parquet("s3://bucket/data/") \
    .filter(F.col("date") >= "2024-01-01")  # Only reads matching partitions

# Column pruning - select only needed columns
df = spark.read.parquet("s3://bucket/data/").select("id", "name", "amount")

# Explicit schema (avoid inference)
df = spark.read.schema(my_schema).json("s3://bucket/data/")
```

### Writing Data

```python
# Optimal file sizes (128MB-256MB)
spark.conf.set("spark.sql.files.maxRecordsPerFile", 1000000)

# Compaction for small files
df.coalesce(100).write.parquet("s3://bucket/output/")

# Partitioned writes
df.write.partitionBy("date").parquet("s3://bucket/output/")

# Bucketed writes (requires Hive metastore)
df.write.bucketBy(100, "user_id").sortBy("timestamp").saveAsTable("table")

# Compression
df.write.option("compression", "snappy").parquet("s3://bucket/output/")
```

### Small File Problem

```python
# Detect small files
file_list = spark.sparkContext._jvm.org.apache.hadoop.fs.FileSystem \
    .get(spark.sparkContext._jsc.hadoopConfiguration()) \
    .listStatus(spark.sparkContext._jvm.org.apache.hadoop.fs.Path("s3://bucket/data/"))

# Compact small files
df = spark.read.parquet("s3://bucket/small_files/")
df.coalesce(optimal_partition_count).write.parquet("s3://bucket/compacted/")

# Or use repartition for even distribution
df.repartition(100).write.parquet("s3://bucket/compacted/")
```

---

## Spark UI Deep Dive

### Jobs Tab

- **Job Duration**: Identify slow jobs
- **Stages**: Number of stages (more stages = more shuffles)
- **DAG Visualization**: Understand data flow

### Stages Tab

| Metric | Healthy | Action if Abnormal |
|--------|---------|-------------------|
| Duration | < 5 min per stage | Break up large stages |
| Tasks | Even distribution | Address skew |
| Shuffle Write | Minimize | Filter earlier, select fewer columns |
| Shuffle Read Blocked Time | Near 0 | Check network, increase parallelism |
| Spill (Disk) | 0 | Increase memory or partitions |
| GC Time | < 10% of task time | Tune GC, reduce cached data |

### Executors Tab

- **Storage Memory**: Cache usage
- **Shuffle Read/Write**: I/O patterns
- **GC Time**: Garbage collection overhead
- **Failed Tasks**: Executor failures

### SQL Tab

- **Duration**: Query execution time
- **Details**: Physical plan details
- **Metrics**: Input/output rows at each stage

### Storage Tab

- **Cached RDDs/DataFrames**: Size and partition distribution
- **Fraction Cached**: Should be 100%

---

## Common Configuration Template

```python
# Production configuration template
spark_configs = {
    # Executor configuration
    "spark.executor.instances": 50,
    "spark.executor.cores": 5,
    "spark.executor.memory": "16g",
    "spark.executor.memoryOverhead": "2g",

    # Driver configuration
    "spark.driver.memory": "8g",
    "spark.driver.maxResultSize": "4g",

    # Shuffle configuration
    "spark.sql.shuffle.partitions": 500,
    "spark.shuffle.compress": "true",
    "spark.io.compression.codec": "lz4",

    # SQL optimization
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    "spark.sql.autoBroadcastJoinThreshold": str(200 * 1024 * 1024),  # 200MB

    # Serialization
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",

    # Dynamic allocation
    "spark.dynamicAllocation.enabled": "true",
    "spark.dynamicAllocation.minExecutors": 5,
    "spark.dynamicAllocation.maxExecutors": 100,
}

for key, value in spark_configs.items():
    spark.conf.set(key, value)
```

---

## Troubleshooting Decision Tree

```
Slow Spark Job
├── Long GC Time (> 10%)?
│   ├── Yes → Increase executor memory or reduce cache
│   └── No → Continue
├── Shuffle Spill to Disk?
│   ├── Yes → Increase partitions or memory
│   └── No → Continue
├── Uneven Task Duration?
│   ├── Yes → Data skew, use salting or AQE
│   └── No → Continue
├── Long Shuffle Read Time?
│   ├── Yes → Network bottleneck, increase locality
│   └── No → Continue
├── Large Shuffle Size?
│   ├── Yes → Filter earlier, broadcast small tables
│   └── No → Continue
└── Too Many Small Tasks?
    ├── Yes → Reduce partitions with coalesce
    └── No → Check for code-level optimizations
```

---

## Best Practices Summary

1. **Size executors appropriately** - 5 cores, 16GB memory typical
2. **Enable AQE (Spark 3.x)** - Automatic optimization for partitions and skew
3. **Tune shuffle partitions** - Based on data size, not default 200
4. **Address data skew** - Salt keys or use AQE automatic handling
5. **Monitor Spark UI** - Check shuffle, spill, GC metrics
6. **Use broadcast joins** - For tables under 200MB
7. **Filter and select early** - Reduce data before shuffle
8. **Avoid UDFs** - Use built-in functions (10-100x faster)
9. **Cache strategically** - Only reused data, unpersist when done
10. **Test at scale** - Performance varies significantly with data volume

---

## Reference: Rdd Operations

# RDD Operations

---

## When to Use RDDs

**Use RDDs when:**
- Processing unstructured data (raw text, custom binary formats)
- Need fine-grained control over physical data placement
- Implementing custom partitioning logic for specific access patterns
- Working with legacy Spark code that needs maintenance
- Building custom data structures not expressible as DataFrames

**Prefer DataFrames when:**
- Processing structured/semi-structured data
- Performing SQL-like operations
- Need Catalyst optimizer benefits
- Working with standard file formats (Parquet, JSON, ORC)

---

## RDD Creation

### From Collections

```python
# PySpark - Create RDD from Python collection
data = [1, 2, 3, 4, 5]
rdd = spark.sparkContext.parallelize(data, numSlices=4)  # 4 partitions

# From key-value pairs
pairs = [("a", 1), ("b", 2), ("c", 3)]
pair_rdd = spark.sparkContext.parallelize(pairs)
```

```scala
// Scala - Create RDD from collection
val data = Seq(1, 2, 3, 4, 5)
val rdd = spark.sparkContext.parallelize(data, numSlices = 4)

// From key-value pairs
val pairs = Seq(("a", 1), ("b", 2), ("c", 3))
val pairRdd = spark.sparkContext.parallelize(pairs)
```

### From Files

```python
# Text files - each line becomes an element
text_rdd = spark.sparkContext.textFile("hdfs://path/to/files/*.txt")

# Whole text files - each file as (filename, content) pair
files_rdd = spark.sparkContext.wholeTextFiles("hdfs://path/to/files/")

# Binary files
binary_rdd = spark.sparkContext.binaryFiles("hdfs://path/to/files/")

# Sequence files (Hadoop)
seq_rdd = spark.sparkContext.sequenceFile("hdfs://path/to/seqfile",
    "org.apache.hadoop.io.Text",
    "org.apache.hadoop.io.IntWritable")
```

### From DataFrame

```python
# Convert DataFrame to RDD of Rows
df = spark.read.parquet("s3://bucket/data/")
row_rdd = df.rdd

# Access Row fields
result_rdd = row_rdd.map(lambda row: (row.user_id, row.amount))

# Convert back to DataFrame
from pyspark.sql import Row
df_new = result_rdd.map(lambda x: Row(user_id=x[0], amount=x[1])).toDF()
```

---

## Transformations (Lazy)

Transformations return a new RDD and are not executed until an action is called.

### Basic Transformations

```python
# map - apply function to each element
squares = rdd.map(lambda x: x ** 2)

# flatMap - apply function returning iterator, flatten results
words = text_rdd.flatMap(lambda line: line.split(" "))

# filter - keep elements matching predicate
evens = rdd.filter(lambda x: x % 2 == 0)

# distinct - remove duplicates (causes shuffle)
unique = rdd.distinct()

# sample - random sample
sampled = rdd.sample(withReplacement=False, fraction=0.1, seed=42)

# union - combine two RDDs
combined = rdd1.union(rdd2)

# intersection - elements in both RDDs (causes shuffle)
common = rdd1.intersection(rdd2)

# subtract - elements in rdd1 not in rdd2 (causes shuffle)
diff = rdd1.subtract(rdd2)

# cartesian - all pairs (expensive!)
product = rdd1.cartesian(rdd2)
```

```scala
// Scala transformations
val squares = rdd.map(x => x * x)
val words = textRdd.flatMap(line => line.split(" "))
val evens = rdd.filter(_ % 2 == 0)
val unique = rdd.distinct()
val sampled = rdd.sample(withReplacement = false, fraction = 0.1, seed = 42L)
```

### MapPartitions (Efficient Batch Processing)

```python
# Process entire partition at once - more efficient than map
# Good for: database connections, expensive initialization, batch operations

def process_partition(iterator):
    # Initialize expensive resource once per partition
    connection = create_database_connection()
    try:
        for record in iterator:
            result = connection.process(record)
            yield result
    finally:
        connection.close()

result_rdd = rdd.mapPartitions(process_partition)

# With partition index
def process_with_index(partition_index, iterator):
    for record in iterator:
        yield (partition_index, record)

result_rdd = rdd.mapPartitionsWithIndex(process_with_index)
```

```scala
// Scala mapPartitions
val result = rdd.mapPartitions { iterator =>
  val connection = createDatabaseConnection()
  try {
    iterator.map(record => connection.process(record))
  } finally {
    connection.close()
  }
}
```

### Repartition and Coalesce

```python
# repartition - increase or decrease partitions (full shuffle)
rdd_repart = rdd.repartition(100)

# coalesce - decrease partitions only (avoids full shuffle)
rdd_coalesced = rdd.coalesce(10)  # Efficient reduction

# glom - collect each partition into an array
partitions = rdd.glom()  # RDD[Array[T]]
```

**When to use:**
- `repartition(n)`: When increasing partitions or need even distribution
- `coalesce(n)`: When decreasing partitions (after filter reduced data)

---

## Pair RDD Operations

Pair RDDs (key-value pairs) enable powerful transformations.

### Creating Pair RDDs

```python
# From tuples
pair_rdd = rdd.map(lambda x: (x.key, x.value))

# keyBy - create pairs from existing elements
pair_rdd = rdd.keyBy(lambda x: x.user_id)
```

### Transformations on Pair RDDs

```python
# reduceByKey - aggregate values by key (more efficient than groupByKey)
counts = pair_rdd.reduceByKey(lambda a, b: a + b)

# groupByKey - group all values for each key (shuffles all data!)
grouped = pair_rdd.groupByKey()  # Avoid when possible

# aggregateByKey - combine with different local/global combiners
sum_count = pair_rdd.aggregateByKey(
    zeroValue=(0, 0),  # (sum, count)
    seqFunc=lambda acc, v: (acc[0] + v, acc[1] + 1),  # within partition
    combFunc=lambda a, b: (a[0] + b[0], a[1] + b[1])  # across partitions
)

# combineByKey - most general aggregation
averages = pair_rdd.combineByKey(
    createCombiner=lambda v: (v, 1),
    mergeValue=lambda acc, v: (acc[0] + v, acc[1] + 1),
    mergeCombiners=lambda a, b: (a[0] + b[0], a[1] + b[1])
).mapValues(lambda x: x[0] / x[1])

# mapValues - transform values only (preserves partitioning)
doubled = pair_rdd.mapValues(lambda v: v * 2)

# flatMapValues - flatMap on values only
expanded = pair_rdd.flatMapValues(lambda v: range(v))

# keys and values
keys_rdd = pair_rdd.keys()
values_rdd = pair_rdd.values()

# sortByKey
sorted_rdd = pair_rdd.sortByKey(ascending=True)

# join operations (all cause shuffle)
joined = rdd1.join(rdd2)              # inner join
left = rdd1.leftOuterJoin(rdd2)       # left outer
right = rdd1.rightOuterJoin(rdd2)     # right outer
full = rdd1.fullOuterJoin(rdd2)       # full outer
cogroup = rdd1.cogroup(rdd2)          # group by key from both RDDs

# subtractByKey - remove keys present in other RDD
filtered = rdd1.subtractByKey(rdd2)
```

```scala
// Scala pair RDD operations
val counts = pairRdd.reduceByKey(_ + _)
val grouped = pairRdd.groupByKey()  // Avoid when possible

val averages = pairRdd.combineByKey(
  (v: Int) => (v, 1),
  (acc: (Int, Int), v: Int) => (acc._1 + v, acc._2 + 1),
  (a: (Int, Int), b: (Int, Int)) => (a._1 + b._1, a._2 + b._2)
).mapValues { case (sum, count) => sum.toDouble / count }

val joined = rdd1.join(rdd2)
```

### reduceByKey vs groupByKey

```python
# BAD: groupByKey shuffles all values
# Memory-intensive, can cause OOM
word_counts = words.map(lambda w: (w, 1)).groupByKey().mapValues(sum)

# GOOD: reduceByKey combines locally first
# Much more efficient, less data shuffled
word_counts = words.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
```

**Spark UI Check:** Compare shuffle write sizes. `reduceByKey` should show much smaller shuffle than `groupByKey` for the same operation.

---

## Actions (Trigger Execution)

Actions return values to the driver or write to storage.

### Collection Actions

```python
# collect - return all elements to driver (OOM risk!)
all_data = rdd.collect()  # Use carefully on large RDDs

# take - return first n elements
first_10 = rdd.take(10)

# takeOrdered - return smallest/largest n elements
smallest_5 = rdd.takeOrdered(5)  # ascending
largest_5 = rdd.takeOrdered(5, key=lambda x: -x)

# takeSample - random sample
sample = rdd.takeSample(withReplacement=False, num=100, seed=42)

# first - return first element
first = rdd.first()

# top - return largest n elements
top_5 = rdd.top(5)

# count - count elements
total = rdd.count()

# countByKey - count elements per key (returns dict to driver)
key_counts = pair_rdd.countByKey()

# countByValue - count occurrences of each value
value_counts = rdd.countByValue()
```

### Aggregation Actions

```python
# reduce - aggregate all elements
total = rdd.reduce(lambda a, b: a + b)

# fold - reduce with zero value
total = rdd.fold(0, lambda a, b: a + b)

# aggregate - combine with different types
stats = rdd.aggregate(
    zeroValue=(0, 0),  # (sum, count)
    seqOp=lambda acc, v: (acc[0] + v, acc[1] + 1),
    combOp=lambda a, b: (a[0] + b[0], a[1] + b[1])
)
average = stats[0] / stats[1]
```

### Output Actions

```python
# saveAsTextFile - save as text files
rdd.saveAsTextFile("hdfs://path/output/")

# saveAsSequenceFile - save as Hadoop sequence file
pair_rdd.saveAsSequenceFile("hdfs://path/output/")

# saveAsPickleFile - Python pickle format
rdd.saveAsPickleFile("hdfs://path/output/")

# foreach - apply function to each element (side effects)
rdd.foreach(lambda x: print(x))  # Runs on executors

# foreachPartition - apply function to each partition
def save_partition(iterator):
    connection = create_connection()
    for record in iterator:
        connection.save(record)
    connection.close()

rdd.foreachPartition(save_partition)
```

---

## Custom Partitioners

### Implementing Custom Partitioner

```python
from pyspark import Partitioner

class RangePartitioner(Partitioner):
    def __init__(self, ranges):
        """
        ranges: list of (min, max) tuples defining partition boundaries
        """
        self.ranges = ranges

    def numPartitions(self):
        return len(self.ranges)

    def getPartition(self, key):
        for i, (min_val, max_val) in enumerate(self.ranges):
            if min_val <= key < max_val:
                return i
        return len(self.ranges) - 1  # Default to last partition

# Use custom partitioner
ranges = [(0, 100), (100, 500), (500, 1000), (1000, float('inf'))]
partitioner = RangePartitioner(ranges)
partitioned_rdd = pair_rdd.partitionBy(partitioner.numPartitions(), partitioner.getPartition)
```

```scala
// Scala custom partitioner
import org.apache.spark.Partitioner

class DomainPartitioner(numParts: Int) extends Partitioner {
  override def numPartitions: Int = numParts

  override def getPartition(key: Any): Int = {
    val domain = key.asInstanceOf[String].split("@")(1)
    math.abs(domain.hashCode % numPartitions)
  }

  override def equals(other: Any): Boolean = other match {
    case p: DomainPartitioner => p.numPartitions == numPartitions
    case _ => false
  }
}

val partitioned = pairRdd.partitionBy(new DomainPartitioner(10))
```

### Hash Partitioner (Default)

```python
from pyspark import HashPartitioner

# Repartition with hash partitioner
partitioned_rdd = pair_rdd.partitionBy(100)  # Uses HashPartitioner

# Preserve partitioning across transformations
# mapValues and flatMapValues preserve partitioner
preserved = partitioned_rdd.mapValues(lambda v: v * 2)
assert preserved.partitioner == partitioned_rdd.partitioner

# map does NOT preserve partitioner
not_preserved = partitioned_rdd.map(lambda x: (x[0], x[1] * 2))
assert not_preserved.partitioner is None
```

---

## Broadcast Variables and Accumulators

### Broadcast Variables

```python
# Broadcast large read-only data to all executors
lookup_table = {"a": 1, "b": 2, "c": 3}  # Small example
lookup_broadcast = spark.sparkContext.broadcast(lookup_table)

def enrich_record(record):
    table = lookup_broadcast.value  # Access broadcast value
    return (record, table.get(record, 0))

enriched_rdd = rdd.map(enrich_record)

# Clean up when done
lookup_broadcast.unpersist()
lookup_broadcast.destroy()
```

```scala
// Scala broadcast
val lookupTable = Map("a" -> 1, "b" -> 2, "c" -> 3)
val lookupBroadcast = spark.sparkContext.broadcast(lookupTable)

val enriched = rdd.map { record =>
  val table = lookupBroadcast.value
  (record, table.getOrElse(record, 0))
}
```

### Accumulators

```python
# Long accumulator
error_count = spark.sparkContext.longAccumulator("Error Count")

def process_record(record):
    try:
        return transform(record)
    except Exception:
        error_count.add(1)
        return None

result_rdd = rdd.map(process_record).filter(lambda x: x is not None)
result_rdd.count()  # Trigger execution

print(f"Errors encountered: {error_count.value}")

# Collection accumulator
from pyspark import AccumulatorParam

class SetAccumulatorParam(AccumulatorParam):
    def zero(self, initial_value):
        return set()

    def addInPlace(self, v1, v2):
        return v1.union(v2)

error_types = spark.sparkContext.accumulator(set(), SetAccumulatorParam())

def track_errors(record):
    try:
        return process(record)
    except ValueError:
        error_types.add({"ValueError"})
        return None
    except TypeError:
        error_types.add({"TypeError"})
        return None
```

**Caution:** Accumulators may be updated more than once if tasks are retried. Use only for debugging/monitoring, not business logic.

---

## Performance Patterns

### Avoiding Shuffle

```python
# BAD: Multiple shuffles
result = rdd.groupByKey().mapValues(sum).reduceByKey(max)

# GOOD: Single shuffle with combineByKey
result = rdd.combineByKey(
    createCombiner=lambda v: v,
    mergeValue=lambda acc, v: acc + v,
    mergeCombiners=lambda a, b: max(a, b)
)

# Co-partition related RDDs to avoid join shuffles
partitioned_users = users.partitionBy(100)
partitioned_orders = orders.partitionBy(100)  # Same partitioner
joined = partitioned_users.join(partitioned_orders)  # No shuffle if same partitioner
```

### Efficient Serialization

```python
# Use Kryo serialization for better performance
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryo.registrationRequired", "false")

# Register custom classes for Kryo (Scala)
# spark.conf.set("spark.kryo.classesToRegister", "com.example.MyClass")
```

### Memory-Efficient Operations

```python
# Prefer iterator-based operations
def efficient_processing(iterator):
    for record in iterator:
        # Process one at a time, don't collect
        yield transform(record)

result = rdd.mapPartitions(efficient_processing)

# Avoid collecting large data to driver
# BAD
all_keys = rdd.keys().collect()  # Could be millions!

# GOOD
key_sample = rdd.keys().take(1000)  # Sample only
```

---

## Spark UI Analysis for RDDs

### Stages Tab Metrics

| Metric | What to Check |
|--------|---------------|
| Shuffle Write | Minimize with reduceByKey over groupByKey |
| Shuffle Read | Large reads indicate join/aggregation overhead |
| Spill (Memory) | Indicates partition too large for memory |
| Spill (Disk) | Data being written to disk - increase memory |
| GC Time | Should be < 10% of task time |

### Common Issues

1. **Uneven partition sizes**: Look for tasks taking much longer than others
2. **Data skew**: One partition has much more data than others
3. **Straggler tasks**: A few tasks taking 10x longer than median

### Debugging Tips

```python
# Check partition sizes
partition_sizes = rdd.glom().map(len).collect()
print(f"Partition sizes: min={min(partition_sizes)}, max={max(partition_sizes)}, avg={sum(partition_sizes)/len(partition_sizes)}")

# Check partitioner
print(f"Partitioner: {rdd.partitioner}")
print(f"Num partitions: {rdd.getNumPartitions()}")

# Debug lineage
print(rdd.toDebugString())
```

---

## Best Practices Summary

1. **Prefer DataFrames** - Use RDDs only when DataFrame API insufficient
2. **Use reduceByKey over groupByKey** - Combines locally first, reduces shuffle
3. **Preserve partitioning** - Use mapValues/flatMapValues to keep partitioner
4. **Minimize shuffles** - Co-partition related RDDs, use broadcast for small data
5. **Use mapPartitions** - For expensive initialization (DB connections, etc.)
6. **Avoid collect on large data** - Use take, takeSample, or foreachPartition
7. **Broadcast lookup tables** - Avoid shuffle for small reference data
8. **Monitor accumulators** - Use for debugging, not business logic
9. **Check partition distribution** - Avoid skew with custom partitioners
10. **Profile with Spark UI** - Identify shuffle, spill, and GC issues

---

## Reference: Spark Sql Dataframes

# Spark SQL and DataFrame API

---

## When to Use DataFrames vs RDDs

**Use DataFrames when:**
- Processing structured or semi-structured data (JSON, Parquet, CSV, Avro)
- Performing SQL-like operations (joins, aggregations, filters)
- Need Catalyst optimizer benefits (predicate pushdown, column pruning)
- Working with columnar formats for better compression

**Use RDDs when:**
- Need fine-grained control over physical data distribution
- Working with unstructured data (text processing, custom binary formats)
- Implementing custom partitioning logic
- Legacy code migration (prefer DataFrame migration when possible)

---

## Schema Definition

### Explicit Schema (Production Required)

```python
# PySpark - Explicit schema definition
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType,
    DoubleType, TimestampType, ArrayType, MapType
)

# Define schema explicitly - ALWAYS do this in production
user_schema = StructType([
    StructField("user_id", StringType(), nullable=False),
    StructField("name", StringType(), nullable=True),
    StructField("age", IntegerType(), nullable=True),
    StructField("email", StringType(), nullable=True),
    StructField("created_at", TimestampType(), nullable=False),
    StructField("tags", ArrayType(StringType()), nullable=True),
    StructField("metadata", MapType(StringType(), StringType()), nullable=True)
])

# Read with explicit schema - no inference overhead
df = spark.read.schema(user_schema).json("s3://bucket/users/")
```

```scala
// Scala - Explicit schema definition
import org.apache.spark.sql.types._

val userSchema = StructType(Seq(
  StructField("user_id", StringType, nullable = false),
  StructField("name", StringType, nullable = true),
  StructField("age", IntegerType, nullable = true),
  StructField("email", StringType, nullable = true),
  StructField("created_at", TimestampType, nullable = false),
  StructField("tags", ArrayType(StringType), nullable = true),
  StructField("metadata", MapType(StringType, StringType), nullable = true)
))

val df = spark.read.schema(userSchema).json("s3://bucket/users/")
```

### Schema Inference Pitfalls

```python
# AVOID in production - causes full data scan
df = spark.read.json("s3://bucket/users/")  # Infers schema - slow!

# If you must infer, sample a small portion
df = spark.read.option("samplingRatio", 0.01).json("s3://bucket/users/")
```

---

## Column Operations and Expressions

### Built-in Functions (Always Prefer Over UDFs)

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Column transformations - use built-in functions
df = df.withColumn("name_upper", F.upper(F.col("name")))
df = df.withColumn("email_domain", F.split(F.col("email"), "@")[1])
df = df.withColumn("age_group",
    F.when(F.col("age") < 18, "minor")
     .when(F.col("age") < 65, "adult")
     .otherwise("senior")
)

# Date/time operations
df = df.withColumn("year", F.year("created_at"))
df = df.withColumn("date_str", F.date_format("created_at", "yyyy-MM-dd"))
df = df.withColumn("days_since", F.datediff(F.current_date(), "created_at"))

# Array operations
df = df.withColumn("first_tag", F.col("tags")[0])
df = df.withColumn("tag_count", F.size("tags"))
df = df.withColumn("has_premium", F.array_contains("tags", "premium"))

# Null handling
df = df.withColumn("name_clean", F.coalesce("name", F.lit("Unknown")))
df = df.filter(F.col("email").isNotNull())
```

### Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

# Define window specifications
user_window = Window.partitionBy("user_id").orderBy("created_at")
category_window = Window.partitionBy("category")

# Ranking functions
df = df.withColumn("row_num", F.row_number().over(user_window))
df = df.withColumn("rank", F.rank().over(user_window))
df = df.withColumn("dense_rank", F.dense_rank().over(user_window))

# Analytic functions
df = df.withColumn("prev_value", F.lag("amount", 1).over(user_window))
df = df.withColumn("next_value", F.lead("amount", 1).over(user_window))
df = df.withColumn("running_total", F.sum("amount").over(user_window))

# Aggregations over windows
df = df.withColumn("category_avg", F.avg("amount").over(category_window))
df = df.withColumn("category_max", F.max("amount").over(category_window))

# Rolling windows
rolling_7day = Window.partitionBy("user_id") \
    .orderBy(F.col("created_at").cast("long")) \
    .rangeBetween(-7*86400, 0)  # 7 days in seconds

df = df.withColumn("rolling_7d_sum", F.sum("amount").over(rolling_7day))
```

```scala
// Scala window functions
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

val userWindow = Window.partitionBy("user_id").orderBy("created_at")
val categoryWindow = Window.partitionBy("category")

val result = df
  .withColumn("row_num", row_number().over(userWindow))
  .withColumn("running_total", sum("amount").over(userWindow))
  .withColumn("category_avg", avg("amount").over(categoryWindow))
```

---

## Spark SQL Queries

### Registering DataFrames as Views

```python
# Temporary view - session scoped
df.createOrReplaceTempView("users")

# Global temporary view - application scoped
df.createOrReplaceGlobalTempView("users")
# Access via: global_temp.users

# Execute SQL
result = spark.sql("""
    SELECT
        user_id,
        name,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    WHERE u.created_at >= '2024-01-01'
    GROUP BY user_id, name
    HAVING total_spent > 1000
    ORDER BY total_spent DESC
""")
```

### CTEs and Subqueries

```python
result = spark.sql("""
    WITH user_stats AS (
        SELECT
            user_id,
            COUNT(*) as order_count,
            SUM(amount) as total_spent,
            AVG(amount) as avg_order
        FROM orders
        WHERE order_date >= '2024-01-01'
        GROUP BY user_id
    ),
    ranked_users AS (
        SELECT
            *,
            PERCENT_RANK() OVER (ORDER BY total_spent) as spend_percentile
        FROM user_stats
    )
    SELECT *
    FROM ranked_users
    WHERE spend_percentile >= 0.9
""")
```

---

## Join Strategies

### Join Types and When to Use

```python
# Inner join - matching records only
result = orders.join(users, orders.user_id == users.user_id, "inner")

# Left outer - all from left, matching from right
result = orders.join(users, "user_id", "left")

# Right outer - all from right, matching from left
result = orders.join(users, "user_id", "right")

# Full outer - all records from both
result = orders.join(users, "user_id", "full")

# Left anti - records in left NOT in right
new_users = all_users.join(existing_users, "user_id", "left_anti")

# Left semi - records in left that have match in right (no columns from right)
active_users = users.join(orders, "user_id", "left_semi")

# Cross join - cartesian product (use carefully!)
result = df1.crossJoin(df2)
```

### Broadcast Join (Small Table Optimization)

```python
from pyspark.sql.functions import broadcast

# Explicit broadcast hint - join small table to large table
# Broadcasts entire small_df to all executors (must fit in memory)
result = large_df.join(broadcast(small_df), "join_key")

# Auto broadcast threshold (default 10MB)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 200 * 1024 * 1024)  # 200MB

# Disable auto broadcast for specific query
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
```

**Spark UI Check:** In SQL tab, look for "BroadcastHashJoin" vs "SortMergeJoin". Broadcast should show quick exchange, while sort-merge shows shuffle.

### Handling Skewed Joins (Spark 3.x AQE)

```python
# Enable Adaptive Query Execution (Spark 3.0+)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", 5)
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# Manual skew handling with salting
from pyspark.sql.functions import monotonically_increasing_id, explode, array, lit

# Add salt to skewed key in large table
salt_count = 10
large_df_salted = large_df.withColumn(
    "join_key_salted",
    F.concat(F.col("join_key"), F.lit("_"), (F.monotonically_increasing_id() % salt_count).cast("string"))
)

# Explode small table to match salted keys
small_df_exploded = small_df.withColumn(
    "salt", F.explode(F.array([F.lit(i) for i in range(salt_count)]))
).withColumn(
    "join_key_salted",
    F.concat(F.col("join_key"), F.lit("_"), F.col("salt").cast("string"))
)

# Join on salted key
result = large_df_salted.join(small_df_exploded, "join_key_salted")
```

---

## Aggregations

### GroupBy Operations

```python
from pyspark.sql import functions as F

# Basic aggregations
stats = df.groupBy("category").agg(
    F.count("*").alias("count"),
    F.sum("amount").alias("total"),
    F.avg("amount").alias("average"),
    F.min("amount").alias("minimum"),
    F.max("amount").alias("maximum"),
    F.stddev("amount").alias("std_dev"),
    F.countDistinct("user_id").alias("unique_users"),
    F.collect_list("product_id").alias("products"),  # Caution: can OOM
    F.collect_set("product_id").alias("unique_products")
)

# Multiple grouping sets (Spark SQL)
result = spark.sql("""
    SELECT
        category,
        region,
        SUM(amount) as total
    FROM sales
    GROUP BY GROUPING SETS (
        (category, region),
        (category),
        (region),
        ()
    )
""")

# Equivalent with rollup/cube
rollup_df = df.rollup("category", "region").agg(F.sum("amount"))
cube_df = df.cube("category", "region").agg(F.sum("amount"))
```

### Pivot Tables

```python
# Pivot - turn row values into columns
pivot_df = df.groupBy("user_id").pivot("category", ["electronics", "clothing", "food"]) \
    .agg(F.sum("amount"))

# Result columns: user_id, electronics, clothing, food

# Unpivot (melt) - turn columns into rows
from pyspark.sql.functions import expr

unpivot_df = pivot_df.select(
    "user_id",
    expr("stack(3, 'electronics', electronics, 'clothing', clothing, 'food', food) as (category, amount)")
).filter("amount is not null")
```

---

## Catalyst Optimizer Tips

### Predicate Pushdown

```python
# Good - filter pushed down to data source
df = spark.read.parquet("s3://bucket/data/").filter(F.col("date") == "2024-01-01")

# Check physical plan for PushedFilters
df.explain(True)
```

### Column Pruning

```python
# Good - only read required columns
df = spark.read.parquet("s3://bucket/data/").select("id", "name", "amount")

# Bad - reads all columns then filters
df = spark.read.parquet("s3://bucket/data/")
result = df.select("id", "name", "amount")
```

### Partition Pruning

```python
# Data partitioned by date
# Good - only reads matching partitions
df = spark.read.parquet("s3://bucket/data/") \
    .filter(F.col("date").between("2024-01-01", "2024-01-31"))

# Verify partition pruning in Spark UI - Files Read should be reduced
```

---

## Common Anti-Patterns

### Avoid These Patterns

```python
# BAD: Using Python UDF when built-in exists
from pyspark.sql.functions import udf
@udf("string")
def upper_udf(s):
    return s.upper() if s else None
df.withColumn("name", upper_udf("name"))  # 10-100x slower!

# GOOD: Use built-in function
df.withColumn("name", F.upper("name"))

# BAD: Collect large data to driver
all_data = df.collect()  # OOM risk!
for row in all_data:
    process(row)

# GOOD: Process distributed or use take/limit
sample = df.take(100)  # Small sample
df.foreach(process_partition)  # Distributed processing

# BAD: Multiple actions triggering recomputation
count = df.count()
total = df.agg(F.sum("amount")).collect()
# Two full scans of data!

# GOOD: Cache if multiple actions needed
df.cache()
count = df.count()
total = df.agg(F.sum("amount")).collect()
df.unpersist()

# BAD: String column used in filter (case sensitivity issues)
df.filter(df.status == "ACTIVE")  # May miss "active", "Active"

# GOOD: Normalize or use case-insensitive comparison
df.filter(F.upper("status") == "ACTIVE")
```

---

## Spark UI Analysis for DataFrames

### SQL Tab Metrics to Monitor

1. **Duration** - Long stages indicate optimization opportunities
2. **Input Size** - Verify partition pruning reduced data read
3. **Shuffle Write/Read** - Large shuffles suggest join/aggregation issues
4. **Spill (Memory/Disk)** - Indicates memory pressure, increase executor memory

### Physical Plan Analysis

```python
# View physical plan
df.explain(True)

# Look for:
# - FileScan with PushedFilters (predicate pushdown working)
# - BroadcastHashJoin vs SortMergeJoin (broadcast optimization)
# - Exchange (shuffle operations)
# - WholeStageCodegen (Tungsten optimization active)
```

### Key Metrics in Stages Tab

| Metric | Healthy Range | Action if High |
|--------|---------------|----------------|
| Shuffle Read Size | < 1GB per task | Increase partitions, add filter |
| Spill (Disk) | 0 | Increase executor memory |
| GC Time | < 10% of task time | Tune memory fractions |
| Task Duration Variance | < 2x median | Address data skew |

---

## Best Practices Summary

1. **Always define explicit schemas** - No inference in production
2. **Use built-in functions** - Avoid UDFs when possible
3. **Broadcast small tables** - Tables under 200MB
4. **Filter early** - Push filters before joins and aggregations
5. **Select only needed columns** - Enable column pruning
6. **Partition by common filter columns** - Enable partition pruning
7. **Cache strategically** - Only reused DataFrames
8. **Monitor Spark UI** - Check shuffle, spill, and GC metrics
9. **Enable AQE in Spark 3.x** - Automatic optimization for skew and partitions
10. **Test with production data volume** - Performance varies with scale

---

## Reference: Streaming Patterns

# Streaming Patterns

---

## Structured Streaming Overview

### When to Use Structured Streaming

**Use when:**
- Processing continuous data streams (Kafka, files, sockets)
- Need exactly-once processing guarantees
- Real-time analytics and dashboards
- Event-driven architectures
- Incremental ETL from streaming sources

**Consider alternatives when:**
- Batch processing is sufficient (lower complexity)
- Sub-second latency required (consider Flink)
- Very simple event processing (Kafka Streams may suffice)

---

## Reading from Streaming Sources

### Kafka Source

```python
# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker1:9092,broker2:9092") \
    .option("subscribe", "topic1,topic2") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", 100000) \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .load()

# Kafka provides key, value as bytes
# Parse JSON value
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType

schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("event_time", TimestampType()),
    StructField("amount", DoubleType())
])

parsed_df = df.select(
    F.col("key").cast("string").alias("kafka_key"),
    F.from_json(F.col("value").cast("string"), schema).alias("data"),
    F.col("timestamp").alias("kafka_timestamp"),
    F.col("partition"),
    F.col("offset")
).select("kafka_key", "data.*", "kafka_timestamp", "partition", "offset")
```

```scala
// Scala Kafka source
val df = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "broker1:9092,broker2:9092")
  .option("subscribe", "topic1")
  .option("startingOffsets", "latest")
  .load()

val parsed = df.select(
  col("key").cast("string"),
  from_json(col("value").cast("string"), schema).as("data")
).select("key", "data.*")
```

### File Source (Auto-Discovery)

```python
# Read new files as they arrive
df = spark.readStream \
    .format("parquet") \
    .schema(my_schema) \
    .option("path", "s3://bucket/incoming/") \
    .option("maxFilesPerTrigger", 100) \
    .load()

# For JSON files
df = spark.readStream \
    .format("json") \
    .schema(my_schema) \
    .option("path", "s3://bucket/incoming/") \
    .load()

# CSV with header
df = spark.readStream \
    .format("csv") \
    .schema(my_schema) \
    .option("path", "s3://bucket/incoming/") \
    .option("header", "true") \
    .load()
```

### Rate Source (Testing)

```python
# Generate test data at specified rate
df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 1000) \
    .option("numPartitions", 10) \
    .load()

# Columns: timestamp, value (incrementing long)
```

---

## Output Modes

### Append Mode (Default)

```python
# Only new rows added since last trigger
# Use when: No aggregations, or windowed aggregations with watermark
query = df.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://bucket/output/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

### Update Mode

```python
# Only rows that changed since last trigger
# Use when: Aggregations, want incremental updates
query = df.groupBy("user_id").count() \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()
```

### Complete Mode

```python
# Entire result table every trigger
# Use when: Need full aggregation result each time
# Warning: Can be expensive for large state
query = df.groupBy("user_id").count() \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
```

### Mode Selection Guide

| Use Case | Output Mode | Notes |
|----------|-------------|-------|
| ETL to files | append | Default, efficient |
| Windowed aggregations | append | With watermark |
| Running counts/sums | update | Incremental |
| Dashboards needing full state | complete | Expensive |
| Deduplication | append | With dropDuplicates |

---

## Watermarks and Event Time

### Understanding Watermarks

Watermarks define how late data can arrive before being dropped. They enable Spark to:
- Clean up old state (bounded memory)
- Emit results at appropriate times
- Handle out-of-order events

### Setting Watermarks

```python
from pyspark.sql import functions as F

# Define watermark on event time column
df_with_watermark = df \
    .withWatermark("event_time", "10 minutes")

# Watermark threshold: max_event_time - 10 minutes
# Events older than watermark are dropped
# State older than watermark is cleaned up
```

### Watermark Guidelines

| Scenario | Watermark Duration | Reasoning |
|----------|-------------------|-----------|
| Real-time analytics | 1-5 minutes | Low latency, tolerate minimal late data |
| Standard ETL | 10-30 minutes | Balance latency and late data |
| Late-arriving data common | 1-24 hours | Accommodate delayed events |
| Best-effort real-time | 0 minutes | No late data tolerance |

### Example with Windowed Aggregation

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Streaming aggregation with watermark
result = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes", "1 minute"),  # 5-min tumbling window, 1-min slide
        "user_id"
    ) \
    .agg(
        F.count("*").alias("event_count"),
        F.sum("amount").alias("total_amount")
    )

# Output schema includes window struct: window.start, window.end
query = result \
    .select(
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        "user_id",
        "event_count",
        "total_amount"
    ) \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://bucket/windowed_output/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

---

## Windowed Operations

### Tumbling Windows (Non-Overlapping)

```python
from pyspark.sql import functions as F

# 5-minute tumbling windows
result = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        F.window("event_time", "5 minutes"),
        "category"
    ) \
    .agg(F.sum("amount").alias("total"))

# Windows: [00:00-00:05), [00:05-00:10), [00:10-00:15), ...
```

### Sliding Windows (Overlapping)

```python
# 10-minute windows, sliding every 2 minutes
result = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        F.window("event_time", "10 minutes", "2 minutes"),
        "category"
    ) \
    .agg(F.sum("amount").alias("total"))

# Windows: [00:00-00:10), [00:02-00:12), [00:04-00:14), ...
```

### Session Windows (Gap-Based)

```python
# Session windows with 5-minute gap threshold
result = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        F.session_window("event_time", "5 minutes"),  # Spark 3.2+
        "user_id"
    ) \
    .agg(
        F.count("*").alias("events_in_session"),
        F.first("event_time").alias("session_start"),
        F.last("event_time").alias("session_end")
    )
```

---

## Stateful Operations

### Aggregations (Built-in State)

```python
# Running count by key
running_counts = df \
    .withWatermark("event_time", "1 hour") \
    .groupBy("user_id") \
    .agg(F.count("*").alias("total_events"))

# State stored per user_id
# Cleaned up based on watermark
```

### Deduplication

```python
# Drop duplicates within watermark window
deduped = df \
    .withWatermark("event_time", "10 minutes") \
    .dropDuplicates(["event_id"])  # Keep first occurrence

# Can also dedupe by multiple columns
deduped = df \
    .withWatermark("event_time", "10 minutes") \
    .dropDuplicates(["user_id", "event_type", "event_time"])
```

### Custom Stateful Processing (flatMapGroupsWithState)

```python
# PySpark - Custom state using applyInPandasWithState (Spark 3.4+)
from pyspark.sql.streaming.state import GroupState, GroupStateTimeout

def update_session_state(
    key: tuple,
    pdf_iter: Iterator[pd.DataFrame],
    state: GroupState
) -> Iterator[pd.DataFrame]:
    # Get or initialize state
    if state.exists:
        session_data = state.get
    else:
        session_data = {"count": 0, "total": 0.0}

    # Process input data
    for pdf in pdf_iter:
        session_data["count"] += len(pdf)
        session_data["total"] += pdf["amount"].sum()

    # Update state
    state.update(session_data)

    # Optionally set timeout
    state.setTimeoutDuration(10 * 60 * 1000)  # 10 minutes

    # Yield output
    yield pd.DataFrame([{
        "user_id": key[0],
        "event_count": session_data["count"],
        "total_amount": session_data["total"]
    }])

# Apply stateful function
result = df \
    .withWatermark("event_time", "10 minutes") \
    .groupBy("user_id") \
    .applyInPandasWithState(
        update_session_state,
        outputStructType=output_schema,
        stateStructType=state_schema,
        outputMode="update",
        timeoutConf=GroupStateTimeout.ProcessingTimeTimeout
    )
```

```scala
// Scala flatMapGroupsWithState
import org.apache.spark.sql.streaming.{GroupState, GroupStateTimeout}

case class UserState(count: Long, totalAmount: Double)
case class UserOutput(userId: String, count: Long, totalAmount: Double)

def updateState(
    userId: String,
    events: Iterator[Event],
    state: GroupState[UserState]
): Iterator[UserOutput] = {

  val currentState = state.getOption.getOrElse(UserState(0, 0.0))

  var newCount = currentState.count
  var newTotal = currentState.totalAmount

  events.foreach { event =>
    newCount += 1
    newTotal += event.amount
  }

  val newState = UserState(newCount, newTotal)
  state.update(newState)
  state.setTimeoutDuration("10 minutes")

  Iterator(UserOutput(userId, newCount, newTotal))
}

val result = df
  .withWatermark("event_time", "10 minutes")
  .as[Event]
  .groupByKey(_.userId)
  .flatMapGroupsWithState(
    OutputMode.Update,
    GroupStateTimeout.ProcessingTimeTimeout
  )(updateState)
```

---

## Streaming Joins

### Stream-Static Join

```python
# Join streaming data with static lookup table
static_df = spark.read.parquet("s3://bucket/lookup/")

# Streaming df joined with static - no watermark needed
result = streaming_df.join(static_df, "join_key", "left")

# Static table can be periodically refreshed
# Use broadcast for small static tables
from pyspark.sql.functions import broadcast
result = streaming_df.join(broadcast(static_df), "join_key")
```

### Stream-Stream Join

```python
# Join two streams - requires watermarks on both
from pyspark.sql import functions as F

stream1 = spark.readStream.format("kafka")...
stream2 = spark.readStream.format("kafka")...

# Both streams need watermarks
stream1_wm = stream1.withWatermark("event_time", "10 minutes")
stream2_wm = stream2.withWatermark("event_time", "10 minutes")

# Inner join with time constraint
result = stream1_wm.join(
    stream2_wm,
    F.expr("""
        stream1.user_id = stream2.user_id AND
        stream1.event_time >= stream2.event_time AND
        stream1.event_time <= stream2.event_time + INTERVAL 5 MINUTES
    """),
    "inner"
)

# Left outer join (Spark 2.3+)
result = stream1_wm.join(
    stream2_wm,
    F.expr("""
        stream1.user_id = stream2.user_id AND
        stream1.event_time >= stream2.event_time - INTERVAL 5 MINUTES AND
        stream1.event_time <= stream2.event_time + INTERVAL 5 MINUTES
    """),
    "leftOuter"
)
```

### Join Type Support

| Join Type | Stream-Static | Stream-Stream |
|-----------|---------------|---------------|
| Inner | Yes | Yes |
| Left Outer | Yes | Yes (Spark 2.3+) |
| Right Outer | Yes | Yes (Spark 2.3+) |
| Full Outer | Yes | Yes (Spark 2.4+) |
| Left Semi | Yes | Not supported |
| Left Anti | Yes | Not supported |

---

## Sinks

### Kafka Sink

```python
# Write to Kafka
query = df \
    .select(
        F.col("user_id").alias("key"),
        F.to_json(F.struct("*")).alias("value")
    ) \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker1:9092") \
    .option("topic", "output_topic") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

### File Sink (Parquet, JSON, CSV)

```python
# Parquet sink with partitioning
query = df.writeStream \
    .format("parquet") \
    .option("path", "s3://bucket/output/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .partitionBy("date", "hour") \
    .trigger(processingTime="1 minute") \
    .start()

# JSON sink
query = df.writeStream \
    .format("json") \
    .option("path", "s3://bucket/output/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

### Delta Lake Sink

```python
# Delta Lake (ACID transactions, schema evolution)
query = df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("path", "s3://bucket/delta_table/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .option("mergeSchema", "true") \
    .start()

# Upsert with foreachBatch
def upsert_to_delta(batch_df, batch_id):
    delta_table = DeltaTable.forPath(spark, "s3://bucket/delta_table/")
    delta_table.alias("target").merge(
        batch_df.alias("source"),
        "target.id = source.id"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

query = df.writeStream \
    .foreachBatch(upsert_to_delta) \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .start()
```

### Custom Sink (foreachBatch)

```python
def write_to_database(batch_df, batch_id):
    """Write each micro-batch to external database."""
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host:5432/db") \
        .option("dbtable", "output_table") \
        .option("user", "user") \
        .option("password", "password") \
        .mode("append") \
        .save()

query = df.writeStream \
    .foreachBatch(write_to_database) \
    .option("checkpointLocation", "s3://bucket/checkpoints/") \
    .trigger(processingTime="30 seconds") \
    .start()
```

### foreach (Row-by-Row)

```python
# For custom processing of each row
class ForeachWriter:
    def open(self, partition_id, epoch_id):
        # Initialize connection
        self.connection = create_connection()
        return True

    def process(self, row):
        # Process each row
        self.connection.insert(row.asDict())

    def close(self, error):
        # Clean up
        self.connection.close()

query = df.writeStream \
    .foreach(ForeachWriter()) \
    .start()
```

---

## Triggers

### Available Trigger Types

```python
# Process as fast as possible (default)
query = df.writeStream.trigger(processingTime="0 seconds").start()

# Fixed interval
query = df.writeStream.trigger(processingTime="1 minute").start()

# Once - process all available data, then stop
query = df.writeStream.trigger(once=True).start()

# Available now - process all available data (Spark 3.3+)
query = df.writeStream.trigger(availableNow=True).start()

# Continuous processing (experimental, low latency)
query = df.writeStream.trigger(continuous="1 second").start()
```

### Trigger Selection Guide

| Trigger | Use Case |
|---------|----------|
| processingTime="0 seconds" | Maximum throughput |
| processingTime="N seconds" | Controlled resource usage |
| once=True | Batch-style processing |
| availableNow=True | Catch-up processing |
| continuous="N ms" | Ultra-low latency (experimental) |

---

## Monitoring and Management

### Query Management

```python
# Start query and get handle
query = df.writeStream.format("console").start()

# Query properties
print(f"Query ID: {query.id}")
print(f"Run ID: {query.runId}")
print(f"Name: {query.name}")
print(f"Is Active: {query.isActive}")
print(f"Status: {query.status}")
print(f"Last Progress: {query.lastProgress}")
print(f"Recent Progress: {query.recentProgress}")

# Wait for termination
query.awaitTermination()
query.awaitTermination(timeout=60)  # With timeout

# Stop query
query.stop()

# Get exception if failed
exception = query.exception()
```

### Progress Monitoring

```python
# Get latest progress
progress = query.lastProgress
if progress:
    print(f"Input rows/sec: {progress['inputRowsPerSecond']}")
    print(f"Processed rows/sec: {progress['processedRowsPerSecond']}")
    print(f"Batch ID: {progress['batchId']}")
    print(f"Duration: {progress['batchDuration']} ms")
    print(f"State rows: {progress['stateOperators']}")

# Custom progress listener
class ProgressListener:
    def onQueryProgress(self, event):
        print(f"Progress: {event.progress}")

    def onQueryTerminated(self, event):
        print(f"Terminated: {event.exception}")

spark.streams.addListener(ProgressListener())
```

### Checkpointing

```python
# Checkpoint location is required for fault tolerance
query = df.writeStream \
    .format("parquet") \
    .option("path", "s3://bucket/output/") \
    .option("checkpointLocation", "s3://bucket/checkpoints/query_name/") \
    .start()

# Checkpoint contains:
# - Offsets (what data has been processed)
# - State (for stateful operations)
# - Commits (what batches completed)

# Recovery: Query restarts from last checkpoint automatically
# Clean start: Delete checkpoint directory (loses state!)
```

---

## Performance Patterns

### Optimizing Throughput

```python
# 1. Increase Kafka partitions for parallelism
# Consumer parallelism = Kafka partitions

# 2. Tune maxOffsetsPerTrigger
query = df.readStream \
    .format("kafka") \
    .option("maxOffsetsPerTrigger", 500000) \  # More data per batch
    .load()

# 3. Optimize shuffle partitions
spark.conf.set("spark.sql.shuffle.partitions", 100)

# 4. Use appropriate trigger interval
query = df.writeStream \
    .trigger(processingTime="30 seconds") \
    .start()

# 5. Enable AQE for dynamic optimization
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

### Managing State Size

```python
# 1. Always use watermarks for stateful operations
df.withWatermark("event_time", "1 hour")

# 2. Monitor state size in progress
progress = query.lastProgress
for operator in progress["stateOperators"]:
    print(f"State rows: {operator['numRowsTotal']}")
    print(f"Memory used: {operator['memoryUsedBytes']}")

# 3. Configure state store
spark.conf.set("spark.sql.streaming.stateStore.providerClass",
    "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider")
# RocksDB handles larger state better than in-memory default

# 4. Set state cleanup mode
spark.conf.set("spark.sql.streaming.stateStore.stateSchemaCheck", "false")
```

---

## Common Anti-Patterns

```python
# BAD: No watermark with aggregation
df.groupBy("user_id").count()  # Unbounded state growth!

# GOOD: Always use watermark
df.withWatermark("event_time", "1 hour").groupBy("user_id").count()

# BAD: Complete mode with large state
df.groupBy("user_id").count().writeStream.outputMode("complete")  # Outputs entire state

# GOOD: Update mode for incremental
df.groupBy("user_id").count().writeStream.outputMode("update")

# BAD: No checkpoint location
query = df.writeStream.format("console").start()  # No fault tolerance!

# GOOD: Always specify checkpoint
query = df.writeStream.format("console") \
    .option("checkpointLocation", "/checkpoints/query") \
    .start()

# BAD: foreach for high-throughput
df.writeStream.foreach(process_row).start()  # Row-by-row overhead

# GOOD: foreachBatch for batched processing
df.writeStream.foreachBatch(process_batch).start()  # Batch-level efficiency
```

---

## Best Practices Summary

1. **Always use watermarks** - Prevents unbounded state growth
2. **Choose appropriate output mode** - Append for ETL, Update for aggregations
3. **Set checkpoint locations** - Required for fault tolerance
4. **Use foreachBatch over foreach** - Better performance for custom sinks
5. **Monitor state size** - Watch for memory growth in progress metrics
6. **Tune trigger intervals** - Balance latency vs throughput
7. **Match Kafka partitions to parallelism** - Consumer tasks = Kafka partitions
8. **Use stream-static joins when possible** - Simpler than stream-stream
9. **Test with production data rates** - Performance varies with volume
10. **Enable structured streaming UI** - Detailed metrics in Spark UI
