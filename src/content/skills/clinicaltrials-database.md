---
title: "Clinicaltrials Database"
description: "Query ClinicalTrials.gov via API v2. Search trials by condition, drug, location, status, or phase. Retrieve trial details by NCT ID, export data, for clinical research and patient matching."
category: "research"
source: "community"
author: "Community"
tags: ["clinicaltrials", "database"]
date: 2026-03-20
---

# ClinicalTrials.gov Database

## Overview

ClinicalTrials.gov is a comprehensive registry of clinical studies conducted worldwide, maintained by the U.S. National Library of Medicine. Access API v2 to search for trials, retrieve detailed study information, filter by various criteria, and export data for analysis. The API is public (no authentication required) with rate limits of ~50 requests per minute, supporting JSON and CSV formats.

## When to Use This Skill

This skill should be used when working with clinical trial data in scenarios such as:

- **Patient matching** - Finding recruiting trials for specific conditions or patient populations
- **Research analysis** - Analyzing clinical trial trends, outcomes, or study designs
- **Drug/intervention research** - Identifying trials testing specific drugs or interventions
- **Geographic searches** - Locating trials in specific locations or regions
- **Sponsor/organization tracking** - Finding trials conducted by specific institutions
- **Data export** - Extracting clinical trial data for further analysis or reporting
- **Trial monitoring** - Tracking status updates or results for specific trials
- **Eligibility screening** - Reviewing inclusion/exclusion criteria for trials

## Quick Start

### Basic Search Query

Search for clinical trials using the helper script:

```bash
cd scientific-databases/clinicaltrials-database/scripts
python3 query_clinicaltrials.py
```

Or use Python directly with the `requests` library:

```python
import requests

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 10
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} trials")
```

### Retrieve Specific Trial

Get detailed information about a trial using its NCT ID:

```python
import requests

nct_id = "NCT04852770"
url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"

response = requests.get(url)
study = response.json()

# Access specific modules
title = study['protocolSection']['identificationModule']['briefTitle']
status = study['protocolSection']['statusModule']['overallStatus']
```

## Core Capabilities

### 1. Search by Condition/Disease

Find trials studying specific medical conditions or diseases using the `query.cond` parameter.

**Example: Find recruiting diabetes trials**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="type 2 diabetes",
    status="RECRUITING",
    page_size=20,
    sort="LastUpdatePostDate:desc"
)

print(f"Found {results['totalCount']} recruiting diabetes trials")
for study in results['studies']:
    protocol = study['protocolSection']
    nct_id = protocol['identificationModule']['nctId']
    title = protocol['identificationModule']['briefTitle']
    print(f"{nct_id}: {title}")
```

**Common use cases:**
- Finding trials for rare diseases
- Identifying trials for comorbid conditions
- Tracking trial availability for specific diagnoses

### 2. Search by Intervention/Drug

Search for trials testing specific interventions, drugs, devices, or procedures using the `query.intr` parameter.

**Example: Find Phase 3 trials testing Pembrolizumab**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    intervention="Pembrolizumab",
    status=["RECRUITING", "ACTIVE_NOT_RECRUITING"],
    page_size=50
)

# Filter by phase in results
phase3_trials = [
    study for study in results['studies']
    if 'PHASE3' in study['protocolSection'].get('designModule', {}).get('phases', [])
]
```

**Common use cases:**
- Drug development tracking
- Competitive intelligence for pharmaceutical companies
- Treatment option research for clinicians

### 3. Geographic Search

Find trials in specific locations using the `query.locn` parameter.

**Example: Find cancer trials in New York**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="cancer",
    location="New York",
    status="RECRUITING",
    page_size=100
)

# Extract location details
for study in results['studies']:
    locations_module = study['protocolSection'].get('contactsLocationsModule', {})
    locations = locations_module.get('locations', [])
    for loc in locations:
        if 'New York' in loc.get('city', ''):
            print(f"{loc['facility']}: {loc['city']}, {loc.get('state', '')}")
```

**Common use cases:**
- Patient referrals to local trials
- Geographic trial distribution analysis
- Site selection for new trials

### 4. Search by Sponsor/Organization

Find trials conducted by specific organizations using the `query.spons` parameter.

**Example: Find trials sponsored by NCI**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    sponsor="National Cancer Institute",
    page_size=100
)

# Extract sponsor information
for study in results['studies']:
    sponsor_module = study['protocolSection']['sponsorCollaboratorsModule']
    lead_sponsor = sponsor_module['leadSponsor']['name']
    collaborators = sponsor_module.get('collaborators', [])
    print(f"Lead: {lead_sponsor}")
    if collaborators:
        print(f"  Collaborators: {', '.join([c['name'] for c in collaborators])}")
```

