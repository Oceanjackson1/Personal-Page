---
title: "Iso 13485 Certification"
description: "Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems. Use when users need help with ISO 13485 QMS documentation, including (1) conducting gap analysis of existing documentation, (2..."
category: "research"
source: "community"
author: "Community"
tags: ["iso", "13485", "certification"]
date: 2026-03-20
---

# ISO 13485 Certification Documentation Assistant

## Overview

This skill helps medical device manufacturers prepare comprehensive documentation for ISO 13485:2016 certification. It provides tools, templates, references, and guidance to create, review, and gap-analyze all required Quality Management System (QMS) documentation.

**What this skill provides:**
- Gap analysis of existing documentation
- Templates for all mandatory documents
- Comprehensive requirements guidance
- Step-by-step documentation creation
- Identification of missing documentation
- Compliance checklists

**When to use this skill:**
- Starting ISO 13485 certification process
- Conducting gap analysis against ISO 13485
- Creating or updating QMS documentation
- Preparing for certification audit
- Transitioning from FDA QSR to QMSR
- Harmonizing with EU MDR requirements

## Core Workflow

### 1. Assess Current State (Gap Analysis)

**When to start here:** User has existing documentation and needs to identify gaps

**Process:**

1. **Collect existing documentation:**
   - Ask user to provide directory of current QMS documents
   - Documents can be in any format (.txt, .md, .doc, .docx, .pdf)
   - Include any procedures, manuals, work instructions, forms

2. **Run gap analysis script:**
   ```bash
   python scripts/gap_analyzer.py --docs-dir <path_to_docs> --output gap-report.json
   ```

3. **Review results:**
   - Identify which of the 31 required procedures are present
   - Identify missing key documents (Quality Manual, MDF, etc.)
   - Calculate compliance percentage
   - Prioritize missing documentation

4. **Present findings to user:**
   - Summarize what exists
   - Clearly list what's missing
   - Provide prioritized action plan
   - Estimate effort required

**Output:** Comprehensive gap analysis report with prioritized action items

### 2. Understand Requirements (Reference Consultation)

**When to use:** User needs to understand specific ISO 13485 requirements

**Available references:**
- `references/iso-13485-requirements.md` - Complete clause-by-clause breakdown
- `references/mandatory-documents.md` - All 31 required procedures explained
- `references/gap-analysis-checklist.md` - Detailed compliance checklist
- `references/quality-manual-guide.md` - How to create Quality Manual

**How to use:**

1. **For specific clause questions:**
   - Read relevant section from `iso-13485-requirements.md`
   - Explain requirements in plain language
   - Provide practical examples

2. **For document requirements:**
   - Consult `mandatory-documents.md`
   - Explain what must be documented
   - Clarify when documents are applicable vs. excludable

3. **For implementation guidance:**
   - Use `quality-manual-guide.md` for policy-level documents
   - Provide step-by-step creation process
   - Show examples of good vs. poor implementation

**Key reference sections to know:**

- **Clause 4:** QMS requirements, documentation, risk management, software validation
- **Clause 5:** Management responsibility, quality policy, objectives, management review
- **Clause 6:** Resources, competence, training, infrastructure
- **Clause 7:** Product realization, design, purchasing, production, traceability
- **Clause 8:** Measurement, audits, CAPA, complaints, data analysis

### 3. Create Documentation (Template-Based Generation)

**When to use:** User needs to create specific QMS documents

**Available templates:**
- Quality Manual: `assets/templates/quality-manual-template.md`
- CAPA Procedure: `assets/templates/procedures/CAPA-procedure-template.md`
- Document Control: `assets/templates/procedures/document-control-procedure-template.md`

**Process for document creation:**

1. **Identify what needs to be created:**
   - Based on gap analysis or user request
   - Prioritize critical documents first (Quality Manual, CAPA, Complaints, Audits)

2. **Select appropriate template:**
   - Use Quality Manual template for QM
   - Use procedure templates as examples for SOPs
   - Adapt structure to organization's needs

3. **Customize template with user-specific information:**
   - Replace all placeholder text: [COMPANY NAME], [DATE], [NAME], etc.
   - Tailor scope to user's actual operations
   - Add or remove sections based on applicability
   - Ensure consistency with organization's processes

4. **Key customization areas:**
   - Company information and addresses
   - Product types and classifications
   - Applicable regulatory requirements
   - Organization structure and responsibilities
   - Actual processes and procedures
   - Document numbering schemes
   - Exclusions and justifications

5. **Validate completeness:**
   - All required sections present
   - All placeholders replaced
   - Cross-references correct
   - Approval sections complete

**Document creation priority order:**

**Phase 1 - Foundation (Critical):**
1. Quality Manual
2. Quality Policy and Objectives
3. Document Control procedure
4. Record Control procedure

**Phase 2 - Core Processes (High Priority):**
5. Corrective and Preventive Action (CAPA)
6. Complaint Handling
7. Internal Audit
8. Management Review
9. Risk Management

**Phase 3 - Product Realization (High Priority):**
10. Design and Development (if applicable)
11. Purchasing
12. Production and Service Provision
13. Control of Nonconforming Product

**Phase 4 - Supporting Processes (Medium Priority):**
14. Training and Competence
15. Calibration/Control of M&M Equipment
16. Process Validation
17. Product Identification and Traceability

**Phase 5 - Additional Requirements (Medium Priority):**
18. Feedback and Post-Market Surveillance
19. Regulatory Reporting
20. Customer Communication
21. Data Analysis

**Phase 6 - Specialized (If Applicable):**
22. Installation (if applicable)
23. Servicing (if applicable)
24. Sterilization (if applicable)
25. Contamination Control (if applicable)

### 4. Develop Specific Documents

#### Creating a Quality Manual

**Process:**

1. **Read the comprehensive guide:**
   - Read `references/quality-manual-guide.md` in full
   - Understand structure and required content
   - Review examples provided

2. **Gather organization information:**
   - Legal company name and addresses
   - Product types and classifications
   - Organizational structure
   - Applicable regulations
   - Scope of operations
   - Any exclusions needed

3. **Use template:**
   - Start with `assets/templates/quality-manual-template.md`
   - Follow structure exactly (required by ISO 13485)
   - Replace all placeholders

4. **Complete required sections:**
   - **Section 0:** Document control, approvals
   - **Section 1:** Introduction, company overview
   - **Section 2:** Scope and exclusions (critical - must justify exclusions)
   - **Section 3:** Quality Policy (must be signed by top management)
   - **Sections 4-8:** Address each ISO 13485 clause at policy level
   - **Appendices:** Procedure list, org chart, process map, definitions

5. **Key requirements:**
   - Must reference all 31 documented procedures (Appendix A)
   - Must describe process interactions (Appendix C - create process map)
   - Must define documentation structure (Section 4.2)
   - Must justify any exclusions (Section 2.4)

6. **Validation checklist:**
   - [ ] All required content per ISO 13485 Clause 4.2.2
   - [ ] Quality Policy signed by top management
   - [ ] All exclusions justified
   - [ ] All procedures listed in Appendix A
   - [ ] Process map included
   - [ ] Organization chart included

#### Creating Procedures (SOPs)

**General approach for all procedures:**

1. **Understand the requirement:**
   - Read relevant clause in `references/iso-13485-requirements.md`
   - Understand WHAT must be documented
   - Identify WHO, WHEN, WHERE for your organization

2. **Use template structure:**
   - Follow CAPA or Document Control templates as examples
   - Standard sections: Purpose, Scope, Definitions, Responsibilities, Procedure, Records, References
   - Keep procedures clear and actionable

3. **Define responsibilities clearly:**
   - Identify specific roles (not names)
   - Define responsibilities for each role
   - Ensure coverage of all required activities

4. **Document the "what" not excessive "how":**
   - Procedures should define WHAT must be done
   - Detailed HOW-TO goes in Work Instructions (Tier 3)
   - Strike balance between guidance and flexibility

5. **Include required elements:**
   - All elements specified in ISO 13485 clause
   - Records that must be maintained
   - Responsibilities for each activity
   - References to related documents

**Example: Creating CAPA Procedure**

1. Read ISO 13485 Clauses 8.5.2 and 8.5.3 from references
2. Use `assets/templates/procedures/CAPA-procedure-template.md`
3. Customize:
   - CAPA prioritization criteria for your organization
   - Root cause analysis methods you'll use
   - Approval authorities and responsibilities
   - Timeframes based on your operations
   - Integration with complaint handling, audits, etc.
4. Add forms as attachments:
   - CAPA Request Form
   - Root Cause Analysis Worksheet
   - Action Plan Template
   - Effectiveness Verification Checklist

#### Creating Medical Device Files (MDF)

**What is an MDF:**
- File for each medical device type or family
- Replaces separate DHF, DMR, DHR (per FDA QMSR harmonization)
- Contains all documentation about the device

**Required contents per ISO 13485 Clause 4.2.3:**

1. General description and intended use
2. Label and instructions for use specifications
3. Product specifications
4. Manufacturing specifications
5. Procedures for purchasing, manufacturing, servicing
6. Procedures for measuring and monitoring
7. Installation requirements (if applicable)
8. Risk management file(s)
9. Verification and validation information
10. Design and development file(s) (when applicable)

**Process:**

1. Identify each device type or family
2. Create MDF structure (folder or binder)
3. Collect or create each required element
4. Ensure traceability between documents
5. Maintain as living document (update with changes)

### 5. Conduct Comprehensive Gap Analysis

**When to use:** User wants detailed assessment of all requirements

**Process:**

1. **Use comprehensive checklist:**
   - Open `references/gap-analysis-checklist.md`
   - Work through clause by clause
   - Mark status for each requirement: Compliant, Partial, Non-compliant, N/A

2. **For each clause:**
   - Read requirement description
   - Identify existing evidence
   - Note gaps or deficiencies
   - Define action required
   - Assign responsibility and target date

3. **Summarize by clause:**
   - Calculate compliance percentage per clause
   - Identify highest-risk gaps
   - Prioritize actions

4. **Create action plan:**
   - List all gaps
   - Prioritize: Critical > High > Medium > Low
   - Assign owners and dates
   - Estimate resources needed

5. **Output:**
   - Completed gap analysis checklist
   - Summary report with compliance percentages
   - Prioritized action plan
   - Timeline and milestones

## Common Scenarios

### Scenario 1: Starting from Scratch

**User request:** "We're a medical device startup and need to implement ISO 13485. Where do we start?"

**Approach:**

1. **Explain the journey:**
   - ISO 13485 requires comprehensive QMS documentation
   - Typically 6-12 months for full implementation
   - Can be done incrementally

2. **Start with foundation:**
   - Quality Policy and Objectives
   - Quality Manual
   - Organization structure and responsibilities

3. **Follow the priority order:**
   - Use Phase 1-6 priority list above
   - Create documents in logical sequence
   - Build on previously created documents

4. **Key milestones:**
   - Month 1-2: Foundation documents (Quality Manual, policies)
   - Month 3-4: Core processes (CAPA, Complaints, Audits)
   - Month 5-6: Product realization processes
   - Month 7-8: Supporting processes
   - Month 9-10: Internal audits and refinement
   - Month 11-12: Management review and certification audit

### Scenario 2: Gap Analysis for Existing QMS

**User request:** "We have some procedures but don't know what we're missing for ISO 13485."

**Approach:**

1. **Run automated gap analysis:**
   - Ask for document directory
   - Run `scripts/gap_analyzer.py`
   - Review automated findings

2. **Conduct detailed assessment:**
   - Use comprehensive checklist for user's specific situation
   - Go deeper than automated analysis
   - Assess quality of existing documents, not just presence

3. **Provide prioritized gap list:**
   - Missing mandatory procedures
   - Incomplete procedures
   - Quality issues with existing documents
   - Missing records or forms

4. **Create remediation plan:**
   - High priority: Safety-related, regulatory-required
   - Medium priority: Core QMS processes
   - Low priority: Improvement opportunities

### Scenario 3: Creating Specific Document

**User request:** "Help me create a CAPA procedure."

**Approach:**

1. **Explain requirements:**
   - Read ISO 13485 Clauses 8.5.2 and 8.5.3 from references
   - Explain what must be in CAPA procedure
   - Provide examples of good CAPA processes

2. **Use template:**
   - Start with CAPA procedure template
   - Explain each section's purpose
   - Show what needs customization

3. **Gather user-specific info:**
   - How are CAPAs initiated in their organization?
   - Who are the responsible parties?
   - What prioritization criteria make sense?
   - What RCA methods will they use?
   - What are appropriate timeframes?

4. **Create customized procedure:**
   - Replace all placeholders
   - Adapt to user's processes
   - Ensure completeness

5. **Add supporting materials:**
   - CAPA request form
   - RCA worksheets
   - Action plan template
   - Effectiveness verification checklist

### Scenario 4: Updating for Regulatory Changes

**User request:** "We need to update our QMS for FDA QMSR harmonization."

**Approach:**

1. **Explain changes:**
   - FDA 21 CFR Part 820 harmonized with ISO 13485
   - Now called QMSR (effective Feb 2, 2026)
   - Key change: Medical Device File replaces DHF/DMR/DHR

2. **Review current documentation:**
   - Identify documents referencing QSR
   - Find separate DHF, DMR, DHR structures
   - Check for ISO 13485 compliance gaps

3. **Update strategy:**
   - Update references from QSR to QMSR
   - Consolidate DHF/DMR/DHR into Medical Device Files
   - Add any missing ISO 13485 requirements
   - Maintain backward compatibility during transition

4. **Create transition plan:**
   - Update Quality Manual
   - Update MDF procedure
   - Reorganize device history files
   - Train personnel on changes

