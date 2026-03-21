---
title: "Openalex Database"
description: "Query and analyze scholarly literature using the OpenAlex database. This skill should be used when searching for academic papers, analyzing research trends, finding works by authors or institutions, tracking citations, discovering open access publ..."
category: "research"
source: "community"
author: "Community"
tags: ["openalex", "database"]
date: 2026-03-20
---

# OpenAlex Database

## Overview

OpenAlex is a comprehensive open catalog of 240M+ scholarly works, authors, institutions, topics, sources, publishers, and funders. This skill provides tools and workflows for querying the OpenAlex API to search literature, analyze research output, track citations, and conduct bibliometric studies.

## Quick Start

### Basic Setup

Always initialize the client with an email address to access the polite pool (10x rate limit boost):

```python
from scripts.openalex_client import OpenAlexClient

client = OpenAlexClient(email="your-email@example.edu")
```

### Installation Requirements

Install required package using uv:

```bash
uv pip install requests
```

No API key required - OpenAlex is completely open.

## Core Capabilities

### 1. Search for Papers

**Use for**: Finding papers by title, abstract, or topic

```python
# Simple search
results = client.search_works(
    search="machine learning",
    per_page=100
)

# Search with filters
results = client.search_works(
    search="CRISPR gene editing",
    filter_params={
        "publication_year": ">2020",
        "is_oa": "true"
    },
    sort="cited_by_count:desc"
)
```

### 2. Find Works by Author

**Use for**: Getting all publications by a specific researcher

Use the two-step pattern (entity name → ID → works):

```python
from scripts.query_helpers import find_author_works

works = find_author_works(
    author_name="Jennifer Doudna",
    client=client,
    limit=100
)
```

**Manual two-step approach**:
```python
# Step 1: Get author ID
author_response = client._make_request(
    '/authors',
    params={'search': 'Jennifer Doudna', 'per-page': 1}
)
author_id = author_response['results'][0]['id'].split('/')[-1]

# Step 2: Get works
works = client.search_works(
    filter_params={"authorships.author.id": author_id}
)
```

### 3. Find Works from Institution

**Use for**: Analyzing research output from universities or organizations

```python
from scripts.query_helpers import find_institution_works

works = find_institution_works(
    institution_name="Stanford University",
    client=client,
    limit=200
)
```

### 4. Highly Cited Papers

**Use for**: Finding influential papers in a field

```python
from scripts.query_helpers import find_highly_cited_recent_papers

papers = find_highly_cited_recent_papers(
    topic="quantum computing",
    years=">2020",
    client=client,
    limit=100
)
```

### 5. Open Access Papers

**Use for**: Finding freely available research

```python
from scripts.query_helpers import get_open_access_papers

papers = get_open_access_papers(
    search_term="climate change",
    client=client,
    oa_status="any",  # or "gold", "green", "hybrid", "bronze"
    limit=200
)
```

### 6. Publication Trends Analysis

**Use for**: Tracking research output over time

```python
from scripts.query_helpers import get_publication_trends

trends = get_publication_trends(
    search_term="artificial intelligence",
    filter_params={"is_oa": "true"},
    client=client
)

# Sort and display
for trend in sorted(trends, key=lambda x: x['key'])[-10:]:
    print(f"{trend['key']}: {trend['count']} publications")
```

### 7. Research Output Analysis

**Use for**: Comprehensive analysis of author or institution research

```python
from scripts.query_helpers import analyze_research_output

analysis = analyze_research_output(
    entity_type='institution',  # or 'author'
    entity_name='MIT',
    client=client,
    years='>2020'
)

print(f"Total works: {analysis['total_works']}")
print(f"Open access: {analysis['open_access_percentage']}%")
print(f"Top topics: {analysis['top_topics'][:5]}")
```

### 8. Batch Lookups

**Use for**: Getting information for multiple DOIs, ORCIDs, or IDs efficiently

```python
dois = [
    "https://doi.org/10.1038/s41586-021-03819-2",
    "https://doi.org/10.1126/science.abc1234",
    # ... up to 50 DOIs
]

works = client.batch_lookup(
    entity_type='works',
    ids=dois,
    id_field='doi'
)
```

### 9. Random Sampling

**Use for**: Getting representative samples for analysis

