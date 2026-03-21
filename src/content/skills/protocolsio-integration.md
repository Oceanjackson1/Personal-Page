---
title: "Protocolsio Integration"
description: "Integration with protocols.io API for managing scientific protocols. This skill should be used when working with protocols.io to search, create, update, or publish protocols; manage protocol steps and materials; handle discussions and comments; or..."
category: "research"
source: "community"
author: "Community"
tags: ["protocolsio", "integration"]
date: 2026-03-20
---

# Protocols.io Integration

## Overview

Protocols.io is a comprehensive platform for developing, sharing, and managing scientific protocols. This skill provides complete integration with the protocols.io API v3, enabling programmatic access to protocols, workspaces, discussions, file management, and collaboration features.

## When to Use This Skill

Use this skill when working with protocols.io in any of the following scenarios:

- **Protocol Discovery**: Searching for existing protocols by keywords, DOI, or category
- **Protocol Management**: Creating, updating, or publishing scientific protocols
- **Step Management**: Adding, editing, or organizing protocol steps and procedures
- **Collaborative Development**: Working with team members on shared protocols
- **Workspace Organization**: Managing lab or institutional protocol repositories
- **Discussion & Feedback**: Adding or responding to protocol comments
- **File Management**: Uploading data files, images, or documents to protocols
- **Experiment Tracking**: Documenting protocol executions and results
- **Data Export**: Backing up or migrating protocol collections
- **Integration Projects**: Building tools that interact with protocols.io

## Core Capabilities

This skill provides comprehensive guidance across five major capability areas:

### 1. Authentication & Access

Manage API authentication using access tokens and OAuth flows. Includes both client access tokens (for personal content) and OAuth tokens (for multi-user applications).

**Key operations:**
- Generate authorization links for OAuth flow
- Exchange authorization codes for access tokens
- Refresh expired tokens
- Manage rate limits and permissions

**Reference:** Read `references/authentication.md` for detailed authentication procedures, OAuth implementation, and security best practices.

### 2. Protocol Operations

Complete protocol lifecycle management from creation to publication.

**Key operations:**
- Search and discover protocols by keywords, filters, or DOI
- Retrieve detailed protocol information with all steps
- Create new protocols with metadata and tags
- Update protocol information and settings
- Manage protocol steps (create, update, delete, reorder)
- Handle protocol materials and reagents
- Publish protocols with DOI issuance
- Bookmark protocols for quick access
- Generate protocol PDFs

**Reference:** Read `references/protocols_api.md` for comprehensive protocol management guidance, including API endpoints, parameters, common workflows, and examples.

### 3. Discussions & Collaboration

Enable community engagement through comments and discussions.

**Key operations:**
- View protocol-level and step-level comments
- Create new comments and threaded replies
- Edit or delete your own comments
- Analyze discussion patterns and feedback
- Respond to user questions and issues

**Reference:** Read `references/discussions.md` for discussion management, comment threading, and collaboration workflows.

### 4. Workspace Management

Organize protocols within team workspaces with role-based permissions.

**Key operations:**
- List and access user workspaces
- Retrieve workspace details and member lists
- Request access or join workspaces
- List workspace-specific protocols
- Create protocols within workspaces
- Manage workspace permissions and collaboration

**Reference:** Read `references/workspaces.md` for workspace organization, permission management, and team collaboration patterns.

### 5. File Operations

Upload, organize, and manage files associated with protocols.

**Key operations:**
- Search workspace files and folders
- Upload files with metadata and tags
- Download files and verify uploads
- Organize files into folder hierarchies
- Update file metadata
- Delete and restore files
- Manage storage and organization

**Reference:** Read `references/file_manager.md` for file upload procedures, organization strategies, and storage management.

### 6. Additional Features

Supplementary functionality including profiles, notifications, and exports.

**Key operations:**
- Manage user profiles and settings
- Query recently published protocols
- Create and track experiment records
- Receive and manage notifications
- Export organization data for archival

**Reference:** Read `references/additional_features.md` for profile management, publication discovery, experiment tracking, and data export.

## Getting Started

### Step 1: Authentication Setup

Before using any protocols.io API functionality:

1. Obtain an access token (CLIENT_ACCESS_TOKEN or OAUTH_ACCESS_TOKEN)
2. Read `references/authentication.md` for detailed authentication procedures
3. Store the token securely
4. Include in all requests as: `Authorization: Bearer YOUR_TOKEN`

### Step 2: Identify Your Use Case

Determine which capability area addresses your needs:

- **Working with protocols?** → Read `references/protocols_api.md`
- **Managing team protocols?** → Read `references/workspaces.md`
- **Handling comments/feedback?** → Read `references/discussions.md`
- **Uploading files/data?** → Read `references/file_manager.md`
- **Tracking experiments or profiles?** → Read `references/additional_features.md`

### Step 3: Implement Integration

Follow the guidance in the relevant reference files:

- Each reference includes detailed endpoint documentation
- API parameters and request/response formats are specified
- Common use cases and workflows are provided with examples
- Best practices and error handling guidance included

## Base URL and Request Format

All API requests use the base URL:
```
https://protocols.io/api/v3
```

All requests require the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Most endpoints support JSON request/response format with `Content-Type: application/json`.

## Content Format Options

Many endpoints support a `content_format` parameter to control how protocol content is returned:

- `json`: Draft.js JSON format (default)
- `html`: HTML format
- `markdown`: Markdown format

Include as query parameter: `?content_format=html`

## Rate Limiting

Be aware of API rate limits:

- **Standard endpoints**: 100 requests per minute per user
- **PDF endpoint**: 5 requests/minute (signed-in), 3 requests/minute (unsigned)

Implement exponential backoff for rate limit errors (HTTP 429).

## Common Workflows

### Workflow 1: Import and Analyze Protocol

To analyze an existing protocol from protocols.io:

1. **Search**: Use `GET /protocols` with keywords to find relevant protocols
2. **Retrieve**: Get full details with `GET /protocols/{protocol_id}`
3. **Extract**: Parse steps, materials, and metadata for analysis
4. **Review discussions**: Check `GET /protocols/{id}/comments` for user feedback
5. **Export**: Generate PDF if needed for offline reference

**Reference files**: `protocols_api.md`, `discussions.md`

### Workflow 2: Create and Publish Protocol

To create a new protocol and publish with DOI:

1. **Authenticate**: Ensure you have valid access token (see `authentication.md`)
2. **Create**: Use `POST /protocols` with title and description
3. **Add steps**: For each step, use `POST /protocols/{id}/steps`
4. **Add materials**: Document reagents in step components
5. **Review**: Verify all content is complete and accurate
6. **Publish**: Issue DOI with `POST /protocols/{id}/publish`

**Reference files**: `protocols_api.md`, `authentication.md`

### Workflow 3: Collaborative Lab Workspace

