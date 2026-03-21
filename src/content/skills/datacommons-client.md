---
title: "Datacommons Client"
description: "Work with Data Commons, a platform providing programmatic access to public statistical data from global sources. Use this skill when working with demographic data, economic indicators, health statistics, environmental data, or any public datasets ..."
category: "research"
source: "community"
author: "Community"
tags: ["datacommons", "client"]
date: 2026-03-20
---

# Data Commons Client

## Overview

Provides comprehensive access to the Data Commons Python API v2 for querying statistical observations, exploring the knowledge graph, and resolving entity identifiers. Data Commons aggregates data from census bureaus, health organizations, environmental agencies, and other authoritative sources into a unified knowledge graph.

## Installation

Install the Data Commons Python client with Pandas support:

```bash
uv pip install "datacommons-client[Pandas]"
```

For basic usage without Pandas:
```bash
uv pip install datacommons-client
```

## Core Capabilities

The Data Commons API consists of three main endpoints, each detailed in dedicated reference files:

### 1. Observation Endpoint - Statistical Data Queries

Query time-series statistical data for entities. See `references/observation.md` for comprehensive documentation.

**Primary use cases:**
- Retrieve population, economic, health, or environmental statistics
- Access historical time-series data for trend analysis
- Query data for hierarchies (all counties in a state, all countries in a region)
- Compare statistics across multiple entities
- Filter by data source for consistency

**Common patterns:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Get latest population data
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06"],  # California
    date="latest"
)

