---
title: "Modern Python"
description: "Configures Python projects with modern tooling (uv, ruff, ty). Use when creating projects, writing standalone scripts, or migrating from pip/Poetry/mypy/black."
category: "writing"
source: "community"
author: "Community"
tags: ["modern", "python"]
date: 2026-03-20
---

# Modern Python

Guide for modern Python tooling and best practices, based on [trailofbits/cookiecutter-python](https://github.com/trailofbits/cookiecutter-python).

## When to Use This Skill

- Creating a new Python project or package
- Setting up `pyproject.toml` configuration
- Configuring development tools (linting, formatting, testing)
- Writing Python scripts with external dependencies
- Migrating from legacy tools (when user requests it)

## When NOT to Use This Skill

- **User wants to keep legacy tooling**: Respect existing workflows if explicitly requested
- **Python < 3.11 required**: These tools target modern Python
- **Non-Python projects**: Mixed codebases where Python isn't primary

## Anti-Patterns to Avoid

| Avoid | Use Instead |
|-------|-------------|
| `[tool.ty]` python-version | `[tool.ty.environment]` python-version |
| `uv pip install` | `uv add` and `uv sync` |
| Editing pyproject.toml manually to add deps | `uv add <pkg>` / `uv remove <pkg>` |
| `hatchling` build backend | `uv_build` (simpler, sufficient for most cases) |
| Poetry | uv (faster, simpler, better ecosystem integration) |
| requirements.txt | PEP 723 for scripts, pyproject.toml for projects |
| mypy / pyright | ty (faster, from Astral team) |
| `[project.optional-dependencies]` for dev tools | `[dependency-groups]` (PEP 735) |
| Manual virtualenv activation (`source .venv/bin/activate`) | `uv run <cmd>` |
| pre-commit | prek (faster, no Python runtime needed) |

**Key principles:**
- Always use `uv add` and `uv remove` to manage dependencies
- Never manually activate or manage virtual environments—use `uv run` for all commands
- Use `[dependency-groups]` for dev/test/docs dependencies, not `[project.optional-dependencies]`

## Decision Tree

```
What are you doing?
│
├─ Single-file script with dependencies?
│   └─ Use PEP 723 inline metadata (./references/pep723-scripts.md)
│
├─ New multi-file project (not distributed)?
│   └─ Minimal uv setup (see Quick Start below)
│
├─ New reusable package/library?
│   └─ Full project setup (see Full Setup below)
│
└─ Migrating existing project?
    └─ See Migration Guide below
```

## Tool Overview

| Tool | Purpose | Replaces |
|------|---------|----------|
| **uv** | Package/dependency management | pip, virtualenv, pip-tools, pipx, pyenv |
| **ruff** | Linting AND formatting | flake8, black, isort, pyupgrade, pydocstyle |
| **ty** | Type checking | mypy, pyright (faster alternative) |
| **pytest** | Testing with coverage | unittest |
| **prek** | Pre-commit hooks ([setup](./references/prek.md)) | pre-commit (faster, Rust-native) |

### Security Tools

| Tool | Purpose | When It Runs |
|------|---------|--------------|
| **shellcheck** | Shell script linting | pre-commit |
| **detect-secrets** | Secret detection | pre-commit |
| **actionlint** | Workflow syntax validation | pre-commit, CI |
| **zizmor** | Workflow security audit | pre-commit, CI |
| **pip-audit** | Dependency vulnerability scanning | CI, manual |
| **Dependabot** | Automated dependency updates | scheduled |

See [security-setup.md](./references/security-setup.md) for configuration and usage.

## Quick Start: Minimal Project

For simple multi-file projects not intended for distribution:

```bash
# Create project with uv
uv init myproject
cd myproject

# Add dependencies
uv add requests rich

# Add dev dependencies
uv add --group dev pytest ruff ty

# Run code
uv run python src/myproject/main.py

# Run tools
uv run pytest
uv run ruff check .
```

## Full Project Setup
If starting from scratch, ask the user if they prefer to use the Trail of Bits cookiecutter template to bootstrap a complete project with already preconfigured tooling.

```bash
uvx cookiecutter gh:trailofbits/cookiecutter-python
```

### 1. Create Project Structure

```bash
uv init --package myproject
cd myproject
```

This creates:
```
myproject/
├── pyproject.toml
├── README.md
├── src/
│   └── myproject/
│       └── __init__.py
└── .python-version
```

### 2. Configure pyproject.toml

See [pyproject.md](./references/pyproject.md) for complete configuration reference.

Key sections:
```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [{include-group = "lint"}, {include-group = "test"}, {include-group = "audit"}]
lint = ["ruff", "ty"]
test = ["pytest", "pytest-cov"]
audit = ["pip-audit"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["ALL"]
ignore = ["D", "COM812", "ISC001"]

[tool.pytest]
addopts = ["--cov=myproject", "--cov-fail-under=80"]

[tool.ty.terminal]
error-on-warning = true

[tool.ty.environment]
python-version = "3.11"

[tool.ty.rules]
# Strict from day 1 for new projects
possibly-unresolved-reference = "error"
unused-ignore-comment = "warn"
```

### 3. Install Dependencies

```bash
# Install all dependency groups
uv sync --all-groups

# Or install specific groups
uv sync --group dev
```

### 4. Add Makefile

```makefile
.PHONY: dev lint format test build

dev:
	uv sync --all-groups

lint:
	uv run ruff format --check && uv run ruff check && uv run ty check src/

format:
	uv run ruff format .

test:
	uv run pytest

build:
	uv build
```

## Migration Guide

When a user requests migration from legacy tooling:

### From requirements.txt + pip

First, determine the nature of the code:

**For standalone scripts**: Convert to PEP 723 inline metadata (see [pep723-scripts.md](./references/pep723-scripts.md))

**For projects**:
```bash
# Initialize uv in existing project
uv init --bare

# Add dependencies using uv (not by editing pyproject.toml)
uv add requests rich  # add each package

# Or import from requirements.txt (review each package before adding)
# Note: Complex version specifiers may need manual handling
grep -v '^#' requirements.txt | grep -v '^-' | grep -v '^\s*$' | while read -r pkg; do
    uv add "$pkg" || echo "Failed to add: $pkg"
done

uv sync
```

Then:
1. Delete `requirements.txt`, `requirements-dev.txt`
2. Delete virtual environment (`venv/`, `.venv/`)
3. Add `uv.lock` to version control

### From setup.py / setup.cfg

1. Run `uv init --bare` to create pyproject.toml
2. Use `uv add` to add each dependency from `install_requires`
3. Use `uv add --group dev` for dev dependencies
4. Copy non-dependency metadata (name, version, description, etc.) to `[project]`
5. Delete `setup.py`, `setup.cfg`, `MANIFEST.in`

### From flake8 + black + isort

1. Remove flake8, black, isort via `uv remove`
2. Delete `.flake8`, `pyproject.toml [tool.black]`, `[tool.isort]` configs
3. Add ruff: `uv add --group dev ruff`
4. Add ruff configuration (see [ruff-config.md](./references/ruff-config.md))
5. Run `uv run ruff check --fix .` to apply fixes
6. Run `uv run ruff format .` to format

### From mypy / pyright

1. Remove mypy/pyright via `uv remove`
2. Delete `mypy.ini`, `pyrightconfig.json`, or `[tool.mypy]`/`[tool.pyright]` sections
3. Add ty: `uv add --group dev ty`
4. Run `uv run ty check src/`

## Quick Reference: uv Commands

| Command | Description |
|---------|-------------|
| `uv init` | Create new project |
| `uv init --package` | Create distributable package |
| `uv add <pkg>` | Add dependency |
| `uv add --group dev <pkg>` | Add to dependency group |
| `uv remove <pkg>` | Remove dependency |
| `uv sync` | Install dependencies |
| `uv sync --all-groups` | Install all dependency groups |
| `uv run <cmd>` | Run command in venv |
| `uv run --with <pkg> <cmd>` | Run with temporary dependency |
| `uv build` | Build package |
| `uv publish` | Publish to PyPI |

### Ad-hoc Dependencies with `--with`

Use `uv run --with` for one-off commands that need packages not in your project:

```bash
# Run Python with a temporary package
uv run --with requests python -c "import requests; print(requests.get('https://httpbin.org/ip').json())"

# Run a module with temporary deps
uv run --with rich python -m rich.progress

# Multiple packages
uv run --with requests --with rich python script.py

# Combine with project deps (adds to existing venv)
uv run --with httpx pytest  # project deps + httpx
```

**When to use `--with` vs `uv add`:**
- `uv add`: Package is a project dependency (goes in pyproject.toml/uv.lock)
- `--with`: One-off usage, testing, or scripts outside a project context

See [uv-commands.md](./references/uv-commands.md) for complete reference.

## Quick Reference: Dependency Groups

```toml
[dependency-groups]
dev = ["ruff", "ty"]
test = ["pytest", "pytest-cov", "hypothesis"]
docs = ["sphinx", "myst-parser"]
```

Install with: `uv sync --group dev --group test`

## Best Practices Checklist

- [ ] Use `src/` layout for packages
- [ ] Set `requires-python = ">=3.11"`
- [ ] Configure ruff with `select = ["ALL"]` and explicit ignores
- [ ] Use ty for type checking
- [ ] Enforce test coverage minimum (80%+)
- [ ] Use dependency groups instead of extras for dev tools
- [ ] Add `uv.lock` to version control
- [ ] Use PEP 723 for standalone scripts

## Read Next

- [migration-checklist.md](./references/migration-checklist.md) - Step-by-step migration cleanup
- [pyproject.md](./references/pyproject.md) - Complete pyproject.toml reference
- [uv-commands.md](./references/uv-commands.md) - uv command reference
- [ruff-config.md](./references/ruff-config.md) - Ruff linting/formatting configuration
- [testing.md](./references/testing.md) - pytest and coverage setup
- [pep723-scripts.md](./references/pep723-scripts.md) - PEP 723 inline script metadata
- [prek.md](./references/prek.md) - Fast pre-commit hooks with prek
- [security-setup.md](./references/security-setup.md) - Security hooks and dependency scanning
- [dependabot.md](./references/dependabot.md) - Automated dependency updates

---

## Reference: Dependabot

# Dependabot: Automated Dependency Updates

[Dependabot](https://docs.github.com/en/code-security/dependabot) automatically creates pull requests to keep your dependencies up to date. GitHub hosts it natively—no external service required.

## Why Use Dependabot?

- **Security**: Automatically patches known vulnerabilities
- **Freshness**: Keeps dependencies current without manual tracking
- **Visibility**: PRs show changelogs and compatibility notes

## Configuration

Copy [templates/dependabot.yml](../templates/dependabot.yml) to `.github/dependabot.yml`.

The template includes:
- Weekly update schedule for pip and GitHub Actions
- 7-day cooldown for supply chain protection
- Grouping to reduce PR noise

## Supply Chain Protection

The `cooldown.default-days: 7` setting delays updates for newly published versions. This provides time for the community to detect compromised packages before they reach your project.

**Why this matters:**
- Attackers sometimes publish malicious versions of legitimate packages
- A 7-day delay allows time for detection and removal
- Combined with weekly schedules, this balances security with freshness

## Common Options

| Option | Description |
|--------|-------------|
| `interval` | `daily`, `weekly`, or `monthly` |
| `cooldown.default-days` | Days to wait before updating new releases |
| `ignore` | Skip specific dependencies or versions |
| `groups` | Group related updates into single PRs |
| `reviewers` | Auto-assign reviewers to PRs |

## See Also

- [GitHub Dependabot docs](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [security-setup.md](./security-setup.md) - Security tooling overview
- [prek.md](./prek.md) - Pre-commit hooks (complementary tool)

---

## Reference: Migration Checklist

# Migration Checklist

Comprehensive checklist for migrating Python projects to modern tooling.

## Before Migration

- [ ] **Determine layout**: `src/` or flat? Configure `[tool.uv.build-backend]` if flat
- [ ] **Decide uv.lock strategy**: app (commit) vs library (.gitignore)
- [ ] **Backup current state**: Create a branch or tag before starting

## Cleanup Old Artifacts

Find and remove legacy linter comments:

```bash
# Find files with old linter pragmas
rg "# pylint:|# noqa:|# type: ignore" --files-with-matches

# Find missing __init__.py files
uv run ruff check --select=INP001 .
```

Remove these files after migration:
- [ ] `requirements.txt`, `requirements-dev.txt`
- [ ] `setup.py`, `setup.cfg`, `MANIFEST.in`
- [ ] `.flake8`, `mypy.ini`, `pyrightconfig.json`
- [ ] `tox.ini` (if not needed)
- [ ] `Pipfile`, `Pipfile.lock`
- [ ] Old virtual environments (`venv/`, `.venv/`)

## .gitignore Updates

Add these entries:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/

# Tools
.ruff_cache/
.ty/

# uv (for libraries only - apps should commit uv.lock)
# uv.lock
```

## pyproject.toml Sections to Remove

- [ ] `[tool.black]`
- [ ] `[tool.isort]`
- [ ] `[tool.mypy]`
- [ ] `[tool.pyright]`
- [ ] `[tool.pylint]`
- [ ] `[tool.flake8]` (if present)

## Post-Migration Easy Wins

Run these to modernize code automatically:

```bash
# Pyupgrade modernization (typing, syntax)
uv run ruff check --select=UP --fix .

# Unnecessary variable assignments before return
uv run ruff check --select=RET504 --fix .

# Simplifications (conditionals, comprehensions)
uv run ruff check --select=SIM --fix .

# Remove commented-out code
uv run ruff check --select=ERA --fix .
```

## CI Cleanup

- [ ] Remove scheduled CI triggers (activity without progress is theater)
- [ ] Update CI to use `uv sync` and `uv run`
- [ ] Pin GitHub Actions to SHA hashes
- [ ] Set up security tooling (see [security-setup.md](./security-setup.md))

## Gradual ty Adoption

For legacy codebases with many type errors, start lenient:

```toml
[tool.ty.terminal]
error-on-warning = true

[tool.ty.environment]
python-version = "3.11"

[tool.ty.rules]
# Start with these ignored for legacy codebases
possibly-missing-attribute = "ignore"
unresolved-import = "ignore"
invalid-argument-type = "ignore"
not-subscriptable = "ignore"
unresolved-attribute = "ignore"
```

Remove rules as you fix errors. Track progress:

```bash
# Count remaining issues
uv run ty check src/ 2>&1 | grep -c "error"
```

## Supply Chain Security

- [ ] Add pip-audit to dependency groups
- [ ] Configure Dependabot with 7-day cooldown
- [ ] Pin exact versions in production (`==` not `>=`)

See [security-setup.md](./security-setup.md) for pip-audit and Dependabot configuration.

## Verification

After migration, verify everything works:

```bash
# Install all dependencies
uv sync --all-groups

# Run linting
uv run ruff check .
uv run ruff format --check .

# Run type checking
uv run ty check src/

# Run tests
uv run pytest

# Security audit
uv run pip-audit

# Build package (if distributable)
uv build
```

---

## Reference: Pep723 Scripts

# PEP 723: Inline Script Metadata

PEP 723 allows embedding dependency metadata directly in Python scripts, eliminating the need for separate `requirements.txt` or `pyproject.toml` files for simple scripts.

## When to Use PEP 723

**Use for:**
- Single-file scripts with external dependencies
- Quick automation scripts
- Utility scripts shared between projects
- Scripts that need to be self-contained

**Don't use for:**
- Multi-file projects (use `pyproject.toml`)
- Reusable packages/libraries
- Projects requiring complex configuration

## Basic Syntax

The metadata block uses TOML format embedded in a special comment:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "rich",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.example.com/data")
print(response.json())
```

## Running Scripts

```bash
# With uv (recommended)
uv run script.py

# Script handles its own dependencies automatically
./script.py  # If shebang is set
```

## Metadata Fields

### Required Python Version

```python
# /// script
# requires-python = ">=3.11"
# ///
```

### Dependencies

```python
# /// script
# dependencies = [
#     "requests",
#     "click",
#     "rich",
# ]
# ///
```

### Private Package Index

```python
# /// script
# dependencies = ["httpx"]
#
# [tool.uv]
# extra-index-url = ["https://pypi.company.com/simple/"]
# ///
```

## Complete Example

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "rich",
#     "typer",
# ]
# ///

"""Fetch and display API data with nice formatting."""

import httpx
import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command()
def fetch(url: str, format: str = "table"):
    """Fetch data from URL and display it."""
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()

    if format == "table" and isinstance(data, list):
        table = Table()
        if data:
            for key in data[0].keys():
                table.add_column(key)
            for item in data:
                table.add_row(*[str(v) for v in item.values()])
        console.print(table)
    else:
        console.print_json(data=data)


if __name__ == "__main__":
    app()
```

## Creating Scripts with uv

```bash
# Create new script with metadata
uv init --script myscript.py

# Add dependency to existing script
uv add --script myscript.py requests

# Remove dependency from script
uv remove --script myscript.py requests
```

## Shebang Options

### Basic (requires uv in PATH)

```python
#!/usr/bin/env -S uv run --script
```

### With specific Python version

```python
#!/usr/bin/env -S uv run --python 3.12 --script
```

### Quiet mode (suppress uv output)

```python
#!/usr/bin/env -S uv run --quiet --script
```

## Examples by Use Case

### Data Processing Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "openpyxl"]
# ///

import pandas as pd
import sys

df = pd.read_excel(sys.argv[1])
print(df.describe())
```

### Web Scraping Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "beautifulsoup4", "lxml"]
# ///

import httpx
from bs4 import BeautifulSoup

response = httpx.get("https://example.com")
soup = BeautifulSoup(response.text, "lxml")
print(soup.title.string)
```

### CLI Tool Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer", "rich"]
# ///

import typer
from rich import print

app = typer.Typer()

@app.command()
def greet(name: str):
    print(f"[green]Hello, {name}![/green]")

if __name__ == "__main__":
    app()
```

### Async Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///

import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        urls = ["https://api1.example.com", "https://api2.example.com"]
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        for r in responses:
            print(r.status_code)

asyncio.run(main())
```

## Best Practices

1. **Always specify `requires-python`** - Ensures compatibility
2. **Pin major versions for Python** - Use `>=3.11` not `==3.11`
3. **Omit version constraints for dependencies** - Use `uv add --script` to add dependencies; let uv select versions
4. **Keep scripts focused** - One script, one purpose
5. **Add docstring** - Document what the script does
6. **Use type hints** - Improves readability and catches errors

## Limitations

- No support for dependency groups
- No support for editable installs
- No support for local dependencies (use relative imports)
- No lockfile (versions may vary between runs)

For projects needing these features, use a full `pyproject.toml` setup instead.

---

## Reference: Prek

# prek: Fast Pre-commit Hooks

[prek](https://github.com/j178/prek) is a fast, Rust-native drop-in replacement for pre-commit. It uses the same `.pre-commit-config.yaml` format and is fully compatible with existing configurations.

## Why prek over pre-commit?

| Feature | prek | pre-commit |
|---------|------|------------|
| Speed | ~7x faster hook installation | Slower |
| Dependencies | Single binary, no runtime needed | Requires Python |
| Disk usage | Shared toolchains between hooks | Isolated environments |
| Parallelism | Parallel repo cloning and hook execution | Sequential |
| Python management | Uses uv automatically | Manual Python setup |
| Monorepo support | Built-in workspace mode | Not supported |

**Already using prek:** CPython, Apache Airflow, FastAPI, Ruff, Home Assistant, and [many more](https://github.com/j178/prek#who-is-using-prek).

## Installation

See [security-setup.md](./security-setup.md#tool-installation) for installation options.

## Quick Start

### For Existing pre-commit Users

prek is fully compatible with `.pre-commit-config.yaml`. Just replace commands:

```bash
# Instead of: pre-commit install
prek install

# Instead of: pre-commit run --all-files
prek run --all-files

# Instead of: pre-commit autoupdate
prek auto-update
```

### New Setup

1. Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: <latest>  # https://github.com/astral-sh/ruff-pre-commit/releases
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

2. Install and run:

```bash
# Install git hooks
prek install

# Run manually on all files
prek run --all-files

# Run specific hook
prek run ruff
```

## Configuration

For a complete, copy-paste-ready configuration, see [templates/pre-commit-config.yaml](../templates/pre-commit-config.yaml).

### Recommended `.pre-commit-config.yaml`

> **Note:** Versions shown as `<latest>` are placeholders. Always check the linked releases for current stable versions before use.

```yaml
# See https://pre-commit.com for more information
default_language_version:
  python: python3.12

repos:
  # Ruff - linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: <latest>  # https://github.com/astral-sh/ruff-pre-commit/releases
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # General file checks (prek builtin - faster, no external deps)
  - repo: builtin
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict

  # Security hooks - see security-setup.md for detailed guidance
  # Shell script linting
  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: <latest>  # https://github.com/koalaman/shellcheck-precommit/tags
    hooks:
      - id: shellcheck
        args: [--severity=error]

  # Secret detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: <latest>  # https://github.com/Yelp/detect-secrets/releases
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]

  # GitHub Actions linting
  - repo: https://github.com/rhysd/actionlint
    rev: <latest>  # https://github.com/rhysd/actionlint/releases
    hooks:
      - id: actionlint

  # GitHub Actions security audit
  - repo: https://github.com/zizmorcore/zizmor-pre-commit
    rev: <latest>  # https://github.com/zizmorcore/zizmor-pre-commit/releases
    hooks:
      - id: zizmor
        args: [--persona=regular, --min-severity=medium, --min-confidence=medium]
```

See [security-setup.md](./security-setup.md) for detailed guidance on each security hook.

### Using Built-in Hooks

prek includes Rust-native implementations of common hooks for extra speed:

```yaml
repos:
  - repo: builtin
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
```

## Commands

| Command | Description |
|---------|-------------|
| `prek install` | Install git hooks |
| `prek uninstall` | Remove git hooks |
| `prek run` | Run hooks on staged files |
| `prek run --all-files` | Run on all files |
| `prek run --last-commit` | Run on last commit's files |
| `prek run HOOK [HOOK...]` | Run specific hook(s) |
| `prek run -d src/` | Run on files in directory |
| `prek auto-update` | Update hook versions |
| `prek list` | List configured hooks |
| `prek clean` | Remove cached environments |

## CI Configuration

### GitHub Actions

```yaml
name: Pre-commit
on: [push, pull_request]

jobs:
  prek:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>  # <latest> https://github.com/actions/checkout/releases
      - uses: j178/prek-action@<sha>  # <latest> https://github.com/j178/prek-action/releases
```

Or manually:

```yaml
- name: Install prek
  run: uv tool install prek

- name: Run hooks
  run: prek run --all-files
```

## Makefile Integration

```makefile
.PHONY: hooks hooks-install

hooks:
	prek run --all-files

hooks-install:
	prek install
```

## Migration from pre-commit

1. Install prek: `uv tool install prek`
2. Remove pre-commit: `pip uninstall pre-commit` or `uv tool uninstall pre-commit`
3. Re-install hooks: `prek install`
4. (Optional) Clean old environments: `rm -rf ~/.cache/pre-commit`

Your existing `.pre-commit-config.yaml` works unchanged.

## Best Practices

1. **Use `prek run --all-files` in CI** - Ensures all files are checked, not just changed ones
2. **Pin hook versions** - Use specific `rev` values, not branches
3. **Use `--cooldown-days` for auto-update** - Mitigates supply chain attacks: `prek auto-update --cooldown-days 7`
4. **Prefer built-in hooks** - Use `repo: builtin` for common checks (faster, offline)
5. **Run hooks before commit** - `prek install` sets this up automatically
6. **Initialize detect-secrets baseline** - Run `detect-secrets scan > .secrets.baseline` before first commit

---

## Reference: Pyproject

# pyproject.toml Configuration Reference

Complete reference for configuring `pyproject.toml` for modern Python projects.

**Important**: Always use `uv add` and `uv remove` to manage dependencies. Do not edit the `dependencies` or `dependency-groups` sections directly.

## Complete Example

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "requests",
    "rich",
]

[project.optional-dependencies]
# Use for optional features users can install
cli = ["typer"]

[project.scripts]
myproject = "myproject.cli:main"

[project.urls]
Homepage = "https://github.com/org/myproject"
Documentation = "https://myproject.readthedocs.io"
Repository = "https://github.com/org/myproject"

[build-system]
requires = ["uv_build>=0.9,<1"]  # Use latest 0.x; check https://pypi.org/project/uv-build/
build-backend = "uv_build"

[dependency-groups]
dev = ["ruff", "ty"]
test = ["pytest", "pytest-cov", "hypothesis"]
docs = ["sphinx", "myst-parser"]

[tool.uv]
default-groups = ["dev", "test"]

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src"]

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D",        # pydocstyle (enable selectively)
    "COM812",   # trailing comma (conflicts with formatter)
    "ISC001",   # implicit string concat (conflicts with formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",     # assert allowed in tests
    "PLR2004",  # magic values allowed in tests
    "ANN",      # annotations optional in tests
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

[tool.pytest]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "--cov=myproject",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]

[tool.coverage.run]
branch = true
source = ["src/myproject"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

## Section Reference

### [project]

Core project metadata following PEP 621.

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Package name (lowercase, hyphens) |
| `version` | Yes | Semantic version |
| `description` | No | One-line description |
| `readme` | No | Path to README file |
| `license` | No | SPDX license identifier |
| `requires-python` | Recommended | Python version constraint |
| `authors` | No | List of author dicts |
| `dependencies` | No | Runtime dependencies |

### [project.optional-dependencies]

**Rarely needed.** Only use for optional *runtime* features that end users install:

```toml
[project.optional-dependencies]
# User installs with: uv add myproject[postgres]
postgres = ["psycopg2"]
```

**Do NOT use for dev tools**—use `[dependency-groups]` instead.

### [project.scripts]

Console entry points:

```toml
[project.scripts]
myproject = "myproject.cli:main"
myproject-serve = "myproject.server:run"
```

### [build-system]

Build backend configuration. Use `uv_build` for most projects:

```toml
[build-system]
requires = ["uv_build>=0.9,<1"]  # Use latest 0.x; check https://pypi.org/project/uv-build/
build-backend = "uv_build"
```

`uv_build` is simpler and sufficient for most use cases. Use static versioning in `[project] version` rather than VCS-aware dynamic versioning.

For flat layout (no `src/` directory), configure the module root:

```toml
[tool.uv.build-backend]
module-root = ""
```

> **Note:** These tools evolve rapidly. Prefer `>=X.Y,<X+1` constraints to automatically get newer releases within the same major version.

### [dependency-groups]

Development dependencies (PEP 735). Unlike optional-dependencies, these are NOT installed by users:

```toml
[dependency-groups]
dev = [{include-group = "lint"}, {include-group = "test"}, {include-group = "audit"}]
lint = ["ruff", "ty"]
test = ["pytest", "pytest-cov"]
audit = ["pip-audit"]
docs = ["sphinx", "myst-parser"]
```

Install with: `uv sync --group dev --group test`

### [tool.uv]

uv-specific configuration:

```toml
[tool.uv]
# Default groups to install with `uv sync`
default-groups = ["dev", "test"]

# Python version management
python-preference = "managed"
```

## Version Specifiers

| Specifier | Meaning |
|-----------|---------|
| `>=1.0` | At least version 1.0 |
| `>=1.0,<2.0` | Version 1.x only |
| `~=1.4` | Compatible release (>=1.4, <2.0) |
| `==1.4.*` | Any 1.4.x version |

## uv.lock Handling

| Project Type | uv.lock in Git? | Why |
|--------------|-----------------|-----|
| Application | ✅ Commit | Reproducible deploys |
| Library | ❌ .gitignore | Users resolve their own deps |

## Common Patterns

### Library Package

```toml
[project]
dependencies = []  # Minimal runtime deps

[project.optional-dependencies]
# Optional runtime features (user installs with mylib[async])
async = ["httpx"]

[dependency-groups]
dev = ["ruff", "ty"]
test = ["pytest", "pytest-cov"]
```

### Application Package

```toml
[project]
dependencies = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
]

[project.scripts]
myapp = "myapp.main:run"

[dependency-groups]
dev = ["ruff", "ty", "pytest"]
```

### CLI Tool

```toml
[project]
dependencies = [
    "typer",
    "rich",
]

[project.scripts]
mytool = "mytool.cli:app"

[dependency-groups]
dev = ["ruff", "ty", "pytest"]
```

---

## Reference: Ruff Config

# Ruff Configuration Reference

Ruff is an extremely fast Python linter and formatter written in Rust. It replaces flake8, black, isort, pyupgrade, pydocstyle, and many other tools.

## Basic Setup

Add to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src"]

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D",        # pydocstyle
    "COM812",   # trailing comma (formatter conflict)
    "ISC001",   # string concat (formatter conflict)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true
```

## Running Ruff

```bash
# Lint
uv run ruff check .
uv run ruff check --fix .        # Auto-fix
uv run ruff check --fix --unsafe-fixes .  # Including unsafe fixes

# Format
uv run ruff format .
uv run ruff format --check .     # Check only
uv run ruff format --diff .      # Show diff
```

## Rule Categories

Using `select = ["ALL"]` enables all rules. Common categories:

| Code | Category | Description |
|------|----------|-------------|
| `E`, `W` | pycodestyle | Style errors and warnings |
| `F` | Pyflakes | Logical errors |
| `I` | isort | Import sorting |
| `N` | pep8-naming | Naming conventions |
| `D` | pydocstyle | Docstring conventions |
| `UP` | pyupgrade | Python upgrade suggestions |
| `B` | flake8-bugbear | Bug detection |
| `S` | flake8-bandit | Security issues |
| `A` | flake8-builtins | Built-in shadowing |
| `C4` | flake8-comprehensions | Comprehension improvements |
| `DTZ` | flake8-datetimez | Timezone-aware datetime |
| `T10` | flake8-debugger | Debugger statements |
| `T20` | flake8-print | Print statements |
| `PT` | flake8-pytest-style | Pytest style |
| `Q` | flake8-quotes | Quote consistency |
| `SIM` | flake8-simplify | Simplification suggestions |
| `TID` | flake8-tidy-imports | Import hygiene |
| `ARG` | flake8-unused-arguments | Unused arguments |
| `ERA` | eradicate | Commented-out code |
| `PL` | Pylint | Pylint rules |
| `RUF` | Ruff-specific | Ruff's own rules |
| `ANN` | flake8-annotations | Type annotation checks |

## Recommended Ignores

### Always Ignore (Formatter Conflicts)

```toml
ignore = [
    "COM812",   # missing-trailing-comma
    "ISC001",   # single-line-implicit-string-concatenation
]
```

### Common Ignores

```toml
ignore = [
    "D",        # Docstrings (enable selectively)
    "ANN401",   # Dynamically typed Any
    "TD002",    # Missing TODO author
    "TD003",    # Missing TODO link
    "FIX002",   # Line contains TODO
]
```

## Per-File Ignores

```toml
[tool.ruff.lint.per-file-ignores]
# Tests
"tests/**/*.py" = [
    "S101",     # assert usage
    "PLR2004",  # magic values
    "ANN",      # type annotations
    "D",        # docstrings
]

# Scripts
"scripts/**/*.py" = [
    "T20",      # print statements
    "INP001",   # implicit namespace package
]

# __init__.py
"__init__.py" = [
    "F401",     # unused imports (re-exports)
]

# Migrations
"**/migrations/*.py" = [
    "ALL",      # ignore all
]
```

## Import Sorting (isort)

```toml
[tool.ruff.lint.isort]
force-single-line = false
known-first-party = ["myproject"]
required-imports = ["from __future__ import annotations"]
section-order = [
    "future",
    "standard-library",
    "third-party",
    "first-party",
    "local-folder",
]
```

## Docstring Style (pydocstyle)

If enabling docstring checks:

```toml
[tool.ruff.lint]
select = ["D"]
ignore = [
    "D100",     # Missing module docstring
    "D104",     # Missing public package docstring
    "D203",     # 1 blank line before class docstring (conflicts D211)
    "D213",     # Multi-line summary second line (conflicts D212)
]

[tool.ruff.lint.pydocstyle]
convention = "google"  # or "numpy", "pep257"
```

## Formatter Configuration

```toml
[tool.ruff.format]
quote-style = "double"           # or "single"
indent-style = "space"           # or "tab"
skip-magic-trailing-comma = false
line-ending = "auto"             # or "lf", "crlf"
docstring-code-format = true
docstring-code-line-length = 80
```

## Type Checking

Ruff does NOT do type checking. Use **ty** (from Astral, the same team behind ruff and uv):

```bash
# Add ty to dev dependencies
uv add --group dev ty

# Run type checking
uv run ty check src/
```

ty is significantly faster than mypy or pyright and integrates well with the modern Python toolchain.

## CI Configuration

```yaml
# GitHub Actions
- name: Lint
  run: uv run ruff check --output-format=github .

- name: Format check
  run: uv run ruff format --check .
```

## Migration from Other Tools

### From flake8

Ruff covers most flake8 plugins. Remove:
- flake8
- flake8-* plugins
- .flake8 config file

### From black

Remove black and use `ruff format`. Remove:
- black
- [tool.black] config

### From isort

Ruff includes isort. Remove:
- isort
- [tool.isort] config

Use `[tool.ruff.lint.isort]` for isort settings.

## Code Modernization

Run pyupgrade rules to modernize syntax to your target Python version:

```bash
uv run ruff check --select=UP --fix .  # Auto-fix upgrades
uv run ruff check --select=UP .        # Preview only
```

Common modernizations include:
- `typing.Optional[X]` → `X | None`
- `typing.List[X]` → `list[X]`
- `super(ClassName, self)` → `super()`
- Format strings and other syntax upgrades

## Line Length Migration

If migrating from 120 to 100 char lines, expect manual fixes.
For less churn during initial migration, keep existing:

```toml
line-length = 120  # Match existing; tighten later
```

---

## Reference: Security Setup

# Security Setup

Security tooling for Python projects: pre-commit hooks, CI auditing, and dependency scanning.

## Tool Installation

Install these tools before running the quick setup commands below.

### prek (pre-commit runner)

```bash
# Homebrew (recommended)
brew install prek

# Cargo
cargo install prek

# Standalone installer
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/j178/prek/releases/latest/download/prek-installer.sh | sh
```

### Security tools

Pre-commit hooks auto-install tools when run via prek. For manual CLI usage:

```bash
# Homebrew (macOS/Linux)
brew install actionlint shellcheck

# Python tools via uv
uv tool install detect-secrets
uv tool install zizmor
```

Alternative installation methods:

- **actionlint**: `go install github.com/rhysd/actionlint/cmd/actionlint@latest`
- **zizmor**: `cargo install zizmor`
- **detect-secrets**: `pipx install detect-secrets`

## Quick Setup

```bash
# 1. Install security hooks
prek install

# 2. Initialize secrets baseline
detect-secrets scan > .secrets.baseline

# 3. Audit existing workflows
actionlint .github/workflows/
zizmor .github/workflows/
```

See [templates/pre-commit-config.yaml](../templates/pre-commit-config.yaml) for a complete hook configuration.

## Tool Matrix

| Tool | Runs | Catches |
|------|------|---------|
| **shellcheck** | pre-commit | Shell script bugs, quoting issues |
| **detect-secrets** | pre-commit | Leaked API keys, passwords, tokens |
| **actionlint** | pre-commit, CI | Workflow syntax errors, invalid refs |
| **zizmor** | pre-commit, CI | Workflow security issues, excessive permissions |
| **pip-audit** | CI, manual | Known CVEs in dependencies |
| **Dependabot** | scheduled | Outdated dependencies with vulnerabilities |

## Pre-commit Hooks

These run locally before each commit via prek.

### shellcheck - Shell Script Linting

Catches common shell scripting errors: unquoted variables, undefined variables, deprecated syntax.

```yaml
# In .pre-commit-config.yaml
- repo: https://github.com/koalaman/shellcheck-precommit
  rev: <latest>  # https://github.com/koalaman/shellcheck-precommit/tags
  hooks:
    - id: shellcheck
      args: [--severity=error]  # Start strict, adjust if needed
```

Common findings:
- `SC2086`: Unquoted variable expansion (word splitting risk)
- `SC2046`: Unquoted command substitution
- `SC2155`: Declare and assign separately to avoid masking return values

### detect-secrets - Secret Detection

Prevents accidentally committing API keys, passwords, and tokens.

```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: <latest>  # https://github.com/Yelp/detect-secrets/releases
  hooks:
    - id: detect-secrets
      args: [--baseline, .secrets.baseline]
```

**First-time setup:**

```bash
# Generate baseline of existing "secrets" (false positives to ignore)
detect-secrets scan > .secrets.baseline

# Review the baseline - ensure no real secrets
cat .secrets.baseline

# Commit the baseline
git add .secrets.baseline
```

**When hook fails:**

```bash
# View the finding (non-interactive)
detect-secrets audit --report .secrets.baseline
```

If false positive: update baseline with `detect-secrets scan --update .secrets.baseline`
If real secret: remove from code and rotate the credential.

## CI Security

These run in GitHub Actions on every push/PR.

### actionlint - Workflow Syntax Validation

Catches syntax errors, invalid action references, and type mismatches before they fail in CI.

```yaml
- repo: https://github.com/rhysd/actionlint
  rev: <latest>  # https://github.com/rhysd/actionlint/releases
  hooks:
    - id: actionlint
```

Run manually:

```bash
actionlint .github/workflows/
```

Common findings:
- Invalid event triggers
- Undefined workflow inputs
- Shell syntax errors in `run:` blocks
- Invalid action version references

### zizmor - Workflow Security Audit

Finds security issues in GitHub Actions workflows: excessive permissions, injection risks, untrusted inputs.

```yaml
- repo: https://github.com/zizmorcore/zizmor-pre-commit
  rev: <latest>  # https://github.com/zizmorcore/zizmor-pre-commit/releases
  hooks:
    - id: zizmor
      args: [--persona=regular, --min-severity=medium, --min-confidence=medium]
```

Run manually:

```bash
zizmor .github/workflows/
```

**Fixing `excessive-permissions`:**

By default, workflows get `write` access to everything. Lock down with explicit permissions:

```yaml
# Read-only workflows (lint, test, audit)
permissions:
  contents: read

# Workflows that push or create releases
permissions:
  contents: write

# Workflows that comment on PRs
permissions:
  contents: read
  pull-requests: write
```

Common findings:
- `excessive-permissions`: No `permissions:` block
- `template-injection`: Using `${{ github.event.* }}` unsafely
- `unpinned-action`: Actions not pinned to SHA
- `dangerous-triggers`: `pull_request_target` with checkout

## Dependency Security

### pip-audit - Vulnerability Scanning

Checks installed packages against the Python Advisory Database (PyPA) for known CVEs.

**Setup:**

```toml
# pyproject.toml
[dependency-groups]
audit = ["pip-audit"]
```

**Usage:**

```bash
# Audit current environment
uv run pip-audit

# Audit without installing (faster for CI)
uv run pip-audit .

# Fix automatically (upgrades vulnerable packages)
uv run pip-audit --fix
```

**In CI:**

```yaml
- name: Security audit
  run: uv run pip-audit .
```

**When vulnerabilities found:**

1. Check if the CVE affects your usage (many are in unused code paths)
2. Update the package: `uv add <package>@latest`
3. If no fix available: evaluate risk, consider alternatives, or add to ignore list

### Dependabot - Automated Updates

Automatically creates PRs for outdated dependencies.

Copy [templates/dependabot.yml](../templates/dependabot.yml) to `.github/dependabot.yml`.

**How pip-audit and Dependabot work together:**

| Tool | Trigger | Scope |
|------|---------|-------|
| pip-audit | Every CI run | Known CVEs in current deps |
| Dependabot | Weekly schedule | All outdated deps, security + non-security |

- **pip-audit** catches: "You have a vulnerable version right now"
- **Dependabot** prevents: "You'll fall behind and accumulate vulnerabilities"

The 7-day cooldown protects against attackers publishing malicious updates and hoping for quick adoption before detection.

See [dependabot.md](./dependabot.md) for advanced configuration.

See [prek.md](./prek.md) for complete pre-commit hook configuration including security hooks.

---

## Reference: Testing

# Testing with pytest

Configuration and best practices for pytest with coverage enforcement.

## Setup

Add test dependencies:

```bash
uv add --group test pytest pytest-cov hypothesis
```

## pyproject.toml Configuration

```toml
[tool.pytest]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-ra",                      # Show summary of all test outcomes
    "--strict-markers",         # Error on unknown markers
    "--strict-config",          # Error on config issues
    "--cov=myproject",          # Coverage for package
    "--cov-report=term-missing", # Show missing lines
    "--cov-fail-under=80",      # Minimum coverage
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
filterwarnings = [
    "error",                    # Treat warnings as errors
    "ignore::DeprecationWarning:third_party.*",
]

[tool.coverage.run]
branch = true
source = ["src/myproject"]
omit = [
    "*/__main__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "@abstractmethod",
]
fail_under = 80
show_missing = true
```

## Project Structure

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_core.py
│   └── integration/
│       └── test_api.py
└── pyproject.toml
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific file
uv run pytest tests/test_core.py

# Run specific test
uv run pytest tests/test_core.py::test_function_name

# Run tests matching pattern
uv run pytest -k "test_parse"

# Run marked tests
uv run pytest -m "not slow"

# Stop on first failure
uv run pytest -x

# Run last failed
uv run pytest --lf
```

## Coverage Commands

```bash
# Run with coverage
uv run pytest --cov=myproject

# Generate HTML report
uv run pytest --cov=myproject --cov-report=html
open htmlcov/index.html

# Coverage without running tests (use existing data)
uv run coverage report
uv run coverage html
```

## Writing Tests

### Basic Test

```python
# tests/test_core.py
from myproject.core import add_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5

def test_add_negative():
    assert add_numbers(-1, 1) == 0
```

### Using Fixtures

```python
# tests/conftest.py
import pytest
from myproject.db import Database

@pytest.fixture
def db():
    """Provide a test database."""
    database = Database(":memory:")
    database.init()
    yield database
    database.close()

@pytest.fixture
def sample_data(db):
    """Populate database with sample data."""
    db.insert({"name": "test"})
    return db
```

```python
# tests/test_db.py
def test_query(sample_data):
    result = sample_data.query("test")
    assert result is not None
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("test", 4),
])
def test_string_length(input, expected):
    assert len(input) == expected
