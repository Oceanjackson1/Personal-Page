---
title: "Fda Database"
description: "Query openFDA API for drugs, devices, adverse events, recalls, regulatory submissions (510k, PMA), substance identification (UNII), for FDA regulatory data analysis and safety research."
category: "research"
source: "community"
author: "Community"
tags: ["fda", "database"]
date: 2026-03-20
---

# FDA Database Access

## Overview

Access comprehensive FDA regulatory data through openFDA, the FDA's initiative to provide open APIs for public datasets. Query information about drugs, medical devices, foods, animal/veterinary products, and substances using Python with standardized interfaces.

**Key capabilities:**
- Query adverse events for drugs, devices, foods, and veterinary products
- Access product labeling, approvals, and regulatory submissions
- Monitor recalls and enforcement actions
- Look up National Drug Codes (NDC) and substance identifiers (UNII)
- Analyze device classifications and clearances (510k, PMA)
- Track drug shortages and supply issues
- Research chemical structures and substance relationships

## When to Use This Skill

This skill should be used when working with:
- **Drug research**: Safety profiles, adverse events, labeling, approvals, shortages
- **Medical device surveillance**: Adverse events, recalls, 510(k) clearances, PMA approvals
- **Food safety**: Recalls, allergen tracking, adverse events, dietary supplements
- **Veterinary medicine**: Animal drug adverse events by species and breed
- **Chemical/substance data**: UNII lookup, CAS number mapping, molecular structures
- **Regulatory analysis**: Approval pathways, enforcement actions, compliance tracking
- **Pharmacovigilance**: Post-market surveillance, safety signal detection
- **Scientific research**: Drug interactions, comparative safety, epidemiological studies

## Quick Start

### 1. Basic Setup

```python
from scripts.fda_query import FDAQuery

# Initialize (API key optional but recommended)
fda = FDAQuery(api_key="YOUR_API_KEY")

# Query drug adverse events
events = fda.query_drug_events("aspirin", limit=100)

# Get drug labeling
label = fda.query_drug_label("Lipitor", brand=True)

# Search device recalls
recalls = fda.query("device", "enforcement",
                   search="classification:Class+I",
                   limit=50)
```

### 2. API Key Setup

While the API works without a key, registering provides higher rate limits:
- **Without key**: 240 requests/min, 1,000/day
- **With key**: 240 requests/min, 120,000/day

Register at: https://open.fda.gov/apis/authentication/

Set as environment variable:
```bash
export FDA_API_KEY="your_key_here"
```

### 3. Running Examples

```bash
# Run comprehensive examples
python scripts/fda_examples.py

# This demonstrates:
# - Drug safety profiles
# - Device surveillance
# - Food recall monitoring
# - Substance lookup
# - Comparative drug analysis
# - Veterinary drug analysis
```

## FDA Database Categories

### Drugs

Access 6 drug-related endpoints covering the full drug lifecycle from approval to post-market surveillance.

**Endpoints:**
1. **Adverse Events** - Reports of side effects, errors, and therapeutic failures
2. **Product Labeling** - Prescribing information, warnings, indications
3. **NDC Directory** - National Drug Code product information
4. **Enforcement Reports** - Drug recalls and safety actions
5. **Drugs@FDA** - Historical approval data since 1939
6. **Drug Shortages** - Current and resolved supply issues

**Common use cases:**
```python
# Safety signal detection
fda.count_by_field("drug", "event",
                  search="patient.drug.medicinalproduct:metformin",
                  field="patient.reaction.reactionmeddrapt")

# Get prescribing information
label = fda.query_drug_label("Keytruda", brand=True)

# Check for recalls
recalls = fda.query_drug_recalls(drug_name="metformin")

# Monitor shortages
shortages = fda.query("drug", "drugshortages",
                     search="status:Currently+in+Shortage")
```

**Reference:** See `references/drugs.md` for detailed documentation

### Devices

Access 9 device-related endpoints covering medical device safety, approvals, and registrations.

**Endpoints:**
1. **Adverse Events** - Device malfunctions, injuries, deaths
2. **510(k) Clearances** - Premarket notifications
3. **Classification** - Device categories and risk classes
4. **Enforcement Reports** - Device recalls
5. **Recalls** - Detailed recall information
6. **PMA** - Premarket approval data for Class III devices
7. **Registrations & Listings** - Manufacturing facility data
8. **UDI** - Unique Device Identification database
9. **COVID-19 Serology** - Antibody test performance data

**Common use cases:**
```python
# Monitor device safety
events = fda.query_device_events("pacemaker", limit=100)

# Look up device classification
classification = fda.query_device_classification("DQY")

# Find 510(k) clearances
clearances = fda.query_device_510k(applicant="Medtronic")

# Search by UDI
device_info = fda.query("device", "udi",
                       search="identifiers.id:00884838003019")
```

**Reference:** See `references/devices.md` for detailed documentation

### Foods

Access 2 food-related endpoints for safety monitoring and recalls.

**Endpoints:**
1. **Adverse Events** - Food, dietary supplement, and cosmetic events
2. **Enforcement Reports** - Food product recalls

**Common use cases:**
```python
# Monitor allergen recalls
recalls = fda.query_food_recalls(reason="undeclared peanut")

# Track dietary supplement events
events = fda.query_food_events(
    industry="Dietary Supplements")

# Find contamination recalls
listeria = fda.query_food_recalls(
    reason="listeria",
    classification="I")
```

**Reference:** See `references/foods.md` for detailed documentation

### Animal & Veterinary

Access veterinary drug adverse event data with species-specific information.

**Endpoint:**
1. **Adverse Events** - Animal drug side effects by species, breed, and product

**Common use cases:**
```python
# Species-specific events
dog_events = fda.query_animal_events(
    species="Dog",
    drug_name="flea collar")

# Breed predisposition analysis
breed_query = fda.query("animalandveterinary", "event",
    search="reaction.veddra_term_name:*seizure*+AND+"
           "animal.breed.breed_component:*Labrador*")
```

**Reference:** See `references/animal_veterinary.md` for detailed documentation

### Substances & Other

Access molecular-level substance data with UNII codes, chemical structures, and relationships.

**Endpoints:**
1. **Substance Data** - UNII, CAS, chemical structures, relationships
2. **NSDE** - Historical substance data (legacy)

**Common use cases:**
```python
# UNII to CAS mapping
substance = fda.query_substance_by_unii("R16CO5Y76E")

# Search by name
results = fda.query_substance_by_name("acetaminophen")

# Get chemical structure
structure = fda.query("other", "substance",
    search="names.name:ibuprofen+AND+substanceClass:chemical")
```

**Reference:** See `references/other.md` for detailed documentation

## Common Query Patterns

### Pattern 1: Safety Profile Analysis

Create comprehensive safety profiles combining multiple data sources:

```python
def drug_safety_profile(fda, drug_name):
    """Generate complete safety profile."""

    # 1. Total adverse events
    events = fda.query_drug_events(drug_name, limit=1)
    total = events["meta"]["results"]["total"]

    # 2. Most common reactions
    reactions = fda.count_by_field(
        "drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*",
        field="patient.reaction.reactionmeddrapt",
        exact=True
    )

    # 3. Serious events
    serious = fda.query("drug", "event",
        search=f"patient.drug.medicinalproduct:*{drug_name}*+AND+serious:1",
        limit=1)

    # 4. Recent recalls
    recalls = fda.query_drug_recalls(drug_name=drug_name)

    return {
        "total_events": total,
        "top_reactions": reactions["results"][:10],
        "serious_events": serious["meta"]["results"]["total"],
        "recalls": recalls["results"]
    }
```

### Pattern 2: Temporal Trend Analysis

Analyze trends over time using date ranges:

```python
from datetime import datetime, timedelta

def get_monthly_trends(fda, drug_name, months=12):
    """Get monthly adverse event trends."""
    trends = []

    for i in range(months):
        end = datetime.now() - timedelta(days=30*i)
        start = end - timedelta(days=30)

        date_range = f"[{start.strftime('%Y%m%d')}+TO+{end.strftime('%Y%m%d')}]"
        search = f"patient.drug.medicinalproduct:*{drug_name}*+AND+receivedate:{date_range}"

        result = fda.query("drug", "event", search=search, limit=1)
        count = result["meta"]["results"]["total"] if "meta" in result else 0

        trends.append({
            "month": start.strftime("%Y-%m"),
            "events": count
        })

    return trends
```

### Pattern 3: Comparative Analysis

Compare multiple products side-by-side:

```python
def compare_drugs(fda, drug_list):
    """Compare safety profiles of multiple drugs."""
    comparison = {}

    for drug in drug_list:
        # Total events
        events = fda.query_drug_events(drug, limit=1)
        total = events["meta"]["results"]["total"] if "meta" in events else 0

        # Serious events
        serious = fda.query("drug", "event",
            search=f"patient.drug.medicinalproduct:*{drug}*+AND+serious:1",
            limit=1)
        serious_count = serious["meta"]["results"]["total"] if "meta" in serious else 0

        comparison[drug] = {
            "total_events": total,
            "serious_events": serious_count,
            "serious_rate": (serious_count/total*100) if total > 0 else 0
        }

    return comparison
```

### Pattern 4: Cross-Database Lookup

Link data across multiple endpoints:

```python
def comprehensive_device_lookup(fda, device_name):
    """Look up device across all relevant databases."""

    return {
        "adverse_events": fda.query_device_events(device_name, limit=10),
        "510k_clearances": fda.query_device_510k(device_name=device_name),
        "recalls": fda.query("device", "enforcement",
                           search=f"product_description:*{device_name}*"),
        "udi_info": fda.query("device", "udi",
                            search=f"brand_name:*{device_name}*")
    }
```

## Working with Results

### Response Structure

All API responses follow this structure:

```python
{
    "meta": {
        "disclaimer": "...",
        "results": {
            "skip": 0,
            "limit": 100,
            "total": 15234
        }
    },
    "results": [
        # Array of result objects
    ]
}
```

### Error Handling

Always handle potential errors:

```python
result = fda.query_drug_events("aspirin", limit=10)

if "error" in result:
    print(f"Error: {result['error']}")
elif "results" not in result or len(result["results"]) == 0:
    print("No results found")
else:
    # Process results
    for event in result["results"]:
        # Handle event data
        pass
```

### Pagination

For large result sets, use pagination:

```python
# Automatic pagination
all_results = fda.query_all(
    "drug", "event",
    search="patient.drug.medicinalproduct:aspirin",
    max_results=5000
)

# Manual pagination
for skip in range(0, 1000, 100):
    batch = fda.query("drug", "event",
                     search="...",
                     limit=100,
                     skip=skip)
    # Process batch
```

## Best Practices

### 1. Use Specific Searches

**DO:**
```python
# Specific field search
search="patient.drug.medicinalproduct:aspirin"
```

**DON'T:**
```python
# Overly broad wildcard
search="*aspirin*"
```

### 2. Implement Rate Limiting

The `FDAQuery` class handles rate limiting automatically, but be aware of limits:
- 240 requests per minute
- 120,000 requests per day (with API key)

### 3. Cache Frequently Accessed Data

The `FDAQuery` class includes built-in caching (enabled by default):