To set up team protocol management:

1. **Create/join workspace**: Access or request workspace membership (see `workspaces.md`)
2. **Organize structure**: Create folder hierarchy for lab protocols (see `file_manager.md`)
3. **Create protocols**: Use `POST /workspaces/{id}/protocols` for team protocols
4. **Upload files**: Add experimental data and images
5. **Enable discussions**: Team members can comment and provide feedback
6. **Track experiments**: Document protocol executions with experiment records

**Reference files**: `workspaces.md`, `file_manager.md`, `protocols_api.md`, `discussions.md`, `additional_features.md`

### Workflow 4: Experiment Documentation

To track protocol executions and results:

1. **Execute protocol**: Perform protocol in laboratory
2. **Upload data**: Use File Manager API to upload results (see `file_manager.md`)
3. **Create record**: Document execution with `POST /protocols/{id}/runs`
4. **Link files**: Reference uploaded data files in experiment record
5. **Note modifications**: Document any protocol deviations or optimizations
6. **Analyze**: Review multiple runs for reproducibility assessment

**Reference files**: `additional_features.md`, `file_manager.md`, `protocols_api.md`

### Workflow 5: Protocol Discovery and Citation

To find and cite protocols in research:

1. **Search**: Query published protocols with `GET /publications`
2. **Filter**: Use category and keyword filters for relevant protocols
3. **Review**: Read protocol details and community comments
4. **Bookmark**: Save useful protocols with `POST /protocols/{id}/bookmarks`
5. **Cite**: Use protocol DOI in publications (proper attribution)
6. **Export PDF**: Generate formatted PDF for offline reference

**Reference files**: `protocols_api.md`, `additional_features.md`

## Python Request Examples

### Basic Protocol Search

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Search for CRISPR protocols
response = requests.get(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    params={
        "filter": "public",
        "key": "CRISPR",
        "page_size": 10,
        "content_format": "html"
    }
)

protocols = response.json()
for protocol in protocols["items"]:
    print(f"{protocol['title']} - {protocol['doi']}")
```

### Create New Protocol

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create protocol
data = {
    "title": "CRISPR-Cas9 Gene Editing Protocol",
    "description": "Comprehensive protocol for CRISPR gene editing",
    "tags": ["CRISPR", "gene editing", "molecular biology"]
}

response = requests.post(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    json=data
)

protocol_id = response.json()["item"]["id"]
print(f"Created protocol: {protocol_id}")
```

### Upload File to Workspace

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Upload file
with open("data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "folder_id": "root",
        "description": "Experimental results",
        "tags": "experiment,data,2025"
    }

    response = requests.post(
        "https://protocols.io/api/v3/workspaces/12345/files/upload",
        headers=headers,
        files=files,
        data=data
    )

file_id = response.json()["item"]["id"]
print(f"Uploaded file: {file_id}")
```

## Error Handling

Implement robust error handling for API requests:

```python
import requests
import time

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue
            elif response.status_code >= 500:  # Server error
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception("Max retries exceeded")
```

## Reference Files

Load the appropriate reference file based on your task:

- **`authentication.md`**: OAuth flows, token management, rate limiting
- **`protocols_api.md`**: Protocol CRUD, steps, materials, publishing, PDFs
- **`discussions.md`**: Comments, replies, collaboration
- **`workspaces.md`**: Team workspaces, permissions, organization
- **`file_manager.md`**: File upload, folders, storage management
- **`additional_features.md`**: Profiles, publications, experiments, notifications

To load a reference file, read the file from the `references/` directory when needed for specific functionality.

## Best Practices

1. **Authentication**: Store tokens securely, never in code or version control
2. **Rate Limiting**: Implement exponential backoff and respect rate limits
3. **Error Handling**: Handle all HTTP error codes appropriately
4. **Data Validation**: Validate input before API calls
5. **Documentation**: Document protocol steps thoroughly
6. **Collaboration**: Use comments and discussions for team communication
7. **Organization**: Maintain consistent naming and tagging conventions
8. **Versioning**: Track protocol versions when making updates
9. **Attribution**: Properly cite protocols using DOIs
10. **Backup**: Regularly export important protocols and workspace data

## Additional Resources

- **Official API Documentation**: https://apidoc.protocols.io/
- **Protocols.io Platform**: https://www.protocols.io/
- **Support**: Contact protocols.io support for API access and technical issues
- **Community**: Engage with protocols.io community for best practices

## Troubleshooting

**Authentication Issues:**
- Verify token is valid and not expired
- Check Authorization header format: `Bearer YOUR_TOKEN`
- Ensure appropriate token type (CLIENT vs OAUTH)

**Rate Limiting:**
- Implement exponential backoff for 429 errors
- Monitor request frequency
- Consider caching frequent requests

**Permission Errors:**
- Verify workspace/protocol access permissions
- Check user role in workspace
- Ensure protocol is not private if accessing without permission

**File Upload Failures:**
- Check file size against workspace limits
- Verify file type is supported
- Ensure multipart/form-data encoding is correct

For detailed troubleshooting guidance, refer to the specific reference files covering each capability area.

---

## Reference: Additional_Features

# Additional Features

## Overview

This document covers additional protocols.io API features including user profiles, recently published protocols, experiment records, and notifications.

## Base URL

All endpoints use the base URL: `https://protocols.io/api/v3`

## User Profile Management

### Get User Profile

Retrieve the authenticated user's profile information.

**Endpoint:** `GET /profile`

**Response includes:**
- User ID and username
- Full name
- Email address
- Affiliation/institution
- Bio and description
- Profile image URL
- Account creation date
- Protocol count and statistics

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/profile"
```

### Update User Profile

Update profile information.

**Endpoint:** `PATCH /profile`

**Request Body:**
- `first_name`: First name
- `last_name`: Last name
- `email`: Email address
- `affiliation`: Institution or organization
- `bio`: Profile bio/description
- `location`: Geographic location
- `website`: Personal or lab website URL
- `twitter`: Twitter handle
- `orcid`: ORCID identifier

**Example Request:**
```bash
curl -X PATCH \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "affiliation": "University of Example, Department of Biology",
    "bio": "Researcher specializing in CRISPR gene editing and molecular biology",
    "orcid": "0000-0001-2345-6789"
  }' \
  "https://protocols.io/api/v3/profile"