```

### Testing Exceptions

```python
import pytest
from myproject.core import divide

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

def test_divide_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(1, 0)
```

### Async Tests

```bash
uv add --group test pytest-asyncio
```

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data()
    assert result is not None
```

## Property-Based Testing with Hypothesis

```bash
uv add --group test hypothesis
```

```python
from hypothesis import given, strategies as st
from myproject.core import reverse_string

@given(st.text())
def test_reverse_is_reversible(s):
    assert reverse_string(reverse_string(s)) == s

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

## Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    # Long running test
    pass

@pytest.mark.integration
def test_api_call():
    # Requires external service
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass
```

## CI Configuration

```yaml
# GitHub Actions
- name: Checkout
  uses: actions/checkout@<sha>  # <latest> https://github.com/actions/checkout/releases

- name: Run tests
  run: |
    uv sync --group test
    uv run pytest --cov-report=xml

- name: Security audit
  run: |
    uv sync --group audit
    uv run pip-audit

- name: Upload coverage
  uses: codecov/codecov-action@<sha>  # <latest> https://github.com/codecov/codecov-action/releases
  with:
    files: ./coverage.xml
```

## Makefile Target

```makefile
.PHONY: test

test:
	uv run pytest

test-cov:
	uv run pytest --cov-report=html
	open htmlcov/index.html

test-fast:
	uv run pytest -x -q --no-cov
```

