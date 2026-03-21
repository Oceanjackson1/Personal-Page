---
title: "Notebooklm"
description: "Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through docume..."
category: "writing"
source: "community"
author: "Community"
tags: ["notebooklm"]
date: 2026-03-20
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details missing, use Smart Add to discover them.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## Core Workflow

### Step 1: Check Authentication Status
```bash
python scripts/run.py auth_manager.py status
```

If not authenticated, proceed to setup.

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```

**Important:**
- Browser is VISIBLE for authentication
- Browser window opens automatically
- User must manually log in to Google
- Tell user: "A browser window will open for Google login"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# BEFORE ADDING: Ask user for metadata if unknown!
# "What does this notebook contain?"
# "What topics should I tag it with?"

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \  # REQUIRED - ASK USER IF UNKNOWN!
  --topics "topic1,topic2,topic3"  # REQUIRED - ASK USER IF UNKNOWN!

# Search notebooks by topic
python scripts/run.py notebook_manager.py search --query "keyword"

# Set active notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Quick Workflow
1. Check library: `python scripts/run.py notebook_manager.py list`
2. Ask question: `python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook if set)
python scripts/run.py ask_question.py --question "Your question here"

# Query specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required Claude Behavior:**
1. **STOP** - Do not immediately respond to user
2. **ANALYZE** - Compare answer to user's original request
3. **IDENTIFY GAPS** - Determine if more information needed
4. **ASK FOLLOW-UP** - If gaps exist, immediately ask:
   ```bash
   python scripts/run.py ask_question.py --question "Follow-up with context..."
   ```
5. **REPEAT** - Continue until information is complete
6. **SYNTHESIZE** - Combine all answers before responding to user

## Script Reference

### Authentication Management (`auth_manager.py`)
```bash
python scripts/run.py auth_manager.py setup    # Initial setup (browser visible)
python scripts/run.py auth_manager.py status   # Check authentication
python scripts/run.py auth_manager.py reauth   # Re-authenticate (browser visible)
python scripts/run.py auth_manager.py clear    # Clear authentication
```

### Notebook Management (`notebook_manager.py`)
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### Question Interface (`ask_question.py`)
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Data Cleanup (`cleanup_manager.py`)
```bash
python scripts/run.py cleanup_manager.py                    # Preview cleanup
python scripts/run.py cleanup_manager.py --confirm          # Execute cleanup
python scripts/run.py cleanup_manager.py --preserve-library # Keep notebooks
```

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Chromium browser installs automatically
- Everything isolated in skill directory

Manual setup (only if automatic fails):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Data Storage

All data stored in `~/.claude/skills/notebooklm/data/`:
- `library.json` - Notebook metadata
- `auth_info.json` - Authentication status
- `browser_state/` - Browser cookies and session

**Security:** Protected by `.gitignore`, never commit to git.

## Configuration

Optional `.env` file in skill directory:
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Decision Flow

```
User mentions NotebookLM
    ↓
Check auth → python scripts/run.py auth_manager.py status
    ↓
If not authenticated → python scripts/run.py auth_manager.py setup
    ↓
Check/Add notebook → python scripts/run.py notebook_manager.py list/add (with --description)
    ↓
Activate notebook → python scripts/run.py notebook_manager.py activate --id ID
    ↓
Ask question → python scripts/run.py ask_question.py --question "..."
    ↓
See "Is that ALL you need?" → Ask follow-ups until complete
    ↓
Synthesize and respond to user
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Authentication fails | Browser must be visible for setup! --show-browser |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook not found | Check with `notebook_manager.py list` |

## Best Practices

1. **Always use run.py** - Handles environment automatically
2. **Check auth first** - Before any operations
3. **Follow-up questions** - Don't stop at first answer
4. **Browser visible for auth** - Required for manual login
5. **Include context** - Each question is independent
6. **Synthesize answers** - Combine multiple responses

## Limitations

- No session persistence (each question = new browser)
- Rate limits on free Google accounts (50 queries/day)
- Manual upload required (user must add docs to NotebookLM)
- Browser overhead (few seconds per question)

## Resources (Skill Structure)

**Important directories and files:**

- `scripts/` - All automation scripts (ask_question.py, notebook_manager.py, etc.)
- `data/` - Local storage for authentication and notebook library
- `references/` - Extended documentation:
  - `api_reference.md` - Detailed API documentation for all scripts
  - `troubleshooting.md` - Common issues and solutions
  - `usage_patterns.md` - Best practices and workflow examples
- `.venv/` - Isolated Python environment (auto-created on first run)
- `.gitignore` - Protects sensitive data from being committed

---

## Reference: Api_Reference

# NotebookLM Skill API Reference

Complete API documentation for all NotebookLM skill modules.

## Important: Always Use run.py Wrapper

**All commands must use the `run.py` wrapper to ensure proper environment:**

```bash
# ✅ CORRECT:
python scripts/run.py [script_name].py [arguments]

