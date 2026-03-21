---
title: "Dockerfile Validator"
description: "Validate, lint, audit, or scan a Dockerfile for security and best practices."
category: "devops"
source: "community"
author: "Community"
tags: ["dockerfile", "validator"]
date: 2026-03-20
---

# Dockerfile Validator

Validate Dockerfiles with deterministic stages, clear severity reporting, and explicit fallbacks when tools or network access are constrained.

## Trigger Phrases

Use this skill when the user asks for tasks like:
- "validate this Dockerfile"
- "lint/check my Dockerfile"
- "security scan Dockerfile"
- "optimize Docker image size/build time"
- "review Dockerfile before merge"
- "find issues in Dockerfile.prod/Dockerfile.dev"

## Use / Do Not Use

Use this skill for:
- Syntax and lint validation
- Security and secrets checks
- Best-practice and performance review
- Dockerfile hardening before CI/CD or production

Do not use this skill for:
- Generating a new Dockerfile from scratch (use `dockerfile-generator`)
- Running containers, debugging runtime behavior, or image registry operations

## Local Files In This Skill

- Validator script: `scripts/dockerfile-validate.sh`
- References:
  - `references/security_checklist.md`
  - `references/optimization_guide.md`
  - `references/docker_best_practices.md`
- Example Dockerfiles: `examples/*.Dockerfile`

## Deterministic Execution Flow (Required)

Run these steps in order. Do not skip steps unless a documented fallback branch applies.

### 1. Preflight and Path Setup

Assume repo root as working directory:

```bash
cd /path/to/repo
SKILL_DIR="devops-skills-plugin/skills/dockerfile-validator"
TARGET_DOCKERFILE="Dockerfile"   # replace when user provides a path
```

Validate inputs before running tools:

```bash
test -f "$SKILL_DIR/scripts/dockerfile-validate.sh"
test -f "$TARGET_DOCKERFILE"
```

If either check fails, stop and report the exact missing path.

### 2. Read the Target Dockerfile Explicitly

Use explicit file-read commands (not abstract "Read tool" wording):

```bash
sed -n '1,220p' "$TARGET_DOCKERFILE"
```

If needed for long files:

```bash
sed -n '220,440p' "$TARGET_DOCKERFILE"
```

### 3. Run Validation Script

Primary command:

```bash
bash "$SKILL_DIR/scripts/dockerfile-validate.sh" "$TARGET_DOCKERFILE"
```

Optional captured run for structured reporting:

```bash
bash "$SKILL_DIR/scripts/dockerfile-validate.sh" "$TARGET_DOCKERFILE" | tee /tmp/dockerfile-validator.out
```

### 4. Classify Findings by Severity (Standard)

Use this standard severity model:

- `Critical`
  - Hardcoded secrets/credentials
  - Explicit root runtime with high-risk context
  - High-impact security policy failures
- `High`
  - Checkov failures for container hardening
  - hadolint errors likely to cause insecure/unreliable builds
  - Missing or unsafe runtime-user posture (`USER`)
- `Medium`
  - `:latest` image tags, missing pinning, cache-cleanup misses
  - Build cache inefficiency and layered install anti-patterns
- `Low`
  - Style/info guidance and non-blocking optimization suggestions

### 5. No-Issue Fast Path (Required)

If validation has no actionable findings:
- Return a concise pass summary.
- Do **not** open reference files.
- Do **not** generate fix diffs.

Use fast path when all are true:
- Script reports overall pass.
- No security failures.
- No error/warning findings requiring user action.

### 6. Reference Loading Rules (Only When Findings Exist)

Only read references that match actual findings. Read each required file once.

Issue-to-reference mapping:

| Issue category | Trigger examples | Read this file |
|---|---|---|
| Secrets, root user, exposed sensitive ports, hardening gaps | `CKV_DOCKER_*`, hardcoded token/password, root runtime | `references/security_checklist.md` |
| Image size, layer count, multi-stage opportunities, cache efficiency, `.dockerignore` gaps | too many `RUN`, single-stage with build deps, cache misses | `references/optimization_guide.md` |
| Tag pinning, instruction usage, COPY vs ADD, WORKDIR/CMD/ENTRYPOINT conventions | `:latest`, unpinned packages, instruction-level best practices | `references/docker_best_practices.md` |

Explicit read commands:

```bash
sed -n '1,220p' "$SKILL_DIR/references/security_checklist.md"
sed -n '1,220p' "$SKILL_DIR/references/optimization_guide.md"
sed -n '1,220p' "$SKILL_DIR/references/docker_best_practices.md"
```

For targeted extraction:

```bash
rg -n "USER|secrets|EXPOSE|HEALTHCHECK" "$SKILL_DIR/references/security_checklist.md"
rg -n "multi-stage|cache|layer|dockerignore" "$SKILL_DIR/references/optimization_guide.md"
rg -n "FROM|COPY|ADD|WORKDIR|CMD|ENTRYPOINT|latest" "$SKILL_DIR/references/docker_best_practices.md"
```

### 7. Produce Standard Report Output

Use this template for every non-fast-path run:

```markdown
## Dockerfile Validation Report
- Target: <path>
- Command: `bash <skill-script> <target>`
- Overall result: PASS | FAIL | PARTIAL (fallback)

### Critical
- <issue or `None`>

### High
- <issue or `None`>

### Medium
- <issue or `None`>

### Low
- <issue or `None`>

### Recommended Fixes
- <specific code-level fix per actionable issue>

### References Used
- <list only files actually read>

### Fallbacks Used
- `None` or exact fallback branch + reason
```

### 8. Offer Fix Application

After reporting:
- Ask whether to apply fixes.
- If user approves, patch the Dockerfile and rerun validation.

## Fallback Behavior (Explicit)

When the primary script cannot complete, use deterministic fallback branches and report them.

### Fallback A: Python/Tool Install Constraint

Condition:
- Script exits with tool-install failure (for example Python missing, package install blocked, or restricted environment).

Action:
1. Report primary failure and why.
2. Run manual minimum checks:

```bash
# Basic syntax signal (if Docker is available)
DOCKERFILE_DIR="$(dirname "$TARGET_DOCKERFILE")"
docker build --no-cache -f "$TARGET_DOCKERFILE" "$DOCKERFILE_DIR"

# High-value static checks
grep -nEi "^[[:space:]]*FROM[[:space:]]+.*:latest" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*(ENV|ARG)[[:space:]].*(password|secret|token|api[_-]?key)[[:space:]]*=" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*USER[[:space:]]+(root|0(:0)?)$" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*HEALTHCHECK[[:space:]]+" "$TARGET_DOCKERFILE" || true
```

3. Classify output with `PARTIAL` result and clearly label skipped checks.

### Fallback B: hadolint Not Available but Docker Available

Use hadolint container image:

```bash
docker run --rm -i hadolint/hadolint < "$TARGET_DOCKERFILE"
```

### Fallback C: No Docker, No hadolint/checkov

Run only manual regex-based checks (Fallback A step 2), clearly mark as `PARTIAL`, and state which scanners were skipped.

## Quick Command Set

### Validate one Dockerfile

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/dockerfile-validate.sh Dockerfile
```

### Validate alternate file

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/dockerfile-validate.sh Dockerfile.prod
```

### Validate skill examples

```bash
cd /path/to/repo/devops-skills-plugin/skills/dockerfile-validator
bash scripts/dockerfile-validate.sh examples/good-example.Dockerfile
bash scripts/dockerfile-validate.sh examples/security-issues.Dockerfile
```

