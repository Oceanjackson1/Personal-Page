---
title: "Product Manager Toolkit"
description: "Comprehensive toolkit for product managers including RICE prioritization, customer interview analysis, PRD templates, discovery frameworks, and go-to-market strategies. Use for feature prioritizati..."
category: "other"
source: "community"
author: "Community"
tags: ["product", "manager", "toolkit"]
date: 2026-03-20
---

# Product Manager Toolkit

Essential tools and frameworks for modern product management, from discovery to delivery.

## Quick Start

### For Feature Prioritization
```bash
python scripts/rice_prioritizer.py sample  # Create sample CSV
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### For Interview Analysis
```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### For PRD Creation
1. Choose template from `references/prd_templates.md`
2. Fill in sections based on discovery work
3. Review with stakeholders
4. Version control in your PM tool

## Core Workflows

### Feature Prioritization Process

1. **Gather Feature Requests**
   - Customer feedback
   - Sales requests
   - Technical debt
   - Strategic initiatives

2. **Score with RICE**
   ```bash
   # Create CSV with: name,reach,impact,confidence,effort
   python scripts/rice_prioritizer.py features.csv
   ```
   - **Reach**: Users affected per quarter
   - **Impact**: massive/high/medium/low/minimal
   - **Confidence**: high/medium/low
   - **Effort**: xl/l/m/s/xs (person-months)

3. **Analyze Portfolio**
   - Review quick wins vs big bets
   - Check effort distribution
   - Validate against strategy

4. **Generate Roadmap**
   - Quarterly capacity planning
   - Dependency mapping
   - Stakeholder alignment

### Customer Discovery Process

1. **Conduct Interviews**
   - Use semi-structured format
   - Focus on problems, not solutions
   - Record with permission

2. **Analyze Insights**
   ```bash
   python scripts/customer_interview_analyzer.py transcript.txt
   ```
   Extracts:
   - Pain points with severity
   - Feature requests with priority
   - Jobs to be done
   - Sentiment analysis
   - Key themes and quotes

3. **Synthesize Findings**
   - Group similar pain points
   - Identify patterns across interviews
   - Map to opportunity areas

4. **Validate Solutions**
   - Create solution hypotheses
   - Test with prototypes
   - Measure actual vs expected behavior

### PRD Development Process

1. **Choose Template**
   - **Standard PRD**: Complex features (6-8 weeks)
   - **One-Page PRD**: Simple features (2-4 weeks)
   - **Feature Brief**: Exploration phase (1 week)
   - **Agile Epic**: Sprint-based delivery

2. **Structure Content**
   - Problem → Solution → Success Metrics
   - Always include out-of-scope
   - Clear acceptance criteria

3. **Collaborate**
   - Engineering for feasibility
   - Design for experience
   - Sales for market validation
   - Support for operational impact

## Key Scripts

### rice_prioritizer.py
Advanced RICE framework implementation with portfolio analysis.

**Features**:
- RICE score calculation
- Portfolio balance analysis (quick wins vs big bets)
- Quarterly roadmap generation
- Team capacity planning
- Multiple output formats (text/json/csv)

**Usage Examples**:
```bash
# Basic prioritization
python scripts/rice_prioritizer.py features.csv

# With custom team capacity (person-months per quarter)
python scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON for integration
python scripts/rice_prioritizer.py features.csv --output json
```

### customer_interview_analyzer.py
NLP-based interview analysis for extracting actionable insights.

**Capabilities**:
- Pain point extraction with severity assessment
- Feature request identification and classification
- Jobs-to-be-done pattern recognition
- Sentiment analysis
- Theme extraction
- Competitor mentions
- Key quotes identification

**Usage Examples**:
```bash
# Analyze single interview
python scripts/customer_interview_analyzer.py interview.txt

# Output as JSON for aggregation
python scripts/customer_interview_analyzer.py interview.txt json
```

## Reference Documents

### prd_templates.md
Multiple PRD formats for different contexts:

1. **Standard PRD Template**
   - Comprehensive 11-section format
   - Best for major features
   - Includes technical specs

2. **One-Page PRD**
   - Concise format for quick alignment
   - Focus on problem/solution/metrics
   - Good for smaller features

3. **Agile Epic Template**
   - Sprint-based delivery
   - User story mapping
   - Acceptance criteria focus

4. **Feature Brief**
   - Lightweight exploration
   - Hypothesis-driven
   - Pre-PRD phase

## Prioritization Frameworks

### RICE Framework
```
Score = (Reach × Impact × Confidence) / Effort

Reach: # of users/quarter
Impact: 
  - Massive = 3x
  - High = 2x
  - Medium = 1x
  - Low = 0.5x
  - Minimal = 0.25x
Confidence:
  - High = 100%
  - Medium = 80%
  - Low = 50%
Effort: Person-months
```

### Value vs Effort Matrix
```
         Low Effort    High Effort
         
High     QUICK WINS    BIG BETS
Value    [Prioritize]   [Strategic]
         
Low      FILL-INS      TIME SINKS
Value    [Maybe]       [Avoid]
```

### MoSCoW Method
- **Must Have**: Critical for launch
- **Should Have**: Important but not critical
- **Could Have**: Nice to have
- **Won't Have**: Out of scope

## Discovery Frameworks

### Customer Interview Guide
```
1. Context Questions (5 min)
   - Role and responsibilities
   - Current workflow
   - Tools used

2. Problem Exploration (15 min)
   - Pain points
   - Frequency and impact
   - Current workarounds

3. Solution Validation (10 min)
   - Reaction to concepts
   - Value perception
   - Willingness to pay

4. Wrap-up (5 min)
   - Other thoughts
   - Referrals
   - Follow-up permission
```

### Hypothesis Template
```
We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We'll know we're right when [metric]
```

### Opportunity Solution Tree
```
Outcome
├── Opportunity 1
│   ├── Solution A
│   └── Solution B
└── Opportunity 2
    ├── Solution C
    └── Solution D
```

## Metrics & Analytics

### North Star Metric Framework
1. **Identify Core Value**: What's the #1 value to users?
2. **Make it Measurable**: Quantifiable and trackable
3. **Ensure It's Actionable**: Teams can influence it
4. **Check Leading Indicator**: Predicts business success

### Funnel Analysis Template
```
Acquisition → Activation → Retention → Revenue → Referral

Key Metrics:
- Conversion rate at each step
- Drop-off points
- Time between steps
- Cohort variations
```

### Feature Success Metrics
- **Adoption**: % of users using feature
- **Frequency**: Usage per user per time period
- **Depth**: % of feature capability used
- **Retention**: Continued usage over time
- **Satisfaction**: NPS/CSAT for feature

## Best Practices

### Writing Great PRDs
1. Start with the problem, not solution
2. Include clear success metrics upfront
3. Explicitly state what's out of scope
4. Use visuals (wireframes, flows)
5. Keep technical details in appendix
6. Version control changes

### Effective Prioritization
1. Mix quick wins with strategic bets
2. Consider opportunity cost
3. Account for dependencies
4. Buffer for unexpected work (20%)
5. Revisit quarterly
6. Communicate decisions clearly

### Customer Discovery Tips
1. Ask "why" 5 times
2. Focus on past behavior, not future intentions
3. Avoid leading questions
4. Interview in their environment
5. Look for emotional reactions
6. Validate with data

### Stakeholder Management
1. Identify RACI for decisions
2. Regular async updates
3. Demo over documentation
4. Address concerns early
5. Celebrate wins publicly
6. Learn from failures openly

## Common Pitfalls to Avoid

1. **Solution-First Thinking**: Jumping to features before understanding problems
2. **Analysis Paralysis**: Over-researching without shipping
3. **Feature Factory**: Shipping features without measuring impact
4. **Ignoring Technical Debt**: Not allocating time for platform health
5. **Stakeholder Surprise**: Not communicating early and often
6. **Metric Theater**: Optimizing vanity metrics over real value