# Get time series
response = client.observation.fetch(
    variable_dcids=["UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

# Query by hierarchy
response = client.observation.fetch(
    variable_dcids=["MedianIncome_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

### 2. Node Endpoint - Knowledge Graph Exploration

Explore entity relationships and properties within the knowledge graph. See `references/node.md` for comprehensive documentation.

**Primary use cases:**
- Discover available properties for entities
- Navigate geographic hierarchies (parent/child relationships)
- Retrieve entity names and metadata
- Explore connections between entities
- List all entity types in the graph

**Common patterns:**
```python
# Discover properties
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=True
)

# Navigate hierarchy
children = client.node.fetch_place_children(
    node_dcids=["country/USA"]
)

# Get entity names
names = client.node.fetch_entity_names(
    node_dcids=["geoId/06", "geoId/48"]
)
```

### 3. Resolve Endpoint - Entity Identification

Translate entity names, coordinates, or external IDs into Data Commons IDs (DCIDs). See `references/resolve.md` for comprehensive documentation.

**Primary use cases:**
- Convert place names to DCIDs for queries
- Resolve coordinates to places
- Map Wikidata IDs to Data Commons entities
- Handle ambiguous entity names

**Common patterns:**
```python
# Resolve by name
response = client.resolve.fetch_dcids_by_name(
    names=["California", "Texas"],
    entity_type="State"
)

# Resolve by coordinates
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=37.7749,
    longitude=-122.4194
)

# Resolve Wikidata IDs
response = client.resolve.fetch_dcids_by_wikidata_id(
    wikidata_ids=["Q30", "Q99"]
)
```

## Typical Workflow

Most Data Commons queries follow this pattern:

1. **Resolve entities** (if starting with names):
   ```python
   resolve_response = client.resolve.fetch_dcids_by_name(
       names=["California", "Texas"]
   )
   dcids = [r["candidates"][0]["dcid"]
            for r in resolve_response.to_dict().values()
            if r["candidates"]]
   ```

2. **Discover available variables** (optional):
   ```python
   variables = client.observation.fetch_available_statistical_variables(
       entity_dcids=dcids
   )
   ```

3. **Query statistical data**:
   ```python
   response = client.observation.fetch(
       variable_dcids=["Count_Person", "UnemploymentRate_Person"],
       entity_dcids=dcids,
       date="latest"
   )
   ```

4. **Process results**:
   ```python
   # As dictionary
   data = response.to_dict()

   # As Pandas DataFrame
   df = response.to_observations_as_records()
   ```

## Finding Statistical Variables

Statistical variables use specific naming patterns in Data Commons:

**Common variable patterns:**
- `Count_Person` - Total population
- `Count_Person_Female` - Female population
- `UnemploymentRate_Person` - Unemployment rate
- `Median_Income_Household` - Median household income
- `Count_Death` - Death count
- `Median_Age_Person` - Median age

**Discovery methods:**
```python
# Check what variables are available for an entity
available = client.observation.fetch_available_statistical_variables(
    entity_dcids=["geoId/06"]
)

# Or explore via the web interface
# https://datacommons.org/tools/statvar
```

## Working with Pandas

All observation responses integrate with Pandas:

```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06", "geoId/48"],
    date="all"
)

# Convert to DataFrame
df = response.to_observations_as_records()
# Columns: date, entity, variable, value

# Reshape for analysis
pivot = df.pivot_table(
    values='value',
    index='date',
    columns='entity'
)
```

## API Authentication

**For datacommons.org (default):**
- An API key is required
- Set via environment variable: `export DC_API_KEY="your_key"`
- Or pass when initializing: `client = DataCommonsClient(api_key="your_key")`
- Request keys at: https://apikeys.datacommons.org/

**For custom Data Commons instances:**
- No API key required
- Specify custom endpoint: `client = DataCommonsClient(url="https://custom.datacommons.org")`

## Reference Documentation

Comprehensive documentation for each endpoint is available in the `references/` directory:

- **`references/observation.md`**: Complete Observation API documentation with all methods, parameters, response formats, and common use cases
- **`references/node.md`**: Complete Node API documentation for graph exploration, property queries, and hierarchy navigation
- **`references/resolve.md`**: Complete Resolve API documentation for entity identification and DCID resolution
- **`references/getting_started.md`**: Quickstart guide with end-to-end examples and common patterns

## Additional Resources

- **Official Documentation**: https://docs.datacommons.org/api/python/v2/
- **Statistical Variable Explorer**: https://datacommons.org/tools/statvar
- **Data Commons Browser**: https://datacommons.org/browser/
- **GitHub Repository**: https://github.com/datacommonsorg/api-python

## Tips for Effective Use

1. **Always start with resolution**: Convert names to DCIDs before querying data
2. **Use relation expressions for hierarchies**: Query all children at once instead of individual queries
3. **Check data availability first**: Use `fetch_available_statistical_variables()` to see what's queryable
4. **Leverage Pandas integration**: Convert responses to DataFrames for analysis
5. **Cache resolutions**: If querying the same entities repeatedly, store name→DCID mappings
6. **Filter by facet for consistency**: Use `filter_facet_domains` to ensure data from the same source
7. **Read reference docs**: Each endpoint has extensive documentation in the `references/` directory

---

## Reference: Getting_Started

# Getting Started with Data Commons

## Quick Start Guide

This guide provides end-to-end examples for common Data Commons workflows.

## Installation and Setup

```bash
# Install with Pandas support
pip install "datacommons-client[Pandas]"

# Set up API key for datacommons.org
export DC_API_KEY="your_api_key_here"
```

Request an API key at: https://apikeys.datacommons.org/

## Example 1: Basic Population Query

Query current population for specific places:

```python
from datacommons_client import DataCommonsClient

# Initialize client
client = DataCommonsClient()

# Step 1: Resolve place names to DCIDs
places = ["California", "Texas", "New York"]
resolve_response = client.resolve.fetch_dcids_by_name(
    names=places,
    entity_type="State"
)

# Extract DCIDs
dcids = []
for name, result in resolve_response.to_dict().items():
    if result["candidates"]:
        dcids.append(result["candidates"][0]["dcid"])
        print(f"{name}: {result['candidates'][0]['dcid']}")

# Step 2: Query population data
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=dcids,
    date="latest"
)

# Step 3: Display results
data = response.to_dict()
for variable, entities in data.items():
    for entity, observations in entities.items():
        for obs in observations:
            print(f"{entity}: {obs['value']:,} people ({obs['date']})")
```

## Example 2: Time Series Analysis

Retrieve and plot historical unemployment rates:

```python
import pandas as pd
import matplotlib.pyplot as plt

client = DataCommonsClient()

# Query unemployment rate over time
response = client.observation.fetch(
    variable_dcids=["UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"  # Get all historical data
)

# Convert to DataFrame
df = response.to_observations_as_records()

# Plot
df = df.sort_values('date')
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['value'])
plt.title('US Unemployment Rate Over Time')
plt.xlabel('Year')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True)
plt.show()
```

## Example 3: Geographic Hierarchy Query

Get data for all counties within a state:

```python
client = DataCommonsClient()

# Query median income for all California counties
response = client.observation.fetch(
    variable_dcids=["Median_Income_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)

# Convert to DataFrame and sort
df = response.to_observations_as_records()

# Get county names
county_dcids = df['entity'].unique().tolist()
names = client.node.fetch_entity_names(node_dcids=county_dcids)

# Add names to dataframe
df['name'] = df['entity'].map(names)

# Display top 10 by income
top_counties = df.nlargest(10, 'value')[['name', 'value']]
print("\nTop 10 California Counties by Median Household Income:")
for idx, row in top_counties.iterrows():
    print(f"{row['name']}: ${row['value']:,.0f}")
```

## Example 4: Multi-Variable Comparison

Compare multiple statistics across entities:

```python
import pandas as pd

client = DataCommonsClient()

# Define places
places = ["California", "Texas", "Florida", "New York"]
resolve_response = client.resolve.fetch_dcids_by_name(names=places)

dcids = []
name_map = {}
for name, result in resolve_response.to_dict().items():
    if result["candidates"]:
        dcid = result["candidates"][0]["dcid"]
        dcids.append(dcid)
        name_map[dcid] = name

# Query multiple variables
variables = [
    "Count_Person",
    "Median_Income_Household",
    "UnemploymentRate_Person",
    "Median_Age_Person"
]

response = client.observation.fetch(
    variable_dcids=variables,
    entity_dcids=dcids,
    date="latest"
)

# Convert to DataFrame
df = response.to_observations_as_records()

# Add readable names
df['state'] = df['entity'].map(name_map)

# Pivot for comparison
pivot = df.pivot_table(
    values='value',
    index='state',
    columns='variable'
)

print("\nState Comparison:")
print(pivot.to_string())
```

## Example 5: Coordinate-Based Query

Find and query data for a location by coordinates:

```python
client = DataCommonsClient()

# User provides coordinates (e.g., from GPS)
latitude, longitude = 37.7749, -122.4194  # San Francisco

# Step 1: Resolve coordinates to place
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=latitude,
    longitude=longitude
)

# Step 2: Get place name
name = client.node.fetch_entity_names(node_dcids=[dcid])
print(f"Location: {name[dcid]}")

# Step 3: Check available variables
available_vars = client.observation.fetch_available_statistical_variables(
    entity_dcids=[dcid]
)

print(f"\nAvailable variables: {len(available_vars[dcid])} found")
print("First 10:", list(available_vars[dcid])[:10])

# Step 4: Query specific variables
response = client.observation.fetch(
    variable_dcids=["Count_Person", "Median_Income_Household"],
    entity_dcids=[dcid],
    date="latest"
)

# Display results
df = response.to_observations_as_records()
print("\nStatistics:")
for _, row in df.iterrows():
    print(f"{row['variable']}: {row['value']}")
```

## Example 6: Data Source Filtering

Query data from specific sources for consistency:

```python
client = DataCommonsClient()

# Query with facet filtering
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["country/USA"],
    date="all",
    filter_facet_domains=["census.gov"]  # Only US Census data
)

df = response.to_observations_as_records()
print(f"Found {len(df)} observations from census.gov")

# Compare with all sources
response_all = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

df_all = response_all.to_observations_as_records()
print(f"Found {len(df_all)} observations from all sources")
```

## Example 7: Exploring the Knowledge Graph

Discover entity properties and relationships:

```python
client = DataCommonsClient()

# Step 1: Explore what properties exist
entity = "geoId/06"  # California

# Get outgoing properties
out_props = client.node.fetch_property_labels(
    node_dcids=[entity],
    out=True
)

print(f"Outgoing properties for California:")
print(out_props[entity])

# Get incoming properties
in_props = client.node.fetch_property_labels(
    node_dcids=[entity],
    out=False
)

print(f"\nIncoming properties for California:")
print(in_props[entity])

# Step 2: Get specific property values
name_response = client.node.fetch_property_values(
    node_dcids=[entity],
    property="name",
    out=True
)

print(f"\nName property value:")
print(name_response.to_dict())

# Step 3: Explore hierarchy
children = client.node.fetch_place_children(node_dcids=[entity])
print(f"\nNumber of child places: {len(children[entity])}")

# Get names for first 5 children
if children[entity]:
    child_sample = children[entity][:5]
    child_names = client.node.fetch_entity_names(node_dcids=child_sample)
    print("\nSample child places:")
    for dcid, name in child_names.items():
        print(f"  {name}")
```

## Example 8: Batch Processing Multiple Queries

Efficiently query data for many entities:

```python
import pandas as pd

client = DataCommonsClient()

# List of cities to analyze
cities = [
    "San Francisco, CA",
    "Los Angeles, CA",
    "San Diego, CA",
    "Sacramento, CA",
    "San Jose, CA"
]

# Resolve all cities
resolve_response = client.resolve.fetch_dcids_by_name(
    names=cities,
    entity_type="City"
)

# Build mapping
city_dcids = []
dcid_to_name = {}
for name, result in resolve_response.to_dict().items():
    if result["candidates"]:
        dcid = result["candidates"][0]["dcid"]
        city_dcids.append(dcid)
        dcid_to_name[dcid] = name

# Query multiple variables at once
variables = [
    "Count_Person",
    "Median_Income_Household",
    "UnemploymentRate_Person"
]

response = client.observation.fetch(
    variable_dcids=variables,
    entity_dcids=city_dcids,
    date="latest"
)

# Process into a comparison table
df = response.to_observations_as_records()
df['city'] = df['entity'].map(dcid_to_name)

# Create comparison table
comparison = df.pivot_table(
    values='value',
    index='city',
    columns='variable',
    aggfunc='first'
)

print("\nCalifornia Cities Comparison:")
print(comparison.to_string())

# Export to CSV
comparison.to_csv('ca_cities_comparison.csv')
print("\nData exported to ca_cities_comparison.csv")
```

## Common Patterns Summary

### Pattern 1: Name → DCID → Data
```python
names = ["California"]
dcids = resolve_names(names)
data = query_observations(dcids, variables)
```

### Pattern 2: Coordinates → DCID → Data
```python
dcid = resolve_coordinates(lat, lon)
data = query_observations([dcid], variables)
```

### Pattern 3: Parent → Children → Data
```python
children = get_place_children(parent_dcid)
data = query_observations(children, variables)
```

### Pattern 4: Explore → Select → Query
```python
available_vars = check_available_variables(dcids)
selected_vars = filter_relevant(available_vars)
data = query_observations(dcids, selected_vars)
```

## Error Handling Best Practices

```python
client = DataCommonsClient()

# Always check for candidates
resolve_response = client.resolve.fetch_dcids_by_name(names=["Unknown Place"])
result = resolve_response.to_dict()["Unknown Place"]

if not result["candidates"]:
    print("No matches found - try a more specific name")
    # Handle error appropriately
else:
    dcid = result["candidates"][0]["dcid"]
    # Proceed with query

# Check for multiple candidates (ambiguity)
if len(result["candidates"]) > 1:
    print(f"Multiple matches found: {len(result['candidates'])}")
    for candidate in result["candidates"]:
        print(f"  {candidate['dcid']} ({candidate.get('dominantType', 'N/A')})")
    # Let user select or use additional filtering
```

## Next Steps

1. Explore available statistical variables: https://datacommons.org/tools/statvar
2. Browse the knowledge graph: https://datacommons.org/browser/
3. Read detailed endpoint documentation in `references/` directory
4. Check official documentation: https://docs.datacommons.org/api/python/v2/

---

## Reference: Node

# Node Endpoint - Knowledge Graph Exploration

## Purpose

The Node endpoint retrieves property relationships and values from the Data Commons knowledge graph. It returns information about directed edges (properties) connecting nodes, enabling discovery of connections within the graph structure.

## Core Capabilities

The Node API performs three primary functions:
1. Retrieve property labels associated with nodes
2. Obtain values for specific properties across nodes
3. Discover all connected nodes linked through relationships

## Available Methods

### 1. fetch()

Retrieve properties using relation expressions with arrow notation.

**Key Parameters:**
- `node_dcids`: Target node identifier(s)
- `expression`: Relation syntax using arrows (`->`, `<-`, `<-*`)
- `all_pages`: Enable pagination (default: True)
- `next_token`: Continue paginated results

**Arrow Notation:**
- `->`: Outgoing property (from node to value)
- `<-`: Incoming property (from value to node)
- `<-*`: Multi-hop incoming traversal

**Example Usage:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Get outgoing properties from California
response = client.node.fetch(
    node_dcids=["geoId/06"],
    expression="->name"
)

# Get incoming properties (what points to this node)
response = client.node.fetch(
    node_dcids=["geoId/06"],
    expression="<-containedInPlace"
)
```

### 2. fetch_property_labels()

Get property labels without retrieving values—useful for discovering what properties exist.

**Parameters:**
- `node_dcids`: Node identifier(s)
- `out`: Boolean—True for outgoing properties, False for incoming

**Example Usage:**
```python
# Get all outgoing property labels for California
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=True
)

# Get all incoming property labels
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=False
)
```

### 3. fetch_property_values()

Obtain specific property values with optional filters.

**Parameters:**
- `node_dcids`: Node identifier(s)
- `property`: Property name to query
- `out`: Direction (True for outgoing, False for incoming)
- `limit`: Maximum number of values to return

**Example Usage:**
```python
# Get name property for California
values = client.node.fetch_property_values(
    node_dcids=["geoId/06"],
    property="name",
    out=True
)
```

### 4. fetch_all_classes()

List all entity types (Class nodes) in the Data Commons graph.

**Example Usage:**
```python
classes = client.node.fetch_all_classes()
```

### 5. fetch_entity_names()

Look up entity names by DCID in selected languages.

**Parameters:**
- `node_dcids`: Entity identifier(s)
- `language`: Language code (default: "en")

**Example Usage:**
```python
names = client.node.fetch_entity_names(
    node_dcids=["geoId/06", "country/USA"],
    language="en"
)
# Returns: {"geoId/06": "California", "country/USA": "United States"}
```

### 6. Place Hierarchy Methods

These methods navigate geographic relationships:

#### fetch_place_children()
Get direct child places.

**Example Usage:**
```python
# Get all states in USA
children = client.node.fetch_place_children(
    node_dcids=["country/USA"]
)
```

#### fetch_place_descendants()
Retrieve full child hierarchies (recursive).

**Example Usage:**
```python
# Get all descendants of California (counties, cities, etc.)
descendants = client.node.fetch_place_descendants(
    node_dcids=["geoId/06"]
)
```

#### fetch_place_parents()
Get direct parent places.

**Example Usage:**
```python
# Get parent of San Francisco
parents = client.node.fetch_place_parents(
    node_dcids=["geoId/0667000"]
)
```

#### fetch_place_ancestors()
Retrieve complete parent lineages.

**Example Usage:**
```python
# Get all ancestors of San Francisco (CA, USA, etc.)
ancestors = client.node.fetch_place_ancestors(
    node_dcids=["geoId/0667000"]
)
```

### 7. fetch_statvar_constraints()

Access constraint properties for statistical variables—useful for understanding variable definitions and constraints.

**Example Usage:**
```python
constraints = client.node.fetch_statvar_constraints(
    node_dcids=["Count_Person"]
)
```

## Response Format

Methods return either:
- **NodeResponse objects** with `.to_dict()`, `.to_json()`, and `.nextToken` properties
- **Dictionaries** for entity names and place hierarchy methods

## Pagination

For large responses:
1. Set `all_pages=False` to receive data in chunks
2. Response includes a `nextToken` value
3. Re-query using that token to fetch subsequent pages

**Example:**
```python
# First page
response = client.node.fetch(
    node_dcids=["country/USA"],
    expression="<-containedInPlace",
    all_pages=False
)

# Get next page if available
if response.nextToken:
    next_response = client.node.fetch(
        node_dcids=["country/USA"],
        expression="<-containedInPlace",
        next_token=response.nextToken
    )
```

## Common Use Cases

### Use Case 1: Explore Available Properties

```python
# Discover what properties an entity has
labels = client.node.fetch_property_labels(
    node_dcids=["geoId/06"],
    out=True
)
print(labels)  # Shows all outgoing properties like 'name', 'latitude', etc.
```

### Use Case 2: Navigate Geographic Hierarchies

```python
# Get all counties in California
counties = client.node.fetch_place_children(
    node_dcids=["geoId/06"]
)

# Filter for specific type if needed
county_dcids = [child for child in counties["geoId/06"]
                if "County" in child]
```

### Use Case 3: Build Entity Relationships

```python
# Find all entities that reference a specific node
references = client.node.fetch(
    node_dcids=["geoId/06"],
    expression="<-location"
)
```

## Important Notes

- Use `fetch_property_labels()` first to discover available properties
- The Node API cannot resolve complex relation expressions—use simpler expressions or break into multiple queries
- For linked entity properties with arc relationships, combine Node API queries with Observation API
- Place hierarchy methods return dictionaries, not NodeResponse objects

---

## Reference: Observation

# Observation Endpoint - Statistical Data Queries

## Purpose

The Observation API retrieves statistical observations—data points linking entities, variables, and specific dates. Examples include:
- "USA population in 2020"
- "California GDP over time"
- "Unemployment rate for all counties in a state"

## Core Methods

### 1. fetch()

Primary method for retrieving observations with flexible entity specification.

**Key Parameters:**
- `variable_dcids` (required): List of statistical variable identifiers
- `entity_dcids` or `entity_expression` (required): Specify entities by ID or relation expression
- `date` (optional): Defaults to "latest". Accepts:
  - ISO-8601 format (e.g., "2020", "2020-01", "2020-01-15")
  - "all" for complete time series
  - "latest" for most recent data
- `select` (optional): Controls returned fields
  - Default: `["date", "entity", "variable", "value"]`
  - Alternative: `["entity", "variable", "facet"]` to check availability without data
- `filter_facet_domains`: Filter by data source domain
- `filter_facet_ids`: Filter by specific facet IDs

**Response Structure:**
Data organized hierarchically by variable → entity, with metadata about "facets" (data sources) including:
- Provenance URLs
- Measurement methods
- Observation periods
- Import names

**Example Usage:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Get latest population for multiple entities
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06", "geoId/48"],  # California and Texas
    date="latest"
)

# Get complete time series
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["country/USA"],
    date="all"
)

# Use relation expressions to query hierarchies
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

### 2. fetch_available_statistical_variables()

Discovers which statistical variables contain data for given entities.

**Input:** Entity DCIDs only
**Output:** Dictionary of available variables organized by entity

**Example Usage:**
```python
# Check what variables are available for California
available = client.observation.fetch_available_statistical_variables(
    entity_dcids=["geoId/06"]
)
```

### 3. fetch_observations_by_entity_dcid()

Explicit method targeting specific entities by DCID (functionally equivalent to `fetch()` with entity_dcids).

### 4. fetch_observations_by_entity_type()

Retrieves observations for multiple entities grouped by parent and type—useful for querying all countries in a region or all counties within a state.

**Parameters:**
- `parent_entity`: Parent entity DCID
- `entity_type`: Type of child entities
- `variable_dcids`: Statistical variables to query
- `date`: Time specification
- `select` and filter options

**Example Usage:**
```python
# Get population for all counties in California
response = client.observation.fetch_observations_by_entity_type(
    parent_entity="geoId/06",
    entity_type="County",
    variable_dcids=["Count_Person"],
    date="2020"
)
```

## Response Object Methods

All response objects support:
- `to_json()`: Format as JSON string
- `to_dict()`: Return as dictionary
- `get_data_by_entity()`: Reorganize by entity instead of variable
- `to_observations_as_records()`: Flatten into individual records

## Common Use Cases

### Use Case 1: Check Data Availability Before Querying

Use `select=["entity", "variable"]` to confirm entities have observations without retrieving actual data:
```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06"],
    select=["entity", "variable"]
)
```

### Use Case 2: Access Complete Time Series

Request `date="all"` to obtain complete historical observations for trend analysis:
```python
response = client.observation.fetch(
    variable_dcids=["Count_Person", "UnemploymentRate_Person"],
    entity_dcids=["country/USA"],
    date="all"
)
```

### Use Case 3: Filter by Data Source

Specify `filter_facet_domains` to retrieve data from specific sources for consistency:
```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["country/USA"],
    filter_facet_domains=["census.gov"]
)
```

### Use Case 4: Query Hierarchical Relationships

Use relation expressions to fetch observations for related entities:
```python
# Get data for all counties within California
response = client.observation.fetch(
    variable_dcids=["MedianIncome_Household"],
    entity_expression="geoId/06<-containedInPlace+{typeOf:County}",
    date="2020"
)
```

## Working with Pandas

The API integrates seamlessly with Pandas. Install with Pandas support:
```bash
pip install "datacommons-client[Pandas]"
```

Response objects can be converted to DataFrames for analysis:
```python
response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=["geoId/06", "geoId/48"],
    date="all"
)