### Scenario 5: Preparing for Certification Audit

**User request:** "We have our documentation ready. How do we prepare for the certification audit?"

**Approach:**

1. **Conduct readiness assessment:**
   - Use comprehensive gap analysis checklist
   - Review all documentation for completeness
   - Verify records exist for all required items
   - Check for consistent implementation

2. **Pre-audit checklist:**
   - [ ] All 31 procedures documented and approved
   - [ ] Quality Manual complete with all required content
   - [ ] Medical Device Files complete for all products
   - [ ] Internal audit completed with findings addressed
   - [ ] Management review completed
   - [ ] Personnel trained on QMS procedures
   - [ ] Records maintained per retention requirements
   - [ ] CAPA system functional with effectiveness demonstrated
   - [ ] Complaints system operational

3. **Conduct mock audit:**
   - Use ISO 13485 requirements as audit criteria
   - Sample records to verify consistent implementation
   - Interview personnel to verify understanding
   - Identify any non-conformances

4. **Address findings:**
   - Correct any deficiencies
   - Document corrections
   - Verify effectiveness

5. **Final preparation:**
   - Brief management and staff
   - Prepare audit schedule
   - Organize evidence and records
   - Designate escorts and support personnel

## Best Practices

### Document Development

1. **Start at policy level, then add detail:**
   - Quality Manual = policy level
   - Procedures = what, who, when
   - Work Instructions = detailed how-to
   - Forms = data collection

2. **Maintain consistency:**
   - Use same terminology throughout
   - Cross-reference related documents
   - Keep numbering scheme consistent
   - Update all related documents together

3. **Write for your audience:**
   - Clear, simple language
   - Avoid jargon
   - Define technical terms
   - Provide examples where helpful

4. **Make procedures usable:**
   - Action-oriented language
   - Logical flow
   - Clear responsibilities
   - Realistic timeframes

### Exclusions

**When you can exclude:**
- Design and development (if contract manufacturer only)
- Installation (if product requires no installation)
- Servicing (if not offered)
- Sterilization (if non-sterile product)

**Justification requirements:**
- Must be in Quality Manual
- Must explain why excluded
- Cannot exclude if process performed
- Cannot affect ability to provide safe, effective devices

**Example good justification:**
> "Clause 7.3 Design and Development is excluded. ABC Company operates as a contract manufacturer and produces medical devices according to complete design specifications provided by customers. All design activities are performed by the customer and ABC Company has no responsibility for design inputs, outputs, verification, validation, or design changes."

