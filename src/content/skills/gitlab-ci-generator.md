---
title: "GitLab CI 生成器"
description: "生成 GitLab CI/CD 管道配置文件"
category: "devops"
source: "community"
author: "Community"
tags: ["gitlab", "ci", "generator"]
date: 2026-03-20
---

# GitLab CI/CD Pipeline Generator

## Overview

Generate production-ready GitLab CI/CD pipeline configurations following current best practices, security standards, and naming conventions. All generated resources are automatically validated using the devops-skills:gitlab-ci-validator skill to ensure syntax correctness and compliance with best practices.

---

## Trigger Phrases

Use this skill when the user asks for GitLab CI/CD generation requests such as:
- "Create a `.gitlab-ci.yml` for..."
- "Build a GitLab pipeline for Node/Python/Java..."
- "Add Docker build and deploy jobs in GitLab CI"
- "Set up GitLab parent-child or multi-project pipelines"
- "Include SAST/dependency scanning templates in GitLab CI"

## Execution Model

Follow this deterministic flow in order:
1. Classify request complexity (`targeted`, `lightweight`, or `full`).
2. Load only the required reference tier for that complexity.
3. Output the matching response profile for the selected mode.
4. For complete pipeline generation, start from the closest template and customize.
5. Validate complete pipelines with strict Critical/High gates.
6. Present output with validation status and template/version notes.

If tooling is unavailable, use the documented fallback branch and report it explicitly.

## Mode Routing (Quick Decision)

| Request shape | Mode | Required references | Output profile |
|---------------|------|---------------------|----------------|
| Simple single-file pipeline with common jobs/stages and low risk | **Lightweight** | Tier 1 (+ Tier 2 only if needed) | Lightweight confirmation + compact final sections |
| Multi-environment deploy, advanced `rules`, includes/templates, security/compliance-sensitive workflow, or unclear/risky requirement | **Full** | Tier 1 + Tier 2 (Tier 3 only if needed) | Full confirmation + full final sections |
| Review/Q&A/snippet/focused fix (not full file generation) | **Targeted** | Only directly relevant files | Concise targeted response (no full boilerplate) |

When uncertain on a complete-generation request, route to **Full** mode.

## MANDATORY PRE-GENERATION STEPS

**CRITICAL:** Before generating any complete GitLab CI/CD pipeline, complete these steps.

### Step 1: Classify Complexity (REQUIRED)

| Mode | Use When | Minimum Confirmation |
|------|----------|----------------------|
| **Targeted** | Review/Q&A/snippet/focused fix where full pipeline generation is not requested | Concise targeted response |
| **Lightweight** | Simple single-file pipeline, common stages/jobs, no advanced GitLab features, no sensitive deploy/security customization | Lightweight confirmation |
| **Full** | Multi-environment deploys, includes/templates, advanced `rules` logic, security scanning customization, compliance-sensitive workflows, or any unclear/risky request | Full confirmation |

When uncertain on a complete-generation request, default to **Full** mode.

### Step 2: Load References by Tier (REQUIRED)

Use an open/read action to load references based on the selected mode.

**Targeted mode (review/Q&A/snippet/focused fix):**
- Load only directly relevant references/templates for the scoped request.
- Do not enforce Full-generation Tier 1/Tier 2 checklist items.

**Tier 1 (Required for complete pipeline generation in Lightweight and Full modes):**
1. `references/best-practices.md` - baseline security, performance, naming
2. `references/common-patterns.md` - starting pattern selection
3. Matching template from `assets/templates/`:
   - Docker pipelines -> `assets/templates/docker-build.yml`
   - Kubernetes deployments -> `assets/templates/kubernetes-deploy.yml`
   - Multi-project pipelines -> `assets/templates/multi-project.yml`
   - Basic pipelines -> `assets/templates/basic-pipeline.yml`

**Tier 2 (Required for Full mode; optional for Lightweight mode):**
1. `references/gitlab-ci-reference.md` - keyword/syntax edge cases
2. `references/security-guidelines.md` - security-sensitive controls

**Tier 3 (Conditional external docs lookup):**
- Use only when local references do not cover requested features or version-specific behavior.
- Follow the lookup flow in "Handling GitLab CI/CD Documentation Lookup."

**If a required local reference or template is unavailable:**
- Report the exact missing path.
- Continue with available references and mark assumptions explicitly.
- Do not claim production-ready confidence until missing critical inputs are resolved.

### Step 3: Confirm Understanding (EXPLICIT OUTPUT REQUIRED)

#### Lightweight Confirmation Mode

Use for simple requests only.

**Required format:**
```markdown
## Reference Analysis Complete (Lightweight)

**Pattern:** [Pattern name] from common-patterns.md
**Template:** [Template file]
**Key standards to enforce:**
- [2-3 concrete standards]
```

**Example:**
```markdown
## Reference Analysis Complete (Lightweight)

**Pattern:** Basic Build-Test-Deploy from common-patterns.md
**Template:** assets/templates/basic-pipeline.yml
**Key standards to enforce:**
- Pin runtime image versions (no `:latest`)
- Add explicit job timeouts
- Use `rules` instead of deprecated `only`/`except`
```

#### Full Confirmation Mode

Use for complex or security-sensitive requests.

**Required format:**
```markdown
## Reference Analysis Complete (Full)

**Pipeline Pattern Identified:** [Pattern name] from common-patterns.md
- [Brief description of why this pattern fits]

**Best Practices to Apply:**
- [List 3-5 key best practices relevant to this pipeline]

**Security Guidelines:**
- [List security measures to implement]

**Template Foundation:** [Template file name]
- [What will be customized from this template]
```

**Example:**
```markdown
## Reference Analysis Complete (Full)

**Pipeline Pattern Identified:** Docker Build + Kubernetes Deployment from common-patterns.md
- User needs containerized deployment to K8s clusters with staging/production environments

**Best Practices to Apply:**
- Pin all Docker images to specific versions (not `:latest`)
- Use caching for pip dependencies
- Implement DAG optimization with `needs` keyword
- Set explicit timeout on all jobs (15-20 minutes)
- Use `resource_group` for deployment jobs

**Security Guidelines:**
- Use masked CI/CD variables for secrets (KUBE_CONTEXT, registry credentials)
- Include container scanning with Trivy
- Never expose secrets in logs

**Template Foundation:** assets/templates/docker-build.yml + assets/templates/kubernetes-deploy.yml
- Combine Docker build pattern with K8s kubectl deployment
- Add Python-specific test jobs
```

**Skipping confirmation is not allowed for complete pipeline generation.**

---

## Core Capabilities

### 1. Generate Basic CI/CD Pipelines

Create complete, production-ready `.gitlab-ci.yml` files with proper structure, security best practices, and efficient CI/CD patterns.

**When to use:**
- User requests: "Create a GitLab pipeline for...", "Build a CI/CD pipeline...", "Generate GitLab CI config..."
- Scenarios: CI/CD pipelines, automated testing, build automation, deployment pipelines

**Process:**
1. Understand the user's requirements (what needs to be automated)
2. Identify stages, jobs, dependencies, and artifacts
3. Use `assets/templates/basic-pipeline.yml` as structural foundation
4. Reference `references/best-practices.md` for implementation patterns
5. Reference `references/common-patterns.md` for standard pipeline patterns
6. Generate the pipeline following these principles:
   - Use semantic stage and job names
   - Pin Docker images to specific versions (not :latest)
   - Implement proper secrets management with masked variables
   - Use caching for dependencies to improve performance
   - Implement proper artifact handling with expiration
   - Use `needs` keyword for DAG optimization when appropriate
   - Add proper error handling with retry and allow_failure
   - Use `rules` instead of deprecated only/except
   - **Set explicit `timeout` for all jobs** (10-30 minutes typically)
   - Add meaningful job descriptions in comments
7. **ALWAYS validate** the generated pipeline using the devops-skills:gitlab-ci-validator skill
8. If validation fails, fix the issues and re-validate

**Example structure:**
```yaml
# Basic CI/CD Pipeline
# Builds, tests, and deploys the application

stages:
  - build
  - test
  - deploy

# Global variables
variables:
  NODE_VERSION: "20"
  DOCKER_DRIVER: overlay2

# Default settings for all jobs
default:
  image: node:20-alpine
  timeout: 20 minutes  # Default timeout for all jobs
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - echo "Starting job ${CI_JOB_NAME}"
  tags:
    - docker
  interruptible: true

# Build stage - Compiles the application
build-application:
  stage: build
  timeout: 15 minutes
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour
  rules:
    - changes:
        - src/**/*
        - package*.json
      when: always
    - when: on_success

# Test stage
test-unit:
  stage: test
  needs: [build-application]
  script:
    - npm run test:unit
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test-lint:
  stage: test
  needs: []  # Can run immediately
  script:
    - npm run lint
  allow_failure: true

# Deploy stage
deploy-staging:
  stage: deploy
  needs: [build-application, test-unit]
  script:
    - npm run deploy:staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
  when: manual

deploy-production:
  stage: deploy
  needs: [build-application, test-unit]
  script:
    - npm run deploy:production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
  resource_group: production
```

### 2. Generate Docker Build Pipelines

Create pipelines for building, testing, and pushing Docker images to container registries.

**When to use:**
- User requests: "Create a Docker build pipeline...", "Build and push Docker images..."
- Scenarios: Container builds, multi-stage Docker builds, registry pushes

**Process:**
1. Understand the Docker build requirements (base images, registries, tags)
2. Use `assets/templates/docker-build.yml` as foundation
3. Implement Docker-in-Docker or Kaniko for builds
4. Configure registry authentication
5. Implement image tagging strategy
6. Add security scanning if needed
7. **ALWAYS validate** using devops-skills:gitlab-ci-validator skill

**Example:**
```yaml
stages:
  - build
  - scan
  - push

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

# Build Docker image
docker-build:
  stage: build
  image: docker:24-dind
  timeout: 20 minutes
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build
        --cache-from $IMAGE_NAME:latest
        --tag $IMAGE_NAME:$IMAGE_TAG
        --tag $IMAGE_NAME:latest
        .
    - docker push $IMAGE_NAME:$IMAGE_TAG
    - docker push $IMAGE_NAME:latest
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  retry:
    max: 2
    when:
      - runner_system_failure

# Scan for vulnerabilities
container-scan:
  stage: scan
  image: aquasec/trivy:0.49.0
  timeout: 15 minutes
  script:
    - trivy image --exit-code 0 --severity HIGH,CRITICAL $IMAGE_NAME:$IMAGE_TAG
  needs: [docker-build]
  allow_failure: true
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### 3. Generate Kubernetes Deployment Pipelines

Create pipelines that deploy applications to Kubernetes clusters.

**When to use:**
- User requests: "Deploy to Kubernetes...", "Create K8s deployment pipeline..."
- Scenarios: Kubernetes deployments, Helm deployments, kubectl operations

**Process:**
1. Identify the Kubernetes deployment method (kubectl, Helm, Kustomize)
2. Use `assets/templates/kubernetes-deploy.yml` as foundation
3. Configure cluster authentication (service accounts, kubeconfig)
4. Implement proper environment management
5. Add rollback capabilities
6. **ALWAYS validate** using devops-skills:gitlab-ci-validator skill

**Example:**
```yaml
stages:
  - build
  - deploy

# Kubernetes deployment job
deploy-k8s:
  stage: deploy
  image: bitnami/kubectl:1.29
  timeout: 10 minutes
  before_script:
    - kubectl config use-context $KUBE_CONTEXT
  script:
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/myapp -n $KUBE_NAMESPACE --timeout=5m
  environment:
    name: production
    url: https://example.com
    kubernetes:
      namespace: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
  resource_group: k8s-production
  retry:
    max: 2
    when:
      - runner_system_failure
```

### 4. Generate Multi-Project Pipelines

Create pipelines that trigger other projects or use parent-child pipeline patterns.

**When to use:**
- User requests: "Create multi-project pipeline...", "Trigger other pipelines..."
- Scenarios: Monorepos, microservices, orchestration pipelines

**Process:**
1. Identify the pipeline orchestration needs
2. Use `assets/templates/multi-project.yml` or parent-child templates
3. Configure proper artifact passing
4. Implement parallel execution where appropriate
5. **ALWAYS validate** using devops-skills:gitlab-ci-validator skill

**Example (Parent-Child):**
```yaml
# Parent pipeline
stages:
  - trigger

generate-child-pipeline:
  stage: trigger
  script:
    - echo "Generating child pipeline config"
    - |
      cat > child-pipeline.yml <<EOF
      stages:
        - build

      child-job:
        stage: build
        script:
          - echo "Running child job"
      EOF
  artifacts:
    paths:
      - child-pipeline.yml

trigger-child:
  stage: trigger
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-child-pipeline
    strategy: depend
  needs: [generate-child-pipeline]
```

### 5. Generate Template-Based Configurations

Create reusable templates using extends, YAML anchors, and includes.

**When to use:**
- User requests: "Create reusable templates...", "Build modular pipeline config..."
- Scenarios: Template libraries, DRY configurations, shared CI/CD logic

**Process:**
1. Identify common patterns to extract
2. Create hidden jobs (prefixed with .)
3. Use `extends` keyword for inheritance
4. Organize into separate files with `include`
5. **ALWAYS validate** using devops-skills:gitlab-ci-validator skill

**Example:**
```yaml
# Hidden template jobs (include timeout in templates)
.node-template:
  image: node:20-alpine
  timeout: 15 minutes  # Default timeout for jobs using this template
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci
  interruptible: true