**Common use cases:**
- Tracking institutional research portfolios
- Analyzing funding organization priorities
- Identifying collaboration opportunities

### 5. Filter by Study Status

Filter trials by recruitment or completion status using the `filter.overallStatus` parameter.

**Valid status values:**
- `RECRUITING` - Currently recruiting participants
- `NOT_YET_RECRUITING` - Not yet open for recruitment
- `ENROLLING_BY_INVITATION` - Only enrolling by invitation
- `ACTIVE_NOT_RECRUITING` - Active but no longer recruiting
- `SUSPENDED` - Temporarily halted
- `TERMINATED` - Stopped prematurely
- `COMPLETED` - Study has concluded
- `WITHDRAWN` - Withdrawn prior to enrollment

**Example: Find recently completed trials with results**

```python
from scripts.query_clinicaltrials import search_studies

results = search_studies(
    condition="alzheimer disease",
    status="COMPLETED",
    sort="LastUpdatePostDate:desc",
    page_size=50
)

# Filter for trials with results
trials_with_results = [
    study for study in results['studies']
    if study.get('hasResults', False)
]

print(f"Found {len(trials_with_results)} completed trials with results")
```

### 6. Retrieve Detailed Study Information

Get comprehensive information about specific trials including eligibility criteria, outcomes, contacts, and locations.

**Example: Extract eligibility criteria**

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
eligibility = study['protocolSection']['eligibilityModule']

print(f"Eligible Ages: {eligibility.get('minimumAge')} - {eligibility.get('maximumAge')}")
print(f"Eligible Sex: {eligibility.get('sex')}")
print(f"\nInclusion Criteria:")
print(eligibility.get('eligibilityCriteria'))
```

**Example: Extract contact information**

```python
from scripts.query_clinicaltrials import get_study_details

study = get_study_details("NCT04852770")
contacts_module = study['protocolSection']['contactsLocationsModule']

# Overall contacts
if 'centralContacts' in contacts_module:
    for contact in contacts_module['centralContacts']:
        print(f"Contact: {contact.get('name')}")
        print(f"Phone: {contact.get('phone')}")
        print(f"Email: {contact.get('email')}")

# Study locations
if 'locations' in contacts_module:
    for location in contacts_module['locations']:
        print(f"\nFacility: {location.get('facility')}")
        print(f"City: {location.get('city')}, {location.get('state')}")
        if location.get('status'):
            print(f"Status: {location['status']}")
```

### 7. Pagination and Bulk Data Retrieval

Handle large result sets efficiently using pagination.

**Example: Retrieve all matching trials**

```python
from scripts.query_clinicaltrials import search_with_all_results

# Get all trials (automatically handles pagination)
all_trials = search_with_all_results(
    condition="rare disease",
    status="RECRUITING"
)

print(f"Retrieved {len(all_trials)} total trials")
```

**Example: Manual pagination with control**

```python
from scripts.query_clinicaltrials import search_studies

all_studies = []
page_token = None
max_pages = 10  # Limit to avoid excessive requests

for page in range(max_pages):
    results = search_studies(
        condition="cancer",
        page_size=1000,  # Max page size
        page_token=page_token
    )

    all_studies.extend(results['studies'])

    # Check for next page
    page_token = results.get('pageToken')
    if not page_token:
        break

print(f"Retrieved {len(all_studies)} studies across {page + 1} pages")
```

### 8. Data Export to CSV

Export trial data to CSV format for analysis in spreadsheet software or data analysis tools.

**Example: Export to CSV file**

```python
from scripts.query_clinicaltrials import search_studies

# Request CSV format
results = search_studies(
    condition="heart disease",
    status="RECRUITING",
    format="csv",
    page_size=1000
)

# Save to file
with open("heart_disease_trials.csv", "w") as f:
    f.write(results)

print("Data exported to heart_disease_trials.csv")
```

**Note:** CSV format returns a string instead of JSON dictionary.

### 9. Extract and Summarize Study Information

Extract key information for quick overview or reporting.

**Example: Create trial summary**

```python
from scripts.query_clinicaltrials import get_study_details, extract_study_summary

# Get details and extract summary
study = get_study_details("NCT04852770")
summary = extract_study_summary(study)

