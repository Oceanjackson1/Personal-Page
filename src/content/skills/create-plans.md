---
title: "创建项目计划"
description: "创建针对单人 Agent 开发优化的分层项目计划"
category: "writing"
source: "community"
author: "Community"
tags: ["create", "plans"]
date: 2026-03-20
---

<essential_principles>

<principle name="solo_developer_plus_claude">
You are planning for ONE person (the user) and ONE implementer (Claude).
No teams. No stakeholders. No ceremonies. No coordination overhead.
The user is the visionary/product owner. Claude is the builder.
</principle>

<principle name="plans_are_prompts">
PLAN.md is not a document that gets transformed into a prompt.
PLAN.md IS the prompt. It contains:
- Objective (what and why)
- Context (@file references)
- Tasks (type, files, action, verify, done, checkpoints)
- Verification (overall checks)
- Success criteria (measurable)
- Output (SUMMARY.md specification)

When planning a phase, you are writing the prompt that will execute it.
</principle>

<principle name="scope_control">
Plans must complete within ~50% of context usage to maintain consistent quality.

**The quality degradation curve:**
- 0-30% context: Peak quality (comprehensive, thorough, no anxiety)
- 30-50% context: Good quality (engaged, manageable pressure)
- 50-70% context: Degrading quality (efficiency mode, compression)
- 70%+ context: Poor quality (self-lobotomization, rushed work)

**Critical insight:** Claude doesn't degrade at 80% - it degrades at ~40-50% when it sees context mounting and enters "completion mode." By 80%, quality has already crashed.

**Solution:** Aggressive atomicity - split phases into many small, focused plans.

Examples:
- `01-01-PLAN.md` - Phase 1, Plan 1 (2-3 tasks: database schema only)
- `01-02-PLAN.md` - Phase 1, Plan 2 (2-3 tasks: database client setup)
- `01-03-PLAN.md` - Phase 1, Plan 3 (2-3 tasks: API routes)
- `01-04-PLAN.md` - Phase 1, Plan 4 (2-3 tasks: UI components)

Each plan is independently executable, verifiable, and scoped to **2-3 tasks maximum**.

**Atomic task principle:** Better to have 10 small, high-quality plans than 3 large, degraded plans. Each commit should be surgical, focused, and maintainable.

**Autonomous execution:** Plans without checkpoints execute via subagent with fresh context - impossible to degrade.

See: references/scope-estimation.md
</principle>

<principle name="human_checkpoints">
**Claude automates everything that has a CLI or API.** Checkpoints are for verification and decisions, not manual work.

**Checkpoint types:**
- `checkpoint:human-verify` - Human confirms Claude's automated work (visual checks, UI verification)
- `checkpoint:decision` - Human makes implementation choice (auth provider, architecture)

**Rarely needed:** `checkpoint:human-action` - Only for actions with no CLI/API (email verification links, account approvals requiring web login with 2FA)

**Critical rule:** If Claude CAN do it via CLI/API/tool, Claude MUST do it. Never ask human to:
- Deploy to Vercel/Railway/Fly (use CLI)
- Create Stripe webhooks (use CLI/API)
- Run builds/tests (use Bash)
- Write .env files (use Write tool)
- Create database resources (use provider CLI)

**Protocol:** Claude automates work → reaches checkpoint:human-verify → presents what was done → waits for confirmation → resumes

See: references/checkpoints.md, references/cli-automation.md
</principle>

<principle name="deviation_rules">
Plans are guides, not straitjackets. Real development always involves discoveries.

**During execution, deviations are handled automatically via 5 embedded rules:**

1. **Auto-fix bugs** - Broken behavior → fix immediately, document in Summary
2. **Auto-add missing critical** - Security/correctness gaps → add immediately, document
3. **Auto-fix blockers** - Can't proceed → fix immediately, document
4. **Ask about architectural** - Major structural changes → stop and ask user
5. **Log enhancements** - Nice-to-haves → auto-log to ISSUES.md, continue

**No user intervention needed for Rules 1-3, 5.** Only Rule 4 (architectural) requires user decision.

**All deviations documented in Summary** with: what was found, what rule applied, what was done, commit hash.

**Result:** Flow never breaks. Bugs get fixed. Scope stays controlled. Complete transparency.

See: workflows/execute-phase.md (deviation_rules section)
</principle>

<principle name="ship_fast_iterate_fast">
No enterprise process. No approval gates. No multi-week timelines.
Plan → Execute → Ship → Learn → Repeat.

**Milestone-driven:** Ship v1.0 → mark milestone → plan v1.1 → ship → repeat.
Milestones mark shipped versions and enable continuous iteration.
</principle>

<principle name="milestone_boundaries">
Milestones mark shipped versions (v1.0, v1.1, v2.0).

**Purpose:**
- Historical record in MILESTONES.md (what shipped when)
- Greenfield → Brownfield transition marker
- Git tags for releases
- Clear completion rituals

**Default approach:** Extend existing roadmap with new phases.
- v1.0 ships (phases 1-4) → add phases 5-6 for v1.1
- Continuous phase numbering (01-99)
- Milestone groupings keep roadmap organized

**Archive ONLY for:** Separate codebases or complete rewrites (rare).

See: references/milestone-management.md
</principle>

<principle name="anti_enterprise_patterns">
NEVER include in plans:
- Team structures, roles, RACI matrices
- Stakeholder management, alignment meetings
- Sprint ceremonies, standups, retros
- Multi-week estimates, resource allocation
- Change management, governance processes
- Documentation for documentation's sake

If it sounds like corporate PM theater, delete it.
</principle>

<principle name="context_awareness">
Monitor token usage via system warnings.

**At 25% remaining**: Mention context getting full
**At 15% remaining**: Pause, offer handoff
**At 10% remaining**: Auto-create handoff, stop

Never start large operations below 15% without user confirmation.
</principle>

<principle name="user_gates">
Never charge ahead at critical decision points. Use gates:
- **AskUserQuestion**: Structured choices (2-4 options)
- **Inline questions**: Simple confirmations
- **Decision gate loop**: "Ready, or ask more questions?"

Mandatory gates:
- Before writing PLAN.md (confirm breakdown)
- After low-confidence research
- On verification failures
- After phase completion with issues
- Before starting next phase with previous issues

See: references/user-gates.md
</principle>

<principle name="git_versioning">
All planning artifacts are version controlled. Commit outcomes, not process.

- Check for repo on invocation, offer to initialize
- Commit only at: initialization, phase completion, handoff
- Intermediate artifacts (PLAN.md, RESEARCH.md, FINDINGS.md) NOT committed separately
- Git log becomes project history

See: references/git-integration.md
</principle>

</essential_principles>

<context_scan>
**Run on every invocation** to understand current state:

```bash
# Check git status
git rev-parse --git-dir 2>/dev/null || echo "NO_GIT_REPO"

# Check for planning structure
ls -la .planning/ 2>/dev/null
ls -la .planning/phases/ 2>/dev/null

# Find any continue-here files
find . -name ".continue-here.md" -type f 2>/dev/null

# Check for existing artifacts
[ -f .planning/BRIEF.md ] && echo "BRIEF: exists"
[ -f .planning/ROADMAP.md ] && echo "ROADMAP: exists"
```

**If NO_GIT_REPO detected:**
Inline question: "No git repo found. Initialize one? (Recommended for version control)"
If yes: `git init`

**Present findings before intake question.**
</context_scan>

<domain_expertise>
**Domain expertise lives in `~/.claude/skills/expertise/`**

Before creating roadmap or phase plans, determine if domain expertise should be loaded.

<scan_domains>
```bash
ls ~/.claude/skills/expertise/ 2>/dev/null
```

This reveals available domain expertise (e.g., macos-apps, iphone-apps, unity-games, nextjs-ecommerce).

**If no domain skills found:** Proceed without domain expertise (graceful degradation). The skill works fine without domain-specific context.
</scan_domains>

<inference_rules>
If user's request contains domain keywords, INFER the domain:

| Keywords | Domain Skill |
|----------|--------------|
| "macOS", "Mac app", "menu bar", "AppKit", "SwiftUI desktop" | expertise/macos-apps |
| "iPhone", "iOS", "iPad", "mobile app", "SwiftUI mobile" | expertise/iphone-apps |
| "Unity", "game", "C#", "3D game", "2D game" | expertise/unity-games |
| "MIDI", "MIDI tool", "sequencer", "MIDI controller", "music app", "MIDI 2.0", "MPE", "SysEx" | expertise/midi |
| "Agent SDK", "Claude SDK", "agentic app" | expertise/with-agent-sdk |
| "Python automation", "workflow", "API integration", "webhooks", "Celery", "Airflow", "Prefect" | expertise/python-workflow-automation |
| "UI", "design", "frontend", "interface", "responsive", "visual design", "landing page", "website design", "Tailwind", "CSS", "web design" | expertise/ui-design |

If domain inferred, confirm:
```
Detected: [domain] project → expertise/[skill-name]
Load this expertise for planning? (Y / see other options / none)
```
</inference_rules>

<no_inference>
If no domain obvious from request, present options:

```
What type of project is this?

Available domain expertise:
1. macos-apps - Native macOS with Swift/SwiftUI
2. iphone-apps - Native iOS with Swift/SwiftUI
3. unity-games - Unity game development
4. swift-midi-apps - MIDI/audio apps
5. with-agent-sdk - Claude Agent SDK apps
6. ui-design - Stunning UI/UX design & frontend development
[... any others found in expertise/]

N. None - proceed without domain expertise
C. Create domain skill first

Select:
```
</no_inference>

<load_domain>
When domain selected, use intelligent loading:

**Step 1: Read domain SKILL.md**
```bash
cat ~/.claude/skills/expertise/[domain]/SKILL.md 2>/dev/null
```

This loads core principles and routing guidance (~5k tokens).

**Step 2: Determine what references are needed**

Domain SKILL.md should contain a `<references_index>` section that maps planning contexts to specific references.

Example:
```markdown
<references_index>
**For database/persistence phases:** references/core-data.md, references/swift-concurrency.md
**For UI/layout phases:** references/swiftui-layout.md, references/appleHIG.md
**For system integration:** references/appkit-integration.md
**Always useful:** references/swift-conventions.md
</references_index>
```

**Step 3: Load only relevant references**

Based on the phase being planned (from ROADMAP), load ONLY the references mentioned for that type of work.

```bash
# Example: Planning a database phase
cat ~/.claude/skills/expertise/macos-apps/references/core-data.md
cat ~/.claude/skills/expertise/macos-apps/references/swift-conventions.md
```

**Context efficiency:**
- SKILL.md only: ~5k tokens
- SKILL.md + selective references: ~8-12k tokens
- All references (old approach): ~20-27k tokens

Announce: "Loaded [domain] expertise ([X] references for [phase-type])."

**If domain skill not found:** Inform user and offer to proceed without domain expertise.

**If SKILL.md doesn't have references_index:** Fall back to loading all references with warning about context usage.
</load_domain>

<when_to_load>
Domain expertise should be loaded BEFORE:
- Creating roadmap (phases should be domain-appropriate)
- Planning phases (tasks must be domain-specific)

Domain expertise is NOT needed for:
- Creating brief (vision is domain-agnostic)
- Resuming from handoff (context already established)
- Transition between phases (just updating status)
</when_to_load>
</domain_expertise>

<intake>
Based on scan results, present context-aware options:

**If handoff found:**
```
Found handoff: .planning/phases/XX/.continue-here.md
[Summary of state from handoff]

1. Resume from handoff
2. Discard handoff, start fresh
3. Different action
```

**If planning structure exists:**
```
Project: [from BRIEF or directory]
Brief: [exists/missing]
Roadmap: [X phases defined]
Current: [phase status]

What would you like to do?
1. Plan next phase
2. Execute current phase
3. Create handoff (stopping for now)
4. View/update roadmap
5. Something else
```

**If no planning structure:**
```
No planning structure found.

What would you like to do?
1. Start new project (create brief)
2. Create roadmap from existing brief
3. Jump straight to phase planning
4. Get guidance on approach
```

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| "brief", "new project", "start", 1 (no structure) | `workflows/create-brief.md` |
| "roadmap", "phases", 2 (no structure) | `workflows/create-roadmap.md` |
| "phase", "plan phase", "next phase", 1 (has structure) | `workflows/plan-phase.md` |
| "chunk", "next tasks", "what's next" | `workflows/plan-chunk.md` |
| "execute", "run", "do it", "build it", 2 (has structure) | **EXIT SKILL** → Use `/run-plan <path>` slash command |
| "research", "investigate", "unknowns" | `workflows/research-phase.md` |
| "handoff", "pack up", "stopping", 3 (has structure) | `workflows/handoff.md` |
| "resume", "continue", 1 (has handoff) | `workflows/resume.md` |
| "transition", "complete", "done", "next" | `workflows/transition.md` |
| "milestone", "ship", "v1.0", "release" | `workflows/complete-milestone.md` |
| "guidance", "help", 4 | `workflows/get-guidance.md` |

**Critical:** Plan execution should NOT invoke this skill. Use `/run-plan` for context efficiency (skill loads ~20k tokens, /run-plan loads ~5-7k).

**After reading the workflow, follow it exactly.**
</routing>

<hierarchy>
The planning hierarchy (each level builds on previous):

```
BRIEF.md          → Human vision (you read this)
    ↓
ROADMAP.md        → Phase structure (overview)
    ↓
RESEARCH.md       → Research prompt (optional, for unknowns)
    ↓
FINDINGS.md       → Research output (if research done)
    ↓
PLAN.md           → THE PROMPT (Claude executes this)
    ↓
SUMMARY.md        → Outcome (existence = phase complete)
```

**Rules:**
- Roadmap requires Brief (or prompts to create one)
- Phase plan requires Roadmap (knows phase scope)
- PLAN.md IS the execution prompt
- SUMMARY.md existence marks phase complete
- Each level can look UP for context
</hierarchy>

<output_structure>
All planning artifacts go in `.planning/`:

