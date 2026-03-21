---
title: "Pubmed Database"
description: "Direct REST API access to PubMed. Advanced Boolean/MeSH queries, E-utilities API, batch processing, citation management. For Python workflows, prefer biopython (Bio.Entrez). Use this for direct HTTP/REST work or custom API implementations."
category: "research"
source: "community"
author: "Community"
tags: ["pubmed", "database"]
date: 2026-03-20
---

# PubMed Database

## Overview

PubMed is the U.S. National Library of Medicine's comprehensive database providing free access to MEDLINE and life sciences literature. Construct advanced queries with Boolean operators, MeSH terms, and field tags, access data programmatically via E-utilities API for systematic reviews and literature analysis.

## When to Use This Skill

This skill should be used when:
- Searching for biomedical or life sciences research articles
- Constructing complex search queries with Boolean operators, field tags, or MeSH terms
- Conducting systematic literature reviews or meta-analyses
- Accessing PubMed data programmatically via the E-utilities API
- Finding articles by specific criteria (author, journal, publication date, article type)
- Retrieving citation information, abstracts, or full-text articles
- Working with PMIDs (PubMed IDs) or DOIs
- Creating automated workflows for literature monitoring or data extraction

## Core Capabilities

### 1. Advanced Search Query Construction

Construct sophisticated PubMed queries using Boolean operators, field tags, and specialized syntax.

**Basic Search Strategies**:
- Combine concepts with Boolean operators (AND, OR, NOT)
- Use field tags to limit searches to specific record parts
- Employ phrase searching with double quotes for exact matches
- Apply wildcards for term variations
- Use proximity searching for terms within specified distances

**Example Queries**:
```
# Recent systematic reviews on diabetes treatment
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Clinical trials comparing two drugs
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Author-specific research
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**When to consult search_syntax.md**:
- Need comprehensive list of available field tags
- Require detailed explanation of search operators
- Constructing complex proximity searches
- Understanding automatic term mapping behavior
- Need specific syntax for date ranges, wildcards, or special characters

Grep pattern for field tags: `\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`

### 2. MeSH Terms and Controlled Vocabulary

Use Medical Subject Headings (MeSH) for precise, consistent searching across the biomedical literature.

**MeSH Searching**:
- [mh] tag searches MeSH terms with automatic inclusion of narrower terms
- [majr] tag limits to articles where the topic is the main focus
- Combine MeSH terms with subheadings for specificity (e.g., diabetes mellitus/therapy[mh])

**Common MeSH Subheadings**:
- /diagnosis - Diagnostic methods
- /drug therapy - Pharmaceutical treatment
- /epidemiology - Disease patterns and prevalence
- /etiology - Disease causes
- /prevention & control - Preventive measures
- /therapy - Treatment approaches

**Example**:
```
# Diabetes therapy with specific focus
diabetes mellitus, type 2[mh]/drug therapy AND cardiovascular diseases[mh]/prevention & control
```

### 3. Article Type and Publication Filtering

Filter results by publication type, date, text availability, and other attributes.

**Publication Types** (use [pt] field tag):
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Guideline

**Date Filtering**:
- Single year: `2024[dp]`
- Date range: `2020:2024[dp]`
- Specific date: `2024/03/15[dp]`

**Text Availability**:
- Free full text: Add `AND free full text[sb]` to query
- Has abstract: Add `AND hasabstract[text]` to query

**Example**:
```
# Recent free full-text RCTs on hypertension
hypertension[mh] AND randomized controlled trial[pt] AND 2023:2024[dp] AND free full text[sb]
```

### 4. Programmatic Access via E-utilities API

Access PubMed data programmatically using the NCBI E-utilities REST API for automation and bulk operations.

**Core API Endpoints**:
1. **ESearch** - Search database and retrieve PMIDs
2. **EFetch** - Download full records in various formats
3. **ESummary** - Get document summaries
4. **EPost** - Upload UIDs for batch processing
5. **ELink** - Find related articles and linked data

**Basic Workflow**:
```python
import requests

# Step 1: Search for articles
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # Optional but recommended
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# Step 2: Fetch article details
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

**Rate Limits**:
- Without API key: 3 requests/second
- With API key: 10 requests/second
- Always include User-Agent header

**Best Practices**:
- Use history server (usehistory=y) for large result sets
- Implement batch operations via EPost for multiple UIDs
- Cache results locally to minimize redundant calls
- Respect rate limits to avoid service disruption

**When to consult api_reference.md**:
- Need detailed endpoint documentation
- Require parameter specifications for each E-utility
- Constructing batch operations or history server workflows
- Understanding response formats (XML, JSON, text)
- Troubleshooting API errors or rate limit issues

Grep pattern for API endpoints: `esearch|efetch|esummary|epost|elink|einfo`

### 5. Citation Matching and Article Retrieval

Find articles using partial citation information or specific identifiers.

**By Identifier**:
```
# By PMID
12345678[pmid]

# By DOI
10.1056/NEJMoa123456[doi]

# By PMC ID
PMC123456[pmc]
```

**Citation Matching** (via ECitMatch API):
Use journal name, year, volume, page, and author to find PMIDs:
```
Format: journal|year|volume|page|author|key|
Example: Science|2008|320|5880|1185|key1|
```

**By Author and Metadata**:
```
# First author with year and topic
smith ja[1au] AND 2023[dp] AND cancer[tiab]

# Journal, volume, and page
nature[ta] AND 2024[dp] AND 456[vi] AND 123-130[pg]
```

### 6. Systematic Literature Reviews