---

## Reference: Uv Commands

# uv Command Reference

`uv` is an extremely fast Python package and project manager written in Rust. It replaces pip, virtualenv, pip-tools, pipx, and pyenv.

**Key principle:** Always use `uv run` to execute commands. Never manually activate virtual environments.

## Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew
brew install uv

# pipx
pipx install uv
```

## Project Commands

### Initialize Projects

| Command | Description |
|---------|-------------|
| `uv init` | Create new project (application) |
| `uv init --package` | Create distributable package with src/ layout |
| `uv init --lib` | Create library package |
| `uv init --script file.py` | Create script with PEP 723 metadata |

### Dependency Management

| Command | Description |
|---------|-------------|
| `uv add <pkg>` | Add dependency to project |
| `uv add <pkg> --group dev` | Add to dependency group |
| `uv add <pkg> --optional feature` | Add to optional dependency |
| `uv remove <pkg>` | Remove dependency |
| `uv lock` | Update lock file without installing |

### Environment Management

uv manages virtual environments automatically. Do not manually create or activate venvs.

| Command | Description |
|---------|-------------|
| `uv sync` | Install dependencies (creates venv if needed) |
| `uv sync --all-groups` | Install all dependency groups |
| `uv sync --group dev` | Install specific group |
| `uv sync --frozen` | Install from lock file exactly |

### Running Code

| Command | Description |
|---------|-------------|
| `uv run <cmd>` | Run command in project venv |
| `uv run python script.py` | Run Python script |
| `uv run pytest` | Run pytest |
| `uv run --with pkg cmd` | Run with temporary dependency |

### Building & Publishing

| Command | Description |
|---------|-------------|
| `uv build` | Build wheel and sdist |
| `uv build --wheel` | Build wheel only |
| `uv build --sdist` | Build sdist only |
| `uv publish` | Publish to PyPI |
| `uv publish --token $TOKEN` | Publish with API token |

## Tool Commands

Run Python tools without installing globally:

```bash
# Run any tool
uv tool run ruff check .
uvx ruff check .  # shorthand