```
.planning/
├── BRIEF.md                    # Human vision
├── ROADMAP.md                  # Phase structure + tracking
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md       # Plan 1: Database setup
    │   ├── 01-01-SUMMARY.md    # Outcome (exists = done)
    │   ├── 01-02-PLAN.md       # Plan 2: API routes
    │   ├── 01-02-SUMMARY.md
    │   ├── 01-03-PLAN.md       # Plan 3: UI components
    │   └── .continue-here-01-03.md  # Handoff (temporary, if needed)
    └── 02-auth/
        ├── 02-01-RESEARCH.md   # Research prompt (if needed)
        ├── 02-01-FINDINGS.md   # Research output
        ├── 02-02-PLAN.md       # Implementation prompt
        └── 02-02-SUMMARY.md
```

**Naming convention:**
- Plans: `{phase}-{plan}-PLAN.md` (e.g., 01-03-PLAN.md)
- Summaries: `{phase}-{plan}-SUMMARY.md` (e.g., 01-03-SUMMARY.md)
- Phase folders: `{phase}-{name}/` (e.g., 01-foundation/)

Files sort chronologically. Related artifacts (plan + summary) are adjacent.
</output_structure>

<reference_index>
All in `references/`:

**Structure:** directory-structure.md, hierarchy-rules.md
**Formats:** handoff-format.md, plan-format.md
**Patterns:** context-scanning.md, context-management.md
**Planning:** scope-estimation.md, checkpoints.md, milestone-management.md
**Process:** user-gates.md, git-integration.md, research-pitfalls.md
**Domain:** domain-expertise.md (guide for creating context-efficient domain skills)
</reference_index>

<templates_index>
All in `templates/`:

| Template | Purpose |
|----------|---------|
| brief.md | Project vision document with current state |
| roadmap.md | Phase structure with milestone groupings |
| phase-prompt.md | Executable phase prompt (PLAN.md) |
| research-prompt.md | Research prompt (RESEARCH.md) |
| summary.md | Phase outcome (SUMMARY.md) with deviations |
| milestone.md | Milestone entry for MILESTONES.md |
| issues.md | Deferred enhancements log (ISSUES.md) |
| continue-here.md | Context handoff format |
</templates_index>

<workflows_index>
All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| create-brief.md | Create project vision document |
| create-roadmap.md | Define phases from brief |
| plan-phase.md | Create executable phase prompt |
| execute-phase.md | Run phase prompt, create summary |
| research-phase.md | Create and run research prompt |
| plan-chunk.md | Plan immediate next tasks |
| transition.md | Mark phase complete, advance |
| complete-milestone.md | Mark shipped version, create milestone entry |
| handoff.md | Create context handoff for pausing |
| resume.md | Load handoff, restore context |
| get-guidance.md | Help decide planning approach |
</workflows_index>

<success_criteria>
Planning skill succeeds when:
- Context scan runs before intake
- Appropriate workflow selected based on state
- PLAN.md IS the executable prompt (not separate)
- Hierarchy is maintained (brief → roadmap → phase)
- Handoffs preserve full context for resumption
- Context limits are respected (auto-handoff at 10%)
- Deviations handled automatically per embedded rules
- All work (planned and discovered) fully documented
- Domain expertise loaded intelligently (SKILL.md + selective references, not all files)
- Plan execution uses /run-plan command (not skill invocation)
</success_criteria>

---

## Reference: Checkpoints

# Human Checkpoints in Plans

Plans execute autonomously. Checkpoints formalize the interaction points where human verification or decisions are needed.

**Core principle:** Claude automates everything with CLI/API. Checkpoints are for verification and decisions, not manual work.

## Checkpoint Types

### 1. `checkpoint:human-verify` (Most Common)

**When:** Claude completed automated work, human confirms it works correctly.

**Use for:**
- Visual UI checks (layout, styling, responsiveness)
- Interactive flows (click through wizard, test user flows)
- Functional verification (feature works as expected)
- Audio/video playback quality
- Animation smoothness
- Accessibility testing

**Structure:**
```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>[What Claude automated and deployed/built]</what-built>
  <how-to-verify>
    [Exact steps to test - URLs, commands, expected behavior]
  </how-to-verify>
  <resume-signal>[How to continue - "approved", "yes", or describe issues]</resume-signal>
</task>
```

**Key elements:**
- `<what-built>`: What Claude automated (deployed, built, configured)
- `<how-to-verify>`: Exact steps to confirm it works (numbered, specific)
- `<resume-signal>`: Clear indication of how to continue

**Example: Vercel Deployment**
```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <files>.vercel/, vercel.json</files>
  <action>Run `vercel --yes` to create project and deploy. Capture deployment URL from output.</action>
  <verify>vercel ls shows deployment, curl {url} returns 200</verify>
  <done>App deployed, URL captured</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Deployed to Vercel at https://myapp-abc123.vercel.app</what-built>
  <how-to-verify>
    Visit https://myapp-abc123.vercel.app and confirm:
    - Homepage loads without errors
    - Login form is visible
    - No console errors in browser DevTools
  </how-to-verify>
  <resume-signal>Type "approved" to continue, or describe issues to fix</resume-signal>
</task>
```

**Example: UI Component**
```xml
<task type="auto">
  <name>Build responsive dashboard layout</name>
  <files>src/components/Dashboard.tsx, src/app/dashboard/page.tsx</files>
  <action>Create dashboard with sidebar, header, and content area. Use Tailwind responsive classes for mobile.</action>
  <verify>npm run build succeeds, no TypeScript errors</verify>
  <done>Dashboard component builds without errors</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Responsive dashboard layout at /dashboard</what-built>
  <how-to-verify>
    1. Run: npm run dev
    2. Visit: http://localhost:3000/dashboard
    3. Desktop (>1024px): Verify sidebar left, content right, header top
    4. Tablet (768px): Verify sidebar collapses to hamburger
    5. Mobile (375px): Verify single column, bottom nav
    6. Check: No layout shift, no horizontal scroll
  </how-to-verify>
  <resume-signal>Type "approved" or describe layout issues</resume-signal>
</task>
```