### Run regression checks (CI entrypoint)

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/test_validate.sh
```

Optional strict mode for CI environments that must enforce ShellCheck:

```bash
STRICT_SHELLCHECK=true bash devops-skills-plugin/skills/dockerfile-validator/scripts/test_validate.sh
```

## Progressive Disclosure Rules

- Always read the target Dockerfile first.
- Do not read any reference files unless findings require them.
- Read only the matching reference file(s) from the issue-to-reference mapping.
- Do not reread the same reference unless new issue categories appear.

## Done Criteria

Consider this skill execution complete only when all conditions below are satisfied:

- Trigger matched a Dockerfile validation/lint/security/optimization request.
- Target Dockerfile path was explicitly verified.
- Validation command (or explicit fallback) was executed.
- Findings were reported using severity buckets (`Critical`, `High`, `Medium`, `Low`).
- Reference usage matched issue categories and was explicitly listed.
- No-issue fast path skipped unnecessary reference reads.
- If fixes were applied, validation was rerun and final status reported.

## Resources

- Script: `scripts/dockerfile-validate.sh`
- CI/regression entrypoint: `scripts/test_validate.sh`
- Security reference: `references/security_checklist.md`
- Optimization reference: `references/optimization_guide.md`
- Best-practices reference: `references/docker_best_practices.md`
- Examples: `examples/good-example.Dockerfile`, `examples/bad-example.Dockerfile`, `examples/security-issues.Dockerfile`, `examples/python-optimized.Dockerfile`, `examples/golang-distroless.Dockerfile`

## Source Links

- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Checkov Dockerfile Scanning](https://www.checkov.io/7.Scan%20Examples/Dockerfile.html)
- [hadolint](https://github.com/hadolint/hadolint)

---

## Reference: Docker_Best_Practices

# Docker Best Practices Reference

This document summarizes official Docker best practices based on current recommendations from Docker documentation and industry standards.

## General Principles

### 1. Create Ephemeral Containers
- Containers should be as stateless and ephemeral as possible
- Should be able to stop, destroy, and recreate with minimal setup
- Align with Twelve-Factor App methodology

### 2. Understand Build Context
- Use `.dockerignore` to exclude unnecessary files
- Keep context size minimal for faster builds
- Don't include secrets or sensitive data in context

### 3. Use Multi-Stage Builds
- Separate build dependencies from runtime
- Dramatically reduce final image size
- Improve security by minimizing attack surface

### 4. One Concern Per Container
- Each container should address a single concern
- Makes containers more reusable and easier to scale
- Simplifies debugging and updates

## Dockerfile Instructions Best Practices

### FROM

**Use specific tags, not :latest**
```dockerfile
# Bad
FROM node:latest

# Good
FROM node:21-alpine

# Better
FROM node:21-alpine@sha256:abc123...
```

**Choose minimal base images**
- Alpine Linux: ~5 MB base (vs ~80 MB for Ubuntu)
- Distroless: No shell, package manager (minimal attack surface)
- Scratch: Absolutely minimal (for static binaries)

**Prefer official images**
- Look for "Official Image" or "Verified Publisher" badges
- Official images are maintained and regularly updated

### RUN

**Chain commands to reduce layers**
```dockerfile
# Bad - creates 4 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN curl -sL https://example.com/script.sh | bash

# Good - creates 1 layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sL https://example.com/script.sh | bash
```

**Clean up in same layer**
```dockerfile
# Package manager cache must be removed in same RUN
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# For Alpine
RUN apk add --no-cache package1 package2
```

**Use --no-install-recommends for apt**
```dockerfile
RUN apt-get install -y --no-install-recommends package
```

**Pin package versions**
```dockerfile
# For apt
RUN apt-get install -y package=1.2.3-1

# For apk
RUN apk add package=1.2.3-r0

# For pip
RUN pip install package==1.2.3
```

**Sort multi-line arguments**
```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*
```

**Use pipefail for pipes**
```dockerfile
RUN set -o pipefail && wget -O - https://example.com | wc -l > /number
```

### COPY vs ADD

**Prefer COPY over ADD**
```dockerfile
# Use COPY for files and directories
COPY app.py /app/

# Only use ADD for auto-extraction or remote URLs
ADD https://example.com/file.tar.gz /tmp/
```

**Use COPY --chown to avoid extra layer**
```dockerfile
# Bad - creates extra layer
COPY app.py /app/
RUN chown user:user /app/app.py

# Good - single layer
COPY --chown=user:user app.py /app/
```

### WORKDIR

**Use absolute paths**
```dockerfile
# Bad
WORKDIR app

# Good
WORKDIR /app
```

**Don't use RUN cd**
```dockerfile
# Bad
RUN cd /app && npm install

# Good
WORKDIR /app
RUN npm install
```

### USER

**Don't run as root**
```dockerfile
# Create user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Or for Alpine
RUN addgroup -g 1001 -S appuser && adduser -S appuser -u 1001

# Switch to user
USER appuser
```

**Use high UID (>10000) for better security**
```dockerfile
RUN useradd -u 10001 -m appuser
USER appuser
```

### CMD and ENTRYPOINT

**Use exec form for proper signal handling**
```dockerfile
# Bad - shell form (doesn't handle signals)
CMD python app.py

# Good - exec form
CMD ["python", "app.py"]
```

**Combine ENTRYPOINT and CMD**
```dockerfile
# ENTRYPOINT defines the executable
ENTRYPOINT ["python"]

