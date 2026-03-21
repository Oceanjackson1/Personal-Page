---
title: "Jenkinsfile Validator"
description: "Validate, lint, audit, or check Jenkinsfiles and shared libraries."
category: "devops"
source: "community"
author: "Community"
tags: ["jenkinsfile", "validator"]
date: 2026-03-20
---

# Jenkinsfile Validator Skill

Use this skill to validate Jenkins pipelines and shared libraries with local scripts first, then optionally enrich findings with plugin documentation.

## Trigger Phrases

Use this skill when requests look like:
- "Validate this Jenkinsfile"
- "Check this pipeline for security issues"
- "Lint my Declarative/Scripted pipeline"
- "Why is this Jenkins pipeline failing syntax checks?"
- "Validate vars/*.groovy or src/**/*.groovy shared library files"

## Scope

This skill validates:
- Declarative pipelines (`pipeline { ... }`)
- Scripted pipelines (`node { ... }` and Groovy-style pipelines)
- Shared library files (`vars/*.groovy`, `src/**/*.groovy`)
- Hardcoded credential patterns
- Pipeline best practices and maintainability signals

## Prerequisites

Run commands from repository root unless noted.

### Required tools
- `bash`
- `grep`
- `sed`
- `awk`
- `head`
- `wc`
- `find` (needed for shared-library directory scans)

### Recommended tools
- `jq` (optional; improves JSON-heavy troubleshooting workflows)

### Script prerequisites
- Scripts live in `devops-skills-plugin/skills/jenkinsfile-validator/scripts/`
- Main orchestrator can run child scripts even if `+x` is missing (it uses `bash` fallback)
- If you want direct execution (`./script.sh`), make scripts executable:

```bash
chmod +x devops-skills-plugin/skills/jenkinsfile-validator/scripts/*.sh
```

### Preflight check (recommended)

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"

command -v bash grep sed awk head wc find >/dev/null && echo "required tools: ok" || echo "required tools: missing"
command -v jq >/dev/null && echo "jq: installed (optional)" || echo "jq: missing (optional)"

[ -d "$SKILL_DIR/scripts" ] && echo "scripts dir: ok" || echo "scripts dir: missing"
[ -f "$SKILL_DIR/scripts/validate_jenkinsfile.sh" ] && echo "main validator: ok" || echo "main validator: missing"
```

## Quick Start (Normalized Paths)

Use a single base path variable to avoid path ambiguity.

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
TARGET_JENKINSFILE="Jenkinsfile"

# Full validation (recommended)
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" "$TARGET_JENKINSFILE"
```

### Common options

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
TARGET_JENKINSFILE="Jenkinsfile"

bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --syntax-only "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --security-only "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --best-practices "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --no-security "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --no-best-practices "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --strict "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --assume-declarative "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" --assume-scripted "$TARGET_JENKINSFILE"
```

### Shared library validation

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"

bash "$SKILL_DIR/scripts/validate_shared_library.sh" vars/myStep.groovy
bash "$SKILL_DIR/scripts/validate_shared_library.sh" vars/
bash "$SKILL_DIR/scripts/validate_shared_library.sh" src/
bash "$SKILL_DIR/scripts/validate_shared_library.sh" /path/to/shared-library
```

