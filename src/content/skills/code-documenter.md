---
title: "Code Documenter"
description: "Expert documentation generator for coding projects. Analyzes codebases to create thorough, comprehensive documentation for developers and users. Supports incremental updates, multi-audience documentation, architecture decision records, and documen..."
category: "writing"
source: "community"
author: "Community"
tags: ["code", "documenter"]
date: 2026-03-20
---

# Code Documenter Skill

An intelligent documentation system that analyzes codebases and generates
thorough, comprehensive documentation tailored to your project type and audience
needs.

## Core Philosophy

**Documentation serves readers, not authors.** Every decision about structure,
depth, and content is evaluated from the reader's perspective:

- Will this help them understand?
- Will this help them succeed?
- Will this answer their questions?
- Does this earn its place?

**Comprehensive without overwhelm.** Thorough coverage of what matters, ruthless
cutting of what doesn't. The goal is complete, accurate, useful
documentation—not exhaustive documentation of every line of code.

**Documentation as code artifact.** Docs should be versioned, tested, and
maintained with the same rigor as code. They're not afterthoughts; they're
essential.

## When to Use This Skill

**Primary use cases:**

- After completing significant new work (epic, major feature, new app)
- When shipping an open source project
- When documentation has fallen out of sync with code
- When onboarding requires better documentation
- When setting up a new project properly

**Not for:**

- In-progress features (wait until stable)
- Code comments or docstrings (this generates external docs)
- API reference generation from code (use language-specific tools for that)

## Session Flow

### Mode Selection

The skill operates in two modes:

| Mode                   | When to Use                                     | Behavior                                          |
| ---------------------- | ----------------------------------------------- | ------------------------------------------------- |
| **Quick Mode**         | Incremental updates after new features          | Autonomous, fast, focused on what changed         |
| **Comprehensive Mode** | New projects, major overhauls, first-time setup | Collaborative, thorough, quality gates throughout |

**The skill will ask:** "Quick update or comprehensive documentation?"

### Phase 1: Multi-Agent Project Analysis

The skill deploys specialized analysis agents to understand your project:

```
Analysis Phase:
├─ Agent 1: Project Structure
│  └─ Scanning file tree, identifying project type, tech stack
├─ Agent 2: Code Surface Analysis
│  └─ Finding APIs, components, commands, exports
├─ Agent 3: Dependency Analysis
│  └─ Reviewing packages, frameworks, key dependencies
├─ Agent 4: Git History Analysis
│  └─ Analyzing commits since last doc update
├─ Agent 5: Existing Documentation Review
│  └─ Reading current docs, assessing state
└─ Synthesis: Generating documentation plan...
```

**Quick Mode:** Focused analysis on what changed since last update  
**Comprehensive Mode:** Full analysis of entire project

Each agent reports findings in structured format. You see everything happening.

### Phase 2: Documentation State Assessment

The skill compares code state vs. documentation state:

**If manifest exists (`.doc-state.json`):**

- Loads documentation state from last run
- Compares current code vs. last documented state
- Identifies what's changed (added/modified/removed)
- Shows you the documentation debt

**If no manifest:**

- First time documenting this project
- Will create fresh manifest after completion

**Key metrics shown:**

- **Health Score:** Current documentation health (0-100)
- **Coverage:** What % of public surface is documented
- **Freshness:** How current are docs vs. code
- **Debt:** What needs attention (prioritized)

### Phase 3: Audience & Scope Discovery

The skill asks:

1. **"Who needs these docs?"**
   - Developers only
   - Users only
   - Both developers and users

2. **"What depth of documentation?"**
   - **Standard:** Right-sized coverage (4,000-7,000 words)
   - **Deep:** Comprehensive with internals (8,000-12,000 words)

**Quick Mode:** Uses stored preferences from manifest  
**Comprehensive Mode:** Asks explicitly, shows examples

### Phase 4: Documentation Boundaries

The skill proposes what should be documented:

```
Based on my analysis of your Express + PostgreSQL API:

PUBLIC SURFACE (Always Document)
├─ 12 API endpoints in /routes
├─ Database schema (3 tables)
├─ 14 environment variables
└─ Authentication flow

INTERNAL IMPLEMENTATION (Recommended for Deep)
├─ 6 middleware functions
├─ Error handling patterns
└─ Database migration strategy

INFRASTRUCTURE (Essential for all levels)
├─ Docker setup
├─ CI/CD pipeline
└─ Deployment process

EXCLUDED (Recommend skip)
├─ Test files (obvious from names)
├─ Build scripts (standard tooling)
└─ Internal helpers (<10 lines each)

Adjust these boundaries? [approve/modify]
```

You approve or adjust before documentation generation begins.

### Phase 5: Documentation Plan Presentation

The skill presents a complete plan:

```
DOCUMENTATION PLAN

Structure:
└─ /docs
   ├─ developers/
   │  ├─ api.md (API endpoint reference)
   │  ├─ architecture.md (System design + diagrams)
   │  ├─ contributing.md (How to contribute)
   │  ├─ deployment.md (Deploy & operate)
   │  ├─ troubleshooting.md (Common issues)
   │  ├─ examples/ (12 runnable examples)
   │  └─ adr/ (4 architecture decisions)
   ├─ users/
   │  ├─ getting-started.md (Quick start guide)
   │  ├─ features.md (Feature overview)
   │  ├─ troubleshooting.md (User-facing issues)
   │  └─ examples/ (5 user examples)
   ├─ CHANGELOG.md (Documentation change log)
   └─ documentation-map.md (Navigation guide)

Files to update:
- README.md (complete rewrite, progressive disclosure)
- docs/developers/api.md (2 new endpoints, 1 modified)
- docs/CHANGELOG.md (new entry)

Files to create:
- docs/adr/004-caching-strategy.md (new decision)
- docs/developers/examples/pagination.js (new example)

Files to remove:
- docs/developers/legacy-auth.md (endpoint removed)

Estimated scope: ~5,200 words total
Target health score: 92/100

Proceed? [yes/adjust scope/abort]
```

**Comprehensive Mode:** Review and approve before generation  
**Quick Mode:** Brief preview, option to review or proceed

### Phase 6: Documentation Generation

#### Comprehensive Mode (with Quality Gates)

The skill works through documentation in phases, pausing for review:

**Gate 1: Core Documentation** (README + Getting Started)

- Generates README with progressive disclosure
- Creates getting started guides
- **Quality Check:** Does this hook and onboard effectively?
- **You review and approve or request changes**

**Gate 2: Reference Documentation** (API/Commands/Components)

- Generates reference documentation
- Creates working examples
- **Quality Check:** Is everything covered? Examples clear?
- **You review and approve or request changes**

**Gate 3: Architecture & Decisions**

- Documents architecture with Mermaid diagrams
- Creates ADRs for key decisions
- **Quality Check:** Does this explain the WHY?
- **You review and approve or request changes**

**Gate 4: Supporting Documentation**

- Generates troubleshooting guides
- Creates contributing guidelines
- Documentation map for navigation
- **Quality Check:** Complete and helpful?
- **You review and approve or request changes**

**Gate 5: Polish & Verification**

- Generates test scripts for examples
- Creates link validation script
- Runs accessibility check
- Final health score calculation
- **Final review**

#### Quick Mode (Autonomous)

The skill executes the plan efficiently:

- Updates only changed sections
- Preserves manual edits in unchanged areas
- Generates new content as needed
- Updates manifest and changelog
- Reports final results

### Phase 7: Session Completion

The skill produces:

**Files Created/Updated:**

- All documentation files as planned
- `.doc-state.json` (updated manifest)
- `docs/CHANGELOG.md` (new entry)
- Test and validation scripts

**Documentation Health Report:**

```
DOCUMENTATION HEALTH REPORT

Overall Health Score: 92/100 (↑ from 78)

Component Scores:
├─ Coverage Health: 95/100 (↑ from 82)
│  └─ 97% of public surface documented
├─ Freshness Health: 98/100 (↑ from 65)
│  └─ All docs current as of commit a3f2b1c
├─ Quality Health: 88/100 (↑ from 81)
│  └─ 12 examples, 4 ADRs, troubleshooting complete
└─ Consistency Health: 90/100 (↑ from 84)
   └─ Tone consistent, terminology standardized

Debt Status:
├─ Critical: 0 items (was 2)
├─ Important: 1 item (was 4)
└─ Minor: 3 items (unchanged)

Next session recommendations:
- Document the new webhook system (flagged as potential)
- Add performance troubleshooting section
- Consider hosting docs on GitHub Pages
```

**Session Notes:**

- Decisions made
- Scope adjustments
- What was included/excluded and why
- Next steps

## File Outputs

### Core Documentation Structure

**Developer-only projects:**

```
/docs
├── CHANGELOG.md
├── api.md / commands.md / components.md
├── architecture.md
├── contributing.md
├── deployment.md
├── troubleshooting.md
├── examples/
│   ├── example-1.js
│   ├── example-2.js
│   └── test-examples.sh
├── adr/
│   ├── 001-initial-decisions.md
│   ├── 002-database-choice.md
│   └── ...
└── scripts/
    ├── validate-links.sh
    └── accessibility-check.md
```

**Multi-audience projects:**

```
/docs
├── CHANGELOG.md
├── documentation-map.md
├── users/
│   ├── getting-started.md
│   ├── features.md
│   ├── troubleshooting.md
│   └── examples/
│       ├── basic-usage.js
│       └── advanced-usage.js
├── developers/
│   ├── api.md / architecture.md
│   ├── contributing.md
│   ├── deployment.md
│   ├── troubleshooting.md
│   ├── examples/
│   │   ├── integration.js
│   │   ├── extending.js
│   │   └── test-examples.sh
│   └── adr/
│       ├── 001-framework-choice.md
│       └── ...
└── scripts/
    ├── validate-links.sh
    └── accessibility-check.md
```

### Documentation Manifest (`.doc-state.json`)

Tracks complete documentation state:

```json
{
  "version": "1.0",
  "project": {
    "name": "my-api",
    "type": "express-api",
    "lastScanned": "2025-01-10T14:30:00Z",
    "gitCommit": "a3f2b1c"
  },
  "preferences": {
    "audiences": ["developers", "users"],
    "depthLevel": "standard",
    "tone": "professional"
  },
  "healthScore": {
    "overall": 92,
    "components": {
      "coverage": 95,
      "freshness": 98,
      "quality": 88,
      "consistency": 90
    },
    "trend": [78, 85, 92]
  },
  "coverage": {
    "endpoints": { "total": 12, "documented": 12, "changed": 0 },
    "components": { "total": 8, "documented": 8, "changed": 0 },
    "schemas": { "total": 3, "documented": 3, "changed": 0 }
  },
  "debt": {
    "critical": [],
    "important": [
      {
        "item": "Document webhook system",
        "effort": "medium",
        "status": "to-fix"
      }
    ],
    "minor": [
      {
        "item": "Add performance troubleshooting",
        "effort": "low",
        "status": "accepted"
      }
    ]
  },
  "documentationMap": {
    "README.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["overview", "quickstart"],
      "wordCount": 850
    },
    "docs/developers/api.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["endpoints"],
      "wordCount": 2400
    }
  }
}
```

## Collaboration Behaviors

### In Comprehensive Mode

**Proactive contributions:**

- "I notice you're using Redis but there's no ADR explaining why—should I
  document that decision?"
- "Your error handling is sophisticated. This deserves explanation in
  architecture docs."
- "The authentication flow is non-standard. Users will have questions—let me
  address them."

**Challenge assumptions:**

- "You said 'standard depth' but you have 47 endpoints. That needs Deep
  documentation."
- "This 'getting started' guide assumes too much. Your users won't know X."
- "Three examples aren't enough here. The concept is complex."