# ❌ WRONG:
python scripts/[script_name].py [arguments]  # Will fail without venv!
```

## Core Scripts

### ask_question.py
Query NotebookLM with automated browser interaction.

```bash
# Basic usage
python scripts/run.py ask_question.py --question "Your question"

# With specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# With direct URL
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser (debugging)
python scripts/run.py ask_question.py --question "..." --show-browser
```

**Parameters:**
- `--question` (required): Question to ask
- `--notebook-id`: Use notebook from library
- `--notebook-url`: Use URL directly
- `--show-browser`: Make browser visible

**Returns:** Answer text with follow-up prompt appended

### notebook_manager.py
Manage notebook library with CRUD operations.

```bash
# Smart Add (discover content first)
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"
# Then add with discovered info
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Name" \
  --description "Description" \
  --topics "topic1,topic2"

# Direct add (when you know the content)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Name" \
  --description "What it contains" \
  --topics "topic1,topic2"

# List notebooks
python scripts/run.py notebook_manager.py list

# Search notebooks
python scripts/run.py notebook_manager.py search --query "keyword"

# Activate notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id

# Show statistics
python scripts/run.py notebook_manager.py stats
```

**Commands:**
- `add`: Add notebook (requires --url, --name, --topics)
- `list`: Show all notebooks
- `search`: Find notebooks by keyword
- `activate`: Set default notebook
- `remove`: Delete from library
- `stats`: Display library statistics

### auth_manager.py
Handle Google authentication and browser state.

```bash
# Setup (browser visible for login)
python scripts/run.py auth_manager.py setup

# Check status
python scripts/run.py auth_manager.py status

# Re-authenticate
python scripts/run.py auth_manager.py reauth

# Clear authentication
python scripts/run.py auth_manager.py clear
```

**Commands:**
- `setup`: Initial authentication (browser MUST be visible)
- `status`: Check if authenticated
- `reauth`: Clear and re-setup
- `clear`: Remove all auth data

### cleanup_manager.py
Clean skill data with preservation options.

```bash
# Preview cleanup
python scripts/run.py cleanup_manager.py

# Execute cleanup
python scripts/run.py cleanup_manager.py --confirm

# Keep library
python scripts/run.py cleanup_manager.py --confirm --preserve-library

# Force without prompt
python scripts/run.py cleanup_manager.py --confirm --force
```

**Options:**
- `--confirm`: Actually perform cleanup
- `--preserve-library`: Keep notebook library
- `--force`: Skip confirmation prompt

### run.py
Script wrapper that handles environment setup.

```bash
# Usage
python scripts/run.py [script_name].py [arguments]

# Examples
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."
```

**Automatic actions:**
1. Creates `.venv` if missing
2. Installs dependencies
3. Activates environment
4. Executes target script

## Python API Usage

### Using subprocess with run.py

```python
import subprocess
import json

# Always use run.py wrapper
result = subprocess.run([
    "python", "scripts/run.py", "ask_question.py",
    "--question", "Your question",
    "--notebook-id", "notebook-id"
], capture_output=True, text=True)

answer = result.stdout
```

### Direct imports (after venv exists)

```python
# Only works if venv is already created and activated
from notebook_manager import NotebookLibrary
from auth_manager import AuthManager

library = NotebookLibrary()
notebooks = library.list_notebooks()

