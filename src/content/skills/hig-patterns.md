---
title: "Hig Patterns"
description: "Apple Human Interface Guidelines interaction and UX patterns."
category: "development"
source: "community"
author: "Community"
tags: ["hig"]
date: 2026-03-20
---

# Apple HIG: Interaction Patterns

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Minimize modality.** Use modality only when it is critical to get attention, a task must be completed or abandoned, or saving changes is essential. Prefer non-modal alternatives.

2. **Provide clear feedback.** Every action should produce visible, audible, or haptic response. Activity indicators for indeterminate waits, progress bars for determinate, haptics for physical confirmation.

3. **Support undo over confirmation dialogs.** Destructive actions should be reversible when possible. Undo is almost always better than "Are you sure?"

4. **Launch quickly.** Display a launch screen that transitions seamlessly into the first screen. No splash screens with logos. Restore previous state.

5. **Defer sign-in.** Let users explore before requiring account creation. Support Sign in with Apple and passkeys.

6. **Keep onboarding brief.** Three screens max. Let users skip. Teach through progressive disclosure and contextual hints.

7. **Use progressive disclosure.** Show essentials first, let users drill into details. Don't overwhelm with every option on one screen.

8. **Respect user attention.** Consolidate notifications, minimize interruptions, give users control over alerts. Never use notifications for marketing.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [charting-data.md](references/charting-data.md) | Charting Data | Data visualization patterns, accessible charts, interactive elements |
| [collaboration-and-sharing.md](references/collaboration-and-sharing.md) | Collaboration & Sharing | Share sheets, activity views, collaborative editing, SharePlay |
| [drag-and-drop.md](references/drag-and-drop.md) | Drag and Drop | Drag sources, drop targets, spring loading, multi-item drag, visual feedback |
| [entering-data.md](references/entering-data.md) | Entering Data | Text fields, pickers, steppers, input validation, keyboard types, autofill |
| [feedback.md](references/feedback.md) | Feedback | Alerts, action sheets, haptic patterns, sound feedback, visual indicators |
| [file-management.md](references/file-management.md) | File Management | Document browser, file providers, iCloud integration, document lifecycle |
| [going-full-screen.md](references/going-full-screen.md) | Going Full Screen | Full-screen transitions, immersive content, exiting full screen |
| [launching.md](references/launching.md) | Launching | Launch screens, state restoration, cold vs warm launch |
| [live-viewing-apps.md](references/live-viewing-apps.md) | Live Viewing Apps | Live content display, real-time updates, Live Activities, Dynamic Island |
| [loading.md](references/loading.md) | Loading | Activity indicators, progress views, skeleton screens, lazy loading, placeholders |
| [managing-accounts.md](references/managing-accounts.md) | Managing Accounts | Sign in with Apple, passkeys, account creation, credential autofill, account deletion |
| [managing-notifications.md](references/managing-notifications.md) | Managing Notifications | Permission requests, grouping, actionable notifications, provisional delivery |
| [modality.md](references/modality.md) | Modality | Sheets, alerts, popovers, full-screen modals, when to use each |
| [multitasking.md](references/multitasking.md) | Multitasking | iPad Split View, Slide Over, Stage Manager, responsive layout, size class transitions |
| [offering-help.md](references/offering-help.md) | Offering Help | Contextual tips, onboarding hints, help menus, support links |
| [onboarding.md](references/onboarding.md) | Onboarding | Welcome screens, feature highlights, progressive onboarding, skip options |
| [playing-audio.md](references/playing-audio.md) | Playing Audio | Audio sessions, background audio, Now Playing, audio routing, interruptions |
| [playing-haptics.md](references/playing-haptics.md) | Playing Haptics | Core Haptics, UIFeedbackGenerator, haptic patterns, custom haptics |
| [playing-video.md](references/playing-video.md) | Playing Video | Video player controls, picture-in-picture, AirPlay, full-screen video |
| [printing.md](references/printing.md) | Printing | Print dialogs, page setup, AirPrint integration |
| [ratings-and-reviews.md](references/ratings-and-reviews.md) | Ratings & Reviews | SKStoreReviewController, timing, frequency limits, in-app feedback |
| [searching.md](references/searching.md) | Searching | Search bars, suggestions, scoped search, results display, recents |
| [settings.md](references/settings.md) | Settings | In-app vs Settings app, preference organization, toggles, defaults |
| [undo-and-redo.md](references/undo-and-redo.md) | Undo and Redo | Shake to undo, undo/redo stack, multi-level undo |
| [workouts.md](references/workouts.md) | Workouts | Workout sessions, live metrics, Always On display, summaries, HealthKit |

## Pattern Selection Guide

| User Goal | Recommended Pattern | Avoid |
|---|---|---|
| First app experience | Brief onboarding (max 3 screens) + progressive disclosure | Long tutorials, mandatory sign-up |
| Waiting for content | Skeleton screens or progress indicators | Blocking spinners with no context |
| Confirming destructive action | Undo support | Excessive "Are you sure?" dialogs |
| Collecting user input | Inline validation, smart defaults, autofill | Modal forms for simple inputs |
| Requesting permissions | Contextual, just-in-time with explanation | Requesting all permissions at launch |
| Providing feedback | Haptics + visual indicator | Silent actions with no confirmation |
| Organizing preferences | In-app settings for frequent items | Burying all settings in system Settings app |

## Output Format

1. **Recommended pattern with rationale**, citing the relevant reference file.
2. **Step-by-step implementation** covering each screen or state.
3. **Platform variations** for targeted platforms.
4. **Common pitfalls** that violate HIG for this pattern.

## Questions to Ask

1. Where in the app does this pattern appear? What comes before and after?
2. Which platforms?
3. Designing from scratch or improving an existing flow?
4. Does this involve sensitive actions? (Destructive operations, payments, permissions)

## Related Skills

- **hig-foundations** -- Accessibility, color, typography, and privacy principles underlying every pattern
- **hig-platforms** -- Platform-specific pattern implementations
- **hig-components-layout** -- Structural components (tab bars, sidebars, split views) for navigation patterns
- **hig-components-content** -- Content display within patterns (charts, collections, search results)

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Charting Data

