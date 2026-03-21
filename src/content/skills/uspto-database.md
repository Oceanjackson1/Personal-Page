---
title: "Uspto Database"
description: "Access USPTO APIs for patent/trademark searches, examination history (PEDS), assignments, citations, office actions, TSDR, for IP analysis and prior art searches."
category: "research"
source: "community"
author: "Community"
tags: ["uspto", "database"]
date: 2026-03-20
---

# USPTO Database

## Overview

USPTO provides specialized APIs for patent and trademark data. Search patents by keywords/inventors/assignees, retrieve examination history via PEDS, track assignments, analyze citations and office actions, access TSDR for trademarks, for IP analysis and prior art searches.

## When to Use This Skill

This skill should be used when:

- **Patent Search**: Finding patents by keywords, inventors, assignees, classifications, or dates
- **Patent Details**: Retrieving full patent data including claims, abstracts, citations
- **Trademark Search**: Looking up trademarks by serial or registration number
- **Trademark Status**: Checking trademark status, ownership, and prosecution history
- **Examination History**: Accessing patent prosecution data from PEDS (Patent Examination Data System)
- **Office Actions**: Retrieving office action text, citations, and rejections
- **Assignments**: Tracking patent/trademark ownership transfers
- **Citations**: Analyzing patent citations (forward and backward)
- **Litigation**: Accessing patent litigation records
- **Portfolio Analysis**: Analyzing patent/trademark portfolios for companies or inventors

## USPTO API Ecosystem

The USPTO provides multiple specialized APIs for different data needs:

### Core APIs

1. **PatentSearch API** - Modern ElasticSearch-based patent search (replaced legacy PatentsView in May 2025)
   - Search patents by keywords, inventors, assignees, classifications, dates
   - Access to patent data through June 30, 2025
   - 45 requests/minute rate limit
   - **Base URL**: `https://search.patentsview.org/api/v1/`

2. **PEDS (Patent Examination Data System)** - Patent examination history
   - Application status and transaction history from 1981-present
   - Office action dates and examination events
   - Use `uspto-opendata-python` Python library
   - **Replaced**: PAIR Bulk Data (PBD) - decommissioned

3. **TSDR (Trademark Status & Document Retrieval)** - Trademark data
   - Trademark status, ownership, prosecution history
   - Search by serial or registration number
   - **Base URL**: `https://tsdrapi.uspto.gov/ts/cd/`

### Additional APIs

4. **Patent Assignment Search** - Ownership records and transfers
5. **Trademark Assignment Search** - Trademark ownership changes
6. **Enriched Citation API** - Patent citation analysis
7. **Office Action Text Retrieval** - Full text of office actions
8. **Office Action Citations** - Citations from office actions
9. **Office Action Rejection** - Rejection reasons and types
10. **PTAB API** - Patent Trial and Appeal Board proceedings
11. **Patent Litigation Cases** - Federal district court litigation data
12. **Cancer Moonshot Data Set** - Cancer-related patents

## Quick Start

### API Key Registration

USPTO APIs require an API key. Register at:
**https://account.uspto.gov/api-manager/**

API key for **PatentSearch API** is provided by PatentsView. Register at:
**https://patentsview.org/api-v01-information-page**

Set the API key as an environment variable:
```bash
export USPTO_API_KEY="your_api_key_here"
export PATENTSVIEW_API_KEY="you_api_key_here"
```

### Helper Scripts

This skill includes Python scripts for common operations:

- **`scripts/patent_search.py`** - PatentSearch API client for searching patents
- **`scripts/peds_client.py`** - PEDS client for examination history
- **`scripts/trademark_client.py`** - TSDR client for trademark data

## Task 1: Searching Patents

### Using the PatentSearch API

The PatentSearch API uses a JSON query language with various operators for flexible searching.

#### Basic Patent Search Examples

**Search by keywords in abstract:**
```python
from scripts.patent_search import PatentSearchClient

client = PatentSearchClient()

# Search for machine learning patents
results = client.search_patents({
    "_text_all": {"patent_abstract": "machine learning"}
})

for patent in results['patents']:
    print(f"{patent['patent_number']}: {patent['patent_title']}")
```

**Search by inventor:**
```python
results = client.search_by_inventor("John Smith")
```

**Search by assignee/company:**
```python
results = client.search_by_assignee("Google")
```

**Search by date range:**
```python
results = client.search_by_date_range("2024-01-01", "2024-12-31")
```

**Search by CPC classification:**
```python
results = client.search_by_classification("H04N")  # Video/image tech
```

#### Advanced Patent Search

Combine multiple criteria with logical operators:

```python
results = client.advanced_search(
    keywords=["artificial", "intelligence"],
    assignee="Microsoft",
    start_date="2023-01-01",
    end_date="2024-12-31",
    cpc_codes=["G06N", "G06F"]  # AI and computing classifications
)
```

#### Direct API Usage

For complex queries, use the API directly:

```python
import requests

url = "https://search.patentsview.org/api/v1/patent"
headers = {
    "X-Api-Key": "YOUR_API_KEY",
    "Content-Type": "application/json"
}

query = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"assignee_organization": {"_text_any": ["Google", "Alphabet"]}},
            {"cpc_subclass_id": ["G06N", "H04N"]}
        ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "inventor_name"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100, "page": 1}
}

response = requests.post(url, headers=headers, json=query)
results = response.json()
```

### Query Operators

- **Equality**: `{"field": "value"}` or `{"field": {"_eq": "value"}}`
- **Comparison**: `_gt`, `_gte`, `_lt`, `_lte`, `_neq`
- **Text search**: `_text_all`, `_text_any`, `_text_phrase`
- **String matching**: `_begins`, `_contains`
- **Logical**: `_and`, `_or`, `_not`

**Best Practice**: Use `_text_*` operators for text fields (more performant than `_contains` or `_begins`)

### Available Patent Endpoints

- `/patent` - Granted patents
- `/publication` - Pregrant publications
- `/inventor` - Inventor information
- `/assignee` - Assignee information
- `/cpc_subclass`, `/cpc_at_issue` - CPC classifications
- `/uspc` - US Patent Classification
- `/ipc` - International Patent Classification
- `/claims`, `/brief_summary_text`, `/detail_description_text` - Text data (beta)