### Regression and local CI checks

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
bash "$SKILL_DIR/tests/run_local_ci.sh"
```

`run_local_ci.sh` is the supported local/CI entrypoint for regression coverage. It runs:
- `bash -n` syntax checks for all `scripts/*.sh` and `tests/*.sh` files
- `tests/test_validate_jenkinsfile.sh` regression scenarios

## Deterministic Validation Flow

### 1) Detect pipeline type
- `pipeline {` => Declarative validator
- `node (...)` or `node {` => Scripted validator
- Unknown => fails closed by default (`ERROR [TypeDetection]`)
- Override intentionally ambiguous files with `--assume-declarative` or `--assume-scripted`

### 2) Run syntax validation
- Declarative: `validate_declarative.sh`
- Scripted: `validate_scripted.sh`

### 3) Run security scan
- `common_validation.sh check_credentials`

### 4) Run best practices check
- `best_practices.sh`

### 5) Aggregate and return final status
- Unified summary with pass/fail per phase and final exit code

### 6) Run regression suite after script changes
- `bash tests/run_local_ci.sh`
- Intended for both local pre-commit checks and CI job wiring

## Individual Script Commands (Advanced)

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
TARGET_JENKINSFILE="Jenkinsfile"

# Type detection
bash "$SKILL_DIR/scripts/common_validation.sh" detect_type "$TARGET_JENKINSFILE"

# Syntax-only by type
bash "$SKILL_DIR/scripts/validate_declarative.sh" "$TARGET_JENKINSFILE"
bash "$SKILL_DIR/scripts/validate_scripted.sh" "$TARGET_JENKINSFILE"

# Security-only
bash "$SKILL_DIR/scripts/common_validation.sh" check_credentials "$TARGET_JENKINSFILE"

# Best-practices-only
bash "$SKILL_DIR/scripts/best_practices.sh" "$TARGET_JENKINSFILE"
```

## Exit Code and Log Interpretation

### Main orchestrator: `validate_jenkinsfile.sh`
- `0`: Validation passed
- `1`: Validation failed (syntax/security errors, or warnings in `--strict` mode)
- `2`: Usage or environment error (bad args, missing file, missing required tools)

### Sub-scripts
- `validate_declarative.sh`: `0` pass (errors=0), `1` usage/file/validation failure
- `validate_scripted.sh`: `0` pass (errors=0), `1` usage/file/validation failure
- `common_validation.sh check_credentials`: `0` no credential errors, `1` credential issues found
- `validate_shared_library.sh`: `0` pass, `1` validation errors found, `2` invalid input target
- `best_practices.sh`: `1` only for usage/file errors; content findings are reported in logs and score output

### Log severity patterns
- `ERROR [Line N]: ...` => must fix
- `WARNING [Line N]: ...` => should review
- `INFO [Line N]: ...` => optional improvement
- Summary banners (`VALIDATION PASSED/FAILED`) determine final interpretation quickly

### Practical interpretation rules
- For CI gating, rely on main orchestrator exit code.
- Use `--strict` when warnings should fail pipelines.
- When `best_practices.sh` is run standalone, read report sections (`CRITICAL ISSUES`, `IMPROVEMENTS RECOMMENDED`, score); do not rely only on exit code.

## Fallback Behavior

### Missing optional tools
- If `jq` is missing, continue validation; treat as non-blocking.

### Non-executable child scripts
- Main orchestrator warns and falls back to `bash <script>` execution.

### Missing child scripts
- Main orchestrator reports runner error and returns failure for that phase.

### Unknown plugin steps
Use this order:
1. Check local reference: `devops-skills-plugin/skills/jenkinsfile-validator/references/common_plugins.md`
2. Context7 lookup:
   - `mcp__context7__resolve-library-id` with query like `jenkinsci <plugin-name>-plugin`
   - `mcp__context7__query-docs` for usage and parameters
3. Web fallback: [plugins.jenkins.io](https://plugins.jenkins.io/) and official Jenkins docs

### Offline/air-gapped mode
- Run all local validators.
- If plugin docs cannot be fetched, report: "Plugin docs lookup skipped due to environment constraints; local validation only."

## Plugin Documentation Lookup Workflow

When plugin-specific validation is requested:
1. Identify unknown steps from Jenkinsfile or validator logs.
2. Check `references/common_plugins.md` first.
3. If missing, use Context7 (`resolve-library-id` then `query-docs`).
4. If still missing, use web search against official plugin index/docs.
5. Return required parameters, optional parameters, version-sensitive notes, and security guidance.

## References

Local references:
- `devops-skills-plugin/skills/jenkinsfile-validator/references/declarative_syntax.md`
- `devops-skills-plugin/skills/jenkinsfile-validator/references/scripted_syntax.md`
- `devops-skills-plugin/skills/jenkinsfile-validator/references/best_practices.md`
- `devops-skills-plugin/skills/jenkinsfile-validator/references/common_plugins.md`

External references:
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Development Tools](https://www.jenkins.io/doc/book/pipeline/development/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Jenkins Plugins](https://plugins.jenkins.io/)

## Reporting Template

Use this structure in validation responses:

```text
Validation Target: <path>
Pipeline Type: <Declarative|Scripted|Shared Library|Unknown>

Findings:
- ERROR [Line X]: <issue>
- WARNING [Line Y]: <issue>
- INFO [Line Z]: <suggestion>

Phase Results:
- Syntax: <PASSED|FAILED|SKIPPED>
- Security: <PASSED|FAILED|SKIPPED>
- Best Practices: <PASSED|REVIEW NEEDED|SKIPPED>

Exit Code: <0|1|2>
Next Actions:
1. <highest-priority fix>
2. <second fix>
```

## Example Flows

### Example 1: Full Jenkinsfile validation

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
bash "$SKILL_DIR/scripts/validate_jenkinsfile.sh" Jenkinsfile
```

Expected behavior:
- Runs syntax + security + best practices
- Prints per-phase results and unified summary
- Returns `0/1/2` per orchestrator rules

### Example 2: Shared library directory validation

```bash
SKILL_DIR="devops-skills-plugin/skills/jenkinsfile-validator"
bash "$SKILL_DIR/scripts/validate_shared_library.sh" examples/shared-library
```

Expected behavior:
- Validates both `vars/` and `src/` files
- Aggregates issues with line references
- Returns `1` when errors are present

### Example 3: Unknown plugin step follow-up

Input step:
```groovy
nexusArtifactUploader artifacts: [[...]], nexusUrl: 'https://nexus.example.com'
```

Flow:
1. Validate locally first.
2. If step behavior is unclear, resolve docs via Context7.
3. If unavailable, use plugin site docs.
4. Report usage guidance and security-safe parameter patterns.

## Done Criteria

The skill usage is complete when all are true:
- Commands use normalized paths (`$SKILL_DIR/scripts/...`) with no cwd ambiguity.
- Prerequisites and optional dependencies are explicit.
- Exit-code semantics and log-severity interpretation are documented.
- Fallback behavior is defined for missing tools/docs and constrained environments.
- At least one runnable example exists for full validation and shared-library validation.
- Reporting format is deterministic and actionable.

---

## Reference: Best_Practices

# Jenkins Pipeline Best Practices

Comprehensive guide based on official Jenkins documentation and community best practices.

## Performance Best Practices

### 1. Combine Shell Commands

**Bad:**
```groovy
sh 'echo "Starting build"'
sh 'mkdir build'
sh 'cd build'
sh 'cmake ..'
sh 'make'
sh 'echo "Build complete"'
```

**Good:**
```groovy
sh '''
    echo "Starting build"
    mkdir build
    cd build
    cmake ..
    make
    echo "Build complete"
'''
```

**Why:** Each `sh` step has start-up and tear-down overhead. Combining commands reduces this overhead and improves performance.

### 2. Use Agent-Based Operations

**Bad (runs on controller):**
```groovy
@NonCPS
def parseJson(String jsonString) {
    def jsonSlurper = new groovy.json.JsonSlurper()
    return jsonSlurper.parseText(jsonString)
}

def data = readFile('data.json')
def parsed = parseJson(data)
```

**Good (runs on agent):**
```groovy
def result = sh(script: 'jq ".field" data.json', returnStdout: true).trim()
```

**Why:** Controller resources are shared across all builds. Heavy operations should run on agents to prevent controller bottlenecks.

### 3. Minimize Data Transfer to Controller

**Bad:**
```groovy
def logFile = readFile('huge-log.txt')  // Loads entire file into controller memory
def lines = logFile.split('\n')
```

**Good:**
```groovy
def errorCount = sh(script: 'grep ERROR huge-log.txt | wc -l', returnStdout: true).trim()
```

**Why:** Reduces memory usage on controller and network transfer time.

## Security Best Practices

### 1. Never Hardcode Credentials

**Bad:**
```groovy
sh 'docker login -u admin -p password123'
sh 'curl -H "Authorization: Bearer abc123xyz" https://api.example.com'
```

**Good:**
```groovy
withCredentials([usernamePassword(
    credentialsId: 'docker-hub',
    usernameVariable: 'DOCKER_USER',
    passwordVariable: 'DOCKER_PASS'
)]) {
    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
}

withCredentials([string(credentialsId: 'api-token', variable: 'API_TOKEN')]) {
    sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com'
}
```

**Why:** Credentials stored in Jenkins Credentials Manager are encrypted and access-controlled.

### 2. Use Credentials Binding

**Good:**
```groovy
environment {
    AWS_CREDENTIALS = credentials('aws-credentials-id')
    // Creates AWS_CREDENTIALS_USR and AWS_CREDENTIALS_PSW
}
```

### 3. Validate User Input

**Bad:**
```groovy
parameters {
    string(name: 'BRANCH', defaultValue: '', description: 'Branch to build')
}

sh "git checkout ${params.BRANCH}"  // Injection risk!
```

**Good:**
```groovy
parameters {
    choice(name: 'BRANCH', choices: ['main', 'develop', 'release'], description: 'Branch to build')
}

// Or validate input
def branch = params.BRANCH
if (!branch.matches(/^[a-zA-Z0-9_\-\/]+$/)) {
    error "Invalid branch name: ${branch}"
}
```

## Reliability Best Practices

### 1. Use Timeouts

**Good:**
```groovy
// Declarative
options {
    timeout(time: 1, unit: 'HOURS')
}

// Scripted
timeout(time: 30, unit: 'MINUTES') {
    node {
        // steps
    }
}
```

**Why:** Prevents builds from hanging indefinitely and consuming resources.

### 2. Implement Error Handling

**Declarative:**
```groovy
post {
    always {
        cleanWs()
    }
    success {
        slackSend color: 'good', message: "Build succeeded"
    }
    failure {
        mail to: 'team@example.com',
             subject: "Build Failed: ${currentBuild.fullDisplayName}",
             body: "Check ${env.BUILD_URL}"
    }
}
```

**Scripted:**
```groovy
node {
    try {
        stage('Build') {
            sh 'make build'
        }
        stage('Test') {
            sh 'make test'
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        mail to: 'team@example.com',
             subject: "Build Failed",
             body: "Error: ${e.message}"
        throw e
    } finally {
        cleanWs()
    }
}
```

### 3. Use Proper Workspace Cleanup

**Good:**
```groovy
post {
    always {
        cleanWs()
    }
}

// Or for specific cleanup
post {
    cleanup {
        deleteDir()
    }
}
```

**Why:** Ensures consistent build environment and prevents disk space issues.

### 4. Implement Retries for Flaky Operations

**Good:**
```groovy
retry(3) {
    sh 'curl -f https://flaky-api.example.com/data'
}

// Or with exponential backoff
script {
    def attempts = 0
    retry(3) {
        attempts++
        if (attempts > 1) {
            sleep time: attempts * 10, unit: 'SECONDS'
        }
        sh 'flaky-command'
    }
}
```

## Maintainability Best Practices

### 1. Use Shared Libraries

**Bad:** Copy-pasting common code across Jenkinsfiles

**Good:**
```groovy
@Library('my-shared-library@master') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildMavenProject()  // From shared library
            }
        }
        stage('Deploy') {
            steps {
                deployToKubernetes(env: 'production')  // From shared library
            }
        }
    }
}
```

### 2. Use Descriptive Stage Names

**Bad:**
```groovy
stage('Step 1') { }
stage('Step 2') { }
```

**Good:**
```groovy
stage('Build Application') { }
stage('Run Unit Tests') { }
stage('Build Docker Image') { }
stage('Deploy to Staging') { }
```

### 3. Add Comments for Complex Logic

**Good:**
```groovy
script {
    // Calculate next version based on git tags
    def lastTag = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
    def (major, minor, patch) = lastTag.tokenize('.')

    // Increment patch version for feature branches
    if (env.BRANCH_NAME.startsWith('feature/')) {
        patch = patch.toInteger() + 1
    }

    def nextVersion = "${major}.${minor}.${patch}"
    echo "Next version: ${nextVersion}"
}
```

### 4. Break Long Pipelines into Stages

**Good:**
```groovy
pipeline {
    stages {
        stage('Preparation') {
            stages {
                stage('Checkout') { }
                stage('Setup Environment') { }
            }
        }
        stage('Build') {
            stages {
                stage('Compile') { }
                stage('Package') { }
            }
        }
        stage('Quality Checks') {
            parallel {
                stage('Unit Tests') { }
                stage('Integration Tests') { }
                stage('Code Analysis') { }
            }
        }
    }
}
```

## Optimization Best Practices

### 1. Use Parallel Execution

**Good:**
```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'mvn verify'
            }
        }
        stage('E2E Tests') {
            steps {
                sh 'npm run e2e'
            }
        }
    }
}
```

### 2. Use failFast with Parallel

**Good:**
```groovy
stage('Deploy') {
    failFast true
    parallel {
        stage('Region 1') { }
        stage('Region 2') { }
        stage('Region 3') { }
    }
}
```

**Why:** Stops remaining parallel tasks immediately if one fails, saving time and resources.

### 3. Use Stash/Unstash for Artifacts

**Good:**
```groovy
node('build-agent') {
    stage('Build') {
        sh 'mvn package'
        stash name: 'app-jar', includes: 'target/*.jar'
    }
}

node('test-agent') {
    stage('Test') {
        unstash 'app-jar'
        sh 'java -jar target/*.jar --test'
    }
}
```

### 4. Skip Default Checkout When Not Needed

**Good:**
```groovy
options {
    skipDefaultCheckout()  // Don't checkout automatically
}

stages {
    stage('Build') {
        steps {
            checkout scm  // Checkout only when needed
        }
    }
}
```

## Docker Best Practices

### 1. Use Docker Agents for Consistent Environment

**Good:**
```groovy
agent {
    docker {
        image 'maven:3.8.1-adoptopenjdk-11'
        args '-v $HOME/.m2:/root/.m2'
    }
}
```

### 2. Reuse Docker Images

**Bad:**
```groovy
sh 'docker run maven:3.8.1 mvn clean'
sh 'docker run maven:3.8.1 mvn compile'
sh 'docker run maven:3.8.1 mvn package'
```

**Good:**
```groovy
docker.image('maven:3.8.1').inside {
    sh 'mvn clean compile package'
}
```

### 3. Build Once, Deploy Many Times

**Good:**
```groovy
stage('Build') {
    steps {
        script {
            dockerImage = docker.build("myapp:${env.BUILD_NUMBER}")
        }
    }
}

stage('Test') {
    steps {
        script {
            dockerImage.inside {
                sh 'run-tests.sh'
            }
        }
    }
}

stage('Deploy to Staging') {
    steps {
        script {
            dockerImage.push('staging')
        }
    }
}

stage('Deploy to Production') {
    steps {
        script {
            dockerImage.push('production')
            dockerImage.push('latest')
        }
    }
}
```

## Kubernetes Best Practices

### 1. Use Resource Limits

**Good:**
```groovy
agent {
    kubernetes {
        yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8.1
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
'''
    }
}
```

### 2. Use Service Accounts

**Good:**
```groovy
agent {
    kubernetes {
        yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  containers:
  - name: kubectl
    image: bitnami/kubectl:latest
'''
    }
}
```

## Testing Best Practices

### 1. Always Publish Test Results

**Good:**
```groovy
post {
    always {
        junit '**/target/test-results/*.xml'
        publishHTML([
            reportDir: 'coverage',
            reportFiles: 'index.html',
            reportName: 'Coverage Report'
        ])
    }
}
```

### 2. Archive Artifacts

**Good:**
```groovy
post {
    success {
        archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
    }
}
```

### 3. Separate Build and Test Stages

**Good:**
```groovy
stages {
    stage('Build') {
        steps {
            sh 'mvn clean package -DskipTests'
        }
    }
    stage('Test') {
        steps {
            sh 'mvn test'
        }
        post {
            always {
                junit '**/target/test-results/*.xml'
            }
        }
    }
}
```

## Build Trigger Best Practices

### 1. Use Webhooks Instead of Polling

**Bad:**
```groovy
triggers {
    pollSCM('H/5 * * * *')  // Polls every 5 minutes
}
```

**Good:**
Configure webhooks in your repository to trigger builds on push/PR

**Why:** Webhooks are more efficient and provide faster feedback than polling.

### 2. Use Appropriate Cron Syntax

**Good:**
```groovy
triggers {
    cron('H 2 * * *')  // Daily at ~2 AM (H for hash-based distribution)
    cron('H H(0-7) * * *')  // Once between midnight and 7 AM
}
```

## Notification Best Practices

### 1. Send Notifications for Important Events

**Good:**
```groovy
post {
    failure {
        slackSend (
            color: 'danger',
            message: "Build FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        )
    }
    fixed {
        slackSend (
            color: 'good',
            message: "Build FIXED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

### 2. Include Relevant Information

**Good:**
```groovy
post {
    failure {
        mail to: 'team@example.com',
             subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
             body: """
Build: ${env.BUILD_URL}
Branch: ${env.BRANCH_NAME}
Commit: ${env.GIT_COMMIT}
Author: ${env.CHANGE_AUTHOR}

Please check the build logs for details.
"""
    }
}
```

## Multi-Branch Pipeline Best Practices

### 1. Use Branch-Specific Logic

**Good:**
```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        sh 'deploy-production.sh'
    }
}

stage('Deploy to Staging') {
    when {
        branch 'develop'
    }
    steps {
        sh 'deploy-staging.sh'
    }
}
```

### 2. Use Pull Request Triggers

**Good:**
```groovy
stage('PR Validation') {
    when {
        changeRequest()
    }
    steps {
        sh 'run-pr-checks.sh'
    }
}
```

## Credential Management Best Practices

### 1. Use Least Privilege

- Create separate credentials for different purposes
- Use read-only credentials where possible
- Rotate credentials regularly

### 2. Use Credential Domains

Organize credentials by domain (global, project-specific, etc.)

### 3. Mask Sensitive Output

**Good:**
```groovy
withCredentials([string(credentialsId: 'api-key', variable: 'API_KEY')]) {
    wrap([$class: 'MaskPasswordsBuildWrapper']) {
        sh 'echo "Using API key: $API_KEY"'  // Will be masked in logs
    }
}
```

## Pipeline Configuration Best Practices

### 1. Use Build Discarder

**Good:**
```groovy
options {
    buildDiscarder(logRotator(
        numToKeepStr: '10',           // Keep last 10 builds
        daysToKeepStr: '30',          // Keep builds from last 30 days
        artifactNumToKeepStr: '5',    // Keep artifacts from last 5 builds
        artifactDaysToKeepStr: '14'   // Keep artifacts from last 14 days
    ))
}
```

### 2. Disable Concurrent Builds When Needed

**Good:**
```groovy
options {
    disableConcurrentBuilds()
}
```

### 3. Use Timestamps

**Good:**
```groovy
options {
    timestamps()
}
```

## Summary Checklist

- [ ] Combine multiple shell commands into single steps
- [ ] Use agent-based operations, not controller-based
- [ ] Never hardcode credentials
- [ ] Implement timeouts for all builds
- [ ] Add proper error handling (try-catch, post blocks)
- [ ] Clean workspace after builds
- [ ] Use parallel execution for independent tasks
- [ ] Publish test results and artifacts
- [ ] Send notifications for important events
- [ ] Use webhooks instead of polling
- [ ] Implement retries for flaky operations
- [ ] Use descriptive stage names
- [ ] Add comments for complex logic
- [ ] Use shared libraries for common code
- [ ] Configure build discarder
- [ ] Use Docker for consistent build environment
- [ ] Set resource limits for Kubernetes pods
- [ ] Validate user input
- [ ] Use least-privilege credentials
- [ ] Separate build and test stages

## References

- [Official Jenkins Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [CloudBees Pipeline Best Practices](https://docs.cloudbees.com/docs/admin-resources/latest/pipeline-best-practices/)
- [Jenkins Performance Best Practices](https://www.jenkins.io/doc/book/scaling/best-practices/)

---

## Reference: Common_Plugins

# Common Jenkins Plugins Reference

Documentation for frequently used Jenkins plugins in pipelines.

## Table of Contents

1. [Git Plugin](#git-plugin)
2. [Docker Plugin](#docker-plugin)
3. [Kubernetes Plugin](#kubernetes-plugin)
4. [Credentials Plugin](#credentials-plugin)
5. [Pipeline Utility Steps](#pipeline-utility-steps)
6. [JUnit Plugin](#junit-plugin)
7. [HTML Publisher Plugin](#html-publisher-plugin)
8. [Slack Notification Plugin](#slack-notification-plugin)
9. [Email Extension Plugin](#email-extension-plugin)
10. [Build Timeout Plugin](#build-timeout-plugin)
11. [Timestamper Plugin](#timestamper-plugin)
12. [AnsiColor Plugin](#ansicolor-plugin)
13. [Workspace Cleanup Plugin](#workspace-cleanup-plugin)

---

## Git Plugin

Provides Git repository access for Jenkins jobs.

### Checkout SCM

**Declarative:**
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
    }
}
```

**Scripted:**
```groovy
node {
    checkout scm
}
```

### Explicit Git Checkout

```groovy
checkout([
    $class: 'GitSCM',
    branches: [[name: '*/main']],
    userRemoteConfigs: [[
        url: 'https://github.com/user/repo.git',
        credentialsId: 'github-credentials'
    ]]
])