**Surface insights:**

- "Your git history shows you refactored auth 3 times. That's an ADR waiting to
  be written."
- "These three files handle all business logic but aren't documented at all.
  Gap."
- "You have inline JSDoc but it contradicts what's in the markdown docs.
  Consistency issue."

### In Quick Mode

**Efficient execution:**

- "Updating 3 files based on changes in commit a3f2b1c..."
- "2 new endpoints detected, adding to api.md..."
- "Removed documentation for deleted legacy-auth endpoint..."

**Flag concerns:**

- "Warning: Manual changes detected in architecture.md, preserving your edits"
- "Note: Health score dropped from 92 to 85 due to new undocumented features"

## Quality Standards

The skill maintains high documentation quality through:

### Clarity

- Concepts explained before they're used
- Technical terms defined on first use
- Examples precede or immediately follow concepts
- Progressive disclosure (simple → complex)

### Completeness

- Every public-facing element documented
- Edge cases and gotchas addressed
- Troubleshooting for predictable failures
- Examples for common use cases

### Accuracy

- All facts verified against code
- Examples tested and working
- Links validated
- No outdated information

### Accessibility

- Diagrams include alt text
- Links have descriptive text
- Heading hierarchy is logical
- Code snippets have language labels

### Consistency

- Terminology used uniformly
- Tone maintained throughout
- Formatting standardized
- Structure predictable

## Special Features

### Architecture Decision Records (ADRs)

Captures WHY decisions were made:

The skill identifies decision points through:

- Major dependency additions (git history)
- Non-standard architectural patterns (code analysis)
- Framework/library choices
- Flagged commits with "decision" language
- Your explicit identification

Each ADR documents:

- Context (what was the situation?)
- Decision (what did we decide?)
- Rationale (why this choice?)
- Consequences (trade-offs accepted)
- Alternatives considered

### Living, Tested Examples

Examples are runnable code in `/examples`:

- Actually work (not pseudocode)
- Cover common use cases
- Include test script to verify they run
- Referenced from documentation
- Maintained as code evolves

### Troubleshooting Database

Two flavors:

- **User troubleshooting:** Common errors, how to fix them
- **Developer troubleshooting:** Debugging guides, edge cases, gotchas

The skill seeds initial content in Comprehensive Mode, grows it in Quick Mode as
you add real troubleshooting content.

### Documentation Map

For large projects, a navigation guide:

- Different learning paths (beginner/advanced)
- How docs connect to each other
- What to read when
- Visual/textual navigation aid

### Mermaid Diagrams

The skill generates code-based diagrams:

- Architecture diagrams
- Sequence diagrams
- Entity-relationship diagrams
- State diagrams
- Flowcharts

All version-controllable, all render in GitHub.

### Documentation Hosting Integration

Detects if you're using:

- GitHub Pages
- ReadTheDocs
- GitBook
- MkDocs

Generates appropriate config files and optimizes structure for static site
generation.

## Reference Documents

Load contextually when needed:

- **`references/project-types-guide.md`** — How to document different project
  types
- **`references/documentation-patterns.md`** — Common documentation patterns and
  structures
- **`references/quality-standards.md`** — Detailed quality criteria and examples
- **`references/manifest-spec.md`** — Technical specification for
  `.doc-state.json`
- **`references/depth-levels-guide.md`** — Standard vs. Deep explained with
  examples
- **`references/health-score-formula.md`** — How health score is calculated
- **`references/adr-guide.md`** — Writing effective Architecture Decision
  Records

## Templates

Available in `templates/`:

- **`README-template.md`** — Progressive disclosure README structure
- **`api-docs-template.md`** — API endpoint documentation
- **`component-docs-template.md`** — Component/module documentation
- **`troubleshooting-template.md`** — Troubleshooting guide structure
- **`contributing-template.md`** — Contributing guidelines
- **`documentation-map-template.md`** — Navigation guide template

## Success Criteria

Documentation is complete when:

✓ Health score ≥ 85  
✓ All critical and important debt resolved  
✓ Examples run without errors  
✓ Links validate successfully  
✓ Accessibility check passes  
✓ Tone is consistent throughout  
✓ You're confident someone could use your project from the docs alone

## Key Reminders

- **Reader-first always:** Every decision serves the reader
- **Git-aware:** Smart incremental updates, not regeneration
- **Transparency:** You see all analysis and decisions
- **Preserve quality:** Don't overwrite good manual edits
- **Test examples:** Generate test scripts for working code
- **Track health:** Health score trends over time
- **Prioritize debt:** Not all debt is equal
- **Comprehensive without exhaustive:** Document what matters

---

## Reference: Adr Guide

# Architecture Decision Records (ADR) Guide

How to identify, write, and organize Architecture Decision Records.

## What is an ADR?

An Architecture Decision Record documents a significant architectural or design
decision, capturing:

- **What** was decided
- **Why** it was decided
- **What alternatives** were considered
- **What consequences** (trade-offs) were accepted

ADRs answer the question: **"Why did we build it this way?"**

## When to Create an ADR

### Clear Signals

**Create an ADR when:**

- ✅ Choosing a framework or major library
- ✅ Selecting a database or data store
- ✅ Deciding on authentication/authorization approach
- ✅ Adopting a significant architectural pattern
- ✅ Making a decision that's hard to reverse
- ✅ Choosing between multiple viable approaches
- ✅ Accepting a significant trade-off

**Examples:**

- "Why Express instead of Fastify?"
- "Why PostgreSQL instead of MongoDB?"
- "Why JWT tokens instead of sessions?"
- "Why microservices instead of monolith?"
- "Why GraphQL instead of REST?"

### Don't Create an ADR For

**Not worth documenting:**

- ❌ Obvious, industry-standard choices
- ❌ Trivial decisions easily reversed
- ❌ Personal coding preferences
- ❌ Temporary workarounds
- ❌ Decisions with only one viable option

**Examples of what NOT to document:**

- "Why JavaScript for a Node.js project?" (obvious)
- "Why we use const instead of var?" (coding style, not architecture)
- "Why we use npm instead of yarn?" (preference, easily reversible)

## ADR Structure

### Standard Template

```markdown
# ADR [number]: [Short title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]  
**Date:** YYYY-MM-DD  
**Deciders:** [Who made this decision]  
**Technical Story:** [Issue/PR/ticket reference, if any]

## Context

[What is the situation forcing this decision?] [What is the current state?]
[What problems are we trying to solve?]

## Decision

[What did we decide to do?] [Be specific and clear.]

## Rationale

[Why did we choose this option?] [What makes this the best choice given our
context?] [What benefits does this provide?]

## Consequences

### Positive

[What improves?] [What becomes possible?] [What gets easier?]

### Negative

[What trade-offs are we accepting?] [What becomes harder?] [What are we giving
up?]

### Neutral

[Other changes that aren't clearly positive or negative]

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [What is this alternative?]

**Pros:**

- [Benefit 1]
- [Benefit 2]

**Cons:**

- [Drawback 1]
- [Drawback 2]

**Why not chosen:** [Specific reason]

### Alternative 2: [Name]

[Repeat structure]

## References

[Links to documentation, discussions, benchmarks, etc.]
```

---

## Real Examples

### Example 1: Database Choice

```markdown
# ADR 001: Use PostgreSQL for Primary Database

**Status:** Accepted  
**Date:** 2025-01-05  
**Deciders:** Engineering team  
**Technical Story:** Issue #23

## Context

We need to choose a database for our multi-tenant SaaS application. The system
needs to:

- Store structured user data and relationships
- Support complex queries across tenant data
- Handle transactions for billing operations
- Scale to thousands of tenants
- Provide strong consistency for financial data

## Decision

We will use PostgreSQL 14+ as our primary database.

## Rationale

PostgreSQL provides:

1. **ACID transactions:** Critical for billing and payment operations
2. **Rich query capabilities:** Complex JOINs and aggregations for analytics
3. **Row-level security:** Native multi-tenancy support
4. **JSON support:** Flexible schema for tenant-specific data
5. **Mature ecosystem:** Well-understood, excellent tooling
6. **Battle-tested:** Proven at scale in similar applications

## Consequences

### Positive

- Strong consistency guarantees for financial data
- Rich querying eliminates need for separate analytics database
- Native multi-tenancy features simplify tenant isolation
- Extensive PostgreSQL expertise in team

### Negative

- Higher operational complexity than managed NoSQL
- Scaling horizontally requires careful sharding strategy
- Must manage schema migrations across tenants
- Connection pooling required for high concurrency

### Neutral

- Need to set up replication for high availability
- Backup strategy required (but we'd need this anyway)

## Alternatives Considered

### Alternative 1: MongoDB

**Pros:**

- Easy horizontal scaling
- Flexible schema per tenant
- Simpler sharding

**Cons:**

- Weaker consistency model risky for financial data
- More complex transactions
- Team less familiar with MongoDB

**Why not chosen:** Financial data requires strong consistency. MongoDB's
eventual consistency model adds complexity and risk we're unwilling to accept.

### Alternative 2: MySQL

**Pros:**

- Similar benefits to PostgreSQL
- Slightly simpler operations
- Large community

**Cons:**

- Inferior JSON support
- No row-level security
- Less powerful query optimizer

**Why not chosen:** PostgreSQL's row-level security and JSON support are
valuable for multi-tenancy. Small operational simplicity gain doesn't outweigh
these features.

## References

- [PostgreSQL Multi-tenancy Guide](https://example.com/pg-multitenancy)
- [Benchmark: Postgres vs MySQL vs MongoDB](https://example.com/benchmark)
- Team discussion thread: [Slack link]
```

---

### Example 2: Authentication Approach

```markdown
# ADR 002: JWT Tokens with Refresh Token Rotation

**Status:** Accepted  
**Date:** 2025-01-08  
**Deciders:** Security team, Backend team

## Context

We need an authentication system for our REST API that will:

- Support web and mobile clients
- Work across multiple API servers (load balanced)
- Enable single sign-out across devices
- Maintain security against token theft
- Scale horizontally without session state

Current state: No authentication implemented yet.

## Decision

We will use JWT access tokens (15-minute expiry) with refresh tokens (30-day
expiry) and refresh token rotation.

**Flow:**

1. Login returns both access token and refresh token
2. Access token used for API requests
3. When access token expires, client uses refresh token to get new pair
4. Old refresh token is invalidated (rotation)
5. Refresh tokens stored in database for revocation

## Rationale

This approach provides:

1. **Stateless API servers:** Access tokens contain all needed info, no session
   lookup
2. **Short-lived access tokens:** Limits damage from stolen tokens
3. **Refresh token rotation:** Detects token theft (reuse of invalidated token)
4. **Single sign-out:** Revoke refresh tokens to force re-login
5. **Mobile-friendly:** Long-lived refresh tokens avoid constant logins

## Consequences

### Positive

- API servers are fully stateless
- Easy horizontal scaling
- Good security vs. usability balance
- Works well for mobile apps

### Negative

- Requires database lookup for refresh operation
- More complex than simple session cookies
- Client must handle token refresh logic
- Refresh token storage adds database load

### Neutral

- Need background job to clean up expired refresh tokens
- Must handle refresh token rotation carefully

## Alternatives Considered

### Alternative 1: Session Cookies

**Pros:**

- Simpler to implement
- Server controls all state
- Easy to revoke sessions

**Cons:**

- Requires session store (Redis)
- CSRF protection needed
- Harder to use from mobile apps
- Doesn't work well with load balancing

**Why not chosen:** Need to support mobile apps first-class, and session cookies
are awkward for native mobile. Also want stateless API servers.

### Alternative 2: JWTs without Refresh Tokens

**Pros:**

- Simplest implementation
- Fully stateless

**Cons:**

- Must choose between long-lived tokens (security risk) or short-lived (bad UX)
- No way to revoke tokens before expiry
- Cannot implement single sign-out

**Why not chosen:** No token revocation is a security dealbreaker. We need
ability to force logout.

### Alternative 3: OAuth 2.0 with External Provider

**Pros:**

- Don't manage passwords ourselves
- Mature, well-tested
- Users can use existing accounts

**Cons:**

- Adds dependency on third-party
- More complex integration
- Less control over authentication flow

**Why not chosen:** For MVP, want to control entire auth flow. May add social
login later as alternative, but need native auth first.

## References

- [JWT Best Practices](https://example.com/jwt-best-practices)
- [Refresh Token Rotation Explained](https://example.com/refresh-rotation)
- [OWASP Auth Cheatsheet](https://owasp.org/cheatsheets/auth)
```