|---  
September 23, 2022| New page.

---

## Reference: Collaboration And Sharing

|---  
December 5, 2023| Added artwork illustrating button placement and various types of collaboration permissions.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| New page.

---

## Reference: Drag And Drop

|---  
October 24, 2023| Added artwork.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Entering Data

|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Feedback

---
title: "Feedback | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/feedback

# Feedback

Feedback helps people know what’s happening, discover what they can do next, understand the results of actions, and avoid mistakes.

<!-- image: A sketch of a pointer surrounded by a circular set of short lines, suggesting a response to a mouse click. The image is overlaid with rectangular and circular grid lines and is tinted orange to subtly reflect the orange in the original six-color Apple logo. -->

Providing clear, consistent feedback as people interact with your app or game can make it feel intuitive and encourage deeper exploration. Feedback can communicate several different things, such as:

  * The current status of something

  * The success or failure of an important task or action

  * A warning about an action that can have negative consequences

  * An opportunity to correct a mistake or problematic situation




The most effective feedback tends to match the significance of the information to the way it’s delivered. For example, it often works well to display status information in a passive way so that people can view it when they need it. In contrast, a warning about possible data loss needs to interrupt people so they have a chance to avoid the problem.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/feedback#Best-practices)

**Make sure all feedback is accessible.** When you use multiple ways to provide feedback, you reach more people and give them the opportunity to receive the feedback in ways that work for them. For example, when you provide feedback using color, text, sound, and haptics, people can receive it whether they silence their device, look away from the screen, or use VoiceOver. (For guidance on providing haptic feedback, see [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics).)

**Consider integrating status feedback into your interface.** When status feedback is available near the items it describes, people get important information without having to take action or leave their current context. For example, Mail in iOS and iPadOS describes the most recent update and displays the number of unread messages in the toolbar of the mailbox screen, making the information unobtrusive but easy for people to check when they’re interested.

**Use alerts to deliver critical — and ideally actionable — information.** By design, alerts disrupt the current context, so you need to match the importance of the information to the level of interruption. Alerts can lose their impact if you use them too often or to deliver unimportant information. For guidance, see [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts).

**Warn people when they initiate a task that can cause data loss that’s unexpected and irreversible.** In contrast, don’t warn people when data loss is the expected result of their action. For example, the Finder doesn’t warn people every time they throw away a file because deleting the file is the expected result.

**When it makes sense, confirm that a significant action or task has completed.** For example, people appreciate getting feedback that confirms a successful Apple Pay transaction. It’s generally best to reserve this type of confirmation for activities that are sufficiently important — because people typically expect their action or task to succeed, they only need to know when it doesn’t.

**Show people when a command can’t be carried out and help them understand why.** For example, if people request directions without specifying a destination, Maps tells them that it can’t provide directions to and from the same location.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/feedback#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS._

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/feedback#watchOS)

**Avoid displaying an indeterminate progress indicator — such as a loading indicator — in a watchOS app.** An animated indicator can make people think they need to continue paying attention to the display, which isn’t a good user experience. To provide a better experience, reassure people that they’ll receive a notification when the process completes.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/feedback#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/feedback#Related)

[Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio)

[Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

[Motion](https://developer.apple.com/design/human-interface-guidelines/motion)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/feedback#Developer-documentation)

[Animation and haptics](https://developer.apple.com/documentation/UIKit/animation-and-haptics) — UIKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/feedback#Videos)

[<!-- image:  --> Designing Fluid Interfaces ](https://developer.apple.com/videos/play/wwdc2018/803)

[<!-- image:  --> Essential Design Principles ](https://developer.apple.com/videos/play/wwdc2017/802)

---

## Reference: File Management

|---  
June 10, 2024| Added guidelines for using the document launcher in iOS and iPadOS.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Going Full Screen

|---  
June 9, 2025| Updated guidance for hiding toolbars and navigation controls, and deferring Home Screen indicator gestures in full-screen iOS and iPadOS apps and games.  
June 10, 2024| Enhanced guidance for playing a game in full-screen mode.

---

## Reference: Launching

|---  
June 10, 2024| Added guidance on displaying a splash screen.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Live Viewing Apps

---
title: "Live-viewing apps | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps

# Live-viewing apps

As you design a live-viewing app, prioritize the content and create fun, fluid interactions that encourage immersion in the live-viewing experience.

<!-- image: A sketch of a television containing a play button, suggesting playback of media. The image is overlaid with rectangular and circular grid lines and is tinted orange to subtly reflect the orange in the original six-color Apple logo. -->

Live-viewing apps need to elevate and prioritize live content. In every screen, draw people’s attention to live content and make sure they can distinguish it from video-on-demand (VOD) content at a glance.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#Best-practices)

**Feature live content prominently and make it easy to access.** People come to your app to watch content, so you want to minimize the interval between starting your app and playing content. When live content is in the first tab, people don’t have to tap more than once to start viewing it.

**Let people tap once — or not at all — to start playback.** For example, you might display a Watch Now button on top of featured or recently viewed live content. When people tap this button, it immediately disappears and playback begins, replacing your app’s UI with a full-screen, immersive viewing experience.

**Make sure live content looks live.** People need to be able to distinguish live content from VOD content. Although simply playing live content is the best way to make it feel live, you can also help people recognize live content by marking it in some way. For example, you might display other channels in a collection row titled “Live” and give each item a visual indicator — such as a badge, symbol, or sash — that identifies it as live.

**Consider indicating the progress of currently playing live content.** People appreciate knowing where they’ll land when they jump into in-progress live content. You can use a progress bar or other indicator to show people how much content remains.

**Give people additional actions and viewing alternatives.** In addition to playback, which always needs to be the primary action, make it easy for people to record, restart, download, and perform other actions that you support. Display these actions in the same order throughout your app — for example, Watch, Start Over, Record, and Favorite. Also, if the currently playing content is playing again at other times, show this information so that people can schedule their viewing.

**Consider using a content footer for browsing channels during playback.** A content footer lets people browse without taking them out of the live playback experience. If you decide to use a content footer, be sure to:

  * Give it a subtle treatment, such as a darkening, to keep text legible and help all items remain visually distinct from the content playing behind it.

  * Make it easy for people to identify the thumbnail that represents the currently playing content by, for example, badging the thumbnail or tinting its progress bar.

  * Match the categories in the content footer to those in your electronic program guide (for related guidance, see [EPG experience](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#EPG-experience)).

  * Design a simple, predictable way for people to invoke and dismiss the content footer — for example, if swiping up invokes the footer, people would expect swiping down to dismiss it.




**Provide instant visual feedback when people change channels.** This is essential for two reasons: people need confirmation that they’ve arrived at the channel they want, and providing feedback can give the streaming content some time to load.

**Match audio to the current context.** When people start playing live content, they expect the audio to match even if they switch to browsing while the content plays in the background. However, when people navigate away from the live tab in your app, they leave the live-viewing context, so audio needs to stop.

## [EPG experience](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#EPG-experience)

Live-viewing apps typically provide an electronic program guide (EPG) that contains information about scheduled programming. Follow these guidelines to give people a streamlined EPG experience that feels designed specifically for your live-viewing app.

**Prominently display current information and make it easy to return to playback.** When people first open the EPG, the current program, channel, and time needs to be easy to spot so they can instantly return to the current channel.

**Make browsing the EPG effortless.** A typical EPG contains a lot of information, so it’s important to help people page, scroll, or jump through it easily. Also consider providing a My Channels group or a Favorites group that gives people quick access to the content they view most often.

**Group content into familiar categories to help people find it more easily.** For example, you might use categories like Movies, TV Shows, Kids, Sports, and Popular. If your app includes a content footer, organize content thumbnails using the same categories as in the EPG.

**Let people browse the EPG without leaving their current content.** For example, you can continue playing content in a picture-in-picture (PiP) mode or in the background while people browse the EPG.

## [Cloud DVR](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#Cloud-DVR)

If you support digital video recording (DVR) in the cloud, follow these guidelines to provide a great recording experience in your live-viewing app.

**Let people start and stop recording from the info panel.** While live-streaming, people want to reveal the info panel to start recording immediately.

**Let people record a future program in a view that provides details about the content.** Also, give people the option to record only that program or all future episodes.

**Help people adapt the recording experience to their needs.** Let people specify precisely what they want to record, such as only the current episode, only new episodes, or only games that involve specific teams.

**Allow playback and other content-specific actions within your cloud DVR area.** When people open a view that displays content details in your cloud DVR section, let them play or delete content and, if applicable, adjust recording settings.

**Consider offering a control that lets people manage cloud DVR settings.** For example, you might let people delete recordings they’ve already watched or content that’s older than a certain number of days. Ideally, help people avoid running out of space by letting them set up automatic storage management, which overwrites the oldest or already viewed content.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#Related)

[Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes)

[Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)

---

## Reference: Loading

|---  
June 9, 2025| Revised guidance for storing downloads to reflect downloading large assets in the background.  
June 10, 2024| Added guidelines for showing progress and storing downloads, and enhanced guidance for games.

---

## Reference: Managing Accounts

---
title: "Managing accounts | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/managing-accounts

# Managing accounts

When it doesn’t create an unnecessary barrier to your experience, an account can be a convenient way for people to access their content and track personal details.

<!-- image: A sketch of a person, suggesting personal information. The image is overlaid with rectangular and circular grid lines and is tinted orange to subtly reflect the orange in the original six-color Apple logo. -->

Ask people to create an account only if your core functionality requires it; otherwise, let people enjoy your app or game without one. If you require an account, consider using [Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) to give people a consistent sign-in experience they can trust and the convenience of not having to remember multiple accounts and authentication methods.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Best-practices)

**Explain the benefits of creating an account and how to sign up.** If your app or game requires an account, write a brief, friendly description of the reasons for the requirement and its benefits. Display this message in your sign-in view.

**Delay sign-in for as long as possible.** People often abandon apps when they’re forced to sign in before they can do anything useful. To help avoid this situation, give people a chance to get a sense of what your app or game does before asking them to make a commitment to it. For example, a shopping app might let people browse as much as they want, requiring sign-in only when they’re ready to make a purchase.

**If you don’t use Sign in with Apple in your iOS, iPadOS, macOS, or visionOS app, prefer using a passkey.** Passkeys simplify account creation and authentication, eliminating the need for people to create or enter passwords. When an app supports passkeys, people simply provide their user name when creating a new account or signing in to an existing one. For developer guidance, see [Supporting passkeys](https://developer.apple.com/documentation/AuthenticationServices/supporting-passkeys). If you need to continue using passwords for authentication, augment security by requiring two-factor authentication (for developer guidance, see [Securing Logins with iCloud Keychain Verification Codes](https://developer.apple.com/documentation/AuthenticationServices/securing-logins-with-icloud-keychain-verification-codes)).

**Always identify the authentication method you offer.** For example, if you display a button for signing in to your app with Face ID, title it using a phrase like “Sign In with Face ID” instead of a generic phrase like “Sign In.”

**Refer only to authentication methods that are available in the current context.** For example, don’t reference Face ID on a device that doesn’t offer it. Check the device’s capabilities and use the appropriate terminology. For developer guidance, see [`LABiometryType`](https://developer.apple.com/documentation/LocalAuthentication/LABiometryType).

**In general, avoid offering an app-specific setting for opting in to biometric authentication.** People turn on biometric authentication at the system level, so presenting an in-app setting is redundant and could be confusing.

**Avoid using the term _passcode_ to refer to account authentication.** People create a passcode to unlock their device or authenticate for Apple services. If you use the term in your interface, people might think you’re asking them to reuse their passcode in your app or game.

## [Deleting accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Deleting-accounts)

If you help people create an account within your app or game, you must also help them delete it, not just deactivate it. In addition to following the guidelines below, be sure to understand and comply with your region’s legal requirements related to account deletion and the right to be forgotten.

Important

If legal requirements compel your app to maintain accounts or information — such as digital health records — or to follow a specific account-deletion process, clearly describe the situation so people can understand the information or accounts you must maintain and the process you must follow.

**Provide a clear way to initiate account deletion within your app or game.** If people can’t perform account deletion within your app, you must provide a direct link to the webpage on which people can do so. Make the link easy to discover — for example, don’t bury it in your Privacy Policy or Terms of Service pages.

Developer note

If people used [Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple) to create an account within your app, you revoke the associated tokens when they delete their account. See [`Token revocation`](https://developer.apple.com/documentation/SigninwithAppleRESTAPI/Revoke-tokens).

**Provide a consistent account-deletion experience whether people perform it within your app or game or on the website.** For example, avoid making one version of the deletion flow longer or more complicated than the other.

**Consider letting people schedule account deletion to occur in the future.** People can appreciate the opportunity to use their remaining services or wait until their subscription auto-renews before deleting their account. If you offer a way to schedule account deletion, offer an option for immediate deletion as well.

**Tell people when account deletion will complete, and notify them when it’s finished.** Because it can sometimes take a while to fully delete an account, it’s essential to keep people informed about the status of the deletion process so they know what to expect.

**If you support in-app purchases, help people understand how billing and cancellation work when they delete their account.** For example, you might need to help people understand the following scenarios:

  * Billing for an auto-renewable subscription continues through Apple until people cancel the subscription, regardless of whether they delete their account.

  * After they delete their account, people need to cancel their subscription or request a refund.




In addition to helping people understand these scenarios, provide information that describes how to cancel subscriptions and manage purchases. For guidance, see [Helping people manage their subscriptions](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase#Helping-people-manage-their-subscriptions) and [Providing help with in-app purchases](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase#Providing-help-with-in-app-purchases).

Note

Even if people didn’t use your app to purchase the subscription, you still need to support account deletion.

## [TV provider accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#TV-provider-accounts)

Many popular TV providers let people sign in to their accounts at the system level, eliminating the need to authenticate on an app-by-app basis. If your TV provider app requires people to sign in, use TV Provider Authentication to provide the most efficient onboarding experience.

**Avoid displaying a sign-out option when people are signed in at the system level.** If your app must include a sign-out option, invoking it needs to prompt people to navigate to Settings > TV Provider to sign out of their account.

**Never instruct people to sign out by adjusting privacy controls.** The TV provider controls in Settings > Privacy aren’t a sign-out mechanism. These settings help people manage the apps that can access their TV provider account.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or visionOS._

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#tvOS)

Most people interact with Apple TV using a remote, not a keyboard, so ask for the minimum amount of information necessary.

**Prefer letting people use another device to sign up or authenticate.** When you configure your app’s associated domains, Apple TV can work with other devices to safely suggest sign-in credentials, including [Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple). For developer guidance, see [Configuring an associated domain](https://developer.apple.com/documentation/Xcode/configuring-an-associated-domain).

**When people are signed in to a shared account, avoid asking them to choose their profile every time they become the current user.** In tvOS 16 and later, your app can share its credentials with all users while storing each individual’s profile and user data separately. When you support this type of sharing, your app can automatically use the current user’s profile without asking each person to sign in separately to a shared account. For developer guidance, see [`kSecUseUserIndependentKeychain`](https://developer.apple.com/documentation/Security/kSecUseUserIndependentKeychain) and [`User Management Entitlement`](https://developer.apple.com/documentation/BundleResources/Entitlements/com.apple.developer.user-management).

**Minimize data entry.** If you need to gather more than a small amount of information, ask people to visit a website from another device. If you need an email address, show the email keyboard screen, which includes a list of recently entered addresses.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#watchOS)

Use iCloud synchronization to provide access to the Keychain, letting people autofill user names and passwords and preserve app settings.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Related)

[Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)

[Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Developer-documentation)

[Supporting passkeys](https://developer.apple.com/documentation/AuthenticationServices/supporting-passkeys) — Authentication Services

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/managing-accounts#Videos)

[<!-- image:  --> What’s new in passkeys ](https://developer.apple.com/videos/play/wwdc2025/279)

[<!-- image:  --> What’s new in device management ](https://developer.apple.com/videos/play/wwdc2024/10143)

---

## Reference: Managing Notifications

|---|---|---  
Passive| No| No| No  
Active| No| No| No  
Time Sensitive| Yes| Yes| No  
Critical| Yes| Yes| Yes  
  
Note

Because a Critical notification can override the Ring/Silent switch and break through scheduled delivery and Focus, you must get an entitlement to send one.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Best-practices)

**Build trust by accurately representing the urgency of each notification.** People have several ways to adjust how they receive your notifications — including turning off all notifications — so it’s essential to be as realistic as possible when assigning an interruption level. You don’t want people to feel that a notification uses a high level of urgency to interrupt them with low-priority information.

**Use the Time Sensitive interruption level only for notifications that are relevant in the moment.** To help people understand the benefits of letting Time Sensitive notifications break through a Focus or scheduled delivery, make sure the notification is about an event that’s happening now or will happen within an hour. The first time a Time Sensitive notification arrives from your app, the system describes how such a notification works and gives people a way to turn it off if they don’t agree that the information requires their immediate attention. Going forward, the system periodically gives people additional opportunities to evaluate how your Time Sensitive notification is working for them. For developer guidance, see [`UNNotificationInterruptionLevel`](https://developer.apple.com/documentation/UserNotifications/UNNotificationInterruptionLevel).

## [Sending marketing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Sending-marketing-notifications)

Don’t use notifications to send marketing or promotional content unless people explicitly agree to receive such information. When people want to learn about new features, content, or events related to your app or game, they can grant their permission to receive marketing notifications. For example, people who use a subscription app might appreciate getting an offer to become a subscriber, and game players might want to receive a special offer related to a live game event.

**Never use the Time Sensitive interruption level to send a marketing notification.** People may have agreed to receive marketing notifications from your app, but such a notification must never break through a Focus or scheduled delivery setting.

**Get people’s permission if you want to send them promotional or marketing notifications.** Before you send these notifications to people, you must receive their explicit permission to do so. Create an alert, modal view, or other interface that describes the types of information you want to send and gives people a clear way to opt in or out.

**Make sure people can manage their notification settings within your app.** In addition to requesting permission to send informational or marketing notifications, you must also provide an in-app settings screen that lets people change their choice. For guidance, see [Settings](https://developer.apple.com/design/human-interface-guidelines/settings).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, or visionOS._

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#watchOS)

By default, the notification settings people use for apps on their iPhone apply to the same apps on their Apple Watch. People can manage these settings in the Apple Watch app on iPhone, or they can access per-notification options — such as Mute 1 Hour or Turn off Time Sensitive — by swiping left when a notification arrives on their Apple Watch.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Related)

[Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Developer-documentation)

[User Notifications](https://developer.apple.com/documentation/UserNotifications)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/managing-notifications#Videos)

[<!-- image:  --> Send communication and Time Sensitive notifications ](https://developer.apple.com/videos/play/wwdc2021/10091)

[<!-- image:  --> The Push Notifications primer ](https://developer.apple.com/videos/play/wwdc2020/10095)

---

## Reference: Modality

|---  
December 5, 2023| Enhanced guidance for in-depth modal experiences and clarified guidance on multiple modal views.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Multitasking

|---  
June 9, 2025| Reorganized guidance in platform considerations, and added guidance for multitasking with multiple windows in iPadOS.  
December 5, 2023| Added artwork for primary and auxiliary windows in iPadOS.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Offering Help

|---  
December 5, 2023| Included visionOS in guidance for creating tooltips.  
September 12, 2023| Added guidance for creating tips.

---

## Reference: Onboarding

|---  
June 10, 2024| Clarified different approaches to onboarding and added a guideline on displaying a splash screen.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Playing Audio

|---|---  
Solo ambient| Sound isn’t essential, but it silences other audio. For example, a game with a soundtrack.| Responds to the silence switch. Doesn’t mix with other sounds. Doesn’t play in the background.  
Ambient| Sound isn’t essential, and it doesn’t silence other audio. For example, a game that lets people play music from another app during gameplay in place of the game’s soundtrack.| Responds to the silence switch. Mixes with other sounds. Doesn’t play in the background.  
Playback| Sound is essential and might mix with other audio. For example, an audiobook or educational app that teaches a foreign language, which people might want to listen to after leaving the app.| Doesn’t respond to the silence switch. May or may not mix with other sounds. Can play in the background.  
Record| Sound is recorded. For example, a note-taking app that offers an audio recording mode. An app of this nature might switch its category to playback if it lets people play the recorded notes.| Doesn’t respond to the silence switch. Doesn’t mix with other sounds. Can record in the background.  
Play and record| Sound is recorded and played, potentially simultaneously. For example, an audio messaging or video calling app.| Doesn’t respond to the silence switch. May or may not mix with other sounds. Can record and play in the background.  
  
**Respond to audio controls only when it makes sense.** People can control audio playback from outside your app’s interface — such as in Control Center or with controls on their headphones — regardless of whether your app is in the foreground or background. If your app is actively playing audio, in a clear audio-related context, or connected to a device that uses Bluetooth or AirPlay, it’s fine to respond to audio controls. Otherwise, when people activate a control, avoid halting audio currently playing from another app.

**Avoid repurposing audio controls.** People expect audio controls to behave consistently in all apps, so it’s essential to avoid redefining the meaning of an audio control in your app. If your app doesn’t support certain controls, don’t respond to them.

**Consider creating custom audio player controls only if you need to offer commands that the system doesn’t support.** For example, you might want to define custom increments for skipping forward or backward, or present content that’s related to the playing audio, such as a sports score.

**Let other apps know when your app finishes playing temporary audio.** If your app can temporarily interrupt the audio of other apps, be sure to flag your audio session in a way that lets other apps know when they can resume. For developer guidance, see [`notifyOthersOnDeactivation`](https://developer.apple.com/documentation/AVFAudio/AVAudioSession/SetActiveOptions/notifyOthersOnDeactivation).

## [Handling interruptions](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Handling-interruptions)

Although most apps and games rely on the system’s default interruption behavior, you can customize this behavior to better accommodate your needs.

**Determine how to respond to audio-session interruptions.** For example, if your app supports recording or other audio-related tasks that people don’t want interrupted, you can tell the system to avoid interrupting the currently playing audio for an incoming call unless people choose to accept it. Another example is a VoIP app, which must end a call when people close the Smart Folio of their iPad while they’re using the built-in microphone. Closing the Smart Folio automatically mutes the iPad microphone and by default interrupts the audio session associated with it. If a VoIP app restarts the audio session when people reopen their Smart Folio, it risks invading people’s privacy by unmuting the microphone without their knowledge. You can inspect an audio-session interruption to help determine the right way to respond; for developer guidance, see [Handling audio interruptions](https://developer.apple.com/documentation/AVFAudio/handling-audio-interruptions).

**When an interruption ends, determine whether to resume audio playback automatically.** Sometimes, audio from a different app can interrupt the audio your app is playing. An interruption can be _resumable_ , like an incoming phone call, or _nonresumable_ , like when people start a new music playlist. Use the interruption type and your app’s type to decide whether to resume playback automatically. For example, a media playback app that’s actively playing audio when an interruption occurs can check to be sure the type is resumable before continuing playback when the interruption ends. On the other hand, a game doesn’t need to check the interruption type before automatically resuming playback, because a game plays audio without an explicit user choice. For developer guidance, see [`shouldResume`](https://developer.apple.com/documentation/AVFAudio/AVAudioSession/InterruptionOptions/shouldResume).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Platform-considerations)

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#iOS-iPadOS)

**Use the system’s sound services to play short sounds and vibrations.** For developer guidance, see [Audio Services](https://developer.apple.com/documentation/AudioToolbox/audio-services).

### [macOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#macOS)

In macOS, notification sounds mix with other audio by default.

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#tvOS)

In tvOS, the system plays audio only when people initiate it, through interactions within apps and games or when performing device calibrations. For example, tvOS doesn’t play sounds to accompany components like alerts or notifications.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#visionOS)

Subtle, expressive sounds are everywhere in visionOS, enhancing experiences and providing essential feedback when people look at a virtual object and use gestures to interact with it. The system combines audio algorithms with information about a person’s physical surroundings to produce _Spatial Audio_ , which is sound that people can perceive as coming from specific locations in space, not just from speakers.

Important

In visionOS, as in every platform, avoid communicating important information using only sound. Always provide additional ways to help people understand your app. For guidance, see [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

In visionOS, audio playback from the Now Playing app pauses automatically when people close the app’s window, and audio from an app that isn’t the Now Playing app can duck when people look away from it to different app.

**Prefer playing sound.** People generally choose to keep sounds audible while they’re wearing the device, so an app that doesn’t play sound — especially in an immersive moment — can feel lifeless and may even seem broken. Throughout the design process, look for opportunities to create meaningful sounds that aid navigation and help people understand the spatial qualities of your app.

**Design custom sounds for custom UI elements.** In general, a system-provided element plays sound to help people locate it and receive feedback when they interact with it. To help people interact with your custom elements, design sounds that provide feedback and enhance the spatial experience of your app.

**Use Spatial Audio to create an intuitive, engaging experience.** Because people can perceive Spatial Audio as coming from anywhere around them, it works especially well in a fully immersive context as a way to help an experience feel lifelike. _Ambient audio_ provides pervasive sounds that can help anchor people in a virtual world and an _audio source_ can sound like it comes from a specific object. As you build the soundscape for your app, consider using both types of audio.

**Consider defining a range of places from which your app sounds can originate.** Spatial Audio helps people locate the object that’s making sound, whether it’s stationary or moving in space. For example, when people move an app window that’s playing audio, the sound continues to come directly from the window, wherever people move it.

**Consider varying sounds that people could perceive as repetitive over time.** For example, the system subtly varies the pitch and volume of the virtual keyboard’s sounds, suggesting the different sounds a physical keyboard can make as people naturally vary the speed and forcefulness of their typing. An efficient way to achieve a pleasing variation in sound is to randomize a sound file’s pitch and volume during playback, instead of creating different files.

**Decide whether you need to play sound that’s fixed to the wearer or tracked by the wearer.** People perceive _fixed_ sound as if it’s pointed at them, regardless of the direction they look or the virtual objects they move. In contrast, people tend to perceive _tracked_ sound as coming from a particular object, so moving the object closer or farther away changes what they hear. In general, you want to use tracked sound to enhance the realism of your experience, but there could be cases where fixed sound is a good choice. For example, Mindfulness uses fixed sound to envelop the wearer in an engaging, peaceful setting.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#watchOS)

In watchOS, the system manages audio playback. An app can play short audio clips while it’s active and running in the foreground, or it can play longer audio that continues even when people lower their wrist or switch to another app. For developer guidance, see [Playing Background Audio](https://developer.apple.com/documentation/WatchKit/playing-background-audio).

**Use the recommended encoding values for media assets.** Specifically, use the 64 kbps HE-AAC (High-Efficiency Advanced Audio Coding) format to produce good-quality audio with lower data requirements.

**Consider** **presenting a Now Playing view so people can control current or recently played audio without leaving your app.** The system-provided Now Playing view also displays information about the current audio source — which might be another app on a person’s Apple Watch or iPhone — and automatically selects the current or most recently used source. For developer guidance, see [Adding a Now Playing View](https://developer.apple.com/documentation/WatchKit/adding-a-now-playing-view).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Related)

[Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Developer-documentation)

[Configuring your app for media playback](https://developer.apple.com/documentation/AVFoundation/configuring-your-app-for-media-playback) — AVFoundation

[`AVAudioSession`](https://developer.apple.com/documentation/AVFAudio/AVAudioSession) — AVFAudio

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Videos)

[<!-- image:  --> Explore immersive sound design ](https://developer.apple.com/videos/play/wwdc2023/10271)

[<!-- image:  --> Principles of spatial design ](https://developer.apple.com/videos/play/wwdc2023/10072)

[<!-- image:  --> Immerse your app in Spatial Audio ](https://developer.apple.com/videos/play/wwdc2021/10265)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/playing-audio#Change-log)

Date| Changes  
---|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Playing Haptics

|---  
Alignment| Indicates the alignment of a dragged item. For example, this pattern could be used in a drawing app when the people drag a shape into alignment with another shape. Other scenarios where this type of feedback could be used might include scaling an object to fit within specific dimensions, positioning an object at a preferred location, or reaching the beginning/end or minimum/maximum of something like a scrubber in a video app.  
Level change| Indicates movement between discrete levels of pressure. For example, as people press a fast-forward button on a video player, playback could increase or decrease and haptic feedback could be provided as different levels of pressure are reached.  
Generic| Intended for providing general feedback when the other patterns don’t apply.  
  
For developer guidance, see [`NSHapticFeedbackPerformer`](https://developer.apple.com/documentation/AppKit/NSHapticFeedbackPerformer).

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#watchOS)

Apple Watch Series 4 and later provides haptic feedback for the Digital Crown, which gives people a more tactile experience as they scroll through content. By default, the system provides linear haptic detents that people can feel as they rotate the Digital Crown. Some system controls, like table views, provide detents as new items scroll onto the screen. For developer guidance, see [`WKHapticType`](https://developer.apple.com/documentation/WatchKit/WKHapticType).

watchOS defines the following set of haptics, each of which conveys a specific meaning to people.

  * Notification 
  * Up 
  * Down 
  * Success 
  * Failure 
  * Retry 
  * Start 
  * Stop 
  * Click 



Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Notification.** Tells the person that something significant or out of the ordinary has happened and requires their attention. The system plays this same haptic when a local or remote notification arrives.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Up.** Tells the person that an important value increased above a significant threshold.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Down.** Tells the person that an important value decreased below a significant threshold.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Success.** Tells the person that an action completed successfully.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Failure.** Tells the person that an action failed.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Retry.** Tells the person that an action failed but they can retry it.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Start.** Tells the person that an activity started. Use this haptic when starting a timer or any other activity that a person can explicitly start and stop. The stop haptic usually follows this haptic.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Stop.** Tells the person that an activity stopped. Use this haptic when stopping a timer or other activity that the person previously started.

Video with custom controls. 

Content description: An animation that represents an arrangement of haptic pulses of various durations and strengths by showing a set of thin vertical lines that symbolize sound waves. 

Play 

**Click.** Provides the sensation of a dial clicking, helping you communicate progress at predefined increments or intervals. Overusing the click haptic tends to diminish its utility and can even be confusing when clicks overlap each other.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Related)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Developer-documentation)

[Core Haptics](https://developer.apple.com/documentation/CoreHaptics)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Videos)

[<!-- image:  --> Practice audio haptic design ](https://developer.apple.com/videos/play/wwdc2021/10278)

[<!-- image:  --> Introducing Core Haptics ](https://developer.apple.com/videos/play/wwdc2019/520)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Change-log)

Date| Changes  
---|---  
May 7, 2024| Added guidance for playing haptics on Apple Pencil Pro.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Playing Video

|---  
Video codec| H.264 High Profile  
Video bit rate| 160 kbps at up to 30 fps  
Resolution (full screen)| 208x260 px (portrait orientation)  
Resolution (16:9)| 320x180 px (landscape orientation)  
Audio| 64 kbps HE-AAC  
  
**Avoid creating a poster image that looks like a system control.** You want people to understand that they can tap a movie element for playback; you don’t want to confuse people by making movie elements look like something else.

**Consider creating a poster image that represents a video clip’s contents.** When people tap a poster image, the system replaces the image with the video and begins inline playback. A relevant poster image can help people make an informed decision about whether to view the video. In general, avoid creating a poster image that has nothing to do with the content or that people might mistake for a control.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/playing-video#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/playing-video#Related)

[Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/playing-video#Developer-documentation)

[Configuring your app for media playback](https://developer.apple.com/documentation/AVFoundation/configuring-your-app-for-media-playback) — AVFoundation

[AVKit](https://developer.apple.com/documentation/AVKit)

[HTTP Live Streaming](https://developer.apple.com/streaming/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/playing-video#Videos)

[<!-- image:  --> Create a great video playback experience ](https://developer.apple.com/videos/play/wwdc2022/10147)

[<!-- image:  --> Explore video experiences for visionOS ](https://developer.apple.com/videos/play/wwdc2025/304)

[<!-- image:  --> Deliver a great playback experience on tvOS ](https://developer.apple.com/videos/play/wwdc2021/10191)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/playing-video#Change-log)

Date| Changes  
---|---  
September 12, 2023| Corrected the recommended width for a thumbnail in visionOS.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Printing

---
title: "Printing | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/printing

# Printing

An iOS, iPadOS, macOS, or visionOS app can integrate system-provided print functionality when it makes sense, presenting custom printer- and document-specific options if necessary.

<!-- image: A sketch of a printer, suggesting printing. The image is overlaid with rectangular and circular grid lines and is tinted orange to subtly reflect the orange in the original six-color Apple logo. -->

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/printing#Best-practices)

**Make printing discoverable.** Help people find your print action by placing it in standard system locations. For example, include a Print item in your macOS app’s File menu; in your iOS or iPadOS app, add a toolbar button that opens an [action sheet](https://developer.apple.com/design/human-interface-guidelines/action-sheets). If your macOS app has a toolbar, you might want to put a Print button there, too, but consider making it an optional button that people can add when they customize the toolbar.

**Present a printing option only when it’s possible.** If there’s nothing onscreen to print, or no printers are available, dim the Print item in a macOS app’s File menu and remove the Print action from the Action sheet in an iOS or iPadOS app. If you implement a custom print button, dim or hide it when printing isn’t possible.

**Present relevant printing options.** If it makes sense to offer options like selecting a page range, requesting multiple copies, or printing on both sides — and the printer supports the options — use the system-provided view to present them.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/printing#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or visionOS. Not supported in tvOS or watchOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/printing#macOS)

**If your macOS app offers app-specific print options that the system doesn’t offer, consider creating a custom category for the print panel.** By default, the print panel offers several categories of settings, such as Layout, Paper Handling, and Media & Quality. Give your custom category a unique name, such as your app name, and include options that help people have a great print experience in your app. For example, Keynote offers presentation-specific options, like the ability to print presenter notes, slide backgrounds, and skipped slides.

**If your app supports document-specific page settings, consider presenting a page setup dialog.** A _page setup dialog_ includes rarely changed settings for page size, orientation, and scaling that apply to printing a particular document. If this makes sense in your app, avoid implementing features the system already provides. For example, you don’t need to include options like changing the page orientation or printing in reverse order because the system implements these options.

**Make sure interdependencies between options are clear.** For example, if double-sided printing is available, an option to print on transparencies becomes unavailable.

**Separate advanced features from frequently used features.** Consider using a disclosure control to hide advanced options until they’re needed. Label advanced options as _Advanced Options_.

**Consider letting people preview the effect of a setting.** For example, you could update a thumbnail image to show the effect of changing a tone control.

**Consider storing modified settings with the document.** At minimum, it makes sense to store print settings until the document is closed in case people want to print it again.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/printing#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/printing#Related)

[File management](https://developer.apple.com/design/human-interface-guidelines/file-management)

[File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/printing#Developer-documentation)

[`UIPrintInteractionController`](https://developer.apple.com/documentation/UIKit/UIPrintInteractionController) — UIKit

[`NSDocument`](https://developer.apple.com/documentation/AppKit/NSDocument) — AppKit

---

## Reference: Ratings And Reviews

|---  
September 12, 2023| Added artwork.

---

## Reference: Searching

|---  
June 9, 2025| Updated best practices with general guidance from Search fields, and reorganized guidance for systemwide search.

---

## Reference: Settings

|---  
June 10, 2024| Reorganized some guidance into new topics and added game-specific examples.

---

## Reference: Undo And Redo

---
title: "Undo and redo | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo

# Undo and redo

Undo and redo gives people easy ways to reverse many types of actions, which can also help people explore and experiment safely as they learn a new interface or task.

<!-- image: A sketch of an arrow that starts right, curves upward, and points to the left, suggesting a return to the start. The image is overlaid with rectangular and circular grid lines and is tinted orange to subtly reflect the orange in the original six-color Apple logo. -->

People expect undo and redo to let them reverse their recent actions, so they’re likely to try undoing — often multiple times — until something changes. In a situation like this, people might not remember which of their previous actions an undo is targeting, which can lead to unintended changes and frustration. To help people remain in control, it’s essential to help people predict the outcome of undoing and redoing and to highlight the results.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Best-practices)

**Help people predict the results of undo and redo as much as possible.** On iPhone, for example, you can describe the result in the alert that displays when people shake the device, giving them the option of performing the undo or canceling it. If you provide undo and redo menu items, you can modify the menu item labels to identify the result. For example, a document-based app might use menu item labels like Undo Typing or Redo Bold.

**Show the results of an undo or redo.** Sometimes, the most recent action that people want to undo affects content or an area that’s no longer visible. In cases like this, it’s crucial to highlight the result of each undo and redo to keep people from thinking that the action had no effect, which can lead them to perform it repeatedly. For example, if people undo after deleting a paragraph in a document area that’s no longer onscreen, you might scroll the document to show the restored paragraph.

**Let people undo multiple times.** Avoid placing unnecessary limits on the number of times people can undo or redo. People generally expect to undo every action they’ve performed since taking a logical step like opening a document or saving their work.

**Consider giving people the option to revert multiple changes at once.** In some scenarios, people might appreciate the ability to undo a batch of discrete but related actions — like incremental adjustments to a single property or attribute — so they don’t have to undo each individual adjustment. In other cases, it can make sense to give people a convenient way to undo all the changes they made since opening a document or saving their work.

**Provide undo and redo buttons only when necessary.** People generally expect to initiate undo and redo in system-supported ways, such as choosing the items in a macOS app’s Edit menu, using keyboard shortcuts on a Mac or iPad, or shaking their iPhone. If it’s important to provide dedicated undo and redo buttons in your app, use the standard system-provided symbols and put the buttons in a toolbar.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Platform-considerations)

 _No additional considerations for visionOS. Not supported in tvOS or watchOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#iOS-iPadOS)

**Avoid redefining standard gestures for undo and redo.** For example, people can use a three-finger swipe to initiate an undo or redo, or shake their iPhone. As with all standard gestures, redefining them in your interface runs the risk of confusing people and making your experience unpredictable.

**Briefly and precisely describe the operation to be undone or redone.** The undo and redo alert title automatically includes a prefix of “Undo ” or “Redo ” (including the trailing space). You need to provide an additional word or two that describes what’s being undone or redone, to appear after this prefix. For example, you might create alert titles such as “Undo Name” or “Redo Address Change.”

### [macOS](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#macOS)

**Place undo and redo commands in the Edit menu and support the standard keyboard shortcuts.** Mac users expect to find undo and redo at the top of the Edit menu; they also expect to use Command–Z and Shift–Command–Z to perform undo and redo, respectively.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Related)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

[Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

[Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

[Edit menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Developer-documentation)

[`UndoManager`](https://developer.apple.com/documentation/Foundation/UndoManager) — Foundation

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo#Videos)

[<!-- image:  --> Essential Design Principles ](https://developer.apple.com/videos/play/wwdc2017/802)

---

## Reference: Workouts

|---  
<!-- image: A checkmark in a circle to indicate correct usage. -->| GPS is not used during a Pool Swim, and water may prevent a heart-rate measurement, but Apple Watch will still track your calories, laps, and distance using the built-in accelerometer.  
<!-- image: A checkmark in a circle to indicate correct usage. -->| In this type of workout, you earn the calorie equivalent of a brisk walk anytime sensor readings are unavailable.  
<!-- image: A checkmark in a circle to indicate correct usage. -->| GPS will only provide distance when you do a freestyle stroke. Water might prevent a heart-rate measurement, but calories will still be tracked using the built-in accelerometer.  
  
**Provide a summary at the end of a session.** A summary screen confirms that a workout is finished and displays the recorded information. Consider enhancing the summary by including Activity rings, so that people can easily check their current progress.

**Discard extremely brief workout sessions.** If a session ends a few seconds after it starts, either discard the data automatically or ask people if they want to record the data as a workout.

**Make sure text is legible for when people are in motion.** When a session requires movement, use large font sizes, high-contrast colors, and arrange text so that the most important information is easy to read.

**Use Activity rings correctly.** The Activity rings view is an Apple-designed element featuring one or more rings whose colors and meanings match those in the Activity app. Use them only for their documented purpose.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/workouts#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or watchOS. Not supported in macOS, tvOS, or visionOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/workouts#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/workouts#Related)

[Activity rings](https://developer.apple.com/design/human-interface-guidelines/activity-rings)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/workouts#Developer-documentation)

[WorkoutKit](https://developer.apple.com/documentation/WorkoutKit)

[Workouts and activity rings](https://developer.apple.com/documentation/HealthKit/workouts-and-activity-rings) — HealthKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/workouts#Videos)

[<!-- image:  --> Track workouts with HealthKit on iOS and iPadOS ](https://developer.apple.com/videos/play/wwdc2025/322)

[<!-- image:  --> Build custom workouts with WorkoutKit ](https://developer.apple.com/videos/play/wwdc2023/10016)

[<!-- image:  --> Build a workout app for Apple Watch ](https://developer.apple.com/videos/play/wwdc2021/10009)