### Reference Documentation

See `references/patentsearch_api.md` for complete PatentSearch API documentation including:
- All available endpoints
- Complete field reference
- Query syntax and examples
- Response formats
- Rate limits and best practices

## Task 2: Retrieving Patent Examination Data

### Using PEDS (Patent Examination Data System)

PEDS provides comprehensive prosecution history including transaction events, status changes, and examination timeline.

#### Installation

```bash
uv pip install uspto-opendata-python
```

#### Basic PEDS Usage

**Get application data:**
```python
from scripts.peds_client import PEDSHelper

helper = PEDSHelper()

# By application number
app_data = helper.get_application("16123456")
print(f"Title: {app_data['title']}")
print(f"Status: {app_data['app_status']}")

# By patent number
patent_data = helper.get_patent("11234567")
```

**Get transaction history:**
```python
transactions = helper.get_transaction_history("16123456")

for trans in transactions:
    print(f"{trans['date']}: {trans['code']} - {trans['description']}")
```

**Get office actions:**
```python
office_actions = helper.get_office_actions("16123456")

for oa in office_actions:
    if oa['code'] == 'CTNF':
        print(f"Non-final rejection: {oa['date']}")
    elif oa['code'] == 'CTFR':
        print(f"Final rejection: {oa['date']}")
    elif oa['code'] == 'NOA':
        print(f"Notice of allowance: {oa['date']}")
```

**Get status summary:**
```python
summary = helper.get_status_summary("16123456")

print(f"Current status: {summary['current_status']}")
print(f"Filing date: {summary['filing_date']}")
print(f"Pendency: {summary['pendency_days']} days")

if summary['is_patented']:
    print(f"Patent number: {summary['patent_number']}")
    print(f"Issue date: {summary['issue_date']}")
```

#### Prosecution Analysis

Analyze prosecution patterns:

```python
analysis = helper.analyze_prosecution("16123456")

print(f"Total office actions: {analysis['total_office_actions']}")
print(f"Non-final rejections: {analysis['non_final_rejections']}")
print(f"Final rejections: {analysis['final_rejections']}")
print(f"Allowed: {analysis['allowance']}")
print(f"Responses filed: {analysis['responses']}")
```

### Common Transaction Codes

- **CTNF** - Non-final rejection mailed
- **CTFR** - Final rejection mailed
- **NOA** - Notice of allowance mailed
- **WRIT** - Response filed
- **ISS.FEE** - Issue fee payment
- **ABND** - Application abandoned
- **AOPF** - Office action mailed

### Reference Documentation

See `references/peds_api.md` for complete PEDS documentation including:
- All available data fields
- Transaction code reference
- Python library usage
- Portfolio analysis examples

## Task 3: Searching and Monitoring Trademarks

### Using TSDR (Trademark Status & Document Retrieval)

Access trademark status, ownership, and prosecution history.

#### Basic Trademark Usage

**Get trademark by serial number:**
```python
from scripts.trademark_client import TrademarkClient

client = TrademarkClient()

# By serial number
tm_data = client.get_trademark_by_serial("87654321")

# By registration number
tm_data = client.get_trademark_by_registration("5678901")
```

**Get trademark status:**
```python
status = client.get_trademark_status("87654321")

print(f"Mark: {status['mark_text']}")
print(f"Status: {status['status']}")
print(f"Filing date: {status['filing_date']}")

if status['is_registered']:
    print(f"Registration #: {status['registration_number']}")
    print(f"Registration date: {status['registration_date']}")
```

**Check trademark health:**
```python
health = client.check_trademark_health("87654321")

print(f"Mark: {health['mark']}")
print(f"Status: {health['status']}")

for alert in health['alerts']:
    print(alert)

if health['needs_attention']:
    print("⚠️  This mark needs attention!")
```

#### Trademark Portfolio Monitoring

Monitor multiple trademarks:

```python
def monitor_portfolio(serial_numbers, api_key):
    """Monitor trademark portfolio health."""
    client = TrademarkClient(api_key)

    results = {
        'active': [],
        'pending': [],
        'problems': []
    }

    for sn in serial_numbers:
        health = client.check_trademark_health(sn)

        if 'REGISTERED' in health['status']:
            results['active'].append(health)
        elif 'PENDING' in health['status'] or 'PUBLISHED' in health['status']:
            results['pending'].append(health)
        elif health['needs_attention']:
            results['problems'].append(health)

    return results
```

### Common Trademark Statuses

- **REGISTERED** - Active registered mark
- **PENDING** - Under examination
- **PUBLISHED FOR OPPOSITION** - In opposition period
- **ABANDONED** - Application abandoned
- **CANCELLED** - Registration cancelled
- **SUSPENDED** - Examination suspended
- **REGISTERED AND RENEWED** - Registration renewed

### Reference Documentation

See `references/trademark_api.md` for complete trademark API documentation including:
- TSDR API reference
- Trademark Assignment Search API
- All status codes
- Prosecution history access
- Ownership tracking

## Task 4: Tracking Assignments and Ownership

### Patent and Trademark Assignments

Both patents and trademarks have Assignment Search APIs for tracking ownership changes.

#### Patent Assignment API

**Base URL**: `https://assignment-api.uspto.gov/patent/v1.4/`

**Search by patent number:**
```python
import requests
import xml.etree.ElementTree as ET

def get_patent_assignments(patent_number, api_key):
    url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # Returns XML

assignments_xml = get_patent_assignments("11234567", api_key)
root = ET.fromstring(assignments_xml)

for assignment in root.findall('.//assignment'):
    recorded_date = assignment.find('recordedDate').text
    assignor = assignment.find('.//assignor/name').text
    assignee = assignment.find('.//assignee/name').text
    conveyance = assignment.find('conveyanceText').text

    print(f"{recorded_date}: {assignor} → {assignee}")
    print(f"  Type: {conveyance}\n")
```

**Search by company name:**
```python
def find_company_patents(company_name, api_key):
    url = "https://assignment-api.uspto.gov/patent/v1.4/assignment/search"
    headers = {"X-Api-Key": api_key}
    data = {"criteria": {"assigneeName": company_name}}

    response = requests.post(url, headers=headers, json=data)
    return response.text
```