// With multiple remotes
checkout([
    $class: 'GitSCM',
    branches: [[name: '*/develop']],
    userRemoteConfigs: [
        [url: 'https://github.com/user/repo.git', name: 'origin'],
        [url: 'https://github.com/upstream/repo.git', name: 'upstream']
    ]
])
```

### Git Operations

```groovy
// Get commit hash
def commit = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()

// Get short commit hash
def shortCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()

// Get current branch
def branch = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()

// Get commit author
def author = sh(script: 'git log -1 --pretty=%an', returnStdout: true).trim()

// Get commit message
def message = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()

// Tag commit
sh "git tag -a v${env.BUILD_NUMBER} -m 'Release ${env.BUILD_NUMBER}'"
sh 'git push origin --tags'
```

### Environment Variables

- `GIT_COMMIT` - Current commit hash
- `GIT_BRANCH` - Branch name
- `GIT_PREVIOUS_COMMIT` - Previous commit
- `GIT_PREVIOUS_SUCCESSFUL_COMMIT` - Last successful build commit
- `GIT_URL` - Repository URL
- `GIT_AUTHOR_NAME` - Commit author name
- `GIT_AUTHOR_EMAIL` - Commit author email

---

## Docker Plugin

Jenkins plugin for running builds in Docker containers.

### Docker Agent

**Declarative:**
```groovy
pipeline {
    agent {
        docker {
            image 'maven:3.8.1-adoptopenjdk-11'
            args '-v /tmp:/tmp'
            label 'docker-agent'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'mvn --version'
            }
        }
    }
}
```

### Docker in Scripted Pipeline

```groovy
node {
    // Run inside container
    docker.image('maven:3.8.1').inside {
        sh 'mvn clean package'
    }

    // With additional arguments
    docker.image('node:14').inside('-v /tmp:/tmp -e NODE_ENV=production') {
        sh 'npm install'
        sh 'npm test'
    }

    // Build Docker image
    def image = docker.build("myapp:${env.BUILD_NUMBER}")

    // Build with custom Dockerfile
    def image2 = docker.build("myapp:latest", "-f Dockerfile.prod .")

    // Push to registry
    docker.withRegistry('https://registry.example.com', 'registry-credentials') {
        image.push()
        image.push('latest')
    }

    // Run container
    def container = docker.image('nginx:latest').run('-p 8080:80')
    try {
        sh 'curl http://localhost:8080'
    } finally {
        container.stop()
    }
}
```

### Docker Compose

```groovy
sh 'docker-compose up -d'
try {
    sh 'run-integration-tests.sh'
} finally {
    sh 'docker-compose down'
}
```

---

## Kubernetes Plugin

Run Jenkins agents as Kubernetes pods.

### Pod Template

**Declarative:**
```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: agent
spec:
  containers:
  - name: maven
    image: maven:3.8.1-adoptopenjdk-11
    command:
    - cat
    tty: true
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package'
                }
            }
        }
        stage('Docker Build') {
            steps {
                container('docker') {
                    sh 'docker build -t myapp:latest .'
                }
            }
        }
    }
}
```

### Scripted with Pod Template

```groovy
podTemplate(
    label: 'my-pod',
    containers: [
        containerTemplate(name: 'maven', image: 'maven:3.8.1', ttyEnabled: true, command: 'cat'),
        containerTemplate(name: 'kubectl', image: 'bitnami/kubectl:latest', ttyEnabled: true, command: 'cat')
    ],
    volumes: [
        secretVolume(secretName: 'kubeconfig', mountPath: '/home/jenkins/.kube')
    ]
) {
    node('my-pod') {
        stage('Build') {
            container('maven') {
                sh 'mvn clean package'
            }
        }
        stage('Deploy') {
            container('kubectl') {
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
```

---

## Credentials Plugin

Securely store and use credentials in pipelines.

### Credential Types

#### Username and Password

```groovy
withCredentials([usernamePassword(
    credentialsId: 'my-credentials',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD'
)]) {
    sh 'echo "User: $USERNAME"'
    // Use $PASSWORD
}
```

#### Secret Text

```groovy
withCredentials([string(
    credentialsId: 'api-token',
    variable: 'API_TOKEN'
)]) {
    sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com'
}
```

#### SSH User Private Key

```groovy
withCredentials([sshUserPrivateKey(
    credentialsId: 'ssh-key',
    keyFileVariable: 'SSH_KEY',
    usernameVariable: 'SSH_USER'
)]) {
    sh 'ssh -i $SSH_KEY $SSH_USER@server.example.com "deploy.sh"'
}
```

#### File

```groovy
withCredentials([file(
    credentialsId: 'kubeconfig',
    variable: 'KUBECONFIG'
)]) {
    sh 'kubectl --kubeconfig=$KUBECONFIG get pods'
}
```

#### Certificate

```groovy
withCredentials([certificate(
    credentialsId: 'cert-id',
    keystoreVariable: 'KEYSTORE',
    passwordVariable: 'KEYSTORE_PASSWORD'
)]) {
    sh 'sign-app.sh $KEYSTORE $KEYSTORE_PASSWORD'
}
```

### Environment Credentials Binding

**Declarative:**
```groovy
environment {
    DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    // Creates DOCKER_CREDENTIALS_USR and DOCKER_CREDENTIALS_PSW

    API_KEY = credentials('api-key')  // Secret text
}
```

---

## Pipeline Utility Steps

Common utility steps for pipelines.

### Read and Write Files

```groovy
// Read file
def content = readFile(file: 'version.txt')

// Write file
writeFile(file: 'output.txt', text: 'Hello World')

// Read JSON
def json = readJSON(file: 'config.json')
// Or from text
def data = readJSON(text: '{"key": "value"}')

// Write JSON
writeJSON(file: 'output.json', json: [name: 'Jenkins', version: '2.0'])

// Read YAML
def yaml = readYAML(file: 'config.yaml')

// Write YAML
writeYAML(file: 'output.yaml', data: [name: 'Jenkins', version: '2.0'])

// Read CSV
def csv = readCSV(file: 'data.csv')

// Read properties
def props = readProperties(file: 'config.properties')
```

### File Operations

```groovy
// Check if file exists
if (fileExists('path/to/file')) {
    echo 'File exists'
}

// Find files
def files = findFiles(glob: '**/*.jar')
files.each { file ->
    echo "Found: ${file.path}"
}

// Touch file
touch(file: 'marker.txt')

// ZIP files
zip(zipFile: 'archive.zip', dir: 'target')

// Unzip
unzip(zipFile: 'archive.zip', dir: 'output')
```

---

## JUnit Plugin

Publish JUnit test results.

### Basic Usage

```groovy
post {
    always {
        junit '**/target/test-results/*.xml'
    }
}

// With options
junit(
    testResults: '**/target/surefire-reports/*.xml',
    allowEmptyResults: true,
    keepLongStdio: true,
    healthScaleFactor: 1.0
)
```

---

## HTML Publisher Plugin

Publish HTML reports.

```groovy
publishHTML([
    reportDir: 'coverage',
    reportFiles: 'index.html',
    reportName: 'Coverage Report',
    keepAll: true,
    alwaysLinkToLastBuild: true,
    allowMissing: false
])

// Multiple reports
publishHTML([
    reportDir: 'test-results',
    reportFiles: 'index.html',
    reportName: 'Test Results'
])
publishHTML([
    reportDir: 'coverage',
    reportFiles: 'index.html',
    reportName: 'Code Coverage'
])
```

---

## Slack Notification Plugin

Send notifications to Slack.

```groovy
// Simple notification
slackSend(
    color: 'good',
    message: 'Build succeeded!'
)

// With details
slackSend(
    color: currentBuild.result == 'SUCCESS' ? 'good' : 'danger',
    message: """
Build: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Status: ${currentBuild.result}
Duration: ${currentBuild.durationString}
URL: ${env.BUILD_URL}
""",
    channel: '#builds',
    teamDomain: 'myteam',
    tokenCredentialId: 'slack-token'
)

// Conditional notifications
post {
    success {
        slackSend color: 'good', message: "Build ${env.BUILD_NUMBER} succeeded"
    }
    failure {
        slackSend color: 'danger', message: "Build ${env.BUILD_NUMBER} failed"
    }
    fixed {
        slackSend color: 'good', message: "Build ${env.BUILD_NUMBER} fixed!"
    }
}
```

---

## Email Extension Plugin

Send detailed email notifications.

```groovy
emailext(
    subject: "Build ${currentBuild.result}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
    body: """
<h2>Build ${currentBuild.result}</h2>
<p><strong>Job:</strong> ${env.JOB_NAME}</p>
<p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
<p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
<p><strong>Duration:</strong> ${currentBuild.durationString}</p>
""",
    to: 'team@example.com',
    from: 'jenkins@example.com',
    replyTo: 'noreply@example.com',
    mimeType: 'text/html',
    attachLog: true,
    compressLog: true,
    attachmentsPattern: '**/target/*.jar'
)

// Conditional emails
post {
    failure {
        emailext(
            subject: "Build Failed: ${env.JOB_NAME}",
            body: "Check ${env.BUILD_URL}",
            to: 'team@example.com',
            recipientProviders: [
                developers(),  // Send to developers who made changes
                culprits(),    // Send to developers who broke the build
                requestor()    // Send to user who triggered the build
            ]
        )
    }
}
```

---

## Build Timeout Plugin

Set timeouts for builds.

**Declarative:**
```groovy
options {
    timeout(time: 1, unit: 'HOURS')
}
```

**Scripted:**
```groovy
timeout(time: 30, unit: 'MINUTES') {
    node {
        // steps
    }
}

// Activity timeout (no console output)
timeout(time: 10, unit: 'MINUTES', activity: true) {
    node {
        // steps
    }
}
```

---

## Timestamper Plugin

Add timestamps to console output.

**Declarative:**
```groovy
options {
    timestamps()
}
```

**Scripted:**
```groovy
timestamps {
    node {
        echo 'This will have timestamps'
    }
}
```

---

## AnsiColor Plugin

Add color to console output.

**Declarative:**
```groovy
options {
    ansiColor('xterm')
}
```

**Scripted:**
```groovy
ansiColor('xterm') {
    node {
        sh 'ls --color=always'
    }
}
```

---

## Workspace Cleanup Plugin

Clean workspace before/after builds.

```groovy
// Clean before build
cleanWs()

// Clean after build
post {
    always {
        cleanWs()
    }
}

// Clean with options
cleanWs(
    deleteDirs: true,
    disableDeferredWipeout: true,
    notFailBuild: true,
    patterns: [
        [pattern: 'target', type: 'INCLUDE'],
        [pattern: '*.log', type: 'INCLUDE']
    ]
)

// Delete directory
deleteDir()
```

---

## Additional Common Plugins

### Archive Artifacts

```groovy
archiveArtifacts(
    artifacts: '**/*.jar',
    allowEmptyArchive: false,
    fingerprint: true,
    onlyIfSuccessful: true
)
```

### Stash/Unstash

```groovy
// Stash files
stash(
    name: 'build-artifacts',
    includes: 'target/*.jar',
    excludes: 'target/*-sources.jar'
)

// Unstash files
unstash 'build-artifacts'
```

### Build Job

```groovy
// Trigger another job
build(
    job: 'downstream-job',
    parameters: [
        string(name: 'ENVIRONMENT', value: 'production'),
        booleanParam(name: 'RUN_TESTS', value: true)
    ],
    wait: true,
    propagate: true
)
```

### Input

```groovy
def userInput = input(
    message: 'Deploy to production?',
    ok: 'Deploy',
    parameters: [
        choice(name: 'ENVIRONMENT', choices: ['staging', 'production'], description: 'Target environment'),
        string(name: 'VERSION', defaultValue: '1.0', description: 'Version to deploy')
    ],
    submitter: 'admin,ops',
    submitterParameter: 'approver'
)

echo "Deploying ${userInput.VERSION} to ${userInput.ENVIRONMENT}"
echo "Approved by: ${userInput.approver}"
```

### Retry

```groovy
retry(3) {
    sh 'flaky-command'
}
```

### Sleep

```groovy
sleep(time: 30, unit: 'SECONDS')
```

### Wait Until

```groovy
waitUntil {
    def status = sh(script: 'check-status.sh', returnStatus: true)
    return status == 0
}
```

---

## Plugin Documentation Lookup

For unlisted plugins, use:

1. **Context7**: Search for `/jenkinsci/<plugin-name>-plugin`
2. **Web Search**: "Jenkins <plugin-name> plugin documentation"
3. **Official Plugins**: https://plugins.jenkins.io/

---

## References

- [Jenkins Plugins Index](https://plugins.jenkins.io/)
- [Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Plugins Development Guide](https://www.jenkins.io/doc/developer/plugin-development/)

---

## Reference: Declarative_Syntax

# Declarative Pipeline Syntax Reference

Complete reference for Jenkins Declarative Pipeline syntax based on official documentation.

## Basic Structure

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}
```

## Required Sections

### 1. pipeline
The outermost block that contains all pipeline code.

```groovy
pipeline {
    // All declarative pipeline code goes here
}
```

### 2. agent
Specifies where the pipeline or stage will execute. **Required** at top level or per stage.

```groovy
// Execute on any available agent
agent any

// Execute on agent with specific label
agent {
    label 'linux'
}

// Execute in Docker container
agent {
    docker {
        image 'maven:3.8.1-adoptopenjdk-11'
        args '-v /tmp:/tmp'
    }
}

// Execute in Kubernetes pod
agent {
    kubernetes {
        yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8.1-adoptopenjdk-11
'''
    }
}

// No agent (stages must define their own)
agent none
```

### 3. stages
Contains a sequence of one or more stage directives. **Required**.

```groovy
stages {
    stage('Build') {
        steps {
            // build steps
        }
    }
    stage('Test') {
        steps {
            // test steps
        }
    }
}
```

### 4. steps
Defines actions to execute within a stage. **Required** in each stage (unless stage has stages).

```groovy
steps {
    echo 'Hello World'
    sh 'make'
    bat 'build.bat'
    script {
        // Groovy script
        def myVar = 'value'
    }
}
```

## Optional Top-Level Directives

### environment
Defines environment variables available to all steps.

```groovy
environment {
    CC = 'clang'
    DISABLE_AUTH = 'true'
    DB_ENGINE = 'sqlite'

    // From credentials
    AWS_ACCESS_KEY_ID = credentials('aws-secret-key-id')

    // From credentials with username/password
    DOCKER_CREDS = credentials('docker-hub-credentials')
    // Creates: DOCKER_CREDS_USR and DOCKER_CREDS_PSW
}
```

### options
Configures pipeline-specific settings.

```groovy
options {
    // Keep only last 10 builds
    buildDiscarder(logRotator(numToKeepStr: '10'))

    // Disable concurrent builds
    disableConcurrentBuilds()

    // Prevent builds from running forever
    timeout(time: 1, unit: 'HOURS')

    // Add timestamps to console output
    timestamps()

    // Retry failed pipeline up to 3 times
    retry(3)

    // Skip default checkout
    skipDefaultCheckout()

    // Prepend all console output with time
    ansiColor('xterm')
}
```

### parameters
Defines build parameters users can provide.

```groovy
parameters {
    string(
        name: 'DEPLOY_ENV',
        defaultValue: 'staging',
        description: 'Environment to deploy to'
    )

    choice(
        name: 'VERSION',
        choices: ['1.0', '1.1', '2.0'],
        description: 'Version to deploy'
    )

    booleanParam(
        name: 'RUN_TESTS',
        defaultValue: true,
        description: 'Run tests before deploy'
    )

    text(
        name: 'RELEASE_NOTES',
        defaultValue: '',
        description: 'Release notes'
    )

    password(
        name: 'SECRET',
        defaultValue: '',
        description: 'Secret value'
    )
}

// Access in pipeline:
// ${params.DEPLOY_ENV}
```

### triggers
Defines automatic build triggers.

```groovy
triggers {
    // Poll SCM every 15 minutes
    pollSCM('H/15 * * * *')

    // Cron schedule
    cron('H 4 * * 1-5')  // Weekdays at 4 AM

    // Trigger from upstream job
    upstream(
        upstreamProjects: 'job1,job2',
        threshold: hudson.model.Result.SUCCESS
    )
}
```

### tools
Auto-installs and configures tools.

```groovy
tools {
    maven 'Maven 3.8.1'
    jdk 'JDK 11'
    gradle 'Gradle 7.0'
}
```

### libraries
Loads shared libraries.

```groovy
@Library('my-shared-library@master') _

// Or
libraries {
    lib('my-shared-library@master')
}
```

## Stage-Level Directives

### agent (stage-level)
Override agent for specific stage.

```groovy
stage('Build') {
    agent {
        docker 'maven:3.8.1-adoptopenjdk-11'
    }
    steps {
        sh 'mvn clean package'
    }
}
```

### environment (stage-level)
Stage-specific environment variables.

```groovy
stage('Deploy') {
    environment {
        DEPLOY_ENV = 'production'
    }
    steps {
        sh 'deploy.sh $DEPLOY_ENV'
    }
}
```

### when
Conditional execution of stage.

```groovy
stage('Deploy to Production') {
    when {
        branch 'main'
        environment name: 'DEPLOY_ENV', value: 'production'
        expression { return params.RUN_DEPLOY }
    }
    steps {
        echo 'Deploying...'
    }
}

// When conditions:
when {
    branch 'main'                              // Branch name
    branch pattern: "release-\\d+", comparator: "REGEXP"

    environment name: 'DEPLOY', value: 'true'  // Environment variable

    expression { return currentBuild.result == null }  // Groovy expression

    tag "release-*"                            // Git tag
    tag pattern: "release-\\d+", comparator: "REGEXP"

    not { branch 'main' }                      // Negation

    allOf {                                    // AND
        branch 'main'
        environment name: 'DEPLOY', value: 'true'
    }

    anyOf {                                    // OR
        branch 'main'
        branch 'develop'
    }

    triggeredBy 'UserIdCause'                  // Trigger type
    triggeredBy cause: 'UserIdCause', detail: 'admin'

    buildingTag()                              // Building a tag

    changelog '.*\\[DEPLOY\\].*'               // Changelog pattern

    changeset "**/*.js"                        // Changed files

    equals expected: 2, actual: currentBuild.number  // Comparison
}
```

### input
Pause for user input.

```groovy
stage('Deploy') {
    input {
        message "Deploy to production?"
        ok "Deploy"
        submitter "admin,ops"
        parameters {
            string(name: 'VERSION', description: 'Version to deploy')
        }
    }
    steps {
        echo "Deploying ${VERSION}"
    }
}
```

### options (stage-level)
Stage-specific options.

```groovy
stage('Test') {
    options {
        timeout(time: 30, unit: 'MINUTES')
        retry(2)
        timestamps()
    }
    steps {
        sh 'run-tests.sh'
    }
}
```

## post
Runs after pipeline/stage completion.

```groovy
post {
    always {
        // Always run, regardless of status
        echo 'Pipeline completed'
        cleanWs()
    }

    success {
        // Run only if successful
        slackSend color: 'good', message: 'Build succeeded!'
    }

    failure {
        // Run only if failed
        mail to: 'team@example.com',
             subject: "Build Failed: ${currentBuild.fullDisplayName}",
             body: "Something is wrong"
    }

    unstable {
        // Run if unstable (tests failed but build succeeded)
        echo 'Build is unstable'
    }

    changed {
        // Run if status changed from previous build
        echo 'Build status changed'
    }

    fixed {
        // Run if previous build failed but current succeeded
        echo 'Build is fixed'
    }

    regression {
        // Run if previous build succeeded but current failed
        echo 'Build regressed'
    }

    aborted {
        // Run if aborted
        echo 'Build was aborted'
    }

    cleanup {
        // Always run, after all other post conditions
        echo 'Cleaning up...'
        deleteDir()
    }
}
```

## Parallel Stages

Execute stages in parallel.

```groovy
stage('Parallel Tests') {
    parallel {
        stage('Test on Linux') {
            agent { label 'linux' }
            steps {
                sh 'make test'
            }
        }
        stage('Test on Windows') {
            agent { label 'windows' }
            steps {
                bat 'make test'
            }
        }
        stage('Test on Mac') {
            agent { label 'mac' }
            steps {
                sh 'make test'
            }
        }
    }
}

// With failFast
stage('Parallel Deploy') {
    failFast true  // Stop all parallel stages if one fails
    parallel {
        stage('Deploy to Region 1') {
            steps { sh 'deploy-region1.sh' }
        }
        stage('Deploy to Region 2') {
            steps { sh 'deploy-region2.sh' }
        }
    }
}
```

## Sequential Stages

Nested stages that run sequentially.

```groovy
stage('Build and Test') {
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh 'make test'
            }
        }
    }
}
```

## Matrix

Run stages across combinations of axes.

```groovy
stage('Test') {
    matrix {
        axes {
            axis {
                name 'PLATFORM'
                values 'linux', 'mac', 'windows'
            }
            axis {
                name 'BROWSER'
                values 'chrome', 'firefox', 'safari'
            }
        }

        excludes {
            exclude {
                axis {
                    name 'PLATFORM'
                    values 'linux'
                }
                axis {
                    name 'BROWSER'
                    values 'safari'
                }
            }
        }

        stages {
            stage('Test') {
                steps {
                    echo "Testing on ${PLATFORM} with ${BROWSER}"
                }
            }
        }
    }
}
```

## Common Steps

```groovy
steps {
    // Shell commands
    sh 'echo "Hello"'
    sh '''
        echo "Multi-line"
        echo "shell script"
    '''
    sh(script: 'ls -la', returnStdout: true)
    sh(script: 'exit 1', returnStatus: true)

    // Windows batch
    bat 'echo Hello'

    // PowerShell
    powershell 'Write-Host "Hello"'

    // Echo
    echo 'Message'

    // Error
    error 'Build failed'

    // Retry
    retry(3) {
        sh 'flaky-command'
    }

    // Timeout
    timeout(time: 5, unit: 'MINUTES') {
        sh 'long-running-command'
    }

    // Script (run Groovy code)
    script {
        def myVar = 'value'
        if (myVar == 'value') {
            echo 'Condition met'
        }
    }

    // Credentials
    withCredentials([string(credentialsId: 'my-secret', variable: 'SECRET')]) {
        sh 'echo $SECRET'
    }

    // Git checkout
    checkout scm
    checkout([
        $class: 'GitSCM',
        branches: [[name: '*/main']],
        userRemoteConfigs: [[url: 'https://github.com/user/repo.git']]
    ])

    // Archive artifacts
    archiveArtifacts artifacts: '**/*.jar', fingerprint: true

    // Publish test results
    junit '**/target/test-results/*.xml'

    // Stash/unstash
    stash name: 'build-artifacts', includes: 'target/*.jar'
    unstash 'build-artifacts'

    // Delete workspace
    deleteDir()

    // Clean workspace
    cleanWs()
}
```

## Built-in Variables

```groovy
// Build info
currentBuild.number          // Build number
currentBuild.result          // SUCCESS, FAILURE, UNSTABLE, ABORTED
currentBuild.currentResult   // Current result
currentBuild.displayName     // Display name
currentBuild.description     // Build description
currentBuild.duration        // Build duration in ms

// Environment variables
env.BUILD_ID
env.BUILD_NUMBER
env.BUILD_TAG
env.BUILD_URL
env.JOB_NAME
env.JOB_BASE_NAME
env.NODE_NAME
env.WORKSPACE
env.JENKINS_HOME
env.BRANCH_NAME              // For multibranch pipelines
env.CHANGE_ID                // For pull requests
env.GIT_COMMIT
env.GIT_BRANCH

// Parameters
params.PARAMETER_NAME

// SCM
scm.userRemoteConfigs
scm.branches
```

## Complete Example

```groovy
pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests')
    }

    environment {
        APP_NAME = 'my-app'
        VERSION = "${env.BUILD_NUMBER}"
        DOCKER_IMAGE = "${APP_NAME}:${VERSION}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            agent {
                docker {
                    image 'maven:3.8.1-adoptopenjdk-11'
                }
            }
            steps {
                sh 'mvn clean package'
                stash name: 'build-artifacts', includes: 'target/*.jar'
            }
        }

        stage('Test') {
            when {
                expression { return params.RUN_TESTS }
            }
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'mvn test'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'mvn verify'
                    }
                }
            }
            post {
                always {
                    junit '**/target/test-results/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                unstash 'build-artifacts'
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to ${params.ENVIRONMENT}?"
                ok "Deploy"
                submitter "ops,admin"
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        docker login -u $USER -p $PASS
                        docker push ${DOCKER_IMAGE}
                    '''
                }
                sh "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_IMAGE}"
            }
        }
    }

    post {
        success {
            slackSend color: 'good', message: "Build ${env.BUILD_NUMBER} succeeded"
        }
        failure {
            mail to: 'team@example.com',
                 subject: "Build ${env.BUILD_NUMBER} failed",
                 body: "Check ${env.BUILD_URL}"
        }
        cleanup {
            cleanWs()
        }
    }
}
```

## References

- [Official Pipeline Syntax Documentation](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Pipeline Development Tools](https://www.jenkins.io/doc/book/pipeline/development/)

---

## Reference: Scripted_Syntax

# Scripted Pipeline Syntax Reference

Complete reference for Jenkins Scripted Pipeline syntax using Groovy.

## Overview

Scripted Pipeline is written using Groovy, providing maximum flexibility and power. Unlike Declarative Pipeline, Scripted Pipeline uses imperative programming and has few structural restrictions.

## Basic Structure

```groovy
node {
    stage('Build') {
        echo 'Building...'
    }

    stage('Test') {
        echo 'Testing...'
    }

    stage('Deploy') {
        echo 'Deploying...'
    }
}
```

## node Block

The `node` block allocates an executor (agent) for the pipeline.

```groovy
// Run on any available agent
node {
    // steps here
}

// Run on specific labeled agent
node('linux') {
    // steps here
}

// Run on Docker agent
node('docker') {
    // steps here
}

// Run on specific node
node('master') {
    // steps here
}

// Run on agent matching expression
node('linux && java11') {
    // steps here
}
```

## stage Block

Stages organize pipeline into logical sections (mainly for visualization).

```groovy
node {
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        sh 'make build'
    }

    stage('Test') {
        sh 'make test'
    }
}
```

## Variables and Data Types

### Variable Declaration

```groovy
// Using def (recommended for local scope)
def myString = 'Hello'
def myNumber = 42
def myBoolean = true
def myList = [1, 2, 3]
def myMap = [key1: 'value1', key2: 'value2']

// Without def (global scope - use cautiously)
globalVar = 'accessible everywhere'

// Typed variables
String name = 'Jenkins'
Integer count = 10
Boolean flag = false
List<String> items = ['a', 'b', 'c']
Map<String, String> config = [env: 'prod', version: '1.0']
```

### String Interpolation

```groovy
def name = 'World'

// Double quotes for interpolation
def greeting = "Hello, ${name}!"

// Single quotes for literal strings
def literal = 'Hello, ${name}!'  // Won't interpolate

// Multi-line strings
def multiLine = """
    This is a
    multi-line string
    with ${name}
"""

// Multi-line without interpolation
def multiLineLiteral = '''
    This is a
    literal multi-line string
    with ${name}
'''
```

## Control Structures

### if-else

```groovy
node {
    def environment = 'production'

    if (environment == 'production') {
        echo 'Deploying to production'
    } else if (environment == 'staging') {
        echo 'Deploying to staging'
    } else {
        echo 'Deploying to development'
    }

    // Ternary operator
    def message = (environment == 'production') ? 'PROD' : 'NON-PROD'
}
```

### for Loops

```groovy
node {
    // Iterate over list
    def items = ['build', 'test', 'deploy']
    for (item in items) {
        echo "Step: ${item}"
    }

    // Iterate with index
    for (int i = 0; i < items.size(); i++) {
        echo "${i}: ${items[i]}"
    }

    // Range iteration
    for (i in 0..5) {
        echo "Number: ${i}"
    }

    // Each method
    items.each { item ->
        echo "Processing ${item}"
    }

    // Each with index
    items.eachWithIndex { item, index ->
        echo "${index}: ${item}"
    }
}
```

### while Loops

```groovy
node {
    def counter = 0
    while (counter < 5) {
        echo "Counter: ${counter}"
        counter++
    }
}
```

### switch Statement

```groovy
node {
    def environment = 'staging'

    switch(environment) {
        case 'development':
            echo 'Dev environment'
            break
        case 'staging':
            echo 'Staging environment'
            break
        case 'production':
            echo 'Production environment'
            break
        default:
            error 'Unknown environment'
    }
}
```

## Error Handling

### try-catch-finally

```groovy
node {
    try {
        sh 'make build'
        sh 'make test'
    } catch (Exception e) {
        echo "Build failed: ${e.message}"
        currentBuild.result = 'FAILURE'
        throw e  // Re-throw if needed
    } finally {
        echo 'Cleaning up...'
        sh 'make clean'
    }
}
```

### try-catch with Different Exception Types

```groovy
node {
    try {
        sh 'risky-command'
    } catch (hudson.AbortException e) {
        echo "Process was aborted: ${e.message}"
    } catch (Exception e) {
        echo "General error: ${e.message}"
        currentBuild.result = 'FAILURE'
    }
}
```

### Catching Specific Errors

```groovy
node {
    try {
        def result = sh(script: 'test-command', returnStatus: true)
        if (result != 0) {
            error "Command failed with exit code ${result}"
        }
    } catch (Exception e) {
        echo "Handling error: ${e}"
        // Continue or fail
    }
}
```

## Methods and Functions

### Defining Methods

```groovy
// Method definition
def buildApplication() {
    echo 'Building application...'
    sh 'mvn clean package'
}

// Method with parameters
def deploy(String environment, String version) {
    echo "Deploying version ${version} to ${environment}"
    sh "kubectl set image deployment/app app=${version}"
}

// Method with return value
def getVersion() {
    return sh(script: 'git describe --tags', returnStdout: true).trim()
}

// Usage
node {
    buildApplication()
    def version = getVersion()
    deploy('production', version)
}
```

### @NonCPS Methods

Methods that should not use Continuation Passing Style (for complex Groovy operations).

```groovy
@NonCPS
def parseJson(String json) {
    def jsonSlurper = new groovy.json.JsonSlurper()
    return jsonSlurper.parseText(json)
}

@NonCPS
def processData(data) {
    // Complex Groovy logic that doesn't involve pipeline steps
    return data.collect { it.toUpperCase() }
}

node {
    def json = '{"name": "Jenkins", "version": "2.0"}'
    def parsed = parseJson(json)
    echo "Name: ${parsed.name}"

    // WARNING: Cannot use pipeline steps (sh, echo, etc.) in @NonCPS methods
}
```

## Parallel Execution

### Basic Parallel

```groovy
node {
    stage('Parallel Tests') {
        parallel(
            'Unit Tests': {
                node('linux') {
                    sh 'make unit-test'
                }
            },
            'Integration Tests': {
                node('linux') {
                    sh 'make integration-test'
                }
            },
            'Smoke Tests': {
                node('linux') {
                    sh 'make smoke-test'
                }
            }
        )
    }
}
```

### Parallel with failFast

```groovy
node {
    stage('Deploy to Regions') {
        parallel(
            failFast: true,  // Stop all if one fails
            'Region US-EAST': {
                sh 'deploy-us-east.sh'
            },
            'Region US-WEST': {
                sh 'deploy-us-west.sh'
            },
            'Region EU': {
                sh 'deploy-eu.sh'
            }
        )
    }
}
```

### Dynamic Parallel Execution

```groovy
node {
    def branches = [:]

    def environments = ['dev', 'qa', 'staging']

    for (int i = 0; i < environments.size(); i++) {
        def env = environments[i]  // Important: capture variable

        branches["Deploy to ${env}"] = {
            node {
                echo "Deploying to ${env}"
                sh "deploy.sh ${env}"
            }
        }
    }

    parallel branches
}
```

## Working with Credentials

### Username and Password

```groovy
node {
    withCredentials([usernamePassword(
        credentialsId: 'my-credentials',
        usernameVariable: 'USERNAME',
        passwordVariable: 'PASSWORD'
    )]) {
        sh '''
            echo "Username: $USERNAME"
            # Use $PASSWORD in commands
        '''
    }
}
```

### Secret Text

```groovy
node {
    withCredentials([string(
        credentialsId: 'api-token',
        variable: 'API_TOKEN'
    )]) {
        sh 'curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com'
    }
}
```

### SSH Key

```groovy
node {
    withCredentials([sshUserPrivateKey(
        credentialsId: 'ssh-key',
        keyFileVariable: 'SSH_KEY',
        usernameVariable: 'SSH_USER'
    )]) {
        sh '''
            ssh -i $SSH_KEY $SSH_USER@server.example.com 'deploy.sh'
        '''
    }
}
```

### Multiple Credentials

```groovy
node {
    withCredentials([
        usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS'),
        string(credentialsId: 'api-key', variable: 'API_KEY')
    ]) {
        sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
        sh 'curl -H "X-API-Key: $API_KEY" https://api.example.com'
    }
}
```

## Environment Variables

### Setting Environment Variables

```groovy
node {
    // Using withEnv
    withEnv(['ENV=production', 'VERSION=1.0']) {
        sh 'echo "Environment: $ENV, Version: $VERSION"'
    }

    // Direct assignment
    env.MY_VAR = 'value'
    sh 'echo $MY_VAR'

    // From shell command
    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
}
```

### Accessing Environment Variables

```groovy
node {
    echo "Build number: ${env.BUILD_NUMBER}"
    echo "Job name: ${env.JOB_NAME}"
    echo "Workspace: ${env.WORKSPACE}"

    def branch = env.BRANCH_NAME ?: 'main'
    echo "Branch: ${branch}"
}
```

## Common Wrappers

### Timestamps

```groovy
timestamps {
    node {
        echo 'This output will have timestamps'
        sh 'sleep 5'
        echo 'Done'
    }
}
```

### Timeout

```groovy
timeout(time: 30, unit: 'MINUTES') {
    node {
        sh 'long-running-command'
    }
}

// With activity timeout
timeout(time: 5, unit: 'MINUTES', activity: true) {
    node {
        // Timeout if no console output for 5 minutes
        sh 'command-with-output'
    }
}
```

### Retry

```groovy
retry(3) {
    node {
        sh 'flaky-test-command'
    }
}

// With custom condition
retry(3) {
    try {
        sh 'test-command'
    } catch (Exception e) {
        if (e.message.contains('timeout')) {
            throw e  // Retry
        } else {
            return  // Don't retry
        }
    }
}
```

### Lock

```groovy
lock(resource: 'deployment-lock', inversePrecedence: true) {
    node {
        echo 'Only one build can deploy at a time'
        sh 'deploy.sh'
    }
}
```

### AnsiColor

```groovy
ansiColor('xterm') {
    node {
        sh 'ls --color=always'
    }
}
```

## Working with Docker

### Using Docker Images

```groovy
node {
    docker.image('maven:3.8.1-adoptopenjdk-11').inside {
        sh 'mvn --version'
        sh 'mvn clean package'
    }

    // With additional arguments
    docker.image('maven:3.8.1').inside('-v /tmp:/tmp -e MAVEN_OPTS="-Xmx1024m"') {
        sh 'mvn clean install'
    }
}
```

### Building Docker Images

```groovy
node {
    def image = docker.build("my-app:${env.BUILD_NUMBER}")

    // With custom Dockerfile
    def image2 = docker.build("my-app:latest", "-f Dockerfile.prod .")

    // Push to registry
    docker.withRegistry('https://registry.example.com', 'registry-credentials') {
        image.push()
        image.push('latest')
    }
}
```

### Running Docker Containers

```groovy
node {
    def container = docker.image('nginx:latest').run('-p 8080:80')

    try {
        // Run tests against container
        sh 'curl http://localhost:8080'
    } finally {
        container.stop()
    }
}
```

## Working with Git

### Basic Checkout

```groovy
node {
    checkout scm

    // Or explicit checkout
    checkout([
        $class: 'GitSCM',
        branches: [[name: '*/main']],
        userRemoteConfigs: [[
            url: 'https://github.com/user/repo.git',
            credentialsId: 'github-credentials'
        ]]
    ])
}
```

### Git Operations

```groovy
node {
    // Get commit info
    def commit = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
    def shortCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    def branch = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()

    echo "Commit: ${commit}"
    echo "Short: ${shortCommit}"
    echo "Branch: ${branch}"

    // Tag
    sh "git tag -a v${env.BUILD_NUMBER} -m 'Build ${env.BUILD_NUMBER}'"
    sh 'git push origin --tags'
}
```

## Stash and Unstash

```groovy
node('build-agent') {
    stage('Build') {
        sh 'make build'
        stash name: 'build-artifacts', includes: 'target/*.jar'
    }
}

node('deploy-agent') {
    stage('Deploy') {
        unstash 'build-artifacts'
        sh 'deploy.sh target/*.jar'
    }
}
```

## Input and Approval

```groovy
node {
    stage('Build') {
        sh 'make build'
    }

    stage('Approval') {
        def userInput = input(
            message: 'Deploy to production?',
            parameters: [
                choice(name: 'ENVIRONMENT', choices: ['staging', 'production'], description: 'Target environment'),
                string(name: 'VERSION', defaultValue: '1.0', description: 'Version to deploy')
            ],
            submitter: 'admin,ops'
        )

        echo "Deploying ${userInput.VERSION} to ${userInput.ENVIRONMENT}"
    }

    stage('Deploy') {
        sh "deploy.sh ${userInput.ENVIRONMENT} ${userInput.VERSION}"
    }
}
```

## Build Parameters

```groovy
properties([
    parameters([
        string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Deployment environment'),
        choice(name: 'VERSION', choices: ['1.0', '1.1', '2.0'], description: 'Version'),
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests')
    ])
])

node {
    echo "Environment: ${params.DEPLOY_ENV}"
    echo "Version: ${params.VERSION}"

    if (params.RUN_TESTS) {
        sh 'make test'
    }
}
```

## Accessing Build Information

```groovy
node {
    // Current build
    echo "Build number: ${currentBuild.number}"
    echo "Build result: ${currentBuild.result}"  // SUCCESS, FAILURE, UNSTABLE, ABORTED
    echo "Display name: ${currentBuild.displayName}"
    echo "Duration: ${currentBuild.duration}"

    // Set build properties
    currentBuild.displayName = "#${env.BUILD_NUMBER} - ${env.BRANCH_NAME}"
    currentBuild.description = "Deployed version ${version}"
    currentBuild.result = 'SUCCESS'

    // Previous build
    if (currentBuild.previousBuild) {
        echo "Previous result: ${currentBuild.previousBuild.result}"
    }
}
```

## Complete Example

```groovy
@Library('shared-library@master') _

// Build properties
properties([
    buildDiscarder(logRotator(numToKeepStr: '10')),
    disableConcurrentBuilds(),
    parameters([
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Target environment'),
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests')
    ])
])

// Variables
def version
def dockerImage

// Helper methods
def buildApp() {
    sh 'mvn clean package'
}

@NonCPS
def parseVersion(String pomXml) {
    def matcher = (pomXml =~ /<version>(.+)<\/version>/)
    return matcher[0][1]
}

// Main pipeline
timestamps {
    ansiColor('xterm') {
        node('linux') {
            try {
                stage('Checkout') {
                    checkout scm
                    version = sh(script: 'git describe --tags --always', returnStdout: true).trim()
                    currentBuild.displayName = "#${env.BUILD_NUMBER} - ${version}"
                }

                stage('Build') {
                    docker.image('maven:3.8.1-adoptopenjdk-11').inside {
                        buildApp()
                        stash name: 'app-jar', includes: 'target/*.jar'
                    }
                }

                if (!params.SKIP_TESTS) {
                    stage('Test') {
                        parallel(
                            'Unit Tests': {
                                sh 'mvn test'
                            },
                            'Integration Tests': {
                                sh 'mvn verify'
                            }
                        )
                        junit '**/target/test-results/*.xml'
                    }
                }

                stage('Docker Build') {
                    unstash 'app-jar'
                    dockerImage = docker.build("myapp:${version}")
                }

                if (params.ENVIRONMENT == 'production') {
                    stage('Approval') {
                        timeout(time: 1, unit: 'HOURS') {
                            input message: 'Deploy to production?', submitter: 'ops,admin'
                        }
                    }
                }

                stage('Deploy') {
                    withCredentials([
                        usernamePassword(credentialsId: 'registry-creds', usernameVariable: 'USER', passwordVariable: 'PASS'),
                        string(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')
                    ]) {
                        sh 'docker login -u $USER -p $PASS registry.example.com'
                        dockerImage.push()

                        sh """
                            kubectl set image deployment/myapp myapp=myapp:${version}
                            kubectl rollout status deployment/myapp
                        """
                    }
                }

                currentBuild.result = 'SUCCESS'

            } catch (Exception e) {
                currentBuild.result = 'FAILURE'
                echo "Pipeline failed: ${e.message}"
                throw e

            } finally {
                stage('Cleanup') {
                    cleanWs()

                    // Send notification
                    def color = currentBuild.result == 'SUCCESS' ? 'good' : 'danger'
                    slackSend color: color, message: "Build ${currentBuild.displayName}: ${currentBuild.result}"
                }
            }
        }
    }
}
```

## References

- [Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Groovy Language Documentation](http://groovy-lang.org/documentation.html)
- [Jenkins Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