```

### Upload Profile Image

Update profile picture.

**Endpoint:** `POST /profile/image`

**Request Format**: `multipart/form-data`

**Form Parameters:**
- `image` (required): Image file (JPEG, PNG)

**Recommended specifications:**
- Minimum size: 200x200 pixels
- Aspect ratio: Square (1:1)
- Format: JPEG or PNG
- Max file size: 5 MB

## Recently Published Protocols

### Query Published Protocols

Discover recently published public protocols.

**Endpoint:** `GET /publications`

**Query Parameters:**
- `key`: Search keywords
- `category`: Filter by category
  - Example categories: `molecular-biology`, `cell-biology`, `biochemistry`, etc.
- `date_from`: Start date (ISO 8601 format: YYYY-MM-DD)
- `date_to`: End date
- `order_field`: Sort field (`published_on`, `title`, `views`)
- `order_dir`: Sort direction (`desc`, `asc`)
- `page_size`: Number of results per page (default: 10, max: 50)
- `page_id`: Page number for pagination

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/publications?category=molecular-biology&date_from=2025-01-01&order_field=published_on&order_dir=desc"
```

**Use Cases:**
- Discover trending protocols
- Monitor new publications in your field
- Find recently published protocols for specific techniques
- Track citation-worthy protocols

## Experiment Records

### Overview

Experiment records allow users to document individual runs or executions of a protocol, tracking what worked, what didn't, and any modifications made.

### Create Experiment Record

Document an execution of a protocol.

**Endpoint:** `POST /protocols/{protocol_id}/runs`

**Path Parameters:**
- `protocol_id`: The protocol's unique identifier

**Request Body:**
- `title` (required): Experiment run title
- `date`: Date of experiment execution (ISO 8601 format)
- `status`: Experiment outcome
  - `success`: Experiment succeeded
  - `partial`: Partially successful
  - `failed`: Experiment failed
- `notes`: Detailed notes about the experiment run
- `modifications`: Protocol modifications or deviations
- `results`: Summary of results
- `attachments`: File IDs for data files or images

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CRISPR Editing - HEK293 Cells - Trial 3",
    "date": "2025-10-20",
    "status": "success",
    "notes": "Successfully achieved 87% editing efficiency. Increased sgRNA concentration from 100nM to 150nM based on previous trials.",
    "modifications": "Extended incubation time in step 3 from 30 min to 45 min",
    "results": "Flow cytometry confirmed 87% GFP+ cells after 72h. Western blot showed complete knockout in positive population."
  }' \
  "https://protocols.io/api/v3/protocols/12345/runs"
```

### List Experiment Records

Retrieve all experiment records for a protocol.

**Endpoint:** `GET /protocols/{protocol_id}/runs`

**Query Parameters:**
- `status`: Filter by outcome (`success`, `partial`, `failed`)
- `date_from`: Start date
- `date_to`: End date
- `page_size`: Number of results per page
- `page_id`: Page number for pagination

### Update Experiment Record

**Endpoint:** `PATCH /protocols/{protocol_id}/runs/{run_id}`

**Request Body**: Same parameters as create, all optional

### Delete Experiment Record

**Endpoint:** `DELETE /protocols/{protocol_id}/runs/{run_id}`

**Use Cases:**
- Track reproducibility across multiple experiments
- Document troubleshooting and optimization
- Share successful modifications with collaborators
- Build institutional knowledge base
- Support lab notebook requirements

## Notifications

### Get User Notifications

Retrieve notifications for the authenticated user.

**Endpoint:** `GET /notifications`

**Query Parameters:**
- `type`: Filter by notification type
  - `comment`: New comments on your protocols
  - `mention`: You were mentioned in a comment
  - `protocol_update`: Protocol you follow was updated
  - `workspace`: Workspace activity
  - `publication`: Protocol was published
- `read`: Filter by read status
  - `true`: Only read notifications
  - `false`: Only unread notifications
  - Omit for all notifications
- `page_size`: Number of results per page (default: 20, max: 100)
- `page_id`: Page number for pagination

**Response includes:**
- Notification ID and type
- Message/description
- Related protocol/comment/workspace
- Timestamp
- Read status

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/notifications?read=false&type=comment"
```

### Mark Notification as Read

**Endpoint:** `PATCH /notifications/{notification_id}`

**Request Body:**
- `read`: Set to `true`

### Mark All Notifications as Read

**Endpoint:** `POST /notifications/mark-all-read`

### Delete Notification

**Endpoint:** `DELETE /notifications/{notification_id}`

## Organization Management

### Export Organization Data

Export all protocols and workspace data from an organization.

**Endpoint:** `GET /organizations/{organization_id}/export`

**Path Parameters:**
- `organization_id`: The organization's unique identifier

**Query Parameters:**
- `format`: Export format
  - `json`: JSON format with full metadata
  - `csv`: CSV format for spreadsheet import
  - `xml`: XML format
- `include_files`: Include associated files (`true`/`false`)
- `include_comments`: Include discussions (`true`/`false`)

**Response**: Download URL for export package

**Use Cases:**
- Institutional archival
- Compliance and audit requirements
- Migration to other systems
- Backup and disaster recovery
- Data analysis and reporting

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/organizations/12345/export?format=json&include_files=true&include_comments=true"
```

## Common Integration Patterns

### 1. Protocol Discovery and Import

Build a protocol discovery workflow:

```python
# Search for relevant protocols
response = requests.get(
    'https://protocols.io/api/v3/publications',
    headers={'Authorization': f'Bearer {token}'},
    params={'key': 'CRISPR', 'category': 'molecular-biology'}
)

# For each interesting protocol
for protocol in response.json()['items']:
    # Get full details
    details = requests.get(
        f'https://protocols.io/api/v3/protocols/{protocol["id"]}',
        headers={'Authorization': f'Bearer {token}'}
    )
    # Import to local system
    import_protocol(details.json())