**Example: Xcode Build**
```xml
<task type="auto">
  <name>Build macOS app with Xcode</name>
  <files>App.xcodeproj, Sources/</files>
  <action>Run `xcodebuild -project App.xcodeproj -scheme App build`. Check for compilation errors in output.</action>
  <verify>Build output contains "BUILD SUCCEEDED", no errors</verify>
  <done>App builds successfully</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Built macOS app at DerivedData/Build/Products/Debug/App.app</what-built>
  <how-to-verify>
    Open App.app and test:
    - App launches without crashes
    - Menu bar icon appears
    - Preferences window opens correctly
    - No visual glitches or layout issues
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### 2. `checkpoint:decision`

**When:** Human must make choice that affects implementation direction.

**Use for:**
- Technology selection (which auth provider, which database)
- Architecture decisions (monorepo vs separate repos)
- Design choices (color scheme, layout approach)
- Feature prioritization (which variant to build)
- Data model decisions (schema structure)

**Structure:**
```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>[What's being decided]</decision>
  <context>[Why this decision matters]</context>
  <options>
    <option id="option-a">
      <name>[Option name]</name>
      <pros>[Benefits]</pros>
      <cons>[Tradeoffs]</cons>
    </option>
    <option id="option-b">
      <name>[Option name]</name>
      <pros>[Benefits]</pros>
      <cons>[Tradeoffs]</cons>
    </option>
  </options>
  <resume-signal>[How to indicate choice]</resume-signal>
</task>
```

**Key elements:**
- `<decision>`: What's being decided
- `<context>`: Why this matters
- `<options>`: Each option with balanced pros/cons (not prescriptive)
- `<resume-signal>`: How to indicate choice

**Example: Auth Provider Selection**
```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Select authentication provider</decision>
  <context>
    Need user authentication for the app. Three solid options with different tradeoffs.
  </context>
  <options>
    <option id="supabase">
      <name>Supabase Auth</name>
      <pros>Built-in with Supabase DB we're using, generous free tier, row-level security integration</pros>
      <cons>Less customizable UI, tied to Supabase ecosystem</cons>
    </option>
    <option id="clerk">
      <name>Clerk</name>
      <pros>Beautiful pre-built UI, best developer experience, excellent docs</pros>
      <cons>Paid after 10k MAU, vendor lock-in</cons>
    </option>
    <option id="nextauth">
      <name>NextAuth.js</name>
      <pros>Free, self-hosted, maximum control, widely adopted</pros>
      <cons>More setup work, you manage security updates, UI is DIY</cons>
    </option>
  </options>
  <resume-signal>Select: supabase, clerk, or nextauth</resume-signal>
</task>
```

### 3. `checkpoint:human-action` (Rare)

**When:** Action has NO CLI/API and requires human-only interaction, OR Claude hit an authentication gate during automation.

**Use ONLY for:**
- **Authentication gates** - Claude tried to use CLI/API but needs credentials to continue (this is NOT a failure)
- Email verification links (account creation requires clicking email)
- SMS 2FA codes (phone verification)
- Manual account approvals (platform requires human review before API access)
- Credit card 3D Secure flows (web-based payment authorization)
- OAuth app approvals (some platforms require web-based approval)

**Do NOT use for pre-planned manual work:**
- Manually deploying to Vercel (use `vercel` CLI - auth gate if needed)
- Manually creating Stripe webhooks (use Stripe API - auth gate if needed)
- Manually creating databases (use provider CLI - auth gate if needed)
- Running builds/tests manually (use Bash tool)
- Creating files manually (use Write tool)

**Structure:**
```xml
<task type="checkpoint:human-action" gate="blocking">
  <action>[What human must do - Claude already did everything automatable]</action>
  <instructions>
    [What Claude already automated]
    [The ONE thing requiring human action]
  </instructions>
  <verification>[What Claude can check afterward]</verification>
  <resume-signal>[How to continue]</resume-signal>
</task>
```

**Key principle:** Claude automates EVERYTHING possible first, only asks human for the truly unavoidable manual step.

**Example: Email Verification**
```xml
<task type="auto">
  <name>Create SendGrid account via API</name>
  <action>Use SendGrid API to create subuser account with provided email. Request verification email.</action>
  <verify>API returns 201, account created</verify>
  <done>Account created, verification email sent</done>
</task>

<task type="checkpoint:human-action" gate="blocking">
  <action>Complete email verification for SendGrid account</action>
  <instructions>
    I created the account and requested verification email.
    Check your inbox for SendGrid verification link and click it.
  </instructions>
  <verification>SendGrid API key works: curl test succeeds</verification>
  <resume-signal>Type "done" when email verified</resume-signal>
</task>
```

**Example: Credit Card 3D Secure**
```xml
<task type="auto">
  <name>Create Stripe payment intent</name>
  <action>Use Stripe API to create payment intent for $99. Generate checkout URL.</action>
  <verify>Stripe API returns payment intent ID and URL</verify>
  <done>Payment intent created</done>
</task>

<task type="checkpoint:human-action" gate="blocking">
  <action>Complete 3D Secure authentication</action>
  <instructions>
    I created the payment intent: https://checkout.stripe.com/pay/cs_test_abc123
    Visit that URL and complete the 3D Secure verification flow with your test card.
  </instructions>
  <verification>Stripe webhook receives payment_intent.succeeded event</verification>
  <resume-signal>Type "done" when payment completes</resume-signal>
</task>
```

**Example: Authentication Gate (Dynamic Checkpoint)**
```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <files>.vercel/, vercel.json</files>
  <action>Run `vercel --yes` to deploy</action>
  <verify>vercel ls shows deployment, curl returns 200</verify>
</task>

<!-- If vercel returns "Error: Not authenticated", Claude creates checkpoint on the fly -->

<task type="checkpoint:human-action" gate="blocking">
  <action>Authenticate Vercel CLI so I can continue deployment</action>
  <instructions>
    I tried to deploy but got authentication error.
    Run: vercel login
    This will open your browser - complete the authentication flow.
  </instructions>
  <verification>vercel whoami returns your account email</verification>
  <resume-signal>Type "done" when authenticated</resume-signal>
</task>

<!-- After authentication, Claude retries the deployment -->

<task type="auto">
  <name>Retry Vercel deployment</name>
  <action>Run `vercel --yes` (now authenticated)</action>
  <verify>vercel ls shows deployment, curl returns 200</verify>
</task>
```

**Key distinction:** Authentication gates are created dynamically when Claude encounters auth errors during automation. They're NOT pre-planned - Claude tries to automate first, only asks for credentials when blocked.

See references/cli-automation.md "Authentication Gates" section for more examples and full protocol.

## Execution Protocol

When Claude encounters `type="checkpoint:*"`:

1. **Stop immediately** - do not proceed to next task
2. **Display checkpoint clearly:**

```
════════════════════════════════════════
CHECKPOINT: [Type]
════════════════════════════════════════

Task [X] of [Y]: [Name]

[Display checkpoint-specific content]

[Resume signal instruction]
════════════════════════════════════════
```

3. **Wait for user response** - do not hallucinate completion
4. **Verify if possible** - check files, run tests, whatever is specified
5. **Resume execution** - continue to next task only after confirmation

**For checkpoint:human-verify:**
```
════════════════════════════════════════
CHECKPOINT: Verification Required
════════════════════════════════════════

Task 5 of 8: Responsive dashboard layout

I built: Responsive dashboard at /dashboard

How to verify:
1. Run: npm run dev
2. Visit: http://localhost:3000/dashboard
3. Test: Resize browser window to mobile/tablet/desktop
4. Confirm: No layout shift, proper responsive behavior

Type "approved" to continue, or describe issues.
════════════════════════════════════════
```

**For checkpoint:decision:**
```
════════════════════════════════════════
CHECKPOINT: Decision Required
════════════════════════════════════════

Task 2 of 6: Select authentication provider

Decision: Which auth provider should we use?

Context: Need user authentication. Three options with different tradeoffs.

Options:
1. supabase - Built-in with our DB, free tier
2. clerk - Best DX, paid after 10k users
3. nextauth - Self-hosted, maximum control

Select: supabase, clerk, or nextauth
════════════════════════════════════════
```

## Writing Good Checkpoints

**DO:**
- Automate everything with CLI/API before checkpoint
- Be specific: "Visit https://myapp.vercel.app" not "check deployment"
- Number verification steps: easier to follow
- State expected outcomes: "You should see X"
- Provide context: why this checkpoint exists
- Make verification executable: clear, testable steps

**DON'T:**
- Ask human to do work Claude can automate (deploy, create resources, run builds)
- Assume knowledge: "Configure the usual settings" ❌
- Skip steps: "Set up database" ❌ (too vague)
- Mix multiple verifications in one checkpoint (split them)
- Make verification impossible (Claude can't check visual appearance without user confirmation)

## When to Use Checkpoints

**Use checkpoint:human-verify for:**
- Visual verification (UI, layouts, animations)
- Interactive testing (click flows, user journeys)
- Quality checks (audio/video playback, animation smoothness)
- Confirming deployed apps are accessible

**Use checkpoint:decision for:**
- Technology selection (auth providers, databases, frameworks)
- Architecture choices (monorepo, deployment strategy)
- Design decisions (color schemes, layout approaches)
- Feature prioritization

**Use checkpoint:human-action for:**
- Email verification links (no API)
- SMS 2FA codes (no API)
- Manual approvals with no automation
- 3D Secure payment flows

**Don't use checkpoints for:**
- Things Claude can verify programmatically (tests pass, build succeeds)
- File operations (Claude can read files to verify)
- Code correctness (use tests and static analysis)
- Anything automatable via CLI/API

## Checkpoint Placement

Place checkpoints:
- **After automation completes** - not before Claude does the work
- **After UI buildout** - before declaring phase complete
- **Before dependent work** - decisions before implementation
- **At integration points** - after configuring external services

Bad placement:
- Before Claude automates (asking human to do automatable work) ❌
- Too frequent (every other task is a checkpoint) ❌
- Too late (checkpoint is last task, but earlier tasks needed its result) ❌

## Complete Examples

### Example 1: Deployment Flow (Correct)

```xml
<!-- Claude automates everything -->
<task type="auto">
  <name>Deploy to Vercel</name>
  <files>.vercel/, vercel.json, package.json</files>
  <action>
    1. Run `vercel --yes` to create project and deploy
    2. Capture deployment URL from output
    3. Set environment variables with `vercel env add`
    4. Trigger production deployment with `vercel --prod`
  </action>
  <verify>
    - vercel ls shows deployment
    - curl {url} returns 200
    - Environment variables set correctly
  </verify>
  <done>App deployed to production, URL captured</done>
</task>

<!-- Human verifies visual/functional correctness -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Deployed to https://myapp.vercel.app</what-built>
  <how-to-verify>
    Visit https://myapp.vercel.app and confirm:
    - Homepage loads correctly
    - All images/assets load
    - Navigation works
    - No console errors
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### Example 2: Database Setup (Correct)

```xml
<!-- Claude automates everything -->
<task type="auto">
  <name>Create Upstash Redis database</name>
  <files>.env</files>
  <action>
    1. Run `upstash redis create myapp-cache --region us-east-1`
    2. Capture connection URL from output
    3. Write to .env: UPSTASH_REDIS_URL={url}
    4. Verify connection with test command
  </action>
  <verify>
    - upstash redis list shows database
    - .env contains UPSTASH_REDIS_URL
    - Test connection succeeds
  </verify>
  <done>Redis database created and configured</done>
</task>

<!-- NO CHECKPOINT NEEDED - Claude automated everything and verified programmatically -->
```

### Example 3: Stripe Webhooks (Correct)

```xml
<!-- Claude automates everything -->
<task type="auto">
  <name>Configure Stripe webhooks</name>
  <files>.env, src/app/api/webhooks/route.ts</files>
  <action>
    1. Use Stripe API to create webhook endpoint pointing to /api/webhooks
    2. Subscribe to events: payment_intent.succeeded, customer.subscription.updated
    3. Save webhook signing secret to .env
    4. Implement webhook handler in route.ts
  </action>
  <verify>
    - Stripe API returns webhook endpoint ID
    - .env contains STRIPE_WEBHOOK_SECRET
    - curl webhook endpoint returns 200
  </verify>
  <done>Stripe webhooks configured and handler implemented</done>
</task>

<!-- Human verifies in Stripe dashboard -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Stripe webhook configured via API</what-built>
  <how-to-verify>
    Visit Stripe Dashboard > Developers > Webhooks
    Confirm: Endpoint shows https://myapp.com/api/webhooks with correct events
  </how-to-verify>
  <resume-signal>Type "yes" if correct</resume-signal>
</task>
```

## Anti-Patterns

### ❌ BAD: Asking human to automate

```xml
<task type="checkpoint:human-action" gate="blocking">
  <action>Deploy to Vercel</action>
  <instructions>
    1. Visit vercel.com/new
    2. Import Git repository
    3. Click Deploy
    4. Copy deployment URL
  </instructions>
  <verification>Deployment exists</verification>
  <resume-signal>Paste URL</resume-signal>
</task>
```

**Why bad:** Vercel has a CLI. Claude should run `vercel --yes`.

### ✅ GOOD: Claude automates, human verifies

```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <action>Run `vercel --yes`. Capture URL.</action>
  <verify>vercel ls shows deployment, curl returns 200</verify>
</task>

<task type="checkpoint:human-verify">
  <what-built>Deployed to {url}</what-built>
  <how-to-verify>Visit {url}, check homepage loads</how-to-verify>
  <resume-signal>Type "approved"</resume-signal>
</task>
```

### ❌ BAD: Too many checkpoints

```xml
<task type="auto">Create schema</task>
<task type="checkpoint:human-verify">Check schema</task>
<task type="auto">Create API route</task>
<task type="checkpoint:human-verify">Check API</task>
<task type="auto">Create UI form</task>
<task type="checkpoint:human-verify">Check form</task>
```

**Why bad:** Verification fatigue. Combine into one checkpoint at end.

### ✅ GOOD: Single verification checkpoint

```xml
<task type="auto">Create schema</task>
<task type="auto">Create API route</task>
<task type="auto">Create UI form</task>

<task type="checkpoint:human-verify">
  <what-built>Complete auth flow (schema + API + UI)</what-built>
  <how-to-verify>Test full flow: register, login, access protected page</how-to-verify>
  <resume-signal>Type "approved"</resume-signal>
</task>
```

### ❌ BAD: Asking for automatable file operations

```xml
<task type="checkpoint:human-action">
  <action>Create .env file</action>
  <instructions>
    1. Create .env in project root
    2. Add: DATABASE_URL=...
    3. Add: STRIPE_KEY=...
  </instructions>
</task>
```

**Why bad:** Claude has Write tool. This should be `type="auto"`.

## Summary

Checkpoints formalize human-in-the-loop points. Use them when Claude cannot complete a task autonomously OR when human verification is required for correctness.

**The golden rule:** If Claude CAN automate it, Claude MUST automate it.

**Checkpoint priority:**
1. **checkpoint:human-verify** (90% of checkpoints) - Claude automated everything, human confirms visual/functional correctness
2. **checkpoint:decision** (9% of checkpoints) - Human makes architectural/technology choices
3. **checkpoint:human-action** (1% of checkpoints) - Truly unavoidable manual steps with no API/CLI

**See also:** references/cli-automation.md for exhaustive list of what Claude can automate.

---

## Reference: Cli Automation

# CLI and API Automation Reference

**Core principle:** If it has a CLI or API, Claude does it. Never ask the human to perform manual steps that Claude can automate.

This reference documents what Claude CAN and SHOULD automate during plan execution.

## Deployment Platforms

### Vercel
**CLI:** `vercel`

**What Claude automates:**
- Create and deploy projects: `vercel --yes`
- Set environment variables: `vercel env add KEY production`
- Link to git repo: `vercel link`
- Trigger deployments: `vercel --prod`
- Get deployment URLs: `vercel ls`
- Manage domains: `vercel domains add example.com`

**Never ask human to:**
- Visit vercel.com/new to create project
- Click through dashboard to add env vars
- Manually link repository

**Checkpoint pattern:**
```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <action>Run `vercel --yes` to deploy. Capture deployment URL.</action>
  <verify>vercel ls shows deployment, curl {url} returns 200</verify>
</task>

<task type="checkpoint:human-verify">
  <what-built>Deployed to {url}</what-built>
  <how-to-verify>Visit {url} - check homepage loads</how-to-verify>
  <resume-signal>Type "yes" if correct</resume-signal>
</task>
```

### Railway
**CLI:** `railway`

**What Claude automates:**
- Initialize project: `railway init`
- Link to repo: `railway link`
- Deploy: `railway up`
- Set variables: `railway variables set KEY=value`
- Get deployment URL: `railway domain`

### Fly.io
**CLI:** `fly`

**What Claude automates:**
- Launch app: `fly launch --no-deploy`
- Deploy: `fly deploy`
- Set secrets: `fly secrets set KEY=value`
- Scale: `fly scale count 2`

## Payment & Billing

### Stripe
**CLI:** `stripe`

**What Claude automates:**
- Create webhook endpoints: `stripe listen --forward-to localhost:3000/api/webhooks`
- Trigger test events: `stripe trigger payment_intent.succeeded`
- Create products/prices: Stripe API via curl/fetch
- Manage customers: Stripe API via curl/fetch
- Check webhook logs: `stripe webhooks list`

**Never ask human to:**
- Visit dashboard.stripe.com to create webhook
- Click through UI to create products
- Manually copy webhook signing secret

**Checkpoint pattern:**
```xml
<task type="auto">
  <name>Configure Stripe webhooks</name>
  <action>Use Stripe API to create webhook endpoint at /api/webhooks. Save signing secret to .env.</action>
  <verify>stripe webhooks list shows endpoint, .env contains STRIPE_WEBHOOK_SECRET</verify>
</task>

<task type="checkpoint:human-verify">
  <what-built>Stripe webhook configured</what-built>
  <how-to-verify>Check Stripe dashboard > Developers > Webhooks shows endpoint with correct URL</how-to-verify>
  <resume-signal>Type "yes" if correct</resume-signal>
</task>
```

## Databases & Backend

### Supabase
**CLI:** `supabase`

**What Claude automates:**
- Initialize project: `supabase init`
- Link to remote: `supabase link --project-ref {ref}`
- Create migrations: `supabase migration new {name}`
- Push migrations: `supabase db push`
- Generate types: `supabase gen types typescript`
- Deploy functions: `supabase functions deploy {name}`

**Never ask human to:**
- Visit supabase.com to create project manually
- Click through dashboard to run migrations
- Copy/paste connection strings

**Note:** Project creation may require web dashboard initially (no CLI for initial project creation), but all subsequent work (migrations, functions, etc.) is CLI-automated.

### Upstash (Redis/Kafka)
**CLI:** `upstash`

**What Claude automates:**
- Create Redis database: `upstash redis create {name} --region {region}`
- Get connection details: `upstash redis get {id}`
- Create Kafka cluster: `upstash kafka create {name} --region {region}`

**Never ask human to:**
- Visit console.upstash.com
- Click through UI to create database
- Copy/paste connection URLs manually

**Checkpoint pattern:**
```xml
<task type="auto">
  <name>Create Upstash Redis database</name>
  <action>Run `upstash redis create myapp-cache --region us-east-1`. Save URL to .env.</action>
  <verify>.env contains UPSTASH_REDIS_URL, upstash redis list shows database</verify>
</task>
```

### PlanetScale
**CLI:** `pscale`

**What Claude automates:**
- Create database: `pscale database create {name} --region {region}`
- Create branch: `pscale branch create {db} {branch}`
- Deploy request: `pscale deploy-request create {db} {branch}`
- Connection string: `pscale connect {db} {branch}`

## Version Control & CI/CD

### GitHub
**CLI:** `gh`

**What Claude automates:**
- Create repo: `gh repo create {name} --public/--private`
- Create issues: `gh issue create --title "{title}" --body "{body}"`
- Create PR: `gh pr create --title "{title}" --body "{body}"`
- Manage secrets: `gh secret set {KEY}`
- Trigger workflows: `gh workflow run {name}`
- Check status: `gh run list`

**Never ask human to:**
- Visit github.com to create repo
- Click through UI to add secrets
- Manually create issues/PRs

## Build Tools & Testing

### Node/npm/pnpm/bun
**What Claude automates:**
- Install dependencies: `npm install`, `pnpm install`, `bun install`
- Run builds: `npm run build`
- Run tests: `npm test`, `npm run test:e2e`
- Type checking: `tsc --noEmit`

**Never ask human to:** Run these commands manually

### Xcode (macOS/iOS)
**CLI:** `xcodebuild`

**What Claude automates:**
- Build project: `xcodebuild -project App.xcodeproj -scheme App build`
- Run tests: `xcodebuild test -project App.xcodeproj -scheme App`
- Archive: `xcodebuild archive -project App.xcodeproj -scheme App`
- Check compilation: Parse xcodebuild output for errors

**Never ask human to:**
- Open Xcode and click Product > Build
- Click Product > Test manually
- Check for errors by looking at Xcode UI

**Checkpoint pattern:**
```xml
<task type="auto">
  <name>Build macOS app</name>
  <action>Run `xcodebuild -project App.xcodeproj -scheme App build`. Check output for errors.</action>
  <verify>Build succeeds with "BUILD SUCCEEDED" in output</verify>
</task>

<task type="checkpoint:human-verify">
  <what-built>Built macOS app at DerivedData/Build/Products/Debug/App.app</what-built>
  <how-to-verify>Open App.app and check: login flow works, no visual glitches</how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

## Environment Configuration

### .env Files
**Tool:** Write tool

**What Claude automates:**
- Create .env files: Use Write tool
- Append variables: Use Edit tool
- Read current values: Use Read tool

**Never ask human to:**
- Manually create .env file
- Copy/paste values into .env
- Edit .env in text editor

**Pattern:**
```xml
<task type="auto">
  <name>Configure environment variables</name>
  <action>Write .env file with: DATABASE_URL, STRIPE_KEY, JWT_SECRET (generated).</action>
  <verify>Read .env confirms all variables present</verify>
</task>
```

## Email & Communication

### Resend
**API:** Resend API via HTTP

**What Claude automates:**
- Create API keys via dashboard API (if available) or instructions for one-time setup
- Send emails: Resend API
- Configure domains: Resend API

### SendGrid
**API:** SendGrid API via HTTP

**What Claude automates:**
- Create API keys via API
- Send emails: SendGrid API
- Configure webhooks: SendGrid API

**Note:** Initial account setup may require email verification (checkpoint:human-action), but all subsequent work is API-automated.

## Authentication Gates

**Critical distinction:** When Claude tries to use a CLI/API and gets an authentication error, this is NOT a failure - it's a gate that requires human input to unblock automation.

**Pattern: Claude encounters auth error → creates checkpoint → you authenticate → Claude continues**

### Example: Vercel CLI Not Authenticated

```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <files>.vercel/, vercel.json</files>
  <action>Run `vercel --yes` to deploy</action>
  <verify>vercel ls shows deployment</verify>
</task>

<!-- If vercel returns "Error: Not authenticated" -->

<task type="checkpoint:human-action" gate="blocking">
  <action>Authenticate Vercel CLI so I can continue deployment</action>
  <instructions>
    I tried to deploy but got authentication error.
    Run: vercel login
    This will open your browser - complete the authentication flow.
  </instructions>
  <verification>vercel whoami returns your account email</verification>
  <resume-signal>Type "done" when authenticated</resume-signal>
</task>

<!-- After authentication, Claude retries automatically -->

<task type="auto">
  <name>Retry Vercel deployment</name>
  <action>Run `vercel --yes` (now authenticated)</action>
  <verify>vercel ls shows deployment, curl returns 200</verify>
</task>
```

### Example: Stripe CLI Needs API Key

```xml
<task type="auto">
  <name>Create Stripe webhook endpoint</name>
  <action>Use Stripe API to create webhook at /api/webhooks</action>
</task>

<!-- If API returns 401 Unauthorized -->

<task type="checkpoint:human-action" gate="blocking">
  <action>Provide Stripe API key so I can continue webhook configuration</action>
  <instructions>
    I need your Stripe API key to create webhooks.
    1. Visit dashboard.stripe.com/apikeys
    2. Copy your "Secret key" (starts with sk_test_ or sk_live_)
    3. Paste it here or run: export STRIPE_SECRET_KEY=sk_...
  </instructions>
  <verification>Stripe API key works: curl test succeeds</verification>
  <resume-signal>Type "done" or paste the key</resume-signal>
</task>

<!-- After key provided, Claude writes to .env and continues -->

<task type="auto">
  <name>Save Stripe key and create webhook</name>
  <action>
    1. Write STRIPE_SECRET_KEY to .env
    2. Create webhook endpoint via Stripe API
    3. Save webhook secret to .env
  </action>
  <verify>.env contains both keys, webhook endpoint exists</verify>
</task>
```

### Example: GitHub CLI Not Logged In

```xml
<task type="auto">
  <name>Create GitHub repository</name>
  <action>Run `gh repo create myapp --public`</action>
</task>

<!-- If gh returns "Not logged in" -->

<task type="checkpoint:human-action" gate="blocking">
  <action>Authenticate GitHub CLI so I can create repository</action>
  <instructions>
    I need GitHub authentication to create the repo.
    Run: gh auth login
    Follow the prompts to authenticate (browser or token).
  </instructions>
  <verification>gh auth status shows "Logged in"</verification>
  <resume-signal>Type "done" when authenticated</resume-signal>
</task>

<task type="auto">
  <name>Create repository (authenticated)</name>
  <action>Run `gh repo create myapp --public`</action>
  <verify>gh repo view shows repository exists</verify>
</task>
```

### Example: Upstash CLI Needs API Key

```xml
<task type="auto">
  <name>Create Upstash Redis database</name>
  <action>Run `upstash redis create myapp-cache --region us-east-1`</action>
</task>

<!-- If upstash returns auth error -->

<task type="checkpoint:human-action" gate="blocking">
  <action>Configure Upstash CLI credentials so I can create database</action>
  <instructions>
    I need Upstash authentication to create Redis database.
    1. Visit console.upstash.com/account/api
    2. Copy your API key
    3. Run: upstash auth login
    4. Paste your API key when prompted
  </instructions>
  <verification>upstash auth status shows authenticated</verification>
  <resume-signal>Type "done" when authenticated</resume-signal>
</task>

<task type="auto">
  <name>Create Redis database (authenticated)</name>
  <action>
    1. Run `upstash redis create myapp-cache --region us-east-1`
    2. Capture connection URL
    3. Write to .env: UPSTASH_REDIS_URL={url}
  </action>
  <verify>upstash redis list shows database, .env contains URL</verify>
</task>
```

### Authentication Gate Protocol

**When Claude encounters authentication error during execution:**

1. **Recognize it's not a failure** - Missing auth is expected, not a bug
2. **Stop current task** - Don't retry repeatedly
3. **Create checkpoint:human-action on the fly** - Dynamic checkpoint, not pre-planned
4. **Provide exact authentication steps** - CLI commands, where to get keys
5. **Verify authentication** - Test that auth works before continuing
6. **Retry the original task** - Resume automation where it left off
7. **Continue normally** - One auth gate doesn't break the flow

**Key difference from pre-planned checkpoints:**
- Pre-planned: "I need you to do X" (wrong - Claude should automate)
- Auth gate: "I tried to automate X but need credentials to continue" (correct - unblocks automation)

**This preserves agentic flow:**
- Claude tries automation first
- Only asks for help when blocked by credentials
- Continues automating after unblocked
- You never manually deploy/create resources - just provide keys

## When checkpoint:human-action is REQUIRED

**Truly rare cases where no CLI/API exists:**

1. **Email verification links** - Account signup requires clicking verification email
2. **SMS verification codes** - 2FA requiring phone
3. **Manual account approvals** - Platform requires human review before API access
4. **Domain DNS records at registrar** - Some registrars have no API
5. **Credit card input** - Payment methods requiring 3D Secure web flow
6. **OAuth app approval** - Some platforms require web-based app approval flow

**For these rare cases:**
```xml
<task type="checkpoint:human-action" gate="blocking">
  <action>Complete email verification for SendGrid account</action>
  <instructions>
    I created the account and requested verification email.
    Check your inbox for verification link and click it.
  </instructions>
  <verification>SendGrid API key works: curl test succeeds</verification>
  <resume-signal>Type "done" when verified</resume-signal>
</task>
```

**Key difference:** Claude does EVERYTHING possible first (account creation, API requests), only asks human for the one thing with no automation path.

## Quick Reference: "Can Claude automate this?"

| Action | CLI/API? | Claude does it? |
|--------|----------|-----------------|
| Deploy to Vercel | ✅ `vercel` | YES |
| Create Stripe webhook | ✅ Stripe API | YES |
| Run xcodebuild | ✅ `xcodebuild` | YES |
| Write .env file | ✅ Write tool | YES |
| Create Upstash DB | ✅ `upstash` CLI | YES |
| Install npm packages | ✅ `npm` | YES |
| Create GitHub repo | ✅ `gh` | YES |
| Run tests | ✅ `npm test` | YES |
| Create Supabase project | ⚠️ Web dashboard | NO (then CLI for everything else) |
| Click email verification link | ❌ No API | NO |
| Enter credit card with 3DS | ❌ No API | NO |

**Default answer: YES.** Unless explicitly in the "NO" category, Claude automates it.

## Decision Tree

```
┌─────────────────────────────────────┐
│ Task requires external resource?    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Does it have CLI/API/tool access?   │
└──────────────┬──────────────────────┘
               │
         ┌─────┴─────┐
         │           │
         ▼           ▼
       YES          NO
         │           │
         │           ▼
         │     ┌──────────────────────────────┐
         │     │ checkpoint:human-action      │
         │     │ (email links, 2FA, etc.)     │
         │     └──────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────────┐
    │ task type="auto"                       │
    │ Claude automates via CLI/API           │
    └────────────┬───────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────────┐
    │ checkpoint:human-verify                │
    │ Human confirms visual/functional       │
    └────────────────────────────────────────┘
```

## Summary

**The rule:** If Claude CAN do it, Claude MUST do it.

Checkpoints are for:
- **Verification** - Confirming Claude's automated work looks/behaves correctly
- **Decisions** - Choosing between valid approaches
- **True blockers** - Rare actions with literally no API/CLI (email links, 2FA)

Checkpoints are NOT for:
- Deploying (use CLI)
- Creating resources (use CLI/API)
- Running builds (use Bash)
- Writing files (use Write tool)
- Anything with automation available

**This keeps the agentic coding workflow intact - Claude does the work, you verify results.**

---

## Reference: Context Management

<overview>
Claude has a finite context window. This reference defines how to monitor usage and handle approaching limits gracefully.
</overview>

<context_awareness>
Claude receives system warnings showing token usage:

```
Token usage: 150000/200000; 50000 remaining
```

This information appears in `<system_warning>` tags during the conversation.
</context_awareness>

<thresholds>
<threshold level="comfortable" remaining="50%+">
**Status**: Plenty of room
**Action**: Work normally
</threshold>

<threshold level="getting_full" remaining="25%">
**Status**: Context accumulating
**Action**: Mention to user: "Context getting full. Consider wrapping up or creating handoff soon."
**No immediate action required.**
</threshold>

<threshold level="low" remaining="15%">
**Status**: Running low
**Action**:
1. Pause at next safe point (complete current atomic operation)
2. Ask user: "Running low on context (~30k tokens remaining). Options:
   - Create handoff now and resume in fresh session
   - Push through (risky if complex work remains)"
3. Await user decision

**Do not start new large operations.**
</threshold>

<threshold level="critical" remaining="10%">
**Status**: Must stop
**Action**:
1. Complete current atomic task (don't leave broken state)
2. **Automatically create handoff** without asking
3. Tell user: "Context limit reached. Created handoff at [location]. Start fresh session to continue."
4. **Stop working** - do not start any new tasks

This is non-negotiable. Running out of context mid-task is worse than stopping early.
</threshold>
</thresholds>

<what_counts_as_atomic>
An atomic operation is one that shouldn't be interrupted:

**Atomic (finish before stopping)**:
- Writing a single file
- Running a validation command
- Completing a single task from the plan

**Not atomic (can pause between)**:
- Multiple tasks in sequence
- Multi-file changes (can pause between files)
- Research + implementation (can pause between)

When hitting 10% threshold, finish current atomic operation, then stop.
</what_counts_as_atomic>

<handoff_content_at_limit>
When auto-creating handoff at 10%, include:

```yaml
---
phase: [current phase]
task: [current task number]
total_tasks: [total]
status: context_limit_reached
last_updated: [timestamp]
---
```

Body must capture:
1. What was just completed
2. What task was in progress (and how far)
3. What remains
4. Any decisions/context from this session

Be thorough - the next session starts fresh.
</handoff_content_at_limit>

<preventing_context_bloat>
Strategies to extend context life:

**Don't re-read files unnecessarily**
- Read once, remember content
- Don't cat the same file multiple times

**Summarize rather than quote**
- "The schema has 5 models including User and Session"
- Not: [paste entire schema]

**Use targeted reads**
- Read specific functions, not entire files
- Use grep to find relevant sections

**Clear completed work from "memory"**
- Once a task is done, don't keep referencing it
- Move forward, don't re-explain

**Avoid verbose output**
- Concise responses
- Don't repeat user's question back
- Don't over-explain obvious things
</preventing_context_bloat>

<user_signals>
Watch for user signals that suggest context concern:

- "Let's wrap up"
- "Save my place"
- "I need to step away"
- "Pack it up"
- "Create a handoff"
- "Running low on context?"

Any of these → trigger handoff workflow immediately.
</user_signals>

<fresh_session_guidance>
When user returns in fresh session:

1. They invoke skill
2. Context scan finds handoff
3. Resume workflow activates
4. Load handoff, present summary
5. Delete handoff after confirmation
6. Continue from saved state

The fresh session has full context available again.
</fresh_session_guidance>

---

## Reference: Domain Expertise

# Domain Expertise Structure

Guide for creating domain expertise skills that work efficiently with create-plans.

## Purpose

Domain expertise provides context-specific knowledge (Swift/macOS patterns, Next.js conventions, Unity workflows) that makes plans more accurate and actionable.

**Critical:** Domain skills must be context-efficient. Loading 20k+ tokens of references defeats the purpose.

## File Structure

```
~/.claude/skills/expertise/[domain-name]/
├── SKILL.md              # Core principles + references_index (5-7k tokens)
├── references/           # Selective loading based on phase type
│   ├── always-useful.md  # Conventions, patterns used in all phases
│   ├── database.md       # Database-specific guidance
│   ├── ui-layout.md      # UI-specific guidance
│   ├── api-routes.md     # API-specific guidance
│   └── ...
└── workflows/            # Optional: domain-specific workflows
    └── ...
```

## SKILL.md Template

```markdown
---
name: [domain-name]
description: [What this expertise covers]
---

<principles>
## Core Principles

[Fundamental patterns that apply to ALL work in this domain]
[Should be complete enough to plan without loading references]

Examples:
- File organization patterns
- Naming conventions
- Architecture patterns
- Common gotchas to avoid
- Framework-specific requirements

**Keep this section comprehensive but concise (~3-5k tokens).**
</principles>

<references_index>
## Reference Loading Guide

When planning phases, load references based on phase type:

**For [phase-type-1] phases:**
- references/[file1].md - [What it contains]
- references/[file2].md - [What it contains]

**For [phase-type-2] phases:**
- references/[file3].md - [What it contains]
- references/[file4].md - [What it contains]

**Always useful (load for any phase):**
- references/conventions.md - [What it contains]
- references/common-patterns.md - [What it contains]

**Examples of phase type mapping:**
- Database/persistence phases → database.md, migrations.md
- UI/layout phases → ui-patterns.md, design-system.md
- API/backend phases → api-routes.md, auth.md
- Integration phases → system-apis.md, third-party.md
</references_index>

<workflows>
## Optional Workflows

[If domain has specific workflows, list them here]
[These are NOT auto-loaded - only used when specifically invoked]
</workflows>
```

## Reference File Guidelines

Each reference file should be:

**1. Focused** - Single concern (database patterns, UI layout, API design)

**2. Actionable** - Contains patterns Claude can directly apply
```markdown
# Database Patterns

## Table Naming
- Singular nouns (User, not Users)
- snake_case for SQL, PascalCase for models

## Common Patterns
- Soft deletes: deleted_at timestamp
- Audit columns: created_at, updated_at
- Foreign keys: [table]_id format
```

**3. Sized appropriately** - 500-2000 lines (~1-5k tokens)
   - Too small: Not worth separate file
   - Too large: Split into more focused files

**4. Self-contained** - Can be understood without reading other references

## Context Efficiency Examples

**Bad (old approach):**
```
Load all references: 10,728 lines = ~27k tokens
Result: 50% context before planning starts
```

**Good (new approach):**
```
Load SKILL.md: ~5k tokens
Planning UI phase → load ui-layout.md + conventions.md: ~7k tokens
Total: ~12k tokens (saves 15k for workspace)
```

## Phase Type Classification

Help create-plans determine which references to load:

**Common phase types:**
- **Foundation/Setup** - Project structure, dependencies, configuration
- **Database/Data** - Schema, models, migrations, queries
- **API/Backend** - Routes, controllers, business logic, auth
- **UI/Frontend** - Components, layouts, styling, interactions
- **Integration** - External APIs, system services, third-party SDKs
- **Features** - Domain-specific functionality
- **Polish** - Performance, accessibility, error handling

**References should map to these types** so create-plans can load the right context.

## Migration Guide

If you have an existing domain skill with many references:

1. **Audit references** - What's actually useful vs. reference dumps?

2. **Consolidate principles** - Move core patterns into SKILL.md principles section

3. **Create references_index** - Map phase types to relevant references

4. **Test loading** - Verify you can plan a phase with <15k token overhead

5. **Iterate** - Adjust groupings based on actual planning needs

## Example: macos-apps

**Before (inefficient):**
- 20 reference files
- Load all: 10,728 lines (~27k tokens)

**After (efficient):**

SKILL.md contains:
- Swift/SwiftUI core principles
- macOS app architecture patterns
- Common patterns (MV VM, data flow)
- references_index mapping:
  - UI phases → swiftui-layout.md, appleHIG.md (~4k)
  - Data phases → core-data.md, swift-concurrency.md (~5k)
  - System phases → appkit-integration.md, menu-bar.md (~3k)
  - Always → swift-conventions.md (~2k)

**Result:** 5-12k tokens instead of 27k (saves 15-22k for planning)

---

## Reference: Git Integration

# Git Integration Reference

## Core Principle

**Commit outcomes, not process.**

The git log should read like a changelog of what shipped, not a diary of planning activity.

## Commit Points (Only 3)

| Event | Commit? | Why |
|-------|---------|-----|
| BRIEF + ROADMAP created | YES | Project initialization |
| PLAN.md created | NO | Intermediate - commit with completion |
| RESEARCH.md created | NO | Intermediate |
| FINDINGS.md created | NO | Intermediate |
| **Phase completed** | YES | Actual code shipped |
| Handoff created | YES | WIP state preserved |

## Git Check on Invocation

```bash
git rev-parse --git-dir 2>/dev/null || echo "NO_GIT_REPO"
```

If NO_GIT_REPO:
- Inline: "No git repo found. Initialize one? (Recommended for version control)"
- If yes: `git init`

## Commit Message Formats

### 1. Project Initialization (brief + roadmap together)

```
docs: initialize [project-name] ([N] phases)

[One-liner from BRIEF.md]

Phases:
1. [phase-name]: [goal]
2. [phase-name]: [goal]
3. [phase-name]: [goal]
```

What to commit:
```bash
git add .planning/
git commit
```

### 2. Phase Completion

```
feat([domain]): [one-liner from SUMMARY.md]

- [Key accomplishment 1]
- [Key accomplishment 2]
- [Key accomplishment 3]

[If issues encountered:]
Note: [issue and resolution]
```

Use `fix([domain])` for bug fix phases.

What to commit:
```bash
git add .planning/phases/XX-name/  # PLAN.md + SUMMARY.md
git add src/                        # Actual code created
git commit
```

### 3. Handoff (WIP)

```
wip: [phase-name] paused at task [X]/[Y]

Current: [task name]
[If blocked:] Blocked: [reason]
```

What to commit:
```bash
git add .planning/
git commit
```

## Example Clean Git Log

```
a]7f2d1 feat(checkout): Stripe payments with webhook verification
b]3e9c4 feat(products): catalog with search, filters, and pagination
c]8a1b2 feat(auth): JWT with refresh rotation using jose
d]5c3d7 feat(foundation): Next.js 15 + Prisma + Tailwind scaffold
e]2f4a8 docs: initialize ecommerce-app (5 phases)
```

## What NOT To Commit Separately

- PLAN.md creation (wait for phase completion)
- RESEARCH.md (intermediate)
- FINDINGS.md (intermediate)
- Minor planning tweaks
- "Fixed typo in roadmap"

These create noise. Commit outcomes, not process.

---

## Reference: Hierarchy Rules

<overview>
The planning hierarchy ensures context flows down and progress flows up.
Each level builds on the previous and enables the next.
</overview>

<hierarchy>
```
BRIEF.md          ← Vision (human-focused)
    ↓
