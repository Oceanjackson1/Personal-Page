---
title: "Benchling 集成"
description: "Benchling 研发平台集成，访问 DNA、蛋白质注册表和实验室工作流"
category: "research"
source: "community"
author: "Community"
tags: ["benchling", "integration"]
date: 2026-03-20
---

# Benchling Integration

## Overview

Benchling is a cloud platform for life sciences R&D. Access registry entities (DNA, proteins), inventory, electronic lab notebooks, and workflows programmatically via Python SDK and REST API.

## When to Use This Skill

This skill should be used when:
- Working with Benchling's Python SDK or REST API
- Managing biological sequences (DNA, RNA, proteins) and registry entities
- Automating inventory operations (samples, containers, locations, transfers)
- Creating or querying electronic lab notebook entries
- Building workflow automations or Benchling Apps
- Syncing data between Benchling and external systems
- Querying the Benchling Data Warehouse for analytics
- Setting up event-driven integrations with AWS EventBridge

## Core Capabilities

### 1. Authentication & Setup

**Python SDK Installation:**
```python
# Stable release
uv pip install benchling-sdk
# or with Poetry
poetry add benchling-sdk
```

**Authentication Methods:**

API Key Authentication (recommended for scripts):
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key")
)
```

OAuth Client Credentials (for apps):
```python
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

**Key Points:**
- API keys are obtained from Profile Settings in Benchling
- Store credentials securely (use environment variables or password managers)
- All API requests require HTTPS
- Authentication permissions mirror user permissions in the UI

For detailed authentication information including OIDC and security best practices, refer to `references/authentication.md`.

### 2. Registry & Entity Management

Registry entities include DNA sequences, RNA sequences, AA sequences, custom entities, and mixtures. The SDK provides typed classes for creating and managing these entities.

**Creating DNA Sequences:**
```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",  # optional
        fields=benchling.models.fields({"gene_name": "GFP"})
    )
)
```

**Registry Registration:**

To register an entity directly upon creation:
```python
sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",  # Registry to register in
        naming_strategy="NEW_IDS"  # or "IDS_FROM_NAMES"
    )
)
```

**Important:** Use either `entity_registry_id` OR `naming_strategy`, never both.

**Updating Entities:**
```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="Updated Plasmid Name",
        fields=benchling.models.fields({"gene_name": "mCherry"})
    )
)
```

Unspecified fields remain unchanged, allowing partial updates.

**Listing and Pagination:**
```python
# List all DNA sequences (returns a generator)
sequences = benchling.dna_sequences.list()
for page in sequences:
    for seq in page:
        print(f"{seq.name} ({seq.id})")

# Check total count
total = sequences.estimated_count()
```

**Key Operations:**
- Create: `benchling.<entity_type>.create()`
- Read: `benchling.<entity_type>.get(id)` or `.list()`
- Update: `benchling.<entity_type>.update(id, update_object)`
- Archive: `benchling.<entity_type>.archive(id)`

Entity types: `dna_sequences`, `rna_sequences`, `aa_sequences`, `custom_entities`, `mixtures`

For comprehensive SDK reference and advanced patterns, refer to `references/sdk_reference.md`.

### 3. Inventory Management

Manage physical samples, containers, boxes, and locations within the Benchling inventory system.

**Creating Containers:**
```python
from benchling_sdk.models import ContainerCreate

container = benchling.containers.create(
    ContainerCreate(
        name="Sample Tube 001",
        schema_id="cont_schema_abc123",
        parent_storage_id="box_abc123",  # optional
        fields=benchling.models.fields({"concentration": "100 ng/μL"})
    )
)
```

**Managing Boxes:**
```python
from benchling_sdk.models import BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Freezer Box A1",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_abc123"
    )
)
```

**Transferring Items:**
```python
# Transfer a container to a new location
transfer = benchling.containers.transfer(
    container_id="cont_abc123",
    destination_id="box_xyz789"
)
```

**Key Inventory Operations:**
- Create containers, boxes, locations, plates
- Update inventory item properties
- Transfer items between locations
- Check in/out items
- Batch operations for bulk transfers

### 4. Notebook & Documentation

Interact with electronic lab notebook (ELN) entries, protocols, and templates.

**Creating Notebook Entries:**
```python
from benchling_sdk.models import EntryCreate

entry = benchling.entries.create(
    EntryCreate(
        name="Experiment 2025-10-20",
        folder_id="fld_abc123",
        schema_id="entry_schema_abc123",
        fields=benchling.models.fields({"objective": "Test gene expression"})
    )
)
```

**Linking Entities to Entries:**
```python
# Add references to entities in an entry
entry_link = benchling.entry_links.create(
    entry_id="entry_abc123",
    entity_id="seq_xyz789"
)
```

**Key Notebook Operations:**
- Create and update lab notebook entries
- Manage entry templates
- Link entities and results to entries
- Export entries for documentation

### 5. Workflows & Automation

Automate laboratory processes using Benchling's workflow system.

**Creating Workflow Tasks:**
```python
from benchling_sdk.models import WorkflowTaskCreate

task = benchling.workflow_tasks.create(
    WorkflowTaskCreate(
        name="PCR Amplification",
        workflow_id="wf_abc123",
        assignee_id="user_abc123",
        fields=benchling.models.fields({"template": "seq_abc123"})
    )
)
```

**Updating Task Status:**
```python
from benchling_sdk.models import WorkflowTaskUpdate

updated_task = benchling.workflow_tasks.update(
    task_id="task_abc123",
    workflow_task=WorkflowTaskUpdate(
        status_id="status_complete_abc123"
    )
)
```

**Asynchronous Operations:**

Some operations are asynchronous and return tasks:
```python
# Wait for task completion
from benchling_sdk.helpers.tasks import wait_for_task

result = wait_for_task(
    benchling,
    task_id="task_abc123",
    interval_wait_seconds=2,
    max_wait_seconds=300
)
```

**Key Workflow Operations:**
- Create and manage workflow tasks
- Update task statuses and assignments
- Execute bulk operations asynchronously
- Monitor task progress

### 6. Events & Integration

Subscribe to Benchling events for real-time integrations using AWS EventBridge.

**Event Types:**
- Entity creation, update, archive
- Inventory transfers
- Workflow task status changes
- Entry creation and updates
- Results registration

