---
title: "Paywall Pricing Optimizer"
description: "Design effective paywalls, structure subscription tiers, and optimize pricing for mobile apps. Covers monetization model selection, paywall screen design, pricing psychology, A/B testing strategy, and RevenueCat/StoreKit/Google Billing integration..."
category: "development"
source: "community"
author: "Community"
tags: ["paywall", "pricing", "optimizer"]
date: 2026-03-20
---

## Prerequisites

- A defined app concept (what it does, who it serves)
- Target platform (iOS, Android, or both)
- Revenue goal (hobby $1K/mo vs business $10K/mo)
- No tools required — this skill produces strategy and implementation guidance

## Workflow Overview

```
1. Assess the App
2. Choose Monetization Model
3. Design Subscription Tiers
4. Set Pricing
5. Design the Paywall Screen
6. Plan Pricing Experiments
```

---

## Step 1: Assess the App

Gather these inputs before making any monetization decisions:

**Questions to ask:**

1. What core value does the app provide? (entertainment, productivity, health,
   utility)
2. How often do users engage? (daily, weekly, occasionally)
3. Who is the target audience? (age, income, tech savviness)
4. What do competitors charge? (research 3-5 direct competitors)
5. Does the app have ongoing costs? (AI API calls, server infrastructure,
   content creation)

**Usage frequency determines model viability:**

| Frequency       | Best Models                      | Why                                      |
| --------------- | -------------------------------- | ---------------------------------------- |
| Daily           | Subscription                     | High engagement justifies recurring cost |
| 2-3x per week   | Subscription or freemium         | Moderate engagement, needs strong value  |
| Weekly or less  | One-time purchase or consumable  | Hard to justify subscription             |
| Sporadic/urgent | One-time purchase or pay-per-use | Users pay when they need it              |

---

## Step 2: Choose Monetization Model

### Decision Framework

```
Does the app provide ongoing, evolving value?
├── YES → Does it have significant per-use costs (AI, API)?
│   ├── YES → Freemium with consumables (credits/tokens)
│   └── NO → Subscription
└── NO → Is it a tool with finite, clear value?
    ├── YES → One-time purchase (or lifetime unlock)
    └── NO → Freemium with ads + optional ad removal
```

### Model Deep-Dive

**Subscription** (~70% of top-grossing apps)

- Best for: ongoing value, content, AI features, daily-use apps
- Pros: predictable revenue, high LTV, aligns with App Store incentives
- Cons: higher churn, requires continuous value delivery
- Apple/Google take: 30% year 1, 15% year 2+ (Small Business Program)

**One-Time Purchase**

- Best for: utilities, tools with finite value, privacy-focused apps
- Pros: simple, no churn anxiety, easy to communicate value
- Cons: no recurring revenue, need constant new user acquisition
- Tip: offer a "Pro" unlock at $9.99-29.99 for utilities

**Freemium with Consumables**

- Best for: AI-heavy apps (credits/tokens), on-demand services
- Pros: pay-for-what-you-use feels fair, low barrier to start
- Cons: unpredictable revenue, complex to balance
- Pattern: give 10-20 free credits, then sell packs ($2.99/50, $9.99/200)

**Ads + Ad Removal**

- Best for: mass-market apps with 100K+ DAU
- Pros: monetize free users, ad removal is easy upsell
- Cons: only viable at massive scale, degrades UX
- Reality check: most indie apps never reach the DAU needed

---

## Step 3: Design Subscription Tiers

### Free vs Premium Split

The free tier must deliver enough value to hook users, but leave them wanting
more. Apply the **"taste, not feast"** principle.

**What goes in Free:**

- Core functionality (enough to experience the value proposition)
- Limited usage (3-5 uses per day, 7-day history, basic features)
- Onboarding and setup
- Basic customization

**What goes in Premium:**

- Unlimited usage
- Advanced features (AI, analytics, export, sync)
- Customization and personalization
- Ad removal (if applicable)
- Priority support or early access

### Tier Naming

Choose names that communicate value, not hierarchy:

| Pattern          | Free Tier | Paid Tier | Best For           |
| ---------------- | --------- | --------- | ------------------ |
| Status-based     | Basic     | Pro       | Productivity tools |
| Capability-based | Starter   | Unlimited | Usage-limited apps |
| Experience-based | Free      | Premium   | Content/media apps |
| Playful          | Explorer  | Champion  | Gamified/wellness  |

Avoid: "Lite" (implies inferior), numbered tiers (confusing), more than 2 tiers
for indie apps (3+ tiers create decision paralysis).

### Two-Tier vs Three-Tier

**Two tiers (recommended for most indie apps):**

- Free + Premium
- Simple, clear upgrade path
- One decision: upgrade or not

**Three tiers (only if justified):**

- Free + Standard + Pro
- Use the decoy effect: make Standard the obvious choice
- Only viable if you have meaningfully different feature sets for each

---

## Step 4: Set Pricing

### Pricing Benchmarks by Category (2025)

| App Type           | Monthly     | Annual       | One-Time     |
| ------------------ | ----------- | ------------ | ------------ |
| Simple utility     | $2.99-4.99  | $19.99-29.99 | $4.99-9.99   |
| Habit/tracker      | $4.99-6.99  | $29.99-44.99 | $9.99-14.99  |
| Productivity       | $5.99-9.99  | $39.99-59.99 | $14.99-29.99 |
| Health/fitness     | $6.99-12.99 | $39.99-79.99 | -            |
| AI-powered tool    | $9.99-19.99 | $59.99-99.99 | -            |
| Education/learning | $6.99-14.99 | $49.99-99.99 | -            |
| Creative tool      | $4.99-9.99  | $29.99-59.99 | $14.99-29.99 |

### Pricing Sweet Spots

| Tier         | Monthly           | Annual              | Best For                 |
| ------------ | ----------------- | ------------------- | ------------------------ |
| Impulse buy  | $2.99-4.99/mo     | $19.99-29.99/yr     | Simple utilities         |
| **Standard** | **$5.99-6.99/mo** | **$34.99-44.99/yr** | **Most indie apps**      |
| Premium      | $9.99-14.99/mo    | $59.99-99.99/yr     | AI-heavy or professional |

### Pricing Psychology Rules

1. **Anchor with annual pricing** — show annual plan first, display the
   per-month equivalent, cross out the monthly price to show savings
2. **Use odd pricing** — $6.99 not $7.00, $49.99 not $50.00
3. **Show savings percentage** — "Save 40%" on annual plan
4. **Three-tier decoy** — if offering 3 options, make the middle tier the
   obvious best value (price it closer to the cheap option, feature-set closer
   to the expensive one)
5. **Pre-select the best-value plan** — highlight and pre-select the annual plan

### Free Trial Strategy

| Length  | Best For                       | Conversion Impact                     |
| ------- | ------------------------------ | ------------------------------------- |
| 3 days  | Apps with immediate value      | Higher conversion, lower trial starts |
| 7 days  | Standard choice for most apps  | Balanced conversion and adoption      |
| 14 days | Apps requiring habit formation | Higher trial starts, lower conversion |
| 30 days | B2B or complex tools           | Very low conversion, use sparingly    |

**Introductory offers:**

- 50% off first month or first year
- Extended free trial (14 days instead of 7)
- Seasonal promotions (New Year, back to school)

---

## Step 5: Design the Paywall Screen

### Hard vs Soft Paywall

**Hard paywall** (before any use):

- Only for apps with strong brand recognition or no free alternative
- Very few indie apps should use this
- Risk: 90%+ of users bounce immediately

**Soft paywall** (after value demonstration):

- Show the paywall after the user has experienced value
- Best triggers for showing the paywall:
  - After 3-5 uses of the core feature
  - After completing onboarding
  - After hitting a usage limit ("You've used 3 of 3 free scans today")
  - After achieving a milestone ("Great progress! Unlock unlimited tracking")
  - On attempting a premium feature (contextual upgrade prompt)

### Paywall Screen Anatomy

Design the paywall screen with these sections in order:

**1. Hero Section**