ROADMAP.md        ← Structure (phases)
    ↓
phases/XX/PLAN.md ← Implementation (Claude-executable)
    ↓
prompts/          ← Execution (via create-meta-prompts)
```
</hierarchy>

<level name="brief">
**Purpose**: Capture vision, goals, constraints
**Audience**: Human (the user)
**Contains**: What we're building, why, success criteria, out of scope
**Creates**: `.planning/BRIEF.md`

**Requires**: Nothing (can start here)
**Enables**: Roadmap creation

This is the ONLY document optimized for human reading.
</level>

<level name="roadmap">
**Purpose**: Define phases and sequence
**Audience**: Both human and Claude
**Contains**: Phase names, goals, dependencies, progress tracking
**Creates**: `.planning/ROADMAP.md`, `.planning/phases/` directories

**Requires**: Brief (or quick context if skipping)
**Enables**: Phase planning

Roadmap looks UP to Brief for scope, looks DOWN to track phase completion.
</level>

<level name="phase_plan">
**Purpose**: Define Claude-executable tasks
**Audience**: Claude (the implementer)
**Contains**: Tasks with Files/Action/Verification/Done-when
**Creates**: `.planning/phases/XX-name/PLAN.md`

**Requires**: Roadmap (to know phase scope)
**Enables**: Prompt generation, direct execution

Phase plan looks UP to Roadmap for scope, produces implementation details.
</level>

<level name="prompts">
**Purpose**: Optimized execution instructions
**Audience**: Claude (via create-meta-prompts)
**Contains**: Research/Plan/Do prompts with metadata
**Creates**: `.planning/phases/XX-name/prompts/`

**Requires**: Phase plan (tasks to execute)
**Enables**: Autonomous execution

Prompts are generated from phase plan via create-meta-prompts skill.
</level>

<navigation_rules>
<looking_up>
When creating a lower-level artifact, ALWAYS read higher levels for context:

- Creating Roadmap → Read Brief
- Planning Phase → Read Roadmap AND Brief
- Generating Prompts → Read Phase Plan AND Roadmap

This ensures alignment with overall vision.
</looking_up>

<looking_down>
When updating a higher-level artifact, check lower levels for status:

- Updating Roadmap progress → Check which phase PLANs exist, completion state
- Reviewing Brief → See how far we've come via Roadmap

This enables progress tracking.
</looking_down>

<missing_prerequisites>
If a prerequisite doesn't exist:

```
Creating phase plan but no roadmap exists.