# Convert to DataFrame
df = response.to_observations_as_records()
# Returns DataFrame with columns: date, entity, variable, value
```

## Important Notes

- **facets** represent data sources and include provenance metadata
- **orderedFacets** are sorted by reliability/recency
- Use relation expressions for complex graph queries
- The `fetch()` method is the most flexible—use it for most queries

---

## Reference: Resolve

# Resolve Endpoint - Entity Identification

## Purpose

The Resolve API identifies Data Commons IDs (DCIDs) for entities in the knowledge graph. DCIDs are required for most queries in the Data Commons API, so resolution is typically the first step in any workflow.

## Key Capabilities

The endpoint currently supports **place entities only** and allows resolution through multiple methods:
- **By name**: Search using descriptive terms like "San Francisco, CA"
- **By Wikidata ID**: Lookup using external identifiers (e.g., "Q30" for USA)
- **By coordinates**: Locate places via latitude/longitude
- **By relation expressions**: Advanced searches using synthetic attributes

## Available Methods

### 1. fetch()

General resolution using relation expressions—most flexible method.

**Parameters:**
- `nodes`: List of search terms or identifiers
- `property`: Property to search (e.g., "name", "wikidataId")

**Example Usage:**
```python
from datacommons_client import DataCommonsClient

client = DataCommonsClient()

