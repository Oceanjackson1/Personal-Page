---
title: "Spec Miner"
description: "Reverse-engineering specialist that extracts specifications from existing codebases. Use when working with legacy or undocumented systems, inherited projects, or old codebases with no documentation. Invoke to map code dependencies, generate API do..."
category: "writing"
source: "community"
author: "Community"
tags: ["spec", "miner"]
date: 2026-03-20
---

# Spec Miner

Reverse-engineering specialist who extracts specifications from existing codebases.

## Role Definition

You operate with two perspectives: **Arch Hat** for system architecture and data flows, and **QA Hat** for observable behaviors and edge cases.

## When to Use This Skill

- Understanding legacy or undocumented systems
- Creating documentation for existing code
- Onboarding to a new codebase
- Planning enhancements to existing features
- Extracting requirements from implementation

## Core Workflow

1. **Scope** - Identify analysis boundaries (full system or specific feature)
2. **Explore** - Map structure using Glob, Grep, Read tools
   - _Validation checkpoint:_ Confirm sufficient file coverage before proceeding. If key entry points, configuration files, or core modules remain unread, continue exploration before writing documentation.
3. **Trace** - Follow data flows and request paths
4. **Document** - Write observed requirements in EARS format
5. **Flag** - Mark areas needing clarification

### Example Exploration Patterns

```
# Find entry points and public interfaces
Glob('**/*.py', exclude=['**/test*', '**/__pycache__/**'])

# Locate technical debt markers
Grep('TODO|FIXME|HACK|XXX', include='*.py')

# Discover configuration and environment usage
Grep('os\.environ|config\[|settings\.', include='*.py')

# Map API route definitions (Flask/Django/Express examples)
Grep('@app\.route|@router\.|router\.get|router\.post', include='*.py')
```

### EARS Format Quick Reference

EARS (Easy Approach to Requirements Syntax) structures observed behavior as:

| Type | Pattern | Example |
|------|---------|---------|
| Ubiquitous | The `<system>` shall `<action>`. | The API shall return JSON responses. |
| Event-driven | When `<trigger>`, the `<system>` shall `<action>`. | When a request lacks an auth token, the system shall return HTTP 401. |
| State-driven | While `<state>`, the `<system>` shall `<action>`. | While in maintenance mode, the system shall reject all write operations. |
| Optional | Where `<feature>` is supported, the `<system>` shall `<action>`. | Where caching is enabled, the system shall store responses for 60 seconds. |

> See `references/ears-format.md` for the complete EARS reference.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Analysis Process | `references/analysis-process.md` | Starting exploration, Glob/Grep patterns |
| EARS Format | `references/ears-format.md` | Writing observed requirements |
| Specification Template | `references/specification-template.md` | Creating final specification document |
| Analysis Checklist | `references/analysis-checklist.md` | Ensuring thorough analysis |

## Constraints

### MUST DO
- Ground all observations in actual code evidence
- Use Read, Grep, Glob extensively to explore
- Distinguish between observed facts and inferences
- Document uncertainties in dedicated section
- Include code locations for each observation

### MUST NOT DO
- Make assumptions without code evidence
- Skip security pattern analysis
- Ignore error handling patterns
- Generate spec without thorough exploration

## Output Templates

Save specification as: `specs/{project_name}_reverse_spec.md`

Include:
1. Technology stack and architecture
2. Module/directory structure
3. Observed requirements (EARS format)
4. Non-functional observations
5. Inferred acceptance criteria
6. Uncertainties and questions
7. Recommendations

---

## Reference: Analysis Checklist

# Analysis Checklist

## Comprehensive Checklist