```

### 2. Experiment Tracking

Track all protocol executions:

1. Execute protocol in lab
2. Document execution: `POST /protocols/{id}/runs`
3. Upload result files to workspace
4. Link files in experiment record
5. Analyze success rates across runs

### 3. Notification System Integration

Build custom notification system:

1. Poll for new notifications: `GET /notifications?read=false`
2. Process each notification type
3. Send to internal communication system
4. Mark as read: `PATCH /notifications/{id}`

### 4. Profile Synchronization

Keep profiles synchronized across systems:

1. Retrieve profile: `GET /profile`
2. Compare with internal system
3. Update discrepancies
4. Sync profile images and metadata

## API Response Formats

### Standard Response Structure

Most API responses follow this structure:

```json
{
  "status_code": 0,
  "status_message": "Success",
  "item": { /* single item data */ },
  "items": [ /* array of items */ ],
  "pagination": {
    "current_page": 0,
    "total_pages": 5,
    "page_size": 10,
    "total_items": 42
  }
}
```

### Error Response Structure

```json
{
  "status_code": 400,
  "status_message": "Bad Request",
  "error_message": "Missing required parameter: title",
  "error_details": {
    "field": "title",
    "issue": "required"
  }
}
```

## Best Practices

1. **Profile Completeness**
   - Complete all profile fields
   - Add ORCID for research attribution
   - Keep affiliation current

2. **Experiment Documentation**
   - Document all protocol executions
   - Include both successes and failures
   - Note all modifications
   - Attach relevant data files

3. **Notification Management**
   - Review notifications regularly
   - Enable relevant notification types
   - Disable notification types you don't need
   - Respond to comments promptly

4. **Publication Discovery**
   - Set up regular searches for your research area
   - Follow prolific authors in your field
   - Bookmark useful protocols
   - Cite protocols in publications

5. **Data Export**
   - Export organization data regularly
   - Test restore procedures
   - Store exports securely
   - Document export procedures

---

## Reference: Authentication

# Protocols.io Authentication

## Overview

The protocols.io API supports two types of access tokens for authentication, enabling access to both public and private content.

## Access Token Types

### 1. CLIENT_ACCESS_TOKEN

- **Purpose**: Enables access to public content and the private content of the client user
- **Use case**: When accessing your own protocols and public protocols
- **Scope**: Limited to the token owner's private content plus all public content

### 2. OAUTH_ACCESS_TOKEN

- **Purpose**: Grants access to specific users' private content plus all public content
- **Use case**: When building applications that need to access other users' content with their permission
- **Scope**: Full access to authorized user's private content plus all public content

## Authentication Header

All API requests must include an Authorization header:

```
Authorization: Bearer [ACCESS_TOKEN]
```

## OAuth Flow

### Step 1: Generate Authorization Link

Direct users to the authorization URL to grant access:

```
GET https://protocols.io/api/v3/oauth/authorize
```

**Parameters:**
- `client_id` (required): Your application's client ID
- `redirect_uri` (required): URL to redirect users after authorization
- `response_type` (required): Set to "code"
- `state` (optional but recommended): Random string to prevent CSRF attacks

**Example:**
```
https://protocols.io/api/v3/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&state=RANDOM_STRING
```

### Step 2: Exchange Authorization Code for Token

After user authorization, protocols.io redirects to your `redirect_uri` with an authorization code. Exchange this code for an access token:

```
POST https://protocols.io/api/v3/oauth/token
```

**Parameters:**
- `grant_type`: Set to "authorization_code"
- `code`: The authorization code received
- `client_id`: Your application's client ID
- `client_secret`: Your application's client secret
- `redirect_uri`: Must match the redirect_uri used in Step 1

**Response includes:**
- `access_token`: The OAuth access token to use for API requests
- `token_type`: "Bearer"
- `expires_in`: Token lifetime in seconds (typically 1 year)
- `refresh_token`: Token for refreshing the access token

### Step 3: Refresh Access Token

Before the access token expires (typically 1 year), use the refresh token to obtain a new access token:

```
POST https://protocols.io/api/v3/oauth/token
```

**Parameters:**
- `grant_type`: Set to "refresh_token"
- `refresh_token`: The refresh token received in Step 2
- `client_id`: Your application's client ID
- `client_secret`: Your application's client secret

## Rate Limits

Be aware of rate limiting when making API requests:

- **Standard endpoints**: 100 requests per minute per user
- **PDF endpoint** (`/view/[protocol-uri].pdf`):
  - Signed-in users: 5 requests per minute
  - Unsigned users: 3 requests per minute

## Best Practices

1. **Store tokens securely**: Never expose access tokens in client-side code or version control
2. **Handle token expiration**: Implement automatic token refresh before expiration
3. **Respect rate limits**: Implement exponential backoff for rate limit errors
4. **Use state parameter**: Always include a state parameter in OAuth flow for security
5. **Validate redirect_uri**: Ensure redirect URIs match exactly between authorization and token requests

---

## Reference: Discussions

# Discussions API

## Overview

The Discussions API enables collaborative commenting on protocols. Comments can be added at both the protocol level and the individual step level, with support for threaded replies, editing, and deletion.

## Base URL

All discussion endpoints use the base URL: `https://protocols.io/api/v3`

## Protocol-Level Comments

### List Protocol Comments

Retrieve all comments for a protocol.

**Endpoint:** `GET /protocols/{protocol_id}/comments`

**Path Parameters:**
- `protocol_id`: The protocol's unique identifier

**Query Parameters:**
- `page_size`: Number of results per page (default: 10, max: 50)
- `page_id`: Page number for pagination (starts at 0)

**Response includes:**
- Comment ID and content
- Author information (name, affiliation, avatar)
- Timestamp (created and modified)
- Reply count and thread structure

### Create Protocol Comment

Add a new comment to a protocol.

**Endpoint:** `POST /protocols/{protocol_id}/comments`

**Request Body:**
- `body` (required): Comment text (supports HTML or Markdown)
- `parent_comment_id` (optional): ID of parent comment for threaded replies

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "This protocol worked excellently for our CRISPR experiments. We achieved 85% editing efficiency."
  }' \
  "https://protocols.io/api/v3/protocols/12345/comments"
```

### Create Threaded Reply

To reply to an existing comment, include the parent comment ID:

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "What cell type did you use?",
    "parent_comment_id": 67890
  }' \
  "https://protocols.io/api/v3/protocols/12345/comments"
```

### Update Comment

Edit your own comment.

**Endpoint:** `PATCH /protocols/{protocol_id}/comments/{comment_id}`

**Request Body:**
- `body` (required): Updated comment text

**Authorization**: Only the comment author can edit their comments

### Delete Comment

Remove a comment.

**Endpoint:** `DELETE /protocols/{protocol_id}/comments/{comment_id}`

**Authorization**: Only the comment author can delete their comments

**Note**: Deleting a parent comment may affect the entire thread, depending on API implementation

## Step-Level Comments

### List Step Comments

Retrieve all comments for a specific protocol step.

**Endpoint:** `GET /protocols/{protocol_id}/steps/{step_id}/comments`

**Path Parameters:**
- `protocol_id`: The protocol's unique identifier
- `step_id`: The step's unique identifier

**Query Parameters:**
- `page_size`: Number of results per page
- `page_id`: Page number for pagination

### Create Step Comment

Add a comment to a specific step.

**Endpoint:** `POST /protocols/{protocol_id}/steps/{step_id}/comments`

**Request Body:**
- `body` (required): Comment text
- `parent_comment_id` (optional): ID of parent comment for replies

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "At this step, we found that increasing the incubation time to 2 hours improved results significantly."
  }' \
  "https://protocols.io/api/v3/protocols/12345/steps/67890/comments"