# Install tool globally
uv tool install ruff

# List installed tools
uv tool list

# Upgrade tool
uv tool upgrade ruff
```

## Python Version Management

```bash
# Install Python version
uv python install 3.12

# List available versions
uv python list

# Pin project to Python version
uv python pin 3.12

# Use specific version
uv run --python 3.11 pytest
```

## Script Commands (PEP 723)

```bash
# Create script with inline metadata
uv init --script myscript.py

# Add dependency to script
uv add --script myscript.py requests

# Run script (auto-installs deps)
uv run myscript.py
```

## Common Workflows

### New Application Project

```bash
uv init myapp
cd myapp
uv add fastapi uvicorn
uv add --group dev ruff pytest
uv sync --all-groups
uv run uvicorn myapp:app
```

### New Library Package

```bash
uv init --package mylib
cd mylib
uv add --group dev ruff pytest pytest-cov
uv add --group docs sphinx
uv sync --all-groups
uv run pytest
uv build
```

### Add Tool to Existing Project

```bash
cd existing-project
uv add --group dev ruff
uv run ruff check .
```

### One-off Script Execution

```bash
# Run script with dependencies (no project needed)
uv run --with requests --with rich script.py

# Or use PEP 723 inline metadata
uv run script_with_metadata.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `UV_CACHE_DIR` | Cache directory location |
| `UV_NO_CACHE` | Disable caching |
| `UV_PYTHON` | Default Python version |
| `UV_PROJECT` | Project directory path |
| `UV_PROJECT_ENVIRONMENT` | Custom venv directory (e.g., `.venv-dev`) |
| `UV_SYSTEM_PYTHON` | Use system Python |

## Container/Host Development

When developing on a host machine while also running in containers, you can use separate venvs to avoid rebuilding on each context switch:

```bash
# On host machine (add to shell profile or .envrc)
export UV_PROJECT_ENVIRONMENT=.venv-dev

# Now host uses .venv-dev, containers use default .venv
uv sync  # creates .venv-dev on host
```

Add both to `.gitignore`:
```
.venv/
.venv-dev/
```

This avoids rebuilding the venv when switching between host and container (different OS, Python versions, or native dependencies).

## Performance Tips

- uv caches aggressively; first install may be slower
- Use `uv sync --frozen` in CI for reproducible builds
- Use `uv cache clean` if cache grows too large