- Benefit-focused headline (NOT feature-focused)
- Bad: "Unlock Premium Features"
- Good: "Track Every Habit, Crush Every Goal"
- Good: "Never Lose a Thought Again"
- Subheadline reinforcing the outcome

**2. Feature/Benefit List**

- 3-5 items maximum (more causes decision fatigue)
- Use checkmarks or icons
- Frame as benefits, not features:
  - Bad: "Unlimited storage"
  - Good: "Save everything, forget nothing"
- Optional: side-by-side Free vs Premium comparison

**3. Social Proof**

- Star rating with review count ("4.8 stars from 12,000 reviews")
- Testimonial quote from a real review
- User count ("Join 50,000+ users")
- Press mentions or awards

**4. Pricing Cards**

- Show annual plan first (left or top position)
- Highlight annual as "Best Value" or "Most Popular"
- Show per-month equivalent for annual plan
- Show savings: "Save 40%" or cross out monthly equivalent
- Pre-select the annual plan

**5. Call-to-Action**

- Action-oriented text:
  - Good: "Start Free Trial", "Try 7 Days Free", "Unlock Everything"
  - Bad: "Subscribe", "Buy", "Purchase"
- Make the button large, high-contrast, and unmissable
- Below CTA: "Cancel anytime" or "No commitment"

**6. Trust Signals**

- "Cancel anytime" (most important — always include)
- "No commitment"
- "Secured by Apple" / "Secured by Google Play"
- "Restore purchases" link
- Privacy policy link

See [references/paywall-copy-formulas.md](references/paywall-copy-formulas.md)
for headline templates, CTA variations, and feature list copy patterns.

### Common Paywall Mistakes

1. **Too many plan options** — 2 is ideal, 3 max. Never 4+.
2. **Feature-focused copy** — users buy outcomes, not features.
3. **No free trial** — always offer a trial for subscriptions.
4. **Paywall too early** — show value before asking for money.
5. **Weak CTA** — "Subscribe" converts far worse than "Start Free Trial".
6. **No social proof** — testimonials and ratings build trust.
7. **Missing "Cancel anytime"** — this single line lifts conversion 10-15%.
8. **No price anchoring** — always show what the user saves.
9. **Ugly design** — the paywall is a product page; invest in its design.
10. **Same paywall everywhere** — contextualize based on what triggered it.

---

## Step 6: Plan Pricing Experiments

Before committing to a pricing strategy, plan what to test.

See [references/pricing-experiments.md](references/pricing-experiments.md) for
detailed A/B testing methodology, sample size calculators, and experiment
prioritization.

### What to Test First (Priority Order)

1. **Free trial length** (3 vs 7 vs 14 days) — biggest lever
2. **Paywall timing** (after onboarding vs after 3 uses vs on premium feature)
3. **Annual vs monthly default** (which is pre-selected)
4. **Headline copy** (benefit A vs benefit B)
5. **Price point** ($4.99 vs $6.99 vs $9.99)
6. **Social proof** (with vs without)

### Key Metrics to Track

| Metric                   | Formula                            | Target   |
| ------------------------ | ---------------------------------- | -------- |
| Trial start rate         | Trials / paywall views             | 15-30%   |
| Trial-to-paid conversion | Paid / trial starts                | 40-60%   |
| Paywall conversion rate  | Purchases / paywall views          | 5-15%    |
| ARPU (avg revenue/user)  | Total revenue / total users        | Varies   |
| LTV (lifetime value)     | ARPU \* avg subscription length    | > 3x CAC |
| Monthly churn rate       | Cancellations / active subscribers | < 10%    |

---

## RevenueCat / StoreKit / Google Billing Integration

### RevenueCat (Recommended for Indie Devs)

RevenueCat abstracts StoreKit and Google Billing into a single SDK. Free up to
$2,500/mo MTR.

**Setup pattern:**

1. Create a RevenueCat project and add App Store / Google Play apps
2. Configure products in App Store Connect / Google Play Console
3. Configure offerings and entitlements in RevenueCat dashboard
4. Install SDK: `expo install react-native-purchases`
5. Initialize on app launch with API key
6. Fetch offerings to display on paywall
7. Make purchase and check entitlement status
8. Handle restore purchases