| Area | What to Find | Glob/Grep Patterns |
|------|--------------|-------------------|
| **Entry points** | main.ts, app.ts, index.ts | `**/main.{ts,js,py}` |
| **Routes** | Controllers, route files | `**/routes/**/*`, `@Controller` |
| **Models** | Entities, schemas | `**/models/**/*`, `@Entity` |
| **Auth** | Guards, middleware, JWT | `**/auth/**/*`, `passport` |
| **Validation** | DTOs, validators, pipes | `**/dto/**/*`, `@IsString` |
| **Error handling** | Exception filters, try/catch | `ExceptionFilter`, `catch` |
| **External calls** | HTTP clients, SDK usage | `fetch(`, `axios.` |
| **Config** | Env files, config modules | `**/.env*`, `ConfigService` |
| **Tests** | Test files reveal behaviors | `**/*.spec.ts`, `**/*.test.ts` |
| **Background jobs** | Queues, cron, workers | `@Cron`, `Bull`, `Queue` |

## Analysis Phases

### Phase 1: Structure Discovery
- [ ] Identify technology stack
- [ ] Map directory structure
- [ ] Find entry points
- [ ] List all modules/packages

### Phase 2: API Surface
- [ ] Document all endpoints
- [ ] Note HTTP methods and paths
- [ ] Identify request/response formats
- [ ] Find authentication requirements

### Phase 3: Data Layer
- [ ] Map all data models
- [ ] Document relationships
- [ ] Find migrations
- [ ] Note validation rules

### Phase 4: Business Logic
- [ ] Trace main flows
- [ ] Identify business rules
- [ ] Document state transitions
- [ ] Find external integrations

### Phase 5: Security
- [ ] Check authentication method
- [ ] Review authorization patterns
- [ ] Find input validation
- [ ] Note security configurations

### Phase 6: Quality & Testing
- [ ] Review existing tests
- [ ] Note test coverage
- [ ] Document error handling
- [ ] Find logging patterns

## Verification Questions

Before finalizing specification:

- [ ] All endpoints documented?
- [ ] All models mapped?
- [ ] Authentication flow clear?
- [ ] Error responses documented?
- [ ] External dependencies listed?
- [ ] Uncertainties flagged?

---

## Reference: Analysis Process

# Analysis Process

## Step 1: Project Structure

```bash
# Find entry points
Glob: **/main.{ts,js,py,go}
Glob: **/app.{ts,js,py}
Glob: **/index.{ts,js}

# Find routes/controllers
Glob: **/routes/**/*.{ts,js}
Glob: **/controllers/**/*.{ts,js}
Grep: @Controller|@Get|@Post|router\.|app\.get
```

## Step 2: Data Models

```bash
# Database schemas
Glob: **/models/**/*.{ts,js,py}
Glob: **/schema*.{ts,js,py,sql}
Glob: **/migrations/**/*
Grep: @Entity|class.*Model|schema\s*=
```

## Step 3: Business Logic

```bash
# Services and logic
Glob: **/services/**/*.{ts,js}
Grep: async.*function|export.*class
```

## Step 4: Authentication & Security

```bash
# Auth patterns
Glob: **/auth/**/*
Glob: **/guards/**/*
Grep: @Guard|middleware|passport|jwt
```

## Step 5: External Integrations

```bash
# External calls
Grep: fetch\(|axios\.|HttpService|request\(
Glob: **/integrations/**/*
Glob: **/clients/**/*
```

## Step 6: Configuration

```bash
# Config files
Glob: **/*.config.{ts,js}
Glob: **/.env*
Glob: **/config/**/*
```

## Quick Reference

| Pattern | Purpose |
|---------|---------|
| `**/main.{ts,js,py}` | Entry points |
| `**/routes/**/*` | API routes |
| `**/models/**/*` | Data models |
| `@Controller\|@Get` | NestJS patterns |
| `router.\|app.get` | Express patterns |

---

## Reference: Ears Format

# EARS Format

## EARS Syntax

Easy Approach to Requirements Syntax for clear, unambiguous requirements.

### Basic Patterns

**Ubiquitous (Always)**
```
The system shall [action].
```

**Event-Driven**
```
When [trigger], the system shall [action].
```

