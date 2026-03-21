---
title: "Labarchive Integration"
description: "Electronic lab notebook API integration. Access notebooks, manage entries/attachments, backup notebooks, integrate with Protocols.io/Jupyter/REDCap, for programmatic ELN workflows."
category: "writing"
source: "community"
author: "Community"
tags: ["labarchive", "integration"]
date: 2026-03-20
---

# LabArchives Integration

## Overview

LabArchives is an electronic lab notebook platform for research documentation and data management. Access notebooks, manage entries and attachments, generate reports, and integrate with third-party tools programmatically via REST API.

## When to Use This Skill

This skill should be used when:
- Working with LabArchives REST API for notebook automation
- Backing up notebooks programmatically
- Creating or managing notebook entries and attachments
- Generating site reports and analytics
- Integrating LabArchives with third-party tools (Protocols.io, Jupyter, REDCap)
- Automating data upload to electronic lab notebooks
- Managing user access and permissions programmatically

## Core Capabilities

### 1. Authentication and Configuration

Set up API access credentials and regional endpoints for LabArchives API integration.

**Prerequisites:**
- Enterprise LabArchives license with API access enabled
- API access key ID and password from LabArchives administrator
- User authentication credentials (email and external applications password)

**Configuration setup:**

Use the `scripts/setup_config.py` script to create a configuration file:

```bash
python3 scripts/setup_config.py
```

This creates a `config.yaml` file with the following structure:

```yaml
api_url: https://api.labarchives.com/api  # or regional endpoint
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

**Regional API endpoints:**
- US/International: `https://api.labarchives.com/api`
- Australia: `https://auapi.labarchives.com/api`
- UK: `https://ukapi.labarchives.com/api`

For detailed authentication instructions and troubleshooting, refer to `references/authentication_guide.md`.

### 2. User Information Retrieval

Obtain user ID (UID) and access information required for subsequent API operations.

**Workflow:**

1. Call the `users/user_access_info` API method with login credentials
2. Parse the XML/JSON response to extract the user ID (UID)
3. Use the UID to retrieve detailed user information via `users/user_info_via_id`

**Example using Python wrapper:**

```python
from labarchivespy.client import Client

# Initialize client
client = Client(api_url, access_key_id, access_password)

# Get user access info
login_params = {'login_or_email': user_email, 'password': auth_token}
response = client.make_call('users', 'user_access_info', params=login_params)

# Extract UID from response
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text

# Get detailed user info
params = {'uid': uid}
user_info = client.make_call('users', 'user_info_via_id', params=params)
```

### 3. Notebook Operations

Manage notebook access, backup, and metadata retrieval.

**Key operations:**

- **List notebooks:** Retrieve all notebooks accessible to a user
- **Backup notebooks:** Download complete notebook data with optional attachment inclusion
- **Get notebook IDs:** Retrieve institution-defined notebook identifiers for integration with grants/project management systems
- **Get notebook members:** List all users with access to a specific notebook
- **Get notebook settings:** Retrieve configuration and permissions for notebooks

**Notebook backup example:**

Use the `scripts/notebook_operations.py` script:

```bash
# Backup with attachments (default, creates 7z archive)
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID

# Backup without attachments, JSON format
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID --json --no-attachments
```

**API endpoint format:**
```
https://<api_url>/notebooks/notebook_backup?uid=<UID>&nbid=<NOTEBOOK_ID>&json=true&no_attachments=false
```

For comprehensive API method documentation, refer to `references/api_reference.md`.

### 4. Entry and Attachment Management

Create, modify, and manage notebook entries and file attachments.

**Entry operations:**
- Create new entries in notebooks
- Add comments to existing entries
- Create entry parts/components
- Upload file attachments to entries

**Attachment workflow:**

Use the `scripts/entry_operations.py` script:

```bash
# Upload attachment to an entry
python3 scripts/entry_operations.py upload --uid USER_ID --nbid NOTEBOOK_ID --entry-id ENTRY_ID --file /path/to/file.pdf

# Create a new entry with text content
python3 scripts/entry_operations.py create --uid USER_ID --nbid NOTEBOOK_ID --title "Experiment Results" --content "Results from today's experiment..."
```

**Supported file types:**
- Documents (PDF, DOCX, TXT)
- Images (PNG, JPG, TIFF)
- Data files (CSV, XLSX, HDF5)
- Scientific formats (CIF, MOL, PDB)
- Archives (ZIP, 7Z)

### 5. Site Reports and Analytics

Generate institutional reports on notebook usage, activity, and compliance (Enterprise feature).

