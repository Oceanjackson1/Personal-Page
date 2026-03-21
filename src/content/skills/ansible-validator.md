---
title: "Ansible 验证器"
description: "验证、审查和调试 Ansible Playbook、角色、清单和集合"
category: "devops"
source: "community"
author: "Community"
tags: ["ansible", "validator"]
date: 2026-03-20
---

# Ansible Validator

## Overview

Comprehensive toolkit for validating, linting, and testing Ansible playbooks, roles, and collections. This skill provides automated workflows for ensuring Ansible code quality, syntax validation, dry-run testing with check mode and molecule, and intelligent documentation lookup for custom modules and collections with version awareness.

**Default behavior:** When validating any Ansible role with a `molecule/` directory, attempt Molecule automatically using `bash scripts/test_role.sh <role-path>`. If Molecule cannot run due to environment/runtime limits, mark Molecule as `BLOCKED`, report why, and continue all non-Molecule validation steps.

## Trigger Guidance

Use this skill when the request is about validating or debugging existing Ansible code, not generating new code.

Common trigger phrases:
- "validate this playbook"
- "lint this role"
- "why is ansible-lint failing"
- "run check mode safely"
- "test this role with molecule"
- "find security issues in these Ansible files"
- "module not found in this collection"

## When to Use This Skill

Apply this skill when encountering any of these scenarios:

- Working with Ansible files (`.yml`, `.yaml` playbooks, roles, inventories, vars)
- Validating Ansible playbook syntax and structure
- Linting and formatting Ansible code
- Performing dry-run testing with `ansible-playbook --check`
- Testing roles and playbooks with Molecule
- Debugging Ansible errors or misconfigurations
- Understanding custom Ansible modules, collections, or roles
- Ensuring infrastructure-as-code best practices
- Security validation of Ansible playbooks
- Version compatibility checks for collections and modules

## Preflight (Run First)

Run preflight before validation to avoid dead ends:

```bash
bash scripts/setup_tools.sh
```

Command path assumption: run commands from this skill root (`devops-skills-plugin/skills/ansible-validator`) or use absolute paths.

Preflight requirements:
- Baseline validation: `ansible`, `ansible-playbook`, `ansible-lint` (plus `yamllint` recommended)
- Molecule execution: `molecule` plus an available runtime (`docker` or `podman`)
- Security scanning: `checkov` (wrapper can bootstrap if missing)

Deterministic fallback rules:
- If baseline tools are missing but Python + pip are available, wrapper scripts bootstrap temporary environments automatically.
- If wrapper bootstrap fails (offline index, pip failure, missing Python), run direct commands for available tools, mark missing stages as `BLOCKED`, and continue.
- If Molecule runtime is unavailable (Docker/Podman missing or daemon not running), skip Molecule execution, mark as `BLOCKED`, and continue remaining stages.

## Wrapper vs Direct Command Routing

Use wrappers by default for consistent behavior and fallback handling.

| Validation scenario | Default command | Use direct command when | Fallback if command cannot run |
|---|---|---|---|
| Playbook syntax/lint | `bash scripts/validate_playbook.sh <playbook.yml>` | User asks for a single focused check only (`ansible-playbook --syntax-check`, `ansible-lint`, or `yamllint`) | Run any available direct checks and report skipped checks as `BLOCKED` |
| Role structural validation | `bash scripts/validate_role.sh <role-dir>` | User asks only for specific sub-checks (for example, structure only) | Run structure/YAML checks that are possible and report missing stages |
| Role Molecule execution | `bash scripts/test_role.sh <role-dir> [scenario]` | User explicitly asks for manual stage-by-stage Molecule commands | Mark Molecule `BLOCKED` with reason and continue non-Molecule role checks |
| Security scanning | `bash scripts/validate_playbook_security.sh <path>` or `bash scripts/validate_role_security.sh <path>` plus `bash scripts/scan_secrets.sh <path>` | User requests raw Checkov output formatting or custom flags | Run whichever scanner is available; if one is missing, run the other and report coverage gap |
| Module/collection discovery | `bash scripts/extract_ansible_info_wrapper.sh <path>` | Python environment is already known-good and user wants direct parser output | If extraction fails, manually inspect `requirements.yml`/`galaxy.yml` and continue with best-effort lookup |

## Validation Workflow

Follow this deterministic workflow and never stop at a missing dependency:

```
0. Preflight
   ├─> Run: bash scripts/setup_tools.sh
   ├─> Record tool/runtime readiness
   └─> Continue even when optional tools are missing

1. Identify scope
   ├─> Single playbook validation
   ├─> Role validation
   ├─> Collection validation
   └─> Multi-playbook/inventory validation

2. Syntax Validation
   ├─> Run ansible-playbook --syntax-check
   ├─> Run yamllint for YAML syntax
   └─> Report as PASS/FAIL/BLOCKED

3. Lint and Best Practices
   ├─> Run ansible-lint (comprehensive linting)
   ├─> Check for deprecated modules (see references/module_alternatives.md)
   ├─> **DETECT NON-FQCN MODULE USAGE** (apt vs ansible.builtin.apt)
   │   └─> Run bash scripts/check_fqcn.sh to identify short module names
   │   └─> Recommend FQCN alternatives from references/module_alternatives.md
   ├─> Verify role structure
   └─> Report linting issues

4. Dry-Run Testing (check mode)
   ├─> Run ansible-playbook --check (if inventory available)
   ├─> Analyze what would change
   └─> Report potential issues

5. Molecule Testing (for roles with molecule/) - AUTOMATIC ATTEMPT
   ├─> Check if molecule/ directory exists in role
   ├─> If present, run: bash scripts/test_role.sh <role-path> [scenario]
   ├─> If script exits 2, mark Molecule as BLOCKED (environment/runtime issue)
   ├─> If script exits 1, mark Molecule as FAIL (role/test issue)
   └─> Continue remaining validation regardless of Molecule outcome

6. Custom Module/Collection Analysis (if detected)
   ├─> Extract module/collection information
   ├─> Identify versions
   ├─> Lookup documentation (Context7 first, then web.search_query fallback)
   └─> Provide version-specific guidance

7. Security and Best Practices Review - DUAL SCANNING DEFAULT
   ├─> Run bash scripts/validate_playbook_security.sh or validate_role_security.sh (Checkov)
   ├─> Run bash scripts/scan_secrets.sh for hardcoded secret detection
   │   └─> This catches secrets Checkov may miss (passwords, API keys, tokens)
   ├─> If one scanner is unavailable, run the other and report reduced coverage
   ├─> Validate privilege escalation
   ├─> Review file permissions
   └─> Identify common anti-patterns

8. Reference Routing
   ├─> Map each error/warning class to the matching reference file
   ├─> Extract concrete remediation from references (not file-name-only mention)
   └─> Include source section + fix guidance in final report

9. Final Report (required format)
   ├─> Summary counts: PASS / FAIL / BLOCKED / SKIPPED
   ├─> Findings grouped by severity
   ├─> Tool/runtime blockers with exact command that failed
   └─> Next actions to reach full validation coverage
```

**Status contract:** `BLOCKED` means validation could not run due to environment/runtime constraints; `FAIL` means the Ansible code or tests failed.

## Error-Class Reference Routing

When issues are detected, consult the mapped reference and include a specific remediation excerpt in the report.

| Error class | Typical detector | Required reference | Required action |
|---|---|---|---|
| YAML parse/format errors | `yamllint`, `ansible-playbook --syntax-check` | `references/common_errors.md` (Syntax Errors) | Quote the matching syntax fix pattern and apply corrected YAML structure |
| Module/action resolution errors | `ansible-playbook`, `ansible-lint` | `references/common_errors.md` (Module/Collection Errors) | Provide install/version fix commands (`ansible-galaxy collection install ...`) |
| Deprecated or non-FQCN module usage | `ansible-lint`, `bash scripts/check_fqcn.sh` | `references/module_alternatives.md` | Provide exact FQCN/module replacement per finding |
| Template/variable errors | `ansible-playbook`, check mode | `references/common_errors.md` (Template/Variable Errors), `references/best_practices.md` (Variable Management) | Recommend `default()`, `required()`, or type conversion fixes |
| Connection/inventory/privilege errors | `ansible-playbook --check`, runtime output | `references/common_errors.md` (Connection, Inventory, Privilege sections) | Provide corrected inventory/auth/become configuration |
| Security policy failures (CKV_*) | `validate_*_security.sh` / Checkov | `references/security_checklist.md` | Map failed policy to a secure task rewrite |
| Hardcoded secrets | `bash scripts/scan_secrets.sh` | `references/security_checklist.md` (Secrets Management) | Replace with Vault/env/external secret manager approach |
| Role structure/idempotency warnings | `validate_role.sh`, Molecule idempotence | `references/best_practices.md` | Provide role layout or idempotency remediation steps |

External documentation lookup trigger:
- If the issue involves a custom/private collection or unknown module parameters not covered locally, run module discovery + documentation lookup (see section 7).

## Core Capabilities

### 1. YAML Syntax Validation

**Purpose:** Ensure YAML files are syntactically correct before Ansible parsing.

**Tools:**
- `yamllint` - YAML linter for syntax and formatting
- `ansible-playbook --syntax-check` - Ansible-specific syntax validation

**Workflow:**

```bash
# Check YAML syntax with yamllint
yamllint playbook.yml

# Or for entire directory
yamllint -c .yamllint .

# Check Ansible playbook syntax
ansible-playbook playbook.yml --syntax-check
```

**Common Issues Detected:**
- Indentation errors
- Invalid YAML syntax
- Duplicate keys
- Trailing whitespace
- Line length violations
- Missing colons or quotes

**Best Practices:**
- Always run yamllint before ansible-lint
- Use 2-space indentation consistently
- Configure yamllint rules in `.yamllint`
- Fix YAML syntax errors first, then Ansible-specific issues

### 2. Ansible Lint

**Purpose:** Enforce Ansible best practices and catch common errors.

**Workflow:**

```bash
# Lint a single playbook
ansible-lint playbook.yml

# Lint all playbooks in directory
ansible-lint .

# Lint with specific rules
ansible-lint -t yaml,syntax playbook.yml

# Skip specific rules
ansible-lint -x yaml[line-length] playbook.yml

# Output parseable format
ansible-lint -f pep8 playbook.yml

# Show rule details
ansible-lint -L
```

**Common Issues Detected:**
- Deprecated modules or syntax
- Missing task names
- Improper use of `command` vs `shell`
- Unquoted template expressions
- Hard-coded values that should be variables
- Missing `become` directives
- Inefficient task patterns
- Jinja2 template errors
- Incorrect variable usage
- Role dependencies issues

**Severity Levels:**
- **Error:** Must fix - will cause failures
- **Warning:** Should fix - potential issues
- **Info:** Consider fixing - best practice violations

**Auto-fix approach:**
- ansible-lint supports `--fix` for auto-fixable issues
- Always review changes before applying
- Some issues require manual intervention

### 3. Security Scanning (Checkov)