```python
# Small sample
works = client.sample_works(
    sample_size=100,
    seed=42,  # For reproducibility
    filter_params={"publication_year": "2023"}
)

# Large sample (>10k) - automatically handles multiple requests
works = client.sample_works(
    sample_size=25000,
    seed=42,
    filter_params={"is_oa": "true"}
)
```

### 10. Citation Analysis

**Use for**: Finding papers that cite a specific work

```python
# Get the work
work = client.get_entity('works', 'https://doi.org/10.1038/s41586-021-03819-2')

# Get citing papers using cited_by_api_url
import requests
citing_response = requests.get(
    work['cited_by_api_url'],
    params={'mailto': client.email, 'per-page': 200}
)
citing_works = citing_response.json()['results']
```

### 11. Topic and Subject Analysis

**Use for**: Understanding research focus areas

```python
# Get top topics for an institution
topics = client.group_by(
    entity_type='works',
    group_field='topics.id',
    filter_params={
        "authorships.institutions.id": "I136199984",  # MIT
        "publication_year": ">2020"
    }
)

for topic in topics[:10]:
    print(f"{topic['key_display_name']}: {topic['count']} works")
```

### 12. Large-Scale Data Extraction

**Use for**: Downloading large datasets for analysis

```python
# Paginate through all results
all_papers = client.paginate_all(
    endpoint='/works',
    params={
        'search': 'synthetic biology',
        'filter': 'publication_year:2020-2024'
    },
    max_results=10000
)

# Export to CSV
import csv
with open('papers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Citations', 'DOI', 'OA Status'])

    for paper in all_papers:
        writer.writerow([
            paper.get('title', 'N/A'),
            paper.get('publication_year', 'N/A'),
            paper.get('cited_by_count', 0),
            paper.get('doi', 'N/A'),
            paper.get('open_access', {}).get('oa_status', 'closed')
        ])
```

## Critical Best Practices

### Always Use Email for Polite Pool
Add email to get 10x rate limit (1 req/sec → 10 req/sec):
```python
client = OpenAlexClient(email="your-email@example.edu")
```

### Use Two-Step Pattern for Entity Lookups
Never filter by entity names directly - always get ID first:
```python
# ✅ Correct
# 1. Search for entity → get ID
# 2. Filter by ID

# ❌ Wrong
# filter=author_name:Einstein  # This doesn't work!
```

### Use Maximum Page Size
Always use `per-page=200` for efficient data retrieval:
```python
results = client.search_works(search="topic", per_page=200)
```

### Batch Multiple IDs
Use batch_lookup() for multiple IDs instead of individual requests:
```python
# ✅ Correct - 1 request for 50 DOIs
works = client.batch_lookup('works', doi_list, 'doi')

# ❌ Wrong - 50 separate requests
for doi in doi_list:
    work = client.get_entity('works', doi)
```

### Use Sample Parameter for Random Data
Use `sample_works()` with seed for reproducible random sampling:
```python
# ✅ Correct
works = client.sample_works(sample_size=100, seed=42)

# ❌ Wrong - random page numbers bias results
# Using random page numbers doesn't give true random sample
```

### Select Only Needed Fields
Reduce response size by selecting specific fields:
```python
results = client.search_works(
    search="topic",
    select=['id', 'title', 'publication_year', 'cited_by_count']
)
```

## Common Filter Patterns

### Date Ranges
```python
# Single year
filter_params={"publication_year": "2023"}

# After year
filter_params={"publication_year": ">2020"}

# Range
filter_params={"publication_year": "2020-2024"}
```

### Multiple Filters (AND)
```python
# All conditions must match
filter_params={
    "publication_year": ">2020",
    "is_oa": "true",
    "cited_by_count": ">100"
}
```

### Multiple Values (OR)
```python
# Any institution matches
filter_params={
    "authorships.institutions.id": "I136199984|I27837315"  # MIT or Harvard
}
```

### Collaboration (AND within attribute)
```python
# Papers with authors from BOTH institutions
filter_params={
    "authorships.institutions.id": "I136199984+I27837315"  # MIT AND Harvard
}
```

### Negation
```python
# Exclude type
filter_params={
    "type": "!paratext"
}
```

## Entity Types

OpenAlex provides these entity types:
- **works** - Scholarly documents (articles, books, datasets)
- **authors** - Researchers with disambiguated identities
- **institutions** - Universities and research organizations
- **sources** - Journals, repositories, conferences
- **topics** - Subject classifications
- **publishers** - Publishing organizations
- **funders** - Funding agencies