Conduct comprehensive literature searches for systematic reviews and meta-analyses.

**PICO Framework** (Population, Intervention, Comparison, Outcome):
Structure clinical research questions systematically:
```
# Example: Diabetes treatment effectiveness
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**Comprehensive Search Strategy**:
```
# Include multiple synonyms and MeSH terms
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND
english[la]
```

**Search Refinement**:
1. Start broad, review results
2. Add specificity with field tags
3. Apply date and publication type filters
4. Use Advanced Search to view query translation
5. Combine search history for complex queries

**When to consult common_queries.md**:
- Need example queries for specific disease types or research areas
- Require templates for different study designs
- Looking for population-specific query patterns (pediatric, geriatric, etc.)
- Constructing methodology-specific searches
- Need quality filters or best practice patterns

Grep pattern for query examples: `diabetes|cancer|cardiovascular|clinical trial|systematic review`

### 7. Search History and Saved Searches

Use PubMed's search history and My NCBI features for efficient research workflows.

**Search History** (via Advanced Search):
- Maintains up to 100 searches
- Expires after 8 hours of inactivity
- Combine previous searches using # references
- Preview result counts before executing

**Example**:
```
#1: diabetes mellitus[mh]
#2: cardiovascular diseases[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

**My NCBI Features**:
- Save searches indefinitely
- Set up email alerts for new matching articles
- Create collections of saved articles
- Organize research by project or topic

**RSS Feeds**:
Create RSS feeds for any search to monitor new publications in your area of interest.

### 8. Related Articles and Citation Discovery

Find related research and explore citation networks.

**Similar Articles Feature**:
Every PubMed article includes pre-calculated related articles based on:
- Title and abstract similarity
- MeSH term overlap
- Weighted algorithmic matching

**ELink for Related Data**:
```
# Find related articles programmatically
elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor
```

**Citation Links**:
- LinkOut to full text from publishers
- Links to PubMed Central free articles
- Connections to related NCBI databases (GenBank, ClinicalTrials.gov, etc.)

### 9. Export and Citation Management

Export search results in various formats for citation management and further analysis.

**Export Formats**:
- .nbib files for reference managers (Zotero, Mendeley, EndNote)
- AMA, MLA, APA, NLM citation styles
- CSV for data analysis
- XML for programmatic processing

**Clipboard and Collections**:
- Clipboard: Temporary storage for up to 500 items (8-hour expiration)
- Collections: Permanent storage via My NCBI account

**Batch Export via API**:
```python
# Export citations in MEDLINE format
efetch.fcgi?db=pubmed&id=PMID1,PMID2&rettype=medline&retmode=text
```

## Working with Reference Files

This skill includes three comprehensive reference files in the `references/` directory:

### references/api_reference.md
Complete E-utilities API documentation including all nine endpoints, parameters, response formats, and best practices. Consult when:
- Implementing programmatic PubMed access
- Constructing API requests
- Understanding rate limits and authentication
- Working with large datasets via history server
- Troubleshooting API errors

### references/search_syntax.md
Detailed guide to PubMed search syntax including field tags, Boolean operators, wildcards, and special characters. Consult when:
- Constructing complex search queries
- Understanding automatic term mapping
- Using advanced search features (proximity, wildcards)
- Applying filters and limits
- Troubleshooting unexpected search results

### references/common_queries.md
Extensive collection of example queries for various research scenarios, disease types, and methodologies. Consult when:
- Starting a new literature search
- Need templates for specific research areas
- Looking for best practice query patterns
- Conducting systematic reviews
- Searching for specific study designs or populations

**Reference Loading Strategy**:
Load reference files into context as needed based on the specific task. For brief queries or basic searches, the information in this SKILL.md may be sufficient. For complex operations, consult the appropriate reference file.

## Common Workflows

### Workflow 1: Basic Literature Search

1. Identify key concepts and synonyms
2. Construct query with Boolean operators and field tags
3. Review initial results and refine query
4. Apply filters (date, article type, language)
5. Export results for analysis

### Workflow 2: Systematic Review Search

1. Define research question using PICO framework
2. Identify all relevant MeSH terms and synonyms
3. Construct comprehensive search strategy
4. Search multiple databases (include PubMed)
5. Document search strategy and date
6. Export results for screening and review

### Workflow 3: Programmatic Data Extraction

1. Design search query and test in web interface
2. Implement search using ESearch API
3. Use history server for large result sets
4. Retrieve detailed records with EFetch
5. Parse XML/JSON responses
6. Store data locally with caching
7. Implement rate limiting and error handling

### Workflow 4: Citation Discovery

1. Start with known relevant article
2. Use Similar Articles to find related work
3. Check citing articles (when available)
4. Explore MeSH terms from relevant articles
5. Construct new searches based on discoveries
6. Use ELink to find related database entries

### Workflow 5: Ongoing Literature Monitoring

1. Construct comprehensive search query
2. Test and refine query for precision
3. Save search to My NCBI account
4. Set up email alerts for new matches
5. Create RSS feed for feed reader monitoring
6. Review new articles regularly

## Tips and Best Practices

### Search Strategy
- Start broad, then narrow with field tags and filters
- Include synonyms and MeSH terms for comprehensive coverage
- Use quotation marks for exact phrases
- Check Search Details in Advanced Search to verify query translation
- Combine multiple searches using search history

### API Usage
- Obtain API key for higher rate limits (10 req/sec vs 3 req/sec)
- Use history server for result sets > 500 articles
- Implement exponential backoff for rate limit handling
- Cache results locally to minimize redundant requests
- Always include descriptive User-Agent header