**Key concepts:**

- **Product** — the SKU in App Store Connect / Google Play Console
- **Entitlement** — what the user unlocks (e.g., "premium")
- **Offering** — a group of packages shown on the paywall (allows remote config)
- **Package** — a product within an offering (e.g., monthly, annual)

### StoreKit 2 (iOS Native)

Use StoreKit 2 for Swift/SwiftUI apps without RevenueCat:

- `Product.products(for:)` to fetch products
- `product.purchase()` to initiate purchase
- `Transaction.currentEntitlements` to check active subscriptions
- `Transaction.updates` to listen for transaction changes
- Handle `Transaction.unverified` cases

### Google Play Billing Library (Android Native)

Use Billing Library 6+ for Kotlin/Java apps:

- `BillingClient.queryProductDetailsAsync()` to fetch products
- `BillingClient.launchBillingFlow()` to initiate purchase
- `BillingClient.queryPurchasesAsync()` to check active subscriptions
- Acknowledge purchases within 3 days or they auto-refund

### Cross-Platform (Expo / React Native)

For Expo apps, RevenueCat is the standard approach:

- `expo install react-native-purchases`
- Configure `app.json` with `eas.build` for native module support
- Test with sandbox accounts on both platforms
- Use `expo-dev-client` for development builds (Expo Go does not support IAP)

---

## Output Deliverables

At the end of this workflow, deliver:

1. **Monetization model recommendation** with reasoning
2. **Tier structure** — what is free vs premium
3. **Pricing recommendation** — monthly, annual, and any introductory offers
4. **Paywall screen spec** — layout, copy, and design direction
5. **Experiment plan** — first 3 tests to run, ordered by impact
6. **Integration guidance** — RevenueCat/StoreKit/Billing setup steps

---

## Reference: Paywall Copy Formulas

# Paywall Copy Formulas

## Headline Formulas

### Benefit-Outcome Pattern

- "Unlock [Desired Outcome] — [Timeframe]"
- "[Action Verb] Every [Thing], [Achieve Goal]"
- "Never [Pain Point] Again"
- "Your [Category] Journey, Supercharged"

### Examples by Category

**Productivity:**

- "Get More Done in Less Time"
- "Never Miss a Deadline Again"
- "Your Most Productive Self Starts Here"

**Health & Fitness:**

- "Unlock Your Full Potential"
- "Every Workout Tracked, Every Goal Crushed"
- "The Body You Want, the Plan You Need"

**Habit Tracking:**

- "Build Habits That Actually Stick"
- "Track Every Habit, Crush Every Goal"
- "Your Streak, Your Rules, No Limits"

**AI-Powered Tools:**

- "Unlimited AI, Unlimited Possibilities"
- "Your Personal AI — Always On, Always Ready"
- "Ask Anything, Anytime, Without Limits"

**Journaling / Mindfulness:**

- "Never Lose a Thought Again"
- "Your Mind, Organized and Calm"
- "Reflect Deeper, Live Better"

**Finance / Budgeting:**

- "Take Control of Every Dollar"
- "Your Money, Your Rules, Full Visibility"
- "Spend Smarter Starting Today"

**Learning / Education:**

- "Learn Faster, Remember Longer"
- "Your Personal Tutor, Always Available"
- "Master Anything at Your Pace"

### Headlines to Avoid

- "Unlock Premium Features" (generic, says nothing)
- "Go Pro" (overused, no value proposition)
- "Upgrade Now" (command without benefit)
- "Subscribe to Premium" (describes the action, not the outcome)

---

## Subheadline Patterns

Subheadlines reinforce the headline with specifics:

- "Join [X] users who [achieved outcome]"
- "Get [specific feature], [specific feature], and more"
- "Starting at just [price]/month — cancel anytime"
- "[X]-day free trial, no commitment"

---

## CTA Button Copy

### High-Converting CTAs (Use These)

- "Start Free Trial"
- "Try [X] Days Free"
- "Unlock Everything"
- "Start My Free Week"
- "Get Started Free"
- "Claim Your Free Trial"
- "Continue with Premium"