### Common Assignment Types

- **ASSIGNMENT OF ASSIGNORS INTEREST** - Ownership transfer
- **SECURITY AGREEMENT** - Collateral/security interest
- **MERGER** - Corporate merger
- **CHANGE OF NAME** - Name change
- **ASSIGNMENT OF PARTIAL INTEREST** - Partial ownership

## Task 5: Accessing Additional USPTO Data

### Office Actions, Citations, and Litigation

Multiple specialized APIs provide additional patent data.

#### Office Action Text Retrieval

Retrieve full text of office actions using application number. Integrate with PEDS to identify which office actions exist, then retrieve full text.

#### Enriched Citation API

Analyze patent citations:
- Forward citations (patents citing this patent)
- Backward citations (prior art cited)
- Examiner vs. applicant citations
- Citation context

#### Patent Litigation Cases API

Access federal district court patent litigation records:
- 74,623+ litigation records
- Patents asserted
- Parties and venues
- Case outcomes

#### PTAB API

Patent Trial and Appeal Board proceedings:
- Inter partes review (IPR)
- Post-grant review (PGR)
- Appeal decisions

### Reference Documentation

See `references/additional_apis.md` for comprehensive documentation on:
- Enriched Citation API
- Office Action APIs (Text, Citations, Rejections)
- Patent Litigation Cases API
- PTAB API
- Cancer Moonshot Data Set
- OCE Status/Event Codes

## Complete Analysis Example

### Comprehensive Patent Analysis

Combine multiple APIs for complete patent intelligence:

```python
def comprehensive_patent_analysis(patent_number, api_key):
    """
    Full patent analysis using multiple USPTO APIs.
    """
    from scripts.patent_search import PatentSearchClient
    from scripts.peds_client import PEDSHelper

    results = {}

    # 1. Get patent details
    patent_client = PatentSearchClient(api_key)
    patent_data = patent_client.get_patent(patent_number)
    results['patent'] = patent_data

    # 2. Get examination history
    peds = PEDSHelper()
    results['prosecution'] = peds.analyze_prosecution(patent_number)
    results['status'] = peds.get_status_summary(patent_number)

    # 3. Get assignment history
    import requests
    assign_url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    assign_resp = requests.get(assign_url, headers={"X-Api-Key": api_key})
    results['assignments'] = assign_resp.text if assign_resp.status_code == 200 else None

    # 4. Analyze results
    print(f"\n=== Patent {patent_number} Analysis ===\n")
    print(f"Title: {patent_data['patent_title']}")
    print(f"Assignee: {', '.join(patent_data.get('assignee_organization', []))}")
    print(f"Issue Date: {patent_data['patent_date']}")

    print(f"\nProsecution:")
    print(f"  Office Actions: {results['prosecution']['total_office_actions']}")
    print(f"  Rejections: {results['prosecution']['non_final_rejections']} non-final, {results['prosecution']['final_rejections']} final")
    print(f"  Pendency: {results['prosecution']['pendency_days']} days")

    # Analyze citations
    if 'cited_patent_number' in patent_data:
        print(f"\nCitations:")
        print(f"  Cites: {len(patent_data['cited_patent_number'])} patents")
    if 'citedby_patent_number' in patent_data:
        print(f"  Cited by: {len(patent_data['citedby_patent_number'])} patents")

    return results
```

## Best Practices

1. **API Key Management**
   - Store API key in environment variables
   - Never commit keys to version control
   - Use same key across all USPTO APIs

2. **Rate Limiting**
   - PatentSearch: 45 requests/minute
   - Implement exponential backoff for rate limit errors
   - Cache responses when possible

3. **Query Optimization**
   - Use `_text_*` operators for text fields (more performant)
   - Request only needed fields to reduce response size
   - Use date ranges to narrow searches

4. **Data Handling**
   - Not all fields populated for all patents/trademarks
   - Handle missing data gracefully
   - Parse dates consistently

5. **Combining APIs**
   - Use PatentSearch for discovery
   - Use PEDS for prosecution details
   - Use Assignment APIs for ownership tracking
   - Combine data for comprehensive analysis

## Important Notes

- **Legacy API Sunset**: PatentsView legacy API discontinued May 1, 2025 - use PatentSearch API
- **PAIR Bulk Data Decommissioned**: Use PEDS instead
- **Data Coverage**: PatentSearch has data through June 30, 2025; PEDS from 1981-present
- **Text Endpoints**: Claims and description endpoints are in beta with ongoing backfilling
- **Rate Limits**: Respect rate limits to avoid service disruptions

## Resources

### API Documentation
- **PatentSearch API**: https://search.patentsview.org/docs/
- **USPTO Developer Portal**: https://developer.uspto.gov/
- **USPTO Open Data Portal**: https://data.uspto.gov/
- **API Key Registration**: https://account.uspto.gov/api-manager/

### Python Libraries
- **uspto-opendata-python**: https://pypi.org/project/uspto-opendata-python/
- **USPTO Docs**: https://docs.ip-tools.org/uspto-opendata-python/

### Reference Files
- `references/patentsearch_api.md` - Complete PatentSearch API reference
- `references/peds_api.md` - PEDS API and library documentation
- `references/trademark_api.md` - Trademark APIs (TSDR and Assignment)
- `references/additional_apis.md` - Citations, Office Actions, Litigation, PTAB

### Scripts
- `scripts/patent_search.py` - PatentSearch API client
- `scripts/peds_client.py` - PEDS examination data client
- `scripts/trademark_client.py` - Trademark search client

---

## Reference: Additional_Apis

# Additional USPTO APIs Reference

## Overview

Beyond patent search, PEDS, and trademarks, USPTO provides specialized APIs for citations, office actions, assignments, litigation, and other patent data.

## 1. Enriched Citation API

### Overview

Provides insights into patent evaluation processes and cited references for the IP5 (USPTO, EPO, JPO, KIPO, CNIPA) and public use.

**Versions:** v3, v2, v1

**Base URL:** Access through USPTO Open Data Portal

### Purpose

Analyze which references examiners cite during patent examination and how patents cite prior art.

### Key Features