auth = AuthManager()
is_auth = auth.is_authenticated()
```

## Data Storage

Location: `~/.claude/skills/notebooklm/data/`

```
data/
├── library.json       # Notebook metadata
├── auth_info.json     # Auth status
└── browser_state/     # Browser cookies
    └── state.json
```

**Security:** Protected by `.gitignore`, never commit.

## Environment Variables

Optional `.env` file configuration:

```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default display
STEALTH_ENABLED=true     # Human behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Error Handling

Common patterns:

```python
# Using run.py prevents most errors
result = subprocess.run([
    "python", "scripts/run.py", "ask_question.py",
    "--question", "Question"
], capture_output=True, text=True)

if result.returncode != 0:
    error = result.stderr
    if "rate limit" in error.lower():
        # Wait or switch accounts
        pass
    elif "not authenticated" in error.lower():
        # Run auth setup
        subprocess.run(["python", "scripts/run.py", "auth_manager.py", "setup"])
```

## Rate Limits

Free Google accounts: 50 queries/day

Solutions:
1. Wait for reset (midnight PST)
2. Switch accounts with `reauth`
3. Use multiple Google accounts

## Advanced Patterns

### Parallel Queries

```python
import concurrent.futures
import subprocess

def query(question, notebook_id):
    result = subprocess.run([
        "python", "scripts/run.py", "ask_question.py",
        "--question", question,
        "--notebook-id", notebook_id
    ], capture_output=True, text=True)
    return result.stdout

# Run multiple queries simultaneously
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(query, q, nb)
        for q, nb in zip(questions, notebooks)
    ]
    results = [f.result() for f in futures]
```

### Batch Processing

```python
def batch_research(questions, notebook_id):
    results = []
    for question in questions:
        result = subprocess.run([
            "python", "scripts/run.py", "ask_question.py",
            "--question", question,
            "--notebook-id", notebook_id
        ], capture_output=True, text=True)
        results.append(result.stdout)
        time.sleep(2)  # Avoid rate limits
    return results
```

## Module Classes

### NotebookLibrary
- `add_notebook(url, name, topics)`
- `list_notebooks()`
- `search_notebooks(query)`
- `get_notebook(notebook_id)`
- `activate_notebook(notebook_id)`
- `remove_notebook(notebook_id)`

### AuthManager
- `is_authenticated()`
- `setup_auth(headless=False)`
- `get_auth_info()`
- `clear_auth()`
- `validate_auth()`

### BrowserSession (internal)
- Handles browser automation
- Manages stealth behavior
- Not intended for direct use

## Best Practices

1. **Always use run.py** - Ensures environment
2. **Check auth first** - Before operations
3. **Handle rate limits** - Implement retries
4. **Include context** - Questions are independent
5. **Clean sessions** - Use cleanup_manager

---

## Reference: Troubleshooting

# NotebookLM Skill Troubleshooting Guide

## Quick Fix Table

| Error | Solution |
|-------|----------|
| ModuleNotFoundError | Use `python scripts/run.py [script].py` |
| Authentication failed | Browser must be visible for setup |
| Browser crash | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Rate limit hit | Wait 1 hour or switch accounts |
| Notebook not found | `python scripts/run.py notebook_manager.py list` |
| Script not working | Always use run.py wrapper |

## Critical: Always Use run.py

Most issues are solved by using the run.py wrapper:

```bash
# ✅ CORRECT - Always:
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never:
python scripts/auth_manager.py status  # ModuleNotFoundError!
```

## Common Issues and Solutions

### Authentication Issues

#### Not authenticated error
```
Error: Not authenticated. Please run auth setup first.
```

**Solution:**
```bash
# Check status
python scripts/run.py auth_manager.py status

# Setup authentication (browser MUST be visible!)
python scripts/run.py auth_manager.py setup
# User must manually log in to Google

# If setup fails, try re-authentication
python scripts/run.py auth_manager.py reauth
```

#### Authentication expires frequently
**Solution:**
```bash
# Clear old authentication
python scripts/run.py cleanup_manager.py --preserve-library

# Fresh authentication setup
python scripts/run.py auth_manager.py setup --timeout 15

# Use persistent browser profile
export PERSIST_AUTH=true
```