```

### Update Step Comment

**Endpoint:** `PATCH /protocols/{protocol_id}/steps/{step_id}/comments/{comment_id}`

**Request Body:**
- `body` (required): Updated comment text

### Delete Step Comment

**Endpoint:** `DELETE /protocols/{protocol_id}/steps/{step_id}/comments/{comment_id}`

## Common Use Cases

### 1. Discussion Thread Analysis

To analyze discussions around a protocol:

1. Retrieve protocol comments: `GET /protocols/{id}/comments`
2. For each step, retrieve step-specific comments
3. Build a discussion thread tree using `parent_comment_id`
4. Analyze feedback patterns and common issues

### 2. Collaborative Protocol Improvement

To gather feedback on a protocol:

1. Publish the protocol
2. Monitor new comments: `GET /protocols/{id}/comments`
3. Respond to questions with threaded replies
4. Update protocol based on feedback
5. Publish updated version with notes acknowledging contributors

### 3. Community Engagement

To engage with protocol users:

1. Set up monitoring for new comments on your protocols
2. Respond promptly to questions and issues
3. Use step-level comments to provide detailed clarifications
4. Create threaded discussions for complex topics

### 4. Protocol Troubleshooting

To document troubleshooting experiences:

1. Identify problematic steps in a protocol
2. Add step-level comments with specific issues encountered
3. Document solutions or workarounds
4. Create a discussion thread with other users experiencing similar issues

## Comment Formatting

Comments support rich text formatting:

- **HTML**: Use standard HTML tags for formatting
- **Markdown**: Use Markdown syntax for simpler formatting
- **Links**: Include URLs to related resources or publications
- **Mentions**: Reference other users (format may vary)

**Example with Markdown:**
```json
{
  "body": "## Important Note\n\nWe achieved better results with:\n\n- Increasing temperature to 37°C\n- Extending incubation to 2 hours\n- Using freshly prepared reagents\n\nSee our publication: [doi:10.xxxx/xxxxx](https://doi.org/...)"
}
```

## Best Practices

1. **Be specific**: When commenting on steps, reference specific parameters or conditions
2. **Provide context**: Include relevant experimental details (cell type, reagent batch, equipment)
3. **Use step-level comments**: Direct feedback to specific steps rather than protocol-level when appropriate
4. **Engage constructively**: Respond to questions and feedback promptly
5. **Update protocols**: Incorporate validated feedback into protocol updates
6. **Thread related discussions**: Use reply functionality to keep related comments together
7. **Document variations**: Share protocol modifications that worked in your hands

## Permissions and Privacy

- **Public protocols**: Anyone can comment on published public protocols
- **Private protocols**: Only collaborators with access can comment
- **Comment ownership**: Only comment authors can edit or delete their comments
- **Moderation**: Protocol authors may have additional moderation capabilities

## Error Handling

Common error responses:

- `400 Bad Request`: Invalid comment format or missing required fields
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: Insufficient permissions (e.g., trying to edit another user's comment)
- `404 Not Found`: Protocol, step, or comment not found
- `429 Too Many Requests`: Rate limit exceeded

## Notifications

Comments may trigger notifications:

- Protocol authors receive notifications for new comments
- Comment authors receive notifications for replies
- Users can manage notification preferences in their account settings

---

## Reference: File_Manager

# File Manager API

## Overview

The File Manager API enables file operations within protocols.io workspaces, including uploading files, organizing folders, searching content, and managing file lifecycle. This is useful for attaching data files, images, documents, and other resources to protocols.

## Base URL

All file manager endpoints use the base URL: `https://protocols.io/api/v3`

## Search and Browse

### Search Workspace Files

Search for files and folders within a workspace.

**Endpoint:** `GET /workspaces/{workspace_id}/files/search`

**Path Parameters:**
- `workspace_id`: The workspace's unique identifier

**Query Parameters:**
- `query`: Search keywords (searches filenames and metadata)
- `type`: Filter by type
  - `file`: Files only
  - `folder`: Folders only
  - `all`: Both files and folders (default)
- `folder_id`: Limit search to specific folder
- `page_size`: Number of results per page (default: 20, max: 100)
- `page_id`: Page number for pagination (starts at 0)

**Response includes:**
- File/folder ID and name
- File size and type
- Creation and modification dates
- File path in workspace
- Download URL (for files)

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces/12345/files/search?query=microscopy&type=file"
```

### List Folder Contents

Browse files and folders within a specific folder.

**Endpoint:** `GET /workspaces/{workspace_id}/folders/{folder_id}`

**Path Parameters:**
- `workspace_id`: The workspace's unique identifier
- `folder_id`: The folder's unique identifier (use `root` for workspace root)

**Query Parameters:**
- `order_by`: Sort field (`name`, `size`, `created`, `modified`)
- `order_dir`: Sort direction (`asc`, `desc`)
- `page_size`: Number of results per page
- `page_id`: Page number for pagination

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces/12345/folders/root?order_by=modified&order_dir=desc"
```

## File Upload

### Upload File

Upload a file to a workspace folder.

**Endpoint:** `POST /workspaces/{workspace_id}/files/upload`

**Request Format**: `multipart/form-data`

**Form Parameters:**
- `file` (required): The file to upload
- `folder_id`: Target folder ID (omit or use `root` for workspace root)
- `name`: Custom filename (optional, uses original filename if omitted)
- `description`: File description
- `tags`: Comma-separated tags

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/local/data.xlsx" \
  -F "folder_id=67890" \
  -F "description=Experimental results from trial #3" \
  -F "tags=experiment,data,2025" \
  "https://protocols.io/api/v3/workspaces/12345/files/upload"
```

### Upload Verification

After upload, verify the file was processed correctly.

**Endpoint:** `GET /workspaces/{workspace_id}/files/{file_id}/status`

**Response includes:**
- Upload status (`processing`, `complete`, `failed`)
- File metadata
- Any processing errors

## File Operations

### Download File

Download a file from the workspace.

**Endpoint:** `GET /workspaces/{workspace_id}/files/{file_id}/download`

**Path Parameters:**
- `workspace_id`: The workspace's unique identifier
- `file_id`: The file's unique identifier

**Response**: Binary file data with appropriate Content-Type header

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  -o "downloaded_file.xlsx" \
  "https://protocols.io/api/v3/workspaces/12345/files/67890/download"
```

### Get File Metadata

Retrieve file information without downloading.

**Endpoint:** `GET /workspaces/{workspace_id}/files/{file_id}`

**Response includes:**
- File name, size, and type
- Upload date and author
- Description and tags
- File path and location
- Download URL
- Sharing permissions

### Update File Metadata

Update file description, tags, or other metadata.

**Endpoint:** `PATCH /workspaces/{workspace_id}/files/{file_id}`

**Request Body:**
- `name`: New filename
- `description`: Updated description
- `tags`: Updated tags (comma-separated)
- `folder_id`: Move to different folder

**Example Request:**
```bash
curl -X PATCH \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Experimental results from trial #3 - REVISED",
    "tags": "experiment,data,2025,revised"
  }' \
  "https://protocols.io/api/v3/workspaces/12345/files/67890"
```

### Delete File

Move a file to trash (soft delete).

**Endpoint:** `DELETE /workspaces/{workspace_id}/files/{file_id}`

**Note**: Deleted files may be recoverable from trash for a limited time

### Restore File