**Purpose:** Identify security vulnerabilities and compliance violations in Ansible code using Checkov, a static code analysis tool for infrastructure-as-code.

**What Checkov Provides Beyond ansible-lint:**

While ansible-lint focuses on code quality and best practices, Checkov specifically targets security policies and compliance:

- **SSL/TLS Security:** Certificate validation enforcement
- **HTTPS Enforcement:** Ensures secure protocols for downloads
- **Package Security:** GPG signature verification for packages
- **Cloud Security:** AWS, Azure, GCP misconfiguration detection
- **Compliance Frameworks:** Maps to security standards
- **Network Security:** Firewall and network policy validation

**Workflow:**

```bash
# Scan playbook for security issues
bash scripts/validate_playbook_security.sh playbook.yml

# Scan entire directory
bash scripts/validate_playbook_security.sh /path/to/playbooks/

# Scan role for security issues
bash scripts/validate_role_security.sh roles/webserver/

# Direct checkov usage
checkov -d . --framework ansible

# Scan with specific output format
checkov -d . --framework ansible --output json

# Scan and skip specific checks
checkov -d . --framework ansible --skip-check CKV_ANSIBLE_1
```

**Common Security Issues Detected:**

**Certificate Validation:**
- **CKV_ANSIBLE_1:** URI module disabling certificate validation
- **CKV_ANSIBLE_2:** get_url disabling certificate validation
- **CKV_ANSIBLE_3:** yum disabling certificate validation
- **CKV_ANSIBLE_4:** yum disabling SSL verification

**HTTPS Enforcement:**
- **CKV2_ANSIBLE_1:** URI module using HTTP instead of HTTPS
- **CKV2_ANSIBLE_2:** get_url using HTTP instead of HTTPS

**Package Security:**
- **CKV_ANSIBLE_5:** apt installing packages without GPG signature
- **CKV_ANSIBLE_6:** apt using force parameter bypassing signatures
- *
- *CKV2_ANSIBLE_4:** dnf installing packages without GPG signature
- **CKV2_ANSIBLE_5:** dnf disabling SSL verification
- **CKV2_ANSIBLE_6:** dnf disabling certificate validation

**Error Handling:**
- **CKV2_ANSIBLE_3:** Block missing error handling

**Cloud Security (when managing cloud resources):**
- **CKV_AWS_88:** EC2 instances with public IPs
- **CKV_AWS_135:** EC2 instances without EBS optimization

**Example Violation:**

```yaml
# BAD - Disables certificate validation
- name: Download file
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    validate_certs: false  # Security issue!

# GOOD - Certificate validation enabled
- name: Download file
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    validate_certs: true  # Or omit (true by default)
```
**Integration with Validation Workflow:**

Checkov complements ansible-lint:
1. **ansible-lint** catches code quality issues, deprecated modules, best practices
2. **Checkov** catches security vulnerabilities, compliance violations, cryptographic issues

**Best Practice:** Run both tools for comprehensive validation:
```bash
# Complete validation workflow
bash scripts/validate_playbook.sh playbook.yml         # Syntax + Lint
bash scripts/validate_playbook_security.sh playbook.yml  # Security
```

**Output Format:**

Checkov provides clear security scan results:
```
Security Scan Results:
  Passed:  15 checks
  Failed:  2 checks
  Skipped: 0 checks

Failed Checks:
  Check: CKV_ANSIBLE_2 - "Ensure that certificate validation isn't disabled with get_url"
    FAILED for resource: tasks/main.yml:download_file
    File: /roles/webserver/tasks/main.yml:10-15
```

**Remediation Resources:**
- Checkov Policy Index: https://www.checkov.io/5.Policy%20Index/ansible.html
- Ansible Security Checklist: `references/security_checklist.md`
- Ansible Best Practices: `references/best_practices.md`

**Installation:**

Checkov is automatically installed in a temporary environment if not available system-wide. For permanent installation:

```bash
pip3 install checkov
```

**When to Use:**
- Before deploying to production
- In CI/CD pipelines for automated security checks
- When working with sensitive infrastructure
- For compliance audits and security reviews
- When downloading files or installing packages
- When managing cloud resources with Ansible

### 4. Playbook Syntax Check

**Purpose:** Validate playbook syntax without executing tasks.

**Workflow:**

```bash
# Basic syntax check
ansible-playbook playbook.yml --syntax-check

# Syntax check with inventory
ansible-playbook -i inventory playbook.yml --syntax-check

# Syntax check with extra vars
ansible-playbook playbook.yml --syntax-check -e @vars.yml

# Check all playbooks
for file in *.yml; do
  ansible-playbook "$file" --syntax-check
done
```

**Validation Checks:**
- YAML parsing
- Playbook structure
- Task definitions
- Variable references
- Module parameter syntax
- Jinja2 template syntax
- Include/import statements

**Error Handling:**
- Parse error messages for specific issues
- Check for typos in module names
- Verify variable definitions
- Ensure proper indentation
- Check file paths for includes/imports

### 5. Dry-Run Testing (Check Mode)

**Purpose:** Preview changes that would be made without actually applying them.

**Workflow:**

```bash
# Run in check mode (dry-run)
ansible-playbook -i inventory playbook.yml --check

# Check mode with diff
ansible-playbook -i inventory playbook.yml --check --diff

# Check mode with verbose output
ansible-playbook -i inventory playbook.yml --check -v

# Check mode for specific hosts
ansible-playbook -i inventory playbook.yml --check --limit webservers

# Check mode with tags
ansible-playbook -i inventory playbook.yml --check --tags deploy

# Step through tasks
ansible-playbook -i inventory playbook.yml --check --step
```

**Check Mode Analysis:**

When reviewing check mode output, focus on:

1. **Task Changes:**
   - `ok`: No changes needed
   - `changed`: Would make changes
   - `failed`: Would fail (check for check_mode support)
   - `skipped`: Conditional skip

2. **Diff Output:**
   - Shows exact changes to files
   - Helps identify unintended modifications
   - Useful for reviewing template changes

3. **Handlers:**
   - Which handlers would be notified
   - Service restarts that would occur
   - Potential downtime

4. **Failed Tasks:**
   - Some modules don't support check mode
   - May need `check_mode: no` override
   - Identify tasks that would fail

**Limitations:**
- Not all modules support check mode
- Some tasks depend on previous changes
- May not accurately reflect all changes
- Stateful operations may show unexpected results

**Safety Considerations:**
- Always run check mode before real execution
- Review diff output carefully
- Test in non-production first
- Validate changes make sense
- Check for unintended side effects

### 6. Molecule Testing

**Purpose:** Test Ansible roles in isolated environments with multiple scenarios.

**Automatic attempt policy:** When validating any Ansible role with a `molecule/` directory, automatically attempt Molecule tests using `bash scripts/test_role.sh <role-path> [scenario]`.

**When to Use:**
- Automatically triggered when validating roles with molecule/ directory
- Testing roles before deployment
- Validating role compatibility across different OS versions
- Integration testing for complex roles
- CI/CD pipeline validation

**Workflow:**

```bash
# Initialize molecule for a role
cd roles/myrole
molecule init scenario --driver-name docker

# List scenarios
molecule list

# Run full test sequence
molecule test

# Individual test stages
molecule create      # Create test instances
molecule converge    # Run Ansible against instances
molecule verify      # Run verification tests
molecule destroy     # Destroy test instances

# Test with specific scenario
molecule test -s alternative

# Debug mode
molecule --debug test

# Keep instances for debugging
molecule converge
molecule login       # SSH into test instance
```

**Test Sequence:**
1. `dependency` - Install role dependencies
2. `lint` - Run yamllint and ansible-lint
3. `cleanup` - Clean up before testing
4. `destroy` - Destroy existing instances
5. `syntax` - Run syntax check
6. `create` - Create test instances
7. `prepare` - Prepare instances (install requirements)
8. `converge` - Run the role
9. `idempotence` - Run again, verify no changes
10. `side_effect` - Optional side effect playbook
11. `verify` - Run verification tests (Testinfra, etc.)
12. `cleanup` - Final cleanup
13. `destroy` - Destroy test instances

**Molecule Configuration:**

Check `molecule/default/molecule.yml`:
```yaml
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: ubuntu:22.04
provisioner:
  name: ansible
verifier:
  name: ansible
```

**Verification Tests:**

Molecule supports multiple verifiers:
- **Ansible** (built-in): Use Ansible tasks to verify
- **Testinfra**: Python-based infrastructure tests
- **Goss**: YAML-based server validation

Example Ansible verifier (`molecule/default/verify.yml`):
```yaml
---
- name: Verify
  hosts: all
  tasks:
    - name: Check service is running
      service:
        name: nginx
        state: started
      check_mode: true
      register: result
      failed_when: result.changed
```

**Common Molecule Errors:**
- Driver not installed (docker, podman, vagrant)
- Missing Python dependencies
- Platform image not available
- Network connectivity issues
- Insufficient permissions for driver

**Molecule Skip/Fallback Policy (Required):**
- If `molecule/` does not exist: mark Molecule as `SKIPPED` and continue.
- If `test_role.sh` exits `2`: mark Molecule as `BLOCKED` (missing/unavailable runtime dependency) and continue.
- If `test_role.sh` exits `1`: mark Molecule as `FAIL` (role/test issue) and continue.
- Never stop the full validation report because Molecule is blocked.

Use this reporting language for blocked Molecule runs:

```text
Molecule Status: BLOCKED
Reason: <missing dependency/runtime and failing command>
Fallback Applied: Completed syntax, lint, check-mode, and security validation without Molecule runtime tests.
Next Action: <install/start dependency>; rerun `bash scripts/test_role.sh <role-path> [scenario]`
```

### 7. Custom Module and Collection Documentation Lookup

**Purpose:** Automatically discover and retrieve version-specific documentation for custom modules and collections using web search and Context7 MCP.

**When to Trigger:**
- Encountering unfamiliar module usage
- Working with custom/private collections
- Debugging module-specific errors
- Understanding new module parameters
- Checking version compatibility
- Deprecated module alternatives

**Detection Workflow:**

1. **Extract Module Information:**
   - Use `scripts/extract_ansible_info_wrapper.sh` to parse playbooks and roles
   - Identify module usage and collections
   - Extract version constraints from `requirements.yml`

2. **Extract Collection Information:**
   - Identify collection namespaces (e.g., `community.general`, `ansible.posix`)
   - Determine collection versions from `requirements.yml` or `galaxy.yml`
   - Detect custom/private vs. public collections

**Documentation Lookup Strategy:**

Use this deterministic lookup order:

1. For public collections/modules:
   - Resolve library: `mcp__context7__resolve-library-id`
   - Query docs: `mcp__context7__query-docs`
2. If Context7 has no suitable result:
   - Use web search via `web.search_query` with versioned queries
   - Prioritize official docs (docs.ansible.com, galaxy.ansible.com, vendor docs)
3. For custom/private modules:
   - Prefer in-repo docs (`README`, module docs, role docs) first
   - Then use targeted web search with collection/module/version terms