**Available reports:**
- Detailed Usage Report: User activity metrics and engagement statistics
- Detailed Notebook Report: Notebook metadata, member lists, and settings
- PDF/Offline Notebook Generation Report: Export tracking for compliance
- Notebook Members Report: Access control and collaboration analytics
- Notebook Settings Report: Configuration and permission auditing

**Report generation:**

```python
# Generate detailed usage report
response = client.make_call('site_reports', 'detailed_usage_report',
                           params={'start_date': '2025-01-01', 'end_date': '2025-10-20'})
```

### 6. Third-Party Integrations

LabArchives integrates with numerous scientific software platforms. This skill provides guidance on leveraging these integrations programmatically.

**Supported integrations:**
- **Protocols.io:** Export protocols directly to LabArchives notebooks
- **GraphPad Prism:** Export analyses and figures (Version 8+)
- **SnapGene:** Direct molecular biology workflow integration
- **Geneious:** Bioinformatics analysis export
- **Jupyter:** Embed Jupyter notebooks as entries
- **REDCap:** Clinical data capture integration
- **Qeios:** Research publishing platform
- **SciSpace:** Literature management

**OAuth authentication:**
LabArchives now uses OAuth for all new integrations. Legacy integrations may use API key authentication.

For detailed integration setup instructions and use cases, refer to `references/integrations.md`.

## Common Workflows

### Complete notebook backup workflow

1. Authenticate and obtain user ID
2. List all accessible notebooks
3. Iterate through notebooks and backup each one
4. Store backups with timestamp metadata

```bash
# Complete backup script
python3 scripts/notebook_operations.py backup-all --email user@example.edu --password AUTH_TOKEN
```

### Automated data upload workflow

1. Authenticate with LabArchives API
2. Identify target notebook and entry
3. Upload experimental data files
4. Add metadata comments to entries
5. Generate activity report

### Integration workflow example (Jupyter → LabArchives)

1. Export Jupyter notebook to HTML or PDF
2. Use entry_operations.py to upload to LabArchives
3. Add comment with execution timestamp and environment info
4. Tag entry for easy retrieval

## Python Package Installation

Install the `labarchives-py` wrapper for simplified API access:

```bash
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
uv pip install .
```

Alternatively, use direct HTTP requests via Python's `requests` library for custom implementations.

## Best Practices

1. **Rate limiting:** Implement appropriate delays between API calls to avoid throttling
2. **Error handling:** Always wrap API calls in try-except blocks with appropriate logging
3. **Authentication security:** Store credentials in environment variables or secure config files (never in code)
4. **Backup verification:** After notebook backup, verify file integrity and completeness
5. **Incremental operations:** For large notebooks, use pagination and batch processing
6. **Regional endpoints:** Use the correct regional API endpoint for optimal performance

## Troubleshooting

**Common issues:**

- **401 Unauthorized:** Verify access key ID and password are correct; check API access is enabled for your account
- **404 Not Found:** Confirm notebook ID (nbid) exists and user has access permissions
- **403 Forbidden:** Check user permissions for the requested operation
- **Empty response:** Ensure required parameters (uid, nbid) are provided correctly
- **Attachment upload failures:** Verify file size limits and format compatibility

For additional support, contact LabArchives at support@labarchives.com.

## Resources

This skill includes bundled resources to support LabArchives API integration:

### scripts/

- `setup_config.py`: Interactive configuration file generator for API credentials
- `notebook_operations.py`: Utilities for listing, backing up, and managing notebooks
- `entry_operations.py`: Tools for creating entries and uploading attachments

### references/

- `api_reference.md`: Comprehensive API endpoint documentation with parameters and examples
- `authentication_guide.md`: Detailed authentication setup and configuration instructions
- `integrations.md`: Third-party integration setup guides and use cases

---

## Reference: Api_Reference

# LabArchives API Reference

## API Structure

All LabArchives API calls follow this URL pattern:

```
https://<base_url>/api/<api_class>/<api_method>?<authentication_parameters>&<method_parameters>
```

## Regional API Endpoints

| Region | Base URL |
|--------|----------|
| US/International | `https://api.labarchives.com/api` |
| Australia | `https://auapi.labarchives.com/api` |
| UK | `https://ukapi.labarchives.com/api` |

## Authentication

All API calls require authentication parameters:

- `access_key_id`: Provided by LabArchives administrator
- `access_password`: Provided by LabArchives administrator
- Additional user-specific credentials may be required for certain operations

## API Classes and Methods

### Users API Class

#### `users/user_access_info`