### Low-Converting CTAs (Avoid These)

- "Subscribe" (transactional, cold)
- "Buy" (too direct, triggers loss aversion)
- "Purchase" (formal, corporate)
- "Pay" (focuses on cost, not value)
- "Sign Up" (vague, no value)

### CTA Modifiers That Lift Conversion

- Add "Free" — "Start Free Trial" beats "Start Trial"
- Add timeframe — "Try 7 Days Free" beats "Start Free Trial"
- Add possessive — "Start My Free Trial" beats "Start Free Trial"
- Add action — "Unlock Everything" beats "Get Premium"

---

## Feature List Copy Patterns

### Transform Features into Benefits

| Feature (Don't Use)    | Benefit (Use This)                               |
| ---------------------- | ------------------------------------------------ |
| Unlimited storage      | Save everything, forget nothing                  |
| Cloud sync             | Access anywhere, on any device                   |
| Advanced analytics     | Understand your progress at a glance             |
| Custom themes          | Make it yours with unlimited styles              |
| AI-powered suggestions | Get personalized recommendations daily           |
| Export to PDF          | Share professional reports instantly             |
| Priority support       | Get help whenever you need it                    |
| Ad-free experience     | Zero distractions, pure focus                    |
| Unlimited projects     | No limits on what you can create                 |
| Widget support         | Your data at a glance, right on your home screen |

### Feature List Structure

Present 3-5 benefits maximum. Order by value:

1. **Primary differentiator** — the #1 reason to upgrade
2. **Usage unlock** — remove the limit they just hit
3. **Quality upgrade** — better version of something they already use
4. **Convenience feature** — nice-to-have that sweetens the deal
5. **Trust/support** — priority support or early access (optional)

### Free vs Premium Comparison Pattern

```
FREE                          PREMIUM
✓ 3 habits per day            ✓ Unlimited habits
✓ 7-day history               ✓ Full history & trends
✓ Basic reminders             ✓ Smart reminders & widgets
✗ No export                   ✓ Export & share reports
✗ Ads                         ✓ Ad-free experience
```

---

## Objection Handling Copy

Place these near the CTA or below the pricing cards:

### Price Objections

- "Less than a coffee a week" (for $2.99-4.99/mo)
- "Less than a single [competitor] month" (if undercutting)
- "That's just [X] cents per day"

### Commitment Objections

- "Cancel anytime — no questions asked" (MOST IMPORTANT, always include)
- "No commitment, no contracts"
- "Try it risk-free for [X] days"
- "Not ready? Keep using the free version"

### Trust Objections

- "Secured by Apple" / "Protected by Google Play"
- "Your data stays on your device"
- "Trusted by [X]+ users"
- "4.8 stars from [X] reviews"
- "30-day money-back guarantee"

### Value Objections

- "Everything you need, nothing you don't"
- "New features added monthly"
- "Built by [solo dev / small team] who actually uses it"

---

## Contextual Paywall Copy

Match the paywall message to what triggered it:

### Usage Limit Hit

- Headline: "You're on a Roll — Keep Going"
- Subheadline: "You've used all 3 free [actions] today. Unlock unlimited
  [actions]."

### Premium Feature Tap

- Headline: "Unlock [Feature Name]"
- Subheadline: "[Feature name] helps you [specific benefit]. Try it free for [X]
  days."

### Post-Onboarding

- Headline: "You're All Set — Now Go Further"
- Subheadline: "Upgrade to get the most out of [App Name]."

### Milestone Achievement

- Headline: "Amazing Progress — Don't Stop Now"
- Subheadline: "You've [achieved X]. Premium users [achieve Y] faster."

### Re-Engagement (Lapsed User)

- Headline: "Welcome Back — We Missed You"
- Subheadline: "Pick up where you left off with [X] new features."

---

## Reference: Pricing Experiments

# Pricing Experiments Guide

## Experiment Prioritization

Run experiments in this order — each one is a higher-impact lever than the next:

| Priority | Experiment             | Expected Impact | Difficulty |
| -------- | ---------------------- | --------------- | ---------- |
| 1        | Free trial length      | 20-50% lift     | Low        |
| 2        | Paywall timing/trigger | 15-40% lift     | Medium     |
| 3        | Default plan selection | 10-30% lift     | Low        |
| 4        | Headline copy          | 5-20% lift      | Low        |
| 5        | Price point            | 10-30% lift     | Medium     |
| 6        | Social proof presence  | 5-15% lift      | Low        |
| 7        | Number of plan options | 5-15% lift      | Low        |
| 8        | CTA button copy        | 3-10% lift      | Low        |
| 9        | Feature list content   | 3-10% lift      | Low        |
| 10       | Visual design          | 3-10% lift      | Medium     |

---

## Experiment Design

### Anatomy of a Good Experiment

1. **Hypothesis** — "Changing [X] from [A] to [B] will increase [metric] by
   [amount] because [reasoning]"
2. **Primary metric** — one metric that determines success (e.g., trial start
   rate)
3. **Guardrail metrics** — metrics that must not degrade (e.g., retention,
   refund rate)
4. **Sample size** — minimum users per variant for statistical significance
5. **Duration** — how long to run before making a decision
6. **Segments** — new users only, all users, or specific cohorts

### Sample Size Requirements

For a standard A/B test with 95% confidence and 80% power:

| Baseline Rate | Minimum Detectable Effect | Sample Size Per Variant |
| ------------- | ------------------------- | ----------------------- |
| 5%            | 20% relative (5% → 6%)    | ~14,500                 |
| 5%            | 50% relative (5% → 7.5%)  | ~2,500                  |
| 10%           | 20% relative (10% → 12%)  | ~6,500                  |
| 10%           | 50% relative (10% → 15%)  | ~1,100                  |
| 20%           | 20% relative (20% → 24%)  | ~2,800                  |
| 20%           | 50% relative (20% → 30%)  | ~500                    |

**For indie apps with limited traffic:** focus on tests with large expected
effect sizes (>30% relative change). Small optimizations require traffic volumes
most indie apps do not have.

### Minimum Viable Experiment

If traffic is too low for formal A/B testing:

1. **Sequential testing** — run variant A for 2 weeks, then variant B for 2
   weeks. Less rigorous but practical for <1,000 users/month.
2. **Cohort comparison** — compare new users in week 1 (variant A) vs week 3
   (variant B). Account for seasonality.
3. **Price sensitivity survey** — ask users directly via in-app survey. "What
   would you expect to pay for this app?" with ranges.

---

## Experiment Playbooks

### Experiment 1: Free Trial Length

**Variants:**

- A: 3-day free trial
- B: 7-day free trial
- C: 14-day free trial (optional third variant if traffic allows)

**Primary metric:** Trial-to-paid conversion rate **Secondary metrics:** Trial
start rate, Day 30 retention **Why it matters:** Shorter trials create urgency
but fewer users start them. Longer trials build habit but many users forget to
cancel and then refund.

**Expected results:**

- 3-day: Higher conversion rate (50-70%), lower trial starts
- 7-day: Balanced (40-55% conversion, moderate trial starts)
- 14-day: Lower conversion (30-45%), higher trial starts

**Decision framework:** Optimize for total revenue, not conversion rate alone.
`Revenue = trial_starts * conversion_rate * price`

---

### Experiment 2: Paywall Timing

**Variants:**

- A: Show paywall after onboarding completion
- B: Show paywall after 3rd use of core feature
- C: Show paywall only on premium feature tap

**Primary metric:** Overall paywall conversion rate **Secondary metrics:** Day 7
retention, lifetime value **Why it matters:** Too early = user hasn't seen
value. Too late = user is happy with free tier.

**Expected results:**

- After onboarding: Highest impression volume, lowest conversion
- After 3rd use: Moderate impressions, highest conversion (user has seen value)
- On premium feature tap: Lowest impressions, moderate conversion (contextual)

**Decision framework:** Measure conversion AND retention together. A paywall
that converts 15% but causes 30% of non-converters to churn is worse than one
that converts 8% with 90% retention.

---

### Experiment 3: Default Plan Selection

**Variants:**

- A: Monthly plan pre-selected
- B: Annual plan pre-selected
- C: No plan pre-selected

**Primary metric:** Revenue per paywall view **Secondary metrics:** Plan mix (%
annual vs monthly), refund rate **Why it matters:** Pre-selecting annual
increases ARPU but may increase chargebacks if users feel tricked.

**Expected results:**

- Monthly pre-selected: Higher conversion count, lower ARPU
- Annual pre-selected: Lower conversion count, higher ARPU, watch refund rate
- No pre-selection: Lowest conversion, but most intentional subscribers

---

### Experiment 4: Headline Copy

**Variants:**

- A: Benefit-focused ("Build Habits That Actually Stick")
- B: Outcome-focused ("Join 50,000 Users Who Changed Their Lives")
- C: Feature-focused ("Unlock Unlimited Tracking & Analytics")

**Primary metric:** Trial start rate **Secondary metrics:** Paywall scroll
depth, time on paywall **Why it matters:** The headline is the first thing users
read. It frames everything below it.

**Expected results:** Benefit and outcome headlines typically outperform
feature-focused headlines by 15-30%.

---

### Experiment 5: Price Point

**Variants:**

- A: $4.99/mo ($29.99/yr)
- B: $6.99/mo ($44.99/yr)
- C: $9.99/mo ($59.99/yr)

**Primary metric:** Revenue per user (not conversion rate alone) **Secondary
metrics:** Conversion rate, churn rate at 30/60/90 days **Why it matters:**
Higher price = fewer conversions but more revenue per conversion. The optimum
depends on your app's perceived value.

**Revenue calculation:**

```
Revenue per 1,000 paywall views:
$4.99 at 12% conversion = $598.80
$6.99 at 9% conversion  = $629.10  ← often the winner
$9.99 at 6% conversion  = $599.40
```

**Warning:** Price experiments are the hardest to run cleanly. Different users
seeing different prices can cause complaints. Consider sequential testing
(change price for all users, measure cohort performance over time).

---

## Measuring Results

### Statistical Significance

Do not make decisions until reaching statistical significance (p < 0.05).

**Quick significance check:**

- Use an online calculator (e.g., ABTestGuide, Evan Miller's calculator)
- Input: visitors per variant, conversions per variant
- Output: confidence level and whether the result is significant

**Common mistakes:**

- Peeking at results too early and declaring a winner
- Stopping the test as soon as one variant "looks better"
- Running tests for less than 1 full week (day-of-week effects)
- Not accounting for novelty effect (new UI converts better initially)

### Minimum Test Duration

Always run for at least:

- **7 days** — to capture day-of-week variation
- **14 days** — for subscription tests (to capture trial expiration)
- **1 full billing cycle** — for price tests (to capture actual payments)

### Revenue vs Conversion Rate

Optimize for **revenue per paywall view**, not conversion rate:

```
Revenue per paywall view = conversion_rate * average_revenue_per_conversion
```

A variant with 5% conversion at $9.99/mo generates more revenue than 10%
conversion at $3.99/mo.

---

## RevenueCat Experiments

RevenueCat has built-in experiment support (requires paid plan):

1. Create an experiment in the RevenueCat dashboard
2. Define control and variant offerings
3. Set allocation percentage (usually 50/50)
4. RevenueCat automatically tracks revenue metrics per variant
5. View results in the Experiments tab with statistical significance

**Advantages:** Tracks actual revenue (not just conversions), handles
subscription lifecycle automatically, accounts for refunds and renewals.

**Limitation:** Only tests different offerings (price/plan structure). For
paywall UI/copy tests, use a feature flag system (PostHog, LaunchDarkly,
Firebase Remote Config) alongside RevenueCat.

---

## Post-Experiment Action Plan

After each experiment concludes:

1. **Document the result** — hypothesis, variants, sample sizes, winner, lift
2. **Implement the winner** for all users
3. **Wait 2 weeks** before starting the next experiment (clean baseline)
4. **Re-test the winner** in 6 months (user base evolves, market changes)
5. **Share learnings** — price sensitivity and paywall behavior inform product
   decisions beyond just the paywall
