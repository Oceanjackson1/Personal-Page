---
title: "Ansible Generator"
description: "Generate, create, or scaffold Ansible playbooks, roles, tasks, handlers, inventory, vars."
category: "devops"
source: "community"
author: "Community"
tags: ["ansible", "generator"]
date: 2026-03-20
---

# Ansible Generator

## Trigger Phrases

Use this skill when the request is to generate or scaffold Ansible content, for example:

- "Create a playbook to deploy nginx with TLS."
- "Generate an Ansible role for PostgreSQL backups."
- "Write inventory files for prod and staging."
- "Build reusable Ansible tasks for user provisioning."
- "Initialize an Ansible project with ansible.cfg and requirements.yml."
- "Give me a quick Ansible snippet to install Docker."

Do not use this skill as the primary workflow when the request is validation/debug-only (syntax errors, lint failures, Molecule/test failures). Use `ansible-validator` for those cases.

## Deterministic Execution Flow

Run these stages in order. Do not skip a stage unless the `Validation Exceptions Matrix` explicitly allows it.

### Stage 0: Classify Request Mode

Determine one mode first:

| Mode | Typical user intent | Deliverable |
| --- | --- | --- |
| `full-generation` | "create/build/generate" a full playbook/role/inventory/project file set | Complete file(s), production-ready |
| `snippet-only` | "quick snippet/example" without full file context | Focused task/play snippet |
| `docs-only` | explanation, pattern comparison, or conceptual guidance only | Explanatory content, optional examples |

### Stage 1: Collect Minimum Inputs

If details are missing, ask briefly. If the user does not provide them, proceed with safe defaults and state assumptions.

| Resource type | Required inputs | Safe defaults if missing |
| --- | --- | --- |
| Playbook | target hosts, privilege (`become`), OS family, objective | `hosts: all`, `become: false`, OS-agnostic modules |
| Role | role name, primary service/package, supported OS | role name from task domain, Debian + RedHat vars |
| Tasks file | operation scope, required vars, execution context | standalone reusable tasks with documented vars |
| Inventory | environments, host groups, hostnames/IPs | `production`/`staging` groups with placeholders |
| Project config | collections/roles dependencies, lint policy | minimal `ansible.cfg`, `requirements.yml`, `.ansible-lint` |

### Stage 2: Reference Extraction Checklist

Before drafting content, extract the following from local references/templates.

#### Required references

- `references/best-practices.md`
  - Extract: FQCN requirements, idempotency rules, naming, security expectations.
- `references/module-patterns.md`
  - Extract: correct module/parameter patterns for the exact task type.

#### Required templates by output type

- Playbook: `assets/templates/playbook/basic_playbook.yml`
- Role: `assets/templates/role/` (including `meta/argument_specs.yml` and `molecule/default/` for test scaffolding)
- Inventory (INI): `assets/templates/inventory/hosts`
- Inventory (YAML): `assets/templates/inventory/hosts.yml`
- Project config: `assets/templates/project/ansible.cfg`, `assets/templates/project/requirements.yml`, `assets/templates/project/.ansible-lint`

#### Extraction checks

- Identify every `[PLACEHOLDER]` that must be replaced.
- Decide module selection priority (`ansible.builtin.*` first).
- Capture at least one OS-appropriate package pattern when OS-specific behavior is needed.
- Capture required prerequisites (collections, binaries, target assumptions).

### Stage 3: Generate

Apply these generation standards:

1. Use FQCN module names (`ansible.builtin.*` first choice).
2. Keep tasks idempotent (`state`, `creates/removes`, `changed_when` when needed).
3. Use descriptive verb-first task names.
4. Use `true`/`false` booleans (not `yes`/`no`).
5. Add `no_log: true` for sensitive values.
6. Replace all placeholders before presenting output.
7. Prefer `ansible.builtin.dnf` for RHEL 8+/CentOS 8+ (legacy `yum` only for older systems).

### Stage 4: Validate (Default) or Apply Exception (Fallback)

Use the matrix below to keep validation deterministic and non-blocking.

## Validation Exceptions Matrix

| Scenario | Default behavior | Allowed fallback | What to report |
| --- | --- | --- | --- |
| `full-generation` | Run `ansible-validator` after generation and after each fix pass | If validator/tools are unavailable, run manual static checks (YAML shape, placeholder scan, FQCN/idempotency/security review) and provide exact deferred validation commands | Explicitly list which checks ran, which were skipped, and why |
| `snippet-only` | Skip full validator by default; do inline sanity checks | Run full validator only if user asks or snippet is promoted to full file | State that validation was limited because output is snippet-only |
| `docs-only` | No runtime validation | None needed | State that no executable artifact was generated |
| Offline environment (no web/docs access) | Continue with local references and templates | Skip external doc lookups; prefer builtin-module implementations; provide notes for later external verification | State offline constraint and impacted checks/lookups |

## Resource Generation Guidance

### Playbooks

- Use `assets/templates/playbook/basic_playbook.yml` as structure.
- Include: header comments, `pre_tasks`/`tasks`/`post_tasks` as needed, handlers, tags.
- Add health checks when service deployment/configuration is involved.

### Roles

- Build from `assets/templates/role/` structure.
- Keep defaults in `defaults/main.yml`; keep higher-priority role vars in `vars/main.yml`.
- Include OS-specific vars (`vars/Debian.yml`, `vars/RedHat.yml`) when relevant.
- Add `meta/argument_specs.yml` for variable validation.
- Include `molecule/default/` scaffold (from `assets/templates/role/molecule/`) for production-ready roles.

### Task Files

- Keep scope narrow and reusable.
- Document required input variables in comments.
- Use conditionals for environment/OS-sensitive operations.

### Inventory

- Build logical host groups and optional group hierarchies.
- Use variable layering intentionally: `group_vars/all.yml` -> group -> host.
- Default to INI format (`hosts`) for simple topologies; use YAML format (`hosts.yml`) when the user requests it or when the hierarchy is complex.

### Project Configuration

- Provide baseline `ansible.cfg`, `requirements.yml`, and `.ansible-lint`.
- Keep defaults practical and editable.

## Custom Modules and Collections

When the request depends on non-builtin modules/collections:

1. Identify collection + module and required version sensitivity.
2. Check local `references/module-patterns.md` first.
3. If still unresolved and network/tools are available, query Context7:
   - `mcp__context7__resolve-library-id`
   - `mcp__context7__query-docs`
4. If Context7 is unavailable, use official Ansible docs / Ansible Galaxy pages.
5. If external lookup is unavailable, provide a builtin fallback approach and state the limitation.

Always include collection installation guidance when collection modules are used.

## Canonical Example Flows

### Flow A: Full Generation (Playbook)

User prompt: "Create a playbook to deploy nginx with TLS on Ubuntu and RHEL."

1. Classify as `full-generation`.
2. Gather/confirm required inputs (hosts, cert paths, become, service name).
3. Extract required references (`best-practices.md`, `module-patterns.md`) and playbook template.
4. Generate complete playbook with OS conditionals (`apt`/`dnf`), handlers, validation for config templates.
5. Run `ansible-validator`.
6. Fix issues and rerun until checks pass (or apply matrix fallback if tooling unavailable).
7. Present output with validation summary, usage command, and prerequisites.

### Flow B: Quick Snippet (Task Block)

User prompt: "Give me a snippet to create a user and SSH key."

1. Classify as `snippet-only`.
2. Extract minimal module patterns for `ansible.builtin.user` and `ansible.builtin.authorized_key`.
3. Generate concise snippet with FQCN, idempotency, and variable placeholders.
4. Perform inline sanity checks (YAML shape, FQCN, obvious idempotency/security).
5. Present snippet and note that full validator run was skipped due to snippet-only mode.