### Quality Filtering
- Prefer systematic reviews and meta-analyses for synthesized evidence
- Use publication type filters to find specific study designs
- Filter by date for most recent research
- Apply language filters as appropriate
- Use free full text filter for immediate access

### Citation Management
- Export early and often to avoid losing search results
- Use .nbib format for compatibility with most reference managers
- Create My NCBI account for permanent collections
- Document search strategies for reproducibility
- Use Collections to organize research by project

## Limitations and Considerations

### Database Coverage
- Primarily biomedical and life sciences literature
- Pre-1975 articles often lack abstracts
- Full author names available from 2002 forward
- Non-English abstracts available but may default to English display

### Search Limitations
- Display limited to 10,000 results maximum
- Search history expires after 8 hours of inactivity
- Clipboard holds max 500 items with 8-hour expiration
- Automatic term mapping may produce unexpected results

### API Considerations
- Rate limits apply (3-10 requests/second)
- Large queries may time out (use history server)
- XML parsing required for detailed data extraction
- API key recommended for production use

### Access Limitations
- PubMed provides citations and abstracts (not always full text)
- Full text access depends on publisher, institutional access, or open access status
- LinkOut availability varies by journal and institution
- Some content requires subscription or payment

## Support Resources

- **PubMed Help**: https://pubmed.ncbi.nlm.nih.gov/help/
- **E-utilities Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NLM Help Desk**: 1-888-FIND-NLM (1-888-346-3656)
- **Technical Support**: vog.hin.mln.ibcn@seitilitue
- **Mailing List**: utilities-announce@ncbi.nlm.nih.gov

---

## Reference: Api_Reference

# PubMed E-utilities API Reference

## Overview

The NCBI E-utilities provide programmatic access to PubMed and other Entrez databases through a REST API. The base URL for all E-utilities is:

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## API Key Requirements

As of December 1, 2018, NCBI enforces API key usage for E-utility calls. API keys increase rate limits from 3 requests/second to 10 requests/second. To obtain an API key, register for an NCBI account and generate a key from your account settings.

Include the API key in requests using the `&api_key` parameter:
```
esearch.fcgi?db=pubmed&term=cancer&api_key=YOUR_API_KEY
```

## Rate Limits

- **Without API key**: 3 requests per second
- **With API key**: 10 requests per second
- Always include a User-Agent header in requests

## Core E-utility Tools

### 1. ESearch - Query Databases

**Endpoint**: `esearch.fcgi`

**Purpose**: Search an Entrez database and retrieve a list of UIDs (e.g., PMIDs for PubMed)

**Required Parameters**:
- `db` - Database to search (e.g., pubmed, gene, protein)
- `term` - Search query

**Optional Parameters**:
- `retmax` - Maximum records to return (default: 20, max: 10000)
- `retstart` - Index of first record to return (default: 0)
- `usehistory=y` - Store results on history server for large result sets
- `retmode` - Return format (xml, json)
- `sort` - Sort order (relevance, pub_date, first_author, last_author, journal)
- `field` - Limit search to specific field
- `datetype` - Type of date to use for filtering (pdat for publication date)
- `mindate` - Minimum date (YYYY/MM/DD format)
- `maxdate` - Maximum date (YYYY/MM/DD format)

**Example Request**:
```
esearch.fcgi?db=pubmed&term=breast+cancer&retmax=100&retmode=json&api_key=YOUR_API_KEY
```

**Response Elements**:
- `Count` - Total number of records matching query
- `RetMax` - Number of records returned in this response
- `RetStart` - Index of first returned record
- `IdList` - List of UIDs (PMIDs)
- `WebEnv` - History server environment string (when usehistory=y)
- `QueryKey` - Query key for history server (when usehistory=y)

### 2. EFetch - Download Records

**Endpoint**: `efetch.fcgi`

**Purpose**: Retrieve full records from a database in various formats

**Required Parameters**:
- `db` - Database name
- `id` - Comma-separated list of UIDs, or use WebEnv/query_key from ESearch

**Optional Parameters**:
- `rettype` - Record type (abstract, medline, xml, uilist)
- `retmode` - Return mode (text, xml)
- `retstart` - Starting record index
- `retmax` - Maximum records per request

**Example Request**:
```
efetch.fcgi?db=pubmed&id=123456,234567&rettype=abstract&retmode=text&api_key=YOUR_API_KEY
```

**Common rettype Values for PubMed**:
- `abstract` - Abstract text
- `medline` - Full MEDLINE format
- `xml` - PubMed XML format
- `uilist` - List of UIDs only

### 3. ESummary - Retrieve Document Summaries

**Endpoint**: `esummary.fcgi`

**Purpose**: Get document summaries (DocSum) for a list of UIDs

**Required Parameters**:
- `db` - Database name
- `id` - Comma-separated UIDs or WebEnv/query_key

**Optional Parameters**:
- `retmode` - Return format (xml, json)
- `version` - DocSum version (1.0 or 2.0, default is 1.0)

**Example Request**:
```
esummary.fcgi?db=pubmed&id=123456,234567&retmode=json&version=2.0&api_key=YOUR_API_KEY
```

**DocSum Fields** (vary by database, common PubMed fields):
- Title
- Authors
- Source (journal)
- PubDate
- Volume, Issue, Pages
- DOI
- PmcRefCount (citations in PMC)

### 4. EPost - Upload UIDs

**Endpoint**: `epost.fcgi`

**Purpose**: Upload a list of UIDs to the history server for use in subsequent requests

**Required Parameters**:
- `db` - Database name
- `id` - Comma-separated list of UIDs