- **Forward citations** - Patents that cite a given patent
- **Backward citations** - References cited by a patent
- **Examiner citations** - References cited by examiner vs. applicant
- **Citation context** - How and why references are cited

### Use Cases

- Prior art analysis
- Patent landscape analysis
- Identifying related technologies
- Assessing patent strength based on citations

## 2. Office Action APIs

### 2.1 Office Action Text Retrieval API

**Version:** v1

### Purpose

Retrieves complete full-text office action correspondence documents for patent applications.

### Features

- Full text of office actions
- Restrictions, rejections, objections
- Examiner amendments
- Search information

### Example Use

```python
# Retrieve office action text by application number
def get_office_action_text(app_number, api_key):
    """
    Fetch full text of office actions for an application.
    Note: Integrate with PEDS to identify which office actions exist.
    """
    # API implementation
    pass
```

### 2.2 Office Action Citations API

**Versions:** v2, beta v1

### Purpose

Provides patent citation data extracted from office actions, showing which references examiners used during examination.

### Key Data

- Patent and non-patent literature citations
- Citation context (rejection, information, etc.)
- Examiner search strategies
- Prosecution research dataset

### 2.3 Office Action Rejection API

**Versions:** v2, beta v1

### Purpose

Details rejection reasons and examination outcomes with bulk rejection data through March 2025.

### Rejection Types

- **35 U.S.C. § 102** - Anticipation (lack of novelty)
- **35 U.S.C. § 103** - Obviousness
- **35 U.S.C. § 112** - Enablement, written description, indefiniteness
- **35 U.S.C. § 101** - Subject matter eligibility

### Use Cases

- Analyze common rejection reasons
- Identify problematic claim language
- Prepare responses based on historical data
- Portfolio analysis of rejection patterns

### 2.4 Office Action Weekly Zips API

**Version:** v1

### Purpose

Delivers bulk downloads of full-text office action documents organized by weekly release schedules.

### Features

- Weekly archive downloads
- Complete office action text
- Bulk access for large-scale analysis

## 3. Patent Assignment Search API

### Overview

**Version:** v1.4

Accesses USPTO patent assignment database for ownership records and transfers.

**Base URL:** `https://assignment-api.uspto.gov/patent/`

### Purpose

Track patent ownership, assignments, security interests, and corporate transactions.

### Search Methods

#### By Patent Number

```
GET /v1.4/assignment/patent/{patent_number}
```

#### By Application Number

```
GET /v1.4/assignment/application/{application_number}
```

#### By Assignee Name

```
POST /v1.4/assignment/search
{
  "criteria": {
    "assigneeName": "Company Name"
  }
}
```

### Response Format

Returns XML with assignment records similar to trademark assignments:

- Reel/frame numbers
- Conveyance type
- Dates (execution and recorded)
- Assignors and assignees
- Affected patents/applications

### Common Uses

```python
def track_patent_ownership(patent_number, api_key):
    """Track ownership history of a patent."""
    url = f"https://assignment-api.uspto.gov/patent/v1.4/assignment/patent/{patent_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse XML to extract assignment history
        return response.text
    return None

def find_company_patents(company_name, api_key):
    """Find patents assigned to a company."""
    url = "https://assignment-api.uspto.gov/patent/v1.4/assignment/search"
    headers = {"X-Api-Key": api_key}
    data = {"criteria": {"assigneeName": company_name}}

    response = requests.post(url, headers=headers, json=data)
    return response.text
```

## 4. PTAB API (Patent Trial and Appeal Board)

### Overview

**Version:** v2

Access to Patent Trial and Appeal Board proceedings data.

### Purpose

Retrieve information about:
- Inter partes review (IPR)
- Post-grant review (PGR)
- Covered business method (CBM) review
- Ex parte appeals

### Data Available

- Petition information
- Trial decisions
- Final written decisions
- Petitioner and patent owner information
- Claims challenged
- Trial outcomes

### Note

Currently migrating to new Open Data Portal. Check current documentation for access details.

## 5. Patent Litigation Cases API

### Overview

**Version:** v1

Contains 74,623+ district court litigation records covering patent litigation data.

### Purpose

Access federal district court patent infringement cases.

### Key Data

- Case numbers and filing dates
- Patents asserted
- Parties (plaintiffs and defendants)
- Venues
- Case outcomes

### Use Cases

- Litigation risk analysis
- Identify frequently litigated patents
- Track litigation trends
- Analyze venue preferences
- Assess patent enforcement patterns

## 6. Cancer Moonshot Patent Data Set API

### Overview

**Version:** v1.0.1

Specialized dataset for cancer-related patent discoveries.

### Purpose

Search and download patents related to cancer research, treatment, and diagnostics.

### Features

- Curated cancer-related patents
- Bulk data download
- Classification by cancer type
- Treatment modality categorization

### Use Cases

- Cancer research prior art
- Technology landscape analysis
- Identify research trends
- Licensing opportunities

## 7. OCE Patent Examination Status/Event Codes APIs

### Overview

**Version:** v1

Provides official descriptions of USPTO status and event codes used in patent examination.

### Purpose

Decode transaction codes and status codes found in PEDS and other examination data.

### Data Provided

- **Status codes** - Application status descriptions
- **Event codes** - Transaction/event descriptions
- **Code definitions** - Official meanings

### Integration

Use with PEDS data to interpret transaction codes:

```python
def get_code_description(code, api_key):
    """Get human-readable description of USPTO code."""
    # Fetch from OCE API
    pass

def enrich_peds_data(peds_transactions, api_key):
    """Add descriptions to PEDS transaction codes."""
    for trans in peds_transactions:
        trans['description'] = get_code_description(trans['code'], api_key)
    return peds_transactions
```

## API Integration Patterns

### Combined Workflow Example

```python
def comprehensive_patent_analysis(patent_number, api_key):
    """
    Comprehensive analysis combining multiple APIs.
    """
    results = {}

    # 1. Get patent details from PatentSearch
    results['patent_data'] = search_patent(patent_number, api_key)

    # 2. Get examination history from PEDS
    results['prosecution'] = get_peds_data(patent_number, api_key)

    # 3. Get assignment history
    results['assignments'] = get_assignments(patent_number, api_key)

    # 4. Get citation data
    results['citations'] = get_citations(patent_number, api_key)

    # 5. Check litigation history
    results['litigation'] = get_litigation(patent_number, api_key)

    # 6. Get PTAB challenges
    results['ptab'] = get_ptab_proceedings(patent_number, api_key)

    return results
```