## Output Requirements

For generated executable artifacts, use this response structure:

```markdown
## Generated [Resource Type]: [Name]

**Validation Status:** [Passed / Partially validated / Skipped with reason]
- YAML syntax: [status]
- Ansible syntax: [status]
- Lint: [status]

**Summary:**
- [What was generated]
- [Key implementation choices]

**Assumptions:**
- [Defaults or inferred values]

**Usage:**
```bash
[Exact command(s)]
```

**Prerequisites:**
- [Collections, binaries, environment needs]
```

## Done Criteria

This skill execution is complete only when all applicable items are true:

- Trigger decision is explicit (`full-generation`, `snippet-only`, or `docs-only`).
- Required references/templates were consulted for the selected artifact type.
- Generated output has no unresolved placeholders.
- Validation followed default behavior or a documented exception from the matrix.
- Any skipped checks include a concrete reason and deferred command(s).
- Final output includes summary, assumptions, usage, and prerequisites.

---

## Reference: Best Practices

# Ansible Best Practices

## Directory Structure

### Standard Playbook Structure
```
playbook.yml
roles/
  common/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
    files/
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
inventory/
  production/
    hosts
    group_vars/
    host_vars/
  staging/
    hosts
    group_vars/
    host_vars/
```

### Role Structure
Each role should have:
- `tasks/main.yml` - Main task list
- `handlers/main.yml` - Handlers triggered by tasks
- `templates/` - Jinja2 templates
- `files/` - Static files to copy
- `vars/main.yml` - Role-specific variables (high priority)
- `defaults/main.yml` - Default variables (low priority, overridable)
- `meta/main.yml` - Role dependencies and metadata

## Naming Conventions

### Files and Directories
- Use lowercase with underscores: `install_nginx.yml`, `backup_database.yml`
- Playbook files: descriptive names ending in `.yml`
- Role names: short, descriptive, lowercase with underscores

### Variables
- Use descriptive names: `nginx_port`, `db_backup_dir`, `app_version`
- Prefix role-specific variables with role name: `nginx_worker_processes`
- Use snake_case, not camelCase or kebab-case
- Group related variables with common prefixes

### Tasks
- Use descriptive names that explain what the task does
- Start with a verb: "Install nginx", "Copy configuration file", "Start service"

## Task Writing Best Practices

### Always Use State Declaration
```yaml
# Good
- name: Ensure nginx is installed
  ansible.builtin.package:
    name: nginx
    state: present

# Bad
- name: Install nginx
  ansible.builtin.package:
    name: nginx
```

### Use Fully Qualified Collection Names (FQCN)
```yaml
# Good - FQCN (Ansible 2.10+)
- name: Copy configuration file
  ansible.builtin.copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf

# Avoid - Short names (deprecated)
- name: Copy configuration file
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
```

### Idempotency
- All tasks should be idempotent (safe to run multiple times)
- Use `state: present/absent` instead of imperative commands
- Avoid using `command` or `shell` modules when builtin modules exist
- When using `command`/`shell`, use `creates`, `removes`, or `changed_when`

```yaml
# Good - idempotent
- name: Create directory
  ansible.builtin.file:
    path: /opt/app
    state: directory
    mode: '0755'

# Bad - not idempotent
- name: Create directory
  ansible.builtin.command: mkdir -p /opt/app
```

### Error Handling
```yaml
- name: Attempt to start service
  ansible.builtin.service:
    name: myapp
    state: started
  register: service_result
  failed_when: false
  changed_when: service_result.rc == 0

- name: Handle service failure
  ansible.builtin.debug:
    msg: "Service failed to start: {{ service_result.msg }}"
  when: service_result.failed
```

## Variables and Facts

### Variable Precedence (High to Low)
1. Extra vars (`-e` in CLI)
2. Task vars
3. Block vars
4. Role and include vars
5. Set_facts / registered vars
6. Play vars
7. Play vars_files
8. Role defaults
9. Inventory vars (host_vars, group_vars)

### Using Variables
```yaml
# Use default values
- name: Set port with default
  ansible.builtin.set_fact:
    app_port: "{{ custom_port | default(8080) }}"

# Combine variables
- name: Create full path
  ansible.builtin.set_fact:
    config_path: "{{ base_dir }}/{{ app_name }}/config.yml"
```

## Conditionals and Loops

### When Statements
```yaml
- name: Install on Debian-based systems
  ansible.builtin.apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

- name: Install on RedHat-based systems (RHEL 8+)
  ansible.builtin.dnf:
    name: nginx
    state: present
  when: ansible_os_family == "RedHat"
```

### Loops
```yaml
# Good - using loop
- name: Install packages
  ansible.builtin.package:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - postgresql
    - redis

# Complex loop with dict
- name: Create users
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { name: 'alice', groups: 'admin,developers' }
    - { name: 'bob', groups: 'developers' }
```

## Handlers

### Naming and Usage
```yaml
# In tasks/main.yml
- name: Copy nginx configuration
  ansible.builtin.copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx

# In handlers/main.yml
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
```

### Handler Best Practices
- Handlers run once at the end of a play
- Use descriptive names
- Listen to multiple notifications with same handler name
- Use `meta: flush_handlers` to run handlers immediately if needed

## Templates

### Jinja2 Templates
```yaml
# Task
- name: Deploy configuration from template
  ansible.builtin.template:
    src: app_config.j2
    dest: /etc/app/config.yml
    mode: '0644'
    backup: true
```

```jinja2
# Template file: templates/app_config.j2
server:
  port: {{ app_port }}
  host: {{ ansible_default_ipv4.address }}

database:
  host: {{ db_host }}
  port: {{ db_port | default(5432) }}
  name: {{ db_name }}

{% if enable_ssl %}
ssl:
  enabled: true
  cert: {{ ssl_cert_path }}
  key: {{ ssl_key_path }}
{% endif %}
```

## Advanced Jinja2 Templating

### Common Filters

#### Data Format Conversion
```yaml
- name: Convert to JSON
  ansible.builtin.copy:
    content: "{{ my_dict | to_json }}"
    dest: /tmp/config.json

- name: Convert to YAML
  ansible.builtin.copy:
    content: "{{ my_dict | to_yaml }}"
    dest: /tmp/config.yml

- name: Convert to pretty JSON
  ansible.builtin.copy:
    content: "{{ my_dict | to_nice_json }}"
    dest: /tmp/config.json

# Parse JSON/YAML strings
- name: Parse JSON string
  ansible.builtin.set_fact:
    parsed_data: "{{ json_string | from_json }}"

- name: Parse YAML string
  ansible.builtin.set_fact:
    parsed_data: "{{ yaml_string | from_yaml }}"
```

#### String Manipulation
```yaml
# Regex operations
- name: Replace text
  ansible.builtin.set_fact:
    new_string: "{{ original | regex_replace('^old', 'new') }}"

- name: Extract with regex
  ansible.builtin.set_fact:
    extracted: "{{ text | regex_search('version: (\\d+\\.\\d+)', '\\1') }}"

# Case conversion
- name: Convert case
  ansible.builtin.set_fact:
    upper: "{{ text | upper }}"
    lower: "{{ text | lower }}"
    title: "{{ text | title }}"

# String operations
- name: String operations
  ansible.builtin.set_fact:
    trimmed: "{{ '  text  ' | trim }}"
    replaced: "{{ text | replace('old', 'new') }}"
    split_list: "{{ 'a,b,c' | split(',') }}"
    joined: "{{ ['a', 'b', 'c'] | join('-') }}"
```