Options:
1. Create roadmap first (recommended)
2. Create quick roadmap placeholder
3. Proceed anyway (not recommended - loses hierarchy benefits)
```

Always offer to create missing pieces rather than skipping.
</missing_prerequisites>
</navigation_rules>

<file_locations>
All planning artifacts in `.planning/`:

```
.planning/
├── BRIEF.md                    # One per project
├── ROADMAP.md                  # One per project
└── phases/
    ├── 01-phase-name/
    │   ├── PLAN.md             # One per phase
    │   ├── .continue-here.md   # Temporary (when paused)
    │   └── prompts/            # Generated execution prompts
    ├── 02-phase-name/
    │   ├── PLAN.md
    │   └── prompts/
    └── ...
```

Phase directories use `XX-kebab-case` for consistent ordering.
</file_locations>

<scope_inheritance>
Each level inherits and narrows scope:

**Brief**: "Build a task management app"
**Roadmap**: "Phase 1: Core task CRUD, Phase 2: Projects, Phase 3: Collaboration"
**Phase 1 Plan**: "Task 1: Database schema, Task 2: API endpoints, Task 3: UI"

Scope flows DOWN and gets more specific.
Progress flows UP and gets aggregated.
</scope_inheritance>

<cross_phase_context>
When planning Phase N, Claude should understand:

- What Phase N-1 delivered (completed work)
- What Phase N should build on (foundations)
- What Phase N+1 will need (don't paint into corner)

Read previous phase's PLAN.md to understand current state.
</cross_phase_context>

---

## Reference: Milestone Management

# Milestone Management & Greenfield/Brownfield Planning

Milestones mark shipped versions. They solve the "what happens after v1.0?" problem.

## The Core Problem

**After shipping v1.0:**
- Planning artifacts optimized for greenfield (starting from scratch)
- But now you have: existing code, users, constraints, shipped features
- Need brownfield awareness without losing planning structure

**Solution:** Milestone-bounded extensions with updated BRIEF.

## Three Planning Modes

### 1. Greenfield (v1.0 Initial Development)

**Characteristics:**
- No existing code
- No users
- No constraints from shipped versions
- Pure "build from scratch" mode

**Planning structure:**
```
.planning/
├── BRIEF.md              # Original vision
├── ROADMAP.md            # Phases 1-4
└── phases/
    ├── 01-foundation/
    ├── 02-features/
    ├── 03-polish/
    └── 04-launch/
```

**BRIEF.md looks like:**
```markdown
# Project Brief: AppName

**Vision:** Build a thing that does X

**Purpose:** Solve problem Y

**Scope:**
- Feature A
- Feature B
- Feature C

**Success:** Ships and works
```

**Workflow:** Normal planning → execution → transition flow

---

### 2. Brownfield Extensions (v1.1, v1.2 - Same Codebase)

**Characteristics:**
- v1.0 shipped and in use
- Adding features / fixing issues
- Same codebase, continuous evolution
- Existing code referenced in new plans

**Planning structure:**
```
.planning/
├── BRIEF.md              # Updated with "Current State"
├── ROADMAP.md            # Phases 1-6 (grouped by milestone)
├── MILESTONES.md         # v1.0 entry
└── phases/
    ├── 01-foundation/    # ✓ v1.0
    ├── 02-features/      # ✓ v1.0
    ├── 03-polish/        # ✓ v1.0
    ├── 04-launch/        # ✓ v1.0
    ├── 05-security/      # 🚧 v1.1 (in progress)
    └── 06-performance/   # 📋 v1.1 (planned)
```

**BRIEF.md updated:**
```markdown
# Project Brief: AppName

## Current State (Updated: 2025-12-01)

**Shipped:** v1.0 MVP (2025-11-25)
**Users:** 500 downloads, 50 daily actives
**Feedback:** Requesting dark mode, occasional crashes on network errors
**Codebase:** 2,450 lines Swift, macOS 13.0+, AppKit

## v1.1 Goals

**Vision:** Harden reliability and add dark mode based on user feedback

**Motivation:**
- 5 crash reports related to network errors
- 15 users requested dark mode
- Want to improve before marketing push

**Scope (v1.1):**
- Comprehensive error handling
- Dark mode support
- Crash reporting integration

---

<details>
<summary>Original Vision (v1.0 - Archived)</summary>

[Original brief content]

</details>
```

**ROADMAP.md updated:**
```markdown
# Roadmap: AppName

## Milestones

- ✅ **v1.0 MVP** - Phases 1-4 (shipped 2025-11-25)
- 🚧 **v1.1 Hardening** - Phases 5-6 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) - SHIPPED 2025-11-25</summary>

- [x] Phase 1: Foundation
- [x] Phase 2: Core Features
- [x] Phase 3: Polish
- [x] Phase 4: Launch

</details>

### 🚧 v1.1 Hardening (In Progress)

- [ ] Phase 5: Error Handling & Stability
- [ ] Phase 6: Dark Mode UI
```

**How plans become brownfield-aware:**

When planning Phase 5, the PLAN.md automatically gets context:

```markdown
<context>
@.planning/BRIEF.md                      # Knows: v1.0 shipped, codebase exists
@.planning/MILESTONES.md                 # Knows: what v1.0 delivered
@AppName/NetworkManager.swift            # Existing code to improve
@AppName/APIClient.swift                 # Existing code to fix
</context>

<tasks>
<task type="auto">
  <name>Add comprehensive error handling to NetworkManager</name>
  <files>AppName/NetworkManager.swift</files>
  <action>Existing NetworkManager has basic try/catch. Add: retry logic (3 attempts with exponential backoff), specific error types (NetworkError enum), user-friendly error messages. Maintain existing public API - internal improvements only.</action>
  <verify>Build succeeds, existing tests pass, new error tests pass</verify>
  <done>All network calls have retry logic, error messages are user-friendly</done>