# Resolve by name
response = client.resolve.fetch(
    nodes=["California", "Texas"],
    property="name"
)
```

### 2. fetch_dcids_by_name()

Name-based lookup with optional type filtering—most commonly used method.

**Parameters:**
- `names`: List of place names to resolve
- `entity_type`: Optional type filter (e.g., "City", "State", "County")

**Returns:** `ResolveResponse` object with candidates for each name

**Example Usage:**
```python
# Basic name resolution
response = client.resolve.fetch_dcids_by_name(
    names=["San Francisco, CA", "Los Angeles"]
)

# With type filtering
response = client.resolve.fetch_dcids_by_name(
    names=["San Francisco"],
    entity_type="City"
)

# Access results
for name, result in response.to_dict().items():
    print(f"{name}: {result['candidates']}")
```

### 3. fetch_dcids_by_wikidata_id()

Wikidata ID resolution for entities with known Wikidata identifiers.

**Parameters:**
- `wikidata_ids`: List of Wikidata IDs (e.g., "Q30", "Q99")

**Example Usage:**
```python
# Resolve Wikidata IDs
response = client.resolve.fetch_dcids_by_wikidata_id(
    wikidata_ids=["Q30", "Q99"]  # USA and California
)
```

### 4. fetch_dcid_by_coordinates()

Geographic coordinate lookup to find the place at specific lat/long coordinates.

**Parameters:**
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate

**Returns:** Single DCID string for the place at those coordinates

**Example Usage:**
```python
# Find place at coordinates
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=37.7749,
    longitude=-122.4194
)
# Returns DCID for San Francisco
```

## Response Structure

All methods (except `fetch_dcid_by_coordinates`) return a `ResolveResponse` object containing:
- **node**: The search term provided
- **candidates**: List of matching DCIDs with optional metadata
  - Each candidate may include `dominantType` field for disambiguation
- **Helper methods**:
  - `to_dict()`: Full response as dictionary
  - `to_json()`: JSON string format
  - `to_flat_dict()`: Simplified format with just DCIDs

**Example Response:**
```python
response = client.resolve.fetch_dcids_by_name(names=["Springfield"])