#### Google blocks automated login
**Solution:**
1. Use dedicated Google account for automation
2. Enable "Less secure app access" if available
3. ALWAYS use visible browser:
```bash
python scripts/run.py auth_manager.py setup
# Browser MUST be visible - user logs in manually
# NO headless parameter exists - use --show-browser for debugging
```

### Browser Issues

#### Browser crashes or hangs
```
TimeoutError: Waiting for selector failed
```

**Solution:**
```bash
# Kill hanging processes
pkill -f chromium
pkill -f chrome

# Clean browser state
python scripts/run.py cleanup_manager.py --confirm --preserve-library

# Re-authenticate
python scripts/run.py auth_manager.py reauth
```

#### Browser not found error
**Solution:**
```bash
# Install Chromium via run.py (automatic)
python scripts/run.py auth_manager.py status
# run.py will install Chromium automatically

# Or manual install if needed
cd ~/.claude/skills/notebooklm
source .venv/bin/activate
python -m patchright install chromium
```

### Rate Limiting

#### Rate limit exceeded (50 queries/day)
**Solutions:**

**Option 1: Wait**
```bash
# Check when limit resets (usually midnight PST)
date -d "tomorrow 00:00 PST"
```

**Option 2: Switch accounts**
```bash
# Clear current auth
python scripts/run.py auth_manager.py clear

# Login with different account
python scripts/run.py auth_manager.py setup
```

**Option 3: Rotate accounts**
```python
# Use multiple accounts
accounts = ["account1", "account2"]
for account in accounts:
    # Switch account on rate limit
    subprocess.run(["python", "scripts/run.py", "auth_manager.py", "reauth"])
```

### Notebook Access Issues

#### Notebook not found
**Solution:**
```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# Search for notebook
python scripts/run.py notebook_manager.py search --query "keyword"

# Add notebook if missing
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/..." \
  --name "Name" \
  --topics "topics"
```

#### Access denied to notebook
**Solution:**
1. Check if notebook is still shared publicly
2. Re-add notebook with updated URL
3. Verify correct Google account is used

#### Wrong notebook being used
**Solution:**
```bash
# Check active notebook
python scripts/run.py notebook_manager.py list | grep "active"

# Activate correct notebook
python scripts/run.py notebook_manager.py activate --id correct-id
```

### Virtual Environment Issues

#### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'patchright'
```

**Solution:**
```bash
# ALWAYS use run.py - it handles venv automatically!
python scripts/run.py [any_script].py

# run.py will:
# 1. Create .venv if missing
# 2. Install dependencies
# 3. Run the script
```

#### Wrong Python version
**Solution:**
```bash
# Check Python version (needs 3.8+)
python --version

# If wrong version, specify correct Python
python3.8 scripts/run.py auth_manager.py status
```

### Network Issues

#### Connection timeouts
**Solution:**
```bash
# Increase timeout
export TIMEOUT_SECONDS=60

# Check connectivity
ping notebooklm.google.com

# Use proxy if needed
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### Data Issues

#### Corrupted notebook library
```
JSON decode error when listing notebooks
```

**Solution:**
```bash
# Backup current library
cp ~/.claude/skills/notebooklm/data/library.json library.backup.json

# Reset library
rm ~/.claude/skills/notebooklm/data/library.json

# Re-add notebooks
python scripts/run.py notebook_manager.py add --url ... --name ...
```

#### Disk space full
**Solution:**
```bash
# Check disk usage
df -h ~/.claude/skills/notebooklm/data/

# Clean up
python scripts/run.py cleanup_manager.py --confirm --preserve-library
```

## Debugging Techniques

### Enable verbose logging
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python scripts/run.py ask_question.py --question "Test" --show-browser
```

### Test individual components
```bash
# Test authentication
python scripts/run.py auth_manager.py status

# Test notebook access
python scripts/run.py notebook_manager.py list

# Test browser launch
python scripts/run.py ask_question.py --question "test" --show-browser
```

### Save screenshots on error
Add to scripts for debugging:
```python
try:
    # Your code