Retrieve user ID and notebook access information.

**Parameters:**
- `login_or_email` (required): User's email address or login username
- `password` (required): User's external applications password (not regular login password)

**Returns:** XML or JSON response containing:
- User ID (uid)
- List of accessible notebooks with IDs (nbid)
- Account status and permissions

**Example:**
```python
params = {
    'login_or_email': 'researcher@university.edu',
    'password': 'external_app_password'
}
response = client.make_call('users', 'user_access_info', params=params)
```

#### `users/user_info_via_id`

Retrieve detailed user information by user ID.

**Parameters:**
- `uid` (required): User ID obtained from user_access_info

**Returns:** User profile information including:
- Name and email
- Account creation date
- Institution affiliation
- Role and permissions
- Storage quota and usage

**Example:**
```python
params = {'uid': '12345'}
response = client.make_call('users', 'user_info_via_id', params=params)
```

### Notebooks API Class

#### `notebooks/notebook_backup`

Download complete notebook data including entries, attachments, and metadata.

**Parameters:**
- `uid` (required): User ID
- `nbid` (required): Notebook ID
- `json` (optional, default: false): Return data in JSON format instead of XML
- `no_attachments` (optional, default: false): Exclude attachments from backup

**Returns:**
- When `no_attachments=false`: 7z compressed archive containing all notebook data
- When `no_attachments=true`: XML or JSON structured data with entry content

**File format:**
The returned archive includes:
- Entry text content in HTML format
- File attachments in original formats
- Metadata XML files with timestamps, authors, and version history
- Comment threads and annotations

**Example:**
```python
# Full backup with attachments
params = {
    'uid': '12345',
    'nbid': '67890',
    'json': 'false',
    'no_attachments': 'false'
}
response = client.make_call('notebooks', 'notebook_backup', params=params)

# Write to file
with open('notebook_backup.7z', 'wb') as f:
    f.write(response.content)
```

```python
# Metadata only backup (JSON format, no attachments)
params = {
    'uid': '12345',
    'nbid': '67890',
    'json': 'true',
    'no_attachments': 'true'
}
response = client.make_call('notebooks', 'notebook_backup', params=params)
import json
notebook_data = json.loads(response.content)
```

#### `notebooks/list_notebooks`

Retrieve all notebooks accessible to a user (method name may vary by API version).

**Parameters:**
- `uid` (required): User ID

**Returns:** List of notebooks with:
- Notebook ID (nbid)
- Notebook name
- Creation and modification dates
- Access level (owner, editor, viewer)
- Member count

### Entries API Class

#### `entries/create_entry`

Create a new entry in a notebook.

**Parameters:**
- `uid` (required): User ID
- `nbid` (required): Notebook ID
- `title` (required): Entry title
- `content` (optional): HTML-formatted entry content
- `date` (optional): Entry date (defaults to current date)

**Returns:** Entry ID and creation confirmation

**Example:**
```python
params = {
    'uid': '12345',
    'nbid': '67890',
    'title': 'Experiment 2025-10-20',
    'content': '<p>Conducted PCR amplification of target gene...</p>',
    'date': '2025-10-20'
}
response = client.make_call('entries', 'create_entry', params=params)
```

#### `entries/create_comment`

Add a comment to an existing entry.

**Parameters:**
- `uid` (required): User ID
- `nbid` (required): Notebook ID
- `entry_id` (required): Target entry ID
- `comment` (required): Comment text (HTML supported)

**Returns:** Comment ID and timestamp

#### `entries/create_part`

Add a component/part to an entry (e.g., text section, table, image).

**Parameters:**
- `uid` (required): User ID
- `nbid` (required): Notebook ID
- `entry_id` (required): Target entry ID
- `part_type` (required): Type of part (text, table, image, etc.)
- `content` (required): Part content in appropriate format

**Returns:** Part ID and creation confirmation

#### `entries/upload_attachment`

Upload a file attachment to an entry.

**Parameters:**
- `uid` (required): User ID
- `nbid` (required): Notebook ID
- `entry_id` (required): Target entry ID
- `file` (required): File data (multipart/form-data)
- `filename` (required): Original filename

**Returns:** Attachment ID and upload confirmation

**Example using requests library:**
```python
import requests

url = f'{api_url}/entries/upload_attachment'
files = {'file': open('/path/to/data.csv', 'rb')}
params = {
    'uid': '12345',
    'nbid': '67890',
    'entry_id': '11111',
    'filename': 'data.csv',
    'access_key_id': access_key_id,
    'access_password': access_password
}
response = requests.post(url, files=files, data=params)
```

