---
title: "Mobile App Launch Checklist"
description: "Comprehensive step-by-step launch checklist for shipping mobile apps to the iOS App Store and Google Play Store. Covers pre-submission preparation, store asset creation, build and submission, launch day execution, and post-launch monitoring. Use w..."
category: "devops"
source: "community"
author: "Community"
tags: ["mobile", "app", "launch", "checklist"]
date: 2026-03-20
---

# Mobile App Launch Checklist

Generate a structured, actionable launch checklist tailored to the user's app,
target platform(s), and timeline. Walk through each phase sequentially, confirm
completion of critical items, and flag blockers.

## Inputs

| Input       | Required | Description                        | Default            |
| ----------- | -------- | ---------------------------------- | ------------------ |
| App name    | Yes      | Name of the app being launched     | —                  |
| Platform    | Yes      | iOS, Android, or both              | Both               |
| Launch date | No       | Target launch date                 | 4 weeks from today |
| App type    | No       | Free, freemium, paid, subscription | Freemium           |

Ask for these inputs before generating the checklist. Adjust timelines and
requirements based on the target platform.

---

## Phase 1: Pre-Submission Preparation (2-4 Weeks Before)

### App Quality

- [ ] Crash-free rate exceeds 99.5% across all supported devices
- [ ] All core user flows tested end-to-end (onboarding, purchase, key features)
- [ ] Performance benchmarks met:
  - Cold launch under 2 seconds
  - Smooth scrolling at 60fps
  - Memory usage within platform limits
  - Battery impact acceptable (no background drain)
- [ ] Accessibility audit complete (VoiceOver/TalkBack, Dynamic Type, contrast)
- [ ] Offline behavior handled gracefully (error states, cached data)
- [ ] Edge cases tested: no network, low storage, permissions denied,
      interruptions

### Privacy & Compliance

- [ ] Privacy policy URL live and accessible
- [ ] **iOS:** App Tracking Transparency prompt implemented (if tracking)
- [ ] **Android:** Data safety section completed in Google Play Console
- [ ] GDPR compliance verified (if serving EU users): consent flows, data
      deletion
- [ ] CCPA compliance verified (if serving California users)
- [ ] Data collection accurately declared on both platforms
- [ ] Third-party SDK privacy policies reviewed

### Legal

- [ ] Terms of service URL live and accessible
- [ ] EULA prepared (required if subscription or in-app purchases)
- [ ] Open source license compliance: all libraries audited, attributions
      included
- [ ] Trademark search completed for app name

### Analytics & Monitoring

- [ ] Crash reporting integrated (Firebase Crashlytics, Sentry, or Bugsnag)
- [ ] Event tracking implemented for key actions (signup, purchase, core
      features)
- [ ] Funnel definitions configured (onboarding completion, trial-to-paid)
- [ ] Real-time dashboard set up for launch day monitoring
- [ ] Alerts configured for crash rate spikes and error thresholds

### Deep Linking

- [ ] **iOS:** Universal Links configured with apple-app-site-association file
- [ ] **Android:** App Links configured with assetlinks.json
- [ ] Deep links tested from email, SMS, social media, and web
- [ ] Deferred deep linking works for new installs (if applicable)

---

## Phase 2: Store Asset Preparation

Prepare all required store assets. See platform-specific reference files for
detailed specifications:

- [references/ios-submission.md](references/ios-submission.md) — Full iOS App
  Store Connect walkthrough, screenshot specs, common rejection reasons
- [references/google-play-submission.md](references/google-play-submission.md) —
  Full Google Play Console walkthrough, asset specs, policy requirements

### iOS App Store Connect

- [ ] App icon: 1024x1024 PNG, no transparency, no rounded corners
- [ ] Screenshots prepared for required device sizes:
  - 6.7" (1290x2796) — iPhone 15 Pro Max
  - 6.5" (1284x2778) — iPhone 14 Plus
  - 5.5" (1242x2208) — iPhone 8 Plus
- [ ] App preview video recorded (optional, 15-30 seconds, H.264)
- [ ] App description written (up to 4000 characters)
- [ ] Promotional text written (up to 170 characters, editable without review)
- [ ] Keywords field populated (up to 100 characters, comma-separated)
- [ ] What's New text written for version 1.0
- [ ] Age rating questionnaire completed
- [ ] App Review Information prepared:
  - Demo account credentials (if login required)
  - Review notes explaining non-obvious features
  - Contact information for reviewer questions
