---
title: "Treatment Plans"
description: "Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Supports general medical treatment, rehabilitation therapy, mental health care, chronic disease management, perioperative care, and pain..."
category: "research"
source: "community"
author: "Community"
tags: ["treatment", "plans"]
date: 2026-03-20
---

# Treatment Plan Writing

## Overview

Treatment plan writing is the systematic documentation of clinical care strategies designed to address patient health conditions through evidence-based interventions, measurable goals, and structured follow-up. This skill provides comprehensive LaTeX templates and validation tools for creating **concise, focused** treatment plans (3-4 pages standard) across all medical specialties with full regulatory compliance.

**Critical Principles:**
1. **CONCISE & ACTIONABLE**: Treatment plans default to 3-4 pages maximum, focusing only on clinically essential information that impacts care decisions
2. **Patient-Centered**: Plans must be evidence-based, measurable, and compliant with healthcare regulations (HIPAA, documentation standards)
3. **Minimal Citations**: Use brief in-text citations only when needed to support clinical recommendations; avoid extensive bibliographies

Every treatment plan should include clear goals, specific interventions, defined timelines, monitoring parameters, and expected outcomes that align with patient preferences and current clinical guidelines - all presented as efficiently as possible.

## When to Use This Skill

This skill should be used when:
- Creating individualized treatment plans for patient care
- Documenting therapeutic interventions for chronic disease management
- Developing rehabilitation programs (physical therapy, occupational therapy, cardiac rehab)
- Writing mental health and psychiatric treatment plans
- Planning perioperative and surgical care pathways
- Establishing pain management protocols
- Setting patient-centered goals using SMART criteria
- Coordinating multidisciplinary care across specialties
- Ensuring regulatory compliance in treatment documentation
- Generating professional treatment plans for medical records

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every treatment plan MUST include at least 1 AI-generated figure using the scientific-schematics skill.**

This is not optional. Treatment plans benefit greatly from visual elements. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., treatment pathway flowchart, care coordination diagram, or therapy timeline)
2. For complex plans: include decision algorithm flowchart
3. For rehabilitation plans: include milestone progression diagram

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Treatment pathway flowcharts
- Care coordination diagrams
- Therapy progression timelines
- Multidisciplinary team interaction diagrams
- Medication management flowcharts
- Rehabilitation protocol visualizations
- Clinical decision algorithm diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Document Format and Best Practices

### Document Length Options

Treatment plans come in three format options based on clinical complexity and use case:

#### Option 1: One-Page Treatment Plan (PREFERRED for most cases)

**When to use**: Straightforward clinical scenarios, standard protocols, busy clinical settings

**Format**: Single page containing all essential treatment information in scannable sections
- No table of contents needed
- No extensive narratives
- Focused on actionable items only
- Similar to precision oncology reports or treatment recommendation cards

**Required sections** (all on one page):
1. **Header Box**: Patient info, diagnosis, date, molecular/risk profile if applicable
2. **Treatment Regimen**: Numbered list of specific interventions
3. **Supportive Care**: Brief bullet points
4. **Rationale**: 1-2 sentence justification (optional for standard protocols)
5. **Monitoring**: Key parameters and frequency
6. **Evidence Level**: Guideline reference or evidence grade (e.g., "Level 1, FDA approved")
7. **Expected Outcome**: Timeline and success metrics

**Design principles**:
- Use small boxes/tables for organization (like the clinical treatment recommendation card format)
- Eliminate all non-essential text
- Use abbreviations familiar to clinicians
- Dense information layout - maximize information per square inch
- Think "quick reference card" not "comprehensive documentation"

**Example structure**:
```latex
[Patient ID/Diagnosis Box at top]

TARGET PATIENT POPULATION
  Number of patients, demographics, key features

PRIMARY TREATMENT REGIMEN
  • Medication 1: dose, frequency, duration
  • Procedure: specific details
  • Monitoring: what and when

SUPPORTIVE CARE
  • Key supportive medications

RATIONALE
  Brief clinical justification

MOLECULAR TARGETS / RISK FACTORS
  Relevant biomarkers or risk stratification

EVIDENCE LEVEL
  Guideline reference, trial data

MONITORING REQUIREMENTS
  Key labs/vitals, frequency

EXPECTED CLINICAL BENEFIT
  Primary endpoint, timeline
```

#### Option 2: Standard 3-4 Page Format

**When to use**: Moderate complexity, need for patient education materials, multidisciplinary coordination

Uses the Foundation Medicine first-page summary model with 2-3 additional pages of details.

#### Option 3: Extended 5-6 Page Format

**When to use**: Complex comorbidities, research protocols, extensive safety monitoring required

### First Page Summary (Foundation Medicine Model)

**CRITICAL REQUIREMENT: All treatment plans MUST have a complete executive summary on the first page ONLY, before any table of contents or detailed sections.**

Following the Foundation Medicine model for precision medicine reporting and clinical summary documents, treatment plans begin with a one-page executive summary that provides immediate access to key actionable information. This entire summary must fit on the first page.

**Required First Page Structure (in order):**

1. **Title and Subtitle**
   - Main title: Treatment plan type (e.g., "Comprehensive Treatment Plan")
   - Subtitle: Specific condition or focus (e.g., "Type 2 Diabetes Mellitus - Young Adult Patient")

2. **Report Information Box** (using `\begin{infobox}` or `\begin{patientinfo}`)
   - Report type/document purpose
   - Date of plan creation
   - Patient demographics (age, sex, de-identified)
   - Primary diagnosis with ICD-10 code
   - Report author/clinic (if applicable)
   - Analysis approach or framework used

3. **Key Findings or Treatment Highlights** (2-4 colored boxes using appropriate box types)
   - **Primary Treatment Goals** (using `\begin{goalbox}`)
     - 2-3 SMART goals in bullet format
   - **Main Interventions** (using `\begin{keybox}` or `\begin{infobox}`)
     - 2-3 key interventions (pharmacological, non-pharmacological, monitoring)
   - **Critical Decision Points** (using `\begin{warningbox}` if urgent)
     - Important monitoring thresholds or safety considerations
   - **Timeline Overview** (using `\begin{infobox}`)
     - Brief treatment duration/phases
     - Key milestone dates

**Visual Format Requirements:**
- Use `\thispagestyle{empty}` to remove page numbers from first page
- All content must fit on page 1 (before `\newpage`)
- Use colored boxes (tcolorbox package) with different colors for different information types
- Boxes should be visually prominent and easy to scan
- Use concise, bullet-point format
- Table of contents (if included) starts on page 2
- Detailed sections start on page 3

**Example First Page Structure:**
```latex
\maketitle
\thispagestyle{empty}

% Report Information Box
\begin{patientinfo}
  Report Type, Date, Patient Info, Diagnosis, etc.
\end{patientinfo}

% Key Finding #1: Treatment Goals
\begin{goalbox}[Primary Treatment Goals]
  • Goal 1
  • Goal 2
  • Goal 3
\end{goalbox}

% Key Finding #2: Main Interventions
\begin{keybox}[Core Interventions]
  • Intervention 1
  • Intervention 2
  • Intervention 3
\end{keybox}

% Key Finding #3: Critical Monitoring (if applicable)
\begin{warningbox}[Critical Decision Points]
  • Decision point 1
  • Decision point 2
\end{warningbox}

\newpage
\tableofcontents  % TOC on page 2
\newpage  % Detailed content starts page 3
```

### Concise Documentation

**CRITICAL: Treatment plans MUST prioritize brevity and clinical relevance. Default to 3-4 pages maximum unless clinical complexity absolutely demands more detail.**

Treatment plans should prioritize **clarity and actionability** over exhaustive detail:

- **Focused**: Include only clinically essential information that impacts care decisions
- **Actionable**: Emphasize what needs to be done, when, and why
- **Efficient**: Facilitate quick decision-making without sacrificing clinical quality
- **Target length options**:
  - **1-page format** (preferred for straightforward cases): Quick-reference card with all essential information
  - **3-4 pages standard**: Standard format with first-page summary + supporting details
  - **5-6 pages** (rare): Only for highly complex cases with multiple comorbidities or multidisciplinary interventions

**Streamlining Guidelines:**
- **First Page Summary**: Use individual colored boxes to consolidate key information (goals, interventions, decision points) - this alone can often convey the essential treatment plan
- **Eliminate Redundancy**: If information is in the first-page summary, don't repeat it verbatim in detailed sections
- **Patient Education section**: 3-5 key bullet points on critical topics and warning signs only
- **Risk Mitigation section**: Highlight only critical medication safety concerns and emergency actions (not exhaustive lists)
- **Expected Outcomes section**: 2-3 concise statements on anticipated responses and timelines
- **Interventions**: Focus on primary interventions; secondary/supportive measures in brief bullet format
- **Use tables and bullet points** extensively for efficient presentation
- **Avoid narrative prose** where structured lists suffice
- **Combine related sections** when appropriate to reduce page count

### Quality Over Quantity

The goal is professional, clinically complete documentation that respects clinicians' time while ensuring comprehensive patient care. Every section should add value; remove or condense sections that don't directly inform treatment decisions.

### Citations and Evidence Support

**Use minimal, targeted citations to support clinical recommendations:**

- **Text Citations Preferred**: Use brief in-text citations (Author Year) or simple references rather than extensive bibliographies unless specifically requested
- **When to Cite**:
  - Clinical practice guideline recommendations (e.g., "per ADA 2024 guidelines")
  - Specific medication dosing or protocols (e.g., "ACC/AHA recommendations")
  - Novel or controversial interventions requiring evidence support
  - Risk stratification tools or validated assessment scales
- **When NOT to Cite**:
  - Standard-of-care interventions widely accepted in the field
  - Basic medical facts and routine clinical practices
  - General patient education content
- **Citation Format**: 
  - Inline: "Initiate metformin as first-line therapy (ADA Standards of Care 2024)"
  - Minimal: "Treatment follows ACC/AHA heart failure guidelines"
  - Avoid formal numbered references and extensive bibliography sections unless document is for academic/research purposes
- **Keep it Brief**: A 3-4 page treatment plan should have 0-3 citations maximum, only where essential for clinical credibility or novel recommendations

## Core Capabilities

### 1. General Medical Treatment Plans

General medical treatment plans address common chronic conditions and acute medical issues requiring structured therapeutic interventions.

#### Standard Components

**Patient Information (De-identified)**
- Demographics (age, sex, relevant medical background)
- Active medical conditions and comorbidities
- Current medications and allergies
- Relevant social and family history
- Functional status and baseline assessments
- **HIPAA Compliance**: Remove all 18 identifiers per Safe Harbor method

**Diagnosis and Assessment Summary**
- Primary diagnosis with ICD-10 code
- Secondary diagnoses and comorbidities
- Severity classification and staging
- Functional limitations and quality of life impact
- Risk stratification (e.g., cardiovascular risk, fall risk)
- Prognostic indicators

**Treatment Goals (SMART Format)**

Short-term goals (1-3 months):
- **Specific**: Clearly defined outcome (e.g., "Reduce HbA1c to <7%")
- **Measurable**: Quantifiable metrics (e.g., "Decrease systolic BP by 10 mmHg")
- **Achievable**: Realistic given patient capabilities
- **Relevant**: Aligned with patient priorities and values
- **Time-bound**: Specific timeframe (e.g., "within 8 weeks")

Long-term goals (6-12 months):
- Disease control or remission targets
- Functional improvement objectives
- Quality of life enhancement
- Prevention of complications
- Maintenance of independence

**Interventions**

*Pharmacological*:
- Medications with specific dosages, routes, frequencies
- Titration schedules and target doses
- Drug-drug interaction considerations
- Monitoring for adverse effects
- Medication reconciliation

*Non-pharmacological*:
- Lifestyle modifications (diet, exercise, smoking cessation)
- Behavioral interventions
- Patient education and self-management
- Monitoring and self-tracking (glucose, blood pressure, weight)
- Assistive devices or adaptive equipment

*Procedural*:
- Planned procedures or interventions
- Referrals to specialists
- Diagnostic testing schedule
- Preventive care (vaccinations, screenings)

**Timeline and Schedule**
- Treatment phases with specific timeframes
- Appointment frequency (weekly, monthly, quarterly)
- Milestone assessments and goal evaluations
- Medication adjustments schedule
- Expected duration of treatment

**Monitoring Parameters**
- Clinical outcomes to track (vital signs, lab values, symptoms)
- Assessment tools and scales (e.g., PHQ-9, pain scales)
- Frequency of monitoring
- Thresholds for intervention or escalation
- Patient-reported outcomes

**Expected Outcomes**
- Primary outcome measures
- Success criteria and benchmarks
- Expected timeline for improvement
- Criteria for treatment modification
- Long-term prognosis

**Follow-up Plan**
- Scheduled appointments and reassessments
- Communication plan (phone calls, secure messaging)
- Emergency contact procedures
- Criteria for urgent evaluation
- Transition or discharge planning

**Patient Education**
- Understanding of condition and treatment rationale
- Self-management skills training
- Medication administration and adherence
- Warning signs and when to seek help
- Resources and support services

**Risk Mitigation**
- Potential adverse effects and management
- Drug interactions and contraindications
- Fall prevention, infection prevention
- Emergency action plans
- Safety monitoring

#### Common Applications

- Diabetes mellitus management
- Hypertension control
- Heart failure treatment
- COPD management
- Asthma care plans
- Hyperlipidemia treatment
- Osteoarthritis management
- Chronic kidney disease

### 2. Rehabilitation Treatment Plans

Rehabilitation plans focus on restoring function, improving mobility, and enhancing quality of life through structured therapeutic programs.

#### Core Components

**Functional Assessment**
- Baseline functional status (ADLs, IADLs)
- Range of motion, strength, balance, endurance
- Gait analysis and mobility assessment
- Standardized measures (FIM, Barthel Index, Berg Balance Scale)
- Environmental assessment (home safety, accessibility)

**Rehabilitation Goals**

*Impairment-level goals*:
- Improve shoulder flexion to 140 degrees
- Increase quadriceps strength by 2/5 MMT grades
- Enhance balance (Berg Score >45/56)

*Activity-level goals*:
- Independent ambulation 150 feet with assistive device
- Climb 12 stairs with handrail supervision
- Transfer bed-to-chair independently

*Participation-level goals*:
- Return to work with modifications
- Resume recreational activities
- Independent community mobility

**Therapeutic Interventions**

*Physical Therapy*:
- Therapeutic exercises (strengthening, stretching, endurance)
- Manual therapy techniques
- Gait training and balance activities
- Modalities (heat, ice, electrical stimulation, ultrasound)
- Assistive device training

*Occupational Therapy*:
- ADL training (bathing, dressing, grooming, feeding)
- Upper extremity strengthening and coordination
- Adaptive equipment and modifications
- Energy conservation techniques
- Cognitive rehabilitation

*Speech-Language Pathology*:
- Swallowing therapy and dysphagia management
- Communication strategies and augmentative devices
- Cognitive-linguistic therapy
- Voice therapy

*Other Services*:
- Recreational therapy
- Aquatic therapy
- Cardiac rehabilitation
- Pulmonary rehabilitation
- Vestibular rehabilitation

**Treatment Schedule**
- Frequency: 3x/week PT, 2x/week OT (example)
- Session duration: 45-60 minutes
- Treatment phase durations (acute, subacute, maintenance)
- Expected total duration: 8-12 weeks
- Reassessment intervals

**Progress Monitoring**
- Weekly functional assessments
- Standardized outcome measures
- Goal attainment scaling
- Pain and symptom tracking
- Patient satisfaction

**Home Exercise Program**
- Specific exercises with repetitions/sets/frequency
- Precautions and safety instructions
- Progression criteria
- Self-monitoring strategies

#### Specialty Rehabilitation

- Post-stroke rehabilitation
- Orthopedic rehabilitation (joint replacement, fracture)
- Cardiac rehabilitation (post-MI, post-surgery)
- Pulmonary rehabilitation
- Vestibular rehabilitation
- Neurological rehabilitation
- Sports injury rehabilitation

### 3. Mental Health Treatment Plans

Mental health treatment plans address psychiatric conditions through integrated psychotherapeutic, pharmacological, and psychosocial interventions.

#### Essential Components

**Psychiatric Assessment**
- Primary psychiatric diagnosis (DSM-5 criteria)
- Symptom severity and functional impairment
- Co-occurring mental health conditions
- Substance use assessment
- Suicide/homicide risk assessment
- Trauma history and PTSD screening
- Social determinants of mental health

**Treatment Goals**

*Symptom reduction*:
- Decrease depression severity (PHQ-9 score from 18 to <10)
- Reduce anxiety symptoms (GAD-7 score <5)
- Improve sleep quality (Pittsburgh Sleep Quality Index)
- Stabilize mood (reduced mood episodes)

*Functional improvement*:
- Return to work or school
- Improve social relationships and support
- Enhance coping skills and emotional regulation
- Increase engagement in meaningful activities

*Recovery-oriented goals*:
- Build resilience and self-efficacy
- Develop crisis management skills
- Establish sustainable wellness routines
- Achieve personal recovery goals

**Therapeutic Interventions**

*Psychotherapy*:
- Evidence-based modality (CBT, DBT, ACT, psychodynamic, IPT)
- Session frequency (weekly, biweekly)
- Treatment duration (12-16 weeks, ongoing)
- Specific techniques and targets
- Group therapy participation

*Psychopharmacology*:
- Medication class and rationale
- Starting dose and titration schedule
- Target symptoms
- Expected response timeline (2-4 weeks for antidepressants)
- Side effect monitoring
- Combination therapy considerations

*Psychosocial Interventions*:
- Case management services
- Peer support programs
- Family therapy or psychoeducation
- Vocational rehabilitation
- Supported housing or community integration
- Substance abuse treatment

**Safety Planning**
- Crisis contacts and emergency services
- Warning signs and triggers
- Coping strategies and self-soothing techniques
- Safe environment modifications
- Means restriction (firearms, medications)
- Support system activation

**Monitoring and Assessment**
- Symptom rating scales (weekly or biweekly)
- Medication adherence and side effects
- Suicidal ideation screening
- Functional status assessments
- Treatment engagement and therapeutic alliance

**Patient and Family Education**
- Psychoeducation about diagnosis
- Treatment rationale and expectations
- Medication information
- Relapse prevention strategies
- Community resources

#### Mental Health Conditions

- Major depressive disorder
- Anxiety disorders (GAD, panic, social anxiety)
- Bipolar disorder
- Schizophrenia and psychotic disorders
- PTSD and trauma-related disorders
- Eating disorders
- Substance use disorders
- Personality disorders

### 4. Chronic Disease Management Plans

Comprehensive long-term care plans for chronic conditions requiring ongoing monitoring, treatment adjustments, and multidisciplinary coordination.

#### Key Features

**Disease-Specific Targets**
- Evidence-based treatment goals per guidelines
- Stage-appropriate interventions
- Complication prevention strategies
- Disease progression monitoring

**Self-Management Support**
- Patient activation and engagement
- Shared decision-making
- Action plans for symptom changes
- Technology-enabled monitoring (apps, remote monitoring)

**Care Coordination**
- Primary care physician oversight
- Specialist consultations and co-management
- Care transitions (hospital to home)
- Medication management across providers
- Communication protocols

**Population Health Integration**
- Registry tracking and outreach
- Preventive care and screening schedules
- Quality measure reporting
- Care gaps identification

#### Applicable Conditions

- Type 1 and Type 2 diabetes
- Cardiovascular disease (CHF, CAD)
- Chronic respiratory diseases (COPD, asthma)
- Chronic kidney disease
- Inflammatory bowel disease
- Rheumatoid arthritis and autoimmune conditions
- HIV/AIDS
- Cancer survivorship care

### 5. Perioperative Care Plans