Access any entity type using consistent patterns:
```python
client.search_works(...)
client.get_entity('authors', author_id)
client.group_by('works', 'topics.id', filter_params={...})
```

## External IDs

Use external identifiers directly:
```python
# DOI for works
work = client.get_entity('works', 'https://doi.org/10.7717/peerj.4375')

# ORCID for authors
author = client.get_entity('authors', 'https://orcid.org/0000-0003-1613-5981')

# ROR for institutions
institution = client.get_entity('institutions', 'https://ror.org/02y3ad647')

# ISSN for sources
source = client.get_entity('sources', 'issn:0028-0836')
```

## Reference Documentation

### Detailed API Reference
See `references/api_guide.md` for:
- Complete filter syntax
- All available endpoints
- Response structures
- Error handling
- Performance optimization
- Rate limiting details

### Common Query Examples
See `references/common_queries.md` for:
- Complete working examples
- Real-world use cases
- Complex query patterns
- Data export workflows
- Multi-step analysis procedures

## Scripts

### openalex_client.py
Main API client with:
- Automatic rate limiting
- Exponential backoff retry logic
- Pagination support
- Batch operations
- Error handling

Use for direct API access with full control.

### query_helpers.py
High-level helper functions for common operations:
- `find_author_works()` - Get papers by author
- `find_institution_works()` - Get papers from institution
- `find_highly_cited_recent_papers()` - Get influential papers
- `get_open_access_papers()` - Find OA publications
- `get_publication_trends()` - Analyze trends over time
- `analyze_research_output()` - Comprehensive analysis

Use for common research queries with simplified interfaces.

## Troubleshooting

### Rate Limiting
If encountering 403 errors:
1. Ensure email is added to requests
2. Verify not exceeding 10 req/sec
3. Client automatically implements exponential backoff

