---
title: "App Growth Playbook"
description: "Generate platform-specific, actionable growth playbooks for mobile apps. Use when planning a Product Hunt launch, creating TikTok/Reels content strategies, setting up Apple Search Ads campaigns, preparing App Store featuring submissions, building ..."
category: "workflow"
source: "community"
author: "Community"
tags: ["app", "growth", "playbook"]
date: 2026-03-20
---

# App Growth Playbook

## Core Workflow

### 1. Assess Current State

Gather the following before selecting channels:

- **Downloads**: monthly installs, trend direction, organic vs. paid split
- **Retention**: D1, D7, D30 retention rates
- **Revenue**: ARPU, LTV, current monetization model
- **Audience**: primary demographic, geographic concentration, device split
- **Current channels**: what has been tried, what worked, what failed

### 2. Select Growth Channels

Use the channel selection matrix to pick 2-3 channels based on app category and
budget.

| Channel               | Best For                                       | Budget    | Timeline to Results |
| --------------------- | ---------------------------------------------- | --------- | ------------------- |
| Product Hunt          | B2B, productivity, developer tools             | Free      | 1-2 weeks           |
| Reddit                | Niche/community apps, indie projects           | Free      | 2-4 weeks           |
| TikTok/Reels          | Consumer apps, visual apps, lifestyle          | Free      | 4-8 weeks           |
| Apple Search Ads      | Any iOS app with clear keywords                | $5-20/day | 1-2 weeks           |
| App Store Featuring   | High-quality, design-forward apps              | Free      | 4-12 weeks          |
| Content Marketing/SEO | Apps solving searchable problems               | Free-low  | 2-6 months          |
| Referral/Viral Loops  | Social, messaging, collaboration apps          | Dev time  | 4-8 weeks           |
| Email/Push            | Apps with existing user base needing retention | Free-low  | 1-2 weeks           |

**Budget tiers:**

- **$0/month**: Product Hunt, Reddit, TikTok/Reels, App Store Featuring,
  Referral
- **$150-600/month**: Apple Search Ads, Content Marketing (hosting/tools)
- **$600+/month**: Paid social, influencer partnerships, Google Ads

### 3. Execute Channel Playbooks

Load the appropriate reference file for detailed execution:

- `references/product-hunt-playbook.md` — Full Product Hunt launch timeline,
  templates, and activation plan
- `references/social-media-templates.md` — TikTok/Reels scripts, Reddit posts,
  hashtag strategies
- `references/paid-acquisition.md` — Apple Search Ads and Google Ads campaign
  setup
- `references/content-marketing.md` — Blog templates, SEO strategies, landing
  page patterns

### 4. Measure and Iterate

Track these metrics weekly per channel:

| Metric                | Formula                        | Target       |
| --------------------- | ------------------------------ | ------------ |
| CAC                   | spend / installs               | < 1/3 of LTV |
| Install-to-trial rate | trials / installs              | > 30%        |
| Trial-to-paid rate    | paid / trials                  | > 10%        |
| Payback period        | CAC / monthly revenue per user | < 3 months   |
| Channel ROI           | (revenue - spend) / spend      | > 2x         |

**Decision framework after 2 weeks per channel:**

- ROI > 2x → double budget
- ROI 1-2x → optimize creative/targeting for 2 more weeks
- ROI < 1x → pause and reallocate to higher-performing channel

## Channel Playbook Summaries

### Product Hunt Launch

**Preparation timeline**: start 2 weeks before launch.

Key elements:

- Schedule for Tuesday-Thursday, post goes live at 12:01 AM PT
- Secure a hunter with 1,000+ followers or self-hunt with a strong network
- Prepare maker's comment (first comment on post) — personal story, not sales
  pitch
- Build activation list of 50+ people who will upvote and comment authentically
- Prepare 5 different social media announcements for launch day

Load `references/product-hunt-playbook.md` for the full timeline, hunter
outreach template, maker's comment template, and activation plan.

### Reddit Launch & Ongoing

**Core principle**: contribute value first, promote second.

Key elements:

- Research 5-10 subreddits where the target audience participates
- Use "soft launch" format — ask for feedback, share the journey, not "check out
  my app"
- Target subreddits: r/SideProject, r/IndieDev, r/EntrepreneurRideAlong, plus
  niche-specific
- Follow each subreddit's self-promotion rules exactly
- Build karma and history before posting about the app

Load `references/social-media-templates.md` for Reddit post templates and
subreddit research guide.

### TikTok/Reels Content

**Video structure** (20 seconds total):

1. Hook (2s) — pattern interrupt or bold claim
2. Problem (3s) — relatable frustration
3. Demo (10s) — screen recording with zooms and annotations
4. Result (3s) — before/after or outcome
5. CTA (2s) — "Link in bio" or "Search [app name]"

**Hook formulas:**

- "POV: you discover an app that [solves specific problem]"
- "This app is a game changer for [audience]"
- "Stop [old way]. Start [new way with app]"
- "I wish I found this app sooner"