#### Hashing and Encoding
```yaml
# Hash values
- name: Generate hashes
  ansible.builtin.set_fact:
    md5_hash: "{{ 'mystring' | hash('md5') }}"
    sha256_hash: "{{ 'mystring' | hash('sha256') }}"

# Password hashing
- name: Hash password
  ansible.builtin.user:
    name: myuser
    password: "{{ user_password | password_hash('sha512', 'mysecretsalt') }}"

# Encoding
- name: Encode/decode
  ansible.builtin.set_fact:
    base64_encoded: "{{ 'text' | b64encode }}"
    base64_decoded: "{{ encoded_value | b64decode }}"
    url_encoded: "{{ url_string | urlencode }}"
```

#### List and Dict Operations
```yaml
# List operations
- name: List operations
  ansible.builtin.set_fact:
    unique_items: "{{ my_list | unique }}"
    sorted_items: "{{ my_list | sort }}"
    first_item: "{{ my_list | first }}"
    last_item: "{{ my_list | last }}"
    list_length: "{{ my_list | length }}"
    flattened: "{{ nested_list | flatten }}"

# Dict operations
- name: Dict operations
  ansible.builtin.set_fact:
    dict_keys: "{{ my_dict | dict2items }}"
    dict_values: "{{ my_dict | list }}"
    combined: "{{ dict1 | combine(dict2) }}"

# Extract values
- name: Extract from list of dicts
  ansible.builtin.set_fact:
    names: "{{ users | map(attribute='name') | list }}"
    ids: "{{ items | map(attribute='id') | list }}"
```

#### Network Filters
```yaml
# IP address operations (requires netaddr Python package)
- name: IP operations
  ansible.builtin.set_fact:
    is_valid: "{{ ip_address | ipaddr }}"
    network: "{{ ip_address | ipaddr('network') }}"
    netmask: "{{ ip_address | ipaddr('netmask') }}"
    broadcast: "{{ ip_address | ipaddr('broadcast') }}"
    host_ip: "{{ ip_address | ipaddr('address') }}"

# CIDR operations
- name: CIDR operations
  ansible.builtin.set_fact:
    hosts_in_network: "{{ '192.168.1.0/24' | ipaddr('size') }}"
    first_host: "{{ '192.168.1.0/24' | ipaddr('1') | ipaddr('address') }}"
```

#### File and Math Filters
```yaml
# File size formatting
- name: Format file size
  ansible.builtin.debug:
    msg: "File size: {{ file_stat.stat.size | filesizeformat }}"

# Math operations
- name: Math operations
  ansible.builtin.set_fact:
    sum: "{{ [1, 2, 3] | sum }}"
    min: "{{ [5, 2, 8] | min }}"
    max: "{{ [5, 2, 8] | max }}"
    rounded: "{{ 3.14159 | round(2) }}"
    absolute: "{{ -42 | abs }}"
```

#### Default and Mandatory Values
```yaml
# Provide defaults
- name: Use default values
  ansible.builtin.set_fact:
    port: "{{ custom_port | default(8080) }}"
    config: "{{ app_config | default({}) }}"

# Nested defaults (Ansible 2.8+)
- name: Nested default
  ansible.builtin.set_fact:
    value: "{{ foo.bar.baz | default('fallback') }}"

# Mandatory values
- name: Require variable
  ansible.builtin.set_fact:
    required_value: "{{ must_be_defined | mandatory }}"
```

### Lookup Plugins

#### File and Environment Lookups
```yaml
# Read file content
- name: Read SSH public key
  ansible.builtin.authorized_key:
    user: deploy
    key: "{{ lookup('file', '/home/user/.ssh/id_rsa.pub') }}"

# Environment variables
- name: Get environment variable
  ansible.builtin.set_fact:
    home_dir: "{{ lookup('env', 'HOME') }}"
    path: "{{ lookup('env', 'PATH') }}"

# Pipe command output
- name: Get command output
  ansible.builtin.set_fact:
    current_date: "{{ lookup('pipe', 'date +%Y-%m-%d') }}"
    git_commit: "{{ lookup('pipe', 'git rev-parse HEAD') }}"
```

#### Template and URL Lookups
```yaml
# Template lookup
- name: Inline template
  ansible.builtin.set_fact:
    greeting: "{{ lookup('template', 'greeting.j2') }}"

# URL content
- name: Fetch URL content
  ansible.builtin.set_fact:
    remote_content: "{{ lookup('url', 'https://api.example.com/config') }}"
```

#### Password and Random Lookups
```yaml
# Generate random password
- name: Generate password
  ansible.builtin.set_fact:
    random_password: "{{ lookup('password', '/dev/null length=32 chars=ascii_letters,digits') }}"

# Random choice
- name: Pick random item
  ansible.builtin.set_fact:
    random_server: "{{ lookup('random_choice', ['server1', 'server2', 'server3']) }}"
```

#### Query vs Lookup
```yaml
# lookup returns comma-separated string
- name: Using lookup
  ansible.builtin.debug:
    msg: "{{ lookup('file', 'file1.txt', 'file2.txt') }}"
  # Returns: "content1,content2"

# query always returns list
- name: Using query
  ansible.builtin.debug:
    msg: "{{ query('file', 'file1.txt', 'file2.txt') }}"
  # Returns: ["content1", "content2"]

# Prefer query for loops
- name: Loop with query
  ansible.builtin.debug:
    msg: "{{ item }}"
  loop: "{{ query('inventory_hostnames', 'all') }}"
```

### Template Control Structures

#### Loops in Templates
```jinja2
{# templates/config.j2 #}
# User list
{% for user in users %}
user {{ user.name }}:
  uid: {{ user.uid }}
  groups: {{ user.groups | join(',') }}
{% endfor %}

# Conditional in loop
{% for item in items if item.enabled %}
  - {{ item.name }}: {{ item.value }}
{% endfor %}

# Loop with index
{% for server in servers %}
server_{{ loop.index }}: {{ server.hostname }}
{% endfor %}
```

#### Conditionals in Templates
```jinja2
{# templates/app_config.j2 #}
{% if environment == 'production' %}
log_level: warning
max_connections: 1000
{% elif environment == 'staging' %}
log_level: info
max_connections: 500
{% else %}
log_level: debug
max_connections: 100
{% endif %}

# Complex conditions
{% if ansible_os_family == 'Debian' and ansible_distribution_major_version|int >= 20 %}
use_modern_config: true
{% endif %}

# Check if defined
{% if custom_setting is defined %}
custom_setting: {{ custom_setting }}
{% endif %}

# Check if none
{% if database_host is none %}
database_host: localhost
{% else %}
database_host: {{ database_host }}
{% endif %}
```

#### Whitespace Control
```jinja2
{# Remove whitespace before #}
{%- if condition %}
content
{% endif %}

{# Remove whitespace after #}
{% if condition -%}
content
{% endif %}

{# Remove both #}
{%- if condition -%}
content
{%- endif -%}
```

#### Macros and Includes
```jinja2
{# Define macro #}
{% macro render_user(name, uid) -%}
user: {{ name }}
uid: {{ uid }}
{%- endmacro %}

{# Use macro #}
{{ render_user('alice', 1000) }}
{{ render_user('bob', 1001) }}

{# Include other template #}
{% include 'header.j2' %}

{# Import macros from other template #}
{% from 'macros.j2' import render_user %}
```

### Advanced Template Patterns