**Example Request**:
```
epost.fcgi?db=pubmed&id=123456,234567,345678&api_key=YOUR_API_KEY
```

**Response**:
Returns WebEnv and QueryKey for use in subsequent requests

### 5. ELink - Find Related Data

**Endpoint**: `elink.fcgi`

**Purpose**: Find related records within the same database or in different databases

**Required Parameters**:
- `dbfrom` - Source database
- `db` - Target database (can be same as dbfrom)
- `id` - UID(s) from source database

**Optional Parameters**:
- `cmd` - Link command (neighbor, neighbor_history, prlinks, llinks, etc.)
- `linkname` - Specific link type to retrieve
- `term` - Filter results with search query
- `holding` - Filter by library holdings

**Example Request**:
```
elink.fcgi?dbfrom=pubmed&db=pubmed&id=123456&cmd=neighbor&api_key=YOUR_API_KEY
```

**Common Link Commands**:
- `neighbor` - Return related records
- `neighbor_history` - Post related records to history server
- `prlinks` - Return provider URLs
- `llinks` - Return LinkOut URLs

### 6. EInfo - Database Information

**Endpoint**: `einfo.fcgi`

**Purpose**: Get information about available Entrez databases or specific database fields

**Parameters**:
- `db` - Database name (optional; omit to list all databases)
- `retmode` - Return format (xml, json)

**Example Request**:
```
einfo.fcgi?db=pubmed&retmode=json&api_key=YOUR_API_KEY
```

**Returns**:
- Database description
- Record count
- Last update date
- Available search fields with descriptions

### 7. EGQuery - Global Query

**Endpoint**: `egquery.fcgi`

**Purpose**: Search term counts across all Entrez databases

**Required Parameters**:
- `term` - Search query

**Example Request**:
```
egquery.fcgi?term=cancer&api_key=YOUR_API_KEY
```

### 8. ESpell - Spelling Suggestions

**Endpoint**: `espell.fcgi`

**Purpose**: Get spelling suggestions for queries

**Required Parameters**:
- `db` - Database name
- `term` - Search term with potential misspelling

**Example Request**:
```
espell.fcgi?db=pubmed&term=cancre&api_key=YOUR_API_KEY
```

### 9. ECitMatch - Citation Matching

**Endpoint**: `ecitmatch.cgi`

**Purpose**: Search PubMed citations using journal, year, volume, page, author information

**Request Format**: POST request with citation strings

**Citation String Format**:
```
journal|year|volume|page|author|key|
```

**Example**:
```
Science|2008|320|5880|1185|key1|
Nature|2010|463|7279|318|key2|
```

**Rate Limit**: 3 requests per second with User-Agent header required

## Best Practices

### Use History Server for Large Result Sets

For queries returning more than 500 records, use the history server:

1. **Initial Search with History**:
```
esearch.fcgi?db=pubmed&term=cancer&usehistory=y&retmode=json&api_key=YOUR_API_KEY
```

2. **Retrieve Records in Batches**:
```
efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_12345&retstart=0&retmax=500&rettype=xml&api_key=YOUR_API_KEY
efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_12345&retstart=500&retmax=500&rettype=xml&api_key=YOUR_API_KEY
```

### Batch Operations

Use EPost to upload large lists of UIDs before fetching:

```
# Step 1: Post UIDs
epost.fcgi?db=pubmed&id=123,456,789,...&api_key=YOUR_API_KEY

# Step 2: Fetch using WebEnv/query_key
efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_12345&rettype=xml&api_key=YOUR_API_KEY
```

### Error Handling

Common HTTP status codes:
- `200` - Success
- `400` - Bad request (check parameters)
- `414` - URI too long (use POST or history server)
- `429` - Rate limit exceeded

### Caching

Implement local caching to:
- Reduce redundant API calls
- Stay within rate limits
- Improve response times
- Respect NCBI resources

## Response Formats

### XML (Default)

Most detailed format with full structured data. Each database has its own DTD (Document Type Definition).

### JSON

Available for most utilities with `retmode=json`. Easier to parse in modern applications.

### Text

Plain text format, useful for abstracts and simple data retrieval.

## Support and Resources

- **API Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **Mailing List**: utilities-announce@ncbi.nlm.nih.gov
- **Support**: vog.hin.mln.ibcn@seitilitue
- **NLM Help Desk**: 1-888-FIND-NLM (1-888-346-3656)

---

## Reference: Common_Queries

# Common PubMed Query Patterns

This reference provides practical examples of common PubMed search patterns for various research scenarios.

## General Research Queries

### Finding Recent Research on a Topic
```
breast cancer[tiab] AND 2023:2024[dp]
```

### Systematic Reviews on a Topic
```
(diabetes[tiab] OR diabetes mellitus[mh]) AND systematic review[pt]
```

### Meta-Analyses
```
hypertension[tiab] AND meta-analysis[pt] AND 2020:2024[dp]
```

### Clinical Trials
```
alzheimer disease[mh] AND randomized controlled trial[pt]
```

### Finding Guidelines
```
asthma[tiab] AND (guideline[pt] OR practice guideline[pt])
```

## Disease-Specific Queries

### Cancer Research
```
# General cancer screening
cancer screening[tiab] AND systematic review[pt] AND 2020:2024[dp]

# Specific cancer type with treatment
lung cancer[tiab] AND immunotherapy[tiab] AND clinical trial[pt]

# Cancer genetics
breast neoplasms[mh] AND BRCA1[tiab] AND genetic testing[tiab]
```