```python
# Caching is automatic
fda = FDAQuery(api_key=api_key, use_cache=True, cache_ttl=3600)
```

### 4. Use Exact Matching for Counting

When counting/aggregating, use `.exact` suffix:

```python
# Count exact phrases
fda.count_by_field("drug", "event",
                  search="...",
                  field="patient.reaction.reactionmeddrapt",
                  exact=True)  # Adds .exact automatically
```

### 5. Validate Input Data

Clean and validate search terms:

```python
def clean_drug_name(name):
    """Clean drug name for query."""
    return name.strip().replace('"', '\\"')

drug_name = clean_drug_name(user_input)
```

## API Reference

For detailed information about:
- **Authentication and rate limits** → See `references/api_basics.md`
- **Drug databases** → See `references/drugs.md`
- **Device databases** → See `references/devices.md`
- **Food databases** → See `references/foods.md`
- **Animal/veterinary databases** → See `references/animal_veterinary.md`
- **Substance databases** → See `references/other.md`

## Scripts

### `scripts/fda_query.py`

Main query module with `FDAQuery` class providing:
- Unified interface to all FDA endpoints
- Automatic rate limiting and caching
- Error handling and retry logic
- Common query patterns

### `scripts/fda_examples.py`

Comprehensive examples demonstrating:
- Drug safety profile analysis
- Device surveillance monitoring
- Food recall tracking
- Substance lookup
- Comparative drug analysis
- Veterinary drug analysis

Run examples:
```bash
python scripts/fda_examples.py
```

## Additional Resources

- **openFDA Homepage**: https://open.fda.gov/
- **API Documentation**: https://open.fda.gov/apis/
- **Interactive API Explorer**: https://open.fda.gov/apis/try-the-api/
- **GitHub Repository**: https://github.com/FDA/openfda
- **Terms of Service**: https://open.fda.gov/terms/

## Support and Troubleshooting

### Common Issues

**Issue**: Rate limit exceeded
- **Solution**: Use API key, implement delays, or reduce request frequency

**Issue**: No results found
- **Solution**: Try broader search terms, check spelling, use wildcards

**Issue**: Invalid query syntax
- **Solution**: Review query syntax in `references/api_basics.md`

**Issue**: Missing fields in results
- **Solution**: Not all records contain all fields; always check field existence

### Getting Help

- **GitHub Issues**: https://github.com/FDA/openfda/issues
- **Email**: open-fda@fda.hhs.gov

---

## Reference: Animal_Veterinary

# FDA Animal and Veterinary Databases

This reference covers FDA animal and veterinary medicine API endpoints accessible through openFDA.

## Overview

The FDA animal and veterinary databases provide access to information about adverse events related to animal drugs and veterinary medical products. These databases help monitor the safety of products used in companion animals, livestock, and other animals.

## Available Endpoints

### Animal Drug Adverse Events

**Endpoint**: `https://api.fda.gov/animalandveterinary/event.json`

**Purpose**: Access reports of side effects, product use errors, product quality problems, and therapeutic failures associated with animal drugs.

**Data Source**: FDA Center for Veterinary Medicine (CVM) Adverse Event Reporting System

**Key Fields**:
- `unique_aer_id_number` - Unique adverse event report identifier
- `report_id` - Report ID number
- `receiver.organization` - Organization receiving report
- `receiver.street_address` - Receiver address
- `receiver.city` - Receiver city
- `receiver.state` - Receiver state
- `receiver.postal_code` - Receiver postal code
- `receiver.country` - Receiver country
- `primary_reporter` - Primary reporter type (e.g., veterinarian, owner)
- `onset_date` - Date adverse event began
- `animal.species` - Animal species affected
- `animal.gender` - Animal gender
- `animal.age.min` - Minimum age
- `animal.age.max` - Maximum age
- `animal.age.unit` - Age unit (days, months, years)
- `animal.age.qualifier` - Age qualifier
- `animal.breed.is_crossbred` - Whether crossbred
- `animal.breed.breed_component` - Breed(s)
- `animal.weight.min` - Minimum weight
- `animal.weight.max` - Maximum weight
- `animal.weight.unit` - Weight unit
- `animal.female_animal_physiological_status` - Reproductive status
- `animal.reproductive_status` - Spayed/neutered status
- `drug` - Array of drugs involved
- `drug.active_ingredients` - Active ingredients
- `drug.active_ingredients.name` - Ingredient name
- `drug.active_ingredients.dose` - Dose information
- `drug.brand_name` - Brand name
- `drug.manufacturer.name` - Manufacturer
- `drug.administered_by` - Who administered drug
- `drug.route` - Route of administration
- `drug.dosage_form` - Dosage form
- `drug.atc_vet_code` - ATC veterinary code
- `reaction` - Array of adverse reactions
- `reaction.veddra_version` - VeDDRA dictionary version
- `reaction.veddra_term_code` - VeDDRA term code
- `reaction.veddra_term_name` - VeDDRA term name
- `reaction.accuracy` - Accuracy of diagnosis
- `reaction.number_of_animals_affected` - Number affected
- `reaction.number_of_animals_treated` - Number treated
- `outcome.medical_status` - Medical outcome
- `outcome.number_of_animals_affected` - Animals affected by outcome
- `serious_ae` - Whether serious adverse event
- `health_assessment_prior_to_exposure.assessed_by` - Who assessed health
- `health_assessment_prior_to_exposure.condition` - Health condition
- `treated_for_ae` - Whether treated
- `time_between_exposure_and_onset` - Time to onset
- `duration.unit` - Duration unit
- `duration.value` - Duration value

**Common Animal Species**:
- Dog (Canis lupus familiaris)
- Cat (Felis catus)
- Horse (Equus caballus)
- Cattle (Bos taurus)
- Pig (Sus scrofa domesticus)
- Chicken (Gallus gallus domesticus)
- Sheep (Ovis aries)
- Goat (Capra aegagrus hircus)
- And many others

**Common Use Cases**:
- Veterinary pharmacovigilance
- Product safety monitoring
- Adverse event trend analysis
- Drug safety comparison
- Species-specific safety research
- Breed predisposition studies

**Example Queries**:
```python
import requests

api_key = "YOUR_API_KEY"
url = "https://api.fda.gov/animalandveterinary/event.json"

# Find adverse events in dogs
params = {
    "api_key": api_key,
    "search": "animal.species:Dog",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
```

```python
# Search for specific drug adverse events
params = {
    "api_key": api_key,
    "search": "drug.brand_name:*flea+collar*",
    "limit": 20
}
```

```python
# Count most common reactions by species
params = {
    "api_key": api_key,
    "search": "animal.species:Cat",
    "count": "reaction.veddra_term_name.exact"
}
```

```python
# Find serious adverse events
params = {
    "api_key": api_key,
    "search": "serious_ae:true+AND+outcome.medical_status:Died",
    "limit": 50,
    "sort": "onset_date:desc"
}
```

```python
# Search by active ingredient
params = {
    "api_key": api_key,
    "search": "drug.active_ingredients.name:*ivermectin*",
    "limit": 25
}
```

```python
# Find events in specific breed
params = {
    "api_key": api_key,
    "search": "animal.breed.breed_component:*Labrador*",
    "limit": 30
}
```

```python
# Get events by route of administration
params = {
    "api_key": api_key,
    "search": "drug.route:*topical*",
    "limit": 40
}
```

## VeDDRA - Veterinary Dictionary for Drug Related Affairs

The Veterinary Dictionary for Drug Related Affairs (VeDDRA) is a standardized international veterinary terminology for adverse event reporting. It provides:

- Standardized terms for veterinary adverse events
- Hierarchical organization of terms
- Species-specific terminology
- International harmonization

**VeDDRA Term Structure**:
- Terms are organized hierarchically
- Each term has a unique code
- Terms are species-appropriate
- Multiple versions exist (check `veddra_version` field)

## Integration Tips

### Species-Specific Adverse Event Analysis

```python
def analyze_species_adverse_events(species, drug_name, api_key):
    """
    Analyze adverse events for a specific drug in a particular species.

    Args:
        species: Animal species (e.g., "Dog", "Cat", "Horse")
        drug_name: Drug brand name or active ingredient
        api_key: FDA API key

    Returns:
        Dictionary with analysis results
    """
    import requests
    from collections import Counter

    url = "https://api.fda.gov/animalandveterinary/event.json"
    params = {
        "api_key": api_key,
        "search": f"animal.species:{species}+AND+drug.brand_name:*{drug_name}*",
        "limit": 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return {"error": "No results found"}

    results = data["results"]

    # Collect reactions and outcomes
    reactions = []
    outcomes = []
    serious_count = 0

    for event in results:
        if "reaction" in event:
            for reaction in event["reaction"]:
                if "veddra_term_name" in reaction:
                    reactions.append(reaction["veddra_term_name"])

        if "outcome" in event:
            for outcome in event["outcome"]:
                if "medical_status" in outcome:
                    outcomes.append(outcome["medical_status"])

        if event.get("serious_ae") == "true":
            serious_count += 1

    reaction_counts = Counter(reactions)
    outcome_counts = Counter(outcomes)

    return {
        "total_events": len(results),
        "serious_events": serious_count,
        "most_common_reactions": reaction_counts.most_common(10),
        "outcome_distribution": dict(outcome_counts),
        "serious_percentage": round((serious_count / len(results)) * 100, 2) if len(results) > 0 else 0
    }
```

### Breed Predisposition Research

```python
def analyze_breed_predisposition(reaction_term, api_key, min_events=5):
    """
    Identify breed predispositions for specific adverse reactions.

    Args:
        reaction_term: VeDDRA reaction term to analyze
        api_key: FDA API key
        min_events: Minimum number of events to include breed

    Returns:
        List of breeds with event counts
    """
    import requests
    from collections import Counter

    url = "https://api.fda.gov/animalandveterinary/event.json"
    params = {
        "api_key": api_key,
        "search": f"reaction.veddra_term_name:*{reaction_term}*",
        "limit": 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return []

    breeds = []
    for event in data["results"]:
        if "animal" in event and "breed" in event["animal"]:
            breed_info = event["animal"]["breed"]
            if "breed_component" in breed_info:
                if isinstance(breed_info["breed_component"], list):
                    breeds.extend(breed_info["breed_component"])
                else:
                    breeds.append(breed_info["breed_component"])

    breed_counts = Counter(breeds)

    # Filter by minimum events
    filtered_breeds = [
        {"breed": breed, "count": count}
        for breed, count in breed_counts.most_common()
        if count >= min_events
    ]

    return filtered_breeds
```

### Comparative Drug Safety

```python
def compare_drug_safety(drug_list, species, api_key):
    """
    Compare safety profiles of multiple drugs for a specific species.

    Args:
        drug_list: List of drug names to compare
        species: Animal species
        api_key: FDA API key

    Returns:
        Dictionary comparing drugs
    """
    import requests

    url = "https://api.fda.gov/animalandveterinary/event.json"
    comparison = {}

    for drug in drug_list:
        params = {
            "api_key": api_key,
            "search": f"animal.species:{species}+AND+drug.brand_name:*{drug}*",
            "limit": 1000
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data:
            results = data["results"]
            serious = sum(1 for r in results if r.get("serious_ae") == "true")
            deaths = sum(
                1 for r in results
                if "outcome" in r
                and any(o.get("medical_status") == "Died" for o in r["outcome"])
            )

            comparison[drug] = {
                "total_events": len(results),
                "serious_events": serious,
                "deaths": deaths,
                "serious_rate": round((serious / len(results)) * 100, 2) if len(results) > 0 else 0,
                "death_rate": round((deaths / len(results)) * 100, 2) if len(results) > 0 else 0
            }

    return comparison
```