**Integration Pattern:**
1. Configure event routing to AWS EventBridge in Benchling settings
2. Create EventBridge rules to filter events
3. Route events to Lambda functions or other targets
4. Process events and update external systems

**Use Cases:**
- Sync Benchling data to external databases
- Trigger downstream processes on workflow completion
- Send notifications on entity changes
- Audit trail logging

Refer to Benchling's event documentation for event schemas and configuration.

### 7. Data Warehouse & Analytics

Query historical Benchling data using SQL through the Data Warehouse.

**Access Method:**
The Benchling Data Warehouse provides SQL access to Benchling data for analytics and reporting. Connect using standard SQL clients with provided credentials.

**Common Queries:**
- Aggregate experimental results
- Analyze inventory trends
- Generate compliance reports
- Export data for external analysis

**Integration with Analysis Tools:**
- Jupyter notebooks for interactive analysis
- BI tools (Tableau, Looker, PowerBI)
- Custom dashboards

## Best Practices

### Error Handling

The SDK automatically retries failed requests:
```python
# Automatic retry for 429, 502, 503, 504 status codes
# Up to 5 retries with exponential backoff
# Customize retry behavior if needed
from benchling_sdk.retry import RetryStrategy

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=RetryStrategy(max_retries=3)
)
```

### Pagination Efficiency

Use generators for memory-efficient pagination:
```python
# Generator-based iteration
for page in benchling.dna_sequences.list():
    for sequence in page:
        process(sequence)

# Check estimated count without loading all pages
total = benchling.dna_sequences.list().estimated_count()
```

### Schema Fields Helper

Use the `fields()` helper for custom schema fields:
```python
# Convert dict to Fields object
custom_fields = benchling.models.fields({
    "concentration": "100 ng/μL",
    "date_prepared": "2025-10-20",
    "notes": "High quality prep"
})
```

### Forward Compatibility

The SDK handles unknown enum values and types gracefully:
- Unknown enum values are preserved
- Unrecognized polymorphic types return `UnknownType`
- Allows working with newer API versions

### Security Considerations

- Never commit API keys to version control
- Use environment variables for credentials
- Rotate keys if compromised
- Grant minimal necessary permissions for apps
- Use OAuth for multi-user scenarios

## Resources

### references/

Detailed reference documentation for in-depth information:

- **authentication.md** - Comprehensive authentication guide including OIDC, security best practices, and credential management
- **sdk_reference.md** - Detailed Python SDK reference with advanced patterns, examples, and all entity types
- **api_endpoints.md** - REST API endpoint reference for direct HTTP calls without the SDK

Load these references as needed for specific integration requirements.

### scripts/

This skill currently includes example scripts that can be removed or replaced with custom automation scripts for your specific Benchling workflows.

## Common Use Cases

**1. Bulk Entity Import:**
```python
# Import multiple sequences from FASTA file
from Bio import SeqIO

for record in SeqIO.parse("sequences.fasta", "fasta"):
    benchling.dna_sequences.create(
        DnaSequenceCreate(
            name=record.id,
            bases=str(record.seq),
            is_circular=False,
            folder_id="fld_abc123"
        )
    )
```

**2. Inventory Audit:**
```python
# List all containers in a specific location
containers = benchling.containers.list(
    parent_storage_id="box_abc123"
)

for page in containers:
    for container in page:
        print(f"{container.name}: {container.barcode}")
```

**3. Workflow Automation:**
```python
# Update all pending tasks for a workflow
tasks = benchling.workflow_tasks.list(
    workflow_id="wf_abc123",
    status="pending"
)

for page in tasks:
    for task in page:
        # Perform automated checks
        if auto_validate(task):
            benchling.workflow_tasks.update(
                task_id=task.id,
                workflow_task=WorkflowTaskUpdate(
                    status_id="status_complete"
                )
            )
```

**4. Data Export:**
```python
# Export all sequences with specific properties
sequences = benchling.dna_sequences.list()
export_data = []

for page in sequences:
    for seq in page:
        if seq.schema_id == "target_schema_id":
            export_data.append({
                "id": seq.id,
                "name": seq.name,
                "bases": seq.bases,
                "length": len(seq.bases)
            })

# Save to CSV or database
import csv
with open("sequences.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
    writer.writeheader()
    writer.writerows(export_data)
```

## Additional Resources

- **Official Documentation:** https://docs.benchling.com
- **Python SDK Reference:** https://benchling.com/sdk-docs/
- **API Reference:** https://benchling.com/api/reference
- **Support:** [email protected]

---

## Reference: Api_Endpoints

# Benchling REST API Endpoints Reference

## Base URL

All API requests use the base URL format:
```
https://{tenant}.benchling.com/api/v2
```

Replace `{tenant}` with your Benchling tenant name.

## API Versioning

Current API version: `v2` (2025-10-07)

The API version is specified in the URL path. Benchling maintains backward compatibility within a major version.

## Authentication

All requests require authentication via HTTP headers:

**API Key (Basic Auth):**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -u "your_api_key:"
```

**OAuth Bearer Token:**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer your_access_token"
```

## Common Headers

```
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
```

## Response Format

All responses follow a consistent JSON structure:

**Single Resource:**
```json
{
  "id": "seq_abc123",
  "name": "My Sequence",
  "bases": "ATCGATCG",
  ...
}
```

**List Response:**
```json
{
  "results": [
    {"id": "seq_1", "name": "Sequence 1"},
    {"id": "seq_2", "name": "Sequence 2"}
  ],
  "nextToken": "token_for_next_page"
}
```

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `pageSize`: Number of items per page (default: 50, max: 100)
- `nextToken`: Token from previous response for next page

**Example:**
```bash
curl -X GET \
  "https://your-tenant.benchling.com/api/v2/dna-sequences?pageSize=50&nextToken=abc123"
```

## Error Responses

**Format:**
```json
{
  "error": {
    "type": "NotFoundError",
    "message": "DNA sequence not found",
    "userMessage": "The requested sequence does not exist or you don't have access"
  }
}
```

**Common Status Codes:**
- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Missing or invalid credentials
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Core Endpoints

### DNA Sequences

**List DNA Sequences:**
```http
GET /api/v2/dna-sequences

Query Parameters:
- pageSize: integer (default: 50, max: 100)
- nextToken: string
- folderId: string
- schemaId: string
- name: string (filter by name)
- modifiedAt: string (ISO 8601 date)
```