Load `references/social-media-templates.md` for full video scripts, posting
schedule, and hashtag strategy.

### Apple Search Ads

**Campaign structure for indie budgets ($5-20/day):**

| Campaign   | Keywords               | Bid        | Budget Share |
| ---------- | ---------------------- | ---------- | ------------ |
| Brand      | App name, variations   | $0.50-1.00 | 10%          |
| Competitor | Competitor app names   | $1.00-3.00 | 20%          |
| Category   | Generic category terms | $0.75-2.00 | 40%          |
| Discovery  | Search Match (auto)    | $0.50-1.50 | 30%          |

Load `references/paid-acquisition.md` for full setup guide, bid optimization,
and creative set strategy.

### App Store Featuring

**What Apple looks for:**

- Exceptional design following Human Interface Guidelines
- Accessibility support (VoiceOver, Dynamic Type)
- Adoption of latest Apple technologies (widgets, Live Activities, visionOS)
- Localization (more languages = higher chance)
- No crashes, no major bugs

**How to submit:**

1. Open App Store Connect → navigate to the app
2. Use the "Promote Your App" section or email appstorepromotion@apple.com
3. Time submissions around iOS releases, seasonal events, or major app updates
4. Create App Store Connect events for in-app promotions

Load `references/content-marketing.md` for tips on optimizing App Store
presence.

### Referral & Viral Loops

**Trigger moments** — prompt sharing after:

- First achievement or milestone
- Positive feedback moment (completed task, reached goal)
- Social proof moment (join streak, leaderboard placement)
- Content creation (user generates something shareable)

**Incentive structures that convert:**

- 7-day premium trial for both referrer and invitee
- In-app credits or currency
- Feature unlocks (themes, icons, advanced features)
- Never require a referral — always make it optional

Load `references/content-marketing.md` for referral program design patterns.

### Email & Push Notification Strategy

**Push notification rules:**

- Send within user's active hours (track per-user timezone)
- Limit to 1-2 per day maximum
- Personalize with user data (name, last action, streak count)
- Use urgency sparingly — not every message is urgent

**Re-engagement timing:**

| Segment     | Timing | Message Type                |
| ----------- | ------ | --------------------------- |
| D1 churned  | Day 2  | "You left off at [state]"   |
| D7 churned  | Day 8  | Feature they haven't tried  |
| D30 churned | Day 31 | Major update or new feature |
| D90 churned | Day 91 | "We miss you" + incentive   |

Load `references/content-marketing.md` for email sequence templates and push
notification copy patterns.

## Execution Priority

For a brand-new app with zero budget, execute channels in this order:

1. **Week 1-2**: Optimize App Store listing (screenshots, description, keywords)
2. **Week 2-3**: Soft launch on Reddit (r/SideProject, niche subreddits)
3. **Week 3-4**: Product Hunt launch
4. **Week 4-8**: Begin TikTok/Reels content (3 videos/week)
5. **Week 4+**: Start Apple Search Ads at $5/day
6. **Month 2+**: Build referral loop into the app
7. **Month 3+**: Begin content marketing / SEO

For an app with an existing user base, start with email/push re-engagement and
referral loops before acquiring new users.

---

## Reference: Content Marketing

# Content Marketing & Organic Growth

## Blog Post Templates for App SEO

### Target Keyword Strategy

Focus on keywords with purchase intent — people searching for solutions:

| Keyword Pattern            | Example                           | Search Intent            |
| -------------------------- | --------------------------------- | ------------------------ |
| "[problem] app"            | "habit tracker app"               | High — ready to download |
| "best [category] app"      | "best budgeting app"              | High — comparing options |
| "how to [task] on iPhone"  | "how to track expenses on iPhone" | Medium — may want an app |
| "[competitor] alternative" | "todoist alternative"             | High — ready to switch   |
| "[task] template"          | "workout plan template"           | Medium — may want an app |

### Blog Post Template 1: "[Problem] App" Article

Target keyword: "[specific problem] app"

```
Title: The Best [Problem] App for [Year]: How [App Name] [Solves It]

H2: Why You Need a [Problem] App
[2-3 paragraphs about the problem. Reference statistics or common pain points.
Link to studies or surveys if available.]

H2: What to Look for in a [Problem] App
[Bulleted list of 5-7 criteria. Position these to match your app's strengths.]
- [Criterion 1 — your app's top strength]
- [Criterion 2]
- [Criterion 3]
- [Criterion 4]
- [Criterion 5]

H2: How [App Name] Solves [Problem]
[3-4 paragraphs with screenshots showing the app in action.
Focus on outcomes, not features.]

H3: [Feature 1 as Benefit]
[Paragraph + screenshot]

H3: [Feature 2 as Benefit]
[Paragraph + screenshot]

H3: [Feature 3 as Benefit]
[Paragraph + screenshot]

H2: How to Get Started with [App Name]
[Step-by-step guide with screenshots. Make it easy to visualize using the app.]
1. Download from [App Store / Play Store link]
2. [Setup step]
3. [First use step]
4. [Key feature step]

H2: What Users Are Saying
[3-5 real user testimonials or App Store reviews]

H2: Start [Solving Problem] Today
[CTA paragraph. Link to App Store / Play Store. Mention free trial if applicable.]
```