</task>
```

**Key difference from greenfield:**
- PLAN references existing files in `<context>`
- Tasks say "update existing X" not "create X"
- Verify includes "existing tests pass" (regression check)
- Checkpoints may verify existing behavior still works

---

### 3. Major Iterations (v2.0+ - Still Same Codebase)

**Characteristics:**
- Large rewrites within same codebase
- 8-15+ phases planned
- Breaking changes, new architecture
- Still continuous from v1.x

**Planning structure:**
```
.planning/
├── BRIEF.md              # Updated for v2.0 vision
├── ROADMAP.md            # Phases 1-14 (grouped)
├── MILESTONES.md         # v1.0, v1.1 entries
└── phases/
    ├── 01-foundation/    # ✓ v1.0
    ├── 02-features/      # ✓ v1.0
    ├── 03-polish/        # ✓ v1.0
    ├── 04-launch/        # ✓ v1.0
    ├── 05-security/      # ✓ v1.1
    ├── 06-performance/   # ✓ v1.1
    ├── 07-swiftui-core/  # 🚧 v2.0 (in progress)
    ├── 08-swiftui-views/ # 📋 v2.0 (planned)
    ├── 09-new-arch/      # 📋 v2.0
    └── ...               # Up to 14
```

**ROADMAP.md:**
```markdown
## Milestones

- ✅ **v1.0 MVP** - Phases 1-4 (shipped 2025-11-25)
- ✅ **v1.1 Hardening** - Phases 5-6 (shipped 2025-12-10)
- 🚧 **v2.0 SwiftUI Redesign** - Phases 7-14 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4)</summary>
[Collapsed]
</details>

<details>
<summary>✅ v1.1 Hardening (Phases 5-6)</summary>
[Collapsed]
</details>

### 🚧 v2.0 SwiftUI Redesign (In Progress)

- [ ] Phase 7: SwiftUI Core Migration
- [ ] Phase 8: SwiftUI Views
- [ ] Phase 9: New Architecture
- [ ] Phase 10: Widget Support
- [ ] Phase 11: iOS Companion
- [ ] Phase 12: Performance
- [ ] Phase 13: Testing
- [ ] Phase 14: Launch
```

**Same rules apply:** Continuous phase numbering, milestone groupings, brownfield-aware plans.

---

## When to Archive and Start Fresh

**Archive ONLY for these scenarios:**

### Scenario 1: Separate Codebase

**Example:**
- Built: WeatherBar (macOS app) ✓ shipped
- Now building: WeatherBar-iOS (separate Xcode project, different repo or workspace)

**Action:**
```
.planning/
├── archive/
│   └── v1-macos/
│       ├── BRIEF.md
│       ├── ROADMAP.md
│       ├── MILESTONES.md
│       └── phases/
├── BRIEF.md              # Fresh: iOS app
├── ROADMAP.md            # Fresh: starts at phase 01
└── phases/
    └── 01-ios-foundation/
```

**Why:** Different codebase = different planning context. Old planning doesn't help with iOS-specific decisions.

### Scenario 2: Complete Rewrite (Different Repo)

**Example:**
- Built: AppName v1 (AppKit, shipped) ✓
- Now building: AppName v2 (complete SwiftUI rewrite, new git repo)

**Action:** Same as Scenario 1 - archive v1, fresh planning for v2

**Why:** New repo, starting from scratch, v1 planning doesn't transfer.

### Scenario 3: Different Product

**Example:**
- Built: WeatherBar (weather app) ✓
- Now building: TaskBar (task management app)

**Action:** New project entirely, new `.planning/` directory

**Why:** Completely different product, no relationship.

---

## Decision Tree

```
Starting new work?
│
├─ Same codebase/repo?
│  │
│  ├─ YES → Extend existing roadmap
│  │        ├─ Add phases 5-6+ to ROADMAP
│  │        ├─ Update BRIEF "Current State"
│  │        ├─ Plans reference existing code in @context
│  │        └─ Continue normal workflow
│  │
│  └─ NO → Is it a separate platform/codebase for same product?
│           │
│           ├─ YES (e.g., iOS version of Mac app)
│           │    └─ Archive existing planning
│           │         └─ Start fresh with new BRIEF/ROADMAP
│           │              └─ Reference original in "Context" section
│           │
│           └─ NO (completely different product)
│                └─ New project, new planning directory
│
└─ Is this v1.0 initial delivery?
   └─ YES → Greenfield mode
            └─ Just follow normal workflow
```

---

## Milestone Workflow Triggers

### When completing v1.0 (first ship):

**User:** "I'm ready to ship v1.0"

**Action:**
1. Verify phases 1-4 complete (all summaries exist)
2. `/milestone:complete "v1.0 MVP"`
3. Creates MILESTONES.md entry
4. Updates BRIEF with "Current State"
5. Reorganizes ROADMAP with milestone grouping
6. Git tag v1.0
7. Commit milestone changes

**Result:** Historical record created, ready for v1.1 work

### When adding v1.1 work:

**User:** "Add dark mode and notifications"

**Action:**
1. Check BRIEF "Current State" - sees v1.0 shipped
2. Ask: "Add phases 5-6 to existing roadmap? (yes / archive and start fresh)"
3. User: "yes"
4. Update BRIEF with v1.1 goals
5. Add Phase 5-6 to ROADMAP under "v1.1" milestone heading
6. Continue normal planning workflow

**Result:** Phases 5-6 added, brownfield-aware through updated BRIEF

### When completing v1.1:

**User:** "Ship v1.1"

**Action:**
1. Verify phases 5-6 complete
2. `/milestone:complete "v1.1 Security"`
3. Add v1.1 entry to MILESTONES.md (prepended, newest first)
4. Update BRIEF current state to v1.1
5. Collapse phases 5-6 in ROADMAP
6. Git tag v1.1

**Result:** v1.0 and v1.1 both in MILESTONES.md, ROADMAP shows history

---

## Brownfield Plan Patterns

**How a brownfield plan differs from greenfield:**

### Greenfield Plan (v1.0):
```markdown
<objective>
Create authentication system from scratch.
</objective>

<context>
@.planning/BRIEF.md
@.planning/ROADMAP.md
</context>

<tasks>
<task type="auto">
  <name>Create User model</name>
  <files>src/models/User.ts</files>
  <action>Create User interface with id, email, passwordHash, createdAt fields. Export from models/index.</action>
  <verify>TypeScript compiles, User type exported</verify>
  <done>User model exists and is importable</done>
</task>
```

### Brownfield Plan (v1.1):
```markdown
<objective>
Add MFA to existing authentication system.
</objective>

<context>
@.planning/BRIEF.md              # Shows v1.0 shipped, auth exists
@.planning/MILESTONES.md         # Shows what v1.0 delivered
@src/models/User.ts              # Existing User model
@src/auth/AuthService.ts         # Existing auth logic
</context>

<tasks>
<task type="auto">
  <name>Add MFA fields to User model</name>
  <files>src/models/User.ts</files>
  <action>Add to existing User interface: mfaEnabled (boolean), mfaSecret (string | null), mfaBackupCodes (string[]). Maintain backward compatibility - all new fields optional or have defaults.</action>
  <verify>TypeScript compiles, existing User usages still work</verify>
  <done>User model has MFA fields, no breaking changes</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>MFA enrollment flow</what-built>
  <how-to-verify>
    1. Run: npm run dev
    2. Login as existing user (test@example.com)
    3. Navigate to Settings → Security
    4. Click "Enable MFA" - should show QR code
    5. Scan with authenticator app (Google Authenticator)
    6. Enter code - should enable successfully
    7. Logout, login again - should prompt for MFA code
    8. Verify: existing users without MFA can still login (backward compat)
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

**Key differences:**
1. **@context** includes existing code files
2. **Actions** say "add to existing" / "update existing" / "maintain backward compat"
3. **Verification** includes regression checks ("existing X still works")
4. **Checkpoints** may verify existing user flows still work

---

## BRIEF Current State Section

The "Current State" section in BRIEF.md is what makes plans brownfield-aware.

**After v1.0 ships:**

```markdown
## Current State (Updated: 2025-11-25)

**Shipped:** v1.0 MVP (2025-11-25)
**Status:** Production
**Users:** 500 downloads, 50 daily actives, growing 10% weekly
**Feedback:**
- "Love the simplicity" (common theme)
- 15 requests for dark mode
- 5 crash reports on network errors
- 3 requests for multiple accounts

**Codebase:**
- 2,450 lines of Swift
- macOS 13.0+ (AppKit)
- OpenWeather API integration
- Auto-refresh every 30 min
- Signed and notarized

**Known Issues:**
- Network errors crash app (no retry logic)
- Memory leak in auto-refresh timer
- No dark mode support
```

When planning Phase 5 (v1.1), Claude reads this and knows:
- Code exists (2,450 lines Swift)
- Users exist (500 downloads)
- Feedback exists (15 want dark mode)
- Issues exist (network crashes, memory leak)

Plans automatically become brownfield-aware because BRIEF says "this is what we have."

---

## Summary

**Greenfield (v1.0):**
- Fresh BRIEF with vision
- Phases 1-4 (or however many)
- Plans create from scratch
- Ship → complete milestone

**Brownfield (v1.1+):**
- Update BRIEF "Current State"
- Add phases 5-6+ to ROADMAP
- Plans reference existing code
- Plans include regression checks
- Ship → complete milestone

**Archive (rare):**
- Only for separate codebases or different products
- Move `.planning/` to `.planning/archive/v1-name/`
- Start fresh with new BRIEF/ROADMAP
- New planning references old in context

**Key insight:** Same roadmap, continuous phase numbering (01-99), milestone groupings keep it organized. BRIEF "Current State" makes everything brownfield-aware automatically.

This scales from "hello world" to 100 shipped versions.

---

## Reference: Plan Format

<overview>
Claude-executable plans have a specific format that enables Claude to implement without interpretation. This reference defines what makes a plan executable vs. vague.

**Key insight:** PLAN.md IS the executable prompt. It contains everything Claude needs to execute the phase, including objective, context references, tasks, verification, success criteria, and output specification.
</overview>

<core_principle>
A plan is Claude-executable when Claude can read the PLAN.md and immediately start implementing without asking clarifying questions.

If Claude has to guess, interpret, or make assumptions - the task is too vague.
</core_principle>

<prompt_structure>
Every PLAN.md follows this XML structure:

```markdown
---
phase: XX-name
type: execute
domain: [optional]
---

<objective>
[What and why]
Purpose: [...]
Output: [...]
</objective>

<context>
@.planning/BRIEF.md
@.planning/ROADMAP.md
@relevant/source/files.ts
</context>

<tasks>
<task type="auto">
  <name>Task N: [Name]</name>
  <files>[paths]</files>
  <action>[what to do, what to avoid and WHY]</action>
  <verify>[command/check]</verify>
  <done>[criteria]</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>[what Claude automated]</what-built>
  <how-to-verify>[numbered verification steps]</how-to-verify>
  <resume-signal>[how to continue - "approved" or describe issues]</resume-signal>
</task>

<task type="checkpoint:decision" gate="blocking">
  <decision>[what needs deciding]</decision>
  <context>[why this matters]</context>
  <options>
    <option id="option-a"><name>[Name]</name><pros>[pros]</pros><cons>[cons]</cons></option>
    <option id="option-b"><name>[Name]</name><pros>[pros]</pros><cons>[cons]</cons></option>
  </options>
  <resume-signal>[how to indicate choice]</resume-signal>
</task>
</tasks>

<verification>
[Overall phase checks]
</verification>

<success_criteria>
[Measurable completion]
</success_criteria>

<output>
[SUMMARY.md specification]
</output>
```
</prompt_structure>

<task_anatomy>
Every task has four required fields:

<field name="files">
**What it is**: Exact file paths that will be created or modified.

**Good**: `src/app/api/auth/login/route.ts`, `prisma/schema.prisma`
**Bad**: "the auth files", "relevant components"

Be specific. If you don't know the file path, figure it out first.
</field>

<field name="action">
**What it is**: Specific implementation instructions, including what to avoid and WHY.

**Good**: "Create POST endpoint that accepts {email, password}, validates using bcrypt against User table, returns JWT in httpOnly cookie with 15-min expiry. Use jose library (not jsonwebtoken - CommonJS issues with Next.js Edge runtime)."

**Bad**: "Add authentication", "Make login work"

Include: technology choices, data structures, behavior details, pitfalls to avoid.
</field>

<field name="verify">
**What it is**: How to prove the task is complete.

**Good**:
- `npm test` passes
- `curl -X POST /api/auth/login` returns 200 with Set-Cookie header
- Build completes without errors

**Bad**: "It works", "Looks good", "User can log in"

Must be executable - a command, a test, an observable behavior.
</field>

<field name="done">
**What it is**: Acceptance criteria - the measurable state of completion.

**Good**: "Valid credentials return 200 + JWT cookie, invalid credentials return 401"

**Bad**: "Authentication is complete"

Should be testable without subjective judgment.
</field>
</task_anatomy>

<task_types>
Tasks have a `type` attribute that determines how they execute:

<type name="auto">
**Default task type** - Claude executes autonomously.

**Structure:**
```xml
<task type="auto">
  <name>Task 3: Create login endpoint with JWT</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>POST endpoint accepting {email, password}. Query User by email, compare password with bcrypt. On match, create JWT with jose library, set as httpOnly cookie (15-min expiry). Return 200. On mismatch, return 401.</action>
  <verify>curl -X POST localhost:3000/api/auth/login returns 200 with Set-Cookie header</verify>
  <done>Valid credentials → 200 + cookie. Invalid → 401.</done>
</task>
```

Use for: Everything Claude can do independently (code, tests, builds, file operations).
</type>

<type name="checkpoint:human-action">
**RARELY USED** - Only for actions with NO CLI/API. Claude automates everything possible first.