### Portfolio Analysis Example

```python
def analyze_company_portfolio(company_name, api_key):
    """
    Analyze a company's patent portfolio using multiple APIs.
    """
    # 1. Find all assigned patents
    assignments = find_company_patents(company_name, api_key)
    patent_numbers = extract_patent_numbers(assignments)

    # 2. Get details for each patent
    portfolio = []
    for patent_num in patent_numbers:
        patent_data = {
            'number': patent_num,
            'details': search_patent(patent_num, api_key),
            'citations': get_citations(patent_num, api_key),
            'litigation': get_litigation(patent_num, api_key)
        }
        portfolio.append(patent_data)

    # 3. Aggregate statistics
    stats = {
        'total_patents': len(portfolio),
        'cited_by_count': sum(len(p['citations']) for p in portfolio),
        'litigated_count': sum(1 for p in portfolio if p['litigation']),
        'technology_areas': aggregate_tech_areas(portfolio)
    }

    return {'portfolio': portfolio, 'statistics': stats}
```

## Best Practices

1. **API Key Management** - Use environment variables, never hardcode
2. **Rate Limiting** - Implement exponential backoff for all APIs
3. **Caching** - Cache API responses to minimize redundant calls
4. **Error Handling** - Gracefully handle API errors and missing data
5. **Data Validation** - Validate input formats before API calls
6. **Combining APIs** - Use appropriate APIs together for comprehensive analysis
7. **Documentation** - Keep track of API versions and changes

## API Key Registration

All APIs require registration at:
**https://account.uspto.gov/api-manager/**

Single API key works across most USPTO APIs.

## Resources

- **Developer Portal**: https://developer.uspto.gov/
- **Open Data Portal**: https://data.uspto.gov/
- **API Catalog**: https://developer.uspto.gov/api-catalog
- **Swagger Docs**: Available for individual APIs

---

## Reference: Patentsearch_Api

# PatentSearch API Reference

## Overview

The PatentSearch API is USPTO's modern ElasticSearch-based patent search system that replaced the legacy PatentsView API in May 2025. It provides access to patent data through June 30, 2025, with regular updates.

**Base URL:** `https://search.patentsview.org/api/v1/`

## Authentication

All API requests require authentication using an API key in the request header:

```
X-Api-Key: YOUR_API_KEY
```

Register for an API key at: https://account.uspto.gov/api-manager/

## Rate Limits

- **45 requests per minute** per API key
- Exceeding rate limits results in HTTP 429 errors

## Available Endpoints

### Core Patent & Publication Endpoints

- **`/patent`** - General patent data (granted patents)
- **`/publication`** - Pregrant publication data
- **`/publication/rel_app_text`** - Related application data for publications

### Entity Endpoints

- **`/inventor`** - Inventor information with location and gender code fields
- **`/assignee`** - Assignee details with location identifiers
- **`/location`** - Geographic data including latitude/longitude coordinates
- **`/attorney`** - Legal representative information

### Classification Endpoints

- **`/cpc_subclass`** - Cooperative Patent Classification at subclass level
- **`/cpc_at_issue`** - CPC classification as of patent issue date
- **`/uspc`** - US Patent Classification data
- **`/wipo`** - World Intellectual Property Organization classifications
- **`/ipc`** - International Patent Classification

### Text Data Endpoints (Beta)

- **`/brief_summary_text`** - Patent brief summaries (granted and pre-grant)
- **`/claims`** - Patent claims text
- **`/drawing_description_text`** - Drawing descriptions
- **`/detail_description_text`** - Detailed description text

*Note: Text endpoints are in beta with data primarily from 2023 onward. Historical backfilling is in progress.*

### Supporting Endpoints

- **`/other_reference`** - Patent reference materials
- **`/related_document`** - Cross-references between patents

## Query Parameters

All endpoints support four main parameters:

### 1. Query String (`q`)

Filters data using JSON query objects. **Required parameter.**

**Query Operators:**

- **Equality**: `{"field": "value"}` or `{"field": {"_eq": "value"}}`
- **Not equal**: `{"field": {"_neq": "value"}}`
- **Comparison**: `_gt`, `_gte`, `_lt`, `_lte`
- **String matching**:
  - `_begins` - starts with
  - `_contains` - substring match
- **Full-text search** (recommended for text fields):
  - `_text_all` - all terms must match
  - `_text_any` - any term matches
  - `_text_phrase` - exact phrase match
- **Logical operators**: `_and`, `_or`, `_not`
- **Array matching**: Use arrays for OR conditions

**Examples:**

```json
// Simple equality
{"patent_number": "11234567"}

// Date range
{"patent_date": {"_gte": "2020-01-01", "_lte": "2020-12-31"}}

// Text search (preferred for text fields)
{"patent_abstract": {"_text_all": ["machine", "learning"]}}

// Inventor name
{"inventor_name": {"_text_phrase": "John Smith"}}

// Complex query with logical operators
{
  "_and": [
    {"patent_date": {"_gte": "2020-01-01"}},
    {"assignee_organization": {"_text_any": ["Google", "Alphabet"]}}
  ]
}

// Array for OR conditions
{"cpc_subclass_id": ["H04N", "H04L"]}
```

### 2. Field List (`f`)

Specifies which fields to return in the response. Optional - each endpoint has default fields.

**Format:** JSON array of field names

```json
["patent_number", "patent_title", "patent_date", "inventor_name"]
```

### 3. Sorting (`s`)

Orders results by specified fields. Optional.

**Format:** JSON array with field name and direction

```json
[{"patent_date": "desc"}]
```

### 4. Options (`o`)

Controls pagination and additional settings. Optional.

**Available options:**

- `page` - Page number (default: 1)
- `per_page` - Records per page (default: 100, max: 1,000)
- `pad_patent_id` - Pad patent IDs with leading zeros (default: false)
- `exclude_withdrawn` - Exclude withdrawn patents (default: true)

**Format:** JSON object