**Get DNA Sequence:**
```http
GET /api/v2/dna-sequences/{sequenceId}
```

**Create DNA Sequence:**
```http
POST /api/v2/dna-sequences

Body:
{
  "name": "My Plasmid",
  "bases": "ATCGATCG",
  "isCircular": true,
  "folderId": "fld_abc123",
  "schemaId": "ts_abc123",
  "fields": {
    "gene_name": {"value": "GFP"},
    "resistance": {"value": "Kanamycin"}
  },
  "entityRegistryId": "src_abc123",  // optional for registration
  "namingStrategy": "NEW_IDS"        // optional for registration
}
```

**Update DNA Sequence:**
```http
PATCH /api/v2/dna-sequences/{sequenceId}

Body:
{
  "name": "Updated Plasmid",
  "fields": {
    "gene_name": {"value": "mCherry"}
  }
}
```

**Archive DNA Sequence:**
```http
POST /api/v2/dna-sequences:archive

Body:
{
  "dnaSequenceIds": ["seq_abc123"],
  "reason": "Deprecated construct"
}
```

### RNA Sequences

**List RNA Sequences:**
```http
GET /api/v2/rna-sequences
```

**Get RNA Sequence:**
```http
GET /api/v2/rna-sequences/{sequenceId}
```

**Create RNA Sequence:**
```http
POST /api/v2/rna-sequences

Body:
{
  "name": "gRNA-001",
  "bases": "AUCGAUCG",
  "folderId": "fld_abc123",
  "fields": {
    "target_gene": {"value": "TP53"}
  }
}
```

**Update RNA Sequence:**
```http
PATCH /api/v2/rna-sequences/{sequenceId}
```

**Archive RNA Sequence:**
```http
POST /api/v2/rna-sequences:archive
```

### Amino Acid (Protein) Sequences

**List AA Sequences:**
```http
GET /api/v2/aa-sequences
```

**Get AA Sequence:**
```http
GET /api/v2/aa-sequences/{sequenceId}
```

**Create AA Sequence:**
```http
POST /api/v2/aa-sequences

Body:
{
  "name": "GFP Protein",
  "aminoAcids": "MSKGEELFTGVVPILVELDGDVNGHKF",
  "folderId": "fld_abc123"
}
```

### Custom Entities

**List Custom Entities:**
```http
GET /api/v2/custom-entities

Query Parameters:
- schemaId: string (required to filter by type)
- pageSize: integer
- nextToken: string
```

**Get Custom Entity:**
```http
GET /api/v2/custom-entities/{entityId}
```

**Create Custom Entity:**
```http
POST /api/v2/custom-entities

Body:
{
  "name": "HEK293T-Clone5",
  "schemaId": "ts_cellline_abc",
  "folderId": "fld_abc123",
  "fields": {
    "passage_number": {"value": "15"},
    "mycoplasma_test": {"value": "Negative"}
  }
}
```

**Update Custom Entity:**
```http
PATCH /api/v2/custom-entities/{entityId}

Body:
{
  "fields": {
    "passage_number": {"value": "16"}
  }
}
```

### Mixtures

**List Mixtures:**
```http
GET /api/v2/mixtures
```

**Create Mixture:**
```http
POST /api/v2/mixtures

Body:
{
  "name": "LB-Amp Media",
  "folderId": "fld_abc123",
  "schemaId": "ts_mixture_abc",
  "ingredients": [
    {
      "componentEntityId": "ent_lb_base",
      "amount": {"value": "1000", "units": "mL"}
    },
    {
      "componentEntityId": "ent_ampicillin",
      "amount": {"value": "100", "units": "mg"}
    }
  ]
}
```

### Containers

**List Containers:**
```http
GET /api/v2/containers

Query Parameters:
- parentStorageId: string (filter by location/box)
- schemaId: string
- barcode: string
```

**Get Container:**
```http
GET /api/v2/containers/{containerId}
```

**Create Container:**
```http
POST /api/v2/containers

Body:
{
  "name": "Sample-001",
  "schemaId": "cont_schema_abc",
  "barcode": "CONT001",
  "parentStorageId": "box_abc123",
  "fields": {
    "concentration": {"value": "100 ng/μL"},
    "volume": {"value": "50 μL"}
  }
}
```

**Update Container:**
```http
PATCH /api/v2/containers/{containerId}

Body:
{
  "fields": {
    "volume": {"value": "45 μL"}
  }
}
```

**Transfer Container:**
```http
POST /api/v2/containers:transfer

Body:
{
  "containerIds": ["cont_abc123"],
  "destinationStorageId": "box_xyz789"
}
```

**Check Out Container:**
```http
POST /api/v2/containers:checkout

Body:
{
  "containerIds": ["cont_abc123"],
  "comment": "Taking to bench"
}
```

**Check In Container:**
```http
POST /api/v2/containers:checkin

Body:
{
  "containerIds": ["cont_abc123"],
  "locationId": "bench_loc_abc"
}
```

### Boxes

**List Boxes:**
```http
GET /api/v2/boxes

Query Parameters:
- parentStorageId: string
- schemaId: string
```

**Get Box:**
```http
GET /api/v2/boxes/{boxId}
```

**Create Box:**
```http
POST /api/v2/boxes

Body:
{
  "name": "Freezer-A-Box-01",
  "schemaId": "box_schema_abc",
  "parentStorageId": "loc_freezer_a",
  "barcode": "BOX001"
}
```

### Locations

**List Locations:**
```http
GET /api/v2/locations
```

**Get Location:**
```http
GET /api/v2/locations/{locationId}
```

**Create Location:**
```http
POST /api/v2/locations

Body:
{
  "name": "Freezer A - Shelf 2",
  "parentStorageId": "loc_freezer_a",
  "barcode": "LOC-A-S2"
}
```

### Plates

**List Plates:**
```http
GET /api/v2/plates
```

**Get Plate:**
```http
GET /api/v2/plates/{plateId}
```

**Create Plate:**
```http
POST /api/v2/plates

Body:
{
  "name": "PCR-Plate-001",
  "schemaId": "plate_schema_abc",
  "barcode": "PLATE001",
  "wells": [
    {"position": "A1", "entityId": "ent_abc"},
    {"position": "A2", "entityId": "ent_xyz"}
  ]
}
```