### Site Reports API Class

Enterprise-only features for institutional reporting and analytics.

#### `site_reports/detailed_usage_report`

Generate comprehensive usage statistics for the institution.

**Parameters:**
- `start_date` (required): Report start date (YYYY-MM-DD)
- `end_date` (required): Report end date (YYYY-MM-DD)
- `format` (optional): Output format (csv, json, xml)

**Returns:** Usage metrics including:
- User login frequency
- Entry creation counts
- Storage utilization
- Collaboration statistics
- Time-based activity patterns

#### `site_reports/detailed_notebook_report`

Generate detailed report on all notebooks in the institution.

**Parameters:**
- `include_settings` (optional, default: false): Include notebook settings
- `include_members` (optional, default: false): Include member lists

**Returns:** Notebook inventory with:
- Notebook names and IDs
- Owner information
- Creation and last modified dates
- Member count and access levels
- Storage size
- Settings (if requested)

#### `site_reports/pdf_offline_generation_report`

Track PDF exports for compliance and auditing purposes.

**Parameters:**
- `start_date` (required): Report start date
- `end_date` (required): Report end date

**Returns:** Export activity log with:
- User who generated PDF
- Notebook and entry exported
- Export timestamp
- IP address

### Utilities API Class

#### `utilities/institutional_login_urls`

Retrieve institutional login URLs for SSO integration.

**Parameters:** None required (uses access key authentication)

**Returns:** List of institutional login endpoints

## Response Formats

### XML Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <uid>12345</uid>
    <email>researcher@university.edu</email>
    <notebooks>
        <notebook>
            <nbid>67890</nbid>
            <name>Lab Notebook 2025</name>
            <role>owner</role>
        </notebook>
    </notebooks>
</response>
```

### JSON Response Example

```json
{
    "uid": "12345",
    "email": "researcher@university.edu",
    "notebooks": [
        {
            "nbid": "67890",
            "name": "Lab Notebook 2025",
            "role": "owner"
        }
    ]
}
```

## Error Codes

| Code | Message | Meaning | Solution |
|------|---------|---------|----------|
| 401 | Unauthorized | Invalid credentials | Verify access_key_id and access_password |
| 403 | Forbidden | Insufficient permissions | Check user role and notebook access |
| 404 | Not Found | Resource doesn't exist | Verify uid, nbid, or entry_id are correct |
| 429 | Too Many Requests | Rate limit exceeded | Implement exponential backoff |
| 500 | Internal Server Error | Server-side issue | Retry request or contact support |

## Rate Limiting

LabArchives implements rate limiting to ensure service stability:

- **Recommended:** Maximum 60 requests per minute per API key
- **Burst allowance:** Short bursts up to 100 requests may be tolerated
- **Best practice:** Implement 1-2 second delays between requests for batch operations

## API Versioning

LabArchives API is backward compatible. New methods are added without breaking existing implementations. Monitor LabArchives announcements for new capabilities.

## Support and Documentation

For API access requests, technical questions, or feature requests:
- Email: support@labarchives.com
- Include your institution name and specific use case for faster assistance

---

## Reference: Authentication_Guide

# LabArchives Authentication Guide

## Prerequisites

### 1. Enterprise License

API access requires an Enterprise LabArchives license. Contact your LabArchives administrator or sales@labarchives.com to:
- Verify your institution has Enterprise access
- Request API access enablement for your account
- Obtain institutional API credentials

### 2. API Credentials

You need two sets of credentials:

#### Institutional API Credentials (from LabArchives administrator)
- **Access Key ID**: Institution-level identifier
- **Access Password**: Institution-level secret

#### User Authentication Credentials (self-configured)
- **Email**: Your LabArchives account email (e.g., researcher@university.edu)
- **External Applications Password**: Set in your LabArchives account settings

## Setting Up External Applications Password

The external applications password is different from your regular LabArchives login password. It provides API access without exposing your primary credentials.

**Steps to create external applications password:**

1. Log into your LabArchives account at mynotebook.labarchives.com (or your institutional URL)
2. Navigate to **Account Settings** (click your name in top-right corner)
3. Select **Security & Privacy** tab
4. Find **External Applications** section
5. Click **Generate New Password** or **Reset Password**
6. Copy and securely store this password (you won't see it again)
7. Use this password for all API authentication

**Security note:** Treat this password like an API token. If compromised, regenerate it immediately from account settings.

## Configuration File Setup

Create a `config.yaml` file to store your credentials securely:

```yaml
# Regional API endpoint
api_url: https://api.labarchives.com/api