Structured plans for surgical and procedural patients covering preoperative preparation, intraoperative management, and postoperative recovery.

#### Components

**Preoperative Assessment**
- Surgical indication and planned procedure
- Preoperative risk stratification (ASA class, cardiac risk)
- Optimization of medical conditions
- Medication management (continuation, discontinuation)
- Preoperative testing and clearances
- Informed consent and patient education

**Perioperative Interventions**
- Enhanced recovery after surgery (ERAS) protocols
- Venous thromboembolism prophylaxis
- Antibiotic prophylaxis
- Glycemic control strategies
- Pain management plan (multimodal analgesia)

**Postoperative Care**
- Immediate recovery goals (24-48 hours)
- Early mobilization protocols
- Diet advancement
- Wound care and drain management
- Pain control regimen
- Complication monitoring

**Discharge Planning**
- Activity restrictions and progression
- Medication reconciliation
- Follow-up appointments
- Home health or rehabilitation services
- Return-to-work timeline

### 6. Pain Management Plans

Multimodal approaches to acute and chronic pain using evidence-based interventions and opioid-sparing strategies.

#### Comprehensive Components

**Pain Assessment**
- Pain location, quality, intensity (0-10 scale)
- Temporal pattern (constant, intermittent, breakthrough)
- Aggravating and alleviating factors
- Functional impact (sleep, activities, mood)
- Previous treatments and responses
- Psychosocial contributors

**Multimodal Interventions**

*Pharmacological*:
- Non-opioid analgesics (acetaminophen, NSAIDs)
- Adjuvant medications (antidepressants, anticonvulsants, muscle relaxants)
- Topical agents (lidocaine, capsaicin, diclofenac)
- Opioid therapy (when appropriate, with risk mitigation)
- Titration and rotation strategies

*Interventional Procedures*:
- Nerve blocks and injections
- Radiofrequency ablation
- Spinal cord stimulation
- Intrathecal drug delivery

*Non-pharmacological*:
- Physical therapy and exercise
- Cognitive-behavioral therapy for pain
- Mindfulness and relaxation techniques
- Acupuncture
- TENS units

**Opioid Safety (when prescribed)**
- Indication and planned duration
- Prescription drug monitoring program (PDMP) check
- Opioid risk assessment tools
- Naloxone prescription
- Treatment agreements
- Random urine drug screening
- Frequent follow-up and reassessment

**Functional Goals**
- Specific activity improvements
- Sleep quality enhancement
- Reduced pain interference
- Improved quality of life
- Return to work or meaningful activities

## Best Practices

### Brevity and Focus (HIGHEST PRIORITY)

**Treatment plans MUST be concise and focused on actionable clinical information:**

- **1-page format is PREFERRED**: For most clinical scenarios, a single-page treatment plan (like precision oncology reports) provides all necessary information
- **Default to shortest format possible**: Start with 1-page; only expand if clinical complexity genuinely requires it
- **Every sentence must add value**: If a section doesn't change clinical decision-making, omit it entirely
- **Think "quick reference card" not "comprehensive textbook"**: Busy clinicians need scannable, dense information
- **Avoid academic verbosity**: This is clinical documentation, not a literature review or teaching document
- **Maximum lengths by complexity**:
  - Simple/standard cases: 1 page
  - Moderate complexity: 3-4 pages (first-page summary + details)
  - High complexity (rare): 5-6 pages maximum

### First Page Summary (Most Important)

**ALWAYS create a one-page executive summary as the first page:**
- The first page must contain ONLY: Title, Report Info Box, and Key Findings boxes
- This provides an at-a-glance overview similar to precision medicine reports
- Table of contents and detailed sections start on page 2 or later
- Think of it as a "clinical highlights" page that a busy clinician can scan in 30 seconds
- Use 2-4 colored boxes for different key findings (goals, interventions, decision points)
- **A strong first page can often stand alone** - subsequent pages are for details, not repetition

### SMART Goal Setting

All treatment goals should meet SMART criteria:

- **Specific**: "Improve HbA1c to <7%" not "Better diabetes control"
- **Measurable**: Use quantifiable metrics, validated scales, objective measures
- **Achievable**: Consider patient capabilities, resources, social support
- **Relevant**: Align with patient values, priorities, and life circumstances
- **Time-bound**: Define clear timeframes for goal achievement and reassessment

### Patient-Centered Care

✓ **Shared Decision-Making**: Involve patients in goal-setting and treatment choices  
✓ **Cultural Competence**: Respect cultural beliefs, language preferences, health literacy  
✓ **Patient Preferences**: Honor treatment preferences and personal values  
✓ **Individualization**: Tailor plans to patient's unique circumstances  
✓ **Empowerment**: Support patient activation and self-management  

### Evidence-Based Practice

✓ **Clinical Guidelines**: Follow current specialty society recommendations  
✓ **Quality Measures**: Incorporate HEDIS, CMS quality measures  
✓ **Comparative Effectiveness**: Use treatments with proven efficacy  
✓ **Avoid Low-Value Care**: Eliminate unnecessary tests and interventions  
✓ **Stay Current**: Update plans based on emerging evidence  

### Documentation Standards

✓ **Completeness**: Include all required elements  
✓ **Clarity**: Use clear, professional medical language  
✓ **Accuracy**: Ensure factual correctness and current information  
✓ **Timeliness**: Document plans promptly  
✓ **Legibility**: Professional formatting and organization  
✓ **Signature and Date**: Authenticate all treatment plans  

### Regulatory Compliance

✓ **HIPAA Privacy**: De-identify all protected health information  
✓ **Informed Consent**: Document patient understanding and agreement  
✓ **Billing Support**: Include documentation to support medical necessity  
✓ **Quality Reporting**: Enable extraction of quality metrics  
✓ **Legal Protection**: Maintain defensible clinical documentation  

### Multidisciplinary Coordination

✓ **Team Communication**: Share plans across care team  
✓ **Role Clarity**: Define responsibilities for each team member  
✓ **Care Transitions**: Ensure continuity across settings  
✓ **Specialist Integration**: Coordinate with subspecialty care  
✓ **Patient-Centered Medical Home**: Align with PCMH principles  

## LaTeX Template Usage

### Template Selection

Choose the appropriate template based on clinical context and desired length:

#### Concise Templates (PREFERRED)

1. **one_page_treatment_plan.tex** - **FIRST CHOICE** for most cases
   - All clinical specialties
   - Standard protocols and straightforward cases
   - Quick-reference format similar to precision oncology reports
   - Dense, scannable, clinician-focused
   - Use this unless complexity demands more detail

#### Standard Templates (3-4 pages)

Use only when one-page format is insufficient due to complexity:

2. **general_medical_treatment_plan.tex** - Primary care, chronic disease, general medicine
3. **rehabilitation_treatment_plan.tex** - PT/OT, post-surgery, injury recovery
4. **mental_health_treatment_plan.tex** - Psychiatric conditions, behavioral health
5. **chronic_disease_management_plan.tex** - Complex chronic diseases, multiple conditions
6. **perioperative_care_plan.tex** - Surgical patients, procedural care
7. **pain_management_plan.tex** - Acute or chronic pain conditions

**Note**: Even when using standard templates, adapt them to be concise (3-4 pages max) by removing non-essential sections.

### Template Structure

All LaTeX templates include:
- Professional formatting with appropriate margins and fonts
- Structured sections for all required components
- Tables for medications, interventions, timelines
- Goal-tracking sections with SMART criteria
- Space for provider signatures and dates
- HIPAA-compliant de-identification guidance
- Comments with detailed instructions

### Generating PDFs

```bash
# Compile LaTeX template to PDF
pdflatex general_medical_treatment_plan.tex

# For templates with references
pdflatex treatment_plan.tex
bibtex treatment_plan
pdflatex treatment_plan.tex
pdflatex treatment_plan.tex
```

## Validation and Quality Assurance

### Completeness Checking

Use validation scripts to ensure all required sections are present:

```bash
python check_completeness.py my_treatment_plan.tex
```

The script checks for:
- Patient information section
- Diagnosis and assessment
- SMART goals (short-term and long-term)
- Interventions (pharmacological, non-pharmacological)
- Timeline and schedule
- Monitoring parameters
- Expected outcomes
- Follow-up plan
- Patient education
- Risk mitigation

### Treatment Plan Validation

Comprehensive validation of treatment plan quality:

```bash
python validate_treatment_plan.py my_treatment_plan.tex
```

Validation includes:
- SMART goal criteria assessment
- Evidence-based intervention verification
- Timeline feasibility check
- Monitoring parameter adequacy
- Safety and risk mitigation review
- Regulatory compliance check

### Quality Checklist

Review treatment plans against the quality checklist (`quality_checklist.md`):

**Clinical Quality**
- [ ] Diagnosis is accurate and properly coded (ICD-10)
- [ ] Goals are SMART and patient-centered
- [ ] Interventions are evidence-based and guideline-concordant
- [ ] Timeline is realistic and clearly defined
- [ ] Monitoring plan is comprehensive
- [ ] Safety considerations are addressed

**Patient-Centered Care**
- [ ] Patient preferences and values incorporated
- [ ] Shared decision-making documented
- [ ] Health literacy appropriate language
- [ ] Cultural considerations addressed
- [ ] Patient education plan included

**Regulatory Compliance**
- [ ] HIPAA-compliant de-identification
- [ ] Medical necessity documented
- [ ] Informed consent noted
- [ ] Provider signature and credentials
- [ ] Date of plan creation/revision

**Coordination and Communication**
- [ ] Specialist referrals documented
- [ ] Care team roles defined
- [ ] Follow-up schedule clear
- [ ] Emergency contacts provided
- [ ] Transition planning addressed

## Integration with Other Skills

### Clinical Reports Integration

Treatment plans often accompany other clinical documentation:

- **SOAP Notes** (`clinical-reports` skill): Document ongoing implementation
- **H&P** (`clinical-reports` skill): Initial assessment informs treatment plan
- **Discharge Summaries** (`clinical-reports` skill): Summarize treatment plan execution
- **Progress Notes**: Track goal achievement and plan modifications

### Scientific Writing Integration

Evidence-based treatment planning requires literature support:

- **Citation Management** (`citation-management` skill): Reference clinical guidelines
- **Literature Review** (`literature-review` skill): Understand treatment evidence base
- **Research Lookup** (`research-lookup` skill): Find current best practices

### Research Integration

Treatment plans may be developed for clinical trials or research studies:

- **Research Grants** (`research-grants` skill): Treatment protocols for funded studies
- **Clinical Trial Reports** (`clinical-reports` skill): Intervention documentation

## Common Use Cases

### Example 1: Type 2 Diabetes Management

**Scenario**: 58-year-old patient with newly diagnosed Type 2 diabetes, HbA1c 8.5%, BMI 32

**Template**: `general_medical_treatment_plan.tex`

**Goals**:
- Short-term: Reduce HbA1c to <7.5% in 3 months
- Long-term: Achieve HbA1c <7%, lose 15 pounds in 6 months

**Interventions**:
- Pharmacological: Metformin 500mg BID, titrate to 1000mg BID
- Lifestyle: Mediterranean diet, 150 min/week moderate exercise
- Education: Diabetes self-management education, glucose monitoring

### Example 2: Post-Stroke Rehabilitation

**Scenario**: 70-year-old patient s/p left MCA stroke with right hemiparesis

**Template**: `rehabilitation_treatment_plan.tex`

**Goals**:
- Short-term: Improve right arm strength 2/5 to 3/5 in 4 weeks
- Long-term: Independent ambulation 150 feet with cane in 12 weeks

**Interventions**:
- PT 3x/week: Gait training, balance, strengthening
- OT 3x/week: ADL training, upper extremity function
- SLP 2x/week: Dysphagia therapy

### Example 3: Major Depressive Disorder

**Scenario**: 35-year-old with moderate depression, PHQ-9 score 16

**Template**: `mental_health_treatment_plan.tex`

**Goals**:
- Short-term: Reduce PHQ-9 to <10 in 8 weeks
- Long-term: Achieve remission (PHQ-9 <5), return to work

**Interventions**:
- Psychotherapy: CBT weekly sessions
- Medication: Sertraline 50mg daily, titrate to 100mg
- Lifestyle: Sleep hygiene, exercise 30 min 5x/week

### Example 4: Total Knee Arthroplasty

**Scenario**: 68-year-old scheduled for right TKA for osteoarthritis

**Template**: `perioperative_care_plan.tex`

**Preoperative Goals**:
- Optimize diabetes control (glucose <180)
- Discontinue anticoagulation per protocol
- Complete medical clearance

**Postoperative Goals**:
- Ambulate 50 feet by POD 1
- 90-degree knee flexion by POD 3
- Discharge home with PT services by POD 2-3

### Example 5: Chronic Low Back Pain

**Scenario**: 45-year-old with chronic non-specific low back pain, pain 7/10

**Template**: `pain_management_plan.tex`

**Goals**:
- Short-term: Reduce pain to 4/10 in 6 weeks
- Long-term: Return to work full-time, pain 2-3/10

**Interventions**:
- Pharmacological: Gabapentin 300mg TID, duloxetine 60mg daily
- PT: Core strengthening, McKenzie exercises 2x/week x 8 weeks
- Behavioral: CBT for pain, mindfulness meditation
- Interventional: Consider lumbar ESI if inadequate response

## Professional Standards and Guidelines

Treatment plans should align with:

### General Medicine
- American Diabetes Association (ADA) Standards of Care
- ACC/AHA Cardiovascular Guidelines
- GOLD COPD Guidelines
- JNC-8 Hypertension Guidelines
- KDIGO Chronic Kidney Disease Guidelines

### Rehabilitation
- APTA Clinical Practice Guidelines
- AOTA Practice Guidelines
- Cardiac Rehabilitation Guidelines (AHA/AACVPR)
- Stroke Rehabilitation Guidelines

### Mental Health
- APA Practice Guidelines
- VA/DoD Clinical Practice Guidelines
- NICE Guidelines (National Institute for Health and Care Excellence)
- Cochrane Reviews for psychiatric interventions

### Pain Management
- CDC Opioid Prescribing Guidelines
- AAPM/APS Chronic Pain Guidelines
- WHO Pain Ladder
- Multimodal Analgesia Best Practices

## Timeline Generation

Use the timeline generator script to create visual treatment timelines:

```bash
python timeline_generator.py --plan my_treatment_plan.tex --output timeline.pdf
```

Generates:
- Gantt chart of treatment phases
- Milestone markers for goal assessments
- Medication titration schedules
- Follow-up appointment calendar
- Intervention intensity over time

## Support and Resources

### Template Generation

Interactive template selection:

```bash
cd .claude/skills/treatment-plans/scripts
python generate_template.py

# Or specify type directly
python generate_template.py --type mental_health --output depression_treatment_plan.tex
```

### Validation Workflow

1. **Create treatment plan** using appropriate LaTeX template
2. **Check completeness**: `python check_completeness.py plan.tex`
3. **Validate quality**: `python validate_treatment_plan.py plan.tex`
4. **Review checklist**: Compare against `quality_checklist.md`
5. **Generate PDF**: `pdflatex plan.tex`
6. **Review with patient**: Ensure understanding and agreement
7. **Implement and document**: Track progress in clinical notes

### Additional Resources

- Clinical practice guidelines from specialty societies
- AHRQ Effective Health Care Program
- Cochrane Library for intervention evidence
- UpToDate and DynaMed for treatment recommendations
- CMS Quality Measures and HEDIS specifications

## Professional Document Styling

### Overview

Treatment plans can be enhanced with professional medical document styling using the `medical_treatment_plan.sty` LaTeX package. This custom style transforms plain academic documents into visually appealing, color-coded clinical documents that maintain scientific rigor while improving readability and usability.

### Medical Treatment Plan Style Package

The `medical_treatment_plan.sty` package (located in `assets/medical_treatment_plan.sty`) provides:

**Professional Color Scheme**
- **Primary Blue** (RGB: 0, 102, 153): Headers, section titles, primary accents
- **Secondary Blue** (RGB: 102, 178, 204): Light backgrounds, subtle accents
- **Accent Blue** (RGB: 0, 153, 204): Hyperlinks, key highlights
- **Success Green** (RGB: 0, 153, 76): Goals, positive outcomes
- **Warning Red** (RGB: 204, 0, 0): Warnings, critical information
- **Dark Gray** (RGB: 64, 64, 64): Body text
- **Light Gray** (RGB: 245, 245, 245): Background fills

**Styled Elements**
- Custom colored headers and footers with professional rules
- Blue section titles with underlines for clear hierarchy
- Enhanced table formatting with colored headers and alternating rows
- Optimized list spacing with colored bullets and numbering
- Professional page layout with appropriate margins

### Custom Information Boxes

The style package includes five specialized box environments for organizing clinical information:

#### 1. Info Box (Blue Border, Light Gray Background)

For general information, clinical assessments, and testing schedules:

```latex
\begin{infobox}[Title]
  \textbf{Key Information:}
  \begin{itemize}
    \item Clinical assessment details
    \item Testing schedules
    \item General guidance
  \end{itemize}
\end{infobox}
```

**Use cases**: Metabolic status, baseline assessments, monitoring schedules, titration protocols

#### 2. Warning Box (Red Border, Yellow Background)

For critical decision points, safety protocols, and alerts:

```latex
\begin{warningbox}[Alert Title]
  \textbf{Important Safety Information:}
  \begin{itemize}
    \item Critical drug interactions
    \item Safety monitoring requirements
    \item Red flag symptoms requiring immediate action
  \end{itemize}
\end{warningbox}
```

**Use cases**: Medication safety, decision points, contraindications, emergency protocols

#### 3. Goal Box (Green Border, Green-Tinted Background)

For treatment goals, targets, and success criteria:

```latex
\begin{goalbox}[Treatment Goals]
  \textbf{Primary Objectives:}
  \begin{itemize}
    \item Reduce HbA1c to <7\% within 3 months
    \item Achieve 5-7\% weight loss in 12 weeks
    \item Complete diabetes education program
  \end{itemize}
\end{goalbox}
```

**Use cases**: SMART goals, target outcomes, success metrics, CGM goals

#### 4. Key Points Box (Blue Background)

For executive summaries, key takeaways, and important recommendations:

```latex
\begin{keybox}[Key Highlights]
  \textbf{Essential Points:}
  \begin{itemize}
    \item Main therapeutic approach
    \item Critical patient instructions
    \item Priority interventions
  \end{itemize}
\end{keybox}
```

**Use cases**: Plan overview, plate method instructions, important dietary guidelines

#### 5. Emergency Box (Large Red Design)

For emergency contacts and urgent protocols:

```latex
\begin{emergencybox}
  \begin{itemize}
    \item \textbf{Emergency Services:} 911
    \item \textbf{Endocrinology Office:} [Phone] (business hours)
    \item \textbf{After-Hours Hotline:} [Phone] (nights/weekends)
    \item \textbf{Pharmacy:} [Phone and location]
  \end{itemize}
\end{emergencybox}
```

**Use cases**: Emergency contacts, critical hotlines, urgent resource information

#### 6. Patient Info Box (White with Blue Border)

For patient demographics and baseline information:

```latex
\begin{patientinfo}
  \begin{tabular}{ll}
    \textbf{Age:} & 23 years \\
    \textbf{Sex:} & Male \\
    \textbf{Diagnosis:} & Type 2 Diabetes Mellitus \\
    \textbf{Plan Start Date:} & \today \\
  \end{tabular}
\end{patientinfo}
```

**Use cases**: Patient information sections, demographic data

### Professional Table Formatting

Enhanced table environment with medical styling:

```latex
\begin{medtable}{Caption Text}
\begin{tabular}{|p{5cm}|p{4cm}|p{4.5cm}|}
\hline
\tableheadercolor  % Blue header with white text
\textcolor{white}{\textbf{Column 1}} & 
\textcolor{white}{\textbf{Column 2}} & 
\textcolor{white}{\textbf{Column 3}} \\
\hline
Data row 1 content & Value 1 & Details 1 \\
\hline
\tablerowcolor  % Alternating light gray row
Data row 2 content & Value 2 & Details 2 \\
\hline
Data row 3 content & Value 3 & Details 3 \\
\hline
\end{tabular}
\caption{Table caption}
\end{medtable}
```

**Features:**
- Blue headers with white text for visual prominence
- Alternating row colors (`\tablerowcolor`) for improved readability
- Automatic centering and spacing
- Professional borders and padding

### Using the Style Package

#### Basic Setup

1. **Add to document preamble:**

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}

% Use custom medical treatment plan style
\usepackage{medical_treatment_plan}
\usepackage{natbib}

\begin{document}
\maketitle
% Your content here
\end{document}
```

2. **Ensure style file is in same directory** as your `.tex` file, or install to LaTeX path

3. **Compile with XeLaTeX** (recommended for best results):

```bash
xelatex treatment_plan.tex
bibtex treatment_plan
xelatex treatment_plan.tex
xelatex treatment_plan.tex
```

#### Custom Title Page

The package automatically formats the title with a professional blue header:

```latex
\title{\textbf{Individualized Diabetes Treatment Plan}\\
\large{23-Year-Old Male Patient with Type 2 Diabetes}}
\author{Comprehensive Care Plan}
\date{\today}

\begin{document}
\maketitle
```

This creates an eye-catching blue box with white text and clear hierarchy.

### Compilation Requirements

**Required LaTeX Packages** (automatically loaded by the style):
- `geometry` - Page layout and margins
- `xcolor` - Color support
- `tcolorbox` with `[most]` library - Custom colored boxes
- `tikz` - Graphics and drawing
- `fontspec` - Font management (XeLaTeX/LuaLaTeX)
- `fancyhdr` - Custom headers and footers
- `titlesec` - Section styling
- `enumitem` - Enhanced list formatting
- `booktabs` - Professional table rules
- `longtable` - Multi-page tables
- `array` - Enhanced table features
- `colortbl` - Colored table cells
- `hyperref` - Hyperlinks and PDF metadata
- `natbib` - Bibliography management

**Recommended Compilation:**

```bash
# Using XeLaTeX (best font support)
xelatex document.tex
bibtex document
xelatex document.tex
xelatex document.tex

# Using PDFLaTeX (alternative)
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

### Customization Options

#### Changing Colors

Edit the style file to modify the color scheme:

```latex
% In medical_treatment_plan.sty
\definecolor{primaryblue}{RGB}{0, 102, 153}      % Modify these
\definecolor{secondaryblue}{RGB}{102, 178, 204}
\definecolor{accentblue}{RGB}{0, 153, 204}
\definecolor{successgreen}{RGB}{0, 153, 76}
\definecolor{warningred}{RGB}{204, 0, 0}
```

#### Adjusting Page Layout

Modify geometry settings in the style file:

```latex
\RequirePackage[margin=1in, top=1.2in, bottom=1.2in]{geometry}
```

#### Custom Fonts (XeLaTeX only)

Uncomment and modify in the style file:

```latex
\setmainfont{Your Preferred Font}
\setsansfont{Your Sans-Serif Font}
```

#### Header/Footer Customization

Modify in the style file:

```latex
\fancyhead[L]{\color{primaryblue}\sffamily\small\textbf{Treatment Plan Title}}
\fancyhead[R]{\color{darkgray}\sffamily\small Patient Info}
```

### Style Package Download and Installation

#### Option 1: Copy to Project Directory

Copy `assets/medical_treatment_plan.sty` to the same directory as your `.tex` file.

#### Option 2: Install to User TeX Directory

```bash
# Find your local texmf directory
kpsewhich -var-value TEXMFHOME

# Copy to appropriate location (usually ~/texmf/tex/latex/)
mkdir -p ~/texmf/tex/latex/medical_treatment_plan
cp assets/medical_treatment_plan.sty ~/texmf/tex/latex/medical_treatment_plan/

# Update TeX file database
texhash ~/texmf
```

#### Option 3: System-Wide Installation

```bash
# Copy to system texmf directory (requires sudo)
sudo cp assets/medical_treatment_plan.sty /usr/local/texlive/texmf-local/tex/latex/
sudo texhash
```

### Additional Professional Styles (Optional)

Other medical/clinical document styles available from CTAN:

**Journal Styles:**
```bash
# Install via TeX Live Manager
tlmgr install nejm        # New England Journal of Medicine
tlmgr install jama        # JAMA style
tlmgr install bmj         # British Medical Journal
```

**General Professional Styles:**
```bash
tlmgr install apa7        # APA 7th edition (health sciences)
tlmgr install IEEEtran    # IEEE (medical devices/engineering)
tlmgr install springer    # Springer journals
```

**Download from CTAN:**
- Visit: https://ctan.org/
- Search for medical document classes
- Download and install per package instructions

### Troubleshooting

**Issue: Package not found**
```bash
# Install missing packages via TeX Live Manager
sudo tlmgr update --self
sudo tlmgr install tcolorbox tikz pgf
```

**Issue: Missing characters (✓, ≥, etc.)**
- Use XeLaTeX instead of PDFLaTeX
- Or replace with LaTeX commands: `$\checkmark$`, `$\geq$`
- Requires `amssymb` package for math symbols

**Issue: Header height warnings**
- Style file sets `\setlength{\headheight}{22pt}`
- Adjust if needed for your content

**Issue: Boxes not rendering**
```bash
# Ensure complete tcolorbox installation
sudo tlmgr install tcolorbox tikz pgf
```

**Issue: Font not found (XeLaTeX)**
- Comment out custom font lines in .sty file
- Or install specified fonts on your system

### Best Practices for Styled Documents

1. **Appropriate Box Usage**
   - Match box type to content purpose (goals→green, warnings→yellow/red)
   - Don't overuse boxes; reserve for truly important information
   - Keep box content concise and focused

2. **Visual Hierarchy**
   - Use section styling for structure
   - Boxes for emphasis and organization
   - Tables for comparative data
   - Lists for sequential or grouped items

3. **Color Consistency**
   - Stick to defined color scheme
   - Use `\textcolor{primaryblue}{\textbf{Text}}` for emphasis
   - Maintain consistent meaning (red=warning, green=goals)

4. **White Space**
   - Don't overcrowd pages with boxes
   - Use `\vspace{0.5cm}` between major sections
   - Allow breathing room around colored elements

5. **Professional Appearance**
   - Maintain readability as top priority
   - Ensure sufficient contrast for accessibility
   - Test print output in grayscale
   - Keep styling consistent throughout document

6. **Table Formatting**
   - Use `\tableheadercolor` for all header rows
   - Apply `\tablerowcolor` to alternating rows in tables >3 rows
   - Keep column widths balanced
   - Use `\small\sffamily` for large tables

### Example: Styled Treatment Plan Structure

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{medical_treatment_plan}
\usepackage{natbib}

\title{\textbf{Comprehensive Treatment Plan}\\
\large{Patient-Centered Care Strategy}}
\author{Multidisciplinary Care Team}
\date{\today}

\begin{document}
\maketitle

\section*{Patient Information}
\begin{patientinfo}
  % Demographics table
\end{patientinfo}

\section{Executive Summary}
\begin{keybox}[Plan Overview]
  % Key highlights
\end{keybox}

\section{Treatment Goals}
\begin{goalbox}[SMART Goals - 3 Months]
  \begin{medtable}{Primary Treatment Targets}
    % Goals table with colored headers
  \end{medtable}
\end{goalbox}

\section{Medication Plan}
\begin{infobox}[Titration Schedule]
  % Medication instructions
\end{infobox}

\begin{warningbox}[Critical Decision Point]
  % Important safety information
\end{warningbox}

\section{Emergency Protocols}
\begin{emergencybox}
  % Emergency contacts
\end{emergencybox}

\bibliographystyle{plainnat}
\bibliography{references}
\end{document}
```

### Benefits of Professional Styling

**Clinical Practice:**
- Faster information scanning during patient encounters
- Clear visual hierarchy for critical vs. routine information
- Professional appearance suitable for patient-facing documents
- Color-coded sections reduce cognitive load

**Educational Use:**
- Enhanced readability for teaching materials
- Visual differentiation of concept types (goals, warnings, procedures)
- Professional presentation for case discussions
- Print and digital-ready formats

**Documentation Quality:**
- Modern, polished appearance
- Maintains clinical accuracy while improving aesthetics
- Standardized formatting across treatment plans
- Easy to customize for institutional branding

**Patient Engagement:**
- More approachable than dense text documents
- Color coding helps patients identify key sections
- Professional appearance builds trust
- Clear organization facilitates understanding

## Ethical Considerations

### Informed Consent
All treatment plans should involve patient understanding and voluntary agreement to proposed interventions.

### Cultural Sensitivity
Treatment plans must respect diverse cultural beliefs, health practices, and communication styles.

### Health Equity
Consider social determinants of health, access barriers, and health disparities when developing plans.

### Privacy Protection
Maintain strict HIPAA compliance; de-identify all protected health information in shared documents.

### Autonomy and Beneficence
Balance medical recommendations with patient autonomy and values while promoting patient welfare.

## License

Part of the Claude Scientific Writer project. See main LICENSE file.

---

## Reference: Readme

# Treatment Plans Skill

## Overview

Skill for generating **concise, clinician-focused** medical treatment plans across all clinical specialties. Provides LaTeX/PDF templates with SMART goal frameworks, evidence-based interventions, regulatory compliance, and validation tools for patient-centered care planning.

**Default to 1-page format** for most cases - think "quick reference card" not "comprehensive textbook".

## What's Included

### 📋 Seven Treatment Plan Types

1. **One-Page Treatment Plan** (PREFERRED) - Concise, quick-reference format for most clinical scenarios
2. **General Medical Treatment Plans** - Primary care, chronic diseases (diabetes, hypertension, heart failure)
3. **Rehabilitation Treatment Plans** - Physical therapy, occupational therapy, cardiac/pulmonary rehab
4. **Mental Health Treatment Plans** - Psychiatric care, depression, anxiety, PTSD, substance use
5. **Chronic Disease Management Plans** - Complex multimorbidity, long-term care coordination
6. **Perioperative Care Plans** - Preoperative optimization, ERAS protocols, postoperative recovery
7. **Pain Management Plans** - Acute and chronic pain, multimodal analgesia, opioid-sparing strategies

### 📚 Reference Files (5 comprehensive guides)

- `treatment_plan_standards.md` - Professional standards, documentation requirements, legal considerations
- `goal_setting_frameworks.md` - SMART goals, patient-centered outcomes, shared decision-making
- `intervention_guidelines.md` - Evidence-based treatments, pharmacological and non-pharmacological
- `regulatory_compliance.md` - HIPAA compliance, billing documentation, quality measures
- `specialty_specific_guidelines.md` - Detailed guidelines for each treatment plan type

### 📄 LaTeX Templates (7 professional templates)

- `one_page_treatment_plan.tex` - **FIRST CHOICE** - Dense, scannable 1-page format (like precision oncology reports)
- `general_medical_treatment_plan.tex` - Comprehensive medical care planning
- `rehabilitation_treatment_plan.tex` - Functional restoration and therapy
- `mental_health_treatment_plan.tex` - Psychiatric and behavioral health
- `chronic_disease_management_plan.tex` - Long-term disease management
- `perioperative_care_plan.tex` - Surgical and procedural care
- `pain_management_plan.tex` - Multimodal pain treatment

### 🔧 Validation Scripts (4 automation tools)

- `generate_template.py` - Interactive template selection and generation
- `validate_treatment_plan.py` - Comprehensive quality and compliance checking
- `check_completeness.py` - Verify all required sections present
- `timeline_generator.py` - Create visual treatment timelines and schedules

## Quick Start

### Generate a Treatment Plan Template

```bash
cd .claude/skills/treatment-plans/scripts
python generate_template.py

# Or specify type directly
python generate_template.py --type general_medical --output diabetes_plan.tex
```

Available template types:
- `one_page` (PREFERRED - use for most cases)
- `general_medical`
- `rehabilitation`
- `mental_health`
- `chronic_disease`
- `perioperative`
- `pain_management`

### Compile to PDF

```bash
cd /path/to/your/treatment/plan
pdflatex my_treatment_plan.tex
```

### Validate Your Treatment Plan

```bash
# Check for completeness
python check_completeness.py my_treatment_plan.tex

# Comprehensive validation
python validate_treatment_plan.py my_treatment_plan.tex
```

### Generate Treatment Timeline

```bash
python timeline_generator.py --plan my_treatment_plan.tex --output timeline.pdf
```

## Standard Treatment Plan Components

All templates include these essential sections:

### 1. Patient Information (De-identified)
- Demographics and relevant medical background
- Active conditions and comorbidities
- Current medications and allergies
- Functional status baseline
- HIPAA-compliant de-identification

### 2. Diagnosis and Assessment Summary
- Primary diagnosis (ICD-10 coded)
- Secondary diagnoses
- Severity classification
- Functional limitations
- Risk stratification

### 3. Treatment Goals (SMART Format)

**Short-term goals** (1-3 months):
- Specific, measurable outcomes
- Realistic targets with defined timeframes
- Patient-centered priorities

**Long-term goals** (6-12 months):
- Disease control targets
- Functional improvement objectives
- Quality of life enhancement
- Complication prevention

### 4. Interventions

- **Pharmacological**: Medications with dosages, frequencies, monitoring
- **Non-pharmacological**: Lifestyle modifications, behavioral interventions, education
- **Procedural**: Planned procedures, specialist referrals, diagnostic testing

### 5. Timeline and Schedule
- Treatment phases with timeframes
- Appointment frequency
- Milestone assessments
- Expected treatment duration

### 6. Monitoring Parameters
- Clinical outcomes to track
- Assessment tools and scales
- Monitoring frequency
- Intervention thresholds

### 7. Expected Outcomes
- Primary outcome measures
- Success criteria
- Timeline for improvement
- Long-term prognosis

### 8. Follow-up Plan
- Scheduled appointments
- Communication protocols
- Emergency procedures
- Transition planning

### 9. Patient Education
- Condition understanding
- Self-management skills
- Warning signs
- Resources and support

### 10. Risk Mitigation
- Adverse effect management
- Safety monitoring
- Emergency action plans
- Fall/infection prevention

## Common Use Cases

### 1. Type 2 Diabetes Management

```
Goal: Create comprehensive treatment plan for newly diagnosed diabetes

Template: general_medical_treatment_plan.tex

Key Components:
- SMART goals: HbA1c <7% in 3 months, weight loss 10 lbs in 6 months
- Medications: Metformin titration schedule
- Lifestyle: Diet, exercise, glucose monitoring
- Monitoring: HbA1c every 3 months, quarterly visits
- Education: Diabetes self-management education
```

### 2. Post-Stroke Rehabilitation

```
Goal: Develop rehab plan for stroke patient with hemiparesis

Template: rehabilitation_treatment_plan.tex

Key Components:
- Functional assessment: FIM scores, ROM, strength testing
- PT goals: Ambulation 150 feet with cane in 12 weeks
- OT goals: Independent ADLs, upper extremity function
- Treatment schedule: PT/OT/SLP 3x week each
- Home exercise program
```

### 3. Major Depressive Disorder

```
Goal: Create integrated treatment plan for depression

Template: mental_health_treatment_plan.tex

Key Components:
- Assessment: PHQ-9 score 16 (moderate depression)
- Goals: Reduce PHQ-9 to <5, return to work in 12 weeks
- Psychotherapy: CBT weekly sessions
- Medication: SSRI with titration schedule
- Safety planning: Crisis contacts, warning signs
```

### 4. Total Knee Replacement

```
Goal: Perioperative care plan for elective TKA

Template: perioperative_care_plan.tex

Key Components:
- Preop optimization: Medical clearance, medication management
- ERAS protocol implementation
- Postop milestones: Ambulation POD 1, discharge POD 2-3
- Pain management: Multimodal analgesia
- Rehab plan: PT starting POD 0
```

### 5. Chronic Low Back Pain

```
Goal: Multimodal pain management plan

Template: pain_management_plan.tex

