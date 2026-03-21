---
title: "OMERO 生物影像"
description: "OMERO 生物影像平台集成，显微镜图像管理和分析"
category: "workflow"
source: "community"
author: "Community"
tags: ["omero", "integration"]
date: 2026-03-20
---

# OMERO Integration

## Overview

OMERO is an open-source platform for managing, visualizing, and analyzing microscopy images and metadata. Access images via Python API, retrieve datasets, analyze pixels, manage ROIs and annotations, for high-content screening and microscopy workflows.

## When to Use This Skill

This skill should be used when:
- Working with OMERO Python API (omero-py) to access microscopy data
- Retrieving images, datasets, projects, or screening data programmatically
- Analyzing pixel data and creating derived images
- Creating or managing ROIs (regions of interest) on microscopy images
- Adding annotations, tags, or metadata to OMERO objects
- Storing measurement results in OMERO tables
- Creating server-side scripts for batch processing
- Performing high-content screening analysis

## Core Capabilities

This skill covers eight major capability areas. Each is documented in detail in the references/ directory:

### 1. Connection & Session Management
**File**: `references/connection.md`

Establish secure connections to OMERO servers, manage sessions, handle authentication, and work with group contexts. Use this for initial setup and connection patterns.

**Common scenarios:**
- Connect to OMERO server with credentials
- Use existing session IDs
- Switch between group contexts
- Manage connection lifecycle with context managers

### 2. Data Access & Retrieval
**File**: `references/data_access.md`

Navigate OMERO's hierarchical data structure (Projects → Datasets → Images) and screening data (Screens → Plates → Wells). Retrieve objects, query by attributes, and access metadata.

**Common scenarios:**
- List all projects and datasets for a user
- Retrieve images by ID or dataset
- Access screening plate data
- Query objects with filters

### 3. Metadata & Annotations
**File**: `references/metadata.md`

Create and manage annotations including tags, key-value pairs, file attachments, and comments. Link annotations to images, datasets, or other objects.

**Common scenarios:**
- Add tags to images
- Attach analysis results as files
- Create custom key-value metadata
- Query annotations by namespace

### 4. Image Processing & Rendering
**File**: `references/image_processing.md`

Access raw pixel data as NumPy arrays, manipulate rendering settings, create derived images, and manage physical dimensions.

**Common scenarios:**
- Extract pixel data for computational analysis
- Generate thumbnail images
- Create maximum intensity projections
- Modify channel rendering settings

### 5. Regions of Interest (ROIs)
**File**: `references/rois.md`

Create, retrieve, and analyze ROIs with various shapes (rectangles, ellipses, polygons, masks, points, lines). Extract intensity statistics from ROI regions.

**Common scenarios:**
- Draw rectangular ROIs on images
- Create polygon masks for segmentation
- Analyze pixel intensities within ROIs
- Export ROI coordinates

### 6. OMERO Tables
**File**: `references/tables.md`

Store and query structured tabular data associated with OMERO objects. Useful for analysis results, measurements, and metadata.

**Common scenarios:**
- Store quantitative measurements for images
- Create tables with multiple column types
- Query table data with conditions
- Link tables to specific images or datasets

### 7. Scripts & Batch Operations
**File**: `references/scripts.md`

Create OMERO.scripts that run server-side for batch processing, automated workflows, and integration with OMERO clients.

**Common scenarios:**
- Process multiple images in batch
- Create automated analysis pipelines
- Generate summary statistics across datasets
- Export data in custom formats

### 8. Advanced Features
**File**: `references/advanced.md`

Covers permissions, filesets, cross-group queries, delete operations, and other advanced functionality.

**Common scenarios:**
- Handle group permissions
- Access original imported files
- Perform cross-group queries
- Delete objects with callbacks

## Installation

```bash
uv pip install omero-py
```

**Requirements:**
- Python 3.7+
- Zeroc Ice 3.6+
- Access to an OMERO server (host, port, credentials)

## Quick Start

Basic connection pattern:

```python
from omero.gateway import BlitzGateway

# Connect to OMERO server
conn = BlitzGateway(username, password, host=host, port=port)
connected = conn.connect()

if connected:
    # Perform operations
    for project in conn.listProjects():
        print(project.getName())

    # Always close connection
    conn.close()
else:
    print("Connection failed")
```

**Recommended pattern with context manager:**

```python
from omero.gateway import BlitzGateway

with BlitzGateway(username, password, host=host, port=port) as conn:
    # Connection automatically managed
    for project in conn.listProjects():
        print(project.getName())
    # Automatically closed on exit
```

## Selecting the Right Capability

**For data exploration:**
- Start with `references/connection.md` to establish connection
- Use `references/data_access.md` to navigate hierarchy
- Check `references/metadata.md` for annotation details

**For image analysis:**
- Use `references/image_processing.md` for pixel data access
- Use `references/rois.md` for region-based analysis
- Use `references/tables.md` to store results

**For automation:**
- Use `references/scripts.md` for server-side processing
- Use `references/data_access.md` for batch data retrieval

**For advanced operations:**
- Use `references/advanced.md` for permissions and deletion
- Check `references/connection.md` for cross-group queries

## Common Workflows

### Workflow 1: Retrieve and Analyze Images

1. Connect to OMERO server (`references/connection.md`)
2. Navigate to dataset (`references/data_access.md`)
3. Retrieve images from dataset (`references/data_access.md`)
4. Access pixel data as NumPy array (`references/image_processing.md`)
5. Perform analysis
6. Store results as table or file annotation (`references/tables.md` or `references/metadata.md`)

### Workflow 2: Batch ROI Analysis

1. Connect to OMERO server
2. Retrieve images with existing ROIs (`references/rois.md`)
3. For each image, get ROI shapes
4. Extract pixel intensities within ROIs (`references/rois.md`)
5. Store measurements in OMERO table (`references/tables.md`)

### Workflow 3: Create Analysis Script

1. Design analysis workflow
2. Use OMERO.scripts framework (`references/scripts.md`)
3. Access data through script parameters
4. Process images in batch
5. Generate outputs (new images, tables, files)

## Error Handling

Always wrap OMERO operations in try-except blocks and ensure connections are properly closed:

```python
from omero.gateway import BlitzGateway
import traceback

try:
    conn = BlitzGateway(username, password, host=host, port=port)
    if not conn.connect():
        raise Exception("Connection failed")

    # Perform operations

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
finally:
    if conn:
        conn.close()
```

## Additional Resources

- **Official Documentation**: https://omero.readthedocs.io/en/stable/developers/Python.html
- **BlitzGateway API**: https://omero.readthedocs.io/en/stable/developers/Python.html#omero-blitzgateway
- **OMERO Model**: https://omero.readthedocs.io/en/stable/developers/Model.html
- **Community Forum**: https://forum.image.sc/tag/omero

## Notes

- OMERO uses group-based permissions (READ-ONLY, READ-ANNOTATE, READ-WRITE)
- Images in OMERO are organized hierarchically: Project > Dataset > Image
- Screening data uses: Screen > Plate > Well > WellSample > Image
- Always close connections to free server resources
- Use context managers for automatic resource management
- Pixel data is returned as NumPy arrays for analysis

---

## Reference: Advanced

# Advanced Features

This reference covers advanced OMERO operations including permissions, deletion, filesets, and administrative tasks.

## Deleting Objects

### Delete with Wait

```python
# Delete objects and wait for completion
project_ids = [1, 2, 3]
conn.deleteObjects("Project", project_ids, wait=True)
print("Deletion complete")

# Delete without waiting (asynchronous)
conn.deleteObjects("Dataset", [dataset_id], wait=False)
```

### Delete with Callback Monitoring

```python
from omero.callbacks import CmdCallbackI

# Start delete operation
handle = conn.deleteObjects("Project", [project_id])

# Create callback to monitor progress
cb = CmdCallbackI(conn.c, handle)
print("Deleting, please wait...")

# Poll for completion
while not cb.block(500):  # Check every 500ms
    print(".", end="", flush=True)

print("\nDeletion finished")

# Check for errors
response = cb.getResponse()
if isinstance(response, omero.cmd.ERR):
    print("Error occurred:")
    print(response)
else:
    print("Deletion successful")

# Clean up
cb.close(True)  # Also closes handle
```

### Delete Different Object Types

```python
# Delete images
image_ids = [101, 102, 103]
conn.deleteObjects("Image", image_ids, wait=True)

# Delete datasets
dataset_ids = [10, 11]
conn.deleteObjects("Dataset", dataset_ids, wait=True)

# Delete ROIs
roi_ids = [201, 202]
conn.deleteObjects("Roi", roi_ids, wait=True)

# Delete annotations
annotation_ids = [301, 302]
conn.deleteObjects("Annotation", annotation_ids, wait=True)
```

### Delete with Cascade

```python
# Deleting a project will cascade to contained datasets
# This behavior depends on server configuration
project_id = 123
conn.deleteObjects("Project", [project_id], wait=True)

# Datasets and images may be deleted or orphaned
# depending on delete specifications
```

## Filesets

Filesets represent collections of original imported files. They were introduced in OMERO 5.0.

### Check if Image Has Fileset

```python
image = conn.getObject("Image", image_id)

fileset = image.getFileset()
if fileset:
    print(f"Image is part of fileset {fileset.getId()}")
else:
    print("Image has no fileset (pre-OMERO 5.0)")
```

### Access Fileset Information

```python
image = conn.getObject("Image", image_id)
fileset = image.getFileset()

if fileset:
    fs_id = fileset.getId()
    print(f"Fileset ID: {fs_id}")

    # List all images in this fileset
    print("Images in fileset:")
    for fs_image in fileset.copyImages():
        print(f"  {fs_image.getId()}: {fs_image.getName()}")

    # List original imported files
    print("\nOriginal files:")
    for orig_file in fileset.listFiles():
        print(f"  {orig_file.getPath()}/{orig_file.getName()}")
        print(f"    Size: {orig_file.getSize()} bytes")
```

### Get Fileset Directly

```python
# Get fileset object
fileset = conn.getObject("Fileset", fileset_id)

if fileset:
    # Access images
    for image in fileset.copyImages():
        print(f"Image: {image.getName()}")

    # Access files
    for orig_file in fileset.listFiles():
        print(f"File: {orig_file.getName()}")
```

### Download Original Files

```python
import os

fileset = image.getFileset()

if fileset:
    download_dir = "./original_files"
    os.makedirs(download_dir, exist_ok=True)

    for orig_file in fileset.listFiles():
        file_name = orig_file.getName()
        file_path = os.path.join(download_dir, file_name)

        print(f"Downloading: {file_name}")

        # Get file as RawFileStore
        raw_file_store = conn.createRawFileStore()
        raw_file_store.setFileId(orig_file.getId())

        # Download in chunks
        with open(file_path, 'wb') as f:
            offset = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            size = orig_file.getSize()

            while offset < size:
                chunk = raw_file_store.read(offset, chunk_size)
                f.write(chunk)
                offset += len(chunk)

        raw_file_store.close()
        print(f"Saved to: {file_path}")
```

## Group Permissions

OMERO uses group-based permissions to control data access.

### Permission Levels

- **PRIVATE** (`rw----`): Only owner can read/write
- **READ-ONLY** (`rwr---`): Group members can read, only owner can write
- **READ-ANNOTATE** (`rwra--`): Group members can read and annotate
- **READ-WRITE** (`rwrw--`): Group members can read and write

### Check Current Group Permissions

```python
# Get current group
group = conn.getGroupFromContext()

# Get permissions
permissions = group.getDetails().getPermissions()
perm_string = str(permissions)

# Map to readable names
permission_names = {
    'rw----': 'PRIVATE',
    'rwr---': 'READ-ONLY',
    'rwra--': 'READ-ANNOTATE',
    'rwrw--': 'READ-WRITE'
}

perm_name = permission_names.get(perm_string, 'UNKNOWN')
print(f"Group: {group.getName()}")
print(f"Permissions: {perm_name} ({perm_string})")
```

### List User's Groups

```python
# Get all groups for current user
print("User's groups:")
for group in conn.getGroupsMemberOf():
    print(f"  {group.getName()} (ID: {group.getId()})")

    # Get group permissions
    perms = group.getDetails().getPermissions()
    print(f"    Permissions: {perms}")
```

### Get Group Members

```python
# Get group
group = conn.getObject("ExperimenterGroup", group_id)

# List members
print(f"Members of {group.getName()}:")
for member in group.getMembers():
    print(f"  {member.getFullName()} ({member.getOmeName()})")
```

## Cross-Group Queries

### Query Across All Groups

```python
# Set context to query all accessible groups
conn.SERVICE_OPTS.setOmeroGroup('-1')

# Now queries span all groups
image = conn.getObject("Image", image_id)
if image:
    group = image.getDetails().getGroup()
    print(f"Image found in group: {group.getName()}")

# List projects across all groups
for project in conn.getObjects("Project"):
    group = project.getDetails().getGroup()
    print(f"Project: {project.getName()} (Group: {group.getName()})")
```

### Switch to Specific Group

```python
# Get image's group
image = conn.getObject("Image", image_id)
group_id = image.getDetails().getGroup().getId()

# Switch to that group's context
conn.SERVICE_OPTS.setOmeroGroup(group_id)

# Subsequent operations use this group
projects = conn.listProjects()  # Only from this group
```

### Reset to Default Group

```python
# Get default group
default_group_id = conn.getEventContext().groupId

# Switch back to default
conn.SERVICE_OPTS.setOmeroGroup(default_group_id)
```

## Administrative Operations

### Check Admin Status

```python
# Check if current user is admin
if conn.isAdmin():
    print("User has admin privileges")

# Check if full admin
if conn.isFullAdmin():
    print("User is full administrator")
else:
    # Check specific privileges
    privileges = conn.getCurrentAdminPrivileges()
    print(f"Admin privileges: {privileges}")
```

### List Administrators

```python
# Get all administrators
print("Administrators:")
for admin in conn.getAdministrators():
    print(f"  ID: {admin.getId()}")
    print(f"  Username: {admin.getOmeName()}")
    print(f"  Full Name: {admin.getFullName()}")
```

### Set Object Owner (Admin Only)

```python
import omero.model

# Create annotation with specific owner (requires admin)
tag_ann = omero.gateway.TagAnnotationWrapper(conn)
tag_ann.setValue("Admin-created tag")

# Set owner
user_id = 5
tag_ann._obj.details.owner = omero.model.ExperimenterI(user_id, False)
tag_ann.save()

print(f"Created annotation owned by user {user_id}")
```

### Substitute User Connection (Admin Only)

```python
# Connect as admin
admin_conn = BlitzGateway(admin_user, admin_pass, host=host, port=4064)
admin_conn.connect()

# Get target user
target_user_id = 10
user = admin_conn.getObject("Experimenter", target_user_id)
username = user.getOmeName()

# Create connection as that user
user_conn = admin_conn.suConn(username)

print(f"Connected as {username}")

# Perform operations as that user
for project in user_conn.listProjects():
    print(f"  {project.getName()}")

# Close connections
user_conn.close()
admin_conn.close()
```

### List All Users

```python
# Get all users (admin operation)
print("All users:")
for user in conn.getObjects("Experimenter"):
    print(f"  ID: {user.getId()}")
    print(f"  Username: {user.getOmeName()}")
    print(f"  Full Name: {user.getFullName()}")
    print(f"  Email: {user.getEmail()}")
    print()
```

## Service Access

OMERO provides various services for specific operations.

### Update Service