### Empty Results
If searches return no results:
1. Check filter syntax (see `references/api_guide.md`)
2. Use two-step pattern for entity lookups (don't filter by names)
3. Verify entity IDs are correct format

### Timeout Errors
For large queries:
1. Use pagination with `per-page=200`
2. Use `select=` to limit returned fields
3. Break into smaller queries if needed

## Rate Limits

- **Default**: 1 request/second, 100k requests/day
- **Polite pool (with email)**: 10 requests/second, 100k requests/day

Always use polite pool for production workflows by providing email to client.

## Notes

- No authentication required
- All data is open and free
- Rate limits apply globally, not per IP
- Use LitLLM with OpenRouter if LLM-based analysis is needed (don't use Perplexity API directly)
- Client handles pagination, retries, and rate limiting automatically

---

## Reference: Api_Guide

# OpenAlex API Complete Guide

## Base Information

**Base URL:** `https://api.openalex.org`
**Authentication:** None required
**Rate Limits:**
- Default: 1 request/second, 100k requests/day
- Polite pool (with email): 10 requests/second, 100k requests/day

## Critical Best Practices

### ✅ DO: Use `?sample` parameter for random sampling
```
https://api.openalex.org/works?sample=20&seed=123
```
For large samples (10k+), use multiple seeds and deduplicate.

### ❌ DON'T: Use random page numbers for sampling
Incorrect: `?page=5`, `?page=17` - This biases results!

### ✅ DO: Use two-step lookup for entity filtering
```
1. Find entity ID: /authors?search=einstein
2. Use ID: /works?filter=authorships.author.id:A5023888391
```

### ❌ DON'T: Filter by entity names directly
Incorrect: `/works?filter=author_name:Einstein` - Names are ambiguous!

### ✅ DO: Use maximum page size for bulk extraction
```
?per-page=200
```
This is 8x faster than default (25).

### ❌ DON'T: Use default page sizes
Default is only 25 results per page.

### ✅ DO: Use OR filter (pipe |) for batch lookups
```
/works?filter=doi:10.1/abc|10.2/def|10.3/ghi
```
Up to 50 values per filter.

### ❌ DON'T: Make sequential API calls for lists
Making 100 separate calls when you can batch them is inefficient.

### ✅ DO: Implement exponential backoff for retries
```python
for attempt in range(max_retries):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        wait_time = 2 ** attempt
        time.sleep(wait_time)
```

### ✅ DO: Add email for 10x rate limit boost
```
?mailto=yourname@example.edu
```
Increases from 1 req/sec → 10 req/sec.

## Entity Endpoints

- `/works` - 240M+ scholarly documents
- `/authors` - Researcher profiles
- `/sources` - Journals, repositories, conferences
- `/institutions` - Universities, research organizations
- `/topics` - Subject classifications (3-level hierarchy)
- `/publishers` - Publishing organizations
- `/funders` - Funding agencies
- `/text` - Tag your own text with topics/keywords (POST)

## Essential Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `filter=` | Filter results | `?filter=publication_year:2020` |
| `search=` | Full-text search | `?search=machine+learning` |
| `sort=` | Sort results | `?sort=cited_by_count:desc` |
| `per-page=` | Results per page (max 200) | `?per-page=200` |
| `page=` | Page number | `?page=2` |
| `sample=` | Random results | `?sample=50&seed=42` |
| `select=` | Limit fields | `?select=id,title` |
| `group_by=` | Aggregate by field | `?group_by=publication_year` |
| `mailto=` | Email for polite pool | `?mailto=you@example.edu` |

## Filter Syntax

### Basic Filtering
```
Single filter:     ?filter=publication_year:2020
Multiple (AND):    ?filter=publication_year:2020,is_oa:true
Values (OR):       ?filter=type:journal-article|book
Negation:          ?filter=type:!journal-article
```

### Comparison Operators
```
Greater than:      ?filter=cited_by_count:>100
Less than:         ?filter=publication_year:<2020
Range:             ?filter=publication_year:2020-2023
```

### Multiple Values in Same Attribute
```
Repeat filter:     ?filter=institutions.country_code:us,institutions.country_code:gb
Use + symbol:      ?filter=institutions.country_code:us+gb
```
Both mean: "works with author from US AND author from GB"

### OR Queries
```
Any of these:      ?filter=institutions.country_code:us|gb|ca
Batch IDs:         ?filter=doi:10.1/abc|10.2/def
```
Up to 50 values with pipes.

## Common Query Patterns

### Get Random Sample
```bash
# Small sample
https://api.openalex.org/works?sample=20&seed=42

# Large sample (10k+) - make multiple requests
https://api.openalex.org/works?sample=1000&seed=1
https://api.openalex.org/works?sample=1000&seed=2
# Then deduplicate by ID
```

### Search Works
```bash
# Simple search
https://api.openalex.org/works?search=machine+learning

# Search specific field
https://api.openalex.org/works?filter=title.search:CRISPR

# Search + filter
https://api.openalex.org/works?search=climate&filter=publication_year:2023
```

### Find Works by Author (Two-Step)
```bash
# Step 1: Get author ID
https://api.openalex.org/authors?search=Heather+Piwowar
# Returns: "id": "https://openalex.org/A5023888391"

# Step 2: Get their works
https://api.openalex.org/works?filter=authorships.author.id:A5023888391
```

### Find Works by Institution (Two-Step)
```bash
# Step 1: Get institution ID
https://api.openalex.org/institutions?search=MIT
# Returns: "id": "https://openalex.org/I136199984"

# Step 2: Get their works
https://api.openalex.org/works?filter=authorships.institutions.id:I136199984
```

### Highly Cited Recent Papers
```bash
https://api.openalex.org/works?filter=publication_year:>2020&sort=cited_by_count:desc&per-page=200
```

### Open Access Works
```bash
# All OA
https://api.openalex.org/works?filter=is_oa:true

# Gold OA only
https://api.openalex.org/works?filter=open_access.oa_status:gold
```

### Multiple Criteria
```bash
# Recent OA works about COVID from top institutions
https://api.openalex.org/works?filter=publication_year:2022,is_oa:true,title.search:covid,authorships.institutions.id:I136199984|I27837315
```

### Bulk DOI Lookup
```bash
# Get specific works by DOI (up to 50 per request)
https://api.openalex.org/works?filter=doi:https://doi.org/10.1371/journal.pone.0266781|https://doi.org/10.1371/journal.pone.0267149&per-page=50
```

### Aggregate Data
```bash
# Top topics
https://api.openalex.org/works?group_by=topics.id

# Papers per year
https://api.openalex.org/works?group_by=publication_year

# Most prolific institutions
https://api.openalex.org/works?group_by=authorships.institutions.id
```

### Pagination
```bash
# First page
https://api.openalex.org/works?filter=publication_year:2023&per-page=200

# Next pages
https://api.openalex.org/works?filter=publication_year:2023&per-page=200&page=2
```

## Response Structure

### List Endpoints
```json
{
  "meta": {
    "count": 240523418,
    "db_response_time_ms": 42,
    "page": 1,
    "per_page": 25
  },
  "results": [
    { /* entity object */ }
  ]
}
```

### Single Entity
```
https://api.openalex.org/works/W2741809807
→ Returns Work object directly (no meta/results wrapper)
```

### Group By
```json
{
  "meta": { "count": 100 },
  "group_by": [
    {
      "key": "https://openalex.org/T10001",
      "key_display_name": "Artificial Intelligence",
      "count": 15234
    }
  ]
}
```

## Works Filters (Most Common)

| Filter | Description | Example |
|--------|-------------|---------|
| `authorships.author.id` | Author's OpenAlex ID | `A5023888391` |
| `authorships.institutions.id` | Institution's ID | `I136199984` |
| `cited_by_count` | Citation count | `>100` |
| `is_oa` | Is open access | `true/false` |
| `publication_year` | Year published | `2020`, `>2020`, `2018-2022` |
| `primary_location.source.id` | Source (journal) ID | `S137773608` |
| `topics.id` | Topic ID | `T10001` |
| `type` | Document type | `article`, `book`, `dataset` |
| `has_doi` | Has DOI | `true/false` |
| `has_fulltext` | Has fulltext | `true/false` |

## Authors Filters

| Filter | Description |
|--------|-------------|
| `last_known_institution.id` | Current/last institution |
| `works_count` | Number of works |
| `cited_by_count` | Total citations |
| `orcid` | ORCID identifier |

## External ID Support

### Works
```
DOI:  /works/https://doi.org/10.7717/peerj.4375
PMID: /works/pmid:29844763
```

### Authors
```
ORCID: /authors/https://orcid.org/0000-0003-1613-5981
```

### Institutions
```
ROR: /institutions/https://ror.org/02y3ad647
```

### Sources
```
ISSN: /sources/issn:0028-0836
```

## Performance Tips

1. **Use maximum page size**: `?per-page=200` (8x fewer calls)
2. **Batch ID lookups**: Use pipe operator for up to 50 IDs
3. **Select only needed fields**: `?select=id,title,publication_year`
4. **Use concurrent requests**: With rate limiting (10 req/sec with email)
5. **Add email**: `?mailto=you@example.edu` for 10x speed boost

## Error Handling

### HTTP Status Codes
- `200` - Success
- `400` - Bad request (check filter syntax)
- `403` - Rate limit exceeded (implement backoff)
- `404` - Entity doesn't exist
- `500` - Server error (retry with backoff)

### Exponential Backoff
```python
def fetch_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [403, 500, 502, 503, 504]:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                response.raise_for_status()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```

## Rate Limiting

### Without Email (Default Pool)
- 1 request/second
- 100,000 requests/day

### With Email (Polite Pool)
- 10 requests/second
- 100,000 requests/day
- **Always use for production**

### Concurrent Request Strategy
1. Track requests per second globally
2. Use semaphore or rate limiter across threads
3. Monitor for 403 responses
4. Back off if limits hit

## Common Mistakes to Avoid

1. ❌ Using page numbers for sampling → ✅ Use `?sample=`
2. ❌ Filtering by entity names → ✅ Get IDs first
3. ❌ Default page size → ✅ Use `per-page=200`
4. ❌ Sequential ID lookups → ✅ Batch with pipe operator
5. ❌ No error handling → ✅ Implement retry with backoff
6. ❌ Ignoring rate limits → ✅ Global rate limiting
7. ❌ Not including email → ✅ Add `mailto=`
8. ❌ Fetching all fields → ✅ Use `select=`

## Additional Resources

- Full documentation: https://docs.openalex.org
- API Overview: https://docs.openalex.org/how-to-use-the-api/api-overview
- Entity schemas: https://docs.openalex.org/api-entities
- Help: https://openalex.org/help
- User group: https://groups.google.com/g/openalex-users

---

## Reference: Common_Queries

# Common OpenAlex Query Examples

This document provides practical examples for common research queries using OpenAlex.

## Finding Papers by Author

**User query**: "Find papers by Albert Einstein"

**Approach**: Two-step pattern
1. Search for author to get ID
2. Filter works by author ID

**Python example**:
```python
from scripts.openalex_client import OpenAlexClient
from scripts.query_helpers import find_author_works

client = OpenAlexClient(email="your-email@example.edu")
works = find_author_works("Albert Einstein", client, limit=100)

for work in works:
    print(f"{work['title']} ({work['publication_year']})")
```

## Finding Papers from an Institution

**User query**: "What papers has MIT published in the last year?"

**Approach**: Two-step pattern with date filter
1. Search for institution to get ID
2. Filter works by institution ID and year

**Python example**:
```python
from scripts.query_helpers import find_institution_works

works = find_institution_works("MIT", client, limit=200)

# Filter for recent papers
import datetime
current_year = datetime.datetime.now().year
recent_works = [w for w in works if w['publication_year'] == current_year]
```

## Highly Cited Papers on a Topic

**User query**: "Find the most cited papers on CRISPR from the last 5 years"

**Approach**: Search + filter + sort

**Python example**:
```python
works = client.search_works(
    search="CRISPR",
    filter_params={
        "publication_year": ">2019"
    },
    sort="cited_by_count:desc",
    per_page=100
)

for work in works['results']:
    title = work['title']
    citations = work['cited_by_count']
    year = work['publication_year']
    print(f"{title} ({year}): {citations} citations")
```

## Open Access Papers on a Topic

**User query**: "Find open access papers about climate change"

**Approach**: Search + OA filter

**Python example**:
```python
from scripts.query_helpers import get_open_access_papers

papers = get_open_access_papers(
    search_term="climate change",
    client=client,
    oa_status="any",  # or "gold", "green", "hybrid", "bronze"
    limit=200
)

for paper in papers:
    print(f"{paper['title']}")
    print(f"  OA Status: {paper['open_access']['oa_status']}")
    print(f"  URL: {paper['open_access']['oa_url']}")
```

## Publication Trends Analysis

**User query**: "Show me publication trends for machine learning over the years"

**Approach**: Use group_by to aggregate by year

**Python example**:
```python
from scripts.query_helpers import get_publication_trends

trends = get_publication_trends(
    search_term="machine learning",
    client=client
)

# Sort by year
trends_sorted = sorted(trends, key=lambda x: x['key'])

for trend in trends_sorted[-10:]:  # Last 10 years
    year = trend['key']
    count = trend['count']
    print(f"{year}: {count} publications")
```

## Analyzing Research Output

**User query**: "Analyze the research output of Stanford University from 2020-2024"

**Approach**: Multiple aggregations for comprehensive analysis

**Python example**:
```python
from scripts.query_helpers import analyze_research_output

analysis = analyze_research_output(
    entity_type='institution',
    entity_name='Stanford University',
    client=client,
    years='2020-2024'
)

print(f"Institution: {analysis['entity_name']}")
print(f"Total works: {analysis['total_works']}")
print(f"Open access: {analysis['open_access_percentage']}%")
print("\nTop topics:")
for topic in analysis['top_topics'][:5]:
    print(f"  - {topic['key_display_name']}: {topic['count']} works")
```

## Finding Papers by DOI (Batch)

**User query**: "Get information for these 10 DOIs: ..."

**Approach**: Batch lookup with pipe separator

**Python example**:
```python
dois = [
    "https://doi.org/10.1371/journal.pone.0266781",
    "https://doi.org/10.1371/journal.pone.0267149",
    "https://doi.org/10.1038/s41586-021-03819-2",
    # ... up to 50 DOIs
]

works = client.batch_lookup(
    entity_type='works',
    ids=dois,
    id_field='doi'
)

for work in works:
    print(f"{work['title']} - {work['publication_year']}")
```

## Random Sample of Papers

**User query**: "Give me 50 random papers from 2023"

**Approach**: Use sample parameter with seed for reproducibility

**Python example**:
```python
works = client.sample_works(
    sample_size=50,
    seed=42,  # For reproducibility
    filter_params={
        "publication_year": "2023",
        "is_oa": "true"
    }
)

print(f"Got {len(works)} random papers from 2023")
```

## Papers from Multiple Institutions

**User query**: "Find papers with authors from both MIT and Stanford"

**Approach**: Use + operator for AND within same attribute

**Python example**:
```python
# First, get institution IDs
mit_response = client._make_request(
    '/institutions',
    params={'search': 'MIT', 'per-page': 1}
)
mit_id = mit_response['results'][0]['id'].split('/')[-1]

stanford_response = client._make_request(
    '/institutions',
    params={'search': 'Stanford', 'per-page': 1}
)
stanford_id = stanford_response['results'][0]['id'].split('/')[-1]

# Find works with authors from both institutions
works = client.search_works(
    filter_params={
        "authorships.institutions.id": f"{mit_id}+{stanford_id}"
    },
    per_page=100
)

print(f"Found {works['meta']['count']} collaborative papers")
```

## Papers in a Specific Journal

**User query**: "Get all papers from Nature published in 2023"

**Approach**: Two-step - find journal ID, then filter works

**Python example**:
```python
# Step 1: Find journal source ID
source_response = client._make_request(
    '/sources',
    params={'search': 'Nature', 'per-page': 1}
)
source = source_response['results'][0]
source_id = source['id'].split('/')[-1]

print(f"Found journal: {source['display_name']} (ID: {source_id})")

# Step 2: Get works from that source
works = client.search_works(
    filter_params={
        "primary_location.source.id": source_id,
        "publication_year": "2023"
    },
    per_page=200
)

print(f"Found {works['meta']['count']} papers from Nature in 2023")
```

## Topic Analysis by Institution

**User query**: "What topics does MIT research most?"

**Approach**: Filter by institution, group by topics

**Python example**:
```python
# Get MIT ID
inst_response = client._make_request(
    '/institutions',
    params={'search': 'MIT', 'per-page': 1}
)
mit_id = inst_response['results'][0]['id'].split('/')[-1]

# Group by topics
topics = client.group_by(
    entity_type='works',
    group_field='topics.id',
    filter_params={
        "authorships.institutions.id": mit_id,
        "publication_year": ">2020"
    }
)

print("Top research topics at MIT (2020+):")
for i, topic in enumerate(topics[:10], 1):
    print(f"{i}. {topic['key_display_name']}: {topic['count']} works")
```

## Citation Analysis

**User query**: "Find papers that cite this specific DOI"

**Approach**: Get work by DOI, then use cited_by_api_url

**Python example**:
```python
# Get the work
doi = "https://doi.org/10.1038/s41586-021-03819-2"
work = client.get_entity('works', doi)

# Get papers that cite it
cited_by_url = work['cited_by_api_url']

# Extract just the query part and use it
import requests
response = requests.get(cited_by_url, params={'mailto': client.email})
citing_works = response.json()

print(f"{work['title']}")
print(f"Total citations: {work['cited_by_count']}")
print(f"\nRecent citing papers:")
for citing_work in citing_works['results'][:5]:
    print(f"  - {citing_work['title']} ({citing_work['publication_year']})")
```

## Large-Scale Data Extraction

**User query**: "Get all papers on quantum computing from the last 3 years"

**Approach**: Paginate through all results

**Python example**:
```python
all_papers = client.paginate_all(
    endpoint='/works',
    params={
        'search': 'quantum computing',
        'filter': 'publication_year:2022-2024'
    },
    max_results=10000  # Limit to prevent excessive API calls
)

print(f"Retrieved {len(all_papers)} papers")

# Save to CSV
import csv
with open('quantum_papers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Citations', 'DOI', 'OA Status'])

    for paper in all_papers:
        writer.writerow([
            paper['title'],
            paper['publication_year'],
            paper['cited_by_count'],
            paper.get('doi', 'N/A'),
            paper['open_access']['oa_status']
        ])
```

## Complex Multi-Filter Query

**User query**: "Find recent, highly-cited, open access papers on AI from top institutions"

**Approach**: Combine multiple filters

**Python example**:
```python
# Get IDs for top institutions
top_institutions = ['MIT', 'Stanford', 'Oxford']
inst_ids = []

for inst_name in top_institutions:
    response = client._make_request(
        '/institutions',
        params={'search': inst_name, 'per-page': 1}
    )
    if response['results']:
        inst_id = response['results'][0]['id'].split('/')[-1]
        inst_ids.append(inst_id)

# Combine with pipe for OR
inst_filter = '|'.join(inst_ids)

# Complex query
works = client.search_works(
    search="artificial intelligence",
    filter_params={
        "publication_year": ">2022",
        "cited_by_count": ">50",
        "is_oa": "true",
        "authorships.institutions.id": inst_filter
    },
    sort="cited_by_count:desc",
    per_page=200
)

print(f"Found {works['meta']['count']} papers matching criteria")
for work in works['results'][:10]:
    print(f"{work['title']}")
    print(f"  Citations: {work['cited_by_count']}, Year: {work['publication_year']}")
```