Restore a deleted file from trash.

**Endpoint:** `POST /workspaces/{workspace_id}/files/{file_id}/restore`

## Folder Operations

### Create Folder

Create a new folder in the workspace.

**Endpoint:** `POST /workspaces/{workspace_id}/folders`

**Request Body:**
- `name` (required): Folder name
- `parent_folder_id`: Parent folder ID (omit for workspace root)
- `description`: Folder description

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "2025 Experiments",
    "parent_folder_id": "root",
    "description": "All experimental data from 2025"
  }' \
  "https://protocols.io/api/v3/workspaces/12345/folders"
```

### Rename Folder

**Endpoint:** `PATCH /workspaces/{workspace_id}/folders/{folder_id}`

**Request Body:**
- `name`: New folder name
- `description`: Updated description

### Delete Folder

Delete a folder and optionally its contents.

**Endpoint:** `DELETE /workspaces/{workspace_id}/folders/{folder_id}`

**Query Parameters:**
- `recursive`: Set to `true` to delete folder and all contents (default: `false`)

**Warning**: Recursive deletion cannot be easily undone

## Common Use Cases

### 1. Protocol Data Attachment

Attach experimental data files to protocols:

1. Upload data files: `POST /workspaces/{id}/files/upload`
2. Verify upload completion
3. Reference file IDs in protocol steps
4. Include download links in protocol description

**Example Workflow:**
```bash
# Upload the data file
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@results.csv" \
  -F "description=Results from protocol execution" \
  "https://protocols.io/api/v3/workspaces/12345/files/upload"

# Note the file_id from response, then reference in protocol
```

### 2. Workspace Organization

Organize files into logical folder structures:

1. Create folder hierarchy: `POST /workspaces/{id}/folders`
2. Upload files to appropriate folders
3. Use consistent naming conventions
4. Tag files for easy search

**Example Structure:**
```
Workspace Root
├── Protocols
│   ├── Published
│   └── Drafts
├── Data
│   ├── Raw
│   └── Processed
├── Images
│   ├── Microscopy
│   └── Gels
└── Documents
    ├── Papers
    └── Presentations
```

### 3. File Search and Discovery

Find files across workspace:

1. Search by keywords: `GET /workspaces/{id}/files/search?query=keywords`
2. Filter by type and date
3. Download relevant files
4. Update metadata for better organization

### 4. Batch File Upload

Upload multiple related files:

1. Create target folder
2. For each file:
   - Upload file
   - Verify upload status
   - Add consistent tags
3. Create index or manifest file listing all uploads

### 5. Data Backup and Export

Export workspace files for backup:

1. List all folders: `GET /workspaces/{id}/folders/root`
2. For each folder, list files
3. Download all files: `GET /workspaces/{id}/files/{file_id}/download`
4. Maintain folder structure locally
5. Store metadata separately for restoration

### 6. File Versioning

Manage file versions manually:

1. Upload new version with versioned name (e.g., `data_v2.csv`)
2. Update previous version metadata to indicate superseded
3. Maintain version history in folder structure
4. Reference specific versions in protocols

## Supported File Types

Protocols.io supports various file types:

**Data Files:**
- Spreadsheets: `.xlsx`, `.xls`, `.csv`, `.tsv`
- Statistical data: `.rds`, `.rdata`, `.sav`, `.dta`
- Plain text: `.txt`, `.log`, `.json`, `.xml`

**Images:**
- Common formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tif`, `.tiff`
- Scientific: `.czi`, `.nd2`, `.lsm` (may require special handling)

**Documents:**
- PDF: `.pdf`
- Word: `.docx`, `.doc`
- PowerPoint: `.pptx`, `.ppt`

**Code and Scripts:**
- Python: `.py`, `.ipynb`
- R: `.r`, `.rmd`
- Shell: `.sh`, `.bash`

**Multimedia:**
- Video: `.mp4`, `.avi`, `.mov`
- Audio: `.mp3`, `.wav`

**Archives:**
- Compressed: `.zip`, `.tar.gz`, `.7z`

**File Size Limits:**
- Standard files: Check workspace limits (typically 100 MB - 1 GB)
- Large files: May require chunked upload or special handling

## Best Practices

1. **File Naming**
   - Use descriptive, consistent naming conventions
   - Include dates in ISO format (YYYY-MM-DD)
   - Avoid special characters and spaces (use underscores)
   - Example: `experiment_results_2025-10-26.csv`

2. **Organization**
   - Create logical folder hierarchy
   - Group related files together
   - Separate raw data from processed results
   - Keep protocol-specific files in dedicated folders

3. **Metadata**
   - Add detailed descriptions
   - Tag files consistently
   - Include version information
   - Document processing steps

4. **Storage Management**
   - Regularly review and archive old files
   - Delete unnecessary duplicates
   - Compress large datasets
   - Monitor workspace storage limits

5. **Collaboration**
   - Use clear file names for team members
   - Document file purposes in descriptions
   - Maintain consistent folder structures
   - Communicate major organizational changes

6. **Security**
   - Avoid uploading sensitive data without proper permissions
   - Be aware of workspace visibility settings
   - Use appropriate access controls
   - Regularly audit file access

## Error Handling

Common error responses:

- `400 Bad Request`: Invalid file format or parameters
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: Insufficient workspace permissions
- `404 Not Found`: File or folder not found
- `413 Payload Too Large`: File exceeds size limit
- `422 Unprocessable Entity`: File validation failed
- `429 Too Many Requests`: Rate limit exceeded
- `507 Insufficient Storage`: Workspace storage limit reached

## Performance Considerations

1. **Large Files**
   - Consider chunked upload for files > 100 MB
   - Use compression for large datasets
   - Upload during off-peak hours if possible

2. **Batch Operations**
   - Implement retry logic for failed uploads
   - Use exponential backoff for rate limits
   - Process uploads in parallel where possible

3. **Download Optimization**
   - Cache frequently accessed files locally
   - Use streaming for large file downloads
   - Implement resume capability for interrupted downloads

---

## Reference: Protocols_Api

# Protocols API

## Overview

The Protocols API is the core functionality of protocols.io, supporting the complete protocol lifecycle from creation to publication. This includes searching, creating, updating, managing steps, handling materials, bookmarking, and generating PDFs.

## Base URL

All protocol endpoints use the base URL: `https://protocols.io/api/v3`

## Content Format Parameter

Many endpoints support a `content_format` parameter to specify how content is returned:

- `json`: Draft.js JSON format (default)
- `html`: HTML format
- `markdown`: Markdown format

Include this as a query parameter: `?content_format=html`

## List and Search Operations

### List Protocols

Retrieve protocols with filtering and pagination.

**Endpoint:** `GET /protocols`

**Query Parameters:**
- `filter`: Filter type
  - `public`: Public protocols only
  - `private`: Your private protocols
  - `shared`: Protocols shared with you
  - `user_public`: Another user's public protocols