---

## How the Skill Identifies ADR Opportunities

The skill looks for:

### 1. Git History Analysis

- Commits adding major dependencies
- Large refactors or restructuring
- Framework migrations
- Breaking changes

**Example signals:**

```
feat: migrate from REST to GraphQL
feat: add Redis for session storage
refactor: switch from MongoDB to PostgreSQL
```

### 2. Code Pattern Analysis

- Non-standard architectural patterns
- Unusual technology combinations
- Custom solutions instead of libraries

**Example signals:**

- Custom authentication instead of Passport.js
- Manual connection pooling instead of library
- Unusual folder structure

### 3. Technology Choices

- Database selection
- Framework choice
- State management approach
- Deployment strategy

### 4. Configuration Analysis

- Complex configuration files
- Environment-specific settings
- Feature flags

### 5. User Input

The skill asks:

- "I noticed you added Redis. Should we document why?"
- "Your auth approach is custom. Is there an ADR for this decision?"

---

## ADR Numbering and Organization

### File Naming

```
/docs/adr/
├── 001-use-postgresql.md
├── 002-jwt-authentication.md
├── 003-microservices-architecture.md
├── 004-graphql-api.md
└── README.md (index of all ADRs)
```

**Format:** `[number]-[short-title].md`

- Zero-padded numbers (001, 002, etc.)
- Lowercase, hyphen-separated
- Descriptive but concise

### ADR Index

Create an index (`/docs/adr/README.md`):

```markdown
# Architecture Decision Records

## Active Decisions

- [ADR 001: Use PostgreSQL](./001-use-postgresql.md) - 2025-01-05
- [ADR 002: JWT Authentication](./002-jwt-authentication.md) - 2025-01-08
- [ADR 003: Microservices Architecture](./003-microservices-architecture.md) -
  2025-01-10

## Superseded Decisions

- [ADR 000: Use MongoDB](./000-use-mongodb.md) - Superseded by ADR 001

## Proposed (Not Yet Decided)

- [ADR 004: GraphQL API](./004-graphql-api.md) - Under discussion
```

---

## ADR Lifecycle

### Status Values

| Status         | Meaning                              |
| -------------- | ------------------------------------ |
| **Proposed**   | Under consideration, not yet decided |
| **Accepted**   | Decision made and implemented        |
| **Deprecated** | Still in use but we plan to change   |
| **Superseded** | Replaced by a newer decision         |

### Evolution Example

**Initial decision:**

```markdown
# ADR 001: Use MongoDB

**Status:** Accepted  
**Date:** 2024-06-15
```

**Later deprecated:**

```markdown
# ADR 001: Use MongoDB

**Status:** Deprecated  
**Date:** 2024-06-15  
**Deprecated:** 2025-01-05  
**Superseded by:** ADR 005

## Deprecation Note

This decision was superseded by ADR 005 (Switch to PostgreSQL) due to need for
stronger consistency guarantees.
```

**New decision:**

```markdown
# ADR 005: Migrate to PostgreSQL

**Status:** Accepted  
**Date:** 2025-01-05  
**Supersedes:** ADR 001

## Context

After 6 months with MongoDB, we discovered that... [Explains why original
decision didn't work out]
```

---

## ADR Quality Checklist

Good ADRs have:

- [ ] Clear, specific decision stated
- [ ] Context explains situation/problem
- [ ] Rationale explains WHY this choice
- [ ] Consequences honestly assessed (positive AND negative)
- [ ] At least 2 alternatives considered
- [ ] Each alternative has pros/cons listed
- [ ] Clear reason why alternatives weren't chosen
- [ ] References to supporting materials

Poor ADRs are:

- ❌ Just "we chose X" with no context
- ❌ No alternatives mentioned
- ❌ Only positive consequences listed
- ❌ Vague or generic reasoning
- ❌ No specific decision (just philosophy)

---

## Common ADR Topics

### Technology Choices

- Programming language
- Framework
- Database
- Message queue
- Cache layer
- Search engine

### Architecture Patterns

- Monolith vs. microservices
- Event-driven vs. request/response
- Server-side rendering vs. client-side
- Serverless vs. traditional deployment

### Security & Auth

- Authentication approach
- Authorization model
- Secrets management
- Encryption strategy

### Data & State

- Data modeling approach
- State management (frontend)
- Caching strategy
- Session management

### Operations

- Deployment strategy
- Monitoring approach
- Logging system
- Backup strategy

### Development Process

- Branching strategy
- Code review process
- Testing approach
- CI/CD pipeline

---

## Tips for Writing ADRs

### Do:

✅ Write ADRs soon after decision (while fresh) ✅ Be honest about trade-offs ✅
Include enough context for newcomers ✅ Link to supporting materials ✅ Keep it
concise (1-2 pages typically)

### Don't:

❌ Write ADRs for every tiny decision ❌ Hide or minimize downsides ❌ Write in
overly technical jargon ❌ Make it a design document (keep focused) ❌ Let them
get out of sync with reality

---

## ADR Value

**For current team:**

- Capture reasoning before it's forgotten
- Avoid relitigating settled decisions
- Understand trade-offs when issues arise

**For new team members:**

- Quick understanding of "why we build it this way"
- Learn from past decisions
- Avoid suggesting already-rejected alternatives

**For future you:**

- Remember why you made this choice
- Understand what you were optimizing for
- Know what trade-offs were acceptable

---

## When to Update ADRs

**Never change the decision section** - ADRs are historical records.

**Do add:**

- Deprecation notes when decision changes
- "Update YYYY-MM-DD" sections with learnings
- References to newer ADRs

**Example:**

```markdown
# ADR 002: JWT Authentication

**Status:** Accepted  
**Date:** 2025-01-08

[Original content...]

## Update: 2025-06-15

After 6 months in production, we've learned:

- 15-minute token expiry is too short for mobile, causing poor UX
- Increased to 1-hour based on user feedback
- No security incidents related to longer expiry
```

---

## Reference: Depth Levels Guide

# Documentation Depth Levels

Guide to choosing between **Standard** and **Deep** documentation depth.

## Overview

The skill offers two documentation depth levels:

| Level        | Word Count   | Coverage                      | Use When                           |
| ------------ | ------------ | ----------------------------- | ---------------------------------- |
| **Standard** | 4,000-7,000  | Public surface + essentials   | Most projects, balanced coverage   |
| **Deep**     | 8,000-12,000 | Public + internals + advanced | Complex projects, teaching-focused |

## Standard Depth

### What's Included

✅ **Core Documentation:**

- README with quick start
- Installation guide
- API/CLI/Component reference
- Basic architecture overview
- Common use cases with examples
- Troubleshooting for frequent issues
- Contributing guide (for open source)

✅ **Coverage:**

- All public APIs documented
- Key configuration options
- Main user flows
- Common error scenarios

✅ **Examples:**

- 1-2 examples per major feature
- Basic usage patterns
- Common configurations

**NOT included:**

- Internal implementation details
- Advanced edge cases
- Performance tuning deep dives
- Extensive architectural rationale

### Ideal For

- **Most web APIs:** Document endpoints, not internal middleware details
- **CLIs with <20 commands:** Full command reference, standard examples
- **Libraries with focused API:** Document public surface well
- **Internal tools:** Enough for team to use effectively
- **MVP/Early stage:** Sufficient for initial users

### Example: Standard REST API Docs

```
README.md (~800 words)
├─ Quick start
├─ What is this?
└─ Links to full docs

/docs/developers/
├─ api.md (~2,500 words)
│  ├─ Authentication
│  ├─ Endpoints (grouped by resource)
│  ├─ Request/response examples
│  └─ Error codes
├─ architecture.md (~1,200 words)
│  ├─ High-level system diagram
│  ├─ Database schema overview
│  └─ Key technologies
├─ deployment.md (~800 words)
│  ├─ Docker deployment
│  ├─ Environment variables
│  └─ Basic troubleshooting
├─ contributing.md (~500 words)
└─ examples/ (5-7 working examples)

Total: ~6,000 words
```

---

## Deep Depth

### What's Included

✅ **Everything from Standard, plus:**

- Internal architecture deep dive
- Design pattern explanations
- Performance considerations
- Advanced use cases
- Extensive troubleshooting
- Multiple ADRs (Architecture Decision Records)
- Migration guides
- Testing strategies
- Security considerations

✅ **Coverage:**

- Public APIs fully documented
- Internal implementation patterns explained
- Edge cases and gotchas
- Performance characteristics
- Advanced configuration

✅ **Examples:**

- 3-5 examples per major feature
- Progressive examples (basic → advanced)
- Real-world scenarios
- Anti-pattern warnings

**Includes:**

- Why decisions were made (ADRs)
- How things work internally
- When to use advanced features
- Performance tuning guides

### Ideal For

- **Complex systems:** Microservices, distributed systems
- **Teaching/learning resources:** Need to explain "why" deeply
- **Framework/library:** Users need to understand internals to extend
- **Enterprise software:** Teams need deep knowledge
- **Open source with contributors:** Help people contribute effectively

### Example: Deep REST API Docs

```
README.md (~1,000 words)
├─ Comprehensive quick start
├─ What/why/who
└─ Full navigation

/docs/developers/
├─ api.md (~3,500 words)
│  ├─ Authentication (with flow diagrams)
│  ├─ All endpoints with details
│  ├─ Request/response examples
│  ├─ Error codes with recovery
│  └─ Rate limiting internals
├─ architecture.md (~2,500 words)
│  ├─ System architecture (detailed diagrams)
│  ├─ Request lifecycle
│  ├─ Database design with ERD
│  ├─ Caching strategy
│  └─ Service dependencies
├─ deployment.md (~1,500 words)
│  ├─ Multiple deployment options
│  ├─ Configuration deep dive
│  ├─ Monitoring and logging
│  ├─ Performance tuning
│  └─ Comprehensive troubleshooting
├─ contributing.md (~800 words)
│  ├─ Development setup
│  ├─ Code organization
│  ├─ Testing approach
│  └─ PR workflow
├─ security.md (~1,000 words)
│  ├─ Threat model
│  ├─ Authentication details
│  ├─ Authorization patterns
│  └─ Security best practices
├─ performance.md (~900 words)
│  ├─ Benchmarks
│  ├─ Optimization techniques
│  ├─ Caching strategies
│  └─ Scaling considerations
├─ adr/ (6-10 decision records)
│  ├─ 001-framework-choice.md
│  ├─ 002-database-selection.md
│  ├─ 003-authentication-approach.md
│  └─ ...
└─ examples/ (12-15 working examples)
   ├─ basic/
   ├─ intermediate/
   └─ advanced/

Total: ~11,000 words
```

---

## Comparison by Project Type

### REST API

**Standard:**

- Document all endpoints
- Basic architecture
- Standard deployment
- ~5-7 examples

**Deep:**

- All endpoints with internals
- Request lifecycle explained
- Database design details
- Performance tuning
- Security deep dive
- ~12-15 examples

---

### CLI Tool