### Entries (Notebook)

**List Entries:**
```http
GET /api/v2/entries

Query Parameters:
- folderId: string
- schemaId: string
- modifiedAt: string
```

**Get Entry:**
```http
GET /api/v2/entries/{entryId}
```

**Create Entry:**
```http
POST /api/v2/entries

Body:
{
  "name": "Experiment 2025-10-20",
  "folderId": "fld_abc123",
  "schemaId": "entry_schema_abc",
  "fields": {
    "objective": {"value": "Test gene expression"},
    "date": {"value": "2025-10-20"}
  }
}
```

**Update Entry:**
```http
PATCH /api/v2/entries/{entryId}

Body:
{
  "fields": {
    "results": {"value": "Successful expression"}
  }
}
```

### Workflow Tasks

**List Workflow Tasks:**
```http
GET /api/v2/tasks

Query Parameters:
- workflowId: string
- statusIds: string[] (comma-separated)
- assigneeId: string
```

**Get Task:**
```http
GET /api/v2/tasks/{taskId}
```

**Create Task:**
```http
POST /api/v2/tasks

Body:
{
  "name": "PCR Amplification",
  "workflowId": "wf_abc123",
  "assigneeId": "user_abc123",
  "schemaId": "task_schema_abc",
  "fields": {
    "template": {"value": "seq_abc123"},
    "priority": {"value": "High"}
  }
}
```

**Update Task:**
```http
PATCH /api/v2/tasks/{taskId}

Body:
{
  "statusId": "status_complete_abc",
  "fields": {
    "completion_date": {"value": "2025-10-20"}
  }
}
```

### Folders

**List Folders:**
```http
GET /api/v2/folders

Query Parameters:
- projectId: string
- parentFolderId: string
```

**Get Folder:**
```http
GET /api/v2/folders/{folderId}
```

**Create Folder:**
```http
POST /api/v2/folders

Body:
{
  "name": "2025 Experiments",
  "parentFolderId": "fld_parent_abc",
  "projectId": "proj_abc123"
}
```

### Projects

**List Projects:**
```http
GET /api/v2/projects
```

**Get Project:**
```http
GET /api/v2/projects/{projectId}
```

### Users

**Get Current User:**
```http
GET /api/v2/users/me
```

**List Users:**
```http
GET /api/v2/users
```

**Get User:**
```http
GET /api/v2/users/{userId}
```

### Teams

**List Teams:**
```http
GET /api/v2/teams
```

**Get Team:**
```http
GET /api/v2/teams/{teamId}
```

### Schemas

**List Schemas:**
```http
GET /api/v2/schemas

Query Parameters:
- entityType: string (e.g., "dna_sequence", "custom_entity")
```

**Get Schema:**
```http
GET /api/v2/schemas/{schemaId}
```

### Registries

**List Registries:**
```http
GET /api/v2/registries
```

**Get Registry:**
```http
GET /api/v2/registries/{registryId}
```

## Bulk Operations

### Batch Archive

**Archive Multiple Entities:**
```http
POST /api/v2/{entity-type}:archive

Body:
{
  "{entity}Ids": ["id1", "id2", "id3"],
  "reason": "Cleanup"
}
```

### Batch Transfer

**Transfer Multiple Containers:**
```http
POST /api/v2/containers:bulk-transfer

Body:
{
  "transfers": [
    {"containerId": "cont_1", "destinationId": "box_a"},
    {"containerId": "cont_2", "destinationId": "box_b"}
  ]
}
```

## Async Operations

Some operations return task IDs for async processing:

**Response:**
```json
{
  "taskId": "task_abc123"
}
```

**Check Task Status:**
```http
GET /api/v2/tasks/{taskId}

Response:
{
  "id": "task_abc123",
  "status": "RUNNING", // or "SUCCEEDED", "FAILED"
  "message": "Processing...",
  "response": {...}  // Available when status is SUCCEEDED
}
```

## Field Value Format

Custom schema fields use a specific format:

**Simple Value:**
```json
{
  "field_name": {
    "value": "Field Value"
  }
}
```

**Dropdown:**
```json
{
  "dropdown_field": {
    "value": "Option1"  // Must match exact option name
  }
}
```

**Date:**
```json
{
  "date_field": {
    "value": "2025-10-20"  // Format: YYYY-MM-DD
  }
}
```

**Entity Link:**
```json
{
  "entity_link_field": {
    "value": "seq_abc123"  // Entity ID
  }
}
```

**Numeric:**
```json
{
  "numeric_field": {
    "value": "123.45"  // String representation
  }
}
```

## Rate Limiting

**Limits:**
- Default: 100 requests per 10 seconds per user/app
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`: Total allowed requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

**Handling 429 Responses:**
```json
{
  "error": {
    "type": "RateLimitError",
    "message": "Rate limit exceeded",
    "retryAfter": 5  // Seconds to wait
  }
}
```

## Filtering and Searching

**Common Query Parameters:**
- `name`: Partial name match
- `modifiedAt`: ISO 8601 datetime
- `createdAt`: ISO 8601 datetime
- `schemaId`: Filter by schema
- `folderId`: Filter by folder
- `archived`: Boolean (include archived items)

**Example:**
```bash
curl -X GET \
  "https://tenant.benchling.com/api/v2/dna-sequences?name=plasmid&folderId=fld_abc&archived=false"