### Cardiovascular Disease
```
# Heart disease prevention
(heart disease[tiab] OR cardiovascular disease[mh]) AND prevention[tiab] AND 2022:2024[dp]

# Stroke treatment
stroke[mh] AND (thrombectomy[tiab] OR thrombolysis[tiab]) AND randomized controlled trial[pt]

# Hypertension management
hypertension[mh]/drug therapy AND comparative effectiveness[tiab]
```

### Infectious Diseases
```
# COVID-19 research
COVID-19[tiab] AND (vaccine[tiab] OR vaccination[tiab]) AND 2023:2024[dp]

# Antibiotic resistance
(antibiotic resistance[tiab] OR drug resistance, bacterial[mh]) AND systematic review[pt]

# Tuberculosis treatment
tuberculosis[mh]/drug therapy AND (multidrug-resistant[tiab] OR MDR-TB[tiab])
```

### Neurological Disorders
```
# Alzheimer's disease
alzheimer disease[mh] AND (diagnosis[sh] OR biomarkers[tiab]) AND 2020:2024[dp]

# Parkinson's disease treatment
parkinson disease[mh] AND treatment[tiab] AND clinical trial[pt]

# Multiple sclerosis
multiple sclerosis[mh] AND disease modifying[tiab] AND review[pt]
```

### Diabetes
```
# Type 2 diabetes management
diabetes mellitus, type 2[mh] AND (lifestyle[tiab] OR diet[tiab]) AND randomized controlled trial[pt]

# Diabetes complications
diabetes mellitus[mh] AND (complications[sh] OR diabetic neuropathy[mh])

# New diabetes drugs
diabetes mellitus, type 2[mh] AND (GLP-1[tiab] OR SGLT2[tiab]) AND 2022:2024[dp]
```

## Drug and Treatment Research

### Drug Efficacy Studies
```
# Compare two drugs
(drug A[nm] OR drug B[nm]) AND condition[mh] AND comparative effectiveness[tiab]

# Drug side effects
medication name[nm] AND (adverse effects[sh] OR side effects[tiab])

# Drug combination therapy
(aspirin[nm] AND clopidogrel[nm]) AND acute coronary syndrome[mh]
```

### Treatment Comparisons
```
# Surgery vs medication
condition[mh] AND (surgery[tiab] OR surgical[tiab]) AND (medication[tiab] OR drug therapy[sh]) AND comparative study[pt]

# Different surgical approaches
procedure[tiab] AND (laparoscopic[tiab] OR open surgery[tiab]) AND outcomes[tiab]
```

### Alternative Medicine
```
# Herbal supplements
(herbal medicine[mh] OR phytotherapy[mh]) AND condition[tiab] AND clinical trial[pt]

# Acupuncture
acupuncture[mh] AND pain[tiab] AND randomized controlled trial[pt]
```

## Diagnostic Research

### Diagnostic Tests
```
# Sensitivity and specificity
test name[tiab] AND condition[tiab] AND (sensitivity[tiab] AND specificity[tiab])

# Diagnostic imaging
(MRI[tiab] OR magnetic resonance imaging[tiab]) AND brain tumor[tiab] AND diagnosis[sh]

# Lab test evaluation
biomarker name[tiab] AND disease[tiab] AND (diagnostic[tiab] OR screening[tiab])
```

### Screening Programs
```
# Cancer screening
cancer type[tiab] AND screening[tiab] AND (cost effectiveness[tiab] OR benefit[tiab])

# Population screening
condition[tiab] AND mass screening[mh] AND public health[tiab]
```

## Population-Specific Queries

### Pediatric Research
```
# Children with specific condition
condition[tiab] AND (child[mh] OR pediatric[tiab]) AND treatment[tiab]

# Age-specific
disease[tiab] AND (infant[mh] OR child, preschool[mh])

# Pediatric dosing
drug name[nm] AND pediatric[tiab] AND (dosing[tiab] OR dose[tiab])
```

### Geriatric Research
```
# Elderly population
condition[tiab] AND (aged[mh] OR elderly[tiab] OR geriatric[tiab])

# Aging and disease
aging[mh] AND disease[tiab] AND mechanism[tiab]

# Polypharmacy
polypharmacy[tiab] AND elderly[tiab] AND adverse effects[tiab]
```

### Pregnant Women
```
# Pregnancy and medications
drug name[nm] AND (pregnancy[mh] OR pregnant women[tiab]) AND safety[tiab]

# Pregnancy complications
pregnancy complication[tiab] AND management[tiab]
```

### Sex-Specific Research
```
# Female-specific
condition[tiab] AND female[mh] AND hormones[tiab]

# Male-specific
disease[tiab] AND male[mh] AND risk factors[tiab]

# Sex differences
condition[tiab] AND (sex factors[mh] OR gender differences[tiab])
```

## Epidemiology and Public Health

### Prevalence Studies
```
disease[tiab] AND (prevalence[tiab] OR epidemiology[sh]) AND country/region[tiab]
```

### Incidence Studies
```
condition[tiab] AND incidence[tiab] AND population[tiab] AND 2020:2024[dp]
```

### Risk Factors
```
disease[mh] AND (risk factors[mh] OR etiology[sh]) AND cohort study[tiab]
```

### Global Health
```
disease[tiab] AND (developing countries[mh] OR low income[tiab]) AND burden[tiab]
```

### Health Disparities
```
condition[tiab] AND (health disparities[tiab] OR health equity[tiab]) AND minority groups[tiab]
```

## Methodology-Specific Queries

### Research Methodology

#### Cohort Studies
```
condition[tiab] AND cohort study[tiab] AND prospective[tiab]
```