except Exception as e:
    page.screenshot(path=f"error_{timestamp}.png")
    raise e
```

## Recovery Procedures

### Complete reset
```bash
#!/bin/bash
# Kill processes
pkill -f chromium

# Backup library if exists
if [ -f ~/.claude/skills/notebooklm/data/library.json ]; then
    cp ~/.claude/skills/notebooklm/data/library.json ~/library.backup.json
fi

# Clean everything
cd ~/.claude/skills/notebooklm
python scripts/run.py cleanup_manager.py --confirm --force

# Remove venv
rm -rf .venv

# Reinstall (run.py will handle this)
python scripts/run.py auth_manager.py setup

# Restore library if backup exists
if [ -f ~/library.backup.json ]; then
    mkdir -p ~/.claude/skills/notebooklm/data/
    cp ~/library.backup.json ~/.claude/skills/notebooklm/data/library.json
fi
```

### Partial recovery (keep data)
```bash
# Keep auth and library, fix execution
cd ~/.claude/skills/notebooklm
rm -rf .venv

# run.py will recreate venv automatically
python scripts/run.py auth_manager.py status
```

## Error Messages Reference

### Authentication Errors
| Error | Cause | Solution |
|-------|-------|----------|
| Not authenticated | No valid auth | `run.py auth_manager.py setup` |
| Authentication expired | Session old | `run.py auth_manager.py reauth` |
| Invalid credentials | Wrong account | Check Google account |
| 2FA required | Security challenge | Complete in visible browser |

### Browser Errors
| Error | Cause | Solution |
|-------|-------|----------|
| Browser not found | Chromium missing | Use run.py (auto-installs) |
| Connection refused | Browser crashed | Kill processes, restart |
| Timeout waiting | Page slow | Increase timeout |
| Context closed | Browser terminated | Check logs for crashes |

### Notebook Errors
| Error | Cause | Solution |
|-------|-------|----------|
| Notebook not found | Invalid ID | `run.py notebook_manager.py list` |
| Access denied | Not shared | Re-share in NotebookLM |
| Invalid URL | Wrong format | Use full NotebookLM URL |
| No active notebook | None selected | `run.py notebook_manager.py activate` |

## Prevention Tips

1. **Always use run.py** - Prevents 90% of issues
2. **Regular maintenance** - Clear browser state weekly
3. **Monitor queries** - Track daily count to avoid limits
4. **Backup library** - Export notebook list regularly
5. **Use dedicated account** - Separate Google account for automation

## Getting Help

### Diagnostic information to collect
```bash
# System info
python --version
cd ~/.claude/skills/notebooklm
ls -la

# Skill status
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list | head -5

# Check data directory
ls -la ~/.claude/skills/notebooklm/data/
```

### Common questions

**Q: Why doesn't this work in Claude web UI?**
A: Web UI has no network access. Use local Claude Code.

**Q: Can I use multiple Google accounts?**
A: Yes, use `run.py auth_manager.py reauth` to switch.

**Q: How to increase rate limit?**
A: Use multiple accounts or upgrade to Google Workspace.

**Q: Is this safe for my Google account?**
A: Use dedicated account for automation. Only accesses NotebookLM.

---

## Reference: Usage_Patterns

# NotebookLM Skill Usage Patterns

Advanced patterns for using the NotebookLM skill effectively.

## Critical: Always Use run.py

**Every command must use the run.py wrapper:**
```bash
# ✅ CORRECT:
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG:
python scripts/auth_manager.py status  # Will fail!
```

## Pattern 1: Initial Setup

```bash
# 1. Check authentication (using run.py!)
python scripts/run.py auth_manager.py status

# 2. If not authenticated, setup (Browser MUST be visible!)
python scripts/run.py auth_manager.py setup
# Tell user: "Please log in to Google in the browser window"

# 3. Add first notebook - ASK USER FOR DETAILS FIRST!
# Ask: "What does this notebook contain?"
# Ask: "What topics should I tag it with?"
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "User provided name" \
  --description "User provided description" \  # NEVER GUESS!
  --topics "user,provided,topics"  # NEVER GUESS!