4. Always report source + version context used in final guidance

**Search Query Templates:**

```
# For custom modules
"[module-name] ansible module version [version] documentation"
"[module-name] ansible [module-type] example"
"ansible [collection-name].[module-name] parameters"

# For custom collections
"ansible collection [collection-name] version [version]"
"[collection-namespace].[collection-name] ansible documentation"
"ansible galaxy [collection-name] modules"

# For specific errors
"ansible [module-name] error: [error-message]"
"ansible [collection-name] module failed"
```

**Example Workflow:**

```
User working with: community.docker.docker_container version 3.0.0

1. Extract module info from playbook:
   tasks:
     - name: Start container
       community.docker.docker_container:
         name: myapp
         image: nginx:latest

2. Detect collection: community.docker

3. Search for documentation:
   - Try Context7: mcp__context7__resolve-library-id("ansible community.docker")
   - Fallback to web.search_query("ansible community.docker collection version 3.0 docker_container module documentation")

4. If official docs found:
   - Parse module parameters (required vs optional)
   - Identify return values
   - Find usage examples
   - Check version compatibility

5. Provide version-specific guidance to user
```

**Version Compatibility Checks:**

- Compare required collection versions with available versions
- Identify deprecated modules or parameters
- Suggest upgrade paths if using outdated versions
- Warn about breaking changes between versions
- Check Ansible core version compatibility

**Common Collection Sources:**
- **Ansible Galaxy**: Official community collections
- **Red Hat Automation Hub**: Certified collections
- **GitHub**: Custom/private collections
- **Internal repositories**: Company-specific collections

### 8. Security and Best Practices Validation

**Purpose:** Identify security vulnerabilities and anti-patterns in Ansible playbooks.

**Security Checks:**

1. **Secrets Detection:**
   ```bash
   # Check for hardcoded credentials
   grep -r "password:" *.yml
   grep -r "secret:" *.yml
   grep -r "api_key:" *.yml
   grep -r "token:" *.yml
   ```

   **Remediation:** Use Ansible Vault, environment variables, or external secret management

2. **Privilege Escalation:**
   - Unnecessary use of `become: yes`
   - Missing `become_user` specification
   - Over-permissive sudo rules
   - Running entire playbooks as root

3. **File Permissions:**
   - World-readable sensitive files
   - Missing mode parameter on file/template tasks
   - Incorrect ownership settings
   - Sensitive files not encrypted with vault

4. **Command Injection:**
   - Unvalidated variables in shell/command modules
   - Missing `quote` filter for user input
   - Direct use of {{ var }} in command strings

5. **Network Security:**
   - Unencrypted protocols (HTTP instead of HTTPS)
   - Missing SSL/TLS validation
   - Exposing services on 0.0.0.0
   - Insecure default ports

**Best Practices:**

1. **Playbook Organization:**
   - Logical task separation
   - Reusable roles for common patterns
   - Clear directory structure
   - Meaningful playbook names

2. **Variable Management:**
   - Vault encryption for sensitive data
   - Clear variable naming conventions
   - Variable precedence awareness
   - Group/host vars organization
   - Default values using `default()` filter

3. **Task Naming:**
   - Descriptive task names
   - Consistent naming convention
   - Action-oriented descriptions
   - Include changed resource in name

4. **Idempotency:**
   - All tasks should be idempotent
   - Use proper modules instead of command/shell
   - Check mode compatibility
   - Proper use of `creates`, `removes` for command tasks
   - Avoid `changed_when: false` unless necessary

5. **Error Handling:**
   - Use `failed_when` for custom failure conditions
   - Implement `block/rescue/always` for error recovery
   - Set appropriate `any_errors_fatal`
   - Use `ignore_errors` sparingly

6. **Documentation:**
   - README for each role
   - Variable documentation in defaults/main.yml
   - Role metadata in meta/main.yml
   - Playbook header comments

**Reference Documentation:**

For detailed security guidelines and best practices, refer to:
- `references/security_checklist.md` - Common security vulnerabilities
- `references/best_practices.md` - Ansible coding standards
- `references/common_errors.md` - Common errors and solutions

## Tool Prerequisites

Run this preflight before validation:

```bash
# Preferred one-shot preflight
bash scripts/setup_tools.sh

# Check Ansible installation
ansible --version
ansible-playbook --version

# Check ansible-lint installation
ansible-lint --version

# Check yamllint installation
yamllint --version

# Check molecule installation (for role testing with molecule/)
molecule --version

# Check container runtime for Molecule
docker --version
docker info
# or
podman --version
podman info

# Install missing tools (example for pip)
pip install ansible ansible-lint yamllint ansible-compat

# Install molecule with docker driver
pip install molecule molecule-docker

# Install molecule with podman driver (alternative)
pip install molecule molecule-podman
```

**Minimum Versions:**
- Ansible: >= 2.9 (recommend >= 2.12)
- ansible-lint: >= 6.0.0
- yamllint: >= 1.26.0
- molecule: >= 3.4.0 (if testing roles)

**Execution policy when tools are missing:**
- If `ansible`/`ansible-lint` are missing, wrappers (`validate_playbook.sh`, `validate_role.sh`) attempt temporary venv bootstrap.
- If Molecule runtime (`docker info` or `podman info`) is unavailable, Molecule is `BLOCKED` and non-Molecule checks continue.
- If `checkov` is missing, security wrappers bootstrap it when possible; otherwise run `scan_secrets.sh` and report reduced security coverage.

**Optional Tools:**
- `ansible-inventory` - Inventory validation and graphing
- `ansible-doc` - Module documentation lookup
- `jq` - JSON parsing for structured output

## Error Troubleshooting

### Common Errors and Solutions

**Error: Module Not Found**
```
Solution: Install required collection with ansible-galaxy
Check collections/requirements.yml
Verify collection namespace and name
```

**Error: Undefined Variable**
```
Solution: Define variable in vars, defaults, or group_vars
Check variable precedence
Use default() filter for optional variables
Verify variable file is included
```

**Error: Template Syntax Error**
```
Solution: Check Jinja2 template syntax
Verify variable types match filters
Ensure proper quote escaping
Test template rendering separately
```

**Error: Connection Failed**
```
Solution: Verify inventory host accessibility
Check SSH configuration and keys
Verify ansible_host and ansible_port
Test with ansible -m ping
```

**Error: Permission Denied**
```
Solution: Add become: yes for privilege escalation
Verify sudo/su configuration
Check file permissions
Verify user has necessary privileges
```

**Error: Deprecated Module**
```
Solution: Check ansible-lint output for replacement
Consult module documentation for alternatives
Update to recommended module
Test functionality with new module
```

## Resources

### scripts/

**setup_tools.sh** - Preflight checker for Ansible validator dependencies. Verifies baseline tools (`ansible`, `ansible-playbook`, `ansible-lint`, `yamllint`) and Molecule runtime readiness (`docker`/`podman`) and provides installation guidance.

Usage:
```bash
bash scripts/setup_tools.sh
```

**extract_ansible_info_wrapper.sh** - Bash wrapper for extract_ansible_info.py that automatically handles PyYAML dependencies. Creates a temporary venv if PyYAML is not available in system Python.

Usage:
```bash
bash scripts/extract_ansible_info_wrapper.sh <path-to-playbook-or-role>
```

Output: JSON structure with modules, collections, and versions

**extract_ansible_info.py** - Python script (called by wrapper) to parse Ansible playbooks and roles to extract module usage, collection dependencies, and version information. The wrapper script handles dependency management automatically.

**validate_playbook.sh** - Comprehensive validation script that runs syntax check, yamllint, and ansible-lint on playbooks. Automatically installs ansible and ansible-lint in a temporary venv if not available on the system (prefers system versions when available).

Usage:
```bash
bash scripts/validate_playbook.sh <playbook.yml>
```

**validate_playbook_security.sh** - Security validation script that scans playbooks for security vulnerabilities using Checkov. Automatically installs checkov in a temporary venv if not available. Complements validate_playbook.sh by focusing on security-specific checks like SSL/TLS validation, HTTPS enforcement, and package signature verification.

Usage:
```bash
bash scripts/validate_playbook_security.sh <playbook.yml>
# Or scan entire directory
bash scripts/validate_playbook_security.sh /path/to/playbooks/
```

**validate_role.sh** - Comprehensive role validation script that checks role structure, YAML syntax, Ansible syntax, linting, and molecule configuration.

Usage:
```bash
bash scripts/validate_role.sh <role-directory>
```

Validates:
- Role directory structure (required and recommended directories)
- Presence of main.yml files in each directory
- YAML syntax across all role files
- Ansible syntax using a test playbook
- Best practices with ansible-lint
- Molecule test configuration

**validate_role_security.sh** - Security validation script for Ansible roles using Checkov. Scans entire role directory for security issues. Automatically installs checkov in a temporary venv if not available. Complements validate_role.sh with security-focused checks.

Usage:
```bash
bash scripts/validate_role_security.sh <role-directory>
```

**test_role.sh** - Wrapper script for Molecule testing with automatic dependency installation. If `molecule` is missing, it creates a temporary venv and installs dependencies. Returns exit code `2` for environment/runtime blockers (for example missing Docker/Podman runtime) and exit code `1` for role/test failures.

Usage:
```bash
bash scripts/test_role.sh <role-directory> [scenario]
```

**scan_secrets.sh** - Comprehensive secret scanner that uses grep-based pattern matching to detect hardcoded secrets in Ansible files. Complements Checkov security scanning by catching secrets that static analysis may miss, including passwords, API keys, tokens, AWS credentials, and private keys.

Usage:
```bash
bash scripts/scan_secrets.sh <playbook.yml|role-directory|directory>
```

Detects:
- Hardcoded passwords and credentials
- API keys and tokens
- AWS access keys and secret keys
- Database connection strings with embedded credentials
- Private key content (RSA, OpenSSH, EC, DSA)

**IMPORTANT:** This script should ALWAYS be run alongside Checkov (`validate_*_security.sh`) for comprehensive security scanning. Checkov catches SSL/TLS and protocol issues; this script catches hardcoded secrets.

**check_fqcn.sh** - Scans Ansible files to identify modules using short names instead of Fully Qualified Collection Names (FQCN). Recommends migration to `ansible.builtin.*` or appropriate collection namespace for better clarity and future compatibility.

Usage:
```bash
bash scripts/check_fqcn.sh <playbook.yml|role-directory|directory>
```

Detects:
- ansible.builtin modules (apt, yum, copy, file, template, service, etc.)
- community.general modules (ufw, docker_container, timezone, etc.)
- ansible.posix modules (synchronize, acl, firewalld, etc.)

Provides specific migration recommendations with FQCN alternatives.

**validate_inventory.sh** - Validates Ansible inventory files and directories. Checks YAML syntax, resolves host/group hierarchy, and flags common structural issues such as plaintext credentials and missing `ansible_connection=local` for localhost entries. Automatically installs ansible in a temporary venv if not available.