#### Case-Control Studies
```
disease[tiab] AND case-control studies[mh] AND risk factors[tiab]
```

#### Cross-Sectional Studies
```
condition[tiab] AND cross-sectional studies[mh] AND prevalence[tiab]
```

### Statistical Methods
```
# Machine learning in medicine
(machine learning[tiab] OR artificial intelligence[tiab]) AND diagnosis[tiab] AND validation[tiab]

# Bayesian analysis
condition[tiab] AND bayes theorem[mh] AND clinical decision[tiab]
```

### Genetic and Molecular Research
```
# GWAS studies
disease[tiab] AND (genome-wide association study[tiab] OR GWAS[tiab])

# Gene expression
gene name[tiab] AND (gene expression[mh] OR mRNA[tiab]) AND disease[tiab]

# Proteomics
condition[tiab] AND proteomics[mh] AND biomarkers[tiab]

# CRISPR research
CRISPR[tiab] AND (gene editing[tiab] OR genome editing[tiab]) AND 2020:2024[dp]
```

## Author and Institution Queries

### Finding Work by Specific Author
```
# Single author
smith ja[au] AND cancer[tiab] AND 2023:2024[dp]

# First author only
jones m[1au] AND cardiology[tiab]

# Multiple authors from same group
(smith ja[au] OR jones m[au] OR wilson k[au]) AND research topic[tiab]
```

### Institution-Specific Research
```
# University affiliation
harvard[affil] AND cancer research[tiab] AND 2023:2024[dp]

# Hospital research
"mayo clinic"[affil] AND clinical trial[pt]

# Country-specific
japan[affil] AND robotics[tiab] AND surgery[tiab]
```

## Journal-Specific Queries

### High-Impact Journals
```
# Specific journal
nature[ta] AND genetics[tiab] AND 2024[dp]

# Multiple journals
(nature[ta] OR science[ta] OR cell[ta]) AND immunology[tiab]

# Journal with ISSN
0028-4793[issn] AND clinical trial[pt]
```

## Citation and Reference Queries

### Finding Specific Articles
```
# By PMID
12345678[pmid]

# By DOI
10.1056/NEJMoa123456[doi]

# By first author and year
smith ja[1au] AND 2023[dp] AND cancer[tiab]
```

### Finding Cited Work
```
# Related articles
Similar Articles feature from any PubMed result

# By keyword in references
Use "Cited by" links when available
```

## Advanced Combination Queries

### Comprehensive Literature Review
```
(disease name[tiab] OR disease name[mh]) AND
((treatment[tiab] OR therapy[tiab] OR management[tiab]) OR
(diagnosis[tiab] OR screening[tiab]) OR
(epidemiology[tiab] OR prevalence[tiab])) AND
(systematic review[pt] OR meta-analysis[pt] OR review[pt]) AND
2019:2024[dp] AND english[la]
```

### Precision Medicine Query
```
(precision medicine[tiab] OR personalized medicine[tiab] OR pharmacogenomics[mh]) AND
cancer[tiab] AND
(biomarkers[tiab] OR genetic testing[tiab]) AND
clinical application[tiab] AND
2020:2024[dp]
```

### Translational Research
```
(basic science[tiab] OR bench to bedside[tiab] OR translational medical research[mh]) AND
disease[tiab] AND
(clinical trial[pt] OR clinical application[tiab]) AND
2020:2024[dp]
```

## Quality Filters

### High-Quality Evidence
```
condition[tiab] AND
(randomized controlled trial[pt] OR systematic review[pt] OR meta-analysis[pt]) AND
humans[mh] AND
english[la] AND
2020:2024[dp]
```

### Free Full Text Articles
```
topic[tiab] AND free full text[sb] AND 2023:2024[dp]
```

### Articles with Abstracts
```
condition[tiab] AND hasabstract[text] AND review[pt]
```

## Staying Current

### Latest Publications
```
topic[tiab] AND 2024[dp] AND english[la]
```

### Preprints and Early Access
```
topic[tiab] AND (epub ahead of print[tiab] OR publisher[sb])
```

### Setting Up Alerts
```
# Create search and save to My NCBI
# Enable email alerts for new matching articles
topic[tiab] AND (randomized controlled trial[pt] OR systematic review[pt])
```

## COVID-19 Specific Queries

### Vaccine Research
```
(COVID-19[tiab] OR SARS-CoV-2[tiab]) AND
(vaccine[tiab] OR vaccination[tiab]) AND
(efficacy[tiab] OR effectiveness[tiab]) AND
2023:2024[dp]
```

### Long COVID
```
(long covid[tiab] OR post-acute covid[tiab] OR PASC[tiab]) AND
(symptoms[tiab] OR treatment[tiab])
```

### COVID Treatment
```
COVID-19[tiab] AND
(antiviral[tiab] OR monoclonal antibody[tiab] OR treatment[tiab]) AND
randomized controlled trial[pt]
```

## Tips for Constructing Queries

### 1. PICO Framework
Use PICO (Population, Intervention, Comparison, Outcome) to structure clinical queries:

```
P: diabetes mellitus, type 2[mh]
I: metformin[nm]
C: lifestyle modification[tiab]
O: glycemic control[tiab]

Query: diabetes mellitus, type 2[mh] AND (metformin[nm] OR lifestyle modification[tiab]) AND glycemic control[tiab]
```

### 2. Iterative Refinement
Start broad, review results, refine:
```
1. diabetes → too broad
2. diabetes mellitus type 2 → better
3. diabetes mellitus, type 2[mh] AND metformin[nm] → more specific
4. diabetes mellitus, type 2[mh] AND metformin[nm] AND randomized controlled trial[pt] → focused
```