# May return multiple candidates since many cities named Springfield exist
# {
#   "Springfield": {
#     "candidates": [
#       {"dcid": "geoId/1767000", "dominantType": "City"},  # Springfield, IL
#       {"dcid": "geoId/2567000", "dominantType": "City"},  # Springfield, MA
#       ...
#     ]
#   }
# }
```

## Common Use Cases

### Use Case 1: Resolve Place Names Before Querying

Most workflows start by resolving names to DCIDs:
```python
# Step 1: Resolve names
resolve_response = client.resolve.fetch_dcids_by_name(
    names=["California", "Texas"]
)

# Step 2: Extract DCIDs
dcids = []
for name, result in resolve_response.to_dict().items():
    if result["candidates"]:
        dcids.append(result["candidates"][0]["dcid"])

# Step 3: Query data using DCIDs
data_response = client.observation.fetch(
    variable_dcids=["Count_Person"],
    entity_dcids=dcids,
    date="latest"
)
```

### Use Case 2: Handle Ambiguous Names

When multiple candidates exist, use `dominantType` or be more specific:
```python
# Ambiguous name
response = client.resolve.fetch_dcids_by_name(names=["Springfield"])
candidates = response.to_dict()["Springfield"]["candidates"]

# Filter by type or choose based on context
city_candidates = [c for c in candidates if c.get("dominantType") == "City"]