### Blog Post Template 2: "[Competitor] Alternative" Article

Target keyword: "[competitor name] alternative"

```
Title: Looking for a [Competitor] Alternative? Try [App Name]

H2: Why People Switch from [Competitor]
[Research actual complaints from Reddit, App Store reviews, Twitter.
List 3-5 genuine pain points.]

H2: [App Name] vs [Competitor]: Key Differences
[Comparison table]

| Feature | [App Name] | [Competitor] |
|---------|-----------|-------------|
| [Feature 1] | ✓ [detail] | ✗ or partial |
| [Feature 2] | ✓ [detail] | ✓ [but limitation] |
| Pricing | $X/month | $Y/month |
| Free tier | [Details] | [Details] |

H2: What [App Name] Does Better
[2-3 sections, each with screenshots, focusing on genuine differentiators]

H2: Making the Switch
[Migration guide if applicable. Step-by-step process to move from competitor.]

H2: Try [App Name] Free
[CTA with link]
```

### Blog Post Template 3: "How To" Tutorial

Target keyword: "how to [task]"

```
Title: How to [Task]: A Step-by-Step Guide (with [App Name])

H2: The Quick Way to [Task]
[4-5 numbered steps using the app. Include screenshots for each step.
Put this first — many readers want the answer immediately.]

H2: Why [Task] Matters
[Context and motivation. Keep brief — 2 paragraphs max.]

H2: Method 1: Using [App Name] (Recommended)
[Detailed walkthrough with screenshots]

H2: Method 2: Manual Approach
[Show the harder way. This builds credibility and makes the app look appealing.]

H2: Tips for Better [Task Outcomes]
[5-7 actionable tips. Mix app-specific and general advice.]

H2: Get Started
[CTA paragraph]
```

## Landing Page Optimization

### Above-the-Fold Checklist

Every app landing page must have these elements visible without scrolling:

- [ ] Headline: "[Verb] [outcome] with [App Name]" (8 words max)
- [ ] Subheadline: 1 sentence expanding on the benefit
- [ ] App screenshot or demo video (phone mockup)
- [ ] App Store badge + Play Store badge (linked)
- [ ] Social proof: "X downloads" or "Rated Y stars" or press logos

### Landing Page Structure

```
Section 1: Hero (above the fold)
- Headline + subheadline
- Phone mockup with app screenshot
- Download buttons
- Social proof bar

Section 2: Problem/Solution (3-4 short paragraphs)
- State the problem
- Show how the app solves it
- Include a GIF or short video

Section 3: Features (3 key features with screenshots)
- Feature 1 with screenshot
- Feature 2 with screenshot
- Feature 3 with screenshot

Section 4: Social Proof
- App Store reviews (embed or screenshot)
- User testimonials (with photos and names)
- Press mentions
- Download count or user count

Section 5: Pricing (if applicable)
- Clear pricing table
- Highlight recommended plan
- Free trial CTA

Section 6: FAQ (5-7 questions)
- Address common objections
- Include "Is it free?" question
- Include platform availability

Section 7: Final CTA
- Repeat download buttons
- Urgency or incentive ("Start free today")
```

### Conversion Rate Benchmarks

| Element                    | Benchmark         | Action if Below                           |
| -------------------------- | ----------------- | ----------------------------------------- |
| Page load time             | < 3 seconds       | Compress images, reduce scripts           |
| Bounce rate                | < 50%             | Improve headline and hero section         |
| Scroll depth               | > 60% see pricing | Shorten page or improve engagement        |
| CTA click rate             | > 5%              | Make buttons larger, improve copy         |
| App Store visit to install | > 30%             | Improve App Store screenshots/description |

## YouTube Video Templates

### App Demo Video (3-5 minutes)

```
[0:00-0:15] Hook
"If you've been looking for a better way to [solve problem], this is it."
(Show the end result first — the best output of the app)

[0:15-0:45] Introduce the Problem
"Most [audience] struggle with [problem] because [reason]."
(Show the frustrating old way briefly)

[0:45-1:00] Introduce the App
"That's why I want to show you [App Name]."
(Show the app icon and name)

[1:00-3:30] Demo
(Full walkthrough of the core use case)
Step 1: [Action] — explain why this matters
Step 2: [Action] — highlight what's different
Step 3: [Action] — show the output/result
(Use zoom-ins, annotations, and highlight clicks)

[3:30-4:00] Results
"In [X minutes], I was able to [achieve outcome]."
(Show before/after or the completed result)

[4:00-4:30] CTA
"Download [App Name] from the link in the description."
"If this was helpful, subscribe for more [category] content."
```

### YouTube SEO Checklist

