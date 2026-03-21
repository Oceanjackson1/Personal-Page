---
title: "Dockerfile 生成器"
description: "生成安全、高效、生产就绪的多阶段 Dockerfile"
category: "devops"
source: "community"
author: "Community"
tags: ["dockerfile", "generator"]
date: 2026-03-20
---

# Dockerfile Generator

## Overview

This skill provides a comprehensive workflow for generating production-ready Dockerfiles with security, optimization, and best practices built-in. Generates multi-stage builds, security-hardened configurations, and optimized layer structures with automatic validation and iterative error fixing.

**Key Features:**
- Multi-stage builds for optimal image size (50-85% reduction)
- Security hardening (non-root users, minimal base images, no secrets)
- Layer caching optimization for faster builds
- Language-specific templates (Node.js, Python, Go, Java)
- Automatic .dockerignore generation
- Integration with `dockerfile-validator` for validation
- Iterative validation and error fixing (minimum 1 iteration if errors found)
- Local references plus docs lookup fallback chain for framework-specific patterns

## When to Use This Skill

Invoke this skill when:
- Creating new Dockerfiles from scratch
- Containerizing applications (Node.js, Python, Go, Java, or other languages)
- Implementing multi-stage builds for size optimization
- Converting existing Dockerfiles to best practices
- Generating production-ready container configurations
- Optimizing Docker builds for security and performance
- The user asks to "create", "generate", "build", or "write" a Dockerfile
- Implementing containerization for microservices
- Setting up CI/CD pipeline container builds

### Trigger Phrases

Use this skill immediately when the request contains phrasing like:
- "Generate a production Dockerfile for my app"
- "Create a multi-stage Dockerfile for <language/framework>"
- "Containerize this service with security best practices"
- "Optimize this Dockerfile for size and build speed"
- "Write Dockerfile and .dockerignore for deployment"

## Do NOT Use This Skill For

- Validating existing Dockerfiles (use `dockerfile-validator` instead)
- Building or running containers (use docker build/run commands)
- Debugging running containers (use docker logs, docker exec)
- Managing Docker images or registries

## Deterministic Execution Model

Run these stages in order, and do not skip a stage unless the skip reason is reported in the final output.

1. Gather requirements (language, runtime version, entrypoint, exposed port, package manager, health endpoint).
2. Load references (local reference files first; external docs only when local references are insufficient).
3. Generate Dockerfile and `.dockerignore`.
4. Validate with `dockerfile-validator` or fallback local tools.
5. Iterate fixes until stop condition is met.
6. Publish final artifacts plus validation/audit report.

Stop conditions for stage 5:
- Stop when there are zero validation errors and no unapproved warnings.
- Stop after 3 iterations maximum, then emit an intentional-deviation report for unresolved findings.

## Reference Path Map

Consult these files directly by path as needed:
- `references/security_best_practices.md` for non-root users, secret handling, base image hardening, vulnerability scanning.
- `references/optimization_patterns.md` for multi-stage strategy, cache optimization, layer reduction, BuildKit cache mounts.
- `references/language_specific_guides.md` for language/framework runtime and package-manager patterns.
- `references/multistage_builds.md` for advanced stage-splitting and artifact-copy patterns.

## Dockerfile Generation Workflow

Follow this workflow when generating Dockerfiles. Adapt based on user needs:

### Stage 1: Gather Requirements

**Objective:** Understand what needs to be containerized and gather all necessary information.

**Information to Collect:**

1. **Application Details:**
   - Programming language and version (Node.js 18/20, Python 3.11/3.12, Go 1.21+, Java 17/21, etc.)
   - Application type (web server, API, CLI tool, batch job, etc.)
   - Framework (Express, FastAPI, Spring Boot, etc.)
   - Entry point (main file, command to run)

2. **Dependencies:**
   - Package manager (npm/yarn/pnpm, pip/poetry, go mod, maven/gradle)
   - System dependencies (build tools, libraries, etc.)
   - Build-time vs runtime dependencies

3. **Application Configuration:**
   - Port(s) to expose
   - Environment variables needed
   - Configuration files
   - Health check endpoint (for web services)
   - Volume mounts (if any)

4. **Build Requirements:**
   - Build commands
   - Test commands (optional)
   - Compilation needs (for compiled languages)
   - Static asset generation

5. **Production Requirements:**
   - Expected image size constraints
   - Security requirements
   - Scaling needs
   - Resource constraints (CPU, memory)

**Use AskUserQuestion if information is missing or unclear.**

**Example Questions:**
```
- What programming language and version is your application using?
- What is the main entry point to run your application?
- Does your application expose any ports? If so, which ones?
- Do you need any system dependencies beyond the base language runtime?
- Does your application need a health check endpoint?
```

### Stage 2: Framework/Library Documentation Lookup (if needed)

**Objective:** Research framework-specific containerization patterns and best practices.

**When to Perform This Stage:**
- User mentions a specific framework (Next.js, Django, FastAPI, Spring Boot, etc.)
- Application has complex build requirements
- Need guidance on framework-specific optimization

**Research Process (strict fallback chain):**

1. **Read local references first (required):**
   - `references/security_best_practices.md`
   - `references/optimization_patterns.md`
   - `references/language_specific_guides.md`

2. **Use Context7 docs lookup when local references are insufficient (preferred external source):**
   ```
   Use mcp__context7__resolve-library-id with the framework name
   Then use mcp__context7__query-docs with query:
   "docker deployment production build"
   ```

3. **Use web search only if Context7 is unavailable or missing needed details:**
   ```
   "<framework>" "<version>" dockerfile production deployment best practices
   ```

4. **If external lookup is unavailable (offline/tooling limits):**
   - Continue with local references and language templates in this file.
   - State assumptions explicitly in the output.
   - Mark the lookup limitation in the final report.

5. **Extract only actionable data:**
   - Recommended base image + version policy
   - Build optimization techniques
   - Required runtime environment variables
   - Production vs development differences
   - Security requirements specific to the framework

### Stage 3: Generate Dockerfile

**Objective:** Create a production-ready, multi-stage Dockerfile following best practices.

**Core Principles:**

1. **Multi-Stage Builds (REQUIRED for compiled languages, RECOMMENDED for all):**
   - Separate build stage from runtime stage
   - Keep build tools out of final image
   - Copy only necessary artifacts
   - Results in 50-85% smaller images

2. **Security Hardening (REQUIRED):**
   - Use specific version tags (NEVER use :latest)
   - Run as non-root user (create dedicated user)
   - Use minimal base images (alpine, distroless)
   - No hardcoded secrets
   - Scan base images for vulnerabilities

3. **Layer Optimization (REQUIRED):**
   - Order instructions from least to most frequently changing
   - Copy dependency files before application code
   - Combine related RUN commands with &&
   - Clean up package manager caches in same layer
   - Leverage build cache effectively

4. **Production Readiness (REQUIRED):**
   - Add HEALTHCHECK for services
   - Use exec form for ENTRYPOINT/CMD
   - Set WORKDIR to absolute paths
   - Document exposed ports with EXPOSE

**Language-Specific Templates:**

#### Node.js Multi-Stage Dockerfile