# Or be more specific in the query
response = client.resolve.fetch_dcids_by_name(
    names=["Springfield, Illinois"],
    entity_type="City"
)
```

### Use Case 3: Batch Resolution

Resolve multiple entities efficiently:
```python
places = [
    "San Francisco, CA",
    "Los Angeles, CA",
    "San Diego, CA",
    "Sacramento, CA"
]

response = client.resolve.fetch_dcids_by_name(names=places)

# Build mapping of name to DCID
name_to_dcid = {}
for name, result in response.to_dict().items():
    if result["candidates"]:
        name_to_dcid[name] = result["candidates"][0]["dcid"]
```

### Use Case 4: Coordinate-Based Queries

Find the administrative place for a location:
```python
# User provides coordinates, find the place
latitude, longitude = 37.7749, -122.4194
dcid = client.resolve.fetch_dcid_by_coordinates(
    latitude=latitude,
    longitude=longitude
)

# Now query data for that place
response = client.observation.fetch(
    variable_dcids=["Count_Person", "MedianIncome_Household"],
    entity_dcids=[dcid],
    date="latest"
)
```

### Use Case 5: External ID Integration

When working with external datasets that use Wikidata IDs:
```python
# External dataset has Wikidata IDs
wikidata_ids = ["Q30", "Q99", "Q1384"]  # USA, California, New York