# CMD provides default arguments (can be overridden)
CMD ["app.py"]
```

### EXPOSE

**Document ports even though it doesn't publish**
```dockerfile
EXPOSE 8080
EXPOSE 443
```

### HEALTHCHECK

**Add health checks for services**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

### LABEL

**Add metadata**
```dockerfile
LABEL org.opencontainers.image.authors="team@example.com"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="Application description"
```

## Build Optimization

### Layer Caching

**Order instructions from least to most frequently changing**
```dockerfile
# 1. Base image (rarely changes)
FROM node:21-alpine

# 2. System packages (rarely change)
RUN apk add --no-cache curl

# 3. Dependencies (change occasionally)
COPY package*.json ./
RUN npm ci

# 4. Source code (changes frequently)
COPY . .
```

### Multi-Stage Builds

**Separate build and runtime**
```dockerfile
# Build stage
FROM node:21 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Runtime stage
FROM node:21-alpine
COPY --from=builder /app/dist /app
CMD ["node", "/app/index.js"]
```

### BuildKit Features

**Enable modern features**
```dockerfile
# syntax=docker/dockerfile:1

# Use cache mounts
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Use secret mounts (secrets not in final image)
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://bucket/file .
```

## Security Best Practices

### 1. Scan Images
```bash
docker scan myimage:tag
# or
trivy image myimage:tag
```

### 2. Use Minimal Base Images
- Fewer packages = fewer vulnerabilities
- Alpine, distroless, or scratch

### 3. Don't Store Secrets in Images
```dockerfile
# Bad
ENV DATABASE_PASSWORD=secret123

# Good - use runtime config or secrets
# Pass at runtime: docker run -e DATABASE_PASSWORD=...
```

### 4. Run as Non-Root
```dockerfile
USER appuser
```

### 5. Use Read-Only Filesystem
```bash
docker run --read-only myimage
```

### 6. Limit Capabilities
```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myimage
```

## Common Anti-Patterns

### ❌ Using :latest tag
- Unpredictable
- Not reproducible
- Can break without warning

### ❌ Not cleaning package cache
```dockerfile
# Missing cleanup increases image by hundreds of MB
RUN apt-get update && apt-get install -y package
# Missing: && rm -rf /var/lib/apt/lists/*
```

### ❌ Running as root
- Security risk
- Violates principle of least privilege

### ❌ Installing unnecessary packages
```dockerfile
# Bloated image
RUN apt-get install -y vim nano emacs curl wget
```

### ❌ Using ADD instead of COPY
- ADD has implicit behavior
- Can extract archives unexpectedly

### ❌ Multiple FROM in non-multi-stage context
- Creates confusion
- Use multi-stage builds properly

## Resources

- [Official Docker Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

## Reference: Optimization_Guide

# Dockerfile Optimization Guide

Comprehensive guide for optimizing Docker images for size, build time, and runtime performance.

## Image Size Optimization

### 1. Choose Minimal Base Images

**Size Comparison:**
```
ubuntu:22.04          ~80 MB
alpine:3.21           ~5 MB
distroless/base       ~20 MB
scratch               ~0 MB (empty)
```

**When to use each:**

**Alpine** - General purpose minimal Linux
```dockerfile
FROM alpine:3.21
RUN apk add --no-cache python3
```
- ✅ Very small (5 MB)
- ✅ Has package manager
- ✅ Good for interpreted languages
- ⚠️  Uses musl libc (compatibility issues with some C libraries)

**Distroless** - Production containers
```dockerfile
FROM gcr.io/distroless/python3
COPY --from=builder /app /app
```
- ✅ No shell, package manager (secure)
- ✅ Minimal attack surface
- ✅ Small size
- ⚠️  Cannot exec into container for debugging
- ⚠️  Must use multi-stage builds

**Scratch** - Static binaries only
```dockerfile
FROM scratch
COPY --from=builder /app/binary /
```
- ✅ Absolutely minimal
- ✅ Perfect for Go, Rust static binaries
- ⚠️  No OS utilities
- ⚠️  No debug capabilities

### 2. Multi-Stage Builds

**Problem: Build tools bloat production images**

**Single-stage (bloated):**
```dockerfile
FROM golang:1.21
WORKDIR /app
COPY . .
RUN go build -o server
CMD ["./server"]

# Result: ~1 GB (includes Go toolchain)
```

**Multi-stage (optimized):**
```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o server