```json
{
  "page": 1,
  "per_page": 500,
  "exclude_withdrawn": false
}
```

## Response Format

All responses follow this structure:

```json
{
  "error": false,
  "count": 100,
  "total_hits": 5432,
  "patents": [...],
  // or "inventors": [...], "assignees": [...], etc.
}
```

- `error` - Boolean indicating if an error occurred
- `count` - Number of records in current response
- `total_hits` - Total number of matching records
- Endpoint-specific data array (e.g., `patents`, `inventors`)

## Complete Request Example

### Using curl

```bash
curl -X POST "https://search.patentsview.org/api/v1/patent" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "q": {
      "_and": [
        {"patent_date": {"_gte": "2024-01-01"}},
        {"patent_abstract": {"_text_all": ["artificial", "intelligence"]}}
      ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100}
  }'
```

### Using Python

```python
import requests

url = "https://search.patentsview.org/api/v1/patent"
headers = {
    "X-Api-Key": "YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"patent_abstract": {"_text_all": ["artificial", "intelligence"]}}
        ]
    },
    "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100}
}

response = requests.post(url, headers=headers, json=data)
results = response.json()
```

## Common Field Names

### Patent Endpoint Fields

- `patent_number` - Patent number
- `patent_title` - Title of the patent
- `patent_date` - Grant date
- `patent_abstract` - Abstract text
- `patent_type` - Type of patent
- `inventor_name` - Inventor names (array)
- `assignee_organization` - Assignee company names (array)
- `cpc_subclass_id` - CPC classification codes
- `uspc_class` - US classification codes
- `cited_patent_number` - Citations to other patents
- `citedby_patent_number` - Patents citing this patent

Refer to the full field dictionary at: https://search.patentsview.org/docs/

## Best Practices

1. **Use `_text*` operators for text fields** - More performant than `_contains` or `_begins`
2. **Request only needed fields** - Reduces response size and improves performance
3. **Implement pagination** - Handle large result sets efficiently
4. **Respect rate limits** - Implement backoff/retry logic for 429 errors
5. **Cache results** - Reduce redundant API calls
6. **Use date ranges** - Narrow searches to improve performance

## Error Handling

Common HTTP status codes:

- **200** - Success
- **400** - Bad request (invalid query syntax)
- **401** - Unauthorized (missing or invalid API key)
- **429** - Too many requests (rate limit exceeded)
- **500** - Server error

## Recent Updates (February 2025)

- Data updated through December 31, 2024
- New `pad_patent_id` option for formatting patent IDs
- New `exclude_withdrawn` option to show withdrawn patents
- Text endpoints continue beta backfilling

## Resources

- **Official Documentation**: https://search.patentsview.org/docs/
- **API Key Registration**: https://account.uspto.gov/api-manager/
- **Legacy API Notice**: The old PatentsView API was discontinued May 1, 2025

---

## Reference: Peds_Api

# Patent Examination Data System (PEDS) API Reference

## Overview

The Patent Examination Data System (PEDS) provides access to USPTO patent application and filing status records. It contains bibliographic data, published document information, and patent term extension data.

**Data Coverage:** 1981 to present (some data back to 1935)

**Base URL:** Access through USPTO Open Data Portal

## What PEDS Provides

PEDS gives comprehensive transaction history and status information for patent applications:

- **Bibliographic data** - Application numbers, filing dates, titles, inventors, assignees
- **Published documents** - Publication numbers and dates
- **Transaction history** - All examination events with dates, codes, and descriptions
- **Patent term adjustments** - PTA/PTE information
- **Application status** - Current status and status codes
- **File wrapper access** - Links to prosecution documents

## Key Features

1. **Transaction Activity** - Complete examination timeline with transaction dates, codes, and descriptions
2. **Status Information** - Current application status and status codes
3. **Bibliographic Updates** - Changes to inventors, assignees, titles over time
4. **Family Data** - Related applications and continuity data
5. **Office Action Tracking** - Mail dates and office action information

## Python Library: uspto-opendata-python

The recommended way to access PEDS is through the `uspto-opendata-python` library.

### Installation

```bash
pip install uspto-opendata-python
```

### Basic Usage

```python
from uspto.peds import PE DSClient

# Initialize client
client = PEDSClient()

# Search by application number
app_number = "16123456"
result = client.get_application(app_number)

# Access application data
print(f"Title: {result['title']}")
print(f"Filing Date: {result['filing_date']}")
print(f"Status: {result['status']}")

# Get transaction history
transactions = result['transactions']
for trans in transactions:
    print(f"{trans['date']}: {trans['code']} - {trans['description']}")
```

### Search Methods

```python
# By application number
client.get_application("16123456")

# By patent number
client.get_patent("11234567")

# By customer number (assignee)
client.search_by_customer_number("12345")

# Bulk retrieval
app_numbers = ["16123456", "16123457", "16123458"]
results = client.bulk_retrieve(app_numbers)
```

## Data Fields

### Bibliographic Fields

- `application_number` - Application number
- `filing_date` - Filing date
- `patent_number` - Patent number (if granted)
- `patent_issue_date` - Issue date (if granted)
- `title` - Application/patent title
- `inventors` - List of inventors
- `assignees` - List of assignees
- `app_type` - Application type (utility, design, plant, reissue)
- `app_status` - Current application status
- `app_status_date` - Status date

### Transaction Fields

- `transaction_date` - Date of transaction
- `transaction_code` - USPTO event code
- `transaction_description` - Description of event
- `mail_date` - Mail room date (for office actions)

### Patent Term Data

- `pta_pte_summary` - Patent term adjustment/extension summary
- `pta_pte_history` - History of term calculations

## Status Codes

Common application status codes:

- **Patented Case** - Patent has been granted
- **Abandoned** - Application is abandoned
- **Pending** - Application is under examination
- **Allowed** - Application has been allowed, awaiting issue
- **Final Rejection** - Final rejection issued
- **Non-Final Rejection** - Non-final rejection issued
- **Response Filed** - Applicant response filed

## Transaction Codes

Common transaction codes include:

- **CTNF** - Non-final rejection mailed
- **CTFR** - Final rejection mailed
- **AOPF** - Office action mailed
- **WRIT** - Response filed
- **NOA** - Notice of allowance mailed
- **ISS.FEE** - Issue fee payment
- **ABND** - Application abandoned