> **Build-stage dependency rule:** If the application has a build step (TypeScript,
> Vite, Webpack, etc.), install **all** dependencies in the builder stage (omit
> `--only=production`) and prune dev deps after the build. Using
> `--only=production` before a build step will cause `npm run build` to fail
> because dev tools are not installed.

```dockerfile
# syntax=docker/dockerfile:1

# Build stage — installs all deps so build tools (tsc, vite, etc.) are available,
# then prunes dev deps so the production stage only ships what is needed at runtime.
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependency files for caching
COPY package*.json ./
# Install ALL dependencies (including devDependencies required by the build step)
RUN npm ci && \
    npm cache clean --force

# Copy application code
COPY . .

# Build application and prune dev dependencies
RUN npm run build && \
    npm prune --production

# Production stage
FROM node:20-alpine AS production
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy pruned node_modules and built application from builder
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app .

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start application
CMD ["node", "index.js"]
```

> **Simple app (no build step):** If there is no compilation or bundling, install
> only production deps in the builder stage and copy source from the host context:
> ```dockerfile
> RUN npm ci --only=production && npm cache clean --force
> ...
> COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
> COPY --chown=nodejs:nodejs . .
> ```

#### Python Multi-Stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim AS production
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1001 appuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Update PATH and set Python production env vars
# PYTHONUNBUFFERED=1 ensures stdout/stderr are flushed immediately (essential for container logs)
# PYTHONDONTWRITEBYTECODE=1 prevents writing .pyc files to disk
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check (adjust endpoint as needed)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Start application
CMD ["python", "app.py"]
```

#### Go Multi-Stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o main .

# Production stage (using distroless for minimal image)
# gcr.io/distroless/static-debian12 IS a specific tag; hadolint DL3006 is a
# false positive for non-Docker-Hub registries.
# hadolint ignore=DL3006
FROM gcr.io/distroless/static-debian12 AS production
WORKDIR /

# Copy binary from builder
COPY --from=builder /app/main /main

# Expose port
EXPOSE 8080

# HEALTHCHECK is not supported in distroless images (no shell available)

# Switch to non-root user (distroless runs as nonroot by default)
USER nonroot:nonroot

# Start application
ENTRYPOINT ["/main"]
```

#### Java Multi-Stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM eclipse-temurin:21-jdk-jammy AS builder
WORKDIR /app

# Copy Maven wrapper and pom.xml
COPY mvnw pom.xml ./
COPY .mvn .mvn

# Download dependencies (cached layer)
RUN ./mvnw dependency:go-offline

# Copy source code
COPY src ./src