- `key`: Search keywords in protocol title, description, and content
- `order_field`: Sort field (`activity`, `created_on`, `modified_on`, `name`, `id`)
- `order_dir`: Sort direction (`desc`, `asc`)
- `page_size`: Number of results per page (default: 10, max: 50)
- `page_id`: Page number for pagination (starts at 0)
- `fields`: Comma-separated list of fields to return
- `content_format`: Content format (`json`, `html`, `markdown`)

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/protocols?filter=public&key=CRISPR&page_size=20&content_format=html"
```

### Search by DOI

Retrieve a protocol by its DOI.

**Endpoint:** `GET /protocols/{doi}`

**Path Parameters:**
- `doi`: The protocol DOI (e.g., `dx.doi.org/10.17504/protocols.io.xxxxx`)

## Retrieve Protocol Details

### Get Protocol by ID

**Endpoint:** `GET /protocols/{protocol_id}`

**Path Parameters:**
- `protocol_id`: The protocol's unique identifier

**Query Parameters:**
- `content_format`: Content format (`json`, `html`, `markdown`)

**Response includes:**
- Protocol metadata (title, authors, description, DOI)
- All protocol steps with content
- Materials and reagents
- Guidelines and warnings
- Version information
- Publication status

## Create and Update Protocols

### Create New Protocol

**Endpoint:** `POST /protocols`

**Request Body Parameters:**
- `title` (required): Protocol title
- `description`: Protocol description
- `tags`: Array of tag strings
- `vendor_name`: Vendor/company name
- `vendor_link`: Vendor website URL
- `warning`: Warning or safety message
- `guidelines`: Usage guidelines
- `manuscript_citation`: Citation for related manuscript
- `link`: External link to related resource

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CRISPR Gene Editing Protocol",
    "description": "Comprehensive protocol for CRISPR-Cas9 mediated gene editing",
    "tags": ["CRISPR", "gene editing", "molecular biology"]
  }' \
  "https://protocols.io/api/v3/protocols"
```

### Update Protocol

**Endpoint:** `PATCH /protocols/{protocol_id}`

**Path Parameters:**
- `protocol_id`: The protocol's unique identifier

**Request Body**: Same parameters as create, all optional

## Protocol Steps Management

### Create Protocol Step

**Endpoint:** `POST /protocols/{protocol_id}/steps`

**Request Body Parameters:**
- `title` (required): Step title
- `description`: Step description (HTML, Markdown, or Draft.js JSON)
- `duration`: Step duration in seconds
- `temperature`: Temperature setting
- `components`: Array of materials/reagents used
- `software`: Software or tools required
- `commands`: Commands to execute
- `expected_result`: Expected outcome description

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare sgRNA",
    "description": "Design and synthesize single guide RNA (sgRNA) targeting your gene of interest",
    "duration": 3600,
    "temperature": 25
  }' \
  "https://protocols.io/api/v3/protocols/12345/steps"
```

### Update Protocol Step

**Endpoint:** `PATCH /protocols/{protocol_id}/steps/{step_id}`

**Parameters**: Same as create step, all optional

### Delete Protocol Step

**Endpoint:** `DELETE /protocols/{protocol_id}/steps/{step_id}`

### Reorder Steps

**Endpoint:** `POST /protocols/{protocol_id}/steps/reorder`

**Request Body:**
- `step_order`: Array of step IDs in desired order

## Materials and Reagents

### Get Protocol Materials

Retrieve all materials and reagents used in a protocol.

**Endpoint:** `GET /protocols/{protocol_id}/materials`

**Response includes:**
- Reagent names and descriptions
- Catalog numbers
- Vendor information
- Concentrations and amounts
- Links to product pages

## Publishing and DOI

### Publish Protocol

Issue a DOI and make the protocol publicly available.

**Endpoint:** `POST /protocols/{protocol_id}/publish`

**Request Body Parameters:**
- `version_notes`: Description of changes in this version
- `publish_type`: Publication type
  - `new`: First publication
  - `update`: Update to existing published protocol

**Important Notes:**
- Once published, protocols receive a permanent DOI
- Published protocols cannot be deleted, only updated with new versions
- Published protocols are publicly accessible

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version_notes": "Initial publication",
    "publish_type": "new"
  }' \
  "https://protocols.io/api/v3/protocols/12345/publish"
```

## Bookmarks

### Add Bookmark

Add a protocol to your bookmarks for quick access.

**Endpoint:** `POST /protocols/{protocol_id}/bookmarks`

### Remove Bookmark

**Endpoint:** `DELETE /protocols/{protocol_id}/bookmarks`

### List Bookmarked Protocols

**Endpoint:** `GET /bookmarks`

## PDF Export

### Generate Protocol PDF

Generate a formatted PDF version of a protocol.

**Endpoint:** `GET /view/{protocol_uri}.pdf`

**Query Parameters:**
- `compact`: Set to `1` for compact view without large spacing

**Rate Limits:**
- Signed-in users: 5 requests per minute
- Unsigned users: 3 requests per minute

**Example:**
```
https://protocols.io/api/v3/view/crispr-protocol-abc123.pdf?compact=1
```

## Common Use Cases

### 1. Import Existing Protocol

To import and work with an existing protocol:

1. Search for the protocol using keywords or DOI
2. Retrieve full protocol details with `/protocols/{protocol_id}`
3. Extract steps, materials, and metadata for local use

### 2. Create New Protocol from Scratch

To create a new protocol:

1. Create protocol with title and description: `POST /protocols`
2. Add steps sequentially: `POST /protocols/{id}/steps`
3. Review and test the protocol
4. Publish when ready: `POST /protocols/{id}/publish`

### 3. Update Published Protocol

To update an already-published protocol:

1. Retrieve current version: `GET /protocols/{protocol_id}`
2. Make necessary updates: `PATCH /protocols/{protocol_id}`
3. Update or add steps as needed
4. Publish new version: `POST /protocols/{protocol_id}/publish` with `publish_type: "update"`

### 4. Clone and Modify Protocol

To create a modified version of an existing protocol:

1. Retrieve original protocol details
2. Create new protocol with modified metadata
3. Copy and modify steps from original
4. Publish as new protocol

## Error Handling

Common error responses:

- `400 Bad Request`: Invalid parameters or request format
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: Insufficient permissions for the operation
- `404 Not Found`: Protocol or resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side error

Implement retry logic with exponential backoff for `429` and `500` errors.

---

## Reference: Workspaces

# Workspaces API

## Overview

Workspaces in protocols.io enable team collaboration by organizing protocols, managing members, and controlling access permissions. The Workspaces API allows you to list workspaces, manage memberships, and access workspace-specific protocols.

## Base URL

All workspace endpoints use the base URL: `https://protocols.io/api/v3`