# Production stage
FROM alpine:3.21
COPY --from=builder /app/server /server
CMD ["/server"]

# Result: ~10 MB (100x smaller!)
```

### 3. Layer Optimization

**Combine RUN commands:**

```dockerfile
# Bad - 4 layers, poor caching
RUN apt-get update
RUN apt-get install -y curl
RUN curl -O https://example.com/file
RUN rm -f file

# Good - 1 layer, cache cleaned
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -O https://example.com/file \
    && rm -rf /var/lib/apt/lists/*
```

### 4. Package Manager Cache Cleanup

**APT (Debian/Ubuntu):**
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```
- Saves ~100-200 MB per layer
- Must be in same RUN command

**APK (Alpine):**
```dockerfile
RUN apk add --no-cache package1 package2
```
- Doesn't create cache at all
- Or: `apk add package && rm -rf /var/cache/apk/*`

**YUM/DNF (RHEL/Fedora):**
```dockerfile
RUN yum install -y package \
    && yum clean all \
    && rm -rf /var/cache/yum
```

**Pip (Python):**
```dockerfile
RUN pip install --no-cache-dir package
```

**NPM (Node.js):**
```dockerfile
RUN npm ci --only=production
# Or with cache mount:
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

### 5. Use .dockerignore

**Problem: Entire project copied into image**

```
.dockerignore contents:
.git/
node_modules/
*.log
.env
tests/
docs/
README.md
```

**Impact:**
- Faster builds (smaller context)
- Smaller images (fewer files)
- Prevents accidental secret leaks

## Build Time Optimization

### 1. Leverage Build Cache

**Order matters - least to most frequently changing:**

```dockerfile
# 1. Base image (rarely changes)
FROM node:21-alpine

# 2. System dependencies (rarely change)
RUN apk add --no-cache curl

# 3. Application dependencies (change occasionally)
COPY package*.json ./
RUN npm ci

# 4. Application code (changes frequently)
COPY . .
RUN npm run build
```

**Why this works:**
- Docker caches each layer
- Layers rebuild when files change
- Putting frequently-changing files last preserves cache for earlier layers

### 2. BuildKit Cache Mounts

**Enable BuildKit:**
```bash
export DOCKER_BUILDKIT=1
```

**Use cache mounts:**
```dockerfile
# syntax=docker/dockerfile:1

# Python with pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Node.js with npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go with module cache
RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o app
```

**Benefits:**
- Persistent cache across builds
- Dramatically faster dependency installation
- Shared cache between projects

### 3. Parallel Multi-Stage Builds

```dockerfile
# These stages run in parallel
FROM alpine AS fetch-1
RUN wget https://example.com/file1

FROM alpine AS fetch-2
RUN wget https://example.com/file2

# This stage waits for both
FROM alpine
COPY --from=fetch-1 /file1 .
COPY --from=fetch-2 /file2 .
```

## Runtime Performance Optimization

### 1. Exec Form for CMD/ENTRYPOINT

```dockerfile
# Bad - shell form (extra shell process)
CMD python app.py

# Good - exec form (direct execution)
CMD ["python", "app.py"]
```

**Benefits:**
- Faster startup (no shell)
- Proper signal handling (SIGTERM)
- Lower memory usage

### 2. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD curl -f http://localhost:8080/health || exit 1
```

**Benefits:**
- Container orchestrators can detect unhealthy containers
- Automatic restarts
- Better uptime

### 3. Resource Awareness

```dockerfile
# Use all available CPUs
ENV GOMAXPROCS=0

# Or limit to specific count
ENV GOMAXPROCS=4
```

## Language-Specific Optimizations

### Node.js

```dockerfile
FROM node:21-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:21-alpine
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "server.js"]
```

**Tips:**
- Use `npm ci` instead of `npm install`
- Install only production dependencies
- Use Alpine variant (node:21-alpine vs node:21 = 150MB vs 900MB)

### Python

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
USER nobody
CMD ["python", "app.py"]
```

**Tips:**
- Use slim variant (python:3.12-slim vs python:3.12 = 50MB vs 1GB)
- Install to --user to copy to final stage
- Use --no-cache-dir to avoid pip cache

### Go

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app

FROM scratch
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

**Tips:**
- Use scratch for static binaries
- Disable CGO for static linking
- Use `-ldflags="-s -w"` to strip debug info (smaller binary)

### Java

```dockerfile
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package

FROM eclipse-temurin:21-jre-alpine
COPY --from=builder /app/target/*.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
```

**Tips:**
- Use JRE instead of JDK for runtime (smaller)
- Download dependencies separately for caching
- Consider custom JRE with jlink for minimal image

## Advanced Techniques

### 1. Multi-Architecture Builds

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .
```

### 2. Build Secrets

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
docker build --secret id=npmrc,src=$HOME/.npmrc .
```

**Benefits:**
- Secrets not in final image
- Not in build history
- Secure credential usage

### 3. SSH Mounts

```dockerfile
RUN --mount=type=ssh \
    git clone git@github.com:private/repo.git
```

```bash
docker build --ssh default .
```

### 4. Layer Squashing

```bash
docker build --squash -t myapp .
```

**Benefits:**
- Single layer in final image
- Smaller size if cleanup commands are separate

**Drawbacks:**
- Loses layer caching benefits
- Slower rebuilds

## Optimization Checklist

- [ ] Use minimal base image (Alpine, distroless, scratch)
- [ ] Implement multi-stage builds
- [ ] Combine RUN commands
- [ ] Clean package manager cache
- [ ] Order layers by change frequency
- [ ] Use BuildKit cache mounts
- [ ] Create .dockerignore file
- [ ] Use exec form for CMD/ENTRYPOINT
- [ ] Add HEALTHCHECK for services
- [ ] Pin dependency versions
- [ ] Remove development dependencies
- [ ] Use --no-install-recommends for apt
- [ ] Consider language-specific optimizations
- [ ] Enable BuildKit features

## Measuring Optimization

### Before Optimization
```bash
docker images myapp
# REPOSITORY   TAG       SIZE
# myapp        latest    1.2GB
```

### After Optimization
```bash
docker images myapp-optimized
# REPOSITORY        TAG       SIZE
# myapp-optimized   latest    50MB
```

### Build Time Comparison
```bash
time docker build -t myapp .
# real    5m30s

time docker build -t myapp-optimized .
# real    0m45s (with cache)
```

## Tools for Analysis

### dive - Layer Analysis
```bash
dive myapp:latest
```
- Shows layer-by-layer size
- Identifies wasted space
- Suggests optimizations

### docker history
```bash
docker history myapp:latest
```
- Shows each layer's size
- Identifies large layers

### docker scout
```bash
docker scout cves myapp:latest
```
- Scans for vulnerabilities
- Recommends base image updates

## Resources

- [Docker Best Practices](https://docs.docker.com/build/building/best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [dive - Layer Explorer](https://github.com/wagoodman/dive)

---

## Reference: Security_Checklist

# Container Security Checklist

A comprehensive security checklist for Dockerfiles and container images.

## Build-Time Security

### Base Image Security

- [ ] Use official or verified base images
- [ ] Pin base image to specific tag (not :latest)
- [ ] Consider digest pinning for critical applications
- [ ] Prefer minimal base images (Alpine, distroless, scratch)
- [ ] Scan base images for known vulnerabilities
- [ ] Keep base images updated regularly

### Secrets Management

- [ ] Never hardcode secrets in Dockerfile
- [ ] Don't use ENV or ARG for sensitive data
- [ ] Use Docker build secrets (--secret flag)
- [ ] Use runtime configuration for secrets
- [ ] Scan for accidentally committed secrets
- [ ] Use .dockerignore to exclude secret files

### Package Management

- [ ] Pin package versions for reproducibility
- [ ] Only install necessary packages (--no-install-recommends)
- [ ] Clean package manager cache in same layer
- [ ] Verify package signatures when possible
- [ ] Use official package repositories
- [ ] Audit dependencies for known vulnerabilities

### User and Permissions

- [ ] Create and use non-root user
- [ ] Set USER directive before CMD/ENTRYPOINT
- [ ] Use high UID (>10000) for better isolation
- [ ] Set proper file ownership with COPY --chown
- [ ] Don't use sudo in containers
- [ ] Avoid privileged operations

### Layer and File Security

- [ ] Use .dockerignore to exclude sensitive files
- [ ] Don't copy unnecessary files (use specific COPY)
- [ ] Remove secrets after use in same layer
- [ ] Don't log sensitive information
- [ ] Minimize number of layers
- [ ] Use multi-stage builds to exclude build secrets

## Common Vulnerabilities

### SSH/Remote Access

- [ ] Don't install or expose SSH (port 22)
- [ ] Don't install telnet, FTP, or other insecure protocols
- [ ] Use `docker exec` for debugging instead of SSH
- [ ] Don't run sshd in containers

### Network Exposure

- [ ] Only EXPOSE necessary ports
- [ ] Don't bind to 0.0.0.0 in development images
- [ ] Use internal networks for inter-container communication
- [ ] Implement proper firewall rules
- [ ] Use TLS for network communications

### File System Security

- [ ] Consider read-only root filesystem
- [ ] Use tmpfs for temporary files
- [ ] Set proper file permissions
- [ ] Don't store secrets in environment variables
- [ ] Use volume mounts for sensitive data

## Runtime Security

### Container Configuration

- [ ] Run with --read-only flag when possible
- [ ] Drop unnecessary capabilities (--cap-drop)
- [ ] Use security profiles (AppArmor, SELinux)
- [ ] Set resource limits (CPU, memory)
- [ ] Use user namespaces
- [ ] Enable content trust (DOCKER_CONTENT_TRUST)

### Health and Monitoring

- [ ] Implement HEALTHCHECK in Dockerfile
- [ ] Monitor container logs
- [ ] Set up security scanning in CI/CD
- [ ] Use runtime security tools
- [ ] Monitor for anomalous behavior
- [ ] Implement proper logging without secrets

### Network Security

- [ ] Use custom bridge networks
- [ ] Implement network segmentation
- [ ] Use encrypted overlays for swarm
- [ ] Configure DNS properly
- [ ] Use service mesh for microservices
- [ ] Implement network policies

## Image Registry Security

### Registry Configuration

- [ ] Use private registries for internal images
- [ ] Enable image scanning in registry
- [ ] Implement access controls
- [ ] Use image signing (Docker Content Trust)
- [ ] Scan for vulnerabilities before pull
- [ ] Regularly update registry software

### Image Distribution

- [ ] Sign images before distribution
- [ ] Verify image signatures on pull
- [ ] Use TLS for registry communication
- [ ] Implement role-based access control
- [ ] Audit image pull/push events
- [ ] Use image provenance metadata

## Security Scanning Tools

### Static Analysis
- **hadolint** - Dockerfile linting
- **Checkov** - Policy-as-code scanning
- **dockerfilelint** - Best practices checker

### Vulnerability Scanning
- **Trivy** - Comprehensive vulnerability scanner
- **Snyk** - Dependency vulnerability scanner
- **Clair** - Container vulnerability analysis
- **Anchore** - Deep image inspection

### Runtime Security
- **Falco** - Runtime threat detection
- **Aqua Security** - Container security platform
- **Sysdig** - Container monitoring and security

## Compliance and Standards

### Industry Standards

- [ ] Follow CIS Docker Benchmark
- [ ] Comply with NIST guidelines
- [ ] Adhere to OWASP Container Security
- [ ] Meet PCI DSS requirements (if applicable)
- [ ] Follow SOC 2 controls (if applicable)

### Security Policies

- [ ] Document security requirements
- [ ] Implement security review process
- [ ] Define incident response procedures
- [ ] Regular security audits
- [ ] Security training for developers
- [ ] Maintain security documentation

## Quick Security Wins

### Easy Fixes

1. **Use specific base image tags**
   ```dockerfile
   FROM alpine:3.21  # Not alpine:latest
   ```

2. **Run as non-root**
   ```dockerfile
   USER appuser
   ```

3. **Clean package cache**
   ```dockerfile
   RUN apk add --no-cache package
   ```

4. **Don't expose unnecessary ports**
   ```dockerfile
   # Only expose what's needed
   EXPOSE 8080
   ```

5. **Add health checks**
   ```dockerfile
   HEALTHCHECK CMD curl -f http://localhost/ || exit 1
   ```

## Security Checklist Summary

| Category | Critical | High | Medium |
|----------|----------|------|--------|
| Base Image | Use official, pin version | Scan for CVEs | Update regularly |
| Secrets | Never in code | Use secrets mgmt | Scan commits |
| Users | Run as non-root | High UID | Proper permissions |
| Network | TLS only | Minimal exposure | Firewall rules |
| Runtime | Drop capabilities | Read-only FS | Resource limits |

## Resources

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [NIST Container Security Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