#### Multi-line Strings
```jinja2
server {
    listen 80;
    server_name {{ server_name }};

    {% if ssl_enabled %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
    {% endif %}

    location / {
        proxy_pass http://{{ backend_host }}:{{ backend_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Complex Data Structures
```jinja2
{# Nested loops for complex config #}
{% for service in services %}
[{{ service.name }}]
{% for key, value in service.config.items() %}
{{ key }} = {{ value }}
{% endfor %}

{% endfor %}

{# Generate from dict #}
{% for key, value in app_settings.items() %}
export {{ key | upper }}="{{ value }}"
{% endfor %}
```

## Security Best Practices

### Sensitive Data
```yaml
# Use no_log for sensitive operations
- name: Set database password
  ansible.builtin.user:
    name: dbadmin
    password: "{{ db_password | password_hash('sha512') }}"
  no_log: true

# Use ansible-vault for secrets
# Encrypt with: ansible-vault encrypt secrets.yml
# Include encrypted vars
- name: Include vault variables
  ansible.builtin.include_vars:
    file: secrets.yml
```

### File Permissions
```yaml
- name: Copy sensitive file
  ansible.builtin.copy:
    src: private_key
    dest: /etc/ssl/private/app.key
    mode: '0600'
    owner: root
    group: root
```

## Tags

### Using Tags
```yaml
- name: Install packages
  ansible.builtin.package:
    name: nginx
    state: present
  tags:
    - packages
    - nginx
    - install

# Run with: ansible-playbook playbook.yml --tags "install"
# Skip with: ansible-playbook playbook.yml --skip-tags "install"
```

### Tag Categories
- `install` - Installation tasks
- `configure` - Configuration tasks
- `update` - Update tasks
- `backup` - Backup tasks
- `always` - Always run (special tag)
- `never` - Never run unless explicitly called (special tag)

## Playbook Structure

### Complete Playbook Example
```yaml
---
- name: Deploy web application
  hosts: webservers
  become: true
  vars:
    app_version: "1.2.3"
    app_port: 8080

  pre_tasks:
    - name: Update package cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  roles:
    - common
    - nginx
    - application

  post_tasks:
    - name: Verify application is running
      ansible.builtin.uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      register: health_check
      until: health_check.status == 200
      retries: 5
      delay: 10

  handlers:
    - name: Restart application
      ansible.builtin.service:
        name: myapp
        state: restarted
```

## Testing and Validation

### Check Mode (Dry Run)
```yaml
# Run in check mode
ansible-playbook playbook.yml --check

# Task that always runs in check mode
- name: Get service status
  ansible.builtin.command: systemctl status nginx
  check_mode: false
  changed_when: false
```

### Diff Mode
```yaml
# Show differences
ansible-playbook playbook.yml --check --diff
```

### Assert and Validate
```yaml
- name: Verify configuration
  ansible.builtin.assert:
    that:
      - ansible_distribution in ['Ubuntu', 'Debian', 'CentOS', 'RedHat']
      - app_port | int > 0
      - app_port | int < 65536
    fail_msg: "Invalid configuration"
    success_msg: "Configuration validated"
```

## Performance Optimization

### Gathering Facts
```yaml
# Disable fact gathering when not needed
- name: Quick task
  hosts: all
  gather_facts: false
  tasks:
    - name: Ping hosts
      ansible.builtin.ping:

# Gather specific facts
- name: Gather minimal facts
  hosts: all
  gather_facts: true
  gather_subset:
    - '!all'
    - '!min'
    - network
```

### Parallelism
```yaml
# Set forks in ansible.cfg or via CLI
# ansible-playbook playbook.yml --forks 20

# Control serial execution
- name: Rolling update
  hosts: webservers
  serial: 2  # Update 2 hosts at a time
```

### Async Tasks
```yaml
- name: Long running task
  ansible.builtin.command: /opt/long_running_script.sh
  async: 3600  # Maximum runtime
  poll: 0  # Fire and forget
  register: long_task

- name: Check on long task
  ansible.builtin.async_status:
    jid: "{{ long_task.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 30
  delay: 10
```

## Documentation

### Playbook Documentation
```yaml
---
# playbook.yml
# Description: Deploy and configure web application
# Requirements:
#   - Ansible 2.10+
#   - Target hosts: Ubuntu 20.04+ or RHEL 8+
# Variables:
#   - app_version: Application version to deploy (required)
#   - app_port: Port for application (default: 8080)
#   - enable_ssl: Enable SSL/TLS (default: false)
# Usage:
#   ansible-playbook -i inventory/production playbook.yml -e "app_version=1.2.3"
```

### Role Documentation (meta/main.yml)
```yaml
---
galaxy_info:
  role_name: nginx
  author: Your Name
  description: Install and configure nginx
  license: MIT
  min_ansible_version: 2.10
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: EL
      versions:
        - 8
        - 9
  galaxy_tags:
    - web
    - nginx

dependencies: []
```

## Common Pitfalls to Avoid

1. **Not using FQCN** - Always use fully qualified collection names
2. **Hard-coded values** - Use variables for configuration
3. **Not handling different OS** - Check `ansible_os_family` or `ansible_distribution`
4. **Ignoring idempotency** - Tasks should be safe to run multiple times
5. **Not using handlers** - Restart services via handlers, not direct tasks
6. **Sensitive data in plain text** - Use ansible-vault for secrets
7. **Not using tags** - Tags enable selective execution
8. **Not validating** - Always run with `--check` first
9. **Complex logic in playbooks** - Move complex logic to roles
10. **Not documenting variables** - Document required and optional vars

## Module Selection Priority

1. **Builtin modules first**: Use `ansible.builtin.*` modules when available
2. **Collection modules**: Use official collection modules (e.g., `community.general.*`)
3. **Custom modules**: Only when no suitable module exists
4. **Avoid `command`/`shell`**: Use specific modules instead of raw commands

---

## Reference: Module Patterns

# Common Ansible Module Usage Patterns

## Core Modules (ansible.builtin)

### Package Management

#### ansible.builtin.package (Universal)
```yaml
- name: Install package (OS-agnostic)
  ansible.builtin.package:
    name: nginx
    state: present
```

#### ansible.builtin.apt (Debian/Ubuntu)
```yaml
- name: Install package with apt
  ansible.builtin.apt:
    name: nginx
    state: present
    update_cache: true
    cache_valid_time: 3600

- name: Install specific version
  ansible.builtin.apt:
    name: nginx=1.18.0-0ubuntu1
    state: present

- name: Install multiple packages
  ansible.builtin.apt:
    name:
      - nginx
      - postgresql
      - redis-server
    state: present
```

#### ansible.builtin.dnf (RHEL 8+/CentOS 8+) - Recommended
```yaml
# NOTE: Use ansible.builtin.dnf for RHEL 8+ and CentOS 8+
# ansible.builtin.yum is deprecated in favor of dnf for modern RHEL systems

- name: Install package with dnf
  ansible.builtin.dnf:
    name: nginx
    state: present
    update_cache: true

- name: Install from specific repository
  ansible.builtin.dnf:
    name: nginx
    state: present
    enablerepo: epel

- name: Install multiple packages
  ansible.builtin.dnf:
    name:
      - nginx
      - postgresql
      - redis
    state: present
```

#### ansible.builtin.yum (RHEL 7/CentOS 7 - Legacy)
```yaml
# NOTE: Only use for RHEL 7/CentOS 7 systems
# For RHEL 8+ use ansible.builtin.dnf instead

- name: Install package with yum (legacy systems)
  ansible.builtin.yum:
    name: nginx
    state: present
    update_cache: true

- name: Install from specific repository (legacy)
  ansible.builtin.yum:
    name: nginx
    state: present
    enablerepo: epel
```

### File Operations

#### ansible.builtin.file
```yaml
# Create directory
- name: Create directory
  ansible.builtin.file:
    path: /opt/app/config
    state: directory
    mode: '0755'
    owner: appuser
    group: appgroup
    recurse: true

# Create symbolic link
- name: Create symlink
  ansible.builtin.file:
    src: /opt/app/current
    dest: /opt/app/releases/v1.2.3
    state: link

# Remove file/directory
- name: Remove file
  ansible.builtin.file:
    path: /tmp/tempfile
    state: absent

# Set permissions
- name: Set file permissions
  ansible.builtin.file:
    path: /etc/app/secret.key
    mode: '0600'
    owner: root
    group: root
```

#### ansible.builtin.copy
```yaml
# Copy file from control node
- name: Copy configuration file
  ansible.builtin.copy:
    src: files/nginx.conf
    dest: /etc/nginx/nginx.conf
    mode: '0644'
    owner: root
    group: root
    backup: true
    validate: 'nginx -t -c %s'

# Copy with inline content
- name: Create file with content
  ansible.builtin.copy:
    content: |
      server {
        listen 80;
        server_name example.com;
      }
    dest: /etc/nginx/sites-available/example
    mode: '0644'

# Remote copy (on target host)
- name: Copy file on remote host
  ansible.builtin.copy:
    src: /tmp/source.txt
    dest: /opt/destination.txt
    remote_src: true
```

#### ansible.builtin.template
```yaml
- name: Deploy configuration from template
  ansible.builtin.template:
    src: templates/app_config.j2
    dest: /etc/app/config.yml
    mode: '0644'
    owner: appuser
    group: appgroup
    backup: true
    validate: '/usr/bin/app validate %s'
```

#### ansible.builtin.fetch
```yaml
- name: Fetch file from remote to control node
  ansible.builtin.fetch:
    src: /var/log/app/error.log
    dest: /tmp/logs/{{ inventory_hostname }}/
    flat: true
```

#### ansible.builtin.lineinfile
```yaml
- name: Ensure line is present
  ansible.builtin.lineinfile:
    path: /etc/hosts
    line: '192.168.1.100 app.local'
    state: present

- name: Replace or add line with regexp
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?PermitRootLogin'
    line: 'PermitRootLogin no'
    state: present
    backup: true
  notify: Restart sshd

- name: Remove line
  ansible.builtin.lineinfile:
    path: /etc/hosts
    regexp: '.*old-server.*'
    state: absent
```

#### ansible.builtin.blockinfile
```yaml
- name: Add block of text
  ansible.builtin.blockinfile:
    path: /etc/hosts
    block: |
      192.168.1.10 web1.local
      192.168.1.11 web2.local
      192.168.1.20 db1.local
    marker: "# {mark} ANSIBLE MANAGED BLOCK - SERVERS"
    backup: true
```

### Service Management

#### ansible.builtin.service
```yaml
- name: Ensure service is running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true

- name: Restart service
  ansible.builtin.service:
    name: nginx
    state: restarted

- name: Stop and disable service
  ansible.builtin.service:
    name: apache2
    state: stopped
    enabled: false
```

#### ansible.builtin.systemd
```yaml
- name: Reload systemd daemon
  ansible.builtin.systemd:
    daemon_reload: true

- name: Start and enable service
  ansible.builtin.systemd:
    name: myapp
    state: started
    enabled: true
    daemon_reload: true

- name: Mask service
  ansible.builtin.systemd:
    name: apache2
    masked: true
```

### User and Group Management

#### ansible.builtin.user
```yaml
- name: Create user
  ansible.builtin.user:
    name: appuser
    uid: 1500
    group: appgroup
    groups: docker,sudo
    shell: /bin/bash
    home: /home/appuser
    createhome: true
    state: present

- name: Set user password
  ansible.builtin.user:
    name: appuser
    password: "{{ user_password | password_hash('sha512') }}"
    update_password: always

- name: Add SSH key
  ansible.builtin.user:
    name: appuser
    ssh_key_bits: 4096
    ssh_key_file: .ssh/id_rsa
```

#### ansible.builtin.group
```yaml
- name: Create group
  ansible.builtin.group:
    name: appgroup
    gid: 1500
    state: present
```

#### ansible.builtin.authorized_key
```yaml
- name: Add SSH authorized key
  ansible.builtin.authorized_key:
    user: appuser
    state: present
    key: "{{ lookup('file', '/home/user/.ssh/id_rsa.pub') }}"

- name: Add multiple keys
  ansible.builtin.authorized_key:
    user: appuser
    state: present
    key: "{{ item }}"
  loop:
    - ssh-rsa AAAAB3... user1@host
    - ssh-rsa AAAAB3... user2@host
```

### Command Execution

#### ansible.builtin.command
```yaml
- name: Run command (no shell processing)
  ansible.builtin.command: /usr/bin/make install
  args:
    chdir: /opt/app
    creates: /opt/app/bin/app
  register: make_result
  changed_when: make_result.rc == 0

- name: Run with environment variables
  ansible.builtin.command: /opt/app/deploy.sh
  environment:
    APP_ENV: production
    DB_HOST: localhost
```

#### ansible.builtin.shell
```yaml
- name: Run shell command (with pipes/redirects)
  ansible.builtin.shell: cat /var/log/app.log | grep ERROR > /tmp/errors.txt
  args:
    executable: /bin/bash
  changed_when: false

- name: Use shell with creates
  ansible.builtin.shell: /opt/install.sh
  args:
    creates: /opt/app/installed.flag
```

#### ansible.builtin.script
```yaml
- name: Run script from control node
  ansible.builtin.script: scripts/setup.sh
  args:
    creates: /etc/app/setup.done
```

### Git Operations

#### ansible.builtin.git
```yaml
- name: Clone repository
  ansible.builtin.git:
    repo: https://github.com/user/repo.git
    dest: /opt/app
    version: main
    force: true

- name: Clone specific branch/tag
  ansible.builtin.git:
    repo: https://github.com/user/repo.git
    dest: /opt/app
    version: v1.2.3

- name: Clone with SSH key
  ansible.builtin.git:
    repo: git@github.com:user/repo.git
    dest: /opt/app
    key_file: /home/deploy/.ssh/id_rsa
    accept_hostkey: true
```

### Archive Operations

#### ansible.builtin.unarchive
```yaml
- name: Extract archive from control node
  ansible.builtin.unarchive:
    src: files/app.tar.gz
    dest: /opt/
    owner: appuser
    group: appgroup

- name: Extract remote archive
  ansible.builtin.unarchive:
    src: /tmp/app.tar.gz
    dest: /opt/
    remote_src: true

- name: Download and extract
  ansible.builtin.unarchive:
    src: https://example.com/app.tar.gz
    dest: /opt/
    remote_src: true
```

#### ansible.builtin.archive
```yaml
- name: Create archive
  ansible.builtin.archive:
    path:
      - /opt/app/config
      - /opt/app/data
    dest: /tmp/backup.tar.gz
    format: gz
```

### Download Operations

#### ansible.builtin.get_url
```yaml
- name: Download file
  ansible.builtin.get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    mode: '0644'
    checksum: sha256:abc123...

- name: Download with authentication
  ansible.builtin.get_url:
    url: https://secure.example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    url_username: user
    url_password: "{{ download_password }}"
```

### URI/API Operations

#### ansible.builtin.uri
```yaml
- name: Check API endpoint
  ansible.builtin.uri:
    url: http://localhost:8080/health
    method: GET
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 5
  delay: 10

- name: POST to API
  ansible.builtin.uri:
    url: https://api.example.com/deploy
    method: POST
    body_format: json
    body:
      version: "1.2.3"
      environment: production
    headers:
      Authorization: "Bearer {{ api_token }}"
    status_code: [200, 201]

- name: Download response to file
  ansible.builtin.uri:
    url: https://api.example.com/data
    method: GET
    dest: /tmp/data.json
```

### Cron Jobs

#### ansible.builtin.cron
```yaml
- name: Add cron job
  ansible.builtin.cron:
    name: "Daily backup"
    minute: "0"
    hour: "2"
    job: "/opt/backup.sh"
    user: root
    state: present

- name: Add cron job with special time
  ansible.builtin.cron:
    name: "Reboot task"
    special_time: reboot
    job: "/opt/startup.sh"

- name: Remove cron job
  ansible.builtin.cron:
    name: "Daily backup"
    state: absent
```

### Debug and Assert

#### ansible.builtin.debug
```yaml
- name: Print variable
  ansible.builtin.debug:
    var: ansible_distribution

- name: Print message
  ansible.builtin.debug:
    msg: "Server IP: {{ ansible_default_ipv4.address }}"

- name: Conditional debug
  ansible.builtin.debug:
    msg: "This is a production server"
  when: env == "production"
```

#### ansible.builtin.assert
```yaml
- name: Validate configuration
  ansible.builtin.assert:
    that:
      - ansible_distribution in ['Ubuntu', 'Debian']
      - app_port | int > 0
      - app_port | int < 65536
      - db_password is defined
    fail_msg: "Configuration validation failed"
    success_msg: "Configuration is valid"
    quiet: false
```

### Set Facts

#### ansible.builtin.set_fact
```yaml
- name: Set computed fact
  ansible.builtin.set_fact:
    app_full_version: "{{ app_name }}-{{ app_version }}"
    deployment_time: "{{ ansible_date_time.iso8601 }}"

- name: Set fact with conditional
  ansible.builtin.set_fact:
    db_host: "{{ 'localhost' if env == 'dev' else 'db.prod.example.com' }}"

- name: Combine facts
  ansible.builtin.set_fact:
    app_config:
      name: "{{ app_name }}"
      version: "{{ app_version }}"
      port: "{{ app_port }}"
```

### Include and Import

#### ansible.builtin.include_tasks
```yaml
- name: Include tasks dynamically
  ansible.builtin.include_tasks: "{{ ansible_os_family }}.yml"

- name: Include with variables
  ansible.builtin.include_tasks: deploy.yml
  vars:
    app_version: "1.2.3"
```

#### ansible.builtin.import_tasks
```yaml
- name: Import tasks statically
  ansible.builtin.import_tasks: common.yml
```

#### ansible.builtin.include_vars
```yaml
- name: Load variables from file
  ansible.builtin.include_vars:
    file: "{{ env }}.yml"

- name: Load all YAML files from directory
  ansible.builtin.include_vars:
    dir: vars/
    extensions:
      - yml
      - yaml
```

### Wait Operations

#### ansible.builtin.wait_for
```yaml
- name: Wait for port to be available
  ansible.builtin.wait_for:
    port: 8080
    delay: 5
    timeout: 300
    state: started

- name: Wait for file to exist
  ansible.builtin.wait_for:
    path: /opt/app/ready
    state: present
    timeout: 300

- name: Wait for service to stop
  ansible.builtin.wait_for:
    port: 8080
    state: stopped
    timeout: 60
```

### Error Handling with Block/Rescue/Always

#### Basic Block with Rescue
```yaml
- name: Handle errors gracefully
  block:
    - name: Attempt risky operation
      ansible.builtin.command: /opt/risky_script.sh

    - name: This won't run if above fails
      ansible.builtin.debug:
        msg: "Script succeeded"
  rescue:
    - name: Handle failure
      ansible.builtin.debug:
        msg: "Script failed, performing recovery"

    - name: Log error details
      ansible.builtin.copy:
        content: "{{ ansible_failed_result }}"
        dest: /var/log/error.log
```

#### Block with Rescue and Always
```yaml
- name: Deploy with rollback capability
  block:
    - name: Stop application
      ansible.builtin.service:
        name: myapp
        state: stopped

    - name: Deploy new version
      ansible.builtin.copy:
        src: app-v2.jar
        dest: /opt/app/app.jar
        backup: true
      register: deploy_result

    - name: Start application
      ansible.builtin.service:
        name: myapp
        state: started
  rescue:
    - name: Rollback on failure
      ansible.builtin.copy:
        remote_src: true
        src: "{{ deploy_result.backup_file }}"
        dest: /opt/app/app.jar
      when: deploy_result.backup_file is defined

    - name: Start application with old version
      ansible.builtin.service:
        name: myapp
        state: started
  always:
    - name: Verify application is running
      ansible.builtin.wait_for:
        port: 8080
        timeout: 60
```

#### Configuration Update with Validation and Backup
```yaml
- name: Update config with validation
  block:
    - name: Deploy new configuration
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        backup: true
        validate: 'nginx -t -c %s'
      register: config_update

    - name: Reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
  rescue:
    - name: Restore backup on failure
      ansible.builtin.copy:
        remote_src: true
        src: "{{ config_update.backup_file }}"
        dest: /etc/nginx/nginx.conf
      when: config_update.backup_file is defined

    - name: Reload nginx with old config
      ansible.builtin.service:
        name: nginx
        state: reloaded
  always:
    - name: Verify nginx is responding
      ansible.builtin.uri:
        url: http://localhost/health
        status_code: 200
```

#### Accessing Error Variables in Rescue
```yaml
- name: Use error variables
  block:
    - name: Task that might fail
      ansible.builtin.command: /opt/backup.sh
      register: backup_result
  rescue:
    - name: Log failed task name
      ansible.builtin.debug:
        msg: "Failed task: {{ ansible_failed_task.name }}"

    - name: Log error details
      ansible.builtin.debug:
        msg: "Error: {{ ansible_failed_result.msg }}"

    - name: Send alert
      ansible.builtin.uri:
        url: https://alerts.example.com/api/alert
        method: POST
        body_format: json
        body:
          task: "{{ ansible_failed_task.name }}"
          error: "{{ ansible_failed_result.msg }}"
          host: "{{ inventory_hostname }}"
```

#### Flush Handlers After Error
```yaml
- name: Ensure handlers run even on failure
  block:
    - name: Update configuration
      ansible.builtin.copy:
        src: app.conf
        dest: /etc/app/app.conf
      notify: Restart application
      changed_when: true

    - name: Task that might fail
      ansible.builtin.command: /opt/verify.sh
  rescue:
    - name: Flush handlers before recovery
      meta: flush_handlers

    - name: Perform recovery actions
      ansible.builtin.debug:
        msg: "Recovering from failure"
```

### File Search and Status

#### ansible.builtin.find
```yaml
# Find old log files
- name: Find log files older than 7 days
  ansible.builtin.find:
    paths: /var/log
    patterns: "*.log"
    age: "7d"
    age_stamp: mtime
  register: old_logs

- name: Delete old log files
  ansible.builtin.file:
    path: "{{ item.path }}"
    state: absent
  loop: "{{ old_logs.files }}"

# Find large files
- name: Find files larger than 100MB
  ansible.builtin.find:
    paths: /var/data
    patterns: "*"
    size: "100m"
    recurse: true
  register: large_files

- name: Display large files
  ansible.builtin.debug:
    msg: "{{ item.path }} - {{ item.size | filesizeformat }}"
  loop: "{{ large_files.files }}"

# Find files by regex pattern
- name: Find backup files
  ansible.builtin.find:
    paths:
      - /opt/backups
      - /var/backups
    patterns: "backup-.*\\.tar\\.gz$"
    use_regex: true
    file_type: file
  register: backup_files

# Find directories
- name: Find empty directories
  ansible.builtin.find:
    paths: /tmp
    file_type: directory
    recurse: false
  register: directories

- name: Remove empty directories
  ansible.builtin.file:
    path: "{{ item.path }}"
    state: absent
  loop: "{{ directories.files }}"
  when: item.isdir
```

#### ansible.builtin.stat
```yaml
# Check if file exists
- name: Check if config file exists
  ansible.builtin.stat:
    path: /etc/app/config.yml
  register: config_file

- name: Create config if missing
  ansible.builtin.copy:
    content: "default: config"
    dest: /etc/app/config.yml
  when: not config_file.stat.exists

# Verify file ownership
- name: Check file owner
  ansible.builtin.stat:
    path: /etc/app/secret.key
  register: secret_file

- name: Fail if not owned by root
  ansible.builtin.fail:
    msg: "Secret file must be owned by root"
  when:
    - secret_file.stat.exists
    - secret_file.stat.pw_name != 'root'

# Check file permissions
- name: Check file permissions
  ansible.builtin.stat:
    path: /etc/ssl/private/app.key
  register: ssl_key

- name: Fix permissions if needed
  ansible.builtin.file:
    path: /etc/ssl/private/app.key
    mode: '0600'
    owner: root
    group: root
  when:
    - ssl_key.stat.exists
    - ssl_key.stat.mode != '0600'

# Check if path is directory
- name: Verify directory
  ansible.builtin.stat:
    path: /opt/app
  register: app_dir

- name: Create directory if needed
  ansible.builtin.file:
    path: /opt/app
    state: directory
    mode: '0755'
  when: not app_dir.stat.exists or not app_dir.stat.isdir

# Get file size and age
- name: Check log file size
  ansible.builtin.stat:
    path: /var/log/app.log
  register: log_file

- name: Rotate log if too large
  ansible.builtin.command: logrotate -f /etc/logrotate.d/app
  when:
    - log_file.stat.exists
    - log_file.stat.size > 104857600  # 100MB

# Check symlink
- name: Check if symlink
  ansible.builtin.stat:
    path: /usr/bin/python
  register: python_link

- name: Display symlink target
  ansible.builtin.debug:
    msg: "Python links to {{ python_link.stat.lnk_target }}"
  when:
    - python_link.stat.exists
    - python_link.stat.islnk
```

### Advanced Control Flow

#### delegate_to
```yaml
# Run task on different host
- name: Add server to load balancer
  ansible.builtin.uri:
    url: "http://lb.example.com/api/add"
    method: POST
    body_format: json
    body:
      server: "{{ inventory_hostname }}"
      port: 8080
  delegate_to: localhost

# Run on specific host in group
- name: Run database migration
  ansible.builtin.command: /opt/migrate.sh
  delegate_to: "{{ groups['database'] | first }}"

# Local command with delegation
- name: Generate local certificate
  ansible.builtin.command: >
    openssl req -x509 -nodes -days 365
    -newkey rsa:2048
    -keyout "/tmp/{{ inventory_hostname }}.key"
    -out "/tmp/{{ inventory_hostname }}.crt"
    -subj "/CN={{ inventory_hostname }}"
  delegate_to: localhost
  become: false
```

#### run_once
```yaml
# Execute once for entire play
- name: Create shared resource
  ansible.builtin.file:
    path: /shared/data
    state: directory
  run_once: true
  delegate_to: "{{ groups['storage'] | first }}"

# Run once with loop over all hosts
- name: Register all hosts in monitoring
  ansible.builtin.uri:
    url: https://monitoring.example.com/api/register
    method: POST
    body_format: json
    body:
      hostname: "{{ item }}"
  loop: "{{ ansible_play_hosts }}"
  run_once: true
  delegate_to: localhost

# Database seed data (once per cluster)
- name: Seed database
  ansible.builtin.command: /opt/seed_data.sh
  run_once: true
  delegate_to: "{{ groups['database'] | first }}"
```

#### local_action
```yaml
# Execute on control node
- name: Generate configuration locally
  local_action:
    module: ansible.builtin.template
    src: config.j2
    dest: "/tmp/{{ inventory_hostname }}_config.yml"

# Fetch file from remote to local
- name: Backup configuration locally
  local_action:
    module: ansible.builtin.copy
    content: "{{ lookup('file', '/etc/app/config.yml') }}"
    dest: "/backup/{{ inventory_hostname }}_config.yml"

# Send notification from control node
- name: Send deployment notification
  local_action:
    module: ansible.builtin.uri
    url: https://chat.example.com/webhook
    method: POST
    body_format: json
    body:
      message: "Deploying to {{ inventory_hostname }}"
  run_once: true

# Local script execution
- name: Run local analysis script
  local_action:
    module: ansible.builtin.command
    cmd: python3 analyze.py --host {{ inventory_hostname }}
  register: analysis_result
```

## Common Collection Modules

### community.general

#### community.general.ufw (Firewall)
```yaml
- name: Allow SSH
  community.general.ufw:
    rule: allow
    port: '22'
    proto: tcp

- name: Enable firewall
  community.general.ufw:
    state: enabled
```

#### community.general.timezone
```yaml
- name: Set timezone
  community.general.timezone:
    name: America/New_York
```

### community.docker

#### community.docker.docker_container
```yaml
- name: Run Docker container
  community.docker.docker_container:
    name: myapp
    image: nginx:latest
    state: started
    restart_policy: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /opt/data:/data
    env:
      APP_ENV: production
```

### community.postgresql

#### community.postgresql.postgresql_db
```yaml
- name: Create database
  community.postgresql.postgresql_db:
    name: appdb
    state: present
```

### ansible.posix

#### ansible.posix.mount
```yaml
- name: Mount filesystem
  ansible.posix.mount:
    path: /data
    src: /dev/sdb1
    fstype: ext4
    state: mounted
```

#### ansible.posix.sysctl
```yaml
- name: Set sysctl parameter
  ansible.posix.sysctl:
    name: net.ipv4.ip_forward
    value: '1'
    state: present
    reload: true
```

## Cloud Provider Modules

### Amazon AWS (amazon.aws)

#### amazon.aws.ec2_instance
```yaml
# Requirements:
#   - ansible-galaxy collection install amazon.aws
#   - boto3 and botocore Python packages
#   - Python 3.8+

# Launch EC2 instance with public IP
- name: Launch EC2 instance
  amazon.aws.ec2_instance:
    name: web-server-01
    key_name: my-ssh-key
    vpc_subnet_id: subnet-12345678
    instance_type: t3.micro
    security_group: default
    network:
      assign_public_ip: true
    image_id: ami-0c55b159cbfafe1f0  # Amazon Linux 2
    tags:
      Environment: production
      Application: web
    state: running

# Launch instance with EBS volumes
- name: Launch instance with additional storage
  amazon.aws.ec2_instance:
    name: database-server
    key_name: my-ssh-key
    vpc_subnet_id: subnet-12345678
    instance_type: t3.large
    image_id: ami-0c55b159cbfafe1f0
    volumes:
      - device_name: /dev/sda1
        ebs:
          volume_size: 30
          volume_type: gp3
          delete_on_termination: true
      - device_name: /dev/sdb
        ebs:
          volume_size: 100
          volume_type: gp3
          delete_on_termination: false
    tags:
      Environment: production
      Role: database
    state: running

# Start/stop instances by ID
- name: Start EC2 instances
  amazon.aws.ec2_instance:
    instance_ids:
      - i-0123456789abcdef0
      - i-0123456789abcdef1
    state: running

- name: Stop EC2 instances
  amazon.aws.ec2_instance:
    instance_ids:
      - i-0123456789abcdef0
    state: stopped

# Terminate instance (use with EXTREME caution)
- name: Terminate EC2 instance
  amazon.aws.ec2_instance:
    instance_ids:
      - i-0123456789abcdef0
    state: terminated
```

#### amazon.aws.ec2_instance_info
```yaml
# Gather info about all instances
- name: Get all EC2 instances
  amazon.aws.ec2_instance_info:
  register: ec2_instances

# Filter instances by tag
- name: Get production web servers
  amazon.aws.ec2_instance_info:
    filters:
      "tag:Environment": production
      "tag:Role": webserver
      instance-state-name: running
  register: prod_web_servers

- name: Display instance IPs
  ansible.builtin.debug:
    msg: "{{ item.public_ip_address }}"
  loop: "{{ prod_web_servers.instances }}"
```

#### amazon.aws.s3_object
```yaml
# Upload file to S3
- name: Upload file to S3 bucket
  amazon.aws.s3_object:
    bucket: my-backup-bucket
    object: "backups/{{ ansible_date_time.date }}/app.tar.gz"
    src: /tmp/app.tar.gz
    mode: put
    encrypt: true

# Download file from S3
- name: Download configuration from S3
  amazon.aws.s3_object:
    bucket: my-config-bucket
    object: app/config.yml
    dest: /etc/app/config.yml
    mode: get

# Delete object from S3
- name: Remove old backup
  amazon.aws.s3_object:
    bucket: my-backup-bucket
    object: "backups/old/app.tar.gz"
    mode: delobj
```

#### amazon.aws.rds_instance
```yaml
# Create RDS instance
- name: Create PostgreSQL RDS instance
  amazon.aws.rds_instance:
    db_instance_identifier: myapp-db
    engine: postgres
    engine_version: "15.4"
    db_instance_class: db.t3.micro
    allocated_storage: 20
    storage_type: gp3
    master_username: dbadmin
    master_user_password: "{{ db_password }}"
    vpc_security_group_ids:
      - sg-12345678
    db_subnet_group_name: my-db-subnet
    backup_retention_period: 7
    multi_az: false
    publicly_accessible: false
    tags:
      Environment: production
      Application: myapp
```

### Microsoft Azure (azure.azcollection)

#### azure.azcollection.azure_rm_virtualmachine
```yaml
# Requirements:
#   - ansible-galaxy collection install azure.azcollection
#   - Azure SDK packages (see collection requirements.txt)

# Create VM with defaults
- name: Create Azure VM
  azure.azcollection.azure_rm_virtualmachine:
    resource_group: myResourceGroup
    name: webserver01
    admin_username: azureuser
    admin_password: "{{ vm_password }}"
    vm_size: Standard_B2s
    image:
      offer: 0001-com-ubuntu-server-focal
      publisher: Canonical
      sku: 20_04-lts
      version: latest
    tags:
      Environment: production
      Role: webserver

# Create VM with managed disk
- name: Create VM with managed disk
  azure.azcollection.azure_rm_virtualmachine:
    resource_group: myResourceGroup
    name: appserver01
    admin_username: azureuser
    ssh_password_enabled: false
    ssh_public_keys:
      - path: /home/azureuser/.ssh/authorized_keys
        key_data: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    vm_size: Standard_D4s_v3
    managed_disk_type: Premium_LRS
    image:
      offer: 0001-com-ubuntu-server-focal
      publisher: Canonical
      sku: 20_04-lts-gen2
      version: latest
    os_disk_size_gb: 128
    data_disks:
      - lun: 0
        disk_size_gb: 256
        managed_disk_type: Premium_LRS
    network_interfaces: mynetworkinterface
    tags:
      Environment: production

# Start/stop Azure VMs
- name: Stop Azure VM
  azure.azcollection.azure_rm_virtualmachine:
    resource_group: myResourceGroup
    name: webserver01
    allocated: false

- name: Start Azure VM
  azure.azcollection.azure_rm_virtualmachine:
    resource_group: myResourceGroup
    name: webserver01
    allocated: true

# Delete Azure VM
- name: Delete Azure VM
  azure.azcollection.azure_rm_virtualmachine:
    resource_group: myResourceGroup
    name: webserver01
    state: absent
```

#### azure.azcollection.azure_rm_virtualmachine_info
```yaml
# Get all VMs in resource group
- name: Get VM facts
  azure.azcollection.azure_rm_virtualmachine_info:
    resource_group: myResourceGroup
  register: azure_vms

# Get specific VM info
- name: Get specific VM info
  azure.azcollection.azure_rm_virtualmachine_info:
    resource_group: myResourceGroup
    name: webserver01
  register: vm_info

- name: Display VM private IP
  ansible.builtin.debug:
    msg: "{{ vm_info.vms[0].network_profile.network_interfaces[0].ip_configurations[0].private_ip_address }}"
```

#### azure.azcollection.azure_rm_storageblob
```yaml
# Upload file to Azure Blob Storage
- name: Upload backup to blob storage
  azure.azcollection.azure_rm_storageblob:
    resource_group: myResourceGroup
    storage_account_name: mystorageaccount
    container: backups
    blob: "{{ ansible_date_time.date }}/app-backup.tar.gz"
    src: /tmp/app-backup.tar.gz
    content_type: application/gzip

# Download from blob storage
- name: Download config from blob storage
  azure.azcollection.azure_rm_storageblob:
    resource_group: myResourceGroup
    storage_account_name: mystorageaccount
    container: configs
    blob: app-config.yml
    dest: /etc/app/config.yml
```

#### azure.azcollection.azure_rm_sqldatabase
```yaml
# Create Azure SQL Database
- name: Create SQL database
  azure.azcollection.azure_rm_sqldatabase:
    resource_group: myResourceGroup
    server_name: mydbserver
    name: mydatabase
    sku:
      name: S0
      tier: Standard
    max_size_bytes: 268435456000  # 250GB
    tags:
      Environment: production
      Application: myapp
```

## Secrets Management Lookups

### HashiCorp Vault

#### community.hashi_vault.hashi_vault lookup
```yaml
# Requirements:
#   - ansible-galaxy collection install community.hashi_vault
#   - hvac Python package

# Retrieve secret from Vault
- name: Get database password from Vault
  ansible.builtin.set_fact:
    db_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/database:password') }}"
  no_log: true

# Use multiple vault paths
- name: Get multiple secrets
  ansible.builtin.set_fact:
    api_key: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/api:key') }}"
    api_secret: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/api:secret') }}"
  no_log: true

# Configure Vault connection
- name: Get secret with custom Vault config
  ansible.builtin.set_fact:
    admin_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/admin:password', url='https://vault.example.com:8200', auth_method='token', token=vault_token) }}"
  no_log: true
```

### AWS Secrets Manager

#### community.aws.aws_secret lookup
```yaml
# Requirements:
#   - ansible-galaxy collection install community.aws
#   - boto3 and botocore

# Retrieve secret from AWS Secrets Manager
- name: Get database credentials from Secrets Manager
  ansible.builtin.set_fact:
    db_creds: "{{ lookup('community.aws.aws_secret', 'prod/database/credentials', region='us-east-1') | from_json }}"
  no_log: true

- name: Use retrieved credentials
  ansible.builtin.debug:
    msg: "Connecting to {{ db_creds.host }} as {{ db_creds.username }}"

# Retrieve specific version
- name: Get specific secret version
  ansible.builtin.set_fact:
    api_key: "{{ lookup('community.aws.aws_secret', 'prod/api/key', version_id='EXAMPLE1-90ab-cdef-fedc-ba987EXAMPLE') }}"
  no_log: true
```

### Azure Key Vault

#### azure.azcollection.azure_keyvault_secret lookup
```yaml
# Requirements:
#   - ansible-galaxy collection install azure.azcollection

# Retrieve secret from Azure Key Vault
- name: Get secret from Key Vault
  ansible.builtin.set_fact:
    app_secret: "{{ lookup('azure.azcollection.azure_keyvault_secret', 'app-secret', vault_url='https://myvault.vault.azure.net') }}"
  no_log: true

# Use in tasks
- name: Deploy application with secret
  ansible.builtin.template:
    src: config.j2
    dest: /etc/app/config.yml
  vars:
    secret_key: "{{ lookup('azure.azcollection.azure_keyvault_secret', 'secret-key', vault_url='https://myvault.vault.azure.net') }}"
  no_log: true
```