## Workspace Operations

### List User Workspaces

Retrieve all workspaces the authenticated user has access to.

**Endpoint:** `GET /workspaces`

**Query Parameters:**
- `page_size`: Number of results per page (default: 10, max: 50)
- `page_id`: Page number for pagination (starts at 0)

**Response includes:**
- Workspace ID and name
- Workspace type (personal, group, institutional)
- Member count
- Access level (owner, admin, member, viewer)
- Creation date

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces"
```

### Get Workspace Details

Retrieve detailed information about a specific workspace.

**Endpoint:** `GET /workspaces/{workspace_id}`

**Path Parameters:**
- `workspace_id`: The workspace's unique identifier

**Response includes:**
- Complete workspace metadata
- Member list with roles
- Workspace settings and permissions
- Protocol count and categories

## Workspace Membership

### List Workspace Members

Retrieve all members of a workspace.

**Endpoint:** `GET /workspaces/{workspace_id}/members`

**Query Parameters:**
- `page_size`: Number of results per page
- `page_id`: Page number for pagination

**Response includes:**
- Member name and email
- Role (owner, admin, member, viewer)
- Join date
- Activity status

### Request Workspace Access

Request to join a workspace.

**Endpoint:** `POST /workspaces/{workspace_id}/join-request`

**Request Body:**
- `message` (optional): Message to workspace admins explaining the request

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am collaborating with Dr. Smith on the CRISPR project and would like to access the shared protocols."
  }' \
  "https://protocols.io/api/v3/workspaces/12345/join-request"
```

### Join Public Workspace

Directly join a public workspace without approval.

**Endpoint:** `POST /workspaces/{workspace_id}/join`

**Note**: Only available for workspaces configured to allow public joining

## Workspace Protocols

### List Workspace Protocols

Retrieve all protocols in a workspace.

**Endpoint:** `GET /workspaces/{workspace_id}/protocols`

**Query Parameters:**
- `filter`: Filter protocols
  - `all`: All protocols in the workspace
  - `own`: Only protocols you created
  - `shared`: Protocols shared with you
- `key`: Search keywords
- `order_field`: Sort field (`activity`, `created_on`, `modified_on`, `name`)
- `order_dir`: Sort direction (`desc`, `asc`)
- `page_size`: Number of results per page
- `page_id`: Page number for pagination
- `content_format`: Content format (`json`, `html`, `markdown`)

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/workspaces/12345/protocols?filter=all&order_field=modified_on&order_dir=desc"
```

### Create Protocol in Workspace

Create a new protocol within a specific workspace.

**Endpoint:** `POST /workspaces/{workspace_id}/protocols`

**Request Body**: Same parameters as standard protocol creation (see protocols_api.md)

**Note**: The protocol will be created within the workspace and inherit workspace permissions

## Workspace Types and Permissions

### Workspace Types

1. **Personal Workspace**
   - Default workspace for individual users
   - Private by default
   - Can share specific protocols

2. **Group Workspace**
   - Collaborative workspace for teams
   - Shared access for all members
   - Role-based permissions

3. **Institutional Workspace**
   - Organization-wide workspace
   - Often includes branding
   - Centralized protocol management

### Permission Levels

1. **Owner**
   - Full workspace control
   - Manage members and permissions
   - Delete workspace

2. **Admin**
   - Manage protocols and members
   - Configure workspace settings
   - Cannot delete workspace

3. **Member**
   - Create and edit protocols
   - View all workspace protocols
   - Comment and collaborate

4. **Viewer**
   - View-only access
   - Can comment on protocols
   - Cannot create or edit

## Common Use Cases

### 1. Lab Protocol Repository

Organize lab protocols in a shared workspace:

1. Create or join lab workspace: `GET /workspaces`
2. List existing protocols: `GET /workspaces/{id}/protocols`
3. Create new protocols: `POST /workspaces/{id}/protocols`
4. Invite lab members: Share workspace invitation
5. Organize by categories or tags

### 2. Collaborative Protocol Development

Develop protocols with team members:

1. Identify target workspace: `GET /workspaces`
2. Create draft protocol in workspace
3. Share with team members automatically via workspace
4. Gather feedback through comments
5. Iterate and publish final version

### 3. Cross-Institutional Collaboration

Work with external collaborators:

1. Create or identify shared workspace
2. Request access: `POST /workspaces/{id}/join-request`
3. Once approved, access shared protocols
4. Contribute new protocols or updates
5. Maintain institutional protocol copies in personal workspace

### 4. Protocol Migration

Move protocols between workspaces:

1. List source workspace protocols: `GET /workspaces/{source_id}/protocols`
2. For each protocol, retrieve full details
3. Create protocol in target workspace: `POST /workspaces/{target_id}/protocols`
4. Copy all steps and metadata
5. Update references and links

### 5. Workspace Audit

Review workspace activity and content:

1. List all workspaces: `GET /workspaces`
2. For each workspace, get member list
3. Retrieve protocol lists with activity dates
4. Identify inactive or outdated protocols
5. Generate activity reports

## Workspace Management Best Practices

1. **Organization**
   - Use consistent naming conventions
   - Tag protocols by project or category
   - Maintain workspace directory or index

2. **Access Control**
   - Review member list regularly
   - Assign appropriate permission levels
   - Remove inactive members

3. **Protocol Standards**
   - Establish workspace-wide protocol templates
   - Define required metadata fields
   - Implement quality review process

4. **Collaboration**
   - Communicate workspace guidelines to members
   - Encourage protocol documentation
   - Facilitate knowledge sharing

5. **Backup and Archival**
   - Regularly export workspace protocols
   - Maintain protocol version history
   - Archive completed projects

## Organizations and Workspaces

Organizations are higher-level entities that can contain multiple workspaces.

### Export Organization Data

**Endpoint:** `GET /organizations/{org_id}/export`

**Use case**: Bulk export of all protocols and workspace data for institutional archives or backups

## Notifications and Activity

Workspace activity may trigger notifications:

- New protocols added to workspace
- Protocol updates by team members
- New comments on workspace protocols
- Member joins or leaves workspace
- Permission changes

Configure notification preferences in account settings.

## Error Handling

Common error responses:

- `400 Bad Request`: Invalid workspace ID or parameters
- `401 Unauthorized`: Missing or invalid access token
- `403 Forbidden`: Insufficient workspace permissions
- `404 Not Found`: Workspace not found or no access
- `429 Too Many Requests`: Rate limit exceeded

## Integration Considerations

When integrating workspace functionality:

1. **Cache workspace list**: Avoid repeated workspace list calls
2. **Respect permissions**: Check user's role before attempting operations
3. **Handle join requests**: Implement workflow for workspace access approval
4. **Sync regularly**: Update local workspace data periodically
5. **Support offline access**: Cache protocols for offline work with sync on reconnection