- Title: Include target keyword naturally — "[How to Task] with [App Name]"
- Description: First 2 lines should contain keyword and download link
- Tags: 5-10 relevant tags including app name, category, and problem keywords
- Thumbnail: Phone mockup + text overlay + bright color background
- Chapters: Add timestamps for each section

## Referral Program Design Patterns

### In-App Referral Flow

```
Trigger moment → Share prompt → Personalized link → Invitee onboarding → Reward delivery

Step 1: Detect trigger moment
- User completes first [achievement]
- User hits [milestone]
- User rates app positively (4-5 stars in in-app prompt)

Step 2: Show share prompt
"Love [App Name]? Share it with a friend and you both get [reward]."
[Share Button] [Maybe Later]
(Never block the user — always offer dismissal)

Step 3: Generate personalized link
- Deep link that tracks referrer
- Link opens App Store with attribution
- Fallback to landing page for web users

Step 4: Invitee onboarding
- When invitee installs and opens, show: "You were invited by [Referrer Name]!"
- Fast-track onboarding for referred users (they have higher intent)

Step 5: Deliver rewards
- Reward BOTH referrer and invitee
- Deliver immediately upon qualifying action (install, signup, or first use)
- Show confirmation notification to referrer
```

### Incentive Structures

| Incentive               | Works Best For          | Example                                |
| ----------------------- | ----------------------- | -------------------------------------- |
| Premium trial extension | Subscription apps       | "7 extra days of Pro for each friend"  |
| In-app currency         | Games, marketplace apps | "500 coins for each referral"          |
| Feature unlock          | Freemium apps           | "Unlock [feature] after 3 referrals"   |
| Donation                | Mission-driven apps     | "We'll plant a tree for each referral" |

## Email & Push Notification Templates

### Re-Engagement Push Notification Copy

**D2 (missed Day 1 return):**

```
Title: You left off at [last state]
Body: Pick up where you stopped — [specific context from their last session].
```

**D8 (churned after first week):**

```
Title: Have you tried [feature they haven't used]?
Body: [One sentence benefit of that feature]. Tap to explore.
```

**D31 (monthly churn):**

```
Title: New in [App Name]: [latest feature]
Body: We shipped [feature] this month. Here's what it does for you.
```

**D91 (long-term churn):**

```
Title: We've missed you, [Name]
Body: [App Name] has changed a lot since you last visited. Come see what's new — [incentive if applicable].
```

### Push Notification Timing Rules

- Send during user's historically active hours (track per user)
- Default window if no data: 10 AM - 8 PM in user's timezone
- Maximum: 2 push notifications per day
- Space notifications at least 4 hours apart
- Never send between 10 PM and 8 AM unless the app is alarm/time-critical

### Lifecycle Email Sequence

**Email 1 (Day 0 — Welcome):**

```
Subject: Welcome to [App Name] — here's how to get the most out of it

Body:
- Thank them for downloading
- 3 quick tips to get started
- Link to the best tutorial or guide
- Support contact info
```

**Email 2 (Day 3 — Value Reinforcement):**

```
Subject: Did you know [App Name] can [surprising feature]?

Body:
- Highlight a feature they likely haven't found
- Include a GIF or screenshot showing how to use it
- Social proof: "[X] users do this every day"
```

**Email 3 (Day 7 — Social Proof):**

```
Subject: Why [number] people use [App Name] every day

Body:
- 2-3 user testimonials or success stories
- App Store review highlights
- CTA: rate the app if they're enjoying it
```

**Email 4 (Day 14 — Upgrade/Expand):**

```
Subject: Ready for more? Here's what [Premium/Pro] unlocks

Body:
- List premium features with benefits
- Offer limited-time discount for upgrading
- Include comparison table (free vs. premium)
```

**Email 5 (Day 30 — Re-engagement):**

```
Subject: It's been a while — here's what's new in [App Name]

Body:
- Summary of new features or improvements
- Personal note from the founder
- Incentive to return (extended trial, discount)
```

---

## Reference: Paid Acquisition

# Paid Acquisition Playbook

## Apple Search Ads Setup

### Account Setup

1. Go to searchads.apple.com and sign in with the Apple ID linked to App Store
   Connect
2. Add payment method (credit card or Apple Ads credit)
3. Create the first campaign group named after the app

### Campaign Structure

Create 4 campaigns, each with a distinct purpose:

#### Campaign 1: Brand Defense (10% of budget)

**Purpose:** Capture users searching for the app by name. Prevent competitors
from stealing brand searches.

- **Match type:** Exact match
- **Keywords:** app name, app name variations, common misspellings
- **Default bid:** $0.50-1.00 (brand terms are cheap)
- **Negative keywords:** none needed

**Example for a fitness app called "FitTrack Pro":**

```
Keywords: "fittrack pro", "fittrackpro", "fit track pro", "fittrack"
Bid: $0.50
Daily budget: $1-2
```

#### Campaign 2: Competitor Conquest (20% of budget)

**Purpose:** Show ads when users search for competing apps.