Usage:
```bash
bash scripts/validate_inventory.sh <inventory-file|inventory-directory>
```

Validation stages:
1. YAML syntax check (yamllint) on all inventory YAML files
2. Inventory parse — `ansible-inventory --list` to verify host/group resolution
3. Host graph — `ansible-inventory --graph` to display group hierarchy
4. Structural checks — plaintext passwords, localhost connection settings, group_vars/host_vars presence

### references/

**security_checklist.md** - Comprehensive security validation checklist for Ansible playbooks covering secrets management, privilege escalation, file permissions, and command injection.

**best_practices.md** - Ansible coding standards and best practices for playbook organization, variable handling, task naming, idempotency, and documentation.

**common_errors.md** - Database of common Ansible errors with detailed solutions and prevention strategies.

**module_alternatives.md** - Guide for replacing deprecated modules with current alternatives.

### assets/

**.yamllint** - Pre-configured yamllint rules for Ansible YAML files.

**.ansible-lint** - Pre-configured ansible-lint configuration with reasonable rule settings.

**molecule.yml.template** - Template molecule configuration for role testing.

## Workflow Examples

### Example 1: Validate a Single Playbook

```
User: "Check if this playbook.yml file is valid"

Steps:
1. Run preflight: `bash scripts/setup_tools.sh`
2. Run wrapper: `bash scripts/validate_playbook.sh playbook.yml`
3. If inventory is provided, run check mode: `ansible-playbook -i <inventory> playbook.yml --check --diff`
4. Run security wrappers:
   - `bash scripts/validate_playbook_security.sh playbook.yml`
   - `bash scripts/scan_secrets.sh playbook.yml`
5. If custom modules are detected, run docs lookup workflow (Context7 first, web fallback)
6. Report results with PASS/FAIL/BLOCKED/SKIPPED counts and remediation steps
```

### Example 2: Validate an Ansible Role

```
User: "Validate my ansible role in ./roles/webserver/"

Steps:
1. Run preflight: `bash scripts/setup_tools.sh`
2. Run role wrapper: `bash scripts/validate_role.sh ./roles/webserver/`
3. This checks:
   - Role directory structure (tasks/, defaults/, handlers/, meta/, etc.)
   - Required main.yml files
   - YAML syntax with yamllint
   - Ansible syntax with ansible-playbook
   - Best practices with ansible-lint
   - Molecule configuration (if present)
4. If `molecule/` exists, attempt Molecule automatically:
   - `bash scripts/test_role.sh ./roles/webserver/`
   - Exit `2`: report `Molecule Status: BLOCKED` with reason, continue remaining checks
   - Exit `1`: report `Molecule Status: FAIL` with debugging guidance
5. Run role security checks:
   - `bash scripts/validate_role_security.sh ./roles/webserver/`
   - `bash scripts/scan_secrets.sh ./roles/webserver/`
6. If custom modules detected, run documentation lookup workflow
7. Provide final report with severity, blockers, and rerun actions
```

### Example 3: Dry-Run Testing for Production

```
User: "Run playbook in check mode for production servers"

Steps:
1. Verify inventory file exists
2. Run ansible-playbook --check --diff -i production
3. Analyze check mode output
4. Highlight tasks that would change
5. Review handler notifications
6. Flag any security concerns
7. Provide recommendation on safety of applying
```

### Example 4: Understanding Custom Collection Module

```
User: "I'm using community.postgresql.postgresql_db version 2.3.0, what parameters are available?"

Steps:
1. Try Context7 MCP: `mcp__context7__resolve-library-id("ansible community.postgresql")`
2. If found, query docs with `mcp__context7__query-docs` for `postgresql_db`
3. If not found, use `web.search_query`: "ansible community.postgresql version 2.3.0 postgresql_db module documentation"
4. Extract module parameters (required vs optional)
5. Provide examples of common usage patterns
6. Note any version-specific considerations
```

### Example 5: Testing Role with Molecule

```
User: "Test my nginx role with molecule"

Steps:
1. Check if molecule is configured in role
2. Run preflight (`bash scripts/setup_tools.sh`) and confirm Docker/Podman runtime availability
3. Run `bash scripts/test_role.sh <role-path> [scenario]`
4. If exit code is `2`, mark Molecule `BLOCKED`, report reason, and continue non-Molecule checks
5. If exit code is `1`, inspect converge/verify output and report role issues
6. Analyze idempotency, syntax, and verification outcomes
7. Suggest improvements and exact rerun command
```

## Integration with Other Skills

This skill works well in combination with:
- **k8s-yaml-validator** - When Ansible manages Kubernetes resources
- **terraform-validator** - When Ansible and Terraform are used together
- **k8s-debug** - For debugging infrastructure managed by Ansible

## Notes

- Run stages in order: preflight -> syntax -> lint/FQCN -> check mode -> Molecule (when applicable) -> security -> reference routing -> final report.
- Use wrapper scripts as default execution path; switch to direct commands only when user asks or when wrapper bootstrapping is blocked.
- Treat missing dependencies/runtime as `BLOCKED` (not silent skip), and continue with remaining stages.
- For every detected issue class, include mapped reference guidance (`common_errors`, `best_practices`, `module_alternatives`, `security_checklist`).
- Always include explicit rerun commands for failed or blocked stages.

## Done Criteria

This skill execution is complete when:
- Preflight status for required tools is reported (`ansible`, `ansible-lint`, and Molecule runtime status when role tests are in scope).
- Validation produces deterministic stage outcomes using `PASS`, `FAIL`, `BLOCKED`, and `SKIPPED`.
- Molecule never dead-ends the full validation flow; blocked runtime conditions are reported with fallback language.
- Wrapper-vs-direct command choice is explicit and justified.
- Reference lookups are tied to the actual error classes found, with concrete remediation guidance.

---

## Reference: Best_Practices

# Ansible Best Practices

## Overview

This guide provides comprehensive best practices for writing clean, maintainable, and reliable Ansible playbooks, roles, and collections.

## Playbook Organization

### Directory Structure

```
ansible-project/
├── ansible.cfg              # Ansible configuration
├── inventory/               # Inventory files
│   ├── production/
│   │   ├── hosts           # Production inventory
│   │   └── group_vars/
│   │       └── all.yml
│   └── staging/
│       ├── hosts           # Staging inventory
│       └── group_vars/
│           └── all.yml
├── group_vars/             # Group-specific variables
│   ├── all.yml
│   ├── webservers.yml
│   └── databases.yml
├── host_vars/              # Host-specific variables
│   └── server1.yml
├── roles/                  # Reusable roles
│   ├── common/
│   ├── webserver/
│   └── database/
├── playbooks/              # Playbooks
│   ├── site.yml           # Master playbook
│   ├── webservers.yml
│   └── databases.yml
├── files/                  # Static files
├── templates/              # Jinja2 templates
├── vars/                   # Additional variables
│   └── external_vars.yml
└── requirements.yml        # Collection dependencies
```

### Role Structure

```
roles/webserver/
├── README.md              # Role documentation
├── defaults/
│   └── main.yml          # Default variables (lowest precedence)
├── vars/
│   └── main.yml          # Role variables (higher precedence)
├── tasks/
│   ├── main.yml          # Main task list
│   ├── install.yml       # Installation tasks
│   └── configure.yml     # Configuration tasks
├── handlers/
│   └── main.yml          # Handlers
├── templates/
│   └── nginx.conf.j2     # Template files
├── files/
│   └── index.html        # Static files
├── meta/
│   └── main.yml          # Role metadata and dependencies
└── molecule/             # Molecule test scenarios
    └── default/
        ├── molecule.yml
        ├── converge.yml
        └── verify.yml
```

## Task Naming and Documentation

### ✅ Good Task Names

```yaml
# Descriptive, action-oriented names
- name: Install nginx web server
  apt:
    name: nginx
    state: present

- name: Configure nginx virtual host for example.com
  template:
    src: vhost.conf.j2
    dest: /etc/nginx/sites-available/example.com

- name: Enable and start nginx service
  systemd:
    name: nginx
    state: started
    enabled: yes

- name: Create application user with limited privileges
  user:
    name: appuser
    system: yes
    shell: /bin/false
    home: /var/lib/app
```

### ❌ Bad Task Names

```yaml
# Vague, uninformative names
- name: Install package
  apt:
    name: nginx

- name: Configure
  template:
    src: vhost.conf.j2
    dest: /etc/nginx/sites-available/example.com

- name: Service
  systemd:
    name: nginx
    state: started

# No name at all
- apt:
    name: nginx
```

### Best Practices

1. **Always name your tasks** - makes output readable
2. **Use action verbs** - Install, Configure, Enable, Create, etc.
3. **Be specific** - mention what is being installed/configured
4. **Keep names concise** - but not at the expense of clarity
5. **Use consistent naming** - across all playbooks

## Variable Management

### Variable Naming Conventions

```yaml
# ✅ Good - Descriptive, namespaced
nginx_version: "1.18.0"
nginx_worker_processes: 4
nginx_worker_connections: 1024
app_database_host: "db.example.com"
app_database_port: 5432

# ❌ Bad - Generic, collision-prone
version: "1.18.0"  # Too generic
workers: 4         # Unclear
db: "db.example.com"  # Vague
```

### Variable Precedence

Understand variable precedence (from lowest to highest):

