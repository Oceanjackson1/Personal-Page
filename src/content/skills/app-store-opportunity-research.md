---
title: "App Store Opportunity Research"
description: "Full-pipeline mobile app opportunity research for iOS App Store and Google Play Store. Discovers underserved niches, analyzes competitor gaps, produces revenue-validated top-3 opportunity reports, writes MVP PRDs, and builds working prototypes on ..."
category: "devops"
source: "community"
author: "Community"
tags: ["app", "store", "opportunity", "research"]
date: 2026-03-20
---

## Prerequisites

- **Chrome browser** with Claude in Chrome extension (for store browsing)
- **Rork account** at [rork.com](https://rork.com/) (for prototype building,
  optional)
- No API keys required — all research is done through live browser interaction
- Supports **iOS App Store**, **Google Play Store**, or **both** platforms

## Pipeline Overview

```
1. Define Category
2. App Store Charts
3. Community & Demand Research
4. Competitor Deep-Dive
5. Gap Analysis
6. Score & Rank
7. Top 3 Report
8. Quick Validation (optional)
9. MVP PRD
10. Rork Prototype (optional)
```

---

## Step 1: Define the Category

Ask the user what space they want to explore. Help them narrow down:

- **Too broad:** "Health apps" (thousands of competitors)
- **Good:** "Sleep + anxiety apps for consumers" (specific intersection)
- **Good:** "Habit tracking for fitness beginners" (audience + niche)
- **Good:** "AI-powered journaling apps" (tech angle + category)

**Key questions to ask:**

1. What category or problem space interests you?
2. **Target platform?** iOS, Android, or both?
   - **iOS only:** Higher revenue per user, research via App Store charts
   - **Android only:** Larger user base, unique categories (Personalization,
     Tools), research via Google Play charts
   - **Both:** Cross-platform framework recommended (React Native/Expo or
     Flutter), research both stores for the fullest picture
3. Consumer or B2B? (Consumer is easier to validate quickly)
4. Any budget constraints? (No-AI = cheaper to build, AI = higher ceiling)
5. Target revenue? ($1K/mo hobby vs $10K/mo business)

---

## Step 2: Store Charts Research

Browse the charts for the user's target platform(s) using Chrome. Research both
stores when targeting both platforms — the competitive landscape often differs.

### iOS App Store

1. **Navigate to:**
   `https://apps.apple.com/us/charts/iphone/{category-slug}/{category-id}`

   **Apps:**
   - Books: `/books-apps/6018`
   - Business: `/business-apps/6000`
   - Education: `/education-apps/6017`
   - Entertainment: `/entertainment-apps/6016`
   - Finance: `/finance-apps/6015`
   - Food & Drink: `/food-drink-apps/6023`
   - Graphics & Design: `/graphics-design-apps/6027`
   - Health & Fitness: `/health-fitness-apps/6013`
   - Lifestyle: `/lifestyle-apps/6012`
   - Medical: `/medical-apps/6020`
   - Music: `/music-apps/6011`
   - Navigation: `/navigation-apps/6010`
   - News: `/news-apps/6009`
   - Photo & Video: `/photo-video-apps/6008`
   - Productivity: `/productivity-apps/6007`
   - Reference: `/reference-apps/6006`
   - Shopping: `/shopping-apps/6024`
   - Social Networking: `/social-networking-apps/6005`
   - Sports: `/sports-apps/6004`
   - Travel: `/travel-apps/6003`
   - Utilities: `/utilities-apps/6002`
   - Weather: `/weather-apps/6001`

   **Games:**
   - Action: `/action-games/7001`
   - Adventure: `/adventure-games/7002`
   - Board: `/board-games/7004`
   - Card: `/card-games/7005`
   - Casino: `/casino-games/7006`
   - Puzzle: `/puzzle-games/7012`
   - Racing: `/racing-games/7013`
   - Role-Playing: `/role-playing-games/7014`
   - Simulation: `/simulation-games/7016`
   - Sports: `/sports-games/7017`
   - Strategy: `/strategy-games/7018`
   - Trivia: `/trivia-games/7019`
   - Word: `/word-games/7020`

### Google Play Store

If targeting Android, see [references/google-play.md](references/google-play.md)
for the full category list, chart URLs, and Android-specific data points. Google
Play exposes install counts directly (more useful than iOS rating-count
proxies).