# Institutional credentials (from administrator)
access_key_id: YOUR_ACCESS_KEY_ID_HERE
access_password: YOUR_ACCESS_PASSWORD_HERE

# User credentials (for user-specific operations)
user_email: researcher@university.edu
user_external_password: YOUR_EXTERNAL_APP_PASSWORD_HERE
```

**Alternative: Environment variables**

For enhanced security, use environment variables instead of config file:

```bash
export LABARCHIVES_API_URL="https://api.labarchives.com/api"
export LABARCHIVES_ACCESS_KEY_ID="your_key_id"
export LABARCHIVES_ACCESS_PASSWORD="your_access_password"
export LABARCHIVES_USER_EMAIL="researcher@university.edu"
export LABARCHIVES_USER_PASSWORD="your_external_app_password"
```

## Regional Endpoints

Select the correct regional API endpoint for your institution:

| Region | Endpoint | Use if your LabArchives URL is |
|--------|----------|--------------------------------|
| US/International | `https://api.labarchives.com/api` | `mynotebook.labarchives.com` |
| Australia | `https://auapi.labarchives.com/api` | `aunotebook.labarchives.com` |
| UK | `https://ukapi.labarchives.com/api` | `uknotebook.labarchives.com` |

Using the wrong regional endpoint will result in authentication failures even with correct credentials.

## Authentication Flow

### Option 1: Using labarchives-py Python Wrapper

```python
from labarchivespy.client import Client
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize client with institutional credentials
client = Client(
    config['api_url'],
    config['access_key_id'],
    config['access_password']
)

# Authenticate as specific user to get UID
login_params = {
    'login_or_email': config['user_email'],
    'password': config['user_external_password']
}
response = client.make_call('users', 'user_access_info', params=login_params)

# Parse response to extract UID
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text
print(f"Authenticated as user ID: {uid}")
```

### Option 2: Direct HTTP Requests with Python requests

```python
import requests
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Construct API call
url = f"{config['api_url']}/users/user_access_info"
params = {
    'access_key_id': config['access_key_id'],
    'access_password': config['access_password'],
    'login_or_email': config['user_email'],
    'password': config['user_external_password']
}

# Make authenticated request
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Authentication successful!")
    print(response.content.decode('utf-8'))
else:
    print(f"Authentication failed: {response.status_code}")
    print(response.content.decode('utf-8'))
```

### Option 3: Using R

```r
library(httr)
library(xml2)

# Configuration
api_url <- "https://api.labarchives.com/api"
access_key_id <- "YOUR_ACCESS_KEY_ID"
access_password <- "YOUR_ACCESS_PASSWORD"
user_email <- "researcher@university.edu"
user_external_password <- "YOUR_EXTERNAL_APP_PASSWORD"

# Make authenticated request
response <- GET(
    paste0(api_url, "/users/user_access_info"),
    query = list(
        access_key_id = access_key_id,
        access_password = access_password,
        login_or_email = user_email,
        password = user_external_password
    )
)

# Parse response
if (status_code(response) == 200) {
    content <- content(response, as = "text", encoding = "UTF-8")
    xml_data <- read_xml(content)
    uid <- xml_text(xml_find_first(xml_data, "//uid"))
    print(paste("Authenticated as user ID:", uid))
} else {
    print(paste("Authentication failed:", status_code(response)))
}
```

## OAuth Authentication (New Integrations)

LabArchives now uses OAuth 2.0 for new third-party integrations. Legacy API key authentication (described above) continues to work for direct API access.

**OAuth flow (for app developers):**

1. Register your application with LabArchives
2. Obtain client ID and client secret
3. Implement OAuth 2.0 authorization code flow
4. Exchange authorization code for access token
5. Use access token for API requests

Contact LabArchives developer support for OAuth integration documentation.

## Troubleshooting Authentication Issues

### 401 Unauthorized Error

**Possible causes and solutions:**

1. **Incorrect access_key_id or access_password**
   - Verify credentials with your LabArchives administrator
   - Check for typos or extra whitespace in config file

2. **Wrong external applications password**
   - Confirm you're using the external applications password, not your regular login password
   - Regenerate external applications password in account settings

3. **API access not enabled**
   - Contact your LabArchives administrator to enable API access for your account
   - Verify your institution has Enterprise license

4. **Wrong regional endpoint**
   - Confirm your api_url matches your institution's LabArchives instance
   - Check if you're using .com, .auapi, or .ukapi domain

### 403 Forbidden Error

**Possible causes and solutions:**