1. role defaults (defaults/main.yml)
2. inventory file or script group vars
3. inventory group_vars/all
4. playbook group_vars/all
5. inventory group_vars/*
6. playbook group_vars/*
7. inventory file or script host vars
8. inventory host_vars/*
9. playbook host_vars/*
10. host facts / cached set_facts
11. play vars
12. play vars_prompt
13. play vars_files
14. role vars (vars/main.yml)
15. block vars
16. task vars
17. include_vars
18. set_facts / registered vars
19. role (and include_role) params
20. include params
21. extra vars (always win precedence)

### Variable Organization

```yaml
# defaults/main.yml - Intended to be overridden
---
nginx_port: 80
nginx_user: www-data
nginx_worker_processes: "auto"

# vars/main.yml - Should not be overridden
---
nginx_config_dir: /etc/nginx
nginx_log_dir: /var/log/nginx
nginx_pid_file: /run/nginx.pid
```

### Using Defaults and Required Variables

```yaml
# Use default filter for optional variables
- name: Set API endpoint
  set_fact:
    api_endpoint: "{{ custom_api_endpoint | default('https://api.example.com') }}"

# Use required filter for mandatory variables
- name: Configure database
  template:
    src: db.conf.j2
    dest: /etc/app/database.conf
  vars:
    db_password: "{{ database_password | required('database_password must be defined') }}"
```

## Idempotency

### What is Idempotency?

Idempotency means running the same playbook multiple times produces the same result without making unnecessary changes.

### ✅ Idempotent Tasks

```yaml
# File module - inherently idempotent
- name: Ensure configuration directory exists
  file:
    path: /etc/myapp
    state: directory
    mode: '0755'

# Template module - only changes if content differs
- name: Configure application
  template:
    src: app.conf.j2
    dest: /etc/myapp/app.conf
    mode: '0644'

# Package module - idempotent
- name: Install required packages
  apt:
    name:
      - nginx
      - python3
      - git
    state: present

# Service module - idempotent
- name: Ensure service is running
  systemd:
    name: myapp
    state: started
    enabled: yes
```

### ⚠️ Non-Idempotent Tasks (Need Fixes)

```yaml
# Command/shell without creates/removes
- name: Download file
  command: curl -o /tmp/file.tar.gz https://example.com/file.tar.gz
  # This runs every time!

# Fix with creates
- name: Download file
  command: curl -o /tmp/file.tar.gz https://example.com/file.tar.gz
  args:
    creates: /tmp/file.tar.gz

# Or better - use get_url module
- name: Download file
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    checksum: sha256:abc123...

# Command that always reports changed
- name: Check service status
  command: systemctl status myapp
  register: service_status
  # Always shows as changed!

# Fix with changed_when
- name: Check service status
  command: systemctl status myapp
  register: service_status
  changed_when: false
  failed_when: service_status.rc not in [0, 3]
```

### Best Practices for Idempotency

1. **Use modules instead of command/shell** whenever possible
2. **Use creates/removes** parameters for command/shell when necessary
3. **Set changed_when appropriately** for read-only commands
4. **Test idempotency** - run playbook twice, second run should show no changes
5. **Use check mode** to verify idempotency without making changes

## Module Selection

### Prefer Modules Over Commands

```yaml
# ❌ Bad - Using shell/command
- name: Create directory
  shell: mkdir -p /opt/myapp

- name: Install package
  command: apt-get install -y nginx

- name: Add line to file
  shell: echo "export PATH=$PATH:/opt/bin" >> ~/.bashrc

# ✅ Good - Using appropriate modules
- name: Create directory
  file:
    path: /opt/myapp
    state: directory
    mode: '0755'

- name: Install package
  apt:
    name: nginx
    state: present

- name: Add line to file
  lineinfile:
    path: ~/.bashrc
    line: 'export PATH=$PATH:/opt/bin'
    create: yes
```

### Module Hierarchy

1. **First choice**: Specific module (apt, yum, systemd, copy, etc.)
2. **Second choice**: Generic module (package, service, etc.)
3. **Last resort**: command or shell module

## Error Handling

### Using Blocks

```yaml
- name: Handle errors gracefully
  block:
    - name: Attempt risky operation
      command: /usr/local/bin/risky-operation.sh
      register: result

    - name: Process successful result
      debug:
        msg: "Operation succeeded: {{ result.stdout }}"

  rescue:
    - name: Handle failure
      debug:
        msg: "Operation failed, applying fallback"

    - name: Apply fallback configuration
      copy:
        src: fallback.conf
        dest: /etc/app/config.conf

  always:
    - name: Cleanup temporary files
      file:
        path: /tmp/operation.lock
        state: absent
```

### Failed When and Changed When

```yaml
# Custom failure conditions
- name: Check disk space
  shell: df -h / | tail -1 | awk '{print $5}' | sed 's/%//'
  register: disk_usage
  failed_when: disk_usage.stdout | int > 90

# Custom changed conditions
- name: Verify configuration
  command: /usr/local/bin/check-config.sh
  register: config_check
  changed_when: false
  failed_when: config_check.rc != 0

# Multiple conditions
- name: Run healthcheck
  uri:
    url: http://localhost:8080/health
    method: GET
  register: health
  failed_when:
    - health.status != 200
    - "'healthy' not in health.json.status"
```

### Ignoring Errors (Use Sparingly)

```yaml
# Only when failure is acceptable
- name: Try to stop service (may not exist)
  systemd:
    name: old-service
    state: stopped
  ignore_errors: yes

# Better approach - check first
- name: Check if service exists
  systemd:
    name: old-service
  register: service_status
  failed_when: false

- name: Stop service if it exists
  systemd:
    name: old-service
    state: stopped
  when: service_status.status.ActiveState is defined
```

## Conditionals and Loops

### When Conditions

```yaml
# Simple condition
- name: Install Apache (Debian)
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"

# Multiple conditions (AND)
- name: Install package on Ubuntu 20.04
  apt:
    name: package
    state: present
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "20.04"

# OR conditions
- name: Install on RHEL or CentOS
  yum:
    name: package
    state: present
  when: ansible_distribution == "RedHat" or ansible_distribution == "CentOS"

# Complex conditions
- name: Configure firewall
  ufw:
    rule: allow
    port: '443'
  when:
    - ansible_os_family == "Debian"
    - firewall_enabled | default(true) | bool
    - ansible_virtualization_type != "docker"
```

### Loops

```yaml
# Simple loop
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - python3
    - git

# Loop with hash
- name: Create users
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { name: 'alice', groups: 'developers' }
    - { name: 'bob', groups: 'operators' }

# Loop with dict
- name: Create directories
  file:
    path: "{{ item.path }}"
    state: directory
    mode: "{{ item.mode }}"
  loop:
    - { path: '/opt/app', mode: '0755' }
    - { path: '/var/log/app', mode: '0755' }
    - { path: '/etc/app', mode: '0750' }

# Loop with conditional
- name: Install debug tools (dev only)
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - strace
    - tcpdump
    - gdb
  when: environment == "development"
```

## Templates and Jinja2

### Template Best Practices

```jinja2
{# templates/nginx.conf.j2 #}

{# Use comments to explain complex logic #}
user {{ nginx_user }};
worker_processes {{ nginx_worker_processes }};
pid {{ nginx_pid_file }};

{# Conditionals in templates #}
{% if nginx_enable_ssl %}
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
{% endif %}

{# Loops in templates #}
{% for vhost in nginx_vhosts %}
server {
    listen {{ vhost.port }};
    server_name {{ vhost.server_name }};
    root {{ vhost.document_root }};

    {% if vhost.ssl_enabled | default(false) %}
    ssl_certificate {{ vhost.ssl_cert }};
    ssl_certificate_key {{ vhost.ssl_key }};
    {% endif %}
}
{% endfor %}

{# Filters #}
upstream_servers = {{ backend_servers | join(',') }}
max_connections = {{ max_connections | default(1024) }}
```

### Useful Jinja2 Filters

```yaml
# String manipulation
- debug:
    msg: "{{ 'hello' | upper }}"  # HELLO
    msg: "{{ 'HELLO' | lower }}"  # hello
    msg: "{{ '  hello  ' | trim }}"  # hello

# List operations
- debug:
    msg: "{{ [1,2,3] | first }}"  # 1
    msg: "{{ [1,2,3] | last }}"  # 3
    msg: "{{ [1,2,3] | length }}"  # 3
    msg: "{{ [1,2,3] | join(',') }}"  # 1,2,3

# Default values
- debug:
    msg: "{{ undefined_var | default('default_value') }}"

# Type conversion
- debug:
    msg: "{{ '123' | int }}"  # 123
    msg: "{{ 'true' | bool }}"  # True

# JSON and YAML
- debug:
    msg: "{{ my_dict | to_json }}"
    msg: "{{ my_dict | to_nice_json }}"
    msg: "{{ my_dict | to_yaml }}"
```

## Tags

### Using Tags Effectively

```yaml
---
- name: Configure web server
  hosts: webservers
  tasks:
    - name: Install nginx
      apt:
        name: nginx
      tags:
        - packages
        - nginx

    - name: Configure nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      tags:
        - configuration
        - nginx

    - name: Start nginx
      systemd:
        name: nginx
        state: started
      tags:
        - services
        - nginx

    - name: Configure firewall
      ufw:
        rule: allow
        port: '80'
      tags:
        - security
        - firewall
```

### Running with Tags

```bash
# Run only nginx tasks
ansible-playbook site.yml --tags nginx

# Run configuration tasks only
ansible-playbook site.yml --tags configuration

# Skip certain tags
ansible-playbook site.yml --skip-tags packages

# Multiple tags
ansible-playbook site.yml --tags "nginx,firewall"
```

## Handlers

### Handler Best Practices

```yaml
# tasks/main.yml
- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify:
    - Validate nginx configuration
    - Restart nginx

- name: Add virtual host
  template:
    src: vhost.conf.j2
    dest: "/etc/nginx/sites-available/{{ vhost_name }}"
  notify:
    - Reload nginx

# handlers/main.yml
- name: Validate nginx configuration
  command: nginx -t
  changed_when: false

- name: Restart nginx
  systemd:
    name: nginx
    state: restarted

- name: Reload nginx
  systemd:
    name: nginx
    state: reloaded
```

### Handler Facts

1. **Handlers run once** at the end of a play, even if notified multiple times
2. **Handlers run in order** they're defined, not in order they're notified
3. **Use listen** for handler groups
4. **Flush handlers** with `meta: flush_handlers` to run immediately

## Check Mode and Diff Mode

### Supporting Check Mode

```yaml
# Task that supports check mode naturally (file module)
- name: Create directory
  file:
    path: /opt/myapp
    state: directory

# Task that doesn't support check mode, but can run anyway
- name: Check service status
  command: systemctl status myapp
  check_mode: no  # Always run, even in check mode
  changed_when: false

# Task that should be skipped in check mode
- name: Apply complex changes
  command: /usr/local/bin/complex-script.sh
  when: not ansible_check_mode
```

### Using Check Mode

```bash
# Run in check mode (dry-run)
ansible-playbook site.yml --check

# Check mode with diff (show changes)
ansible-playbook site.yml --check --diff

# See what would change
ansible-playbook site.yml --check --diff | grep -A 10 "changed:"
```

## Documentation

### Playbook Documentation

```yaml
---
# site.yml - Master playbook for deploying web application
#
# This playbook:
#   - Configures common settings on all hosts
#   - Deploys web servers
#   - Configures databases
#   - Sets up load balancers
#
# Usage:
#   ansible-playbook -i inventory/production site.yml
#
# Tags:
#   - common: Common configuration tasks
#   - webserver: Web server setup
#   - database: Database configuration
#
# Variables (see group_vars/all.yml):
#   - app_version: Application version to deploy
#   - environment: Environment name (production/staging)

- name: Configure common settings
  hosts: all
  roles:
    - common
  tags: common

- name: Deploy web servers
  hosts: webservers
  roles:
    - webserver
  tags: webserver
```

### Role Documentation (README.md)

```markdown
# Webserver Role

## Description

Installs and configures Nginx web server with virtual hosts and SSL support.

## Requirements

- Ansible >= 2.9
- Supported OS: Ubuntu 20.04, Debian 11

## Role Variables

### Required Variables

- `nginx_vhosts`: List of virtual hosts to configure (see example)

### Optional Variables

- `nginx_worker_processes`: Number of worker processes (default: auto)
- `nginx_worker_connections`: Max connections per worker (default: 1024)
- `nginx_enable_ssl`: Enable SSL support (default: false)

## Dependencies

None

## Example Playbook

```yaml
- hosts: webservers
  roles:
    - role: webserver
      vars:
        nginx_vhosts:
          - server_name: example.com
            port: 80
            document_root: /var/www/example
```

## License

MIT

## Author

Your Name
```

## Testing Best Practices

See the molecule configuration and testing section in the main SKILL.md for comprehensive testing guidance.

## Performance Tips

1. **Use pipelining** in ansible.cfg
   ```ini
   [ssh_connection]
   pipelining = True
   ```

2. **Enable fact caching**
   ```ini
   [defaults]
   gathering = smart
   fact_caching = jsonfile
   fact_caching_connection = /tmp/ansible_facts
   fact_caching_timeout = 86400
   ```

3. **Limit fact gathering**
   ```yaml
   - hosts: all
     gather_facts: no  # Don't gather if not needed
   ```

4. **Use async for long-running tasks**
   ```yaml
   - name: Long running task
     command: /usr/local/bin/long-task.sh
     async: 3600
     poll: 0
     register: long_task

   - name: Check on long task
     async_status:
       jid: "{{ long_task.ansible_job_id }}"
     register: job_result
     until: job_result.finished
     retries: 30
   ```

## Summary Checklist

- [ ] Playbooks and roles have clear directory structure
- [ ] All tasks have descriptive names
- [ ] Variables use namespacing (role_variable_name)
- [ ] Sensitive data encrypted with Ansible Vault
- [ ] Playbooks are idempotent (can run multiple times safely)
- [ ] Using modules instead of shell/command where possible
- [ ] Error handling with blocks, failed_when, changed_when
- [ ] Conditionals used appropriately
- [ ] Templates properly commented
- [ ] Tags used for granular execution
- [ ] Handlers used for service restarts
- [ ] Check mode supported
- [ ] Documentation complete (README, comments)
- [ ] Tested with molecule or similar framework
- [ ] No hardcoded secrets
- [ ] File permissions explicitly set

---

## Reference: Common_Errors

# Common Ansible Errors and Solutions

## Overview

This document provides solutions to common Ansible errors, including syntax errors, module errors, connection issues, and runtime problems.

## Syntax Errors

### Error: mapping values are not allowed here

```
ERROR! Syntax Error while loading YAML.
  mapping values are not allowed here
```

**Cause:** YAML indentation error or missing quote

**Example Problem:**
```yaml
- name: Configure app
  template:
    src: config.j2
    dest: /etc/app/config.yml
    vars:
      db_host: localhost:5432  # WRONG: colon not quoted
```

**Solution:**
```yaml
- name: Configure app
  template:
    src: config.j2
    dest: /etc/app/config.yml
    vars:
      db_host: "localhost:5432"  # Quoted
```

### Error: found undefined alias

```
ERROR! Syntax Error while loading YAML.
  found undefined alias 'anchor'
```

**Cause:** Using YAML anchor/alias incorrectly

**Solution:** Ensure anchors are defined before use
```yaml
# Define anchor
common_packages: &common_packages
  - git
  - curl
  - vim

# Use alias
- name: Install common packages
  apt:
    name: *common_packages
```

### Error: could not find expected ':'

```
ERROR! could not find expected ':'
```

**Cause:** Missing colon or improper YAML structure

**Example Problem:**
```yaml
- name Install package  # Missing colon after name
  apt:
    name nginx  # Missing colon after name
```

**Solution:**
```yaml
- name: Install package
  apt:
    name: nginx
```

## Module Errors

### Error: Unsupported parameters for module

```
ERROR! Unsupported parameters for (module) module: parameter_name
```

**Cause:** Using wrong parameter name or typo

**Example Problem:**
```yaml
- name: Create file
  file:
    path: /tmp/test
    state: present
    mod: '0644'  # WRONG: should be 'mode'
```

**Solution:**
```yaml
- name: Create file
  file:
    path: /tmp/test
    state: present
    mode: '0644'  # Correct parameter name
```

**How to check:** Use `ansible-doc module_name` to see correct parameters

### Error: MODULE FAILURE

```
fatal: [host]: FAILED! => {"changed": false, "module_stderr": "..."}
```

**Common Causes:**
1. Python not installed on target
2. Wrong Python interpreter
3. SELinux blocking module execution

**Solutions:**
```yaml
# Specify Python interpreter in inventory
[webservers]
server1 ansible_python_interpreter=/usr/bin/python3

# Or in playbook
- hosts: all
  vars:
    ansible_python_interpreter: /usr/bin/python3
```

### Error: Missing required arguments

```
fatal: [host]: FAILED! => {"changed": false, "msg": "missing required arguments: name"}
```

**Cause:** Required module parameter not provided

**Solution:** Add the required parameter
```yaml
# Wrong
- name: Install package
  apt:
    state: present

# Correct
- name: Install package
  apt:
    name: nginx
    state: present
```

## Template Errors

### Error: template error while templating string

```
fatal: [host]: FAILED! => {"msg": "An unhandled exception occurred while templating..."}
```

**Common Causes:**
1. Undefined variable
2. Wrong filter syntax
3. Jinja2 syntax error

**Example Problem:**
```yaml
- name: Configure app
  template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    port: "{{ app_port }}"  # app_port undefined
```

**Solutions:**
```yaml
# Use default filter
vars:
  port: "{{ app_port | default(8080) }}"

# Or use required filter
vars:
  port: "{{ app_port | required('app_port must be defined') }}"

# Or check if defined
- name: Configure app
  template:
    src: config.j2
    dest: /etc/app/config.yml
  when: app_port is defined
```

### Error: Unexpected templating type error

```
fatal: [host]: FAILED! => {"msg": "Unexpected templating type error occurred on (...)"}
```

**Cause:** Wrong variable type (e.g., trying to use int as string)

**Solution:** Use type conversion filters
```yaml
# Convert to string
port: "{{ app_port | string }}"

# Convert to int
replicas: "{{ replica_count | int }}"

# Convert to bool
enabled: "{{ feature_enabled | bool }}"
```

## Connection Errors

### Error: Failed to connect to the host via ssh

```
fatal: [host]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh"}
```

**Common Causes:**
1. Host not accessible
2. Wrong SSH key
3. Wrong username
4. SSH not running on host

**Solutions:**
```bash
# Test SSH connectivity
ssh user@host

# Check Ansible can ping
ansible host -m ping

# Use correct SSH key
ansible-playbook -i inventory playbook.yml --private-key=~/.ssh/id_rsa

# Specify user in inventory
[webservers]
server1 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### Error: Permission denied (publickey)

```
fatal: [host]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}
```

**Solutions:**
```bash
# Ensure SSH key is added to target
ssh-copy-id user@host

# Or specify key in inventory
[webservers]
server1 ansible_ssh_private_key_file=~/.ssh/custom_key

# Check SSH agent
ssh-add -l
ssh-add ~/.ssh/id_rsa
```

### Error: Authentication or permission failure

```
fatal: [host]: UNREACHABLE! => {"msg": "Authentication or permission failure."}
```

**Solutions:**
```yaml
# Use password authentication (less secure)
- hosts: all
  vars:
    ansible_ssh_pass: password  # Better to use vault
    ansible_become_pass: password

# Or use ask-pass
ansible-playbook -i inventory playbook.yml --ask-pass --ask-become-pass
```

## Privilege Escalation Errors

### Error: Missing sudo password

```
fatal: [host]: FAILED! => {"msg": "Missing sudo password"}
```

**Solutions:**
```bash
# Provide sudo password at runtime
ansible-playbook -i inventory playbook.yml --ask-become-pass

# Or configure passwordless sudo on target
# /etc/sudoers.d/ansible
ansible_user ALL=(ALL) NOPASSWD: ALL
```

### Error: you must be root

```
fatal: [host]: FAILED! => {"msg": "Could not create file: Permission denied"}
```

**Solution:** Add `become: yes` to task or play
```yaml
- name: Install package
  apt:
    name: nginx
    state: present
  become: yes

# Or for entire play
- hosts: all
  become: yes
  tasks:
    - name: Install package
      apt:
        name: nginx
```

## Variable Errors

### Error: The task includes an option with an undefined variable

```
fatal: [host]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'variable' is undefined"}
```

**Solutions:**
```yaml
# Use default filter
- name: Use variable with default
  debug:
    msg: "{{ my_var | default('default_value') }}"

# Check if defined before use
- name: Use variable conditionally
  debug:
    msg: "{{ my_var }}"
  when: my_var is defined

# Use required filter to make it explicit
- name: Require variable
  debug:
    msg: "{{ my_var | required('my_var must be defined') }}"
```

### Error: Conflicting variable name

```
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details
```

**Cause:** Variable or group name contains invalid characters (hyphens, spaces)

**Solution:** Use underscores instead
```ini
# Wrong
[web-servers]

# Correct
[web_servers]
```

## Inventory Errors

### Error: Could not match supplied host pattern

```
[WARNING]: Could not match supplied host pattern, ignoring: webservers
```

**Cause:** Host group not defined in inventory

**Solution:** Check inventory file
```ini
# inventory/hosts
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
```

### Error: Unable to parse inventory

```
[WARNING]: Unable to parse /path/to/inventory as an inventory source
```

**Cause:** Invalid inventory format

**Solution:** Fix inventory syntax
```ini
# Wrong - mixing styles
[webservers]
web1 ansible_host=192.168.1.10
web2
  ansible_host: 192.168.1.11  # YAML syntax in INI file

# Correct - consistent INI format
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11
```

## Loop Errors

### Error: Invalid data passed to 'loop'

```
fatal: [host]: FAILED! => {"msg": "Invalid data passed to 'loop', it requires a list"}
```

**Cause:** Loop variable is not a list

**Solution:** Ensure loop variable is a list
```yaml
# Wrong
- name: Install packages
  apt:
    name: "{{ item }}"
  loop: nginx  # String, not list

# Correct
- name: Install packages
  apt:
    name: "{{ item }}"
  loop:
    - nginx
    - python3
```

### Error: with_items is deprecated

```
[DEPRECATION WARNING]: with_items is deprecated, use loop instead
```

**Solution:** Replace `with_items` with `loop`
```yaml
# Old style (deprecated)
- name: Install packages
  apt:
    name: "{{ item }}"
  with_items:
    - nginx
    - python3

# New style
- name: Install packages
  apt:
    name: "{{ item }}"
  loop:
    - nginx
    - python3
```

## Handler Errors

### Error: Handler not found

```
ERROR! The requested handler 'restart nginx' was not found
```

**Cause:** Handler name mismatch or handler not defined

**Solution:** Ensure handler name matches exactly
```yaml
# tasks/main.yml
- name: Configure nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx  # Must match handler name exactly

# handlers/main.yml
- name: restart nginx  # Must match notification exactly
  systemd:
    name: nginx
    state: restarted
```

## Include/Import Errors

### Error: Unable to retrieve file contents

```
fatal: [host]: FAILED! => {"msg": "Unable to retrieve file contents. Could not find or access 'file.yml'"}
```

**Cause:** File path incorrect or file doesn't exist

**Solution:** Check file path (relative to playbook location)
```yaml
# Wrong
- include_tasks: tasks/install.yml  # If tasks/ doesn't exist

# Correct
- include_tasks: install.yml  # File in same directory
# Or
- include_tasks: roles/common/tasks/install.yml  # Full path
```

### Error: Include/Import loop detected

```
ERROR! Recursively included/imported file is causing infinite loop
```

**Cause:** Circular dependency (file A includes file B, file B includes file A)

**Solution:** Restructure includes to avoid circular dependencies

## Collection Errors

### Error: couldn't resolve module/action

```
ERROR! couldn't resolve module/action 'community.general.docker_container'
```

**Cause:** Collection not installed

**Solution:** Install required collection
```bash
# Install single collection
ansible-galaxy collection install community.general

# Install from requirements.yml
# requirements.yml
collections:
  - name: community.general
    version: ">=5.0.0"

ansible-galaxy collection install -r requirements.yml
```

### Error: Collection version conflict

```
ERROR! Requirement already satisfied by a different version
```

**Solution:** Update or downgrade collection
```bash
# Force reinstall
ansible-galaxy collection install community.general --force

# Install specific version
ansible-galaxy collection install community.general:5.0.0
```

## Dry-Run / Check Mode Errors

### Error: This module does not support check mode

```
fatal: [host]: FAILED! => {"msg": "This module does not support check mode"}
```

**Cause:** Module doesn't support check mode

**Solution:** Skip check mode for this task
```yaml
- name: Command that doesn't support check mode
  command: /usr/local/bin/custom-script.sh
  check_mode: no  # Always run, even in check mode
```

## Debugging Tips

### Enable Verbose Output

```bash
# Basic verbosity
ansible-playbook playbook.yml -v

# More details
ansible-playbook playbook.yml -vv

# Very verbose (shows module arguments)
ansible-playbook playbook.yml -vvv

# Connection debugging
ansible-playbook playbook.yml -vvvv
```

### Use Debug Module

```yaml
# Print variable
- name: Debug variable
  debug:
    var: my_variable

# Print message
- name: Debug message
  debug:
    msg: "Value is {{ my_variable }}"

# Print all facts
- name: Print all facts
  debug:
    var: ansible_facts

# Conditional debug
- name: Debug when condition met
  debug:
    msg: "Debug message"
  when: ansible_distribution == "Ubuntu"
```

### Use assert Module

```yaml
# Validate conditions
- name: Assert variables are defined
  assert:
    that:
      - app_version is defined
      - app_version | length > 0
      - app_port | int > 0
      - app_port | int < 65536
    fail_msg: "Invalid configuration"
    success_msg: "Configuration validated"
```

## Performance Issues

### Slow Playbook Execution

**Solutions:**
1. Enable SSH pipelining
```ini
# ansible.cfg
[ssh_connection]
pipelining = True
```

2. Use fact caching
```ini
# ansible.cfg
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400
```

3. Disable fact gathering if not needed
```yaml
- hosts: all
  gather_facts: no
```

4. Use async for long tasks
```yaml
- name: Long running task
  command: /usr/bin/long-task
  async: 3600
  poll: 0
```

### High Memory Usage

**Solutions:**
1. Process hosts in batches
```yaml
- hosts: all
  serial: 10  # Process 10 hosts at a time
```

2. Use free strategy
```yaml
- hosts: all
  strategy: free  # Don't wait for all hosts to complete task
```

## Error Prevention Checklist

- [ ] Run yamllint before ansible-playbook
- [ ] Run ansible-lint on all playbooks
- [ ] Use --syntax-check before execution
- [ ] Test with --check mode first
- [ ] Start with limited host scope (--limit)
- [ ] Use tags for incremental testing
- [ ] Enable verbose mode for debugging (-vvv)
- [ ] Validate variables with assert
- [ ] Use molecule for role testing
- [ ] Test in staging before production
- [ ] Keep collections up to date
- [ ] Document custom variables
- [ ] Use version control for all playbooks

## Quick Reference Commands

```bash
# Syntax check
ansible-playbook playbook.yml --syntax-check

# Dry run
ansible-playbook playbook.yml --check --diff

# Run with tags
ansible-playbook playbook.yml --tags webserver

# Limit to specific hosts
ansible-playbook playbook.yml --limit webserver1

# Verbose output
ansible-playbook playbook.yml -vvv

# List tasks
ansible-playbook playbook.yml --list-tasks

# List hosts
ansible-playbook playbook.yml --list-hosts

# Step through tasks
ansible-playbook playbook.yml --step

# Start at specific task
ansible-playbook playbook.yml --start-at-task="Install nginx"
```

---

## Reference: Module_Alternatives

# Ansible Module Alternatives

## Overview

This guide provides replacement alternatives for deprecated or legacy Ansible modules. Use this reference when ansible-lint reports deprecated module warnings or when updating older playbooks to modern best practices.

## Quick Detection

Use the FQCN checker script to automatically detect non-FQCN module usage:

```bash
# Scan a playbook
bash scripts/check_fqcn.sh playbook.yml

# Scan a role
bash scripts/check_fqcn.sh roles/webserver/

# Scan entire directory
bash scripts/check_fqcn.sh .
```

The script identifies modules using short names and provides specific FQCN migration recommendations.

## Deprecated Modules and Replacements

### Package Management

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `apt` (short name) | `ansible.builtin.apt` | Use FQCN for clarity |
| `yum` (short name) | `ansible.builtin.yum` or `ansible.builtin.dnf` | dnf preferred for RHEL 8+ |
| `pip` (short name) | `ansible.builtin.pip` | Use FQCN |
| `easy_install` | `ansible.builtin.pip` | easy_install is deprecated in Python |
| `homebrew` | `community.general.homebrew` | Moved to community.general |
| `zypper` | `community.general.zypper` | Moved to community.general |
| `apk` | `community.general.apk` | Moved to community.general |

### File Operations

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `copy` (short name) | `ansible.builtin.copy` | Use FQCN |
| `file` (short name) | `ansible.builtin.file` | Use FQCN |
| `template` (short name) | `ansible.builtin.template` | Use FQCN |
| `lineinfile` (short name) | `ansible.builtin.lineinfile` | Use FQCN |
| `blockinfile` (short name) | `ansible.builtin.blockinfile` | Use FQCN |
| `synchronize` | `ansible.posix.synchronize` | Moved to ansible.posix |
| `acl` | `ansible.posix.acl` | Moved to ansible.posix |

### Service Management

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `service` (short name) | `ansible.builtin.service` or `ansible.builtin.systemd` | Use systemd for systemd-based systems |
| `systemd` (short name) | `ansible.builtin.systemd` | Use FQCN |
| `sysvinit` | `ansible.builtin.service` | service module handles sysvinit |

### User and Group Management

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `user` (short name) | `ansible.builtin.user` | Use FQCN |
| `group` (short name) | `ansible.builtin.group` | Use FQCN |
| `authorized_key` (short name) | `ansible.posix.authorized_key` | Moved to ansible.posix |

### Networking

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `get_url` (short name) | `ansible.builtin.get_url` | Use FQCN |
| `uri` (short name) | `ansible.builtin.uri` | Use FQCN |
| `iptables` | `ansible.builtin.iptables` | Use FQCN |
| `ufw` | `community.general.ufw` | Moved to community.general |
| `firewalld` | `ansible.posix.firewalld` | Moved to ansible.posix |

### Command Execution

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `command` (short name) | `ansible.builtin.command` | Use FQCN; prefer specific modules |
| `shell` (short name) | `ansible.builtin.shell` | Use FQCN; prefer specific modules |
| `raw` (short name) | `ansible.builtin.raw` | Use FQCN; use only when necessary |
| `script` (short name) | `ansible.builtin.script` | Use FQCN |

### Cloud Providers

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `ec2` | `amazon.aws.ec2_instance` | Use amazon.aws collection |
| `ec2_ami` | `amazon.aws.ec2_ami` | Use amazon.aws collection |
| `ec2_vpc` | `amazon.aws.ec2_vpc_net` | Use amazon.aws collection |
| `azure_rm_*` | `azure.azcollection.*` | Use azure.azcollection |
| `gcp_*` | `google.cloud.*` | Use google.cloud collection |
| `docker_container` | `community.docker.docker_container` | Use community.docker collection |
| `docker_image` | `community.docker.docker_image` | Use community.docker collection |

### Database

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `mysql_db` | `community.mysql.mysql_db` | Use community.mysql collection |
| `mysql_user` | `community.mysql.mysql_user` | Use community.mysql collection |
| `postgresql_db` | `community.postgresql.postgresql_db` | Use community.postgresql collection |
| `postgresql_user` | `community.postgresql.postgresql_user` | Use community.postgresql collection |
| `mongodb_*` | `community.mongodb.*` | Use community.mongodb collection |

### Monitoring and Logging

| Deprecated Module | Replacement | Notes |
|-------------------|-------------|-------|
| `nagios` | `community.general.nagios` | Use community.general collection |
| `zabbix_*` | `community.zabbix.*` | Use community.zabbix collection |

## FQCN Migration

### Why Use Fully Qualified Collection Names (FQCN)?

1. **Clarity**: Explicitly shows which collection provides the module
2. **Conflict Prevention**: Avoids naming conflicts between collections
3. **Future-Proofing**: Prevents breakage when modules move between collections
4. **Best Practice**: Recommended by Ansible for all new playbooks

### Migration Examples

```yaml
# Old style (deprecated)
- name: Install nginx
  apt:
    name: nginx
    state: present

# New style (recommended)
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
```

```yaml
# Old style (deprecated)
- name: Configure firewall
  ufw:
    rule: allow
    port: '443'

# New style (recommended)
- name: Configure firewall
  community.general.ufw:
    rule: allow
    port: '443'
```

## Installing Required Collections

When migrating to FQCN modules, ensure the required collections are installed:

```bash
# Install common collections
ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
ansible-galaxy collection install community.docker
ansible-galaxy collection install community.mysql
ansible-galaxy collection install community.postgresql
ansible-galaxy collection install amazon.aws
ansible-galaxy collection install azure.azcollection
ansible-galaxy collection install google.cloud
```

Or create a `requirements.yml`:

```yaml
---
collections:
  - name: ansible.posix
    version: ">=1.5.0"
  - name: community.general
    version: ">=6.0.0"
  - name: community.docker
    version: ">=3.0.0"
  - name: community.mysql
    version: ">=3.0.0"
  - name: community.postgresql
    version: ">=2.0.0"
```

Then install with:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Checking for Deprecated Modules

Use ansible-lint to identify deprecated modules in your playbooks:

```bash
# Check for deprecated module usage
ansible-lint --profile production playbook.yml

# Show rule documentation for deprecated modules
ansible-lint -L | grep deprecated
```

## Version Compatibility Notes

- **Ansible 2.9**: Last version with many modules in ansible.builtin
- **Ansible 2.10+**: Collections separated from core
- **Ansible 2.12+**: Many deprecated modules removed from core
- **Ansible 2.14+**: FQCN strongly recommended for all modules

## Resources

- [Ansible Collections Index](https://docs.ansible.com/ansible/latest/collections/index.html)
- [Ansible Changelog](https://docs.ansible.com/ansible/latest/porting_guides/porting_guides.html)
- [Community Collections](https://galaxy.ansible.com/)
- [ansible-lint Rules](https://ansible.readthedocs.io/projects/lint/rules/)

---

## Reference: Security_Checklist

# Ansible Security Checklist

## Overview

This checklist provides comprehensive security validation guidelines for Ansible playbooks, roles, and collections. Use this as a reference when reviewing Ansible code for security vulnerabilities.

## Secrets Management

### ❌ Bad Practices

```yaml
# Hardcoded passwords
- name: Create user
  user:
    name: admin
    password: "P@ssw0rd123"  # NEVER DO THIS

# Hardcoded API keys
- name: Configure API
  template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    api_key: "sk-1234567890abcdef"  # NEVER DO THIS

# Credentials in variables
vars:
  db_password: "secret123"  # NEVER DO THIS
  aws_secret_key: "AKIAIOSFODNN7EXAMPLE"  # NEVER DO THIS
```

### ✅ Good Practices

```yaml
# Use Ansible Vault for sensitive data
- name: Create user
  user:
    name: admin
    password: "{{ admin_password | password_hash('sha512') }}"
  no_log: true

# Load vaulted variables
- name: Include vaulted vars
  include_vars:
    file: secrets.yml  # This file is encrypted with ansible-vault

# Use environment variables
- name: Configure API
  template:
    src: config.j2
    dest: /etc/app/config.yml
  environment:
    API_KEY: "{{ lookup('env', 'API_KEY') }}"
  no_log: true

# Use external secret management
- name: Fetch secret from HashiCorp Vault
  set_fact:
    db_password: "{{ lookup('hashi_vault', 'secret=secret/data/db:password') }}"
  no_log: true
```

### Best Practices

1. **Always use Ansible Vault** for sensitive data
   ```bash
   ansible-vault create secrets.yml
   ansible-vault encrypt existing_file.yml
   ```

2. **Never commit unencrypted secrets** to version control

3. **Use `no_log: true`** for tasks handling sensitive data
   ```yaml
   - name: Set database password
     set_fact:
       db_password: "{{ vault_db_password }}"
     no_log: true
   ```

4. **Rotate secrets regularly** and use version control for vault IDs

5. **Use different vault passwords** for different environments

## Privilege Escalation

### ❌ Bad Practices

```yaml
# Running entire playbook as root unnecessarily
- hosts: all
  become: yes
  become_user: root
  tasks:
    - name: Check application status
      command: systemctl status myapp

    - name: Read configuration
      slurp:
        src: /etc/myapp/config.yml

# No privilege escalation when needed
- name: Install package
  apt:
    name: nginx
    state: present
  # This will fail without become
```

### ✅ Good Practices

```yaml
# Only use become when necessary
- hosts: all
  tasks:
    - name: Check application status
      command: systemctl status myapp
      # No become needed for read-only systemctl

    - name: Install package
      apt:
        name: nginx
        state: present
      become: yes
      # Only escalate for this task

    - name: Configure application
      template:
        src: config.j2
        dest: /etc/myapp/config.yml
        owner: myapp
        group: myapp
        mode: '0640'
      become: yes
```

### Best Practices

1. **Principle of least privilege** - only escalate when necessary
2. **Use specific become_user** instead of always root
3. **Limit sudo access** to specific commands in sudoers
4. **Audit all become usage** in playbooks
5. **Use become_flags** carefully and document why

## File Permissions

### ❌ Bad Practices

```yaml
# World-readable sensitive files
- name: Create SSH key
  copy:
    src: id_rsa
    dest: /home/user/.ssh/id_rsa
    mode: '0644'  # WRONG: Private key readable by all

# No mode specified
- name: Create config file
  template:
    src: database.conf.j2
    dest: /etc/app/database.conf
  # Missing mode - depends on umask

# Overly permissive
- name: Create script
  copy:
    src: deploy.sh
    dest: /usr/local/bin/deploy.sh
    mode: '0777'  # WRONG: World writable
```

### ✅ Good Practices

```yaml
# Appropriate permissions for private keys
- name: Create SSH key
  copy:
    src: id_rsa
    dest: /home/user/.ssh/id_rsa
    owner: user
    group: user
    mode: '0600'

# Explicit permissions for config files
- name: Create config file
  template:
    src: database.conf.j2
    dest: /etc/app/database.conf
    owner: appuser
    group: appgroup
    mode: '0640'

# Minimal necessary permissions
- name: Create script
  copy:
    src: deploy.sh
    dest: /usr/local/bin/deploy.sh
    owner: root
    group: root
    mode: '0755'

# Set directory permissions properly
- name: Create secure directory
  file:
    path: /etc/app/secrets
    state: directory
    owner: appuser
    group: appgroup
    mode: '0750'
```

### Permission Guidelines

| File Type | Recommended Mode | Owner | Group |
|-----------|-----------------|-------|-------|
| Private keys | 0600 | user | user |
| Public keys | 0644 | user | user |
| Config files (sensitive) | 0640 | app | app |
| Config files (public) | 0644 | app | app |
| Executables | 0755 | root | root |
| Directories (sensitive) | 0750 | app | app |
| Directories (public) | 0755 | app | app |
| Log files | 0640 | app | app |

## Command Injection Prevention

### ❌ Bad Practices

```yaml
# Unvalidated user input in commands
- name: Process user file
  shell: "cat {{ user_provided_filename }}"
  # VULNERABLE: User could provide "; rm -rf /"

# Direct variable interpolation
- name: Search logs
  command: "grep {{ search_term }} /var/log/app.log"
  # VULNERABLE: User could inject commands

# Using shell when not needed
- name: Create directory
  shell: "mkdir -p {{ directory_name }}"
  # RISKY: Use file module instead
```

### ✅ Good Practices

```yaml
# Use quote filter for variables in shell
- name: Process user file
  shell: "cat {{ user_provided_filename | quote }}"
  when: user_provided_filename is match('^[a-zA-Z0-9._-]+$')

# Better: Use modules instead of shell/command
- name: Create directory
  file:
    path: "{{ directory_name }}"
    state: directory
    mode: '0755'

# Validate input before use
- name: Search logs
  command: "grep {{ search_term }} /var/log/app.log"
  when:
    - search_term is defined
    - search_term | length > 0
    - search_term is match('^[a-zA-Z0-9 ]+$')
  args:
    warn: false

# Use args for command parameters
- name: Run script with arguments
  command: /usr/local/bin/script.sh
  args:
    stdin: "{{ user_input }}"
```

### Best Practices

1. **Prefer modules over command/shell** whenever possible
2. **Always use quote filter** for variables in shell commands
3. **Validate input** with regex patterns
4. **Use whitelist validation** not blacklist
5. **Never trust user input** without validation

## Network Security

### ❌ Bad Practices

```yaml
# Unencrypted protocols
- name: Download file
  get_url:
    url: http://example.com/file.tar.gz  # WRONG: HTTP not HTTPS
    dest: /tmp/file.tar.gz

# Disabled SSL verification
- name: Call API
  uri:
    url: https://api.example.com/data
    validate_certs: no  # WRONG: Disables security

# Exposing on all interfaces unnecessarily
- name: Configure service
  template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    bind_address: "0.0.0.0"  # RISKY: Expose to all
```

### ✅ Good Practices

```yaml
# Use HTTPS
- name: Download file
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    checksum: sha256:abc123...

# Validate SSL certificates
- name: Call API
  uri:
    url: https://api.example.com/data
    validate_certs: yes
    client_cert: /path/to/cert.pem
    client_key: /path/to/key.pem

# Bind to specific interface
- name: Configure service
  template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    bind_address: "127.0.0.1"  # Localhost only

# Use firewall rules
- name: Configure firewall
  ufw:
    rule: allow
    port: '443'
    proto: tcp
    src: '10.0.0.0/8'  # Only from internal network
```

### Best Practices

1. **Always use HTTPS** for external communications
2. **Validate SSL certificates** - only disable for testing
3. **Bind services to specific interfaces** when possible
4. **Use firewall rules** to restrict access
5. **Encrypt sensitive data in transit** (TLS/SSL)

## SELinux and AppArmor

### Best Practices

```yaml
# Don't disable SELinux
- name: Configure SELinux
  selinux:
    policy: targeted
    state: enforcing  # Not permissive or disabled

# Set proper SELinux contexts
- name: Set SELinux context for web content
  sefcontext:
    target: '/web/content(/.*)?'
    setype: httpd_sys_content_t
    state: present

- name: Apply SELinux context
  command: restorecon -Rv /web/content

# Manage AppArmor profiles
- name: Load AppArmor profile
  command: apparmor_parser -r /etc/apparmor.d/usr.bin.myapp
```

## Audit and Logging

### Best Practices

```yaml
# Log security-relevant actions
- name: Create admin user
  user:
    name: admin
    groups: sudo
    state: present
  register: admin_user_result

- name: Log user creation
  lineinfile:
    path: /var/log/ansible-changes.log
    line: "{{ ansible_date_time.iso8601 }} - Admin user created by {{ ansible_user_id }}"
    create: yes
  when: admin_user_result.changed

# Use tags for security-related tasks
- name: Configure SSH
  template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
  tags:
    - security
    - ssh
```

## Security Validation Checklist

Before running playbooks in production, verify:

- [ ] No hardcoded secrets (passwords, API keys, tokens)
- [ ] All sensitive data encrypted with Ansible Vault
- [ ] `no_log: true` used for tasks handling secrets
- [ ] Privilege escalation only where necessary
- [ ] File permissions explicitly set (not relying on umask)
- [ ] Private keys have mode 0600
- [ ] No world-writable files or directories
- [ ] Input validation for user-provided variables
- [ ] Using modules instead of shell/command where possible
- [ ] Quote filter used for variables in shell commands
- [ ] HTTPS used instead of HTTP
- [ ] SSL certificate validation enabled
- [ ] Services bound to specific interfaces, not 0.0.0.0
- [ ] Firewall rules configured appropriately
- [ ] SELinux/AppArmor not disabled
- [ ] Security contexts set correctly
- [ ] Security-relevant actions logged
- [ ] Regular security updates applied
- [ ] Unused packages removed
- [ ] Default credentials changed
- [ ] Unnecessary services disabled

## Tools for Security Scanning

1. **ansible-lint** - Includes security-focused rules
   ```bash
   ansible-lint --profile security playbook.yml
   ```

2. **Ansible Galaxy Security Scan**
   ```bash
   ansible-galaxy collection scan namespace.collection
   ```

3. **Git-secrets** - Prevent committing secrets
   ```bash
   git secrets --scan
   ```

4. **Trivy** - Scan for vulnerabilities
   ```bash
   trivy config .
   ```

## Additional Resources

- [Ansible Security Automation](https://www.ansible.com/use-cases/security-automation)
- [Ansible Best Practices - Security](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