```python
# Get update service
updateService = conn.getUpdateService()

# Save and return object
roi = omero.model.RoiI()
roi.setImage(image._obj)
saved_roi = updateService.saveAndReturnObject(roi)

# Save multiple objects
objects = [obj1, obj2, obj3]
saved_objects = updateService.saveAndReturnArray(objects)
```

### ROI Service

```python
# Get ROI service
roi_service = conn.getRoiService()

# Find ROIs for image
result = roi_service.findByImage(image_id, None)

# Get shape statistics
shape_ids = [shape.id.val for roi in result.rois
             for shape in roi.copyShapes()]
stats = roi_service.getShapeStatsRestricted(shape_ids, 0, 0, [0])
```

### Metadata Service

```python
# Get metadata service
metadataService = conn.getMetadataService()

# Load annotations by type and namespace
ns_to_include = ["mylab.analysis"]
ns_to_exclude = []

annotations = metadataService.loadSpecifiedAnnotations(
    'omero.model.FileAnnotation',
    ns_to_include,
    ns_to_exclude,
    None
)

for ann in annotations:
    print(f"Annotation: {ann.getId().getValue()}")
```

### Query Service

```python
# Get query service
queryService = conn.getQueryService()

# Build query (more complex queries)
params = omero.sys.ParametersI()
params.addLong("image_id", image_id)

query = "select i from Image i where i.id = :image_id"
image = queryService.findByQuery(query, params)
```

### Thumbnail Service

```python
# Get thumbnail service
thumbnailService = conn.createThumbnailStore()

# Set current image
thumbnailService.setPixelsId(image.getPrimaryPixels().getId())

# Get thumbnail
thumbnail = thumbnailService.getThumbnail(96, 96)

# Close service
thumbnailService.close()
```

### Raw File Store

```python
# Get raw file store
rawFileStore = conn.createRawFileStore()

# Set file ID
rawFileStore.setFileId(orig_file_id)

# Read file
data = rawFileStore.read(0, rawFileStore.size())

# Close
rawFileStore.close()
```

## Object Ownership and Details

### Get Object Details

```python
image = conn.getObject("Image", image_id)

# Get details
details = image.getDetails()

# Owner information
owner = details.getOwner()
print(f"Owner ID: {owner.getId()}")
print(f"Username: {owner.getOmeName()}")
print(f"Full Name: {owner.getFullName()}")

# Group information
group = details.getGroup()
print(f"Group: {group.getName()} (ID: {group.getId()})")

# Creation information
creation_event = details.getCreationEvent()
print(f"Created: {creation_event.getTime()}")

# Update information
update_event = details.getUpdateEvent()
print(f"Updated: {update_event.getTime()}")
```

### Get Permissions

```python
# Get object permissions
details = image.getDetails()
permissions = details.getPermissions()

# Check specific permissions
can_edit = permissions.canEdit()
can_annotate = permissions.canAnnotate()
can_link = permissions.canLink()
can_delete = permissions.canDelete()

print(f"Can edit: {can_edit}")
print(f"Can annotate: {can_annotate}")
print(f"Can link: {can_link}")
print(f"Can delete: {can_delete}")
```

## Event Context

### Get Current Event Context

```python
# Get event context (current session info)
ctx = conn.getEventContext()

print(f"User ID: {ctx.userId}")
print(f"Username: {ctx.userName}")
print(f"Group ID: {ctx.groupId}")
print(f"Group Name: {ctx.groupName}")
print(f"Session ID: {ctx.sessionId}")
print(f"Is Admin: {ctx.isAdmin}")
```

## Complete Admin Example

```python
from omero.gateway import BlitzGateway

# Connect as admin
ADMIN_USER = 'root'
ADMIN_PASS = 'password'
HOST = 'omero.example.com'
PORT = 4064

with BlitzGateway(ADMIN_USER, ADMIN_PASS, host=HOST, port=PORT) as admin_conn:
    print("=== Administrator Operations ===\n")

    # List all users
    print("All Users:")
    for user in admin_conn.getObjects("Experimenter"):
        print(f"  {user.getOmeName()}: {user.getFullName()}")

    # List all groups
    print("\nAll Groups:")
    for group in admin_conn.getObjects("ExperimenterGroup"):
        perms = group.getDetails().getPermissions()
        print(f"  {group.getName()}: {perms}")

        # List members
        for member in group.getMembers():
            print(f"    - {member.getOmeName()}")

    # Query across all groups
    print("\nAll Projects (all groups):")
    admin_conn.SERVICE_OPTS.setOmeroGroup('-1')

    for project in admin_conn.getObjects("Project"):
        owner = project.getDetails().getOwner()
        group = project.getDetails().getGroup()
        print(f"  {project.getName()}")
        print(f"    Owner: {owner.getOmeName()}")
        print(f"    Group: {group.getName()}")

    # Connect as another user
    target_user_id = 5
    user = admin_conn.getObject("Experimenter", target_user_id)

    if user:
        print(f"\n=== Operating as {user.getOmeName()} ===\n")

        user_conn = admin_conn.suConn(user.getOmeName())

        # List that user's projects
        for project in user_conn.listProjects():
            print(f"  {project.getName()}")

        user_conn.close()
```

## Best Practices

1. **Permissions**: Always check permissions before operations
2. **Group Context**: Set appropriate group context for queries
3. **Admin Operations**: Use admin privileges sparingly and carefully
4. **Delete Confirmation**: Always confirm before deleting objects
5. **Callback Monitoring**: Monitor long delete operations with callbacks
6. **Fileset Awareness**: Check for filesets when working with images
7. **Service Cleanup**: Close services when done (thumbnailStore, rawFileStore)
8. **Cross-Group Queries**: Use `-1` group ID for cross-group access
9. **Error Handling**: Always handle permission and access errors
10. **Documentation**: Document administrative operations clearly

## Troubleshooting

### Permission Denied

```python
try:
    conn.deleteObjects("Project", [project_id], wait=True)
except Exception as e:
    if "SecurityViolation" in str(e):
        print("Permission denied: You don't own this object")
    else:
        raise
```

### Object Not Found

```python
# Check if object exists before accessing
obj = conn.getObject("Image", image_id)
if obj is None:
    print(f"Image {image_id} not found or not accessible")
else:
    # Process object
    pass
```

### Group Context Issues

```python
# If object not found, try cross-group query
conn.SERVICE_OPTS.setOmeroGroup('-1')
obj = conn.getObject("Image", image_id)

if obj:
    # Switch to object's group for further operations
    group_id = obj.getDetails().getGroup().getId()
    conn.SERVICE_OPTS.setOmeroGroup(group_id)
```

---

## Reference: Connection

# Connection & Session Management

This reference covers establishing and managing connections to OMERO servers using BlitzGateway.

## Basic Connection

### Standard Connection Pattern

```python
from omero.gateway import BlitzGateway

# Create connection
conn = BlitzGateway(username, password, host=host, port=4064)

# Connect to server
if conn.connect():
    print("Connected successfully")
    # Perform operations
    conn.close()
else:
    print("Failed to connect")
```

### Connection Parameters

- **username** (str): OMERO user account name
- **password** (str): User password
- **host** (str): OMERO server hostname or IP address
- **port** (int): Server port (default: 4064)
- **secure** (bool): Force encrypted connection (default: False)

### Secure Connection

To ensure all data transfers are encrypted:

```python
conn = BlitzGateway(username, password, host=host, port=4064, secure=True)
conn.connect()
```

## Context Manager Pattern (Recommended)

Use context managers for automatic connection management and cleanup:

```python
from omero.gateway import BlitzGateway

with BlitzGateway(username, password, host=host, port=4064) as conn:
    # Connection automatically established
    for project in conn.getObjects('Project'):
        print(project.getName())
    # Connection automatically closed on exit
```

**Benefits:**
- Automatic `connect()` call
- Automatic `close()` call on exit
- Exception-safe resource cleanup
- Cleaner code

## Session Management

### Connection from Existing Client

Create BlitzGateway from an existing `omero.client` session:

```python
import omero.clients
from omero.gateway import BlitzGateway

# Create client and session
client = omero.client(host, port)
session = client.createSession(username, password)

# Create BlitzGateway from existing client
conn = BlitzGateway(client_obj=client)

# Use connection
# ...

# Close when done
conn.close()
```

### Retrieve Session Information

```python
# Get current user information
user = conn.getUser()
print(f"User ID: {user.getId()}")
print(f"Username: {user.getName()}")
print(f"Full Name: {user.getFullName()}")
print(f"Is Admin: {conn.isAdmin()}")

# Get current group
group = conn.getGroupFromContext()
print(f"Current Group: {group.getName()}")
print(f"Group ID: {group.getId()}")
```

### Check Admin Privileges

```python
if conn.isAdmin():
    print("User has admin privileges")

if conn.isFullAdmin():
    print("User is full administrator")
else:
    # Check specific admin privileges
    privileges = conn.getCurrentAdminPrivileges()
    print(f"Admin privileges: {privileges}")
```

## Group Context Management

OMERO uses groups to manage data access permissions. Users can belong to multiple groups.

### Get Current Group Context

```python
# Get the current group context
group = conn.getGroupFromContext()
print(f"Current group: {group.getName()}")
print(f"Group ID: {group.getId()}")
```

### Query Across All Groups

Use group ID `-1` to query across all accessible groups:

```python
# Set context to query all groups
conn.SERVICE_OPTS.setOmeroGroup('-1')

# Now queries span all accessible groups
image = conn.getObject("Image", image_id)
projects = conn.listProjects()
```

### Switch to Specific Group

Switch context to work within a specific group:

```python
# Get group ID from an object
image = conn.getObject("Image", image_id)
group_id = image.getDetails().getGroup().getId()

# Switch to that group's context
conn.SERVICE_OPTS.setOmeroGroup(group_id)

# Subsequent operations use this group context
projects = conn.listProjects()
```

### List Available Groups

```python
# Get all groups for current user
for group in conn.getGroupsMemberOf():
    print(f"Group: {group.getName()} (ID: {group.getId()})")
```

## Advanced Connection Features

### Substitute User Connection (Admin Only)

Administrators can create connections acting as other users:

```python
# Connect as admin
admin_conn = BlitzGateway(admin_user, admin_pass, host=host, port=4064)
admin_conn.connect()

# Get target user
target_user = admin_conn.getObject("Experimenter", user_id).getName()

# Create connection as that user
user_conn = admin_conn.suConn(target_user)

# Operations performed as target user
for project in user_conn.listProjects():
    print(project.getName())

# Close substitute connection
user_conn.close()
admin_conn.close()
```

### List Administrators

```python
# Get all administrators
for admin in conn.getAdministrators():
    print(f"ID: {admin.getId()}, Name: {admin.getFullName()}, "
          f"Username: {admin.getOmeName()}")
```

## Connection Lifecycle

### Closing Connections

Always close connections to free server resources:

```python
try:
    conn = BlitzGateway(username, password, host=host, port=4064)
    conn.connect()

    # Perform operations

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
```

### Check Connection Status

```python
if conn.isConnected():
    print("Connection is active")
else:
    print("Connection is closed")
```

## Error Handling

### Robust Connection Pattern

```python
from omero.gateway import BlitzGateway
import traceback

def connect_to_omero(username, password, host, port=4064):
    """
    Establish connection to OMERO server with error handling.

    Returns:
        BlitzGateway connection object or None if failed
    """
    try:
        conn = BlitzGateway(username, password, host=host, port=port, secure=True)
        if conn.connect():
            print(f"Connected to {host}:{port} as {username}")
            return conn
        else:
            print("Failed to establish connection")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        traceback.print_exc()
        return None

# Usage
conn = connect_to_omero(username, password, host)
if conn:
    try:
        # Perform operations
        pass
    finally:
        conn.close()
```

## Common Connection Patterns

### Pattern 1: Simple Script

```python
from omero.gateway import BlitzGateway

# Connection parameters
HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

# Connect
with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    print(f"Connected as {conn.getUser().getName()}")
    # Perform operations
```

### Pattern 2: Configuration-Based Connection

```python
import yaml
from omero.gateway import BlitzGateway

# Load configuration
with open('omero_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connect using config
with BlitzGateway(
    config['username'],
    config['password'],
    host=config['host'],
    port=config.get('port', 4064),
    secure=config.get('secure', True)
) as conn:
    # Perform operations
    pass
```

### Pattern 3: Environment Variables

```python
import os
from omero.gateway import BlitzGateway

# Get credentials from environment
USERNAME = os.environ.get('OMERO_USER')
PASSWORD = os.environ.get('OMERO_PASSWORD')
HOST = os.environ.get('OMERO_HOST', 'localhost')
PORT = int(os.environ.get('OMERO_PORT', 4064))

# Connect
with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Perform operations
    pass
```

## Best Practices

1. **Use Context Managers**: Always prefer context managers for automatic cleanup
2. **Secure Connections**: Use `secure=True` for production environments
3. **Error Handling**: Wrap connection code in try-except blocks
4. **Close Connections**: Always close connections when done
5. **Group Context**: Set appropriate group context before queries
6. **Credential Security**: Never hardcode credentials; use environment variables or config files
7. **Connection Pooling**: For web applications, implement connection pooling
8. **Timeouts**: Consider implementing connection timeouts for long-running operations

## Troubleshooting

### Connection Refused

```
Unable to contact ORB
```

**Solutions:**
- Verify host and port are correct
- Check firewall settings
- Ensure OMERO server is running
- Verify network connectivity

### Authentication Failed

```
Cannot connect to server
```

**Solutions:**
- Verify username and password
- Check user account is active
- Verify group membership
- Check server logs for details

### Session Timeout

**Solutions:**
- Increase session timeout on server
- Implement session keepalive
- Reconnect on timeout
- Use connection pools for long-running applications

---

## Reference: Data_Access

# Data Access & Retrieval

This reference covers navigating OMERO's hierarchical data structure and retrieving objects.

## OMERO Data Hierarchy

### Standard Hierarchy

```
Project
  └─ Dataset
       └─ Image
```

### Screening Hierarchy

```
Screen
  └─ Plate
       └─ Well
            └─ WellSample
                 └─ Image
```

## Listing Objects

### List Projects

```python
# List all projects for current user
for project in conn.listProjects():
    print(f"Project: {project.getName()} (ID: {project.getId()})")
```

### List Projects with Filtering

```python
# Get current user and group
my_exp_id = conn.getUser().getId()
default_group_id = conn.getEventContext().groupId

# List projects with filters
for project in conn.getObjects("Project", opts={
    'owner': my_exp_id,                    # Filter by owner
    'group': default_group_id,             # Filter by group
    'order_by': 'lower(obj.name)',         # Sort alphabetically
    'limit': 10,                           # Limit results
    'offset': 0                            # Pagination offset
}):
    print(f"Project: {project.getName()}")
```

### List Datasets

```python
# List all datasets
for dataset in conn.getObjects("Dataset"):
    print(f"Dataset: {dataset.getName()} (ID: {dataset.getId()})")

# List orphaned datasets (not in any project)
for dataset in conn.getObjects("Dataset", opts={'orphaned': True}):
    print(f"Orphaned Dataset: {dataset.getName()}")
```

### List Images

```python
# List all images
for image in conn.getObjects("Image"):
    print(f"Image: {image.getName()} (ID: {image.getId()})")

# List images in specific dataset
dataset_id = 123
for image in conn.getObjects("Image", opts={'dataset': dataset_id}):
    print(f"Image: {image.getName()}")

# List orphaned images
for image in conn.getObjects("Image", opts={'orphaned': True}):
    print(f"Orphaned Image: {image.getName()}")
```

## Retrieving Objects by ID

### Get Single Object