- [ ] App category and subcategory selected
- [ ] Support URL configured
- [ ] Copyright field filled

### Google Play Console

- [ ] Hi-res icon: 512x512 PNG
- [ ] Feature graphic: 1024x500 PNG or JPG — **REQUIRED, prominently displayed**
- [ ] Screenshots: minimum 2, maximum 8 per device type (16:9 or 9:16)
- [ ] Short description written (up to 80 characters)
- [ ] Full description written (up to 4000 characters, optimize for search)
- [ ] What's New text written
- [ ] Content rating questionnaire completed (IARC)
- [ ] Data safety form completed
- [ ] App category and tags selected
- [ ] Contact details configured (email required, phone/website optional)
- [ ] Target audience and content declarations completed

### Both Platforms

- [ ] Store listing localized for target markets (if applicable)
- [ ] Screenshot text and captions proofread
- [ ] All URLs (privacy policy, terms, support) return 200 status
- [ ] Preview the listing as users will see it

---

## Phase 3: Build & Submit

### iOS Submission

- [ ] Archive build in Xcode with Release configuration
- [ ] Upload build via Xcode or Transporter
- [ ] Export compliance questionnaire answered (encryption usage)
- [ ] Build appears in App Store Connect (allow 15-30 minutes for processing)
- [ ] Internal TestFlight testing completed (team members)
- [ ] External TestFlight testing completed (beta testers, requires Beta Review)
- [ ] All app metadata finalized in App Store Connect
- [ ] Submit for App Review
- [ ] **Expected review time:** 24-48 hours (can be longer, plan buffer)

### Android Submission

- [ ] Signed Android App Bundle (AAB) generated — APKs no longer accepted
- [ ] ProGuard/R8 obfuscation verified (no crashes from minification)
- [ ] Internal testing track: upload and verify on real devices
- [ ] Closed testing track: distribute to beta testers
- [ ] Open testing track (optional): broader beta audience
- [ ] Pre-launch report reviewed in Google Play Console (automated testing)
- [ ] All store listing metadata finalized
- [ ] Set staged rollout percentage (start at 10-20%, NOT 100%)
- [ ] Submit for review
- [ ] **Expected review time:** hours to 7 days (new apps take longer)

### Common Rejection Reasons

Avoid these before submitting. See reference files for full lists.

**iOS top rejections:**

- Crashes or bugs during review
- Broken links (privacy policy, support URL)
- Incomplete metadata or placeholder content
- Login required without demo account provided
- Guideline 4.3: spam or duplicate app
- Guideline 2.1: app not fully functional

**Google Play top rejections:**