1. **Insufficient permissions**
   - Verify your account role has necessary permissions
   - Check if you have access to the specific notebook (nbid)

2. **Account suspended or expired**
   - Contact your LabArchives administrator to check account status

### Network and Connection Issues

**Firewall/proxy configuration:**

If your institution uses a firewall or proxy:

```python
import requests

# Configure proxy
proxies = {
    'http': 'http://proxy.university.edu:8080',
    'https': 'http://proxy.university.edu:8080'
}

# Make request with proxy
response = requests.get(url, params=params, proxies=proxies)
```

**SSL certificate verification:**

For self-signed certificates (not recommended for production):

```python
# Disable SSL verification (use only for testing)
response = requests.get(url, params=params, verify=False)
```

## Security Best Practices

1. **Never commit credentials to version control**
   - Add `config.yaml` to `.gitignore`
   - Use environment variables or secret management systems

2. **Rotate credentials regularly**
   - Change external applications password every 90 days
   - Regenerate API keys annually

3. **Use least privilege principle**
   - Request only necessary API permissions
   - Create separate API credentials for different applications

4. **Monitor API usage**
   - Regularly review API access logs
   - Set up alerts for unusual activity

5. **Secure storage**
   - Encrypt configuration files at rest
   - Use system keychain or secret management tools (e.g., AWS Secrets Manager, Azure Key Vault)

## Testing Authentication

Use this script to verify your authentication setup:

```python
#!/usr/bin/env python3
"""Test LabArchives API authentication"""

from labarchivespy.client import Client
import yaml
import sys

def test_authentication():
    try:
        # Load config
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        print("Configuration loaded successfully")
        print(f"API URL: {config['api_url']}")

        # Initialize client
        client = Client(
            config['api_url'],
            config['access_key_id'],
            config['access_password']
        )
        print("Client initialized")

        # Test authentication
        login_params = {
            'login_or_email': config['user_email'],
            'password': config['user_external_password']
        }
        response = client.make_call('users', 'user_access_info', params=login_params)

        if response.status_code == 200:
            print("✅ Authentication successful!")

            # Extract UID
            import xml.etree.ElementTree as ET
            uid = ET.fromstring(response.content)[0].text
            print(f"User ID: {uid}")

            # Get user info
            user_response = client.make_call('users', 'user_info_via_id', params={'uid': uid})
            print("✅ User information retrieved successfully")

            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.content.decode('utf-8'))
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_authentication()
    sys.exit(0 if success else 1)
```

Run this script to confirm everything is configured correctly:

```bash
python3 test_auth.py
```

## Getting Help

If authentication continues to fail after troubleshooting:

1. Contact your institutional LabArchives administrator
2. Email LabArchives support: support@labarchives.com
3. Include:
   - Your institution name
   - Your LabArchives account email
   - Error messages and response codes
   - Regional endpoint you're using
   - Programming language and library versions

---

## Reference: Integrations

# LabArchives Third-Party Integrations

## Overview

LabArchives integrates with numerous scientific software platforms to streamline research workflows. This document covers programmatic integration approaches, automation strategies, and best practices for each supported platform.

## Integration Categories

### 1. Protocol Management

#### Protocols.io Integration

Export protocols directly from Protocols.io to LabArchives notebooks.

**Use cases:**
- Standardize experimental procedures across lab notebooks
- Maintain version control for protocols
- Link protocols to experimental results

**Setup:**
1. Enable Protocols.io integration in LabArchives settings
2. Authenticate with Protocols.io account
3. Browse and select protocols to export

**Programmatic approach:**
```python
# Export Protocols.io protocol as HTML/PDF
# Then upload to LabArchives via API

def import_protocol_to_labarchives(client, uid, nbid, protocol_id):
    """Import Protocols.io protocol to LabArchives entry"""
    # 1. Fetch protocol from Protocols.io API
    protocol_data = fetch_protocol_from_protocolsio(protocol_id)

    # 2. Create new entry in LabArchives
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"Protocol: {protocol_data['title']}",
        'content': protocol_data['html_content']
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    # 3. Add protocol metadata as comment
    entry_id = extract_entry_id(response)
    comment_params = {
        'uid': uid,
        'nbid': nbid,
        'entry_id': entry_id,
        'comment': f"Protocols.io ID: {protocol_id}<br>Version: {protocol_data['version']}"
    }
    client.make_call('entries', 'create_comment', params=comment_params)

    return entry_id
```

**Updated:** September 22, 2025

### 2. Data Analysis Tools

#### GraphPad Prism Integration (Version 8+)