### 3. Use Search History
Combine previous searches in Advanced Search:
```
#1: diabetes mellitus, type 2[mh]
#2: cardiovascular disease[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

### 4. Save Effective Searches
Create My NCBI account to save successful queries for future use and set up automatic alerts.

---

## Reference: Search_Syntax

# PubMed Search Syntax and Field Tags

## Boolean Operators

PubMed supports standard Boolean operators to combine search terms:

### AND
Retrieves results containing all search terms. PubMed automatically applies AND between separate concepts.

**Example**:
```
diabetes AND hypertension
```

### OR
Retrieves results containing at least one of the search terms. Useful for synonyms or related concepts.

**Example**:
```
heart attack OR myocardial infarction
```

### NOT
Excludes results containing the specified term. Use cautiously as it may eliminate relevant results.

**Example**:
```
cancer NOT lung
```

**Precedence**: Operations are processed left to right. Use parentheses to control evaluation order:
```
(heart attack OR myocardial infarction) AND treatment
```

## Phrase Searching

### Double Quotes
Enclose exact phrases in double quotes to search for terms in specific order:

```
"kidney allograft"
"machine learning"
"systematic review"
```

### Field Tags
Alternative method using field tags:
```
kidney allograft[Title]
```

## Wildcards

Use asterisk (*) to substitute for zero or more characters:

**Rules**:
- Minimum 4 characters before first wildcard
- Matches word variations and plurals

**Examples**:
```
vaccin*        → matches vaccine, vaccination, vaccines, vaccinate
pediatr*       → matches pediatric, pediatrics, pediatrician
colo*r         → matches color, colour
```

**Limitations**:
- Cannot use at beginning of search term
- May retrieve unexpected variations

## Proximity Searching

Search for terms within a specified distance from each other. Only available in Title, Title/Abstract, and Affiliation fields.

**Syntax**: `"search terms"[field:~N]`
- N = maximum number of words between terms

**Examples**:
```
"vitamin C"[Title:~3]           → vitamin within 3 words of C in title
"breast cancer screening"[TIAB:~5]  → terms within 5 words in title/abstract
```

## Search Field Tags

Field tags limit searches to specific parts of PubMed records. Format: `term[tag]`

### Author Searching

| Tag | Field | Example |
|-----|-------|---------|
| [au] | Author | smith j[au] |
| [1au] | First Author | jones m[1au] |
| [lastau] | Last Author | wilson k[lastau] |
| [fau] | Full Author Name | smith john a[fau] |

**Author Search Notes**:
- Full author names searchable from 2002 forward
- Format: last name + initials (e.g., `smith ja[au]`)
- Can search without field tag, but [au] ensures accuracy

**Corporate Authors**:
Search organizations as authors:
```
world health organization[au]
```

### Title and Abstract

| Tag | Field | Example |
|-----|-------|---------|
| [ti] | Title | diabetes[ti] |
| [ab] | Abstract | treatment[ab] |
| [tiab] | Title/Abstract | cancer screening[tiab] |
| [tw] | Text Word | cardiovascular[tw] |

**Notes**:
- [tw] searches title, abstract, and other text fields
- [tiab] is most commonly used for comprehensive searching

### Journal Information

| Tag | Field | Example |
|-----|-------|---------|
| [ta] | Journal Title Abbreviation | Science[ta] |
| [jour] | Journal | New England Journal of Medicine[jour] |
| [issn] | ISSN | 0028-4793[issn] |

### Date Fields

| Tag | Field | Format | Example |
|-----|-------|--------|---------|
| [dp] | Publication Date | YYYY/MM/DD | 2023[dp] |
| [edat] | Entrez Date | YYYY/MM/DD | 2023/01/15[edat] |
| [crdt] | Create Date | YYYY/MM/DD | 2023[crdt] |
| [mhda] | MeSH Date | YYYY/MM/DD | 2023[mhda] |

**Date Ranges**:
Use colon to specify ranges:
```
2020:2023[dp]                    → publications from 2020 to 2023
2023/01/01:2023/06/30[dp]        → first half of 2023
```

**Relative Dates**:
PubMed filters provide common ranges:
- Last 1 year
- Last 5 years
- Last 10 years
- Custom date range

### MeSH and Subject Headings

| Tag | Field | Example |
|-----|-------|---------|
| [mh] | MeSH Terms | diabetes mellitus[mh] |
| [majr] | MeSH Major Topic | hypertension[majr] |
| [mesh] | MeSH Terms | cancer[mesh] |
| [sh] | MeSH Subheading | therapy[sh] |

**MeSH Searching**:
- Medical Subject Headings provide controlled vocabulary
- [mh] includes narrower terms automatically
- [majr] limits to articles where topic is main focus
- Combine with subheadings: `diabetes mellitus/therapy[mh]`

**Common MeSH Subheadings**:
- /diagnosis
- /drug therapy
- /epidemiology
- /etiology
- /prevention & control
- /therapy

### Publication Types

| Tag | Field | Example |
|-----|-------|---------|
| [pt] | Publication Type | clinical trial[pt] |
| [ptyp] | Publication Type | review[ptyp] |

**Common Publication Types**:
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Letter
- Editorial
- Guideline

**Example**:
```
cancer AND systematic review[pt]
```

### Other Useful Fields

| Tag | Field | Example |
|-----|-------|---------|
| [la] | Language | english[la] |
| [affil] | Affiliation | harvard[affil] |
| [pmid] | PubMed ID | 12345678[pmid] |
| [pmc] | PMC ID | PMC123456[pmc] |
| [doi] | DOI | 10.1234/example[doi] |
| [gr] | Grant Number | R01CA123456[gr] |
| [isbn] | ISBN | 9780123456789[isbn] |
| [pg] | Pagination | 123-145[pg] |
| [vi] | Volume | 45[vi] |
| [ip] | Issue | 3[ip] |

### Supplemental Concepts

| Tag | Field | Example |
|-----|-------|---------|
| [nm] | Substance Name | aspirin[nm] |
| [ps] | Personal Name | darwin charles[ps] |

## Automatic Term Mapping (ATM)

When searching without field tags, PubMed automatically:

1. **Searches MeSH translation table** for matching MeSH terms
2. **Searches journal translation table** for journal names
3. **Searches author index** for author names
4. **Searches full text** for remaining terms

**Bypass ATM**:
- Use double quotes: `"breast cancer"`
- Use field tags: `breast cancer[tiab]`

**View Translation**:
Use Advanced Search to see how PubMed translated your query in the Search Details box.

## Filters and Limits

### Article Types
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review

### Text Availability
- Free full text
- Full text
- Abstract

### Publication Date
- Last 1 year
- Last 5 years
- Last 10 years
- Custom date range

### Species
- Humans
- Animals (specific species available)

### Sex
- Female
- Male

### Age Groups
- Child (0-18 years)
- Infant (birth-23 months)
- Child, Preschool (2-5 years)
- Child (6-12 years)
- Adolescent (13-18 years)
- Adult (19+ years)
- Aged (65+ years)
- 80 and over

### Languages
- English
- Spanish
- French
- German
- Chinese
- And many others

### Other Filters
- Journal categories
- Subject area
- Article attributes (e.g., has abstract, free PMC article)

## Advanced Search Strategies

### Clinical Queries
PubMed provides specialized filters for clinical research:

**Study Categories**:
- Therapy (narrow/broad)
- Diagnosis (narrow/broad)
- Etiology (narrow/broad)
- Prognosis (narrow/broad)
- Clinical prediction guides

**Medical Genetics**:
- Diagnosis
- Differential diagnosis
- Clinical description
- Management
- Genetic counseling

### Hedges and Filters
Pre-built search strategies for specific purposes:
- Systematic review filters
- Quality filters for study types
- Geographic filters

### Combining Searches
Use Advanced Search to combine previous queries:
```
#1 AND #2
#3 OR #4
#5 NOT #6
```

### Search History
- Saves up to 100 searches
- Expires after 8 hours of inactivity
- Access via Advanced Search page
- Combine using # references

## Best Practices

### 1. Start Broad, Then Narrow
Begin with general terms and add specificity:
```
diabetes                                 → too broad
diabetes mellitus type 2                 → better
diabetes mellitus type 2[mh] AND treatment[tiab] → more specific
```

### 2. Use Synonyms with OR
Include alternative terms:
```
heart attack OR myocardial infarction OR MI
```

### 3. Combine Concepts with AND
Link different aspects of your research question:
```
(heart attack OR myocardial infarction) AND (aspirin OR acetylsalicylic acid) AND prevention
```

### 4. Leverage MeSH Terms
Use MeSH for consistent indexing:
```
diabetes mellitus[mh] AND hypertension[mh]
```

### 5. Use Filters Strategically
Apply filters to refine results:
- Publication date for recent research
- Article type for specific study designs
- Free full text for accessible articles

### 6. Review Search Details
Check how PubMed interpreted your search in Advanced Search to ensure accuracy.

### 7. Save Effective Searches
Create My NCBI account to:
- Save searches
- Set up email alerts
- Create collections

## Common Search Patterns

### Systematic Review Search
```
(breast cancer[tiab] OR breast neoplasm[mh]) AND (screening[tiab] OR early detection[tiab]) AND systematic review[pt]
```

### Clinical Trial Search
```
diabetes mellitus type 2[mh] AND metformin[nm] AND randomized controlled trial[pt] AND 2020:2024[dp]
```

### Recent Research by Author
```
smith ja[au] AND cancer[tiab] AND 2023:2024[dp] AND english[la]
```

### Drug Treatment Studies
```
hypertension[mh] AND (amlodipine[nm] OR losartan[nm]) AND drug therapy[sh] AND humans[mh]
```

### Geographic-Specific Research
```
malaria[tiab] AND (africa[affil] OR african[tiab]) AND 2020:2024[dp]
```

## Special Characters

| Character | Purpose | Example |
|-----------|---------|---------|
| * | Wildcard | colo*r |
| " " | Phrase search | "breast cancer" |
| ( ) | Group terms | (A OR B) AND C |
| : | Range | 2020:2023[dp] |
| - | Hyphenated terms | COVID-19 |
| / | MeSH subheading | diabetes/therapy[mh] |

## Troubleshooting

### Too Many Results
- Add more specific terms
- Use field tags to limit search scope
- Apply date restrictions
- Use filters for article type
- Add additional concepts with AND

### Too Few Results
- Remove restrictive terms
- Use OR to add synonyms
- Check spelling and terminology
- Remove field tags for broader search
- Expand date range
- Remove filters

### No Results
- Check spelling using ESpell
- Try alternative terminology
- Remove field tags
- Verify correct database (PubMed vs. PMC)
- Broaden search terms

### Unexpected Results
- Review Search Details to see query translation
- Use field tags to prevent automatic term mapping
- Check for common synonyms that may be included
- Refine with additional limiting terms