```python
# Get project by ID
project = conn.getObject("Project", project_id)
if project:
    print(f"Project: {project.getName()}")
else:
    print("Project not found")

# Get dataset by ID
dataset = conn.getObject("Dataset", dataset_id)

# Get image by ID
image = conn.getObject("Image", image_id)
```

### Get Multiple Objects by ID

```python
# Get multiple projects at once
project_ids = [1, 2, 3, 4, 5]
projects = conn.getObjects("Project", project_ids)

for project in projects:
    print(f"Project: {project.getName()}")
```

### Supported Object Types

The `getObject()` and `getObjects()` methods support:
- `"Project"`
- `"Dataset"`
- `"Image"`
- `"Screen"`
- `"Plate"`
- `"Well"`
- `"Roi"`
- `"Annotation"` (and specific types: `"TagAnnotation"`, `"FileAnnotation"`, etc.)
- `"Experimenter"`
- `"ExperimenterGroup"`
- `"Fileset"`

## Query by Attributes

### Query Objects by Name

```python
# Find images with specific name
images = conn.getObjects("Image", attributes={"name": "sample_001.tif"})

for image in images:
    print(f"Found image: {image.getName()} (ID: {image.getId()})")

# Find datasets with specific name
datasets = conn.getObjects("Dataset", attributes={"name": "Control Group"})
```

### Query Annotations by Value

```python
# Find tags with specific text value
tags = conn.getObjects("TagAnnotation",
                      attributes={"textValue": "experiment_tag"})

for tag in tags:
    print(f"Tag: {tag.getValue()}")

# Find map annotations
map_anns = conn.getObjects("MapAnnotation",
                          attributes={"ns": "custom.namespace"})
```

## Navigating Hierarchies

### Navigate Down (Parent to Children)

```python
# Project → Datasets → Images
project = conn.getObject("Project", project_id)

for dataset in project.listChildren():
    print(f"Dataset: {dataset.getName()}")

    for image in dataset.listChildren():
        print(f"  Image: {image.getName()}")
```

### Navigate Up (Child to Parent)

```python
# Image → Dataset → Project
image = conn.getObject("Image", image_id)

# Get parent dataset
dataset = image.getParent()
if dataset:
    print(f"Dataset: {dataset.getName()}")

    # Get parent project
    project = dataset.getParent()
    if project:
        print(f"Project: {project.getName()}")
```

### Complete Hierarchy Traversal

```python
# Traverse complete project hierarchy
for project in conn.getObjects("Project", opts={'order_by': 'lower(obj.name)'}):
    print(f"Project: {project.getName()} (ID: {project.getId()})")

    for dataset in project.listChildren():
        image_count = dataset.countChildren()
        print(f"  Dataset: {dataset.getName()} ({image_count} images)")

        for image in dataset.listChildren():
            print(f"    Image: {image.getName()}")
            print(f"      Size: {image.getSizeX()} x {image.getSizeY()}")
            print(f"      Channels: {image.getSizeC()}")
```

## Screening Data Access

### List Screens and Plates

```python
# List all screens
for screen in conn.getObjects("Screen"):
    print(f"Screen: {screen.getName()} (ID: {screen.getId()})")

    # List plates in screen
    for plate in screen.listChildren():
        print(f"  Plate: {plate.getName()} (ID: {plate.getId()})")
```

### Access Plate Wells

```python
# Get plate
plate = conn.getObject("Plate", plate_id)

# Plate metadata
print(f"Plate: {plate.getName()}")
print(f"Grid size: {plate.getGridSize()}")  # e.g., (8, 12) for 96-well
print(f"Number of fields: {plate.getNumberOfFields()}")

# Iterate through wells
for well in plate.listChildren():
    print(f"Well at row {well.row}, column {well.column}")

    # Count images in well (fields)
    field_count = well.countWellSample()
    print(f"  Number of fields: {field_count}")

    # Access images in well
    for index in range(field_count):
        image = well.getImage(index)
        print(f"    Field {index}: {image.getName()}")
```

### Direct Well Access

```python
# Get specific well by row and column
well = plate.getWell(row=0, column=0)  # Top-left well

# Get image from well
if well.countWellSample() > 0:
    image = well.getImage(0)  # First field
    print(f"Image: {image.getName()}")
```

### Well Sample Access

```python
# Access well samples directly
for well in plate.listChildren():
    for ws in well.listChildren():  # ws = WellSample
        image = ws.getImage()
        print(f"WellSample {ws.getId()}: {image.getName()}")
```

## Image Properties

### Basic Dimensions

```python
image = conn.getObject("Image", image_id)

# Pixel dimensions
print(f"X: {image.getSizeX()}")
print(f"Y: {image.getSizeY()}")
print(f"Z: {image.getSizeZ()} (Z-sections)")
print(f"C: {image.getSizeC()} (Channels)")
print(f"T: {image.getSizeT()} (Time points)")

# Image type
print(f"Type: {image.getPixelsType()}")  # e.g., 'uint16', 'uint8'
```

### Physical Dimensions

```python
# Get pixel sizes with units (OMERO 5.1.0+)
size_x_obj = image.getPixelSizeX(units=True)
size_y_obj = image.getPixelSizeY(units=True)
size_z_obj = image.getPixelSizeZ(units=True)

print(f"Pixel Size X: {size_x_obj.getValue()} {size_x_obj.getSymbol()}")
print(f"Pixel Size Y: {size_y_obj.getValue()} {size_y_obj.getSymbol()}")
print(f"Pixel Size Z: {size_z_obj.getValue()} {size_z_obj.getSymbol()}")

# Get as floats (micrometers)
size_x = image.getPixelSizeX()  # Returns float in µm
size_y = image.getPixelSizeY()
size_z = image.getPixelSizeZ()
```

### Channel Information

```python
# Iterate through channels
for channel in image.getChannels():
    print(f"Channel {channel.getLabel()}:")
    print(f"  Color: {channel.getColor().getRGB()}")
    print(f"  Lookup Table: {channel.getLut()}")
    print(f"  Wavelength: {channel.getEmissionWave()}")
```

### Image Metadata

```python
# Acquisition date
acquired = image.getAcquisitionDate()
if acquired:
    print(f"Acquired: {acquired}")

# Description
description = image.getDescription()
if description:
    print(f"Description: {description}")

# Owner and group
details = image.getDetails()
print(f"Owner: {details.getOwner().getFullName()}")
print(f"Username: {details.getOwner().getOmeName()}")
print(f"Group: {details.getGroup().getName()}")
print(f"Created: {details.getCreationEvent().getTime()}")
```

## Object Ownership and Permissions

### Get Owner Information

```python
# Get object owner
obj = conn.getObject("Dataset", dataset_id)
owner = obj.getDetails().getOwner()

print(f"Owner ID: {owner.getId()}")
print(f"Username: {owner.getOmeName()}")
print(f"Full Name: {owner.getFullName()}")
print(f"Email: {owner.getEmail()}")
```

### Get Group Information

```python
# Get object's group
obj = conn.getObject("Image", image_id)
group = obj.getDetails().getGroup()

print(f"Group: {group.getName()} (ID: {group.getId()})")
```

### Filter by Owner

```python
# Get objects for specific user
user_id = 5
datasets = conn.getObjects("Dataset", opts={'owner': user_id})

for dataset in datasets:
    print(f"Dataset: {dataset.getName()}")
```

## Advanced Queries

### Pagination

```python
# Paginate through large result sets
page_size = 50
offset = 0

while True:
    images = list(conn.getObjects("Image", opts={
        'limit': page_size,
        'offset': offset,
        'order_by': 'obj.id'
    }))

    if not images:
        break

    for image in images:
        print(f"Image: {image.getName()}")

    offset += page_size
```

### Sorting Results

```python
# Sort by name (case-insensitive)
projects = conn.getObjects("Project", opts={
    'order_by': 'lower(obj.name)'
})

# Sort by ID (ascending)
datasets = conn.getObjects("Dataset", opts={
    'order_by': 'obj.id'
})

# Sort by name (descending)
images = conn.getObjects("Image", opts={
    'order_by': 'lower(obj.name) desc'
})
```

### Combining Filters

```python
# Complex query with multiple filters
my_exp_id = conn.getUser().getId()
default_group_id = conn.getEventContext().groupId

images = conn.getObjects("Image", opts={
    'owner': my_exp_id,
    'group': default_group_id,
    'dataset': dataset_id,
    'order_by': 'lower(obj.name)',
    'limit': 100,
    'offset': 0
})
```

## Counting Objects

### Count Children

```python
# Count images in dataset
dataset = conn.getObject("Dataset", dataset_id)
image_count = dataset.countChildren()
print(f"Dataset contains {image_count} images")

# Count datasets in project
project = conn.getObject("Project", project_id)
dataset_count = project.countChildren()
print(f"Project contains {dataset_count} datasets")
```

### Count Annotations

```python
# Count annotations on object
image = conn.getObject("Image", image_id)
annotation_count = image.countAnnotations()
print(f"Image has {annotation_count} annotations")
```

## Orphaned Objects

### Find Orphaned Datasets

```python
# Datasets not linked to any project
orphaned_datasets = conn.getObjects("Dataset", opts={'orphaned': True})

print("Orphaned Datasets:")
for dataset in orphaned_datasets:
    print(f"  {dataset.getName()} (ID: {dataset.getId()})")
    print(f"    Owner: {dataset.getDetails().getOwner().getOmeName()}")
    print(f"    Images: {dataset.countChildren()}")
```

### Find Orphaned Images

```python
# Images not in any dataset
orphaned_images = conn.getObjects("Image", opts={'orphaned': True})

print("Orphaned Images:")
for image in orphaned_images:
    print(f"  {image.getName()} (ID: {image.getId()})")
```

### Find Orphaned Plates

```python
# Plates not in any screen
orphaned_plates = conn.getObjects("Plate", opts={'orphaned': True})

for plate in orphaned_plates:
    print(f"Orphaned Plate: {plate.getName()}")
```

## Complete Example

```python
from omero.gateway import BlitzGateway

# Connection details
HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

# Connect and query data
with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get user context
    user = conn.getUser()
    group = conn.getGroupFromContext()

    print(f"Connected as {user.getName()} in group {group.getName()}")
    print()

    # List projects with datasets and images
    for project in conn.getObjects("Project", opts={'limit': 5}):
        print(f"Project: {project.getName()} (ID: {project.getId()})")

        for dataset in project.listChildren():
            image_count = dataset.countChildren()
            print(f"  Dataset: {dataset.getName()} ({image_count} images)")

            # Show first 3 images
            for idx, image in enumerate(dataset.listChildren()):
                if idx >= 3:
                    print(f"    ... and {image_count - 3} more")
                    break
                print(f"    Image: {image.getName()}")
                print(f"      Size: {image.getSizeX()}x{image.getSizeY()}")
                print(f"      Channels: {image.getSizeC()}, Z: {image.getSizeZ()}")

        print()
```

## Best Practices

1. **Use Context Managers**: Always use `with` statements for automatic connection cleanup
2. **Limit Results**: Use `limit` and `offset` for large datasets
3. **Filter Early**: Apply filters to reduce data transfer
4. **Check for None**: Always check if `getObject()` returns None before using
5. **Efficient Traversal**: Use `listChildren()` instead of querying separately
6. **Count Before Loading**: Use `countChildren()` to decide whether to load data
7. **Group Context**: Set appropriate group context before cross-group queries
8. **Pagination**: Implement pagination for large result sets
9. **Object Reuse**: Cache frequently accessed objects to reduce queries
10. **Error Handling**: Wrap queries in try-except blocks for robustness

---

## Reference: Image_Processing

# Image Processing & Rendering

This reference covers accessing raw pixel data, image rendering, and creating new images in OMERO.

## Accessing Raw Pixel Data

### Get Single Plane

```python
# Get image
image = conn.getObject("Image", image_id)

# Get dimensions
size_z = image.getSizeZ()
size_c = image.getSizeC()
size_t = image.getSizeT()

# Get pixels object
pixels = image.getPrimaryPixels()

# Get single plane (returns NumPy array)
z, c, t = 0, 0, 0  # First Z-section, channel, and timepoint
plane = pixels.getPlane(z, c, t)

print(f"Shape: {plane.shape}")
print(f"Data type: {plane.dtype.name}")
print(f"Min: {plane.min()}, Max: {plane.max()}")
```

### Get Multiple Planes

```python
import numpy as np

# Get Z-stack for specific channel and timepoint
pixels = image.getPrimaryPixels()
c, t = 0, 0  # First channel and timepoint

# Build list of (z, c, t) coordinates
zct_list = [(z, c, t) for z in range(size_z)]

# Get all planes at once
planes = pixels.getPlanes(zct_list)

# Stack into 3D array
z_stack = np.array([p for p in planes])
print(f"Z-stack shape: {z_stack.shape}")
```

### Get Hypercube (Subset of 5D Data)

```python
# Get subset of 5D data (Z, C, T)
zct_list = []
for z in range(size_z // 2, size_z):  # Second half of Z
    for c in range(size_c):           # All channels
        for t in range(size_t):       # All timepoints
            zct_list.append((z, c, t))

# Get planes
planes = pixels.getPlanes(zct_list)

# Process each plane
for i, plane in enumerate(planes):
    z, c, t = zct_list[i]
    print(f"Plane Z={z}, C={c}, T={t}: Min={plane.min()}, Max={plane.max()}")
```

### Get Tile (Region of Interest)

```python
# Define tile coordinates
x, y = 50, 50          # Top-left corner
width, height = 100, 100  # Tile size
tile = (x, y, width, height)

# Get tile for specific Z, C, T
z, c, t = 0, 0, 0
zct_list = [(z, c, t, tile)]

tiles = pixels.getTiles(zct_list)
tile_data = tiles[0]

print(f"Tile shape: {tile_data.shape}")  # Should be (height, width)
```

### Get Multiple Tiles

```python
# Get tiles from Z-stack
c, t = 0, 0
tile = (50, 50, 100, 100)  # x, y, width, height

# Build list with tiles
zct_list = [(z, c, t, tile) for z in range(size_z)]

tiles = pixels.getTiles(zct_list)

for i, tile_data in enumerate(tiles):
    print(f"Tile Z={i}: {tile_data.shape}, Min={tile_data.min()}")
```

## Image Histograms

### Get Histogram

```python
# Get histogram for first channel
channel_index = 0
num_bins = 256
z, t = 0, 0

histogram = image.getHistogram([channel_index], num_bins, False, z, t)
print(f"Histogram bins: {len(histogram)}")
print(f"First 10 bins: {histogram[:10]}")
```

### Multi-Channel Histogram

```python
# Get histograms for all channels
channels = list(range(image.getSizeC()))
histograms = image.getHistogram(channels, 256, False, 0, 0)

for c, hist in enumerate(histograms):
    print(f"Channel {c}: Total pixels = {sum(hist)}")
```

## Image Rendering

### Render Image with Current Settings

```python
from PIL import Image
from io import BytesIO

# Get image
image = conn.getObject("Image", image_id)

# Render at specific Z and T
z = image.getSizeZ() // 2  # Middle Z-section
t = 0

rendered_image = image.renderImage(z, t)
# rendered_image is a PIL Image object
rendered_image.save("rendered_image.jpg")
```

### Get Thumbnail

```python
from PIL import Image
from io import BytesIO

# Get thumbnail (uses current rendering settings)
thumbnail_data = image.getThumbnail()

# Convert to PIL Image
thumbnail = Image.open(BytesIO(thumbnail_data))
thumbnail.save("thumbnail.jpg")

# Get specific thumbnail size
thumbnail_data = image.getThumbnail(size=(96, 96))
thumbnail = Image.open(BytesIO(thumbnail_data))
```