.deploy-template:
  timeout: 10 minutes  # Deploy jobs should have explicit timeout
  before_script:
    - echo "Deploying to ${ENVIRONMENT}"
  after_script:
    - echo "Deployment complete"
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  interruptible: false  # Deploys should not be interrupted

# Actual jobs using templates
build:
  extends: .node-template
  stage: build
  script:
    - npm run build

deploy-staging:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: staging
  script:
    - ./deploy.sh staging
  resource_group: staging
```

### 6. Handling GitLab CI/CD Documentation Lookup

Use this flow only when local references do not cover requested features or version-sensitive behavior.

**Detection:**
- User mentions specific GitLab features (e.g., "Auto DevOps", "SAST", "dependency scanning")
- User requests integration with GitLab templates
- Pipeline requires specific GitLab runner features

**Process:**

1. **Identify the feature:**
   - Extract the GitLab feature or template name
   - Determine if version-specific information is needed

2. **Check local references first (Tier 1/Tier 2):**
   - `references/common-patterns.md`
   - `references/gitlab-ci-reference.md`
   - `references/security-guidelines.md`

3. **Use Context7 first when external lookup is needed:**
   - Resolve library: `mcp__context7__resolve-library-id`
   - Query docs: `mcp__context7__query-docs`
   - Prefer GitLab official/library docs over secondary sources

4. **Fallback to web search when Context7 is unavailable or insufficient:**
   - Use `web.search_query`
   - Query pattern: `"GitLab CI/CD [feature] documentation"`
   - Prefer results from `docs.gitlab.com`

5. **Open and extract from specific docs pages when needed:**
   - Use `web.open` for selected documentation pages
   - Capture required syntax, variables, and version constraints

6. **Analyze discovered documentation for:**
   - Current recommended approach
   - Required variables and configuration
   - Template include syntax
   - Best practices and security recommendations
   - Example usage

7. **If network tools are unavailable (offline/constrained environment):**
   - Continue using local references only
   - State that external version verification could not be performed
   - Add a version-assumption note in the final output

8. **Generate pipeline using discovered information:**
   - Use correct template include syntax
   - Configure required variables
   - Add security best practices
   - Include comments about versions and choices

**Example with GitLab templates:**
```yaml
# Include GitLab's security templates (use Jobs/ prefix for current templates)
include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Dependency-Scanning.gitlab-ci.yml

# Customize SAST behavior via global variables
# Note: Set variables globally rather than overriding template jobs
# to avoid validation issues with partial job definitions
variables:
  SAST_EXCLUDED_PATHS: "spec, test, tests, tmp, node_modules"
  DS_EXCLUDED_PATHS: "node_modules, vendor"
  SECURE_LOG_LEVEL: "info"
```

> **Important:** When using `include` with GitLab templates, the included jobs are
> fully defined in the template. If you need to customize them, prefer setting
> variables globally rather than creating partial job overrides (which will fail
> local validation because the validator cannot resolve the included template).
> GitLab merges the configuration at runtime, but local validators only see
> your `.gitlab-ci.yml` file.

## Validation Workflow

**CRITICAL:** Every generated GitLab CI/CD configuration MUST be validated before presenting to the user.

### Validation Process

1. **Primary validation path:** after generating a complete pipeline, invoke the `devops-skills:gitlab-ci-validator` skill:
   ```
   Skill: devops-skills:gitlab-ci-validator
   ```

2. **Script fallback path (if validator skill cannot be invoked):**
   ```bash
   PIPELINE_FILE="<generated-output-path>"
   ```
   - Set `PIPELINE_FILE` to the exact generated file path (for example, `pipelines/review.yml` or `.gitlab-ci.yml`).
   - Fail fast if that file does not exist:
     ```bash
     if [[ ! -f "$PIPELINE_FILE" ]]; then
       echo "ERROR: CI file not found: $PIPELINE_FILE" >&2
       exit 1
     fi
     ```
   ```bash
   # From repository root
   bash devops-skills-plugin/skills/gitlab-ci-validator/scripts/validate_gitlab_ci.sh "$PIPELINE_FILE"
   ```
   ```bash
   # From skills/gitlab-ci-generator directory
   bash ../gitlab-ci-validator/scripts/validate_gitlab_ci.sh "$PIPELINE_FILE"
   ```
   - If the script is not executable:
     ```bash
     chmod +x devops-skills-plugin/skills/gitlab-ci-validator/scripts/validate_gitlab_ci.sh
     ```
   - Optional API lint fallback when GitLab project context is available:
     ```bash
     jq --null-input --arg yaml "$(<"$PIPELINE_FILE")" '.content=$yaml' \
     | curl --header "Content-Type: application/json" \
       --url "https://gitlab.com/api/v4/projects/:id/ci/lint?include_merged_yaml=true" \
       --data @-
     ```

3. **Manual fallback path (only if both primary and script paths are unavailable):**
   - Run manual checks for YAML validity, stage/job references, and obvious secret exposure.
   - Mark output as `Validation status: Manual fallback (not fully verified)`.
   - Do not claim production-ready status if Critical/High risk cannot be confidently ruled out.

4. **The validator skill/script checks:**
   - Validate YAML syntax
   - Check GitLab CI/CD schema compliance
   - Verify job references and dependencies
   - Check for best practices violations
   - Perform security scanning
   - Report any errors, warnings, or issues

5. **Analyze validation results and take action based on severity:**

   | Severity | Action Required |
   |----------|-----------------|
   | **CRITICAL** | MUST fix before presenting. Pipeline is broken or severely insecure. |
   | **HIGH** | MUST fix before presenting. Significant security or functionality issues. |
   | **MEDIUM** | SHOULD fix before presenting. Apply fixes or explain why not applicable. |
   | **LOW** | MAY fix or acknowledge. Inform user of recommendations. |
   | **SUGGESTIONS** | Review and apply if beneficial. No fix required. |

6. **Fix-and-Revalidate Loop (MANDATORY for Critical/High issues):**
   ```
   While validation has CRITICAL or HIGH issues:
     1. Edit the generated file to fix the issue
     2. Re-run validation
     3. Repeat until no CRITICAL or HIGH issues remain
   ```

7. **Before presenting to user, ensure:**
   - Zero CRITICAL issues
   - Zero HIGH issues
   - MEDIUM issues either fixed OR explained why they're acceptable
   - LOW issues and suggestions acknowledged

8. **When presenting the validated configuration:**
   - State validation status clearly
   - State validation path used (skill, script fallback, or manual fallback)
   - List any remaining MEDIUM/LOW issues with explanations
   - Include template/version freshness notes
   - Provide usage instructions
   - Mention any trade-offs made

**Critical/High gate is strict and never optional for production-ready claims.**

### Validation Pass Criteria

**Pipeline is READY to present when:**
- ✅ Validation path executed (validator skill or script fallback)
- ✅ Syntax validation: PASSED
- ✅ Security scan: No CRITICAL or HIGH issues
- ✅ Best practices: Reviewed (warnings acceptable with explanation)

**Pipeline is NOT READY when:**
- ❌ Any syntax errors exist
- ❌ Any CRITICAL security issues exist
- ❌ Any HIGH security issues exist
- ❌ Job references are broken
- ❌ Only manual fallback was used and Critical/High risks cannot be ruled out

### When to Skip Validation

Only skip validation when:
- Generating partial code snippets (not complete files)
- Creating examples for documentation purposes
- User explicitly requests to skip validation

### Handling MEDIUM Severity Issues (REQUIRED OUTPUT)

When the validator reports MEDIUM severity issues, you MUST either fix them OR explain why they're acceptable. This explanation is REQUIRED in your output.

**Required format for MEDIUM issue handling:**
```
## Validation Issues Addressed

### MEDIUM Severity Issues