**Standard:**

- All commands documented
- Installation for main platforms
- Configuration basics
- ~5-8 examples

**Deep:**

- Commands + internal architecture
- Plugin system explained
- Advanced configuration
- Shell integration details
- Cross-platform nuances
- ~12-15 examples

---

### JavaScript Library

**Standard:**

- Public API documented
- Basic usage patterns
- Installation
- ~5-7 examples

**Deep:**

- Public API + internals
- How the library works
- Extension points
- Advanced patterns
- Bundle size optimization
- Tree-shaking guidance
- ~12-18 examples

---

### Web Application

**Standard:**

- User guide
- Developer setup
- Component overview
- Deployment basics
- ~6-8 examples

**Deep:**

- User guide + internals
- State management explained
- Component architecture
- Performance optimization
- Testing strategies
- Multiple deployment scenarios
- ~15-20 examples

---

## Decision Framework

### Choose **Standard** if:

✓ Your project has:

- Straightforward architecture
- Well-defined public API
- Standard patterns
- Documentation mainly for usage

✓ Your users need to:

- Use the product effectively
- Understand what it does
- Get started quickly
- Troubleshoot common issues

✓ Your goal is:

- Get docs shipped quickly
- Cover the essentials well
- Maintain minimal docs

### Choose **Deep** if:

✓ Your project has:

- Complex architecture
- Non-obvious design decisions
- Novel approaches
- Extension points

✓ Your users need to:

- Understand how it works internally
- Extend or modify the system
- Contribute code
- Optimize performance

✓ Your goal is:

- Comprehensive knowledge transfer
- Enable advanced usage
- Support contributors
- Explain complex decisions

---

## Real-World Examples

### Standard Depth Example

**Project:** Simple REST API for task management

**Documentation includes:**

- Quick start (create task via API)
- All 8 endpoints documented
- Basic architecture (Express + Postgres)
- Docker deployment guide
- 6 examples (CRUD operations)

**What's excluded:**

- How middleware chain works
- Why Postgres over MongoDB (not complex)
- Performance optimization (not needed yet)
- Internal validation logic

**Result:** 5,800 words, covers all user needs

---

### Deep Depth Example

**Project:** Multi-tenant SaaS API platform

**Documentation includes:**

- Everything from Standard, plus:
- How tenant isolation works
- Database sharding explained
- ADR on authentication approach
- ADR on multi-tenancy design
- Performance tuning guide
- Security threat model
- Advanced examples (webhooks, batch operations)
- Testing strategy for multi-tenant code

**Result:** 10,500 words, enables advanced usage and contribution

---

## Transitioning Between Depths

### Starting Standard, Going Deep Later

Common path:

1. **Launch:** Start with Standard depth
2. **Users ask questions:** Identify gaps in understanding
3. **Contributors appear:** Need deeper architecture knowledge
4. **Scale challenges:** Performance docs become important
5. **Upgrade:** Run skill in Deep mode, preserves existing docs

### When to Upgrade

Signals it's time for Deep documentation:

- Contributors struggle to understand codebase
- Same architectural questions asked repeatedly
- Performance optimization needed
- Advanced use cases emerging
- Team growing and onboarding slower

---

## Word Count Targets Explained

### Why Word Counts?

Word counts provide concrete boundaries:

- Forces prioritization
- Prevents endless expansion
- Creates consistency across projects

### Word Count Includes

Counted:

- All prose in documentation files
- Code comments within examples
- Table content
- List items

Not counted:

- Code examples themselves
- Mermaid diagram code
- Markdown formatting

### Flexibility

Targets are guides, not hard limits:

- Simple projects may be under target
- Complex projects may exceed slightly
- Quality matters more than hitting exact count

---

## Choosing Wisely

**Start with Standard** unless you're certain you need Deep.

**Reasons:**

- Faster to produce and maintain
- Sufficient for most projects
- You can always go deeper later
- Over-documentation is burden

**Deep is investment:**

- Takes longer to create
- More to maintain
- Only worth it if users need it
- Better to start lean, expand as needed

**When uncertain:** Ask yourself:

- "Will users need to understand internals?"
- "Is this architecture novel or complex?"
- "Do I expect contributors?"

If all "no" → Standard is probably right.

---

## Reference: Documentation Patterns

# Documentation Patterns

Common patterns for organizing and structuring documentation across all project
types.

## Progressive Disclosure README

The README is the entry point. Structure it like a newspaper: most important
information first, progressive depth.

### Structure

```markdown
# Project Name

One-sentence description of what this does and why it exists.

## Quick Start

[30-second version: install and run]

npm install my-project node index.js

## What is This?

[2-minute explanation]

- What problem does this solve?
- Who is this for?
- What makes it different?

## Installation

[Detailed installation for all platforms]

## Usage

[Core usage patterns with examples]

## Documentation

- [Full documentation](./docs/)
- [API Reference](./docs/api.md)
- [Contributing Guide](./docs/contributing.md)

## License

[License information]
```

### Anti-Patterns to Avoid

❌ **Burying the quick start**

```markdown
# Project

[Long backstory about why project exists] [Detailed technical architecture]
[Finally, 10 paragraphs down: how to install]
```

✅ **Quick start first**

```markdown
# Project

Solves X problem in Y way.

## Quick Start

npm install && npm start
```

❌ **Feature laundry list**

```markdown
Features:

- Feature 1
- Feature 2
- [50 more features]
```

✅ **Headline benefits**

```markdown
- Fast: 10x faster than alternatives
- Simple: 3 lines of code to get started
- Reliable: Used in production by [big names]
```

## API Endpoint Documentation

### Pattern: Per-Endpoint Detail

For each endpoint, document:

````markdown
### GET /api/users/:id

Retrieves a single user by ID.

**Parameters:**

- `id` (path, required): User ID

**Query Parameters:**

- `include` (optional): Related data to include. Options: `posts`, `comments`

**Request Headers:**

- `Authorization`: Bearer token required

**Response:** `200 OK`

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "posts": [...]
}
```
````

**Errors:**

- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User does not exist

**Example:**

```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.example.com/api/users/123?include=posts
```

````

### Pattern: Resource Grouping

Group related endpoints:

```markdown
## Users Resource

### List Users
GET /api/users

### Get User
GET /api/users/:id

### Create User
POST /api/users

### Update User
PATCH /api/users/:id

### Delete User
DELETE /api/users/:id
````

## Command Documentation

### Pattern: Command Reference

````markdown
### myapp deploy

Deploys the application to production.

**Usage:**

```bash
myapp deploy [environment] [options]
```
````

**Arguments:**

- `environment` (optional): Target environment. Default: `production`

**Options:**

- `-f, --force`: Skip confirmation prompts
- `-v, --verbose`: Show detailed output
- `--dry-run`: Show what would be deployed without deploying

**Examples:**

Deploy to production:

```bash
myapp deploy production
```

Deploy to staging with verbose output:

```bash
myapp deploy staging --verbose
```

Dry run:

```bash
myapp deploy --dry-run
```

````

## Component Documentation

### Pattern: Component API

For React/Vue/other components:

```markdown
### UserCard

Displays user information in a card layout.

**Props:**

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| user | User | Yes | - | User object to display |
| showEmail | boolean | No | false | Whether to show email |
| onEdit | function | No | - | Callback when edit clicked |

**Example:**
```jsx
<UserCard
  user={user}
  showEmail={true}
  onEdit={() => console.log('Edit clicked')}
/>
````

**Styling:**

- Accepts `className` prop for custom styling
- CSS variables: `--card-bg`, `--card-border`

**Accessibility:**

- Semantic HTML with proper heading hierarchy
- Keyboard navigation supported
- Screen reader friendly

````

## Architecture Documentation

### Pattern: System Overview

```markdown
# Architecture

## High-Level Design

[Mermaid diagram showing system components]

```mermaid
graph TD
    Client[Web Client] --> API[API Server]
    API --> DB[(PostgreSQL)]
    API --> Cache[Redis Cache]
    API --> Queue[Message Queue]
    Queue --> Worker[Background Worker]
    Worker --> DB
````

## Components

### API Server

- Express.js application
- Handles HTTP requests
- Implements business logic
- Manages authentication

### Database

- PostgreSQL 14
- Stores user data, posts, comments
- See [schema documentation](./schema.md)

### Cache Layer

- Redis for session storage and rate limiting
- 5-minute TTL on frequently accessed data

### Background Worker

- Processes asynchronous tasks
- Email sending, image processing
- Runs on separate server

````

### Pattern: Data Flow

```markdown
## Request Flow: Creating a Post

1. **Client** sends POST to `/api/posts`
2. **API Server** validates request
3. **API Server** checks authentication (Redis session)
4. **API Server** writes to database
5. **API Server** enqueues image processing job
6. **API Server** returns 201 Created
7. **Background Worker** processes images asynchronously
````

## Troubleshooting Documentation

### Pattern: Problem-Solution

```markdown
## Common Issues

### Database Connection Fails

**Symptom:**
```

Error: connect ECONNREFUSED 127.0.0.1:5432

```

**Cause:** PostgreSQL is not running or connection config is incorrect

**Solution:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check connection string in `.env`
3. Ensure database exists: `createdb myapp_dev`

**Related:** See [Database Setup](./database.md)
```

### Pattern: Error Code Reference

```markdown
## Error Codes

### AUTH_001: Invalid Token

**When:** Token validation fails

**Common Causes:**

- Token has expired
- Token format is incorrect
- Token was revoked

**Resolution:**

1. Get a new token via `/api/auth/login`
2. Ensure token is passed in `Authorization` header
3. Check token expiration time

### RATE_001: Rate Limit Exceeded

**When:** Too many requests from same IP

**Common Causes:**

- Burst of requests
- Polling too frequently

**Resolution:**

- Wait for rate limit window to reset (shown in response headers)
- Implement exponential backoff
- Cache responses when possible
```

## Contributing Guide

### Pattern: Getting Started

```markdown
# Contributing

Thanks for your interest in contributing!

## Quick Start

1. Fork and clone
2. Install dependencies: `npm install`
3. Create branch: `git checkout -b my-feature`
4. Make changes
5. Run tests: `npm test`
6. Push and create PR

## Development Setup

### Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Environment Setup

1. Copy `.env.example` to `.env`
2. Update database credentials
3. Run migrations: `npm run migrate`
4. Seed test data: `npm run seed`

## Code Style

We use ESLint and Prettier:

- Run linter: `npm run lint`
- Format code: `npm run format`

## Testing

- Unit tests: `npm run test:unit`
- Integration tests: `npm run test:integration`
- All tests must pass before PR

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers
```

## Installation Documentation

### Pattern: Multi-Platform Installation

````markdown
## Installation

### macOS

```bash
brew install myapp
```
````

### Linux

**Debian/Ubuntu:**

```bash
curl -fsSL https://example.com/install.sh | bash
```

**Arch Linux:**

```bash
yay -S myapp
```

### Windows

**Using npm:**

```bash
npm install -g myapp
```

**Using installer:** Download from
[releases page](https://github.com/user/myapp/releases)

### From Source

```bash
git clone https://github.com/user/myapp.git
cd myapp
npm install
npm run build
npm link
```

### Verify Installation

```bash
myapp --version
```

Should output: `myapp v1.2.3`

````

## Configuration Documentation

### Pattern: Configuration Reference

```markdown
## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| REDIS_URL | No | localhost:6379 | Redis connection string |
| PORT | No | 3000 | Server port |
| LOG_LEVEL | No | info | Logging level (debug, info, warn, error) |

### Config File

Create `config.yml`:

```yaml
server:
  port: 3000
  host: 0.0.0.0

database:
  host: localhost
  port: 5432
  name: myapp

cache:
  enabled: true
  ttl: 300
````

### Config Priority

1. Environment variables (highest priority)
2. Config file
3. Defaults (lowest priority)

**Example:** `PORT` env var overrides `server.port` in config file

````

## Deployment Documentation

### Pattern: Deployment Guide

```markdown
## Deployment

### Prerequisites
- Server with Ubuntu 20.04+
- Docker and Docker Compose
- Domain name pointing to server

### Quick Deploy

1. Clone repository:
```bash
git clone https://github.com/user/myapp.git
cd myapp
````

2. Set environment variables:

```bash
cp .env.example .env
nano .env  # Edit as needed
```

3. Deploy with Docker:

```bash
docker-compose up -d
```

4. Run migrations:

```bash
docker-compose exec api npm run migrate
```

5. Verify:

```bash
curl https://yourdomain.com/health
```

### Production Checklist

- [ ] Set `NODE_ENV=production`
- [ ] Use strong database password
- [ ] Configure SSL/TLS
- [ ] Set up backups
- [ ] Configure monitoring
- [ ] Set up logging

````

## Migration Guide

### Pattern: Version Migration

```markdown
## Migrating from v1 to v2

### Breaking Changes

#### Database Schema
Users table renamed to `accounts`:

**Before (v1):**
```sql
SELECT * FROM users WHERE id = 1;
````

**After (v2):**

```sql
SELECT * FROM accounts WHERE id = 1;
```

#### API Changes

Authentication endpoint changed:

**Before (v1):**

```
POST /auth/login
```

**After (v2):**

```
POST /api/v2/auth/token
```

### Migration Steps

1. **Backup your database**

```bash
pg_dump myapp > backup.sql
```

2. **Update code**

```bash
git pull origin main
npm install
```

3. **Run migrations**

```bash
npm run migrate:v2
```

4. **Update environment variables**

- Add: `API_VERSION=v2`
- Remove: `LEGACY_MODE=true`

5. **Restart application**

```bash
pm2 restart myapp
```

6. **Verify**

```bash
curl https://api.example.com/health
```

### Rollback

If needed:

```bash
git checkout v1.x.x
npm run migrate:down
pm2 restart myapp
```

````

## Cross-References and Linking

### Pattern: Internal Links

```markdown
## Authentication

All API endpoints require authentication. See [Authentication Guide](./auth.md) for details.

### Quick Example

```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.example.com/users
````

For full authentication flow, see [Auth Flow Diagram](./auth.md#flow-diagram).

````

### Pattern: External Links

```markdown
## Dependencies