**Example poor justification:**
> "We don't do design." (Too brief, doesn't explain why or demonstrate no impact)

### Common Mistakes to Avoid

1. **Copying ISO 13485 text verbatim**
   - Write in your own words
   - Describe YOUR processes
   - Make it actionable for your organization

2. **Making procedures too detailed**
   - Procedures should be stable
   - Excessive detail belongs in work instructions
   - Balance guidance with flexibility

3. **Creating documents in isolation**
   - Ensure consistency across QMS
   - Cross-reference related documents
   - Build on previously created documents

4. **Forgetting records**
   - Every procedure should specify records
   - Define retention requirements
   - Ensure records actually maintained

5. **Inadequate approval**
   - Quality Manual must be signed by top management
   - All procedures must be properly approved
   - Train staff before documents become effective

## Resources

### scripts/
- `gap_analyzer.py` - Automated tool to analyze existing documentation and identify gaps against ISO 13485 requirements

### references/
- `iso-13485-requirements.md` - Complete breakdown of ISO 13485:2016 requirements clause by clause
- `mandatory-documents.md` - Detailed list of all 31 required procedures plus other mandatory documents
- `gap-analysis-checklist.md` - Comprehensive checklist for detailed gap assessment
- `quality-manual-guide.md` - Step-by-step guide for creating a compliant Quality Manual

### assets/templates/
- `quality-manual-template.md` - Complete template for Quality Manual with all required sections
- `procedures/CAPA-procedure-template.md` - Example CAPA procedure following best practices
- `procedures/document-control-procedure-template.md` - Example document control procedure

## Quick Reference

### The 31 Required Documented Procedures

1. Risk Management (4.1.5)
2. Software Validation (4.1.6)
3. Control of Documents (4.2.4)
4. Control of Records (4.2.5)
5. Internal Communication (5.5.3)
6. Management Review (5.6.1)
7. Human Resources/Competence (6.2)
8. Infrastructure Maintenance (6.3) - when applicable
9. Contamination Control (6.4.2) - when applicable
10. Customer Communication (7.2.3)
11. Design and Development (7.3.1-10) - when applicable
12. Purchasing (7.4.1)
13. Verification of Purchased Product (7.4.3)
14. Production Control (7.5.1)
15. Product Cleanliness (7.5.2) - when applicable
16. Installation (7.5.3) - when applicable
17. Servicing (7.5.4) - when applicable
18. Process Validation (7.5.6) - when applicable
19. Sterilization Validation (7.5.7) - when applicable
20. Product Identification (7.5.8)
21. Traceability (7.5.9)
22. Customer Property (7.5.10) - when applicable
23. Preservation of Product (7.5.11)
24. Control of M&M Equipment (7.6)
25. Feedback (8.2.1)
26. Complaint Handling (8.2.2)
27. Regulatory Reporting (8.2.3)
28. Internal Audit (8.2.4)
29. Process Monitoring (8.2.5)
30. Product Monitoring (8.2.6)
31. Control of Nonconforming Product (8.3)
32. Corrective Action (8.5.2)
33. Preventive Action (8.5.3)

*(Note: Traditional count is "31 procedures" though list shows more because some are conditional)*

### Key Regulatory Requirements

**FDA (United States):**
- 21 CFR Part 820 (now QMSR) - harmonized with ISO 13485 as of Feb 2026
- Device classification determines requirements
- Establishment registration and device listing required

**EU (European Union):**
- MDR 2017/745 (Medical Devices Regulation)
- IVDR 2017/746 (In Vitro Diagnostic Regulation)
- Technical documentation requirements
- CE marking requirements

**Canada:**
- Canadian Medical Devices Regulations (SOR/98-282)
- Device classification system
- Medical Device Establishment License (MDEL)

**Other Regions:**
- Australia TGA, Japan PMDA, China NMPA, etc.
- Often require or recognize ISO 13485 certification

### Document Retention

**Minimum retention:** Lifetime of medical device as defined by organization

**Typical retention periods:**
- Design documents: Life of device + 5-10 years
- Manufacturing records: Life of device
- Complaint records: Life of device + 5-10 years
- CAPA records: 5-10 years minimum
- Calibration records: Retention period of equipment + 1 calibration cycle

**Always comply with applicable regulatory requirements which may specify longer periods.**

---

## Getting Started

**First-time users should:**

1. Read `references/iso-13485-requirements.md` to understand the standard
2. If you have existing documentation, run gap analysis script
3. Create Quality Manual using template and guide
4. Develop procedures in priority order
5. Use comprehensive checklist for final validation

**For specific tasks:**
- Creating Quality Manual → See Section 4 and use quality-manual-guide.md
- Creating CAPA procedure → See Section 4 and use CAPA template
- Gap analysis → See Section 1 and 5
- Understanding requirements → See Section 2

**Need help?** Start by describing your situation: what stage you're at, what you have, and what you need to create.

---

## Reference: Gap Analysis Checklist

# ISO 13485:2016 Gap Analysis Checklist

This comprehensive checklist helps identify gaps between your current Quality Management System and ISO 13485:2016 requirements.

## How to Use This Checklist

**Status Indicators:**
- ✅ **Compliant:** Requirement fully implemented and documented
- ⚠️ **Partial:** Requirement partially implemented, needs improvement
- ❌ **Non-compliant:** Requirement not implemented or documented
- N/A **Not Applicable:** Requirement doesn't apply (must be justified)

**For Each Item:**
1. Assess current status
2. Identify existing documentation
3. Note gaps or deficiencies
4. Prioritize actions needed
5. Assign responsibility and target dates

---

## Clause 4: Quality Management System

### 4.1 General Requirements

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 4.1.1 | QMS established, documented, implemented, and maintained | | | | |
| 4.1.2 | QMS processes identified with sequence and interaction | | | | |
| 4.1.3 | Outsourced processes controlled and documented | | | | |
| 4.1.4 | QMS requirements and applicable regulatory requirements met | | | | |
| 4.1.5 | Risk management requirements documented and maintained | | | | |
| 4.1.6 | Computer software applications validated before use | | | | |

### 4.2 Documentation Requirements

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 4.2.1 | QMS documentation includes policy, manual, procedures, records | | | | |
| 4.2.2 | Quality Manual established with required content | | | | |
| 4.2.2.a | Scope of QMS with justified exclusions | | | | |
| 4.2.2.b | Documented procedures or references | | | | |
| 4.2.2.c | Description of process interactions | | | | |
| 4.2.2.d | Structure of documentation described | | | | |
| 4.2.3 | Medical Device File established for each device type/family | | | | |
| 4.2.3.a | General description and intended use documented | | | | |
| 4.2.3.b | Label and IFU specifications | | | | |
| 4.2.3.c | Product specifications | | | | |
| 4.2.3.d | Manufacturing specifications | | | | |
| 4.2.3.e | Purchasing, manufacturing, servicing procedures | | | | |
| 4.2.3.f | Measurement and monitoring procedures | | | | |
| 4.2.3.g | Installation requirements (if applicable) | | | | |
| 4.2.3.h | Risk management file(s) | | | | |
| 4.2.3.i | Verification and validation information | | | | |
| 4.2.3.j | Design and development file(s) when applicable | | | | |
| 4.2.4 | Control of Documents procedure established | | | | |
| 4.2.4.a | Documents approved before issue | | | | |
| 4.2.4.b | Documents reviewed, updated, and re-approved | | | | |
| 4.2.4.c | Changes and current revision status identified | | | | |
| 4.2.4.d | Relevant versions available at point of use | | | | |
| 4.2.4.e | Documents remain legible and identifiable | | | | |
| 4.2.4.f | External documents controlled | | | | |
| 4.2.4.g | Obsolete documents prevented from unintended use | | | | |
| 4.2.4.h | Obsolete documents identified if retained | | | | |
| 4.2.5 | Control of Records procedure established | | | | |
| 4.2.5.a | Records remain legible, identifiable, and retrievable | | | | |
| 4.2.5.b | Changes to records remain identifiable | | | | |
| 4.2.5.c | Retention time at least device lifetime | | | | |
| 4.2.5.d | Storage, security, integrity, retrieval, disposition defined | | | | |

---

## Clause 5: Management Responsibility

### 5.1 Management Commitment

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.1.a | Importance of meeting requirements communicated | | | | |
| 5.1.b | Quality policy established | | | | |
| 5.1.c | Quality objectives established | | | | |
| 5.1.d | Management reviews conducted | | | | |
| 5.1.e | Resource availability ensured | | | | |

### 5.2 Customer Focus

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.2 | Customer and regulatory requirements determined and met | | | | |

### 5.3 Quality Policy

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.3.a | Policy appropriate to organization | | | | |
| 5.3.b | Includes commitment to meet requirements and maintain effectiveness | | | | |
| 5.3.c | Provides framework for quality objectives | | | | |
| 5.3.d | Communicated and understood within organization | | | | |
| 5.3.e | Reviewed for continuing suitability | | | | |

### 5.4 Planning

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.4.1 | Quality objectives established at relevant functions/levels | | | | |
| 5.4.1 | Objectives measurable and consistent with policy | | | | |
| 5.4.2 | QMS planning meets general requirements and objectives | | | | |
| 5.4.2 | QMS integrity maintained when changes occur | | | | |

### 5.5 Responsibility, Authority and Communication

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.5.1 | Responsibilities and authorities defined and communicated | | | | |
| 5.5.1 | Roles for QMS management, performance, verification documented | | | | |
| 5.5.1 | Interrelation of personnel identified | | | | |
| 5.5.2 | Management representative appointed | | | | |
| 5.5.2.a | Representative ensures QMS processes established and maintained | | | | |
| 5.5.2.b | Representative reports to top management on performance | | | | |
| 5.5.2.c | Representative ensures awareness of requirements | | | | |
| 5.5.3 | Internal communication processes established | | | | |

### 5.6 Management Review

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 5.6.1 | QMS reviewed at planned intervals (at least annually) | | | | |
| 5.6.1 | Review ensures suitability, adequacy, effectiveness | | | | |
| 5.6.1 | Review includes improvement opportunities | | | | |
| 5.6.1 | Records of reviews maintained | | | | |
| 5.6.2 | Review includes audit results | | | | |
| 5.6.2 | Review includes customer feedback | | | | |
| 5.6.2 | Review includes process performance and product conformity | | | | |
| 5.6.2 | Review includes status of corrective and preventive actions | | | | |
| 5.6.2 | Review includes follow-up from previous reviews | | | | |
| 5.6.2 | Review includes changes affecting QMS | | | | |
| 5.6.2 | Review includes recommendations for improvement | | | | |
| 5.6.2 | Review includes new/revised regulatory requirements | | | | |
| 5.6.3 | Review output includes QMS improvements | | | | |
| 5.6.3 | Review output includes product improvements | | | | |
| 5.6.3 | Review output includes resource needs | | | | |
| 5.6.3 | Review output includes changes to maintain effectiveness | | | | |

---

## Clause 6: Resource Management

### 6.1 Provision of Resources

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 6.1 | Resources determined and provided for QMS | | | | |
| 6.1 | Resources provided to meet regulatory and customer requirements | | | | |

### 6.2 Human Resources

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 6.2 | Personnel competent based on education, training, skills, experience | | | | |
| 6.2 | Documented evidence of competence maintained | | | | |

### 6.3 Infrastructure

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 6.3 | Infrastructure determined, provided, and maintained | | | | |
| 6.3.a | Buildings, workspace, and utilities provided | | | | |
| 6.3.b | Process equipment (hardware and software) provided | | | | |
| 6.3.c | Supporting services provided | | | | |
| 6.3 | Maintenance requirements documented (when affecting quality) | | | | |
| 6.3 | Maintenance activity records maintained | | | | |

### 6.4 Work Environment and Contamination Control

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 6.4.1 | Work environment determined and managed | | | | |
| 6.4.1 | Work environment requirements documented | | | | |
| 6.4.2 | Contamination control requirements documented (if applicable) | | | | |
| 6.4.2 | Special arrangements for contaminated product established | | | | |

---

## Clause 7: Product Realization

### 7.1 Planning of Product Realization

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.1.a | Quality objectives and requirements determined | | | | |
| 7.1.b | Need for processes, documentation, and resources determined | | | | |
| 7.1.c | Verification, validation, monitoring, measurement activities determined | | | | |
| 7.1.c | Handling, storage, distribution, traceability determined | | | | |
| 7.1.d | Records to provide evidence of conformity determined | | | | |
| 7.1 | Risk management requirements documented | | | | |
| 7.1 | Risk management records maintained | | | | |

### 7.2 Customer-Related Processes

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.2.1.a | Requirements specified by customer determined | | | | |
| 7.2.1.b | Requirements not stated but necessary determined | | | | |
| 7.2.1.c | Applicable regulatory requirements determined | | | | |
| 7.2.1.d | Additional requirements determined by organization | | | | |
| 7.2.2 | Product requirements reviewed before commitment | | | | |
| 7.2.2 | Requirements defined and documented | | | | |
| 7.2.2 | Differences resolved | | | | |
| 7.2.2 | Ability to meet requirements ensured | | | | |
| 7.2.2 | Records of review and follow-up maintained | | | | |
| 7.2.3 | Arrangements for communication with customers documented | | | | |
| 7.2.3.a | Communication on product information | | | | |
| 7.2.3.b | Communication on inquiry, contract, order handling | | | | |
| 7.2.3.c | Communication on customer feedback including complaints | | | | |
| 7.2.3.d | Communication on advisory notices | | | | |

### 7.3 Design and Development

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.3.1 | Design and development procedures documented | | | | |
| 7.3.1 | Design and development plan documented for each device | | | | |
| 7.3.1 | Design and development files maintained | | | | |
| 7.3.2 | Design and development stages determined | | | | |
| 7.3.2 | Required review, verification, validation determined | | | | |
| 7.3.2 | Responsibilities and authorities defined | | | | |
| 7.3.2 | Resources and interfaces managed | | | | |
| 7.3.2 | Plans updated as design progresses | | | | |
| 7.3.3 | Design inputs determined and recorded | | | | |
| 7.3.3 | Functional, performance, usability, safety requirements included | | | | |
| 7.3.3 | Regulatory requirements and standards included | | | | |
| 7.3.3 | Risk management outputs included | | | | |
| 7.3.3 | Previous similar design information included | | | | |
| 7.3.3 | Inputs reviewed for adequacy | | | | |
| 7.3.4 | Design outputs meet input requirements | | | | |
| 7.3.4 | Outputs provide information for purchasing, production, service | | | | |
| 7.3.4 | Outputs contain acceptance criteria | | | | |
| 7.3.4 | Outputs specify characteristics for safe and proper use | | | | |
| 7.3.4 | Outputs documented and maintained as records | | | | |
| 7.3.5 | Systematic reviews conducted at suitable stages | | | | |
| 7.3.5 | Review evaluates ability to meet requirements | | | | |
| 7.3.5 | Review identifies problems and proposes actions | | | | |
| 7.3.5 | Representatives of functions concerned included | | | | |
| 7.3.5 | Records of reviews and follow-up maintained | | | | |
| 7.3.6 | Verification performed per planned arrangements | | | | |
| 7.3.6 | Verification ensures outputs meet inputs | | | | |
| 7.3.6 | Records of verification and follow-up maintained | | | | |
| 7.3.7 | Validation performed per planned arrangements | | | | |
| 7.3.7 | Validation ensures product meets specified application | | | | |
| 7.3.7 | Validation conducted before delivery or implementation | | | | |
| 7.3.7 | Validation includes defined operating conditions | | | | |
| 7.3.7 | Records of validation and follow-up maintained | | | | |
| 7.3.8 | Transfer procedures documented | | | | |
| 7.3.8 | Manufacturing output verified against design output | | | | |
| 7.3.8 | Specifications appropriate for manufacturing | | | | |
| 7.3.8 | Transfer records maintained | | | | |
| 7.3.9 | Design changes identified, documented, and controlled | | | | |
| 7.3.9 | Changes reviewed, verified, validated, and approved | | | | |
| 7.3.9 | Effects on constituent parts and delivered product evaluated | | | | |
| 7.3.9 | Records of changes and review maintained | | | | |
| 7.3.10 | Design and development files maintained including all required content | | | | |

### 7.4 Purchasing

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.4.1 | Purchased product conforms to purchase information | | | | |
| 7.4.1 | Purchasing activities documented | | | | |
| 7.4.1 | Criteria for supplier evaluation and selection established | | | | |
| 7.4.1 | Criteria based on supplier ability to supply per requirements | | | | |
| 7.4.1 | Supplier performance monitored | | | | |
| 7.4.1 | Records of supplier evaluations and follow-up maintained | | | | |
| 7.4.1 | Process for notifying suppliers of changes established | | | | |
| 7.4.2 | Purchasing information includes product approval requirements | | | | |
| 7.4.2 | Purchasing information includes qualification of personnel | | | | |
| 7.4.2 | Purchasing information includes QMS requirements | | | | |
| 7.4.2 | Purchasing information includes notification requirements | | | | |
| 7.4.2 | Purchasing information includes supplier change notification | | | | |
| 7.4.2 | Purchasing information communicated to sub-tier suppliers | | | | |
| 7.4.3 | Verification activities to ensure purchased product conformity | | | | |
| 7.4.3 | Extent of verification documented | | | | |
| 7.4.3 | Verification at supplier's premises documented (if applicable) | | | | |

### 7.5 Production and Service Provision

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.5.1.a | Documented procedures and work instructions available | | | | |
| 7.5.1.b | Suitable infrastructure and work environment available | | | | |
| 7.5.1.c | Monitoring and measuring equipment available | | | | |
| 7.5.1.d | Monitoring and measuring activities available and used | | | | |
| 7.5.1.e | Product release, delivery, post-delivery activities implemented | | | | |
| 7.5.1.f | Operations for labelling and packaging defined | | | | |
| 7.5.1.g | Procedures for servicing documented (if applicable) | | | | |
| 7.5.1 | Requirements for product cleanliness documented | | | | |
| 7.5.1 | Requirements for installation and verification documented | | | | |
| 7.5.2 | Cleanliness requirements documented (if applicable) | | | | |
| 7.5.2 | Hygiene requirements in manufacturing documented | | | | |
| 7.5.3 | Installation requirements documented (if applicable) | | | | |
| 7.5.3 | Verification of installation conducted | | | | |
| 7.5.3 | Records of installation and verification maintained | | | | |
| 7.5.4 | Servicing procedures documented (if applicable) | | | | |
| 7.5.4 | Servicing records analyzed for feedback | | | | |
| 7.5.4 | Records of servicing maintained | | | | |
| 7.5.5 | Records of sterilization process parameters maintained (if applicable) | | | | |
| 7.5.6 | Processes validated where output cannot be verified | | | | |
| 7.5.6 | Defined criteria for review and approval | | | | |
| 7.5.6 | Equipment approval and personnel qualification | | | | |
| 7.5.6 | Specific methods, procedures, and acceptance criteria used | | | | |
| 7.5.6 | Requirements for records defined | | | | |
| 7.5.6 | Revalidation criteria defined | | | | |
| 7.5.6 | Software validation for production documented | | | | |
| 7.5.6 | Sterilization process validation documented (if applicable) | | | | |
| 7.5.6 | Aseptic processing validation documented (if applicable) | | | | |
| 7.5.6 | Clean room validation documented (if applicable) | | | | |
| 7.5.7 | Sterilization process validation records maintained (if applicable) | | | | |
| 7.5.7 | Sterile barrier system validation records maintained (if applicable) | | | | |
| 7.5.8 | Product identification procedures documented | | | | |
| 7.5.8 | Product identified by suitable means throughout realization | | | | |
| 7.5.8 | Records of identification maintained where traceability required | | | | |
| 7.5.9.1 | Traceability extent defined and documented | | | | |
| 7.5.9.1 | Distribution and location documented | | | | |
| 7.5.9.2 | Consignee name and address recorded | | | | |
| 7.5.9.2 | Quantity shipped recorded | | | | |
| 7.5.9.2 | Regulatory traceability requirements included | | | | |
| 7.5.9.2 | Traceability records maintained for defined period | | | | |
| 7.5.10 | Customer property identified, verified, protected (if applicable) | | | | |
| 7.5.10 | Loss, damage, unsuitability reported to customer | | | | |
| 7.5.10 | Records of customer property maintained | | | | |
| 7.5.11 | Product preservation during processing and delivery | | | | |
| 7.5.11 | Identification, handling, packaging, storage, protection included | | | | |
| 7.5.11 | Preservation applies to constituent parts | | | | |
| 7.5.11 | Special handling requirements documented (if applicable) | | | | |

### 7.6 Control of Monitoring and Measuring Equipment

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 7.6 | Monitoring and measurement to be undertaken determined | | | | |
| 7.6 | Monitoring and measuring equipment needed determined | | | | |
| 7.6.a | Calibration or verification at specified intervals | | | | |
| 7.6.b | Adjustment or re-adjustment as necessary | | | | |
| 7.6.c | Identification to determine calibration status | | | | |
| 7.6.d | Safeguarding from adjustments invalidating calibration | | | | |
| 7.6.e | Protection from damage and deterioration | | | | |
| 7.6 | Validity of previous results assessed when non-conforming | | | | |
| 7.6 | Records of calibration and verification maintained | | | | |
| 7.6 | Computer software confirmed for intended application | | | | |
| 7.6 | Software confirmation before initial use and reconfirmation | | | | |

---

## Clause 8: Measurement, Analysis and Improvement

### 8.1 General

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 8.1 | Monitoring, measurement, analysis, improvement processes planned | | | | |
| 8.1 | Product conformity demonstrated | | | | |
| 8.1 | QMS conformity ensured | | | | |
| 8.1 | QMS effectiveness maintained | | | | |
| 8.1 | Applicable methods including statistical techniques determined | | | | |

### 8.2 Monitoring and Measurement

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 8.2.1 | Feedback procedure established | | | | |
| 8.2.1 | Early warning system for quality issues established | | | | |
| 8.2.1 | Post-production information collected | | | | |
| 8.2.1 | Requirements for regulatory reporting included | | | | |
| 8.2.1 | Feedback used as input to risk management | | | | |
| 8.2.1 | Feedback used as input to corrective/preventive action | | | | |
| 8.2.2 | Complaint handling procedure established | | | | |
| 8.2.2 | Requirements for receiving, recording, evaluating complaints | | | | |
| 8.2.2 | Requirements for handling, investigating complaints | | | | |
| 8.2.2 | Requirements for reporting to regulatory authorities | | | | |
| 8.2.2 | Requirements for informing customer of actions | | | | |
| 8.2.2 | Complaint information transferred to organization | | | | |
| 8.2.2 | Records of complaints and investigations maintained | | | | |
| 8.2.3 | Regulatory reporting procedure established | | | | |
| 8.2.3 | Notification to regulatory authorities per requirements | | | | |
| 8.2.3 | Advisory notices per applicable requirements | | | | |
| 8.2.3 | Records of reporting maintained | | | | |
| 8.2.4 | Internal audits conducted at planned intervals | | | | |
| 8.2.4 | QMS conformity to ISO 13485 and requirements determined | | | | |
| 8.2.4 | QMS effective implementation and maintenance determined | | | | |
| 8.2.4 | Audit program considers importance, changes, previous results | | | | |
| 8.2.4 | Audit criteria, scope, frequency, methods defined | | | | |
| 8.2.4 | Audit procedure includes responsibilities and reporting | | | | |
| 8.2.4 | Objective and impartial auditors selected | | | | |
| 8.2.4 | Records of audits and results maintained | | | | |
| 8.2.4 | Need for corrections or corrective actions identified | | | | |
| 8.2.4 | Follow-up activities conducted | | | | |
| 8.2.5 | Suitable methods for process monitoring and measurement | | | | |
| 8.2.5 | Ability to achieve planned results demonstrated | | | | |
| 8.2.5 | Corrections and corrective actions implemented when needed | | | | |
| 8.2.5 | Records maintained | | | | |
| 8.2.6 | Product characteristics monitored and measured | | | | |
| 8.2.6 | Conducted at appropriate stages per planned arrangements | | | | |
| 8.2.6 | Records show conformity to acceptance criteria | | | | |
| 8.2.6 | Authority responsible for release recorded | | | | |
| 8.2.6 | Release and delivery not proceed until arrangements completed | | | | |

### 8.3 Control of Nonconforming Product

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 8.3.1 | Nonconforming product identified and controlled | | | | |
| 8.3.1 | Procedure for identification, documentation established | | | | |
| 8.3.1 | Procedure for evaluation, segregation, disposition established | | | | |
| 8.3.1 | Procedure for notification to external parties established | | | | |
| 8.3.1 | Review of nonconforming product conducted | | | | |
| 8.3.1 | Records of nonconformities and actions maintained | | | | |
| 8.3.2 | Action taken to eliminate detected nonconformity | | | | |
| 8.3.2 | Use under concession authorized (if applicable) | | | | |
| 8.3.2 | Action taken to preclude original intended use | | | | |
| 8.3.2 | Records of concessions maintained | | | | |
| 8.3.2 | Authority making concession identified | | | | |
| 8.3.3 | Appropriate action for nonconformity after delivery | | | | |
| 8.3.3 | Procedure includes regulatory notification requirements | | | | |
| 8.3.3 | Records maintained | | | | |
| 8.3.4 | Rework procedures documented | | | | |
| 8.3.4 | Potential effects on medical device evaluated | | | | |
| 8.3.4 | Approval before rework implementation | | | | |
| 8.3.4 | Records of results and actions maintained | | | | |
| 8.3.4 | Re-verification after rework | | | | |
| 8.3.4 | Rework procedure documented before beginning | | | | |

### 8.4 Analysis of Data

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 8.4 | Appropriate data determined, collected, and analyzed | | | | |
| 8.4 | Continual improvement opportunities evaluated | | | | |
| 8.4 | Procedures for data analysis established | | | | |
| 8.4.a | Analysis provides information on customer satisfaction | | | | |
| 8.4.b | Analysis of conformity to product requirements | | | | |
| 8.4.c | Analysis of process and product characteristics and trends | | | | |
| 8.4.d | Analysis of suppliers | | | | |
| 8.4.e | Analysis of feedback and risk management outputs | | | | |
| 8.4 | Statistical techniques used if necessary | | | | |
| 8.4 | Records of analysis results maintained | | | | |

### 8.5 Improvement

| # | Requirement | Status | Evidence | Gaps | Action Required |
|---|------------|--------|----------|------|-----------------|
| 8.5.1 | Changes identified and implemented to ensure effectiveness | | | | |
| 8.5.1 | Quality policy, objectives, audits, data, CAPA, reviews used | | | | |
| 8.5.2 | Corrective action procedure established | | | | |
| 8.5.2.a | Nonconformities including complaints reviewed | | | | |
| 8.5.2.b | Causes of nonconformities determined | | | | |
| 8.5.2.c | Need for actions to prevent recurrence evaluated | | | | |
| 8.5.2.d | Actions needed planned, documented, and implemented | | | | |
| 8.5.2.e | Results of actions documented | | | | |
| 8.5.2.f | Effectiveness of corrective actions reviewed | | | | |
| 8.5.2 | Records of investigation and follow-up maintained | | | | |
| 8.5.3 | Preventive action procedure established | | | | |
| 8.5.3.a | Potential nonconformities and causes determined | | | | |
| 8.5.3.b | Need for action to prevent occurrence evaluated | | | | |
| 8.5.3.c | Actions needed planned, documented, and implemented | | | | |
| 8.5.3.d | Results of actions documented | | | | |
| 8.5.3.e | Effectiveness of preventive actions reviewed | | | | |
| 8.5.3 | Appropriate information sources used | | | | |
| 8.5.3 | Records of investigation and follow-up maintained | | | | |

---

## Summary and Prioritization

### Gap Summary by Clause

| Clause | Total Items | Compliant | Partial | Non-Compliant | N/A | Compliance % |
|--------|-------------|-----------|---------|---------------|-----|--------------|
| 4. QMS | | | | | | |
| 5. Management | | | | | | |
| 6. Resources | | | | | | |
| 7. Product Realization | | | | | | |
| 8. Measurement & Improvement | | | | | | |
| **TOTAL** | | | | | | |

### Priority Actions

**Critical (Immediate Action Required):**
1.
2.
3.

**High Priority (Within 30 days):**
1.
2.
3.

**Medium Priority (Within 90 days):**
1.
2.
3.

**Low Priority (Within 180 days):**
1.
2.
3.

### Resource Requirements

**Personnel:**
-
-

**Training:**
-
-

**Tools/Systems:**
-
-

**External Support:**
-
-

### Timeline and Milestones

| Milestone | Target Date | Responsible | Status |
|-----------|-------------|-------------|--------|
| Gap analysis completion | | | |
| Priority 1 items complete | | | |
| Priority 2 items complete | | | |
| Priority 3 items complete | | | |
| Internal audit readiness | | | |
| Certification audit | | | |

---

## Notes and Additional Considerations

### Regulatory Requirements
Document any additional requirements beyond ISO 13485:
- FDA QMSR requirements
- EU MDR/IVDR requirements
- Health Canada requirements
- Other regional requirements

### Exclusions
Document and justify any clause exclusions:

| Clause | Exclusion | Justification |
|--------|-----------|---------------|
| | | |

### Additional Documentation Needed
List any additional documents identified during gap analysis:
-
-

### Lessons Learned and Best Practices
-
-

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | | | Initial gap analysis |

---

## Reference: Iso 13485 Requirements

# ISO 13485:2016 Requirements Breakdown

This document provides a comprehensive breakdown of ISO 13485:2016 requirements for medical device Quality Management Systems (QMS).

## Table of Contents

1. [Clause 4: Quality Management System](#clause-4-quality-management-system)
2. [Clause 5: Management Responsibility](#clause-5-management-responsibility)
3. [Clause 6: Resource Management](#clause-6-resource-management)
4. [Clause 7: Product Realization](#clause-7-product-realization)
5. [Clause 8: Measurement, Analysis and Improvement](#clause-8-measurement-analysis-and-improvement)

## Clause 4: Quality Management System

### 4.1 General Requirements

#### 4.1.1 QMS Requirements
- Establish, document, implement, and maintain a QMS
- Maintain its effectiveness in accordance with ISO 13485
- Document the QMS processes and their interactions

#### 4.1.2 Process Approach
- Identify processes needed for the QMS
- Determine sequence and interaction of these processes
- Determine criteria and methods for effective operation and control
- Ensure availability of resources and information
- Monitor, measure, and analyze processes
- Implement actions to achieve planned results and maintain effectiveness

#### 4.1.3 Outsourced Processes
- Control any QMS process that is outsourced
- Ensure control is documented in the QMS
- Outsourcing does not relieve the organization of responsibility

#### 4.1.4 General QMS Requirements
- Establish, document, implement, and maintain QMS requirements per ISO 13485
- Include requirements for medical devices and applicable regulatory requirements
- Establish documented procedures for QMS activities

#### 4.1.5 Risk Management
- Establish documented requirements for risk management in product realization
- Maintain risk management records
- Ensure risk management is conducted according to documented requirements

#### 4.1.6 Software Validation
- Validate computer software applications used in QMS
- Validation must be conducted prior to initial use and after changes
- Establish documented approach including:
  - Risk associated with the software application
  - Validation activities
  - Acceptance criteria
  - User responsibilities
  - Validation records

### 4.2 Documentation Requirements

#### 4.2.1 General Documentation
QMS documentation must include:
- Quality policy and quality objectives
- Quality manual
- Documented procedures and records required by ISO 13485
- Documents required by organization for effective processes
- Records required by ISO 13485
- Medical device files as required by applicable regulatory requirements

#### 4.2.2 Quality Manual
Establish and maintain a quality manual that includes:
- Scope of the QMS with details and justification for exclusions
- Documented procedures or reference to them
- Description of interaction between QMS processes
- Structure of documentation used in the QMS

#### 4.2.3 Medical Device File
Establish and maintain a medical device file for each type or family that includes:
- General description, intended use/purpose
- Label and instructions for use specifications
- Specifications for product and/or manufacturing
- Specifications for procedures for purchasing, manufacturing, servicing
- Procedures for measuring and monitoring
- Installation requirements (if applicable)
- Risk management file(s)
- Verification and validation information
- Design and development file(s) when applicable

#### 4.2.4 Control of Documents
Establish documented procedure to:
- Approve documents before issue
- Review, update, and re-approve documents
- Ensure changes and current revision status are identified
- Ensure relevant versions are available at points of use
- Ensure documents remain legible and readily identifiable
- Control distribution of documents
- Prevent unintended use of obsolete documents
- Apply suitable identification if retained for any purpose

Document changes must:
- Be reviewed and approved by original function unless otherwise designated
- Have access to pertinent background information
- Be identified in the document or appropriate attachments

#### 4.2.5 Control of Records
Establish documented procedure for:
- Identification, storage, security, integrity, retrieval, retention time, and disposition
- Records must remain legible, readily identifiable, and retrievable
- Changes to records must remain identifiable
- Retention time must be at least the lifetime of the medical device
- Records may be stored on any media but must remain retrievable

## Clause 5: Management Responsibility

### 5.1 Management Commitment
Top management must provide evidence of commitment by:
- Communicating importance of meeting regulatory and customer requirements
- Establishing quality policy
- Establishing quality objectives
- Conducting management reviews
- Ensuring availability of resources

### 5.2 Customer Focus
- Determine customer requirements and regulatory requirements
- Ensure customer requirements are met to enhance satisfaction
- Maintain documented requirements related to the medical device

### 5.3 Quality Policy
- Appropriate to the organization
- Includes commitment to meet requirements and maintain QMS effectiveness
- Provides framework for quality objectives
- Communicated and understood within organization
- Reviewed for continuing suitability

### 5.4 Planning

#### 5.4.1 Quality Objectives
- Establish quality objectives at relevant functions and levels
- Must be measurable and consistent with quality policy
- Objectives must support conformity to product requirements

#### 5.4.2 QMS Planning
- Plan to meet general requirements and quality objectives
- Maintain QMS integrity when changes are planned and implemented
- Document planning

### 5.5 Responsibility, Authority and Communication

#### 5.5.1 Responsibility and Authority
- Define and communicate responsibilities and authorities
- Document roles that manage, perform, verify QMS work
- Identify interrelation of all personnel

#### 5.5.2 Management Representative
Appoint a member of management who:
- Ensures QMS processes are established, implemented, and maintained
- Reports to top management on QMS performance and improvement needs
- Ensures promotion of awareness of regulatory and customer requirements

#### 5.5.3 Internal Communication
- Ensure communication processes are established
- Ensure communication occurs regarding QMS effectiveness

### 5.6 Management Review

#### 5.6.1 General
- Review QMS at planned intervals (at least annually)
- Review to ensure continuing suitability, adequacy, and effectiveness
- Include assessment of opportunities for improvement
- Maintain records of management reviews

#### 5.6.2 Review Input
Include:
- Results of audits
- Customer feedback
- Process performance and product conformity
- Status of preventive and corrective actions
- Follow-up actions from previous reviews
- Changes affecting QMS
- Recommendations for improvement
- Applicable new or revised regulatory requirements

#### 5.6.3 Review Output
Include decisions and actions related to:
- Improvements to QMS effectiveness and processes
- Product improvements related to customer requirements
- Resource needs
- Changes necessary to maintain QMS effectiveness

## Clause 6: Resource Management

### 6.1 Provision of Resources
Determine and provide resources needed to:
- Implement and maintain QMS and its effectiveness
- Meet regulatory and customer requirements

### 6.2 Human Resources

#### 6.2 General
Personnel performing work affecting product quality must be competent based on:
- Education, training, skills, and experience
- Documented evidence of competence

#### 6.3 Infrastructure
Determine, provide, and maintain infrastructure including:
- Buildings, workspace, and associated utilities
- Process equipment (hardware and software)
- Supporting services

Infrastructure maintenance requirements:
- Document requirements including maintenance activities
- Document requirements when maintenance can affect product quality
- Maintain records of maintenance activities

### 6.4 Work Environment and Contamination Control

#### 6.4.1 Work Environment
- Determine and manage work environment needed for product conformity
- Document requirements for work environment
- Document requirements if work environment can adversely affect product quality

#### 6.4.2 Contamination Control
- When applicable to medical device, document requirements for control of contaminated or potentially contaminated product
- Establish special arrangements for control of contaminated product

## Clause 7: Product Realization

### 7.1 Planning of Product Realization
Plan and develop processes needed for product realization including:
- Quality objectives and requirements for the product
- Need to establish processes, documentation, and resources
- Required verification, validation, monitoring, measurement, inspection, handling, storage, distribution, and traceability
- Records to provide evidence of conformity

Risk management requirements:
- Establish documented requirements for risk management throughout product realization
- Maintain risk management records

### 7.2 Customer-Related Processes

#### 7.2.1 Determination of Requirements
Determine:
- Requirements specified by customer including delivery and post-delivery
- Requirements not stated but necessary for specified or intended use
- Applicable regulatory requirements
- Any additional requirements determined by organization

#### 7.2.2 Review of Requirements
- Review product requirements before commitment
- Ensure requirements are defined and documented
- Ensure differences are resolved
- Ensure ability to meet requirements
- Maintain records of review results and follow-up actions

#### 7.2.3 Communication
Establish and document effective arrangements for communication with customers concerning:
- Product information
- Inquiry, contract or order handling, amendments
- Customer feedback including complaints
- Advisory notices

### 7.3 Design and Development

#### 7.3.1 General
- Establish, document, and maintain design and development procedures
- Document design and development plan for each medical device
- Maintain design and development files

#### 7.3.2 Design and Development Planning
Plan and control design and development including:
- Stages of design and development
- Required review, verification, and validation activities
- Responsibilities and authorities
- Resources and interfaces
- Update plans as design progresses
- Document plans

#### 7.3.3 Design and Development Inputs
- Determine inputs relating to product requirements
- Include functional, performance, usability, and safety requirements
- Include applicable regulatory requirements and standards
- Include applicable outputs of risk management
- Include appropriate information from previous similar designs
- Review inputs for adequacy and completeness
- Resolve incomplete, ambiguous, or conflicting requirements
- Maintain records

#### 7.3.4 Design and Development Outputs
Provide outputs that:
- Meet design input requirements
- Provide appropriate information for purchasing, production, and service
- Contain or reference product acceptance criteria
- Specify characteristics essential for safe and proper use
- Document outputs and maintain as records

#### 7.3.5 Design and Development Review
- Conduct systematic reviews at suitable stages
- Evaluate ability to meet requirements
- Identify problems and propose actions
- Include representatives of functions concerned
- Maintain records including results and follow-up actions

#### 7.3.6 Design and Development Verification
- Perform verification per planned arrangements
- Ensure outputs meet input requirements
- Maintain records of verification results and follow-up actions

#### 7.3.7 Design and Development Validation
- Perform validation per planned arrangements
- Ensure product meets specified application or intended use
- Conduct validation before delivery or implementation
- Include validation under defined operating conditions
- Maintain records of validation results and follow-up actions

#### 7.3.8 Design and Development Transfer
- Document procedures for transfer to manufacturing
- Verify manufacturing output meets design output
- Ensure specification for materials, production, QC, servicing are appropriate
- Maintain records

#### 7.3.9 Control of Design and Development Changes
- Identify, document, and control changes
- Review, verify, validate, and approve changes before implementation
- Evaluate effects on constituent parts, in-process product, and delivered product
- Maintain records of changes, review results, and follow-up actions

#### 7.3.10 Design and Development Files
Establish and maintain design and development files for each type or family including:
- Design and development plan
- Design inputs
- Design outputs
- Design review, verification, validation records
- Design change records
- Risk management file

### 7.4 Purchasing

#### 7.4.1 Purchasing Process
- Ensure purchased product conforms to purchase information
- Establish documented processes for purchasing activities
- Establish criteria for evaluation and selection of suppliers
- Base criteria on ability to supply per organization's requirements
- Monitor supplier performance
- Maintain records of evaluations and follow-up actions
- Establish process for notifying suppliers of changed product requirements

#### 7.4.2 Purchasing Information
Purchasing information must include:
- Requirements for approval of product, procedures, processes, equipment
- Requirements for qualification of personnel
- Quality management system requirements
- Requirements for notification to organization of nonconforming product
- Agreement that suppliers provide notification of changes to purchased product
- Agreement that purchase information be communicated to sub-tier suppliers

#### 7.4.3 Verification of Purchased Product
- Establish and implement inspection or other activities to ensure conformity
- Document extent of verification
- Verify at supplier's premises when customer intends to perform verification at supplier
- Document verification arrangements and method of product release

### 7.5 Production and Service Provision

#### 7.5.1 Control of Production and Service Provision
Plan and carry out production under controlled conditions including:
- Availability of documented procedures and work instructions
- Availability of suitable infrastructure and work environment
- Availability of monitoring and measuring equipment
- Availability and use of suitable monitoring and measuring activities
- Implementation of product release, delivery, and post-delivery activities
- Implementation of defined operations for labelling and packaging
- Procedures for servicing if applicable

Document requirements for:
- Control of product cleanliness if applicable
- Control during installation and verification if applicable

#### 7.5.2 Cleanliness of Product
Document requirements if:
- Product is cleaned per specified requirements before sterilization and/or use
- Product cannot be cleaned before sterilization
- Product is supplied non-sterile to be cleaned and then sterilized

Establish requirements for product hygiene in manufacturing, handling, and storage.

#### 7.5.3 Installation Activities
If applicable:
- Document requirements for installation and verification
- Maintain records of installation and verification

#### 7.5.4 Servicing Activities
If servicing is specified requirement:
- Establish documented procedures, reference materials, and measurements for servicing
- Analyze records of servicing for feedback into post-production phase
- Maintain records of servicing activities

#### 7.5.5 Particular Requirements for Sterile Medical Devices
Maintain records of process parameters for sterilization of each batch.

#### 7.5.6 Validation of Processes
Validate processes where resulting output cannot be verified by subsequent monitoring or measurement, including:
- Defined criteria for review and approval
- Approval of equipment and qualification of personnel
- Use of specific methods, procedures, and acceptance criteria
- Requirements for records
- Revalidation including criteria for revalidation
- Approval of changes to process

Document requirements for validation of:
- Computer software used in production and service provision
- Sterilization processes
- Aseptic processing
- Clean room requirements if applicable

#### 7.5.7 Particular Requirements for Validation of Processes for Sterilization and Sterile Barrier Systems
Maintain records of validation of:
- Sterilization processes for each batch
- Sterile barrier systems

#### 7.5.8 Identification
- Establish documented procedures for product identification throughout realization
- Identify product by suitable means
- Maintain records of identification where traceability is a requirement

#### 7.5.9 Traceability

##### 7.5.9.1 General
Establish documented procedures defining extent of traceability including:
- Distribution and location of medical device

##### 7.5.9.2 Particular Requirements
Document procedures to maintain records of:
- Name and address of shipping package consignee
- Identification of quantity shipped
- Include requirements of applicable regulatory requirements
- Maintain traceability records for defined period

#### 7.5.10 Customer Property
- Exercise care with customer property while under organization's control
- Identify, verify, protect, and safeguard customer property
- Record and report to customer if lost, damaged, or unsuitable
- Maintain records

#### 7.5.11 Preservation of Product
- Preserve product during internal processing and delivery
- Include identification, handling, packaging, storage, and protection
- Apply to constituent parts of product
- Document requirements for special handling if applicable

### 7.6 Control of Monitoring and Measuring Equipment
- Determine monitoring and measurement to be undertaken
- Determine monitoring and measuring equipment needed
- Establish documented procedures for:
  - Calibration or verification at specified intervals before use
  - Adjustment or re-adjustment as necessary
  - Identification to enable determination of calibration status
  - Safeguarding from adjustments that would invalidate calibration
  - Protection from damage and deterioration
- Assess and record validity of previous results when found not to conform
- Maintain records of calibration and verification
- Confirm ability of computer software to satisfy intended application when used
- Undertake confirmation before initial use and reconfirm as necessary

## Clause 8: Measurement, Analysis and Improvement

### 8.1 General
- Plan and implement monitoring, measurement, analysis, and improvement processes
- Demonstrate product conformity
- Ensure QMS conformity
- Maintain QMS effectiveness
- Include determination of applicable methods including statistical techniques

### 8.2 Monitoring and Measurement

#### 8.2.1 Feedback
Establish documented procedure for feedback including early warning system for:
- Post-production information including complaints
- Requirements for reporting to regulatory authorities
- Use as potential input to risk management for monitoring and maintaining product requirements
- Use as potential input for corrective and preventive action

#### 8.2.2 Complaint Handling
Establish documented procedures for timely complaint handling including:
- Requirements and responsibilities for receiving, recording, and evaluating complaints
- Requirements and responsibilities for handling, investigating, and evaluating complaints
- Requirements and responsibilities for reporting complaint information to regulatory authorities
- Requirements for informing customer of organization's actions
- Requirements to ensure complaint information not handled by organization is transferred to organization
- Maintain records of complaints and investigations

#### 8.2.3 Reporting to Regulatory Authorities
Establish documented procedures to:
- Provide notification to regulatory authorities per applicable requirements
- Provide advisory notices per applicable requirements
- Maintain records of reporting

#### 8.2.4 Internal Audit
- Conduct internal audits at planned intervals
- Determine if QMS conforms to ISO 13485 and organization's requirements
- Determine if QMS is effectively implemented and maintained
- Plan audit program considering importance of processes, changes, and previous results
- Define audit criteria, scope, frequency, and methods
- Establish documented procedure for audits including responsibilities, requirements, and reporting
- Select objective and impartial auditors
- Maintain records of audits and results
- Identify need for corrections or corrective actions
- Conduct follow-up activities to verify implementation and effectiveness

#### 8.2.5 Monitoring and Measurement of Processes
- Apply suitable methods for monitoring and measurement of QMS processes
- Demonstrate ability to achieve planned results
- Implement corrections and corrective actions when planned results not achieved
- Maintain records

#### 8.2.6 Monitoring and Measurement of Product
- Monitor and measure product characteristics to verify conformity
- Conduct at appropriate stages per planned arrangements
- Maintain records showing conformity to acceptance criteria
- Record authority responsible for release
- Ensure product release and delivery not proceed until planned arrangements completed
- Allow release by relevant authority and customer when applicable

### 8.3 Control of Nonconforming Product

#### 8.3.1 General
- Ensure nonconforming product is identified and controlled
- Establish documented procedures for:
  - Identification, documentation, evaluation, segregation, and disposition
  - Notification to external parties
  - Review of nonconforming product
- Maintain records of nonconformities and subsequent actions including concessions

#### 8.3.2 Actions in Response to Nonconforming Product Detected Before Delivery
Deal with nonconforming product by:
- Taking action to eliminate detected nonconformity
- Authorizing use, release, or acceptance under concession per applicable regulatory requirements
- Taking action to preclude original intended use or application
- Taking action appropriate to effects of nonconformity when detected after delivery or use

Maintain records of concessions and identify authority making concession.

#### 8.3.3 Actions in Response to Nonconforming Product Detected After Delivery
When nonconforming product detected after delivery or use:
- Take action appropriate to effects of nonconformity
- Establish documented procedure including notification requirements to regulatory authorities
- Maintain records

#### 8.3.4 Rework
Establish documented procedures for rework including:
- Requirements to evaluate potential effects on medical device
- Approval before implementation
- Records of results and actions including nonconformities and rework
- Re-verification after rework
- Documentation of rework procedure before rework begins

### 8.4 Analysis of Data
- Determine, collect, and analyze appropriate data from monitoring and measurement
- Evaluate where continual improvement of QMS effectiveness can be made
- Establish documented procedures for:
  - Analysis of data to provide information on customer satisfaction
  - Analysis of conformity to product requirements
  - Analysis of characteristics and trends of processes and products including preventive action opportunities
  - Analysis of suppliers
  - Analysis of other relevant data including feedback and output from risk management
- Include use of statistical techniques if necessary
- Maintain records of analysis results

### 8.5 Improvement

#### 8.5.1 General
- Identify and implement changes to ensure and maintain QMS effectiveness
- Include use of quality policy, objectives, audit results, data analysis, corrective and preventive actions, and management review

#### 8.5.2 Corrective Action
- Establish documented procedures to:
  - Review nonconformities including complaints
  - Determine causes of nonconformities
  - Evaluate need for actions to ensure nonconformities do not recur
  - Plan and document actions needed and implement
  - Document results of actions taken
  - Review effectiveness of corrective actions taken
- Maintain records including investigation results and follow-up

#### 8.5.3 Preventive Action
- Establish documented procedures to:
  - Determine potential nonconformities and their causes
  - Evaluate need for action to prevent occurrence
  - Plan and document actions needed and implement
  - Document results of actions taken
  - Review effectiveness of preventive actions taken
- Use appropriate sources of information including:
  - Work processes and operations affecting product quality
  - Concessions
  - Analysis of data and risk management outputs
  - Medical device performance data
  - Records of nonconformities
- Maintain records including investigation results and follow-up

## Key Regulatory Updates

### FDA QMSR Harmonization (Effective February 2, 2026)
- FDA 21 CFR Part 820 has been harmonized with ISO 13485:2016
- Renamed to QMSR (Quality Management System Regulation)
- Medical Device File (MDF) replaces separate DHF, DMR, and DHR
- Organizations should prepare for transition to unified documentation approach

## References and Resources

This requirements breakdown is based on ISO 13485:2016, which was last reviewed and confirmed in 2025.

For additional guidance, refer to:
- ISO 13485:2016 standard document
- FDA Quality Management System Regulation (QMSR)
- Applicable regional regulatory requirements (EU MDR, Health Canada, etc.)

---

## Reference: Mandatory Documents

# ISO 13485:2016 Mandatory Documents and Records

This document provides a complete list of all mandatory documents and records required by ISO 13485:2016 for medical device Quality Management Systems.

## Overview

ISO 13485:2016 requires organizations to establish and maintain **31 documented procedures** along with a **Quality Manual** and **Medical Device Files**. Additionally, numerous **records** must be maintained to provide evidence of conformity.

**Important Notes:**
- The 31 documented procedures do not need to be 31 separate documents
- Multiple procedures can be combined into one document
- One procedure can be split across multiple documents
- Not all procedures may be applicable to every organization (exclusions must be justified)
- Additional documentation may be required by applicable regulatory requirements

## 1. Quality Manual (Required by 4.2.2)

**Description:** Foundational QMS document

**Must Include:**
- Scope of QMS with justified exclusions
- Documented procedures or references to them
- Description of interaction between QMS processes
- Structure of documentation used in QMS

**Applicable To:** All organizations

---

## 2. Medical Device File (Required by 4.2.3)

**Description:** File for each medical device type or family

**Must Include:**
- General description and intended use
- Label and instructions for use specifications
- Product and/or manufacturing specifications
- Procedures for purchasing, manufacturing, servicing
- Measuring and monitoring procedures
- Installation requirements (if applicable)
- Risk management file(s)
- Verification and validation information
- Design and development file(s) when applicable

**Applicable To:** All organizations for each device type/family

---

## 3. The 31 Documented Procedures

### Clause 4: Quality Management System

#### 1. Risk Management Procedures (4.1.5)
**Description:** Requirements for risk management throughout product realization
**Must Address:**
- Risk management methodology
- Risk analysis and evaluation
- Risk control measures
- Risk acceptability criteria
- Risk management review
**Referenced Standard:** ISO 14971

#### 2. Software Validation Procedure (4.1.6)
**Description:** Validation of computer software applications used in QMS
**Must Address:**
- Risk assessment of software
- Validation approach and activities
- Acceptance criteria
- User responsibilities
- Validation before initial use and after changes
- Revalidation criteria

#### 3. Control of Documents Procedure (4.2.4)
**Description:** Control of all QMS documents
**Must Address:**
- Document approval before issue
- Document review and update
- Identification of changes and revision status
- Availability of relevant document versions
- Document legibility and identification
- Control of external documents
- Prevention of obsolete document use
- Identification of retained obsolete documents

#### 4. Control of Records Procedure (4.2.5)
**Description:** Control of all QMS records
**Must Address:**
- Record identification
- Storage and security
- Integrity protection
- Retrieval procedures
- Retention time determination
- Record disposition
- Legibility requirements
- Change identification

### Clause 5: Management Responsibility

#### 5. Management Review Procedure (5.6.1)
**Description:** Systematic review of QMS by top management
**Must Address:**
- Review frequency (at least annually)
- Review agenda and inputs
- Review outputs and actions
- Attendee requirements
- Record-keeping requirements

#### 6. Internal Communication Procedure (5.5.3)
**Description:** Communication regarding QMS effectiveness
**Must Address:**
- Communication channels
- Communication frequency
- Responsible parties
- Topics to be communicated
- Documentation of communications

### Clause 6: Resource Management

#### 7. Human Resources/Competence Procedure (6.2)
**Description:** Ensuring personnel competence
**Must Address:**
- Competence requirements determination
- Training needs identification
- Training provision and evaluation
- Education, training, skills, and experience requirements
- Competence records maintenance
- Awareness of personnel contributions

#### 8. Infrastructure Maintenance Procedure (6.3)
**Description:** Maintenance of facilities and equipment (when affecting quality)
**Must Address:**
- Maintenance activities definition
- Maintenance scheduling
- Maintenance records
- Impact on product quality
- Verification after maintenance

#### 9. Contamination Control Procedure (6.4.2)
**Description:** Control of contaminated or potentially contaminated product (when applicable)
**Must Address:**
- Contamination identification
- Contaminated product handling
- Segregation requirements
- Decontamination procedures
- Special arrangements for control

### Clause 7: Product Realization

#### 10. Customer Communication Procedure (7.2.3)
**Description:** Communication with customers
**Must Address:**
- Product information provision
- Inquiry, contract, order handling
- Customer feedback including complaints
- Advisory notices
- Communication channels and responsibilities

#### 11. Design and Development Procedures (7.3.1 - 7.3.10)
**Description:** Control of design and development process
**Must Address:**
- Design and development planning
- Input determination and review
- Output provision and approval
- Design reviews at suitable stages
- Verification against inputs
- Validation for intended use
- Transfer to manufacturing
- Change control
- Design file maintenance

#### 12. Purchasing Procedures (7.4.1)
**Description:** Control of purchasing process
**Must Address:**
- Supplier evaluation and selection criteria
- Supplier monitoring and re-evaluation
- Supplier performance tracking
- Purchasing controls
- Supplier notification of changes
- Communication to sub-tier suppliers

#### 13. Verification of Purchased Product Procedure (7.4.3)
**Description:** Verification that purchased product meets requirements
**Must Address:**
- Verification activities
- Extent of verification
- Method of product release
- Verification at supplier's premises (if applicable)
- Customer verification arrangements (if applicable)

#### 14. Production and Service Provision Control Procedures (7.5.1)
**Description:** Control of production and service activities
**Must Address:**
- Work instructions and documented procedures
- Use of suitable equipment
- Monitoring and measuring activities
- Release, delivery, and post-delivery activities
- Labelling and packaging operations
- Servicing procedures (if applicable)

#### 15. Product Cleanliness Procedures (7.5.2)
**Description:** Control of product cleanliness (when applicable)
**Must Address:**
- Cleaning requirements and specifications
- Cleaning before sterilization
- Uncleanable product handling
- Hygiene requirements in manufacturing
- Cleaning verification

#### 16. Installation and Verification Procedures (7.5.3)
**Description:** Installation activities (when applicable)
**Must Address:**
- Installation requirements
- Installation instructions
- Verification of installation
- Installation records
- Responsible parties

#### 17. Servicing Procedures (7.5.4)
**Description:** Servicing activities (when applicable)
**Must Address:**
- Servicing requirements
- Reference materials and measurements
- Feedback analysis from servicing
- Servicing records
- Servicing notification to regulatory authorities

#### 18. Process Validation Procedure (7.5.6)
**Description:** Validation of processes where output cannot be verified
**Must Address:**
- Process validation for manufacturing
- Computer software validation for production
- Sterilization process validation
- Aseptic processing validation
- Clean room validation (if applicable)
- Criteria for review and approval
- Equipment approval and personnel qualification
- Revalidation criteria and triggers

#### 19. Sterilization and Sterile Barrier System Validation (7.5.7)
**Description:** Validation of sterilization processes (when applicable)
**Must Address:**
- Sterilization method validation
- Sterile barrier system validation
- Process parameters for each batch
- Validation of changes to sterilization
- Maintenance of validation records

#### 20. Product Identification and Traceability Procedures (7.5.8, 7.5.9)
**Description:** Identification and traceability throughout realization
**Must Address:**
- Identification methods throughout realization
- Traceability extent definition
- Distribution and location tracking
- Consignee identification
- Quantity shipped identification
- Retention period requirements
- Applicable regulatory traceability requirements

#### 21. Customer Property Procedure (7.5.10)
**Description:** Control of customer-provided property
**Must Address:**
- Customer property identification
- Verification of customer property
- Protection and safeguarding
- Loss, damage, or unsuitability reporting
- Records of customer property

#### 22. Preservation of Product Procedure (7.5.11)
**Description:** Product preservation during processing and delivery
**Must Address:**
- Identification requirements
- Handling requirements
- Packaging requirements
- Storage requirements
- Protection requirements
- Special handling (if applicable)
- Application to constituent parts

#### 23. Control of Monitoring and Measuring Equipment Procedure (7.6)
**Description:** Calibration and control of measuring equipment
**Must Address:**
- Equipment identification
- Calibration or verification intervals
- Calibration methods and standards
- Adjustment procedures
- Identification of calibration status
- Protection from invalid adjustments
- Protection from damage
- Assessment when found non-conforming
- Computer software confirmation

### Clause 8: Measurement, Analysis and Improvement

#### 24. Feedback Procedure (8.2.1)
**Description:** Post-production information system
**Must Address:**
- Early warning system for quality issues
- Post-production information collection
- Complaint handling linkage
- Reporting to regulatory authorities
- Input to risk management
- Input to corrective and preventive action
- Feedback sources and channels

#### 25. Complaint Handling Procedure (8.2.2)
**Description:** Timely handling of complaints
**Must Address:**
- Complaint receipt and recording
- Complaint evaluation and investigation
- Determination of need for reporting to authorities
- Determination of need for advisory notices
- Information to customer about actions taken
- Transfer of complaint information not directly handled
- Complaint trending and analysis

#### 26. Reporting to Regulatory Authorities Procedure (8.2.3)
**Description:** Notification to regulatory authorities
**Must Address:**
- Determination of reportable events
- Notification timeframes
- Notification content requirements
- Advisory notice requirements
- Applicable regulatory requirements by region
- Responsible parties for reporting

#### 27. Internal Audit Procedure (8.2.4)
**Description:** Conduct of internal audits
**Must Address:**
- Audit program planning
- Audit criteria, scope, frequency, methods
- Auditor selection and impartiality
- Audit responsibilities and requirements
- Audit reporting
- Records of audits
- Follow-up activities

#### 28. Process Monitoring and Measurement Procedures (8.2.5)
**Description:** Monitoring and measurement of QMS processes
**Must Address:**
- Process monitoring methods
- Process measurement methods
- Demonstration of achieving planned results
- Implementation of corrections when needed
- Corrective actions when processes fail

#### 29. Product Monitoring and Measurement Procedures (8.2.6)
**Description:** Monitoring and measurement of product
**Must Address:**
- Product acceptance criteria
- Measurement at appropriate stages
- Release authority identification
- Release procedures
- Records of conformity to criteria
- Traceability to measuring authority

#### 30. Control of Nonconforming Product Procedure (8.3)
**Description:** Identification and control of nonconforming product
**Must Address:**
- Identification of nonconformity
- Documentation requirements
- Evaluation of nonconformity
- Segregation of nonconforming product
- Disposition of nonconforming product
- Notification to external parties
- Concession process (if applicable)
- Rework procedures
- Actions for nonconformity detected before delivery
- Actions for nonconformity detected after delivery
- Reporting requirements

#### 31A. Corrective Action Procedure (8.5.2)
**Description:** Elimination of causes of nonconformities
**Must Address:**
- Review of nonconformities including complaints
- Cause determination methodology
- Evaluation of need for action
- Planning and documentation of actions
- Implementation of actions
- Effectiveness review of actions
- Records of investigation and follow-up

#### 31B. Preventive Action Procedure (8.5.3)
**Description:** Elimination of causes of potential nonconformities
**Must Address:**
- Determination of potential nonconformities
- Evaluation of need for action
- Planning and documentation of actions
- Implementation of actions
- Effectiveness review of actions
- Sources of information for preventive action
- Records of investigation and follow-up

---

## Additional Required Documentation

### Analysis of Data Procedure (8.4)
While not explicitly called out as requiring a "documented procedure," organizations must establish processes for:
- Data determination, collection, and analysis
- Evaluation of continual improvement opportunities
- Statistical techniques (if applicable)
- Analysis of:
  - Customer satisfaction
  - Conformity to product requirements
  - Process and product characteristics and trends
  - Suppliers
  - Other relevant data including feedback and risk management outputs

---

## Required Records by Clause

### Clause 4 Records
- Software validation records (4.1.6)
- Risk management records (4.1.5)
- All records specified in documented procedures and work instructions
- All records required by applicable regulatory requirements

### Clause 5 Records
- Management review records (5.6.1)
- Evidence of personnel competence (6.2)

### Clause 6 Records
- Infrastructure maintenance records (6.3)
- Personnel training and competence records (6.2)

### Clause 7 Records
- Product requirements review and follow-up actions (7.2.2)
- Design and development files (7.3.10) including:
  - Design and development plans
  - Design inputs
  - Design outputs
  - Design review records
  - Design verification records
  - Design validation records
  - Design change records
  - Risk management file
- Design and development transfer records (7.3.8)
- Supplier evaluation, selection, and monitoring (7.4.1)
- Verification of purchased product (7.4.3)
- Cleanliness of product records (7.5.2)
- Installation and verification records (7.5.3)
- Servicing activity records (7.5.4)
- Sterilization process parameter records for each batch (7.5.5, 7.5.7)
- Process validation records (7.5.6)
- Product identification and traceability records (7.5.8, 7.5.9)
  - Including distribution records with consignee name/address and quantity (7.5.9.2)
- Customer property records (7.5.10)
- Calibration and verification records (7.6)

### Clause 8 Records
- Post-production feedback and complaints (8.2.1, 8.2.2)
- Complaint investigations (8.2.2)
- Regulatory authority reporting (8.2.3)
- Internal audit records (8.2.4)
- Process monitoring and measurement results (8.2.5)
- Product monitoring and measurement records (8.2.6)
- Product release authority (8.2.6)
- Nonconforming product records (8.3.1)
- Concession records and authority (8.3.2)
- Nonconforming product actions after delivery (8.3.3)
- Rework procedures and results (8.3.4)
- Data analysis results (8.4)
- Corrective action records including investigation and follow-up (8.5.2)
- Preventive action records including investigation and follow-up (8.5.3)

---

## Documentation Matrix

| Clause | Document Type | Document Name | Mandatory? | Records Required? |
|--------|--------------|---------------|------------|-------------------|
| 4.2.2 | Manual | Quality Manual | Yes | No |
| 4.2.3 | File | Medical Device File | Yes (per device) | Yes |
| 4.1.5 | Procedure | Risk Management | Yes | Yes |
| 4.1.6 | Procedure | Software Validation | Yes | Yes |
| 4.2.4 | Procedure | Control of Documents | Yes | No |
| 4.2.5 | Procedure | Control of Records | Yes | No |
| 5.5.3 | Procedure | Internal Communication | Yes | No |
| 5.6.1 | Procedure | Management Review | Yes | Yes |
| 6.2 | Procedure | Competence/Training | Yes | Yes |
| 6.3 | Procedure | Infrastructure Maintenance | When applicable | Yes |
| 6.4.2 | Procedure | Contamination Control | When applicable | Yes |
| 7.2.3 | Procedure | Customer Communication | Yes | Yes |
| 7.3.1-10 | Procedures | Design and Development | When applicable | Yes |
| 7.4.1 | Procedure | Purchasing | Yes | Yes |
| 7.4.3 | Procedure | Verification of Purchased Product | Yes | Yes |
| 7.5.1 | Procedures | Production Control | Yes | Yes |
| 7.5.2 | Procedure | Product Cleanliness | When applicable | Yes |
| 7.5.3 | Procedure | Installation | When applicable | Yes |
| 7.5.4 | Procedure | Servicing | When applicable | Yes |
| 7.5.6 | Procedure | Process Validation | When applicable | Yes |
| 7.5.7 | Procedure | Sterilization Validation | When applicable | Yes |
| 7.5.8 | Procedure | Product Identification | Yes | Yes |
| 7.5.9 | Procedure | Traceability | Yes | Yes |
| 7.5.10 | Procedure | Customer Property | When applicable | Yes |
| 7.5.11 | Procedure | Preservation of Product | Yes | Yes |
| 7.6 | Procedure | Control of M&M Equipment | Yes | Yes |
| 8.2.1 | Procedure | Feedback | Yes | Yes |
| 8.2.2 | Procedure | Complaint Handling | Yes | Yes |
| 8.2.3 | Procedure | Regulatory Reporting | Yes | Yes |
| 8.2.4 | Procedure | Internal Audit | Yes | Yes |
| 8.2.5 | Procedure | Process Monitoring | Yes | Yes |
| 8.2.6 | Procedure | Product Monitoring | Yes | Yes |
| 8.3 | Procedure | Control of Nonconforming Product | Yes | Yes |
| 8.4 | Process | Analysis of Data | Yes | Yes |
| 8.5.2 | Procedure | Corrective Action | Yes | Yes |
| 8.5.3 | Procedure | Preventive Action | Yes | Yes |

---

## Common Additional Documents (Not Required by ISO 13485 but Often Needed)

While not explicitly required by ISO 13485, the following documents are commonly needed for effective QMS operation and regulatory compliance:

### Work Instructions
- Manufacturing work instructions
- Testing work instructions
- Inspection work instructions
- Cleaning instructions
- Equipment operation instructions

### Forms and Templates
- Training records forms
- Calibration forms
- Audit checklists
- Complaint forms
- CAPA forms
- Change request forms
- Document review forms
- Supplier evaluation forms

### Additional Plans
- Quality plan
- Product realization plan
- Validation plans
- Clinical evaluation plans
- Post-market surveillance plans

### Technical Documentation
- Product specifications
- Material specifications
- Test methods and protocols
- Packaging specifications
- Labeling artwork
- Instructions for use

### Regulatory Documentation
- Technical files (EU MDR/IVDR)
- 510(k) submissions (FDA)
- Clinical evaluation reports
- Post-market surveillance reports
- Periodic safety update reports

---

## Tips for Document Management

### Combining Procedures
Multiple procedures can be combined into single documents, such as:
- "Corrective and Preventive Action (CAPA) Procedure" (combines 8.5.2 and 8.5.3)
- "Document and Record Control Procedure" (combines 4.2.4 and 4.2.5)
- "Monitoring and Measurement Procedure" (combines 8.2.5 and 8.2.6)
- "Product Identification and Traceability Procedure" (combines 7.5.8 and 7.5.9)

### Determining Applicability
Not all procedures apply to all organizations. Common exclusions include:
- Design and development (when only manufacturing per customer specifications)
- Installation (when product doesn't require installation)
- Servicing (when not offered)
- Sterilization (when product is non-sterile)
- Contamination control (when not applicable to product type)

All exclusions must be justified in the Quality Manual.

### Regulatory Requirements
Remember that applicable regulatory requirements may mandate additional documentation beyond ISO 13485, including:
- FDA regulations (21 CFR Part 820 / QMSR)
- EU MDR/IVDR requirements
- Health Canada requirements
- Other regional regulatory requirements

---

## Record Retention

Per ISO 13485:2016 (4.2.5), records must be retained for:
- **Minimum:** The lifetime of the medical device as defined by the organization
- **Additional:** Not less than the retention period of any resulting record
- **Regulatory:** As specified by applicable regulatory requirements

Organizations must define the "lifetime" of their medical devices and establish retention times that meet or exceed:
- ISO 13485 minimum requirements
- Applicable regulatory requirements (often 5-10 years minimum)
- Any customer contractual requirements

---

## Transition to Medical Device File (MDF)

With FDA QMSR harmonization (effective February 2, 2026), organizations should prepare for transitioning from separate files to a unified Medical Device File (MDF) that replaces:
- **DHF** (Design History File)
- **DMR** (Device Master Record)
- **DHR** (Device History Record)

The MDF approach aligns with ISO 13485:2016 requirements and provides a more unified documentation structure.

---

## Reference: Quality Manual Guide

# Quality Manual Development Guide

This guide provides comprehensive instructions for creating an ISO 13485:2016 compliant Quality Manual.

## Purpose of the Quality Manual

The Quality Manual is the foundational policy-level document of your Quality Management System (QMS). It:

1. **Defines the scope** of your QMS
2. **Documents or references** all QMS procedures
3. **Describes the interaction** between QMS processes
4. **Outlines the structure** of QMS documentation
5. **Demonstrates management commitment** to quality and regulatory compliance
6. **Serves as a guide** for employees and auditors

The Quality Manual is typically 20-50 pages and remains relatively stable over time, while procedures and work instructions may change more frequently.

---

## Required Content per ISO 13485:2016 (Clause 4.2.2)

The Quality Manual must include:

### a) Scope of the QMS
- Define which parts of the organization are covered
- Identify exclusions with justification
- Specify product types covered
- Define applicable regulatory requirements

### b) Documented Procedures or References
- List all 31 documented procedures (or reference where they can be found)
- Provide document numbers/titles for easy reference

### c) Description of Process Interactions
- Show how QMS processes interact and sequence
- May include process maps or flowcharts
- Explain dependencies between processes

### d) Structure of Documentation
- Describe the documentation hierarchy
- Explain document numbering and control systems
- Define document types (procedures, work instructions, forms, records)

---

## Quality Manual Structure

### Recommended Table of Contents

#### Section 0: Document Control
- Document identification
- Revision history
- Approval signatures
- Distribution list

#### Section 1: Introduction
- 1.1 Company Overview
- 1.2 Purpose of the Quality Manual
- 1.3 Document Control and Revisions
- 1.4 Definitions and Abbreviations

#### Section 2: Scope and Exclusions (ISO 13485 Clause 4.2.2.a)
- 2.1 Scope of QMS
- 2.2 Products Covered
- 2.3 Applicable Regulatory Requirements
- 2.4 Exclusions and Justifications

#### Section 3: Quality Policy and Objectives (ISO 13485 Clauses 5.3, 5.4)
- 3.1 Quality Policy Statement
- 3.2 Quality Objectives
- 3.3 Communication of Policy and Objectives

#### Section 4: Quality Management System (ISO 13485 Clause 4)
- 4.1 General Requirements
  - 4.1.1 Processes and Their Application
  - 4.1.2 Process Interactions (with process map)
  - 4.1.3 Outsourced Processes
  - 4.1.4 Risk Management
  - 4.1.5 Software Validation
- 4.2 Documentation Requirements
  - 4.2.1 General
  - 4.2.2 Quality Manual (this document)
  - 4.2.3 Medical Device File
  - 4.2.4 Control of Documents
  - 4.2.5 Control of Records
- 4.3 Documentation Structure (ISO 13485 Clause 4.2.2.d)

#### Section 5: Management Responsibility (ISO 13485 Clause 5)
- 5.1 Management Commitment
- 5.2 Customer Focus
- 5.3 Quality Policy (reference to Section 3)
- 5.4 Planning
- 5.5 Responsibility, Authority and Communication
  - 5.5.1 Organization Structure and Responsibilities
  - 5.5.2 Management Representative
  - 5.5.3 Internal Communication
- 5.6 Management Review

#### Section 6: Resource Management (ISO 13485 Clause 6)
- 6.1 Provision of Resources
- 6.2 Human Resources
- 6.3 Infrastructure
- 6.4 Work Environment and Contamination Control

#### Section 7: Product Realization (ISO 13485 Clause 7)
- 7.1 Planning of Product Realization
- 7.2 Customer-Related Processes
- 7.3 Design and Development
- 7.4 Purchasing
- 7.5 Production and Service Provision
- 7.6 Control of Monitoring and Measuring Equipment

#### Section 8: Measurement, Analysis and Improvement (ISO 13485 Clause 8)
- 8.1 General
- 8.2 Monitoring and Measurement
  - 8.2.1 Feedback
  - 8.2.2 Complaint Handling
  - 8.2.3 Reporting to Regulatory Authorities
  - 8.2.4 Internal Audit
  - 8.2.5 Monitoring and Measurement of Processes
  - 8.2.6 Monitoring and Measurement of Product
- 8.3 Control of Nonconforming Product
- 8.4 Analysis of Data
- 8.5 Improvement
  - 8.5.1 General
  - 8.5.2 Corrective Action
  - 8.5.3 Preventive Action

#### Section 9: Appendices
- Appendix A: List of Documented Procedures (ISO 13485 Clause 4.2.2.b)
- Appendix B: Organization Chart
- Appendix C: Process Map/Interactions (ISO 13485 Clause 4.2.2.c)
- Appendix D: Definitions and Abbreviations
- Appendix E: Applicable Regulatory Requirements

---

## Writing Guidelines

### Level of Detail

The Quality Manual should be at a **policy level**, not operational level:

**DO:**
- State WHAT the organization does
- State WHY policies exist
- Reference WHO is responsible
- Reference WHERE to find detailed procedures

**DON'T:**
- Provide step-by-step HOW-TO instructions (that's for procedures)
- Include forms or templates (that's for procedures and work instructions)
- Provide excessive technical detail

### Example - Correct Level of Detail:

**Good (Policy Level):**
> "The organization has established a documented procedure for the control of nonconforming product. This procedure ensures that nonconforming product is identified, segregated, and dispositioned appropriately. The Quality Manager is responsible for reviewing all nonconformances and determining appropriate corrective actions. Refer to SOP-8.3-01 Control of Nonconforming Product."

**Too Detailed (Operational Level - Don't do this):**
> "When a nonconforming product is identified, the inspector fills out Form NCR-001 and places a red tag on the product. The product is moved to the quarantine area in Building B, Row 5. The Quality Manager reviews the NCR within 24 hours and checks one of three boxes: Rework, Scrap, or Use As-Is. If rework is selected, the inspector..."

### Language and Style

- Use present tense and active voice
- Be clear and concise
- Avoid jargon where possible
- Define technical terms in the definitions section
- Use consistent terminology throughout
- Number all sections and subsections

### Cross-Referencing

- Reference specific procedures by number and title
- Reference specific clause numbers from ISO 13485
- Use consistent format: "Refer to SOP-XXX [Title]"
- Ensure all referenced documents exist

---

## Section-by-Section Guidance

### Section 0: Document Control

**Purpose:** Control and identification of the manual itself

**Content:**
- Document number and title
- Revision number and date
- Page numbers (Page X of Y)
- Approval signatures (typically top management)
- Distribution list (who has controlled copies)
- Revision history table

**Example Revision History Table:**

| Revision | Date | Description of Changes | Approved By |
|----------|------|------------------------|-------------|
| 00 | YYYY-MM-DD | Initial release | [Name] |
| 01 | YYYY-MM-DD | Updated Section 7.3 for new design process | [Name] |

### Section 1: Introduction

#### 1.1 Company Overview
- Company name and legal entity
- Business address(es)
- Type of business (manufacturer, contract manufacturer, etc.)
- History and background (brief)
- Mission statement (optional)

#### 1.2 Purpose of the Quality Manual
Explain that this manual:
- Describes the QMS established per ISO 13485:2016
- Demonstrates compliance with applicable regulatory requirements
- Serves as primary reference for QMS

#### 1.3 Document Control and Revisions
- How the manual is controlled
- Who approves changes
- How often it's reviewed
- Reference to document control procedure

#### 1.4 Definitions and Abbreviations
List key terms used in the manual:
- QMS: Quality Management System
- CAPA: Corrective and Preventive Action
- DHF: Design History File
- MDF: Medical Device File
- SOP: Standard Operating Procedure
- WI: Work Instruction
- etc.

### Section 2: Scope and Exclusions

#### 2.1 Scope of QMS

**Must Include:**
- Organizational units covered
- Physical locations covered
- Activities covered (design, manufacturing, distribution, servicing, etc.)
- Product types covered

**Example:**
> "This Quality Management System applies to [Company Name] and covers all activities related to the design, development, production, installation, and servicing of [product type] medical devices at our facility located at [address]. The QMS applies to all employees, contractors, and temporary staff performing work that affects product quality and regulatory compliance."

#### 2.2 Products Covered

List product categories or families covered:
- Class I, II, or III medical devices
- Product names or families
- Intended use categories

**Example:**
> "This QMS covers the following medical device product families:
> - Surgical instruments (Class I)
> - Patient monitoring systems (Class II)
> - Implantable cardiac devices (Class III)"

#### 2.3 Applicable Regulatory Requirements

List all applicable regulations:
- ISO 13485:2016
- FDA 21 CFR Part 820 (QMSR)
- EU MDR 2017/745
- Health Canada Medical Devices Regulations
- [Other applicable requirements]

#### 2.4 Exclusions and Justifications

**Common Exclusions:**

**Design and Development (Clause 7.3):**
If you only manufacture per customer specifications without your own design:
> "Clause 7.3 Design and Development is excluded from the scope of this QMS. [Company Name] operates as a contract manufacturer and produces medical devices according to complete design specifications provided by customers. All design activities are performed by the customer and [Company Name] has no responsibility for design inputs, outputs, verification, validation, or design changes."

**Installation (Clause 7.5.3):**
If product requires no installation:
> "Clause 7.5.3 Installation Activities is excluded. The medical devices manufactured by [Company Name] are supplied ready for use and do not require installation activities at the customer site."

**Servicing (Clause 7.5.4):**
If servicing is not offered:
> "Clause 7.5.4 Servicing Activities is excluded. [Company Name] does not provide servicing of medical devices after delivery to the customer. Products are intended for single use [or] servicing is performed by authorized service partners under separate contractual arrangements."

**Important:** All exclusions must be justified based on the nature of the organization and products. Exclusions must not affect the organization's ability or responsibility to provide safe and effective medical devices that meet regulatory requirements.

### Section 3: Quality Policy and Objectives

#### 3.1 Quality Policy Statement

**Requirements:**
- Appropriate to the organization
- Includes commitment to meeting requirements
- Includes commitment to maintaining QMS effectiveness
- Provides framework for quality objectives
- Signed by top management

**Example:**
> **QUALITY POLICY**
>
> [Company Name] is committed to providing safe, effective, and high-quality medical devices that meet or exceed customer expectations and comply with all applicable regulatory requirements.
>
> We achieve this through:
> - Maintaining an effective Quality Management System compliant with ISO 13485 and applicable regulatory requirements
> - Establishing, monitoring, and achieving measurable quality objectives
> - Continually improving our processes, products, and QMS effectiveness
> - Ensuring all personnel understand their responsibilities and are properly trained
> - Managing risks throughout the product lifecycle
> - Promptly addressing customer feedback and complaints
>
> This policy is communicated to all employees and reviewed annually to ensure continuing suitability.
>
> [Signature]
> [Name], Chief Executive Officer
> [Date]

#### 3.2 Quality Objectives

List measurable objectives that support the policy:
- Customer satisfaction targets
- Product quality metrics
- Process performance goals
- Delivery performance
- Training completion rates
- CAPA closure rates

**Example:**
> The organization has established the following measurable quality objectives:
> 1. Customer satisfaction rating ≥ 4.5 out of 5.0
> 2. Product defect rate < 0.5% of units shipped
> 3. On-time delivery ≥ 95%
> 4. CAPA closed within 60 days ≥ 90%
> 5. Employee training completion rate ≥ 100% on schedule
> 6. Internal audit findings addressed within 30 days ≥ 95%
>
> Quality objectives are reviewed quarterly and revised as necessary to drive continual improvement.

#### 3.3 Communication

Explain how policy and objectives are communicated:
- Employee orientation and training
- Posted in facility
- Included in employee handbook
- Management review meetings
- Quality meetings

### Section 4: Quality Management System

This section describes how you've implemented ISO 13485 Clause 4 requirements.

#### 4.1.1 Processes and Their Application

List QMS processes:
- Management processes (planning, review, communication)
- Product realization processes (design, purchasing, production, etc.)
- Support processes (HR, maintenance, document control, etc.)
- Monitoring and measurement processes (audits, inspections, CAPA, etc.)

Reference the process map in Appendix C.

#### 4.1.2 Process Interactions

Describe how processes interact:
> "The QMS processes are interconnected and sequential. Management review provides direction for all processes. Product realization processes transform customer requirements into delivered products. Support processes enable product realization. Monitoring processes provide feedback for continual improvement. A detailed process map showing interactions is provided in Appendix C."

#### 4.1.3 Outsourced Processes

If applicable, list outsourced processes and how they're controlled:
- Sterilization (controlled through supplier qualification and ongoing monitoring)
- Calibration services (controlled through qualified service providers)
- Software development (controlled through development agreements and audits)

#### 4.1.4 Risk Management

Describe risk management approach:
> "The organization has established documented requirements for risk management throughout product realization in accordance with ISO 14971. Risk management activities are integrated into design and development, production, and post-market surveillance. Risk management records are maintained as part of the Medical Device File. Refer to SOP-4.1.5 Risk Management."

#### 4.1.5 Software Validation

Describe approach to software validation:
> "Computer software applications used in the QMS, including [list key software systems], are validated prior to initial use and after changes. Validation activities are based on risk assessment and include installation qualification, operational qualification, and performance qualification as appropriate. Refer to SOP-4.1.6 Software Validation."

#### 4.2 Documentation Requirements

Describe the documentation structure (fulfill 4.2.2.d requirement):

**Four-Tier Documentation Structure:**

**Tier 1: Quality Manual** (This Document)
- Policy-level document
- Defines QMS scope and structure
- References all procedures

**Tier 2: Procedures (SOPs)**
- Define WHAT must be done, WHO does it, WHEN
- Cover multi-functional activities
- Include the 31 required documented procedures

**Tier 3: Work Instructions (WIs)**
- Define HOW to perform specific tasks
- Step-by-step instructions
- Department or process-specific

**Tier 4: Records and Forms**
- Provide evidence of conformity
- Demonstrate effective QMS operation
- Maintained per retention requirements

Include a visual diagram of the documentation hierarchy.

#### 4.2.3 Medical Device File

Describe MDF structure:
> "A Medical Device File (MDF) is established and maintained for each medical device type or family. The MDF contains all documentation specified in ISO 13485:2016 Clause 4.2.3, including general description, intended use, specifications, procedures, risk management file, and design and development files when applicable. MDF contents and control are defined in SOP-4.2.3 Medical Device File."

#### 4.2.4 Control of Documents

Summarize document control process:
> "All QMS documents are controlled per SOP-4.2.4 Control of Documents. This ensures documents are approved before use, reviewed and updated as necessary, properly identified with revision status, available at points of use, legible and identifiable, and protected from unintended use of obsolete versions."

#### 4.2.5 Control of Records

Summarize record control process:
> "QMS records provide evidence of conformity and effective operation. Records are controlled per SOP-4.2.5 Control of Records to ensure they remain legible, readily identifiable, retrievable, and protected. Records are retained for at least the lifetime of the medical device as defined by the organization, and in accordance with applicable regulatory requirements."

### Sections 5-8: Management, Resources, Realization, Measurement

For these sections, follow this pattern for each clause:

1. **State the requirement** (what ISO 13485 requires)
2. **Describe how you meet it** (policy-level summary)
3. **Reference the detailed procedure(s)**
4. **Identify responsible parties**

**Example for Clause 8.2.2 Complaint Handling:**

> **8.2.2 Complaint Handling**
>
> The organization has established a documented procedure for timely complaint handling. All complaints are promptly received, recorded, evaluated, investigated, and appropriately resolved. Complaints are analyzed for trends and potential product quality or safety issues. Complaints that meet regulatory reporting criteria are reported to applicable regulatory authorities within required timeframes.
>
> The Quality Assurance Manager is responsible for complaint handling and ensuring compliance with regulatory requirements.
>
> Refer to SOP-8.2.2 Complaint Handling for detailed procedures.

Repeat this pattern for all clauses 5.1 through 8.5.3.

### Section 9: Appendices

#### Appendix A: List of Documented Procedures

Create a table listing all QMS procedures:

| SOP Number | Title | ISO 13485 Clause | Approval Date | Revision |
|------------|-------|------------------|---------------|----------|
| SOP-4.1.5 | Risk Management | 4.1.5 | YYYY-MM-DD | 02 |
| SOP-4.1.6 | Software Validation | 4.1.6 | YYYY-MM-DD | 01 |
| SOP-4.2.4 | Control of Documents | 4.2.4 | YYYY-MM-DD | 03 |
| ... | ... | ... | ... | ... |

Include all 31 required procedures plus any additional procedures.

#### Appendix B: Organization Chart

Include a current organization chart showing:
- Reporting relationships
- Key quality functions
- Management representative
- Design responsible (if applicable)

#### Appendix C: Process Map/Interactions

Include a visual process map showing:
- All QMS processes
- Process interactions and sequence
- Inputs and outputs
- Interfaces between processes

This can be a flowchart, swim-lane diagram, or process interaction matrix.

#### Appendix D: Definitions and Abbreviations

Comprehensive list of terms and abbreviations used in the QMS.

#### Appendix E: Applicable Regulatory Requirements

Detailed list of all regulatory requirements applicable to your organization:
- FDA regulations and guidance documents
- EU regulations and harmonized standards
- Other regional requirements
- Recognized consensus standards (e.g., IEC 60601, ISO 14971, etc.)

---

## Development Process

### Step 1: Preparation
1. Gather reference materials (ISO 13485 standard, regulatory requirements)
2. Review existing quality documentation
3. Identify responsible personnel for each clause
4. Determine applicable exclusions

### Step 2: Drafting
1. Use the recommended structure above
2. Start with Sections 0-3 (administrative and policy)
3. Draft Sections 4-8 using the pattern (requirement, implementation, reference, responsibility)
4. Complete appendices
5. Keep at policy level - don't get too detailed

### Step 3: Review and Approval
1. Technical review by Quality Manager
2. Management review by top management
3. Legal review (if needed)
4. Address all comments
5. Final approval by CEO or authorized representative

### Step 4: Implementation
1. Communicate to all employees
2. Provide training on Quality Manual
3. Make available at all locations
4. Establish controlled distribution

### Step 5: Maintenance
1. Review annually (minimum)
2. Update when significant changes occur
3. Keep revision history
4. Ensure all distributed copies are current

---

## Common Mistakes to Avoid

### 1. Too Much Detail
**Problem:** Including step-by-step procedures in the manual
**Solution:** Keep at policy level, reference detailed procedures

### 2. Copy-Paste from Standard
**Problem:** Copying text directly from ISO 13485
**Solution:** Write in your own words describing YOUR QMS

### 3. Inconsistent References
**Problem:** Referencing procedures that don't exist or have wrong numbers
**Solution:** Maintain a master list of procedures and verify all references

### 4. Unjustified Exclusions
**Problem:** Excluding clauses without proper justification
**Solution:** Carefully justify all exclusions based on business activities

### 5. No Process Map
**Problem:** Missing visual representation of process interactions
**Solution:** Create clear process map in Appendix C

### 6. Generic Quality Policy
**Problem:** Quality policy that could apply to any company
**Solution:** Make policy specific to your organization and products

### 7. Outdated Content
**Problem:** Manual doesn't reflect current operations
**Solution:** Review and update regularly

### 8. Missing Signatures
**Problem:** No management approval signatures
**Solution:** Ensure top management signs the document control page and quality policy

### 9. No Revision Control
**Problem:** Multiple versions in circulation
**Solution:** Implement proper document control per Section 4.2.4

### 10. Forgetting Appendix A
**Problem:** Not including complete list of documented procedures
**Solution:** Create comprehensive procedure list in Appendix A

---

## Quality Manual Checklist

Use this checklist to verify your Quality Manual is complete:

### Required Content (ISO 13485 Clause 4.2.2)
- [ ] Scope of QMS defined
- [ ] Exclusions identified and justified
- [ ] Documented procedures listed or referenced
- [ ] Process interactions described
- [ ] Documentation structure outlined

### Management Approval
- [ ] Approved by top management
- [ ] Approval signature and date included
- [ ] Document control information complete

### Completeness
- [ ] All ISO 13485 clauses 4-8 addressed
- [ ] Quality policy included and signed
- [ ] Quality objectives defined and measurable
- [ ] Responsibilities assigned for each clause
- [ ] All procedures referenced by correct number/title

### Appendices
- [ ] Appendix A: Complete list of procedures
- [ ] Appendix B: Organization chart
- [ ] Appendix C: Process map
- [ ] Appendix D: Definitions
- [ ] Appendix E: Regulatory requirements

### Format and Style
- [ ] Numbered sections and subsections
- [ ] Consistent terminology
- [ ] Policy-level (not operational detail)
- [ ] Clear and understandable
- [ ] Professional appearance

### References
- [ ] All referenced procedures exist
- [ ] All procedure numbers/titles correct
- [ ] ISO 13485 clauses correctly cited
- [ ] Regulatory requirements accurately stated

### Distribution and Access
- [ ] Distribution list established
- [ ] Controlled copy process defined
- [ ] Available to all relevant personnel
- [ ] Training plan for Quality Manual

---

## Example Quality Policy Statements

Choose a style appropriate for your organization:

### Example 1: Detailed Commitment
> **QUALITY POLICY**
>
> At [Company Name], quality is our highest priority. We are committed to designing, manufacturing, and delivering medical devices that meet the highest standards of safety, performance, and reliability.
>
> Our commitments include:
> - Compliance with ISO 13485 and all applicable regulatory requirements
> - Understanding and meeting customer and patient needs
> - Establishing and achieving measurable quality objectives
> - Managing risks throughout the product lifecycle
> - Continually improving our processes and products
> - Maintaining competent and motivated personnel
> - Responding promptly and effectively to feedback and complaints
> - Fostering a culture of quality and accountability
>
> This policy applies to all employees, contractors, and suppliers. Every person in our organization is responsible for quality and for supporting our QMS. This policy is reviewed annually and communicated throughout the organization.
>
> [Signature Block]

### Example 2: Concise Focus
> **QUALITY POLICY**
>
> [Company Name] is committed to providing safe and effective medical devices that meet customer expectations and regulatory requirements. We maintain a quality management system compliant with ISO 13485 and continually improve its effectiveness through measurable objectives and employee engagement.
>
> [Signature Block]

### Example 3: Patient-Centered
> **QUALITY POLICY**
>
> Our mission is to improve patient outcomes through innovative, high-quality medical devices. We achieve this by:
> - Placing patient safety first in all decisions
> - Complying with ISO 13485 and regulatory requirements
> - Engaging employees in quality and continuous improvement
> - Partnering with customers to exceed expectations
> - Managing risks proactively throughout product lifecycle
>
> This policy is communicated to all personnel and reviewed for effectiveness.
>
> [Signature Block]

---

## Next Steps After Manual Approval

1. **Conduct training** - Train all employees on the Quality Manual
2. **Develop procedures** - Create or update the 31 documented procedures
3. **Create work instructions** - Develop operational-level instructions
4. **Implement processes** - Put QMS into practice
5. **Conduct internal audits** - Verify effective implementation
6. **Management review** - Review QMS effectiveness
7. **Prepare for certification** - Schedule certification audit when ready

---

## Resources and References

- ISO 13485:2016 - Medical devices — Quality management systems
- ISO 14971 - Application of risk management to medical devices
- FDA 21 CFR Part 820 - Quality System Regulation (QMSR)
- EU MDR 2017/745 - Medical Devices Regulation
- ISO/TR 14969 - Medical devices quality management systems - Guidance on ISO 13485