**State-Driven**
```
While [state], the system shall [action].
```

**Conditional**
```
While [state], when [trigger], the system shall [action].
```

**Optional**
```
Where [feature enabled], the system shall [action].
```

## Example Observations

### Authentication

**OBS-AUTH-001: Login Flow**
```
While credentials are valid, when POST /auth/login is called,
the system shall return JWT access token (15m) and refresh token (7d).
```

**OBS-AUTH-002: Token Refresh**
```
While refresh token is valid, when POST /auth/refresh is called,
the system shall issue new access token.
```

**OBS-AUTH-003: Invalid Token**
```
When expired or invalid token is provided,
the system shall return 401 Unauthorized.
```

### User Management

**OBS-USER-001: User Creation**
```
While email is unique, when POST /users is called with valid data,
the system shall create user with bcrypt-hashed password (rounds=12).
```

**OBS-USER-002: Email Validation**
```
When email format is invalid,
the system shall return 400 with error message "Invalid email format".
```

### Input Validation

**OBS-INPUT-001: Required Fields**
```
When required fields are missing,
the system shall return 400 with field-specific error messages.
```

## Quick Reference

| Type | Pattern | Example Trigger |
|------|---------|-----------------|
| Ubiquitous | shall [action] | Always true |
| Event | When [X], shall | On button click |
| State | While [X], shall | While logged in |
| Conditional | While [X], when [Y], shall | While admin, when delete |
| Optional | Where [X], shall | If feature enabled |

---

## Reference: Specification Template

# Specification Template

## Full Template

```markdown
# Reverse-Engineered Specification: [System/Feature Name]

## Overview
[High-level description based on analysis]

## Architecture Summary

### Technology Stack
- **Language**: TypeScript 5.x
- **Framework**: NestJS 10.x
- **Database**: PostgreSQL 15
- **ORM**: Prisma 5.x

### Module Structure
```
src/
├── auth/         # Authentication (JWT, guards)
├── users/        # User CRUD operations
├── orders/       # Order processing
└── common/       # Shared utilities
```

### Data Flow
```
Request → Guard → Controller → Service → Repository → Database
                                     ↓
                              External APIs
```

## Observed Functional Requirements

### [Module Name]

**OBS-XXX-001**: [Feature Name]
[EARS format requirement]

**OBS-XXX-002**: [Feature Name]
[EARS format requirement]

## Observed Non-Functional Requirements

### Security
- JWT tokens signed with RS256
- Passwords hashed with bcrypt (12 rounds)
- Rate limiting: 100 req/min per IP

### Performance
- Database connection pool: 10 connections
- Response timeout: 30 seconds
- Pagination: default 20, max 100

### Error Handling
| Code | Condition | Response |
|------|-----------|----------|
| 400 | Validation failure | `{ error: string, details: object }` |
| 401 | Invalid/missing token | `{ error: "Unauthorized" }` |
| 404 | Resource not found | `{ error: "Not found" }` |
| 500 | Unhandled error | `{ error: "Internal server error" }` |

## Inferred Acceptance Criteria

### AC-001: [Feature]
Given [precondition]
When [action]
Then [expected result]

## Uncertainties and Questions

- [ ] What triggers order status transitions?
- [ ] Is soft delete implemented for users?
- [ ] What external APIs are called?
- [ ] Are there background jobs?

## Recommendations

1. Add OpenAPI documentation to controllers
2. Missing input validation on PATCH endpoints
3. Consider adding request tracing
```

## Output Location

Save specification as: `specs/{project_name}_reverse_spec.md`

## Required Sections

| Section | Purpose |
|---------|---------|
| Overview | High-level summary |
| Architecture | Tech stack, structure, data flow |
| Functional Requirements | EARS format observations |
| Non-Functional | Security, performance, errors |
| Acceptance Criteria | Given/When/Then format |
| Uncertainties | Questions for clarification |
| Recommendations | Improvements identified |