### For Both Platforms

2. **Document the top 25-50 apps** on each target store, noting:
   - App name and position
   - Rating count (proxy for install base)
   - Star rating
   - Price/monetization model
   - Brief description

3. **Identify patterns:**
   - Which apps have massive ratings (>100K)? These are saturated.
   - Which apps have moderate ratings (1K-50K)? Proven demand, beatable.
   - Which apps have low ratings (<500)? Possible new/underserved niche.

---

## Step 3: Community & Demand Research

Before deep-diving into competitors, validate that real demand exists outside
the App Store. See
[references/research-sources.md](references/research-sources.md) for detailed
search patterns and sources.

### Reddit & Forum Research

Search Reddit for unmet demand signals in the category. Look for:

- "Is there an app that..." posts with no good answer
- Complaints about existing apps (pain points users will pay to escape)
- Feature requests with high upvotes
- "I switched from X to Y because..." (switching triggers)

### Google Trends Validation

Check Google Trends for the core problem keywords:

- **Rising trend** = growing demand, may not be saturated
- **Declining trend** = caution, avoid unless you have a unique angle
- Note seasonal patterns to time your launch

### Cross-Platform Gap Detection

Check for opportunities invisible from a single store:

- Apps successful on one platform but weak on the other (e.g., strong on Android
  with 1M+ installs but no quality iOS equivalent, or vice versa)
- Popular web tools (Product Hunt, AlternativeTo) without native mobile apps
- Top apps in other countries not yet available in the US

### Indie Revenue Intelligence