## Rendering Settings

### View Current Settings

```python
# Display rendering settings
print("Current Rendering Settings:")
print(f"Grayscale mode: {image.isGreyscaleRenderingModel()}")
print(f"Default Z: {image.getDefaultZ()}")
print(f"Default T: {image.getDefaultT()}")
print()

# Channel settings
print("Channel Settings:")
for idx, channel in enumerate(image.getChannels()):
    print(f"Channel {idx + 1}:")
    print(f"  Label: {channel.getLabel()}")
    print(f"  Color: {channel.getColor().getHtml()}")
    print(f"  Active: {channel.isActive()}")
    print(f"  Window: {channel.getWindowStart()} - {channel.getWindowEnd()}")
    print(f"  Min/Max: {channel.getWindowMin()} - {channel.getWindowMax()}")
```

### Set Rendering Model

```python
# Switch to grayscale rendering
image.setGreyscaleRenderingModel()

# Switch to color rendering
image.setColorRenderingModel()
```

### Set Active Channels

```python
# Activate specific channels (1-indexed)
image.setActiveChannels([1, 3])  # Channels 1 and 3 only

# Activate all channels
all_channels = list(range(1, image.getSizeC() + 1))
image.setActiveChannels(all_channels)

# Activate single channel
image.setActiveChannels([2])
```

### Set Channel Colors

```python
# Set channel colors (hex format)
channels = [1, 2, 3]
colors = ['FF0000', '00FF00', '0000FF']  # Red, Green, Blue

image.setActiveChannels(channels, colors=colors)

# Use None to keep existing color
colors = ['FF0000', None, '0000FF']  # Keep channel 2's color
image.setActiveChannels(channels, colors=colors)
```

### Set Channel Window (Intensity Range)

```python
# Set intensity windows for channels
channels = [1, 2]
windows = [
    [100.0, 500.0],  # Channel 1: 100-500
    [50.0, 300.0]    # Channel 2: 50-300
]

image.setActiveChannels(channels, windows=windows)

# Use None to keep existing window
windows = [[100.0, 500.0], [None, None]]
image.setActiveChannels(channels, windows=windows)
```

### Set Default Z and T

```python
# Set default Z-section and timepoint
image.setDefaultZ(5)
image.setDefaultT(0)

# Render using defaults
rendered_image = image.renderImage(z=None, t=None)
rendered_image.save("default_rendering.jpg")
```

## Render Individual Channels

### Render Each Channel Separately

```python
# Set grayscale mode
image.setGreyscaleRenderingModel()

z = image.getSizeZ() // 2
t = 0

# Render each channel
for c in range(1, image.getSizeC() + 1):
    image.setActiveChannels([c])
    rendered = image.renderImage(z, t)
    rendered.save(f"channel_{c}.jpg")
```

### Render Multi-Channel Composites

```python
# Color composite of first 3 channels
image.setColorRenderingModel()
channels = [1, 2, 3]
colors = ['FF0000', '00FF00', '0000FF']  # RGB

image.setActiveChannels(channels, colors=colors)
rendered = image.renderImage(z, t)
rendered.save("rgb_composite.jpg")
```

## Image Projections

### Maximum Intensity Projection

```python
# Set projection type
image.setProjection('intmax')

# Render (projects across all Z)
z, t = 0, 0  # Z is ignored for projections
rendered = image.renderImage(z, t)
rendered.save("max_projection.jpg")

# Reset to normal rendering
image.setProjection('normal')
```

### Mean Intensity Projection

```python
image.setProjection('intmean')
rendered = image.renderImage(z, t)
rendered.save("mean_projection.jpg")
image.setProjection('normal')
```

### Available Projection Types

- `'normal'`: No projection (default)
- `'intmax'`: Maximum intensity projection
- `'intmean'`: Mean intensity projection
- `'intmin'`: Minimum intensity projection (if supported)

## Save and Reset Rendering Settings

### Save Current Settings as Default

```python
# Modify rendering settings
image.setActiveChannels([1, 2])
image.setDefaultZ(5)

# Save as new default
image.saveDefaults()
```

### Reset to Import Settings

```python
# Reset to original import settings
image.resetDefaults(save=True)
```

## Create Images from NumPy Arrays

### Create Simple Image

```python
import numpy as np

# Create sample data
size_x, size_y = 512, 512
size_z, size_c, size_t = 10, 2, 1

# Generate planes
def plane_generator():
    """Generator that yields planes"""
    for z in range(size_z):
        for c in range(size_c):
            for t in range(size_t):
                # Create synthetic data
                plane = np.random.randint(0, 255, (size_y, size_x), dtype=np.uint8)
                yield plane

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "Test Image",
    size_z, size_c, size_t,
    description="Image created from NumPy arrays",
    dataset=None
)

print(f"Created image ID: {image.getId()}")
```

### Create Image from Hard-Coded Arrays

```python
from numpy import array, int8

# Define dimensions
size_x, size_y = 5, 4
size_z, size_c, size_t = 1, 2, 1

# Create planes
plane1 = array(
    [[0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9]],
    dtype=int8
)

plane2 = array(
    [[5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9],
     [0, 1, 2, 3, 4]],
    dtype=int8
)

planes = [plane1, plane2]

def plane_gen():
    for p in planes:
        yield p

# Create image
desc = "Image created from hard-coded arrays"
image = conn.createImageFromNumpySeq(
    plane_gen(),
    "numpy_image",
    size_z, size_c, size_t,
    description=desc,
    dataset=None
)

print(f"Created image: {image.getName()} (ID: {image.getId()})")
```

### Create Image in Dataset

```python
# Get target dataset
dataset = conn.getObject("Dataset", dataset_id)

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "New Analysis Result",
    size_z, size_c, size_t,
    description="Result from analysis pipeline",
    dataset=dataset  # Add to dataset
)
```

### Create Derived Image

```python
# Get source image
source = conn.getObject("Image", source_image_id)
size_z = source.getSizeZ()
size_c = source.getSizeC()
size_t = source.getSizeT()
dataset = source.getParent()

pixels = source.getPrimaryPixels()
new_size_c = 1  # Average channels

def plane_gen():
    """Average channels together"""
    for z in range(size_z):
        for c in range(new_size_c):
            for t in range(size_t):
                # Get multiple channels
                channel0 = pixels.getPlane(z, 0, t)
                channel1 = pixels.getPlane(z, 1, t)

                # Combine
                new_plane = (channel0.astype(float) + channel1.astype(float)) / 2
                new_plane = new_plane.astype(channel0.dtype)

                yield new_plane

# Create new image
desc = "Averaged channels from source image"
derived = conn.createImageFromNumpySeq(
    plane_gen(),
    f"{source.getName()}_averaged",
    size_z, new_size_c, size_t,
    description=desc,
    dataset=dataset
)

print(f"Created derived image: {derived.getId()}")
```

## Set Physical Dimensions

### Set Pixel Sizes with Units

```python
from omero.model.enums import UnitsLength
import omero.model

# Get image
image = conn.getObject("Image", image_id)

# Create unit objects
pixel_size_x = omero.model.LengthI(0.325, UnitsLength.MICROMETER)
pixel_size_y = omero.model.LengthI(0.325, UnitsLength.MICROMETER)
pixel_size_z = omero.model.LengthI(1.0, UnitsLength.MICROMETER)

# Get pixels object
pixels = image.getPrimaryPixels()._obj

# Set physical sizes
pixels.setPhysicalSizeX(pixel_size_x)
pixels.setPhysicalSizeY(pixel_size_y)
pixels.setPhysicalSizeZ(pixel_size_z)

# Save changes
conn.getUpdateService().saveObject(pixels)

print("Updated pixel dimensions")
```

### Available Length Units

From `omero.model.enums.UnitsLength`:
- `ANGSTROM`
- `NANOMETER`
- `MICROMETER`
- `MILLIMETER`
- `CENTIMETER`
- `METER`
- `PIXEL`

### Set Pixel Size on New Image

```python
from omero.model.enums import UnitsLength
import omero.model

# Create image
image = conn.createImageFromNumpySeq(
    plane_generator(),
    "New Image with Dimensions",
    size_z, size_c, size_t
)

# Set pixel sizes
pixel_size = omero.model.LengthI(0.5, UnitsLength.MICROMETER)
pixels = image.getPrimaryPixels()._obj
pixels.setPhysicalSizeX(pixel_size)
pixels.setPhysicalSizeY(pixel_size)

z_size = omero.model.LengthI(2.0, UnitsLength.MICROMETER)
pixels.setPhysicalSizeZ(z_size)

conn.getUpdateService().saveObject(pixels)
```

## Complete Example: Image Processing Pipeline

```python
from omero.gateway import BlitzGateway
import numpy as np

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get source image
    source = conn.getObject("Image", source_image_id)
    print(f"Processing: {source.getName()}")

    # Get dimensions
    size_x = source.getSizeX()
    size_y = source.getSizeY()
    size_z = source.getSizeZ()
    size_c = source.getSizeC()
    size_t = source.getSizeT()

    pixels = source.getPrimaryPixels()

    # Process: Maximum intensity projection over Z
    def plane_gen():
        for c in range(size_c):
            for t in range(size_t):
                # Get all Z planes for this C, T
                z_stack = []
                for z in range(size_z):
                    plane = pixels.getPlane(z, c, t)
                    z_stack.append(plane)

                # Maximum projection
                max_proj = np.max(z_stack, axis=0)
                yield max_proj

    # Create result image (single Z-section)
    result = conn.createImageFromNumpySeq(
        plane_gen(),
        f"{source.getName()}_MIP",
        1, size_c, size_t,  # Z=1 for projection
        description="Maximum intensity projection",
        dataset=source.getParent()
    )

    print(f"Created MIP image: {result.getId()}")

    # Copy pixel sizes (X and Y only, no Z for projection)
    from omero.model.enums import UnitsLength
    import omero.model

    source_pixels = source.getPrimaryPixels()._obj
    result_pixels = result.getPrimaryPixels()._obj

    result_pixels.setPhysicalSizeX(source_pixels.getPhysicalSizeX())
    result_pixels.setPhysicalSizeY(source_pixels.getPhysicalSizeY())

    conn.getUpdateService().saveObject(result_pixels)

    print("Processing complete")
```

## Working with Different Data Types

### Handle Various Pixel Types

```python
# Get pixel type
pixel_type = image.getPixelsType()
print(f"Pixel type: {pixel_type}")

# Common types: uint8, uint16, uint32, int8, int16, int32, float, double

# Get plane with correct dtype
plane = pixels.getPlane(z, c, t)
print(f"NumPy dtype: {plane.dtype}")

# Convert if needed for processing
if plane.dtype == np.uint16:
    # Convert to float for processing
    plane_float = plane.astype(np.float32)
    # Process...
    # Convert back
    result = plane_float.astype(np.uint16)
```

### Handle Large Images

```python
# Process large images in tiles to save memory
tile_size = 512
size_x = image.getSizeX()
size_y = image.getSizeY()

for y in range(0, size_y, tile_size):
    for x in range(0, size_x, tile_size):
        # Get tile dimensions
        w = min(tile_size, size_x - x)
        h = min(tile_size, size_y - y)
        tile = (x, y, w, h)

        # Get tile data
        zct_list = [(z, c, t, tile)]
        tile_data = pixels.getTiles(zct_list)[0]

        # Process tile
        # ...
```

## Best Practices

1. **Use Generators**: For creating images, use generators to avoid loading all data in memory
2. **Specify Data Types**: Match NumPy dtypes to OMERO pixel types
3. **Set Physical Dimensions**: Always set pixel sizes for new images
4. **Tile Large Images**: Process large images in tiles to manage memory
5. **Close Connections**: Always close connections when done
6. **Rendering Efficiency**: Cache rendering settings when rendering multiple images
7. **Channel Indexing**: Remember channels are 1-indexed for rendering, 0-indexed for pixel access
8. **Save Settings**: Save rendering settings if they should be permanent
9. **Compression**: Use compression parameter in renderImage() for faster transfers
10. **Error Handling**: Check for None returns and handle exceptions

---

## Reference: Metadata

# Metadata & Annotations

This reference covers creating and managing annotations in OMERO, including tags, key-value pairs, file attachments, and comments.

## Annotation Types

OMERO supports several annotation types:

- **TagAnnotation**: Text labels for categorization
- **MapAnnotation**: Key-value pairs for structured metadata
- **FileAnnotation**: File attachments (PDFs, CSVs, analysis results, etc.)
- **CommentAnnotation**: Free-text comments
- **LongAnnotation**: Integer values
- **DoubleAnnotation**: Floating-point values
- **BooleanAnnotation**: Boolean values
- **TimestampAnnotation**: Date/time stamps
- **TermAnnotation**: Ontology terms

## Tag Annotations

### Create and Link Tag

```python
import omero.gateway

# Create new tag
tag_ann = omero.gateway.TagAnnotationWrapper(conn)
tag_ann.setValue("Experiment 2024")
tag_ann.setDescription("Optional description of this tag")
tag_ann.save()

# Link tag to an object
project = conn.getObject("Project", project_id)
project.linkAnnotation(tag_ann)
```

### Create Tag with Namespace

```python
# Create tag with custom namespace
tag_ann = omero.gateway.TagAnnotationWrapper(conn)
tag_ann.setValue("Quality Control")
tag_ann.setNs("mylab.qc.tags")
tag_ann.save()

# Link to image
image = conn.getObject("Image", image_id)
image.linkAnnotation(tag_ann)
```

### Reuse Existing Tag

```python
# Find existing tag
tag_id = 123
tag_ann = conn.getObject("TagAnnotation", tag_id)

# Link to multiple images
for image in conn.getObjects("Image", [img1, img2, img3]):
    image.linkAnnotation(tag_ann)
```

### Create Tag Set (Tag with Children)

```python
# Create tag set (parent tag)
tag_set = omero.gateway.TagAnnotationWrapper(conn)
tag_set.setValue("Cell Types")
tag_set.save()

# Create child tags
tags = ["HeLa", "U2OS", "HEK293"]
for tag_value in tags:
    tag = omero.gateway.TagAnnotationWrapper(conn)
    tag.setValue(tag_value)
    tag.save()

    # Link child to parent
    tag_set.linkAnnotation(tag)
```

## Map Annotations (Key-Value Pairs)

### Create Map Annotation

```python
import omero.gateway
import omero.constants.metadata

# Prepare key-value data
key_value_data = [
    ["Drug Name", "Monastrol"],
    ["Concentration", "5 mg/ml"],
    ["Treatment Time", "24 hours"],
    ["Temperature", "37C"]
]

# Create map annotation
map_ann = omero.gateway.MapAnnotationWrapper(conn)

# Use standard client namespace
namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
map_ann.setNs(namespace)

# Set data
map_ann.setValue(key_value_data)
map_ann.save()

# Link to dataset
dataset = conn.getObject("Dataset", dataset_id)
dataset.linkAnnotation(map_ann)
```

### Custom Namespace for Map Annotations

```python
# Use custom namespace for organization-specific metadata
key_value_data = [
    ["Microscope", "Zeiss LSM 880"],
    ["Objective", "63x Oil"],
    ["Laser Power", "10%"]
]

map_ann = omero.gateway.MapAnnotationWrapper(conn)
map_ann.setNs("mylab.microscopy.settings")
map_ann.setValue(key_value_data)
map_ann.save()

image = conn.getObject("Image", image_id)
image.linkAnnotation(map_ann)
```