## Integration Points

This toolkit integrates with:
- **Analytics**: Amplitude, Mixpanel, Google Analytics
- **Roadmapping**: ProductBoard, Aha!, Roadmunk
- **Design**: Figma, Sketch, Miro
- **Development**: Jira, Linear, GitHub
- **Research**: Dovetail, UserVoice, Pendo
- **Communication**: Slack, Notion, Confluence

## Quick Commands Cheat Sheet

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Create sample data
python scripts/rice_prioritizer.py sample

# JSON outputs for integration
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt json
```

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Prd_Templates

# Product Requirements Document (PRD) Templates

## Standard PRD Template

### 1. Executive Summary
**Purpose**: One-page overview for executives and stakeholders

#### Components:
- **Problem Statement** (2-3 sentences)
- **Proposed Solution** (2-3 sentences)
- **Business Impact** (3 bullet points)
- **Timeline** (High-level milestones)
- **Resources Required** (Team size and budget)
- **Success Metrics** (3-5 KPIs)

### 2. Problem Definition

#### 2.1 Customer Problem
- **Who**: Target user persona(s)
- **What**: Specific problem or need
- **When**: Context and frequency
- **Where**: Environment and touchpoints
- **Why**: Root cause analysis
- **Impact**: Cost of not solving

#### 2.2 Market Opportunity
- **Market Size**: TAM, SAM, SOM
- **Growth Rate**: Annual growth percentage
- **Competition**: Current solutions and gaps
- **Timing**: Why now?

#### 2.3 Business Case
- **Revenue Potential**: Projected impact
- **Cost Savings**: Efficiency gains
- **Strategic Value**: Alignment with company goals
- **Risk Assessment**: What if we don't do this?

### 3. Solution Overview

#### 3.1 Proposed Solution
- **High-Level Description**: What we're building
- **Key Capabilities**: Core functionality
- **User Journey**: End-to-end flow
- **Differentiation**: Unique value proposition

#### 3.2 In Scope
- Feature 1: Description and priority
- Feature 2: Description and priority
- Feature 3: Description and priority

#### 3.3 Out of Scope
- Explicitly what we're NOT doing
- Future considerations
- Dependencies on other teams

#### 3.4 MVP Definition
- **Core Features**: Minimum viable feature set
- **Success Criteria**: Definition of "working"
- **Timeline**: MVP delivery date
- **Learning Goals**: What we want to validate

### 4. User Stories & Requirements

#### 4.1 User Stories
```
As a [persona]
I want to [action]
So that [outcome/benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

#### 4.2 Functional Requirements
| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| FR1 | User can... | P0 | Critical for MVP |
| FR2 | System should... | P1 | Important |
| FR3 | Feature must... | P2 | Nice to have |

#### 4.3 Non-Functional Requirements
- **Performance**: Response times, throughput
- **Scalability**: User/data growth targets
- **Security**: Authentication, authorization, data protection
- **Reliability**: Uptime targets, error rates
- **Usability**: Accessibility standards, device support
- **Compliance**: Regulatory requirements

### 5. Design & User Experience

#### 5.1 Design Principles
- Principle 1: Description
- Principle 2: Description
- Principle 3: Description

#### 5.2 Wireframes/Mockups
- Link to Figma/Sketch files
- Key screens and flows
- Interaction patterns

#### 5.3 Information Architecture
- Navigation structure
- Data organization
- Content hierarchy

### 6. Technical Specifications

#### 6.1 Architecture Overview
- System architecture diagram
- Technology stack
- Integration points
- Data flow

#### 6.2 API Design
- Endpoints and methods
- Request/response formats
- Authentication approach
- Rate limiting

#### 6.3 Database Design
- Data model
- Key entities and relationships
- Migration strategy

#### 6.4 Security Considerations
- Authentication method
- Authorization model
- Data encryption
- PII handling

### 7. Go-to-Market Strategy

#### 7.1 Launch Plan
- **Soft Launch**: Beta users, timeline
- **Full Launch**: All users, timeline
- **Marketing**: Campaigns and channels
- **Support**: Documentation and training

#### 7.2 Pricing Strategy
- Pricing model
- Competitive analysis
- Value proposition

#### 7.3 Success Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Adoption Rate | X% | Daily Active Users |
| User Satisfaction | X/10 | NPS Score |
| Revenue Impact | $X | Monthly Recurring Revenue |
| Performance | <Xms | P95 Response Time |

### 8. Risks & Mitigations

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| Technical debt | Medium | High | Allocate 20% for refactoring |
| User adoption | Low | High | Beta program with feedback loops |
| Scope creep | High | Medium | Weekly stakeholder reviews |

### 9. Timeline & Milestones

| Milestone | Date | Deliverables | Success Criteria |
|-----------|------|--------------|-----------------|
| Design Complete | Week 2 | Mockups, IA | Stakeholder approval |
| MVP Development | Week 6 | Core features | All P0s complete |
| Beta Launch | Week 8 | Limited release | 100 beta users |
| Full Launch | Week 12 | General availability | <1% error rate |

### 10. Team & Resources

#### 10.1 Team Structure
- **Product Manager**: [Name]
- **Engineering Lead**: [Name]
- **Design Lead**: [Name]
- **Engineers**: X FTEs
- **QA**: X FTEs

#### 10.2 Budget
- Development: $X
- Infrastructure: $X
- Marketing: $X
- Total: $X

### 11. Appendix
- User Research Data
- Competitive Analysis
- Technical Diagrams
- Legal/Compliance Docs

---

## Agile Epic Template

### Epic: [Epic Name]

#### Overview
**Epic ID**: EPIC-XXX
**Theme**: [Product Theme]
**Quarter**: QX 20XX
**Status**: Discovery | In Progress | Complete

#### Problem Statement
[2-3 sentences describing the problem]

#### Goals & Objectives
1. Objective 1
2. Objective 2
3. Objective 3

#### Success Metrics
- Metric 1: Target
- Metric 2: Target
- Metric 3: Target

#### User Stories
| Story ID | Title | Priority | Points | Status |
|----------|-------|----------|--------|--------|
| US-001 | As a... | P0 | 5 | To Do |
| US-002 | As a... | P1 | 3 | To Do |

#### Dependencies
- Dependency 1: Team/System
- Dependency 2: Team/System

#### Acceptance Criteria
- [ ] All P0 stories complete
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Documentation updated

---

## One-Page PRD Template

### [Feature Name] - One-Page PRD

**Date**: [Date]
**Author**: [PM Name]
**Status**: Draft | In Review | Approved

#### Problem
*What problem are we solving? For whom?*
[2-3 sentences]

#### Solution
*What are we building?*
[2-3 sentences]

#### Why Now?
*What's driving urgency?*
- Reason 1
- Reason 2
- Reason 3

#### Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| KPI 1 | X | Y |
| KPI 2 | X | Y |

#### Scope
**In**: Feature 1, Feature 2, Feature 3
**Out**: Feature A, Feature B

#### User Flow
```
Step 1 → Step 2 → Step 3 → Success!
```

#### Risks
1. Risk 1 → Mitigation
2. Risk 2 → Mitigation

#### Timeline
- Design: Week 1-2
- Development: Week 3-6
- Testing: Week 7
- Launch: Week 8

#### Resources
- Engineering: X developers
- Design: X designer
- QA: X tester

#### Open Questions
1. Question 1?
2. Question 2?

---

## Feature Brief Template (Lightweight)

### Feature: [Name]

#### Context
*Why are we considering this?*

#### Hypothesis
*We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We'll know we're right when [we see this metric]*

#### Proposed Solution
*High-level approach*

#### Effort Estimate
- **Size**: XS | S | M | L | XL
- **Confidence**: High | Medium | Low

#### Next Steps
1. [ ] User research
2. [ ] Design exploration
3. [ ] Technical spike
4. [ ] Stakeholder review