Search IndieHackers and Twitter (#buildinpublic) for real revenue data from solo
devs and small teams in the category. Real numbers beat estimates.

---

## Step 4: Competitor Deep-Dive

For each promising niche area, deep-dive into 5-8 competitor apps:

### Data to Collect Per App

| Field                  | How to Find                                                   |
| ---------------------- | ------------------------------------------------------------- |
| Name                   | Store listing                                                 |
| Ratings count          | Store listing (Google Play also shows install count directly) |
| Star rating            | Store listing                                                 |
| Price / subscription   | Store listing                                                 |
| Last updated           | Store listing — stale (6+ months) = vulnerable                |
| App size               | Store listing — bloated (200MB+) = simplifier opportunity     |
| Dev replies to reviews | Store reviews — silence = likely abandoned                    |
| Trustpilot score       | Search `{app name} trustpilot`                                |
| Estimated revenue      | Search `{app name} revenue` or use web research               |
| Key features           | Store description / screenshots                               |
| Top complaints         | 1-star reviews on store and Trustpilot                        |
| Missing features       | Compare across competitors                                    |

### Systematic Review Mining

For each competitor, read the 10 most recent 1-star and 2-star reviews on the
target store(s). Categorize complaints into:

- **Bugs/crashes** — Technical issues (less useful for opportunity finding)
- **Missing features** — "I wish it had..." (direct feature gap signals)
- **UX frustration** — "Too complicated", "Can't find..." (design opportunity)
- **Pricing complaints** — "Too expensive for what it does" (pricing
  opportunity)
- **Broken promises** — "Doesn't do what it says" (trust/quality opportunity)

The most valuable complaints are **missing features** and **UX frustration** —
these are problems you can solve. If the same complaint appears across 3+
competitors, you've found a validated gap.

### Revenue Estimation Techniques

- **Direct sources:** Search "{app name} revenue", "{app name} ARR"
- **Proxy calculation:** `rating_count * 40-80 = approximate installs` (rule of
  thumb)
- **Industry benchmarks:** 2-5% of free users convert to paid
- **Comparable apps:** Find similar apps with known revenue

### Red Flags (Avoid These Niches)

- Top app has 1M+ ratings (dominated by a giant)
- Category requires hardware integration (Apple Watch data, etc.)
- Heavy regulation (medical devices, financial trading)
- All competitors are free with no monetization path

### Green Flags (Pursue These Niches)

- Top competitors have poor reviews (< 3.0 Trustpilot)
- Solo devs making $50K+/yr (proves indie viability)
- Editors' Choice / Editor's Pick app exists with low ratings (store promotes
  the niche)
- Users complain about the same missing feature across multiple apps
- Clear $5-15/mo willingness to pay

### Opportunity Archetypes

When analyzing competitors, identify which archetype fits the opportunity. This
sharpens positioning and guides the PRD:

| Archetype              | Signal                                           | Your Play                                    |
| ---------------------- | ------------------------------------------------ | -------------------------------------------- |
| **The Simplifier**     | Market leader is bloated, 200MB+, does too much  | Focused app that does 1 thing perfectly      |
| **The Privacy Play**   | Competitors harvest data, require accounts       | Privacy-first, local-only, no account needed |
| **The Design Upgrade** | Competitors are functional but visually dated    | Same core features, premium modern UI        |
| **The Unbundler**      | Big app has 10 features, users only need 2       | Extract the 2 features into a clean app      |
| **The Combiner**       | Users always pair 2 separate apps together       | Merge them into one seamless experience      |
| **The Localizer**      | App thrives in other countries, no US equivalent | Bring the validated concept to a new market  |

Most successful indie apps fit one or more of these archetypes. Name the
archetype in the opportunity report — it clarifies the "why you win" story.

---

## Step 5: Gap Analysis

Create a **feature comparison matrix** across the top competitors:

```markdown
| Feature         | App A  | App B | App C | App D | YOUR APP |
| --------------- | ------ | ----- | ----- | ----- | -------- |
| Core Feature 1  | Yes    | Yes   | No    | Yes   | YES      |
| Core Feature 2  | No     | Yes   | Yes   | No    | YES      |
| Missing Feature | No     | No    | No    | No    | YES      |
| Price           | $14.99 | $9.99 | Free  | $6.99 | $5.99    |
| UX Quality      | Poor   | Good  | OK    | Good  | Premium  |
```

The winning opportunity is where:

1. Multiple competitors exist (proven demand)
2. They all miss the same 1-2 features
3. Users vocally complain about the gap
4. Pricing is high enough to support indie revenue

---

## Step 6: Score & Rank Opportunities

Before writing the final report, score each candidate opportunity using the
structured rubric in
[references/scoring-framework.md](references/scoring-framework.md). Score on 5
dimensions (1-5 each): Market Demand, Competition Weakness, Revenue Potential,
Build Feasibility, and Differentiation Clarity. Total score determines rank.

Present the scorecard to the user alongside the top 3 report.

---

## Step 7: Top 3 Opportunity Report

Produce a ranked report with this structure:

```markdown
# Top 3 App Opportunities in {Category}

## Opportunity Scorecard

| Dimension            | Opp 1: {Name} | Opp 2: {Name} | Opp 3: {Name} |
| -------------------- | ------------- | ------------- | ------------- |
| Market Demand (1-5)  |               |               |               |
| Competition Weakness |               |               |               |
| Revenue Potential    |               |               |               |
| Build Feasibility    |               |               |               |
| Differentiation      |               |               |               |
| **TOTAL**            |               |               |               |

## Opportunity 1: {App Name} (RECOMMENDED)

**Archetype:** {Simplifier / Privacy Play / Design Upgrade / Unbundler /
Combiner / Localizer} **One-line pitch:** {What it does in 10 words} **The
gap:** {What's missing in the market} **Target user:** {Who and why they'd pay}
**Revenue model:** {Price point and conversion assumptions} **Revenue path:**
{How to reach $X/mo} **Competition:** {Who exists, why you win} **Build
complexity:** {Low/Medium/High} **Confidence:** {High/Medium/Low with reasoning}

## Opportunity 2: {App Name}

{Same fields as above}

## Opportunity 3: {App Name}

{Same fields as above}

## Recommendation

{Why #1 is the best bet, with specific reasoning}
```

**Present this to the user and get their pick before proceeding.**

---

## Step 8: Quick Validation (Optional)

Before investing in a full PRD, suggest a lightweight smoke test to de-risk the
chosen opportunity:

- **Reddit validation post:** Post in a relevant subreddit describing the
  concept and ask if people would use/pay for it. Frame as "I'm thinking about
  building X — would this solve your problem?"
- **Landing page test:** Create a simple one-page site describing the app with
  an email signup. Use Carrd, Framer, or a single HTML page. Run for 3-7 days.
- **Twitter/X poll:** Post a poll describing the problem and 3-4 solution
  approaches. See which resonates.

Skip this step if: the user wants to move fast, the opportunity scored 20+, or
strong demand evidence already exists from Step 3.

---

## Step 9: Write the MVP PRD

Once the user selects an opportunity, write a comprehensive PRD with these
sections:

1. **Executive Summary** — One paragraph pitch, name the opportunity archetype
2. **Market Opportunity** — Problem, market size, competitive landscape table,
   revenue validation
3. **Target Users** — 3 personas with name, age, job, pain points, willingness
   to pay
4. **MVP Feature Set** — 5-8 feature groups with detailed specs, UI behavior,
   edge cases
5. **Screen Map** — All screens listed with parent/child relationships
6. **Onboarding Flow** — First-time user experience step by step: what the user
   sees on first launch, how many screens before value delivery, what
   permissions are requested and when, how the app demonstrates its core value
   within 60 seconds. This is the single biggest factor in retention.
7. **User Flow** — Primary user journey from onboarding to daily use
8. **Monetization** — Free vs Premium feature split, pricing, trial strategy
9. **Tech Stack** — Framework, libraries, state management, persistence. For
   Android-specific or cross-platform options, see
   [references/google-play.md](references/google-play.md)
10. **AI Features** — If applicable, what AI does and doesn't do
11. **Data Models** — TypeScript interfaces for core entities
12. **Design Direction** — Color palette (with hex codes), typography, component
    style, mood
13. **Store Listing (ASO)** — Optimized for discoverability. Write for each
    target platform:
    - **App name** (30 char max both platforms) — include primary keyword
    - **iOS subtitle** (30 char max) / **Google Play short description** (80
      char max) — reinforce value proposition
    - **iOS keywords** (100 char max, comma-separated) — Google Play has no
      keyword field; instead optimize the full description for search terms
    - **First 3 lines of description** — these show before "more" tap, must hook
      immediately
    - **Screenshot strategy** — what each screenshot should show (iOS: max 10,
      Google Play: max 8 per device type)
    - **Google Play feature graphic** (1024x500) — required, prominently
      displayed
    - See [references/google-play.md](references/google-play.md) for full ASO
      comparison between platforms
14. **Launch Strategy** — Week 1-12 plan, marketing channels, content strategy
15. **Success Metrics** — KPIs with specific targets
16. **Risks & Mitigations** — Top 5 risks with solutions
17. **Compliance** — Privacy, data handling, App Store / Google Play guidelines
18. **Future Roadmap** — V2, V3 features beyond MVP

**Save the PRD as:** `PRD-{AppName}.md`

---

## Step 10: Build on Rork (Optional)

If the user has a Rork account, build a working prototype:

1. **Navigate to** [rork.com](https://rork.com/)
2. **Select model:** Opus 4.6 (or latest available)
3. **Write the prompt** — Condense the PRD into a detailed Rork prompt covering:
   - App name and purpose (1 sentence)
   - Design system (colors with hex codes, card styles, corner radii,
     typography)
   - Navigation structure (tab names, icons)
   - Each tab/screen with specific UI elements
   - Modal screens with full interaction specs
   - State management approach and mock data
   - Tech stack (Expo SDK, TypeScript, key libraries)
4. **Submit and monitor** the build (typically 5-10 min, 7-10 steps)
5. **Verify the preview** renders correctly (Cmd+R if stuck on loading)
6. **Share the project URL** with the user

### Rork Prompt Template

```
Build "{AppName}" — {one-line description}.

DESIGN: {Theme name}. Background: {color}. Cards: {style}.
Primary accent: {color}. Secondary accent: {color}.
Text: {color}. Corners: {radius}. Effects: {glow/shadow/glass}.

NAVIGATION: {N} tabs — {Tab1} ({icon}), {Tab2} ({icon}), ...

{TAB1 NAME} TAB:
- {Element 1 with full spec}
- {Element 2 with full spec}
...

{TAB2 NAME} TAB:
...

{MODAL SCREEN}:
...

STATE MANAGEMENT: {Approach}. Mock data for {N} days.

TECH: Expo SDK 52+, TypeScript, Expo Router, {styling}, {animations}.
```

---

## Revenue & Marketing Benchmarks

See [references/benchmarks.md](references/benchmarks.md) for revenue validation
benchmarks, pricing sweet spots, and marketing channel playbook. Reference this
when validating opportunities in Steps 5-7 and writing the launch strategy in
Step 8.

---

## Reference: Benchmarks

# Revenue & Marketing Benchmarks

## Revenue Validation Benchmarks

Use these benchmarks to reality-check opportunity viability:

| App Type            | Solo Dev Benchmark | Small Team  | Reference                    |
| ------------------- | ------------------ | ----------- | ---------------------------- |
| Niche utility       | $1-5K/mo           | $5-20K/mo   | Rootd ($1M+ total, 1 person) |
| Habit/tracker       | $5-15K/mo          | $20-80K/mo  | Daylio ($50K/mo)             |
| Gamified self-care  | $10-50K/mo         | $100K+/mo   | Finch ($2M/mo)               |
| Meditation/wellness | $5-20K/mo          | $50-500K/mo | Calm ($100M+/yr)             |
| Productivity        | $3-10K/mo          | $20-100K/mo | Various                      |
| AI-powered tool     | $5-30K/mo          | $50-300K/mo | Emerging category            |

## Pricing Sweet Spots (2025)

| Tier         | Monthly           | Annual              | Best For                 |
| ------------ | ----------------- | ------------------- | ------------------------ |
| Impulse buy  | $2.99-4.99/mo     | $19.99-29.99/yr     | Simple utilities         |
| **Standard** | **$5.99-6.99/mo** | **$34.99-44.99/yr** | **Most indie apps**      |
| Premium      | $9.99-14.99/mo    | $59.99-99.99/yr     | AI-heavy or professional |

## Marketing Channel Playbook

| Channel             | Best For                    | Cost        | Time to Results  |
| ------------------- | --------------------------- | ----------- | ---------------- |
| TikTok organic      | Consumer apps, visual demos | Free        | 2-4 weeks        |
| Reddit (niche subs) | Technical/niche apps        | Free        | 1-2 weeks        |
| Product Hunt        | Productivity/dev tools      | Free        | Launch day spike |
| Apple Search Ads    | Any iOS app                 | $0.50-3/tap | Immediate        |
| Instagram Reels     | Lifestyle/wellness apps     | Free        | 2-6 weeks        |
| Twitter/X           | Dev tools, indie hackers    | Free        | Ongoing          |

---

## Reference: Google Play

# Google Play Store Research

## Browsing Google Play Charts

### Top Charts

Browse top free/paid/grossing apps: `https://play.google.com/store/apps/top`

### Category Pages

Browse by category: `https://play.google.com/store/apps/category/{CATEGORY_ID}`

**Apps:**

| Category          | ID                  |
| ----------------- | ------------------- |
| Art & Design      | ART_AND_DESIGN      |
| Auto & Vehicles   | AUTO_AND_VEHICLES   |
| Beauty            | BEAUTY              |
| Books & Reference | BOOKS_AND_REFERENCE |
| Business          | BUSINESS            |
| Communication     | COMMUNICATION       |
| Dating            | DATING              |
| Education         | EDUCATION           |
| Entertainment     | ENTERTAINMENT       |
| Events            | EVENTS              |
| Finance           | FINANCE             |
| Food & Drink      | FOOD_AND_DRINK      |
| Health & Fitness  | HEALTH_AND_FITNESS  |
| House & Home      | HOUSE_AND_HOME      |
| Lifestyle         | LIFESTYLE           |
| Maps & Navigation | MAPS_AND_NAVIGATION |
| Medical           | MEDICAL             |
| Music & Audio     | MUSIC_AND_AUDIO     |
| News & Magazines  | NEWS_AND_MAGAZINES  |
| Parenting         | PARENTING           |
| Personalization   | PERSONALIZATION     |
| Photography       | PHOTOGRAPHY         |
| Productivity      | PRODUCTIVITY        |
| Shopping          | SHOPPING            |
| Social            | SOCIAL              |
| Sports            | SPORTS              |
| Tools             | TOOLS               |
| Travel & Local    | TRAVEL_AND_LOCAL    |
| Video Players     | VIDEO_PLAYERS       |
| Weather           | WEATHER             |

**Games:**

| Category     | ID                |
| ------------ | ----------------- |
| Action       | GAME_ACTION       |
| Adventure    | GAME_ADVENTURE    |
| Arcade       | GAME_ARCADE       |
| Board        | GAME_BOARD        |
| Card         | GAME_CARD         |
| Casino       | GAME_CASINO       |
| Casual       | GAME_CASUAL       |
| Educational  | GAME_EDUCATIONAL  |
| Music        | GAME_MUSIC        |
| Puzzle       | GAME_PUZZLE       |
| Racing       | GAME_RACING       |
| Role Playing | GAME_ROLE_PLAYING |
| Simulation   | GAME_SIMULATION   |
| Sports       | GAME_SPORTS       |
| Strategy     | GAME_STRATEGY     |
| Trivia       | GAME_TRIVIA       |
| Word         | GAME_WORD         |

### Data Differences from iOS

Google Play listings expose additional useful data:

| Field             | Notes                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| Install count     | Shown as range (e.g., "1M+") — more direct than iOS rating-count proxy |
| Last updated date | Prominently displayed — easy to spot stale apps                        |
| Requires Android  | Shows minimum API level — hints at tech debt                           |
| Content rating    | Everyone / Teen / Mature — affects audience size                       |
| In-app purchases  | Price range shown (e.g., "$0.99-$99.99 per item")                      |
| Developer website | Direct link — useful for competitor research                           |
| Similar apps      | Google's own recommendations — reveals competitive set                 |

### Country-Specific Research

Change locale with URL parameters:

- US: `?hl=en_US&gl=us`
- UK: `?hl=en_GB&gl=gb`
- Germany: `?hl=de&gl=de`
- Japan: `?hl=ja&gl=jp`
- Brazil: `?hl=pt_BR&gl=br`
- India: `?hl=en_IN&gl=in`
- South Korea: `?hl=ko&gl=kr`
- Australia: `?hl=en_AU&gl=au`

## Google Play ASO (vs iOS)

| Field             | Google Play                                   | iOS App Store                |
| ----------------- | --------------------------------------------- | ---------------------------- |
| App name          | 30 chars max                                  | 30 chars max                 |
| Short description | 80 chars max                                  | Subtitle: 30 chars max       |
| Full description  | 4,000 chars max (searchable)                  | 4,000 chars (NOT searchable) |
| Keywords          | No keyword field — extracted from description | 100 chars, comma-separated   |
| Screenshots       | Min 2, max 8 per device type                  | Max 10                       |
| Feature graphic   | Required (1024x500)                           | No equivalent                |
| Video             | YouTube link (optional)                       | App preview video (optional) |

**Key difference:** Google Play indexes the full description for search, so
keyword stuffing the description matters more than on iOS. On iOS, the keyword
field and app name are what matter.

## Android-Specific Tech Stack Options

For the PRD tech stack section, choose based on the user's situation:

### Native Android

- **Language:** Kotlin
- **UI:** Jetpack Compose
- **Architecture:** MVVM with ViewModel + StateFlow
- **DI:** Hilt / Koin
- **Persistence:** Room (SQLite), DataStore (preferences)
- **Best for:** Performance-critical apps, deep Android integration

### Cross-Platform (recommended for indie devs)

- **React Native / Expo:** JavaScript/TypeScript, largest community, works with
  Rork
- **Flutter:** Dart, excellent UI performance, growing ecosystem
- **Best for:** Shipping to both iOS and Android with one codebase

### Android-Specific Opportunities

Categories/features that are stronger opportunities on Android than iOS:

- **Personalization:** Android allows custom launchers, icon packs, widgets —
  huge category with no iOS equivalent
- **Tools/Utilities:** Android allows deeper system integration (file managers,
  default app replacement, automation)
- **Communication:** Default SMS/dialer replacement possible on Android
- **Sideloading market:** Apps rejected by Google Play can still distribute via
  APK — not possible on iOS

### Red Flags Specific to Android

- **Fragmentation:** If the app needs to work across many screen sizes and
  Android versions, testing burden is much higher
- **Lower willingness to pay:** Android users historically convert to paid at
  lower rates than iOS users (~50-70% of iOS conversion rates)
- **Piracy:** APKs are easily shared — subscription models are more defensible
  than one-time purchases on Android

---

## Reference: Research Sources

# Research Sources & Search Patterns

## Reddit Research

Reddit surfaces unmet demand that App Store charts never show.

### High-Value Search Queries

Use web search with these patterns:

```
site:reddit.com "is there an app" {category/problem}
site:reddit.com "looking for an app" {category/problem}
site:reddit.com "I wish" {competitor app name}
site:reddit.com "switched from" {competitor app name}
site:reddit.com "alternative to" {competitor app name}
site:reddit.com "{category}" app recommendation
```

### Key Subreddits by Category

| Category         | Subreddits                                                       |
| ---------------- | ---------------------------------------------------------------- |
| General app recs | r/AppRecommendations, r/iphone, r/ios, r/androidapps             |
| Productivity     | r/productivity, r/ADHD, r/GetStudying, r/bulletjournal           |
| Health & Fitness | r/fitness, r/loseit, r/running, r/meditation, r/sleep            |
| Finance          | r/personalfinance, r/YNAB, r/budgeting, r/financialplanning      |
| Mental Health    | r/anxiety, r/depression, r/selfimprovement, r/DecidingToBeBetter |
| Parenting        | r/parenting, r/daddit, r/Mommit, r/NewParents                    |
| Food & Cooking   | r/MealPrepSunday, r/EatCheapAndHealthy, r/Cooking                |
| Education        | r/learnprogramming, r/languagelearning, r/GetStudying            |
| Travel           | r/travel, r/solotravel, r/digitalnomad                           |
| Lifestyle        | r/minimalism, r/declutter, r/organization                        |

### What to Extract from Reddit

- **Unmet needs:** Posts asking "is there an app that..." with no good answer
- **Pain points:** Complaints about existing apps (features, pricing, UX)
- **Switching triggers:** Why users left one app for another
- **Willingness to pay:** Comments about pricing ("I'd pay $X for...")
- **Feature requests:** Highly upvoted feature suggestions on app subreddits

## Google Trends Validation

Before committing to an opportunity, verify search demand:

1. **Navigate to:** `https://trends.google.com/trends/`
2. **Search the core problem keyword** (e.g., "sleep tracker app", "habit
   tracker")
3. **Check 5-year trend:** Rising = green light, declining = caution, stable =
   okay
4. **Compare related terms:** See what variations are growing fastest
5. **Check seasonality:** Fitness peaks in January, tax apps in spring, etc.

### Interpreting Trends

- **Rising >50% YoY:** Strong signal — growing demand, may not be saturated yet
- **Stable:** Proven demand, but competition is likely established
- **Declining:** Avoid unless you've found a specific underserved angle
- **Seasonal spikes:** Plan launch timing around peak interest

## Cross-Platform Gap Detection

Look for opportunities where demand exists but supply is weak on iOS:

### Android → iOS Gaps

1. Browse Google Play top charts in the same category
2. Identify apps with 1M+ installs on Android
3. Search the App Store for equivalents
4. If no strong iOS equivalent exists → high-confidence opportunity

### Web → Mobile Gaps

1. Search Product Hunt for recently launched web tools in the category
2. Check if they have a native mobile app
3. Popular web tools without mobile apps = opportunity (especially if the use
   case is mobile-native)

### International → US Gaps

1. Check App Store charts in other countries (UK, Germany, Japan, South Korea)
2. Identify top apps not available or not localized for the US market
3. Successful international apps with no US presence = validated concept

### How to Browse Other Countries

Change the country code in the App Store URL:

- UK: `apps.apple.com/gb/charts/iphone/...`
- Germany: `apps.apple.com/de/charts/iphone/...`
- Japan: `apps.apple.com/jp/charts/iphone/...`
- Australia: `apps.apple.com/au/charts/iphone/...`
- Canada: `apps.apple.com/ca/charts/iphone/...`
- South Korea: `apps.apple.com/kr/charts/iphone/...`
- Brazil: `apps.apple.com/br/charts/iphone/...`
- India: `apps.apple.com/in/charts/iphone/...`

## Indie Hacker Revenue Intelligence

Real revenue data beats estimates. Search these sources:

### IndieHackers.com

```
site:indiehackers.com {category} revenue
site:indiehackers.com {app name}
```

Browse: `https://www.indiehackers.com/products` — filter by revenue range and
category.

### Twitter/X Revenue Reports

```
site:twitter.com "{category} app" "revenue" OR "MRR" OR "ARR"
site:twitter.com "{category} app" "$" "month"
```

Indie devs frequently share monthly revenue screenshots. Search for:

- `#buildinpublic {category}`
- `#indiehackers {category} revenue`

### Other Sources

- **MicroConf talks:** Search YouTube for `microconf {category}` — founders
  share detailed revenue breakdowns
- **Starter Story:** `https://www.starterstory.com/` — founder interviews with
  revenue data
- **AppFigures / Sensor Tower blogs:** Sometimes publish category revenue
  reports

## Product Hunt & Alternative Discovery

### Product Hunt

Browse `https://www.producthunt.com/` for recently launched apps in the space:

- See what's being built (market direction)
- Check upvote counts (demand signal)
- Read comments for feature requests and criticism

### AlternativeTo

Browse `https://alternativeto.net/` — search for competitor apps to find:

- What users are looking for alternatives to (dissatisfaction signal)
- Which alternatives have the most "likes" (demand signal)
- User comments explaining why they switched

---

## Reference: Scoring Framework

# Opportunity Scoring Framework

Score each opportunity on 5 dimensions (1-5 scale). Total score determines rank.

## Scoring Rubric

### 1. Market Demand (1-5)

| Score | Criteria                                                                           |
| ----- | ---------------------------------------------------------------------------------- |
| 1     | No evidence of demand; no search volume; no Reddit posts                           |
| 2     | Minimal demand; few competitors; sparse user discussion                            |
| 3     | Moderate demand; several competitors exist; some search volume                     |
| 4     | Strong demand; active Reddit/forum discussions; growing trend                      |
| 5     | Intense demand; many "is there an app for X?" posts; rising trend on Google Trends |

### 2. Competition Weakness (1-5)

| Score | Criteria                                                              |
| ----- | --------------------------------------------------------------------- |
| 1     | Dominant player with 1M+ ratings and strong reviews; no gaps          |
| 2     | Strong incumbents but with minor UX issues                            |
| 3     | Several competitors; mixed reviews; some feature gaps                 |
| 4     | Competitors have poor reviews (<3.5 stars); clear missing features    |
| 5     | Competitors are widely hated; same complaints everywhere; outdated UX |

### 3. Revenue Potential (1-5)

| Score | Criteria                                                        |
| ----- | --------------------------------------------------------------- |
| 1     | Users expect free; no monetization path; ad-only viable         |
| 2     | Low willingness to pay (<$2/mo); small addressable market       |
| 3     | Moderate pricing possible ($3-5/mo); niche but paying audience  |
| 4     | Strong pricing ($6-10/mo); competitors successfully monetize    |
| 5     | Premium pricing ($10+/mo); proven willingness to pay; large TAM |

### 4. Build Feasibility (1-5)

| Score | Criteria                                                             |
| ----- | -------------------------------------------------------------------- |
| 1     | Requires hardware, complex AI, regulatory approval, or large team    |
| 2     | Significant backend infrastructure; complex integrations             |
| 3     | Moderate complexity; standard APIs; some backend needed              |
| 4     | Mostly frontend; minimal backend; well-documented APIs               |
| 5     | Pure frontend app; simple data model; solo dev can ship in 2-4 weeks |

### 5. Differentiation Clarity (1-5)

| Score | Criteria                                                        |
| ----- | --------------------------------------------------------------- |
| 1     | No clear differentiator; "me too" product                       |
| 2     | Slightly better UX but no unique value proposition              |
| 3     | One clear differentiator but hard to communicate                |
| 4     | Strong differentiator; easy to explain in one sentence          |
| 5     | Obvious gap everyone complains about; "why doesn't this exist?" |

## Score Interpretation

| Total Score | Assessment                                                   |
| ----------- | ------------------------------------------------------------ |
| 20-25       | Strong opportunity — pursue with confidence                  |
| 15-19       | Promising — worth building if the differentiator is clear    |
| 10-14       | Marginal — only pursue if you have a unique unfair advantage |
| 5-9         | Weak — avoid unless other factors compensate                 |

## Scorecard Template

```markdown
| Dimension                  | App Idea A | App Idea B | App Idea C |
| -------------------------- | ---------- | ---------- | ---------- |
| Market Demand (1-5)        |            |            |            |
| Competition Weakness (1-5) |            |            |            |
| Revenue Potential (1-5)    |            |            |            |
| Build Feasibility (1-5)    |            |            |            |
| Differentiation (1-5)      |            |            |            |
| **TOTAL**                  |            |            |            |
```

## Tiebreaker Criteria

When two opportunities score within 2 points of each other:

1. **Personal interest** — Will the builder stay motivated for 6+ months?
2. **Speed to market** — Which can ship an MVP faster?
3. **Moat potential** — Which builds defensibility over time (network effects,
   data, brand)?
4. **Content marketing fit** — Which has a natural content/SEO angle for growth?