This project uses:
- [Express.js](https://expressjs.com/) - Web framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Redis](https://redis.io/) - Cache and sessions

See [package.json](../package.json) for full dependency list.
````

## Examples Documentation

### Pattern: Progressive Examples

````markdown
## Examples

### Basic Usage

Simplest possible example:

```javascript
const app = require("myapp");
app.start();
```
````

### Common Pattern

Most users do this:

```javascript
const app = require("myapp");

app.configure({
  port: 3000,
  database: process.env.DATABASE_URL,
});

app.start();
```

### Advanced Usage

For complex scenarios:

```javascript
const app = require("myapp");

app.use(customMiddleware());

app.configure({
  port: 3000,
  database: {
    host: "localhost",
    pool: { min: 2, max: 10 },
  },
  cache: {
    enabled: true,
    strategy: "lru",
  },
});

app.on("ready", () => {
  console.log("App is running");
});

app.start();
```

### Real-World Example

Complete application:

```javascript
// See /examples/complete-app.js for full runnable code
```

````

## Diagrams and Visuals

### Pattern: Mermaid Diagrams

**Sequence Diagram:**
```markdown
```mermaid
sequenceDiagram
    Client->>+API: POST /api/posts
    API->>+Auth: Validate token
    Auth-->>-API: Token valid
    API->>+DB: Insert post
    DB-->>-API: Post created
    API->>Queue: Enqueue processing
    API-->>-Client: 201 Created
    Queue->>Worker: Process images
````

````

**Architecture Diagram:**
```markdown
```mermaid
graph LR
    A[Client] --> B[Load Balancer]
    B --> C[API Server 1]
    B --> D[API Server 2]
    C --> E[(Database)]
    D --> E
    C --> F[Cache]
    D --> F
````

````

**State Diagram:**
```markdown
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review
    Review --> Published
    Review --> Draft: Rejected
    Published --> Archived
    Archived --> [*]
````

```

```

---

## Reference: Health Score Formula

# Documentation Health Score Formula

Detailed explanation of how the documentation health score is calculated.

## Overall Health Score

The overall health score is a weighted average of four component scores:

```
Overall = (Coverage × 0.40) + (Freshness × 0.30) + (Quality × 0.20) + (Consistency × 0.10)
```

**Range:** 0-100  
**Interpretation:**

- 90-100: Excellent
- 80-89: Good
- 70-79: Adequate
- 60-69: Needs improvement
- <60: Poor

## Component Scores

### 1. Coverage Score (40% weight)

**What it measures:** Percentage of public surface area that is documented

**Calculation:**

```
Coverage = (documented_elements / total_public_elements) × 100
```

**Example for REST API:**

```
Documented endpoints: 12
Total endpoints: 12
Documented schemas: 3
Total schemas: 3
Documented error codes: 8
Total error codes: 10

Coverage = ((12 + 3 + 8) / (12 + 3 + 10)) × 100
         = (23 / 25) × 100
         = 92
```

**Adjustments:**

- **Critical elements undocumented:** -10 points per critical gap
  - Critical: Authentication, main API endpoints, installation
- **Examples missing:** -5 points if <50% of features have examples
- **Configuration undocumented:** -10 points if env vars or config missing

**Floor:** 0 (cannot go negative)

---

### 2. Freshness Score (30% weight)

**What it measures:** How current the documentation is relative to code

**Calculation:**

```
freshness_factor = 100 - (staleness_penalty)

staleness_penalty = (critical_stale × 20) + (important_stale × 10) + (minor_stale × 2)
```

**Staleness categories:**

- **Critical stale:** Docs contradict current code, examples don't run
- **Important stale:** New features undocumented, removed features still
  documented
- **Minor stale:** Out-of-date version numbers, old screenshots

**Example:**

```
Critical stale items: 0
Important stale items: 2
Minor stale items: 3

staleness_penalty = (0 × 20) + (2 × 10) + (3 × 2)
                  = 0 + 20 + 6
                  = 26

Freshness = 100 - 26 = 74
```

**Git-based freshness:**

If git is available, additional calculation:

```
commits_since_last_doc = number of commits since .doc-state.json was updated
max_acceptable_commits = 20

git_penalty = (commits_since_last_doc / max_acceptable_commits) × 30

Freshness = max(100 - staleness_penalty - git_penalty, 0)
```

**Example:**

```
Commits since last doc: 15
Max acceptable: 20

git_penalty = (15 / 20) × 30 = 22.5

Total penalty = 26 + 22.5 = 48.5
Freshness = 100 - 48.5 = 51.5
```

**Floor:** 0

---

### 3. Quality Score (20% weight)

**What it measures:** How well-written and useful the documentation is

**Calculation:**

```
Quality = base_quality + bonuses - penalties
```

**Base quality:** 70 (assuming adequate documentation exists)

**Bonuses (max +30):**

- Examples exist: +10
- Working, tested examples: +5
- ADRs present (≥3): +5
- Troubleshooting guide: +5
- Diagrams/visuals: +3
- Progressive examples (basic → advanced): +2

**Penalties:**

- No examples: -20
- Examples don't run: -15
- No troubleshooting: -10
- Jargon without definitions: -5
- Broken links: -5 per broken link (max -15)
- Poor formatting: -5
- No diagrams for complex concepts: -5

**Example:**

```
Base: 70
Has 12 working examples: +15
Has 4 ADRs: +5
Has troubleshooting: +5
Has 3 diagrams: +3
Has progressive examples: +2
Total bonuses: +30

No penalties

Quality = 70 + 30 - 0 = 100
```

**Example with penalties:**

```
Base: 70
Has examples but some don't run: +10 - 10 = 0
No troubleshooting: -10
3 broken links: -15
Total: 70 + 0 - 25 = 45
```

**Floor:** 20  
**Ceiling:** 100

---

### 4. Consistency Score (10% weight)

**What it measures:** Uniformity in style, terminology, and structure

**Calculation:**

```
Consistency = 100 - (inconsistency_penalty)
```

**Inconsistency penalties:**

**Terminology (max -30):**

- Same concept, different terms: -10 per conflict
- Inconsistent capitalization: -5 per conflict
- Example: "user" vs "customer" vs "client" → -10

**Tone (max -30):**

- Mix of formal and casual: -15
- Inconsistent voice (you vs one vs we): -10
- Varying formality across sections: -5

**Structure (max -20):**

- Inconsistent heading hierarchy: -10
- Different formatting for similar content: -5
- Mixed list styles: -5

**Formatting (max -20):**

- Inconsistent code block styling: -10
- Different link formats: -5
- Varying emphasis patterns: -5

**Example:**

```
Terminology issues:
- "API key" vs "access token" used interchangeably: -10

Tone issues:
- Mix of "you should" and "one should": -10

Structure issues:
- None

Formatting issues:
- Some code blocks have language labels, others don't: -10

Total penalty: -30
Consistency = 100 - 30 = 70
```

**Floor:** 0  
**Ceiling:** 100

---

## Complete Example Calculation

### Project State

**Coverage:**

- 12/12 endpoints documented
- 3/3 schemas documented
- 8/10 error codes documented
- No critical gaps

```
Coverage = ((12 + 3 + 8) / (12 + 3 + 10)) × 100
         = 92
```

**Freshness:**

- 0 critical stale items
- 2 important stale items (new endpoints not documented)
- 3 minor stale items (version numbers)
- 5 commits since last doc update

```
staleness_penalty = (0 × 20) + (2 × 10) + (3 × 2) = 26
git_penalty = (5 / 20) × 30 = 7.5
Freshness = 100 - 26 - 7.5 = 66.5 → 67
```

**Quality:**

- Base: 70
- 12 working examples: +15
- 4 ADRs: +5
- Troubleshooting guide: +5
- 3 diagrams: +3
- No penalties

```
Quality = 70 + 28 = 98
```

**Consistency:**

- One terminology inconsistency: -10
- Minor formatting issues: -5

```
Consistency = 100 - 15 = 85
```

**Overall:**

```
Overall = (92 × 0.40) + (67 × 0.30) + (98 × 0.20) + (85 × 0.10)
        = 36.8 + 20.1 + 19.6 + 8.5
        = 85
```

**Result:** Health score of 85 (Good)

---

## Health Score Trending

The manifest tracks the last 10 health scores:

```json
"trend": [65, 72, 78, 85, 85]
```

**Interpretation:**

**Upward trend (65 → 85):**

- ✅ Documentation improving
- ✅ Debt being addressed
- ✅ Quality increasing

**Flat trend (85 → 85):**

- ⚠️ Stable but not improving
- ⚠️ May indicate acceptable plateau
- ⚠️ Or may indicate neglect

**Downward trend (92 → 85):**

- ❌ Quality declining
- ❌ Debt accumulating
- ❌ Freshness degrading
- ❌ Needs attention

---

## Improvement Strategies

### To Improve Coverage (if <85)

1. Identify undocumented elements
2. Prioritize public API documentation
3. Add examples for complex features
4. Document error scenarios

### To Improve Freshness (if <85)

1. Update docs after each feature
2. Remove references to deleted features
3. Test and update examples
4. Address git commit gap

### To Improve Quality (if <85)

1. Add working examples
2. Create ADRs for major decisions
3. Build troubleshooting guide
4. Add diagrams for complex concepts
5. Fix broken links

### To Improve Consistency (if <85)

1. Create terminology glossary
2. Standardize tone throughout
3. Use consistent formatting
4. Apply consistent structure

---

## Health Score as Quality Gate

### Recommended Thresholds

**For production release:**

- Minimum overall score: 80
- Minimum coverage: 90
- Minimum freshness: 85

**For open source launch:**

- Minimum overall score: 85
- Minimum coverage: 95
- Minimum quality: 85

**For internal tools:**

- Minimum overall score: 70
- Minimum coverage: 80
- Minimum freshness: 70

### CI/CD Integration

The health score can be checked in CI:

```bash
#!/bin/bash
# check-docs-health.sh

HEALTH_SCORE=$(jq '.healthScore.overall' .doc-state.json)
MIN_SCORE=80

if (( $(echo "$HEALTH_SCORE < $MIN_SCORE" | bc -l) )); then
  echo "❌ Documentation health score ($HEALTH_SCORE) below minimum ($MIN_SCORE)"
  exit 1
else
  echo "✅ Documentation health score: $HEALTH_SCORE"
  exit 0
fi
```

Add to CI pipeline:

```yaml
- name: Check Documentation Health
  run: ./scripts/check-docs-health.sh
```

---

## Calibration and Adjustments

### Initial Baseline

First documentation run typically scores:

- 50-70: Brand new docs, gaps expected
- 70-80: Decent first pass
- 80-90: Unusually thorough initial effort
- 90-100: Rare, very comprehensive

### Realistic Targets

**Maintainable scores:**

- 85-95: Excellent and sustainable
- 95-100: Requires constant attention

**Avoid perfectionism:**

- 100/100 is rarely maintainable
- 85-90 is typically "good enough"
- Focus on high-value improvements

### When Scores Seem Wrong

If health score seems inaccurate:

1. Review component scores individually
2. Check for overly harsh penalties
3. Verify bonus criteria are fair
4. Adjust weights if needed (advanced)

**Default weights are appropriate for most projects:**

- Coverage: 40% (most important)
- Freshness: 30% (critical for accuracy)
- Quality: 20% (matters, but subjective)
- Consistency: 10% (nice to have)

---

## FAQ

**Q: Why is coverage weighted highest?** A: Undocumented features are worse than
imperfect documentation. Coverage ensures basics are present.

**Q: Why is consistency only 10%?** A: Perfect consistency is nice but not
critical. Better to have complete, fresh docs with minor inconsistencies than
perfect but incomplete docs.

**Q: Can I change the weights?** A: The skill uses standard weights. If needed,
manually adjust manifest scores, but default weights work well for most
projects.

**Q: What's a "good" health score?** A: 80+ is good, 85+ is very good, 90+ is
excellent. Anything above 80 indicates solid documentation.

**Q: How often should I check health score?** A: After each feature release or
weekly for active projects. Track trend over time.

---

## Reference: Manifest Spec

# Documentation Manifest Specification

Technical specification for the `.doc-state.json` file that tracks documentation
state.

## Purpose

The manifest enables:

- **Incremental updates:** Know what changed since last documentation
- **Health tracking:** Monitor documentation quality over time
- **Debt management:** Track what needs attention
- **Consistency:** Remember preferences across sessions

## File Location

```
project-root/.doc-state.json
```

This file should be committed to version control.

## Schema

```json
{
  "version": "string",
  "project": {
    "name": "string",
    "type": "string",
    "lastScanned": "ISO 8601 datetime",
    "gitCommit": "string (optional)"
  },
  "preferences": {
    "audiences": ["string"],
    "depthLevel": "string",
    "tone": "string"
  },
  "healthScore": {
    "overall": "number (0-100)",
    "components": {
      "coverage": "number (0-100)",
      "freshness": "number (0-100)",
      "quality": "number (0-100)",
      "consistency": "number (0-100)"
    },
    "trend": ["number"]
  },
  "coverage": {
    "[element-type]": {
      "total": "number",
      "documented": "number",
      "changed": "number"
    }
  },
  "debt": {
    "critical": ["DebtItem"],
    "important": ["DebtItem"],
    "minor": ["DebtItem"]
  },
  "documentationMap": {
    "[file-path]": {
      "lastUpdated": "ISO 8601 datetime",
      "covers": ["string"],
      "wordCount": "number"
    }
  }
}
```

## Field Definitions

### version

**Type:** String  
**Required:** Yes  
**Format:** Semantic version (e.g., "1.0")  
**Description:** Manifest format version. Current version is "1.0"

**Example:**

```json
"version": "1.0"
```

---

### project

**Type:** Object  
**Required:** Yes  
**Description:** Project metadata

#### project.name

**Type:** String  
**Required:** Yes  
**Description:** Project name from package.json, Cargo.toml, or directory name

**Example:**

```json
"name": "express-api"
```

#### project.type

**Type:** String  
**Required:** Yes  
**Allowed values:** `rest-api`, `cli`, `library`, `web-app`, `database`,
`monorepo`, `other`  
**Description:** Project type identified during analysis

**Example:**

```json
"type": "rest-api"
```

#### project.lastScanned

**Type:** String (ISO 8601 datetime)  
**Required:** Yes  
**Description:** When the project was last analyzed

**Example:**

```json
"lastScanned": "2025-01-10T14:30:00Z"
```

#### project.gitCommit

**Type:** String  
**Required:** No  
**Description:** Git commit hash at last scan. Used for delta analysis.

**Example:**

```json
"gitCommit": "a3f2b1c9d8e7f6a5b4c3d2e1f0"
```

---

### preferences

**Type:** Object  
**Required:** Yes  
**Description:** User preferences for documentation generation

#### preferences.audiences

**Type:** Array of strings  
**Required:** Yes  
**Allowed values:** `"developers"`, `"users"`  
**Description:** Who needs the documentation

**Example:**

```json
"audiences": ["developers", "users"]
```

#### preferences.depthLevel

**Type:** String  
**Required:** Yes  
**Allowed values:** `"standard"`, `"deep"`  
**Description:** Documentation depth preference

**Example:**

```json
"depthLevel": "standard"
```

#### preferences.tone

**Type:** String  
**Required:** Yes  
**Allowed values:** `"technical"`, `"professional"`, `"conversational"`  
**Description:** Documentation tone/voice

**Example:**

```json
"tone": "professional"
```

---

### healthScore

**Type:** Object  
**Required:** Yes  
**Description:** Documentation health metrics

#### healthScore.overall

**Type:** Number  
**Required:** Yes  
**Range:** 0-100  
**Description:** Weighted average of component scores

**Calculation:**

```
overall = (coverage * 0.40) + (freshness * 0.30) + (quality * 0.20) + (consistency * 0.10)
```

**Example:**

```json
"overall": 92
```

#### healthScore.components

**Type:** Object  
**Required:** Yes  
**Description:** Individual quality dimension scores

**Fields:**

- `coverage`: 0-100, represents % of public surface documented
- `freshness`: 0-100, represents how current docs are
- `quality`: 0-100, represents documentation quality
- `consistency`: 0-100, represents uniformity

**Example:**

```json
"components": {
  "coverage": 95,
  "freshness": 98,
  "quality": 88,
  "consistency": 90
}
```

#### healthScore.trend

**Type:** Array of numbers  
**Required:** Yes  
**Description:** Historical overall health scores (last 10)

**Example:**

```json
"trend": [65, 72, 78, 85, 92]
```

---

### coverage

**Type:** Object  
**Required:** Yes  
**Description:** Coverage tracking by element type

**Structure:** Dynamic keys based on project type

**For REST APIs:**

```json
"coverage": {
  "endpoints": {
    "total": 12,
    "documented": 12,
    "changed": 0
  },
  "schemas": {
    "total": 3,
    "documented": 3,
    "changed": 0
  }
}
```

**For CLIs:**

```json
"coverage": {
  "commands": {
    "total": 8,
    "documented": 8,
    "changed": 1
  },
  "options": {
    "total": 24,
    "documented": 22,
    "changed": 2
  }
}
```

**For Libraries:**

```json
"coverage": {
  "functions": {
    "total": 45,
    "documented": 43,
    "changed": 2
  },
  "classes": {
    "total": 12,
    "documented": 12,
    "changed": 0
  }
}
```

**For Web Apps:**

```json
"coverage": {
  "components": {
    "total": 32,
    "documented": 28,
    "changed": 4
  },
  "features": {
    "total": 15,
    "documented": 15,
    "changed": 0
  }
}
```

---

### debt

**Type:** Object  
**Required:** Yes  
**Description:** Documentation debt tracking

#### DebtItem Structure

```typescript
{
  "item": string,          // What needs to be done
  "effort": string,        // "low" | "medium" | "high"
  "status": string,        // "to-fix" | "accepted" | "wont-fix"
  "created": string,       // ISO 8601 datetime
  "notes": string          // Optional context
}
```

#### debt.critical

**Type:** Array of DebtItem  
**Required:** Yes  
**Description:** Critical documentation issues (missing core docs, broken
examples)

**Example:**

```json
"critical": [
  {
    "item": "API authentication not documented",
    "effort": "medium",
    "status": "to-fix",
    "created": "2025-01-08T10:00:00Z"
  }
]
```

#### debt.important

**Type:** Array of DebtItem  
**Required:** Yes  
**Description:** Important but not blocking (missing examples, incomplete
guides)

**Example:**

```json
"important": [
  {
    "item": "Add deployment troubleshooting section",
    "effort": "low",
    "status": "to-fix",
    "created": "2025-01-09T14:00:00Z"
  }
]
```

#### debt.minor

**Type:** Array of DebtItem  
**Required:** Yes  
**Description:** Nice-to-have improvements

**Example:**

```json
"minor": [
  {
    "item": "Add more advanced examples",
    "effort": "high",
    "status": "accepted",
    "created": "2025-01-05T09:00:00Z",
    "notes": "Acceptable gap for v1"
  }
]
```

---

### documentationMap

**Type:** Object  
**Required:** Yes  
**Description:** Index of all documentation files

**Structure:** Keys are file paths relative to project root

#### DocumentationFile Structure

```typescript
{
  "lastUpdated": string,    // ISO 8601 datetime
  "covers": string[],       // Topics covered
  "wordCount": number       // Approximate word count
}
```

**Example:**

```json
"documentationMap": {
  "README.md": {
    "lastUpdated": "2025-01-10T14:30:00Z",
    "covers": ["overview", "quick-start", "installation"],
    "wordCount": 850
  },
  "docs/developers/api.md": {
    "lastUpdated": "2025-01-10T14:30:00Z",
    "covers": ["endpoints", "authentication", "rate-limiting"],
    "wordCount": 2400
  },
  "docs/users/getting-started.md": {
    "lastUpdated": "2025-01-10T14:30:00Z",
    "covers": ["installation", "first-use", "basic-features"],
    "wordCount": 1200
  }
}
```

---

## Complete Example

```json
{
  "version": "1.0",
  "project": {
    "name": "express-api",
    "type": "rest-api",
    "lastScanned": "2025-01-10T14:30:00Z",
    "gitCommit": "a3f2b1c9d8e7f6a5b4c3d2e1f0"
  },
  "preferences": {
    "audiences": ["developers", "users"],
    "depthLevel": "standard",
    "tone": "professional"
  },
  "healthScore": {
    "overall": 92,
    "components": {
      "coverage": 95,
      "freshness": 98,
      "quality": 88,
      "consistency": 90
    },
    "trend": [65, 72, 78, 85, 92]
  },
  "coverage": {
    "endpoints": {
      "total": 12,
      "documented": 12,
      "changed": 0
    },
    "schemas": {
      "total": 3,
      "documented": 3,
      "changed": 0
    },
    "middleware": {
      "total": 6,
      "documented": 5,
      "changed": 1
    }
  },
  "debt": {
    "critical": [],
    "important": [
      {
        "item": "Document webhook validation",
        "effort": "medium",
        "status": "to-fix",
        "created": "2025-01-09T10:00:00Z"
      }
    ],
    "minor": [
      {
        "item": "Add performance optimization guide",
        "effort": "high",
        "status": "accepted",
        "created": "2025-01-05T15:00:00Z",
        "notes": "Defer to v2"
      }
    ]
  },
  "documentationMap": {
    "README.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["overview", "quick-start"],
      "wordCount": 850
    },
    "docs/developers/api.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["endpoints", "auth"],
      "wordCount": 2400
    },
    "docs/developers/architecture.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["system-design", "database"],
      "wordCount": 1800
    },
    "docs/users/getting-started.md": {
      "lastUpdated": "2025-01-10T14:30:00Z",
      "covers": ["installation", "first-use"],
      "wordCount": 1200
    }
  }
}
```

---

## Manifest Evolution

### Version History

**v1.0** (Current)

- Initial manifest format
- Four quality dimensions
- Debt prioritization
- Documentation map

### Future Considerations

Potential additions in future versions:

- Performance metrics (doc load times)
- User feedback integration
- Translation tracking
- Asset references (images, diagrams)

---

## Working with the Manifest

### Initial Creation

On first run, the skill creates a manifest with:

- Empty coverage (will be populated)
- Initial health score of 0
- Empty debt arrays
- Empty documentation map

### Updates

On subsequent runs, the skill:

1. Loads existing manifest
2. Compares current code state vs. manifest
3. Identifies changes (added/modified/removed)
4. Updates coverage data
5. Recalculates health scores
6. Updates trend array
7. Modifies debt items
8. Updates documentation map

### Git Integration

If git is available:

- Manifest stores current commit hash
- Next run compares HEAD to stored commit
- Git diff shows exactly what changed
- Only changed files trigger doc updates

### Manual Edits

If user manually edits documentation:

- Quick Mode preserves manual changes
- Comprehensive Mode can ask to regenerate or preserve
- Manifest tracks last update time per file

---

## Error Handling

### Missing Manifest

If `.doc-state.json` doesn't exist:

- Treat as first-time documentation
- Create fresh manifest
- No delta analysis possible
- Generate all documentation

### Corrupted Manifest

If manifest is invalid JSON:

- Log error
- Ask user: regenerate or fix?
- If regenerate: back up old manifest to `.doc-state.json.bak`
- Create fresh manifest

### Version Mismatch

If manifest version doesn't match current:

- Attempt migration if possible
- Otherwise: regenerate manifest
- Preserve what's possible from old version

---

## Best Practices

### Commit to Version Control

The manifest should be committed because:

- Team members share documentation state
- CI/CD can check doc freshness
- Documentation health visible in repo

### Don't Edit Manually

The manifest is generated and managed by the skill. Manual edits will be
overwritten.

### Review Trends

Health score trend shows documentation quality over time:

- Upward trend: good
- Downward trend: debt accumulating
- Flat trend: stable but may need improvement

### Address Critical Debt

Don't let critical debt accumulate:

- Critical items block users
- Fix before adding new features
- Schedule time for doc maintenance

---

## Reference: Project Types Guide

# Project Types Guide

This guide helps the skill adapt documentation structure and content to
different project types.

## Project Type Identification

The skill identifies project type through:

- File structure patterns
- Package.json / requirements.txt / Cargo.toml presence
- Framework detection
- Folder naming conventions

## Documentation Patterns by Project Type

### REST API / Web Service

**Key characteristics:**

- Endpoints are the primary interface
- Request/response patterns matter
- Authentication/authorization critical
- Error handling needs emphasis

**Documentation structure:**

```
/docs
├── api.md (or per-resource files)
│   ├── Authentication
│   ├── Endpoints (grouped by resource)
│   ├── Request/response examples
│   ├── Error codes
│   └── Rate limiting
├── architecture.md
│   ├── System design
│   ├── Database schema
│   └── Service dependencies
├── deployment.md
└── troubleshooting.md
```

**What to emphasize:**

- Every endpoint documented with method, path, parameters, response
- Request/response examples in multiple formats
- Authentication flow with examples
- Error codes with meaning and resolution
- Rate limiting and quotas

**Common ADRs:**

- Why this framework (Express/FastAPI/etc)?
- Why this database?
- Why this authentication approach?
- API versioning strategy

---

### Command-Line Tool (CLI)

**Key characteristics:**

- Commands and subcommands are the interface
- Flags and options are critical
- Installation and PATH setup matter
- Help text should match docs

**Documentation structure:**

```
/docs
├── installation.md
│   ├── Prerequisites
│   ├── Installation methods
│   └── Verification
├── commands.md (or per-command files)
│   ├── Global options
│   ├── Command reference
│   └── Examples
├── configuration.md
│   ├── Config file format
│   └── Environment variables
└── troubleshooting.md
```

**What to emphasize:**

- Installation for multiple platforms
- Every command with all flags/options
- Abundant examples showing common workflows
- Configuration options
- Shell integration (completions, aliases)

**Common ADRs:**

- Why this CLI framework?
- Why this config format (YAML/JSON/TOML)?
- Plugin architecture decisions

---

### JavaScript/TypeScript Library

**Key characteristics:**

- API surface is functions/classes/types
- Installation from npm/yarn
- Import patterns matter
- TypeScript types are documentation

**Documentation structure:**

```
/docs
├── getting-started.md
│   ├── Installation
│   ├── Basic usage
│   └── Core concepts
├── api-reference.md
│   ├── Functions
│   ├── Classes
│   └── Types
├── guides/
│   ├── common-patterns.md
│   ├── advanced-usage.md
│   └── migration-guides.md
└── examples/
```

**What to emphasize:**

- Installation command and import patterns
- Function signatures with parameter descriptions
- Return values and types
- Common use cases with examples
- Browser vs Node differences (if applicable)

**Common ADRs:**

- Why these peer dependencies?
- Why this module format (ESM/CommonJS)?
- Tree-shaking considerations

---

### Web Application (React/Vue/etc)

**Key characteristics:**

- UI is the interface
- Component hierarchy matters
- State management needs explanation
- Deployment varies widely

**Documentation structure:**

```
/docs
├── users/ (if public-facing)
│   ├── getting-started.md
│   ├── features.md
│   └── troubleshooting.md
├── developers/
│   ├── architecture.md
│   ├── components.md
│   ├── state-management.md
│   ├── styling.md
│   ├── deployment.md
│   └── contributing.md
```

**What to emphasize:**

- Architecture overview (data flow, state, routing)
- Component organization and patterns
- Environment variables and configuration
- Build and deployment process
- Development setup

**Common ADRs:**

- Why this framework?
- Why this state management approach?
- Why this styling solution?
- Routing architecture

---

### Python Package

**Key characteristics:**

- Installable via pip
- Modules and classes are API
- Python version support matters
- Virtual environments standard

**Documentation structure:**

```
/docs
├── installation.md
│   ├── Requirements
│   ├── pip install
│   └── Virtual environments
├── quickstart.md
├── api/
│   ├── module-name.md (per module)
│   └── classes.md
├── guides/
└── examples/
```

**What to emphasize:**

- Python version requirements
- Installation via pip
- Import patterns
- Class/function documentation
- Type hints as part of API

**Common ADRs:**

- Why these dependencies?
- Why this project structure?
- Python version support decisions

---

### Database / Data Store

**Key characteristics:**

- Schema/data model is primary
- Queries and operations are interface
- Performance characteristics matter
- Migration strategy critical

**Documentation structure:**

```
/docs
├── getting-started.md
├── schema.md
│   ├── Tables/Collections
│   ├── Relationships
│   └── Indexes
├── operations.md
│   ├── CRUD operations
│   ├── Queries
│   └── Transactions
├── performance.md
└── migrations.md
```

**What to emphasize:**

- Data model with diagrams
- Query patterns and examples
- Indexing strategy
- Migration approach
- Backup and restore

**Common ADRs:**

- Why this database technology?
- Schema design decisions
- Normalization choices
- Indexing strategy

---

### Monorepo / Multi-Package

**Key characteristics:**

- Multiple projects in one repo
- Shared dependencies and tooling
- Workspace management
- Package relationships

**Documentation structure:**

```
/docs
├── overview.md
│   ├── Repository structure
│   ├── Package relationships
│   └── Development workflow
├── packages/
│   ├── package-a/
│   ├── package-b/
│   └── shared/
└── contributing.md
```

**What to emphasize:**

- Overall architecture
- How packages relate
- Shared dependencies management
- Development commands
- Publishing workflow

**Common ADRs:**

- Why monorepo approach?
- Why this workspace tool?
- Versioning strategy
- Deployment coordination

---

## Adapting Documentation Structure

### Small Projects (<1000 lines)

Keep it simple:

- Single comprehensive README
- Maybe 1-2 additional docs if needed
- Inline code comments sufficient

### Medium Projects (1000-10000 lines)

Structured documentation:

- README for overview
- /docs with 5-10 focused files
- Examples directory
- Contributing guide

### Large Projects (>10000 lines)

Full documentation suite:

- Comprehensive README
- Structured /docs with subsections
- Documentation map
- Multiple example sets
- ADRs for major decisions

## Framework-Specific Considerations

### Express.js

- Route organization
- Middleware chain
- Error handling middleware
- Request/response lifecycle

### React

- Component patterns
- State management (Context/Redux/Zustand)
- Hook usage
- Rendering optimization

### FastAPI

- Automatic OpenAPI docs
- Pydantic models
- Dependency injection
- Async patterns

### Next.js

- App vs Pages router
- Server vs Client components
- Data fetching patterns
- Deployment options

### Django

- Apps structure
- Models and migrations
- Views and templates
- Admin customization

## Documentation Depth by Project Maturity

### Proof of Concept

- Minimal docs, README sufficient
- Focus on "what is this" and "how to run it"

### Internal Tool

- Installation and usage
- Configuration options
- Common workflows
- Troubleshooting

### Public Open Source

- Comprehensive getting started
- Full API reference
- Contributing guide
- Code of conduct
- License information
- Examples and guides

### Production Service

- All of open source, plus:
- SLA documentation
- Incident response
- Monitoring and alerting
- Disaster recovery

## Special Considerations

### Microservices

Document each service AND the system:

- System architecture overview
- Service boundaries and responsibilities
- Inter-service communication
- Data ownership
- Deployment orchestration

### Serverless

- Function documentation
- Event triggers
- Environment variables
- Cold start considerations
- Cost implications

### Mobile Apps

- Platform-specific setup (iOS/Android)
- Build and deployment
- App Store submission
- Testing on devices

### Browser Extensions

- Installation from store
- Development mode setup
- Permissions explanation
- Browser compatibility

## Integration Points

### CI/CD

Document:

- Build process
- Test execution
- Deployment pipeline
- Environment promotion

### Third-Party Services

Document:

- API keys and configuration
- Rate limits and quotas
- Error handling
- Webhook setup

### Authentication Providers

Document:

- Setup process
- Configuration
- User flows
- Token management

---

## Reference: Quality Standards

# Documentation Quality Standards

Concrete criteria for evaluating documentation quality. These standards guide
documentation generation and assessment.

## The Four Quality Dimensions

Documentation quality is measured across four dimensions:

1. **Coverage** (40% of health score)
2. **Freshness** (30% of health score)
3. **Quality** (20% of health score)
4. **Consistency** (10% of health score)

---

## 1. Coverage Quality

**Definition:** What percentage of the public surface area is documented?

### Scoring Criteria

| Score  | Coverage | Description               |
| ------ | -------- | ------------------------- |
| 90-100 | ≥95%     | Nearly complete coverage  |
| 80-89  | 85-94%   | Good coverage, minor gaps |
| 70-79  | 75-84%   | Adequate, noticeable gaps |
| 60-69  | 65-74%   | Partial coverage          |
| <60    | <65%     | Significant gaps          |

### What Counts as "Public Surface"

**For APIs:**

- Every endpoint
- Every request parameter
- Every response field
- Every error code
- Authentication requirements

**For CLIs:**

- Every command
- Every flag/option
- Every subcommand
- Configuration options
- Environment variables

**For Libraries:**

- Every exported function
- Every exported class
- Every public method
- Every exported type
- Key configuration options

**For Web Apps:**

- Every user-facing feature
- Major UI components
- Configuration options
- Deployment process

### Quality Criteria for Coverage

✅ **High Quality:**

- Every public element has documentation
- No "TODO" or placeholder sections
- Examples provided for non-trivial elements
- Edge cases and limitations noted

❌ **Low Quality:**

- Missing documentation for key features
- Placeholder text like "Coming soon"
- No examples for complex features
- Undocumented breaking changes

### Example: API Coverage

**100% Coverage:**

```markdown
### GET /api/users/:id