## Best Practices

1. **Use standard species names** - Full scientific or common names work best
2. **Consider breed variations** - Spelling and naming can vary
3. **Check VeDDRA versions** - Terms may change between versions
4. **Account for reporter bias** - Veterinarians vs. owners report differently
5. **Filter by serious events** - Focus on clinically significant reactions
6. **Consider animal demographics** - Age, weight, and reproductive status matter
7. **Track temporal patterns** - Seasonal variations may exist
8. **Cross-reference products** - Same active ingredient may have multiple brands
9. **Analyze by route** - Topical vs. systemic administration affects safety
10. **Consider species differences** - Drugs affect species differently

## Reporting Sources

Animal drug adverse event reports come from:
- **Veterinarians** - Professional medical observations
- **Animal owners** - Direct observations and concerns
- **Pharmaceutical companies** - Required post-market surveillance
- **FDA field staff** - Official investigations
- **Research institutions** - Clinical studies
- **Other sources** - Varies

Different sources may have different reporting thresholds and detail levels.

## Additional Resources

- OpenFDA Animal & Veterinary API: https://open.fda.gov/apis/animalandveterinary/
- FDA Center for Veterinary Medicine: https://www.fda.gov/animal-veterinary
- VeDDRA: https://www.veddra.org/
- API Basics: See `api_basics.md` in this references directory
- Python examples: See `scripts/fda_animal_query.py`

---

## Reference: Api_Basics

# OpenFDA API Basics

This reference provides comprehensive information about using the openFDA API, including authentication, rate limits, query syntax, and best practices.

## Getting Started

### Base URL

All openFDA API endpoints follow this structure:
```
https://api.fda.gov/{category}/{endpoint}.json
```

Examples:
- `https://api.fda.gov/drug/event.json`
- `https://api.fda.gov/device/510k.json`
- `https://api.fda.gov/food/enforcement.json`

### HTTPS Required

**All requests must use HTTPS**. HTTP requests are not accepted and will fail.

## Authentication

### API Key Registration

While openFDA can be used without an API key, registering for a free API key is strongly recommended for higher rate limits.

**Registration**: Visit https://open.fda.gov/apis/authentication/ to sign up

**Benefits of API Key**:
- Higher rate limits (240 req/min, 120,000 req/day)
- Better for production applications
- No additional cost

### Using Your API Key

Include your API key in requests using one of two methods:

**Method 1: Query Parameter (Recommended)**
```python
import requests

api_key = "YOUR_API_KEY_HERE"
url = "https://api.fda.gov/drug/event.json"

params = {
    "api_key": api_key,
    "search": "patient.drug.medicinalproduct:aspirin",
    "limit": 10
}

response = requests.get(url, params=params)
```

**Method 2: Basic Authentication**
```python
import requests

api_key = "YOUR_API_KEY_HERE"
url = "https://api.fda.gov/drug/event.json"

params = {
    "search": "patient.drug.medicinalproduct:aspirin",
    "limit": 10
}

response = requests.get(url, params=params, auth=(api_key, ''))
```

## Rate Limits

### Current Limits

| Status | Requests per Minute | Requests per Day |
|--------|-------------------|------------------|
| **Without API Key** | 240 per IP address | 1,000 per IP address |
| **With API Key** | 240 per key | 120,000 per key |

### Rate Limit Headers

The API returns rate limit information in response headers:
```python
response = requests.get(url, params=params)

print(f"Rate limit: {response.headers.get('X-RateLimit-Limit')}")
print(f"Remaining: {response.headers.get('X-RateLimit-Remaining')}")
print(f"Reset time: {response.headers.get('X-RateLimit-Reset')}")
```

### Handling Rate Limits

When you exceed rate limits, the API returns:
- **Status Code**: `429 Too Many Requests`
- **Error Message**: Indicates rate limit exceeded

**Best Practice**: Implement exponential backoff:
```python
import requests
import time

def query_with_rate_limit_handling(url, params, max_retries=3):
    """Query API with automatic rate limit handling."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                # Rate limit exceeded
                wait_time = (2 ** attempt) * 60  # Exponential backoff
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Increasing Limits

For applications requiring higher limits, contact the openFDA team through their website with details about your use case.

## Query Syntax

### Basic Structure

Queries use this format:
```
?api_key=YOUR_KEY&parameter=value&parameter2=value2
```

Parameters are separated by ampersands (`&`).

### Search Parameter

The `search` parameter is the primary way to filter results.

**Basic Format**:
```
search=field:value
```

**Example**:
```python
params = {
    "api_key": api_key,
    "search": "patient.drug.medicinalproduct:aspirin"
}
```

### Search Operators

#### AND Operator
Combines multiple conditions (both must be true):
```python
# Find aspirin adverse events in Canada
params = {
    "search": "patient.drug.medicinalproduct:aspirin+AND+occurcountry:ca"
}
```

#### OR Operator
Either condition can be true (OR is implicit with space):
```python
# Find aspirin OR ibuprofen
params = {
    "search": "patient.drug.medicinalproduct:(aspirin ibuprofen)"
}
```

Or explicitly:
```python
params = {
    "search": "patient.drug.medicinalproduct:aspirin+OR+patient.drug.medicinalproduct:ibuprofen"
}
```

#### NOT Operator
Exclude results:
```python
# Events NOT in the United States
params = {
    "search": "_exists_:occurcountry+AND+NOT+occurcountry:us"
}
```

#### Wildcards
Use asterisk (`*`) for partial matching:
```python
# Any drug starting with "met"
params = {
    "search": "patient.drug.medicinalproduct:met*"
}

# Any drug containing "cillin"
params = {
    "search": "patient.drug.medicinalproduct:*cillin*"
}
```

#### Exact Phrase Matching
Use quotes for exact phrases:
```python
params = {
    "search": 'patient.reaction.reactionmeddrapt:"heart attack"'
}
```

#### Range Queries
Search within ranges:
```python
# Date range (YYYYMMDD format)
params = {
    "search": "receivedate:[20200101+TO+20201231]"
}

# Numeric range
params = {
    "search": "patient.patientonsetage:[18+TO+65]"
}

# Open-ended ranges
params = {
    "search": "patient.patientonsetage:[65+TO+*]"  # 65 and older
}
```

#### Field Existence
Check if a field exists:
```python
# Records that have a patient age
params = {
    "search": "_exists_:patient.patientonsetage"
}

# Records missing patient age
params = {
    "search": "_missing_:patient.patientonsetage"
}
```

### Limit Parameter

Controls how many results to return (1-1000, default 1):
```python
params = {
    "search": "...",
    "limit": 100
}
```

**Maximum**: 1000 results per request

### Skip Parameter

For pagination, skip the first N results:
```python
# Get results 101-200
params = {
    "search": "...",
    "limit": 100,
    "skip": 100
}
```

**Pagination Example**:
```python
def get_all_results(url, search_query, api_key, max_results=5000):
    """Retrieve results with pagination."""
    all_results = []
    skip = 0
    limit = 100

    while len(all_results) < max_results:
        params = {
            "api_key": api_key,
            "search": search_query,
            "limit": limit,
            "skip": skip
        }

        response = requests.get(url, params=params)
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            break

        all_results.extend(data["results"])

        if len(data["results"]) < limit:
            break  # No more results

        skip += limit
        time.sleep(0.25)  # Rate limiting courtesy

    return all_results[:max_results]
```

### Count Parameter

Aggregate and count results by a field (instead of returning individual records):
```python
# Count events by country
params = {
    "search": "patient.drug.medicinalproduct:aspirin",
    "count": "occurcountry"
}
```

**Response Format**:
```json
{
  "results": [
    {"term": "us", "count": 12543},
    {"term": "ca", "count": 3421},
    {"term": "gb", "count": 2156}
  ]
}
```

#### Exact Counting

Add `.exact` suffix for exact phrase counting (especially important for multi-word fields):
```python
# Count exact reaction terms (not individual words)
params = {
    "search": "patient.drug.medicinalproduct:aspirin",
    "count": "patient.reaction.reactionmeddrapt.exact"
}
```

**Without `.exact`**: Counts individual words
**With `.exact`**: Counts complete phrases

### Sort Parameter

Sort results by field:
```python
# Sort by date, newest first
params = {
    "search": "...",
    "sort": "receivedate:desc"
}