Key Components:
- Pain assessment: Location, intensity, functional impact
- Goals: Reduce pain 7/10 to 3/10, return to work
- Medications: Non-opioid analgesics, adjuvants
- PT: Core strengthening, McKenzie exercises
- Behavioral: CBT for pain, mindfulness
- Interventional: Consider ESI if inadequate response
```

## SMART Goals Framework

All treatment plans use SMART criteria for goal-setting:

- **Specific**: Clear, well-defined outcome (not vague)
- **Measurable**: Quantifiable metrics or observable behaviors
- **Achievable**: Realistic given patient capabilities and resources
- **Relevant**: Aligned with patient priorities and values
- **Time-bound**: Specific timeframe for achievement

### Examples

**Good SMART Goals**:
- Reduce HbA1c from 8.5% to <7% within 3 months
- Walk independently 150 feet with assistive device by 8 weeks
- Decrease PHQ-9 depression score from 18 to <10 in 8 weeks
- Achieve knee flexion >90 degrees by postoperative day 14
- Reduce pain from 7/10 to ≤4/10 within 6 weeks

**Poor Goals** (not SMART):
- "Feel better" (not specific or measurable)
- "Improve diabetes" (not specific or time-bound)
- "Get stronger" (not measurable)
- "Return to normal" (vague, not specific)

## Workflow Examples

### Standard Treatment Plan Workflow

1. **Assess patient** - Complete history, physical, diagnostic testing
2. **Select template** - Choose appropriate template for clinical context
3. **Generate template** - `python generate_template.py --type [type]`
4. **Customize plan** - Fill in patient-specific information (de-identified)
5. **Set SMART goals** - Define measurable short and long-term goals
6. **Specify interventions** - Evidence-based pharmacological and non-pharmacological
7. **Create timeline** - Schedule appointments, milestones, reassessments
8. **Define monitoring** - Outcome measures, assessment frequency
9. **Validate completeness** - `python check_completeness.py plan.tex`
10. **Quality check** - `python validate_treatment_plan.py plan.tex`
11. **Review quality checklist** - Compare to `quality_checklist.md`
12. **Generate PDF** - `pdflatex plan.tex`
13. **Review with patient** - Shared decision-making, confirm understanding
14. **Implement and document** - Execute plan, track progress in clinical notes
15. **Reassess and modify** - Adjust plan based on outcomes

### Multidisciplinary Care Plan Workflow

1. **Identify team members** - PCP, specialists, therapists, case manager
2. **Create base plan** - Generate template for primary condition
3. **Add specialty sections** - Integrate consultant recommendations
4. **Coordinate goals** - Ensure alignment across disciplines
5. **Define communication** - Team meeting schedule, documentation sharing
6. **Assign responsibilities** - Clarify who manages each intervention
7. **Create care timeline** - Coordinate appointments across providers
8. **Share plan** - Distribute to all team members and patient
9. **Track collectively** - Shared monitoring and outcome tracking
10. **Regular team review** - Adjust plan collaboratively

## Best Practices

### Patient-Centered Care
✓ Involve patients in goal-setting and decision-making  
✓ Respect cultural beliefs and language preferences  
✓ Address health literacy with appropriate language  
✓ Align plan with patient values and life circumstances  
✓ Support patient activation and self-management  

### Evidence-Based Practice
✓ Follow current clinical practice guidelines  
✓ Use interventions with proven efficacy  
✓ Incorporate quality measures (HEDIS, CMS)  
✓ Avoid low-value or ineffective interventions  
✓ Update plans based on emerging evidence  

### Regulatory Compliance
✓ De-identify per HIPAA Safe Harbor method (18 identifiers)  
✓ Document medical necessity for billing support  
✓ Include informed consent documentation  
✓ Sign and date all treatment plans  
✓ Maintain professional documentation standards  

### Quality Documentation
✓ Complete all required sections  
✓ Use clear, professional medical language  
✓ Include specific, measurable goals  
✓ Specify exact medications (dose, route, frequency)  
✓ Define monitoring parameters and frequency  
✓ Address safety and risk mitigation  

### Care Coordination
✓ Communicate plan to entire care team  
✓ Define roles and responsibilities  
✓ Coordinate across care settings  
✓ Integrate specialist recommendations  
✓ Plan for care transitions  

## Integration with Other Skills

### Clinical Reports
- **SOAP Notes**: Document treatment plan implementation and progress
- **H&P Documents**: Initial assessment informs treatment planning
- **Discharge Summaries**: Summarize treatment plan execution
- **Progress Notes**: Track goal achievement and plan modifications

### Scientific Writing
- **Citation Management**: Reference clinical practice guidelines
- **Literature Review**: Understand evidence base for interventions
- **Research Lookup**: Find current treatment recommendations

### Research
- **Research Grants**: Treatment protocols for clinical trials
- **Clinical Trial Reports**: Document trial interventions

## Clinical Practice Guidelines

Treatment plans should align with evidence-based guidelines:

### General Medicine
- American Diabetes Association (ADA) Standards of Care
- ACC/AHA Cardiovascular Guidelines
- GOLD COPD Guidelines
- JNC-8 Hypertension Guidelines
- KDIGO Chronic Kidney Disease Guidelines

### Rehabilitation
- APTA Physical Therapy Clinical Practice Guidelines
- AOTA Occupational Therapy Practice Guidelines
- AHA/AACVPR Cardiac Rehabilitation Guidelines
- Stroke Rehabilitation Best Practices

### Mental Health
- APA (American Psychiatric Association) Practice Guidelines
- VA/DoD Clinical Practice Guidelines for Mental Health
- NICE Guidelines (UK)
- Evidence-based psychotherapy protocols (CBT, DBT, ACT)

### Pain Management
- CDC Opioid Prescribing Guidelines
- AAPM (American Academy of Pain Medicine) Guidelines
- WHO Analgesic Ladder
- Multimodal Analgesia Best Practices

### Perioperative Care
- ERAS (Enhanced Recovery After Surgery) Society Guidelines
- ASA Perioperative Guidelines
- SCIP (Surgical Care Improvement Project) Measures

## Professional Standards

### Documentation Requirements
- Complete and accurate patient information
- Clear diagnosis with appropriate ICD-10 coding
- Evidence-based interventions
- Measurable goals and outcomes
- Defined monitoring and follow-up
- Provider signature, credentials, and date

### Medical Necessity
Treatment plans must demonstrate:
- Medical appropriateness of interventions
- Alignment with diagnosis and severity
- Evidence supporting treatment choices
- Expected outcomes and benefit
- Frequency and duration justification

### Legal Considerations
- Informed consent documentation
- Patient understanding and agreement
- Risk disclosure and mitigation
- Professional liability protection
- Compliance with state/federal regulations

## Support and Resources

### Getting Help

1. **Check reference files** - Comprehensive guidance in `references/` directory
2. **Review templates** - See example structures in `assets/` directory
3. **Run validation scripts** - Identify issues with automated tools
4. **Consult SKILL.md** - Detailed documentation and best practices
5. **Review quality checklist** - Ensure all quality criteria met

### External Resources

- Clinical practice guidelines from specialty societies
- UpToDate and DynaMed for treatment recommendations
- AHRQ Effective Health Care Program
- Cochrane Library for intervention evidence
- CMS Quality Measures and HEDIS specifications
- HEDIS (Healthcare Effectiveness Data and Information Set)

### Professional Organizations

- American Medical Association (AMA)
- American Academy of Family Physicians (AAFP)
- Specialty society guidelines (ADA, ACC, AHA, APA, etc.)
- Joint Commission standards
- Centers for Medicare & Medicaid Services (CMS)

## Frequently Asked Questions

### How do I choose the right template?

Match the template to your primary clinical focus:
- **Chronic medical conditions** → general_medical or chronic_disease
- **Post-surgery or injury** → rehabilitation or perioperative
- **Psychiatric conditions** → mental_health
- **Pain as primary issue** → pain_management

### What if my patient has multiple conditions?

Use the `chronic_disease_management_plan.tex` template for complex multimorbidity, or choose the template for the primary condition and add sections for comorbidities.

### How often should treatment plans be updated?

- **Initial creation**: At diagnosis or treatment initiation
- **Regular updates**: Every 3-6 months for chronic conditions
- **Significant changes**: When goals are met or treatment is modified
- **Annual review**: Minimum for all chronic disease plans

### Can I modify the LaTeX templates?

Yes! Templates are designed to be customized. Modify sections, add specialty-specific content, or adjust formatting to meet your needs.

### How do I ensure HIPAA compliance?

- Remove all 18 HIPAA identifiers (see Safe Harbor method)
- Use age ranges instead of exact ages (e.g., "60-65" not "63")
- Remove specific dates, use relative timelines
- Omit geographic identifiers smaller than state
- Use `check_deidentification.py` script from clinical-reports skill

### What if validation scripts find issues?

Review the specific issues identified, consult reference files for guidance, and revise the plan accordingly. Common issues include:
- Missing required sections
- Goals not meeting SMART criteria
- Insufficient monitoring parameters
- Incomplete medication information

## License

Part of the Claude Scientific Writer project. See main LICENSE file.

---

For detailed documentation, see `SKILL.md`. For issues or questions, consult the comprehensive reference files in the `references/` directory.

---

## Reference: Goal_Setting_Frameworks

# Goal Setting Frameworks for Treatment Plans

## Overview

Effective treatment goals are the cornerstone of successful patient care. This reference provides comprehensive guidance on creating SMART goals, patient-centered outcome selection, and shared decision-making processes for treatment planning across all medical specialties.

## SMART Goals Framework

### Definition

**SMART** is a mnemonic for goal criteria that ensure objectives are well-defined and achievable:
- **S**pecific
- **M**easurable
- **A**chievable
- **R**elevant
- **T**ime-bound

### 1. Specific

Goals must be clear, well-defined, and unambiguous.

**Components of Specificity**:
- **What**: Exactly what will be accomplished
- **Who**: Who is responsible (patient, provider, both)
- **Where**: Context or setting if relevant
- **Which**: Specific aspect of health/function addressed

**Examples**:

| Poor (Vague) | Good (Specific) |
|--------------|-----------------|
| "Feel better" | "Reduce depressive symptoms as measured by PHQ-9 score" |
| "Improve diabetes" | "Reduce HbA1c from current 8.5% to less than 7%" |
| "Get stronger" | "Increase right quadriceps strength from 3/5 to 4/5 on manual muscle testing" |
| "Lose weight" | "Reduce body weight by 10 pounds (from 210 to 200 lbs)" |
| "Exercise more" | "Walk 30 minutes, 5 days per week" |

### 2. Measurable

Goals must include quantifiable metrics or observable criteria to track progress.

**Types of Measurement**:
- **Quantitative**: Numbers, percentages, scores, scales
  - Lab values: HbA1c, LDL cholesterol, eGFR
  - Vital signs: BP, heart rate, weight
  - Scales: Pain (0-10 NRS), PHQ-9, GAD-7, FIM
  - Functional: Distance walked, ROM degrees, strength grades
  
- **Qualitative Observable**: Behaviors that can be observed and verified
  - "Patient demonstrates proper insulin injection technique"
  - "Patient ambulates 150 feet with walker independently"
  - "Patient follows 2-step commands"

**Examples**:

| Not Measurable | Measurable |
|----------------|------------|
| "Better blood pressure" | "Systolic BP <130 mmHg and diastolic BP <80 mmHg" |
| "Less pain" | "Pain intensity reduced from 7/10 to ≤4/10 on numeric rating scale" |
| "Improved mobility" | "Ambulate 300 feet with front-wheeled walker, supervision level" |
| "Take medications regularly" | "Medication adherence >90% as measured by refill rates" |
| "Sleep better" | "Sleep 7-8 hours nightly with <2 awakenings per night" |

### 3. Achievable

Goals must be realistic given patient's capabilities, resources, and circumstances.

**Factors to Consider**:
- **Patient capabilities**: Physical, cognitive, psychological capacity
- **Severity of condition**: Advanced disease may have limited improvement potential
- **Treatment efficacy**: What can realistically be achieved with available treatments
- **Resources**: Access to care, medications, equipment, support
- **Time available**: Adequate time to achieve the goal
- **Motivation**: Patient's readiness to change and engagement

**Setting Achievable Goals**:
- Start with baseline assessment
- Know expected treatment effects (e.g., metformin reduces HbA1c by 1-1.5%)
- Set incremental goals for large changes (lose 5 lbs, then 10 lbs, rather than jump to 50 lbs)
- Challenge but don't overwhelm patient
- Adjust goals based on progress

**Examples**:

| Not Achievable | Achievable |
|----------------|------------|
| "Marathon ready in 1 month" (sedentary 70-year-old post-MI) | "Walk 1 mile continuously in 3 months" |
| "HbA1c from 12% to <6% in 6 weeks" | "HbA1c from 12% to <9% in 3 months, <7% in 6 months" |
| "Full knee ROM 0-140° by POD 3" (post-TKA) | "Knee ROM 0-90° by week 2, 0-110° by week 6" |
| "Cure chronic pain" | "Reduce pain from 7/10 to 4/10 and improve function by 30%" |

### 4. Relevant

Goals must align with patient values, priorities, and overall treatment objectives.

**Relevance Criteria**:
- **Patient-centered**: Matters to the patient, reflects their priorities
- **Clinically meaningful**: Achieving goal improves health or quality of life
- **Aligned with diagnosis**: Goal addresses the condition being treated
- **Appropriate timing**: Right goal for current phase of treatment
- **Integrated**: Fits with other treatment goals

**Assessing Relevance**:
- Ask patient: "What's most important to you?" "What do you want to be able to do?"
- Ensure goals address functional limitations that matter to patient
- Connect clinical metrics to patient-meaningful outcomes (e.g., "HbA1c <7% reduces risk of vision loss")
- Avoid provider-driven goals that don't resonate with patient

**Examples**:

| Less Relevant | More Relevant |
|---------------|---------------|
| "Reduce medication count" (when medications controlling symptoms well) | "Simplify regimen to improve adherence" (if missing doses due to complexity) |
| "Perfect blood sugars" (patient's priority is energy) | "Improve energy levels through better glucose control" |
| "Walk 5 miles" (patient just wants to shop independently) | "Walk through grocery store without assistance" |

### 5. Time-Bound

Goals must have specific deadlines or timeframes for achievement.

**Timeframe Considerations**:
- **Short-term goals**: Days to 3 months
- **Intermediate goals**: 3-6 months
- **Long-term goals**: 6-12 months or longer for chronic conditions
- **Reassessment intervals**: Check progress at defined intervals

**Time Elements to Include**:
- Target date or timeframe
- Checkpoint dates for progress review
- Frequency of actions (e.g., "exercise 30 min, 5x/week")

**Examples**:

| Not Time-Bound | Time-Bound |
|----------------|------------|
| "Eventually lose weight" | "Lose 15 pounds within 6 months (approximately 1-2 lbs/week)" |
| "Attend physical therapy" | "Complete 12 physical therapy sessions over 8 weeks, 1-2x weekly" |
| "When ready, return to work" | "Return to modified duty work within 12 weeks post-surgery" |
| "Improve depression symptoms" | "Reduce PHQ-9 score from 18 to <10 within 8 weeks of starting SSRI and CBT" |

## Creating SMART Goals: Step-by-Step Process

### Step 1: Assess Baseline
- Identify current status: symptoms, lab values, functional level
- Use standardized assessments when available
- Document quantitative baseline

### Step 2: Identify Desired Outcome
- What needs to improve?
- Engage patient: "What would you like to be different?"
- Consider clinical needs and patient priorities

### Step 3: Make It Specific
- Define exact outcome
- Eliminate vague language
- Include all relevant details

### Step 4: Add Measurement
- How will progress be tracked?
- What metric or observable behavior?
- Baseline → Target value

### Step 5: Reality Check (Achievable?)
- Is this possible given patient's condition, resources, treatment effects?
- May need to adjust expectations
- Set incremental goals if needed

### Step 6: Ensure Relevance
- Does patient care about this goal?
- Is it clinically meaningful?
- Does it align with overall treatment plan?

### Step 7: Set Timeline
- When will goal be achieved?
- When will progress be reviewed?
- Break into short-term and long-term if needed

### Step 8: Document and Communicate
- Write goal in clear SMART format
- Share with patient and care team
- Ensure patient understanding

## Goal Hierarchies and Levels

### ICF Framework (International Classification of Functioning, Disability and Health)

Useful for rehabilitation and functional goals:

1. **Impairment-Level Goals**: Body structure/function
   - Example: "Increase shoulder flexion ROM from 90° to 140°"
   
2. **Activity-Level Goals**: Task performance
   - Example: "Dress upper body independently"
   
3. **Participation-Level Goals**: Life role engagement
   - Example: "Return to work as teacher"

### Medical Outcome Levels

1. **Biological/Clinical Goals**: Lab values, vital signs, disease markers
   - Example: "HbA1c <7%, BP <130/80, LDL <70 mg/dL"
   
2. **Symptom Goals**: Patient-reported symptoms
   - Example: "Pain ≤4/10, no dyspnea with ADLs"
   
3. **Functional Goals**: What patient can do
   - Example: "Walk 1 mile, climb 2 flights of stairs"
   
4. **Quality of Life Goals**: Overall well-being
   - Example: "Return to hobbies, improve sleep quality"

## Patient-Centered Outcome Measures (PCOMs)

### Definition
Outcomes that matter most to patients, beyond traditional clinical metrics.

### Common PCOMs

**Patient-Reported Outcome Measures (PROMs)**:
- SF-36 or SF-12 (general health-related quality of life)
- PROMIS (Patient-Reported Outcomes Measurement Information System)
- Disease-specific QoL scales (e.g., Kansas City Cardiomyopathy Questionnaire for HF)

**Functional Outcomes**:
- Activities of Daily Living (ADLs): Bathing, dressing, toileting, transferring, feeding, continence
- Instrumental ADLs (IADLs): Shopping, cooking, housekeeping, managing finances, transportation
- Occupational/educational functioning
- Social functioning and relationships
- Recreation and leisure participation

**Patient Priorities**:
- What matters most to individual patient
- May differ from clinician priorities
- Examples: "Play with grandchildren," "Travel to daughter's wedding," "Avoid nursing home"

### Integrating PCOMs into Goals

**Approach**:
1. Ask patient about priorities early in assessment
2. Link clinical goals to patient-meaningful outcomes
3. Include at least some goals directly addressing patient priorities
4. Use patient's language in documenting goals when possible

**Example Integration**:
- **Clinical goal**: "Reduce HbA1c from 8.5% to <7% in 3 months"
- **Linked patient-centered goal**: "Improve energy levels to play with grandchildren without fatigue"
- Both goals documented, progress on both tracked

## Shared Decision-Making in Goal Setting

### What is Shared Decision-Making (SDM)?

Collaborative process where clinicians and patients jointly:
- Discuss treatment options
- Weigh risks and benefits
- Consider patient values and preferences
- Make decisions together

### SDM in Treatment Goal Setting

**Steps**:

1. **Choice Awareness**: Acknowledge multiple possible goals/approaches
   - "We could focus on aggressive HbA1c lowering vs. minimizing hypoglycemia risk. What's more important to you?"

2. **Option Presentation**: Present goal options with pros/cons
   - "Option A: Intensive BP control (<120/80) reduces stroke risk but requires more medications. Option B: Standard control (<140/90) is easier but slightly higher stroke risk."

3. **Values Clarification**: Understand patient priorities
   - "How do you feel about taking multiple medications?" "How much does avoiding injections matter to you?"

4. **Preference Integration**: Incorporate preferences into goals
   - If patient prioritizes avoiding medications → "Control BP with lifestyle changes and one medication if possible"

5. **Decision**: Agree on goals together
   - "It sounds like you'd like to try intensive lifestyle changes for 3 months before adding another medication. Let's plan for that."

6. **Document**: Record shared decision-making process
   - "Goals established through shared decision-making. Patient expressed preference for..."

### Decision Aids

Tools to facilitate SDM:
- Option grids comparing approaches
- Numerical risk/benefit data
- Patient stories/testimonials
- Visual aids (pictures, diagrams)
- "What matters to you" worksheets

## Special Considerations for Different Populations

### Older Adults
- Functional independence often priority over disease-specific metrics
- Balance aggressive treatment vs. treatment burden
- Consider life expectancy and time to benefit
- Fall prevention, polypharmacy reduction may be key goals
- Quality over quantity of life

### Pediatric
- Developmental stage-appropriate goals
- Family-centered (involve parents/caregivers)
- Growth and development milestones
- School/social functioning
- Transition planning (pediatric to adult care)

### Chronic Disease
- Long-term sustainable goals
- Balance ambition with realistic expectations
- Complication prevention
- Quality of life maintenance
- Adaptation and acceptance alongside improvement

### Palliative/End-of-Life
- Comfort and symptom management primary
- Functional goals focused on valued activities
- Psychosocial and spiritual needs
- Caregiver support
- Dignity and autonomy

### Complex Multi-Morbidity
- Prioritize most impactful goals
- Coordinate goals across conditions (when treatments overlap, even better)
- Avoid conflicting treatments
- Minimize treatment burden
- Realistic expectations with multiple conditions

## Common Goal-Setting Pitfalls

### Pitfall 1: Provider-Centric Goals
**Problem**: Goals reflect what provider thinks is important, not patient priorities  
**Solution**: Ask patient early in visit what they hope to achieve, incorporate their language

### Pitfall 2: Too Many Goals
**Problem**: Overwhelming patient with 10+ goals  
**Solution**: Prioritize 3-5 key goals, build on success

### Pitfall 3: All-or-Nothing Thinking
**Problem**: Goal is "cure" or "perfection"  
**Solution**: Incremental goals, meaningful improvement valued

### Pitfall 4: Ignoring Barriers
**Problem**: Goals set without assessing feasibility (resources, support, access)  
**Solution**: Identify barriers during assessment, problem-solve or adjust goals

### Pitfall 5: Static Goals
**Problem**: Set goals and never revisit  
**Solution**: Regular reassessment, modify as patient progresses or circumstances change

### Pitfall 6: Purely Clinical Metrics
**Problem**: All goals are lab values, no functional or QoL goals  
**Solution**: Balance clinical markers with functional, symptom, and QoL outcomes

### Pitfall 7: No Patient Buy-In
**Problem**: Patient doesn't believe goal is achievable or important  
**Solution**: Shared decision-making, motivational interviewing to explore ambivalence

## Examples of SMART Goals by Condition

### Diabetes
**Short-term**: "Reduce HbA1c from 8.5% to <7.5% within 3 months by initiating metformin 1000mg BID and reducing carbohydrate intake to 45-60g per meal."

**Long-term**: "Maintain HbA1c <7% for 6+ months, prevent microvascular complications, and improve energy levels to engage in daily walking for 30 minutes."

### Heart Failure
**Short-term**: "Achieve euvolemia (no edema, stable weight within 2 lbs) within 2 weeks through furosemide dose optimization and sodium restriction <2000mg/day."

**Long-term**: "Maintain NYHA Class II functional status, prevent HF hospitalizations, and walk 1/4 mile without dyspnea within 3 months."

### Depression
**Short-term**: "Reduce PHQ-9 score from 18 to <10 within 8 weeks by starting escitalopram 10mg daily and attending weekly CBT sessions."

**Long-term**: "Achieve depression remission (PHQ-9 <5), return to work full-time, and re-engage in social activities with friends 2-3x/week within 4 months."

### Post-Stroke Rehabilitation
**Short-term**: "Increase right arm strength from 2/5 to 3+/5 and improve Functional Independence Measure (FIM) score from 85 to 100 within 4 weeks through PT/OT 5x/week."

**Long-term**: "Achieve independence in all ADLs, ambulate 500 feet with cane on level surfaces, and return home (not nursing facility) within 3 months."

### Chronic Low Back Pain
**Short-term**: "Reduce pain intensity from 7/10 to 4/10 and increase walking tolerance from 10 minutes to 30 minutes within 6 weeks using multimodal analgesia (SNRI, NSAID, PT)."

**Long-term**: "Return to modified duty work within 3 months, engage in hobbies (fishing, gardening with adaptations), and reduce pain interference on daily life by 50% (Brief Pain Inventory)."

### Hypertension
**Short-term**: "Reduce blood pressure from 152/94 to <140/90 mmHg within 4 weeks by initiating lisinopril 10mg daily and reducing sodium intake to <2300mg/day."

**Long-term**: "Achieve and maintain BP <130/80 mmHg, reduce ASCVD 10-year risk from 15% to <10%, and prevent cardiovascular events."

## Tools and Resources

### Goal-Setting Templates
- SMART goal worksheet (fill-in-the-blank format)
- Goal-tracking sheets for patients
- Motivational interviewing "change talk" to elicit goals

### Assessment Tools
- Goal Attainment Scaling (GAS): Personalized outcome measure
- Canadian Occupational Performance Measure (COPM): Patient-identified functional goals
- Patient-Reported Outcomes Measurement Information System (PROMIS)

### Patient Education
- "Setting Health Goals" handouts
- Goal visualization exercises
- Tracking apps and logs

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: January 2026

---

## Reference: Intervention_Guidelines

# Evidence-Based Intervention Guidelines

## Overview

This reference provides comprehensive guidance on selecting, implementing, and documenting evidence-based interventions across pharmacological, non-pharmacological, and procedural treatment modalities. These guidelines support treatment plan development with current best practices and clinical recommendations.

## Evidence Hierarchy

### Levels of Evidence

**Level I: Highest Quality**
- Systematic reviews and meta-analyses of randomized controlled trials (RCTs)
- Large multi-center RCTs

**Level II: High Quality**
- Individual RCTs
- Systematic reviews of observational studies

**Level III: Moderate Quality**
- Cohort studies
- Case-control studies
- Well-designed observational studies

**Level IV: Lower Quality**
- Case series
- Case reports
- Expert opinion

**Recommendation Strength**:
- **Grade A**: Strong recommendation, high-quality evidence
- **Grade B**: Moderate recommendation, moderate-quality evidence  
- **Grade C**: Weak recommendation, low-quality evidence
- **Grade D**: Recommendation against (evidence of harm or no benefit)

## Pharmacological Interventions

### Medication Selection Principles

#### 1. Evidence-Based Prescribing
- Use medications with proven efficacy for indication
- Follow clinical practice guidelines
- Consider comparative effectiveness data
- Prefer medications with better safety profiles when equivalent efficacy

#### 2. Patient-Specific Factors
- Comorbidities and contraindications
- Organ function (renal, hepatic)
- Drug allergies and intolerances
- Concurrent medications (drug interactions)
- Age, pregnancy status
- Genetic factors (pharmacogenomics when available)
- Cost and insurance coverage

#### 3. Medication Safety
- Start low, go slow (especially in elderly, multiple comorbidities)
- Titrate to target dose based on response and tolerance
- Monitor for adverse effects
- Avoid potentially inappropriate medications (Beers Criteria for elderly)
- Polypharmacy reduction when possible

### Common Medication Classes by Indication

#### Hypertension

**First-Line Agents** (per JNC-8, ACC/AHA guidelines):
- **ACE Inhibitors** (lisinopril, enalapril): Preferred if diabetes, CKD, or heart failure
- **ARBs** (losartan, valsartan): Alternative to ACE if intolerant
- **Calcium Channel Blockers** (amlodipine): Particularly effective in elderly, Black patients
- **Thiazide Diuretics** (chlorthalidone, HCTZ): Cost-effective, good CV outcomes

**Dosing Strategy**:
- Start single agent at low dose
- Titrate to maximum tolerated dose before adding second agent
- Combination therapy often needed (2-3 agents)
- Monitor BP response, adjust every 2-4 weeks

#### Type 2 Diabetes Mellitus

**First-Line** (ADA Standards of Care):
- **Metformin**: First-line for all patients unless contraindicated (eGFR <30)
  - Start 500-850mg daily or BID, titrate to 2000mg total daily

**Second-Line** (individualize based on comorbidities):
- **SGLT2 Inhibitors** (empagliflozin, dapagliflozin): If heart failure or CKD (strong cardio-renal benefits)
- **GLP-1 Receptor Agonists** (semaglutide, dulaglutide): If ASCVD or high risk, weight loss needed
- **DPP-4 Inhibitors** (sitagliptin): If low hypoglycemia risk desired
- **Sulfonylureas** (glipizide): Cost-effective but hypoglycemia risk
- **Insulin**: If HbA1c very elevated ($>$10%) or symptoms of hyperglycemia

#### Depression

**First-Line SSRIs** (APA guidelines):
- Sertraline, escitalopram, fluoxetine, citalopram, paroxetine
- Start low (e.g., sertraline 50mg, escitalopram 10mg)
- Titrate after 2-4 weeks if partial response
- Full trial: 6-8 weeks at therapeutic dose
- Continue 6-12 months after remission (longer if recurrent)

**Second-Line**:
- **SNRIs** (venlafaxine, duloxetine): Especially if chronic pain comorbidity
- **Bupropion**: If sexual dysfunction concern, smoking cessation
- **Mirtazapine**: If insomnia/appetite stimulation needed

**Augmentation** (if partial response):
- Second antidepressant from different class
- Atypical antipsychotic (aripiprazole, quetiapine) - FDA-approved augmentation
- Lithium, thyroid hormone (triiodothyronine)

#### Chronic Pain

**Multimodal Analgesia** (WHO Pain Ladder, CDC Opioid Guidelines):

**Non-Opioid Analgesics**:
- **Acetaminophen**: 3-4g/day divided, safe if liver function normal
- **NSAIDs**: Ibuprofen, naproxen, meloxicam - short-term or chronic with GI protection
  - Monitor: Renal function, BP, GI bleeding risk

**Adjuvant Analgesics for Neuropathic Pain**:
- **Gabapentin**: 300mg titrated to 1800-3600mg/day divided TID
- **Pregabalin**: 75mg BID titrated to 150-300mg BID (better bioavailability than gabapentin)
- **SNRIs** (duloxetine): 60mg daily for diabetic neuropathy, chronic MSK pain
- **TCAs** (amitriptyline, nortriptyline): Low-dose (10-75mg QHS) - second-line due to side effects

**Topical Agents**:
- Lidocaine patches 5%, diclofenac gel, capsaicin cream
- Local effect, minimal systemic absorption

**Opioids** (CDC guidelines - use cautiously):
- Only after non-opioid multimodal therapies inadequate
- Lowest effective dose, short-acting preferred initially
- Avoid $>$90 MME/day if possible
- UDS, PDMP monitoring, naloxone co-prescription
- Reassess frequently, taper if not meeting functional goals

#### Heart Failure with Reduced Ejection Fraction (HFrEF)

**Guideline-Directed Medical Therapy (GDMT)** - "Foundational Four":

1. **ACE Inhibitor or ARB or ARNI**
   - ACE: Lisinopril 20-40mg daily, enalapril 10-20mg BID
   - ARNI (Sacubitril/Valsartan): 24/26mg BID → 97/103mg BID (superior to ACE/ARB)
   - Monitor: BP, renal function, potassium

2. **Beta-Blocker**
   - Carvedilol 3.125-6.25mg BID → 25mg BID (target)
   - Metoprolol succinate 12.5-25mg daily → 200mg daily
   - Bisoprolol 1.25mg → 10mg daily
   - Titrate slowly, monitor HR, BP

3. **Mineralocorticoid Receptor Antagonist (MRA)**
   - Spironolactone 12.5-25mg daily (up to 50mg)
   - Eplerenone 25mg daily → 50mg daily
   - Monitor: Potassium, renal function (risk hyperkalemia)

4. **SGLT2 Inhibitor**
   - Dapagliflozin 10mg daily or empagliflozin 10mg daily
   - Reduces HF hospitalizations and mortality
   - Also beneficial for diabetes and CKD

**Additional Therapies**:
- Loop diuretic (furosemide) for volume management (not mortality benefit)
- Hydralazine-isosorbide dinitrate (if African American or intolerant to ACE/ARB)
- Ivabradine (if EF $\leq$35%, HR $>$70 on max beta-blocker)
- Digoxin (symptomatic benefit, reduce hospitalizations)

### Medication Documentation Best Practices

**Include in Treatment Plan**:
- Generic name (brand name optional)
- Dose, route, frequency
- Indication/rationale
- Titration plan if applicable
- Expected timeline for benefit
- Key side effects to monitor
- Drug interactions
- When to adjust or discontinue

**Example**: "Lisinopril 10mg PO daily - ACE inhibitor for hypertension and renal protection in diabetes. Titrate to 20mg in 2-4 weeks if BP not at goal and tolerating (monitor for cough, hyperkalemia). Target BP <130/80."

## Non-Pharmacological Interventions

### Lifestyle Modifications

#### Diet and Nutrition

**Mediterranean Diet** (Evidence: multiple RCTs, PREDIMED trial):
- **Indications**: Cardiovascular disease prevention, diabetes management
- **Components**:
  - High intake: Fruits, vegetables, whole grains, legumes, nuts, olive oil
  - Moderate: Fish, poultry
  - Low: Red meat, sweets
- **Evidence**: Reduces cardiovascular events by 30%, improves glucose control
- **Implementation**: Dietitian referral for medical nutrition therapy

**DASH Diet** (Dietary Approaches to Stop Hypertension):
- **Indication**: Hypertension
- **Components**: High fruits/vegetables, low-fat dairy, reduced sodium (<2300mg, ideally <1500mg)
- **Evidence**: Reduces SBP by 8-14 mmHg
- **Implementation**: DASH eating plan education, sodium tracking

**Carbohydrate Counting** (for Diabetes):
- Consistent carbohydrate intake: 45-60g per meal
- Enables insulin dosing adjustment
- Prevents glycemic variability
- Dietitian teaches carb counting skills

**Weight Management**:
- Caloric deficit: 500-750 kcal/day for 1-2 lb/week weight loss
- Behavior change strategies: Self-monitoring, stimulus control, goal-setting
- Structured programs (Weight Watchers, MOVE!, etc.) more effective than self-directed
- Pharmacotherapy (GLP-1 agonists, orlistat) or bariatric surgery for BMI $\geq$30-35 with comorbidities

#### Physical Activity and Exercise

**Aerobic Exercise**:
- **Recommendation**: 150 min/week moderate intensity OR 75 min/week vigorous
- **Moderate**: Brisk walking, cycling, swimming - can talk but not sing
- **Vigorous**: Running, fast cycling - can say few words before pause
- **Benefits**: Cardiovascular health, glucose control, weight management, mood
- **Implementation**: Start with 10 min sessions, gradually increase

**Resistance Training**:
- **Recommendation**: 2-3 sessions/week, all major muscle groups
- **Benefits**: Muscle strength, bone density, metabolic rate, glucose control
- **Implementation**: Bodyweight exercises, resistance bands, free weights, machines

**Balance and Flexibility**:
- Important for fall prevention in elderly
- Yoga, tai chi
- Stretching routines

**Exercise Prescription**:
- FITT principle: **F**requency, **I**ntensity, **T**ime, **T**ype
- Individualize based on fitness level, comorbidities, goals
- Cardiac clearance if indicated (using ACSM or ACC/AHA guidelines)

**Example**: "Aerobic exercise: Walk 30 minutes, 5 days/week at moderate intensity (target HR 50-70% max). Resistance training: Upper and lower body exercises 2x/week, 2 sets of 10-12 reps."

#### Smoking Cessation

**Evidence**: Strongest intervention for COPD, cardiovascular disease, cancer prevention

**5 A's Approach**:
1. **Ask**: Screen all patients for tobacco use
2. **Advise**: Urge all tobacco users to quit
3. **Assess**: Willingness to make quit attempt
4. **Assist**: Aid in quitting (counseling + medication)
5. **Arrange**: Follow-up contact

**Pharmacotherapy** (doubles quit rates):
- **Nicotine Replacement**: Patch, gum, lozenge - OTC, safe
- **Varenicline**: Most effective (Chantix), start 1 week before quit date
- **Bupropion**: Alternative, also treats depression
- **Combination**: NRT + varenicline/bupropion more effective

**Counseling**:
- Quitline: 1-800-QUIT-NOW
- Individual or group counseling
- Cognitive-behavioral techniques

**Implementation**: Set quit date within 30 days, prescribe pharmacotherapy + counseling referral, follow up within 1 week of quit date.

#### Sleep Hygiene

**Indications**: Insomnia, poor sleep quality

**Components**:
- Consistent sleep-wake schedule (same bedtime/wake time)
- Bedroom: Dark, quiet, cool (60-67°F)
- Avoid: Caffeine after 2 PM, alcohol, large meals before bed
- Screen time: Stop 1 hour before bed
- Wind-down routine: Reading, bath, relaxation
- Use bed only for sleep (not TV, work)
- If can't sleep after 20 min, get up and do quiet activity

**Evidence**: Effective for chronic insomnia, often combined with CBT for insomnia (CBT-I)

#### Stress Management

**Techniques**:
- **Mindfulness meditation**: 10-20 min daily, reduces anxiety, depression
- **Progressive muscle relaxation**: Systematic tensing and relaxing muscle groups
- **Deep breathing**: Diaphragmatic breathing, 4-7-8 technique
- **Yoga, tai chi**: Mind-body practices
- **Cognitive restructuring**: Challenge stress-inducing thoughts

**Evidence**: Reduces stress hormones, improves mood, pain perception

### Behavioral Interventions

#### Cognitive Behavioral Therapy (CBT)

**Indications**: Depression, anxiety, insomnia, chronic pain, substance use

**Core Components**:
- Psychoeducation
- Cognitive restructuring (identify and challenge distorted thoughts)
- Behavioral activation (increase rewarding activities)
- Problem-solving skills
- Relapse prevention

**Evidence**: Equivalent to antidepressants for mild-moderate depression, first-line for anxiety, insomnia

**Implementation**: 12-16 weekly 50-min sessions with trained therapist, homework between sessions

**Variants**:
- **CBT-I** (insomnia): Sleep restriction, stimulus control, cognitive therapy for sleep
- **CBT-CP** (chronic pain): Pain education, activity pacing, cognitive restructuring of pain catastrophizing

#### Motivational Interviewing (MI)

**Indication**: Ambivalence about behavior change (diet, exercise, substance use, medication adherence)

**Principles**:
- Express empathy
- Develop discrepancy (between current behavior and goals/values)
- Roll with resistance (don't argue)
- Support self-efficacy

**Techniques**:
- Open-ended questions
- Affirmations
- Reflective listening
- Summarizing
- Elicit "change talk"

**Evidence**: Effective for initiating behavior change in multiple domains

### Patient Education and Self-Management

**Components**:
- Disease education (pathophysiology, natural history, treatment)
- Self-monitoring skills (blood glucose, BP, weight, symptoms)
- Medication management (purpose, dosing, side effects)
- Symptom recognition and action plans
- Lifestyle modification skills
- Problem-solving
- When to seek care

**Evidence**: Self-management education improves outcomes in diabetes, asthma, heart failure, chronic pain

**Delivery**:
- Individual education by clinician or educator
- Structured programs (DSMES for diabetes, cardiac rehab for heart disease)
- Group classes
- Written materials, videos, apps

## Procedural and Interventional Therapies

### Rehabilitation Therapies

#### Physical Therapy

**Indications**: Musculoskeletal injuries, post-surgical rehabilitation, balance/gait disorders, chronic pain

**Interventions**:
- Therapeutic exercise: Strengthening, stretching, endurance
- Manual therapy: Soft tissue mobilization, joint mobilization
- Gait and balance training
- Modalities: Heat, ice, ultrasound, electrical stimulation, TENS
- Functional training: ADL retraining, body mechanics

**Evidence**: Strong evidence for specific conditions (e.g., PT for knee OA reduces pain and improves function equivalent to NSAIDs)

**Prescription**: Frequency (e.g., 2-3x/week), duration (e.g., 4-8 weeks), specific interventions/goals

#### Occupational Therapy

**Indications**: ADL limitations, upper extremity dysfunction, cognitive-perceptual deficits, work-related injuries

**Interventions**:
- ADL/IADL training
- Adaptive equipment and environmental modifications
- Upper extremity strengthening and coordination
- Energy conservation techniques
- Cognitive rehabilitation
- Work hardening/conditioning

**Evidence**: Improves independence post-stroke, post-injury, with chronic conditions

#### Speech-Language Pathology

**Indications**: Dysphagia, aphasia, dysarthria, cognitive-communication disorders

**Interventions**:
- Swallow therapy and diet modifications
- Language therapy (aphasia)
- Articulation therapy
- Cognitive-linguistic therapy
- Augmentative and alternative communication (AAC)

### Interventional Pain Procedures

#### Epidural Steroid Injections (ESI)

**Indication**: Radicular pain from disc herniation or spinal stenosis

**Evidence**: Moderate-quality evidence for short-term pain relief (3-6 weeks to 3 months), variable long-term benefit

**Approach**: Fluoroscopy-guided, transforaminal, interlaminar, or caudal

**Frequency**: Up to 3-4 injections per year

**Risks**: Infection, bleeding, nerve injury (rare), dural puncture

#### Radiofrequency Ablation (RFA)

**Indication**: Facet joint-mediated pain (after positive diagnostic medial branch blocks)

**Evidence**: Good evidence for lumbar facet pain relief for 6-12 months

**Procedure**: Thermal lesioning of medial branch nerves supplying facet joints

**Repeatable**: Can repeat when pain returns

#### Spinal Cord Stimulation (SCS)

**Indication**: Refractory chronic neuropathic pain (failed back surgery syndrome, CRPS, diabetic neuropathy)

**Evidence**: 50-60% achieve $\geq$50% pain relief, improves function

**Procedure**: Trial lead placement (5-7 days), if successful → permanent implant

**Technologies**: Traditional, high-frequency, burst stimulation, dorsal root ganglion (DRG)

### Surgical Interventions

**When to Refer for Surgery**:
- Failed conservative management (adequate trial - typically 6-12 weeks minimum)
- Progressive neurologic deficit
- Cauda equina syndrome (emergency)
- Severe functional limitation affecting quality of life
- Structural pathology amenable to surgical correction
- Patient preference after risks/benefits discussion

**Shared Decision-Making**: Discuss operative vs. non-operative management, risks, benefits, expected outcomes, recovery

## Integrative and Complementary Therapies

### Acupuncture

**Evidence**:
- **Moderate evidence** for chronic low back pain, osteoarthritis knee pain, tension headaches, migraine
- **Mechanism**: Unclear (endorphin release, gate control theory, placebo)

**Implementation**: 8-12 sessions by licensed acupuncturist

### Massage Therapy

**Evidence**: Modest benefit for chronic low back pain, anxiety, cancer-related symptoms

**Types**: Swedish, deep tissue, myofascial release

**Implementation**: 1-2x/week, 30-60 min sessions

### Yoga

**Evidence**: Improves back pain, balance, flexibility, reduces stress and anxiety

**Types**: Hatha (gentle), Vinyasa (flowing), Iyengar (alignment-focused)

**Implementation**: Group classes or home practice, 2-3x/week

### Mindfulness-Based Stress Reduction (MBSR)

**Evidence**: Reduces stress, anxiety, depression, chronic pain

**Program**: 8-week structured program, weekly 2.5-hour sessions, daily home practice

**Components**: Meditation, body scan, mindful movement (yoga)

### Chiropractic Care

**Evidence**: Effective for acute and chronic low back pain, neck pain

**Techniques**: Spinal manipulation, mobilization, soft tissue therapy

**Safety**: Generally safe, avoid high-velocity manipulation if osteoporosis, spinal instability

## Intervention Selection and Documentation

### Treatment Algorithm Approach

1. **Diagnosis-Specific**: Follow evidence-based guidelines for condition
2. **Severity-Appropriate**: Mild → conservative; severe → aggressive
3. **Stepwise Intensification**: Start with first-line, add or switch if inadequate response
4. **Multimodal**: Combine complementary interventions (pharmacologic + non-pharmacologic)
5. **Individualized**: Adjust for patient factors (comorbidities, preferences, resources)

### Documentation Template

For each intervention, document:
- **Intervention**: Specific name/type
- **Indication**: Why this intervention for this patient
- **Evidence**: Guideline-based, RCT data supporting use
- **Dose/Frequency/Duration**: Specific parameters
- **Expected Benefit**: What should improve, by how much, when
- **Monitoring**: How will response be assessed
- **Risks/Side Effects**: Key concerns to monitor
- **Alternatives Considered**: What else was considered, why not chosen

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: January 2026

---

## Reference: Regulatory_Compliance

# Regulatory Compliance for Treatment Plans

## Overview

Treatment plans must comply with multiple federal and state regulations governing healthcare documentation, patient privacy, billing practices, and quality standards. This reference provides comprehensive guidance on regulatory requirements affecting treatment plan development and implementation.

## HIPAA Privacy and Security

### Health Insurance Portability and Accountability Act (HIPAA)

**Applicable Rules**:
- Privacy Rule (45 CFR Part 164, Subpart E)
- Security Rule (45 CFR Part 164, Subparts A and C)
- Breach Notification Rule (45 CFR Part 164, Subpart D)

### Protected Health Information (PHI)

**Definition**: Any information about health status, provision of healthcare, or payment for healthcare that can be linked to a specific individual.

**18 HIPAA Identifiers** (Safe Harbor Method):
1. Names
2. Geographic subdivisions smaller than state (street address, city, county, ZIP code if <20,000 people)
3. Dates (birth, admission, discharge, death) - except year
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers (license plate)
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voice prints)
17. Full-face photographs
18. Any other unique identifying number, characteristic, or code

### De-identification for Sharing Treatment Plans

**Safe Harbor Method**: Remove all 18 identifiers listed above

**Practical De-identification**:
- **Name**: Use "Patient" or de-identified code (e.g., "PT-001")
- **Age**: Use age range (e.g., "60-65 years") instead of exact age
- **Dates**: Use relative timelines (e.g., "3 months ago") or month/year only
- **Location**: State only, remove city, address, specific facility names
- **Identifiers**: Remove MRN, account numbers, SSN
- **Dates of Service**: Refer to "Month/Year" or "recent visit"

**Example**:
- **Before**: "John Smith, DOB 3/15/1965 (58 years old), MRN 123456, address 123 Main St, Anytown, CA 12345, seen 1/15/2025"
- **After**: "Patient, age range 55-60 years, seen Month/Year 2025, California"

### Permitted Uses and Disclosures

**Without Patient Authorization**:
- **Treatment**: Sharing PHI among healthcare providers for patient care
- **Payment**: Disclosing PHI to obtain payment for services
- **Healthcare Operations**: Quality improvement, training, accreditation

**With Patient Authorization**:
- Marketing
- Research (unless IRB waiver granted)
- Sharing with non-covered entities (e.g., patient's employer)
- Psychotherapy notes (special protection)

### Minimum Necessary Standard

Use, disclose, or request only the minimum amount of PHI necessary to accomplish the purpose.

**Exception**: Does NOT apply to treatment - providers may share all relevant information for patient care.

### Patient Rights Under HIPAA

- Right to access own medical records (within 30 days)
- Right to request amendments to records
- Right to accounting of disclosures
- Right to request restrictions on uses/disclosures (provider may deny)
- Right to confidential communications
- Right to be notified of privacy practices (Notice of Privacy Practices)

### Breach Notification

**Breach**: Unauthorized acquisition, access, use, or disclosure of PHI that compromises security or privacy.

**Notification Requirements**:
- **Individual**: Notify affected individuals within 60 days
- **HHS**: If $\geq$500 individuals affected, notify HHS and media
- **Business Associates**: Must notify covered entity of breaches

### HIPAA Violations and Penalties

**Civil Penalties**: $100 to $50,000 per violation (up to $1.5 million per year for identical violations)

**Criminal Penalties**: Up to $250,000 fine and 10 years imprisonment for knowing misuse with intent to sell/transfer PHI

## 42 CFR Part 2 (Substance Use Disorder Records)

### Applicability

**Scope**: Federally assisted substance use disorder (SUD) treatment programs

**More Restrictive than HIPAA**: Provides additional confidentiality protections for SUD treatment records.

### Key Requirements

**Patient Consent Required** for most disclosures (even for treatment, payment, operations - differs from HIPAA).

**Prohibition on Re-disclosure**: Recipients of 42 CFR Part 2-protected information cannot re-disclose without patient consent.

**Documentation**: Patient consent must be written, specific to the information disclosed, and include expiration date.

**Exceptions** (Disclosure without consent allowed):
- Medical emergency
- Court order (not subpoena alone)
- Suspected child abuse/neglect (per state law)
- Crime on premises or against personnel

### Integration with HIPAA

**HIPAA Compliance**: Covered entities must comply with both HIPAA and 42 CFR Part 2 (whichever is more protective applies).

**Note in Treatment Plans**: If patient has SUD and received treatment at 42 CFR Part 2 program, annotate: "Substance use information subject to 42 CFR Part 2 confidentiality protections."

## 21 CFR Part 11 (Electronic Records - FDA)

### Applicability

**Scope**: Clinical trials, research involving FDA-regulated products, drug/device manufacturers.

**Requirements for Electronic Records and Signatures**:
- Validation of systems
- Audit trails (who accessed, when, what changed)
- Electronic signatures equivalent to handwritten
- Controls to prevent unauthorized access

### Treatment Plan Implications

**If part of clinical trial**: Treatment plans must meet 21 CFR Part 11 requirements for electronic documentation.

**Non-Research Clinical Care**: Typically NOT subject to 21 CFR Part 11 (HIPAA Security Rule applies instead).

## Medicare and Medicaid (CMS) Requirements

### Conditions of Participation (CoPs)

**Hospitals, Skilled Nursing Facilities, Home Health Agencies** must meet CoPs to receive Medicare/Medicaid reimbursement.

**Documentation Requirements**:
- Physician orders for treatments
- Comprehensive care plans
- Periodic reassessment and revision
- Interdisciplinary team involvement
- Patient/family involvement

### Meaningful Use / Promoting Interoperability

**EHR Requirements** (for eligible providers to receive incentive payments):
- Use of certified EHR technology
- Electronic prescribing
- Clinical decision support
- Patient portal access to health information
- Care plan documentation with patient goals

### Documentation for Billing

**Medical Necessity**: Documentation must support the medical necessity of services billed.

**Elements to Document**:
- Diagnosis (ICD-10 codes)
- Treatments provided (CPT codes)
- Rationale for treatments
- Patient response to treatment
- Plans for ongoing care

**E/M Coding Support**: Treatment plans support Evaluation and Management (E/M) coding levels:
- Low complexity: Stable chronic conditions, limited treatment options
- Moderate complexity: Multiple conditions, moderate-risk medications/procedures
- High complexity: Severe conditions, high-risk treatments, poor response to therapy

## Quality Measure Reporting

### HEDIS (Healthcare Effectiveness Data and Information Set)

**Used by**: Health plans to measure quality

**Treatment Plan Elements Supporting HEDIS**:

**Diabetes**:
- HbA1c testing (at least annually, quarterly if not controlled)
- Eye exam (annual dilated retinal exam)
- Kidney disease monitoring (urine albumin-to-creatinine ratio annually)
- BP control (<140/90)

**Cardiovascular**:
- Statin therapy for patients with diabetes or ASCVD
- ACE/ARB for patients with diabetes and hypertension
- Beta-blocker for patients with prior MI or HFrEF

**Preventive Care**:
- Flu vaccine annually
- Colorectal cancer screening
- Breast cancer screening
- Cervical cancer screening

### MIPS (Merit-Based Incentive Payment System)

**Eligible Clinicians**: Medicare Part B providers

**Performance Categories**:
1. **Quality**: Reporting on quality measures relevant to specialty
2. **Improvement Activities**: Participation in improvement activities
3. **Promoting Interoperability**: EHR meaningful use
4. **Cost**: Resource use/cost of care

**Treatment Plan Documentation**: Supports quality measure reporting (e.g., diabetes HbA1c control, depression screening and follow-up).

### Accountable Care Organizations (ACOs)

**Quality Measures**: 33+ measures across patient experience, care coordination, preventive health, at-risk populations.

**Treatment Plans**: Facilitate care coordination, chronic disease management to meet ACO quality benchmarks.

## Opioid Prescribing Regulations

### CDC Opioid Prescribing Guidelines (2022)

**Recommendations**:
- Non-opioid therapies preferred for chronic pain
- If opioids used: Lowest effective dose, shortest duration
- Assess risk before starting opioids (ORT, SOAPP)
- Prescribe naloxone for patients at increased overdose risk
- Urine drug testing before and during opioid therapy
- Check PDMP (Prescription Drug Monitoring Program) before prescribing
- Avoid concurrent benzodiazepines and opioids
- Reassess risk/benefit at each increase in dose (especially if approaching $\geq$50 MME/day)

**Treatment Plan Requirements**:
- Document indication for opioid therapy
- Informed consent discussion (risks, benefits, alternatives)
- Treatment agreement/opioid contract
- Plan for monitoring (UDS frequency, PDMP checks)
- Functional goals (not just pain scores)
- Exit strategy/tapering plan

### State Opioid Regulations

**Vary by State**, common elements:
- MME limits (e.g., 90 MME/day max without exemption)
- Prescription limits for acute pain (e.g., 7-day supply)
- Mandatory PDMP checks before prescribing
- Continuing medical education (CME) requirements for prescribers
- Co-prescription of naloxone required in some states

**Prescribers must know state-specific laws**.

### PDMP (Prescription Drug Monitoring Program)

**Purpose**: State databases tracking controlled substance prescriptions to identify doctor shopping, overprescribing.

**Requirements**: Most states require PDMP check before initial opioid prescription and periodically during treatment (e.g., every 3-6 months).

**Documentation**: Note in treatment plan that PDMP was checked and findings (e.g., "PDMP reviewed, no other controlled substances from other prescribers").

## State Medical Board Requirements

### Scope of Practice

**Prescribers**: Must operate within scope of practice defined by state law.
- Physicians (MD/DO): Full prescriptive authority
- Nurse Practitioners (NP): Varies by state (full practice, reduced practice, or restricted practice authority)
- Physician Assistants (PA): Supervision requirements vary

**Controlled Substances**: DEA registration required, state regulations apply.

### Standard of Care

**Definition**: Degree of care and skill ordinarily employed by similar practitioners under similar circumstances.

**Deviations from Standard**: Must be documented with rationale (e.g., patient-specific factors, shared decision-making, evidence supporting alternative approach).

### Informed Consent Documentation

**Required for**: Procedures, surgeries, medications with significant risks, research.

**Elements to Document**:
- Nature of condition and proposed treatment
- Risks and benefits
- Alternatives
- Likely outcome if no treatment
- Patient questions answered
- Patient capacity to consent
- Voluntary consent

**In Treatment Plans**: Note informed consent discussion occurred, especially for high-risk treatments (e.g., opioids, chemotherapy, surgery).

### Documentation Retention

**Medical Records**: State laws vary (typically 7-10 years from last encounter; longer for minors - often until age of majority + statute of limitations).

**Electronic Records**: Same retention requirements as paper.

## Accreditation Standards

### The Joint Commission

**Applicable to**: Hospitals, ambulatory care, behavioral health, long-term care, laboratories.

**Standards Relevant to Treatment Plans**:

**Patient-Centered Care (PC)**:
- Individualized care planning
- Patient and family involvement
- Cultural and language needs addressed
- Patient preferences incorporated

**Care Coordination (CC)**:
- Comprehensive assessment
- Care plan addresses all identified needs
- Interdisciplinary coordination
- Transitions of care managed

**Medication Management (MM)**:
- Medication reconciliation at transitions
- High-risk medication monitoring (anticoagulants, opioids, insulin)
- Patient education on medications

**National Patient Safety Goals (NPSG)**:
- Accurate patient identification
- Effective communication among caregivers
- Safe medication use
- Reduce healthcare-associated infections
- Prevent falls

### CARF (Commission on Accreditation of Rehabilitation Facilities)

**Applicable to**: Rehabilitation, behavioral health, employment services.

**Standards for Treatment Plans**:
- Comprehensive assessment drives plan
- Individualized goals
- Measurable, time-specific objectives
- Regular team review and updates
- Person-centered (patient directs goals)
- Transition and discharge planning
- Outcomes measurement

## Billing and Reimbursement Compliance

### Coding Accuracy

**ICD-10-CM Diagnosis Codes**:
- Code to highest level of specificity
- Code all documented conditions affecting care during encounter
- Primary diagnosis is reason for visit
- Uncertain diagnoses coded as symptoms (outpatient); can code "probable" if inpatient

**CPT Procedure Codes**:
- Specific codes for services provided
- Modifiers when appropriate
- Unbundling prohibited (billing separately for bundled services)

### Documentation Supports Billing

**Medical Necessity**: Treatment must be medically appropriate for diagnosis, meet standard of care, expected to improve condition.

**Treatment Plan Link**: Plan documents rationale for tests, treatments, referrals → supports medical necessity.

**Avoid**:
- Upcoding (billing higher level service than provided)
- Duplicate billing
- Billing for services not rendered

**Anti-Kickback Statute**: Prohibits offering, paying, soliciting, or receiving remuneration for patient referrals for services reimbursed by federal healthcare programs.

**Stark Law**: Prohibits physician self-referral for designated health services (DHS) covered by Medicare/Medicaid.

## Clinical Research and Trials

### Informed Consent (21 CFR Part 50)

**Required Elements**:
- Research procedures described
- Risks and discomforts
- Potential benefits
- Alternative treatments
- Confidentiality protections
- Voluntary participation, can withdraw
- Contact information for questions/problems

**Documentation**: Signed consent form, copy given to participant.

### IRB Review (21 CFR Part 56)

**Institutional Review Board** reviews and approves research involving human subjects.

**Treatment Plans in Research**: If part of clinical trial protocol, must be approved by IRB, follow protocol exactly, documented per 21 CFR Part 11.

### Good Clinical Practice (ICH-GCP)

**International Standard** for ethical and scientific quality in clinical trials.

**Relevant to Treatment Plans**: Detailed protocol adherence, documentation of interventions, adverse event reporting.

## Mental Health Specific Regulations

### Duty to Warn/Protect

**Tarasoff Rule** (varies by state): If patient poses credible threat to identifiable person, provider must:
- Warn intended victim
- Notify police
- Take steps to protect

**Documentation**: Document threat assessment, steps taken to protect.

### Involuntary Commitment

**Criteria** (vary by state): Typically requires patient to be:
- Mentally ill, AND
- Danger to self or others OR gravely disabled

**Due Process**: Emergency hold (24-72 hours), followed by court hearing for longer commitment.

**Documentation**: Clear documentation of dangerousness, efforts at least restrictive intervention.

### Parity Laws

**Mental Health Parity and Addiction Equity Act (MHPAEA)**: Health plans must provide mental health/substance use disorder benefits comparable to medical/surgical benefits.

**Implications**: Cannot limit therapy visits or impose higher copays for mental health vs. medical care.

## Compliance Best Practices

### 1. Know Applicable Regulations
- Federal (HIPAA, 42 CFR Part 2, CDC guidelines, CMS CoPs)
- State (medical practice act, opioid laws, consent requirements)
- Accreditation (Joint Commission, CARF if applicable)

### 2. Document Thoroughly
- Complete all required elements
- Clear rationale for clinical decisions
- Informed consent discussions
- Regulatory compliance (PDMP checks, etc.)

### 3. Privacy Protection
- De-identify before sharing outside treatment team
- Minimum necessary principle
- Secure storage and transmission of records

### 4. Quality Measure Integration
- Include elements that support quality reporting (preventive care, chronic disease metrics)
- Structured data enables measure extraction

### 5. Regular Training
- HIPAA training annually for all staff
- Updates on regulation changes
- Specialty-specific compliance (opioid prescribing, mental health)

### 6. Audit and Monitor
- Internal audits for documentation compliance
- Billing compliance reviews
- Privacy breach monitoring

### 7. Policies and Procedures
- Written policies on treatment planning, consent, privacy
- Regularly reviewed and updated

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: January 2026  
**Note**: Regulations subject to change; verify current requirements.

---

## Reference: Specialty_Specific_Guidelines

# Specialty-Specific Treatment Plan Guidelines

## Overview

This reference provides detailed guidelines for developing treatment plans specific to each of the six template types: general medical, rehabilitation, mental health, chronic disease management, perioperative, and pain management. Each section includes specialty-specific considerations, clinical pearls, and best practices.

## Concise Documentation Examples by Specialty

### Foundation Medicine Model: Concise vs. Verbose

**PRINCIPLE**: Focus on actionable information; eliminate redundancy; use bullet points and short paragraphs.

### General Medical - Diabetes Example

**VERBOSE (Avoid)**:
> "Patient education was provided on the pathophysiology of Type 2 Diabetes Mellitus, including detailed explanation of insulin resistance, pancreatic beta-cell dysfunction, and the progressive nature of the disease. The patient was educated about the various potential complications of diabetes including microvascular complications such as diabetic retinopathy which can lead to blindness, diabetic nephropathy which can progress to end-stage renal disease requiring dialysis, and diabetic neuropathy which can cause pain and sensory loss. Additionally, macrovascular complications were discussed including increased risk of myocardial infarction, stroke, and peripheral arterial disease."

**CONCISE (Preferred - 75% shorter)**:
> "Key Education: Disease understanding, micro/macrovascular complication risks, self-monitoring techniques (glucose, BP), medication timing, diet basics, exercise safety, sick day management. Critical warnings: Hypoglycemia (shakiness, confusion - treat with 15g carbs), severe hyperglycemia >300 (call office), chest pain/stroke symptoms (911)."

### Mental Health - Depression Example

**VERBOSE (Avoid)**:
> "The patient will participate in individual psychotherapy sessions utilizing Cognitive Behavioral Therapy techniques. Sessions will be scheduled on a weekly basis for a duration of 50 minutes each. The therapist will work with the patient to identify negative thought patterns, challenge cognitive distortions, develop behavioral activation strategies, and build coping skills for managing depressive symptoms."

**CONCISE (Preferred - 60% shorter)**:
> "CBT weekly × 16 sessions (50 min) focusing on: identifying/challenging negative thoughts, behavioral activation, coping skills development. Goals: PHQ-9 <10, return to work, 3 effective stress management strategies."

### Rehabilitation - Post-Stroke Example

**VERBOSE (Avoid)**:
> "Expected outcomes include improvement in upper extremity function with anticipated achievement of the ability to perform self-care activities including bathing, dressing, and grooming with minimal assistance or independently. The patient is expected to demonstrate improved ambulation capabilities with progression from wheelchair mobility to ambulation with a rolling walker under supervision, with eventual goal of independent ambulation with a straight cane for distances up to 300 feet."

**CONCISE (Preferred - 70% shorter)**:
> "Expected outcomes (8 weeks): Independent ADLs with adaptive equipment, ambulation 300+ feet with walker/supervision, stair negotiation with handrail, safe home discharge. Timeline: Week 2 - transfers with supervision; Week 4 - ambulate 150 feet; Week 8 - community ambulation, discharge ready."

### Perioperative - Laparoscopic Surgery Example

**VERBOSE (Avoid)**:
> "Postoperative pain management will utilize a multimodal approach to analgesia in order to minimize opioid consumption and reduce the risk of opioid-related adverse effects including nausea, vomiting, constipation, and respiratory depression. The multimodal regimen will include scheduled acetaminophen administered at a dose of 1000 milligrams every 6 hours, ibuprofen 600 milligrams every 6 hours as needed, and opioid analgesics reserved for breakthrough pain only."

**CONCISE (Preferred - 65% shorter)**:
> "Multimodal analgesia: Acetaminophen 1000mg Q6H scheduled, ibuprofen 600mg Q6H PRN, opioids for breakthrough only. Goal: Pain <4/10, minimize opioid use, early mobilization."

### Key Principles for Concise Documentation

1. **Use abbreviations appropriately**: Q6H, PRN, ADLs, BP (define on first use if uncommon)
2. **Bullet points over paragraphs**: Easier to scan, more actionable
3. **Combine related information**: Group similar items together
4. **Eliminate filler words**: "The patient will...", "It is anticipated that..."
5. **Focus on "what, when, why"**: Action, timing, rationale in minimal words
6. **Use tables for complex data**: Medication lists, monitoring schedules
7. **Prioritize critical information**: Safety warnings, emergency actions

## 1. General Medical Treatment Plans

### Applicable Conditions
- Chronic diseases: Diabetes, hypertension, heart failure, COPD, asthma
- Common acute conditions requiring structured follow-up
- Primary care management of stable chronic conditions

### Key Assessment Components

**Baseline Status**:
- Vital signs, BMI, functional status
- Disease-specific metrics (HbA1c, BP, lipids, PFTs)
- Comorbidity assessment
- Medication reconciliation
- Social determinants of health screening

**Disease Severity Staging**:
- Use validated staging systems when available
- Examples: CKD stages 1-5, GOLD COPD stages I-IV, NYHA heart failure classes I-IV, ADA diabetes complications
- Document severity to guide treatment intensity

### Treatment Goal Specifics

**Guideline-Based Targets**:
- HbA1c <7% for most diabetics (<8% if elderly, limited life expectancy)
- BP <130/80 for most; <140/90 if elderly or low cardiovascular risk
- LDL <70 mg/dL if ASCVD, <100 mg/dL moderate risk
- Use individualized targets based on patient factors

**Functional Goals**:
- Maintain independence in ADLs
- Return to work if applicable
- Engage in valued activities
- Quality of life improvement

### Pharmacotherapy Considerations

**Polypharmacy Management**:
- Consider deprescribing when possible (Beers Criteria for elderly)
- Medication reconciliation at each visit
- Simplify regimens (once-daily dosing, combination pills)
- Address adherence barriers (cost, side effects, complexity)

**Drug-Disease Interactions**:
- Avoid NSAIDs if CKD, heart failure
- Caution with metformin if eGFR <30
- Beta-blockers contraindicated in severe COPD/asthma (use cardioselective if needed)

### Monitoring Schedules by Condition

**Diabetes**:
- HbA1c every 3 months if not at goal, every 6 months if stable
- Annual: dilated eye exam, foot exam, urine ACR, lipids
- Each visit: BP, weight, medication adherence

**Hypertension**:
- Home BP monitoring (HBPM) - most accurate, average of multiple readings
- Office BP at each visit
- Labs (BMP for K+, creatinine) 1-2 weeks after ACE/ARB initiation, then annually

**Heart Failure**:
- Daily weights (report gain >2-3 lbs in 2 days)
- BNP/NT-proBNP when clinically changing
- Echo annually or if EF change suspected
- Medication titration every 2 weeks during optimization phase

### Primary Care Integration

**Preventive Care**:
- Include age-appropriate cancer screenings
- Vaccination schedule (flu, pneumococcal, zoster, COVID)
- Lifestyle counseling (tobacco, alcohol, diet, exercise)

**Chronic Disease Management Models**:
- Chronic Care Model components: Self-management support, delivery system redesign, clinical information systems, decision support
- Team-based care: Involvement of nurses, pharmacists, dietitians, care coordinators

---

## 2. Rehabilitation Treatment Plans

### Applicable Settings
- Post-acute inpatient rehabilitation
- Outpatient PT/OT/SLP
- Home health therapy
- Skilled nursing facility rehabilitation

### Key Assessment Components

**Functional Assessments (use validated tools)**:
- **FIM** (Functional Independence Measure): 18 items, 7-point scale, 126 total - most widely used
- **Barthel Index**: 10 ADLs, 100-point scale - simpler than FIM
- **Berg Balance Scale**: 14 tasks, 56 points - fall risk (score <45 = high risk)
- **6-Minute Walk Test**: Distance walked in 6 minutes - cardiopulmonary endurance
- **Timed Up and Go (TUG)**: Time to stand, walk 3 meters, turn, return, sit - fall risk (>12 sec = high risk)
- **9-Hole Peg Test**: Upper extremity fine motor speed
- **ROM**: Goniometric measurement for each joint
- **Manual Muscle Testing**: 0-5 scale (0=no contraction, 5=normal strength)

**ICF Framework Goals**:
- **Body Functions/Structures**: Impairments (ROM, strength, balance)
- **Activity**: Task performance (walk 150 feet, dress independently)
- **Participation**: Life roles (return to work, community engagement)

### Rehabilitation Goals Specifics

**Goal Levels**:
1. **Impairment Goals**: Increase knee ROM 90→110°, improve MMT 3/5→4/5
2. **Activity Goals**: Ambulate 300 feet with walker, transfer bed-chair independently
3. **Participation Goals**: Return to work, resume hobbies, live independently

**Assistance Levels** (document current and goal):
- I = Independent
- SV = Supervision (cues, no physical assist)
- CG = Contact Guard (hands close, no assist)
- Min A = Minimal Assist (patient does 75%+)
- Mod A = Moderate Assist (patient does 50-74%)
- Max A = Maximal Assist (patient does 25-49%)
- Total A = Total Assist (patient does <25%)

### Therapy Interventions

**Physical Therapy**:
- Therapeutic exercise dose: Specify sets, reps, resistance, frequency
- Gait training: Distance, assistive device, supervision level
- Balance training: Static, dynamic, perturbation-based
- Modalities: Heat, ice, TENS, E-stim - adjuncts only, not primary intervention

**Occupational Therapy**:
- ADL training: Use of adaptive equipment (reacher, sock aid, built-up utensils)
- Upper extremity strengthening: Functional tasks, fine motor activities
- Cognitive retraining: Memory strategies, attention training, executive function

**Speech-Language Pathology**:
- Dysphagia: Diet texture modifications (IDDSI levels), swallow strategies (chin tuck, multiple swallows)
- Aphasia therapy: Constraint-induced language therapy, semantic feature analysis
- Dysarthria: Articulation drills, rate control, augmentative communication

### Home Exercise Program (HEP)

**Essentials**:
- Illustrated handout with pictures/descriptions
- Specific dosage (e.g., "2 sets x 10 reps, daily")
- Progression criteria
- Safety precautions
- Patient/caregiver demonstrates understanding

### DME and Environmental Modifications

**Common DME**:
- Ambulation: Walker, cane, crutches (specify type, e.g., front-wheeled walker)
- Bathroom: Raised toilet seat, shower chair, grab bars
- Dressing: Reacher, sock aid, long shoe horn, button hook, elastic laces
- Mobility: Hospital bed, wheelchair (if needed)

**Home Modifications**:
- Ramp for stairs
- Stair lift if multiple levels
- Remove scatter rugs (fall hazard)
- Improve lighting
- Rearrange for accessibility

### Discharge Planning

**Discharge Criteria**:
- Functional plateau reached or goals met
- Safe for discharge setting
- Patient/caregiver educated
- DME obtained and home modifications complete
- Follow-up arranged

**Discharge Destination**:
- Home with outpatient therapy
- Home with home health
- Skilled nursing facility
- Long-term acute care hospital (if medically complex)

---

## 3. Mental Health Treatment Plans

### Applicable Conditions
- Major depressive disorder, dysthymia
- Anxiety disorders (GAD, panic, social anxiety, specific phobias)
- Bipolar disorder
- Schizophrenia and psychotic disorders
- PTSD and trauma-related disorders
- Eating disorders
- Substance use disorders
- Personality disorders

### Key Assessment Components

**Diagnostic Assessment**:
- Meet DSM-5 criteria for diagnosis
- Symptom severity assessment (use validated scales)
- Functional impairment (work, relationships, self-care)
- Psychiatric history (prior episodes, treatments, hospitalizations)
- Substance use assessment (AUDIT, DAST)
- Trauma history
- Family psychiatric history

**Validated Assessment Tools**:
- **PHQ-9**: Depression severity (0-27, scores ≥10 indicate moderate-severe depression)
- **GAD-7**: Anxiety severity (0-21, scores ≥10 indicate moderate-severe anxiety)
- **MDQ** (Mood Disorder Questionnaire): Bipolar screening
- **PC-PTSD-5**: PTSD screening, then full PCL-5 if positive
- **AUDIT**: Alcohol use (0-40, ≥8 indicates hazardous drinking)
- **PHQ-15**: Somatic symptoms
- **WHODAS 2.0**: Functional disability

**Risk Assessment**:
- **Suicide Risk**: Use Columbia Suicide Severity Rating Scale (C-SSRS)
  - Ideation (passive, active, plan, intent)
  - Protective factors (reasons for living, social support)
  - Risk factors (prior attempts, impulsivity, access to means)
- **Violence/Homicide Risk**: History of violence, current ideation, access to weapons

### Treatment Goals Specifics

**Symptom Goals**:
- Reduction in standardized scale scores (e.g., PHQ-9 from 18→<10→<5 for remission)
- Specific symptom targets (sleep 7 hours, reduce panic attacks from 3/week→0)

**Functional Goals**:
- Return to work/school
- Resume social activities
- Improve relationships
- Self-care independence

**Recovery-Oriented Goals**:
- Personal meaning and purpose
- Hope and empowerment
- Social connections and community integration
- Independent living

### Evidence-Based Psychotherapies

**Depression**:
- **CBT**: 12-16 sessions, homework between sessions
- **Behavioral Activation**: Focus on increasing rewarding activities
- **Interpersonal Therapy (IPT)**: 12-16 sessions, focus on relationships
- **Problem-Solving Therapy**: Brief (6-8 sessions), structured approach

**Anxiety**:
- **CBT with exposure**: Gold standard for anxiety disorders
- **Panic Control Therapy**: Interoceptive exposure, cognitive restructuring
- **Social skills training**: For social anxiety

**PTSD**:
- **Prolonged Exposure (PE)**: 8-15 sessions, imaginal and in vivo exposure
- **Cognitive Processing Therapy (CPT)**: 12 sessions, challenge trauma-related cognitions
- **EMDR** (Eye Movement Desensitization and Reprocessing): Alternative, less evidence than PE/CPT

**Bipolar**:
- **Family-Focused Therapy**: Psychoeducation, communication, problem-solving
- **Interpersonal and Social Rhythm Therapy**: Stabilize daily routines, sleep

**Borderline Personality Disorder**:
- **DBT** (Dialectical Behavior Therapy): 1 year program, individual + group + phone coaching
- Skills: Mindfulness, distress tolerance, emotion regulation, interpersonal effectiveness

### Psychopharmacology Specifics

**Antidepressants**:
- First-line: SSRIs (sertraline, escitalopram, fluoxetine)
- 2-4 weeks for initial response, 6-8 weeks for full effect
- Titrate after 2-4 weeks if partial response
- Switch if no response after full trial
- Augmentation strategies if partial response (second antidepressant, atypical antipsychotic, lithium)
- Continue 6-12 months after remission (longer if recurrent)

**Antipsychotics**:
- First-generation (typical): Haloperidol - high EPS risk, use second-generation preferred
- Second-generation (atypical): Risperidone, olanzapine, quetiapine, aripiprazole, lurasidone
- Monitoring: Metabolic syndrome (weight, glucose, lipids), EPS, prolactin, QTc

**Mood Stabilizers**:
- Lithium: Narrow therapeutic window, monitor levels (0.6-1.2 mEq/L), TSH, renal function
- Valproic acid: Monitor levels, LFTs, CBC (thrombocytopenia)
- Lamotrigine: Titrate slowly (risk of Stevens-Johnson syndrome if too fast)

### Safety Planning

**Essential for All Mental Health Plans**:
- Warning signs (thoughts, feelings, behaviors)
- Internal coping strategies
- Social support contacts
- Professional contacts (therapist, psychiatrist, crisis line)
- Means restriction (firearms removed, medications limited)
- Reason for living

**Crisis Resources**:
- 988 Suicide & Crisis Lifeline
- Crisis Text Line (text HOME to 741741)
- Local mobile crisis team
- Emergency department

---

## 4. Chronic Disease Management Plans

### Multiple Comorbidities Management

**Common Clusters**:
- Cardiometabolic: Diabetes + hypertension + hyperlipidemia + obesity
- Cardiopulmonary: Heart failure + COPD
- Renal-cardiovascular: CKD + hypertension + diabetes
- Mental-physical: Depression + chronic pain + chronic disease

### Prioritization Strategies

**When Multiple Goals Compete**:
1. **Life-threatening issues first**: Unstable angina, uncontrolled heart failure
2. **High-impact, modifiable conditions**: Diabetes with HbA1c 10% (significant reduction possible)
3. **Synergistic treatments**: Medications that help multiple conditions (SGLT2i for diabetes + heart failure + CKD)
4. **Patient priorities**: What matters most to patient

### Medication Optimization for Multimorbidity

**Synergistic Medications** (dual/triple benefit):
- **SGLT2 inhibitors**: Diabetes + heart failure + CKD
- **ACE inhibitors/ARBs**: Hypertension + diabetes (renal protection) + heart failure
- **Beta-blockers**: Hypertension + heart failure + CAD
- **Statins**: Hyperlipidemia + ASCVD prevention + diabetes
- **GLP-1 agonists**: Diabetes + weight loss + cardiovascular benefit

**Deprescribing**:
- Identify medications with limited benefit (e.g., strict glycemic control in limited life expectancy)
- Discontinue medications with more harm than benefit
- Simplify regimens (reduce pill burden)

### Care Coordination

**Team-Based Care**:
- Primary care coordinates
- Specialists co-manage (cardiologist for HF, endocrinologist for diabetes)
- Care coordinator facilitates (schedules, education, barrier identification)
- Pharmacist reviews medications, optimizes therapy
- Dietitian provides medical nutrition therapy
- Social worker addresses social needs

**Communication**:
- Shared EHR when possible
- Care plan accessible to all team members
- Medication reconciliation after specialist visits
- Regular team meetings or e-consultations

### Population Health Integration

**Registry Management**:
- Identify patients due for care (HbA1c testing, diabetic eye exam)
- Outreach for overdue preventive care
- Risk stratification (high-utilizers, complex patients)

**Transition Management**:
- Hospital discharge follow-up within 7 days
- Medication reconciliation post-discharge
- Red flags review
- Escalation plan if decompensating

---

## 5. Perioperative Care Plans

### Preoperative Risk Assessment

**Cardiac Risk** (Revised Cardiac Risk Index - RCRI):
- High-risk surgery, ischemic heart disease, heart failure, CVD, diabetes on insulin, creatinine >2
- 0 points = <1% risk, 1 point = 1%, 2 points = 2.4%, ≥3 points = 5.4% risk of cardiac event

**If High Risk**: Consider further testing (stress test, echo), cardiology consultation, perioperative beta-blockade.

**Pulmonary Risk** (ARISCAT score):
- Age, SpO2, respiratory infection recent, preop anemia, surgical incision, duration, emergency
- Higher risk: Smoking cessation, incentive spirometry, early mobilization

**VTE Risk** (Caprini Score):
- Age, surgery type, mobility, prior VTE, obesity, cancer
- Stratify to guide prophylaxis (none, mechanical, pharmacologic, or both)

### Preoperative Optimization

**Diabetes**:
- Target HbA1c <8% for elective surgery (delay if >9%)
- Hold metformin 24-48 hours before (risk of lactic acidosis)
- Hold SGLT2i 3-4 days before (DKA risk)
- Insulin: Reduce long-acting by 20-25% day of surgery, hold short-acting

**Hypertension**:
- Continue most medications through surgery
- Hold ACE/ARB morning of surgery (avoid intraop hypotension)
- Continue beta-blocker (avoid withdrawal)

**Anticoagulation**:
- Warfarin: Hold 5 days before, bridge with LMWH if high VTE risk
- DOACs: Hold 24-48 hours (based on renal function and bleeding risk)
- Antiplatelet: Continue aspirin for most surgeries, hold P2Y12 inhibitors (clopidogrel) 5-7 days if high bleeding risk

**Anemia**:
- Optimize iron stores preop (IV iron if time limited)
- Avoid transfusion triggers if possible (restrictive strategy)

### Enhanced Recovery After Surgery (ERAS)

**Preoperative**:
- Patient education, expectation setting
- No prolonged fasting (clear liquids 2 hours before)
- Carbohydrate loading (reduces insulin resistance)
- No routine premedication

**Intraoperative**:
- Multimodal analgesia (minimize opioids)
- Goal-directed fluid therapy (avoid overhydration)
- Normothermia (prevent hypothermia)
- Antiemetic prophylaxis

**Postoperative**:
- Early mobilization (out of bed day of surgery)
- Early oral nutrition (resume diet POD 0-1)
- Multimodal analgesia (acetaminophen, NSAIDs, regional blocks)
- Remove tubes/drains early (Foley, NG tube, surgical drains)
- DVT prophylaxis

### Postoperative Milestones

**Day of Surgery (POD 0)**:
- Out of bed to chair 4-6 hours post-op
- Sips of clear liquids if appropriate
- Pain controlled on multimodal regimen

**POD 1**:
- Ambulate in hallway
- Regular diet
- Foley catheter removed
- Transition to oral pain medications

**POD 2-3** (typical discharge for many surgeries):
- Ambulate 150+ feet
- Adequate oral intake
- Pain controlled on oral meds
- No complications requiring hospitalization

### Discharge Readiness

**Criteria**:
- Adequate pain control on oral medications
- Tolerating regular diet
- Mobile (ambulate, transfers)
- Voiding spontaneously
- Stable vital signs
- No active complications
- Safe discharge plan (home support, DME arranged)

---

## 6. Pain Management Plans

### Pain Assessment

**Comprehensive Pain Evaluation**:
- Location, radiation
- Quality (sharp, dull, burning, aching, shooting)
- Intensity (0-10 NRS)
- Temporal pattern (constant, intermittent, episodic)
- Aggravating/alleviating factors
- Functional impact (Brief Pain Inventory - BPI interference items)
- Prior treatments and responses

**Pain Classification**:
- **Nociceptive**: Somatic (MSK) or visceral (organ)
- **Neuropathic**: Nerve injury/dysfunction (burning, shooting, electric, numbness/tingling)
- **Nociplastic**: Central sensitization, fibromyalgia
- **Mixed**: Combination

### Multimodal Analgesia Principles

**Goal**: Additive/synergistic pain relief from multiple mechanisms, opioid-sparing.

**Components**:
1. Non-opioid analgesics (acetaminophen, NSAIDs)
2. Adjuvant analgesics (gabapentinoids, SNRIs, TCAs for neuropathic)
3. Topical agents (lidocaine patches, diclofenac gel, capsaicin)
4. Interventional procedures (injections, nerve blocks, RFA, SCS)
5. Physical therapies (PT, exercise, TENS)
6. Psychological therapies (CBT-CP, mindfulness, biofeedback)
7. Complementary therapies (acupuncture, massage, yoga)
8. Opioids (if other modalities insufficient) - lowest dose, reassess frequently

### Neuropathic Pain Specific Treatments

**First-Line**:
- Gabapentin 300mg titrate to 1800-3600mg/day divided TID
- Pregabalin 75mg BID titrate to 150-300mg BID
- Duloxetine 60mg daily (also for fibromyalgia, chronic MSK pain)
- TCAs (amitriptyline, nortriptyline) 10-75mg QHS - second-line due to side effects

**Topical**:
- Lidocaine patches 5% (localized neuropathic pain)
- Capsaicin 8% patch (high-concentration, applied by provider)

**Refractory**:
- Tramadol (dual mechanism - opioid + SNRI)
- Opioids (if severe and function-limiting despite above)

### Opioid Prescribing (CDC Guidelines)

**Before Initiating**:
- Non-opioid multimodal therapies tried and inadequate
- Functional goals established (not just pain scores)
- Risks vs. benefits discussed and documented
- Opioid risk assessment (ORT, SOAPP)
- Informed consent discussion
- Treatment agreement signed
- PDMP checked
- Baseline UDS

**During Opioid Therapy**:
- Start low dose (<50 MME/day), short-acting
- Reassess frequently (every 1-3 months)
- Functional improvement expected (not just pain scores)
- UDS every 3-6 months (check for adherence and illicit substances)
- PDMP check each prescription or at least every 3 months
- Naloxone co-prescribed
- Avoid concurrent benzodiazepines
- If dose approaching 50 MME, reassess; avoid >90 MME if possible

**Tapering**:
- If not meeting functional goals
- Serious adverse effects
- Aberrant behaviors
- Patient request
- Slow taper: 10-25% dose reduction per week to month (faster if safety concern)

### Interventional Pain Procedures

**Indications and Evidence**:
- **Epidural Steroid Injection**: Radicular pain from disc herniation/stenosis - short-term benefit
- **Facet Joint Injections**: Diagnostic (if >50% relief, proceed to RFA)
- **Radiofrequency Ablation**: 6-12 months relief for facet-mediated pain
- **Spinal Cord Stimulation**: Refractory neuropathic pain (FBSS, CRPS) - 50-60% success
- **Intrathecal Pump**: Severe refractory pain, cancer pain - delivers medication to CSF

**Documentation for Procedures**:
- Indication, prior conservative treatments tried
- Expected benefit and duration
- Risks discussed
- Number of injections/procedures allowed per year

### Functional Goals Emphasis

**Shift from Pain Scores to Function**:
- "Reduce pain to 3/10" is less meaningful than "Walk 1 mile, return to work, play with grandchildren"
- BPI interference scores track functional impact
- SMART functional goals (see Goal Setting reference)

### Psychological Integration

**CBT for Chronic Pain (CBT-CP)**:
- Pain education and reconceptualization (pain ≠ harm)
- Cognitive restructuring (challenge catastrophizing, all-or-nothing thinking)
- Activity pacing and graded exposure (increase activity without flares)
- Relaxation techniques
- Acceptance and mindfulness

**Essential for Chronic Pain**: Psychological factors (depression, anxiety, catastrophizing) perpetuate pain; must be addressed.

---

## Cross-Cutting Considerations for All Treatment Plans

### Cultural Competence
- Ask about cultural health beliefs, practices
- Use interpreter services when language barriers exist
- Respect religious/spiritual practices in treatment
- Adapt interventions to cultural context when possible

### Health Literacy
- Assess understanding (teach-back method)
- Use plain language, avoid jargon
- Visual aids, written materials at 5th-6th grade reading level
- Confirm patient can execute plan (demonstrate inhaler use, insulin injection, etc.)

### Social Determinants of Health (SDOH)
- Screen for food insecurity, housing instability, transportation barriers
- Connect to community resources (SNAP, Medicaid, patient assistance programs)
- Address barriers in treatment plan (e.g., medication cost → generic alternatives, patient assistance)

### Advance Care Planning
- Appropriate for serious illness, elderly, declining function
- Goals of care discussion
- Healthcare proxy designation
- Advance directive completion
- Preferences for resuscitation, intubation, dialysis, etc.

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: January 2026

---

## Reference: Treatment_Plan_Standards

% Treatment Plan Standards and Best Practices
% Professional guidelines for treatment plan documentation
% Last updated: 2025

# Treatment Plan Standards

## Overview

Treatment plans are comprehensive documents that outline systematic approaches to addressing patient health conditions through evidence-based interventions, measurable goals, and structured follow-up. This reference provides professional standards, documentation requirements, and legal considerations for creating high-quality treatment plans across all medical specialties.

## Core Documentation Standards

### 1. Executive Summary Best Practices (Foundation Medicine Model)

**CRITICAL: All treatment plans MUST include a prominent "Treatment Plan Highlights" summary box on the first page.**

Following the Foundation Medicine model for genomic profiling reports, treatment plans should begin with a concise, bulletin-style summary that provides immediate access to key actionable information:

**Components of Treatment Plan Highlights Box:**
- **Key Diagnosis**: Primary condition with ICD-10 code, severity/stage (1 line)
- **Primary Treatment Goals**: 2-3 SMART goals in bullet format
- **Main Interventions**: 2-3 key interventions (pharmacological, non-pharmacological, monitoring)
- **Timeline Overview**: Brief treatment duration/phases (1 line)

**Format Requirements:**
- Use colored box (tcolorbox in LaTeX) to make it visually prominent
- Place immediately after title, before Patient Information section
- Summary must fit on first page with patient demographics
- Use concise, actionable language
- Focus on what clinicians need to know immediately

**Optimal Document Length:**
- **Preferred**: 1 page for most treatment plans (quick-reference format)
- **Standard**: 3-4 pages for moderate complexity cases
- **Extended**: 5-6 pages maximum for highly complex cases only
- Prioritize brevity, clarity, and actionability over comprehensive detail
- Think "clinical decision support card" not "comprehensive textbook"

**Design Philosophy:**
The highlights box enables efficient clinical decision-making by providing critical information upfront, following evidence-based practices from precision medicine reporting. This approach improves care coordination, reduces time to treatment initiation, and ensures key information is never overlooked.

### 2. Essential Components

All treatment plans must include:

#### Patient Information (De-identified for Sharing)
- Unique patient identifier (not name or MRN)
- Age range (not exact birth date)
- Relevant demographics
- Date of plan creation
- Provider name and credentials
- HIPAA compliance statement

#### Diagnosis and Assessment
- Primary diagnosis with ICD-10 code
- Secondary diagnoses and comorbidities
- Severity classification or staging
- Functional assessment and baseline status
- Risk stratification
- Prognostic considerations

#### Treatment Goals (SMART Format)
- **Specific**: Clearly defined outcomes
- **Measurable**: Quantifiable metrics or observable criteria
- **Achievable**: Realistic given patient circumstances
- **Relevant**: Aligned with patient values and priorities
- **Time-bound**: Defined timeframe for achievement

Short-term goals (weeks to 3 months) and long-term goals (3-12+ months) should be distinguished.

#### Interventions
- **Pharmacological**: Specific medications, doses, frequencies, rationales
- **Non-pharmacological**: Lifestyle modifications, behavioral interventions, education
- **Procedural**: Planned procedures, specialist referrals, diagnostic testing

#### Timeline and Schedule
- Treatment phases with durations
- Appointment frequency
- Milestone assessments
- Expected treatment duration

#### Monitoring Parameters
- Clinical outcomes to track
- Assessment tools and scales
- Monitoring frequency
- Intervention thresholds

#### Expected Outcomes
- Primary outcome measures
- Success criteria
- Timeline for improvement
- Criteria for treatment modification

#### Follow-up Plan
- Scheduled appointments
- Communication protocols
- Emergency procedures
- Transition planning

#### Patient Education
- Condition understanding
- Self-management skills
- Warning signs
- Resources and support

#### Risk Mitigation
- Potential adverse effects
- Safety monitoring
- Emergency action plans
- Complication prevention

### 2. Professional Documentation Standards

#### Clarity and Precision
- Use professional medical terminology appropriately
- Define abbreviations on first use
- Avoid ambiguous language
- Specific rather than vague descriptions

**Good Example**: "Reduce HbA1c from 8.5% to <7% within 3 months"  
**Poor Example**: "Improve diabetes control"

#### Completeness
- Address all relevant aspects of condition
- Include rationale for treatment choices
- Document shared decision-making
- Address patient preferences and concerns

#### Accuracy
- Factually correct information
- Current evidence-based recommendations
- Appropriate dosing and frequencies
- Correct ICD-10 and CPT codes

#### Timeliness
- Plans created at diagnosis or treatment initiation
- Updated after significant clinical changes
- Regular scheduled updates (quarterly to annually)
- Dated and signed promptly

#### Legibility and Organization
- Professional formatting
- Logical flow and structure
- Consistent use of headings and sections
- Easy to locate key information

### 3. Legal and Regulatory Requirements

#### Medical Necessity Documentation
Treatment plans must demonstrate:
- Appropriateness of interventions for diagnosis
- Evidence supporting treatment choices
- Expected outcomes justify costs and risks
- Frequency and duration are reasonable
- Less invasive options considered

#### Informed Consent Documentation
Record that patient:
- Understands diagnosis and prognosis
- Aware of treatment options, risks, and benefits
- Knows alternatives to proposed treatment
- Had opportunity to ask questions
- Voluntarily agrees to treatment plan

#### Privacy and Confidentiality (HIPAA)
- Protected Health Information (PHI) safeguarded
- De-identification for sharing:
  - Remove 18 HIPAA identifiers per Safe Harbor method
  - Names, dates (except year), geographic subdivisions smaller than state
  - Contact information (phone, fax, email, addresses)
  - Social Security numbers, medical record numbers, account numbers
  - Biometric identifiers, photos, other unique identifiers
- Access limited to those with treatment, payment, or operations need
- Patient authorization for non-routine disclosures

#### Billing and Reimbursement Support
- ICD-10 diagnosis codes for all conditions
- CPT codes for procedures
- Documentation of medical necessity
- Justification for level of service
- Compliance with payer-specific requirements

#### Quality Measure Reporting
Enable extraction of quality metrics:
- HEDIS measures (diabetes HbA1c testing, BP control, etc.)
- CMS quality reporting (MIPS, ACO measures)
- Disease-specific quality indicators
- Patient safety indicators

#### Liability Protection
Defensible documentation includes:
- Rationale for clinical decisions
- Consideration of differential diagnosis
- Risk-benefit analysis
- Patient education and warnings
- Follow-up plan for abnormal findings
- Addressing non-adherence or patient refusal

## Professional Practice Standards

### Joint Commission Standards

#### Patient-Centered Care
- Treatment plans developed with patient participation
- Goals reflect patient values and preferences
- Cultural and linguistic needs addressed
- Health literacy appropriate communication

#### Multidisciplinary Coordination
- Input from relevant disciplines
- Clear role delineation
- Communication among team members
- Coordinated interventions

#### Evidence-Based Practice
- Interventions based on current evidence
- Clinical practice guidelines followed
- Variation from guidelines documented and justified
- Literature supports treatment choices

### Commission on Accreditation of Rehabilitation Facilities (CARF)

For rehabilitation treatment plans:
- Individualized based on comprehensive assessment
- Measurable, achievable, time-specific goals
- Regular team review and modification
- Patient and family involvement
- Transition and discharge planning

### Centers for Medicare & Medicaid Services (CMS)

#### Conditions of Participation
- Physician orders for treatment
- Periodic review and revision
- Progress toward goals documented
- Care plan accessible to all team members

#### Documentation Requirements
- Legible (typed or clear handwriting)
- Dated and authenticated (signed)
- Amendments/corrections properly marked
- Retention per state law (typically 7-10 years, longer for minors)

## Medical Specialty Standards

### Primary Care
- Annual comprehensive assessment and plan update
- Chronic disease management protocols
- Preventive care integration
- Medication reconciliation
- Care coordination with specialists

### Behavioral Health
- Mental status examination
- Psychiatric diagnoses per DSM-5 criteria
- Suicide/homicide risk assessment and safety planning
- Measurable behavioral outcomes
- Crisis intervention plan
- Substance use assessment
- 42 CFR Part 2 compliance for substance use treatment

### Rehabilitation
- Functional assessments (FIM, Barthel Index, etc.)
- Activity limitations and participation restrictions
- Short-term and long-term functional goals
- Therapy frequency, intensity, duration
- Home exercise program
- Assistive devices and DME
- Discharge criteria

### Surgical/Perioperative
- Indication for surgery documented
- Preoperative risk assessment (ASA, RCRI)
- Medical optimization plan
- Enhanced Recovery After Surgery (ERAS) protocols when applicable
- Postoperative milestones
- Discharge criteria and planning

### Pain Management
- Comprehensive pain assessment (location, intensity, quality, temporal pattern, impact)
- Pain type (nociceptive, neuropathic, mixed)
- Multimodal analgesia approach
- Opioid risk assessment (ORT, SOAPP)
- If opioids: CDC guidelines compliance, treatment agreement, UDS, PDMP
- Functional goals (not just pain scores)
- Psychological screening and intervention

## Quality Indicators for Treatment Plans

### Completeness Metrics
- All required sections present (100%)
- Goals meet SMART criteria ($\geq$90%)
- Interventions have clear rationales ($\geq$95%)
- Monitoring plan includes frequency ($\geq$95%)
- Patient education documented (100%)

### Clinical Quality Metrics
- Evidence-based interventions ($\geq$90%)
- Guideline-concordant care ($\geq$85%)
- Avoidance of low-value care (100%)
- Appropriate preventive care included ($\geq$95%)

### Patient-Centered Metrics
- Patient preferences documented ($\geq$90%)
- Shared decision-making noted ($\geq$85%)
- Culturally appropriate care (100%)
- Health literacy addressed ($\geq$90%)

### Safety Metrics
- Risk mitigation strategies present (100%)
- Medication safety addressed (100%)
- Emergency procedures documented (100%)
- Red flags/warning signs communicated (100%)

## Common Documentation Deficiencies and Solutions

### Problem: Vague Goals
**Deficiency**: "Improve diabetes"  
**Solution**: "Reduce HbA1c from 8.5% to <7% within 3 months through medication intensification and lifestyle modification"

### Problem: Missing Rationales
**Deficiency**: Lists medications without explanation  
**Solution**: "Metformin 1000mg BID - first-line therapy for T2DM, reduces hepatic glucose production, target dose for HbA1c reduction"

### Problem: No Timeline
**Deficiency**: Goals without timeframes  
**Solution**: "Short-term (3 months): HbA1c <7.5%; Long-term (6 months): HbA1c <7%"

### Problem: Incomplete Monitoring
**Deficiency**: "Monitor labs"  
**Solution**: "HbA1c every 3 months until at goal, then every 6 months; CMP every 6 months to monitor renal function on metformin and ACE inhibitor"

### Problem: Absent Patient Education
**Deficiency**: No documentation of education provided  
**Solution**: Dedicated section documenting: condition education, self-management skills taught, warning signs communicated, resources provided

### Problem: Missing Safety Planning
**Deficiency**: No risk mitigation  
**Solution**: Specific safety concerns addressed (e.g., hypoglycemia risk with insulin, monitoring plan, patient taught recognition and treatment)

## Electronic Health Record (EHR) Integration

### Structured Data Entry
- Use templates for consistency
- Coded diagnoses (ICD-10), procedures (CPT)
- Structured goals enable outcome tracking
- Discrete medication fields (name, dose, route, frequency)

### Clinical Decision Support
- Evidence-based order sets
- Drug-drug interaction alerts
- Guideline reminders
- Quality measure tracking

### Care Plan Sharing
- Patient portal access (patient-friendly version)
- Interoperability standards (C-CDA)
- Shared with care team
- Transitions of care summary

## Audit and Peer Review

### Internal Quality Review
- Random sample chart audits (e.g., 5% quarterly)
- Checklist-based review (completeness, quality)
- Feedback to providers
- Continuous quality improvement

### External Review
- Payer audits (documentation supports billing)
- Regulatory surveys (Joint Commission, CMS)
- Malpractice case review
- Peer review for privileging/credentialing

### Audit Criteria
- Documentation completeness
- Clinical appropriateness
- Regulatory compliance
- Billing integrity
- Patient safety

## Treatment Plan Revision and Updates

### When to Update Treatment Plans

**Scheduled Updates**:
- Chronic disease management: Every 3-6 months minimum
- Behavioral health: Every 30-90 days depending on acuity
- Rehabilitation: Weekly to biweekly during active therapy
- Annual comprehensive update for all chronic conditions

**Triggered Updates**:
- Significant change in clinical status
- New diagnosis
- Treatment goals achieved or not progressing
- Patient request or preference change
- Hospitalization or emergency department visit
- Medication changes or adverse events

### Documentation of Changes
- Date of revision
- Reason for update
- What changed (goals, interventions, timeline)
- Provider signature
- Maintain prior versions for record

## Specialty-Specific Requirements

### Diabetes Management Plans
- HbA1c targets individualized
- Complication screening schedule (eyes, feet, kidneys)
- Self-monitoring blood glucose frequency
- Hypoglycemia recognition and treatment
- Sick day management

### Heart Failure Plans
- GDMT (guideline-directed medical therapy) checklist
- Volume management (daily weights, fluid/sodium restriction)
- NYHA functional class documentation
- Device therapy consideration
- Hospitalization triggers

### Mental Health Treatment Plans
- DSM-5 diagnostic criteria met
- Suicide/violence risk assessment
- Safety planning
- Psychotherapy modality and frequency
- Medication trials and responses
- Functional goals (return to work, relationships)

### Chronic Pain Plans
- Comprehensive pain assessment
- Functional goals (not just pain scores)
- Multimodal analgesia
- Opioid risk assessment if prescribing
- Physical and psychological interventions
- Activity modification and pacing

## Cultural Competence and Health Equity

### Culturally Appropriate Care
- Recognize cultural health beliefs and practices
- Address language barriers (interpreter services)
- Respect religious and cultural preferences in treatment
- Consider social determinants of health (housing, food security, transportation)
- Avoid assumptions based on stereotypes

### Health Literacy
- Assess patient understanding (teach-back method)
- Use plain language, avoid medical jargon
- Visual aids and written materials at appropriate reading level
- Tailor education to patient's learning style

### Addressing Disparities
- Screen for social needs and barriers
- Connect to community resources
- Culturally tailored interventions when evidence supports
- Track outcomes by demographic groups, address disparities

## References and Guidelines

### General Standards
- Joint Commission Standards Manual
- CMS Conditions of Participation
- State medical board documentation requirements

### Specialty Guidelines
- American College of Physicians (ACP)
- American Academy of Family Physicians (AAFP)
- American Psychiatric Association (APA)
- American Physical Therapy Association (APTA)
- Disease-specific societies (ADA, AHA, ACC, etc.)

### Regulatory
- HIPAA Privacy Rule (45 CFR Part 160, 164)
- 42 CFR Part 2 (Substance Use Disorder Confidentiality)
- 21 CFR Part 11 (Electronic Records, applicable for research/trials)
- State scope of practice laws

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Next Review**: January 2026