Retrieves a single user by ID.

**Parameters:**

- `id` (required): User ID as UUID

**Response:** 200 OK [full response example]

**Errors:**

- 401: Unauthorized
- 404: User not found

**Example:** [working code example]
```

**50% Coverage:**

```markdown
### GET /api/users/:id

Gets a user.
```

---

## 2. Freshness Quality

**Definition:** How current is the documentation relative to the codebase?

### Scoring Criteria

| Score  | Freshness      | Description                               |
| ------ | -------------- | ----------------------------------------- |
| 90-100 | Current        | Docs match latest code                    |
| 80-89  | Mostly current | 1-2 minor outdated items                  |
| 70-79  | Somewhat stale | 3-5 outdated items                        |
| 60-69  | Stale          | 6-10 outdated items                       |
| <60    | Very stale     | >10 outdated items or critical stale docs |

### What Makes Docs Stale

**Code changed, docs didn't:**

- New features undocumented
- Changed API signatures not updated
- Removed features still documented
- Old examples that no longer work

**Indicators of staleness:**

- Git commits adding features without doc updates
- Inline code comments contradicting docs
- Examples using deprecated patterns
- Screenshots showing old UI

### Quality Criteria for Freshness

✅ **High Quality:**

- All recent changes documented
- Examples tested and working
- Breaking changes clearly noted
- Migration guides for major changes

❌ **Low Quality:**

- Examples don't run
- References to removed features
- Old version numbers in examples
- Contradictions between code and docs

### Example: Fresh vs. Stale

**Fresh:**

```markdown
### Authentication (Updated: 2025-01-10)