### Read Map Annotation

```python
# Get map annotation
image = conn.getObject("Image", image_id)

for ann in image.listAnnotations():
    if isinstance(ann, omero.gateway.MapAnnotationWrapper):
        print(f"Map Annotation (ID: {ann.getId()}):")
        print(f"Namespace: {ann.getNs()}")

        # Get key-value pairs
        for key, value in ann.getValue():
            print(f"  {key}: {value}")
```

## File Annotations

### Upload and Attach File

```python
import os

# Prepare file
file_path = "analysis_results.csv"

# Create file annotation
namespace = "mylab.analysis.results"
file_ann = conn.createFileAnnfromLocalFile(
    file_path,
    mimetype="text/csv",
    ns=namespace,
    desc="Cell segmentation results"
)

# Link to dataset
dataset = conn.getObject("Dataset", dataset_id)
dataset.linkAnnotation(file_ann)
```

### Supported MIME Types

Common MIME types:
- Text: `"text/plain"`, `"text/csv"`, `"text/tab-separated-values"`
- Documents: `"application/pdf"`, `"application/vnd.ms-excel"`
- Images: `"image/png"`, `"image/jpeg"`
- Data: `"application/json"`, `"application/xml"`
- Archives: `"application/zip"`, `"application/gzip"`

### Upload Multiple Files

```python
files = ["figure1.pdf", "figure2.pdf", "table1.csv"]
namespace = "publication.supplementary"

dataset = conn.getObject("Dataset", dataset_id)

for file_path in files:
    file_ann = conn.createFileAnnfromLocalFile(
        file_path,
        mimetype="application/octet-stream",
        ns=namespace,
        desc=f"Supplementary file: {os.path.basename(file_path)}"
    )
    dataset.linkAnnotation(file_ann)
```

### Download File Annotation

```python
import os

# Get object with file annotation
image = conn.getObject("Image", image_id)

# Download directory
download_path = "./downloads"
os.makedirs(download_path, exist_ok=True)

# Filter by namespace
namespace = "mylab.analysis.results"

for ann in image.listAnnotations(ns=namespace):
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        file_name = ann.getFile().getName()
        file_path = os.path.join(download_path, file_name)

        print(f"Downloading: {file_name}")

        # Download file in chunks
        with open(file_path, 'wb') as f:
            for chunk in ann.getFileInChunks():
                f.write(chunk)

        print(f"Saved to: {file_path}")
```

### Get File Annotation Metadata

```python
for ann in dataset.listAnnotations():
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        orig_file = ann.getFile()

        print(f"File Annotation ID: {ann.getId()}")
        print(f"  File Name: {orig_file.getName()}")
        print(f"  File Size: {orig_file.getSize()} bytes")
        print(f"  MIME Type: {orig_file.getMimetype()}")
        print(f"  Namespace: {ann.getNs()}")
        print(f"  Description: {ann.getDescription()}")
```

## Comment Annotations

### Add Comment

```python
# Create comment
comment = omero.gateway.CommentAnnotationWrapper(conn)
comment.setValue("This image shows excellent staining quality")
comment.save()

# Link to image
image = conn.getObject("Image", image_id)
image.linkAnnotation(comment)
```

### Add Comment with Namespace

```python
comment = omero.gateway.CommentAnnotationWrapper(conn)
comment.setValue("Approved for publication")
comment.setNs("mylab.publication.status")
comment.save()

dataset = conn.getObject("Dataset", dataset_id)
dataset.linkAnnotation(comment)
```

## Numeric Annotations

### Long Annotation (Integer)

```python
# Create long annotation
long_ann = omero.gateway.LongAnnotationWrapper(conn)
long_ann.setValue(42)
long_ann.setNs("mylab.cell.count")
long_ann.save()

image = conn.getObject("Image", image_id)
image.linkAnnotation(long_ann)
```

### Double Annotation (Float)

```python
# Create double annotation
double_ann = omero.gateway.DoubleAnnotationWrapper(conn)
double_ann.setValue(3.14159)
double_ann.setNs("mylab.fluorescence.intensity")
double_ann.save()

image = conn.getObject("Image", image_id)
image.linkAnnotation(double_ann)
```

## Listing Annotations

### List All Annotations on Object

```python
import omero.model

# Get object
project = conn.getObject("Project", project_id)

# List all annotations
for ann in project.listAnnotations():
    print(f"Annotation ID: {ann.getId()}")
    print(f"  Type: {ann.OMERO_TYPE}")
    print(f"  Added by: {ann.link.getDetails().getOwner().getOmeName()}")

    # Type-specific handling
    if ann.OMERO_TYPE == omero.model.TagAnnotationI:
        print(f"  Tag value: {ann.getTextValue()}")

    elif isinstance(ann, omero.gateway.MapAnnotationWrapper):
        print(f"  Map data: {ann.getValue()}")

    elif isinstance(ann, omero.gateway.FileAnnotationWrapper):
        print(f"  File: {ann.getFile().getName()}")

    elif isinstance(ann, omero.gateway.CommentAnnotationWrapper):
        print(f"  Comment: {ann.getValue()}")

    print()
```

### Filter Annotations by Namespace

```python
# Get annotations with specific namespace
namespace = "mylab.qc.tags"

for ann in image.listAnnotations(ns=namespace):
    print(f"Found annotation: {ann.getId()}")

    if isinstance(ann, omero.gateway.MapAnnotationWrapper):
        for key, value in ann.getValue():
            print(f"  {key}: {value}")
```

### Get First Annotation with Namespace

```python
# Get single annotation by namespace
namespace = "mylab.analysis.results"
ann = dataset.getAnnotation(namespace)

if ann:
    print(f"Found annotation with namespace: {ann.getNs()}")
else:
    print("No annotation found with that namespace")
```

### Query Annotations Across Multiple Objects

```python
# Get all tag annotations linked to image IDs
image_ids = [1, 2, 3, 4, 5]

for link in conn.getAnnotationLinks('Image', parent_ids=image_ids):
    ann = link.getChild()

    if isinstance(ann._obj, omero.model.TagAnnotationI):
        print(f"Image {link.getParent().getId()}: Tag '{ann.getTextValue()}'")
```

## Counting Annotations

```python
# Count annotations on project
project_id = 123
count = conn.countAnnotations('Project', [project_id])
print(f"Project has {count[project_id]} annotations")

# Count annotations on multiple images
image_ids = [1, 2, 3]
counts = conn.countAnnotations('Image', image_ids)

for image_id, count in counts.items():
    print(f"Image {image_id}: {count} annotations")
```

## Annotation Links

### Create Annotation Link Manually

```python
# Get annotation and image
tag = conn.getObject("TagAnnotation", tag_id)
image = conn.getObject("Image", image_id)

# Create link
link = omero.model.ImageAnnotationLinkI()
link.setParent(omero.model.ImageI(image.getId(), False))
link.setChild(omero.model.TagAnnotationI(tag.getId(), False))

# Save link
conn.getUpdateService().saveAndReturnObject(link)
```

### Update Annotation Links

```python
# Get existing links
annotation_ids = [1, 2, 3]
new_tag_id = 5

for link in conn.getAnnotationLinks('Image', ann_ids=annotation_ids):
    print(f"Image ID: {link.getParent().id}")

    # Change linked annotation
    link._obj.child = omero.model.TagAnnotationI(new_tag_id, False)
    link.save()
```

## Removing Annotations

### Delete Annotations

```python
# Get image
image = conn.getObject("Image", image_id)

# Collect annotation IDs to delete
to_delete = []
namespace = "mylab.temp.annotations"

for ann in image.listAnnotations(ns=namespace):
    to_delete.append(ann.getId())

# Delete annotations
if to_delete:
    conn.deleteObjects('Annotation', to_delete, wait=True)
    print(f"Deleted {len(to_delete)} annotations")
```

### Unlink Annotations (Keep Annotation, Remove Link)

```python
# Get image
image = conn.getObject("Image", image_id)

# Collect link IDs to delete
to_delete = []

for ann in image.listAnnotations():
    if isinstance(ann, omero.gateway.TagAnnotationWrapper):
        to_delete.append(ann.link.getId())

# Delete links (annotations remain in database)
if to_delete:
    conn.deleteObjects("ImageAnnotationLink", to_delete, wait=True)
    print(f"Unlinked {len(to_delete)} annotations")
```

### Delete Specific Annotation Types

```python
import omero.gateway

# Delete only map annotations
image = conn.getObject("Image", image_id)
to_delete = []

for ann in image.listAnnotations():
    if isinstance(ann, omero.gateway.MapAnnotationWrapper):
        to_delete.append(ann.getId())

conn.deleteObjects('Annotation', to_delete, wait=True)
```

## Annotation Ownership

### Set Annotation Owner (Admin Only)

```python
import omero.model

# Create tag with specific owner
tag_ann = omero.gateway.TagAnnotationWrapper(conn)
tag_ann.setValue("Admin Tag")

# Set owner (requires admin privileges)
user_id = 5
tag_ann._obj.details.owner = omero.model.ExperimenterI(user_id, False)
tag_ann.save()
```

### Create Annotation as Another User (Admin Only)

```python
# Admin connection
admin_conn = BlitzGateway(admin_user, admin_pass, host=host, port=4064)
admin_conn.connect()

# Get target user
user_id = 10
user = admin_conn.getObject("Experimenter", user_id).getName()

# Create connection as user
user_conn = admin_conn.suConn(user)

# Create annotation as that user
map_ann = omero.gateway.MapAnnotationWrapper(user_conn)
map_ann.setNs("mylab.metadata")
map_ann.setValue([["key", "value"]])
map_ann.save()

# Link to project
project = admin_conn.getObject("Project", project_id)
project.linkAnnotation(map_ann)

# Close connections
user_conn.close()
admin_conn.close()
```

## Bulk Annotation Operations

### Tag Multiple Images

```python
# Create or get tag
tag = omero.gateway.TagAnnotationWrapper(conn)
tag.setValue("Validated")
tag.save()

# Get images to tag
dataset = conn.getObject("Dataset", dataset_id)

# Tag all images in dataset
for image in dataset.listChildren():
    image.linkAnnotation(tag)
    print(f"Tagged image: {image.getName()}")
```

### Batch Add Map Annotations

```python
# Prepare metadata for multiple images
image_metadata = {
    101: [["Quality", "Good"], ["Reviewed", "Yes"]],
    102: [["Quality", "Excellent"], ["Reviewed", "Yes"]],
    103: [["Quality", "Poor"], ["Reviewed", "No"]]
}

# Add annotations
for image_id, kv_data in image_metadata.items():
    image = conn.getObject("Image", image_id)

    if image:
        map_ann = omero.gateway.MapAnnotationWrapper(conn)
        map_ann.setNs("mylab.qc")
        map_ann.setValue(kv_data)
        map_ann.save()

        image.linkAnnotation(map_ann)
        print(f"Annotated image {image_id}")
```

## Namespaces

### Standard OMERO Namespaces

```python
import omero.constants.metadata as omero_ns

# Client map annotation namespace
omero_ns.NSCLIENTMAPANNOTATION
# "openmicroscopy.org/omero/client/mapAnnotation"

# Bulk annotations namespace
omero_ns.NSBULKANNOTATIONS
# "openmicroscopy.org/omero/bulk_annotations"
```

### Custom Namespaces

Best practices for custom namespaces:
- Use reverse domain notation: `"org.mylab.category.subcategory"`
- Be specific: `"com.company.project.analysis.v1"`
- Include version if schema may change: `"mylab.metadata.v2"`

```python
# Define namespaces
NS_QC = "org.mylab.quality_control"
NS_ANALYSIS = "org.mylab.image_analysis.v1"
NS_PUBLICATION = "org.mylab.publication.2024"

# Use in annotations
map_ann.setNs(NS_ANALYSIS)
```

## Load All Annotations by Type

### Load All File Annotations

```python
# Define namespaces to include/exclude
ns_to_include = ["mylab.analysis.results"]
ns_to_exclude = []

# Get metadata service
metadataService = conn.getMetadataService()

# Load all file annotations with namespace
annotations = metadataService.loadSpecifiedAnnotations(
    'omero.model.FileAnnotation',
    ns_to_include,
    ns_to_exclude,
    None
)

for ann in annotations:
    print(f"File Annotation ID: {ann.getId().getValue()}")
    print(f"  File: {ann.getFile().getName().getValue()}")
    print(f"  Size: {ann.getFile().getSize().getValue()} bytes")
```

## Complete Example

```python
from omero.gateway import BlitzGateway
import omero.gateway
import omero.constants.metadata

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get dataset
    dataset = conn.getObject("Dataset", dataset_id)

    # Add tag
    tag = omero.gateway.TagAnnotationWrapper(conn)
    tag.setValue("Analysis Complete")
    tag.save()
    dataset.linkAnnotation(tag)

    # Add map annotation with metadata
    metadata = [
        ["Analysis Date", "2024-10-20"],
        ["Software", "CellProfiler 4.2"],
        ["Pipeline", "cell_segmentation_v3"]
    ]
    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setNs(omero.constants.metadata.NSCLIENTMAPANNOTATION)
    map_ann.setValue(metadata)
    map_ann.save()
    dataset.linkAnnotation(map_ann)

    # Add file annotation
    file_ann = conn.createFileAnnfromLocalFile(
        "analysis_summary.pdf",
        mimetype="application/pdf",
        ns="mylab.reports",
        desc="Analysis summary report"
    )
    dataset.linkAnnotation(file_ann)

    # Add comment
    comment = omero.gateway.CommentAnnotationWrapper(conn)
    comment.setValue("Dataset ready for review")
    comment.save()
    dataset.linkAnnotation(comment)

    print(f"Added 4 annotations to dataset {dataset.getName()}")
```

## Best Practices

1. **Use Namespaces**: Always use namespaces to organize annotations
2. **Descriptive Tags**: Use clear, consistent tag names
3. **Structured Metadata**: Prefer map annotations over comments for structured data
4. **File Organization**: Use descriptive filenames and MIME types
5. **Link Reuse**: Reuse existing tags instead of creating duplicates
6. **Batch Operations**: Process multiple objects in loops for efficiency
7. **Error Handling**: Check for successful saves before linking
8. **Cleanup**: Remove temporary annotations when no longer needed
9. **Documentation**: Document custom namespace meanings
10. **Permissions**: Consider annotation ownership for collaborative workflows

---

## Reference: Rois

# Regions of Interest (ROIs)

This reference covers creating, retrieving, and analyzing ROIs in OMERO.

## ROI Overview

ROIs (Regions of Interest) in OMERO are containers for geometric shapes that mark specific regions on images. Each ROI can contain multiple shapes, and shapes can be specific to Z-sections and timepoints.

### Supported Shape Types

- **Rectangle**: Rectangular regions
- **Ellipse**: Circular and elliptical regions
- **Line**: Line segments
- **Point**: Single points
- **Polygon**: Multi-point polygons
- **Mask**: Pixel-based masks
- **Polyline**: Multi-segment lines

## Creating ROIs

### Helper Functions

```python
from omero.rtypes import rdouble, rint, rstring
import omero.model

def create_roi(conn, image, shapes):
    """
    Create an ROI and link it to shapes.

    Args:
        conn: BlitzGateway connection
        image: Image object
        shapes: List of shape objects

    Returns:
        Saved ROI object
    """
    roi = omero.model.RoiI()
    roi.setImage(image._obj)

    for shape in shapes:
        roi.addShape(shape)

    updateService = conn.getUpdateService()
    return updateService.saveAndReturnObject(roi)

def rgba_to_int(red, green, blue, alpha=255):
    """
    Convert RGBA values (0-255) to integer encoding for OMERO.

    Args:
        red, green, blue, alpha: Color values (0-255)

    Returns:
        Integer color value
    """
    return int.from_bytes([red, green, blue, alpha],
                          byteorder='big', signed=True)
```