```

## Best Practices

### Request Efficiency

1. **Use appropriate page sizes:**
   - Default: 50 items
   - Max: 100 items
   - Adjust based on needs

2. **Filter on server-side:**
   - Use query parameters instead of client filtering
   - Reduces data transfer and processing

3. **Batch operations:**
   - Use bulk endpoints when available
   - Archive/transfer multiple items in one request

### Error Handling

```javascript
// Example error handling
async function fetchSequence(id) {
  try {
    const response = await fetch(
      `https://tenant.benchling.com/api/v2/dna-sequences/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        }
      }
    );

    if (!response.ok) {
      if (response.status === 429) {
        // Rate limit - retry with backoff
        const retryAfter = response.headers.get('Retry-After');
        await sleep(retryAfter * 1000);
        return fetchSequence(id);
      } else if (response.status === 404) {
        return null;  // Not found
      } else {
        throw new Error(`API error: ${response.status}`);
      }
    }

    return await response.json();
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}
```

### Pagination Loop

```javascript
async function getAllSequences() {
  let allSequences = [];
  let nextToken = null;

  do {
    const url = new URL('https://tenant.benchling.com/api/v2/dna-sequences');
    if (nextToken) {
      url.searchParams.set('nextToken', nextToken);
    }
    url.searchParams.set('pageSize', '100');

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    });

    const data = await response.json();
    allSequences = allSequences.concat(data.results);
    nextToken = data.nextToken;
  } while (nextToken);

  return allSequences;
}
```

## References

- **API Documentation:** https://benchling.com/api/reference
- **Interactive API Explorer:** https://your-tenant.benchling.com/api/reference (requires authentication)
- **Changelog:** https://docs.benchling.com/changelog

---

## Reference: Authentication

# Benchling Authentication Reference

## Authentication Methods

Benchling supports three authentication methods, each suited for different use cases.

### 1. API Key Authentication (Basic Auth)

**Best for:** Personal scripts, prototyping, single-user integrations

**How it works:**
- Use your API key as the username in HTTP Basic authentication
- Leave the password field empty
- All requests must use HTTPS

**Obtaining an API Key:**
1. Log in to your Benchling account
2. Navigate to Profile Settings
3. Find the API Key section
4. Generate a new API key
5. Store it securely (it will only be shown once)

**Python SDK Usage:**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key_here")
)
```

**Direct HTTP Usage:**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -u "your_api_key_here:"
```

Note the colon after the API key with no password.

**Environment Variable Pattern:**
```python
import os
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

api_key = os.environ.get("BENCHLING_API_KEY")
tenant_url = os.environ.get("BENCHLING_TENANT_URL")

benchling = Benchling(
    url=tenant_url,
    auth_method=ApiKeyAuth(api_key)
)
```

### 2. OAuth 2.0 Client Credentials

**Best for:** Multi-user applications, service accounts, production integrations

**How it works:**
1. Register an application in Benchling's Developer Console
2. Obtain client ID and client secret
3. Exchange credentials for an access token
4. Use the access token for API requests
5. Refresh token when expired

**Registering an App:**
1. Log in to Benchling as an admin
2. Navigate to Developer Console
3. Create a new App
4. Record the client ID and client secret
5. Configure OAuth redirect URIs and permissions

**Python SDK Usage:**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

The SDK automatically handles token refresh.

**Direct HTTP Token Flow:**
```bash
# Get access token
curl -X POST \
  https://your-tenant.benchling.com/api/v2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret"

# Response:
# {
#   "access_token": "token_here",
#   "token_type": "Bearer",
#   "expires_in": 3600
# }

# Use access token
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer access_token_here"
```

### 3. OpenID Connect (OIDC)

**Best for:** Enterprise integrations with existing identity providers, SSO scenarios

**How it works:**
- Authenticate users through your identity provider (Okta, Azure AD, etc.)
- Identity provider issues an ID token with email claim
- Benchling verifies the token against the OpenID configuration endpoint
- Matches authenticated user by email

**Requirements:**
- Enterprise Benchling account
- Configured identity provider (IdP)
- IdP must issue tokens with email claims
- Email in token must match Benchling user email

**Identity Provider Configuration:**
1. Configure your IdP to issue OpenID Connect tokens
2. Ensure tokens include the `email` claim
3. Provide Benchling with your IdP's OpenID configuration URL
4. Benchling will verify tokens against this configuration

**Python Usage:**
```python
# Assuming you have an ID token from your IdP
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.oidc_auth import OidcAuth

auth_method = OidcAuth(id_token="id_token_from_idp")

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

**Direct HTTP Usage:**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer id_token_here"
```

## Security Best Practices

### Credential Storage

**DO:**
- Store credentials in environment variables
- Use password managers or secret management services (AWS Secrets Manager, HashiCorp Vault)
- Encrypt credentials at rest
- Use different credentials for dev/staging/production

**DON'T:**
- Commit credentials to version control
- Hardcode credentials in source files
- Share credentials via email or chat
- Store credentials in plain text files

**Example with Environment Variables:**
```python
import os
from dotenv import load_dotenv  # python-dotenv package

# Load from .env file (add .env to .gitignore!)
load_dotenv()

api_key = os.environ["BENCHLING_API_KEY"]
tenant = os.environ["BENCHLING_TENANT_URL"]
```

### Credential Rotation

**API Key Rotation:**
1. Generate a new API key in Profile Settings
2. Update your application to use the new key
3. Verify the new key works
4. Delete the old API key

**App Secret Rotation:**
1. Navigate to Developer Console
2. Select your app
3. Generate new client secret
4. Update your application configuration
5. Delete the old secret after verifying

**Best Practice:** Rotate credentials regularly (e.g., every 90 days) and immediately if compromised.

### Access Control

**Principle of Least Privilege:**
- Grant only the minimum necessary permissions
- Use service accounts (apps) instead of personal accounts for automation
- Review and audit permissions regularly

**App Permissions:**
Apps require explicit access grants to:
- Organizations
- Teams
- Projects
- Folders

Configure these in the Developer Console when setting up your app.

**User Permissions:**
API access mirrors UI permissions:
- Users can only access data they have permission to view/edit in the UI
- Suspended users lose API access
- Archived apps lose API access until unarchived

### Network Security

**HTTPS Only:**
All Benchling API requests must use HTTPS. HTTP requests will be rejected.

**IP Allowlisting (Enterprise):**
Some enterprise accounts can restrict API access to specific IP ranges. Contact Benchling support to configure.

**Rate Limiting:**
Benchling implements rate limiting to prevent abuse:
- Default: 100 requests per 10 seconds per user/app
- 429 status code returned when rate limit exceeded
- SDK automatically retries with exponential backoff

### Audit Logging

**Tracking API Usage:**
- All API calls are logged with user/app identity
- OAuth apps show proper audit trails with user attribution
- API key calls are attributed to the key owner
- Review audit logs in Benchling's admin console

**Best Practice for Apps:**
Use OAuth instead of API keys when multiple users interact through your app. This ensures proper audit attribution to the actual user, not just the app.

## Troubleshooting

### Common Authentication Errors

**401 Unauthorized:**
- Invalid or expired credentials
- API key not properly formatted
- Missing "Authorization" header

**Solution:**
- Verify credentials are correct
- Check API key is not expired or deleted
- Ensure proper header format: `Authorization: Bearer <token>`

**403 Forbidden:**
- Valid credentials but insufficient permissions
- User doesn't have access to the requested resource
- App not granted access to the organization/project

**Solution:**
- Check user/app permissions in Benchling
- Grant necessary access in Developer Console (for apps)
- Verify the resource exists and user has access

**429 Too Many Requests:**
- Rate limit exceeded
- Too many requests in short time period

**Solution:**
- Implement exponential backoff
- SDK handles this automatically
- Consider caching results
- Spread requests over time

### Testing Authentication

**Quick Test with curl:**
```bash
# Test API key
curl -X GET \
  https://your-tenant.benchling.com/api/v2/users/me \
  -u "your_api_key:" \
  -v

# Test OAuth token
curl -X GET \
  https://your-tenant.benchling.com/api/v2/users/me \
  -H "Authorization: Bearer your_token" \
  -v
```

The `/users/me` endpoint returns the authenticated user's information and is useful for verifying credentials.

**Python SDK Test:**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

try:
    benchling = Benchling(
        url="https://your-tenant.benchling.com",
        auth_method=ApiKeyAuth("your_api_key")
    )

    # Test authentication
    user = benchling.users.get_me()
    print(f"Authenticated as: {user.name} ({user.email})")

except Exception as e:
    print(f"Authentication failed: {e}")
```

## Multi-Tenant Considerations

If working with multiple Benchling tenants:

```python
# Configuration for multiple tenants
tenants = {
    "production": {
        "url": "https://prod.benchling.com",
        "api_key": os.environ["PROD_API_KEY"]
    },
    "staging": {
        "url": "https://staging.benchling.com",
        "api_key": os.environ["STAGING_API_KEY"]
    }
}

# Initialize clients
clients = {}
for name, config in tenants.items():
    clients[name] = Benchling(
        url=config["url"],
        auth_method=ApiKeyAuth(config["api_key"])
    )

# Use specific client
prod_sequences = clients["production"].dna_sequences.list()
```

## Advanced: Custom HTTPS Clients

For environments with self-signed certificates or corporate proxies:

```python
import httpx
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

# Custom httpx client with certificate verification
custom_client = httpx.Client(
    verify="/path/to/custom/ca-bundle.crt",
    timeout=30.0
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    http_client=custom_client
)
```

## References

- **Official Authentication Docs:** https://docs.benchling.com/docs/authentication
- **Developer Console:** https://your-tenant.benchling.com/developer
- **SDK Documentation:** https://benchling.com/sdk-docs/

---

## Reference: Sdk_Reference

# Benchling Python SDK Reference

## Installation & Setup

### Installation

```bash
# Stable release
pip install benchling-sdk

# With Poetry
poetry add benchling-sdk

# Pre-release/preview versions (not recommended for production)
pip install benchling-sdk --pre
poetry add benchling-sdk --allow-prereleases
```

### Requirements
- Python 3.7 or higher
- API access enabled on your Benchling tenant

### Basic Initialization

```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key")
)
```

## SDK Architecture

### Main Classes

**Benchling Client:**
The `benchling_sdk.benchling.Benchling` class is the root of all SDK interactions. It provides access to all resource endpoints:

```python
benchling.dna_sequences      # DNA sequence operations
benchling.rna_sequences      # RNA sequence operations
benchling.aa_sequences       # Amino acid sequence operations
benchling.custom_entities    # Custom entity operations
benchling.mixtures           # Mixture operations
benchling.containers         # Container operations
benchling.boxes              # Box operations
benchling.locations          # Location operations
benchling.plates             # Plate operations
benchling.entries            # Notebook entry operations
benchling.workflow_tasks     # Workflow task operations
benchling.requests           # Request operations
benchling.folders            # Folder operations
benchling.projects           # Project operations
benchling.users              # User operations
benchling.teams              # Team operations
```

### Resource Pattern

All resources follow a consistent CRUD pattern:

```python
# Create
resource.create(CreateModel(...))

# Read (single)
resource.get(id="resource_id")

# Read (list)
resource.list(optional_filters...)

# Update
resource.update(id="resource_id", UpdateModel(...))

# Archive/Delete
resource.archive(id="resource_id")
```

## Entity Management

### DNA Sequences

**Create:**
```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="pET28a-GFP",
        bases="ATCGATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",
        fields=benchling.models.fields({
            "gene_name": "GFP",
            "resistance": "Kanamycin",
            "copy_number": "High"
        })
    )
)
```

**Read:**
```python
# Get by ID
seq = benchling.dna_sequences.get(sequence_id="seq_abc123")
print(f"{seq.name}: {len(seq.bases)} bp")