# Sort by date, oldest first
params = {
    "search": "...",
    "sort": "receivedate:asc"
}
```

## Response Format

### Standard Response Structure

```json
{
  "meta": {
    "disclaimer": "...",
    "terms": "...",
    "license": "...",
    "last_updated": "2024-01-15",
    "results": {
      "skip": 0,
      "limit": 10,
      "total": 15234
    }
  },
  "results": [
    {
      // Individual result record
    },
    {
      // Another result record
    }
  ]
}
```

### Response Fields

- **meta**: Metadata about the query and results
  - `disclaimer`: Important legal disclaimer
  - `terms`: Terms of use URL
  - `license`: Data license information
  - `last_updated`: When data was last updated
  - `results.skip`: Number of skipped results
  - `results.limit`: Maximum results per page
  - `results.total`: Total matching results (may be approximate for large result sets)

- **results**: Array of matching records

### Empty Results

When no results match:
```json
{
  "meta": {...},
  "results": []
}
```

### Error Response

When an error occurs:
```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Detailed error message"
  }
}
```

**Common Error Codes**:
- `NOT_FOUND`: No results found (404)
- `INVALID_QUERY`: Malformed search query (400)
- `RATE_LIMIT_EXCEEDED`: Too many requests (429)
- `UNAUTHORIZED`: Invalid API key (401)
- `SERVER_ERROR`: Internal server error (500)

## Advanced Techniques

### Nested Field Queries

Query nested objects:
```python
# Drug adverse events where serious outcome is death
params = {
    "search": "serious:1+AND+seriousnessdeath:1"
}
```

### Multiple Field Search

Search across multiple fields:
```python
# Search drug name in multiple fields
params = {
    "search": "(patient.drug.medicinalproduct:aspirin+OR+patient.drug.openfda.brand_name:aspirin)"
}
```

### Complex Boolean Logic

Combine multiple operators:
```python
# (Aspirin OR Ibuprofen) AND (Heart Attack) AND NOT (US)
params = {
    "search": "(patient.drug.medicinalproduct:aspirin+OR+patient.drug.medicinalproduct:ibuprofen)+AND+patient.reaction.reactionmeddrapt:*heart*attack*+AND+NOT+occurcountry:us"
}
```

### Counting with Filters

Count within a specific subset:
```python
# Count reactions for serious events only
params = {
    "search": "serious:1",
    "count": "patient.reaction.reactionmeddrapt.exact"
}
```

## Best Practices

### 1. Query Efficiency

**DO**:
- Use specific field searches
- Filter before counting
- Use exact match when possible
- Implement pagination for large datasets

**DON'T**:
- Use overly broad wildcards (e.g., `search=*`)
- Request more data than needed
- Skip error handling
- Ignore rate limits

### 2. Error Handling

Always handle common errors:
```python
def safe_api_call(url, params):
    """Safely call FDA API with comprehensive error handling."""
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "No results found"}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded"}
        elif response.status_code == 400:
            return {"error": "Invalid query"}
        else:
            return {"error": f"HTTP error: {e}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}
```

### 3. Data Validation

Validate and clean data:
```python
def clean_search_term(term):
    """Clean and prepare search term."""
    # Remove special characters that break queries
    term = term.replace('"', '\\"')  # Escape quotes
    term = term.strip()
    return term

def validate_date(date_str):
    """Validate date format (YYYYMMDD)."""
    import re
    if not re.match(r'^\d{8}$', date_str):
        raise ValueError("Date must be in YYYYMMDD format")
    return date_str
```

### 4. Caching

Implement caching for frequently accessed data:
```python
import json
from pathlib import Path
import hashlib
import time

class FDACache:
    """Simple file-based cache for FDA API responses."""

    def __init__(self, cache_dir="fda_cache", ttl=3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = ttl  # Time to live in seconds

    def _get_cache_key(self, url, params):
        """Generate cache key from URL and params."""
        cache_string = f"{url}_{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    def get(self, url, params):
        """Get cached response if available and not expired."""
        key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            # Check if expired
            age = time.time() - cache_file.stat().st_mtime
            if age < self.ttl:
                with open(cache_file, 'r') as f:
                    return json.load(f)

        return None

    def set(self, url, params, data):
        """Cache response data."""
        key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{key}.json"

        with open(cache_file, 'w') as f:
            json.dump(data, f)

# Usage
cache = FDACache(ttl=3600)  # 1 hour cache

def cached_api_call(url, params):
    """API call with caching."""
    # Check cache
    cached = cache.get(url, params)
    if cached:
        return cached

    # Make request
    response = requests.get(url, params=params)
    data = response.json()

    # Cache result
    cache.set(url, params, data)

    return data
```

### 5. Rate Limit Management

Track and respect rate limits:
```python
import time
from collections import deque

class RateLimiter:
    """Track and enforce rate limits."""

    def __init__(self, max_per_minute=240):
        self.max_per_minute = max_per_minute
        self.requests = deque()

    def wait_if_needed(self):
        """Wait if necessary to stay under rate limit."""
        now = time.time()

        # Remove requests older than 1 minute
        while self.requests and now - self.requests[0] > 60:
            self.requests.popleft()

        # Check if at limit
        if len(self.requests) >= self.max_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.requests.popleft()

        self.requests.append(time.time())

# Usage
rate_limiter = RateLimiter(max_per_minute=240)

def rate_limited_request(url, params):
    """Make request with rate limiting."""
    rate_limiter.wait_if_needed()
    return requests.get(url, params=params)
```

## Common Query Patterns

### Pattern 1: Time-based Analysis
```python
# Get events from last 30 days
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=30)

params = {
    "search": f"receivedate:[{start_date.strftime('%Y%m%d')}+TO+{end_date.strftime('%Y%m%d')}]",
    "limit": 1000
}
```

### Pattern 2: Top N Analysis
```python
# Get top 10 most common reactions for a drug
params = {
    "search": "patient.drug.medicinalproduct:aspirin",
    "count": "patient.reaction.reactionmeddrapt.exact",
    "limit": 10
}
```

### Pattern 3: Comparative Analysis
```python
# Compare two drugs
drugs = ["aspirin", "ibuprofen"]
results = {}

for drug in drugs:
    params = {
        "search": f"patient.drug.medicinalproduct:{drug}",
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": 10
    }
    results[drug] = requests.get(url, params=params).json()
```

## Additional Resources

- **openFDA Homepage**: https://open.fda.gov/
- **API Documentation**: https://open.fda.gov/apis/
- **Interactive API Explorer**: https://open.fda.gov/apis/try-the-api/
- **Terms of Service**: https://open.fda.gov/terms/
- **GitHub**: https://github.com/FDA/openfda
- **Status Page**: Check for API outages and maintenance

## Support

For questions or issues:
- **GitHub Issues**: https://github.com/FDA/openfda/issues
- **Email**: open-fda@fda.hhs.gov
- **Discussion Forum**: Check GitHub discussions

---

## Reference: Devices

# FDA Medical Device Databases

This reference covers all FDA medical device-related API endpoints accessible through openFDA.

## Overview

The FDA device databases provide access to information about medical devices, including adverse events, recalls, approvals, registrations, and classification data. Medical devices range from simple items like tongue depressors to complex instruments like pacemakers and surgical robots.

## Device Classification System

Medical devices are classified into three categories based on risk:

- **Class I**: Low risk (e.g., bandages, examination gloves)
- **Class II**: Moderate risk (e.g., powered wheelchairs, infusion pumps)
- **Class III**: High risk (e.g., heart valves, implantable pacemakers)

## Available Endpoints

### 1. Device Adverse Events

**Endpoint**: `https://api.fda.gov/device/event.json`

**Purpose**: Access reports documenting serious injuries, deaths, malfunctions, and other undesirable effects from medical device use.

**Data Source**: Manufacturer and User Facility Device Experience (MAUDE) database

**Key Fields**:
- `device.brand_name` - Brand name of device
- `device.generic_name` - Generic device name
- `device.manufacturer_d_name` - Manufacturer name
- `device.device_class` - Device class (1, 2, or 3)
- `event_type` - Type of event (Death, Injury, Malfunction, Other)
- `date_received` - Date FDA received report
- `mdr_report_key` - Unique report identifier
- `adverse_event_flag` - Whether reported as adverse event
- `product_problem_flag` - Whether product problem reported
- `patient.patient_problems` - Patient problems/complications
- `device.openfda.device_name` - Official device name
- `device.openfda.medical_specialty_description` - Medical specialty
- `remedial_action` - Actions taken (recall, repair, replace, etc.)

**Common Use Cases**:
- Post-market surveillance
- Safety signal detection
- Device comparison studies
- Risk analysis
- Quality improvement

**Example Queries**:
```python
import requests

api_key = "YOUR_API_KEY"
url = "https://api.fda.gov/device/event.json"

# Find adverse events for a specific device
params = {
    "api_key": api_key,
    "search": "device.brand_name:pacemaker",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
```

```python
# Count events by type
params = {
    "api_key": api_key,
    "search": "device.generic_name:insulin+pump",
    "count": "event_type"
}
```

```python
# Find death events for Class III devices
params = {
    "api_key": api_key,
    "search": "event_type:Death+AND+device.device_class:3",
    "limit": 50,
    "sort": "date_received:desc"
}
```

### 2. Device 510(k) Clearances

**Endpoint**: `https://api.fda.gov/device/510k.json`

**Purpose**: Access 510(k) premarket notification data demonstrating device equivalence to legally marketed predicate devices.

**Data Source**: 510(k) Premarket Notifications

**Key Fields**:
- `k_number` - 510(k) number (unique identifier)
- `applicant` - Company submitting 510(k)
- `device_name` - Name of device
- `device_class` - Device classification (1, 2, or 3)
- `decision_date` - Date of FDA decision
- `decision_description` - Substantially Equivalent (SE) or Not SE
- `product_code` - FDA product code
- `statement_or_summary` - Type of summary provided
- `clearance_type` - Traditional, Special, Abbreviated, etc.
- `expedited_review_flag` - Whether expedited review
- `advisory_committee` - Advisory committee name
- `openfda.device_name` - Official device name
- `openfda.device_class` - Device class description
- `openfda.medical_specialty_description` - Medical specialty
- `openfda.regulation_number` - CFR regulation number

**Common Use Cases**:
- Regulatory pathway research
- Predicate device identification
- Market entry analysis
- Competitive intelligence
- Device development planning

**Example Queries**:
```python
# Find 510(k) clearances by company
params = {
    "api_key": api_key,
    "search": "applicant:Medtronic",
    "limit": 50,
    "sort": "decision_date:desc"
}

response = requests.get("https://api.fda.gov/device/510k.json", params=params)
```

```python
# Search for specific device type clearances
params = {
    "api_key": api_key,
    "search": "device_name:*surgical+robot*",
    "limit": 10
}
```

```python
# Get all Class III 510(k) clearances in recent year
params = {
    "api_key": api_key,
    "search": "device_class:3+AND+decision_date:[20240101+TO+20241231]",
    "limit": 100
}
```

### 3. Device Classification

**Endpoint**: `https://api.fda.gov/device/classification.json`

**Purpose**: Access device classification database with medical device names, product codes, medical specialty panels, and classification information.

**Data Source**: FDA Device Classification Database

**Key Fields**:
- `product_code` - Three-letter FDA product code
- `device_name` - Official device name
- `device_class` - Class (1, 2, or 3)
- `medical_specialty` - Medical specialty (e.g., Radiology, Cardiovascular)
- `medical_specialty_description` - Full specialty description
- `regulation_number` - CFR regulation number (e.g., 21 CFR 870.2300)
- `review_panel` - FDA review panel
- `definition` - Official device definition
- `physical_state` - Solid, liquid, gas
- `technical_method` - Method of operation
- `target_area` - Body area/system targeted
- `gmp_exempt_flag` - Whether exempt from Good Manufacturing Practice
- `implant_flag` - Whether device is implanted
- `life_sustain_support_flag` - Whether life-sustaining/supporting

**Common Use Cases**:
- Device identification
- Regulatory requirement determination
- Product code lookup
- Classification research
- Device categorization

**Example Queries**:
```python
# Look up device by product code
params = {
    "api_key": api_key,
    "search": "product_code:LWL",
    "limit": 1
}

response = requests.get("https://api.fda.gov/device/classification.json", params=params)
```

```python
# Find all cardiovascular devices
params = {
    "api_key": api_key,
    "search": "medical_specialty:CV",
    "limit": 100
}
```

```python
# Get all implantable Class III devices
params = {
    "api_key": api_key,
    "search": "device_class:3+AND+implant_flag:Y",
    "limit": 50
}
```

### 4. Device Recall Enforcement Reports

**Endpoint**: `https://api.fda.gov/device/enforcement.json`

**Purpose**: Access medical device product recall enforcement reports.

**Data Source**: FDA Enforcement Reports

**Key Fields**:
- `status` - Current status (Ongoing, Completed, Terminated)
- `recall_number` - Unique recall identifier
- `classification` - Class I, II, or III
- `product_description` - Description of recalled device
- `reason_for_recall` - Why device was recalled
- `product_quantity` - Amount of product recalled
- `code_info` - Lot numbers, serial numbers, model numbers
- `distribution_pattern` - Geographic distribution
- `recalling_firm` - Company conducting recall
- `recall_initiation_date` - When recall began
- `report_date` - When FDA received notice
- `product_res_number` - Product problem number

**Common Use Cases**:
- Quality monitoring
- Supply chain risk management
- Patient safety tracking
- Regulatory compliance
- Device surveillance

**Example Queries**:
```python
# Find all Class I device recalls (most serious)
params = {
    "api_key": api_key,
    "search": "classification:Class+I",
    "limit": 20,
    "sort": "report_date:desc"
}

response = requests.get("https://api.fda.gov/device/enforcement.json", params=params)
```

```python
# Search recalls by manufacturer
params = {
    "api_key": api_key,
    "search": "recalling_firm:*Philips*",
    "limit": 50
}
```

### 5. Device Recalls

**Endpoint**: `https://api.fda.gov/device/recall.json`

**Purpose**: Access information about device recalls addressing problems that violate FDA law or pose health risks.

**Data Source**: FDA Recalls Database

**Key Fields**:
- `res_event_number` - Recall event number
- `product_code` - FDA product code
- `openfda.device_name` - Device name
- `openfda.device_class` - Device class
- `product_res_number` - Product recall number
- `firm_fei_number` - Firm establishment identifier
- `k_numbers` - Associated 510(k) numbers
- `pma_numbers` - Associated PMA numbers
- `root_cause_description` - Root cause of issue

**Common Use Cases**:
- Recall tracking
- Quality investigation
- Root cause analysis
- Trend identification

**Example Queries**:
```python
# Search recalls by product code
params = {
    "api_key": api_key,
    "search": "product_code:DQY",
    "limit": 20
}

response = requests.get("https://api.fda.gov/device/recall.json", params=params)
```

### 6. Premarket Approval (PMA)

**Endpoint**: `https://api.fda.gov/device/pma.json`

**Purpose**: Access data from FDA's premarket approval process for Class III medical devices.

**Data Source**: PMA Database

**Key Fields**:
- `pma_number` - PMA application number (e.g., P850005)
- `supplement_number` - Supplement number if applicable
- `applicant` - Company name
- `trade_name` - Trade/brand name
- `generic_name` - Generic name
- `product_code` - FDA product code
- `decision_date` - Date of FDA decision
- `decision_code` - Approval status (APPR = approved)
- `advisory_committee` - Advisory committee
- `openfda.device_name` - Official device name
- `openfda.device_class` - Device class
- `openfda.medical_specialty_description` - Medical specialty
- `openfda.regulation_number` - Regulation number

**Common Use Cases**:
- High-risk device research
- Approval timeline analysis
- Regulatory strategy
- Market intelligence
- Clinical trial planning

**Example Queries**:
```python
# Find PMA approvals by company
params = {
    "api_key": api_key,
    "search": "applicant:Boston+Scientific",
    "limit": 50
}

response = requests.get("https://api.fda.gov/device/pma.json", params=params)
```

```python
# Search for specific device PMAs
params = {
    "api_key": api_key,
    "search": "generic_name:*cardiac+pacemaker*",
    "limit": 10
}
```

### 7. Registrations and Listings

**Endpoint**: `https://api.fda.gov/device/registrationlisting.json`

**Purpose**: Access location data for medical device establishments and devices they manufacture.

**Data Source**: Device Registration and Listing Database

**Key Fields**:
- `registration.fei_number` - Facility establishment identifier
- `registration.name` - Facility name
- `registration.registration_number` - Registration number
- `registration.reg_expiry_date_year` - Registration expiration year
- `registration.address_line_1` - Street address
- `registration.city` - City
- `registration.state_code` - State/province
- `registration.iso_country_code` - Country code
- `registration.zip_code` - Postal code
- `products.product_code` - Device product code
- `products.created_date` - When device was listed
- `products.openfda.device_name` - Device name
- `products.openfda.device_class` - Device class
- `proprietary_name` - Proprietary/brand names
- `establishment_type` - Types of operations (manufacturer, etc.)

**Common Use Cases**:
- Manufacturer identification
- Facility location lookup
- Supply chain mapping
- Due diligence research
- Market analysis

**Example Queries**:
```python
# Find registered facilities by country
params = {
    "api_key": api_key,
    "search": "registration.iso_country_code:US",
    "limit": 100
}

response = requests.get("https://api.fda.gov/device/registrationlisting.json", params=params)
```

```python
# Search by facility name
params = {
    "api_key": api_key,
    "search": "registration.name:*Johnson*",
    "limit": 10
}
```

### 8. Unique Device Identification (UDI)

**Endpoint**: `https://api.fda.gov/device/udi.json`

**Purpose**: Access the Global Unique Device Identification Database (GUDID) containing device identification information.

**Data Source**: GUDID

**Key Fields**:
- `identifiers.id` - Device identifier (DI)
- `identifiers.issuing_agency` - Issuing agency (GS1, HIBCC, ICCBBA)
- `identifiers.type` - Primary or Package DI
- `brand_name` - Brand name
- `version_model_number` - Version/model number
- `catalog_number` - Catalog number
- `company_name` - Device company
- `device_count_in_base_package` - Quantity in base package
- `device_description` - Description
- `is_rx` - Prescription device (true/false)
- `is_otc` - Over-the-counter device (true/false)
- `is_combination_product` - Combination product (true/false)
- `is_kit` - Kit (true/false)
- `is_labeled_no_nrl` - Latex-free labeled
- `has_lot_or_batch_number` - Uses lot/batch numbers
- `has_serial_number` - Uses serial numbers
- `has_manufacturing_date` - Has manufacturing date
- `has_expiration_date` - Has expiration date
- `mri_safety` - MRI safety status
- `gmdn_terms` - Global Medical Device Nomenclature terms
- `product_codes` - FDA product codes
- `storage` - Storage requirements
- `customer_contacts` - Contact information

**Common Use Cases**:
- Device identification and verification
- Supply chain tracking
- Adverse event reporting
- Inventory management
- Procurement

**Example Queries**:
```python
# Look up device by UDI
params = {
    "api_key": api_key,
    "search": "identifiers.id:00884838003019",
    "limit": 1
}

response = requests.get("https://api.fda.gov/device/udi.json", params=params)
```

```python
# Find prescription devices by brand name
params = {
    "api_key": api_key,
    "search": "brand_name:*insulin+pump*+AND+is_rx:true",
    "limit": 10
}
```

```python
# Search for MRI safe devices
params = {
    "api_key": api_key,
    "search": 'mri_safety:"MR Safe"',
    "limit": 50
}
```

### 9. COVID-19 Serological Testing Evaluations

**Endpoint**: `https://api.fda.gov/device/covid19serology.json`

**Purpose**: Access FDA's independent evaluations of COVID-19 antibody tests.

**Data Source**: FDA COVID-19 Serology Test Performance

**Key Fields**:
- `manufacturer` - Test manufacturer
- `device` - Device/test name
- `authorization_status` - EUA status
- `control_panel` - Control panel used for evaluation
- `sample_sensitivity_report_one` - Sensitivity data (first report)
- `sample_specificity_report_one` - Specificity data (first report)
- `sample_sensitivity_report_two` - Sensitivity data (second report)
- `sample_specificity_report_two` - Specificity data (second report)

**Common Use Cases**:
- Test performance comparison
- Diagnostic accuracy assessment
- Procurement decision support
- Quality assurance

**Example Queries**:
```python
# Find tests by manufacturer
params = {
    "api_key": api_key,
    "search": "manufacturer:Abbott",
    "limit": 10
}

response = requests.get("https://api.fda.gov/device/covid19serology.json", params=params)
```

```python
# Get all tests with EUA
params = {
    "api_key": api_key,
    "search": "authorization_status:*EUA*",
    "limit": 100
}
```

## Integration Tips

### Comprehensive Device Search

```python
def search_device_across_databases(device_name, api_key):
    """
    Search for a device across multiple FDA databases.

    Args:
        device_name: Name or partial name of device
        api_key: FDA API key

    Returns:
        Dictionary with results from each database
    """
    results = {}

    # Search adverse events
    events_url = "https://api.fda.gov/device/event.json"
    events_params = {
        "api_key": api_key,
        "search": f"device.brand_name:*{device_name}*",
        "limit": 10
    }
    results["adverse_events"] = requests.get(events_url, params=events_params).json()

    # Search 510(k) clearances
    fiveten_url = "https://api.fda.gov/device/510k.json"
    fiveten_params = {
        "api_key": api_key,
        "search": f"device_name:*{device_name}*",
        "limit": 10
    }
    results["510k_clearances"] = requests.get(fiveten_url, params=fiveten_params).json()

    # Search recalls
    recall_url = "https://api.fda.gov/device/enforcement.json"
    recall_params = {
        "api_key": api_key,
        "search": f"product_description:*{device_name}*",
        "limit": 10
    }
    results["recalls"] = requests.get(recall_url, params=recall_params).json()

    # Search UDI
    udi_url = "https://api.fda.gov/device/udi.json"
    udi_params = {
        "api_key": api_key,
        "search": f"brand_name:*{device_name}*",
        "limit": 10
    }
    results["udi"] = requests.get(udi_url, params=udi_params).json()

    return results
```

### Product Code Lookup

```python
def get_device_classification(product_code, api_key):
    """
    Get detailed classification information for a device product code.

    Args:
        product_code: Three-letter FDA product code
        api_key: FDA API key

    Returns:
        Classification details dictionary
    """
    url = "https://api.fda.gov/device/classification.json"
    params = {
        "api_key": api_key,
        "search": f"product_code:{product_code}",
        "limit": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        classification = data["results"][0]
        return {
            "product_code": classification.get("product_code"),
            "device_name": classification.get("device_name"),
            "device_class": classification.get("device_class"),
            "regulation_number": classification.get("regulation_number"),
            "medical_specialty": classification.get("medical_specialty_description"),
            "gmp_exempt": classification.get("gmp_exempt_flag") == "Y",
            "implant": classification.get("implant_flag") == "Y",
            "life_sustaining": classification.get("life_sustain_support_flag") == "Y"
        }
    return None
```

## Best Practices

1. **Use product codes** - Most efficient way to search across device databases
2. **Check multiple databases** - Device information is spread across multiple endpoints
3. **Handle large result sets** - Device databases can be very large; use pagination
4. **Validate device identifiers** - Ensure UDIs, 510(k) numbers, and PMA numbers are properly formatted
5. **Filter by device class** - Narrow searches by risk classification when relevant
6. **Use exact brand names** - Wildcards work but exact matches are more reliable
7. **Consider date ranges** - Device data accumulates over decades; filter by date when appropriate
8. **Cross-reference data** - Link adverse events to recalls and registrations for complete picture
9. **Monitor recall status** - Recall statuses change from "Ongoing" to "Completed"
10. **Check establishment registrations** - Facilities must register annually; check expiration dates

## Additional Resources

- OpenFDA Device API Documentation: https://open.fda.gov/apis/device/
- Device Classification Database: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpcd/classification.cfm
- GUDID: https://accessgudid.nlm.nih.gov/
- API Basics: See `api_basics.md` in this references directory
- Python examples: See `scripts/fda_device_query.py`

---

## Reference: Drugs

# FDA Drug Databases

This reference covers all FDA drug-related API endpoints accessible through openFDA.

## Overview

The FDA drug databases provide access to information about pharmaceutical products, including adverse events, labeling, recalls, approvals, and shortages. All endpoints follow the openFDA API structure and return JSON-formatted data.

## Available Endpoints

### 1. Drug Adverse Events

**Endpoint**: `https://api.fda.gov/drug/event.json`

**Purpose**: Access reports of drug side effects, product use errors, product quality problems, and therapeutic failures submitted to the FDA.

**Data Source**: FDA Adverse Event Reporting System (FAERS)

**Key Fields**:
- `patient.drug.medicinalproduct` - Drug name
- `patient.drug.drugindication` - Reason for taking the drug
- `patient.reaction.reactionmeddrapt` - Adverse reaction description
- `receivedate` - Date report was received
- `serious` - Whether the event was serious (1 = serious, 2 = not serious)
- `seriousnessdeath` - Whether the event resulted in death
- `primarysource.qualification` - Reporter qualification (physician, pharmacist, etc.)

**Common Use Cases**:
- Safety signal detection
- Post-market surveillance
- Drug interaction analysis
- Comparative safety research

**Example Queries**:
```python
# Find adverse events for a specific drug
import requests

api_key = "YOUR_API_KEY"
url = "https://api.fda.gov/drug/event.json"

# Search for aspirin-related adverse events
params = {
    "api_key": api_key,
    "search": "patient.drug.medicinalproduct:aspirin",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
```

```python
# Count most common reactions for a drug
params = {
    "api_key": api_key,
    "search": "patient.drug.medicinalproduct:metformin",
    "count": "patient.reaction.reactionmeddrapt.exact"
}
```

### 2. Drug Product Labeling

**Endpoint**: `https://api.fda.gov/drug/label.json`

**Purpose**: Access structured product information including prescribing information, warnings, indications, and usage for FDA-approved and marketed drug products.

**Data Source**: Structured Product Labeling (SPL)

**Key Fields**:
- `openfda.brand_name` - Brand name(s) of the drug
- `openfda.generic_name` - Generic name(s)
- `indications_and_usage` - Approved uses
- `warnings` - Important safety warnings
- `adverse_reactions` - Known adverse reactions
- `dosage_and_administration` - How to use the drug
- `description` - Chemical and physical description
- `pharmacodynamics` - How the drug works
- `contraindications` - When not to use the drug
- `drug_interactions` - Known drug interactions
- `active_ingredient` - Active ingredients
- `inactive_ingredient` - Inactive ingredients

**Common Use Cases**:
- Clinical decision support
- Drug information lookup
- Patient education materials
- Formulary management
- Drug comparison analysis

**Example Queries**:
```python
# Get full labeling for a brand-name drug
params = {
    "api_key": api_key,
    "search": "openfda.brand_name:Lipitor",
    "limit": 1
}

response = requests.get("https://api.fda.gov/drug/label.json", params=params)
label_data = response.json()

# Extract specific sections
if "results" in label_data:
    label = label_data["results"][0]
    indications = label.get("indications_and_usage", ["Not available"])[0]
    warnings = label.get("warnings", ["Not available"])[0]
```

```python
# Search labels containing specific warnings
params = {
    "api_key": api_key,
    "search": "warnings:*hypertension*",
    "limit": 10
}
```

### 3. National Drug Code (NDC) Directory

**Endpoint**: `https://api.fda.gov/drug/ndc.json`

**Purpose**: Access the NDC Directory containing information about drug products identified by National Drug Codes.

**Data Source**: FDA NDC Directory

**Key Fields**:
- `product_ndc` - 10-digit NDC product identifier
- `generic_name` - Generic drug name
- `labeler_name` - Company that manufactures/distributes
- `brand_name` - Brand name if applicable
- `dosage_form` - Form (tablet, capsule, solution, etc.)
- `route` - Administration route (oral, injection, topical, etc.)
- `product_type` - Type of drug product
- `marketing_category` - Regulatory pathway (NDA, ANDA, OTC, etc.)
- `application_number` - FDA application number
- `active_ingredients` - List of active ingredients with strengths
- `packaging` - Package descriptions and NDC codes
- `listing_expiration_date` - When listing expires

**Common Use Cases**:
- NDC lookup and validation
- Product identification
- Supply chain management
- Prescription processing
- Insurance claims processing

**Example Queries**:
```python
# Look up drug by NDC code
params = {
    "api_key": api_key,
    "search": "product_ndc:0069-2110",
    "limit": 1
}

response = requests.get("https://api.fda.gov/drug/ndc.json", params=params)
```

```python
# Find all products from a specific manufacturer
params = {
    "api_key": api_key,
    "search": "labeler_name:Pfizer",
    "limit": 100
}
```

```python
# Get all oral tablets of a generic drug
params = {
    "api_key": api_key,
    "search": "generic_name:lisinopril+AND+dosage_form:TABLET",
    "limit": 50
}
```

### 4. Drug Recall Enforcement Reports

**Endpoint**: `https://api.fda.gov/drug/enforcement.json`

**Purpose**: Access drug product recall enforcement reports issued by the FDA.

**Data Source**: FDA Enforcement Reports

**Key Fields**:
- `status` - Current status (Ongoing, Completed, Terminated)
- `recall_number` - Unique recall identifier
- `classification` - Class I, II, or III (severity)
- `product_description` - Description of recalled product
- `reason_for_recall` - Why product was recalled
- `product_quantity` - Amount of product recalled
- `code_info` - Lot numbers, serial numbers, NDCs
- `distribution_pattern` - Geographic distribution
- `recalling_firm` - Company conducting recall
- `recall_initiation_date` - When recall began
- `report_date` - When FDA received notice
- `voluntary_mandated` - Type of recall

**Classification Levels**:
- **Class I**: Dangerous or defective products that could cause serious health problems or death
- **Class II**: Products that might cause temporary health problems or pose slight threat of serious nature
- **Class III**: Products unlikely to cause adverse health reaction but violate FDA labeling/manufacturing regulations

**Common Use Cases**:
- Quality assurance monitoring
- Supply chain risk management
- Patient safety alerts
- Regulatory compliance tracking

**Example Queries**:
```python
# Find all Class I (most serious) drug recalls
params = {
    "api_key": api_key,
    "search": "classification:Class+I",
    "limit": 20,
    "sort": "report_date:desc"
}

response = requests.get("https://api.fda.gov/drug/enforcement.json", params=params)
```

```python
# Search for recalls of a specific drug
params = {
    "api_key": api_key,
    "search": "product_description:*metformin*",
    "limit": 10
}
```

```python
# Find ongoing recalls
params = {
    "api_key": api_key,
    "search": "status:Ongoing",
    "limit": 50
}
```

### 5. Drugs@FDA

**Endpoint**: `https://api.fda.gov/drug/drugsfda.json`

**Purpose**: Access comprehensive information about FDA-approved drug products from Drugs@FDA database, including approval history and regulatory information.

**Data Source**: Drugs@FDA Database (most drugs approved since 1939)

**Key Fields**:
- `application_number` - NDA/ANDA/BLA number
- `sponsor_name` - Company that submitted application
- `openfda.brand_name` - Brand name(s)
- `openfda.generic_name` - Generic name(s)
- `products` - Array of approved products under this application
- `products.active_ingredients` - Active ingredients with strengths
- `products.dosage_form` - Dosage form
- `products.route` - Route of administration
- `products.marketing_status` - Current marketing status
- `submissions` - Array of regulatory submissions
- `submissions.submission_type` - Type of submission
- `submissions.submission_status` - Status (approved, pending, etc.)
- `submissions.submission_status_date` - Status date
- `submissions.review_priority` - Priority or standard review

**Common Use Cases**:
- Drug approval research
- Regulatory pathway analysis
- Historical approval tracking
- Competitive intelligence
- Market access research

**Example Queries**:
```python
# Find approval information for a specific drug
params = {
    "api_key": api_key,
    "search": "openfda.brand_name:Keytruda",
    "limit": 1
}

response = requests.get("https://api.fda.gov/drug/drugsfda.json", params=params)
```

```python
# Get all drugs approved by a specific sponsor
params = {
    "api_key": api_key,
    "search": "sponsor_name:Moderna",
    "limit": 100
}
```

```python
# Find drugs with priority review designation
params = {
    "api_key": api_key,
    "search": "submissions.review_priority:Priority",
    "limit": 50
}
```

### 6. Drug Shortages

**Endpoint**: `https://api.fda.gov/drug/drugshortages.json`

**Purpose**: Access information about current and resolved drug shortages affecting the United States.

**Data Source**: FDA Drug Shortages Database

**Key Fields**:
- `product_name` - Name of drug in shortage
- `status` - Current status (Currently in Shortage, Resolved, Discontinued)
- `reason` - Reason for shortage
- `shortage_start_date` - When shortage began
- `resolution_date` - When shortage was resolved (if applicable)
- `discontinuation_date` - If product was discontinued
- `active_ingredient` - Active ingredients
- `marketed_by` - Companies marketing the product
- `presentation` - Dosage form and strength

**Common Use Cases**:
- Formulary management
- Supply chain planning
- Patient care continuity
- Therapeutic alternative identification
- Procurement planning

**Example Queries**:
```python
# Find current drug shortages
params = {
    "api_key": api_key,
    "search": "status:Currently+in+Shortage",
    "limit": 100
}

response = requests.get("https://api.fda.gov/drug/drugshortages.json", params=params)
```

```python
# Search for shortages of a specific drug
params = {
    "api_key": api_key,
    "search": "product_name:*amoxicillin*",
    "limit": 10
}
```

```python
# Get shortage history (both current and resolved)
params = {
    "api_key": api_key,
    "search": "active_ingredient:epinephrine",
    "limit": 50
}
```

## Integration Tips

### Error Handling

```python
import requests
import time

def query_fda_drug(endpoint, params, max_retries=3):
    """
    Query FDA drug database with error handling and retry logic.

    Args:
        endpoint: Full URL endpoint (e.g., "https://api.fda.gov/drug/event.json")
        params: Dictionary of query parameters
        max_retries: Maximum number of retry attempts

    Returns:
        Response JSON data or None if error
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"No results found for query")
                return None
            elif response.status_code == 429:
                # Rate limit exceeded, wait and retry
                wait_time = 60 * (attempt + 1)
                print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None
    return None
```

### Pagination for Large Result Sets

```python
def get_all_results(endpoint, search_query, api_key, max_results=1000):
    """
    Retrieve all results for a query using pagination.

    Args:
        endpoint: API endpoint URL
        search_query: Search query string
        api_key: FDA API key
        max_results: Maximum total results to retrieve

    Returns:
        List of all result records
    """
    all_results = []
    skip = 0
    limit = 100  # Max per request

    while len(all_results) < max_results:
        params = {
            "api_key": api_key,
            "search": search_query,
            "limit": limit,
            "skip": skip
        }

        data = query_fda_drug(endpoint, params)
        if not data or "results" not in data:
            break

        results = data["results"]
        all_results.extend(results)

        # Check if we've retrieved all available results
        if len(results) < limit:
            break

        skip += limit
        time.sleep(0.25)  # Rate limiting courtesy

    return all_results[:max_results]
```

## Best Practices

1. **Always use HTTPS** - HTTP requests are not accepted
2. **Include API key** - Provides higher rate limits (120,000/day vs 1,000/day)
3. **Use exact matching for aggregations** - Add `.exact` suffix to field names in count queries
4. **Implement rate limiting** - Stay within 240 requests/minute
5. **Cache results** - Avoid redundant queries for the same data
6. **Handle errors gracefully** - Implement retry logic for transient failures
7. **Use specific field searches** - More efficient than full-text searches
8. **Validate NDC codes** - Use standard 11-digit format with hyphens removed
9. **Monitor API status** - Check openFDA status page for outages
10. **Respect data limitations** - OpenFDA contains public data only, not all FDA data

## Additional Resources

- OpenFDA Drug API Documentation: https://open.fda.gov/apis/drug/
- API Basics: See `api_basics.md` in this references directory
- Python examples: See `scripts/fda_drug_query.py`
- Field reference guides: Available at https://open.fda.gov/apis/drug/[endpoint]/searchable-fields/

---

## Reference: Foods

# FDA Food Databases

This reference covers FDA food-related API endpoints accessible through openFDA.

## Overview

The FDA food databases provide access to information about food products, including adverse events and enforcement actions. These databases help track food safety issues, recalls, and consumer complaints.

## Available Endpoints

### 1. Food Adverse Events

**Endpoint**: `https://api.fda.gov/food/event.json`

**Purpose**: Access adverse event reports for food products, dietary supplements, and cosmetics.

**Data Source**: CAERS (CFSAN Adverse Event Reporting System)

**Key Fields**:
- `date_started` - When adverse event began
- `date_created` - When report was created
- `report_number` - Unique report identifier
- `outcomes` - Event outcomes (e.g., hospitalization, death)
- `reactions` - Adverse reactions/symptoms reported
- `consumer.age` - Consumer age
- `consumer.age_unit` - Age unit (years, months, etc.)
- `consumer.gender` - Consumer gender
- `products` - Array of products involved
- `products.name_brand` - Product brand name
- `products.industry_code` - Product category code
- `products.industry_name` - Product category name
- `products.role` - Product role (Suspect, Concomitant)

**Product Categories (industry_name)**:
- Bakery Products/Dough/Mixes/Icing
- Beverages (coffee, tea, soft drinks, etc.)
- Dietary Supplements
- Ice Cream Products
- Cosmetics
- Vitamins and nutritional supplements
- Many others

**Common Use Cases**:
- Food safety surveillance
- Dietary supplement monitoring
- Adverse event trend analysis
- Product safety assessment
- Consumer complaint tracking

**Example Queries**:
```python
import requests

api_key = "YOUR_API_KEY"
url = "https://api.fda.gov/food/event.json"

# Find adverse events for dietary supplements
params = {
    "api_key": api_key,
    "search": "products.industry_name:Dietary+Supplements",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
```

```python
# Count most common reactions
params = {
    "api_key": api_key,
    "search": "products.industry_name:*Beverages*",
    "count": "reactions.exact"
}
```

```python
# Find serious outcomes (hospitalizations, deaths)
params = {
    "api_key": api_key,
    "search": "outcomes:Hospitalization",
    "limit": 50,
    "sort": "date_created:desc"
}
```

```python
# Search by product brand name
params = {
    "api_key": api_key,
    "search": "products.name_brand:*protein+powder*",
    "limit": 20
}
```

### 2. Food Enforcement Reports

**Endpoint**: `https://api.fda.gov/food/enforcement.json`

**Purpose**: Access food product recall enforcement reports issued by the FDA.

**Data Source**: FDA Enforcement Reports

**Key Fields**:
- `status` - Current status (Ongoing, Completed, Terminated)
- `recall_number` - Unique recall identifier
- `classification` - Class I, II, or III
- `product_description` - Description of recalled food product
- `reason_for_recall` - Why product was recalled
- `product_quantity` - Amount of product recalled
- `code_info` - Lot numbers, batch codes, UPCs
- `distribution_pattern` - Geographic distribution
- `recalling_firm` - Company conducting recall
- `recall_initiation_date` - When recall began
- `report_date` - When FDA received notice
- `voluntary_mandated` - Voluntary or FDA-mandated recall
- `city` - Recalling firm city
- `state` - Recalling firm state
- `country` - Recalling firm country
- `initial_firm_notification` - How firm was notified

**Classification Levels**:
- **Class I**: Dangerous or defective products that could cause serious health problems or death (e.g., undeclared allergens with severe risk, botulism contamination)
- **Class II**: Products that might cause temporary health problems or pose slight threat (e.g., minor allergen issues, quality defects)
- **Class III**: Products unlikely to cause adverse health reactions but violate FDA regulations (e.g., labeling errors, quality issues)

**Common Recall Reasons**:
- Undeclared allergens (milk, eggs, peanuts, tree nuts, soy, wheat, fish, shellfish, sesame)
- Microbial contamination (Listeria, Salmonella, E. coli, etc.)
- Foreign material contamination (metal, plastic, glass)
- Labeling errors
- Improper processing/packaging
- Chemical contamination

**Common Use Cases**:
- Food safety monitoring
- Supply chain risk management
- Allergen tracking
- Retailer recall coordination
- Consumer safety alerts

**Example Queries**:
```python
# Find all Class I food recalls (most serious)
params = {
    "api_key": api_key,
    "search": "classification:Class+I",
    "limit": 20,
    "sort": "report_date:desc"
}

response = requests.get("https://api.fda.gov/food/enforcement.json", params=params)
```

```python
# Search for allergen-related recalls
params = {
    "api_key": api_key,
    "search": "reason_for_recall:*undeclared+allergen*",
    "limit": 50
}
```

```python
# Find Listeria contamination recalls
params = {
    "api_key": api_key,
    "search": "reason_for_recall:*listeria*",
    "limit": 30,
    "sort": "recall_initiation_date:desc"
}
```

```python
# Get recalls by specific company
params = {
    "api_key": api_key,
    "search": "recalling_firm:*General+Mills*",
    "limit": 20
}
```

```python
# Find ongoing recalls
params = {
    "api_key": api_key,
    "search": "status:Ongoing",
    "limit": 100
}
```

```python
# Search by product type
params = {
    "api_key": api_key,
    "search": "product_description:*ice+cream*",
    "limit": 25
}
```

## Integration Tips

### Allergen Monitoring System

```python
def monitor_allergen_recalls(allergens, api_key, days_back=30):
    """
    Monitor food recalls for specific allergens.

    Args:
        allergens: List of allergens to monitor (e.g., ["peanut", "milk", "soy"])
        api_key: FDA API key
        days_back: Number of days to look back

    Returns:
        List of matching recalls
    """
    import requests
    from datetime import datetime, timedelta

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    date_range = f"[{start_date.strftime('%Y%m%d')}+TO+{end_date.strftime('%Y%m%d')}]"

    url = "https://api.fda.gov/food/enforcement.json"
    all_recalls = []

    for allergen in allergens:
        params = {
            "api_key": api_key,
            "search": f"reason_for_recall:*{allergen}*+AND+report_date:{date_range}",
            "limit": 100
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                for result in data["results"]:
                    result["detected_allergen"] = allergen
                    all_recalls.append(result)

    return all_recalls
```

### Adverse Event Analysis

```python
def analyze_product_adverse_events(product_name, api_key):
    """
    Analyze adverse events for a specific food product.

    Args:
        product_name: Product name or partial name
        api_key: FDA API key

    Returns:
        Dictionary with analysis results
    """
    import requests
    from collections import Counter

    url = "https://api.fda.gov/food/event.json"
    params = {
        "api_key": api_key,
        "search": f"products.name_brand:*{product_name}*",
        "limit": 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return {"error": "No results found"}

    results = data["results"]

    # Extract all reactions
    all_reactions = []
    all_outcomes = []

    for event in results:
        if "reactions" in event:
            all_reactions.extend(event["reactions"])
        if "outcomes" in event:
            all_outcomes.extend(event["outcomes"])

    # Count frequencies
    reaction_counts = Counter(all_reactions)
    outcome_counts = Counter(all_outcomes)

    return {
        "total_events": len(results),
        "most_common_reactions": reaction_counts.most_common(10),
        "outcome_distribution": dict(outcome_counts),
        "serious_outcomes": sum(1 for o in all_outcomes if o in ["Hospitalization", "Death", "Disability"])
    }
```

### Recall Alert System

```python
def get_recent_recalls_by_state(state_code, api_key, days=7):
    """
    Get recent food recalls for products distributed in a specific state.

    Args:
        state_code: Two-letter state code (e.g., "CA", "NY")
        api_key: FDA API key
        days: Number of days to look back

    Returns:
        List of recent recalls affecting the state
    """
    import requests
    from datetime import datetime, timedelta

    url = "https://api.fda.gov/food/enforcement.json"

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = f"[{start_date.strftime('%Y%m%d')}+TO+{end_date.strftime('%Y%m%d')}]"

    params = {
        "api_key": api_key,
        "search": f"distribution_pattern:*{state_code}*+AND+report_date:{date_range}",
        "limit": 100,
        "sort": "report_date:desc"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    return []
```

## Best Practices

1. **Monitor allergen recalls** - Critical for food service and retail
2. **Check distribution patterns** - Recalls may be regional or national
3. **Track recall status** - Status changes from "Ongoing" to "Completed"
4. **Filter by classification** - Prioritize Class I recalls for immediate action
5. **Use date ranges** - Focus on recent events for operational relevance
6. **Cross-reference products** - Same product may appear in both adverse events and enforcement
7. **Parse code_info carefully** - Lot numbers and UPCs vary in format
8. **Consider product categories** - Industry codes help categorize products
9. **Track serious outcomes** - Hospitalization and death require immediate attention
10. **Implement alert systems** - Automate monitoring for critical products/allergens

## Common Allergens to Monitor

The FDA recognizes 9 major food allergens that must be declared:
1. Milk
2. Eggs
3. Fish
4. Crustacean shellfish
5. Tree nuts
6. Peanuts
7. Wheat
8. Soybeans
9. Sesame

These account for over 90% of food allergies and are the most common reasons for Class I recalls.

## Additional Resources

- OpenFDA Food API Documentation: https://open.fda.gov/apis/food/
- CFSAN Adverse Event Reporting: https://www.fda.gov/food/compliance-enforcement-food/cfsan-adverse-event-reporting-system-caers
- Food Recalls: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts
- API Basics: See `api_basics.md` in this references directory
- Python examples: See `scripts/fda_food_query.py`

---

## Reference: Other

# FDA Other Databases - Substances and NSDE

This reference covers FDA substance-related and other specialized API endpoints accessible through openFDA.

## Overview

The FDA maintains additional databases for substance-level information that is precise to the molecular level. These databases support regulatory activities across drugs, biologics, devices, foods, and cosmetics.

## Available Endpoints

### 1. Substance Data

**Endpoint**: `https://api.fda.gov/other/substance.json`

**Purpose**: Access substance information that is precise to the molecular level for internal and external use. This includes information about active pharmaceutical ingredients, excipients, and other substances used in FDA-regulated products.

**Data Source**: FDA Global Substance Registration System (GSRS)

**Key Fields**:
- `uuid` - Unique substance identifier (UUID)
- `approvalID` - FDA Unique Ingredient Identifier (UNII)
- `approved` - Approval date
- `substanceClass` - Type of substance (chemical, protein, nucleic acid, polymer, etc.)
- `names` - Array of substance names
- `names.name` - Name text
- `names.type` - Name type (systematic, brand, common, etc.)
- `names.preferred` - Whether preferred name
- `codes` - Array of substance codes
- `codes.code` - Code value
- `codes.codeSystem` - Code system (CAS, ECHA, EINECS, etc.)
- `codes.type` - Code type
- `relationships` - Array of substance relationships
- `relationships.type` - Relationship type (ACTIVE MOIETY, METABOLITE, IMPURITY, etc.)
- `relationships.relatedSubstance` - Related substance reference
- `moieties` - Molecular moieties
- `properties` - Array of physicochemical properties
- `properties.name` - Property name
- `properties.value` - Property value
- `properties.propertyType` - Property type
- `structure` - Chemical structure information
- `structure.smiles` - SMILES notation
- `structure.inchi` - InChI string
- `structure.inchiKey` - InChI key
- `structure.formula` - Molecular formula
- `structure.molecularWeight` - Molecular weight
- `modifications` - Structural modifications (for proteins, etc.)
- `protein` - Protein-specific information
- `protein.subunits` - Protein subunits
- `protein.sequenceType` - Sequence type
- `nucleicAcid` - Nucleic acid information
- `nucleicAcid.subunits` - Sequence subunits
- `polymer` - Polymer information
- `mixture` - Mixture components
- `mixture.components` - Component substances
- `tags` - Substance tags
- `references` - Literature references

**Substance Classes**:
- **Chemical** - Small molecules with defined chemical structure
- **Protein** - Proteins and peptides
- **Nucleic Acid** - DNA, RNA, oligonucleotides
- **Polymer** - Polymeric substances
- **Structurally Diverse** - Complex mixtures, botanicals
- **Mixture** - Defined mixtures
- **Concept** - Abstract concepts (e.g., groups)

**Common Use Cases**:
- Active ingredient identification
- Molecular structure lookup
- UNII code resolution
- Chemical identifier mapping (CAS to UNII, etc.)
- Substance relationship analysis
- Excipient identification
- Botanical substance information
- Protein and biologic characterization

**Example Queries**:
```python
import requests

api_key = "YOUR_API_KEY"
url = "https://api.fda.gov/other/substance.json"

# Look up substance by UNII code
params = {
    "api_key": api_key,
    "search": "approvalID:R16CO5Y76E",  # Aspirin UNII
    "limit": 1
}

response = requests.get(url, params=params)
data = response.json()
```

```python
# Search by substance name
params = {
    "api_key": api_key,
    "search": "names.name:acetaminophen",
    "limit": 5
}
```

```python
# Find substances by CAS number
params = {
    "api_key": api_key,
    "search": "codes.code:50-78-2",  # Aspirin CAS
    "limit": 1
}
```

```python
# Get chemical substances only
params = {
    "api_key": api_key,
    "search": "substanceClass:chemical",
    "limit": 100
}
```

```python
# Search by molecular formula
params = {
    "api_key": api_key,
    "search": "structure.formula:C8H9NO2",  # Acetaminophen
    "limit": 10
}
```

```python
# Find protein substances
params = {
    "api_key": api_key,
    "search": "substanceClass:protein",
    "limit": 50
}
```

### 2. NSDE (National Substance Database Entry)

**Endpoint**: `https://api.fda.gov/other/nsde.json`

**Purpose**: Access historical substance data from legacy National Drug Code (NDC) directory entries. This endpoint provides substance information as it appears in historical drug product listings.

**Note**: This database is primarily for historical reference. For current substance information, use the Substance Data endpoint.

**Key Fields**:
- `proprietary_name` - Product proprietary name
- `nonproprietary_name` - Nonproprietary name
- `dosage_form` - Dosage form
- `route` - Route of administration
- `company_name` - Company name
- `substance_name` - Substance name
- `active_numerator_strength` - Active ingredient strength (numerator)
- `active_ingred_unit` - Active ingredient unit
- `pharm_classes` - Pharmacological classes
- `dea_schedule` - DEA controlled substance schedule

**Common Use Cases**:
- Historical drug formulation research
- Legacy system integration
- Historical substance name mapping
- Pharmaceutical history research

**Example Queries**:
```python
# Search by substance name
params = {
    "api_key": api_key,
    "search": "substance_name:ibuprofen",
    "limit": 20
}

response = requests.get("https://api.fda.gov/other/nsde.json", params=params)
```

```python
# Find controlled substances by DEA schedule
params = {
    "api_key": api_key,
    "search": "dea_schedule:CII",
    "limit": 50
}
```

## Integration Tips

### UNII to CAS Mapping

```python
def get_substance_identifiers(unii, api_key):
    """
    Get all identifiers for a substance given its UNII code.

    Args:
        unii: FDA Unique Ingredient Identifier
        api_key: FDA API key

    Returns:
        Dictionary with substance identifiers
    """
    import requests

    url = "https://api.fda.gov/other/substance.json"
    params = {
        "api_key": api_key,
        "search": f"approvalID:{unii}",
        "limit": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    substance = data["results"][0]

    identifiers = {
        "unii": substance.get("approvalID"),
        "uuid": substance.get("uuid"),
        "preferred_name": None,
        "cas_numbers": [],
        "other_codes": {}
    }

    # Extract names
    if "names" in substance:
        for name in substance["names"]:
            if name.get("preferred"):
                identifiers["preferred_name"] = name.get("name")
                break
        if not identifiers["preferred_name"] and len(substance["names"]) > 0:
            identifiers["preferred_name"] = substance["names"][0].get("name")

    # Extract codes
    if "codes" in substance:
        for code in substance["codes"]:
            code_system = code.get("codeSystem", "").upper()
            code_value = code.get("code")

            if "CAS" in code_system:
                identifiers["cas_numbers"].append(code_value)
            else:
                if code_system not in identifiers["other_codes"]:
                    identifiers["other_codes"][code_system] = []
                identifiers["other_codes"][code_system].append(code_value)

    return identifiers
```

### Chemical Structure Lookup

```python
def get_chemical_structure(substance_name, api_key):
    """
    Get chemical structure information for a substance.

    Args:
        substance_name: Name of the substance
        api_key: FDA API key

    Returns:
        Dictionary with structure information
    """
    import requests

    url = "https://api.fda.gov/other/substance.json"
    params = {
        "api_key": api_key,
        "search": f"names.name:{substance_name}",
        "limit": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    substance = data["results"][0]

    if "structure" not in substance:
        return None

    structure = substance["structure"]

    return {
        "smiles": structure.get("smiles"),
        "inchi": structure.get("inchi"),
        "inchi_key": structure.get("inchiKey"),
        "formula": structure.get("formula"),
        "molecular_weight": structure.get("molecularWeight"),
        "substance_class": substance.get("substanceClass")
    }
```

### Substance Relationship Mapping

```python
def get_substance_relationships(unii, api_key):
    """
    Get all related substances (metabolites, active moieties, etc.).

    Args:
        unii: FDA Unique Ingredient Identifier
        api_key: FDA API key

    Returns:
        Dictionary organizing relationships by type
    """
    import requests

    url = "https://api.fda.gov/other/substance.json"
    params = {
        "api_key": api_key,
        "search": f"approvalID:{unii}",
        "limit": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    substance = data["results"][0]

    relationships = {}

    if "relationships" in substance:
        for rel in substance["relationships"]:
            rel_type = rel.get("type")
            if rel_type not in relationships:
                relationships[rel_type] = []

            related = {
                "uuid": rel.get("relatedSubstance", {}).get("uuid"),
                "unii": rel.get("relatedSubstance", {}).get("approvalID"),
                "name": rel.get("relatedSubstance", {}).get("refPname")
            }
            relationships[rel_type].append(related)

    return relationships
```

### Active Ingredient Extraction

```python
def find_active_ingredients_by_product(product_name, api_key):
    """
    Find active ingredients in a drug product.

    Args:
        product_name: Drug product name
        api_key: FDA API key

    Returns:
        List of active ingredient UNIIs and names
    """
    import requests

    # First search drug label database
    label_url = "https://api.fda.gov/drug/label.json"
    label_params = {
        "api_key": api_key,
        "search": f"openfda.brand_name:{product_name}",
        "limit": 1
    }

    response = requests.get(label_url, params=label_params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    label = data["results"][0]

    # Extract UNIIs from openfda section
    active_ingredients = []

    if "openfda" in label:
        openfda = label["openfda"]

        # Get UNIIs
        unii_list = openfda.get("unii", [])
        generic_names = openfda.get("generic_name", [])

        for i, unii in enumerate(unii_list):
            ingredient = {"unii": unii}
            if i < len(generic_names):
                ingredient["name"] = generic_names[i]

            # Get additional substance info
            substance_info = get_substance_identifiers(unii, api_key)
            if substance_info:
                ingredient.update(substance_info)

            active_ingredients.append(ingredient)

    return active_ingredients
```

## Best Practices

1. **Use UNII as primary identifier** - Most consistent across FDA databases
2. **Map between identifier systems** - CAS, UNII, InChI Key for cross-referencing
3. **Handle substance variations** - Different salt forms, hydrates have different UNIIs
4. **Check substance class** - Different classes have different data structures
5. **Validate chemical structures** - SMILES and InChI should be verified
6. **Consider substance relationships** - Active moiety vs. salt form matters
7. **Use preferred names** - More consistent than trade names
8. **Cache substance data** - Substance information changes infrequently
9. **Cross-reference with other endpoints** - Link substances to drugs/products
10. **Handle mixture components** - Complex products have multiple components

## UNII System

The FDA Unique Ingredient Identifier (UNII) system provides:
- **Unique identifiers** - Each substance gets one UNII
- **Substance specificity** - Different forms (salts, hydrates) get different UNIIs
- **Global recognition** - Used internationally
- **Stability** - UNIIs don't change once assigned
- **Free access** - No licensing required

**UNII Format**: 10-character alphanumeric code (e.g., `R16CO5Y76E`)

## Substance Classes Explained

### Chemical
- Traditional small molecule drugs
- Have defined molecular structure
- Include organic and inorganic compounds
- SMILES, InChI, molecular formula available

### Protein
- Polypeptides and proteins
- Sequence information available
- May have post-translational modifications
- Includes antibodies, enzymes, hormones

### Nucleic Acid
- DNA and RNA sequences
- Oligonucleotides
- Antisense, siRNA, mRNA
- Sequence data available

### Polymer
- Synthetic and natural polymers
- Structural repeat units
- Molecular weight distributions
- Used as excipients and active ingredients

### Structurally Diverse
- Complex natural products
- Botanical extracts
- Materials without single molecular structure
- Characterized by source and composition

### Mixture
- Defined combinations of substances
- Fixed or variable composition
- Each component trackable

## Additional Resources

- FDA Substance Registration System: https://fdasis.nlm.nih.gov/srs/
- UNII Search: https://precision.fda.gov/uniisearch
- OpenFDA Other APIs: https://open.fda.gov/apis/other/
- API Basics: See `api_basics.md` in this references directory
- Python examples: See `scripts/fda_substance_query.py`