**Structure:**
```xml
<task type="checkpoint:human-action" gate="blocking">
  <action>[Unavoidable manual step - email link, 2FA code]</action>
  <instructions>
    [What Claude already automated]
    [The ONE thing requiring human action]
  </instructions>
  <verification>[What Claude can check afterward]</verification>
  <resume-signal>[How to continue]</resume-signal>
</task>
```

Use ONLY for: Email verification links, SMS 2FA codes, manual approvals with no API, 3D Secure payment flows.

Do NOT use for: Anything with a CLI (Vercel, Stripe, Upstash, Railway, GitHub), builds, tests, file creation, deployments.

See: references/cli-automation.md for what Claude can automate.

**Execution:** Claude automates everything with CLI/API, stops only for truly unavoidable manual steps.
</type>

<type name="checkpoint:human-verify">
**Human must verify Claude's work** - Visual checks, UX testing.

**Structure:**
```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Responsive dashboard layout</what-built>
  <how-to-verify>
    1. Run: npm run dev
    2. Visit: http://localhost:3000/dashboard
    3. Desktop (>1024px): Verify sidebar left, content right
    4. Tablet (768px): Verify sidebar collapses to hamburger
    5. Mobile (375px): Verify single column, bottom nav
    6. Check: No layout shift, no horizontal scroll
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

Use for: UI/UX verification, visual design checks, animation smoothness, accessibility testing.

**Execution:** Claude builds the feature, stops, provides testing instructions, waits for approval/feedback.
</type>

<type name="checkpoint:decision">
**Human must make implementation choice** - Direction-setting decisions.

**Structure:**
```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Select authentication provider</decision>
  <context>We need user authentication. Three approaches with different tradeoffs:</context>
  <options>
    <option id="supabase">
      <name>Supabase Auth</name>
      <pros>Built-in with Supabase, generous free tier</pros>
      <cons>Less customizable UI, tied to ecosystem</cons>
    </option>
    <option id="clerk">
      <name>Clerk</name>
      <pros>Beautiful pre-built UI, best DX</pros>
      <cons>Paid after 10k MAU</cons>
    </option>
    <option id="nextauth">
      <name>NextAuth.js</name>
      <pros>Free, self-hosted, maximum control</pros>
      <cons>More setup, you manage security</cons>
    </option>
  </options>
  <resume-signal>Select: supabase, clerk, or nextauth</resume-signal>
</task>
```

Use for: Technology selection, architecture decisions, design choices, feature prioritization.

**Execution:** Claude presents options with balanced pros/cons, waits for decision, proceeds with chosen direction.
</type>

**When to use checkpoints:**
- Visual/UX verification (after Claude builds) → `checkpoint:human-verify`
- Implementation direction choice → `checkpoint:decision`
- Truly unavoidable manual actions (email links, 2FA) → `checkpoint:human-action` (rare)

**When NOT to use checkpoints:**
- Anything with CLI/API (Claude automates it) → `type="auto"`
- Deployments (Vercel, Railway, Fly) → `type="auto"` with CLI
- Creating resources (Upstash, Stripe, GitHub) → `type="auto"` with CLI/API
- File operations, tests, builds → `type="auto"`

**Golden rule:** If Claude CAN automate it, Claude MUST automate it. See: references/cli-automation.md

See `references/checkpoints.md` for comprehensive checkpoint guidance.
</task_types>

<context_references>
Use @file references to load context for the prompt:

```markdown
<context>
@.planning/BRIEF.md           # Project vision
@.planning/ROADMAP.md         # Phase structure
@.planning/phases/02-auth/FINDINGS.md  # Research results
@src/lib/db.ts                # Existing database setup
@src/types/user.ts            # Existing type definitions
</context>
```

Reference files that Claude needs to understand before implementing.
</context_references>

<verification_section>
Overall phase verification (beyond individual task verification):

```markdown
<verification>
Before declaring phase complete:
- [ ] `npm run build` succeeds without errors
- [ ] `npm test` passes all tests
- [ ] No TypeScript errors
- [ ] Feature works end-to-end manually
</verification>
```
</verification_section>

<success_criteria_section>
Measurable criteria for phase completion:

```markdown
<success_criteria>
- All tasks completed
- All verification checks pass
- No errors or warnings introduced
- JWT auth flow works end-to-end
- Protected routes redirect unauthenticated users
</success_criteria>
```
</success_criteria_section>

<output_section>
Specify the SUMMARY.md structure:

```markdown
<output>
After completion, create `.planning/phases/XX-name/SUMMARY.md`:

# Phase X: Name Summary

**[Substantive one-liner]**

## Accomplishments
## Files Created/Modified
## Decisions Made
## Issues Encountered
## Next Phase Readiness
</output>
```
</output_section>

<specificity_levels>
<too_vague>
```xml
<task type="auto">
  <name>Task 1: Add authentication</name>
  <files>???</files>
  <action>Implement auth</action>
  <verify>???</verify>
  <done>Users can authenticate</done>
</task>
```

Claude: "How? What type? What library? Where?"
</too_vague>

<just_right>
```xml
<task type="auto">
  <name>Task 1: Create login endpoint with JWT</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>POST endpoint accepting {email, password}. Query User by email, compare password with bcrypt. On match, create JWT with jose library, set as httpOnly cookie (15-min expiry). Return 200. On mismatch, return 401. Use jose instead of jsonwebtoken (CommonJS issues with Edge).</action>
  <verify>curl -X POST localhost:3000/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"test123"}' returns 200 with Set-Cookie header containing JWT</verify>
  <done>Valid credentials → 200 + cookie. Invalid → 401. Missing fields → 400.</done>
</task>
```

Claude can implement this immediately.
</just_right>

<too_detailed>
Writing the actual code in the plan. Trust Claude to implement from clear instructions.
</too_detailed>
</specificity_levels>

<anti_patterns>
<vague_actions>
- "Set up the infrastructure"
- "Handle edge cases"
- "Make it production-ready"
- "Add proper error handling"

These require Claude to decide WHAT to do. Specify it.
</vague_actions>

<unverifiable_completion>
- "It works correctly"
- "User experience is good"
- "Code is clean"
- "Tests pass" (which tests? do they exist?)

These require subjective judgment. Make it objective.
</unverifiable_completion>

<missing_context>
- "Use the standard approach"
- "Follow best practices"
- "Like the other endpoints"

Claude doesn't know your standards. Be explicit.
</missing_context>
</anti_patterns>

<sizing_tasks>
Good task size: 15-60 minutes of Claude work.

**Too small**: "Add import statement for bcrypt" (combine with related task)
**Just right**: "Create login endpoint with JWT validation" (focused, specific)
**Too big**: "Implement full authentication system" (split into multiple plans)

If a task takes multiple sessions, break it down.
If a task is trivial, combine with related tasks.

**Note on scope:** If a phase has >7 tasks or spans multiple subsystems, split into multiple plans using the naming convention `{phase}-{plan}-PLAN.md`. See `references/scope-estimation.md` for guidance.
</sizing_tasks>

---

## Reference: Research Pitfalls

# Research Pitfalls - Known Patterns to Avoid

## Purpose
This document catalogs research mistakes discovered in production use, providing specific patterns to avoid and verification strategies to prevent recurrence.

## Known Pitfalls

### Pitfall 1: Configuration Scope Assumptions
**What**: Assuming global configuration means no project-scoping exists
**Example**: Concluding "MCP servers are configured GLOBALLY only" while missing project-scoped `.mcp.json`
**Why it happens**: Not explicitly checking all known configuration patterns
**Prevention**:
```xml
<verification_checklist>
**CRITICAL**: Verify ALL configuration scopes:
□ User/global scope - System-wide configuration
□ Project scope - Project-level configuration files
□ Local scope - Project-specific user overrides
□ Workspace scope - IDE/tool workspace settings
□ Environment scope - Environment variables
</verification_checklist>
```

### Pitfall 2: "Search for X" Vagueness
**What**: Asking researchers to "search for documentation" without specifying where
**Example**: "Research MCP documentation" → finds outdated community blog instead of official docs
**Why it happens**: Vague research instructions don't specify exact sources
**Prevention**:
```xml
<sources>
Official sources (use WebFetch):
- https://exact-url-to-official-docs
- https://exact-url-to-api-reference

Search queries (use WebSearch):
- "specific search query {current_year}"
- "another specific query {current_year}"
</sources>
```

### Pitfall 3: Deprecated vs Current Features
**What**: Finding archived/old documentation and concluding feature doesn't exist
**Example**: Finding 2022 docs saying "feature not supported" when current version added it
**Why it happens**: Not checking multiple sources or recent updates
**Prevention**:
```xml
<verification_checklist>
□ Check current official documentation
□ Review changelog/release notes for recent updates
□ Verify version numbers and publication dates
□ Cross-reference multiple authoritative sources
</verification_checklist>
```

### Pitfall 4: Tool-Specific Variations
**What**: Conflating capabilities across different tools/environments
**Example**: "Claude Desktop supports X" ≠ "Claude Code supports X"
**Why it happens**: Not explicitly checking each environment separately
**Prevention**:
```xml
<verification_checklist>
□ Claude Desktop capabilities
□ Claude Code capabilities
□ VS Code extension capabilities
□ API/SDK capabilities
Document which environment supports which features
</verification_checklist>
```

### Pitfall 5: Confident Negative Claims Without Citations
**What**: Making definitive "X is not possible" statements without official source verification
**Example**: "Folder-scoped MCP configuration is not supported" (missing `.mcp.json`)
**Why it happens**: Drawing conclusions from absence of evidence rather than evidence of absence
**Prevention**:
```xml
<critical_claims_audit>
For any "X is not possible" or "Y is the only way" statement:
- [ ] Is this verified by official documentation stating it explicitly?
- [ ] Have I checked for recent updates that might change this?
- [ ] Have I verified all possible approaches/mechanisms?
- [ ] Am I confusing "I didn't find it" with "it doesn't exist"?
</critical_claims_audit>
```

### Pitfall 6: Missing Enumeration
**What**: Investigating open-ended scope without enumerating known possibilities first
**Example**: "Research configuration options" instead of listing specific options to verify
**Why it happens**: Not creating explicit checklist of items to investigate
**Prevention**:
```xml
<verification_checklist>
Enumerate ALL known options FIRST:
□ Option 1: [specific item]
□ Option 2: [specific item]
□ Option 3: [specific item]
□ Check for additional unlisted options

For each option above, document:
- Existence (confirmed/not found/unclear)
- Official source URL
- Current status (active/deprecated/beta)
</verification_checklist>
```

### Pitfall 7: Single-Source Verification
**What**: Relying on a single source for critical claims
**Example**: Using only Stack Overflow answer from 2021 for current best practices
**Why it happens**: Not cross-referencing multiple authoritative sources
**Prevention**:
```xml
<source_verification>
For critical claims, require multiple sources:
- [ ] Official documentation (primary)
- [ ] Release notes/changelog (for currency)
- [ ] Additional authoritative source (for verification)
- [ ] Contradiction check (ensure sources agree)
</source_verification>
```

### Pitfall 8: Assumed Completeness
**What**: Assuming search results are complete and authoritative
**Example**: First Google result is outdated but assumed current
**Why it happens**: Not verifying publication dates and source authority
**Prevention**:
```xml
<source_verification>
For each source consulted:
- [ ] Publication/update date verified (prefer recent/current)
- [ ] Source authority confirmed (official docs, not blogs)
- [ ] Version relevance checked (matches current version)
- [ ] Multiple search queries tried (not just one)
</source_verification>
```

## Red Flags in Research Outputs

### 🚩 Red Flag 1: Zero "Not Found" Results
**Warning**: Every investigation succeeds perfectly
**Problem**: Real research encounters dead ends, ambiguity, and unknowns
**Action**: Expect honest reporting of limitations, contradictions, and gaps

### 🚩 Red Flag 2: No Confidence Indicators
**Warning**: All findings presented as equally certain
**Problem**: Can't distinguish verified facts from educated guesses
**Action**: Require confidence levels (High/Medium/Low) for key findings

### 🚩 Red Flag 3: Missing URLs
**Warning**: "According to documentation..." without specific URL
**Problem**: Can't verify claims or check for updates
**Action**: Require actual URLs for all official documentation claims

### 🚩 Red Flag 4: Definitive Statements Without Evidence
**Warning**: "X cannot do Y" or "Z is the only way" without citation
**Problem**: Strong claims require strong evidence
**Action**: Flag for verification against official sources

### 🚩 Red Flag 5: Incomplete Enumeration
**Warning**: Verification checklist lists 4 items, output covers 2
**Problem**: Systematic gaps in coverage
**Action**: Ensure all enumerated items addressed or marked "not found"

## Continuous Improvement

When research gaps occur:

1. **Document the gap**
   - What was missed or incorrect?
   - What was the actual correct information?
   - What was the impact?

2. **Root cause analysis**
   - Why wasn't it caught?
   - Which verification step would have prevented it?
   - What pattern does this reveal?

3. **Update this document**
   - Add new pitfall entry
   - Update relevant checklists
   - Share lesson learned

## Quick Reference Checklist

Before submitting research, verify:

- [ ] All enumerated items investigated (not just some)
- [ ] Negative claims verified with official docs
- [ ] Multiple sources cross-referenced for critical claims
- [ ] URLs provided for all official documentation
- [ ] Publication dates checked (prefer recent/current)
- [ ] Tool/environment-specific variations documented
- [ ] Confidence levels assigned honestly
- [ ] Assumptions distinguished from verified facts
- [ ] "What might I have missed?" review completed

---

**Living Document**: Update after each significant research gap
**Lessons From**: MCP configuration research gap (missed `.mcp.json`)

---

## Reference: Scope Estimation

# Scope Estimation & Quality-Driven Plan Splitting

Plans must maintain consistent quality from first task to last. This requires understanding the **quality degradation curve** and splitting aggressively to stay in the peak quality zone.

## The Quality Degradation Curve

**Critical insight:** Claude doesn't degrade at arbitrary percentages - it degrades when it *perceives* context pressure and enters "completion mode."

```
Context Usage  │  Quality Level   │  Claude's Mental State
─────────────────────────────────────────────────────────
0-30%          │  ████████ PEAK   │  "I can be thorough and comprehensive"
               │                  │  No anxiety, full detail, best work