```

**Critical Notes:**
- Virtual environment created automatically by run.py
- Browser MUST be visible for authentication
- ALWAYS discover content via query OR ask user for notebook metadata

## Pattern 2: Adding Notebooks (Smart Discovery!)

**When user shares a NotebookLM URL:**

**OPTION A: Smart Discovery (Recommended)**
```bash
# 1. Query the notebook to discover its content
python scripts/run.py ask_question.py \
  --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" \
  --notebook-url "[URL]"

# 2. Use discovered info to add it
python scripts/run.py notebook_manager.py add \
  --url "[URL]" \
  --name "[Based on content]" \
  --description "[From discovery]" \
  --topics "[Extracted topics]"
```

**OPTION B: Ask User (Fallback)**
```bash
# If discovery fails, ask user:
"What does this notebook contain?"
"What topics does it cover?"

# Then add with user-provided info:
python scripts/run.py notebook_manager.py add \
  --url "[URL]" \
  --name "[User's answer]" \
  --description "[User's description]" \
  --topics "[User's topics]"
```

**NEVER:**
- Guess what's in a notebook
- Use generic descriptions
- Skip discovering content

## Pattern 3: Daily Research Workflow

```bash
# Check library
python scripts/run.py notebook_manager.py list

# Research with comprehensive questions
python scripts/run.py ask_question.py \
  --question "Detailed question with all context" \
  --notebook-id notebook-id

# Follow-up when you see "Is that ALL you need to know?"
python scripts/run.py ask_question.py \
  --question "Follow-up question with previous context"
```

## Pattern 4: Follow-Up Questions (CRITICAL!)

When NotebookLM responds with "EXTREMELY IMPORTANT: Is that ALL you need to know?":

```python
# 1. STOP - Don't respond to user yet
# 2. ANALYZE - Is answer complete?
# 3. If gaps exist, ask follow-up:
python scripts/run.py ask_question.py \
  --question "Specific follow-up with context from previous answer"

# 4. Repeat until complete
# 5. Only then synthesize and respond to user
```

## Pattern 5: Multi-Notebook Research

```python
# Query different notebooks for comparison
python scripts/run.py notebook_manager.py activate --id notebook-1
python scripts/run.py ask_question.py --question "Question"

python scripts/run.py notebook_manager.py activate --id notebook-2
python scripts/run.py ask_question.py --question "Same question"

# Compare and synthesize answers
```

## Pattern 6: Error Recovery

```bash
# If authentication fails
python scripts/run.py auth_manager.py status
python scripts/run.py auth_manager.py reauth  # Browser visible!

# If browser crashes
python scripts/run.py cleanup_manager.py --preserve-library
python scripts/run.py auth_manager.py setup  # Browser visible!

# If rate limited
# Wait or switch accounts
python scripts/run.py auth_manager.py reauth  # Login with different account
```

## Pattern 7: Batch Processing

```bash
#!/bin/bash
NOTEBOOK_ID="notebook-id"
QUESTIONS=(
    "First comprehensive question"
    "Second comprehensive question"
    "Third comprehensive question"
)

for question in "${QUESTIONS[@]}"; do
    echo "Asking: $question"
    python scripts/run.py ask_question.py \
        --question "$question" \
        --notebook-id "$NOTEBOOK_ID"
    sleep 2  # Avoid rate limits
done
```

## Pattern 8: Automated Research Script

```python
#!/usr/bin/env python
import subprocess

def research_topic(topic, notebook_id):
    # Comprehensive question
    question = f"""
    Explain {topic} in detail:
    1. Core concepts
    2. Implementation details
    3. Best practices
    4. Common pitfalls
    5. Examples
    """

    result = subprocess.run([
        "python", "scripts/run.py", "ask_question.py",
        "--question", question,
        "--notebook-id", notebook_id
    ], capture_output=True, text=True)

    return result.stdout
```

## Pattern 9: Notebook Organization

```python
# Organize by domain - with proper metadata
# ALWAYS ask user for descriptions!

# Backend notebooks
add_notebook("Backend API", "Complete API documentation", "api,rest,backend")
add_notebook("Database", "Schema and queries", "database,sql,backend")