- Data safety form inaccurate or incomplete
- Missing privacy policy for apps requesting sensitive permissions
- Deceptive behavior (description doesn't match functionality)
- Broken core functionality
- Target audience misconfigured (apps for children have extra requirements)

---

## Phase 4: Launch Day

Follow the hour-by-hour launch day timeline in
[references/launch-day-timeline.md](references/launch-day-timeline.md) for a
detailed execution plan.

### Release Strategy

- [ ] **iOS:** Release manually (not automatically after approval) for control
- [ ] **Android:** Staged rollout at 10-20% initially
- [ ] Coordinate release timing across platforms (if launching on both)
- [ ] Choose launch time: Tuesday-Thursday, 9-10 AM in primary market timezone

### Monitoring (First 6 Hours)

- [ ] Watch crash-free rate in real-time (target: >99.5%)
- [ ] **Android:** Monitor ANR (App Not Responding) rate (target: <0.5%)
- [ ] Check App Store Connect / Play Console for review alerts
- [ ] Monitor support channels for user-reported issues
- [ ] Track download velocity against projections
- [ ] Watch first user reviews and ratings

### Support Readiness

- [ ] Prepared responses drafted for common issues:
  - Login/account problems
  - Payment/subscription questions
  - Feature explanations
  - Known issues acknowledgment
- [ ] Support team briefed on new features and known limitations
- [ ] Escalation path defined for critical issues

### Marketing Activation

- [ ] Social media posts scheduled (Twitter/X, LinkedIn, Instagram)
- [ ] Product Hunt launch prepared (if applicable — launch at 12:01 AM PT)
- [ ] Reddit posts in relevant subreddits (follow community rules)
- [ ] Press outreach sent to relevant journalists/bloggers
- [ ] Email announcement sent to waitlist/existing users
- [ ] App Store / Play Store promotional campaign activated (if using)

### Go/No-Go Decision Points

- **Halt rollout if:** crash-free rate drops below 99%, critical bug in core
  flow
- **Proceed to 50% if:** 4+ hours stable, no critical issues, reviews positive
- **Proceed to 100% if:** 24+ hours stable at 50%, metrics within targets

---

## Phase 5: Post-Launch (Week 1)

### Review Management

- [ ] Respond to every review (positive and negative) within 24 hours
- [ ] Flag and report fraudulent/spam reviews
- [ ] Categorize feedback themes for product roadmap input
- [ ] **iOS:** Implement SKStoreReviewController for in-app review prompts
      (after positive moments, max 3 times per 365 days)
- [ ] **Android:** Implement In-App Review API (after meaningful engagement)

### Crash Triage & Hotfix

- [ ] Review crash reports daily for the first week
- [ ] Prioritize crashes by user impact (affected users x severity)
- [ ] Ship hotfix within 48 hours for any crash affecting >1% of users
- [ ] **iOS:** Request expedited review for critical hotfixes
- [ ] **Android:** Use staged rollout to validate hotfix before full release

### Metrics Review

Track and review these metrics at Day 1, Day 3, and Day 7:

| Metric                   | Target | Action if Below            |
| ------------------------ | ------ | -------------------------- |
| D1 Retention             | >40%   | Review onboarding flow     |
| D7 Retention             | >20%   | Review core value delivery |
| Crash-free rate          | >99.5% | Prioritize stability fixes |
| Store rating             | >4.0   | Address top complaints     |
| Trial-to-paid conversion | >5%    | Review paywall and pricing |
| Session length           | >3 min | Review engagement hooks    |
| Onboarding completion    | >70%   | Simplify onboarding steps  |

### Feature Request & Visibility

- [ ] Submit App Store feature request to Apple editorial team (via App Store
      Connect → App Features page)
- [ ] Apply for Google Play editorial feature (via Play Console → Store presence
      → Feature request)
- [ ] Compile feature request list from user feedback for v1.1 planning
- [ ] Schedule v1.1 planning session based on launch data

---

## Generating the Checklist

When producing the checklist for the user:

1. **Tailor to platform.** Remove iOS-specific items for Android-only launches
   and vice versa. Keep both sections for cross-platform launches.
2. **Adjust timeline.** Map checklist phases to the user's actual launch date.
   Add specific dates to each phase header.
3. **Flag blockers.** Mark items that block submission (privacy policy, app
   icon, signed build) distinctly from nice-to-haves (preview video, Product
   Hunt).
4. **Save as file.** Write the completed checklist to
   `LAUNCH-CHECKLIST-{AppName}.md` in the project root.
5. **Offer to deep-dive.** After generating the checklist, ask if the user wants
   to walk through any specific phase in detail, referencing the appropriate
   reference file.

---

## Reference: Google Play Submission

# Google Play Console Submission Guide

## Account Prerequisites

- Google Play Developer account ($25 one-time fee)
- Google Play Console access at
  [play.google.com/console](https://play.google.com/console)
- Signing key managed by Google Play App Signing (recommended) or self-managed

## App Creation in Play Console

### Create the App

1. Open Google Play Console → All apps → Create app
2. Fill in:
   - App name (30 characters max)
   - Default language
   - App or Game designation
   - Free or Paid (cannot change after publishing)
3. Complete the declarations checklist before first submission

### Dashboard Setup Checklist

Google Play Console provides a setup dashboard with required steps. Complete all
items marked as mandatory before submitting:

- [ ] App access (does your app restrict access with login?)
- [ ] Ads declaration (does your app contain ads?)
- [ ] Content ratings (IARC questionnaire)
- [ ] Target audience
- [ ] News app declaration (if applicable)
- [ ] COVID-19 contact tracing / status app declaration (if applicable)
- [ ] Data safety form
- [ ] Government apps declaration (if applicable)

## Store Listing Assets

### App Icon

| Attribute | Requirement             |
| --------- | ----------------------- |
| Size      | 512 x 512 pixels        |
| Format    | PNG (32-bit with alpha) |
| File size | Up to 1024 KB           |

### Feature Graphic — REQUIRED

| Attribute    | Requirement       |
| ------------ | ----------------- |
| Size         | 1024 x 500 pixels |
| Format       | PNG or JPEG       |
| File size    | Up to 1024 KB     |
| Transparency | Not allowed       |

The feature graphic is prominently displayed on the store listing and in
promotional placements. Treat it as a billboard for the app.

**Best practices:**

- Do not place critical text in the outer 15% margins (may be cropped)
- Use bold, simple imagery that reads well at small sizes
- Include the app name and a short tagline
- Test visibility at both full size and thumbnail

### Screenshots

| Attribute     | Requirement                    |
| ------------- | ------------------------------ |
| Minimum       | 2 per device type              |
| Maximum       | 8 per device type              |
| Aspect ratio  | 16:9 or 9:16                   |
| Min dimension | 320px on shortest side         |
| Max dimension | 3840px on longest side         |
| Format        | PNG or JPEG (24-bit, no alpha) |

**Device types requiring screenshots:**

- Phone (required)
- 7-inch tablet (recommended)
- 10-inch tablet (recommended)
- Chromebook (recommended if targeting Chrome OS)

### Promotional Video

- Host on YouTube (unlisted is fine)
- Paste the YouTube URL in the store listing
- No age restriction on the video
- Keep under 2 minutes; first 30 seconds are most important
- Do not include ads in the video

## Store Listing Text

### Short Description

- Maximum 80 characters
- Appears prominently in search results and store listing
- Include primary keyword and value proposition
- Equivalent to iOS "subtitle" in prominence

### Full Description

- Maximum 4000 characters
- First 1-3 lines visible before "Read more" — make them count
- **Google Play has no keyword field** — optimize the full description for
  target search terms naturally
- Use formatting: bullet points, line breaks, emoji (sparingly)
- Include a call to action near the end

### What's New (Release Notes)

- Maximum 500 characters
- Shown to existing users considering the update
- Be specific about changes, not generic ("bug fixes and improvements")

## Content Rating (IARC)

1. Navigate to Policy → App content → Content ratings
2. Start the IARC questionnaire
3. Answer questions about: violence, sexuality, language, substances, user
   interaction, data sharing, location sharing, purchasing
4. Receive automatic rating for multiple regions:
   - ESRB (Americas)
   - PEGI (Europe)
   - USK (Germany)
   - ClassInd (Brazil)
   - GRAC (South Korea)
   - IARC Generic
5. Review and apply the ratings

**Warning:** Inaccurate responses can lead to app removal. Be thorough and
honest.

## Data Safety Form

Required for all apps. Declare:

1. **Data collection:** What types of data the app collects
   - Personal info (name, email, phone, address)
   - Financial info (purchase history, credit info)
   - Location (approximate, precise)
   - App activity (app interactions, search history)
   - Device/IDs (device ID, advertising ID)

2. **Data sharing:** What data is shared with third parties
   - Include analytics SDKs, ad networks, crash reporters

3. **Data handling practices:**
   - Is data encrypted in transit?
   - Can users request data deletion?
   - Is the app compliant with the Families policy (if targeting children)?

4. **Security practices:**
   - Data encrypted in transit (HTTPS)
   - Follows Google Play Families Policy (if applicable)

## Build Upload

### App Bundle Requirements

- **Format:** Android App Bundle (.aab) — APKs no longer accepted for new apps
- **Signing:** Enroll in Google Play App Signing (required for new apps)
- **Upload key:** Used to sign the upload; Google re-signs with the app signing
  key
- **Target API level:** Must target latest required API level (currently API 34
  / Android 14 for new apps)

### Testing Tracks

| Track      | Audience               | Review Required  | Purpose            |
| ---------- | ---------------------- | ---------------- | ------------------ |
| Internal   | Up to 100 testers      | No               | Quick team testing |
| Closed     | Invite-only, unlimited | Yes (first time) | Beta testing       |
| Open       | Anyone can join        | Yes              | Public beta        |
| Production | All users              | Yes              | Live release       |

### Upload Process

1. Select the testing track → Create new release
2. Upload the signed .aab file
3. Add release notes
4. Review and roll out

### Pre-Launch Report

Google automatically tests the uploaded build on real devices:

- Accessibility issues
- Crashes and ANRs
- Security vulnerabilities
- Performance metrics

Review the pre-launch report before promoting to production.

## Staged Rollout

### How It Works

- Set a percentage of users to receive the update
- Recommended progression: 10% → 25% → 50% → 100%
- Monitor crash rate and ANR rate at each stage
- Pause or halt rollout if issues arise

### Rollout Controls

- **Increase percentage:** Click "Edit release" → adjust percentage
- **Halt rollout:** Stops the update from reaching new users
- **Resume rollout:** Continue from where it was halted
- **Full rollout:** Release to 100% of users

### When to Halt

- Crash-free rate drops below 99%
- ANR rate exceeds 0.5%
- Critical bug reports from users in rollout
- Unexpected battery or data usage spikes

## Common Rejection Reasons and Fixes

### Policy: Deceptive Behavior

**Rejection:** App description or screenshots don't match functionality.

**Fix:** Update store listing to accurately reflect current features. Remove
claims about features not yet implemented.

### Policy: Privacy and Data Safety

**Rejection:** Data safety form doesn't match actual data collection.

**Fix:** Audit all SDKs and libraries for data collection. Update data safety
form to match reality. Add privacy policy link.

### Policy: Families

**Rejection:** App targets children but violates Families Policy.

**Fix:** If not targeting children, update target audience settings. If
targeting children, comply with COPPA and Families Policy requirements.

### Policy: Permissions

**Rejection:** App requests permissions not justified by core functionality.

**Fix:** Remove unnecessary permission requests. Provide in-context explanation
before requesting each permission. Use the least-privileged permission
available.

### Policy: Ads

**Rejection:** Ads are deceptive, interruptive, or inappropriate.

**Fix:** Use non-intrusive ad formats. Do not show ads that mimic system
notifications. Label ads clearly. Do not show inappropriate ads in apps
targeting children.

### Technical: Target API Level

**Rejection:** App doesn't target the required minimum API level.

**Fix:** Update `targetSdkVersion` in build.gradle to the current requirement.
Test on the latest Android version.

### Technical: 64-bit Requirement

**Rejection:** App doesn't include 64-bit native libraries.

**Fix:** Ensure all native libraries (NDK) include arm64-v8a and x86_64
architectures. Using App Bundles handles this automatically for most cases.

## Post-Publish Actions

1. Verify the listing appears in Google Play search
2. Install from the store on a test device
3. Confirm in-app billing works in production
4. Check Firebase / analytics for incoming data
5. Review the Android vitals dashboard for crash and ANR rates
6. Apply for editorial feature consideration via Play Console

---

## Reference: Ios Submission

# iOS App Store Connect Submission Guide

## Account Prerequisites

- Apple Developer Program membership ($99/year)
- App ID registered in Apple Developer portal
- Provisioning profiles configured for distribution
- Certificates: Apple Distribution certificate active and valid

## App Store Connect Setup

### Create the App Record

1. Log in to [App Store Connect](https://appstoreconnect.apple.com/)
2. Navigate to My Apps → "+" → New App
3. Fill in required fields:
   - Platform: iOS
   - App name (30 characters max, must be unique on the store)
   - Primary language
   - Bundle ID (must match Xcode project)
   - SKU (internal identifier, not public)

### App Information Tab

- **Category:** Select primary and optional secondary category
- **Content Rights:** Declare if app contains third-party content
- **Age Rating:** Complete questionnaire (violence, language, mature themes)

### Pricing and Availability

- Set price tier or configure in-app purchases
- Select availability by country/region
- Pre-order configuration (optional, up to 180 days before release)

## Screenshot Specifications

### Required Device Sizes

| Device                          | Resolution  | Required                          |
| ------------------------------- | ----------- | --------------------------------- |
| 6.7" iPhone (iPhone 15 Pro Max) | 1290 x 2796 | Yes                               |
| 6.5" iPhone (iPhone 14 Plus)    | 1284 x 2778 | Yes                               |
| 5.5" iPhone (iPhone 8 Plus)     | 1242 x 2208 | Yes (if supporting older devices) |
| 12.9" iPad Pro (6th gen)        | 2048 x 2732 | Required if iPad app              |
| 12.9" iPad Pro (2nd gen)        | 2048 x 2732 | Required if iPad app              |

### Screenshot Rules

- Minimum 1 screenshot per required size, maximum 10
- Format: PNG or JPEG, RGB color space, no alpha
- Must represent the actual app experience
- Text overlays allowed but must not mislead
- Status bar content should be clean (full signal, full battery, 9:41 AM)
- Screenshots for one size can be auto-scaled to other sizes in some cases

### Screenshot Best Practices

1. **First screenshot is critical** — it appears in search results
2. Show the core value proposition immediately
3. Use device frames for professional appearance
4. Include concise callout text (2-4 words per screen)
5. Tell a story across screenshots: problem → solution → features → social proof
6. Localize text overlays for each target market

## App Preview Video Specifications

| Attribute  | Requirement                                      |
| ---------- | ------------------------------------------------ |
| Duration   | 15-30 seconds                                    |
| Format     | H.264, M4V, MP4, MOV                             |
| Resolution | Must match screenshot resolution for device size |
| Frame rate | 30fps                                            |
| Audio      | AAC, optional but recommended                    |
| File size  | Up to 500 MB                                     |

### Video Best Practices

- Show real app footage, not marketing animations
- Demonstrate the core experience in the first 5 seconds
- Add captions (many users browse without sound)
- Record on device or simulator at native resolution

## App Icon Requirements

| Attribute       | Requirement                         |
| --------------- | ----------------------------------- |
| Size            | 1024 x 1024 pixels                  |
| Format          | PNG                                 |
| Color space     | sRGB or Display P3                  |
| Transparency    | Not allowed                         |
| Rounded corners | Do not apply — the system adds them |
| Layers/alpha    | Flattened, no alpha channel         |

## Build Upload Process

### Via Xcode

1. Select Generic iOS Device as build target
2. Product → Archive
3. Window → Organizer → select archive → Distribute App
4. Select App Store Connect → Upload
5. Follow prompts for signing and export compliance

### Via Transporter

1. Export archive as .ipa from Xcode Organizer
2. Open Transporter app (free from Mac App Store)
3. Drag .ipa file into Transporter
4. Click Deliver

### Build Processing

- Builds take 15-30 minutes to process after upload
- Status progresses: Processing → Ready for Sale / Ready for Review
- Check email for processing failure notifications
- Invalid Binary status requires fix and re-upload

## Export Compliance

Answer these questions during submission:

1. **Does your app use encryption?**
   - HTTPS only → Yes, but exempt (select appropriate exemption)
   - Custom encryption → May require ERN (Encryption Registration Number)
   - No encryption at all → No

2. **Common exemptions:**
   - Standard HTTPS/TLS for API calls
   - Standard encryption from iOS SDK
   - Authentication-only encryption

## App Review Process

### Timeline

- **Standard review:** 24-48 hours (90% of apps)
- **Expedited review:** Request via App Store Connect for critical bug fixes
- **Extended review:** Up to 7 days for complex apps or first submissions

### Review Information to Provide

- **Demo account:** Username and password for any authenticated features
- **Review notes:** Explain non-obvious functionality, special hardware needs,
  or features that require specific conditions to test
- **Contact info:** Phone number and email for reviewer questions
- **Attachment:** Screenshots or video of features that are hard to access

## Common Rejection Reasons and Fixes

### Guideline 1.2: User-Generated Content

**Rejection:** App allows user-generated content without moderation.

**Fix:** Implement content reporting, blocking, and filtering. Add terms of
service. Provide mechanism to report offensive content.

### Guideline 2.1: App Completeness

**Rejection:** App crashes, has broken features, or includes placeholder
content.

**Fix:** Test every feature thoroughly. Remove all placeholder text, images, and
lorem ipsum. Ensure all buttons and links function.

### Guideline 2.3: Accurate Metadata

**Rejection:** Screenshots or description don't match the app.

**Fix:** Retake screenshots from the current build. Update description to
reflect actual features. Remove mentions of features not yet implemented.

### Guideline 3.1.1: In-App Purchase

**Rejection:** App uses external payment for digital content.

**Fix:** Use Apple's In-App Purchase for all digital goods and subscriptions.
Physical goods and services can use external payment.

### Guideline 4.0: Design

**Rejection:** App is a thin wrapper around a website, or copies another app.

**Fix:** Provide native functionality beyond what the website offers. Ensure the
app has unique value and doesn't simply duplicate App Store apps.

### Guideline 4.3: Spam

**Rejection:** App is too similar to existing apps (including your own).

**Fix:** Ensure your app has unique functionality and value. Do not submit
multiple versions of the same app targeting different keywords.

### Guideline 5.1.1: Data Collection and Storage

**Rejection:** App collects data without proper disclosure or consent.

**Fix:** Update privacy policy. Implement consent flows. Declare all data
collection in App Privacy section. Minimize data collection.

### Guideline 5.1.2: Data Use and Sharing

**Rejection:** App shares data with third parties without user consent.

**Fix:** Disclose all third-party SDKs that collect data. Implement opt-in
consent for data sharing. Update privacy policy.

## Post-Approval Actions

### Release Options

- **Manually release:** You control when the app goes live (recommended)
- **Automatic release:** Goes live immediately after approval
- **Scheduled release:** Set a specific date and time

### Phased Release (Staged Rollout)

- Available for updates (not initial release)
- Releases to increasing percentages: 1%, 2%, 5%, 10%, 20%, 50%, 100%
- Over 7 days by default
- Can pause, resume, or release to all users at any point

### After Release

1. Verify the listing is live and correct
2. Download the app from the store to test
3. Confirm in-app purchases work in production
4. Check that analytics and crash reporting receive data
5. Submit promotional artwork for editorial consideration

---

## Reference: Launch Day Timeline

# Launch Day Timeline

Hour-by-hour execution plan for mobile app launch day. Adjust times based on the
primary market timezone. This template assumes a morning launch in the primary
market.

## Pre-Launch (Day Before)

### T-24 Hours

- [ ] Verify app status: approved and ready for release on all platforms
- [ ] Confirm all store listing metadata is final and accurate
- [ ] Test download of the approved build on a clean device (TestFlight /
      internal track)
- [ ] Verify backend services are scaled for expected traffic
- [ ] Confirm monitoring dashboards are accessible and functioning
- [ ] Brief the support team on launch plan and escalation contacts
- [ ] Pre-write social media posts and stage them in scheduling tool
- [ ] Confirm press embargo lift time (if applicable)

### T-12 Hours

- [ ] Final check of all backend APIs and services
- [ ] Verify push notification infrastructure is ready
- [ ] Confirm analytics events are flowing from the approved build
- [ ] Get 8 hours of sleep — launch day requires sustained attention

---

## Launch Morning

### T-0 (Launch Hour — Recommended: 9-10 AM Primary Market)

**Release the app:**

- [ ] **iOS:** Click "Release This Version" in App Store Connect (or the version
      will auto-release if configured)
- [ ] **Android:** Set production rollout to 10-20%
- [ ] Note exact release timestamp for all tracking

**Immediate verification (within 15 minutes):**

- [ ] Search for the app in each store — confirm it appears
- [ ] Download the app from the store on a fresh device
- [ ] Complete the primary user flow end-to-end
- [ ] Verify in-app purchases / subscriptions work in production
- [ ] Confirm crash reporting receives events
- [ ] Confirm analytics receives events

### T+1 Hour

**Monitor and activate:**

- [ ] Check crash-free rate — must be above 99.5%
- [ ] Check ANR rate (Android) — must be below 0.5%
- [ ] Review any incoming support messages
- [ ] Publish social media announcements
- [ ] Send email announcement to waitlist / mailing list
- [ ] Post on Product Hunt (if planned — must be posted by 12:01 AM PT ideally,
      or as early as possible)
- [ ] Notify press contacts that the app is live

### T+2 Hours

**First metrics check:**

- [ ] Downloads so far vs. projection
- [ ] Onboarding completion rate
- [ ] Any crash clusters forming? (check by device, OS version)
- [ ] First user reviews appearing?
- [ ] Social media engagement and sentiment
- [ ] Respond to any Product Hunt comments

### T+4 Hours

**Mid-day assessment:**

- [ ] Crash-free rate holding above 99.5%? → **Continue rollout**
- [ ] Any critical bugs reported? → **Assess severity**
- [ ] Download velocity trending? → **Adjust marketing if needed**
- [ ] **Android:** Consider increasing staged rollout to 25-50% if stable
- [ ] Post follow-up social content (behind-the-scenes, thank you)
- [ ] Respond to all user reviews

---

## Launch Afternoon

### T+6 Hours

**Stability confirmation:**

- [ ] Review crash reports from the full first half-day
- [ ] Check backend service health (response times, error rates)
- [ ] Review support ticket volume and themes
- [ ] Update team on status: green (proceed) / yellow (monitor) / red (halt)

### T+8 Hours

**End of business day check:**

- [ ] Total downloads for Day 1 (partial)
- [ ] Crash-free rate stable?
- [ ] Any show-stopping issues requiring immediate hotfix?
- [ ] If stable: **Android** can increase to 50% rollout
- [ ] Respond to all new reviews
- [ ] Post evening social media update (metrics celebration if appropriate)

---

## Decision Framework

### Green Light (Proceed with Rollout)

All of these must be true:

- Crash-free rate > 99.5%
- ANR rate < 0.5% (Android)
- No critical bugs in core user flow
- Store rating ≥ 4.0 (if enough reviews to judge)
- Backend services healthy

**Action:** Increase Android rollout percentage. Maintain iOS release.

### Yellow Light (Proceed with Caution)

Any of these are true:

- Crash-free rate between 99.0% and 99.5%
- Non-critical bugs reported but core flow works
- Store rating between 3.5 and 4.0
- Backend services showing elevated latency

**Action:** Hold rollout percentage. Investigate issues. Prepare hotfix if
needed. Increase monitoring frequency.

### Red Light (Halt Rollout)

Any of these are true:

- Crash-free rate below 99.0%
- Critical bug in core user flow (login, purchase, primary feature)
- Data loss or security issue
- Backend services down or severely degraded

**Action:** Halt Android staged rollout immediately. Prepare emergency hotfix.
For iOS, submit hotfix with expedited review request. Communicate with affected
users.

---

## Day 2 Morning

### T+24 Hours

- [ ] Review full Day 1 metrics:
  - Total downloads
  - D1 retention (users who opened the app again)
  - Onboarding completion rate
  - Crash-free rate trend
  - Review count and average rating
  - Revenue (if applicable)
- [ ] Compare metrics against projections
- [ ] Triage all crash reports — assign owners for top 3
- [ ] Respond to all new reviews
- [ ] **Android:** If Day 1 was green, increase to 100% rollout
- [ ] Plan any necessary hotfix release
- [ ] Share Day 1 results with stakeholders

---

## Post-Launch Week Schedule

| Day     | Focus Area       | Key Actions                                                       |
| ------- | ---------------- | ----------------------------------------------------------------- |
| Day 1   | Launch & Monitor | Release, verify, monitor, market                                  |
| Day 2   | Stabilize        | Review metrics, fix critical bugs, expand rollout                 |
| Day 3   | Respond          | Answer all reviews, handle support tickets, second marketing push |
| Day 4   | Analyze          | Deep metrics review, identify retention issues                    |
| Day 5   | Fix              | Ship hotfix for top crash/bug, respond to reviews                 |
| Day 6-7 | Plan             | Compile launch report, plan v1.1, celebrate                       |

---

## Emergency Contacts Template

Fill in before launch day:

| Role              | Name | Contact |
| ----------------- | ---- | ------- |
| Release manager   |      |         |
| Backend/API lead  |      |         |
| iOS developer     |      |         |
| Android developer |      |         |
| Support lead      |      |         |
| Marketing lead    |      |         |

## Launch Day Communication Template

### Internal Status Update (Send Every 2 Hours)

```
Launch Status: [GREEN / YELLOW / RED]
Time: [timestamp]
Downloads: [count] (projection: [count])
Crash-free rate: [iOS: X% / Android: X%]
Reviews: [count] (avg: [rating])
Android rollout: [X%]
Issues: [none / brief description]
Next update: [time]
```

### External Launch Announcement Template

```
[App Name] is live on [App Store / Google Play / both]!

[One sentence describing what the app does and why it matters]

Download: [link]

Built with [relevant tech/philosophy]. We'd love your feedback.
```