# List with filters
sequences = benchling.dna_sequences.list(
    folder_id="fld_abc123",
    schema_id="ts_abc123",
    name="pET28a"  # Filter by name
)

for page in sequences:
    for seq in page:
        print(f"{seq.id}: {seq.name}")
```

**Update:**
```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="pET28a-GFP-v2",
        fields=benchling.models.fields({
            "gene_name": "eGFP",
            "notes": "Codon optimized"
        })
    )
)
```

**Archive:**
```python
benchling.dna_sequences.archive(
    sequence_id="seq_abc123",
    reason="Deprecated construct"
)
```

### RNA Sequences

Similar pattern to DNA sequences:

```python
from benchling_sdk.models import RnaSequenceCreate, RnaSequenceUpdate

# Create
rna = benchling.rna_sequences.create(
    RnaSequenceCreate(
        name="gRNA-target1",
        bases="AUCGAUCGAUCG",
        folder_id="fld_abc123",
        fields=benchling.models.fields({
            "target_gene": "TP53",
            "off_target_score": "95"
        })
    )
)

# Update
updated_rna = benchling.rna_sequences.update(
    rna_sequence_id=rna.id,
    rna_sequence=RnaSequenceUpdate(
        fields=benchling.models.fields({
            "validated": "Yes"
        })
    )
)
```

### Amino Acid (Protein) Sequences

```python
from benchling_sdk.models import AaSequenceCreate