We use JWT tokens. As of v2.0, tokens expire after 1 hour.

**Breaking Change in v2.0:** Token lifetime reduced from 24h to 1h.

**Migration:** Implement token refresh. See [refresh guide](./auth-refresh.md)
```

**Stale:**

```markdown
### Authentication

We use session cookies.

[Note: This was true in v1.x but changed in v2.0]
```

---

## 3. Quality Quality

**Definition:** How well-written and useful is the documentation?

This dimension evaluates the documentation itself, not just coverage or
freshness.

### Scoring Criteria

| Score  | Quality Level | Description                                 |
| ------ | ------------- | ------------------------------------------- |
| 90-100 | Excellent     | Clear, complete, helpful, abundant examples |
| 80-89  | Good          | Clear and helpful, some examples            |
| 70-79  | Adequate      | Understandable but could be better          |
| 60-69  | Poor          | Confusing or minimal                        |
| <60    | Very poor     | Unclear, unhelpful, or misleading           |

### Quality Factors

#### Clarity

- Concepts explained before used
- Technical terms defined
- Logical flow of information
- No ambiguity

#### Completeness

- "Why" explained, not just "what"
- Edge cases covered
- Limitations noted
- Troubleshooting provided

#### Examples

- Working code examples
- Multiple examples showing different use cases
- Examples progress from simple to complex
- Examples are realistic

#### Usability

- Easy to navigate
- Good table of contents
- Cross-references work
- Searchable

### Quality Criteria

✅ **High Quality:**

- Multiple working examples per major feature
- Architecture Decision Records explaining "why"
- Troubleshooting section with real issues
- Diagrams for complex concepts
- Progressive disclosure (simple → complex)

❌ **Low Quality:**

- No examples, or examples that don't run
- Only "what" documented, no "why"
- No troubleshooting
- Assumes too much knowledge
- Disorganized structure

### Example: High Quality Section

````markdown
## Rate Limiting

To prevent abuse, all API endpoints are rate limited.

### How It Works

Each API key gets 1000 requests per hour. This counter resets at the top of each
hour (e.g., 2:00pm, 3:00pm).

### Why Rate Limiting?

We implement rate limiting to:

- Prevent abuse and DoS attacks
- Ensure fair resource allocation
- Maintain service stability

See [ADR-003](./adr/003-rate-limiting.md) for the full decision rationale.

### Checking Your Limit

Response headers show your status:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1641654000
```
````

### Example: Handling Rate Limits

```javascript
async function makeRequest() {
  const response = await fetch("/api/users", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (response.status === 429) {
    const resetTime = response.headers.get("X-RateLimit-Reset");
    const waitMs = resetTime * 1000 - Date.now();
    console.log(`Rate limited. Waiting ${waitMs}ms`);
    await sleep(waitMs);
    return makeRequest(); // Retry
  }

  return response.json();
}
```

### Troubleshooting

**Problem:** Getting 429 errors frequently

**Causes:**

- Making requests in tight loops
- Multiple servers using same key
- Burst traffic patterns

**Solutions:**

- Implement exponential backoff
- Use separate API keys per server
- Batch requests where possible
- Cache responses

````

---

## 4. Consistency Quality

**Definition:** Is documentation uniform in style, terminology, and structure?

### Scoring Criteria

| Score | Consistency | Description |
|-------|-------------|-------------|
| 90-100 | Very consistent | Uniform throughout |
| 80-89 | Mostly consistent | Minor inconsistencies |
| 70-79 | Somewhat inconsistent | Noticeable variance |
| 60-69 | Inconsistent | Feels disjointed |
| <60 | Very inconsistent | Chaotic, confusing |

### Consistency Factors

#### Terminology
- Same terms used for same concepts
- No synonyms causing confusion
- Capitalization consistent
- Abbreviations defined once, used consistently

#### Tone
- Formal vs. casual consistent
- Second person ("you") vs. third person
- Active vs. passive voice

#### Structure
- Sections follow similar patterns
- Headers use consistent hierarchy
- Code blocks formatted uniformly
- Lists formatted the same way

#### Formatting
- Consistent markdown style
- Code syntax highlighting
- Link formatting
- Emphasis (bold/italic) patterns

### Quality Criteria

✅ **High Quality:**
- Style guide followed throughout
- Terminology defined in glossary
- Consistent section structure
- Uniform code formatting
- Same tone throughout

❌ **Low Quality:**
- "User" vs "customer" vs "client" used interchangeably
- Mix of casual and formal tone
- Inconsistent header levels
- Different code formatting styles
- Random capitalization

### Example: Inconsistent vs. Consistent

**Inconsistent:**
```markdown
## Getting Started

Install the package:
`npm install myapp`

## API reference

Use the createUser method:

~~~javascript
createUser(userData)
~~~

## Usage

You can make a new user like this:
```js
makeNewUser({name: "John"})
````

````

**Consistent:**
```markdown
## Getting Started

Install the package:

```bash
npm install myapp
````

## API Reference

### createUser(userData)

Creates a new user.

**Example:**

```javascript
const user = await createUser({ name: "John" });
```

## Usage

### Creating Users

```javascript
const user = await createUser({ name: "John" });
```

````

---

## Additional Quality Indicators

### Examples Quality

**Excellent examples:**
- Actually run without modification
- Cover common use cases
- Show error handling
- Include comments explaining why
- Progress from simple to advanced

**Poor examples:**
- Pseudocode that doesn't run
- Missing setup steps
- No error handling
- No context provided

### Architecture Documentation Quality

**Excellent architecture docs:**
- System diagram showing components
- Data flow diagrams
- Explanation of design decisions
- Trade-offs discussed
- Alternatives considered documented

**Poor architecture docs:**
- No diagrams
- Just lists of technologies
- No explanation of "why"
- Missing important details

### Troubleshooting Quality

**Excellent troubleshooting:**
- Organized by symptom/error
- Common issues documented
- Root causes explained
- Step-by-step solutions
- Prevention tips

**Poor troubleshooting:**
- Just "check the logs"
- No specific errors listed
- Vague solutions
- Missing common issues

### ADR Quality

**Excellent ADRs:**
- Clear context (what was the situation?)
- Specific decision made
- Detailed rationale
- Consequences acknowledged
- Alternatives considered with trade-offs

**Poor ADRs:**
- Just "we chose X"
- No context
- No rationale
- Alternatives not mentioned

---

## Accessibility Quality

Good documentation is accessible:

✅ **Accessible:**
- Headings use proper hierarchy (h1 → h2 → h3)
- Links have descriptive text ("see authentication guide" not "click here")
- Images have alt text
- Code blocks have language labels
- Color not sole means of conveying info

❌ **Not accessible:**
- Broken heading hierarchy
- "Click here" links
- Images without alt text
- Unlabeled code blocks
- Red/green as only diff indicator

---

## Testing Documentation Quality

### Manual Tests

1. **The Newcomer Test**
   - Can someone who's never seen this project get started?
   - Are prerequisites clear?
   - Do the quick start steps work?

2. **The Example Test**
   - Copy examples and run them
   - Do they work without modification?
   - Are all dependencies mentioned?

3. **The Search Test**
   - Pick a common task
   - Can you find the answer in docs?
   - Is it easy to find?

4. **The Link Test**
   - Do all internal links work?
   - Do external links resolve?
   - No broken references?

5. **The Completeness Test**
   - Pick a public API element
   - Is it fully documented?
   - Are edge cases covered?

### Automated Tests

**Link validation:**
```bash
# Script to check all links
./docs/scripts/validate-links.sh
````

**Example testing:**

```bash
# Run all example code
./docs/scripts/test-examples.sh
```

**Accessibility checking:**

```bash
# Check heading hierarchy, alt text, etc.
./docs/scripts/accessibility-check.sh
```

---

## Quality Improvement Checklist

When improving documentation quality:

**Coverage:**

- [ ] Identify undocumented public APIs
- [ ] Add missing examples
- [ ] Document edge cases
- [ ] Cover error scenarios

**Freshness:**

- [ ] Update examples to match current code
- [ ] Remove references to deleted features
- [ ] Add migration guides for breaking changes
- [ ] Update version numbers

**Quality:**

- [ ] Add "why" to accompany "what"
- [ ] Create working examples
- [ ] Add troubleshooting section
- [ ] Create diagrams for complex concepts

**Consistency:**

- [ ] Standardize terminology
- [ ] Uniform tone throughout
- [ ] Consistent formatting
- [ ] Follow style guide

---

## Reviewing Documentation

### Review Checklist

**Accuracy:**

- [ ] All facts verified against code
- [ ] Examples tested and working
- [ ] Version numbers correct
- [ ] Links resolve

**Completeness:**

- [ ] All features documented
- [ ] Configuration covered
- [ ] Troubleshooting present
- [ ] Examples for main use cases

**Clarity:**

- [ ] Understandable to target audience
- [ ] No jargon without definition
- [ ] Logical flow
- [ ] Visual aids where helpful

**Findability:**

- [ ] Good navigation
- [ ] Clear headings
- [ ] Searchable terms
- [ ] Useful table of contents