### Rectangle ROI

```python
from omero.rtypes import rdouble, rint, rstring
import omero.model

# Get image
image = conn.getObject("Image", image_id)

# Define position and size
x, y = 50, 100
width, height = 200, 150
z, t = 0, 0  # Z-section and timepoint

# Create rectangle
rect = omero.model.RectangleI()
rect.x = rdouble(x)
rect.y = rdouble(y)
rect.width = rdouble(width)
rect.height = rdouble(height)
rect.theZ = rint(z)
rect.theT = rint(t)

# Set label and colors
rect.textValue = rstring("Cell Region")
rect.fillColor = rint(rgba_to_int(255, 0, 0, 50))    # Red, semi-transparent
rect.strokeColor = rint(rgba_to_int(255, 255, 0, 255))  # Yellow border

# Create ROI
roi = create_roi(conn, image, [rect])
print(f"Created ROI ID: {roi.getId().getValue()}")
```

### Ellipse ROI

```python
# Center position and radii
center_x, center_y = 250, 250
radius_x, radius_y = 100, 75
z, t = 0, 0

# Create ellipse
ellipse = omero.model.EllipseI()
ellipse.x = rdouble(center_x)
ellipse.y = rdouble(center_y)
ellipse.radiusX = rdouble(radius_x)
ellipse.radiusY = rdouble(radius_y)
ellipse.theZ = rint(z)
ellipse.theT = rint(t)
ellipse.textValue = rstring("Nucleus")
ellipse.fillColor = rint(rgba_to_int(0, 255, 0, 50))

# Create ROI
roi = create_roi(conn, image, [ellipse])
```

### Line ROI

```python
# Line endpoints
x1, y1 = 100, 100
x2, y2 = 300, 200
z, t = 0, 0

# Create line
line = omero.model.LineI()
line.x1 = rdouble(x1)
line.y1 = rdouble(y1)
line.x2 = rdouble(x2)
line.y2 = rdouble(y2)
line.theZ = rint(z)
line.theT = rint(t)
line.textValue = rstring("Measurement Line")
line.strokeColor = rint(rgba_to_int(0, 0, 255, 255))

# Create ROI
roi = create_roi(conn, image, [line])
```

### Point ROI

```python
# Point position
x, y = 150, 150
z, t = 0, 0

# Create point
point = omero.model.PointI()
point.x = rdouble(x)
point.y = rdouble(y)
point.theZ = rint(z)
point.theT = rint(t)
point.textValue = rstring("Feature Point")

# Create ROI
roi = create_roi(conn, image, [point])
```

### Polygon ROI

```python
from omero.model.enums import UnitsLength

# Define vertices as string "x1,y1 x2,y2 x3,y3 ..."
vertices = "10,20 50,150 200,200 250,75"
z, t = 0, 0

# Create polygon
polygon = omero.model.PolygonI()
polygon.points = rstring(vertices)
polygon.theZ = rint(z)
polygon.theT = rint(t)
polygon.textValue = rstring("Cell Outline")

# Set colors and stroke width
polygon.fillColor = rint(rgba_to_int(255, 0, 255, 50))
polygon.strokeColor = rint(rgba_to_int(255, 255, 0, 255))
polygon.strokeWidth = omero.model.LengthI(2, UnitsLength.PIXEL)

# Create ROI
roi = create_roi(conn, image, [polygon])
```

### Mask ROI

```python
import numpy as np
import struct
import math

def create_mask_bytes(mask_array, bytes_per_pixel=1):
    """
    Convert binary mask array to bit-packed bytes for OMERO.

    Args:
        mask_array: Binary numpy array (0s and 1s)
        bytes_per_pixel: 1 or 2

    Returns:
        Byte array for OMERO mask
    """
    if bytes_per_pixel == 2:
        divider = 16.0
        format_string = "H"
        byte_factor = 0.5
    elif bytes_per_pixel == 1:
        divider = 8.0
        format_string = "B"
        byte_factor = 1
    else:
        raise ValueError("bytes_per_pixel must be 1 or 2")

    mask_bytes = mask_array.astype(np.uint8).tobytes()
    steps = math.ceil(len(mask_bytes) / divider)
    packed_mask = []

    for i in range(int(steps)):
        binary = mask_bytes[i * int(divider):
                           i * int(divider) + int(divider)]
        format_str = str(int(byte_factor * len(binary))) + format_string
        binary = struct.unpack(format_str, binary)
        s = "".join(str(bit) for bit in binary)
        packed_mask.append(int(s, 2))

    return bytearray(packed_mask)

# Create binary mask (1s and 0s)
mask_w, mask_h = 100, 100
mask_array = np.fromfunction(
    lambda x, y: ((x - 50)**2 + (y - 50)**2) < 40**2,  # Circle
    (mask_w, mask_h)
)

# Pack mask
mask_packed = create_mask_bytes(mask_array, bytes_per_pixel=1)

# Mask position
mask_x, mask_y = 50, 50
z, t, c = 0, 0, 0

# Create mask
mask = omero.model.MaskI()
mask.setX(rdouble(mask_x))
mask.setY(rdouble(mask_y))
mask.setWidth(rdouble(mask_w))
mask.setHeight(rdouble(mask_h))
mask.setTheZ(rint(z))
mask.setTheT(rint(t))
mask.setTheC(rint(c))
mask.setBytes(mask_packed)
mask.textValue = rstring("Segmentation Mask")

# Set color
from omero.gateway import ColorHolder
mask_color = ColorHolder()
mask_color.setRed(255)
mask_color.setGreen(0)
mask_color.setBlue(0)
mask_color.setAlpha(100)
mask.setFillColor(rint(mask_color.getInt()))

# Create ROI
roi = create_roi(conn, image, [mask])
```

## Multiple Shapes in One ROI

```python
# Create multiple shapes for the same ROI
shapes = []

# Rectangle
rect = omero.model.RectangleI()
rect.x = rdouble(100)
rect.y = rdouble(100)
rect.width = rdouble(50)
rect.height = rdouble(50)
rect.theZ = rint(0)
rect.theT = rint(0)
shapes.append(rect)

# Ellipse
ellipse = omero.model.EllipseI()
ellipse.x = rdouble(125)
ellipse.y = rdouble(125)
ellipse.radiusX = rdouble(20)
ellipse.radiusY = rdouble(20)
ellipse.theZ = rint(0)
ellipse.theT = rint(0)
shapes.append(ellipse)

# Create single ROI with both shapes
roi = create_roi(conn, image, shapes)
```

## Retrieving ROIs

### Get All ROIs for Image

```python
# Get ROI service
roi_service = conn.getRoiService()

# Find all ROIs for image
result = roi_service.findByImage(image_id, None)

print(f"Found {len(result.rois)} ROIs")

for roi in result.rois:
    print(f"ROI ID: {roi.getId().getValue()}")
    print(f"  Number of shapes: {len(roi.copyShapes())}")
```

### Parse ROI Shapes

```python
import omero.model

result = roi_service.findByImage(image_id, None)

for roi in result.rois:
    roi_id = roi.getId().getValue()
    print(f"ROI ID: {roi_id}")

    for shape in roi.copyShapes():
        shape_id = shape.getId().getValue()
        z = shape.getTheZ().getValue() if shape.getTheZ() else None
        t = shape.getTheT().getValue() if shape.getTheT() else None

        # Get label
        label = ""
        if shape.getTextValue():
            label = shape.getTextValue().getValue()

        print(f"  Shape ID: {shape_id}, Z: {z}, T: {t}, Label: {label}")

        # Type-specific parsing
        if isinstance(shape, omero.model.RectangleI):
            x = shape.getX().getValue()
            y = shape.getY().getValue()
            width = shape.getWidth().getValue()
            height = shape.getHeight().getValue()
            print(f"    Rectangle: ({x}, {y}) {width}x{height}")

        elif isinstance(shape, omero.model.EllipseI):
            x = shape.getX().getValue()
            y = shape.getY().getValue()
            rx = shape.getRadiusX().getValue()
            ry = shape.getRadiusY().getValue()
            print(f"    Ellipse: center ({x}, {y}), radii ({rx}, {ry})")

        elif isinstance(shape, omero.model.PointI):
            x = shape.getX().getValue()
            y = shape.getY().getValue()
            print(f"    Point: ({x}, {y})")

        elif isinstance(shape, omero.model.LineI):
            x1 = shape.getX1().getValue()
            y1 = shape.getY1().getValue()
            x2 = shape.getX2().getValue()
            y2 = shape.getY2().getValue()
            print(f"    Line: ({x1}, {y1}) to ({x2}, {y2})")

        elif isinstance(shape, omero.model.PolygonI):
            points = shape.getPoints().getValue()
            print(f"    Polygon: {points}")

        elif isinstance(shape, omero.model.MaskI):
            x = shape.getX().getValue()
            y = shape.getY().getValue()
            width = shape.getWidth().getValue()
            height = shape.getHeight().getValue()
            print(f"    Mask: ({x}, {y}) {width}x{height}")
```

## Analyzing ROI Intensities

### Get Statistics for ROI Shapes

```python
# Get all shapes from ROIs
roi_service = conn.getRoiService()
result = roi_service.findByImage(image_id, None)

shape_ids = []
for roi in result.rois:
    for shape in roi.copyShapes():
        shape_ids.append(shape.id.val)

# Define position
z, t = 0, 0
channel_index = 0

# Get statistics
stats = roi_service.getShapeStatsRestricted(
    shape_ids, z, t, [channel_index]
)

# Display statistics
for i, stat in enumerate(stats):
    shape_id = shape_ids[i]
    print(f"Shape {shape_id} statistics:")
    print(f"  Points Count: {stat.pointsCount[channel_index]}")
    print(f"  Min: {stat.min[channel_index]}")
    print(f"  Mean: {stat.mean[channel_index]}")
    print(f"  Max: {stat.max[channel_index]}")
    print(f"  Sum: {stat.sum[channel_index]}")
    print(f"  Std Dev: {stat.stdDev[channel_index]}")
```

### Extract Pixel Values Within ROI

```python
import numpy as np

# Get image and ROI
image = conn.getObject("Image", image_id)
result = roi_service.findByImage(image_id, None)

# Get first rectangle shape
roi = result.rois[0]
rect = roi.copyShapes()[0]

# Get rectangle bounds
x = int(rect.getX().getValue())
y = int(rect.getY().getValue())
width = int(rect.getWidth().getValue())
height = int(rect.getHeight().getValue())
z = rect.getTheZ().getValue()
t = rect.getTheT().getValue()

# Get pixel data
pixels = image.getPrimaryPixels()

# Extract region for each channel
for c in range(image.getSizeC()):
    # Get plane
    plane = pixels.getPlane(z, c, t)

    # Extract ROI region
    roi_region = plane[y:y+height, x:x+width]

    print(f"Channel {c}:")
    print(f"  Mean intensity: {np.mean(roi_region)}")
    print(f"  Max intensity: {np.max(roi_region)}")
```

## Modifying ROIs

### Update Shape Properties

```python
# Get ROI and shape
result = roi_service.findByImage(image_id, None)
roi = result.rois[0]
shape = roi.copyShapes()[0]

# Modify shape (example: change rectangle size)
if isinstance(shape, omero.model.RectangleI):
    shape.setWidth(rdouble(150))
    shape.setHeight(rdouble(100))
    shape.setTextValue(rstring("Updated Rectangle"))

# Save changes
updateService = conn.getUpdateService()
updated_roi = updateService.saveAndReturnObject(roi._obj)
```

### Remove Shape from ROI

```python
result = roi_service.findByImage(image_id, None)

for roi in result.rois:
    for shape in roi.copyShapes():
        # Check condition (e.g., remove by label)
        if (shape.getTextValue() and
            shape.getTextValue().getValue() == "test-Ellipse"):

            print(f"Removing shape {shape.getId().getValue()}")
            roi.removeShape(shape)

            # Save modified ROI
            updateService = conn.getUpdateService()
            roi = updateService.saveAndReturnObject(roi)
```

## Deleting ROIs

### Delete Single ROI

```python
# Delete ROI by ID
roi_id = 123
conn.deleteObjects("Roi", [roi_id], wait=True)
print(f"Deleted ROI {roi_id}")
```

### Delete All ROIs for Image

```python
# Get all ROI IDs for image
result = roi_service.findByImage(image_id, None)
roi_ids = [roi.getId().getValue() for roi in result.rois]

# Delete all
if roi_ids:
    conn.deleteObjects("Roi", roi_ids, wait=True)
    print(f"Deleted {len(roi_ids)} ROIs")
```

## Batch ROI Creation

### Create ROIs for Multiple Images

```python
# Get images
dataset = conn.getObject("Dataset", dataset_id)

for image in dataset.listChildren():
    # Create rectangle at center of each image
    x = image.getSizeX() // 2 - 50
    y = image.getSizeY() // 2 - 50

    rect = omero.model.RectangleI()
    rect.x = rdouble(x)
    rect.y = rdouble(y)
    rect.width = rdouble(100)
    rect.height = rdouble(100)
    rect.theZ = rint(0)
    rect.theT = rint(0)
    rect.textValue = rstring("Auto ROI")

    roi = create_roi(conn, image, [rect])
    print(f"Created ROI for image {image.getName()}")
```

### Create ROIs Across Z-Stack

```python
image = conn.getObject("Image", image_id)
size_z = image.getSizeZ()

# Create rectangle on each Z-section
shapes = []
for z in range(size_z):
    rect = omero.model.RectangleI()
    rect.x = rdouble(100)
    rect.y = rdouble(100)
    rect.width = rdouble(50)
    rect.height = rdouble(50)
    rect.theZ = rint(z)
    rect.theT = rint(0)
    shapes.append(rect)

# Single ROI with shapes across Z
roi = create_roi(conn, image, shapes)
```

## Complete Example

```python
from omero.gateway import BlitzGateway
from omero.rtypes import rdouble, rint, rstring
import omero.model

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

def rgba_to_int(r, g, b, a=255):
    return int.from_bytes([r, g, b, a], byteorder='big', signed=True)

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get image
    image = conn.getObject("Image", image_id)
    print(f"Processing: {image.getName()}")

    # Create multiple ROIs
    updateService = conn.getUpdateService()

    # ROI 1: Rectangle
    roi1 = omero.model.RoiI()
    roi1.setImage(image._obj)

    rect = omero.model.RectangleI()
    rect.x = rdouble(50)
    rect.y = rdouble(50)
    rect.width = rdouble(100)
    rect.height = rdouble(100)
    rect.theZ = rint(0)
    rect.theT = rint(0)
    rect.textValue = rstring("Cell 1")
    rect.strokeColor = rint(rgba_to_int(255, 0, 0, 255))

    roi1.addShape(rect)
    roi1 = updateService.saveAndReturnObject(roi1)
    print(f"Created ROI 1: {roi1.getId().getValue()}")

    # ROI 2: Ellipse
    roi2 = omero.model.RoiI()
    roi2.setImage(image._obj)

    ellipse = omero.model.EllipseI()
    ellipse.x = rdouble(200)
    ellipse.y = rdouble(150)
    ellipse.radiusX = rdouble(40)
    ellipse.radiusY = rdouble(30)
    ellipse.theZ = rint(0)
    ellipse.theT = rint(0)
    ellipse.textValue = rstring("Cell 2")
    ellipse.strokeColor = rint(rgba_to_int(0, 255, 0, 255))

    roi2.addShape(ellipse)
    roi2 = updateService.saveAndReturnObject(roi2)
    print(f"Created ROI 2: {roi2.getId().getValue()}")

    # Retrieve and analyze
    roi_service = conn.getRoiService()
    result = roi_service.findByImage(image_id, None)

    shape_ids = []
    for roi in result.rois:
        for shape in roi.copyShapes():
            shape_ids.append(shape.id.val)

    # Get statistics
    stats = roi_service.getShapeStatsRestricted(shape_ids, 0, 0, [0])

    for i, stat in enumerate(stats):
        print(f"Shape {shape_ids[i]}:")
        print(f"  Mean intensity: {stat.mean[0]:.2f}")
```

