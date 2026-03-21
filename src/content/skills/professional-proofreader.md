---
title: "Professional Proofreader"
description: "Use when a user asks to 'proofread', 'review and correct', 'fix grammar', 'improve readability while keeping my voice', and to proofread a document file and save an updated version."
category: "writing"
source: "community"
author: "Community"
tags: ["professional", "proofreader"]
date: 2026-03-20
---

# Professional Proofreader

## Overview

This skill transforms flawed writing — whether pasted text or uploaded documents — into publication-ready prose without altering the author’s intent.
It eliminates grammatical, spelling, punctuation, clarity, and tone issues while strictly preserving the author’s voice and intent.
Returns a corrected version plus a structured modification log, or generates an updated file when requested. Not for code editing or technical refactoring.

---

## When to Use

- Use when user asks to "proofread", "review and correct", "fix grammar", "polish this text", "improve readability while keeping my voice".
- Use when user asks to proofread a document file (like .docx, .pdf, .txt) and save the updated version as new file with 'UPDATED_' prefix.

---

# WORKFLOW MODES

This skill operates in two modes:
1. Inline Text Mode
2. File Processing Mode

### MODE 1: Inline Text

Refer [markdown](references/inline-text-mode.md) for complete inline text mode.

### MODE 2: File Processing

Trigger when user says:

- "Proofread [filename].[extension]
- "Edit this document"
- "Correct grammar in this file"
- "Save updated version"
- "Add prefix UPDATED_"
- "Return corrected .[extension]"

Refer [markdown](references/file-processing-mode.md) for complete file processing mode.

---

## Best Practices

### ✅ **Do:** [Good practice]
- Always include modification explanations.
- Always keep quality standards equivalent to: Academic proofreading, business document refinement, pre-publication review.
- Always follow below editing standards:

#### Grammar
- Subject-verb agreement  
- Tense consistency 
- Article usage 
- Prepositions
- Pronoun clarity 

#### Spelling
- Correct typos 
- Maintain original spelling variant (US/UK)

#### Punctuation
- Commas 
- Apostrophes 
- Quotation marks 
- Sentence boundaries 

#### Style & Tone
- Maintain author voice 
- Avoid unnecessary formalization 
- Preserve rhetorical choices 

#### Readability
- Improve structure 
- Enhance logical flow 
- Remove redundancy 

### ❌ **Don't:** [What to avoid] 
- Never alter meaning.
- Never drop formatting intentionally.
- Never change file name logic beyond request.
- Never expand the content

---

# Output Rules

If inline:
-> Return Corrected Version + Modifications list.

If file rewrite:
-> Save updated file.
-> Confirm filename.
-> Provide modifications list unless suppressed.

Give friendly message to user in the end.

---

---

## Reference: File Processing Mode

### File Processing Workflow

### 1. Identify File Type
Supported:
- .docx
- .txt
- .pdf (text-based)

If unsupported -> inform user clearly.

---

### 2. Extract Text
Read file contents completely before editing.

---

### 3. Apply Standard Proofreading Workflow
Follow:
- Error detection
- Voice preservation
- Minimal corrections
- Validation pass

---

### 4. Regenerate File

If user requests saving:

- Preserve original formatting where possible.
- Save corrected document.
- Apply requested prefix or naming rule.

Example:
Input: `weekly_meal_plan.docx`  
Output: `UPDATED_weekly_meal_plan.docx`

---

### 5. Return Both:

- Confirmation of saved file
- Modification log (unless user explicitly requests file-only output)

---

## Reference: Inline Text Mode

# MODE 1: Inline Text

## Step 1 — Content Isolation

Extract only the text intended for proofreading.

If no text is provided, respond:

> No text was provided for proofreading. Please paste the content you would like reviewed.

---

## Step 2 — Error Detection Pass

Scan for:

- Grammar violations  
- Spelling mistakes  
- Punctuation issues  
- Sentence fragments  
- Run-ons  
- Tense inconsistencies  
- Article/preposition misuse  
- Pronoun ambiguity  
- Redundancy  
- Awkward phrasing  
- Logical flow breaks  
- Tone inconsistency  
- Terminology inconsistency  

---

## Step 3 — Voice Preservation Check (CRITICAL)

Before modifying any sentence, verify:

- Is the tone intentional?
- Is informality deliberate?
- Is repetition rhetorical?
- Is fragmentation stylistic?

If grammatically valid and intentional → DO NOT CHANGE.

Never:

- Formalize casual writing without cause  
- Dilute emotional intensity  
- Replace distinctive vocabulary unnecessarily  
- Remove expressive phrasing  

---

## Step 4 — Minimal Necessary Corrections

Apply the smallest effective edit required.

Do not:

- Expand content  
- Add new ideas  
- Remove nuance  
- Rewrite entire paragraphs unless structurally broken  

Precision over preference.

---

## Step 5 — Clarity & Flow Optimization

Where required:

- Break long run-on sentences  
- Merge fragmented thoughts  
- Improve transitions  
- Remove redundancy  

Meaning must remain intact.

---

## Step 6 — Validation Pass

Before finalizing:

- Confirm zero remaining grammar errors  
- Confirm tone remains consistent  
- Confirm meaning is unchanged  
- Confirm no stylistic identity was erased  
- Confirm every edit is documented  

If violation detected → refine before output.

---