protein = benchling.aa_sequences.create(
    AaSequenceCreate(
        name="Green Fluorescent Protein",
        amino_acids="MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKF",
        folder_id="fld_abc123",
        fields=benchling.models.fields({
            "molecular_weight": "27000",
            "extinction_coefficient": "21000"
        })
    )
)
```

### Custom Entities

Custom entities are defined by your tenant's schemas:

```python
from benchling_sdk.models import CustomEntityCreate, CustomEntityUpdate

# Create
cell_line = benchling.custom_entities.create(
    CustomEntityCreate(
        name="HEK293T-Clone5",
        schema_id="ts_cellline_abc123",
        folder_id="fld_abc123",
        fields=benchling.models.fields({
            "passage_number": "15",
            "mycoplasma_test": "Negative",
            "freezing_date": "2025-10-15"
        })
    )
)

# Update
updated_cell_line = benchling.custom_entities.update(
    entity_id=cell_line.id,
    custom_entity=CustomEntityUpdate(
        fields=benchling.models.fields({
            "passage_number": "16",
            "notes": "Expanded for experiment"
        })
    )
)
```

### Mixtures

Mixtures combine multiple components:

```python
from benchling_sdk.models import MixtureCreate, IngredientCreate

mixture = benchling.mixtures.create(
    MixtureCreate(
        name="LB-Amp Media",
        folder_id="fld_abc123",
        schema_id="ts_mixture_abc123",
        ingredients=[
            IngredientCreate(
                component_entity_id="ent_lb_base",
                amount="1000 mL"
            ),
            IngredientCreate(
                component_entity_id="ent_ampicillin",
                amount="100 mg"
            )
        ],
        fields=benchling.models.fields({
            "pH": "7.0",
            "sterilized": "Yes"
        })
    )
)
```

### Registry Operations

**Direct Registry Registration:**
```python
# Register entity upon creation
registered_seq = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="Construct-001",
        bases="ATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",
        naming_strategy="NEW_IDS"  # or "IDS_FROM_NAMES"
    )
)
print(f"Registry ID: {registered_seq.registry_id}")
```

**Naming Strategies:**
- `NEW_IDS`: Benchling generates new registry IDs
- `IDS_FROM_NAMES`: Use entity names as registry IDs (names must be unique)

## Inventory Management

### Containers

```python
from benchling_sdk.models import ContainerCreate, ContainerUpdate

# Create
container = benchling.containers.create(
    ContainerCreate(
        name="Sample-001-Tube",
        schema_id="cont_schema_abc123",
        barcode="CONT001",
        parent_storage_id="box_abc123",  # Place in box
        fields=benchling.models.fields({
            "concentration": "100 ng/μL",
            "volume": "50 μL",
            "sample_type": "gDNA"
        })
    )
)

# Update location
benchling.containers.transfer(
    container_id=container.id,
    destination_id="box_xyz789"
)

# Update properties
updated = benchling.containers.update(
    container_id=container.id,
    container=ContainerUpdate(
        fields=benchling.models.fields({
            "volume": "45 μL",
            "notes": "Used 5 μL for PCR"
        })
    )
)

# Check out
benchling.containers.check_out(
    container_id=container.id,
    comment="Taking to bench"
)

# Check in
benchling.containers.check_in(
    container_id=container.id,
    location_id="bench_location_abc"
)
```

### Boxes

```python
from benchling_sdk.models import BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Freezer-A-Box-01",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_freezer_a",
        barcode="BOX001",
        fields=benchling.models.fields({
            "box_type": "81-place",
            "temperature": "-80C"
        })
    )
)

# List containers in box
containers = benchling.containers.list(
    parent_storage_id=box.id
)
```

### Locations

```python
from benchling_sdk.models import LocationCreate

location = benchling.locations.create(
    LocationCreate(
        name="Freezer A - Shelf 2",
        parent_storage_id="loc_freezer_a",
        barcode="LOC-A-S2"
    )
)
```

### Plates

```python
from benchling_sdk.models import PlateCreate, WellCreate

# Create 96-well plate
plate = benchling.plates.create(
    PlateCreate(
        name="PCR-Plate-001",
        schema_id="plate_schema_abc123",
        barcode="PLATE001",
        wells=[
            WellCreate(
                position="A1",
                entity_id="sample_entity_abc"
            ),
            WellCreate(
                position="A2",
                entity_id="sample_entity_xyz"
            )
            # ... more wells
        ]
    )
)
```

## Notebook Operations

### Entries

```python
from benchling_sdk.models import EntryCreate, EntryUpdate

# Create entry
entry = benchling.entries.create(
    EntryCreate(
        name="Cloning Experiment 2025-10-20",
        folder_id="fld_abc123",
        schema_id="entry_schema_abc123",
        fields=benchling.models.fields({
            "objective": "Clone GFP into pET28a",
            "date": "2025-10-20",
            "experiment_type": "Molecular Biology"
        })
    )
)

# Update entry
updated_entry = benchling.entries.update(
    entry_id=entry.id,
    entry=EntryUpdate(
        fields=benchling.models.fields({
            "results": "Successful cloning, 10 colonies",
            "notes": "Colony 5 shows best fluorescence"
        })
    )
)
```

### Linking Entities to Entries

```python
# Link DNA sequence to entry
link = benchling.entry_links.create(
    entry_id="entry_abc123",
    entity_id="seq_xyz789"
)

# List links for an entry
links = benchling.entry_links.list(entry_id="entry_abc123")
```

## Workflow Management

### Tasks

```python
from benchling_sdk.models import WorkflowTaskCreate, WorkflowTaskUpdate

# Create task
task = benchling.workflow_tasks.create(
    WorkflowTaskCreate(
        name="PCR Amplification",
        workflow_id="wf_abc123",
        assignee_id="user_abc123",
        schema_id="task_schema_abc123",
        fields=benchling.models.fields({
            "template": "seq_abc123",
            "primers": "Forward: ATCG, Reverse: CGAT",
            "priority": "High"
        })
    )
)

# Update status
completed_task = benchling.workflow_tasks.update(
    task_id=task.id,
    workflow_task=WorkflowTaskUpdate(
        status_id="status_complete_abc123",
        fields=benchling.models.fields({
            "completion_date": "2025-10-20",
            "yield": "500 ng"
        })
    )
)

# List tasks
tasks = benchling.workflow_tasks.list(
    workflow_id="wf_abc123",
    status_ids=["status_pending", "status_in_progress"]
)
```

## Advanced Features

### Pagination

The SDK uses generators for memory-efficient pagination:

```python
# Automatic pagination
sequences = benchling.dna_sequences.list()