## Best Practices

1. **Organize Shapes**: Group related shapes in single ROIs
2. **Label Shapes**: Use textValue for identification
3. **Set Z and T**: Always specify Z-section and timepoint
4. **Color Coding**: Use consistent colors for shape types
5. **Validate Coordinates**: Ensure shapes are within image bounds
6. **Batch Creation**: Create multiple ROIs in single transaction when possible
7. **Delete Unused**: Remove temporary or test ROIs
8. **Export Data**: Store ROI statistics in tables for later analysis
9. **Version Control**: Document ROI creation methods in annotations
10. **Performance**: Use shape statistics service instead of manual pixel extraction

---

## Reference: Scripts

# Scripts & Batch Operations

This reference covers creating OMERO.scripts for server-side processing and batch operations.

## OMERO.scripts Overview

OMERO.scripts are Python scripts that run on the OMERO server and can be called from OMERO clients (web, insight, CLI). They function as plugins that extend OMERO functionality.

### Key Features

- **Server-Side Execution**: Scripts run on the server, avoiding data transfer
- **Client Integration**: Callable from any OMERO client with auto-generated UI
- **Parameter Handling**: Define input parameters with validation
- **Result Reporting**: Return images, files, or messages to clients
- **Batch Processing**: Process multiple images or datasets efficiently

## Basic Script Structure

### Minimal Script Template

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import omero
from omero.gateway import BlitzGateway
import omero.scripts as scripts
from omero.rtypes import rlong, rstring, robject

def run_script():
    """
    Main script function.
    """
    # Script definition
    client = scripts.client(
        'Script_Name.py',
        """
        Description of what this script does.
        """,

        # Input parameters
        scripts.String("Data_Type", optional=False, grouping="1",
                      description="Choose source of images",
                      values=[rstring('Dataset'), rstring('Image')],
                      default=rstring('Dataset')),

        scripts.Long("IDs", optional=False, grouping="2",
                    description="Dataset or Image ID(s)").ofType(rlong(0)),

        # Outputs
        namespaces=[omero.constants.namespaces.NSDYNAMIC],
        version="1.0"
    )

    try:
        # Get connection
        conn = BlitzGateway(client_obj=client)

        # Get script parameters
        script_params = client.getInputs(unwrap=True)
        data_type = script_params["Data_Type"]
        ids = script_params["IDs"]

        # Process data
        message = process_data(conn, data_type, ids)

        # Return results
        client.setOutput("Message", rstring(message))

    finally:
        client.closeSession()

def process_data(conn, data_type, ids):
    """
    Process images based on parameters.
    """
    # Implementation here
    return "Processing complete"

if __name__ == "__main__":
    run_script()
```

## Script Parameters

### Parameter Types

```python
# String parameter
scripts.String("Name", optional=False,
              description="Enter a name")

# String with choices
scripts.String("Mode", optional=False,
              values=[rstring('Fast'), rstring('Accurate')],
              default=rstring('Fast'))

# Integer parameter
scripts.Long("ImageID", optional=False,
            description="Image to process").ofType(rlong(0))

# List of integers
scripts.List("ImageIDs", optional=False,
            description="Multiple images").ofType(rlong(0))

# Float parameter
scripts.Float("Threshold", optional=True,
             description="Threshold value",
             min=0.0, max=1.0, default=0.5)

# Boolean parameter
scripts.Bool("SaveResults", optional=True,
            description="Save results to OMERO",
            default=True)
```

### Parameter Grouping

```python
# Group related parameters
scripts.String("Data_Type", grouping="1",
              description="Source type",
              values=[rstring('Dataset'), rstring('Image')])

scripts.Long("Dataset_ID", grouping="1.1",
            description="Dataset ID").ofType(rlong(0))

scripts.List("Image_IDs", grouping="1.2",
            description="Image IDs").ofType(rlong(0))
```

## Accessing Input Data

### Get Script Parameters

```python
# Inside run_script()
client = scripts.client(...)

# Get parameters as Python objects
script_params = client.getInputs(unwrap=True)

# Access individual parameters
data_type = script_params.get("Data_Type", "Image")
image_ids = script_params.get("Image_IDs", [])
threshold = script_params.get("Threshold", 0.5)
save_results = script_params.get("SaveResults", True)
```

### Get Images from Parameters

```python
def get_images_from_params(conn, script_params):
    """
    Get image objects based on script parameters.
    """
    images = []

    data_type = script_params["Data_Type"]

    if data_type == "Dataset":
        dataset_id = script_params["Dataset_ID"]
        dataset = conn.getObject("Dataset", dataset_id)
        if dataset:
            images = list(dataset.listChildren())

    elif data_type == "Image":
        image_ids = script_params["Image_IDs"]
        for image_id in image_ids:
            image = conn.getObject("Image", image_id)
            if image:
                images.append(image)

    return images
```

## Processing Images

### Batch Image Processing

```python
def process_images(conn, images, threshold):
    """
    Process multiple images.
    """
    results = []

    for image in images:
        print(f"Processing: {image.getName()}")

        # Get pixel data
        pixels = image.getPrimaryPixels()
        size_z = image.getSizeZ()
        size_c = image.getSizeC()
        size_t = image.getSizeT()

        # Process each plane
        for z in range(size_z):
            for c in range(size_c):
                for t in range(size_t):
                    plane = pixels.getPlane(z, c, t)

                    # Apply threshold
                    binary = (plane > threshold).astype(np.uint8)

                    # Count features
                    feature_count = count_features(binary)

                    results.append({
                        'image_id': image.getId(),
                        'image_name': image.getName(),
                        'z': z, 'c': c, 't': t,
                        'feature_count': feature_count
                    })

    return results
```

## Generating Outputs

### Return Messages

```python
# Simple message
message = "Processed 10 images successfully"
client.setOutput("Message", rstring(message))

# Detailed message
message = "Results:\n"
for result in results:
    message += f"Image {result['image_id']}: {result['count']} cells\n"
client.setOutput("Message", rstring(message))
```

### Return Images

```python
# Return newly created image
new_image = conn.createImageFromNumpySeq(...)
client.setOutput("New_Image", robject(new_image._obj))
```

### Return Files

```python
# Create and return file annotation
file_ann = conn.createFileAnnfromLocalFile(
    output_file_path,
    mimetype="text/csv",
    ns="analysis.results"
)

client.setOutput("Result_File", robject(file_ann._obj))
```

### Return Tables

```python
# Create OMERO table and return
resources = conn.c.sf.sharedResources()
table = create_results_table(resources, results)
orig_file = table.getOriginalFile()
table.close()

# Create file annotation
file_ann = omero.model.FileAnnotationI()
file_ann.setFile(orig_file)
file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

client.setOutput("Results_Table", robject(file_ann._obj))
```

## Complete Example Scripts

### Example 1: Maximum Intensity Projection

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import omero
from omero.gateway import BlitzGateway
import omero.scripts as scripts
from omero.rtypes import rlong, rstring, robject
import numpy as np

def run_script():
    client = scripts.client(
        'Maximum_Intensity_Projection.py',
        """
        Creates maximum intensity projection from Z-stack images.
        """,

        scripts.String("Data_Type", optional=False, grouping="1",
                      description="Process images from",
                      values=[rstring('Dataset'), rstring('Image')],
                      default=rstring('Image')),

        scripts.List("IDs", optional=False, grouping="2",
                    description="Dataset or Image ID(s)").ofType(rlong(0)),

        scripts.Bool("Link_to_Source", optional=True, grouping="3",
                    description="Link results to source dataset",
                    default=True),

        version="1.0"
    )

    try:
        conn = BlitzGateway(client_obj=client)
        script_params = client.getInputs(unwrap=True)

        # Get images
        images = get_images(conn, script_params)
        created_images = []

        for image in images:
            print(f"Processing: {image.getName()}")

            # Create MIP
            mip_image = create_mip(conn, image)
            if mip_image:
                created_images.append(mip_image)

        # Report results
        if created_images:
            message = f"Created {len(created_images)} MIP images"
            # Return first image for display
            client.setOutput("Message", rstring(message))
            client.setOutput("Result", robject(created_images[0]._obj))
        else:
            client.setOutput("Message", rstring("No images created"))

    finally:
        client.closeSession()

def get_images(conn, script_params):
    """Get images from script parameters."""
    images = []
    data_type = script_params["Data_Type"]
    ids = script_params["IDs"]

    if data_type == "Dataset":
        for dataset_id in ids:
            dataset = conn.getObject("Dataset", dataset_id)
            if dataset:
                images.extend(list(dataset.listChildren()))
    else:
        for image_id in ids:
            image = conn.getObject("Image", image_id)
            if image:
                images.append(image)

    return images

def create_mip(conn, source_image):
    """Create maximum intensity projection."""
    pixels = source_image.getPrimaryPixels()
    size_z = source_image.getSizeZ()
    size_c = source_image.getSizeC()
    size_t = source_image.getSizeT()

    if size_z == 1:
        print("  Skipping (single Z-section)")
        return None

    def plane_gen():
        for c in range(size_c):
            for t in range(size_t):
                # Get Z-stack
                z_stack = []
                for z in range(size_z):
                    plane = pixels.getPlane(z, c, t)
                    z_stack.append(plane)

                # Maximum projection
                max_proj = np.max(z_stack, axis=0)
                yield max_proj

    # Create new image
    new_image = conn.createImageFromNumpySeq(
        plane_gen(),
        f"{source_image.getName()}_MIP",
        1, size_c, size_t,
        description="Maximum intensity projection",
        dataset=source_image.getParent()
    )

    return new_image

if __name__ == "__main__":
    run_script()
```

### Example 2: Batch ROI Analysis

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import omero
from omero.gateway import BlitzGateway
import omero.scripts as scripts
from omero.rtypes import rlong, rstring, robject
import omero.grid

def run_script():
    client = scripts.client(
        'Batch_ROI_Analysis.py',
        """
        Analyzes ROIs across multiple images and creates results table.
        """,

        scripts.Long("Dataset_ID", optional=False,
                    description="Dataset with images and ROIs").ofType(rlong(0)),

        scripts.Long("Channel_Index", optional=True,
                    description="Channel to analyze (0-indexed)",
                    default=0, min=0),

        version="1.0"
    )

    try:
        conn = BlitzGateway(client_obj=client)
        script_params = client.getInputs(unwrap=True)

        dataset_id = script_params["Dataset_ID"]
        channel_index = script_params["Channel_Index"]

        # Get dataset
        dataset = conn.getObject("Dataset", dataset_id)
        if not dataset:
            client.setOutput("Message", rstring("Dataset not found"))
            return

        # Analyze ROIs
        results = analyze_rois(conn, dataset, channel_index)

        # Create table
        table_file = create_results_table(conn, dataset, results)

        # Report
        message = f"Analyzed {len(results)} ROIs from {dataset.getName()}"
        client.setOutput("Message", rstring(message))
        client.setOutput("Results_Table", robject(table_file._obj))

    finally:
        client.closeSession()

def analyze_rois(conn, dataset, channel_index):
    """Analyze all ROIs in dataset images."""
    roi_service = conn.getRoiService()
    results = []

    for image in dataset.listChildren():
        result = roi_service.findByImage(image.getId(), None)

        if not result.rois:
            continue

        # Get shape IDs
        shape_ids = []
        for roi in result.rois:
            for shape in roi.copyShapes():
                shape_ids.append(shape.id.val)

        # Get statistics
        stats = roi_service.getShapeStatsRestricted(
            shape_ids, 0, 0, [channel_index]
        )

        # Store results
        for i, stat in enumerate(stats):
            results.append({
                'image_id': image.getId(),
                'image_name': image.getName(),
                'shape_id': shape_ids[i],
                'mean': stat.mean[channel_index],
                'min': stat.min[channel_index],
                'max': stat.max[channel_index],
                'sum': stat.sum[channel_index],
                'area': stat.pointsCount[channel_index]
            })

    return results

def create_results_table(conn, dataset, results):
    """Create OMERO table from results."""
    # Prepare data
    image_ids = [r['image_id'] for r in results]
    shape_ids = [r['shape_id'] for r in results]
    means = [r['mean'] for r in results]
    mins = [r['min'] for r in results]
    maxs = [r['max'] for r in results]
    sums = [r['sum'] for r in results]
    areas = [r['area'] for r in results]

    # Create table
    resources = conn.c.sf.sharedResources()
    repository_id = resources.repositories().descriptions[0].getId().getValue()
    table = resources.newTable(repository_id, f"ROI_Analysis_{dataset.getId()}")

    # Define columns
    columns = [
        omero.grid.ImageColumn('Image', 'Source image', []),
        omero.grid.LongColumn('ShapeID', 'ROI shape ID', []),
        omero.grid.DoubleColumn('Mean', 'Mean intensity', []),
        omero.grid.DoubleColumn('Min', 'Min intensity', []),
        omero.grid.DoubleColumn('Max', 'Max intensity', []),
        omero.grid.DoubleColumn('Sum', 'Integrated density', []),
        omero.grid.LongColumn('Area', 'Area in pixels', [])
    ]
    table.initialize(columns)

    # Add data
    data = [
        omero.grid.ImageColumn('Image', 'Source image', image_ids),
        omero.grid.LongColumn('ShapeID', 'ROI shape ID', shape_ids),
        omero.grid.DoubleColumn('Mean', 'Mean intensity', means),
        omero.grid.DoubleColumn('Min', 'Min intensity', mins),
        omero.grid.DoubleColumn('Max', 'Max intensity', maxs),
        omero.grid.DoubleColumn('Sum', 'Integrated density', sums),
        omero.grid.LongColumn('Area', 'Area in pixels', areas)
    ]
    table.addData(data)

    orig_file = table.getOriginalFile()
    table.close()

    # Link to dataset
    file_ann = omero.model.FileAnnotationI()
    file_ann.setFile(orig_file)
    file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

    link = omero.model.DatasetAnnotationLinkI()
    link.setParent(dataset._obj)
    link.setChild(file_ann)
    conn.getUpdateService().saveAndReturnObject(link)

    return file_ann

if __name__ == "__main__":
    run_script()
```

## Script Deployment

### Installation Location

Scripts should be placed in the OMERO server scripts directory:
```
OMERO_DIR/lib/scripts/
```

### Recommended Structure

```
lib/scripts/
├── analysis/
│   ├── Cell_Counter.py
│   └── ROI_Analyzer.py
├── export/
│   ├── Export_Images.py
│   └── Export_ROIs.py
└── util/
    └── Helper_Functions.py
```

### Testing Scripts

```bash
# Test script syntax
python Script_Name.py

# Upload to OMERO
omero script upload Script_Name.py

# List scripts
omero script list