- **Match type:** Exact match
- **Keywords:** competitor app names, competitor brand terms
- **Default bid:** $1.00-3.00 (competitive, higher CPT)
- **Negative keywords:** add brand terms to avoid overlap

**How to find competitor keywords:**

1. Search App Store for the app's primary category
2. Note the top 20 apps in the category
3. Add each competitor name as an exact match keyword
4. Monitor which ones convert and prune those that don't after 100 impressions

**Example:**

```
Keywords: "myfitnesspal", "strava", "nike training", "peloton app"
Bid: $2.00
Daily budget: $3-4
```

#### Campaign 3: Category/Generic (40% of budget)

**Purpose:** Capture users searching for a type of app, not a specific one.

- **Match type:** Broad match and exact match (separate ad groups)
- **Keywords:** category terms, problem-based phrases, use-case phrases
- **Default bid:** $0.75-2.00
- **Negative keywords:** competitor names (handled in Campaign 2), irrelevant
  terms

**Keyword research process:**

1. List 10 ways someone would describe the app's function
2. Use Apple Search Ads keyword suggestions tool
3. Check App Store search suggestions (type partial words)
4. Review competitor App Store descriptions for keyword ideas

**Example:**

```
Exact match ad group:
"fitness tracker", "workout app", "exercise log", "gym tracker"
Bid: $1.50

Broad match ad group:
"fitness tracker", "workout app"
Bid: $1.00 (lower because broad match is less targeted)
```

#### Campaign 4: Discovery (30% of budget)

**Purpose:** Find new keywords Apple's algorithm suggests.

- **Match type:** Search Match (automatic)
- **Default bid:** $0.50-1.50
- **Negative keywords:** ALL keywords from Campaigns 1-3 (to avoid overlap)
- **Strategy:** Mine this campaign weekly for converting keywords, then move
  them to the appropriate campaign

### Bid Optimization Process

**Week 1-2: Data gathering**

- Set bids at the midpoint of suggested range
- Do not change bids — let data accumulate
- Need minimum 100 impressions per keyword to evaluate

**Week 3+: Optimization cycle (run weekly)**

| Metric                         | Action                                               |
| ------------------------------ | ---------------------------------------------------- |
| CPA < target, high impressions | Increase bid 10-20% to get more volume               |
| CPA < target, low impressions  | Increase bid 20-30% to compete for more auctions     |
| CPA > target, high impressions | Decrease bid 10-20%                                  |
| CPA > target, low impressions  | Pause keyword — not enough volume at any price       |
| High impressions, low taps     | Improve ad creative (custom product pages)           |
| High taps, low installs        | Improve App Store listing (screenshots, description) |

**Target CPA formula:**

```
Target CPA = LTV × target ROI ratio

Example:
- LTV = $15
- Target 3x ROI
- Target CPA = $15 / 3 = $5
```

### Creative Set Optimization

Apple Search Ads pull screenshots from the App Store listing. Optimize with
Custom Product Pages:

1. Create 3-4 Custom Product Pages in App Store Connect
2. Each page targets a different audience segment with different screenshot sets
3. Assign each Custom Product Page to the relevant ad group

**Example product page variants:**

- **Variant A (Beginners):** Screenshots showing ease of setup, simple UI
- **Variant B (Power Users):** Screenshots showing advanced features,
  integrations
- **Variant C (Social Proof):** Screenshots with review quotes, user count,
  awards

### Budget Pacing

**$5/day budget ($150/month):**

```
Brand: $0.50/day
Competitor: $1.00/day
Category: $2.00/day
Discovery: $1.50/day
```

**$10/day budget ($300/month):**

```
Brand: $1.00/day
Competitor: $2.00/day
Category: $4.00/day
Discovery: $3.00/day
```

**$20/day budget ($600/month):**

```
Brand: $2.00/day
Competitor: $4.00/day
Category: $8.00/day
Discovery: $6.00/day
```

## Google Ads for Apps (Universal App Campaigns)

### When to Use Google Ads vs. Apple Search Ads

| Factor            | Apple Search Ads           | Google UAC                         |
| ----------------- | -------------------------- | ---------------------------------- |
| Platform          | iOS only                   | Android + iOS                      |
| Targeting control | High (keyword level)       | Low (algorithmic)                  |
| Creative control  | Limited (App Store assets) | More options (text, video, images) |
| Best for          | High-intent users          | Volume at lower CPA                |
| Minimum budget    | $5/day                     | $10-20/day recommended             |

### Google UAC Setup

1. Create a Google Ads account linked to Google Play Console (or App Store for
   iOS)
2. Select "App promotion" campaign type
3. Choose optimization goal:
   - **Install volume** — start here to build data
   - **In-app actions** — switch after 100+ conversions
   - **ROAS** — switch after 500+ conversions with revenue data

### Asset Requirements

Provide Google with:

- **Text ideas:** 5 headlines (30 char max), 5 descriptions (90 char max)
- **Images:** 3-5 images in landscape (1200x628), portrait (1200x1500), and
  square (1200x1200)