# Get estimated total count
total = sequences.estimated_count()
print(f"Total sequences: {total}")

# Iterate through all pages
for page in sequences:
    for seq in page:
        process(seq)

# Manual page size control
sequences = benchling.dna_sequences.list(page_size=50)
```

### Async Task Handling

Some operations are asynchronous and return task IDs:

```python
from benchling_sdk.helpers.tasks import wait_for_task
from benchling_sdk.errors import WaitForTaskExpiredError

# Start async operation
response = benchling.some_bulk_operation(...)
task_id = response.task_id

# Wait for completion
try:
    result = wait_for_task(
        benchling,
        task_id=task_id,
        interval_wait_seconds=2,  # Poll every 2 seconds
        max_wait_seconds=600       # Timeout after 10 minutes
    )
    print("Task completed successfully")
except WaitForTaskExpiredError:
    print("Task timed out")
```

### Error Handling

```python
from benchling_sdk.errors import (
    BenchlingError,
    NotFoundError,
    ValidationError,
    UnauthorizedError
)

try:
    sequence = benchling.dna_sequences.get(sequence_id="seq_invalid")
except NotFoundError:
    print("Sequence not found")
except UnauthorizedError:
    print("Insufficient permissions")
except ValidationError as e:
    print(f"Invalid data: {e}")
except BenchlingError as e:
    print(f"General Benchling error: {e}")
```

### Retry Strategy

Customize retry behavior:

```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth
from benchling_sdk.retry import RetryStrategy

# Custom retry configuration
retry_strategy = RetryStrategy(
    max_retries=3,
    backoff_factor=0.5,
    status_codes_to_retry=[429, 502, 503, 504]
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=retry_strategy
)

# Disable retries
benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=RetryStrategy(max_retries=0)
)
```

### Custom API Calls

For unsupported endpoints:

```python
# GET request with model parsing
from benchling_sdk.models import DnaSequence

response = benchling.api.get_modeled(
    path="/api/v2/dna-sequences/seq_abc123",
    response_type=DnaSequence
)

# POST request
from benchling_sdk.models import DnaSequenceCreate

response = benchling.api.post_modeled(
    path="/api/v2/dna-sequences",
    request_body=DnaSequenceCreate(...),
    response_type=DnaSequence
)

# Raw requests
raw_response = benchling.api.get(
    path="/api/v2/custom-endpoint",
    params={"key": "value"}
)
```

### Batch Operations

Efficiently process multiple items:

```python
# Bulk create
from benchling_sdk.models import DnaSequenceCreate

sequences_to_create = [
    DnaSequenceCreate(name=f"Seq-{i}", bases="ATCG", folder_id="fld_abc")
    for i in range(100)
]

# Create in batches
batch_size = 10
for i in range(0, len(sequences_to_create), batch_size):
    batch = sequences_to_create[i:i+batch_size]
    for seq in batch:
        benchling.dna_sequences.create(seq)
```

### Schema Fields Helper

Convert dictionaries to Fields objects:

```python
# Using fields helper
fields_dict = {
    "concentration": "100 ng/μL",
    "volume": "50 μL",
    "quality_score": "8.5",
    "date_prepared": "2025-10-20"
}

fields = benchling.models.fields(fields_dict)

# Use in create/update
container = benchling.containers.create(
    ContainerCreate(
        name="Sample-001",
        schema_id="schema_abc",
        fields=fields
    )
)
```

### Forward Compatibility

The SDK handles unknown API values gracefully:

```python
# Unknown enum values are preserved
entity = benchling.dna_sequences.get("seq_abc")
# Even if API returns new enum value not in SDK, it's preserved

# Unknown polymorphic types return UnknownType
from benchling_sdk.models import UnknownType

if isinstance(entity, UnknownType):
    print(f"Unknown type: {entity.type}")
    # Can still access raw data
    print(entity.raw_data)
```

## Best Practices

### Use Type Hints

```python
from benchling_sdk.models import DnaSequence, DnaSequenceCreate
from typing import List

def create_sequences(names: List[str], folder_id: str) -> List[DnaSequence]:
    sequences = []
    for name in names:
        seq = benchling.dna_sequences.create(
            DnaSequenceCreate(
                name=name,
                bases="ATCG",
                folder_id=folder_id
            )
        )
        sequences.append(seq)
    return sequences
```

### Efficient Filtering

Use API filters instead of client-side filtering:

```python
# Good - filter on server
sequences = benchling.dna_sequences.list(
    folder_id="fld_abc123",
    schema_id="ts_abc123"
)

# Bad - loads everything then filters
all_sequences = benchling.dna_sequences.list()
filtered = [s for page in all_sequences for s in page if s.folder_id == "fld_abc123"]
```

### Resource Cleanup

```python
# Archive old entities
cutoff_date = "2024-01-01"
sequences = benchling.dna_sequences.list()

for page in sequences:
    for seq in page:
        if seq.created_at < cutoff_date:
            benchling.dna_sequences.archive(
                sequence_id=seq.id,
                reason="Archiving old sequences"
            )
```

## Troubleshooting

### Common Issues

**Import Errors:**
```python
# Wrong
from benchling_sdk import Benchling  # ImportError

# Correct
from benchling_sdk.benchling import Benchling
```

**Field Validation:**
```python
# Fields must match schema
# Check schema field types in Benchling UI
fields = benchling.models.fields({
    "numeric_field": "123",    # Should be string even for numbers
    "date_field": "2025-10-20", # Format: YYYY-MM-DD
    "dropdown_field": "Option1" # Must match dropdown options exactly
})
```

**Pagination Exhaustion:**
```python
# Generators can only be iterated once
sequences = benchling.dna_sequences.list()
for page in sequences:  # First iteration OK
    pass
for page in sequences:  # Second iteration returns nothing!
    pass

# Solution: Create new generator
sequences = benchling.dna_sequences.list()  # New generator
```

## References

- **SDK Source:** https://github.com/benchling/benchling-sdk
- **SDK Docs:** https://benchling.com/sdk-docs/
- **API Reference:** https://benchling.com/api/reference
- **Common Examples:** https://docs.benchling.com/docs/common-sdk-interactions-and-examples