print(f"NCT ID: {summary['nct_id']}")
print(f"Title: {summary['title']}")
print(f"Status: {summary['status']}")
print(f"Phase: {', '.join(summary['phase'])}")
print(f"Enrollment: {summary['enrollment']}")
print(f"Last Update: {summary['last_update']}")
print(f"\nBrief Summary:\n{summary['brief_summary']}")
```

### 10. Combined Query Strategies

Combine multiple filters for targeted searches.

**Example: Multi-criteria search**

```python
from scripts.query_clinicaltrials import search_studies

# Find Phase 2/3 immunotherapy trials for lung cancer in California
results = search_studies(
    condition="lung cancer",
    intervention="immunotherapy",
    location="California",
    status=["RECRUITING", "NOT_YET_RECRUITING"],
    page_size=100
)

# Further filter by phase
phase2_3_trials = [
    study for study in results['studies']
    if any(phase in ['PHASE2', 'PHASE3']
           for phase in study['protocolSection'].get('designModule', {}).get('phases', []))
]

print(f"Found {len(phase2_3_trials)} Phase 2/3 immunotherapy trials")
```

## Resources

### scripts/query_clinicaltrials.py

Comprehensive Python script providing helper functions for common query patterns:

- `search_studies()` - Search for trials with various filters
- `get_study_details()` - Retrieve full information for a specific trial
- `search_with_all_results()` - Automatically paginate through all results
- `extract_study_summary()` - Extract key information for quick overview

Run the script directly for example usage:

```bash
python3 scripts/query_clinicaltrials.py
```

### references/api_reference.md

Detailed API documentation including:

- Complete endpoint specifications
- All query parameters and valid values
- Response data structure and modules
- Common use cases with code examples
- Error handling and best practices
- Data standards (ISO 8601 dates, CommonMark markdown)

Load this reference when working with unfamiliar API features or troubleshooting issues.

## Best Practices

### Rate Limit Management

The API has a rate limit of approximately 50 requests per minute. For bulk data retrieval:

1. Use maximum page size (1000) to minimize requests
2. Implement exponential backoff on rate limit errors (429 status)
3. Add delays between requests for large-scale data collection

```python
import time
import requests

def search_with_rate_limit(params):
    try:
        response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limited. Waiting 60 seconds...")
            time.sleep(60)
            return search_with_rate_limit(params)  # Retry
        raise
```

### Data Structure Navigation

The API response has a nested structure. Key paths to common information:

- **NCT ID**: `study['protocolSection']['identificationModule']['nctId']`
- **Title**: `study['protocolSection']['identificationModule']['briefTitle']`
- **Status**: `study['protocolSection']['statusModule']['overallStatus']`
- **Phase**: `study['protocolSection']['designModule']['phases']`
- **Eligibility**: `study['protocolSection']['eligibilityModule']`
- **Locations**: `study['protocolSection']['contactsLocationsModule']['locations']`
- **Interventions**: `study['protocolSection']['armsInterventionsModule']['interventions']`

### Error Handling

Always implement proper error handling for network requests:

```python
import requests

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"JSON decode error: {e}")
```

### Handling Missing Data

Not all trials have complete information. Always check for field existence:

```python
# Safe navigation with .get()
phases = study['protocolSection'].get('designModule', {}).get('phases', [])
enrollment = study['protocolSection'].get('designModule', {}).get('enrollmentInfo', {}).get('count', 'N/A')

# Check before accessing
if 'resultsSection' in study:
    # Process results
    pass
```

## Technical Specifications

- **Base URL**: `https://clinicaltrials.gov/api/v2`
- **Authentication**: Not required (public API)
- **Rate Limit**: ~50 requests/minute per IP
- **Response Formats**: JSON (default), CSV
- **Max Page Size**: 1000 studies per request
- **Date Format**: ISO 8601
- **Text Format**: CommonMark Markdown for rich text fields
- **API Version**: 2.0 (released March 2024)
- **API Specification**: OpenAPI 3.0

For complete technical details, see `references/api_reference.md`.

---

## Reference: Api_Reference

# ClinicalTrials.gov API v2 Reference Documentation

## Overview

The ClinicalTrials.gov API v2 is a modern REST API that provides programmatic access to the ClinicalTrials.gov database, which contains information about clinical studies conducted around the world. The API follows the OpenAPI Specification 3.0 and provides both JSON and CSV response formats.

**Base URL:** `https://clinicaltrials.gov/api/v2`