- **Videos:** 1-3 videos (landscape and portrait) — 15-30 seconds
- **HTML5 ads:** optional, for interactive ads

**Headline formulas:**

```
"[Solve Problem] in [Time]"
"Free [App Category] App"
"[Number] [Users/Reviews] Love [App Name]"
"Try [App Name] — [Key Benefit]"
"[Action Verb] [Outcome] Today"
```

### Budget and Bidding

- Set target CPI (cost per install) at 80% of target — Google's algorithm learns
  and optimizes
- Minimum budget: 10x target CPI per day
- Allow 2 weeks for the algorithm to learn before adjusting

**Example:**

```
Target CPI: $2.00
Set bid: $1.60
Daily budget: $20 (10 × $2.00)
Learning period: 14 days
```

### Optimization Cadence

| Week | Action                                                                |
| ---- | --------------------------------------------------------------------- |
| 1-2  | Do not touch. Let algorithm learn.                                    |
| 3    | Review CPI and conversion rate. If CPI > 2x target, lower bid 10%.    |
| 4    | Add or replace worst-performing text/image assets.                    |
| 5-6  | If hitting CPI target, increase budget 20-30%.                        |
| 7-8  | Switch optimization goal to in-app actions if enough conversion data. |

---

## Reference: Product Hunt Playbook

# Product Hunt Launch Playbook

## 2-Week Preparation Timeline

### Week 1 (14-8 days before launch)

**Day 14: Account & Asset Preparation**

- Create or update Product Hunt maker profile with real photo, bio, and social
  links
- Prepare all visual assets:
  - Gallery images: 5-6 images (1270x760px), first image is most important
  - Logo: 240x240px, clean on white background
  - Animated GIF: optional but significantly boosts engagement
- Write tagline (60 char max) — focus on benefit, not feature

**Day 13: Hunter Selection**

- Option A: Self-hunt (fine if you have a network; no algorithmic penalty)
- Option B: Find a hunter with 1,000+ followers

**Hunter Outreach Template:**

```
Subject: Would you hunt [App Name] on Product Hunt?

Hi [Hunter Name],

I've been following your Product Hunt activity — you clearly have great taste in [category] products.

I'm launching [App Name], which [one-sentence value prop]. [One specific metric or proof point, e.g., "We have 2,000 beta users with 45% D7 retention."]

I'd love for you to hunt it. I have all assets ready and a community of [number] people prepared to support the launch.

Would you be open to a quick 10-min call this week?

[Your name]
[Link to app / landing page]
```

**Day 12-10: Build Activation List**

- Compile a list of 50-100 people who will authentically engage on launch day
- Sources: beta users, Twitter/X followers, newsletter subscribers, friends in
  tech, indie maker communities
- Prepare a short, personalized message for each (do NOT send identical
  messages)
- Do NOT ask for upvotes — ask people to "check out the launch and share
  feedback"

**Day 9-8: Prepare Launch Day Content**

- Write the maker's comment (see template below)
- Draft 5 social media posts (Twitter/X, LinkedIn, Instagram, Threads, Mastodon)
- Prepare an email blast to existing users/newsletter
- Write a blog post about the launch story

### Week 2 (7-1 days before launch)

**Day 7: Select Launch Day**

- Best days: Tuesday, Wednesday, Thursday
- Avoid: Monday (competition from weekend buildup), Friday-Sunday (lower
  traffic)
- Check Product Hunt upcoming page for major competing launches
- Avoid Apple event days, major holidays, or big tech news days

**Day 5: Test Everything**

- Verify App Store / Play Store links work
- Test all gallery images render correctly
- Confirm landing page loads fast and has clear CTA
- Ensure the app is stable — no known crashes

**Day 3: Pre-notify Key Supporters**

- Send personal messages to activation list: "Launching on Product Hunt this
  [day]. I'll share the link early morning — would love your genuine feedback."
- Brief any team members on the plan

**Day 1 (Launch Eve):**

- Schedule social posts for launch morning
- Prepare email blast, ready to send
- Get a good night's sleep — launch day is long

## Launch Day Execution

### 12:01 AM PT — Go Live

- Post goes live (either you or your hunter publishes)
- Immediately post the maker's comment (see template below)
- Share the direct Product Hunt link — NOT a redirect or shortened URL

### 6:00-7:00 AM PT — Morning Push

- Send activation messages: "We're live on Product Hunt! Would love your
  thoughts: [link]"
- Send email blast
- Post on social media
- Share in relevant Slack/Discord communities (where allowed)

### Throughout the Day

- Respond to EVERY comment on the Product Hunt page within 30 minutes
- Share progress updates on social media ("We're #3 on Product Hunt right now!")
- Thank people who share or comment, personally
- Do NOT ask for upvotes — this violates PH guidelines and can get you penalized

### 11:59 PM PT — Day Ends

- Voting period ends at midnight PT
- Post a thank-you update regardless of ranking

## Maker's Comment Template

Post this as the first comment immediately after launch:

```
Hey Product Hunt! 👋

I'm [Name], the maker of [App Name].

**Why I built this:**
[2-3 sentences about the personal problem or frustration that led to building the app. Make it relatable and specific.]

**What it does:**
[3-4 bullet points of key features — focus on outcomes, not features]
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

**Where we are:**
[1-2 sentences about traction, beta feedback, or early results. Include specific numbers if possible.]

**What's next:**
[1-2 sentences about upcoming features or roadmap items you're excited about.]

I'd love to hear your feedback — especially about [specific aspect you want feedback on]. I'll be here all day responding to comments!

[Optional: special offer for PH community, e.g., "Use code PRODUCTHUNT for 50% off the first year."]
```

## Post-Launch Follow-Up (Days 2-7)

**Day 2:**

- Write a "lessons learned" Twitter/X thread about the launch
- Follow up with everyone who commented — thank them, answer questions
- Analyze traffic sources in your analytics

**Day 3-5:**

- Write a blog post: "How we launched on Product Hunt: results and lessons"
- Share results transparently (upvotes, traffic, signups, revenue impact)
- Connect with other makers who launched the same day

**Day 7:**

- Compile final metrics: upvotes, comments, website traffic, signups, downloads
- Identify which activation channels drove the most engagement
- Document lessons learned for future launches

## Common Mistakes to Avoid

1. **Asking for upvotes** — Product Hunt detects and penalizes this. Ask for
   "feedback" instead.
2. **Using URL shorteners** — PH may flag these. Use the direct producthunt.com
   link.
3. **Launching with bugs** — The PH audience is tech-savvy and will call out
   issues publicly.
4. **Ignoring comments** — Not responding makes the launch look abandoned.
5. **Launching on Friday** — Weekend traffic is significantly lower.
6. **Sending identical mass messages** — PH detects coordinated voting.
   Personalize outreach.
7. **Not having a special offer** — PH community expects an exclusive deal or
   discount.

---

## Reference: Social Media Templates

# Social Media Templates

## Reddit Launch Templates

### Subreddit Research Process

1. Search Reddit for the app's problem space (not the app category)
2. Identify subreddits where users discuss the problem the app solves
3. Check each subreddit's rules for self-promotion policies
4. Sort by subscriber count and engagement level

**Common subreddits for app launches:**

| Subreddit               | Subscribers | Self-Promo Rules          | Best For         |
| ----------------------- | ----------- | ------------------------- | ---------------- |
| r/SideProject           | 100k+       | Allowed, flair required   | Any indie app    |
| r/IndieDev              | 50k+        | Allowed with context      | Games, dev tools |
| r/EntrepreneurRideAlong | 150k+       | Journey posts welcome     | B2B, SaaS        |
| r/iOSProgramming        | 100k+       | Show-off threads          | iOS apps         |
| r/androiddev            | 200k+       | Promo in weekly thread    | Android apps     |
| r/startups              | 1M+         | Share Your Startup thread | Any startup      |
| r/AppIdeas              | 50k+        | Show completed apps       | Any app          |
| r/InternetIsBeautiful   | 17M+        | No self-promo             | Web apps/tools   |

### Soft Launch Post Template (r/SideProject)

```
Title: I built [App Name] to solve [specific problem] — looking for feedback

Hey everyone,

For the past [time period], I've been working on [App Name] because [personal reason/frustration].

**The problem:** [2-3 sentences describing the problem you experienced personally]

**What I built:** [Brief description of the app — what it does, not how it works]

**Key features:**
- [Feature 1 framed as benefit]
- [Feature 2 framed as benefit]
- [Feature 3 framed as benefit]

**Current state:** [Beta/launched, number of users if impressive, any metrics]

**What I'd love feedback on:**
1. [Specific question about UX/feature/pricing]
2. [Specific question about the value prop]

Here's the link: [App Store / Play Store / website link]

I'm happy to answer any questions about the tech stack, growth, or anything else. Thanks for checking it out!
```

### Journey/Story Post Template (r/EntrepreneurRideAlong)

```
Title: Month [X] building [App Name]: [specific milestone or metric]

Quick update on my journey building [App Name].

**Background:** [1-2 sentences on what the app does]

**This month's numbers:**
- Downloads: [number] (up/down X% from last month)
- Revenue: $[amount]
- Retention: [D7 rate]
- Key learning: [one insight]

**What worked:**
- [Tactic 1 with specific result]
- [Tactic 2 with specific result]

**What didn't work:**
- [Failed tactic with honest reflection]

**Next month's focus:**
- [Goal 1]
- [Goal 2]

Happy to answer questions about [specific topic]. Link in my profile if you want to check it out.
```

### Comment-First Strategy Template

Before posting about the app, spend 2 weeks being genuinely helpful:

1. Answer questions in the niche subreddit (10-15 helpful comments)
2. Share insights without mentioning the app
3. Build a comment history that shows expertise
4. Only then post about the app — the community will recognize the name

## TikTok/Reels Content Templates

### Video Script Template 1: "POV Discovery"