| Issue | Status | Explanation |
|-------|--------|-------------|
| [Issue code] | Fixed/Acceptable | [Why it was fixed OR why it's acceptable] |
```

**Example MEDIUM issue explanations:**

```
## Validation Issues Addressed

### MEDIUM Severity Issues

| Issue | Status | Explanation |
|-------|--------|-------------|
| `image-variable-no-digest` | Acceptable | Using `python:${PYTHON_VERSION}-alpine` allows flexible version management via CI/CD variables. The PYTHON_VERSION variable is controlled internally and pinned to "3.12". SHA digest pinning would require updating the digest with every image update, adding maintenance burden without significant security benefit for this use case. |
| `pip-without-hashes` | Acceptable | This pipeline installs well-known packages (pytest, flake8) from PyPI. Using `--require-hashes` would require maintaining hash files for all transitive dependencies. For internal CI/CD, the security trade-off is acceptable. For higher security environments, consider using a private PyPI mirror with verified packages. |
| `git-strategy-none` | Acceptable | The `stop-staging` and `rollback-production` jobs use `GIT_STRATEGY: none` because they only run kubectl commands that don't require source code. The scripts are inline in the YAML (not from the repo), so there's no risk of executing untrusted code. |
```

**When to FIX vs ACCEPT:**

| Scenario | Action |
|----------|--------|
| Production/high-security environment | FIX the issue |
| Issue has simple fix with no downside | FIX the issue |
| Fix adds significant complexity | ACCEPT with explanation |
| Fix requires external changes (e.g., CI/CD variables) | ACCEPT with explanation |
| Issue is false positive for this context | ACCEPT with explanation |

### Reviewing Suggestions (REQUIRED OUTPUT)

When the validator provides suggestions, you MUST briefly acknowledge them and explain whether they should be applied.

**Required format:**
```
## Validator Suggestions Review

| Suggestion | Recommendation | Reason |
|------------|----------------|--------|
| [suggestion] | Apply/Skip | [Why] |
```

**Example suggestions review:**

```
## Validator Suggestions Review

| Suggestion | Recommendation | Reason |
|------------|----------------|--------|
| `missing-retry` on test jobs | Skip | Test jobs are deterministic and don't interact with external services. Retry would mask flaky tests rather than fail fast. |
| `parallel-opportunity` for test-unit | Apply if beneficial | Could be added if pytest supports sharding. Add `parallel: 3` with `pytest --shard=${CI_NODE_INDEX}/${CI_NODE_TOTAL}` if test suite is large enough to benefit. |
| `dag-optimization` for stop-staging | Skip | This job is manual and only runs on environment cleanup. DAG optimization wouldn't provide meaningful speedup. |
| `no-dependency-proxy` | Apply for production | Consider using `$CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX` to avoid Docker Hub rate limits. Requires GitLab Premium. |
| `environment-no-url` for rollback | Skip | Rollback jobs don't deploy new versions, so a URL would be misleading. |
| `missing-coverage` for lint job | Skip | Linting doesn't produce coverage data. This is a false positive. |
```

### Template and Version Notes (REQUIRED OUTPUT)

After validation results, include a concise freshness note for templates and documentation assumptions.

**Required format:**
```markdown
## Template and Version Notes

- **Template base:** [assets/templates/<file>.yml]
- **Template customization scope:** [what changed from template]
- **Version/doc basis:** [Context7, docs.gitlab.com, or local references only]
- **Freshness note:** [exact date checked, or "external lookup unavailable"]
- **Version-sensitive assumptions:** [if any]
```

**Example:**
```markdown
## Template and Version Notes

- **Template base:** assets/templates/docker-build.yml
- **Template customization scope:** Added unit-test stage and environment-specific deploy rules
- **Version/doc basis:** docs.gitlab.com include-template docs + local references
- **Freshness note:** Verified template syntax on 2026-02-28
- **Version-sensitive assumptions:** Uses `Jobs/SAST.gitlab-ci.yml` template path
```

### Usage Instructions Template (REQUIRED OUTPUT)

After presenting the validated pipeline, you MUST provide usage instructions. This is NOT optional.

**Required format:**
```
## Usage Instructions

### Required CI/CD Variables

Configure these variables in **Settings → CI/CD → Variables**:

| Variable | Description | Masked | Protected |
|----------|-------------|--------|-----------|
| [VARIABLE_NAME] | [Description] | Yes/No | Yes/No |

### Setup Steps

1. [First setup step]
2. [Second setup step]
...

### Pipeline Behavior

- **On push to `develop`:** [What happens]
- **On push to `main`:** [What happens]
- **On tag `vX.Y.Z`:** [What happens]

### Customization

[Any customization notes]
```

**Example usage instructions:**

```
## Usage Instructions

### Required CI/CD Variables

Configure these variables in **Settings → CI/CD → Variables**:

| Variable | Description | Masked | Protected |
|----------|-------------|--------|-----------|
| `KUBE_CONTEXT` | Kubernetes cluster context name | No | Yes |
| `KUBE_NAMESPACE_STAGING` | Staging namespace (default: staging) | No | No |
| `KUBE_NAMESPACE_PRODUCTION` | Production namespace (default: production) | No | Yes |

**Note:** `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`, and `CI_REGISTRY` are automatically provided by GitLab.

### Kubernetes Integration Setup

1. **Enable Kubernetes integration** in **Settings → Infrastructure → Kubernetes clusters**
2. **Add your cluster** using the agent-based or certificate-based method
3. **Create namespaces** for staging and production if they don't exist:
   ```bash
   kubectl create namespace staging
   kubectl create namespace production
   ```
4. **Ensure deployment exists** in the target namespaces before running the pipeline

### Pipeline Behavior

- **On push to `develop`:** Runs tests → builds Docker image → deploys to staging automatically
- **On push to `main`:** Runs tests → builds Docker image → manual deployment to production
- **On tag `vX.Y.Z`:** Runs tests → builds Docker image → manual deployment to production

### Customization

- Update `APP_NAME` variable to match your Kubernetes deployment name
- Modify environment URLs in `deploy-staging` and `deploy-production` jobs
- Add Helm deployment by uncommenting the Helm jobs in the template
```

## Best Practices to Enforce

Reference `references/best-practices.md` for comprehensive guidelines. Key principles:

### Mandatory Standards

1. **Security First:**
   - Pin Docker images to specific versions (not :latest)
   - Use masked variables for secrets ($CI_REGISTRY_PASSWORD should be masked)
   - Never expose secrets in logs
   - Validate inputs and sanitize variables
   - Use protected variables for sensitive environments

2. **Performance:**
   - Implement caching for dependencies (ALWAYS for npm, pip, maven, etc.)
   - Use `needs` keyword for DAG optimization (ALWAYS when jobs have dependencies)
   - Set artifact expiration to avoid storage bloat (ALWAYS set `expire_in`)
   - Use `parallel` execution *when applicable* (only if test framework supports sharding)
   - Minimize unnecessary artifact passing (use `artifacts: false` in `needs` when not needed)

3. **Reliability:**
   - **Set explicit `timeout` for ALL jobs** (prevents hanging jobs, typically 10-30 minutes)
     - Even when using `default` or `extends` for timeout inheritance, add explicit `timeout` to each job
     - This improves readability and avoids validator warnings about missing timeout
     - Example: A job using `.deploy-template` should still have `timeout: 15 minutes` explicitly set
   - Add retry logic for flaky operations (network calls, external API interactions)
   - Use `allow_failure` appropriately for non-critical jobs (linting, optional scans)
   - Use `resource_group` for deployment jobs (prevents concurrent deployments)
   - Add `interruptible: true` for test jobs (allows cancellation when new commits push)

4. **Naming:**
   - Job names: Descriptive, kebab-case (e.g., "build-application", "test-unit")
   - Stage names: Short, clear (e.g., "build", "test", "deploy")
   - Variable names: UPPER_SNAKE_CASE for environment variables
   - Environment names: lowercase (e.g., "production", "staging")

5. **Configuration Organization:**
   - Use `extends` for reusable configuration (PREFERRED over YAML anchors for GitLab CI)
   - Use `include` for modular pipeline files (organize large pipelines into multiple files)
   - Use `rules` instead of deprecated only/except (ALWAYS)
   - Define `default` settings for common configurations (image, timeout, cache, tags)
   - Use YAML anchors *only when necessary* for complex repeated structures within a single file
     - Note: `extends` is preferred because it provides better visualization in GitLab UI

6. **Error Handling:**
   - Set appropriate timeout values (ALWAYS - prevents hanging jobs)
   - Configure retry behavior for flaky operations (network calls, external APIs)
   - Use `allow_failure: true` for non-blocking jobs (linting, optional scans)
   - Add cleanup steps with `after_script` *when needed* (e.g., stopping test containers, cleanup)
   - Implement notification mechanisms *when required* (e.g., Slack integration for deployment failures)

## Resources

### References (Tiered Loading)

- `references/best-practices.md` (**Tier 1: required for all**) - Comprehensive GitLab CI/CD best practices
  - Security patterns, performance optimization
  - Pipeline design, configuration organization
  - Common patterns and anti-patterns
  - **Use this:** When implementing any GitLab CI/CD resource

- `references/common-patterns.md` (**Tier 1: required for all**) - Frequently used pipeline patterns
  - Basic CI pipeline patterns
  - Docker build and push patterns
  - Deployment patterns (K8s, cloud platforms)
  - Multi-project and parent-child patterns
  - **Use this:** When selecting which pattern to use

- `references/gitlab-ci-reference.md` (**Tier 2: required for Full mode**) - GitLab CI/CD YAML syntax reference
  - Complete keyword reference
  - Job configuration options
  - Rules and conditional execution
  - Variables and environments
  - **Use this:** For syntax and keyword details

- `references/security-guidelines.md` (**Tier 2: required for Full mode**) - Security best practices
  - Secrets management
  - Image security
  - Script security
  - Artifact security
  - **Use this:** For security-sensitive configurations

### Assets (Templates to Customize)

- `assets/templates/basic-pipeline.yml` - Complete basic pipeline template
- `assets/templates/docker-build.yml` - Docker build pipeline template
- `assets/templates/kubernetes-deploy.yml` - Kubernetes deployment template
- `assets/templates/multi-project.yml` - Multi-project orchestration template

**How to use templates:**
1. Copy the relevant template structure
2. Replace all `[PLACEHOLDERS]` with actual values
3. Customize logic based on user requirements
4. Remove unnecessary sections
5. Validate the result

## Typical Workflow Example

**User request:** "Create a CI/CD pipeline for a Node.js app with testing and Docker deployment"

**Process:**
1. ✅ Understand requirements:
   - Node.js application
   - Run tests (unit, lint)
   - Build Docker image
   - Deploy to container registry
   - Trigger on push and merge requests

2. ✅ Reference resources:
   - Check `references/best-practices.md` for pipeline structure
   - Check `references/common-patterns.md` for Node.js + Docker pattern
   - Use `assets/templates/docker-build.yml` as base

3. ✅ Generate pipeline:
   - Define stages (build, test, dockerize, deploy)
   - Create build job with caching
   - Create test jobs (unit, lint) with needs optimization
   - Create Docker build job
   - Add proper artifact management
   - Pin Docker images to versions
   - Include proper secrets handling

4. ✅ Validate:
   - Invoke `devops-skills:gitlab-ci-validator` skill
   - Fix any reported issues
   - Re-validate if needed

5. ✅ Present to user:
   - Show validated pipeline
   - Explain key sections
   - Provide usage instructions
   - Mention successful validation

## Common Pipeline Patterns

### Basic Three-Stage Pipeline
```yaml
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script: make build

test-job:
  stage: test
  script: make test

deploy-job:
  stage: deploy
  script: make deploy
  when: manual
```

### DAG Pipeline with Needs
```yaml
stages:
  - build
  - test
  - deploy

build-frontend:
  stage: build
  script: npm run build:frontend

build-backend:
  stage: build
  script: npm run build:backend

test-frontend:
  stage: test
  needs: [build-frontend]
  script: npm test:frontend

test-backend:
  stage: test
  needs: [build-backend]
  script: npm test:backend

deploy:
  stage: deploy
  needs: [test-frontend, test-backend]
  script: make deploy
```

### Conditional Execution with Rules
```yaml
deploy-staging:
  script: deploy staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
      when: always
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual

deploy-production:
  script: deploy production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
    - when: never
```

### Matrix Parallel Jobs
```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
        OS: ['ubuntu', 'alpine']
  image: node:${NODE_VERSION}-${OS}
  script:
    - npm test
```

## Error Messages and Troubleshooting

### If devops-skills:gitlab-ci-validator reports errors:

1. **Syntax errors:** Fix YAML formatting, indentation, or structure
2. **Job reference errors:** Ensure referenced jobs exist in needs/dependencies
3. **Stage errors:** Verify all job stages are defined in stages list
4. **Rule errors:** Check rules syntax and variable references
5. **Security warnings:** Address hardcoded secrets and image pinning

### If GitLab documentation is not found:

1. Try Context7 first: `mcp__context7__resolve-library-id` -> `mcp__context7__query-docs`
2. If needed, run `web.search_query` scoped to `docs.gitlab.com`
3. Open specific pages with `web.open` and extract only required syntax/variables
4. If offline, continue with local references and add version-assumption notes

---

## PRE-DELIVERY CHECKLIST

**MANDATORY:** Before presenting ANY generated pipeline to the user, verify ALL items:

### Mode and References
- [ ] Complexity mode selected (`Targeted`, `Lightweight`, or `Full`)
- [ ] For **Targeted** mode: only directly relevant files/references loaded
- [ ] For **Lightweight/Full** modes: read `references/best-practices.md` before generating
- [ ] For **Lightweight/Full** modes: read `references/common-patterns.md` before generating
- [ ] For **Lightweight/Full** modes: read appropriate template from `assets/templates/` for the pipeline type
- [ ] For **Full** mode: read `references/gitlab-ci-reference.md`
- [ ] For **Full** mode: read `references/security-guidelines.md`
- [ ] **Output explicit confirmation statement** for Lightweight/Full modes

### Generation Standards Applied
- [ ] All Docker images pinned to specific versions (no `:latest`)
- [ ] All jobs have explicit `timeout` (10-30 minutes typically)
- [ ] `default` block includes `timeout` if defined
- [ ] Hidden templates (`.template-name`) include `timeout`
- [ ] Caching configured for dependency installation
- [ ] `needs` keyword used for DAG optimization where appropriate
- [ ] `rules` used (not deprecated `only`/`except`)
- [ ] `resource_group` configured for deployment jobs
- [ ] Artifacts have `expire_in` set
- [ ] Secrets use masked CI/CD variables (not hardcoded)

### Validation Completed
- [ ] Validation executed via `devops-skills:gitlab-ci-validator` or script fallback
- [ ] Zero CRITICAL issues
- [ ] Zero HIGH issues
- [ ] **MEDIUM issues addressed** (fixed OR explained in output using required format)
- [ ] **LOW issues acknowledged** (listed in output)
- [ ] **Suggestions reviewed** (using required format)
- [ ] Re-validated after any fixes
- [ ] If only manual fallback was available: output marked as not fully verified

### Presentation Ready
- [ ] Validation status stated clearly
- [ ] Validation path stated clearly (skill, script fallback, or manual fallback)
- [ ] **MEDIUM/LOW issues explained** (with table format)
- [ ] **Suggestions review provided** (with table format)
- [ ] **Template and version notes provided** (with required format)
- [ ] **Usage instructions provided** (with required sections)
- [ ] Key sections explained

**If any checkbox is unchecked, DO NOT present the pipeline. Complete the missing steps first.**

### Required Output Sections

Use the smallest valid output profile for the selected mode.

**Full mode (complete/complex pipeline):**
1. **Reference Analysis Complete** (from Step 3)
2. **Generated Pipeline** (the `.gitlab-ci.yml` content)
3. **Validation Results Summary** (pass/fail status)
4. **Validation Issues Addressed** (MEDIUM issues table)
5. **Validator Suggestions Review** (suggestions table)
6. **Template and Version Notes** (template base + freshness/version assumptions)
7. **Usage Instructions** (variables, setup, behavior)

**Lightweight mode (complete/simple pipeline):**
1. **Reference Analysis Complete (Lightweight)**
2. **Generated Pipeline**
3. **Validation Results Summary**
4. **Template and Version Notes**
5. **Usage Instructions**
- Add **Validation Issues Addressed** only when MEDIUM issues exist.
- Add **Validator Suggestions Review** only when suggestions are present.

**Targeted mode (review/Q&A/snippet/focused fix):**
- Provide only the directly requested artifact/answer and a concise rationale.
- Include validation/fallback disclosure if validation was not run.
- Do not force full pipeline-generation sections.

## Done Criteria

This skill execution is done when:
- Simple requests use **Lightweight mode** without unnecessary Tier 2 loading.
- Complex requests use **Full mode** with Tier 2 references and complete confirmation.
- Validation enforces strict Critical/High gates before production-ready claims.
- Output includes template/version freshness notes plus usage instructions.
- Any fallback path is explicit and does not hide verification gaps.

---

## Summary

Always follow this sequence when generating GitLab CI/CD pipelines:

1. **Classify Complexity** - choose `Targeted`, `Lightweight`, or `Full` mode.
2. **Load References** - use tiered loading:
   - For `Targeted` mode, load only directly relevant files.
   - For `Lightweight/Full` modes, load:
     - `references/best-practices.md`
     - `references/common-patterns.md`
     - Plus the appropriate template from `assets/templates/`
   - For `Full` mode, also load:
     - `references/gitlab-ci-reference.md`
     - `references/security-guidelines.md`
3. **Confirm** - Output targeted response or Lightweight/Full reference analysis as required by mode.
4. **Generate** - Use templates and follow standards (security, caching, naming, explicit timeout on ALL jobs).
5. **Lookup Docs When Needed** - Context7 first, then `web.search_query`/`web.open`, with offline fallback notes when constrained.
6. **Validate** - Use `devops-skills:gitlab-ci-validator`, script fallback if needed.
7. **Fix** - Resolve all Critical/High issues, address Medium issues.
8. **Verify Checklist** - Confirm all pre-delivery checklist items.
9. **Present** - Deliver output with validation summary, template/version notes, and usage instructions.

Generate GitLab CI/CD pipelines that are:
- ✅ Secure with pinned images and proper secrets handling
- ✅ Following current best practices and conventions
- ✅ Using proper configuration organization (extends, includes)
- ✅ Optimized for performance (caching, needs, DAG)
- ✅ Properly documented with usage instructions
- ✅ Validated with zero Critical/High issues
- ✅ Production-ready and maintainable

---

## Reference: Best Practices

# GitLab CI/CD Best Practices

This document outlines comprehensive best practices for creating production-ready, secure, and efficient GitLab CI/CD pipelines.

## Table of Contents

1. [Security Best Practices](#security-best-practices)
2. [Performance Optimization](#performance-optimization)
3. [Configuration Organization](#configuration-organization)
4. [Reliability and Error Handling](#reliability-and-error-handling)
5. [Naming Conventions](#naming-conventions)
6. [Pipeline Architecture](#pipeline-architecture)
7. [Common Anti-Patterns](#common-anti-patterns)

---

## Security Best Practices

### 1. Docker Image Pinning

**Always pin Docker images to specific versions** to ensure reproducibility and security.

```yaml
# ❌ BAD: Using :latest tag
test-job:
  image: node:latest
  script: npm test

# ✅ GOOD: Pinned to specific version
test-job:
  image: node:20.11-alpine3.19
  script: npm test
```

**Best practices:**
- Pin to major.minor.patch versions
- Use official images from trusted registries
- Regularly update pinned versions
- Document why specific versions are chosen

### 2. Secrets and Variables Management

**Never hardcode secrets** in your `.gitlab-ci.yml` file. Use GitLab CI/CD variables instead.

```yaml
# ❌ BAD: Hardcoded credentials
deploy:
  script:
    - deploy --token abc123xyz

# ✅ GOOD: Using masked variables
deploy:
  script:
    - deploy --token $DEPLOY_TOKEN
```

**Best practices:**
- Mark sensitive variables as **Masked** and **Protected**
- Use project/group CI/CD variables for secrets
- Rotate secrets regularly
- Use `$CI_JOB_TOKEN` for GitLab API operations
- Limit variable scope to specific environments

### 3. Artifact Security

**Be careful with artifact paths** to avoid exposing sensitive files.

```yaml
# ❌ BAD: Overly broad artifact paths
build:
  artifacts:
    paths:
      - ./**  # Exposes everything including .env files

# ✅ GOOD: Specific artifact paths
build:
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - "**/*.env"
      - "**/*.pem"
      - "**/credentials.*"
    expire_in: 1 hour
```

**Best practices:**
- Be explicit about artifact paths
- Use `exclude` to prevent sensitive files
- Set appropriate expiration times
- Use `artifacts:reports` for test/coverage reports
- Don't include node_modules or vendor directories

### 4. Script Security

**Avoid dangerous script patterns** that can introduce security vulnerabilities.

```yaml
# ❌ BAD: Dangerous patterns
install:
  script:
    - curl https://install.sh | bash  # Pipe to bash
    - eval "$COMMAND"  # Code injection risk
    - chmod 777 /app  # Overly permissive

# ✅ GOOD: Secure patterns
install:
  script:
    - curl -o install.sh https://install.sh
    - sha256sum -c install.sh.sha256  # Verify integrity
    - bash install.sh
```

**Best practices:**
- Never pipe curl directly to bash
- Validate downloaded scripts
- Use minimal file permissions
- Sanitize user inputs
- Avoid `eval` and similar dynamic execution

### 5. Protected Branches and Environments

Configure protected branches and environments for critical deployments.

```yaml
deploy-production:
  stage: deploy
  script:
    - deploy production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_TAG == null
  when: manual
  resource_group: production
```

**Best practices:**
- Require manual approval for production deployments
- Use protected environments
- Restrict who can deploy to production
- Use resource_group to prevent concurrent deployments
- Implement approval rules in GitLab

---

## Performance Optimization

### 1. Caching Strategies

**Use cache to speed up repeated operations** like dependency installation.

```yaml
# ✅ GOOD: Comprehensive caching
variables:
  CACHE_VERSION: "v1"  # Bump to invalidate cache

default:
  cache:
    key: ${CACHE_VERSION}-${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
    policy: pull

build:
  stage: build
  script:
    - npm ci
    - npm run build
  cache:
    key: ${CACHE_VERSION}-${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
    policy: pull-push  # Push after installing

test:
  stage: test
  script:
    - npm test
  cache:
    key: ${CACHE_VERSION}-${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull  # Only pull, don't push
```

**Cache best practices:**
- Use appropriate cache keys (branch, commit, files)
- Set `policy: pull` for jobs that only read cache
- Set `policy: pull-push` for jobs that update cache
- Cache language-specific directories (node_modules/, vendor/, .gradle/)
- Use `CACHE_VERSION` variable for cache invalidation
- Don't cache build artifacts (use artifacts instead)

### 2. DAG Optimization with `needs`

**Use the `needs` keyword** to create Directed Acyclic Graphs for faster pipelines.

```yaml
stages:
  - build
  - test
  - deploy

# Without needs: runs sequentially (slow)
build-frontend:
  stage: build
  script: build frontend

build-backend:
  stage: build
  script: build backend

test-frontend:
  stage: test
  script: test frontend

test-backend:
  stage: test
  script: test backend

# ✅ With needs: runs in parallel (fast)
build-frontend:
  stage: build
  script: build frontend

build-backend:
  stage: build
  script: build backend

test-frontend:
  stage: test
  needs: [build-frontend]  # Can start as soon as build-frontend finishes
  script: test frontend

test-backend:
  stage: test
  needs: [build-backend]  # Can start as soon as build-backend finishes
  script: test backend

deploy:
  stage: deploy
  needs: [test-frontend, test-backend]  # Only depends on tests
  script: deploy
```

**Benefits:**
- Pipelines run faster by parallelizing independent jobs
- Reduces waiting time between stages
- Clear dependency visualization

### 3. Parallel Execution

**Use parallel jobs** for matrix testing or splitting workloads.

```yaml
# Parallel with matrix
test:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
        OS: ['ubuntu', 'alpine']
  image: node:${NODE_VERSION}-${OS}
  script:
    - npm test

# Parallel with index
test-split:
  parallel: 4
  script:
    - npm test -- --shard=${CI_NODE_INDEX}/${CI_NODE_TOTAL}
```

### 4. Artifact Optimization

**Minimize artifact size** and set appropriate expiration.

```yaml
build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    exclude:
      - dist/**/*.map  # Exclude source maps if not needed
    expire_in: 1 hour  # Short expiration for intermediate artifacts

deploy:
  stage: deploy
  needs: [build]
  script:
    - deploy dist/
```

**Best practices:**
- Set short expiration for intermediate artifacts (1 hour - 1 day)
- Set longer expiration for release artifacts (1 week - 1 month)
- Use `artifacts:reports` for test/coverage reports
- Exclude unnecessary files
- Compress large artifacts

---

## Configuration Organization

### 1. Using `extends` for Reusability

**Use `extends` to reduce duplication** and create maintainable configurations.

```yaml
# Hidden template jobs (prefixed with .)
.node-base:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci

.deploy-base:
  before_script:
    - echo "Deploying to ${ENVIRONMENT}"
  retry:
    max: 2
    when:
      - runner_system_failure
  resource_group: ${ENVIRONMENT}

# Actual jobs extending templates
build:
  extends: .node-base
  stage: build
  script:
    - npm run build

test:
  extends: .node-base
  stage: test
  script:
    - npm test

deploy-staging:
  extends: .deploy-base
  stage: deploy
  variables:
    ENVIRONMENT: staging
  script:
    - ./deploy.sh staging

deploy-production:
  extends: .deploy-base
  stage: deploy
  variables:
    ENVIRONMENT: production
  script:
    - ./deploy.sh production
  when: manual
```

### 2. Using `include` for Modular Configuration

**Split large configurations** into multiple files using `include`.

```yaml
# .gitlab-ci.yml (main file)
include:
  - local: '.gitlab/ci/templates.yml'
  - local: '.gitlab/ci/build-jobs.yml'
  - local: '.gitlab/ci/test-jobs.yml'
  - local: '.gitlab/ci/deploy-jobs.yml'

stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"
```

```yaml
# .gitlab/ci/templates.yml
.node-base:
  image: node:${NODE_VERSION}-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci
```

### 3. Using YAML Anchors

**Use YAML anchors** for complex repeated structures within a file.

```yaml
# Define anchor
.retry-config: &retry-config
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure

# Use anchor
deploy-staging:
  stage: deploy
  <<: *retry-config
  script:
    - deploy staging

deploy-production:
  stage: deploy
  <<: *retry-config
  script:
    - deploy production
```

### 4. Using `default` for Common Settings

**Set default values** for all jobs using the `default` keyword.

```yaml
default:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - echo "Starting job ${CI_JOB_NAME}"
  retry:
    max: 1
    when:
      - runner_system_failure
  tags:
    - docker
  interruptible: true

# Jobs inherit default settings
build:
  stage: build
  script: npm run build

test:
  stage: test
  script: npm test
```

---

## Reliability and Error Handling

### 1. Retry Configuration

**Configure retry for flaky operations** to improve reliability.

```yaml
# Retry on specific failures
test-integration:
  script:
    - npm run test:integration
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
      - api_failure

# Conditional retry
deploy:
  script:
    - deploy.sh
  retry:
    max: 2
    when: always
```

**Retry scenarios:**
- Network-dependent operations
- External API calls
- Integration tests
- Deployment operations
- Runner system failures

### 2. Timeout Settings

**Set appropriate timeouts** to prevent jobs from hanging.

```yaml
# Global default timeout (project settings)
# Job-specific timeout
test-quick:
  script: npm run test:unit
  timeout: 10 minutes

test-e2e:
  script: npm run test:e2e
  timeout: 30 minutes

deploy:
  script: deploy.sh
  timeout: 15 minutes
```

### 3. Allow Failure

**Use `allow_failure` strategically** for non-critical jobs.

```yaml
# Job can fail without blocking pipeline
lint:
  script: npm run lint
  allow_failure: true

# Conditional allow_failure
test-experimental:
  script: npm run test:experimental
  allow_failure:
    exit_codes: [1, 137]
```

### 4. Interruptible Jobs

**Mark test jobs as interruptible** to save resources.

```yaml
test:
  script: npm test
  interruptible: true  # Can be canceled if new pipeline starts

deploy:
  script: deploy.sh
  interruptible: false  # Should not be canceled
```

### 5. After Script for Cleanup

**Use `after_script` for cleanup operations** that always run.

```yaml
test:
  script:
    - npm test
  after_script:
    - echo "Cleaning up..."
    - docker stop test-container || true
    - rm -rf temp/
```

---

## Naming Conventions

### Job Names

**Use descriptive, action-oriented names** in kebab-case.

```yaml
# ✅ GOOD: Clear, descriptive names
build-frontend:
  script: npm run build:frontend

test-unit:
  script: npm run test:unit

test-integration:
  script: npm run test:integration

deploy-staging:
  script: deploy staging

# ❌ BAD: Vague names
job1:
  script: npm build

job2:
  script: npm test
```

### Stage Names

**Use short, standard stage names**.

```yaml
stages:
  - build      # ✅ Standard, clear
  - test       # ✅ Standard, clear
  - deploy     # ✅ Standard, clear
  - .pre       # ✅ GitLab special stage
  - .post      # ✅ GitLab special stage
```

### Variable Names

**Use UPPER_SNAKE_CASE for variables**.

```yaml
variables:
  NODE_VERSION: "20"
  DOCKER_DRIVER: overlay2
  CACHE_VERSION: "v1"
  DEPLOY_ENVIRONMENT: staging
```

### Environment Names

**Use lowercase for environment names**.

```yaml
deploy-staging:
  environment:
    name: staging  # ✅ lowercase
    url: https://staging.example.com

deploy-production:
  environment:
    name: production  # ✅ lowercase
    url: https://example.com
```

---

## Pipeline Architecture

### 1. Basic Three-Stage Pipeline

**Simple, linear pipeline** for straightforward projects.

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script: make build

test:
  stage: test
  script: make test

deploy:
  stage: deploy
  script: make deploy
  when: manual
```

**Use when:**
- Simple projects with linear workflows
- Few dependencies between jobs
- Quick prototyping

### 2. DAG Pipeline with Needs

**Optimized pipeline** for complex projects with independent components.

```yaml
stages:
  - build
  - test
  - security
  - deploy

build-frontend:
  stage: build
  script: build frontend

build-backend:
  stage: build
  script: build backend

test-frontend:
  stage: test
  needs: [build-frontend]
  script: test frontend

test-backend:
  stage: test
  needs: [build-backend]
  script: test backend

security-scan:
  stage: security
  needs: []  # Runs immediately
  script: security scan

deploy:
  stage: deploy
  needs: [test-frontend, test-backend, security-scan]
  script: deploy
```

**Use when:**
- Large projects with multiple components
- Need faster pipeline execution
- Clear dependencies between jobs

### 3. Parent-Child Pipelines

**Hierarchical pipelines** for monorepos or complex orchestration.

```yaml
# Parent pipeline
stages:
  - trigger

trigger-frontend:
  stage: trigger
  trigger:
    include: frontend/.gitlab-ci.yml
    strategy: depend

trigger-backend:
  stage: trigger
  trigger:
    include: backend/.gitlab-ci.yml
    strategy: depend
```

**Use when:**
- Monorepo with multiple projects
- Need isolated pipeline configurations
- Complex orchestration scenarios

### 4. Multi-Project Pipelines

**Cross-project orchestration** triggering other projects.

```yaml
trigger-downstream:
  stage: deploy
  trigger:
    project: group/downstream-project
    branch: main
    strategy: depend
```

**Use when:**
- Microservices deployment
- Library updates triggering dependent projects
- Complex multi-project workflows

---

## Common Anti-Patterns

### 1. Using `:latest` Tag

```yaml
# ❌ ANTI-PATTERN
test:
  image: node:latest
  script: npm test

# ✅ CORRECT
test:
  image: node:20.11-alpine3.19
  script: npm test
```

### 2. Hardcoding Secrets

```yaml
# ❌ ANTI-PATTERN
deploy:
  script:
    - deploy --api-key abc123xyz

# ✅ CORRECT
deploy:
  script:
    - deploy --api-key $API_KEY
```

### 3. Using Deprecated `only`/`except`

```yaml
# ❌ ANTI-PATTERN
deploy:
  only:
    - main
  except:
    - tags

# ✅ CORRECT
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_TAG == null
```

### 4. Not Using Cache

```yaml
# ❌ ANTI-PATTERN (installs dependencies every time)
test:
  script:
    - npm install
    - npm test

# ✅ CORRECT (caches node_modules)
test:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  script:
    - npm ci
    - npm test
```

### 5. No Artifact Expiration

```yaml
# ❌ ANTI-PATTERN (artifacts stored forever)
build:
  artifacts:
    paths:
      - dist/

# ✅ CORRECT (artifacts expire)
build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour
```

### 6. Missing Resource Groups for Deployments

```yaml
# ❌ ANTI-PATTERN (concurrent deployments possible)
deploy-production:
  script: deploy production

# ✅ CORRECT (prevents concurrent deployments)
deploy-production:
  script: deploy production
  resource_group: production
```

### 7. Overly Broad Artifact Paths

```yaml
# ❌ ANTI-PATTERN
build:
  artifacts:
    paths:
      - ./**  # Includes everything

# ✅ CORRECT
build:
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - "**/*.env"
```

### 8. Not Using Needs for DAG Optimization

```yaml
# ❌ ANTI-PATTERN (waits for all stage jobs)
stages:
  - build
  - test

build-frontend:
  stage: build
  script: build frontend

build-backend:
  stage: build
  script: build backend

test-frontend:
  stage: test
  script: test frontend  # Waits for build-backend too

# ✅ CORRECT (starts as soon as build-frontend completes)
test-frontend:
  stage: test
  needs: [build-frontend]
  script: test frontend
```

---

## Summary Checklist

When creating GitLab CI/CD pipelines, ensure:

- [ ] Docker images pinned to specific versions
- [ ] Secrets stored in masked CI/CD variables
- [ ] Cache configured for dependencies
- [ ] Artifacts have appropriate expiration times
- [ ] `needs` keyword used for DAG optimization
- [ ] `rules` used instead of deprecated `only`/`except`
- [ ] `resource_group` used for deployment jobs
- [ ] `interruptible: true` for test jobs
- [ ] Retry configured for flaky operations
- [ ] Timeout set for long-running jobs
- [ ] `extends` or `include` used to reduce duplication
- [ ] Descriptive job and stage names
- [ ] Cleanup operations in `after_script`
- [ ] Manual approval for production deployments
- [ ] Security scanning included in pipeline

---

**Reference this document when generating or reviewing GitLab CI/CD pipelines to ensure best practices are followed.**

---

## Reference: Common Patterns

# GitLab CI/CD Common Patterns

This document provides ready-to-use patterns for common GitLab CI/CD scenarios. Use these patterns as starting points and customize them for your specific needs.

## Table of Contents

1. [Basic CI Pipeline Patterns](#basic-ci-pipeline-patterns)
2. [Docker Build and Push Patterns](#docker-build-and-push-patterns)
3. [Kubernetes Deployment Patterns](#kubernetes-deployment-patterns)
4. [Testing Patterns](#testing-patterns)
5. [Deployment Patterns](#deployment-patterns)
6. [Multi-Project Pipeline Patterns](#multi-project-pipeline-patterns)
7. [Parent-Child Pipeline Patterns](#parent-child-pipeline-patterns)
8. [Monorepo Patterns](#monorepo-patterns)
9. [Template and Reusability Patterns](#template-and-reusability-patterns)

---

## Basic CI Pipeline Patterns

### Pattern 1: Simple Three-Stage Pipeline

**Use case:** Basic projects with build, test, and deploy stages.

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"

build-job:
  stage: build
  image: node:${NODE_VERSION}-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test-job:
  stage: test
  image: node:${NODE_VERSION}-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull
  script:
    - npm ci
    - npm test

deploy-job:
  stage: deploy
  image: alpine:3.19
  script:
    - apk add --no-cache rsync openssh
    - rsync -avz dist/ $DEPLOY_SERVER:/var/www/html/
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
```

### Pattern 2: Multi-Language Build Pipeline

**Use case:** Projects with multiple language components.

```yaml
stages:
  - build
  - test
  - deploy

build-frontend:
  stage: build
  image: node:20-alpine
  script:
    - cd frontend
    - npm ci
    - npm run build
  artifacts:
    paths:
      - frontend/dist/
    expire_in: 1 hour

build-backend:
  stage: build
  image: golang:1.22-alpine
  script:
    - cd backend
    - go build -o app
  artifacts:
    paths:
      - backend/app
    expire_in: 1 hour

test-frontend:
  stage: test
  image: node:20-alpine
  needs: [build-frontend]
  script:
    - cd frontend
    - npm ci
    - npm test

test-backend:
  stage: test
  image: golang:1.22-alpine
  needs: [build-backend]
  script:
    - cd backend
    - go test ./...
```

---

## Docker Build and Push Patterns

### Pattern 1: Docker Build with Multi-Stage

**Use case:** Building and pushing Docker images to GitLab Container Registry.

```yaml
stages:
  - build
  - push

variables:
  DOCKER_DRIVER: overlay2
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  DOCKER_TLS_CERTDIR: "/certs"

build-docker-image:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build
        --cache-from $IMAGE_NAME:latest
        --tag $IMAGE_NAME:$CI_COMMIT_SHORT_SHA
        --tag $IMAGE_NAME:latest
        --build-arg VERSION=$CI_COMMIT_SHORT_SHA
        .
    - docker push $IMAGE_NAME:$CI_COMMIT_SHORT_SHA
    - docker push $IMAGE_NAME:latest
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Alternative: Build and push with tags
push-release-image:
  stage: push
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build --tag $IMAGE_NAME:$CI_COMMIT_TAG .
    - docker push $IMAGE_NAME:$CI_COMMIT_TAG
  rules:
    - if: $CI_COMMIT_TAG
```

### Pattern 2: Docker Build with Kaniko (Rootless)

**Use case:** Building Docker images without Docker-in-Docker (more secure).

```yaml
stages:
  - build

variables:
  IMAGE_NAME: $CI_REGISTRY_IMAGE

docker-build-kaniko:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:v1.21.0-debug
    entrypoint: [""]
  script:
    - mkdir -p /kaniko/.docker
    - echo "{\"auths\":{\"${CI_REGISTRY}\":{\"auth\":\"$(printf "%s:%s" "${CI_REGISTRY_USER}" "${CI_REGISTRY_PASSWORD}" | base64 | tr -d '\n')\"}}}" > /kaniko/.docker/config.json
    - /kaniko/executor
        --context "${CI_PROJECT_DIR}"
        --dockerfile "${CI_PROJECT_DIR}/Dockerfile"
        --destination "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}"
        --destination "${IMAGE_NAME}:latest"
        --cache=true
        --cache-ttl=24h
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Pattern 3: Multi-Platform Docker Build

**Use case:** Building Docker images for multiple architectures.

```yaml
stages:
  - build

variables:
  DOCKER_DRIVER: overlay2

build-multiarch:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker buildx create --use
  script:
    - docker buildx build
        --platform linux/amd64,linux/arm64
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
        --tag $CI_REGISTRY_IMAGE:latest
        --push
        .
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

---

## Kubernetes Deployment Patterns

### Pattern 1: kubectl Deployment

**Use case:** Deploying to Kubernetes using kubectl.

```yaml
stages:
  - build
  - deploy

variables:
  KUBE_NAMESPACE: production
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

deploy-k8s:
  stage: deploy
  image: bitnami/kubectl:1.29
  before_script:
    - kubectl config use-context $KUBE_CONTEXT
    - kubectl config set-context --current --namespace=$KUBE_NAMESPACE
  script:
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$IMAGE_TAG
    - kubectl rollout status deployment/myapp --timeout=5m
  environment:
    name: production
    url: https://example.com
    kubernetes:
      namespace: $KUBE_NAMESPACE
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
  resource_group: k8s-production
```

### Pattern 2: Helm Deployment

**Use case:** Deploying to Kubernetes using Helm charts.

```yaml
stages:
  - build
  - deploy

variables:
  HELM_CHART_PATH: ./helm/mychart
  RELEASE_NAME: myapp

deploy-helm-staging:
  stage: deploy
  image: alpine/helm:3.14.0
  before_script:
    - kubectl config use-context $KUBE_CONTEXT
  script:
    - helm upgrade --install $RELEASE_NAME $HELM_CHART_PATH
        --namespace staging
        --create-namespace
        --set image.tag=$CI_COMMIT_SHORT_SHA
        --set environment=staging
        --wait
        --timeout 5m
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-helm-production:
  stage: deploy
  image: alpine/helm:3.14.0
  before_script:
    - kubectl config use-context $KUBE_CONTEXT
  script:
    - helm upgrade --install $RELEASE_NAME $HELM_CHART_PATH
        --namespace production
        --create-namespace
        --set image.tag=$CI_COMMIT_TAG
        --set environment=production
        --wait
        --timeout 10m
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG
  when: manual
  resource_group: k8s-production
```

### Pattern 3: Kustomize Deployment

**Use case:** Deploying to Kubernetes using Kustomize.

```yaml
stages:
  - deploy

deploy-kustomize:
  stage: deploy
  image:
    name: registry.k8s.io/kubectl:v1.29.1
    entrypoint: [""]
  before_script:
    - kubectl config use-context $KUBE_CONTEXT
  script:
    - cd k8s/overlays/$ENVIRONMENT
    - kustomize edit set image myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - kustomize build . | kubectl apply -f -
    - kubectl rollout status deployment/myapp -n $ENVIRONMENT
  environment:
    name: $ENVIRONMENT
    kubernetes:
      namespace: $ENVIRONMENT
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        ENVIRONMENT: production
  when: manual
```

---

## Testing Patterns

### Pattern 1: Comprehensive Testing Pipeline

**Use case:** Multiple types of tests (unit, integration, e2e).

```yaml
stages:
  - test
  - integration

variables:
  NODE_VERSION: "20"

default:
  image: node:${NODE_VERSION}-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull

test-unit:
  stage: test
  needs: []
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test-lint:
  stage: test
  needs: []
  script:
    - npm ci
    - npm run lint
  allow_failure: true

test-types:
  stage: test
  needs: []
  image: node:${NODE_VERSION}-alpine
  script:
    - npm ci
    - npm run type-check

test-integration:
  stage: integration
  needs: [test-unit]
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgres://testuser:testpass@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  script:
    - npm ci
    - npm run test:integration
  retry:
    max: 2
    when:
      - runner_system_failure
      - api_failure

test-e2e:
  stage: integration
  needs: [test-unit]
  image: cypress/browsers:node-20.11.0-chrome-121.0.6167.85-1-ff-123.0-edge-121.0.2277.83-1
  script:
    - npm ci
    - npm run start:test &
    - npx wait-on http://localhost:3000
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - cypress/videos/
      - cypress/screenshots/
    expire_in: 1 week
```

### Pattern 2: Matrix Testing (Multiple Versions)

**Use case:** Testing across multiple language/platform versions.

```yaml
stages:
  - test

test-matrix:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
        OS: ['alpine', 'bookworm-slim']
  image: node:${NODE_VERSION}-${OS}
  script:
    - node --version
    - npm --version
    - npm ci
    - npm test
```

### Pattern 3: Security Scanning

**Use case:** SAST, dependency scanning, container scanning.

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

stages:
  - test
  - security

# Customize SAST
semgrep-sast:
  variables:
    SAST_EXCLUDED_PATHS: "spec, test, tests, tmp"

# Customize dependency scanning
gemnasium-dependency_scanning:
  variables:
    DS_EXCLUDED_PATHS: "node_modules, vendor"

# Container scanning after build
container_scanning:
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  needs: [build-docker-image]
```

---

## Deployment Patterns

### Pattern 1: Multi-Environment Deployment

**Use case:** Deploy to multiple environments (dev, staging, production).

```yaml
stages:
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

.deploy-template:
  image: alpine:3.19
  before_script:
    - apk add --no-cache curl
  script:
    - curl -X POST $DEPLOY_WEBHOOK_URL
        -H "Authorization: Bearer $DEPLOY_TOKEN"
        -d "{\"environment\":\"${ENVIRONMENT}\",\"version\":\"${IMAGE_TAG}\"}"
  resource_group: ${ENVIRONMENT}

deploy-dev:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: development
  environment:
    name: development
    url: https://dev.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-staging:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual

deploy-production:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
  when: manual
  needs: [deploy-staging]
```

### Pattern 2: Blue-Green Deployment

**Use case:** Zero-downtime deployments with blue-green strategy.

```yaml
stages:
  - deploy
  - verify
  - switch

deploy-green:
  stage: deploy
  script:
    - kubectl apply -f k8s/deployment-green.yaml
    - kubectl rollout status deployment/myapp-green -n production
  environment:
    name: production-green
    url: https://green.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual

verify-green:
  stage: verify
  needs: [deploy-green]
  script:
    - curl -f https://green.example.com/health || exit 1
    - npm run test:smoke -- --baseUrl=https://green.example.com
  retry:
    max: 3
    when: always

switch-traffic:
  stage: switch
  needs: [verify-green]
  script:
    - kubectl patch service myapp -n production -p '{"spec":{"selector":{"version":"green"}}}'
    - echo "Traffic switched to green deployment"
  environment:
    name: production
    url: https://example.com
  when: manual
```

### Pattern 3: Canary Deployment

**Use case:** Gradual rollout with traffic splitting.

```yaml
stages:
  - deploy
  - canary

deploy-canary:
  stage: deploy
  script:
    - kubectl apply -f k8s/deployment-canary.yaml
    - kubectl set image deployment/myapp-canary myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  environment:
    name: production-canary
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual

# Increase canary traffic gradually
canary-10-percent:
  stage: canary
  script:
    - kubectl patch virtualservice myapp -n production --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"myapp-stable"},"weight":90},{"destination":{"host":"myapp-canary"},"weight":10}]}]}}'
  needs: [deploy-canary]
  when: manual

canary-50-percent:
  stage: canary
  script:
    - kubectl patch virtualservice myapp -n production --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"myapp-stable"},"weight":50},{"destination":{"host":"myapp-canary"},"weight":50}]}]}}'
  needs: [canary-10-percent]
  when: manual

canary-promote:
  stage: canary
  script:
    - kubectl patch virtualservice myapp -n production --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"myapp-canary"},"weight":100}]}]}}'
    - kubectl set image deployment/myapp-stable myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  needs: [canary-50-percent]
  when: manual
```

---

## Multi-Project Pipeline Patterns

### Pattern 1: Trigger Downstream Projects

**Use case:** Orchestrate multiple project pipelines.

```yaml
stages:
  - build
  - trigger

build-library:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

trigger-dependent-projects:
  stage: trigger
  parallel:
    matrix:
      - PROJECT: ['group/app1', 'group/app2', 'group/app3']
  trigger:
    project: $PROJECT
    branch: main
    strategy: depend
  needs: [build-library]
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Pattern 2: Multi-Project Pipeline with Variables

**Use case:** Pass variables to downstream pipelines.

```yaml
trigger-downstream:
  stage: deploy
  trigger:
    project: group/deployment-project
    branch: main
    strategy: depend
  variables:
    SERVICE_NAME: my-service
    SERVICE_VERSION: $CI_COMMIT_SHORT_SHA
    ENVIRONMENT: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
```

---

## Parent-Child Pipeline Patterns

### Pattern 1: Dynamic Child Pipeline

**Use case:** Generate child pipeline configuration dynamically.

```yaml
stages:
  - generate
  - deploy

generate-child-pipeline:
  stage: generate
  script:
    - python scripts/generate-pipeline.py > generated-pipeline.yml
  artifacts:
    paths:
      - generated-pipeline.yml

trigger-child-pipeline:
  stage: deploy
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-child-pipeline
    strategy: depend
  needs: [generate-child-pipeline]
```

### Pattern 2: Monorepo with Multiple Child Pipelines

**Use case:** Each component has its own pipeline configuration.

```yaml
# Parent .gitlab-ci.yml
stages:
  - trigger

trigger-frontend:
  stage: trigger
  trigger:
    include: frontend/.gitlab-ci.yml
    strategy: depend
  rules:
    - changes:
        - frontend/**/*

trigger-backend:
  stage: trigger
  trigger:
    include: backend/.gitlab-ci.yml
    strategy: depend
  rules:
    - changes:
        - backend/**/*

trigger-infrastructure:
  stage: trigger
  trigger:
    include: infrastructure/.gitlab-ci.yml
    strategy: depend
  rules:
    - changes:
        - infrastructure/**/*
```

---

## Monorepo Patterns

### Pattern 1: Conditional Jobs Based on Changes

**Use case:** Only run jobs for changed components.

```yaml
stages:
  - build
  - test
  - deploy

build-frontend:
  stage: build
  script:
    - cd frontend
    - npm ci
    - npm run build
  rules:
    - changes:
        - frontend/**/*

build-backend:
  stage: build
  script:
    - cd backend
    - go build
  rules:
    - changes:
        - backend/**/*

test-frontend:
  stage: test
  needs: [build-frontend]
  script:
    - cd frontend
    - npm test
  rules:
    - changes:
        - frontend/**/*

test-backend:
  stage: test
  needs: [build-backend]
  script:
    - cd backend
    - go test ./...
  rules:
    - changes:
        - backend/**/*
```

### Pattern 2: Monorepo with Parallel Child Pipelines

**Use case:** Run multiple child pipelines in parallel for different components.

```yaml
stages:
  - trigger

.trigger-template:
  stage: trigger
  trigger:
    strategy: depend

trigger-service-a:
  extends: .trigger-template
  trigger:
    include: services/service-a/.gitlab-ci.yml
  rules:
    - changes:
        - services/service-a/**/*

trigger-service-b:
  extends: .trigger-template
  trigger:
    include: services/service-b/.gitlab-ci.yml
  rules:
    - changes:
        - services/service-b/**/*

trigger-service-c:
  extends: .trigger-template
  trigger:
    include: services/service-c/.gitlab-ci.yml
  rules:
    - changes:
        - services/service-c/**/*
```

---

## Template and Reusability Patterns

### Pattern 1: Global Template Library

**Use case:** Reusable templates across multiple projects.

```yaml
# templates/build-templates.yml
.node-build-template:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

.python-build-template:
  image: python:3.12-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .venv/
  before_script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
  script:
    - python setup.py build
```

```yaml
# Project .gitlab-ci.yml
include:
  - project: 'group/ci-templates'
    file: 'templates/build-templates.yml'

stages:
  - build

build-app:
  extends: .node-build-template
  stage: build
```

### Pattern 2: Local Template with Extends

**Use case:** DRY configuration within a single project.

```yaml
# Hidden template jobs
.deployment-base:
  image: alpine:3.19
  before_script:
    - apk add --no-cache curl
  script:
    - ./scripts/deploy.sh $ENVIRONMENT
  resource_group: ${ENVIRONMENT}
  retry:
    max: 2
    when:
      - runner_system_failure

# Actual deployment jobs
deploy-staging:
  extends: .deployment-base
  stage: deploy
  variables:
    ENVIRONMENT: staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy-production:
  extends: .deployment-base
  stage: deploy
  variables:
    ENVIRONMENT: production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG
  when: manual
```

---

## Summary

These patterns provide a solid foundation for common GitLab CI/CD scenarios. When using these patterns:

1. **Customize** them for your specific needs
2. **Validate** using gitlab-ci-validator skill
3. **Follow** best practices from references/best-practices.md
4. **Test** locally when possible
5. **Document** any modifications

**Remember:** These are starting points. Always adapt them to your project's specific requirements, security policies, and infrastructure.

---

## Reference: Gitlab Ci Reference

# GitLab CI/CD YAML Syntax Reference

Comprehensive reference for GitLab CI/CD `.gitlab-ci.yml` configuration syntax.

## Table of Contents

1. [Global Keywords](#global-keywords)
2. [Job Keywords](#job-keywords)
3. [Script Execution](#script-execution)
4. [Artifacts and Cache](#artifacts-and-cache)
5. [Rules and Conditions](#rules-and-conditions)
6. [Dependencies and Needs](#dependencies-and-needs)
7. [Docker Configuration](#docker-configuration)
8. [Environment and Deployment](#environment-and-deployment)
9. [Advanced Features](#advanced-features)

---

## Global Keywords

Global keywords control pipeline-wide behavior and configuration.

### `stages`

Defines the order of pipeline stages. Jobs in the same stage run in parallel.

```yaml
stages:
  - build
  - test
  - deploy
```

**Default stages:**
```yaml
stages:
  - .pre       # Special stage, runs before everything
  - build
  - test
  - deploy
  - .post      # Special stage, runs after everything
```

### `default`

Sets default values for all jobs. Job-level configurations override defaults completely (no merging).

```yaml
default:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - echo "Starting job"
  tags:
    - docker
  interruptible: true
  retry:
    max: 1
    when:
      - runner_system_failure
```

### `include`

Imports external YAML configuration files.

```yaml
# Local file from same repository
include:
  - local: '.gitlab/ci/build-jobs.yml'

# File from another project
include:
  - project: 'group/ci-templates'
    ref: main
    file: 'templates/build.yml'

# Remote file via HTTP
include:
  - remote: 'https://example.com/ci-template.yml'

# GitLab CI/CD template
include:
  - template: 'Security/SAST.gitlab-ci.yml'

# CI/CD component
include:
  - component: gitlab.com/my-org/components/build@1.0.0
```

### `variables`

Defines CI/CD variables available to all jobs.

```yaml
variables:
  NODE_VERSION: "20"
  DOCKER_DRIVER: overlay2
  CACHE_VERSION: "v1"
```

**Variable types:**
- `$VARIABLE` - Simple substitution
- `${VARIABLE}` - Explicit variable reference
- `$$VARIABLE` - Escaped variable (passed to script)

### `workflow`

Controls when pipelines run and their auto-cancellation behavior.

```yaml
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_MERGE_REQUEST_ID
    - if: $CI_COMMIT_TAG
  auto_cancel:
    on_new_commit: interruptible
```

---

## Job Keywords

Jobs are the basic building blocks that define what to execute.

### Job Structure

```yaml
job-name:
  stage: build
  image: node:20-alpine
  script:
    - npm ci
    - npm run build
```

**Reserved job names:**
- `image`, `services`, `stages`, `before_script`, `after_script`, `variables`, `cache`, `include`

### `stage`

Assigns the job to a pipeline stage.

```yaml
build-job:
  stage: build  # Default: test
  script: make build
```

### `script` (required)

Shell commands to execute. At least one of `script`, `trigger`, or `extends` is required.

```yaml
build:
  script:
    - echo "Building..."
    - make build
    - make package

# Multi-line script
test:
  script:
    - |
      echo "Running tests"
      npm test
      echo "Tests complete"
```

### `before_script`

Commands executed before `script`. Runs in the same shell context as `script`.

```yaml
test:
  before_script:
    - echo "Setting up..."
    - npm ci
  script:
    - npm test
```

### `after_script`

Commands executed after `script`, runs in a separate shell. Cannot affect job exit code.

```yaml
deploy:
  script:
    - deploy.sh
  after_script:
    - echo "Cleaning up..."
    - rm -rf temp/
```

**Note:** `after_script` has a separate 5-minute timeout by default.

### `image`

Docker image for job execution.

```yaml
# Simple image
build:
  image: node:20-alpine

# Image with entrypoint override
test:
  image:
    name: my-image:latest
    entrypoint: [""]
```

### `services`

Docker service containers (databases, caches, etc.).

```yaml
test:
  image: node:20-alpine
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
```

### `tags`

Selects runners with matching tags.

```yaml
deploy:
  tags:
    - docker
    - production
  script: deploy.sh
```

### `when`

Controls when jobs run.

**Values:**
- `on_success` (default) - Run when all previous stage jobs succeed
- `on_failure` - Run when at least one previous stage job fails
- `always` - Always run regardless of status
- `manual` - Requires manual trigger
- `delayed` - Run after delay
- `never` - Don't run

```yaml
cleanup:
  when: always
  script: cleanup.sh

deploy:
  when: manual
  script: deploy.sh

delayed-job:
  when: delayed
  start_in: 30 minutes
  script: echo "Running after delay"
```

### `allow_failure`

Allows job to fail without blocking pipeline.

```yaml
lint:
  script: npm run lint
  allow_failure: true

# Conditional allow_failure
test-experimental:
  script: npm test
  allow_failure:
    exit_codes: [1, 137]
```

### `retry`

Configures automatic retry on failure.

```yaml
# Simple retry
deploy:
  retry: 2

# Advanced retry configuration
integration-test:
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
      - api_failure
```

**Retry conditions:**
- `always` - Retry on any failure
- `runner_system_failure` - Runner system failed
- `stuck_or_timeout_failure` - Job stuck or timed out
- `script_failure` - Script failed
- `api_failure` - API failure
- `unknown_failure` - Unknown failure

### `timeout`

Job-specific timeout override.

```yaml
test-quick:
  timeout: 10 minutes
  script: npm run test:unit

test-e2e:
  timeout: 1 hour
  script: npm run test:e2e
```

### `interruptible`

Marks job as cancellable when superseded by newer pipelines.

```yaml
test:
  interruptible: true  # Can be canceled
  script: npm test

deploy:
  interruptible: false  # Cannot be canceled
  script: deploy.sh
```

### `resource_group`

Limits job concurrency for resource-sensitive operations.

```yaml
deploy-production:
  resource_group: production
  script: deploy.sh

deploy-staging:
  resource_group: staging
  script: deploy.sh
```

### `parallel`

Runs multiple job instances in parallel.

```yaml
# Parallel with count
test:
  parallel: 5
  script: npm test -- --shard=${CI_NODE_INDEX}/${CI_NODE_TOTAL}

# Parallel with matrix
test-matrix:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
        OS: ['alpine', 'bookworm-slim']
  image: node:${NODE_VERSION}-${OS}
  script: npm test
```

---

## Script Execution

### Multiline Scripts

```yaml
# Using |
test:
  script:
    - |
      echo "Line 1"
      echo "Line 2"
      echo "Line 3"

# Using >
deploy:
  script:
    - >
      kubectl apply -f deployment.yaml
      --namespace production
      --timeout 5m
```

### Error Handling in Scripts

```yaml
# Stop on first error (default)
build:
  script:
    - command1
    - command2  # Won't run if command1 fails

# Continue on error
test:
  script:
    - command1 || true
    - command2  # Runs even if command1 fails
```

---

## Artifacts and Cache

### `artifacts`

Files/directories to preserve after job completion.

```yaml
build:
  script: make build
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - "**/*.map"
      - dist/temp/
    expire_in: 1 hour
    when: on_success  # on_success, on_failure, always
    name: "build-${CI_COMMIT_SHORT_SHA}"
```

**Artifact types:**
```yaml
test:
  script: npm test
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      dotenv: build.env
```

**Expiration values:**
- `30 minutes`, `1 hour`, `2 hours`
- `1 day`, `2 days`, `1 week`, `1 month`
- `never` - Keep forever

### `cache`

Preserves files between pipeline runs.

```yaml
build:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
    policy: pull-push
    when: on_success
```

**Cache policies:**
- `pull-push` (default) - Download and upload cache
- `pull` - Only download cache
- `push` - Only upload cache

**Cache keys:**
```yaml
# Branch-based key
cache:
  key: ${CI_COMMIT_REF_SLUG}

# File-based key
cache:
  key:
    files:
      - package-lock.json
    prefix: npm

# Multiple caches
cache:
  - key: npm-cache
    paths:
      - node_modules/
  - key: build-cache
    paths:
      - dist/
```

---

## Rules and Conditions

### `rules`

Determines when to create jobs and which attributes to apply.

```yaml
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: always
    - if: $CI_MERGE_REQUEST_ID
      when: manual
    - when: never  # Default: don't run
```

**Rule clauses:**
- `if` - Variable expressions
- `changes` - File modifications
- `exists` - File existence
- `when` - Execution timing
- `variables` - Dynamic variables
- `allow_failure` - Failure behavior

### Examples

```yaml
# Run on specific branch
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# Run on file changes
test-frontend:
  rules:
    - changes:
        - frontend/**/*

# Run if file exists
docs-build:
  rules:
    - exists:
        - docs/mkdocs.yml

# Complex rules
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_TAG == null
      when: manual
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
      when: on_success
    - when: never
```

### `only` / `except` (Deprecated)

**Note:** Use `rules` instead. `only` and `except` are deprecated.

```yaml
# ❌ Deprecated
deploy:
  only:
    - main
  except:
    - tags

# ✅ Use rules instead
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_TAG == null
```

---

## Dependencies and Needs

### `dependencies`

Restricts artifact downloads from specific jobs.

```yaml
build:
  stage: build
  script: make build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  dependencies: [build]  # Only download artifacts from build
  script: test dist/

deploy:
  stage: deploy
  dependencies: []  # Don't download any artifacts
  script: deploy
```

### `needs`

Creates Directed Acyclic Graph (DAG) for faster pipelines.

```yaml
build-frontend:
  stage: build
  script: build frontend

build-backend:
  stage: build
  script: build backend

test-frontend:
  stage: test
  needs: [build-frontend]  # Starts as soon as build-frontend completes
  script: test frontend

test-backend:
  stage: test
  needs: [build-backend]
  script: test backend

deploy:
  stage: deploy
  needs: [test-frontend, test-backend]
  script: deploy
```

**Needs with artifacts:**
```yaml
deploy:
  needs:
    - job: build
      artifacts: true  # Default
    - job: test
      artifacts: false  # Don't download artifacts
```

---

## Docker Configuration

### Docker-in-Docker (dind)

```yaml
build-docker:
  image: docker:24-dind
  services:
    - docker:24-dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker build -t myimage .
```

### Kaniko (Rootless)

```yaml
build-kaniko:
  image:
    name: gcr.io/kaniko-project/executor:v1.21.0-debug
    entrypoint: [""]
  script:
    - /kaniko/executor
        --context "${CI_PROJECT_DIR}"
        --dockerfile "${CI_PROJECT_DIR}/Dockerfile"
        --destination "${CI_REGISTRY_IMAGE}:latest"
```

---

## Environment and Deployment

### `environment`

Marks jobs that deploy to environments.

```yaml
deploy-staging:
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging
    auto_stop_in: 1 day
    action: start  # start, prepare, stop
  script: deploy staging

stop-staging:
  environment:
    name: staging
    action: stop
  when: manual
  script: stop staging
```

**Kubernetes integration:**
```yaml
deploy-k8s:
  environment:
    name: production
    url: https://example.com
    kubernetes:
      namespace: production
  script: kubectl apply -f deployment.yaml
```

**Dynamic environments:**
```yaml
review:
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
    auto_stop_in: 1 week
  script: deploy review
  rules:
    - if: $CI_MERGE_REQUEST_ID
```

---

## Advanced Features

### `extends`

Inherits configuration from other jobs.

```yaml
.deploy-template:
  image: alpine:3.19
  before_script:
    - apk add --no-cache curl
  retry:
    max: 2

deploy-staging:
  extends: .deploy-template
  script: deploy staging

deploy-production:
  extends: .deploy-template
  script: deploy production
```

**Multiple inheritance:**
```yaml
.base:
  image: alpine:3.19

.retry:
  retry: 2

deploy:
  extends:
    - .base
    - .retry
  script: deploy
```

### `trigger`

Triggers downstream pipelines.

```yaml
# Trigger another project
trigger-downstream:
  trigger:
    project: group/downstream-project
    branch: main
    strategy: depend  # Wait for downstream pipeline

# Trigger child pipeline
trigger-child:
  trigger:
    include: child-pipeline.yml
    strategy: depend

# Trigger with variables
trigger-deploy:
  trigger:
    project: group/deploy-project
  variables:
    VERSION: $CI_COMMIT_SHORT_SHA
    ENVIRONMENT: production
```

### `coverage`

Extracts code coverage percentage from job output.

```yaml
test:
  script: npm test
  coverage: '/Coverage: \d+\.\d+%/'
```

### `release`

Creates GitLab releases.

```yaml
release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - echo "Creating release"
  release:
    tag_name: $CI_COMMIT_TAG
    name: 'Release $CI_COMMIT_TAG'
    description: 'Release notes for $CI_COMMIT_TAG'
```

### `secrets`

Retrieves secrets from external sources.

```yaml
deploy:
  secrets:
    DATABASE_PASSWORD:
      vault: production/db/password@secret
      file: false
```

### `inherit`

Controls inheritance of global defaults.

```yaml
job:
  inherit:
    default: false  # Don't inherit default settings
    variables: [VAR1, VAR2]  # Only inherit specific variables
```

---

## Predefined CI/CD Variables

Common GitLab CI/CD variables:

### Pipeline Variables
- `$CI_PIPELINE_ID` - Pipeline ID
- `$CI_PIPELINE_IID` - Pipeline IID (internal ID)
- `$CI_PIPELINE_SOURCE` - Pipeline source (push, merge_request_event, etc.)
- `$CI_PIPELINE_URL` - Pipeline URL

### Commit Variables
- `$CI_COMMIT_SHA` - Full commit SHA
- `$CI_COMMIT_SHORT_SHA` - Short commit SHA (8 chars)
- `$CI_COMMIT_BRANCH` - Branch name
- `$CI_COMMIT_TAG` - Tag name (if pipeline for tag)
- `$CI_COMMIT_REF_NAME` - Branch or tag name
- `$CI_COMMIT_REF_SLUG` - Slugified branch/tag name
- `$CI_COMMIT_MESSAGE` - Commit message
- `$CI_COMMIT_AUTHOR` - Commit author

### Job Variables
- `$CI_JOB_ID` - Job ID
- `$CI_JOB_NAME` - Job name
- `$CI_JOB_STAGE` - Job stage
- `$CI_JOB_URL` - Job URL
- `$CI_JOB_TOKEN` - Job token for API access
- `$CI_NODE_INDEX` - Job index in parallel jobs (1-based)
- `$CI_NODE_TOTAL` - Total number of parallel jobs

### Project Variables
- `$CI_PROJECT_ID` - Project ID
- `$CI_PROJECT_NAME` - Project name
- `$CI_PROJECT_PATH` - Project path (group/project)
- `$CI_PROJECT_DIR` - Working directory
- `$CI_PROJECT_URL` - Project URL

### Registry Variables
- `$CI_REGISTRY` - GitLab Container Registry URL
- `$CI_REGISTRY_IMAGE` - Full image path
- `$CI_REGISTRY_USER` - Registry username
- `$CI_REGISTRY_PASSWORD` - Registry password

### Merge Request Variables
- `$CI_MERGE_REQUEST_ID` - MR ID
- `$CI_MERGE_REQUEST_IID` - MR IID
- `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` - Source branch
- `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` - Target branch

---

## YAML Anchors and Aliases

YAML anchors for reusing configuration within a file.

```yaml
# Define anchor
.retry-config: &retry-config
  retry:
    max: 2
    when:
      - runner_system_failure

# Use anchor
job1:
  <<: *retry-config
  script: command1

job2:
  <<: *retry-config
  script: command2
```

**Merge multiple anchors:**
```yaml
.cache: &cache
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

.image: &image
  image: node:20-alpine

build:
  <<: [*cache, *image]
  script: npm run build
```

---

## Complete Example

```yaml
# Global configuration
stages:
  - build
  - test
  - security
  - deploy

variables:
  NODE_VERSION: "20"
  DOCKER_DRIVER: overlay2

default:
  image: node:${NODE_VERSION}-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  tags:
    - docker
  interruptible: true

# Hidden template
.deploy-template:
  before_script:
    - echo "Deploying to ${ENVIRONMENT}"
  retry:
    max: 2
    when:
      - runner_system_failure
  resource_group: ${ENVIRONMENT}

# Build job
build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

# Test jobs
test-unit:
  stage: test
  needs: []
  script:
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test-lint:
  stage: test
  needs: []
  script:
    - npm ci
    - npm run lint
  allow_failure: true

# Security scanning
include:
  - template: Security/SAST.gitlab-ci.yml

# Deployment jobs
deploy-staging:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: staging
  needs: [build, test-unit]
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - ./deploy.sh staging
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy-production:
  extends: .deploy-template
  stage: deploy
  variables:
    ENVIRONMENT: production
  needs: [build, test-unit]
  environment:
    name: production
    url: https://example.com
  script:
    - ./deploy.sh production
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
  when: manual
```

---

## Additional Resources

- Official GitLab CI/CD YAML reference: https://docs.gitlab.com/ci/yaml/
- GitLab CI/CD examples: https://docs.gitlab.com/ci/examples/
- GitLab CI/CD templates: https://gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/ci/templates

---

**Use this reference when generating or troubleshooting GitLab CI/CD configurations.**

---

## Reference: Security Guidelines

# GitLab CI/CD Security Guidelines

Comprehensive security guidelines for creating secure GitLab CI/CD pipelines. Follow these practices to protect your code, credentials, and infrastructure.

## Table of Contents

1. [Secrets Management](#secrets-management)
2. [Image Security](#image-security)
3. [Script Security](#script-security)
4. [Artifact Security](#artifact-security)
5. [Network Security](#network-security)
6. [Access Control](#access-control)
7. [Supply Chain Security](#supply-chain-security)
8. [Compliance and Auditing](#compliance-and-auditing)

---

## Secrets Management

### 1. Never Hardcode Secrets

**❌ BAD:**
```yaml
deploy:
  script:
    - deploy --api-key sk_live_abc123xyz
    - mysql -u admin -ppassword123 -h db.example.com
```

**✅ GOOD:**
```yaml
deploy:
  script:
    - deploy --api-key $API_KEY
    - mysql -u $DB_USER -p$DB_PASSWORD -h $DB_HOST
```

### 2. Use Masked and Protected Variables

**Settings for sensitive variables:**
- ✅ **Masked** - Hides value in job logs
- ✅ **Protected** - Only available in protected branches/tags
- ✅ **Expanded** - Controls variable expansion

**Example configuration in GitLab UI:**
```
Settings → CI/CD → Variables
Key: API_KEY
Value: sk_live_abc123xyz
Flags: [x] Mask variable
       [x] Protect variable
       [ ] Expand variable reference (disable for JSON/special chars)
```

### 3. Scope Variables Appropriately

```yaml
# Environment-specific variables
deploy-staging:
  environment:
    name: staging
  variables:
    API_ENDPOINT: https://api-staging.example.com
  script:
    - deploy --endpoint $API_ENDPOINT

deploy-production:
  environment:
    name: production
  variables:
    API_ENDPOINT: https://api.example.com
  script:
    - deploy --endpoint $API_ENDPOINT
```

### 4. Use GitLab Secrets Management

```yaml
deploy:
  secrets:
    DATABASE_PASSWORD:
      vault: production/db/password@secret
      token: $VAULT_TOKEN
  script:
    - deploy --db-password $DATABASE_PASSWORD
```

### 5. Rotate Secrets Regularly

- Set expiration for tokens and credentials
- Implement automated rotation where possible
- Remove unused credentials immediately
- Audit secret usage regularly

### 6. Avoid Secrets in Artifacts

```yaml
build:
  script:
    - make build
  artifacts:
    paths:
      - dist/
    exclude:
      - "**/*.env"
      - "**/*.pem"
      - "**/*.key"
      - "**/credentials.*"
      - "**/.env.*"
      - "**/config.production.*"
```

---

## Image Security

### 1. Pin Images to Specific Versions

**❌ BAD:**
```yaml
test:
  image: node:latest  # Unpredictable, security risk
```

**✅ GOOD:**
```yaml
test:
  image: node:20.11-alpine3.19  # Pinned version
```

**Best practice:**
- Use specific major.minor.patch versions
- Consider using SHA256 digests for maximum security
- Document why specific versions are chosen

### 2. Use Official and Trusted Images

```yaml
# ✅ GOOD: Official images
build:
  image: node:20-alpine  # Official Node.js image

test:
  image: postgres:15-alpine  # Official PostgreSQL image

# ⚠️ CAUTION: Third-party images (verify trust)
scan:
  image: aquasec/trivy:0.49.0  # Verify publisher reputation
```

### 3. Scan Images for Vulnerabilities

```yaml
stages:
  - build
  - scan

build-image:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .

scan-image:
  stage: scan
  image: aquasec/trivy:latest
  script:
    - trivy image --severity HIGH,CRITICAL --exit-code 1 $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  needs: [build-image]
  allow_failure: false  # Fail pipeline on vulnerabilities
```

### 4. Use Minimal Base Images

```dockerfile
# ✅ GOOD: Alpine-based images (smaller attack surface)
FROM node:20-alpine

# ⚠️ LARGER: Full images have more packages
FROM node:20-bookworm
```

### 5. Don't Run Containers as Root

```dockerfile
# Dockerfile best practice
FROM node:20-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Change ownership
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

CMD ["node", "server.js"]
```

---

## Script Security

### 1. Avoid Dangerous Script Patterns

**❌ DANGEROUS PATTERNS:**

```yaml
# Piping to bash
install:
  script:
    - curl https://install.sh | bash  # ❌ Dangerous

# Using eval
deploy:
  script:
    - eval "$COMMAND"  # ❌ Code injection risk

# Overly permissive permissions
setup:
  script:
    - chmod 777 /app  # ❌ Security risk
```

**✅ SECURE PATTERNS:**

```yaml
# Download and verify before execution
install:
  script:
    - curl -o install.sh https://install.sh
    - sha256sum -c install.sh.sha256  # Verify integrity
    - bash install.sh

# Avoid eval, use explicit commands
deploy:
  script:
    - ./deploy.sh $ENVIRONMENT

# Minimal permissions
setup:
  script:
    - chmod 755 /app
    - chmod 600 /app/config.yml
```

### 2. Validate and Sanitize Inputs

```yaml
deploy:
  script:
    - |
      # Validate branch name
      if [[ ! "$CI_COMMIT_BRANCH" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Invalid branch name"
        exit 1
      fi

      # Validate version format
      if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Invalid version format"
        exit 1
      fi

      ./deploy.sh "$CI_COMMIT_BRANCH" "$VERSION"
```

### 3. Use `set -e` for Error Handling

```yaml
deploy:
  script:
    - |
      set -e  # Exit on first error
      set -o pipefail  # Exit on pipe failures

      echo "Starting deployment"
      ./build.sh
      ./test.sh
      ./deploy.sh
```

### 4. Avoid Exposing Secrets in Logs

```yaml
# ❌ BAD: Secret might appear in logs
deploy:
  script:
    - echo "Deploying with token $API_TOKEN"

# ✅ GOOD: Don't echo secrets
deploy:
  script:
    - echo "Starting deployment"
    - deploy --token $API_TOKEN  # Token won't appear if masked

# ✅ GOOD: Use GitLab's masking
deploy:
  before_script:
    - echo "::add-mask::$API_TOKEN"  # Mask custom secrets
  script:
    - deploy --token $API_TOKEN
```

### 5. Disable Debug Mode in Production

```yaml
# ❌ BAD: Debug mode exposes information
deploy-production:
  variables:
    CI_DEBUG_TRACE: "true"  # ❌ Don't use in production
  script:
    - deploy production

# ✅ GOOD: Only debug in non-production
test:
  variables:
    CI_DEBUG_TRACE: "true"  # ✅ OK for testing
  script:
    - npm test
```

---

## Artifact Security

### 1. Use Specific Artifact Paths

**❌ BAD:**
```yaml
build:
  artifacts:
    paths:
      - ./**  # Includes everything, might expose secrets
```

**✅ GOOD:**
```yaml
build:
  artifacts:
    paths:
      - dist/
      - build/
    exclude:
      - "**/*.env"
      - "**/*.pem"
      - "**/*.key"
      - "**/node_modules/"
```

### 2. Set Appropriate Expiration

```yaml
# Short-lived artifacts for builds
build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour  # ✅ Minimize exposure window

# Longer retention for releases
release:
  artifacts:
    paths:
      - release/
    expire_in: 1 month  # ✅ Appropriate for releases
```

### 3. Don't Include Sensitive Dependencies

```yaml
build:
  artifacts:
    paths:
      - dist/
    exclude:
      - node_modules/  # ✅ Don't include dependencies
      - vendor/  # ✅ Don't include vendor code
      - .git/  # ✅ Don't include git history
```

### 4. Use Access Controls for Artifacts

Configure in **Settings → CI/CD → General pipelines:**
- Limit artifact downloads to project members
- Require authentication for artifact access
- Set appropriate visibility levels

---

## Network Security

### 1. Use TLS/SSL for All Connections

```yaml
deploy:
  script:
    # ✅ HTTPS
    - curl -X POST https://api.example.com/deploy

    # ❌ HTTP (only for local development)
    # - curl -X POST http://api.example.com/deploy
```

### 2. Don't Disable SSL Verification

**❌ BAD:**
```yaml
test:
  script:
    - curl -k https://api.example.com  # ❌ Disables verification
    - git config --global http.sslVerify false  # ❌ Dangerous
```

**✅ GOOD:**
```yaml
test:
  script:
    - curl --cacert /etc/ssl/certs/ca-bundle.crt https://api.example.com
    - git config --global http.sslCAInfo /etc/ssl/certs/ca-bundle.crt
```

### 3. Use Private Registries for Internal Images

```yaml
variables:
  # ✅ Use private registry for internal images
  INTERNAL_REGISTRY: registry.internal.example.com

build:
  image: $INTERNAL_REGISTRY/build-tools:latest
  script:
    - make build
```

### 4. Restrict Outbound Connections

```yaml
# Configure runner to limit outbound connections
# Only allow specific domains/IPs in firewall rules

deploy:
  script:
    # Whitelist specific endpoints
    - curl https://api.allowed-service.com/deploy
```

---

## Access Control

### 1. Use Protected Branches

**Settings → Repository → Protected branches:**
- Protect `main` and `production` branches
- Require merge request approvals
- Restrict who can push
- Restrict who can merge

```yaml
deploy-production:
  script:
    - deploy production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"  # Only on protected branch
  when: manual
```

### 2. Use Protected Environments

**Settings → CI/CD → Environments:**
- Mark production environments as protected
- Define deployment approvals
- Restrict access to authorized users

```yaml
deploy-production:
  environment:
    name: production  # Protected environment
    url: https://example.com
  script:
    - deploy production
  when: manual  # Requires manual approval
```

### 3. Use Protected Tags for Releases

```yaml
release:
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/  # Only on version tags
  script:
    - make release
  when: manual
```

### 4. Limit Runner Access

**Settings → CI/CD → Runners:**
- Use specific runners for sensitive operations
- Tag runners appropriately
- Disable shared runners for security-sensitive projects

```yaml
deploy-production:
  tags:
    - production-runner  # Specific runner for production
    - secured
  script:
    - deploy production
```

### 5. Use Resource Groups

```yaml
deploy-production:
  resource_group: production  # ✅ Prevents concurrent deployments
  script:
    - deploy production

deploy-staging:
  resource_group: staging  # ✅ Independent resource group
  script:
    - deploy staging
```

---

## Supply Chain Security

### 1. Pin All Dependencies

```yaml
# ✅ GOOD: Lock file ensures reproducibility
build:
  script:
    - npm ci  # Uses package-lock.json
    # - npm install  # ❌ Don't use in CI
```

### 2. Verify Dependency Integrity

```yaml
build:
  script:
    - npm ci --audit  # Check for vulnerabilities
    - npm audit --audit-level=high  # Fail on high severity issues
```

### 3. Use Dependency Scanning

```yaml
include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

gemnasium-dependency_scanning:
  variables:
    DS_EXCLUDED_PATHS: "node_modules,vendor"
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
```

### 4. Scan for Secrets in Code

```yaml
include:
  - template: Security/Secret-Detection.gitlab-ci.yml

secret_detection:
  variables:
    SECRET_DETECTION_EXCLUDED_PATHS: "tests/"
```

### 5. Use SBOM (Software Bill of Materials)

```yaml
sbom-generation:
  image: anchore/syft:latest
  script:
    - syft packages dir:. -o cyclonedx-json > sbom.json
  artifacts:
    paths:
      - sbom.json
    expire_in: 1 year
```

---

## Compliance and Auditing

### 1. Enable Audit Logging

- Enable audit events in GitLab
- Monitor pipeline execution logs
- Track variable changes
- Review access patterns

### 2. Implement Compliance Pipelines

```yaml
include:
  - template: 'Workflows/MergeRequest-Pipelines.gitlab-ci.yml'
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

compliance-check:
  stage: .pre
  script:
    - echo "Running compliance checks"
    - ./scripts/compliance-audit.sh
  allow_failure: false
```

### 3. Implement Separation of Duties

```yaml
# Different teams/roles for different stages
deploy-staging:
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
  # Can be triggered by developers

deploy-production:
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+/
  when: manual  # Requires ops team approval
  environment:
    name: production
```

### 4. Maintain Audit Trails

```yaml
deploy:
  before_script:
    - echo "Deploy initiated by $GITLAB_USER_LOGIN at $(date)"
    - echo "Commit: $CI_COMMIT_SHORT_SHA"
    - echo "Branch: $CI_COMMIT_BRANCH"
  script:
    - deploy production
  after_script:
    - echo "Deploy completed at $(date)"
    - ./scripts/log-audit-event.sh
```

### 5. Regular Security Reviews

- Review CI/CD configurations quarterly
- Audit access controls monthly
- Scan for exposed secrets weekly
- Update dependencies regularly
- Review runner security monthly

---

## Security Checklist

When creating or reviewing GitLab CI/CD pipelines, ensure:

### Secrets & Credentials
- [ ] No hardcoded secrets in `.gitlab-ci.yml`
- [ ] Sensitive variables are masked
- [ ] Production variables are protected
- [ ] Secrets are scoped to appropriate environments
- [ ] Regular secret rotation schedule exists

### Images & Containers
- [ ] All images pinned to specific versions
- [ ] Images from trusted sources only
- [ ] Container vulnerability scanning enabled
- [ ] Containers run as non-root users
- [ ] Minimal base images used where possible

### Scripts & Commands
- [ ] No `curl | bash` patterns
- [ ] No use of `eval` with external input
- [ ] Input validation implemented
- [ ] Proper error handling (`set -e`)
- [ ] No secrets echoed to logs

### Artifacts & Cache
- [ ] Specific artifact paths (not `./**`)
- [ ] Sensitive files excluded from artifacts
- [ ] Appropriate expiration times set
- [ ] No credentials in cached files

### Network & Communication
- [ ] HTTPS/TLS used for all external calls
- [ ] SSL verification enabled
- [ ] Private registries for internal images
- [ ] Outbound connections restricted

### Access Control
- [ ] Protected branches configured
- [ ] Protected environments for production
- [ ] Protected tags for releases
- [ ] Specific runners for sensitive operations
- [ ] Resource groups for deployments

### Supply Chain
- [ ] Dependencies pinned/locked
- [ ] Dependency scanning enabled
- [ ] SAST scanning enabled
- [ ] Secret detection enabled
- [ ] Regular dependency updates scheduled

### Compliance
- [ ] Audit logging enabled
- [ ] Compliance pipelines implemented
- [ ] Separation of duties enforced
- [ ] Audit trails maintained
- [ ] Regular security reviews scheduled

---

## Security Incident Response

### If Secrets Are Exposed

1. **Immediate Actions:**
   - Rotate the compromised credentials immediately
   - Revoke exposed tokens/keys
   - Review access logs for unauthorized usage
   - Notify security team

2. **Investigation:**
   - Identify scope of exposure
   - Review pipeline logs
   - Check for unauthorized access
   - Document timeline

3. **Remediation:**
   - Remove secrets from code/logs
   - Update `.gitlab-ci.yml` with proper secret management
   - Implement additional controls
   - Update security documentation

4. **Prevention:**
   - Enable secret scanning
   - Implement pre-commit hooks
   - Conduct security training
   - Review secret management practices

---

## Additional Resources

- GitLab Security Best Practices: https://docs.gitlab.com/ee/security/
- OWASP CI/CD Security: https://owasp.org/www-project-ci-cd-security/
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- NIST Supply Chain Security: https://www.nist.gov/itl/executive-order-improving-nations-cybersecurity/software-security-supply-chains

---

**Always prioritize security in your GitLab CI/CD pipelines. When in doubt, choose the more secure option.**