# Build application
RUN ./mvnw clean package -DskipTests && \
    mv target/*.jar target/app.jar

# Production stage (using JRE instead of JDK)
FROM eclipse-temurin:21-jre-jammy AS production
WORKDIR /app

# Install healthcheck dependency and create non-root user
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1001 appuser

# Copy JAR from builder
COPY --from=builder --chown=appuser:appuser /app/target/app.jar ./app.jar

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Start application
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Selection Logic:**
- Node.js: Use for JavaScript/TypeScript applications
- Python: Use for Python applications (web, API, scripts)
- Go: Use for Go applications (excellent for minimal images)
- Java: Use for Spring Boot, Quarkus, or other Java frameworks
- Generic: Create custom Dockerfile for other languages

**Always Include:**
1. Syntax directive: `# syntax=docker/dockerfile:1`
2. Multi-stage build (build + production stages)
3. Non-root user creation and usage
4. HEALTHCHECK for services (if applicable)
5. Proper WORKDIR settings
6. EXPOSE for documented ports
7. Clean package manager caches
8. exec form for CMD/ENTRYPOINT

### Stage 4: Generate .dockerignore

**Objective:** Create comprehensive .dockerignore to reduce build context and prevent secret leaks.

**Always create .dockerignore with generated Dockerfile.**

**Standard .dockerignore Template:**

```
# Git
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
.travis.yml
.circleci

# Documentation
README.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
*.md
docs/

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Environment
.env
.env.*
*.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Dependencies (language-specific - add as needed)
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/
target/
*.class

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
coverage/
.coverage
*.cover
.pytest_cache/
.tox/
test-results/

# Build artifacts
dist/
build/
*.egg-info/
```

**Customize based on language:**
- Node.js: Add `node_modules/`, `npm-debug.log`, `yarn-error.log`
- Python: Add `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`
- Go: Add `vendor/`, `*.exe`, `*.test`
- Java: Add `target/`, `*.class`, `*.jar` (except final artifact)

### Stage 5: Validate with `dockerfile-validator`

**Objective:** Ensure generated Dockerfile follows best practices and has no unresolved critical findings.

**REQUIRED: Always run validation after generation.**

**Primary path (preferred):**
1. Invoke `dockerfile-validator`.
2. Capture findings by severity (`error`, `warning`, `info`).
3. Prioritize security and reproducibility findings first.

**Fallback path (if skill invocation is unavailable):**
1. Try local validator script directly:
   ```bash
   bash ../dockerfile-validator/scripts/dockerfile-validate.sh Dockerfile
   ```
2. If that path is unavailable, run available tools directly:
   ```bash
   hadolint Dockerfile
   checkov -f Dockerfile --framework dockerfile
   ```
3. If one or more tools are unavailable, continue generation and report each skipped check in the final report.

**Expected validator stages:**
```
[1/4] Syntax Validation (hadolint)
[2/4] Security Scan (Checkov)
[3/4] Best Practices Validation
[4/4] Optimization Analysis
```

### Stage 6: Validate-Iterate Loop (Explicit Requirements)

**Objective:** Apply deterministic fix loops with auditable iteration records.

**Loop rules (required):**
1. Run at least one validation pass.
2. If any `error` exists, apply fixes and re-run validation.
3. Continue until:
   - no `error` remains, or
   - iteration count reaches 3.
4. For `warning`, either fix it or mark it as intentional deviation with justification.
5. Never silently suppress a finding.

**Iteration log format (required):**

| Iteration | Command/Path Used | Errors | Warnings | Fixes Applied | Result |
|-----------|-------------------|--------|----------|---------------|--------|
| 1 | `dockerfile-validator` or fallback command | N | N | short summary | pass/fail |
| 2 | ... | N | N | short summary | pass/fail |
| 3 | ... | N | N | short summary | pass/fail |

**Common fixes:**
- Add version tags to base images
- Add USER directive before CMD/ENTRYPOINT
- Add HEALTHCHECK for services
- Combine RUN commands where safe
- Clean package caches in same layer
- Replace `ADD` with `COPY` where archive/url behavior is not needed

### Stage 7: Final Review and Audit Report

**Objective:** Deliver runnable artifacts plus an auditable report.

**Deliverables (required):**
1. Generated files:
   - Dockerfile (validated and optimized)
   - `.dockerignore` (comprehensive)
2. Validation summary:
   - tool path used (primary vs fallback)
   - findings by severity
   - final status after loop
3. Iteration log table from Stage 6.
4. Intentional deviation report (only when applicable).
5. Usage instructions.
6. Optimization metrics and next steps.

**Intentional deviation report (required when any finding is not fixed):**

| ID | Rule/Check | Severity | Decision | Justification | Risk | Mitigation | Expiry/Review Date |
|----|------------|----------|----------|---------------|------|------------|--------------------|
| DEV-001 | e.g., DL3059 | warning | accepted | build step readability requirement | minor layer overhead | revisit after refactor | YYYY-MM-DD |

**Usage instructions template:**
```bash
# Build image
docker build -t myapp:1.0 .

# Run container
docker run -p 3000:3000 myapp:1.0

# Probe health endpoint (if exposed)
curl http://localhost:3000/health
```

**Optimization metrics (required):**
```
## Optimization Metrics

| Metric | Estimate |
|--------|----------|
| Image Size | ~150MB (vs ~500MB without multi-stage, 70% reduction) |
| Build Cache | Layer caching enabled for dependencies |
| Security | Non-root user, minimal base image, no secrets |
```

**Language-specific size estimates:**
- **Node.js**: ~50-150MB with Alpine (vs ~1GB with full node image)
- **Python**: ~150-250MB with slim (vs ~900MB with full python image)
- **Go**: ~5-20MB with distroless/scratch (vs ~800MB with full golang image)
- **Java**: ~200-350MB with JRE (vs ~500MB+ with JDK)

**Next steps (required):**
```
## Next Steps

- [ ] Test the build locally: `docker build -t myapp:1.0 .`
- [ ] Run and verify the container works as expected
- [ ] Update CI/CD pipeline to use the new Dockerfile
- [ ] Consider BuildKit cache mounts for faster builds (see references/optimization_patterns.md)
- [ ] Set up automated vulnerability scanning with `docker scout` or `trivy`
- [ ] Push to registry and deploy
```

## Generation Scripts (Optional Reference)

The `scripts/` directory contains standalone bash scripts for manual Dockerfile generation outside of this skill:

- `generate_nodejs.sh` - CLI tool for Node.js Dockerfiles
- `generate_python.sh` - CLI tool for Python Dockerfiles
- `generate_golang.sh` - CLI tool for Go Dockerfiles
- `generate_java.sh` - CLI tool for Java Dockerfiles
- `generate_dockerignore.sh` - CLI tool for .dockerignore generation

**Purpose:** These scripts are reference implementations and manual tools for users who want to generate Dockerfiles via command line without using skill invocation. They demonstrate the same best practices embedded in this skill.

**When using this skill:** Codex generates Dockerfiles directly using the templates and patterns documented in this SKILL.md, rather than invoking these scripts. The templates in this document are the authoritative source.

**Script usage example:**
```bash
# Manual Dockerfile generation
cd devops-skills-plugin/skills/dockerfile-generator/scripts
./generate_nodejs.sh --version 20 --port 3000 --output Dockerfile
```

**Node/Python entrypoint flags (script mode):**

| Flag | Purpose | Notes |
|------|---------|-------|
| `--entry` | Legacy shorthand entrypoint | Simple whitespace split only. Quoted values are rejected. |
| `--entry-cmd` | Preferred command/executable | Use with repeated `--entry-arg` for exact argv control. |
| `--entry-arg` | Preferred argument value | Repeat for each argument; spaces are preserved per arg. |

```bash
# Recommended for arguments containing spaces
./generate_nodejs.sh \
  --entry-cmd node \
  --entry-arg server.js \
  --entry-arg --message \
  --entry-arg "hello world"
```

## Best Practices Reference

### Security Best Practices

1. **Use Specific Tags:**
   ```dockerfile
   # Bad
   FROM node:alpine

   # Good
   FROM node:20-alpine

   # Better (with digest for reproducibility)
   FROM node:20-alpine@sha256:abc123...
   ```

2. **Run as Non-Root:**
   ```dockerfile
   # Create user
   RUN addgroup -g 1001 -S appgroup && \
       adduser -S appuser -u 1001 -G appgroup

   # Switch to user before CMD
   USER appuser
   ```

3. **Use Minimal Base Images:**
   - Alpine Linux (small, secure)
   - Distroless (no shell, minimal attack surface)
   - Specific runtime images (node:alpine vs node:latest)

4. **Never Hardcode Secrets:**
   ```dockerfile
   # Bad
   ENV API_KEY=secret123

   # Good - use build secrets
   # docker build --secret id=api_key,src=.env
   RUN --mount=type=secret,id=api_key \
       API_KEY=$(cat /run/secrets/api_key) ./configure
   ```

### Optimization Best Practices

1. **Layer Caching:**
   ```dockerfile
   # Copy dependency files first
   COPY package.json package-lock.json ./
   RUN npm ci

   # Copy application code last
   COPY . .
   ```

2. **Combine RUN Commands:**
   ```dockerfile
   # Bad (creates 3 layers)
   RUN apt-get update
   RUN apt-get install -y curl
   RUN rm -rf /var/lib/apt/lists/*

   # Good (creates 1 layer)
   RUN apt-get update && \
       apt-get install -y --no-install-recommends curl && \
       rm -rf /var/lib/apt/lists/*
   ```

3. **Multi-Stage Builds:**
   ```dockerfile
   # Build stage - can be large
   FROM node:20 AS builder
   WORKDIR /app
   COPY . .
   RUN npm install && npm run build

   # Production stage - minimal
   FROM node:20-alpine
   COPY --from=builder /app/dist ./dist
   CMD ["node", "dist/index.js"]
   ```

### Production Readiness

1. **Health Checks:**
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:3000/health || exit 1
   ```

2. **Proper Signals:**
   ```dockerfile
   # Use exec form for proper signal handling
   CMD ["node", "server.js"]  # Good
   CMD node server.js         # Bad (no signal forwarding)
   ```

3. **Metadata:**
   ```dockerfile
   LABEL maintainer="team@example.com" \
         version="1.0.0" \
         description="My application"
   ```

## Common Patterns

### Pattern 1: Node.js with Next.js

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

### Pattern 2: Python with FastAPI

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Pattern 3: Go CLI Tool

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /bin/app

FROM scratch
COPY --from=builder /bin/app /app
ENTRYPOINT ["/app"]
```

## Modern Docker Features (2025)

### Multi-Platform Builds with BuildX

**Use Case:** Build images that work on both AMD64 and ARM64 architectures (e.g., x86 servers and Apple Silicon Macs).

**Enable BuildX:**
```bash
# BuildX is included in Docker Desktop by default
# For Linux, ensure BuildX is installed
docker buildx version
```

**Create Multi-Platform Images:**
```bash
# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest \
  --push \
  .

# Build and load for current platform (testing)
docker buildx build \
  --platform linux/amd64 \
  -t myapp:latest \
  --load \
  .
```

**Dockerfile Considerations:**
```dockerfile
# Most Dockerfiles work across platforms automatically
# Use platform-specific base images when needed
FROM --platform=$BUILDPLATFORM node:20-alpine AS builder

# Access build arguments for platform info
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Building on $BUILDPLATFORM for $TARGETPLATFORM"
```

**When to Use:**
- Deploying to mixed infrastructure (x86 + ARM)
- Supporting Apple Silicon Macs in development
- Optimizing for AWS Graviton (ARM-based) instances
- Building cross-platform CLI tools

### Software Bill of Materials (SBOM)

**Use Case:** Generate SBOM for supply chain security and compliance (increasingly required in 2025).

**Generate SBOM During Build:**
```bash
# Generate SBOM with BuildKit (Docker 24.0+)
docker buildx build \
  --sbom=true \
  -t myapp:latest \
  .

# SBOM is attached as attestation to the image
# View SBOM
docker buildx imagetools inspect myapp:latest --format "{{ json .SBOM }}"
```

**Generate SBOM from Existing Image:**
```bash
# Using Syft
syft myapp:latest -o json > sbom.json

# Using Docker Scout
docker scout sbom myapp:latest
```

**SBOM Benefits:**
- Vulnerability tracking across supply chain
- License compliance verification
- Dependency transparency
- Audit trail for security reviews
- Required for government/enterprise contracts

**Integration with CI/CD:**
```yaml
# GitHub Actions example
- name: Build with SBOM
  run: |
    docker buildx build \
      --sbom=true \
      --provenance=true \
      -t myapp:latest \
      --push \
      .
```

### BuildKit Cache Mounts (Advanced)

**Use Case:** Dramatically faster builds by persisting package manager caches across builds.

**Already covered in detail in `references/optimization_patterns.md`.**

**Quick reference:**
```dockerfile
# syntax=docker/dockerfile:1

# NPM cache mount (30-50% faster builds)
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go module cache
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

## Error Handling

### Common Generation Issues

1. **Missing dependency files:**
   - Ensure package.json, requirements.txt, go.mod, pom.xml exist
   - Ask user to provide or generate template

2. **Unknown framework:**
   - Use local references first, then Context7, then web search
   - Fall back to generic template
   - Ask user for specific runtime/build requirements

3. **Validation failures:**
   - Apply fixes automatically
   - Iterate until clean
   - Document any suppressions

## Integration with Other Skills

This skill works well in combination with:
- **dockerfile-validator** - Validates generated Dockerfiles (REQUIRED)
- **k8s-yaml-generator** - Generate Kubernetes deployments for the container
- **helm-generator** - Create Helm charts with the container image

## Notes

- **Always use multi-stage builds** for compiled languages
- **Always create non-root user** for security
- **Always generate .dockerignore** to prevent secret leaks
- **Always validate** with `dockerfile-validator` (or explicit fallback checks)
- **Iterate at least once** if validation finds errors
- Use alpine or distroless base images when possible
- Pin all version tags (never use :latest)
- Clean up package manager caches in same layer
- Order Dockerfile instructions from least to most frequently changing
- Use BuildKit features for advanced optimization
- Test builds locally before committing
- Keep Dockerfiles simple and maintainable
- Document any non-obvious patterns with comments

## Done Criteria

Mark the task done only when all items below are true:
- Dockerfile and `.dockerignore` are generated.
- Validation has been executed via `dockerfile-validator` or documented fallback commands.
- Validate-iterate loop evidence is present (iteration log with command path, counts, and fixes).
- No remaining validation `error` findings.
- Every remaining `warning` has either a fix or an intentional-deviation report row.
- Output includes optimization metrics and actionable next steps.

## Sources

This skill is based on comprehensive research from authoritative sources:

**Official Docker Documentation:**
- [Docker Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Multi-stage Builds](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)

**Security Guidelines:**
- [Dockerfile Best Practices 2025](https://blog.bytescrum.com/dockerfile-best-practices-2025-secure-fast-and-modern)
- [Docker Security Best Practices](https://betterstack.com/community/guides/scaling-docker/docker-build-best-practices/)

**Optimization Resources:**
- [Docker Multistage Builds Guide](https://spacelift.io/blog/docker-multistage-builds)
- [Building Optimized Docker Images](https://developers-heaven.net/blog/building-optimized-docker-images-dockerfile-best-practices-multi-stage-builds/)

---

## Reference: Language_Specific_Guides

# Language-Specific Dockerfile Guides

## Overview

This guide provides best practices and optimized Dockerfile templates for popular programming languages and frameworks.

## Node.js

### Basic Node.js Application

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS base
WORKDIR /app

# Dependencies stage
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# Production stage
FROM base AS production
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
EXPOSE 3000
HEALTHCHECK CMD node -e "require('http').get('http://localhost:3000/health',(r)=>{process.exit(r.statusCode===200?0:1)})"
CMD ["node", "server.js"]
```

### Next.js Application

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

### Express.js API

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup && \
    chown -R appuser:appgroup /app
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD node -e "require('http').get('http://localhost:3000/health',(r)=>{process.exit(r.statusCode===200?0:1)})"
CMD ["node", "server.js"]
```

**Best Practices:**
- Use `npm ci` instead of `npm install` for deterministic builds
- Always use `package-lock.json` for version locking
- Run `npm cache clean --force` after install
- Use `--only=production` to exclude dev dependencies
- Set `NODE_ENV=production`

## Python

### Basic Python Application

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
```

### FastAPI Application

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Django Application

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
RUN useradd -m -u 1001 appuser
COPY --chown=appuser:appuser . .
RUN python manage.py collectstatic --noinput
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
```

**Best Practices:**
- Use `pip install --no-cache-dir` to reduce image size
- Install build dependencies in builder stage only
- Use wheels for compiled dependencies
- Set `PYTHONUNBUFFERED=1` for real-time container logs (stdout/stderr flushed immediately)
- Set `PYTHONDONTWRITEBYTECODE=1` to skip `.pyc` files in the image
- Use `--user` flag for pip install (non-root)

## Go

### Basic Go Application

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o main .

FROM alpine:3.21
RUN apk --no-cache add ca-certificates
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
COPY --from=builder /app/main .
USER appuser
EXPOSE 8080
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1
CMD ["./main"]
```

### Go with Distroless (Minimal)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o /main .

# gcr.io/distroless/static-debian12 IS a specific tag; hadolint DL3006 is a
# false positive for non-Docker-Hub registries.
# hadolint ignore=DL3006
FROM gcr.io/distroless/static-debian12
COPY --from=builder /main /main
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/main"]
```

### Go with Scratch (Absolute Minimal)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o /main .

FROM scratch
COPY --from=builder /main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001:1001
ENTRYPOINT ["/main"]
```

**Best Practices:**
- Use `CGO_ENABLED=0` for static binaries
- Use `-ldflags="-s -w"` to strip debug symbols
- Use scratch or distroless for minimal images
- Include ca-certificates if making HTTPS requests
- Use go modules (go.mod) for dependency management

## Java

### Spring Boot with Maven

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-jammy AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw clean package -DskipTests && mv target/*.jar target/app.jar

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder --chown=appuser:appuser /app/target/app.jar ./app.jar
USER appuser
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Spring Boot with Gradle

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-jammy AS builder
WORKDIR /app
COPY gradlew ./
COPY gradle gradle
COPY build.gradle settings.gradle ./
RUN ./gradlew dependencies --no-daemon
COPY src ./src
RUN ./gradlew build -x test --no-daemon && \
    mv build/libs/*.jar build/libs/app.jar

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder --chown=appuser:appuser /app/build/libs/app.jar ./app.jar
USER appuser
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Spring Boot Layered (Optimized)

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-jammy AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src ./src
RUN ./mvnw clean package -DskipTests
RUN java -Djarmode=layertools -jar target/*.jar extract --destination target/extracted

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
RUN useradd -m -u 1001 appuser
USER appuser
COPY --from=builder /app/target/extracted/dependencies/ ./
COPY --from=builder /app/target/extracted/spring-boot-loader/ ./
COPY --from=builder /app/target/extracted/snapshot-dependencies/ ./
COPY --from=builder /app/target/extracted/application/ ./
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

**Best Practices:**
- Use JRE instead of JDK for runtime (smaller)
- Use layered JARs for better caching
- Run `./mvnw dependency:go-offline` to cache dependencies
- Use `--no-daemon` with Gradle to avoid background processes
- Set appropriate Java heap size with `-Xmx` and `-Xms`

## Rust

### Rust Application

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.75-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev
COPY Cargo.toml Cargo.lock ./
# Cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src
COPY src ./src
RUN touch src/main.rs && cargo build --release

FROM alpine:3.21
RUN apk --no-cache add ca-certificates
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
COPY --from=builder /app/target/release/app ./
USER appuser
EXPOSE 8080
CMD ["./app"]
```

## Ruby

### Ruby on Rails

```dockerfile
# syntax=docker/dockerfile:1
FROM ruby:3.3-alpine AS builder
WORKDIR /app
RUN apk add --no-cache build-base postgresql-dev nodejs yarn
COPY Gemfile Gemfile.lock ./
RUN bundle install --without development test
COPY package.json yarn.lock ./
RUN yarn install --production
COPY . .
RUN bundle exec rake assets:precompile

FROM ruby:3.3-alpine
WORKDIR /app
RUN apk add --no-cache postgresql-client nodejs
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder --chown=appuser:appgroup /app ./
USER appuser
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
```

## PHP

### PHP with Laravel

```dockerfile
# syntax=docker/dockerfile:1
FROM composer:2 AS composer
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist

FROM php:8.3-fpm-alpine
WORKDIR /app
RUN apk add --no-cache postgresql-dev && \
    docker-php-ext-install pdo pdo_pgsql
COPY --from=composer /app/vendor ./vendor
COPY . .
RUN composer dump-autoload --optimize --classmap-authoritative
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup && \
    chown -R appuser:appgroup /app
USER appuser
EXPOSE 9000
CMD ["php-fpm"]
```

## .NET

### ASP.NET Core

```dockerfile
# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder
WORKDIR /app
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=builder --chown=appuser:appuser /app/out ./
USER appuser
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

## Common Patterns Across Languages

### Development vs Production

```dockerfile
# syntax=docker/dockerfile:1
ARG NODE_ENV=production

FROM node:20-alpine AS development
ENV NODE_ENV=development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

FROM node:20-alpine AS production
ENV NODE_ENV=production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
CMD ["node", "server.js"]

FROM ${NODE_ENV} AS final
```

### With Database Migrations

```dockerfile
# Add entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "app.py"]
```

**docker-entrypoint.sh:**
```bash
#!/bin/sh
set -e

# Run migrations
python manage.py migrate

# Start application
exec "$@"
```

## Framework-Specific Tips

### Next.js
- Use standalone output mode for smaller images
- Set `NEXT_TELEMETRY_DISABLED=1`
- Copy only `.next/standalone` and `.next/static`

### Django
- Run `collectstatic` during build
- Use gunicorn or uvicorn for production
- Include database client libraries

### Spring Boot
- Use layered JARs for better caching
- Include actuator for health checks
- Set appropriate JVM memory limits

### FastAPI
- Use uvicorn with workers for production
- Include health check endpoint
- Use `--proxy-headers` if behind proxy

## References

- [Official Docker Samples](https://github.com/docker/awesome-compose)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)
- [Python Docker Best Practices](https://docs.python-guide.org/shipping/docker/)
- [Go Docker Best Practices](https://docs.docker.com/language/golang/build-images/)

---

## Reference: Multistage_Builds

# Multi-Stage Docker Builds

## Overview

Multi-stage builds allow you to use multiple FROM statements in your Dockerfile. Each FROM instruction can use a different base, and each begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don't want in the final image.

**Benefits:**
- **Smaller images:** 50-85% size reduction
- **Separation of concerns:** Build vs runtime environments
- **Better security:** No build tools in production images
- **Faster deployments:** Smaller images transfer faster
- **Cleaner builds:** No manual cleanup scripts needed

## Basic Syntax

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Named "builder"
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Stage 2: Final production image
FROM alpine:3.21
COPY --from=builder /app/myapp /usr/local/bin/
CMD ["myapp"]
```

## Stage Naming

### Explicit Names (Recommended)

```dockerfile
# Name stages explicitly for clarity
FROM node:20 AS dependencies
RUN npm install

FROM node:20 AS builder
COPY --from=dependencies /app/node_modules ./node_modules
RUN npm run build

FROM node:20-alpine AS production
COPY --from=builder /app/dist ./dist
```

### Numeric References (Less Clear)

```dockerfile
# Reference previous stages by number (0-indexed)
FROM node:20
RUN npm install

FROM node:20
COPY --from=0 /app/node_modules ./node_modules
RUN npm run build

FROM node:20-alpine
COPY --from=1 /app/dist ./dist
```

## Common Patterns

### Pattern 1: Build and Runtime Separation

**Use Case:** Compiled languages (Go, Rust, C++, Java)

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o main .

# Runtime stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

**Size Impact:**
- Builder stage: ~300MB
- Final image: ~8MB
- **Reduction: 97%**

### Pattern 2: Dependency Installation

**Use Case:** Separate dependency installation from application code

```dockerfile
# Dependency stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Benefits:**
- Cached dependency layer (only rebuilds when package.json changes)
- Production dependencies only in final image
- Faster builds with layer caching

### Pattern 3: Test Stage

**Use Case:** Run tests without including test dependencies in final image

```dockerfile
# Dependency stage
FROM python:3.12-slim AS deps
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --user -r requirements.txt

# Test stage
FROM deps AS test
RUN pip install --user -r requirements-dev.txt
COPY . .
RUN pytest tests/

# Production stage
FROM python:3.12-slim AS production
WORKDIR /app
COPY --from=deps /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Build with tests:**
```bash
docker build --target test -t myapp:test .
```

**Build production (tests automatically run before this stage):**
```bash
docker build -t myapp:latest .
```

### Pattern 4: Multi-Architecture

**Use Case:** Build for different platforms

```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.21-alpine AS builder
ARG TARGETARCH
ARG TARGETOS
WORKDIR /app
COPY . .
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o app

FROM alpine:3.21
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
```

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### Pattern 5: Development vs Production

**Use Case:** Different images for dev and prod

```dockerfile
# Base stage with common dependencies
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Development stage
FROM base AS development
ENV NODE_ENV=development
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM base AS builder
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

**Build for development:**
```bash
docker build --target development -t myapp:dev .
```

**Build for production:**
```bash
docker build --target production -t myapp:prod .
```

## Language-Specific Examples

### Node.js (Next.js)

```dockerfile
# syntax=docker/dockerfile:1

# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner stage
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

### Python (Django/FastAPI)

```dockerfile
# syntax=docker/dockerfile:1

# Builder stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Runner stage
FROM python:3.12-slim AS runner
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
RUN useradd -m -u 1001 appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Go (Minimal)

```dockerfile
# syntax=docker/dockerfile:1

# Builder stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-s -w" -o main .

# Runner stage (scratch = 0 bytes base)
FROM scratch
COPY --from=builder /app/main /main
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001:1001
ENTRYPOINT ["/main"]
```

### Java (Spring Boot)

```dockerfile
# syntax=docker/dockerfile:1

# Dependencies stage
FROM eclipse-temurin:21-jdk-jammy AS deps
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline

# Builder stage
FROM deps AS builder
COPY src ./src
RUN ./mvnw clean package -DskipTests

# Extractor stage (for layered JAR)
FROM builder AS extractor
WORKDIR /app
RUN java -Djarmode=layertools -jar target/*.jar extract --destination target/extracted

# Runner stage
FROM eclipse-temurin:21-jre-jammy AS runner
WORKDIR /app
RUN useradd -m -u 1001 appuser
USER appuser
COPY --from=extractor /app/target/extracted/dependencies/ ./
COPY --from=extractor /app/target/extracted/spring-boot-loader/ ./
COPY --from=extractor /app/target/extracted/snapshot-dependencies/ ./
COPY --from=extractor /app/target/extracted/application/ ./
EXPOSE 8080
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

## Advanced Techniques

### Copying from External Images

```dockerfile
# Copy from official images
FROM alpine:3.21 AS production
COPY --from=nginx:alpine /usr/share/nginx/html /usr/share/nginx/html
COPY --from=myregistry/common:latest /app/lib /app/lib
```

### Conditional Stages (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1
ARG BUILD_ENV=production

FROM node:20 AS development
ENV NODE_ENV=development
CMD ["npm", "run", "dev"]

FROM node:20-alpine AS production
ENV NODE_ENV=production
CMD ["node", "dist/server.js"]

FROM ${BUILD_ENV} AS final
```

```bash
docker build --build-arg BUILD_ENV=development -t myapp:dev .
docker build --build-arg BUILD_ENV=production -t myapp:prod .
```

### Parallel Stages

```dockerfile
# syntax=docker/dockerfile:1

# Independent stages run in parallel
FROM alpine AS fetch-config
RUN wget https://example.com/config.json -O /config.json

FROM alpine AS fetch-data
RUN wget https://example.com/data.csv -O /data.csv

# Final stage waits for both
FROM alpine AS final
COPY --from=fetch-config /config.json /app/
COPY --from=fetch-data /data.csv /app/
```

## Build Optimization

### Target Specific Stage

```bash
# Build only up to specific stage
docker build --target builder -t myapp:builder .

# Useful for debugging
docker run -it myapp:builder /bin/sh
```

### Cache Mounts with Multi-Stage

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o app

FROM alpine:3.21
COPY --from=builder /app/app /app
CMD ["/app"]
```

## Best Practices

### 1. Order Stages Logically

```dockerfile
# dependencies → builder → test → production
FROM node:20 AS deps
# Install dependencies

FROM deps AS builder
# Build application

FROM builder AS test
# Run tests

FROM node:20-alpine AS production
# Minimal runtime
```

### 2. Name Stages Clearly

```dockerfile
# Good
FROM golang:1.21 AS compiler
FROM alpine:3.21 AS runtime

# Bad
FROM golang:1.21 AS stage1
FROM alpine:3.21 AS stage2
```

### 3. Minimize Final Stage

```dockerfile
# Copy only what's needed
COPY --from=builder /app/binary /app/binary

# Don't copy unnecessary files
# Bad: COPY --from=builder /app /app
```

### 4. Use Specific Base Images per Stage

```dockerfile
# JDK for building
FROM eclipse-temurin:21-jdk-jammy AS builder

# JRE for running (smaller)
FROM eclipse-temurin:21-jre-jammy AS runner
```

### 5. Document Stages

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Install and cache dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build application with dependencies
FROM deps AS builder
COPY . .
RUN npm run build

# Stage 3: Production runtime with minimal footprint
FROM node:20-alpine AS production
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]
```

## Common Pitfalls

### 1. Not Using Stage Names

```dockerfile
# Hard to maintain
FROM node:20
COPY --from=0 /app/node_modules ./node_modules

# Better
FROM node:20 AS deps
COPY --from=deps /app/node_modules ./node_modules
```

### 2. Copying Entire Stage

```dockerfile
# Bad - copies everything including build tools
COPY --from=builder /app /app

# Good - copy only artifacts
COPY --from=builder /app/dist /app/dist
```

### 3. Not Leveraging Cache

```dockerfile
# Bad - copy all before installing
COPY . .
RUN npm install

# Good - install dependencies first (cached)
COPY package*.json ./
RUN npm install
COPY . .
```

## Troubleshooting

### Check Stage Sizes

```bash
# Build with specific target
docker build --target builder -t myapp:builder .
docker build --target production -t myapp:production .

# Compare sizes
docker images | grep myapp
```

### Debug Intermediate Stages

```bash
# Build up to specific stage
docker build --target builder -t debug:builder .

# Run and inspect
docker run -it debug:builder /bin/sh
```

### View Build Process

```bash
# Enable BuildKit with progress
DOCKER_BUILDKIT=1 docker build --progress=plain .

# See all stages and their timing
```

## References

- [Docker Multi-stage Builds Documentation](https://docs.docker.com/build/building/multi-stage/)
- [Multi-stage Build Examples](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)
- [BuildKit Features](https://docs.docker.com/build/buildkit/)

---

## Reference: Optimization_Patterns

# Dockerfile Optimization Patterns

## Overview

This guide provides comprehensive optimization techniques for reducing Docker image size, improving build times, and enhancing runtime performance.

## Image Size Optimization

### Use Multi-Stage Builds

**Impact:** 50-85% size reduction

```dockerfile
# Before: Single stage (500MB)
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "dist/server.js"]

# After: Multi-stage (150MB)
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

### Choose Minimal Base Images

**Size Comparison:**
```
ubuntu:22.04          → 77MB
node:20               → 996MB
node:20-slim          → 239MB
node:20-alpine        → 132MB
alpine:3.21           → 7.8MB
distroless/static     → 2MB
scratch               → 0MB
```

**Selection Guide:**
- **Full OS (ubuntu, debian):** When you need many system tools
- **Slim variants:** Good balance of size and compatibility
- **Alpine:** Minimal size, may have glibc compatibility issues
- **Distroless:** Highest security, minimal attack surface
- **Scratch:** For static binaries only (Go, Rust)

### Remove Unnecessary Files

```dockerfile
# Clean up in same RUN layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Remove build artifacts
RUN npm run build && \
    rm -rf src/ tests/ docs/

# Use .dockerignore
# (prevents files from being sent to build context)
```

## Build Time Optimization

### Layer Caching Strategy

**Order instructions from least to most frequently changing:**

```dockerfile
# Bad - Invalidates cache on any code change
COPY . /app
RUN npm install

# Good - Cache dependencies separately
COPY package*.json /app/
RUN npm install
COPY . /app
```

**Optimal Layer Order:**
1. Base image (FROM)
2. System packages (RUN apt-get)
3. Application dependencies (package.json, requirements.txt)
4. Application code (COPY . .)
5. Build commands (RUN build)
6. Runtime configuration (CMD, ENTRYPOINT)

### BuildKit Cache Mounts

**Mount external caches to persist across builds:**

```dockerfile
# syntax=docker/dockerfile:1

# NPM cache mount
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go module cache
FROM golang:1.21-alpine
WORKDIR /app
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Pip cache
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Enable BuildKit:**
```bash
export DOCKER_BUILDKIT=1
docker build .
```

### Parallel Stage Execution

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine AS fetch-1
RUN wget https://example.com/file1

FROM alpine AS fetch-2
RUN wget https://example.com/file2

FROM alpine AS final
COPY --from=fetch-1 /file1 .
COPY --from=fetch-2 /file2 .
```

BuildKit automatically parallelizes independent stages.

## Layer Optimization

### Combine RUN Commands

```dockerfile
# Bad - Creates 5 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim
RUN rm -rf /var/lib/apt/lists/*

# Good - Creates 1 layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        vim && \
    rm -rf /var/lib/apt/lists/*
```

### Minimize Layer Count

**Each instruction creates a layer:**
- FROM, RUN, COPY, ADD create layers
- ENV, WORKDIR, EXPOSE, USER do not create significant layers
- Combine related operations

```dockerfile
# Bad - Many layers
COPY package.json .
COPY package-lock.json .
COPY tsconfig.json .
COPY src/ ./src/
COPY tests/ ./tests/

# Good - Fewer layers (use .dockerignore)
COPY . .
```

### Layer Size Analysis

```bash
# Inspect layer sizes
docker history myimage:latest

# Find large layers
docker history --no-trunc --format "table {{.Size}}\t{{.CreatedBy}}" myimage:latest | sort -hr | head -10
```

## Dependency Optimization

### Install Only Production Dependencies

**Node.js:**
```dockerfile
# Development dependencies excluded
RUN npm ci --only=production

# Or use package.json scripts
RUN npm ci --omit=dev
```

**Python:**
```dockerfile
# Create separate requirements files
# requirements.txt (production)
# requirements-dev.txt (development)
RUN pip install --no-cache-dir -r requirements.txt
```

**Java (Maven):**
```dockerfile
# Skip tests during build
RUN ./mvnw clean package -DskipTests
```

### Remove Development Tools

```dockerfile
# Multi-stage: Keep build tools in builder stage
FROM golang:1.21 AS builder
RUN apk add --no-cache git make
RUN make build

FROM alpine:3.21
# No build tools in final image
COPY --from=builder /app/binary /app/
```

## .dockerignore Optimization

**Reduces build context size and build time:**

```dockerignore
# Version control
.git
.gitignore

# Dependencies (installed during build)
node_modules
vendor
__pycache__

# IDE files
.vscode
.idea
*.swp

# Build artifacts
dist
build
target

# Documentation
*.md
docs/

# CI/CD
.github
.gitlab-ci.yml

# Environment files
.env
.env.*

# Logs
*.log
logs/

# Tests
tests/
*.test
coverage/
```

**Impact:**
- Smaller build context → Faster upload to Docker daemon
- Fewer files → Faster COPY operations
- No accidental secret leaks

## Runtime Performance

### Use Exec Form for CMD/ENTRYPOINT

```dockerfile
# Bad - Shell form (spawns extra sh process)
CMD node server.js

# Good - Exec form (direct process execution)
CMD ["node", "server.js"]

# Benefits:
# - Proper signal handling (SIGTERM, SIGINT)
# - Faster startup
# - Lower memory usage
```

### Optimize Application

```dockerfile
# Node.js: Use production mode
ENV NODE_ENV=production

# Python: Use optimized bytecode
ENV PYTHONOPTIMIZE=1

# Java: Set heap size
ENV JAVA_OPTS="-Xms512m -Xmx2048m"

# Go: Build with optimizations
RUN go build -ldflags="-s -w" -o app
```

### Health Checks

```dockerfile
# Efficient health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Avoid heavy health checks
# Bad: HEALTHCHECK CMD curl http://localhost/full-db-check
```

## Build Optimization Checklist

- [ ] Use multi-stage builds
- [ ] Choose minimal base images (Alpine, distroless)
- [ ] Order layers from least to most frequently changing
- [ ] Combine RUN commands where logical
- [ ] Use BuildKit cache mounts
- [ ] Create comprehensive .dockerignore
- [ ] Install only production dependencies
- [ ] Clean package manager caches in same layer
- [ ] Remove development tools from final image
- [ ] Use exec form for CMD/ENTRYPOINT
- [ ] Optimize application for production
- [ ] Add efficient health checks

## Advanced Techniques

### Squash Layers (Use with Caution)

```bash
# Squash all layers into one (loses layer caching)
docker build --squash -t myapp:latest .
```

**Use Cases:**
- Final production images
- When layer caching isn't important
- To hide sensitive information in layers (better: use multi-stage)

**Drawbacks:**
- Loses layer caching benefits
- Larger initial download
- Less transparent image history

### BuildKit Secrets (Zero-Copy Secrets)

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=aws_credentials \
    aws configure set credentials $(cat /run/secrets/aws_credentials)
```

```bash
docker build --secret id=aws_credentials,src=$HOME/.aws/credentials .
```

### Cross-Platform Builds

```dockerfile
# Build for multiple platforms
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t myapp:latest \
    .
```

## Measuring Optimization Impact

### Before and After Comparison

```bash
# Build original
docker build -t myapp:before .
docker images myapp:before

# Build optimized
docker build -t myapp:after .
docker images myapp:after

# Compare sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep myapp
```

### Build Time Measurement

```bash
# Measure build time
time docker build -t myapp:latest .

# Measure with cache
docker build -t myapp:cached .

# Measure without cache
docker build --no-cache -t myapp:no-cache .
```

### Dive Tool (Layer Analysis)

```bash
# Install dive
brew install dive  # macOS
# or download from https://github.com/wagoodman/dive

# Analyze image
dive myapp:latest
```

## Real-World Examples

### Node.js Optimization

**Before (996MB):**
```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

**After (50MB, 95% reduction):**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/server.js ./
CMD ["node", "server.js"]
```

### Go Optimization

**Before (800MB):**
```dockerfile
FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build -o app
CMD ["./app"]
```

**After (8MB, 99% reduction):**
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o app

FROM scratch
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
```

## References

- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Image Size Optimization](https://betterstack.com/community/guides/scaling-docker/docker-build-best-practices/)

---

## Reference: Security_Best_Practices

# Dockerfile Security Best Practices

## Overview

This guide provides comprehensive security best practices for writing secure Dockerfiles. Security should be a primary consideration when containerizing applications.

## Table of Contents

1. [Base Image Security](#base-image-security)
2. [User Management](#user-management)
3. [Secrets Management](#secrets-management)
4. [Dependency Management](#dependency-management)
5. [Attack Surface Reduction](#attack-surface-reduction)
6. [Vulnerability Scanning](#vulnerability-scanning)

## Base Image Security

### Use Specific Tags

**Problem:** Using `:latest` tag can lead to unpredictable builds and security vulnerabilities.

```dockerfile
# Bad - Unpredictable, may pull vulnerable versions
FROM node:latest

# Good - Specific version
FROM node:20-alpine

# Better - Specific version with digest for reproducibility
FROM node:20-alpine@sha256:2c6c59cf4d34d4f937ddfcf33bab9d8bbad8658d1b9de7b97622566a52167f5b
```

### Use Minimal Base Images

**Principle:** Smaller images have fewer attack vectors.

```dockerfile
# Large attack surface (>1GB)
FROM ubuntu:22.04

# Medium attack surface (~200MB)
FROM node:20

# Small attack surface (~50MB)
FROM node:20-alpine

# Minimal attack surface (~2MB for Go apps)
FROM gcr.io/distroless/static-debian12
```

**Recommended Base Images:**
- **Alpine Linux:** Minimal Linux distribution (~5MB base)
- **Distroless:** Google's minimal container images (no shell, package managers)
- **Scratch:** Empty base image (for static binaries only)

### Scan Base Images

```bash
# Use Trivy to scan base images
trivy image node:20-alpine

# Use Snyk
snyk container test node:20-alpine

# Use Docker Scout
docker scout cves node:20-alpine
```

## User Management

### Never Run as Root

**Problem:** Running as root gives attackers full system access if container is compromised.

```dockerfile
# Bad - Runs as root (default)
FROM node:20-alpine
COPY . /app
CMD ["node", "server.js"]

# Good - Creates and uses non-root user
FROM node:20-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
COPY --chown=nodejs:nodejs . /app
USER nodejs
CMD ["node", "server.js"]
```

### User Creation Patterns

**Alpine Linux:**
```dockerfile
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup
USER appuser
```

**Debian/Ubuntu:**
```dockerfile
RUN useradd -m -u 1001 appuser
USER appuser
```

**Distroless (built-in nonroot user):**
```dockerfile
FROM gcr.io/distroless/static-debian12
USER nonroot:nonroot
```

### Set Proper File Permissions

```dockerfile
# Copy with ownership
COPY --chown=appuser:appuser . /app

# Ensure executables have correct permissions
RUN chmod +x /app/entrypoint.sh
```

## Secrets Management

### Never Hardcode Secrets

```dockerfile
# Bad - Hardcoded secrets
ENV API_KEY=sk_live_abc123
ENV DATABASE_PASSWORD=password123

# Good - Use runtime environment variables
ENV API_KEY=""
ENV DATABASE_PASSWORD=""
```

### Use Build Secrets (BuildKit)

```dockerfile
# Mount secrets during build (never stored in image layers)
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    echo "Configuring with API key..." && \
    # Use API_KEY here
    rm -f /run/secrets/api_key
```

**Build command:**
```bash
docker build --secret id=api_key,src=.env .
```

### Avoid Secrets in Layers

```dockerfile
# Bad - Secret remains in image history
FROM alpine
RUN echo "SECRET_KEY=abc123" > /app/config
RUN rm /app/config  # Secret still in previous layer!

# Good - Use multi-stage builds or build secrets
FROM alpine
RUN --mount=type=secret,id=config \
    cat /run/secrets/config > /app/config && \
    process_config && \
    rm /app/config
```

## Dependency Management

### Pin Dependency Versions

```dockerfile
# Bad - Unpinned versions
RUN apt-get install -y curl git

# Good - Pinned versions
RUN apt-get install -y \
    curl=7.81.0-1ubuntu1.16 \
    git=1:2.34.1-1ubuntu1.11
```

**Node.js:**
```dockerfile
# Use package-lock.json or yarn.lock
COPY package*.json ./
RUN npm ci  # Uses lock file
```

**Python:**
```dockerfile
# Pin versions in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Go:**
```dockerfile
# go.sum ensures reproducible builds
COPY go.mod go.sum ./
RUN go mod download
```

### Clean Package Manager Caches

```dockerfile
# Alpine (apk)
RUN apk add --no-cache curl

# Debian/Ubuntu (apt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Node.js (npm)
RUN npm ci && npm cache clean --force

# Python (pip)
RUN pip install --no-cache-dir -r requirements.txt
```

## Attack Surface Reduction

### Minimize Installed Packages

```dockerfile
# Bad - Installs unnecessary packages
RUN apt-get install -y \
    curl \
    wget \
    vim \
    sudo \
    ssh

# Good - Only essential packages
RUN apt-get install -y --no-install-recommends \
    curl \
    ca-certificates
```

### Use Multi-Stage Builds

```dockerfile
# Build stage - can include build tools
FROM golang:1.21-alpine AS builder
RUN apk add --no-cache git make
COPY . .
RUN make build

# Production stage - minimal runtime
FROM alpine:3.21
COPY --from=builder /app/binary /app/binary
CMD ["/app/binary"]
```

### Remove Build Dependencies

```dockerfile
# Install, use, and remove in same layer
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
```

### Disable Unnecessary Services

```dockerfile
# Don't include SSH, telnet, or other services
# Use docker exec for debugging instead
```

## Network Security

### Expose Only Necessary Ports

```dockerfile
# Document exposed ports
EXPOSE 8080

# Don't expose unnecessary ports
# Bad: EXPOSE 22 (SSH)
# Bad: EXPOSE 3306 (MySQL in app container)
```

### Use Non-Privileged Ports

```dockerfile
# Good - Use port > 1024 (doesn't require root)
EXPOSE 8080

# Avoid privileged ports (< 1024)
# EXPOSE 80  # Requires root
```

## Vulnerability Scanning

### Integrate Scanning into CI/CD

```yaml
# GitHub Actions example
- name: Scan Docker image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    format: 'sarif'
    output: 'trivy-results.sarif'
```

### Regular Image Updates

```dockerfile
# Rebuild images regularly to get security patches
FROM node:20-alpine  # Alpine releases security updates frequently
```

### Scan for Secrets

```bash
# Use gitleaks or trufflehog
docker run -v $(pwd):/path zricethezav/gitleaks:latest detect --source=/path

# Use hadolint to detect some secret patterns
hadolint Dockerfile
```

## Security Checklist

- [ ] Use specific base image tags (no `:latest`)
- [ ] Use minimal base images (Alpine, distroless)
- [ ] Create and use non-root user
- [ ] Never hardcode secrets
- [ ] Use build secrets for sensitive data
- [ ] Pin dependency versions
- [ ] Clean package manager caches
- [ ] Minimize installed packages
- [ ] Use multi-stage builds
- [ ] Expose only necessary ports
- [ ] Scan images for vulnerabilities
- [ ] Update base images regularly
- [ ] Use HEALTHCHECK for services
- [ ] Validate with hadolint and Checkov

## Common Vulnerabilities

### CVE-Related Issues

1. **Outdated base images:** Rebuild regularly
2. **Known vulnerable packages:** Scan and update
3. **Missing security patches:** Use latest patch versions

### Configuration Issues

1. **Running as root:** Create non-root user
2. **Exposed secrets:** Use build secrets or runtime config
3. **Unnecessary packages:** Minimize attack surface
4. **Missing health checks:** Add HEALTHCHECK directive

## Tools for Security

- **Trivy:** Comprehensive vulnerability scanner
- **Snyk:** Security scanning and monitoring
- **Checkov:** Policy-as-code security scanning
- **hadolint:** Dockerfile linting with security rules
- **Docker Scout:** Docker's official security tool
- **Clair:** Container vulnerability analysis
- **Anchore:** Container security and compliance

## References

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Snyk Docker Security Best Practices](https://snyk.io/learn/docker-security/)