```
[HOOK - 2 seconds]
(Text overlay: "POV: you find an app that [solves problem]")
(Show phone screen, hand picking it up)

[PROBLEM - 3 seconds]
(Text overlay: "When you're tired of [frustrating manual process]")
(Show the frustrating old way — spreadsheet, paper, slow process)

[DEMO - 10 seconds]
(Screen recording of app with zoom-ins on key features)
(Text overlays highlighting each step)
Step 1: [Action] → (show result)
Step 2: [Action] → (show result)
Step 3: [Action] → (show result)

[RESULT - 3 seconds]
(Text overlay: "What used to take [old time] now takes [new time]")
(Show the final result / output)

[CTA - 2 seconds]
(Text overlay: "[App Name] — link in bio")
(Point to bio or show App Store icon)
```

### Video Script Template 2: "Game Changer"

```
[HOOK - 2 seconds]
(Face to camera, excited expression)
"This app is a GAME CHANGER for [audience]"

[PROBLEM - 3 seconds]
"I used to spend [time] doing [task] every [frequency]"
(Show frustrated gesture or old method)

[DEMO - 10 seconds]
"Watch this..."
(Screen recording: show the core workflow in 3 steps)
(Use zoom-ins and annotations)
(Add satisfying sound effect on key moments)

[RESULT - 3 seconds]
"Now it takes me [short time] and it's [better outcome]"
(Show before/after comparison if possible)

[CTA - 2 seconds]
"Search [App Name] on the App Store"
(Show App Store search result)
```

### Video Script Template 3: "Stop/Start"

```
[HOOK - 2 seconds]
(Text overlay: "STOP [old way of doing thing]")
(Show X or stop gesture)

[PROBLEM - 3 seconds]
(Text overlay: "This is what most people do...")
(Quick montage of the painful old way)

[DEMO - 10 seconds]
(Text overlay: "START using [App Name]")
(Clean demo of the app solving the problem)
(Highlight 2-3 key moments with zoom + sound)

[RESULT - 3 seconds]
(Side by side or before/after)
(Text overlay showing time/money/effort saved)

[CTA - 2 seconds]
(Text overlay: "Link in bio 🔗")
```

### Posting Strategy

**Frequency:** 3-5 videos per week minimum for first 8 weeks

**Best posting times (in user's primary timezone):**

- Weekdays: 7-8 AM, 12-1 PM, 7-9 PM
- Weekends: 9-11 AM, 7-9 PM

**Hashtag strategy (TikTok):**

- 3-5 hashtags per post (not 30)
- Mix of sizes: 1 large (1B+ views), 2 medium (100M-1B), 2 niche (<100M)
- Always include: #app #[appcategory] #tech
- Rotate niche tags based on content angle

**Example hashtag sets:**

Productivity app:

```
#productivityapp #productivityhack #techtools #organizeyourlife #appsworthdownloading
```

Fitness app:

```
#fitnessapp #workouttips #fittech #gymlife #appsthathelp
```

Creative app:

```
#creativeapp #designtools #digitalart #creatortool #appsworthit
```

### Content Calendar Framework

| Day | Content Type                         | Goal             |
| --- | ------------------------------------ | ---------------- |
| Mon | POV Discovery                        | Hook new viewers |
| Wed | Tutorial/How-to                      | Show depth       |
| Fri | Before/After or Results              | Social proof     |
| Sat | Behind the scenes / Building journey | Build connection |

## Twitter/X Thread Templates

### Launch Announcement Thread

```
Tweet 1:
I just launched [App Name] 🚀

After [time period] of building, it's live on the [App Store / Play Store].

Here's the story of why I built it and what I learned:

🧵👇

Tweet 2:
The problem:
[Describe the problem in relatable terms]

I was spending [X hours/week] doing [task] and thought "there has to be a better way."

Spoiler: there wasn't. So I built one.

Tweet 3:
What [App Name] does:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

[Screenshot or GIF of the app]

Tweet 4:
The tech stack (for the builders out there):
- [Framework/language]
- [Backend/infrastructure]
- [Notable libraries or services]

Total cost to build and launch: $[amount]

Tweet 5:
Early results:
- [Metric 1]
- [Metric 2]
- [Metric 3]

[If you have a graph or chart, include it]

Tweet 6:
What's next:
- [Upcoming feature 1]
- [Upcoming feature 2]
- [Upcoming feature 3]

If you want to try it: [link]

I'd love feedback from this community. What would make this useful for you?
```

### Weekly Build-in-Public Thread

```
Tweet 1:
Week [X] building [App Name]:

📊 [Key metric] → [number]
💰 [Revenue metric] → $[amount]
📱 [User metric] → [number]

Biggest win and biggest failure this week:
🧵

Tweet 2:
WIN: [Describe what worked]
[Include specific numbers]

Tweet 3:
FAIL: [Describe what didn't work]
[Include honest reflection and what you'd do differently]

Tweet 4:
This week I'm focused on:
- [Priority 1]
- [Priority 2]

Follow along if you're interested in [topic] 🤙
```