Export analyses, graphs, and figures directly from Prism to LabArchives.

**Use cases:**
- Archive statistical analyses with raw data
- Document figure generation for publications
- Maintain analysis audit trail for compliance

**Setup:**
1. Install GraphPad Prism 8 or higher
2. Configure LabArchives connection in Prism preferences
3. Use "Export to LabArchives" option from File menu

**Programmatic approach:**
```python
# Upload Prism files to LabArchives via API

def upload_prism_analysis(client, uid, nbid, entry_id, prism_file_path):
    """Upload GraphPad Prism file to LabArchives entry"""
    import requests

    url = f'{client.api_url}/entries/upload_attachment'
    files = {'file': open(prism_file_path, 'rb')}
    params = {
        'uid': uid,
        'nbid': nbid,
        'entry_id': entry_id,
        'filename': os.path.basename(prism_file_path),
        'access_key_id': client.access_key_id,
        'access_password': client.access_password
    }

    response = requests.post(url, files=files, data=params)
    return response
```

**Supported file types:**
- .pzfx (Prism project files)
- .png, .jpg, .pdf (exported graphs)
- .xlsx (exported data tables)

**Updated:** September 8, 2025

### 3. Molecular Biology & Bioinformatics

#### SnapGene Integration

Direct integration for molecular biology workflows, plasmid maps, and sequence analysis.

**Use cases:**
- Document cloning strategies
- Archive plasmid maps with experimental records
- Link sequences to experimental results

**Setup:**
1. Install SnapGene software
2. Enable LabArchives export in SnapGene preferences
3. Use "Send to LabArchives" feature

**File format support:**
- .dna (SnapGene files)
- .gb, .gbk (GenBank format)
- .fasta (sequence files)
- .png, .pdf (plasmid map exports)

**Programmatic workflow:**
```python
def upload_snapgene_file(client, uid, nbid, entry_id, snapgene_file):
    """Upload SnapGene file with preview image"""
    # Upload main SnapGene file
    upload_attachment(client, uid, nbid, entry_id, snapgene_file)

    # Generate and upload preview image (requires SnapGene CLI)
    preview_png = generate_snapgene_preview(snapgene_file)
    upload_attachment(client, uid, nbid, entry_id, preview_png)
```

#### Geneious Integration

Bioinformatics analysis export from Geneious to LabArchives.

**Use cases:**
- Archive sequence alignments and phylogenetic trees
- Document NGS analysis pipelines
- Link bioinformatics workflows to wet-lab experiments

**Supported exports:**
- Sequence alignments
- Phylogenetic trees
- Assembly reports
- Variant calling results

**File formats:**
- .geneious (Geneious documents)
- .fasta, .fastq (sequence data)
- .bam, .sam (alignment files)
- .vcf (variant files)

### 4. Computational Notebooks

#### Jupyter Integration

Embed Jupyter notebooks as LabArchives entries for reproducible computational research.

**Use cases:**
- Document data analysis workflows
- Archive computational experiments
- Link code, results, and narrative

**Workflow:**

```python
def export_jupyter_to_labarchives(notebook_path, client, uid, nbid):
    """Export Jupyter notebook to LabArchives"""
    import nbformat
    from nbconvert import HTMLExporter

    # Load notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Convert to HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(nb)

    # Create entry in LabArchives
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"Jupyter Notebook: {os.path.basename(notebook_path)}",
        'content': body
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    # Upload original .ipynb file as attachment
    entry_id = extract_entry_id(response)
    upload_attachment(client, uid, nbid, entry_id, notebook_path)

    return entry_id
```

**Best practices:**
- Export with outputs included (Run All Cells before export)
- Include environment.yml or requirements.txt as attachment
- Add execution timestamp and system info in comments

### 5. Clinical Research

#### REDCap Integration

Clinical data capture integration with LabArchives for research compliance and audit trails.

**Use cases:**
- Link clinical data collection to research notebooks
- Maintain audit trails for regulatory compliance
- Document clinical trial protocols and amendments

**Integration approach:**
- REDCap API exports data to LabArchives entries
- Automated data synchronization for longitudinal studies
- HIPAA-compliant data handling

**Example workflow:**
```python
def sync_redcap_to_labarchives(redcap_api_token, client, uid, nbid):
    """Sync REDCap data to LabArchives"""
    # Fetch REDCap data
    redcap_data = fetch_redcap_data(redcap_api_token)

    # Create LabArchives entry
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"REDCap Data Export {datetime.now().strftime('%Y-%m-%d')}",
        'content': format_redcap_data_html(redcap_data)
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    return response
```