Full code list available in OCE Patent Examination Status/Event Codes API.

## Use Cases

### 1. Track Application Progress

Monitor pending applications for office actions and status changes.

```python
# Get current status
app = client.get_application("16123456")
print(f"Current status: {app['app_status']}")
print(f"Status date: {app['app_status_date']}")

# Check for recent office actions
recent_oas = [t for t in app['transactions']
              if t['code'] in ['CTNF', 'CTFR', 'AOPF']
              and t['date'] > '2024-01-01']
```

### 2. Portfolio Analysis

Analyze prosecution history across a portfolio.

```python
# Get all applications for an assignee
apps = client.search_by_customer_number("12345")

# Calculate average pendency
pendencies = []
for app in apps:
    if app['patent_issue_date']:
        filing = datetime.strptime(app['filing_date'], '%Y-%m-%d')
        issue = datetime.strptime(app['patent_issue_date'], '%Y-%m-%d')
        pendencies.append((issue - filing).days)

avg_pendency = sum(pendencies) / len(pendencies)
print(f"Average pendency: {avg_pendency} days")
```

### 3. Examine Rejection Patterns

Analyze types of rejections received.

```python
# Count rejection types
rejections = {}
for trans in app['transactions']:
    if 'rejection' in trans['description'].lower():
        code = trans['code']
        rejections[code] = rejections.get(code, 0) + 1
```

## Integration with Other APIs

PEDS data can be combined with other USPTO APIs:

- **Office Action Text API** - Retrieve full text of office actions using application number
- **Patent Assignment Search** - Find ownership changes
- **PTAB API** - Check for appeal proceedings

## Important Notes

1. **PAIR Bulk Data (PBD) is decommissioned** - Use PEDS instead
2. **Data updates** - PEDS is updated regularly but may have 1-2 day lag
3. **Application numbers** - Use standardized format (no slashes or spaces)
4. **Continuity data** - Parent/child applications tracked in transaction history

## Best Practices

1. **Batch requests** - Use bulk retrieval for multiple applications
2. **Cache data** - Avoid redundant API calls for same application
3. **Monitor updates** - Check for transaction updates regularly
4. **Handle missing data** - Not all fields populated for all applications
5. **Parse transaction codes** - Use code descriptions for user-friendly display

## Resources

- **Library Documentation**: https://docs.ip-tools.org/uspto-opendata-python/
- **PyPI Package**: https://pypi.org/project/uspto-opendata-python/
- **GitHub Repository**: https://github.com/ip-tools/uspto-opendata-python
- **USPTO PEDS Portal**: https://ped.uspto.gov/

---

## Reference: Trademark_Api

# USPTO Trademark APIs Reference

## Overview

USPTO provides two main APIs for trademark data:

1. **Trademark Status & Document Retrieval (TSDR)** - Retrieve trademark case status and documents
2. **Trademark Assignment Search** - Search trademark assignment records

## 1. Trademark Status & Document Retrieval (TSDR) API

### Overview

TSDR enables programmatic retrieval of trademark case status documents and information.

**API Version:** v1.0

**Base URL:** `https://tsdrapi.uspto.gov/ts/cd/`

### Authentication

Requires API key registration at: https://account.uspto.gov/api-manager/

Include API key in request header:
```
X-Api-Key: YOUR_API_KEY
```

### Endpoints

#### Get Trademark Status by Serial Number

```
GET /ts/cd/casedocs/sn{serial_number}/info.json
```

**Example:**
```bash
curl -H "X-Api-Key: YOUR_KEY" \
  "https://tsdrapi.uspto.gov/ts/cd/casedocs/sn87654321/info.json"
```

#### Get Trademark Status by Registration Number

```
GET /ts/cd/casedocs/rn{registration_number}/info.json
```

### Response Format

Returns JSON with comprehensive trademark information:

```json
{
  "TradeMarkAppln": {
    "ApplicationNumber": "87654321",
    "ApplicationDate": "2017-10-15",
    "RegistrationNumber": "5678901",
    "RegistrationDate": "2019-03-12",
    "MarkVerbalElementText": "EXAMPLE MARK",
    "MarkCurrentStatusExternalDescriptionText": "REGISTERED",
    "MarkCurrentStatusDate": "2019-03-12",
    "GoodsAndServices": [...],
    "Owners": [...],
    "Correspondents": [...]
  }
}
```

### Key Data Fields

- **Application Information:**
  - `ApplicationNumber` - Serial number
  - `ApplicationDate` - Filing date
  - `ApplicationType` - Type (TEAS Plus, TEAS Standard, etc.)

- **Registration Information:**
  - `RegistrationNumber` - Registration number (if registered)
  - `RegistrationDate` - Registration date

- **Mark Information:**
  - `MarkVerbalElementText` - Text of the mark
  - `MarkCurrentStatusExternalDescriptionText` - Current status
  - `MarkCurrentStatusDate` - Status date
  - `MarkDrawingCode` - Type of mark (words, design, etc.)

- **Classification:**
  - `GoodsAndServices` - Array of goods/services with classes

- **Owner Information:**
  - `Owners` - Array of trademark owners/applicants

- **Prosecution History:**
  - `ProsecutionHistoryEntry` - Array of events in prosecution

### Common Status Values

- **REGISTERED** - Mark is registered and active
- **PENDING** - Application under examination
- **ABANDONED** - Application/registration abandoned
- **CANCELLED** - Registration cancelled
- **SUSPENDED** - Examination suspended
- **PUBLISHED FOR OPPOSITION** - Published, in opposition period
- **REGISTERED AND RENEWED** - Registration renewed

### Python Example

```python
import requests

def get_trademark_status(serial_number, api_key):
    """Retrieve trademark status by serial number."""
    url = f"https://tsdrapi.uspto.gov/ts/cd/casedocs/sn{serial_number}/info.json"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage
data = get_trademark_status("87654321", "YOUR_API_KEY")
trademark = data['TradeMarkAppln']

print(f"Mark: {trademark['MarkVerbalElementText']}")
print(f"Status: {trademark['MarkCurrentStatusExternalDescriptionText']}")
print(f"Application Date: {trademark['ApplicationDate']}")
if 'RegistrationNumber' in trademark:
    print(f"Registration #: {trademark['RegistrationNumber']}")
```