# Frontend notebooks
add_notebook("React Docs", "React framework documentation", "react,frontend")
add_notebook("CSS Framework", "Styling documentation", "css,styling,frontend")

# Search by domain
python scripts/run.py notebook_manager.py search --query "backend"
python scripts/run.py notebook_manager.py search --query "frontend"
```

## Pattern 10: Integration with Development

```python
# Query documentation during development
def check_api_usage(api_endpoint):
    result = subprocess.run([
        "python", "scripts/run.py", "ask_question.py",
        "--question", f"Parameters and response format for {api_endpoint}",
        "--notebook-id", "api-docs"
    ], capture_output=True, text=True)

    # If follow-up needed
    if "Is that ALL you need" in result.stdout:
        # Ask for examples
        follow_up = subprocess.run([
            "python", "scripts/run.py", "ask_question.py",
            "--question", f"Show code examples for {api_endpoint}",
            "--notebook-id", "api-docs"
        ], capture_output=True, text=True)

    return combine_answers(result.stdout, follow_up.stdout)
```

## Best Practices

### 1. Question Formulation
- Be specific and comprehensive
- Include all context in each question
- Request structured responses
- Ask for examples when needed

### 2. Notebook Management
- **ALWAYS ask user for metadata**
- Use descriptive names
- Add comprehensive topics
- Keep URLs current

### 3. Performance
- Batch related questions
- Use parallel processing for different notebooks
- Monitor rate limits (50/day)
- Switch accounts if needed

### 4. Error Handling
- Always use run.py to prevent venv issues
- Check auth before operations
- Implement retry logic
- Have fallback notebooks ready

### 5. Security
- Use dedicated Google account
- Never commit data/ directory
- Regularly refresh auth
- Track all access

## Common Workflows for Claude

### Workflow 1: User Sends NotebookLM URL

```python
# 1. Detect URL in message
if "notebooklm.google.com" in user_message:
    url = extract_url(user_message)

    # 2. Check if in library
    notebooks = run("notebook_manager.py list")

    if url not in notebooks:
        # 3. ASK USER FOR METADATA (CRITICAL!)
        name = ask_user("What should I call this notebook?")
        description = ask_user("What does this notebook contain?")
        topics = ask_user("What topics does it cover?")

        # 4. Add with user-provided info
        run(f"notebook_manager.py add --url {url} --name '{name}' --description '{description}' --topics '{topics}'")

    # 5. Use the notebook
    answer = run(f"ask_question.py --question '{user_question}'")
```

### Workflow 2: Research Task

```python
# 1. Understand task
task = "Implement feature X"

# 2. Formulate comprehensive questions
questions = [
    "Complete implementation guide for X",
    "Error handling for X",
    "Performance considerations for X"
]

# 3. Query with follow-ups
for q in questions:
    answer = run(f"ask_question.py --question '{q}'")

    # Check if follow-up needed
    if "Is that ALL you need" in answer:
        # Ask more specific question
        follow_up = run(f"ask_question.py --question 'Specific detail about {q}'")

# 4. Synthesize and implement
```

## Tips and Tricks

1. **Always use run.py** - Prevents all venv issues
2. **Ask for metadata** - Never guess notebook contents
3. **Use verbose questions** - Include all context
4. **Follow up automatically** - When you see the prompt
5. **Monitor rate limits** - 50 queries per day
6. **Batch operations** - Group related queries
7. **Export important answers** - Save locally
8. **Version control notebooks** - Track changes
9. **Test auth regularly** - Before important tasks
10. **Document everything** - Keep notes on notebooks

## Quick Reference

```bash
# Always use run.py!
python scripts/run.py [script].py [args]

# Common operations
run.py auth_manager.py status          # Check auth
run.py auth_manager.py setup           # Login (browser visible!)
run.py notebook_manager.py list        # List notebooks
run.py notebook_manager.py add ...     # Add (ask user for metadata!)
run.py ask_question.py --question ...  # Query
run.py cleanup_manager.py ...          # Clean up
```

**Remember:** When in doubt, use run.py and ask the user for notebook details!