**Compliance features:**
- 21 CFR Part 11 compliance
- Audit trail maintenance
- Data integrity verification

### 6. Research Publishing

#### Qeios Integration

Research publishing platform integration for preprints and peer review.

**Use cases:**
- Export research findings to preprint servers
- Document publication workflows
- Link published articles to lab notebooks

**Workflow:**
- Export formatted entries from LabArchives
- Submit to Qeios platform
- Maintain bidirectional links between notebook and publication

#### SciSpace Integration

Literature management and citation integration.

**Use cases:**
- Link references to experimental procedures
- Maintain literature review in notebooks
- Generate bibliographies for reports

**Features:**
- Citation import from SciSpace to LabArchives
- PDF annotation synchronization
- Reference management

## OAuth Authentication for Integrations

LabArchives now uses OAuth 2.0 for new third-party integrations.

**OAuth flow for app developers:**

```python
def labarchives_oauth_flow(client_id, client_secret, redirect_uri):
    """Implement OAuth 2.0 flow for LabArchives integration"""
    import requests

    # Step 1: Get authorization code
    auth_url = "https://mynotebook.labarchives.com/oauth/authorize"
    auth_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'read write'
    }
    # User visits auth_url and grants permission

    # Step 2: Exchange code for access token
    token_url = "https://mynotebook.labarchives.com/oauth/token"
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code': authorization_code  # From redirect
    }

    response = requests.post(token_url, data=token_params)
    tokens = response.json()

    return tokens['access_token'], tokens['refresh_token']
```

**OAuth advantages:**
- More secure than API keys
- Fine-grained permission control
- Token refresh for long-running integrations
- Revocable access

## Custom Integration Development

### General Workflow

For tools not officially supported, develop custom integrations:

1. **Export data** from source application (API or file export)
2. **Transform format** to HTML or supported file type
3. **Authenticate** with LabArchives API
4. **Create entry** or upload attachment
5. **Add metadata** via comments for traceability

### Example: Custom Integration Template

```python
class LabArchivesIntegration:
    """Template for custom LabArchives integrations"""

    def __init__(self, config_path):
        self.client = self._init_client(config_path)
        self.uid = self._authenticate()

    def _init_client(self, config_path):
        """Initialize LabArchives client"""
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Client(config['api_url'],
                     config['access_key_id'],
                     config['access_password'])

    def _authenticate(self):
        """Get user ID"""
        # Implementation from authentication_guide.md
        pass

    def export_data(self, source_data, nbid, title):
        """Export data to LabArchives"""
        # Transform data to HTML
        html_content = self._transform_to_html(source_data)

        # Create entry
        params = {
            'uid': self.uid,
            'nbid': nbid,
            'title': title,
            'content': html_content
        }
        response = self.client.make_call('entries', 'create_entry', params=params)

        return extract_entry_id(response)

    def _transform_to_html(self, data):
        """Transform data to HTML format"""
        # Custom transformation logic
        pass
```

## Integration Best Practices

1. **Version control:** Track which software version generated the data
2. **Metadata preservation:** Include timestamps, user info, and processing parameters
3. **File format standards:** Use open formats when possible (CSV, JSON, HTML)
4. **Batch operations:** Implement rate limiting for bulk uploads
5. **Error handling:** Implement retry logic with exponential backoff
6. **Audit trails:** Log all API operations for compliance
7. **Testing:** Validate integrations in test notebooks before production use

## Troubleshooting Integrations

### Common Issues

**Integration not appearing in LabArchives:**
- Verify integration is enabled by administrator
- Check OAuth permissions if using OAuth
- Ensure compatible software version

**File upload failures:**
- Verify file size limits (typically 2GB per file)
- Check file format compatibility
- Ensure sufficient storage quota

**Authentication errors:**
- Verify API credentials are current
- Check if integration-specific tokens have expired
- Confirm user has necessary permissions

### Integration Support

For integration-specific issues:
- Check software vendor documentation (e.g., GraphPad, Protocols.io)
- Contact LabArchives support: support@labarchives.com
- Review LabArchives knowledge base: help.labarchives.com

## Future Integration Opportunities

Potential integrations for custom development:
- Electronic data capture (EDC) systems
- Laboratory information management systems (LIMS)
- Instrument data systems (chromatography, spectroscopy)
- Cloud storage platforms (Box, Dropbox, Google Drive)
- Project management tools (Asana, Monday.com)
- Grant management systems

For custom integration development, contact LabArchives for API partnership opportunities.