30-50%         │  ██████ GOOD     │  "Still have room, maintaining quality"
               │                  │  Engaged, confident, solid work

50-70%         │  ███ DEGRADING   │  "Getting tight, need to be efficient"
               │                  │  Efficiency mode, compression begins

70%+           │  █ POOR          │  "Running out, must finish quickly"
               │                  │  Self-lobotomization, rushed, minimal
```

**The 40-50% inflection point:**

This is where quality breaks. Claude sees context mounting and thinks "I'd better conserve now or I won't finish." Result: The classic mid-execution statement "I'll complete the remaining tasks more concisely" = quality crash.

**The fundamental rule:** Stop BEFORE quality degrades, not at context limit.

## Target: 50% Context Maximum

**Plans should complete within ~50% of context usage.**

Why 50% not 80%?
- Huge safety buffer
- No context anxiety possible
- Quality maintained from start to finish
- Room for unexpected complexity
- Space for iteration and fixes

**If you target 80%, you're planning for failure.** By the time you hit 80%, you've already spent 40% in degradation mode.

## The 2-3 Task Rule

**Each plan should contain 2-3 tasks maximum.**

Why this number?

**Task 1 (0-15% context):**
- Fresh context
- Peak quality
- Comprehensive implementation
- Full testing
- Complete documentation

**Task 2 (15-35% context):**
- Still in peak zone
- Quality maintained
- Buffer feels safe
- No anxiety

**Task 3 (35-50% context):**
- Beginning to feel pressure
- Quality still good but managing it
- Natural stopping point
- Better to commit here

**Task 4+ (50%+ context):**
- DEGRADATION ZONE
- "I'll do this concisely" appears
- Quality crashes
- Should have split before this

**The principle:** Each task is independently committable. 2-3 focused changes per commit creates beautiful, surgical git history.

## Signals to Split Into Multiple Plans

### Always Split If:

**1. More than 3 tasks**
- Even if tasks seem small
- Each additional task increases degradation risk
- Split into logical groups of 2-3

**2. Multiple subsystems**
```
❌ Bad (1 plan):
- Database schema (3 files)
- API routes (5 files)
- UI components (8 files)
Total: 16 files, 1 plan → guaranteed degradation

✅ Good (3 plans):
- 01-01-PLAN.md: Database schema (3 files, 2 tasks)
- 01-02-PLAN.md: API routes (5 files, 3 tasks)
- 01-03-PLAN.md: UI components (8 files, 3 tasks)
Total: 16 files, 3 plans → consistent quality
```

**3. Any task with >5 file modifications**
- Large tasks burn context fast
- Split by file groups or logical units
- Better: 3 plans of 2 files each vs 1 plan of 6 files

**4. Checkpoint + implementation work**
- Checkpoints require user interaction (context preserved)
- Implementation after checkpoint should be separate plan
```
✅ Good split:
- 02-01-PLAN.md: Setup (checkpoint: decision on auth provider)
- 02-02-PLAN.md: Implement chosen auth solution
```

**5. Research + implementation**
- Research produces FINDINGS.md (separate plan)
- Implementation consumes FINDINGS.md (separate plan)
- Clear boundary, clean handoff

### Consider Splitting If:

**1. Estimated >5 files modified total**
- Context from reading existing code
- Context from diffs
- Context from responses
- Adds up faster than expected

**2. Complex domains (auth, payments, data modeling)**
- These require careful thinking
- Burns more context per task than simple CRUD
- Split more aggressively

**3. Any uncertainty about approach**
- "Figure out X" phase separate from "implement X" phase
- Don't mix exploration and implementation

**4. Natural semantic boundaries**
- Setup → Core → Features
- Backend → Frontend
- Configuration → Implementation → Testing

## Splitting Strategies

### By Subsystem

**Phase:** "Authentication System"

**Split:**
```
- 03-01-PLAN.md: Database models (User, Session tables + relations)
- 03-02-PLAN.md: Auth API (register, login, logout endpoints)
- 03-03-PLAN.md: Protected routes (middleware, JWT validation)
- 03-04-PLAN.md: UI components (login form, registration form)
```

Each plan: 2-3 tasks, single subsystem, clean commits.

### By Dependency

**Phase:** "Payment Integration"

**Split:**
```
- 04-01-PLAN.md: Stripe setup (webhook endpoints via API, env vars, test mode)
- 04-02-PLAN.md: Subscription logic (plans, checkout, customer portal)
- 04-03-PLAN.md: Frontend integration (pricing page, payment flow)
```

Later plans depend on earlier completion. Sequential execution, fresh context each time.

### By Complexity

**Phase:** "Dashboard Buildout"

**Split:**
```
- 05-01-PLAN.md: Layout shell (simple: sidebar, header, routing)
- 05-02-PLAN.md: Data fetching (moderate: TanStack Query setup, API integration)
- 05-03-PLAN.md: Data visualization (complex: charts, tables, real-time updates)
```

Complex work gets its own plan with full context budget.

### By Verification Points

**Phase:** "Deployment Pipeline"

**Split:**
```
- 06-01-PLAN.md: Vercel setup (deploy via CLI, configure domains)
  → Ends with checkpoint:human-verify "check xyz.vercel.app loads"

- 06-02-PLAN.md: Environment config (secrets via CLI, env vars)
  → Autonomous (no checkpoints) → subagent execution

- 06-03-PLAN.md: CI/CD (GitHub Actions, preview deploys)
  → Ends with checkpoint:human-verify "check PR preview works"
```

Verification checkpoints create natural boundaries. Autonomous plans between checkpoints execute via subagent with fresh context.

## Autonomous vs Interactive Plans

**Critical optimization:** Plans without checkpoints don't need main context.

### Autonomous Plans (No Checkpoints)
- Contains only `type="auto"` tasks
- No user interaction needed
- **Execute via subagent with fresh 200k context**
- Impossible to degrade (always starts at 0%)
- Creates SUMMARY, commits, reports back
- Can run in parallel (multiple subagents)

### Interactive Plans (Has Checkpoints)
- Contains `checkpoint:human-verify` or `checkpoint:decision` tasks
- Requires user interaction
- Must execute in main context
- Still target 50% context (2-3 tasks)

**Planning guidance:** If splitting a phase, try to:
- Group autonomous work together (→ subagent)
- Separate interactive work (→ main context)
- Maximize autonomous plans (more fresh contexts)

Example:
```
Phase: Feature X
- 07-01-PLAN.md: Backend (autonomous) → subagent
- 07-02-PLAN.md: Frontend (autonomous) → subagent
- 07-03-PLAN.md: Integration test (has checkpoint:human-verify) → main context
```

Two fresh contexts, one interactive verification. Perfect.

## Anti-Patterns

### ❌ The "Comprehensive Plan" Anti-Pattern

```
Plan: "Complete Authentication System"
Tasks:
1. Database models
2. Migration files
3. Auth API endpoints
4. JWT utilities
5. Protected route middleware
6. Password hashing
7. Login form component
8. Registration form component

Result: 8 tasks, 80%+ context, degradation at task 4-5
```

**Why this fails:**
- Task 1-3: Good quality
- Task 4-5: "I'll do these concisely" = degradation begins
- Task 6-8: Rushed, minimal, poor quality

### ✅ The "Atomic Plan" Pattern

```
Split into 4 plans:

Plan 1: "Auth Database Models" (2 tasks)
- Database schema (User, Session)
- Migration files

Plan 2: "Auth API Core" (3 tasks)
- Register endpoint
- Login endpoint
- JWT utilities

Plan 3: "Auth API Protection" (2 tasks)
- Protected route middleware
- Logout endpoint

Plan 4: "Auth UI Components" (2 tasks)
- Login form
- Registration form
```

**Why this succeeds:**
- Each plan: 2-3 tasks, 30-40% context
- All tasks: Peak quality throughout
- Git history: 4 focused commits
- Easy to verify each piece
- Rollback is surgical

### ❌ The "Efficiency Trap" Anti-Pattern

```
Thinking: "These tasks are small, let's do 6 to be efficient"

Result: Task 1-2 are good, task 3-4 begin degrading, task 5-6 are rushed
```

**Why this fails:** You're optimizing for fewer plans, not quality. The "efficiency" is false - poor quality requires more rework.

### ✅ The "Quality First" Pattern

```
Thinking: "These tasks are small, but let's do 2-3 to guarantee quality"

Result: All tasks peak quality, clean commits, no rework needed
```

**Why this succeeds:** You optimize for quality, which is true efficiency. No rework = faster overall.

## Estimating Context Usage

**Rough heuristics for plan size:**

### File Counts
- 0-3 files modified: Small task (~10-15% context)
- 4-6 files modified: Medium task (~20-30% context)
- 7+ files modified: Large task (~40%+ context) - split this

### Complexity
- Simple CRUD: ~15% per task
- Business logic: ~25% per task
- Complex algorithms: ~40% per task
- Domain modeling: ~35% per task

### 2-Task Plan (Safe)
- 2 simple tasks: ~30% total ✅ Plenty of room
- 2 medium tasks: ~50% total ✅ At target
- 2 complex tasks: ~80% total ❌ Too tight, split

### 3-Task Plan (Risky)
- 3 simple tasks: ~45% total ✅ Good
- 3 medium tasks: ~75% total ⚠️ Pushing it
- 3 complex tasks: 120% total ❌ Impossible, split

**Conservative principle:** When in doubt, split. Better to have an extra plan than degraded quality.

## The Atomic Commit Philosophy

**What we're optimizing for:** Beautiful git history where each commit is:
- Focused (2-3 related changes)
- Complete (fully implemented, tested)
- Documented (clear commit message)
- Reviewable (small enough to understand)
- Revertable (surgical rollback possible)

**Bad git history (large plans):**
```
feat(auth): Complete authentication system
- Added 16 files
- Modified 8 files
- 1200 lines changed
- Contains: models, API, UI, middleware, utilities
```

Impossible to review, hard to understand, can't revert without losing everything.

**Good git history (atomic plans):**
```
feat(auth-01): Add User and Session database models
- Added schema files
- Added migration
- 45 lines changed

feat(auth-02): Implement register and login API endpoints
- Added /api/auth/register
- Added /api/auth/login
- Added JWT utilities
- 120 lines changed

feat(auth-03): Add protected route middleware
- Added middleware/auth.ts
- Added tests
- 60 lines changed

feat(auth-04): Build login and registration forms
- Added LoginForm component
- Added RegisterForm component
- 90 lines changed
```

Each commit tells a story. Each is reviewable. Each is revertable. This is craftsmanship.

## Quality Assurance Through Scope Control

**The guarantee:** When you follow the 2-3 task rule with 50% context target:

1. **Consistency:** First task has same quality as last task
2. **Thoroughness:** No "I'll complete X concisely" degradation
3. **Documentation:** Full context budget for comments/tests
4. **Error handling:** Space for proper validation and edge cases
5. **Testing:** Room for comprehensive test coverage

**The cost:** More plans to manage.

**The benefit:** Consistent excellence. No rework. Clean history. Maintainable code.

**The trade-off is worth it.**

## Summary

**Old way (3-6 tasks, 80% target):**
- Tasks 1-2: Good
- Tasks 3-4: Degrading
- Tasks 5-6: Poor
- Git: Large, unreviewable commits
- Quality: Inconsistent

**New way (2-3 tasks, 50% target):**
- All tasks: Peak quality
- Git: Atomic, surgical commits
- Quality: Consistent excellence
- Autonomous plans: Subagent execution (fresh context)

**The principle:** Aggressive atomicity. More plans, smaller scope, consistent quality.

**The rule:** If in doubt, split. Quality over consolidation. Always.

---

## Reference: User Gates

# User Gates Reference

User gates prevent Claude from charging ahead at critical decision points.

## Question Types

### AskUserQuestion Tool
Use for **structured choices** (2-4 options):
- Selecting from distinct approaches
- Domain/type selection
- When user needs to see options to decide

Examples:
- "What type of project?" (macos-app / iphone-app / web-app / other)
- "Research confidence is low. How to proceed?" (dig deeper / proceed anyway / pause)
- "Multiple valid approaches exist:" (Option A / Option B / Option C)

### Inline Questions
Use for **simple confirmations**:
- Yes/no decisions
- "Does this look right?"
- "Ready to proceed?"

Examples:
- "Here's the task breakdown: [list]. Does this look right?"
- "Proceed with this approach?"
- "I'll initialize a git repo. OK?"

## Decision Gate Loop

After gathering context, ALWAYS offer:

```
Ready to [action], or would you like me to ask more questions?

1. Proceed - I have enough context
2. Ask more questions - There are details to clarify
3. Let me add context - I want to provide additional information
```

Loop continues until user selects "Proceed".

## Mandatory Gate Points

| Location | Gate Type | Trigger |
|----------|-----------|---------|
| plan-phase | Inline | Confirm task breakdown |
| plan-phase | AskUserQuestion | Multiple valid approaches |
| plan-phase | AskUserQuestion | Decision gate before writing |
| research-phase | AskUserQuestion | Low confidence findings |
| research-phase | Inline | Open questions acknowledgment |
| execute-phase | Inline | Verification failure |
| execute-phase | Inline | Issues review before proceeding |
| execute-phase | AskUserQuestion | Previous phase had issues |
| create-brief | AskUserQuestion | Decision gate before writing |
| create-roadmap | Inline | Confirm phase breakdown |
| create-roadmap | AskUserQuestion | Decision gate before writing |
| handoff | Inline | Handoff acknowledgment |

## Good vs Bad Gating

### Good
- Gate before writing artifacts (not after)
- Gate when genuinely ambiguous
- Gate when issues affect next steps
- Quick inline for simple confirmations

### Bad
- Asking obvious choices ("Should I save the file?")
- Multiple gates for same decision
- AskUserQuestion for yes/no
- Gates after the fact