# Convert to Data Commons DCIDs
response = client.resolve.fetch_dcids_by_wikidata_id(
    wikidata_ids=wikidata_ids
)

# Extract DCIDs for further queries
dcids = []
for wid, result in response.to_dict().items():
    if result["candidates"]:
        dcids.append(result["candidates"][0]["dcid"])
```

## Important Limitations

1. **Place entities only**: The Resolve API currently supports only place entities (countries, states, cities, counties, etc.). For other entity types, DCIDs must be obtained through other means (e.g., Node API exploration).

2. **Cannot resolve linked entity properties**: For queries involving relationships like `containedInPlace`, use the Node API instead.

3. **Ambiguity handling**: When multiple candidates exist, the API returns all matches. The application must decide which is correct based on context or additional filtering.

## Best Practices

1. **Always resolve names first**: Never assume DCID format—always use the Resolve API
2. **Cache resolutions**: If querying the same places repeatedly, cache name→DCID mappings
3. **Handle ambiguity**: Check for multiple candidates and use `entity_type` filtering or more specific names
4. **Validate results**: Always check that `candidates` list is not empty before accessing DCIDs
5. **Use appropriate method**:
   - Names → `fetch_dcids_by_name()`
   - Coordinates → `fetch_dcid_by_coordinates()`
   - Wikidata IDs → `fetch_dcids_by_wikidata_id()`