## 2. Trademark Assignment Search API

### Overview

Retrieves trademark assignment records from the USPTO assignment database. Shows ownership transfers and security interests.

**API Version:** v1.4

**Base URL:** `https://assignment-api.uspto.gov/trademark/`

### Authentication

Requires API key in header:
```
X-Api-Key: YOUR_API_KEY
```

### Search Methods

#### By Registration Number

```
GET /v1.4/assignment/application/{registration_number}
```

#### By Serial Number

```
GET /v1.4/assignment/application/{serial_number}
```

#### By Assignee Name

```
POST /v1.4/assignment/search
```

**Request body:**
```json
{
  "criteria": {
    "assigneeName": "Company Name"
  }
}
```

### Response Format

Returns XML containing assignment records:

```xml
<assignments>
  <assignment>
    <reelFrame>12345/0678</reelFrame>
    <conveyanceText>ASSIGNMENT OF ASSIGNORS INTEREST</conveyanceText>
    <recordedDate>2020-01-15</recordedDate>
    <executionDate>2020-01-10</executionDate>
    <assignors>
      <assignor>
        <name>Original Owner LLC</name>
      </assignor>
    </assignors>
    <assignees>
      <assignee>
        <name>New Owner Corporation</name>
      </assignee>
    </assignees>
  </assignment>
</assignments>
```

### Key Fields

- `reelFrame` - USPTO reel and frame number
- `conveyanceText` - Type of transaction
- `recordedDate` - Date recorded at USPTO
- `executionDate` - Date document was executed
- `assignors` - Original owners
- `assignees` - New owners
- `propertyNumbers` - Affected serial/registration numbers

### Common Conveyance Types

- **ASSIGNMENT OF ASSIGNORS INTEREST** - Ownership transfer
- **SECURITY AGREEMENT** - Collateral/security interest
- **MERGER** - Corporate merger
- **CHANGE OF NAME** - Name change
- **ASSIGNMENT OF PARTIAL INTEREST** - Partial ownership transfer

### Python Example

```python
import requests
import xml.etree.ElementTree as ET

def search_trademark_assignments(registration_number, api_key):
    """Search assignments for a trademark registration."""
    url = f"https://assignment-api.uspto.gov/trademark/v1.4/assignment/application/{registration_number}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # Returns XML
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage
xml_data = search_trademark_assignments("5678901", "YOUR_API_KEY")
root = ET.fromstring(xml_data)

for assignment in root.findall('.//assignment'):
    reel_frame = assignment.find('reelFrame').text
    recorded_date = assignment.find('recordedDate').text
    conveyance = assignment.find('conveyanceText').text

    assignor = assignment.find('.//assignor/name').text
    assignee = assignment.find('.//assignee/name').text

    print(f"{recorded_date}: {assignor} -> {assignee}")
    print(f"  Type: {conveyance}")
    print(f"  Reel/Frame: {reel_frame}\n")
```

## Use Cases

### 1. Monitor Trademark Status

Check status of pending applications or registrations:

```python
def check_trademark_health(serial_number, api_key):
    """Check if trademark needs attention."""
    data = get_trademark_status(serial_number, api_key)
    tm = data['TradeMarkAppln']

    status = tm['MarkCurrentStatusExternalDescriptionText']
    alerts = []

    if 'ABANDON' in status:
        alerts.append("⚠️ ABANDONED")
    elif 'PUBLISHED' in status:
        alerts.append("📢 In opposition period")
    elif 'SUSPENDED' in status:
        alerts.append("⏸️ Examination suspended")
    elif 'REGISTERED' in status:
        alerts.append("✅ Active")

    return alerts
```

### 2. Track Ownership Changes

Monitor assignment records for ownership changes:

```python
def get_current_owner(registration_number, api_key):
    """Find current trademark owner from assignment records."""
    xml_data = search_trademark_assignments(registration_number, api_key)
    root = ET.fromstring(xml_data)

    assignments = []
    for assignment in root.findall('.//assignment'):
        date = assignment.find('recordedDate').text
        assignee = assignment.find('.//assignee/name').text
        assignments.append((date, assignee))

    # Most recent assignment
    if assignments:
        assignments.sort(reverse=True)
        return assignments[0][1]
    return None
```

### 3. Portfolio Management

Analyze trademark portfolio:

```python
def analyze_portfolio(serial_numbers, api_key):
    """Analyze status of multiple trademarks."""
    results = {
        'active': 0,
        'pending': 0,
        'abandoned': 0,
        'expired': 0
    }

    for sn in serial_numbers:
        data = get_trademark_status(sn, api_key)
        status = data['TradeMarkAppln']['MarkCurrentStatusExternalDescriptionText']

        if 'REGISTERED' in status:
            results['active'] += 1
        elif 'PENDING' in status or 'PUBLISHED' in status:
            results['pending'] += 1
        elif 'ABANDON' in status:
            results['abandoned'] += 1
        elif 'EXPIRED' in status or 'CANCELLED' in status:
            results['expired'] += 1

    return results
```

## Rate Limits and Best Practices

1. **Respect rate limits** - Implement retry logic with exponential backoff
2. **Cache responses** - Trademark data changes infrequently
3. **Batch processing** - Spread requests over time for large portfolios
4. **Error handling** - Handle missing data gracefully (not all marks have all fields)
5. **Data validation** - Verify serial/registration numbers before API calls

## Integration with Other Data

Combine trademark data with other sources:

- **TSDR + Assignment** - Current status + ownership history
- **Multiple marks** - Analyze related marks in a family
- **Patent data** - Cross-reference IP portfolio

## Resources

- **TSDR API**: https://developer.uspto.gov/api-catalog/tsdr-data-api
- **Assignment API**: https://developer.uspto.gov/api-catalog/trademark-assignment-search-data-api
- **API Key Registration**: https://account.uspto.gov/api-manager/
- **Trademark Search**: https://tmsearch.uspto.gov/
- **Swagger Documentation**: https://developer.uspto.gov/swagger/tsdr-api-v1