**API Version:** 2.0 (released March 2024, replacing the classic API)

## Authentication & Rate Limits

- **Authentication:** Not required (public API)
- **Rate Limit:** Approximately 50 requests per minute per IP address
- **Response Formats:** JSON (default) or CSV
- **Standards:** Uses ISO 8601 for dates, CommonMark Markdown for rich text

## Core Endpoints

### 1. Search Studies

**Endpoint:** `GET /api/v2/studies`

Search for clinical trials using various query parameters and filters.

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query.cond` | string | Disease or condition search | `lung cancer`, `diabetes` |
| `query.intr` | string | Treatment or intervention search | `Pembrolizumab`, `exercise` |
| `query.locn` | string | Geographic location filtering | `New York`, `California, USA` |
| `query.spons` | string | Sponsor or collaborator name | `National Cancer Institute` |
| `query.term` | string | General full-text search | `breast cancer treatment` |
| `filter.overallStatus` | string | Status-based filtering (comma-separated) | `RECRUITING,NOT_YET_RECRUITING` |
| `filter.ids` | string | NCT ID intersection filtering (comma-separated) | `NCT04852770,NCT01728545` |
| `filter.phase` | string | Study phase filtering | `PHASE1,PHASE2` |
| `sort` | string | Result ordering | `LastUpdatePostDate:desc` |
| `pageSize` | integer | Results per page (max 1000) | `100` |
| `pageToken` | string | Pagination token from previous response | `<token>` |
| `format` | string | Response format (`json` or `csv`) | `json` |

**Valid Status Values:**
- `RECRUITING` - Currently recruiting participants
- `NOT_YET_RECRUITING` - Not yet open for recruitment
- `ENROLLING_BY_INVITATION` - Only enrolling by invitation
- `ACTIVE_NOT_RECRUITING` - Active but no longer recruiting
- `SUSPENDED` - Temporarily halted
- `TERMINATED` - Stopped prematurely
- `COMPLETED` - Study has concluded
- `WITHDRAWN` - Withdrawn prior to enrollment

**Valid Phase Values:**
- `EARLY_PHASE1` - Early Phase 1 (formerly Phase 0)
- `PHASE1` - Phase 1
- `PHASE2` - Phase 2
- `PHASE3` - Phase 3
- `PHASE4` - Phase 4
- `NA` - Not Applicable

**Sort Options:**
- `LastUpdatePostDate:asc` / `LastUpdatePostDate:desc` - Sort by last update date
- `EnrollmentCount:asc` / `EnrollmentCount:desc` - Sort by enrollment count
- `StartDate:asc` / `StartDate:desc` - Sort by start date
- `StudyFirstPostDate:asc` / `StudyFirstPostDate:desc` - Sort by first posted date

**Example Request:**
```bash
curl "https://clinicaltrials.gov/api/v2/studies?query.cond=lung+cancer&filter.overallStatus=RECRUITING&pageSize=10&format=json"
```

**Example Response Structure:**
```json
{
  "studies": [
    {
      "protocolSection": { ... },
      "derivedSection": { ... },
      "hasResults": false
    }
  ],
  "totalCount": 1234,
  "pageToken": "next_page_token_here"
}
```

### 2. Get Study Details

**Endpoint:** `GET /api/v2/studies/{NCT_ID}`

Retrieve comprehensive information about a specific clinical trial.

**Path Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `NCT_ID` | string | The unique NCT identifier | `NCT04852770` |

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `format` | string | Response format (`json` or `csv`) | `json` |

**Example Request:**
```bash
curl "https://clinicaltrials.gov/api/v2/studies/NCT04852770?format=json"
```

## Response Data Structure

The API returns study data organized into hierarchical modules. Key sections include:

### protocolSection

Core study information and design:

- **identificationModule** - NCT ID, official title, brief title, organization
- **statusModule** - Overall status, start date, completion date, last update
- **sponsorCollaboratorsModule** - Lead sponsor, collaborators, responsible party
- **descriptionModule** - Brief summary, detailed description
- **conditionsModule** - Conditions being studied
- **designModule** - Study type, phases, enrollment info, design details
- **armsInterventionsModule** - Study arms and interventions
- **outcomesModule** - Primary and secondary outcomes
- **eligibilityModule** - Inclusion/exclusion criteria, age/sex requirements
- **contactsLocationsModule** - Overall contacts, study locations
- **referencesModule** - References, links, citations

### derivedSection

Computed/derived information:

- **miscInfoModule** - Version holder, removed countries
- **conditionBrowseModule** - Condition mesh terms
- **interventionBrowseModule** - Intervention mesh terms

### resultsSection

Study results (when available):

- **participantFlowModule** - Participant flow through study
- **baselineCharacteristicsModule** - Baseline participant characteristics
- **outcomeMeasuresModule** - Outcome measure results
- **adverseEventsModule** - Adverse events data

### hasResults

Boolean indicating if results are available for the study.

## Common Use Cases

### Use Case 1: Find Recruiting Trials for a Condition

Search for trials currently recruiting participants for a specific disease or condition:

```python
import requests

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.cond": "breast cancer",
    "filter.overallStatus": "RECRUITING",
    "pageSize": 20,
    "sort": "LastUpdatePostDate:desc"
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['totalCount']} recruiting breast cancer trials")
for study in data['studies']:
    nct_id = study['protocolSection']['identificationModule']['nctId']
    title = study['protocolSection']['identificationModule']['briefTitle']
    print(f"{nct_id}: {title}")