# Run script from CLI
omero script launch Script_ID Dataset_ID=123
```

## Best Practices

1. **Error Handling**: Always use try-finally to close session
2. **Progress Updates**: Print status messages for long operations
3. **Parameter Validation**: Check parameters before processing
4. **Memory Management**: Process large datasets in batches
5. **Documentation**: Include clear description and parameter docs
6. **Versioning**: Include version number in script
7. **Namespaces**: Use appropriate namespaces for outputs
8. **Return Objects**: Return created objects for client display
9. **Logging**: Use print() for server logs
10. **Testing**: Test with various input combinations

## Common Patterns

### Progress Reporting

```python
total = len(images)
for idx, image in enumerate(images):
    print(f"Processing {idx + 1}/{total}: {image.getName()}")
    # Process image
```

### Error Collection

```python
errors = []
for image in images:
    try:
        process_image(image)
    except Exception as e:
        errors.append(f"{image.getName()}: {str(e)}")

if errors:
    message = "Completed with errors:\n" + "\n".join(errors)
else:
    message = "All images processed successfully"
```

### Resource Cleanup

```python
try:
    # Script processing
    pass
finally:
    # Clean up temporary files
    if os.path.exists(temp_file):
        os.remove(temp_file)
    client.closeSession()
```

---

## Reference: Tables

# OMERO Tables

This reference covers creating and managing structured tabular data in OMERO using OMERO.tables.

## OMERO.tables Overview

OMERO.tables provides a way to store structured tabular data associated with OMERO objects. Tables are stored as HDF5 files and can be queried efficiently. Common use cases include:

- Storing quantitative measurements from images
- Recording analysis results
- Tracking experimental metadata
- Linking measurements to specific images or ROIs

## Column Types

OMERO.tables supports various column types:

- **LongColumn**: Integer values (64-bit)
- **DoubleColumn**: Floating-point values
- **StringColumn**: Text data (fixed max length)
- **BoolColumn**: Boolean values
- **LongArrayColumn**: Arrays of integers
- **DoubleArrayColumn**: Arrays of floats
- **FileColumn**: References to OMERO files
- **ImageColumn**: References to OMERO images
- **RoiColumn**: References to OMERO ROIs
- **WellColumn**: References to OMERO wells

## Creating Tables

### Basic Table Creation

```python
from random import random
import omero.grid

# Create unique table name
table_name = f"MyAnalysisTable_{random()}"

# Define columns (empty data for initialization)
col1 = omero.grid.LongColumn('ImageID', 'Image identifier', [])
col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel intensity', [])
col3 = omero.grid.StringColumn('Category', 'Classification', 64, [])

columns = [col1, col2, col3]

# Get resources and create table
resources = conn.c.sf.sharedResources()
repository_id = resources.repositories().descriptions[0].getId().getValue()
table = resources.newTable(repository_id, table_name)

# Initialize table with column definitions
table.initialize(columns)
```

### Add Data to Table

```python
# Prepare data
image_ids = [1, 2, 3, 4, 5]
intensities = [123.4, 145.2, 98.7, 156.3, 132.8]
categories = ["Good", "Good", "Poor", "Excellent", "Good"]

# Create data columns
data_col1 = omero.grid.LongColumn('ImageID', 'Image identifier', image_ids)
data_col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel intensity', intensities)
data_col3 = omero.grid.StringColumn('Category', 'Classification', 64, categories)

data = [data_col1, data_col2, data_col3]

# Add data to table
table.addData(data)

# Get file reference
orig_file = table.getOriginalFile()
table.close()  # Always close table when done
```

### Link Table to Dataset

```python
# Create file annotation from table
orig_file_id = orig_file.id.val
file_ann = omero.model.FileAnnotationI()
file_ann.setFile(omero.model.OriginalFileI(orig_file_id, False))
file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

# Link to dataset
link = omero.model.DatasetAnnotationLinkI()
link.setParent(omero.model.DatasetI(dataset_id, False))
link.setChild(omero.model.FileAnnotationI(file_ann.getId().getValue(), False))
conn.getUpdateService().saveAndReturnObject(link)

print(f"Linked table to dataset {dataset_id}")
```

## Column Types in Detail

### Long Column (Integers)

```python
# Column for integer values
image_ids = [101, 102, 103, 104, 105]
col = omero.grid.LongColumn('ImageID', 'Image identifier', image_ids)
```

### Double Column (Floats)

```python
# Column for floating-point values
measurements = [12.34, 56.78, 90.12, 34.56, 78.90]
col = omero.grid.DoubleColumn('Measurement', 'Value in microns', measurements)
```

### String Column (Text)

```python
# Column for text (max length required)
labels = ["Control", "Treatment A", "Treatment B", "Control", "Treatment A"]
col = omero.grid.StringColumn('Condition', 'Experimental condition', 64, labels)
```

### Boolean Column

```python
# Column for boolean values
flags = [True, False, True, True, False]
col = omero.grid.BoolColumn('QualityPass', 'Passes quality control', flags)
```

### Image Column (References to Images)

```python
# Column linking to OMERO images
image_ids = [101, 102, 103, 104, 105]
col = omero.grid.ImageColumn('Image', 'Source image', image_ids)
```

### ROI Column (References to ROIs)

```python
# Column linking to OMERO ROIs
roi_ids = [201, 202, 203, 204, 205]
col = omero.grid.RoiColumn('ROI', 'Associated ROI', roi_ids)
```

### Array Columns

```python
# Column for arrays of doubles
histogram_data = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [12, 22, 32, 42]
]
col = omero.grid.DoubleArrayColumn('Histogram', 'Intensity histogram', histogram_data)

# Column for arrays of longs
bin_counts = [[5, 10, 15], [8, 12, 16], [6, 11, 14]]
col = omero.grid.LongArrayColumn('Bins', 'Histogram bins', bin_counts)
```

## Reading Table Data

### Open Existing Table

```python
# Get table file by name
orig_table_file = conn.getObject("OriginalFile",
                                 attributes={'name': table_name})

# Open table
resources = conn.c.sf.sharedResources()
table = resources.openTable(orig_table_file._obj)

print(f"Opened table: {table.getOriginalFile().getName().getValue()}")
print(f"Number of rows: {table.getNumberOfRows()}")
```

### Read All Data

```python
# Get column headers
print("Columns:")
for col in table.getHeaders():
    print(f"  {col.name}: {col.description}")

# Read all data
row_count = table.getNumberOfRows()
data = table.readCoordinates(range(row_count))

# Display data
for col in data.columns:
    print(f"\nColumn: {col.name}")
    for value in col.values:
        print(f"  {value}")

table.close()
```

### Read Specific Rows

```python
# Read rows 10-20
start = 10
stop = 20
data = table.read(list(range(table.getHeaders().__len__())), start, stop)

for col in data.columns:
    print(f"Column: {col.name}")
    for value in col.values:
        print(f"  {value}")
```

### Read Specific Columns

```python
# Read only columns 0 and 2
column_indices = [0, 2]
start = 0
stop = table.getNumberOfRows()

data = table.read(column_indices, start, stop)

for col in data.columns:
    print(f"Column: {col.name}")
    print(f"Values: {col.values}")
```

## Querying Tables

### Query with Conditions

```python
# Query rows where MeanIntensity > 100
row_count = table.getNumberOfRows()

query_rows = table.getWhereList(
    "(MeanIntensity > 100)",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

print(f"Found {len(query_rows)} matching rows")

# Read matching rows
data = table.readCoordinates(query_rows)

for col in data.columns:
    print(f"\n{col.name}:")
    for value in col.values:
        print(f"  {value}")
```

### Complex Queries

```python
# Multiple conditions with AND
query_rows = table.getWhereList(
    "(MeanIntensity > 100) & (MeanIntensity < 150)",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

# Multiple conditions with OR
query_rows = table.getWhereList(
    "(Category == 'Good') | (Category == 'Excellent')",
    variables={},
    start=0,
    stop=row_count,
    step=0
)

# String matching
query_rows = table.getWhereList(
    "(Category == 'Good')",
    variables={},
    start=0,
    stop=row_count,
    step=0
)
```

## Complete Example: Image Analysis Results

```python
from omero.gateway import BlitzGateway
import omero.grid
import omero.model
import numpy as np

HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Get dataset
    dataset = conn.getObject("Dataset", dataset_id)
    print(f"Analyzing dataset: {dataset.getName()}")

    # Collect measurements from images
    image_ids = []
    mean_intensities = []
    max_intensities = []
    cell_counts = []

    for image in dataset.listChildren():
        image_ids.append(image.getId())

        # Get pixel data
        pixels = image.getPrimaryPixels()
        plane = pixels.getPlane(0, 0, 0)  # Z=0, C=0, T=0

        # Calculate statistics
        mean_intensities.append(float(np.mean(plane)))
        max_intensities.append(float(np.max(plane)))

        # Simulate cell count (would be from actual analysis)
        cell_counts.append(np.random.randint(50, 200))

    # Create table
    table_name = f"Analysis_Results_{dataset.getId()}"

    # Define columns
    col1 = omero.grid.ImageColumn('Image', 'Source image', [])
    col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel value', [])
    col3 = omero.grid.DoubleColumn('MaxIntensity', 'Maximum pixel value', [])
    col4 = omero.grid.LongColumn('CellCount', 'Number of cells detected', [])

    # Initialize table
    resources = conn.c.sf.sharedResources()
    repository_id = resources.repositories().descriptions[0].getId().getValue()
    table = resources.newTable(repository_id, table_name)
    table.initialize([col1, col2, col3, col4])

    # Add data
    data_col1 = omero.grid.ImageColumn('Image', 'Source image', image_ids)
    data_col2 = omero.grid.DoubleColumn('MeanIntensity', 'Mean pixel value',
                                        mean_intensities)
    data_col3 = omero.grid.DoubleColumn('MaxIntensity', 'Maximum pixel value',
                                        max_intensities)
    data_col4 = omero.grid.LongColumn('CellCount', 'Number of cells detected',
                                      cell_counts)

    table.addData([data_col1, data_col2, data_col3, data_col4])

    # Get file and close table
    orig_file = table.getOriginalFile()
    table.close()

    # Link to dataset
    orig_file_id = orig_file.id.val
    file_ann = omero.model.FileAnnotationI()
    file_ann.setFile(omero.model.OriginalFileI(orig_file_id, False))
    file_ann = conn.getUpdateService().saveAndReturnObject(file_ann)

    link = omero.model.DatasetAnnotationLinkI()
    link.setParent(omero.model.DatasetI(dataset_id, False))
    link.setChild(omero.model.FileAnnotationI(file_ann.getId().getValue(), False))
    conn.getUpdateService().saveAndReturnObject(link)

    print(f"Created and linked table with {len(image_ids)} rows")

    # Query results
    table = resources.openTable(orig_file)

    high_cell_count_rows = table.getWhereList(
        "(CellCount > 100)",
        variables={},
        start=0,
        stop=table.getNumberOfRows(),
        step=0
    )

    print(f"Images with >100 cells: {len(high_cell_count_rows)}")

    # Read those rows
    data = table.readCoordinates(high_cell_count_rows)
    for i in range(len(high_cell_count_rows)):
        img_id = data.columns[0].values[i]
        count = data.columns[3].values[i]
        print(f"  Image {img_id}: {count} cells")

    table.close()
```

## Retrieve Tables from Objects

### Find Tables Attached to Dataset

```python
# Get dataset
dataset = conn.getObject("Dataset", dataset_id)

# List file annotations
for ann in dataset.listAnnotations():
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        file_obj = ann.getFile()
        file_name = file_obj.getName()

        # Check if it's a table (might have specific naming pattern)
        if "Table" in file_name or file_name.endswith(".h5"):
            print(f"Found table: {file_name} (ID: {file_obj.getId()})")

            # Open and inspect
            resources = conn.c.sf.sharedResources()
            table = resources.openTable(file_obj._obj)

            print(f"  Rows: {table.getNumberOfRows()}")
            print(f"  Columns:")
            for col in table.getHeaders():
                print(f"    {col.name}")

            table.close()
```

## Updating Tables

### Append Rows

```python
# Open existing table
resources = conn.c.sf.sharedResources()
table = resources.openTable(orig_file._obj)

# Prepare new data
new_image_ids = [106, 107]
new_intensities = [88.9, 92.3]
new_categories = ["Good", "Excellent"]

# Create data columns
data_col1 = omero.grid.LongColumn('ImageID', '', new_image_ids)
data_col2 = omero.grid.DoubleColumn('MeanIntensity', '', new_intensities)
data_col3 = omero.grid.StringColumn('Category', '', 64, new_categories)

# Append data
table.addData([data_col1, data_col2, data_col3])

print(f"New row count: {table.getNumberOfRows()}")
table.close()
```

## Deleting Tables

### Delete Table File

```python
# Get file object
orig_file = conn.getObject("OriginalFile", file_id)

# Delete file (also deletes table)
conn.deleteObjects("OriginalFile", [file_id], wait=True)
print(f"Deleted table file {file_id}")
```

### Unlink Table from Object

```python
# Find annotation links
dataset = conn.getObject("Dataset", dataset_id)

for ann in dataset.listAnnotations():
    if isinstance(ann, omero.gateway.FileAnnotationWrapper):
        if "Table" in ann.getFile().getName():
            # Delete link (keeps table, removes association)
            conn.deleteObjects("DatasetAnnotationLink",
                             [ann.link.getId()],
                             wait=True)
            print(f"Unlinked table from dataset")
```

## Best Practices

1. **Descriptive Names**: Use meaningful table and column names
2. **Close Tables**: Always close tables after use
3. **String Length**: Set appropriate max length for string columns
4. **Link to Objects**: Attach tables to relevant datasets or projects
5. **Use References**: Use ImageColumn, RoiColumn for object references
6. **Query Efficiently**: Use getWhereList() instead of reading all data
7. **Document**: Add descriptions to columns
8. **Version Control**: Include version info in table name or metadata
9. **Batch Operations**: Add data in batches for better performance
10. **Error Handling**: Check for None returns and handle exceptions

## Common Patterns

### ROI Measurements Table

```python
# Table structure for ROI measurements
columns = [
    omero.grid.ImageColumn('Image', 'Source image', []),
    omero.grid.RoiColumn('ROI', 'Measured ROI', []),
    omero.grid.LongColumn('ChannelIndex', 'Channel number', []),
    omero.grid.DoubleColumn('Area', 'ROI area in pixels', []),
    omero.grid.DoubleColumn('MeanIntensity', 'Mean intensity', []),
    omero.grid.DoubleColumn('IntegratedDensity', 'Sum of intensities', []),
    omero.grid.StringColumn('CellType', 'Cell classification', 32, [])
]
```

### Time Series Data Table

```python
# Table structure for time series measurements
columns = [
    omero.grid.ImageColumn('Image', 'Time series image', []),
    omero.grid.LongColumn('Timepoint', 'Time index', []),
    omero.grid.DoubleColumn('Timestamp', 'Time in seconds', []),
    omero.grid.DoubleColumn('Value', 'Measured value', []),
    omero.grid.StringColumn('Measurement', 'Type of measurement', 64, [])
]
```

### Screening Results Table

```python
# Table structure for screening plate analysis
columns = [
    omero.grid.WellColumn('Well', 'Plate well', []),
    omero.grid.LongColumn('FieldIndex', 'Field number', []),
    omero.grid.DoubleColumn('CellCount', 'Number of cells', []),
    omero.grid.DoubleColumn('Viability', 'Percent viable', []),
    omero.grid.StringColumn('Phenotype', 'Observed phenotype', 128, []),
    omero.grid.BoolColumn('Hit', 'Hit in screen', [])
]
```