```

### Use Case 2: Search by Intervention/Drug

Find trials testing a specific intervention or drug:

```python
params = {
    "query.intr": "Pembrolizumab",
    "filter.phase": "PHASE3",
    "pageSize": 50
}

response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
```

### Use Case 3: Geographic Search

Find trials in a specific location:

```python
params = {
    "query.cond": "diabetes",
    "query.locn": "Boston, Massachusetts",
    "filter.overallStatus": "RECRUITING"
}

response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
```

### Use Case 4: Retrieve Full Study Details

Get comprehensive information about a specific trial:

```python
nct_id = "NCT04852770"
url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"

response = requests.get(url)
study = response.json()

# Access specific information
eligibility = study['protocolSection']['eligibilityModule']
contacts = study['protocolSection']['contactsLocationsModule']
```

### Use Case 5: Pagination Through Results

Handle large result sets with pagination:

```python
all_studies = []
page_token = None

while True:
    params = {
        "query.cond": "cancer",
        "pageSize": 1000
    }
    if page_token:
        params['pageToken'] = page_token

    response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
    data = response.json()

    all_studies.extend(data['studies'])

    # Check if there are more pages
    page_token = data.get('pageToken')
    if not page_token:
        break

print(f"Retrieved {len(all_studies)} total studies")
```

### Use Case 6: Export to CSV

Retrieve data in CSV format for analysis:

```python
params = {
    "query.cond": "alzheimer",
    "format": "csv",
    "pageSize": 100
}

response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=params)
csv_data = response.text

# Save to file
with open("alzheimer_trials.csv", "w") as f:
    f.write(csv_data)
```

## Error Handling

### Common HTTP Status Codes

- **200 OK** - Request succeeded
- **400 Bad Request** - Invalid parameters or malformed request
- **404 Not Found** - NCT ID not found
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error

### Example Error Response

```json
{
  "error": {
    "code": 400,
    "message": "Invalid parameter: filter.overallStatus must be one of: RECRUITING, NOT_YET_RECRUITING, ..."
  }
}
```

### Best Practices for Error Handling

```python
import requests
import time

def search_with_retry(params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(
                "https://clinicaltrials.gov/api/v2/studies",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # Rate limited - wait and retry
                wait_time = 60  # Wait 1 minute
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

    raise Exception("Max retries exceeded")
```

## Data Standards

### Date Format

All dates use ISO 8601 format with structured objects:

```json
"lastUpdatePostDateStruct": {
  "date": "2024-03-15",
  "type": "ACTUAL"
}
```

### Rich Text

Descriptive text fields use CommonMark Markdown format, allowing for structured formatting:

```json
"briefSummary": "This is a **Phase 2** study evaluating:\n\n- Safety\n- Efficacy\n- Tolerability"
```

### Enumerated Values

Many fields use standardized enumerated values (e.g., study status, phase) rather than free-form text, improving data consistency and query reliability.

## Migration from Classic API

The API v2 replaced the classic API (retired June 2024). Key improvements:

1. **Structured Data** - Enumerated values instead of free text
2. **Modern Standards** - ISO 8601 dates, CommonMark markdown
3. **Better Performance** - Optimized queries and pagination
4. **OpenAPI Spec** - Standard API specification format
5. **Consistent Fields** - Number fields properly typed

For detailed migration guidance, see: https://clinicaltrials.gov/data-api/about-api/api-migration
